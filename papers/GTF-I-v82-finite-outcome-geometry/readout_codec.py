#!/usr/bin/env python3
"""Exact rational codec for observable varying-readout instruments.

Inputs are ordered rank-one rational projections and normalized conditional
row states. Pivoted LU chooses a bounded flag chart without square roots.
The payload does not include public dimensions/ranks/horizon/error or expanded
Choi matrices. No claim about learning, programme hardware or optimal workspace.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import factorial, gcd, lcm
from pathlib import Path
import sys
from choi_streaming import Instrument, decode_matrix
import preparation_codec as prep
from conditional_codec import canonical_fraction, ceil_sqrt, rank_data

SCHEMA = 'gtf72.observable-readout-code/1'
TARGET = 'gtf72.readout-target/1'
Z = (F(0), F(0))
ONE = (F(1), F(0))


def ga(a, b): return (a[0]+b[0], a[1]+b[1])
def gn(a): return (-a[0], -a[1])
def gc(a): return (a[0], -a[1])
def gm(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def gs(a, b): return ga(a, gn(b))
def abs2(a): return a[0]*a[0]+a[1]*a[1]
def gd(a, b):
    q = abs2(b)
    if not q: raise ValueError('zero complex divisor')
    c = gm(a, gc(b)); return (c[0]/q, c[1]/q)
def gz(n, m=None): return [[Z for _ in range(n if m is None else m)] for _ in range(n)]
def gi(n): return [[ONE if i == j else Z for j in range(n)] for i in range(n)]
def adj(a): return [[gc(a[i][j]) for i in range(len(a))] for j in range(len(a[0]))]
def mm(a, b):
    return [[sumg(gm(a[i][k], b[k][j]) for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def sumg(seq):
    a = Z
    for v in seq: a = ga(a, v)
    return a

def inner(a, b): return sumg(gm(gc(x), y) for x, y in zip(a, b))
def frob2(a, b):
    return sum(abs2(gs(a[i][j], b[i][j])) for i in range(len(a)) for j in range(len(a[0])))
def round0(q: F) -> int:
    return (1 if q >= 0 else -1)*(abs(q.numerator)//q.denominator)
def ceilq(q: F) -> int: return -(-q.numerator//q.denominator)
def bits_for_count(n: int) -> int: return (n-1).bit_length()


def integer_matrices(mats):
    """Common denominator, reduced jointly; no rounded or float conversion."""
    den = 1
    for mat in mats:
        for row in mat:
            for z in row:
                for t in z: den = lcm(den, F(t).denominator)
    out = [[[(int(F(z[0])*den), int(F(z[1])*den)) for z in row] for row in a] for a in mats]
    g = den
    for a in out:
        for row in a:
            for z in row:
                for t in z: g = gcd(g, abs(t))
    return den//g, [[[(z[0]//g,z[1]//g) for z in row] for row in a] for a in out]


def flag_from_dict(raw):
    if not isinstance(raw, dict) or set(raw) != {'denominator','projectors'}:
        raise ValueError('flag must contain exactly denominator and projectors')
    den = prep.positive(raw['denominator'], 'flag denominator')
    mats = raw['projectors']
    if not isinstance(mats, list) or not mats: raise ValueError('empty flag')
    d = len(mats)
    out = []
    for a in mats:
        integers = decode_matrix(a, d)
        out.append([[(F(x,den),F(y,den)) for x,y in row] for row in integers])
    validate_flag(out)
    return out


def flag_to_dict(P):
    validate_flag(P)
    den, mats = integer_matrices(P)
    return {'denominator':den, 'projectors':[[[list(z) for z in row] for row in a] for a in mats]}


def validate_flag(P):
    d = len(P)
    if d < 1: raise ValueError('empty flag')
    total = gz(d)
    for x, a in enumerate(P):
        if len(a) != d or any(len(row) != d for row in a): raise ValueError('flag shape')
        if adj(a) != a or mm(a,a) != a: raise ValueError('flag is not an orthogonal projection')
        if sumg(a[i][i] for i in range(d)) != ONE: raise ValueError('projection is not rank one')
        for prev in P[:x]:
            if mm(a,prev) != gz(d): raise ValueError('nonorthogonal flag outcomes')
        total = [[ga(total[i][j],a[i][j]) for j in range(d)] for i in range(d)]
    if total != gi(d): raise ValueError('flag does not resolve identity')


def target_from_dict(raw):
    if not isinstance(raw, dict) or set(raw) != {'schema','flag','rows'} or raw['schema'] != TARGET:
        raise ValueError('invalid readout target schema')
    P = flag_from_dict(raw['flag'])
    rr = raw['rows']
    if not isinstance(rr, list) or len(rr) != len(P): raise ValueError('one state row per projection required')
    rr = [Instrument.from_dict(a) for a in rr]
    n,m = rr[0].n,len(rr[0].outcomes)
    if any(a.d != 1 or a.n != n or len(a.outcomes) != m for a in rr):
        raise ValueError('conditional row interface mismatch')
    return P,rr


def target_to_dict(P,rr):
    out = {'schema':TARGET, 'flag':flag_to_dict(P), 'rows':[a.to_dict() for a in rr]}
    target_from_dict(out)
    return out


def flag_chart(P):
    """Canonical partial-pivot LU of rational unnormalized projection columns."""
    validate_flag(P); d=len(P)
    cols=[]
    for a in P:
        k=next(i for i in range(d) if a[i][i][0] > 0)
        cols.append([a[i][k] for i in range(d)])
    U=[[cols[j][i] for j in range(d)] for i in range(d)]
    L=gi(d); perm=list(range(d))
    for j in range(d):
        p=max(range(j,d), key=lambda i:abs2(U[i][j]))
        if abs2(U[p][j]) == 0: raise ValueError('singular ordered projection columns')
        U[j],U[p]=U[p],U[j];perm[j],perm[p]=perm[p],perm[j]
        for k in range(j):L[j][k],L[p][k]=L[p][k],L[j][k]
        for i in range(j+1,d):
            a=gd(U[i][j],U[j][j]); L[i][j]=a
            if abs2(a)>1: raise ArithmeticError('partial-pivot bound failed')
            for k in range(j,d): U[i][k]=gs(U[i][k],gm(a,U[j][k]))
    return perm,L


def flag_from_chart(perm,L):
    """Unnormalized Gram--Schmidt gives rational rank-one projection differences."""
    d=len(L)
    if sorted(perm)!=list(range(d)) or len(perm)!=d: raise ValueError('invalid permutation')
    if any(L[i][j] != (ONE if i==j else Z) for i in range(d) for j in range(i,d)):
        raise ValueError('chart is not unit lower triangular')
    basis=[]; out=[]
    for j in range(d):
        v=[L[i][j] for i in range(d)]
        for u in basis:
            a=gd(inner(u,v),inner(u,u));v=[gs(z,gm(a,w)) for z,w in zip(v,u)]
        norm=inner(v,v)
        if norm[1] or norm[0]<=0: raise ValueError('invalid chart Gram residual')
        basis.append(v)
        P=gz(d)
        for i in range(d):
            for k in range(d):P[perm[i]][perm[k]]=gd(gm(v[i],gc(v[k])),norm)
        out.append(P)
    validate_flag(out);return out


def flag_constant(d): return 4*d*d*(2*d)**(d-1)


def flag_encode(P,B):
    prep.positive(B,'flag grid');perm,L=flag_chart(P);d=len(P)
    digits=[round0(t*B) for i in range(d) for j in range(i) for t in L[i][j]]
    return {'grid':B, 'permutation':perm, 'digits':digits}


def flag_decode(raw,d):
    if not isinstance(raw,dict) or set(raw)!={'grid','permutation','digits'}:raise ValueError('invalid flag word')
    B=prep.positive(raw['grid'],'flag grid');perm=raw['permutation'];digits=raw['digits']
    if (not isinstance(perm,list) or len(perm)!=d or any(type(x) is not int for x in perm)
        or sorted(perm)!=list(range(d))):raise ValueError('invalid flag permutation')
    if (not isinstance(digits,list) or len(digits)!=d*(d-1)
        or any(type(t) is not int or abs(t)>B for t in digits)):raise ValueError('invalid flag digits')
    L=gi(d);k=0
    for i in range(d):
        for j in range(i):L[i][j]=(F(digits[k],B),F(digits[k+1],B));k+=2
    return flag_from_chart(perm,L)


def assemble(P,rr, retain_readout=True, orthogonal_output=False):
    """Input-first Choi: P_x^T tensor sigma_xy. Optional public output embeddings."""
    d=len(P);n=rr[0].n;m=len(rr[0].outcomes)
    target_from_dict(target_to_dict(P,rr))
    out_n=d*n if orthogonal_output else n
    count=d*m if retain_readout else m
    mats=[gz(d*out_n) for _ in range(count)]
    for x,(px,a) in enumerate(zip(P,rr)):
        for y,sig in enumerate(a.outcomes):
            idx=x*m+y if retain_readout else y
            for i in range(d):
                for j in range(d):
                    for k in range(n):
                        for ell in range(n):
                            u=i*out_n+(x*n if orthogonal_output else 0)+k
                            v=j*out_n+(x*n if orthogonal_output else 0)+ell
                            val=gm(px[j][i],(F(sig[k][ell][0],a.denominator),F(sig[k][ell][1],a.denominator)))
                            mats[idx][u][v]=ga(mats[idx][u][v],val)
    den,ints=integer_matrices(mats);a=Instrument(d,out_n,den,ints);a.validate();return a


def grids(d,V,N,error):
    prep.positive(N,'horizon')
    if not isinstance(error,F) or not 0<error<2:raise ValueError('error must be rational in (0,2)')
    bf=1 if d==1 else max(1,ceilq(F(2*flag_constant(d)*N)/error))
    bs=max(1,ceil_sqrt(F(64*N*V)/error**2))
    return bf,bs


def encode(target,N,error,ranks=None):
    P,rr=target_from_dict(target);d=len(P);n=rr[0].n;m=len(rr[0].outcomes)
    ranks=rank_data([[n]*m for _ in range(d)] if ranks is None else ranks,d,n,m)
    V=sum(prep.rank_dimension(n,r) for r in ranks);bf,bs=grids(d,V,N,error)
    fw=flag_encode(P,bf);rows=[prep.encode(a,bs,r) for a,r in zip(rr,ranks)]
    loss=sum(c['factor_coordinates']-1 for c in rows)
    bits=bits_for_count(factorial(d))+d*(d-1)*bits_for_count(2*bf+1)+sum(c['fixed_length_bits'] for c in rows)
    out={'schema':SCHEMA,'input_dimension':d,'output_dimension':n,'outcomes_per_row':m,
         'horizon':N,'requested_unhalved_error':str(error),'rank_bounds':ranks,
         'flag_dimension':d*(d-1),'row_dimension':V,'flag':fw,'row_grid':bs,'rows':rows,
         'fixed_length_bits':bits,'basis_error_upper':str(F(0) if d==1 else F(flag_constant(d)*N,bf)),
         'row_error_squared_upper':str(F(16*N*loss,bs*bs)),
         'scope':'Supplied observable-readout description. Fixed public headers are not payload; permutation, flag digits and row factor words are charged. Expanded Choi matrices, workspace, learning and quantum hardware are separate.'}
    decode_parts(out);return out


def decode_parts(raw):
    keys={'schema','input_dimension','output_dimension','outcomes_per_row','horizon','requested_unhalved_error','rank_bounds','flag_dimension','row_dimension','flag','row_grid','rows','fixed_length_bits','basis_error_upper','row_error_squared_upper','scope'}
    if not isinstance(raw,dict) or set(raw)!=keys or raw['schema']!=SCHEMA:raise ValueError('invalid readout code schema or fields')
    d=prep.positive(raw['input_dimension'],'input dimension');n=prep.positive(raw['output_dimension'],'output dimension')
    m=prep.positive(raw['outcomes_per_row'],'outcomes per row');N=prep.positive(raw['horizon'],'horizon')
    error=canonical_fraction(raw['requested_unhalved_error'],'requested error')
    ranks=rank_data(raw['rank_bounds'],d,n,m);V=sum(prep.rank_dimension(n,r) for r in ranks)
    bf,bs=grids(d,V,N,error)
    for name,v in [('flag_dimension',d*(d-1)),('row_dimension',V),('row_grid',bs)]:
        if type(raw[name]) is not int or raw[name]!=v:raise ValueError(name+' mismatch')
    P=flag_decode(raw['flag'],d)
    if raw['flag']['grid']!=bf:raise ValueError('flag grid mismatch')
    codes=raw['rows']
    if not isinstance(codes,list) or len(codes)!=d:raise ValueError('row count mismatch')
    rr=[]
    for c,r in zip(codes,ranks):
        a=prep.decode(c)
        if a.d!=1 or a.n!=n or len(a.outcomes)!=m or c['grid']!=bs or c['rank_bounds']!=r:
            raise ValueError('row/public interface mismatch')
        rr.append(a)
    bits=bits_for_count(factorial(d))+d*(d-1)*bits_for_count(2*bf+1)+sum(c['fixed_length_bits'] for c in codes)
    if type(raw['fixed_length_bits']) is not int or raw['fixed_length_bits']!=bits:raise ValueError('payload mismatch')
    be=F(0) if d==1 else F(flag_constant(d)*N,bf)
    re=F(16*N*sum(c['factor_coordinates']-1 for c in codes),bs*bs)
    if canonical_fraction(raw['basis_error_upper'],'basis certificate')!=be or canonical_fraction(raw['row_error_squared_upper'],'row certificate')!=re:
        raise ValueError('error certificate mismatch')
    if be>error/2 or re>(error/2)**2:raise ValueError('insufficient error budget')
    return P,rr


def decode(raw): return assemble(*decode_parts(raw))


def verify(target,raw):
    decode_parts(raw)
    expected=encode(target,raw['horizon'],F(raw['requested_unhalved_error']),raw['rank_bounds'])
    if json.dumps(expected,sort_keys=True)!=json.dumps(raw,sort_keys=True):raise ValueError('not canonical target-bound encoding')
    return True


PAULI=[[[ONE,Z],[Z,ONE]],[[Z,ONE],[ONE,Z]],[[Z,(F(0),F(-1))],[(F(0),F(1)),Z]],[[ONE,Z],[Z,gn(ONE)]]]


def pauli_channel(p):
    if len(p)!=4 or any(not isinstance(x,F) or x<0 for x in p) or sum(p)!=1:raise ValueError('Pauli probabilities')
    J=gz(4)
    for prob,U in zip(p,PAULI):
        vec=[U[k][i] for i in range(2) for k in range(2)]
        for i in range(4):
            for j in range(4):J[i][j]=ga(J[i][j],gm((prob,F(0)),gm(vec[i],gc(vec[j]))))
    den,mats=integer_matrices([J]);a=Instrument(2,2,den,mats);a.validate();return a


def seize_pauli(a):
    a.validate()
    if a.d!=2 or a.n!=2 or len(a.outcomes)!=1:raise ValueError('qubit channel required')
    J=[[(F(x,a.denominator),F(y,a.denominator)) for x,y in row] for row in a.outcomes[0]]
    p=[]
    for U in PAULI:
        vec=[U[k][i] for i in range(2) for k in range(2)]
        val=sumg(gm(gc(vec[i]),gm(J[i][j],vec[j])) for i in range(4) for j in range(4))
        if val[1]!=0 or val[0]<0:raise ArithmeticError('Bell probability invalid')
        p.append(val[0]/4)
    if sum(p)!=1:raise ArithmeticError('Bell normalization invalid')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for command in ['encode','decode','verify','assemble']:
        a=sub.add_parser(command);a.add_argument('--input',required=True)
        if command=='encode':
            a.add_argument('--horizon',type=int,required=True);a.add_argument('--error',required=True);a.add_argument('--ranks')
        if command=='verify':a.add_argument('--certificate',required=True)
    a=parser.parse_args()
    try:
        raw=json.loads(Path(a.input).read_text())
        if a.command=='encode':out=encode(raw,a.horizon,F(a.error),None if a.ranks is None else json.loads(a.ranks))
        elif a.command=='decode':out=decode(raw).to_dict()
        elif a.command=='assemble':out=assemble(*target_from_dict(raw)).to_dict()
        else:
            cert=json.loads(Path(a.certificate).read_text());verify(raw,cert)
            out={'schema':'gtf72.readout-verification/1','status':'success','target_bound':True}
        print(json.dumps(out,indent=2,sort_keys=True));return 0
    except (ValueError,TypeError,KeyError,OSError,ZeroDivisionError,ArithmeticError,StopIteration) as exc:
        print('readout codec: '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
