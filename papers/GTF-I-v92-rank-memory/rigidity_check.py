#!/usr/bin/env python3
"""Exact finite regression for contact defects and stable centered-swap bounds.

The continuum statements are proved in the manuscript, not by this suite.
No floating-point threshold, sampling certificate, or optimization-mode assert
is used. The noncommuting fixtures exercise the fidelity-defect algebra.
"""
import json
import sympy as s

checks = 0
negative = 0

def require(ok, message):
    if not bool(ok):
        raise RuntimeError(message)

def equal(a, b, message):
    global checks
    if isinstance(a, s.MatrixBase):
        require((a-b).applyfunc(s.simplify) == s.zeros(*a.shape), message)
    else:
        require(s.simplify(a-b) == 0, message)
    checks += 1

def ge(a, b, message):
    global checks
    require(s.simplify(a-b).is_nonnegative is True, message)
    checks += 1

# Diagonal states: exact centered-swap eigenvalues, including singular factors.
for d in range(2, 9):
    flat = [s.Rational(1,d)]*d
    tilted = [s.Rational(i+1,d*(d+1)//2) for i in range(d)]
    pure = [s.Integer(1)]+[s.Integer(0)]*(d-1)
    c = d-1-s.Rational(1,d)
    K = d*(1+s.Rational(9,2)/c)
    for a,b in ((flat,flat),(tilted,tilted),(pure,pure),(pure,flat),
                (pure,[s.Integer(0),s.Integer(1)]+[s.Integer(0)]*(d-2))):
        tr_ab=sum(x*y for x,y in zip(a,b))
        fidelity=sum(s.sqrt(x*y) for x,y in zip(a,b))
        eta=1-fidelity**2
        e=s.simplify(tr_ab-fidelity**2/d)
        norm=(d-1)*tr_ab
        for i in range(d):
            for j in range(i+1,d):
                u,v=a[i]*b[j],a[j]*b[i]
                norm+=s.sqrt((u-v)**2+4*d*d*u*v)
        delta=s.simplify(d-s.Rational(1,d)-norm)
        ge(delta,c*eta+e,'centered-swap lower defect')
        for x in (a,b):
            distance=sum(abs(v-s.Rational(1,d)) for v in x)
            ge(K*(c*eta+e),distance**2,'stable equality via elementary defects')
            ge(K*delta,distance**2,'stable centered-swap bound')
        if a==flat and b==flat:
            equal(delta,0,'scalar exact equality')
        else:
            require(delta>0,'non-scalar nonzero factors have strict defect')
            negative+=1

# Noncommuting complex states: f^2=tr(ab)+2 sqrt(det(a)det(b)) in dimension two.
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]])
for x,y in ((s.Rational(1,2),s.Rational(1,2)),(s.Rational(3,5),s.Rational(4,5)),
            (s.Rational(1),s.Rational(1,2))):
    a,b=(I+x*X)/2,(I+y*Y)/2
    require(a*b!=b*a,'fixture is noncommuting')
    f2=s.simplify(s.trace(a*b)+2*s.sqrt(a.det()*b.det()))
    eta=1-f2;e=s.trace(a*b)-f2/2
    ge(eta,0,'fidelity defect is nonnegative')
    ge(e,0,'spectral defect is nonnegative')
    for distance in (x,y):
        ge(20*(eta/2+e),distance**2,'complex noncommuting rigidity')
    negative+=1

# A genuine finite experiment with identical devices under both hypotheses.
# Its leaf optimum is analytically g_y(a)=(3/5) tr(a E_y^T).
E=((I+Y/2)/2,(I-Y/2)/2)
rho=s.diag(s.Rational(1,3),s.Rational(2,3))
parts=((rho/2+X/12,rho/2-X/12),(rho/2+Y/12,rho/2-Y/12))
p=s.Rational(3,5)
H=(p*E[0].T+s.diag(s.Rational(1,8),0),
   p*E[1].T+s.diag(0,s.Rational(1,16)))
S=H[0]+H[1];U=p+s.Rational(1,8)
v=s.Integer(0);contact=s.Integer(0);leaf=s.Integer(0)
for y in range(2):
    equal(sum(parts[y],s.zeros(2)),rho,'common barycenter')
    for h,A in enumerate(parts[y]):
        ge(A.det(),0,'positive branch atom')
        w=s.trace(A);atom=A/w
        g=p*s.trace(atom*E[y].T)
        achieved=(p if h==0 else 1-p)*s.trace(A*E[y].T)
        defect=w*(s.trace(H[y]*atom)-g)
        loss=w*g-achieved
        ge(defect,0,'analytical majorant branch defect')
        ge(loss,0,'chosen final-readout loss')
        contact+=defect;leaf+=loss;v+=achieved
spectral=s.trace(rho*(U*I-S))
equal(U-v,spectral+contact+leaf,'exact primal-dual deficit decomposition')
equal(spectral,rho[1,1]/16,'spectral mass bound at gap 1/16')
require(leaf>0,'suboptimal readout negative control')
negative+=1

# Exact normalization of the near-optimal bound and the relative t^2 scale.
for d in range(2, 10):
    c=d-1-s.Rational(1,d);K=d*(1+s.Rational(9,2)/c)
    for t in (s.Rational(1,7),s.Rational(1,2),s.Rational(1)):
        alpha=t*t/(2*d*d*(d+1))
        equal(2*K/(alpha*d),4*K*d*(d+1)/(t*t),'Gram-weight coefficient')
        equal(alpha*d*(d-s.Rational(1,d)),t*t*(d-1)/(2*d*d),
              'reset optimum gain before rigidity')

print(json.dumps({'schema':'gtf91.rigidity-regression/1','status':'success',
    'positive_checks':checks,'negative_controls':negative,
    'continuum_proof_by_regression':False,'physical_reset_calibration':False,
    'history_probabilities_identified_with_gram_weights':False,
    'unique_instrument_or_dilation_claimed':False,
    'independent_priority_clearance':False},sort_keys=True))
