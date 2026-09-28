"""Exact rational qubit realization compiler (v58).

Optional scipy proposes hull facets to accelerate search; every returned row is
checked with Fraction arithmetic, and exhaustive triples are the fallback.
The output is a classical hidden-label sampler with a numerical density-matrix
decoder, NOT a quantum-state preparation algorithm. A size limit is enforced.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path
from typing import Iterable

Vec=tuple[F,F,F]
Mat=tuple[Vec,Vec,Vec]
ZERO=(F(0),F(0),F(0))
E1=(F(1),F(0),F(0))
I:Mat=((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1)))
U:Mat=((F(-7,25),F(-24,25),F(0)),(F(24,25),F(-7,25),F(0)),(F(0),F(0),F(1)))
V:Mat=((F(-7,25),F(0),F(24,25)),(F(0),F(1),F(0)),(F(-24,25),F(0),F(-7,25)))

def require(ok:bool,message:str)->None:
    if not ok:raise ValueError(message)

def transpose(a:Mat)->Mat:return tuple(tuple(a[j][i] for j in range(3)) for i in range(3))
COMMANDS={'I':I,'U':U,'U*':transpose(U),'V':V,'V*':transpose(V)}
def dot(a:Vec,b:Vec)->F:return sum((x*y for x,y in zip(a,b)),F(0))
def cross(a:Vec,b:Vec)->Vec:return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def apply(a:Mat,v:Vec)->Vec:return tuple(dot(row,v) for row in a)
def scale(a:F,v:Vec)->Vec:return tuple(a*x for x in v)
def net(m:int)->list[Vec]:
    require(isinstance(m,int) and m>=2,'m must be an integer at least two')
    points={ZERO}
    for j in range(-m,m+1):
        for l in range(-m,m+1):
            den=m*m+j*j+l*l
            for s in [-1,1]:points.add((F(s*2*j*m,den),F(s*2*l*m,den),F(s*(m*m-j*j-l*l),den)))
    return [ZERO]+sorted(points-{ZERO})

def ceil_sqrt(x:F)->int:
    require(x>=0,'negative square root')
    k=math.isqrt(x.numerator//x.denominator)
    return k if k*k>=x else k+1

def facet_candidates(vertices:list[Vec])->list[tuple[int,int,int]]:
    try:
        from scipy.spatial import ConvexHull
        hull=ConvexHull([[float(x) for x in v] for v in vertices[1:]])
        return sorted(set(tuple(sorted(int(i)+1 for i in face)) for face in hull.simplices))
    except (ImportError,ValueError,RuntimeError):return []

def rowsolver(vertices:list[Vec],triples:Iterable[tuple[int,int,int]]):
    for ids in triples:
        a,b,c=(vertices[i] for i in ids)
        dual=(cross(b,c),cross(c,a),cross(a,b))
        det=dot(a,dual[0])
        if det:yield ids,tuple(scale(1/det,v) for v in dual)

def valid_row(vertices:list[Vec],row:list[tuple[int,F]],target:Vec)->bool:
    if not row or len(row)>4 or len({i for i,_ in row})!=len(row):return False
    if any(i<0 or i>=len(vertices) or p<0 for i,p in row):return False
    if sum((p for _,p in row),F(0))!=1:return False
    return all(sum((p*vertices[i][d] for i,p in row),F(0))==target[d] for d in range(3))

def find_row(vertices:list[Vec],target:Vec,fast)->list[tuple[int,F]]:
    if target==ZERO:return [(0,F(1))]
    for source in (fast,rowsolver(vertices,combinations(range(1,len(vertices)),3))):
        for ids,dual in source:
            weights=tuple(dot(v,target) for v in dual)
            if min(weights)<0 or sum(weights)>1:continue
            row=[(i,p) for i,p in zip(ids,weights) if p]
            if sum(weights)<1:row.append((0,1-sum(weights)))
            require(valid_row(vertices,row,target),'internal rational row verification failed')
            return row
    raise RuntimeError('no certified row; hull theorem or input assumptions violated')

def dyadic(row:list[tuple[int,F]],b:int)->list[tuple[int,F]]:
    require(b>=0,'negative precision')
    den=1<<b
    nums=[(p.numerator*den)//p.denominator for _,p in row[:-1]]
    nums.append(den-sum(nums))
    return [(i,F(n,den)) for (i,_),n in zip(row,nums) if n]

def compile_exact(n:int,beta:F,*,max_labels:int=20000)->dict:
    require(isinstance(n,int) and n>=0,'horizon must be a nonnegative integer')
    require(0<beta<1,'amplitude must lie strictly between zero and one')
    m=max(2,ceil_sqrt(F(n)/(1-beta)))
    require(1+2*(2*m+1)**2<=max_labels,'declared label limit exceeded before allocating tables')
    vertices=net(m);r=1-F(1,m*m)
    require(r**n>=beta,'amplitude enclosure failed')
    fast=list(rowsolver(vertices,facet_candidates(vertices)))
    tables={name:[find_row(vertices,scale(r,apply(a,v)),fast) for v in vertices] for name,a in COMMANDS.items()}
    d=beta/(r**n)
    decoders=[scale(d,v) for v in vertices]
    require(all(dot(v,v)<=1 for v in decoders),'illegal matrix decoder')
    return {'horizon':n,'amplitude':beta,'m':m,'contraction':r,'labels':len(vertices),
            'vertices':vertices,'initial_label':vertices.index(E1),'rows':tables,
            'decoder_bloch':decoders,'max_row_support':max(len(row) for rows in tables.values() for row in rows),
            'certificate':'every unrounded row verified by exact rational barycentric equality',
            'spectral_gap_certified':False}

def compile_noisy(n:int,epsilon:F,*,max_labels:int=20000)->dict:
    require(epsilon>0 and epsilon*epsilon<F(1,2),'error must satisfy 0 < epsilon < 1/sqrt(2)')
    data=compile_exact(n,1-min(epsilon,F(1,2)),max_labels=max_labels)
    bound=F(24*(n+1))/epsilon;b=0
    while (1<<b)<bound:b+=1
    data['exact_rows']=data['rows']
    data['rows']={name:[dyadic(row,b) for row in rows] for name,rows in data['rows'].items()}
    data.update({'requested_error':epsilon,'fair_bits_per_transition':b,'total_fair_bits':n*b,
                 'error_bound':'epsilon/sqrt(2)+epsilon/4 < epsilon',
                 'sampler':'uniform b-bit integer and cumulative integer row; numerical output only'})
    return data

def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--horizon',type=int,required=True)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--amplitude',type=F);g.add_argument('--error',type=F)
    p.add_argument('--max-labels',type=int,default=20000)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    data=compile_exact(args.horizon,args.amplitude,max_labels=args.max_labels) if args.amplitude is not None else compile_noisy(args.horizon,args.error,max_labels=args.max_labels)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(encode(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'success','labels':data['labels'],'max_row_support':data['max_row_support'],'output':str(args.output)}))

if __name__=='__main__':main()
