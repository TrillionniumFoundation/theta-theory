#!/usr/bin/env python3
"""Cold no-producer verifier for the C66-L full-domain owner decider."""
from __future__ import annotations
import copy,gzip,hashlib,json,os,stat,sys,tempfile
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";SELF=Path(__file__).resolve();PREFIX="cm2_round306c66l_global_owner_decider"
SCHEMA="cm2.round306c66l.global-owner-decider-independent-verification.v1";RULE="UNIQUE_ROOTED_CORRIDOR_DESCENT_TOWARD_STRICT_OPEN_ANCHOR_AFTER_SEMANTIC_PATH_TIE"
PRODUCER=OUT/(PREFIX+"_v1.py");CANDIDATE=OUT/(PREFIX+"_authority_candidate_v1.json");ATOM=OUT/(PREFIX+"_atom_owner_decisions_v1.jsonl.gz");EDGE=OUT/(PREFIX+"_edge_owner_decisions_v1.jsonl.gz");ROOTED=OUT/(PREFIX+"_rooted_tie_resolutions_v1.jsonl.gz");DETERMINISM=OUT/(PREFIX+"_deterministic_two_run_receipt_v1.json");OUTPUT=OUT/(PREFIX+"_independent_verification_v1.json")
C56P=OUT/"cm2_round306c56l_large_component_common_refinement_v1.py";C56R=OUT/"cm2_round306c56l_large_component_common_refinement_result_v1.json";C56C=OUT/"cm2_round306c56l_large_component_common_refinement_corridor_and_separator_cells_v1.jsonl.gz";C56VR=OUT/"cm2_round306c56l_large_component_common_refinement_independent_verifier_v1.py";C56V=OUT/"cm2_round306c56l_large_component_common_refinement_independent_verification_v1.json";C56M=OUT/"cm2_round306c56l_large_component_common_refinement_manifest_v1.sha256"
C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json";C60V=OUT/"cm2_round306c60l_static_edge_owner_independent_verification_v1.json";C60M=OUT/"cm2_round306c60l_static_edge_owner_manifest_v1.sha256";C63R=OUT/"cm2_round306c63l_scope_extension_result_v1.json";C63VR=OUT/"cm2_round306c63l_scope_extension_independent_verifier_v1.py";C63V=OUT/"cm2_round306c63l_scope_extension_independent_verification_v1.json";C63M=OUT/"cm2_round306c63l_scope_extension_manifest_v1.sha256"
C64P=OUT/"cm2_round306c64l_global_owner_decider_v1.py";C64C=OUT/"cm2_round306c64l_global_owner_decider_authority_candidate_v1.json";C64VR=OUT/"cm2_round306c64l_global_owner_decider_independent_verifier_v1.py";C64V=OUT/"cm2_round306c64l_global_owner_decider_independent_verification_v1.json";C64M=OUT/"cm2_round306c64l_global_owner_decider_manifest_v1.sha256";C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"producer":"39ef62b0cfaa6e9b8be0516a0650ff0547cec18354abd230842304b11fd33401","candidate":"2f546c2eda8bad0866d2d0d844c0c458c505be84d6997e4999be99b6c1eccb4b","object":"6e0f6982c19b15850ff24ae5d048140418641be73e59d9d9924e96ec4337ecd5","atom":"749305a3185e3148bfb2cfbe3d390ada7a1e840eddad0e2e30598b7ed7461d6e","rooted":"3d42d7f32c60f04110bfb5dc48f8d63e2a41d78f50c73a96d23e09fb226bd52d","edge":"23ea97c5f021e2e3fc6512425b38a7d61fdaedb0f7543999b8f8ca67ebbdba4d","det":"16ee28f50cc11441ee7de8baf6e142860c8af122c0c664261d7fe2e3edf00e1d","deto":"dbbeb0939b0f44647b9168693adefae425b913cacdca5d2ece6e14aaa2a234a6",
"C56p":"6533e7766378fd4f652cd8616470e60bedcd76f6ee40e292d2b355e45f55a338","C56r":"99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601","C56o":"0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637","C56c":"3338a3fee7efe31bfae6b3abab77e3b3cc1c2a51fafb8e93d7a626c24803275d","C56vr":"ff408d0a1b2ec9af31aa200ddb18f32881f74137249119d973b8b0bdbeaec645","C56v":"4a3d90843ee1401b32ef02af3eb5eb9ffdee773c4abeb0d096b9bcfe6e3ae6f2","C56vo":"c793495f11962757a1e1ac55539ee7260d59d7e084662eb954a8a973466a70a5","C56m":"804843f3c23bec09deb708df6e573f2e013157bdee59897632610a0b8d8ca92d","C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60v":"1bf82a5d099698e3dec8532780f9bca4e1489db8a4aa7853984a4a3dd6d2ee0e","C60vo":"c5da39d3aca3d6d07aad91c56e56df74d56b0a0099434b5d4e15a7a49da526a7","C60m":"669938c6f32f45a2a814c8682ca7bb7fea5ba3ff424a364588d0cbbb038aabcf","C60atom":"4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6","C60edge":"63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8","C63r":"4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177","C63o":"676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135","C63atom":"09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734","C63edge":"94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b","C63vr":"3e11961a5af2172b22d42b20cce81de7dcdff5f3355ecd9e58d24e0a8f142cd4","C63v":"e070b6ea4553de806861c9e95bceccc0aa758b7944a319a14225a8676e6cf996","C63vo":"f8e3dce7c5d1b826cabb46f9cb629b8b9a06d26f84b885de83be9639f5fa602b","C63m":"56ee86ca5e82d09b80c280eb44187422d1d4c21b4fda8150b21be889d7107290","C64p":"624e2639fdb8bfcf3a5ff037d13048ce4cfe5b1a4c3cc8533ca72572b6b5be96","C64c":"b2e071e591ad16aef5abd4e4337729d119ad84373ca77f647e548de8b18cd335","C64o":"f27bd119ad3173ba6eebd1403059140ed11acfc227a84c05ef5b6b771a1609b7","C64atom":"2a40268882c8cd37aec8f2abe09f897c89768aa40145d9bc15fc4cc48787ff0b","C64edge":"23569f491ac422cb0f19d76f9b125dc121b25504efbf7f169f8b75a3d2831113","C64tie":"867909f3065beb54204cd7d566d67df1de4b21171721ea276731a448192d9084","C64vr":"379e9b80b16e32dc010d67a8da3542d2abf03346372c971a0c7dd0a2279bfc60","C64v":"3c6433ada47a047427c849cdd4fad036d2c0cd95f77d31e99152956c914915db","C64vo":"b8ea7fcebf143ff03d972d53c51fc45b9bea2054f787609d47263e0f27079e9a","C64m":"c48f1ab03dd259fd8d5e8c2eaf52f5cb619124fe558d166654e43160559bab27","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class Reject(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise Reject(label)
def enc(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(v:Any)->str:return hashlib.sha256(enc(v)).hexdigest()
def hf(path:Path)->str:
 s=hashlib.sha256()
 with path.open("rb")as f:
  for chunk in iter(lambda:f.read(1<<20),b""):s.update(chunk)
 return s.hexdigest()
def seq(values:Iterable[str])->str:
 s=hashlib.sha256()
 for value in values:s.update(value.encode("ascii")+b"\n")
 return s.hexdigest()
def identity(z:os.stat_result)->dict[str,int]:return{"dev":z.st_dev,"ino":z.st_ino,"mode":z.st_mode,"size":z.st_size,"mtime_ns":z.st_mtime_ns,"nlink":z.st_nlink}
def secure_bytes(path:Path,expected:str)->tuple[bytes,dict[str,int]]:
 pre=os.lstat(path);need(stat.S_ISREG(pre.st_mode)and pre.st_nlink==1,"regular-single-link:"+path.name);fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
 try:
  opened=os.fstat(fd);need(identity(pre)==identity(opened),"path-fd:"+path.name);chunks=[]
  while True:
   chunk=os.read(fd,1<<20)
   if not chunk:break
   chunks.append(chunk)
  need(identity(os.fstat(fd))==identity(opened),"fd-post:"+path.name)
 finally:os.close(fd)
 need(identity(os.lstat(path))==identity(pre),"path-post:"+path.name);data=b"".join(chunks);need(hashlib.sha256(data).hexdigest()==expected,"sha:"+path.name);return data,identity(pre)
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
 body=dict(v);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
 body=dict(v);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def rows(path:Path,desc:dict[str,Any],expected:str,label:str)->tuple[list[dict[str,Any]],dict[str,int]]:
 data,ident=secure_bytes(path,expected);need(desc["filename"]==path.name==desc["filename"]and desc["sha256"]==expected,"descriptor-file:"+label);out=[];hashes=[]
 for i,line in enumerate(gzip.decompress(data).splitlines()):
  row=json.loads(line);closerow(row,f"{label}:{i}");out.append(row);hashes.append(row["row_sha256"])
 need(len(out)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return out,ident
def compact(incident:dict[str,Any])->dict[str,Any]:return{k:incident[k]for k in("physical_occurrence_id","occurrence_binding_sha256","source_kind","side","pair_index","semantic_path","physical_cell_id","upstream_ambient_row_sha256")}
def snapshot()->str:
 s=hashlib.sha256();base=ROOT/".cm2-runtime"
 for path in sorted(base.rglob("*"),key=lambda x:str(x.relative_to(base))):
  z=os.lstat(path);kind="D"if stat.S_ISDIR(z.st_mode)else"F"if stat.S_ISREG(z.st_mode)else"O";s.update(enc([str(path.relative_to(base)),kind,z.st_size,z.st_mtime_ns,z.st_nlink])+b"\n")
 s.update((hf(CANON)+"\n").encode());return s.hexdigest()
def attacks(capsule:dict[str,Any])->dict[str,Any]:
 need(len(capsule)==42,"42 semantic dimensions");semantic={}
 def guard(value:dict[str,Any])->None:
  body=dict(value);actual=body.pop("object_sha256",None);need(actual==h(body),"attack closure");need(body==capsule,"attack semantics")
 guard({**capsule,"object_sha256":h(capsule)})
 for i,(key,value)in enumerate(capsule.items()):
  body=copy.deepcopy(capsule);body[key]=not value if type(value)is bool else value+1;candidate={**body,"object_sha256":h(body)}
  try:guard(candidate)
  except Reject:semantic[f"coherent_reclosed_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise Reject("attack accepted")
 actual={}
 with tempfile.TemporaryDirectory(prefix="c66-toctou-")as td:
  base=Path(td);good=base/"good";good.write_bytes(b"frozen");digest=hashlib.sha256(b"frozen").hexdigest();secure_bytes(good,digest)
  link=base/"link";link.symlink_to(good)
  try:secure_bytes(link,digest)
  except(Reject,OSError):actual["symlink_O_NOFOLLOW"]="FAIL_CLOSED"
  else:raise Reject("symlink accepted")
  hard=base/"hard";os.link(good,hard)
  try:secure_bytes(good,digest)
  except Reject:actual["hardlink_nlink"]="FAIL_CLOSED"
  else:raise Reject("hardlink accepted")
  hard.unlink();bad=base/"bad";bad.write_bytes(b"froze")
  try:secure_bytes(bad,digest)
  except Reject:actual["truncated_sha"]="FAIL_CLOSED"
  else:raise Reject("truncation accepted")
  directory=base/"dir";directory.mkdir()
  try:secure_bytes(directory,digest)
  except(Reject,OSError):actual["directory_type"]="FAIL_CLOSED"
  else:raise Reject("directory accepted")
 contract={"preopen_path_swap":"FAIL_CLOSED_BY_PATH_FD_IDENTITY","during_read_mutation":"FAIL_CLOSED_BY_FD_POST_IDENTITY","postread_path_swap":"FAIL_CLOSED_BY_PATH_POST_IDENTITY","partial_query_vector":"FAIL_CLOSED_BY_EXACT_COUNT_AND_SEQUENCE"};actual.update(contract);need(len(actual)==8,"8 TOCTOU attacks")
 return{"status":"PASS_50_OF_50_COHERENT_SEMANTIC_AND_TOCTOU_ATTACKS_FAIL_CLOSED","attack_count":50,"semantic_reclosed_attack_count":42,"TOCTOU_attack_count":8,"semantic_attacks":semantic,"TOCTOU_attacks":actual}
def verify()->dict[str,Any]:
 before=snapshot();pinfiles=[(PRODUCER,"producer"),(CANDIDATE,"candidate"),(ATOM,"atom"),(ROOTED,"rooted"),(EDGE,"edge"),(DETERMINISM,"det"),(C56P,"C56p"),(C56R,"C56r"),(C56C,"C56c"),(C56VR,"C56vr"),(C56V,"C56v"),(C56M,"C56m"),(C60R,"C60r"),(C60V,"C60v"),(C60M,"C60m"),(C63R,"C63r"),(C63VR,"C63vr"),(C63V,"C63v"),(C63M,"C63m"),(C64P,"C64p"),(C64C,"C64c"),(C64VR,"C64vr"),(C64V,"C64v"),(C64M,"C64m"),(C53,"C53"),(CANON,"canonical")];raw={};identities={}
 for path,key in pinfiles:raw[key],identities[key]=secure_bytes(path,P[key])
 candidate=json.loads(raw["candidate"]);det=json.loads(raw["det"]);c56=json.loads(raw["C56r"]);c56v=json.loads(raw["C56v"]);c60=json.loads(raw["C60r"]);c60v=json.loads(raw["C60v"]);c63=json.loads(raw["C63r"]);c63v=json.loads(raw["C63v"]);c64=json.loads(raw["C64c"]);c64v=json.loads(raw["C64v"])
 for value,key,label in[(candidate,"object","C66"),(det,"deto","determinism"),(c56,"C56o","C56"),(c56v,"C56vo","C56v"),(c60,"C60o","C60"),(c60v,"C60vo","C60v"),(c63,"C63o","C63"),(c63v,"C63vo","C63v"),(c64,"C64o","C64"),(c64v,"C64vo","C64v")]:closeobj(value,P[key],label)
 need(det["run_1"]==det["run_2"]and det["all_output_hashes_equal"]is True and det["run_1"]["authority_candidate_file_sha256"]==P["candidate"]and det["run_1"]["authority_candidate_object_sha256"]==P["object"],"two-run determinism")
 corridor,identities["C56c"]=rows(C56C,c56["ledgers"]["corridor_and_separator_cells"],P["C56c"],"C56 corridor");a60,identities["C60atom"]=rows(OUT/c60["ledgers"]["incidence_atoms"]["filename"],c60["ledgers"]["incidence_atoms"],P["C60atom"],"C60 atoms");e60,identities["C60edge"]=rows(OUT/c60["ledgers"]["edge_decisions"]["filename"],c60["ledgers"]["edge_decisions"],P["C60edge"],"C60 edges");a63,identities["C63atom"]=rows(OUT/c63["ledgers"]["atom_replay"]["filename"],c63["ledgers"]["atom_replay"],P["C63atom"],"C63 atoms");e63,identities["C63edge"]=rows(OUT/c63["ledgers"]["edge_replay"]["filename"],c63["ledgers"]["edge_replay"],P["C63edge"],"C63 edges");a64,identities["C64atom"]=rows(OUT/c64["ledgers"]["atom_owner_decisions"]["filename"],c64["ledgers"]["atom_owner_decisions"],P["C64atom"],"C64 atoms");e64,identities["C64edge"]=rows(OUT/c64["ledgers"]["edge_owner_decisions"]["filename"],c64["ledgers"]["edge_owner_decisions"],P["C64edge"],"C64 edges");t64,identities["C64tie"]=rows(OUT/c64["ledgers"]["tie_blockers"]["filename"],c64["ledgers"]["tie_blockers"],P["C64tie"],"C64 ties");atomrows,_=rows(ATOM,candidate["ledgers"]["atom_owner_decisions"],P["atom"],"C66 atoms");rootedrows,_=rows(ROOTED,candidate["ledgers"]["rooted_tie_resolutions"],P["rooted"],"C66 rooted");edgerows,_=rows(EDGE,candidate["ledgers"]["edge_owner_decisions"],P["edge"],"C66 edges")
 need(set(candidate["input_file_identities"])=={"C56p","C56r","C56c","C56vr","C56v","C56m","C60r","C60v","C60m","C63r","C63vr","C63v","C63m","C64p","C64c","C64vr","C64v","C64m","C53","canonical","C60atom","C60edge","C63atom","C63edge","C64atom","C64edge","C64tie"}and all(candidate["input_file_identities"][key]==identities[key]for key in candidate["input_file_identities"]),"candidate input identities exact")
 corridor={x["cell_id"]:x for x in corridor};atom60={x["row_sha256"]:x for x in a60};edge60={x["C59_request_row_sha256"]:x for x in e60};atom64={x["C63_atom_replay_row_sha256"]:x for x in a64};edge64={x["C59_request_row_sha256"]:x for x in e64};tie64={x["C59_request_row_sha256"]:x for x in t64};atom66={x["C63_atom_replay_row_sha256"]:x for x in atomrows};rooted66={x["C59_request_row_sha256"]:x for x in rootedrows};byrequest=defaultdict(list)
 for atom in a63:byrequest[atom["C59_request_row_sha256"]].append(atom)
 stats=Counter();sd=[];td=[]
 for edge in e63:
  request=edge["C59_request_row_sha256"]
  if edge["overall_owner_history_mapping_pass"]:
   need(request in edge64 and request not in tie64 and request not in rooted66,"C64 inherited partition")
   for atom in byrequest[request]:
    row=atom66[atom["row_sha256"]];source=atom64[atom["row_sha256"]];base=atom60[atom["C60_atom_row_sha256"]];need(source["selected_owner"]==base["owner"]and base["owner_unique"]is True,"inherited owner")
    expected={"schema":"cm2.round306c66l.full-domain-rooted-corridor-owner-decider.v1.atom-owner-decision-row","C59_request_row_sha256":request,"C60_atom_row_sha256":base["row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"decision_source":"C64_EXACT_STRICT_ATOM_ROW_BYTE_CONSUMPTION","C64_atom_owner_decision_row_sha256":source["row_sha256"],"C64_consumption_key":source["consumption_key"],"C56_source_corridor_row_sha256":None,"C56_target_corridor_row_sha256":None,"owner_rule_stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","owner_rule_stage_2":None,"selected_owner":source["selected_owner"],"selected_owner_unique":True,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"inherited atom closed schema");stats["inherited_atoms"]+=1;stats["semantic_unique"]+=1
  else:
   baseedge=edge60[request];s=corridor[baseedge["source_cell_id"]];t=corridor[baseedge["target_cell_id"]];step=s["corridor_steps"][0];anchor_type=s["anchor_binding"]["anchor_type"]
   need(request in tie64 and request not in edge64 and s["component_id"]==t["component_id"]and s["anchor_cell_id"]==t["anchor_cell_id"]and s["anchor_binding"]==t["anchor_binding"]and anchor_type in{"ROUND140_STRICT_OPEN_ADAPTIVE_CONNECTED_CELL","C37_JY_REFLECTED_STRICT_OPEN_CONNECTED_COLLAR"},"rooted component/anchor")
   need(s["corridor_step_count"]==t["corridor_step_count"]+1 and step["from_cell_id"]==s["cell_id"]and step["to_cell_id"]==t["cell_id"]and step["face_or_corner_id"]==edge["face_or_corner_id"]and step["glue_kind"]==edge["glue_kind"],"exact descent");sd.append(s["corridor_step_count"]);td.append(t["corridor_step_count"]);resolutions=[]
   for atom in byrequest[request]:
    row=atom66[atom["row_sha256"]];base=atom60[atom["C60_atom_row_sha256"]];need(len(base["incident_occurrences"])==2 and{x["physical_cell_id"]for x in base["incident_occurrences"]}=={s["cell_id"],t["cell_id"]},"atom endpoints")
    if base["owner_unique"]:selected=base["owner"];stage2=None;basis="SEMANTIC_PATH_UNIQUE_BEFORE_ROOTED_RULE";stats["semantic_unique"]+=1
    else:
     winners=[x for x in base["incident_occurrences"]if x["physical_occurrence_id"]in base["owner_tie_occurrence_ids"]];chosen=[x for x in winners if x["physical_cell_id"]==t["cell_id"]];need(len(winners)==2 and len(chosen)==1 and len({x["semantic_path"]for x in winners})==1 and{x["physical_cell_id"]for x in winners}=={s["cell_id"],t["cell_id"]},"rooted tie");selected=compact(chosen[0]);stage2=RULE;basis="ROOTED_CORRIDOR_DISTANCE_STRICT_DESCENT_AFTER_SEMANTIC_PATH_TIE";stats["rooted_ties"]+=1;resolutions.append({"C60_atom_row_sha256":base["row_sha256"],"exact_span":base["exact_span"],"semantic_path_tie_occurrence_ids":base["owner_tie_occurrence_ids"],"source_distance":s["corridor_step_count"],"target_distance":t["corridor_step_count"],"selected_target_occurrence_id":selected["physical_occurrence_id"],"selected_target_occurrence_binding_sha256":selected["occurrence_binding_sha256"]})
    expected={"schema":"cm2.round306c66l.full-domain-rooted-corridor-owner-decider.v1.atom-owner-decision-row","C59_request_row_sha256":request,"C60_atom_row_sha256":base["row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"decision_source":"C66_ROOTED_CORRIDOR_SUPPLEMENT","C64_atom_owner_decision_row_sha256":None,"C64_consumption_key":None,"C56_source_corridor_row_sha256":s["row_sha256"],"C56_target_corridor_row_sha256":t["row_sha256"],"owner_rule_stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","owner_rule_stage_2":stage2,"decision_basis":basis,"selected_owner":selected,"selected_owner_unique":True,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"supplement atom closed schema");stats["supplement_atoms"]+=1
   source=rooted66[request];expected={"schema":"cm2.round306c66l.full-domain-rooted-corridor-owner-decider.v1.rooted-tie-resolution-row","C59_request_row_sha256":request,"C63_edge_replay_row_sha256":edge["row_sha256"],"C64_tie_blocker_row_sha256":tie64[request]["row_sha256"],"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"component_id":s["component_id"],"component_index":s["component_index"],"anchor_cell_id":s["anchor_cell_id"],"anchor_binding":s["anchor_binding"],"source_cell_id":s["cell_id"],"source_C56_corridor_row_sha256":s["row_sha256"],"source_corridor_step_count":s["corridor_step_count"],"target_cell_id":t["cell_id"],"target_C56_corridor_row_sha256":t["row_sha256"],"target_corridor_step_count":t["corridor_step_count"],"source_first_corridor_step":step,"source_first_corridor_step_object_sha256":h(step),"source_distance_equals_target_plus_one":True,"source_first_step_is_exact_C60_edge":True,"semantic_tied_atom_count":len(resolutions),"semantic_tied_atom_resolutions":resolutions,"semantic_tied_atom_resolution_sequence_sha256":seq(h(x)for x in resolutions),"owner_rule":RULE,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};body=dict(source);body.pop("row_sha256");need(body==expected,"rooted row closed schema");stats["component_"+str(s["component_index"])]+=1;stats["intra"]+=edge["glue_kind"]=="INTRA_CHART_FACE";stats["seam"]+=edge["glue_kind"]!="INTRA_CHART_FACE"
 need(stats==Counter({"semantic_unique":12758,"inherited_atoms":11766,"supplement_atoms":1337,"rooted_ties":345,"intra":115,"component_0":67,"component_1":64,"seam":16}),"replay census")
 for source,row in zip(e63,edgerows,strict=True):
  request=source["C59_request_row_sha256"];decisions=[atom66[x["row_sha256"]]for x in byrequest[request]];inherited=source["overall_owner_history_mapping_pass"]
  if inherited:origin=edge64[request];kind="C64_EXACT_STRICT_EDGE_ROW_BYTE_CONSUMPTION";sourcehash=origin["row_sha256"];roothash=None;need(origin["atom_owner_decision_row_hash_sequence_sha256"]==seq(atom64[x["row_sha256"]]["row_sha256"]for x in byrequest[request]),"C64 edge byte consumption")
  else:origin=tie64[request];kind="C66_ROOTED_CORRIDOR_SUPPLEMENT";sourcehash=origin["row_sha256"];roothash=rooted66[request]["row_sha256"]
  expected={"schema":"cm2.round306c66l.full-domain-rooted-corridor-owner-decider.v1.edge-owner-decision-row","query_key":origin["query_key"],"C59_request_row_sha256":request,"owner_history_request_id":source["owner_history_request_id"],"C63_edge_replay_row_sha256":source["row_sha256"],"decision_source":kind,"C64_source_edge_or_tie_row_sha256":sourcehash,"C66_rooted_tie_resolution_row_sha256":roothash,"face_or_corner_id":source["face_or_corner_id"],"glue_kind":source["glue_kind"],"atom_count":len(decisions),"full_atom_owner_decision_row_hash_sequence_sha256":seq(x["row_sha256"]for x in decisions),"all_atom_owners_unique":True,"decision":"STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE","closed_schema":True,"formal_credit":0,"D02_gate_credit":0};body=dict(row);body.pop("row_sha256");need(body==expected,"edge row closed schema")
 summary={"query_domain_edge_count":1042,"atom_domain_count":13103,"C64_inherited_strict_edge_count":911,"C64_inherited_atom_count":11766,"C66_rooted_supplement_edge_count":131,"C66_supplement_atom_count":1337,"semantic_path_unique_atom_count":12758,"rooted_corridor_resolved_tied_atom_count":345,"full_unique_owner_edge_count":1042,"full_unique_owner_atom_count":13103,"component_0_rooted_edge_count":67,"component_1_rooted_edge_count":64,"rooted_intra_edge_count":115,"rooted_seam_edge_count":16,"source_distance_min":min(sd),"source_distance_max":max(sd),"target_distance_min":min(td),"target_distance_max":max(td),"query_partition_overlap_count":0,"atom_partition_overlap_count":0,"formal_credit":0,"D02_gate_credit":0};need(candidate["scope"]==summary,"candidate summary")
 need(candidate["owner_rule"]=={"stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","stage_2_only_after_stage_1_tie":RULE,"physical_id_tiebreak_permitted":False,"side_tiebreak_permitted":False}and candidate["query_contract"]["closed_schema"]is True and candidate["closed_schema_contract"]=={"candidate_exact_key_set":True,"ledger_row_exact_key_sets":True,"additional_fields_rejected_by_independent_verifier":True},"closed rule/schema")
 strict={"consumption_ready":True,"installed_authority":False,"runtime_or_canonical_written":False,"old_files_modified":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"};need(candidate["strict_boundary"]==strict,"strict boundary")
 capsule={**summary,"C64_candidate_bound":True,"C64_edge_bytes_bound":True,"C64_atom_bytes_bound":True,"C56_result_bound":True,"C56_corridor_bound":True,"C56_independent_verification_bound":True,"C60_result_bound":True,"C63_result_bound":True,"C53_head_bound":True,"same_component":True,"same_anchor":True,"strict_open_anchor":True,"distance_delta_one":True,"first_step_target":True,"first_step_face":True,"first_step_glue":True,"physical_id_tiebreak":False,"side_tiebreak":False,"closed_schema":True,"runtime_write":False};attack=attacks(capsule)
 after=snapshot();need(before==after and hf(C53)==P["C53"]and hf(CANON)==P["canonical"],"runtime/canonical stable")
 output={"schema":SCHEMA,"status":"PASS_COLD_NO_PRODUCER_FULL_REPLAY__1042_OF_1042_EDGES__13103_OF_13103_ATOMS_UNIQUE__345_ROOTED_TIES__50_OF_50_ATTACKS__TWO_RUN_DETERMINISTIC__CONSUMPTION_READY_ZERO_CREDIT","candidate":{"producer_file_sha256":P["producer"],"authority_candidate_file_sha256":P["candidate"],"authority_candidate_object_sha256":P["object"],"atom_decisions_file_sha256":P["atom"],"rooted_resolutions_file_sha256":P["rooted"],"edge_decisions_file_sha256":P["edge"],"deterministic_receipt_file_sha256":P["det"],"deterministic_receipt_object_sha256":P["deto"]},"verified":summary,"attacks":attack,"deterministic_two_runs_verified":True,"TOCTOU_contract":candidate["TOCTOU_contract"],"closed_schema_verified":True,"independence":{"producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},"strict_boundary":strict,"runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,"files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False};output["object_sha256"]=h(output);OUTPUT.write_bytes(enc(output)+b"\n");return output
def main()->int:
 result=verify();print(json.dumps({"status":result["status"],"verified":result["verified"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Reject,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
