#!/usr/bin/env python3
"""Finite algebra/models for the exact bridge proof; not a billiard proof."""
from fractions import Fraction as F
import sympy as sp

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def finite_checks():
    l, x, z = sp.symbols('l x z', positive=True)
    expr = sp.exp(-l*(x+z)**2/2)
    fourth = sp.simplify(sp.diff(expr,z,4).subs(z,0)/sp.exp(-l*x*x/2))
    require(sp.expand(fourth-(3*l*l-6*l**3*x*x+l**4*x**4)) == 0,'fourth derivative')
    # Scalar Gaussian bridges: exact interval fourth moment divided by alpha^2.
    moments = 0
    for m in range(1,51):
        for length in range(1,m+1):
            a = F(length,m)
            for endpoint in range(-4,5):
                mean = a*endpoint; var = a*(1-a)
                moment = mean**4+6*mean*mean*var+3*var*var
                require(moment <= a*a*(3+6*endpoint**2+endpoint**4),'Gaussian bridge moment budget')
                require(F(length**4,m**2) <= length**2,'local integral power balance')
                moments += 1
    # Conditional covariance of independent Gaussian vector increments.
    S = sp.Matrix([[2,sp.Rational(1,3),0],[sp.Rational(1,3),3,sp.Rational(1,4)],[0,sp.Rational(1,4),4]])
    require(all(S[:j,:j].det()>0 for j in range(1,4)),'test covariance positive')
    alpha=[sp.Rational(1,5),sp.Rational(1,3),sp.Rational(7,15)]
    vectors=[sp.Matrix([1,2,-1]),sp.Matrix([0,-1,2]),sp.Matrix([2,0,1])]
    vbar=sum((a*v for a,v in zip(alpha,vectors)),sp.zeros(3,1))
    block=sp.diag(*(a*S for a in alpha)); summap=sp.Matrix.hstack(*([sp.eye(3)]*3))
    conditional=block-block*summap.T*S.inv()*summap*block
    w=sp.Matrix.vstack(*vectors)
    lhs=(w.T*conditional*w)[0]
    rhs=sum(a*(v.T*S*v)[0] for a,v in zip(alpha,vectors))-(vbar.T*S*vbar)[0]
    require(sp.simplify(lhs-rhs)==0 and lhs>=0,'bridge characteristic covariance')
    require(conditional*summap.T==sp.zeros(9,3),'bridge pinned sum')
    # Exact physical clock covariance and pin.
    tau,t,m,k1,k2=sp.symbols('tau t m k1 k2',positive=True)
    clock=sp.diag(1,1,-1/tau); V=clock*S*clock.T/tau
    require(sp.simplify(V.det()-S.det()/tau**5)==0,'clock determinant')
    pin=sp.sqrt(m/t)*clock*sp.Matrix([k1,k2,t-m*tau])/sp.sqrt(m)
    wanted=sp.Matrix([k1/sp.sqrt(t),k2/sp.sqrt(t),(m-t/tau)/sp.sqrt(t)])
    require(all(sp.simplify(q)==0 for q in pin-wanted),'physical bridge pin')
    # Support functions, exact area and perimeter for independent harmonics.
    theta,r,a2,b2,a3,b3=sp.symbols('theta r a2 b2 a3 b3',real=True)
    h=r+a2*sp.cos(2*theta)+b2*sp.sin(2*theta)+a3*sp.cos(3*theta)+b3*sp.sin(3*theta)
    area=sp.integrate(sp.expand_trig(h*(h+sp.diff(h,theta,2))),(theta,0,2*sp.pi))/2
    target=sp.pi*r*r-sp.pi*(3*(a2*a2+b2*b2)+8*(a3*a3+b3*b3))/2
    require(sp.simplify(area-target)==0,'support area')
    require(sp.integrate(h,(theta,0,2*sp.pi))==2*sp.pi*r,'support perimeter')
    require(F(91,200)-F(1,200)==F(9,20) and F(93,200)+F(1,200)==F(47,100),'curvature-radius bounds')
    require(F(91,200)-F(1,600)>F(9,20) and F(93,200)+F(1,600)<F(47,100),'disk support bounds')
    require(8*F(1,1600)==F(1,200),'noncentrally symmetric example budget')
    aa,bb=sp.symbols('aa bb',real=True)
    require(sp.expand((sp.Rational(3,5)*aa-sp.Rational(4,5)*bb)**2+(sp.Rational(4,5)*aa+sp.Rational(3,5)*bb)**2-aa**2-bb**2)==0,'rotation-invariant harmonic budget')
    # Entry root with A=1, B=-2, C=3; zero-root current obstacle with B=1.
    roots=[2-sp.sqrt(4-3),2+sp.sqrt(4-3)]
    require(roots==[1,3],'entering versus exiting root')
    require(-1+sp.sqrt(1)==0 and -1-sp.sqrt(1)<0,'current zero root exclusion')
    # Deliberately wrong Gaussian factor, clock sign and no-denominator scaling.
    require(sp.simplify(lhs-sum(a*(v.T*S*v)[0] for a,v in zip(alpha,vectors)))!=0,'unconditioned covariance negative control')
    require(sp.simplify(pin[2]-(t-m*tau)/(tau*sp.sqrt(t)))!=0,'wrong clock sign negative control')
    require(F(8**2,1)>F(8**2,64),'missing normalization negative control')
    return {'Gaussian_bridge_fourth_moment_cases':moments,
            'marked_fourth_derivative_identity':True,'multiblock_conditional_covariance_identity':True,
            'exact_physical_pin_and_determinant':True,'support_area_and_perimeter':True,
            'rotation_invariant_support_budget':True,'entry_root_and_zero_root':True,'negative_controls':3,
            'no_conditioned_independence_assumption':True,
            'continuum_proof_verified_by_finite_models':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
