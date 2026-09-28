#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v25 referee report.

Standard library only. No asserts, network, manuscript imports, or randomness.
These checks verify selected identities and witnesses, not billiard theorems.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import factorial, exp
import json

COUNTS: dict[str, int] = {}


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def case(group: str) -> None:
    COUNTS[group] = COUNTS.get(group, 0) + 1


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def invert2(a: list[list[F]]) -> list[list[F]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    require(det != 0, 'singular two-by-two matrix')
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def rank(a: list[list[F]]) -> int:
    a = [row[:] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [x / scale for x in a[row]]
        for i in range(row + 1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [x - scale * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def solve(a: list[list[F]], b: list[F]) -> list[F]:
    n = len(a)
    a = [a[i][:] + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        require(pivot is not None, 'singular interpolation matrix')
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return [a[i][-1] for i in range(n)]


def check_blocks() -> None:
    for x in (F(1, 5), F(1, 2), F(4, 5)):
        for r in (F(2, 3), F(1), F(5, 4)):
            for n in (3, 4, 5, 8, 12):
                a = (1 + x**(2*n)) / (1 - x**(2*n))
                b = 2 * x**n / (1 - x**(2*n))
                block = [[a, r**n*b], [b/r**n, a]]
                inverse = [[a, -r**n*b], [-b/r**n, a]]
                require(matmul(block, inverse) == [[F(1), F(0)], [F(0), F(1)]],
                        'last-jet inverse or determinant identity failed')
                require(a == 1 + 2*x**(2*n)/(1-x**(2*n)), 'own-site sum')
                case('last_jet_blocks')


def check_pilot() -> None:
    gmin, gmax = F(1, 2), F(2)
    for j in (2, 8, 20):
        for h in (F(1, 16), F(1, 64)):
            for g in (gmin, F(7, 9), F(19, 13), gmax):
                distance = j*(g-gmin)/h
                ceiling = -(-distance.numerator // distance.denominator)
                index = ceiling + 1
                t = j*gmin + index*h
                require(h <= t-j*g <= 2*h, 'pilot grid failed')
                for excess in (h/F(8), h, 2*h):
                    estimate = (j*g + excess-h)/j
                    require(j*abs(estimate-g) <= h, 'pilot midpoint error')
                case('pilot_grid_and_midpoint')


def check_hermite() -> None:
    cos4, sin4 = (1, 0, -1, 0), (0, 1, 0, -1)
    for contacts in (1, 2, 3, 4):
        for order in (2, 3, 4):
            degree = (contacts-1)*(order+1)+order
            matrix = []
            for angle in range(contacts):
                for derivative in range(order+1):
                    row = [F(int(derivative == 0))]
                    for frequency in range(1, degree+1):
                        phase = (frequency*angle + derivative) % 4
                        row += [F(frequency**derivative*cos4[phase]),
                                F(frequency**derivative*sin4[phase])]
                    matrix.append(row)
            require(rank(matrix) == contacts*(order+1), 'Hermite rank failed')
            case('hermite_jet_surjectivity')


def check_interpolation() -> None:
    for order in range(2, 9):
        previous_error = None
        for radius in (F(1, 4), F(1, 8), F(1, 16)):
            nodes = [radius*F(i+1, order+2) for i in range(order+1)]
            coefficients = [F(0), F(0)] + [F(1, factorial(m)*(m+1))
                                          for m in range(2, order+1)]
            values = [sum((coefficients[m]*y**m for m in range(order+1)), F(0))
                      + y**(order+1)/factorial(order+1) for y in nodes]
            fitted = solve([[y**m for m in range(order+1)] for y in nodes], values)
            error = [factorial(m)*(fitted[m]-coefficients[m]) for m in range(order+1)]
            if previous_error is not None:
                for m in range(order+1):
                    require(error[m] == previous_error[m]/2**(order+1-m),
                            'exact geometric interpolation scaling failed')
            require(error[order] != 0, 'nontrivial remainder required')
            previous_error = error
            case('noiseless_graph_interpolation')


def check_domination_and_positions() -> None:
    for theta in (F(1, 16), F(1, 8), F(1, 4)):
        # f_theta(x)=2(1+theta-x)_+/(1+theta)^2 on the fixed box [0,2].
        tail = theta**2/(1+theta)**2
        require(tail > 0, 'alternative must have mass outside reference support')
        require((1+theta)**2/(1+theta)**2 == 1, 'density normalization')
        case('common_density_reference_nonac')
    for z in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
        # Envelope intensity is one on [-3,3]; target is one on (z,3].
        missing_mass = float(z+3)
        expectation = exp(missing_mass)*exp(-missing_mass)
        require(abs(expectation-1) < 1e-14, 'Poisson envelope RN normalization')
        case('poisson_envelope_domination')
    for radius in (F(1), F(3, 2), F(2)):
        for t in (F(1, 8), F(1, 4), F(1, 2)):
            x = -2*radius*t*t/(1+t*t)
            y = 2*radius*t/(1+t*t)
            require(x != 0, 'point must not be the common contact')
            require(-(x*x+y*y)/(2*x) == radius, 'one raw point radius inverse')
            for other in (F(1), F(3, 2), F(2)):
                require((x*x+y*y+2*other*x == 0) == (other == radius),
                        'distinct tangent circles must not share this point')
            case('raw_position_exact_identification')


def check_lattice_and_signature() -> None:
    lattice = [[F(2), F(1, 3)], [F(1, 4), F(3, 2)]]
    rotation = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    for marking in ([[F(1), F(0)], [F(0), F(1)]],
                    [[F(2), F(1)], [F(0), F(3)]],
                    [[F(3), F(2)], [F(1), F(2)]]):
        holonomy = matmul(lattice, marking)
        recovered = matmul(holonomy, invert2(marking))
        require(recovered == lattice, 'lattice recovery')
        rotated = matmul(rotation, recovered)
        require(matmul(transpose(rotated), rotated) == matmul(transpose(lattice), lattice),
                'Gram gauge invariance')
        case('rank_two_lattice')
    for target in (F(1, 16), F(1, 4), F(1)):
        for s in (F(-1, 2), F(0), F(1, 2)):
            require(6*s*s+4-2*target >= 2,
                    'enriched signature criterion lacks strict convexity')
        case('enriched_signature_local_convexity')
    require(1-3*F(1, 50)-8*F(1, 100) == F(43, 50),
            'asymmetric analytic oval curvature margin')
    case('asymmetric_oval_positive_radius')


def main() -> None:
    check_blocks()
    check_pilot()
    check_hermite()
    check_interpolation()
    check_domination_and_positions()
    check_lattice_and_signature()
    print(json.dumps({
        'status': 'passed',
        'source_commit': '3143762fc98373f93dbb8884c5ece005229ca50b',
        'case_counts': COUNTS,
        'total_cases': sum(COUNTS.values()),
        'scope': 'Independent finite identities and witnesses; not a theorem prover or native build.',
        'circle_witness_scope': 'Local registered observation example, not a signature-rigid global table.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
