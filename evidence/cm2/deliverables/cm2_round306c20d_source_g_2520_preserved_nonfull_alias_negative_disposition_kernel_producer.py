#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";I2="cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz";R294="cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz";R295="cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={C20:"bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",I2:"68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83",R294:"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",R295:"5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"};TPS="EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER";T2="EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL";ADJ="ADJACENT_POSITIVE_T_CONTINUATION";EXPECTED={TPS:720,T2:1524,ADJ:276}
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def h(v):return hashlib.sha256(c(v)).hexdigest()
def fh(q):
 x=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):x.update(b)
 return x.hexdigest()
def rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   raw=line[:-1];r=json.loads(raw);need(line.endswith(b"\n") and c(r)==raw,"canonical");b=dict(r);need(b.pop("row_sha256",None)==h(b),"closure");yield r
def volume(box):return (Fraction(box[1])-Fraction(box[0]))*(Fraction(box[3])-Fraction(box[2]))*(Fraction(box[5])-Fraction(box[4]))
def strict_subset(box,outer):return all(Fraction(outer[2*i])<=Fraction(box[2*i])<Fraction(box[2*i+1])<=Fraction(outer[2*i+1]) for i in range(3)) and box!=outer
def transformed(box):
 a,b=Fraction(box[0]),Fraction(box[1]);need(a*b>0,"fixed sign");lo,hi=sorted((a*a,b*b));return [str(lo),str(hi),*box[2:]]
def build(q):
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 owner={r["member_id"]:r for r in rows(ROOT/C20)};i2={r["source_row_id"]:r for r in rows(ROOT/I2) if r.get("representation_semantics") in EXPECTED};source={};counts=Counter()
 with gzip.open(ROOT/R294,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  kind=s["support_representation_kind"]
  if kind not in {TPS,T2}:continue
  x=i2.get(s["Round294_occurrence_representation_binding_row_id"])
  if x is None:continue
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R294");ast=owner[x["owner_member_id"]]["support_ast"];need(s["physical_support_chart"]==ast["coordinate_chart"] and x["source_row_sha256"]==s["row_sha256"],"R294 join")
  if kind==TPS:box=s["exact_support_representation_box"];outer=ast["bounds"];coord="TPS"
  else:box=s["exact_transformed_open_cell"];outer=transformed(ast["bounds"]);coord="T2PS"
  if not strict_subset(box,outer):continue
  v=volume(box);declared=s.get("exact_transformed_cell_volume");need(v>0 and (declared is None or Fraction(declared)==v),"subcover volume");source[x["representation_id"]]=(kind,x,s,ast,{"kind":"OPEN_RATIONAL_BOX","coordinate_system":coord,"coordinate_chart":ast["coordinate_chart"],"coordinates":(["t","p","s"]if coord=="TPS"else["t^2","p","s"]),"bounds":box,"exact_coordinate_volume":str(v)});counts[kind]+=1
 with gzip.open(ROOT/R295,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R295");x=i2.get(s["Round295A_retained_continuation_alias_row_id"]);need(x is not None and x["source_row_sha256"]==s["row_sha256"] and x["owner_member_id"]==s["target_Round294_registry_occurrence_id"],"R295 join");ast=owner[x["owner_member_id"]]["support_ast"];box=s["retained_positive_t_open_box"];need(s["source_chart"]==ast["coordinate_chart"] and box[1]==ast["bounds"][0] and box[2:]==ast["bounds"][2:] and s["exact_full_face_shared"] is True and s["formal_occurrence_alias_credit"]==1,"adjacency");v=volume(box);need(v>0 and Fraction(s["retained_exact_coordinate_volume"])==v,"R295 volume");source[x["representation_id"]]=(ADJ,x,s,ast,{"kind":"OPEN_RATIONAL_BOX","coordinate_system":"TPS","coordinate_chart":ast["coordinate_chart"],"coordinates":["t","p","s"],"bounds":box,"exact_coordinate_volume":str(v)});counts[ADJ]+=1
 need(counts==Counter(EXPECTED) and len(source)==2520,"source census");rep={r["representation_id"]:r for r in rows(ROOT/REP) if r["representation_id"] in source};need(set(rep)==set(source),"C16");out=[]
 for i,rid in enumerate(sorted(source,key=lambda x:x.encode())):
  kind,x,s,ast,sub=source[rid];relation="STRICT_SUBCOVER_OF_OWNER_SUPPORT"if kind!=ADJ else"ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE";b={"schema":"cm2.round306c20d.source-g-2520-preserved-nonfull-alias-negative-disposition-kernel.v1.row.v1","ordinal":i,"representation_id":rid,"owner_member_id":x["owner_member_id"],"fresh_component_id":rep[rid]["fresh_component_id"],"source_semantics":kind,"typed_source_support_ast":sub,"typed_source_support_ast_sha256":h(sub),"owner_support_ast_sha256":owner[x["owner_member_id"]]["support_ast_sha256"],"exact_relation_to_owner_support":relation,"negative_disposition":"NOT_A_COMPLETE_SUPPORT_REPRESENTATION__RETAIN_AS_TYPED_NONFULL_ALIAS_HANDLE","source_row_sha256":s["row_sha256"],"formal_credit":{"typed_nonfull_representation_disposition":1,"alias_representation_set_equality":0},"strict_nonpromotion":{"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 desc={"filename":L,"row_count":2520,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c20d.source-g-2520-preserved-nonfull-alias-negative-disposition-kernel.v1","status":"PASS_2520_PRESERVED_NONFULL_ALIASES_TYPED_AND_NEGATIVELY_DISPOSED","typed_nonfull_representation_disposition_credit":2520,"disposition_census":EXPECTED,"preserved_representation_set_equality_credit":163224,"preserved_typed_nonfull_representation_count":2520,"preserved_representation_semantic_closure_count":165744,"remaining_preserved_alias_semantic_debt":0,"remaining_preserved_A1_A2_obligation_debt":80092,"ledger":desc,"strict_nonpromotion":{"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
