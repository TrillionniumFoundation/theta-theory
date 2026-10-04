#!/usr/bin/env python3
"""Deterministic finite diagnostics for the A2 v39 manuscript.

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
import math
import random
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
        "scope": "Finite algebra of the retained v36 bounds. The new matching uniform-disk power is checked separately in shrinking_layer_controller.",
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


def torus_average(field, nx, ny):
    return {(x, y): (field[((x + 1) % nx, y)] + field[((x - 1) % nx, y)]
                     + field[(x, (y + 1) % ny)] + field[(x, (y - 1) % ny)]) / 4
            for x, y in field}


def obstacle_iterate(field, forcing, nx, ny):
    average = torus_average(field, nx, ny)
    return {point: max(F(0), average[point] - forcing[point]) for point in field}


def torus_periods(field, nx, ny):
    return {(dx, dy) for dx in range(nx) for dy in range(ny)
            if all(field[((x + dx) % nx, (y + dy) % ny)] == value
                   for (x, y), value in field.items())}


def global_response_inverse(checks):
    nx = ny = 12
    occupation = {(x, y): F(0) for x in range(nx) for y in range(ny)}
    clusters = []
    motifs = ({(1, 1): F(1, 4), (1, 2): F(3, 4), (2, 1): F(1, 2)},
              {(4, 6): F(1, 3), (4, 7): F(2, 3),
               (5, 6): F(1, 2), (5, 7): F(5, 6)})
    for shift in (0, 6):
        for motif in motifs:
            component = {(x + shift, y): value for (x, y), value in motif.items()}
            occupation.update(component)
            clusters.append(tuple(sorted(component)))
    average = torus_average(occupation, nx, ny)
    forcing = {point: average[point] - value for point, value in occupation.items()}
    # A bound of two for each component diameter and a unit compass step
    # give H=(2+1)^2 and b=ceil(2H), exactly as in the displayed proof.
    H, block = F(9), 18
    horizon = 3 * block
    history = [{point: F(0) for point in occupation}]
    for time in range(1, horizon + 1):
        history.append(obstacle_iterate(history[-1], forcing, nx, ny))
        for point, value in occupation.items():
            checks.require(F(0) <= history[-2][point] <= history[-1][point] <= value,
                           "global finite obstacle iterates lose monotonicity or domination")
            checks.require(value - history[-1][point] <= F(1, 2 ** (time // block)),
                           "the finite global iterate exceeds its exit-tail bound")
    martingale_cases = 0
    for component in clusters:
        index = {point: number for number, point in enumerate(component)}
        transition = [[F(0) for _ in component] for _ in component]
        for row, (x, y) in enumerate(component):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbor = (x + dx, y + dy)
                if neighbor in index:
                    transition[row][index[neighbor]] += F(1, 4)
                else:
                    checks.require(occupation[(neighbor[0] % nx, neighbor[1] % ny)] == 0,
                                   "a component-exit step lands in a different positive component")
        system = [[F(i == j) - transition[i][j] for j in range(len(component))]
                  for i in range(len(component))]
        mean_exit = solve_fraction(system, [F(1)] * len(component))
        exit_payoff = solve_fraction(system, [-forcing[point] for point in component])
        checks.require(all(F(0) < value <= H for value in mean_exit),
                       "a finite component exit time violates the stated mean budget")
        checks.require(exit_payoff == [occupation[point] for point in component],
                       "the first-zero stopping payoff fails to recover occupation")
        survival = [F(1)] * len(component)
        for time in range(horizon + 1):
            for row, point in enumerate(component):
                checks.require(occupation[point] - history[time][point] <= survival[row]
                               <= F(1, 2 ** (time // block)),
                               "a finite stopped comparison or block-exit estimate failed")
            survival = matvec(transition, survival)
        for start in component:
            distribution = {(start, True): F(1)}
            truncated_mean = F(0)
            for _ in range(12):
                truncated_mean += sum(weight for (_, active), weight in distribution.items() if active)
                updated = {}
                for (point, active), weight in distribution.items():
                    if not active:
                        updated[(point, False)] = updated.get((point, False), F(0)) + weight
                        continue
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        following = (point[0] + dx, point[1] + dy)
                        state = (following, following in index)
                        updated[state] = updated.get(state, F(0)) + weight / 4
                distribution = updated
                squared_displacement = sum(weight * ((point[0] - start[0]) ** 2
                                                     + (point[1] - start[1]) ** 2)
                                           for (point, _), weight in distribution.items())
                checks.require(sum(distribution.values()) == 1
                               and squared_displacement == truncated_mean <= H,
                               "the finite stopped squared-displacement martingale identity failed")
                martingale_cases += 1
    stability_cases = 0
    for shift in ((0, 1), (1, 0), (1, 1)):
        for shrink in (F(0), F(1, 8), F(1, 4)):
            other = {(x, y): (1 - shrink) * occupation[((x - shift[0]) % nx,
                                                        (y - shift[1]) % ny)]
                     for x, y in occupation}
            other_average = torus_average(other, nx, ny)
            other_forcing = {point: other_average[point] - value for point, value in other.items()}
            occupation_error = max(abs(occupation[point] - other[point]) for point in occupation)
            forcing_error = max(abs(forcing[point] - other_forcing[point]) for point in occupation)
            checks.require(occupation_error <= H * forcing_error,
                           "the global stability bound fails for unrelated finite zero sets")
            stability_cases += 1
    numerical_cases = 0
    for error in (F(1, 1024), F(1, 4096)):
        noisy = {point: value + error * ((point[0] + 2 * point[1]) % 3 - 1)
                 for point, value in forcing.items()}
        iterate = {point: F(0) for point in occupation}
        for time in range(1, block + 1):
            iterate = obstacle_iterate(iterate, noisy, nx, ny)
            checks.require(max(abs(iterate[point] - history[time][point]) for point in occupation)
                           <= time * error,
                           "the finite forcing-error reserve is larger than N times epsilon")
            numerical_cases += 1
    locality_cases = 0
    target = (1, 1)
    for time in (1, 2, 3, 4):
        modified = dict(forcing)
        altered = 0
        for x, y in occupation:
            distance = min((x - target[0]) % nx, (target[0] - x) % nx)
            distance += min((y - target[1]) % ny, (target[1] - y) % ny)
            if distance > time:
                modified[(x, y)] += F(1, 3)
                altered += 1
        iterate = {point: F(0) for point in occupation}
        for _ in range(time):
            iterate = obstacle_iterate(iterate, modified, nx, ny)
        checks.require(altered > 0 and iterate[target] == history[time][target],
                       "forcing outside the finite reachability diamond changes its target")
        locality_cases += 1
    occupation_periods = torus_periods(occupation, nx, ny)
    forcing_periods = torus_periods(forcing, nx, ny)
    checks.require(occupation_periods == forcing_periods == {(0, 0), (6, 0)},
                   "the finite reciprocal forcing has gained or lost a translation period")
    return {
        "arithmetic": "exact rational finite periodic graph and killed component systems",
        "component_count": len(clusters),
        "finite_horizon": horizon,
        "graph_states": len(occupation),
        "locality_cases": locality_cases,
        "numerical_stability_cases": numerical_cases,
        "stopped_martingale_cases": martingale_cases,
        "unrelated_zero_set_stability_cases": stability_cases,
        "scope": "Finite graph checks of the displayed mechanisms; not a continuum inverse or a test of every admissible stopping rule.",
    }


def centered_support(p):
    return (p[0], F(0), F(0)) + p[3:]


def translated_support(p, vector):
    return (p[0], p[1] + vector[0], p[2] + vector[1]) + p[3:]


def evaluate_support(p, normal):
    value = p[0]
    cosine, sine = F(1), F(0)
    for frequency in range(1, 5):
        cosine, sine = (cosine * normal[0] - sine * normal[1],
                        sine * normal[0] + cosine * normal[1])
        value += p[2 * frequency - 1] * cosine + p[2 * frequency] * sine
    return value


def mean_support(collection):
    return tuple(sum(p[index] for p in collection) / len(collection) for index in range(9))


def canonical_components(collection, cell):
    return frozenset((p[1] % cell[0], p[2] % cell[1], centered_support(p)) for p in collection)


def translate_collection(collection, vector):
    return tuple(translated_support(p, vector) for p in collection)


def finite_component_periods(collection, candidates, cell):
    canonical = canonical_components(collection, cell)
    return {vector for vector in candidates
            if canonical_components(translate_collection(collection, vector), cell) == canonical}


def periodic_disk_bit(start, displacement, table_translation):
    point = sub(start, table_translation)
    period = (30, 40)
    anchor = (point[0] // period[0], point[1] // period[1])
    motifs = (((F(0), F(0)), F(3)), ((F(12), F(4)), F(3)),
              ((F(3), F(17)), F(3)), ((F(16), F(21)), F(7, 2)))
    nearby = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            translation = ((anchor[0] + dx) * period[0], (anchor[1] + dy) * period[1])
            nearby.extend((add(center, translation), radius) for center, radius in motifs)
    if any(dot(sub(point, center), sub(point, center)) <= radius ** 2 for center, radius in nearby):
        return False
    return any(segment_hits_disk(point, displacement, center, radius) for center, radius in nearby)


def unregistered_setting_rigidity(checks):
    # Equal base radii force the lower-envelope minimizer to depend on
    # direction.  A larger fourth body also exercises different width
    # deficits when entirely different components are chosen at settings.
    shapes = (
        support(3, {2: (F(0), F(1, 10))}),
        support(3, {2: (F(0), F(-1, 10))}),
        support(3, {2: (F(1, 12), F(0))}),
        support(F(7, 2), {2: (F(1, 12), F(1, 15)), 4: (F(1, 600), F(0))}),
    )
    centers = ((F(0), F(0)), (F(12), F(4)), (F(3), F(17)), (F(16), F(21)))
    components = tuple(translated_support(shape, add(center, (F(shift), F(0))))
                       for shift in (0, 30) for shape, center in zip(shapes, centers))
    q = support(F(3, 5), {2: (F(1, 80), F(-1, 90)),
                          3: (F(1, 600), F(1, 700)), 4: (F(-1, 900), F(1, 1000))})
    ratios = (F(1), F(7, 4), F(2, 3), F(5, 2))
    shifts = ((F(1, 3), F(-2, 7)), (F(-5, 4), F(3, 8)),
              (F(7, 10), F(-4, 9)), (F(-1, 8), F(2, 5)))
    step = F(1, 2)
    collections = []
    deficits = []
    selected_widths = set()
    for body in shapes + (q,):
        checks.require(curvature_radius_bounds(body)[0] > 0,
                       "an unregistered noncircular support has no positive curvature margin")
    for setting, (ratio, shift) in enumerate(zip(ratios, shifts)):
        ordered = tuple(translated_support(support_add(C, support_scale(ratio, q)), mul(-1, shift))
                        for C in components)
        # These independent permutations are deliberately not undone by any
        # cross-setting matching operation below.
        permutation = list(range(len(components)))
        permutation = permutation[setting + 1:] + permutation[:setting + 1]
        if setting % 2:
            permutation.reverse()
        rows = tuple(ordered[index] for index in permutation)
        collections.append(rows)
        for P, original_index in zip(rows, permutation):
            C = components[original_index]
            flux = step * width_sum(C) / 2
            deficit = width_sum(P) - 2 * flux / step
            checks.require(deficit == ratio * width_sum(q) > 0,
                           "an integrated footprint deficit depends on the chosen component or shift")
            recovered_C = support_sub(P, support_scale(ratio, q))
            checks.require(recovered_C == translated_support(C, mul(-1, shift)),
                           "unregistered support subtraction does not preserve its observed frame")
        chosen_index = (2, 0, 7, 6)[setting]
        original = components[permutation[chosen_index]]
        flux = step * width_sum(original) / 2
        selected_widths.add(width_sum(original))
        deficits.append(width_sum(rows[chosen_index]) - 2 * flux / step)
    checks.require(len(selected_widths) > 1,
                   "the arbitrary selected components accidentally all have the same width")
    checks.require(tuple(deficit / deficits[0] for deficit in deficits) == ratios,
                   "independently chosen component deficits fail to recover scale order and ratios")

    normals = rational_unit_normals() + (rotate_rational(E[0], F(1, 64)),
                                        rotate_rational(E[0], F(-1, 64)))
    minimizers = set()
    envelope_cases = 0
    for normal in normals:
        baseline_values = tuple(evaluate_support(shape, normal) for shape in shapes)
        baseline = min(baseline_values)
        minimizers.update(index for index, value in enumerate(baseline_values) if value == baseline)
        envelope = [min(evaluate_support(centered_support(P), normal) for P in rows)
                    for rows in collections]
        for index in range(len(ratios)):
            checks.require(envelope[index] == baseline + ratios[index] * evaluate_support(q, normal),
                           "the unlabeled centered-support envelope fails to split into a common part")
            if index:
                checks.require((envelope[index] - envelope[0]) / (ratios[index] - 1)
                               == evaluate_support(q, normal),
                               "a lower-envelope difference does not recover the centered footprint")
                envelope_cases += 1
    checks.require(len(minimizers) >= 3,
                   "the envelope examples do not exercise changing minimizing components")
    plus, minus = normals[-2:]
    middle = add(plus, minus)
    homogeneous_middle = middle[0] * min(evaluate_support(shape, E[0]) for shape in shapes)
    endpoint_sum = min(evaluate_support(shape, plus) for shape in shapes)
    endpoint_sum += min(evaluate_support(shape, minus) for shape in shapes)
    checks.require(middle[1] == 0 and homogeneous_middle > endpoint_sum,
                   "the example fails to distinguish a lower envelope from a convex support function")

    averages = [mean_support(tuple(centered_support(P) for P in rows)) for rows in collections]
    baseline_average = mean_support(tuple(centered_support(C) for C in components))
    centroid_means = [tuple(sum(P[coordinate] for P in rows) / len(rows) for coordinate in (1, 2))
                      for rows in collections]
    centroid_original = tuple(sum(C[coordinate] for C in components) / len(components)
                              for coordinate in (1, 2))
    for index, ratio in enumerate(ratios):
        checks.require(averages[index] == support_add(baseline_average, support_scale(ratio, q)),
                       "the finite unordered support average fails its exact cancellation identity")
        checks.require(centroid_means[index] == sub(centroid_original, shifts[index]),
                       "the finite complete-cloud Steiner mean has an incorrect translation")
        checks.require(sub(centroid_means[0], centroid_means[index]) == sub(shifts[index], shifts[0]),
                       "complete-cloud centroid registration fails to recover the relative vector")
        if index:
            checks.require(support_scale(1 / (ratio - 1), support_sub(averages[index], averages[0])) == q,
                           "the finite cloud average fails to recover the common footprint")

    cell = (F(60), F(40))
    candidate_periods = {(F(0), F(0))}
    for C in components:
        for D in components:
            candidate_periods.add(((D[1] - C[1]) % cell[0], (D[2] - C[2]) % cell[1]))
    periods = finite_component_periods(components, candidate_periods, cell)
    checks.require(periods == {(F(0), F(0)), (F(30), F(0))},
                   "the finite periodic support collection has an unexpected primitive period")
    period_cancellation_cases = 0
    common_Q = translated_support(support_scale(F(3, 2), q), (F(1, 8), F(-2, 11)))
    common_b = (F(2, 9), F(3, 7))
    expanded = tuple(translated_support(support_add(C, common_Q), mul(-1, common_b)) for C in components)
    checks.require(finite_component_periods(expanded, candidate_periods, cell) == periods,
                   "a common Minkowski summand changes the complete component-period candidates")
    for C, expanded_C in zip(components, expanded):
        for D, expanded_D in zip(components, expanded):
            for translation in ((F(0), F(0)), (F(30), F(0)), (F(1, 3), F(4, 5))):
                checks.require(support_sub(translated_support(expanded_C, translation), expanded_D)
                               == support_sub(translated_support(C, translation), D),
                               "a common expansion changes a translated pair's support difference")
                period_cancellation_cases += 1
    checks.require(len(canonical_components(components, (F(30), F(40)))) == len(shapes)
                   == len(canonical_components(expanded, (F(30), F(40)))),
                   "common expansion changes the finite primitive component-orbit count")

    orbit_averages = []
    for setting, (ratio, shift) in enumerate(zip(ratios, shifts)):
        representatives = []
        for index, C in enumerate(components[:len(shapes)]):
            representative_shift = (F(30 * (index - setting)), F(40 * ((index + setting) % 3 - 1)))
            P = translated_support(support_add(C, support_scale(ratio, q)), sub(representative_shift, shift))
            representatives.append(centered_support(P))
        representatives.reverse()
        orbit_averages.append(mean_support(tuple(representatives)))
    for index in range(1, len(ratios)):
        checks.require(support_scale(1 / (ratios[index] - 1),
                                      support_sub(orbit_averages[index], orbit_averages[0])) == q,
                       "arbitrary orbit representatives spoil footprint cancellation")

    coset_cases = 0
    reference_frame = translate_collection(components, mul(-1, shifts[0]))
    for index, shift in enumerate(shifts):
        frame = translate_collection(components, mul(-1, shift))
        relative = sub(shift, shifts[0])
        for px in (-1, 0, 1):
            for py in (-1, 0, 1):
                period = (F(30 * px), F(40 * py))
                for defect in ((F(0), F(0)), (F(1), F(0)), (F(12), F(4))):
                    candidate = add(relative, add(period, defect))
                    accepted = canonical_components(translate_collection(frame, candidate), cell)
                    accepted = accepted == canonical_components(reference_frame, cell)
                    expected = ((period[0] + defect[0]) % cell[0],
                                (period[1] + defect[1]) % cell[1]) in periods
                    checks.require(accepted == expected,
                                   "finite registration candidates do not form the predicted period coset")
                    coset_cases += 1

    gauge_translation = (F(5, 7), F(-2, 9))
    setting_periods = ((F(0), F(40)), (F(30), F(0)),
                       (F(-30), F(40)), (F(60), F(-40)))
    for index, (ratio, shift) in enumerate(zip(ratios, shifts)):
        transformed_table = translate_collection(components, gauge_translation)
        new_shift = add(shift, add(gauge_translation, setting_periods[index]))
        transformed_expanded = tuple(translated_support(support_add(C, support_scale(ratio, q)),
                                                        mul(-1, new_shift)) for C in transformed_table)
        checks.require(canonical_components(transformed_expanded, cell)
                       == canonical_components(collections[index], cell),
                       "a common translation and independent setting periods alter expanded observations")
    binary_couplings = 0
    binary_outcomes = set()
    targets = ((F(-13, 4), F(0)), (F(13, 4), F(0)), (F(0), F(0)),
               (F(0), F(13, 4)), (F(35, 4), F(4)), (F(3), F(55, 4)))
    launch_offsets = ((F(0), F(0)), (F(1, 10), F(0)), (F(0), F(-1, 12)))
    commands = (mul(F(1, 2), E[0]), mul(F(1, 2), E[1]),
                mul(F(1, 2), E[2]), mul(F(1, 2), E[3]), (F(0), F(0)))
    for index, (ratio, shift) in enumerate(zip(ratios, shifts)):
        for target in targets:
            nominal = sub(target, shift)
            for offset in launch_offsets:
                launch = add(shift, mul(ratio, offset))
                transformed_launch = add(launch, add(gauge_translation, setting_periods[index]))
                for displacement in commands:
                    for reverse in (False, True):
                        center = add(nominal, displacement) if reverse else nominal
                        command = mul(-1, displacement) if reverse else displacement
                        original_bit = periodic_disk_bit(add(center, launch), command, (F(0), F(0)))
                        transformed_bit = periodic_disk_bit(add(center, transformed_launch), command, gauge_translation)
                        checks.require(original_bit == transformed_bit,
                                       "a gauge transformation changes a forward or reciprocal collision bit")
                        binary_outcomes.add(original_bit)
                        binary_couplings += 1
    checks.require(binary_outcomes == {False, True},
                   "the finite gauge coupling does not exercise both collision outcomes")
    return {
        "arithmetic": "exact rational Fourier supports, component sets, and collision bits",
        "components_in_complete_cloud": len(components),
        "distinct_envelope_minimizers": len(minimizers),
        "envelope_inverse_cases": envelope_cases,
        "gauge_binary_couplings": binary_couplings,
        "period_coset_cases": coset_cases,
        "settings": len(ratios),
        "translated_pair_cancellation_cases": period_cancellation_cases,
        "scope": "Finite complete clouds and finite periodic candidate classes; no assertion about arbitrary infinite infima or continuum registration stability.",
    }


def is_dyadic(value):
    denominator = value.denominator
    return denominator > 0 and denominator & (denominator - 1) == 0


def shrinking_layer_controller(checks):
    A, contraction = F(8), F(3, 4)
    successful_updates = rejected_labels = 0
    for index in range(33):
        radius = F(1) + F(index, 16)
        intervals = [(F(1), F(3))]
        for level in range(8):
            next_intervals = []
            for left, right in intervals:
                width = right - left
                midpoint = (left + right) / 2
                layer = width / (4 * A)
                for label in (0, 1):
                    new_left, new_right = ((midpoint - A * layer, right) if label
                                           else (left, midpoint + A * layer))
                    legal = midpoint <= radius + A * layer if label else midpoint >= radius - A * layer
                    checks.require(left <= new_left < new_right <= right
                                   and new_right - new_left == contraction * width,
                                   "a safeguarded update loses its exact three-quarter width schedule")
                    checks.require(is_dyadic(new_left) and is_dyadic(new_right) and is_dyadic(layer),
                                   "a scalar shrinking interval or physical layer is not dyadic")
                    if legal:
                        checks.require(new_left <= radius <= new_right,
                                       "an allowed ambiguous-layer label discards the true boundary")
                        next_intervals.append((new_left, new_right))
                        successful_updates += 1
                    else:
                        checks.require(not (new_left <= radius <= new_right),
                                       "the illegal-label counterexample does not cross the certified layer")
                        rejected_labels += 1
            intervals = next_intervals
            checks.require(intervals and all(right - left == 2 * contraction ** (level + 1)
                                            for left, right in intervals),
                           "the deterministic width schedule depends on an allowed answer history")
    checks.require(rejected_labels > 0,
                   "the interval diagnostics do not exercise incorrect-label counterexamples")

    schedules = weighted_cost_cases = 0
    maximum_depth = 0
    # q^(3/2) <= 21/32, proved here by a rational comparison of squares.
    # Thus the same geometric majorant works for every kappa >= 3/2.
    majorant = F(21, 32)
    checks.require(contraction ** 3 < majorant ** 2 < 1,
                   "the rational majorant of q^(3/2) is invalid")
    for tolerance in (F(1, 16), F(1, 64), F(1, 256), F(1, 4096)):
        widths = [F(2)]
        while widths[-1] > 2 * tolerance:
            widths.append(contraction * widths[-1])
        depth = len(widths) - 1
        maximum_depth = max(maximum_depth, depth)
        checks.require(depth >= 1 and widths[-2] > 2 * tolerance
                       and 2 * contraction * tolerance < widths[-1] <= 2 * tolerance,
                       "the stopping level is not minimal or violates the final-width bracket")
        for width in widths[:-1]:
            checks.require(tolerance / (8 * A) < (width / (4 * A)) / 2,
                           "the common target mesh exceeds a preceding layer's rounding reserve")
        for confidence in (F(1, 8), F(1, 32)):
            for searches in (1, 7, 16):
                schedules += 1
                allowances = [confidence / (4 * searches) * F(1, 2 ** (depth - 1 - level))
                              for level in range(depth)]
                checks.require(sum(allowances) < confidence / (2 * searches)
                               and searches * sum(allowances) < confidence / 2,
                               "the fine-level conditional confidence allocation exceeds its reserve")
                checks.require(all(allowances[level + 1] == 2 * allowances[level]
                                   for level in range(depth - 1)),
                               "the expensive fine levels do not receive the stated confidence allowance")
                logarithm_bound = 0
                while 2 ** logarithm_bound < 4 * searches / confidence:
                    logarithm_bound += 1
                for twice_kappa in (3, 4, 5, 8):
                    weighted_cost_cases += 1
                    weighted_majorant = F(0)
                    for k in range(1, depth + 1):
                        level = depth - k
                        checks.require((widths[-1] / widths[level]) ** twice_kappa
                                       == contraction ** (twice_kappa * k),
                                       "a normalized layer cost has the wrong exponent or level index")
                        checks.require(contraction ** (twice_kappa * k) <= majorant ** (2 * k),
                                       "the exact squared layer cost exceeds its geometric majorant")
                        weighted_majorant += majorant ** k * (logarithm_bound + k - 1)
                    geometric_sum = majorant * (1 - majorant ** depth) / (1 - majorant)
                    weighted_sum = (majorant ** 2 - depth * majorant ** (depth + 1)
                                    + (depth - 1) * majorant ** (depth + 2)) / (1 - majorant) ** 2
                    checks.require(weighted_majorant == logarithm_bound * geometric_sum + weighted_sum,
                                   "the finite geometric and level-weighted cost identity failed")
                    uniform_bound = (logarithm_bound * majorant / (1 - majorant)
                                     + majorant ** 2 / (1 - majorant) ** 2)
                    checks.require(weighted_majorant <= uniform_bound,
                                   "the normalized attempted cost retains an unbounded depth factor")
    exponent_cases = 0
    for beta in (F(1, 100), F(1, 4), F(1, 2), F(3, 4), F(1)):
        s = 6 + beta
        information_exponent = F(3, 2) * s
        lower = (information_exponent + 1) / (s - 2)
        upper = (F(3, 2) * s + 1) / (s - 2)
        checks.require(lower == upper > 2,
                       "the uniform-disk packing and shrinking upper powers do not match")
        for gamma in (F(0), F(1, 2), F(2)):
            kappa = gamma + F(3, 2)
            displayed = (kappa * s + 1) / (s - 2)
            checks.require(displayed == kappa * s / (s - 2) + 1 / (s - 2),
                           "the total radial-search exponent fails to add angular and layer costs")
            checks.require(displayed - lower == gamma * s / (s - 2),
                           "the density-exponent upper cost was incorrectly identified with the disk lower power")
            exponent_cases += 1
    return {
        "arithmetic": "exact rational safeguarded intervals, confidence sums, and cost majorants",
        "conditional_confidence_schedules": schedules,
        "exponent_cases": exponent_cases,
        "maximum_tested_depth": maximum_depth,
        "rejected_label_counterexamples": rejected_labels,
        "successful_interval_updates": successful_updates,
        "weighted_cost_cases": weighted_cost_cases,
        "scope": "Finite interval histories and exact geometric-sum algebra; not a statistical execution of the controller.",
    }


def effective_boundary_models(checks):
    interval_cases = two_arc_cases = 0
    intervals = [set(range(left, right)) for left in range(7) for right in range(left, 7)]
    coefficients = {index: F(index + 2, 11) for index in range(6)}
    for original in intervals:
        for translated in intervals:
            interval_cases += 1
            active = original ^ translated
            pieces = sum(index - 1 not in active for index in active)
            two_arc_cases += int(pieces == 2)
            original_derivative = sum(coefficients[index] for index in original)
            translated_derivative = sum(coefficients[index] for index in translated)
            cancelled = sum(coefficients[index] for index in translated - original)
            cancelled -= sum(coefficients[index] for index in original - translated)
            checks.require(pieces <= 2 and translated_derivative - original_derivative == cancelled,
                           "the two curved sides do not cancel to at most two active intervals")
            if original == translated:
                checks.require(not active and cancelled == 0,
                               "identical endpoint memberships leave a spurious curved variation")
    checks.require(two_arc_cases > 0,
                   "the effective-boundary examples do not exercise two disjoint active arcs")

    harmonic_cases = 0
    c0 = F(1, 4)
    for length in (F(1, 8), F(1, 16), F(1, 64), F(1, 1024)):
        for entering in (length / 4, length / 2, length, 2 * length, F(1, 2), F(1)):
            for tangential in (F(0), length / 100, length / 2, length, 10 * length, F(1, 4)):
                harmonic_cases += 1
                value = entering * (tangential + length) / (entering + tangential + length)
                checks.require(entering >= c0 * length and value >= c0 * length / (1 + c0),
                               "the active-arc harmonic-mean estimate loses its uniform length factor")
                scaled_entering, scaled_tangent = entering / length, tangential / length
                checks.require(value / length == scaled_entering * (scaled_tangent + 1)
                               / (scaled_entering + scaled_tangent + 1),
                               "the active-arc estimate is not invariant under its stated normalization")

    ray_cases = 0
    disk_radius = F(1, 64)
    for length in (F(1, 64), F(1, 128), F(1, 512), F(1, 8192)):
        slope = length / 4
        entering = 2 * slope / (1 + slope ** 2)
        normal = (-entering, (1 - slope ** 2) / (1 + slope ** 2))
        tangent = (-normal[1], normal[0])
        clearance = length / 8
        for sign in (-1, 1):
            point = (sign * (disk_radius - clearance), F(0))
            tangent_size = abs(dot(point, tangent))
            G = disk_radius ** 2 - dot(point, point)
            exit_distance = clearance
            direction = (F(sign), F(0))
            checks.require(dot(normal, normal) == 1 and normal[0] < 0
                           and entering >= length / 4,
                           "a rational near-seam normal fails its entering-angle reserve")
            checks.require(G >= length * (tangent_size + length) / 16,
                           "a near-seam ray example lacks the specified disk-clearance lower bound")
            checks.require(abs(point[0]) <= disk_radius * entering + tangent_size,
                           "the normal/tangent decomposition fails its projected-distance bound")
            checks.require(dot(add(point, mul(exit_distance, direction)),
                               add(point, mul(exit_distance, direction))) == disk_radius ** 2,
                           "the rational ray exit does not solve the disk equation")
            checks.require(exit_distance >= G / (2 * abs(point[0]) + disk_radius)
                           and entering * exit_distance >= length ** 2 / 32,
                           "a short near-seam ray loses the quadratic Jacobian-depth lower bound")
            checks.require(length * entering * exit_distance / 2 >= length ** 3 / 64,
                           "the active-ray rectangle loses its cubic area order")
            for multiplier in (2, 3, 5):
                command_length = multiplier * exit_distance
                other = add(point, mul(command_length, direction))
                checks.require(exit_distance <= command_length and dot(other, other) > disk_radius ** 2,
                               "the short active ray does not have one endpoint outside its launch disk")
                ray_cases += 1

    facet_cases = facet_point_pairs = 0
    smallest_command = None
    for radius in (F(1, 64), F(1, 128)):
        for parameter in (F(1, 4), F(1, 8), F(1, 32), F(1, 128)):
            length = 4 * radius * parameter / (1 + parameter ** 2)
            offset = radius * (1 - parameter ** 2) / (1 + parameter ** 2)
            depth = length ** 2 / 256
            checks.require((length / 2) ** 2 + offset ** 2 == radius ** 2,
                           "the facet intersection is not the declared exact disk chord")
            for multiplier in (1, 2, 4):
                command_length = multiplier * length
                smallest_command = command_length if smallest_command is None else min(smallest_command, command_length)
                left, right = -command_length / 2 - length / 4, -command_length / 2 + length / 4
                checks.require(left + command_length >= length / 4 and -right >= length / 4,
                               "the middle chord lacks clearance from the whole swept facet endpoints")
                checks.require(2 * depth - depth ** 2 <= (length / 8) ** 2,
                               "the circle's entering endpoint moves beyond the facet-rectangle reserve")
                checks.require(length * depth / 2 == length ** 3 / 512,
                               "the exact facet rectangle does not have cubic area")
                for upper_or_lower in (-1, 1):
                    for disk_side in (-1, 1):
                        facet_cases += 1
                        disk_center = (-command_length / 2,
                                       upper_or_lower * (1 + disk_side * offset))
                        for horizontal in (left, -command_length / 2, right):
                            for vertical in (depth / 2, depth):
                                inner = (horizontal, upper_or_lower * (1 - vertical))
                                outer = (horizontal, upper_or_lower * (1 + vertical))
                                checks.require(dot(sub(inner, disk_center), sub(inner, disk_center)) <= radius ** 2
                                               and dot(sub(outer, disk_center), sub(outer, disk_center)) <= radius ** 2,
                                               "a collision or complement facet rectangle exits the launch disk")
                                checks.require(segment_hits_disk(inner, (command_length, F(0)),
                                                                 (F(0), F(0)), F(1))
                                               and not segment_hits_disk(outer, (command_length, F(0)),
                                                                         (F(0), F(0)), F(1)),
                                               "the inward/outward facet models do not lie on opposite collision sides")
                                facet_point_pairs += 1
    for start in ((F(0), F(0)), (F(1), F(0)), (F(2), F(0)), (F(-3, 2), F(1, 3))):
        checks.require(not segment_hits_disk(start, (F(0), F(0)), (F(0), F(0)), F(1)),
                       "a zero-length command has a spurious positive collision bit")
    return {
        "arithmetic": "exact interval cancellation, rational near-seam rays, and circle/facet geometry",
        "active_harmonic_mean_cases": harmonic_cases,
        "active_interval_pairs": interval_cases,
        "facet_rectangle_cases": facet_cases,
        "facet_collision_complement_point_pairs": facet_point_pairs,
        "short_ray_cases": ray_cases,
        "smallest_facet_command": str(smallest_command),
        "scope": "Finite algebra and explicit geometric models only; no numerical certification of the continuum effective-boundary estimate or its uniform constants.",
    }


def hellinger_capacity_algebra(checks):
    root_pairs = []
    for parameter in (F(0), F(1, 16), F(1, 8), F(1, 4), F(1, 3),
                      F(1, 2), F(2, 3), F(3, 4), F(1)):
        success_root = 2 * parameter / (1 + parameter ** 2)
        failure_root = (1 - parameter ** 2) / (1 + parameter ** 2)
        checks.require(success_root ** 2 + failure_root ** 2 == 1,
                       "a rational-square Bernoulli endpoint is not normalized")
        root_pairs.append((success_root, failure_root))
    endpoint_cases = posterior_cases = 0
    priors = ((F(1, 4),) * 4, (F(1, 10), F(2, 10), F(3, 10), F(4, 10)),
              (F(1, 100), F(1, 100), F(1, 100), F(97, 100)))
    for index, roots_a in enumerate(root_pairs):
        for roots_b in root_pairs[index:]:
            endpoint_cases += 1
            a, b = roots_a[0] ** 2, roots_b[0] ** 2
            affinity = roots_a[0] * roots_b[0] + roots_a[1] * roots_b[1]
            squared_hellinger = (roots_a[0] - roots_b[0]) ** 2 + (roots_a[1] - roots_b[1]) ** 2
            checks.require(0 <= affinity <= 1 and squared_hellinger == 2 * (1 - affinity),
                           "the endpoint Hellinger/affinity identity failed")
            midpoint = (a + b) / 2
            if 0 < midpoint < 1:
                checks.require((b - a) ** 2 / (4 * midpoint * (1 - midpoint)) <= squared_hellinger,
                               "the midpoint chi-square radius exceeds the endpoint Hellinger diameter")
            else:
                checks.require(a == b and squared_hellinger == 0,
                               "a degenerate midpoint has a nonconstant response family")
            means = tuple(a + interpolation * (b - a)
                          for interpolation in (F(0), F(1, 5), F(2, 3), F(1)))
            for prior in priors:
                posterior_cases += 1
                mean = sum(weight * probability for weight, probability in zip(prior, means))
                variance = sum(weight * (probability - mean) ** 2
                               for weight, probability in zip(prior, means))
                endpoint_product = (mean - a) * (b - mean)
                checks.require(variance <= endpoint_product,
                               "a finite posterior violates the endpoint variance bound")
                checks.require((1 - affinity ** 2) * mean * (1 - mean) - endpoint_product
                               == (affinity * mean - roots_a[0] * roots_b[0]) ** 2,
                               "the exact posterior endpoint-capacity identity failed")
                if 0 < mean < 1:
                    checks.require(variance / (mean * (1 - mean)) <= 1 - affinity ** 2 <= squared_hellinger,
                                   "a rational posterior information-radius bound exceeds Hellinger diameter")
                else:
                    checks.require(variance == 0,
                                   "an endpoint posterior mean has positive conditional variance")
    mixture_cases = 0
    mixture_weights = (F(1, 6), F(1, 3), F(1, 2))
    for index in range(len(root_pairs)):
        left = tuple(root_pairs[(index + shift) % len(root_pairs)] for shift in (0, 2, 5))
        right = tuple(root_pairs[(index + shift) % len(root_pairs)] for shift in (1, 4, 7))
        mixed_left = sum(weight * roots[0] ** 2 for weight, roots in zip(mixture_weights, left))
        mixed_right = sum(weight * roots[0] ** 2 for weight, roots in zip(mixture_weights, right))
        success_affinity = sum(weight * x[0] * y[0] for weight, x, y in zip(mixture_weights, left, right))
        failure_affinity = sum(weight * x[1] * y[1] for weight, x, y in zip(mixture_weights, left, right))
        checks.require(success_affinity ** 2 <= mixed_left * mixed_right
                       and failure_affinity ** 2 <= (1 - mixed_left) * (1 - mixed_right),
                       "a parameter-independent mixture violates the exact affinity convexity bound")
        averaged_distance = sum(weight * ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
                                for weight, x, y in zip(mixture_weights, left, right))
        checks.require(averaged_distance == 2 * (1 - success_affinity - failure_affinity),
                       "the pooled Hellinger mixture identity has an incorrect normalization")
        mixture_cases += 1
    holder_cases = 0
    values = (F(0), F(1, 32), F(1, 8), F(1, 3), F(1, 2), F(3, 4), F(1))
    for left in values:
        for right in values:
            # P=left^6 gives P^(2/3)=left^4 and sqrt(P)=left^3.
            # Squaring once more removes the remaining fractional power.
            checks.require((left ** 3 - right ** 3) ** 4 <= abs(left ** 4 - right ** 4) ** 3,
                           "the endpoint-safe Holder step does not yield the 3/2 Hellinger power")
            holder_cases += 1
    checks.require(F(2, 3) - 1 + F(1, 3) == 0 and 2 * F(3, 4) == F(3, 2),
                   "the differential and Holder exponents do not combine as displayed")
    return {
        "arithmetic": "exact rational square-root endpoints, posterior identities, and integer powers",
        "endpoint_intervals": endpoint_cases,
        "holder_endpoint_cases": holder_cases,
        "mixture_cases": mixture_cases,
        "posterior_capacity_cases": posterior_cases,
        "scope": "Finite information-radius and exponent algebra; no entropy computation or continuum Hellinger theorem is being certified.",
    }


def v38_solve(a, b):
    """Small exact Gauss--Jordan solver; errors are never disabled by -O."""
    n = len(b)
    mat = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if mat[i][col]), None)
        if pivot is None:
            raise DiagnosticFailure('Singular exact system')
        mat[col], mat[pivot] = mat[pivot], mat[col]
        scale = mat[col][col]
        mat[col] = [x / scale for x in mat[col]]
        for i in range(n):
            if i != col and mat[i][col]:
                scale = mat[i][col]
                mat[i] = [x - scale*y for x, y in zip(mat[i], mat[col])]
    return [row[-1] for row in mat]

def v38_dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def v38_matrix(k):
    sites = [(i, j) for i in range(-k, k+1) for j in range(-k, k+1)]
    n = len(sites)
    index = {z: i for i, z in enumerate(sites)}
    q = [[F(0) for _ in sites] for _ in sites]
    for i, (x, y) in enumerate(sites):
        for step in [(1,0),(-1,0),(0,1),(0,-1)]:
            z = (x+step[0], y+step[1])
            if z in index:
                q[i][index[z]] += F(1,4)
    return sites, q, index[(0,0)]

def v38_stopping_vectors(q, origin):
    n = len(q)
    results = []
    for mask in range(1 << n):
        active = [i for i in range(n) if (mask >> i) & 1]
        m = [F(0)]*n
        if origin in active:
            a = [[F(i == j) - q[j][i] for j in active] for i in active]
            b = [F(i == origin) for i in active]
            for i, val in zip(active, v38_solve(a, b)):
                m[i] = val
        results.append(m)
    return results

def retained_v38_finite_stencil(checks):
    require = checks.require
    sites, q, origin = v38_matrix(1)
    n = len(sites)
    ident = [[F(i == j)-q[i][j] for j in range(n)] for i in range(n)]
    h = v38_solve(ident, [F(1)]*n)
    g = v38_solve(ident, [F(i == origin) for i in range(n)])
    require(all(0 < x <= 5 for x in h), 'exit time bound')
    require(sum(g) == h[origin], 'Green row mass')
    vectors = v38_stopping_vectors(q, origin)
    for m in vectors:
        require(all(0 <= m[i] <= g[i] for i in range(n)), 'Green dominance')
        require(sum(m) <= h[origin], 'occupation mass')
        stop = [F(i == origin)+sum(q[j][i]*m[j] for j in range(n))-m[i]
                for i in range(n)]
        require(all(x >= 0 for x in stop), 'flow feasibility')
    def value(f):
        return max(-v38_dot(f, m) for m in vectors)
    rng = random.Random(38004)
    for _ in range(80):
        f = [F(rng.randrange(-8,9),8) for _ in sites]
        eps = [F(rng.randrange(0,5),32) for _ in sites]
        pert = [F(rng.choice([-1,1]))*e for e in eps]
        f2 = [x+y for x,y in zip(f,pert)]
        v, w = value(f), value(f2)
        require(abs(v-w) <= v38_dot(g, eps), 'arbitrary-data Lipschitz')
        lo = value([x+e for x,e in zip(f,eps)])
        hi = value([x-e for x,e in zip(f,eps)])
        require(lo <= w <= hi, 'interval monotonicity')
    # Discrete analogues only: the target component is isolated from edge mass.
    # Values on the computational boundary are deliberately positive.
    for a in [F(0),F(1,4),F(1,2),F(1)]:
        for b in [F(0),F(1,3),F(1)]:
            physical = {(0,0): a, (1,1): b, (2,1): b, (1,2): b}
            def v(z): return physical.get(z,F(0))
            forcing = []
            for x,y in sites:
                avg = sum(v((x+dx,y+dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])/4
                forcing.append(avg-v((x,y)))
            require(value(forcing) == a, 'nonzero boundary recovery')
    # A non-symmetric, centered lattice law with positive second moment.
    mu = [(-1,F(2,3)),(2,F(1,3))]
    require(sum(a*p for a,p in mu) == 0, 'centered non-symmetric design')
    require(sum(a*a*p for a,p in mu) == 2, 'trace variance')
    # Width and perimeter normalization, and unmatched-component deficits.
    for c in [F(1),F(3,2),F(2)]:
        for r in [F(1,2),F(1),F(3)]:
            for rho in [F(1),F(3,2),F(2)]:
                perimeter_over_pi = 2*(c+rho*r)
                flux_over_t = 2*c
                deficit_over_pi = perimeter_over_pi-flux_over_t
                require(deficit_over_pi == 2*rho*r, 'isotropic deficit')
                require(deficit_over_pi/(2*r) == rho, 'isotropic ratio')
    for m in [9,25,49]:
        for delta in [0.01,0.1,0.5]:
            for eps in [0.01,0.1,0.75]:
                hs=25
                reps=math.ceil(8*hs*hs/eps**2*math.log(4*m/delta))
                logfail=math.log(4*m)-reps*eps*eps/(8*hs*hs)
                require(logfail <= math.log(delta)+1e-12, 'batch confidence algebra')
    for beta in [F(1,4),F(1,2),F(1)]:
        s=6+beta
        require((F(3,2)*s+1)/(s-2) > 2, 'retained stationary rate')
    return {
        "arithmetic": "retained v38 exact stopping-policy and perimeter checks",
        "enumerated_stopping_policies": len(vectors),
        "scope": "All 1796 finite v38 checks are retained here without ancestor imports; finite examples are not continuum proof certificates.",
    }


def v39_trigonometric_powers(normal, maximum):
    """cos(m phi), sin(m phi) at a rational unit normal."""
    result = [(F(1), F(0))]
    for _ in range(maximum):
        cosine, sine = result[-1]
        result.append((cosine * normal[0] - sine * normal[1],
                       sine * normal[0] + cosine * normal[1]))
    return result


def single_law_angular_kernel(checks):
    """Fourier tests of a distribution identity, with pi kept symbolic."""
    def integral_cosine(frequency):
        # The pair (a,b) denotes the exact value a+b*pi.  These are
        # integrals, not normalized Fourier coefficients, over one period.
        if frequency == 0:
            return F(2), F(0)
        if frequency == 1:
            return F(0), F(-1, 2)
        if frequency % 2:
            return F(0), F(0)
        return F(2 * (-1) ** (frequency // 2), 1 - frequency ** 2), F(0)

    normals = rational_unit_normals()
    modes = range(17)
    fourier_cases = odd_cases = 0
    for normal in normals:
        powers = v39_trigonometric_powers(normal, 16)
        for frequency in modes:
            integral = integral_cosine(frequency)
            quarter_turn_cosine = (1, 0, -1, 0)[frequency % 4]
            for projection in powers[frequency]:
                left = tuple((1 - frequency ** 2) * value * projection
                             for value in integral)
                right = (2 * quarter_turn_cosine * projection, F(0))
                checks.require(left == right,
                               "angular resolution loses a unit atom or a quarter-turn sign")
                fourier_cases += 1
        for direction in normals:
            cosine = dot(normal, direction)
            incoming = max(-cosine, F(0))
            opposite = max(cosine, F(0))
            checks.require(incoming - opposite == -cosine,
                           "the odd forward flux has the wrong orientation")
            odd_cases += 1
    checks.require(integral_cosine(0) == (F(2), F(0))
                   and integral_cosine(1) == (F(0), F(-1, 2)),
                   "the zeroth or first angular kernel moment is incorrectly normalized")
    return {
        "arithmetic": "exact rational Fourier tests, with pi retained as a formal coefficient",
        "fourier_test_identities": fourier_cases,
        "odd_forward_flux_identities": odd_cases,
        "largest_test_frequency": 16,
        "scope": "Finite trigonometric test functions exercise k''+k=delta_(pi/2)+delta_(-pi/2); the distributional and L1 arguments remain manuscript proofs.",
    }


def v39_gauss_contact(p, normal):
    powers = v39_trigonometric_powers(normal, 4)
    value, derivative, second_derivative = p[0], F(0), F(0)
    for frequency in range(1, 5):
        cosine, sine = powers[frequency]
        contribution = p[2 * frequency - 1] * cosine + p[2 * frequency] * sine
        value += contribution
        derivative += frequency * (-p[2 * frequency - 1] * sine
                                   + p[2 * frequency] * cosine)
        second_derivative -= frequency ** 2 * contribution
    tangent = (-normal[1], normal[0])
    return add(mul(value, normal), mul(derivative, tangent)), value + second_derivative


def single_law_component_geometry(checks):
    # A non-symmetric positive density on a translated rectangle is allowed
    # by the exact theorem.  It detects the reflection in j(c-x) even though
    # the centered rectangle itself is centrally symmetric.
    half_width = (F(1, 4), F(1, 3))
    shift = (F(2, 7), F(-3, 8))
    density_coefficients = (F(1, 5), F(-1, 7), F(1, 11))
    area = 4 * half_width[0] * half_width[1]
    checks.require(sum(abs(value) for value in density_coefficients) < 1,
                   "the asymmetric rectangle density is not strictly positive")

    def centered_density(z):
        u, v = z[0] / half_width[0], z[1] / half_width[1]
        if abs(u) > 1 or abs(v) > 1:
            return F(0)
        a, b, c = density_coefficients
        return (1 + a * u + b * v + c * u * v) / area

    def original_density(z):
        return centered_density(sub(z, shift))

    corners = tuple((sx * half_width[0], sy * half_width[1])
                    for sx in (-1, 1) for sy in (-1, 1))
    samples = tuple((a * half_width[0], b * half_width[1])
                    for a in (F(-1), F(-1, 3), F(0), F(1, 2), F(1))
                    for b in (F(-1), F(-1, 2), F(0), F(2, 3), F(1)))
    translations = ((F(0), F(0)), (F(5, 3), F(-7, 4)), (F(-13), F(8)))
    bodies = tuple(translated_support(pair[0], displacement)
                   for pair, displacement in zip(support_examples(),
                                                  ((F(0), F(0)), (F(30), F(7)))))
    component_cases = density_cases = pair_cases = gauge_cases = 0
    wrong_reflections = 0
    radii = set()
    normals = rational_unit_normals()
    for direction in normals:
        tangent_normals = ((-direction[1], direction[0]),
                           (direction[1], -direction[0]))
        components = []
        for body in bodies:
            for normal in tangent_normals:
                contact, radius = v39_gauss_contact(body, normal)
                radii.add(radius)
                center = sub(contact, shift)
                component = tuple(sub(contact, add(shift, corner)) for corner in corners)
                component_cases += 1
                checks.require(radius > 0,
                               "a single-law model contact has nonpositive curvature radius")
                checks.require(dot(contact, normal) == evaluate_support(body, normal),
                               "the rational Gauss contact does not attain the body support")
                checks.require(set(mul(-1, sub(point, center)) for point in component)
                               == set(corners),
                               "a translated angular component does not recover the centered footprint")
                # Integrate the density in laboratory coordinates over K.
                # Keeping its first moments explicit detects a misplaced
                # center before the odd polynomial terms cancel.
                lower = tuple(min(point[k] for point in component) for k in range(2))
                upper = tuple(max(point[k] for point in component) for k in range(2))
                lengths = tuple(upper[k] - lower[k] for k in range(2))
                first_moments = tuple((upper[k] ** 2 - lower[k] ** 2) / 2 for k in range(2))
                centered_integrals = tuple((contact[k] - shift[k]) * lengths[k] - first_moments[k]
                                           for k in range(2))
                a, b, mixed = density_coefficients
                mass = radius / area * (lengths[0] * lengths[1]
                                        + a / half_width[0] * centered_integrals[0] * lengths[1]
                                        + b / half_width[1] * centered_integrals[1] * lengths[0]
                                        + mixed / (half_width[0] * half_width[1])
                                        * centered_integrals[0] * centered_integrals[1])
                checks.require(mass == radius,
                               "the resolved density mass does not equal its curvature radius")
                for z in samples:
                    x = sub(center, z)
                    resolved = radius * original_density(sub(contact, x))
                    recovered = resolved / mass
                    checks.require(recovered == centered_density(z) > 0,
                                   "reflection about the component Steiner point loses the density")
                    density_cases += 1
                    wrong_reflections += int(centered_density(z) != centered_density(mul(-1, z)))
                    for translation in translations:
                        shifted_contact = add(contact, translation)
                        shifted_density_argument = sub(sub(shifted_contact, x), translation)
                        checks.require(radius * original_density(shifted_density_argument) == resolved,
                                       "the common-translation observational gauge changes a resolved density")
                        gauge_cases += 1
                checks.require(dot(center, normal)
                               == evaluate_support(translated_support(body, mul(-1, shift)), normal),
                               "the recovered component Steiner point misses the canonical obstacle boundary")
                components.append((body, normal, contact, center, radius))
        for i, (_, _, contact, center, _) in enumerate(components):
            for _, _, other_contact, other_center, _ in components[i + 1:]:
                gap_squared = sum(max(abs(center[k] - other_center[k]) - 2 * half_width[k], F(0)) ** 2
                                  for k in range(2))
                checks.require(gap_squared > 1,
                               "two translated angular density copies overlap in a separated finite model")
                checks.require(sub(contact, other_contact) == sub(center, other_center),
                               "centering changes a pairwise contact displacement")
                pair_cases += 1
        for body in bodies:
            plus, _ = v39_gauss_contact(body, tangent_normals[0])
            minus, _ = v39_gauss_contact(body, tangent_normals[1])
            projected = dot(sub(plus, minus), tangent_normals[0])
            width = sum(evaluate_support(body, normal) for normal in tangent_normals)
            checks.require(projected == width > 4,
                           "opposite contact copies lose the obstacle width separation")
    checks.require(len(radii) > 10 and wrong_reflections > 0,
                   "the component examples do not exercise varying curvature and asymmetric densities")
    return {
        "arithmetic": "rational Fourier support bodies and exact polynomial densities on a rectangle",
        "resolved_components": component_cases,
        "density_recovery_samples": density_cases,
        "common_translation_gauge_samples": gauge_cases,
        "separated_component_pairs": pair_cases,
        "distinct_curvature_radii": len(radii),
        "wrong_density_reflections_detected": wrong_reflections,
        "scope": "Finite exact geometry and density identities; no finite angular sample set is claimed to recover an entire continuum boundary or an arbitrary density norm.",
    }


def single_law_flux_and_weak_error(checks):
    # A rectangle supplies an exactly integrated finite divergence example.
    # It is used only for the projection and translation mechanisms, not as
    # an example satisfying the strict-curvature hypothesis of the theorem.
    a, b, launch_half_width = F(1), F(3, 2), F(8)
    normalization = 4 * launch_half_width ** 2
    area = 4 * a * b
    normals = rational_unit_normals()
    odd_cases = weak_cases = 0
    for linear_x, linear_y, mixed in ((F(1, 5), F(-1, 7), F(1, 11)),
                                     (F(-1, 6), F(1, 4), F(-1, 13))):
        for x in ((F(0), F(0)), (F(1, 3), F(-1, 4)), (F(-1), F(1, 2))):
            vertical = {}
            horizontal = {}
            for sign in (-1, 1):
                zx, zy = sign * a - x[0], -x[1]
                vertical[sign] = 2 * b / normalization * (
                    1 + linear_x * zx / launch_half_width
                    + linear_y * zy / launch_half_width
                    + mixed * zx * zy / launch_half_width ** 2)
                zx, zy = -x[0], sign * b - x[1]
                horizontal[sign] = 2 * a / normalization * (
                    1 + linear_x * zx / launch_half_width
                    + linear_y * zy / launch_half_width
                    + mixed * zx * zy / launch_half_width ** 2)
            gradient = (area / normalization * (-linear_x / launch_half_width
                                                + mixed * x[1] / launch_half_width ** 2),
                        area / normalization * (-linear_y / launch_half_width
                                                + mixed * x[0] / launch_half_width ** 2))
            for direction in normals:
                forward = sum(max(-sign * direction[0], F(0)) * vertical[sign]
                              + max(-sign * direction[1], F(0)) * horizontal[sign]
                              for sign in (-1, 1))
                reverse = sum(max(sign * direction[0], F(0)) * vertical[sign]
                              + max(sign * direction[1], F(0)) * horizontal[sign]
                              for sign in (-1, 1))
                checks.require(forward >= 0 and reverse >= 0
                               and forward - reverse == dot(direction, gradient),
                               "the integrated odd forward flux has an incorrect occupation-gradient sign")
                odd_cases += 1
        mean_launch = (linear_x * launch_half_width / 3,
                       linear_y * launch_half_width / 3)
        incoming_average = (F(-1), F(0))
        direction = (F(1), F(0))
        width = 2 * b
        for length in (F(1, 2), F(1, 8), F(1, 64), F(1, 4096)):
            for gradient in normals:
                boundary_value = width * dot(gradient, sub(incoming_average, mean_launch))
                strip_value = width * dot(gradient, sub(sub(incoming_average,
                                                            mul(length / 2, direction)), mean_launch))
                error = strip_value - boundary_value
                checks.require(error == -length * width * dot(gradient, direction) / 2,
                               "the averaged short-flight weak error has the wrong length coefficient")
                checks.require(abs(error) <= length * width / 2,
                               "the affine weak-flight model exceeds the stated Lipschitz bound")
                weak_cases += 1
    return {
        "arithmetic": "exact rectangle boundary flux and affine test-function integrals",
        "odd_flux_gradient_cases": odd_cases,
        "weak_short_flight_cases": weak_cases,
        "scope": "Finite projection/divergence and weak-bias identities only; the rectangle is not used as a strictly curved obstacle, and no density modulus is inferred.",
    }


def v39_poly_derivative(p):
    return tuple(F(i) * value for i, value in enumerate(p) if i)


def v39_poly_add(p, q):
    return tuple((p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0))
                 for i in range(max(len(p), len(q))))


def v39_poly_multiply(p, q):
    result = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            result[i + j] += a * b
    return tuple(result)


def v39_poly_value(p, x):
    return sum(value * x ** i for i, value in enumerate(p))


def v39_poly_integral(p, left, right):
    return sum(value * (right ** (i + 1) - left ** (i + 1)) / (i + 1)
               for i, value in enumerate(p))


def single_law_regularization(checks):
    chi = tuple(F(315, 256) * (-1) ** (i // 2) * math.comb(4, i // 2)
                if i % 2 == 0 else F(0) for i in range(9))
    checks.require(v39_poly_integral(chi, F(-1), F(1)) == 1,
                   "the compact polynomial kernel is not normalized")
    derivative = chi
    for order in range(4):
        checks.require(v39_poly_value(derivative, F(-1)) == 0
                       and v39_poly_value(derivative, F(1)) == 0,
                       "a kernel endpoint derivative needed for integration by parts does not vanish")
        derivative = v39_poly_derivative(derivative)
    for degree, expected in ((1, F(0)), (2, F(1, 11)), (4, F(3, 143))):
        monomial = (F(0),) * degree + (F(1),)
        checks.require(v39_poly_integral(v39_poly_multiply(chi, monomial), F(-1), F(1)) == expected,
                       "a compact angular kernel moment has an incorrect coefficient")
    ibp_cases = stencil_cases = 0
    signed_stencils = 0
    for eta in (F(1, 2), F(1, 4), F(1, 8), F(1, 16)):
        angular = tuple(value / eta ** (i + 1) for i, value in enumerate(chi))
        second = v39_poly_derivative(v39_poly_derivative(angular))
        resolved = v39_poly_add(angular, second)
        checks.require(v39_poly_integral(resolved, -eta, eta) == 1,
                       "the angular resolution stencil is not of signed mass one")
        for degree in range(13):
            test = (F(0),) * degree + (F(1),)
            derivative_test = v39_poly_derivative(v39_poly_derivative(test))
            left = v39_poly_integral(v39_poly_multiply(resolved, test), -eta, eta)
            right = v39_poly_integral(v39_poly_multiply(angular, v39_poly_add(test, derivative_test)), -eta, eta)
            checks.require(left == right,
                           "angular integration by parts loses a boundary term or an eta factor")
            ibp_cases += 1
        for subdivisions in (4, 8, 16):
            spacing = eta / subdivisions
            weights = [spacing * v39_poly_value(resolved, j * spacing)
                       for j in range(-subdivisions, subdivisions + 1)]
            checks.require(any(weight > 0 for weight in weights)
                           and any(weight < 0 for weight in weights),
                           "the finite angular example does not exercise signed sampling")
            signed_stencils += 1
            # Integral Riemann-error control from the integral of a crude
            # polynomial derivative majorant, all evaluated exactly.
            resolved_derivative = v39_poly_derivative(resolved)
            derivative_integral_bound = sum(2 * abs(value) * eta ** (i + 1) / (i + 1)
                                            for i, value in enumerate(resolved_derivative))
            checks.require(abs(sum(weights) - 1) <= spacing * derivative_integral_bound,
                           "the signed angular quadrature exceeds its explicit variation majorant")
            stencil_cases += 1

    estimator_cases = 0
    # These are finite Bernoulli tables, not a simulated physical sensor.
    # Their probabilities obey the rare-event envelope used in the proof.
    for radius, eta, subdivisions in ((F(1, 2), F(1, 4), 4),
                                      (F(1, 4), F(1, 8), 4),
                                      (F(1, 2), F(1, 8), 8)):
        spatial_step = radius / subdivisions
        one_dimensional = [spatial_step / radius * v39_poly_value(chi, F(i, subdivisions))
                           for i in range(-subdivisions, subdivisions + 1)]
        spatial_weights = [left * right for left in one_dimensional for right in one_dimensional]
        Z = sum(spatial_weights)
        checks.require(all(weight >= 0 for weight in spatial_weights) and F(1, 2) <= Z <= 2,
                       "the spatial stencil is not a positive uniformly normalized law")
        angular = tuple(value / eta ** (i + 1) for i, value in enumerate(chi))
        resolved = v39_poly_add(angular, v39_poly_derivative(v39_poly_derivative(angular)))
        angular_step = eta / subdivisions
        angular_weights = [angular_step * v39_poly_value(resolved, j * angular_step)
                           for j in range(-subdivisions, subdivisions + 1)]
        B = sum(abs(value) for value in angular_weights)
        checks.require(B > 0 and B * eta ** 2 < 20,
                       "the finite signed sampling envelope exceeds the displayed eta power")
        length = radius ** 2 * eta ** 3 / 4
        envelope = length / radius ** 2
        expectation = direct = second_moment = total_probability = F(0)
        for i, spatial_weight in enumerate(spatial_weights):
            for j, angular_weight in enumerate(angular_weights):
                if not spatial_weight or not angular_weight:
                    continue
                command_probability = (spatial_weight / Z) * (abs(angular_weight) / B)
                success_probability = envelope * F(1 + (3 * i + 5 * j) % 7, 8)
                magnitude = Z * B / length
                sign = 1 if angular_weight > 0 else -1
                total_probability += command_probability
                expectation += command_probability * magnitude * sign * success_probability
                second_moment += command_probability * magnitude ** 2 * success_probability
                direct += spatial_weight * angular_weight * success_probability / length
                estimator_cases += 1
        checks.require(total_probability == 1 and expectation == direct,
                       "finite randomized signed sampling does not reproduce the deterministic weak stencil")
        variance = second_moment - expectation ** 2
        checks.require(0 <= variance <= second_moment <= (Z * B / length) ** 2 * envelope,
                       "the rare-event second moment or signed-estimator variance bound fails")
        checks.require(variance * length * radius ** 2 * eta ** 4 <= 1600,
                       "the finite variance does not have the t^-1 r^-2 eta^-4 scaling")
    return {
        "arithmetic": "exact compact-polynomial integrals, signed quadrature, and finite Bernoulli moments",
        "polynomial_integration_by_parts_cases": ibp_cases,
        "signed_quadrature_cases": stencil_cases,
        "signed_stencils": signed_stencils,
        "nonzero_estimator_table_entries": estimator_cases,
        "scope": "Finite regularization and estimator identities. The finite Bernoulli tables are algebraic examples, not a continuous sensor experiment or a finite-sample density estimator.",
    }


def single_law_resource_algebra(checks):
    exponent_cases = confidence_cases = geometric_cases = 0
    for gamma in (F(0), F(1, 4), F(1, 2), F(1), F(2), F(3)):
        flight = gamma + 5
        spatial_step = 2 * gamma + 9
        angular_step = gamma + 5
        rounding = 2 * gamma + 9
        bias_powers = (flight - 3 - 2,
                       spatial_step - 2 - 2 - flight,
                       angular_step - 2 - 3,
                       rounding - 2 - 2 - flight)
        checks.require(bias_powers == (gamma,) * 4,
                       "one of the four finite directional bias terms exceeds its target power")
        variance_cost = flight + 2 + 4 + 2 * gamma
        range_cost = flight + 2 + gamma
        total_cost = variance_cost + 2 + F(1, 2)
        checks.require(variance_cost == 3 * gamma + 11 > range_cost,
                       "the Bernstein range term dominates the claimed variance cost")
        checks.require(total_cost == 3 * gamma + F(27, 2),
                       "the spatial and angular target counts are missing from total attempted-bit cost")
        for beta in (F(1, 4), F(1, 2), F(1)):
            smoothness = 6 + beta
            conversion = smoothness / (smoothness - 2)
            total_nu_power = total_cost * conversion
            coordinate_nu_power = spatial_step * conversion
            checks.require(total_nu_power == (3 * gamma + F(27, 2)) * smoothness / (smoothness - 2)
                           and coordinate_nu_power > flight * conversion,
                           "conversion from Hausdorff accuracy to C2 accuracy loses precision or rate powers")
            exponent_cases += 1
        for inverse_epsilon in (2, 4, 8):
            # Logarithms are kept outside this exact Bernstein denominator
            # check: n >= 2(V+M*tau/3)*log(2K/delta)/tau^2 suffices.
            if gamma.denominator != 1:
                continue
            epsilon = F(1, inverse_epsilon)
            tolerance = epsilon ** gamma.numerator
            V = epsilon ** -(gamma.numerator + 11)
            M = epsilon ** -(gamma.numerator + 7)
            coefficient = 4 * epsilon ** -(3 * gamma.numerator + 11)
            checks.require(coefficient * tolerance ** 2 >= 2 * (V + M * tolerance / 3),
                           "the finite Bernstein coefficient does not attain the simultaneous error exponent")
            confidence_cases += 1
    # For a disk with a rational normal, the exact support deficit is
    # R(1-cos alpha).  Rational tangent-half-angle coordinates give the
    # upper reserve 2R*u^2 without numerical trigonometry.
    for radius in (F(1, 2), F(1), F(2), F(4)):
        for parameter in (F(0), F(1, 64), F(1, 16), F(1, 8), F(1, 4)):
            cosine = (1 - parameter ** 2) / (1 + parameter ** 2)
            deficit = radius * (1 - cosine)
            checks.require(0 <= deficit == 2 * radius * parameter ** 2 / (1 + parameter ** 2)
                           <= 2 * radius * parameter ** 2,
                           "the finite angular support-sampling model loses its quadratic deficit")
            geometric_cases += 1
    return {
        "arithmetic": "exact rational bias, Bernstein, precision and quadratic-support exponents",
        "smoothness_and_density_exponent_cases": exponent_cases,
        "Bernstein_denominator_cases": confidence_cases,
        "angular_support_deficit_cases": geometric_cases,
        "target_attempt_power_in_e": "3*gamma+27/2",
        "target_coordinate_power_in_e": "2*gamma+9",
        "scope": "Finite algebra for the stated geometric finite-reconstruction theorem; no finite density norm, minimax optimality, or continuum sampling theorem is certified.",
    }


def run():
    checks = Checks()
    sections = {}
    for name, function in (
        ("compass_candidates", compass_geometry),
        ("shifted_disk_detector", disk_detector),
        ("killed_adjoint_area", green_area_identity),
        ("unknown_ratio_direct_flux", direct_flux_scale_recovery),
        ("unknown_ratio_mixed_area", mixed_area_scale_recovery),
        ("retained_rate_exponents", rate_algebra),
        ("retained_information_and_density", retained_information_and_density),
        ("global_response_inverse", global_response_inverse),
        ("unregistered_setting_rigidity", unregistered_setting_rigidity),
        ("shrinking_layer_controller", shrinking_layer_controller),
        ("effective_boundary_models", effective_boundary_models),
        ("hellinger_capacity_algebra", hellinger_capacity_algebra),
        ("retained_v38_finite_stencil", retained_v38_finite_stencil),
        ("single_law_angular_kernel", single_law_angular_kernel),
        ("single_law_component_geometry", single_law_component_geometry),
        ("single_law_flux_and_weak_error", single_law_flux_and_weak_error),
        ("single_law_regularization", single_law_regularization),
        ("single_law_resource_algebra", single_law_resource_algebra),
    ):
        before = checks.count
        section = function(checks)
        section["finite_checks"] = checks.count - before
        sections[name] = section
    return {
        "status": "passed",
        "manuscript": "A2-v39-response-rigidity",
        "finite_checks": checks.count,
        "sections": sections,
        "formal_proof_certificate": False,
        "physical_sensor_executed": False,
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
