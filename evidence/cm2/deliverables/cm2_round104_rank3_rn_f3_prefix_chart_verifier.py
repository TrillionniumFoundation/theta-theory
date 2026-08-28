#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import cm2_round104_rank3_rn_f3_prefix_chart as c
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;M=H/"cm2-round104-rank3-rn-f3-prefix-chart-2026-07-22.json";P="ee9416d62db65e9d5daa9d89b5bec31c29f7a002d406e0842b7b3db39a028c69"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 if sha(H/"cm2_round104_rank3_rn_f3_prefix_chart.py")!=P:raise RuntimeError("pin")
 f=json.loads(M.read_text());h=c.build(640)
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["F3_slot_rows"])!=f["result"]["F3_slot_rows_sha256"]:raise ValueError("digest")
 fr=json.loads(json.dumps(f["result"]));hr=json.loads(json.dumps(h["result"]));fr.pop("precision_bits");hr.pop("precision_bits")
 if fr!=hr:raise ValueError("replay")
 n=0
 for k,v in (("new_immutable_F3_slot_count",11),("complete_18_field_operator_block_count",1),("global_Gate5","CERTIFIED")):
  x=json.loads(json.dumps(f));x["result"][k]=v;x["result_sha256"]=digest(x["result"])
  xr=json.loads(json.dumps(x["result"]));xr.pop("precision_bits")
  if xr!=hr:n+=1
 r={"status":"PASS","independent_precision_bits":640,"hostile_semantic_mutations_rejected":f"{n}/3","producer_sha256":P,"manifest_sha256":sha(M)};return {"schema":"cm2.round104.rank3-rn-f3-prefix-chart-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
