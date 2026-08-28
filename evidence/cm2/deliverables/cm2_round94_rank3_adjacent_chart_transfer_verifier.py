#!/usr/bin/env python3
"""Independent 640-bit audit of Round94 adjacent-chart transfers."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import cm2_round94_rank3_adjacent_chart_transfer_cert as cert
from cm2_round79_tangency_intersection_generator import digest
HERE=Path(__file__).resolve().parent
MANIFEST=HERE/"cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
PRODUCER_SHA="ecc5fae4bf35bb33408f10b8357b546d487be57329e2a798fc1ace95a3c0a24b"
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def hook(pairs):
 out={}
 for key,value in pairs:
  if key in out:raise ValueError("duplicate JSON key")
  out[key]=value
 return out
def bad(value):raise ValueError(f"nonfinite:{value}")
def summary(result):return (
 result["input_round93_chart_seam_count"],result["certified_unique_adjacent_chart_transfer_count"],
 result["algebraic_transferred_source_grazing_count"],result["second_chart_seam_count"],
 result["strict_transferred_physical_prefix_probe_total"],tuple(sorted(result["physical_terminal_event_histogram"].items())))
def signature(result):return sorted((row["exterior_port_id"],tuple(row["branch_key"]),row["projective_end"],row["old_source_chart"],row["adjacent_source_chart"],row["first_physical_terminal_event_type"],row["strict_transferred_physical_prefix_probe_count"]) for row in result["transfer_rows"])
def verify(frozen,higher):
 if set(frozen)!={"schema","result","result_sha256"}:raise ValueError("schema keys")
 if frozen["schema"]!=cert.SCHEMA or digest(frozen["result"])!=frozen["result_sha256"]:raise ValueError("schema/digest")
 if digest(frozen["result"]["transfer_rows"])!=frozen["result"]["transfer_rows_sha256"]:raise ValueError("rows digest")
 expected=(28,28,28,0,1792,(("ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION",3),("SOURCE_GRAZING",25)))
 if summary(frozen["result"])!=expected:raise ValueError("frozen summary")
 if summary(frozen["result"])!=summary(higher["result"]) or signature(frozen["result"])!=signature(higher["result"]):raise ValueError("higher precision")
def build():
 if sha(HERE/"cm2_round94_rank3_adjacent_chart_transfer_cert.py")!=PRODUCER_SHA:raise RuntimeError("producer pin")
 frozen=json.loads(MANIFEST.read_text(),object_pairs_hook=hook,parse_constant=bad);higher=cert.build(640);verify(frozen,higher)
 rejected=0
 for field,value in (("certified_unique_adjacent_chart_transfer_count",27),("second_chart_seam_count",1),("strict_transferred_physical_prefix_probe_total",1791)):
  changed=json.loads(json.dumps(frozen));changed["result"][field]=value;changed["result_sha256"]=digest(changed["result"])
  try:verify(changed,higher)
  except ValueError:rejected+=1
 result={"status":"PASS","independent_precision_bits":640,"higher_precision_summary":summary(higher["result"]),"hostile_semantic_mutations_rejected":f"{rejected}/3","strict_json_loader":"duplicate and nonfinite rejected","producer_sha256":PRODUCER_SHA,"manifest_sha256":sha(MANIFEST)}
 return {"schema":"cm2.round94.rank3-adjacent-chart-transfer.audit.v1","result":result,"result_sha256":digest(result)}
if __name__=="__main__":print(json.dumps(build(),sort_keys=True,indent=2))
