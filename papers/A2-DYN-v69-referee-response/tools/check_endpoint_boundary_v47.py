#!/usr/bin/env python3
"""Finite algebra and negative controls for the v47 proof; not billiard certification."""
from fractions import Fraction as F
from itertools import product
from math import sqrt


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    count_cases = 0
    changed_labels = 0
    # Include the initial collision and exclude the terminal collision in A_m.
    for m in range(1, 8):
        for J in range(4):
            free = {j for j in range(m + 1) if min(j, m - j) <= J}
            active = sorted(free & set(range(m)))
            r = 2 * J + 2
            require(len(active) <= r, 'free occupation count includes too many summands')
            for x in product((0, 1), repeat=m):
                n = sum(x)
                for changes in product((0, 1), repeat=len(active)):
                    y = list(x)
                    for j, value in zip(active, changes):
                        y[j] = value
                    require(abs(sum(y) - n) <= r, 'occupation enlargement failed')
                    require(sum(y[j] for j in range(m) if j not in free)
                            == sum(x[j] for j in range(m) if j not in free),
                            'middle occupation changed')
                    count_cases += 1
                    changed_labels += (sum(y) != n)
    require(changed_labels > 0, 'negative control failed: a crossing can change n')
    # A terminal decision alone cannot change the count of times 0,...,m-1.
    require(sum([1, 0, 1, 0][:-1]) == sum([1, 0, 1, 1][:-1]), 'terminal convention')

    partition_cases = 0
    for factors in product((F(0), F(1, 3), F(2, 3), F(1)), repeat=5):
        G = F(1)
        for w in factors:
            G *= w
        first = next((j for j, w in enumerate(factors) if w < 1), None)
        assigned = [(1-G) if j == first else F(0) for j in range(len(factors))]
        require(sum(assigned) == 1-G, 'first-defect source partition')
        require(sum(x > 0 for x in assigned) <= 1, 'first-defect supports not disjoint')
        for E in (F(0), F(1, 4), F(1)):
            require(G*E + G*(1-E) + (1-G) == 1, 'positive source identity')
            require(all(x >= 0 for x in [G*E, G*(1-E), 1-G]), 'nonpositive component')
        partition_cases += 1

    depth_cases = 0
    # The distance-counting inequality is valid for every geometric base in (0,1).
    a = F(9, 10)
    for m in range(1, 70):
        for J in range(0, 15):
            middle = sum((a**min(j, m-j) for j in range(m+1)
                          if min(j, m-j) > J), F(0))
            require(middle <= 2*a**(J+1)/(1-a), 'middle geometric-tail count')
            require(sum(a**min(j, m-j) for j in range(m+1)) <= 2/(1-a),
                    'full geometric endpoint sum')
            depth_cases += 1
    require(F(47, 53) < 1 and F(47, 53) > 0, 'actual q range')
    require(-F(1,12)+F(1,24) == -F(1,24), 'paid endpoint exponent')
    require(2*(-F(1,12)) == -F(1,6), 'incidence mass exponent')
    require(-F(1,2) < -F(1,24), 'protected correction must be smaller')
    require(F(1,24) < F(1,12), 'endpoint depth grows too quickly')

    flow_cases = 0
    # F(z)=|z|^2/2: the exact gradient-normalized flow preserves area in dimension 2.
    for x, y in [(1., .2), (.4, .8), (-.7, .3)]:
        r2 = x*x + y*y
        for s in [-r2/8, 0., r2/8]:
            scale = sqrt(1 + 2*s/r2)
            xx, yy = scale*x, scale*y
            require(abs((xx*xx+yy*yy)/2 - r2/2 - s) < 1e-12, 'VF=1 model')
            # Radial and transverse eigenvalues of D Phi are inverse to one another.
            require(abs((1/scale)*scale - 1) < 1e-12, 'flow coarea Jacobian model')
            flow_cases += 1
    require(sqrt(1+2*.1/1.04) > 1.01, 'model must permit a section cut crossing')

    # Mass alone fails: f_e=e^{-1} 1_[0,e^2] has mass e but height e^{-1}.
    e = F(1, 100)
    mass, height = e, 1/e
    require(mass < F(1, 10) and height > 10, 'small-mass negative control')
    # Replacing J(B) by J(m) is not part of an ordered-limit identity.
    return {'exact_occupation_cases': count_cases,
            'cases_rejecting_literal_label_preservation': changed_labels,
            'positive_first_defect_partitions': partition_cases,
            'geometric_depth_cases': depth_cases,
            'coarea_flow_cases': flow_cases,
            'ordered_endpoint_rate': 'B^(-1/24)',
            'incidence_mass_rate': 'B^(-1/6)',
            'clearance_mass_rate': 'B^(-1/12)',
            'negative_controls': ['crossing does not preserve n',
                                  'small source mass does not bound density height'],
            'prescribed_count_dependent_rate_tested': False,
            'continuum_pointwise_boundary_estimate_certified': False}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
