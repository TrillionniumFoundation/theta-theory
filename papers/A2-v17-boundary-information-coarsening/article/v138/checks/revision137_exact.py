#!/usr/bin/env python3
"""Finite exact regressions for v137. Not verification of general scheme proofs."""
from pathlib import Path
import itertools, json, math
import sympy as S
ROOT=Path(__file__).resolve().parents[1]

def compositions(total,n):
    if n==1:
        yield (total,);return
    for a in range(total+1):
        for b in compositions(total-a,n-1):yield (a,)+b

def mono(xs,aa):return S.prod(x**a for x,a in zip(xs,aa))

# Linearized equations u wedge A(u)=0: basis vectors and pairwise sums.
fano=[]
for n in range(2,8):
    av=S.symbols('a:'+str(n*n));A=S.Matrix(n,n,av);eqs=[]
    us=[S.eye(n)[:,i] for i in range(n)]
    us += [S.eye(n)[:,i]+S.eye(n)[:,j] for i in range(n) for j in range(i+1,n)]
    for u in us:
        v=A*u
        eqs.extend(u[i]*v[j]-u[j]*v[i] for i in range(n) for j in range(i+1,n))
    mat,_=S.linear_eq_to_matrix(eqs,av);rank=mat.rank()
    assert rank==n*n-1
    fano.append({'n':n,'one_transverse_coordinate_rank':rank,'ruling_tangent_dimension':(n-1)*(n*n-rank)})

# Full-group lemma's radial harmonic recurrence and distinct Casimir scalars.
z,r=S.symbols('z r');harmonics=[]
for n in range(2,9):
    for a in range(11):
        cs=[S.Integer(1)]
        for j in range(a//2):
            cs.append(-S.Rational((a-2*j)*(a-2*j-1),2*(j+1)*(2*j+n-1))*cs[-1])
        p=sum(c*z**(a-2*j)*r**j for j,c in enumerate(cs))
        lap=S.expand(S.diff(p,z,2)+4*r*S.diff(p,r,2)+2*(n-1)*S.diff(p,r))
        assert lap==0
        harmonics.append({'n':n,'degree':a,'fixed_space_recurrence_checked':True})
    assert len({a*(a+n-2) for a in range(11)})==11

# Exact coefficient injections; no random sampling, floating ranks, or tolerances.
polar=[]
for n,d in [(2,1),(2,2),(2,3),(3,2),(3,3),(3,4)]:
    xs=S.symbols('x:'+str(n));us=S.symbols('u:'+str(n))
    ts=S.symbols('t:'+str(n*n));T=S.Matrix(n,n,ts);Tu=T*S.Matrix(us)
    aa=list(compositions(d,n));ambient=list(compositions(d,n*n));index={a:i for i,a in enumerate(ambient)}
    columns=[]
    for a in aa:
        p=S.Poly(S.expand(mono(Tu,a)),*us)
        for b in aa:
            q=S.Poly(p.coeff_monomial(mono(us,b)),*ts)
            columns.append({index[e]:c for e,c in q.terms()})
    entries={(i,j):c for j,col in enumerate(columns) for i,c in col.items()}
    mat=S.MutableSparseMatrix(len(ambient),len(columns),entries)
    # DomainMatrix rank is exact over QQ; rational coefficient matrix only.
    rank=mat.to_DM().convert_to(S.QQ).rank()
    assert rank==len(aa)**2
    for k in (1,min(2,len(aa))):
        restricted=mat[:,:k*len(aa)]
        assert restricted.to_DM().convert_to(S.QQ).rank()==k*len(aa)
    polar.append({'n':n,'d':d,'ambient_dimension':len(ambient),'coefficient_rank':rank,'expected_rank':len(aa)**2})

# Independently expand the two routes of a nontrivial common-g/right-h substitution.
u,v=S.symbols('u v');a,b,c,e=S.symbols('a b c e');T=S.Matrix([[a,b],[c,e]])
g=S.Matrix([[1,1],[1,2]]);h=S.Matrix([[2,1],[1,1]]);uv=S.Matrix([u,v])
f=lambda q:q[0]**3+2*q[0]*q[1]**2+3*q[1]**3
left=S.expand(f(g*T*h.inv()*uv))
fg=f(g*uv);right=S.expand(fg.subs({u:(T*h.inv()*uv)[0],v:(T*h.inv()*uv)[1]},simultaneous=True))
assert left==right

# Block Fitting minors, and the explicit nilpotency-three polar example.
delta=a*e-b*c;A=a*a+c*c;B=a*b+c*e;C=b*b+e*e
Psi=S.Matrix([[delta,0,0,0],[0,A,2*B,C]])
minors=[S.expand(Psi[:,list(j)].det()) for j in itertools.combinations(range(4),2)]
assert minors[:3]==[S.expand(delta*A),S.expand(2*delta*B),S.expand(delta*C)]
assert all(x==0 for x in minors[3:])
assert S.expand(A*C-B**2-delta**2)==0
mons=list(compositions(2,4));xx=(a,b,c,e)
col=lambda p:S.Matrix([S.Poly(p,*xx).coeff_monomial(mono(xx,k)) for k in mons])
M=S.Matrix.hstack(*(col(p) for p in (A,B,C)))
assert M.rank()==3 and M.row_join(col(delta)).rank()==4
# Multiplication by determinant over dual numbers in a finite-degree truncation.
small=[aa for deg in range(4) for aa in compositions(deg,4)]
large=[aa for deg in range(2,6) for aa in compositions(deg,4)];ix={aa:i for i,aa in enumerate(large)}
MM=S.zeros(len(large),len(small))
for j,aa in enumerate(small):
    for power,coef in S.Poly(S.expand(delta*mono(xx,aa)),*xx).terms():MM[ix[power],j]=coef
assert MM.rank()==len(small)
dual_rank=2*MM.rank();assert dual_rank==2*len(small)

# Explicit nondiagonal relation spaces, including n=5 and even n.
webs=[]
for n in range(4,9):
    x=S.symbols('x:'+str(n));q=[x[0]**2+x[1]*x[2]]+[y*y for y in x[1:]]
    jac=S.Matrix([[S.diff(qi,y) for y in x] for qi in q]).det()
    assert S.expand(jac-2**n*S.prod(x))==0
    deriv=[S.Poly(S.diff(jac,y),*x) for y in x]
    assert len({p.monoms()[0] for p in deriv})==n
    webs.append({'n':n,'essential_variables':n,'exterior_support':n*(n+1)//2,'rank_one_quadric_points':n-1})
a1,t=S.symbols('a1 t');nonprincipal_minor=S.det(S.Matrix([[a1,0],[0,a1*t/2]]))
assert nonprincipal_minor==a1*a1*t/2

checks={'fano_tangent_regressions':True,'harmonic_recurrence_77_cases':len(harmonics)==77,
'polar_coefficient_injections_six_cases':len(polar)==6,'nontrivial_two_sided_naturality':True,
'block_fitting_and_nilpotency_three':True,'dual_number_determinant_truncation':True,
'nondiagonal_uniform_webs_five_dimensions':len(webs)==5}
out={'revision':137,'ok':all(checks.values()),'checks':checks,'fano':fano,
'harmonic_cases':len(harmonics),'polar_injections':polar,'dual_number_truncation_rank':dual_rank,
'nondiagonal_webs':webs,'structural_proofs_not_machine_certified':[
'relative Fano scheme identification and arbitrary base change','full orthogonal-group harmonic irreducibility',
'intrinsic common-coordinate descent and coefficient criterion','abstract polar-system Torelli theorem',
'general contraction and support theorems','historical priority and Ballico theorem comparison']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION137_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
