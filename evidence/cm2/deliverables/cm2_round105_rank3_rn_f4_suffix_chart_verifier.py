#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import cm2_round105_rank3_rn_f4_suffix_chart as c
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;M=H/"cm2-round105-rank3-rn-f4-suffix-chart-2026-07-22.json";P="94a2a93c10356032635c809ca65d520ec4ac9cbb295e787bd4f5791d48b42059"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 if sha(H/"cm2_round105_rank3_rn_f4_suffix_chart.py")!=P:raise RuntimeError("pin")
 f=json.loads(M.read_text());h=c.build(640)
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["F4_slot_rows"])!=f["result"]["F4_slot_rows_sha256"]:raise ValueError("digest")
 a=json.loads(json.dumps(f["result"]));b=json.loads(json.dumps(h["result"]));a.pop("precision_bits");b.pop("precision_bits")
 if a!=b:raise ValueError("higher")
 n=0
 for k,v in (("new_immutable_F4_slot_count",11),("complete_18_field_operator_block_count",1),("global_Gate5","CERTIFIED")):
  x=json.loads(json.dumps(a));x[k]=v
  if x!=b:n+=1
 r={"status":"PASS","independent_precision_bits":640,"hostile_semantic_mutations_rejected":f"{n}/3","producer_sha256":P,"manifest_sha256":sha(M)};return {"schema":"cm2.round105.rank3-rn-f4-suffix-chart-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
