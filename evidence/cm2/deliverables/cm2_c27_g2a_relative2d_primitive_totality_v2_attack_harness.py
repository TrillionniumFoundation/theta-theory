#!/usr/bin/env python3
"""Coherent mutation attacks for the independent G2A scoped-route verifier."""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from typing import Any,Callable

class Failure(RuntimeError):pass
def need(v,label):
 if type(v)is not bool or not v:raise Failure(label)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def file_sha(path):
 h=hashlib.sha256()
 with path.open("rb")as f:
  while b:=f.read(4<<20):h.update(b)
 return h.hexdigest()
def load_doc(path):return json.loads(path.read_bytes())
def close_doc(doc):
 body=dict(doc);body.pop("result_sha256",None);body.pop("semantic_projection_sha256",None);body["semantic_projection_sha256"]=digest({k:v for k,v in body.items()if k not in{"invocation_seed","root_input_capture","input_capture"}});body["result_sha256"]=digest(body);return body
def save_doc(path,doc):path.write_bytes(canonical(close_doc(doc))+b"\n");return file_sha(path)
def rows(path):
 with gzip.open(path,"rb")as z:return[json.loads(line)for line in z]
def reclose(row):
 body=dict(row);body.pop("row_sha256",None);body["row_sha256"]=digest(body);return body
def write_rows(path,data):
 seq=hashlib.sha256()
 with path.open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as z:
   for row in data:z.write(canonical(row)+b"\n");seq.update(bytes.fromhex(row["row_sha256"]))
 return{"filename":path.name,"row_count":len(data),"file_sha256":file_sha(path),"row_sequence_sha256":seq.hexdigest()}
def copy_bundle(src_result,dst):shutil.copytree(src_result.parent,dst);return dst/src_result.name

def mutate_theorem(base:Path,dst:Path,name:str)->tuple[Path,str]:
 result_path=copy_bundle(base,dst);doc=load_doc(result_path)
 ledger_key=None;mut:Callable|None=None
 if name=="contact_omit":ledger_key="contacts";mut=lambda x:x[:-1]
 elif name=="contact_duplicate":ledger_key="contacts";mut=lambda x:x+[x[-1]]
 elif name=="contact_terminal_flip":
  ledger_key="contacts"
  def mut(x):y=list(x);r=dict(y[0]);r["assigned_unique_terminal"]="NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT";y[0]=reclose(r);return y
 elif name=="contact_raw_signed_true":
  ledger_key="contacts"
  def mut(x):y=list(x);r=dict(y[0]);r["raw_SIGNED_pair"]=True;y[0]=reclose(r);return y
 elif name=="reverse_omit":ledger_key="reverse_empty";mut=lambda x:x[:-1]
 elif name=="cross_contact_hash_flip":
  ledger_key="cross_C15_witnesses"
  def mut(x):y=list(x);r=dict(y[0]);r["contact_alias_route_row_sha256"]="0"*64;y[0]=reclose(r);return y
 elif name=="edge_count_increment":
  ledger_key="unique_cross_C15_component_edges"
  def mut(x):y=list(x);r=dict(y[0]);r["contact_alias_witness_count"]+=1;y[0]=reclose(r);return y
 elif name=="final_route_terminal_flip":
  ledger_key="routes"
  def mut(x):y=list(x);r=dict(y[0]);r["assigned_unique_terminal"]="MUTATED_TERMINAL";y[0]=reclose(r);return y
 elif name=="complement_omit":ledger_key="complement";mut=lambda x:x[:-1]
 elif name=="global_unique_true":doc["global_three_terminal_unique_assignment"]=True
 elif name=="positive_C19_closed":doc["positive_C19_91672_intersection_gate"]="CLOSED_WITHOUT_FRESH_LEDGER"
 elif name=="C23_candidate_one":doc["C23_zero_proof"]["candidate_count"]=1
 elif name=="shared_pin_flip":doc["implementation_dependency_pin"]["sha256"]="f"*64
 else:raise Failure("unknown theorem attack:"+name)
 if ledger_key is not None:
  meta=doc["ledgers"][ledger_key];path=result_path.parent/meta["filename"];data=rows(path);data=mut(data);doc["ledgers"][ledger_key]=write_rows(path,data)
 return result_path,save_doc(result_path,doc)

def mutate_factor(base:Path,dst:Path)->tuple[Path,str]:
 result_path=copy_bundle(base,dst);doc=load_doc(result_path);path=result_path.parent/doc["ledger"]["filename"];data=rows(path);r=dict(data[0]);r["disposition"]="EXACT_EMPTY_INTERSECTION"if r["disposition"]=="EXACT_POSITIVE_SUPPORT"else"EXACT_POSITIVE_SUPPORT";data[0]=reclose(r);doc["ledger"]=write_rows(path,data);return result_path,save_doc(result_path,doc)
def mutate_candidate(base:Path,dst:Path)->tuple[Path,str]:
 result_path=copy_bundle(base,dst);doc=load_doc(result_path);meta=doc["G2A"]["candidate_ledger"];path=result_path.parent/meta["filename"];data=rows(path);r=dict(data[0]);r["R300C_validation_pair"]=False;data[0]=reclose(r);doc["G2A"]["candidate_ledger"]=write_rows(path,data);return result_path,save_doc(result_path,doc)

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--candidate-result",required=True);p.add_argument("--candidate-result-sha256",required=True);p.add_argument("--factor-result",required=True);p.add_argument("--factor-result-sha256",required=True);p.add_argument("--theorem-result",required=True);p.add_argument("--theorem-result-sha256",required=True);p.add_argument("--verifier",required=True);p.add_argument("--verifier-sha256",required=True);p.add_argument("--shared-implementation-source",required=True);p.add_argument("--shared-implementation-sha256",required=True);p.add_argument("--seed",type=int,required=True);a=p.parse_args()
 out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);ver=Path(a.verifier).resolve();shared=Path(a.shared_implementation_source).resolve();need(file_sha(ver)==a.verifier_sha256,"verifier pin");need(file_sha(shared)==a.shared_implementation_sha256,"shared source pin")
 base_candidate=Path(a.candidate_result).resolve();base_factor=Path(a.factor_result).resolve();base_theorem=Path(a.theorem_result).resolve();need(file_sha(base_candidate)==a.candidate_result_sha256 and file_sha(base_factor)==a.factor_result_sha256 and file_sha(base_theorem)==a.theorem_result_sha256,"base result pins")
 def invoke(name,candidate,csha,factor,fsha,theorem,tsha):
  run=out/name;run.mkdir();cmd=[sys.executable,str(ver),"--out-dir",str(run/"verification"),"--candidate-result",str(candidate),"--candidate-result-sha256",csha,"--factor-result",str(factor),"--factor-result-sha256",fsha,"--theorem-result",str(theorem),"--theorem-result-sha256",tsha,"--shared-implementation-source",str(shared),"--shared-implementation-sha256",a.shared_implementation_sha256,"--front-gate-only","--seed",str(a.seed)];cp=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180);(run/"command.json").write_bytes(canonical(cmd)+b"\n");(run/"stdout.log").write_bytes(cp.stdout);(run/"stderr.log").write_bytes(cp.stderr);(run/"exit_code.txt").write_text(str(cp.returncode)+"\n",encoding="ascii");return cp
 control=invoke("00_control",base_candidate,a.candidate_result_sha256,base_factor,a.factor_result_sha256,base_theorem,a.theorem_result_sha256);need(control.returncode==0,"control front gate")
 theorem_attacks=["contact_omit","contact_duplicate","contact_terminal_flip","contact_raw_signed_true","reverse_omit","cross_contact_hash_flip","edge_count_increment","final_route_terminal_flip","complement_omit","global_unique_true","positive_C19_closed","C23_candidate_one","shared_pin_flip"]
 results=[]
 for i,name in enumerate(theorem_attacks,1):
  stage=out/f"payload_theorem_{i:02d}_{name}";tp,tsha=mutate_theorem(base_theorem,stage,name);cp=invoke(f"attack_{i:02d}_{name}",base_candidate,a.candidate_result_sha256,base_factor,a.factor_result_sha256,tp,tsha);need(cp.returncode!=0,name+":accepted");results.append({"attack":name,"exit_code":cp.returncode,"rejected":True})
 stage=out/"payload_factor_disposition_flip";fp,fsha=mutate_factor(base_factor,stage);cp=invoke("attack_14_factor_disposition_flip",base_candidate,a.candidate_result_sha256,fp,fsha,base_theorem,a.theorem_result_sha256);need(cp.returncode!=0,"factor flip accepted");results.append({"attack":"factor_disposition_flip","exit_code":cp.returncode,"rejected":True})
 stage=out/"payload_candidate_R300C_injection";cpth,csha=mutate_candidate(base_candidate,stage);cp=invoke("attack_15_candidate_R300C_injection",cpth,csha,base_factor,a.factor_result_sha256,base_theorem,a.theorem_result_sha256);need(cp.returncode!=0,"R300C injection accepted");results.append({"attack":"candidate_R300C_injection","exit_code":cp.returncode,"rejected":True})
 receipt={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-coherent-attacks.v2","status":"PASS_CONTROL_AND_REJECT_15_OF_15_COHERENT_MUTATIONS__ZERO_CREDIT","invocation_seed":a.seed,"control_exit_code":0,"attack_count":len(results),"accepted":0,"rejected":len(results),"attacks":results,"verifier_sha256":a.verifier_sha256,"shared_implementation_source_sha256":a.shared_implementation_sha256,"formal_credit":0,"global_three_terminal_unique_assignment":False,"positive_C19_91672_gate":"OPEN"};receipt["result_sha256"]=digest(receipt);(out/"attack_receipt.json").write_bytes(canonical(receipt)+b"\n");print(canonical({"status":receipt["status"],"result_sha256":receipt["result_sha256"]}).decode());return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Failure,KeyError,TypeError,ValueError,OSError,subprocess.TimeoutExpired)as e:print("FAIL:"+str(e));raise SystemExit(2)
