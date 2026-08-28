#!/usr/bin/env python3
"""Weighted transverse disintegration and fail-closed F14 integration audit."""
from __future__ import annotations

import hashlib, json, sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert
import cm2_gate4_inner_core_strong_product_bridge_frontier_cert as strong_cert

HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round87.gate5-f14-transverse-packet-recovery-frontier.v2"
WINDOWS = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
DENSITY = HERE / "cm2-round85-gate5-f14-local-collision-density-input-2026-07-22.json"
TYPED = HERE / "cm2-round85-gate5-f14-typed-standard-pair-frontier-2026-07-22.json"
TYPED_AUDIT = HERE / "cm2-round85-gate5-f14-typed-standard-pair-frontier-audit-2026-07-22.json"
OPERATOR_FRONTIER = HERE / "cm2-round85-gate5-finite-root-operator-field-frontier-2026-07-22.json"
PACKETS = HERE / "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json"
EMPTY_SLOTS = HERE / "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
STRONG_BRIDGE = HERE / "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
PINS = {
 "windows":"81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
 "density":"8a7ff59660cae11d213982b79d8bcb8692649df6ec0edbba39780846d4099a16",
 "typed":"5ade1c0ed5183b316277cd9b519e2291dcf2a4c914cd17c86c7ee1afcf2b6f78",
 "typed_audit":"fa67ffeeb1f5cb3deaf32dec9440ff0c9718f32c74551a4139a4cf7834ced8f8",
 "typed_source":"70608f5b372495f5f5cd84277657f2a9096aea2e611eff3fe69936a3dcc89821",
 "round85_operator_frontier":"f0fd1dc13a7a51b82ca0eb511ce3bd6d44fcd1744b11a0c512b7e5a96f652d19",
 "round25_packet_registry":"f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4",
 "round27_F10_F13_slots":"9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
 "round27_slot_source":"aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43",
 "strong_source_space_bridge":"3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3",
 "strong_source_space_source":"4720669e90824e8c630276aa3d73606435eb88da2a51b2a756f651f56071605a",
 "first_hit_source":"6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
 "core_source":"2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
 "full_core_return_source":"d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}

def canon(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False)
def dig(v:Any)->str:return hashlib.sha256(canon(v).encode()).hexdigest()
def fd(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path)->dict[str,Any]:
 def pairs(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError("duplicate JSON key")
   d[k]=v
  return d
 x=json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
 if not isinstance(x,dict):raise ValueError("top-level object")
 return x
def aq(x):x=Q(x);return arb(x.numerator)/x.denominator

def build(bits:int=512)->dict[str,Any]:
 ctx.prec=bits
 actual={
  "windows":fd(WINDOWS),"density":fd(DENSITY),"typed":fd(TYPED),"typed_audit":fd(TYPED_AUDIT),
  "typed_source":fd(HERE/"cm2_round85_gate5_f14_typed_standard_pair_frontier_cert.py"),
  "round85_operator_frontier":fd(OPERATOR_FRONTIER),"round25_packet_registry":fd(PACKETS),
  "round27_F10_F13_slots":fd(EMPTY_SLOTS),
  "round27_slot_source":fd(HERE/"cm2_gate5_round27_r1_empty_physical_face_join_cert.py"),
  "strong_source_space_bridge":fd(STRONG_BRIDGE),
  "strong_source_space_source":fd(HERE/"cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py"),
  "first_hit_source":fd(HERE/"cm2_gate3_candidate_first_hit_cert.py"),
  "core_source":fd(HERE/"cm2_gate25_physical_return_core_registry_cert.py"),
  "full_core_return_source":fd(HERE/"cm2_gate34_full_core_return_adaptive_frontier_cert.py")}
 if actual!=PINS:raise ValueError("upstream pins")
 windows=load(WINDOWS)["result"]["evidence"]["window_rows"]
 typed=load(TYPED)["result"]; audit=load(TYPED_AUDIT)["result"]
 density=load(DENSITY)["result"]
 frontier=load(OPERATOR_FRONTIER)["result"]
 packets=load(PACKETS)["result"]["R1_inner_candidate_field_packet_rows"]
 empty=load(EMPTY_SLOTS)["result"]
 strong=strong_cert.core_local_strong_multiplier()
 if len(windows)!=152 or typed["finite_root_typed_F14_central_subfamily_input"]!="CERTIFIED_152_OF_152":raise ValueError("typed")
 if audit["verdict"]!="PASS" or density["F14_numerical_formula_input_rows"]!="152/152":raise ValueError("density audit")
 if frontier["candidate_local_maturity_after"]!="13/18" or frontier["new_F14_through_F18_fields_installed"]!=0:raise ValueError("frontier")
 if empty["F14_F18_frontier"]["F14_through_F18_materialized_slot_count"]!=0:raise ValueError("F14 registry")
 source_norm=strong["source_norm"]
 if source_norm!="M*(1+Reg_alpha(rho)+1/length)":raise ValueError("strong norm")
 packet_map={r["atom_id"]:r for r in packets}
 attach={r["atom_id"]:r for r in frontier["evidence"]["attachment_rows"]}
 cores={return_cert.core_id(c):c for c in core_cert.physical_cores()}
 rows=[]
 for w in sorted(windows,key=lambda z:z["positive_atom_id"]):
  aid=w["positive_atom_id"]; p=packet_map[aid]; a=attach[aid]
  if p["r1_candidate_field_packet_id"]!=a["candidate_packet_id"] or p["physical_homogeneity_subbranch_id"]!=a["physical_homogeneity_subbranch_id"]:raise ValueError("packet crosswalk")
  if p["roof"]!=1 or p["roof_level_j"]!=0 or a["F10_coarea_density_regular_cost"]!="0":raise ValueError("slots")
  c=cores[w["source_core_id"]];R=aq(first_hit.RADIUS[c.source]);t0,t1=map(aq,w["common_t"]);p0,p1=map(aq,w["common_p"])
  r0,r1=R*t0.asin(),R*t1.asin();phi0,phi1=p0.asin(),p1.asin();dr=r1-r0
  width=phi1-phi0+4*dr;M=dr*(p1-p0);pmax=max(abs(p0),abs(p1))
  bv_num=width*(1+4*pmax*dr)/arb(17).sqrt(); bv_cost=bv_num/M
  length_term=width/(arb(17).sqrt()*M)
  if not (M>aq(Q(1,12000000)) and M<aq(Q(1,5000000)) and width>aq(Q(3,2000)) and width<aq(Q(19,10000))):raise ValueError("geometry")
  if not (phi0.cos()>aq(Q(999,1000)) and phi1.cos()>aq(Q(999,1000)) and bv_cost<4300 and length_term<4300):raise ValueError("weighted bounds")
  rows.append({
   "atom_id":aid,"candidate_packet_id":a["candidate_packet_id"],
   "physical_homogeneity_subbranch_id":a["physical_homogeneity_subbranch_id"],"roof_level_j":p["roof_level_j"],
   "F10_slot_id":a["F10_slot_id"],"F10_slot_value":"0_EMPTY_PHYSICAL_OCCURRENCE_FACE_FAMILY",
   "immutable_F14_slot_id":"NOT_MATERIALIZED","F14_slot_status":"NOT_CERTIFIED",
   "coordinates":"r=R*asin(t),phi=asin(p),v=phi-4r",
   "fibre":"I_v=[max(r0,(phi0-v)/4),min(r1,(phi1-v)/4)]",
   "mass":"m(v)=integral_Iv cos(4r+v)dr","packet_mass":"M=(r1-r0)*(p1-p0)",
   "normalized_transverse_probability":"dLambda=m(v)dv/M",
   "conditional_probability":"rho_v=cos(phi)/(sqrt(17)*m(v)) with respect to internal arclength ds",
   "weighted_BV_space":"L1(Lambda;BV_internal(W_v))",
   "weighted_BV_synthesis":"S(c)_v=c*rho_v","weighted_BV_synthesis_cost_strict_upper":"4300",
   "accepted_strong_source_norm":source_norm,"accepted_length_over_Z_term_strict_upper":"4300",
   "accepted_Reg_alpha_term":"NOT_CROSSWALKED_FROM_INTERNAL_FIBRE_BV_OR_COORDINATE_LOG_LIPSCHITZ",
  })
 evidence={
  "precision_bits":bits,"row_count":len(rows),"exact_measure_identity":"cos(phi)drdphi=rho_v ds dLambda*M",
  "normalization":{"Lambda":"dLambda=m(v)dv/M","Lambda_total":"1","recipient":"X_BV=direct_sum_(152)L1(Lambda_i;BV_internal(W_i,v))","internal_fibre_BV":"no zero-extension endpoint jumps","synthesis":"S(c)_v=c*rho_v","norm_bound":"||S||<4300"},
  "fibre_checks":{"cos_phi_strict_lower":"999/1000","positive_mass_on_every_interior_label":True,"zero_mass_endpoint_count":304,"identity":"m(v)*||rho_v||_BV_internal=||h_v||_BV_internal"},
  "integration":{"round25_packet_crosswalk_rows":152,"round27_F10_slot_crosswalk_rows":152,"round27_registered_F14_slot_count":0,"emitted_not_materialized_F14_markers":152,"accepted_source_space":source_norm,"accepted_length_over_Z_term":"FINITE_<4300","accepted_Reg_alpha_crosswalk":"NOT_CERTIFIED","recovered_strong_interface":"NOT_CERTIFIED"},
  "integration_rows":rows}
 result={
  "status":"CERTIFIED_WEIGHTED_BV_DISINTEGRATION_AND_EXACT_F14_INTEGRATION_FRONTIER",
  "weighted_BV_disintegration_on_152_packets":"CERTIFIED",
  "short_fibre_mass_weighted_recovery":"CERTIFIED_IN_INTERNAL_FIBRE_BV",
  "F14_regular_density_operator_cost":"NOT_CERTIFIED__NO_REGISTERED_IMMUTABLE_F14_SLOT_AND_NO_ACCEPTED_REG_ALPHA_RECOVERY_CROSSWALK",
  "candidate_local_maturity_before":"13/18","candidate_local_maturity_after":"13/18",
  "new_F14_slots_installed":0,"complete_18_field_blocks":0,"global_Gate5":"NOT_CERTIFIED__10/18_BLOCKS_0",
  "sharp_remaining_condition":"construct an immutable same-key F14 slot whose recipient is the frozen M*(1+Reg_alpha+1/L) completion and prove the Reg_alpha/recovery intertwiner; internal-fibre BV alone is insufficient",
  "strict_nonclaims":["weighted BV is not relabelled as the accepted recovered strong space","the empty F10 physical-face value 0 does not pay the nonempty packet Reg_alpha term","no F14 maturity promotion","no F15-F18 or global promotion"],
  "evidence":evidence,"evidence_sha256":dig(evidence)}
 return {"schema":SCHEMA,"pins":actual,"result":result,"result_sha256":dig(result)}

if __name__=="__main__":
 try:print(canon(build()))
 except Exception as e:print(canon({"schema":SCHEMA,"status":"FAIL_CLOSED","error":str(e)}));sys.exit(2)
