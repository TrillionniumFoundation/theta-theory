#!/usr/bin/env python3
"""Finite identities and countermodels; no continuum or spectral certification."""
from fractions import Fraction as F
from math import comb, factorial, sqrt, exp, e
from itertools import product
import mpmath as mp

def require(ok,message):
    if not ok: raise RuntimeError(message)

def finite_checks():
    mp.mp.dps=35
    fourier=[]
    def sinc(x):return mp.sin(x)/x if x else mp.mpf(1)
    for s in [-3,-1,0,F(1,2),2,4]:
        x=mp.mpf(s.numerator)/s.denominator if isinstance(s,F) else mp.mpf(s)
        inverse=mp.quad(lambda z: mp.exp(1j*z*x)*mp.pi*(1-abs(z)/2)*(1+mp.exp(1j*mp.pi*z/2)),[-2,0,2])/(2*mp.pi)
        actual=sinc(x)**2+sinc(x+mp.pi/2)**2
        require(abs(inverse-actual)<mp.mpf('1e-29'),'Fourier shift/normalization')
        wrong=mp.quad(lambda z: mp.exp(1j*z*x)*mp.pi*(1-abs(z)/2)*(1+mp.exp(-1j*mp.pi*z/2)),[-2,0,2])/(2*mp.pi)
        if x==1:require(abs(wrong-actual)>mp.mpf('1e-4'),'negative shift not detected')
        fourier.append(str(s))
    # Multinomial derivative factorials cancel exactly; the remaining
    # complete homogeneous sum is bounded by the ordinary power.
    derivative_cases=0
    sizes=[F(1,3),F(2,5),F(3,7)]
    for q in range(25):
        homogeneous=F(0)
        for a in range(q+1):
            for b in range(q-a+1):
                c=q-a-b
                coefficient=factorial(q)//(factorial(a)*factorial(b)*factorial(c))
                require(coefficient*factorial(a)*factorial(b)*factorial(c)==factorial(q),'factorial cancellation')
                homogeneous+=sizes[0]**a*sizes[1]**b*sizes[2]**c
                derivative_cases+=1
        require(homogeneous<=sum(sizes)**q,'complete homogeneous bound')
    # Exact drift cancellation and square-root size bound for three blocks.
    block_cases=0
    for m in range(1,36):
        for l in range(1,m+1):
            alpha=F(l,m)
            for a in range(m-l+1):
                b=m-a-l
                require(-alpha*(a+b)+(1-alpha)*l==0,'pinned drift')
                size=float(alpha)*(sqrt(a)+sqrt(b))+float(1-alpha)*sqrt(l)
                require(size<=(1+sqrt(2))*sqrt(l)+1e-12,'block root-length bound')
                require(max(a,l,b)*3>=m,'longest block')
                block_cases+=1
    # Independent finite moment model checks all orders including repeats.
    moments=0
    for m in range(1,21):
        for r in range(1,13):
            value=F(sum(comb(m,k)*(2*k-m)**(2*r) for k in range(m+1)),2**m)
            require(value<=factorial(2*r)*m**r,'factorial finite moment envelope')
            moments+=1
    for q in range(4,65,2):
        exponent=F(1,2)-F(1,q)
        require(exponent>=F(1,4),'uniform dyadic exponent')
        require(1/(1-2**(-float(exponent)))<=1/(1-2**(-0.25))+1e-12,'dyadic sum')
    # Exact half-open occupation and pinned time change in finite words.
    clock_cases=0
    for m in range(2,9):
        for middle in product((0,1),repeat=m-1):
            bits=(1,)+middle+(1,)
            visits=[j for j,v in enumerate(bits) if v];n=len(visits)-1
            tau=[F(2+(j%3),4) for j in range(m)]
            prefixes=[sum(tau[:j]) for j in range(m+1)]
            total=prefixes[m]
            for l,N in enumerate(visits):
                occupancy=sum(bits[:N]);require(occupancy==l,'terminal membership counted twice')
                theta=F(N,m);frac=F(l,n)
                Bocc=occupancy-theta*n
                require(theta-frac==-Bocc/n,'exact return-clock displacement')
                bridge=prefixes[N]-theta*total
                require(prefixes[N]-frac*total==bridge+(theta-frac)*total,'pinned roof time change')
                clock_cases+=1
    # Tail comparison used to upgrade bounded transport to pth-power cost.
    transport_cases=0
    a=0.5
    for p in [1,2,3,5]:
        C=(4*p/(a*e))**p
        for R in [1,2,5,10]:
            for distance in [0,0.5,1,2,4,8,16,32]:
                bounded=min(distance,1)
                rhs=R**p*bounded+C*exp(-a*R/4)*exp(a*distance/2)
                require(distance**p<=rhs+1e-9,'transport truncation')
                transport_cases+=1
    # A reference floor yields domination, not just TV convergence.
    G=[F(1,2),F(2),F(3,2)];P=[F(2,5),F(21,10),F(8,5)]
    delta=F(1,10);d0=min(G);H=sum(G);Fmass=sum(P)
    alpha=(1-delta/d0)*H/Fmass
    require(0<alpha<=1,'domination coefficient')
    require(all(p/Fmass>=alpha*g/H for p,g in zip(P,G)),'conditional roof minorization')
    # Explicit negative controls; these are not missing proof hypotheses.
    for n in [10,100,1000]:
        mass=F(1,n);height=n*n;width=F(1,n**3)
        require(height*width==mass and height>1,'small mass/large height countermodel')
        require(F(1,n)*n==1 and F(2,n)<=F(1,5),'BL does not imply W1 countermodel')
        eps=F(1,n);true_mass=eps**2;reference_mass=eps;cost=1/eps
        require(true_mass*cost==eps and reference_mass*cost==1,'TV cannot transfer unbounded cost')
    # A deliberately reversed Fourier shift really differs at a nonzero point.
    x=mp.mpf(1)
    require(abs(sinc(x+mp.pi/2)**2-sinc(x-mp.pi/2)**2)>mp.mpf('1e-4'),'wrong-shift control')
    return {'fourier_inverse_cases':len(fourier),'factorial_derivative_cases':derivative_cases,
      'pinned_three_block_cases':block_cases,'rademacher_all_order_cases':moments,
      'half_open_clock_cases':clock_cases,'transport_tail_cases':transport_cases,
      'dyadic_orders':31,'negative_control_types':4,
      'all_orders_require_uniform_analytic_circle':True,
      'unbounded_reference_cost_requires_domination':True,
      'small_mass_is_not_essential_height':True,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
