#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import cm2_round106_rank3_f5_adjacent_cell_scope_audit as c
from cm2_round79_tangency_intersection_generator import digest
H=Path(__file__).resolve().parent;M=H/"cm2-round106-rank3-f5-adjacent-cell-scope-audit-2026-07-22.json";P="e4318bf7bcf6b44671434df829b61a1dd1f457bdf08e859336e2b3422460d8da"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
 if sha(H/"cm2_round106_rank3_f5_adjacent_cell_scope_audit.py")!=P:raise RuntimeError("pin")
 f=json.loads(M.read_text());h=c.build()
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["audit_rows"])!=f["result"]["audit_rows_sha256"] or f!=h:raise ValueError("replay")
 n=0
 for k,v in (("materialized_adjacent_side_germ_count",24),("new_immutable_F5_slot_count",12),("global_Gate5","CERTIFIED")):
  x=json.loads(json.dumps(f));x["result"][k]=v;x["result_sha256"]=digest(x["result"])
  if x!=h:n+=1
 r={"status":"PASS","hostile_semantic_mutations_rejected":f"{n}/3","producer_sha256":P,"manifest_sha256":sha(M)};return {"schema":"cm2.round106.rank3-f5-adjacent-cell-scope-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
