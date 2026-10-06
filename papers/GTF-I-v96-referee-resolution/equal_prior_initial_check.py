#!/usr/bin/env python3
"""Exact algebra fixtures and separately labeled numerical sanity checks."""
from fractions import Fraction
import json
import numpy as np
import sympy as sp
from equal_prior_initial import certificate, sqrt_interval

exact = numeric = negative = 0

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

# Symbolic certificate: rationalize by h^2 = c_d(v)/(d^2-1).
d,h=sp.symbols('d h',positive=True)
e=d-1
v=((d*d-1)*h*h-d*(d-2))/(2*d-1)
z2=1-v
C=d*(d-2)+(2*d-1)*v
T=e+(2*d-1)*v/(e+d*h)
require(sp.factor(T*T-(1+(d*d-1)*v)-z2*(e*T-1)**2/C)==0,
        'constant coefficient in universal square certificate')
require(sp.factor(e*e*z2-(1-d*d*v)-C)==0,'quadratic coefficient')
require(sp.factor(e*T-1-(d*(d-2)+e*(2*d-1)*v/(e+d*h)))==0,
        'feasible fresh optimizer coefficient')
exact+=3
# The scalar concavity derivatives are checked as rational identities.
a,b,c,y=sp.symbols('a b c y',positive=True)
Hp=(a+b*(y+c/y)/2)/(a+b*y)**2
Dtarget=-b*(3*a+a*c/y**2+b*y+3*b*c/y)/(2*(a+b*y)**3)
require(sp.factor(sp.diff(Hp,y)-Dtarget)==0,'scalar derivative identity')
exact+=1
for dd in range(2,11):
    for j in range(1,16):
        x=Fraction(15+j,30)
        spectrum=[str(x),str(1-x)]+['0']*(dd-2)
        out=certificate(spectrum,'3/5',45,2)
        lo,hi=Fraction(out['sqrt_lower']),Fraction(out['sqrt_upper'])
        rad=Fraction(out['radicand'])
        require(lo*lo<=rad<=hi*hi,'rational square-root bracket')
        p,q=Fraction(out['score_lower']),Fraction(out['score_upper'])
        require(p<=q and q-p<=Fraction(1,2**40),'rational score width')
        require(certificate(spectrum,'0',20,2)['score_lower']=='1/2','zero signal')
        exact+=3
    eq=certificate([str(Fraction(1,dd))]*dd,'1',35,dd)
    require(Fraction(eq['score_lower'])<=Fraction(1,2)+Fraction(2*dd-1,4*dd*(dd+1))
            <=Fraction(eq['score_upper']),'global rank-two benchmark')
    pure=certificate(['1']+['0']*(dd-1),'1',35,2)
    require(Fraction(pure['score_lower'])==Fraction(1,2)+Fraction(dd-1,2*dd*(dd+1)),
            'rank-one endpoint')
    exact+=2
# Exactly normalized attaining instrument for a three-dimensional initial Gram.
V1=sp.Matrix([[1/sp.sqrt(2),0,0],[0,1,0]])
V2=sp.Matrix([[1/sp.sqrt(2),0,0],[0,0,1]])
rho=sp.diag(sp.Rational(3,4),sp.Rational(1,8),sp.Rational(1,8))
C0=sp.diag(*[sp.sqrt(rho[i,i]) for i in range(3)])
require(V1.H*V1+V2.H*V2==sp.eye(3),'instrument completeness')
require((V1*C0).H*(V1*C0)+(V2*C0).H*(V2*C0)==rho,'fixed Gram not replaced')
exact+=2

def swap(dd):
    out=np.zeros((dd*dd,dd*dd),complex)
    for i in range(dd):
        for j in range(dd): out[i*dd+j,j*dd+i]=1
    return out

def sqrtm(A):
    val,U=np.linalg.eigh((A+A.conj().T)/2)
    return (U*np.sqrt(np.maximum(val,0)))@U.conj().T

def normleaf(A,B,dd):
    L=np.kron(sqrtm(A),sqrtm(B))
    Q=L@(np.eye(dd*dd)-dd*swap(dd))@L
    return float(np.abs(np.linalg.eigvalsh((Q+Q.conj().T)/2)).sum())

def psi(dd,vv):
    return dd-1+(2*dd-1)*vv/(2*(dd-1+dd*np.sqrt((dd*(dd-2)+(2*dd-1)*vv)/(dd*dd-1))))

def weights(dd,x):
    vv=4*x*(1-x)
    if vv<1e-16: return np.array([1.,0.])
    tt=2*psi(dd,vv)-(dd-1)
    ww=(2*x-1)*((dd-1)*tt-1)/(dd*(dd-2)+(2*dd-1)*vv)
    return np.array([(1+ww)/2,(1-ww)/2])

rng=np.random.default_rng(95062026)
for dd in range(2,8):
    for x in [.5,.55,.625,.75,.875,.95,.999,1.]:
        A=np.diag([x,1-x]+[0.]*(dd-2)).astype(complex)
        beta=weights(dd,x);Bopt=np.diag([*beta,*([0.]*(dd-2))])
        target=psi(dd,4*x*(1-x))
        require(abs(normleaf(A,Bopt,dd)-target)<2e-9,'analytic fresh Gram attainment')
        numeric+=1
        for _ in range(4):
            G=rng.normal(size=(dd,dd))+1j*rng.normal(size=(dd,dd))
            B=G@G.conj().T;B/=np.trace(B)
            val=normleaf(A,B,dd);pinch=normleaf(A,np.diag(B.diagonal()),dd)
            require(val<=pinch+2e-9 and pinch<=target+2e-9,'noncommuting pinching upper')
            numeric+=1
    for _ in range(25):
        x,y,w=rng.random(3)
        require(psi(dd,4*(w*x+(1-w)*y)*(1-w*x-(1-w)*y))
                >=w*psi(dd,4*x*(1-x))+(1-w)*psi(dd,4*y*(1-y))-1e-10,
                'concavity sanity check')
        numeric+=1
# Direct Born calculation on the seven concrete Pauli devices.
I=np.eye(2,dtype=complex)
paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.])]
S=swap(2)
for x in [.5,.625,.75,.9,1.]:
    C=np.diag(np.sqrt([x,1-x]));D=np.diag(np.sqrt(weights(2,x)))
    X=np.kron(C,D)@(np.eye(4)-2*S)@np.kron(C,D)
    eig,U=np.linalg.eigh(X)
    Fp=(U*(eig>1e-10))@U.conj().T
    Fm=(U*(eig< -1e-10))@U.conj().T
    def event(E):
        total=0.
        for y in range(2):
            for z in range(2):
                block=np.kron(C@E[y].T@C.conj().T,D@E[z].T@D.conj().T)
                total+=np.trace((Fp if y==z else Fm)@block).real
        return total
    for t in [0.,.25,.5,1.]:
        baseline=event([I/2,I/2])
        alt=sum(event([(I+t*sgn*P)/2,(I-t*sgn*P)/2])
                for P in paulis for sgn in [-1,1])/6
        score=.5+.5*(baseline-alt)
        require(abs(score-(.5+t*t*psi(2,4*x*(1-x))/12))<1e-10,'Pauli Born score')
        numeric+=1
    # Independent redraw has exactly the scalar tensor moment.
    mean=[sum(((I+sgn*P)/2 if y==0 else (I-sgn*P)/2)
              for P in paulis for sgn in [-1,1])/6 for y in range(2)]
    require(all(np.allclose(E,I/2) for E in mean),'independent redraw moment')
    negative+=1
# False heuristics and invalid inputs must not pass.
A=np.diag([.75,.25])
require(normleaf(A,I/2,2)<psi(2,.75)-1e-3,'uniform fresh heuristic is strictly suboptimal')
require(normleaf(A,A,2)<psi(2,.75)-1e-3,'matching initial spectrum is strictly suboptimal')
negative+=2
bad=[(['1/2','1/3'],'1',20,2),(['-1','2'],'1',20,2),(['1'],'1',20,2),
     ([.5,.5],'1',20,2),(['1/2','1/2'],'2',20,2),(['1/2','1/2'],'1',0,2),
     (['1/2','1/2'],'1',20,1),(['1/2','1/2'],'1',20,3),
     ([True,'0'],'1',20,2),('10','1',20,2),({'1':0,'0':1},'1',20,2)]
for args in bad:
    try: certificate(*args)
    except (ValueError,TypeError,ZeroDivisionError): negative+=1
    else: raise RuntimeError('invalid input was accepted')
print(json.dumps({'schema':'gtf95.equal-prior-initial-check/1','status':'success',
    'symbolic_and_exact_checks':exact,'numerical_sanity_checks':numeric,
    'negative_controls':negative,'physical_execution':False,
    'continuum_proof_by_replay':False,'independent_priority_clearance':False},sort_keys=True))
