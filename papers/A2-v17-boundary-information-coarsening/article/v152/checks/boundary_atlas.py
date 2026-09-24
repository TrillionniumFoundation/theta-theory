"""Exact algebraic regressions for A2 v128.

These checks reproduce selected normal-form colon calculations and the
Schur-character identities used in the paper.  They are regression
evidence, not a substitute for the written proofs.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sympy as sp

a,b,c,d,z = sp.symbols("a b c d z")
VARS=(a,b,c,d)
delta=a*d-b*c

IT=sp.Matrix([
    [a,b,0,0],
    [c,d,0,0],
    [0,0,a,b],
    [0,0,c,d],
])
S2=sp.Matrix([
    [a*a,a*b,b*b],
    [2*a*c,a*d+b*c,2*b*d],
    [c*c,c*d,d*d],
])

def residual_ideal(B,C):
    X=(B*IT).row_join(C*S2)
    return [sp.expand(X[:,cols].det())
            for cols in combinations(range(7),3)
            if sp.expand(X[:,cols].det()) != 0]

def intersection(I,J):
    G=sp.groebner([z*f for f in I]+[(1-z)*g for g in J],
                  z,*VARS,order="lex")
    return [sp.expand(p.as_expr()) for p in G.polys
            if not p.as_expr().has(z)]

def colon(I,f):
    out=[]
    for g in intersection(I,[f]):
        q,r=sp.div(g,f,*VARS)
        assert sp.expand(r)==0
        out.append(sp.expand(q))
    G=sp.groebner(out,*VARS,order="grevlex")
    return [sp.expand(p.as_expr()) for p in G.polys]

def contains(I,f):
    G=sp.groebner(I,*VARS,order="grevlex")
    return sp.expand(G.reduce(f)[1])==0

def first_delta_power(I):
    for k in range(1,6):
        if contains(I,delta**k):
            return k
    raise AssertionError("universal d^5 bound violated in witness")

def hilbert_prefix(I,nmax=8):
    G=sp.groebner(I,*VARS,order="grevlex")
    lms=[p.LM(order=G.order).exponents for p in G.polys]
    out=[]
    for n in range(nmax+1):
        count=0
        for e in product(range(n+1), repeat=4):
            if sum(e)!=n:
                continue
            if not any(all(x>=y for x,y in zip(e,lm)) for lm in lms):
                count+=1
        out.append(count)
    return out

def layer_ideal(J,j):
    K=J
    for _ in range(j-1):
        K=colon(K,delta)
    return K+[delta]

B={
"r3_off":sp.Matrix([[0,1,0,0],[0,0,1,0],[1,0,0,-1]]),
"r3_on":sp.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,1]]),
"r2_sec":sp.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,0]]),
"r2_tan":sp.Matrix([[0,1,-1,0],[0,0,0,1],[0,0,0,0]]),
"r2_Hr":sp.Matrix([[0,0,1,0],[0,0,0,1],[0,0,0,0]]),
"r2_Wr":sp.Matrix([[0,1,0,0],[0,0,0,1],[0,0,0,0]]),
"r1_nd":sp.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0]]),
"r1_dec":sp.Matrix([[1,0,0,0],[0,0,0,0],[0,0,0,0]]),
"r0":sp.zeros(3,4),
}
C={
"r3_off":sp.eye(3),
"r3_on":sp.eye(3),
"r2_sec":sp.Matrix([[1,2,-2],[-2,-1,1],[-2,1,-2]]),
"r2_tan":sp.Matrix([[1,-2,-1],[0,1,0],[-1,-2,2]]),
"r2_Hr":sp.Matrix([[1,-1,-1],[1,1,-1],[2,-1,0]]),
"r2_Wr":sp.Matrix([[1,-1,1],[2,1,2],[1,0,-2]]),
"r1_nd":sp.Matrix([[-2,1,-1],[0,0,-2],[-2,0,-1]]),
"r1_dec":sp.Matrix([[-2,2,-1],[1,1,1],[2,1,-2]]),
"r0":sp.eye(3),
}

EXPECTED={
"r3_off":{"k":2,"W2":[1,0]},
"r3_on":{"k":2,"W2":[1,2,0]},
"r2_sec":{"k":2,"W2":[1,4,3,0]},
"r2_tan":{"k":2,"W2":[1,4,3,0]},
"r2_Hr":{"k":3,"W2":[1,4,6,4,0],"W3":[1,0]},
"r2_Wr":{"k":2,"W2":[1,4,6,4,5,6,7,8]},
"r1_nd":{"k":3,"W2":[1,4,9,8,10,12,14],"W3":[1,0]},
"r1_dec":{"k":3,"W2":[1,4,9,12,15,18,21],"W3":[1,2,0]},
"r0":{"k":3,"W2":[1,4,9,16,25,36],"W3":[1,4,9,16,25,36]},
}

def compositions(n,k,prefix=()):
    if k==1:
        yield prefix+(n,)
    else:
        for i in range(n+1):
            yield from compositions(n-i,k-1,prefix+(i,))

def add(A,B,scale=1):
    C0=defaultdict(int); C0.update(A)
    for w,v in B.items():
        C0[w]+=scale*v
        if C0[w]==0:
            del C0[w]
    return dict(C0)

def mul(A,B):
    n=len(next(iter(A))) if A else len(next(iter(B)))
    C0=defaultdict(int)
    for w,u in A.items():
        for z0,v in B.items():
            C0[tuple(w[i]+z0[i] for i in range(n))]+=u*v
    return dict(C0)

def sign(p):
    inv=sum(p[i]>p[j] for i in range(len(p))
            for j in range(i+1,len(p)))
    return -1 if inv%2 else 1

def schur(lam,n):
    lam=tuple(lam)+(0,)*(n-len(lam))
    @lru_cache(None)
    def h(k):
        if k<0:
            return {}
        if k==0:
            return {tuple([0]*n):1}
        return {w:1 for w in compositions(k,n)}
    total={}
    for p in permutations(range(n)):
        q={tuple([0]*n):1}
        ok=True
        for i in range(n):
            hh=h(lam[i]-i+p[i])
            if not hh:
                ok=False; break
            q=mul(q,hh)
        if ok:
            total=add(total,q,sign(p))
    return total

def wedge_sym2_char(n,k):
    weights=[]
    for i in range(n):
        for j in range(i,n):
            w=[0]*n; w[i]+=1; w[j]+=1
            weights.append(tuple(w))
    out=defaultdict(int)
    for I in combinations(range(len(weights)),k):
        w=tuple(sum(weights[j][i] for j in I) for i in range(n))
        out[w]+=1
    return dict(out)

def representation_checks():
    lhs=wedge_sym2_char(4,6)
    rhs=add(schur((5,4,2,1),4),schur((4,4,4,0),4))
    assert lhs==rhs
    assert (3,3,3,3) not in {(5,4,2,1),(4,4,4,0)}
    # The GL3 decompositions used to exclude det^3 at corank three.
    assert wedge_sym2_char(3,2)==schur((3,1,0),3)
    assert wedge_sym2_char(3,3)==add(
        schur((4,1,1),3),schur((3,3,0),3))
    assert wedge_sym2_char(3,4)==schur((4,3,1),3)
    return True

def run():
    rows={}
    for name in B:
        J=residual_ideal(B[name],C[name])
        k=first_delta_power(J)
        assert k==EXPECTED[name]["k"], (name,k)
        w2=hilbert_prefix(layer_ideal(J,2),7)
        exp2=EXPECTED[name]["W2"]
        assert w2[:len(exp2)]==exp2, (name,"W2",w2,exp2)
        row={"first_delta_power":k,"W2_hilbert_prefix":w2}
        if "W3" in EXPECTED[name]:
            w3=hilbert_prefix(layer_ideal(J,3),5)
            exp3=EXPECTED[name]["W3"]
            assert w3[:len(exp3)]==exp3, (name,"W3",w3,exp3)
            row["W3_hilbert_prefix"]=w3
        rows[name]=row
    assert representation_checks()
    # Exact b=0 identity J=(delta^3), up to the unit det(C)=1.
    J0=residual_ideal(B["r0"],C["r0"])
    assert all(contains([delta**3],f) for f in J0)
    assert contains(J0,delta**3)
    out={
      "kind":"exact symbolic regression, not theorem certification",
      "mixed_kernel_witnesses":rows,
      "wedge6_sym2_GL4_decomposition":True,
      "corank3_GL3_character_identities":True,
      "b0_exact_delta_cubed":True,
    }
    evidence=Path(__file__).resolve().parents[1]/"evidence"
    evidence.mkdir(exist_ok=True)
    (evidence/"BOUNDARY_ATLAS_CERTIFICATES.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    run()
