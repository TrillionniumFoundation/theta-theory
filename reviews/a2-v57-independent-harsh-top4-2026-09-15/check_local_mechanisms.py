#!/usr/bin/env python3
"""Independent finite controls for the v57 report, not a proof certificate.

Requires SymPy. No manuscript checker is imported. Output is deterministic and
uses explicit exceptions, so python -O does not remove the checks.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as s


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil(q):
    return -(-q.numerator // q.denominator)


def run():
    blocks = 0
    for t in [F(1,5), F(1,3), F(1,2), F(2,3), F(4,5)]:
        c = (1+t*t)/(2*t)
        for w in [F(k,6) for k in range(1,6)]:
            r = (1-w)/c+w*c
            c0, c1 = c*r, c/r
            require(c0>1 and c1>1 and c0*c1==c*c, 'inadmissible geometry')
            q = (1+t*t)/2
            for n in range(3,33):
                den=1-t**(2*n)
                a=(1+t**(2*n))/den
                b=2*(r*t)**n/den
                d=2*(t/r)**n/den
                require(a*a-b*d==1, 'determinant')
                # The inverse [[a,-b],[-d,a]] has the same infinity norm.
                bound=(3+t**6)/(1-t**6)
                require(max(a+b,a+d)<=bound, 'uniform block/inverse bound')
                require(max(a-1+b,a-1+d)<=4*q**n/(1-t**6), 'exponential identity limit')
                # Finite partial sums plus their exact geometric tails.
                K=7
                diagonal=1+2*sum(t**(2*k*n) for k in range(1,K+1))
                diagonal+=2*t**(2*(K+1)*n)/den
                off=2*r**n*sum(t**((2*k+1)*n) for k in range(K))
                off+=2*r**n*t**((2*K+1)*n)/den
                require(diagonal==a and off==b, 'endpoint/interior multiplicities')
                blocks+=1
    u,v=s.symbols('u v', real=True)
    S=lambda z: z**2+z**3/s.Integer(5)+z**4/s.Integer(7)
    d=s.Integer(2)
    f=lambda x,y: (2+x)*(3-y/s.Integer(4))*(d-S(x)-S(y))/11
    ratio=s.cancel(f(u,v)*f(0,0)/(f(u,0)*f(0,v)))
    t=lambda z:S(z)/(d-S(z))
    require(s.cancel(1-ratio-t(u)*t(v))==0, 'four-density identity')
    anchor=s.Rational(1,10)
    qa=t(anchor)
    require(qa>0, 'scalar anchor sign')
    T=s.cancel((1-ratio.subs(v,anchor))/qa)
    recovered=s.cancel(d*T/(1+T))
    require(s.cancel(recovered-S(u))==0, 'signed action inverse')
    require(s.diff(recovered,u,3).subs(u,0)==s.Rational(6,5), 'odd jet')
    cross=s.diff(f(u,v),u,v)/f(u,v)-s.diff(f(u,v),u)*s.diff(f(u,v),v)/f(u,v)**2
    require(s.cancel(cross+s.diff(S(u),u)*s.diff(S(v),v)/(d-S(u)-S(v))**2)==0,'mixed log derivative')
    x,p,theta=s.symbols('x p theta')
    k,q3,q4=s.symbols('k q3 q4', nonzero=True)
    psi=k*x*x/2+q3*x**3/6+q4*x**4/24
    y=p/k-q3*p*p/(2*k**3)+(3*q3*q3-k*q4)*p**3/(6*k**5)
    require(s.series(s.diff(psi,x).subs(x,y)-p,p,0,4).removeO().expand()==0,'Legendre inverse')
    H=s.integrate(y,p)
    h=s.series(s.cos(theta)*H.subs(p,s.tan(theta)),theta,0,5).removeO().expand()
    h4=s.simplify(s.diff(h,theta,4).subs(theta,0))
    require(s.simplify(h4-(2/k-q4/k**4+3*q3*q3/k**5))==0,'support fourth jet')
    area_s=s.integrate(s.sin(theta)**4,(theta,0,2*s.pi))
    area_z=s.integrate(s.sin(theta)**6,(theta,0,2*s.pi))
    require(area_s==3*s.pi/4 and area_z==5*s.pi/8,'area derivatives')
    require(-area_s/area_z==-s.Rational(6,5),'area preserving tangent')
    dq=-s.Integer(24)
    slope=s.simplify(-(7+2)/(12*3*4*s.sqrt(3))*dq)
    require(slope==s.sqrt(3)/2,'quartic nonlinear information')
    L=s.Matrix([[2,s.Rational(1,3)],[s.Rational(1,5),3]])
    M=s.Matrix([[2,1],[0,3]])
    require(M.det()==6 and (L*M)*M.inv()==L,'nonunimodular gain inverse')
    grids=0
    for j in [2,10,50]:
        for hstep in [F(1,10),F(1,20)]:
            for g in [F(1),F(101,100),F(4,3),F(17,10),F(2)]:
                gm,gp=F(1),F(2)
                l=ceil(j*(g-gm)/hstep)+1
                length=ceil(j*(gp-gm)/hstep)+2
                excess=j*gm+l*hstep-j*g
                require(0<=l<=length and hstep<=excess<=2*hstep,'onset grid coverage')
                grids+=1
    return {
        'status':'passed', 'proof_certificate':False,
        'admissible_rational_last_jet_blocks':blocks,
        'orders_checked':[3,32],
        'block_controls':['determinant and explicit inverse','uniform infinity-norm bound','exponential approach to identity','endpoint/interior geometric sums'],
        'signed_density_control':{'third_action_derivative':'6/5','four_density_identity':True,'mixed_log_derivative':True,'realized_billiard_claim':False},
        'support_fourth_derivative':'2/k - q4/k^4 + 3*q3^2/k^5',
        'area_derivatives':['3*pi/4','5*pi/8'],'area_preserving_tangent':'-6/5',
        'quartic_information_slope':'sqrt(3)/2',
        'gain_matrix_determinant':6,'onset_grid_cases':grids,
        'limitations':'Finite algebraic controls do not prove orbit localization, trace-class limits, all-order smooth remainders, analytic continuation, statistical probability bounds or global rigidity.'
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(run(),indent=2)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')


if __name__=='__main__':
    main()
