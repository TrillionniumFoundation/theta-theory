#!/usr/bin/env python3
"""Independent finite controls for A2 commit 070aa946 (v40).

No repository mathematics is imported. These are finite algebraic and model
checks, not a proof of the billiard theorems or a native manuscript build.
All checks use explicit exceptions, so python -O preserves the checks.
"""
from fractions import Fraction as F
import json
from itertools import product
import math
import platform


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inverse2(a):
    d = a[0][0]*a[1][1] - a[0][1]*a[1][0]
    require(d != 0, 'singular test matrix')
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def algebra():
    green_cases = jet_cases = lattice_cases = 0
    for t in [F(1, 2), F(2, 3), F(3, 4)]:
        c = (t + 1/t)/2
        for r in [F(1), (1+c)/2]:
            cs = [c*r, c/r]
            require(min(cs) > 1, 'nonpositive test curvature')
            for b in [0, 1]:
                def green(i, k):
                    if i == 0:
                        return F(0)
                    # sigma_i^2 = c_{1-((b+i) mod 2)}.
                    sigprod = cs[1-((b+i) % 2)] if i % 2 == k % 2 else c
                    return sigprod/(c*(1/t-t))*(t**abs(i-k)-t**(i+k))
                for i in range(1, 9):
                    for k in range(1, 9):
                        val = -green(i-1, k)+2*cs[(b+i) % 2]*green(i, k)-green(i+1, k)
                        require(val == int(i == k), 'half-line Green jump failed')
                        green_cases += 1
            for n in range(3, 21):
                d = (1+t**(2*n))/(1-t**(2*n))
                u = 2*r**n*t**n/(1-t**(2*n))
                v = 2*r**(-n)*t**n/(1-t**(2*n))
                require(d*d-u*v == 1, 'last-jet determinant failed')
                require(matmul([[d,u],[v,d]], [[d,-u],[-v,d]]) == [[1,0],[0,1]], 'inverse block failed')
                jet_cases += 1
    J = [[F(1),F(0)],[F(0),F(-1)]]
    R = [[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    for L in [[[F(3),F(1)],[F(0),F(2)]], [[F(2),F(-1)],[F(1),F(3)]]]:
        for M in [[[F(2),F(0)],[F(0),F(3)]], [[F(2),F(1)],[F(1),F(2)]]]:
            V = matmul(L, M)
            require(matmul(V, inverse2(M)) == L, 'marked lattice inverse failed')
            reflected = matmul(matmul(J,V), inverse2(M))
            require(reflected == matmul(J,L), 'reflection-equivariance failed')
            require(matmul(transpose(reflected),reflected) == matmul(transpose(L),L), 'Gram invariance failed')
            require(matmul(matmul(R,V),inverse2(M)) == matmul(R,L), 'common-frame covariance failed')
            lattice_cases += 1
    return {'half_line_green_exact_cases':green_cases, 'jet_block_exact_cases':jet_cases,
            'lattice_exact_cases':lattice_cases, 'arithmetic':'exact rational', 'passed':True}


def geometric_hellinger():
    rows = []
    for p in [1e-6, 1e-3, 0.05, 0.2, 0.45]:
        for shift in [-0.7, -0.15, 0.1]:
            q = p*math.exp(shift)
            require(max(p,q) <= 0.5, 'outside chosen probability bound')
            # Rationalize the affinity denominator to avoid cancellation.
            affinity = math.sqrt(p*q)*(1+math.sqrt((1-p)*(1-q)))/(p+q-p*q)
            h2 = 2*(1-affinity)
            bound = shift*shift/(4*(1-0.5))
            require(-1e-12 <= h2 <= bound+1e-12, 'geometric Hellinger inequality failed')
            rows.append({'p':p,'log_q_over_p':shift,'H2_over_bound':h2/bound})
    return {'cases':len(rows),'max_H2_over_bound':max(x['H2_over_bound'] for x in rows),
            'convention':'H2 = integral (sqrt(p)-sqrt(q))^2','passed':True}


def layer_corner():
    # Exact normalized model: q = 2/[pi*(1-z/k)^2] on
    # 0<r<1-u^2-v^2-z/k. Reference layer y=k*(1-u^2-v^2-r).
    # pi factors cancel. R=3, z in {-1,0,1}; k>R.
    rows = []
    R = F(3)
    for k_int in [16, 64, 256, 1024]:
        k = F(k_int)
        for z in [F(-1),F(0),F(1)]:
            c0, cz = F(2), 2/(1-z/k)**2
            cuts = sorted(set([z, R] + ([F(0)] if z < 0 else [])))
            variation = F(0)
            for lo,hi in zip(cuts,cuts[1:]):
                dy = hi-lo
                iy = (hi*hi-lo*lo)/2
                if hi <= 0:
                    variation += abs(cz-c0)*dy + cz*(-iy)/k
                else:
                    variation += abs(cz-c0)*(dy-iy/k) + c0*iy/k
            kp = cz*((R-z)-(R*R-z*z)/(2*k))
            require(variation >= 0 and 0 < kp/k < 1, 'invalid layer probability')
            require(k*variation < 30, 'model corner/trace bound failed')
            rows.append({'k':k_int,'z':int(z),'k_times_intensity_variation':float(k*variation),
                         'k_times_layer_probability':float(kp)})
    return {'cases':len(rows),'max_k_times_intensity_variation':max(x['k_times_intensity_variation'] for x in rows),
            'bulk_H2':0,'rows':rows,'passed':True}


def trace_only_negative_control():
    # A fixed-support probability model, NOT a counterexample to A2.
    # h=+1 on r<1/4, -1 on 1/4<=r<1/2, 0 near ceiling r=1.
    # 1+eps*h has unchanged trace and integral one, but product laws
    # separate when eps=k^(-1/4). A2 explicitly excludes this bulk size.
    rows = []
    previous = -1.0
    for k in [16,256,4096,65536]:
        eps = k**(-0.25)
        affinity = 0.5+0.25*(math.sqrt(1+eps)+math.sqrt(1-eps))
        h2_product = -2*math.expm1(k*math.log(affinity))
        require(h2_product > previous, 'negative control should separate')
        previous = h2_product
        rows.append({'k':k,'eps':eps,'product_H2':h2_product})
    require(rows[-1]['product_H2'] > 1.99, 'negative control not separated')
    return {'role':'necessity check; not a counterexample to the manuscript',
            'rows':rows,'passed':True}


def rerooting():
    """Exhaustive finite combinatorial control; not analytic-signature proof."""
    def edges_from_prufer(n, seq):
        if n == 1:
            return []
        degree = [1]*n
        for v in seq:
            degree[v] += 1
        edges = []
        for v in seq:
            leaf = next(i for i in range(n) if degree[i] == 1)
            edges.append((leaf, v))
            degree[leaf] -= 1
            degree[v] -= 1
        remaining = [i for i in range(n) if degree[i] == 1]
        edges.append(tuple(remaining))
        return edges

    def parents(n, edges, root):
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        seen, stack, answer = {root}, [root], set()
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
                    answer.add(u)
        require(len(seen) == n, 'tree control disconnected')
        return answer

    tree_count = valid_original = reroot_checks = 0
    for n in range(1, 6):
        for seq in product(range(n), repeat=max(0, n-2)):
            edges = edges_from_prufer(n, seq)
            tree_count += 1
            parent_sets = [parents(n, edges, r) for r in range(n)]
            for root in range(n):
                for mask in range(1 << n):
                    rigid = {v for v in range(n) if mask & (1 << v)}
                    if not parent_sets[root] <= rigid:
                        continue
                    valid_original += 1
                    for new_root in rigid:
                        require(parent_sets[new_root] <= rigid,
                                'signature-rigid tree reroot control failed')
                        reroot_checks += 1
    # Dropping rigidity of the new root is not justified: symmetric leaves
    # may remain leaves, but cannot become a nontrivial parent.
    e, rigid = [(0, 1), (0, 2)], {0}
    require(parents(3, e, 0) <= rigid, 'negative-control premise failed')
    require(not parents(3, e, 1) <= rigid, 'negative control not detected')
    return {'labelled_trees_n_le_5':tree_count,
            'valid_original_root_and_rigidity_assignments':valid_original,
            'reroot_checks':reroot_checks,
            'new_root_rigidity_negative_control':True,'passed':True}


def main():
    result = {'reviewed_commit':'070aa946fb28001916ad1bbd3503afa5f6cae3b3',
              'inherited_formula_source_commit':'dd0e5aefd49d200652afc3fc3f29f7a6f38ae326',
              'scope':'independent finite algebra and explicit probability-model controls; no imported manuscript, no native build',
              'python':platform.python_version(),
              'rerooting':rerooting(), 'algebra':algebra(), 'geometric_hellinger':geometric_hellinger(),
              'layer_corner':layer_corner(), 'trace_only_negative_control':trace_only_negative_control()}
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))


if __name__ == '__main__':
    main()
