#!/usr/bin/env python3
"""Independent exact-rational diagnostics for A1 v23, not a proof certificate.
No author implementation or external dependencies are imported. Run normally and
with python -O. Only the requested output JSON is written. Explicit exceptions,
not assert statements, implement the checks. The uniform-prior Mellin formula
makes the Newton/Hermite computations exact even at repeated exponent nodes.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
from pathlib import Path
from math import factorial
import hashlib
import json
import sys

COUNTS: Counter[str] = Counter()
CASES: Counter[str] = Counter()

def check(ok: bool, group: str) -> None:
    COUNTS[group] += 1
    if not ok:
        raise RuntimeError('Failed diagnostic: ' + group)

def prod(xs):
    z = F(1)
    for x in xs:
        z *= x
    return z

def rank(rows) -> int:
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    i = 0
    for j in range(len(a[0])):
        pivot = next((k for k in range(i, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[i], a[pivot] = a[pivot], a[i]
        c = a[i][j]
        a[i] = [v/c for v in a[i]]
        for k in range(i+1, len(a)):
            c = a[k][j]
            if c:
                a[k] = [x-c*y for x,y in zip(a[k], a[i])]
        i += 1
        if i == len(a):
            break
    return i

def multiply(a, b):
    out = {}
    for e,c in a.items():
        for f,d in b.items():
            out[e+f] = out.get(e+f,F(0)) + c*d
    return {e:c for e,c in out.items() if c}

def polynomial_product(factors):
    out = {F(0):F(1)}
    for f in factors:
        out = multiply(out,f)
    return out

def moment(poly):
    return sum((c/(e+1) for e,c in poly.items()),F(0))

def newton_moment(poly, nodes):
    # Integral_0^1 t^e [b1,...,bj](b -> t^b) dt
    # = (-1)^(j-1) / product(e+1+bi), including Hermite nodes.
    return sum((c * (-1)**(len(nodes)-1) / prod(e+1+b for b in nodes)
                for e,c in poly.items()),F(0))

def formal_nodes(A, m):
    return sorted(sum((A[i] for i in w),F(0))
                  for w in combinations_with_replacement(range(len(A)),m)
                  if any(w))

def leja(nodes):
    remaining = list(enumerate(nodes))
    first = min(remaining,key=lambda t:(t[1],t[0]))
    remaining.remove(first)
    chosen = [first[1]]
    scales = [F(1)]
    while remaining:
        pivot = max(remaining,key=lambda t:(prod(abs(t[1]-x) for x in chosen),-t[0]))
        scales.append(prod(abs(pivot[1]-x) for x in chosen))
        chosen.append(pivot[1])
        remaining.remove(pivot)
    return chosen,scales

def volume(nodes,j):
    return max((prod(abs(a-b) for a,b in combinations(J,2))
                for J in combinations(nodes,j)),default=F(0))

def test_leja(nodes):
    # H=32 keeps all pair distances <=1 in these fixed-horizon cases.
    x = [b/F(32) for b in nodes]
    ordered,d = leja(x)
    s = len(set(x))
    q = len(x)
    check(all(d[i]>=d[i+1] for i in range(q-1)), 'leja_monotonicity')
    check(sum(v>0 for v in d)==s,'zero_pivot_rank')
    L = [[prod(ordered[i]-ordered[h] for h in range(j))/d[j] if d[j] else F(0)
          for j in range(q)] for i in range(q)]
    check(all(abs(v)<=1 for row in L for v in row),'bounded_triangular_entries')
    check(all(abs(L[i][i])==1 for i in range(s)),'triangular_diagonal')
    check(rank([row[:s] for row in L[:s]])==s,'triangular_rank')
    for j in range(1,q+1):
        v = volume(x,j)
        t = prod(d[:j])
        check(t<=v<=factorial(j)*t,'maximal_vandermonde_comparison')
    # Scalar reciprocal is an exact test of the Newton identity.
    for c in (F(1),F(3,2),F(4)):
        gj = [(-1)**j/prod(c+b for b in ordered[:j+1]) for j in range(q)]
        for i,b in enumerate(ordered):
            check(sum((L[i][j]*d[j]*gj[j] for j in range(q)),F(0))==1/(c+b),
                  'newton_identity_including_repeats')
    CASES['node_multisets'] += 1

def test_acquired(A,n,m):
    nodes = formal_nodes(A,m)
    p = min(n*(len(A)-1),len(nodes))
    D = A[-1]
    factors = [{F(0):F(1), D:F(i+1,64)} for i in range(n)]
    P = polynomial_product(factors)
    Q = []
    for i in range(n):
        omitted = polynomial_product(factors[:i]+factors[i+1:])
        for a in A:
            Q.append({e+a:c for e,c in omitted.items()})
    exponents = sorted(set().union(*(q.keys() for q in Q)))
    check(rank([[q.get(e,F(0)) for q in Q] for e in exponents])==n*(len(A)-1)+1,
          'binomial_product_tangent_rank')
    greedy,_ = leja(nodes)
    orders = [nodes,list(reversed(nodes)),greedy,nodes[1:]+nodes[:1]]
    Z = moment(P)
    for ordering in orders:
        unnormalized = [[moment(q) for q in Q]]
        jac = []
        for j in range(1,p+1):
            prefix = ordering[:j]
            value = newton_moment(P,prefix)
            row = [newton_moment(q,prefix) for q in Q]
            unnormalized.append(row)
            jac.append([(v*Z-value*moment(q))/(Z*Z) for v,q in zip(row,Q)])
        check(rank(unnormalized)==p+1,'confluent_mixed_pairing_rank')
        check(rank(jac)==p,'normalized_prefix_surjectivity')
        for j in range(1,p+1):
            # Vary the whole product in its own scalar direction: derivative zero.
            v = newton_moment(P,ordering[:j])
            check((v*Z-v*moment(P))==0,'evidence_scaling_kernel')
        CASES['acquisition_orderings'] += 1
    # Ordinary raw moments lose rank at collisions, unlike unscaled Hermite tests.
    raw = []
    for b in nodes:
        v = moment({e+b:c for e,c in P.items()})
        raw.append([(moment({e+b:c for e,c in q.items()})*Z-v*moment(q))/(Z*Z) for q in Q])
    check(rank(raw)==min(n*(len(A)-1),len(set(nodes))),'raw_acquired_dimension')
    CASES['acquisition_models'] += 1

def algebra_case(weights, attenuation):
    d = len(attenuation)
    f = [[F(0)]*d] + [[attenuation[i] if i==j else F(0) for j in range(d)] for i in range(d)]
    mean = [sum((w*row[i] for w,row in zip(weights,f)),F(0)) for i in range(d)]
    second = [[sum((w*row[i]*row[j] for w,row in zip(weights,f)),F(0))
               for j in range(d)] for i in range(d)]
    cov = [[second[i][j]-mean[i]*mean[j] for j in range(d)] for i in range(d)]
    support = {tuple(row) for w,row in zip(weights,f) if w}
    check(rank(cov)==len(support)-1,'covariance_observable_support_rank')
    commands = [[F((-1)**(i+j)*(j+1),64*d) for j in range(d)] for i in range(3)]
    all_word_mass = F(0)
    for signs in product((-1,1),repeat=3):
        a,b = F(1),[F(0)]*d
        direct = list(weights)
        v = mean[:]
        for t,(u,y) in enumerate(zip(commands,signs),1):
            z = [y*x for x in u]
            # Indicator-algebra rule f_i f_j = delta_ij tau_i f_i.
            b = [a*z[i]+b[i]+b[i]*z[i]*attenuation[i] for i in range(d)]
            Z = a+sum((b[i]*mean[i] for i in range(d)),F(0))
            chart = [mean[i]+sum((cov[i][j]*b[j] for j in range(d)),F(0))/Z for i in range(d)]
            direct = [w*(1+sum((z[i]*row[i] for i in range(d)),F(0)))
                      for w,row in zip(direct,f)]
            evidence = sum(direct,F(0))
            actual = [sum((w*row[i] for w,row in zip(direct,f)),F(0))/evidence for i in range(d)]
            den = 1+sum((z[i]*v[i] for i in range(d)),F(0))
            v = [(v[i]+z[i]*attenuation[i]*v[i])/den for i in range(d)]
            check(Z==evidence,'algebra_evidence_identity')
            check(chart==actual==v,'algebra_chart_raw_bayes_update')
            check(F(3,4)**t<=Z<=F(5,4)**t,'positive_evidence_bound')
            delta = F(1,4*d)
            s = 4-t
            p0 = F(1,2)**s
            preds = [p0]+[p0*(1+delta*x) for x in v]
            prior_preds = [p0]+[p0*(1+delta*x) for x in mean]
            loss = sum(((x-z)**2 for x,z in zip(preds,prior_preds)),F(0))/F(d+1)
            expected = p0*p0*delta*delta*sum(((x-z)**2 for x,z in zip(v,mean)),F(0))/F(d+1)
            check(loss==expected,'physical_query_squared_metric')
            CASES['algebra_prefixes'] += 1
        all_word_mass += evidence/F(8)
        CASES['algebra_histories'] += 1
    check(all_word_mass==1,'unconditional_word_probability_partition')
    CASES['algebra_models'] += 1

def misc():
    # Deliberately incorrect alternative formulas must differ on explicit cases.
    p,tau,u = F(1,3),F(1,2),F(1,8)
    m=tau*p
    sigma=tau*tau*p*(1-p)
    dv=sigma*u/(1+m*u)
    actual=tau*p*(1+u*tau)/(1+u*m)-m
    check(actual==dv,'scalar_normalized_posterior')
    check(actual!=sigma*u,'negative_control_omitted_normalization')
    check(sigma!=tau*p*(1-p),'negative_control_wrong_covariance_scale')
    check(sigma!=tau*tau*p,'negative_control_second_moment')
    check((1+u*m)/2!=1,'negative_control_conditioned_report_word')
    losses=((0,1),(1,0))
    im=min(max(row) for row in losses)
    mi=max(min(row[j] for row in losses) for j in range(2))
    check(im==1 and mi==0,'negative_control_infimum_maximum_interchange')
    # The introduction example has 5 raw positive directions but acquisition cap 2.
    nodes=formal_nodes([F(0),F(1),F(3)],2)
    check(len(set(nodes))==5 and min(2,len(nodes))==2,'introduction_dimension_truncation')
    # Exact exponent arithmetic for the two-parameter phase transitions.
    for k in range(2,9):
        for B,expected in ((F(6),F(2)),(F(8*k-2),F(2*k))):
            exps=(B/F(3),F(1,2)+B/F(4),F(4+2*k,9)+2*B/F(9))
            check(min(exps)==expected,'two_parameter_crossover_exponents')
        CASES['tangent_contact_orders']+=1
    # Integer inverse witnesses, checked without extracting irrational roots.
    for lam in ((F(1),F(1,2),F(1,8)),(F(1,3),F(1,3),F(0)),
                (F(1,1024),F(1,4096),F(1,65536)),(F(1),F(0),F(0))):
        for ell,x in enumerate(lam,1):
            if not x:
                continue
            Vl=prod(lam[:ell]); M0=Vl/x**ell
            check(M0>=1,'integer_inverse_witness_at_least_one')
            for j in range(1,len(lam)+1):
                check(prod(lam[:j])<=M0*x**j,'all_inverse_branches')
            Mc=(M0.numerator+M0.denominator-1)//M0.denominator
            check(Mc<=2*M0,'integer_inverse_rounding')
    # Recurrence expands the previous errors, rather than replacing by last error.
    q=[F(1,4),F(1,16),F(1,64)]; L=F(3,2); e=F(0)
    for n,x in enumerate(q,1):
        e=L*e+x
        check(e==sum((L**(n-j)*q[j-1] for j in range(1,n+1)),F(0)),
              'causal_accumulation_identity')
    check(e!=q[-1],'negative_control_last_stage_only')

def main():
    alphabets = [[F(0),F(1),F(2)+eps] for eps in
                 (F(0),F(1,64),F(-1,64),F(1,1024),F(1))]
    for A in alphabets:
        for m in (1,2):
            test_leja(formal_nodes(A,m))
            for n in (1,2,3):
                test_acquired(A,n,m)
    for u,v in ((F(0),F(0)),(F(0),F(1,64)),(F(1,64),F(1,64)),
                (F(1,64),F(1,32)),(F(1,64),F(3,64)),
                (F(1,64),F(1,64)+F(1,4096))):
        A=[F(0),F(1),F(2)+u,F(3)+v]
        nodes=formal_nodes(A,2)
        test_leja(nodes)
        test_acquired(A,3,2)
        rho=max(abs(u),abs(v)); small=min(abs(u),abs(v-u),abs(v-2*u))
        expected=6 if rho==0 else 8 if small==0 else 9
        check(len(set(nodes))==expected,'two_parameter_collision_stratum_rank')
        CASES['two_parameter_calibrations']+=1
    priors=[(F(1,3),)*3,(F(0),F(1,2),F(1,2)),(F(1),F(0),F(0)),
            (F(1,2),F(0),F(1,2)),(F(1,1024),F(1,2),F(511,1024))]
    for weights in priors:
        for tau in ((F(1),F(1)),(F(1),F(1,8)),(F(0),F(1)),(F(0),F(0)),
                    (F(1,1024),F(1,4096))):
            algebra_case(weights,tau)
    misc()
    result={
        'status':'passed',
        'reviewed_commit':'e7c1111d0ab8fb39e4b213902186db2cdf6d0dea',
        'arithmetic':'fractions.Fraction; exact, no floating-point tolerances',
        'imports_author_code':False,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'total_checks':sum(COUNTS.values()),
        'checks_by_group':dict(sorted(COUNTS.items())),
        'cases':dict(sorted(CASES.items())),
        'limitations':[
            'Finite examples do not prove parameter-uniform constants or mass domination.',
            'Uniform-prior monomial calculations do not test all full-support priors.',
            'Indicator-algebra calculations do not exhaust redundant coefficient representations.',
            'No optimal quantizer, global semialgebraic cover, or causal minimax infimum is computed.',
            'No author test suite, source-manifest verification, or PDF build is performed by this script.'
        ]}
    payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>2:
        raise SystemExit('Usage: independent_diagnostics.py [output.json]')
    if len(sys.argv)==2:
        Path(sys.argv[1]).write_text(payload,encoding='utf-8')
    print(payload,end='')

if __name__=='__main__':
    main()
