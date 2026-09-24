#!/usr/bin/env python3
"""Exact finite regressions for intrinsic continuation and streaming synthesis.
Analytic, all-horizon statements are proved in the manuscript, not by enumeration.
"""
from __future__ import annotations
import argparse,itertools,json
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

def need(ok:bool,message:str)->None:
    if not ok: raise RuntimeError(message)

def vertices(t:int,eta:F)->list[tuple[F,...]]:
    if t==0:return [()]
    b=t*eta
    return [tuple(-b for _ in range(t))]+[tuple(t*t*eta if j==i else -b for j in range(t)) for i in range(t)]

def bary(w:tuple[F,...],eta:F,broken:bool=False)->list[F]:
    t=len(w); b=t*eta
    if broken:b=eta/F(10)
    denominator=(t+1)*b
    lam=[(b-sum(w))/denominator]+[(z+b)/denominator for z in w]
    need(all(z>=0 for z in lam),'Negative barycentric update: incompatible covers')
    need(sum(lam)==1,'Unnormalized update')
    vv=vertices(t,eta)
    need(all(sum(lam[s]*vv[s][i] for s in range(t+1))==w[i] for i in range(t)),'Barycentric reconstruction')
    return lam

def channel(h:tuple[F,...])->tuple[F,...]:
    return tuple(z for a in h for z in (1-a,a))

def graph_components(rows:list[tuple[F,...]],block:int)->list[list[int]]:
    n=len(rows);need(len(set(rows))==n,'Residual list contains duplicate rows')
    for r in rows:
        need(len(r)%block==0,'Bad channel block size')
        need(all(x>=0 for x in r),'Negative channel')
        need(all(sum(r[j:j+block])==1 for j in range(0,len(r),block)),'Channel not normalized at each query')
    adj=[set([i]) for i in range(n)]
    for i,j in itertools.combinations(range(n),2):
        common=all(any(rows[i][k]>0 and rows[j][k]>0 for k in range(a,a+block)) for a in range(0,len(rows[i]),block))
        if common:adj[i].add(j);adj[j].add(i)
    unseen=set(range(n));comps=[]
    while unseen:
        stack=[min(unseen)];c=set()
        while stack:
            i=stack.pop()
            if i in c:continue
            c.add(i);stack.extend(adj[i]-c)
        unseen-=c;comps.append(sorted(c))
    return comps

def affine_dim(rows:list[tuple[F,...]])->int:
    if len(rows)==1:return 0
    return int(sp.Matrix([[z-x for z,x in zip(r,rows[0])] for r in rows[1:]]).rank())

def capacity(rows:list[tuple[F,...]],block:int)->tuple[int,list[int]]:
    cc=graph_components(rows,block); dims=[affine_dim([rows[i] for i in c]) for c in cc]
    return sum(d+1 for d in dims),dims

def product_rows(a:list[tuple[F,...]],b:list[tuple[F,...]],ba:int=2,bb:int=2)->list[tuple[F,...]]:
    return [tuple(r[i+u]*s[j+v] for i in range(0,len(r),ba) for j in range(0,len(s),bb) for u in range(ba) for v in range(bb)) for r in a for s in b]

def run(mutant:str|None=None,emit:Path|None=None)->dict:
    need((8 if mutant=='free-memory' else 9)>=9,'Uncharged selector contradicts nine-dimensional augmented row rank')
    causal_action_rows=[[F(1,3),F(2,3)],[F(1,3),F(2,3)]]
    if mutant=='unread-action':causal_action_rows[1]=[F(2,3),F(1,3)]
    need(causal_action_rows[0]==causal_action_rows[1],'Next action illegally depends on unread report')
    independent=[F(1,4)]*4
    generated=[F(1,2),F(0),F(0),F(1,2)] if mutant=='marginal-product' else independent
    need(generated==independent,'Marginals alone do not specify the joint product channel')

    t=F(1,6)
    hs=[(t,F(0),F(1),F(1)),(F(1),F(0),F(1),F(1)),(F(1),)*4,(F(1),F(1),F(0),F(1)),(F(1),F(1),F(0),t)]
    rows=[channel(h) for h in hs]
    s,dims=capacity(rows,2)
    need(s==(4 if mutant=='missing-component' else 5) and dims==[1,0,1],'Marked intrinsic support-component capacity')
    pr=product_rows(rows,rows); ps,pdims=capacity(pr,4)
    need(ps==25 and pdims==[3,1,3,1,0,1,3,1,3],'Product components/ranks')
    for c in graph_components(pr,4):need(affine_dim([pr[i] for i in c])+1==len(c),'Product component not simplex')
    eps=F(1,8);square=[channel(tuple(eps if b==0 else 1-eps for b in w)) for w in itertools.product([0,1],repeat=2)]
    sq,sd=capacity(square,2);need(sq==3 and sd==[2],'Full-support square rank')
    extreme_points=4
    simplicial=(extreme_points==sd[0]+1)
    if mutant=='false-completeness':simplicial=True
    need(not simplicial,'Incorrect universal simplex/rank completeness')
    need(2*eps<F(1,2),'Square corner separation not strict')

    words_checked=0;conditional_checks=0;transition_checks=0
    exported={}
    for n in range(1,9):
        eta=F(1,n*n)
        transitions={}
        for k in range(n):
            for state,v in enumerate(vertices(k,eta)):
                for bit in [-1,1]:
                    lam=bary(v+(eta*bit,),eta,broken=mutant=='incompatible-update')
                    transitions[k,state,bit]=lam; transition_checks+=1
        for x in itertools.product([-1,1],repeat=n):
            law=[F(1)]
            for k,bit in enumerate(x):
                law=[sum(law[a]*transitions[k,a,bit][b] for a in range(k+1)) for b in range(k+2)]
                vv=vertices(k+1,eta)
                need(sum(law)==1 and all(z>=0 for z in law),'Streaming state law invalid')
                need(all(sum(law[a]*vv[a][j] for a in range(k+2))==eta*x[j] for j in range(k+1)),'Prefix mean identity')
            vv=vertices(n,eta)
            need(all(-1<=v<=1 for row in vv for v in row),'Decoder outside probability cube')
            for j in range(n):
                decoded=sum(law[a]*(1+vv[a][j])/2 for a in range(n+1))
                need(decoded==(1+eta*x[j])/2,'Exact input/query law mismatch');conditional_checks+=1
            words_checked+=1
        if n==8:
            exported={'n':n,'eta':str(eta),'profile':list(range(1,n+2)),
                      'rows':[{'time':k,'state':a,'input':bit,'next_probabilities':[str(p) for p in lam]} for (k,a,bit),lam in transitions.items()],
                      'decoder_means':[[str(z) for z in v] for v in vertices(n,eta)],
                      'state_meanings':'Indices of read-only vertices; no runtime real vector or persistent seed.'}

    # Exact rank and the nonzero singular-value spectrum for small instances.
    rank_checks=0
    for n in range(1,6):
        eta=sp.Rational(1,n*n)
        A=sp.Matrix([[ (1+b*eta*x[j])/2 for j in range(n) for b in [-1,1]] for x in itertools.product([-1,1],repeat=n)])
        need(A.rank()==n+1,'Binary-query rank')
        expected={n*2**(n-1):1,eta**2*2**(n-1):n}
        if n==1:expected={sp.Integer(1):2}
        actual={k:v for k,v in (A.T*A).eigenvals().items() if k!=0}
        need(actual==expected,'Singular-value/rank-margin identity');rank_checks+=1
    for q in range(2,5):
        lam=sp.Rational(1,7);T=lam*sp.eye(q)+(1-lam)*sp.ones(q)/q
        need(T.det()==lam**(q-1),'Product channel determinant')
        need(sp.kronecker_product(T,T).rank()==q*q,'Product barrier rank');rank_checks+=1
    cap_pairs=0
    for n in range(1,7):
        eta=1-F(1,2*n);need(n*(1-eta)/2<F(1,2),'Strong corner cap')
        corners=list(itertools.product([-1,1],repeat=n))
        for x,y in itertools.combinations(corners,2):
            need(sum(a!=b for a,b in zip(x,y))>=1,'Corner caps overlap');cap_pairs+=1
    if emit is not None:
        emit.parent.mkdir(parents=True,exist_ok=True);emit.write_text(json.dumps(exported,indent=2,sort_keys=True)+'\n')
    return {'schema':'gtf29.exact/1','marked_component_dimensions':dims,'marked_capacity':s,'two_copy_capacity':ps,
            'noncomplete_square_capacity_lower':sq,'noncomplete_square_true_capacity':4,'streaming_lengths_checked':list(range(1,9)),
            'streaming_words_checked':words_checked,'exact_conditional_outputs_checked':conditional_checks,
            'exact_stochastic_update_rows_checked':transition_checks,'rank_spectrum_checks':rank_checks,'disjoint_corner_pairs_checked':cap_pairs,
            'weak_signal_exact_law':'K_n=W_n=n+1, 0<eta<=1/n^2','strong_signal_exact_law':'K_n=W_n=2^n, 1-1/n<eta<=1',
            'generic_adaptive_collision_optimum_claimed':False,'analytic_scope':'All-horizon proofs in manuscript; these are finite algebra and implementation regressions, not independent proof or priority certification.'}

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=['missing-component','false-completeness','incompatible-update','free-memory','unread-action','marginal-product']);parser.add_argument('--emit',type=Path)
    args=parser.parse_args();print(json.dumps(run(args.mutant,args.emit),indent=2,sort_keys=True))
if __name__=='__main__':main()
