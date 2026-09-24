#!/usr/bin/env python3
"""Exact finite regressions; not a formal proof of the all-dimensional theorems.

A full-rank matrix of evaluations modulo a prime proves linear independence
of the corresponding integer coefficient polynomials in the n=3 case.
The seed, sample digest and evaluation digest make that witness reproducible.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement
import hashlib,json,math,random
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
P=1009; rng=random.Random(13920260923)

def inverse_det(a):
    a=[[int(x)%P for x in r] for r in a]; n=len(a); det=1
    aug=[a[i]+[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        k=next((i for i in range(j,n) if aug[i][j]),None)
        if k is None: return 0,None
        if j!=k: aug[j],aug[k]=aug[k],aug[j]; det=-det
        v=aug[j][j];det=det*v%P;iv=pow(v,-1,P)
        aug[j]=[x*iv%P for x in aug[j]]
        for i in range(n):
            if i==j: continue
            c=aug[i][j]
            aug[i]=[(x-c*y)%P for x,y in zip(aug[i],aug[j])]
    assert all(aug[i][j]==int(i==j) for i in range(n) for j in range(n))
    return det%P,[r[n:] for r in aug]

def sym2(t):
    mon=list(combinations_with_replacement(range(3),2));mi={q:i for i,q in enumerate(mon)}
    a=[[0]*6 for _ in mon]
    for col,(i,j) in enumerate(mon):
        for k in range(3):
            for l in range(3):
                row=mi[tuple(sorted((k,l)))];a[row][col]=(a[row][col]+t[k][i]*t[l][j])%P
    return a

inds=list(combinations(range(6),4));comps=[tuple(i for i in range(6) if i not in c) for c in inds]
def compound4(a):
    det,iv=inverse_det(a)
    assert det and iv is not None
    out=[]
    for I,Ic in zip(inds,comps):
        row=[]
        for J,Jc in zip(inds,comps):
            x,y=Jc;u,v=Ic
            minor=(iv[x][u]*iv[y][v]-iv[x][v]*iv[y][u])%P
            row.append(((-1)**(sum(I)+sum(J))*det*minor)%P)
        out.append(row)
    return out

def rank_mod(a):
    a=np.asarray(a,dtype=np.int64).copy()%P; rank=0
    for j in range(a.shape[1]):
        nz=np.flatnonzero(a[rank:,j])
        if not len(nz):continue
        k=rank+int(nz[0]);a[[rank,k]]=a[[k,rank]]
        a[rank]=(a[rank]*pow(int(a[rank,j]),-1,P))%P
        if rank+1<a.shape[0]:
            a[rank+1:]=(a[rank+1:]-a[rank+1:,j,None]*a[rank])%P
        rank+=1
        if rank==min(a.shape):break
    return rank

samples=[];ev=[];direct_minor_checks=0;scale_checks=0
while len(samples)<240:
    t=[[rng.randrange(P) for _ in range(3)] for _ in range(3)]
    det,_=inverse_det(t)
    if not det:continue
    a=sym2(t);da,_=inverse_det(a);assert da==pow(det,4,P)
    c=compound4(a)
    # Independent direct 4x4 determinant checks of the complementary-minor formula.
    if len(samples)<12:
        for i,j in [(0,0),(2,7),(8,13),(14,14)]:
            sub=[[a[k][l] for l in inds[j]] for k in inds[i]]
            assert inverse_det(sub)[0]==c[i][j];direct_minor_checks+=1
        scale=7
        ts=[[scale*x%P for x in row] for row in t]
        cs=compound4(sym2(ts));ds,_=inverse_det(ts)
        assert all(ds*cs[i][j]%P==pow(scale,11,P)*det*c[i][j]%P for i in range(15) for j in range(15))
        scale_checks+=225
    samples.append(t)
    # Include the determinant factor: nu, not just residual mu.
    ev.append([det*x%P for row in c for x in row])
r=rank_mod(ev);assert r==225

# The standard Pluecker chart of Gr(2,6), including its exact first derivatives.
x=s.symbols('x0:8');R=s.eye(2).col_join(s.Matrix(4,2,x))
pl=[R[list(I),:].det() for I in combinations(range(6),2)]
assert pl[0]==1
J=s.Matrix(pl).jacobian(x).subs(dict.fromkeys(x,0));assert J.rank()==8
# Line-to-subspace map: every chart block is beta_i times I_15.
# Recover the 8 independent first derivatives by one diagonal entry in each block.
blocks=[b*s.eye(15) for b in pl[1:]]
recovered=s.Matrix([b[0,0] for b in blocks]).jacobian(x).subs(dict.fromkeys(x,0))
assert recovered.rank()==8
for block in blocks:
    assert all(block[i,j]==0 for i in range(15) for j in range(15) if i!=j)
    assert all(block[i,i]==block[0,0] for i in range(15))

orders=[]
for n in range(3,11):
    N=n*(n+1)//2;p=N-2;d=n+2*p;M=math.comb(N,2);h=n*n
    assert p>n and d==n*n+2*n-4
    before=sum(math.comb(h+j-1,j) for j in range(d))
    length=before+math.comb(h+d-1,d)-M
    assert length==math.comb(h+d,d)-M and math.comb(h+d-1,d)>M
    orders.append({'n':n,'p':p,'first_relation_degree':d,'last_constant_order':d-1,
                   'relation_rank':M,'finite_algebra_length':length})
hyper=[{'g':g,'n':2*g+2,'order':4*g*g+12*g+4,'dimension':2*g-1} for g in range(2,9)]
assert all(a['order']==a['n']**2+2*a['n']-4 for a in hyper)
checks={'coefficient_evaluation_rank_225_mod_1009':r==225,
'direct_compound_minor_checks':direct_minor_checks==48,
'homogeneous_degree_eleven_checks':scale_checks==2700,
'pluecker_and_line_subspace_tangent_rank_eight':recovered.rank()==8,
'orders_and_hilbert_length_identities':len(orders)==8,'hyperelliptic_order_substitution':True}
out={'revision':139,'ok':all(checks.values()),'checks':checks,
'coefficient_witness':{'dimension':3,'prime':P,'seed':13920260923,'sample_count':240,'rank':r,
'sample_sha256':hashlib.sha256(json.dumps(samples,separators=(',',':')).encode()).hexdigest(),
'evaluation_sha256':hashlib.sha256(json.dumps(ev,separators=(',',':')).encode()).hexdigest()},
'orders':orders,'hyperelliptic':hyper,
'structural_proofs_not_machine_certified':['intrinsic reconstruction from the nilradical of the d-th neighbourhood',
'global oriented-ruling descent on the projective socle Grassmannian',
'sharp all-dimensional finite-neighbourhood Torelli theorem',
'closed immersion and arbitrary-base-change assertions in all dimensions',
'full historical novelty and Ballico 1993 theorem-level comparison']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION139_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['ok']
