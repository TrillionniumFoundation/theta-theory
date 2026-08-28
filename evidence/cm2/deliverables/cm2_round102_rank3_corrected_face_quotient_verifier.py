#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round102_rank3_corrected_face_quotient as cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent;M=HERE/"cm2-round102-rank3-corrected-face-quotient-2026-07-22.json";P="c71f7aff942da5a6db5dee9140d333c964a9c4ff50480b6b0b58ca7b352815fa"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hook(pairs):
 o={}
 for k,v in pairs:
  if k in o:raise ValueError("duplicate")
  o[k]=v
 return o
def bad(v):raise ValueError(v)
def summary(r):return (r["corrected_rank3_physical_face_count"],r["corrected_face_registered_port_count"],r["corrected_face_interior_link_count"],r["registered_physical_arc_link_count"],r["immutable_certified_gap_link_count"],r["face_endpoint_count"],tuple(sorted(r["endpoint_type_histogram"].items())),tuple(sorted(r["face_endpoint_pair_histogram"].items())),r["unmatched_registered_port_count"],r["unmatched_face_endpoint_count"],r["remaining_geometric_residual_count"],r["face_rows_sha256"],r["interior_link_rows_sha256"],r["endpoint_incidence_rows_sha256"])
def verify(f,h):
 if f["schema"]!=cert.SCHEMA or digest(f["result"])!=f["result_sha256"]:raise ValueError("envelope")
 for rows,key in (("face_rows","face_rows_sha256"),("interior_link_rows","interior_link_rows_sha256"),("endpoint_incidence_rows","endpoint_incidence_rows_sha256")):
  if digest(f["result"][rows])!=f["result"][key]:raise ValueError(rows)
 if summary(f["result"])!=summary(h["result"]):raise ValueError("higher")
 if summary(f["result"])[:6]!=(12,120,108,52,56,24):raise ValueError("counts")
def build():
 if sha(HERE/"cm2_round102_rank3_corrected_face_quotient.py")!=P:raise RuntimeError("pin")
 f=json.loads(M.read_text(),object_pairs_hook=hook,parse_constant=bad);h=cert.build(640);verify(f,h);n=0
 for k,v in (("corrected_rank3_physical_face_count",11),("unmatched_face_endpoint_count",1),("remaining_geometric_residual_count",1)):
  c=json.loads(json.dumps(f));c["result"][k]=v;c["result_sha256"]=digest(c["result"])
  try:verify(c,h)
  except ValueError:n+=1
 r={"status":"PASS","independent_precision_bits":640,"higher_precision_summary_sha256":digest(summary(h["result"])),"hostile_semantic_mutations_rejected":f"{n}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":P,"manifest_sha256":sha(M)};return {"schema":"cm2.round102.rank3-corrected-face-quotient-verification.v1","result":r,"result_sha256":digest(r)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
