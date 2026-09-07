#!/usr/bin/env python3
"""Independent exact diagnostics for the pinned A1 v19 referee review.

Run: python independent_checks.py --output INDEPENDENT_CHECK_RESULTS.json
Requires Python >=3.10 and SymPy (executed here with 1.14.0).
No repository code is imported, no network is used, and no author test suite
or LaTeX build is run. Finite checks supplement, not replace, the proofs
and scope qualifications in REFEREE_REPORT.md.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools as it
import json
import math
import platform
import sys
import time
from collections import defaultdict
from pathlib import Path
import sympy as s

PIN = "01abeb689b203ea871b88495d16a826bb4942e16"
COUNTS: dict[str, int] = defaultdict(int)
DETAILS: dict[str, object] = {}


def check(suite: str, condition: object, description: str) -> None:
    if not bool(condition):
        raise AssertionError(f"{suite}: {description}")
    COUNTS[suite] += 1


def zero(x: object) -> bool:
    return s.simplify(x) == 0


def kernel_example() -> None:
    suite = "exact_kernel_counterexample"
    points = list(it.product(range(1, 5), (-1, 1)))
    ev_e = s.Matrix([[int(j == k) for j, sign in points] for k in range(1, 5)])
    ev_f = s.Matrix([[1, sign, j * sign] for j, sign in points])
    check(suite, ev_e.rank() == 4 and ev_f.rank() == 3, "dimensions 4 and 3")
    p = s.symbols("p0:8", positive=True)
    H = ev_e * s.diag(*p) * ev_f
    expected = s.Matrix([[p[2*j]+p[2*j+1], p[2*j+1]-p[2*j],
                          (j+1)*(p[2*j+1]-p[2*j])] for j in range(4)])
    check(suite, H == expected, "symbolic pairing formula")
    check(suite, H[:, 2] == s.diag(1, 2, 3, 4) * H[:, 1], "forced companion kernel")
    H0 = H.subs({v: s.Rational(1, 8) for v in p})
    check(suite, H0.rank() == 1, "full-support witness rank one")
    check(suite, H0.nullspace() == [s.Matrix([0, 1, 0]), s.Matrix([0, 0, 1])],
          "kernel contains two independent nonconstant functions")
    GU = ev_e * s.diag(*(sign for j, sign in points))
    check(suite, GU.rank() == 4, "product vectors span R4")
    check(suite, GU * s.ones(8, 1) == s.zeros(4, 1), "strictly positive barycentric mean zero")
    check(suite, all(GU[:, 2*j] == -GU[:, 2*j+1] for j in range(4)),
          "product body is the full-dimensional crosspolytope")
    # A positive affine realization has augmented tangent E and future space F.
    for j, sign in points:
        f = [s.Rational(int(j == k), 6) for k in range(1, 4)]
        for u in it.product((-1, 1), repeat=3):
            for y in (-1, 1):
                L = (1 + y * sum(ui*fi for ui, fi in zip(u, f))) / 2
                check(suite, L >= s.Rational(5, 12), "physical likelihood lower bound")
        for g in (s.Rational(1, 2)+s.Rational(sign, 4),
                  s.Rational(1, 2)+s.Rational(j*sign, 16)):
            check(suite, s.Rational(1, 4) <= g <= s.Rational(3, 4), "physical query bounds")
    DETAILS[suite] = {"points": 8, "E_dimension": 4, "F_dimension": 3,
                      "U_dimension": 1, "forced_nullity_when_U_is_contained": 2,
                      "refutes": "exact-kernel reading of introductory/response claims",
                      "does_not_refute": "thm:v19-rank-alternative as printed"}


def pentagon() -> None:
    suite = "pentagon_and_square_obstruction"
    pts = [(0,0),(2,0),(3,1),(1,3),(-1,1)]
    vals = [[x+3*y-1 for x,y in pts], [2*y-1 for x,y in pts],
            [-x+y-1 for x,y in pts], [-2*x-1 for x,y in pts]]
    wanted = [[-1,1,5,9,1],[-1,-1,1,5,1],[-1,-3,-3,1,1],[-1,-5,-7,-3,1]]
    for row, target in zip(vals, wanted):
        for x,y in zip(row,target):
            check(suite, x == y, "separator value")
    a,b=s.symbols("a b", real=True)
    inc=[2*a,a+b,-2*a+2*b,-2*a-2*b]
    check(suite, zero(2*inc[0]+inc[2]+inc[3]), "positive linear dependence of three inequalities")
    check(suite, s.solve([inc[0],inc[2],inc[3]],(a,b)) == {a:0,b:0},
          "all nonnegative increments force zero affine direction")
    check(suite, max(abs(x)+abs(y) for x,y in pts) == 4, "likelihood bound")
    DETAILS[suite] = {"separator_entries":20,"nonnegative_increment_certificate":"2*g0+g2+g3=0"}


def walsh() -> None:
    suite="walsh_covariance_realization"
    for b,q in [(1,1),(2,2),(2,3),(3,2)]:
        A=s.Matrix(q,b,lambda j,i:s.Symbol(f"a{j}_{i}"))
        points=list(it.product((-1,1), repeat=b+q))
        densities=[1+sum(A[j,i]*z[i]*z[b+j] for j in range(q) for i in range(b)) for z in points]
        average=lambda values:s.expand(sum(values)/len(points))
        check(suite,average(densities)==1,"normalization")
        for k in range(b+q):
            check(suite,average([rho*z[k] for rho,z in zip(densities,points)])==0,"coordinate mean")
        for j in range(q):
            for i in range(b):
                cross=average([rho*z[i]*z[b+j] for rho,z in zip(densities,points)])
                check(suite,cross==A[j,i],"cross moment")
                cov=cross/(8*b*s.sqrt(q))
                check(suite,zero(cov-A[j,i]/(8*b*s.sqrt(q))),"weighted physical covariance")
        numeric={A[j,i]:s.Rational((-1)**(i+j),2*b*q) for j in range(q) for i in range(b)}
        for rho in densities:
            v=rho.subs(numeric)
            check(suite,s.Rational(1,2)<=v<=s.Rational(3,2),"density envelope on boundary example")
        for z in points:
            for u in it.product((-1,1),repeat=b):
                for y in (-1,1):
                    L=(1+y*sum(s.Rational(u[i]*z[i],2*b) for i in range(b)))/2
                    check(suite,L>=s.Rational(1,4),"all command-vertex likelihoods")
    DETAILS[suite]={"symbolic_dimension_pairs":[[1,1],[2,2],[2,3],[3,2]],
                    "universal_positivity_argument":"triangle inequality in the report/source, not finite enumeration"}


def orders(C: s.Matrix, t: s.Symbol) -> list[object]:
    result=[]
    for k in range(1,min(C.shape)+1):
        values=[]
        for rows in it.combinations(range(C.rows),k):
            for cols in it.combinations(range(C.cols),k):
                p=s.Poly(s.expand(C.extract(rows,cols).det()),t)
                values.append(min(m[0] for m,c in p.terms() if c) if not p.is_zero else s.oo)
        result.append(min(values))
    return result


def determinantal_orders() -> None:
    suite="analytic_minor_orders"
    t=s.Symbol("t")
    C=s.Matrix([[t,t**2],[t**2,t**3+t**5]])/16
    check(suite,s.expand(C.det())==t**6/256,"displayed determinant")
    check(suite,orders(C,t)==[1,6],"displayed minor orders")
    examples=[]
    for alphas in [(0,2,2),(1,2,6),(0,0,3),(1,5)]:
        r=len(alphas); n=r+1
        D=s.zeros(n,n+1)
        for i,a in enumerate(alphas): D[i,i]=t**a
        U=s.eye(n); V=s.eye(n+1)
        for i in range(n-1): U[i,i+1]=t+i+1
        for i in range(n): V[i+1,i]=t**2+i+1
        check(suite,U.det()==1 and V.det()==1,"analytic unimodular multipliers")
        B=U*D*V
        got=orders(B,t)
        expected=[sum(alphas[:k]) for k in range(1,r+1)]+[s.oo]
        check(suite,got==expected,"non-diagonal rectangular minor valuations")
        check(suite,B.subs(t,0).rank()==sum(a==0 for a in alphas),"zero endpoint rank")
        examples.append({"orders":list(alphas),"minor_orders":[str(v) for v in got]})
    check(suite,orders(s.zeros(2,3),t)==[s.oo,s.oo],"identically zero case")
    DETAILS[suite]={"examples":examples,"displayed_two_scale_orders":[1,5]}


def phase_envelopes() -> None:
    suite="phase_transition_envelopes"
    number=0
    for r in range(1,5):
        for alpha in it.combinations_with_replacement(range(5),r):
            number+=1
            A=[sum(alpha[:k]) for k in range(1,r+1)]
            beta=[k*alpha[k]-A[k-1] for k in range(1,r)]
            check(suite,all(x>=0 for x in beta) and beta==sorted(beta),"ordered nonnegative transitions")
            boundaries=[s.Integer(0)]+list(map(s.Integer,beta))
            for k in range(1,r+1):
                left=boundaries[k-1]
                right=s.Integer(beta[k-1]) if k<r else left+7
                for gamma in set((left,right,(left+right)/2)):
                    exponents=[2*(s.Integer(A[j])+gamma)/(j+1) for j in range(r)]
                    check(suite,exponents[k-1]==min(exponents),"advertised branch minimizes on its interval")
    DETAILS[suite]={"ordered_lists_checked":number,"list_lengths":[1,2,3,4],"entries":[0,1,2,3,4]}


def integer_envelope() -> None:
    suite="integer_budget_envelope"
    families=[(s.Integer(1),s.Rational(1,3),s.Rational(1,9)),
              (s.Rational(2,3),)*3,(s.Integer(2),s.Rational(3,2),0),
              (s.Rational(1,7),0,0),(0,0,0),(3,2,1,s.Rational(1,5))]
    cases=0
    for values in families:
        values=list(map(s.sympify,values)); V=[s.prod(values[:j]) for j in range(1,len(values)+1)]
        for ell,scale in enumerate(values,1):
            if scale==0: continue
            cases+=1
            real_budget=V[ell-1]/scale**ell
            M=s.ceiling(real_budget)
            check(suite,M>=1 and M<=2*real_budget,"admissible rounding")
            # Raise each branch comparison to a positive integer power, avoiding floats.
            for j,prod in enumerate(V,1):
                check(suite,M**j*(prod/M)**ell <= (2*V[ell-1])**j,
                      "each branch obeys integer upper recovery bound")
            check(suite,M*(V[ell-1]/M)==V[ell-1],"own branch supplies lower bound")
    DETAILS[suite]={"families":len(families),"positive_product_cases":cases,
                    "zero_product_infima":"proved by the unbounded-budget argument in the report, not by a finite test"}


def dominated_margin() -> None:
    suite="dominated_margin_example"
    for c in [s.Rational(1,4),s.Rational(1,2),s.Integer(1)]:
        m=1-c
        H=s.Matrix([[1,m],[m,1]])
        eigen=H.eigenvals()
        check(suite,min(eigen)==c,"least singular value at the dominated extreme")
        weights=[(1+m)/2,(1-m)/2]
        check(suite,all(w>=c/2 for w in weights) and sum(weights)==1,"dominated witness")
    DETAILS[suite]={"exact_formula":"inf s_min([[1,m],[m,1]]) = c for |m| <= 1-c"}


def projective_jacobian() -> None:
    suite="projective_evidence_jacobian"
    for b in range(1,4):
        v=s.Matrix(s.symbols(f"v0:{b}")); m=s.Matrix(s.symbols(f"m0:{b}"))
        den=1+(m.T*v)[0]
        J=(v/den).jacobian(v)
        det=s.factor(J.det())
        check(suite,zero(det-den**(-b-1)),"projective Jacobian")
        check(suite,zero((den/s.Integer(2)**b)/det-den**(b+2)/s.Integer(2)**b),
              "unconditional transformed density exponent b+2")
    DETAILS[suite]={"dimensions":[1,2,3]}


def leja_volumes() -> None:
    suite="leja_collision_volume_checks"
    sets=[[0,0,0],[0,s.Rational(1,3),1],
          [s.Rational(1,10),s.Rational(1,10),s.Rational(1,5),s.Rational(9,10)],
          [0,s.Rational(1,100),s.Rational(2,100),s.Rational(1,2),1]]
    for nodes in sets:
        nodes=list(map(s.sympify,nodes)); remaining=list(range(len(nodes)))
        chosen=[]; d=[]
        while remaining:
            idx=max(remaining,key=lambda i:(s.prod(abs(nodes[i]-nodes[j]) for j in chosen),-i))
            d.append(s.prod(abs(nodes[idx]-nodes[j]) for j in chosen)); chosen.append(idx); remaining.remove(idx)
        check(suite,all(d[i]>=d[i+1] for i in range(len(d)-1)),"nonincreasing pivots")
        for ell in range(1,len(nodes)+1):
            volume=max(s.prod(abs(nodes[i]-nodes[j]) for i,j in it.combinations(sub,2))
                       for sub in it.combinations(range(len(nodes)),ell))
            p=s.prod(d[:ell])
            check(suite,p<=volume<=math.factorial(ell)*p,"maximal Vandermonde product bounds")
    DETAILS[suite]={"node_configurations":len(sets),"includes_exact_repetitions":True}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("INDEPENDENT_CHECK_RESULTS.json"))
    args=parser.parse_args(); start=time.perf_counter()
    functions=[kernel_example,pentagon,walsh,determinantal_orders,phase_envelopes,
               integer_envelope,dominated_margin,projective_jacobian,leja_volumes]
    try:
        for function in functions: function()
    except Exception as exc:
        print(f"FAILED: {exc}",file=sys.stderr)
        return 1
    payload={"reviewed_commit":PIN,"status":"passed","suite_count":len(COUNTS),
             "exact_check_count":sum(COUNTS.values()),"checks_by_suite":dict(COUNTS),
             "details":DETAILS,"python":platform.python_version(),"sympy":s.__version__,
             "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "elapsed_seconds":round(time.perf_counter()-start,3),
             "limits":["Finite diagnostics are not formal proof verification.",
                       "No author validator, preservation mutation, LaTeX build, or CI rerun was executed.",
                       "No numerical optimization over all encoders was performed.",
                       "The exact-kernel counterexample concerns prose scope, not the printed inclusion theorem."]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
