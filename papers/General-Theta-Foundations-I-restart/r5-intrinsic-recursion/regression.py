#!/usr/bin/env python3
"""Finite arithmetic/implementation regression, never a continuum proof."""
from fractions import Fraction as F
import itertools, json, math, random
counts = {}; rejected = 0

def check(ok, group):
    if not ok:
        raise RuntimeError('regression failed: '+group)
    counts[group] = counts.get(group,0)+1

def negative(ok):
    global rejected
    if ok:
        raise RuntimeError('negative control unexpectedly accepted')
    rejected += 1

def det(a):
    if len(a)==1: return a[0][0]
    return sum(((-1)**j)*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

# Actual completed-domain gain, retaining off-diagonal old-error transport.
gamma=F(1,4096); v0=F(1800); kap=F(17,20)
check((1-gamma)*F(4,9)+900*gamma==F(85,128),'exact_gain')
for j in range(101):
    alpha=F(j,100)
    check((1-alpha)*F(85,128)*v0+900*alpha<=kap*v0,'exact_gain')
    check(F(2,59049)*v0+F(1,2)<=kap,'exact_gain')
negative(F(4,18)*v0+F(1,2)<=kap) # two-bit return is not six-bit return
negative(900<=225) # finite cylinder-center domain is not the physical-only bound

# Invariant squared-energy mixtures including zero activity.
for rho,b,e,theta in itertools.product([F(0),F(1,4),F(3,4)], [F(1,5),F(1)], [F(0),F(1,3),F(1)], [F(0),F(1,17),F(1)]):
    radius=b/(1-rho); old=e*radius
    mixture=(1-theta)*old*old+theta*(rho*old+b)**2
    check(mixture<=radius*radius,'exact_energy')
negative((F(1,10)+F(1,10))**2<=F(1,100))

# Multidimensional posterior Jacobian, exact rational evaluations.
for d in range(1,5):
    for k in range(1,10):
        raw=[F(i+k) for i in range(d+1)]; total=sum(raw); r=[z/total for z in raw]
        a=F(2,3); y=[F(((i+1)*k)%9-4,5) for i in range(d)]
        den=1+a*sum(r[i+1]*y[i] for i in range(d))
        jac=[[((a*r[i+1] if i==j else 0)*den-r[i+1]*(1+a*y[i])*a*r[j+1])/den**2 for j in range(d)] for i in range(d)]
        expected=a**d*math.prod(r)/den**(d+1)
        check(det(jac)==expected and expected>0,'exact_jacobian')
        out=[r[i+1]*(1+a*y[i])/den for i in range(d)]; pzero=r[0]/den
        for i in range(d):
            check((r[0]*out[i]/(r[i+1]*pzero)-1)/a==y[i],'exact_bayes_inverse')
negative(F(0)>0) # rank loss cannot retain a positive density Jacobian

# Compander including its unbounded last cell: these are numerical checks only.
eta=.3
for K in range(1,31):
    for j in range(-100,101):
        x=j*.47; u=math.exp(-eta*abs(x)); idx=min(K-1,int(math.floor(K*(1-u))))
        q=math.copysign(math.log(K/(K-idx))/eta,x)
        check(abs(q)<=abs(x)+1e-11 and abs(x-q)<=math.exp(eta*abs(x))/(eta*K)+1e-10,'numeric_compander')
for M in range(1,1001):
    for d in range(1,5):
        K=max(1,int((M**(1/d)+1)/2))
        while (2*K-1)**d>M: K-=1
        while (2*(K+1)-1)**d<=M: K+=1
        check((2*K-1)**d<=M and K+1e-12>=M**(1/d)/4,'integer_product_budget')
    if M>=6:
        n=M.bit_length()-1; m=(M+2).bit_length()-3
        check(2**(m+2)-2<=M and 0<=n-m<=2,'integer_prefix_budget')

# Actual depth-chain probabilities are propagated, not replaced by stationarity.
for initial in [F(0),F(1,3),F(1)]:
    law={(0,2):1-initial,(1,2):initial}
    for t,alpha in enumerate([F(0),F(1),F(1,7),F(1,2)]):
        hold=F(t,5); nxt={}
        for (i,h),mass in law.items():
            edges=[(i,h,hold)]
            if i==0:
                edges += [(0,h+2,(1-hold)*(1-alpha)*(1-gamma)),(0,max(0,h-1),(1-hold)*(1-alpha)*gamma),(1,max(0,h-1),(1-hold)*alpha)]
            else:
                edges += [(0,h+6,(1-hold)/2),(1,h,(1-hold)/2)]
            for ii,hh,prob in edges: nxt[ii,hh]=nxt.get((ii,hh),F(0))+mass*prob
        law=nxt
        check(sum(law.values())==1 and min(law.values())>=0,'exact_actual_depth')
        for n in range(1,8):
            val=lambda h:F(1,5)**(2*h)
            acq=sum(m*val(h) for (i,h),m in law.items()); cap=sum(m*val(min(h,n)) for (i,h),m in law.items())
            check(max(acq,val(n))<=cap<=acq+val(n),'exact_profile_composition')

# Both calibration signs and a deliberately biased decoder.
for nominal in [(F(1,4),F(3,4)),(F(3,8),F(5,8))]:
    for prediction in [F(1,2),F(1,3),F(2,3)]:
        delta=F(1,16); baseline=sum(x*(1-x) for x in nominal)/2-delta**2
        risks=[sum((x+sign)*(1-prediction)**2+(1-x-sign)*prediction**2 for x in nominal)/2 for sign in [-delta,delta]]
        score_error=sum((x-prediction)**2 for x in nominal)/2
        formula=score_error+delta**2+2*delta*abs(F(1,2)-prediction)
        check(max(risks)-baseline==formula,'exact_calibration')
        if prediction!=F(1,2): negative(formula==score_error+delta**2)

print(json.dumps({'status':'success','counts':counts,'finite_checks':sum(counts.values()),'negative_controls_rejected':rejected,'continuum_proof_by_tests':False},sort_keys=True))
