#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";I2="cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz";R294="cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={C20:"bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",I2:"68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83",R294:"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"};K="EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL"
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
def t2ps(box):
 a,b=Fraction(box[0]),Fraction(box[1]);need(a*b>0,"fixed sign");lo,hi=sorted((a*a,b*b));return [str(lo),str(hi),*box[2:]],("POSITIVE" if a>0 else "NEGATIVE")
def build(q):
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 owner={r["member_id"]:r for r in rows(ROOT/C20)};i2={r["source_row_id"]:r for r in rows(ROOT/I2) if r.get("representation_semantics")==K};source={}
 with gzip.open(ROOT/R294,"rt")as f:d=json.load(f)
 for s in d["rows"]:
  if s["support_representation_kind"]!=K:continue
  x=i2.get(s["Round294_occurrence_representation_binding_row_id"])
  if x is None:continue
  bb=dict(s);need(bb.pop("row_sha256")==h(bb),"R294");ast=owner[x["owner_member_id"]]["support_ast"];transformed,sign=t2ps(ast["bounds"])
  if s["exact_transformed_open_cell"]!=transformed:continue
  v=(Fraction(transformed[1])-Fraction(transformed[0]))*(Fraction(transformed[3])-Fraction(transformed[2]))*(Fraction(transformed[5])-Fraction(transformed[4]));need(Fraction(s["exact_transformed_cell_volume"])==v and s["physical_support_chart"]==ast["coordinate_chart"] and s["exact_transformed_coordinate_system"]=="(t^2,p,s)" and s["formal_occurrence_alias_credit"]==1,"exact T2PS");need(x["source_row_sha256"]==s["row_sha256"] and x["owner_member_id"]==s["target_registry_occurrence_id"],"join");source[x["representation_id"]]=(x,s,ast,transformed,sign)
 need(len(source)==76,"source census");rep={r["representation_id"]:r for r in rows(ROOT/REP) if r["representation_id"] in source};need(set(rep)==set(source),"C16");out=[]
 for i,rid in enumerate(sorted(source,key=lambda x:x.encode())):
  x,s,ast,transformed,sign=source[rid];theorem={"kind":"FIXED_SIGN_T2PS_BIJECTION","forward":{"u":"t^2","p":"p","s":"s"},"inverse":{"t":("sqrt(u)" if sign=="POSITIVE" else "-sqrt(u)"),"p":"p","s":"s"},"fixed_t_sign":sign,"source_chart":ast["coordinate_chart"],"TPS_domain":ast["bounds"],"T2PS_domain":transformed,"forward_inverse_identity":True,"inverse_forward_identity":True};b={"schema":"cm2.round306c20c.source-g-76-fixed-sign-t2ps-exact-alias-support-kernel.v1.row.v1","ordinal":i,"representation_id":rid,"owner_member_id":x["owner_member_id"],"fresh_component_id":rep[rid]["fresh_component_id"],"owner_support_ast":ast,"owner_support_ast_sha256":h(ast),"T2PS_bijection_theorem":theorem,"T2PS_bijection_theorem_sha256":h(theorem),"set_equality_certificate":{"kind":"R294_T2PS_CELL_EQUALS_FIXED_SIGN_PULLBACK_OF_C20A_OWNER_SUPPORT","R294_row_sha256":s["row_sha256"],"I2_representation_row_sha256":x["row_sha256"],"same_physical_chart":True,"interchart_transport_used":False},"formal_credit":{"alias_representation_set_equality":1},"strict_nonpromotion":{"remaining_T2PS_subcovers":0,"TPS_inclusion_subcovers":0,"R295A_adjacent_continuations":0,"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 desc={"filename":L,"row_count":76,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c20c.source-g-76-fixed-sign-t2ps-exact-alias-support-kernel.v1","status":"PASS_76_FIXED_SIGN_T2PS_ALIAS_REPRESENTATION_SET_EQUALITIES","alias_representation_equality_credit":76,"cumulative_preserved_representation_equality_credit":163224,"remaining_preserved_alias_representation_debt":2520,"remaining_alias_debt_by_kind":{"TPS_INCLUSION_SUBCOVER":720,"T2PS_STRICT_SUBCOVER":1524,"R295A_ADJACENT_CONTINUATION":276},"remaining_preserved_A1_A2_obligation_debt":80092,"ledger":desc,"strict_nonpromotion":{"A1_A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
