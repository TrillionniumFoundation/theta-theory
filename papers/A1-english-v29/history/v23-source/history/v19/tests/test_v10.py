#!/usr/bin/env python3
"""Exact finite diagnostics, not a proof of continuum entropy or journal merit."""
import json
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import random
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from finite_compiler import Machine, compile_tables, distance, dyadic, greedy

COUNTS = Counter()
def check(condition, category):
    if not condition:
        raise AssertionError(category)
    COUNTS[category] += 1


def labels(m):
    return tuple((i, j, m-i-j) for i in range(m+1) for j in range(m-i+1))


def multiply(p, f):
    out = {}
    for b, c in p.items():
        for i, d in enumerate(f):
            a = tuple(b[j] + (j == i) for j in range(3))
            out[a] = out.get(a, F(0)) + c*d
    return out


class Model:
    def __init__(self, gap, prior):
        self.a = (F(0), F(1), F(2)+gap)
        self.prior = prior
        self.grid = tuple(product((F(1,4), F(3,4)), repeat=3))
        d = F(1,16)
        self.cells = ((F(1,3), -d, -d), (F(1,3), d, F(0)),
                      (F(1,3), F(0), d))
        self.cache = {}

    def moment(self, b):
        s = sum(v*a for v, a in zip(b, self.a))
        if self.prior == 'uniform':
            return 1/(s+1)
        return 3/(s+3)  # density 3t^2, also full support

    def factor(self, g, x):
        if x < 3:
            return tuple(g[x]*c for c in self.cells[x])
        return tuple(sum((1-g[j])*self.cells[j][i] for j in range(3)) for i in range(3))

    def polynomial(self, history, actual=False):
        p = {(0,0,0): F(1)}
        for g, x in history:
            p = multiply(p, self.factor(g if actual else self.grid[g], x))
        return p

    def state(self, history, actual=False):
        key = (history, actual)
        if key not in self.cache:
            p = self.polynomial(history, actual)
            z = sum(c*self.moment(b) for b, c in p.items())
            check(z >= F(1,32)**len(history), 'positive_prefix_evidence')
            self.cache[key] = tuple(sum(c*self.moment(tuple(v+w for v,w in zip(a,b)))
                                       for b,c in p.items())/z
                                    for a in labels(3-len(history)))
        return self.cache[key]

    def predictions(self, history):
        m = 3-len(history)
        raw = dict(zip(labels(m), self.state(history)))
        basis = ((F(1,2),F(0),F(0)), (F(1,2),F(1,32),F(0)),
                 (F(1,2),F(0),F(1,32)))
        out=[]
        for word in product(basis, repeat=m):
            p={(0,0,0):F(1)}
            for f in word:
                p=multiply(p,f)
            out.append(sum(c*raw[b] for b,c in p.items()))
        return tuple(out)

    def update(self, v, n, g, x):
        m=3-n
        old=dict(zip(labels(m),v))
        f=self.factor(g,x)
        den=sum(f[i]*old[tuple((m-1)*(j==0)+(i==j) for j in range(3))] for i in range(3))
        return tuple(sum(f[i]*old[tuple(a[j]+(i==j) for j in range(3))]
                         for i in range(3))/den for a in labels(m-1))


def greedy_checks():
    samples = [(F(1,2),)*5, (F(0),F(1,1000),F(1,3),F(2,3),F(1)),
               (F(0),F(1,10**12),F(1,8),F(1,8)+F(1,10**12),F(1))]
    for xs in samples:
        xs=tuple(sorted(xs)); size=len(xs)
        for budget in range(1,size+1):
            # Exact one-dimensional unrestricted-centre optimum via contiguous partitions.
            dp={(0,0):F(0)}
            for k in range(1,budget+1):
                for j in range(1,size+1):
                    candidates=[max(dp[(k-1,i)],(xs[j-1]-xs[i])/2)
                                for i in range(j) if (k-1,i) in dp]
                    if candidates: dp[(k,j)]=min(candidates)
            optimum=min(dp[k,size] for k in range(1,budget+1) if (k,size) in dp)
            approx=tuple(dyadic((x,),3) for x in xs)
            indices=greedy(approx,budget)
            radius=max(min(abs(x-xs[i]) for i in indices) for x in xs)
            check(radius <= 2*optimum+4*F(1,8), 'approximate_greedy_cover')
            check(len(indices)<=budget and len(set(indices))==len(indices),'greedy_index_budget')


def run_fixture(gap, prior, budgets):
    model=Model(gap,prior)
    rng=random.Random(1006)
    receipts=[]
    for budget in budgets:
        bits=8+budget.bit_length(); tau=F(1,1<<bits)
        program,audit=compile_tables(2,8,4,budget,bits,model.state,model.predictions)
        check(all(k<=budget for k in program.state_counts),'persistent_budget')
        check(audit.candidate_counts==(1,32,1024),'candidate_enumeration')
        machine=Machine()
        check(machine.__slots__==('index',) and not hasattr(machine,'__dict__'),'index_only_runtime')
        check(not hasattr(program,'representatives') and not hasattr(program,'evaluate'),
              'no_history_or_oracle_in_program')
        for n in range(2):
            for i,hist in enumerate(audit.representatives[n]):
                old=audit.exact_vectors[n][i]
                for u,g in enumerate(model.grid):
                    for x in range(4):
                        y=model.state(hist+((u,x),))
                        check(model.update(old,n,g,x)==y,'raw_update_equals_product_integral')
                        j=program.transitions[n][i][u][x]
                        check(0<=j<program.state_counts[n+1],'integer_transition_range')
                        check(distance(y,audit.exact_vectors[n+1][j]) <=
                              audit.sample_cover_radii[n+1]+4*tau,'compiled_transition_error')
        for _ in range(24):
            machine=Machine(); actual=(); old=model.state(actual,True)
            previous_error=F(0)
            for n in range(2):
                g=tuple(F(rng.randrange(16,49),64) for _ in range(3))
                u=min(range(8),key=lambda j:(distance(g,model.grid[j]),j))
                x=rng.randrange(4)
                actual+=((g,x),)
                truth=model.state(actual,True)
                check(model.update(old,n,g,x)==truth,'offgrid_raw_update')
                machine.step(program,n,u,x)
                error=distance(truth,audit.exact_vectors[n+1][machine.index])
                # L=128, G=192 are conservative uniform bounds with kappa=1/32.
                check(error<=128*previous_error+192*F(1,4)+
                      audit.sample_cover_radii[n+1]+4*tau,'accumulated_offgrid_error')
                out=machine.output(program,n+1,0)
                check(0<=out<=1,'dyadic_probability')
                previous_error=error;old=truth
        # Exact coincident labels must agree, without deduplicating their indices.
        if gap==0:
            for h in audit.representatives[1]:
                pairs=list(zip(labels(2),model.state(h)))
                for a,v in pairs:
                    for b,w in pairs:
                        if sum(x*y for x,y in zip(a,model.a))==sum(x*y for x,y in zip(b,model.a)):
                            check(v==w,'coincident_formal_labels')
        receipts.append({'M':budget,'bits':bits,'state_counts':program.state_counts,
                         'candidate_counts':audit.candidate_counts,
                         'sample_radii':[str(x) for x in audit.sample_cover_radii]})
    return {'gap':str(gap),'prior':prior,'runs':receipts}


def main():
    greedy_checks()
    fixtures=[run_fixture(g,p,(1,2,4)) for g,p in
              [(F(0),'uniform'),(F(1,10**12),'uniform'),(F(1,7),'density_3t2')]]
    result={'status':'passed','assertions':sum(COUNTS.values()),'categories':dict(COUNTS),
            'fixtures':fixtures,'scope':'Exact finite diagnostics; not continuum proof, priority or editorial approval.'}
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('V10_DIAGNOSTICS.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))

if __name__=='__main__': main()
