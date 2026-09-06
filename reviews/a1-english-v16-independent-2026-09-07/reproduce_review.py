#!/usr/bin/env python3
"""Independent finite diagnostics for A1 v16. No author modules are imported.

Python 3.10+ standard library. Run:
  python3 reproduce_review.py --paper /path/to/papers/A1-english-v16 --output EXECUTION.json
The mathematical checks are exact rational calculations except the explicitly
labelled Fourier floating-point regressions. They are not proofs of uniform
analytic theorems. --paper checks pinned bytes and preservation in expanded.tex
when that optional, author-prepared file exists; it never changes paper files.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import cmath
import hashlib
import json
import math
import platform
import random
import re
import sys
import time

PIN = '9f6875ebf1473b84dcde2ccabcb1556202233276'
MANIFEST_BLOB = '56abcea02dc07ce483e0eb2c2182ebce31c4e48d'
PDF_SHA256 = '7e3bdfe801faa834a2a1da0cd771f5d0e68674a4b35c9f8d73d52c4dbf28b45d'
COUNTS: Counter[str] = Counter()


def check(condition: bool, suite: str, message: str) -> None:
    COUNTS[suite] += 1
    if not condition:
        raise AssertionError(f'{suite}: {message}')


def product(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    rr = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rr, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        scale = a[rr][col]
        a[rr] = [x / scale for x in a[rr]]
        for i in range(rr + 1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [x - scale*y for x, y in zip(a[i], a[rr])]
        rr += 1
        if rr == len(a):
            break
    return rr


def formal_nodes(a, m, H=F(12)):
    # Retain formal multiplicities, including equal numerical sums.
    return [sum(a[i] for i in word)/H
            for word in combinations_with_replacement(range(len(a)), m)
            if any(i != 0 for i in word)]


def leja(nodes):
    rest = list(enumerate(nodes))
    order, pivots = [], []
    while rest:
        if not order:
            index = 0
            val = F(1)
        else:
            values = [product(abs(x-y) for y in order) for _, x in rest]
            index = max(range(len(rest)), key=lambda i: values[i])
            val = values[index]
        _, node = rest.pop(index)
        order.append(node)
        pivots.append(val)
    return order, pivots


def leja_diagnostics():
    s = 'exact_leja_and_exterior_products'
    families = 0
    for theta in (F(0), F(1, 10), F(1, 100), F(1, 10000)):
        for a in ([F(0), F(1), F(2)+theta],
                  [F(0), F(1), F(2)+theta, F(3)+theta+theta*theta]):
            for m in (1, 2):
                nodes = formal_nodes(a, m)
                ordered, d = leja(nodes)
                families += 1
                check(all(d[j] >= d[j+1] for j in range(len(d)-1)), s,
                      'pivots must be nonincreasing on [0,1]')
                check(sum(x > 0 for x in d) == len(set(nodes)), s,
                      'exact collision rank')
                for ell in range(1, len(nodes)+1):
                    volume = max(product(abs(nodes[i]-nodes[j])
                                         for i, j in combinations(subset, 2))
                                 for subset in combinations(range(len(nodes)), ell))
                    pivot_product = product(d[:ell])
                    check(pivot_product <= volume <= math.factorial(ell)*pivot_product,
                          s, 'Vandermonde exterior product comparison')
    return {'parameter_families': families, 'arithmetic': 'fractions.Fraction'}


def normalized_tangent_diagnostics():
    s = 'exact_confluent_normalized_tangent'
    cases = 0
    for theta in (F(0), F(1, 100), F(1, 10000)):
        a = [F(0), F(1), F(2)+theta]
        D, H = a[-1], F(12)
        for n in (1, 2, 3):
            # Product of (1+c_i t^D); scalar 2^{-n} cancels in derivative rank.
            P = [F(1)]
            for i in range(n):
                c = F(i+1, 20)
                Q = [F(0)]*(len(P)+1)
                for j, coeff in enumerate(P):
                    Q[j] += coeff
                    Q[j+1] += c*coeff
                P = Q
            Z = sum(c/(1+j*D) for j, c in enumerate(P))
            B = sorted({j*D for j in range(n+1)} |
                       {a[1]+j*D for j in range(n)})
            nodes, _ = leja(formal_nodes(a, 2, H))
            p = min(2*n, len(nodes))
            # For the uniform probability on [0,1], exact divided difference:
            # integral t^b [x1,...,xj] t^(H x) dt
            # = (-H)^(j-1)/prod_i (b+H*x_i+1), also at repeated nodes.
            for order in (nodes, list(reversed(nodes))):
                def pairing(b, j):
                    return (-H)**(j-1)/product(b+H*x+1 for x in order[:j])
                moments = [sum(c*pairing(k*D, j) for k, c in enumerate(P))
                           for j in range(1, p+1)]
                J = [[pairing(b, j)/Z - moments[j-1]/((b+1)*Z*Z)
                      for b in B] for j in range(1, p+1)]
                check(len(B) == 2*n+1, s, 'true product-tangent dimension')
                for ell in range(1, p+1):
                    check(rank(J[:ell]) == ell, s,
                          'normalized complete flag rank, including exact repeats')
                cases += 1
    return {'cases': cases, 'arithmetic': 'exact rational integration',
            'prior': 'uniform on [0,1]', 'not_proved_by_samples':
            'arbitrary full-support priors or uniform bounds over compact parameter sets'}


def elementary(xs):
    e = [F(1)]
    for x in xs:
        e.append(F(0))
        for j in range(len(e)-1, 0, -1):
            e[j] += x*e[j-1]
    return e


def symmetric_diagnostics():
    s = 'exact_circular_limiting_jacobian'
    for n in range(1, 7):
        z = [F(i+1, 40*n) for i in range(n)]
        J = [[elementary(z[:i]+z[i+1:])[j-1] for i in range(n)]
             for j in range(1, n+1)]
        for k in range(1, n+1):
            check(rank(J[:k]) == k, s, 'complex coefficient differential prefix')
            # At this real tuple the real differential is diag(J,J).
            R = [row + [F(0)]*n for row in J[:k]] + \
                [[F(0)]*n + row for row in J[:k]]
            check(rank(R) == 2*k, s, 'real rank of complex coefficient map')
    return {'max_degree': 6, 'arithmetic': 'fractions.Fraction',
            'limitation': 'rank tests do not select or certify a uniform positive contrast interval'}


def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] = out.get(i+j, 0) + x*y
    return out


def laurent(zs, tau):
    p = {0: 1+0j}
    for z in zs:
        p = mul(p, {0: 1, 1: tau*z, -1: tau*z.conjugate()})
    return p


def circular_float_diagnostics():
    s = 'floating_circular_update_query_metric'
    rng = random.Random(20260907)
    errors = {'update': 0.0, 'query_metric': 0.0, 'one_one': 0.0}
    cases = 0
    for tau in (0.0, 1e-6, 1e-3, 0.03, 0.2, 0.5):
        for n in range(0, 6):
            zs = [complex(rng.uniform(-.15, .15), rng.uniform(-.15, .15))
                  for _ in range(n)]
            p = laurent(zs, tau)
            p0 = p[0].real
            check(p0 >= (1-tau)**n - 1e-13, s, 'Haar evidence lower bound')
            def Y(j):
                return tau**abs(j)*p.get(j, 0)/p0
            for z in (0.5+0j, -0.5+0j, 0.5j, -0.5j, .12-.09j):
                new = mul(p, {0: 1, 1: tau*z, -1: tau*z.conjugate()})
                den = 1+z*Y(1).conjugate()+z.conjugate()*Y(1)
                check(den.real >= 1-tau-1e-13, s, 'weighted transition denominator')
                for j in range(1, n+3):
                    actual = tau**j*new.get(j, 0)/new[0]
                    predicted = (Y(j)+tau*tau*z*Y(j-1)+z.conjugate()*Y(j+1))/den
                    err = abs(actual-predicted)
                    errors['update'] = max(errors['update'], err)
                    check(err < 2e-13, s, 'weighted recurrence against full Laurent convolution')
            zs2 = [complex(rng.uniform(-.15, .15), rng.uniform(-.15, .15))
                   for _ in range(n)]
            p2 = laurent(zs2, tau)
            rho = .01
            for m in range(1, 5):
                observed = 0.0
                for ell in range(2*m+1):
                    phi = 2*math.pi*ell/(2*m+1)
                    query = laurent([rho*cmath.exp(-1j*phi)]*m, tau)
                    q1 = mul(p, query).get(0, 0)/p[0]/2**m
                    q2 = mul(p2, query).get(0, 0)/p2[0]/2**m
                    observed += abs(q1-q2)**2/(2*m+1)
                target = 0.0
                for j in range(1, m+1):
                    B = sum(math.factorial(m)*rho**(j+2*h)*tau**(2*h)/
                            (math.factorial(j+h)*math.factorial(h)*math.factorial(m-j-2*h))
                            for h in range((m-j)//2+1))
                    dy = tau**j*(p.get(j, 0)/p[0]-p2.get(j, 0)/p2[0])
                    target += 2**(1-2*m)*B*B*abs(dy)**2
                err = abs(observed-target)
                errors['query_metric'] = max(errors['query_metric'], err)
                check(err < 2e-18, s, 'full physical query metric vs weighted Parseval')
                cases += 1
            z, zp = .13-.17j, -.12+.09j
            vals = [rho*tau*tau*((z-zp)*cmath.exp(2j*math.pi*ell/3)).real
                    for ell in range(3)]
            actual = sum(x*x for x in vals)/3
            target = .5*rho*rho*tau**4*abs(z-zp)**2
            errors['one_one'] = max(errors['one_one'], abs(actual-target))
            check(abs(actual-target) < 1e-18, s, 'v16 one-past/one-future illustration')
    return {'query_metric_cases': cases, 'seed': 20260907, 'max_absolute_errors': errors,
            'arithmetic': 'Python double-precision complex',
            'warning': 'absolute-error finite regressions; not relative accuracy at zero or a proof'}


def profile_diagnostics():
    s = 'exact_log_profile_and_phase_crossings'
    for k in range(1, 9):
        for neglogtau in (F(1, 10), F(1), F(10)):
            logs = [-2*j*neglogtau for j in range(1, k+1) for _ in range(2)]
            for logM in [F(0), F(1), F(3), F(100), F(10000)]:
                terms = [2*(sum(logs[:ell])-logM)/ell for ell in range(1, 2*k+1)]
                even = [terms[2*j-1] for j in range(1, k+1)]
                check(max(terms) == max(even), s, 'odd exterior orders are dominated')
                for j in range(1, k+1):
                    expected = -2*(j+1)*neglogtau-logM/j
                    check(even[j-1] == expected, s, 'paired contrast exponent')
            for j in range(1, k):
                logM = 2*j*(j+1)*neglogtau
                t1 = -2*(j+1)*neglogtau-logM/j
                t2 = -2*(j+2)*neglogtau-logM/(j+1)
                check(t1 == t2, s, 'adjacent branch crossing')
    return {'max_harmonic': 8, 'arithmetic': 'exact rational logarithmic exponents'}


def padd(a, b):
    out = dict(a)
    for j, x in b.items():
        out[j] = out.get(j, F(0))+x
    return {j: x for j, x in out.items() if x}


def scale(a, c):
    return {j: x*c for j, x in a.items()}


def integrate(a):
    return sum((x/F(j+1) for j, x in a.items()), F(0))


def prior_diagnostics():
    s = 'exact_nonconstant_history_prior_normalization'
    likelihood = mul({0: F(1, 3), 1: F(1, 3)}, {0: F(1, 4), 1: F(1, 2)})
    Z = integrate(likelihood)
    def nu(poly):
        return integrate(mul(likelihood, poly))/Z
    phi = [{1: F(1)}, {2: F(1)}]
    mean = [nu(x) for x in phi]
    cov = [[nu(mul(x, y))-mean[i]*mean[j] for j, y in enumerate(phi)]
           for i, x in enumerate(phi)]
    det = cov[0][0]*cov[1][1]-cov[0][1]*cov[1][0]
    check(det > 0, s, 'two-test posterior covariance is positive')
    v = [F(1, 3), -F(2, 5)]
    coeff = [(cov[1][1]*v[0]-cov[0][1]*v[1])/det,
             (cov[0][0]*v[1]-cov[1][0]*v[0])/det]
    f = {}
    for i in range(2):
        f = padd(f, scale(padd(phi[i], {0: -mean[i]}), coeff[i]))
    check(nu(f) == 0, s, 'posterior-centered dual')
    for i in range(2):
        check(nu(mul(phi[i], f)) == v[i], s, 'exact dual pairing')
    muf = integrate(f)
    check(muf != 0, s, 'nonconstant history detects missing prior normalization')
    eps = F(1, 10)
    K = max(F(1), sum(abs(x) for x in f.values()))
    step = eps/(4*K)
    density = scale(padd({0: F(1)}, scale(f, step)), 1/(1+step*muf))
    check(integrate(density) == 1, s, 'pulled-back prior integrates to one')
    check(2*step*K/(1-step*K) <= eps, s, 'relative-prior envelope bound')
    Znew = integrate(mul(likelihood, density))
    for i in range(2):
        newmean = integrate(mul(mul(likelihood, density), phi[i]))/Znew
        check(newmean-mean[i] == step*v[i], s, 'exact posterior displacement')
    return {'prior_mean_of_posterior_centered_dual': str(muf),
            'step': str(step), 'arithmetic': 'fractions.Fraction polynomial integration'}


def overlap_diagnostics():
    s = 'exact_common_name_overlap'
    L = mul({0: F(1, 3), 1: F(1, 3)}, {0: F(1, 4), 1: F(1, 2)})
    Z = integrate(L)
    nu = lambda p: integrate(mul(L, p))/Z
    f = {0: -F(1, 2), 1: F(1)}
    q = {0: F(1, 2), 1: F(1, 8)}
    epsilon = F(1, 20)
    dplus = padd({0: F(1)}, scale(f, epsilon))
    dminus = padd({0: F(1)}, scale(f, -epsilon))
    check(integrate(dplus) == integrate(dminus) == 1, s, 'two normalized priors')
    Zp, Zm = integrate(mul(L, dplus)), integrate(mul(L, dminus))
    check(Zp/Z == 1+epsilon*nu(f) and Zm/Z == 1-epsilon*nu(f), s,
          'actual evidence likelihood ratios')
    check(Zp != Zm and min(Zp/Z, Zm/Z) >= 1-epsilon, s,
          'history laws overlap but are not identical')
    qp = integrate(mul(mul(L, dplus), q))/Zp
    qm = integrate(mul(mul(L, dminus), q))/Zm
    gap = 2*epsilon*(nu(mul(q, f))-nu(q)*nu(f))/(1-epsilon**2*nu(f)**2)
    check(qp-qm == gap and gap > 0, s, 'posterior query gap identity')
    for degree in range(9):
        moment = {degree: F(1)}
        center = integrate(moment)
        check(abs(integrate(mul(dplus, moment))-center) <= epsilon and
              abs(integrate(mul(dminus, moment))-center) <= epsilon, s,
              'one common finite moment name')
    return {'posterior_query_gap': str(gap),
            'history_likelihood_ratios': [str(Zp/Z), str(Zm/Z)],
            'arithmetic': 'fractions.Fraction'}


def artifact_diagnostics(paper: Path):
    s = 'pinned_artifact_integrity'
    data = (paper/'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    check(blob == MANIFEST_BLOB, s, 'source manifest matches independently fetched Git blob')
    manifest = json.loads(data)['files']
    for rel, expected in manifest.items():
        check(hashlib.sha256((paper/rel).read_bytes()).hexdigest() == expected, s, rel)
    pdf_hash = hashlib.sha256((paper/'main.pdf').read_bytes()).hexdigest()
    check(pdf_hash == PDF_SHA256, s, 'PDF matches pinned receipt')
    preservation = {'checked': False}
    expanded = paper/'build/expanded.tex'
    if expanded.exists():
        text = expanded.read_text()
        old = json.loads((paper/'V15_PRESERVATION_MANIFEST.json').read_text())
        blocks = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', text, re.S)
        current = Counter(hashlib.sha256(x.encode()).hexdigest() for x in blocks)
        check(not (Counter(old['proof_sha256'])-current), s,
              'v15 complete proof blocks are included unchanged')
        # Match the same named environments, but compute hashes independently.
        named = re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}', text, re.S)
        statement_blocks = [m.group(0) for m in re.finditer(
            r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}', text, re.S)]
        current_s = Counter(hashlib.sha256(x.encode()).hexdigest() for x in statement_blocks)
        key = next((k for k in old if k in ('statement_sha256', 'statements_sha256')), None)
        if key is None:
            raise KeyError('V15 statement hash list is absent')
        check(not (Counter(old[key])-current_s), s, 'v15 complete statements are included unchanged')
        preservation = {'checked': True, 'v15_proof_blocks': len(old['proof_sha256']),
                        'v15_statement_blocks': len(old[key]), 'current_proof_blocks': len(blocks),
                        'current_statement_blocks': len(named),
                        'expanded_source_sha256': hashlib.sha256(expanded.read_bytes()).hexdigest(),
                        'note': 'Compares bytes in author-prepared expansion, not proof validity.'}
    return {'manifest_git_blob': blob, 'source_entries_checked': len(manifest),
            'pdf_sha256': pdf_hash, 'preservation': preservation}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper', type=Path, help='Optional local v16 directory for integrity checks')
    parser.add_argument('--output', type=Path, default=Path('EXECUTION.json'))
    args = parser.parse_args()
    start = time.monotonic()
    result = {'submission_commit': PIN, 'review_date': '2026-09-07',
              'python': platform.python_version(),
              'review_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'status': 'RUNNING', 'suites': {}}
    suites = [('leja', leja_diagnostics), ('confluent_tangent', normalized_tangent_diagnostics),
              ('circle_limiting_jacobian', symmetric_diagnostics),
              ('circle_physical_metric_and_update', circular_float_diagnostics),
              ('paired_profiles', profile_diagnostics), ('prior_pullback', prior_diagnostics),
              ('common_name_overlap', overlap_diagnostics)]
    try:
        if args.paper:
            result['suites']['artifact'] = artifact_diagnostics(args.paper)
        for name, function in suites:
            result['suites'][name] = function()
        result['status'] = 'PASS_WITH_STATED_SCOPE'
    except Exception as exc:
        result['status'] = 'FAIL'
        result['error'] = f'{type(exc).__name__}: {exc}'
    result['assertions_by_suite'] = dict(COUNTS)
    result['total_assertions'] = sum(COUNTS.values())
    result['elapsed_seconds'] = round(time.monotonic()-start, 3)
    result['limits'] = ['Finite regression checks are not proofs of analytic uniformity.',
                        'No author test suite was imported or rerun.',
                        'No TeX compilation is performed by this script.',
                        'No verification of every compiler/workspace appendix or journal importance is claimed.']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS_WITH_STATED_SCOPE' else 1


if __name__ == '__main__':
    sys.exit(main())
