"""Exact rational terminal and adaptive-process realization compiler (v59).

Optional scipy proposes hull facets to accelerate search; every returned row is
checked with Fraction arithmetic, and exhaustive triples are the fallback.
The output is a classical hidden-label sampler with a numerical density-matrix
decoder, NOT a quantum-state preparation algorithm. Process mode samples actual
classical probe outputs. Generic inputs are exact rational SO(3) matrices with
a rational unit seed. Allocation and input-byte limits are enforced.
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

def rational(x)->F:
    require(type(x) is int or isinstance(x,F) or isinstance(x,str),
            'rational inputs must be integers or fraction strings, never floats')
    try:return F(x)
    except (ValueError,ZeroDivisionError,TypeError) as exc:
        raise ValueError('invalid rational value') from exc

def vector(x)->Vec:
    require(isinstance(x,(tuple,list)) and len(x)==3,'a vector needs three coordinates')
    return tuple(rational(v) for v in x)

def validate_geometry(commands=None,seed=E1):
    commands=COMMANDS if commands is None else commands
    require(isinstance(commands,dict) and bool(commands),'nonempty command dictionary required')
    parsed={}
    for name,a in commands.items():
        require(isinstance(name,str) and bool(name),'command names must be nonempty strings')
        require(isinstance(a,(tuple,list)) and len(a)==3,'rotation must have three rows')
        a=tuple(vector(row) for row in a)
        require(all(dot(a[i],a[j])==int(i==j) for i in range(3) for j in range(3)),
                'rotation is not exactly orthogonal')
        require(dot(a[0],cross(a[1],a[2]))==1,'rotation determinant must be +1')
        parsed[name]=a
    seed=vector(seed)
    require(dot(seed,seed)==1,'seed must be a rational unit vector')
    return parsed,seed

def validate_probes(probes,eta,commands):
    eta=rational(eta)
    require(0<eta<=1,'a positive probability floor is required')
    require(isinstance(probes,dict) and bool(probes),'nonempty probe dictionary required')
    parsed={}
    for name,outcomes in probes.items():
        require(isinstance(name,str) and name and name not in commands,'invalid or colliding probe name')
        require(isinstance(outcomes,(list,tuple)) and bool(outcomes),'probe outcomes must be nonempty')
        values=[]
        for out in outcomes:
            require(isinstance(out,dict) and set(out)=={'bias','linear'},'invalid affine outcome fields')
            bias=rational(out['bias']);linear=vector(out['linear'])
            require(bias>=eta and (bias-eta)**2>=dot(linear,linear),
                    'probe probability floor fails on the full unit ball')
            values.append({'bias':bias,'linear':linear})
        require(sum((v['bias'] for v in values),F(0))==1,'probe biases do not sum to one')
        require(all(sum((v['linear'][d] for v in values),F(0))==0 for d in range(3)),
                'probe linear parts do not sum to zero')
        parsed[name]=values
    return parsed,eta

def supplied_input(data):
    require(isinstance(data,dict),'input must be a JSON object')
    require(set(data)<= {'schema','commands','seed','probes','eta'},'unknown input field')
    require(data.get('schema')=='gtf59.rotations/1','unsupported input schema')
    require('commands' in data and 'seed' in data,'commands and seed are required')
    commands,seed=validate_geometry(data['commands'],data['seed'])
    if 'probes' in data:
        require('eta' in data,'probes require an exact positive eta')
        probes,eta=validate_probes(data['probes'],data['eta'],commands)
    else:
        require('eta' not in data,'eta without probes is ambiguous')
        probes=eta=None
    return commands,seed,probes,eta

def weak_probes(lam=F(1,8)):
    lam=rational(lam)
    require(0<lam<1,'probe contrast must lie between zero and one')
    return {f'probe{j+1}':[{'bias':F(1,2),'linear':tuple((sgn*lam/2 if d==j else F(0)) for d in range(3))}
             for sgn in [1,-1]] for j in range(3)}

def build_rows(m,commands,seed,max_labels):
    require(type(max_labels) is int and max_labels>=1,'max_labels must be a positive integer')
    require(2+2*(2*m+1)**2<=max_labels,'declared label limit exceeded before allocating tables')
    vertices=net(m)
    if seed not in vertices:vertices.append(seed)
    r=1-F(1,m*m)
    fast=list(rowsolver(vertices,facet_candidates(vertices)))
    tables={name:[find_row(vertices,scale(r,apply(a,v)),fast) for v in vertices] for name,a in commands.items()}
    return vertices,r,tables

def compile_exact(n:int,beta:F,*,max_labels:int=20000,commands=None,seed=E1)->dict:
    require(type(n) is int and n>=0,'horizon must be a nonnegative integer')
    beta=rational(beta)
    require(0<beta<1,'amplitude must lie strictly between zero and one')
    commands,seed=validate_geometry(commands,seed)
    m=max(2,ceil_sqrt(F(n)/(1-beta)))
    vertices,r,tables=build_rows(m,commands,seed,max_labels)
    require(r**n>=beta,'amplitude enclosure failed')
    d=beta/(r**n);decoders=[scale(d,v) for v in vertices]
    require(all(dot(v,v)<=1 for v in decoders),'illegal matrix decoder')
    return {'schema':'gtf59.terminal/1','horizon':n,'amplitude':beta,'m':m,'contraction':r,'labels':len(vertices),
            'vertices':vertices,'initial_label':vertices.index(seed),'rows':tables,'commands':commands,'seed':seed,
            'decoder_bloch':decoders,'max_row_support':max(len(row) for rows in tables.values() for row in rows),
            'certificate':'every unrounded row verified by exact rational barycentric equality',
            'spectral_gap_certified':False}

def bits_for(bound:F)->int:
    b=0
    while (1<<b)<bound:b+=1
    return b

def compile_noisy(n:int,epsilon:F,*,max_labels:int=20000,commands=None,seed=E1)->dict:
    epsilon=rational(epsilon)
    require(epsilon>0 and epsilon*epsilon<F(1,2),'error must satisfy 0 < epsilon < 1/sqrt(2)')
    data=compile_exact(n,1-min(epsilon,F(1,2)),max_labels=max_labels,commands=commands,seed=seed)
    b=bits_for(F(24*(n+1))/epsilon)
    data['exact_rows']=data['rows']
    data['rows']={name:[dyadic(row,b) for row in rows] for name,rows in data['rows'].items()}
    data.update({'requested_error':epsilon,'fair_bits_per_transition':b,'total_fair_bits':n*b,
                 'error_bound':'epsilon/sqrt(2)+epsilon/4 < epsilon',
                 'sampler':'uniform b-bit integer and cumulative integer row; numerical output only'})
    return data

def compile_causal(n:int,epsilon:F,*,commands=None,seed=E1,probes=None,eta=None,max_labels:int=20000)->dict:
    require(type(n) is int and n>=0,'horizon must be a nonnegative integer')
    epsilon=rational(epsilon)
    require(0<epsilon<1,'process error must lie strictly between zero and one')
    commands,seed=validate_geometry(commands,seed)
    if probes is None:
        probes=weak_probes();eta=F(7,16)
    probes,eta=validate_probes(probes,eta,commands)
    A=max(sum((dot(v['linear'],v['linear']) for v in values),F(0)) for values in probes.values())
    C0=max(3,max(len(values)-1 for values in probes.values()))
    m=max(2,ceil_sqrt(4*A*n*n/(eta*epsilon*epsilon)))
    vertices,r,exact=build_rows(m,commands,seed,max_labels)
    b=bits_for(F(2*C0*max(1,n))/epsilon)
    emission={name:[[(y,out['bias']+dot(out['linear'],v)) for y,out in enumerate(outcomes)]
                    for v in vertices] for name,outcomes in probes.items()}
    require(all(all(p>=eta for _,p in row) and sum((p for _,p in row),F(0))==1
                for rows in emission.values() for row in rows),'illegal exact probe table')
    return {'schema':'gtf59.causal/1','horizon':n,'requested_path_tv':epsilon,'m':m,'contraction':r,
            'commands':commands,'seed':seed,'probes':probes,'eta':eta,'A':A,'C0':C0,
            'labels':len(vertices),'vertices':vertices,'initial_label':vertices.index(seed),
            'exact_rows':exact,'rows':{name:[dyadic(row,b) for row in rows] for name,rows in exact.items()},
            'exact_emissions':emission,'emissions':{name:[dyadic(row,b) for row in rows] for name,rows in emission.items()},
            'probe_state_update':'identity','fair_bits_per_control':b,'total_fair_bits':n*b,
            'max_row_support':max(len(row) for rows in exact.values() for row in rows),
            'kl_upper_bound':2*A*n*n/(eta*m*m),'rounding_path_tv_bound':F(n*C0,1<<b),
            'certificate':'exact rational common-row means, probe positivity, and dyadic normalization; full-path bound proved in manuscript',
            'sampling_scope':'classical hidden labels and classical probe outputs; not quantum preparation',
            'spectral_gap_certified':False,'universal_process_theorem_certified_by_tests':False}

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
    g.add_argument('--process-error',type=F)
    p.add_argument('--input',type=Path,help='exact rational SO(3) list, unit seed, optional affine probes')
    p.add_argument('--max-input-bytes',type=int,default=1048576)
    p.add_argument('--max-labels',type=int,default=20000)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    commands,seed,probes,eta=COMMANDS,E1,None,None
    if args.input is not None:
        require(args.max_input_bytes>0 and args.input.stat().st_size<=args.max_input_bytes,'input byte limit exceeded')
        def unique_pairs(pairs):
            obj={}
            for key,value in pairs:
                require(key not in obj,'duplicate JSON key');obj[key]=value
            return obj
        data=json.loads(args.input.read_text(encoding='utf-8'),object_pairs_hook=unique_pairs)
        commands,seed,probes,eta=supplied_input(data)
    opts={'max_labels':args.max_labels,'commands':commands,'seed':seed}
    if args.amplitude is not None:data=compile_exact(args.horizon,args.amplitude,**opts)
    elif args.error is not None:data=compile_noisy(args.horizon,args.error,**opts)
    else:
        require(args.input is None or probes is not None,'process input must supply its probe list')
        data=compile_causal(args.horizon,args.process_error,probes=probes,eta=eta,**opts)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(encode(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'success','schema':data['schema'],'labels':data['labels'],
                     'max_row_support':data['max_row_support'],'output':str(args.output)}))

if __name__=='__main__':main()
