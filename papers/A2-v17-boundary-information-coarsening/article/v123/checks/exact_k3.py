"""Exact finite certificates for the explicit v123 member (not a general proof checker).
Run with Python 3, SymPy and NumPy; no network or random choices are used.
The residue computations certify nonzero integer minors over characteristic zero.
"""
from pathlib import Path
import sympy as s, numpy as np, json, time
x=s.symbols('x0:4'); cross=[x[i]*x[j] for i in range(4) for j in range(i+1,4)]
C=s.Matrix([[2,-1,2,0],[-2,0,-1,1],[2,-1,-2,0],[1,-1,2,1],[1,-1,0,0],[1,-2,1,-2]])
Q=[s.expand(x[i]**2+sum(C[j,i]*cross[j] for j in range(6))) for i in range(4)]
J=s.Matrix(Q).jacobian(x); F=s.expand(J.det(method='domain-ge'))
def exps(d,n=4):
 if n==1: return [(d,)]
 return [(a,)+r for a in range(d,-1,-1) for r in exps(d-a,n-1)]
def vec(poly,d):
 D=s.Poly(poly,*x).as_dict(); return [int(D.get(e,0)) for e in exps(d)]
def rank_certificate(M,prime=101):
 A=np.array(M,dtype=np.int64)%prime
 m,n=A.shape; rowperm=list(range(m)); rows=[];cols=[];rank=0
 for j in range(n):
  hits=np.flatnonzero(A[rank:,j]);
  if not len(hits): continue
  k=rank+int(hits[0]); A[[rank,k]]=A[[k,rank]]; rowperm[rank],rowperm[k]=rowperm[k],rowperm[rank]
  rows.append(rowperm[rank]);cols.append(j)
  A[rank]=(A[rank]*pow(int(A[rank,j]),-1,prime))%prime
  A[rank+1:]=(A[rank+1:]-A[rank+1:,j,None]*A[rank])%prime
  rank+=1
  if rank==m:break
 B=np.array(M,dtype=np.int64)[np.ix_(rows,cols)]%prime; det=1
 for j in range(rank):
  hits=np.flatnonzero(B[j:,j]); k=j+int(hits[0]);
  if k!=j: B[[j,k]]=B[[k,j]];det=-det
  pivot=int(B[j,j]);det=det*pivot%prime;B[j]=B[j]*pow(pivot,-1,prime)%prime
  B[j+1:]=(B[j+1:]-B[j+1:,j,None]*B[j])%prime
 return {'prime':prime,'shape':[m,n],'rank':rank,'rows_zero_based':rows,'columns_zero_based':cols,'minor_determinant_mod_prime':int(det%prime)}
def macaulay(polys,d):
 mons=exps(d); idx={e:i for i,e in enumerate(mons)}; cols=[]
 for q in polys:
  D=s.Poly(q,*x).as_dict(); degree=s.Poly(q,*x).total_degree()
  for beta in exps(d-degree):
   col=[0]*len(mons)
   for alpha,c in D.items():col[idx[tuple(a+b for a,b in zip(alpha,beta))]]+=int(c)
   cols.append(col)
 return np.array(cols,dtype=np.int64).T
cof=J.cofactor_matrix()
derivatives=[s.expand(sum(cof[i,j]*s.diff(cross[k],x[j]) for j in range(4))) for i in range(4) for k in range(6)]
D=np.array([vec(F,4)]+[vec(f,4) for f in derivatives],dtype=np.int64).T
print('Quartic',F,flush=True)
print('derivative',rank_certificate(D),flush=True)
base=rank_certificate(macaulay(Q,5));print('basepoint',base['rank'],base['minor_determinant_mod_prime'],flush=True)
smooth=rank_certificate(macaulay([s.diff(F,a) for a in x],9));print('smooth',smooth['rank'],smooth['minor_determinant_mod_prime'],flush=True)
# H = <x0,x1>, W = <x2,x3>; quotient gamma in square-first basis
mons=[v*v for v in x]+cross; gamma=(-C).row_join(s.eye(6))
def gv(q):return gamma*s.Matrix([s.Poly(q,*x).coeff_monomial(m) for m in mons])
A=s.Matrix.hstack(gv(x[0]**2),gv(x[0]*x[1]),gv(x[1]**2))
B=s.Matrix.hstack(*[gv(x[i]*x[j]) for i in (0,1) for j in (2,3)])
AC=s.Matrix.hstack(*[gv(x[2]**2),gv(x[2]*x[3]),gv(x[3]**2)])
L=s.Matrix.vstack(*[v.T for v in A.T.nullspace()]); Bb=L*B;Cc=L*AC
ker=Bb.nullspace();detkernel=s.Matrix(2,2,list(ker[0])).det() if len(ker)==1 else 0
u,v=s.symbols('u v'); h=s.factor(s.Matrix.hstack(Bb[:,0]*u+Bb[:,1]*v,Bb[:,2]*u+Bb[:,3]*v,Cc*s.Matrix([u*u,2*u*v,v*v])).det())
print('A rank',A.rank(),'B rank',Bb.rank(),'kernel det',detkernel,'h',h,flush=True)
print('h discrim',s.discriminant(h.subs(v,1),u),flush=True)
record={'field':'QQ with exact reduction certificates over GF(101)','quadrics':[str(q) for q in Q],'quartic':str(F),'cross_matrix':C.tolist(),'quartic_monomial_order':[list(e) for e in exps(4)],'derivative_order':'F, then row i=0..3, cross k=(01,02,03,12,13,23)','immersion':rank_certificate(D),'basepoint_degree5':base,'smoothness_degree9':smooth,'corank_two_witness':{'A':A.tolist(),'left_quotient':L.tolist(),'B':Bb.tolist(),'C':Cc.tolist(),'kernel_vector':list(ker[0]),'kernel_determinant':str(detkernel),'ramification_binary_quartic':str(h),'discriminant':str(s.discriminant(h.subs(v,1),u))}}

assert record['immersion']['rank'] == 25
assert base['rank'] == 56 and base['minor_determinant_mod_prime'] == 44
assert smooth['rank'] == 220 and smooth['minor_determinant_mod_prime'] == 79
exact_det = int(s.Matrix(D[:25, :]).det(method='domain-ge'))
assert exact_det == 4279473148893659522379284480
assert exact_det % 101 == 41
assert A.rank() == 3 and Bb.rank() == 3
assert detkernel == -7
assert s.discriminant(h.subs(v,1),u) == -s.Rational(632301,4)
record['first_25_rows_exact_determinant'] = str(exact_det)
record['first_25_rows_minor_mod_101'] = 41
record['finite_witness_checks_passed'] = True
record['general_proof_machine_certified'] = False

(Path(__file__).resolve().parents[1]/'evidence'/'K3_CERTIFICATES.json').write_text(json.dumps(record,indent=2,default=str)+'\n')

