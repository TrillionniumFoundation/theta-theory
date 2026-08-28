#!/usr/bin/env python3
"""Interval-certified pullback refinement of frozen C24 leaf boundaries."""
from __future__ import annotations
import hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas

HERE=Path(__file__).resolve().parent
SCHEMA="cm2.round87.c24-landing-pullback-arrangement.v1"
FULL=HERE/"cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
CROSS=HERE/"cm2-round85-c24-variable-return-crosswalk-2026-07-22.json"
R86=HERE/"cm2-round86-c24-finite-refinement-2026-07-22.json"
PINS={FULL.name:"f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",CROSS.name:"f20e24ed0ef879628ad54c91e7ecb939ea9d870fd6ffbb638f048bce0be54ebc",R86.name:"c7d5dfc6fb960c315de3692f45e7ab5f2dbd2e84cc7f4b8b5602d525af005e7b","cm2_round86_c24_finite_refinement_cert.py":"ee16678567c14057992255714bcd26b424b03a93ad8f3ed4cbe0868e40e37c44","cm2_gate34_full_core_return_adaptive_frontier_cert.py":"d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24","cm2_gate25_physical_return_core_registry_cert.py":"2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"}
BN,BS,MAX_DEPTH=64,16,2
def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False)
def dig(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def req(x,s):
 if not x:raise ValueError(s)
def qstr(x):return str(x.numerator)if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def collect(x,out):
 if isinstance(x,dict):
  if "classification"in x and"source_box"in x and"atom_id"in x:out.append(x)
  for y in x.values():collect(y,out)
 elif isinstance(x,list):
  for y in x:collect(y,out)
def volume(a):return(a.t1-a.t0)*(a.p1-a.p0)*(a.s1-a.s0)
def split_dim(a,dim):
 b=[a.t0,a.t1,a.p0,a.p1,a.s0,a.s1];i={"t":(0,1),"p":(2,3),"s":(4,5)}[dim];m=(b[i[0]]+b[i[1]])/2;l=list(b);r=list(b);l[i[1]]=m;r[i[0]]=m
 return atlas.Atom(0,a.source_core,*l,a.path+dim+"0"),atlas.Atom(0,a.source_core,*r,a.path+dim+"1")
def landing(a,d):
 g=atlas.atom_geometry(a);req(g is not None,"lost collision geometry")
 return atlas.chart_tests(d.chart_id.split(":")[1],g["normal_x"],g["normal_y"])[0],g["p_target"]
def width(x):return float(x.upper())-float(x.lower())
def overlaps_q(x,q):
 # Rigorous interval/rational overlap: both strict interval separators fail.
 y=atlas.arbq(q);return not bool(x<y)and not bool(x>y)

def build(bits=512,max_depth=MAX_DEPTH):
 ctx.prec=bits
 for n,h in PINS.items():req(sha(HERE/n)==h,"pin "+n)
 r86=json.loads(R86.read_text());req(r86["result"]["preimage_frontier"]=={"contained_children":1304,"residual_children":15344,"residual_volume_ratio":"1991/2298"},"Round86 frontier")
 rows=[];collect(json.loads(FULL.read_text()),rows);cores_list=core_cert.physical_cores();cores={atlas.core_id(c):c for c in cores_list}
 cross=json.loads(CROSS.read_text())["result"]["evidence"];contained_sources={e[0]for e in cross["edge_rows"]if e[3]=="WHOLE_ENCLOSURE_CONTAINED"}
 source_rows=sorted((r for r in rows if r["classification"]=="RETURN_AT_1_INNER"and r["atom_id"]not in contained_sources),key=lambda r:r["atom_id"]);req(len(source_rows)==2328,"parent count")
 bins={};boundaries={}
 for r in rows:
  cid=r["source_core_id"];c=cores[cid];b=r["source_box"];boundaries.setdefault(cid,{"t":set(),"p":set(),"s":set()})
  for dim in("t","p","s"):boundaries[cid][dim].update(map(Q,b[dim]))
  rr=[]
  for dim,lo,hi,n in(("t",c.t0,c.t1,BN),("p",c.p0,c.p1,BN),("s",core_cert.S_LOWER,core_cert.S_UPPER,BS)):
   x0,x1=map(Q,b[dim]);i0=max(0,min(n-1,int((x0-lo)*n/(hi-lo))));i1=max(0,min(n-1,int((x1-lo)*n/(hi-lo))));rr.append(range(i0,i1+1))
  for it in rr[0]:
   for ip in rr[1]:
    for iss in rr[2]:bins.setdefault((cid,it,ip,iss),[]).append(r)
 def proposal(a,cid,t,p):
  d=cores[cid];tm,pm,sm=float(t.mid()),float(p.mid()),float((a.s0+a.s1)/2)
  it=max(0,min(BN-1,int((Q(str(tm))-d.t0)*BN/(d.t1-d.t0))));ip=max(0,min(BN-1,int((Q(str(pm))-d.p0)*BN/(d.p1-d.p0))));iss=max(0,min(BS-1,int((Q(str(sm))-core_cert.S_LOWER)*BS/(core_cert.S_UPPER-core_cert.S_LOWER))))
  return bins.get((cid,it,ip,iss),())
 def contain(a,cid):
  t,p=landing(a,cores[cid])
  for r in proposal(a,cid,t,p):
   b=r["source_box"];t0,t1=map(Q,b["t"]);p0,p1=map(Q,b["p"]);s0,s1=map(Q,b["s"])
   if bool(t>atlas.arbq(t0))and bool(t<atlas.arbq(t1))and bool(p>atlas.arbq(p0))and bool(p<atlas.arbq(p1))and a.s0>=s0 and a.s1<=s1:return r,t,p
  return None,t,p
 selector=Counter()
 def choose(a,cid,t,p):
  # Bounded pullback calibration: test the exact rational bisection of each
  # source coordinate, propagate both children with Arb, and choose the cut
  # whose worst normalized landing diameter is smallest.  The choice is only
  # an efficiency heuristic; validity rests on the exact child cover.
  d=cores[cid];opts=[]
  for order,dim in enumerate(("t","p","s")):
   children=split_dim(a,dim);score=0.0
   for z in children:
    tt,pp=landing(z,d);score=max(score,BN*width(tt)/float(d.t1-d.t0)+BN*width(pp)/float(d.p1-d.p0)+BS*float(z.s1-z.s0)/float(core_cert.S_UPPER-core_cert.S_LOWER))
   opts.append((score,order,dim,children))
  # Float conversion is a deterministic numeric efficiency heuristic only;
  # no correctness or selector-optimality claim depends on this ordering.
  opts.sort(key=lambda z:(z[0],z[1]));selector[opts[0][2]]+=1
  return opts[0][3]
 initial=[]
 for r in source_rows:
  b=r["source_box"];initial.append((atlas.Atom(0,cores[r["source_core_id"]],*map(Q,b["t"]),*map(Q,b["p"]),*map(Q,b["s"]),r["dyadic_path"]),r["destination_core_id"],r["atom_id"]))
 v0=sum((volume(a)for a,_,_ in initial),Q());work=initial;resolved=[];levels=[]
 for depth in range(max_depth+1):
  nxt=[];new=0
  for a,cid,parent in work:
   target,_t,_p=contain(a,cid)
   if target is not None:resolved.append((a,parent,target["atom_id"],target["classification"]));new+=1
   elif depth<max_depth:nxt.extend((z,cid,parent)for z in choose(a,cid,_t,_p))
   else:nxt.append((a,cid,parent))
  work=nxt;vr=sum((volume(a)for a,_,_ in work),Q());levels.append({"depth":depth,"newly_contained":new,"cumulative_contained":len(resolved),"residual_leaf_count":len(work),"residual_volume":qstr(vr),"residual_volume_ratio":qstr(vr/v0)})
  if not work:break
 vr=sum((volume(a)for a,_,_ in work),Q());vc=sum((volume(a)for a,_,_,_ in resolved),Q());req(vc+vr==v0,"mass")
 target_hist=Counter(kind for _,_,_,kind in resolved);parent_resolved={p for _,p,_,_ in resolved};parent_residual={p for _,_,p in work};residual_hit=Counter();residual_rows=[]
 for a,cid,parent in work:
  t,p=landing(a,cores[cid]);hits=[]
  for dim,x in(("t",t),("p",p)):
   n=sum(1 for q in boundaries[cid][dim]if overlaps_q(x,q))
   if n:hits.append([dim,n]);residual_hit[dim]+=1
  n=sum(1 for q in boundaries[cid]["s"]if a.s0<q<a.s1)
  if n:hits.append(["s",n]);residual_hit["s"]+=1
  req(bool(hits),"residual without boundary equation")
  residual_rows.append({"parent_atom_id":parent,"destination_core_id":cid,"path":a.path,"t":[qstr(a.t0),qstr(a.t1)],"p":[qstr(a.p0),qstr(a.p1)],"s":[qstr(a.s0),qstr(a.s1)],"intersected_boundary_coordinate_counts":hits})
 evidence={"precision_bits":bits,"maximum_pullback_depth":max_depth,"input_boundary_parent_count":2328,"input_volume":qstr(v0),"frozen_target_boundary_value_occurrences_by_coordinate":{d:sum(len(x[d])for x in boundaries.values())for d in("t","p","s")},"pullback_equations":["landing_t(t,p,s)=target_t_boundary","landing_p(t,p,s)=target_p_boundary","s=target_s_boundary"],"levels":levels,"selector_role":"DETERMINISTIC_NUMERIC_EFFICIENCY_HEURISTIC_ONLY__NO_OPTIMALITY_OR_VALIDITY_DEPENDS_ON_IT","selector_histogram":dict(sorted(selector.items())),"contained_target_classification_histogram":dict(sorted(target_hist.items())),"contained_leaf_count":len(resolved),"contained_volume":qstr(vc),"residual_leaf_count":len(work),"residual_volume":qstr(vr),"residual_volume_ratio":qstr(vr/v0),"parents_with_contained_children":len(parent_resolved),"parents_with_residual_children":len(parent_residual),"residual_boundary_coordinate_histogram":dict(sorted(residual_hit.items())),"resolved_ledger_sha256":dig(sorted([a.path,p,t,k,qstr(volume(a))]for a,p,t,k in resolved)),"residual_rows":residual_rows}
 result={"status":"CERTIFIED_BOUNDED_LANDING_PULLBACK_EVENT_ARRANGEMENT_WITH_QUANTIFIED_RESIDUAL","round86_comparison":{"round86_blind_three_split_residual_volume_ratio":"1991/2298","round87_is_a_two_cut_event_equation_certificate_not_a_claim_of_deeper_closure":True},"exact_cover":{"input_volume":qstr(v0),"contained_plus_residual_volume":qstr(vc+vr),"mass_preserved":True},"remaining_equation_frontier":{"residual_leaf_count":len(work),"all_residuals_intersect_frozen_target_boundary":True,"equations":evidence["pullback_equations"]},"strict_nonpromotion":{"target_box_containment_is_not_an_orbit_or_stable_plaque":True,"no_RETURN_to_RETURN_edge_constructed":True,"Gate2":"NOT_CERTIFIED__0_OF_17","Gate4":"NOT_CERTIFIED__1_OF_7"},"evidence":evidence,"evidence_sha256":dig(evidence)}
 return{"schema":SCHEMA,"pins":dict(PINS),"result":result,"result_sha256":dig(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2,allow_nan=False))
