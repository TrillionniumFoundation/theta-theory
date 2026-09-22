#!/usr/bin/env python3
"""Finite diagnostic examples, NOT an asymptotic or formal proof certificate."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import itertools as it
import json
import math
from typing import Callable
import numpy as np
from scipy.optimize import linprog
from scipy.integrate import quad

COUNT=0
MUTANTS=('task_after_encoder','convexify_private','free_seed_index',
         'drop_prediction','drop_likelihood','omit_action','mix_logarithms')

def check(condition: bool, message: str) -> None:
    global COUNT
    COUNT+=1
    if not bool(condition): raise RuntimeError(message)

def game(rows: list[list[float]]) -> tuple[float,float]:
    r=np.array(rows,dtype=float);n,m=r.shape
    primal=linprog(np.r_[np.zeros(n),1.],A_ub=np.c_[r.T,-np.ones(m)],
        b_ub=np.zeros(m),A_eq=np.array([np.r_[np.ones(n),0.]]),b_eq=[1.],
        bounds=[(0,None)]*n+[(None,None)],method='highs')
    dual=linprog(np.r_[np.zeros(m),-1.],A_ub=np.c_[-r,np.ones(n)],
        b_ub=np.zeros(n),A_eq=np.array([np.r_[np.ones(m),0.]]),b_eq=[1.],
        bounds=[(0,None)]*m+[(None,None)],method='highs')
    check(primal.success and dual.success,'finite primal/dual failed')
    check(abs(primal.fun+dual.fun)<1e-9,'minimax primal/dual disagree')
    return float(primal.fun),float(-dual.fun)

def common_tasks(mutant: str|None) -> dict:
    words=list(it.product((0,1),repeat=2));rows=[];partition_rows=[]
    for f in it.product((0,1),repeat=4):
        bayes=[]
        for d in range(2):
            bayes.append(min(sum(F(b[f[k]]!=x[d],4) for k,x in enumerate(words))
                             for b in it.product((0,1),repeat=2)))
        partition_rows.append(bayes)
        for bs in it.product(list(it.product((0,1),repeat=2)),repeat=2):
            rows.append([float(sum(F(bs[d][f[k]]!=x[d],4)
                                  for k,x in enumerate(words))) for d in range(2)])
    value,dual=game(rows)
    tested=max(min(v[d] for v in partition_rows) for d in range(2)) if mutant=='task_after_encoder' else value
    check(abs(float(tested)-.25)<1e-10,'common encoder cannot follow the task')
    pv,_=game([[float(x) for x in r] for r in partition_rows])
    check(abs(pv-value)<1e-10,'partition Bayes envelopes disagree with full designs')
    for k in range(21):
        w=F(k,20)
        envelope=min(w*v[0]+(1-w)*v[1] for v in partition_rows)
        direct=min(float(w)*v[0]+float(1-w)*v[1] for v in rows)
        check(abs(float(envelope)-direct)<1e-10,'weighted partition support mismatch')
    return {'designs':len(rows),'common_bayes_error':value,'dual':dual}

def seed_gap(mutant: str|None) -> dict:
    rows=[]
    for f in it.product(range(2),repeat=3):
        for b in it.product(range(3),repeat=2):
            rows.append([float(b[f[x]]!=x) for x in range(3)])
    public,_=game(rows)
    check(abs(public-1/3)<1e-10,'three-symbol shared minimax value')
    # A finite decoder grid checks the witness, not the analytical global lower bound.
    simplex=[(F(a,8),F(b,8),F(8-a-b,8)) for a in range(9) for b in range(9-a)]
    private_grid=1-max(min(max(r[x],s[x]) for x in range(3)) for r in simplex for s in simplex)
    tested=public if mutant=='convexify_private' else private_grid
    check(abs(float(tested)-.5)<1e-10,'shared convexification is not private randomization')
    k,S=3,2
    stored=S if mutant=='free_seed_index' else len(list(it.product(range(k),range(S))))
    check(stored==6,'a privately retained design index must be charged')
    for p in range(1,13):
        lam=[F(1,3)]*3
        rounded=[F(int(lam[i]*2**p),2**p) for i in range(2)]
        rounded.append(1-sum(rounded))
        tv=sum(abs(a-b) for a,b in zip(lam,rounded))/2
        check(tv<=F(k,2**p),'dyadic mixture total-variation bound')
        check(sum(rounded)==1 and min(rounded)>=0,'dyadic mixture probability')
    return {'shared':public,'private_grid_witness':str(private_grid),
            'private_global_bound':'analytical pigeonhole proof in ex:v9-privategap',
            'private_implementation_states':stored}

def controlled_occupancy() -> dict:
    # Two hidden parameters, two task-specific controllers, one common update.
    # Initial hidden state equals theta; control changes the NEW state.
    designs=[];supports=[]
    for f in it.product((0,1),repeat=4):
        for actions in it.product((0,1),repeat=2):
            for decs in it.product(list(it.product((0,1),repeat=2)),repeat=2):
                risk=[]
                for d,theta in it.product(range(2),repeat=2):
                    a=actions[d];new=theta^a;p=F(3,4) if a==0 else F(4,5)
                    risk.append(sum((p if y==new else 1-p)*int(decs[d][f[2*a+y]]!=(new^d)) for y in range(2)))
                designs.append(risk)
    for ints in [(1,1,1,1),(1,2,3,4),(4,1,2,1),(0,1,2,0),(5,0,0,1)]:
        w=[F(v,sum(ints)) for v in ints]
        direct=min(sum(a*b for a,b in zip(w,r)) for r in designs)
        best=None
        for f in it.product((0,1),repeat=4):
            for acts in it.product((0,1),repeat=2):
                # Occupancy indexed by task,theta,new hidden state,label.
                z={}
                for d,theta in it.product(range(2),repeat=2):
                    a=acts[d];new=theta^a;p=F(3,4) if a==0 else F(4,5)
                    for y in range(2):
                        key=(d,theta,new,f[2*a+y]);z[key]=z.get(key,F(0))+w[2*d+theta]*(p if y==new else 1-p)
                terminal=F(0)
                for d,i in it.product(range(2),repeat=2):
                    terminal+=min(sum(m*int(b!=(new^d)) for (dd,th,new,ii),m in z.items() if dd==d and ii==i) for b in range(2))
                best=terminal if best is None else min(best,terminal)
        check(direct==best,'controlled occupancy differs from direct closed-loop enumeration')
        supports.append(str(best))
    return {'deterministic_designs':len(designs),'exact_supports':supports}

def saturation(T: int, ntheta: int, nstate: int, na: int, ny: int,
               kernel: Callable, prior: tuple[F,...], mode: str|None=None) -> dict:
    initial=[[F(z==0) for z in range(nstate)] for th in range(ntheta)]
    levels=[{():initial}]; likelihood=[]
    for t in range(T):
        nxt={}
        for h,u in levels[-1].items():
            for a,y in it.product(range(na),range(ny)):
                v=[[sum(u[th][z]*kernel(t,th,z,a,zp,y) for z in range(nstate))
                    for zp in range(nstate)] for th in range(ntheta)]
                if sum(prior[th]*sum(v[th]) for th in range(ntheta))>0:
                    nxt[h+((a,y),)]=v
        levels.append(nxt)
    for level in levels:
        likelihood.append({h:tuple(sum(x) for x in u) for h,u in level.items()})
    def posterior(t,h):
        l=likelihood[t][h];b=sum(prior[i]*l[i] for i in range(ntheta))
        return tuple(prior[i]*l[i]/b for i in range(ntheta))
    def pred(t,h,a,y):
        l=likelihood[t][h];b=sum(prior[i]*l[i] for i in range(ntheta))
        ln=likelihood[t+1].get(h+((a,y),),(F(0),)*ntheta)
        return sum(prior[i]*ln[i] for i in range(ntheta))/b
    classes=[{} for _ in range(T+1)]
    for t in range(T,-1,-1):
        keys={}
        for h in levels[t]:
            post=() if mode=='drop_likelihood' else posterior(t,h)
            if t<T:
                continuation=tuple((F(0) if mode=='drop_prediction' else pred(t,h,a,y),
                    classes[t+1].get(h+((a,y),),-1)) for a,y in it.product(range(na),range(ny)))
            else: continuation=()
            key=(post,continuation)
            if key not in keys: keys[key]=len(keys)
            classes[t][h]=keys[key]
    # Check exactly reconstructed parameter-conditional report rows.
    for t in range(T):
        for h in levels[t]:
            for a,th in it.product(range(na),range(ntheta)):
                l=likelihood[t][h][th]
                if not l:continue
                for y in range(ny):
                    hy=h+((a,y),)
                    if hy not in levels[t+1]:continue
                    c=classes[t+1][hy]
                    ys=[q for q in range(ny) if classes[t+1].get(h+((a,q),))==c]
                    refden=sum(pred(t,h,a,q) for q in ys)
                    hiddenclass=sum(likelihood[t+1][h+((a,q),)][th]/l for q in ys)
                    reconstructed=hiddenclass*pred(t,h,a,y)/refden
                    actual=likelihood[t+1][hy][th]/l
                    check(reconstructed==actual,'finite reconstruction fails parameter-uniform change of measure')
    return {'widths':[len(set(c.values())) for c in classes],'classes':classes}

def saturated_examples(mutant: str|None) -> dict:
    def copy(t,th,z,a,zp,y):
        if t==0:return F(1,2) if zp==y else F(0)
        return (F(3,4) if y==zp else F(1,4)) if zp==(z^a) else F(0)
    repeat=saturation(2,1,2,2,2,copy,(F(1),),mutant if mutant=='drop_prediction' else None)
    check(repeat['widths']==[1,2,1],'likelihood-only quotient does not close prediction')
    def reveal(t,th,z,a,zp,y):
        return F(int(zp==0 and y==(th if t==0 else 0)))
    word=saturation(2,2,1,1,2,reveal,(F(1,2),F(1,2)),mutant if mutant=='drop_likelihood' else None)
    check(word['widths']==[1,2,2],'predictive quotient must retain parameter likelihoods')
    def mixed(t,th,z,a,zp,y):
        move=F(2+th+a,5) if zp!=z else 1-F(2+th+a,5)
        sensor=F(3+t,7) if y==zp else 1-F(3+t,7)
        return move*sensor
    u=saturation(3,2,2,2,2,mixed,(F(1,2),F(1,2)))
    v=saturation(3,2,2,2,2,mixed,(F(1,3),F(2,3)))
    for cu,cv in zip(u['classes'],v['classes']):
        hs=list(cu)
        for h,hp in it.product(hs,repeat=2):
            check((cu[h]==cu[hp])==(cv[h]==cv[hp]),'positive-prior change altered saturated equivalence')
    successor={(h,a,0):(h if a else 0) for h,a in it.product(range(2),repeat=2)}
    actions=[0] if mutant=='omit_action' else [0,1]
    compatible=all(successor[(0,a,0)]==successor[(1,a,0)] for a in actions)
    check(not compatible,'controlled compatibility must check every legal action')
    return {'copy_widths':repeat['widths'],'revealing_widths':word['widths'],
            'positive_hmm_widths':u['widths'],'prior_invariance_exact':True}

def pressure(mutant: str|None) -> dict:
    moments=[(1.,math.e),(math.e,1.)]
    actual=math.log((1+math.e)/2)
    tested=.5*(math.log(1)+math.log(math.e)) if mutant=='mix_logarithms' else actual
    check(abs(tested-actual)<1e-12,'mix exponential moments before taking logarithms')
    check(actual>0,'phase-specific optimizer is forbidden to hidden-phase controller')
    return {'common_policy_entropic_risk':actual,'forbidden_phase_oracle_risk':0.}

def gaussian_finite_checks() -> dict:
    sigma=.7
    def post(x):
        z=quad(lambda u:math.exp(-(x-u)**2/(2*sigma*sigma)),-1,1,epsabs=1e-12)[0]
        m=quad(lambda u:u*math.exp(-(x-u)**2/(2*sigma*sigma)),-1,1,epsabs=1e-12)[0]/z
        q=quad(lambda u:u*u*math.exp(-(x-u)**2/(2*sigma*sigma)),-1,1,epsabs=1e-12)[0]/z
        return m,q-m*m
    for x in np.linspace(-2,2,17):
        m,v=post(float(x));der=(post(float(x)+1e-5)[0]-post(float(x)-1e-5)[0])/2e-5
        check(v>0 and abs(der-v/sigma**2)<1e-7,'Gaussian posterior-mean derivative diagnostic')
    d,L=3,3;S=L**d;max_states=[set() for _ in range(d)]
    for bins in it.product(range(L),repeat=d):
        reg=0
        for j,b in enumerate(bins):
            reg=L*reg+b;max_states[j].add(reg)
        for query in range(d):
            selected=(reg//(L**(d-1-query)))%L
            check(selected==bins[query],'delayed-query label not recoverable from charged register')
    sizes=[len(s) for s in max_states]
    check(sizes==[3,9,27] and max(sizes)<=S,'append register exceeds total state budget')
    return {'posterior_derivative_points':17,'register_sizes':sizes,
            'scope':'finite identities only; asymptotic bounds are analytical, not inferred numerically'}

def main() -> int:
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',choices=MUTANTS);args=ap.parse_args()
    try:
        results={'common_tasks':common_tasks(args.mutant),'seed_gap':seed_gap(args.mutant),
                 'controlled_occupancy':controlled_occupancy(),'saturation':saturated_examples(args.mutant),
                 'pressure':pressure(args.mutant),'gaussian':gaussian_finite_checks()}
        if args.mutant:raise RuntimeError('designated mutant survived')
        print(json.dumps({'status':'passed','finite_checks':COUNT,'results':results,
                         'scope':'Exact finite examples and floating-point diagnostics; not a proof certificate.'},indent=2))
        return 0
    except RuntimeError as exc:
        print('FAILED: '+str(exc));return 1
if __name__=='__main__':raise SystemExit(main())
