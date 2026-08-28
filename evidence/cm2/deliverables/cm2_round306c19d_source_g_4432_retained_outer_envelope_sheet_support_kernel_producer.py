#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent;P="cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json";C14="cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_old_outer_envelope_family_disposition_ledger.jsonl.gz";R248="cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json";MEM="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";REP="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";PINS={C14:"96dee605bbec4024e8943b4d40c13ca5e86de411d92efa3ae48b075fb5d80817",R248:"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",MEM:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",REP:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1"}
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
def closed(r):b=dict(r);need(b.pop("row_sha256",None)==h(b),"R248 closure")
def build(q):
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 disp={r["old_outer_envelope_sheet_member_id"]:r for r in rows(ROOT/C14)};need(len(disp)==4432,"disposition census")
 owners={}
 for r in json.loads((ROOT/R248).read_bytes())["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]:
  mid=r["wall_sheet_node_id"]
  if mid not in disp:continue
  closed(r);rect=r["exact_closed_base_rectangle"];area=(Fraction(rect[1])-Fraction(rect[0]))*(Fraction(rect[3])-Fraction(rect[2]));need(area>0 and Fraction(r["exact_positive_2D_sheet_area"])==area and r["sheet_three_dimensional_coordinate_volume"]=="0","sheet geometry");need(disp[mid]["R248_owner_row_sha256"]==r["row_sha256"],"owner binding");owners[mid]=(r,rect,area)
 need(set(owners)==set(disp),"owner exhaustion");mem={r["member_id"]:r for r in rows(ROOT/MEM) if r["member_id"] in disp};rep={r["owner_member_id"]:r for r in rows(ROOT/REP) if r["owner_member_id"] in disp};need(set(disp)==set(mem)==set(rep),"joins");out=[]
 for i,mid in enumerate(sorted(disp,key=lambda x:x.encode())):
  d=disp[mid];s,rect,area=owners[mid];need(mem[mid]["coarse_family"]=="NON_GRAPH" and d["old_family_after"]=="NON_GRAPH","family");ast={"kind":"CLOSED_RATIONAL_RECTANGLE_SHEET","coordinates":["p","s"],"bounds":rect,"exact_area":str(area.numerator) if area.denominator==1 else f"{area.numerator}/{area.denominator}","ambient_coordinates":["t","p","s"],"ambient_3D_coordinate_volume":"0"};b={"schema":"cm2.round306c19d.source-g-4432-retained-outer-envelope-sheet-support-kernel.v1.row.v1","ordinal":i,"member_id":mid,"representation_id":rep[mid]["representation_id"],"fresh_component_id":mem[mid]["fresh_component_id"],"support_ast":ast,"support_ast_sha256":h(ast),"construction_certificate":{"kind":"R248_HALF_OPEN_OWNER_ROW_DEFINES_COMPLETE_RETAINED_OUTER_ENVELOPE_SHEET","R248_owner_row_sha256":s["row_sha256"],"C14c_family_disposition_row_sha256":d["row_sha256"],"half_open_owner_rule":s["half_open_owner_rule"],"source_partition_kind":s["source_partition_kind"],"graph_projection_or_new_exact_partial_sheet_substitution_used":False},"formal_credit":{"member_typed_normalized_support":1,"primary_representation_set_equality":1},"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":0}};out.append({**b,"row_sha256":h(b)})
 q.mkdir(parents=True,exist_ok=True);raw=b"".join(c(x)+b"\n" for x in out)
 with (q/L).open("wb")as f:
  with gzip.GzipFile(filename="",mode="wb",fileobj=f,mtime=0)as g:g.write(raw)
 d={"filename":L,"row_count":4432,"size":(q/L).stat().st_size,"sha256":fh(q/L)};b={"schema":"cm2.round306c19d.source-g-4432-retained-outer-envelope-sheet-support-kernel.v1","status":"PASS_4432_RETAINED_OUTER_ENVELOPE_SHEETS_HAVE_EXACT_R248_BASE_RECTANGLE_SUPPORTS","member_support_credit":4432,"primary_representation_equality_credit":4432,"cumulative_nongraph_support_credit":55604,"remaining_nongraph_debt":0,"ledger":d,"strict_nonpromotion":{"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**b,"result_sha256":h(b)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
