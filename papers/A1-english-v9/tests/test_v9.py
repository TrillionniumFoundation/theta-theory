#!/usr/bin/env python3
"""Finite exact diagnostics of v9. No continuum or all-prior proof certification.

The index-only fixtures use a finite command menu and arbitrary reachable
codebooks, not the continuum-optimal codebooks whose existence is proved.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations, product
from functools import lru_cache
import hashlib, json, math, platform, random, re
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
CHECKS=[]
def check(name, ok, **details):
    if not ok: raise AssertionError((name,details))
    CHECKS.append({'name':name,'passed':True,**details})
def prod(xs):
    out=F(1)
    for x in xs:out*=x
    return out

def leja(nodes):
    rest=list(enumerate(map(F,nodes))); selected=[]; scales=[]
    while rest:
        if not selected:j=min(range(len(rest)),key=lambda j:(rest[j][1],rest[j][0]))
        else:j=max(range(len(rest)),key=lambda j:(prod(abs(rest[j][1]-x) for x in selected),-rest[j][0]))
        _,x=rest.pop(j);scales.append(prod(abs(x-y) for y in selected));selected.append(x)
    return selected,scales

def detvol(nodes,k):
    return max((prod(abs(x-y) for x,y in combinations(c,2)) for c in combinations(nodes,k)),default=F(0))

def complete_homogeneous(nodes,degree):
    if degree<0:return F(0)
    h=[F(1)]+[F(0)]*degree
    for x in nodes:
        for k in range(1,degree+1):h[k]+=x*h[k-1]
    return h[degree]

rng=random.Random(90609)
configs=[[F(1,5)]*5,[F(1,8),F(1,8),F(1,4),F(1,4),F(3,4)],
 [F(1,3),F(1,3)+F(1,10**9),F(1,3)+F(1,10**3),F(5,6)]]
configs += [[F(rng.randrange(1,17),17) for _ in range(q)] for q in range(2,9) for _ in range(4)]
for case,nodes in enumerate(configs):
    x,d=leja(nodes);q=len(x);s=len(set(x))
    check(f'leja-monotonic-zero-tail-{case}',all(d[j]>=d[j+1] for j in range(q-1)) and all(t==0 for t in d[s:]))
    L=[[prod(xi-y for y in x[:j])/d[j] if d[j] else F(0) for j in range(q)] for xi in x]
    check(f'leja-bounded-triangular-{case}',all(abs(z)<=1 for row in L for z in row) and all(abs(L[j][j])==1 for j in range(s)))
    for ell in range(1,q+1):
        v=detvol(x,ell);dl=prod(d[:ell])
        check(f'determinant-volume-{case}-{ell}',dl<=v<=math.factorial(ell)*dl)
    for degree in (0,1,q-1,q,q+2):
        g=[complete_homogeneous(x[:j+1],degree-j) for j in range(q)]
        # Newton interpolation is exact at all nodes even for a polynomial
        # of degree above the number of distinct sites; the remainder vanishes.
        recovered=[sum(L[i][j]*d[j]*g[j] for j in range(q)) for i in range(q)]
        check(f'hermite-newton-evaluation-{case}-{degree}',recovered==[xi**degree for xi in x])

@lru_cache(None)
def labels(r,m):
    if r==1:return ((m,),)
    return tuple((j,)+a for j in range(m+1) for a in labels(r-1,m-j))
def exponent(A,alpha):return sum((a*b for a,b in zip(A,alpha)),F(0))
def positive_nodes(A,m,H=F(20)):
    return [exponent(A,a)/H for a in labels(len(A),m) if any(a[1:])]
def moment(e,prior):
    if prior==0:return 1/(e+1)
    if prior==1:return 2/(e+2)
    return F(1,2)/(e+1)+F(1,4)+F(e==0,4)
def ddmoment(b,xs,H,prior):
    # Exact exponent divided difference of the integral, including repeated nodes.
    j=len(xs)
    uniform=(-H)**(j-1)/prod(b+H*x+1 for x in xs)
    if prior==0:return uniform
    if prior==1:return 2*(-H)**(j-1)/prod(b+H*x+2 for x in xs)
    return uniform/2+F(j==1,4)  # positive g_j vanish at t=0

def rank(rows):return int(sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(rows)).rank())
calibrations=[(F(0),F(1),F(2)),(F(0),F(1),F(2)+F(1,1000)),
 (F(0),F(1),F(2),F(3)),(F(0),F(1),F(2)+F(1,32),F(3)+F(1,32)),
 (F(0),F(1),F(2)+F(1,32),F(3)+F(1,32)+F(1,32**4))]
for ci,A in enumerate(calibrations):
    r=len(A);D=A[-1];H=F(20)
    for n,m in ((1,2),(2,2),(3,2),(2,3)):
        B=sorted({j*D for j in range(n+1)}|{a+j*D for a in A[1:-1] for j in range(n)})
        x,d=leja(positive_nodes(A,m,H));p=min(n*(r-1),len(x))
        # Include a nongreedy order to test the repeated-node flag lemma itself.
        for ordering,xs in (('greedy',x),('reverse',list(reversed(x)))):
            for prior in (0,1,2):
                mat=[[moment(b,prior)]+[ddmoment(b,xs[:j],H,prior) for j in range(1,p+1)] for b in B]
                check(f'complete-newton-pairing-{ci}-{n}-{m}-{ordering}-{prior}',rank(mat)==p+1,rank=p+1)
                P={F(0):F(1)}
                for i in range(1,n+1):
                    out={}
                    for b,v in P.items():
                        out[b]=out.get(b,F(0))+v;out[b+D]=out.get(b+D,F(0))+v*F(i,100*(n+1))
                    P=out
                ev=sum(v*moment(b,prior) for b,v in P.items())
                z=[sum(v*ddmoment(b,xs[:j],H,prior) for b,v in P.items())/ev for j in range(1,p+1)]
                normalized=[[row[j+1]-z[j]*row[0] for j in range(p)] for row in mat]
                check(f'normalized-newton-rank-{ci}-{n}-{m}-{ordering}-{prior}',rank(normalized)==p,rank=p)

# Pair-order tree allocation, checked against independent subset enumeration.
def valuation(a,b):
    for j in range(max(len(a),len(b))):
        if (a[j] if j<len(a) else 0)!=(b[j] if j<len(b) else 0):return j
    raise ValueError('identical analytic labels must be identified')
def merge_tables(tables):
    out=[0]
    for table in tables:
        new=[math.inf]*(len(out)+len(table)-1)
        for i,x in enumerate(out):
            for j,y in enumerate(table):new[i+j]=min(new[i+j],x+y)
        out=new
    return out

def tree_energies(W):
    def classes(ids,height):
        groups=[]
        for i in ids:
            for g in groups:
                if W[i][g[0]]>height:g.append(i);break
            else:groups.append([i])
        return groups
    def solve(ids,parent):
        if len(ids)==1:return [0,0]
        height=min(W[i][j] for i,j in combinations(ids,2))
        groups=classes(ids,height)
        out=merge_tables([solve(g,height) for g in groups])
        return [v+(height-parent)*k*(k-1)//2 for k,v in enumerate(out)]
    ids=list(range(len(W)))
    return merge_tables([solve(g,0) for g in classes(ids,0)])

trees=[[(1,),(1,1),(1,0,1)],[(1,),(1,1),(1,1,0,1),(2,),(2,0,1)],
 [(1,),(1,0,0,1),(1,0,0,2),(1,1),(2,),(2,0,1),(3,)]]
for ci,polys in enumerate(trees):
    W=[[math.inf if i==j else valuation(a,b) for j,b in enumerate(polys)] for i,a in enumerate(polys)]
    Ftree=tree_energies(W)
    brute=[0]+[min(sum(W[i][j] for i,j in combinations(c,2)) for c in combinations(range(len(W)),ell)) for ell in range(1,len(W)+1)]
    check(f'collision-tree-versus-subset-{ci}',Ftree==brute,energies=Ftree)

for k in (2,3,5,8):
    A=[(0,),(1,),(2,1),tuple([3,1]+[0]*(k-2)+[1])]
    polys=[]
    for alpha in labels(4,2):
        if not any(alpha[1:]):continue
        polys.append(tuple(sum(alpha[i]*(A[i][j] if j<len(A[i]) else 0) for i in range(4)) for j in range(k+1)))
    W=[[math.inf if i==j else valuation(a,b) for j,b in enumerate(polys)] for i,a in enumerate(polys)]
    energies=tree_energies(W)
    check(f'tangent-path-energy-k{k}',energies==[0]+[0]*6+[1,2,k+2],energies=energies)
    for b,expected in ((F(6),F(2)),(F(8*k-2),F(2*k))):
        exps=[F(2*(energies[ell]+b),ell) for ell in range(1,10)]
        check(f'tangent-crossover-k{k}-budget{b}',min(exps)==expected)

# A physical index-only transducer with r=4, five counted trials and collisions.
COMMANDS=((F(1,4),F(1,2),F(3,4),F(1,3)),(F(2,3),F(1,3),F(1,2),F(1,4)))
CELLS=((F(1,4),F(1,16),F(1,16),F(1,16)),
       (F(1,4),-F(1,16),F(0),F(0)),(F(1,4),F(0),-F(1,16),F(0)),
       (F(1,4),F(0),F(0),-F(1,16)))
def factor(ci,report):
    g=COMMANDS[ci]
    if report:return tuple(g[report-1]*v for v in CELLS[report-1])
    return tuple(sum((1-g[j])*CELLS[j][i] for j in range(4)) for i in range(4))
def direct_multiply(P,co,A):
    out={}
    for b,v in P.items():
        for a,f in zip(A,co):out[b+a]=out.get(b+a,F(0))+v*f
    return {b:v for b,v in out.items() if v}
def integrate(P,shift,prior):return sum((v*moment(b+shift,prior) for b,v in P.items()),F(0))
def reference(P,m,A,prior):
    ev=integrate(P,F(0),prior)
    return {alpha:integrate(P,exponent(A,alpha),prior)/ev for alpha in labels(4,m)}
def raw_update(v,m,co):
    denom=sum(co[i]*v[tuple((m-1 if j==0 else 0)+(1 if j==i else 0) for j in range(4))] for i in range(4))
    if denom<F(1,64):raise AssertionError('invalid positive denominator')
    return {a:sum(co[i]*v[tuple(a[j]+(j==i) for j in range(4))] for i in range(4))/denom for a in labels(4,m-1)}
def distance(v,w):return sum((v[a]-w[a])**2 for a in v)
class IndexOnly:
    __slots__=('index',)
    def __init__(self):self.index=0
    def step(self,table,command,report):
        self.index=table[self.index,command,report]
        return self.index
fixtures=0;updates=0
caluv=[(F(0),F(0)),(F(0),F(1,32)),(F(1,32),F(1,32)),
       (F(1,32),F(1,16)),(F(1,32),F(1,64)),
       (F(1,32),F(1,32)+F(1,32**4)),(-F(1,32),F(1,32))]
for ci,(u,vv) in enumerate(caluv):
    A=(F(0),F(1),F(2)+u,F(3)+vv)
    for M in (1,3):
        prior=0 if M==1 else 2
        books=[[reference({F(0):F(1)},5,A,prior)]];tables=[]
        for n in range(5):
            candidates=[];keys=[]
            for idx,v in enumerate(books[-1]):
                for command,report in product(range(2),range(5)):
                    candidates.append(raw_update(v,5-n,factor(command,report)));keys.append((idx,command,report))
            unique=list({tuple(v.items()):v for v in candidates}.values());size=min(M,len(unique))
            reps=[unique[j*len(unique)//size] for j in range(size)]
            tables.append({key:min(range(size),key=lambda j:distance(w,reps[j])) for key,w in zip(keys,candidates)})
            books.append(reps)
        for stream in range(12):
            machine=IndexOnly();P={F(0):F(1)};exact=books[0][0]
            for n in range(5):
                command,report=rng.randrange(2),rng.randrange(5);co=factor(command,report)
                exact=raw_update(exact,5-n,co);P=direct_multiply(P,co,A)
                if exact!=reference(P,4-n,A,prior):raise AssertionError('raw/direct mismatch')
                idx=machine.step(tables[n],command,report)
                if not 0<=idx<M:raise AssertionError('state budget')
                if any(not 0<=x<=1 for x in books[n+1][idx].values()):raise AssertionError('unreachable representative')
                updates+=1
        check(f'index-only-collision-fixture-{ci}-M{M}',True,streams=12,updates=60,
              persistent_fields=['index'],codebooks='finite-input reachable, not asymptotically optimal')
        fixtures+=1

# The exact source-pinned input is included even in standalone bundles.
meta=json.loads((ROOT/'validation/V8_PREDECESSOR.json').read_text())
new='\n'.join(p.read_text() for p in sorted((ROOT/'sections').glob('*.tex')))
labels_new=set(re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',new))
proofs_new=re.findall(r'\\begin\{proof\}(?:\[[^\]]*\])?.*?\\end\{proof\}',new,re.S)
hashes={hashlib.sha256(x.encode()).hexdigest() for x in proofs_new}
check('all-34-v8-result-labels-retained',set(meta['result_labels'])<=labels_new)
check('all-33-v8-proof-blocks-byte-identical',set(meta['proof_sha256'])<=hashes)
receipt={'revision':'A1 English v9','python':platform.python_version(),'sympy':sp.__version__,
 'passed':len(CHECKS),'executed':len(CHECKS),'failed':0,'skipped':[],
 'index_only_fixtures':fixtures,'exact_raw_update_comparisons':updates,
 'predecessor_result_labels':len(meta['result_labels']),'predecessor_proof_blocks':len(meta['proof_sha256']),
 'current_result_labels':len(labels_new),'current_proof_blocks':len(proofs_new),'checks':CHECKS,
 'scope':'Finite diagnostics; not a proof of the continuum covering, all-prior rank, codebook synthesis, originality, or editorial acceptance.'}
(ROOT/'V9_DIAGNOSTICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
