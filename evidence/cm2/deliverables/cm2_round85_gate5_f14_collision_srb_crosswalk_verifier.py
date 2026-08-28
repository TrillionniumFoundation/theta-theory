#!/usr/bin/env python3
"""Verifier for the Round-85 F14 collision-SRB root crosswalk."""
from __future__ import annotations

import copy, json, math, sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
import cm2_round85_gate5_f14_collision_srb_crosswalk_cert as cert

HERE=Path(__file__).resolve().parent
INPUT=HERE/"cm2-round85-gate5-f14-collision-srb-crosswalk-2026-07-22.json"
def unique(pairs):
    result={}
    for k,v in pairs:
        if k in result: raise ValueError("duplicate")
        result[k]=v
    return result
def loads(raw):
    x=json.loads(raw,object_pairs_hook=unique,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
    def walk(v):
        if isinstance(v,float) and not math.isfinite(v):raise ValueError("nonfinite")
        if isinstance(v,dict):
            for c in v.values():walk(c)
        elif isinstance(v,list):
            for c in v:walk(c)
    walk(x);return x
def validate(x,e):
    if not isinstance(x,dict) or set(x)!={"schema","pins","result","result_sha256"}:raise ValueError("schema")
    if x["result_sha256"]!=cert.digest(x["result"]):raise ValueError("digest")
    if x["result"]["evidence_sha256"]!=cert.digest(x["result"]["evidence"]):raise ValueError("evidence")
    if x!=e:raise ValueError("replay")
def rejected(x,e):
    try:validate(x,e)
    except (ValueError,KeyError,TypeError,IndexError):return True
    return False
def main(argv):
    path=Path(argv[1]).resolve() if len(argv)>1 else INPUT
    value=loads(path.read_text());expected=cert.build();validate(value,expected)
    rows=value["result"]["evidence"]["crosswalk_rows"]
    if len(rows)!=152 or len({r["atom_id"] for r in rows})!=152:raise ValueError("rows")
    if any(Q(r["exact_gap"])<Q(9,6400) or r["F14_formula_attachable"] for r in rows):raise ValueError("gap")
    mutations=(
      lambda x:x["result"].__setitem__("F14_regular_density_operator_cost","CERTIFIED"),
      lambda x:x["result"].__setitem__("candidate_local_maturity","14/18"),
      lambda x:x["result"].__setitem__("F15_standard_family_operator_cost","CERTIFIED"),
      lambda x:x["result"]["evidence"].__setitem__("attachable_F14_row_count",152),
      lambda x:x["result"]["evidence"]["crosswalk_rows"][0].__setitem__("F14_formula_attachable",True),
      lambda x:x.__setitem__("extra_claim","CERTIFIED"),
    )
    attacks=[]
    for m in mutations:
      h=copy.deepcopy(value);m(h);h["result"]["evidence_sha256"]=cert.digest(h["result"]["evidence"]);h["result_sha256"]=cert.digest(h["result"]);attacks.append(rejected(h,expected))
    pins=[]
    for k in value["pins"]:
      h=copy.deepcopy(value);h["pins"][k]="0"*64;pins.append(rejected(h,expected))
    if not all(attacks) or not all(pins):raise ValueError("mutation")
    strict=0
    for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}','{"x":1e9999}'):
      try:loads(raw)
      except ValueError:strict+=1
    if strict!=4:raise ValueError("strict")
    result={"exact_crosswalk_rows":152,"uniform_s_gap":"9/6400","attachable_F14_rows":0,
      "candidate_local_maturity":"13/18_UNCHANGED","hostile_mutations_rejected":f"{sum(attacks)}/{len(attacks)}",
      "coordinated_pin_mutations_rejected":f"{sum(pins)}/{len(pins)}","strict_json_attacks_rejected":f"{strict}/4","verdict":"PASS"}
    audit={"schema":"cm2.round85.gate5-f14-collision-srb-crosswalk-audit.v1","result":result,"result_sha256":cert.digest(result)}
    json.dump(audit,sys.stdout,sort_keys=True,indent=2,allow_nan=False);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main(sys.argv))
