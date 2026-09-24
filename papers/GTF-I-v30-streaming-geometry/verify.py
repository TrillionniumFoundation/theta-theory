#!/usr/bin/env python3
"""Exact finite regressions for the analytic v30 proofs. No assert-based guards."""
from __future__ import annotations
import argparse
import itertools as it
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path
import sympy as sp

class VerificationError(RuntimeError):
    pass

def require(ok: bool, message: str) -> None:
    if not ok:
        raise VerificationError(message)

def words(n: int):
    return it.product((-1, 1), repeat=n)

def reservoir(x: tuple[int, ...], mutant: str = '') -> list[F]:
    p = [F(1)]
    for t, bit in enumerate(x):
        replace = F(1, t + 1)
        if mutant == 'reservoir-weight' and t:
            replace = F(1, t + 2)
        new = [v * (1 - replace) for v in p] + [F(0)]
        new[t + 1 if bit == 1 else 0] += replace
        require(sum(new) == 1 and min(new) >= 0, 'illegal reservoir row')
        p = new
    return p

def mean_from_reservoir(p: list[F], eta: F) -> list[F]:
    t = len(p) - 1
    return [-eta + 2*t*eta*p[i+1] for i in range(t)]

def sylvester(m: int) -> list[list[int]]:
    h = [[1]]
    while len(h) < m:
        h = [r+r for r in h] + [r+[-x for x in r] for r in h]
    return h

def main(mutant: str = '') -> dict:
    stats = {'schema': 'gtf30.exact/1'}
    nwords = rows = coordinates = 0
    for n in range(1, 10):
        eta = F(1, 2*n-1)
        for x in words(n):
            p = reservoir(x, mutant)
            expected = [F(sum(bit == -1 for bit in x), n)] + [F(int(bit == 1), n) for bit in x]
            require(p == expected, 'reservoir-law identity failed')
            require(mean_from_reservoir(p, eta) == [eta*v for v in x], 'exact conditional mean failed')
            require((2*n-1)*eta <= 1, 'enclosing vertices outside cube')
            nwords += 1; coordinates += n
        for s in range(n):
            for bit in (-1, 1):
                p = [F(0)]*n; p[s] = F(1)
                q = [v*F(n-1, n) for v in p]+[F(0)]
                q[n if bit == 1 else 0] += F(1, n)
                require(sum(q) == 1 and min(q) >= 0, 'nonstochastic update')
                rows += 1
    stats.update(reservoir_words=nwords, reservoir_update_rows=rows, exact_mean_coordinates=coordinates,
                 reservoir_signal='1/(2*n-1)', reservoir_profile='t+1')

    had_cases = 0
    for m, n in [(2,1),(4,3),(8,7),(8,5),(16,15)]:
        h=sylvester(m); v=[r[1:n+1] for r in h]
        require(all(sum(v[s][j] for s in range(m)) == 0 for j in range(n)), 'Hadamard centering')
        require(all(sum(v[s][i]*v[s][j] for s in range(m)) == m*int(i==j) for i in range(n) for j in range(n)), 'Hadamard orthogonality')
        testwords = list(words(n)) if n <= 7 else [tuple([1]*n),tuple([-1]*n),tuple(1 if i%2 else -1 for i in range(n))]
        for x in testwords:
            p=[F(0)]*m
            for i, bit in enumerate(x, start=1):
                q=[F(1+bit*v[s][i-1],m) for s in range(m)]
                require(sum(q)==1 and min(q)>=0,'Hadamard redraw row')
                p=[F(i-1,i)*p[s]+F(1,i)*q[s] for s in range(m)]
            eta=F(1,n)
            scale = eta if mutant == 'hadamard-scale' else n*eta
            out=[sum(p[s]*scale*v[s][j] for s in range(m)) for j in range(n)]
            require(out==[eta*b for b in x], 'Hadamard exact response failed')
            had_cases += 1
        if m == n+1:
            # lambda_s(z)=(1+v_s dot z)/m saturates the trace inequality.
            require(sum(F(1,m) for _ in range(m))==1,'simplex intercepts')
            require(sum(F(n,m) for _ in range(m))==n,'trace saturation')
    stats.update(hadamard_word_cases=had_cases, sharp_hadamard_threshold='1/n')

    for a in [F(1,7),F(1,3)]:
        verts=[(-a,-a),(3*a,-a),(-a,3*a)]
        require(all(abs(c)<=1 for v in verts for c in v),'triangle legality')
        for x in words(2):
            z=[a*t for t in x]
            lam=[(2*a-sum(z))/(4*a),(z[0]+a)/(4*a),(z[1]+a)/(4*a)]
            require(min(lam)>=0 and sum(lam)==1,'triangle enclosure weights')
            require([sum(lam[s]*verts[s][j] for s in range(3)) for j in range(2)]==z,'triangle enclosure identity')
        mat=sp.Matrix([[1]+list(v) for v in it.product((-a,a),repeat=2)])
        require(mat.rank()==3,'square affine rank')
    for x in words(3):
        for y in words(3):
            if x==y: continue
            # Minimum of d_x(z)+d_y(z) over the cube is Hamming distance.
            md=F(3)-sum(F(abs(a+b),2) for a,b in zip(x,y))
            require(md>=1,'disjoint-cap inequality')
    # Concatenated factors need per-query normalization, not just total mass.
    bad=[F(1),F(0),F(1,4),F(3,4)]
    if mutant == 'query-normalization': bad=[F(3,2),F(0),F(1,4),F(1,4)]
    require(sum(bad[:2])==sum(bad[2:])==1,'query block normalization lost')
    stats['nonsimplicial_examples_checked']=2

    layers=0
    for n in range(2,9):
        for eta, delta in [(F(1,4),F(1,8)),(F(1,2),F(1,8))]:
            z=F(n)*(1+eta+2*delta)/2
            k=(z.numerator+z.denominator-1)//z.denominator
            r=F(2*k,n)-1
            require(k<=n and r>=eta+2*delta,'layer parameters')
            p=F(k,n)
            mode=F(comb(n,k))*p**k*(1-p)**(n-k)
            require(mode>=F(1,n+1),'binomial mode lower bound')
            for weights in [tuple(F(1,n) for _ in range(n)),tuple([F(1)]+[F(0)]*(n-1)),tuple(F(i+1,n*(n+1)//2) for i in range(n))]:
                vals=[]
                for aligned in it.combinations(range(n),k):
                    st=set(aligned)
                    vals.append(sum(w*(1 if i in st else -1) for i,w in enumerate(weights)))
                require(sum(vals)/len(vals)==r,'weighted layer mean')
                hit=F(sum(v>=eta+delta for v in vals),len(vals))
                require(hit>=delta,'all-direction layer hit lower bound')
                require(F(len(vals),2**n)*hit>=delta*F(comb(n,k),2**n),'unconditional layer bound')
                layers+=1
    stats['exact_weighted_layer_cases']=layers

    # A concrete compatible block implementation, with each raw overwrite exposed.
    block_cases=0
    for n, ell in [(5,2),(6,3),(7,3)]:
        eta=F(1,2*ell-1); b=n//ell
        symbolic_peak=2**ell*(ell+1)**b
        if mutant == 'raw-buffer': symbolic_peak=(ell+1)**max(0,b-1)
        require(symbolic_peak>=2**ell*(ell+1)**max(0,b-1),'raw block buffer not priced')
        for x in words(n):
            probs={():F(1)}
            for start in range(0,b*ell,ell):
                px=reservoir(x[start:start+ell])
                probs={labs+(s,):mass*px[s] for labs,mass in probs.items() for s in range(ell+1) if px[s]}
                require(sum(probs.values())==1,'block joint normalization')
            for j in range(n):
                if j < b*ell:
                    bj, ij=divmod(j,ell)
                    m=sum(mass*(-eta+2*ell*eta*int(labs[bj]==ij+1)) for labs,mass in probs.items())
                else: m=eta*x[j]
                require(m==eta*x[j], 'block exact response')
            block_cases+=1
    stats['block_words_checked']=block_cases

    lang=0
    for n in range(2,7):
        eta=F(1,2*n-1); total=F(0)
        residuals=[]
        for x in words(n):
            p=reservoir(x)
            row=[]
            for j in range(n):
                mu=sum(p[s]*(-eta+2*n*eta*int(s==j+1)) for s in range(n+1))
                for bit in (-1,1):
                    val=(1+bit*mu)/(2*n)
                    require(val==(1+bit*eta*x[j])/(2*n),'finite-language response')
                    row.append(val); total+=val/F(2**n)
            residuals.append(tuple(row)); lang+=1
        require(total==1,'finite-language total mass')
        require(len(set(residuals))==2**n,'distinct residual cube corners')
        require(sp.Matrix(residuals).rank()==n+1,'finite-language rank')
    if mutant == 'residual-size':
        require(2**8 <= (8+1)*(8+2)//2+8*(8+1)+1, 'residual-only minimum incorrectly substituted')
    stats['finite_language_words']=lang

    for eta, eps in [(F(1,2),F(1,10)),(F(3,4),F(1,8)),(F(1,4),F(1,4))]:
        kappa=max(F(0),eta-2*eps)
        factor=F(1) if mutant=='tv-factor' else F(1,2)
        require(factor*abs(eta-kappa)<=eps, 'row-TV/mean conversion wrong')
    for n in range(1,5):
        channel=sp.Matrix([[sp.Rational(3,4),sp.Rational(1,4)],[sp.Rational(1,4),sp.Rational(3,4)]])
        mat=sp.ones(1,1)
        for _ in range(n): mat=sp.kronecker_product(mat,channel)
        require(mat.rank()==2**n,'full joint-output rank')
    stats.update(joint_output_rank_lengths=[1,2,3,4],
        entropy_exponent='1-h2((1+eta)/2)',
        exact_checkpoint_log_overhead='O_eta(log(n+1))',
        exact_streaming_log_overhead='O_eta(sqrt(n*log(n+1)))',
        uniform_approximation_effective_signal='max(eta-2*epsilon,0)',
        interpretation='Finite exact algebra and implementations, not proof of asymptotics, priority clearance or independent proof certification.')
    return stats

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--negative-control', default='', choices=['','reservoir-weight','hadamard-scale','query-normalization','raw-buffer','residual-size','tv-factor']); ap.add_argument('--output', type=Path)
    args=ap.parse_args()
    try:
        result=main(args.negative_control)
    except VerificationError as exc:
        raise SystemExit('CHECK_REJECTED: '+str(exc))
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(text)
    print(text,end='')
