#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";I2="cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz";R294="cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";K="EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL"
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
def transform(box):
 left,right=Fraction(box[0]),Fraction(box[1]);need(left*right>0,"sign");lo,hi=sorted((left*left,right*right));return [str(lo),str(hi),*box[2:]],("POSITIVE"if left>0 else"NEGATIVE")
def verify(q):
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");b=dict(z);claimed=b.pop("result_sha256");need(claimed==h(b),"result closure");need((z["alias_representation_equality_credit"],z["cumulative_preserved_representation_equality_credit"],z["remaining_preserved_alias_representation_debt"],z["remaining_preserved_A1_A2_obligation_debt"],z["ledger"]["row_count"])==(76,163224,2520,80092,76),"census");need(z["remaining_alias_debt_by_kind"]=={"TPS_INCLUSION_SUBCOVER":720,"T2PS_STRICT_SUBCOVER":1524,"R295A_ADJACENT_CONTINUATION":276} and z["strict_nonpromotion"]=={"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"boundary");need(fh(q/L)==z["ledger"]["sha256"] and (q/L).stat().st_size==z["ledger"]["size"],"descriptor")
 owner={r["member_id"]:r for r in rows(ROOT/C20)};i2={r["source_row_id"]:r for r in rows(ROOT/I2) if r.get("representation_semantics")==K};source={}
 with gzip.open(ROOT/R294,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  if s["support_representation_kind"]!=K:continue
  x=i2.get(s["Round294_occurrence_representation_binding_row_id"])
  if x is None:continue
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R294");ast=owner[x["owner_member_id"]]["support_ast"];cell,sign=transform(ast["bounds"])
  if s["exact_transformed_open_cell"]!=cell:continue
  v=(Fraction(cell[1])-Fraction(cell[0]))*(Fraction(cell[3])-Fraction(cell[2]))*(Fraction(cell[5])-Fraction(cell[4]));need(Fraction(s["exact_transformed_cell_volume"])==v and s["physical_support_chart"]==ast["coordinate_chart"] and x["source_row_sha256"]==s["row_sha256"],"exact");source[x["representation_id"]]=(x,s,ast,cell,sign)
 need(len(source)==76,"source census");rep={r["representation_id"]:r for r in rows(ROOT/REP) if r["representation_id"] in source};need(set(rep)==set(source),"C16");seen=set()
 for i,r in enumerate(rows(q/L)):
  rid=r["representation_id"];need(rid in source and rid not in seen and r["ordinal"]==i,"order");seen.add(rid);x,s,ast,cell,sign=source[rid];th={"kind":"FIXED_SIGN_T2PS_BIJECTION","forward":{"u":"t^2","p":"p","s":"s"},"inverse":{"t":("sqrt(u)"if sign=="POSITIVE"else"-sqrt(u)"),"p":"p","s":"s"},"fixed_t_sign":sign,"source_chart":ast["coordinate_chart"],"TPS_domain":ast["bounds"],"T2PS_domain":cell,"forward_inverse_identity":True,"inverse_forward_identity":True};cert={"kind":"R294_T2PS_CELL_EQUALS_FIXED_SIGN_PULLBACK_OF_C20A_OWNER_SUPPORT","R294_row_sha256":s["row_sha256"],"I2_representation_row_sha256":x["row_sha256"],"same_physical_chart":True,"interchart_transport_used":False};need(r["owner_member_id"]==x["owner_member_id"] and r["fresh_component_id"]==rep[rid]["fresh_component_id"] and r["owner_support_ast"]==ast and r["owner_support_ast_sha256"]==h(ast) and r["T2PS_bijection_theorem"]==th and r["T2PS_bijection_theorem_sha256"]==h(th),"body");need(r["set_equality_certificate"]==cert and r["formal_credit"]=={"alias_representation_set_equality":1},"credit")
 need(seen==set(source),"exhaustion");return {"status":"PASS_INDEPENDENT_C20C_76_FIXED_SIGN_T2PS_EQUALITIES","result_sha256":claimed,"rows":76}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
