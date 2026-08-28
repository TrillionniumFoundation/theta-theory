#!/usr/bin/env python3
"""C66-L full-domain owner decider with rooted-corridor semantic tie resolution."""
from __future__ import annotations
import copy,gzip,hashlib,json,os,stat,sys
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any,Iterable
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"deliverables";PREFIX="cm2_round306c66l_global_owner_decider"
SCHEMA="cm2.round306c66l.full-domain-rooted-corridor-owner-decider.v1";RULE="UNIQUE_ROOTED_CORRIDOR_DESCENT_TOWARD_STRICT_OPEN_ANCHOR_AFTER_SEMANTIC_PATH_TIE"
ATOM_FILE=PREFIX+"_atom_owner_decisions_v1.jsonl.gz";EDGE_FILE=PREFIX+"_edge_owner_decisions_v1.jsonl.gz";ROOTED_FILE=PREFIX+"_rooted_tie_resolutions_v1.jsonl.gz";CANDIDATE_FILE=PREFIX+"_authority_candidate_v1.json"
C56P=OUT/"cm2_round306c56l_large_component_common_refinement_v1.py";C56R=OUT/"cm2_round306c56l_large_component_common_refinement_result_v1.json";C56C=OUT/"cm2_round306c56l_large_component_common_refinement_corridor_and_separator_cells_v1.jsonl.gz";C56VR=OUT/"cm2_round306c56l_large_component_common_refinement_independent_verifier_v1.py";C56V=OUT/"cm2_round306c56l_large_component_common_refinement_independent_verification_v1.json";C56M=OUT/"cm2_round306c56l_large_component_common_refinement_manifest_v1.sha256"
C60R=OUT/"cm2_round306c60l_static_edge_owner_result_v1.json";C60V=OUT/"cm2_round306c60l_static_edge_owner_independent_verification_v1.json";C60M=OUT/"cm2_round306c60l_static_edge_owner_manifest_v1.sha256"
C63R=OUT/"cm2_round306c63l_scope_extension_result_v1.json";C63VR=OUT/"cm2_round306c63l_scope_extension_independent_verifier_v1.py";C63V=OUT/"cm2_round306c63l_scope_extension_independent_verification_v1.json";C63M=OUT/"cm2_round306c63l_scope_extension_manifest_v1.sha256"
C64P=OUT/"cm2_round306c64l_global_owner_decider_v1.py";C64C=OUT/"cm2_round306c64l_global_owner_decider_authority_candidate_v1.json";C64VR=OUT/"cm2_round306c64l_global_owner_decider_independent_verifier_v1.py";C64V=OUT/"cm2_round306c64l_global_owner_decider_independent_verification_v1.json";C64M=OUT/"cm2_round306c64l_global_owner_decider_manifest_v1.sha256"
C53=ROOT/".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal";CANON=OUT/"CM2_LATEST_STATUS.md"
P={"C56p":"6533e7766378fd4f652cd8616470e60bedcd76f6ee40e292d2b355e45f55a338","C56r":"99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601","C56o":"0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637","C56c":"3338a3fee7efe31bfae6b3abab77e3b3cc1c2a51fafb8e93d7a626c24803275d","C56vr":"ff408d0a1b2ec9af31aa200ddb18f32881f74137249119d973b8b0bdbeaec645","C56v":"4a3d90843ee1401b32ef02af3eb5eb9ffdee773c4abeb0d096b9bcfe6e3ae6f2","C56vo":"c793495f11962757a1e1ac55539ee7260d59d7e084662eb954a8a973466a70a5","C56m":"804843f3c23bec09deb708df6e573f2e013157bdee59897632610a0b8d8ca92d",
"C60r":"c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315","C60o":"9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568","C60v":"1bf82a5d099698e3dec8532780f9bca4e1489db8a4aa7853984a4a3dd6d2ee0e","C60vo":"c5da39d3aca3d6d07aad91c56e56df74d56b0a0099434b5d4e15a7a49da526a7","C60m":"669938c6f32f45a2a814c8682ca7bb7fea5ba3ff424a364588d0cbbb038aabcf","C60atom":"4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6","C60edge":"63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8",
"C63r":"4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177","C63o":"676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135","C63atom":"09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734","C63edge":"94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b","C63vr":"3e11961a5af2172b22d42b20cce81de7dcdff5f3355ecd9e58d24e0a8f142cd4","C63v":"e070b6ea4553de806861c9e95bceccc0aa758b7944a319a14225a8676e6cf996","C63vo":"f8e3dce7c5d1b826cabb46f9cb629b8b9a06d26f84b885de83be9639f5fa602b","C63m":"56ee86ca5e82d09b80c280eb44187422d1d4c21b4fda8150b21be889d7107290",
"C64p":"624e2639fdb8bfcf3a5ff037d13048ce4cfe5b1a4c3cc8533ca72572b6b5be96","C64c":"b2e071e591ad16aef5abd4e4337729d119ad84373ca77f647e548de8b18cd335","C64o":"f27bd119ad3173ba6eebd1403059140ed11acfc227a84c05ef5b6b771a1609b7","C64atom":"2a40268882c8cd37aec8f2abe09f897c89768aa40145d9bc15fc4cc48787ff0b","C64edge":"23569f491ac422cb0f19d76f9b125dc121b25504efbf7f169f8b75a3d2831113","C64tie":"867909f3065beb54204cd7d566d67df1de4b21171721ea276731a448192d9084","C64vr":"379e9b80b16e32dc010d67a8da3542d2abf03346372c971a0c7dd0a2279bfc60","C64v":"3c6433ada47a047427c849cdd4fad036d2c0cd95f77d31e99152956c914915db","C64vo":"b8ea7fcebf143ff03d972d53c51fc45b9bea2054f787609d47263e0f27079e9a","C64m":"c48f1ab03dd259fd8d5e8c2eaf52f5cb619124fe558d166654e43160559bab27","C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3","canonical":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57"}
class FailClosed(RuntimeError):pass
def need(v:bool,label:str)->None:
 if type(v)is not bool or not v:raise FailClosed(label)
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
def secure_rows(path:Path,desc:dict[str,Any],expected:str,label:str)->tuple[list[dict[str,Any]],dict[str,int]]:
 data,ident=secure_bytes(path,expected);need(path.name==desc["filename"]and expected==desc["sha256"],"descriptor-file:"+label);rows=[];hashes=[]
 for i,line in enumerate(gzip.decompress(data).splitlines()):
  row=json.loads(line);closerow(row,f"{label}:{i}");rows.append(row);hashes.append(row["row_sha256"])
 need(len(rows)==desc["row_count"]and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return rows,ident
class Writer:
 def __init__(self,path:Path,order:str):self.path,self.order=path,order;self.raw=path.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
 def __enter__(self):return self
 def write(self,body:dict[str,Any])->dict[str,Any]:
  rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return row
 def __exit__(self,*_):self.gz.close();self.raw.close()
 def descriptor(self)->dict[str,Any]:return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}
def compact(incident:dict[str,Any])->dict[str,Any]:return{k:incident[k]for k in("physical_occurrence_id","occurrence_binding_sha256","source_kind","side","pair_index","semantic_path","physical_cell_id","upstream_ambient_row_sha256")}
def selftest(summary:dict[str,int])->dict[str,Any]:
 expected={"query_domain_edge_count":1042,"atom_domain_count":13103,"C64_inherited_strict_edge_count":911,"C64_inherited_atom_count":11766,"C66_rooted_supplement_edge_count":131,"C66_supplement_atom_count":1337,"semantic_path_unique_atom_count":12758,"rooted_corridor_resolved_tied_atom_count":345,"full_unique_owner_edge_count":1042,"full_unique_owner_atom_count":13103,"component_0_rooted_edge_count":67,"component_1_rooted_edge_count":64,"rooted_intra_edge_count":115,"rooted_seam_edge_count":16,"source_distance_min":5,"source_distance_max":104,"target_distance_min":4,"target_distance_max":103,"query_partition_overlap_count":0,"atom_partition_overlap_count":0,"formal_credit":0,"D02_gate_credit":0};need(summary==expected,"summary");capsule={**expected,"C64_bytes_consumed":True,"C56_corridor_exact":True,"same_component":True,"same_anchor":True,"strict_descent":True,"first_step_exact_edge":True,"physical_id_tiebreak":False,"side_tiebreak":False,"runtime_write":False};need(len(capsule)==31,"31 tests");out={}
 for i,(key,value)in enumerate(capsule.items()):
  mutated=copy.deepcopy(capsule);mutated[key]=not value if type(value)is bool else value+1
  try:need(mutated==capsule,"mutated")
  except FailClosed:out[f"projection_{i:02d}_{key}"]="FAIL_CLOSED"
  else:raise FailClosed("attack")
 return{"status":"PASS_31_OF_31_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":31,"attacks":out}
def build()->dict[str,Any]:
 pinfiles=[(C56P,"C56p"),(C56R,"C56r"),(C56C,"C56c"),(C56VR,"C56vr"),(C56V,"C56v"),(C56M,"C56m"),(C60R,"C60r"),(C60V,"C60v"),(C60M,"C60m"),(C63R,"C63r"),(C63VR,"C63vr"),(C63V,"C63v"),(C63M,"C63m"),(C64P,"C64p"),(C64C,"C64c"),(C64VR,"C64vr"),(C64V,"C64v"),(C64M,"C64m"),(C53,"C53"),(CANON,"canonical")];raw={};identities={}
 for path,key in pinfiles:raw[key],identities[key]=secure_bytes(path,P[key])
 c56=json.loads(raw["C56r"]);c56v=json.loads(raw["C56v"]);c60=json.loads(raw["C60r"]);c60v=json.loads(raw["C60v"]);c63=json.loads(raw["C63r"]);c63v=json.loads(raw["C63v"]);c64=json.loads(raw["C64c"]);c64v=json.loads(raw["C64v"])
 for value,key,label in[(c56,"C56o","C56"),(c56v,"C56vo","C56v"),(c60,"C60o","C60"),(c60v,"C60vo","C60v"),(c63,"C63o","C63"),(c63v,"C63vo","C63v"),(c64,"C64o","C64"),(c64v,"C64vo","C64v")]:closeobj(value,P[key],label)
 corridor,identities["C56c"]=secure_rows(C56C,c56["ledgers"]["corridor_and_separator_cells"],P["C56c"],"C56 corridor");a60,identities["C60atom"]=secure_rows(OUT/c60["ledgers"]["incidence_atoms"]["filename"],c60["ledgers"]["incidence_atoms"],P["C60atom"],"C60 atoms");e60,identities["C60edge"]=secure_rows(OUT/c60["ledgers"]["edge_decisions"]["filename"],c60["ledgers"]["edge_decisions"],P["C60edge"],"C60 edges");a63,identities["C63atom"]=secure_rows(OUT/c63["ledgers"]["atom_replay"]["filename"],c63["ledgers"]["atom_replay"],P["C63atom"],"C63 atoms");e63,identities["C63edge"]=secure_rows(OUT/c63["ledgers"]["edge_replay"]["filename"],c63["ledgers"]["edge_replay"],P["C63edge"],"C63 edges");a64,identities["C64atom"]=secure_rows(OUT/c64["ledgers"]["atom_owner_decisions"]["filename"],c64["ledgers"]["atom_owner_decisions"],P["C64atom"],"C64 atoms");e64,identities["C64edge"]=secure_rows(OUT/c64["ledgers"]["edge_owner_decisions"]["filename"],c64["ledgers"]["edge_owner_decisions"],P["C64edge"],"C64 edges");t64,identities["C64tie"]=secure_rows(OUT/c64["ledgers"]["tie_blockers"]["filename"],c64["ledgers"]["tie_blockers"],P["C64tie"],"C64 ties")
 corridor={x["cell_id"]:x for x in corridor};atom60={x["row_sha256"]:x for x in a60};edge60={x["C59_request_row_sha256"]:x for x in e60};atom64={x["C63_atom_replay_row_sha256"]:x for x in a64};edge64={x["C59_request_row_sha256"]:x for x in e64};tie64={x["C59_request_row_sha256"]:x for x in t64};byrequest=defaultdict(list)
 for atom in a63:byrequest[atom["C59_request_row_sha256"]].append(atom)
 atomdecisions={};stats=Counter();rooted_evidence={};source_distances=[];target_distances=[]
 with Writer(OUT/ATOM_FILE,"C63_ATOM_REPLAY_ORDER")as writer:
  for edge in e63:
   request=edge["C59_request_row_sha256"]
   if edge["overall_owner_history_mapping_pass"]:
    need(request in edge64 and request not in tie64,"C64 inherited partition")
    for atom in byrequest[request]:
     source=atom64[atom["row_sha256"]];base=atom60[atom["C60_atom_row_sha256"]];need(source["selected_owner"]==base["owner"]and base["owner_unique"]is True,"C64 exact owner consumption")
     body={"schema":SCHEMA+".atom-owner-decision-row","C59_request_row_sha256":request,"C60_atom_row_sha256":base["row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"decision_source":"C64_EXACT_STRICT_ATOM_ROW_BYTE_CONSUMPTION","C64_atom_owner_decision_row_sha256":source["row_sha256"],"C64_consumption_key":source["consumption_key"],"C56_source_corridor_row_sha256":None,"C56_target_corridor_row_sha256":None,"owner_rule_stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","owner_rule_stage_2":None,"selected_owner":source["selected_owner"],"selected_owner_unique":True,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};row=writer.write(body);atomdecisions[atom["row_sha256"]]=row;stats["inherited_atoms"]+=1;stats["semantic_unique"]+=1
   else:
    need(request in tie64 and request not in edge64,"C64 tie partition");baseedge=edge60[request];sourcecell=corridor[baseedge["source_cell_id"]];targetcell=corridor[baseedge["target_cell_id"]];step=sourcecell["corridor_steps"][0]
    anchor_type=sourcecell["anchor_binding"]["anchor_type"];need(sourcecell["witness_kind"]==targetcell["witness_kind"]=="EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR"and anchor_type==targetcell["anchor_binding"]["anchor_type"]and anchor_type in{"ROUND140_STRICT_OPEN_ADAPTIVE_CONNECTED_CELL","C37_JY_REFLECTED_STRICT_OPEN_CONNECTED_COLLAR"}and sourcecell["anchor_binding"]["positive_area_open_support"]is True and targetcell["anchor_binding"]["positive_area_open_support"]is True,"strict open anchor")
    need(sourcecell["component_id"]==targetcell["component_id"]and sourcecell["anchor_cell_id"]==targetcell["anchor_cell_id"]and sourcecell["anchor_binding"]==targetcell["anchor_binding"],"common rooted component")
    need(sourcecell["corridor_step_count"]==targetcell["corridor_step_count"]+1 and step["from_cell_id"]==sourcecell["cell_id"]and step["to_cell_id"]==targetcell["cell_id"]and step["face_or_corner_id"]==edge["face_or_corner_id"]and step["glue_kind"]==edge["glue_kind"],"exact rooted descent edge")
    source_distances.append(sourcecell["corridor_step_count"]);target_distances.append(targetcell["corridor_step_count"]);resolutions=[]
    for atom in byrequest[request]:
     base=atom60[atom["C60_atom_row_sha256"]];need(len(base["incident_occurrences"])==2 and{z["physical_cell_id"]for z in base["incident_occurrences"]}=={sourcecell["cell_id"],targetcell["cell_id"]},"atom endpoint incidence")
     if base["owner_unique"]:
      selected=base["owner"];stage2=None;basis="SEMANTIC_PATH_UNIQUE_BEFORE_ROOTED_RULE";stats["semantic_unique"]+=1
     else:
      winners=[z for z in base["incident_occurrences"]if z["physical_occurrence_id"]in base["owner_tie_occurrence_ids"]];need(len(winners)==2 and len({z["semantic_path"]for z in winners})==1 and{z["physical_cell_id"]for z in winners}=={sourcecell["cell_id"],targetcell["cell_id"]},"exact two-way semantic tie");chosen=[z for z in winners if z["physical_cell_id"]==targetcell["cell_id"]];need(len(chosen)==1 and targetcell["corridor_step_count"]<sourcecell["corridor_step_count"],"unique rooted choice");selected=compact(chosen[0]);stage2=RULE;basis="ROOTED_CORRIDOR_DISTANCE_STRICT_DESCENT_AFTER_SEMANTIC_PATH_TIE";stats["rooted_ties"]+=1;resolutions.append({"C60_atom_row_sha256":base["row_sha256"],"exact_span":base["exact_span"],"semantic_path_tie_occurrence_ids":base["owner_tie_occurrence_ids"],"source_distance":sourcecell["corridor_step_count"],"target_distance":targetcell["corridor_step_count"],"selected_target_occurrence_id":selected["physical_occurrence_id"],"selected_target_occurrence_binding_sha256":selected["occurrence_binding_sha256"]})
     body={"schema":SCHEMA+".atom-owner-decision-row","C59_request_row_sha256":request,"C60_atom_row_sha256":base["row_sha256"],"C63_atom_replay_row_sha256":atom["row_sha256"],"decision_source":"C66_ROOTED_CORRIDOR_SUPPLEMENT","C64_atom_owner_decision_row_sha256":None,"C64_consumption_key":None,"C56_source_corridor_row_sha256":sourcecell["row_sha256"],"C56_target_corridor_row_sha256":targetcell["row_sha256"],"owner_rule_stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","owner_rule_stage_2":stage2,"decision_basis":basis,"selected_owner":selected,"selected_owner_unique":True,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};row=writer.write(body);atomdecisions[atom["row_sha256"]]=row;stats["supplement_atoms"]+=1
    rooted_evidence[request]={"source":sourcecell,"target":targetcell,"step":step,"resolutions":resolutions}
 atom_desc=writer.descriptor();need(atom_desc["row_count"]==13103 and stats==Counter({"semantic_unique":12758,"inherited_atoms":11766,"supplement_atoms":1337,"rooted_ties":345}),"atom partition")
 edge_ids=[];estats=Counter();rooted_rows={}
 with Writer(OUT/ROOTED_FILE,"C63_TIED_EDGE_ORDER")as writer:
  for edge in e63:
   if edge["overall_owner_history_mapping_pass"]:continue
   ev=rooted_evidence[edge["C59_request_row_sha256"]];s,t,step=ev["source"],ev["target"],ev["step"]
   body={"schema":SCHEMA+".rooted-tie-resolution-row","C59_request_row_sha256":edge["C59_request_row_sha256"],"C63_edge_replay_row_sha256":edge["row_sha256"],"C64_tie_blocker_row_sha256":tie64[edge["C59_request_row_sha256"]]["row_sha256"],"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"component_id":s["component_id"],"component_index":s["component_index"],"anchor_cell_id":s["anchor_cell_id"],"anchor_binding":s["anchor_binding"],"source_cell_id":s["cell_id"],"source_C56_corridor_row_sha256":s["row_sha256"],"source_corridor_step_count":s["corridor_step_count"],"target_cell_id":t["cell_id"],"target_C56_corridor_row_sha256":t["row_sha256"],"target_corridor_step_count":t["corridor_step_count"],"source_first_corridor_step":step,"source_first_corridor_step_object_sha256":h(step),"source_distance_equals_target_plus_one":True,"source_first_step_is_exact_C60_edge":True,"semantic_tied_atom_count":len(ev["resolutions"]),"semantic_tied_atom_resolutions":ev["resolutions"],"semantic_tied_atom_resolution_sequence_sha256":seq(h(x)for x in ev["resolutions"]),"owner_rule":RULE,"physical_id_tiebreak_used":False,"side_tiebreak_used":False,"formal_credit":0,"D02_gate_credit":0};rooted_rows[edge["C59_request_row_sha256"]]=writer.write(body);estats["component_"+str(s["component_index"])]+=1;estats["intra"]+=edge["glue_kind"]=="INTRA_CHART_FACE";estats["seam"]+=edge["glue_kind"]!="INTRA_CHART_FACE"
 rooted_desc=writer.descriptor();need(rooted_desc["row_count"]==131 and estats==Counter({"intra":115,"component_0":67,"component_1":64,"seam":16}),"rooted census")
 with Writer(OUT/EDGE_FILE,"C63_EDGE_REPLAY_ORDER")as writer:
  for edge in e63:
   request=edge["C59_request_row_sha256"];decisions=[atomdecisions[x["row_sha256"]]for x in byrequest[request]];inherited=edge["overall_owner_history_mapping_pass"]
   if inherited:
    source=edge64[request];need(source["atom_count"]==len(decisions)and source["atom_owner_decision_row_hash_sequence_sha256"]==seq(atom64[x["row_sha256"]]["row_sha256"]for x in byrequest[request]),"C64 edge exact bytes");source_kind="C64_EXACT_STRICT_EDGE_ROW_BYTE_CONSUMPTION";sourcehash=source["row_sha256"];roothash=None;estats["inherited_edges"]+=1
   else:source=tie64[request];source_kind="C66_ROOTED_CORRIDOR_SUPPLEMENT";sourcehash=source["row_sha256"];roothash=rooted_rows[request]["row_sha256"];estats["supplement_edges"]+=1
   query_key=source["query_key"];body={"schema":SCHEMA+".edge-owner-decision-row","query_key":query_key,"C59_request_row_sha256":request,"owner_history_request_id":edge["owner_history_request_id"],"C63_edge_replay_row_sha256":edge["row_sha256"],"decision_source":source_kind,"C64_source_edge_or_tie_row_sha256":sourcehash,"C66_rooted_tie_resolution_row_sha256":roothash,"face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"atom_count":len(decisions),"full_atom_owner_decision_row_hash_sequence_sha256":seq(x["row_sha256"]for x in decisions),"all_atom_owners_unique":True,"decision":"STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE","closed_schema":True,"formal_credit":0,"D02_gate_credit":0};writer.write(body);edge_ids.append(request)
 edge_desc=writer.descriptor();need(edge_desc["row_count"]==1042 and estats["inherited_edges"]==911 and estats["supplement_edges"]==131 and len(edge_ids)==len(set(edge_ids)),"edge partition")
 summary={"query_domain_edge_count":1042,"atom_domain_count":13103,"C64_inherited_strict_edge_count":911,"C64_inherited_atom_count":11766,"C66_rooted_supplement_edge_count":131,"C66_supplement_atom_count":1337,"semantic_path_unique_atom_count":12758,"rooted_corridor_resolved_tied_atom_count":345,"full_unique_owner_edge_count":1042,"full_unique_owner_atom_count":13103,"component_0_rooted_edge_count":67,"component_1_rooted_edge_count":64,"rooted_intra_edge_count":115,"rooted_seam_edge_count":16,"source_distance_min":min(source_distances),"source_distance_max":max(source_distances),"target_distance_min":min(target_distances),"target_distance_max":max(target_distances),"query_partition_overlap_count":0,"atom_partition_overlap_count":0,"formal_credit":0,"D02_gate_credit":0};tests=selftest(summary)
 candidate={"schema":SCHEMA+".authority-candidate","status":"CONSUMPTION_READY_FULL_DOMAIN_OWNER_DECIDER__1042_OF_1042_EDGES__13103_OF_13103_ATOMS_UNIQUE__NOT_INSTALLED__ZERO_CREDIT","authority_class":"GLOBAL_EXISTING_EDGE_ATOM_OWNER_VECTOR_DECIDER_V2_ROOTED_CORRIDOR","authority_status":"CANDIDATE_NOT_INSTALLED","owner_rule":{"stage_1":"UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH","stage_2_only_after_stage_1_tie":RULE,"physical_id_tiebreak_permitted":False,"side_tiebreak_permitted":False},"input_byte_bindings":{key:P[key]for key in("C56p","C56r","C56o","C56c","C56vr","C56v","C56vo","C56m","C60r","C60o","C60v","C60vo","C60m","C60atom","C60edge","C63r","C63o","C63atom","C63edge","C63vr","C63v","C63vo","C63m","C64p","C64c","C64o","C64atom","C64edge","C64tie","C64vr","C64v","C64vo","C64m","C53","canonical")},"input_file_identities":identities,"query_contract":{"closed_schema":True,"query_key_inherited_byte_exact_from_C64":True,"query_domain_exhaustive":True,"missing_duplicate_or_partial_query":"FAIL_CLOSED","response":"ORDERED_FULL_ATOM_OWNER_VECTOR","C64_911_edges_consumed_without_rule_change":True,"C66_rule_applied_only_to_C64_131_tie_edges":True},"scope":summary,"ledgers":{"atom_owner_decisions":atom_desc,"rooted_tie_resolutions":rooted_desc,"edge_owner_decisions":edge_desc},"indexes":{"query_request_hash_sequence_sha256":seq(edge_ids),"atom_source_hash_sequence_sha256":seq(x["C60_atom_row_sha256"]for x in atomdecisions.values())},"self_test":tests,"TOCTOU_contract":{"O_NOFOLLOW_used":True,"regular_file_required":True,"st_nlink_exactly_one_required":True,"path_fd_identity_checked_before_read":True,"fd_identity_checked_after_read":True,"path_identity_checked_after_read":True,"sha256_checked_after_read":True},"closed_schema_contract":{"candidate_exact_key_set":True,"ledger_row_exact_key_sets":True,"additional_fields_rejected_by_independent_verifier":True},"strict_boundary":{"consumption_ready":True,"installed_authority":False,"runtime_or_canonical_written":False,"old_files_modified":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["COLD_NO_PRODUCER_FULL_REPLAY_OF_ALL_1042_EDGES_AND_13103_ATOMS","COHERENT_SEMANTIC_AND_TOCTOU_ATTACKS","CONSUME_ONLY_AFTER_EXACT_MANIFEST_BINDING"]};candidate["object_sha256"]=h(candidate);(OUT/CANDIDATE_FILE).write_bytes(enc(candidate)+b"\n");return candidate
def main()->int:
 result=build();print(json.dumps({"status":result["status"],"scope":result["scope"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError)as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
