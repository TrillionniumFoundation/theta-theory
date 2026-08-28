#!/usr/bin/env python3
"""Independent higher-precision audit of the Round89 projective gap frontier."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
from typing import Any
from cm2_round79_tangency_intersection_generator import digest
import cm2_round89_rank3_projective_gap_closure_cert as cert

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"cm2-round89-rank3-projective-gap-closure-2026-07-22.json"
PRODUCER_SHA256="6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf"

def pairs_hook(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError(f"duplicate key: {k}")
        out[k]=v
    return out
def bad_number(token): raise ValueError(f"nonfinite: {token}")
def strict_load(path:Path):
    return json.loads(path.read_text(),object_pairs_hook=pairs_hook,parse_constant=bad_number)
def sha(path:Path): return hashlib.sha256(path.read_bytes()).hexdigest()

def summary(result:dict[str,Any]):
    names=("input_locally_physical_port_count","input_live_registered_arc_count",
           "oriented_projective_tangent_branch_count","registered_source_endpoint_count",
           "unregistered_consecutive_projective_gap_count","certified_whole_tube_physical_gap_count",
           "remaining_unresolved_interior_projective_gap_count","remaining_exterior_branch_ray_count")
    return tuple(result[x] for x in names)
def endpoint_set(rows): return {(r["left_registered_port_id"],r["right_registered_port_id"]) for r in rows}

def verify_document(document:dict[str,Any], recomputed:dict[str,Any]) -> None:
    if set(document)!={"schema","result","result_sha256"} or document["schema"]!=cert.SCHEMA:
        raise ValueError("closed top-level schema")
    if digest(document["result"])!=document["result_sha256"]: raise ValueError("result digest")
    result=document["result"]; higher=recomputed["result"]
    if summary(result)!=(945,496,56,47,440,432,8,112): raise ValueError("frozen summary")
    if summary(result)!=summary(higher): raise ValueError("768-bit summary mismatch")
    if endpoint_set(result["gap_rows"])!=endpoint_set(higher["gap_rows"]): raise ValueError("certified gap-set mismatch")
    if endpoint_set(result["unresolved_gap_rows"])!=endpoint_set(higher["unresolved_gap_rows"]): raise ValueError("residual gap-set mismatch")
    if result["registered_arc_branch_key_mismatch_count"] or result["registered_arc_projective_rank_gap_histogram"]!={"1":449}:
        raise ValueError("projective adjacency")
    if result["branch_registered_source_endpoint_histogram"]!={"0":21,"1":23,"2":12}: raise ValueError("source histogram")
    if result["unresolved_gap_reason_histogram"]!={"IFT_BOUNDARY_SIGNS":8}: raise ValueError("residual reasons")
    if any(r["total_registered_endpoint_parity"] for r in result["branch_rows"]): raise ValueError("branch parity")

def build() -> dict[str,Any]:
    if sha(HERE/"cm2_round89_rank3_projective_gap_closure_cert.py")!=PRODUCER_SHA256:
        raise RuntimeError("producer pin mismatch")
    frozen=strict_load(MANIFEST)
    higher=cert.build(768)
    verify_document(frozen,higher)
    hostile=0
    for field,value in (("certified_whole_tube_physical_gap_count",440),
                        ("remaining_unresolved_interior_projective_gap_count",0),
                        ("remaining_exterior_branch_ray_count",0),
                        ("oriented_projective_tangent_branch_count",1)):
        mutated=json.loads(json.dumps(frozen)); mutated["result"][field]=value; mutated["result_sha256"]=digest(mutated["result"])
        try: verify_document(mutated,higher)
        except ValueError: hostile+=1
    if hostile!=4: raise RuntimeError("hostile mutation rejection")
    result={"status":"PASS","independent_precision_bits":768,"higher_precision_summary":summary(higher["result"]),
            "certified_gap_set_sha256":digest(sorted(endpoint_set(frozen["result"]["gap_rows"]))),
            "unresolved_gap_set_sha256":digest(sorted(endpoint_set(frozen["result"]["unresolved_gap_rows"]))),
            "producer_sha256":PRODUCER_SHA256,"manifest_sha256":sha(MANIFEST),
            "hostile_semantic_mutations_rejected":"4/4","strict_json_loader":"duplicate and nonfinite values rejected"}
    return {"schema":"cm2.round89.rank3-projective-gap-closure.audit.v1","result":result,"result_sha256":digest(result)}
def main(): json.dump(build(),sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__": raise SystemExit(main())
