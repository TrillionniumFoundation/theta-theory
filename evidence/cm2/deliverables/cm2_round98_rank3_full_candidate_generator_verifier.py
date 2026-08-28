#!/usr/bin/env python3
"""Independent 640-bit verification of the Round98 generator-consumption audit."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round98_rank3_full_candidate_generator_audit as cert
from cm2_round79_tangency_intersection_generator import digest
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round98-rank3-full-candidate-generator-audit-2026-07-22.json"
PRODUCER_SHA = "cb237fa18a72a9d586fbf7b1aecb5aff77168328e3c3df5db0c5cf162350c551"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(pairs):
 out={}
 for k,v in pairs:
  if k in out:raise ValueError("duplicate")
  out[k]=v
 return out
def bad(v):raise ValueError(v)
def summary(r):return (r["audited_probe_count"],r["round93_probe_count"],r["round94_transferred_probe_count"],r["corrected_physical_probe_count"],r["corrected_occluded_probe_count"],r["rays_with_any_corrected_occlusion"],r["rays_all_probes_corrected_physical"],r["minimum_consumed_prefix_count"],r["maximum_consumed_prefix_count"],tuple(sorted(r["earlier_candidate_histogram"].items())))
def verify(f,h):
 if set(f)!={"schema","result","result_sha256"} or f["schema"]!=cert.SCHEMA:raise ValueError("schema")
 if digest(f["result"])!=f["result_sha256"] or digest(f["result"]["probe_rows"])!=f["result"]["probe_rows_sha256"]:raise ValueError("digest")
 if summary(f["result"])!=summary(h["result"]):raise ValueError("higher")
 if summary(f["result"])[:9]!=(10112,8320,1792,1536,8576,57,8,15,57):raise ValueError("summary")
def build():
 if sha(HERE/"cm2_round98_rank3_full_candidate_generator_audit.py")!=PRODUCER_SHA:raise RuntimeError("pin")
 f=json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);rejected=0
 for field,value in (("corrected_occluded_probe_count",8575),("rays_with_any_corrected_occlusion",56),("minimum_consumed_prefix_count",14)):
  c=json.loads(json.dumps(f));c["result"][field]=value;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:rejected+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary_sha256":digest(summary(h["result"])),"hostile_semantic_mutations_rejected":f"{rejected}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA,"manifest_sha256":sha(MANIFEST)};return {"schema":"cm2.round98.rank3-full-candidate-generator.audit.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
