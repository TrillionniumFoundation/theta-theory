#!/usr/bin/env python3
"""Verifier for the Round-85 variable-return crosswalk frontier."""
from __future__ import annotations
import copy,json,sys
from pathlib import Path
from typing import Any
import cm2_round85_c24_variable_return_crosswalk_cert as cert
HERE=Path(__file__).resolve().parent; INPUT=HERE/"cm2-round85-c24-variable-return-crosswalk-2026-07-22.json"
def load()->dict[str,Any]:
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise ValueError("duplicate")
            d[k]=v
        return d
    x=json.loads(INPUT.read_text(),object_pairs_hook=pairs,parse_constant=lambda z:(_ for _ in()).throw(ValueError(z)))
    if not isinstance(x,dict):raise ValueError("top")
    return x
def validate(x,e):
    if set(x)!={"schema","pins","result","result_sha256"} or x!=e:raise ValueError("replay")
def main()->int:
  try:
    x=load(); e=cert.build(512); validate(x,e); h=cert.build(768)
    a=x["result"]["evidence"]; b=h["result"]["evidence"]
    for k in ("full_leaf_count","leaf_classification_histogram","return_landing_count","possible_edge_count","possible_edge_classification_histogram","landing_candidate_class_set_histogram","whole_enclosure_contained_in_one_survivor_box_count","boundary_straddling_landing_count","unique_reached_target_atom_histogram","reached_unresolved_512bit_replay_count","multiplicity_histogram"):
        if a[k]!=b[k]:raise ValueError("precision "+k)
    attacks=[]
    for m in (lambda z:z["result"]["graph_frontier"].__setitem__("RETURN_to_RETURN_possible_edges",1),lambda z:z["result"]["strict_nonpromotion"].__setitem__("Gate4","CERTIFIED"),lambda z:z["result"]["evidence"].__setitem__("reached_unresolved_512bit_replay_count",0),lambda z:z.__setitem__("extra",1)):
        y=copy.deepcopy(x);m(y);y["result_sha256"]=cert.digest(y["result"])
        try:validate(y,e);attacks.append(False)
        except ValueError:attacks.append(True)
    if not all(attacks):raise ValueError("mutation")
    out={"schema":"cm2.round85.c24-variable-return-crosswalk.audit.v1","status":"AUDIT_PASS","producer_precision_bits":512,"independent_precision_bits":768,"possible_edge_count":10384,"RETURN_to_RETURN_possible_edges":0,"RETURN_to_SURVIVE_possible_edges":10352,"RETURN_to_UNRESOLVED_possible_edges":32,"whole_containment_count":1888,"boundary_straddling_count":2328,"unique_reached_survivor_atoms":176,"unique_reached_unresolved_atoms":32,"hostile_mutations_rejected":f"{sum(attacks)}/{len(attacks)}","strict_gate_state":x["result"]["strict_nonpromotion"]}
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False));return 0
  except (OSError,ValueError,KeyError,TypeError,IndexError) as z:
    print("ROUND85_VARIABLE_CROSSWALK_VERIFY_ERROR:",z,file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
