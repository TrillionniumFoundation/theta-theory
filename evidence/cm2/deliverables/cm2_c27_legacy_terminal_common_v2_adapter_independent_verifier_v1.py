#!/usr/bin/env python3
"""Independent inverse reconstruction of the six-terminal common-v2 adapter."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / ".cm2-runtime/audit/c27-legacy-terminal-typed-ownership-v1-seed-30650101"
SOURCE_CANDIDATES = SOURCE_DIR / "typed_candidate_ownership.jsonl.gz"
SOURCE_INCIDENCES = SOURCE_DIR / "proof_incidence.jsonl.gz"
SOURCE_VERIFY = SOURCE_DIR / "independent_verification_seed30651701.json"
INTERFACE = ROOT / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json"
PINS = {
    SOURCE_CANDIDATES: "0eb6f69029f8fa005b105867641027c8a70b41d0fd72c9fe271b367b64c31887",
    SOURCE_INCIDENCES: "89198283305ea41885c8aa7c36faaf410a3bd92b536f8e8f46cd87b488cad4db",
    SOURCE_VERIFY: "7efea3814968b13cba70a86a53fa4c8e4f649806c289e0a12c88f78d9634fe9c",
    INTERFACE: "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6",
}
TERMINALS = {
    "RETAINED_CONTINUATION": (1, "T01_RETAINED_CONTINUATION", "REPRESENTATION_CANDIDATE"),
    "OUTGOING_GRAPHS": (2, "T02_OUTGOING_GRAPHS", "GRAPH_ROOT_CANDIDATE"),
    "SINGLE_GRAPHS": (3, "T03_SINGLE_GRAPHS", "GRAPH_ROOT_CANDIDATE"),
    "SHEET_OWNER": (5, "T05_SHEET_OWNER", "PHYSICAL_SHEET_ROLE_CANDIDATE"),
    "SHEET_SHADOW": (6, "T06_SHEET_SHADOW", "PHYSICAL_SHEET_ROLE_CANDIDATE"),
    "INCLUDED_STRATUM_ATTACHMENTS": (10, "T10_INCLUDED_STRATUM_ATTACHMENTS", "REPRESENTATION_CANDIDATE"),
}
EXPECTED = {"RETAINED_CONTINUATION":276,"OUTGOING_GRAPHS":264,
            "SINGLE_GRAPHS":4984,"SHEET_OWNER":17940,"SHEET_SHADOW":17940,
            "INCLUDED_STRATUM_ATTACHMENTS":10660}
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(encode(value)).hexdigest()


def file_hash(path: Path) -> str:
    state=hashlib.sha256()
    with path.open("rb") as handle:
        while block:=handle.read(8<<20): state.update(block)
    return state.hexdigest()


def closed(row: dict[str,Any], key: str, label: str) -> None:
    claim=row.get(key); body=dict(row); body.pop(key,None)
    need(type(claim) is str and claim==digest(body),label+":closure")


def jsonl(path: Path) -> Iterable[dict[str,Any]]:
    with gzip.open(path,"rt",encoding="ascii") as handle:
        for line in handle: yield json.loads(line)


def sequence_sha(shas: list[str]) -> str:
    state=hashlib.sha256()
    for value in shas: state.update(value.encode("ascii")+b"\n")
    return state.hexdigest()


def load_rows(path: Path, schema: str, label: str) -> list[dict[str,Any]]:
    rows=[]
    for ordinal,row in enumerate(jsonl(path)):
        closed(row,"row_sha256",f"{label}:{ordinal}")
        need(row["ordinal"]==ordinal and row["schema"]==schema,f"{label}:{ordinal}:wire")
        rows.append(row)
    return rows


def verify(directory: Path) -> dict[str,Any]:
    for path,expected in PINS.items():
        need(path.is_file() and not path.is_symlink() and file_hash(path)==expected,"pin:"+path.name)
    native_verify=json.loads(SOURCE_VERIFY.read_bytes());closed(native_verify,"verification_sha256","native verify")
    need(native_verify["producer_imported_or_executed"] is False
         and native_verify["candidate_total"]==52064
         and native_verify["proof_incidence_total"]==62160,"native verified source")
    interface=json.loads(INTERFACE.read_bytes())["corrected_interface"]
    need(interface["candidate_ownership_ledger"]["row_schema"]==CANDIDATE_SCHEMA
         and interface["materialized_physical_proof_join_ledger"]["row_schema"]==PROOF_SCHEMA,
         "corrected interface")
    result_path=directory/"result.json"; result=json.loads(result_path.read_bytes())
    closed(result,"result_sha256","result")
    need(result["candidate_total"]==52064 and result["native_semantic_proof_incidence_total"]==62160
         and result["materialized_physical_proof_join_total"]==216
         and result["component_relation_disposition_census"]=={
             "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED":216,
             "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS":11056,
             "SAME_FROZEN_C15_COMPONENT__NO_EDGE":40792}
         and result["formal_credit"]==0 and result["manifest_authorized"] is False
         and result["source_W_transition_authorized"] is False
         and result["global_atom_and_full_twenty_family_totality_closed"] is False,
         "result semantics")

    native_candidates: dict[str,dict[str,Any]]={}; by_terminal={t:[] for t in TERMINALS}
    for ordinal,row in enumerate(jsonl(SOURCE_CANDIDATES)):
        closed(row,"row_sha256",f"native candidate:{ordinal}")
        need(row["ordinal"]==ordinal and row["terminal"] in TERMINALS,"native candidate wire")
        native_candidates[row["candidate_id"]]=row;by_terminal[row["terminal"]].append(row)
    incidences={key:[] for key in native_candidates}
    for ordinal,row in enumerate(jsonl(SOURCE_INCIDENCES)):
        closed(row,"row_sha256",f"native incidence:{ordinal}")
        need(row["ordinal"]==ordinal and row["candidate_id"] in incidences,"native incidence wire")
        incidences[row["candidate_id"]].append(row)
    need({t:len(rows) for t,rows in by_terminal.items()}==EXPECTED,"native census")

    entry_by_terminal={entry["terminal"]:entry for entry in result["adapter_entries"]}
    need(set(entry_by_terminal)==set(TERMINALS),"adapter entries")
    total=proof_total=0; relation_census={}; proof_keys=set(); edge_keys=set(); member_pairs=set()
    for terminal,(ti,slot,kind) in sorted(TERMINALS.items(),key=lambda item:item[1][0]):
        entry=entry_by_terminal[terminal]
        candidate_path=directory/entry["candidate_ownership_ledger"]["path"]
        proof_path=directory/entry["materialized_physical_proof_join_ledger"]["path"]
        observed_candidates=load_rows(candidate_path,CANDIDATE_SCHEMA,terminal+":candidate")
        observed_proofs=load_rows(proof_path,PROOF_SCHEMA,terminal+":proof")
        for path,rows,desc in ((candidate_path,observed_candidates,entry["candidate_ownership_ledger"]),
                               (proof_path,observed_proofs,entry["materialized_physical_proof_join_ledger"])):
            need(file_hash(path)==desc["file_sha256"] and path.stat().st_size==desc["file_size"]
                 and len(rows)==desc["row_count"]
                 and sequence_sha([row["row_sha256"] for row in rows])==desc["row_sequence_sha256"],
                 terminal+":descriptor")
        expected_candidates=[]; expected_proofs=[]
        for ordinal,source in enumerate(sorted(by_terminal[terminal],key=lambda row:row["candidate_id"])):
            candidate_proofs=[]
            if terminal=="SINGLE_GRAPHS":
                evidence_rows=incidences[source["candidate_id"]]
                g2a_rows=[row for row in evidence_rows if row["evidence"]["role"]=="G2A_SHEET"]
                need(len(g2a_rows)==1,"single G2A")
                g2a=g2a_rows[0]["evidence"]
                positives=[row for row in evidence_rows if row["evidence"]["role"]=="G2B_POSITIVE_SIDE"]
                cross=[row for row in positives if row["evidence"]["fresh_component_id"]!=g2a["fresh_component_id"]]
                components={row["evidence"]["fresh_component_id"] for row in evidence_rows}
                if cross:
                    relation="CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
                    for incidence in sorted(cross,key=lambda row:row["row_sha256"]):
                        positive=incidence["evidence"]
                        mp=sorted([g2a["member_id"],positive["member_id"]])
                        cp=sorted([g2a["fresh_component_id"],positive["fresh_component_id"]])
                        proof_key="round306c27r2-v5-physical-proof:"+digest([source["candidate_id"],incidence["row_sha256"],mp])
                        witness="single-graph-positive-incidence:"+digest([source["candidate_id"],g2a_rows[0]["row_sha256"],incidence["row_sha256"]])
                        edge="round306c27r2-v5-component-edge:"+digest(cp)
                        body={"schema":PROOF_SCHEMA,"ordinal":len(expected_proofs),"proof_row_key":proof_key,
                              "candidate_key":source["candidate_id"],"atom_pair_incidence_key_or_null":None,
                              "terminal":terminal,"authority_slot":slot,
                              "primitive_authority_row_sha256":source["row_sha256"],
                              "ordered_C15_member_pair":mp,"ordered_C15_component_pair":cp,
                              "component_edge_key":edge,"physical_witness_key":witness,"formal_credit":0}
                        proof={**body,"row_sha256":digest(body)}
                        expected_proofs.append(proof);candidate_proofs.append(proof)
                elif len(components)==1:
                    relation="SAME_FROZEN_C15_COMPONENT__NO_EDGE"
                else:
                    need(any(row["evidence"]["role"]=="G2B_EXACT_EMPTY_SIDE"
                             and row["evidence"]["fresh_component_id"]!=g2a["fresh_component_id"]
                             for row in evidence_rows),"single empty-only split")
                    relation="NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
            elif terminal in {"OUTGOING_GRAPHS","SHEET_OWNER","SHEET_SHADOW"}:
                relation="SAME_FROZEN_C15_COMPONENT__NO_EDGE"
            else:
                relation="NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
            body={"schema":CANDIDATE_SCHEMA,"ordinal":ordinal,"candidate_key":source["candidate_id"],
                  "candidate_kind":kind,"candidate_pair_key_or_null":None,"terminal_ordinal":ti,
                  "terminal":terminal,"authority_slot":slot,
                  "primitive_authority_row_sha256":source["row_sha256"],
                  "component_relation_disposition":relation,
                  "physical_proof_row_count":len(candidate_proofs),
                  "physical_proof_row_sequence_sha256":sequence_sha([p["row_sha256"] for p in candidate_proofs]),
                  "formal_credit":0}
            expected_candidates.append({**body,"row_sha256":digest(body)})
            relation_census[relation]=relation_census.get(relation,0)+1
        need(observed_candidates==expected_candidates and observed_proofs==expected_proofs,
             terminal+":inverse exact match")
        for proof in observed_proofs:
            need(proof["proof_row_key"] not in proof_keys
                 and tuple(proof["ordered_C15_member_pair"]) not in member_pairs,
                 "proof uniqueness")
            proof_keys.add(proof["proof_row_key"]);member_pairs.add(tuple(proof["ordered_C15_member_pair"]))
            edge_keys.add(proof["component_edge_key"])
        need(entry["native_candidate_count"]==len(observed_candidates)
             and entry["semantic_incidences_promoted_to_physical_proof_count"]==len(observed_proofs),
             terminal+":entry census")
        total+=len(observed_candidates);proof_total+=len(observed_proofs)
    need(total==52064 and proof_total==216 and len(member_pairs)==216 and len(edge_keys)==88,
         "global adapter census")
    need(relation_census==result["component_relation_disposition_census"],"relation census")
    body={
        "schema":"cm2.c27-independent.legacy-terminal.common-v2-adapter.verification.v1",
        "status":"PASS_NO_ADAPTER_IMPORT__EXACT_INVERSE_52064_CANDIDATES__216_T03_PHYSICAL_PROOFS__88_EDGES__ZERO_CREDIT",
        "adapter_imported_or_executed":False,
        "native_authority_verification_bound":True,
        "candidate_total":52064,"materialized_physical_proof_join_total":216,
        "unique_member_pair_count":216,"unique_component_edge_count":88,
        "exact_empty_side_promoted_as_physical_proof_count":0,
        "component_relation_disposition_census":relation_census,
        "result_file_sha256":file_hash(result_path),
        "formal_credit":0,"manifest_authorized":False,
        "source_W_transition_authorized":False,
        "global_atom_and_full_twenty_family_totality_closed":False,
    }
    return {**body,"verification_sha256":digest(body)}


def main() -> int:
    parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir",required=True);parser.add_argument("--output",required=True)
    args=parser.parse_args()
    try:
        value=verify(Path(args.candidate_dir).resolve());output=Path(args.output)
        need(not output.exists(),"fresh output");output.write_bytes(encode(value)+b"\n")
    except (Reject,KeyError,TypeError,ValueError,OSError,json.JSONDecodeError) as error:
        print("REJECT:"+str(error));return 2
    print(encode({"status":value["status"],"verification_sha256":value["verification_sha256"]}).decode("ascii"));return 0


if __name__=="__main__": raise SystemExit(main())
