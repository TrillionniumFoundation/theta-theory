#!/usr/bin/env python3
"""Reproducible diagnostics for A2 v87; NOT mathematical proof certification.

Run from the paper directory. Native LaTeX builds remain separate checks.
An optional source archive verifies local preservation. In GitHub CI,
--review-base verifies that the revision adds files and changes no old file.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import tarfile
import sys
import numpy as np
import sympy as sp

REVIEW = "18de3872c705b5be9582429567877aac8d1a5fbe"
INHERITED_SOURCE = "bf67e3f33d394c80d7d7daeb51e52de12ec3d180"
CLOCKS = np.array([5.0, 6.0, 8.0])


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def close(a, b, message: str, atol: float = 3e-11, rtol: float = 2e-9) -> float:
    aa, bb = np.asarray(a), np.asarray(b)
    error = float(np.max(np.abs(aa - bb)))
    require(bool(np.allclose(aa, bb, atol=atol, rtol=rtol)), f"{message}: error={error}")
    return error


def symbolic_checks() -> dict:
    T, T1, T2, h, x, u, a = sp.symbols("T T1 T2 h x u a")
    H = (T1-h)*(T2-h)
    q = a*(1+(h-x)*(T1+T2-h-T)/H)
    au = a*(1+u*(h-x)/H)
    xu = (x+u*(1+(h-x)*(T1+T2-h)/H))/(1+u*(h-x)/H)
    expressions = {
        "first_clock_interpolant": q.subs(T,T1)-a*(T1-x)/(T1-h),
        "second_clock_interpolant": q.subs(T,T2)-a*(T2-x)/(T2-h),
        "gauge_affine_identity": au*(T-xu)-(a*(T-x)-u*q),
        "gauge_derivative": sp.diff(xu,u).subs(u,0)-(T1-x)*(T2-x)/H,
    }
    s, t, e, q1, q2 = sp.symbols("s t e q1 q2")
    expressions["determinant_cancellation"] = (s-e*q1)*(t-e*q2)-s*t+e*(s*q2+t*q1)-e**2*q1*q2
    lam, d, epsu, epsv, um, vm, z = sp.symbols("lam d epsu epsv um vm z")
    pair = ((T-z+lam*d)*(um+epsu/(2*lam))*(vm+epsv/(2*lam))
            +(T-z-lam*d)*(um-epsu/(2*lam))*(vm-epsv/(2*lam)))
    expressions["general_rank_pair_interaction"] = pair-pair.subs(lam,1)-(T-z)*epsu*epsv*(lam**-2-1)/2
    B, shift = sp.symbols("B shift")
    expressions["collapse_identity"] = B/(T-h-shift)-B/(T-h)-shift*B/((T-h-shift)*(T-h))
    for name, expr in expressions.items():
        require(sp.cancel(expr) == 0, name)
    return {"passed": list(expressions), "count": len(expressions)}


def helmert(m: int) -> np.ndarray:
    columns = []
    for j in range(1,m):
        v = np.zeros(m); v[:j] = 1; v[j] = -j
        columns.append(v/np.sqrt(j*(j+1)))
    return np.column_stack(columns)


def observe(U, V, alpha, xi, clocks=CLOCKS):
    h = float(alpha @ xi)
    return np.array([(U*(alpha*(T-xi)/(T-h))) @ V.T for T in clocks])


def signal(U, V, alpha, xi):
    h = float(alpha @ xi)
    B = (U*(alpha*(h-xi))) @ V.T
    kap = float(np.linalg.svd(U,compute_uv=False)[-1]*np.linalg.svd(V,compute_uv=False)[-1])
    gam = float(np.linalg.norm(B))
    theta = kap*gam/(kap+gam) if kap+gam else 0.0
    return h, B, kap, gam, theta


def random_model(rng, k, m1, m2, repeat=False):
    U = rng.uniform(.1,1,(m1,k)); U /= U.sum(axis=0)
    V = rng.uniform(.1,1,(m2,k)); V /= V.sum(axis=0)
    alpha = np.full(k,1/k)
    xi = np.linspace(.3,3.6,k)
    if repeat and k >= 3:
        xi[1] = xi[0]
    return U,V,alpha,xi


def curve_and_pencil_checks() -> dict:
    rng = np.random.default_rng(8701)
    count = 0; worst_identity = 0.0; worst_recovery = 0.0
    for k in range(2,7):
        for m1,m2 in [(k,k),(k+1,k+2)]:
            for repeat in [False,True]:
                U,V,alpha,xi = random_model(rng,k,m1,m2,repeat)
                h,B,kap,gam,theta = signal(U,V,alpha,xi)
                P = observe(U,V,alpha,xi)
                A = (U*alpha)@V.T
                worst_identity = max(worst_identity, close(P, np.array([A+B/(T-h) for T in CLOCKS]), "rational curve"))
                X,Y = P[0]-P[1],P[1]-P[2]
                ratio = np.sum(X*Y)/np.sum(Y*Y)
                c = (CLOCKS[1]-CLOCKS[0])/(CLOCKS[2]-CLOCKS[1]); z=ratio/c
                recovered_h=(z*CLOCKS[0]-CLOCKS[2])/(z-1)
                worst_recovery=max(worst_recovery,close(recovered_h,h,"pole recovery",atol=2e-8))
                cleared = np.array([(T-h)*p for T,p in zip(CLOCKS,P)])
                L=np.linalg.pinv(U); R=np.linalg.pinv(V).T
                for T,K in zip(CLOCKS,cleared):
                    worst_identity=max(worst_identity,close(L@K@R,np.diag(alpha*(T-xi)),"true-channel diagonalization",atol=2e-8))
                # A competing model, including repeated spectra, tests the exact
                # coefficient decomposition before any inverse inequality.
                Up,Vp,ap,xp=random_model(rng,k,m1,m2,not repeat)
                hp=float(ap@xp); Pp=observe(Up,Vp,ap,xp)
                for j in [0,1]:
                    T=CLOCKS[j]
                    Fj=(T-hp)*L@(Pp[j]-P[j])@R
                    target=np.diag(alpha*(T-xi))-(hp-h)*np.diag(alpha*(T-xi)/(T-h))+Fj
                    close(L@((T-hp)*Pp[j])@R,target,"candidate identity",atol=2e-8)
                # Explicit two-clock gauge, including preservation of normalization.
                shift=.01; H=(CLOCKS[0]-h)*(CLOCKS[1]-h)
                aq=alpha*(1+shift*(h-xi)/H)
                xq=(xi+shift*(1+(h-xi)*(CLOCKS[0]+CLOCKS[1]-h)/H))/(1+shift*(h-xi)/H)
                close(aq.sum(),1,"gauge weight sum")
                close(aq@xq,h+shift,"gauge pole")
                Pg=observe(U,V,aq,xq)
                close(Pg[:2],P[:2],"two-clock fibre")
                require(np.linalg.norm(Pg[2]-P[2])>1e-10,"third clock must resolve gauge")
                count+=1
    # Real diagonal perturbations with multiplicity and highly nonnormal
    # triangular competitors: a diagnostic of the multiset matching lemma.
    matching=0
    for k in range(2,12):
        diag=np.sort(rng.integers(0,4,k)).astype(float)
        for typ in ["symmetric","triangular"]:
            E=rng.normal(size=(k,k))*.02
            E=(E+E.T)/2 if typ=="symmetric" else np.triu(E)
            values=np.linalg.eigvals(np.diag(diag)+E)
            require(np.max(abs(values.imag))<1e-10,"real-spectrum diagnostic")
            error=np.max(abs(np.sort(values.real)-diag))
            require(error<=(2*k-1)*np.linalg.norm(E,2)+1e-10,"matching bound")
            matching+=1
    return {"model_cases":count,"matching_cases":matching,"max_identity_error":worst_identity,"max_pole_error":worst_recovery}


def lower_family(k,m1,m2,epsu,epsv,t):
    d=.4; center=.8; lam=1-t/d
    xi=np.concatenate(([center-d+t,center+d-t],np.linspace(1.8,3.6,k-2))) if k>2 else np.array([center-d+t,center+d-t])
    alpha=np.full(k,1/k)
    eu,ev=helmert(m1),helmert(m2)
    U=np.full((m1,k),1/m1);V=np.full((m2,k),1/m2)
    U[:,0]+=epsu*eu[:,0]/(2*lam);U[:,1]-=epsu*eu[:,0]/(2*lam)
    V[:,0]+=epsv*ev[:,0]/(2*lam);V[:,1]-=epsv*ev[:,0]/(2*lam)
    for b in range(2,k):
        U[:,b]+=.03*eu[:,b-1];V[:,b]+=.03*ev[:,b-1]
    return U,V,alpha,xi,eu[:,0],ev[:,0]


def singular_family_checks() -> dict:
    cases=0; zero_cases=0; err=0.0; floors=[]; theta_ratios=[]
    clocks=np.array([5.,5.4,6.,6.5,7.9,8.])
    for k in range(2,7):
        for m1,m2 in [(k,k),(k+1,k+2)]:
            for epsu,epsv in [(0.,0.),(0.,.004),(.005,0.),(.001,.001),(.002,.009),(.0001,.007)]:
                base=lower_family(k,m1,m2,epsu,epsv,0)
                U,V,alpha,xi,e,f=base
                P0=observe(U,V,alpha,xi,clocks)
                h=float(alpha@xi)
                for t in [.04,.12]:
                    U,V,alpha,xi,e,f=lower_family(k,m1,m2,epsu,epsv,t)
                    Pt=observe(U,V,alpha,xi,clocks); lam=1-t/.4
                    rhs=np.array([(T-.8)/(2*k*(T-h))*epsu*epsv*(lam**-2-1)*np.outer(e,f) for T in clocks])
                    err=max(err,close(Pt-P0,rhs,"higher-rank least-favourable identity",atol=5e-15))
                    close(Pt.sum(axis=1),P0.sum(axis=1),"first marginal",atol=5e-15)
                    close(Pt.sum(axis=2),P0.sum(axis=2),"second marginal",atol=5e-15)
                    floors.append(float(min(U.min(),V.min(),Pt.min())))
                    _,_,kap,gam,theta=signal(U,V,alpha,xi)
                    if epsu*epsv:
                        close(kap,epsu*epsv/(2*lam**2),"exact weakest singular product",atol=1e-15,rtol=5e-8)
                        theta_ratios.append(theta/(epsu*epsv))
                    else:
                        close(Pt,P0,"exact singular fibre",atol=5e-15);zero_cases+=1
                    cases+=1
    require(min(floors)>0,"uniform positivity diagnostic")
    return {"cases":cases,"exact_zero_contrast_cases":zero_cases,"max_identity_error":err,"minimum_tested_cell_or_channel_probability":min(floors),"theta_over_product_range":[min(theta_ratios),max(theta_ratios)]}


def collapse_checks() -> dict:
    rng=np.random.default_rng(8702);cases=0;err=0.0;ratios=[]
    for k in range(2,7):
        U,V,alpha,_=random_model(rng,k,k+1,k+2)
        z=np.linspace(-1,1,k);z-=alpha@z
        for spread in [0.,1e-4,.001,.05]:
            a=1.5;t=.2;xi0=a+spread*z;xit=xi0+t
            P0=observe(U,V,alpha,xi0);Pt=observe(U,V,alpha,xit)
            _,B,kap,gam,theta=signal(U,V,alpha,xi0)
            rhs=np.array([t*B/((T-a-t)*(T-a)) for T in CLOCKS])
            err=max(err,close(Pt-P0,rhs,"whole-spectrum collapse",atol=5e-15))
            if spread:
                ratios.append(theta/spread)
            else:
                close(Pt,P0,"constant spectrum fibre",atol=5e-15)
            cases+=1
    return {"cases":cases,"max_identity_error":err,"theta_over_spread_range":[min(ratios),max(ratios)]}


def box_ls(A,b,lo,hi):
    candidates=[]
    h=np.linalg.lstsq(A,b,rcond=None)[0]
    if np.all(h>=lo) and np.all(h<=hi):candidates.append(h)
    for j in [0,1]:
        ell=1-j
        for value in [lo[j],hi[j]]:
            h=np.zeros(2);h[j]=value
            h[ell]=np.clip(A[:,ell]@(b-value*A[:,j])/(A[:,ell]@A[:,ell]),lo[ell],hi[ell])
            candidates.append(h)
    return min(((float(np.linalg.norm(A@h-b)),h) for h in candidates),key=lambda q:q[0])


def anchor_checks() -> dict:
    T=np.array([3.,5.]);x=np.array([.2,.5,1.,1.6]);k=np.array([.7,.4])
    r=(T[None,:]-x[:,None])*k;hstar=1/k;b=np.full(4,T[0]-T[1]);lo=np.array([.5,.5]);hi=np.array([4.,4.])
    patterns=list(itertools.product([0,1],repeat=4)); matrices=[]
    for pattern in patterns:
        chosen=np.where(np.array(pattern)[:,None],1/r,r)
        matrices.append(chosen*np.array([1.,-1.]))
    active=[i for i,A in enumerate(matrices) if np.linalg.norm(A@hstar-b)<1e-10]
    require(bool(active),"active shared pattern")
    lam=min(np.linalg.svd(matrices[i],compute_uv=False)[-1] for i in active)
    d=min(box_ls(A,b,lo,hi)[0] for i,A in enumerate(matrices) if i not in active)
    require(lam>0 and d>0,"positive anchor certificate")
    eps=min(1e-8,d*1e-6);rp=r+eps*np.sin(np.arange(8).reshape(4,2))
    candidates=[]
    for i,pattern in enumerate(patterns):
        chosen=np.where(np.array(pattern)[:,None],1/rp,rp)
        residual,h=box_ls(chosen*np.array([1.,-1.]),b,lo,hi)
        candidates.append((residual,i,h))
    residual,i,h=min(candidates,key=lambda q:q[0])
    require(i in active,"finite-pattern stability diagnostic")
    require(np.linalg.norm(h-hstar)<=100*eps/lam,"anchor calibration diagnostic")
    return {"label_patterns":len(patterns),"active_patterns":len(active),"lambda":float(lam),"inactive_residual_margin":float(d),"perturbation":eps,"calibration_error":float(np.linalg.norm(h-hstar))}


def tex_graph(root: Path, entry: str):
    paths=[];chunks=[]
    def walk(name,stack):
        file=(root/name).with_suffix('.tex')
        require(file.exists(),f"missing input: {file}")
        rel=file.relative_to(root).as_posix()
        require(rel not in stack,f"input cycle: {rel}")
        text=re.sub(r'(?<!\\)%[^\n]*','',file.read_text())
        paths.append(rel);chunks.append(text)
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):
            walk(child,stack+[rel])
    walk(entry,[])
    text='\n'.join(chunks)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    refs=re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}',text)
    bibs=re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text)
    cites=[x.strip() for group in re.findall(r'\\cite(?:p|t)?(?:\[[^\]]*\])*\{([^}]+)\}',text) for x in group.split(',')]
    duplicates=[k for k,v in collections.Counter(labels).items() if v>1]
    duplicate_bibs=[k for k,v in collections.Counter(bibs).items() if v>1]
    return {"files":paths,"labels":labels,"citations":bibs,"missing_references":sorted(set(refs)-set(labels)),"missing_citations":sorted(set(cites)-set(bibs)),"duplicate_labels":duplicates,"duplicate_bibkeys":duplicate_bibs}


def source_checks(root: Path, archive: Path | None, review_base: str | None) -> dict:
    graphs={}
    for entry in ['rigidity_v87.tex','rigidity_v87_companion.tex']:
        g=tex_graph(root,entry)
        for field in ['missing_references','missing_citations','duplicate_labels','duplicate_bibkeys']:
            require(not g[field],f"{entry}: {field}: {g[field]}")
        graphs[entry]=g
    old=tex_graph(root,'rigidity_v86_full.tex')
    exemption={'rigidity_v86_full.tex','article/v86/frontmatter.tex','article/v86/principal_body.tex'}
    retained=set(old['files'])-exemption
    require(retained<=set(graphs['rigidity_v87_companion.tex']['files']),"missing inherited mathematical input")
    require(set(old['labels'])<=set(graphs['rigidity_v87_companion.tex']['labels']),"missing inherited theorem/equation label")
    hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in sorted(set(sum([g['files'] for g in graphs.values()],[])))}
    aggregate=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    preservation={"retained_inherited_tex_inputs":len(retained),"retained_inherited_labels":len(set(old['labels'])),"excluded_old_wrappers":sorted(exemption)}
    if archive:
        repo=root.parent.parent;checked=0
        with tarfile.open(archive,'r:gz') as tf:
            for member in tf:
                if not member.isfile():continue
                local=repo/member.name
                require(local.is_file(),f"lost inherited archive file: {member.name}")
                data=tf.extractfile(member).read()
                require(hashlib.sha256(data).digest()==hashlib.sha256(local.read_bytes()).digest(),f"changed inherited file: {member.name}")
                checked+=1
        preservation.update({"archive_files_byte_identical":checked,"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"archive_source_commit":INHERITED_SOURCE})
    if review_base:
        repo=root.parent.parent
        diff=subprocess.check_output(['git','diff','--name-status',review_base,'HEAD'],cwd=repo,text=True)
        changes=[line.split('\t') for line in diff.splitlines() if line]
        require(all(row[0]=='A' for row in changes),f"non-additive change against review base: {changes}")
        preservation.update({"git_review_base":review_base,"git_added_paths":len(changes),"git_modified_or_deleted_paths":0})
    return {"graphs":{e:{"input_files":len(g['files']),"labels":len(g['labels']),"bibliography_keys":len(g['citations']),**{key:g[key] for key in ['missing_references','missing_citations','duplicate_labels','duplicate_bibkeys']}} for e,g in graphs.items()},"source_graph_sha256":aggregate,"source_file_sha256":hashes,"preservation":preservation}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--review-base')
    args=parser.parse_args()
    report={"revision":87,"review_commit":REVIEW,"status":"failed","scope":"Symbolic identities, finite numerical diagnostics, TeX source integrity and source preservation; NOT proof certification."}
    try:
        report.update(symbolic=symbolic_checks(),curve_and_pencil=curve_and_pencil_checks(),product_families=singular_family_checks(),spectrum_collapse=collapse_checks(),shared_anchors=anchor_checks(),source=source_checks(args.base.resolve(),args.archive,args.review_base))
        report['status']='passed'
    except Exception as exc:
        report['error']=f"{type(exc).__name__}: {exc}"
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        raise
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source'},indent=2))
    print('Source graphs, citations, references, and preservation: passed')
    return 0


if __name__=='__main__':
    sys.exit(main())
