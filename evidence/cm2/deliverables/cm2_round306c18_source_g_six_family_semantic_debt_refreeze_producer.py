#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parent;P="cm2_round306c18_source_g_six_family_semantic_debt_refreeze";LEDGER=P+"_ledger.jsonl.gz";RESULT=P+"_result.json"
S={"MEMBER":("cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz","0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a"),"REP":("cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz","47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"),"PULLBACK":("cm2_round306c17_source_g_15224_representation_pullback_kernel_ledger.jsonl.gz","2d7a86fe0518ca2a003f1e70b3de56aa5eb80d7b1a176eb788333fc6ad75199c"),"NEG":("cm2_round306c16b_source_g_relation_theorem_component_replay_negative_disposition_ledger.jsonl.gz","6d1b80a4bca95bc7d0b3730b4970214705b6d8ff15aea385c7db6f29059f9edc"),"AUTH":("cm2_round306c8_source_g_fresh_full_support_authority_frontier.json","1ec052ba9a6c26929d3a8242f3d12f405640f6399c331977acf51a315e201792")}
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def osh(v):return hashlib.sha256(c(v)).hexdigest()
def fsha(q):
 h=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==osh(b),"closure");yield r
def classify(r):
 f=r["coarse_family"];p=r["member_id"].split(":",1)[0]
 if f=="PRESERVED":return "PRESERVED_DIRECT_GEOMETRY"
 if f=="R2":return "R2_SOURCE_FREE_INTERVAL_AND_REGLUE"
 if f=="R292":return "R292_FIXED_SIGN_SIGMA_AND_FACE"
 if f=="G2A":return "G2A_PULLBACK_CLOSED_SUPPORT_PENDING"
 if f=="G2B":return "G2B_RELATION_PARTITION_PENDING"
 if r["C14c_family_disposition_ref"] is not None:return "NON_GRAPH_RETAINED_OUTER_ENVELOPE"
 if p=="round248-wall-bulk" and r["identity_replay_source"]["kind"]=="C7_REPLAY":return "NON_GRAPH_WALL_BULK"
 return "NON_GRAPH_LEGACY_DIRECT"
LABELS={"PRESERVED_DIRECT_GEOMETRY":["DIRECT_SOURCE_GEOMETRY_FULL_SUPPORT_EQUALITY_NOT_PROVED","REPRESENTATION_COVER_NOT_PROVED","A1_A2_NOT_DISCHARGED"],"NON_GRAPH_LEGACY_DIRECT":["NON_GRAPH_FULL_SUPPORT_CONSTRUCTION_SEMANTICS_NOT_PROVED","REPRESENTATION_COVER_NOT_PROVED","A1_A2_NOT_DISCHARGED"],"NON_GRAPH_WALL_BULK":["EMPTY_GRAPH_OR_WALL_BULK_NON_GRAPH_SUPPORT_AST_NOT_MATERIALIZED","REPRESENTATION_COVER_NOT_PROVED","A1_A2_NOT_DISCHARGED"],"NON_GRAPH_RETAINED_OUTER_ENVELOPE":["OUTER_ENVELOPE_IS_NOT_EXACT_NON_GRAPH_SUPPORT","REPRESENTATION_COVER_NOT_PROVED","A1_A2_NOT_DISCHARGED"],"R2_SOURCE_FREE_INTERVAL_AND_REGLUE":["SOURCE_FREE_INTERVAL_PREDICATE_EQUIVALENCE_NOT_PROVED","W_TAIL_ARTIFICIAL_FACE_REGLUE_NOT_CREDITED","A1_A2_NOT_DISCHARGED"],"R292_FIXED_SIGN_SIGMA_AND_FACE":["FIXED_SIGN_PULLBACK_EQUIVALENCE_NOT_PROVED","SIGMA_BRANCH_AUTHORITY_NOT_PROVED","REFINED_PHYSICAL_FACE_KRUSKAL_SEMANTICS_NOT_PROVED"],"G2A_PULLBACK_CLOSED_SUPPORT_PENDING":["GRAPH_DEFINITION_AND_PULLBACK_CLOSED","MEMBER_TYPED_NORMALIZED_SUPPORT_NOT_ISSUED"],"G2B_RELATION_BACKED_PULLBACK_CLOSED":["PHYSICAL_INCIDENCE_TRACE_AND_PULLBACK_CLOSED","MEMBER_TYPED_NORMALIZED_SUPPORT_NOT_ISSUED"],"G2B_NEGATIVE_NONINCIDENCE_SIDE":["NEGATIVE_NONINCIDENCE_DISPOSITION_CLOSED","STANDALONE_SIDE_NORMALIZED_SUPPORT_NOT_ISSUED"]}
def build(q):
 for n,h in S.values():need(fsha(ROOT/n)==h,"pin:"+n)
 auth=json.loads((ROOT/S["AUTH"][0]).read_bytes());need(auth["formal_credit"]["normalized_support"]==0,"authority boundary")
 members={};mc=Counter()
 for r in rows(ROOT/S["MEMBER"][0]):members[r["member_id"]]=classify(r);mc[classify(r)]+=1
 need(len(members)==502204,"members")
 covered=set();pc=Counter()
 for r in rows(ROOT/S["PULLBACK"][0]):covered.add(r["endpoint_member_id"]);pc[(r["endpoint_family"],r["relation_kind"])]+=1
 need(pc=={("G2A","GRAPH_TO_SHEET"):5264,("G2B","GRAPH_TO_SIDE"):9960},"pullback census")
 neg=set(r["endpoint_member_id"] for r in rows(ROOT/S["NEG"][0]));need(len(neg)==168,"negative census")
 rc=Counter()
 for r in rows(ROOT/S["REP"][0]):
  owner=r["owner_member_id"];cat=members[owner]
  if cat=="G2B_RELATION_PARTITION_PENDING":cat="G2B_RELATION_BACKED_PULLBACK_CLOSED" if owner in covered else "G2B_NEGATIVE_NONINCIDENCE_SIDE"
  rc[cat]+=1
 expected={"PRESERVED_DIRECT_GEOMETRY":(126468,165744),"NON_GRAPH_LEGACY_DIRECT":(5596,5596),"NON_GRAPH_WALL_BULK":(45576,45576),"NON_GRAPH_RETAINED_OUTER_ENVELOPE":(4432,4432),"R2_SOURCE_FREE_INTERVAL_AND_REGLUE":(295336,302624),"R292_FIXED_SIGN_SIGMA_AND_FACE":(9404,10252),"G2A_PULLBACK_CLOSED_SUPPORT_PENDING":(5264,5264),"G2B_RELATION_BACKED_PULLBACK_CLOSED":(9960,9960),"G2B_NEGATIVE_NONINCIDENCE_SIDE":(168,168)}
 out=[]
 for i,(cat,(m,rp)) in enumerate(expected.items()):
  actual_m=mc[cat] if not cat.startswith("G2B_") else (9960 if cat.endswith("CLOSED") else 168);need((actual_m,rc[cat])==(m,rp),"category:"+cat);b={"schema":"cm2.round306c18.source-g-six-family-semantic-debt-refreeze.v1.row.v1","ordinal":i,"category":cat,"member_count":m,"representation_count":rp,"semantic_obligation_labels":LABELS[cat],"formal_credit":{"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":0},"status":"EXACT_DEBT_FRONTIER_ONLY"};out.append({**b,"row_sha256":osh(b)})
 raw=b"".join(c(r)+b"\n" for r in out);q.mkdir(parents=True,exist_ok=True)
 with (q/LEDGER).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":LEDGER,"row_count":9,"size":(q/LEDGER).stat().st_size,"sha256":fsha(q/LEDGER),"sequence_sha256":hashlib.sha256(b"".join(bytes.fromhex(r["row_sha256"]) for r in out)).hexdigest()};b={"schema":"cm2.round306c18.source-g-six-family-semantic-debt-refreeze.v1","status":"PASS_EXACT_502204_MEMBER_549616_REPRESENTATION_SEMANTIC_DEBT_FRONTIER__ZERO_SUPPORT_CREDIT","member_count":502204,"representation_count":549616,"category_count":9,"ledger":d,"pullback_closed_endpoint_count":15224,"negative_nonincidence_endpoint_count":168,"strict_nonpromotion":{"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"PROVE_CATEGORY_KERNELS_AND_ISSUE_502204_MEMBER_TYPED_NORMALIZED_SUPPORT"};result={**b,"result_sha256":osh(b)};(q/RESULT).write_bytes(c(result));return result
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();r=build(Path(a.candidate_dir).resolve());print(c({"status":r["status"],"result_sha256":r["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
