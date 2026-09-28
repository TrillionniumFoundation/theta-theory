#!/usr/bin/env python3
"""Referee-designed finite controls for A2 v51; requires SymPy.

Run with Python and Python -O; output is deterministic. No repository code is
imported. These identities are not a proof of infinite-flight estimates,
Banach-space differentiability, billiard realization, or sampling guarantees.
"""
from __future__ import annotations
import json
import sympy as s


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def zero(expr: s.Expr, message: str) -> None:
    require(s.cancel(expr) == 0, message)


def main() -> None:
    u, v, z = s.symbols("u v z", real=True)
    a = s.Rational(1, 3)
    def action(t):
        return t**2 + t**3/5 + t**4/10
    def prime(t):
        return 2*t + 3*t**2/5 + 2*t**3/5
    zero(s.diff(action(z), z, 2) - (s.Rational(6,5)*(z+s.Rational(1,2))**2+s.Rational(17,10)), "convexity")
    H = 1-action(u)-action(v)
    A, C = 2+u+u*u, 3-v+2*v*v
    f = A*C*H/s.Integer(11)
    K = s.cancel(s.diff(f,u,v)/f-s.diff(f,u)*s.diff(f,v)/f**2)
    zero(K+prime(u)*prime(v)/H**2, "interaction cancellation")
    zero(K.subs(u,0), "vertical origin")
    zero(K.subs(v,0), "horizontal origin")
    kx = s.cancel(s.diff(K,u).subs({u:0,v:a}))
    ky = s.cancel(s.diff(K,v).subs({u:a,v:0}))
    require(kx != 0 and ky != 0, "simple roots")
    R = s.cancel(f*f.subs({u:0,v:0})/(f.subs(v,0)*f.subs(u,0)))
    def t(x):
        return action(x)/(1-action(x))
    zero(1-R-t(u)*t(v), "rank-one defect with unequal factors")
    q = s.cancel(t(a))
    require(q > 0, "positive scalar anchor")
    T = s.cancel((1-R.subs(v,a))/q)
    zero(T/(1+T)-action(u), "signed action inverse")
    require(action(a) != action(-a), "odd signed term exercised")
    zero((f.subs(v,0)/f.subs({u:0,v:0}))*(1+T)-A/A.subs(u,0), "first effective factor")
    zero((f.subs(u,0)/f.subs({u:0,v:0}))*(1+T.subs(u,v))-C/C.subs(v,0), "second effective factor")

    # A prescribed action and origin variation, plus arbitrary separate
    # logarithmic weight variations and an irrelevant normalization constant.
    alpha, beta = s.Rational(2,3), -s.Rational(3,4)
    def J(x):
        return x**2/7+x**3/9
    dotlog = u**3+2*v**2-s.Rational(5,8)+(alpha*prime(u)+beta*prime(v)-J(u)-J(v))/H
    dotK = s.diff(dotlog,u,v)
    recovered_x = s.cancel(-dotK.subs({u:0,v:a})/kx)
    recovered_y = s.cancel(-dotK.subs({u:a,v:0})/ky)
    require(recovered_x == alpha and recovered_y == beta, "origin transport")
    require(dotK.subs({u:0,v:a}) != 0, "frozen-origin negative control")
    def dt(x):
        return J(x)/(1-action(x))**2
    dotR = -dt(u)*t(v)-t(u)*dt(v)
    dotq = s.cancel(-dotR.subs({u:a,v:a})/(2*q))
    dotT = s.cancel(-dotR.subs(v,a)/q-(1-R.subs(v,a))*dotq/q**2)
    zero(dotT/(1+T)**2-J(u), "differentiated anchor inverse")
    bad = s.cancel((-dotR.subs(v,a)/q)/(1+T)**2-J(u))
    require(bad.subs(u,a) != 0, "omitted-anchor-derivative negative control")

    # Support equality does not determine the action. Conversely, the excluded
    # class of inseparable positive weights can mask two different actions.
    x,y = s.symbols('x y', nonnegative=True)
    eps = s.Rational(1,20)
    def phi(w):
        return w+eps*w*(1-w)*(w-s.Rational(1,2))
    zero(phi(1-x)-(1-phi(x)), "complement symmetry")
    factor = s.cancel((1-phi(x)-phi(y))/(1-x-y))
    expected = 1+eps*((x+y)/2-x*x+x*y-y*y)
    zero(factor-expected, "regular joint-factor extension")
    # On the cap x+y<=1, factor>=1-eps. On the box
    # 0<=x,y<=121/100, factor>=1-2*eps*(121/100)**2>0.
    zero(2*(x*x-x*y+y*y)-((x-y)**2+x*x+y*y), "positive factor decomposition")
    joint = 1/factor.subs({x:u*u,y:v*v})
    zero(joint*(1-phi(u*u)-phi(v*v))-(1-u*u-v*v), "joint masking identity")
    mixed = s.diff(joint,u,v)/joint-s.diff(joint,u)*s.diff(joint,v)/joint**2
    require(s.cancel(mixed.subs({u:a,v:a})) != 0, "mask is not separate")
    require(phi(a*a) != a*a, "distinct actions")
    # Exact quadratic support widths: no density amplitudes enter.
    width = 2*s.sqrt(1-u*u)
    require(s.diff(width,u).subs(u,0)==0 and s.diff(width,u,2).subs(u,0)==-2, "support-width maximum")

    # Determinant-one high-jet blocks at an asymmetric hyperbolic reference.
    for n in range(3,13):
        r, h = s.Rational(5,3), s.Rational(1,4)**n
        coth, csch = (1+h*h)/(1-h*h), 2*h/(1-h*h)
        M = s.Matrix([[coth,r**n*csch],[r**(-n)*csch,coth]])
        require(M.det()==1, f"jet block {n}")
    print(json.dumps({
        'status':'passed', 'imports_author_code':False, 'mathematical_certification':False,
        'controls':{
            'non_even_action_global_convexity_lower_bound':'17/10',
            'unequal_weight_interaction_and_action_identities':True,
            'scalar_anchor':str(q), 'simple_root_slope':str(kx),
            'origin_velocities':[str(recovered_x),str(recovered_y)],
            'moving_anchor_derivative':True,
            'support_preserving_distinct_action_and_joint_mask':True,
            'joint_cap_factor_positive_lower_bound':'19/20',
            'quadratic_support_width_second_derivative_at_center':'-2',
            'asymmetric_contact_block_orders':list(range(3,13))},
        'negative_controls':['freezing an unknown moving origin',
            'omitting the scalar-anchor derivative',
            'assuming a positive joint recording factor is separate'],
        'scope':'Exact finite functional and matrix controls. The support-width argument for all admissible strictly convex actions is proved in the report. No billiard realization or statistical guarantee is certified.'
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
