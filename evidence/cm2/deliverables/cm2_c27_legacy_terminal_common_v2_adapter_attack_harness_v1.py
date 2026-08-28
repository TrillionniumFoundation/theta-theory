#!/usr/bin/env python3
"""Coherent re-signed attacks on the six-terminal common-v2 adapter."""

from __future__ import annotations

import argparse,copy,gzip,hashlib,json
from pathlib import Path
import shutil,subprocess,sys,tempfile
from typing import Any,Callable

ROOT=Path(__file__).resolve().parent.parent
VERIFIER=ROOT/"deliverables/cm2_c27_legacy_terminal_common_v2_adapter_independent_verifier_v1.py"

def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def dig(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def fsha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(4<<20):h.update(b)
 return h.hexdigest()
def seq(shas:list[str])->str:
 h=hashlib.sha256()
 for s in shas:h.update(s.encode("ascii")+b"\n")
 return h.hexdigest()
def load(p:Path)->list[dict[str,Any]]:
 with gzip.open(p,"rt",encoding="ascii") as f:return [json.loads(l) for l in f]
def write(p:Path,rows:list[dict[str,Any]])->None:
 with p.open("wb") as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as z:
   for r in rows:z.write(enc(r)+b"\n")
def close_rows(rows:list[dict[str,Any]])->None:
 for i,r in enumerate(rows):
  r["ordinal"]=i;r.pop("row_sha256",None);r["row_sha256"]=dig(r)
def flip(s:str)->str:return ("0" if s[0]!="0" else "1")+s[1:]

def resign(directory:Path,result:dict[str,Any],sync:bool=True)->None:
 entries={e["authority_slot"]:e for e in result["adapter_entries"]}
 relation={};candidate_total=proof_total=0
 for slot,e in entries.items():
  cp=directory/e["candidate_ownership_ledger"]["path"]
  pp=directory/e["materialized_physical_proof_join_ledger"]["path"]
  candidates=load(cp);proofs=load(pp)
  close_rows(proofs)
  if sync:
   by={}
   for p in proofs:by.setdefault(p["candidate_key"],[]).append(p)
   for c in candidates:
    owned=by.get(c["candidate_key"],[])
    c["physical_proof_row_count"]=len(owned)
    c["physical_proof_row_sequence_sha256"]=seq([p["row_sha256"] for p in owned])
  close_rows(candidates);write(cp,candidates);write(pp,proofs)
  for path,rows,key in ((cp,candidates,"candidate_ownership_ledger"),(pp,proofs,"materialized_physical_proof_join_ledger")):
   d=e[key];d["row_count"]=len(rows);d["file_size"]=path.stat().st_size;d["file_sha256"]=fsha(path)
   d["row_sequence_sha256"]=seq([r["row_sha256"] for r in rows])
  e["native_candidate_count"]=len(candidates)
  e["semantic_incidences_promoted_to_physical_proof_count"]=len(proofs)
  candidate_total+=len(candidates);proof_total+=len(proofs)
  for c in candidates:relation[c["component_relation_disposition"]]=relation.get(c["component_relation_disposition"],0)+1
 result["candidate_total"]=candidate_total;result["materialized_physical_proof_join_total"]=proof_total
 result["component_relation_disposition_census"]=dict(sorted(relation.items()))
 result.pop("result_sha256",None);result["result_sha256"]=dig(result)
 (directory/"result.json").write_bytes(enc(result)+b"\n")

def mutate_rows(directory:Path,slot:str,kind:str,fn:Callable[[list[dict[str,Any]]],None])->None:
 p=directory/slot/("candidate_ownership.jsonl.gz" if kind=="candidate" else "materialized_physical_proof_join.jsonl.gz")
 rows=load(p);fn(rows);write(p,rows)

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument("--baseline",required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
 baseline=Path(a.baseline).resolve();baseline_result=json.loads((baseline/"result.json").read_bytes())
 attacks=[]
 def add(name:str,fn:Callable[[Path,dict[str,Any]],None],sync:bool=True):attacks.append((name,fn,sync))
 add("drop_candidate",lambda d,r:mutate_rows(d,"T01_RETAINED_CONTINUATION","candidate",lambda x:x.pop(0)))
 add("duplicate_candidate",lambda d,r:mutate_rows(d,"T02_OUTGOING_GRAPHS","candidate",lambda x:x.insert(1,copy.deepcopy(x[0]))))
 def field(field:str,value:Any):
  return lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","candidate",lambda x:x[len(x)//2].__setitem__(field,value))
 add("candidate_kind",field("candidate_kind","FORGED_KIND"));add("candidate_pair_nonnull",field("candidate_pair_key_or_null","forged-pair"))
 add("terminal_ordinal",field("terminal_ordinal",4));add("authority_slot",field("authority_slot","T04_DOUBLE_GRAPHS"))
 add("primitive_authority_pin",field("primitive_authority_row_sha256","0"*64));add("component_relation",field("component_relation_disposition","NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"))
 add("candidate_formal_credit",field("formal_credit",1))
 def proof_bearing_candidate_field(field_name:str,value:Any):
  def attack(directory:Path,result:dict[str,Any])->None:
   def edit(rows:list[dict[str,Any]])->None:
    row=next(r for r in rows if r["physical_proof_row_count"]>0)
    row[field_name]=value
   mutate_rows(directory,"T03_SINGLE_GRAPHS","candidate",edit)
  return attack
 add("candidate_proof_count",proof_bearing_candidate_field("physical_proof_row_count",0),False)
 add("candidate_proof_sequence",proof_bearing_candidate_field("physical_proof_row_sequence_sha256","0"*64),False)
 add("drop_physical_proof",lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","proof",lambda x:x.pop(0)))
 def dup_proof(rows):
  q=copy.deepcopy(rows[0]);q["proof_row_key"] += ":duplicate";rows.insert(1,q)
 add("duplicate_physical_proof",lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","proof",dup_proof))
 def proof_field(field:str,value:Any):
  return lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","proof",lambda x:x[0].__setitem__(field,value))
 add("proof_candidate_key",proof_field("candidate_key","cm2-c27-independent:SINGLE_GRAPHS:forged"))
 def mutate_pair(rows):rows[0]["ordered_C15_member_pair"][0]+="-mutant";rows[0]["ordered_C15_member_pair"].sort()
 add("proof_member_pair",lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","proof",mutate_pair))
 def mutate_component(rows):rows[0]["ordered_C15_component_pair"][0]+="-mutant";rows[0]["ordered_C15_component_pair"].sort()
 add("proof_component_pair",lambda d,r:mutate_rows(d,"T03_SINGLE_GRAPHS","proof",mutate_component))
 add("proof_edge_key",proof_field("component_edge_key","round306c27r2-v5-component-edge:"+"0"*64))
 add("proof_witness_key",proof_field("physical_witness_key","forged-witness"))
 add("proof_primitive_pin",proof_field("primitive_authority_row_sha256","0"*64))
 add("proof_atom_incidence",proof_field("atom_pair_incidence_key_or_null","forged-incidence"))
 add("proof_formal_credit",proof_field("formal_credit",1))
 add("source_W_promotion",lambda d,r:r.__setitem__("source_W_transition_authorized",True))
 add("global_totality_promotion",lambda d,r:r.__setitem__("global_atom_and_full_twenty_family_totality_closed",True))
 add("result_native_semantic_incidence_total",lambda d,r:r.__setitem__("native_semantic_proof_incidence_total",62159),False)
 results=[]
 with tempfile.TemporaryDirectory(prefix="cm2-common-v2-attacks-") as td:
  root=Path(td)
  for i,(name,fn,sync) in enumerate(attacks):
   d=root/f"a{i:02d}";shutil.copytree(baseline,d);result=copy.deepcopy(baseline_result);fn(d,result);resign(d,result,sync)
   out=d/"attack_verification.json";p=subprocess.run([sys.executable,"-I","-B",str(VERIFIER),"--candidate-dir",str(d),"--output",str(out)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   ok=p.returncode==2 and p.stderr==b"";results.append({"ordinal":i,"attack":name,"rejected":ok,"numeric_exit":p.returncode,"stdout_sha256":hashlib.sha256(p.stdout).hexdigest(),"stderr_empty":p.stderr==b""})
   if not ok:raise RuntimeError(f"not rejected:{name}:{p.stdout!r}:{p.stderr!r}")
 body={"schema":"cm2.c27-independent.legacy-terminal.common-v2-adapter.coherent-attacks.v1",
       "status":f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT",
       "attack_count":len(attacks),"all_rejected":True,"attacks":results,
       "baseline_result_file_sha256":fsha(baseline/"result.json"),"verifier_file_sha256":fsha(VERIFIER),
       "formal_credit":0,"manifest_authorized":False,"source_W_transition_authorized":False}
 v={**body,"attack_result_sha256":dig(body)};o=Path(a.output)
 if o.exists():raise RuntimeError("fresh output required")
 o.write_bytes(enc(v)+b"\n");print(enc({"status":v["status"],"attack_result_sha256":v["attack_result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
