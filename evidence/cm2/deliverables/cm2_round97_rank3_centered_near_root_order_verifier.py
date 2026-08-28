#!/usr/bin/env python3
"""Independent audit of the Round97 centered near-root frontier."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round97_rank3_centered_near_root_order_cert as cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent;MANIFEST=HERE/"cm2-round97-rank3-centered-near-root-order-frontier-2026-07-22.json";PRODUCER_SHA="98fc3c1f0ac80c5f624fdd37a9dec4a19b0e90bdc38b8b3c18837452c6df9a36"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(pairs):
 out={}
 for k,v in pairs:
  if k in out:raise ValueError("duplicate")
  out[k]=v
 return out
def bad(v):raise ValueError(v)
def summary(r):return (r["input_round96_base_gap_count"],r["first_second_owner_base_gap_certified_count"],r["third_competitor_certified_leaf_count"],r["third_competitor_residual_leaf_count"],r["representation_boundary_residual_leaf_count"],r["fully_correlated_owner_covered_ray_count"])
def verify(f,h):
 if set(f)!={"schema","result","result_sha256"} or f["schema"]!=cert.SCHEMA:raise ValueError("schema")
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["ray_rows"])!=f["result"]["ray_rows_sha256"]:raise ValueError("digest")
 if summary(f["result"])!=(10205,10180,1552,8628,25,8) or summary(f["result"])!=summary(h["result"]):raise ValueError("summary")
def build():
 if sha(HERE/"cm2_round97_rank3_centered_near_root_order_cert.py")!=PRODUCER_SHA:raise RuntimeError("pin")
 f=json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);rejected=0
 for field,value in (("third_competitor_residual_leaf_count",8627),("third_competitor_certified_leaf_count",1553),("representation_boundary_residual_leaf_count",24)):
  c=json.loads(json.dumps(f));c["result"][field]=value;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:rejected+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary":summary(h["result"]),"hostile_semantic_mutations_rejected":f"{rejected}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA,"manifest_sha256":sha(MANIFEST)};return {"schema":"cm2.round97.rank3-centered-near-root-order.audit.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
