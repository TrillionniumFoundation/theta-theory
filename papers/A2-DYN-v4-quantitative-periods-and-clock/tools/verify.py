#!/usr/bin/env python3
"""Independent finite checks; exact algebra is separated from float models."""
from fractions import Fraction as F
import math,json,itertools
from pathlib import Path

def det(A):
 A=[list(map(F,row)) for row in A];n=len(A);ans=F(1)
 for j in range(n):
  p=next((i for i in range(j,n) if A[i][j]),None)
  if p is None:return F(0)
  if p!=j:A[j],A[p]=A[p],A[j];ans=-ans
  a=A[j][j];ans*=a
  for i in range(j+1,n):
   r=A[i][j]/a
   for k in range(j+1,n):A[i][k]-=r*A[j][k]
 return ans

def schur(n,R):
 g=1-2*R;c=1+g/R
 H=[[F(0) for _ in range(n+1)] for _ in range(n+1)]
 for j in range(n):
  H[j][j]+=1/R+1/g;H[j+1][j+1]+=1/R+1/g
  H[j][j+1]-=1/g;H[j+1][j]-=1/g
 for j in range(1,n):
  z=H[j][j]
  for i in [0]+list(range(j+1,n+1)):
   for k in [0]+list(range(j+1,n+1)):H[i][k]-=H[i][j]*H[j][k]/z
 return H[0][0],-H[0][n],H[n][n]

def ray(R,y,p,n):
 q=[math.sqrt(R*R-y*y),y];normal=[z/R for z in q];v=[math.sqrt(1-p*p)*normal[0]-p*normal[1],math.sqrt(1-p*p)*normal[1]+p*normal[0]];time=0.
 for j in range(n):
  center=[float((j+1)%2),0.];d=[center[k]-q[k] for k in range(2)];L=sum(d[k]*v[k] for k in range(2));disc=R*R-sum(z*z for z in d)+L*L
  if disc<=0:raise ValueError('grazing')
  t=L-math.sqrt(disc)
  if t<=0:raise ValueError('nonpositive flight')
  q=[q[k]+t*v[k] for k in range(2)];normal=[(q[k]-center[k])/R for k in range(2)];vn=sum(v[k]*normal[k] for k in range(2));v=[v[k]-2*vn*normal[k] for k in range(2)];time+=t
 return time

def run():
 checks={};counts={}
 def need(v,group):
  counts[group]=counts.get(group,0)+1
  if not v:raise ValueError('failed: '+group)
 V=[[0,0,2,1],[0,0,3,1],[1,0,4,1],[0,1,4,1]]
 need(abs(det(V))==1,'exact_augmented_lattice')
 for den in range(2,10):
  # Fixed-point congruences: solve s first, then the two winding characters.
  for s in range(den):
   for c in range(den):
    if (2*s-c)%den==0 and (3*s-c)%den==0:
     need(s==0 and c==0,'exact_augmented_lattice')
 for R in (F(9,20),F(23,50),F(47,100)):
  g=1-2*R;c=1+g/R;T0,T1=F(1),c;U0,U1=F(1),2*c
  for n in range(1,13):
   T=T1 if n==1 else None
   if n>1:T0,T1=T1,2*c*T1-T0;T=T1
   if n==1:U=U0
   elif n==2:U=U1
   else:U0,U1=U1,2*c*U1-U0;U=U1
   a,b,d=schur(n,R)
   need(a==d==T/(g*U) and b==1/(g*U),'exact_schur_recurrence')
   need(T*T-(c*c-1)*U*U==1,'exact_hessian_determinant')
   need((a*a-b*b)/(b*b)==(c*c-1)*U*U,'exact_hessian_determinant')
 # Positive optical Jacobi matrices: algebraic examples, not new orbit certificates.
 tstar=F(50,3);vstar=F(200,47);q=F(47,53);Cstar=F(47,90)*tstar*tstar/(vstar*(1-q))
 for R in (F(9,20),F(23,50),F(47,100)):
  for n in range(2,13):
   times=[1/(1-2*R+F(j%4,20)) for j in range(n)]
   cs=[F(1)]+[F(1,1+(j%3)*8) for j in range(1,n)]+[F(1)]
   H=[[F(0) for _ in range(n+1)] for _ in range(n+1)]
   H[0][0]=1/R+times[0];H[n][n]=1/R+times[-1]
   for j in range(1,n):
    H[j][j]=times[j-1]+times[j]+2/(R*cs[j])
    need((times[j-1]+times[j])/H[j][j]<=q,'exact_optical_contraction')
   for j in range(n):H[j][j+1]=H[j+1][j]=-times[j]
   for j in range(1,n):
    pivot=H[j][j]
    for i in [0]+list(range(j+1,n+1)):
     for k in [0]+list(range(j+1,n+1)):H[i][k]-=H[i][j]*H[j][k]/pivot
   aa,cc,dd=H[0][0],H[0][n],H[n][n]
   need(aa>=1/R and dd>=1/R and (aa-1/R)*(dd-1/R)>=cc*cc,'exact_optical_endpoint_margin')
   need(abs(cc)<=tstar*tstar*q**(n-2)/(vstar*(1-q)),'exact_optical_transmission')
   need(cc*cc/(4*R*R*(aa*dd-cc*cc))<=Cstar*Cstar*q**(2*(n-2)),'exact_general_edge_bound')
 for R in (.45,.46,.47):
  g=1-2*R;z=math.acosh(1+g/R)
  for n in (1,2,3):
   a=math.sinh(z)/g/math.tanh(n*z);b=math.sinh(z)/g/math.sinh(n*z)
   exact=[a*((a/b)**2-1),(a*a-b*b)/(b*b),a/(b*b)]
   h=2e-5;f=lambda y,p:ray(R,y,p,n);base=f(0,0)
   approx=[(f(h,0)+f(-h,0)-2*base)/h**2,(f(h,h)-f(h,-h)-f(-h,h)+f(-h,-h))/(4*h*h),(f(0,h)+f(0,-h)-2*base)/h**2]
   for x,y in zip(exact,approx):need(abs(x-y)<2e-4*max(1,abs(x)),'floating_physical_hessian')
  for n in range(1,20):
   need(0<math.sinh(n*z)/math.sinh((n+1)*z)<math.exp(-z),'floating_edge_decay')
 for b in (1,10,100,1000,10000):
  J=.7;a=.2;raw=J/(1-1j*b)+a/(1-1j*b)**2;res=raw-J/(1-1j*b)
  need(abs(res)*(1+b*b)<a+1e-9,'floating_edge_subtraction')
  if b>=100:need(abs(b*abs(raw)-J)<.001,'floating_raw_boundary_term')
 # Exact suspension probabilities for a finite periodic base, not a billiard.
 roofs=[F(1,10),F(1,5),F(3,10)];mean=sum(roofs)/3
 for t in [F(j,100) for j in range(1,81)]:
  prob0=sum(max(tau-t,0) for tau in roofs)/(3*mean);total=prob0;expect=F(0)
  for k in range(1,10):
   mass=F(0)
   for y in range(3):
    prev=roofs[(y-1)%3];sk=sum(roofs[(y+i)%3] for i in range(k));skm=sk-roofs[(y+k-1)%3]
    mass+=max(F(0),min(prev,t-skm)-max(F(0),t-sk))
   pk=mass/(3*mean);total+=pk;expect+=k*pk
  need(total==1 and expect==t/mean,'exact_marked_suspension_model')
 need(F(3,5)/5<F(1,2)<F(2)/2,'exact_valid_splice')
 for M in range(2,101):need(not(2*(M-1)/F(M-1)<1),'exact_rejected_splice')
 return {'status':'passed','checks':counts,'total_checks':sum(counts.values()),'full_billiard_LLT_verified':False,'human_review':False,'scope':'Exact finite algebra and explicitly floating physical/model diagnostics; no continuum proof certification.'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
