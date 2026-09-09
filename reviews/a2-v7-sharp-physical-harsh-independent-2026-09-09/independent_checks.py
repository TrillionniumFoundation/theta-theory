#!/usr/bin/env python3
"""Independent finite diagnostics for the two source-pinned A2 v7 reviews.

No repository/author/referee diagnostic modules are imported. These checks
are not physical billiard simulations, interval arithmetic, or proofs of
uniform nonlinear estimates. Run with Python 3, SymPy, and SciPy.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
import platform
import sympy as sp
import scipy
from scipy.integrate import quad

RESULTS: list[dict[str, str]] = []

def check(name: str, condition: bool, kind: str = "exact") -> None:
    if not bool(condition):
        raise RuntimeError(f"FAILED: {name}")
    RESULTS.append({"name": name, "kind": kind, "status": "pass"})

def zero(name: str, expression: sp.Expr) -> None:
    check(name, sp.simplify(expression) == 0)

def close(name: str, left: float, right: float, tol: float = 2e-10) -> None:
    check(name, math.isfinite(left) and math.isfinite(right)
          and abs(left-right) <= tol * max(1.0, abs(left), abs(right)),
          "ordinary_float")

def run() -> dict:
    # Exact Schur complements: genuinely unequal contacts and both parities.
    for case, (q, c0, g) in enumerate([
        (sp.Rational(1,3), sp.Rational(2), sp.Rational(1,2)),
        (sp.Rational(1,4), sp.Rational(3,2), sp.Rational(2,3)),
        (sp.Rational(1,3), sp.Rational(5,4), sp.Rational(3,4)),
    ]):
        c=(q+1/q)/2
        sh=(1/q-q)/2
        c1=c*c/c0
        a0=c*sh/(g*c1)
        a1=c*sh/(g*c0)
        for j in range(1,9):
            full=sp.zeros(j+1)
            for i in range(j+1):
                ci=c0 if i%2==0 else c1
                full[i,i]=ci/g if i in (0,j) else 2*ci/g
                if i<j:
                    full[i,i+1]=full[i+1,i]=-1/g
            inds=[0,j]
            h=full.extract(inds,inds)
            if j>1:
                middle=list(range(1,j))
                h-=full.extract(inds,middle)*full.extract(middle,middle).inv()*full.extract(middle,inds)
            aj=a0 if j%2==0 else a1
            mixed=a0 if j%2==0 else sh/g
            cot=(1+q**(2*j))/(1-q**(2*j))
            csc=2*q**j/(1-q**(2*j))
            expected=sp.Matrix([[a0*cot,-mixed*csc],[-mixed*csc,aj*cot]])
            check(f"jacobi_{case}_{j}_schur", h==expected)
            zero(f"jacobi_{case}_{j}_determinant", h.det()-a0*aj)
            zero(f"jacobi_{case}_{j}_physical_ratio", -h[0,1]/mixed-csc)

    # Physical radius coordinates and full permutation action.
    al, be, ze, R=sp.symbols('alpha beta zeta R', real=True)
    root3=sp.sqrt(3)
    xs=sp.Matrix([36*(al+be),36*(al-be/2+root3*ze/2),36*(al-be/2-root3*ze/2)])
    e1=sum(xs); e2=sum(xs[i]*xs[j] for i in range(3) for j in range(i+1,3)); e3=sp.prod(xs)
    zero('radius_e1',e1-108*al)
    zero('radius_e2',e2-(3888*al**2-972*(be**2+ze**2)))
    rotated=xs.subs({be:-be/2-root3*ze/2,ze:root3*be/2-ze/2},simultaneous=True)
    reflected=xs.subs(ze,-ze)
    check('rotation_cycles_radii',all(sp.simplify(rotated[i]-xs[(i+2)%3])==0 for i in range(3)))
    check('reflection_swaps_radii',reflected==sp.Matrix([xs[0],xs[2],xs[1]]))
    area1=sp.sqrt(3)/2-sp.pi*(R**2+2*R*al-sp.Rational(33,2)*al**2-sp.Rational(45,4)*(be**2+ze**2))
    area2=sp.sqrt(3)/2-sp.pi*R**2-sp.pi*R*e1/54+41*sp.pi*e1**2/7776-5*sp.pi*e2/432
    zero('physical_area_constraint',area1-area2)
    s=sp.symbols('s',positive=True)
    zero('opposite_path_e1',e1.subs({al:0,be:s,ze:0}))
    zero('opposite_path_e2_even',e2.subs({al:0,be:s,ze:0})-e2.subs({al:0,be:-s,ze:0}))
    zero('opposite_path_e3_difference',e3.subs({al:0,be:s,ze:0})-e3.subs({al:0,be:-s,ze:0})-23328*s**3)
    for sr in [sp.Rational(1,10000),sp.Rational(1,1000),sp.Rational(1,500)]:
        rr=sp.Rational(1,4)
        left=sorted([1/(rr+36*sr),1/(rr-18*sr),1/(rr-18*sr)])
        right=sorted([1/(rr-36*sr),1/(rr+18*sr),1/(rr+18*sr)])
        zero(f'curvature_matching_{sr}',max(abs(x-y) for x,y in zip(left,right))-36*sr/(rr**2-324*sr**2))

    # Independently differentiate the three physical amplitude functions.
    r,g=sp.symbols('r g',positive=True)
    phi1=r/sp.sqrt(g*(g+2*r))
    phis=[phi1,phi1/(2*(1+g/r)),phi1/(4*(1+g/r)**2-1)]
    table=[
        [sp.Rational(1,4),sp.Rational(3,4),-sp.Rational(5,4),sp.Rational(21,4)],
        [sp.Rational(1,24),sp.Rational(17,72),sp.Rational(35,216),-sp.Rational(491,216)],
        [sp.Rational(1,140),sp.Rational(297,4900),sp.Rational(36243,171500),-sp.Rational(4458537,6002500)]
    ]
    vals=[]
    for j,phi in enumerate(phis):
        vals.append([])
        for k in range(4):
            val=sp.simplify(sp.diff(phi,r,k).subs({r:sp.Rational(1,4),g:sp.Rational(1,2)}))
            vals[-1].append(val)
            zero(f'physical_amplitude_derivative_{j+1}_{k}',val/sp.sqrt(2)-table[j][k])
    A=sp.symbols('A',positive=True)
    J=sp.Matrix([[(v[1]+sp.pi*v[0]/(72*A))/A,(-v[2]+5*sp.pi*v[0]/(144*A))/A,v[3]/(2*A)] for v in vals])
    claimed=-2*sp.sqrt(2)*(15804720*A+64253*sp.pi)/(72930375*A**4)
    zero('physical_three_amplitude_determinant',J.det()-claimed)

    # Referee four-window comparison: g is unknown, not supplied.
    C1,C2,C3=sp.symbols('C1 C2 C3')
    entries=sp.symbols('a0:9')
    D=sp.Matrix(3,3,entries)
    limit=sp.Matrix([[C1,0,0,0],[-2*C1,*list(D.row(0))],[-4*C2,*list(D.row(1))],[-6*C3,*list(D.row(2))]])
    zero('four_window_scaled_jacobian',limit.det()-C1*D.det())
    # Original observation order gives the opposite determinant sign.
    original=sp.Matrix([[-2*C1,*list(D.row(0))],[-C1,*list(D.row(0))],[-4*C2,*list(D.row(1))],[-6*C3,*list(D.row(2))]])
    zero('four_window_original_order',original.det()+C1*D.det())

    # Exact heterogeneous raw product overlap, independently enumerated.
    specifications=[(Fraction(1,7),[1,2,3],[2,3,4]),(Fraction(2,9),[1,2],[2,3]),(Fraction(1,4),[1,2,3,4],[3,4,5,6])]
    marginals=[]
    for p,L,U in specifications:
        lp={'fail':1-p}; rp={'fail':1-p}
        lp.update({str(x):p/len(L) for x in L}); rp.update({str(x):p/len(U) for x in U})
        marginals.append((lp,rp))
    for n in (1,2,3):
        overlap=Fraction(0)
        for point in product(*(sorted(set(L)|set(U)) for L,U in marginals[:n])):
            p=math.prod(marginals[i][0].get(x,Fraction(0)) for i,x in enumerate(point))
            q=math.prod(marginals[i][1].get(x,Fraction(0)) for i,x in enumerate(point))
            overlap+=min(p,q)
        formula=math.prod(1-p*(1-Fraction(len(set(L)&set(U)),len(L))) for p,L,U in specifications[:n])
        check(f'heterogeneous_raw_overlap_{n}',overlap==formula)

    # Independent ordinary quadrature of the geometric intersection area.
    for q in (.02,.2,.5,.8):
        lam=(1-q)/(1+q)
        angle=math.atan(math.sqrt(lam))
        area=2*quad(lambda t:min(1.0,1/(lam*math.cos(t)**2+math.sin(t)**2/lam)),0,math.pi/2,points=[angle],epsabs=1e-12)[0]
        close(f'polar_overlap_q{q}',1-area/math.pi,2*math.asin(q)/math.pi)
    for b in (.2,1.,3.):
        q=2.**-20
        k=round(b/q)
        tv=-math.expm1(k*math.log1p(-2*math.asin(q)/math.pi))
        close(f'critical_tangent_b{b}',tv,1-math.exp(-2*b/math.pi),tol=2e-6)
    q=sp.Rational(1,2)**20; d=q*q; k=1/q**2
    check('supercritical_full_error_does_not_vanish_example',k*d==1 and k*q>1000)
    check('supercritical_projected_error_vanishes_example',100*d/q<sp.Rational(1,1000))

    # Bernoulli entropy inequalities: floats are not proof certificates.
    for p in (1e-5,.001,.05,.2):
        for factor in (.8,1.05,1.4):
            q=p*factor
            kl=p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
            upper=(p-q)**2/(q*(1-q))
            check(f'bernoulli_kl_{p}_{factor}',-1e-13<=kl<=upper+1e-13,'ordinary_float')
    for eta in (.249,.1,.01,1e-5):
        binary=(1-2*eta)*math.log((1-eta)/eta)
        check(f'confidence_log_{eta}',binary>=math.log(1/eta)/4,'ordinary_float')

    # Exhaustive all-outcome width recursions, with memoized rational states.
    W=Fraction(1,8)
    for scale in range(1,8):
        h=W/(2**scale)
        @lru_cache(None)
        def widths(w: Fraction) -> tuple[Fraction,int]:
            if w<=h/2:
                return Fraction(0),0
            children=[widths(w/2),widths(3*w/4)]
            return 1/(w*w)+max(v for v,n in children),1+max(n for v,n in children)
        exposure,stages=widths(W)
        check(f'bracket_all_history_cost_{scale}',h*h*exposure<Fraction(64,7))
        upper=math.ceil(math.log(2*float(W/h))/math.log(4/3))
        check(f'bracket_all_history_stages_{scale}',stages<=upper)
    for m in range(1,7):
        weights=[(-1)**(l-1)*math.comb(m,l) for l in range(1,m+1)]
        for power in range(m):
            val=sum(w*l**power for l,w in enumerate(weights,1))
            check(f'extrapolation_m{m}_degree{power}',val==(1 if power==0 else 0))
        check(f'harmonic_m{m}',sum(Fraction(w,l) for l,w in enumerate(weights,1))==sum(Fraction(1,l) for l in range(1,m+1)))
        for jj in (3,4):
            L=jj+1
            check(f'pilot_second_stage_margin_m{m}_J{jj}',Fraction(L)-Fraction(3*jj,4)>1 and Fraction(L*m)+Fraction(3*jj,4)>0)

    return {
        'schema':'a2-v7-independent-finite-checks-v1',
        'status':'pass',
        'environment':{'python':platform.python_version(),'sympy':sp.__version__,'scipy':scipy.__version__},
        'counts':{'total':len(RESULTS),'by_kind':dict(sorted(Counter(x['kind'] for x in RESULTS).items()))},
        'checks':RESULTS,
        'nonclaims':[
            'No source or earlier diagnostic suite was imported.',
            'No positive-offset billiard probabilities were numerically computed.',
            'No physical billiard simulation, interval arithmetic, PDF build, or formal proof assistant was run.',
            'The analytic descent and local fixed-offset inverse are justified in the written comparison, not by these finite checks.',
            'Finite identities do not certify uniform infinite-dimensional estimates or publication significance.'
        ]
    }

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding='utf-8')
    else:
        print(data,end='')

if __name__=='__main__':
    main()
