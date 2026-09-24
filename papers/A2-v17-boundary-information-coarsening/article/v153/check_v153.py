#!/usr/bin/env python3
"""Exact finite consistency checks; these do not certify the general proofs."""
from __future__ import annotations
import hashlib, itertools as it, json, math
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
results=[]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def minimal(gens):
    unique=sorted(set(gens),key=lambda x:(sum(x),x))
    answer=[]
    for mon in unique:
        if not any(all(a<=b for a,b in zip(old,mon)) for old in answer):
            answer.append(mon)
    return set(answer)


def intersection(left,right):
    return minimal(tuple(max(a,b) for a,b in zip(x,y)) for x in left for y in right)


def coordinate_ideal(blocks,s,m):
    return {tuple(int(j==i*m+k) for j in range(s*m)) for i in blocks for k in range(m)}


def block_ideal(blocks,s,m):
    if not blocks:
        return {(0,)*(s*m)}
    answer=set()
    for choices in it.product(range(m),repeat=len(blocks)):
        mon=[0]*(s*m)
        for i,k in zip(blocks,choices):
            mon[i*m+k]=1
        answer.add(tuple(mon))
    return answer


def squarefree_checks():
    cases=0
    for s in range(1,6):
        for m in (1,2):
            for g in range(1,s+1):
                branches=list(it.combinations(range(s),g))
                ideals=[coordinate_ideal(A,s,m) for A in branches]
                got={(0,)*(s*m)}
                for ideal in ideals:
                    got=intersection(got,ideal)
                expected=set().union(*(block_ideal(B,s,m) for B in it.combinations(range(s),s-g+1)))
                require(got==expected,f'branch image {s,m,g}')
                for index,A in enumerate(branches):
                    other={(0,)*(s*m)}
                    for j,ideal in enumerate(ideals):
                        if j!=index:
                            other=intersection(other,ideal)
                    surviving={x for x in other if not any(x[i*m+k] for i in A for k in range(m))}
                    expected_c=block_ideal(tuple(i for i in range(s) if i not in A),s,m)
                    require(minimal(surviving)==expected_c,f'conductor {s,m,g,A}')
                cases+=1
    results.append({'family':'squarefree image and conductor monomial ideals','parameter_cases':cases,'pass':True})


def reciprocal(g,k):
    q=sp.symbols(f'q1:{k+1}')
    c=[sp.Integer(1)]
    for j in range(1,g+k+1):
        c.append(sp.expand(-sum(q[i-1]*c[j-i] for i in range(1,min(j,k)+1))))
    return q,c


def binary_checks():
    z=sp.Symbol('z'); cases=0
    for k in range(1,4):
        for g in range(k,6):
            q,c=reciprocal(g,k)
            basis=sp.groebner(c[g+1:g+k+1],*q,order='grevlex')
            require(basis.is_zero_dimensional,f'binary finiteness {g,k}')
            leading=[p.LM(order=basis.order).exponents for p in basis.polys]
            bounds=[]
            for i in range(k):
                bounds.append(min(mon[i] for mon in leading if mon[i]>0 and sum(mon)==mon[i]))
            standard=[v for v in it.product(*(range(b) for b in bounds))
                if not any(all(a<=b for a,b in zip(mon,v)) for mon in leading)]
            hilbert=sp.Poly(sum(z**sum((i+1)*v[i] for i in range(k)) for v in standard),z)
            predicted=sp.cancel(sp.prod((1-z**(g+i))/(1-z**i) for i in range(1,k+1)))
            require(sp.expand(hilbert.as_expr()-predicted)==0,f'weighted Hilbert {g,k}')
            require(len(standard)==math.comb(g+k,k),f'length {g,k}')
            require(basis.reduce(q[-1]**g)[1]!=0,f'socle nonzero {g,k}')
            for x in q:
                require(basis.reduce(x*q[-1]**g)[1]==0,f'socle annihilation {g,k}')
            cases+=1
    for parts in [(1,1,1,1),(2,1,3),(3,3),(2,2,2),(4,3,1)]:
        for g in range(sum(parts)+1):
            value=sum(math.prod(math.comb(s,a) for s,a in zip(parts,choice))
                for choice in it.product(*(range(s+1) for s in parts)) if sum(choice)==g)
            require(value==math.comb(sum(parts),g),f'cluster length {parts,g}')
    results.append({'family':'binary reciprocal Hilbert series, length and socle','parameter_cases':cases,'cluster_partitions':5,'pass':True})


def fitting_checks():
    cases=[]
    for m in range(1,5):
        u=sp.symbols(f'u0:{m}'); w=sp.symbols(f'w0:{m}')
        delta,t=sp.symbols('Delta t')
        relations=[u[i]*w[j]-u[j]*w[i] for i in range(m) for j in range(i+1,m)]
        relations += [w[i]*w[j]-delta*u[i]*u[j] for i in range(m) for j in range(i,m)]
        jac=sp.Matrix(relations).jacobian(u+(delta,)+w)
        sub=dict(zip(w,[x*t for x in u]));sub[delta]=t*t
        all_minors=0
        if m<=2:
            for rows in it.combinations(range(len(relations)),m):
                for cols in it.combinations(range(2*m+1),m):
                    value=sp.expand(jac.extract(rows,cols).det().subs(sub))
                    for powers,coeff in sp.Poly(value,*(u+(t,))).terms():
                        if coeff:
                            require(sum(powers[:-1])>=m and (sum(powers[:-1])>=m+1 or powers[-1]>=1),
                                f'Fitting upper inclusion {m,rows,cols}')
                    all_minors+=1
        selected=[u[0]*w[j]-u[j]*w[0] for j in range(1,m)]+[w[0]**2-delta*u[0]**2]
        matrix=sp.Matrix(selected).jacobian(u+(delta,)+w)
        choices=[list(range(m+1,2*m+1)),[0]+list(range(m+2,2*m+1)),[m]+list(range(m+2,2*m+1))]
        targets=[u[0]**m*t,u[0]**m*t*t,u[0]**(m+1)]
        for cols,target in zip(choices,targets):
            quotient=sp.cancel(matrix.extract(range(m),cols).det().subs(sub)/target)
            require(quotient.is_number and quotient!=0,f'Fitting lower generators {m,cols}')
        cases.append({'m':m,'all_minors_tested':all_minors,'three_generator_minors':True})
    results.append({'family':'evaluated Fitting ideal','cases':cases,'pass':True})


def multivariate_checks():
    x,y,a,b,c,d,e=sp.symbols('x y a b c d e');vars=(a,b,c,d,e)
    Q1=a*x+b*y;Q2=c*x*x+d*x*y+e*y*y
    C3=sp.Poly(2*Q1*Q2-Q1**3,x,y).coeffs()
    C4=sp.Poly(Q1**4-3*Q1**2*Q2+Q2**2,x,y).coeffs()
    def rank(polys):
        pp=[sp.Poly(p,*vars) for p in polys]
        mon=sorted(set().union(*(set(p.monoms()) for p in pp)))
        return sp.Matrix([[p.coeff_monomial(v) for v in mon] for p in pp]).rank()
    lower=[v*f for v in (a,b) for f in C3]
    require(rank(C3)==4,'weight-three minimal coefficient space')
    require(rank(lower+C4)-rank(lower)==5,'weight-four minimal coefficient space')
    basis=sp.groebner(C3+C4,*vars,order='grevlex')
    leading=[p.LM(order=basis.order).exponents for p in basis.polys]
    bounds=[min(mon[i] for mon in leading if mon[i]>0 and sum(mon)==mon[i]) for i in range(5)]
    standard=[v for v in it.product(*(range(q) for q in bounds))
        if not any(all(a<=b for a,b in zip(mon,v)) for mon in leading)]
    h={}
    for v in standard:
        j=sum(w*z for w,z in zip((1,1,2,2,2),v));h[j]=h.get(j,0)+1
    require(h=={0:1,1:2,2:6,3:6,4:7},'multivariate weighted Hilbert example')
    require(math.comb(10,2)-1==44 and math.comb(14,7)+math.comb(15,8)==9867,'ternary-pencil counts')
    results.append({'family':'multivariate reciprocal minimality','example':{'d':2,'g':2,'k':2,'minimal_relations':9,'length':len(standard),'weighted_hilbert':h},'ternary_embedding_dimension':44,'ternary_minimal_relations':9867,'pass':True})


if __name__=='__main__':
    squarefree_checks();binary_checks();fitting_checks();multivariate_checks()
    data={'revision':153,'all_families_pass':True,'families':results,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'new_core_sha256':hashlib.sha256((HERE/'new-core.tex').read_bytes()).hexdigest(),
        'proof_certified_by_computation':False,'historical_28_checks_rerun':False}
    (HERE/'EXACT_CHECKS_V153.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
