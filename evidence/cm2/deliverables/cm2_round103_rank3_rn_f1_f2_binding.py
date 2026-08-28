#!/usr/bin/env python3
"""Bind corrected rank-three faces to official Gate5/RN F1-F2 slots."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from flint import ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent
QUOTIENT=HERE/"cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
SCHEMA_FILE=HERE/"cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
PINS={QUOTIENT.name:"85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",SCHEMA_FILE.name:"47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"}
SCHEMA="cm2.round103.rank3-rn-f1-f2-binding.v1";PRECISION_BITS=512
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def slot_id(word,subbranch,field):return "gate5-rank3-slot:"+digest({"word_key":word,"homogeneous_subbranch_id":subbranch,"roof_level_j":0,"field_name":field})
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin:{n}")
 quotient=json.loads(QUOTIENT.read_text())["result"];schema=json.loads(SCHEMA_FILE.read_text())["result"]["required_operator_field_schema"];fields=schema["required_fields"]
 if len(fields)!=18 or fields[:2]!=["nonempty_or_empty_domain_proof","physical_homogeneity_subbranch_table"]:raise RuntimeError("field schema")
 cores=core_cert.physical_cores();rows=[];slots=[]
 for face in quotient["face_rows"]:
  source=cores[face["source_core_index"]];owners=[source.target_id,face["second_selected_target_id"],face["third_candidate_id"]]
  word="physical-s0-rank3-return-word:"+digest({"ordered_collision_owner_ids":owners,"rank":3})
  binding={"word_key":word,"ordered_collision_owner_ids":owners,"homogeneous_subbranch_id":face["face_id"],"roof_level_j":0,"face_id":face["face_id"],"source_core_index":face["source_core_index"],"signed_transverse_tangency_factor_sign":face["signed_transverse_tangency_factor_sign"],"ordered_registered_port_count":face["ordered_registered_port_count"],"interior_link_count":face["interior_link_count"],"endpoint_type_pair":face["endpoint_type_pair"],"F1_slot_id":slot_id(word,face["face_id"],fields[0]),"F2_slot_id":slot_id(word,face["face_id"],fields[1]),"installed_field_count":2,"required_field_count":18,"first_missing_field":fields[2],"complete_18_field_block":False};rows.append(binding)
  slots.extend([{"immutable_slot_id":binding["F1_slot_id"],"word_key":word,"homogeneous_subbranch_id":face["face_id"],"roof_level_j":0,"field_index":1,"field_name":fields[0],"field_status":"CERTIFIED_NONEMPTY_PHYSICAL_FACE","field_value":{"face_id":face["face_id"],"ordered_registered_port_count":face["ordered_registered_port_count"],"endpoint_complete":face["endpoint_complete"]}},{"immutable_slot_id":binding["F2_slot_id"],"word_key":word,"homogeneous_subbranch_id":face["face_id"],"roof_level_j":0,"field_index":2,"field_name":fields[1],"field_status":"CERTIFIED_COMPLETE_PHYSICAL_HOMOGENEITY_SUBBRANCH_ROW","field_value":{"face_id":face["face_id"],"source_core_index":face["source_core_index"],"second_selected_target_id":face["second_selected_target_id"],"third_candidate_id":face["third_candidate_id"],"signed_transverse_tangency_factor_sign":face["signed_transverse_tangency_factor_sign"],"ordered_registered_port_ids_sha256":face["ordered_registered_port_ids_sha256"],"endpoint_ids":face["endpoint_ids"]}}])
 result={"precision_bits":precision_bits,"bound_rank3_return_word_count":len(rows),"bound_physical_homogeneous_subbranch_count":len(rows),"new_immutable_F1_slot_count":sum(s["field_index"]==1 for s in slots),"new_immutable_F2_slot_count":sum(s["field_index"]==2 for s in slots),"new_immutable_slot_count":len(slots),"rank3_face_local_maturity":"2/18","complete_18_field_operator_block_count":0,"first_missing_rank3_field":"F3_homogeneous_prefix_chart","global_Gate5":"NOT_CERTIFIED__10/18_BLOCKS_0","binding_rows":rows,"binding_rows_sha256":digest(rows),"immutable_slot_rows":slots,"immutable_slot_rows_sha256":digest(slots),"required_field_schema_sha256":schema["required_field_schema_sha256"],"strict_scope":"official immutable F1-F2 Gate5/RN binding of all twelve corrected rank-three physical faces","strict_nonclaims":["F3 and F4 are not inferred from endpoint chart labels because eight faces cross a source chart seam","F5 through F18 require analytic operator bounds not supplied by the face quotient","no complete operator block or global Gate5 credit is claimed"],"upstream_pins":PINS}
 if (len(rows),len(slots),len({s["immutable_slot_id"] for s in slots}))!=(12,24,24):raise RuntimeError("slot accounting")
 result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--precision-bits",type=int,default=PRECISION_BITS);a=p.parse_args();print(json.dumps(build(a.precision_bits),sort_keys=True,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
