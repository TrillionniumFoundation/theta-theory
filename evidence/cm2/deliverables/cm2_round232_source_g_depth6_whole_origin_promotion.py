#!/usr/bin/env python3
"""Promote fully resolved Round231 seam roots to whole-origin local signatures."""
from __future__ import annotations
import argparse, hashlib, json, os, stat, tempfile
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
SCHEMA="cm2.round232.source-g-depth6-whole-origin-promotion.v1"
OUTPUT=HERE/"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json"
PINS={
"cm2_round179_source_g_residual_tube_arrangement_rows.json":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974",
"cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json":"7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374"}
def need(x:bool,s:str)->None:
    if not x: raise RuntimeError(s)
def enc(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def dig(x:Any)->str:return hashlib.sha256(enc(x)).hexdigest()
def load(n:str)->dict[str,Any]:
    p=HERE/n;i=p.lstat();need(stat.S_ISREG(i.st_mode) and not p.is_symlink() and i.st_nlink==1,"regular:"+n)
    b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[n],"pin:"+n);d=json.loads(b)
    need(dig(d["result"])==d["result_sha256"],"digest:"+n);return d["result"]
def rows(d:dict[str,Any],n:str)->list[dict[str,Any]]:
    c=d["row_column_schemas"][n];return[dict(zip(c,r,strict=True))for r in d[n]]
def vol(b:list[str])->Q:
    q=list(map(Q,b));return(q[1]-q[0])*(q[3]-q[2])*(q[5]-q[4])
def sig(r:dict[str,Any])->dict[str,Any]:return{"source_chart":r["chart"],"target_lift":r["owner_target"],"ordered_integer_wall_events":r["ordered_integer_wall_events"],"signed_wall_word":r["signed_wall_word"],"roof":r["roof"],"outgoing_cell":r["outgoing_cell"],"target_chart":r["target_chart"],"official_key_row":r["official_key_row"],"official_key_ordinal":r["official_key_ordinal"],"official_key_id":r["official_key_id"]}
def safe(b:bytes)->None:
    f,n=tempfile.mkstemp(prefix=".round232.",suffix=".tmp",dir=HERE);p=Path(n)
    try:
        with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
        os.replace(p,OUTPUT)
    finally:
        if p.exists():p.unlink()
def build()->dict[str,Any]:
    a=load("cm2_round179_source_g_residual_tube_arrangement_rows.json");b=load("cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json");c=load("cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json")
    origins={r["origin_row_id"]:r for r in rows(a,"origin_tube_rows")};resolved={r["row_id"]:r for r in rows(a,"resolved_3d_child_rows")};retained={r["row_id"]:r for r in rows(a,"retained_3d_child_rows")}
    full={r["Round220_split_interface_id"]:r for r in c["root_summary_rows"]if r["depth6_retained_frontier_count"]==0};need(len(full)==2220,"full roots")
    descendants=defaultdict(list)
    for r in c["resolved_descendant_rows"]:
        if r["Round220_split_interface_id"]in full:descendants[r["Round220_split_interface_id"]].append(r)
    t=b["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"];interfaces={}
    for packed in t["rows"]:
        r=dict(zip(t["columns"],packed,strict=True));iid=r["split_interface_id"]
        if iid not in full:continue
        rid=r["lower_child_row_id"]if r["lower_child_kind"]=="RESOLVED"else r["upper_child_row_id"]
        tid=r["upper_child_row_id"]if r["upper_child_kind"]=="RETAINED"else r["lower_child_row_id"]
        interfaces[iid]=(rid,tid)
    need(len(interfaces)==2220,"interfaces")
    out=[]
    for iid in sorted(full):
        rid,tid=interfaces[iid];old=resolved[rid];root=retained[tid];origin=origins[root["origin_row_id"]];children=descendants[iid];s=sig(old)
        need(origin["resolved_child_count"]==1 and origin["retained_child_count"]==1 and origin["guard_child_count"]==0 and origin["original_reason_labels"]==["outgoing_chart_seam"],"origin partition")
        need(children and all(x["local_return_signature"]==s for x in children),"one signature")
        need(sum((Q(x["coordinate_volume"])for x in children),Q(0))==Q(root["coordinate_volume"]),"retained cover")
        need(Q(old["coordinate_volume"])+Q(root["coordinate_volume"])==Q(origin["original_coordinate_volume"]),"origin volume")
        out.append({"whole_origin_promotion_row_id":"round232-whole-origin:"+dig([iid,origin["origin_row_id"],s]),"Round220_split_interface_id":iid,"origin_row_id":origin["origin_row_id"],"parent_id":origin["parent_id"],"chart":origin["chart"],"original_box":origin["original_box"],"original_coordinate_volume":origin["original_coordinate_volume"],"Round179_resolved_child_row_id":rid,"Round179_retained_child_row_id":tid,"Round231_resolved_descendant_count":len(children),"Round231_resolved_descendant_ids_sha256":dig(sorted(x["materialized_row_id"]for x in children)),"local_return_signature":s,"whole_origin_local_return_signature_credit":1,"whole_origin_positive_3D_occurrence_credit":1,"known_block_incidence_credit":0,"known_block_membership_credit":0,"physical_component_credit":0,"maximal_physical_component_credit":0,"global_exact_key_disposition_credit":0})
    need(len(out)==2220 and len({x["origin_row_id"]for x in out})==2220,"promotion census")
    return{"status":"CERTIFIED_2220_WHOLE_ORIGIN_LOCAL_RETURN_SIGNATURES_ZERO_GLOBAL_PROMOTION","census":{"promoted_whole_origin_count":2220,"promoted_round231_descendant_count":sum(x["Round231_resolved_descendant_count"]for x in out),"distinct_exact_key_count":len({x["local_return_signature"]["official_key_ordinal"]for x in out}),"known_block_incidence_count":0,"global_exact_key_disposition_count":0},"whole_origin_promotion_rows_sha256":dig(out),"whole_origin_promotion_rows":out,"scope_contract":{"finite_depth6_partition_covers_every_promoted_origin":True,"one_exact_return_signature_on_every_promoted_origin":True,"local_whole_origin_credit_is_not_global_fibre_credit":True,"known_block_or_component_assignment_proved":False},"strict_nonpromotion":{"known_block_incidence_credit":0,"physical_component_credit":0,"maximal_physical_component_credit":0,"global_exact_key_disposition_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"attach promoted whole origins only through certified event/common-refinement contact; use interval root isolation for the remaining 3148 seam roots"}
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=build();d={"schema":SCHEMA,"result":r,"result_sha256":dig(r)};b=enc(d)+b"\n"
    if not x.no_write:safe(b)
    print(r["status"]);print(json.dumps(r["census"],sort_keys=True));print("result_sha256="+d["result_sha256"]);print("certificate_sha256="+hashlib.sha256(b).hexdigest());return 0
if __name__=="__main__":raise SystemExit(main())
