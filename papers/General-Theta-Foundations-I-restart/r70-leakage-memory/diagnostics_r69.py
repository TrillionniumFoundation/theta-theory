#!/usr/bin/env python3
"""Finite exact and floating diagnostics for R69; not continuum proof or review.
No assertions are used, so optimization must not remove a check.
"""
from __future__ import annotations
import json, math
from fractions import Fraction as F
import numpy as np
import scipy
import sympy as sp
COUNTS: dict[str,int] = {}
DETAILS: dict[str,object] = {}

def check(ok, group: str, detail) -> None:
    if not bool(ok):
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] = COUNTS.get(group, 0) + 1

def zero(matrix) -> bool:
    return all(sp.simplify(sp.expand(x)) == 0 for x in matrix)

def cycle(n: int):
    C = sp.zeros(n)
    for i in range(n): C[i,(i+1)%n] = 1
    return C

def exact_spectral():
    # Nonsymmetric, noncirculant chain: the largest eigenvector coordinate is NOT first.
    Q = sp.Matrix([[sp.Rational(1,2),sp.Rational(1,2),0],
                   [0,sp.Rational(1,3),sp.Rational(2,3)],
                   [sp.Rational(3,4),0,sp.Rational(1,4)]])
    z=(1+sp.I*sp.sqrt(167))/24
    v=sp.Matrix([(-5+sp.I*sp.sqrt(167))/18,(-14-2*sp.I*sp.sqrt(167))/27,1])
    check(zero(Q*v-z*v), 'exact_noncircular_eigenvector', 'raw eigen equation')
    check([sp.simplify(x*sp.conjugate(x)) for x in v] == [sp.Rational(16,27),sp.Rational(32,27),1],
          'exact_max_coordinate', 'normalizing the first coordinate would be unsafe')
    perm=[1,0,2];v=v/v[1];Q=Q.extract(perm,perm);v=v.extract(perm,[0])
    a=sp.re(v);c=sp.im(v)
    check(v[0]==1 and all(sp.simplify(x*sp.conjugate(x))<=1 for x in v),
          'exact_max_coordinate', 'pure initial anchor with same three labels')
    check(zero(Q*a-sp.re(z)*a+sp.im(z)*c) and zero(Q*c-sp.im(z)*a-sp.re(z)*c),
          'exact_bilinear_certificate', 'both real equations')
    for gamma in [sp.Rational(1),sp.Rational(1,3)]:
        for phase in [sp.Integer(1),sp.I,(3+4*sp.I)/5]:
            d=sp.Matrix([(1+gamma*sp.re(phase*x))/2 for x in v])
            check(all(sp.simplify(x)>=0 and sp.simplify(1-x)>=0 for x in d),
                  'exact_legal_decoder', (str(gamma),str(phase)))
            check(zero(d-sp.ones(3,1)/2-gamma*(sp.re(phase)*a-sp.im(phase)*c)/2),
                  'exact_decoder_intertwining', str(phase))
            row=sp.Matrix([[1,0,0]])
            for n in range(9):
                target=(1+gamma*sp.re(sp.expand(phase*z**n)))/2
                check(sp.simplify((row*d)[0]-target)==0,'exact_spectral_coefficients',(str(gamma),str(phase),n))
                row=row*Q
    # Real, zero, and unit-circle degeneracies are not three-mode instances.
    for lam in [sp.Rational(-1),sp.Rational(-2,3),sp.Rational(0),sp.Rational(1,2),sp.Rational(1)]:
        Q=sp.Matrix([[1+lam,1-lam],[1-lam,1+lam]])/2
        for contrast in [sp.Rational(-1),sp.Rational(0),sp.Rational(2,3)]:
            d=sp.Matrix([1+contrast,1-contrast])/2
            row=sp.Matrix([[1,0]])
            for n in range(7):
                check((row*d)[0]==(1+contrast*lam**n)/2,'exact_scalar_degenerate',(str(lam),str(contrast),n))
                row=row*Q
    for n in range(3,10):
        Q=sp.eye(n)*sp.Rational(2,3)+cycle(n)/3
        row=sp.zeros(1,n);row[0]=1
        W=sp.Matrix.vstack(*[row*Q**k for k in range(n)])
        check(W.det()!=0,'exact_boundary_decoder_uniqueness',n)
        check(Q*sp.ones(n,1)==sp.ones(n,1),'exact_lazy_cycle_rows',n)


def exact_thresholds_and_obstructions():
    thresholds={j:5/(3+4*sp.tan(sp.pi/j)) for j in [3,4,5,6]}
    check(sp.simplify(thresholds[4]-sp.Rational(5,7))==0,'exact_four_label_endpoint','5/7')
    for j in [3,4,6]:
        alpha=thresholds[j];beta=2*sp.pi/j
        b=sp.simplify(alpha*sp.Rational(4,5)/sp.sin(beta))
        a=sp.simplify(alpha*sp.Rational(3,5)-b*sp.cos(beta))
        check(sp.simplify(a+b-1)==0 and a>=0 and b>0,'exact_sector_endpoint',(j,str(alpha)))
        Q=a*sp.eye(j)+b*cycle(j)
        V=sp.Matrix([[1,sp.cos(2*sp.pi*k/j),sp.sin(2*sp.pi*k/j)] for k in range(j)])
        T=sp.Matrix([[1,0,0],[0,alpha*sp.Rational(3,5),alpha*sp.Rational(4,5)],
                      [0,-alpha*sp.Rational(4,5),alpha*sp.Rational(3,5)]])
        check(zero(Q*V-V*T),'exact_sector_all_time_intertwining',j)
        for phase in [(sp.Integer(1),sp.Integer(0)),(sp.Rational(3,5),sp.Rational(4,5))]:
            d=V*sp.Matrix([sp.Rational(1,2),phase[0]/2,-phase[1]/2])
            check(all(sp.simplify(x)>=0 and sp.simplify(1-x)>=0 for x in d),
                  'exact_sector_decoder',j)
        if j>3:
            check(sp.simplify(alpha*(sp.Rational(3,5)+sp.Rational(4,5)*sp.tan(sp.pi/(j-1)))-1)>0,
                  'exact_smaller_size_exclusion',j)
    A,B=1,0
    for k in range(1,101):
        A,B=3*A-4*B,4*A+3*B
        gap=(A-5**k)**2+B*B
        check(A*A+B*B==25**k,'exact_gaussian_norm',k)
        check(gap>=1,'exact_gaussian_nonzero_gap',k)
    for M in range(3,51):
        new=F(3,16*M*M*25**M)
        old=F(1,49*M*(25*M)**M)
        check(new>old,'exact_improved_algebraic_exclusion',M)
    x=(3-sp.sqrt(5))/2;xp=(3+sp.sqrt(5))/2
    check(sp.simplify(x*x-3*x+1)==0 and sp.simplify(x+xp)==3,
          'exact_quadratic_phase_certificate','integer polynomial and conjugate')
    check(sp.sqrt(5)+sp.Rational(1,2)<3,'exact_quadratic_conjugate_bound','global c=1/3 proof')
    DETAILS['algebraic_first_sector_endpoints']={str(j):str(v) for j,v in thresholds.items()}


def raw_squared_embedding():
    I=sp.eye(2);A=sp.diag(1,0);E=sp.diag(1,0);epsilon=sp.Rational(1,4);R=sp.Rational(3,2)
    target=sp.Matrix([[sp.Rational(4,5),sp.Rational(1,5)],[sp.Rational(1,5),sp.Rational(1,5)]])
    check(target.det()>0 and sp.trace(target)==1,'exact_squared_preparation','physical mixed target')
    for alive in [sp.Rational(0),sp.Rational(2,5),sp.Rational(1)]:
        state=sp.kronecker_product(sp.diag(alive,1-alive),target)
        for sign in [-1,1]:
            V=sp.eye(4)-sign*epsilon*sp.kronecker_product(A,2*E-I)
            mean=-sign*epsilon*sp.kronecker_product(A,I)/2
            plus=(V+R*mean)/(2*R*R);minus=(V-R*mean)/(2*R*R);center=sp.eye(4)-V/(R*R)
            check(zero(plus+minus+center-sp.eye(4)) and all(e>=0 for mat in [plus,minus,center] for e in mat.eigenvals()),
                  'exact_squared_audit_povm',(str(alive),sign))
            for choice in [-1,1]:
                loss=(choice-R)**2*plus+choice**2*center+(choice+R)**2*minus
                expected=2*sp.eye(4)+sign*epsilon*sp.kronecker_product(A,choice*I-(2*E-I))
                check(zero(loss-expected),'exact_squared_loss_observable',(sign,choice))
            born=sp.trace(E*target)
            average=born*sp.trace((2*sp.eye(4)+sign*epsilon*sp.kronecker_product(A,I-(2*E-I)))*state)
            average+=(1-born)*sp.trace((2*sp.eye(4)+sign*epsilon*sp.kronecker_product(A,-I-(2*E-I)))*state)
            check(sp.simplify(average-2)==0,'exact_squared_calibrated_risk',(str(alive),sign))


def exact_spectral_mixture():
    # Two distinct complex phase pairs; all output coefficients below are rational.
    alpha=sp.Rational(1,3)
    Qs=[alpha*cycle(3)+(1-alpha)*sp.ones(3)/3,
        alpha*cycle(4)+(1-alpha)*sp.ones(4)/4]
    ds=[sp.Matrix([1,sp.Rational(1,4),sp.Rational(1,4)]),
        sp.Matrix([1,sp.Rational(1,2),0,sp.Rational(1,2)])]
    for w1,w2 in [(sp.Rational(1,3),sp.Rational(1,2)),(sp.Rational(1,4),sp.Rational(3,4))]:
        w0=1-w1-w2;dim=8+int(bool(w0>0));Q=sp.zeros(dim);d=sp.zeros(dim,1);d[0]=(1+w1+w2)/2
        offset=1
        for weight,block,decoder in zip([w1,w2],Qs,ds):
            size=block.rows;Q[offset:offset+size,offset:offset+size]=block
            Q[0,offset:offset+size]=weight*block[0,:];d[offset:offset+size,0]=decoder
            offset+=size
        if w0>0:Q[0,offset]=w0;Q[offset,offset]=1;d[offset]=sp.Rational(1,2)
        check(Q*sp.ones(dim,1)==sp.ones(dim,1) and all(x>=0 for x in Q),'exact_mixture_counted_anchor',(str(w1),str(w2),dim))
        values=[];row=sp.zeros(1,dim);row[0]=1
        for n in range(15):
            target=(1+alpha**n*(w1*sp.cos(2*sp.pi*n/3)+w2*sp.cos(sp.pi*n/2)))/2
            value=(row*d)[0]
            check(sp.simplify(value-target)==0,'exact_mixture_response',(str(w1),str(w2),n))
            values.append(value);row=row*Q
        H=sp.Matrix([[values[i+j] for j in range(5)] for i in range(5)])
        check(H.det()!=0,'exact_mixture_hankel_lower','five independent modes')


def numeric_circulant(q:int,alpha:float,theta:float):
    beta=2*math.pi/q;wrapped=theta%(2*math.pi);j=int(math.floor(wrapped/beta))
    psi=wrapped-j*beta
    aa=alpha*math.sin(beta-psi)/math.sin(beta)
    bb=alpha*math.sin(psi)/math.sin(beta);cc=1-aa-bb
    check(min(aa,bb,cc)>-2e-12,'float_circulant_nonnegative',(q,alpha,theta,aa,bb,cc))
    shifts=np.array([j%q,(j+1)%q]);weights=np.array([aa,bb])
    roots=np.exp(2j*np.pi*np.arange(q)/q)
    ev=aa*roots[j%q]+bb*roots[(j+1)%q]
    check(abs(ev-alpha*np.exp(1j*theta))<2e-12,'float_circulant_eigenvalue',(q,alpha))
    return shifts,weights,max(cc,0.)


def floating():
    rng=np.random.default_rng(69016);largest=0.;phase_rows=[]
    for K in range(4,61):
        lo=math.cos(math.pi/(K-1));hi=math.cos(math.pi/K);alpha=(lo+hi)/2
        theta=math.pi/(K-1);predicted=max(3,math.ceil(math.pi/math.acos(alpha)))
        check(predicted==K and alpha>lo and alpha<=hi,'float_worst_phase_bracket',K)
        check(alpha*(math.cos(theta)+math.sin(theta)*math.tan(math.pi/(K-1)))>1,
              'float_worst_phase_lower',K)
        numeric_circulant(K,alpha,theta)
    angle=math.atan2(4,3)
    for M in [3,4,5,6]:
        limit=1/(math.cos(angle)+math.sin(angle)*math.tan(math.pi/M))
        for alpha in [limit/3,limit*.8,limit]:
            shifts,weights,cc=numeric_circulant(M,alpha,angle)
            for gamma,phi in [(1.,0.),(.17,1.3),(.75,-.7)]:
                row=np.zeros(M);row[0]=1
                d=(1+gamma*np.cos(phi+2*np.pi*np.arange(M)/M))/2
                bloch=np.array([gamma*math.sin(phi),gamma*math.cos(phi)])
                R=np.array([[.6,.8],[-.8,.6]])
                for n in range(40):
                    target=(1+bloch[1])/2
                    err=abs(row@d-target);largest=max(largest,err)
                    check(err<4e-12,'float_raw_qubit_response',(M,alpha,gamma,phi,n))
                    row=weights[0]*np.roll(row,int(shifts[0]))+weights[1]*np.roll(row,int(shifts[1]))+cc*row.sum()/M
                    bloch=alpha*(R@bloch)
    for M in [3,4,6,9]:
        for trial in range(7):
            Q=rng.dirichlet(np.ones(M),size=M)
            if trial==0: Q[0,:]=0;Q[0,0]=1
            for z in np.linalg.eigvals(Q):
                for k in [1,2,3,7,15]:
                    w=z**k
                    check(w.real+abs(w.imag)*math.tan(math.pi/M)<=1+1e-12,
                          'float_power_sector',(M,trial,k))
    x=(3-math.sqrt(5))/2;theta=2*math.pi*x;c=1/3
    for eps in [1e-2,1e-3,1e-4,1e-5,1e-6]:
        Q=max(4,math.ceil(3/c),math.ceil((4*math.pi**2/(c*c*eps))**(1/3)))
        distances=[abs(q*x-round(q*x)) for q in range(1,Q+1)]
        q=min(range(1,Q+1),key=lambda k:distances[k-1])
        delta=2*math.pi*distances[q-1]/q
        radial=math.cos(math.pi/q)/math.cos(math.pi/q-delta)
        check(distances[q-1]<=1/Q+1e-12 and q>=c*Q-1e-10,'float_dirichlet_certificate',(eps,q,Q))
        check(1-radial<=eps+2e-12,'float_arithmetic_polygon_budget',(eps,q))
        shifts,weights,cc=numeric_circulant(q,1-eps,theta)
        roots=np.exp(2j*np.pi*np.arange(q)/q)
        row=np.zeros(q);row[0]=1;d=(1+roots.real)/2
        for n in range(60):
            err=abs(row@d-(1+(1-eps)**n*math.cos(n*theta))/2);largest=max(largest,err)
            check(err<4e-11,'float_arithmetic_actual_response',(eps,q,n))
            row=weights[0]*np.roll(row,int(shifts[0]))+weights[1]*np.roll(row,int(shifts[1]))+cc*row.sum()/q
        lower=(math.pi*math.pi*c/(16*eps))**(1/3)
        check(lower<=q+1e-10 and q<=Q,'float_cubic_enclosure',(eps,lower,q,Q))
        phase_rows.append({'epsilon':eps,'proved_size_upper':Q,'constructed_size':q,'proved_size_lower':lower})
    DETAILS['golden_phase_constructions']=phase_rows
    DETAILS['maximum_floating_response_residual']=largest
    DETAILS['seed']=69016

if __name__=='__main__':
    exact_spectral();exact_thresholds_and_obstructions();raw_squared_embedding();exact_spectral_mixture();floating()
    print(json.dumps({'schema':'theta.r69.finite-diagnostics.v1','status':'PASS',
        'checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),'details':DETAILS,
        'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
        'limits':'Finite exact algebra and separate floating probes; no proof by sampling, formal proof, human endorsement, exhaustive priority or editorial certification.'},indent=2,sort_keys=True))
