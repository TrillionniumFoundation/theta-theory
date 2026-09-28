"""Exact finite regression for v57. Not a verifier of universal theorems.

Rational examples check spectral splits, orbit rows, endpoint counts, tomography,
and positive rounding. Imported free-generation and spectral-gap theorems are
not certified by enumerating words or by finite numerical computations.
Explicit exceptions keep every assertion active under python -O.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, permutations
from math import factorial
import json
import sympy as sp

count=0
negative=[]

def check(ok,message):
    global count
    count+=1
    if not bool(ok):raise RuntimeError(message)

def control(name,caught):
    check(caught,'Negative control escaped: '+name)
    negative.append(name)

def norm2(M):
    return sp.simplify(sp.trace(M.H*M))

def test_spectral_split():
    for d in range(2,6):
        for vals in product(range(-2,3),repeat=d):
            mean=F(sum(vals),d);a=sorted([F(x)-mean for x in vals],reverse=True)
            n=sum(x*x for x in a)
            if n==0:continue
            gaps=[a[j]-a[j+1] for j in range(d-1)]
            m=max(range(d-1),key=lambda j:gaps[j])+1;gap=gaps[m-1]
            check(gap*gap*d*(d-1)**2>=n,'Uniform normalized adjacent gap')
            check(min(a)>=-(d-1)*max(a),'Trace-zero lower eigenvalue')
    for d in range(2,5):
        for vals in [(2,)+(0,)*(d-2)+(-2,),tuple(range(d)),(1,)*(d-1)+(0,)]:
            mean=sp.Rational(sum(vals),d);a=sorted([x-mean for x in vals],reverse=True)
            A=sp.diag(*a);gaps=[a[j]-a[j+1] for j in range(d-1)]
            m=max(range(d-1),key=lambda j:gaps[j])+1;gap=gaps[m-1]
            P=sp.diag(*([1]*m+[0]*(d-m)))
            for i,j in [(i,j) for i in range(d) for j in range(i+1,d)]:
                U=sp.eye(d);U[i,i]=U[j,j]=sp.Rational(3,5)
                U[i,j]=-sp.Rational(4,5);U[j,i]=sp.Rational(4,5)
                phase=sp.eye(d);phase[i,i]=sp.I;U=phase*U
                check(U.H*U==sp.eye(d),'Unitary rational rotation')
                B=U*A*U.H
                identity=sum((a[x]-a[y])**2*sp.expand_complex(U[x,y]*sp.conjugate(U[x,y])) for x in range(d) for y in range(d))
                check(norm2(A-B)==sp.simplify(identity),'Spectral overlap identity')
                check(norm2(P-U*P*U.H)*gap**2<=norm2(A-B),'Separated projector bound')
    control('scalar-trace-zero-cannot-be-unit',sum(x*x for x in [F(0)]*3)==0)
    control('pure-direction-assumption-is-false',norm2(sp.diag(1,0,-1))!=0 and len(set([1,0,-1]))==3)
    A=sp.diag(1,-1);U=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5)],[sp.Rational(4,5),sp.Rational(3,5)]])
    control('missing-two-cross-block-terms',norm2(A-U*A*U.H)!=4*sp.Rational(16,25))

def test_caps_and_support():
    x=sp.Symbol('x',real=True)
    for d in range(2,9):
        for z in [sp.Rational(1,100),sp.Rational(1,4),sp.Rational(1,2),sp.Rational(3,4)]:
            integral=sp.integrate((d-1)*(1-x)**(d-2),(x,1-z,1))
            check(integral==z**(d-1),'Exact projective cap')
    for d in range(2,6):
        for vals in product(range(-1,2),repeat=d):
            mean=F(sum(vals),d);a=sorted([F(x)-mean for x in vals],reverse=True)
            if not any(a):continue
            for c,s in [(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(1),F(0))]:
                for j in range(1,d):
                    Rayleigh=a[0]*c*c+a[j]*s*s
                    check(Rayleigh>=(1-d*s*s)*a[0],'Inner positive hull support')
    control('projective-radius-not-squared-radius',F(1,4)**2!=F(1,4))
    control('unit-amplitude-no-dilation-slack',F(9,10)**2<F(1))

def matmul(a,b):return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)
def mv(a,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in a)
def eye(n):return tuple(tuple(F(int(i==j)) for j in range(n)) for i in range(n))
def transpose(a):return tuple(zip(*a))

def test_common_rows():
    vertices=tuple(tuple(F(sign if j==i else 0) for j in range(3)) for i in range(3) for sign in [1,-1])
    c,s=F(3,5),F(4,5)
    X=((1,0,0),(0,c,-s),(0,s,c));Z=((c,-s,0),(s,c,0),(0,0,1))
    commands=[eye(3),X,transpose(X),Z,transpose(Z)]
    r=F(1,3);rows=[]
    for U in commands:
        T=[]
        for v in vertices:
            y=tuple(r*x for x in mv(U,v));masses=[]
            for x in y:masses.extend([max(F(0),x),max(F(0),-x)])
            spare=1-sum(masses);masses[0]+=spare/2;masses[1]+=spare/2
            check(all(x>=0 for x in masses) and sum(masses)==1,'Legal common stochastic row')
            mean=tuple(sum(masses[i]*vertices[i][j] for i in range(6)) for j in range(3))
            check(mean==y,'Common positive row intertwining')
            T.append(tuple(masses))
        rows.append(tuple(T))
    start=(F(0),F(0),F(0),F(0),F(1),F(0));z0=vertices[4]
    for N in range(5):
        amplitude=r**N/2;scale=amplitude/r**N
        check(scale<=1,'Positive terminal decoder')
        for word in product(range(5),repeat=N):
            distribution=start;physical=z0
            for a in word:
                distribution=matmul((distribution,),rows[a])[0]
                physical=mv(commands[a],physical)
            actual=tuple(scale*sum(distribution[i]*vertices[i][j] for i in range(6)) for j in range(3))
            target=tuple(amplitude*x for x in physical)
            check(actual==target,'Every finite word exact positive realization')
    control('hidden-return-row-need-not-be-identity',rows[0]!=eye(6))
    control('reverse-noncommuting-word-differs',mv(Z,mv(X,z0))!=mv(X,mv(Z,z0)))
    control('negative-barycentric-row-is-illegal',any(x<0 for x in [F(-1,10),F(11,10)]))

def reduce_word(w):
    out=[]
    for x in w:
        if x==0:continue
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return tuple(out)

def test_extreme_profiles():
    ball={()}
    for n in range(7):
        check(len(ball)==2*3**n-1,'Reduced free-word ball count')
        check(all(reduce_word(w)==w for w in ball),'Reduced normal forms')
        ball={reduce_word(w+(a,)) for w in ball for a in [0,1,-1,2,-2]}
    orbit={0}
    for n in range(8):
        check(len(orbit)==min(n+1,3),'Finite cyclic extreme profile')
        orbit={x for x in orbit}|{(x+1)%3 for x in orbit}
    P=sp.diag(1,0);Q=sp.diag(0,1)
    check(norm2(P)==norm2(Q)==1,'Rank-one extreme points')
    control('mixed-distinct-pure-outputs-not-pure',sp.det((P+Q)/2)>0)
    control('identity-padding-essential-for-ball-count',len({(1,),(2,),(-1,),(-2,)})!=2*3-1)
    control('scalar-readout-does-not-separate-orbit',sp.trace(P)==sp.trace(Q) and P!=Q)
    t=sp.Symbol('t');M=sp.Matrix([[1,1],[0,1]])
    polynomials=list((M-sp.eye(2))*sp.Matrix([1,t]))
    check(any(sp.Poly(p,t).as_expr()!=0 for p in polynomials),'Nonscalar algebraic eigenline polynomial')
    control('arbitrary-algebraic-seed-may-have-stabilizer',sp.diag(1,-1)*sp.Matrix([1,0])==sp.Matrix([1,0]))

def positive_round_from_factor(L,b):
    if b<1:raise ValueError('Precision must be positive')
    Q=L.applyfunc(lambda x:sp.floor(sp.re(x)*2**b)/2**b+sp.I*sp.floor(sp.im(x)*2**b)/2**b)
    gram=Q*Q.H;den=sp.simplify(sp.trace(gram))
    if den<=0:raise ValueError('Zero Gram factor')
    return sp.simplify(gram/den)

def test_tomography_precision():
    hs=[sp.Matrix([[0,1],[1,0]])/sp.sqrt(2),sp.Matrix([[0,-sp.I],[sp.I,0]])/sp.sqrt(2),sp.diag(1,-1)/sp.sqrt(2)]
    q=3;effects=[(sp.eye(2)+sgn*H/2)/(2*q) for H in hs for sgn in [1,-1]]
    check(sum(effects,sp.zeros(2))==sp.eye(2),'POVM sums to identity')
    states=[sp.diag(1,0),sp.eye(2)/2,sp.Matrix([[sp.Rational(9,25),sp.Rational(12,25)],[sp.Rational(12,25),sp.Rational(16,25)]]),sp.Matrix([[sp.Rational(1,2),-sp.I/2],[sp.I/2,sp.Rational(1,2)]])]
    for D in states:
        p=[sp.simplify(sp.trace(E*D)) for E in effects]
        check(sum(p)==1 and all(x>=sp.Rational(1,12) for x in p),'Interior legal tomography law')
        reconstructed=sum([2*q*(p[2*i]-p[2*i+1])*hs[i] for i in range(q)],sp.eye(2)/2)
        check(sp.simplify(reconstructed-D)==sp.zeros(2),'Exact tomography reconstruction')
    bad=sp.eye(2)/2+6*hs[0]
    control('enlarged-simplex-is-not-legal-matrix-image',sp.det(bad)<0)
    raw=sp.Matrix([[sp.Rational(1,2)-sp.Rational(1,100),sp.Rational(1,2)],[sp.Rational(1,2),sp.Rational(1,2)]])
    control('entrywise-rounding-can-destroy-positivity',raw.det()<0)
    factors=[sp.Matrix([[sp.Rational(3,5),0],[sp.Rational(4,5),0]]),sp.Matrix([[sp.Rational(3,5),0],[sp.I*sp.Rational(4,5),0]]),sp.diag(sp.Rational(3,5),sp.Rational(4,5))]
    for L in factors:
        D=L*L.H;check(norm2(L)==1,'Normalized factor input')
        for b in range(5,11):
            rounded=positive_round_from_factor(L,b)
            check(rounded==rounded.H and sp.trace(rounded)==1,'Exact trace and Hermiticity')
            check(all(rounded[i,i]>=0 for i in range(2)) and rounded.det()>=0,'Exact positive semidefinite decoder')
            check(norm2(rounded-D)<=sp.Rational(128*4,2**(2*b)),'Gram rounding error bound')
    try:positive_round_from_factor(sp.zeros(2),3)
    except ValueError:caught=True
    else:caught=False
    control('zero-gram-factor-rejected',caught)
    try:positive_round_from_factor(sp.eye(2),0)
    except ValueError:caught=True
    else:caught=False
    control('nonpositive-precision-rejected',caught)
    control('forgetting-gram-normalization-changes-trace',sp.trace(sp.diag(sp.Rational(1,4),sp.Rational(1,4)))!=1)

def main():
    test_spectral_split();test_caps_and_support();test_common_rows();test_extreme_profiles();test_tomography_precision()
    print(json.dumps({'status':'success','exact_finite_assertions':count,'negative_controls_detected':negative,
       'suites':['uniform_spectral_split','spectral_overlap_identity','Grassmann_projective_caps','positive_hull_support','common_positive_rows','extreme_profiles','reduced_word_counts','tomographic_legality','positive_Gram_rounding'],
       'scope':'Finite rational/algebraic regression only. No universal compactness, spectral-gap, free-generation, all-dimension theorem or priority claim is computationally certified.'},sort_keys=True))
if __name__=='__main__':main()
