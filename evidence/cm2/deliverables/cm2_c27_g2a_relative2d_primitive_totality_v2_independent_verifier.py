#!/usr/bin/env python3
"""Independent primitive recomputation of the scoped 5,264 G2A route theorem.

This verifier deliberately imports no candidate producer, exact classifier,
theorem builder, or shared implementation module.  Candidate totality is
recomputed by an endpoint-event sweep rather than the producer interval tree.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
R235="cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236="cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242="cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
C4="cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
C5="cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C10="cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C11A="cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_ledger.jsonl.gz"
C11BR="cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_relation_theorem_ledger.jsonl.gz"
C11BI="cm2_round306c11b_source_g_r242_side_incidence_trace_kernel_interface_kernel_ledger.jsonl.gz"
C12A="cm2_round306c12a_source_g_rerouted_shared_side_kernel_ledger.jsonl.gz"
C14A="cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_equality_ledger.jsonl.gz"
C14B="cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_exact_sheet_member_ledger.jsonl.gz"
C15="cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C22="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz"
C23="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz"
C24="cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C25="cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26="cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
SIGNED="cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_ledger.json.gz"
COMPLETE="cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_face_inventory.json.gz"
PINS={R235:"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",R236:"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",R242:"8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",C4:"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db",C5:"8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",C10:"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",C11A:"87a37e007408adf667ae30a7575c928263512bf8a08cfd9e7144db11296680cd",C11BR:"37155fe874b8f4acd49773c013f4ec605a2f9388a0d1eb7443c88a731f1e0299",C11BI:"815ed3b2ab73b3165e203cf8215421c89412b6d4f5190b816cb0d2e02f409a59",C12A:"12ae529eb5ccb53b75da1622c2c7b655a2acea6faf25d9018871a4fd079b35b9",C14A:"09aff7b141e519a1d7252e4ad8becdb668b8b12f84c99cdb69ffe43ae3529883",C14B:"6f69b5e82377cde72e7223e86b518da12e19ef85b93a5706989ebb81ab78a6d6",C15:"e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",C22:"e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",C23:"230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",C24:"ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",C25:"66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",C26:"fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",SIGNED:"9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9",COMPLETE:"443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d"}


class Failure(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise Failure(label)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v:Any)->str:return hashlib.sha256(canonical(v)).hexdigest()
def fp(s:os.stat_result)->tuple[int,...]:return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
def check_row(r:dict[str,Any],label:str)->None:
 b=dict(r);claimed=b.pop("row_sha256",None);need(type(claimed)is str and claimed==digest(b),label+":closure")


@dataclass
class Capture:
 label:str;path:Path;fd:int;pre:tuple[int,...];sha256:str
 @classmethod
 def open(cls,label:str,path:Path,expected:str)->"Capture":
  p=path.resolve();fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
  try:
   s=os.fstat(fd);need(stat.S_ISREG(s.st_mode),label+":regular");h=hashlib.sha256()
   while block:=os.read(fd,4<<20):h.update(block)
   got=h.hexdigest();need(got==expected,label+":sha256");need(fp(os.fstat(fd))==fp(s),label+":hash-stat");return cls(label,p,fd,fp(s),got)
  except BaseException:os.close(fd);raise
 def rows(self)->Iterator[dict[str,Any]]:
  os.lseek(self.fd,0,0);dup=os.dup(self.fd)
  with os.fdopen(dup,"rb")as raw:
   with gzip.GzipFile(fileobj=raw,mode="rb")as z:
    for i,line in enumerate(z):
     need(line.endswith(b"\n"),self.label+":newline");wire=line[:-1];r=json.loads(wire);need(type(r)is dict and canonical(r)==wire,self.label+":canonical");check_row(r,self.label+":"+str(i));yield r
  self.unchanged("rows")
 def document(self)->dict[str,Any]:
  os.lseek(self.fd,0,0);chunks=[]
  while block:=os.read(self.fd,4<<20):chunks.append(block)
  wire=b"".join(chunks);r=json.loads(wire);need(type(r)is dict and canonical(r)+b"\n"==wire,self.label+":canonical document");b=dict(r);claimed=b.pop("result_sha256",None);need(type(claimed)is str and claimed==digest(b),self.label+":closure");self.unchanged("document");return r
 def json(self)->dict[str,Any]:
  os.lseek(self.fd,0,0);chunks=[]
  while block:=os.read(self.fd,4<<20):chunks.append(block)
  r=json.loads(b"".join(chunks));need(type(r)is dict,self.label+":json");self.unchanged("json");return r
 def unchanged(self,phase:str)->None:need(fp(os.fstat(self.fd))==self.pre,self.label+":"+phase+":stat")
 def att(self)->dict[str,Any]:self.unchanged("final");return{"filename":self.path.name,"observed_sha256":self.sha256,"O_NOFOLLOW":True,"single_open_file_description_hash_parse_fstat":True,"stat_fingerprint":list(self.pre)}
 def close(self)->None:os.close(self.fd)


def cert(cap:Capture)->dict[str,Any]:
 x=cap.json();need(set(x)=={"schema","result","result_sha256"}and x["result_sha256"]==digest(x["result"]),cap.label+":certificate");return x["result"]
def intervals(ast:Any)->tuple[Q,...]:
 found:dict[str,list[tuple[Q,Q]]]={"t":[],"p":[],"s":[]}
 def walk(x:Any)->None:
  if type(x)is dict:
   if x.get("op")in{"OPEN_INTERVAL","CLOSED_INTERVAL"}and x.get("coordinate")in found:found[x["coordinate"]].append((Q(x["lower"]),Q(x["upper"])))
   for y in x.values():walk(y)
  elif type(x)is list:
   for y in x:walk(y)
 walk(ast)
 for coordinate,values in found.items():need(bool(values)and len(set(values))==1,"consistent "+coordinate+" interval constraints")
 return found["t"][0]+found["p"][0]+found["s"][0]
def strict_predicate(ast:Any)->dict[str,Any]:
 out=[]
 def walk(x:Any)->None:
  if type(x)is dict:
   if x.get("op")in{"LT","GT"}:out.append(x)
   else:
    for y in x.values():walk(y)
  elif type(x)is list:
   for y in x:walk(y)
 walk(ast);need(len(out)==1,"unique strict predicate");return out[0]
def strip_unit(expr:Any)->tuple[int,Any]:
 if type(expr)is dict and expr.get("op")=="MUL"and type(expr.get("args"))is list:
  units=[];others=[]
  for a in expr["args"]:
   if type(a)is dict and a.get("op")=="RATIONAL_CONSTANT"and Q(a["value"])in{-1,1}:units.append(int(Q(a["value"])))
   else:others.append(a)
  if len(units)==len(others)==1:return units[0],others[0]
 return 1,expr
def is_zero(x:Any)->bool:return type(x)is dict and x.get("op")=="RATIONAL_CONSTANT"and Q(x["value"])==0
def sgn(x:str)->int:need(x in{"STRICT_NEGATIVE","STRICT_POSITIVE"},"strict sign");return 1 if x=="STRICT_POSITIVE"else-1
def qtext(x:Q)->str:return str(x.numerator)if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def boxtext(x:tuple[Q,...])->list[str]:return[qtext(z)for z in x]
def box_intersection(a:tuple[Q,...],b:tuple[Q,...])->tuple[Q,...]|None:
 out=[]
 for i in range(0,6,2):
  lo=max(a[i],b[i]);hi=min(a[i+1],b[i+1])
  if lo>=hi:return None
  out.extend((lo,hi))
 return tuple(out)
def t2_intersection(carrier:tuple[Q,...],target:tuple[Q,...],sign:int)->tuple[Q,...]|None:
 p0,p1=max(carrier[2],target[2]),min(carrier[3],target[3]);s0,s1=max(carrier[4],target[4]),min(carrier[5],target[5])
 if p0>=p1 or s0>=s1:return None
 lo,hi=carrier[:2];q0,q1=target[:2]
 if sign==1:
  if hi<=0:return None
  lo=max(lo,Q(0));u0,u1=lo*lo,hi*hi
 else:
  if lo>=0:return None
  hi=min(hi,Q(0));u0,u1=hi*hi,lo*lo
 x0,x1=max(q0,u0),min(q1,u1)
 return None if x0>=x1 else(x0,x1,p0,p1,s0,s1)
def simple_t_sign(expr:Any,bounds:list[str])->int:
 need(type(expr)is dict and expr.get("op")=="MUL","t core MUL");coef=None;coord=None
 for a in expr["args"]:
  if a.get("op")=="RATIONAL_CONSTANT":coef=Q(a["value"])
  elif a.get("op")=="COORDINATE":coord=a["name"]
 need(coef not in{None,Q(0)}and coord=="t","simple t core");lo,hi=map(Q,bounds[:2]);need(lo<hi and(hi<=0 or lo>=0),"one-sided t target");return(1 if coef>0 else-1)*(-1 if hi<=0 else 1)


@dataclass(slots=True)
class Carrier:
 key:str;graph:str;member:str;chart:str;box:tuple[Q,...];component:str;row:dict[str,Any]
@dataclass(slots=True)
class Target:
 member:str;source:str;chart:str;box:tuple[Q,...];sign:int|None;row:dict[str,Any]


def bucket_scan(left:list[Carrier],right:list[Target],emit)->None:
 p_groups:dict[tuple[Q,Q],dict[tuple[Q,Q],list[Target]]]=defaultdict(lambda:defaultdict(list))
 for target in right:p_groups[(target.box[2],target.box[3])][(target.box[4],target.box[5])].append(target)
 p_index=[]
 for p_key,s_groups in p_groups.items():
  s_index=sorted((s_key[0],s_key[1],rows)for s_key,rows in s_groups.items());p_index.append((p_key[0],p_key[1],[x[0]for x in s_index],s_index))
 p_index.sort();p_lowers=[x[0]for x in p_index]
 for carrier in left:
  for p_lo,p_hi,s_lowers,s_index in p_index[:bisect_left(p_lowers,carrier.box[3])]:
   if p_hi<=carrier.box[2]:continue
   for s_lo,s_hi,rows in s_index[:bisect_left(s_lowers,carrier.box[5])]:
    if s_hi<=carrier.box[4]:continue
    for target in rows:emit(carrier,target)


def document_rows(cap:Capture)->Iterator[dict[str,Any]]:
 os.lseek(cap.fd,0,0);dup=os.dup(cap.fd)
 with os.fdopen(dup,"rb")as raw:
  with gzip.GzipFile(fileobj=raw,mode="rb")as compressed:
   with io.TextIOWrapper(compressed,encoding="ascii")as z:
    marker='"rows":[';buf=""
    while marker not in buf:
     chunk=z.read(1<<20);need(bool(chunk),cap.label+":marker");buf+=chunk
    buf=buf.split(marker,1)[1];decoder=json.JSONDecoder();n=0
    while True:
     buf=buf.lstrip()
     if not buf:
      chunk=z.read(1<<20);need(bool(chunk),cap.label+":eof");buf=chunk;continue
     if buf[0]==',':buf=buf[1:];continue
     if buf[0]==']':break
     try:r,end=decoder.raw_decode(buf)
     except json.JSONDecodeError:
      chunk=z.read(1<<20);need(bool(chunk),cap.label+":truncated");buf+=chunk;continue
     check_row(r,cap.label+":"+str(n));yield r;n+=1;buf=buf[end:]
 cap.unchanged("document rows")


def relative_certificate(role:str,row:dict[str,Any])->str:
 if role in{"C11A","C12A"}:
  c=row["closure_incidence_certificate"]
  need(c["kind"]=="EXACT_SIGN_STRATUM_RELATIVE_CLOSURE_INCIDENCE_V1"and c["closure_incidence_complete"]is True and c["graph_subset_of_relative_side_closure_by_trace_atlas"]is True and c["strict_side_and_graph_are_disjoint"]is True and c["strict_sign_stratum_is_relatively_open"]is True and c["relative_closure_intersection_statement"]=="closure_in_carrier(exact_side_stratum) INTERSECT exact_graph_support = exact_graph_support","relative closure certificate");return c["certificate_sha256"]
 need(role=="C11B","C11B role");c=row["common_boundary_trace_receipt"];need(c["R245_role_edge_has_exact_R242_patch_contact"]is True and c["closure_of_one_sided_sign_collar_meets_zero_set_in_exact_C10_support"]is True and c["strict_monotone_unique_zero_over_full_base"]is True and c["primitive_factor_continuity_bound_to_C10_radical_receipts"]is True and row["local_graph_side_physical_incidence_proved"]is True and row["one_sided_trace_proved"]is True,"C11B trace certificate");return digest(c)


def verify(a:argparse.Namespace)->dict[str,Any]:
 out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);caps:dict[str,Capture]={}
 try:
  caps["candidate_result"]=Capture.open("candidate_result",Path(a.candidate_result),a.candidate_result_sha256)
  caps["factor_result"]=Capture.open("factor_result",Path(a.factor_result),a.factor_result_sha256)
  caps["theorem_result"]=Capture.open("theorem_result",Path(a.theorem_result),a.theorem_result_sha256)
  caps["shared_source"]=Capture.open("shared_source",Path(a.shared_implementation_source),a.shared_implementation_sha256)
  cr=caps["candidate_result"].document();fr=caps["factor_result"].document();tr=caps["theorem_result"].document()
  need(cr["historical_edge_or_validation_ledger_opened"]is False and fr["historical_edge_or_validation_ledger_opened"]is False and tr["historical_edge_or_validation_ledger_opened"]is False,"no historical validation")
  need(fr["status"].endswith("NO_HISTORICAL_VALIDATION_INPUT__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT")and tr["status"].startswith("PASS_SCOPED_G2A_5264_UNIQUE_ROUTES__")and tr["status"].endswith("POSITIVE_C19_OPEN__CAPTURED_SOURCE_EXECUTION_BOUND__ZERO_CREDIT"),"scoped predecessor status")
  need(tr["implementation_dependency_pin"]["sha256"]==a.shared_implementation_sha256 and tr["implementation_dependency_pin"]["captured_source_bytes_compiled_and_executed"]is True,"shared implementation pin")
  def derived(label:str,base:Path,meta:dict[str,Any])->Capture:
   c=Capture.open(label,base/meta["filename"],meta["file_sha256"]);caps[label]=c;return c
  cbase=Path(a.candidate_result).resolve().parent;fbase=Path(a.factor_result).resolve().parent;tbase=Path(a.theorem_result).resolve().parent
  route_cap=derived("candidate_routes",cbase,cr["G2A"]["route_ledger"]);g2a_cap=derived("G2A_candidates",cbase,cr["G2A"]["candidate_ledger"]);g2b_cap=derived("G2B_candidates",cbase,cr["G2B_candidate_ledger"]);factor_cap=derived("factor_dispositions",fbase,fr["ledger"])
  theorem_caps={k:derived("theorem_"+k,tbase,v)for k,v in tr["ledgers"].items()}
  route_rows=list(route_cap.rows());g2a_rows=list(g2a_cap.rows());g2b_rows=list(g2b_cap.rows());factor_rows=list(factor_cap.rows());final_rows=list(theorem_caps["routes"].rows());contact_rows=list(theorem_caps["contacts"].rows());reverse_rows=list(theorem_caps["reverse_empty"].rows());complement_rows=list(theorem_caps["complement"].rows());cross_rows=list(theorem_caps["cross_C15_witnesses"].rows());edge_rows=list(theorem_caps["unique_cross_C15_component_edges"].rows())
  need((len(route_rows),len(g2a_rows),len(g2b_rows),len(factor_rows),len(final_rows),len(contact_rows),len(reverse_rows),len(complement_rows),len(cross_rows),len(edge_rows))==(5264,9408,18800,18800,5264,9408,9392,552,596,144),"output ledger census")
  need(all("R300C_validation_pair"not in r for rows in(g2a_rows,g2b_rows,factor_rows,contact_rows)for r in rows),"R300C field absent")
  need(Counter(r["disposition"]for r in factor_rows)=={"EXACT_POSITIVE_SUPPORT":9408,"EXACT_EMPTY_INTERSECTION":9392},"fast factor census")
  fast_g2a={(r["graph_id"],r["target_member_id"]):r for r in g2a_rows};fast_pos={(r["graph_id"],r["target_member_id"]):r for r in factor_rows if r["disposition"]=="EXACT_POSITIVE_SUPPORT"};fast_neg={(r["graph_id"],r["target_member_id"]):r for r in factor_rows if r["disposition"]=="EXACT_EMPTY_INTERSECTION"};fast_contacts={(r["graph_id"],r["target_member_id"]):r for r in contact_rows}
  need(len(fast_g2a)==len(fast_pos)==len(fast_contacts)==9408 and set(fast_g2a)==set(fast_pos)==set(fast_contacts),"fast 9408 bijection")
  for k,r in fast_contacts.items():
   need(r["G2A_outer_candidate_row_sha256"]==fast_g2a[k]["row_sha256"]and r["positive_factor_disposition_row_sha256"]==fast_pos[k]["row_sha256"]and r["assigned_unique_terminal"]=="SAME_CHART_RELATIVE_CELLS"and r["raw_SIGNED_pair"]is False and r["raw_COMPLETE_pair"]is False and r["raw_positive_side_SIGNED_pair"]is False and r["raw_positive_side_COMPLETE_pair"]is False,"fast contact binding")
  fast_reverse={(r["graph_id"],r["target_member_id"]):r for r in reverse_rows};need(set(fast_reverse)==set(fast_neg)and len(fast_neg)==9392,"fast reverse cover")
  for k,r in fast_reverse.items():need(r["positive_factor_row_sha256"]==fast_pos[k]["row_sha256"]and r["empty_factor_row_sha256"]==fast_neg[k]["row_sha256"],"fast reverse binding")
  fast_cross={k:r for k,r in fast_contacts.items()if not r["g2a_target_components_equal"]};fast_cross_rows={(r["graph_id"],r["target_member_id"]):r for r in cross_rows};need(len(fast_cross)==596 and set(fast_cross_rows)==set(fast_cross),"fast cross cover")
  for k,r in fast_cross_rows.items():need(r["contact_alias_route_row_sha256"]==fast_cross[k]["row_sha256"]and r["g2a_target_components_distinct"]is True,"fast cross binding")
  fast_edge_groups=defaultdict(list)
  for r in fast_cross.values():fast_edge_groups[tuple(sorted((r["g2a_component_id"],r["target_component_id"])))].append(r["row_sha256"])
  fast_edges={tuple(r["unordered_component_pair"]):r for r in edge_rows};need(len(fast_edge_groups)==144 and set(fast_edges)==set(fast_edge_groups),"fast edge cover")
  for k,rows in fast_edge_groups.items():need(fast_edges[k]["contact_alias_witness_count"]==len(rows)and fast_edges[k]["contact_alias_route_row_sha256s"]==sorted(rows),"fast edge binding")
  fast_routes={r["graph_id"]:r for r in route_rows};fast_final={r["graph_id"]:r for r in final_rows};fast_comp={r["graph_id"]:r for r in complement_rows};need(len(fast_routes)==len(fast_final)==5264,"fast route cover")
  for gid,r in fast_routes.items():
   n=r["C22_contact_candidate_count"];terminal="NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"if n==0 else"SAME_CHART_RELATIVE_CELLS";need(fast_final[gid]["contact_alias_count"]==n and fast_final[gid]["C23_contact_count"]==0 and fast_final[gid]["assigned_unique_terminal"]==terminal,"fast final route")
   need((gid in fast_comp)==(n==0),"fast complement cover")
  need(tr["global_three_terminal_unique_assignment"]is False and tr["positive_C19_91672_intersection_gate"].startswith("OPEN")and tr["C23_zero_proof"]["candidate_count"]==0 and tr["formal_credit"]==0,"fast scoped nonpromotion")
  if a.front_gate_only:
   result={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-front-gate-verification.v2","status":"PASS_INDEPENDENT_FRONT_GATE__SCOPED_G2A_OUTPUT_BINDINGS__ZERO_CREDIT","invocation_seed":a.seed,"front_gate_only":True,"census":{"routes":5264,"G2A_candidates":9408,"G2B_candidates":18800,"positive":9408,"empty":9392,"contacts":9408,"reverse":9392,"complement":552,"cross_C15":596,"component_edges":144},"global_three_terminal_unique_assignment":False,"positive_C19_91672_gate":"OPEN","input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.att()for k,v in sorted(caps.items())}},"formal_credit":0}
   result["semantic_projection_sha256"]=digest({k:v for k,v in result.items()if k not in{"invocation_seed","input_capture"}});result["result_sha256"]=digest(result);(out/"verification.json").write_bytes(canonical(result)+b"\n");return result
  for name,pin in PINS.items():caps[name]=Capture.open(name,ROOT/name,pin)

  p235={r["endpoint_graph_partition_row_id"]:r["source_chart"]for r in cert(caps[R235])["single_endpoint_graph_partition_rows"]}
  p242={r["transition_sheet_patch_row_id"]:r["source_chart"]for r in cert(caps[R242])["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]}
  p236={r["double_endpoint_partition_row_id"]:r["same_sign_event_absent_signature"]["source_chart"]for r in cert(caps[R236])["double_endpoint_partition_rows"]}
  c4={}
  for r in caps[C4].rows():commit=r["canonical_input_commitment"];c4[r["bridge_ordinal"]]=(commit["B1G0_source_graph_row"],p236[commit["R236_double_endpoint_partition_row"][1]])
  c5={}
  for r in caps[C5].rows():
   sem=r["semantic_classification"]
   if sem["classification"]=="POSITIVE_GRAPH":
    ch=c4[r["canonical_input_commitment"]["C4_bridge_row"][0]][1]if sem["kernel"]=="SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE"else None;c5[r["graph_id"]]=ch
  graphs={}
  for r in caps[C10].rows():
   gid=r["graph_id"];cl=r["graph_class"]
   ch=p235[gid]if cl in{"R235_TARGET_POSITIVE_PARTIAL_BASE","R235_SOURCE_EXACT_FACE_FULL_BASE"}else p242[gid]if cl=="R242_UNIQUE_GRAPH_FULL_PATCH"else c5[gid]
   unit,core=strip_unit(r["equation_ast"]["left"]);need(unit==1 and r["equation_ast"]["op"]=="EQ"and is_zero(r["equation_ast"]["right"]),"C10 equation");graphs[gid]={"chart":ch,"box":intervals(r["carrier_domain_ast"]),"class":cl,"row":r,"core":core,"core_sha":digest(core)}
  need(len(graphs)==5264,"C10 graph census")
  c14={}
  for r in caps[C14A].rows():c14[r["row_id"]]=(r["graph_id"],r["sheet_member_id"],r["row_sha256"],"C14A_EQ")
  for r in caps[C14B].rows():c14[r["row_id"]]=(r["graph_id"],r["new_exact_sheet_member_id"],r["row_sha256"],"C14B_EQ")
  need(len(c14)==5264,"C14 census")
  g2a={};sides=defaultdict(list);member_need=set()
  for r in caps[C24].rows():
   gid=r["graph_id"];need(gid in graphs,"C24 graph");member_need.add(r["member_id"])
   if r["coarse_family"]=="G2A":
    au=r["semantic_theorem_ast"]["sealed_exact_support_authority"];need(au["row_id"]in c14 and c14[au["row_id"]]==(gid,r["member_id"],au["row_sha256"],au["role"]),"C24/C14 exact equality");need(gid not in g2a,"unique G2A graph");g2a[gid]=r
   else:sides[gid].append(r)
  need(len(g2a)==5264 and sum(map(len,sides.values()))==9960 and set(g2a)==set(sides),"C24 G2 census")
  targets:dict[str,list[Target]]=defaultdict(list);target_by_row={}
  for r in caps[C22].rows():
   support=r["support_ast"];m=r["owner_member_id"];member_need.add(m);t=Target(m,"C22A",support["coordinate_chart"],tuple(map(Q,support["bounds"])),None,r);targets[t.chart].append(t);target_by_row[r["row_sha256"]]=t
  c23_count=0
  for r in caps[C23].rows():
   support=r["support_ast"];m=r["owner_member_id"];member_need.add(m);t=Target(m,"C23A",support["recharted_target_chart"],tuple(map(Q,support["bounds"])),support["physical_t_sign"],r);targets[t.chart].append(t);target_by_row[r["row_sha256"]]=t;c23_count+=1
  need(sum(map(len,targets.values()))==305592 and len(target_by_row)==305592 and c23_count==10252,"target census")
  components={};keys={};c15sha={}
  for r in caps[C15].rows():
   m=r["registry_member_id"]
   if m in member_need:components[m]=r["fresh_component_id"];keys[m]=r["official_key_id"];c15sha[m]=r["row_sha256"]
  need(set(components)==member_need,"C15 relevant totality")
  c25={}
  for r in caps[C25].rows():
   if r["member_id"]in member_need:c25[r["member_id"]]=r["source_bindings"]
  need(set(c25)==member_need,"C25 relevant totality")
  for gid,r in g2a.items():need(c25[r["member_id"]]["support_kernel"]=="C24A"and c25[r["member_id"]]["support_kernel_row_sha256"]==r["row_sha256"]and r["fresh_component_id"]==components[r["member_id"]],"G2A C15/C25")
  for rs in sides.values():
   for r in rs:need(c25[r["member_id"]]["support_kernel"]=="C24A"and c25[r["member_id"]]["support_kernel_row_sha256"]==r["row_sha256"]and r["fresh_component_id"]==components[r["member_id"]],"G2B C15/C25")
  for t in target_by_row.values():need(c25[t.member]["support_kernel"]==("C22B"if t.source=="C22A"else"C23B"),"target C25")
  g1=set();g2af=set()
  for r in caps[C26].rows():
   if r["node_id"]=="G1":g1.add(r["feature_id"])
   elif r["node_id"]=="G2A":g2af.add(r["feature_id"])
  need(g1==set(g2a)and g2af=={r["member_id"]for r in g2a.values()},"C26 exact G1/G2A cover")

  expected_g2a={};expected_g2b={};c23_hits=[]
  for chart in sorted(targets):
   tg=targets[chart]
   left=[Carrier(gid,gid,r["member_id"],chart,graphs[gid]["box"],components[r["member_id"]],r)for gid,r in g2a.items()if graphs[gid]["chart"]==chart]
   def emit_g2a(x:Carrier,t:Target)->None:
    z=box_intersection(x.box,t.box)if t.source=="C22A"else t2_intersection(x.box,t.box,t.sign)
    if z is None:return
    if t.source=="C23A":c23_hits.append((x.graph,t.member));return
    key=(x.graph,t.member);need(key not in expected_g2a,"duplicate G2A graph/member candidate");expected_g2a[key]=(z,t.row["row_sha256"])
   bucket_scan(left,tg,emit_g2a)
   side_left=[]
   for gid,rows in sides.items():
    if graphs[gid]["chart"]!=chart:continue
    for r in rows:side_left.append(Carrier(r["member_id"],gid,r["member_id"],chart,intervals(r["normalized_support_ast"]),components[r["member_id"]],r))
   def emit_g2b(x:Carrier,t:Target)->None:
    z=box_intersection(x.box,t.box)if t.source=="C22A"else t2_intersection(x.box,t.box,t.sign)
    if z is None:return
    need(t.source=="C22A","G2B/C23 gap");key=(x.member,t.member);need(key not in expected_g2b,"duplicate G2B side/member candidate");expected_g2b[key]=(z,t.row["row_sha256"])
   bucket_scan(side_left,tg,emit_g2b)
  need(len(expected_g2a)==9408 and len(expected_g2b)==18800 and not c23_hits,"independent event-sweep census")
  g2a_out={(r["graph_id"],r["target_member_id"]):r for r in g2a_rows};g2b_out={(r["c24_member_id"],r["target_member_id"]):r for r in g2b_rows};need(set(g2a_out)==set(expected_g2a)and set(g2b_out)==set(expected_g2b),"event-sweep exact candidate sets")
  for k,(z,tsha) in expected_g2a.items():
   r=g2a_out[k];g=g2a[k[0]];t=target_by_row[tsha];need(r["target_C22_row_sha256"]==tsha and r["outer_envelope_intersection_box"]==boxtext(z)and r["g2a_component_id"]==components[g["member_id"]]and r["target_component_id"]==components[t.member]and r["components_equal"]==(components[g["member_id"]]==components[t.member]),"G2A candidate semantics")
  side_by_member={r["member_id"]:r for rows in sides.values()for r in rows}
  for k,(z,tsha) in expected_g2b.items():
   r=g2b_out[k];s=side_by_member[k[0]];t=target_by_row[tsha];p=strict_predicate(s["normalized_support_ast"]);need(r["target_row_sha256"]==tsha and r["exact_envelope_intersection_box"]==boxtext(z)and r["c24_predicate_op"]==p["op"]and r["c24_predicate_ast_sha256"]==digest(p)and r["current_C15_components_equal"]==(components[s["member_id"]]==components[t.member]),"G2B candidate semantics")
  chart_graphs=Counter(graphs[g]["chart"]for g in g2a);chart22=Counter(t.chart for t in target_by_row.values()if t.source=="C22A");chart23=Counter(t.chart for t in target_by_row.values()if t.source=="C23A");den22=sum(chart_graphs[c]*chart22[c]for c in chart_graphs);den23=sum(chart_graphs[c]*chart23[c]for c in chart_graphs)
  need(cr["G2A"]["C22_same_chart_full_pair_denominator"]==den22==388915528 and cr["G2A"]["C23_same_chart_full_pair_denominator"]==den23==13491560 and cr["G2A"]["C23_outer_candidate_count"]==0,"denominator/C23 proof")

  authids={"C11A":set(),"C11B":set(),"C12A":set()}
  for s in side_by_member.values():authids[s["semantic_theorem_ast"]["sealed_exact_support_authority"]["role"]].add(s["semantic_theorem_ast"]["sealed_exact_support_authority"]["row_id"])
  a11={r["row_id"]:r for r in caps[C11A].rows()if r["row_id"]in authids["C11A"]};b11={};interfaces=set()
  for r in caps[C11BR].rows():
   if r["row_id"]in authids["C11B"]:b11[r["row_id"]]=r;interfaces.add(r["interface_kernel_ref"]["row_id"])
  bi11={r["row_id"]:r for r in caps[C11BI].rows()if r["row_id"]in interfaces};a12={r["row_id"]:r for r in caps[C12A].rows()if r["row_id"]in authids["C12A"]}
  need(set(a11)==authids["C11A"]and set(b11)==authids["C11B"]and set(a12)==authids["C12A"]and set(bi11)==interfaces,"side authority totality")
  factor_out={(r["side_member_id"],r["target_member_id"]):r for r in factor_rows};need(set(factor_out)==set(expected_g2b),"factor output candidate cover");disp=Counter();role_disp=Counter()
  for k in sorted(expected_g2b):
   side=side_by_member[k[0]];target=target_by_row[g2b_out[k]["target_row_sha256"]];pred=strict_predicate(side["normalized_support_ast"]);unit,core=strip_unit(pred["left"]);need(is_zero(pred["right"]),"side zero predicate");required=1 if pred["op"]=="GT"else-1;theorem=target.row["theorem_ast"];source_auth=theorem["sealed_source_authority"];sealed=side["semantic_theorem_ast"]["sealed_exact_support_authority"];role=sealed["role"]
   if role=="C11A":
    ar=a11[sealed["row_id"]];need(ar["row_sha256"]==sealed["row_sha256"]and ar["side_member_id"]==side["member_id"],"C11A binding");part=ar["partition_semantic_ref"]
    if part["kind"]=="R235_SINGLE_ENDPOINT_GRAPH_PARTITION_ROW":active=part["active_endpoint_factor"];factor_sign=sgn(source_auth["witness_"+active+"_factor_sign"])
    else:need(part["kind"]=="R236_DOUBLE_ENDPOINT_PARTITION_PLUS_C4_SOURCE_BRIDGE","C11A R235D");factor_sign=simple_t_sign(graphs[side["graph_id"]]["core"],target.row["support_ast"]["bounds"])
   elif role=="C11B":
    ar=b11[sealed["row_id"]];iface=bi11[ar["interface_kernel_ref"]["row_id"]];need(ar["row_sha256"]==sealed["row_sha256"]and iface["row_sha256"]==ar["interface_kernel_ref"]["row_sha256"]and unit==1,"C11B binding");factor_sign=sgn(source_auth["region_factor_sign"]);need(sgn(ar["one_sided_direction_receipt"]["factor_sign_on_side"])==required,"C11B side sign")
   else:
    need(role=="C12A","C12A role");ar=a12[sealed["row_id"]];need(ar["row_sha256"]==sealed["row_sha256"]and ar["side_member_id"]==side["member_id"],"C12A binding");factor_sign=simple_t_sign(graphs[side["graph_id"]]["core"],target.row["support_ast"]["bounds"])
   actual=unit*factor_sign;expected="EXACT_POSITIVE_SUPPORT"if actual==required else"EXACT_EMPTY_INTERSECTION";row=factor_out[k];need(row["disposition"]==expected and row["authority_role"]==role and row["candidate_row_sha256"]==g2b_out[k]["row_sha256"]and row["components"]==[components[k[0]],components[k[1]]],"independent factor classification");disp[expected]+=1;role_disp[role+"|"+expected]+=1
  need(disp=={"EXACT_POSITIVE_SUPPORT":9408,"EXACT_EMPTY_INTERSECTION":9392}and role_disp=={"C11A|EXACT_POSITIVE_SUPPORT":8870,"C11A|EXACT_EMPTY_INTERSECTION":8864,"C11B|EXACT_POSITIVE_SUPPORT":528,"C11B|EXACT_EMPTY_INTERSECTION":528,"C12A|EXACT_POSITIVE_SUPPORT":10},"factor census")

  pos=defaultdict(list);neg=defaultdict(list)
  for r in factor_rows:(pos if r["disposition"]=="EXACT_POSITIVE_SUPPORT"else neg)[(r["graph_id"],r["target_member_id"])].append(r)
  g2a_by_graph_target={(r["graph_id"],r["target_member_id"]):r for r in g2a_rows};need(set(pos)==set(g2a_by_graph_target)and all(len(v)==1 for v in pos.values()),"9408 G2A-positive bijection")
  authority_by_sha={}
  for role,rows in(("C11A",a11.values()),("C11B",b11.values()),("C12A",a12.values())):
   for r in rows:authority_by_sha[(role,r["row_sha256"])]=(r,relative_certificate(role,r))
  signed=set()
  for r in document_rows(caps[SIGNED]):
   if r["decision"].startswith("ACCEPT_")and r["left_formal_occurrence_id"]!=r["right_formal_occurrence_id"]:signed.add(tuple(sorted((r["left_formal_occurrence_id"],r["right_formal_occurrence_id"]))))
  complete=set()
  for r in document_rows(caps[COMPLETE]):
   if not r["decision"].startswith("ACCEPT_"):continue
   for x in r["left_formal_occurrence_endpoints"]:
    for y in r["right_formal_occurrence_endpoints"]:
     if x!=y:complete.add(tuple(sorted((x,y))))
  contact_out={(r["graph_id"],r["target_member_id"]):r for r in contact_rows};need(set(contact_out)==set(pos),"contact exact cover");same=cross=0
  for k in sorted(pos):
   c=g2a_by_graph_target[k];p=pos[k][0];outrow=contact_out[k];need(p["components"][0]==c["g2a_component_id"]and p["components"][1]==c["target_component_id"],"positive/G2A component handoff");ar,certsha=authority_by_sha[(p["authority_role"],p["authority_row_sha256"])];need(outrow["G2A_outer_candidate_row_sha256"]==c["row_sha256"]and outrow["positive_factor_disposition_row_sha256"]==p["row_sha256"]and outrow["relative_boundary_certificate_sha256"]==certsha and outrow["g2a_and_positive_side_same_C15_component"]is True,"contact proof binding");pair=tuple(c["unordered_member_pair"]);sidepair=tuple(sorted((p["side_member_id"],p["target_member_id"])));need(pair not in signed and pair not in complete and sidepair not in signed and sidepair not in complete,"raw terminal disjointness");same+=int(c["components_equal"]);cross+=int(not c["components_equal"])
  need((same,cross)==(8812,596),"same/cross contact census")
  reverse_out={(r["graph_id"],r["target_member_id"]):r for r in reverse_rows};expected_reverse={k for k in pos if len(neg.get(k,[]))==1};need(len(expected_reverse)==9392 and set(reverse_out)==expected_reverse and sum(k not in neg for k in pos)==16,"reverse-side exact cover")
  for k in expected_reverse:need(reverse_out[k]["positive_factor_row_sha256"]==pos[k][0]["row_sha256"]and reverse_out[k]["empty_factor_row_sha256"]==neg[k][0]["row_sha256"],"reverse row binding")
  route_input={r["graph_id"]:r for r in route_rows};final_out={r["graph_id"]:r for r in final_rows};complement_out={r["graph_id"]:r for r in complement_rows};need(set(route_input)==set(final_out)==set(g2a),"route graph cover")
  by_graph=Counter(k[0]for k in expected_g2a);zero={g for g in g2a if by_graph[g]==0};need(len(zero)==552 and set(complement_out)==zero,"552 complement cover")
  for gid in g2a:
   n=by_graph[gid];terminal="NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"if n==0 else"SAME_CHART_RELATIVE_CELLS";need(final_out[gid]["contact_alias_count"]==n and final_out[gid]["C23_contact_count"]==0 and final_out[gid]["assigned_unique_terminal"]==terminal,"final scoped route")
   if n==0:need(graphs[gid]["class"]=="R235_SOURCE_EXACT_FACE_FULL_BASE"and len(sides[gid])==1 and complement_out[gid]["one_sided_member_id"]==sides[gid][0]["member_id"],"one-sided complement")
  cross_contact={k:r for k,r in contact_out.items()if not r["g2a_target_components_equal"]};cross_out={(r["graph_id"],r["target_member_id"]):r for r in cross_rows};need(set(cross_out)==set(cross_contact),"596 cross witness cover");edge_groups=defaultdict(list)
  for k,r in cross_contact.items():edge_groups[tuple(sorted((r["g2a_component_id"],r["target_component_id"])))].append(r["row_sha256"])
  edge_out={tuple(r["unordered_component_pair"]):r for r in edge_rows};need(len(edge_groups)==144 and set(edge_out)==set(edge_groups),"144 component edge cover")
  for k,rows in edge_groups.items():need(edge_out[k]["contact_alias_witness_count"]==len(rows)and edge_out[k]["contact_alias_route_row_sha256s"]==sorted(rows),"component edge binding")
  need(tr["G2A_candidate_to_positive_side_bijection"]=={"join_key":["graph_id","target_member_id"],"domain_G2A_candidates":9408,"codomain_positive_side_dispositions":9408,"matched":9408,"missing":0,"duplicate":0}and tr["C23_zero_proof"]=={"G2A_graph_count":5264,"same_chart_full_pair_denominator":13491560,"candidate_count":0,"materialized_route_rows_with_C23_contact_count_zero":5264},"theorem summary binds recomputation")
  need(tr["unique_route_assignment_within_G2A_and_checked_raw_SIGNED_COMPLETE_scope"]is True and tr["global_three_terminal_unique_assignment"]is False and tr["positive_C19_91672_intersection_gate"].startswith("OPEN")and tr["formal_credit"]==0,"strict scoped nonpromotion")
  result={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-independent-verification.v2","status":"PASS_INDEPENDENT_EXACT_PS_CELL_BUCKET_AND_FACTOR_RECOMPUTATION__SCOPED_G2A_5264__POSITIVE_C19_OPEN__ZERO_CREDIT","invocation_seed":a.seed,"independent_implementation":{"imports_candidate_classifier_theorem_or_shared_module":False,"candidate_algorithm":"EXACT_PS_HALF_OPEN_CELL_BUCKET_INDEX_WITH_RATIONAL_ENDPOINT_BISECTION_AND_T_FILTER","factor_algorithm":"DIRECT_ROLE_AUTHORITY_SIGN_EVALUATION"},"census":{"G2A_graphs":5264,"G2A_candidates":9408,"G2B_candidates":18800,"positive":9408,"empty":9392,"reverse_empty":9392,"single_side_no_reverse":16,"complement":552,"C23_candidates":0,"same_C15":8812,"cross_C15":596,"unique_cross_C15_component_edges":144},"raw_terminal_pair_intersections":{"G2A_target_SIGNED":0,"G2A_target_COMPLETE":0,"positive_side_target_SIGNED":0,"positive_side_target_COMPLETE":0},"scoped_unique_route_assignment":True,"positive_C19_91672_gate":"OPEN","global_three_terminal_unique_assignment":False,"historical_edge_or_validation_ledger_opened":False,"C27_FAMILIES_imported_or_read":False,"input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{k:v.att()for k,v in sorted(caps.items())}},"formal_credit":0,"strict_nonpromotion":{"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"}}
  result["semantic_projection_sha256"]=digest({k:v for k,v in result.items()if k not in{"invocation_seed","input_capture"}});result["result_sha256"]=digest(result);(out/"verification.json").write_bytes(canonical(result)+b"\n");return result
 finally:
  for cap in caps.values():cap.close()


def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--out-dir",required=True);p.add_argument("--candidate-result",required=True);p.add_argument("--candidate-result-sha256",required=True);p.add_argument("--factor-result",required=True);p.add_argument("--factor-result-sha256",required=True);p.add_argument("--theorem-result",required=True);p.add_argument("--theorem-result-sha256",required=True);p.add_argument("--shared-implementation-source",required=True);p.add_argument("--shared-implementation-sha256",required=True);p.add_argument("--front-gate-only",action="store_true");p.add_argument("--seed",type=int,required=True);a=p.parse_args()
 try:r=verify(a)
 except(Failure,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));return 2
 print(canonical({"status":r["status"],"result_sha256":r["result_sha256"],"semantic_projection_sha256":r["semantic_projection_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
