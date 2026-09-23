"""Rational regression of the corank-two primary formula for four split simple roots.
This checks an explicit tensor, not all coefficient rings. The general proof is in section 6.
Run with Python 3 and SymPy. No network or floating-point computation is used.
"""
import sympy as s,itertools,json
from pathlib import Path
a,b,c,d,u,v=s.symbols('a b c d u v'); z=(a,b,c,d); delta=a*d-b*c
T=s.Matrix([[a,b],[c,d]])
# B(h1*u)=u1 z1+u2 z2, B(h2*u)=u1 z2+u2 z3.
L=s.Matrix([[a,b,0,0],[c,d,a,b],[0,0,c,d]])
# h=u^2*C3(u)-u*v*C2(u)+v^2*C1(u).
# h = u*v*(u-v)*(u-2*v) = u^3*v-3*u^2*v^2+2*u*v^3.
C=s.Matrix([[0,1,0],[0,0,0],[0,s.Rational(1,2),-3]])
ST=s.Matrix([[a*a,a*b,b*b],[2*a*c,a*d+b*c,2*b*d],[c*c,c*d,d*d]])
M=L.row_join(C*ST)
mins=[s.expand(M[:,inds].det()) for inds in itertools.combinations(range(7),3)]
gens=[delta*w for w in z]
# lifts h(u)*v1^(4-k)*v2^k obtained by coefficients of rank-one minor quotient
G=s.groebner(mins,*z,order='grevlex',domain=s.QQ)
# Pi image lines 0, infinity, 1, 2 (u/v roots)
Ps=[[a,b],[c,d],[a-c,b-d],[a-2*c,b-2*d]]
def intersection(A,B):
 t=s.Dummy('t');gb=s.groebner([t*f for f in A]+[(1-t)*f for f in B],t,*z,order='lex',domain=s.QQ)
 return [p.as_expr() for p in gb.polys if not p.as_expr().has(t)]
def power(P,n):return [s.prod(t) for t in itertools.combinations_with_replacement(P,n)]
def same(A,B):
 GA=s.groebner(A,*z,order='grevlex',domain=s.QQ);GB=s.groebner(B,*z,order='grevlex',domain=s.QQ)
 return all(GA.reduce(f)[1]==0 for f in B) and all(GB.reduce(f)[1]==0 for f in A)
I=Ps[0]
for P in Ps[1:]:I=intersection(I,P)
J=intersection(I,power(list(z),3))
assert same(mins,J)
F=[delta*f for f in mins]
primary=[delta]
for P in Ps:primary=intersection(primary,power(P,2))
primary=intersection(primary,power(list(z),5))
assert same(F,primary)
FG=s.groebner(F,*z,order='grevlex',domain=s.QQ)
assert FG.reduce(delta**2)[1]!=0
assert FG.reduce(delta**3)[1]==0
assert all(FG.reduce(w*delta**2)[1]==0 for w in z)
# Standard symmetrization linear minors are delta times all four vars
assert same([s.expand(L[:,inds].det()) for inds in itertools.combinations(range(4),3)],gens)
h=s.expand(s.Matrix.hstack(s.Matrix([u,v,0]),s.Matrix([0,u,v]),C*s.Matrix([u*u,2*u*v,v*v])).det())
assert s.expand(h-u*v*(u-v)*(u-2*v)) == 0
print('h actual',s.factor(h))
# N.B. coordinates Sym^2 coefficient uv: L convention has product u1*u2 coefficient 2 in square.
print('PASS',len(list(G)), 'delta-square normal form',FG.reduce(delta**2)[1])
(Path(__file__).resolve().parents[1]/'evidence'/'CORANK2_CERTIFICATES.json').write_text(json.dumps({'primary_identity':True,'h':str(s.factor(h)),'nilradical_index':3,'nilradical_square_length':1,'field':'QQ','general_proof_machine_certified':False,'four_simple_roots':True,'basis_linear_block':[[str(t) for t in row] for row in L.tolist()],'C':C.tolist()},indent=2,default=str))
