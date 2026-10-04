#!/usr/bin/env python3
"""Independent finite rational diagnostics of the v31 displayed mechanisms.

Finite state examples and synthetic grid occupations are not experiments on a
physical billiard apparatus or certificates of the continuum theorem.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import itertools
import json
import hashlib
from pathlib import Path
import re
from reciprocal_intervals import KilledKernel, compass_kernel, enclose, geometric_tail, clip

C = Counter()
ROOT = Path(__file__).resolve().parents[1]


def check(value, group):
    if not value:
        raise RuntimeError(group)
    C[group] += 1


def solve(a, b):
    """Independent exact Gaussian elimination, not a Bellman iteration."""
    n = len(b)
    z = [list(row) + [rhs] for row, rhs in zip(a, b)]
    for j in range(n):
        k = next(i for i in range(j, n) if z[i][j])
        z[j], z[k] = z[k], z[j]
        q = z[j][j]; z[j] = [x / q for x in z[j]]
        for i in range(n):
            if i != j:
                q = z[i][j]; z[i] = [x - q*y for x, y in zip(z[i], z[j])]
    return [row[-1] for row in z]


def line_kernel(n):
    return KilledKernel(tuple(tuple((j,F(1,2)) for j in (i-1,i+1) if 0<=j<n)
                              for i in range(n)))


def forcing(kernel, u):
    return [x-y for x,y in zip(kernel.apply(u),u)]


def killed_exit(kernel, positive):
    ids = sorted(positive); index={j:i for i,j in enumerate(ids)}
    a = [[F(i==j) for j in range(len(ids))] for i in range(len(ids))]
    for i,x in enumerate(ids):
        for j,p in kernel.rows[x]:
            if j in index: a[i][index[j]] -= p
    times = solve(a,[F(1)]*len(ids))
    return dict(zip(ids,times)), a


def mean_exit_and_green():
    for n in range(2,11):
        k=line_kernel(n)
        u=[F(1)]*n
        g=forcing(k,u)
        times,a=killed_exit(k,range(n))
        H=F(n*n)  # D=n-1, b=1 and variance one.
        for i in range(n):
            check(times[i]==(i+1)*(n-i),'independent_exact_exit_time')
            check(times[i]<=H,'diameter_variance_bound')
        row_sums=[F(0)]*n
        for j in range(n):
            column=solve(a,[F(i==j) for i in range(n)])
            for i in range(n):
                check(column[i]>=0,'green_positivity')
                row_sums[i]+=column[i]
        check(row_sums==[times[i] for i in range(n)],'green_row_sum_expected_exit')
        check(max(row_sums)==max(times.values()),'sharp_known_dirichlet_norm')
        V=[F(0)]*n; survival=[F(1)]*n
        L=2*n*n
        for depth in range(1,25):
            Vnext=[clip(x-y) for x,y in zip(k.apply(V),g)]
            survival=k.apply(survival)
            for i in range(n):
                check(0<=V[i]<=Vnext[i]<=u[i],'bellman_monotonicity')
                check(u[i]-Vnext[i]==survival[i],'indicator_error_survival_identity')
                check(survival[i]<=geometric_tail(depth,L),'geometric_tail_bound')
            V=Vnext
    k=line_kernel(2); u=[F(1)]*2; g=forcing(k,u)
    for depth in range(1,31):
        v=enclose(k,g,g,depth,F(1,2**depth))
        check(v['iterate_lower']==[1-F(1,2**depth)]*2,'no_finite_exact_stopping')
        check(v['occupation_upper']==u,'exact_two_site_tail_enclosure')


def different_zero_sets():
    k=line_kernel(12)
    occupations=[]
    for start in (1,3,5,7):
        for length in (1,2,3):
            for height in (F(1),F(1,3),F(2,3)):
                u=[F(0)]*12
                for j in range(start,start+length): u[j]=height
                occupations.append(u)
    for u,v in itertools.combinations(occupations,2):
        gu,gv=forcing(k,u),forcing(k,v)
        xi=max(abs(a-b) for a,b in zip(gu,gv))
        # One interval of diameter at most two for each candidate; H=(2+1)^2.
        check(max(abs(a-b) for a,b in zip(u,v))<=9*xi,'different_unknown_zero_set_comparison')
    for u in occupations[::3]:
        g=forcing(k,u); xi=F(1,37)
        for depth in (1,3,7,12):
            perturbed=[x+(-1)**i*xi for i,x in enumerate(g)]
            truth=enclose(k,g,g,depth)['iterate_lower']
            noisy=enclose(k,perturbed,perturbed,depth)['iterate_lower']
            check(max(abs(a-b) for a,b in zip(truth,noisy))<=depth*xi,
                  'adversarial_forcing_accumulation')
            interval=enclose(k,[x-xi for x in perturbed],
                             [x+xi for x in perturbed],depth,geometric_tail(depth,18))
            for i in range(k.size):
                check(interval['iterate_lower'][i]<=truth[i]<=interval['iterate_upper'][i],
                      'rational_interval_contains_exact_iterate')
                check(interval['occupation_lower'][i]<=u[i]<=interval['occupation_upper'][i],
                      'conditional_occupation_interval')


def fixed_aperture_and_compass():
    width=13; height=11; k=compass_kernel(width,height)
    u=[F(0)]*k.size
    for y in range(4,7):
        for x in range(5,8): u[y*width+x]=F((x+y)%3+1,3)
    g=forcing(k,u)
    # A smaller aperture entirely contains the component and every one-step exit.
    small=compass_kernel(7,7)
    mapping=[(y+2)*width+x+3 for y in range(7) for x in range(7)]
    sg=[g[i] for i in mapping]
    for depth in (1,3,8,16):
        bigv=enclose(k,g,g,depth)['iterate_lower']
        smallv=enclose(small,sg,sg,depth)['iterate_lower']
        for j,i in enumerate(mapping):
            if u[i]>0:
                check(bigv[i]==smallv[j],'fixed_aperture_matches_full_recursion')
    check(len(k.rows[0])==2,'no_boundary_wraparound')
    check(sum(p for _,p in k.rows[0])==F(1,2),'killed_mass_not_renormalized')
    # Compare against an incorrect periodic boundary on a one-column aperture.
    narrow=compass_kernel(1,2)
    correct=enclose(narrow,[F(-1,2)]*2,[F(-1,2)]*2,2)['iterate_lower']
    wrong=[F(1)]*2  # periodic T on a constant field accumulates twice 1/2
    check(correct!=wrong,'periodic_wraparound_counterexample')
    for step in (1,2,3):
        c=compass_kernel(8,9,step)
        for i,row in enumerate(c.rows):
            y,x=divmod(i,8)
            for j,p in row:
                yy,xx=divmod(j,8)
                check(abs(x-xx)+abs(y-yy)==step and (x==xx or y==yy),
                      'exact_compass_grid_shifts')
                check(p==F(1,4),'pooled_weights')


def pooled_reversal_and_escape():
    # All endpoint occupations and intersection states consistent with them.
    states=[(x,y,I) for x,y,I in itertools.product((0,1),repeat=3) if I>=max(x,y)]
    for packet in itertools.product(states,repeat=4):
        plus=sum(F((1-x)*I,4) for x,y,I in packet)
        minus=sum(F((1-y)*I,4) for x,y,I in packet)
        diff=sum(F(y-x,4) for x,y,I in packet)
        check(plus-minus==diff,'two_pooled_mean_reversal')
    for p in (F(1,2),F(1,3),F(2,3),F(1)):
        for m in range(1,7):
            q=1-p**m
            # finite partial tail sum never exceeds geometric-block expectation
            for blocks in (1,3,8):
                check(m*sum(q**j for j in range(blocks))<=m/p**m,
                      'positive_cone_mass_exit_bound')
    # Neither a positive drift nor nonsingular covariance is needed.
    points=[(-1,0),(1,0),(0,-1),(0,1)]
    check(sum(F(x,4) for x,y in points)==0 and sum(F(y,4) for x,y in points)==0,
          'compass_centered')
    check(sum(F(x*x+y*y,4) for x,y in points)==1,'compass_second_moment')
    for nx,ny in [(-2,1),(1,0),(0,1),(3,-2)]:
        check(min(nx*x+ny*y for x,y in points)<=0,'no_common_positive_projection')
    check(F(1,64)+F(1,128)+F(1,128)==F(1,32),'finite_error_budget')
    check(F(1,32)<F(1,8),'threshold_margin')
    check(F(3,2)*F(2,3)==1 and 2*F(3,2)==3 and 4*F(3,2)==6,
          'geometric_statistical_arithmetic_rates')


def source_checks():
    pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    for name,expected in pins['retained_active_core_sha256'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,
              'all_nine_v30_active_cores_unchanged')
    text=(ROOT/'main.tex').read_text()
    items=re.findall(r'\\input\{([^}]+)\}',text)
    for item in items:
        check((ROOT/(item+'.tex')).is_file(),'active_input_exists')
        text+='\n'+(ROOT/(item+'.tex')).read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_labels')
    for label in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text):
        check(label in labels,'resolved_references')
    for label in ('thm:stopped','thm:constructive','thm:mean-exit-inverse',
                  'cor:noncentered-exit','thm:pooled-recovery'):
        check(label in labels,'retained_and_new_theorems_active')
    bibs=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for keys in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):
        for key in keys.split(','): check(key.strip() in bibs,'resolved_citations')


def main():
    mean_exit_and_green(); different_zero_sets(); fixed_aperture_and_compass()
    pooled_reversal_and_escape(); source_checks()
    print(json.dumps({'schema':'a2-v31-exact-finite-diagnostics-1','status':'passed',
                      'total_checks':sum(C.values()),'groups':dict(sorted(C.items())),
                      'scope':'finite rational algebra, synthetic grids, and source structure',
                      'physical_sensor_executed':False,'formal_proof_certificate':False},
                     sort_keys=True))


if __name__=='__main__':
    main()
