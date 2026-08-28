#!/usr/bin/env python3
"""Aggregate all 16 frozen C61s12 shards and reconstruct global Kraft state."""

from __future__ import annotations

import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any


SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
OUT = SELF.parent
BASE = "cm2_round306c61s12_depth12_16shard"
SCHEMA = "cm2.round306c61s12.depth12-16shard.v1"
SHARDS = tuple(range(16))
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

CONTRACT = OUT / "cm2_round306c61s12_independent_contract_v1.json"
ASSIGNMENT_RESULT = OUT / (BASE + "_assignment_result_v1.json")
ASSIGNMENT = OUT / (BASE + "_assignment_inventory_v1.jsonl.gz")
C58_BASE = "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement"
C58_RESULT = OUT / (C58_BASE + "_result_v1.json")
C58_LEAVES = OUT / (C58_BASE + "_leaf_ledger_v1.jsonl.gz")
C58_MANIFEST = OUT / (C58_BASE + "_manifest_v1.sha256")
C57_BASE = "cm2_round306c57s1_singleton_collision1_common_refinement"
C57_RESULT = OUT / (C57_BASE + "_result_v1.json")
C57_LEAVES = OUT / (C57_BASE + "_leaf_ledger_v1.jsonl.gz")
C57_MANIFEST = OUT / (C57_BASE + "_manifest_v1.sha256")

# The v1 aggregate stage failed closed before producing a result because its
# parent replay omitted the 462 C57 carried terminals.  Those incomplete stage
# ledgers are deliberately not reused or manifested.  The corrected aggregate
# writes fresh no-replace targets.  The v2 parent census then failed closed in
# independent audit because its generic `disposition` accessor misclassified
# all 462 C57 rows (whose field is `leaf_disposition`).  The final aggregate is
# therefore a fresh transaction with explicit schema-specific accessors.  The
# v3 stage then failed closed before result publication because a local helper
# name shadowed the aggregate disposition-census variable during serialization.
# v4 is the fresh no-replace terminal transaction.
LEAF_FILE = BASE + "_aggregate_leaf_ledger_v4.jsonl.gz"
SOURCE_FILE = BASE + "_aggregate_source_summary_v4.jsonl.gz"
PARENT_FILE = BASE + "_aggregate_parent_summary_v4.jsonl.gz"
RESULT_FILE = BASE + "_aggregate_result_v4.json"

PIN = {
    "contract_file": "7f7efeb0a060fea143c9f6a00b4722f2cc87632bff631feb598c434ca969a418",
    "contract_object": "68c6e8a0899c66056724ea29c42949100b2fc6a625865867fd30aacc16d36f7d",
    "assignment_file": "7d6fae044bd194c790dfc5dba077481d47e3e6850455463bfd61c8832e29ca69",
    "assignment_object": "d1f9549826fa424bd2c29fc217e714527c2e56ac25361e48f31d95aa33536d19",
    "inventory_file": "6ad0fe4d52c468de31fb39f72eabd825320eee86b9738f52fb1142da8a1736b4",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C58_manifest_file": "4cde1af23dbdbcfe4859e971ec698b553664ddaf79c4756e9fd64e59027edc12",
    "C57_result_file": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "C57_result_object": "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58",
    "C57_leaf_file": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "C57_manifest_file": "4427e1376811454ad3b6ec5478c1687064cea81f5d33ebd0c13284952928ced0",
}


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if not value: raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""): h.update(block)
    return h.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    need(type(value) is dict, "JSON object")
    return value


def closed_json(path: Path, file_pin: str | None = None, object_pin: str | None = None) -> dict[str, Any]:
    if file_pin: need(file_sha(path) == file_pin, "file pin:" + path.name)
    value = strict_json(path); body = copy.deepcopy(value); claim = body.pop("object_sha256", None)
    need(type(claim) is str and digest(body) == claim, "object closure:" + path.name)
    if object_pin: need(claim == object_pin, "object pin:" + path.name)
    return value


def rows(path: Path, descriptor: dict[str, Any], pin: str | None = None) -> list[dict[str, Any]]:
    if pin: need(file_sha(path) == pin, "ledger pin:" + path.name)
    need(file_sha(path) == descriptor["sha256"], "descriptor pin:" + path.name)
    answer = []; sequence = hashlib.sha256()
    with gzip.open(path, "rt") as stream:
        for line in stream:
            row = json.loads(line); body = copy.deepcopy(row); claim = body.pop("row_sha256", None)
            need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
            sequence.update((claim + "\n").encode()); answer.append(row)
    need(len(answer) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], "ledger descriptor")
    return answer


class Writer:
    def __init__(self, path: Path, order: str):
        self.path, self.order, self.count = path, order, 0; self.sequence = hashlib.sha256()
    def __enter__(self):
        need(not self.path.exists(), "no replace:" + self.path.name)
        self.raw = self.path.open("xb"); self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0); return self
    def write(self, row):
        claim = digest(row); closed = {**row, "row_sha256": claim}; self.stream.write(canonical(closed)+b"\n")
        self.sequence.update((claim+"\n").encode()); self.count += 1; return closed
    def __exit__(self,*_): self.stream.close(); self.raw.close()
    def descriptor(self): return {"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.sequence.hexdigest(),"sha256":file_sha(self.path),"size":self.path.stat().st_size}


def prefix_free(paths: list[str]) -> bool:
    ordered=sorted(paths,key=lambda x:(len(x),x)); return all(not b.startswith(a) for i,a in enumerate(ordered) for b in ordered[i+1:])


def main() -> int:
    contract=closed_json(CONTRACT,PIN["contract_file"],PIN["contract_object"])
    assignment_result=closed_json(ASSIGNMENT_RESULT,PIN["assignment_file"],PIN["assignment_object"])
    inventory=rows(ASSIGNMENT,assignment_result["inventory"],PIN["inventory_file"])
    need(len(inventory)==2599 and contract["shard_count"]==16,"assignment inputs")
    inventory_by_hash={r["C58_leaf_row_sha256"]:r for r in inventory}; need(len(inventory_by_hash)==2599,"inventory unique")
    all_outputs=[]; receipts=[]; union=set(); route_count=0; disposition={"STRICT_TERMINAL":0,"COLLISION3_READY":0,"COLLISION2_HANDOFF":0}; raw={}
    for shard in SHARDS:
        receipt_path=OUT/(BASE+f"_shard_{shard:02d}_receipt_v1.json")
        receipt=closed_json(receipt_path); receipts.append(receipt)
        need(receipt["shard_id"]==shard and receipt["status"]=="PASS_COMPLETE_NO_REPLACE_SHARD" and receipt["shard_complete"] is True,"receipt")
        need(receipt["assignment_contract_object_sha256"]==PIN["contract_object"] and receipt["assignment_result_object_sha256"]==PIN["assignment_object"],"receipt pins")
        ledger_path=OUT/receipt["output_ledger"]["filename"]
        output=rows(ledger_path,receipt["output_ledger"])
        assigned={r["C58_leaf_row_sha256"] for r in inventory if r["shard_id"]==shard}
        actual={r["source_C58_leaf_row_sha256"] for r in output}
        need(actual==assigned and not (union&actual),"shard coverage/exclusion")
        union|=actual; all_outputs.extend(output); route_count+=receipt["route_evaluation_count"]
        for k,v in receipt["output_disposition_census"].items(): disposition[k]+=v
        for k,v in receipt["raw_classification_census"].items(): raw[k]=raw.get(k,0)+v
    need(union==set(inventory_by_hash) and len(receipts)==16,"global assignment union")

    # Verify each C58 source partition.
    by_source={}
    for r in all_outputs: by_source.setdefault(r["source_C58_leaf_row_sha256"],[]).append(r)
    source_writer=Writer(OUT/SOURCE_FILE,"SOURCE_HANDOFF_ORDINAL_THEN_PATH")
    whole_terminal=whole_c3=0
    with source_writer:
        for source_hash, output in sorted(by_source.items(),key=lambda kv:(inventory_by_hash[kv[0]]["source_handoff_ordinal"],inventory_by_hash[kv[0]]["path"])):
            source=inventory_by_hash[source_hash]; paths=[r["path"] for r in output]; kraft=sum(Fraction(r["parent_volume_fraction"]) for r in output)
            need(prefix_free(paths) and kraft==Fraction(source["parent_volume_fraction"]),"source Kraft")
            t=sum(r["disposition"]=="STRICT_TERMINAL" for r in output); c3=sum(r["disposition"]=="COLLISION3_READY" for r in output); c2=len(output)-t-c3
            whole_terminal+=int(t==len(output)); whole_c3+=int(c2==0)
            source_writer.write({"schema":SCHEMA+".aggregate-source-row","source_handoff_ordinal":source["source_handoff_ordinal"],"source_C58_leaf_row_sha256":source_hash,"source_path":source["path"],"pair_index":source["pair_index"],"output_leaf_count":len(output),"strict_terminal_leaf_count":t,"collision3_ready_leaf_count":c3,"collision2_handoff_leaf_count":c2,"path_prefix_free":True,"Kraft_conservation":source["parent_volume_fraction"],"whole_source_terminal":t==len(output),"whole_source_terminal_or_C3_ready":c2==0,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0})

    # Freeze aggregate leaf order.
    leaf_writer=Writer(OUT/LEAF_FILE,"SOURCE_HANDOFF_ORDINAL_THEN_PATH")
    with leaf_writer:
        for r in sorted(all_outputs,key=lambda x:(x["source_handoff_ordinal"],x["source_path"],x["path"])):
            body=copy.deepcopy(r); body.pop("row_sha256"); leaf_writer.write({"schema":SCHEMA+".aggregate-leaf-row","source_shard_row_sha256":r["row_sha256"],**{k:v for k,v in body.items() if k!="schema"}})

    # Combine the 462 C57 carried terminals, the 2,949 C58 terminals, and
    # every C61 output to derive the complete 12-parent partitions.
    c58_result=closed_json(C58_RESULT,PIN["C58_result_file"],PIN["C58_result_object"]); need(file_sha(C58_MANIFEST)==PIN["C58_manifest_file"],"C58 manifest")
    c58=rows(C58_LEAVES,c58_result["ledgers"]["leaves"],PIN["C58_leaf_file"])
    c57_result=closed_json(C57_RESULT,PIN["C57_result_file"],PIN["C57_result_object"]); need(file_sha(C57_MANIFEST)==PIN["C57_manifest_file"],"C57 manifest")
    c57=rows(C57_LEAVES,c57_result["ledgers"]["leaves"],PIN["C57_leaf_file"])
    carried_c57=[r for r in c57 if r["leaf_disposition"]=="STRICT_TERMINAL"]
    carried_c58=[r for r in c58 if r["disposition"]=="STRICT_TERMINAL"]
    need(len(carried_c57)==462 and len(carried_c58)==2949,"carried terminal census")
    parent_rows={pair:[] for pair in PAIRS}
    for r in carried_c57: parent_rows[r["pair_index"]].append(r)
    for r in carried_c58: parent_rows[r["pair_index"]].append(r)
    for r in all_outputs: parent_rows[r["pair_index"]].append(r)
    parent_writer=Writer(OUT/PARENT_FILE,"PAIR_INDEX_ASCENDING"); whole_pairs=0
    with parent_writer:
        for pair,values in parent_rows.items():
            paths=[r["path"] for r in values]; kraft=sum(Fraction(r["parent_volume_fraction"]) for r in values); need(prefix_free(paths) and kraft==1,"parent Kraft")
            def row_disposition(value: dict[str, Any]) -> str:
                schema = value.get("schema")
                if schema == "cm2.round306c57s1.singleton-collision1-common-refinement.v1.leaf-row":
                    need("leaf_disposition" in value and "disposition" not in value,
                         "C57 schema-specific disposition accessor")
                    return value["leaf_disposition"]
                if schema in {
                    "cm2.round306c58s2.singleton-collision2-handoff-depth6-refinement.v1.leaf-row",
                    SCHEMA + ".shard-leaf-row",
                }:
                    need("disposition" in value and "leaf_disposition" not in value,
                         "C58/C61 schema-specific disposition accessor")
                    return value["disposition"]
                raise Reject("unknown parent-row source schema:" + str(schema))
            dispositions=[row_disposition(r) for r in values]
            t=sum(item=="STRICT_TERMINAL" for item in dispositions); c3=sum(item=="COLLISION3_READY" for item in dispositions); c2=sum(item=="COLLISION2_HANDOFF" for item in dispositions)
            need(t+c3+c2==len(values),"parent disposition exhaustiveness")
            whole=c2==c3==0; whole_pairs+=int(whole)
            parent_writer.write({"schema":SCHEMA+".aggregate-parent-row","pair_index":pair,"combined_leaf_count":len(values),"strict_terminal_leaf_count":t,"collision3_ready_leaf_count":c3,"collision2_handoff_leaf_count":c2,"path_prefix_free":True,"parent_Kraft_conservation":"1","whole_pair_terminal":whole,"whole_pair_credit":0,"D02_gate_credit":0})

    result={"schema":SCHEMA+".aggregate-result.v4","status":"PASS_COMPLETE_16_SHARD_DEPTH12_AGGREGATE_V4__SCHEMA_SPECIFIC_PARENT_CENSUS__ZERO_FORMAL_CREDIT","frozen_inputs":{"contract_object_sha256":PIN["contract_object"],"assignment_object_sha256":PIN["assignment_object"],"C58_result_object_sha256":PIN["C58_result_object"],"C57_result_object_sha256":PIN["C57_result_object"]},"coverage":{"input_C58_residuals":2599,"shard_receipts":16,"assignment_complete":True,"assignment_mutually_exclusive":True,"route_evaluations":route_count,"output_leaf_count":len(all_outputs),"disposition_census":disposition,"whole_input_handoffs_terminal":whole_terminal,"whole_input_handoffs_terminal_or_C3_ready":whole_c3,"carried_C57_terminal_leaves":len(carried_c57),"carried_C58_terminal_leaves":len(carried_c58),"raw_classification_census":dict(sorted(raw.items()))},"ledgers":{"aggregate_leaves":leaf_writer.descriptor(),"source_summaries":source_writer.descriptor(),"parent_summaries":parent_writer.descriptor()},"invariants":{"all_2599_source_partitions_prefix_free_and_Kraft_conserved":True,"all_12_combined_parents_prefix_free_and_Kraft_one":True,"all_16_receipts_complete":True,"C57_C58_C61_parent_carry_complete":True,"schema_specific_disposition_accessors_used":True,"incomplete_v1_stage_ledgers_reused":False,"rejected_v2_stage_ledgers_reused":False,"rejected_v3_stage_ledgers_reused":False,"partial_statistics_used_for_credit":False},"whole_pairs_closed":whole_pairs,"whole_singletons_closed":whole_pairs*2,"whole_singletons_remaining":24-whole_pairs*2,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0,"runtime_canonical_pointer_or_seal_writes":False}
    # Complete serialization/object-closure dry-run before publishing the
    # final result path.  This catches type/name collisions before any result
    # byte is created.
    result["object_sha256"]=digest(result)
    serialized=canonical(result)+b"\n"
    replay=json.loads(serialized)
    replay_body=copy.deepcopy(replay); replay_claim=replay_body.pop("object_sha256",None)
    need(replay_claim==result["object_sha256"] and digest(replay_body)==replay_claim,
         "final result serialization/object closure dry-run")
    path=OUT/RESULT_FILE; need(not path.exists(),"result no replace"); path.write_bytes(serialized)
    print(json.dumps({"status":result["status"],"object_sha256":result["object_sha256"],"coverage":result["coverage"]},sort_keys=True,separators=(",",":"))); return 0


if __name__=="__main__":
    try: raise SystemExit(main())
    except (Reject,KeyError,ValueError) as e: print(json.dumps({"status":"FAIL_CLOSED","reason":str(e)},sort_keys=True,separators=(",",":"))); raise SystemExit(1)
