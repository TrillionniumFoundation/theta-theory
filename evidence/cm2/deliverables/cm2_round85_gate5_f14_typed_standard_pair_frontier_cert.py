#!/usr/bin/env python3
"""Typed central standard pairs and the full-packet recovery frontier for F14."""
from __future__ import annotations
import hashlib,json,sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb,ctx
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert
HERE=Path(__file__).resolve().parent
SCHEMA="cm2.round85.gate5-f14-typed-standard-pair-frontier.v1"
WINDOWS=HERE/"cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
DENSITY=HERE/"cm2-round85-gate5-f14-local-collision-density-input-2026-07-22.json"
CONE=HERE/"cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
PINS={"windows":"81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
 "density_inputs":"8a7ff59660cae11d213982b79d8bcb8692649df6ec0edbba39780846d4099a16",
 "invariant_cone":"173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
 "core_source":"2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"}
def canon(v):return json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False)
def dig(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def fd(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 def u(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError("dup")
   d[k]=v
  return d
 x=json.loads(p.read_text(),object_pairs_hook=u,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
 if not isinstance(x,dict):raise ValueError("top")
 return x
def aq(x):x=Q(x);return arb(x.numerator)/x.denominator
def build(bits=512):
 ctx.prec=bits
 actual={"windows":fd(WINDOWS),"density_inputs":fd(DENSITY),"invariant_cone":fd(CONE),"core_source":fd(HERE/"cm2_gate25_physical_return_core_registry_cert.py")}
 if actual!=PINS:raise ValueError("pins")
 windows=load(WINDOWS)["result"]["evidence"]["window_rows"]
 density=load(DENSITY)["result"];cone=load(CONE)["result"]["global_invariant_geometric_cone"]
 if density["F14_numerical_formula_input_rows"]!="152/152":raise ValueError("density")
 if cone["curvature_lower"]!="25/9" or cone["cone_upper"]!="4108425/145348":raise ValueError("cone")
 if cone["fixed_geometric_unstable_cone"]!="25/9<V=dphi/dr<4108425/145348<29":raise ValueError("cone formula")
 cores={return_cert.core_id(c):c for c in core_cert.physical_cores()};rows=[]
 for w in sorted(windows,key=lambda x:x["positive_atom_id"]):
  c=cores[w["source_core_id"]];R=aq(first_hit.RADIUS[c.source]);t0,t1=map(aq,w["common_t"]);p0,p1=map(aq,w["common_p"])
  tc=(t0+t1)/2;pc=(p0+p1)/2;rc=R*tc.asin();phic=pc.asin()
  left=(phic+4*(R*t0.asin()-rc)).sin();right=(phic+4*(R*t1.asin()-rc)).sin()
  if not (left-p0>aq(Q(3,10000)) and p1-right>aq(Q(3,10000))):raise ValueError("endpoint margin")
  r0=R*t0.asin();r1=R*t1.asin();phi0=phic+4*(r0-rc);phi1=phic+4*(r1-rc)
  length=arb(17).sqrt()*(r1-r0)
  if not (length>aq(Q(1,4000)) and length<aq(Q(7,10000))):raise ValueError("length")
  q0=phi0.cos();q1=phi1.cos();qmin=min(q0,q1);z=(right-left)/4
  if not (qmin>aq(Q(999,1000)) and z>0):raise ValueError("positive collision density")
  density_scale=1/(z*arb(17).sqrt())
  if not (density_scale*qmin>1400 and density_scale<5010):raise ValueError("density range")
  pmax=max(abs(left),abs(right))
  log_lip=4*pmax/(arb(17).sqrt()*qmin)
  tv_bound=density_scale*pmax*(phi1-phi0)
  if not (log_lip<aq(Q(1,40)) and tv_bound<aq(Q(1,15))):raise ValueError("density regularity")
  rows.append({"atom_id":w["positive_atom_id"],"source_core_id":w["source_core_id"],"destination_core_id":w["destination_core_id"],
   "curve":"phi(r)=4*(r-r_c)+phi_c","r_c":"R*asin((t0+t1)/2)","phi_c":"asin((p0+p1)/2)",
   "unstable_slope_dphi_dr":"4","graph_second_derivative":"0","p_strictly_monotone":True,
   "endpoint_type":"TWO_DISTINCT_t_BOUNDARY_ENDPOINTS_STRICTLY_INSIDE_p_RANGE","endpoint_p_margin_strict_lower":"3/10000",
   "arclength_bounds":["1/4000","7/10000"],"homogeneity_owner":"INHERITED_STRICT_ON_WINDOW",
   "conditional_q":"cos(phi)","arclength_factor":"sqrt(17)","Z":"(p_right-p_left)/4",
   "normalized_density":"cos(phi)/(Z*sqrt(17))","density_bounds":"1400<rho<5010",
   "log_density_Lipschitz_strict_upper":"1/40","density_total_variation_strict_upper":"1/15",
   "BV_probability_norm_strict_upper":"16/15","typed_standard_pair":"CERTIFIED_CENTRAL_CURVE"})
 evidence={"precision_bits":bits,"p_constant_fibre_audit":{"dphi_dr":"0","required":"25/9<dphi/dr<29","status":"STRICTLY_OUTSIDE_UNSTABLE_CONE"},
  "cone_aligned_central_standard_pair_count":len(rows),"uniform_slope":"4","uniform_graph_second_derivative":"0",
  "uniform_endpoint_p_margin_strict_lower":"3/10000","uniform_arclength_lower":"1/4000","uniform_arclength_strict_upper":"7/10000",
  "uniform_density_bounds":"1400<rho<5010","uniform_log_density_Lipschitz_strict_upper":"1/40",
  "uniform_density_total_variation_strict_upper":"1/15","local_BV_probability_norm_strict_upper":"16/15",
  "minimal_local_recipient":{"space":"X_central=direct_sum_(152) BV(W_i)","coefficient_space":"ell^1(152)",
   "synthesis":"S(c)_i=c_i*rho_i","operator_norm_strict_upper":"16/15","bounded":True},
  "full_rectangle_parallel_foliation":{"label":"v=phi-4r","corner_support_labels_have_zero_length_fibres":True,
   "infimum_nonempty_fibre_length":"0","normalized_density_supremum_without_transverse_weight_recovery":"INFINITE",
   "covers_complete_packet_with_uniform_BV_cost":False},"standard_pair_rows":rows}
 result={"status":"CERTIFIED_152_TYPED_CENTRAL_STANDARD_PAIRS_AND_BOUNDED_LOCAL_BV_SYNTHESIS",
  "finite_root_typed_F14_central_subfamily_input":"CERTIFIED_152_OF_152","regular_density_operator_cost_on_central_direct_sum":"STRICTLY_LESS_THAN_16/15",
  "full_packet_F14_regular_density_operator_cost":"NOT_CERTIFIED__ZERO_LENGTH_CORNER_FIBRES_AND_NO_TRANSVERSE_WEIGHT_RECOVERY",
  "candidate_packet_maturity":"13/18_UNCHANGED","global_or_all_depth_Gate5":"NOT_CERTIFIED",
  "last_exact_type_gap":"construct the transverse quotient/weights and short-fibre recovery for the full rectangle foliation, or trim/repartition with a keyed recovery law",
  "strict_nonclaims":["a bounded central standard-pair synthesis is not the full packet operator","no stable foliation or all-depth recovery is asserted","no F15/F16 promotion"],
  "evidence":evidence,"evidence_sha256":dig(evidence)}
 return {"schema":SCHEMA,"pins":dict(PINS),"result":result,"result_sha256":dig(result)}
def main():json.dump(build(),sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
