#!/usr/bin/env python3
"""Finite exact controls for the A2 v50 referee report. Requires SymPy.
These are algebraic/geometry diagnostics, not a certification of infinite-flight
estimates, a numerical billiard simulation, or a full manuscript proof audit.
All checks raise explicit exceptions and remain enabled with python -O.
"""
import json
import sympy as s


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def equal(x, y, message):
    require(s.simplify(x-y) == 0, message)


def schur(H):
    n = H.rows
    if n == 2:
        return H
    endpoints = [0, n-1]
    middle = list(range(1, n-1))
    return H.extract(endpoints, endpoints) - H.extract(endpoints, middle) * H.extract(middle, middle).inv() * H.extract(middle, endpoints)


def finite_twists():
    c = [s.Rational(25, 24), s.Rational(3, 2)]
    g = s.Rational(2, 3)
    for j in range(1, 11):
        H = s.zeros(j+1)
        for i in range(j):
            H[i,i] += c[i % 2]/g
            H[i+1,i+1] += c[(i+1) % 2]/g
            H[i,i+1] = H[i+1,i] = -1/g
        d0 = -schur(H)[0,1]
        q = s.Rational(9,8) if j % 2 else s.Rational(15,16)
        sinh = (s.Integer(2)**j - s.Rational(1,2)**j)/2
        equal(d0, q/sinh, 'alternating reference twist')
        P = H.copy()
        for i in range(j+1):
            P[i,i] += s.Rational(i+1, 1000)
        for i in range(j):
            P[i,i+1] = P[i+1,i] = H[i,i+1]*(1+s.Rational(i+1,1000))
        prod = s.prod(g*(-P[i,i+1]) for i in range(j))
        idx = list(range(1,j))
        ratio = s.Integer(1)
        if idx:
            H0 = H.extract(idx,idx)
            delta = P.extract(idx,idx)-H0
            ratio = (s.eye(j-1)+H0.inv()*delta).det()
        equal((-schur(P)[0,1])/d0, prod/ratio, 'normalized cofactor identity')
    require((s.Rational(3,4)/s.Rational(1,2))**20 > 3000,
            'absolute-error negative control')
    return {'reference_and_perturbed_lengths':list(range(1,11)),
            'absolute_bound_alone_does_not_imply_relative_decay':True,
            'scope':'Perturbed matrices are algebraic controls, not asserted billiard realizations.'}


def contact_blocks():
    for n in range(3,13):
        q = s.Rational(1,2)**n
        diag = (1+q*q)/(1-q*q)
        off = 2*q/(1-q*q)
        M = s.Matrix([[diag,s.Rational(5,6)**n*off],
                      [s.Rational(6,5)**n*off,diag]])
        equal(M.det(), 1, 'signed contact determinant')
        # Boundary site is counted once, every interior occurrence twice.
        equal(diag, 1+2*q*q/(1-q*q), 'boundary multiplicity')
        bad = s.Matrix([[1/(1-q*q),s.Rational(5,6)**n*q/(1-q*q)],
                        [s.Rational(6,5)**n*q/(1-q*q),1/(1-q*q)]])
        require(s.simplify(bad.det()-1) != 0, 'multiplicity negative control')
    return {'orders':list(range(3,13)), 'determinants_one':True,
            'missing_interior_multiplicity_detected':True}


def moving_reference():
    t = s.symbols('t', real=True)
    H = s.Matrix([[3+t,1+t/3,0],[1+t/3,4-t/2,1],[0,1,5+t]])
    D = s.Matrix([[s.Rational(1,10)+t/7,t/9,0],[t/9,s.Rational(1,8),t/11],[0,t/11,s.Rational(1,12)-t/13]])
    G = H.inv()
    T = G*D
    T0 = T.subs(t,0)
    inv = (s.eye(3)+T0).inv()
    correct = -(inv*T.diff(t).subs(t,0)).trace()
    quotient = H.det()/(H+D).det()
    direct = (quotient.diff(t)/quotient).subs(t,0)
    equal(correct, direct, 'moving-reference logarithmic derivative')
    wrong = -(inv*(G*D.diff(t)).subs(t,0)).trace()
    require(s.simplify(correct-wrong) != 0, 'omitted moving-reference term detectable')
    return {'correct_log_derivative':str(s.factor(correct)),
            'omitting_dot_G_error':str(s.factor(wrong-correct)),
            'scope':'Noncommuting 3x3 family, not an infinite-operator estimate.'}


def density_inverse():
    t = s.symbols('t', real=True)
    def action(u): return (1+t)*(u*u/s.Integer(10)+u**3/s.Integer(100))
    def B(u): return 1+u/s.Integer(20)+u*u/s.Integer(100)+t*u/s.Integer(30)
    def f(u,v): return B(u)*B(v)*(1-action(u)-action(v))
    def R(u,v): return s.cancel(f(u,v)*f(0,0)/(f(u,0)*f(0,v)))
    a = s.Rational(1,4)
    q = action(a)/(1-action(a))
    equal(q*q, 1-R(a,a), 'anchor square')
    require(q.subs(t,0)>0, 'positive scalar anchor')
    for u in [s.Rational(-1,4),s.Rational(-1,8),s.Integer(0),s.Rational(1,8),a]:
        z = s.cancel((1-R(u,a))/q)
        equal(z/(1+z), action(u), 'action from four densities')
        q0=q.subs(t,0); z0=z.subs(t,0)
        pred=-s.diff(R(u,a),t).subs(t,0)/q0+z0*s.diff(R(a,a),t).subs(t,0)/(2*q0*q0)
        equal(pred,s.diff(z,t).subs(t,0),'anchor derivative sign')
    require(action(a).subs(t,0)!=action(-a).subs(t,0),'signed odd term retained')
    return {'signed_points':5,'amplitude_cancellation':True,'anchor_derivative':True}


def geometry():
    a=s.sqrt(2)/2; R=s.Rational(101,1000)
    Ls=[s.Matrix([[1,a],[0,a]]),s.Matrix([[1,-a],[0,a]])]
    m,n=s.symbols('m n',integer=True)
    theta=s.symbols('theta',real=True)
    h=s.Rational(1,10)+s.cos(4*theta)/1000
    equal((h+s.diff(h,theta,2)).subs(theta,0),s.Rational(17,200),'convexity minimum')
    require(1-a>4*R*R,'all-lattice disk separation')
    for L in Ls:
        w=L*s.Matrix([1,1]); z=L*s.Matrix([m,n])
        equal(s.det(s.Matrix.hstack(w,z)),a*(n-m),'all-lattice added-channel determinant')
    vectors=[s.Matrix([a,a]),s.Matrix([-a,a]),s.Matrix([-a,-a]),s.Matrix([a,-a])]
    signs=[s.sign(s.det(s.Matrix.hstack(s.Matrix([1,0]),v))) for v in vectors]
    require(signs==[1,1,-1,-1],'two orientation-compatible branches')
    ellp=s.sqrt(2+s.sqrt(2)); ellm=s.sqrt(2-s.sqrt(2))
    require(a/ellp>2*R,'actual-segment tube clearance')
    require(ellp-2*R>1 and ellm+2*R<1,'extra-gap separation')
    equal(s.diff(h,theta).subs(theta,s.pi/8),-s.Rational(1,250),'nonradial plus normal')
    equal(s.diff(h,theta).subs(theta,3*s.pi/8),s.Rational(1,250),'nonradial minus normal')
    tolerance=(ellp-ellm-4*R)/2
    threshold=(ellp+ellm)/2
    require(tolerance>0,'deterministic branch margin')
    return {'orientation_signs':[int(x) for x in signs],
            'safe_threshold':float(threshold),'strict_error_tolerance':float(tolerance),
            'actual_segment_clearance_lower_bound':float(a/ellp-2*R),
            'scope':'Exact original two-point fiber; not uniform recovery under noisy original laws.'}


def main():
    result={'mathematical_certification':False,'finite_twists':finite_twists(),
            'contact_blocks':contact_blocks(),'moving_reference':moving_reference(),
            'density_inverse':density_inverse(),'geometry':geometry()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
