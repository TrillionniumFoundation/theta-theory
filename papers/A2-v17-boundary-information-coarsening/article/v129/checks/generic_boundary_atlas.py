"""Exact generic-point calculations for A2 revision 128.

The purpose of this file is narrow:
* certify stabilizer-slice dominance by exact tangent ranks;
* compute the relevant residual colons over rational function fields;
* check the generic Hilbert signatures used in the paper;
* record the rank-one binary factors identifying ruling divisors.

All arithmetic is exact.  This is reproducibility evidence for the
finite computer-assisted calculations; the structural arguments remain
in the manuscript.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
from pathlib import Path
from functools import lru_cache
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

def residual_ideal(B,C,q=None):
    if q is None:
        q=B.rows
    X=(B*IT).row_join(C*S2)
    return [
        sp.expand(X[:,cols].det())
        for cols in combinations(range(7),q)
        if sp.expand(X[:,cols].det()) != 0
    ]

def intersection(I,J,dom):
    G=sp.groebner(
        [z*f for f in I]+[(1-z)*g for g in J],
        z,*VARS,order="lex",domain=dom
    )
    return [
        sp.expand(p.as_expr()) for p in G.polys
        if not p.as_expr().has(z)
    ]

def colon(I,f,dom):
    out=[]
    for g in intersection(I,[f],dom):
        q,r=sp.div(g,f,*VARS,domain=dom)
        assert sp.expand(r)==0
        out.append(sp.expand(q))
    G=sp.groebner(out,*VARS,order="grevlex",domain=dom)
    return [sp.expand(p.as_expr()) for p in G.polys]

def first_delta_power(J,dom):
    G=sp.groebner(J,*VARS,order="grevlex",domain=dom)
    for k in range(1,6):
        if sp.expand(G.reduce(delta**k)[1])==0:
            return k
    raise AssertionError("universal determinant-completion bound failed")

def hilbert_from_lms(lms,nmax=7):
    out=[]
    for n in range(nmax+1):
        count=0
        for e in product(range(n+1),repeat=4):
            if sum(e)!=n:
                continue
            if not any(all(x>=y for x,y in zip(e,lm)) for lm in lms):
                count+=1
        out.append(count)
    return out

def layer_data(J,k,dom):
    K=J
    rows=[]
    for j in range(1,k+1):
        if j>1:
            K=colon(K,delta,dom)
        G=sp.groebner(K+[delta],*VARS,order="grevlex",domain=dom)
        lms=[tuple(p.LM(order=G.order).exponents) for p in G.polys]
        rows.append({
            "j":j,
            "hilbert":hilbert_from_lms(lms),
            "leading_monomials":[list(e) for e in lms],
            "basis":[str(sp.factor(p.as_expr())) for p in G.polys],
        })
    return rows

def sym2_derivative(Y):
    y00,y01,y10,y11=Y[0,0],Y[0,1],Y[1,0],Y[1,1]
    return sp.Matrix([
        [2*y00,y01,0],
        [2*y10,y00+y11,2*y01],
        [0,y10,2*y11],
    ])

def kron_derivative(X,Y):
    return sp.kronecker_product(X,sp.eye(2))+sp.kronecker_product(sp.eye(2),Y)

def stabilizer_tangent(B,C):
    q=B.rows
    xvars=sp.symbols("x0:4")
    yvars=sp.symbols("y0:4")
    zvars=sp.symbols(f"zz0:{q*q}")
    variables=xvars+yvars+zvars
    X=sp.Matrix(2,2,xvars)
    Y=sp.Matrix(2,2,yvars)
    Z=sp.Matrix(q,q,zvars)
    equations=Z*B-B*kron_derivative(X,Y)
    A,_=sp.linear_eq_to_matrix(list(equations),variables)
    kernel=A.nullspace()
    images=[]
    for vec in kernel:
        sub={v:vec[i] for i,v in enumerate(variables)}
        image=(Z*C-C*sym2_derivative(Y)).subs(sub)
        images.append(sp.Matrix(q*3,1,list(image)))
    M=sp.Matrix.hstack(*images) if images else sp.zeros(q*3,0)
    return len(kernel),M

def complement_indices(M,n):
    current=M
    rank=current.rank()
    out=[]
    for i in range(n):
        e=sp.zeros(n,1)
        e[i]=1
        candidate=sp.Matrix.hstack(current,e)
        newrank=candidate.rank()
        if newrank>rank:
            out.append(i)
            current=candidate
            rank=newrank
        if rank==n:
            break
    assert rank==n
    return out

def denominators_nonzero_at_origin(rows,params):
    bad=[]
    for row in rows:
        for expr in row["basis"]:
            ee=sp.sympify(expr)
            num,den=sp.fraction(sp.cancel(ee))
            if den!=1:
                value=sp.simplify(den.subs({p:0 for p in params}))
                if value==0:
                    bad.append(str(den))
    return bad

def generic_slice_case(name,B,C0,slice_positions,expected_k,expected_h):
    params=sp.symbols(f"s0:{len(slice_positions)}")
    C=C0.copy()
    for s0,idx in zip(params,slice_positions):
        C[idx//3,idx%3]+=s0
    dom=sp.QQ.frac_field(*params) if params else sp.QQ

    stabdim,tangent=stabilizer_tangent(B,C0)
    orbit_rank=tangent.rank()
    augmented=tangent
    for idx in slice_positions:
        e=sp.zeros(B.rows*3,1)
        e[idx]=1
        augmented=sp.Matrix.hstack(augmented,e)
    assert augmented.rank()==B.rows*3

    J=residual_ideal(B,C)
    k=first_delta_power(J,dom)
    assert k==expected_k,(name,k,expected_k)
    rows=layer_data(J,k,dom)
    for j,prefix in expected_h.items():
        actual=rows[j-1]["hilbert"][:len(prefix)]
        assert actual==prefix,(name,j,actual,prefix)
    assert not denominators_nonzero_at_origin(rows,params)

    return {
        "name":name,
        "stabilizer_dimension":stabdim,
        "chi_orbit_rank":orbit_rank,
        "slice_positions":slice_positions,
        "slice_matrix_entries":[[i//3,i%3] for i in slice_positions],
        "first_delta_power":k,
        "layers":rows,
    }

B3={
"secant":sp.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,0]]),
"tangent":sp.Matrix([[0,1,-1,0],[0,0,0,1],[0,0,0,0]]),
"H_ruling":sp.Matrix([[0,0,1,0],[0,0,0,1],[0,0,0,0]]),
"W_ruling":sp.Matrix([[0,1,0,0],[0,0,0,1],[0,0,0,0]]),
"dual_rank_2":sp.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0]]),
"dual_rank_1":sp.Matrix([[1,0,0,0],[0,0,0,0],[0,0,0,0]]),
"zero":sp.zeros(3,4),
}
C3={
"secant":sp.Matrix([[1,2,-2],[-2,-1,1],[-2,1,-2]]),
"tangent":sp.Matrix([[1,-2,-1],[0,1,0],[-1,-2,2]]),
"H_ruling":sp.Matrix([[1,-1,-1],[1,1,-1],[2,-1,0]]),
"W_ruling":sp.Matrix([[1,-1,1],[2,1,2],[1,0,-2]]),
"dual_rank_2":sp.Matrix([[-2,1,-1],[0,0,-2],[-2,0,-1]]),
"dual_rank_1":sp.Matrix([[-2,2,-1],[1,1,1],[2,1,-2]]),
"zero":sp.eye(3),
}

MIXED_CASES=[
("secant",B3["secant"],C3["secant"],[0,3,6],2,{2:[1,4,3,0]}),
("tangent",B3["tangent"],C3["tangent"],[0,3],2,{2:[1,4,3,0]}),
("H_ruling",B3["H_ruling"],C3["H_ruling"],[0,2],3,{2:[1,4,6,4,0],3:[1,0]}),
("W_ruling",B3["W_ruling"],C3["W_ruling"],[],2,{2:[1,4,6,4,5,6,7,8]}),
("dual_rank_2",B3["dual_rank_2"],C3["dual_rank_2"],[],3,{2:[1,4,9,8,10,12,14],3:[1,0]}),
("dual_rank_1",B3["dual_rank_1"],C3["dual_rank_1"],[],3,{2:[1,4,9,12,15,18,21],3:[1,2,0]}),
("zero",B3["zero"],C3["zero"],[],3,{2:[1,4,9,16,25,36],3:[1,4,9,16,25,36]}),
]

RANKDROP={
(2,4):{
"C":[[-2,1,3],[3,3,-3],[-1,-3,0],[3,0,0]],
"slice":[0,1,2,4,6],"k":2,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,8,0]}},
(2,3):{
"C":[[2,0,3],[-2,-3,0],[-3,3,0],[0,1,3]],
"slice":[0,1,3,4],"k":3,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,8,5,0],3:[1,0]}},
(2,2):{
"C":[[3,-3,2],[0,-1,2],[3,-2,1],[-3,-1,-3]],
"slice":[6],"k":3,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,20,24],3:[1,4,3,0]}},
(2,1):{
"C":[[-3,-3,2],[1,-3,0],[2,-2,0],[2,-3,1]],
"slice":[],"k":4,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,9,16,25,36],4:[1,0]}},
(1,4):{
"C":[[-2,3,0],[0,1,-2],[-1,-2,2],[-2,3,0],[-1,-3,0]],
"slice":[0,2,6],"k":4,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,6,0],4:[1,0]}},
(1,3):{
"C":[[3,1,2],[-3,-2,2],[2,3,-1],[-3,2,-1],[2,2,1]],
"slice":[0],"k":4,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,9,8,10,12],4:[1,0]}},
(1,2):{
"C":[[0,1,3],[2,-2,-1],[-1,1,0],[3,1,0],[1,3,-3]],
"slice":[],"k":4,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,9,16,25,36],4:[1,4,6,8,10,12]}},
(0,4):{
"C":[[0,-2,2],[3,0,0],[2,-2,-1],[1,2,3],[2,2,-1],[-3,0,2]],
"slice":[],"k":5,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,9,16,25,36],4:[1,4,6,8,10,12],5:[1,0]}},
(0,3):{
"C":[[1,-3,3],[-2,1,3],[0,-1,0],[2,-3,0],[-3,-1,2],[3,1,1]],
"slice":[],"k":5,
"h":{1:[1,4,9,16,25,36],2:[1,4,9,16,25,36],3:[1,4,9,16,25,36],4:[1,4,9,16,25,36],5:[1,0]}},
}

def generic_B(q,b_rank):
    B=sp.zeros(q,4)
    if b_rank==4:
        for i in range(4):
            B[i,i]=1
    elif b_rank==3:
        B[:3,:]=sp.Matrix([[0,1,0,0],[0,0,1,0],[1,0,0,-1]])
    elif b_rank==2:
        B[:3,:]=B3["secant"]
    elif b_rank==1:
        B[:3,:]=B3["dual_rank_2"]
    else:
        raise ValueError(b_rank)
    return B

def numeric_colon(I,f):
    return colon(I,f,sp.QQ)

def numeric_layer(J,j):
    K=J
    for _ in range(j-1):
        K=numeric_colon(K,delta)
    return K+[delta]

u0,u1,v0,v1=sp.symbols("u0 u1 v0 v1")
RANK_ONE_SUBS={a:u0*v0,b:u0*v1,c:u1*v0,d:u1*v1}

def rank_one_common_factor(I):
    polys=[
        sp.factor(sp.expand(f.subs(RANK_ONE_SUBS)))
        for f in I
        if sp.expand(f.subs(RANK_ONE_SUBS))!=0
    ]
    g=polys[0]
    for f in polys[1:]:
        g=sp.gcd(g,f)
    return sp.factor(g)

def ideal_hilbert(I,dom,nmax=10):
    G=sp.groebner(I,*VARS,order="grevlex",domain=dom)
    lms=[tuple(p.LM(order=G.order).exponents) for p in G.polys]
    return hilbert_from_lms(lms,nmax)

def generic_rankdrop_layer(pair,j):
    aa,bb=pair
    data=RANKDROP[pair]
    params=sp.symbols(f"r0:{len(data['slice'])}")
    C=sp.Matrix(data["C"])
    for par,idx in zip(params,data["slice"]):
        C[idx//3,idx%3]+=par
    dom=sp.QQ.frac_field(*params) if params else sp.QQ
    B=generic_B(6-aa,bb)
    J=residual_ideal(B,C)
    K=J
    for _ in range(j-1):
        K=colon(K,delta,dom)
    return params,dom,K+[delta]

def proportional_over_slice(f,g):
    ratio=sp.cancel(f/g)
    return ratio!=0 and not ratio.has(u0,u1,v0,v1)

def quadratic_ruling_ideal(q,dom):
    P=sp.Poly(q,u0,u1,domain=dom)
    A=P.coeff_monomial(u0**2)
    B=P.coeff_monomial(u0*u1)
    C=P.coeff_monomial(u1**2)
    return [
        delta,
        sp.expand(A*a*a+B*a*c+C*c*c),
        sp.expand(A*a*b+B*a*d+C*c*d),
        sp.expand(A*b*b+B*b*d+C*d*d),
    ]

def run():
    mixed=[]
    for args in MIXED_CASES:
        mixed.append(generic_slice_case(*args))

    rankdrop=[]
    for (aa,bb),data in RANKDROP.items():
        q=6-aa
        B=generic_B(q,bb)
        C=sp.Matrix(data["C"])
        rankdrop.append(generic_slice_case(
            f"a{aa}_b{bb}",B,C,data["slice"],data["k"],data["h"]
        ))

    # Generic ruling factors over the same fraction fields as the
    # Groebner bases.  This distinguishes genuine generic support
    # information from a special integral witness.
    p22,dom22,I22=generic_rankdrop_layer((2,2),2)
    s0=p22[0]
    f22=rank_one_common_factor(I22)
    q22=u0*u1*((s0+9)*u0**2+(3*s0+6)*u0*u1-7*u1**2)
    assert proportional_over_slice(f22,q22)
    disc22=sp.factor(sp.discriminant(
        (s0+9)*u0**2+(3*s0+6)*u0*u1-7*u1**2,u0
    ).subs(u1,1))
    assert disc22 == 9*s0**2+64*s0+288

    p13,dom13,I13=generic_rankdrop_layer((1,3),3)
    t0=p13[0]
    f13=rank_one_common_factor(I13)
    q13=10*u0**2+u0*u1-4*u1**2
    assert proportional_over_slice(f13,q13)
    disc13=sp.factor(sp.discriminant(q13,u0).subs(u1,1))
    assert disc13 == 161

    # Exact saturation model for the generic (1,3) embedded vertex.
    Sat13=quadratic_ruling_ideal(q13,dom13)
    Gsat=sp.groebner(Sat13,*VARS,order="grevlex",domain=dom13)
    assert all(sp.expand(Gsat.reduce(f)[1])==0 for f in I13)
    hI=ideal_hilbert(I13,dom13,10)
    hSat=ideal_hilbert(Sat13,dom13,10)
    diff=[x-y for x,y in zip(hI,hSat)]
    assert diff[:4] == [0,0,3,0]
    assert all(x==0 for x in diff[3:])
    embedded_length=sum(diff)
    assert embedded_length==3

    # The remaining positive-dimensional rows have open stabilizer
    # orbit in chi-space, so an integral base point is generic there.
    open_factors={}
    for pair,j in [((1,2),4),((0,4),4)]:
        aa,bb=pair
        B=generic_B(6-aa,bb)
        C=sp.Matrix(RANKDROP[pair]["C"])
        J=residual_ideal(B,C)
        K=J
        for _ in range(j-1):
            K=numeric_colon(K,delta)
        open_factors[f"a{aa}_b{bb}_W{j}"]=str(rank_one_common_factor(K+[delta]))

    # This checks only the horizontal-strip combinatorics.  The actual
    # coordinate-ring structure constant is proved by standard
    # bitableau straightening in the manuscript.
    lam=(4,4,4,0)
    nu=(4,4,4,4)
    added=[]
    for row,(x0,y0) in enumerate(zip(lam,nu)):
        added.extend((row,col) for col in range(x0+1,y0+1))
    columns=[col for _,col in added]
    assert len(added)==4 and len(set(columns))==4

    out={
        "kind":"exact rational-function-field Groebner and stabilizer certificate",
        "scope":{
            "script_checks":"finite exact algebra only",
            "structural_proofs_not_machine_certified":[
                "bounded principal-colon base change theorem",
                "geometric relative-assassin stratification",
                "coordinate-ring Cauchy-Pieri projection",
            ],
        },
        "mixed_kernel_generic_slices":mixed,
        "rankdrop_generic_slices":rankdrop,
        "generic_rank_one_factors":{
            "a2_b2_W2":{
                "field":str(dom22),
                "factor":str(sp.factor(q22)),
                "quadratic_discriminant":str(disc22),
                "noncollision_divisor":str(sp.factor((s0+9)*disc22)),
            },
            "a1_b3_W3":{
                "field":str(dom13),
                "factor":str(sp.factor(q13)),
                "discriminant":str(disc13),
            },
        },
        "generic_embedded_saturation":{
            "a1_b3_W3":{
                "saturated_ideal":[str(sp.factor(x)) for x in Sat13],
                "layer_hilbert":hI,
                "saturation_hilbert":hSat,
                "quotient_hilbert":diff,
                "embedded_vertex_length":embedded_length,
            }
        },
        "open_orbit_rank_one_factors":open_factors,
        "pieri_horizontal_strip_combinatorics_only":True,
        "universal_det_exponent_e4_r2":sp.binomial(5,1),
    }
    evidence=Path(__file__).resolve().parents[1]/"evidence"
    evidence.mkdir(exist_ok=True)
    (evidence/"GENERIC_BOUNDARY_CERTIFICATES.json").write_text(
        json.dumps(out,indent=2,default=str)+"\n",encoding="utf-8"
    )
    print(json.dumps(out,indent=2,default=str))

if __name__=="__main__":
    run()
