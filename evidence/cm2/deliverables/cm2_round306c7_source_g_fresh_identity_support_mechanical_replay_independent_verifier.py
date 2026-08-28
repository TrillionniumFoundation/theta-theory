#!/usr/bin/env python3
"""Independent full-row verifier for Round306C7 fresh replay candidates."""

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
PREFIX:Final="cm2_round306c7_source_g_fresh_identity_support_mechanical_replay"
SCHEMA:Final="cm2.round306c7.source-g-fresh-identity-support-mechanical-replay.v1"
PRODUCER:Final=PREFIX+"_producer.py"
ATTACK:Final=PREFIX+"_attack_suite.json"
VERIFICATION:Final=PREFIX+"_verification.json"
REPORT:Final=PREFIX+"_report.md"
COLD:Final=PREFIX+"_cold_replay.md"
MANIFEST:Final=PREFIX+"_manifest.sha256"
OUTPUTS:Final={"family_census":PREFIX+"_family_census.jsonl.gz","member":PREFIX+"_member_identity_support_ledger.jsonl.gz","representation":PREFIX+"_representation_ledger.jsonl.gz","physical_incidence":PREFIX+"_physical_incidence_statement_ledger.jsonl.gz","gap":PREFIX+"_semantic_gap_ledger.jsonl.gz","component_rebind":PREFIX+"_component_rebind_ledger.jsonl.gz","transition_handle":PREFIX+"_transition_ready_handle_ledger.jsonl.gz","result":PREFIX+"_result.json"}
OUTPUT_ORDER:Final=tuple(OUTPUTS)
MANIFEST_MEMBERS:Final=(PRODUCER,*tuple(OUTPUTS.values()),Path(__file__).name,ATTACK,VERIFICATION,REPORT,COLD)
FAMILIES:Final=("PRESERVED","NON_GRAPH","R2","R292","G2A","G2B")
ZERO:Final={"normalized_support":0,"representation_cover":0,"A1_A2":0,"physical_incidence":0,"pullback_equivalence":0,"transition":0,"B1A":0,"B2":0,"maximality":0,"fibre":0,"global_disposition":0,"CM2":0}
EXPECTED_MEMBERS:Final={"PRESERVED":126_468,"NON_GRAPH":51_172,"R2":295_336,"R292":9_404,"G2A":5_264,"G2B":10_128}
EXPECTED_REPS:Final={"PRESERVED":165_744,"NON_GRAPH":51_172,"R2":302_624,"R292":10_252,"G2A":5_264,"G2B":10_128}
EXPECTED_PHYSICAL:Final={"G2A":5_264,"G2B":10_128}

@dataclass(frozen=True)
class Pin:role:str;filename:str;size:int;sha256:str
SOURCE_PINS:Final=(
Pin("C1_MANIFEST","cm2_round306c1_source_g_corrected_identity_support_replay_manifest.sha256",2_398,"9adfc1499f2c376085b1e7166cce43e41374ac81f4f10ad87409b0d9b14e4b7c"),
Pin("C1_RESULT","cm2_round306c1_source_g_corrected_identity_support_replay_result.json",6_534,"fc23235883e7c97dd63e1324114b9e8a17e21c3ec9383e6bfab60a078215ea09"),
Pin("C1_MEMBER","cm2_round306c1_source_g_corrected_identity_support_replay_member_identity_support_ledger.jsonl.gz",245_137_577,"7833d0bf74b3252a4258695972b4e92845defb2640dace6b9bd1850a0db89497"),
Pin("C1_REPRESENTATION","cm2_round306c1_source_g_corrected_identity_support_replay_representation_ledger.jsonl.gz",217_157_865,"2cc7f2baa97d0cc0579663d5ab7d67c17eb0f9aaccb1489e5c8073382118fd94"),
Pin("C1_INCIDENCE","cm2_round306c1_source_g_corrected_identity_support_replay_physical_incidence_statement_ledger.jsonl.gz",53_797_275,"9cb4ed9467f13f0cec9199a5ad29b716457465bc1c6fb2a77bbaa7aba2a27f04"),
Pin("C1_GAP","cm2_round306c1_source_g_corrected_identity_support_replay_semantic_gap_ledger.jsonl.gz",43_187_989,"feb43759887a642a1d00350218015c801d1a8e1d0b410aa873db3415d9913aa3"),
Pin("C1_HANDLE","cm2_round306c1_source_g_corrected_identity_support_replay_transition_ready_handle_ledger.jsonl.gz",203_902_224,"6511933445169756b8d409d3a8dd57cfd1b894a77e758f301481679ea31306f9"),
Pin("C4_MANIFEST","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256",1_177,"5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
Pin("C4_RESULT","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_result.json",6_204,"1396fadf4ef85340bdc0b1ca3b191a67a8266ed40cc3ee9a3dcc8f9650ffb8da"),
Pin("C4_BRIDGE","cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz",101_147,"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
Pin("C5_MANIFEST","cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256",1_193,"aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
Pin("C5_RESULT","cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_result.json",6_975,"0da7931e1a46d68ae8da69a7de1534a3955c83a8d6f5d8ab0170be7a34dc6320"),
Pin("C5_SEMANTIC","cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz",78_082_824,"8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
Pin("C6_MANIFEST","cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256",2_211,"d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
Pin("C6_RESULT","cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_result.json",9_329,"3f4e3e666dfe0b5b3a163c866057031b42dac09000175f4bc0b32ec353c5e4c5"),
Pin("C6_MEMBER","cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz",213_125_489,"730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),)
PRODUCER_PIN:Final=Pin("PRODUCER",PRODUCER,38_123,"010dc3732ea843decb01b8249df2e538f9000e9cf1c8047e954328cabd8a7f48")
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
   for n,line in enumerate(g):
    v=json.loads(line);need(line.endswith(b"\n")and canonical(v)+b"\n"==line and type(v)is dict,"source row:"+r+":"+str(n));body={k:x for k,x in v.items()if k!="row_sha256"};need(type(v.get("row_sha256"))is str and objsha(body)==v["row_sha256"],"source closure:"+r+":"+str(n));yield v
 finally:
  try:os.close(fd)
  except OSError:pass
def source_plain(s:Sources,r:str)->dict[str,Any]:
 fd=s.dup(r)
 try:
  with os.fdopen(fd,"rb",closefd=True)as raw:data=raw.read()
  v=json.loads(data);need(type(v)is dict and canonical(v)==data,"source doc:"+r);return v
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
    for n,line in enumerate(g):
     v=json.loads(line);need(type(v)is dict and line.endswith(b"\n")and canonical(v)+b"\n"==line,"candidate canonical:"+role+":"+str(n));body={k:x for k,x in v.items()if k!="row_sha256"};need(type(v.get("row_id"))is str and type(v.get("row_sha256"))is str and objsha(body)==v["row_sha256"],"candidate closure:"+role+":"+str(n));yield v
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
    for n,line in enumerate(g):
     v=json.loads(line);need(type(v)is dict and line.endswith(b"\n")and canonical(v)+b"\n"==line,"published canonical:"+role+":"+str(n));body={k:x for k,x in v.items()if k!="row_sha256"};need(type(v.get("row_id"))is str and type(v.get("row_sha256"))is str and objsha(body)==v["row_sha256"],"published closure:"+role+":"+str(n));yield v
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
 b={"schema":SCHEMA+"."+kind+"-row.v1",**p};rid="round306c7-"+kind+":"+objsha(b);r={**b,"row_id":rid};return{**r,"row_sha256":objsha(r)}
def ast(m:str,f:str)->dict[str,Any]:return{"ast_kind":"TYPED_FULL_SUPPORT_OBLIGATION","coarse_family":f,"member_id":m,"fresh_member_universe":"ROUND306C6","full_support_materialized":False,"outer_envelope_sufficient":False,"inner_witness_sufficient":False}
def grammar(f:str)->dict[str,Any]:return{"grammar":"C7_FRESH_TYPED_SUPPORT_CERTIFICATE_V1","coarse_family":f,"requires":["C6_FRESH_MEMBER_AND_COMPONENT_AUTHORITY","SOURCE_AUTHORITY","A1_A2_WHERE_APPLICABLE","PHYSICAL_INCIDENCE_EQUIVALENCE","REPRESENTATION_PULLBACK"],"complete":False}
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

def candidate_contract_preflight(c:Candidate)->dict[str,Any]:
 result=closed_document(c,"result","result_sha256")
 need(result["schema"]==SCHEMA+".result.v1"and result["status"]=="PASS_497772_FRESH_MEMBERS__545184_REPRESENTATIONS__15392_INCIDENCES__15392_OPEN_PHYSICAL_GAPS__ZERO_SUPPORT_CREDIT","candidate result contract")
 need(result["producer_source"]=={"filename":PRODUCER,"size":PRODUCER_PIN.size,"sha256":PRODUCER_PIN.sha256}and result["source_pins"]==[p.__dict__ for p in SOURCE_PINS],"candidate source pins")
 need(result["fresh_base"]=={"member_count":497_772,"root_count":334_604,"component_count":61_928,"cross_component_pair_denominator":123_410_984_634},"candidate fresh base")
 need(result["fresh_census"]=={"family_member_counts":EXPECTED_MEMBERS,"family_representation_counts":EXPECTED_REPS,"member_count":497_772,"representation_count":545_184,"physical_incidence_count":15_392,"semantic_gap_count":15_392,"component_rebind_count":497_772,"transition_handle_count":497_772,"family_census_rows":6},"candidate fresh census")
 need(result["C4_semantic_effect"]=={"orphan_target_empty_graph_disposition_count":16,"retained_distinct_side_relation_count":10,"positive_graph_definition_credit":0,"physical_incidence_credit":0},"candidate C4 boundary")
 need(result["C5_semantic_effect"]=={"positive_graph_definition_count":5_264,"empty_graph_disposition_count":33_344,"invalid_member_count":66_688,"empty_graph_surviving_side_reclassified_to_NON_GRAPH_count":33_344,"closed_graph_definition_gap_count":38_608},"candidate C5 boundary")
 need(result["physical_relation_semantic_authority_counts"]=={"C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION":10,"C5_POSITIVE_GRAPH_DEFINITION":15_382},"candidate relation authority")
 need(result["C1_component_bindings_replaced_count"]==497_772 and result["old_component_ids_are_provenance_only"]is True and result["physical_incidence_relations_not_legacy_member_denominator"]is True,"candidate rebind semantics")
 need(result["legacy_115440_incidence_denominator_reused"]is False and result["legacy_76832_side_member_denominator_reused"]is False,"candidate denominator boundary")
 need(result["formal_credit"]==ZERO and result["normalized_support_sealed"]is False and result["B1A_permitted"]is False and result["B2_permitted"]is False and result["CM2"]=="NO-GO_FOR_CLAIM","candidate zero credit")
 descriptors=[{"role":role,"filename":OUTPUTS[role],"size":c.ids[role][4],"sha256":c.hashes[role]}for role in OUTPUT_ORDER[:-1]]
 need(result["output_artifacts_in_publication_order_before_result"]==descriptors,"candidate descriptors")
 row_kinds={"family_census":"family-census","member":"member-identity-support","representation":"representation","physical_incidence":"physical-incidence-statement","gap":"semantic-gap","component_rebind":"component-rebind","transition_handle":"transition-ready-handle"}
 for role,kind in row_kinds.items():
  rows=c.rows(role)
  try:first=next(rows)
  except StopIteration as error:raise Rejected("candidate empty ledger:"+role)from error
  finally:rows.close()
  need(first["schema"]==SCHEMA+"."+kind+"-row.v1","candidate first-row schema:"+role)
 return result

def verify(s:Sources,c:Candidate)->dict[str,Any]:
 candidate_contract_preflight(c)
 c1=source_plain(s,"C1_RESULT");c4=source_plain(s,"C4_RESULT");c5=source_plain(s,"C5_RESULT");c6=source_plain(s,"C6_RESULT")
 need(c1["schema"]=="cm2.round306c1.source-g-corrected-identity-support-replay.v1.result.v1"and c1["status"]=="PASS_CORRECTED_SIX_FAMILY_MECHANICAL_REPLAY_CANDIDATE__ZERO_SUPPORT_CREDIT","C1 result")
 need(c4["schema"]=="cm2.round306c4.source-g-r235d-to-g2-orphan-graph-semantic-bridge.v1"and c4["status"]=="PASS_16_R235D_TO_G2_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS__ZERO_INCIDENCE_PULLBACK_TRACE_SUPPORT_CREDIT","C4 result")
 need(c5["schema"]=="cm2.round306c5.source-g-corrected-g2-graph-semantic-classification.v1"and c5["status"]=="PASS_5264_POSITIVE_G2_GRAPH_DEFINITIONS__33344_R235_EMPTY_GRAPH_DISPOSITIONS__FRESH_DSU_REQUIRED","C5 result")
 need(c6["schema"]=="cm2.round306c6.source-g-corrected-g2-invalidation-fresh-dsu-freeze.v1"and c6["status"]=="PASS_66688_G2_MEMBER_INVALIDATIONS__476118_RETAINED_EDGES__61928_FRESH_COMPONENTS__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFICATION","C6 result")
 producer_commit={"filename":PRODUCER,"size":PRODUCER_PIN.size,"sha256":PRODUCER_PIN.sha256}
 preliminary=closed_document(c,"result","result_sha256");need(preliminary["producer_source"]==producer_commit and preliminary["source_pins"]==[p.__dict__ for p in SOURCE_PINS],"result source pins")
 need(preliminary["fresh_census"]["member_count"]==497_772 and preliminary["fresh_census"]["representation_count"]==545_184 and preliminary["fresh_census"]["physical_incidence_count"]==15_392 and preliminary["fresh_census"]["semantic_gap_count"]==15_392,"result census preflight")
 need(preliminary["formal_credit"]==ZERO and preliminary["normalized_support_sealed"]is False and preliminary["B1A_permitted"]is False and preliminary["B2_permitted"]is False and preliminary["CM2"]=="NO-GO_FOR_CLAIM","result zero credit")
 need([item["role"]for item in preliminary["output_artifacts_in_publication_order_before_result"]]==list(OUTPUT_ORDER[:-1]),"descriptor order")
 for item in preliminary["output_artifacts_in_publication_order_before_result"]:
  role=item["role"];need(item=={"role":role,"filename":OUTPUTS[role],"size":c.ids[role][4],"sha256":c.hashes[role]},"descriptor:"+role)

 c6_members={}
 for old in source_jsonl(s,"C6_MEMBER"):
  member=old["registry_member_id"];need(member not in c6_members,"duplicate C6 member");c6_members[member]={"component":old["fresh_component_id"],"row_id":old["row_id"],"row_sha256":old["row_sha256"],"root":old["new_base_root_id"]}
 need(len(c6_members)==497_772,"C6 member count")
 orphan_graphs={}
 for old in source_jsonl(s,"C4_BRIDGE"):
  disposition=old["G2_orphan_graph_disposition"];graph=disposition["C3_orphan_target_graph_id"];need(graph not in orphan_graphs and disposition["disposition"]=="EMPTY_GRAPH_ON_COMPLETE_PARAMETER_DOMAIN"and disposition["C3_graph_definition_blocker_resolved"]==1,"C4 orphan disposition");orphan_graphs[graph]={"row_id":old["bridge_row_id"],"row_sha256":old["row_sha256"],"graph_id":graph,"graph_inventory_row_id":disposition["C3_orphan_target_graph_inventory_row_id"]}
 need(len(orphan_graphs)==16,"C4 orphan graph count")
 positive_graphs={};empty_surviving={};invalid_candidates=set();c5_counts=Counter()
 for old in source_jsonl(s,"C5_SEMANTIC"):
  graph=old["graph_id"];semantic=old["semantic_classification"];classification=semantic["classification"];c5_counts[classification]+=1;ref={"row_id":old["semantic_row_id"],"row_sha256":old["row_sha256"],"graph_id":graph}
  if classification=="POSITIVE_GRAPH":need(graph not in positive_graphs and semantic["graph_definition_credit"]==1,"positive graph");positive_graphs[graph]=ref
  elif classification=="EMPTY_GRAPH":
   need(semantic["graph_definition_disposition_credit"]==1,"empty graph");sheet=semantic["invalid_sheet_member_candidate"];invalid_side=semantic["invalid_side_member_candidate"];survivor=semantic["surviving_side_member"];need(sheet!=invalid_side and sheet!=survivor and invalid_side!=survivor,"empty roles");invalid_candidates.add(sheet);invalid_candidates.add(invalid_side);need(survivor not in empty_surviving,"duplicate empty survivor");empty_surviving[survivor]={**ref,"surviving_side_role":semantic["surviving_side_role"]}
  else:raise Rejected("unknown C5 classification")
 need(dict(c5_counts)=={"POSITIVE_GRAPH":5_264,"EMPTY_GRAPH":33_344}and len(invalid_candidates)==66_688 and len(empty_surviving)==33_344,"C5 census")
 need(invalid_candidates.isdisjoint(c6_members)and set(empty_surviving).issubset(c6_members),"C5/C6 partition")

 receipts={};member_refs={};member_counts=Counter();legacy_member_counts=Counter();missing=set()
 member_ids={family:Seq()for family in FAMILIES};member_sources={family:Seq()for family in FAMILIES}
 def expected_members()->Iterator[dict[str,Any]]:
  for old in source_jsonl(s,"C1_MEMBER"):
   member=old["member_id"];legacy_family=old["coarse_family"];legacy_member_counts[legacy_family]+=1;c6ref=c6_members.get(member)
   if c6ref is None:missing.add(member);continue
   family="NON_GRAPH"if member in empty_surviving else legacy_family
   if family!=legacy_family:need(legacy_family=="G2B","member reclassification")
   node=ast(member,family);cert=grammar(family);semantic_ref=empty_surviving.get(member);ic=commit("member-input.v1",{"C1_row_sha256":old["row_sha256"],"C6_row_sha256":c6ref["row_sha256"],"C5_empty_graph_row_sha256":None if semantic_ref is None else semantic_ref["row_sha256"],"member_id":member,"fresh_family":family,"producer_sha256":PRODUCER_PIN.sha256})
   payload={"member_id":member,"coarse_family":family,"legacy_C1_coarse_family":legacy_family,"family_transition":"G2B_TO_NON_GRAPH_BY_C5_EMPTY_GRAPH_DISPOSITION"if family!=legacy_family else"PRESERVED_FROM_C1","primitive_source_kind":"C5_EMPTY_GRAPH_SURVIVING_SIDE_NON_GRAPH_SOURCE"if family!=legacy_family else old["primitive_source_kind"],"source_authority_role":old["source_authority_role"],"source_filename":old["source_filename"],"source_table":old["source_table"],"source_path":old["source_path"],"source_row_id":old["source_row_id"],"source_row_sha256":old["source_row_sha256"],"C1_member_row_id":old["row_id"],"C1_member_row_sha256":old["row_sha256"],"C6_member_component_row_id":c6ref["row_id"],"C6_member_component_row_sha256":c6ref["row_sha256"],"fresh_component_id":c6ref["component"],"fresh_base_root_id":c6ref["root"],"C5_empty_graph_semantic_row_id":None if semantic_ref is None else semantic_ref["row_id"],"C5_empty_graph_semantic_row_sha256":None if semantic_ref is None else semantic_ref["row_sha256"],"typed_support_ast":node,"certificate_grammar":cert,"mechanical_representation_count":old["mechanical_representation_count"],"mechanical_representation_ids_sha256":old["mechanical_representation_ids_sha256"],"primary_mechanical_representation_id":old["primary_mechanical_representation_id"],"support_semantic_state":"FRESH_MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED","canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("member-identity-support",payload);need(member not in member_refs,"duplicate member");member_refs[member]={"family":family,"legacy_family":legacy_family,"row_id":row["row_id"],"row_sha256":row["row_sha256"],"component":c6ref["component"],"c6_row_id":c6ref["row_id"],"c6_row_sha256":c6ref["row_sha256"],"old_component":old["corrected_component_id"],"old_row_id":old["row_id"],"old_row_sha256":old["row_sha256"],"ast_sha256":objsha(node),"representation_set_sha256":old["mechanical_representation_ids_sha256"]};member_counts[family]+=1;member_ids[family].add(member);member_sources[family].add(old["row_sha256"]);yield row
 receipts["member"]=compare_rows(c,"member",expected_members());need(dict(legacy_member_counts)=={"PRESERVED":126_468,"NON_GRAPH":17_828,"R2":295_336,"R292":9_404,"G2A":38_608,"G2B":76_816},"legacy members");need(missing==invalid_candidates and set(member_refs)==set(c6_members)and dict(member_counts)==EXPECTED_MEMBERS,"fresh members")

 rep_counts=Counter();legacy_rep_counts=Counter();rep_ids={family:Seq()for family in FAMILIES};rep_sources={family:Seq()for family in FAMILIES}
 def expected_representations()->Iterator[dict[str,Any]]:
  for old in source_jsonl(s,"C1_REPRESENTATION"):
   owner=old["owner_member_id"];legacy_rep_counts[old["coarse_family"]]+=1;member_ref=member_refs.get(owner)
   if member_ref is None:continue
   family=member_ref["family"];need(old["coarse_family"]==member_ref["legacy_family"],"representation legacy family");rep=old["representation_id"];ic=commit("representation-input.v1",{"C1_row_sha256":old["row_sha256"],"owner_member_row_sha256":member_ref["row_sha256"],"fresh_family":family,"representation_id":rep})
   payload={"representation_id":rep,"owner_member_id":owner,"coarse_family":family,"legacy_C1_coarse_family":old["coarse_family"],"representation_role":old["representation_role"],"source_authority_role":old["source_authority_role"],"source_filename":old["source_filename"],"source_table":old["source_table"],"source_path":old["source_path"],"source_row_id":old["source_row_id"],"source_row_sha256":old["source_row_sha256"],"C1_representation_row_id":old["row_id"],"C1_representation_row_sha256":old["row_sha256"],"owner_member_row_id":member_ref["row_id"],"owner_member_row_sha256":member_ref["row_sha256"],"typed_representation_ast":{"ast_kind":"TYPED_MECHANICAL_REPRESENTATION","representation_id":rep,"owner_member_id":owner,"role":old["representation_role"],"fresh_member_universe":"ROUND306C6"},"certificate_grammar":grammar(family),"pullback_semantic_state":"PULLBACK_EQUIVALENCE_NOT_PROVED","canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("representation",payload);rep_counts[family]+=1;rep_ids[family].add(rep);rep_sources[family].add(old["row_sha256"]);yield row
 receipts["representation"]=compare_rows(c,"representation",expected_representations());need(dict(legacy_rep_counts)=={"PRESERVED":165_744,"NON_GRAPH":17_828,"R2":302_624,"R292":10_252,"G2A":38_608,"G2B":76_816}and dict(rep_counts)==EXPECTED_REPS,"representation census")

 incidence_refs={};incidence_counts=Counter();relations=set();valid_nonpositive=0;semantic_authority_counts=Counter();incidence_ids={family:Seq()for family in FAMILIES};incidence_sources={family:Seq()for family in FAMILIES}
 def expected_incidence()->Iterator[dict[str,Any]]:
  nonlocal valid_nonpositive
  for old in source_jsonl(s,"C1_INCIDENCE"):
   member=old["member_id"];member_ref=member_refs.get(member)
   if member_ref is None:continue
   semantic_ref=positive_graphs.get(old["graph_id"]);bridge_ref=orphan_graphs.get(old["graph_id"])
   if semantic_ref is None and bridge_ref is None:valid_nonpositive+=1;need(member in empty_surviving and old["incidence_role"]=="GRAPH_TO_SIDE","valid nonpositive");continue
   need(not(semantic_ref is not None and bridge_ref is not None),"disjoint authority");family=member_ref["family"];need(family in {"G2A","G2B"}and old["coarse_family"]==family,"retained incidence family")
   if bridge_ref is not None:need(family=="G2B"and old["source_graph_row_id"]==bridge_ref["graph_inventory_row_id"],"C4 bridge binding")
   relation=(old["graph_id"],old["incidence_role"],old["source_incidence_row_id"],member);need(relation not in relations,"duplicate relation");relations.add(relation);authority_kind="C5_POSITIVE_GRAPH_DEFINITION"if semantic_ref is not None else"C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION";authority_ref=semantic_ref if semantic_ref is not None else bridge_ref;semantic_authority_counts[authority_kind]+=1;ic=commit("physical-incidence-input.v1",{"C1_incidence_row_sha256":old["row_sha256"],"graph_semantic_authority_kind":authority_kind,"graph_semantic_authority_row_sha256":authority_ref["row_sha256"],"member_row_sha256":member_ref["row_sha256"]})
   payload={"graph_id":old["graph_id"],"incidence_role":old["incidence_role"],"member_id":member,"coarse_family":family,"source_graph_row_id":old["source_graph_row_id"],"source_graph_row_sha256":old["source_graph_row_sha256"],"source_incidence_row_id":old["source_incidence_row_id"],"source_incidence_row_sha256":old["source_incidence_row_sha256"],"C1_incidence_row_id":old["row_id"],"C1_incidence_row_sha256":old["row_sha256"],"graph_semantic_authority_kind":authority_kind,"graph_semantic_authority_row_id":authority_ref["row_id"],"graph_semantic_authority_row_sha256":authority_ref["row_sha256"],"member_row_id":member_ref["row_id"],"member_row_sha256":member_ref["row_sha256"],"incidence_statement_ast":{**old["incidence_statement_ast"],"proved":False,"fresh_member_universe":"ROUND306C6"},"positive_graph_definition_credit":1 if semantic_ref is not None else 0,"empty_graph_disposition_credit":0 if semantic_ref is not None else 1,"physical_incidence_credit":0,"theorem_semantic_state":old["theorem_semantic_state"],"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("physical-incidence-statement",payload);need(old["row_id"]not in incidence_refs,"duplicate C1 incidence");incidence_refs[old["row_id"]]={"row_id":row["row_id"],"row_sha256":row["row_sha256"]};incidence_counts[family]+=1;incidence_ids[family].add(row["row_id"]);incidence_sources[family].add(old["row_sha256"]);yield row
 receipts["physical_incidence"]=compare_rows(c,"physical_incidence",expected_incidence());need(dict(incidence_counts)==EXPECTED_PHYSICAL and len(relations)==15_392 and valid_nonpositive==33_344,"incidence census");need(dict(semantic_authority_counts)=={"C5_POSITIVE_GRAPH_DEFINITION":15_382,"C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION":10},"incidence authority census")

 gap_counts=Counter();graph_definition_gaps=0;discarded_physical=0;gap_ids={family:Seq()for family in FAMILIES};gap_sources={family:Seq()for family in FAMILIES}
 def expected_gaps()->Iterator[dict[str,Any]]:
  nonlocal graph_definition_gaps,discarded_physical
  for old in source_jsonl(s,"C1_GAP"):
   if old["gap_kind"]=="SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING":graph_definition_gaps+=1;continue
   incidence_ref=incidence_refs.get(old["subject_row_id"])
   if incidence_ref is None:discarded_physical+=1;continue
   member=old["member_id"];member_ref=member_refs[member];family=member_ref["family"];need(family in {"G2A","G2B"},"gap family");ic=commit("semantic-gap-input.v1",{"C1_gap_row_sha256":old["row_sha256"],"C7_incidence_row_sha256":incidence_ref["row_sha256"],"member_row_sha256":member_ref["row_sha256"]})
   payload={"gap_kind":old["gap_kind"],"subject_kind":"PHYSICAL_INCIDENCE","subject_row_id":incidence_ref["row_id"],"member_id":member,"coarse_family":family,"required_closure":old["required_closure"],"C1_gap_row_id":old["row_id"],"C1_gap_row_sha256":old["row_sha256"],"blocking_credit_kinds":["normalized_support","physical_incidence","representation_cover","B1A"],"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("semantic-gap",payload);gap_counts[family]+=1;gap_ids[family].add(row["row_id"]);gap_sources[family].add(old["row_sha256"]);yield row
 receipts["gap"]=compare_rows(c,"gap",expected_gaps());need(graph_definition_gaps==38_608 and discarded_physical==100_032 and dict(gap_counts)==EXPECTED_PHYSICAL,"gap census")

 rebind_counts=Counter();changed=0;rebind_ids={family:Seq()for family in FAMILIES}
 def expected_rebind()->Iterator[dict[str,Any]]:
  nonlocal changed
  for member,member_ref in member_refs.items():
   need(member_ref["old_component"]!=member_ref["component"],"unchanged component");changed+=1;family=member_ref["family"];ic=commit("component-rebind-input.v1",{"member_id":member,"C1_component_id":member_ref["old_component"],"C6_component_id":member_ref["component"],"C6_row_sha256":member_ref["c6_row_sha256"]})
   payload={"member_id":member,"coarse_family":family,"C1_component_id_provenance_only":member_ref["old_component"],"C1_member_row_id":member_ref["old_row_id"],"C1_member_row_sha256":member_ref["old_row_sha256"],"C6_member_component_row_id":member_ref["c6_row_id"],"C6_member_component_row_sha256":member_ref["c6_row_sha256"],"fresh_component_id":member_ref["component"],"rebind_reason":"ALL_SURVIVING_MEMBERS_REBOUND_AFTER_C5_INVALIDATION_AND_C6_FRESH_DSU","canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("component-rebind",payload);rebind_counts[family]+=1;rebind_ids[family].add(row["row_id"]);yield row
 receipts["component_rebind"]=compare_rows(c,"component_rebind",expected_rebind());need(changed==497_772 and dict(rebind_counts)==EXPECTED_MEMBERS,"rebind census")

 handle_counts=Counter();seen_handles=set();handle_ids={family:Seq()for family in FAMILIES}
 def expected_handles()->Iterator[dict[str,Any]]:
  for old in source_jsonl(s,"C1_HANDLE"):
   member=old["member_id"];member_ref=member_refs.get(member)
   if member_ref is None:continue
   need(member not in seen_handles,"duplicate C1 handle");seen_handles.add(member);family=member_ref["family"];ic=commit("transition-handle-input.v1",{"C1_handle_row_sha256":old["row_sha256"],"member_row_sha256":member_ref["row_sha256"],"fresh_component_id":member_ref["component"]})
   payload={"member_id":member,"coarse_family":family,"member_row_id":member_ref["row_id"],"member_row_sha256":member_ref["row_sha256"],"typed_support_ast_sha256":member_ref["ast_sha256"],"representation_set_sha256":member_ref["representation_set_sha256"],"fresh_component_id":member_ref["component"],"C1_handle_row_id":old["row_id"],"C1_handle_row_sha256":old["row_sha256"],"transition_syntax_ready":True,"transition_semantics_ready":False,"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   row=make_row("transition-ready-handle",payload);handle_counts[family]+=1;handle_ids[family].add(row["row_id"]);yield row
 receipts["transition_handle"]=compare_rows(c,"transition_handle",expected_handles());need(seen_handles==set(member_refs)and dict(handle_counts)==EXPECTED_MEMBERS,"handle census")

 def expected_families()->Iterator[dict[str,Any]]:
  for family in FAMILIES:
   source_commit=objsha({"C1_member_rows_sha256":member_sources[family].done(),"C1_representation_rows_sha256":rep_sources[family].done(),"C1_incidence_rows_sha256":incidence_sources[family].done(),"C1_gap_rows_sha256":gap_sources[family].done()});ic=commit("family-census-input.v1",{"family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"physical_incidence_count":incidence_counts[family],"semantic_gap_count":gap_counts[family],"source_commitment_sha256":source_commit})
   payload={"coarse_family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"physical_incidence_count":incidence_counts[family],"semantic_gap_count":gap_counts[family],"component_rebind_count":rebind_counts[family],"transition_handle_count":handle_counts[family],"C5_empty_graph_side_reclassification_count":33_344 if family=="NON_GRAPH"else 0,"member_ids_sha256":member_ids[family].done(),"representation_ids_sha256":rep_ids[family].done(),"physical_incidence_row_ids_sha256":incidence_ids[family].done(),"semantic_gap_row_ids_sha256":gap_ids[family].done(),"component_rebind_row_ids_sha256":rebind_ids[family].done(),"transition_handle_row_ids_sha256":handle_ids[family].done(),"source_rows_commitment_sha256":source_commit,"canonical_input_commitment_sha256":ic,"formal_credit":dict(ZERO)}
   yield make_row("family-census",payload)
 receipts["family_census"]=compare_rows(c,"family_census",expected_families())

 descriptors=[{"role":role,"filename":OUTPUTS[role],"size":c.ids[role][4],"sha256":c.hashes[role]}for role in OUTPUT_ORDER[:-1]]
 result_body={"schema":SCHEMA+".result.v1","status":"PASS_497772_FRESH_MEMBERS__545184_REPRESENTATIONS__15392_INCIDENCES__15392_OPEN_PHYSICAL_GAPS__ZERO_SUPPORT_CREDIT","producer_source":producer_commit,"source_pins":[p.__dict__ for p in SOURCE_PINS],"fresh_base":{"member_count":497_772,"root_count":334_604,"component_count":61_928,"cross_component_pair_denominator":123_410_984_634},"fresh_census":{"family_member_counts":dict(member_counts),"family_representation_counts":dict(rep_counts),"member_count":497_772,"representation_count":545_184,"physical_incidence_count":15_392,"semantic_gap_count":15_392,"component_rebind_count":497_772,"transition_handle_count":497_772,"family_census_rows":6},"C4_semantic_effect":{"orphan_target_empty_graph_disposition_count":16,"retained_distinct_side_relation_count":10,"positive_graph_definition_credit":0,"physical_incidence_credit":0},"C5_semantic_effect":{"positive_graph_definition_count":5_264,"empty_graph_disposition_count":33_344,"invalid_member_count":66_688,"empty_graph_surviving_side_reclassified_to_NON_GRAPH_count":33_344,"closed_graph_definition_gap_count":38_608},"physical_relation_semantic_authority_counts":dict(semantic_authority_counts),"C1_component_bindings_replaced_count":changed,"old_component_ids_are_provenance_only":True,"physical_incidence_relations_not_legacy_member_denominator":True,"legacy_115440_incidence_denominator_reused":False,"legacy_76832_side_member_denominator_reused":False,"ledger_receipts":receipts,"output_artifacts_in_publication_order_before_result":descriptors,"formal_credit":dict(ZERO),"normalized_support_sealed":False,"B1A_permitted":False,"B2_permitted":False,"CM2":"NO-GO_FOR_CLAIM","seed_serialized_or_semantically_used":False};result={**result_body,"result_sha256":objsha(result_body)};need(json.loads(c.raw("result"))==result,"result exact");c.final();s.final()
 return{"status":"PASS_INDEPENDENT_C7_FULL_2069290_ROW_REPLAY__ZERO_SUPPORT_CREDIT","artifact_count":8,"candidate_artifact_sha256":dict(c.hashes),"row_count":sum(value["row_count"]for value in receipts.values()),"ledger_receipts":receipts,"fresh_member_count":497_772,"fresh_representation_count":545_184,"physical_incidence_count":15_392,"semantic_gap_count":15_392,"component_rebind_count":497_772,"producer_imported_or_executed":False,"formal_credit":dict(ZERO)}

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
 parent=Path("/tmp/cm2-round306c7-verifier-attacks");parent.mkdir(mode=0o700,parents=True,exist_ok=True);path=Path(tempfile.mkdtemp(prefix="attack.",dir=parent))
 for role in OUTPUT_ORDER:copy_file(source/OUTPUTS[role],path/OUTPUTS[role])
 return path
def remove_tree(path:Path)->None:
 for e in path.iterdir():e.unlink()
 path.rmdir()
def rewrite_closed(path:Path,field:str,mutate:Any)->None:
 v=json.loads(path.read_bytes());mutate(v);body=dict(v);body.pop(field,None);v[field]=objsha(body);path.write_bytes(canonical(v))
def attack_suite(source_path:Path)->dict[str,Any]:
 sources=Sources().__enter__()
 with Candidate(source_path)as c:baseline=verify(sources,c)
 work=clone_candidate(source_path);attacks=[]
 def restore(role:str)->None:
  p=work/OUTPUTS[role]
  if p.exists()or p.is_symlink():p.unlink()
  copy_file(source_path/OUTPUTS[role],p)
 def execute(aid:str,mutate:Any,rest:Any)->None:
  try:
   mutate()
   try:
    with Candidate(work)as c:verify(sources,c)
   except (Rejected,gzip.BadGzipFile,EOFError,OSError,json.JSONDecodeError) as e:boundary=type(e).__name__+":"+str(e)
   else:raise Rejected("attack accepted:"+aid)
   body={"attack_id":aid,"rejected":True,"rejection_boundary":boundary};attacks.append({**body,"row_sha256":objsha(body)})
  finally:rest()
 execute("A01_EXTRA_FILE",lambda:(work/"foreign").write_bytes(b"x"),lambda:(work/"foreign").unlink())
 execute("A02_MISSING_RESULT",lambda:(work/OUTPUTS["result"]).unlink(),lambda:restore("result"))
 execute("A03_RESULT_SYMLINK",lambda:((work/OUTPUTS["result"]).unlink(),(work/OUTPUTS["result"]).symlink_to(source_path/OUTPUTS["result"])),lambda:restore("result"))
 execute("A04_HARDLINK_MEMBER_AS_RESULT",lambda:((work/OUTPUTS["result"]).unlink(),os.link(work/OUTPUTS["member"],work/OUTPUTS["result"])),lambda:restore("result"))
 execute("A05_RESULT_PRODUCER_PIN",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["producer_source"].__setitem__("sha256","0"*64)),lambda:restore("result"))
 execute("A06_FRESH_BASE_COMPONENT_COUNT",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["fresh_base"].__setitem__("component_count",d["fresh_base"]["component_count"]+1)),lambda:restore("result"))
 fields=("member_count","representation_count","physical_incidence_count","semantic_gap_count","component_rebind_count")
 for n,field in enumerate(fields,7):execute("A"+str(n).zfill(2)+"_RESULT_"+field.upper(),lambda f=field:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["fresh_census"].__setitem__(f,d["fresh_census"][f]+1)),lambda:restore("result"))
 execute("A12_CREDIT_INJECTION",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["formal_credit"].__setitem__("normalized_support",1)),lambda:restore("result"))
 execute("A13_DESCRIPTOR_SUBSTITUTION",lambda:rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:d["output_artifacts_in_publication_order_before_result"][0].__setitem__("sha256","0"*64)),lambda:restore("result"))
 for n,role in enumerate(("family_census","member","representation","physical_incidence","gap","component_rebind","transition_handle"),14):
  def corrupt(r:str=role)->None:
   p=work/OUTPUTS[r];fd=os.open(p,os.O_WRONLY)
   try:os.pwrite(fd,b"X",0)
   finally:os.close(fd)
   h=hashlib.sha256(p.read_bytes()).hexdigest();rewrite_closed(work/OUTPUTS["result"],"result_sha256",lambda d:next(x for x in d["output_artifacts_in_publication_order_before_result"]if x["role"]==r).__setitem__("sha256",h))
  execute("A"+str(n).zfill(2)+"_CORRUPT_"+role.upper(),corrupt,lambda r=role:(restore(r),restore("result")))
 need(len(attacks)==20,"attack count");remove_tree(work);sources.final();sources.__exit__(None,None,None);body={"schema":SCHEMA+".coherent-attack-suite.v1","status":"PASS_20_OF_20_COHERENT_ATTACKS_REJECTED","verifier_filename":Path(__file__).name,"verifier_file_sha256":self_sha(),"attack_count":20,"rejected_count":20,"all_rejected":True,"baseline_candidate_artifact_sha256":baseline["candidate_artifact_sha256"],"attacks":attacks};return{**body,"attack_suite_sha256":objsha(body)}
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
  return{"status":"PASS_MANIFEST_FIRST_HELD_FD_FULL_2069290_ROW_REPLAY__ZERO_WRITES_ZERO_SUPPORT_CREDIT","manifest_filename":MANIFEST,"manifest_member_count":len(MANIFEST_MEMBERS),"verified_row_count":receipt["row_count"],"candidate_artifact_sha256":receipt["candidate_artifact_sha256"],"deliverables_write_syscalls":0,"formal_credit":dict(ZERO)}

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
