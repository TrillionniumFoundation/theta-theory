#!/usr/bin/env python3
"""Auxiliary exact checks for A2 v170; the written proofs are not replaced by tests."""
from __future__ import annotations
import argparse, hashlib, json, math, platform, subprocess, sys, time
from fractions import Fraction
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(n,m):return n[0]*m[0]+n[1]*m[1]
def det(n,m):return n[0]*m[1]-n[1]*m[0]
def data(a,r,s):
 g=[math.gcd(r,i*s) for i in range(1,a+1)]
 rays=[(0,1)]+[(i*s//g[i-1],r//g[i-1]) for i in range(1,a+1)]+[(1,0)]
 kappa=[(r*i*s-r-i*s)//g[i-1]+1 for i in range(1,a+1)]
 return g,rays,kappa

def lattice_and_fibre():
 cases=points=0
 for a,r,s in product(range(2,9),range(1,10),range(1,10)):
  g,rays,kappa=data(a,r,s);cases+=1
  for j,n in enumerate(rays[1:-1],1):
   assert math.gcd(*n)==1 and (r*n[0],s*n[1])==(r*s//g[j-1]*j,r*s//g[j-1])
   assert min(n)==min(r,j*s)//g[j-1]
   assert (min(n)==1)==(r%(j*s)==0 or (j*s)%r==0)
   assert kappa[j-1]>=0 and ((r*j*s-r-j*s+g[j-1])%2==0)
  assert (not any(kappa))==(r==1)
  ds=[abs(det(l,h)) for l,h in zip(rays,rays[1:])]
  assert ds==[s//g[0]]+[r*s//(g[i-1]*g[i]) for i in range(1,a)]+[r//g[-1]]
  for i in range(1,a+1):
   selfint=-Fraction(abs(det(rays[i-1],rays[i+1])),ds[i-1]*ds[i])
   for coord in range(2):
    assert Fraction(rays[i-1][coord],ds[i-1])+selfint*rays[i][coord]+Fraction(rays[i+1][coord],ds[i])==0
  for l,h in zip(rays,rays[1:]):
   for x,y in product(range(-8,9),repeat=2):
    def ins(z):return dot(l,z)>=0 and dot(h,z)>=0
    actual=ins((x-1,y)) or ins((x,y-1))
    divisorial=dot(l,(x,y))>=min(l) and dot(h,(x,y))>=min(h)
    assert actual==divisorial,(a,r,s,l,h,x,y)
    points+=1
 # Also test cones not restricted to the contact family.
 primitive=[(x,y) for x,y in product(range(9),repeat=2) if x+y and math.gcd(x,y)==1]
 arbitrary=0
 for l,h in product(primitive,repeat=2):
  if det(l,h)>=0 or (l==(0,1) and h==(1,0)):continue
  for m in product(range(-4,5),repeat=2):
   actual=all(dot(n,(m[0]-1,m[1]))>=0 for n in (l,h)) or all(dot(n,(m[0],m[1]-1))>=0 for n in (l,h))
   predicted=all(dot(n,m)>=min(n) for n in (l,h))
   assert actual==predicted,(l,h,m);arbitrary+=1
 return {'parameter_triples':cases,'contact_cone_memberships':points,'arbitrary_cone_memberships':arbitrary,'passed':True}

def conductor_charts():
 cases=points=0
 for i,r,s in product(range(1,6),range(1,8),range(1,8)):
  def raw(x,y):
   A=x//r;B=y//s
   return B+(i+1)*A>=0 and B+i*A>=0
  reps=[]
  for x,y in product(range(r),range(s)):
   E=Fraction((i+1)*x,r)+Fraction(y,s);H=Fraction(i*x,r)+Fraction(y,s)
   fe,fh=math.floor(E),math.floor(H)
   reps.append((x-r*(fe-fh),y-s*(-i*fe+(i+1)*fh)))
  g0=math.gcd(r,i*s);g1=math.gcd(r,(i+1)*s)
  n0=(i*s//g0,r//g0);n1=((i+1)*s//g1,r//g1)
  c0=(r*i*s-r-i*s)//g0+1;c1=(r*(i+1)*s-r-(i+1)*s)//g1+1
  for x,y in product(range(-10,17),repeat=2):
   actual=all(raw(x+dx,y+dy) for dx,dy in reps)
   predicted=dot(n0,(x,y))>=c0 and dot(n1,(x,y))>=c1
   assert actual==predicted,(i,r,s,x,y,c0,c1)
   points+=1
  cases+=1
 end_points=0
 for a,r,s in product(range(2,7),range(1,8),range(1,8)):
  g,n,c=data(a,r,s)
  firstreps=[(-(r*y//s),y) for y in range(s)]
  lastreps=[(x,-(a*s*x//r)) for x in range(r)]
  for x,y in product(range(-8,15),repeat=2):
   actual=all(y+dy>=0 and x+dx+r*((y+dy)//s)>=0 for dx,dy in firstreps)
   assert actual==(y>=0 and dot(n[1],(x,y))>=c[0]),('first',a,r,s,x,y)
   actual=all(x+dx>=0 and y+dy+a*s*((x+dx)//r)>=0 for dx,dy in lastreps)
   assert actual==(x>=0 and dot(n[-2],(x,y))>=c[-1]),('last',a,r,s,x,y)
   end_points+=2
 return {'interior_charts':cases,'interior_conductor_memberships':points,'end_conductor_memberships':end_points,'method':'Exact finite module representatives of the normalization over the two boundary monomials, not just generic transverse orders.','passed':True}

def binomial_and_equal_power():
 semigroups=0
 for r,q in product(range(1,41),repeat=2):
  g=math.gcd(r,q);rr=r//g;qq=q//g
  c=(rr-1)*(qq-1)
  represented={rr*x+qq*y for x,y in product(range(qq+rr+1),repeat=2)}
  gaps=[n for n in range(c) if n not in represented]
  assert len(gaps)*2==c
  assert all(n in represented for n in range(c,c+rr+qq))
  if c:assert c-1 not in represented
  assert c+(g-1)*rr*qq==(r*q-r-q)//g+1
  assert g*len(gaps)+g*(g-1)//2*rr*qq==(r*q-r-q+g)//2
  semigroups+=1
 checks=0
 for d,i in product(range(1,9),range(1,9)):
  c=((i+1)*(d-1),i*(d-1))
  def member(x,y):
   j=(x-y)%d;k=(y-i*j)%d
   return x>=(i+1)*j+k and y>=i*j+k
  for x,y in product(range(c[0]+d+1),range(c[1]+d+1)):
   actual=all(member(x+dx,y+dy) for dx,dy in product(range(d),repeat=2))
   assert actual==(x>=c[0] and y>=c[1]);checks+=1
 return {'binomial_pairs':semigroups,'equal_power_rectangle_memberships':checks,'passed':True}

def examples_and_covers():
 g,n,c=data(3,2,3)
 assert g==[1,2,1] and n[1:-1]==[(3,2),(3,1),(9,2)] and c==[2,3,8]
 assert [min(x) for x in n[1:-1]]==[2,1,2]
 assert [abs(det(x,y)) for x,y in zip(n,n[1:])]==[3,3,3,2]
 for a,r,s,rr,ss in product(range(2,7),range(1,6),range(1,6),range(1,5),range(1,5)):
  _,old,_=data(a,r,s);_,new,_=data(a,r*rr,s*ss)
  for x,y in zip(old[1:-1],new[1:-1]):
   assert det(x,(rr*y[0],ss*y[1]))==0
 return {'a3_r2_s3':{'g':g,'rays':n,'kappa':c,'ell':[min(x) for x in n[1:-1]],'delta':[1,3,4]},'successive_cover_composition':True,'passed':True}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true',help='Local audit only; remote publication must rerun the entire inherited chain.')
 args=ap.parse_args();start=time.monotonic();inherited=False
 if not args.skip_inherited:
  predecessor=HERE.parent/'v169'/'check_v169.py'
  p=subprocess.run([sys.executable,str(predecessor)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (HERE/'INHERITED_V169_COMMAND.log').write_text(p.stdout)
  if p.returncode:raise RuntimeError('Inherited v169 chain failed; see INHERITED_V169_COMMAND.log')
  data_=json.loads((predecessor.parent/'EXACT_CHECKS_V169.json').read_text())
  assert data_['all_checks_pass'] and data_['inherited_v167_full_chain_rerun']
  (HERE/'INHERITED_V169_CHECKS_RERUN.json').write_text(json.dumps(data_,indent=2)+'\n');inherited=True
 result={'revision':170,'python':platform.python_version(),'all_checks_pass':False,'inherited_v169_full_chain_rerun':inherited,
 'limitations':'Finite exact algebra and lattice regressions only; not a certificate of general proofs, historical originality, an external Paper I audit, or journal merit.',
 'lattice_and_fibre':lattice_and_fibre(),'full_conductor_charts':conductor_charts(),'binomial_and_equal_power':binomial_and_equal_power(),'examples_and_covers':examples_and_covers()}
 result['all_checks_pass']=True;result['duration_seconds']=round(time.monotonic()-start,3)
 result['source_sha256']={p.name:sha(p) for p in HERE.glob('*-v170.tex')}
 (HERE/'EXACT_CHECKS_V170.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
