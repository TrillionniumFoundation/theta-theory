#!/usr/bin/env python3
"""Local collision-density formula inputs on all 152 finite-root F14 keys."""
from __future__ import annotations

import hashlib, json, sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import ctx

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert

HERE=Path(__file__).resolve().parent
SCHEMA="cm2.round85.gate5-f14-local-collision-density-input.v1"
WINDOWS=HERE/"cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
F14_FRONTIER=HERE/"cm2-round85-gate5-f14-collision-srb-crosswalk-2026-07-22.json"
CORE_MANIFEST=HERE/"cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
FROZEN_PINS={
 "round85_material_windows":"81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
 "round85_F14_crosswalk":"178d4367b017556f5e96c1adad7362b4ae88a0d6ccef64c9b2886db7568dce3f",
 "physical_core_manifest":"144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
 "physical_core_source":"2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
 "return_classifier_source":"d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False)
def digest(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
def fd(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 def uniq(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError("duplicate")
   d[k]=v
  return d
 x=json.loads(p.read_text(),object_pairs_hook=uniq,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
 if not isinstance(x,dict):raise ValueError("top")
 return x
def build(precision_bits=512):
 ctx.prec=precision_bits
 actual={"round85_material_windows":fd(WINDOWS),"round85_F14_crosswalk":fd(F14_FRONTIER),
  "physical_core_manifest":fd(CORE_MANIFEST),"physical_core_source":fd(HERE/"cm2_gate25_physical_return_core_registry_cert.py"),
  "return_classifier_source":fd(HERE/"cm2_gate34_full_core_return_adaptive_frontier_cert.py")}
 if actual!=FROZEN_PINS:raise ValueError("pins")
 windows=load(WINDOWS)["result"]["evidence"]["window_rows"]
 if len(windows)!=152:raise ValueError("windows")
 cores=core_cert.physical_cores(); registry={return_cert.core_id(c):(i,c) for i,c in enumerate(cores)}
 core_rows={return_cert.core_id(c):core_cert.certify_core(c) for c in cores}
 rows=[]
 for w in sorted(windows,key=lambda x:x["positive_atom_id"]):
  sid=w["source_core_id"];did=w["destination_core_id"]
  index,source=registry[sid]
  t0,t1=map(Q,w["common_t"]);p0,p1=map(Q,w["common_p"]);s0,s1=map(Q,w["common_s"])
  if t1-t0!=Q(1,3200) or p1-p0!=Q(1,800) or (s0,s1)!=(-Q(1,6400),Q(1,6400)):raise ValueError("window shape")
  core_row=core_rows[sid]
  if not core_row["strict_first_hit"] or core_row["incoming_and_outgoing_cos_phi_strict_lower"]!="19/20":raise ValueError("owner margin")
  classifications=[]
  for label,lo,hi in (("negative",s0,Q(0)),("positive",Q(0),s1)):
   atom=return_cert.Atom(index,source,t0,t1,p0,p1,lo,hi,"round85-"+label)
   classified=return_cert.classify_atom(atom,cores)
   if classified["classification"]!="RETURN_AT_1_INNER" or classified["destination_core_id"]!=did:raise ValueError("half-slab replay")
   if return_cert.atom_geometry(atom) is None:raise ValueError("flight geometry")
   classifications.append({"side":label,"strict_first_owner":True,"collision_geometry":"STRICT_REAL_ROOT",
    "landing":"STRICTLY_INSIDE_DECLARED_DESTINATION_CORE"})
  R=first_hit.RADIUS[source.source]
  t_abs=max(abs(t0),abs(t1));denom=1-t_abs*t_abs
  if denom<Q(51,100):raise ValueError("denominator")
  # q=a=R/sqrt(1-t^2).  These squared comparisons prove the uniform bounds.
  if R*R/denom>=Q(13,25)**2 or R<Q(4,25):raise ValueError("q/a bound")
  dt=t1-t0;Z_lower=R*dt
  if Z_lower<Q(1,20000):raise ValueError("Z lower")
  if (R*dt)**2/denom>=Q(1,6000)**2:raise ValueError("Z upper")
  rows.append({"atom_id":w["positive_atom_id"],"source_core_id":sid,"destination_core_id":did,
   "source_radius":str(R),"t":w["common_t"],"p":w["common_p"],"s":w["common_s"],
   "coordinate_fibres":"u=t, v=p","Phi":"(R*asin(u),v)","q":"R/sqrt(1-u^2)","a":"R/sqrt(1-u^2)",
   "Z":"R*(asin(t1)-asin(t0))","rho_v":"1/Z","lambda":"1","J":"1",
   "one_minus_t_squared_lower":str(denom),"Z_rational_lower":str(Z_lower),
   "q_a_bounds":"4/25<=q=a<13/25","rho_bounds":"6000<rho_v<=20000","lambda_J_exact":"1",
   "half_slab_physical_replay":classifications,
   "physical_stable_or_standard_family_semantics":"NOT_CERTIFIED"})
 evidence={"precision_bits":precision_bits,"formula_row_count":len(rows),"strict_denominator_rows":len(rows),
  "strict_two_half_slab_flight_owner_landing_replays":2*len(rows),"uniform_one_minus_t_squared_lower":"51/100",
  "uniform_q_a_lower":"4/25","uniform_q_a_strict_upper":"13/25","uniform_Z_lower":"1/20000",
  "uniform_Z_strict_upper":"1/6000","uniform_rho_strict_lower":"6000","uniform_rho_upper":"20000",
  "lambda_exact":"1","J_exact":"1","formula_rows":rows}
 result={"status":"CERTIFIED_152_SAME_KEY_LOCAL_COLLISION_DENSITY_FORMULA_INPUTS",
  "F14_numerical_formula_input_rows":"152/152","F14_regular_density_operator_cost":"NOT_CERTIFIED__RECOVERED_STRONG_BANACH_RECIPIENT_AND_PHYSICAL_STANDARD_FAMILY_TYPING_ABSENT",
  "candidate_local_maturity":"13/18_UNCHANGED","complete_18_field_operator_blocks":0,
  "necessary_next_action":"CONSTRUCT_ONE_RECOVERED_STRONG_OPERATOR_RECIPIENT_AND_TYPE_THE_LOCAL_FIBRES_AS_PHYSICAL_STANDARD_FAMILIES",
  "strict_nonclaims":["p-constant coordinate fibres are not asserted to be invariant stable plaques","bounded collision density is an F14 input, not the recovered strong operator cost","no F15 or aggregate F16 promotion"],
  "evidence":evidence,"evidence_sha256":digest(evidence)}
 return {"schema":SCHEMA,"pins":dict(FROZEN_PINS),"result":result,"result_sha256":digest(result)}
def main():json.dump(build(),sys.stdout,sort_keys=True,indent=2,allow_nan=False);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
