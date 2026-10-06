#!/usr/bin/env python3
"""Finite exact regressions; the universal arguments are in the manuscript."""
import json
import sympy as s

positive = 0
negative = 0

def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)

def eq(x, y, message):
    global positive
    if isinstance(x, s.MatrixBase):
        require((x-y).applyfunc(s.simplify) == s.zeros(*x.shape), message)
    else:
        require(s.simplify(x-y) == 0, message)
    positive += 1

def differs(x, y, message):
    global negative
    require(s.simplify(x-y) != 0, message)
    negative += 1

def swap(d):
    return s.Matrix(d*d, d*d, lambda i,j: int(i//d == j%d and i%d == j//d))

I = s.eye(2)
X = s.Matrix([[0,1],[1,0]])
Y = s.Matrix([[0,-s.I],[s.I,0]])
Z = s.diag(1,-1)
S = swap(2)
minus = (s.eye(4)-S)/2
plus = (s.eye(4)+S)/2
singlet = s.Matrix([0,1,-1,0])/s.sqrt(2)
phi = s.Matrix([1,0,0,1])/s.sqrt(2)
eq((singlet.H*singlet)[0],1,'normalized antisymmetric input')
eq((phi.H*phi)[0],1,'normalized Bell vector')
eq(minus,singlet*singlet.H,'antisymmetric reference effect')
eq(minus+plus,s.eye(4),'complementary reference projections')

for t in (s.Rational(0),s.Rational(1,7),s.Rational(1,2),s.Rational(1)):
    bases = [((I+e*t*A)/2,(I-e*t*A)/2) for A in (X,Y,Z) for e in (-1,1)]
    C = (I/2,I/2)
    a = t*t/24
    for y in range(2):
        eq(sum((E[y] for E in bases),s.zeros(2))/6,C[y],'one-call channel average')
        for z in range(2):
            moment=sum((s.kronecker_product(E[y],E[z]) for E in bases),s.zeros(4))/6
            W=s.kronecker_product(C[y],C[z])/2-moment/2
            eq(W, (1 if y==z else -1)*a*(s.eye(4)-2*S),'equal-prior payoff')
            redraw=s.kronecker_product(sum((E[y] for E in bases),s.zeros(2))/6,
                                       sum((E[z] for E in bases),s.zeros(2))/6)
            eq(redraw,s.kronecker_product(C[y],C[z]),'redrawn-index negative control')
            F=minus if y==z else plus
            T=F.T/4
            Tc=(s.eye(4)-F).T/4
            eq(T+Tc,s.eye(4)/4,'tester deterministic block')
            eq(sum(T+Tc),1,'deterministic tester trace')
    events=[]
    old_events=[]
    input_events=[]
    classical_events=[]
    for E in [C]+bases:
        q=s.Integer(0); oldq=s.Integer(0); aq=s.Integer(0); cq=s.Integer(0)
        for y in range(2):
            for z in range(2):
                receiver=s.kronecker_product(E[y].T,E[z].T)/4
                F=minus if y==z else plus
                q+=s.trace(F*receiver)
                if y==z:
                    oldq+=s.trace(minus*receiver)
                    aq+=(singlet.H*s.kronecker_product(E[y],E[z])*singlet)[0]
                else:
                    cq+=E[y][0,0]*E[z][0,0]
        events.append(s.simplify(q));old_events.append(s.simplify(oldq))
        input_events.append(s.simplify(aq));classical_events.append(s.simplify(cq))
    eq(events[0],s.Rational(1,2),'fair reset event under scalar')
    eq(old_events[0],s.Rational(1,8),'biased reset event under scalar')
    for q in events[1:]:eq(q,s.Rational(1,2)-t*t/4,'fair reset alternative event')
    for q in old_events[1:]:eq(q,(1-t*t)/8,'biased reset alternative event')
    for q in input_events[1:]:eq(q,(1-t*t)/2,'antisymmetric input alternative event')
    eq(sum(classical_events[1:])/6,s.Rational(1,2)-t*t/6,'classical unequal-label average')
    p_reset=events[0]/2+(1-sum(events[1:])/6)/2
    p_ca=classical_events[0]/2+(1-sum(classical_events[1:])/6)/2
    p_all=input_events[0]/2+(1-sum(input_events[1:])/6)/2
    eq(p_ca,s.Rational(1,2)+t*t/12,'classical exact formula')
    eq(p_reset,s.Rational(1,2)+t*t/8,'reset exact formula')
    eq(p_all,s.Rational(1,2)+t*t/4,'all-adaptive exact formula')
    if t:
        differs(p_reset,old_events[0]/2+(1-sum(old_events[1:])/6)/2,
                'old biased readout is not equal-prior optimal')
        require(p_ca<p_reset<p_all,'strict qubit hierarchy')
        negative+=1

eq(p_ca,s.Rational(7,12),'qubit classical 7/12')
eq(p_reset,s.Rational(5,8),'qubit reset 5/8')
eq(p_all,s.Rational(3,4),'qubit unrestricted 3/4')
differs(s.Rational(1,7),s.Rational(1,2),'hypothesis prior is not uniform on seven devices')
differs(s.trace(minus*s.eye(4)),s.trace(minus*s.eye(4)/16),'Choi probability factor cannot be omitted')

for d in range(2,13):
    for weights in ([s.Rational(1,d)]*d,
                    [s.Rational(i+1,d*(d+1)//2) for i in range(d)],
                    [s.Integer(1)]+[s.Integer(0)]*(d-1)):
        # For A=B=diag(weights) the exact trace norm is d(tr A)^2-tr(A^2).
        value=(d-1)*sum(x*x for x in weights)+2*d*sum(weights[i]*weights[j]
                                                    for i in range(d) for j in range(i+1,d))
        eq(value,d-sum(x*x for x in weights),'centered diagonal spectrum')
        bound=s.Rational(d*d-1,d)
        require(value<=bound,'centered norm bound')
        eq(value==bound,len(set(weights))==1,'centered equality characterization')
        positive+=1
    for t in (s.Rational(0),s.Rational(1,3),s.Rational(1)):
        ca=s.Rational(1,2)+t*t*s.Rational(d-1,2*d*(d+1))
        reset=s.Rational(1,2)+t*t*s.Rational(d-1,2*d*d)
        allp=s.Rational(1,2)+t*t*s.Rational(1,2*d)
        eq(reset-ca,t*t*s.Rational(d-1,2*d*d*(d+1)),'first exact gap')
        eq(allp-reset,t*t*s.Rational(1,2*d*d),'second exact gap')
        qC=s.Rational((d-1)*(d+2),2*d*d)
        qb=(d-1)*(d+2-2*t*t)/(2*d*d)
        eq(s.Rational(1,2)+(qC-qb)/2,reset,'all-dimension reset event score')
        require(s.Rational(1,2)<=ca<=reset<=allp<=1,'probability range')
        positive+=1

print(json.dumps({'schema':'gtf91.equal-prior-regression/1','status':'success',
    'positive_checks':positive,'negative_controls':negative,
    'qubit_values':['7/12','5/8','3/4'],
    'continuum_proof_by_regression':False,'physical_reset_calibration':False,
    'independent_priority_clearance':False,'arbitrary_pair_strict_gap':False},sort_keys=True))
