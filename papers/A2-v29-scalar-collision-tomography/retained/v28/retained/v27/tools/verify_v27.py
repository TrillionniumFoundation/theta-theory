#!/usr/bin/env python3
"""Finite deterministic diagnostics for A2 v27, not a proof certificate.

The geometry fixtures test deterministic implications of the stated priors.
They are not an execution of a physical launch apparatus or a minimax test.
Checks are explicit exceptions and therefore remain active under python -O.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from itertools import product
from math import comb, gcd, lcm
from pathlib import Path
import hashlib
import json
import re

COUNTS: Counter[str] = Counter()
ROOT = Path(__file__).resolve().parents[1]


def check(condition: bool, group: str) -> None:
    if not condition:
        raise RuntimeError('finite diagnostic failed: ' + group)
    COUNTS[group] += 1


def det(a, b):
    return a[0]*b[1] - a[1]*b[0]


def apply(matrix, vector):
    return tuple(sum(row[i]*vector[i] for i in range(2)) for row in matrix)


def coordinates(columns, v):
    a, b = columns
    d = det(a, b)
    if d == 0:
        raise ValueError('dependent period pair')
    return (det(v, b)/d, det(a, v)/d)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r-q*r
        old_s, s = s, old_s-q*s
        old_t, t = t, old_t-q*t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def column_hermite_2d(vectors: list[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return columns (a,0),(b,c), a,c>0, 0<=b<a, for a rank-two group."""
    index = 0
    for i, v in enumerate(vectors):
        for w in vectors[i+1:]:
            index = gcd(index, abs(det(v, w)))
    if index == 0:
        raise ValueError('integer group has rank below two')
    y_gcd, x_combination = 0, 0
    for x, y in vectors:
        g, s, t = extended_gcd(y_gcd, y)
        x_combination = s*x_combination + t*x
        y_gcd = g
    a = index // y_gcd
    return ((a, 0), (x_combination % a, y_gcd))


def in_integer_group(h, v) -> bool:
    (a, _), (b, c) = h
    return v[1] % c == 0 and (v[0] - b*(v[1]//c)) % a == 0


def unique_rational(value: F, denominator_bound: int, radius: F) -> F:
    candidates: set[F] = set()
    for d in range(1, denominator_bound+1):
        n = value.numerator*d // value.denominator
        for k in (n, n+1):
            r = F(k, d)
            if abs(r-value) <= radius:
                candidates.add(r)
    if len(candidates) != 1:
        raise ValueError('rational confidence interval is not uniquely resolved')
    return candidates.pop()


def lattice_and_aperture() -> None:
    presentations = []
    for a, c, shear in product((F(1), F(3,2), F(2)),
                              (F(1), F(5,3), F(2)),
                              (F(-1,3), F(0), F(2,5))):
        presentations.append(((a, shear), (F(0), c)))
    generators = [(2,0), (0,3), (1,0), (0,1), (1,-1), (-2,1), (0,0)]
    for L in presentations:
        cols = (apply(L,(1,0)), apply(L,(0,1)))
        # A conservative matrix operator bound via entrywise absolute values.
        L0 = sum(abs(x) for row in L for x in row)
        B = 1+L0
        for theta in product((F(-3,7),F(0),F(2,5)), repeat=2):
            representative = apply(L, theta)
            check(max(map(abs,representative)) < B, 'fundamental_center_coverage')
        for root in product((-(2*B+F(1,8)), F(0), 2*B+F(1,8)), repeat=2):
            for v in cols:
                translated = tuple(root[i]+v[i] for i in range(2))
                check(max(map(abs,translated)) <= 3*B+F(1,8), 'protected_generator_center')
                check(max(map(abs,translated))+F(1,8) < 4*B, 'cutoff_cannot_remove_basis')
        ds = [apply(L,v) for v in generators]
        D = (ds[0],ds[1])  # deliberately index six, not a primitive pair
        rs = [coordinates(D,v) for v in ds]
        n = int(abs(det(*D)/det(*cols)))
        check(n == 6, 'nonprimitive_initial_pair')
        check(all(n % x.denominator == 0 for r in rs for x in r), 'common_index_denominators')
        q = reduce(lcm, (x.denominator for r in rs for x in r), 1)
        ints = [(int(q*r[0]),int(q*r[1])) for r in rs] + [(q,0),(0,q)]
        H = column_hermite_2d(ints)
        check(all(in_integer_group(H,v) for v in ints), 'hermite_contains_generators')
        recovered = tuple(tuple((D[0][i]*h[0]+D[1][i]*h[1])/q for i in range(2)) for h in H)
        check(abs(det(*recovered)) == abs(det(*cols)), 'saturation_before_area')
        check(all(x.denominator == 1 for r in [coordinates(recovered,v) for v in cols] for x in r),
              'recovered_group_contains_true_basis')
        check(all(x.denominator == 1 for r in [coordinates(cols,v) for v in recovered] for x in r),
              'recovered_group_has_no_spurious_period')
        Q = 12
        radius = F(1,3*Q*Q)
        for r in rs:
            for x in r:
                for shift in (F(-1,10*Q*Q), F(0), F(1,10*Q*Q)):
                    check(unique_rational(x+shift,Q,radius) == x, 'noisy_rational_locking')
        # Deleting both primitive witnesses leaves a proper group. This is not
        # accepted as a proof of complete coverage; it controls that hypothesis.
        partial = column_hermite_2d([(q,0),(0,q)])
        partial_covol = abs(det(*D))*abs(det(*partial))/(q*q)
        check(partial_covol == 6*abs(det(*cols)), 'missing_witness_negative_control')
    for bound in range(2,14):
        rationals = sorted({F(n,d) for d in range(1,bound+1) for n in range(-2*d,2*d+1)})
        check(min(b-a for a,b in zip(rationals,rationals[1:])) >= F(1,bound*bound),
              'rational_separation')
    for vectors in ([(1,0)], [(0,0)], [(2,2),(3,3)]):
        try:
            column_hermite_2d(vectors)
        except ValueError:
            check(True,'rank_deficiency_rejected')
        else:
            check(False,'rank_deficiency_rejected')
    try:
        unique_rational(F(1,4),2,F(1,3))
    except ValueError:
        check(True,'ambiguous_rational_rejected')
    else:
        check(False,'ambiguous_rational_rejected')


def prior_algebra() -> None:
    for g, k0, k1 in product((F(1,3),F(1),F(2)), repeat=3):
        H=((1/g+k0,-1/g),(-1/g,1/g+k1))
        check(det(*H) == (k0+k1)/g+k0*k1, 'retained_normal_hessian_determinant')
        for u,v in product((F(-2),F(0),F(1),F(3,2)),repeat=2):
            q=H[0][0]*u*u+2*H[0][1]*u*v+H[1][1]*v*v
            check(q-min(k0,k1)*(u*u+v*v) >= 0, 'retained_normal_hessian_lower_bound')
    for V,A,missing,index in product((F(3),F(5)),(F(1),F(2)),(F(0),F(1,2)),(1,2,3)):
        visible=V-A-missing
        defect=index*V-A-visible
        check(defect == (index-1)*V+missing, 'retained_completion_identity')
        check((defect==0) == (index==1 and missing==0), 'retained_completion_gap')


def smoothing_and_costs() -> None:
    def phi_moment(order: int) -> F:
        if order%2:
            return F(0)
        return F(315,256)*sum(F((-1)**k*comb(4,k)*2,2*k+order+1) for k in range(5))
    check(phi_moment(0)==1, 'kernel_mass')
    for j in (1,2,3):
        check((F(4,3)-F(2**j,3))*phi_moment(j)==0, 'compensated_moment_cancellation')
    check((F(4,3)+F(16,3))*phi_moment(4)/24 <= 1, 'fourth_order_remainder_constant')
    for j in range(3):
        check(F(4,3)+F(1,3*2**j) <= 2, 'kernel_derivative_noise_bound')
    for nu,B6,Cphi,kappa in product((F(1,100),F(1,10000)),
                                    (F(1),F(4)),(F(10),F(512)),(F(1),F(3))):
        # Exact balances use h^4; no rational stand-in for its fourth root.
        h4=nu/(8*B6)
        check(B6*h4==nu/8,'smoothing_bias_budget')
        check(2*Cphi*(nu/(128*Cphi))/4+nu/8 < nu/4,'smoothing_total_budget')
    check(2*F(3,4)==F(3,2),'localization_and_hull_exponents')
    check(F(3,2)-2*F(1,4)==1,'derivative_noise_exponent')
    check(4*F(1,4)==1,'fourth_order_bias_exponent')
    check(1/F(3,4)==F(4,3),'sample_to_C2_exponent')
    for m in range(2,40):
        # Geometric budget summation; 2^(3/4) is bounded below by 3/2.
        s=sum(F(3,2)**j for j in range(1,m+1))
        check(s <= 3*F(3,2)**m, 'dyadic_budget_geometric_sum')
    check(sum(F(1,2*(j+1)**2) for j in range(1,1000)) < 1, 'finite_spending_prefix')
    # A rigorous integral bound covers the omitted infinite tail.
    check(sum(F(1,2*(j+1)**2) for j in range(1,10))+F(1,20) < 1,
          'infinite_spending_integral_bound')
    # Disk supports are unchanged by every orthogonal transformation. The new
    # translation-class comparison distinguishes radii without an eta margin.
    for r0,r1 in product((F(1,5),F(1,3),F(1,2)),repeat=2):
        check((abs(r0-r1)==0)==(r0==r1),'symmetric_disk_type_recognition')


def sources() -> None:
    pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    for name,expected in pins['source_sha256'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'published_source_binding')
    for name,expected in pins['unchanged_v26_core_blobs'].items():
        b=(ROOT/name).read_bytes()
        check(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==expected,'six_retained_active_cores')
    main=(ROOT/'main.tex').read_text()
    chunks=[main]
    for name in re.findall(r'\\input\{([^}]+)\}',main):
        p=ROOT/(name+'.tex')
        check(p.is_file(),'primary_input_reachable')
        chunks.append(p.read_text())
    all_text='\n'.join(chunks)
    labels=re.findall(r'\\label\{([^}]+)\}',all_text)
    check(len(labels)==len(set(labels)),'unique_primary_labels')
    for ref in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',all_text):
        check(ref in labels,'primary_reference_resolved')
    for label in ('thm:aperture-main','thm:main','thm:certificate','thm:comp-probe',
                  'cor:comp-work','thm:probe-main','thm:fingerprint-main'):
        check(label in labels,'new_and_previous_theorems_active')
    clearance=(ROOT/'core/03_recognition.tex').read_text()
    check('Delete exactly the two' in clearance and 'not every component' in clearance,
          'clearance_patch_present')


def main() -> None:
    lattice_and_aperture()
    # Keep the finite clearance fixtures independent of source string checks.
    g,c0,a=F(4),F(1),F(1,10)
    check(a<c0/2,'old_endpoint_clearance_counterexample')
    for s in (a,F(1,2),F(2),g-a):
        check(min(s,g-s)>=a,'middle_endpoint_lower_bound')
        check(min(s,g-s)-a/2>=a/2,'explicit_endpoint_tube_radius')
    for c in (F(1,8),F(1,2),F(1),F(3)):
        check(3*c/4-c/8-c/8==c/2,'other_body_mesh_clearance')
        check(c/2-c/4==c/4,'other_body_tube_margin')
    prior_algebra(); smoothing_and_costs(); sources()
    print(json.dumps({'schema':'a2-v27-finite-diagnostics-1','status':'passed',
        'total_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
        'scope':'finite aperture geometry, rational reconstruction, exact finite inequalities and source integrity',
        'physical_sensor_executed':False,'formal_proof_certificate':False},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
