#!/usr/bin/env python3
"""Rational coherent/preparation descriptions and preparation-centre retraction.

The output is a mathematical quantum instrument, not a physical classical
simulator. N, error, dimensions and rank bounds are public. The compressed
payload, exact encoder workspace and expanded Choi matrices are distinct.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product as tuples
from math import lcm
import json
from pathlib import Path
import sys
from choi_streaming import Instrument
from instrument_streaming import ZERO, zero, identity, mul, conj, product, adjoint, trace
from instrument_codec import pack_digits, unpack_digits
import preparation_codec as prep

SCHEMA='gtf70.coherent-preparation/1'
QSCHEMA='gtf70.quaternion-chart/1'


def rational(s: object) -> F:
    if not isinstance(s,str): raise ValueError('canonical rational string required')
    q=F(s)
    if str(q)!=s: raise ValueError('noncanonical rational')
    return q


def point(q: object, length: int) -> tuple[F,...]:
    if not isinstance(q,(list,tuple)) or len(q)!=length:
        raise ValueError('wrong sphere dimension')
    out=tuple(x if isinstance(x,F) else rational(x) for x in q)
    if sum(x*x for x in out)!=1: raise ValueError('unit vector required')
    return out


def toward(q: F) -> int:
    return (1 if q>=0 else -1)*(abs(q.numerator)//q.denominator)


def sphere_decode(anchor: int, sign: int, digits: list[int], B: int) -> tuple[F,...]:
    prep.positive(B,'grid'); ell=len(digits)
    if type(anchor) is not int or not 0<=anchor<=ell or type(sign) is not int or sign not in (-1,1):
        raise ValueError('invalid sphere chart')
    if any(type(x) is not int or abs(x)>B for x in digits): raise ValueError('invalid chart digits')
    S=sum(x*x for x in digits); den=B*B+S
    rest=[F(sign*2*B*x,den) for x in digits]
    return tuple(rest[:anchor]+[F(sign*(B*B-S),den)]+rest[anchor:])


def sphere_encode(q: tuple[F,...],B: int,projective: bool=False) -> tuple[int,int,list[int]]:
    q=point(q,len(q));prep.positive(B,'grid')
    a=max(range(len(q)),key=lambda j:abs(q[j]));sign=1 if q[a]>0 else -1
    t=[sign*q[i]/(1+abs(q[a])) for i in range(len(q)) if i!=a]
    return a,1 if projective else sign,[toward(B*x) for x in t]


def quaternion_code(q: tuple[F,...],B:int) -> dict:
    q=point(q,4);a,s,digits=sphere_encode(q,B,True)
    body=a*(2*B+1)**3+pack_digits(digits,B)
    return {'schema':QSCHEMA,'grid':B,'body_hex':format(body,'x'),
            'fixed_length_bits':(4*(2*B+1)**3-1).bit_length(),
            'one_use_squared_upper':str(F(48,B*B))}


def quaternion_decode(raw:dict)->tuple[F,...]:
    if not isinstance(raw,dict) or set(raw)!={'schema','grid','body_hex','fixed_length_bits','one_use_squared_upper'} or raw['schema']!=QSCHEMA:
        raise ValueError('invalid quaternion code')
    B=prep.positive(raw['grid'],'grid');cap=4*(2*B+1)**3;bits=(cap-1).bit_length()
    h=raw['body_hex']
    if not isinstance(h,str) or not h or len(h)>(bits+3)//4 or any(x not in '0123456789abcdef' for x in h) or (len(h)>1 and h[0]=='0'):
        raise ValueError('noncanonical chart body')
    value=int(h,16)
    if value>=cap or type(raw['fixed_length_bits']) is not int or raw['fixed_length_bits']!=bits or raw['one_use_squared_upper']!=str(F(48,B*B)):
        raise ValueError('chart metadata mismatch')
    a,body=divmod(value,(2*B+1)**3)
    return sphere_decode(a,1,unpack_digits(body,B,3),B)


def quaternion_matrix(q:tuple[F,...])->list:
    a,b,c,d=point(q,4)
    return [[(a,d),(c,b)],[(-c,b),(a,-d)]]


def unitary_check(U:list)->None:
    if not U or any(len(row)!=len(U) for row in U) or product(U,adjoint(U))!=identity(len(U)):
        raise ValueError('exact square unitary required')


def chi_squared(U:list,V:list)->F:
    unitary_check(U);unitary_check(V)
    if len(U)!=len(V):raise ValueError('unitary dimensions differ')
    W=product(adjoint(U),V); z=(sum(W[i][i][0] for i in range(len(W))),sum(W[i][i][1] for i in range(len(W))))
    return F(1)-(z[0]*z[0]+z[1]*z[1])/len(W)**2


def atlas_pairs(d:int)->list[tuple[int,int]]:
    prep.positive(d,'dimension')
    return [(j,i) for j in range(d-1) for i in range(d-1,j,-1)]


def unitary_atlas_decode(d:int,B:int,givens:list,phases:list)->list:
    """General-d rational Givens/sphere decoder of Lemma unitaryatlas70.

    Each factor is (anchor,sign,digit-list). No projection or square root.
    Factor order corresponds to successive column elimination.
    """
    pairs=atlas_pairs(d)
    if len(givens)!=len(pairs) or len(phases)!=d-1:raise ValueError('wrong atlas factor count')
    U=identity(d)
    for (i,j),data in zip(pairs,givens):
        if not isinstance(data,(list,tuple)) or len(data)!=3 or len(data[2])!=2:raise ValueError('wrong Givens chart')
        c,x,y=sphere_decode(*data,B);G=identity(d);G[i][i]=G[j][j]=(c,F(0));G[i][j]=(-x,y);G[j][i]=(x,y)
        U=product(U,G)
    D=identity(d)
    for j,data in enumerate(phases,1):
        if not isinstance(data,(list,tuple)) or len(data)!=3 or len(data[2])!=1:raise ValueError('wrong phase chart')
        x,y=sphere_decode(*data,B);D[j][j]=(x,y)
    U=product(U,D);unitary_check(U);return U


def unitary_atlas_words(d:int,B:int):
    """Finite exhaustive general encoder search space, no efficiency promise."""
    prep.positive(B,'grid');pairs=atlas_pairs(d)
    def charts(ell):
        for a in range(ell+1):
            for s in (-1,1):
                for z in tuples(range(-B,B+1),repeat=ell):yield (a,s,list(z))
    # Factor lists and intermediate search state are encoder workspace, not payload.
    g=list(charts(2));p=list(charts(1))
    for gs in tuples(g,repeat=len(pairs)):
        for ps in tuples(p,repeat=d-1):yield {'givens':list(gs),'phases':list(ps)}


def unitary_atlas_encode(U:list,B:int,squared_radius:F,max_candidates:int|None=None)->dict:
    """Return the first exact certified word; a finite search cap may be inconclusive.

    Without a cap the finite list is exhausted. Guaranteed coverage requires the
    radius in Lemma unitaryatlas70; a smaller radius is allowed but may fail.
    """
    unitary_check(U)
    if not isinstance(squared_radius,F) or squared_radius<0:raise ValueError('nonnegative rational radius required')
    if max_candidates is not None:prep.positive(max_candidates,'search cap')
    for count,word in enumerate(unitary_atlas_words(len(U),B),1):
        V=unitary_atlas_decode(len(U),B,word['givens'],word['phases'])
        if chi_squared(U,V)<=squared_radius:return word
        if max_candidates is not None and count>=max_candidates:
            raise RuntimeError('inconclusive: declared finite search cap reached')
    raise ValueError('no centre at the requested radius in this finite codebook')


def instrument_from_fraction_blocks(d:int,n:int,mats:list)->Instrument:
    den=1
    for A in mats:
        for row in A:
            for z in row:
                for c in z:den=lcm(den,F(c).denominator)
    ints=[[[(int(F(x)*den),int(F(y)*den)) for x,y in row] for row in A] for A in mats]
    out=Instrument(d,n,den,ints);out.validate();return out


def retract(target:Instrument)->Instrument:
    """Idempotent legal preparation-centre map; deliberately not rank preserving."""
    target.validate();d,n=target.d,target.n;blocks=[]
    for A in target.outcomes:
        block=zero(n)
        for a in range(n):
            for b in range(n):block[a][b]=tuple(sum(A[i*n+a][i*n+b][c] for i in range(d)) for c in (0,1))
        blocks.append(block)
    return prep.lift_blocks(blocks,d,n,d*target.denominator)


def tensor_instrument(U:list,preparation:Instrument)->Instrument:
    """Input-first Choi for X -> U X U* tensor sigma_y; never a Kraus oracle."""
    unitary_check(U);blocks=prep.preparation_blocks(preparation);d,n=len(U),preparation.n
    mats=[]
    for block in blocks:
        A=zero(d*d*n)
        for i,a,k,j,b,l in tuples(range(d),range(d),range(n),range(d),range(d),range(n)):
            z=mul(mul(U[a][i],conj(U[b][j])),block[k][l])
            A[i*(d*n)+a*n+k][j*(d*n)+b*n+l]=tuple(F(x,preparation.denominator) for x in z)
        mats.append(A)
    return instrument_from_fraction_blocks(d,d*n,mats)


def encode(q:tuple[F,...],target:Instrument,N:int,error:F,ranks:list[int])->dict:
    q=point(q,4);prep.positive(N,'horizon')
    if not isinstance(error,F) or not 0<error<=F(1,32):raise ValueError('error must be rational in (0,1/32]')
    B= (16*N*error.denominator+error.numerator-1)//error.numerator
    unit=quaternion_code(q,B);state=prep.adaptive(target,N,error/2,ranks)
    unit_sq=F(48*N*N,B*B);prep_sq=F(state['error_squared_upper']);total_sq=2*(unit_sq+prep_sq)
    if unit_sq>error*error/4 or prep_sq>error*error/4 or total_sq>error*error:raise RuntimeError('construction budget failed')
    return {'schema':SCHEMA,'horizon':N,'requested_unhalved_error':str(error),
            'unitary':unit,'preparation':state,
            'coherent_error_squared_upper':str(unit_sq),'preparation_error_squared_upper':str(prep_sq),
            'total_error_squared_upper':str(total_sq),
            'fixed_length_bits':unit['fixed_length_bits']+state['code']['fixed_length_bits'],
            'scope':'Reusable mathematical instrument description. Public N,error,dimensions,ranks are not payload; encoder workspace and expanded Choi output are separate. Not a physical classical simulator.'}


def decode(raw:dict)->Instrument:
    keys={'schema','horizon','requested_unhalved_error','unitary','preparation','coherent_error_squared_upper','preparation_error_squared_upper','total_error_squared_upper','fixed_length_bits','scope'}
    if not isinstance(raw,dict) or set(raw)!=keys or raw['schema']!=SCHEMA:raise ValueError('invalid coherent code schema')
    N=prep.positive(raw['horizon'],'horizon');error=rational(raw['requested_unhalved_error'])
    if not 0<error<=F(1,32):raise ValueError('unsupported error range')
    q=quaternion_decode(raw['unitary']);state=prep.validate_adaptive(raw['preparation'])
    if raw['preparation']['horizon']!=N or raw['preparation']['requested_unhalved_error']!=str(error/2):raise ValueError('preparation budget mismatch')
    us=F(48*N*N,raw['unitary']['grid']**2);ps=F(raw['preparation']['error_squared_upper']);ts=2*(us+ps)
    if us>error*error/4 or ps>error*error/4 or ts>error*error:raise ValueError('error certificate exceeds tolerance')
    for key,qv in [('coherent_error_squared_upper',us),('preparation_error_squared_upper',ps),('total_error_squared_upper',ts)]:
        if raw[key]!=str(qv):raise ValueError('altered error certificate')
    bits=raw['unitary']['fixed_length_bits']+raw['preparation']['code']['fixed_length_bits']
    if type(raw['fixed_length_bits']) is not int or raw['fixed_length_bits']!=bits:raise ValueError('payload length mismatch')
    return tensor_instrument(quaternion_matrix(q),state)


def verify(q:tuple[F,...],target:Instrument,raw:dict)->bool:
    try:
        decode(raw)
        expected=encode(q,target,raw['horizon'],rational(raw['requested_unhalved_error']),raw['preparation']['code']['rank_bounds'])
        return json.dumps(raw,sort_keys=True)==json.dumps(expected,sort_keys=True)
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,AttributeError):return False


def main():
    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='mode',required=True)
    for name in ['encode','decode','verify','retract']:
        p=sp.add_parser(name);p.add_argument('--input',type=Path,required=True)
        if name in ['encode','verify']:p.add_argument('--quaternion',required=True,help='JSON array of four canonical rational strings')
        if name=='encode':
            p.add_argument('--horizon',type=int,required=True);p.add_argument('--error',required=True);p.add_argument('--ranks',required=True,help='JSON list')
        if name=='verify':p.add_argument('--certificate',type=Path,required=True)
    a=ap.parse_args()
    try:
        raw=json.loads(a.input.read_text())
        if a.mode=='decode':out=decode(raw).to_dict()
        else:
            target=Instrument.from_dict(raw)
            if a.mode=='retract':out=retract(target).to_dict()
            elif a.mode=='encode':out=encode(point(json.loads(a.quaternion),4),target,a.horizon,rational(a.error),json.loads(a.ranks))
            else:
                if not verify(point(json.loads(a.quaternion),4),target,json.loads(a.certificate.read_text())):raise ValueError('target-bound replay failed')
                out={'status':'success','scope':'Exact target-bound encoder replay, not universal proof or priority certification.'}
        print(json.dumps(out,indent=2,sort_keys=True))
    except (OSError,ValueError,TypeError,KeyError,IndexError,ZeroDivisionError) as exc:
        print('coherent codec: '+str(exc),file=sys.stderr);raise SystemExit(2)
if __name__=='__main__':main()
