#!/usr/bin/env python3
"""Finite, independently implemented diagnostics. Not an analytic proof checker."""
from __future__ import annotations
import argparse
from itertools import product, combinations_with_replacement
import json
import math
import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import expm
from scipy.special import ndtr

MUTANTS=('checkpoint_only','fill_null','pairwise_cover','seed_marginal',
         'memory_sign','drop_forcing','discount_formula','resolved_is_full')
parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS)
ARGS=parser.parse_args(); counts={}
def check(ok:bool,group:str,message:str)->None:
    counts[group]=counts.get(group,0)+1
    if not bool(ok):raise RuntimeError('FAILED: '+message)
def compatible(c:tuple[int,...],allowed:tuple[frozenset[int],...])->bool:
    z={0,1}
    for h in c:z.intersection_update(allowed[h])
    return bool(z)
def cells(n:int,allowed:tuple[frozenset[int],...])->list[tuple[int,...]]:
    return [tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)
            if compatible(tuple(i for i in range(n) if mask>>i&1),allowed)]
def covers(n:int,allowed:tuple[frozenset[int],...],s:int):
    for cc in combinations_with_replacement(cells(n,allowed),s):
        if set().union(*(set(c) for c in cc))==set(range(n)):yield cc

def closed_cover(edges:tuple[tuple[int,int],...],opt0,targets,s0:int,s1:int)->bool:
    """Enumerate overlapping compatible covers; do not enumerate machines."""
    opt1=tuple(frozenset({t}) for t in targets)
    for c1 in covers(len(edges),opt1,s1):
        for c0 in covers(2,opt0,s0):
            good=True
            for cell in c0:
                for y in (0,1):
                    successor={i for i,(h,z) in enumerate(edges) if h in cell and z==y}
                    if not any(successor<=set(c) for c in c1):good=False;break
                if not good:break
            if good:return True
    return False

def machine_feasible(edges,opt0,targets,s0:int,s1:int)->bool:
    """Enumerate deterministic initialization/update tables, not covers."""
    for initial in product(range(s0),repeat=2):
        if not all(compatible(tuple(h for h in range(2) if initial[h]==m),opt0) for m in range(s0)):continue
        for transition in product(range(s1),repeat=2*s0):
            outputs=[transition[2*initial[h]+y] for h,y in edges]
            if all(len({targets[i] for i in range(len(edges)) if outputs[i]==m})<=1 for m in range(s1)):
                return True
    return False

rng=np.random.default_rng(20260923)
opts=[(frozenset({0,1}),frozenset({0,1})),
      (frozenset({0}),frozenset({1})),
      (frozenset({0}),frozenset({0,1}))]
for supp0,supp1 in product(((0,),(1,),(0,1)),repeat=2):
    edges=tuple((h,y) for h,supp in enumerate((supp0,supp1)) for y in supp)
    for targets in product((0,1),repeat=len(edges)):
        for opt0 in opts:
            for s0,s1 in product((1,2),repeat=2):
                c=closed_cover(edges,opt0,targets,s0,s1)
                m=machine_feasible(edges,opt0,targets,s0,s1)
                check(c==m,'cover_machine','cover/table mismatch')
                if not c:
                    alpha=0.5/max(2,len(edges))
                    for _ in range(3):
                        q0=rng.dirichlet(np.ones(s0),size=2)
                        q1=rng.dirichlet(np.ones(s1),size=(s0,2))
                        v0=rng.dirichlet(np.ones(2),size=s0)
                        v1=rng.dirichlet(np.ones(2),size=s1)
                        risk0=sum(q0[h,k]*v0[k,b]*(b not in opt0[h]) for h in range(2) for k in range(s0) for b in (0,1))/2
                        risk1=0.0
                        for i,(h,y) in enumerate(edges):
                            dist=q0[h]@q1[:,y,:]
                            risk1+=sum(dist[k]*v1[k,b]*(b!=targets[i]) for k in range(s1) for b in (0,1))/len(edges)
                        check((risk0+risk1)/2+1e-13>=alpha,'randomized_gap','positive risk witness violated')

optconst=opts[0]
actual=machine_feasible(((0,0),(1,0)),optconst,(0,1),1,2)
if ARGS.mutant=='checkpoint_only':actual=True
check(not actual,'negative_targets','checkpoint minima are not causally feasible')
actual=machine_feasible(((0,0),(1,1)),optconst,(0,1),1,2)
if ARGS.mutant=='fill_null':actual=False
check(actual,'negative_targets','null successor completion overcharges state')
sets=({0,1},{1,2},{0,2})
actual=bool(set.intersection(*sets))
if ARGS.mutant=='pairwise_cover':actual=all(sets[i]&sets[j] for i in range(3) for j in range(i+1,3))
check(not actual,'negative_targets','pairwise compatibility is not joint compatibility')
# Marginals (Y,W) agree, but adjoining the simulator's seed distinguishes them.
true=np.full((2,2,2),1/8); simulated=np.zeros((2,2,2))
for w,u in product((0,1),repeat=2):simulated[w^u,w,u]=1/4
marginal_tv=np.abs(true.sum(axis=2)-simulated.sum(axis=2)).sum()/2
joint_tv=np.abs(true-simulated).sum()/2
actual=joint_tv if ARGS.mutant!='seed_marginal' else marginal_tv
check(marginal_tv==0 and actual==0.5,'negative_targets','public-seed marginal bound is insufficient')
for beta,e in product((0.1,0.5,0.9,0.99),(0.001,0.03,0.2,1.0)):
    exact=e/(1-beta+beta*e)
    summed=sum((1-beta)*beta**t*(1-(1-e)**(t+1)) for t in range(8000))
    if ARGS.mutant=='discount_formula':exact=e/(1-beta)
    check(abs(summed-exact)<2e-12,'discount','incorrect coherent geometric error')
    for N in (0,1,8,40):
        partial=sum((1-beta)*beta**t*(1-(1-e)**(t+1)) for t in range(N+1))
        check(-2e-12<=exact-partial<=beta**(N+1)+2e-12,'discount','tail comparison bound')
for gap in (0.01,0.1,0.5):
    for eps in (gap/16,gap/8,gap/5):
        check(2*eps<gap/2<gap-2*eps,'certificate','separating threshold')
for shift,sigma in product((0.0,0.001,0.1,1.0,8.0),(0.2,1.0,3.0)):
    tv=2*ndtr(abs(shift)/(2*sigma))-1
    check(tv<=abs(shift)/(sigma*math.sqrt(2*math.pi))+1e-14,'gaussian','normal translation bound')
for trial in range(6):
    raw=rng.normal(size=(6,6)); L=(raw-raw.T)/5
    A=L[:2,:2]; B=L[:2,2:]; C=L[2:,:2]; D=L[2:,2:]
    K0=B@C
    if ARGS.mutant=='memory_sign':K0=-K0
    check(np.linalg.norm(K0+C.T@C)<1e-13,'memory','wrong skew memory sign')
    f=rng.normal(size=6)
    for t in (0.2,0.7,1.3):
        trajectory=expm(t*L)@f; derivative=(L@trajectory)[:2]
        conv=quad_vec(lambda s:B@expm((t-s)*D)@C@(expm(s*L)@f)[:2],0,t,epsabs=1e-11)[0]
        forcing=B@expm(t*D)@f[2:]
        rhs=A@trajectory[:2]+conv+forcing
        check(np.linalg.norm(derivative-rhs)<1e-10,'memory','forced Volterra identity')
        for z in (0.5+0.7j,2+3j):
            compression=np.linalg.inv(z*np.eye(6)-L)[:2,:2]
            inverse=z*np.eye(2)-A-B@np.linalg.solve(z*np.eye(4)-D,C)
            check(np.linalg.norm(np.linalg.inv(compression)-inverse)<1e-11,'memory','Schur inverse mismatch')
        Lhat=L.copy(); Lhat[:2,:2]-=0.03*np.eye(2)
        error=np.linalg.norm((expm(t*L)@f-expm(t*Lhat)@f)[:2])
        bound=t*0.03*np.linalg.norm(f)*math.cosh(math.sqrt(np.linalg.norm(B,2)*np.linalg.norm(C,2))*t)
        check(error<=bound+1e-12,'memory','Volterra stability bound')
        for m in (4,16,64):
            euler=np.linalg.matrix_power(np.linalg.inv(np.eye(6)-t*L/m),m)@f
            bound=t*np.linalg.norm(L@f)/math.sqrt(m)
            check(np.linalg.norm(euler-trajectory)<=bound+1e-12,'galerkin','Euler gamma estimate')
L=np.array([[0.,1.],[-1.,0.]]); f=np.array([0.,1.])
forcing=1.0 if ARGS.mutant!='drop_forcing' else 0.0
check(abs((L@f)[0]-forcing)<1e-14,'negative_targets','unresolved initial forcing erased')
full_error=np.linalg.norm(f-np.array([f[0],0.]))
if ARGS.mutant=='resolved_is_full':full_error=0.0
check(full_error==1.0,'negative_targets','resolved accuracy is not full observable accuracy')
# A finite tridiagonal test of the graph-core approximation mechanism, not an infinite proof.
L=np.zeros((32,32))
for k in range(31):L[k,k+1]=k+1;L[k+1,k]=-(k+1)
f=np.eye(32)[:,0]; exact=expm(0.15*L)@f
for n in (2,4,8,16,24,32):
    approx=np.zeros(32);approx[:n]=expm(0.15*L[:n,:n])@f[:n]
    check(abs(np.linalg.norm(approx)-1)<1e-12,'galerkin','Galerkin unitarity')
    if n>=16:check(np.linalg.norm(approx-exact)<1e-10,'galerkin','finite graph-core convergence diagnostic')
if ARGS.mutant:raise RuntimeError('FAILED: designated mutant survived')
print(json.dumps({'status':'passed','finite_checks':sum(counts.values()),'groups':counts,
                  'seed':20260923,'scope':'Finite exact enumeration and numerical identities only; not certification of analytic proofs.'},indent=2))
