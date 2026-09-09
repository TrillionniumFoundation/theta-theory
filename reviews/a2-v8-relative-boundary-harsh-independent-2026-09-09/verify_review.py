#!/usr/bin/env python3
"""Independent finite checks for the A2-v8 referee report.
Run: python verify_review.py > VERIFICATION_RESULTS.json
Requires SymPy and mpmath. No network, source parser, billiard solver,
interval arithmetic, PDF build, or proof-assistant certification.
All checks use explicit exceptions and also execute under python -O.
"""
import json
from collections import Counter
import sympy as sp
import mpmath as mp

checks = []

def check(name, condition, category="exact_algebra"):
    if not bool(condition):
        raise RuntimeError("FAILED: " + name)
    checks.append({"name": name, "category": category, "passed": True})

def zero(x):
    if isinstance(x, sp.MatrixBase):
        return all(sp.simplify(v) == 0 for v in x)
    return sp.simplify(x) == 0

# Recompute derivatives, rather than input the displayed derivative matrix.
r, g, A = sp.symbols("r g A", positive=True)
f1 = r/sp.sqrt(g*(g+2*r))
fs = [f1, f1/(2*(1+g/r)), f1/(4*(1+g/r)**2-1)]
table = [[sp.Rational(1,4),sp.Rational(3,4),-sp.Rational(5,4),sp.Rational(21,4)],
         [sp.Rational(1,24),sp.Rational(17,72),sp.Rational(35,216),-sp.Rational(491,216)],
         [sp.Rational(1,140),sp.Rational(297,4900),sp.Rational(36243,171500),-sp.Rational(4458537,6002500)]]
actual = [[sp.simplify(sp.diff(f,r,k).subs({r:sp.Rational(1,4),g:sp.Rational(1,2)})/sp.sqrt(2)) for k in range(4)] for f in fs]
for j in range(3):
    for k in range(4):
        check(f"amplitude_derivative_j{j+1}_k{k}", zero(actual[j][k]-table[j][k]))
D = sp.Matrix([[sp.sqrt(2)/A*(v[1]+sp.pi*v[0]/(72*A)),
                sp.sqrt(2)/A*(-v[2]+5*sp.pi*v[0]/(144*A)),
                sp.sqrt(2)*v[3]/(2*A)] for v in actual])
det_expected = -2*sp.sqrt(2)*(15804720*A+64253*sp.pi)/(72930375*A**4)
check("physical_three_amplitude_determinant", zero(D.det()-det_expected))
C1,C2,C3 = sp.symbols("C1 C2 C3")
block = sp.zeros(4)
block[:,0] = sp.Matrix([C1,-2*C1,-4*C2,-6*C3])
block[1:4,1:4] = D
check("fixed_window_limiting_block", zero(block.det()-C1*det_expected))

# Support-family area, symmetric coordinates, and the genuine splitting pair.
al,be,ze,R = sp.symbols("alpha beta zeta R", real=True)
x = [36*(al+be),36*(al-be/2+sp.sqrt(3)*ze/2),36*(al-be/2-sp.sqrt(3)*ze/2)]
e1 = sum(x)
e2 = sum(x[i]*x[j] for i in range(3) for j in range(i+1,3))
e3 = sp.prod(x)
area_direct = sp.sqrt(3)/2-sp.pi*(R**2+2*R*al-sp.Rational(33,2)*al**2-sp.Rational(45,4)*(be**2+ze**2))
area_coeff = sp.sqrt(3)/2-sp.pi*R**2-sp.pi*R*e1/54+41*sp.pi*e1**2/7776-5*sp.pi*e2/432
check("physical_area_identity", zero(area_direct-area_coeff))
ss = sp.symbols("s", real=True)
check("splitting_e1", zero(e1.subs({al:0,be:ss,ze:0})))
check("splitting_e2", zero(e2.subs({al:0,be:ss,ze:0})+972*ss**2))
check("splitting_e3", zero(e3.subs({al:0,be:ss,ze:0})-11664*ss**3))
rot = {be:-be/2-sp.sqrt(3)*ze/2, ze:sp.sqrt(3)*be/2-ze/2}
xrot = [sp.expand(t.subs(rot, simultaneous=True)) for t in x]
check("rotation_cycles_contact_radii", zero(sp.Matrix(xrot)-sp.Matrix([x[2],x[0],x[1]])))
check("reflection_swaps_contact_radii", zero(sp.Matrix([t.subs(ze,-ze) for t in x])-sp.Matrix([x[0],x[2],x[1]])))

# Independently eliminate finite tridiagonal Hessians, with both parities
# and unequal facing curvatures. These are quadratic checks only.
for family,c0,c1 in [("equal",sp.Integer(3),sp.Integer(3)),
                     ("unequal",sp.Rational(9,4),sp.Integer(4))]:
    gap=sp.Rational(1,2); c=sp.sqrt(c0*c1)
    cs=[c0,c1]
    for j in range(1,9):
        n=j+1
        Q=sp.zeros(n)
        for i in range(n):
            Q[i,i]=(1 if i in (0,j) else 2)*cs[i%2]/gap
            if i<j:
                Q[i,i+1]=Q[i+1,i]=-1/gap
        sig=[sp.sqrt(cs[1-i%2]) for i in range(n)]
        endpoints=Q.extract([0,j],[0,j])
        if j>1:
            H=Q[1:j,1:j]
            G=H.inv()
            cross=Q.extract([0,j],list(range(1,j)))
            effective=endpoints-cross*G*cross.T
            green=sp.Matrix(j-1,j-1,lambda i,k:
                gap*sig[i+1]*sig[k+1]/c * sp.chebyshevu(min(i,k),c)
                *sp.chebyshevu(j-max(i,k)-2,c)/sp.chebyshevu(j-1,c))
            check(f"{family}_j{j}_green",zero(G-green))
            interior_det=H.det()
        else:
            effective=endpoints
            interior_det=sp.Integer(1)
        u=sp.chebyshevu(j-1,c); t=sp.chebyshevt(j,c)
        predicted=c/(gap*u)*sp.Matrix([[t/sig[0]**2,-1/(sig[0]*sig[j])],
                                      [-1/(sig[0]*sig[j]),t/sig[j]**2]])
        check(f"{family}_j{j}_schur_hessian",zero(effective-predicted))
        check(f"{family}_j{j}_cofactor",zero(-effective[0,1]-(1/gap)**j/interior_det))
        q2=c**2*(c**2-1)/(gap**2*sig[0]**2*sig[j]**2)
        check(f"{family}_j{j}_whitening_determinant",zero(effective.det()-q2))

# Richardson moments, cutoff regularity, and the proposed envelope balance.
y=sp.symbols("y", real=True)
for m in range(1,7):
    ws=[(-1)**(l-1)*sp.binomial(m,l) for l in range(1,m+1)]
    for k in range(m):
        check(f"richardson_m{m}_degree{k}",sum(ws[l-1]*l**k for l in range(1,m+1))==(1 if k==0 else 0))
    cutoff=(1-y)**(m+1)
    check(f"cutoff_m{m}_value_zero",cutoff.subs(y,0)==1)
    for k in range(m+1):
        check(f"cutoff_m{m}_splice_derivative{k}",sp.diff(cutoff,y,k).subs(y,1)==0)
    check(f"envelope_curvature_cost_m{m}",sp.Rational(3,m)*(2*m+2)==6+sp.Rational(6,m))
    check(f"envelope_gap_cost_m{m}",sp.Rational(1,m+1)*(2*m+2)==2)

# Independent ordinary high-precision quadrature of disk/ellipse overlap.
mp.mp.dps=60
for qs in ["0.01","0.08","0.2","0.5","0.85"]:
    q=mp.mpf(qs); lam=(1-q)/(1+q)
    th=mp.atan(mp.sqrt(lam))
    quarter=th+mp.quad(lambda t:1/(lam*mp.cos(t)**2+mp.sin(t)**2/lam),[th,mp.pi/2])
    delta=1-2*quarter/mp.pi
    expected=2*mp.asin(q)/mp.pi
    check(f"overlap_q{qs}",abs(delta-expected)<mp.mpf("1e-45"),"ordinary_high_precision")

# Likelihood checks use constructed nuisance-envelope probabilities,
# not numerical exact finite-offset billiard probabilities.
def lead(j,s):
    rr=[mp.mpf("0.25")+36*s,mp.mpf("0.25")-18*s,mp.mpf("0.25")-18*s]
    aa=mp.sqrt(3)/2-mp.pi/16+45*mp.pi*s*s/4
    return sum(1/mp.sinh(j*mp.acosh(1+mp.mpf("0.5")/r0)) for r0 in rr)/aa

def berkl(p,q):
    if p==q:
        return mp.mpf(0)
    if p==0:
        return -mp.log1p(-q)
    return p*mp.log(p/q)+(1-p)*(mp.log1p(-p)-mp.log1p(-q))

s=mp.mpf("0.0001")
for m in [1,2,3]:
    h=100*s**(mp.mpf(3)/m)
    for j in [1,2,3]:
        cp,cm=lead(j,s),lead(j,-s)
        avg=(cp+cm)/2; diff=(cp-cm)/2
        for ratio in [mp.mpf("0.2"),mp.mpf("0.6"),mp.mpf("1"),mp.mpf("2")]:
            d=ratio*h
            psi=max(mp.mpf(0),1-ratio)**(m+1)
            p=d*d*(avg+diff*psi); q=d*d*(avg-diff*psi)
            kl=berkl(p,q)
            upper=(p-q)**2/(q*(1-q))
            check(f"envelope_kl_m{m}_j{j}_d{ratio}",
                  0<p<mp.mpf("0.5") and 0<q<mp.mpf("0.5") and
                  kl>=-mp.mpf("1e-55") and kl<=upper+mp.mpf("1e-55"),
                  "ordinary_high_precision")
            if ratio>=1:
                check(f"envelope_equal_outside_m{m}_j{j}_d{ratio}",p==q,
                      "ordinary_high_precision")

for etas in ["0.001","0.01","0.1","0.249"]:
    eta=mp.mpf(etas)
    check(f"confidence_entropy_eta{etas}",(1-2*eta)*mp.log((1-eta)/eta)>=mp.log(1/eta)/4,
          "ordinary_high_precision")

out={"schema":"a2-v8-independent-finite-checks-v1","status":"pass",
     "reviewed_commit":"9345433799379d23993a038e213e62b6b0c16e34",
     "counts":dict(Counter(t["category"] for t in checks)),"total":len(checks),
     "environment":{"sympy":sp.__version__,"mpmath":mp.__version__,"mpmath_dps":mp.mp.dps},
     "not_claimed":["formal proof verification","interval enclosures","exact nonlinear probability solver",
                    "execution of author diagnostics","independent manuscript build or PDF inspection"],
     "checks":checks}
print(json.dumps(out,indent=2,sort_keys=True))
