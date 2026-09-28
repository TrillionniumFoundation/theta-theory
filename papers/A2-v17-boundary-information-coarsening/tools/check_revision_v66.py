#!/usr/bin/env python3
"""Exact preservation and finite controls for the written v66 proof.

Finite checks do not prove an infinite half-line identity, analyticity, or
exceptional significance.  No assertions are removed under python -O.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, re, stat
import numpy as np
import sympy as sp
from scipy.linalg import solve_banded

P=Path(__file__).resolve().parents[1]
ARCH=P/'history/v65-review-baseline'
CHANGED={'README.md','main.tex','rigidity.tex',
         'article/00_structural_introduction_v48.tex',
         'journal/00_principal_introduction_v61.tex',
         'journal/references_v56.tex','v5/references_v43.tex'}

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def git_blob(b: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def graph(entry: str, old: bool=False, seen: set[str]|None=None) -> set[str]:
    seen=set() if seen is None else seen
    if entry in seen: return seen
    seen.add(entry)
    path=(ARCH/entry) if old and entry in CHANGED else (P/entry)
    text=path.read_text()
    # This graph contains no escaped percent immediately before an input.
    text='\n'.join(re.split(r'(?<!\\)%',line)[0] for line in text.splitlines())
    for raw in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',text):
        require(re.fullmatch(r'[A-Za-z0-9_./-]+',raw) is not None,'Dynamic input')
        graph(raw if raw.endswith('.tex') else raw+'.tex',old,seen)
    return seen

def preservation() -> dict:
    manifest=json.loads((ARCH/'SOURCE_MANIFEST.json').read_text())
    require(digest((ARCH/'SOURCE_MANIFEST.json').read_bytes())=='d0a70195757be19de9b4cda07fb1daea1fd37a95d224ede4906f5226a344ce9d','Baseline manifest changed')
    changed=[]
    for n,d in manifest['files'].items():
        path=P/n;require(path.is_file(),'Missing inherited path: '+n)
        b=path.read_bytes()
        mode='100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
        require(mode==d['mode'],'Inherited mode changed: '+n)
        if digest(b)!=d['sha256']:
            changed.append(n);require(n in CHANGED,'Unexpected inherited edit: '+n)
            b=(ARCH/n).read_bytes()
        require(len(b)==d['bytes'] and digest(b)==d['sha256'] and git_blob(b)==d['git_blob'],'Original byte mismatch: '+n)
    require(set(changed)==CHANGED,'Wrong changed-path set')
    oldgraphs={e:graph(e+'.tex',True) for e in ('main','rigidity','two_collision')}
    newgraphs={e:graph(e+'.tex') for e in oldgraphs}
    for e in oldgraphs:require(oldgraphs[e]<=newgraphs[e],'Lost active proof input: '+e)
    old=set().union(*oldgraphs.values());new=set().union(*newgraphs.values())
    require(len(old)==131,'Unexpected baseline active graph')
    proof=(P/'article/10c_global_curvature_inverse_v66.tex').read_text()
    types=re.findall(r'\\begin\{(lemma|theorem|proposition|corollary)\}',proof)
    require(types==['lemma','theorem','theorem','proposition'],'Unexpected new proof statement list')
    require(proof.count('\\begin{proof}')==4 and proof.count('\\end{proof}')==4,'Incomplete proof environments')
    return {'inherited_files_verified':len(manifest['files']),
            'inherited_files_unchanged':len(manifest['files'])-len(changed),
            'changed_originals_archived':sorted(changed),
            'old_active_union':len(old),'new_active_union':len(new),
            'new_active_inputs':sorted(new-old),
            'active_counts':{e:len(g) for e,g in newgraphs.items()},
            'new_proved_statements':len(types),
            'scope':'Byte/mode and active-input retention; no semantic certificate of all inherited proofs.'}

def sample(r: int, h: int) -> tuple[list[F],list[F],list[F],list[F]]:
    k=[F(5+(i%3),4) for i in range(r)]
    a=[F(2+((2*i+h)%3),16) for i in range(r)]
    c=[F(0) for _ in range(r)]
    for i in range(r):
        j=(i+1)%r;c[j]=(k[i]/a[i]-k[i]-k[j]+k[j]*a[j])/2
    s=[k[i]+c[i]-k[i]*a[i] for i in range(r)]
    require(min(c)>0 and min(s)>0,'Nonpositive rational model')
    return k,a,c,s

def phi(k: list[float],s: list[float],z: list[float]) -> list[float]:
    return [max(s[i]-k[i]+k[i]**2/(k[i]+s[(i+1)%len(k)]+z[(i+1)%len(k)]),0.) for i in range(len(k))]

def finite_hessians(k: list[float],c: list[float],length: int=240) -> np.ndarray:
    r=len(k);out=[]
    for b in range(r):
        n=length-1; ab=np.zeros((3,n)); rhs=np.zeros(n);rhs[0]=k[b]
        for j in range(1,length):
            i=(b+j)%r;ab[1,j-1]=k[(i-1)%r]+k[i]+2*c[i]
        for j in range(1,length-1):
            v=-k[(b+j)%r];ab[0,j]=v;ab[2,j-1]=v
        x=solve_banded((1,1),ab,rhs)
        out.append(k[b]+c[b]-k[b]*x[0])
    return np.array(out)

def controls() -> dict:
    schur=blocks=iters=pairs=0; max_inverse=0.;max_finite=0.;max_jacobian=0.
    for r in range(2,10):
        for h in range(5):
            k,a,c,s=sample(r,h)
            for i in range(r):
                j=(i+1)%r
                require(s[i]==k[i]+c[i]-k[i]**2/(k[i]+c[j]+s[j]),'Schur identity')
                require(a[i]==k[i]/(k[i]+c[j]+s[j]),'Tail ratio')
                schur+=1
            q=max((k[i]/(k[i]+s[(i+1)%r]))**2 for i in range(r))
            require(q<1,'Contraction bound')
            kf,sf,cf=map(lambda arr:list(map(float,arr)),(k,s,c))
            z=[0.]*r; z1=phi(kf,sf,z);start=max(map(abs,z1));qf=float(q)
            for m in range(1,25):
                z=phi(kf,sf,z)
                err=max(abs(z[i]-cf[i]) for i in range(r))
                require(err<=qf**m/(1-qf)*start+2e-13,'Iteration bound')
                iters+=1
            max_inverse=max(max_inverse,err)
            fh=finite_hessians(kf,cf)
            max_finite=max(max_finite,float(np.max(np.abs(fh-np.array(sf)))))
            _,_,ct,st=sample(r,h+1)
            qs=max((k[i]/(k[i]+min(s[(i+1)%r],st[(i+1)%r])))**2 for i in range(r))
            require(max(abs(c[i]-ct[i]) for i in range(r)) <= (1+qs)/(1-qs)*max(abs(s[i]-st[i]) for i in range(r)),'Pair Lipschitz')
            pairs+=1
            if h==0 and r<=7:
                T=sp.zeros(r)
                for i in range(r):T[i,(i+1)%r]=sp.Rational(a[i]**2)
                C=(sp.eye(r)-T).inv()*(sp.eye(r)+T)
                require((sp.eye(r)-T)*C==sp.eye(r)+T,'Exact curvature derivative')
                direction=np.arange(1,r+1,dtype=float)/(r+1);step=1e-4
                plus=finite_hessians(kf,list(np.array(cf)+step*direction))
                minus=finite_hessians(kf,list(np.array(cf)-step*direction))
                errj=float(np.max(np.abs((plus-minus)/(2*step)-np.array(C,dtype=float)@direction)))
                max_jacobian=max(max_jacobian,errj)
                for n in range(2,9):
                    U=sp.zeros(r);sig=[(-1 if i%2==0 else 1)*a[i] for i in range(r)]
                    for i in range(r):U[i,(i+1)%r]=sp.Rational(sig[i]**n)
                    B=(sp.eye(r)+U)*(sp.eye(r)-U).inv();lam=sp.prod(sig)
                    require(sp.simplify(B.det()-(1-(-1)**r*lam**n)/(1-lam**n))==0,'Signed determinant')
                    require(B*(sp.eye(r)-U)*(sp.eye(r)+U).inv()==sp.eye(r),'Signed inverse')
                    blocks+=1
    require(max_finite<1e-11 and max_jacobian<1e-7 and max_inverse<1e-11,'Numerical tolerance')
    # A positive vector outside the strictly positive-curvature image.
    k=[F(1),F(1)];s=[F(1,10),F(10)];z=[F(0),F(109,11)]
    require([max(s[i]-k[i]+k[i]**2/(k[i]+s[1-i]+z[1-i]),F(0)) for i in range(2)]==z,'Nonimage control')
    # Closed two-contact inverse, including its square-root simplification.
    for h in range(6):
        c0=sp.Rational(h+1,4);c1=sp.Rational(h+3,5);g=sp.Rational(7,5)
        C0=1+g*c0;C1=1+g*c1;H=sp.sqrt(C0*C1)
        s0=sp.sqrt(C0/C1)*sp.sqrt(C0*C1-1)/g
        s1=sp.sqrt(C1/C0)*sp.sqrt(C0*C1-1)/g
        require(sp.simplify((H*sp.sqrt(s0/s1)-1)/g-c0)==0,'Two-site inverse 0')
        require(sp.simplify((H*sp.sqrt(s1/s0)-1)/g-c1)==0,'Two-site inverse 1')
    return {'exact_schur_sites':schur,'exact_signed_blocks':blocks,
            'contraction_iteration_controls':iters,'exact_pair_lipschitz_controls':pairs,
            'finite_dirichlet_models':40,'finite_dirichlet_length':240,
            'maximum_iteration_error':max_inverse,'maximum_finite_schur_error':max_finite,
            'finite_difference_curvature_jacobians':6,'maximum_jacobian_error':max_jacobian,
            'positive_nonimage_control':True,'exact_two_site_specializations':6,
            'scope':'Exact rational identities and finite floating-point controls; written proofs supply infinite-dimensional and exact global conclusions.'}

def main() -> None:
    print(json.dumps({'preservation':preservation(),'controls':controls()},indent=2,sort_keys=True))
if __name__=='__main__':main()
