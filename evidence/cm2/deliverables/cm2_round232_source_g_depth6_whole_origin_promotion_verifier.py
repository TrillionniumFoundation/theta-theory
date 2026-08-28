#!/usr/bin/env python3
"""Independent verifier for Round232 whole-origin local promotions."""
from __future__ import annotations
import argparse,hashlib,json,os,stat,tempfile
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import sys
from typing import Any
H=Path(__file__).resolve().parent
OUT=H/"cm2_round232_source_g_depth6_whole_origin_promotion_verification.json"
SC="cm2.round232.source-g-depth6-whole-origin-promotion.v1"
P={"cm2_round179_source_g_residual_tube_arrangement_rows.json":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42","cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974","cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json":"7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374","cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json":"a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"}
def need(x:bool,s:str)->None:
 if not x:raise RuntimeError(s)
def can(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def dg(x:Any)->str:return hashlib.sha256(can(x)).hexdigest()
def load(n:str)->tuple[dict[str,Any],bytes]:
 p=H/n;i=p.lstat();need(stat.S_ISREG(i.st_mode)and not p.is_symlink()and i.st_nlink==1,"regular:"+n);b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==P[n],"pin:"+n);d=json.loads(b);need(set(d)=={"schema","result","result_sha256"}and dg(d["result"])==d["result_sha256"],"envelope:"+n);return d["result"],b
def tab(d:dict[str,Any],n:str)->list[dict[str,Any]]:
 c=d["row_column_schemas"][n];return[dict(zip(c,r,strict=True))for r in d[n]]
def sig(r:dict[str,Any])->dict[str,Any]:return{"source_chart":r["chart"],"target_lift":r["owner_target"],"ordered_integer_wall_events":r["ordered_integer_wall_events"],"signed_wall_word":r["signed_wall_word"],"roof":r["roof"],"outgoing_cell":r["outgoing_cell"],"target_chart":r["target_chart"],"official_key_row":r["official_key_row"],"official_key_ordinal":r["official_key_ordinal"],"official_key_id":r["official_key_id"]}
def safe(b:bytes)->None:
 f,n=tempfile.mkstemp(prefix=".round232v.",suffix=".tmp",dir=H);p=Path(n)
 try:
  with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
  os.replace(p,OUT)
 finally:
  if p.exists():p.unlink()
def verify()->dict[str,Any]:
 a,_=load("cm2_round179_source_g_residual_tube_arrangement_rows.json");b,_=load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json");c,_=load("cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json");candidate,raw=load("cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json")
 source=H/"cm2_round179_source_g_residual_tube_arrangement.py";need(hashlib.sha256(source.read_bytes()).hexdigest()=="8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab","kernel source pin")
 import cm2_round179_source_g_residual_tube_arrangement as kernel
 need(Path(kernel.__file__).resolve()==source.resolve(),"kernel identity");registry=kernel.load_inputs()["registry"]
 need(candidate["status"]=="CERTIFIED_2220_WHOLE_ORIGIN_LOCAL_RETURN_SIGNATURES_ZERO_GLOBAL_PROMOTION","status");need(candidate["whole_origin_promotion_rows_sha256"]==dg(candidate["whole_origin_promotion_rows"]),"rows hash")
 full={x["Round220_split_interface_id"]:x for x in c["root_summary_rows"]if x["depth6_retained_frontier_count"]==0};need(len(full)==2220,"full")
 desc=defaultdict(list)
 for x in c["resolved_descendant_rows"]:
  if x["Round220_split_interface_id"]in full:desc[x["Round220_split_interface_id"]].append(x)
 origins={x["origin_row_id"]:x for x in tab(a,"origin_tube_rows")};resolved={x["row_id"]:x for x in tab(a,"resolved_3d_child_rows")};retained={x["row_id"]:x for x in tab(a,"retained_3d_child_rows")}
 t=b["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"];ifs={}
 for z in t["rows"]:
  x=dict(zip(t["columns"],z,strict=True));iid=x["split_interface_id"]
  if iid not in full:continue
  rid=x["lower_child_row_id"]if x["lower_child_kind"]=="RESOLVED"else x["upper_child_row_id"];tid=x["upper_child_row_id"]if x["upper_child_kind"]=="RETAINED"else x["lower_child_row_id"];ifs[iid]=(rid,tid)
 got={x["Round220_split_interface_id"]:x for x in candidate["whole_origin_promotion_rows"]};need(set(got)==set(full)and len(got)==2220,"row universe")
 keys=set();total_desc=0
 for iid in sorted(full):
  rid,tid=ifs[iid];o=origins[retained[tid]["origin_row_id"]];s=sig(resolved[rid]);ds=desc[iid];r=got[iid]
  need(o["resolved_child_count"]==1 and o["retained_child_count"]==1 and o["guard_child_count"]==0 and o["original_reason_labels"]==["outgoing_chart_seam"],"partition:"+iid)
  need(ds and all(x["local_return_signature"]==s for x in ds),"signature:"+iid)
  for x in ds:
   box=kernel.box_from(x["box"],x["adaptive_depth"],x["materialized_row_id"]);kind,data=kernel.r174.classify_child(x["chart"],box,x["owner_target"],registry)
   recomputed={"source_chart":x["chart"],"target_lift":x["owner_target"],"ordered_integer_wall_events":data["events"],"signed_wall_word":list(data["pattern"]),"roof":data["roof"],"outgoing_cell":data["outgoing"],"target_chart":data["target_chart"],"official_key_row":data["key"]["row"],"official_key_ordinal":data["key"]["ordinal"],"official_key_id":data["key"]["identifier"]}if kind=="resolved"else None
   need(kind=="resolved"and recomputed==x["local_return_signature"],"interval recomputation:"+x["materialized_row_id"])
  need(sum((Q(x["coordinate_volume"])for x in ds),Q(0))==Q(retained[tid]["coordinate_volume"]),"retained volume:"+iid)
  need(Q(resolved[rid]["coordinate_volume"])+Q(retained[tid]["coordinate_volume"])==Q(o["original_coordinate_volume"]),"origin volume:"+iid)
  expected_id="round232-whole-origin:"+dg([iid,o["origin_row_id"],s])
  need(r["whole_origin_promotion_row_id"]==expected_id and r["origin_row_id"]==o["origin_row_id"]and r["Round179_resolved_child_row_id"]==rid and r["Round179_retained_child_row_id"]==tid and r["Round231_resolved_descendant_count"]==len(ds)and r["Round231_resolved_descendant_ids_sha256"]==dg(sorted(x["materialized_row_id"]for x in ds))and r["local_return_signature"]==s,"binding:"+iid)
  need(r["whole_origin_local_return_signature_credit"]==1 and r["whole_origin_positive_3D_occurrence_credit"]==1 and r["known_block_incidence_credit"]==r["physical_component_credit"]==r["maximal_physical_component_credit"]==r["global_exact_key_disposition_credit"]==0,"credits:"+iid)
  keys.add(s["official_key_ordinal"]);total_desc+=len(ds)
 need(candidate["census"]=={"promoted_whole_origin_count":2220,"promoted_round231_descendant_count":total_desc,"distinct_exact_key_count":len(keys),"known_block_incidence_count":0,"global_exact_key_disposition_count":0},"census")
 need(candidate["scope_contract"]["local_whole_origin_credit_is_not_global_fibre_credit"]is True and candidate["scope_contract"]["known_block_or_component_assignment_proved"]is False and all(v==0 for k,v in candidate["strict_nonpromotion"].items()if k!="CM2")and candidate["strict_nonpromotion"]["CM2"]=="NO-GO_FOR_CLAIM","nonpromotion")
 return{"status":"PASS_INDEPENDENT_ROUND232","promoted_whole_origin_count":2220,"promoted_descendant_count":total_desc,"independently_recomputed_interval_descendant_count":total_desc,"distinct_exact_key_count":len(keys),"candidate_sha256":hashlib.sha256(raw).hexdigest(),"candidate_result_sha256":dg(candidate)}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=verify();d={"schema":"cm2.round232.source-g-depth6-whole-origin-promotion-verification.v1","result":r,"result_sha256":dg(r)};b=can(d)+b"\n";
 if not x.no_write:safe(b)
 print(r["status"]);print(json.dumps(r,sort_keys=True));print("verification_result_sha256="+d["result_sha256"]);return 0
if __name__=="__main__":raise SystemExit(main())
