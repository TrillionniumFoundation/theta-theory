#!/usr/bin/env python3
"""Centered-dual interval coverage of the complete Round94 rank-three rays."""
from __future__ import annotations
import hashlib,json
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb,ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round84_reverse_common_tangent_closure_generator as reverse
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round92_rank3_competitor_event_isolation_cert as round92
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign
HERE=Path(__file__).resolve().parent
R93=HERE/"cm2-round93-rank3-full-source-chart-exit-2026-07-22.json"
R94=HERE/"cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
PINS={R93.name:"8a69487f962afe850eb15cc0a0d0b3faebe3c5cc50d6c93662e7a52b4285ccb3",R94.name:"915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3"}
SCHEMA="cm2.round95.rank3-centered-reverse-interval.v1";PRECISION_BITS=512;MAX_DEPTH=120
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
class Dual:
 def __init__(self,value,derivative=0):self.value=value if isinstance(value,arb) else arb(value);self.derivative=derivative if isinstance(derivative,arb) else arb(derivative)
 def coerce(self,o):return o if isinstance(o,Dual) else Dual(o)
 def __add__(self,o):o=self.coerce(o);return Dual(self.value+o.value,self.derivative+o.derivative)
 __radd__=__add__
 def __neg__(self):return Dual(-self.value,-self.derivative)
 def __sub__(self,o):return self+(-self.coerce(o))
 def __rsub__(self,o):return self.coerce(o)-self
 def __mul__(self,o):o=self.coerce(o);return Dual(self.value*o.value,self.derivative*o.value+self.value*o.derivative)
 __rmul__=__mul__
 def __truediv__(self,o):o=self.coerce(o);return Dual(self.value/o.value,(self.derivative*o.value-self.value*o.derivative)/(o.value*o.value))
 def __rtruediv__(self,o):return self.coerce(o)/self
 def sqrt(self):
  if strict_sign(self.value)!=1:raise RuntimeError("dual radicand")
  root=self.value.sqrt();return Dual(root,self.derivative/(2*root))
class Centered:
 def __init__(self,point,value,derivative,delta):self.point=point if isinstance(point,arb) else arb(point);self.value=value if isinstance(value,arb) else arb(value);self.derivative=derivative if isinstance(derivative,arb) else arb(derivative);self.delta=delta
 @staticmethod
 def variable(point,value,delta):return Centered(point,value,arb(1),delta)
 def coerce(self,o):
  if isinstance(o,Centered):return o
  if isinstance(o,Dual):o=o.value
  v=o if isinstance(o,arb) else arb(o);return Centered(v,v,arb(0),self.delta)
 def make(self,point,derivative):return Centered(point,point+derivative*self.delta,derivative,self.delta)
 def __add__(self,o):o=self.coerce(o);return self.make(self.point+o.point,self.derivative+o.derivative)
 __radd__=__add__
 def __neg__(self):return self.make(-self.point,-self.derivative)
 def __sub__(self,o):return self+(-self.coerce(o))
 def __rsub__(self,o):return self.coerce(o)-self
 def __mul__(self,o):o=self.coerce(o);return self.make(self.point*o.point,self.derivative*o.value+self.value*o.derivative)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=self.coerce(o)
  if strict_sign(o.value)==0:raise RuntimeError("centered denominator")
  return self.make(self.point/o.point,(self.derivative*o.value-self.value*o.derivative)/(o.value*o.value))
 def __rtruediv__(self,o):return self.coerce(o)/self
 def sqrt(self):
  if strict_sign(self.value)!=1:raise RuntimeError("centered radicand")
  root_point=self.point.sqrt();return self.make(root_point,self.derivative/(2*self.value.sqrt()))
def D(x):return x if isinstance(x,Dual) else Dual(x)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def scale(x,a):return x*a[0],x*a[1]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def reflect(v,n):return sub(v,scale(2*dot(v,n),n))
def center(identifier):
 return reverse.center(identifier)
def radius(identifier):return aq(reverse.radius(identifier))
def tangent(branch,q):
 ux=(1-q*q)/(1+q*q);uy=2*q/(1+q*q);n=(-uy,ux);direction=(n[1],-n[0]);c=center(branch[2]);h=dot(n,c)-branch[3]*radius(branch[2]);return n,direction,h
def line_hit(n,direction,h,identifier,sign):
 c=center(identifier);r=radius(identifier);distance=h-dot(n,c);root=(r*r-distance*distance).sqrt();foot=add(c,scale(distance,n));hit=add(foot,scale(sign*root,direction));normal=scale(1/r,sub(hit,c));return hit,normal
def ray_hit(point,direction,identifier,sign):
 c=center(identifier);r=radius(identifier);delta=sub(c,point);longitudinal=dot(direction,delta);transverse=cross(direction,delta);root=(r*r-transverse*transverse).sqrt();flight=longitudinal+sign*root;hit=add(point,scale(flight,direction));normal=scale(1/r,sub(hit,c));return hit,normal,flight
def evaluate_path(source,branch,q,path):
 n,direction,h=tangent(branch,q);hit2,normal2=line_hit(n,direction,h,branch[1],path[0]);incoming2=reflect(direction,normal2);reverse1=scale(-1,incoming2);hit1,normal1,flight1=ray_hit(hit2,reverse1,source.target_id,path[1]);initial=reflect(incoming2,normal1);reverse0=scale(-1,initial);hit0,normal0,flight0=ray_hit(hit1,reverse0,f"{source.source}[0,0]",path[2]);side=source.chart_id.split(":")[1];radial=normal0[0] if side in ("E","W") else normal0[1];expected=1 if side in ("E","N") else -1;t=normal0[1] if side in ("E","W") else normal0[0];p=dot(initial,(-normal0[1],normal0[0]));return t,p,dot(direction,normal2),dot(reverse1,normal1),dot(reverse0,normal0),expected*radial,flight1,flight0
def discover_path(source,branch,q):
 valid=[]
 for a in (-1,1):
  for b in (-1,1):
   for c in (-1,1):
    try:row=evaluate_path(source,branch,Dual(aq(q),arb(1)),(a,b,c))
    except RuntimeError:continue
    if all(strict_sign(x.value)==1 for x in (row[2],-row[3],-row[4],row[5],row[6],row[7])):valid.append((a,b,c))
 if len(valid)!=1:raise RuntimeError(f"dual path count {len(valid)}")
 return valid[0]
def centered_box(source,branch,qa,qb):
 lo,hi=min(qa,qb),max(qa,qb);mid=(lo+hi)/2;rad=(hi-lo)/2;path=discover_path(source,branch,mid);point=evaluate_path(source,branch,Dual(aq(mid),arb(1)),path);delta=arb(0,aq(rad).upper());full=evaluate_path(source,branch,Centered.variable(aq(mid),round91.qball(lo,hi),delta),path)
 if not all(strict_sign(x.value)==1 for x in (full[2],-full[3],-full[4],full[5],full[6],full[7])):raise RuntimeError("full-path sign")
 t=full[0].value;p=full[1].value;t0,t1=round91.arb_bounds(t);p0,p1=round91.arb_bounds(p);return (t0,t1,p0,p1),path
def physical_box(source,index,branch,qa,qb,cores):
 box,path=centered_box(source,branch,qa,qb);atom=step1.Atom(index,source,*box,Q(0),Q(0),"round95");first_hit.certify_first_hit_patch(atom.phase_box,source.target_id);_,_,_,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,cores)
 if state1 is None or owner2 is None or owner2["selected_target_id"]!=branch[1]:raise RuntimeError("second owner")
 state2=time3.second_outgoing_state(atom,state1,owner2)
 if state2 is None:raise RuntimeError("second state")
 status,sign,rows,repairs=round92.centered_physical_type(state2,source,branch[1],branch[2],box)
 if status!="PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or sign!=branch[3]:raise RuntimeError(status)
 return box,path,digest(rows),digest(repairs)
def cover(source,index,branch,qa,qb,cores):
 pending=[(qa,qb,0)];leaves=[];failures=[]
 while pending:
  a,b,depth=pending.pop()
  try:box,path=centered_box(source,branch,a,b)
  except (AssertionError,RuntimeError,ValueError,ZeroDivisionError) as exc:
   if depth==MAX_DEPTH:failures.append((str(a),str(b),type(exc).__name__,str(exc)));continue
   m=(a+b)/2;pending.extend(((m,b,depth+1),(a,m,depth+1)));continue
  leaves.append((str(a),str(b),depth,list(map(str,box)),path))
 return leaves,failures
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin mismatch:{n}")
 f93=json.loads(R93.read_text())["result"];f94=json.loads(R94.read_text())["result"];t94={r["exterior_port_id"]:r for r in f94["transfer_rows"]};events,_=round89.load();physical={r["registered_port_id"]:r for r in events if r["port_is_locally_physical_third_tangency"]};cores=core_cert.physical_cores();round91.round87.WORK_CORES=cores;rows=[]
 for ri,(branch,side,pid) in enumerate(round93.rays(physical)):
  q0,d,ce,inner,seam_outer,kind,oldinner,_=round93.isolate_event(branch,side,pid,physical,cores);segments=[];source=cores[branch[0]];bounds=[ce+(inner-ce)*Q(i,round93.PROBE_COUNT+1) for i in range(round93.PROBE_COUNT+2)];segments.extend((source,q0+d*a,q0+d*b) for a,b in zip(bounds,bounds[1:]))
  if pid in t94:
   tr=t94[pid];source=replace(source,chart_id=f"{source.source}:{tr['adjacent_source_chart']}");end=Q(tr["first_physical_terminal_event_parameter_bracket"][0]);bounds=[seam_outer+(end-seam_outer)*Q(i,round94.PROBE_COUNT+1) for i in range(round94.PROBE_COUNT+2)];segments.extend((source,q0+d*a,q0+d*b) for a,b in zip(bounds,bounds[1:]))
  leaves=[];failures=[]
  for source,a,b in segments:
   x,y=cover(source,branch[0],branch,a,b,cores);leaves+=x;failures+=y
  rows.append({"ray_index":ri,"exterior_port_id":pid,"branch_key":list(branch),"projective_end":side,"input_gap_count":len(segments),"certified_leaf_count":len(leaves),"maximum_split_depth":max((x[2] for x in leaves),default=0),"unresolved_leaf_count":len(failures),"certified_rows_sha256":digest(leaves),"unresolved_rows_sha256":digest(failures),"unresolved_reason_histogram":dict(sorted(Counter(x[2]+":"+x[3] for x in failures).items()))});print(f"round95 {ri+1}/65 unresolved={len(failures)}",file=__import__('sys').stderr,flush=True)
 result={"precision_bits":precision_bits,"input_rank3_ray_count":65,"input_probe_gap_count":sum(r["input_gap_count"] for r in rows),"fully_centered_interval_covered_ray_count":sum(not r["unresolved_leaf_count"] for r in rows),"remaining_unresolved_leaf_count":sum(r["unresolved_leaf_count"] for r in rows),"ray_rows":rows,"ray_rows_sha256":digest(rows),"strict_scope":"centered first-order dual enclosure of the reverse source-coordinate map on every Round94 physical probe gap","strict_nonclaims":["the rectangular t,p hull loses q-correlation and is not a physical-owner certificate","the next layer must propagate the same q dual through owner and competitor comparisons","face quotient and RN/Gate5 installation remain open"],"upstream_pins":PINS};result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
