#!/usr/bin/env python3
"""Exact algebra and finite independent chain checks for R80 sharpness.

The symbolic checks authenticate displayed algebraic identities. The rational
grid and high-precision realizations are finite diagnostics; neither is a
proof of the universal optimization or asymptotic theorem. All checks remain
active under python -O. No numerical optimizer is used.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

import sympy as sp

CHECKS = Counter()


def require(condition, group, message):
    if not condition:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] += 1


def exact_equal(left, right, group, message):
    require(sp.cancel(left-right) == 0, group, message)


def symbolic_certificates():
    group = "exact_symbolic_certificates"
    r, s, g, d, beta, B = sp.symbols("r s g d beta B")
    q = 1-beta
    n0 = s+(1-s)*d+(1-r)*g
    d0 = r*s+r*(1-s)*d+s*(1-r)*g
    n1 = beta*(1-s)+q*(1-s)*d+r+q*(1-r)*g
    d1 = beta*(1-s)*(beta+q*r+q*(1-r)*(d+g))
    claimed = (beta*q*s*s*(1-r)**2*g*g
               +2*beta*q*s*r*(1-s)*(1-r)*g*d
               +beta*(1-r)*(beta*beta*(r-s)+s*s*(beta+2*q*r))*g
               +beta*q*r*r*(1-s)**2*d*d
               +beta*s*r*(1-s)*(beta+2*q*r)*d
               +beta*s*s*r*(beta+q*r))
    actual = n1*beta*(beta*n0+q*d0)-d1*(beta*n0+d0)
    exact_equal(actual, claimed, group, "positive-polynomial identity")
    # The opposite orientation: substitute the necessary model-0 transition.
    ge = (s+(1-s)*d)*(1-B*r)/((1-r)*(B*s-1))
    on = beta+q*s+q*(1-s)*d+q*(1-r)*g
    od = beta*(1-r)*(beta+q*s+q*(1-s)*(d+g))
    fun = sp.cancel((on/od).subs(g, ge))
    den = (B*beta*d*r*s-B*beta*d*r-B*beta*d*s*s+B*beta*d*s
           +B*beta*s*s-B*beta*s-B*d*r*s+B*d*r+B*d*s*s-B*d*s
           +B*r*s-B*s*s-beta*d*r*s+beta*d*r+beta*d*s*s-beta*d*s
           +beta*r*s-beta*r-beta*s*s+beta+d*r*s-d*r-d*s*s+d*s
           -r*s+s*s)
    exact_equal(sp.diff(fun,d)*den**2,
                (beta-1)*(r-s)*(s-1)*(B*r-1)*(B*s-1),
                group,"opposite-orientation delta derivative")
    f0 = sp.cancel(fun.subs(d,0))
    den0 = den.subs(d,0)
    exact_equal(sp.diff(f0,r)*den0**2,
                -(B*s-1)**2*(beta*s-beta-s),
                group,"opposite-orientation row derivative")
    exact_equal(sp.diff(f0.subs(r,0),s)*den0.subs(r,0)**2,
                (1-beta)*s*(B*s-2),
                group,"opposite-orientation minimum derivative")
    atmin = (beta+4*q/B)/(beta*(beta+4*q/B-4*q/B**2))
    exact_equal(fun.subs({r:0,d:0,s:2/B}), atmin,
                group,"opposite-orientation reduced value")
    exact_equal((B-atmin).subs(beta,sp.Rational(1,4)),
                B*(B*B+8*B-60)/(B*B+12*B-12),
                group,"opposite-orientation root polynomial")
    D = beta+q*r
    f = (beta+r)/(beta*D)
    exact_equal(sp.diff(f,r),beta/D**2,group,"comparison derivative")
    exact_equal(sp.diff(n1/d1,s).subs({s:0,g:0,d:0}),
                r/(beta*D),group,"second-row first derivative")
    exact_equal(sp.diff(n1/d1,d).subs({s:0,g:0,d:0}),
                q*r*r/(beta*D**2),group,"escape first derivative")
    exact_equal(r/(beta*D)-q*r*r/(beta*D**2),
                r/D**2,group,"strict escape preference")
    h1,h2,t1,t2 = sp.symbols("h1 h2 t1 t2")
    determinant = h1*h2+h1*t2+h2*t1
    c1 = (h2+t2+t1)/determinant
    exact_equal(c1-1/h1,(h1-h2)*t1/(h1*determinant),
                group,"exact activated-trap cost identity")
    return {"identities":CHECKS[group],
            "type":"Exact polynomial and rational-function algebra, not a proof assistant"}


def solve(matrix, vector):
    n = len(vector)
    a = [[Q(v) for v in matrix[i]]+[Q(vector[i])] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:
            return None
        a[j],a[pivot] = a[pivot],a[j]
        v = a[j][j]
        a[j] = [x/v for x in a[j]]
        for i in range(n):
            if i != j:
                v = a[i][j]
                a[i] = [x-v*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]


def cost(parameters, success):
    r,s,alpha,gamma,xi,delta = parameters
    rows = [r,s]
    update = [[(1-alpha,alpha),(1-gamma,gamma)],
              [(xi,1-xi),(delta,1-delta)]]
    transition = [[sum((rows[k] if a == 0 else 1-rows[k])
                       *(1-success[a])*update[k][a][j] for a in range(2))
                   for j in range(2)] for k in range(2)]
    reached = {0}
    while True:
        more = reached | {j for i in reached for j in range(2)
                          if transition[i][j] > 0}
        if more == reached:
            break
        reached = more
    ids = sorted(reached)
    values = solve([[Q(i == j)-transition[i][j] for j in ids] for i in ids],
                   [Q(1)]*len(ids))
    if values is None or any(x < 0 for x in values):
        return None
    return values[0]


def rational_controllers():
    group = "exact_rational_controller_grid"
    rows = [Q(i,4) for i in range(5)]
    updates = [Q(0),Q(1,2),Q(1)]
    total = finite = opposite = perturbations = 0
    for r,s in product(rows,repeat=2):
        for alpha,gamma,xi,delta in product(updates,repeat=4):
            p = (r,s,alpha,gamma,xi,delta)
            c0,c1 = cost(p,(Q(1),Q(0))),cost(p,(Q(0),Q(1,4)))
            total += 1
            if c0 is None or c1 is None:
                continue
            finite += 1
            b = max(c0,c1)
            require(b >= 4 and b*b-b-16 >= 0,group,
                    "finite controller beats the baseline algebraic value")
            if r <= s:
                opposite += 1
                require(b*b+8*b-60 >= 0,group,
                        "opposite orientation beats its algebraic value")
            for eps in (Q(1,10000),Q(1,100)):
                perturbed = cost(p,(1-eps,Q(0)))
                if perturbed is not None:
                    require(perturbed >= c0,group,"cost failed perturbation monotonicity")
                    perturbations += 1
    require(total == 2025,group,"rational grid count")
    # An inaccessible dark state is valid at zero but becomes fatal if
    # the old optimizer's routing is used without an escape at positive error.
    old = (Q(1,5),Q(0),Q(1),Q(0),Q(0),Q(0))
    require(cost(old,(Q(1),Q(0))) == 5,group,"supported baseline chain")
    require(cost(old,(Q(9999,10000),Q(0))) is None,group,"activated dark trap")
    return {"controllers":total,"finite_baseline_controllers":finite,
            "finite_opposite_orientation":opposite,
            "finite_perturbation_comparisons":perturbations,
            "finite_grid_is_not_a_universal_proof":True}


def exact_realizations():
    group = "exact_rational_repaired_programs"
    cases = 0
    for r,delta,eps in product((Q(1,5),Q(1,4),Q(1,3)),
                               (Q(1,1000),Q(1,100),Q(1,10)),
                               (Q(1,1000000),Q(1,10000),Q(1,100))):
        params = (r,Q(0),Q(1),Q(0),Q(0),delta)
        c0 = cost(params,(1-eps,Q(0)))
        c1 = cost(params,(Q(0),Q(1,4)))
        beta,q = Q(1,4),Q(3,4)
        require(c0 == 1/((1-eps)*r)+eps/((1-eps)*delta),group,
                "model-0 explicit repaired program")
        require(c1 == (beta+q*delta+r)/(beta*(beta+q*r+q*(1-r)*delta)),
                group,"model-1 explicit repaired program")
        cases += 1
    for eps in (Q(0),Q(1,10),Q(1,2)):
        fixed = (Q(1,3),Q(1,3),Q(0),Q(0),Q(0),Q(0))
        require(cost(fixed,(1-eps,Q(0))) <= 6,group,"common fallback model 0")
        require(cost(fixed,(Q(0),Q(1,4))) == 6,group,"common fallback model 1")
    return {"repaired_programs":cases,"fallback":"One fixed a-probability 1/3"}


def leading_constant():
    group = "exact_quadratic_field_constants"
    beta = sp.Rational(1,4)
    q = 1-beta
    r = (sp.sqrt(65)-1)/32
    B = 1/r
    D = beta+q*r
    A,F,L = 1/r**2,beta/D**2,q*r**2/(beta*D**2)
    k = beta/sp.sqrt(q)
    h = (1/k-L*k)/(A+F)
    constant = 2*sp.sqrt(q)*r*r/(D*D+beta*r*r)
    require(sp.simplify(r*r+beta*beta*r-beta*beta) == 0,
            group,"baseline row polynomial")
    require(sp.simplify(B-(1+sp.sqrt(65))/2) == 0,
            group,"baseline value")
    require(sp.simplify(k*k-F/(A*L)) == 0,group,"optimal escape scale")
    require(sp.simplify((-A*h+1/k)-constant) == 0,group,"model-0 leading coefficient")
    require(sp.simplify((F*h+L*k)-constant) == 0,group,"model-1 leading coefficient")
    # 70-digit arithmetic checks the explicit constructive upper family only.
    # It does not compute or certify the true optimized V2 at any positive eps.
    fg = "high_precision_constructive_asymptotic"
    samples=[]
    for exponent in (4,6,8,10,12):
        eps=sp.Rational(1,10**exponent)
        rr=r+h*sp.sqrt(eps)
        dd=k*sp.sqrt(eps)
        cost0=1/((1-eps)*rr)+eps/((1-eps)*dd)
        cost1=(beta+q*dd+rr)/(beta*(beta+q*rr+q*(1-rr)*dd))
        normalized0=sp.N((cost0-B)/sp.sqrt(eps),70)
        normalized1=sp.N((cost1-B)/sp.sqrt(eps),70)
        cn=sp.N(constant,70)
        # Explicit finite error tolerance scales with sqrt(eps), as the
        # displayed rational formula's next term does.
        tolerance=sp.N(100*sp.sqrt(eps),70)
        require(abs(normalized0-cn)<tolerance,fg,"constructive model-0 scaled limit")
        require(abs(normalized1-cn)<tolerance,fg,"constructive model-1 scaled limit")
        samples.append({"epsilon":f"1e-{exponent}",
                        "model_0_normalized_upper_gap":str(normalized0),
                        "model_1_normalized_upper_gap":str(normalized1),
                        "absolute_comparison_tolerance":str(tolerance)})
    return {"baseline_value":str(sp.N(B,30)),"coefficient":str(sp.N(constant,30)),
            "escape_scale":str(sp.N(k,30)),"initial_row_shift":str(sp.N(h,30)),
            "upper_construction_only":samples}


def main():
    result={"symbolic":symbolic_certificates(),"rational_grid":rational_controllers(),
            "independent_realizations":exact_realizations(),"leading_constant":leading_constant()}
    source=Path(__file__).resolve().parent/"sections"/"57-sharp-stability.tex"
    if not source.is_file():
        source=Path(__file__).resolve().parent/"57-sharp-stability.tex"
    require(source.is_file(),"source_binding","missing mathematical source")
    result["source_sha256"]=hashlib.sha256(source.read_bytes()).hexdigest()
    floating=CHECKS["high_precision_constructive_asymptotic"]
    total=sum(CHECKS.values())
    print(json.dumps({"schema":"theta.r80.sharp-stability-diagnostics.v1",
                      "status":"PASS","exact_checks":total-floating,
                      "floating_checks":floating,"total_checks":total,
                      "checks_by_group":dict(sorted(CHECKS.items())),
                      "results":result,
                      "limits":"Finite diagnostics and exact algebra identities; not formal verification, universal optimization, external expert review, or priority certification."},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
