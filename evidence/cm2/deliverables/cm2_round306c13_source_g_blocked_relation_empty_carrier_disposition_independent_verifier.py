#!/usr/bin/env python3
"""Independently verify the C13 exact-carrier nonincidence dispositions."""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,stat,sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any,Final,Iterator
ROOT:Final=Path(__file__).parent;PREFIX:Final="cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition";LEDGER:Final=PREFIX+"_ledger.jsonl.gz";RESULT:Final=PREFIX+"_result.json";MANIFEST:Final=PREFIX+"_manifest.sha256";PRODUCER_SHA:Final="47ddc15590daa35e42ec1159101e3b044c05627e8565a9125a4aad706a3634a9"
class Rejected(RuntimeError):pass
def need(x:bool,label:str)->None:
 if type(x) is not bool or not x:raise Rejected(label)
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def fsha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def ref(r:dict[str,Any],field:str="row_id")->dict[str,str]:return {"row_id":r[field],"row_sha256":r["row_sha256"]}
@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
PINS:Final=(Pin("BLOCKED","cm2_round306c11_source_g_graph_side_local_theorem_disposition_blocked_ledger.jsonl.gz",43313,"8607da23d37de93d6cdf8e04a36d2f70d7908e8b55a8595cd34693f377479bdf"),Pin("DISPOSITION","cm2_round306c11_source_g_graph_side_local_theorem_disposition_disposition_ledger.jsonl.gz",10888167,"b1af6336b83842f2c6380929977f6d3591cfb50a1b305c7eafd197931d623543"),Pin("SUPPORT","cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz",19958893,"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),Pin("C4","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz",101147,"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),Pin("R235","cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json",67765471,"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),Pin("R248","cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json",205148977,"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"))
ZERO_KEYS:Final={"local_graph_side_physical_incidence","one_sided_trace","graph_sheet_set_equality","representation_pullback","member_normalized_support","global_normalized_support","DSU_edge","DSU_union","B1A","B2","maximality","CM2"}
def read(p:Pin)->bytes:
 path=ROOT/p.filename;i=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(i.st_mode) and i.st_size==p.size,"pin size:"+p.role);raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==p.sha256,"pin sha:"+p.role);return raw
def rows(raw:bytes,label:str)->Iterator[dict[str,Any]]:
 with gzip.GzipFile(fileobj=io.BytesIO(raw)) as f:
  for n,line in enumerate(f):
   r=json.loads(line);core=dict(r);claimed=core.pop("row_sha256",None);need(claimed==obj(core),f"row closure:{label}:{n}");yield r
def legacy(raw:bytes,label:str)->dict[str,Any]:
 d=json.loads(raw);need(d["result_sha256"]==obj(d["result"]),"legacy closure:"+label);return d["result"]
def interval(s:dict[str,Any])->tuple[Fraction,Fraction,str,int]:
 t=next(x for x in s["carrier_domain_ast"]["args"] if x.get("coordinate")=="t");lo,hi=Fraction(t["lower"]),Fraction(t["upper"]);need(lo<hi and (lo==0 or hi==0),"one-sided carrier");return lo,hi,"LOWER" if lo==0 else "UPPER",1 if lo==0 else -1
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir");ap.add_argument("--manifest-first",action="store_true");a=ap.parse_args();outdir=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve()
 if a.manifest_first:
  entries={}
  for line in (ROOT/MANIFEST).read_text("ascii").splitlines():digest,sep,name=line.partition("  ");need(sep=="  " and name not in entries,"manifest syntax");entries[name]=digest
  need(len(entries)==8 and all(fsha(ROOT/n)==d for n,d in entries.items()),"manifest members")
 raw={p.role:read(p) for p in PINS};result_raw=(outdir/RESULT).read_bytes();result=json.loads(result_raw);core=dict(result);claimed=core.pop("result_sha256",None);need(result_raw==canonical(result) and claimed==obj(core),"result closure");need(result["producer_source"]["sha256"]==PRODUCER_SHA,"producer binding");need(result["census"]=={"R235_EVENT_ABSENT":32,"R235_EVENT_PRESENT":120,"R235D_NEGATIVE_TO_POSITIVE":16,"blocked_input_rows":168,"empty_carrier_nonincidence_dispositions":168},"result census");need(result["scoped_credit"]=={"relation_nonincidence_disposition":168} and set(result["formal_credit"])==ZERO_KEYS and all(v==0 for v in result["formal_credit"].values()),"result credit");need(result["corrected_physical_relation_census"]=={"prior_mechanical_physical_denominator":15392,"invalid_graph_side_relations_removed":168,"corrected_physical_denominator":15224,"valid_graph_to_sheet_relations":5264,"valid_graph_to_side_relations":9960,"remaining_blocked_graph_side_relations":0},"corrected denominator")
 desc=result["disposition_ledger"];lp=outdir/LEDGER;need(lp.stat().st_size==desc["compressed_size"] and fsha(lp)==desc["compressed_sha256"],"ledger descriptor")
 blocked={r["row_id"]:r for r in rows(raw["BLOCKED"],"blocked")};wanted_disp={r["disposition_ref"]["row_id"] for r in blocked.values()};disp={r["row_id"]:r for r in rows(raw["DISPOSITION"],"disp") if r["row_id"] in wanted_disp};wanted_graph={r["graph_id"] for r in blocked.values()};support={r["graph_id"]:r for r in rows(raw["SUPPORT"],"support") if r["graph_id"] in wanted_graph};bridge={r["bridge_row_id"]:r for r in rows(raw["C4"],"C4")};p235={r["endpoint_graph_partition_row_id"]:r for r in legacy(raw["R235"],"R235")["single_endpoint_graph_partition_rows"] if r["endpoint_graph_partition_row_id"] in wanted_graph};wanted_side={r["side_member_id"] for r in blocked.values()};bulk={r["wall_bulk_node_id"]:r for r in legacy(raw["R248"],"R248")["formal_wall_positive_volume_bulk_ledger"]["rows"] if r["wall_bulk_node_id"] in wanted_side};need(len(blocked)==len(disp)==len(support)==len(bulk)==168 and len(p235)==152,"input exhaustion")
 output=list(rows(lp.read_bytes(),"C13"));need(len(output)==168,"output count");seen=set();census={"R235_EVENT_ABSENT":0,"R235_EVENT_PRESENT":0,"R235D_NEGATIVE_TO_POSITIVE":0}
 for n,r in enumerate(output):
  need(r["disposition_ordinal"]==n and r["disposition"]=="MECHANICAL_GRAPH_SIDE_JOIN_INVALID__STRICT_BRANCH_EMPTY_ON_EXACT_CARRIER","row order/disposition");b=blocked[r["C11_blocked_ref"]["row_id"]];d=disp[r["C11_disposition_ref"]["row_id"]];s=support[r["graph_id"]];v=bulk[r["side_member_id"]];need(r["C11_blocked_ref"]==ref(b) and r["C11_disposition_ref"]==ref(d) and r["C10_exact_support_ref"]==ref(s),"row refs");need(r["graph_id"]==b["graph_id"] and r["side_member_id"]==b["side_member_id"] and r["side_role"]==b["side_role"],"row subject");need(s["equation_ast"]["left"]=={"op":"MUL","args":[{"op":"RATIONAL_CONSTANT","value":"9/25"},{"op":"COORDINATE","name":"t"}]},"exact factor");lo,hi,face,inward=interval(s);cert=r["empty_carrier_certificate"];core=dict(cert);csha=core.pop("certificate_sha256",None);geometry=core.pop("R248_null_positive_box_not_used_as_geometry",None);need(csha==obj(core) and geometry is True,"certificate closure");need(cert["zero_face"]==face and cert["carrier_t_interval"]==[str(lo),str(hi)],"certificate carrier");need(v["exact_positive_3D_box"] is None and v["exact_positive_3D_volume"] is None,"R248 null geometry")
  if r["graph_class"]=="R235_SOURCE_EXACT_FACE_FULL_BASE":
   p=p235[r["graph_id"]];eta=1 if p["fixed_endpoint_factor_sign"]=="STRICT_POSITIVE" else -1;local="EVENT_ABSENT" if eta*inward>0 else "EVENT_PRESENT";need(r["side_role"]!=local and cert["kind"]=="R235_EXACT_ONE_SIDED_CARRIER_SIGN_EXHAUSTION" and cert["strict_branch_intersection_with_carrier"]=="EMPTY","R235 empty branch");need(v["branch_label"]==r["side_role"] and v["source_partition_row_id"]==p["endpoint_graph_partition_row_id"],"R235 branch binding");census["R235_"+r["side_role"]]+=1
  else:
   br=bridge[cert["C4_bridge_ref"]["row_id"]];rec=br["semantic_reconstruction"];source="STRICT_POSITIVE" if inward>0 else "STRICT_NEGATIVE";need(r["side_role"]=="source:NEGATIVE_TO_POSITIVE" and rec["target_factor_fixed_sign"]==source,"R235D same-sign carrier");need(cert["kind"]=="R235D_COMPLETE_DOMAIN_ENDPOINT_SIGN_EXHAUSTION" and cert["strict_branch_intersection_with_complete_carrier"]=="EMPTY","R235D empty branch");need(v["branch_label"]=="NEGATIVE_TO_POSITIVE","R235D branch binding");census["R235D_NEGATIVE_TO_POSITIVE"]+=1
  need(r["relation_nonincidence_disposition_credit"]==1 and r["local_graph_side_physical_incidence_proved"] is False and r["one_sided_trace_required"] is False and r["representation_pullback_required"] is False and r["DSU_edge_or_union_authorized"] is False,"row negative scope");need(set(r["formal_credit"])==ZERO_KEYS and all(v==0 for v in r["formal_credit"].values()),"row zero credit");need((r["graph_id"],r["side_member_id"]) not in seen,"row uniqueness");seen.add((r["graph_id"],r["side_member_id"]))
 need(len(seen)==168 and census=={"R235_EVENT_ABSENT":32,"R235_EVENT_PRESENT":120,"R235D_NEGATIVE_TO_POSITIVE":16},"output exhaustion");status="PASS_MANIFEST_FIRST_NO_WRITE_C13_168_EMPTY_RELATIONS" if a.manifest_first else "PASS_INDEPENDENT_C13_168_EMPTY_RELATIONS";print(json.dumps({"status":status,"result_sha256":claimed},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
