#!/usr/bin/env python3
"""768-bit audit of the Round90 tracked residual-gap closure."""
import hashlib,json,sys
from pathlib import Path
from cm2_round79_tangency_intersection_generator import digest
import cm2_round90_rank3_tracked_residual_gap_closure_cert as cert
HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"cm2-round90-rank3-tracked-residual-gap-closure-2026-07-22.json"
PRODUCER_SHA="4f07377f59bb229592f683952868978372e5a46efc9ea9642c04cd340833e16f"
def hook(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError("duplicate JSON key")
  d[k]=v
 return d
def bad(x):raise ValueError("nonfinite JSON number")
def load():return json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def summary(r):return (r["input_round89_residual_gap_count"],r["direct_tracked_representative_gap_count"],r["D4_expanded_tracked_gap_closure_count"],r["remaining_unresolved_interior_projective_gap_count"],r["representative_strip_count"],r["D4_action_count"],r["combined_round89_round90_certified_interior_gap_count"],r["remaining_exterior_projective_ray_count"])
def verify(d,h):
 if set(d)!={"schema","result","result_sha256"} or d["schema"]!=cert.SCHEMA:raise ValueError("closed schema")
 if digest(d["result"])!=d["result_sha256"]:raise ValueError("digest")
 if summary(d["result"])!=(8,1,8,0,128,8,440,65):raise ValueError("frozen summary")
 if summary(d["result"])!=summary(h["result"]):raise ValueError("768-bit mismatch")
 if d["result"]["closure_rows"]!=h["result"]["closure_rows"]:raise ValueError("D4 closure rows")
 if d["result"]["D4_action_rows"]!=h["result"]["D4_action_rows"]:raise ValueError("D4 action rows")
 if d["result"]["source_cap_rows"]!=h["result"]["source_cap_rows"] or d["result"]["source_capped_projective_end_count"]!=47:raise ValueError("source cap rows")
def build():
 if sha(HERE/"cm2_round90_rank3_tracked_residual_gap_closure_cert.py")!=PRODUCER_SHA:raise RuntimeError("producer pin")
 frozen=load();higher=cert.build(768);verify(frozen,higher);rejected=0
 for field,value in (("D4_expanded_tracked_gap_closure_count",7),("remaining_unresolved_interior_projective_gap_count",1),("combined_round89_round90_certified_interior_gap_count",439),("remaining_exterior_projective_ray_count",0)):
  m=json.loads(json.dumps(frozen));m["result"][field]=value;m["result_sha256"]=digest(m["result"])
  try:verify(m,higher)
  except ValueError:rejected+=1
 if rejected!=4:raise RuntimeError("hostile mutation rejection")
 r={"status":"PASS","independent_precision_bits":768,"higher_precision_summary":summary(higher["result"]),"D4_action_rows_sha256":frozen["result"]["D4_action_rows_sha256"],"closure_rows_sha256":frozen["result"]["closure_rows_sha256"],"hostile_semantic_mutations_rejected":"4/4","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA,"manifest_sha256":sha(MANIFEST)}
 return {"schema":"cm2.round90.rank3-tracked-residual-gap-closure.audit.v1","result":r,"result_sha256":digest(r)}
def main():json.dump(build(),sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
