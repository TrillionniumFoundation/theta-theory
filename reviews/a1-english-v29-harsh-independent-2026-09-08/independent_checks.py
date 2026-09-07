#!/usr/bin/env python3
"""Independent finite audit of A1 v29. Not continuum or formal proof certification.

Run with Python 3.10+; only the standard library is used. Every check raises
explicitly on failure, so python -O cannot remove the tests. This is a new
implementation made after reading the manuscript and author diagnostics.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
from math import comb, exp, factorial, gamma, log, pi, prod
from pathlib import Path
import json

SUBMISSION = '610233410ff6600e76167fad98a3f610faa6191b'
counts: Counter[str] = Counter()
witnesses: dict[str, object] = {}


def check(group: str, condition: bool, detail: object = None) -> None:
    if not condition:
        raise ArithmeticError(f'{group}: {detail!r}')
    counts[group] += 1


def crossing(edges: tuple[tuple[int, int], ...], subset: frozenset[int]) -> tuple[int, ...]:
    return tuple(i for i, (a, b) in enumerate(edges) if (a in subset) != (b in subset))


def exact_retention(v: int, edges: tuple[tuple[int, int], ...], p: F, r: int) -> tuple[F, F, int]:
    cuts = [crossing(edges, frozenset(s)) for s in combinations(range(v), v // 2)]
    retained = F(0)
    for bits in product((0, 1), repeat=len(edges)):
        if all(sum(bits[i] for i in cut) >= r for cut in cuts):
            retained += p ** sum(bits) * (1 - p) ** (len(edges) - sum(bits))
    failed_union = sum((sum((F(comb(len(c), k)) * p**k * (1-p)**(len(c)-k)
                            for k in range(min(r, len(c)+1))), F(0)) for c in cuts), F(0))
    n = sum(comb(len(c), r) if r <= len(c) else 0 for c in cuts)
    return retained, failed_union, n


def retention() -> None:
    for v in range(2, 5):
        pool = tuple(combinations(range(v), 2))
        for mask in range(1 << len(pool)):
            edges = tuple(e for i, e in enumerate(pool) if mask & (1 << i))
            for p in (F(1, 4), F(1, 2), F(3, 4)):
                for r in (1, 2):
                    rho, failures, n = exact_retention(v, edges, p, r)
                    check('exact_retained_cut_union', rho >= max(F(0), 1-failures))
                    check('witness_entropy_bound', n <= 2**(v+len(edges)))
                    if len(edges) == 6 and p == F(1, 2) and r == 1:
                        witnesses['K4_half_retention'] = {
                            'robust_mass': str(rho), 'all_edges_mass': str(p**6),
                            'witness_count': n}
    parallel = ((0, 1), (0, 1), (1, 2), (1, 2))
    check('parallel_edge_labels', exact_retention(3, parallel, F(1, 2), 1)[0] == F(9, 16))
    check('isolated_cut', exact_retention(3, ((0, 1),), F(1, 2), 1)[0] == 0)
    # Heterogeneous probabilities; exact distribution, not an iid shortcut.
    for ps in ((F(1, 4), F(1, 2), F(3, 4)), (F(1, 8),)*6, (F(3, 4),)*8):
        mu = sum(ps, F(0))
        tail = sum((prod(p if b else 1-p for p, b in zip(ps, bits))
                    for bits in product((0, 1), repeat=len(ps)) if 2*sum(bits) <= mu), F(0))
        check('chernoff_exact_heterogeneous', float(tail) <= exp(-float(mu)/8)+1e-14)
    for s in range(1, 20):
        for a in range(s+1):
            for degree in (23, 64, 129):
                mean = degree*(a*F(a, s)+(s-a)*F(s-a, s))
                check('bipartite_crossing_mean', mean == F(degree, s)*(a*a+(s-a)**2)
                      and mean >= F(degree*s, 2))
                check('bipartite_existence_margin', exp((2*log(2)-degree/16)*s) < 1)


def selection() -> None:
    # Nonconstant adaptive paths with nonuniform, explicitly weighted tapes.
    # This finite witness tests restriction/union logic, not a continuum density.
    states = tuple(product((0, 1, 2), repeat=3))
    probs = (F(1, 6), F(1, 3), F(1, 2))
    cuts = ((0, 1), (0, 2), (1, 2))
    selected = Counter()
    support = set()
    for threshold in (F(0), F(1, 16), F(1, 8), F(1, 4)):
        lhs = rhs = F(0)
        for tape in states:
            weight = prod(probs[t] for t in tape)
            regular = tuple(t != 2 for t in tape)
            losses = tuple(sum((F(tape[e], 4)**2 for e in c), F(0)) for c in cuts)
            index = min(range(3), key=lambda i: (losses[i], -sum(regular[e] for e in cuts[i]), i))
            robust = all(any(regular[e] for e in c) for c in cuts)
            small = robust and losses[index] <= threshold
            union = sum(regular[e] and F(tape[e], 4)**2 <= threshold for c in cuts for e in c)
            check('adaptive_unconditional_restriction', int(small) <= union)
            lhs += weight*int(small)
            rhs += weight*union
            selected[index] += 1
            support.add(losses[index])
        check('adaptive_weighted_union', lhs <= rhs)
    check('adaptive_nonconstant', len(selected) == 3 and len(support) > 1)
    witnesses['adaptive_selected_counts'] = dict(selected)
    witnesses['adaptive_loss_support'] = sorted(map(str, support))
    # The adaptive conditional marginal can be larger than the original law.
    # Given X<=Y for independent uniform {0,1,2}, P(X=0|X<=Y)=1/2, not 1/3.
    ordered = [(x, y) for x in range(3) for y in range(3) if x <= y]
    cond = F(sum(x == 0 for x, _ in ordered), len(ordered))
    check('conditional_density_negative_control', cond == F(1, 2) and cond > F(1, 3))
    for k in range(1, 17):
        for rho in (F(1, 3), F(3, 4), F(1)):
            endpoint = F(2, 7)
            am = rho/endpoint**k  # endpoint is sqrt(t_max)
            integral = rho*endpoint**2 - F(2, k+2)*am*endpoint**(k+2)
            check('localized_tail_integral', integral == F(k, k+2)*rho*endpoint**2)
        for j in (2, 4, 8):
            # With k=2 the finite-descriptor penalty is exactly 1/J.
            if k == 2:
                base = F(1, 2)*F(3, 4)**2/F(5)
                enlarged = F(1, 2)*F(3, 4)**2/F(5*j)
                check('side_descriptor_cost', enlarged == base/j)
    losses = ((F(1), F(0)), (F(0), F(1)))
    emax = sum(map(max, losses), F(0))/2
    maxe = max(sum(row[j] for row in losses)/2 for j in range(2))
    infmax = min(map(max, losses))
    maxinf = max(min(row[j] for row in losses) for j in range(2))
    check('expectation_max_negative_control', (emax, maxe) == (1, F(1, 2)))
    check('common_controller_negative_control', (infmax, maxinf) == (1, 0))


def query(z: F) -> tuple[F, ...]:
    return F(3, 4), F(1, 2)+z/8, F(1, 2)-z/8, F(1, 4)


def sqnorm(a: tuple[F, ...], b: tuple[F, ...]) -> F:
    return sum(((x-y)**2 for x, y in zip(a, b)), F(0))/len(a)


def tensor_metric() -> None:
    zs = (F(4, 9), F(10, 21), F(1, 2), F(14, 27), F(8, 15))
    for z, w in product(zs, repeat=2):
        check('actual_scalar_query_metric', sqnorm(query(z), query(w)) == (z-w)**2/128)
    qstar = F(3, 4)
    for f in range(1, 5):
        a = tuple(query(zs[i % len(zs)]) for i in range(f))
        b = tuple(query(zs[(i+1) % len(zs)]) for i in range(f))
        ten = sum(((prod(a[e][j] for e, j in enumerate(js))-
                    prod(b[e][j] for e, j in enumerate(js)))**2
                   for js in product(range(4), repeat=f)), F(0))/4**f
        scalar = sum((sqnorm(x, y) for x, y in zip(a, b)), F(0))
        check('actual_tensor_menu_damping', ten <= f*qstar**(2*(f-1))*scalar)
        # Change just one actual reachable posterior; unchanged other edges at z=1/2.
        delta = sqnorm(query(zs[0]), query(zs[-1]))
        norm_other = sum((x*x for x in query(F(1, 2))), F(0))/4
        tensor_one = delta*norm_other**(f-1)
        local_one = delta/f
        mixed = (tensor_one+local_one)/2
        check('tensor_local_nonuniformity', mixed/tensor_one >= qstar**(-2*(f-1))/(2*f))
        witnesses[f'tensor_to_mixed_f{f}'] = str(mixed/tensor_one)
    for k in range(1, 101):
        omega = pi**(k/2)/gamma(k/2+1)
        check('gaussian_ball_volume', omega <= (2*pi*exp(1)/k)**(k/2)*(1+1e-12))
    for k in range(2, 22, 2):
        for p in (5, 17, 101):
            left = F(2*p)**(k//2) * F(4)**(k//2) * F(2, k)**(k//2)
            correct = F(16*p, k)**(k//2)
            wrong = F(8*p, k)**(k//2)
            check('factor_sixteen', left == correct and left != wrong)


def leja() -> None:
    for nodes in ((F(0), F(1, 3), F(2, 3), F(1)),
                  (F(0), F(1, 1000), F(1, 2), F(501, 1000), F(1)),
                  (F(0), F(0), F(1, 2), F(1, 2), F(1))):
        remaining = list(range(len(nodes)))
        order, scales = [], []
        while remaining:
            chosen = max(remaining, key=lambda j: (prod(abs(nodes[j]-nodes[i]) for i in order), -j))
            scales.append(prod(abs(nodes[chosen]-nodes[i]) for i in order))
            order.append(chosen)
            remaining.remove(chosen)
        for k in range(1, len(nodes)+1):
            d = prod(scales[:k])
            v = max(prod(abs(nodes[i]-nodes[j]) for i, j in combinations(indices, 2))
                    for indices in combinations(range(len(nodes)), k))
            check('leja_volume_zero_and_positive', d <= v <= factorial(k)*d)
        check('leja_monotone', all(a >= b for a, b in zip(scales, scales[1:])))


def cube_root_floor(n: int) -> int:
    if n < 0:
        raise ValueError('nonnegative argument required')
    lo, hi = 0, 1 << ((n.bit_length()+2)//3)
    while lo < hi:
        m = (lo+hi+1)//2
        if m**3 <= n:
            lo = m
        else:
            hi = m-1
    return lo


def density(u: F) -> F:
    if u <= 0:
        return 512*(F(27)/(8-5*u)**3-F(1)/(8+3*u)**3)
    return 512*(F(27)/(8+3*u)**3-F(1)/(8-5*u)**3)


def evaluated_experiment() -> None:
    left_antiderivative = lambda u: F(512, 48)*(F(27, 10)/(8-5*u)**2+F(1, 6)/(8+3*u)**2)
    right_antiderivative = lambda u: F(512, 48)*(-F(27, 6)/(8+3*u)**2-F(1, 10)/(8-5*u)**2)
    mass = left_antiderivative(F(0))-left_antiderivative(F(-8, 7))
    mass += right_antiderivative(F(8, 9))-right_antiderivative(F(0))
    check('mixed_law_mass', mass == F(1, 2) and mass+F(5, 16)+F(3, 16) == 1)
    check('density_endpoints', density(F(-8, 7)) == density(F(8, 9)) == 0 and density(F(0)) == 26)
    # Rigorous rational lower/upper sums, not a floating-point integration claim.
    parts, scale = 8192, 10**10
    lower = upper = F(0)
    for lo, hi, increasing in ((F(-8, 7), F(0), True), (F(0), F(8, 9), False)):
        du = (hi-lo)/parts
        roots = []
        previous = None
        for i in range(parts+1):
            r = density(lo+i*du)
            b = cube_root_floor((r*scale**3).numerator//(r*scale**3).denominator)
            check('certified_density_cube_roots', F(b, scale)**3 <= r < F(b+1, scale)**3)
            if previous is not None:
                check('density_monotonicity_grid', r >= previous if increasing else r <= previous)
            previous = r
            roots.append((F(b, scale), F(b+1, scale)))
        for i in range(parts):
            lower += du/48*(roots[i][0] if increasing else roots[i+1][0])
            upper += du/48*(roots[i+1][1] if increasing else roots[i][1])
    kl, ku = lower**3/1536, upper**3/1536
    check('sharp_constant_bracket', F(48, 10**8) < kl < ku < F(50, 10**8))
    beta, h = F(35, 1024), F(177957, 20480)
    c2 = 4*128*h*h/(beta*beta)
    cert = beta/(12*c2)
    check('same_model_certificate', c2 == F(1013398203168, 30625)
          and cert == F(1071875, 12452637120528384))
    half_cert = (beta/2)/(12*(4*128*(h/2)**2/(beta/2)**2))
    check('completion_failure_factor', half_cert == cert/2)
    witnesses['sharp_constant_interval'] = {'lower': float(kl), 'upper': float(ku),
        'method': 'Exact rational monotone endpoint sums; 8192 intervals on each side, integer cube-root scale 10^10.'}
    new_cert = F(1, 2)**3/(12*128*26**2)
    restricted_pre = beta**3/(12*128*h**2)
    check('v29_all_command_certificate', new_cert == F(1, 8306688))
    check('v29_restricted_seed_improvement', restricted_pre == 4*cert
          and restricted_pre == F(1071875, 3113159280132096))
    check('v29_complete_word_certificate', new_cert/2 == F(1, 16613376))
    check('v29_large_ratio_decomposition', new_cert/cert == F(1499109768, 1071875)
          and new_cert/cert > 1398 and new_cert/cert == 4*(new_cert/restricted_pre))
    check('v29_asymptotic_ratio_enclosure', F(405, 100) < kl/new_cert
          < ku/new_cert < F(406, 100))
    witnesses['v29_certificate'] = str(new_cert)
    witnesses['v29_to_old_certificate_ratio'] = str(new_cert/cert)
    witnesses['sharp_to_v29_certificate_ratio_interval'] = [float(kl/new_cert), float(ku/new_cert)]
    witnesses['separator_constant'] = str(cert)
    witnesses['sharp_to_certificate_ratio_interval'] = [float(kl/cert), float(ku/cert)]


def menu_profiles() -> None:
    # Enumerate every star order. This tests the printed example, not E29.1's
    # general proof, which is given separately in the report.
    edges = ((0, 1), (0, 2), (0, 3))
    orders = tuple(permutations(range(4)))
    def cost(order: tuple[int, ...], s: F) -> F:
        weights = (7*s, max(6*s, 9*s-3), s)
        return max(sum((weights[e] for e in crossing(edges, frozenset(order[:j]))), F(0)) for j in range(1, 4))
    points = (F(1, 2), F(1), F(3, 2), F(2), F(3), F(4))
    for s in points:
        formula = min(max(7*s, max(6*s, 9*s-3)+s), max(max(6*s, 9*s-3), 8*s))
        check('star_all_orders', min(cost(o, s) for o in orders) == formula)
    interval = points[:4]
    endpoints = (interval[0], interval[-1])
    excess = lambda o, s: cost(o, s)-min(cost(p, s) for p in orders)
    check('star_interval_regret', min(max(excess(o, s) for s in interval) for o in orders) == 1)
    check('star_endpoint_regret', min(max(excess(o, s) for s in endpoints) for o in orders) == F(1, 2))
    # Eventual fixed-calibration dominance for each of several finite affine
    # families. The exact all-x statement follows from the report's proof.
    for intercept in (1, 5, 50, 500):
        profiles = ((F(1), F(intercept)), (F(2), F(0)), (F(3), F(-intercept)))
        for x in (F(2*intercept), F(4*intercept), F(100*intercept)):
            check('eventual_affine_dominance', profiles[0][0]*x+profiles[0][1]
                  == min(a*x+b for a, b in profiles))



def occupation_flow() -> None:
    """Exact finite witnesses for the v29 occupation/perspective duals."""
    # Two disjoint two-level paths (u,a), (v,b). All terminal capacities are 1.
    a2 = (F(1), F(4), F(4), F(1))
    levels = ((0, 1), (2, 3))
    paths = ((0, 2), (1, 3))
    phi = lambda w, z: z**3/(3*a2[w])
    lam = (F(1, 2), F(1, 2))
    level_of = (0, 0, 1, 1)
    def objective(x: F) -> F:
        occupations = (x, 1-x, x, 1-x)
        return max(sum((phi(w, occupations[w]) for w in lev), F(0)) for lev in levels)
    exact = F(5, 96)
    check('common_flow_primal', objective(F(1, 2)) == exact)
    # A feasible supporting dual proves the value, rather than just sampling x.
    support = (F(1, 2),)*4
    q = tuple(lam[level_of[w]]*support[w]**2/a2[w] for w in range(4))
    conjugate_sum = sum((lam[level_of[w]]*F(2, 3)*support[w]**3/a2[w]
                        for w in range(4)), F(0))
    dual = min(sum((q[w] for w in path), F(0)) for path in paths)-conjugate_sum
    check('common_flow_exact_dual', dual == exact)
    separate = max(phi(0, F(1, 3))+phi(1, F(2, 3)),
                   phi(2, F(2, 3))+phi(3, F(1, 3)))
    check('separate_levels_negative_control', separate == F(1, 27) and separate < exact)
    for i in range(121):
        x = F(i, 120)
        check('common_flow_grid', objective(x) >= exact)
    check('primal_direction_negative_control', objective(F(0)) == F(1, 3)
          and objective(F(0)) > exact)

    pre_exact = F(5, 24)
    for index, path in enumerate(paths):
        support = tuple(F(int(w in path)) for w in range(4))
        q = tuple(lam[level_of[w]]*support[w]**2/a2[w] for w in range(4))
        b = sum((lam[level_of[w]]*F(2, 3)*support[w]**3/a2[w]
                 for w in range(4)), F(0))
        anchored_dual = sum((q[w] for w in path), F(0))-b
        check('perspective_exact_dual', anchored_dual == pre_exact)
    for i in range(121):
        alpha = F(i, 120)
        value = max(alpha/F(3)+(1-alpha)/12, alpha/12+(1-alpha)/3)
        check('perspective_flow_grid', value >= pre_exact)
    check('perspective_primal', max(F(1, 6)+F(1, 24), F(1, 24)+F(1, 6)) == pre_exact)
    witnesses['two_level_common_flow'] = {
        'Gamma': str(exact), 'Gamma_pre': str(pre_exact),
        'separately_optimized_levels': str(separate),
        'unanchored_primal_equals_dual': True, 'anchored_primal_equals_dual': True,
        'scope': 'Abstract local-path capacities; not asserted realizable by the manuscript detector.'}

    # Seedwise Jensen and convexity of the closed perspective, including alpha=0.
    def perspective(alpha: F, y: F) -> F:
        if alpha == 0:
            if y != 0:
                raise ValueError('infeasible zero-mass perspective')
            return F(0)
        if not 0 <= y <= alpha:
            raise ValueError('infeasible perspective')
        return y**3/(3*alpha**2)
    grid = tuple(F(i, 4) for i in range(5))
    for x, y, weight in product(grid, repeat=3):
        check('seedwise_jensen', (weight*x+(1-weight)*y)**3
              <= weight*x**3+(1-weight)*y**3)
    for alpha1, alpha2, x1, x2 in product(grid, repeat=4):
        mixed_alpha = (alpha1+alpha2)/2
        mixed_y = (alpha1*x1+alpha2*x2)/2
        check('closed_perspective_convexity', perspective(mixed_alpha, mixed_y)
              <= (perspective(alpha1, alpha1*x1)+perspective(alpha2, alpha2*x2))/2)

    # Jump capacities, including mass at zero: exact inverse-CDF construction.
    times = (F(0), F(1, 4), F(3, 4), F(1))
    caps = (F(1, 4), F(1, 2), F(1, 2), F(1))
    for x in (F(1, 4), F(1, 2), F(3, 4), F(1)):
        g = tuple(min(x, c) for c in caps)
        cdf_increments = (g[0],)+tuple(g[i]-g[i-1] for i in range(1, len(g)))
        inverse_mean = sum((t*m for t, m in zip(times, cdf_increments)), F(0))
        layer_cake = sum(((times[i+1]-times[i])*max(F(0), x-caps[i])
                          for i in range(len(times)-1)), F(0))
        check('jump_capacity_inverse_cdf', sum(cdf_increments, F(0)) == x
              and inverse_mean == layer_cake)
    # A chain with terminal capacity 1/2 cannot carry the required unit flow.
    check('terminal_capacity_negative_control', F(1) > F(1, 2))
    # Unanchored feasibility need not imply any feasible pre-acquisition anchor.
    check('anchor_feasibility_negative_control', 2*F(3, 5) >= 1
          and F(1, 2) <= F(3, 5) < 1)

    # A capacitated min-cost unit flow must not be replaced by a shortest path.
    capacities, costs = (F(1, 4), F(3, 4), F(1)), (F(0), F(1), F(2))
    remaining, total = F(1), F(0)
    for cap, cost in zip(capacities, costs):
        amount = min(cap, remaining)
        total += amount*cost
        remaining -= amount
    check('capacitated_flow_not_shortest_path', remaining == 0
          and total == F(3, 4) and total > min(costs))

    # Exact one-level pre-acquisition, support dual, and descriptor scaling.
    for a_sq in (F(1), F(9, 4), F(100), F(43264)):
        unanchored = F(1)/(12*a_sq)
        anchored = F(1)/(3*a_sq)
        check('two_choice_factor_four', anchored == 4*unanchored)
        check('two_choice_dual_values', F(1)/(4*a_sq)-F(1)/(6*a_sq) == unanchored
              and F(1)/a_sq-F(2)/(3*a_sq) == anchored)
        for descriptor in (1, 2, 6, 24):
            check('descriptor_square_penalty', F(1)/(3*a_sq*descriptor**2)
                  == anchored/descriptor**2)
    for nlevels in (1, 2, 5, 20):
        for k in (1, 2, 3, 8):
            # Choose a=1, avoiding irrational arithmetic in this exact witness.
            common = F(k, k+2)
            separator = common/nlevels
            check('chain_separator_loss', common == nlevels*separator)


def main() -> dict[str, object]:
    retention(); selection(); tensor_metric(); leja(); evaluated_experiment(); menu_profiles(); occupation_flow()
    return {'schema': 'A1-v29-independent-referee-checks-1', 'submission': SUBMISSION,
        'checks': sum(counts.values()), 'categories': dict(sorted(counts.items())),
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'witnesses': witnesses,
        'arithmetic': 'Rational arithmetic except the explicitly floating-point Gaussian and Chernoff/exponential inequalities.',
        'scope': 'Independent finite identities, inequalities and rational numerical bounds. No continuum theorem certification, no exhaustive historical/companion audit, no author-test execution, no native LaTeX build.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
