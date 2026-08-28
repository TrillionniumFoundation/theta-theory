#!/usr/bin/env python3
"""Fail-closed verifier for selected-component reachability pruning."""
from __future__ import annotations
import argparse,copy,hashlib,json,sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
import cm2_gate25_selected_component_reachability_pruning_cert as certificate

HERE=Path(__file__).resolve().parent
SCHEMA="cm2.gate25.selected-component-reachability-pruning.manifest.v1"
RESULT_SCHEMA="cm2.gate25.selected-component-reachability-pruning.v1"
DEFAULT_MANIFEST=HERE/"cm2-gate25-selected-component-reachability-pruning-manifest-2026-07-17.json"
CERTIFICATE=HERE/"cm2_gate25_selected_component_reachability_pruning_cert.py"
def cj(x:Any)->str:return json.dumps(x,sort_keys=True,separators=(",",":"))
def dg(x:Any)->str:return hashlib.sha256(cj(x).encode()).hexdigest()
def sh(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(r:dict[str,Any])->str:
 x=copy.deepcopy(r);x.pop("internal_replay_digest",None);return dg(x)
def check(d:Any)->list[str]:
 e=[]
 if not isinstance(d,dict):return["manifest type"]
 if d.get("schema")!=SCHEMA:e.append("schema")
 if d.get("certificate_sha256")!=sh(CERTIFICATE):e.append("cert hash")
 if d.get("verifier_sha256")!=sh(Path(__file__)):e.append("verifier hash")
 if d.get("dependencies")!=certificate.DEPENDENCIES:e.append("dependencies")
 else:
  for n,h in certificate.DEPENDENCIES.items():
   if not (HERE/n).is_file() or sh(HERE/n)!=h:e.append("dependency "+n)
 r=d.get("result",{})
 if r.get("schema")!=RESULT_SCHEMA:e.append("result schema")
 if r.get("internal_replay_digest")!=rd(r):e.append("digest")
 if r.get("provenance",{}).get("selected_component_id")!=certificate.SELECTED_COMPONENT_ID:e.append("component id")
 q=r.get("target_central_quadrant_forcing",{})
 for k,v in {"target_transverse_threshold":"6/125","t_nonpositive_transverse_strict_lower":"179/800","zero_to_half_t_transverse_strict_lower":"833/16000","least_exclusion_margin":"13/3200","target_central_implies_t_strictly_greater_than_one_half":True,"outgoing_velocity_both_coordinates_positive":True}.items():
  if q.get(k)!=v:e.append("quadrant "+k)
 a=r.get("automatic_word_owner_wall_and_target_chart",{})
 for k,v in {"segment_coordinatewise_increasing_inside_open_unit_square":True,"no_transparent_integer_wall_crossing":True,"selected_W00_is_strict_first_solid_collision":True,"target_chart_dot_strict_lower":"13/20","target_open_semicircle_automatic":True,"all_remaining_gray_lifts_excluded_by_one_coordinate_distance_gt_9_over_25":True,"all_other_white_lifts_excluded_by_one_coordinate_distance_gt_4_over_25":True,"other_physical_word_and_chart_predicates_are_implied_on_P":True,"raw_algebraic_predicates_are_not_claimed_nonvanishing":True}.items():
  if a.get(k)!=v:e.append("automatic "+k)
 if a.get("other_nearby_gray_disk_squared_distance_margins")!={"G[1,0]":"2673/160000","G[0,1]":"1547/31250","G[1,1]":"3197/32000"}:e.append("disk margins")
 c=r.get("connected_pruned_domain_theorem",{})
 for k,v in {"A_strict_lower":"953/4000","abs_B_strict_upper":"161/800","partial_p_T_strict_upper":"-13277/76000","partial_t_T_strict_upper":"-11/64","T_on_p_equals_minus_3_over_10_strict_lower":"2759/40000","T_on_t_equals_one_half_strict_lower":"833/16000","T_upper_t_limit_at_p_equals_3_over_10_strict_upper":"-2759/40000","target_transverse_level":"6/125","V_t_equals_T_t_3_over_10_is_continuous_strictly_decreasing":True,"V_crosses_plus_then_minus_target_level_uniquely":True,"nonempty_t_projection_is_one_open_interval":True,"every_nonempty_fixed_t_fibre_is_one_open_p_interval":True,"fibre_endpoints_are_continuous_by_uniform_implicit_function_theorem":True,"continuous_midpoint_section_proves_P_path_connected":True,"frozen_full_window_seed_corridor_is_contained_in_P":True,"P_equals_seeded_maximal_connected_component_M":True}.items():
  if c.get(k)!=v:e.append("connected "+k)
 try:
  if not (Q(c["partial_p_T_strict_upper"])<0 and Q(c["partial_t_T_strict_upper"])<0):e.append("connected derivative signs")
  if not (Q(c["T_on_p_equals_minus_3_over_10_strict_lower"])>Q(c["target_transverse_level"])):e.append("connected left side")
  if not (Q(c["T_upper_t_limit_at_p_equals_3_over_10_strict_upper"])<-Q(c["target_transverse_level"])):e.append("connected upper corner")
 except:e.append("connected fractions")
 i=r.get("selected_component_interval_characteristic_theorem",{})
 for k,v in {"other_physical_word_and_chart_predicates_implied_on_P":True,"raw_algebraic_equalities_may_still_vanish_outside_their_physical_roles":True,"P_equals_seeded_maximal_connected_component_M":True,"target_central_preimage_on_unstable_graph_is_interval":True,"selected_component_intersection_component_upper_per_canonical_curve":1,"selected_component_local_unnormalized_characteristic_Z_multiplier":"2000/1999","restriction_then_physical_step_coefficient":"720269600000/720626832337","restriction_then_physical_step_margin":"357232337/720626832337","selected_component_local_characteristic_Growth_contraction":True}.items():
  if i.get(k)!=v:e.append("interval "+k)
 if i.get("frozen_positive_entry_Birkhoff_matrix")!="D T=-c_1^-1[[tau*kappa_0+c_0,tau],[tau*kappa_0*kappa_1+kappa_0*c_1+kappa_1*c_0,tau*kappa_1+c_1]]":e.append("interval Birkhoff matrix")
 try:
  if Q(i["restriction_then_physical_step_coefficient"])>=1:e.append("no contraction")
 except:e.append("coefficient")
 n=r.get("strict_nonpromotion",{})
 for k,v in {"selected_component_local_field7_seed":"CERTIFIED","full_key_all_component_field7":"NOT_CERTIFIED","other_23_seeded_components_receive_this_sharp_pruning":False,"complete_18_field_operator_block_count":0,"stable_saturated_product_base":False,"PPE":False,"Gate2":"NOT_CERTIFIED","Gate5":"NOT_CERTIFIED"}.items():
  if n.get(k)!=v:e.append("scope "+k)
 if d.get("verdict")!={"selected_component_local_contracting_characteristic_Z":"CERTIFIED","full_key_field7":"NOT_CERTIFIED","Gate2":"NOT_CERTIFIED","Gate5":"NOT_CERTIFIED"}:e.append("verdict")
 return e
def refresh(d):d["result"]["internal_replay_digest"]=rd(d["result"])
def selftest(d):
 ms=[]
 def m(path,val):
  x=copy.deepcopy(d);y=x
  for p in path[:-1]:y=y[p]
  y[path[-1]]=val
  if path[0]=="result":refresh(x)
  ms.append(x)
 m(("result","target_central_quadrant_forcing","least_exclusion_margin"),"0")
 m(("result","target_central_quadrant_forcing","target_central_implies_t_strictly_greater_than_one_half"),False)
 m(("result","target_central_quadrant_forcing","outgoing_velocity_both_coordinates_positive"),False)
 m(("result","automatic_word_owner_wall_and_target_chart","no_transparent_integer_wall_crossing"),False)
 m(("result","automatic_word_owner_wall_and_target_chart","selected_W00_is_strict_first_solid_collision"),False)
 m(("result","automatic_word_owner_wall_and_target_chart","target_chart_dot_strict_lower"),"0")
 m(("result","automatic_word_owner_wall_and_target_chart","other_nearby_gray_disk_squared_distance_margins","G[1,0]"),"0")
 m(("result","automatic_word_owner_wall_and_target_chart","other_physical_word_and_chart_predicates_are_implied_on_P"),False)
 m(("result","connected_pruned_domain_theorem","partial_p_T_strict_upper"),"0")
 m(("result","connected_pruned_domain_theorem","partial_t_T_strict_upper"),"0")
 m(("result","connected_pruned_domain_theorem","T_on_p_equals_minus_3_over_10_strict_lower"),"0")
 m(("result","connected_pruned_domain_theorem","T_upper_t_limit_at_p_equals_3_over_10_strict_upper"),"0")
 m(("result","connected_pruned_domain_theorem","nonempty_t_projection_is_one_open_interval"),False)
 m(("result","connected_pruned_domain_theorem","every_nonempty_fixed_t_fibre_is_one_open_p_interval"),False)
 m(("result","connected_pruned_domain_theorem","continuous_midpoint_section_proves_P_path_connected"),False)
 m(("result","connected_pruned_domain_theorem","P_equals_seeded_maximal_connected_component_M"),False)
 m(("result","selected_component_interval_characteristic_theorem","other_physical_word_and_chart_predicates_implied_on_P"),False)
 m(("result","selected_component_interval_characteristic_theorem","P_equals_seeded_maximal_connected_component_M"),False)
 m(("result","selected_component_interval_characteristic_theorem","frozen_positive_entry_Birkhoff_matrix"),"unbound")
 m(("result","selected_component_interval_characteristic_theorem","target_central_preimage_on_unstable_graph_is_interval"),False)
 m(("result","selected_component_interval_characteristic_theorem","selected_component_intersection_component_upper_per_canonical_curve"),2)
 m(("result","selected_component_interval_characteristic_theorem","restriction_then_physical_step_coefficient"),"1")
 m(("result","selected_component_interval_characteristic_theorem","selected_component_local_characteristic_Growth_contraction"),False)
 m(("result","strict_nonpromotion","full_key_all_component_field7"),"CERTIFIED")
 m(("result","strict_nonpromotion","PPE"),True)
 m(("result","strict_nonpromotion","complete_18_field_operator_block_count"),1)
 m(("verdict","Gate5"),"CERTIFIED")
 return sum(bool(check(x)) for x in ms),len(ms)
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--manifest",type=Path,default=DEFAULT_MANIFEST);p.add_argument("--replay",action="store_true");p.add_argument("--integrity-only",action="store_true");p.add_argument("--self-test",action="store_true");a=p.parse_args()
 try:d=json.loads(a.manifest.read_text())
 except Exception as x:print("MANIFEST_READ_ERROR:",x,file=sys.stderr);return 1
 e=check(d)
 if e:print("ERROR:","; ".join(e),file=sys.stderr);return 1
 if a.replay and certificate.build_result()!=d["result"]:print("ERROR: replay",file=sys.stderr);return 1
 if a.self_test:
  x,n=selftest(d);print(f"SELF_TEST: {'PASS' if x==n else 'FAIL'} ({x}/{n} mutations rejected)");return 0 if x==n else 1
 if a.replay or a.integrity_only:print("REPLAY_AND_INTEGRITY: PASS");return 0
 print("GATE25_SELECTED_COMPONENT_LOCAL_CONTRACTING_CHARACTERISTIC_Z: CERTIFIED\nGATE25_FULL_KEY_FIELD7: NOT_CERTIFIED\nGATE2: NOT_CERTIFIED\nGATE5: NOT_CERTIFIED");return 2
if __name__=="__main__":raise SystemExit(main())
