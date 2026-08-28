#!/usr/bin/env python3
"""Independent verifier for C12 local-shared relation rerouting."""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat,sys
from pathlib import Path
from typing import Any,Iterator
ROOT=Path(__file__).parent;PREFIX="cm2_round306c12_source_g_local_shared_relation_reroute";LEDGER=PREFIX+"_ledger.jsonl.gz";RESULT=PREFIX+"_result.json";PRODUCER_SHA="97e80bd52732a08ab1c0e5841485a97fa4074a3fc191f6892265eb2aa7e904c5"
MANIFEST=PREFIX+"_manifest.sha256"
FINDINGS="cm2_round306c11_source_g_graph_side_local_theorem_disposition_missing_local_shared_reroute_findings.jsonl.gz";SUPPORT="cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz";IDENTITY="cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_member_identity_disposition_ledger.jsonl.gz";BRIDGES="cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz";C7="cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_physical_incidence_statement_ledger.jsonl.gz"
UPSTREAM={FINDINGS:"3e257ca914aeb2306eab4064a118d5f1e28a753a215e694b137233a3b066f5c8",SUPPORT:"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",IDENTITY:"5041df1ab4b5bf9e79984859f828c9fb69718f53bd62d2920d51ebea8b7ec9df",BRIDGES:"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db",C7:"e6450435f74f038f3de2ada64935fc1f72bec6eb4323f2dc5ad8069bf3ea490e"}
class Rejected(RuntimeError):pass
def need(x:bool,l:str)->None:
 if type(x) is not bool or not x:raise Rejected(l)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def fsha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def rows(p:Path)->Iterator[dict[str,Any]]:
 with gzip.open(p,"rt",encoding="utf-8") as f:
  for i,l in enumerate(f):
   r=json.loads(l);c=dict(r);need(c.pop("row_sha256",None)==obj(c),f"row closure:{p.name}:{i}");yield r
def ref(r:dict[str,Any],id_field:str="row_id")->dict[str,str]:return {"row_id":r[id_field],"row_sha256":r["row_sha256"]}
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir");ap.add_argument("--manifest-first-no-write",action="store_true");a=ap.parse_args();need((a.candidate_dir is None)!=(a.manifest_first_no_write is False),"one mode");manifest_mode=a.manifest_first_no_write;d=ROOT.resolve() if manifest_mode else Path(a.candidate_dir).resolve();need(fsha(ROOT/(PREFIX+"_producer.py"))==PRODUCER_SHA,"producer pin")
 if manifest_mode:
  expected={PREFIX+"_producer.py",PREFIX+"_independent_verifier.py",PREFIX+"_attack_harness.py",LEDGER,RESULT,PREFIX+"_verification.json",PREFIX+"_report.md",PREFIX+"_cold_replay.md"};entries={}
  for line in (ROOT/MANIFEST).read_text(encoding="ascii").splitlines():digest,mark,name=line.partition("  ");need(mark=="  " and len(digest)==64 and name not in entries,"manifest syntax");entries[name]=digest
  need(set(entries)==expected,"manifest exhaustion")
  for name,digest in entries.items():need(fsha(ROOT/name)==digest,"manifest digest:"+name)
 for n,s in UPSTREAM.items():need(fsha(ROOT/n)==s,"upstream pin:"+n)
 raw=(d/RESULT).read_bytes();result=json.loads(raw);core=dict(result);claimed=core.pop("result_sha256",None);need(raw==canonical(result) and claimed==obj(core),"result closure");need(result["producer_source"]["sha256"]==PRODUCER_SHA,"producer binding");need(result["census"]=={"C11_findings":10,"rerouted_relations":10,"distinct_positive_source_graphs":10,"distinct_surviving_shared_side_members":10},"result census");need(result["scoped_credit"]=={"relation_reroute_disposition":10} and all(v==0 for v in result["formal_credit"].values()),"result credit")
 desc=result["reroute_ledger"];p=d/LEDGER;info=os.stat(p,follow_symlinks=False);need(stat.S_ISREG(info.st_mode) and info.st_size==desc["compressed_size"] and fsha(p)==desc["compressed_sha256"],"ledger descriptor")
 candidate_rows=list(rows(p));need(len(candidate_rows)==10,"candidate row census")
 for i,r in enumerate(candidate_rows):
  need(r["reroute_ordinal"]==i and r["relation_reroute_disposition_credit"]==1,"preflight order/credit");need(r["side_role"]=="source:SAME_SIGN_EVENT_ABSENT" and r["component_relation"]=="SAME_BASE_ROOT","preflight subject");need(r["reroute_disposition"]=="REROUTED_EMPTY_TARGET_SHARED_SIDE_TO_POSITIVE_SOURCE_GRAPH" and r["local_graph_side_physical_incidence_proved"] is False and r["one_sided_trace_proved"] is False and r["representation_pullback_proved"] is False and r["DSU_edge_or_union_authorized"] is False and all(v==0 for v in r["formal_credit"].values()),"preflight boundary")
 findings={r["row_id"]:r for r in rows(ROOT/FINDINGS)};supports={r["graph_id"]:r for r in rows(ROOT/SUPPORT)};identities={r["graph_id"]:r for r in rows(ROOT/IDENTITY)};bridges={r["bridge_row_id"]:r for r in rows(ROOT/BRIDGES)};wanted={r["C7_surviving_target_shared_relation_ref"]["row_id"] for r in findings.values()};c7={r["row_id"]:r for r in rows(ROOT/C7) if r["row_id"] in wanted};need(len(findings)==len(c7)==10 and len(supports)==len(identities)==5264 and len(bridges)==16,"upstream exhaustion")
 seen_g=set();seen_s=set();seen_f=set()
 for i,r in enumerate(candidate_rows):
  need(r["reroute_ordinal"]==i and r["relation_reroute_disposition_credit"]==1,"row order/credit");f=findings[r["C11_finding_ref"]["row_id"]];g=r["positive_source_graph_id"];s=r["side_member_id"];sup=supports[g];ident=identities[g];bridge=bridges[r["C4_bridge_ref"]["row_id"]];old=c7[r["retired_empty_target_relation_ref"]["row_id"]]
  need(r["C11_finding_ref"]==ref(f) and r["C4_bridge_ref"]==ref(bridge,"bridge_row_id") and r["C10_positive_source_support_ref"]==ref(sup) and r["C10_positive_source_identity_ref"]==ref(ident) and r["retired_empty_target_relation_ref"]==ref(old),"direct refs")
  need(g==f["positive_source_graph_id"] and s==f["surviving_shared_side_member_id"] and r["retired_empty_target_graph_id"]==f["empty_target_graph_id"],"finding subjects");need(r["sheet_member_id"]==sup["sheet_member_id"] and r["side_role"]=="source:SAME_SIGN_EVENT_ABSENT","new relation subject")
  need(old["graph_id"]==f["empty_target_graph_id"] and old["member_id"]==s and old["empty_graph_disposition_credit"]==1 and old["incidence_statement_ast"]["side_role"]=="target:SAME_SIGN_EVENT_ABSENT","retired relation")
  need(bridge["canonical_input_commitment"]["B1G0_source_shared_side_row"][1]==r["source_incidence_row_commitment"]["row_id"] and bridge["semantic_reconstruction"]["source_zero_set"]=="EXACT_FACE_GRAPH_t_EQUALS_0","source authority")
  need(r["component_relation"]=="SAME_BASE_ROOT" and f["shared_side_component_ref"]["fresh_component_id"]==f["source_graph_sheet_component_ref"]["fresh_component_id"],"component binding")
  need(r["reroute_disposition"]=="REROUTED_EMPTY_TARGET_SHARED_SIDE_TO_POSITIVE_SOURCE_GRAPH" and r["local_graph_side_physical_incidence_proved"] is False and r["one_sided_trace_proved"] is False and r["representation_pullback_proved"] is False and r["DSU_edge_or_union_authorized"] is False and all(v==0 for v in r["formal_credit"].values()),"row boundary")
  need(g not in seen_g and s not in seen_s and f["row_id"] not in seen_f,"uniqueness");seen_g.add(g);seen_s.add(s);seen_f.add(f["row_id"])
 need(len(seen_g)==len(seen_s)==len(seen_f)==10,"output exhaustion");status="PASS_MANIFEST_FIRST_NO_WRITE_C12_10_REROUTES_ZERO_THEOREM_CREDIT" if manifest_mode else "PASS_INDEPENDENT_C12_10_REROUTES_ZERO_THEOREM_CREDIT";print(json.dumps({"status":status,"result_sha256":claimed},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
