#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip, hashlib, json, os
from pathlib import Path
import sys
from typing import Any

ROOT=Path(__file__).resolve().parent
PREFIX="cm2_round306c16a_source_g_identity_representation_family_replay"
SCHEMA="cm2.round306c16a.source-g-identity-representation-family-replay.v1"
MEMBERS=PREFIX+"_member_identity_family_ledger.jsonl.gz"; REPS=PREFIX+"_representation_ledger.jsonl.gz"; RESULT=PREFIX+"_result.json"
PINS={
"C15_MEMBER":("cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",142025813,"e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
"C7_MEMBER":("cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz",269633111,"de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),
"C7_REP":("cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz",240400592,"1dc805b60f15ec8491b5200ccf9f04a239ce1532f6845a026045709feaaaa468"),
"C14C_DISP":("cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_old_outer_envelope_family_disposition_ledger.jsonl.gz",2697992,"96dee605bbec4024e8943b4d40c13ca5e86de411d92efa3ae48b075fb5d80817"),
"C14C_ADM":("cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz",2526805,"7f65ab28ad43a762d1e02bbd9d869965950b7b6d6db9cceef3fdd8cef12cc205"),
}
class Blocked(RuntimeError):pass
def need(v,label):
 if type(v)is not bool or not v: raise Blocked(label)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(v):return hashlib.sha256(canonical(v)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def source_rows(role):
 with gzip.open(ROOT/PINS[role][0],"rb") as f:
  for ordinal,line in enumerate(f):
   need(line.endswith(b"\n"),"newline:"+role);raw=line[:-1];r=json.loads(raw);need(canonical(r)==raw,"canonical:"+role)
   b=dict(r);need(b.pop("row_sha256",None)==obj(b),"closure:"+role)
   yield ordinal,r,hashlib.sha256(raw).hexdigest()
def close(body):return canonical({**body,"row_sha256":obj(body)})+b"\n"
class Writer:
 def __init__(self,directory,name):
  self.path=directory/name;need(not self.path.exists(),"no clobber");self.raw=self.path.open("xb");self.gz=gzip.GzipFile(fileobj=self.raw,mode="wb",compresslevel=9,mtime=0);self.h=hashlib.sha256();self.count=0
 def add(self,body):
  wire=close(body);self.gz.write(wire);self.h.update(wire);self.count+=1
 def finish(self):
  self.gz.close();self.raw.flush();os.fsync(self.raw.fileno());self.raw.close();return {"filename":self.path.name,"row_count":self.count,"sequence_sha256":self.h.hexdigest(),"size":self.path.stat().st_size,"sha256":fsha(self.path)}
def main()->int:
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B")
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir");p.add_argument("--publish",action="store_true");a=p.parse_args();need((a.candidate_dir is not None)!=a.publish,"mode")
 directory=ROOT if a.publish else Path(a.candidate_dir).resolve()
 if not a.publish:directory.mkdir(mode=0o700,parents=False,exist_ok=False)
 for role,(name,size,sha) in PINS.items():q=ROOT/name;need(q.stat().st_size==size and fsha(q)==sha,"pin:"+role)
 dispositions={}
 for ordinal,r,wire in source_rows("C14C_DISP"):
  member=r["old_outer_envelope_sheet_member_id"];need(member not in dispositions and r["old_family_before"]=="G2A" and r["old_family_after"]=="NON_GRAPH","disposition")
  dispositions[member]=[ordinal,r["row_id"],wire,r["row_sha256"]]
 admissions={};new_rep={}
 for ordinal,r,wire in source_rows("C14C_ADM"):
  member=r["new_exact_sheet_member_id"];rep=r["new_canonical_representation_id"]
  need(member not in admissions and rep not in new_rep,"admission unique")
  ref=[ordinal,r["row_id"],wire,r["row_sha256"]];admissions[member]=(r,ref);new_rep[rep]=(r,ref)
 need(len(dispositions)==len(admissions)==len(new_rep)==4432,"C14c counts")
 c7_members={}
 for source_ordinal,c7,wire7 in source_rows("C7_MEMBER"):
  member=c7["member_id"];need(member not in c7_members,"C7 member unique");c7_members[member]=(source_ordinal,c7,wire7)
 need(len(c7_members)==497772,"C7 member count")
 seen_old=0;seen_new=0;family=Counter();member_meta={}
 mw=Writer(directory,MEMBERS)
 for ordinal,c15,wire15 in source_rows("C15_MEMBER"):
  member=c15["registry_member_id"];source_kind=c15["admission_source"]
  if member in c7_members:
   source_ordinal,c7,wire7=c7_members.pop(member);coarse="NON_GRAPH" if member in dispositions else c7["coarse_family"]
   source_ref={"kind":"C7_REPLAY","ordinal":source_ordinal,"row_id":c7["row_id"],"wire_sha256":wire7,"row_sha256":c7["row_sha256"]};seen_old+=1
  else:
   need(member in admissions and source_kind=="C14C_NEW_EXACT_SHEET","new member join");adm,ref=admissions[member];coarse="G2A";source_ref={"kind":"C14C_ADMISSION","ref":ref};seen_new+=1
  disp_ref=dispositions.get(member);family[coarse]+=1;member_meta[member]=(c15["base_root_id"],c15["fresh_component_id"],c15["official_key_id"],coarse)
  body={"schema":SCHEMA+".member-row.v1","row_id":PREFIX+":member:"+obj(member),"member_ordinal":ordinal,"member_id":member,"base_root_id":c15["base_root_id"],"fresh_component_id":c15["fresh_component_id"],"official_key_id":c15["official_key_id"],"coarse_family":coarse,"identity_replay_source":source_ref,"C15_member_ref":[ordinal,c15["row_id"],wire15,c15["row_sha256"]],"C14c_family_disposition_ref":disp_ref,"formal_credit":{"identity":1,"family":1,"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0}}
  mw.add(body)
 need(not c7_members and seen_old==497772 and seen_new==4432,"member exhaustion")
 need(family=={"PRESERVED":126468,"NON_GRAPH":55604,"R2":295336,"R292":9404,"G2A":5264,"G2B":10128},"member family census")
 mdesc=mw.finish()
 old_reps=[]
 for ordinal,r,wire in source_rows("C7_REP"):old_reps.append((r["representation_id"],"C7",ordinal,r,wire))
 for rep,(r,ref) in new_rep.items():old_reps.append((rep,"C14C",ref[0],r,ref[2]))
 old_reps.sort(key=lambda x:x[0]);need(len(old_reps)==549616,"representation combined")
 rw=Writer(directory,REPS);rfamily=Counter();seen_ids=set()
 for ordinal,(rep,kind,source_ordinal,r,wire) in enumerate(old_reps):
  need(rep not in seen_ids,"representation duplicate");seen_ids.add(rep)
  if kind=="C7":owner=r["owner_member_id"];source_ref=[source_ordinal,r["row_id"],wire,r["row_sha256"]]
  else:owner=r["new_exact_sheet_member_id"];source_ref=[source_ordinal,r["row_id"],wire,r["row_sha256"]]
  root,component,key,coarse=member_meta[owner];rfamily[coarse]+=1
  body={"schema":SCHEMA+".representation-row.v1","row_id":PREFIX+":representation:"+obj(rep),"representation_ordinal":ordinal,"representation_id":rep,"owner_member_id":owner,"base_root_id":root,"fresh_component_id":component,"official_key_id":key,"coarse_family":coarse,"replay_source_kind":kind,"source_row_ref":source_ref,"formal_credit":{"representation_identity":1,"representation_owner_binding":1,"family":1,"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0}}
  rw.add(body)
 rdesc=rw.finish();need(rfamily=={"PRESERVED":165744,"NON_GRAPH":55604,"R2":302624,"R292":10252,"G2A":5264,"G2B":10128},"representation family census")
 body={"schema":SCHEMA,"status":"PASS_502204_MEMBER_549616_REPRESENTATION_FAMILY_REPLAY__RELATION_REPLAY_PENDING","source_pins":[{"role":k,"filename":v[0],"size":v[1],"sha256":v[2]} for k,v in PINS.items()],"member_census":{"total":502204,"old_C7":seen_old,"new_C14c":seen_new,"family_counts":dict(sorted(family.items()))},"representation_census":{"total":549616,"family_counts":dict(sorted(rfamily.items()))},"component_base":{"members":502204,"components":57876},"ledgers":{"members":mdesc,"representations":rdesc},"formal_credit":{"member_identity_family_replay":502204,"representation_identity_owner_family_replay":549616},"strict_nonpromotion":{"relation_theorem_replay":0,"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":"REPLAY_C9_C14_RELATION_AND_THEOREM_REFERENCES_ON_C15_COMPONENT_IDS"}
 result={**body,"result_sha256":obj(body)};data=canonical(result);q=directory/RESULT;need(not q.exists(),"no clobber result");q.write_bytes(data)
 print(json.dumps({"status":result["status"],"result_sha256":result["result_sha256"]},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
