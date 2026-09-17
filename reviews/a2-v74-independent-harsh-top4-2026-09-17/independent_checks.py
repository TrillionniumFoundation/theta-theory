#!/usr/bin/env python3
"""Independent v74 referee diagnostics, not a proof or realization certificate.

Usage: python independent_checks.py [--native-dir DIRECTORY]
Requires SymPy. Optional native-dir contains the downloaded workflow artifact.
No network access, repository writes, or assertions disabled by python -O.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
import sympy as S

u, v = S.symbols('u v', real=True)
Q = S.Rational
checks: list[dict] = []

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def zero(expr, name: str) -> None:
    items = list(expr) if isinstance(expr, S.MatrixBase) else [expr]
    require(all(S.cancel(x) == 0 for x in items), name)

def integ(expr, x):
    return S.integrate(S.expand(expr), (x, -1, 1))

def compress(f):
    M = S.Matrix([[integ(f, v), integ(v*f, v)]])
    N = S.Matrix([integ(f, u), integ(u*f, u)])
    H = S.Matrix([[integ(integ(u**i*v**j*f, v), u)
                   for j in range(2)] for i in range(2)])
    return M, N, H

def algebra() -> None:
    # A nonsymmetric example prevents a transpose error from passing accidentally.
    a = S.Matrix([1+u, 2-u+u*u])
    b = S.Matrix([1+2*v, 3-v*v])
    C = S.Matrix([[2, 3], [-1, 4]])
    f = (a.T*C*b)[0]
    M, N, H = compress(f)
    require(H.det() != 0 and H != H.T, 'nonsymmetric test degeneracy')
    zero((M*H.inv()*N)[0]-f, 'moment reconstruction')
    require(S.cancel((M*H.T.inv()*N)[0]-f) != 0, 'transpose negative control')
    checks.append({'test':'nonsymmetric moment identity and transpose negative control',
                   'passed':True, 'determinant':str(H.det())})

    cases=[]
    for p in (Q(1,2), Q(-1,2), Q(3,4), Q(-3,4)):
        A=-p*u+u*u/20
        Cact=p*v+v*v/30
        w=1+u/10+u*u/20
        z=1-v/7+v*v/25
        raw=w*z*(4-A-Cact)
        Z=integ(integ(raw,v),u)
        f=S.expand(raw/Z)
        M,N,H=compress(f)
        W,V=integ(w,u),integ(z,v)
        covw=integ(u*A*w,u)/W-integ(u*w,u)*integ(A*w,u)/W**2
        covz=integ(v*Cact*z,v)/V-integ(v*z,v)*integ(Cact*z,v)/V**2
        zero(H.det()+W**2*V**2*covw*covz/Z**2, 'covariance determinant')
        zero((M*H.inv()*N)[0]-f, 'weighted factor reconstruction')
        require(H.det()>0 and Z>0, 'positive determinant')
        # On [-1,1], w>=.9, z>=6/7, |A'|>=|p|-.1,
        # |C'|>=|p|-1/15, and 4-A-C >= 4-2|p|-1/12 > 0.
        require(4-2*abs(p)-Q(1,12)>0, 'positive residual floor')
        cases.append({'p':str(p),'det_H':str(H.det())})
    checks.append({'test':'positive weighted models, both obliquity signs',
                   'passed':True,'cases':cases})

    f=(4+u/2-v/2)/16
    q=lambda x:x*x-Q(1,3)
    perturbed=f+q(u)*q(v)/100
    M,N,H=compress(f)
    M2,N2,H2=compress(perturbed)
    zero(M2-M,'invisible weighted profiles M')
    zero(N2-N,'invisible weighted profiles N')
    zero(H2-H,'invisible moment matrix')
    zero((M2*H2.inv()*N2)[0]-f,'surrogate recovers only rank-two part')
    require(S.expand(perturbed-f)!=0,'nonzero rank defect')
    coeff=S.Matrix([[S.expand(perturbed).coeff(u,i).coeff(v,j)
                     for j in range(3)] for i in range(3)])
    require(coeff.rank()==3,'perturbation rank three')
    require(Q(3,16)-Q(4,900)>0,'perturbed density remains positive')
    checks.append({'test':'nonzero positive rank-three density in compression fiber',
        'passed':True,'det_H':str(H.det()),'rank':3,
        'limitation':'Generic kernel example, not an actual billiard counterexample.'})

    normal=4-u*u/5-v*v/7
    normal/=integ(integ(normal,v),u)
    _,_,Hnormal=compress(normal)
    require(Hnormal.det()==0,'normal incidence singularity')
    coeff=S.Matrix([[S.expand(normal).coeff(u,i).coeff(v,j)
                     for j in range(3)] for i in range(3)])
    require(coeff.rank()==2,'normal incidence still rank two')
    checks.append({'test':'normal-incidence rank-two singular first-moment matrix',
                   'passed':True})

    R,p,d=S.symbols('R p d',positive=True)
    f=(d+p*u-p*v)/(4*R**2*d)
    HR=S.Matrix([[S.integrate(u**i*v**j*f,(u,-R,R),(v,-R,R))
                  for j in range(2)] for i in range(2)])
    zero(HR.det()-p*p*R**4/(9*d*d),'gate conditioning formula')
    checks.append({'test':'affine-model gate and obliquity conditioning',
                   'passed':True,'det_H':'p^2 R^4 / (9 d^2)'})

    grid=0
    for m in range(3,9):
        for s in range(1,6):
            den=2*(m+s)+1
            alpha=Q(s,den); gamma=Q(s,m+s+2)
            zero(Q(1,2)-Q(2*m+1,2*den)-alpha,'variance balance')
            zero(1-Q(m+2,m+s+2)-gamma,'readout balance')
            require(alpha>Q(s,2*(m+s)+2),'sample exponent strict gain')
            require(gamma>Q(s,m+s+3),'readout exponent strict gain')
            require(1-Q(m+1,den)>=alpha,'Bernstein envelope absorption')
            require(alpha<Q(1,2),'count error absorption')
            omega,Gamma=Q(2,3),Q(7,5)
            beta=alpha*omega/(omega+alpha*Gamma)
            zero(alpha-beta*alpha*Gamma/omega-beta,'budget balance')
            grid+=1
    checks.append({'test':'sample, readout, count and budget exponent balances',
                   'passed':True,'integer_pairs':grid})

def git_object(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def provenance(native: Path) -> dict:
    manifest=json.loads((native/'frozen-source-manifest.json').read_text())
    tree={}; verified=0
    with zipfile.ZipFile(native/'native-source.zip') as archive:
        expected={'SOURCE_MANIFEST.json'}|{'source/'+x for x in manifest['files']}
        require(set(archive.namelist())==expected,'unexpected source archive entries')
        for name,entry in manifest['files'].items():
            info=archive.getinfo('source/'+name)
            data=archive.read(info)
            require(len(data)==entry['bytes'],'source length '+name)
            require(hashlib.sha256(data).hexdigest()==entry['sha256'],'source SHA256 '+name)
            blob=git_object('blob',data)
            require(blob==entry['git_blob'],'source Git blob '+name)
            mode=format((info.external_attr>>16)&0o777777,'o')
            require(mode==entry['mode'],'source ZIP mode '+name)
            node=tree
            parts=name.split('/')
            for part in parts[:-1]: node=node.setdefault(part,{})
            node[parts[-1]]=(entry['mode'],blob)
            verified+=1
    def build(node):
        entries=[]
        for name,value in node.items():
            if isinstance(value,dict): mode,sha='40000',build(value); key=name+'/'
            else: mode,sha=value; key=name
            entries.append((key.encode(),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
        return git_object('tree',b''.join(x[1] for x in sorted(entries)))
    actual=build(tree)
    require(actual==manifest['source_tree'],'reconstructed manuscript Git tree')
    files={}
    for name in ('rigidity.pdf','main.pdf','two_collision.pdf','native-source.zip'):
        data=(native/name).read_bytes()
        files[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    return {'source_files_verified':verified,'source_tree_reconstructed':actual,
            'source_commit':manifest['source_commit'],'native_files':files,
            'local_TeX_rebuild':False,'proof_certification':False}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-dir',type=Path)
    args=parser.parse_args()
    algebra()
    out={'schema':1,'status':'passed','python_optimization':sys.flags.optimize,
         'sympy_version':S.__version__,'checks':checks,
         'scope':'Independent finite algebra diagnostics; not a uniform theorem proof, physical realization, minimax certificate or journal decision.'}
    if args.native_dir: out['provenance']=provenance(args.native_dir)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
