#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import cm2_round103_rank3_rn_f1_f2_binding as cert
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;M=H/"cm2-round103-rank3-rn-f1-f2-binding-2026-07-22.json";P="eb47d42858d9b537793a79ac8b3d083c253e9e0015e52a1b77f4fa05485669af"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(x):
 d={}
 for k,v in x:
  if k in d:raise ValueError("duplicate")
  d[k]=v
 return d
def bad(v):raise ValueError(v)
def s(r):return (r["bound_rank3_return_word_count"],r["bound_physical_homogeneous_subbranch_count"],r["new_immutable_F1_slot_count"],r["new_immutable_F2_slot_count"],r["new_immutable_slot_count"],r["rank3_face_local_maturity"],r["complete_18_field_operator_block_count"],r["first_missing_rank3_field"],r["global_Gate5"],r["binding_rows_sha256"],r["immutable_slot_rows_sha256"])
def verify(f,h):
 if f["schema"]!=cert.SCHEMA or digest(f["result"])!=f["result_sha256"]:raise ValueError("envelope")
 if digest(f["result"]["binding_rows"])!=f["result"]["binding_rows_sha256"] or digest(f["result"]["immutable_slot_rows"])!=f["result"]["immutable_slot_rows_sha256"]:raise ValueError("rows")
 if s(f["result"])!=s(h["result"]):raise ValueError("higher")
def build():
 if sha(H/"cm2_round103_rank3_rn_f1_f2_binding.py")!=P:raise RuntimeError("pin")
 f=json.loads(M.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);n=0
 for k,v in (("new_immutable_slot_count",23),("complete_18_field_operator_block_count",1),("global_Gate5","CERTIFIED")):
  c=json.loads(json.dumps(f));c["result"][k]=v;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:n+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary_sha256":digest(s(h["result"])),"hostile_semantic_mutations_rejected":f"{n}/3","producer_sha256":P,"manifest_sha256":sha(M)};return {"schema":"cm2.round103.rank3-rn-f1-f2-binding-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
