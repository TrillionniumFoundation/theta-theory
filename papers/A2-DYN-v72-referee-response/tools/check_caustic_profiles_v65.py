#!/usr/bin/env python3
"""Finite algebra/profile diagnostics, not physical-orbit or continuum certification."""
from fractions import Fraction as Q
import math
import numpy as np


def require(ok, message):
    if not bool(ok):
        raise RuntimeError(message)


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def guard(x):
    t=np.clip(np.asarray(x)-1.0,0.0,1.0)
    return t*t*t*(10.0+t*(-15.0+6.0*t))


def finite_checks():
    matrices=0
    for h00,h11,h01 in [(Q(3),Q(4),Q(1)),(Q(8),Q(7),Q(-2)),
                           (Q(23,3),Q(9,2),Q(1,7)),(Q(23,3),Q(9,2),Q(-1,7))]:
        delta=h00*h11-h01*h01
        a,b,c,d=-h00/h01,-1/h01,-delta/h01,-h11/h01
        M=[[a,b],[c,d]]; S=[[Q(1),Q(0)],[Q(0),Q(-1)]]
        Minv=[[d,-b],[-c,a]]
        P=mul(mul(mul(S,Minv),S),M)
        require(det(M)==1 and det(P)==1,'symplectic determinant')
        require(P==[[a*d+b*c,2*b*d],[2*a*c,a*d+b*c]],'reversible multiplication')
        D=det([[1-P[0][0],-P[0][1]],[-P[1][0],1-P[1][1]]])
        require(D==-4*b*c and b*c==delta/(h01*h01),'Hill factor four')
        require(abs(D)!=1,'negative inverse-determinant fixture not discriminating')
        J0=abs(float(h01))/math.sqrt(float(delta))
        J1=2/math.sqrt(abs(float(D)))
        require(abs(J0-J1)<1e-12,'relative coefficient square root')
        require(abs(J0-2/abs(float(D)))>1e-5,'wrong ordinary trace not rejected')
        require(delta/(c*c)==h01*h01/delta,'normal crossing ratio')
        matrices+=1
    # A genuine one-flight normal contact Hessian; no section-membership claim.
    R=Q(23,50); ell=1-2*R; H=[[1/R+1/ell,1/ell],[1/ell,1/R+1/ell]]
    require(det(H)==1/R**2+2/(R*ell),'one-flight contact Hessian')
    # Independent angular quadrature for quadratic and nonlinear finite fixtures.
    N=131072
    th=(np.arange(N)+0.5)*(2*math.pi/N)
    x,y=np.cos(th),np.sin(th); dth=2*math.pi/N
    profiles=0; max_exact_error=0.0; max_scaled_error=0.0
    for ratio in [1e-4,0.05,0.2,0.5,0.99,0.9999,1.0,1.1,2.0]:
        exact=2*math.asin(min(1.0,ratio))
        numeric=dth*np.count_nonzero((x>0)&(x<ratio))
        err=abs(exact-numeric);max_exact_error=max(max_exact_error,err)
        require(err<8*dth,'quadratic arcsine profile')
        profiles+=1
        for r in [1e-1,1e-2,1e-3,1e-4]:
            g=x+0.3*r*y*y
            w=1+0.1*r*x
            numeric=dth*np.sum(w*((g>0)&(g<ratio)))
            scaled=abs(numeric-exact)/math.sqrt(r)
            max_scaled_error=max(max_scaled_error,scaled)
            require(scaled<6.0,'nonlinear width-uniform angular bound')
            profiles+=1
    require(abs(dth*np.count_nonzero((x>0)&(y>0))-math.pi/2)<4*dth,'quarter cone')
    require(np.count_nonzero((x>0)&(-x>0))==0,'opposite parallel cone')
    for r in [0.1,0.01,0.001]:
        cusp=dth*np.count_nonzero((x>0)&(-x+r*y*y>0))
        require(cusp<5*r+8*dth,'parallel-seam cusp tends to zero')
    affine=0
    for r in [0.05,0.005,0.0005]:
        for beta in [0.0,0.2*r,2*r]:
            for width in [1e-7,0.05*r,r,0.01]:
                A1=beta+r*x; A2=r*y
                G1=A1+0.2*r*r*y*y; G2=A2+0.15*r*r*x*x
                Q0=0.1*r+r*(x-y); Q1=Q0+0.2*r*r*x*y
                Ba=(A1>0)&(A2>0); B=(G1>0)&(G2>0)
                va=Ba*(1-np.minimum(guard(A1/width),guard(A2/(0.7*width))))
                v=B*(1-np.minimum(guard(G1/width),guard(G2/(0.7*width))))
                pa=np.array([dth*np.sum(va*(Q0<=0)),dth*np.sum(va*(Q0>0))])
                p=np.array([dth*np.sum(v*(Q1<=0)),dth*np.sum(v*(Q1>0))])
                require(np.sum(np.abs(p-pa))<20*math.sqrt(r),'affine vector profile')
                require(np.sum(pa)<=2*math.pi+1e-12,'affine label partition')
                affine+=1
    # Offsets cannot be dropped uniformly as the positive margin varies.
    offset_profile=dth*np.sum((0.4+x>0)*(1-guard((0.4+x)/0.1)))
    zero_profile=dth*np.sum((x>0)*(1-guard(x/0.1)))
    require(abs(offset_profile-zero_profile)>0.01,'offset omission negative fixture')
    # Each pair of label vectors is zero or a single unit vector, in any dimension.
    for labels in [2,10,1000]:
        a=np.zeros(labels);b=np.zeros(labels);a[0]=1;b[-1]=1
        require(np.sum(np.abs(a-b))==2,'label variation independent of count')
    # Fixed-band and exponentially shrinking diagonal bounds have distinct limits.
    def log_height(m,logB):return 2*math.log(m)+m*math.log(2)-logB/12
    require(log_height(40,100)>log_height(20,100),'fixed-band growth fixture')
    require(log_height(40,36*40*math.log(2))<log_height(20,36*20*math.log(2)),
            'diagonal decay fixture')
    return {'exact_reversible_matrix_fixtures':matrices,'one_flight_geometric_fixture':True,
            'quadratic_and_nonlinear_angular_fixtures':profiles,'affine_label_fixtures':affine,
            'max_quadratic_quadrature_error':float(max_exact_error),
            'max_nonlinear_error_divided_by_sqrt_radius':float(max_scaled_error),
            'wrong_determinant_power_rejected':True,'quarter_and_parallel_cones_checked':True,
            'discarded_affine_offset_rejected':True,'label_variation_factor_two_checked':True,
            'ordered_limit_negative_fixture_checked':True,
            'actual_Lorentz_caustic_realization_certified':False,
            'long_count_trace_concentration_certified':False,
            'continuum_proof_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
