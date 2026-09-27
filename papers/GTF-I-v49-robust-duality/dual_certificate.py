"""Exact threshold certificates for bounded rank-one word tensors.

All decisions use rational products, never numerical logarithms or LP tolerances.
The general algorithm can be exponential. Resource limits raise ResourceLimit;
they NEVER turn an unfinished search into an infeasibility conclusion.
Input: a complete positive-seed mean tensor (the negative seeds are its negative).
Run `python dual_certificate.py --help` for the JSON interface.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from functools import reduce
from itertools import product
from math import gcd, lcm
from pathlib import Path
import json
from typing import Iterable

class ResourceLimit(RuntimeError):
    pass

@dataclass(frozen=True)
class LogValue:
    """An exact rational linear combination of logarithms of positive rationals."""
    terms: tuple[tuple[F, F], ...] = ()

    @classmethod
    def base(cls, value: F) -> 'LogValue':
        value = F(value)
        if value <= 0:
            raise ValueError('A logarithmic base must be strictly positive')
        return cls(()) if value == 1 else cls(((value, F(1)),))

    def __add__(self, other: 'LogValue') -> 'LogValue':
        d = dict(self.terms)
        for b, q in other.terms:
            d[b] = d.get(b, F(0)) + q
        return LogValue(tuple(sorted((b, q) for b, q in d.items() if q)))

    def scale(self, q: F) -> 'LogValue':
        q = F(q)
        return LogValue(tuple((b, e*q) for b, e in self.terms if e*q))

    def __sub__(self, other: 'LogValue') -> 'LogValue':
        return self + other.scale(-1)

    def sign(self, power_limit: int = 1000000) -> int:
        denominator = lcm(*(q.denominator for _, q in self.terms)) if self.terms else 1
        exponents = [(b, int(q*denominator)) for b, q in self.terms]
        if sum(abs(e) for _, e in exponents) > power_limit:
            raise ResourceLimit('Exact rational-product exponent budget exhausted')
        value = F(1)
        for b, e in exponents:
            value *= b**e
        return (value > 1) - (value < 1)

    def le(self, other: 'LogValue') -> bool:
        return (self-other).sign() <= 0

    def dump(self) -> list[list[str]]:
        return [[str(b), str(e)] for b, e in self.terms]

    @classmethod
    def load(cls, data) -> 'LogValue':
        out = cls()
        for b, e in data:
            out = out + cls.base(F(b)).scale(F(e))
        return out

@dataclass(frozen=True)
class Row:
    c: tuple[F, ...]
    rhs: LogValue
    dual: tuple[F, ...]

    def scaled(self, q: F) -> 'Row':
        if q <= 0:
            raise ValueError('An inequality may only be scaled by a positive number')
        return Row(tuple(q*x for x in self.c), self.rhs.scale(q), tuple(q*x for x in self.dual))

    def plus(self, other: 'Row') -> 'Row':
        return Row(tuple(a+b for a,b in zip(self.c, other.c)), self.rhs+other.rhs,
                   tuple(a+b for a,b in zip(self.dual,other.dual)))


def fm_solve(coefficients: list[list[int]], bases: list[F], max_rows=50000):
    """Fourier--Motzkin with a recoverable feasible point or Farkas multipliers."""
    if not coefficients or len(coefficients) != len(bases):
        raise ValueError('Invalid linear system')
    n = len(coefficients[0]); r = len(bases)
    original = [Row(tuple(map(F,c)), LogValue.base(b),
                    tuple(F(i==j) for j in range(r)))
                for i,(c,b) in enumerate(zip(coefficients,bases))]
    rows = original
    stages = []
    remaining = set(range(n))
    while True:
        reduced = {}
        for row in rows:
            pivot = next((x for x in row.c if x), None)
            if pivot is None:
                if row.rhs.sign() < 0:
                    den = lcm(*(z.denominator for z in row.dual))
                    z = [int(q*den) for q in row.dual]
                    div = reduce(gcd, z)
                    z = [q//div for q in z]
                    return {'feasible':False, 'multipliers':z}
                continue
            row = row.scaled(1/abs(pivot))
            incumbent = reduced.get(row.c)
            if incumbent is None or row.rhs.le(incumbent.rhs):
                reduced[row.c] = row
        rows = list(reduced.values())
        if not remaining:
            break
        if len(rows) > max_rows:
            raise ResourceLimit('Fourier--Motzkin row budget exhausted')
        # Preserve exact equality pairs before ordinary elimination.  This is
        # Gaussian substitution implemented only by nonnegative combinations
        # of the two opposing inequalities, so the Farkas multipliers remain
        # valid.  It avoids needless blow-up at exact rank-one boundaries.
        equality = None
        for row in rows:
            opposite = reduced.get(tuple(-c for c in row.c))
            if opposite is not None and (row.rhs+opposite.rhs).sign() == 0:
                equality = (row, opposite)
                break
        if equality is not None:
            a,b = equality
            j = next(j for j in sorted(remaining) if a.c[j])
            stages.append((j, rows))
            substituted = []
            for row in rows:
                if not row.c[j]:
                    substituted.append(row)
                else:
                    cancel = a if a.c[j]*row.c[j] < 0 else b
                    substituted.append(row.plus(cancel.scaled(-row.c[j]/cancel.c[j])))
            rows = substituted
            remaining.remove(j)
            continue
        def score(j):
            pos = sum(row.c[j] > 0 for row in rows)
            neg = sum(row.c[j] < 0 for row in rows)
            return pos*neg, j
        j = min(remaining, key=score)
        stages.append((j, rows))
        pos = [row for row in rows if row.c[j] > 0]
        neg = [row for row in rows if row.c[j] < 0]
        zero = [row for row in rows if row.c[j] == 0]
        if len(pos)*len(neg)+len(zero) > max_rows:
            raise ResourceLimit('Fourier--Motzkin generated-row budget exhausted')
        rows = zero + [a.scaled(1/a.c[j]).plus(b.scaled(-1/b.c[j]))
                       for a in pos for b in neg]
        remaining.remove(j)
    y = {}
    for j, constraints in reversed(stages):
        lower = []; upper = []
        for row in constraints:
            if not row.c[j]:
                continue
            remainder = row.rhs
            for k, c in enumerate(row.c):
                if k != j and c:
                    if k not in y:
                        raise RuntimeError('Uneliminated variable in back substitution')
                    remainder = remainder-y[k].scale(c)
            endpoint = remainder.scale(1/row.c[j])
            (upper if row.c[j] > 0 else lower).append(endpoint)
        lo = None
        for x in lower:
            if lo is None or lo.le(x): lo=x
        hi = None
        for x in upper:
            if hi is None or x.le(hi): hi=x
        if lo is not None and hi is not None and not lo.le(hi):
            raise RuntimeError('Inconsistent exact back substitution')
        y[j] = lo if lo is not None else (hi if hi is not None else LogValue())
    witness = [y[j] for j in range(n)]
    for row in original:
        lhs=LogValue()
        for c, value in zip(row.c, witness): lhs=lhs+value.scale(c)
        if not lhs.le(row.rhs):
            raise RuntimeError('Exact primal verification failed')
    return {'feasible':True,'log_magnitudes':[x.dump() for x in witness]}


def incidence(dims: tuple[int, ...], e: tuple[int, ...]) -> tuple[int, ...]:
    offset=0; result=[]
    for d,j in zip(dims,e):
        result.append(offset+j); offset+=d
    return tuple(result)


def validate(dims, values):
    dims=tuple(dims)
    if len(dims)<2 or any(not isinstance(d,int) or isinstance(d,bool) or d<1 for d in dims):
        raise ValueError('At least seed and query modes, with positive integer sizes, are required')
    keys=list(product(*(range(d) for d in dims)))
    vals=[F(v) for v in values]
    if len(vals)!=len(keys) or any(abs(v)>1 for v in vals):
        raise ValueError('Supply the complete lexicographic mean table with entries in [-1,1]')
    return dims, keys, dict(zip(keys,vals))


def signs_solve(masks, right, variable_count):
    """GF(2) RREF, with a row-XOR inconsistency witness."""
    rows=[[mask,int(b),1<<i] for i,(mask,b) in enumerate(zip(masks,right))]
    rank=0; pivots=[]
    for j in range(variable_count):
        found=next((i for i in range(rank,len(rows)) if rows[i][0]>>j&1),None)
        if found is None: continue
        rows[rank],rows[found]=rows[found],rows[rank]
        for i in range(len(rows)):
            if i!=rank and rows[i][0]>>j&1:
                rows[i]=[rows[i][a]^rows[rank][a] for a in range(3)]
        pivots.append(j); rank+=1
    for mask,b,proof in rows:
        if mask==0 and b:
            return None, [i for i in range(len(masks)) if proof>>i&1]
    free=[j for j in range(variable_count) if j not in pivots]
    out=[]
    for flags in range(1<<len(free)):
        z=sum((1<<j) for k,j in enumerate(free) if flags>>k&1)
        for i,j in enumerate(pivots):
            if (rows[i][1] ^ ((rows[i][0]&z).bit_count()&1)): z|=1<<j
        out.append(z)
    return out, None


def threshold(dims, values, delta, max_rows=50000, max_sign_variables=20):
    dims, keys, f=validate(dims,values); delta=F(delta)
    if delta<0: raise ValueError('Negative tolerance')
    active=[e for e in keys if abs(f[e])>delta]
    if not active:
        return {'feasible':True,'zero_product':True}
    vertices=sorted(set(v for e in active for v in incidence(dims,e)))
    if len(vertices)>max_sign_variables:
        raise ResourceLimit('Factor-sign enumeration budget exhausted')
    index={v:i for i,v in enumerate(vertices)}; n=len(vertices)
    subsets={e:tuple(index[v] for v in incidence(dims,e)) for e in keys
             if all(v in index for v in incidence(dims,e))}
    masks=[sum(1<<i for i in subsets[e]) for e in active]
    right=[int(f[e]<0) for e in active]
    sign_solutions, conflict=signs_solve(masks,right,n)
    if conflict is not None:
        return {'feasible':False,'kind':'sign','balanced_entries':[list(active[i]) for i in conflict]}
    floor={v:max(abs(f[e])-delta for e in active if v in incidence(dims,e)) for v in vertices}
    failures=[]; seen=set()
    for z in sign_solutions:
        entry_signs=tuple(-1 if sum((z>>i)&1 for i in subsets[e])%2 else 1 for e in subsets)
        if entry_signs in seen: continue
        seen.add(entry_signs)
        coeff=[]; bases=[]; names=[]
        for i,v in enumerate(vertices):
            row=[0]*n; row[i]=-1
            coeff.append(row); bases.append(F(1)); names.append(['nonnegative',v])
            row=[0]*n; row[i]=1
            coeff.append(row); bases.append(1/floor[v]); names.append(['cap',v])
        bad=None
        for e,sgn in zip(subsets,entry_signs):
            low=max(F(0),sgn*f[e]-delta); high=sgn*f[e]+delta
            if high<=0:
                bad=e; break
            row=[0]*n
            for i in subsets[e]: row[i]=-1
            coeff.append(row); bases.append(high); names.append(['upper',list(e)])
            if low>0:
                coeff.append([-c for c in row]); bases.append(1/low); names.append(['lower',list(e)])
        if bad is not None:
            failures.append({'sign_mask':z,'kind':'nonpositive_upper','entry':list(bad)})
            continue
        result=fm_solve(coeff,bases,max_rows)
        if result['feasible']:
            return {**result,'zero_product':False,'vertices':vertices,'sign_mask':z,
                    'chambers_tested':len(seen)}
        mult=result['multipliers']
        lhs=[sum(mult[i]*coeff[i][j] for i in range(len(coeff))) for j in range(n)]
        rhs=F(1)
        for b,q in zip(bases,mult): rhs*=b**q
        if any(lhs) or rhs>=1 or any(q<0 for q in mult):
            raise RuntimeError('Invalid generated dual')
        failures.append({'sign_mask':z,'kind':'magnitude','rows':names,
                         'coefficients':coeff,'bases':list(map(str,bases)),
                         'multipliers':mult,'product':str(rhs)})
    return {'feasible':False,'kind':'all_chambers','vertices':vertices,
            'chambers_tested':len(seen),'certificates':failures}


def verify_primal(dims, values, delta, certificate):
    dims,keys,f=validate(dims,values); delta=F(delta)
    if not certificate.get('feasible'): raise ValueError('Not a primal certificate')
    if certificate.get('zero_product'):
        return max(map(abs,f.values()))<=delta
    vertices=certificate['vertices']; index={v:i for i,v in enumerate(vertices)}
    y=[LogValue.load(v) for v in certificate['log_magnitudes']]
    if len(y)!=len(vertices) or any(v.sign()<0 for v in y): return False
    for e in keys:
        factors=incidence(dims,e)
        if any(v not in index for v in factors):
            if abs(f[e])>delta: return False
            continue
        ids=[index[v] for v in factors]
        sgn=-1 if sum((certificate['sign_mask']>>i)&1 for i in ids)%2 else 1
        high=sgn*f[e]+delta; low=max(F(0),sgn*f[e]-delta)
        logmag=LogValue()
        for i in ids: logmag=logmag-y[i]
        if high<=0 or not logmag.le(LogValue.base(high)): return False
        if low>0 and not LogValue.base(low).le(logmag): return False
    return True


def verify_dual(certificate):
    if certificate.get('kind')!='magnitude': raise ValueError('Not a magnitude certificate')
    C=certificate['coefficients']; z=certificate['multipliers']; b=list(map(F,certificate['bases']))
    if not C or not (len(C)==len(z)==len(b)): return False
    if any(not isinstance(q,int) or q<0 for q in z) or not any(z): return False
    if any(sum(q*row[j] for q,row in zip(z,C)) for j in range(len(C[0]))): return False
    value=F(1)
    for q,base in zip(z,b):
        if base<=0: return False
        value*=base**q
    return value<1


def verify_conclusion(dims, values, delta, certificate):
    """Bind a complete primal/dual conclusion to its actual input table.

    This verifier checks sign coverage and reconstructs the logarithmic rows;
    verify_dual alone verifies only a supplied algebraic inequality system.
    """
    dims,keys,f=validate(dims,values); delta=F(delta)
    if certificate.get('feasible'):
        return verify_primal(dims,values,delta,certificate)
    active=[e for e in keys if abs(f[e])>delta]
    if not active: return False
    vertices=sorted(set(v for e in active for v in incidence(dims,e)))
    index={v:i for i,v in enumerate(vertices)}; n=len(vertices)
    if certificate.get('kind')=='sign':
        entries=[tuple(e) for e in certificate['balanced_entries']]
        if not entries or len(set(entries))!=len(entries): return False
        mask=0; parity=0
        for e in entries:
            if e not in active: return False
            mask ^= sum(1<<index[v] for v in incidence(dims,e))
            parity ^= int(f[e]<0)
        return mask==0 and parity==1
    if certificate.get('kind')!='all_chambers' or certificate.get('vertices')!=vertices: return False
    subsets={e:tuple(index[v] for v in incidence(dims,e)) for e in keys
             if all(v in index for v in incidence(dims,e))}
    masks=[sum(1<<i for i in subsets[e]) for e in active]
    sign_solutions,conflict=signs_solve(masks,[int(f[e]<0) for e in active],n)
    if conflict is not None: return False
    def pattern(z): return tuple(-1 if sum((z>>i)&1 for i in subsets[e])%2 else 1 for e in subsets)
    expected={pattern(z) for z in sign_solutions}
    checked=set()
    floor={v:max(abs(f[e])-delta for e in active if v in incidence(dims,e)) for v in vertices}
    for c in certificate['certificates']:
        z=c['sign_mask']; signs=pattern(z)
        if signs not in expected or signs in checked: return False
        checked.add(signs)
        if c['kind']=='nonpositive_upper':
            e=tuple(c['entry'])
            if e not in subsets: return False
            sgn=-1 if sum((z>>i)&1 for i in subsets[e])%2 else 1
            if sgn*f[e]+delta>0: return False
            continue
        if c['kind']!='magnitude': return False
        C=[];bases=[];names=[]
        for i,v in enumerate(vertices):
            row=[0]*n;row[i]=-1
            C.append(row);bases.append(F(1));names.append(['nonnegative',v])
            row=[0]*n;row[i]=1
            C.append(row);bases.append(1/floor[v]);names.append(['cap',v])
        for e,sgn in zip(subsets,signs):
            lo=max(F(0),sgn*f[e]-delta);hi=sgn*f[e]+delta
            if hi<=0: return False
            row=[0]*n
            for i in subsets[e]: row[i]=-1
            C.append(row);bases.append(hi);names.append(['upper',list(e)])
            if lo>0:
                C.append([-q for q in row]);bases.append(1/lo);names.append(['lower',list(e)])
        if c['coefficients']!=C or c['bases']!=list(map(str,bases)) or c['rows']!=names: return False
        if not verify_dual(c): return False
    return checked==expected


def bracket(dims, values, steps=12, **limits):
    _,_,f=validate(dims,values); lo=F(0); hi=max(map(abs,f.values()))
    low_certificate=threshold(dims,values,lo,**limits)
    if low_certificate['feasible']:
        return {'mean_interval':['0','0'],'tv_interval':['0','0'],'upper_witness':low_certificate}
    upper_certificate={'feasible':True,'zero_product':True}
    for _ in range(steps):
        mid=(lo+hi)/2; candidate=threshold(dims,values,mid,**limits)
        if candidate['feasible']: hi=mid; upper_certificate=candidate
        else: lo=mid; low_certificate=candidate
    return {'mean_interval':[str(lo),str(hi)],'tv_interval':[str(lo/2),str(hi/2)],
            'lower_certificate':low_certificate,'upper_witness':upper_certificate}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='JSON with dims and lexicographic values (rational strings)')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--delta',help='Mean-error tolerance as a rational string (twice binary TV)')
    group.add_argument('--bisect',type=int,help='Number of certified rational bisection steps')
    parser.add_argument('--max-rows',type=int,default=50000)
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    try:
        if args.delta is not None:
            result=threshold(data['dims'],data['values'],args.delta,max_rows=args.max_rows)
        else:
            if args.bisect<0: raise ValueError('Negative iteration count')
            result=bracket(data['dims'],data['values'],args.bisect,max_rows=args.max_rows)
    except ResourceLimit as error:
        result={'status':'resource_limit','message':str(error),'feasibility':'undetermined'}
        print(json.dumps(result,indent=2)); raise SystemExit(2)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
