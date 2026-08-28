#!/usr/bin/env python3
"""Independent 640-bit verification of the Round101 eight-ray closure."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round101_rank3_eight_ray_source_grazing_closure as cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json"
PRODUCER_SHA256="2e42513fdc6674200a3a6b29f7fa4182c938bf9b8e30facf43085a790f1b8a1f"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(pairs):
 out={}
 for k,v in pairs:
  if k in out:raise ValueError("duplicate")
  out[k]=v
 return out
def bad(v):raise ValueError(v)
def summary(r):return (r["input_corrected_open_exterior_ray_count"],r["source_chart_segment_count"],r["adjacent_chart_segment_count"],r["immutable_candidate_certified_segment_count"],r["source_grazing_terminal_event_count"],r["remaining_open_exterior_ray_count"],r["ray_rows_sha256"],tuple(x["immutable_source_core_exit_chain_strip_count"] for x in r["ray_rows"]))
def verify(f,h):
 if set(f)!={"schema","result","result_sha256"} or f["schema"]!=cert.SCHEMA:raise ValueError("schema")
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["ray_rows"])!=f["result"]["ray_rows_sha256"]:raise ValueError("digest")
 if summary(f["result"])!=summary(h["result"]):raise ValueError("higher")
 if summary(f["result"])[:6]!=(8,1032,520,1552,8,0):raise ValueError("summary")
def build():
 if sha(HERE/"cm2_round101_rank3_eight_ray_source_grazing_closure.py")!=PRODUCER_SHA256:raise RuntimeError("pin")
 f=json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);rejected=0
 for field,value in (("source_grazing_terminal_event_count",7),("remaining_open_exterior_ray_count",1),("immutable_candidate_certified_segment_count",1551)):
  c=json.loads(json.dumps(f));c["result"][field]=value;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:rejected+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary_sha256":digest(summary(h["result"])),"hostile_semantic_mutations_rejected":f"{rejected}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA256,"manifest_sha256":sha(MANIFEST)}
 return {"schema":"cm2.round101.rank3-eight-ray-source-grazing-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
