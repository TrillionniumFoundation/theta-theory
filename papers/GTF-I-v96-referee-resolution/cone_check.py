#!/usr/bin/env python3
"""Exact finite regressions for one-sided cones and finite-pair neighborhoods.

The universal analytic inequalities are written proofs. These tests pin
matrix identities, certificate replay, finite classical laws, and scope.
"""
from copy import deepcopy
from fractions import Fraction as F
from math import factorial, isqrt
import json
import sympy as s
from cone_geometry import (INPUT,classify,certify,verify,require,matrix_to_json,
    psd,matrix_tuple_legal,gaussian)
from covariance_metric import system,inner,covariance
from curve_geometry import classify as two_sided

positive=0;negative=0;finite_classical=0;range_checks=0

def check(condition,message):
    global positive
    require(bool(condition),message);positive+=1

def rejects(action):
    global negative
    try:action()
    except (ValueError,TypeError,KeyError):negative+=1;return
    raise ValueError('invalid input or mutated certificate was accepted')

def raw(e,h,pair=None):
    return {'schema':INPUT,'dimension':e[0].rows,'outcomes':len(e),
        'effects':[matrix_to_json(a) for a in e],
        'direction':[matrix_to_json(a) for a in h],'pair':pair}

def pairdata(e,h,t,f=None,allowance=0):
    f=f if f is not None else [a+t*b for a,b in zip(e,h)]
    return {'effects':[matrix_to_json(a) for a in f],'scale':str(t),
        'remainder_budget':str(allowance*len(e)),
        'component_budgets':[str(allowance)]*len(e)}

def distance(p,q,n):
    # Multinomial aggregation checks all count vectors, not a sampled subset.
    if len(p)==2:
        return sum(F(factorial(n),factorial(i)*factorial(n-i))*abs(p[0]**i*p[1]**(n-i)-q[0]**i*q[1]**(n-i)) for i in range(n+1))
    return sum(F(factorial(n),factorial(i)*factorial(j)*factorial(n-i-j))*
        abs(p[0]**i*p[1]**j*p[2]**(n-i-j)-q[0]**i*q[1]**j*q[2]**(n-i-j))
        for i in range(n+1) for j in range(n-i+1))

I=s.eye(2);Z=s.zeros(2);P=s.diag(1,0);Q=I-P
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);D=s.diag(1,-1)
fixtures=[
 ('regular_tangent',[I/2,I/2],[X/10,-X/10]),
 ('coherent_tangent',[P,Q],[X,-X]),
 ('support_opening',[P,Q],[Q-P,P-Q]),
 ('support_opening',[P,Q],[Q-P+X,P-Q-X]),
 ('support_opening',[s.Matrix([[0]]),s.Matrix([[1]])],[s.Matrix([[1]]),s.Matrix([[-1]])]),
 ('higher_order_undetermined',[P,Q],[Z,Z]),
 ('regular_tangent',[I/3+X/12,I/3+D/12,I/3-(X+D)/12],[Y/20,X/20,-(Y+X)/20]),
]
# A singular opening block with a cross term into its own kernel.
E3=[s.diag(1,0,0),s.diag(0,1,1)]
H3a=s.Matrix([[-1,0,1],[0,1,0],[1,0,0]]);H3=[H3a,-H3a]
fixtures.append(('support_opening',E3,H3))
for expected,e,h in fixtures:
    c=classify(e,h);cert=certify(raw(e,h));d=e[0].rows
    check(c['mode']==expected,'wrong acquisition mechanism')
    check(verify(raw(e,h),cert)['complete_exact_replay'],'certificate replay failed')
    check(all(psd(a) for a in c['missing']),'negative missing-support cone block')
    check(c['gamma']==c['gamma'].adjoint(),'support generator not Hermitian')
    check(cert['physical_protocol_executed'] is False and cert['continuum_proof_by_replay'] is False,
        'finite execution scope changed')
    basis,G,L=system(e);rhs=s.Matrix([inner(a,h) for a in basis])
    exact_range=L.rank()==L.row_join(rhs).rank()
    check(exact_range==c['in_range'],'support criterion disagrees with full covariance range');range_checks+=1
    if c['lineality']:
        inherited=two_sided(e,h)
        check(inherited['in_span']==c['in_range'],'two-sided specialization failed')
    else:
        rejects(lambda:two_sided(e,h))
        w=c['witness'];j=w['label_index'];r=w['coordinate_index'];v=(s.eye(d)-c['supports'][j])[:,r]
        check((v.adjoint()*e[j]*v)[0]==0,'base opening event not impossible')
        check((v.adjoint()*h[j]*v)[0]>0,'opening witness has nonpositive slope')
        check(str((v.adjoint()*v)[0])==w['norm_squared'],'wrong rational witness norm')

# Exact cone realization, including off-support cross terms that make E+sH indefinite.
t=s.symbols('t',real=True)
for e,h in [([P,Q],[X,-X]),([P,Q],[Q-P+X,P-Q-X]),(E3,H3)]:
    d=e[0].rows;k=len(e);c=s.Rational(25)
    curve=[(a+t*b+c*t*t*s.eye(d))/(1+k*c*t*t) for a,b in zip(e,h)]
    check(sum(curve,s.zeros(d)).applyfunc(s.simplify)==s.eye(d),'cone realization not normalized')
    for a,b,g in zip(e,h,curve):
        check(g.subs(t,0)==a,'wrong cone base')
        check(g.diff(t).subs(t,0)==b,'wrong cone first derivative')
    for value in [s.Rational(1,64),s.Rational(1,32),s.Rational(1,16),s.Rational(1,8)]:
        f=[g.subs(t,value) for g in curve]
        check(matrix_tuple_legal(f,False),'normalized cone realization not legal')
        p=pairdata(e,h,value,f,s.Rational(500))
        ctf=certify(raw(e,h,p));check(ctf['finite_pair']['verified'],'finite cone remainder not certified')
        check(verify(raw(e,h,p),ctf)['complete_exact_replay'],'finite cone replay failed')
check(not psd(E3[0]+s.Rational(1,100)*H3[0]),'cross-kernel opening test lost its obstruction')

# Noncommuting covariance images are regular directions; scalings and permutations are exact.
e=[(I+D)/4,(I-D)/4,(I+X)/4,(I-X)/4]
for K in [[X,Y,D,-X-Y-D],[D,X,Y,-D-X-Y],[Y,D,X,-Y-D-X]]:
    h=covariance(e,K);c=classify(e,h)
    check(c['in_range'] and c['lineality'],'covariance image not in regular cone')
    for scale in [s.Rational(1,3),s.Rational(2),s.Rational(-1)]:
        cc=classify(e,[scale*a for a in h])
        check(cc['mode']==c['mode'],'lineality mechanism not scaling invariant')
        check(cc['gamma']==scale*c['gamma'],'generator scaling failed')
    for permutation in [[3,2,1,0],[1,2,3,0]]:
        cc=classify([e[i] for i in permutation],[h[i] for i in permutation])
        check(cc['in_range']==c['in_range'] and cc['gamma']==c['gamma'],'outcome permutation failed')
U=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
for _,e,h in fixtures[:4]:
    c=classify(e,h);cc=classify([U*a*U.T for a in e],[U*a*U.T for a in h])
    check(cc['mode']==c['mode'],'rational unitary changed mechanism')
    check(cc['gamma']==U*c['gamma']*U.T,'generator conjugation failed')

# Finite canonical factors: the H=X rotation has B*B=I and rational effects.
e=[P,Q];h=[X,-X]
for value in [s.Rational(1,32),s.Rational(1,16),s.Rational(1,8),s.Rational(1,4)]:
    g=[(P+value*X+value**2*Q)/(1+value**2),(Q-value*X+value**2*P)/(1+value**2)]
    check(matrix_tuple_legal(g,False),'normalized rank-one factors not legal')
    check(g[0].rank()==g[1].rank()==1,'rotation changes rank')
    for a,b,u in zip(e,g,h):
        rem=b-a-value*u
        check(psd(3*value**2*I+rem) and psd(3*value**2*I-rem),'factor remainder constant failed')
    opening=[(1-value**2)*a+value**2*I/2 for a in g]
    check(all(a.det()>0 for a in opening),'second-order opening not full rank')
    ctf=certify(raw(e,h,pairdata(e,h,value,opening,s.Rational(4))))
    check(ctf['mechanism']=='coherent_tangent','rank-opening tube changed coherent first jet')
    for n in [1,2,4,9]:
        # Exact squared Choi-record trace separation is 4*(1-(1+s²)^(-n)).
        sq=4*(1-(1+value**2)**(-n))
        check(0<sq<=4*n*value**2,'product Choi fidelity bound failed')
        check(sq<=4,'product Choi trace cap failed')

# Complete finite scalar laws: support opening and power reparametrization.
for q in [1,2,3,4]:
    for tt in [F(1,8),F(1,4)]:
        p=tt**q
        e=[s.Matrix([[0]]),s.Matrix([[1]])];h=[s.Matrix([[1]]),s.Matrix([[-1]])]
        scale=s.Rational(p.numerator,p.denominator);ctf=certify(raw(e,h,pairdata(e,h,scale)))
        check(ctf['finite_pair']['opening_event_probability']==str(p),'opening probability not exact')
        for n in [1,2,4,9]:
            dist=distance([F(0),F(1)],[p,1-p],n);finite_classical+=1
            check(dist==2*(1-(1-p)**n),'opening product law mismatch')
            check(min(F(1),n*p)<=dist<=2*min(F(1),n*p),'opening finite linear order failed')
# Mixed rates: count-vector enumeration includes every multinomial outcome.
for a,b in [(2,3),(3,4),(3,5)]:
    for tt in [F(1,8),F(1,4)]:
        u=tt**a;v=tt**b
        p=[F(1,2),F(1,2),F(0)];qq=[(1-v)*(F(1,2)+u),(1-v)*(F(1,2)-u),v]
        for n in [1,4,9,16]:
            dist=distance(p,qq,n);finite_classical+=1
            leak=2*(1-(1-v)**n)
            coin=distance([F(1,2),F(1,2)],[F(1,2)+(1-v)*u,F(1,2)-(1-v)*u],n)
            check(dist>=leak and dist>=coin,'mixed-law coarse lower failed')
            check(dist<=min(F(2),2*n*v+3*isqrt(n)*u),'mixed-law upper failed')
            check(dist>=F(1,512)*min(F(1),isqrt(n)*u+n*v),'mixed-law lower constant failed')

# Negative inputs and certificate mutations. No partial theorem classification is returned.
e=[P,Q];h=[X,-X];good=raw(e,h);ctf=certify(good)
for field,value in [('mechanism','regular_tangent'),('direction_in_covariance_range',True),
    ('physical_protocol_executed',True),('local_interval_computed',True),
    ('two_sided_first_order_realizable',1),('covariance_kernel_dimension',True),
    ('independent_probe_scale','N*s'),('opening_witness',{}),('extra',0)]:
    bad=deepcopy(ctf);bad[field]=value;rejects(lambda:verify(good,bad))
for field,value in [('dimension',True),('outcomes',1),('schema','old'),('extra',0)]:
    bad=deepcopy(good);bad[field]=value;rejects(lambda:certify(bad))
bad=deepcopy(good);bad['direction'][0][0][0][0]='1';rejects(lambda:certify(bad))
bad=deepcopy(good);bad['effects'][0][0][0][0]='2/2';rejects(lambda:certify(bad))
rejects(lambda:classify([P,Q],[-Q,Q]))
rejects(lambda:certify(good,1));rejects(lambda:certify(good,True))
pair=raw([I/2,I/2],[X/10,-X/10],pairdata([I/2,I/2],[X/10,-X/10],s.Rational(1,4)))
for field,value in [('scale','0'),('remainder_budget','-1'),('component_budgets',['1','0'])]:
    bad=deepcopy(pair);bad['pair'][field]=value;rejects(lambda:certify(bad))
bad=deepcopy(pair);bad['pair']['effects']=[matrix_to_json(a) for a in [I/2,I/2]];rejects(lambda:certify(bad))
bad=deepcopy(pair);bad['pair']['effects'][0][0][0][0]='-1';rejects(lambda:certify(bad))
zero=certify(raw([P,Q],[Z,Z]))
check(zero['mechanism']=='higher_order_undetermined' and zero['theorem'] is None,'zero direction falsely classified')
check(zero['adaptive_scale'] is None and zero['stationarity_inferred_from_zero_direction'] is False,
    'zero direction falsely stationary')
print(json.dumps({'schema':'gtf86.cone-check/1','status':'success','positive_checks':positive,
    'negative_controls':negative,'complete_finite_classical_laws':finite_classical,
    'full_covariance_range_crosschecks':range_checks,'noncommuting_tests':True,
    'singular_opening_cross_kernel_test':True,'all_three_mechanisms_checked':True,
    'finite_pair_remainder_checks':True,'product_Choi_fidelity_identities':True,
    'physical_protocol_executed':False,'continuum_theorem_verified_by_finite_tests':False},
    indent=2,sort_keys=True))
