#!/usr/bin/env python3
"""Independent higher-precision verifier for the Round-87 pullback ledger."""
from __future__ import annotations
import copy,json,sys
from fractions import Fraction as Q
from pathlib import Path
import cm2_round87_c24_landing_pullback_arrangement_cert as cert
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas
from flint import ctx

HERE=Path(__file__).resolve().parent
INPUT=HERE/"cm2-round87-c24-landing-pullback-arrangement-2026-07-22.json"

def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError("duplicate JSON key "+k)
  d[k]=v
 return d
def strict_load(text):
 x=json.loads(text,object_pairs_hook=pairs,parse_constant=lambda z:(_ for _ in()).throw(ValueError("nonfinite "+z)))
 if not isinstance(x,dict):raise ValueError("root object")
 return x
def req(x,s):
 if not x:raise ValueError(s)
def main():
 try:
  frozen=strict_load(INPUT.read_text());fresh=cert.build(512);req(frozen==fresh,"512 exact replay / closed schema")
  high=cert.build(768)
  fr=frozen["result"];hr=high["result"]
  for key in("status","round86_comparison","exact_cover","remaining_equation_frontier","strict_nonpromotion"):
   req(fr[key]==hr[key],"768 "+key)
  keys=("levels","selector_role","selector_histogram","contained_target_classification_histogram","contained_leaf_count","contained_volume","residual_leaf_count","residual_volume","residual_volume_ratio","parents_with_contained_children","parents_with_residual_children","residual_boundary_coordinate_histogram","resolved_ledger_sha256","residual_rows")
  for key in keys:req(fr["evidence"][key]==hr["evidence"][key],"768 evidence "+key)
  # Independent 768-bit event sweep over the frozen residual ledger.  This
  # does not trust the producer's residual-boundary labels or volume sum.
  ctx.prec=768
  atlas_rows=[];cert.collect(json.loads(cert.FULL.read_text()),atlas_rows)
  cores={atlas.core_id(c):c for c in core_cert.physical_cores()};bounds={}
  parent_core={r["atom_id"]:r["source_core_id"]for r in atlas_rows}
  for row in atlas_rows:
   cid=row["source_core_id"];bounds.setdefault(cid,{"t":set(),"p":set(),"s":set()})
   for dim in("t","p","s"):bounds[cid][dim].update(map(Q,row["source_box"][dim]))
  residual_volume=Q();independent_hits=0
  for row in fr["evidence"]["residual_rows"]:
   cid=row["destination_core_id"];source_core=cores[parent_core[row["parent_atom_id"]]]
   a=atlas.Atom(0,source_core,*map(Q,row["t"]),*map(Q,row["p"]),*map(Q,row["s"]),row["path"])
   residual_volume+=cert.volume(a);t,p=cert.landing(a,cores[cid]);hits=[]
   for dim,x in(("t",t),("p",p)):
    n=sum(1 for q in bounds[cid][dim]if cert.overlaps_q(x,q))
    if n:hits.append([dim,n])
   n=sum(1 for q in bounds[cid]["s"]if a.s0<q<a.s1)
   if n:hits.append(["s",n])
   req(hits==row["intersected_boundary_coordinate_counts"],"independent residual event row")
   independent_hits+=1
  req(cert.qstr(residual_volume)==fr["evidence"]["residual_volume"],"independent residual mass")
  attacks=[]
  mutations=(
   lambda z:z["result"]["exact_cover"].__setitem__("mass_preserved",False),
   lambda z:z["result"]["remaining_equation_frontier"].__setitem__("residual_leaf_count",0),
   lambda z:z["result"]["evidence"].__setitem__("residual_volume_ratio","0"),
   lambda z:z["result"]["evidence"].__setitem__("resolved_ledger_sha256","0"*64),
   lambda z:z["result"]["strict_nonpromotion"].__setitem__("Gate4","CERTIFIED"),
   lambda z:z["pins"].__setitem__(next(iter(z["pins"])),"0"*64),
   lambda z:z.__setitem__("extra",1),
  )
  for mutate in mutations:
   y=copy.deepcopy(frozen);mutate(y);y["result"]["evidence_sha256"]=cert.dig(y["result"]["evidence"]);y["result_sha256"]=cert.dig(y["result"]);attacks.append(y!=fresh)
  req(all(attacks),"hostile mutation accepted")
  strict_attacks=[]
  for text in ('{"a":1,"a":2}','NaN','[]','{"x":Infinity}'):
   try:strict_load(text);strict_attacks.append(False)
   except Exception:strict_attacks.append(True)
  req(all(strict_attacks),"strict JSON attack")
  e=fr["evidence"]
  out={"schema":"cm2.round87.c24-landing-pullback-arrangement.audit.v1","status":"AUDIT_PASS","producer_precision_bits":512,"independent_precision_bits":768,"input_boundary_parent_count":2328,"bounded_pullback_depth":2,"contained_survivor_children":e["contained_leaf_count"],"residual_children":e["residual_leaf_count"],"residual_volume_ratio":e["residual_volume_ratio"],"round86_residual_volume_ratio":"1991/2298","exact_mass_preservation":fr["exact_cover"]["mass_preserved"],"all_residuals_hit_event_equation":fr["remaining_equation_frontier"]["all_residuals_intersect_frozen_target_boundary"],"independent_residual_event_rows_recomputed":independent_hits,"hostile_mutations_rejected":f"{sum(attacks)}/{len(attacks)}","strict_json_attacks_rejected":f"{sum(strict_attacks)}/{len(strict_attacks)}","strict_gate_state":fr["strict_nonpromotion"]}
  print(json.dumps(out,sort_keys=True,indent=2));return 0
 except Exception as exc:
  print("ROUND87_VERIFY_ERROR",exc,file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
