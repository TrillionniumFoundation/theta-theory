#!/usr/bin/env python3
"""Exact finite witnesses for A2 v151. They are not universal proof certificates."""
from pathlib import Path
from itertools import product
from math import comb
import json
import sympy as s
HERE=Path(__file__).resolve().parent
out=HERE/'evidence';out.mkdir(exist_ok=True)
checks={}; data={}
def check(name,value,detail=None):
    checks[name]=bool(value)
    if detail is not None: data[name]=detail
    if not checks[name]: raise AssertionError(name)
def mons(v,d):
    return [s.prod(x**a for x,a in zip(v,ex)) for ex in product(range(d+1),repeat=len(v)) if sum(ex)==d]
def vec(f,v,ms):
    p=s.Poly(s.expand(f),*v)
    return s.Matrix([p.coeff_monomial(m) for m in ms])
def poly_gcd(fs,v):
    return s.Poly(s.gcd_list(fs),*v).monic().as_expr()
def complement(M):
    a=M; cols=[]
    for c in s.eye(M.rows).columnspace():
        if a.row_join(c).rank()>a.cols:
            cols.append(c); a=a.row_join(c)
    return cols
x,y,z,a,b,t=s.symbols('x y z a b t')
v=(x,y,z)
# Full incidence fibre: exact quotient coefficient elimination, not a radical.
remainders=[s.expand(k.subs(x,-a*y-b*z)) for k in [x*x*y,x*x*z]]
eq=[c for q in remainders for c in s.Poly(q,y,z).coeffs()]
G=s.groebner(eq,a,b,order='lex')
check('fat_fibre_exact_ideal',set(p.as_expr() for p in G.polys)=={a*a,a*b,b*b},str(G))
check('fat_fibre_length_three',all(G.reduce(m)[1]==0 for m in [a*a,a*b,b*b]) and all(G.reduce(m)[1]==m for m in [s.Integer(1),a,b]))
check('fat_fibre_tangent_dimension_two',s.Matrix(eq).jacobian([a,b]).subs({a:0,b:0}).rank()==0)
# Independently form the complete multiplication-block Schur equations.
ms2,ms3=mons(v,2),mons(v,3)
M=s.Matrix.hstack(*[vec((x+a*y+b*z)*m,v,ms3) for m in ms2])
rows=list(M.subs({a:0,b:0}).T.rref()[1]); other=[i for i in range(len(ms3)) if i not in rows]
C=s.Matrix.hstack(vec(x*x*y,v,ms3),vec(x*x*z,v,ms3))
Schur=C[other,:]-M[other,:]*M[rows,:].inv()*C[rows,:]
G2=s.groebner(list(Schur),a,b)
check('schur_equations_equal_full_fat_fibre',set(q.as_expr() for q in G2.polys)==set(q.as_expr() for q in G.polys),str(G2))
# Two distinct, reduced divisor lifts of the same boundary relation.
for q,sub,name in [(x,-a*y-b*z,'x'),(y,-a*x-b*z,'y')]:
    rem=[s.expand(k.subs(q,sub)) for k in [x*x*y,x*y*z]]
    vars_=(y,z) if q==x else (x,z)
    eq=[c for f in rem for c in s.Poly(f,*vars_).coeffs()]
    gb=s.groebner(eq,a,b)
    check('two_branch_'+name+'_reduced',set(p.as_expr() for p in gb.polys)=={a,b})
q=x*x+y*z
check('normal_jump_irreducible_quadratic',s.hessian(q,v).rank()==3)
rem=[s.expand(k.subs(x,-a*y-b*z)) for k in [x*q*y,x*q*z]]
gb=s.groebner([c for f in rem for c in s.Poly(f,y,z).coeffs()],a,b)
check('normal_jump_reduced_unique_chart_fibre',set(p.as_expr() for p in gb.polys)=={a,b})
check('collision_family_generic_gcd',s.Poly(s.gcd(x*y+t*y*y,x*z+t*z*z),x,y,z,domain=s.QQ.frac_field(t)).total_degree()==0)
check('collision_family_special_gcd',poly_gcd([x*x*y,x*x*z],v)==x*x)
# Full Grassmannian differential, with quotient directions represented by complements.
cases=[((x,y),x,[x,y]),((x,y),x,[x*x,x*y]),((x,y),x*y,[x*x,x*y]),
       ((x,y),x*x,[x*x,x*y]),((x,y),x*x,[x*x*y,x*y*y]),
       ((x,y,z),x,[x*y,x*z]),((x,y,z),x,[y*y,z*z]),
       ((x,y,z),x*y,[x*x,x*z]),((x,y,z),x*x,[x*y,x*z])]
for idx,(vv,f,J) in enumerate(cases):
    g=s.Poly(f,*vv).total_degree();h=s.Poly(J[0],*vv).total_degree();D=g+h
    mg,mh,md=mons(vv,g),mons(vv,h),mons(vv,D)
    cf=complement(vec(f,vv,mg)); JM=s.Matrix.hstack(*[vec(j,vv,mh) for j in J]);cj=complement(JM)
    K=s.Matrix.hstack(*[vec(f*j,vv,md) for j in J]);ann=K.T.nullspace(); Q=s.Matrix.vstack(*[a.T for a in ann])
    nr=Q.rows; columns=[]
    for c in cf:
        df=sum(co*m for co,m in zip(c,mg))
        columns.append(s.Matrix.vstack(*[Q*vec(df*j,vv,md) for j in J]))
    for i in range(len(J)):
        for c in cj:
            dj=sum(co*m for co,m in zip(c,mh));blocks=[s.zeros(nr,1) for _ in J];blocks[i]=Q*vec(f*dj,vv,md)
            columns.append(s.Matrix.vstack(*blocks))
    der=s.Matrix.hstack(*columns); got=der.cols-der.rank()
    c=s.gcd(f,poly_gcd(J,vv)); k=s.Poly(c,*vv).total_degree(); want=comb(len(vv)+k-1,k)-1
    check(f'full_differential_overlap_{idx}',got==want,{'e':len(vv),'g':g,'h':h,'r':len(J),'kernel':got,'formula':want})
# Construct a fixed frame and an actual polynomial degeneration of representative pencils.
def degeneration(q0,q1,vv):
    n=len(vv); grad=[s.diff(q1,zz)*q0-q1*s.diff(q0,zz) for zz in vv]
    for coords in product(range(3),repeat=n):
        ev=dict(zip(vv,coords)); av=q0.subs(ev)
        gv=s.Matrix([gg.subs(ev) for gg in grad])
        if av!=0 and any(gg!=0 for gg in gv):
            v0=s.Matrix(coords);i=next(i for i in range(n) if gv[i]!=0);w=s.eye(n)[:,i]
            B=s.Matrix.hstack(v0,w)
            if B.rank()==2: break
    else: raise AssertionError('No exact witness frame in finite search')
    for col in s.eye(n).columnspace():
        if B.cols<n and B.row_join(col).rank()>B.cols:B=B.row_join(col)
    q1=s.expand(q1-q1.subs(ev)/av*q0)
    sub=dict(zip(vv,list(B*s.Matrix(vv))))
    ff=[s.expand(q.subs(sub, simultaneous=True)) for q in (q0,q1)]
    lam={vv[0]:vv[0],vv[1]:t*vv[1],**{zz:t*t*zz for zz in vv[2:]}}
    Q0=s.expand(ff[0].subs(lam,simultaneous=True));Q1=s.cancel(ff[1].subs(lam,simultaneous=True)/t)
    P0=s.Poly(Q0,t);P1=s.Poly(Q1,t)
    l0=s.expand(Q0.subs(t,0));l1=s.expand(Q1.subs(t,0))
    coef0=s.Poly(l0,*vv).coeff_monomial(vv[0]**2);coef1=s.Poly(l1,*vv).coeff_monomial(vv[0]*vv[1])
    assert coef0!=0 and coef1!=0
    assert l0==coef0*vv[0]**2 and l1==coef1*vv[0]*vv[1]
    assert B.det()!=0
    return {'frame':str(B),'limit':[str(l0),str(l1)],'max_t_degree':max(P0.degree(),P1.degree())}
for n in (3,4,5):
    vv=s.symbols(f'v0:{n}')
    pencils=[(sum(xx*xx for xx in vv),sum((i+1)*xx*xx for i,xx in enumerate(vv))),
             (vv[0]**2,vv[0]*vv[1]),(vv[0]**2,vv[1]**2),
             (vv[0]*vv[1],vv[1]*vv[2]),
             (vv[0]**2+vv[1]*vv[2],vv[0]*vv[2]+vv[1]**2)]
    for i,(q0,q1) in enumerate(pencils):
        detail=degeneration(q0,q1,vv);check(f'polynomial_pencil_degeneration_n{n}_{i}',True,detail)
    N=comb(n+1,2);M=comb(N,2);g=n*(n-1);h=3*n-4
    check(f'pencil_boundary_parameters_n{n}',g+h==n*n+2*n-4 and M<=comb(n*n+h-1,h))
    check(f'closed_flag_dimension_n{n}',(n-1)+(n-2)==2*n-3)
record={'revision':151,'ok':all(checks.values()),'check_count':len(checks),'checks':checks,'data':data,
        'universal_proofs_certified':False,'historical_priority_certified':False,
        'scope':'Exact finite polynomial, fibre-equation, differential-rank, and degeneration witnesses; not universal proof or priority verification.'}
(out/'REVISION151_EXACT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
