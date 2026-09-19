#!/usr/bin/env python3
"""Source, exact-identity and numerical diagnostics for A2 revision 88.

These checks are reproducibility evidence, not a formal proof checker.
Run from the manuscript directory, or pass --base explicitly.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
import sympy as sp
from reconstruct_v88 import normalization_system, reconstruct


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def obs(u, v, alpha, roots, clocks):
    f = np.array([[np.prod(t-np.asarray(rs)) for rs in roots] for t in clocks])
    weights = f * np.asarray(alpha)[None, :]
    weights /= weights.sum(axis=1)[:, None]
    return np.array([u @ np.diag(w) @ v.T for w in weights])


def channel(m, k):
    return .35*np.eye(m, k) + .65*np.ones((m, k))/m


def exact_system(polys, nodes):
    z = sp.Symbol('z')
    k, d = len(polys), sp.degree(polys[0], z)
    u = (sp.eye(k)+sp.ones(k))/(k+1)
    v = (2*sp.eye(k)+sp.ones(k))/(k+2)
    q = sp.expand(sum(polys)/k)
    p = [u*sp.diag(*[f.subs(z, t)/k for f in polys])*v.T/q.subs(z, t)
         for t in nodes]
    w = sp.Matrix([[t**r for r in range(d+1)] for t in nodes])
    residuals = w.T.nullspace()
    cols = []
    for r in range(d):
        entries = []
        for row in residuals:
            block = sp.zeros(k)
            for j,t in enumerate(nodes):
                block += row[j]*t**r*p[j]
            entries.extend(list(block))
        cols.append(sp.Matrix(entries))
    return sp.Matrix.hstack(*cols), q, p, u, v


def canonical_from_factors(u, v, alpha, xi):
    # Diagnostic evaluation of the proven residue formula; the point estimator
    # does not use these factors. Basis invariance is checked independently.
    q1, _ = np.linalg.qr(u)
    q2, _ = np.linalg.qr(v)
    s, t = q1.T @ u, q2.T @ v
    si, ti = np.linalg.inv(s), np.linalg.inv(t)
    residues = [ti.T @ np.diag((xi == x)/alpha) @ si for x in np.unique(xi)]
    beta = sum(np.linalg.norm(r, 2) for r in residues)
    h = float(alpha @ xi)
    a = u @ np.diag(alpha) @ v.T
    b = u @ np.diag(alpha*(h-xi)) @ v.T
    gamma = np.linalg.norm(b)
    kappa = np.linalg.svd(u, compute_uv=False)[-1]*np.linalg.svd(v, compute_uv=False)[-1]
    eta = 1/(beta+1/gamma) if gamma > 0 else 0.
    theta = kappa*gamma/(kappa+gamma) if gamma > 0 else 0.
    leading_inverse = np.linalg.inv(q1.T @ a @ q2)
    check(np.linalg.norm(sum(residues)-leading_inverse) < 1e-9*max(1,beta),
          'Residues must sum to the leading inverse')
    check(beta + 1e-9 >= np.linalg.norm(leading_inverse,2), 'Lower beta bound')
    check(beta <= len(alpha)/(alpha.min()*kappa)*(1+1e-9), 'Upper beta bound')
    rot1,_ = np.linalg.qr(np.arange(1,len(alpha)**2+1).reshape(len(alpha),-1)+np.eye(len(alpha)))
    rot2,_ = np.linalg.qr(np.diag(np.arange(1,len(alpha)+1))+np.ones((len(alpha),len(alpha))))
    rotated_beta = sum(np.linalg.norm(rot2.T@r@rot1,2) for r in residues)
    check(abs(rotated_beta-beta) < 1e-9*max(1,beta), 'Orthonormal frame invariance')
    return beta, gamma, kappa, eta, theta


def run(base: Path, review_base: str | None):
    results = {}
    z, h, x, u, t1, t2 = sp.symbols('z h x u t1 t2')
    h0 = (t1-h)*(t2-h)
    slope = 1+u*(h-x)/h0
    xu = (x+u*(1+(h-x)*(t1+t2-h)/h0))/slope
    qb = 1+(h-x)*(t1+t2-h-z)/h0
    check(sp.cancel((z-x)-u*qb-slope*(z-xu)) == 0, 'Exact pole-shift polynomial')
    check(sp.cancel(sp.diff(xu,u).subs(u,0)-(t1-x)*(t2-x)/h0) == 0, 'Gauge derivative')
    results['symbolic_affine_gauge'] = 'passed'

    cases = [
        [[1],[1],[2]], [[1],[1],[1]],
        [[1,2],[1,3],[4,5]], [[1,2],[1,3],[1,4]], [[1,2],[1,2],[1,2]],
        [[1,2,3],[1,2,4],[2,4,5]], [[1,2,3],[1,2,4],[1,2,5]],
        [[1,2,3],[1,2,3],[1,2,3]], [[1,1,2],[2,3,4],[3,4,5]]]
    rows = []
    for root_lists in cases:
        d = len(root_lists[0])
        polys = [sp.prod(z-a for a in roots).expand() for roots in root_lists]
        nmat, q, _, _, _ = exact_system(polys, list(range(7, 7+2*d+1)))
        gcd = polys[0]
        for f in polys[1:]: gcd = sp.gcd(gcd,f)
        nu = int(sp.degree(gcd,z))
        check(d-nmat.rank() == nu, 'Exact normalization nullity equals gcd degree')
        for i in range(nu):
            rpoly = sp.div(q,gcd,z)[0]*z**i
            coeff = sp.Matrix([sp.expand(rpoly).coeff(z,j) for j in range(d)])
            check(nmat*coeff == sp.zeros(nmat.rows,1), 'Kernel basis q/g times monomials')
        rows.append({'degree':d,'roots':root_lists,'gcd_degree':nu,'rank':int(nmat.rank())})
    results['exact_kernel_cases'] = rows

    polys = [(z-1)*(z-3), (z-2)*(z-4)]
    nodes = [6,7,8,9]
    nmat,q,p,cu,cv = exact_system(polys,nodes)
    check(nmat.rank() == 1, 'Four-clock quadratic defect')
    coeff = nmat.nullspace()[0]
    rp = sp.expand(coeff[0]+coeff[1]*z)
    hp = [sp.interpolate([(t,sp.cancel(rp.subs(z,t)*polys[b].subs(z,t)/(2*q.subs(z,t))))
                          for t in nodes[:3]], z).expand() for b in range(2)]
    displacement = sp.Rational(1,10**6)
    wu = [sp.expand(polys[b]/2+displacement*hp[b]) for b in range(2)]
    qu = q+displacement*rp
    for j,t in enumerate(nodes):
        pu = cu*sp.diag(*[f.subs(z,t) for f in wu])*cv.T/qu.subs(z,t)
        check(all(sp.cancel(a-b)==0 for a,b in zip(pu,p[j])), 'Exact four-clock fibre')
    fnew = [f/sp.Poly(f,z).LC() for f in wu]
    check(sp.cancel(sp.prod(fnew)-sp.prod(polys)) != 0, 'Fibre changes aggregate roots')
    shifted_roots = [float(sp.re(v)) for f in fnew for v in sp.nroots(f)]
    check(all(0 < x < 5 for x in shifted_roots), 'Fibre remains in action interval')
    check(all(sp.Poly(f,z).LC()>sp.Rational(1,10) for f in wu), 'Interior weight floor')
    results['exact_four_clock_quadratic_fibre'] = {'passed': True, 'r':str(rp),
                                                  'shifted_roots':shifted_roots}

    rng = np.random.default_rng(20260919)
    algorithm_tests = []
    for roots, clocks in [([[-.6],[.1],[.7]], np.array([2.,3.,5.])),
                          ([[-.6],[-.6],[.7]], np.array([2.,3.,5.])),
                          ([[-.8,-.1],[-.1,.6],[.25,.8]], np.linspace(2,5,5)),
                          ([[.1,.1],[-.5,.5],[-.8,.8]], np.linspace(2,5,5)),
                          ([[-.8,-.2,.4],[-.65,.1,.65],[-.4,.3,.85]],np.linspace(2,5,7))]:
        d,k = len(roots[0]),len(roots)
        uu,vv = channel(k+1,k),channel(k+2,k)
        alpha = np.full(k,1/k)
        pp = obs(uu,vv,alpha,roots,clocks)
        truth = np.sort(np.ravel(roots))
        nmat,_ = normalization_system(pp,clocks,d)
        tau = np.linalg.svd(nmat,compute_uv=False)[-1]
        kap = np.linalg.svd(uu,compute_uv=False)[-1]*np.linalg.svd(vv,compute_uv=False)[-1]
        if d==1:
            beta,gamma,_,_,_=canonical_from_factors(uu,vv,alpha,np.ravel(roots))
            qr,_=np.linalg.qr(np.vander(clocks,2,increasing=True),mode='complete')
            hh=float(alpha@np.ravel(roots))
            expected_tau=gamma*np.linalg.norm(qr[:,2:].T@(1/(clocks-hh)))
            check(abs(expected_tau-tau)<1e-12,'Affine normalization equals contrast times clock factor')
        for noise in [0.,1e-10,1e-8]:
            perturb = rng.normal(size=pp.shape)
            perturb -= perturb.mean(axis=(1,2),keepdims=True)
            perturb /= max(np.linalg.norm(v) for v in perturb)
            fit = reconstruct(pp+noise*perturb, clocks,d,k,(-1.,1.))
            check(fit.status=='reconstructed', 'Regular synthetic reconstruction')
            error = float(np.max(np.abs(fit.roots-truth)))
            if noise==0.: check(error < (1e-5 if d==3 else 1e-7), 'Noiseless root reconstruction up to roundoff')
            algorithm_tests.append({'degree':d,'roots':roots,'noise':noise,'error':error,
                                    'tau':float(tau),'kappa':float(kap),
                                    'predicted_scale':float((noise*(1/kap+1/tau))**(1/d))})
    results['floating_point_reconstruction'] = algorithm_tests

    beta1 = canonical_from_factors(np.eye(3),np.eye(3),np.ones(3)/3,np.array([-.51,-.49,.5]))[0]
    beta0 = canonical_from_factors(np.eye(3),np.eye(3),np.ones(3)/3,np.array([-.5,-.5,.5]))[0]
    check(abs(beta1-9)<1e-12 and abs(beta0-6)<1e-12, 'Strict semicontinuity example')
    results['residue_collision_example'] = {'before':beta1,'at_collision':beta0}

    family_rows=[]
    for k,m1,m2 in [(2,2,3),(3,4,5),(4,5,6)]:
        basis1 = np.linalg.qr(np.eye(m1)[:,1:]-np.eye(m1)[:,:1])[0]
        basis2 = np.linalg.qr(np.eye(m2)[:,1:]-np.eye(m2)[:,:1])[0]
        ee,ff = basis1[:,0],basis2[:,0]
        alpha=np.ones(k)/k; xi=np.linspace(-.7,.7,k)
        center=(xi[0]+xi[1])/2; b0=(xi[1]-xi[0])/2
        pole=float(alpha@xi); clocks=np.array([2.,3.,5.]); t=.1*b0
        epsu,epsv=.001,.002
        def family(tt):
            lam=1-tt/b0
            uu=np.tile(np.ones(m1)[:,None]/m1,(1,k)); vv=np.tile(np.ones(m2)[:,None]/m2,(1,k))
            uu[:,0]+=epsu*ee/(2*lam); uu[:,1]-=epsu*ee/(2*lam)
            vv[:,0]+=epsv*ff/(2*lam); vv[:,1]-=epsv*ff/(2*lam)
            for b in range(2,k): uu[:,b]+=.025*basis1[:,b-1]; vv[:,b]+=.025*basis2[:,b-1]
            xx=xi.copy(); xx[0]+=tt; xx[1]-=tt
            return uu,vv,xx,obs(uu,vv,alpha,[[x] for x in xx],clocks)
        uu,vv,xx,pp=family(t); _,_,_,p0=family(0)
        for j,clock in enumerate(clocks):
            want=(clock-center)/(2*k*(clock-pole))*epsu*epsv*((1-t/b0)**-2-1)*np.outer(ee,ff)
            check(np.linalg.norm(pp[j]-p0[j]-want)<1e-14,'Exact product-family identity')
            check(np.linalg.norm((pp[j]-p0[j]).sum(axis=0))<1e-14,'Fixed first marginal')
            check(np.linalg.norm((pp[j]-p0[j]).sum(axis=1))<1e-14,'Fixed second marginal')
        beta,gamma,kap,eta,theta=canonical_from_factors(uu,vv,alpha,xx)
        expected_kappa=epsu*epsv/(2*(1-t/b0)**2)
        check(abs(kap-expected_kappa)<1e-10*expected_kappa, 'Exact product kappa')
        av=uu@np.diag(alpha)@vv.T
        smallest_a=np.linalg.svd(av,compute_uv=False)[k-1]
        check(abs(smallest_a-kap/k)<1e-9*kap, 'Exact leading singular value')
        family_rows.append({'k':k,'eta_over_product':eta/(epsu*epsv),
                            'theta_over_product':theta/(epsu*epsv),'gamma':gamma})
        # Collapse identity with independently well-conditioned channels.
        uu,vv=channel(m1,k),channel(m2,k)
        zz=np.linspace(-1,1,k); spread=.03; shift=.08
        base_x=spread*zz; moved_x=base_x+shift
        p0=obs(uu,vv,alpha,[[x] for x in base_x],clocks)
        p1=obs(uu,vv,alpha,[[x] for x in moved_x],clocks)
        bb=-spread*uu@np.diag(alpha*zz)@vv.T
        for j,clock in enumerate(clocks):
            check(np.linalg.norm(p1[j]-p0[j]-shift*bb/((clock-shift)*clock))<1e-14,
                  'Exact collapse-family identity')
    results['least_favourable_family_diagnostics']=family_rows

    # Verify all article inputs and references without calling TeX.
    tex='\n'.join(p.read_text() for p in sorted((base/'article/v88').glob('*.tex')))
    import re
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',tex)
    check(len(labels)==len(set(labels)),'Unique TeX labels')
    check(set(refs)<=set(labels),'All internal references resolve')
    cites=set(x for group in re.findall(r'\\cite\{([^}]+)\}',tex) for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',tex))
    check(cites<=bib,'All citations have bibliography entries')
    files=sorted((base/'article/v88').glob('*.tex'))+[base/'rigidity_v88.tex']
    results['source_sha256']={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    results['source_structure']={'labels':len(labels),'citations':len(cites),'passed':True}
    if review_base:
        repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=base,text=True).strip())
        subprocess.run(['git','merge-base','--is-ancestor',review_base,'HEAD'],cwd=repo,check=True)
        diff=subprocess.check_output(['git','diff','--name-status',review_base,'HEAD'],cwd=repo,text=True)
        check(all(line.startswith('A\t') for line in diff.splitlines()),'Every inherited file is unchanged')
        old=base/'article/v87/paper.tex'
        blob=subprocess.check_output(['git','hash-object',str(old)],cwd=repo,text=True).strip()
        check(blob=='45abc130f8bcebb347abbe895498b1a568bc7e7b','Reviewed v87 source blob retained')
        results['preservation']={'review_base':review_base,'all_changes_additive':True,'v87_blob':blob}
    else:
        results['preservation']={'status':'not_run_locally_without_full_repository',
                                 'required_remote_check':'--review-base 976d23ef269126e68dd90c4c9d3184ee67ff0b54'}
    return {'status':'passed','scope':'finite symbolic/numerical/source diagnostics, not formal proof certification',
            'numpy':np.__version__,'sympy':sp.__version__,'checks':results}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--review-base')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=run(args.base,args.review_base)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'output':str(args.output)},indent=2))


if __name__=='__main__':
    main()
