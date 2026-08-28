#!/usr/bin/env python3
"""Install whole-face F4 suffix collision charts for corrected rank three."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,ctx
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round89_rank3_projective_gap_closure_cert as r89
import cm2_round91_rank3_exterior_source_exit_cert as r91
import cm2_round92_rank3_competitor_event_isolation_cert as r92
from cm2_round79_tangency_intersection_generator import aq,digest,strict_sign
H=Path(__file__).resolve().parent
R87=H/"cm2-round87-rank3-port-event-continuation-2026-07-22.json";R99=H/"cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json";R100=H/"cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json";R101=H/"cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json";R102=H/"cm2-round102-rank3-corrected-face-quotient-2026-07-22.json";R104=H/"cm2-round104-rank3-rn-f3-prefix-chart-2026-07-22.json"
PINS={R87.name:"f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",R99.name:"e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",R100.name:"097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",R101.name:"df29ea8467c09351276a40b38424d6c9effc763f287815e7bac67829bca58172",R102.name:"85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",R104.name:"d6d47ac6b7cb03f70d483536a31ca031718f9aa96bd8adfce072866870bb9c5d"}
SCHEMA="cm2.round105.rank3-rn-f4-suffix-chart.v1"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(precision_bits=512):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(H/n)!=h:raise RuntimeError(f"pin:{n}")
 old=json.loads(R87.read_text())["result"]["port_event_rows"];byid={x["registered_port_id"]:x for x in old};pids=json.loads(R99.read_text())["result"]["corrected_locally_physical_registered_port_ids"];physical={p:byid[p] for p in pids};f100=json.loads(R100.read_text())["result"];f101=json.loads(R101.read_text())["result"];faces=json.loads(R102.read_text())["result"]["face_rows"];f3=json.loads(R104.read_text())["result"]["F3_slot_rows"];f3map={x["homogeneous_subbranch_id"]:x for x in f3};source={(tuple(x["branch_key"]),x["projective_end"]):x for x in f100["source_cap_rows"]};graz={(tuple(x["branch_key"]),x["projective_end"]):x for x in f101["ray_rows"]};cores=core_cert.physical_cores();rows=[]
 for face in faces:
  branch=(face["source_core_index"],face["second_selected_target_id"],face["third_candidate_id"],face["signed_transverse_tangency_factor_sign"]);ends=[]
  for side in ("LEFT_PROJECTIVE_END","RIGHT_PROJECTIVE_END"):
   key=(branch,side)
   if key in source:
    port=source[key]["mated_physical_port_id"];q0,d,x=r92.ray_geometry(branch,side,port,physical,cores);mid=aq(q0+d*x);q=mid+arb(0,aq(Q(1,10**20)).upper());kind="REGISTERED_SOURCE_CAP_CORE_EXIT_ROOT"
   else:
    rr=graz[key];port=rr["exterior_port_id"];q0=r89.qball(byid[port]);d=-1 if side.startswith("LEFT") else 1;a,b=map(Q,rr["terminal_event_parameter_bracket"]);q=q0+d*r91.qball(a,b);kind="SOURCE_GRAZING_ROOT_BRACKET"
   lo,hi=r91.arb_bounds(q);ends.append((lo,hi,side,kind))
  lo=min(x[0] for x in ends);hi=max(x[1] for x in ends);q=r91.qball(lo,hi);den=arb(1)+q*q;ux=(arb(1)-q*q)/den;uy=2*q/den;sx,sy=strict_sign(ux),strict_sign(uy)
  if sx==0 or sy==0:raise RuntimeError(f"suffix chart seam:{branch}")
  value=f"collision:{branch[2]}:open-semicircle:[{sx},{sy}]";parent=f3map[face["face_id"]];slot="gate5-rank3-slot:"+digest({"word_key":parent["word_key"],"homogeneous_subbranch_id":face["face_id"],"roof_level_j":0,"field_name":"homogeneous_suffix_chart"})
  rows.append({"immutable_slot_id":slot,"parent_F3_slot_id":parent["immutable_slot_id"],"word_key":parent["word_key"],"homogeneous_subbranch_id":face["face_id"],"roof_level_j":0,"field_index":4,"field_name":"homogeneous_suffix_chart","field_status":"CERTIFIED_WHOLE_FACE_PROJECTIVE_DIRECTION_ENCLOSURE","field_value":value,"third_collision_target_id":branch[2],"whole_face_q_enclosure":[str(lo),str(hi)],"outgoing_direction_component_strict_signs":[sx,sy],"endpoint_q_evidence":[{"projective_end":x[2],"endpoint_q_interval":[str(x[0]),str(x[1])],"method":x[3]} for x in ends]})
 result={"precision_bits":precision_bits,"input_rank3_face_count":len(rows),"new_immutable_F4_slot_count":len(rows),"suffix_chart_histogram":dict(sorted(__import__('collections').Counter(x["field_value"] for x in rows).items())),"rank3_face_local_maturity":"4/18","complete_18_field_operator_block_count":0,"first_missing_rank3_field":"F5_inverse_Jacobian_bound","global_Gate5":"NOT_CERTIFIED__10/18_BLOCKS_0","F4_slot_rows":rows,"F4_slot_rows_sha256":digest(rows),"strict_scope":"whole-face projective outgoing-direction enclosure in one accepted target open-semicircle collision chart","strict_nonclaims":["F5 inverse Jacobian is not inferred from chart existence","no F5-F18 slot or complete block is claimed"],"upstream_pins":PINS}
 if len(rows)!=12 or len({x["immutable_slot_id"] for x in rows})!=12:raise RuntimeError("accounting")
 result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
