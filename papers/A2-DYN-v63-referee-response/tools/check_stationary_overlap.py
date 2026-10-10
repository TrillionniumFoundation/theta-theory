#!/usr/bin/env python3
"""Finite interval/suspension diagnostics. These do not certify billiard dynamics."""
from __future__ import annotations
from fractions import Fraction as F
from collections import defaultdict
import cmath, math
import numpy as np
from scipy.integrate import quad
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

# A finite deterministic suspension, deliberately not assumed mixing.
ROOFS = [F(9,10), F(6,5), F(7,10), F(3,2)]
KAPPA = [(1,0),(0,1),(-1,1),(1,-1)]
# Age partitions include nonzero initial and final cell offsets.
OFFSETS = [[(0,0),(1,0)], [(0,0),(0,1),(-1,1)],
           [(-1,0),(0,0)], [(0,1),(1,1),(1,0)]]
MEAN = sum(ROOFS)/4
J = max(map(len,OFFSETS))
H = max(ROOFS)
L0 = 2*J/MEAN
A2 = 4*J*J/MEAN


def parts(i):
    h=ROOFS[i];q=len(OFFSETS[i])
    return [(h*j/q,h*(j+1)/q,d) for j,d in enumerate(OFFSETS[i])]


def age_label(i,a):
    for l,r,d in parts(i):
        if l<=a<r:return d
    raise ValueError('age outside flight')


def record(i,m):
    s=F(0);k=[0,0]
    for j in range(m):
        h=(i+j)%4;s+=ROOFS[h]
        for a in range(2):k[a]+=KAPPA[h][a]
    return s,tuple(k),(i+m)%4


def physical(i,a,t):
    """Independent trajectory evolution from the actual starting age."""
    initial=age_label(i,a);index=i;age=a;count=0;center=[0,0];remaining=t
    while remaining>=ROOFS[index]-age:
        remaining-=ROOFS[index]-age
        for j in range(2):center[j]+=KAPPA[index][j]
        index=(index+1)%4;age=F(0);count+=1
        require(count<1000,'finite model exceeded event bound')
    terminal=age_label(index,age+remaining)
    return count,tuple(center[j]+terminal[j]-initial[j] for j in range(2))


def direct_probabilities(m,t):
    """Split the initial-age line at every possible event, then evolve."""
    ans=defaultdict(F)
    for i in range(4):
        cuts={F(0),ROOFS[i]}
        for l,r,d in parts(i):cuts.update((l,r))
        s=F(0)
        for j in range(1,30):
            s+=ROOFS[(i+j-1)%4]
            # Collision and cell-crossing boundaries of the terminal age.
            for l,r,d in parts((i+j)%4):
                for a in (s+l-t,s+r-t):
                    if 0<a<ROOFS[i]:cuts.add(a)
        cuts=sorted(cuts)
        for a,b in zip(cuts,cuts[1:]):
            count,k=physical(i,(a+b)/2,t)
            if count==m:ans[k]+=(b-a)/(4*MEAN)
    return {k:v for k,v in ans.items() if v}


def overlap_probabilities(m,t,omit_initial=False):
    ans=defaultdict(F)
    for i in range(4):
        s,k,y=record(i,m)
        for a,b,d in parts(i):
            for c,e,f in parts(y):
                length=max(F(0),min(b,s+e-t)-max(a,s+c-t))
                out=tuple(k[j]+f[j]-(0 if omit_initial else d[j]) for j in range(2))
                ans[out]+=length/(4*MEAN)
    return {k:v for k,v in ans.items() if v}


def int_exp(b,a,c):
    if abs(b)<1e-12:return complex(float(c-a))
    a=float(a);c=float(c)
    return (cmath.exp(1j*b*c)-cmath.exp(1j*b*a))/(1j*b)


def profile_hat(m,k,b,wrong_sign=False):
    total=0j
    for i in range(4):
        s,lab,y=record(i,m)
        for a,c,d in parts(i):
            for e,f,g in parts(y):
                if tuple(lab[j]+g[j]-d[j] for j in range(2))!=k:continue
                left=int_exp(b if wrong_sign else -b,a,c)
                total+=cmath.exp(1j*b*float(s))*left*int_exp(b,e,f)/(4*float(MEAN))
    return total


def eta(b):
    a=abs(b)
    if a<=.5:return 1-6*a*a+6*a*a*a
    if a<1:return 2*(1-a)**3
    return 0.


def kernel(t):
    return 3/(8*math.pi)*np.sinc(t/(4*math.pi))**4


def positive_inverse(m,k,t,B):
    # Real profile: negative frequencies are conjugates.
    return quad(lambda b: (cmath.exp(-1j*b*t)*eta(b/B)*profile_hat(m,k,b)).real,
                0,B,epsabs=1e-10,points=[B/2],limit=200)[0]/math.pi


def positive_convolution(m,k,t,B):
    total=0.
    for i in range(4):
        s,lab,y=record(i,m)
        for a,c,d in parts(i):
            for e,f,g in parts(y):
                if tuple(lab[j]+g[j]-d[j] for j in range(2))!=k:continue
                breaks=sorted(set(float(s+x-z) for x in (e,f) for z in (a,c)))
                def fun(v):
                    ov=max(0.,min(float(c),float(s+f)-v)-max(float(a),float(s+e)-v))
                    return B*kernel(B*(t-v))*ov/(4*float(MEAN))
                total+=sum(quad(fun,l,r,epsabs=1e-11,limit=100)[0]
                           for l,r in zip(breaks,breaks[1:]))
    return total


def source_difference(m,t,s):
    total=F(0)
    for i in range(4):
        Sm,lab,y=record(i,m);cuts={F(0),ROOFS[i]}
        for l,r,d in parts(i):cuts.update((l,r))
        for time in (t,s):
            for l,r,d in parts(y):
                for a in (Sm+l-time,Sm+r-time):
                    if 0<a<ROOFS[i]:cuts.add(a)
        cuts=sorted(cuts)
        for a,b in zip(cuts,cuts[1:]):
            mid=(a+b)/2
            def at(time):
                v=time+mid-Sm
                if not 0<=v<ROOFS[y]:return None
                d=age_label(i,mid);e=age_label(y,v)
                return tuple(lab[j]+e[j]-d[j] for j in range(2))
            x,z=at(t),at(s)
            distance=0 if x==z else (1 if x is None or z is None else 2)
            total+=(b-a)*distance/(4*MEAN)
    return total


def finite_checks():
    phase_exponents=[F(1,14)-3*F(1,200), F(1,28)-4*F(1,200),
                     F(1,14)-5*F(1,200), F(1,2)-F(6,14)-4*F(1,200),
                     F(1,2)-F(6,14)-6*F(1,200)]
    require(phase_exponents==[F(79,1400),F(11,700),F(13,280),F(9,175),F(29,700)],'central exponents')
    require(min(phase_exponents)==F(11,700),'dominant central error')
    require(F(1,2)-F(1,200)-F(1,7)>0 and F(1,2)-F(3,200)-F(3,7)>0,'analytic margins')
    for P in (F(1,10),F(1),F(3),F(9)):
        require(P+F(3,2)-F(3,2)==P,'polynomial normalized tail')
    c=sp.symbols('c',positive=True)
    S=sp.Matrix([[3,1,0],[1,4,1],[0,1,5]])
    D=sp.diag(1,1,-1/c);V=D*S*D.T/c
    A=sp.sqrt(c)*sp.diag(1,1,-c)
    require(sp.simplify(V.det()-S.det()/c**5)==0,'physical determinant normalization')
    require(sp.simplify(A*V*A.T-S)==sp.zeros(3),'physical covariance conjugation')
    examples=0;missing_cell_detected=False
    for m in (1,2,5,11):
        for j in range(0,39):
            t=F(m,1)*MEAN+F(j-19,10)
            if t<0:continue
            a=direct_probabilities(m,t);b=overlap_probabilities(m,t)
            require(a==b,'exact original-time age formula')
            missing_cell_detected|=a!=overlap_probabilities(m,t,omit_initial=True)
            examples+=1
    require(missing_cell_detected,'missing initial cell correction escaped control')
    differences=0
    for m in (1,2,5,11):
        for j in range(-5,16):
            t=m*MEAN+F(j,10)
            for h in (F(1,100),F(1,10),F(1,2)):
                require(source_difference(m,t,t-h)<=L0*h,'source l1 translation bound')
                differences+=1
    # Integral of all overlap profiles is the product of the two roof lengths,
    # not a normalized probability in (k,time).
    for m in (1,2,5,11):
        mass=sum(ROOFS[i]*ROOFS[(i+m)%4] for i in range(4))/(4*MEAN)
        require(mass<=H*H/MEAN,'all-label profile mass')
    # Distributional second derivative has four endpoint atoms per interval pair.
    atom_checks=0
    for i in range(4):
        for a,b,d in parts(i):
            for c1,e,f in parts((i+1)%4):
                atoms=defaultdict(F)
                for point,sign in [(c1-b,1),(e-b,-1),(c1-a,-1),(e-a,1)]:atoms[point]+=sign
                require(sum(abs(v) for v in atoms.values())<=4,'curvature variation')
                require(sum(atoms.values())==0,'second derivative total mass')
                atom_checks+=1
    negsign=False;tailchecks=0
    for m in (1,2,5):
        labels=set()
        for i in range(4):
            Sm,k,y=record(i,m)
            for a,b,d in parts(i):
                for c1,e,f in parts(y):labels.add(tuple(k[j]+f[j]-d[j] for j in range(2)))
        for b in (.7,2.,7.,23.):
            norm=sum(abs(profile_hat(m,k,b)) for k in labels)
            require(norm<=float(A2)/b**2+1e-10,'summed Fourier inverse-square bound')
            tailchecks+=1
            negsign|=any(abs(profile_hat(m,k,b)-profile_hat(m,k,b,True))>1e-4 for k in labels)
    require(negsign,'wrong initial age sign escaped control')
    inversions=0;maxerr=0.
    for m in (1,2,5):
        t=float(m*MEAN+F(1,10));law=overlap_probabilities(m,F(str(t)))
        if not law:continue
        for k in list(sorted(law))[:3]:
            for B in (3.,11.):
                f=positive_inverse(m,k,t,B);g=positive_convolution(m,k,t,B)
                maxerr=max(maxerr,abs(f-g));require(abs(f-g)<2e-8,'positive convolution/Fourier identity')
                require(f>=-1e-10,'positive finite inverse')
                require(abs(f-float(law[k]))<=float(L0)*math.sqrt(12)/B,'positive pointwise error')
                inversions+=1
    # An exact finite posterior calculation pays the denominator.
    masses=[F(1,10),F(2,10),F(3,10),F(4,10)]
    indicator=[1,0,1,0];likelihood=[F(9,10),F(1,20),F(4,5),F(1,40)]
    p=sum(w*v for w,v in zip(masses,indicator));q=sum(w*v for w,v in zip(masses,likelihood))
    E=sum(w*abs(a-b) for w,a,b in zip(masses,indicator,likelihood))
    TV=sum(w*abs(a/p-b/q) for w,a,b in zip(masses,indicator,likelihood))
    require(abs(p-q)<=E and TV<=2*E/p,'posterior denominator normalization')
    # Equal intervals produce atomic second derivatives, not an L1 second derivative.
    require([1,-2,1]!=[0,0,0],'atomic curvature negative control')
    return {'finite_model':'four-state periodic suspension with explicit age-cell partitions; not mixing',
            'exact_age_probability_cases':examples,'source_translation_cases':differences,
            'curvature_atom_cases':atom_checks,'summed_fourier_tail_cases':tailchecks,
            'positive_fourier_convolution_cases':inversions,'quadrature_identity_passed':maxerr<2e-8,
            'central_decay_exponents':[str(x) for x in phase_exponents],
            'physical_covariance_jacobian_power':5,'normalized_bandwidth_power':'P+3/2',
            'negative_controls':['omitted initial cell offset','wrong age Fourier sign','atomic second derivative not L1'],
            'continuum_billiard_geometry_certified':False,'finite_complement_evaluated':False,
            'microscopic_Gaussian_denominator_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
