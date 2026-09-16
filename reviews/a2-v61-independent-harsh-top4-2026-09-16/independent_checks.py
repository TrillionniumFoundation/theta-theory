#!/usr/bin/env python3
"""Independent finite algebra for the v61 review. Not a theorem/proof certificate.
Requires SymPy. No manuscript checker is imported; no removable assertions.
"""
import json
from fractions import Fraction
import sympy as s

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def integral_sin_even(n):
    return 2*s.pi*s.binomial(n,n//2)/2**n

def support_and_response():
    p,z,t=s.symbols('p z t', real=True)
    I=integral_sin_even
    area=s.pi+p*I(4)+z*I(6)+(p*p*(17*I(8)-16*I(6))+2*p*z*(25*I(10)-24*I(8))+z*z*(37*I(12)-36*I(10)))/2
    normalized=s.expand(area/s.pi)
    wanted=1+s.Rational(3,4)*p+s.Rational(5,8)*z-s.Rational(45,128)*p**2-s.Rational(105,128)*p*z-s.Rational(525,1024)*z**2
    require(s.simplify(normalized-wanted)==0,'Area polynomial')
    slope=-s.diff(area,p).subs({p:0,z:0})/s.diff(area,z).subs({p:0,z:0})
    h=1+p*s.sin(t)**4+z*s.sin(t)**6
    xx=h*s.cos(t)-s.diff(h,t)*s.sin(t); yy=h*s.sin(t)+s.diff(h,t)*s.cos(t)
    xs=s.series(1-xx,t,0,6).removeO();ys=s.series(yy,t,0,6).removeO()
    require(s.expand(xs-(ys**2/2+(3-24*p)*ys**4/24)).series(t,0,6).removeO().expand()==0,'Support-to-graph fourth jet')
    dq_action=7/(4*s.sqrt(3));dq_amp=-s.Rational(1,48);a=s.sqrt(3)
    dq_response=s.simplify(2*dq_amp/(3*a)-dq_action/(12*a*a))
    response=s.simplify(-24*dq_response)
    omitted=s.simplify(24*dq_action/(12*a*a))
    require(response==s.sqrt(3)/2,'Onset response')
    require(omitted!=response,'Omitted-amplitude negative control')
    return {'area_over_pi':str(normalized),'z_prime_at_zero':str(slope),'fourth_graph_derivative':'3 - 24*p','response_derivative':str(response),'omitting_determinant_gives':str(omitted)}

def cofactor_controls():
    count=0;worst=0
    for mode in range(4):
        for j in range(1,13):
            edges=[s.Rational(5+(i+mode)%4,5) for i in range(j)]
            H=s.zeros(j+1)
            for i in range(j+1):
                H[i,i]=s.Rational(2+mode,3)+(edges[i-1] if i else 0)+(edges[i] if i<j else 0)
            for i,b in enumerate(edges):H[i,i+1]=H[i+1,i]=-b
            EE=H.extract([0,j],[0,j])
            if j>1:
                II=H[1:j,1:j];EI=H.extract([0,j],list(range(1,j)))
                K=EE-EI*II.inv()*EI.T;den=II.det()
            else:K=EE;den=1
            require(s.cancel(-K[0,1]-s.prod(edges)/den)==0,'Schur/cofactor identity')
            count+=1
    return {'positive_tridiagonal_cases':count,'scope':'Exact finite algebra, not global billiard realizations.'}

def finite_quartic():
    out=[];count=0
    for t in [s.Rational(1,5),s.Rational(1,3),s.Rational(1,2)]:
        c=(t+1/t)/2;a=(1/t-t)/2
        limit=s.cancel(-(((1/t**2+t**2)/2)+2)/(12*a*a*((1/t**2-t**2)/2)))
        by_j=[]
        for j in [1,2,3,5,8,12,16]:
            sinh=lambda k:(t**(-k)-t**k)/2
            coth=(1+t**(2*j))/(1-t**(2*j));csch=2*t**j/(1-t**(2*j))
            # Independent recurrence solution of the finite quadratic chain.
            H=s.zeros(j+1)
            for i in range(j+1):H[i,i]=c if i in [0,j] else 2*c
            for i in range(j):H[i,i+1]=H[i+1,i]=-1
            E=[0,j];inter=list(range(1,j));K=H.extract(E,E)
            if inter:
                G=H.extract(inter,inter).inv();C=H.extract(inter,E);T=-G*C;K-=C.T*G*C
            else:G=s.zeros(0);T=s.zeros(0,2)
            require(K==a*s.Matrix([[coth,-csch],[-csch,coth]]),'Effective Hessian')
            M=K.inv();L=[s.Matrix([[1,0]])]+[T[i:i+1,:] for i in range(j-1)]+[s.Matrix([[0,1]])]
            for i in range(1,j):
                target=s.Matrix([[sinh(j-i)/sinh(j),sinh(i)/sinh(j)]])
                require(L[i]==target,'Recurrence endpoint interpolation')
            v=[(l*M*l.T)[0] for l in L]
            finite=-sum(G[i-1,i-1]*v[i] for i in range(1,j))/3-(v[0]**2+v[j]**2+2*sum(v[i]**2 for i in range(1,j)))/24
            by_j.append({'flights':j,'coefficient':float(finite),'distance_to_limit':float(abs(finite-limit))});count+=1
        require(by_j[-1]['distance_to_limit']<1e-7,'Finite quartic limit control')
        out.append({'decay_factor':str(t),'limit':str(limit),'finite_records':by_j})
    return {'cases':count,'records':out,'scope':'Exact finite coefficient/Green algebra; this is not a proof of trace-class convergence.'}

if __name__=='__main__':
    result={'scope':'Independent symbolic and exact rational finite controls. No infinite-dimensional inverse, general trace-class limit, or journal significance is certified.','imports_author_checker':False,'support_and_response':support_and_response(),'cofactor_controls':cofactor_controls(),'finite_quartic':finite_quartic()}
    print(json.dumps(result,indent=2,sort_keys=True))
