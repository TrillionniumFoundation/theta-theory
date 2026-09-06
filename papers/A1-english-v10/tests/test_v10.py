#!/usr/bin/env python3
"""Finite rational diagnostics of shared-state composition.

These checks do not establish continuum covers, all-prior minorization,
optimal asymptotics, formal proof verification, or editorial significance.
The machine fixture keeps only an index; witness histories and exact
prefixes belong exclusively to the independent reference computation.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json, math, platform, random, re
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
CHECKS=[]
def check(name, condition, **details):
    if not condition: raise AssertionError((name,details))
    CHECKS.append({'name':name,'passed':True,**details})
def prod(xs):
    ans=F(1)
    for x in xs: ans*=x
    return ans

def leja(nodes):
    rest=list(enumerate(map(F,nodes))); xs=[]; ds=[]
    while rest:
        j=min(range(len(rest)),key=lambda j:(rest[j][1],rest[j][0])) if not xs else max(
            range(len(rest)),key=lambda j:(prod(abs(rest[j][1]-x) for x in xs),-rest[j][0]))
        _,x=rest.pop(j);ds.append(prod(abs(x-y) for y in xs));xs.append(x)
    return xs,ds

def volumes(nodes,p):
    return [F(1)]+[max((prod(abs(x-y) for x,y in combinations(c,2))
                for c in combinations(nodes,k)),default=F(0)) for k in range(1,p+1)]

def convolution(a,b):
    return [max((a[i]*b[k-i] for i in range(len(a)) if 0<=k-i<len(b)),default=F(0))
            for k in range(len(a)+len(b)-1)]

# Real ordinary Vandermonde factorization, with repeats and tiny gaps.
rng=random.Random(100906)
configs=[[F(1,3)]*4,[F(1,9),F(2,9),F(2,9),F(7,9)],
         [F(1,3),F(1,3)+F(1,10**12),F(3,4)]]
configs += [[F(rng.randrange(0,13),13) for _ in range(q)] for q in range(2,7) for _ in range(3)]
z=sp.Symbol('z')
for ci,nodes in enumerate(configs):
    xs,ds=leja(nodes);q=len(xs);s=len(set(xs))
    W=sp.Matrix([[x**j for j in range(q)] for x in xs])
    polys=[sp.expand(sp.prod(z-x for x in xs[:j])) for j in range(q)]
    T=sp.Matrix([[p.coeff(z,i) for p in polys] for i in range(q)])
    L=sp.Matrix([[prod(x-y for y in xs[:j])/ds[j] if j<s else F(i==j)
                  for j in range(q)] for i,x in enumerate(xs)])
    check(f'ordinary-factorization-{ci}',W*T==L*sp.diag(*ds))
    check(f'invertible-bounded-change-{ci}',T.det()==1 and abs(L.det())==1 and all(abs(t)<=1 for t in L))
    check(f'zero-tail-{ci}',all(t>0 for t in ds[:s]) and all(t==0 for t in ds[s:]))
    vv=volumes(xs,q)
    for k in range(1,q+1):
        check(f'exterior-product-comparison-{ci}-{k}',prod(ds[:k])<=vv[k]<=math.factorial(k)*prod(ds[:k]))

# Max-product composition retains each block's own attainable cap.
block_cases=[([F(1,9),F(2,9),F(5,9)],1),
             ([F(1,8),F(1,8),F(3,8),F(6,8)],3),
             ([F(1,7),F(1,7)+F(1,10000),F(4,7)],2),
             ([F(1,3)]*3,3), ([],0)]
for ci,indices in enumerate(product(range(len(block_cases)),repeat=3)):
    vv=[];dds=[]
    for ix in indices:
        nodes,p=block_cases[ix];vv.append(volumes(nodes,p));dds.extend(leja(nodes)[1][:p])
    a=convolution(convolution(vv[0],vv[1]),vv[2]);b=convolution(vv[0],convolution(vv[1],vv[2]))
    check(f'associativity-{ci}',a==b)
    allocations=list(product(*(range(len(v)) for v in vv)))
    check(f'allocation-definition-{ci}',a==[max((prod(v[l] for v,l in zip(vv,ls)) for ls in allocations if sum(ls)==k),default=F(0)) for k in range(len(a))])
    dds.sort(reverse=True)
    factor=prod(math.factorial(len(v)-1) for v in vv)
    for k in range(len(a)):
        d=prod(dds[:k]);check(f'merged-attained-axes-{ci}-{k}',d<=a[k]<=factor*d)
    for accuracy_power in [0,1,4,13]:
        scale=2**accuracy_power # epsilon=scale**(-2)
        joint=max(v*scale**k for k,v in enumerate(a))
        separate=prod(max(v*scale**k for k,v in enumerate(block)) for block in vv)
        check(f'bit-separation-{ci}-{accuracy_power}',joint==separate)
        for bi,(block,ix) in enumerate(zip(vv,indices)):
            nodes,p=block_cases[ix];d=leja(nodes)[1][:p]
            merged=prod(max(F(1),x*scale) for x in d)
            check(f'positive-part-sum-{ci}-{accuracy_power}-{bi}-{ix}-{len(block)}',
                merged<=max(v*scale**k for k,v in enumerate(block))<=math.factorial(p)*merged)
# A falsification fixture for the tempting total-dimension-only cover.
full=[[F(1),F(9,10),F(8,10)],[F(1),F(1,100),F(1,10000)]]
correct=sorted(full[0][:1]+full[1][:2],reverse=True)
wrong=sorted(full[0]+full[1],reverse=True)[:3]
check('individual-past-cap-is-essential',prod(correct)!=prod(wrong) and prod(correct)<prod(wrong))

def schedules(counts):
    if not any(counts): yield ();return
    for b,n in enumerate(counts):
        if n:
            nxt=list(counts);nxt[b]-=1
            for tail in schedules(tuple(nxt)):yield (b,)+tail

def schedule_peak(word,tables):
    n=[0]*len(tables);peak=0
    for b in word:
        n[b]+=1;peak=max(peak,sum(table[k] for table,k in zip(tables,n)))
    return peak

# Exhaust every schedule, including nonunimodal finite-error cost tables.
for ns in [(2,2),(2,3),(3,3),(2,2,2)]:
    words=list(schedules(ns))
    for trial in range(8):
        tables=[[0]+[rng.randrange(0,13) for _ in range(n-1)]+[0] for n in ns]
        peaks=[schedule_peak(w,tables) for w in words];loc=[max(v) for v in tables]
        key='-'.join(map(str,ns))+f'-{trial}'
        check('schedule-extrema-'+key,min(peaks)==max(loc) and max(peaks)==sum(loc),schedules=len(words))
        serial=tuple(b for b,n in enumerate(ns) for _ in range(n))
        check('serial-universal-'+key,schedule_peak(serial,tables)==max(loc))
        arg=[v.index(max(v)) for v in tables]
        overlap=tuple(b for b,n in enumerate(arg) for _ in range(n))+tuple(b for b,n in enumerate(ns) for _ in range(n-arg[b]))
        check('overlap-witness-'+key,schedule_peak(overlap,tables)==sum(loc))
for B,h in product(range(1,4),range(1,4)):
    tabs=[[min(n,2*h-n) for n in range(2*h+1)] for _ in range(B)]
    serial=tuple(b for b in range(B) for _ in range(2*h))
    overlap=tuple(b for b in range(B) for _ in range(h))*2
    check(f'concurrency-dimensions-{B}-{h}',schedule_peak(serial,tabs)==h and schedule_peak(overlap,tabs)==B*h)

# Two-exponent physical blocks with exact raw integration.
def polymul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]+=a*b
    return tuple(r)
def evidence(p,shift=0,density=1):
    # density*density-coordinate**(density-1), full support on [0,1]
    return sum(a*F(density,i+shift+density) for i,a in enumerate(p))
def raw(p,m,density=1):
    ev=evidence(p,density=density)
    return tuple(evidence(p,k,density)/ev for k in range(m+1))
def update(v,f):
    den=f[0]*v[0]+f[1]*v[1]
    return tuple((f[0]*v[k]+f[1]*v[k+1])/den for k in range(len(v)-1))
def tensor(vs):
    return tuple(prod(c) for c in product(*vs))
def probe_matrix(m):
    basis=[(F(1,2),F(0)),(F(1,2),F(1,8))]
    rows=[]
    for word in product(basis,repeat=m):
        p=(F(1),)
        for f in word:p=polymul(p,f)
        rows.append(list(p)+[F(0)]*(m+1-len(p)))
    return sp.Matrix(rows)
for m1,m2 in [(0,1),(1,1),(2,1),(2,2),(3,1)]:
    gs=[probe_matrix(m1),probe_matrix(m2)]
    ls=[(g.T*g).inv()*g.T for g in gs]
    G=sp.kronecker_product(*gs);left=sp.kronecker_product(*ls)
    coord=list(product(range(m1+1),range(m2+1)))
    selection=sp.zeros(m1+m2+2,len(coord))
    for j in range(m1+1):selection[j,coord.index((j,0))]=1
    for j in range(m2+1):selection[m1+1+j,coord.index((0,j))]=1
    recovery=selection*left
    for case in range(4):
        ps=[polymul((F(1,2),F(1,12)),(F(1,2),F(case,48))),
            (F(1,2),-F(case,36))]
        vs=[raw(ps[0],m1),raw(ps[1],m2,2)]
        v=sp.Matrix(tensor(vs));q=G*v
        check(f'tensor-raw-recovery-{m1}-{m2}-{case}',recovery*q==sp.Matrix(vs[0]+vs[1]))
        # Center is generally not on a tensor posterior image. The same linear
        # recovery still acts on it, without normalizing any decoded coordinate.
        center=sp.Matrix([F((i+case)%7,7) for i in range(G.rows)])
        check(f'off-variety-center-map-{m1}-{m2}-{case}',recovery*(q-center)==sp.Matrix(vs[0]+vs[1])-recovery*center)
        direct=[]
        for row1 in gs[0].tolist():
            for row2 in gs[1].tolist():
                p1=tuple(F(x) for x in row1);p2=tuple(F(x) for x in row2)
                direct.append(evidence(polymul(ps[0],p1))/evidence(ps[0])*evidence(polymul(ps[1],p2),density=2)/evidence(ps[1],density=2))
        check(f'physical-tensor-query-{m1}-{m2}-{case}',list(q)==direct)

FACTORS=[(F(1,2),F(1,12)),(F(1,2),-F(1,12)),(F(1,6),F(1,12))]
# These are failures for lookup vectors (1/3,2/3), (2/3,1/3),
# and acceptance of cell 0 with probability 1/3, respectively.
def witness(n,seed):
    p=(F(1),)
    for k in range(n):p=polymul(p,FACTORS[(k+seed)%len(FACTORS)])
    return p

def codebooks(word,ns,M):
    counts=[0]*len(ns);books=[];witnesses=[]
    for stage in range(len(word)+1):
        choices=[list(dict.fromkeys(witness(n,k) for k in range(3))) for n in counts]
        ws=list(product(*choices))
        # Reachable but deliberately not asserted asymptotically optimal.
        picked=ws[:M]
        books.append([tuple(raw(p,N-n,b+1) for b,(p,N,n) in enumerate(zip(ps,ns,counts))) for ps in picked])
        witnesses.append(picked)
        if stage<len(word):counts[word[stage]]+=1
    return books,witnesses

def distance2(v,w):return sum((x-y)**2 for a,b in zip(v,w) for x,y in zip(a,b))
class Machine:
    __slots__=('index',)
    def __init__(self):self.index=0
    def step(self,stage,block,factor,program):
        v=list(program[stage][self.index]);v[block]=update(v[block],factor)
        self.index=min(range(len(program[stage+1])),key=lambda j:(distance2(v,program[stage+1][j]),j))

fixtures=0; raw_comparisons=0
for ns in [(2,2),(3,2)]:
    choices=list(schedules(ns))
    for wi in [0,len(choices)//2,len(choices)-1]:
        word=choices[wi]
        for M in [1,2,4]:
            books,ws=codebooks(word,ns,M);machine=Machine();exact=[(F(1),)]*2;counts=[0,0]
            fixtures+=1
            for stage,block in enumerate(word):
                f=FACTORS[(stage+wi)%len(FACTORS)];before=machine.index
                v=books[stage][before][block];nxt=update(v,f)
                counts[block]+=1
                ref=raw(polymul(ws[stage][before][block],f),ns[block]-counts[block],block+1)
                raw_comparisons+=1
                check(f'index-raw-update-{fixtures}-{stage}',nxt==ref)
                expected=list(books[stage][before]);expected[block]=ref
                j=min(range(len(books[stage+1])),key=lambda j:(distance2(expected,books[stage+1][j]),j))
                machine.step(stage,block,f,books)
                check(f'index-only-step-{fixtures}-{stage}',machine.index==j and Machine.__slots__==('index',) and 0<=machine.index<M)
                exact[block]=polymul(exact[block],f)
                true=tuple(raw(p,N-n,b+1) for b,(p,N,n) in enumerate(zip(exact,ns,counts)))
                check(f'finite-state-error-nonnegative-{fixtures}-{stage}',distance2(true,books[stage+1][machine.index])>=0)
            check(f'completed-blocks-forgotten-{fixtures}',all(v==(F(1),) for v in books[-1][machine.index]))

# Preservation is checked on exactly the files included in the principal.
main=(ROOT/'main.tex').read_text();printed='\n'.join((ROOT/(p+'.tex')).read_text() for p in re.findall(r'\\input\{([^}]+)\}',main))
meta=json.loads((ROOT/'validation/PRESERVATION.json').read_text())
labels=re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}',printed)
proofs=re.findall(r'\\begin\{proof\}(?:\[[^\]]*\])?.*?\\end\{proof\}',printed,re.S)
hashes=Counter(hashlib.sha256(p.encode()).hexdigest() for p in proofs)
check('all-42-inherited-labels',len(meta['old_result_labels'])==42 and set(meta['old_result_labels'])<=set(labels))
check('all-40-inherited-proofs',len(meta['old_proof_sha256'])==40 and not (Counter(meta['old_proof_sha256'])-hashes))
check('unique-printed-result-labels',len(labels)==len(set(labels)))
check('new-joint-theorems-present',{'thm:shared-state','thm:shared-bits','thm:schedule-extrema','thm:product-dimension'}<=set(labels))
receipt={'python':platform.python_version(),'sympy':sp.__version__,'seed':100906,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'passed_assertions':len(CHECKS),'failed_assertions':0,
 'index_only_fixtures':fixtures,'exact_raw_update_comparisons':raw_comparisons,
 'checks':CHECKS,
 'limitation':'Finite diagnostics and source-preservation checks, not a proof of the continuum theorems or a journal judgment.'}
(ROOT/'validation/V10_DIAGNOSTICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['passed_assertions','failed_assertions','index_only_fixtures','exact_raw_update_comparisons']}))
