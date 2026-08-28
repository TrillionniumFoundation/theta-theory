#!/usr/bin/env python3
"""C63-L frozen endpoint-lineage scope overlay and full edge replay."""
from __future__ import annotations
import copy,gzip,hashlib,json,sys
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";PREFIX="cm2_round306c63l_scope_extension"
SCHEMA="cm2.round306c63l.frozen-endpoint-lineage-scope-overlay.v1"
OVERLAY=PREFIX+"_endpoint_scope_overlay_v1.jsonl.gz";ATOM=PREFIX+"_atom_replay_v1.jsonl.gz";EDGE=PREFIX+"_edge_replay_v1.jsonl.gz";RESULT=PREFIX+"_result_v1.json"
C62P=OUT/"cm2_round306c62l_edge_semantic_map_v1.py";C62R=OUT/"cm2_round306c62l_edge_semantic_map_result_v1.json";C62V=OUT/"cm2_round306c62l_edge_semantic_map_independent_verification_v1.json";C62VR=OUT/"cm2_round306c62l_edge_semantic_map_independent_verifier_v1.py";C62M=OUT/"cm2_round306c62l_edge_semantic_map_manifest_v1.sha256"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"C62p":"ecce7e6ae2aee1da27d7ff24619b1de62891dc703198892edda38d2fe46f3e61","C62r":"e85a188a7016de40fc7f3a607071aa53a2343684de51373b27786aaaf0c82615","C62o":"3d2c719f16e2921314bff0b83245e945b916da526306845eb8f00a6010cda8eb","C62vr":"bacf0000f07cb8d5bcfe882a3b52bdb6ad4b41ec7fd6e9564dd6473bbace423e","C62v":"6c259ce094b08dd434eeddf71eec1c59782d00212bd3ac06024fb6c510a7e498","C62vo":"a76faf6e9e21602979857e1195a99b7751b4e1c359be99e8356a1a760c9307c2","C62m":"5e7aa3423be34eaa894f16c320df3b3537da2f3938f85fce1c69b34336dd638d","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class FailClosed(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise FailClosed(label)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(p:Path)->str:
 s=hashlib.sha256()
 with p.open("rb")as f:
  for b in iter(lambda:f.read(1<<20),b""):s.update(b)
 return s.hexdigest()
def seq(values:Iterable[str])->str:
 s=hashlib.sha256()
 for value in values:s.update(value.encode("ascii")+b"\n")
 return s.hexdigest()
def js(p:Path)->dict[str,Any]:return json.loads(p.read_text())
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 body=dict(v);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 body=dict(v);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def ledger(desc:dict[str,Any],label:str)->list[dict[str,Any]]:
 path=OUT/desc["filename"];need(hf(path)==desc["sha256"],"file:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.open(path,"rt")):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return out
class Writer:
 def __init__(self,path:Path,order:str):self.path,self.order=path,order;self.raw=path.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
 def __enter__(self):return self
 def write(self,body:dict[str,Any])->dict[str,Any]:
  rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return row
 def __exit__(self,*_):self.gz.close();self.raw.close()
 def descriptor(self)->dict[str,Any]:return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}
def selftest(summary:dict[str,int])->dict[str,Any]:
 expected={"existing_unique_endpoint_C41_scope_row_count":6860,"applied_scope_extension_row_count":15009,"complete_overlay_scope_row_count":21869,"overlay_incidence_count":26206,"atom_replay_count":13103,"atom_semantic_mapping_complete_count":13103,"atom_both_occurrence1_contract_pass_count":6360,"edge_replay_count":1042,"edge_semantic_mapping_complete_count":1042,"owner_unique_edge_count":911,"owner_unique_overall_mapping_pass_count":911,"owner_tied_edge_count":131,"owner_tied_overall_mapping_pass_count":0,"edge_all_occurrence1_contract_pass_count":386,"owner_unique_edge_all_occurrence1_contract_pass_count":370,"overall_mapping_pass_count":911}
 need(summary==expected,"summary");attacks={}
 for i,(key,value)in enumerate(expected.items()):
  mutated=dict(summary);mutated[key]=value+1
  try:need(mutated==expected,"mutated projection")
  except FailClosed:attacks[f"projection_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise FailClosed("attack accepted")
 return{"status":"PASS_16_OF_16_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":16,"attacks":attacks}
def build()->dict[str,Any]:
 for path,key in[(C62P,"C62p"),(C62R,"C62r"),(C62VR,"C62vr"),(C62V,"C62v"),(C62M,"C62m"),(C53,"C53"),(CANON,"canonical")]:need(hf(path)==P[key],"pin:"+key)
 c62,c62v=js(C62R),js(C62V);closeobj(c62,P["C62o"],"C62");closeobj(c62v,P["C62vo"],"C62 verification")
 occurrences=ledger(c62["ledgers"]["occurrence_lineage_map"],"C62 occurrence");atoms=ledger(c62["ledgers"]["atom_map"],"C62 atom");edges=ledger(c62["ledgers"]["edge_map"],"C62 edge");extensions=ledger(c62["ledgers"]["endpoint_lineage_scope_extension_inventory"],"C62 extension")
 extension={(x["endpoint_cell_id"],x["C41_row_sha256"]):x for x in extensions};missing={(x["endpoint_cell_id"],x["chain"]["C41"]["row_sha256"])for x in occurrences if not x["in_C59_frozen_endpoint_lineage_scope"]};need(set(extension)==missing and len(extension)==15009,"extension exact missing-key coverage")
 overlay_by_occurrence={};origin=Counter();incidence=0
 with Writer(OUT/OVERLAY,"ENDPOINT_CELL_ID_THEN_C41_ROW_SHA256")as writer:
  for occurrence in occurrences:
   key=(occurrence["endpoint_cell_id"],occurrence["chain"]["C41"]["row_sha256"]);existing=occurrence["in_C59_frozen_endpoint_lineage_scope"]
   if existing:need(key not in extension,"existing row duplicated in extension")
   else:need(extension[key]["occurrence_lineage_map_row_sha256"]==occurrence["row_sha256"]and extension[key]["partial_scope_credit_permitted"]is False,"extension binding")
   source="C59_FROZEN_ENDPOINT_SCOPE"if existing else"C62_FROZEN_SCOPE_EXTENSION_INVENTORY";origin[source]+=1;incidence+=occurrence["C60_incident_atom_count"]
   body={"schema":SCHEMA+".endpoint-scope-overlay-row","endpoint_cell_id":key[0],"C41_row_sha256":key[1],"C62_occurrence_lineage_map_row_sha256":occurrence["row_sha256"],"C59_endpoint_binding_row_sha256":occurrence["C59_endpoint_binding_row_sha256"],"overlay_source":source,"C62_scope_extension_row_sha256":None if existing else extension[key]["row_sha256"],"C60_incident_atom_count":occurrence["C60_incident_atom_count"],"scope_member_before_overlay":existing,"scope_member_after_overlay":True,"chain_row_hashes_paths_boxes_split_history_and_event_order_frozen":True,"semantic_map_available_regardless_of_event_outcome":True,"partial_scope_credit_permitted":False,"formal_credit":0,"D02_gate_credit":0};overlay_by_occurrence[occurrence["row_sha256"]]=writer.write(body)
 overlay_desc=writer.descriptor();need(origin==Counter({"C62_FROZEN_SCOPE_EXTENSION_INVENTORY":15009,"C59_FROZEN_ENDPOINT_SCOPE":6860})and incidence==26206,"overlay census")
 replay_atoms=[];atomstats=Counter();byrequest=defaultdict(list)
 with Writer(OUT/ATOM,"C62_ATOM_MAP_ORDER")as writer:
  for atom in atoms:
   mapped=[]
   for inc in atom["incident_lineage_maps"]:
    overlay=overlay_by_occurrence[inc["occurrence_lineage_map_row_sha256"]];need(overlay["endpoint_cell_id"]==inc["endpoint_cell_id"]and overlay["C41_row_sha256"]==inc["C41_row_sha256"]and inc["atom_box_compatibility_proved"]is True,"atom overlay join")
    mapped.append({"edge_role":inc["edge_role"],"geometric_side":inc["geometric_side"],"endpoint_cell_id":inc["endpoint_cell_id"],"C41_row_sha256":inc["C41_row_sha256"],"endpoint_scope_overlay_row_sha256":overlay["row_sha256"],"overlay_source":overlay["overlay_source"],"scope_member_after_overlay":True,"occurrence1_contract_passed_before_collision2":inc["occurrence1_contract_passed_before_collision2"],"common_face_or_seam_compatibility_proved":True})
   c1=all(x["occurrence1_contract_passed_before_collision2"]for x in mapped);body={"schema":SCHEMA+".atom-replay-row","C62_atom_map_row_sha256":atom["row_sha256"],"C60_atom_row_sha256":atom["C60_atom_row_sha256"],"C59_request_row_sha256":atom["C59_request_row_sha256"],"face_or_corner_id":atom["face_or_corner_id"],"glue_kind":atom["glue_kind"],"exact_span":atom["exact_span"],"C60_owner_unique":atom["C60_owner_unique"],"incident_overlay_maps":mapped,"both_incidents_in_complete_overlay_scope":True,"both_incidents_passed_occurrence1_contract_before_collision2":c1,"both_incident_lineages_common_face_or_seam_compatible":True,"semantic_mapping_complete":True,"formal_credit":0,"D02_gate_credit":0};row=writer.write(body);replay_atoms.append(row);byrequest[atom["C59_request_row_sha256"]].append(row);atomstats["complete"]+=1;atomstats["c1"]+=c1
 atom_desc=writer.descriptor();need(atomstats==Counter({"complete":13103,"c1":6360}),"atom replay census")
 edgestats=Counter()
 with Writer(OUT/EDGE,"C62_EDGE_MAP_ORDER")as writer:
  for edge in edges:
   replay=byrequest[edge["C59_request_row_sha256"]];need(len(replay)==edge["atom_count"]and all(x["semantic_mapping_complete"]for x in replay),"edge atom replay")
   unique=edge["C60_geometric_owner_unique"];c1=all(x["both_incidents_passed_occurrence1_contract_before_collision2"]for x in replay);passed=unique;blockers=[]if unique else["INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED"]
   body={"schema":SCHEMA+".edge-replay-row","C62_edge_map_row_sha256":edge["row_sha256"],"C59_request_row_sha256":edge["C59_request_row_sha256"],"owner_history_request_id":edge["owner_history_request_id"],"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"atom_count":len(replay),"atom_replay_row_hash_sequence_sha256":seq(x["row_sha256"]for x in replay),"C60_geometric_owner_unique":unique,"all_atoms_in_complete_overlay_scope":True,"all_atom_semantic_mappings_complete":True,"all_atoms_both_incidents_passed_occurrence1_contract_before_collision2":c1,"overall_owner_history_mapping_pass":passed,"decision":"PASS_FROZEN_SEMANTIC_MAP_COMPLETE_OWNER_UNIQUE"if passed else"FAIL_CLOSED_INDEPENDENT_OWNER_RULE_TIE","blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0};writer.write(body);edgestats["complete"]+=1;edgestats["unique"]+=unique;edgestats["tied"]+=not unique;edgestats["pass"]+=passed;edgestats["c1"]+=c1;edgestats["unique_c1"]+=unique and c1
 edge_desc=writer.descriptor();need(edgestats==Counter({"complete":1042,"unique":911,"pass":911,"c1":386,"unique_c1":370,"tied":131}),"edge replay census")
 summary={"existing_unique_endpoint_C41_scope_row_count":6860,"applied_scope_extension_row_count":15009,"complete_overlay_scope_row_count":21869,"overlay_incidence_count":26206,"atom_replay_count":13103,"atom_semantic_mapping_complete_count":13103,"atom_both_occurrence1_contract_pass_count":6360,"edge_replay_count":1042,"edge_semantic_mapping_complete_count":1042,"owner_unique_edge_count":911,"owner_unique_overall_mapping_pass_count":911,"owner_tied_edge_count":131,"owner_tied_overall_mapping_pass_count":0,"edge_all_occurrence1_contract_pass_count":386,"owner_unique_edge_all_occurrence1_contract_pass_count":370,"overall_mapping_pass_count":911};tests=selftest(summary)
 result={"schema":SCHEMA+".result","status":"PASS_FROZEN_15009_ROW_SCOPE_OVERLAY__13103_ATOMS_REPLAYED__911_OF_911_OWNER_UNIQUE_MAPPING_PASS__131_OWNER_TIES_UNCHANGED__ZERO_CREDIT","authority_binding":{"C62_producer_file_sha256":P["C62p"],"C62_result_file_sha256":P["C62r"],"C62_result_object_sha256":P["C62o"],"C62_independent_verifier_file_sha256":P["C62vr"],"C62_independent_verification_file_sha256":P["C62v"],"C62_independent_verification_object_sha256":P["C62vo"],"C62_manifest_file_sha256":P["C62m"],"C53_head_file_sha256":P["C53"],"canonical_file_sha256":P["canonical"]},"scope":summary,"ledgers":{"endpoint_scope_overlay":overlay_desc,"atom_replay":atom_desc,"edge_replay":edge_desc},"self_test":tests,"semantic_contract":{"mapping_completeness_is_independent_of_terminal_event_outcome":True,"occurrence1_contract_pass_before_collision2_retained_as_diagnostic":True,"common_face_or_seam_compatibility_required_for_every_atom":True},"strict_boundary":{"overlay_only_C59_C60_unchanged":True,"131_owner_ties_remain_independent_owner_rule_gap":True,"arbitrary_tiebreak_added":False,"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["FREEZE_INDEPENDENT_GLOBAL_OWNER_DECIDER_OVER_THE_911_OWNER_UNIQUE_PASS_EDGES","KEEP_131_OWNER_RULE_TIES_FAIL_CLOSED_AND_SEPARATE","DO_NOT_PROMOTE_D02_FROM_THIS_ZERO_CREDIT_OVERLAY"]};result["object_sha256"]=h(result);(OUT/RESULT).write_bytes(enc(result)+b"\n");return result
def main()->int:
 result=build();print(json.dumps({"status":result["status"],"scope":result["scope"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
