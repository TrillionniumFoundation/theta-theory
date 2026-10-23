import numpy as np
from scipy.optimize import differential_evolution

def costs(v):
 n=len(v); M=max(v);m=-min(v)
 if m<=0:return n-1,n-1
 k=np.max(np.tile(v,(n,1))-np.eye(n),axis=1)
 h=np.max(np.eye(n)-np.tile(v,(n,1)),axis=1)
 s=v@k;r=v@h
 C=sum(k)+(s/m if s>=0 else -s/M)
 D=sum(h)+(r/m if r>=0 else -r/M)
 return C,D

def cand(n,p):
 s=np.sqrt(n);tau=(s-1)/(s+1)
 if p<=1/(n-s):return p*tau
 if p<=2/n:return ((n-1)*p-1)/((n-1)*(n*p-1))
 return (1-p)/(n-1)
for n in [5,6,7,10]:
 for p in np.linspace(1/(n-np.sqrt(n))*.9,2/n*1.1,5):
  def f(x):
   v=np.r_[x,1-sum(x)];C,D=costs(v)
   return -min(p/C,(1-p)/D)
  r=differential_evolution(f,[(-1,2)]*(n-1),popsize=20,maxiter=1200,tol=1e-10,seed=42,polish=True)
  print(n,p,'cand',cand(n,p),'found',-r.fun,'v',np.sort(np.r_[r.x,1-sum(r.x)]),flush=True)
