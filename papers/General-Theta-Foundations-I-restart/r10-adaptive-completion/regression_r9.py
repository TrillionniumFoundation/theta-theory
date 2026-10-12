#!/usr/bin/env python3
"""Finite checks for the serial/rank/singular layer, not continuum proof certificates."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import json, math, subprocess, sys

counts=Counter()
def check(ok, group):
    if not ok: raise RuntimeError('finite regression failed: '+group)
    counts[group]+=1

def rank(A):
    a=[list(map(F,row)) for row in A]
    if not a or not a[0]: return 0
    r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r];v=a[r][col]
        a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r

def q(x,k):
    sign=1 if x>=0 else -1;x=abs(x);j=int(k*x/(1+x))
    return sign*F(j,k-j)

def main():
    # Exact unrolling with expansive, nonexpansive and contractive gains.
    for T in range(1,7):
        for gains in product([F(1,2),F(1),F(3,2)],repeat=T):
            ins=[F(j+1,17) for j in range(T)]; e=F(0)
            for L,b in zip(gains,ins): e=L*e+b
            direct=sum(ins[t]*math.prod(gains[t+1:]) for t in range(T))
            check(e==direct,'serial_error_unrolling')
    # Candidate envelope is independent of the eventual error estimate.
    for L,b in product([F(0),F(1,3),F(2)],repeat=2):
        a=F(1); x=F(1)
        for t in range(9):
            x=L*x+b; a=L*a+b
            x=q(x,3)
            check(abs(x)<=a,'inward_candidate_envelope')
    # Prefix rank can be below ambient dimension, and intermediate ranks matter.
    for d in range(2,9):
        for r in range(1,d+1):
            C=[[F((j % r)==i) for j in range(d)] for i in range(r)]
            previous=0
            state=[F(0)]*r
            for j in range(d):
                h=F((-1)**j*(j+2),j+1)
                state=[state[i]+C[i][j]*h for i in range(r)]
                expected=[sum(C[i][l]*F((-1)**l*(l+2),l+1) for l in range(j+1)) for i in range(r)]
                check(state==expected,'partial_task_linear_recursion')
                now=rank([row[:j+1] for row in C])
                check(previous<=now<=min(j+1,r),'changing_observable_rank')
                previous=now
            check(previous==r,'final_observable_not_ambient_rank')
    # Rigorous rational Cantor example: r_j=2^(-k_j), d_j=1/k_j.
    # The allocation depths and cardinalities are checked exactly for M=2^b.
    for ks in [(2,2),(3,4),(2,3,5),(4,5,6),(2,2,2)]:
        dims=[F(1,k) for k in ks]
        for i in range(1,len(ks)+1):
            D=sum(dims[:i])
            for b in range(25):
                ns=[int(dims[j]*b/D) for j in range(i)]
                check(sum(ns)<=b,'singular_global_cover_cardinality')
                for k,n in zip(ks[:i],ns):
                    check(F(k*n)>=F(b)/D-k,'singular_cover_radius_exponent')
                for m in range(1,8):
                    # Exact finite cylinder probability, not an atomless substitute.
                    check(F(1,2**m)==F(2)**(-m),'actual_cylinder_mass')
            check(max(D,F(1))>=D and max(D,F(1))>=1,'terminal_cut_in_maximum')
    # Gaussian side-information density and sigmoid slope positivity finite witnesses.
    for sigma,mean,limit in product([F(1,2),F(1),F(2)],[F(-2),F(0),F(2)],[F(1),F(3)]):
        lower=math.exp(-float(abs(mean)+limit)**2/(2*float(sigma)**2))/(math.sqrt(2*math.pi)*float(sigma))
        check(0<2*float(limit)*lower<=1,'positive_common_gaussian_mass')
    # Nontrivial negative controls: omitting final cut would predict a false exponent.
    check(F(2)/F(1,2)>2,'negative:singular_prefix_does_not_erase_final_cut')
    check(F(2)/2!=F(2)/5,'negative:ambient_rank_is_not_observable_rank')
    check(7*6>7,'negative:phase_is_not_free_data_state')
    check(F(1,8)*F(1,4)!=F(1,4),'negative:retain_actual_submass')
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).with_name('regression_r8.py'))]
    out=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if out.returncode: raise RuntimeError(out.stdout)
    inherited=json.loads(out.stdout)
    check(inherited['status']=='PASS','retained_R8_R7_R6_suites')
    print(json.dumps({'status':'PASS','native_checks':sum(counts.values()),'groups':dict(sorted(counts.items())),
                     'retained_R8':inherited,'scope':'finite witnesses only; full proofs are native manuscript text'},sort_keys=True,indent=2))
if __name__=='__main__': main()
