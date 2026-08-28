#!/usr/bin/env python3
"""Independent 640-bit audit of Round95 centered reverse coverage."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round95_rank3_centered_reverse_interval_cert as cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent;MANIFEST=HERE/"cm2-round95-rank3-centered-reverse-interval-2026-07-22.json";PRODUCER_SHA="c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(pairs):
 out={}
 for k,v in pairs:
  if k in out:raise ValueError("duplicate")
  out[k]=v
 return out
def bad(v):raise ValueError(v)
def summary(r):return (r["input_rank3_ray_count"],r["input_probe_gap_count"],r["fully_centered_interval_covered_ray_count"],r["remaining_unresolved_leaf_count"],sum(x["certified_leaf_count"] for x in r["ray_rows"]),max(x["maximum_split_depth"] for x in r["ray_rows"]))
def signature(r):return sorted((x["exterior_port_id"],tuple(x["branch_key"]),x["projective_end"],x["input_gap_count"],x["certified_leaf_count"],x["maximum_split_depth"],x["unresolved_leaf_count"]) for x in r["ray_rows"])
def verify(f,h):
 if set(f)!={"schema","result","result_sha256"} or f["schema"]!=cert.SCHEMA:raise ValueError("schema")
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["ray_rows"])!=f["result"]["ray_rows_sha256"]:raise ValueError("digest")
 if summary(f["result"])!=(65,10205,65,0,11759,105):raise ValueError("summary")
 if summary(f["result"])!=summary(h["result"]) or signature(f["result"])!=signature(h["result"]):raise ValueError("higher")
def build():
 if sha(HERE/"cm2_round95_rank3_centered_reverse_interval_cert.py")!=PRODUCER_SHA:raise RuntimeError("pin")
 f=json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);rejected=0
 for field,value in (("fully_centered_interval_covered_ray_count",64),("remaining_unresolved_leaf_count",1),("input_probe_gap_count",10204)):
  c=json.loads(json.dumps(f));c["result"][field]=value;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:rejected+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary":summary(h["result"]),"hostile_semantic_mutations_rejected":f"{rejected}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA,"manifest_sha256":sha(MANIFEST)};return {"schema":"cm2.round95.rank3-centered-reverse-interval.audit.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
