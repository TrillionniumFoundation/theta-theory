#!/usr/bin/env python3
"""Promote the source-chart-seam roots by exact atlas-side partition."""
from __future__ import annotations
import argparse,hashlib,json,os,stat,tempfile
from pathlib import Path
from typing import Any
H=Path(__file__).resolve().parent;OUT=H/"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json"
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
def kernel_sig(chart:str,owner:str,s:dict[str,Any])->dict[str,Any]:return{"source_chart":chart,"target_lift":owner,"ordered_integer_wall_events":s["events"],"signed_wall_word":list(s["pattern"]),"roof":s["roof"],"outgoing_cell":s["outgoing"],"target_chart":s["target_chart"],"official_key_row":s["key"]["row"],"official_key_ordinal":s["key"]["ordinal"],"official_key_id":s["key"]["identifier"]}
def write(b:bytes)->None:
 f,n=tempfile.mkstemp(prefix=".r238.",suffix=".tmp",dir=H);p=Path(n)
 try:
  with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
  os.replace(p,OUT)
 finally:
  if p.exists():p.unlink()
def build()->dict[str,Any]:
 for n in P:raw(n)
 import cm2_round179_source_g_residual_tube_arrangement as r179
 reg=r179.load_inputs()["registry"];a=load("cm2_round179_source_g_residual_tube_arrangement_rows.json");ret={r["row_id"]:r for r in unpack(a,"retained_3d_child_rows")};res={r["row_id"]:r for r in unpack(a,"resolved_3d_child_rows")};orig={r["origin_row_id"]:r for r in unpack(a,"origin_tube_rows")};seams={r["origin_row_id"]:r for r in unpack(a,"source_chart_seam_rows")};b=load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json");t=b["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"];ints=[]
 for packed in t["rows"]:
  r=dict(zip(t["columns"],packed,strict=True))
  if{r["lower_child_kind"],r["upper_child_kind"]}=={"RESOLVED","RETAINED"}:rid=r["upper_child_row_id"]if r["upper_child_kind"]=="RETAINED"else r["lower_child_row_id"];ints.append((r,ret[rid]))
 r230=load("cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json");acc={r["Round220_split_interface_id"]for r in r230["formal_certified_local_bulk_bridge_star_ledger"]["rows"]};roots=[(i,r)for i,r in ints if i["split_interface_id"]not in acc and r["reason_labels"]==["source_chart_seam"]];need(len(roots)==264,"root census");rows=[]
 for i,r in roots:
  iid=i["split_interface_id"];o=orig[r["origin_row_id"]];normal=seams[r["origin_row_id"]];need(normal["equation"]=="2*t^2-1=0"and normal["face_classification"]=="FULL_BASE_UNIQUE_GRAPH"and normal["exact_dimension"]==2,"normal form:"+iid);box=r179.box_from(r["box"],len(r["refinement_path"]),r["row_id"]);computed,reasons=r179.r174.certify_signature(r["chart"],box,o["owner_target"],reg);need(computed is not None and reasons==[],"signature:"+iid);sid=i["lower_child_row_id"]if i["lower_child_kind"]=="RESOLVED"else i["upper_child_row_id"];signature=kernel_sig(r["chart"],o["owner_target"],computed);need(signature==sig(res[sid]),"sibling:"+iid);cell=r["chart"].split(":")[1];owner_status="E_OR_W_HALF_OPEN_OWNER"if cell in{"E","W"}else"N_OR_S_EXCLUDES_DIAGONAL_TIE";need(normal["half_open_owner_status"]==owner_status,"owner status:"+iid)
  rows.append({"whole_origin_promotion_row_id":"round238-source-seam:"+dg(iid),"Round220_split_interface_id":iid,"origin_row_id":r["origin_row_id"],"Round179_resolved_sibling_row_id":sid,"Round179_retained_child_row_id":r["row_id"],"source_chart":r["chart"],"seam_equation":"2*t^2-1=0","seam_strict_t_gradient_sign":normal["gradient_sign"],"seam_face_classification":"FULL_BASE_UNIQUE_GRAPH","physical_inside_predicate":"2*t^2-1<0","coordinate_guard_predicate":"2*t^2-1>0","half_open_seam_owner_status":owner_status,"seam_dimension":2,"seam_three_dimensional_coordinate_volume":0,"whole_box_signature_recomputation_ignoring_chart_class_precheck":signature,"whole_origin_local_return_signature_credit":1,"coordinate_guard_global_credit":0,"known_block_incidence_credit":0,"global_exact_key_fibre_credit":0})
 rows.sort(key=lambda r:r["whole_origin_promotion_row_id"]);return{"status":"CERTIFIED_264_SOURCE_CHART_SEAM_WHOLE_ORIGIN_RETURN_SIGNATURES","census":{"source_chart_seam_root_count":len(rows),"whole_box_strict_signature_recomputation_count":len(rows),"full_base_unique_graph_count":len(rows),"distinct_exact_key_count":len({r["whole_box_signature_recomputation_ignoring_chart_class_precheck"]["official_key_ordinal"]for r in rows}),"source_chart_histogram":{chart:sum(r["source_chart"]==chart for r in rows)for chart in("G:E","G:W","G:N","G:S")}},"whole_origin_promotion_rows_sha256":dg(rows),"whole_origin_promotion_rows":rows,"strict_nonpromotion":{"known_block_incidence_credit":0,"physical_component_credit":0,"maximal_physical_component_credit":0,"global_exact_key_fibre_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"assemble all 8512 previously unaccepted interfaces into a local classification ledger and attach it to common-refinement strata and known blocks"}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=build();d={"schema":"cm2.round238.source-g-source-chart-seam-whole-origin-promotion.v1","result":r,"result_sha256":dg(r)};b=can(d)+b"\n"
 if not x.no_write:write(b)
 print(r["status"]);print(json.dumps(r["census"],sort_keys=True));print("result_sha256="+d["result_sha256"]);print("certificate_sha256="+hashlib.sha256(b).hexdigest());return 0
if __name__=="__main__":raise SystemExit(main())
