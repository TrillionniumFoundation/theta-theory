#!/usr/bin/env python3
"""Finite closure attack on the Round-85 C24 refinement frontiers."""
from __future__ import annotations
import hashlib,json,math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas
HERE=Path(__file__).resolve().parent; SCHEMA="cm2.round86.c24-finite-refinement.v1"
FULL=HERE/"cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"; CROSS=HERE/"cm2-round85-c24-variable-return-crosswalk-2026-07-22.json"
PINS={FULL.name:"f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",CROSS.name:"f20e24ed0ef879628ad54c91e7ecb939ea9d870fd6ffbb638f048bce0be54ebc",
"cm2_gate34_full_core_return_adaptive_frontier_cert.py":"d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24","cm2_gate25_physical_return_core_registry_cert.py":"2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"}
def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False)
def dig(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def req(x,s):
 if not x:raise ValueError(s)
def collect(x,out):
 if isinstance(x,dict):
  if "classification"in x and"source_box"in x and"atom_id"in x:out.append(x)
  for y in x.values():collect(y,out)
 elif isinstance(x,list):
  for y in x:collect(y,out)
def vol(a):return(a.t1-a.t0)*(a.p1-a.p0)*(a.s1-a.s0)
def qstr(x):return str(x.numerator)if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def atomrow(a,state,target=None):return {"path":a.path,"t":[str(a.t0),str(a.t1)],"p":[str(a.p0),str(a.p1)],"s":[str(a.s0),str(a.s1)],"state":state,"contained_target_atom_id":target}
def build(bits=512):
 ctx.prec=bits
 for n,h in PINS.items():req(sha(HERE/n)==h,"pin "+n)
 rows=[];collect(json.loads(FULL.read_text()),rows); byid={r["atom_id"]:r for r in rows}; cores_list=core_cert.physical_cores();cores={atlas.core_id(c):c for c in cores_list}
 cross=json.loads(CROSS.read_text())["result"]["evidence"]
 ids=cross["reached_unresolved_atom_ids"]; initial=[]
 for i in ids:
  r=byid[i];b=r["source_box"];c=cores[r["source_core_id"]];initial.append(atlas.Atom(0,c,*map(Q,b["t"]),*map(Q,b["p"]),*map(Q,b["s"]),r["dyadic_path"]))
 v0=sum(map(vol,initial),Q()); leaves=initial; levels=[]
 for level in range(1,13):
  nxt=[]
  for a in leaves:
   z=atlas.classify_atom(a,cores_list)["classification"];nxt.extend(atlas.split_atom(a)if z=="UNRESOLVED_OUTER"else[a])
  leaves=nxt; states=[atlas.classify_atom(a,cores_list)["classification"]for a in leaves];vu=sum(vol(a)for a,z in zip(leaves,states)if z=="UNRESOLVED_OUTER")
  levels.append({"level":level,"leaf_count":len(leaves),"histogram":dict(sorted(Counter(states).items())),"unresolved_volume":qstr(vu),"unresolved_volume_ratio":qstr(vu/v0)})
 req(sum(map(vol,leaves),Q())==v0,"unresolved mass")
 unresolved_rows=[atomrow(a,z)for a,z in zip(leaves,states) if z=="UNRESOLVED_OUTER"]

 # Preimage-guided refinement: resolve whole-enclosure containment in any frozen leaf.
 contained_sources={e[0]for e in cross["edge_rows"] if e[3]=="WHOLE_ENCLOSURE_CONTAINED"}; return_ids={r["atom_id"]for r in rows if r["classification"]=="RETURN_AT_1_INNER"}; boundary=sorted(return_ids-contained_sources);req(len(boundary)==2328,"boundary count")
 bycore={}
 for r in rows:bycore.setdefault(r["source_core_id"],[]).append(r)
 midpoint_bins={};BN=64;BS=16
 for r in rows:
  c=cores[r["source_core_id"]];b=r["source_box"];ranges=[]
  for key,lo,hi,n in (("t",c.t0,c.t1,BN),("p",c.p0,c.p1,BN),("s",core_cert.S_LOWER,core_cert.S_UPPER,BS)):
   x0,x1=map(Q,b[key]);i0=max(0,min(n-1,int((x0-lo)*n/(hi-lo))));i1=max(0,min(n-1,int((x1-lo)*n/(hi-lo))));ranges.append(range(i0,i1+1))
  for it in ranges[0]:
   for ip in ranges[1]:
    for iss in ranges[2]:midpoint_bins.setdefault((r["source_core_id"],it,ip,iss),[]).append(r)
 def target(a,dest):
  g=atlas.atom_geometry(a)
  if g is None:return None
  d=cores[dest];t=atlas.chart_tests(d.chart_id.split(":")[1],g["normal_x"],g["normal_y"])[0];p=g["p_target"]
  tm=float(t.mid());pm=float(p.mid());sm=float((a.s0+a.s1)/2)
  # midpoint proposal; containment is subsequently strict in all coordinates.
  it=max(0,min(BN-1,int((Q(str(tm))-d.t0)*BN/(d.t1-d.t0))));ip=max(0,min(BN-1,int((Q(str(pm))-d.p0)*BN/(d.p1-d.p0))));iss=max(0,min(BS-1,int((Q(str(sm))-core_cert.S_LOWER)*BS/(core_cert.S_UPPER-core_cert.S_LOWER))))
  for r in midpoint_bins.get((dest,it,ip,iss),[]):
   b=r["source_box"];tb=list(map(Q,b["t"]));pb=list(map(Q,b["p"]));sb=list(map(Q,b["s"]))
   if not(float(tb[0])<=tm<=float(tb[1])and float(pb[0])<=pm<=float(pb[1])and float(sb[0])<=sm<=float(sb[1])):continue
   if bool(t>atlas.arbq(tb[0]))and bool(t<atlas.arbq(tb[1]))and bool(p>atlas.arbq(pb[0]))and bool(p<atlas.arbq(pb[1]))and a.s0>=sb[0]and a.s1<=sb[1]:return r["atom_id"]
  return None
 work=[]
 for i in boundary:
  r=byid[i];b=r["source_box"];c=cores[r["source_core_id"]];work.append((atlas.Atom(0,c,*map(Q,b["t"]),*map(Q,b["p"]),*map(Q,b["s"]),r["dyadic_path"]),r["destination_core_id"]))
 pv0=sum(vol(a)for a,_ in work);prelevels=[];resolved=[]
 for level in range(1,4):
  nxt=[]
  for a,d in work:
   hit=target(a,d)
   if hit is not None:resolved.append((a,d,hit))
   else:nxt.extend((x,d)for x in atlas.split_atom(a))
  work=nxt;prelevels.append({"level":level,"newly_or_cumulatively_resolved_leaf_count":len(resolved),"residual_leaf_count":len(work),"residual_volume":qstr(sum(vol(a)for a,_ in work)),"residual_volume_ratio":qstr(sum(vol(a)for a,_ in work)/pv0)})
 req(sum(vol(a)for a,_,_ in resolved)+sum(vol(a)for a,_ in work)==pv0,"preimage mass")
 residual=[atomrow(a,"BOUNDARY_STRADDLING_AFTER_3_SPLITS")|{"destination_core_id":d}for a,d in work]
 evidence={"precision_bits":bits,"unresolved_parent_count":32,"unresolved_parent_volume":qstr(v0),"classification_refinement_levels":levels,"final_classification_leaf_count":len(leaves),"final_survivor_leaf_count":states.count("SURVIVE_THROUGH_1_INNER"),"final_unresolved_leaf_count":states.count("UNRESOLVED_OUTER"),"final_unresolved_volume_ratio":levels[-1]["unresolved_volume_ratio"],"final_unresolved_rows":unresolved_rows,
 "boundary_parent_count":2328,"boundary_parent_volume":qstr(pv0),"preimage_refinement_levels":prelevels,"contained_child_count":len(resolved),"residual_child_count":len(work),"preimage_residual_rows":residual}
 result={"status":"CERTIFIED_FINITE_REFINEMENT_WITH_QUANTIFIED_RESIDUALS","classification_frontier":{"resolved_to_SURVIVE":states.count("SURVIVE_THROUGH_1_INNER"),"unresolved":states.count("UNRESOLVED_OUTER"),"unresolved_volume_ratio":levels[-1]["unresolved_volume_ratio"]},"preimage_frontier":{"contained_children":len(resolved),"residual_children":len(work),"residual_volume_ratio":prelevels[-1]["residual_volume_ratio"]},"mass_preservation":{"classification_cover":True,"preimage_cover":True},"strict_nonpromotion":{"no_recurrent_RETURN_edge_constructed":True,"graph_or_containment_is_not_stable_plaque":True,"Gate2":"NOT_CERTIFIED__0_OF_17","Gate4":"NOT_CERTIFIED__1_OF_7"},"evidence":evidence,"evidence_sha256":dig(evidence)}
 return {"schema":SCHEMA,"pins":dict(PINS),"result":result,"result_sha256":dig(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2,allow_nan=False))
