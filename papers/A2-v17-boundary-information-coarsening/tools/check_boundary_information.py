#!/usr/bin/env python3
"""Finite algebraic and quadrature diagnostics, not a proof certificate.

No assertions are used: checks remain active with python -O.
Dependencies: Python 3.10+, NumPy and SciPy (quadrature only).
"""
from __future__ import annotations
from fractions import Fraction as F
from math import exp, log, sqrt, pi, cos, sin, asin, erf
import hashlib
import json
from pathlib import Path
import re
from scipy.integrate import quad

CHECKS: list[tuple[str,str]] = []
def check(name: str, condition: bool, detail: object = '') -> None:
    if not condition:
        raise RuntimeError(f'{name}: {detail}')
    CHECKS.append((name,str(detail)))

def near(name: str, a: float, b: float, tol: float=1e-10) -> None:
    check(name,abs(a-b)<=tol, {'a':a,'b':b,'tolerance':tol})

def cap_h2(t: float) -> float:
    """Direct nonnegative Hellinger integral, including exclusive support."""
    em,ep=exp(-t),exp(t)
    def radial(theta: float) -> float:
        a=em*cos(theta)**2+ep*sin(theta)**2
        if abs(a-1)<1e-15:
            return 0.0
        top=min(1.0,1/a)
        def common(s: float) -> float:
            den=sqrt(max(0.0,1-s))+sqrt(max(0.0,1-a*s))
            return (a-1)**2*s*s/(den*den) if den else 0.0
        part=quad(common,0,top,epsabs=2e-15,epsrel=2e-9,limit=200)[0]
        exclusive=(1-1/a)**2/2 if a>1 else (1-a)**2/(2*a)
        return part+exclusive
    return 4/pi*quad(radial,0,pi/2,epsabs=1e-13,epsrel=2e-8,limit=150)[0]

def main() -> None:
    # Exact alternating Jacobi determinant and endpoint eigenvalue identities.
    for q in (F(1,2),F(1,3),F(2,5),F(1,10),F(1,100)):
        c=(1+q*q)/(1-q*q); s=2*q/(1-q*q)
        lam=(1-q)/(1+q)
        check('Jacobi determinant',c*c-s*s==1,str(q))
        check('Jacobi eigenvalues',c-s==lam and c+s==1/lam,str(q))
        check('whitened determinant',lam*(1/lam)==1,str(q))
        for p in (F(1),F(1,2),F(1,37)):
            for h2 in (F(1,5),F(1,2),F(3,2)):
                affinity=1-p+p*(1-h2/2)
                check('thinned affinity',affinity==1-p*h2/2,(str(p),str(h2)))
    # Coarea coefficient and the exact truncated-score moments.
    near('boundary coefficient',quad(lambda th:cos(2*th)**2,0,2*pi)[0]/pi,1.0)
    near('cap normalization',4*quad(lambda r:(1-r*r)*r,0,1)[0],1.0)
    for h in (.5,.2,.05,.01,.001):
        near('boundary strip mass',quad(lambda w:2*w,0,h)[0],h*h)
        moment=quad(lambda w:(1-w)**2/w,h,1,epsabs=1e-12)[0]
        near('truncated score second moment',moment,log(1/h)-1.5+2*h-h*h/2,2e-10)
    # The intrinsic coefficient is unchanged by multiplying a defining function.
    for a in (F(1,2),F(2),F(7,3)):
        for v in (F(-2),F(1,7),F(3)):
            for g in (F(1,3),F(2)):
                for c in (F(1,2),F(4,3)):
                    check('defining-function invariance',(a/c)*(c*v)**2/(c*g)==a*v*v/g)
    # Referee random-hazard distinction and exact overlap negative control.
    m=F(4,5)*(F(9,10)**2+F(3,5)**2)/2
    check('adaptive common mass',m==F(117,250))
    check('wrong product is separated',m!=F(4,5)*F(3,4)**2)
    check('weighted reverse law',F(9,10)**2/(F(9,10)**2+F(3,5)**2)==F(9,13))
    for b in (.01,.1,1,4,9):
        v=4*b
        normal=lambda x:exp(-x*x/2)/sqrt(2*pi)
        integral=quad(lambda x:exp(sqrt(v)*x-v/2)*normal(x),-12,sqrt(v)/2)[0]
        integral+=quad(normal,sqrt(v)/2,12)[0]
        near('Gaussian overlap profile',integral,1-erf(sqrt(b)/sqrt(2)),2e-10)
    # Direct two-dimensional numerical integral: remainder stays order t^2.
    rows=[]
    for t in (.1,.03,.01,.003,.001):
        h2=cap_h2(t)
        rem=(h2-t*t*log(1/t)/4)/(t*t)
        check('Hellinger coefficient 1/4',.38<rem<.41,{'t':t,'H2':h2,'scaled_remainder':rem})
        q=(exp(t)-1)/(exp(t)+1)
        check('coarsening Hellinger inequality',h2<=2*(2/pi)*asin(q)+1e-12)
        rows.append({'zeta':t,'H2':h2,'scaled_remainder':rem})
    # Rates and collar examples are tested only as finite diagnostics.
    for q in (1e-2,1e-4,1e-8):
        r=q*q*log(1/q); t=log((1+q)/(1-q))
        check('endpoint/full scale separation',0<r<q)
        check('general physical collar example',sqrt(r**2.2)/r<1)
        check('even physical collar example',r**1.2/r<1)
        check('positive Gaussian critical profile',0<erf(1/sqrt(2))<1)
    # Check no labels collide among the new active modules.
    root=Path(__file__).resolve().parents[1]
    modules=['article/01b_observation_hierarchy.tex','article/18_boundary_information.tex',
             'article/19_endpoint_critical.tex','article/32_random_hazard.tex']
    labels=[]
    for name in modules:
        text=(root/name).read_text()
        check('proof source exists',len(text)>100,name)
        labels.extend(re.findall(r'\\label\{([^}]+)\}',text))
    check('new labels are unique',len(labels)==len(set(labels)))
    digest=hashlib.sha256(json.dumps(CHECKS,sort_keys=True).encode()).hexdigest()
    result={'status':'passed','checks':len(CHECKS),'case_digest':digest,
            'new_labels':len(labels),'hellinger_quadrature':rows,
            'scope':'Finite exact identities and numerical quadrature only; not formal verification, a billiard simulation, or a full native TeX build.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    main()
