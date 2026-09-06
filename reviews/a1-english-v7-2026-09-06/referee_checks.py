#!/usr/bin/env python3
"""Independent finite diagnostics for A1 v7, not a proof verifier.

Run: python referee_checks.py --output INDEPENDENT_DIAGNOSTICS.json
Requires Python 3.10+ and SymPy. No manuscript or author code is imported.
Rational identities are exact; the rectangle sweep is explicitly floating-point.
The program writes only the requested JSON receipt.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib, json, math, platform, sys, time
import sympy as sp

SUBMISSION = '02f68484cf92ef312037cf455bd3f3737ae4facd'
CHECKS: list[dict] = []

def check(name: str, predicate: bool, **details) -> None:
    CHECKS.append(dict(name=name, passed=bool(predicate), **details))
    if not predicate:
        raise AssertionError(name)

# Actual monomial exponents, not an author polynomial implementation.
Poly = dict[F, F]
def multiply(p: Poly, q: Poly) -> Poly:
    out = defaultdict(F)
    for a, x in p.items():
        for b, y in q.items():
            out[a+b] += x*y
    return {a:x for a,x in out.items() if x}

def add(*polys: Poly) -> Poly:
    out = defaultdict(F)
    for p in polys:
        for a,x in p.items(): out[a] += x
    return {a:x for a,x in out.items() if x}

def scale(p: Poly, c: F) -> Poly:
    return {a:c*x for a,x in p.items() if c*x}

def prod(polys: list[Poly]) -> Poly:
    ans = {F(0):F(1)}
    for p in polys: ans = multiply(ans,p)
    return ans

@lru_cache(None)
def moment(s: F, prior: str='uniform', jet: int=0) -> F:
    """Integral t^s (log t)^jet / jet! under specified full-support priors."""
    if prior == 'uniform': return F((-1)**jet)/(s+1)**(jet+1)
    if prior == 'density_3t2': return F(3*(-1)**jet)/(s+3)**(jet+1)
    if prior == 'quarter_uniform_three_quarters_delta1':
        return F(1,4)*moment(s,'uniform',jet) + (F(3,4) if jet==0 else 0)
    raise ValueError(prior)

def integral(p: Poly, prior: str, shift: F=F(0), jet: int=0) -> F:
    return sum((x*moment(a+shift,prior,jet) for a,x in p.items()), F(0))

def mat(entries) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in entries])

def normalized_jacobian(theta: F, prior: str, desingularized: bool) -> sp.Matrix:
    D=2+theta
    factors=[{F(0):F(1,2),D:c/2} for c in (F(1,100),F(3,100),F(7,100))]
    P=prod(factors); ev=integral(P,prior)
    tests=[(F(1),0),(F(2),0),(D+1,0),(2*D,0)]
    def func(q: Poly, i: int) -> F:
        if i<4: return integral(q,prior,*tests[i])
        if theta==0:
            return integral(q,prior,F(2),1) if desingularized else F(0)
        raw=integral(q,prior,D)-integral(q,prior,F(2))
        return raw/theta if desingularized else raw
    variations=[multiply(prod([f for j,f in enumerate(factors) if j!=i]),{a:F(1)})
                for i in range(3) for a in (F(0),F(1),D)]
    return mat([[(func(q,i)*ev-func(P,i)*integral(q,prior))/ev**2 for q in variations]
                for i in range(5)])

def formal_menu():
    # Formal pair (power of t, power of t^(2+theta)).
    cells=[{(0,0):F(1,3),(1,0):-F(1,12),(0,1):-F(1,12)},
           {(0,0):F(1,3),(1,0):F(1,12)},
           {(0,0):F(1,3),(0,1):F(1,12)}]
    probes=[]
    for c in cells:
        p={a:x/8 for a,x in c.items()};p[(0,0)]+=F(1,2);probes.append(p)
    keys=[(0,0),(1,0),(2,0),(0,1),(1,1),(0,2)]
    rows=[]
    for p,q in product(probes,repeat=2):
        pq=defaultdict(F)
        for (i,j),v in p.items():
            for (k,l),w in q.items():pq[(i+k,j+l)]+=v*w
        rows.append([pq[a] for a in keys])
    C=mat(rows)
    G=C.copy();G[:,2]=C[:,2]+C[:,3]
    G=G[:,[0,1,2,4,5,3]]
    return C,G

def report_factors(theta: F, g: tuple[F,...]) -> list[Poly]:
    D=2+theta
    cells=[{F(0):F(1,3),F(1):-F(1,12),D:-F(1,12)},
           {F(0):F(1,3),F(1):F(1,12)},
           {F(0):F(1,3),D:F(1,12)}]
    return [scale(cells[j],g[j]) for j in range(3)]+[add(*[scale(cells[j],1-g[j]) for j in range(3)])]

def run():
    priors=['uniform','density_3t2','quarter_uniform_three_quarters_delta1']
    # Source-independent exact positivity fixtures, including a triple collision.
    for m in (2,3,4):
        groups=defaultdict(set)
        for i in range(m+1):
            for j in range(m-i+1):groups[i+2*j].add(j)
        cols=[(F(lam),k) for lam,gs in sorted(groups.items()) for k in range(len(gs))]
        for prior in priors:
            K=len(cols)
            M=mat([[moment(F(i)+lam,prior,k) for lam,k in cols] for i in range(K)])
            det=M.det(method='domain-ge')
            check(f'confluent_pairing_m{m}_{prior}',det>0, dimension=K,
                  maximal_multiplicity=max(map(len,groups.values())), determinant=str(det))
    displayed=mat([[moment(F(i+j)) if k==0 else moment(F(i+j),'uniform',1)
                    for j,k in [(0,0),(1,0),(2,0),(2,1),(3,0),(4,0)]] for i in range(6)])
    check('displayed_limiting_minor',displayed.det()==sp.Rational(1,338751673344000000),
          determinant=str(displayed.det()))
    for theta in (F(0),F(1,257),F(1,3),F(1,2)):
        for prior in priors:
            J=normalized_jacobian(theta,prior,True)
            Jphysical=normalized_jacobian(theta,prior,False)
            ranks=[J.rank(),Jphysical.rank()]
            check(f'normalized_ranks_theta{theta}_{prior}',ranks==[5,4 if theta==0 else 5],ranks=ranks)
    C,G=formal_menu()
    check('nine_query_formal_and_physical_ranks',C.rank()==6 and G.rank()==6,
          ranks=[C.rank(),G.rank()])
    b=sum(G[j,5]**2 for j in range(9))/18
    check('weak_direction_ticket_coefficient',b==sp.Rational(169,7962624),coefficient=str(b))
    # Different commands and tiny nonzero parameter, exhaustive report words.
    commands=[(F(7,20),F(13,20),F(9,20)),(F(3,5),F(2,5),F(7,10)),
              (F(11,20),F(7,20),F(3,5)),(F(2,5),F(7,10),F(3,10))]
    total_updates=0
    for theta in (F(0),F(1,257),F(1,3),F(1,2)):
        D=2+theta
        fs=[report_factors(theta,g) for g in commands]
        for prior in priors:
            for word in product(range(4),repeat=4):
                P=prod([fs[i][word[i]] for i in range(3)]);Z=integral(P,prior)
                mean=lambda s: integral(P,prior,s)/Z
                w=[mean(F(1)),mean(F(2)),mean(D+1),mean(2*D),mean(D)-mean(F(2))]
                f=fs[3][word[3]];a=f.get(F(0),F(0));bb=f.get(F(1),F(0));c=f.get(D,F(0))
                den=a+bb*w[0]+c*(w[1]+w[4])
                asserted=[(a*w[0]+bb*w[1]+c*w[2])/den,
                          (a*(w[1]+w[4])+bb*w[2]+c*w[3])/den]
                Pf=multiply(P,f);Zf=integral(Pf,prior)
                exact=[integral(Pf,prior,s)/Zf for s in (F(1),D)]
                if asserted!=exact or den<F(1,24):raise AssertionError((theta,prior,word))
                total_updates+=1
            check(f'exhaustive_shrinking_update_theta{theta}_{prior}',True,
                  report_words=256, arithmetic='exact rational')
    # Entire seven-trial profile, not only the m=3 checkpoint.
    def sumsets(A,N):
        out=[{F(0)}]
        for _ in range(N):out.append({x+a for x in out[-1] for a in A})
        return out
    for theta in (F(0),F(1,257),F(1,3),F(1,2)):
        S=sumsets([F(0),F(1),2+theta],7)
        profile=[min(2*n,len(S[7-n])-1) for n in range(8)]
        expected=[0,2,4,6,6,4,2,0] if theta==0 else [0,2,4,6,8,5,2,0]
        check(f'seven_trial_profile_theta{theta}',profile==expected,profile=profile,
              future_dimension_at_n4=len(S[3])-1)
    check('past_limited_exponent_separation',F(1,4)-F(2,9)==F(1,36),difference='1/36')
    # Finite, floating-point allocation stress test. Count sweeps as families.
    sweeps=0
    for orders in ([0,0,0,0,1],[0]*6+[1]*3,[0]*8+[1]*5+[2],[0,0,1,2,3]):
        for theta in (0.,2.**-12,.07,.5):
            lengths=[theta**v if v else 1. for v in orders];lengths=[a for a in lengths if a>0]
            for budget in (1,2,3,7,31,257,4096,10**8):
                prod_a=1.;candidates=[]
                for i,a in enumerate(lengths,1):
                    prod_a*=a;candidates.append((prod_a/budget)**(1/i))
                e=max(candidates);counts=[max(1,int(math.floor(a/e))) for a in lengths]
                if math.prod(counts)>budget or max(a/n for a,n in zip(lengths,counts))>2*e*(1+1e-12):
                    raise AssertionError((orders,theta,budget,e,counts))
                sweeps+=1
            check(f'rectangle_orders{orders}_theta{theta}',True,budgets_checked=8,
                  arithmetic='floating-point; tolerance 1e-12 on width only')
    # Elementary threshold transfer, using abstract positive constants.
    ce,cs=sp.symbols('C_e c_s',positive=True)
    k=(cs/(2*ce))**2
    check('necessary_resolution_budget_constant',sp.simplify(ce-cs/sp.sqrt(k))==-ce,
          meaning='VM-VT <= -C_e theta^2 when M <= (c_s/(2 C_e))^2 theta^-4')
    # Exact unit-box residual and integrated wrong-threshold cost fixtures.
    z,v,r=sp.symbols('z v rho',real=True)
    residual=sp.integrate((z-v)**2,(z,-r,r))/(2*r)
    check('uniform_cube_last_coordinate_variance',sp.simplify(residual-v**2-r**2/3)==0)
    p,q,u=sp.symbols('p q u',real=True)
    wrong=sp.integrate(p-u,(u,q,p))
    check('ticket_gap_identity_for_ordered_thresholds',sp.simplify(wrong-(p-q)**2/2)==0)
    return dict(exact_shrinking_updates=total_updates,rectangle_cases=sweeps,
                no_author_code_imported=True,no_continuum_asymptotic_theorem_verified_by_tests=True,
                scope='Exact finite algebra and explicitly labelled numerical fixtures; analytic proof review is separate.')

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('INDEPENDENT_DIAGNOSTICS.json'))
    args=parser.parse_args();t=time.monotonic();error=None;summary={}
    try:summary=run()
    except Exception as exc:error=f'{type(exc).__name__}: {exc}'
    receipt=dict(submission_commit=SUBMISSION,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 python=sys.version,sympy=sp.__version__,platform=platform.platform(),
                 elapsed_seconds=round(time.monotonic()-t,3),passed=sum(x['passed'] for x in CHECKS),
                 total=len(CHECKS),error=error,summary=summary,checks=CHECKS)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ['passed','total','error','elapsed_seconds','summary']},indent=2))
    return 1 if error else 0

if __name__=='__main__':raise SystemExit(main())
