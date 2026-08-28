#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import gzip, hashlib, json
from pathlib import Path
import sys
from typing import Any

ROOT=Path(__file__).resolve().parent
PREFIX="cm2_round306c16a_source_g_identity_representation_family_replay"
MEMBERS=PREFIX+"_member_identity_family_ledger.jsonl.gz";REPS=PREFIX+"_representation_ledger.jsonl.gz";RESULT=PREFIX+"_result.json"
SOURCE={"C15_MEMBER":"cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz","C7_MEMBER":"cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz","C7_REP":"cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz","C14C_DISP":"cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_old_outer_envelope_family_disposition_ledger.jsonl.gz","C14C_ADM":"cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz"}
class Rejected(RuntimeError):pass
def need(v,label):
 if type(v)is not bool or not v:raise Rejected(label)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(v):return hashlib.sha256(canonical(v)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def rows(path):
 with gzip.open(path,"rb") as f:
  for ordinal,line in enumerate(f):
   need(line.endswith(b"\n"),"newline:"+path.name);raw=line[:-1];r=json.loads(raw);need(canonical(r)==raw,"canonical:"+path.name)
   body=dict(r);need(body.pop("row_sha256",None)==obj(body),"closure:"+path.name)
   yield ordinal,r,hashlib.sha256(raw).hexdigest()
def nxt(it):return next(it,None)
def verify(candidate):
 raw=(candidate/RESULT).read_bytes();result=json.loads(raw);need(canonical(result)==raw,"result canonical");body=dict(result);claimed=body.pop("result_sha256");need(claimed==obj(body),"result closure")
 need(result["status"]=="PASS_502204_MEMBER_549616_REPRESENTATION_FAMILY_REPLAY__RELATION_REPLAY_PENDING","status")
 need(result["strict_nonpromotion"]=={"B1A":0,"B2":0,"CM2":"NO-GO_FOR_CLAIM","maximality":0,"normalized_support":0,"relation_theorem_replay":0,"representation_pullback":0},"nonpromotion")
 need(result["member_census"]=={"total":502204,"old_C7":497772,"new_C14c":4432,"family_counts":{"G2A":5264,"G2B":10128,"NON_GRAPH":55604,"PRESERVED":126468,"R2":295336,"R292":9404}},"member result census")
 need(result["representation_census"]=={"total":549616,"family_counts":{"G2A":5264,"G2B":10128,"NON_GRAPH":55604,"PRESERVED":165744,"R2":302624,"R292":10252}},"representation result census")
 need(result["formal_credit"]=={"member_identity_family_replay":502204,"representation_identity_owner_family_replay":549616},"formal credit")
 for desc in result["ledgers"].values():q=candidate/desc["filename"];need(q.stat().st_size==desc["size"] and fsha(q)==desc["sha256"],"descriptor")
 disp={}
 for ordinal,r,wire in rows(ROOT/SOURCE["C14C_DISP"]):disp[r["old_outer_envelope_sheet_member_id"]]=[ordinal,r["row_id"],wire,r["row_sha256"]]
 admissions=[];new_reps=[]
 for ordinal,r,wire in rows(ROOT/SOURCE["C14C_ADM"]):
  ref=[ordinal,r["row_id"],wire,r["row_sha256"]];admissions.append((r["new_exact_sheet_member_id"],r,ref));new_reps.append((r["new_canonical_representation_id"],r,ref))
 admissions.sort();new_reps.sort();need(len(disp)==len(admissions)==4432,"C14c census")
 c7_members={}
 for so,sr,sw in rows(ROOT/SOURCE["C7_MEMBER"]):
  member=sr["member_id"];need(member not in c7_members,"C7 member unique");c7_members[member]=(so,sr["row_id"],sw,sr["row_sha256"],sr["coarse_family"])
 need(len(c7_members)==497772,"C7 member census")
 admission_by_member={member:(sr,ref) for member,sr,ref in admissions}
 candit=iter(rows(candidate/MEMBERS));family=Counter();meta={};old=0;new=0;previous=""
 for ordinal,c15,wire15 in rows(ROOT/SOURCE["C15_MEMBER"]):
  member=c15["registry_member_id"];need(member>previous,"C15 order");previous=member
  if member in c7_members:
   so,row_id,sw,row_sha,old_family=c7_members.pop(member);coarse="NON_GRAPH" if member in disp else old_family;source={"kind":"C7_REPLAY","ordinal":so,"row_id":row_id,"wire_sha256":sw,"row_sha256":row_sha};old+=1
  else:
   need(member in admission_by_member,"new member admission");sr,ref=admission_by_member.pop(member);coarse="G2A";source={"kind":"C14C_ADMISSION","ref":ref};new+=1
  co,cr,cw=next(candit);need(co==ordinal and cr["member_ordinal"]==ordinal and cr["member_id"]==member and cr["base_root_id"]==c15["base_root_id"] and cr["fresh_component_id"]==c15["fresh_component_id"] and cr["official_key_id"]==c15["official_key_id"] and cr["coarse_family"]==coarse and cr["identity_replay_source"]==source and cr["C14c_family_disposition_ref"]==disp.get(member),"member replay")
  need(cr["formal_credit"]=={"identity":1,"family":1,"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0},"member credit");family[coarse]+=1;meta[member]=(c15["base_root_id"],c15["fresh_component_id"],c15["official_key_id"],coarse)
 need(nxt(candit)is None and not c7_members and not admission_by_member and old==497772 and new==4432,"member exhaustion")
 need(family=={"PRESERVED":126468,"NON_GRAPH":55604,"R2":295336,"R292":9404,"G2A":5264,"G2B":10128},"member families")
 source_reps=[]
 for so,sr,sw in rows(ROOT/SOURCE["C7_REP"]):source_reps.append((sr["representation_id"],sr["owner_member_id"],"C7",[so,sr["row_id"],sw,sr["row_sha256"]]))
 for rep,sr,ref in new_reps:source_reps.append((rep,sr["new_exact_sheet_member_id"],"C14C",ref))
 source_reps.sort();need(len(source_reps)==549616,"source representation census")
 candit=iter(rows(candidate/REPS));rfamily=Counter();previous=""
 for ordinal in range(549616):
  expected,owner,kind,ref=source_reps[ordinal];need(expected>previous,"representation source order");previous=expected
  root,component,key,coarse=meta[owner];co,cr,cw=next(candit);need(co==ordinal and cr["representation_ordinal"]==ordinal and cr["representation_id"]==expected and cr["owner_member_id"]==owner and cr["base_root_id"]==root and cr["fresh_component_id"]==component and cr["official_key_id"]==key and cr["coarse_family"]==coarse and cr["replay_source_kind"]==kind and cr["source_row_ref"]==ref,"representation replay")
  need(cr["formal_credit"]=={"representation_identity":1,"representation_owner_binding":1,"family":1,"representation_pullback":0,"normalized_support":0,"B1A":0,"B2":0,"CM2":0},"representation credit");rfamily[coarse]+=1
 need(nxt(candit)is None,"representation exhaustion")
 need(rfamily=={"PRESERVED":165744,"NON_GRAPH":55604,"R2":302624,"R292":10252,"G2A":5264,"G2B":10128},"representation families")
 need(result["member_census"]["family_counts"]==dict(sorted(family.items())) and result["representation_census"]["family_counts"]==dict(sorted(rfamily.items())),"result census")
 return {"status":"PASS_INDEPENDENT_C16A_REPLAY_VERIFICATION","result_sha256":claimed,"members":502204,"representations":549616,"components":57876}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"python -I -B");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();candidate=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(json.dumps(verify(candidate),sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
