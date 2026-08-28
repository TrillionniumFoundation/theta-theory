#!/usr/bin/env python3
"""Install official F3 prefix collision charts on corrected rank-three faces."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from flint import ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;R103=H/"cm2-round103-rank3-rn-f1-f2-binding-2026-07-22.json";PIN="76ac1099805e5fb3d9eac9984a078ed52f1f6ec706a5a12ec880de28a262c8e8";SCHEMA="cm2.round104.rank3-rn-f3-prefix-chart.v1"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(precision_bits=512):
 ctx.prec=precision_bits
 if sha(R103)!=PIN:raise RuntimeError("pin")
 old=json.loads(R103.read_text())["result"];cores=core_cert.physical_cores();rows=[]
 for b in old["binding_rows"]:
  core=cores[b["source_core_index"]];value="collision:"+core.chart_id;slot="gate5-rank3-slot:"+digest({"word_key":b["word_key"],"homogeneous_subbranch_id":b["homogeneous_subbranch_id"],"roof_level_j":0,"field_name":"homogeneous_prefix_chart"})
  rows.append({"immutable_slot_id":slot,"parent_F2_slot_id":b["F2_slot_id"],"word_key":b["word_key"],"homogeneous_subbranch_id":b["homogeneous_subbranch_id"],"roof_level_j":0,"field_index":3,"field_name":"homogeneous_prefix_chart","field_status":"CERTIFIED_INHERITED_FROM_WHOLE_SOURCE_CORE","field_value":value,"source_core_index":b["source_core_index"],"source_core_chart_id":core.chart_id,"restriction_inherits_chart":True})
 result={"precision_bits":precision_bits,"input_rank3_face_count":len(rows),"new_immutable_F3_slot_count":len(rows),"rank3_face_local_maturity":"3/18","complete_18_field_operator_block_count":0,"first_missing_rank3_field":"F4_homogeneous_suffix_chart","global_Gate5":"NOT_CERTIFIED__10/18_BLOCKS_0","F3_slot_rows":rows,"F3_slot_rows_sha256":digest(rows),"strict_scope":"official homogeneous prefix collision-chart installation on all corrected rank-three faces","strict_nonclaims":["reverse-source parameter chart seams do not alter the collision prefix chart","F4 suffix chart is not inferred from point samples or endpoint labels","no F4-F18 slot or complete block is claimed"],"upstream_pin":{R103.name:PIN}}
 if len(rows)!=12 or len({r["immutable_slot_id"] for r in rows})!=12:raise RuntimeError("accounting")
 result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
