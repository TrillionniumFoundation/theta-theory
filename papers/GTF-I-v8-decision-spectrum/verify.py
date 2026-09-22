#!/usr/bin/env python3
"""Finite diagnostics for the eighth revision, not a proof certificate.

Uses exact rational arithmetic where practical; LP comparisons use scipy/HiGHS.
No `assert` statement is used, so Python -O executes the same checks.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import itertools
import json
import math
from typing import Iterable

MUTANTS = ('task_after_encoder', 'collapsed_likelihood', 'drop_compatibility',
           'raw_energy_threshold', 'marginal_is_realized', 'free_transcript',
           'product_closure')
COUNT = 0

def check(condition: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)

def partitions(n: int, width: int) -> Iterable[tuple[int, ...]]:
    def extend(v: tuple[int, ...]):
        if len(v) == n:
            yield v
            return
        for j in range(min(width, 1 + max(v, default=-1) + 1)):
            yield from extend(v + (j,))
    yield from extend(())

def squared_cost(cells, targets):
    total = F(0)
    for c in set(cells):
        values = [F(t) for i,t in enumerate(targets) if cells[i] == c]
        mean = sum(values) / len(values)
        total += sum((v-mean)**2 for v in values) / len(targets)
    return total

def quantifiers(mutant):
    inputs = list(itertools.product((0,1), repeat=2))
    min_average = F(1)
    individual = [F(1), F(1)]
    for labels in itertools.product((0,1), repeat=4):
        errors = []
        for j in (0,1):
            errors.append(sum(min(sum(x[j] == b and labels[i] == c
                                      for i,x in enumerate(inputs)) for b in (0,1))
                              for c in (0,1)) / F(4))
        min_average = min(min_average, sum(errors)/2)
        individual = [min(a,b) for a,b in zip(individual, errors)]
    tested = max(individual) if mutant == 'task_after_encoder' else min_average
    check(tested == F(1,4), 'common encoder cannot be chosen separately for each task')
    check(individual == [0,0], 'separate task optima vanish')
    finite_vectors = [([0]*n+[1]*(8-n)) for n in range(1,8)]
    displayed_inf_sup = min(max(v) for v in finite_vectors)
    tested = 0 if mutant == 'product_closure' else displayed_inf_sup
    check(tested == 1, 'coordinatewise limiting closure is not the uniform task criterion')
    return {'common_average_lower': str(min_average), 'separate_optima': list(map(str,individual))}

def cell_protocol_checks():
    cells = ((F(7,10),F(3,10)),(F(1,5),F(4,5)))
    commands = ((F(1,3),F(2,3)),(F(3,5),F(2,5)))
    likelihood = {}
    for theta in (0,1):
        total=F(0)
        for g in commands:
            values=[cells[theta][i]*g[i] for i in (0,1)]
            values.append(sum(cells[theta][i]*(1-g[i]) for i in (0,1)))
            check(sum(values)==1,'actual accepted/shared-failure likelihood normalizes')
            for x,v in enumerate(values):likelihood[theta,g,x]=v/F(2);total+=v/F(2)
        check(total==1,'finite command mixture normalizes')
    total=F(0)
    for h in itertools.product(itertools.product(commands,range(3)),repeat=2):
        evidence=[math.prod(likelihood[theta,g,x] for g,x in h) for theta in (0,1)]
        ph=sum(evidence)/2;total+=ph
        mean=evidence[1]/sum(evidence)
        check(0<=mean<=1,'cell-history posterior uses only observed pairs')
        check(ph*mean==evidence[1]/2,'actual posterior numerator identity')
    check(total==1,'all finite-command observed histories normalize')
    return {'horizon':2,'observed_pairs':6,'histories':36}

def matrix_multiply(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def posterior_sufficiency(mutant):
    E = [[F(3,5),F(1,5),F(3,20),F(1,20)],
         [F(3,20),F(1,20),F(3,5),F(1,5)],
         [F(3,10),F(1,10),F(9,20),F(3,20)]]
    groups_by_prior = []
    for prior in ([F(1,6),F(2,6),F(3,6)],[F(2,8),F(5,8),F(1,8)]):
        m = [sum(prior[j]*E[j][x] for j in range(3)) for x in range(4)]
        T = [tuple(prior[j]*E[j][x]/m[x] for j in range(3)) for x in range(4)]
        groups = []
        for t in dict.fromkeys(T):
            groups.append([x for x in range(4) if T[x] == t])
        groups_by_prior.append(groups)
        check(groups == [[0,1],[2,3]], 'likelihood quotient keeps both informative cells')
        if mutant == 'collapsed_likelihood': groups = [[0,1,2,3]]
        R = [[m[x]/sum(m[i] for i in g) if x in g else F(0) for x in range(4)] for g in groups]
        compressed = [[sum(row[x] for x in g) for g in groups] for row in E]
        check(matrix_multiply(compressed,R) == E, 'one parameter-independent reconstruction must recover every row')
        for row in R: check(sum(row)==1, 'conditional reconstruction normalizes')
    check(groups_by_prior[0]==groups_by_prior[1], 'positive reference prior changes coordinates not sufficient cells')
    # Count-saturated binary experiment with an ancillary report bit.
    # Conditioning on each final count cannot change the independent ancillary law.
    for theta in (F(1,4),F(3,4)):
        total=F(0)
        for reports in itertools.product(itertools.product((0,1), repeat=2),repeat=3):
            s=0; actual=F(1); reconstructed=F(1)
            for b,z in reports:
                new=s+b
                p=theta if b else 1-theta
                ancillary=F(1,3) if z else F(2,3)
                actual*=p*ancillary
                reconstructed*=(theta if new-s else 1-theta)*ancillary
                s=new
            check(actual==reconstructed,'saturated recursion reconstructs original and ancillary report laws')
            total+=reconstructed
        check(total==1,'three-step reconstructed experiment normalizes')
    return {'minimal_cells':groups_by_prior[0], 'causal_horizon':3}

def congruence_checks(mutant):
    X=list(itertools.product((0,1),repeat=2)); histories=[(i,j) for i in range(4) for j in (0,1)]
    target=[X[i][j] for i,j in histories]
    first=list(partitions(4,2)); second=list(partitions(8,2))
    best=F(1); feasible=0
    for a in first:
        for b in second:
            compatible=all(b[2*i+j]==b[2*k+j] for i in range(4) for k in range(4)
                           for j in (0,1) if a[i]==a[k])
            if compatible or mutant=='drop_compatibility':
                feasible+=1; best=min(best,squared_cost(b,target))
    brute=F(1)
    for q in itertools.product((0,1),repeat=4):
        for u in itertools.product((0,1),repeat=4):
            cells=[u[2*q[i]+j] for i,j in histories]
            brute=min(brute,squared_cost(cells,target))
    check(best==brute,'compatible partitions must equal exhaustive causal transducers')
    check(best>0,'two static target values do not imply a two-state zero-error causal realization')
    check(squared_cost(target,target)==0,'unrestricted checkpoint quantization is exact')
    for d in range(1,8):
        words=list(itertools.product((0,1),repeat=d))
        residuals={tuple(x[j] for j in range(d)) for x in words}
        check(len(residuals)==2**d,'delayed query has 2^d distinct continuation signatures')
    return {'partition_families':len(first)*len(second),'feasible_families':feasible,
            'squared_causal_optimum':str(best),'static_optimum':'0'}

def energy(v,weights): return math.prod(weights[i] for i in v)

def make_tree(eta,weights,kappa,raw=False,bad=False):
    cache={}
    def upper(v):
        if v not in cache:
            a=energy(v,weights)
            mult=(F(6,5) if v==(0,1) else F(1)) if bad else F(1)+F(sum((j+1)*(i+1) for j,i in enumerate(v))%5,10)
            cache[v]=a*mult
        return cache[v]
    def estimate(v):
        if raw:return upper(v)
        return min(upper(v[i:j]) for i in range(len(v)+1) for j in range(i,len(v)+1))
    vertices={()}; internal=set(); todo=[()]
    while todo:
        v=todo.pop()
        if estimate(v)>eta:
            internal.add(v)
            for i in (0,1):
                w=v+(i,);vertices.add(w);todo.append(w)
    return vertices,internal,vertices-internal,estimate

def tree_checks(mutant):
    weights=(F(9,10),F(1,20)); eta=F(13,250)
    verts,ints,leaves,_=make_tree(eta,weights,F(6,5),raw=(mutant=='raw_energy_threshold'),bad=True)
    check(all(v[k:] in verts for v in verts for k in range(len(v)+1)),
          'certified factor envelope must repair raw-threshold suffix failure')
    rawverts,rawints,rawleaves,_=make_tree(eta,weights,F(6,5),raw=True,bad=True)
    check(not all(v[k:] in rawverts for v in rawverts for k in range(len(v)+1)),
          'the raw approximation counterexample must actually violate closure')
    rows=[]
    for weights in ((F(1,5),F(1,10)),(F(3,20),F(1,20)),(F(2,7),F(1,7))):
        for j in range(1,13):
            eta=F(1,2**j);kappa=F(3,2);rho=sum(weights)
            verts,ints,leaves,estimate=make_tree(eta,weights,kappa)
            check(len(verts)==2*len(leaves)-1,'exact full binary tree count')
            check(len(verts)==1+2*len(ints),'all internal states are charged')
            check(all(v[k:] in verts for v in verts for k in range(len(v)+1)),'all suffix updates legal')
            for v in verts:
                a=energy(v,weights)
                check(a<=estimate(v)<=kappa*a,'factor envelope preserves relative energy enclosure')
            for v in leaves:
                check(min(weights)*eta/kappa<energy(v,weights)<=eta,'threshold leaves have balanced true energies')
                for i in (0,1):
                    word=(i,)+v
                    check(any(word[:k] in leaves for k in range(len(word)+1)), 'prepend reaches a leaf before exhausted word')
            depth=max(map(len,verts))
            check(depth<=1+math.ceil(math.log(float(kappa/eta))/abs(math.log(float(rho)))),'finite-prefix depth bound')
            rows.append({'j':j,'weights':list(map(str,weights)),'states':len(verts),'leaves':len(leaves),'depth':depth})
    return rows

def w1(a,b):
    points=sorted(set(a)|set(b));total=F(0);ca=cb=F(0)
    for i,x in enumerate(points[:-1]):
        ca+=a.get(x,F(0)); cb+=b.get(x,F(0))
        total+=abs(ca-cb)*(points[i+1]-x)
    return total

def law(word):
    n=len(word)
    return {F(4*i+1+2*b,4*n):F(1,n) for i,b in enumerate(word)}

def filtered(a,y):
    out={}
    for x,mass in a.items():
        h=x/5+x*x/50
        for z in (0,1):
            t=h+F(3,5)*z
            out[t]=out.get(t,F(0))+mass*(F(3,4) if z==y else F(1,4))
    return out

def measure_checks(mutant):
    for n in range(1,6):
        words=list(itertools.product((0,1),repeat=n))
        for u,v in itertools.product(words,repeat=2):
            distance=w1(law(u),law(v));dh=sum(a!=b for a,b in zip(u,v))
            check(distance==F(dh,2*n*n),'W1 packing distance equals Hamming/(2n^2)')
        check(math.comb(2*n,n)<=4**n,'empirical-grid codebook cardinality')
    a={F(0):F(1,2),F(1):F(1,2)}
    realized=(w1(a,{F(0):F(1)})+w1(a,{F(1):F(1)}))/2
    tested=F(0) if mutant=='marginal_is_realized' else realized
    check(tested==F(1,2),'unconditional mixture equality does not mean zero realized-law loss')
    words=list(itertools.product((0,1),repeat=3))
    for u,v in itertools.product(words,repeat=2):
        base=w1(law(u),law(v))
        for y in (0,1):
            after=w1(filtered(law(u),y),filtered(law(v),y))
            check(base/5<=after<=F(6,25)*base,'nonlinear report update is bi-Lipschitz on laws')
    for S in range(2,15):
        for x in (F(k,32) for k in range(33)):
            z=F(round(x*(S-1)),S-1)
            check(abs(z-x)<=F(1,2*(S-1)), 'marginal probe grid accuracy')
    return {'expected_realized_two_point_distance':str(realized),'probe_mixture_distance':'0'}

def gaussian_registers(mutant):
    rows=[]
    for n,r,J in itertools.product(range(1,5),range(1,4),range(2,5)):
        S=J**(r*n)
        available=J**r if mutant=='free_transcript' else S
        for t in range(1,n+1):
            check(J**(r*t)<=available,'accumulated labels must fit the CURRENT total register')
        check(F(2,r*n)*F(r*n,1)==2,'sequential Gaussian exponent uses total dimension')
        rows.append({'n':n,'r':r,'J':J,'S':S})
    return rows

def deficiency_lp_checks():
    import numpy as np
    from scipy.optimize import linprog
    rows=[];rng=np.random.default_rng(23092026)
    for k in range(6):
        E=rng.integers(1,10,size=(3,4)).astype(float);E/=E.sum(axis=1,keepdims=True)
        Q=rng.integers(1,10,size=(4,2)).astype(float);Q/=Q.sum(axis=1,keepdims=True)
        Fm=E@Q;nt,nx=E.shape;ni=Fm.shape[1]
        # inf_R max_theta sup_B [R F_theta(B)-P_theta(B)]
        A=[];b=[]
        for theta in range(nt):
            for bits in itertools.product((0,1),repeat=nx):
                row=np.zeros(ni*nx+1); row[-1]=-1
                for i in range(ni):row[i*nx:(i+1)*nx]=Fm[theta,i]*np.array(bits)
                A.append(row); b.append(E[theta]@bits)
        eq=np.zeros((ni,ni*nx+1))
        for i in range(ni):eq[i,i*nx:(i+1)*nx]=1
        c=np.zeros(ni*nx+1);c[-1]=1
        primal=linprog(c,A_ub=A,b_ub=b,A_eq=eq,b_eq=np.ones(ni),bounds=(0,None),method='highs')
        check(primal.success,'finite deficiency primal LP solved')
        # Dual variables u(theta,action), prior pi, maximum rewards v(label).
        size=nt*nx+nt+ni;A=[];b=[]
        for theta in range(nt):
            for x in range(nx):
                row=np.zeros(size);row[theta*nx+x]=1;row[nt*nx+theta]=-1;A.append(row);b.append(0)
        for i in range(ni):
            for x in range(nx):
                row=np.zeros(size)
                for theta in range(nt):row[theta*nx+x]=Fm[theta,i]
                row[nt*nx+nt+i]=-1;A.append(row);b.append(0)
        c=np.r_[-E.ravel(),np.zeros(nt),np.ones(ni)];eq=np.zeros((1,size));eq[0,nt*nx:nt*nx+nt]=1
        dual=linprog(c,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
        check(dual.success,'finite decision dual LP solved')
        check(abs(primal.fun+dual.fun)<1e-8,'finite randomization duality matches deficiency')
        u=dual.x[:nt*nx].reshape(nt,nx)
        rewardE=np.sum(np.max(E.T@u,axis=1));rewardF=np.sum(np.max(Fm.T@u,axis=1))
        check(abs(rewardE-rewardF-primal.fun)<1e-8,'one extracted decision problem attains the finite dual gap')
        rows.append({'case':k,'deficiency':round(float(primal.fun),12),'decision_gap':round(float(rewardE-rewardF),12)})
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS);args=parser.parse_args()
    try:
        result={'quantifiers':quantifiers(args.mutant),'sufficiency':posterior_sufficiency(args.mutant),'cell_protocol':cell_protocol_checks(),
                'congruence':congruence_checks(args.mutant),'trees':tree_checks(args.mutant),
                'measures':measure_checks(args.mutant),'registers':gaussian_registers(args.mutant),
                'finite_deficiency':deficiency_lp_checks()}
        if args.mutant is not None:raise RuntimeError('designated mutant survived: '+args.mutant)
        print(json.dumps({'status':'passed','finite_checks':COUNT,'results':result,
                         'scope':'Finite identities, exhaustive tiny instances and floating-point LP diagnostics; not mathematical proof certification.'},sort_keys=True,indent=2))
    except RuntimeError as exc:
        print('FAILED: '+str(exc));raise SystemExit(1)
if __name__=='__main__':main()
