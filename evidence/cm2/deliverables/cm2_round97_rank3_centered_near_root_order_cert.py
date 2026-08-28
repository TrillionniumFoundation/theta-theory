#!/usr/bin/env python3
"""Centered near-root ordering for the ten Round96 third-competitor families."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from flint import ctx
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round96_rank3_correlated_owner_interval_cert as round96
from cm2_round79_tangency_intersection_generator import digest,strict_sign
HERE=Path(__file__).resolve().parent;R96=HERE/"cm2-round96-rank3-correlated-owner-interval-2026-07-22.json"
PINS={R96.name:"d0bd4983f18ab2ab6d467bb7b0ef20626a6f603a901624e14847cd140f839eeb","cm2_round96_rank3_correlated_owner_interval_cert.py":"5c0205e4756270d8f94ede4947c2b80f82ad655b37d81a6bc02aa8bade54c702"}
SCHEMA="cm2.round97.rank3-centered-near-root-order.v1";PRECISION_BITS=512
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enhanced_clear_before(point,velocity,target,terminal,stage):
 delta=round95.sub(round95.center(target),point);ell=round95.dot(velocity,delta);transverse=round95.cross(velocity,delta);r=round95.radius(target);line_clear=transverse*transverse-r*r;end_clear=(ell-terminal)*(ell-terminal)+transverse*transverse-r*r
 if strict_sign(line_clear.value)==1:return "WHOLE_LINE_MISS"
 if bool(ell.value<0):return "CLOSEST_BEHIND_START"
 if bool(ell.value>terminal.value) and strict_sign(end_clear.value)==1:return "CLOSEST_AFTER_TERMINAL__END_CLEAR"
 discriminant=r*r-transverse*transverse
 if strict_sign(discriminant.value)==1:
  root=discriminant.sqrt();near=ell-root;far=ell+root
  if bool(far.value<0):return "BOTH_ROOTS_BEHIND_START"
  if bool(near.value>terminal.value):return "STRICT_NEAR_ROOT_AFTER_TERMINAL"
 raise RuntimeError(f"{stage} centered near-root unresolved:{target}")
def build(precision_bits=PRECISION_BITS):
 ctx.prec=precision_bits
 for n,h in PINS.items():
  if sha(HERE/n)!=h:raise RuntimeError(f"pin:{n}")
 old_clear,old_depth=round96.clear_before,round96.MAX_DEPTH
 try:
  round96.clear_before=enhanced_clear_before;round96.MAX_DEPTH=0;base=round96.build(precision_bits)
 finally:
  round96.clear_before,round96.MAX_DEPTH=old_clear,old_depth
 r=base["result"];all_reasons=r["global_unresolved_reason_histogram"];third_residual=sum(v for k,v in all_reasons.items() if "third centered near-root" in k);representation=sum(v for k,v in all_reasons.items() if "third centered near-root" not in k);result={"precision_bits":precision_bits,"input_round96_base_gap_count":r["input_probe_gap_count"],"first_second_owner_base_gap_certified_count":r["input_probe_gap_count"]-representation,"third_competitor_certified_leaf_count":sum(x["certified_correlated_leaf_count"] for x in r["ray_rows"]),"third_competitor_residual_leaf_count":third_residual,"representation_boundary_residual_leaf_count":representation,"fully_correlated_owner_covered_ray_count":r["fully_correlated_owner_covered_ray_count"],"global_unresolved_reason_histogram":all_reasons,"ray_rows":r["ray_rows"],"ray_rows_sha256":r["ray_rows_sha256"],"strict_scope":"adaptive same-q centered near-root minus designated-flight ordering for all Round96 third competitors","strict_nonclaims":["Round95 endpoint representation leaves remain separately pinned","face quotient assembly remains separate"],"upstream_pins":PINS};result=json.loads(json.dumps(result,sort_keys=True));return {"schema":SCHEMA,"result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
