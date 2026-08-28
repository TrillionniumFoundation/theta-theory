#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";I2="cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz";R294="cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz";R295="cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";TPS="EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER";T2="EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL";ADJ="ADJACENT_POSITIVE_T_CONTINUATION";EXPECTED={TPS:720,T2:1524,ADJ:276}
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
def vol(b):return(F(b[1])-F(b[0]))*(F(b[3])-F(b[2]))*(F(b[5])-F(b[4]))
def sub(b,o):return all(F(o[2*i])<=F(b[2*i])<F(b[2*i+1])<=F(o[2*i+1])for i in range(3))and b!=o
def t2(b):
 a,z=F(b[0]),F(b[1]);need(a*z>0,"sign");lo,hi=sorted((a*a,z*z));return[str(lo),str(hi),*b[2:]]
def rebuild():
 owner={r["member_id"]:r for r in rows(ROOT/C20)};i2={r["source_row_id"]:r for r in rows(ROOT/I2)if r.get("representation_semantics")in EXPECTED};source={};counts=Counter()
 with gzip.open(ROOT/R294,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  k=s["support_representation_kind"]
  if k not in{TPS,T2}:continue
  x=i2.get(s["Round294_occurrence_representation_binding_row_id"])
  if x is None:continue
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R294");ast=owner[x["owner_member_id"]]["support_ast"];b=s["exact_support_representation_box"]if k==TPS else s["exact_transformed_open_cell"];outer=ast["bounds"]if k==TPS else t2(ast["bounds"])
  if not sub(b,outer):continue
  v=vol(b);need(s["physical_support_chart"]==ast["coordinate_chart"]and x["source_row_sha256"]==s["row_sha256"]and v>0,"R294 join");subast={"kind":"OPEN_RATIONAL_BOX","coordinate_system":("TPS"if k==TPS else"T2PS"),"coordinate_chart":ast["coordinate_chart"],"coordinates":(["t","p","s"]if k==TPS else["t^2","p","s"]),"bounds":b,"exact_coordinate_volume":str(v)};source[x["representation_id"]]=(k,x,s,subast,"STRICT_SUBCOVER_OF_OWNER_SUPPORT");counts[k]+=1
 with gzip.open(ROOT/R295,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R295");x=i2[s["Round295A_retained_continuation_alias_row_id"]];ast=owner[x["owner_member_id"]]["support_ast"];b=s["retained_positive_t_open_box"];need(s["source_chart"]==ast["coordinate_chart"]and b[1]==ast["bounds"][0]and b[2:]==ast["bounds"][2:]and s["exact_full_face_shared"]is True,"adjacent");v=vol(b);subast={"kind":"OPEN_RATIONAL_BOX","coordinate_system":"TPS","coordinate_chart":ast["coordinate_chart"],"coordinates":["t","p","s"],"bounds":b,"exact_coordinate_volume":str(v)};source[x["representation_id"]]=(ADJ,x,s,subast,"ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE");counts[ADJ]+=1
 need(counts==Counter(EXPECTED)and len(source)==2520,"sources");return owner,source
def verify(q):
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need((z["typed_nonfull_representation_disposition_credit"],z["preserved_representation_set_equality_credit"],z["preserved_typed_nonfull_representation_count"],z["preserved_representation_semantic_closure_count"],z["remaining_preserved_alias_semantic_debt"],z["remaining_preserved_A1_A2_obligation_debt"],z["ledger"]["row_count"])==(2520,163224,2520,165744,0,80092,2520),"census");need(z["disposition_census"]==EXPECTED and z["strict_nonpromotion"]=={"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"boundary");need(fh(q/L)==z["ledger"]["sha256"]and(q/L).stat().st_size==z["ledger"]["size"],"descriptor");owner,source=rebuild();rep={r["representation_id"]:r for r in rows(ROOT/REP)if r["representation_id"]in source};need(set(rep)==set(source),"C16");seen=set()
 for i,r in enumerate(rows(q/L)):
  rid=r["representation_id"];need(rid in source and rid not in seen and r["ordinal"]==i,"order");seen.add(rid);k,x,s,subast,relation=source[rid];need(r["owner_member_id"]==x["owner_member_id"]and r["fresh_component_id"]==rep[rid]["fresh_component_id"]and r["source_semantics"]==k and r["typed_source_support_ast"]==subast and r["typed_source_support_ast_sha256"]==h(subast)and r["owner_support_ast_sha256"]==owner[x["owner_member_id"]]["support_ast_sha256"]and r["exact_relation_to_owner_support"]==relation,"body");need(r["negative_disposition"]=="NOT_A_COMPLETE_SUPPORT_REPRESENTATION__RETAIN_AS_TYPED_NONFULL_ALIAS_HANDLE"and r["source_row_sha256"]==s["row_sha256"]and r["formal_credit"]=={"typed_nonfull_representation_disposition":1,"alias_representation_set_equality":0},"credit")
 need(seen==set(source),"exhaustion");return{"status":"PASS_INDEPENDENT_C20D_2520_TYPED_NEGATIVE_ALIAS_DISPOSITIONS","result_sha256":claimed,"rows":2520}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
