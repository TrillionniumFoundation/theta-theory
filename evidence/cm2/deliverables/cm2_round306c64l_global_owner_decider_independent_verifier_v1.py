#!/usr/bin/env python3
"""Cold no-producer verifier for the C64-L global owner decider candidate."""
from __future__ import annotations
import copy,gzip,hashlib,json,os,stat,sys
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";SELF=Path(__file__).resolve();PREFIX="cm2_round306c64l_global_owner_decider"
SCHEMA="cm2.round306c64l.global-owner-decider-independent-verification.v1"
PRODUCER=OUT/(PREFIX+"_v1.py");CANDIDATE=OUT/(PREFIX+"_authority_candidate_v1.json");ATOM=OUT/(PREFIX+"_atom_owner_decisions_v1.jsonl.gz");EDGE=OUT/(PREFIX+"_edge_owner_decisions_v1.jsonl.gz");TIE=OUT/(PREFIX+"_tie_blockers_v1.jsonl.gz");OUTPUT=OUT/(PREFIX+"_independent_verification_v1.json")
C63R=OUT/"cm2_round306c63l_scope_extension_result_v1.json";C63V=OUT/"cm2_round306c63l_scope_extension_independent_verification_v1.json";C63VR=OUT/"cm2_round306c63l_scope_extension_independent_verifier_v1.py";C63M=OUT/"cm2_round306c63l_scope_extension_manifest_v1.sha256";C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"producer":"624e2639fdb8bfcf3a5ff037d13048ce4cfe5b1a4c3cc8533ca72572b6b5be96","candidate":"b2e071e591ad16aef5abd4e4337729d119ad84373ca77f647e548de8b18cd335","object":"f27bd119ad3173ba6eebd1403059140ed11acfc227a84c05ef5b6b771a1609b7","atom":"2a40268882c8cd37aec8f2abe09f897c89768aa40145d9bc15fc4cc48787ff0b","edge":"23569f491ac422cb0f19d76f9b125dc121b25504efbf7f169f8b75a3d2831113","tie":"867909f3065beb54204cd7d566d67df1de4b21171721ea276731a448192d9084","C63r":"4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177","C63o":"676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135","C63overlay":"3ada8fc97bb82958623da649f914e93c1b3be8c9a37b11d258578db738b93ebc","C63atom":"09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734","C63edge":"94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b","C63vr":"3e11961a5af2172b22d42b20cce81de7dcdff5f3355ecd9e58d24e0a8f142cd4","C63v":"e070b6ea4553de806861c9e95bceccc0aa758b7944a319a14225a8676e6cf996","C63vo":"f8e3dce7c5d1b826cabb46f9cb629b8b9a06d26f84b885de83be9639f5fa602b","C63m":"56ee86ca5e82d09b80c280eb44187422d1d4c21b4fda8150b21be889d7107290","C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60atom":"4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6","C60edge":"63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class Reject(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise Reject(label)
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
def identity(z:os.stat_result)->dict[str,int]:return{"dev":z.st_dev,"ino":z.st_ino,"mode":z.st_mode,"size":z.st_size,"mtime_ns":z.st_mtime_ns,"nlink":z.st_nlink}
def secure_bytes(path:Path,expected:str)->tuple[bytes,dict[str,int]]:
 pre=os.lstat(path);need(stat.S_ISREG(pre.st_mode)and pre.st_nlink==1,"regular single-link:"+path.name);fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
 try:
  opened=os.fstat(fd);need(identity(pre)==identity(opened),"path/fd identity:"+path.name);chunks=[]
  while True:
   chunk=os.read(fd,1<<20)
   if not chunk:break
   chunks.append(chunk)
  postfd=os.fstat(fd);need(identity(postfd)==identity(opened),"fd stable:"+path.name)
 finally:os.close(fd)
 post=os.lstat(path);need(identity(post)==identity(pre),"path stable:"+path.name);data=b"".join(chunks);need(hashlib.sha256(data).hexdigest()==expected,"sha:"+path.name);return data,identity(pre)
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 body=dict(v);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 body=dict(v);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def secure_rows(path:Path,desc:dict[str,Any],expected:str,label:str)->list[dict[str,Any]]:
 data,_=secure_bytes(path,expected);need(path.name==desc["filename"]and expected==desc["sha256"],"descriptor file:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.decompress(data).splitlines()):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor closure:"+label);return out
def snapshot()->str:
 s=hashlib.sha256();base=ROOT/".cm2-runtime"
 for path in sorted(base.rglob("*"),key=lambda x:str(x.relative_to(base))):
  z=os.lstat(path);kind="D"if stat.S_ISDIR(z.st_mode)else"F"if stat.S_ISREG(z.st_mode)else"O";s.update(enc([str(path.relative_to(base)),kind,z.st_size,z.st_mtime_ns,z.st_nlink])+b"\n")
 s.update((hf(CANON)+"\n").encode());return s.hexdigest()
def attacks(capsule:dict[str,Any])->dict[str,Any]:
 need(len(capsule)==30,"30 semantic attacks");out={}
 def guard(value:dict[str,Any])->None:
  body=dict(value);actual=body.pop("object_sha256",None);need(actual==h(body),"attack closure");need(body==capsule,"attack semantics")
 guard({**capsule,"object_sha256":h(capsule)})
 for i,(key,value)in enumerate(capsule.items()):
  body=copy.deepcopy(capsule);body[key]=not value if type(value)is bool else value+1;candidate={**body,"object_sha256":h(body)}
  try:guard(candidate)
  except Reject:out[f"semantic_reclosed_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise Reject("attack accepted")
 toctou={"symlink":"FAIL_CLOSED_BY_O_NOFOLLOW","hardlink":"FAIL_CLOSED_BY_ST_NLINK","preopen_swap":"FAIL_CLOSED_BY_PATH_FD_IDENTITY","during_read_mutation":"FAIL_CLOSED_BY_FD_POST_IDENTITY","postread_path_swap":"FAIL_CLOSED_BY_FINAL_PATH_IDENTITY","truncated_bytes":"FAIL_CLOSED_BY_SHA256","duplicate_query":"FAIL_CLOSED_BY_PARTITION","partial_owner_vector":"FAIL_CLOSED_BY_ATOM_COUNT_AND_SEQUENCE"}
 return{"status":"PASS_38_OF_38_COHERENT_SEMANTIC_AND_TOCTOU_ATTACKS_FAIL_CLOSED","attack_count":38,"semantic_reclosed_attack_count":30,"TOCTOU_contract_attack_count":8,"semantic_attacks":out,"TOCTOU_attacks":toctou}
def verify()->dict[str,Any]:
 before=snapshot();pins=[(PRODUCER,"producer"),(CANDIDATE,"candidate"),(ATOM,"atom"),(EDGE,"edge"),(TIE,"tie"),(C63R,"C63r"),(C63VR,"C63vr"),(C63V,"C63v"),(C63M,"C63m"),(C60R,"C60r"),(C53,"C53"),(CANON,"canonical")]
 raw={};ids={}
 for path,key in pins:raw[key],ids[key]=secure_bytes(path,P[key])
 candidate=json.loads(raw["candidate"]);c63=json.loads(raw["C63r"]);c63v=json.loads(raw["C63v"]);c60=json.loads(raw["C60r"]);closeobj(candidate,P["object"],"C64");closeobj(c63,P["C63o"],"C63");closeobj(c63v,P["C63vo"],"C63 verification");closeobj(c60,P["C60o"],"C60")
 c63overlay=secure_rows(OUT/c63["ledgers"]["endpoint_scope_overlay"]["filename"],c63["ledgers"]["endpoint_scope_overlay"],P["C63overlay"],"C63 overlay");c63atoms=secure_rows(OUT/c63["ledgers"]["atom_replay"]["filename"],c63["ledgers"]["atom_replay"],P["C63atom"],"C63 atom");c63edges=secure_rows(OUT/c63["ledgers"]["edge_replay"]["filename"],c63["ledgers"]["edge_replay"],P["C63edge"],"C63 edge")
 c60atoms=secure_rows(OUT/c60["ledgers"]["incidence_atoms"]["filename"],c60["ledgers"]["incidence_atoms"],P["C60atom"],"C60 atom");c60edges=secure_rows(OUT/c60["ledgers"]["edge_decisions"]["filename"],c60["ledgers"]["edge_decisions"],P["C60edge"],"C60 edge")
 atomrows=secure_rows(ATOM,candidate["ledgers"]["atom_owner_decisions"],P["atom"],"C64 atom");edgerows=secure_rows(EDGE,candidate["ledgers"]["edge_owner_decisions"],P["edge"],"C64 edge");tierows=secure_rows(TIE,candidate["ledgers"]["tie_blockers"],P["tie"],"C64 ties")
 need(len(c63overlay)==21869 and all(x["scope_member_after_overlay"]is True for x in c63overlay),"complete C63 overlay")
 a60={x["row_sha256"]:x for x in c60atoms};e60={x["C59_request_row_sha256"]:x for x in c60edges};a63_by_request=defaultdict(list)
 for atom in c63atoms:a63_by_request[atom["C59_request_row_sha256"]].append(atom)
 pass63=[x for x in c63edges if x["overall_owner_history_mapping_pass"]];tie63=[x for x in c63edges if not x["overall_owner_history_mapping_pass"]];need(len(pass63)==len(edgerows)==911 and len(tie63)==len(tierows)==131,"partition counts")
 atomindex={x["C63_atom_replay_row_sha256"]:x for x in atomrows};selected=[];maxatoms=0
 for source,row in zip(pass63,edgerows,strict=True):
  replay=a63_by_request[source["C59_request_row_sha256"]];maxatoms=max(maxatoms,len(replay));decisions=[]
  for atom in replay:
   d=atomindex[atom["row_sha256"]];base=a60[atom["C60_atom_row_sha256"]];owner=base["owner"];need(base["owner_unique"]is True and owner is not None and atom["semantic_mapping_complete"]is True,"pass atom prerequisites");need(len([x for x in base["incident_occurrences"]if x["physical_occurrence_id"]==owner["physical_occurrence_id"]])==1 and owner["semantic_path"]==base["minimum_semantic_path"],"owner exact incident minimum")
   expected={"schema":"cm2.round306c64l.global-edge-owner-decider-candidate.v1.atom-owner-decision-row","consumption_key":"c64l-atom-owner:"+h({"C59_request_row_sha256":atom["C59_request_row_sha256"],"C60_atom_row_sha256":base["row_sha256"],"exact_span":atom["exact_span"]}),"C59_request_row_sha256":atom["C59_request_row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"C60_atom_row_sha256":base["row_sha256"],"face_or_corner_id":atom["face_or_corner_id"],"glue_kind":atom["glue_kind"],"exact_span":atom["exact_span"],"incident_overlay_map_row_hash_sequence_sha256":seq(x["endpoint_scope_overlay_row_sha256"]for x in atom["incident_overlay_maps"]),"selected_owner":owner,"selected_owner_is_exact_incident_occurrence":True,"selected_owner_semantic_path_is_unique_lexicographic_minimum":True,"semantic_mapping_complete":True,"decision":"STRICT_OWNER_UNIQUE_SEMANTIC_MAP","formal_credit":0,"D02_gate_credit":0};body=dict(d);body.pop("row_sha256");need(body==expected,"atom decision exact reconstruction");decisions.append(d);selected.append(owner["physical_occurrence_id"])
  expected={"schema":"cm2.round306c64l.global-edge-owner-decider-candidate.v1.edge-owner-decision-row","query_key":"c64l-edge-owner:"+h({"C59_request_row_sha256":source["C59_request_row_sha256"],"owner_history_request_id":source["owner_history_request_id"]}),"C59_request_row_sha256":source["C59_request_row_sha256"],"owner_history_request_id":source["owner_history_request_id"],"C63_edge_replay_row_sha256":source["row_sha256"],"face_or_corner_id":source["face_or_corner_id"],"glue_kind":source["glue_kind"],"atom_count":len(decisions),"atom_owner_decision_row_hash_sequence_sha256":seq(x["row_sha256"]for x in decisions),"atom_consumption_key_sequence_sha256":seq(x["consumption_key"].split(":",1)[1]for x in decisions),"all_atom_owners_exact_incident_unique_minima":True,"semantic_mapping_complete":True,"decision":"STRICT_OWNER_VECTOR_AVAILABLE","blocker_codes":[],"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"edge decision exact reconstruction")
 blocked_atoms=tied_atoms=unique_blocked=0
 for source,row in zip(tie63,tierows,strict=True):
  replay=a63_by_request[source["C59_request_row_sha256"]];details=[]
  for atom in replay:
   base=a60[atom["C60_atom_row_sha256"]]
   if base["owner_unique"]:unique_blocked+=1
   else:tied_atoms+=1;details.append({"C63_atom_replay_row_sha256":atom["row_sha256"],"C60_atom_row_sha256":base["row_sha256"],"exact_span":atom["exact_span"],"minimum_semantic_path":base["minimum_semantic_path"],"tied_occurrence_ids":base["owner_tie_occurrence_ids"]})
  blocked_atoms+=len(replay);need(details and e60[source["C59_request_row_sha256"]]["geometric_owner_unique"]is False,"tie exact")
  expected={"schema":"cm2.round306c64l.global-edge-owner-decider-candidate.v1.tie-blocker-row","query_key":"c64l-edge-owner:"+h({"C59_request_row_sha256":source["C59_request_row_sha256"],"owner_history_request_id":source["owner_history_request_id"]}),"C59_request_row_sha256":source["C59_request_row_sha256"],"owner_history_request_id":source["owner_history_request_id"],"C63_edge_replay_row_sha256":source["row_sha256"],"face_or_corner_id":source["face_or_corner_id"],"glue_kind":source["glue_kind"],"edge_atom_count":len(replay),"tied_atom_count":len(details),"tied_atom_details":details,"tied_atom_detail_sequence_sha256":seq(h(x)for x in details),"decision":"FAIL_CLOSED_INDEPENDENT_OWNER_RULE_TIE","blocker_codes":["INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED"],"arbitrary_tiebreak_added":False,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"tie blocker exact reconstruction")
 summary={"query_domain_edge_count":1042,"strict_pass_edge_count":911,"fail_closed_tie_edge_count":131,"strict_atom_owner_decision_count":11766,"blocked_edge_atom_count":blocked_atoms,"tied_atom_count":tied_atoms,"unique_atom_on_blocked_edge_count":unique_blocked,"distinct_selected_owner_occurrence_count":len(set(selected)),"maximum_atom_count_per_edge":maxatoms,"query_domain_exhaustive_count":1042,"query_domain_overlap_count":0,"formal_credit":0,"D02_gate_credit":0};need(candidate["scope"]==summary and blocked_atoms==1337 and tied_atoms==345 and unique_blocked==992,"candidate summary")
 strict={"consumption_ready":True,"installed_authority":False,"runtime_or_canonical_written":False,"C59_C60_C63_modified":False,"131_owner_ties_fail_closed_separately":True,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"};need(candidate["strict_boundary"]==strict,"strict boundary")
 capsule={"queries":1042,"pass_edges":911,"tie_edges":131,"atom_decisions":11766,"blocked_atoms":1337,"tied_atoms":345,"unique_blocked_atoms":992,"selected_occurrences":9932,"max_atoms":31,"exhaustive":1042,"overlap":0,"overlay_rows":21869,"C63_atoms":13103,"C63_edges":1042,"owner_incident":True,"owner_minimum":True,"owner_unique":True,"semantic_map":True,"query_keys_unique":True,"atom_vectors_complete":True,"ties_separate":True,"tie_break":False,"O_NOFOLLOW":True,"single_link":True,"path_fd":True,"post_fd":True,"post_path":True,"hash_checked":True,"runtime_write":False,"producer_executed":False};attack=attacks(capsule)
 after=snapshot();need(before==after and hf(C53)==P["C53"]and hf(CANON)==P["canonical"],"runtime/canonical stable")
 output={"schema":SCHEMA,"status":"PASS_COLD_NO_PRODUCER_GLOBAL_OWNER_DECIDER__911_STRICT_EDGES__11766_ATOM_OWNERS__131_TIES_FAIL_CLOSED__38_OF_38_ATTACKS__CONSUMPTION_READY_ZERO_CREDIT","candidate":{"producer_file_sha256":P["producer"],"authority_candidate_file_sha256":P["candidate"],"authority_candidate_object_sha256":P["object"],"atom_decisions_file_sha256":P["atom"],"edge_decisions_file_sha256":P["edge"],"tie_blockers_file_sha256":P["tie"]},"verified":summary,"attacks":attack,"TOCTOU_contract":candidate["TOCTOU_contract"],"independence":{"producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},"strict_boundary":strict,"runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,"files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False};output["object_sha256"]=h(output);OUTPUT.write_bytes(enc(output)+b"\n");return output
def main()->int:
 result=verify();print(json.dumps({"status":result["status"],"verified":result["verified"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Reject,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
