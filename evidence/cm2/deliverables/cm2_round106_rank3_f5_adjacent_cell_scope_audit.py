#!/usr/bin/env python3
"""Audit the F5 scope mismatch between tangent faces and smooth operator cells."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;R102=H/"cm2-round102-rank3-corrected-face-quotient-2026-07-22.json";R105=H/"cm2-round105-rank3-rn-f4-suffix-chart-2026-07-22.json";U=H/"cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
P={R102.name:"85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",R105.name:"ef747bcd760bf8fe0a8bd8ac3bc65f9df4cf381898ffe98afcdb823f19c44b28",U.name:"d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"};SCHEMA="cm2.round106.rank3-f5-adjacent-cell-scope-audit.v1"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 for n,h in P.items():
  if sha(H/n)!=h:raise RuntimeError(f"pin:{n}")
 faces=json.loads(R102.read_text())["result"]["face_rows"];f4=json.loads(R105.read_text())["result"]["F4_slot_rows"];fm={x["homogeneous_subbranch_id"]:x for x in f4};u=json.loads(U.read_text())["result"]["universal_full_collision_branch_templates"]
 rows=[]
 for face in faces:
  rows.append({"face_id":face["face_id"],"third_candidate_id":face["third_candidate_id"],"endpoint_type_pair":face["endpoint_type_pair"],"F4_suffix_chart":fm[face["face_id"]]["field_value"],"geometric_object_type":"CODIMENSION_ONE_THIRD_TANGENCY_FACE","required_F5_template_scope":u["scope"],"materialized_adjacent_smooth_operator_child_count":0,"required_two_sided_adjacent_smooth_operator_child_count":2,"universal_F5_restriction_inheritance_legal":False,"universal_F6_restriction_inheritance_legal":False,"first_missing_evidence":"two side-labelled positive-dimensional rank3 smooth collision cells carrying the same return-word key"})
 result={"audited_rank3_face_count":len(rows),"required_adjacent_side_germ_count":2*len(rows),"materialized_adjacent_side_germ_count":0,"faces_with_source_grazing_endpoint_count":sum("SOURCE_GRAZING" in x["endpoint_type_pair"] for x in faces),"new_immutable_F5_slot_count":0,"new_immutable_F6_slot_count":0,"rank3_face_local_maturity":"4/18","complete_18_field_operator_block_count":0,"first_missing_rank3_field":"F5_inverse_Jacobian_bound","F5_installation_status":"BLOCKED_BY_MISSING_TWO_SIDED_SMOOTH_OPERATOR_CELL_ATLAS","global_Gate5":"NOT_CERTIFIED__10/18_BLOCKS_0","audit_rows":rows,"audit_rows_sha256":digest(rows),"strict_conclusion":"the universal F5/F6 templates quantify smooth positive-dimensional solid-collision children; a codimension-one tangency face is not such a child and cannot inherit those bounds without side-labelled adjacent cells","strict_nonclaims":["the eight grazing-ended faces are not assigned a finite uniform inverse-Jacobian bound","the four cap-to-cap faces are not promoted either because their adjacent operator cells are also absent","Round103-Round105 face-local F1-F4 metadata do not constitute complete operator blocks"],"upstream_pins":P}
 if len(rows)!=12 or result["required_adjacent_side_germ_count"]!=24:raise RuntimeError("accounting")
 return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
