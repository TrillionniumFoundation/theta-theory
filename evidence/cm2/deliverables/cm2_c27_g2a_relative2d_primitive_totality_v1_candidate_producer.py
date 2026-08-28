#!/usr/bin/env python3
"""Primitive-only G2A/G2B vs current C22A/C23A candidate materializer.

No C27 artifact and no historical edge ledger is opened at all.  Any R300C
comparison belongs to a later post-hoc validator and is excluded from this
authority producer and its manifest.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,os,stat
from collections import Counter,defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any,Iterator

ROOT=Path(__file__).resolve().parent
R235="cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json"
R236="cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R242="cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json"
C4="cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz"
C5="cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz"
C10="cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C14A="cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_equality_ledger.jsonl.gz"
C14B="cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_exact_sheet_member_ledger.jsonl.gz"
C15="cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C22="cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz"
C23="cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz"
C24="cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C25="cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26="cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
PINS={R235:"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787",R236:"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",R242:"8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e",C4:"3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db",C5:"8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333",C10:"b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",C14A:"09aff7b141e519a1d7252e4ad8becdb668b8b12f84c99cdb69ffe43ae3529883",C14B:"6f69b5e82377cde72e7223e86b518da12e19ef85b93a5706989ebb81ab78a6d6",C15:"e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",C22:"e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb",C23:"230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528",C24:"ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",C25:"66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",C26:"fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e"}
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def canon(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def dig(v):return hashlib.sha256(canon(v)).hexdigest()
def closed(v):return {**v,"row_sha256":dig(v)}
def check(row,label):b=dict(row);need(b.pop("row_sha256",None)==dig(b),label+":closure")
def fp(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
@dataclass
class Cap:
 name:str;fd:int;pre:tuple;sha:str
 @classmethod
 def open(cls,name):
  fd=os.open(ROOT/name,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0));s=os.fstat(fd);need(stat.S_ISREG(s.st_mode),name+":regular");h=hashlib.sha256()
  while b:=os.read(fd,4<<20):h.update(b)
  got=h.hexdigest();need(got==PINS[name],name+":pin");need(fp(os.fstat(fd))==fp(s),name+":hash-stat");return cls(name,fd,fp(s),got)
 def rows(self):
  os.lseek(self.fd,0,0);dup=os.dup(self.fd)
  with os.fdopen(dup,"rb") as raw:
   with gzip.GzipFile(fileobj=raw,mode="rb") as z:
    for i,line in enumerate(z):
     need(line.endswith(b"\n"),self.name+":newline");wire=line[:-1];r=json.loads(wire);need(canon(r)==wire,self.name+":canonical");check(r,self.name+":"+str(i));yield r
  need(fp(os.fstat(self.fd))==self.pre,self.name+":parse-stat")
 def json(self):
  os.lseek(self.fd,0,0);chunks=[]
  while b:=os.read(self.fd,4<<20):chunks.append(b)
  x=json.loads(b"".join(chunks));need(fp(os.fstat(self.fd))==self.pre,self.name+":json-stat");return x
 def att(self):need(fp(os.fstat(self.fd))==self.pre,self.name+":final-stat");return{"filename":self.name,"sha256":self.sha,"stat":list(self.pre),"single_stable_O_NOFOLLOW_fd":True}
 def close(self):os.close(self.fd)
def cert(c):x=c.json();need(set(x)=={"schema","result","result_sha256"} and x["result_sha256"]==dig(x["result"]),c.name+":cert");return x["result"]
def ints(ast):
 out={}
 def w(x):
  if type(x)is dict:
   if x.get("op")in{"OPEN_INTERVAL","CLOSED_INTERVAL"}and x.get("coordinate")in{"t","p","s"}:out[x["coordinate"]]=(Q(x["lower"]),Q(x["upper"]))
   for v in x.values():w(v)
  elif type(x)is list:
   for v in x:w(v)
 w(ast);need(set(out)=={"t","p","s"},"unique tps envelope");return(out["t"]+out["p"]+out["s"])
def predicate(ast):
 out=[]
 def w(x):
  if type(x)is dict:
   if x.get("op")in{"LT","GT"}:out.append(x)
   else:
    for v in x.values():w(v)
  elif type(x)is list:
   for v in x:w(v)
 w(ast);need(len(out)==1,"one strict predicate");return out[0]
def inter(a,b):
 z=[]
 for i in range(0,6,2):
  lo=max(a[i],b[i]);hi=min(a[i+1],b[i+1])
  if lo>=hi:return None
  z += [lo,hi]
 return tuple(z)
def t2inter(carrier,b,sign):
 p0,p1=max(carrier[2],b[2]),min(carrier[3],b[3]);s0,s1=max(carrier[4],b[4]),min(carrier[5],b[5])
 if p0>=p1 or s0>=s1:return None
 lo,hi=carrier[:2];q0,q1=b[:2]
 if sign==1:
  if hi<=0:return None
  lo=max(lo,Q(0));a,bq=lo*lo,hi*hi
 else:
  if lo>=0:return None
  hi=min(hi,Q(0));a,bq=hi*hi,lo*lo
 x0,x1=max(q0,a),min(q1,bq)
 return None if x0>=x1 else(x0,x1,p0,p1,s0,s1)
def qtxt(x):return str(x.numerator)if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def boxtext(x):return list(map(qtxt,x))
@dataclass(slots=True)
class T:src:str;member:str;component:str;rowsha:str;chart:str;box:tuple;sign:int|None
@dataclass(slots=True)
class Node:center:Q;cross:list;left:Any;right:Any
def tree(xs):
 if not xs:return None
 c=sorted((x.box[2]+x.box[3])/2 for x in xs)[len(xs)//2];l=[];r=[];m=[]
 for x in xs:
  (l if x.box[3]<=c else r if x.box[2]>=c else m).append(x)
 need(bool(m),"tree pivot");return Node(c,m,tree(l),tree(r))
def query(n,lo,hi):
 if n is None:return
 for x in n.cross:
  if x.box[2]<hi and lo<x.box[3]:yield x
 if lo<n.center:yield from query(n.left,lo,hi)
 if n.center<hi:yield from query(n.right,lo,hi)
def write(path,rows):
 seq=hashlib.sha256();n=0
 with path.open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as z:
   for r in rows:w=canon(r);z.write(w+b"\n");seq.update(bytes.fromhex(r["row_sha256"]));n+=1
 h=hashlib.sha256(path.read_bytes()).hexdigest();return{"filename":path.name,"row_count":n,"file_sha256":h,"row_sequence_sha256":seq.hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--out-dir",required=True);ap.add_argument("--seed",type=int,required=True);a=ap.parse_args();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False);caps={n:Cap.open(n)for n in PINS}
 try:
  r235={r["endpoint_graph_partition_row_id"]:r["source_chart"]for r in cert(caps[R235])["single_endpoint_graph_partition_rows"]};r242={r["transition_sheet_patch_row_id"]:r["source_chart"]for r in cert(caps[R242])["formal_positive_2D_transition_sheet_patch_ledger"]["rows"]};r236={r["double_endpoint_partition_row_id"]:(r["same_sign_event_absent_signature"]["source_chart"],r["same_sign_event_absent_signature"]["target_chart"])for r in cert(caps[R236])["double_endpoint_partition_rows"]}
  c4={}
  for r in caps[C4].rows():c=r["canonical_input_commitment"];rid=c["R236_double_endpoint_partition_row"][1];c4[r["bridge_ordinal"]]=(c["B1G0_source_graph_row"],r236[rid][0])
  c5={}
  for r in caps[C5].rows():
   s=r["semantic_classification"]
   if s["classification"]!="POSITIVE_GRAPH":continue
   ch=None
   if s["kernel"]=="SEALED_C4_R235D_SOURCE_EXACT_FACE_GRAPH_BRIDGE":ch=c4[r["canonical_input_commitment"]["C4_bridge_row"][0]][1]
   c5[r["graph_id"]]=(r["graph_inventory_ordinal"],ch,r["row_sha256"])
  graphs={};classes=Counter()
  for r in caps[C10].rows():
   gid=r["graph_id"];cl=r["graph_class"]
   ch=r235[gid]if cl in{"R235_TARGET_POSITIVE_PARTIAL_BASE","R235_SOURCE_EXACT_FACE_FULL_BASE"}else r242[gid]if cl=="R242_UNIQUE_GRAPH_FULL_PATCH"else c5[gid][1]
   need(ch in{"G:N","G:S","G:E","G:W"},"C10 chart");graphs[gid]={"chart":ch,"box":ints(r["carrier_domain_ast"]),"class":cl,"rowsha":r["row_sha256"],"equation_sha":r["ast_sha256"]["equation_ast_sha256"]};classes[cl]+=1
  need(len(graphs)==5264,"C10 census")
  c14={}
  for r in caps[C14A].rows():c14[r["row_id"]]=(r["graph_id"],r["sheet_member_id"],r["row_sha256"],"C14A_EQ")
  for r in caps[C14B].rows():c14[r["row_id"]]=(r["graph_id"],r["new_exact_sheet_member_id"],r["row_sha256"],"C14B_EQ")
  need(len(c14)==5264,"C14 equality census")
  comp={};key={};c15sha={}
  for r in caps[C15].rows():m=r["registry_member_id"];comp[m]=r["fresh_component_id"];key[m]=r["official_key_id"];c15sha[m]=r["row_sha256"]
  need(len(comp)==502204,"C15 census")
  c25={}
  for r in caps[C25].rows():c25[r["member_id"]]=(r["source_bindings"]["support_kernel"],r["source_bindings"]["support_kernel_row_sha256"],r["normalized_support_ast_sha256"],r["row_sha256"])
  need(len(c25)==502204,"C25 census")
  g1=set();g2a_features=set()
  for r in caps[C26].rows():
   if r["node_id"]=="G1":g1.add(r["feature_id"])
   elif r["node_id"]=="G2A":g2a_features.add(r["feature_id"])
  need(len(g1)==len(g2a_features)==5264,"C26 G1/G2A cover")
  ga={};sides=defaultdict(list);c24bysha={}
  for r in caps[C24].rows():
   c24bysha[r["row_sha256"]]=r;gid=r["graph_id"];need(gid in graphs and r["member_id"]in comp,"C24 joins");need(c25[r["member_id"]][0]=="C24A"and c25[r["member_id"]][1]==r["row_sha256"],"C24/C25")
   if r["coarse_family"]=="G2A":
    au=r["semantic_theorem_ast"]["sealed_exact_support_authority"];need(au["row_id"]in c14,"C24/C14 id");x=c14[au["row_id"]];need(x[0]==gid and x[1]==r["member_id"]and x[2]==au["row_sha256"]and x[3]==au["role"],"C24/C14 binding");need(gid in g1 and r["member_id"]in g2a_features,"C26 binding");ga[gid]=r
   else:sides[gid].append(r)
  need(len(ga)==5264 and sum(map(len,sides.values()))==9960 and set(ga)==set(sides),"C24 graph totality")
  targets=defaultdict(list);c22bysha={}
  for r in caps[C22].rows():
   m=r["owner_member_id"];a0=r["support_ast"];need(m in comp and c25[m][0]=="C22B","C22/C15/C25");t=T("C22A",m,comp[m],r["row_sha256"],a0["coordinate_chart"],tuple(map(Q,a0["bounds"])),None);targets[t.chart].append(t);c22bysha[t.rowsha]=r
  for r in caps[C23].rows():
   m=r["owner_member_id"];a0=r["support_ast"];need(m in comp and c25[m][0]=="C23B","C23/C15/C25");t=T("C23A",m,comp[m],r["row_sha256"],a0["recharted_target_chart"],tuple(map(Q,a0["bounds"])),a0["physical_t_sign"]);targets[t.chart].append(t)
  need(sum(map(len,targets.values()))==305592,"target atom census");trees={k:tree(v)for k,v in targets.items()}
  g2a_pairs=[];g2b_pairs=[];routes=[];g2a_mult=Counter();src=Counter();c23_hits=0;den22=den23=0
  chart_graphs=Counter(graphs[x]["chart"]for x in ga);chart22=Counter();chart23=Counter()
  for ch,xs in targets.items():
   chart22[ch]=sum(x.src=="C22A"for x in xs);chart23[ch]=sum(x.src=="C23A"for x in xs)
  den22=sum(chart_graphs[c]*chart22[c]for c in chart_graphs);den23=sum(chart_graphs[c]*chart23[c]for c in chart_graphs)
  bygraph=defaultdict(list)
  for gid in sorted(ga):
   g=graphs[gid];a0=ga[gid];hits=[]
   for t in query(trees[g["chart"]],g["box"][2],g["box"][3]):
    z=inter(g["box"],t.box)if t.src=="C22A"else t2inter(g["box"],t.box,t.sign)
    if z is None:continue
    if t.src=="C23A":c23_hits+=1;continue
    pair=tuple(sorted((a0["member_id"],t.member)));row=closed({"schema":"cm2.c27-independent.g2a-relative2d.outer-candidate.row.v1","g2a_member_id":a0["member_id"],"target_member_id":t.member,"graph_id":gid,"graph_class":g["class"],"physical_chart":g["chart"],"g2a_component_id":a0["fresh_component_id"],"target_component_id":t.component,"components_equal":a0["fresh_component_id"]==t.component,"g2a_C10_row_sha256":g["rowsha"],"g2a_C14_authority_row_sha256":a0["semantic_theorem_ast"]["sealed_exact_support_authority"]["row_sha256"],"g2a_C24_row_sha256":a0["row_sha256"],"target_C22_row_sha256":t.rowsha,"outer_envelope_intersection_box":boxtext(z),"unordered_member_pair":list(pair),"formal_credit":0});g2a_pairs.append(row);hits.append(row);bygraph[gid].append(row)
   g2a_mult[len(hits)]+=1;route="SAME_CHART_RELATIVE_CELLS_PENDING_POSITIVE_SIDE_BINDING"if hits else"NO_CURRENT_C22A_C23A_RELATIVE_2D_CONTACT"
   routes.append(closed({"schema":"cm2.c27-independent.g2a-relative2d.route.row.v1","graph_id":gid,"graph_class":g["class"],"g2a_member_id":a0["member_id"],"g2a_component_id":a0["fresh_component_id"],"physical_chart":g["chart"],"C10_row_sha256":g["rowsha"],"C14_authority_role":a0["semantic_theorem_ast"]["sealed_exact_support_authority"]["role"],"C14_authority_row_sha256":a0["semantic_theorem_ast"]["sealed_exact_support_authority"]["row_sha256"],"C24_row_sha256":a0["row_sha256"],"C22_contact_candidate_count":len(hits),"C23_contact_candidate_count":0,"provisional_unique_route":route,"formal_credit":0}))
  for gid in sorted(sides):
   g=graphs[gid]
   for side in sides[gid]:
    env=ints(side["normalized_support_ast"]);pred=predicate(side["normalized_support_ast"])
    for t in query(trees[g["chart"]],env[2],env[3]):
     z=inter(env,t.box)if t.src=="C22A"else t2inter(env,t.box,t.sign)
     if z is None:continue
     need(t.src=="C22A","G2B/C23 envelope gap")
     pair=tuple(sorted((side["member_id"],t.member)));r=closed({"schema":"cm2.c27-independent.c24a-envelope-candidate.row.v2","left_member_id":pair[0],"right_member_id":pair[1],"c24_member_id":side["member_id"],"target_member_id":t.member,"c24_C15_component_id":side["fresh_component_id"],"target_C15_component_id":t.component,"c24_graph_id":gid,"c24_support_kind":side["semantic_theorem_ast"]["support_kind"],"c24_predicate_op":pred["op"],"c24_predicate_ast_sha256":dig(pred),"c24_row_sha256":side["row_sha256"],"target_atom_id":"C22A:"+t.rowsha,"target_source":"C22A","target_row_sha256":t.rowsha,"physical_chart":g["chart"],"intersection_coordinate_system":"(t,p,s)","exact_envelope_intersection_box":boxtext(z),"atom_envelope_witness_count":1,"current_C15_components_equal":side["fresh_component_id"]==t.component});g2b_pairs.append(r);src[side["semantic_theorem_ast"]["sealed_exact_support_authority"]["role"]]+=1
  need(len(g2a_pairs)==9408 and g2a_mult=={0:552,1:16,2:4696}and c23_hits==0,"G2A exact candidate census");need(len({tuple(r["unordered_member_pair"])for r in g2a_pairs})==9408,"G2A unique pairs");need(len(g2b_pairs)==18800 and len({(r["left_member_id"],r["right_member_id"])for r in g2b_pairs})==18800,"G2B candidate census")
  g2a_pairs.sort(key=lambda r:(r["g2a_member_id"],r["target_member_id"]));g2b_pairs.sort(key=lambda r:(r["c24_member_id"],r["target_member_id"]));routes.sort(key=lambda r:r["g2a_member_id"])
  d1=write(out/"G2A_5264_route_preclassification.jsonl.gz",routes);d2=write(out/"G2A_9408_same_chart_outer_candidates.jsonl.gz",g2a_pairs);d3=write(out/"G2B_18800_same_chart_outer_candidates.jsonl.gz",g2b_pairs)
  scan={"distinct_envelope_candidate_pair_count":18800,"ledger_file_sha256":d3["file_sha256"],"ledger_filename":d3["filename"],"historical_validation_set_opened":False}
  body={"schema":"cm2.c27-independent.g2a-relative2d-primitive-candidate-totality.v2","status":"BLOCKED_ZERO_CREDIT__PRIMITIVE_CANDIDATES_MATERIALIZED__EXACT_RELATION_AND_RELATIVE_2D_ROUTES_OPEN","invocation_seed":a.seed,"C27_FAMILIES_imported_or_read":False,"edge_ledger_used_as_candidate_universe":False,"historical_edge_or_validation_ledger_opened":False,"C24A_G2B_interval_envelope_scan":scan,"G2A":{"row_count":5264,"route_multiplicity":dict(g2a_mult),"C22_same_chart_full_pair_denominator":den22,"C22_outer_candidate_count":9408,"C23_same_chart_full_pair_denominator":den23,"C23_outer_candidate_count":0,"same_C15_outer_candidates":sum(r["components_equal"]for r in g2a_pairs),"cross_C15_outer_candidates":sum(not r["components_equal"]for r in g2a_pairs),"route_ledger":d1,"candidate_ledger":d2},"G2B_candidate_ledger":d3,"graph_class_census":dict(classes),"C26_G1_G2A_exact_cover":5264,"root_input_capture":{"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat":True,"attestations":{n:c.att()for n,c in sorted(caps.items())}},"formal_credit":0,"strict_nonpromotion":{"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};res=dict(body);res["semantic_projection_sha256"]=dig({k:v for k,v in body.items()if k not in{"invocation_seed","root_input_capture"}});res["result_sha256"]=dig(res);(out/"result.json").write_bytes(canon(res)+b"\n");print(canon({"status":res["status"],"result_sha256":res["result_sha256"],"semantic_projection_sha256":res["semantic_projection_sha256"]}).decode());return 0
 finally:
  for c in caps.values():c.close()
if __name__=="__main__":
 try:raise SystemExit(main())
 except(E,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));raise SystemExit(2)
