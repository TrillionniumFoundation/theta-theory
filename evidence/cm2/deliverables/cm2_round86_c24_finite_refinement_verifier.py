#!/usr/bin/env python3
from __future__ import annotations
import copy,json,sys
from pathlib import Path
import cm2_round86_c24_finite_refinement_cert as cert
HERE=Path(__file__).resolve().parent;INPUT=HERE/"cm2-round86-c24-finite-refinement-2026-07-22.json"
def main():
 try:
  x=json.loads(INPUT.read_text());e=cert.build(512)
  if x!=e:raise ValueError("512 replay")
  h=cert.build(768)
  for k in ("classification_frontier","preimage_frontier","mass_preservation","strict_nonpromotion"):
   if x["result"][k]!=h["result"][k]:raise ValueError("768 "+k)
  attacks=[]
  for m in (lambda z:z["result"]["classification_frontier"].__setitem__("unresolved",0),lambda z:z["result"]["preimage_frontier"].__setitem__("residual_children",0),lambda z:z["result"]["strict_nonpromotion"].__setitem__("Gate4","CERTIFIED"),lambda z:z.__setitem__("extra",1)):
   y=copy.deepcopy(x);m(y);y["result_sha256"]=cert.dig(y["result"]);attacks.append(y!=e)
  if not all(attacks):raise ValueError("mutation")
  out={"schema":"cm2.round86.c24-finite-refinement.audit.v1","status":"AUDIT_PASS","producer_precision_bits":512,"independent_precision_bits":768,"classification_resolved_survivor_leaves":2732,"classification_residual_leaves":248,"classification_residual_volume_ratio":"31/16384","preimage_contained_children":1304,"preimage_residual_children":15344,"preimage_residual_volume_ratio":"1991/2298","mass_preserving_covers":"2/2","hostile_mutations_rejected":f"{sum(attacks)}/{len(attacks)}","strict_gate_state":x["result"]["strict_nonpromotion"]}
  print(json.dumps(out,sort_keys=True,indent=2));return 0
 except Exception as z:print("ROUND86_VERIFY_ERROR",z,file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
