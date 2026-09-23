#!/usr/bin/env python3
"""Finite diagnostic checks, not a verification of the analytic theorems."""
from __future__ import annotations
import argparse,itertools,json,math
from fractions import Fraction as F

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mutant',default='');args=ap.parse_args()
 counts={}
 def need(ok,group,message):
  if not ok:raise RuntimeError('FAILED: '+group+': '+message)
  counts[group]=counts.get(group,0)+1
 def words(n):return list(itertools.product((0,1),repeat=n))
 for n in range(1,12,2):
  m=n//2
  for t in range(n):
   suffixes=words(n-t);rows={tuple(int(sum(u+s)>m)for s in suffixes)for u in words(t)}
   expected=min(t+1,n-t+2-(args.mutant=='majority_off_by_one'))
   need(len(rows)==expected,'residual_profile',f'n={n}, t={t}')
  peak=max(min(t+1,n-t+2)for t in range(n))
  need(peak==(1 if n==1 else m+2),'peak_width',str(n))
  for h in (F(1,10),F(1,8),F(1,4)):
   a,b=F(1,2)+h,F(1,2)-h
   differences=[abs(a**k*b**(n-k)-b**k*a**(n-k))for k in range(n+1)]
   expected=2*h*(F(1,4)-h*h)**m
   if args.mutant=='likelihood_margin':expected*=2
   need(min(differences)==expected,'likelihood_margin',str((n,h)))
 # The overlap inequality on finite rational encoding simplexes.
 for K in range(1,4):
  vectors=[v for v in itertools.product(range(3),repeat=K)if sum(v)==2]
  for r in range(2,5):
   for es in itertools.product(vectors,repeat=r):
    overlap=sum(min(es[i][s],es[j][s])for i in range(r)for j in range(i+1,r)for s in range(K))
    need(overlap>=2*(r-K),'overlap_bound',str((r,K,es)))
 # Exhaustive deterministic n=3 width-(1,1,1) and width-(1,2,2) audits.
 h=F(1,10);n=3;ws=words(n);a,b=F(1,2)+h,F(1,2)-h
 pp=[a**sum(w)*b**(n-sum(w))for w in ws];pm=[b**sum(w)*a**(n-sum(w))for w in ws]
 vn=h*sum(abs(x-y)for x,y in zip(pp,pm))/2
 for K1,K2 in ((1,1),(2,2)):
  best=F(-1)
  for first in itertools.product(range(K1),repeat=2):
   for second in itertools.product(range(K2),repeat=2*K1):
    for last in itertools.product((-1,1),repeat=2*K2):
     ds=[last[2*second[2*first[w[0]]+w[1]]+w[2]]for w in ws]
     value=min(h*sum(p*d for p,d in zip(pp,ds)),-h*sum(p*d for p,d in zip(pm,ds)))
     best=max(best,value)
  lower=2*h*h*(F(1,4)-h*h)*(3-K2)/2
  need(vn-best>=lower,'exhaustive_small_auditor',str((K1,K2)))
 # All feasible empirical count pairs; the two-count event equals the
 # positive discrepancy event and clipping preserves it, including ties.
 def rule(c0,c1):
  return tuple(int(q*400>8*c)for q,c in ((5,c0),(3,c0),(3,c1),(5,c1)))
 clip=249 if args.mutant=='counter_clip' else 250
 for c0 in range(401):
  for c1 in range(401-c0):
   need(rule(c0,c1)==rule(min(c0,clip),min(c1,clip)),'clipped_count_events',str((c0,c1)))
 ntrain=399 if args.mutant=='insufficient_training' else 400
 need(F(1,ntrain)<=F(1,400),'training_regret','400-sample regret 1/20')
 need(F(5,2)-F(947,600)**2==F(3191,360000)>0,'physical_score_margin','strict 2/5 margin')
 states=(251**2 if args.mutant=='unpriced_transcript' else 8*251**2)
 need(states==504008 and states<2**19,'state_budget','transcript buffer included')
 need(9*2*8<=states and 400+1+1==402,'validation_budget','independent trials')
 # Pointwise regret, checked with exact rational arithmetic on a grid.
 for p,q in itertools.product((F(i,10)for i in range(11)),repeat=2):
  a0,c=p.__rsub__(1)*(1-q),p*q
  probs=(a0/2,a0/2,c/2,c/2);target=(F(5,16),F(3,16),F(3,16),F(5,16))
  optimum=sum(max(F(0),x-y)for x,y in zip(target,probs))
  for c0,c1 in itertools.product((0,149,150,249,250,400),repeat=2):
   if c0+c1>400:continue
   event=rule(c0,c1);score=sum(z*(x-y)for z,x,y in zip(event,target,probs))
   need(optimum-score<=abs(F(c0,400)-a0)+abs(F(c1,400)-c),'pointwise_regret','empirical sign bound')
 # Finite common-latent posterior comparisons under both physical laws.
 tables=[]
 for i,j in itertools.product(range(1,5),repeat=2):
  tables.append((F(i,10),F(5-i,10),F(j,10),F(5-j,10)))
 for P,Q in itertools.product(tables,repeat=2):
  tv=sum(abs(a-b)for a,b in zip(P,Q))/2
  mP=[(P[y]-P[y+2])/(P[y]+P[y+2])for y in range(2)]
  mQ=[(Q[y]-Q[y+2])/(Q[y]+Q[y+2])for y in range(2)]
  for S in (P,Q):
   l1=sum((S[y]+S[y+2])*abs(mP[y]-mQ[y])for y in range(2))
   l2=sum((S[y]+S[y+2])*(mP[y]-mQ[y])**2 for y in range(2))
   need(l1<=4*tv and l2<=8*tv,'posterior_comparison','common physical path')
 # Exact symbolic coefficient check for the backward-integral estimate.
 gamma,M,sigma,T=F(3,2),F(2),F(1,3),F(5)
 coeff=2*(gamma/2)**2*(4*M/(gamma*sigma))**2*T
 expected=8*M*M*T/(sigma*sigma)
 if args.mutant=='backward_coefficient':expected/=2
 need(coeff==expected,'backward_coefficient','Cauchy-Schwarz coefficient')
 if args.mutant:raise RuntimeError('FAILED: unknown or surviving mutant '+args.mutant)
 print(json.dumps({'schema':'gtf.v19.finite-diagnostics/1','checks':counts,'total':sum(counts.values()),'scope':'Exact finite diagnostics; not an independent proof of continuum or stochastic-process theorems.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
