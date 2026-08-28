#!/usr/bin/env python3
"""Independent full-row verifier for corrected Round306C1 candidates."""

from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import gzip,hashlib,json,os
from pathlib import Path
import stat,sys,tempfile
from typing import Any,Final,Iterator

class Rejected(RuntimeError):pass
def need(c:bool,label:str)->None:
    if type(c)is not bool or not c:raise Rejected(label)

ROOT:Final=Path(__file__).parent
PREFIX:Final="cm2_round306c1_source_g_corrected_identity_support_replay"
SCHEMA:Final="cm2.round306c1.source-g-corrected-identity-support-replay.v1"
PRODUCER:Final=PREFIX+"_producer.py"
ATTACK:Final=PREFIX+"_attack_suite.json"
VERIFICATION:Final=PREFIX+"_verification.json"
REPORT:Final=PREFIX+"_report.md"
COLD:Final=PREFIX+"_cold_replay.md"
MANIFEST:Final=PREFIX+"_manifest.sha256"
OUTPUTS:Final={"authority_frontier":PREFIX+"_authority_frontier.json","family_census":PREFIX+"_family_census.jsonl.gz","member":PREFIX+"_member_identity_support_ledger.jsonl.gz","representation":PREFIX+"_representation_ledger.jsonl.gz","physical_incidence":PREFIX+"_physical_incidence_statement_ledger.jsonl.gz","gap":PREFIX+"_semantic_gap_ledger.jsonl.gz","component_rebind":PREFIX+"_affected_component_rebind_ledger.jsonl.gz","transition_handle":PREFIX+"_transition_ready_handle_ledger.jsonl.gz","obligation_census":PREFIX+"_theorem_obligation_census.json","result":PREFIX+"_result.json"}
OUTPUT_ORDER:Final=tuple(OUTPUTS)
MANIFEST_MEMBERS:Final=(PRODUCER,*tuple(OUTPUTS.values()),Path(__file__).name,ATTACK,VERIFICATION,REPORT,COLD)
FAMILIES:Final=("PRESERVED","NON_GRAPH","R2","R292","G2A","G2B")
ZERO:Final={"normalized_support":0,"representation_cover":0,"A1_A2":0,"physical_incidence":0,"pullback_equivalence":0,"transition":0,"B1A":0,"B2":0,"maximality":0,"fibre":0,"global_disposition":0,"CM2":0}
EXPECTED_MEMBERS:Final={"PRESERVED":126_468,"NON_GRAPH":17_828,"R2":295_336,"R292":9_404,"G2A":38_608,"G2B":76_816}
EXPECTED_REPS:Final={"PRESERVED":165_744,"NON_GRAPH":17_828,"R2":302_624,"R292":10_252,"G2A":38_608,"G2B":76_816}
EXPECTED_REBINDS:Final={"PRESERVED":14_400,"NON_GRAPH":1_776,"R2":800,"R292":3_776,"G2A":584,"G2B":512}

@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
SOURCE_PINS:Final=(
Pin("C1_CONTRACT","cm2_round306c1_source_g_corrected_identity_support_replay_contract.py",63_460,"5724bff115289d3ace2a574b04028ce90842be0d629aa35c45fc9b1b8c85ad11"),Pin("C1_PREFLIGHT_SOURCE","cm2_round306c1_source_g_corrected_identity_support_migration_preflight.py",17_798,"f0acf40806ec9b7d7fa06edb98bc0709841f1136a5fa90b4c00118bfb2f6a63c"),Pin("C1_PREFLIGHT_RESULT","cm2_round306c1_source_g_corrected_identity_support_migration_preflight_result.json",6_698,"fc65ad5c78acddd61decbca9b9057cca0d6d59849ee3921c5433401cd581dacb"),Pin("C0_MANIFEST","cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256",2_182,"9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),Pin("C0_INVALIDATION","cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz",11_867,"865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),Pin("C0_ROOT_DISPOSITION","cm2_round306c0_source_g_r235d_corrected_fresh_freeze_base_root_disposition_ledger.jsonl.gz",115_696_187,"6c8e84a6f247a00470f4abd2b6bb7c4caff6ff813236c3e63f04b884998eccdb"),Pin("C0_MEMBER_COMPONENT","cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz",188_288_564,"81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),Pin("I4_MANIFEST","cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_manifest.sha256",2_176,"53b84967618f80c0781c6728ceef4f0e88df7862bd37c5f4cae4055caf960051"),Pin("I4_MEMBER","cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_member_ledger.jsonl.gz",245_580_399,"0fbdbbb35b833272429499c005e3d24eb1c669cd5d557898e72605668347b4c8"),Pin("I4_REPRESENTATION","cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_representation_ledger.jsonl.gz",162_325_503,"3adcddcf414d2aedc23dab6770cd11ba3dbcf1f911573d5686a7d287b7094712"),Pin("B1G0_MANIFEST","cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256",1_959,"6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),Pin("B1G0_GRAPH","cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz",11_720_893,"5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),Pin("B1G0_SHEET","cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz",13_922_080,"041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),Pin("B1G0_SIDE","cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz",25_932_945,"d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),Pin("B1G0_GAP","cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz",23_240_985,"2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),)
PRODUCER_PIN:Final=Pin("PRODUCER",PRODUCER,31_780,"6365ceba2301bbbbf2bc99b836264b4fc192c97242d89d64e88cd50bb0250fad")
PINS:Final=(*SOURCE_PINS,PRODUCER_PIN)

def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def objsha(v:Any)->str:return hashlib.sha256(canonical(v)).hexdigest()
def identity(i:os.stat_result)->tuple[int,...]:return(i.st_dev,i.st_ino,i.st_mode,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns)
def hashfd(fd:int)->str:
 os.lseek(fd,0,os.SEEK_SET);h=hashlib.sha256()
 while True:
  b=os.read(fd,1_048_576)
  if not b:return h.hexdigest()
  h.update(b)

class Sources:
 def __init__(self)->None:self.dirfd=-1;self.fds={};self.ids={}
 def __enter__(self)->"Sources":
  before=os.stat(ROOT,follow_symlinks=False);need(stat.S_ISDIR(before.st_mode)and not ROOT.is_symlink(),"root");self.dirfd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
  for p in PINS:
   i=os.stat(p.filename,dir_fd=self.dirfd,follow_symlinks=False);need(stat.S_ISREG(i.st_mode)and i.st_nlink==1 and i.st_size==p.size,"pin:"+p.role);fd=os.open(p.filename,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.dirfd);o=os.fstat(fd);need(identity(o)==identity(i),"race:"+p.role);need(hashfd(fd)==hashfd(fd)==p.sha256,"sha:"+p.role);self.fds[p.role]=fd;self.ids[p.role]=identity(o)
  return self
 def dup(self,r:str)->int:fd=os.dup(self.fds[r]);os.lseek(fd,0,os.SEEK_SET);return fd
 def final(self)->None:
  for p in reversed(PINS):need(identity(os.fstat(self.fds[p.role]))==self.ids[p.role] and identity(os.stat(p.filename,dir_fd=self.dirfd,follow_symlinks=False))==self.ids[p.role] and hashfd(self.fds[p.role])==p.sha256,"final:"+p.role)
 def __exit__(self,*_:Any)->None:
  for fd in self.fds.values():
   try:os.close(fd)
   except OSError:pass
  if self.dirfd>=0:os.close(self.dirfd)

def source_jsonl(s:Sources,r:str)->Iterator[dict[str,Any]]:
 fd=s.dup(r)
 try:
  with os.fdopen(fd,"rb",closefd=True)as raw,gzip.GzipFile(fileobj=raw,mode="rb")as g:
   for n,line in enumerate(g):v=json.loads(line);need(line.endswith(b"\n")and canonical(v)+b"\n"==line and type(v)is dict,"source row:"+r+":"+str(n));yield v
 finally:
  try:os.close(fd)
  except OSError:pass
def source_doc(s:Sources,r:str)->dict[str,Any]:
 fd=s.dup(r)
 try:
  with os.fdopen(fd,"rb",closefd=True)as raw,gzip.GzipFile(fileobj=raw,mode="rb")as g:v=json.load(g)
  need(type(v)is dict,"source doc:"+r);return v
 finally:
  try:os.close(fd)
  except OSError:pass

class Candidate:
 def __init__(self,path:Path)->None:self.path=Path(os.path.abspath(path));self.dirfd=-1;self.fds={};self.ids={};self.hashes={}
 def __enter__(self)->"Candidate":
  d=ROOT.resolve(strict=True);need(os.path.commonpath((str(self.path),str(d)))!=str(d),"candidate outside deliverables");before=os.stat(self.path,follow_symlinks=False);need(stat.S_ISDIR(before.st_mode),"candidate dir");self.dirfd=os.open(self.path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC);need(set(os.listdir(self.dirfd))==set(OUTPUTS.values()),"candidate exact set")
  for role in OUTPUT_ORDER:
   name=OUTPUTS[role];i=os.stat(name,dir_fd=self.dirfd,follow_symlinks=False);need(stat.S_ISREG(i.st_mode)and i.st_nlink==1,"candidate regular:"+role);fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.dirfd);o=os.fstat(fd);need(identity(o)==identity(i),"candidate race:"+role);h=hashfd(fd);need(h==hashfd(fd),"candidate two-pass:"+role);self.fds[role]=fd;self.ids[role]=identity(o);self.hashes[role]=h
  return self
 def raw(self,role:str)->bytes:
  fd=self.fds[role];os.lseek(fd,0,os.SEEK_SET);out=[]
  while True:
   b=os.read(fd,1_048_576)
   if not b:return b"".join(out)
   out.append(b)
 def rows(self,role:str)->Iterator[dict[str,Any]]:
  fd=os.dup(self.fds[role]);os.lseek(fd,0,os.SEEK_SET)
  try:
   with os.fdopen(fd,"rb",closefd=True)as raw,gzip.GzipFile(fileobj=raw,mode="rb")as g:
    for n,line in enumerate(g):v=json.loads(line);need(type(v)is dict and line.endswith(b"\n")and canonical(v)+b"\n"==line,"candidate canonical:"+role+":"+str(n));yield v
  finally:
   try:os.close(fd)
   except OSError:pass
 def final(self)->None:
  for role in reversed(OUTPUT_ORDER):need(identity(os.fstat(self.fds[role]))==self.ids[role] and identity(os.stat(OUTPUTS[role],dir_fd=self.dirfd,follow_symlinks=False))==self.ids[role] and hashfd(self.fds[role])==self.hashes[role],"candidate final:"+role)
 def __exit__(self,*_:Any)->None:
  for fd in self.fds.values():
   try:os.close(fd)
   except OSError:pass
  if self.dirfd>=0:os.close(self.dirfd)

class ManifestSnapshotCandidate:
 def __init__(self,snapshot:"ManifestSnapshot")->None:
  self.snapshot=snapshot;self.fds={r:snapshot.fds[OUTPUTS[r]]for r in OUTPUT_ORDER};self.ids={r:snapshot.ids[OUTPUTS[r]]for r in OUTPUT_ORDER};self.hashes={r:snapshot.hashes[OUTPUTS[r]]for r in OUTPUT_ORDER}
 def raw(self,role:str)->bytes:
  fd=self.fds[role];os.lseek(fd,0,os.SEEK_SET);out=[]
  while True:
   b=os.read(fd,1_048_576)
   if not b:return b"".join(out)
   out.append(b)
 def rows(self,role:str)->Iterator[dict[str,Any]]:
  fd=os.dup(self.fds[role]);os.lseek(fd,0,os.SEEK_SET)
  try:
   with os.fdopen(fd,"rb",closefd=True)as raw,gzip.GzipFile(fileobj=raw,mode="rb")as g:
    for n,line in enumerate(g):v=json.loads(line);need(type(v)is dict and line.endswith(b"\n")and canonical(v)+b"\n"==line,"published canonical:"+role+":"+str(n));yield v
  finally:
   try:os.close(fd)
   except OSError:pass
 def final(self)->None:self.snapshot.final_members()

class ManifestSnapshot:
 def __init__(self)->None:self.dirfd=-1;self.manifest_fd=-1;self.manifest_id=();self.fds={};self.ids={};self.hashes={}
 def __enter__(self)->"ManifestSnapshot":
  before=os.stat(ROOT,follow_symlinks=False);need(stat.S_ISDIR(before.st_mode)and not ROOT.is_symlink(),"manifest root");self.dirfd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
  mi=os.stat(MANIFEST,dir_fd=self.dirfd,follow_symlinks=False);need(stat.S_ISREG(mi.st_mode)and mi.st_nlink==1,"manifest regular");self.manifest_fd=os.open(MANIFEST,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.dirfd);mo=os.fstat(self.manifest_fd);need(identity(mo)==identity(mi),"manifest race");self.manifest_id=identity(mo)
  os.lseek(self.manifest_fd,0,os.SEEK_SET);raw=os.read(self.manifest_fd,mo.st_size);need(len(raw)==mo.st_size and raw.endswith(b"\n"),"manifest read")
  lines=raw.decode("ascii").splitlines();need(len(lines)==len(MANIFEST_MEMBERS),"manifest member count");declared=[]
  for line,name in zip(lines,MANIFEST_MEMBERS):
   parts=line.split("  ");need(len(parts)==2 and parts[1]==name and len(parts[0])==64,"manifest ordered member:"+name);int(parts[0],16);declared.append((name,parts[0]))
  for name,want in declared:
   i=os.stat(name,dir_fd=self.dirfd,follow_symlinks=False);need(stat.S_ISREG(i.st_mode)and i.st_nlink==1,"manifest member regular:"+name);fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.dirfd);o=os.fstat(fd);need(identity(o)==identity(i),"manifest member race:"+name);got=hashfd(fd);need(got==hashfd(fd)==want,"manifest member sha:"+name);self.fds[name]=fd;self.ids[name]=identity(o);self.hashes[name]=got
  return self
 def read(self,name:str)->bytes:
  fd=self.fds[name];os.lseek(fd,0,os.SEEK_SET);out=[]
  while True:
   b=os.read(fd,1_048_576)
   if not b:return b"".join(out)
   out.append(b)
 def final_members(self)->None:
  for name in reversed(MANIFEST_MEMBERS):need(identity(os.fstat(self.fds[name]))==self.ids[name] and identity(os.stat(name,dir_fd=self.dirfd,follow_symlinks=False))==self.ids[name] and hashfd(self.fds[name])==self.hashes[name],"manifest final member:"+name)
 def final(self)->None:
  self.final_members();need(identity(os.fstat(self.manifest_fd))==self.manifest_id and identity(os.stat(MANIFEST,dir_fd=self.dirfd,follow_symlinks=False))==self.manifest_id,"manifest final")
 def __exit__(self,*_:Any)->None:
  for fd in self.fds.values():
   try:os.close(fd)
   except OSError:pass
  if self.manifest_fd>=0:os.close(self.manifest_fd)
  if self.dirfd>=0:os.close(self.dirfd)

class Seq:
 def __init__(self)->None:self.h=hashlib.sha256();self.h.update(b"[");self.n=0
 def add(self,v:str)->None:
  if self.n:self.h.update(b",")
  self.h.update(canonical(v));self.n+=1
 def done(self)->str:c=self.h.copy();c.update(b"]");return c.hexdigest()
class Receipt:
 def __init__(self)->None:self.n=0;self.ids=Seq();self.hashes=Seq();self.rows=hashlib.sha256();self.stream=hashlib.sha256();self.size=0
 def add(self,row:dict[str,Any])->None:
  w=canonical(row)+b"\n";self.n+=1;self.ids.add(row["row_id"]);self.hashes.add(row["row_sha256"]);self.rows.update(w);self.stream.update(w);self.size+=len(w)
 def value(self)->dict[str,Any]:return{"row_count":self.n,"row_ids_sha256":self.ids.done(),"row_hashes_sha256":self.hashes.done(),"rows_sha256":self.rows.hexdigest(),"uncompressed_jsonl_sha256":self.stream.hexdigest(),"uncompressed_jsonl_size":self.size}
def make_row(kind:str,p:dict[str,Any])->dict[str,Any]:
 b={"schema":SCHEMA+"."+kind+"-row.v1",**p};rid="round306c1-"+kind+":"+objsha(b);r={**b,"row_id":rid};return{**r,"row_sha256":objsha(r)}
def ast(m:str,f:str)->dict[str,Any]:return{"ast_kind":"TYPED_FULL_SUPPORT_OBLIGATION","coarse_family":f,"member_id":m,"full_support_materialized":False,"outer_envelope_sufficient":False,"inner_witness_sufficient":False}
def grammar(f:str)->dict[str,Any]:return{"grammar":"C1_TYPED_SUPPORT_CERTIFICATE_V1","coarse_family":f,"requires":["SOURCE_AUTHORITY","A1_A2_WHERE_APPLICABLE","PHYSICAL_INCIDENCE_EQUIVALENCE","REPRESENTATION_PULLBACK"],"complete":False}
def commit(d:str,p:dict[str,Any])->str:return objsha({"domain":SCHEMA+"."+d,**p})
def compare_rows(candidate:Candidate,role:str,expected:Iterator[dict[str,Any]])->dict[str,Any]:
 receipt=Receipt();actual=candidate.rows(role)
 for n,want in enumerate(expected):
  try:got=next(actual)
  except StopIteration as e:raise Rejected("missing row:"+role+":"+str(n))from e
  need(got==want,"row mismatch:"+role+":"+str(n));receipt.add(got)
 try:next(actual)
 except StopIteration:return receipt.value()
 raise Rejected("extra row:"+role)

def closed_document(c:Candidate,role:str,field:str)->dict[str,Any]:
 raw=c.raw(role);v=json.loads(raw);need(type(v)is dict and canonical(v)==raw,"candidate document canonical:"+role);body=dict(v);claimed=body.pop(field,None);need(type(claimed)is str and claimed==objsha(body),"candidate document closure:"+role);return v

def candidate_document_preflight(c:Candidate,frontier:dict[str,Any],obligation:dict[str,Any],producer_commit:dict[str,Any])->dict[str,Any]:
 got_frontier=closed_document(c,"authority_frontier","authority_frontier_sha256");need(got_frontier==frontier,"authority frontier")
 got_obligation=closed_document(c,"obligation_census","obligation_census_sha256");need(got_obligation==obligation,"obligation")
 result=closed_document(c,"result","result_sha256");need(result["producer_source"]==producer_commit,"result producer pin");need(result["authority_frontier_sha256"]==frontier["authority_frontier_sha256"],"result authority pin")
 need(result["corrected_census"]=={"member_count":564_460,"representation_count":611_872,"physical_incidence_count":115_424,"semantic_gap_count":154_032,"affected_component_rebind_count":21_848,"transition_handle_count":564_460,"family_member_counts":EXPECTED_MEMBERS,"family_representation_counts":EXPECTED_REPS},"result corrected census")
 need(result["valid_side_reference_count"]==76_832 and result["unique_side_member_count"]==76_816 and result["duplicate_side_reference_excess"]==16,"result side census");need(result["formal_credit"]==ZERO and result["normalized_support_sealed"]is False and result["B1A_permitted"]is False and result["B2_permitted"]is False and result["CM2"]=="NO-GO_FOR_CLAIM","result zero credit")
 desc=result["output_artifacts_in_publication_order_before_result"];need([x["role"]for x in desc]==list(OUTPUT_ORDER[:-1]),"descriptor order")
 for item in desc:
  role=item["role"];need(item=={"role":role,"filename":OUTPUTS[role],"size":c.ids[role][4],"sha256":c.hashes[role]},"descriptor:"+role)
 return result

def verify(s:Sources,c:Candidate)->dict[str,Any]:
 invalid=sorted(r["registry_member_id"]for r in source_jsonl(s,"C0_INVALIDATION"));invalid_set=set(invalid);need(len(invalid_set)==32,"invalid")
 rekey=set(r["old_component_id"]for r in source_jsonl(s,"C0_ROOT_DISPOSITION")if r["disposition"]=="REKEY_ROOT");need(len(rekey)==4,"rekey")
 c0={}
 for r in source_jsonl(s,"C0_MEMBER_COMPONENT"):c0[r["registry_member_id"]]=(r["corrected_component_id"],r["row_id"],r["row_sha256"])
 need(len(c0)==564_460,"c0")
 producer_commit={"filename":PRODUCER,"size":PRODUCER_PIN.size,"sha256":PRODUCER_PIN.sha256}
 frontier_body={"schema":SCHEMA+".authority-frontier.v1","producer_source":producer_commit,"source_precedence":["SEALED_C0_CORRECTED_MEMBER_COMPONENT_AUTHORITY","DIRECT_I0_I1_I2_I3_IDENTITY_PROVENANCE_VIA_I4_MIGRATION_ROWS","B1G0_GRAPH_INCIDENCE_STATEMENTS_MIGRATION_ONLY","C1_NEW_ROWS_ZERO_CREDIT"],"pins":[p.__dict__ for p in SOURCE_PINS],"old_component_ids_are_provenance_only":True,"old_I4_or_B1G0_rows_have_formal_support_authority":False};frontier={**frontier_body,"authority_frontier_sha256":objsha(frontier_body)}
 obligation_body={"schema":SCHEMA+".theorem-obligation-census.v1","status":"EXACT_OBLIGATION_CENSUS_NOT_FEATURE_LEDGER_ROWS","root":{"preserved_non_graph_A1_A2":17_940,"R2_predicate_cells":295_340,"G2_graph_definitions":38_608,"total":351_888},"dependent":{"preserved_non_graph_A1_A2":62_152,"R2_member_pullbacks":295_336,"G2_graph_sheet_identifications":38_608,"G2_graph_side_incidences":76_816,"total":472_912},"corrected_total":824_800,"known_final_feature_ledger_row_count":None,"formal_credit":dict(ZERO)};obligation={**obligation_body,"obligation_census_sha256":objsha(obligation_body)};candidate_document_preflight(c,frontier,obligation,producer_commit)
 member_refs={};member_counts=Counter();member_ids={f:Seq()for f in FAMILIES};member_sources={f:Seq()for f in FAMILIES};missing=[]
 def expected_members()->Iterator[dict[str,Any]]:
  for old in source_jsonl(s,"I4_MEMBER"):
   f=old["coarse_family"];m=old["member_id"]
   if m not in c0:missing.append(m);continue
   component,c0row,c0sha=c0[m];ci=old["canonical_input_commitment"];a=ast(m,f);cert=grammar(f);ic=commit("member-input.v1",{"legacy_I4_row_sha256":old["row_sha256"],"member_id":m,"family":f,"c0_member_row_sha256":c0sha,"producer_sha256":PRODUCER_PIN.sha256});p={"member_id":m,"coarse_family":f,"primitive_source_kind":f+"_PRIMITIVE_SOURCE","source_authority_role":"I4_MIGRATION_REFERENCE_TO_"+ci["source_lane"],"source_filename":ci["source_member_file"],"source_table":"JSONL_MEMBER_INDEX","source_path":"/member_id/"+m,"source_row_id":m,"source_row_sha256":old["row_sha256"],"r235d_disposition":"SURVIVES_C0_CORRECTED_MEMBER_UNIVERSE","c0_member_component_row_id":c0row,"c0_member_component_row_sha256":c0sha,"corrected_component_id":component,"typed_support_ast":a,"certificate_grammar":cert,"mechanical_representation_count":old["mechanical_representation_count"],"mechanical_representation_ids_sha256":old["mechanical_representation_set_sha256"],"primary_mechanical_representation_id":old["primary_mechanical_representation_id"],"support_semantic_state":"MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED","canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)};row=make_row("member-identity-support",p);member_refs[m]={"family":f,"row_id":row["row_id"],"row_sha256":row["row_sha256"],"component":component,"ast_sha":objsha(a),"rep_sha":old["mechanical_representation_set_sha256"],"old_component":old["Round306A_component_id"],"old_row_sha":old["row_sha256"],"c0row":c0row,"c0sha":c0sha};member_counts[f]+=1;member_ids[f].add(m);member_sources[f].add(old["row_sha256"]);yield row
 receipts={"member":compare_rows(c,"member",expected_members())};need(sorted(missing)==invalid and dict(member_counts)==EXPECTED_MEMBERS,"member census")
 rep_counts=Counter();rep_ids={f:Seq()for f in FAMILIES};rep_sources={f:Seq()for f in FAMILIES}
 def expected_reps()->Iterator[dict[str,Any]]:
  for old in source_jsonl(s,"I4_REPRESENTATION"):
   owner=old["owner_member_id"]
   if owner not in member_refs:continue
   f=old["coarse_family"];ci=old["canonical_input_commitment"];o=member_refs[owner];rid=old["representation_id"];ic=commit("representation-input.v1",{"legacy_I4_row_sha256":old["row_sha256"],"representation_id":rid,"owner_member_id":owner,"owner_member_row_sha256":o["row_sha256"],"producer_sha256":PRODUCER_PIN.sha256});p={"representation_id":rid,"owner_member_id":owner,"coarse_family":f,"representation_role":old["representation_role"],"source_authority_role":"I4_MIGRATION_REFERENCE_TO_"+ci["source_lane"],"source_filename":ci["source_representation_file"],"source_table":"JSONL_REPRESENTATION_INDEX","source_path":"/representation_id/"+rid,"source_row_id":rid,"source_row_sha256":old["row_sha256"],"typed_representation_ast":{"ast_kind":"TYPED_MECHANICAL_REPRESENTATION","representation_id":rid,"owner_member_id":owner,"role":old["representation_role"]},"certificate_grammar":grammar(f),"pullback_semantic_state":"PULLBACK_EQUIVALENCE_NOT_PROVED","owner_member_row_id":o["row_id"],"owner_member_row_sha256":o["row_sha256"],"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)};rep_counts[f]+=1;rep_ids[f].add(rid);rep_sources[f].add(old["row_sha256"]);yield make_row("representation",p)
 receipts["representation"]=compare_rows(c,"representation",expected_reps());need(dict(rep_counts)==EXPECTED_REPS,"rep census")
 def expected_families()->Iterator[dict[str,Any]]:
  for f in FAMILIES:
   src=objsha({"member_source_rows_sha256":member_sources[f].done(),"representation_source_rows_sha256":rep_sources[f].done()});ic=commit("family-input.v1",{"family":f,"member_count":member_counts[f],"representation_count":rep_counts[f],"source_authority_commitment_sha256":src});yield make_row("family-census",{"coarse_family":f,"member_count":member_counts[f],"representation_count":rep_counts[f],"member_ids_sha256":member_ids[f].done(),"representation_ids_sha256":rep_ids[f].done(),"source_authority_commitment_sha256":src,"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)})
 receipts["family_census"]=compare_rows(c,"family_census",expected_families())
 graph=source_doc(s,"B1G0_GRAPH")["graph_source_inventory_rows"];gmap={r["Round306B1G0_graph_source_inventory_row_id"]:r for r in graph};sheet=[r for r in source_doc(s,"B1G0_SHEET")["graph_sheet_join_rows"]if r["sheet_member_id"]in member_refs];side_by={};valid_side=0
 for r in source_doc(s,"B1G0_SIDE")["graph_side_join_rows"]:
  m=r["side_member_id"]
  if m not in member_refs:continue
  valid_side+=1;prior=side_by.get(m)
  if prior is None or r["Round306B1G0_graph_side_join_row_id"]<prior["Round306B1G0_graph_side_join_row_id"]:side_by[m]=r
 need(len(sheet)==38_608 and valid_side==76_832 and len(side_by)==76_816,"incidence selection");inc_refs={}
 def incidence(old:dict[str,Any],member:str,role:str,family:str,source_key:str,state:str)->dict[str,Any]:
  m=member_refs[member];g=gmap[old["graph_source_inventory_row_id"]];sid=old[source_key];ic=commit("incidence-input.v1",{"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_sha256":old["row_sha256"],"member_row_sha256":m["row_sha256"]});node={"ast_kind":"GRAPH_SHEET_INCIDENCE_STATEMENT"if role=="GRAPH_TO_SHEET"else"GRAPH_SIDE_INCIDENCE_STATEMENT","graph_id":old["graph_id"],"member_id":member,"proved":False};
  if role=="GRAPH_TO_SIDE":node["side_role"]=old["side_role"]
  row=make_row("physical-incidence-statement",{"graph_id":old["graph_id"],"incidence_role":role,"member_id":member,"coarse_family":family,"source_graph_row_id":g["Round306B1G0_graph_source_inventory_row_id"],"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_id":sid,"source_incidence_row_sha256":old["row_sha256"],"member_row_id":m["row_id"],"member_row_sha256":m["row_sha256"],"incidence_statement_ast":node,"theorem_semantic_state":state,"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)});inc_refs[sid]={"row_id":row["row_id"],"row_sha256":row["row_sha256"]};return row
 def expected_inc()->Iterator[dict[str,Any]]:
  for r in sheet:yield incidence(r,r["sheet_member_id"],"GRAPH_TO_SHEET","G2A","Round306B1G0_graph_sheet_join_row_id","PHYSICAL_IDENTIFICATION_THEOREM_PENDING")
  for m in sorted(side_by):yield incidence(side_by[m],m,"GRAPH_TO_SIDE","G2B","Round306B1G0_graph_side_join_row_id","POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING")
 receipts["physical_incidence"]=compare_rows(c,"physical_incidence",expected_inc())
 ordinary=[];side_gaps={}
 for r in source_doc(s,"B1G0_GAP")["gap_rows"]:
  m=r["member_id"]
  if m not in member_refs:continue
  if r["gap_kind"]=="GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING":
   if r["incidence_join_row_id"]!=side_by[m]["Round306B1G0_graph_side_join_row_id"]:continue
   prior=side_gaps.get(m)
   if prior is None or r["Round306B1G0_gap_row_id"]<prior["Round306B1G0_gap_row_id"]:side_gaps[m]=r
  else:ordinary.append(r)
 gaps=ordinary+[side_gaps[m]for m in sorted(side_gaps)];gaps.sort(key=lambda r:(FAMILIES.index(member_refs[r["member_id"]]["family"]),r["Round306B1G0_gap_row_id"]));need(len(gaps)==154_032,"gap selection")
 def expected_gaps()->Iterator[dict[str,Any]]:
  for old in gaps:
   m=member_refs[old["member_id"]];src=old["incidence_join_row_id"]
   if src is None:kind="GRAPH_DEFINITION";subject=old["graph_source_inventory_row_id"]
   else:kind="PHYSICAL_INCIDENCE";need(src in inc_refs,"gap incidence");subject=inc_refs[src]["row_id"]
   ic=commit("gap-input.v1",{"source_gap_row_sha256":old["row_sha256"],"subject_row_id":subject,"member_row_sha256":m["row_sha256"]});yield make_row("semantic-gap",{"gap_kind":old["gap_kind"],"subject_kind":kind,"subject_row_id":subject,"member_id":old["member_id"],"coarse_family":m["family"],"required_closure":old["required_closure"],"source_statement_row_id":old["Round306B1G0_gap_row_id"],"source_statement_row_sha256":old["row_sha256"],"blocking_credit_kinds":["normalized_support","physical_incidence","representation_cover","B1A"],"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)})
 receipts["gap"]=compare_rows(c,"gap",expected_gaps());rebind_counts=Counter()
 def expected_rebind()->Iterator[dict[str,Any]]:
  for member,m in member_refs.items():
   if m["old_component"]not in rekey:continue
   rebind_counts[m["family"]]+=1;ic=commit("rebind-input.v1",{"member_id":member,"old_component_id":m["old_component"],"c0_member_row_sha256":m["c0sha"],"corrected_component_id":m["component"]});yield make_row("affected-component-rebind",{"member_id":member,"coarse_family":m["family"],"old_component_id_provenance_only":m["old_component"],"old_component_row_sha256":m["old_row_sha"],"c0_member_component_row_id":m["c0row"],"c0_member_component_row_sha256":m["c0sha"],"corrected_component_id":m["component"],"rebind_reason":"SURVIVOR_OF_R235D_AFFECTED_OLD_COMPONENT_REBOUND_TO_FRESH_C0_COMPONENT","canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)})
 receipts["component_rebind"]=compare_rows(c,"component_rebind",expected_rebind());need(dict(rebind_counts)==EXPECTED_REBINDS,"rebind counts")
 def expected_handles()->Iterator[dict[str,Any]]:
  for member,m in member_refs.items():
   ic=commit("transition-handle-input.v1",{"member_id":member,"member_row_sha256":m["row_sha256"],"typed_support_ast_sha256":m["ast_sha"],"representation_set_sha256":m["rep_sha"],"corrected_component_id":m["component"]});yield make_row("transition-ready-handle",{"member_id":member,"coarse_family":m["family"],"member_row_id":m["row_id"],"member_row_sha256":m["row_sha256"],"typed_support_ast_sha256":m["ast_sha"],"representation_set_sha256":m["rep_sha"],"corrected_component_id":m["component"],"transition_syntax_ready":True,"transition_semantics_ready":False,"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)})
 receipts["transition_handle"]=compare_rows(c,"transition_handle",expected_handles())
 descriptors=[{"role":r,"filename":OUTPUTS[r],"size":c.ids[r][4],"sha256":c.hashes[r]}for r in OUTPUT_ORDER[:-1]]
 result_body={"schema":SCHEMA+".result.v1","status":"PASS_CORRECTED_SIX_FAMILY_MECHANICAL_REPLAY_CANDIDATE__ZERO_SUPPORT_CREDIT","producer_source":producer_commit,"authority_frontier_sha256":frontier["authority_frontier_sha256"],"corrected_census":{"member_count":564_460,"representation_count":611_872,"physical_incidence_count":115_424,"semantic_gap_count":154_032,"affected_component_rebind_count":21_848,"transition_handle_count":564_460,"family_member_counts":dict(member_counts),"family_representation_counts":dict(rep_counts)},"exact_C0_invalid_member_ids_sha256":objsha(invalid),"valid_side_reference_count":valid_side,"unique_side_member_count":len(side_by),"duplicate_side_reference_excess":valid_side-len(side_by),"ledger_receipts":receipts,"output_artifacts_in_publication_order_before_result":descriptors,"formal_credit":dict(ZERO),"normalized_support_sealed":False,"B1A_permitted":False,"B2_permitted":False,"CM2":"NO-GO_FOR_CLAIM","seed_serialized_or_semantically_used":False};result={**result_body,"result_sha256":objsha(result_body)};need(json.loads(c.raw("result"))==result,"result exact");c.final();s.final()
 return{"status":"PASS_INDEPENDENT_C1_FULL_2032102_ROW_REPLAY__ZERO_SUPPORT_CREDIT","artifact_count":10,"candidate_artifact_sha256":dict(c.hashes),"row_count":sum(v["row_count"]for v in receipts.values()),"ledger_receipts":receipts,"corrected_member_count":564_460,"corrected_representation_count":611_872,"physical_incidence_count":115_424,"semantic_gap_count":154_032,"affected_component_rebind_count":21_848,"producer_imported_or_executed":False,"formal_credit":dict(ZERO)}

def self_sha()->str:
 path=Path(__file__);i=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(i.st_mode)and i.st_nlink==1,"verifier source");fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 try:need(identity(os.fstat(fd))==identity(i),"verifier source race");a=hashfd(fd);need(a==hashfd(fd),"verifier source digest");return a
 finally:os.close(fd)
def copy_file(src:Path,dst:Path)->None:
 s=os.open(src,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);d=os.open(dst,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
 try:
  while os.copy_file_range(s,d,8_388_608):pass
 finally:os.close(s);os.close(d)
def clone_candidate(source:Path)->Path:
 parent=Path("/tmp/cm2-round306c1-verifier-attacks");parent.mkdir(mode=0o700,parents=True,exist_ok=True);path=Path(tempfile.mkdtemp(prefix="attack.",dir=parent))
 for role in OUTPUT_ORDER:copy_file(source/OUTPUTS[role],path/OUTPUTS[role])
 return path
def remove_tree(path:Path)->None:
 for e in path.iterdir():e.unlink()
 path.rmdir()
def rewrite_closed(path:Path,field:str,mutate:Any)->None:
 v=json.loads(path.read_bytes());mutate(v);body=dict(v);body.pop(field,None);v[field]=objsha(body);path.write_bytes(canonical(v))
def attack_suite(source_path:Path)->dict[str,Any]:
 with Sources()as s,Candidate(source_path)as c:baseline=verify(s,c)
 work=clone_candidate(source_path);attacks=[]
 def restore(role:str)->None:
  p=work/OUTPUTS[role]
  if p.exists()or p.is_symlink():p.unlink()
  copy_file(source_path/OUTPUTS[role],p)
 def execute(aid:str,mutate:Any,rest:Any)->None:
  try:
   mutate()
   try:
    with Sources()as s,Candidate(work)as c:verify(s,c)
   except (Rejected,gzip.BadGzipFile,EOFError,OSError,json.JSONDecodeError) as e:boundary=type(e).__name__+":"+str(e)
   else:raise Rejected("attack accepted:"+aid)
   body={"attack_id":aid,"rejected":True,"rejection_boundary":boundary};attacks.append({**body,"row_sha256":objsha(body)})
  finally:rest()
 execute("A01_EXTRA_FILE",lambda:(work/"foreign").write_bytes(b"x"),lambda:(work/"foreign").unlink())
 execute("A02_MISSING_RESULT",lambda:(work/OUTPUTS["result"]).unlink(),lambda:restore("result"))
 execute("A03_RESULT_SYMLINK",lambda:((work/OUTPUTS["result"]).unlink(),(work/OUTPUTS["result"]).symlink_to(source_path/OUTPUTS["result"])),lambda:restore("result"))
 execute("A04_HARDLINK_AUTHORITY",lambda:((work/OUTPUTS["result"]).unlink(),os.link(work/OUTPUTS["authority_frontier"],work/OUTPUTS["result"])),lambda:restore("result"))
 execute("A05_AUTHORITY_PRODUCER_PIN",lambda:rewrite_closed(work/OUTPUTS["authority_frontier"],"authority_frontier_sha256",lambda d:d["producer_source"].__setitem__("sha256","0"*64)),lambda:restore("authority_frontier"))
 execute("A06_OBLIGATION_AS_FEATURE_COUNT",lambda:rewrite_closed(work/OUTPUTS["obligation_census"],"obligation_census_sha256",lambda d:d.__setitem__("corrected_total",824_864)),lambda:restore("obligation_census"))
 fields=("member_count","representation_count","physical_incidence_count","semantic_gap_count","affected_component_rebind_count")
 for n,field in enumerate(fields,7):execute("A"+str(n).zfill(2)+"_RESULT_"+field.upper(),lambda f=field:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["corrected_census"].__setitem__(f,d["corrected_census"][f]+1)),lambda:restore("result"))
 execute("A12_CREDIT_INJECTION",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["formal_credit"].__setitem__("normalized_support",1)),lambda:restore("result"))
 execute("A13_DESCRIPTOR_SUBSTITUTION",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["output_artifacts_in_publication_order_before_result"][0].__setitem__("sha256","0"*64)),lambda:restore("result"))
 for n,role in enumerate(("family_census","member","representation","physical_incidence","gap","component_rebind","transition_handle"),14):
  def corrupt(r:str=role)->None:
   p=work/OUTPUTS[r];fd=os.open(p,os.O_WRONLY)
   try:os.pwrite(fd,b"X",0)
   finally:os.close(fd)
   h=hashlib.sha256(p.read_bytes()).hexdigest();rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:next(x for x in d["output_artifacts_in_publication_order_before_result"]if x["role"]==r).__setitem__("sha256",h))
  execute("A"+str(n).zfill(2)+"_CORRUPT_"+role.upper(),corrupt,lambda r=role:(restore(r),restore("result")))
 need(len(attacks)==20,"attack count");remove_tree(work);body={"schema":SCHEMA+".coherent-attack-suite.v1","status":"PASS_20_OF_20_COHERENT_ATTACKS_REJECTED","verifier_filename":Path(__file__).name,"verifier_file_sha256":self_sha(),"attack_count":20,"rejected_count":20,"all_rejected":True,"baseline_candidate_artifact_sha256":baseline["candidate_artifact_sha256"],"attacks":attacks};return{**body,"attack_suite_sha256":objsha(body)}
def read_attack()->tuple[dict[str,Any],str]:
 p=ROOT/ATTACK;i=os.stat(p,follow_symlinks=False);need(stat.S_ISREG(i.st_mode)and i.st_nlink==1,"attack regular");raw=p.read_bytes();v=json.loads(raw);need(canonical(v)==raw,"attack canonical");body=dict(v);claimed=body.pop("attack_suite_sha256");need(claimed==objsha(body)and v["verifier_file_sha256"]==self_sha()and(v["attack_count"],v["rejected_count"],v["all_rejected"])==(20,20,True),"attack closure");return v,hashlib.sha256(raw).hexdigest()
def verification_doc_from(receipt:dict[str,Any],a:dict[str,Any],h:str)->dict[str,Any]:
 body={"schema":SCHEMA+".verification.v1",**receipt,"attack_suite":{"filename":ATTACK,"file_sha256":h,"object_self_sha256":a["attack_suite_sha256"],"attack_count":20,"rejected_count":20,"all_rejected":True},"formal_credit_marker":{"mechanical_replay_verified":True,"normalized_support":0,"B1A":0,"B2":0,"CM2":0}};return{**body,"verification_sha256":objsha(body)}
def verification_doc(receipt:dict[str,Any])->dict[str,Any]:
 a,h=read_attack();return verification_doc_from(receipt,a,h)
def manifest_first()->dict[str,Any]:
 with ManifestSnapshot()as snapshot,Sources()as s:
  need(snapshot.hashes[Path(__file__).name]==self_sha(),"manifest verifier self pin");candidate=ManifestSnapshotCandidate(snapshot);receipt=verify(s,candidate)
  attack_raw=snapshot.read(ATTACK);attack=json.loads(attack_raw);need(canonical(attack)==attack_raw,"manifest attack canonical");body=dict(attack);claimed=body.pop("attack_suite_sha256",None);need(claimed==objsha(body)and attack["verifier_file_sha256"]==snapshot.hashes[Path(__file__).name]and(attack["attack_count"],attack["rejected_count"],attack["all_rejected"])==(20,20,True),"manifest attack closure")
  expected=verification_doc_from(receipt,attack,hashlib.sha256(attack_raw).hexdigest());need(snapshot.read(VERIFICATION)==canonical(expected),"manifest verification byte identity");s.final();snapshot.final()
  return{"status":"PASS_MANIFEST_FIRST_HELD_FD_FULL_2032102_ROW_REPLAY__ZERO_WRITES_ZERO_SUPPORT_CREDIT","manifest_filename":MANIFEST,"manifest_member_count":len(MANIFEST_MEMBERS),"verified_row_count":receipt["row_count"],"candidate_artifact_sha256":receipt["candidate_artifact_sha256"],"deliverables_write_syscalls":0,"formal_credit":dict(ZERO)}

def main()->int:
 need(type(sys.flags.isolated)is int and sys.flags.isolated==1,"python -I");need(sys.dont_write_bytecode is True,"python -B");p=argparse.ArgumentParser(description=__doc__);p.add_argument("--candidate-dir");p.add_argument("--verify-publish",action="store_true");p.add_argument("--verify-no-write",action="store_true");p.add_argument("--attack-publish",action="store_true");p.add_argument("--manifest-first-no-write",action="store_true");a=p.parse_args();need(sum((a.verify_publish,a.verify_no_write,a.attack_publish,a.manifest_first_no_write))==1,"one mode")
 if a.manifest_first_no_write:receipt=manifest_first()
 elif a.attack_publish:
  need(a.candidate_dir is not None,"candidate required")
  suite=attack_suite(Path(a.candidate_dir));path=ROOT/ATTACK;need(not path.exists(),"attack no-clobber");fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
  try:os.write(fd,canonical(suite));os.fsync(fd)
  finally:os.close(fd)
  receipt={"status":suite["status"],"attack_count":20,"attack_suite_sha256":suite["attack_suite_sha256"]}
 else:
  need(a.candidate_dir is not None,"candidate required")
  with Sources()as s,Candidate(Path(a.candidate_dir))as c:receipt=verify(s,c)
 if a.verify_publish:
  doc=verification_doc(receipt);path=ROOT/VERIFICATION;need(not path.exists(),"verification no-clobber");fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
  try:os.write(fd,canonical(doc));os.fsync(fd)
  finally:os.close(fd)
 print(json.dumps(receipt,sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
