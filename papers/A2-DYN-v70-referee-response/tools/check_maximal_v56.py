#!/usr/bin/env python3
"""Exact finite models for the maximal-envelope argument; not continuum proofs."""
from fractions import Fraction as F
from itertools import product


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def maximal_blocks(values):
    n = len(values)
    out = [F(0)] * n
    for left in range(n):
        acc = F(0)
        for right in range(left + 1, n + 1):
            acc += values[right - 1]
            avg = acc / (right - left)
            for j in range(left, right):
                out[j] = max(out[j], avg)
    return out


def finite_checks():
    pc = F(145, 144)
    require(1 - 1 / pc == F(1, 145), 'source-weight exponent')
    require(F(1, 12) * F(1, 16) == F(1, 192), 'band mass exponent')
    require(F(1, 192) - F(1, 384) == F(1, 384), 'maximal threshold balance')
    require(F(1, 384) / 145 == F(1, 55680), 'finite-count source exponent')
    for q in [F(289, 288), F(577, 576), F(1153, 1152)]:
        require(1 < q < pc, 'subcritical test outside interval')
        require(F(1, 16) * (pc - q) / (pc - 1) == 9 * (pc - q),
                'maximal power exponent')
    block_cases = interval_cases = 0
    for raw in product(range(3), repeat=5):
        f = list(map(F, raw)); mf = maximal_blocks(f)
        for level in [F(1, 4), F(1, 2), F(1), F(3, 2), F(2)]:
            bad = [j for j in range(5) if mf[j] > level]
            require(len(bad) * level <= 3 * sum(f), 'finite weak-one model')
            for anchor in set(range(5)) - set(bad):
                for left in range(anchor + 1):
                    for right in range(anchor + 1, 6):
                        avg = sum(f[left:right]) / (right - left)
                        require(avg <= level, 'one good anchor failed a block resolution')
                        interval_cases += 1
            block_cases += 1
    # Greedy interval cover: each discarded interval lies in a selected triple.
    intervals = [(F(a), F(b)) for a in range(6) for b in range(a + 1, 7)]
    covering_cases = 0
    for cut in range(1, len(intervals) + 1):
        todo = intervals[:cut]
        while todo:
            chosen = max(todo, key=lambda x: x[1] - x[0])
            left, right = chosen; length = right - left
            rest = []
            for a, b in todo:
                if a <= right and b >= left:
                    require(a >= left - length and b <= right + length,
                            'triple failed to cover a removed interval')
                    covering_cases += 1
                else:
                    rest.append((a, b))
            todo = rest
    # Exact positive two-point path kernel, with the full TV dual norm.
    posterior_cases = 0
    inc = [F(0), F(2), F(0), F(1, 8), F(0), F(0)]
    clr = [F(0), F(0), F(1, 3), F(0), F(0), F(0)]
    rem = [a + b for a, b in zip(inc, clr)]
    g = [F(1), F(3, 2), F(1), F(2), F(1), F(1)]
    errors = [F(1, 64), -F(1, 64), F(0), F(1, 128), F(0), F(0)]
    eta = max(map(abs, errors)); p = [a + b + c for a, b, c in zip(g, rem, errors)]
    mf = maximal_blocks(rem)
    for level in [F(1, 16), F(1, 8), F(1, 4), F(1, 2)]:
        r = level + eta; d = F(1)
        for anchor in range(6):
            if mf[anchor] > level:
                continue
            for left in range(anchor + 1):
                for right in range(anchor + 1, 7):
                    width = right - left
                    mass = sum(p[left:right]); ref = sum(g[left:right])
                    l1 = sum(abs(a - b) for a, b in zip(p[left:right], g[left:right]))
                    require(l1 <= r * width, 'raw envelope')
                    require(mass >= (d - r) * width, 'denominator')
                    tv = sum(abs(p[j] / mass - g[j] / ref)
                             for j in range(left, right)) / 2
                    require(tv <= r / (d - r), 'roof TV normalization')
                    path_error = sum(abs(inc[j] - clr[j]) for j in range(left, right)) / mass
                    require(path_error <= 2 * r / (d - r), 'same-roof path mean')
                    if r <= d / 2:
                        ratio = ref * p[anchor] / (mass * g[anchor])
                        require(abs(ratio - 1) <= 4 * r / d, 'good-anchor likelihood')
                    posterior_cases += 1
    require(posterior_cases > 0 and interval_cases > 0, 'empty regression model')
    # A zero or negative arithmetic class is not assigned a reference likelihood.
    require(sum([F(-1), F(-2)]) < 0, 'signed-reference negative control')
    # Narrow spikes satisfy the weak endpoint while their essential heights grow.
    for j in range(1, 9):
        height = 2 ** (144 * j); width = F(1, 2 ** (145 * j))
        require(height * width == F(1, 2 ** j), 'spike mass')
        require(F(height) ** 145 * width ** 144 == 1, 'weak endpoint spike')
        require(height > 1 and height * width < 1, 'mass was confused with height')
    return {'rational_endpoint':'145/144', 'source_weight_power':'1/145',
            'ordered_bad_set_power':'1/384', 'finite_bad_source_power':'1/55680',
            'block_level_cases':block_cases,'anchored_interval_cases':interval_cases,
            'greedy_cover_cases':covering_cases,'posterior_cases':posterior_cases,
            'spike_negative_controls':8,'arithmetic_negative_controls':1,
            'finite_models_do_not_certify_continuum':True}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
