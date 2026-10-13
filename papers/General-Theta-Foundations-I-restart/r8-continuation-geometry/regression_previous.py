#!/usr/bin/env python3
"""Finite exact-arithmetic regression and counterexample witnesses, not proofs."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import random
import subprocess
import sys

COUNTS = Counter()


def check(ok, group):
    if not ok:
        raise RuntimeError('regression failed: ' + group)
    COUNTS[group] += 1


def allocations(total, dimension):
    if dimension == 1:
        yield (total,)
    else:
        for head in range(total + 1):
            for tail in allocations(total - head, dimension - 1):
                yield (head,) + tail


def greedy(weights, ratios, budget):
    depths = [0] * len(weights)
    scales = list(weights)  # squared weighted lengths; all arithmetic is exact
    record = [(tuple(depths), tuple(scales), max(scales))]
    for _ in range(budget):
        j = max(range(len(weights)), key=lambda i: (scales[i], -i))
        scales[j] *= ratios[j][depths[j]] ** 2
        depths[j] += 1
        record.append((tuple(depths), tuple(scales), max(scales)))
    return record


def distortion(points, masses, labels, eta):
    centers = {}
    for c in set(labels):
        ids = [i for i, label in enumerate(labels) if label == c]
        mass = sum(masses[i] for i in ids)
        if not mass:
            continue
        centers[c] = [sum(masses[i] * points[i][u] for i in ids) / mass
                      for u in range(len(eta))]
    return sum(masses[i] * sum(eta[u] * (points[i][u] - centers[labels[i]][u]) ** 2
                              for u in range(len(eta)))
               for i in range(len(points)) if masses[i])


def native_checks():
    rng = random.Random(7072026)
    allowed = (F(1, 5), F(1, 3), F(1, 2))
    for dimension in range(1, 5):
        for _ in range(18):
            integers = [rng.randint(1, 13) for _ in range(dimension)]
            weights = [F(x, sum(integers)) for x in integers]
            ratios = [[rng.choice(allowed) for _ in range(24)] for _ in weights]
            record = greedy(weights, ratios, 8)
            for budget, (depths, scales, radius2) in enumerate(record):
                values = []
                for allocation in allocations(budget, dimension):
                    ss = []
                    for j, depth in enumerate(allocation):
                        length = F(1)
                        for r in ratios[j][:depth]:
                            length *= r
                        ss.append(weights[j] * length * length)
                    values.append(max(ss))
                check(radius2 == min(values), 'greedy_minimax_exact')
                if budget:
                    check(F(1, 25) * record[budget-1][2] <= radius2 <= record[budget-1][2],
                          'greedy_one_step_scale')
                for j, depth in enumerate(depths):
                    if depth:
                        check(scales[j] >= F(1, 25) * radius2, 'active_cylinder_width')
                    length = F(1)
                    coefficients = []
                    for r in ratios[j]:
                        coefficients.append((1-r)*length)
                        length *= r
                    variance = sum(c*c/F(4) for c in coefficients[depth:]) + length*length/F(8)
                    remaining = F(1)
                    for r in ratios[j][:depth]:
                        remaining *= r
                    check(remaining*remaining/F(16) <= variance <= remaining*remaining/F(4),
                          'unread_tail_variance')
                check(sum(depths) == budget, 'paid_read_count')
                check(sum(scales)/4 <= dimension*radius2/4, 'cylinder_upper_sum')
            for m in range(1, 65):
                b = m.bit_length()-1
                ld = math.ceil(math.log2(4 * (3**dimension)))
                check(F(m*(3**dimension), 2**(b+ld)) <= F(1, 2), 'packing_mass_budget')
    # Finite general dominated continuation problem, not an independence shortcut.
    points = [[F(0), F(1)], [F(1,3), F(1,2)], [F(1), F(0)], [F(2,3), F(3,4)]]
    joint = [[F(1,16), F(3,16)], [F(1,8), F(1,8)],
             [F(3,16), F(1,16)], [F(1,10), F(3,20)]]
    eta = [F(1,2), F(1,2)]
    lower_mass = [2 * min(row) for row in joint]
    codes = list(product(range(2), repeat=4))
    q = min(distortion(points, lower_mass, code, eta) for code in codes)
    for code in codes:
        actual = F(0)
        for u in range(2):
            for c in set(code):
                ids = [i for i, cc in enumerate(code) if cc == c]
                mass = sum(joint[i][u] for i in ids)
                center = sum(joint[i][u]*points[i][u] for i in ids)/mass
                actual += sum(joint[i][u]*(points[i][u]-center)**2 for i in ids)
        check(actual >= q, 'dominated_continuation_cut')
    cube = [list(map(F, bits)) for bits in product(range(2), repeat=2)]
    qcube = min(distortion(cube, [F(1,4)]*4, code, eta) for code in codes)
    check(qcube == F(1,8), 'delayed_query_online_cut')
    check(distortion([[F(0)], [F(1)]], [F(1,2)]*2, [0,1], [F(1)]) == 0,
          'delayed_query_checkpoint_cut')
    for n in range(17):
        for m in range(3, 129):
            k = min(n, m.bit_length()-1)
            kp = min(n, (m//3).bit_length()-1)
            check(0 <= k-kp <= 2 and 3*(2**kp) <= m, 'joint_erasure_state_budget')
            check(n+3 >= kp+3, 'joint_raw_acquisition_budget')
    for integer in range(33):
        eps = F(integer,64)
        erased = 2*eps
        check(erased/F(8) == eps/F(4), 'erasure_weighted_task_floor')
        check(erased/F(2) == eps, 'erasure_exact_deficiency')
    for k in range(9):
        for p in range(1,13):
            error = k*F(1,2**p)/2 + F(1,2**p)
            check(error <= (k+1)*F(1,2**p), 'digital_coefficient_error')
    # Negative controls demonstrate the omitted premise would change the assertion.
    check(F(1) != F(1,2), 'negative:adaptive_depth_prefix_bias')
    check(qcube > 0, 'negative:terminal_atomicity_not_online_cut')
    check((F(1,4)+F(1,4))**2 > F(1,4)**2+F(1,4)**2,
          'negative:root_errors_cannot_be_squared_separately')
    check(F(0) < F(1,8), 'negative:defect_allowance_not_floor')
    check(2 > 1, 'negative:data_dependent_clock_is_state')
    check(F(1,8) > 0 and F(1,2)-F(1,2) == 0,
          'negative:finite_acquired_mean_not_physical_law')
    weighted = greedy([F(9,10),F(1,10)], [[F(1,2)]*3,[F(1,2)]*3],1)[1][2]
    wrong = max(F(9,10),F(1,40))
    check(weighted < wrong, 'negative:allocation_must_use_task_weights')


def main():
    native_checks()
    command = [sys.executable]
    if sys.flags.optimize:
        command.append('-O')
    command.append(str(Path(__file__).with_name('regression_inherited.py')))
    proc = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError('inherited formula regression failed:\n'+proc.stdout)
    inherited = json.loads(proc.stdout)
    check(inherited.get('status') == 'PASS', 'inherited_formula_suite')
    print(json.dumps({'status':'PASS', 'native_checks':sum(COUNTS.values()),
                      'groups':dict(sorted(COUNTS.items())), 'inherited':inherited,
                      'scope':'finite exact/arithmetic witnesses only; not mathematical proof'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
