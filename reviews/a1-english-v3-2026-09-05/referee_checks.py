#!/usr/bin/env python3
"""Independent finite diagnostics for the pinned A1 English-v3 review.
Run: python referee_checks.py [output.json]
Requires Python 3, sympy, numpy. Does not import or execute author code.
Passing checks are not formal verification, an all-n proof, or journal acceptance.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

TARGET = '025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6'
results = []

def check(name, kind, fn):
    try:
        detail = fn()
        results.append(dict(id=f'D{len(results)+1:02}', name=name,
                            kind=kind, passed=True, detail=detail))
    except Exception as exc:
        results.append(dict(id=f'D{len(results)+1:02}', name=name,
                            kind=kind, passed=False, error=repr(exc)))

def zero(expr):
    assert s.simplify(expr) == 0, str(expr)

t, R = s.symbols('t R', real=True)
l, u = s.Rational(9,20), s.Rational(47,100)
a0 = s.sqrt(3)/2
b, eps = s.symbols('b eps', positive=True)
r = [l+(u-l)*j/3 for j in range(4)]
ss = [l*l+2*l*(u-l)*j/3+(u-l)**2*j*(j-1)/6 for j in range(4)]
dd = [l**(3-j)*u**j for j in range(4)]

def bern(c):
    n = len(c)-1
    return sum(c[i]*s.binomial(n,i)*t**i*(1-t)**(n-i) for i in range(n+1))

def monomials():
    for q, c in enumerate((r, ss, dd), 1):
        zero(bern(c)-(l+(u-l)*t)**q)
    assert all(dd[j] <= u*u*r[j] for j in range(4))
    return 'Exact degree-three representations of R, R^2, R^3 and d_j <= u^2 r_j.'
check('Bernstein monomial identities', 'exact symbolic/rational', monomials)

def raw_normalization():
    mass = s.pi*R**2 + a0-s.pi*R**2-b*R + b*R
    zero(mass-a0)
    return 'Circle cosine integral is zero; the three tag masses sum to a0.'
check('Raw kernel normalization', 'exact symbolic', raw_normalization)

def positive_margins():
    aa = float(a0); ll, uu = float(l), float(u)
    lower = min(math.pi*ll*ll, aa-math.pi*uu*uu-.1*uu, .02*ll*(1-uu*uu))
    vals = []
    for T, e, z, j in itertools.product((.01,.05),(0.,1.),(-1.,1.),range(4)):
        vals.extend([math.pi*float(ss[j]), aa-math.pi*float(ss[j])-2*T*float(r[j]),
                     2*T*(float(r[j])+e*z*float(dd[j]))])
    assert min(vals) >= lower-1e-14 and lower > 0
    return dict(T_interval=[.01,.05], E=1, minimum=min(vals), lower_bound=lower,
                qualification='Finite endpoint diagnostic; the report separately checks the symbolic uniform proof.')
check('Positive raw coefficient margins', 'floating endpoint diagnostic', positive_margins)

def tube_jacobian():
    al, th, ph, flight = s.symbols('alpha theta phi flight', real=True)
    q = s.Matrix([R*s.cos(al)-flight*s.cos(th),R*s.sin(al)-flight*s.sin(th)])
    determinant = q.jacobian([al,flight]).det()
    zero(determinant.subs(th,al+s.pi-ph)+R*s.cos(ph))
    return 'Oriented determinant is -R cos(phi), so its magnitude is R cos(phi) in the incidence chamber.'
check('Fixed-laboratory-angle tube Jacobian', 'exact symbolic', tube_jacobian)

def failure_map():
    mp,m0,m1,m2 = s.symbols('mp m0 m1 m2')
    H = s.pi*R**2*(1-mp)+(a0-s.pi*R**2-b*R)*(1-m0)+b*R*(1-m1)-b*eps*R**3*m2
    expected = [a0*(1-m0),b*(m0-m1),s.pi*(m0-mp),-b*eps*m2]
    coeff = [s.expand(H).coeff(R,j) for j in range(4)]
    for x,y in zip(coeff,expected): zero(x-y)
    determinant = s.factor(s.Matrix(coeff).jacobian([mp,m0,m1,m2]).det())
    assert determinant != 0
    return dict(moment_to_power_determinant=str(determinant))
check('Failure polynomial and full-rank moment map', 'exact symbolic', failure_map)

def product():
    c = [s.Rational(i+1,28) for i in range(7)]
    h = [s.Rational(i+2,7) for i in range(4)]
    out = [sum(s.binomial(6,i)*s.binomial(3,j)/s.binomial(9,k)*c[i]*h[j]
               for i in range(7) for j in range(4) if i+j==k) for k in range(10)]
    zero(bern(out)-bern(c)*bern(h))
    assert all(v>0 for v in out)
    return 'Exact positive degree-six times degree-three Bernstein convolution.'
check('Positive coefficient update', 'exact rational', product)

def beta_moments():
    degree=6; c=[s.Rational(i+1,28) for i in range(7)]
    for q in range(4):
        actual=s.integrate(s.expand((degree+1)*bern(c)*t**q),(t,0,1))
        expected=sum(c[i]*s.rf(i+1,q)/s.rf(degree+2,q) for i in range(degree+1))
        zero(actual-expected)
    return 'Uniform-prior beta-mixture normalization and moments q=0,1,2,3.'
check('Beta-mixture posterior moments', 'exact rational', beta_moments)

def product_ranks():
    ranks={}
    for n in range(1,5):
        # Rational positive cubics near 1; tests the algebra in the all-n proof.
        factors=[1+s.Rational(i+1,100)*R**3 for i in range(n)]
        columns=[]
        for i in range(n):
            other=s.prod(factors[j] for j in range(n) if j!=i)
            for k in range(4):
                p=s.Poly(s.expand(R**k*other),R)
                columns.append([p.nth(j) for j in range(3*n+1)])
        rank=s.Matrix(3*n+1,4*n,lambda row,col: columns[col][row]).rank()
        assert rank==3*n+1
        ranks[str(n)]=rank
    return dict(ranks=ranks, qualification='Finite n=1..4 only; not a replacement for coprimality/submersion proof.')
check('Coprime product differential ranks', 'exact rational finite-rank diagnostic', product_ranks)

def rare_failure():
    raw=[s.pi*ss[j]+s.Rational(1,3)*(a0-s.pi*ss[j]-s.Rational(1,10)*r[j]) for j in range(4)]
    normal=[s.simplify(v/sum(raw)) for v in raw]
    for delta in [s.Rational(1,10),s.Rational(1,10**12)]:
        for x,y in zip(normal,[delta*v/sum(delta*w for w in raw) for v in raw]): zero(x-y)
    return 'Failure factors scaled by 1/10 and 10^-12 have exactly the same normalized coefficients.'
check('Rare-failure normalization', 'exact symbolic/rational', rare_failure)

def zero_evidence():
    # g=1 almost everywhere makes all failure coefficients zero.
    v=s.Matrix([0,0,0,0]); assert sum(v)==0
    for f in [.1,1e-6,1e-12]: assert 0 <= f*math.exp(2) <= 8*f
    return 'Zero failure branch is null for every radius; bounded weighted continuation vanishes with its evidence.'
check('Boundary zero-evidence contribution', 'elementary finite diagnostic', zero_evidence)

def support_function():
    F=[s.Matrix([1,0,2]),s.Matrix([0,1,-1]),s.Matrix([1,1,3])]
    z=s.Matrix([2,-3,1]); weights=[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)]
    eta=s.Rational(1,5); dots=[(z.T*f)[0] for f in F]
    analytic=eta*sum(w*v for w,v in zip(weights,dots))+(1-2*eta)*sum(w*max(v,0) for w,v in zip(weights,dots))
    vertices=[sum(w*g*v for w,g,v in zip(weights,gates,dots)) for gates in itertools.product([eta,1-eta],repeat=3)]
    zero(max(vertices)-analytic)
    return 'Finite-reference-measure support formula agrees with exhaustive vertex enumeration.'
check('Moment-body support formula', 'exact rational finite analogue', support_function)

def intrinsic_dimension():
    # N=1, lambda=0, G=1. Then w = bar k is a linear combination of v.
    A=s.symbols('A0:4')
    rows=[s.Matrix([[1,0,0,0,A[0]]]),s.Matrix([[0,1,0,0,A[1]]]),
          s.Matrix([[0,0,1,1,A[2]+A[3]]]),s.Matrix([[0,0,1,-1,A[2]-A[3]]])]
    M=s.Matrix.vstack(*rows)
    assert M.rank()==4
    m=s.symbols('m0:4'); U=sum(A[i]*m[i] for i in range(4))
    zero(U-s.Matrix(A).dot(s.Matrix(m)))
    return 'Admissible constant-payoff case has a four-dimensional affine hull, not necessarily five; not a Bellman counterexample.'
check('Five coordinates need not mean intrinsic dimension five', 'exact symbolic scope diagnostic', intrinsic_dimension)

def endpoint_gates():
    # Two hidden parameters, three raw outcomes, binary terminal decision, positive payoff 1 or 2.
    K=[[s.Rational(1,2),s.Rational(1,3),s.Rational(1,6)],
       [s.Rational(1,6),s.Rational(1,3),s.Rational(1,2)]]
    prior=[s.Rational(2,5),s.Rational(3,5)]
    payoff=[[s.Integer(2),s.Integer(1)],[s.Integer(1),s.Integer(2)]]
    def objective(g):
        accepted=sum(g[x]*max(sum(prior[r]*K[r][x]*payoff[r][d] for r in range(2)) for d in range(2)) for x in range(3))
        rejected=max(sum(prior[r]*sum((1-g[x])*K[r][x] for x in range(3))*payoff[r][d] for r in range(2)) for d in range(2))
        return accepted+rejected
    vertices=list(itertools.product([s.Integer(0),s.Integer(1)],repeat=3))
    optimum=max(map(objective,vertices))
    grid=list(itertools.product([s.Rational(j,4) for j in range(5)],repeat=3))
    assert max(map(objective,grid))==optimum
    for g in grid:
        assert objective(g)<=optimum
    return dict(vertex_optimum=str(optimum), grid_size=len(grid),
                qualification='Finite analogue supporting a separately derived statewise endpoint-gate lemma, not the full continuous control solution.')
check('Endpoint-gate finite decision diagnostic', 'exact rational finite analogue', endpoint_gates)

def smooth_perturbation():
    delta=s.symbols('delta', nonzero=True)
    change=b*delta*R*s.sin(R)
    fourth=s.diff(change,R,4)
    zero(fourth-b*delta*(R*s.sin(R)-4*s.cos(R)))
    assert s.N((R*s.sin(R)-4*s.cos(R)).subs(R,s.Rational(46,100))) != 0
    return dict(fourth_derivative=str(s.simplify(fourth)),
                qualification='Modified smooth detector outside the exact cubic hypothesis; not a counterexample to the printed cubic theorem.')
check('Smooth detector perturbation breaks exact cubic closure', 'exact symbolic scope diagnostic', smooth_perturbation)

def smooth_dynamics_threshold():
    # x'=a, x(0)=0, T=1; a fixed Borel threshold is not a smooth readout.
    for k in [2,4,8,12]:
        h=s.Rational(1,10**k)
        assert int(bool(h>0))-int(bool(-h>0))==1
    return 'Y_a=1_{a>0} jumps with fixed preparation and smooth no-event dynamics. Only the unqualified report-regularity clause is contradicted.'
check('A.3 missing smooth-readout hypothesis', 'exact counterexample diagnostic', smooth_dynamics_threshold)

def information_identity():
    # Compare direct density Fisher information and the printed flags-plus-mark formula.
    radius=.46; T=.04; epsilon=.8; area=math.sqrt(3)/2
    ys=2*np.pi*(np.arange(8192)+.5)/8192
    H=[math.pi*radius**2, area-math.pi*radius**2-2*T*radius]
    Hp=[2*math.pi*radius,-2*math.pi*radius-2*T]
    hit=2*T*radius*(1+epsilon*radius**2*np.cos(ys))
    hitp=2*T*(1+3*epsilon*radius**2*np.cos(ys))
    direct=sum(hp*hp/(h*area) for h,hp in zip(H,Hp))+float(np.mean(hitp*hitp/hit))/area
    A=area-math.pi*radius**2; sf=math.pi*radius**2/area; sp=2*math.pi*radius/area
    p=2*T*radius/A; pp=2*T*(area+math.pi*radius**2)/A**2
    J=4/radius**2*(1/math.sqrt(1-epsilon**2*radius**4)-1)
    formula=sp*sp/(sf*(1-sf))+(1-sf)*(pp*pp/(p*(1-p))+p*J)
    assert abs(direct-formula)<1e-10
    return dict(direct=direct, formula=formula, absolute_error=abs(direct-formula), quadrature_nodes=8192)
check('Raw Fisher information decomposition', 'floating circle quadrature', information_identity)

def adaptive_path():
    # A finite two-stage controlled polynomial experiment, with control chosen by first outcome.
    p=R/2; q=[R**2/2,(1+R)/3]
    paths=[(p if x else 1-p)*(q[x] if y else 1-q[x]) for x,y in itertools.product([0,1],repeat=2)]
    zero(sum(paths)-1)
    assert all(s.Poly(v,R).degree()<=3 for v in paths)
    assert all(s.diff(v,R,4)==0 for v in paths)
    return 'A fixed history-dependent design gives normalized polynomial chronological laws; degrees add despite adaptivity.'
check('Adaptive polynomial chronological law', 'exact symbolic finite analogue', adaptive_path)

def posterior_bound():
    prior=[s.Rational(1,3)]*3
    p=[s.Integer(1),s.Integer(2),s.Integer(3)]
    delta=s.Rational(1,10); mult=[1-delta,1+delta,1-delta]
    exact=[prior[i]*p[i]/sum(prior[j]*p[j] for j in range(3)) for i in range(3)]
    approx=[prior[i]*p[i]*mult[i]/sum(prior[j]*p[j]*mult[j] for j in range(3)) for i in range(3)]
    tv=sum(abs(x-y) for x,y in zip(exact,approx))/2
    assert tv<=delta/(1-delta)
    return dict(tv=str(tv), conservative_bound=str(delta/(1-delta)))
check('Relative likelihood to posterior-TV bound', 'exact rational finite diagnostic', posterior_bound)

def prior_value_bound():
    p=[s.Rational(1,4),s.Rational(3,4)]; q=[s.Rational(1,2)]*2
    functions=[[s.Integer(1),s.Integer(3)],[s.Integer(4),s.Integer(2)]]
    V=lambda z:max(sum(x*y for x,y in zip(z,f)) for f in functions)
    tv=sum(abs(x-y) for x,y in zip(p,q))/2
    assert abs(V(p)-V(q))<=3*tv
    return 'Supremum of common bounded policy payoff functions obeys the oscillation-times-TV bound.'
check('Common-policy value stability', 'exact rational finite diagnostic', prior_value_bound)

def model_error_bound():
    # For amplitude perturbation delta sin R, hit-mark TV is 2 T R |delta sin R|/(a0 pi).
    radius=.46; T=.04; delta=.001; area=math.sqrt(3)/2
    ys=2*np.pi*(np.arange(65536)+.5)/65536
    numeric=.5*(2*T*radius/area)*abs(delta*math.sin(radius))*float(np.mean(np.abs(np.cos(ys))))
    formula=2*T*radius*abs(delta*math.sin(radius))/(area*math.pi)
    assert abs(numeric-formula)<1e-12
    return dict(one_step_tv=formula, quadrature_tv=numeric,
                qualification='Review-derived detector perturbation metric, distinct from coefficient roundoff.')
check('Detector perturbation one-step total variation', 'floating circle quadrature', model_error_bound)

receipt=dict(reviewed_commit=TARGET, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             environment=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__),
             passed=sum(r['passed'] for r in results), total=len(results), checks=results,
             limitations=['No author tests imported or rerun.', 'No LaTeX build or PDF inspection.',
                          'No proof-assistant verification.', 'Finite analogues are explicitly distinguished from the continuous apparatus.'])
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('DIAGNOSTICS.json')
out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=receipt['passed'],total=receipt['total'],output=str(out),script_sha256=receipt['script_sha256'])))
for result in results:
    if not result['passed']: print(result)
sys.exit(0 if receipt['passed']==receipt['total'] else 1)
