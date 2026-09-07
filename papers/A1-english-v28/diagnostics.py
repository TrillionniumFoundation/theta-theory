#!/usr/bin/env python3
"""Exact finite witnesses for v26, not a proof checker or a LaTeX receipt."""
from __future__ import annotations
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

COUNTS: Counter[str] = Counter()


def require(condition: bool, category: str, detail: str) -> None:
    COUNTS[category] += 1
    if not condition:
        raise RuntimeError(category + ': ' + detail)


def coefficients(blocks: list[list[F]]) -> list[F]:
    """Capped max-product convolution, with a zero allocation in each block."""
    result = [F(1)]
    for block in blocks:
        new = [F(0)] * (len(result) + len(block) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(block):
                new[i + j] = max(new[i + j], a * b)
        result = new
    return result


def cut_cost(n: int, edges: list[tuple[int, int, F]], mask: int) -> F:
    return sum((w for a, b, w in edges
                if bool(mask & (1 << a)) != bool(mask & (1 << b))), F(0))


def order_cost(n: int, edges: list[tuple[int, int, F]], order: tuple[int, ...]) -> F:
    mask, best = 0, F(0)
    for x in order:
        mask |= 1 << x
        best = max(best, cut_cost(n, edges, mask))
    return best


def subset_dp(n: int, costs: dict[int, F]) -> tuple[F, tuple[int, ...]]:
    f, parent = {0: F(0)}, {}
    for mask in sorted(range(1, 1 << n), key=lambda x: (x.bit_count(), x)):
        candidates = [(f[mask ^ (1 << x)], x) for x in range(n) if mask & (1 << x)]
        value, x = min(candidates)
        f[mask] = max(costs[mask], value)
        parent[mask] = x
    order, mask = [], (1 << n) - 1
    while mask:
        x = parent[mask]
        order.append(x)
        mask ^= 1 << x
    return f[(1 << n) - 1], tuple(reversed(order))


def lattice_paths(n: int) -> list[tuple[int, ...]]:
    out = []
    for order in permutations(range(n)):
        mask, path = 0, []
        for x in order[:-1]:
            mask |= 1 << x
            path.append(mask)
        out.append(tuple(path))
    return out


def separator_bruteforce(n: int, caps: dict[int, F]) -> F:
    nodes, paths = list(caps), lattice_paths(n)
    best = sum(caps.values(), F(0))
    for bits in range(1 << len(nodes)):
        chosen = {x for j, x in enumerate(nodes) if bits & (1 << j)}
        if all(chosen.intersection(path) for path in paths):
            best = min(best, sum((caps[x] for x in chosen), F(0)))
    return best


def split_flow(n: int, caps: dict[int, F]) -> F:
    """Independent exact Edmonds--Karp implementation on a vertex-split lattice."""
    residual: dict[tuple[str, int], dict[tuple[str, int], F]] = {}
    full = (1 << n) - 1
    source, sink = ('s', 0), ('t', full)
    big = F(1) + sum(caps.values(), F(0))

    def entry(mask: int) -> tuple[str, int]:
        return source if mask == 0 else sink if mask == full else ('i', mask)

    def exit_(mask: int) -> tuple[str, int]:
        return source if mask == 0 else sink if mask == full else ('o', mask)

    def arc(a: tuple[str, int], b: tuple[str, int], c: F) -> None:
        residual.setdefault(a, {})[b] = residual.setdefault(a, {}).get(b, F(0)) + c
        residual.setdefault(b, {}).setdefault(a, F(0))

    for mask, c in caps.items():
        arc(entry(mask), exit_(mask), c)
    for mask in range(1 << n):
        for x in range(n):
            if not mask & (1 << x):
                arc(exit_(mask), entry(mask | (1 << x)), big)
    value = F(0)
    while True:
        previous = {source: None}
        queue = deque([source])
        while queue and sink not in previous:
            a = queue.popleft()
            for b, capacity in residual[a].items():
                if capacity > 0 and b not in previous:
                    previous[b] = a
                    queue.append(b)
        if sink not in previous:
            return value
        b, path = sink, []
        while b != source:
            a = previous[b]
            if a is None:
                raise RuntimeError('Broken augmenting path')
            path.append((a, b))
            b = a
        amount = min(residual[a][b] for a, b in path)
        for a, b in path:
            residual[a][b] -= amount
            residual[b][a] += amount
        value += amount


def star_weights(s: F) -> tuple[F, F, F]:
    return 7*s, max(6*s, 9*s-3), s


def star_phase(s: F) -> F:
    if s <= 1:
        return 7*s
    if s <= F(3, 2):
        return 10*s-3
    if s <= 3:
        return 8*s
    return 9*s-3


def multiply(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def word_evidence(word: tuple[int, ...]) -> F:
    # Uniform latent t in [0,1], fixed-command positive detector.
    poly = [F(1)]
    for report in word:
        poly = multiply(poly, [F(1,2), F(1,4) if report == 1 else F(-1,4)])
    return sum((a/F(i+1) for i, a in enumerate(poly)), F(0))


def run() -> dict:
    losses = ((F(1), F(0)), (F(0), F(1)))
    expectation_of_max = sum(map(max, losses), F(0))/2
    max_of_expectations = max(sum(row[j] for row in losses)/2 for j in range(2))
    inf_max = min(map(max, losses))
    max_inf = max(min(row[j] for row in losses) for j in range(2))
    require(expectation_of_max == 1 and max_of_expectations == F(1,2),
            'quantifiers', 'actual expectation/max operations')
    require(inf_max == 1 and max_inf == 0, 'quantifiers', 'actual controller/checkpoint operations')
    correct = coefficients([[F(1), F(1)], [F(1), F(1), F(1,4)]])
    moved = coefficients([[F(1), F(1), F(1,16)], [F(1), F(1)]])
    require(len(correct) == len(moved) == 4, 'individual_caps', 'same total cap')
    require(correct[3] == F(1,4) and moved[3] == F(1,16),
            'individual_caps', 'same-index coefficient really changes')
    for a, b, c in product((F(0), F(1,16), F(1,4), F(1)), repeat=3):
        blocks = [[F(1), F(1), a], [F(1), b], [F(1), c]]
        coeff = coefficients(blocks)
        for x in (F(1,2), F(1), F(2), F(4), F(8)):
            direct = max(v*x**k for k, v in enumerate(coeff))
            factored = F(1)
            for block in blocks:
                factored *= max(v*x**k for k, v in enumerate(block))
            require(direct == factored, 'capped_factorization', 'max-product identity including zeros')
    graphs = 0
    for n in range(2,5):
        possible = list(combinations(range(n), 2))
        for bits in range(1 << len(possible)):
            edges = [(a,b,F(1+(i%3),2)) for i,(a,b) in enumerate(possible) if bits & (1<<i)]
            costs = {mask:cut_cost(n,edges,mask) for mask in range(1<<n)}
            dynamic, order = subset_dp(n, costs)
            exhaustive = min(order_cost(n,edges,pi) for pi in permutations(range(n)))
            require(dynamic == exhaustive, 'subset_recursion', 'weighted graph DP/exhaustive')
            require(order_cost(n,edges,order) == exhaustive, 'subset_recursion', 'backtracked order')
            graphs += 1
    parallel = [(0,1,F(1)), (0,1,F(2)), (1,2,F(1,3))]
    for n in (3,4):
        costs={m:cut_cost(n,parallel,m) for m in range(1<<n)}
        optimum, order=subset_dp(n,costs)
        require(optimum == min(order_cost(n,parallel,p) for p in permutations(range(n))),
                'subset_recursion', 'parallel edges and isolated vertex')
    for n in (2,3):
        nodes=list(range(1,(1<<n)-1))
        for seed in range(18):
            caps={m:F((m*7+seed*3)%11,10) for m in nodes}
            require(split_flow(n,caps) == separator_bruteforce(n,caps),
                    'separator_flow', 'exact flow versus all separating sets')
    # Genuine discrete subprobability, with arbitrary path selection.
    paths=lattice_paths(3)
    outcomes=[(paths[i%6], (F((i*7)%5),F((i*3+1)%7))) for i in range(24)]
    good=[i for i in range(24) if i%5 != 0]
    beta=F(len(good),24)
    for t in (F(0),F(1),F(2),F(3),F(5),F(7)):
        caps={m:F(sum(1 for i in good if any(x==m and outcomes[i][1][j]<=t
                     for j,x in enumerate(outcomes[i][0]))),len(good)) for m in range(1,7)}
        h=separator_bruteforce(3,caps)
        actual=F(sum(1 for i in good if max(outcomes[i][1])>t),24)
        require(actual >= beta*max(F(0),1-h), 'selected_subprobability', 'unconditioned tail')
    evidence_witness={}
    for n,m in product(range(1,4),repeat=2):
        first=(1,)*n
        marginal=sum((word_evidence(first+tail) for tail in product((0,1),repeat=m)),F(0))
        mass=word_evidence(first)
        all_fail=word_evidence(first+(1,)*m)
        require(marginal==mass, 'evidence_marginalization', 'completion reports sum to one')
        require(all_fail < mass < 1, 'evidence_marginalization', 'first-only event strictly larger')
        if (n,m)==(2,2):
            evidence_witness={'first_block':str(mass),'summed_completions':str(marginal),'all_failures':str(all_fail)}
    nodes=[(1,0),(2,0),(2,1),(3,0),(3,1),(4,1),(4,2),(5,2),(6,3)]
    valuations=[]
    for ell in range(1,10):
        val=min(sum(1 for i,j in combinations(indices,2) if nodes[i][0]==nodes[j][0])
                for indices in combinations(range(9),ell))
        valuations.append(val)
        require(val == max(0,ell-6), 'contact_orders', 'all determinant subsets')
    orders=list(permutations(range(4)))
    samples=sorted({F(i,24) for i in range(1,145)}|{F(3,2)})
    for s in samples:
        w=star_weights(s)
        edges=[(0,i+1,w[i]) for i in range(3)]
        costs=[order_cost(4,edges,pi) for pi in orders]
        require(min(costs)==star_phase(s), 'star_full_phase', 'all 24 vertex orders')
        dp,_=subset_dp(4,{m:cut_cost(4,edges,m) for m in range(16)})
        require(dp==star_phase(s), 'star_full_phase', 'independent subset recursion')
    interval=[F(1,2),F(1),F(3,2),F(2)]
    endpoint=[F(1,2),F(2)]
    def regret(points: list[F]) -> F:
        return min(max(order_cost(4,[(0,i+1,star_weights(s)[i]) for i in range(3)],pi)
                       -star_phase(s) for s in points) for pi in orders)
    require(regret(interval)==1, 'uniform_resolution_regret', 'full interval breakpoints')
    require(regret(endpoint)==F(1,2), 'uniform_resolution_regret', 'two endpoints only')
    slopes=[(star_phase(b)-star_phase(a))/(b-a) for a,b in
            ((F(1,4),F(3,4)),(F(9,8),F(11,8)),(F(7,4),F(5,2)),(F(4),F(5)))]
    require(slopes==[7,10,8,9], 'star_full_phase', 'four exact slopes; nonconvex drop')
    for exponent in (1,2,3):
        for threshold in (F(1,4),F(1,2),F(1)):
            a=F(1,3); beta=a*threshold**exponent; k=2*exponent
            integral=beta*threshold-a*threshold**(exponent+1)/(exponent+1)
            require(integral==F(k,k+2)*beta*threshold,
                    'finite_selection_integral', 'homogeneous layer-cake constant')
    return {'version':26,'status':'passed','checks':sum(COUNTS.values()),
            'categories':dict(sorted(COUNTS.items())), 'simple_graphs':graphs,
            'witnesses':{'expectation_of_max':str(expectation_of_max),
                         'max_of_expectations':str(max_of_expectations),
                         'inf_max':str(inf_max),'max_inf':str(max_inf),
                         'same_total_cap_correct':[str(x) for x in correct],
                         'same_total_cap_moved':[str(x) for x in moved],
                         'first_block_evidence':evidence_witness,
                         'contact_orders':valuations,'star_slopes':[str(x) for x in slopes],
                         'interval_regret':str(regret(interval)), 'endpoint_regret':str(regret(endpoint))},
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Executed finite exact-arithmetic witnesses. Not a proof of continuum acquisition, causal minimax classification, LaTeX compilation, or independent peer review.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
