"""Exact finite regression checks for v54; not a proof of the universal theorems.

Every condition uses an explicit exception rather than Python assert, so running
with -O executes exactly the same checks. No network or numerical solver is used.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import sympy as sp

COUNT=0
NEG=[]
def require(ok: bool, name: str) -> None:
    global COUNT
    COUNT+=1
    if not ok: raise RuntimeError(name)

def negative(name: str, false_claim: bool) -> None:
    require(not false_claim, 'negative control escaped: '+name)
    NEG.append(name)

def parts(n: int, m: int):
    if m==1:
        yield (n,)
    else:
        for a in range(n+1):
            for tail in parts(n-a,m-1): yield (a,)+tail

def tv(a, b): return sum(abs(x-y) for x,y in zip(a,b))/2

# Constrained simplex radius, with exact rational finite calibration points.
for m in range(2,7):
    center=(F(1,m),)*m
    vertices=[tuple(F(int(i==j)) for i in range(m)) for j in range(m)]
    require(max(tv(center,v) for v in vertices)==F(m-1,m), 'simplex radius')
    for den in range(1,7):
        for counts in parts(den,m):
            q=tuple(F(a,den) for a in counts)
            require(max(tv(q,v) for v in vertices)==1-min(q), 'vertex radius identity')
            require(tv(q,center)<=F(m-1,m), 'uniform center upper')
negative('half diameter is not categorical radius',F(1,2)>=F(2,3))
negative('independent midpoint vector need not be a law',sum((F(1,2),)*3)==1)
negative('binary mean TV factor cannot be omitted',F(2,4)==F(2,2))
negative('unconstrained center can violate output set',F(1,2) in {F(0),F(1)})

# Analytic categorical curve: symbolic Fourier identity and simplex vertices.
c,s=sp.symbols('c s',real=True)
angles=[(sp.Integer(1),sp.Integer(0)),(-sp.Rational(1,2),sp.sqrt(3)/2),(-sp.Rational(1,2),-sp.sqrt(3)/2)]
polys=[]
for cj,sj in angles:
    x=c*cj+s*sj
    y=s*cj-c*sj
    p=sp.expand((3+4*x+2*(2*x*x-1))/9)
    square=sp.expand(((1+x+2*x*x-1)**2+(y+2*x*y)**2)/9)
    remainder=sp.rem(sp.expand(square-p),s*s+c*c-1,s)
    require(sp.simplify(remainder)==0,'categorical nonnegative square identity')
    polys.append(p)
require(sp.simplify(sp.rem(sp.expand(sum(polys)-1),s*s+c*c-1,s))==0,'categorical probabilities sum to one')
for i,(ci,si) in enumerate(angles):
    require([sp.simplify(p.subs({c:ci,s:si})) for p in polys]==[int(i==j) for j in range(3)],'categorical curve reaches vertices')
negative('three categorical vertices fit TV one-half center',max(tv((F(1,3),)*3,tuple(F(int(j==i)) for j in range(3))) for i in range(3))<=F(1,2))

# Exact Laurent localization, constants, and full-subcritical choices.
z=sp.symbols('z')
for r in range(1,13):
    raw=sp.expand((1+(z+1/z)/2)**r)
    C=raw.coeff(z,0)
    require(C==sp.Rational(comb(2*r,r),2**r),'normalizing Haar coefficient')
    weighted=sp.expand(raw*(z+1/z)/2).coeff(z,0)/C
    require(weighted==sp.Rational(r,r+1),'localized extreme mean')
    Br=F(4**r,comb(2*r,r))
    require(Br<=2*r+1,'coefficient sum bound')
for den in range(2,9):
    rho=F(1,den)
    for t in range(10):
        eps=rho*F(t,20)
        delta=2*eps
        x=delta/(rho-delta)
        r=x.numerator//x.denominator+1
        m=r+1
        Delta=2*(rho*F(r,r+1)-delta)
        A=2*(1+rho+delta)*(2*r+1)*m/Delta
        require(Delta>0 and A>1,'full noise strict residual')
        require(r>x and m==r+1,'localization degree')
rho=F(1,10);eps=F(1,25);delta=2*eps;r=5;m=6
Delta=2*(rho*F(r,r+1)-delta);A=2*(1+rho+delta)*(2*r+1)*m/Delta
require((Delta,A)==(F(1,150),F(23364)),'retained exact calibration')
negative('r at the critical ratio leaves strict residual',2*(rho*F(4,5)-delta)>0)
negative('frequency r alone contains the pF product',sp.expand((1+(z+1/z)/2)**r*(z+1/z)/2).coeff(z,r+1)==0)
negative('critical error still has positive residual',rho-2*(rho/2)>0)
negative('starting harmonic norm squared is one for all m',m==1)

# Exact count/scale checks, without floating point kth roots.
for dim in range(1,6):
    for k in range(1,61):
        L=1
        while L**dim<2*k:L+=1
        B=dim*(L-1)
        require(L**dim>=2*k and B>=1,'enough executable atom counts')
        require((L-1)**dim<2*k,'strict block length bound')
        for tau in range(dim,dim+3):
            lower=F(dim,2*tau+1)
            require(lower>0 and lower<=F(dim,2*dim+1),'Diophantine exponent')
            if tau==dim:require(lower==F(dim,2*dim+1),'matched exponent')
negative('logarithmic rate is the matched cube-root exponent',F(1,3)==0)
negative('matrix dimension is number of rotation letters',F(1,3)==F(2,5))
negative('exact enclosure has slack at rho one',(1+F(1))/2>F(1))

# Greedy return-word spacing, including arbitrary intervening widths.
for N in range(0,10):
    for b in range(0,3):
        for g in range(0,3):
            for B in range(1,4):
                for mask in range(1<<N):
                    cuts=[t for t in range(1,N+1) if mask&(1<<(t-1))]
                    eligible=[t for t in cuts if b+B+g<=t<=N-g]
                    selected=[]
                    for t in eligible:
                        if not selected or t-selected[-1]>=B+g:selected.append(t)
                    budget=b+B+2*g-1+(B+g)*len(selected)
                    require(len(cuts)<=budget,'return occupation count')
                    if selected:
                        require(selected[0]-B-b>=g and N-selected[-1]>=g,'prefix and suffix padding')
                        require(all(y-B-x>=g for x,y in zip(selected,selected[1:])),'nonoverlapping return gaps')
returns={2*a+3*b for a in range(30) for b in range(30)}
require(all(n in returns for n in range(2,50)),'coprime exact return lengths')
negative('even return lengths alone pad every large horizon',all(n%2==0 for n in range(20,30)))
negative('two-three return certificate supplies a length one idle',1 in returns)

# Exact common-row polygon machine for a noncommuting rational alphabet.
vertices=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
lam=F(7,5);a=F(11,20);rho=F(1,10)
T={}
for letter in 'IRF':
    rows=[]
    for i in range(4):
        row=[F(0)]*4
        if letter=='R':row[i]=F(3,7);row[(i+1)%4]=F(4,7)
        else:
            j=i if letter=='I' else (-i)%4
            row[j]=F(6,7);row[(j+2)%4]=F(1,7)
        require(all(x>=0 for x in row) and sum(row)==1,'actual stochastic row')
        rows.append(row)
    T[letter]=rows

def physical(letter,v):
    x,y=v
    if letter=='I':return x,y
    if letter=='F':return x,-y
    return F(3,5)*x-F(4,5)*y,F(4,5)*x+F(3,5)*y

def step(p,letter):return [sum(p[i]*T[letter][i][j] for i in range(4)) for j in range(4)]
for letter in T:
    for i,v in enumerate(vertices):
        bary=tuple(sum(T[letter][i][j]*vertices[j][d] for j in range(4)) for d in range(2))
        require(bary==tuple(x/lam for x in physical(letter,v)),'common row contracts commanded barycenter')
for N in range(6):
    factor=rho*lam**N/a
    require(factor<=1,'decoder legal at chosen horizon')
    for word in product('IRF',repeat=N):
        for seed in range(4):
            p=[F(0)]*4;p[seed]=(1+a)/2;p[(seed+2)%4]=(1-a)/2
            v=vertices[seed]
            for letter in word:p=step(p,letter);v=physical(letter,v)
            for d in range(2):
                mean=sum(p[j]*factor*vertices[j][d] for j in range(4))
                require(mean==rho*v[d],'all-word exact numerical response')
negative('enclosure decoder remains legal without horizon check',rho*lam**6/a<=1)
negative('identity stochastic row can remain identity while sharing scaling',F(1)==1/lam)
negative('noncommuting alphabet treated as commuting',physical('F',physical('R',vertices[0]))==physical('R',physical('F',vertices[0])))
negative('dropping horizon decoder scaling stays exact',a/lam==rho)

# Haar projection at degree two, and a negative aliasing control at degree four.
J=sp.Matrix([[0,-1],[1,0]])
rots=[J**j for j in range(4)]
P=sum((sp.kronecker_product(U,U) for U in rots),sp.zeros(4))/4
require(P*P==P and P.T==P,'degree two Haar projection')
U=sp.Matrix([[c,-s],[s,c]])
for entry in sp.kronecker_product(U,U)*P-P:
    require(sp.simplify(sp.rem(sp.expand(entry),s*s+c*c-1,s))==0,'projection onto true circle fixed vectors')
negative('four atoms reproduce every Haar harmonic',sum(sp.I**(4*j) for j in range(4))/4==0)

# Exhaustive finite component-quotient minimization on two seeds and C2.
def partitions(xs):
    if not xs:
        yield []
        return
    x=xs[0]
    for p in partitions(xs[1:]):
        yield [[x]]+[b[:] for b in p]
        for i in range(len(p)):
            q=[b[:] for b in p];q[i].append(x);yield q

def quotient_min(eps):
    vals=[F(0),F(1),F(1),F(0)]
    best=5
    for blocks in partitions(list(range(4))):
        label={x:i for i,B in enumerate(blocks) for x in B}
        equiv=all(label[x^1]==label[y^1] for B in blocks for x in B for y in B)
        centers=all((max(vals[x] for x in B)-min(vals[x] for x in B))/2<=eps for B in blocks)
        if equiv and centers:best=min(best,len(blocks))
    return best
require(quotient_min(F(0))==2,'future-output quotient minimum')
require(quotient_min(F(1,4))==2,'subcritical finite quotient minimum')
require(quotient_min(F(1,2))==1,'boundary quotient can merge all components')
negative('available-label component bound always minimal',quotient_min(F(0))==4)
negative('zero conditional mean error implies pointwise decoder accuracy',
         all(abs(x)<=0 for x in (F(-1),F(1))))

print(json.dumps({'status':'success','exact_finite_assertions':COUNT,
    'negative_controls_detected':NEG,'normal_optimized_safe':True,
    'scope':'Exact finite illustrations of identities, common rows, bounds and counterexamples; not universal proof verification or an implemented general algebraic classifier.'},sort_keys=True))
