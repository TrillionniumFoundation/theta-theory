#!/usr/bin/env python3
"""Independent finite controls for A2 v62. No manuscript checker is imported.
These are finite probability/algebra/rounding controls, not billiard-realization
or infinite-dimensional proof certificates. Requires mpmath and sympy.
"""
from fractions import Fraction as F
from math import comb, factorial, ceil, floor, log, exp, sqrt
import json
import mpmath as mp
import sympy as sp

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def conditional_counts():
    cases = 0
    # Exact unconditional counts divided by P(M=m) give the conditional multinomial.
    for p in (F(1, 7), F(1, 2), F(5, 6)):
        q = (F(2, 7), F(3, 7), F(2, 7))
        for n in range(1, 9):
            for m in range(1, n+1):
                pm = comb(n, m)*p**m*(1-p)**(n-m)
                total = F(0)
                for a in range(m+1):
                    for b in range(m-a+1):
                        c = m-a-b
                        mult = factorial(m)//(factorial(a)*factorial(b)*factorial(c))
                        joint = comb(n,m)*mult*(p*q[0])**a*(p*q[1])**b*(p*q[2])**c*(1-p)**(n-m)
                        target = mult*q[0]**a*q[1]**b*q[2]**c
                        require(joint/pm == target, 'Conditional multinomial failure')
                        total += joint/pm
                        cases += 1
                require(total == 1, 'Conditional law not normalized')
    # Removing the outside category changes normalization even with exact probabilities.
    q_in = F(5,7)
    require(F(2,7)/q_in == F(2,5) and F(2,5) != F(2,7), 'Outside negative control')
    return {'exact_conditional_count_configurations': cases,
            'outside_category_control': {'correct_cell_mass':'2/7', 'recropped_mass':'2/5'}}

def probability_bounds():
    mp.mp.dps = 70
    lower_cases = 0
    bernstein_cases = 0
    worst_lower = mp.mpf(0)
    worst_bernstein = mp.mpf(0)
    for n in (8, 17, 40, 75):
        for p0 in (F(1,20), F(1,5), F(1,2), F(4,5)):
            p = mp.mpf(p0.numerator)/p0.denominator
            limit = n*p/2
            mass = sum(mp.mpf(comb(n,k))*p**k*(1-p)**(n-k)
                       for k in range(n+1) if k <= limit)
            bound = mp.exp(-n*p/8)
            require(mass <= bound+mp.mpf('1e-60'), 'Binomial lower-tail bound')
            worst_lower = max(worst_lower, mass/bound)
            lower_cases += 1
    for m in (10, 30, 80, 160):
        for p0 in (F(1,100), F(1,10), F(1,3), F(3,4)):
            p = mp.mpf(p0.numerator)/p0.denominator
            for x0 in (1, 2, 4, 8, 12):
                x = mp.mpf(x0)
                radius = mp.sqrt(2*p*x/m)+2*x/(3*m)
                mass = sum(mp.mpf(comb(m,k))*p**k*(1-p)**(m-k)
                           for k in range(m+1) if abs(mp.mpf(k)/m-p) > radius)
                bound = 2*mp.exp(-x)
                require(mass <= bound+mp.mpf('1e-60'), 'Bernstein tail bound')
                worst_bernstein = max(worst_bernstein, mass/bound)
                bernstein_cases += 1
    return {'binomial_cases':lower_cases, 'bernstein_cases':bernstein_cases,
            'max_binomial_tail_bound_ratio':str(worst_lower),
            'max_bernstein_tail_bound_ratio':str(worst_bernstein)}

def cell_geometry():
    cases=0
    for h in (F(1,5),F(1,20),F(1,100)):
        for ratio in (F(0),F(1,10),F(1,4),F(1,2)):
            r=h*ratio
            require((h+2*r)**2-(h-2*r)**2 == 8*h*r, 'Square tube identity')
            require(h*h+8*h*r <= 5*h*h, 'Displaced cell mass bound')
            cases+=1
    # A Borel map moving a strip by distance r may change an O(hr) cell mass.
    # This finite geometric control shows why dividing by h^2 leaves r/h.
    h,r=F(1,10),F(1,1000)
    require((h*r)/(h*h) == r/h, 'Cell-average displacement scaling')
    return {'exact_square_tube_cases':cases,
            'strip_mass':'1/10000','cell_average_change':'1/100','r_over_h':'1/100'}

def exponents_and_schedules():
    omega,gamma=sp.symbols('omega gamma', positive=True)
    z=omega/(4*omega+gamma)
    require(sp.simplify((1-gamma/(4*omega+gamma))/4-z)==0,'Calibrated exponent')
    require(sp.simplify((1-gamma/(4*omega+gamma)-2*z)/2-z)==0,'Variance exponent')
    require(sp.simplify(1-gamma/(4*omega+gamma)-2*z-2*z)==0,'Linear exponent')
    j=sp.symbols('j',positive=True)
    require(sp.simplify(sp.exp(gamma*j)*(sp.exp(-omega*j)**4)**(-3)
                        /sp.exp((12*omega+gamma)*j))==1,'Pilot exponent')
    calibrated=0; full=0; grid_controls=[]
    for w,G in ((.1,1.),(.3,1.5),(1.,3.)):
        for n in (10**8,10**14,10**22):
            for alpha in (.1,.01,1e-6):
                L=log(100*n/alpha); a=L/n; z=w/(4*w+G)
                jn=2*floor(log(n/L)/(2*(4*w+G)))
                h=(L*exp(G*jn)/n)**.25
                require(jn%2==0 and jn>=2,'Even calibrated flight')
                require(exp(-w*jn) <= exp(2*w)*a**z*(1+1e-12),'Finite bias rounding')
                require(h <= a**z*(1+1e-12),'Calibrated mesh rounding')
                require(n*exp(-G*jn)/L >= (n/L)**(4*z)*(1-1e-12),'Count scaling')
                # An equal-square grid of side at most h loses at most a factor 2.
                grid=ceil(1/h); rounded=1/grid
                require(h/2 <= rounded <= h,'Equal-square rounding')
                calibrated+=1
                jf=2*floor(log(n/(L*L))/(2*(12*w+G)))
                if jf>=2:
                    hf=exp(-w*jf); target=(L*L/n)**(w/(12*w+G))
                    require(hf <= exp(2*w)*target*(1+1e-12),'Complete cap rounding')
                    require(exp((12*w+G)*jf) <= n/(L*L)*(1+1e-12),'Complete cap exponent')
                    full+=1
    # Printed all-history grid endpoint bound is false for fractional grid lengths.
    for n in (10,50,500):
        j=2; gminus=F(1); gplus=F(3,2); eps=F(2,2*n+1)
        q=j*(gplus-gminus)/eps
        L=ceil(q)+2; tlast=j*gminus+L*eps
        printed=j*gplus+2*eps; corrected=j*gplus+3*eps
        require(tlast>printed and tlast<corrected,'Scan ceiling counterexample')
        grid_controls.append({'epsilon':str(eps),'q':str(q),'last_time':str(tlast),
                              'printed_bound':str(printed),'corrected_strict_bound':str(corrected),
                              'overshoot_in_epsilon_units':str((tlast-j*gplus)/eps)})
    return {'symbolic_balance_identities':4, 'calibrated_even_schedules':calibrated,
            'complete_budget_even_schedules':full,
            'scan_ceiling_counterexamples':grid_controls,
            'scope':'The ceiling control corrects a time bound, not either statistical exponent.'}

if __name__=='__main__':
    print(json.dumps({'scope':'Finite exact probability and geometric identities; high-precision finite tail sums; schedule controls. No proof of billiard realization, infinite-dimensional inversion, relative determinant limits, or minimax optimality.',
                      'imports_author_checker':False,
                      'conditional_counts':conditional_counts(),
                      'probability_bounds':probability_bounds(),
                      'cell_geometry':cell_geometry(),
                      'exponents_and_schedules':exponents_and_schedules()},indent=2,sort_keys=True))
