#!/usr/bin/env python3
"""Independent verifier for the C11a R235/R235D local theorem candidate."""

from __future__ import annotations
import argparse, gzip, hashlib, json, os, stat, sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).parent
PREFIX = "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel"
RESULT = PREFIX + "_result.json"
LEDGER = PREFIX + "_ledger.jsonl.gz"
C10_SUPPORT = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C11_ROUTING = "cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz"
PRODUCER_SHA = "2af17cb8f626949dc48824ffb53561f61d3de130438c15c5a20faf5619137485"
MANIFEST = PREFIX + "_manifest.sha256"

class Rejected(RuntimeError): pass
def need(x: bool, label: str) -> None:
    if type(x) is not bool or not x: raise Rejected(label)
def canonical(x: Any) -> bytes: return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def object_sha(x: Any) -> str: return hashlib.sha256(canonical(x)).hexdigest()
def file_sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def row_ref(r: dict[str,Any]) -> dict[str,str]: return {"row_id":r["row_id"],"row_sha256":r["row_sha256"]}
def rows(p: Path) -> Iterator[dict[str,Any]]:
    with gzip.open(p,"rt",encoding="utf-8") as f:
        for i,line in enumerate(f):
            r=json.loads(line); core=dict(r); claimed=core.pop("row_sha256",None)
            need(type(claimed) is str and claimed==object_sha(core),f"row closure:{p.name}:{i}")
            yield r
def validate_ast(n: Any,label: str)->None:
    need(type(n) is dict and type(n.get("op")) is str,"AST node:"+label); op=n["op"]
    if op=="RATIONAL_CONSTANT": need(set(n)=={"op","value"} and type(n["value"]) is str,"AST rational:"+label)
    elif op=="COORDINATE": need(set(n)=={"op","name"} and n["name"] in {"t","p","s"},"AST coordinate:"+label)
    elif op in {"ADD","MUL","AND"}:
        need(set(n)=={"op","args"} and type(n["args"]) is list and bool(n["args"]),"AST nary:"+label)
        for i,c in enumerate(n["args"]): validate_ast(c,label+":"+str(i))
    elif op in {"NEG","SQUARE"}: need(set(n)=={"op","arg"},"AST unary:"+label); validate_ast(n["arg"],label+":arg")
    elif op=="SQRT_PRINCIPAL_NONNEGATIVE": need(set(n)=={"op","radicand"},"AST sqrt:"+label); validate_ast(n["radicand"],label+":radicand")
    elif op in {"EQ","LT","GT"}: need(set(n)=={"op","left","right"},"AST binary:"+label); validate_ast(n["left"],label+":left"); validate_ast(n["right"],label+":right")
    elif op in {"CLOSED_INTERVAL","OPEN_INTERVAL"}: need(set(n)=={"op","coordinate","lower","upper"} and n["coordinate"] in {"t","p","s"},"AST interval:"+label)
    else: raise Rejected("AST op:"+label+":"+op)
def cert_closed(c: dict[str,Any],field: str,label: str)->None:
    core=dict(c); claimed=core.pop(field,None); need(type(claimed) is str and claimed==object_sha(core),label)

def main()->int:
    need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B")
    ap=argparse.ArgumentParser(); ap.add_argument("--candidate-dir"); ap.add_argument("--manifest-first-no-write",action="store_true"); a=ap.parse_args()
    need((a.candidate_dir is None)!=(a.manifest_first_no_write is False),"exactly one verifier mode"); manifest_mode=a.manifest_first_no_write; d=ROOT.resolve() if manifest_mode else Path(a.candidate_dir).resolve()
    if manifest_mode:
        expected={PREFIX+"_producer.py",PREFIX+"_independent_verifier.py",PREFIX+"_attack_harness.py",LEDGER,RESULT,PREFIX+"_verification.json",PREFIX+"_report.md",PREFIX+"_cold_replay.md"}; entries={}
        for line in (ROOT/MANIFEST).read_text(encoding="ascii").splitlines():
            digest,marker,name=line.partition("  ");need(marker=="  " and len(digest)==64 and name not in entries,"manifest syntax");entries[name]=digest
        need(set(entries)==expected,"manifest member exhaustion")
        for name,digest in entries.items():need(file_sha(ROOT/name)==digest,"manifest digest:"+name)
    need(file_sha(ROOT/(PREFIX+"_producer.py"))==PRODUCER_SHA,"producer pin")
    result_path=d/RESULT; raw=result_path.read_bytes(); result=json.loads(raw); core=dict(result); claimed=core.pop("result_sha256",None)
    need(raw==canonical(result) and claimed==object_sha(core),"result closure")
    need(result["producer_source"]["sha256"]==PRODUCER_SHA,"producer result binding")
    need(result["scope_census"]["scoped_kernel_rows"]==9422,"result census")
    need(result["scoped_credit"]=={"local_graph_side_physical_incidence":9422,"one_sided_trace":9422},"result scoped credit")
    need(all(v==0 for v in result["formal_downstream_credit"].values()),"result downstream zero")
    desc=result["kernel_ledger"]; ledger=d/LEDGER; info=os.stat(ledger,follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_size==desc["compressed_size"] and file_sha(ledger)==desc["compressed_sha256"],"ledger file")

    support: dict[str,dict[str,Any]]={}
    for r in rows(ROOT/C10_SUPPORT): support[r["graph_id"]]=r
    need(len(support)==5264,"C10 support exhaustion")
    routing: dict[tuple[str,str,str],dict[str,Any]]={}
    blocked=Counter()
    for r in rows(ROOT/C11_ROUTING):
        if r["graph_class"]=="R242_UNIQUE_GRAPH_FULL_PATCH": continue
        if not r["candidate_ready_routing"]:
            blocked[r["disposition"]]+=1; continue
        key=(r["graph_id"],r["side_role"],r["side_member_id"])
        need(key not in routing,"routing uniqueness")
        need(r["disposition"]=="CANDIDATE_READY_ROUTING" and r["local_graph_side_physical_incidence_proved"] is False and r["one_sided_trace_proved"] is False,"routing pending")
        need(r["DSU_edge_or_union_authorized"] is False and all(v==0 for v in r["formal_credit"].values()),"routing zero")
        routing[key]=r
    need(len(routing)==9422,"routing selected exhaustion")
    need(blocked=={"ADJACENT_DOMAIN_REQUIRED":152,"OUTSIDE_DOMAIN_TRACE_AUTHORITY_REQUIRED":16},"routing blocked exhaustion")

    seen=set(); classes=Counter(); charts=Counter()
    for ordinal,r in enumerate(rows(ledger)):
        need(r["kernel_ordinal"]==ordinal,"kernel order")
        key=(r["graph_id"],r["side_role"],r["side_member_id"])
        need(key in routing and key not in seen,"kernel routing subject"); seen.add(key)
        route=routing[key]; s=support[r["graph_id"]]
        need(r["C11_routing_disposition_ref"]==row_ref(route),"C11 routing ref")
        need(r["C10_exact_graph_support_ref"]==row_ref(s),"C10 support ref")
        need(r["sheet_member_id"]==s["sheet_member_id"] and r["graph_class"]==s["graph_class"],"support subject")
        validate_ast(r["exact_side_stratum_ast"],r["row_id"])
        need(r["exact_side_stratum_ast_sha256"]==object_sha(r["exact_side_stratum_ast"]),"side AST digest")
        need(r["exact_graph_boundary_ast_sha256"]==s["ast_sha256"]["exact_support_ast_sha256"],"graph boundary digest")
        eq=r["partition_branch_to_side_member_equivalence_certificate"]; cert_closed(eq,"certificate_sha256","branch certificate closure")
        need(eq["side_member_exact_support_equivalence_proved"] is True and eq["R248_null_positive_box_used_as_support_geometry"] is False,"branch theorem")
        need(eq["R248_recomputed_side_member_id"]==r["side_member_id"] and eq["exact_side_stratum_ast_sha256"]==r["exact_side_stratum_ast_sha256"],"branch subject")
        closure=r["closure_incidence_certificate"]; cert_closed(closure,"certificate_sha256","closure certificate closure")
        need(closure["closure_incidence_complete"] is True and closure["strict_side_and_graph_are_disjoint"] is True and closure["graph_subset_of_relative_side_closure_by_trace_atlas"] is True,"closure theorem")
        need(closure["exact_graph_support_ast_sha256"]==r["exact_graph_boundary_ast_sha256"] and closure["exact_side_stratum_ast_sha256"]==r["exact_side_stratum_ast_sha256"],"closure subject")
        trace=r["one_sided_trace_certificate"]
        need(trace["every_graph_point_has_a_side_approach_path"] is True and trace["coverage_rule"]["all_exact_graph_points_covered"] is True,"trace coverage")
        need(type(trace["charts"]) is list and bool(trace["charts"]),"trace charts")
        for chart in trace["charts"]:
            cert_closed(chart,"chart_sha256","chart closure")
            need(chart["path_rule"]=="AXIS_RAY_FROM_GRAPH_POINT_V1" and chart["limit_at_lambda_down_to_zero"]=="EXACT_GRAPH_BASE_POINT","chart path")
            need(chart["local_strict_sign_conclusion"] in {"LT_ZERO","GT_ZERO"},"chart sign")
        need(r["scoped_credit"]=={"local_graph_side_physical_incidence":1,"one_sided_trace":1},"row scoped credit")
        np=r["strict_nonpromotion"]
        need(np["graph_sheet_set_equality_proved"] is False and np["representation_pullback_proved"] is False and np["DSU_edge_or_union_authorized"] is False,"row nonpromotion")
        need(all(v==0 for k,v in np.items() if type(v) is int),"row downstream zero")
        classes[(r["graph_class"],r["side_role"])]+=1; charts[r["graph_class"]]+=len(trace["charts"])
    need(seen==set(routing),"kernel routing exhaustion")
    need(classes=={("R235_TARGET_POSITIVE_PARTIAL_BASE","EVENT_ABSENT"):4432,("R235_TARGET_POSITIVE_PARTIAL_BASE","EVENT_PRESENT"):4432,("R235_SOURCE_EXACT_FACE_FULL_BASE","EVENT_ABSENT"):336,("R235_SOURCE_EXACT_FACE_FULL_BASE","EVENT_PRESENT"):216,("R235D_SOURCE_EXACT_FACE_FULL_BASE","source:SAME_SIGN_EVENT_ABSENT"):6},"class role census")
    need(charts=={"R235_TARGET_POSITIVE_PARTIAL_BASE":25648,"R235_SOURCE_EXACT_FACE_FULL_BASE":552,"R235D_SOURCE_EXACT_FACE_FULL_BASE":6},"trace chart census")
    status="PASS_MANIFEST_FIRST_NO_WRITE_C11A_9422_RELATIONS" if manifest_mode else "PASS_INDEPENDENT_C11A_9422_RELATIONS"
    print(json.dumps({"status":status,"result_sha256":claimed},sort_keys=True,separators=(",",":")))
    return 0
if __name__=="__main__": raise SystemExit(main())
