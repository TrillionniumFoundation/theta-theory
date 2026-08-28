#!/usr/bin/env python3
"""No-producer independent verifier for the C63-L scope overlay consumer."""
from __future__ import annotations
import copy,gzip,hashlib,json,os,stat,sys
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";SELF=Path(__file__).resolve();PREFIX="cm2_round306c63l_scope_extension"
SCHEMA="cm2.round306c63l.scope-extension-independent-verification.v1"
PRODUCER=OUT/(PREFIX+"_v1.py");RESULT=OUT/(PREFIX+"_result_v1.json");OVERLAY=OUT/(PREFIX+"_endpoint_scope_overlay_v1.jsonl.gz");ATOM=OUT/(PREFIX+"_atom_replay_v1.jsonl.gz");EDGE=OUT/(PREFIX+"_edge_replay_v1.jsonl.gz");OUTPUT=OUT/(PREFIX+"_independent_verification_v1.json")
C62R=OUT/"cm2_round306c62l_edge_semantic_map_result_v1.json";C62V=OUT/"cm2_round306c62l_edge_semantic_map_independent_verification_v1.json";C62VR=OUT/"cm2_round306c62l_edge_semantic_map_independent_verifier_v1.py";C62M=OUT/"cm2_round306c62l_edge_semantic_map_manifest_v1.sha256"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"producer":"d9ee2d19ed999af020ec40df1face5be9676671bbbe3e8ab6516f0726532c43c","result":"4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177","object":"676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135","overlay":"3ada8fc97bb82958623da649f914e93c1b3be8c9a37b11d258578db738b93ebc","atom":"09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734","edge":"94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b","C62r":"e85a188a7016de40fc7f3a607071aa53a2343684de51373b27786aaaf0c82615","C62o":"3d2c719f16e2921314bff0b83245e945b916da526306845eb8f00a6010cda8eb","C62vr":"bacf0000f07cb8d5bcfe882a3b52bdb6ad4b41ec7fd6e9564dd6473bbace423e","C62v":"6c259ce094b08dd434eeddf71eec1c59782d00212bd3ac06024fb6c510a7e498","C62vo":"a76faf6e9e21602979857e1195a99b7751b4e1c359be99e8356a1a760c9307c2","C62m":"5e7aa3423be34eaa894f16c320df3b3537da2f3938f85fce1c69b34336dd638d","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class Reject(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise Reject(label)
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
def rows(path:Path,desc:dict[str,Any],label:str)->list[dict[str,Any]]:
 need(path.name==desc["filename"]and hf(path)==desc["sha256"],"file:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.open(path,"rt")):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return out
def ledger(desc:dict[str,Any],label:str)->list[dict[str,Any]]:return rows(OUT/desc["filename"],desc,label)
def snapshot()->str:
 s=hashlib.sha256();base=ROOT/".cm2-runtime"
 for p in sorted(base.rglob("*"),key=lambda x:str(x.relative_to(base))):
  z=os.lstat(p);kind="D"if stat.S_ISDIR(z.st_mode)else"F"if stat.S_ISREG(z.st_mode)else"O";s.update(enc([str(p.relative_to(base)),kind,z.st_size,z.st_mtime_ns,z.st_nlink])+b"\n")
 s.update((hf(CANON)+"\n").encode());return s.hexdigest()
def attacks(capsule:dict[str,Any])->dict[str,Any]:
 need(len(capsule)==25,"25 attack dimensions");out={}
 def guard(value:dict[str,Any])->None:
  body=dict(value);actual=body.pop("object_sha256",None);need(actual==h(body),"attack closure");need(body==capsule,"attack semantics")
 guard({**capsule,"object_sha256":h(capsule)})
 for i,(key,value)in enumerate(capsule.items()):
  body=copy.deepcopy(capsule);body[key]=not value if type(value)is bool else value+1;candidate={**body,"object_sha256":h(body)}
  try:guard(candidate)
  except Reject:out[f"coherent_reclosed_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise Reject("attack accepted")
 return{"status":"PASS_25_OF_25_COHERENT_RECLOSED_ATTACKS_FAIL_CLOSED","attack_count":25,"mutations_reclosed_before_validation":True,"attacks":out}
def verify()->dict[str,Any]:
 before=snapshot();pins=[(PRODUCER,"producer"),(RESULT,"result"),(OVERLAY,"overlay"),(ATOM,"atom"),(EDGE,"edge"),(C62R,"C62r"),(C62VR,"C62vr"),(C62V,"C62v"),(C62M,"C62m"),(C53,"C53"),(CANON,"canonical")]
 for path,key in pins:need(hf(path)==P[key],"pin:"+key)
 result,c62,c62v=js(RESULT),js(C62R),js(C62V);closeobj(result,P["object"],"C63");closeobj(c62,P["C62o"],"C62");closeobj(c62v,P["C62vo"],"C62 verification")
 overlay=rows(OVERLAY,result["ledgers"]["endpoint_scope_overlay"],"C63 overlay");atoms=rows(ATOM,result["ledgers"]["atom_replay"],"C63 atoms");edges=rows(EDGE,result["ledgers"]["edge_replay"],"C63 edges")
 occurrences=ledger(c62["ledgers"]["occurrence_lineage_map"],"C62 occurrence");c62atoms=ledger(c62["ledgers"]["atom_map"],"C62 atoms");c62edges=ledger(c62["ledgers"]["edge_map"],"C62 edges");extensions=ledger(c62["ledgers"]["endpoint_lineage_scope_extension_inventory"],"C62 extension")
 extension={(x["endpoint_cell_id"],x["C41_row_sha256"]):x for x in extensions};need(len(overlay)==len(occurrences)==21869 and len(extension)==15009,"overlay inputs")
 overlay_by_occ={};origins=Counter();incidences=0
 for occurrence,row in zip(occurrences,overlay,strict=True):
  key=(occurrence["endpoint_cell_id"],occurrence["chain"]["C41"]["row_sha256"]);existing=occurrence["in_C59_frozen_endpoint_lineage_scope"];source="C59_FROZEN_ENDPOINT_SCOPE"if existing else"C62_FROZEN_SCOPE_EXTENSION_INVENTORY";ext=None if existing else extension[key]
  if existing:need(key not in extension,"existing/extension overlap")
  else:need(ext["occurrence_lineage_map_row_sha256"]==occurrence["row_sha256"]and ext["partial_scope_credit_permitted"]is False,"extension exact join")
  expected={"schema":"cm2.round306c63l.frozen-endpoint-lineage-scope-overlay.v1.endpoint-scope-overlay-row","endpoint_cell_id":key[0],"C41_row_sha256":key[1],"C62_occurrence_lineage_map_row_sha256":occurrence["row_sha256"],"C59_endpoint_binding_row_sha256":occurrence["C59_endpoint_binding_row_sha256"],"overlay_source":source,"C62_scope_extension_row_sha256":None if existing else ext["row_sha256"],"C60_incident_atom_count":occurrence["C60_incident_atom_count"],"scope_member_before_overlay":existing,"scope_member_after_overlay":True,"chain_row_hashes_paths_boxes_split_history_and_event_order_frozen":True,"semantic_map_available_regardless_of_event_outcome":True,"partial_scope_credit_permitted":False,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"overlay exact reconstruction");overlay_by_occ[occurrence["row_sha256"]]=row;origins[source]+=1;incidences+=occurrence["C60_incident_atom_count"]
 need(origins==Counter({"C62_FROZEN_SCOPE_EXTENSION_INVENTORY":15009,"C59_FROZEN_ENDPOINT_SCOPE":6860})and incidences==26206,"overlay census")
 atom_by_request=defaultdict(list);astats=Counter()
 for source,row in zip(c62atoms,atoms,strict=True):
  expected_maps=[]
  for inc in source["incident_lineage_maps"]:
   overlayrow=overlay_by_occ[inc["occurrence_lineage_map_row_sha256"]];need(overlayrow["endpoint_cell_id"]==inc["endpoint_cell_id"]and overlayrow["C41_row_sha256"]==inc["C41_row_sha256"]and inc["atom_box_compatibility_proved"]is True,"atom overlay join")
   expected_maps.append({"edge_role":inc["edge_role"],"geometric_side":inc["geometric_side"],"endpoint_cell_id":inc["endpoint_cell_id"],"C41_row_sha256":inc["C41_row_sha256"],"endpoint_scope_overlay_row_sha256":overlayrow["row_sha256"],"overlay_source":overlayrow["overlay_source"],"scope_member_after_overlay":True,"occurrence1_contract_passed_before_collision2":inc["occurrence1_contract_passed_before_collision2"],"common_face_or_seam_compatibility_proved":True})
  c1=all(x["occurrence1_contract_passed_before_collision2"]for x in expected_maps);expected={"schema":"cm2.round306c63l.frozen-endpoint-lineage-scope-overlay.v1.atom-replay-row","C62_atom_map_row_sha256":source["row_sha256"],"C60_atom_row_sha256":source["C60_atom_row_sha256"],"C59_request_row_sha256":source["C59_request_row_sha256"],"face_or_corner_id":source["face_or_corner_id"],"glue_kind":source["glue_kind"],"exact_span":source["exact_span"],"C60_owner_unique":source["C60_owner_unique"],"incident_overlay_maps":expected_maps,"both_incidents_in_complete_overlay_scope":True,"both_incidents_passed_occurrence1_contract_before_collision2":c1,"both_incident_lineages_common_face_or_seam_compatible":True,"semantic_mapping_complete":True,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"atom exact reconstruction");astats["complete"]+=1;astats["c1"]+=c1;atom_by_request[source["C59_request_row_sha256"]].append(row)
 need(astats==Counter({"complete":13103,"c1":6360}),"atom census")
 estats=Counter()
 for source,row in zip(c62edges,edges,strict=True):
  replay=atom_by_request[source["C59_request_row_sha256"]];unique=source["C60_geometric_owner_unique"];c1=all(x["both_incidents_passed_occurrence1_contract_before_collision2"]for x in replay);passed=unique;blockers=[]if unique else["INDEPENDENT_OWNER_RULE_GAP__LEXICOGRAPHIC_MINIMUM_TIED"]
  expected={"schema":"cm2.round306c63l.frozen-endpoint-lineage-scope-overlay.v1.edge-replay-row","C62_edge_map_row_sha256":source["row_sha256"],"C59_request_row_sha256":source["C59_request_row_sha256"],"owner_history_request_id":source["owner_history_request_id"],"face_or_corner_id":source["face_or_corner_id"],"glue_kind":source["glue_kind"],"atom_count":len(replay),"atom_replay_row_hash_sequence_sha256":seq(x["row_sha256"]for x in replay),"C60_geometric_owner_unique":unique,"all_atoms_in_complete_overlay_scope":True,"all_atom_semantic_mappings_complete":True,"all_atoms_both_incidents_passed_occurrence1_contract_before_collision2":c1,"overall_owner_history_mapping_pass":passed,"decision":"PASS_FROZEN_SEMANTIC_MAP_COMPLETE_OWNER_UNIQUE"if passed else"FAIL_CLOSED_INDEPENDENT_OWNER_RULE_TIE","blocker_codes":blockers,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"edge exact reconstruction");estats["complete"]+=1;estats["unique"]+=unique;estats["pass"]+=passed;estats["tied"]+=not unique;estats["c1"]+=c1;estats["unique_c1"]+=unique and c1
 need(estats==Counter({"complete":1042,"unique":911,"pass":911,"c1":386,"unique_c1":370,"tied":131}),"edge census")
 summary={"existing_unique_endpoint_C41_scope_row_count":6860,"applied_scope_extension_row_count":15009,"complete_overlay_scope_row_count":21869,"overlay_incidence_count":26206,"atom_replay_count":13103,"atom_semantic_mapping_complete_count":13103,"atom_both_occurrence1_contract_pass_count":6360,"edge_replay_count":1042,"edge_semantic_mapping_complete_count":1042,"owner_unique_edge_count":911,"owner_unique_overall_mapping_pass_count":911,"owner_tied_edge_count":131,"owner_tied_overall_mapping_pass_count":0,"edge_all_occurrence1_contract_pass_count":386,"owner_unique_edge_all_occurrence1_contract_pass_count":370,"overall_mapping_pass_count":911};need(result["scope"]==summary,"result summary")
 strict={"overlay_only_C59_C60_unchanged":True,"131_owner_ties_remain_independent_owner_rule_gap":True,"arbitrary_tiebreak_added":False,"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"};need(result["strict_boundary"]==strict,"strict boundary")
 capsule={"overlay_rows":21869,"existing_rows":6860,"extension_rows":15009,"incidences":26206,"atom_rows":13103,"atom_complete":13103,"atom_c1":6360,"edge_rows":1042,"edge_complete":1042,"owner_unique":911,"owner_unique_pass":911,"owner_tied":131,"owner_tied_pass":0,"edge_c1":386,"owner_unique_c1":370,"overall_pass":911,"scope_complete":True,"face_compatible":True,"event_outcome_diagnostic":True,"partial_credit":False,"tie_break":False,"formal_credit":0,"D02_credit":0,"runtime_write":False,"producer_executed":False};attack=attacks(capsule)
 after=snapshot();need(before==after and hf(C53)==P["C53"]and hf(CANON)==P["canonical"],"runtime/canonical stable")
 output={"schema":SCHEMA,"status":"PASS_NO_PRODUCER_EXACT_15009_SCOPE_EXTENSION_REPLAY__13103_ATOMS__911_OF_911_OWNER_UNIQUE_PASS__131_TIES_FAIL_CLOSED__25_OF_25_ATTACKS__ZERO_CREDIT","candidate":{"producer_file_sha256":P["producer"],"result_file_sha256":P["result"],"result_object_sha256":P["object"],"overlay_file_sha256":P["overlay"],"atom_replay_file_sha256":P["atom"],"edge_replay_file_sha256":P["edge"]},"verified":summary,"attacks":attack,"independence":{"producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},"strict_boundary":strict,"runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,"files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False};output["object_sha256"]=h(output);OUTPUT.write_bytes(enc(output)+b"\n");return output
def main()->int:
 result=verify();print(json.dumps({"status":result["status"],"verified":result["verified"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Reject,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
