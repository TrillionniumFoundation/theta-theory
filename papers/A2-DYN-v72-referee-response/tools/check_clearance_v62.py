#!/usr/bin/env python3
"""Exact finite coarea and jet regressions; these are not Lorentz proof certificates."""
from fractions import Fraction as Q
from itertools import product
import json
import math
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rejected(function):
    try:
        function()
    except RuntimeError:
        return True
    return False


def finite_checks():
    x, y, t = sp.symbols('x y t', real=True)
    F = x + x*x + y*y
    Z = x*y + y**3
    D = lambda f: sp.diff(f, y) - sp.diff(F, y)/sp.diff(F, x)*sp.diff(f, x)
    J = sp.det(sp.Matrix([[sp.diff(F,x),sp.diff(F,y)],[sp.diff(Z,x),sp.diff(Z,y)]]))
    require(sp.simplify(D(Z)-J/sp.diff(F,x)) == 0, 'fiber first derivative/Jacobian')
    # Implicit graph x(t,y)=(-1+sqrt(1+4(t-y^2)))/2, on its positive-root branch.
    graph = (-1+sp.sqrt(1+4*(t-y*y)))/2
    for r in (1,2,3):
        jet = Z
        for _ in range(r):
            jet = sp.simplify(D(jet))
        direct = sp.diff(Z.subs(x,graph),y,r)
        for tv,yv in [(Q(1),Q(1,5)),(Q(2),Q(1,3)),(Q(3),Q(-1,4))]:
            difference = (jet.subs(x,graph)-direct).subs({t:sp.Rational(tv), y:sp.Rational(yv)})
            require(abs(float(difference.evalf(25))) < 1e-18, 'higher implicit fiber jet')
    # Forgetting the derivative of the tangent coefficient is a genuine wrong second jet.
    c = sp.diff(F,y)/sp.diff(F,x)
    frozen = sp.diff(Z,y,2)-2*c*sp.diff(Z,x,y)+c*c*sp.diff(Z,x,2)
    require(sp.simplify(D(D(Z))-frozen) != 0, 'frozen-coefficient negative control')

    # Exact monomial fold/type models. Domain is [-1,1]^2, F=y, Z=y+x^r.
    # On t=0 and r even, |{x:0<=x^r<=s}|=2 s^(1/r).
    type_cases = 0
    for r in (2,4,6):
        for k in range(2,17):
            width = Q(1,k**r)
            length = Q(2,k)
            require((length/2)**r == width, 'finite-type width exponent')
            derivative = math.factorial(r)
            C_r = 4*(r+1)*(math.factorial(r)*(r+1))**(1/r)
            require(float(length) <= C_r*(float(width)/derivative)**(1/r), 'sublevel constant')
            type_cases += 1
    # Shifted fold at arbitrary t: admissible positive/negative x intervals are both retained.
    fold_cases = 0
    for width in (Q(1,100),Q(1,16),Q(1,4)):
        for tv in [Q(j,100) for j in range(-100,101)]:
            lo=max(Q(0),-tv);hi=min(Q(1),width-tv)
            height = 0.0 if hi <= lo else 2*(math.sqrt(float(hi))-math.sqrt(float(lo)))
            require(height <= 2*math.sqrt(float(width))+1e-12, 'shifted-fold essential height')
            fold_cases += 1

    # Exact chart density factor d alpha/d x = 2/(1+x^2), no inverse grazing change.
    for a in [Q(j,10) for j in range(-10,11)]:
        jac = 2/(1+a*a)
        require(1 <= jac <= 2, 'rational angular density bound')
    # Uniform summation of the depth weights after taking a fixed r-th root.
    depth_cases = 0
    for m in range(2,101):
        for z in (Q(1,2),Q(3,4),Q(9,10)):
            require(sum(z**min(j,m-1-j) for j in range(m)) <= 2/(1-z), 'fiber depth sum')
            depth_cases += 1

    # Positive later-incidence envelope on an original clearance history.
    incidence_cases = 0
    for m in range(2,7):
        for shift in range(10):
            cs=[Q(1,2+((i+shift)%7)) for i in range(m+1)]
            chi=Q(1,5)
            inverse=Q(1)
            for ci in cs: inverse/=ci
            event=Q(int(min(cs)<chi))
            require(event <= sum(chi/ci for ci in cs) <= (m+1)*chi*inverse, 'later incidence retained')
            incidence_cases += 1

    # At a seam, F=x^2+y and Z=y: J=2x, the caustic is t=0.
    # On [-1,1]^2, |F| <= 2(|Z|+|J|); this tests the separation orientation.
    separation_cases = 0
    for xv,yv in product([Q(j,10) for j in range(-10,11)], repeat=2):
        fv=xv*xv+yv;zv=yv;jv=2*xv
        require(abs(fv) <= 2*(abs(zv)+abs(jv)), 'caustic separation orientation')
        separation_cases += 1
    for N in (1,2,3,5):
        for h,C in product((Q(1,2),Q(1,4)), (Q(1),Q(3))):
            eps=h**N/(4*C)
            require(h**N/C-2*eps == h**N/(2*C), 'rank threshold after strip subtraction')

    # The three-way source partition leaves every source point exactly once.
    partition_cases = 0
    for capped,near,first_clear in product((False,True),repeat=3):
        low=first_clear and not capped
        retained=first_clear and capped and near
        away=first_clear and capped and not near
        require(int(low)+int(retained)+int(away)==int(first_clear),'positive partition')
        partition_cases+=1

    p=Q(145,144)
    require(1/p==Q(144,145) and 1-1/p==Q(1,145),'weak-Lp source-mass exponent')
    # Negative controls use the same strict predicate as the positive checks.
    negatives = [
      rejected(lambda: require(Q(2,10)<=Q(1,10),'one fold branch omitted')),
      rejected(lambda: require(1-Q(1,2)==Q(1,145),'wrong source-mass exponent')),
      rejected(lambda: require(sum([1,1,0])==1,'clearance source counted twice')),
      rejected(lambda: require(sp.simplify(D(D(Z))-frozen)==0,'frozen tangent coefficient')),
    ]
    require(all(negatives),'a negative control escaped')
    return {'implicit_jet_orders':[1,2,3], 'implicit_jet_samples':9,
      'monomial_type_cases':type_cases,'shifted_fold_cases':fold_cases,
      'depth_sum_cases':depth_cases,'later_incidence_cases':incidence_cases,
      'caustic_separation_cases':separation_cases,'positive_partition_cases':partition_cases,
      'weak_mass_exponent':'1/145','negative_controls':len(negatives),
      'fixtures_are_not_Lorentz_realizations':True,
      'count_growth_not_removed':True,'continuum_proof_certified':False}

if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
