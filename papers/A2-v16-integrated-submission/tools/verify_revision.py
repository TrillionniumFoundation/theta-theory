#!/usr/bin/env python3
"""A2 v8 finite diagnostics. These checks are not proofs of the analytic theorems.
Run normally and with python -O. Explicit exceptions are never disabled by -O.
Requires SymPy. Does not evaluate exact finite-offset billiard probabilities.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
CHECKS: list[dict] = []

def check(name: str, value: bool, kind: str = 'exact_algebra') -> None:
    if not value:
        raise RuntimeError('Failed: '+name)
    CHECKS.append({'name':name,'kind':kind,'status':'pass'})

def exact(name: str, value: S.Expr) -> None:
    check(name, S.simplify(value) == 0)

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def sources(rel: str = 'main.tex', stack: tuple[str,...] = ()) -> list[tuple[str,str]]:
    if rel in stack:
        raise RuntimeError('Cyclic input: '+rel)
    text = (ROOT/rel).read_text()
    result=[(rel,text)]
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        result += sources(name+'.tex',stack+(rel,))
    return result

def main() -> dict:
    r = S.symbols('r',positive=True)
    g=S.Rational(1,2);R=S.Rational(1,4);A=S.symbols('A',positive=True)
    phi1=r/S.sqrt(g*(g+2*r));phi=[phi1,phi1/(2*(1+g/r)),phi1/(4*(1+g/r)**2-1)]
    table=[[S.simplify(S.diff(f,r,k).subs(r,R)/S.sqrt(2)) for k in range(4)] for f in phi]
    expected=[[S.Rational(1,4),S.Rational(3,4),-S.Rational(5,4),S.Rational(21,4)],
              [S.Rational(1,24),S.Rational(17,72),S.Rational(35,216),-S.Rational(491,216)],
              [S.Rational(1,140),S.Rational(297,4900),S.Rational(36243,171500),-S.Rational(4458537,6002500)]]
    for j in range(3):
        for k in range(4):exact(f'amplitude_derivative_{j+1}_{k}',table[j][k]-expected[j][k])
    D=S.Matrix([[S.sqrt(2)*(row[1]+S.pi*R*row[0]/(18*A))/A,
                 S.sqrt(2)*(-row[2]+5*S.pi*row[0]/(144*A))/A,
                 S.sqrt(2)*row[3]/(2*A)] for row in table])
    det=-2*S.sqrt(2)*(15804720*A+64253*S.pi)/(72930375*A**4)
    exact('physical_three_amplitude_determinant',D.det()-det)
    c=[3*S.sqrt(2)*row[0]/A for row in table]
    B=S.zeros(4);B[0,0]=c[0]
    for j in range(3):
        B[j+1,0]=-2*(j+1)*c[j]
        for k in range(3):B[j+1,k+1]=D[j,k]
    exact('limiting_four_window_determinant',B.det()-c[0]*det)
    check('reference_free_area_positive',bool(S.sqrt(3)/2-S.pi/16>0))
    # Independently differentiate an analytic polynomial remainder in coefficient coordinates.
    a,v,d=S.symbols('a v d',real=True);es=S.symbols('e1 e2 e3')
    cs=S.symbols('c1:4');ds=S.symbols('d0:9');bs=S.symbols('b1:4')
    means=[]
    for j,l in [(1,1),(1,2),(2,1),(3,1)]:
        amplitude=cs[j-1]+sum(ds[3*(j-1)+k]*es[k] for k in range(3))
        offset=l*a-j*v
        means.append(offset**2/(l*a)**2*(amplitude+offset*(bs[j-1]+sum(es))))
    M=S.Matrix(means).jacobian([v,*es]).subs({v:0,**dict.fromkeys(es,0)})
    M2=S.Matrix.vstack(M[1,:]-M[0,:],M[0,:],M[2,:],M[3,:])*S.diag(a,1,1,1)
    for i in range(4):
        for k in range(4):
            target=(cs[0] if k==0 else 0) if i==0 else (-2*i*cs[i-1] if k==0 else ds[3*(i-1)+k-1])
            exact(f'four_window_block_entry_{i}_{k}',S.limit(M2[i,k],a,0)-target)
    # Radius permutation generators in the actual support-family coordinates.
    T=S.Matrix([[1,1,0],[1,-S.Rational(1,2),S.sqrt(3)/2],[1,-S.Rational(1,2),-S.sqrt(3)/2]])
    rotation=S.diag(1,1,1);rotation[1:3,1:3]=S.Matrix([[-S.Rational(1,2),-S.sqrt(3)/2],[S.sqrt(3)/2,-S.Rational(1,2)]])
    permutation=T*rotation*T.inv()
    exact('radius_rotation_is_permutation',(permutation**3-S.eye(3)).norm())
    check('rotation_entries_zero_or_one',all(x in (0,1) for x in permutation))
    reflection=T*S.diag(1,1,-1)*T.inv()
    exact('radius_reflection', (reflection-S.Matrix([[1,0,0],[0,0,1],[0,1,0]])).norm())
    for m in range(1,9):
        weights=[(-1)**(l-1)*S.binomial(m,l) for l in range(1,m+1)]
        exact(f'extrapolation_mass_{m}',sum(weights)-1)
        for k in range(1,m):exact(f'extrapolation_moment_{m}_{k}',sum(w*l**k for l,w in enumerate(weights,1)))
        exact(f'joint_gap_exponent_{m}',2*(3+S.Rational(3,m))-(6+S.Rational(6,m)))
        # W<d*/12 and small h give admissibility even after an incorrect search.
        W=S.Rational(1,13);h=S.Rational(1,1000*(m+1));dstar=S.Integer(1)
        check(f'nuisance_failed_history_collar_{m}',bool(3*(W+h/2)+4*m*h<dstar))
    # The entropy direction permits p_delta=0; this is a model diagnostic, not billiard quadrature.
    for delta in (1e-2,1e-3,1e-4):
        for ratio in (.1,.5,1.,1.1,2.,10.,100.):
            d0=ratio*delta;p0=.25*d0*d0;p1=.25*max(d0-delta,0.)**2
            if p0>=.5:continue
            kl=(p1*math.log(p1/p0) if p1 else 0.)+(1-p1)*math.log((1-p1)/(1-p0))
            check(f'one_sided_gap_entropy_{delta}_{ratio}',kl<=2*delta**2+1e-15,'ordinary_float')
    for eta in (.249,.1,.01,1e-5):
        bound=(1-2*eta)*math.log((1-eta)/eta)
        check(f'confidence_log_{eta}',bound>=.25*math.log(1/eta),'ordinary_float')
    for q in (1e-2,1e-3,1e-4):
        omega=q**1.5;k=math.ceil(q**-2);nsub=math.floor(.7/q)
        check(f'supercritical_full_error_nonvanishing_{q}',k*omega>1,'ordinary_float')
        check(f'supercritical_subsample_error_{q}',nsub*omega<=.7*math.sqrt(q)+1e-14,'ordinary_float')
    active=sources();pat=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',re.S)
    active_blocks={blob(m.group(0).encode()) for _,text in active for m in pat.finditer(text)}
    baseline=[{'old_path':name,'environment':m.group(1),'git_blob_of_block':blob(m.group(0).encode())}
              for name,text in sources('history/main-v7.tex') for m in pat.finditer(text)]
    for i,item in enumerate(baseline):
        check(f'retained_formal_block_{i}',item['git_blob_of_block'] in active_blocks,'source_integrity')
    check('all_130_original_formal_blocks',len(baseline)==130,'source_integrity')
    labels=[x for _,text in active for x in re.findall(r'\\label\{([^}]+)\}',text)]
    check('no_duplicate_active_labels',len(labels)==len(set(labels)),'source_integrity')
    return {'schema':'a2-v8-diagnostics-v1','status':'pass','counts':{'total':len(CHECKS),**dict(Counter(x['kind'] for x in CHECKS))},
            'checks':CHECKS,'boundaries':['Exact algebra and source-integrity checks are distinct from ordinary floating-point diagnostics.',
              'No interval arithmetic, physical finite-offset probability solver, or formal proof assistant was used.',
              'The written analytic descent, inverse, entropy, and nuisance proofs are not certified by these finite tests.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'verification/diagnostics.json');args=parser.parse_args()
    result=main();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'counts':result['counts']},sort_keys=True))
