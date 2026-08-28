#!/usr/bin/env python3
"""Promote the original wall-crossing-time roots to whole-origin signatures."""

from __future__ import annotations
import argparse, hashlib, json, os, stat, tempfile
from pathlib import Path
from typing import Any
from flint import arb

H=Path(__file__).resolve().parent
OUT=H/"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json"
P={"cm2_round179_source_g_residual_tube_arrangement_rows.json":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42","cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974","cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":"88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73","cm2_round179_source_g_residual_tube_arrangement.py":"8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"}
def need(x:bool,s:str)->None:
 if not x:raise RuntimeError(s)
def can(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def dg(x:Any)->str:return hashlib.sha256(can(x)).hexdigest()
def raw(n:str)->bytes:
 p=H/n;i=p.lstat();need(stat.S_ISREG(i.st_mode)and not p.is_symlink()and i.st_nlink==1,"regular:"+n);b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==P[n],"pin:"+n);return b
def load(n:str)->dict[str,Any]:
 d=json.loads(raw(n));need(set(d)=={"schema","result","result_sha256"}and dg(d["result"])==d["result_sha256"],"envelope:"+n);return d["result"]
def unpack(d:dict[str,Any],n:str)->list[dict[str,Any]]:
 c=d["row_column_schemas"][n];return[dict(zip(c,r,strict=True))for r in d[n]]
def sig(r:dict[str,Any])->dict[str,Any]:return{"source_chart":r["chart"],"target_lift":r["owner_target"],"ordered_integer_wall_events":r["ordered_integer_wall_events"],"signed_wall_word":r["signed_wall_word"],"roof":r["roof"],"outgoing_cell":r["outgoing_cell"],"target_chart":r["target_chart"],"official_key_row":r["official_key_row"],"official_key_ordinal":r["official_key_ordinal"],"official_key_id":r["official_key_id"]}
def write(b:bytes)->None:
 f,n=tempfile.mkstemp(prefix=".r237.",suffix=".tmp",dir=H);p=Path(n)
 try:
  with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
  os.replace(p,OUT)
 finally:
  if p.exists():p.unlink()

def build()->dict[str,Any]:
 for n in P:raw(n)
 import cm2_round179_source_g_residual_tube_arrangement as r179
 a=load("cm2_round179_source_g_residual_tube_arrangement_rows.json");ret={r["row_id"]:r for r in unpack(a,"retained_3d_child_rows")};res={r["row_id"]:r for r in unpack(a,"resolved_3d_child_rows")};orig={r["origin_row_id"]:r for r in unpack(a,"origin_tube_rows")};b=load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json");t=b["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"];interfaces=[]
 for packed in t["rows"]:
  r=dict(zip(t["columns"],packed,strict=True))
  if{r["lower_child_kind"],r["upper_child_kind"]}!={"RESOLVED","RETAINED"}:continue
  rid=r["upper_child_row_id"]if r["upper_child_kind"]=="RETAINED"else r["lower_child_row_id"];interfaces.append((r,ret[rid]))
 r230=load("cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json");accepted={r["Round220_split_interface_id"]for r in r230["formal_certified_local_bulk_bridge_star_ledger"]["rows"]};roots=[(i,r)for i,r in interfaces if i["split_interface_id"]not in accepted and len(r["reason_labels"])==1 and r["reason_labels"][0].startswith("wall_crossing_time_not_strict:")];need(len(roots)==240,"root census");rows=[]
 for interface,r in roots:
  iid=interface["split_interface_id"];origin=orig[r["origin_row_id"]];need((origin["resolved_child_count"],origin["retained_child_count"],origin["guard_child_count"])==(1,1,0),"partition:"+iid);reason=r["reason_labels"][0];_,axis,wtext=reason.split(":");wall=int(wtext);owner=origin["owner_target"];box=r179.box_from(r["box"],len(r["refinement_path"]),r["row_id"]);g=r179.interval_geometry(r["chart"],owner,box);source=g["source_x"][0]if axis=="X"else g["source_y"][0];target=g["hit_x"][0]if axis=="X"else g["hit_y"][0];ss,ts=r179.sign(source-arb(wall)),r179.sign(target-arb(wall));need({ss,ts}=={"STRICT_NEGATIVE","STRICT_POSITIVE"},"endpoints:"+iid);token=axis+("+"if ss=="STRICT_NEGATIVE"else"-");time=(arb(wall)-source)/(target-source);sid=interface["lower_child_row_id"]if interface["lower_child_kind"]=="RESOLVED"else interface["upper_child_row_id"];signature=sig(res[sid]);need([token,wall]in signature["ordered_integer_wall_events"],"event:"+iid);others=[]
  for tok,w in signature["ordered_integer_wall_events"]:
   if[tok,w]==[token,wall]:continue
   os=g["source_x"][0]if tok[0]=="X"else g["source_y"][0];ot=g["hit_x"][0]if tok[0]=="X"else g["hit_y"][0];others.append((arb(w)-os)/(ot-os))
  before=all(bool(time<x)for x in others);after=all(bool(time>x)for x in others);need(before or after,"order:"+iid);position="STRICT_FIRST"if before else"STRICT_LAST"
  rows.append({"whole_origin_promotion_row_id":"round237-crossing:"+dg(iid),"Round220_split_interface_id":iid,"origin_row_id":r["origin_row_id"],"Round179_resolved_sibling_row_id":sid,"Round179_retained_child_row_id":r["row_id"],"reason_label":reason,"axis":axis,"wall":wall,"source_endpoint_sign":ss,"target_endpoint_sign":ts,"transition_event":[token,wall],"exact_endpoint_opposition_proves_crossing_time_in_open_unit_interval":True,"event_order_position":position,"strictly_compared_other_event_count":len(others),"whole_origin_local_return_signature":signature,"whole_origin_local_return_signature_credit":1,"known_block_incidence_credit":0,"global_exact_key_fibre_credit":0})
 rows.sort(key=lambda r:r["whole_origin_promotion_row_id"]);return{"status":"CERTIFIED_240_CROSSING_TIME_WHOLE_ORIGIN_RETURN_SIGNATURES","census":{"crossing_time_root_count":len(rows),"strict_opposite_endpoint_count":len(rows),"strict_event_order_count":len(rows),"distinct_exact_key_count":len({r["whole_origin_local_return_signature"]["official_key_ordinal"]for r in rows}),"event_order_position_histogram":{k:sum(r["event_order_position"]==k for r in rows)for k in("STRICT_FIRST","STRICT_LAST")}},"whole_origin_promotion_rows_sha256":dg(rows),"whole_origin_promotion_rows":rows,"strict_nonpromotion":{"known_block_incidence_credit":0,"physical_component_credit":0,"maximal_physical_component_credit":0,"global_exact_key_fibre_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"close 264 source-chart-seam roots, then attach all 8512 classified interfaces to common-refinement strata and known blocks"}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=build();d={"schema":"cm2.round237.source-g-crossing-time-whole-origin-promotion.v1","result":r,"result_sha256":dg(r)};b=can(d)+b"\n"
 if not x.no_write:write(b)
 print(r["status"]);print(json.dumps(r["census"],sort_keys=True));print("result_sha256="+d["result_sha256"]);print("certificate_sha256="+hashlib.sha256(b).hexdigest());return 0
if __name__=="__main__":raise SystemExit(main())
