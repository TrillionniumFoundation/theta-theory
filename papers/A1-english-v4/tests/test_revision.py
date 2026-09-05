#!/usr/bin/env python3
"""Finite regression diagnostics, not a proof assistant or an all-budget audit."""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import traceback

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
RESULTS: list[dict] = []

def check(identifier: str, name: str, kind: str, function) -> None:
    try:
        detail = function()
        RESULTS.append(dict(id=identifier, name=name, kind=kind, passed=True, detail=detail))
    except Exception:
        RESULTS.append(dict(id=identifier, name=name, kind=kind, passed=False,
                            detail=traceback.format_exc()))

R, t = sp.symbols('R t', real=True)
l, u = sp.Rational(9,20), sp.Rational(47,100)
a0 = sp.sqrt(3)/2

def bern(i, n):
    return sp.binomial(n,i)*t**i*(1-t)**(n-i)

def polynomial_identities():
    for power in (1,2,3):
        c = []
        for j in range(4):
            if power == 1: v = l+(u-l)*j/3
            elif power == 2: v = l*l+2*l*(u-l)*j/3+(u-l)**2*j*(j-1)/6
            else: v = l**(3-j)*u**j
            c.append(v)
        assert sp.expand(sum(c[j]*bern(j,3) for j in range(4))-(l+(u-l)*t)**power) == 0
    for d in (0,1,3,6):
        for i in range(d+1):
            for j in range(4):
                assert sp.expand(bern(i,d)*bern(j,3)-sp.binomial(d,i)*sp.binomial(3,j)/sp.binomial(d+3,i+j)*bern(i+j,d+3)) == 0
    return 'Exact degree-three monomial representations and product identities at degrees 0,1,3,6.'

def raw_and_failure():
    b,e,c = sp.symbols('b e c')
    raw = [sp.pi*R**2, a0-sp.pi*R**2-b*R, b*R]
    assert sp.expand(sum(raw)-a0)==0
    ap,az,ah,ac = sp.symbols('ap az ah ac')
    F = raw[0]*(sp.Rational(1,2)-ap)+raw[1]*(sp.Rational(1,2)-az)+raw[2]*(sp.Rational(1,2)-ah)-b*e*R**3*ac/2
    expected = a0/2-a0*az+b*(az-ah)*R+sp.pi*(az-ap)*R**2-b*e*ac*R**3/2
    assert sp.expand(F-expected)==0
    d0,d1,d2,d3=sp.symbols('d0:4')
    inv={az:-d0/a0,ah:-d0/a0-d1/b,ap:-d0/a0-d2/sp.pi,ac:-2*d3/(b*e)}
    assert sp.simplify(F.subs(inv)-(a0/2+d0+d1*R+d2*R**2+d3*R**3))==0
    return 'Raw masses sum to a0; four failure coefficients and their exact gate inverse agree.'

def coefficient_margins():
    for j in range(4):
        r=l+(u-l)*j/3
        s=l*l+2*l*(u-l)*j/3+(u-l)**2*j*(j-1)/6
        d=l**(3-j)*u**j
        assert d<=u*u*r
        assert float(a0-sp.pi*s-sp.Rational(3,25)*r)>0
    return 'Exact d_j <= u^2 r_j; numerical positive no-hit margin at limiting T=0.06.'

def product_rank():
    records=[]
    for powers in ((0,1,2,3),(0,1,3),(0,1,2)):
        q=max(powers); r=len(powers)
        for n in range(1,5):
            factors=[1+sp.Rational(i+1,100)*R**q for i in range(n)]
            columns=[]
            for i in range(n):
                other=sp.prod(factors[j] for j in range(n) if i!=j)
                for p in powers:
                    columns.append([sp.expand(R**p*other).coeff(R,k) for k in range(q*n+1)])
            rank=sp.Matrix.hstack(*map(sp.Matrix,columns)).rank()
            assert rank==n*(r-1)+1
            records.append((powers,n,rank))
    return {'finite_unnormalized_ranks':records,'not_proved_by_test':'The all-n dimension theorem uses the manuscript proof.'}

def passive_rank():
    s=sp.symbols('s')
    for n in range(1,6):
        factors=[1+sp.Rational(i+1,10)*s for i in range(n)]
        columns=[[sp.expand(s*sp.prod(factors[j] for j in range(n) if j!=i)).coeff(s,k) for k in range(n+1)] for i in range(n)]
        assert sp.Matrix.hstack(*map(sp.Matrix,columns)).rank()==n
    return 'All-hit variable-R^2 product differential has rank n for n=1,...,5.'

def gram_ball():
    psi=sp.Matrix([[1,0,1],[0,1,1],[1,1,0],[1,-1,1]])
    G=psi.T*psi/4
    assert G.det()>0
    d=sp.Matrix([sp.Rational(1,100),sp.Rational(-1,200),sp.Rational(1,300)])
    values=psi*G.inv()*d
    assert psi.T*values/4==d
    assert max(abs(v) for v in values)<sp.Rational(1,2)
    return 'Finite reference-space Gram right inverse exactly realizes its prescribed coefficient displacement.'

def posterior_identities():
    d=6
    c=[sp.Rational(i+1,28) for i in range(7)]
    P=sum(c[i]*bern(i,d) for i in range(d+1))
    assert sp.integrate(P,(t,0,1))==sp.Rational(1,d+1)
    for k in (1,2,3):
        exact=sp.integrate((d+1)*P*t**k,(t,0,1))
        mixture=sum(c[i]*sp.prod(sp.Rational(i+1+j,d+2+j) for j in range(k)) for i in range(d+1))
        assert exact==mixture
    return 'Exact normalization and first three moments of the beta-mixture posterior.'

def rare_failure():
    raw=np.array([[1.,2.,3.,4.],[2.,1.,4.,3.],[3.,4.,1.,2.]])
    normalized=[]
    for eps in (1.,1e-4,1e-12):
        coeff=(eps*np.array([0.2,0.4,0.1]))@raw
        normalized.append(coeff/coeff.sum())
    assert np.max(np.abs(np.array(normalized)-normalized[0]))<1e-14
    return 'Normalized failure coefficients stay unchanged while failure mass tends to zero.'

def body_dimension():
    Mp,M1,M2,M3,b,e=sp.symbols('Mp M1 M2 M3 b e')
    v=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,1],[0,0,1,-1]])
    A=sp.Matrix([sp.pi*M2,a0-sp.pi*M2-b*M1,b*M1,b*e*M3])/a0
    assert v.row_join(v*A).rank()==4
    return 'Constant-reward fifth column is a linear combination of the four likelihood columns.'

def endpoint_layercake():
    g=np.array([.15,.4,.8]); U=np.array([[.5,.2,.3],[.1,.6,.3]])
    def objective(h): return float(.93*np.dot(h,U.max(axis=0))+((1-h)@U.T).max())
    cuts=sorted(set([0.,1.,*g.tolist()])); integral=0.
    for a,b in zip(cuts,cuts[1:]): integral+=(b-a)*objective((g>(a+b)/2).astype(float))
    assert objective(g)<=integral+1e-14
    vertices=[objective(np.array(v)) for v in itertools.product((0.,1.),repeat=3)]
    assert integral<=max(vertices)+1e-14
    return 'Finite three-report convex command objective satisfies layer-cake and endpoint bounds.'

def J(A,B):
    if A>=abs(B): return A
    if A<=-abs(B): return 0.
    return (A*math.acos(-A/abs(B))+math.sqrt(B*B-A*A))/math.pi

def arc_quadrature():
    y=(np.arange(120000)+.5)*2*math.pi/120000
    for A,B in [(2.,.2),(-2.,.2),(.1,.4),(-.1,-.4),(0.,.8)]:
        assert abs(J(A,B)-np.maximum(0,A+B*np.cos(y)).mean())<1e-9
    return 'Midpoint quadrature agrees with the closed arc integral in five regimes to 1e-9.'

def mode_boundaries():
    # Positive two-point payoff model, several priors and acceptance charges.
    radii=np.array([.45,.47]); G=np.array([[1.5,.5],[.5,1.5]])
    for p in (.2,.5,.8):
        moments=np.array([[np.sum(np.array([p,1-p])*Gj*radii**k) for k in range(4)] for Gj in G])
        for alpha in (.9,.999):
            def value(T,e):
                S=math.pi*moments[:,2]/float(a0); A=2*T*moments[:,1]/float(a0)
                N=moments[:,0]-S-A; B=2*T*e*moments[:,3]/float(a0)
                return max(moments[j,0]+max(0,alpha*S[1-j]-S[j])+max(0,alpha*N[1-j]-N[j])+J(alpha*A[1-j]-A[j],alpha*B[1-j]-B[j]) for j in (0,1))
            endpoints=max(value(.01,1.3),value(.055,1.3))
            assert all(value(T,e)<=endpoints+1e-12 for T in np.linspace(.01,.055,13) for e in np.linspace(0,1.3,11))
    return 'Six payoff/prior cases: 13x11 interior mode grids never exceed the proved four-candidate boundary optimum.'

def bernstein_hierarchy():
    y=(np.arange(4000)+.5)*2*math.pi/4000
    for m in (2,5,20):
        rows=1+(.12+.08*np.sin(np.arange(m+1)/m))[:,None]*np.cos(y)
        assert abs(rows.mean(axis=1)-1).max()<1e-14 and rows.min()>.79
        for theta in (.17,.52,.83):
            weights=np.array([math.comb(m,j)*theta**j*(1-theta)**(m-j) for j in range(m+1)])
            qm=weights@rows; exact=1+(.12+.08*math.sin(theta))*np.cos(y)
            error=.5*np.abs(qm-exact).mean()
            assert error<=(.08/math.pi)/(2*math.sqrt(m))+1e-8
    return 'Normalized positive nonpolynomial mark surrogates obey the stated TV Lipschitz bound on sampled t values.'

def adaptive_model_tv():
    # Complete enumeration with a history-dependent Bernoulli mode, not i.i.d. substitution.
    def path_law(n,shift):
        law={():1.}
        for _ in range(n):
            nxt={}
            for h,w in law.items():
                p=.2+.5*(sum(h)%2)+shift
                for z in (0,1): nxt[h+(z,)]=w*(p if z else 1-p)
            law=nxt
        return law
    eps=.03
    out=[]
    for n in range(1,7):
        P,Q=path_law(n,0),path_law(n,eps)
        tv=.5*sum(abs(P[h]-Q[h]) for h in P)
        assert tv<=1-(1-eps)**n+1e-14
        out.append((n,tv))
    return {'enumerated_adaptive_path_TV':out}

def response_and_shapes():
    assert sp.simplify(sp.diff(R*sp.sin(R),R,4)-(R*sp.sin(R)-4*sp.cos(R)))==0
    a=sp.symbols('a',positive=True)
    x=sp.symbols('x')
    f=sp.integrate(x**2,(x,0,a))+2*sp.integrate(x**2,(x,a,1))
    assert sp.diff(f,a)==-a**2
    assert (int(-.1>0),int(0>0),int(.1>0))==(0,0,1)
    return 'Exact sine fourth derivative and two-density interface sign; threshold readout exhibits its discontinuity.'

def rational_certificate():
    run=subprocess.run([sys.executable,str(ROOT/'tests/rational_gate_certificate.py')],capture_output=True,text=True,check=True)
    receipt=json.loads((ROOT/'validation/rational_gate_certificate.json').read_text())
    return {'stdout':run.stdout.strip(),'certificate':receipt}

def source_integrity():
    import re
    for source in [ROOT/'main.tex', ROOT/'references.tex', *sorted((ROOT/'sections').glob('*.tex'))]:
        assert all(b >= 32 or b in (9, 10) for b in source.read_bytes()), source
    main=(ROOT/'main.tex').read_text()
    for part in re.findall(r'\\input\{([^}]+)\}',main):
        assert (ROOT/(part+'.tex')).is_file(),part
    text='\n'.join(p.read_text() for p in [ROOT/'main.tex',*sorted((ROOT/'sections').glob('*.tex')),ROOT/'references.tex'])
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    assert len(labels)==len(set(labels))
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
    assert set(refs)<=set(labels)
    assert 'terminal \\emph{states}' in text
    assert 'fixed spatial position' in text
    return {'labels':len(labels),'input_files':'all present','reference_targets':'all resolved by source labels'}

CASES=[
('V01','Bernstein algebra','exact symbolic',polynomial_identities),
('V02','Kernel and inverse gate coefficients','exact symbolic',raw_and_failure),
('V03','Positive coefficient margins','exact inequalities / numeric margin',coefficient_margins),
('V04','Full and deficient product ranks','exact finite symbolic ranks',product_rank),
('V05','Passive product rank','exact finite symbolic ranks',passive_rank),
('V06','Gram realization','exact rational finite analogue',gram_ball),
('V07','Beta mixture','exact symbolic',posterior_identities),
('V08','Rare failure normalization','floating finite diagnostic',rare_failure),
('V09','Moment body intrinsic dimension','exact symbolic finite analogue',body_dimension),
('V10','Endpoint layer cake','floating finite analogue',endpoint_layercake),
('V11','Circular arc formula','numerical quadrature',arc_quadrature),
('V12','Four-candidate mode solution','numerical grid regression',mode_boundaries),
('V13','Positive approximation hierarchy','numerical finite regression',bernstein_hierarchy),
('V14','Adaptive model TV bound','complete finite path enumeration',adaptive_model_tv),
('V15','Response and scope regressions','symbolic / explicit counterexample',response_and_shapes),
('V16','Strict costly-gate advantage','exact rational interval certificate',rational_certificate),
('V17','Manuscript source integrity','source graph check',source_integrity)]
if __name__=='__main__':
    for case in CASES: check(*case)
    output=dict(review_base='574f2315a136d8b401644d8a3eeeb93c87887010',
                environment=dict(python=platform.python_version(),numpy=np.__version__,sympy=sp.__version__),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                passed=sum(r['passed'] for r in RESULTS),total=len(RESULTS),checks=RESULTS,
                scope='Finite diagnostics only. The referee v3 20-check script and the v3 author suite were not rerun.')
    (ROOT/'validation').mkdir(exist_ok=True)
    (ROOT/'validation/DIAGNOSTICS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(f"{output['passed']}/{output['total']} diagnostics passed")
    for r in RESULTS:
        if not r['passed']: print(r['id'],r['detail'])
    sys.exit(0 if output['passed']==output['total'] else 1)
