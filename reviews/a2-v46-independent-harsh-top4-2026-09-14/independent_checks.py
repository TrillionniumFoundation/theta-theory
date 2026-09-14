#!/usr/bin/env python3
"""Referee's finite exact/algebraic diagnostics for A2 v46.

No author diagnostic is imported. These checks do not certify an infinite
half-line limit or realizability by a periodic billiard table.
Dependencies: Python 3, SymPy. All validity decisions survive python -O.
"""
from __future__ import annotations
import cmath
import json
import math
import random
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def low_degree_bellman() -> dict:
    u, v = sp.symbols('u v')
    cubic = sp.symbols('q03 q13')
    quartic = sp.symbols('q04 q14')
    kappa = [sp.Rational(1, 2), sp.Rational(1, 24)]
    action2 = [sp.Rational(9, 10), sp.Rational(5, 8)]
    alpha = [sp.Rational(3, 5), sp.Rational(5, 12)]
    q = lambda b, x: kappa[b]*x**2/2 + cubic[b]*x**3/6 + quartic[b]*x**4/24
    # Exact total-degree-four expansion of sqrt((1+q_b+q_c)^2+(v-u)^2).
    flight = []
    for b in (0, 1):
        h2 = kappa[b]*u**2/2 + kappa[1-b]*v**2/2
        flight.append(1 + q(b, u) + q(1-b, v) + (v-u)**2/2
                      - h2*(v-u)**2/2 - (v-u)**4/8)
    s3 = sp.symbols('s03 s13')
    equations = []
    for b in (0, 1):
        f = flight[b]-1+action2[1-b]*v**2/2+s3[1-b]*v**3/6
        equations.append(s3[b]-6*sp.expand(f.subs(v, alpha[b]*u)).coeff(u, 3))
    sol3 = sp.solve(equations, s3)
    a3 = sp.Matrix([sp.factor(sol3[x]) for x in s3])
    s4 = sp.symbols('s04 s14')
    a4eq = []
    orbit2 = []
    for b in (0, 1):
        d = sp.Symbol('orbit2')
        f = flight[b]-1+action2[1-b]*v**2/2+a3[1-b]*v**3/6+s4[1-b]*v**4/24
        stationary = sp.expand(sp.diff(f, v).subs(v, alpha[b]*u+d*u**2)).coeff(u, 2)
        db = sp.factor(sp.solve(stationary, d)[0])
        orbit2.append(db)
        rhs = 24*sp.expand(f.subs(v, alpha[b]*u+db*u**2)).coeff(u, 4)
        a4eq.append(s4[b]-rhs)
    sol4 = sp.solve(a4eq, s4)
    a4 = sp.Matrix([sp.factor(sol4[x]) for x in s4])
    verified = []
    for n, an, qn in [(3, a3, cubic), (4, a4, quartic)]:
        bn = sp.Matrix([[0, alpha[0]**n], [alpha[1]**n, 0]])
        mn = (sp.eye(2)-bn).inv()*(sp.eye(2)+bn)
        require(all(sp.simplify(x)==0 for x in an.jacobian(qn)-mn), f'order {n} block')
        require(sp.factor(mn.det())==1, f'order {n} determinant')
        pn = sp.simplify((sp.eye(2)-bn)*an-(sp.eye(2)+bn)*sp.Matrix(qn))
        require(not any(pn.has(x) for x in qn), 'remainder contains new graph coefficient')
        recovered = (sp.eye(2)+bn).inv()*((sp.eye(2)-bn)*an-pn)
        require(all(sp.simplify(x)==0 for x in recovered-sp.Matrix(qn)), 'inverse recovery')
        verified.append(n)
    example = {cubic[0]:sp.Rational(1,5), cubic[1]:sp.Rational(-1,7),
               quartic[0]:sp.Rational(2,9), quartic[1]:sp.Rational(3,11)}
    b4 = sp.Matrix([[0, alpha[0]**4], [alpha[1]**4, 0]])
    wrong = (sp.eye(2)+b4).inv()*(sp.eye(2)-b4)*a4
    omission = [float(sp.N(x.subs(example))) for x in wrong-sp.Matrix(quartic)]
    require(max(map(abs, omission))>0.01, 'lower-remainder negative control failed')
    return {'exact_orders':verified, 'gap':1, 'curvatures':[str(x) for x in kappa],
            'alpha':[str(x) for x in alpha], 'generic_symbolic_new_jets':True,
            'omitted_quartic_remainder_errors':omission,
            'scope':'Exact truncated Bellman algebra; not an independent proof of infinite-orbit convergence.'}


def other_checks() -> dict:
    rng = random.Random(2026091446)
    maximum = 0.0
    cases = 0
    for modes, powers in [([2,3],[-1,1]),([4,9],[-2,1]),([6,10,15],[1,1,-1])]:
        require(sum(k*b for k,b in zip(modes,powers))==1, 'Bezout coefficients')
        for _ in range(100):
            angle=rng.uniform(-math.pi,math.pi)
            p=[cmath.exp(1j*rng.uniform(-math.pi,math.pi)) for _ in modes]
            t=[z*cmath.exp(-1j*k*angle) for z,k in zip(p,modes)]
            recovered=math.prod((x/y)**b for x,y,b in zip(p,t,powers))
            maximum=max(maximum,abs(recovered-cmath.exp(1j*angle)))
            cases+=1
    require(maximum<1e-12, 'phase convention')
    # An exact positive-density aliasing example, not an asserted billiard law.
    x=sp.symbols('x', real=True)
    cells=7
    mass_differences=[sp.integrate(sp.sin(2*sp.pi*cells*x)/5,
                       (x,sp.Rational(k,cells),sp.Rational(k+1,cells))) for k in range(cells)]
    require(all(v==0 for v in mass_differences), 'aliased masses')
    # Exact TV between normalized radial quadratic-cap densities at offsets d and D.
    d,D,w=sp.symbols('d D w', positive=True)
    crossing=d*D/(d+D)
    cdf_difference=sp.factor(2*crossing*(1/d-1/D)-crossing**2*(1/d**2-1/D**2))
    require(sp.simplify(cdf_difference-(D-d)/(D+d))==0,'offset TV identity')
    # Finite sufficient order in the manuscript's own continuation prescription.
    s=1.0;B=2.0;Creg=10.0;eps=1e-3
    r=min(s/8,1/8);steps=math.ceil(math.pi/r)+1;beta=2.0**(-steps)
    logv=(math.log(eps)-math.log(2*Creg)-(1-beta)*math.log(2*B))/beta
    m=math.ceil((math.log(16*B/3)-logv)/math.log(4)-1)
    require(math.log(8*B/3)-(m+1)*math.log(4)<=logv-math.log(2)+1e-6,'tail prescription')
    return {'bezout_cases':cases,'bezout_max_error':maximum,
            'histogram_alias':{'cells':cells,'all_cell_mass_differences':'exactly zero',
                               'density_L1':'2/(5*pi)','scope':'functional negative control'},
            'offset_TV':'(D-d)/(D+d), for D>d>0',
            'offset_scope':'normalized quadratic-cap model, not a periodic-billiard counterexample',
            'accuracy_example':{'s':s,'B':B,'C_reg':Creg,'target':eps,'J_s':steps,
                                 'beta_s':beta,'log_v':logv,'sufficient_jet_order':m,
                                 'practical_efficiency':False}}


def main() -> None:
    result={'status':'passed','mathematical_certification':False,
            'bellman':low_degree_bellman(),'other':other_checks()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
