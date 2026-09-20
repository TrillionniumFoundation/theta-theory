#!/usr/bin/env python3
"""Exact A2 v100 regression, including the unrecorded v99 critical examples.

No floating-point differentiation or optimization is used. Decimal displays
on stdout are informational; every assertion uses rational arithmetic.
Python optimization (-O) is rejected because it disables assertions.
The general geometric theorems are not machine-certified by this program.
"""
from pathlib import Path
if not __debug__:
    raise RuntimeError("Run without -O: exact regression assertions are required")
import sympy as S, itertools, json, argparse
R=S.Rational
T=[R(6,5),R(7,5),R(8,5),R(9,5),R(2),R(5,2),R(3)]
r=R(3,5);pi=R(1,10)
def mul(a,b):
 return [sum((a[i]*b[n-i] for i in range(n+1)),S.S(0)) for n in range(3)]
def divide(a,b):
 c=[a[0]/b[0]]
 for n in [1,2]: c.append((a[n]-sum(b[i]*c[n-i] for i in range(1,n+1)))/b[0])
 return c
def cell_jet(f,h,beta,k,u,v,du,dv):
 # All arguments are exact rational jets at one clock.
 q=[(1-beta)*f[i]+beta*h[i] for i in range(3)]
 for i in [1,2]: q[i]+=k*(h[i-1]-f[i-1])
 result=[]
 for row in range(2):
  for col in range(2):
   out=[S.S(0)]*3
   for j,poly in enumerate([f,h]):
    weight=[1-beta,-k,0] if j==0 else [beta,k,0]
    uj=u[j] if row==0 else 1-u[j]; vj=v[j] if col==0 else 1-v[j]
    duj=du[j] if row==0 else -du[j]; dvj=dv[j] if col==0 else -dv[j]
    term=mul(mul(mul(poly,weight),[uj,duj,0]),[vj,dvj,0])
    out=[out[i]+term[i] for i in range(3)]
   result.append(divide(out,q))
 return result
def wall(mode):
 s=R(1,2) if mode=='B' else R(11,20)
 cstar=4*r**3/((r+3*s)*(2*r-3*s)**2)
 a=4*r*s/(r+3*s); b=r*s/(3*s-2*r)
 alpha=R(2,5) if mode=='B' else 1-pi*cstar
 beta=(1-alpha)/cstar
 vr=[(alpha*R(1,4)+(1-alpha-beta)*R(3,4))/(1-beta),R(3,4)]
 n=10 if mode=='B' else 11
 cone=[0,2,4] if mode=='B' else [0,2,5,6]
 free=[i for i in range(n) if i not in cone]
 def remote(x):
  if mode=='B':
   a0,b0,X,c0,w,k,uf,uh,vf,vh=x;d0=-w;Y=0
  else: a0,b0,X,c0,d0,Y,k,uf,uh,vf,vh=x
  out=[]
  for z in T:
   f=[z*(z-r)**2,-a0*(z-r)**2-b0*z*(z-r)-X*z,a0*b0*(z-r)+a0*X+b0*b0*z/4]
   h=[(z-a)*(z-b)**2,-c0*(z-b)**2-d0*(z-a)*(z-b)-Y*(z-a),c0*d0*(z-b)+c0*Y+d0*d0*(z-a)/4]
   out+=cell_jet(f,h,beta,k,[R(1,3)]*2,vr,[uf,uh],[vf,vh])
  return S.Matrix(out)
 base=[]
 for z in T:
  f=[z*(z-r)**2,0,0]
  h=[(z-s)**3,3*(z-s)**2,3*(z-s)] if mode=='B' else [(z-s)**3,0,0]
  base+=cell_jet(f,h,1-alpha,0 if mode=='B' else -1,[R(1,3)]*2,[R(1,4),R(3,4)],[0,0],[0,0])
 base=S.Matrix(base); zero=remote([S.S(0)]*n)
 assert zero[:,0]==base[:,0]
 cols=[]
 for i in range(n):
  x=[S.S(0)]*n;x[i]=S.S(1);cols.append(remote(x)[:,1])
 score=S.Matrix.hstack(*cols);L=score[:,free];D=score[:,cone]
 W=S.diag(*[1/(7*p) for p in base[:,0]])
 GL=L.T*W*L; assert GL.det()>0
 vf=GL.inv()*(L.T*W*base[:,1])
 resid=base[:,1]-L*vf
 projected=D-L*GL.inv()*(L.T*W*D)
 Q=projected.T*W*projected;g=projected.T*W*resid;bval=(resid.T*W*resid)[0]
 assert all(t<0 for t in g)
 supports=[]
 for k in range(len(cone)+1):
  for A in itertools.combinations(range(len(cone)),k):
   z=S.zeros(len(cone),1)
   if A:
    QA=Q.extract(A,A)
    if any(QA[:j,:j].det()<=0 for j in range(1,k+1)):continue
    sol=QA.inv()*g.extract(A,[0])
    if any(t<0 for t in sol):continue
    for j,v in zip(A,sol):z[j]=v
   if all((Q*z-g)[j]>=0 for j in range(len(cone)) if j not in A):supports.append(list(A))
 assert supports==[[]]
 # All principal minors certify positive semidefiniteness exactly.
 assert all(Q.extract(A,A).det()>=0 for k in range(1,len(cone)+1) for A in itertools.combinations(range(len(cone)),k))
 opt=[S.S(0)]*n
 for i,val in zip(free,vf):opt[i]=val
 rem=remote(opt);p=base[:,0];A=rem[:,1];B=base[:,1];C=rem[:,2];Dd=base[:,2]
 mu2=sum((A[j]-B[j])**2/(28*p[j]) for j in range(len(p)))
 muk=sum(((A[j]-B[j])*(C[j]-Dd[j])/(4*p[j])-(A[j]-B[j])*(A[j]**2-B[j]**2)/(16*p[j]**2))/7 for j in range(len(p)))
 assert mu2==bval/4 and mu2>0 and muk>0
 bounds={'B':('0.000063237134157102','0.000063237134157103','0.071857358263070','0.071857358263071'),'E':('0.000002131024914','0.000002131024915','0.011285405417542','0.011285405417543')}[mode]
 ml,mh,kl,kh=map(R,bounds)
 assert ml*ml<mu2<mh*mh
 assert kl*kl*mu2<muk*muk<kh*kh*mu2
 def mat(M):return [[str(v) for v in row] for row in M.tolist()]
 print(mode, 'mu=',S.sqrt(mu2).evalf(18),'k=',(muk/S.sqrt(mu2)).evalf(18),'ranks',L.rank(),Q.rank(),flush=True)
 return {'mode':mode,'alpha':str(alpha),'a':str(a),'b':str(b),'cstar':str(cstar),'beta':str(beta),'remote_vf':str(vr[0]),'free_indices':free,'cone_indices':cone,'free_gram':mat(GL),'projected_gram':mat(Q),'projected_linear':mat(g),'projected_base_norm_squared':str(bval),'free_optimum':mat(vf),'mu_squared':str(mu2),'mu_times_k':str(muk),'mu_interval':list(bounds[:2]),'k_interval':list(bounds[2:]),'successful_independent_supports':supports,'all_projected_principal_minors_nonnegative':True}

def binary_models():
    r0, s0 = R(1, 4), R(3, 4)
    rr, ss, al, u1, u2, v1, v2 = S.symbols('r s alpha u1 u2 v1 v2')
    variables = [rr, ss, al, u1, u2, v1, v2]
    arrays = []
    for clock in [2, 3, 4]:
        f, h = clock-rr, clock-ss
        U1, U2 = S.Matrix([u1, 1-u1]), S.Matrix([u2, 1-u2])
        V1, V2 = S.Matrix([v1, 1-v1]), S.Matrix([v2, 1-v2])
        P = (al*f*U1*V1.T+(1-al)*h*U2*V2.T)/(al*f+(1-al)*h)
        arrays.extend(list(P))
    P = S.Matrix(arrays)
    jacobian = P.jacobian(variables)
    expected = {
        R(1, 4): S.Matrix([[129609775953, 79361335413], [79361335413, 48691215153]])/404480,
        R(1, 8): S.Matrix([[10058351786055, 6157532670525], [6157532670525, 3781629625095]])/22342144,
    }
    result = {}
    diameters = []
    for epsilon in expected:
        centre = {rr:r0, ss:s0, al:R(1, 2), u1:R(1, 2)+epsilon,
                  u2:R(1, 2)-epsilon, v1:R(1, 4), v2:R(3, 4)}
        p0, score = P.subs(centre), jacobian.subs(centre)
        assert all(value > 0 for value in p0)
        H = score.T*S.diag(*[1/(3*value) for value in p0])*score
        assert H.rank() == 7
        inverse = H.inv()
        assert H*inverse == S.eye(7)
        M = inverse[:2, :2]
        assert M == expected[epsilon]
        assert M[0, 0] > M[1, 1] > 0 and M.det() > 0
        c2 = 16*M[0, 0]
        diameters.append(c2)
        result[str(epsilon)] = {
            'coordinate_order': [str(v) for v in variables],
            'fisher_gram': [[str(v) for v in row] for row in H.tolist()],
            'profiled_root_covariance': [[str(v) for v in row] for row in M.tolist()],
            'score_rank': 7,
            'diameter_squared': str(c2),
        }
    assert diameters[0] != diameters[1]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', type=Path, help='Compare with a committed exact record')
    args = parser.parse_args()
    data = {
        'schema': 'a2-v100-exact-1',
        'review_head': '5485ed6d127b8443fce059db118dc215b68e283a',
        'reviewed_paper_head': 'c49c6d0604f83badf47b32dfdf25dc043b4117ef',
        'index_convention': 'Python zero-based; free/cone coordinates stated in the appendix',
        'cubic_critical_examples': {mode:wall(mode) for mode in ['B', 'E']},
        'binary_valuative_separation': binary_models(),
        'universal_theorems_machine_verified': False,
    }
    if args.check:
        expected = json.loads(args.check.read_text(encoding='utf-8'))
        if data != expected:
            raise AssertionError('Computed exact diagnostics differ from committed record')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n', encoding='utf-8')
    print('PASS: both cubic critical programs and both binary full-rank programs')


if __name__ == '__main__':
    main()
