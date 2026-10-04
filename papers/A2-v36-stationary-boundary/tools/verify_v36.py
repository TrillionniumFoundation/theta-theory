#!/usr/bin/env python3
"""Deterministic finite diagnostics for the A2 v36 manuscript.

These checks exercise finite examples of the displayed constructions.  They
are not proofs, proof certificates, statistical simulations, or substitutes
for the hypotheses and arguments in the manuscript.  In particular, the
finite launch measures below check pointwise geometry; they do not estimate
a continuous launch density or certify a uniform cap-mass constant.

Only the Python standard library is used.  Every check remains active with
``python -O``.  Success and failure each emit exactly one JSON object, and
failure has a nonzero exit status.
"""

from fractions import Fraction as F
from math import gcd, isqrt, log2
import json
import sys


class DiagnosticFailure(RuntimeError):
    """A finite diagnostic failed."""


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, message):
        self.count += 1
        if not condition:
            raise DiagnosticFailure(message)


E = ((F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1)))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def mul(a, x):
    return (a * x[0], a * x[1])


def dot(x, y):
    return x[0] * y[0] + x[1] * y[1]


def rotate_rational(n, q):
    """An exact rational rotation, with angle 2 arctan(q)."""
    denominator = 1 + q * q
    return (
        ((1 - q * q) * n[0] - 2 * q * n[1]) / denominator,
        (2 * q * n[0] + (1 - q * q) * n[1]) / denominator,
    )


def candidates(n_hat):
    """V(n_hat/|n_hat|), compared exactly without irrational square roots."""
    values = [dot(n_hat, v) for v in E]
    maximum = max(values)
    norm_squared = dot(n_hat, n_hat)
    # maximum - value is nonnegative, so squaring is equivalent to
    # maximum - value <= |n_hat| / 4, including the equality case.
    return tuple(v for v, value in zip(E, values)
                 if 16 * (maximum - value) ** 2 <= norm_squared)


def compass_geometry(checks):
    primitive = set()
    for x in range(-12, 13):
        for y in range(-12, 13):
            if x or y:
                divisor = gcd(abs(x), abs(y))
                primitive.add((F(x // divisor), F(y // divisor)))
    normal_pairs = 0
    tied_pairs = 0
    two_candidate_pairs = 0
    for n in sorted(primitive):
        true_maximum = max(dot(n, v) for v in E)
        maximizers = tuple(v for v in E if dot(n, v) == true_maximum)
        for q in (F(-1, 64), F(-1, 128), F(0), F(1, 128), F(1, 64)):
            n_hat = rotate_rational(n, q)
            chosen = candidates(n_hat)
            normal_pairs += 1
            tied_pairs += int(len(maximizers) == 2)
            two_candidate_pairs += int(len(chosen) == 2)
            # The squared distance between normalized normals is <= 1/1024
            # iff their cosine is >= 2047/2048.  Both sides are positive.
            inner = dot(n, n_hat)
            checks.require(
                inner > 0 and inner ** 2 >= F(2047, 2048) ** 2
                * dot(n, n) * dot(n_hat, n_hat),
                "the coarse-normal example exceeds the 1/32 error reserve",
            )
            checks.require(1 <= len(chosen) <= 2,
                           "a compass candidate set has an invalid size")
            checks.require(all(v in chosen for v in maximizers),
                           "a true normal maximizer, including a tie, was lost")
            for v in chosen:
                projection = dot(n, v)
                checks.require(projection > 0 and 64 * projection ** 2
                               > 9 * dot(n, n),
                               "a candidate violates n dot v > 3/8")
    checks.require(tied_pairs > 0 and two_candidate_pairs > 0,
                   "the normal examples did not exercise ties and AND pairs")
    return {
        "arithmetic": "exact rational comparisons of normalized directions",
        "normal_pairs": normal_pairs,
        "tied_maximizer_pairs": tied_pairs,
        "two_candidate_pairs": two_candidate_pairs,
    }


def segment_hits_disk(start, displacement, center, radius):
    """The free-start collision bit for a closed disk, using exact algebra."""
    relative = sub(start, center)
    if dot(relative, relative) <= radius ** 2:
        return False  # The physical convention returns zero from a solid start.
    squared_length = dot(displacement, displacement)
    if not squared_length:
        return False
    parameter = max(F(0), min(F(1), -dot(relative, displacement) / squared_length))
    closest = add(relative, mul(parameter, displacement))
    return dot(closest, closest) <= radius ** 2


def rational_unit_normals():
    normals = set(E)
    for x, y, radius in ((3, 4, 5), (5, 12, 13), (119, 120, 169)):
        for first, second in ((x, y), (y, x)):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    normals.add((F(sx * first, radius), F(sy * second, radius)))
    return tuple(sorted(normals))


def disk_detector(checks):
    normals = rational_unit_normals()
    obstacle_center, footprint_center = (F(2, 5), F(-1, 7)), (F(1, 3), F(1, 5))
    obstacle_radius, footprint_radius, step = F(4), F(1), F(1, 2)
    offsets = {footprint_center}
    for n in normals:
        for radial in (F(1, 2), F(31, 32), F(255, 256)):
            offsets.add(add(footprint_center, mul(radial, n)))
    offsets = tuple(sorted(offsets))
    weights = tuple(F(1 + (index % 7)) for index in range(len(offsets)))
    normalizer = sum(weights)
    weights = tuple(weight / normalizer for weight in weights)
    checks.require(sum(weights) == 1, "finite launch weights do not sum to one")
    checks.require(all(dot(sub(z, footprint_center), sub(z, footprint_center))
                       < footprint_radius ** 2 for z in offsets),
                   "a finite launch node is not strictly inside its footprint")
    interior_cases = exterior_cases = shifted_centers = segment_tests = 0
    exterior_positive_alternatives = 0
    minimum_positive_occupation = F(1)
    maximum_gap_distance = F(0)
    for n in normals:
        checks.require(dot(n, n) == 1, "a disk normal is not a unit vector")
        for q in (F(-1, 64), F(0), F(1, 64)):
            chosen = candidates(rotate_rational(n, q))
            maximizers = tuple(v for v in E if dot(n, v) == max(dot(n, w) for w in E))
            for depth in (F(-1, 32), F(-1, 128), F(1, 128), F(1, 64), F(1, 32)):
                y = add(sub(obstacle_center, footprint_center),
                        mul(obstacle_radius + footprint_radius - depth, n))
                contact = add(obstacle_center, mul(obstacle_radius, n))
                occupancy = sum(weight for z, weight in zip(offsets, weights)
                                if dot(sub(add(y, z), obstacle_center),
                                       sub(add(y, z), obstacle_center)) <= obstacle_radius ** 2)
                pooled = {}
                for v in chosen:
                    shifted_centers += 1
                    nominal = add(y, mul(step, v))
                    collision_weight = F(0)
                    for z, weight in zip(offsets, weights):
                        start = add(nominal, z)
                        checks.require(dot(sub(start, obstacle_center), sub(start, obstacle_center))
                                       > obstacle_radius ** 2,
                                       "a shifted candidate has a nonfree start")
                        endpoint_occupied = dot(sub(add(y, z), obstacle_center),
                                                sub(add(y, z), obstacle_center)) <= obstacle_radius ** 2
                        reverse_hit = segment_hits_disk(start, mul(-step, v),
                                                        obstacle_center, obstacle_radius)
                        checks.require(not endpoint_occupied or reverse_hit,
                                       "an occupied endpoint did not give the required collision")
                        for w in E:
                            segment_tests += 1
                            displacement = mul(step, w)
                            collision_weight += weight * int(segment_hits_disk(
                                start, displacement, obstacle_center, obstacle_radius)) / 4
                            # This is the deterministic distance used to exclude other
                            # components under 2t + diam(K) < d0.  A segment is in
                            # the same ball as its endpoints by convexity.
                            for point in (start, add(start, displacement)):
                                distance_squared = dot(sub(point, contact), sub(point, contact))
                                maximum_gap_distance = max(maximum_gap_distance, distance_squared)
                                checks.require(distance_squared <=
                                               (2 * footprint_radius + 2 * step + abs(depth)) ** 2,
                                               "a shifted segment exceeds the component-exclusion ball")
                    pooled[v] = collision_weight
                if depth < 0:
                    exterior_cases += 1
                    checks.require(occupancy == 0,
                                   "a point outside the expanded disk has positive occupation")
                    checks.require(all(pooled[v] == 0 for v in maximizers),
                                   "a true maximizing exterior candidate has a collision")
                    checks.require(any(value == 0 for value in pooled.values()),
                                   "the exterior AND has no deterministic zero candidate")
                    exterior_positive_alternatives += int(any(value > 0 for value in pooled.values()))
                else:
                    interior_cases += 1
                    checks.require(occupancy > 0,
                                   "interior examples fail to exercise a positive endpoint mass")
                    minimum_positive_occupation = min(minimum_positive_occupation, occupancy)
                    checks.require(all(value >= occupancy / 4 for value in pooled.values()),
                                   "an interior pooled probability is below endpoint occupancy / 4")
    checks.require(exterior_positive_alternatives > 0,
                   "the disk examples do not exercise the need for an AND")
    checks.require(2 * footprint_radius + 2 * step + F(1, 32) < 6,
                   "the example has no fixed component-exclusion margin")
    return {
        "arithmetic": "exact rational closest-point segment/disk intersection",
        "exterior_cases": exterior_cases,
        "exterior_cases_with_positive_nonmaximizing_candidate": exterior_positive_alternatives,
        "interior_cases": interior_cases,
        "launch_nodes": len(offsets),
        "minimum_positive_endpoint_occupation": str(minimum_positive_occupation),
        "segment_tests": segment_tests,
        "shifted_centers": shifted_centers,
        "scope": "Finite asymmetric launch weights check geometric implications only; no density or cap-mass approximation.",
    }


def solve_fraction(matrix, rhs):
    """Small exact linear solver; a missing pivot is an explicit failure."""
    count = len(rhs)
    augmented = [list(row) + [rhs[index]] for index, row in enumerate(matrix)]
    for column in range(count):
        pivot = next((row for row in range(column, count) if augmented[row][column]), None)
        if pivot is None:
            raise DiagnosticFailure("the killed Green system is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(count):
            if row != column and augmented[row][column]:
                factor = augmented[row][column]
                augmented[row] = [value - factor * target
                                  for value, target in zip(augmented[row], augmented[column])]
    return [row[-1] for row in augmented]


def matvec(matrix, vector):
    return [sum(value * coordinate for value, coordinate in zip(row, vector)) for row in matrix]


def green_area_identity(checks):
    domain = sorted((x, y) for x in range(-1, 5) for y in range(-1, 5)
                    if not (x >= 3 and y >= 3) and (x, y) not in ((-1, 4), (4, -1)))
    positions = {point: index for index, point in enumerate(domain)}
    solid = {(1, 1), (1, 2), (2, 1), (2, 2)}
    laws = (
        (((0, 0), F(1)),),
        (((0, 0), F(1, 6)), ((1, 0), F(1, 3)), ((0, 1), F(1, 2))),
        (((0, 0), F(1, 10)), ((1, 0), F(2, 10)),
         ((0, 1), F(3, 10)), ((1, 1), F(4, 10))),
    )
    cell_side = F(1, 2)
    examples = []
    for jump in (1, 2):
        count = len(domain)
        transition = [[F(0) for _ in domain] for _ in domain]
        for index, (x, y) in enumerate(domain):
            for dx, dy in ((jump, 0), (-jump, 0), (0, jump), (0, -jump)):
                neighbor = positions.get((x + dx, y + dy))
                if neighbor is not None:
                    transition[index][neighbor] += F(1, 4)
        row_sums = [sum(row) for row in transition]
        checks.require(all(0 < value <= 1 for value in row_sums),
                       "the killed graph has an invalid transition row")
        checks.require(any(value < 1 for value in row_sums) and any(value == 1 for value in row_sums),
                       "the irregular graph does not exercise both interior and killed rows")
        checks.require(all(transition[i][j] == transition[j][i]
                           for i in range(count) for j in range(count)),
                       "the pooled compass killed transition is not symmetric")
        # The transpose is written explicitly: the area identity uses the
        # adjoint Green equation, not an unweighted occupancy inversion.
        adjoint_system = [[F(i == j) - transition[j][i] for j in range(count)]
                          for i in range(count)]
        green = solve_fraction(adjoint_system, [F(1)] * count)
        checks.require(matvec(adjoint_system, green) == [F(1)] * count,
                       "the exact adjoint Green equation failed")
        checks.require(all(value > 0 for value in green),
                       "a killed expected lifetime is nonpositive")
        normalized = [[value / row_sums[i] for value in row]
                      for i, row in enumerate(transition)]
        checks.require(all(sum(row) == 1 for row in normalized),
                       "the comparison normalization was not stochastic")
        checks.require(normalized != transition,
                       "the example cannot detect erroneous boundary renormalization")
        # Renormalization makes constants harmonic and destroys invertibility.
        checks.require(matvec([[F(i == j) - normalized[i][j] for j in range(count)]
                               for i in range(count)], [F(1)] * count) == [F(0)] * count,
                       "the boundary-renormalization countercheck failed")
        for law in laws:
            checks.require(sum(weight for _, weight in law) == 1,
                           "a convolution launch law is not normalized")
            positive_domain = {(x - z[0], y - z[1]) for x, y in solid for z, _ in law}
            checks.require(positive_domain <= set(domain),
                           "the finite aperture truncates the positive component")
            occupation = [sum(weight for z, weight in law if (x + z[0], y + z[1]) in solid)
                          for x, y in domain]
            forcing = [average - value for average, value in zip(matvec(transition, occupation), occupation)]
            occupation_area = cell_side ** 2 * sum(occupation)
            adjoint_area = -cell_side ** 2 * sum(weight * value for weight, value in zip(green, forcing))
            solid_area = cell_side ** 2 * len(solid)
            checks.require(occupation_area == solid_area,
                           "finite convolution fails the density-independent area identity")
            checks.require(adjoint_area == solid_area,
                           "the killed adjoint occupation-area identity failed")
        examples.append({
            "cells": count,
            "cell_side": str(cell_side),
            "command_step": str(jump * cell_side),
            "killed_rows": sum(value < 1 for value in row_sums),
            "launch_laws": len(laws),
            "maximum_green_weight": str(max(green)),
            "recovered_area": str(cell_side ** 2 * len(solid)),
        })
    return {
        "arithmetic": "exact Fractions on an irregular dyadic-cell domain",
        "examples": examples,
        "scope": "Finite adjoint and convolution identities; no continuum quadrature error or uniform Green bound is certified.",
    }


def support(constant, harmonics):
    result = [F(constant)] + [F(0)] * 8
    for frequency, (cosine, sine) in harmonics.items():
        result[2 * frequency - 1], result[2 * frequency] = F(cosine), F(sine)
    return tuple(result)


def support_add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def support_scale(a, p):
    return tuple(a * x for x in p)


def support_sub(p, q):
    return support_add(p, support_scale(-1, q))


def mixed_area_over_pi(p, q):
    value = p[0] * q[0]
    for frequency in range(1, 5):
        value += F(1 - frequency ** 2, 2) * (
            p[2 * frequency - 1] * q[2 * frequency - 1]
            + p[2 * frequency] * q[2 * frequency])
    return value


def area_over_pi(p):
    return mixed_area_over_pi(p, p)


def curvature_radius_bounds(p):
    remainder = sum((frequency ** 2 - 1) * (abs(p[2 * frequency - 1]) + abs(p[2 * frequency]))
                    for frequency in range(2, 5))
    return p[0] - remainder, p[0] + remainder


def support_c2_bound(p):
    return abs(p[0]) + sum((1 + frequency + frequency ** 2)
                           * (abs(p[2 * frequency - 1]) + abs(p[2 * frequency]))
                           for frequency in range(1, 5))


def support_examples():
    return (
        (support(4, {1: (F(3, 5), F(-2, 5)), 2: (F(1, 10), F(1, 14)),
                     3: (F(1, 70), F(-1, 90)), 4: (F(1, 700), F(1, 900))}),
         support(F(3, 4), {1: (F(-1, 7), F(1, 9)), 2: (F(1, 80), F(-1, 100)),
                          3: (F(1, 900), F(1, 800))})),
        (support(3, {1: (F(-1, 3), F(1, 5)), 2: (F(1, 15), F(-1, 11)),
                     4: (F(1, 500), F(0))}),
         support(F(5, 4), {1: (F(2, 9), F(-1, 8)), 2: (F(-1, 100), F(1, 60)),
                          3: (F(1, 500), F(-1, 400))})),
    )


def axis_widths(p):
    # p(0)+p(pi), p(pi/2)+p(3pi/2), exactly for these Fourier supports.
    return 2 * (p[0] + p[3] + p[7]), 2 * (p[0] - p[3] + p[7])


def width_sum(p):
    return sum(axis_widths(p))


def convex_hull(points):
    ordered = sorted(set(points))

    def cross(a, b, c):
        u, v = sub(b, a), sub(c, a)
        return u[0] * v[1] - u[1] * v[0]

    def half(sequence):
        result = []
        for point in sequence:
            while len(result) >= 2 and cross(result[-2], result[-1], point) <= 0:
                result.pop()
            result.append(point)
        return result

    return tuple(half(ordered)[:-1] + half(reversed(ordered))[:-1])


def polygon_area(polygon):
    return abs(sum(x[0] * y[1] - x[1] * y[0]
                   for x, y in zip(polygon, polygon[1:] + polygon[:1]))) / 2


def direct_flux_scale_recovery(checks):
    polygon_cases = strip_cases = 0
    translate = (F(3, 7), F(-2, 5))
    polygon_inputs = (
        ((0, 0), (2, 0), (3, 1), (2, 3), (0, 2), (-1, 1)),
        ((-2, -1), (1, -2), (3, 0), (2, 2), (-1, 3), (-3, 1)),
    )
    launch_law = (((F(1, 3), F(-1, 7)), F(1, 6)),
                  ((F(-2, 5), F(1, 2)), F(1, 3)),
                  ((F(1, 7), F(2, 9)), F(1, 2)))
    for vertices in polygon_inputs:
        polygon = convex_hull(tuple(add((F(x), F(y)), translate) for x, y in vertices))
        original_area = polygon_area(polygon)
        widths = (max(x for x, _ in polygon) - min(x for x, _ in polygon),
                  max(y for _, y in polygon) - min(y for _, y in polygon))
        checks.require(original_area > 0 and min(widths) > 0,
                       "a finite flux polygon is degenerate")
        for step in (F(1, 2), F(5, 4)):
            polygon_cases += 1
            strips = []
            for v in E:
                strip_cases += 1
                sweep = convex_hull(polygon + tuple(add(point, mul(-step, v)) for point in polygon))
                strip_area = polygon_area(sweep) - original_area
                transverse_width = widths[1] if v[0] else widths[0]
                checks.require(strip_area == step * transverse_width,
                               "a swept convex polygon violates the directional strip-area identity")
                averaged_area = sum(weight * (polygon_area(tuple(sub(point, z) for point in sweep))
                                               - polygon_area(tuple(sub(point, z) for point in polygon)))
                                    for z, weight in launch_law)
                checks.require(averaged_area == strip_area,
                               "an asymmetric launch translation changes the integrated strip area")
                strips.append(strip_area)
            checks.require(sum(strips) / 4 == step * sum(widths) / 2,
                           "the four pooled strip areas have an incorrect factor of two")

    ratio_cases = perturbation_cases = ambiguity_cases = 0
    inradius, gap_prior = F(1, 4), F(1, 2)
    perturb_P = support(1, {1: (F(1, 3), F(-1, 4)), 2: (F(1, 20), F(-1, 30)),
                            4: (F(1, 500), F(0))})
    perturb_D = support(F(1, 2), {1: (F(-1, 5), F(1, 7)),
                                 3: (F(1, 100), F(-1, 120)), 4: (F(-1, 600), F(0))})
    for C, B in support_examples():
        checks.require(B[0] - sum(abs(value) for value in B[1:]) >= inradius,
                       "the footprint support does not certify its stated origin-centered inball")
        for body in (C, B):
            centered = (body[0], F(0), F(0)) + body[3:]
            checks.require(width_sum(body) == width_sum(centered),
                           "the integrated width depends on a translation mode")
        for ratio in (F(3, 2), F(7, 4), F(2), F(11, 4)):
            a = 1 / (ratio - 1)
            P, D = support_add(C, B), support_scale(ratio - 1, B)
            checks.require(width_sum(D) >= 4 * gap_prior * inradius,
                           "the direct-flux inverse violates its prior denominator bound")
            for step in (F(1, 2), F(5, 4)):
                ratio_cases += 1
                widths = axis_widths(C)
                flux = sum((step * widths[1], step * widths[1],
                            step * widths[0], step * widths[0])) / 4
                checks.require(flux == step * width_sum(C) / 2,
                               "the smooth-support pooled flux coefficient is incorrect")
                recovered = (width_sum(P) - 2 * flux / step) / width_sum(D)
                checks.require(recovered == a and 1 + 1 / recovered == ratio,
                               "the linear width inverse fails to recover the unknown ratio")
                checks.require(support_scale(recovered, D) == B
                               and support_sub(P, support_scale(recovered, D)) == C,
                               "the linear flux inverse loses laboratory support coordinates")
                alternative = a + F(1, 32)
                alternative_B = support_scale(alternative, D)
                alternative_C = support_sub(P, alternative_B)
                alternative_ratio = 1 + 1 / alternative
                checks.require(curvature_radius_bounds(alternative_B)[0] > 0
                               and curvature_radius_bounds(alternative_C)[0] > 0,
                               "the positive-support ambiguity example is not physically convex")
                checks.require(support_add(alternative_C, alternative_B) == P
                               and support_add(alternative_C, support_scale(alternative_ratio, alternative_B))
                               == support_add(P, D),
                               "the support-only ambiguity does not preserve the two expanded bodies")
                checks.require(step * width_sum(alternative_C) / 2 != flux,
                               "the measured flux fails to distinguish the support-only ambiguity")
                ambiguity_cases += 1
                for epsilon in (F(1, 256), F(1, 4096), F(1, 65536)):
                    for sign in (-1, 1):
                        perturbation_cases += 1
                        P1 = support_add(P, support_scale(epsilon, perturb_P))
                        D1 = support_add(D, support_scale(-epsilon, perturb_D))
                        flux1 = flux + sign * epsilon
                        width_D1 = width_sum(D1)
                        a1 = (width_sum(P1) - 2 * flux1 / step) / width_D1
                        checks.require(width_D1 >= width_sum(D) / 2 and a1 > a / 2 > 0,
                                       "a finite flux error leaves the stable ratio branch")
                        error_identity = (width_sum(support_sub(P1, P)) - 2 * (flux1 - flux) / step
                                          - a * width_sum(support_sub(D1, D))) / width_D1
                        checks.require(a1 - a == error_identity,
                                       "the exact direct-flux inverse perturbation identity failed")
                        support_error_P = sum(abs(value) for value in support_sub(P1, P))
                        support_error_D = sum(abs(value) for value in support_sub(D1, D))
                        root_bound = (4 * support_error_P + 2 * abs(flux1 - flux) / step
                                      + 4 * a * support_error_D) / width_D1
                        checks.require(abs(a1 - a) <= root_bound,
                                       "the direct-flux inverse exceeds its explicit stability bound")
                        ratio1 = 1 + 1 / a1
                        checks.require(abs(ratio1 - ratio) == abs(a1 - a) / (a1 * a),
                                       "the direct-flux ratio perturbation identity failed")
                        B1 = support_scale(a1, D1)
                        C1 = support_sub(P1, B1)
                        B_bound = a1 * support_c2_bound(support_sub(D1, D)) + abs(a1 - a) * support_c2_bound(D)
                        checks.require(support_c2_bound(support_sub(B1, B)) <= B_bound,
                                       "a measured-flux footprint exceeds its C2 coefficient bound")
                        checks.require(support_c2_bound(support_sub(C1, C)) <=
                                       support_c2_bound(support_sub(P1, P)) + B_bound,
                                       "a measured-flux body exceeds its C2 coefficient bound")
                        checks.require(curvature_radius_bounds(B1)[0] > 0
                                       and curvature_radius_bounds(C1)[0] > 0,
                                       "a measured-flux support loses positive curvature")
    return {
        "arithmetic": "exact polygon sweep areas, Fourier widths, and rational inverses",
        "directional_polygon_strip_cases": strip_cases,
        "flux_perturbation_cases": perturbation_cases,
        "pooled_polygon_cases": polygon_cases,
        "scale_ratio_cases": ratio_cases,
        "support_ambiguities_separated_by_flux": ambiguity_cases,
        "scope": "Finite integrated-width and inverse checks; the manuscript proves isolation and continuum sampling error.",
    }


def exact_square_root(value):
    if value < 0:
        raise DiagnosticFailure("a mixed-area discriminant is negative")
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    if numerator ** 2 != value.numerator or denominator ** 2 != value.denominator:
        raise DiagnosticFailure("an exact physical discriminant is not its expected rational square")
    return F(numerator, denominator)


def recover_scale(P, D, mass):
    area_D = area_over_pi(D)
    mixed = mixed_area_over_pi(P, D)
    deficit = area_over_pi(P) - mass
    discriminant = mixed ** 2 - area_D * deficit
    root = exact_square_root(discriminant)
    if area_D <= 0 or root <= 0 or mixed + root <= 0:
        raise DiagnosticFailure("a scale-recovery example has a degenerate denominator")
    a = (mixed - root) / area_D
    stable_a = deficit / (mixed + root)
    return a, stable_a, (mixed + root) / area_D, discriminant


def mixed_area_scale_recovery(checks):
    bodies = support_examples()
    cases = perturbed_physical_cases = measurement_brackets = 0
    perturb_C = support(1, {1: (F(1, 3), F(-1, 4)), 2: (F(1, 20), F(-1, 30))})
    perturb_B = support(F(1, 2), {1: (F(-1, 5), F(1, 7)), 3: (F(1, 100), F(-1, 120))})
    for C, B in bodies:
        for body in (C, B):
            checks.require(curvature_radius_bounds(body)[0] > 0,
                           "a noncircular support lacks a positive radius-of-curvature margin")
            checks.require(any(body[1:3]) and any(body[3:]),
                           "a support example is centered or circular")
            centered = (body[0], F(0), F(0)) + body[3:]
            checks.require(area_over_pi(centered) == area_over_pi(body),
                           "the support-area calculation depends on a translation mode")
        for ratio in (F(3, 2), F(7, 4), F(2), F(11, 4)):
            cases += 1
            a = 1 / (ratio - 1)
            P, D = support_add(C, B), support_scale(ratio - 1, B)
            mass = area_over_pi(C)
            recovered, stable, other, discriminant = recover_scale(P, D, mass)
            mixed_CD = mixed_area_over_pi(C, D)
            checks.require(discriminant == mixed_CD ** 2 and mixed_CD > 0,
                           "the discriminant is not V(C,D)^2 with positive mixed area")
            checks.require(recovered == stable == a,
                           "the two smaller-root formulas do not recover the reciprocal scale gap")
            checks.require(1 + 1 / recovered == ratio,
                           "the unknown scale ratio is not recovered")
            checks.require(support_scale(recovered, D) == B
                           and support_sub(P, support_scale(recovered, D)) == C,
                           "laboratory-frame support recovery lost shape or translation")
            false_body = support_sub(P, support_scale(other, D))
            checks.require(mixed_area_over_pi(false_body, D) == -mixed_CD,
                           "the larger area root does not reverse the mixed-area sign")
            checks.require(curvature_radius_bounds(false_body)[1] < 0,
                           "the diagnostic failed to reject its nonconvex larger-root support")
            for epsilon in (F(1, 256), F(1, 4096), F(1, 65536)):
                perturbed_physical_cases += 1
                C1 = support_add(C, support_scale(epsilon, perturb_C))
                B1 = support_add(B, support_scale(-epsilon, perturb_B))
                ratio1 = ratio + epsilon
                a1 = 1 / (ratio1 - 1)
                P1, D1 = support_add(C1, B1), support_scale(ratio1 - 1, B1)
                mass1 = area_over_pi(C1)
                answer, stable_answer, _, _ = recover_scale(P1, D1, mass1)
                checks.require(answer == stable_answer == a1,
                               "an admissible perturbed scale system was not recovered")
                checks.require(curvature_radius_bounds(C1)[0] > 0
                               and curvature_radius_bounds(B1)[0] > 0,
                               "a perturbed physical support lost positive curvature")
                delta_area_P = area_over_pi(P1) - area_over_pi(P)
                delta_mixed = mixed_area_over_pi(P1, D1) - mixed_area_over_pi(P, D)
                delta_area_D = area_over_pi(D1) - area_over_pi(D)
                delta_mass = mass1 - mass
                residual = delta_area_P - 2 * a * delta_mixed + a * a * delta_area_D - delta_mass
                denominator = 2 * mixed_area_over_pi(P1, D1) - (a + a1) * area_over_pi(D1)
                checks.require(denominator >= mixed_CD > 0,
                               "the physical perturbation leaves the stable smaller-root branch")
                checks.require(abs(a1 - a) == abs(residual) / denominator,
                               "the exact quadratic-root perturbation identity failed")
                input_error = max(abs(delta_area_P), abs(delta_mixed), abs(delta_area_D), abs(delta_mass))
                root_bound = ((1 + a) ** 2 + 1) * input_error / mixed_CD
                checks.require(abs(a1 - a) <= root_bound,
                               "the inverse ratio exceeds its explicit perturbation bound")
                checks.require(abs(ratio1 - ratio) == abs(a1 - a) / (a * a1),
                               "the reciprocal scale-ratio stability identity failed")
                B_bound = abs(a1) * support_c2_bound(support_sub(D1, D)) + abs(a1 - a) * support_c2_bound(D)
                checks.require(support_c2_bound(support_sub(B1, B)) <= B_bound,
                               "footprint C2 coefficient recovery exceeds its linear bound")
                checks.require(support_c2_bound(support_sub(C1, C)) <=
                               support_c2_bound(support_sub(P1, P)) + B_bound,
                               "body C2 coefficient recovery exceeds its linear bound")
                # Independent area measurement errors need not be another
                # physical exact data triple.  Enclose the real smaller root
                # by rational signs, including both signs of the area error.
                for sign in (-1, 1):
                    measurement_brackets += 1
                    measured_mass = mass1 + sign * epsilon
                    area_P1, area_D1 = area_over_pi(P1), area_over_pi(D1)
                    mixed1 = mixed_area_over_pi(P1, D1)

                    def polynomial(u):
                        return area_P1 - 2 * u * mixed1 + u * u * area_D1 - measured_mass

                    radius = 2 * abs(polynomial(a)) / mixed_CD
                    lo, hi = a - radius, a + radius
                    checks.require(lo > 0 and 2 * (mixed1 - hi * area_D1) >= mixed_CD,
                                   "an area-error bracket lacks a positive inverse derivative bound")
                    checks.require(polynomial(lo) >= 0 >= polynomial(hi),
                                   "the rational area-error interval fails to bracket the smaller root")
                    for _ in range(32):
                        middle = (lo + hi) / 2
                        if polynomial(middle) > 0:
                            lo = middle
                        else:
                            hi = middle
                    checks.require(polynomial(lo) >= 0 >= polynomial(hi)
                                   and a - radius <= lo <= hi <= a + radius,
                                   "the refined rational root enclosure lost its stability reserve")
                    # Every value in the enclosed interval preserves the
                    # manuscript's output curvature condition in these cases.
                    for enclosed in (lo, hi):
                        footprint = support_scale(enclosed, D1)
                        body = support_sub(P1, footprint)
                        checks.require(curvature_radius_bounds(footprint)[0] > 0
                                       and curvature_radius_bounds(body)[0] > 0,
                                       "a measured-area root enclosure admits nonpositive output curvature")
    return {
        "arithmetic": "exact Fourier support coefficients and areas divided by pi",
        "independent_area_error_brackets": measurement_brackets,
        "noncentered_noncircular_support_pairs": len(bodies),
        "perturbed_physical_cases": perturbed_physical_cases,
        "scale_ratio_cases": cases,
        "scope": "Finite support and interval checks; not a proof of a uniform inverse on the full prior class.",
    }


def rate_algebra(checks):
    beta_values = (F(1, 100), F(1, 16), F(1, 4), F(1, 2), F(3, 4), F(1))
    gamma_values = (F(0), F(1, 2), F(1), F(3), F(7, 2))
    examples = []
    cases = 0
    for beta in beta_values:
        s = 6 + beta
        for gamma in gamma_values:
            cases += 1
            kappa = gamma + F(3, 2)
            upper = (kappa * s + 1) / (s - 2)
            old_upper = ((2 * gamma + 3) * s + 1) / (s - 2)
            lower = (s + 1) / (s - 2)
            checks.require(old_upper - upper == kappa * s / (s - 2),
                           "the rare-positive upper exponent improvement is incorrect")
            checks.require(upper - lower == (gamma + F(1, 2)) * s / (s - 2),
                           "the stationary upper/lower exponent gap is incorrect")
            checks.require(upper - F(23, 10) ==
                           gamma * s / (s - 2) + F(4, 5) * (1 - beta) / (s - 2),
                           "the area-cost absorption decomposition is incorrect")
            checks.require(upper >= F(23, 10) > 2,
                           "the nu^-2 area cost is not absorbed on an admissible example")
            # For nu = 2^(-k*denominator(upper)), comparison of the
            # two costs is exactly comparison of these integer exponents.
            for k in (1, 2, 7):
                checks.require(k * upper.numerator >= 2 * k * upper.denominator,
                               "an exact dyadic area-cost comparison failed")
            if not gamma:
                checks.require(upper - lower == s / (2 * (s - 2)),
                               "the displayed gamma=0 exponent gap is incorrect")
                examples.append({"beta": str(beta), "upper": str(upper),
                                 "lower": str(lower), "gap": str(upper - lower)})
    return {
        "arithmetic": "exact rational exponents",
        "parameter_cases": cases,
        "gamma_zero_examples": examples,
        "upper_minus_23_over_10": "gamma*s/(s-2) + 4*(1-beta)/(5*(s-2))",
        "scope": "Finite algebra checks; the manuscript gives the argument over the full beta and gamma ranges.",
    }


def binary_entropy(p):
    if p == 0 or p == 1:
        return 0.0
    value = float(p)
    return -value * log2(value) - (1 - value) * log2(1 - value)


def retained_information_and_density(checks):
    probabilities = (
        (F(0), F(1)), (F(0), F(1, 1000)),
        (F(999, 1000), F(1)), (F(1, 7), F(1, 7)),
        (F(1, 3), F(2, 5), F(1, 2)),
        (F(0), F(1, 10), F(9, 10), F(1)),
    )
    channel_cases = 0
    for means in probabilities:
        for skew in (False, True):
            channel_cases += 1
            raw = [F(index + 1 if skew else 1) for index in range(len(means))]
            weights = [weight / sum(raw) for weight in raw]
            mean = sum(weight * p for weight, p in zip(weights, means))
            information = binary_entropy(mean) - sum(float(weight) * binary_entropy(p)
                                                      for weight, p in zip(weights, means))
            breakpoints = sorted(set((F(0), F(1)) + means))
            revealed_entropy = 0.0
            for left, right in zip(breakpoints, breakpoints[1:]):
                midpoint = (left + right) / 2
                success = sum(weight for weight, p in zip(weights, means) if midpoint <= p)
                revealed_entropy += float(right - left) * binary_entropy(success)
            width = max(means) - min(means)
            checks.require(-1e-13 <= information <= revealed_entropy + 1e-13
                           and revealed_entropy <= float(width) + 1e-13,
                           "the binary erasure/range comparison failed")
    density_cases = 0
    for gamma in range(4):
        # On the unit disk, j(z) = c_gamma*(1-|z|)^gamma / pi,
        # c_gamma=(gamma+1)(gamma+2)/2.  Removing the common pi
        # factor makes the scaling identity exactly rational.
        coefficient = F((gamma + 1) * (gamma + 2), 2)
        checks.require(2 * coefficient / ((gamma + 1) * (gamma + 2)) == 1,
                       "the radial density normalization is incorrect")
        for scale in (F(1, 3), F(1, 2), F(1), F(7, 4), F(3)):
            for distance in (F(1, 100), F(1, 7), F(1, 2), F(1)):
                density_cases += 1
                scaled_density = scale ** -2 * coefficient * distance ** gamma
                lower_expression = coefficient * scale ** (-(gamma + 2)) * (scale * distance) ** gamma
                checks.require(scaled_density == lower_expression,
                               "the scaled boundary-density power is not gamma+2")
    return {"binary_range_cases": channel_cases,
            "binary_entropy_tolerance": "1e-13 (floating entropy only)",
            "exact_scaled_density_cases": density_cases}


def run():
    checks = Checks()
    sections = {}
    for name, function in (
        ("compass_candidates", compass_geometry),
        ("shifted_disk_detector", disk_detector),
        ("killed_adjoint_area", green_area_identity),
        ("unknown_ratio_direct_flux", direct_flux_scale_recovery),
        ("unknown_ratio_mixed_area", mixed_area_scale_recovery),
        ("rate_exponents", rate_algebra),
        ("retained_information_and_density", retained_information_and_density),
    ):
        before = checks.count
        section = function(checks)
        section["finite_checks"] = checks.count - before
        sections[name] = section
    return {
        "status": "passed",
        "manuscript": "A2-v36-stationary-boundary",
        "finite_checks": checks.count,
        "sections": sections,
        "scope": "Deterministic finite diagnostics only. These checks are not a mathematical proof certificate, a continuum experiment, or a claim that every theorem hypothesis has been verified.",
    }


def main():
    try:
        result = run()
        exit_code = 0
    except (DiagnosticFailure, ArithmeticError, ValueError) as error:
        result = {"status": "failed", "error": str(error),
                  "scope": "A finite diagnostic failed; no theorem conclusion follows."}
        exit_code = 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
