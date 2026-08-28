#!/usr/bin/env python3
"""Reverse-projective continuation of all 65 live exterior rank-three rays."""
from __future__ import annotations
import hashlib,json,re,sys
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb,ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_round84_reverse_common_tangent_closure_generator as reverse
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign

HERE=Path(__file__).resolve().parent
ROUND90=HERE/"cm2-round90-rank3-tracked-residual-gap-closure-2026-07-22.json"
PINS={ROUND90.name:"7a121a5348e71136e82981fb9d5fed165faf3a3cab23d35a1b2b434536fa5323",
      "cm2_round84_reverse_common_tangent_closure_generator.py":"612ed787a2454ed6447313e182ea97d77062b0f8db3c518eab5e173b926ff073",
      "cm2_round87_rank3_port_event_continuation_cert.py":"71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834"}
SCHEMA="cm2.round91.rank3-exterior-source-exit.v1";PRECISION_BITS=512
NUMBER=re.compile(r"([+-]?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)")

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def qball(a:Q,b:Q)->arb:
 m=(a+b)/2;r=(b-a)/2;return aq(m)+arb(0,aq(r).upper())
def arb_bounds(x:arb)->tuple[Q,Q]:
 s=str(x)
 m=re.fullmatch(r"\[?([+-]?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)(?: \+/- ([0-9.]+(?:e[+-]?[0-9]+)?))?\]?",s)
 if m:
  c=Q(m.group(1));r=Q(m.group(2)) if m.group(2) else Q(0);return c-r,c+r
 m=re.fullmatch(r"\[\+/- ([0-9.]+(?:e[+-]?[0-9]+)?)\]",s)
 if m:return -Q(m.group(1)),Q(m.group(1))
 raise RuntimeError(f"unparsed Arb enclosure: {s}")
def key(row):return round89.key(row)
def q_mid(row)->Q:
 m=NUMBER.match(row["event_equation_evidence"]["projective_q_enclosure"].lstrip("["))
 if not m:raise RuntimeError("q parse")
 return Q(m.group(1))
def tangent_target(branch:tuple[int,str,str,int],qa:Q,qb:Q)->dict[str,arb]:
 q=qball(min(qa,qb),max(qa,qb));ux=(1-q*q)/(1+q*q);uy=2*q/(1+q*q);nx,ny=-uy,ux
 cx,cy=time2.target_center(branch[2],arb(0));radius=Q(9,25) if branch[2][0]=="G" else Q(4,25)
 return {"nx":nx,"ny":ny,"h":nx*cx+ny*cy-arb(branch[3])*aq(radius)}
def inverse_box(branch,qa:Q,qb:Q,cores)->tuple[Q,Q,Q,Q]:
 status,rows,_=reverse.reverse_target(cores[branch[0]],branch[1],tangent_target(branch,qa,qb))
 if status!="INVERSE_PRESENT" or len(rows)!=1:raise RuntimeError(f"reverse interval status {status}/{len(rows)}")
 t0,t1=arb_bounds(rows[0][0]);p0,p1=arb_bounds(rows[0][1]);return t0,t1,p0,p1
def margins(branch,q:Q,cores)->list[arb]:
 status,rows,_=reverse.reverse_target(cores[branch[0]],branch[1],tangent_target(branch,q,q))
 if status!="INVERSE_PRESENT" or len(rows)!=1:raise RuntimeError("point reverse branch")
 t,p=rows[0];c=cores[branch[0]]
 return [t-aq(c.t0),aq(c.t1)-t,p-aq(c.p0),aq(c.p1)-p]

def certify_ray(branch,side,port_id,physical,cores)->dict[str,Any]:
 q0=q_mid(physical[port_id]);direction=-1 if side=="LEFT_PROJECTIVE_END" else 1
 start=margins(branch,q0,cores)
 if any(strict_sign(x)!=1 for x in start):raise RuntimeError("exterior start not strict core interior")
 outside_step=None;outside=None
 for exponent in range(-12,3):
  step=Q(10)**exponent;candidate=margins(branch,q0+direction*step,cores)
  if any(strict_sign(x)==-1 for x in candidate):outside_step,outside=step,candidate;break
 if outside_step is None:raise RuntimeError("no source exit through q range")
 roots=[]
 for index,value in enumerate(outside):
  if strict_sign(value)!=-1:continue
  lo,hi=Q(0),outside_step;ls=1
  for _ in range(112):
   mid=(lo+hi)/2;ms=strict_sign(margins(branch,q0+direction*mid,cores)[index])
   if ms==0:raise RuntimeError("source-boundary bisection indeterminate")
   if ms==ls:lo=mid
   else:hi=mid
  roots.append((lo,hi,index))
 if not roots:raise RuntimeError("no crossed source boundary")
 roots.sort(key=lambda x:x[0]);first=[roots[0]]
 for root in roots[1:]:
  if root[0]<first[0][1] and first[0][0]<root[1]:first.append(root)
  else:break
 exit_lower=min(r[0] for r in first);labels=("T_LOWER","T_UPPER","P_LOWER","P_UPPER")
 chain=None
 last_reason="NO_ATTEMPT"
 for strips in (16,32,64,128,256,512,1024,2048,4096,8192,16384,32768):
  boxes=[];events=[];ok=True
  for i in range(strips):
   xa=exit_lower*Q(i,strips);xb=exit_lower*Q(i+1,strips);qa=q0+direction*xa;qb=q0+direction*xb
   try:box=inverse_box(branch,qa,qb,cores)
   except RuntimeError as exc:last_reason=str(exc);ok=False;break
   c=cores[branch[0]]
   box=(max(box[0],c.t0),min(box[1],c.t1),max(box[2],c.p0),min(box[3],c.p1))
   if box[0]>box[1] or box[2]>box[3]:last_reason="INVERSE_BOX_DISJOINT_FROM_CORE";ok=False;break
   try:
    atom=step1.Atom(branch[0],c,*box,Q(0),Q(0),f"round91:{strips}:{i}")
    classification,_,destination,state1,owner2=time3.homogeneity_cert.classify_with_geometry(atom,cores)
    if classification!="SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"]!=branch[1]:last_reason="TWO_COLLISION_OWNER";ok=False;break
    state2=time3.second_outgoing_state(atom,state1,owner2)
    if state2 is None:last_reason="SECOND_STATE";ok=False;break
    status,evidence=round87.physical_type(state2,branch[1],branch[2])
    if status!="PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or evidence["signed_transverse_tangency_factor_sign"]!=branch[3]:last_reason=status;ok=False;break
   except RuntimeError as exc:last_reason="RUNTIME:"+str(exc);ok=False;break
   except (ValueError,ZeroDivisionError) as exc:last_reason=type(exc).__name__;ok=False;break
   boxes.append(list(map(str,box)));events.append(evidence["competitor_rows_sha256"])
  if ok:chain=(strips,boxes,events);break
 if chain is None:raise RuntimeError(f"failed physical q-chain: {branch}/{side}/{last_reason}")
 return {"exterior_port_id":port_id,"source_core_index":branch[0],"second_selected_target_id":branch[1],"third_candidate_id":branch[2],
         "signed_transverse_tangency_factor_sign":branch[3],"projective_end":side,"outward_q_direction_sign":direction,
         "source_exit_boundary_type":"SOURCE_CORE_"+"_AND_".join(labels[r[2]] for r in first),
         "exit_parameter_brackets":[[str(r[0]),str(r[1]),labels[r[2]]] for r in first],"root_bisection_depth":112,
         "physical_chain_strip_count":chain[0],"physical_chain_boxes_sha256":digest(chain[1]),"physical_chain_competitor_rows_sha256":digest(chain[2]),
         "whole_open_ray_status":"PHYSICAL_NEXT_TANGENCY_UNTIL_SOURCE_CORE_EXIT"}

def build(precision_bits:int=PRECISION_BITS)->dict[str,Any]:
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin mismatch: {n}")
 round90=json.loads(ROUND90.read_text());events,pairs=round89.load();physical={r["registered_port_id"]:r for r in events if r["port_is_locally_physical_third_tangency"]}
 by=defaultdict(list)
 for p,r in physical.items():by[key(r)].append(p)
 for ids in by.values():ids.sort(key=lambda p:float(round89.qball(physical[p]).mid()))
 caps={(tuple(r["branch_key"]),r["projective_end"]) for r in round90["result"]["source_cap_rows"]};rays=[]
 for branch,ids in sorted(by.items()):
  for side,p in (("LEFT_PROJECTIVE_END",ids[0]),("RIGHT_PROJECTIVE_END",ids[-1])):
   if (branch,side) not in caps:rays.append((branch,side,p))
 if len(rays)!=65:raise RuntimeError("exterior ray accounting")
 cores=core_cert.physical_cores();round87.WORK_CORES=cores
 rows=[];unresolved=[]
 for branch,side,p in rays:
  try:rows.append(certify_ray(branch,side,p,physical,cores))
  except RuntimeError as exc:unresolved.append({"exterior_port_id":p,"branch_key":list(branch),"projective_end":side,"reason":str(exc).rsplit('/',1)[-1]})
 hist=Counter(r["source_exit_boundary_type"] for r in rows);strips=Counter(r["physical_chain_strip_count"] for r in rows)
 result={"precision_bits":precision_bits,"input_exterior_projective_ray_count":65,"certified_source_exit_ray_count":len(rows),
         "remaining_untyped_exterior_ray_count":65-len(rows),"unresolved_reason_histogram":dict(sorted(Counter(r["reason"] for r in unresolved).items())),
         "unresolved_ray_rows":unresolved,"unresolved_ray_rows_sha256":digest(unresolved),"source_exit_type_histogram":dict(sorted(hist.items())),
         "physical_chain_strip_count_histogram":dict(sorted(strips.items())),"ray_rows":rows,"ray_rows_sha256":digest(rows),
         "complete_rank3_projective_branch_continuation_within_frozen_source_cores":len(rows)==65,
         "strict_scope":f"reverse-projective physical continuation of {len(rows)} of 65 exterior rays to their first frozen source-core boundary",
         "strict_nonclaims":["source-core boundaries are frozen-domain endpoints, not automatically global physical-face endpoints","no continuation beyond the source-core registry is asserted","no RN or Gate5 row is installed"],"upstream_pins":PINS}
 if len(rows)+len(unresolved)!=65:raise RuntimeError("exterior accounting")
 result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
def main():json.dump(build(),sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
