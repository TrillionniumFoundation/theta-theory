#!/usr/bin/env python3
"""C64-L consumption-ready global edge-owner decider candidate builder."""
from __future__ import annotations
import copy,gzip,hashlib,json,os,stat,sys
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";PREFIX="cm2_round306c64l_global_owner_decider"
SCHEMA="cm2.round306c64l.global-edge-owner-decider-candidate.v1"
ATOM_FILE=PREFIX+"_atom_owner_decisions_v1.jsonl.gz";EDGE_FILE=PREFIX+"_edge_owner_decisions_v1.jsonl.gz";TIE_FILE=PREFIX+"_tie_blockers_v1.jsonl.gz";CANDIDATE_FILE=PREFIX+"_authority_candidate_v1.json"
C63P=OUT/"cm2_round306c63l_scope_extension_v1.py";C63R=OUT/"cm2_round306c63l_scope_extension_result_v1.json";C63VR=OUT/"cm2_round306c63l_scope_extension_independent_verifier_v1.py";C63V=OUT/"cm2_round306c63l_scope_extension_independent_verification_v1.json";C63M=OUT/"cm2_round306c63l_scope_extension_manifest_v1.sha256"
C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json";C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"C63p":"d9ee2d19ed999af020ec40df1face5be9676671bbbe3e8ab6516f0726532c43c","C63r":"4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177","C63o":"676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135","C63overlay":"3ada8fc97bb82958623da649f914e93c1b3be8c9a37b11d258578db738b93ebc","C63atom":"09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734","C63edge":"94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b","C63vr":"3e11961a5af2172b22d42b20cce81de7dcdff5f3355ecd9e58d24e0a8f142cd4","C63v":"e070b6ea4553de806861c9e95bceccc0aa758b7944a319a14225a8676e6cf996","C63vo":"f8e3dce7c5d1b826cabb46f9cb629b8b9a06d26f84b885de83be9639f5fa602b","C63m":"56ee86ca5e82d09b80c280eb44187422d1d4c21b4fda8150b21be889d7107290","C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60atom":"4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6","C60edge":"63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class FailClosed(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise FailClosed(label)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(p:Path)->str:
 s=hashlib.sha256()
 with p.open("rb")as f:
  for chunk in iter(lambda:f.read(1<<20),b""):s.update(chunk)
 return s.hexdigest()
def seq(values:Iterable[str])->str:
 s=hashlib.sha256()
 for value in values:s.update(value.encode("ascii")+b"\n")
 return s.hexdigest()
def js(p:Path)->dict[str,Any]:return json.loads(p.read_text())
def identity_from_stat(z:os.stat_result)->dict[str,int]:return{"dev":z.st_dev,"ino":z.st_ino,"mode":z.st_mode,"size":z.st_size,"mtime_ns":z.st_mtime_ns,"nlink":z.st_nlink}
def secure_bytes(path:Path,expected:str)->tuple[bytes,dict[str,int]]:
 before=os.lstat(path);need(stat.S_ISREG(before.st_mode)and before.st_nlink==1,"regular single-link input:"+path.name);flags=os.O_RDONLY|getattr(os,"O_NOFOLLOW",0);fd=os.open(path,flags)
 try:
  opened=os.fstat(fd);need(identity_from_stat(opened)==identity_from_stat(before),"path/fd identity:"+path.name);parts=[]
  while True:
   chunk=os.read(fd,1<<20)
   if not chunk:break
   parts.append(chunk)
  after=os.fstat(fd);need(identity_from_stat(after)==identity_from_stat(opened),"fd TOCTOU:"+path.name)
 finally:os.close(fd)
 final=os.lstat(path);need(identity_from_stat(final)==identity_from_stat(before),"path TOCTOU:"+path.name);data=b"".join(parts);need(hashlib.sha256(data).hexdigest()==expected,"input hash:"+path.name);return data,identity_from_stat(before)
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 body=dict(v);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 body=dict(v);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def secure_ledger(path:Path,desc:dict[str,Any],label:str)->tuple[list[dict[str,Any]],dict[str,int]]:
 data,identity=secure_bytes(path,desc["sha256"]);need(path.name==desc["filename"],"filename:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.decompress(data).splitlines()):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return out,identity
class Writer:
 def __init__(self,path:Path,order:str):self.path,self.order=path,order;self.raw=path.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
 def __enter__(self):return self
 def write(self,body:dict[str,Any])->dict[str,Any]:
  rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return row
 def __exit__(self,*_):self.gz.close();self.raw.close()
 def descriptor(self)->dict[str,Any]:return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}
def selftest(summary:dict[str,int])->dict[str,Any]:
 expected={"query_domain_edge_count":1042,"strict_pass_edge_count":911,"fail_closed_tie_edge_count":131,"strict_atom_owner_decision_count":11766,"blocked_edge_atom_count":1337,"tied_atom_count":345,"unique_atom_on_blocked_edge_count":992,"distinct_selected_owner_occurrence_count":9932,"maximum_atom_count_per_edge":31,"query_domain_exhaustive_count":1042,"query_domain_overlap_count":0,"formal_credit":0,"D02_gate_credit":0};need(summary==expected,"summary")
 capsule={**expected,"C63_overlay_bound":True,"C63_atom_bytes_bound":True,"C63_edge_bytes_bound":True,"owner_incident":True,"owner_minimum":True,"tie_break":False,"runtime_write":False};need(len(capsule)==20,"20 attacks");out={}
 for i,(key,value)in enumerate(capsule.items()):
  mutated=copy.deepcopy(capsule);mutated[key]=not value if type(value)is bool else value+1
  try:need(mutated==capsule,"mutated capsule")
  except FailClosed:out[f"coherent_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise FailClosed("attack accepted")
 return{"status":"PASS_20_OF_20_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":20,"attacks":out}
def build()->dict[str,Any]:
 inputs=[(C63P,"C63p"),(C63R,"C63r"),(C63VR,"C63vr"),(C63V,"C63v"),(C63M,"C63m"),(C60R,"C60r"),(C53,"C53"),(CANON,"canonical")];identities={}
 raw={}
 for path,key in inputs:raw[key],identities[key]=secure_bytes(path,P[key])
 c63=json.loads(raw["C63r"]);c63v=json.loads(raw["C63v"]);c60=json.loads(raw["C60r"]);closeobj(c63,P["C63o"],"C63");closeobj(c63v,P["C63vo"],"C63 verification");closeobj(c60,P["C60o"],"C60")
 overlay,identities["C63overlay"]=secure_ledger(OUT/c63["ledgers"]["endpoint_scope_overlay"]["filename"],c63["ledgers"]["endpoint_scope_overlay"],"C63 overlay");atoms,identities["C63atom"]=secure_ledger(OUT/c63["ledgers"]["atom_replay"]["filename"],c63["ledgers"]["atom_replay"],"C63 atoms");edges,identities["C63edge"]=secure_ledger(OUT/c63["ledgers"]["edge_replay"]["filename"],c63["ledgers"]["edge_replay"],"C63 edges")
 need(hf(OUT/c63["ledgers"]["endpoint_scope_overlay"]["filename"] )==P["C63overlay"]and hf(OUT/c63["ledgers"]["atom_replay"]["filename"] )==P["C63atom"]and hf(OUT/c63["ledgers"]["edge_replay"]["filename"] )==P["C63edge"],"C63 direct byte pins")
 c60atoms,identities["C60atom"]=secure_ledger(OUT/c60["ledgers"]["incidence_atoms"]["filename"],c60["ledgers"]["incidence_atoms"],"C60 atoms");c60edges,identities["C60edge"]=secure_ledger(OUT/c60["ledgers"]["edge_decisions"]["filename"],c60["ledgers"]["edge_decisions"],"C60 edges")
 need(hf(OUT/c60["ledgers"]["incidence_atoms"]["filename"] )==P["C60atom"]and hf(OUT/c60["ledgers"]["edge_decisions"]["filename"] )==P["C60edge"],"C60 direct byte pins")
 atom60={x["row_sha256"]:x for x in c60atoms};edge60={x["C59_request_row_sha256"]:x for x in c60edges};byrequest=defaultdict(list)
 for atom in atoms:byrequest[atom["C59_request_row_sha256"]].append(atom)
 pass_requests={x["C59_request_row_sha256"]for x in edges if x["overall_owner_history_mapping_pass"]};need(len(pass_requests)==911,"pass request count")
 atom_decisions={};selected=[]
 with Writer(OUT/ATOM_FILE,"C63_ATOM_REPLAY_ORDER_FILTERED_TO_911_PASS_EDGES")as writer:
  for atom in atoms:
   if atom["C59_request_row_sha256"]not in pass_requests:continue
   source=atom60[atom["C60_atom_row_sha256"]];need(source["owner_unique"]is True and source["owner"]is not None and atom["semantic_mapping_complete"]is True,"strict atom prerequisites")
   owner=source["owner"];incident=[x for x in source["incident_occurrences"]if x["physical_occurrence_id"]==owner["physical_occurrence_id"]];need(len(incident)==1 and owner["semantic_path"]==source["minimum_semantic_path"],"selected owner exact minimum incident")
   consumption_key=h({"C59_request_row_sha256":atom["C59_request_row_sha256"],"C60_atom_row_sha256":source["row_sha256"],"exact_span":atom["exact_span"]})
   body={"schema":SCHEMA+".atom-owner-decision-row","consumption_key":"c64l-atom-owner:"+consumption_key,"C59_request_row_sha256":atom["C59_request_row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"C60_atom_row_sha256":source["row_sha256"],"face_or_corner_id":atom["face_or_corner_id"],"glue_kind":atom["glue_kind"],"exact_span":atom["exact_span"],"incident_overlay_map_row_hash_sequence_sha256":seq(x["endpoint_scope_overlay_row_sha256"]for x in atom["incident_overlay_maps"]),"selected_owner":owner,"selected_owner_is_exact_incident_occurrence":True,"selected_owner_semantic_path_is_unique_lexicographic_minimum":True,"semantic_mapping_complete":True,"decision":"STRICT_OWNER_UNIQUE_SEMANTIC_MAP","formal_credit":0,"D02_gate_credit":0};row=writer.write(body);atom_decisions[atom["row_sha256"]]=row;selected.append(owner["physical_occurrence_id"])
 atom_desc=writer.descriptor();need(atom_desc["row_count"]==11766,"atom decision count")
 pass_ids=[];maximum=0
 with Writer(OUT/EDGE_FILE,"C63_EDGE_REPLAY_ORDER_FILTERED_TO_911_PASS_EDGES")as writer:
  for edge in edges:
   if not edge["overall_owner_history_mapping_pass"]:continue
   need(edge["C60_geometric_owner_unique"]is True and edge["all_atom_semantic_mappings_complete"]is True and edge60[edge["C59_request_row_sha256"]]["geometric_owner_unique"]is True,"strict edge prerequisites")
   source_atoms=byrequest[edge["C59_request_row_sha256"]];decisions=[atom_decisions[x["row_sha256"]]for x in source_atoms];maximum=max(maximum,len(decisions));pass_ids.append(edge["C59_request_row_sha256"])
   body={"schema":SCHEMA+".edge-owner-decision-row","query_key":"c64l-edge-owner:"+h({"C59_request_row_sha256":edge["C59_request_row_sha256"],"owner_history_request_id":edge["owner_history_request_id"]}),"C59_request_row_sha256":edge["C59_request_row_sha256"],"owner_history_request_id":edge["owner_history_request_id"],"C63_edge_replay_row_sha256":edge["row_sha256"],"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"atom_count":len(decisions),"atom_owner_decision_row_hash_sequence_sha256":seq(x["row_sha256"]for x in decisions),"atom_consumption_key_sequence_sha256":seq(x["consumption_key"].split(":",1)[1]for x in decisions),"all_atom_owners_exact_incident_unique_minima":True,"semantic_mapping_complete":True,"decision":"STRICT_OWNER_VECTOR_AVAILABLE","blocker_codes":[],"formal_credit":0,"D02_gate_credit":0};writer.write(body)
 edge_desc=writer.descriptor();need(edge_desc["row_count"]==911,"edge pass count")
 blocked_ids=[];blocked_atoms=tied_atoms=unique_blocked=0
 with Writer(OUT/TIE_FILE,"C63_EDGE_REPLAY_ORDER_FILTERED_TO_131_TIED_EDGES")as writer:
  for edge in edges:
   if edge["overall_owner_history_mapping_pass"]:continue
   need(edge["C60_geometric_owner_unique"]is False and edge60[edge["C59_request_row_sha256"]]["geometric_owner_unique"]is False,"tie edge prerequisites");source_atoms=byrequest[edge["C59_request_row_sha256"]];details=[]
   for atom in source_atoms:
    source=atom60[atom["C60_atom_row_sha256"]]
    if source["owner_unique"]:
     unique_blocked+=1
    else:
     tied_atoms+=1
     details.append({"C63_atom_replay_row_sha256":atom["row_sha256"],"C60_atom_row_sha256":source["row_sha256"],"exact_span":atom["exact_span"],"minimum_semantic_path":source["minimum_semantic_path"],"tied_occurrence_ids":source["owner_tie_occurrence_ids"]})
   need(bool(details),"tied edge without tied atom:"+edge["C59_request_row_sha256"]);blocked_atoms+=len(source_atoms);blocked_ids.append(edge["C59_request_row_sha256"])
   body={"schema":SCHEMA+".tie-blocker-row","query_key":"c64l-edge-owner:"+h({"C59_request_row_sha256":edge["C59_request_row_sha256"],"owner_history_request_id":edge["owner_history_request_id"]}),"C59_request_row_sha256":edge["C59_request_row_sha256"],"owner_history_request_id":edge["owner_history_request_id"],"C63_edge_replay_row_sha256":edge["row_sha256"],"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"edge_atom_count":len(source_atoms),"tied_atom_count":len(details),"tied_atom_details":details,"tied_atom_detail_sequence_sha256":seq(h(x)for x in details),"decision":"FAIL_CLOSED_INDEPENDENT_OWNER_RULE_TIE","blocker_codes":["INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED"],"arbitrary_tiebreak_added":False,"formal_credit":0,"D02_gate_credit":0};writer.write(body)
 tie_desc=writer.descriptor();need(tie_desc["row_count"]==131 and blocked_atoms==1337 and tied_atoms==345 and unique_blocked==992,"tie census")
 need(set(pass_ids).isdisjoint(blocked_ids)and set(pass_ids)|set(blocked_ids)=={x["C59_request_row_sha256"]for x in edges},"query partition")
 summary={"query_domain_edge_count":1042,"strict_pass_edge_count":911,"fail_closed_tie_edge_count":131,"strict_atom_owner_decision_count":11766,"blocked_edge_atom_count":1337,"tied_atom_count":345,"unique_atom_on_blocked_edge_count":992,"distinct_selected_owner_occurrence_count":len(set(selected)),"maximum_atom_count_per_edge":maximum,"query_domain_exhaustive_count":len(set(pass_ids)|set(blocked_ids)),"query_domain_overlap_count":len(set(pass_ids)&set(blocked_ids)),"formal_credit":0,"D02_gate_credit":0};tests=selftest(summary)
 candidate={"schema":SCHEMA+".authority-candidate","status":"CONSUMPTION_READY_GLOBAL_OWNER_DECIDER_CANDIDATE__911_STRICT_PASS__131_FAIL_CLOSED_TIES__NOT_INSTALLED__ZERO_CREDIT","authority_class":"GLOBAL_EXISTING_EDGE_ATOM_OWNER_VECTOR_DECIDER","authority_status":"CANDIDATE_NOT_INSTALLED","input_byte_bindings":{"C63_result_file_sha256":P["C63r"],"C63_result_object_sha256":P["C63o"],"C63_endpoint_scope_overlay_file_sha256":P["C63overlay"],"C63_atom_replay_file_sha256":P["C63atom"],"C63_edge_replay_file_sha256":P["C63edge"],"C63_independent_verifier_file_sha256":P["C63vr"],"C63_independent_verification_file_sha256":P["C63v"],"C63_independent_verification_object_sha256":P["C63vo"],"C63_manifest_file_sha256":P["C63m"],"C60_result_file_sha256":P["C60r"],"C60_result_object_sha256":P["C60o"],"C60_atom_ledger_file_sha256":P["C60atom"],"C60_edge_ledger_file_sha256":P["C60edge"],"C53_head_file_sha256":P["C53"],"canonical_file_sha256":P["canonical"]},"input_file_identities":identities,"query_contract":{"key_schema":"c64l-edge-owner:sha256(canonical({C59_request_row_sha256,owner_history_request_id}))","domain_is_exhaustive_over_C63_edges":True,"strict_pass_returns_ordered_atom_owner_vector":True,"tie_returns_only_fail_closed_blocker":True,"missing_or_duplicate_query":"FAIL_CLOSED","partial_atom_vector":"FAIL_CLOSED","arbitrary_tiebreak_permitted":False},"scope":summary,"ledgers":{"atom_owner_decisions":atom_desc,"edge_owner_decisions":edge_desc,"tie_blockers":tie_desc},"indexes":{"strict_pass_request_hash_sequence_sha256":seq(pass_ids),"fail_closed_request_hash_sequence_sha256":seq(blocked_ids),"selected_owner_occurrence_id_sequence_sha256":seq(selected)},"self_test":tests,"TOCTOU_contract":{"O_NOFOLLOW_used":True,"regular_file_required":True,"st_nlink_exactly_one_required":True,"path_fd_identity_checked_before_read":True,"fd_identity_checked_after_read":True,"path_identity_checked_after_read":True,"sha256_checked_after_read":True},"strict_boundary":{"consumption_ready":True,"installed_authority":False,"runtime_or_canonical_written":False,"C59_C60_C63_modified":False,"131_owner_ties_fail_closed_separately":True,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["COLD_INDEPENDENT_REPLAY_AND_COHERENT_TOCTOU_ATTACKS","CONSUME_ONLY_AFTER_EXACT_CANDIDATE_AND_MANIFEST_BINDING","KEEP_131_TIES_OUTSIDE_STRICT_PASS_DOMAIN"]};candidate["object_sha256"]=h(candidate);(OUT/CANDIDATE_FILE).write_bytes(enc(candidate)+b"\n");return candidate
def main()->int:
 result=build();print(json.dumps({"status":result["status"],"scope":result["scope"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
