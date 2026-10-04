#!/usr/bin/env python3
"""Finite diagnostics for the new v33 arguments; not physical/proof certification."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import re

CHECKS: Counter[str] = Counter()
ROOT = Path(__file__).resolve().parents[1]
PRESERVED = {
 '00_setting.tex':'e21ae6d91dc10606d4f2229afe98ed0692e7c937',
 '01_local_queries.tex':'f262550adf86a3f2c21acadffe744e05307bab26',
 '02_adaptive_boundary.tex':'2325ab695562e62da30cfa75e2d0ed5673387be1',
 '03_period_recognition.tex':'1b4739ed6f454cbd703676656a38d6cd9bc358d2',
 '04_information_bound.tex':'5950d63587ac12fb5eb55458538c4b920b707ac5',
 '05_comparison.tex':'4d57baf52d7b3ad26376cfb322b095b60153d03c'}

def require(ok: bool, group: str) -> None:
 if not ok: raise RuntimeError(group)
 CHECKS[group] += 1

def rounded_bisection() -> None:
 for boundary in [F(i,29) for i in range(1,29)]:
  for tube in [F(0), F(1,64), F(1,32)]:
   for mesh in [F(1,32),F(1,64)]:
    states={(F(0),F(1))}
    for k in range(1,10):
     nxt=set()
     for lo,hi in states:
      mid=(lo+hi)/2
      # Both rounding tie choices are tested, including history-dependent labels.
      floor=math.floor(mid/mesh)*mesh
      for x in {max(lo,min(hi,floor)),max(lo,min(hi,floor+mesh))}:
       require(abs(x-mid)<=mesh,'dyadic_midpoint_error')
       choices=[]
       if x<=boundary+tube: choices.append(1)
       if x>=boundary-tube: choices.append(0)
       for bit in choices:
        l,u=(x,hi) if bit else (lo,x)
        require(l-tube<=boundary<=u+tube,'rounded_relaxed_invariant')
        require(u-l<=(hi-lo)/2+mesh,'rounded_width_recurrence')
        require(u-l<=F(1,2**k)+2*mesh,'rounded_geometric_width')
        require(abs((l+u)/2-boundary)<=tube+F(1,2**(k+1))+mesh,
                'rounded_radius_error')
        nxt.add((l,u))
     states=nxt
 for b in range(5,15):
  step=F(3,16); mesh=F(1,2**b)
  for depth in range(1,8):
   center=(F(13,2**b),F(-7,2**b))
   diamond={(i,j) for i in range(-depth,depth+1)
                    for j in range(-depth,depth+1) if abs(i)+abs(j)<=depth}
   require(len(diamond)==1+2*depth*(depth+1),'diamond_count')
   for i,j in diamond:
    x,y=center[0]+step*i,center[1]+step*j
    require((x/mesh).denominator==(y/mesh).denominator==1,'one_dyadic_stencil')
    require(x+step-step==x,'reciprocal_translation_exact')


def leaves(n: int):
 if n==1: return [('',)]
 out=[]
 for k in range(1,n):
  for left in leaves(k):
   for right in leaves(n-k):
    out.append(tuple('0'+x for x in left)+tuple('1'+x for x in right))
 return out

def entropy(p):
 return -sum(float(x)*math.log2(float(x)) for x in p if x)

def sequential_entropy() -> None:
 for n in range(2,8):
  for words in leaves(n):
   require(sum(F(1,2**len(w)) for w in words)==1,'prefix_kraft_identity')
   require(not any(a!=b and b.startswith(a) for a in words for b in words),
           'terminal_words_prefix_free')
   weights=[F(j+1,n*(n+1)//2) for j in range(n)]
   length=sum(p*len(w) for p,w in zip(weights,words))
   require(entropy(weights)<=float(length)+1e-12,'entropy_below_mean_length')
   # A noisy parameter-to-leaf channel with uniform prior and error 1/8.
   channel=[[F(7,8) if j==i else (F(1,8) if j==(i+1)%n else F(0))
             for j in range(n)] for i in range(n)]
   mean=sum(sum(p*len(w) for p,w in zip(row,words)) for row in channel)/n
   delta=F(1,8)
   bound=float(1-delta)*math.log2(n)-entropy([delta,1-delta])
   require(float(mean)+1e-12>=bound,'sequential_fano_length_bound')
 # A countable prefix tree 1^k 0 with geometric probabilities: truncated checks.
 for depth in range(2,35):
  w=tuple('1'*k+'0' for k in range(depth))+('1'*depth,)
  p=[F(1,2**len(x)) for x in w]
  require(sum(p)==1,'truncated_infinite_tree_mass')
  require(abs(entropy(p)-float(sum(q*len(x) for q,x in zip(p,w))))<1e-11,
          'truncated_infinite_tree_entropy_identity')


def centered_bumps() -> dict:
 from scipy.integrate import quad
 ratios=[]
 # psi(t)=exp(-1/(1-9t^2)) on (-1/3,1/3), with psi''(0)=-18/e.
 for s in [F(13,2),F(20,3),F(7)]:
  for h in [1/4,1/8,1/16,1/32]:
   for theta in [0.,.7,2.1]:
    amplitude=.01*h**float(s)
    def f(t):
     return math.exp(-1/(1-9*t*t)) if abs(t)<1/3 else 0.
    zx=amplitude*h/math.pi*quad(lambda t:f(t)*math.cos(theta+h*t),-1/3,1/3,
                               epsabs=1e-13)[0]
    zy=amplitude*h/math.pi*quad(lambda t:f(t)*math.sin(theta+h*t),-1/3,1/3,
                               epsabs=1e-13)[0]
    raw=-18/math.e*amplitude/h**2
    centered=raw+zx*math.cos(theta)+zy*math.sin(theta)
    require(math.hypot(zx,zy)<=2*amplitude/math.e,'centering_first_harmonic_bound')
    require(abs(centered)>=abs(raw)/2,'centered_C2_packing_separation')
    ratios.append(abs(centered/raw))
 for beta in [F(1),F(1,2),F(1,3),F(2,3)]:
  s=6+beta
  require((s/(s-2))*((s-2)/s)==1,'calibration_exponent_duality')
  require(s/(s-2)>1 and 1/(s-2)<F(1,2),'separate_resource_exponents')
 return {'minimum_centered_to_raw_separation_ratio':min(ratios)}


def common_response_geometry() -> dict:
 import numpy as np
 from shapely.geometry import Point,MultiPoint
 from shapely.ops import nearest_points
 angles=np.linspace(-math.pi,math.pi,512,endpoint=False)
 p=1+.002*np.exp(4*(np.cos(angles)-1))
 dp=-.008*np.sin(angles)*np.exp(4*(np.cos(angles)-1))
 nn=np.column_stack([np.cos(angles),np.sin(angles)])
 tt=np.column_stack([-np.sin(angles),np.cos(angles)])
 c0=MultiPoint(nn).convex_hull
 c1=MultiPoint(p[:,None]*nn+dp[:,None]*tt).convex_hull
 e=float(c0.hausdorff_distance(c1))*1.001
 anchor=Point(6,0).buffer(2,resolution=128)
 bodies=[[c0,anchor],[c1,anchor]]
 maxmove=0.; disagreements=0; case_counts=Counter()
 def sweep(body,a):
  pts=np.asarray(body.exterior.coords)[:-1]
  return MultiPoint(np.vstack([pts,pts-a])).convex_hull
 def bit(q,bs,ss):
  return int(any(s.covers(q) for s in ss) and not any(c.covers(q) for c in bs))
 for phi in np.linspace(0,2*math.pi,12,endpoint=False):
  a=.7*np.array([math.cos(phi),math.sin(phi)])
  sweeps=[[sweep(c,a) for c in bs] for bs in bodies]
  require(sweeps[0][0].distance(sweeps[0][1])>2*e,'swept_component_separation')
  require(sweeps[0][0].hausdorff_distance(sweeps[1][0])<=e*(1+1e-8),
          'sweep_Hausdorff_contraction')
  for theta in np.linspace(-1.5,1.5,25):
   n=np.array([math.cos(theta),math.sin(theta)])
   for shift in [0.,.5,1.]:
    for offset in [-.75,-.25,.25,.75,1.25]:
     qv=n-shift*a+offset*e*n; q=Point(qv)
     raw=[bit(q,bodies[j],sweeps[j]) for j in range(2)]
     moved=[q,q]
     if raw[0]!=raw[1]:
      disagreements+=1; j=raw.index(1); k=1-j
      if bodies[k][0].covers(q):
       near=nearest_points(q,bodies[j][0])[1]
       pv=np.array(near.coords[0]); center=np.array(bodies[j][0].centroid.coords[0])
       lam=e/(4*(1+np.linalg.norm(center-pv)))
       out=Point((1-lam)*pv+lam*center); case_counts['solid_entry']+=1
      else:
       near=nearest_points(q,sweeps[k][0])[1]
       dv=qv-np.array(near.coords[0]); length=np.linalg.norm(dv)
       if length<=1e-13:
        # The pointwise boundary-normal case is proved in the text; this
        # floating diagnostic samples nonzero-distance projection cases only.
        raise RuntimeError('projection too close to a boundary for numeric test')
       out=Point(qv+1.5*e*dv/length); case_counts['swept_exit']+=1
      moved[j]=out; distance=q.distance(out); maxmove=max(maxmove,distance)
      require(distance<=2*e*(1+1e-8),'physical_perturbation_budget')
     actual=[bit(moved[j],bodies[j],sweeps[j]) for j in range(2)]
     require(actual==[min(raw)]*2,'common_physical_response')
 require(disagreements>10,'nonvacuous_disagreements')
 require(all(case_counts[x]>0 for x in ['solid_entry','swept_exit']),
         'both_perturbation_cases_exercised')
 return {'geometric_starts':12*25*3*5,'nominal_disagreements':disagreements,
         'perturbation_cases':dict(case_counts),'Hausdorff_bound':e,
         'maximum_start_displacement':maxmove,
         'maximum_displacement_over_bound':maxmove/e}


def sources() -> None:
 for name,expected in PRESERVED.items():
  b=(ROOT/'core'/name).read_bytes()
  require(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==expected,
          'all_v32_core_blobs_retained')
 text=(ROOT/'main.tex').read_text()
 for name in re.findall(r'\\input\{([^}]+)\}',text):
  p=ROOT/(name+'.tex'); require(p.is_file(),'input_reachable'); text+='\n'+p.read_text()
 labels=re.findall(r'\\label\{([^}]+)\}',text)
 require(len(labels)==len(set(labels)),'unique_labels')
 for label in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
  require(label in labels,'reference_resolved')
 for label in ['thm:adaptive','thm:lower','thm:resources','thm:digital',
               'thm:expected','thm:calibration-floor','eq:accuracy-sets']:
  require(label in labels,'old_and_new_results_active')


def main() -> None:
 rounded_bisection(); sequential_entropy()
 numerical={**centered_bumps(),**common_response_geometry()}
 sources()
 print(json.dumps({'schema':'a2-v33-finite-diagnostics-1','status':'passed',
  'finite_checks':sum(CHECKS.values()),'checks':dict(sorted(CHECKS.items())),
  'numerical_controls':numerical,'formal_proof_certificate':False,
  'physical_sensor_executed':False},indent=2,sort_keys=True))

if __name__=='__main__': main()
