#!/usr/bin/env python3
"""Independent finite controls for the v63 referee report.
Python 3 and SymPy. No manuscript/author checker is imported. No removable
assertions. Outputs exact finite arithmetic controls, not theorem certificates.
"""
from fractions import Fraction as F
from math import comb, factorial, ceil, log, exp, floor
import json
import sympy as s

def require(ok, message):
    if not ok: raise RuntimeError(message)

def grid_checks():
    cases=onsets=old_failures=0
    extrema=[]
    for j in [2,4,8,16,32]:
        for span in [F(0),F(1,7),F(1,2),F(5,3)]:
            for epsilon in [F(1,2),F(2,7),F(2,101),F(3,1009),F(1,10000)]:
                gm=F(1);gp=gm+span;q=j*span/epsilon;L=ceil(q)+2
                t=lambda ell:j*gm+ell*epsilon
                overshoot=(t(L)-j*gp)/epsilon
                require(overshoot==ceil(q)-q+2 and 2<=overshoot<3,'All-history endpoint identity')
                if overshoot>2:old_failures+=1
                require(t(L)<j*gp+3*epsilon,'Revised upper bound')
                # Exact worst-case total pilot duration when all scans exhaust.
                for E in [1,3]:
                    for N in [1,7]:
                        B=2*E*(L+1)*N
                        exact=2*E*N*((L+1)*j*gm+epsilon*L*(L+1)/2)
                        require(exact<=B*t(L)<B*(j*gp+3*epsilon),'Complete pilot duration')
                for frac in [F(0),F(1,5),F(1,2),F(4,5),F(1)]:
                    g=gm+span*frac
                    ell=ceil(j*(g-gm)/epsilon)+1
                    excess=t(ell)-j*g
                    require(0<=ell<=L and epsilon<=excess<2*epsilon,'Near-onset grid point')
                    # Any successful earlier stop is after onset and at most this grid time.
                    for good_excess in [epsilon/100,epsilon,excess]:
                        require(abs((j*g+good_excess-epsilon)/j-g)<=epsilon/j,'Good-history gap error')
                    onsets+=1
                cases+=1
    j=2;gm=F(1);gp=F(3,2);eps=F(2,101)
    L=ceil(j*(gp-gm)/eps)+2;tlast=j*gm+L*eps
    require(tlast==F(308,101) and j*gp+2*eps==F(307,101),'Previous counterexample')
    return {'grid_configurations':cases,'onset_configurations':onsets,
            'exact_worst_duration_configurations':4*cases,'old_bound_violations':old_failures,
            'previous_counterexample':{'last_time':str(tlast),'old_bound':str(j*gp+2*eps),'new_strict_bound':str(j*gp+3*eps)}}

def conditioned_counts():
    cases=0
    for N in range(1,9):
        for p in [F(1,5),F(1,2),F(4,5)]:
            for q in [F(1,3),F(2,5),F(3,4)]:
                for m in range(N+1):
                    pm=comb(N,m)*p**m*(1-p)**(N-m)
                    total=F(0)
                    for k in range(m+1):
                        multi=factorial(N)//(factorial(k)*factorial(m-k)*factorial(N-m))
                        joint=multi*(p*q)**k*(p*(1-q))**(m-k)*(1-p)**(N-m)
                        target=comb(m,k)*q**k*(1-q)**(m-k)
                        require(joint/pm==target,'Conditional mark-count factorization')
                        total+=target;cases+=1
                    require(total==1,'Conditional distribution normalization')
    return {'exact_multinomial_conditioning_cases':cases,'scope':'Counts for fixed independent attempts, not conditioning a stopped stream on cap completion.'}

def pilot_failure_checks():
    cases=[]
    for p in [F(1,100),F(1,10),F(1,2),F(9,10)]:
        for E in [1,3,8]:
            for beta in [.2,.05,.001]:
                N=ceil(log(2*E/beta)/float(p))
                # Numerically evaluate finite binomial zero-success probability in log form.
                upper=2*E*exp(N*log(1-float(p)))
                require(upper<=beta*(1+1e-12),'Pilot union bound')
                cases.append({'p':str(p),'channels':E,'beta':beta,'attempts_per_point':N,'union_bound':upper})
    return {'configurations':len(cases),'records':cases}

def exponents_and_tubes():
    w,G=s.symbols('omega Gamma',positive=True);z=w/(4*w+G);zz=w/(12*w+G)
    identities=[s.simplify(1-G/(4*w+G)-4*z),s.simplify((1-G/(4*w+G)-2*z)/2-z),
                s.simplify(12*zz+G/(12*w+G)-1),s.simplify((1-G/(4*w+G)-2*z)-2*z)]
    require(all(v==0 for v in identities),'Rate exponent balance')
    h,r,Fd=s.symbols('h r F',positive=True)
    require(s.expand((h+2*r)**2-(h-2*r)**2-8*h*r)==0,'Tube area')
    tests=0
    for hh in [F(1,4),F(1,10),F(1,30)]:
        for ratio in [F(0),F(1,8),F(1,4),F(1,2)]:
            rr=ratio*hh
            require(hh*hh+8*hh*rr<=5*hh*hh,'Displaced cell mass coefficient')
            tests+=1
    return {'symbolic_exponent_identities':[str(x) for x in identities],'symbolic_tube_identity':True,'exact_cell_mass_cases':tests,'pilot_epsilon_power':-3,'epsilon_as_power_of_h':4,'resulting_pilot_h_power':-12}

if __name__=='__main__':
    result={'scope':'Independent finite arithmetic, count-factorization, failure-probability and symbolic-balance controls. Not a billiard realization, arbitrary-order inverse, trace-class convergence, minimax or global rigidity proof.','imports_author_checker':False,'pilot_grid':grid_checks(),'fixed_attempt_counts':conditioned_counts(),'pilot_failure':pilot_failure_checks(),'rates_and_calibration':exponents_and_tubes()}
    print(json.dumps(result,indent=2,sort_keys=True))
