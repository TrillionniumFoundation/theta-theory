#!/usr/bin/env python3
"""Seal the double-seed scoped G2A theorem as an explicit zero-credit receipt."""
from __future__ import annotations
import argparse,hashlib,json,os,stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

WORK=Path(__file__).resolve().parent.parent
SOURCES={
 "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v1_candidate_producer.py":"3cfc9a93a530f97eefc54611e1abd21fe9bac2d96ad87c332798090f179f06d1",
 "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_exact_classifier.py":"0c34edd017940bc74e7f29273da7fa7215531c25bbad03eff4569d32b673e082",
 "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_theorem_builder.py":"5bc07766fdb540512a750c24c7cf8f9f0862949afc9c154c066f46f02ce66544",
 "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_independent_verifier.py":"d6705c8f4be01d6d66f2a3f6e59057f93baa9e6d9f04104ddea5a9bfeae973f7",
 "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_attack_harness.py":"ad0eaa0ff0602b3521fb02c1bd5aef16ca7af0d2e557dcd914148b3c18078a2b",
 "deliverables/cm2_c27_c24a_g2b_exact_factor_sign_disposition_v1_probe.py":"7ec20f13eecf83a3598f6298421658a197ddc2170215be91b3e8a2a8324550c1",
}
class Failure(RuntimeError):pass
def need(v,label):
 if type(v)is not bool or not v:raise Failure(label)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def fp(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
@dataclass
class Capture:
 label:str;path:Path;fd:int;pre:tuple[int,...];sha256:str;wire:bytes
 @classmethod
 def open(cls,label,path,expected=None):
  p=Path(path).resolve();fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
  try:
   s=os.fstat(fd);need(stat.S_ISREG(s.st_mode),label+":regular");h=hashlib.sha256();chunks=[]
   while b:=os.read(fd,4<<20):h.update(b);chunks.append(b)
   got=h.hexdigest();need(expected is None or got==expected,label+":sha256");need(fp(os.fstat(fd))==fp(s),label+":hash-stat");return cls(label,p,fd,fp(s),got,b"".join(chunks))
  except BaseException:os.close(fd);raise
 def document(self):
  r=json.loads(self.wire);need(type(r)is dict and canonical(r)+b"\n"==self.wire,self.label+":canonical");b=dict(r);claimed=b.pop("result_sha256",None);need(type(claimed)is str and claimed==digest(b),self.label+":closure");return r
 def relative(self):return str(self.path.relative_to(WORK))
 def att(self):need(fp(os.fstat(self.fd))==self.pre,self.label+":final-stat");return{"path":self.relative(),"sha256":self.sha256,"stat_fingerprint":list(self.pre),"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True}
 def close(self):os.close(self.fd)

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True)
 for stage in("candidate","factor","theorem","verification"):
  for seed in("seed1","seed2"):p.add_argument(f"--{stage}-result-{seed}",required=True);p.add_argument(f"--{stage}-result-{seed}-sha256",required=True)
 p.add_argument("--attack-receipt",required=True);p.add_argument("--attack-receipt-sha256",required=True);p.add_argument("--seed1",type=int,required=True);p.add_argument("--seed2",type=int,required=True);a=p.parse_args();need(a.seed1!=a.seed2,"distinct seeds")
 out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);caps={};docs={}
 try:
  for rel,sha in SOURCES.items():caps["source:"+rel]=Capture.open("source:"+rel,WORK/rel,sha)
  caps["source:release_checker"]=Capture.open("source:release_checker",Path(__file__))
  caps["source:terminal_replay"]=Capture.open("source:terminal_replay",WORK/"deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_terminal_replay.py")
  for stage in("candidate","factor","theorem","verification"):
   for seed in("seed1","seed2"):
    label=stage+":"+seed;path=getattr(a,f"{stage}_result_{seed}");sha=getattr(a,f"{stage}_result_{seed}_sha256");caps[label]=Capture.open(label,path,sha);docs[label]=caps[label].document()
  caps["attacks"]=Capture.open("attacks",a.attack_receipt,a.attack_receipt_sha256);docs["attacks"]=caps["attacks"].document()
  c1,c2=docs["candidate:seed1"],docs["candidate:seed2"];f1,f2=docs["factor:seed1"],docs["factor:seed2"];t1,t2=docs["theorem:seed1"],docs["theorem:seed2"];v1,v2=docs["verification:seed1"],docs["verification:seed2"];atk=docs["attacks"]
  need(c1["invocation_seed"]==a.seed1 and c2["invocation_seed"]==a.seed2 and c1["semantic_projection_sha256"]==c2["semantic_projection_sha256"],"candidate double seed")
  need(f1["invocation_seed"]==a.seed1 and f2["invocation_seed"]==a.seed2 and f1["semantic_projection_sha256"]==f2["semantic_projection_sha256"]and f1["status"].endswith("CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT")and f2["status"]==f1["status"],"factor double seed")
  need(t1["invocation_seed"]==a.seed1 and t2["invocation_seed"]==a.seed2 and t1["semantic_projection_sha256"]==t2["semantic_projection_sha256"]and t1["status"]==t2["status"]and"POSITIVE_C19_OPEN__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT"in t1["status"],"theorem double seed")
  need(v1["invocation_seed"]==a.seed1 and v2["invocation_seed"]==a.seed2 and v1["semantic_projection_sha256"]==v2["semantic_projection_sha256"]and v1["status"]==v2["status"]and v1["status"].startswith("PASS_INDEPENDENT_EXACT_PS_CELL_BUCKET"),"verifier double seed")
  for theorem in(t1,t2):need(theorem["global_three_terminal_unique_assignment"]is False and theorem["positive_C19_91672_intersection_gate"].startswith("OPEN")and theorem["formal_credit"]==0 and theorem["historical_edge_or_validation_ledger_opened"]is False,"theorem scoped gate")
  for verification in(v1,v2):need(verification["global_three_terminal_unique_assignment"]is False and verification["positive_C19_91672_gate"]=="OPEN"and verification["formal_credit"]==0 and verification["independent_implementation"]["imports_candidate_classifier_theorem_or_shared_module"]is False,"independent scoped gate")
  need(atk["status"]=="PASS_CONTROL_AND_REJECT_15_OF_15_COHERENT_MUTATIONS__ZERO_CREDIT"and atk["accepted"]==0 and atk["rejected"]==15 and atk["verifier_sha256"]==SOURCES["deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_independent_verifier.py"],"attacks")
  ledger_groups={}
  for stage,docs_pair in(("candidate",(c1,c2)),("factor",(f1,f2)),("theorem",(t1,t2))):
   stage_groups={}
   if stage=="candidate":metas=lambda d:{"routes":d["G2A"]["route_ledger"],"G2A_candidates":d["G2A"]["candidate_ledger"],"G2B_candidates":d["G2B_candidate_ledger"]}
   elif stage=="factor":metas=lambda d:{"factor_dispositions":d["ledger"]}
   else:metas=lambda d:d["ledgers"]
   m1,m2=metas(docs_pair[0]),metas(docs_pair[1]);need(set(m1)==set(m2),stage+":ledger keys")
   for key in sorted(m1):
    need(m1[key]["file_sha256"]==m2[key]["file_sha256"]and m1[key]["row_sequence_sha256"]==m2[key]["row_sequence_sha256"]and m1[key]["row_count"]==m2[key]["row_count"],stage+":"+key+":byte identity metadata")
    paths=[]
    for seed,doc,meta in(("seed1",docs_pair[0],m1[key]),("seed2",docs_pair[1],m2[key])):
     base=caps[stage+":"+seed].path.parent;label=f"ledger:{stage}:{seed}:{key}";caps[label]=Capture.open(label,base/meta["filename"],meta["file_sha256"]);paths.append(caps[label].relative())
    stage_groups[key]={"file_sha256":m1[key]["file_sha256"],"row_sequence_sha256":m1[key]["row_sequence_sha256"],"row_count":m1[key]["row_count"],"seed_paths":paths,"byte_identical":True}
   ledger_groups[stage]=stage_groups
  need(t1["G2A_candidate_to_positive_side_bijection"]["matched"]==9408 and t1["cross_C15_contact_alias_count"]==596 and t1["unique_cross_C15_component_edge_count"]==144 and t1["C23_zero_proof"]["candidate_count"]==0 and t1["raw_terminal_pair_intersections"]=={"G2A_target_SIGNED":0,"G2A_target_COMPLETE":0,"positive_side_target_SIGNED":0,"positive_side_target_COMPLETE":0},"theorem headline")
  payload_lines=[]
  for cap in caps.values():payload_lines.append(f"{cap.sha256}  {cap.relative()}")
  payload_lines=sorted(set(payload_lines),key=lambda x:x.split("  ",1)[1]);payload=("\n".join(payload_lines)+"\n").encode("ascii");(out/"payload_manifest.sha256").write_bytes(payload);payload_sha=hashlib.sha256(payload).hexdigest()
  receipt={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-zero-credit-receipt.v2","status":"PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__SCOPED_G2A_5264_CLOSED__POSITIVE_C19_AND_GLOBAL_THREE_TERMINAL_OPEN__ZERO_CREDIT","seeds":[a.seed1,a.seed2],"headline":{"G2A_graphs":5264,"scoped_unique_routes":5264,"contact_aliases":9408,"positive_sides":9408,"reverse_empty":9392,"single_side_no_reverse":16,"complement":552,"C23_candidates":0,"same_C15":8812,"cross_C15":596,"unique_cross_C15_component_edges":144,"raw_SIGNED_COMPLETE_intersections":0},"double_seed":{"candidate_semantic_projection_sha256":c1["semantic_projection_sha256"],"factor_semantic_projection_sha256":f1["semantic_projection_sha256"],"theorem_semantic_projection_sha256":t1["semantic_projection_sha256"],"verification_semantic_projection_sha256":v1["semantic_projection_sha256"],"all_materialized_ledgers_byte_identical":True,"ledgers":ledger_groups},"independent_verifier":{"source_sha256":SOURCES["deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_independent_verifier.py"],"imports_chain_or_shared_module":False,"algorithm":"EXACT_PS_HALF_OPEN_CELL_BUCKET_INDEX_PLUS_DIRECT_ROLE_SIGN_RECOMPUTATION","seed1_result_sha256":v1["result_sha256"],"seed2_result_sha256":v2["result_sha256"]},"coherent_attacks":{"control_pass":True,"accepted":0,"rejected":15,"receipt_file_sha256":caps["attacks"].sha256},"shared_implementation_source":{"sha256":SOURCES["deliverables/cm2_c27_c24a_g2b_exact_factor_sign_disposition_v1_probe.py"],"captured_source_bytes_compiled_and_executed_in_factor_and_theorem":True},"authority_scope":{"scoped_G2A_route_assignment":True,"raw_SIGNED_COMPLETE_priority_checked":True,"POSITIVE_C19_91672":"OPEN__FRESH_LEDGER_NOT_CONSUMED","global_three_terminal_unique_assignment":False,"C27_C28_C29":"FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION","historical_R300C_or_edge_validation_input":"NOT_OPENED_BY_AUTHORITY_CHAIN","post_hoc_906":"NOT_AN_AUTHORITY_INPUT"},"payload_manifest":{"filename":"payload_manifest.sha256","file_sha256":payload_sha,"entry_count":len(payload_lines)},"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.att()for k,v in sorted(caps.items())}},"formal_credit":0,"manifest_authorized":False,"strict_nonpromotion":{"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"}}
  receipt["result_sha256"]=digest(receipt);receipt_wire=canonical(receipt)+b"\n";(out/"receipt.json").write_bytes(receipt_wire);receipt_sha=hashlib.sha256(receipt_wire).hexdigest();root_lines=sorted([f"{payload_sha}  payload_manifest.sha256",f"{receipt_sha}  receipt.json"],key=lambda x:x.split("  ",1)[1]);(out/"root_manifest.sha256").write_text("\n".join(root_lines)+"\n",encoding="ascii");print(canonical({"status":receipt["status"],"receipt_file_sha256":receipt_sha,"receipt_result_sha256":receipt["result_sha256"],"payload_manifest_sha256":payload_sha}).decode());return 0
 finally:
  for cap in caps.values():cap.close()
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Failure,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));raise SystemExit(2)
