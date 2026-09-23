"""Exact regression certificates for the v125 stratified rank-two algebra.

These are rational symbolic regressions for explicit coefficient choices.
The general statements are proved in the manuscript; this script is not a
general proof checker.  No random choices, network access, or floating point
arithmetic are used.
"""
from pathlib import Path
import itertools, json
import sympy as s

a,b,c,d,u,v=s.symbols("a b c d u v")
z=(a,b,c,d)
delta=a*d-b*c
L=s.Matrix([[a,b,0,0],[c,d,a,b],[0,0,c,d]])
ST=s.Matrix([
    [a*a,a*b,b*b],
    [2*a*c,a*d+b*c,2*b*d],
    [c*c,c*d,d*d],
])

def minors3(M):
    return [s.expand(M[:,inds].det())
            for inds in itertools.combinations(range(M.cols),3)]

def power(gens,n):
    return [s.prod(t) for t in
            itertools.combinations_with_replacement(gens,n)]

def intersection(A,B):
    t=s.Dummy("t")
    gb=s.groebner(
        [t*f for f in A]+[(1-t)*f for f in B],
        t,*z,order="lex",domain=s.QQ,
    )
    return [p.as_expr() for p in gb.polys if not p.as_expr().has(t)]

def same(A,B):
    GA=s.groebner(A,*z,order="grevlex",domain=s.QQ)
    GB=s.groebner(B,*z,order="grevlex",domain=s.QQ)
    return (
        all(GA.reduce(f)[1] == 0 for f in B)
        and all(GB.reduce(f)[1] == 0 for f in A)
    )

# A mixed-regular repeated-contact witness:
# h(u,v)=u^2(u-v)(u-2v).
C_rep=s.Matrix([[0,0,0],[0,0,0],[1,s.Rational(-3,2),2]])
M_rep=L.row_join(C_rep*ST)
J_rep=minors3(M_rep)
I_rep=[delta]+J_rep
h_rep=s.expand(
    s.Matrix.hstack(
        s.Matrix([u,v,0]),
        s.Matrix([0,u,v]),
        C_rep*s.Matrix([u*u,2*u*v,v*v]),
    ).det()
)
assert s.factor(h_rep) == u**2*(u-v)*(u-2*v)
assert same(J_rep, intersection(I_rep,power(list(z),3)))
assert same(
    [delta*f for f in J_rep],
    intersection([delta*f for f in I_rep],power(list(z),5)),
)

# The containment witness h == 0 has J=delta*m and
# delta*J=(delta^2) cap m^5.
J_zero=minors3(L)
assert same(J_zero,[delta*w for w in z])
assert same(
    [delta*f for f in J_zero],
    intersection([delta**2],power(list(z),5)),
)

# First non-mixed-regular wall: decomposable one-dimensional mixed kernel.
L_dec=s.Matrix([[c,d,0,0],[0,0,a,b],[0,0,c,d]])
C_dec=s.Matrix([[0,2,3],[0,5,7],[1,11,13]])
J_dec=minors3(L_dec.row_join(C_dec*ST))
K_dec=[c,d,a*a,a*b,b*b]
assert same(minors3(L_dec),[delta*c,delta*d])
G_dec=s.groebner(J_dec,*z,order="grevlex",domain=s.QQ)
assert all(G_dec.reduce(delta*k)[1] == 0 for k in K_dec)
assert G_dec.reduce(delta)[1] != 0
assert G_dec.reduce(delta**2)[1] == 0

# Modulo K_dec every class is represented by lambda+mu*a+nu*b.
# The three products delta, a*delta, b*delta remain independent modulo J_dec,
# which is the finite-dimensional degree check used in the colon proof.
remainders=[
    s.expand(G_dec.reduce(delta)[1]),
    s.expand(G_dec.reduce(a*delta)[1]),
    s.expand(G_dec.reduce(b*delta)[1]),
]
mons=sorted(set().union(*(s.Poly(r,*z).monoms() for r in remainders)))
mat=s.Matrix([
    [s.Poly(r,*z).coeff_monomial(m) for r in remainders]
    for m in mons
])
assert mat.rank() == 3

record={
    "field":"QQ",
    "general_proof_machine_certified":False,
    "repeated_contact":{
        "binary_quartic":str(s.factor(h_rep)),
        "J_equals_Icap_m3":True,
        "deltaJ_equals_deltaIcap_m5":True,
    },
    "containment":{
        "h_identically_zero":True,
        "J_equals_delta_m":True,
        "delta2m_equals_delta2_cap_m5":True,
    },
    "decomposable_kernel_wall":{
        "linear_minor_ideal":"delta*(c,d)",
        "expected_colon_generators":["c","d","a^2","a*b","b^2"],
        "delta_times_expected_colon_in_J":True,
        "delta_not_in_J":True,
        "delta_squared_in_J":True,
        "quotient_length_at_vertex":3,
        "degree_test_rank":int(mat.rank()),
    },
}
out=Path(__file__).resolve().parents[1]/"evidence"/"STRATIFIED_CERTIFICATES.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))
