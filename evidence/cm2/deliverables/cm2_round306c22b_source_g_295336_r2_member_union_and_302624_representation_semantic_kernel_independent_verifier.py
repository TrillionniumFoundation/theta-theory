#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sqlite3,sys,tempfile
from collections import Counter
from contextlib import nullcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator,TextIO

ROOT=Path(__file__).resolve().parent
P="cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel";L=P+"_ledger.jsonl.gz";R=P+"_result.json"
C22AL="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz";C22AR="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_result.json";C22AV="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_verification.json";C22AM="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_manifest.sha256"
B1M="cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz";C16M="cm2_round306c16a_source_g_identity_representation_family_replay_member_identity_family_ledger.jsonl.gz";C16R="cm2_round306c16a_source_g_identity_representation_family_replay_representation_ledger.jsonl.gz";C16RESULT="cm2_round306c16a_source_g_identity_representation_family_replay_result.json";C16V="cm2_round306c16a_source_g_identity_representation_family_replay_verification.json";C16MAN="cm2_round306c16a_source_g_identity_representation_family_replay_manifest.sha256"
K2R="cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_representation_index.jsonl.gz";K2RESULT="cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_result.json";K2V="cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_verification.json";K2MAN="cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256"
WLEDGER="cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_theorem_ledger.json";WRESULT="cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_result.json";WV="cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_verification.json";WMAN="cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_manifest.sha256";R287="cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
PINS={C22AL:"e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",C22AR:"597062fe7f9264b2756e92edc712570d279ed16928e5ff5ed560cc6f1d2bf234",C22AV:"5412211a2985486be05ce133dc91d9ca81ce21ad5866a76d21571a0e79a6ea52",C22AM:"888305210de3a93904e6fb26a199ff8d8e11519940550f0f58f2733cdfbbfcce",B1M:"4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7",C16M:"0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a",C16R:"47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1",C16RESULT:"85e692b6e6889ab8fe3c74ede8e11d48aae664988ed93da7a139d3d9137599f8",C16V:"1c9a1ff52673a9865741b95b400c23176bb27563644705b637a3609c20fb6436",C16MAN:"597a9a402190989baa72f0e7955be376b3142850695096e2fdc6d651ce3ce7f4",K2R:"28dccab4f9bbba76171329fb4c55328592e8264686d14d2b47da8efc39867aca",K2RESULT:"65ed7a13792edfe7609662126e4357b9e1ebff39b7d749a959b5a19cb3d5e96a",K2V:"5aa7f0e436835ac427cedd3c214d268832ac84894c519c920c5e42956c5f8280",K2MAN:"e06efae8395e96cf3c1d0489c4de58cbc5e05357b6789f6fb1e56906b6026970",WLEDGER:"e3c27d4e7159aadd4adf35fe98c81f8534de6af0b4d6b6436ec1cffa9fe51bb4",WRESULT:"ed28b179673e0fcd108d4b99be31c0b4ced75236c6e29187218cd06ba4e5dac1",WV:"700b362c6b82ec32eb92262c17a1942ce2a1ba84764b8873cb298a6b593a19ed",WMAN:"37cba25a0663626d54cf1fc3ba5cb7001c799ccffb1b3c1eef48157475444fed",R287:"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"}
READ=1<<18;CAP=10<<20;DEC=json.JSONDecoder()
class E(RuntimeError):pass
def need(value:bool,label:str)->None:
 if type(value)is not bool or not value:raise E(label)
def canon(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(value:Any)->str:return hashlib.sha256(canon(value)).hexdigest()
def file_hash(path:Path)->str:
 state=hashlib.sha256()
 with path.open("rb")as stream:
  while block:=stream.read(1048576):state.update(block)
 return state.hexdigest()
def check_row(row:dict[str,Any],label:str)->None:
 body=dict(row);need(body.pop("row_sha256",None)==digest(body),label)
def check_result(result:dict[str,Any],label:str)->str:
 body=dict(result);claimed=body.pop("result_sha256",None);need(type(claimed)is str and claimed==digest(body),label);return claimed
def iter_array(stream:TextIO,marker:str)->Iterator[Any]:
 def more(buffer:str)->str:
  block=stream.read(READ);need(bool(block),"truncated");out=buffer+block;need(len(out.encode())<=CAP,"buffer cap");return out
 buffer=""
 while marker not in buffer:buffer=more(buffer);buffer=buffer[-max(len(marker)-1,1):]if marker not in buffer else buffer
 buffer=buffer[buffer.find(marker)+len(marker):].lstrip()
 if buffer.startswith(":"):buffer=buffer[1:].lstrip();need(buffer.startswith("["),"array marker");buffer=buffer[1:]
 comma=False
 while True:
  buffer=buffer.lstrip()
  while not buffer:buffer=more(buffer).lstrip()
  if buffer[0]=="]":return
  if comma:need(buffer[0]==",","comma");buffer=buffer[1:].lstrip()
  while True:
   try:value,end=DEC.raw_decode(buffer);break
   except json.JSONDecodeError:buffer=more(buffer)
  yield value;buffer=buffer[end:];comma=True
def gz_rows(path:Path)->Iterator[dict[str,Any]]:
 with gzip.open(path,"rb")as stream:
  for line in stream:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];row=json.loads(raw);need(canon(row)==raw,"canonical row");check_row(row,"row closure");yield row
def insert_rows(db:sqlite3.Connection,sql:str,rows:Iterator[tuple[Any,...]])->int:
 batch=[];count=0
 for row in rows:
  batch.append(row);count+=1
  if len(batch)==4096:db.executemany(sql,batch);batch=[]
 if batch:db.executemany(sql,batch)
 return count
def manifest_has(name:str,member:str,sha:str)->bool:
 return any(len(parts:=line.split(None,1))==2 and parts[0]==sha and Path(parts[1].strip()).name==member for line in(ROOT/name).read_text().splitlines())
def validate_sources()->dict[str,str]:
 for name,sha in PINS.items():need(file_hash(ROOT/name)==sha,"pin:"+name)
 c22a=json.loads((ROOT/C22AR).read_bytes());c22a_sha=check_result(c22a,"C22a result");v=json.loads((ROOT/C22AV).read_bytes());need(c22a["predicate_cell_support_set_equality_credit"]==295340 and c22a["remaining_R2_member_support_debt"]==295336 and v["status"].startswith("PASS_INDEPENDENT_295340_ROW_RECONSTRUCTION")and manifest_has(C22AM,C22AL,PINS[C22AL])and manifest_has(C22AM,C22AV,PINS[C22AV]),"C22a seal")
 c16=json.loads((ROOT/C16RESULT).read_bytes());c16_sha=check_result(c16,"C16 result");v=json.loads((ROOT/C16V).read_bytes());need(c16["member_census"]["family_counts"]["R2"]==295336 and c16["representation_census"]["family_counts"]["R2"]==302624 and v["status"].startswith("PASS_INDEPENDENT_VERIFIER")and manifest_has(C16MAN,C16M,PINS[C16M])and manifest_has(C16MAN,C16R,PINS[C16R]),"C16 seal")
 k2=json.loads((ROOT/K2RESULT).read_bytes());v=json.loads((ROOT/K2V).read_bytes());need(k2["status"]=="PASS_EXACT_R2_MECHANICAL_IDENTITY_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT"and v["status"]=="PASS_INDEPENDENT_COLD_REPLAY_EXACT_R2_MECHANICAL_INDEX__ZERO_THEOREM_CREDIT"and k2["exact_census"]["R2_representation_count"]==302624 and k2["exact_census"]["R2_R287_alias_representation_count"]==7288 and all(value==0 for value in v["anti_join_gaps"].values())and manifest_has(K2MAN,K2R,PINS[K2R])and manifest_has(K2MAN,K2V,PINS[K2V]),"K2 seal")
 wr=json.loads((ROOT/WRESULT).read_bytes());wv=json.loads((ROOT/WV).read_bytes());need(wr["result_sha256"]==digest(wr["result"])and wv["status"].startswith("PASS_INDEPENDENT_REPLAY__4_LOCAL_REGLUES")and wv["credit"]["r2_artificial_face_reglue"]==4 and wv["theorem_ledger_sha256"]==PINS[WLEDGER]and manifest_has(WMAN,WLEDGER,PINS[WLEDGER])and manifest_has(WMAN,WV,PINS[WV]),"W seal")
 return{"C22a_result_object_sha256":c22a_sha,"C16_result_object_sha256":c16_sha,"K2_verification_sha256":PINS[K2V],"W_verification_sha256":PINS[WV]}
def setup(path:Path)->sqlite3.Connection:
 db=sqlite3.connect(":memory:");db.executescript("""PRAGMA journal_mode=OFF;PRAGMA synchronous=OFF;PRAGMA temp_store=MEMORY;PRAGMA cache_size=-524288;
 CREATE TABLE cell(id TEXT PRIMARY KEY,owner TEXT,support_json TEXT,support_sha TEXT,row_sha TEXT);
 CREATE TABLE member(id TEXT PRIMARY KEY,union_id TEXT,envelopes_json TEXT,cells_json TEXT,normalization_json TEXT,row_sha TEXT,primary_seen INTEGER DEFAULT 0,primary_semantic_sha TEXT);
 CREATE TABLE c16m(id TEXT PRIMARY KEY,component TEXT,root TEXT,official_key TEXT,row_sha TEXT);
 CREATE TABLE c16r(id TEXT PRIMARY KEY,owner TEXT,component TEXT,root TEXT,official_key TEXT,row_sha TEXT,seen INTEGER DEFAULT 0);
 CREATE TABLE r287(rep_id TEXT PRIMARY KEY,source_row_id TEXT,source_kind TEXT,row_sha TEXT,payload_json TEXT);
 """);return db
def load(db:sqlite3.Connection)->dict[str,int]:
 def cells():
  for row in gz_rows(ROOT/C22AL):
   need(row["formal_credit"]=={"member_normalized_support":0,"predicate_cell_support_set_equality":1,"representation_cover":0},"C22a credit");yield row["predicate_cell_row_id"],row["owner_member_id"],canon(row["support_ast"]).decode(),row["support_ast_sha256"],row["row_sha256"]
 a=insert_rows(db,"INSERT INTO cell VALUES(?,?,?,?,?)",cells())
 def members():
  with gzip.open(ROOT/B1M,"rt")as stream:
   for row in iter_array(stream,'"member_union_rows"'):
    check_row(row,"B1 member");need(row["outer_envelope_union_structurally_exact"]is True and row["formal_full_support_credit"]==0 and len(row["normalized_outer_envelopes"])==1 and len(row["predicate_source_cell_row_ids"])==row["predicate_source_cell_multiplicity"]and row["predicate_source_cell_multiplicity"]in(1,2),"B1 shape");yield row["member_id"],row["Round306B1R0_member_union_row_id"],canon(row["normalized_outer_envelopes"]).decode(),canon(row["predicate_source_cell_row_ids"]).decode(),None if row["Round271_W_tail_parent_normalization"]is None else canon(row["Round271_W_tail_parent_normalization"]).decode(),row["row_sha256"],0,None
 b=insert_rows(db,"INSERT INTO member VALUES(?,?,?,?,?,?,?,?)",members())
 def c16m():
  for row in gz_rows(ROOT/C16M):
   if row["coarse_family"]=="R2":need(row["formal_credit"]["identity"]==row["formal_credit"]["family"]==1,"C16 member credit");yield row["member_id"],row["fresh_component_id"],row["base_root_id"],row["official_key_id"],row["row_sha256"]
 c=insert_rows(db,"INSERT INTO c16m VALUES(?,?,?,?,?)",c16m())
 def c16r():
  for row in gz_rows(ROOT/C16R):
   if row["coarse_family"]=="R2":need(row["formal_credit"]["representation_identity"]==row["formal_credit"]["representation_owner_binding"]==1 and row["formal_credit"]["normalized_support"]==0,"C16 rep credit");yield row["representation_id"],row["owner_member_id"],row["fresh_component_id"],row["base_root_id"],row["official_key_id"],row["row_sha256"],0
 d=insert_rows(db,"INSERT INTO c16r VALUES(?,?,?,?,?,?,?)",c16r())
 def r287():
  with gzip.open(ROOT/R287,"rt")as stream:
   for row in iter_array(stream,'"region_rows"'):
    check_row(row,"R287 region")
    if row["disposition"]!="EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY":continue
    need(row["exact_inclusion_alias_lemma_satisfied"]is True,"region lemma");payload={key:row[key]for key in("containing_atom_id","disposition","exact_inclusion_alias_lemma_satisfied","source_chart","adjacent_chart","owner_target","physical_t_sign","physical_t_square_open_interval","R275_region_kind")};yield row["Round275_region_id"],row["Round287_region_disposition_row_id"],"ROUND287_R275_REGION_INCLUSION_SUBCOVER",row["row_sha256"],canon(payload).decode()
  with gzip.open(ROOT/R287,"rt")as stream:
   for row in iter_array(stream,'"refinement_cell_rows"'):
    check_row(row,"R287 refinement")
    if row["disposition"]!="EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY":continue
    need(row["exact_inclusion_alias_lemma_satisfied"]is True,"refinement lemma");payload={key:row[key]for key in("containing_atom_id","disposition","exact_inclusion_alias_lemma_satisfied","source_chart","adjacent_chart","owner_target","physical_t_sign","physical_t_square_open_interval","coordinate_box","Round286_coordinate_occupancy_count","signed_region_cell_state")};yield row["Round286_refinement_cell_id"],row["Round287_refinement_cell_disposition_row_id"],"ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER",row["row_sha256"],canon(payload).decode()
 e=insert_rows(db,"INSERT INTO r287 VALUES(?,?,?,?,?)",r287());db.commit();need((a,b,c,d,e)==(295340,295336,295336,302624,8008),"source census");need(db.execute("SELECT COUNT(*) FROM cell x LEFT JOIN member m ON m.id=x.owner WHERE m.id IS NULL").fetchone()[0]==0 and db.execute("SELECT COUNT(*) FROM member m LEFT JOIN c16m c ON c.id=m.id WHERE c.id IS NULL").fetchone()[0]==0,"source anti-join");return{"cells":a,"members":b,"c16_members":c,"c16_representations":d,"R287_rows":e}
def wtail_rows()->dict[str,dict[str,Any]]:
 doc=json.loads((ROOT/WLEDGER).read_bytes());need(doc["row_count"]==len(doc["rows"])==4,"W count");out={}
 for row in doc["rows"]:
  check_row(row,"W row");conclusion=row["local_conclusion"];need(conclusion["two_source_cells_are_one_local_physical_region_across_interface"]is True and conclusion["artificial_interface_is_not_F_zero_physical_separator"]is True and conclusion["candidate_r2_artificial_face_reglue_credit"]==1,"W conclusion");out[row["member_id"]]=row
 need(len(out)==4,"W uniqueness");return out
def support_and_theorem(member_id:str,envelopes:list[Any],cells:list[dict[str,Any]],normalization:dict[str,Any]|None,wtail:dict[str,dict[str,Any]])->tuple[dict[str,Any],dict[str,Any],str|None]:
 parent=envelopes[0];charts={row["support_ast"]["coordinate_chart"]for row in cells};need(len(charts)==1 and all(row["support_ast"]["kind"]=="OPEN_RATIONAL_BOX"for row in cells),"cell supports");support={"kind":"OPEN_RATIONAL_BOX","coordinate_chart":next(iter(charts)),"coordinates":["t","p","s"],"bounds":parent};bindings=[{"predicate_cell_row_id":row["id"],"C22a_row_sha256":row["row_sha"],"support_ast_sha256":row["support_sha"]}for row in cells]
 if len(cells)==1:
  need(normalization is None and cells[0]["support_ast"]["bounds"]==parent,"single union");return support,{"kind":"R2_MEMBER_PREDICATE_CELL_UNION_EQUALS_NORMALIZED_SUPPORT","union_mode":"SINGLE_SOURCE_FREE_EXACT_OPEN_BOX","predicate_cell_equalities":bindings,"B1R0_outer_envelope_union_structurally_exact":True,"cell_union_equals_member_physical_support":True,"member_physical_support_equals_normalized_support_ast":True},None
 need(len(cells)==2 and normalization is not None and member_id in wtail,"W member");interface=normalization["artificial_interface"];need(normalization["normalization_kind"]=="ROUND271_ARTIFICIAL_T_BISECTION_PARENT_NORMALIZATION"and normalization["normalized_parent_box"]==parent and normalization["interface_is_not_a_physical_support_boundary"]is True and interface["axis"]=="t","W normalization");boxes=sorted((row["support_ast"]["bounds"]for row in cells),key=lambda box:Q(box[0]));need(boxes[0][0]==parent[0]and boxes[0][1]==interface["value"]and boxes[1][0]==interface["value"]and boxes[1][1]==parent[1]and all(box[2:]==parent[2:]for box in boxes),"W partition");sealed=wtail[member_id];need(set(sealed["canonical_input_commitment"]["input_rows"]["B1R0_cell_row_ids"])=={row["id"]for row in cells},"W cells");theorem={"kind":"R2_MEMBER_PREDICATE_CELL_UNION_EQUALS_NORMALIZED_SUPPORT","union_mode":"TWO_CHILD_OPEN_BOXES_PLUS_SEALED_ARTIFICIAL_FACE_REGLUE","predicate_cell_equalities":bindings,"artificial_interface":interface,"sealed_reglue_theorem_row_id":sealed["theorem_row_id"],"sealed_reglue_theorem_row_sha256":sealed["row_sha256"],"sealed_reglue_verification_sha256":PINS[WV],"B1R0_outer_envelope_union_structurally_exact":True,"two_child_cells_plus_nonseparating_interface_equal_parent_open_box":True,"cell_union_equals_member_physical_support":True,"member_physical_support_equals_normalized_support_ast":True};return support,theorem,sealed["row_sha256"]
def verify(candidate:Path)->dict[str,Any]:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"runtime");seals=validate_sources();raw=(candidate/R).read_bytes();result=json.loads(raw);need(canon(result)==raw,"result canonical");claimed=check_result(result,"result closure");need(result["status"]=="PASS_295336_R2_MEMBER_SUPPORTS_AND_302624_TYPED_REPRESENTATION_SEMANTICS__R2_CLOSED"and(result["R2_member_normalized_support_set_equality_credit"],result["R2_remaining_member_support_debt"],result["R2_primary_representation_set_equality_credit"],result["R2_alias_exact_subcover_inclusion_disposition_credit"],result["R2_typed_representation_semantic_credit"],result["R2_remaining_representation_semantic_debt"])==(295336,0,295336,7288,302624,0),"result census");need((result["cumulative_global_member_support_credit"],result["remaining_global_member_support_debt"])==(477408,24796)and result["remaining_global_member_debt_by_family"]=={"G2A":5264,"G2B":10128,"R292":9404}and result["strict_nonpromotion"]=={"new_DSU_edges":0,"new_DSU_unions":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"global boundary");need(result["input_pins"]==[{"filename":name,"sha256":sha}for name,sha in sorted(PINS.items())],"pins")
 with nullcontext(".")as scratch:
  db=setup(Path(scratch)/"index.sqlite");source_census=load(db);wtail=wtail_rows();ledger=iter(gz_rows(candidate/L));sequence=hashlib.sha256();primary=aliases=ordinal=0;alias_kinds=Counter();alias_owners=set();wtail_used=set()
  for old in gz_rows(ROOT/K2R):
   need(all(value==0 for value in old["formal_credit"].values()),"old zero");rep_id=old["representation_id"];owner=old["owner_member_id"];c16r=db.execute("SELECT owner,component,root,official_key,row_sha,seen FROM c16r WHERE id=?",(rep_id,)).fetchone();need(c16r is not None and c16r[0]==owner and c16r[5]==0,"C16 rep join");db.execute("UPDATE c16r SET seen=1 WHERE id=?",(rep_id,))
   if old["representation_role"]=="PRIMARY_MEMBER_PREDICATE_UNION_HANDLE":
    joined=db.execute("SELECT m.union_id,m.envelopes_json,m.cells_json,m.normalization_json,m.row_sha,m.primary_seen,c.component,c.root,c.official_key,c.row_sha FROM member m JOIN c16m c ON c.id=m.id WHERE m.id=?",(owner,)).fetchone();need(joined is not None and joined[5]==0,"member join");union_id,envelopes_json,cells_json,norm_json,b1_sha,_,component,root,official_key,c16m_sha=joined;need((component,root,official_key)==c16r[1:4],"identity agreement");cell_ids=json.loads(cells_json);cells=[]
    for cell_id in cell_ids:
     cell=db.execute("SELECT owner,support_json,support_sha,row_sha FROM cell WHERE id=?",(cell_id,)).fetchone();need(cell is not None and cell[0]==owner,"cell join");cells.append({"id":cell_id,"support_ast":json.loads(cell[1]),"support_sha":cell[2],"row_sha":cell[3]})
    need(old["source_B1R0_member_union_row_id"]==union_id and old["source_B1R0_member_row_sha256"]==b1_sha and old["predicate_source_cell_count"]==len(cells),"old primary");support,theorem,reglue=support_and_theorem(owner,json.loads(envelopes_json),cells,None if norm_json is None else json.loads(norm_json),wtail)
    if reglue is not None:wtail_used.add(owner)
    body={"schema":"cm2.round306c22b.source-g-295336-r2-member-union-and-302624-representation-semantic-kernel.v1.row.v1","ordinal":ordinal,"row_kind":"R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY","member_id":owner,"fresh_component_id":component,"base_root_id":root,"official_key_id":official_key,"representation_id":rep_id,"normalized_support_ast":support,"normalized_support_ast_sha256":digest(support),"member_union_theorem_ast":theorem,"member_union_theorem_ast_sha256":digest(theorem),"source_bindings":{"B1R0_member_union_row_id":union_id,"B1R0_member_row_sha256":b1_sha,"C16a_member_row_sha256":c16m_sha,"C16a_representation_row_sha256":c16r[4],"K2_mechanical_representation_row_sha256":old["row_sha256"],"C22a_result_object_sha256":seals["C22a_result_object_sha256"],"sealed_W_tail_reglue_row_sha256":reglue},"formal_credit":{"member_normalized_support_set_equality":1,"primary_representation_set_equality":1,"exact_subcover_inclusion_disposition":0,"typed_representation_semantic_disposition":1},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};primary+=1
   else:
    need(old["representation_role"]=="R287_EXACT_SUBCOVER_ALIAS","alias role");source=db.execute("SELECT source_row_id,source_kind,row_sha,payload_json FROM r287 WHERE rep_id=?",(rep_id,)).fetchone();need(source is not None,"alias source");source_id,source_kind,source_sha,payload_json=source;need((old["source_R287_row_id"],old["source_R287_row_sha256"])==(source_id,source_sha)and old["canonical_input_commitment"]["source_kind"]==source_kind,"alias join");owner_support=db.execute("SELECT primary_semantic_sha,primary_seen FROM member WHERE id=?",(owner,)).fetchone();need(owner_support is not None and owner_support[1]==1,"alias owner");payload=json.loads(payload_json);theorem={"kind":"R287_CONDITIONAL_EXACT_INCLUSION_CONSUMED_BY_SEALED_R294_ATOM_BINDING","source_kind":source_kind,"R287_source_row_id":source_id,"R287_source_row_sha256":source_sha,"R287_exact_inclusion_payload":payload,"sealed_K2_mechanical_binding_verification_sha256":seals["K2_verification_sha256"],"owner_primary_semantic_row_sha256":owner_support[0],"alias_support_is_exactly_included_in_owner_normalized_support":True,"full_set_equality_not_claimed":True};body={"schema":"cm2.round306c22b.source-g-295336-r2-member-union-and-302624-representation-semantic-kernel.v1.row.v1","ordinal":ordinal,"row_kind":"R2_R287_ALIAS_EXACT_SUBCOVER_INCLUSION_DISPOSITION","member_id":owner,"fresh_component_id":c16r[1],"base_root_id":c16r[2],"official_key_id":c16r[3],"representation_id":rep_id,"subcover_theorem_ast":theorem,"subcover_theorem_ast_sha256":digest(theorem),"source_bindings":{"C16a_representation_row_sha256":c16r[4],"K2_mechanical_representation_row_sha256":old["row_sha256"],"K2_manifest_sha256":PINS[K2MAN],"R287_ledger_sha256":PINS[R287]},"formal_credit":{"member_normalized_support_set_equality":0,"primary_representation_set_equality":0,"exact_subcover_inclusion_disposition":1,"typed_representation_semantic_disposition":1},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};aliases+=1;alias_kinds[source_kind]+=1;alias_owners.add(owner)
   expected={**body,"row_sha256":digest(body)};actual=next(ledger,None);need(actual==expected,"full row reconstruction");sequence.update(bytes.fromhex(actual["row_sha256"]));ordinal+=1
   if body["row_kind"].startswith("R2_PRIMARY"):db.execute("UPDATE member SET primary_seen=1,primary_semantic_sha=? WHERE id=?",(actual["row_sha256"],owner))
  need(next(ledger,None)is None and(ordinal,primary,aliases)==(302624,295336,7288),"ledger exhaustion");need(db.execute("SELECT COUNT(*) FROM member WHERE primary_seen<>1 OR primary_semantic_sha IS NULL").fetchone()[0]==0 and db.execute("SELECT COUNT(*) FROM c16r WHERE seen<>1").fetchone()[0]==0,"identity exhaustion");need(alias_kinds=={"ROUND287_R275_REGION_INCLUSION_SUBCOVER":2476,"ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER":4812}and len(alias_owners)==384 and wtail_used==set(wtail),"semantic census");db.close()
 need(result["source_census"]==source_census and result["R2_alias_source_kind_census"]==dict(alias_kinds)and result["R2_alias_owner_member_count"]==384 and result["R2_W_tail_sealed_reglue_consumed"]==4,"result replay census");descriptor=result["ledger"];need(descriptor["filename"]==L and descriptor["row_count"]==302624 and descriptor["size"]==(candidate/L).stat().st_size and descriptor["sha256"]==file_hash(candidate/L)and descriptor["row_sequence_sha256"]==sequence.hexdigest(),"ledger descriptor");return{"status":"PASS_INDEPENDENT_C22B_295336_MEMBER_AND_302624_REPRESENTATION_FULL_RECONSTRUCTION__R2_CLOSED_NO_GLOBAL_PROMOTION","result_sha256":claimed,"rows":302624,"member_supports":295336,"alias_dispositions":7288}
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument("--candidate-dir");args=parser.parse_args();candidate=ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve();print(canon(verify(candidate)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
