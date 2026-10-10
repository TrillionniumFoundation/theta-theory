#!/usr/bin/env python3
"""Deterministic finite regressions. Not proofs of the continuum statements."""
from fractions import Fraction as F
from itertools import product
import json

checks = 0
negative = 0

def require(ok, message):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(message)

def reject(ok, message):
    global negative
    if ok:
        raise RuntimeError('Negative control survived: ' + message)
    negative += 1

# Exact raw-flow recharge, including vanishing activity and rare components.
eta, G, K = F(1), F(15), F(500)
AG, CB = (1+eta)*G*G-1, 1+1/eta
D = CB*(K+1)/(K-AG)
for power in range(1,14):
    w = [F(1,10**power), 1-F(1,10**power)]
    for omega in ([F(1),F(0)], [F(0),F(1)], [F(1,2),F(1,2)]):
        for activity in (F(0),F(1,1000000),F(1,7),F(1)):
            u, v = activity/2001, 2000*activity/2001
            h = 1-activity
            pi = [(a+b)/2 for a,b in zip(w,omega)]
            wn = [(h+u)*a+v*b for a,b in zip(w,pi)]
            require(sum(wn)==1, 'actual forward law normalized')
            for a,b,c in zip(w,pi,wn):
                x,y = u*a,v*b
                require(y>=K*x, 'raw expansion/refresh balance')
                lhs=D*(h*a+(1+eta)*G*G*x)+CB*(x+y)
                require(lhs<=D*c, 'one-step error measure recharge')
                require(D*c-lhs==(D-CB)*y-(D*AG+CB)*x,
                        'recharge deficit exact factorization')
# Not even rare-component constants can fix missing refresh at a positive gain.
reject(D*(1+eta)*G*G+CB<=D, 'expansion without recharge')
reject(D+CB<=D, 'fresh rounding on exact holds')
reject(F(1,1000)==0, 'positive error assigned to a zero-mass stratum')

# Nonhomogeneous binary geometry, exact finite prefixes with all-zero tails.
rhos = [F(1,3) if i%3 else F(1,5) for i in range(10)]
ell = [F(1)]
for r in rhos:
    ell.append(ell[-1]*r)
def point(word):
    return sum(((1-rhos[i])*ell[i]*bit for i,bit in enumerate(word)),F(0))
words=list(product((0,1), repeat=6))
pts=[point(w) for w in words]
for i,x in enumerate(pts):
    fx=point(words[i][1:]+(0,))
    for j,y in enumerate(pts):
        fy=point(words[j][1:]+(0,))
        require(abs(fx-fy)<=15*abs(x-y), 'digit-shift Lipschitz bound')
for k in range(1,17):
    n=k.bit_length()-1
    reps=[point(w) for w in product((0,1), repeat=n)]
    require(len(reps)<=k, 'prefix grid cardinality')
    for x in pts:
        require(min(abs(x-r) for r in reps)<=ell[n], 'prefix cover')
        mass=sum(abs(x-y)<ell[n]/100 for y in pts)
        require(F(mass,len(pts))<=F(1,2*k), 'finite small-ball control')
for k in range(2,513):
    r=ell[k.bit_length()-1]
    prev=ell[(k-1).bit_length()-1]
    require(prev*prev<=25*r*r, 'one-label regularity')
reject(F(1,5)**2==F(1,3)**2, 'oscillatory profile replaced by one scale')

# Exact optimal scalar quantization of a finite law by interval dynamic programming.
def distortion(points, weights, m):
    merged={}
    for x,w in zip(points,weights):
        if w:
            merged[x]=merged.get(x,F(0))+w
    xs=sorted(merged)
    n=len(xs)
    pref=[[F(0)] for _ in range(3)]
    for x in xs:
        w=merged[x]
        for a,value in zip(pref,(w,w*x,w*x*x)):
            a.append(a[-1]+value)
    def cost(i,j):
        w,s,t=[a[j]-a[i] for a in pref]
        return t-s*s/w if w else F(0)
    dp=[None]*(n+1);dp[0]=F(0)
    for _ in range(min(m,n)):
        nd=[F(0)]+[None]*n
        for j in range(1,n+1):
            vals=[dp[i]+cost(i,j) for i in range(j) if dp[i] is not None]
            nd[j]=min(vals) if vals else None
        dp=nd
    return dp[n]

for L in (1,2,4,8):
    a=F(1,4)
    mid=[-a/2+a*F(2*i+1,2*L) for i in range(L)]
    for h in (F(0),F(1,1000),F(1,3),F(1)):
        for M in range(1,10):
            q=distortion([F(0)]+mid,[h]+[(1-h)/L]*L,M)
            for delta in (F(0),F(1,16)):
                exact=delta*delta+h*a*a/12+(1-h)*a*a/(12*L*L)+q
                scale=delta*delta+a*a*(h+(1-h)*(F(1,M*M)+F(1,L*L)))
                require(exact>=scale/24, 'single-probe joint lower scale')
                require(exact<=4*scale, 'single-probe joint upper scale')
            if M==1:
                require(h*a*a/12+(1-h)*a*a/(12*L*L)+q==a*a/12,
                        'one-state full variance identity')
for N in range(12):
    for s,rho in product((F(0),F(1,7),F(1)), repeat=2):
        h=(1-s*(1-rho))**N
        w0=1-(1-s)**N
        w1=1-h
        require(0<=w1<=w0<=1,'thinning and acquired mass')
        require(1-(1-s*rho)**N<=N*s*rho,'complete-path coupling allowance')
        for L in (2,4,8):
            lower=(w0-w1)*(1-F(1,L))
            guess0=w0+(1-w0)/L
            guess1=w1+(1-w1)/L
            require(lower==guess0-guess1,'terminal decision-deficiency lower')
            if w1<1:
                fill=(w0-w1)/(1-w1)
                true=w1+(1-w1)*fill/L
                false=(1-w1)*fill*(1-F(1,L))
                require(w0-true==false==lower,'terminal imputation attains lower')
reject((1-F(9,10)**5)*F(3,4)<=F(1,10), 'raw erasure coin equals complete deficiency')
for M in range(1,30):
    for W in range(8):
        require(M*(2**W)>=M,'surviving workspace charged at cut')
        if W and M>1:
            reject(M+W==M*(2**W), 'state cardinality plus workspace bits')
print(json.dumps({'status':'success','finite_checks':checks,
                  'negative_controls_rejected':negative,
                  'continuum_proof_by_tests':False},sort_keys=True))
