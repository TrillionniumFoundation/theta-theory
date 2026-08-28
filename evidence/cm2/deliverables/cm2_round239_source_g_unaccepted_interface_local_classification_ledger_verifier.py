#!/usr/bin/env python3
"""Independently verify the Round239 exhaustive local ledger."""
from __future__ import annotations
import argparse,hashlib,json,os,stat,tempfile
from collections import Counter
from pathlib import Path
from typing import Any
H=Path(__file__).resolve().parent;OUT=H/"cm2_round239_source_g_unaccepted_interface_local_classification_ledger_verification.json"
P={"cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":"88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73","cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json":"a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0","cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json":"cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41","cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217","cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json":"5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3","cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json":"8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446","cm2_round239_source_g_unaccepted_interface_local_classification_ledger.py":"8443017331bbb31ea5041112e3380525c12ad0e9e6b8f7e1a6b7cb03d8fb4bcb","cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json":"08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf"}
def need(x:bool,s:str)->None:
 if not x:raise RuntimeError(s)
def can(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def dg(x:Any)->str:return hashlib.sha256(can(x)).hexdigest()
def raw(n:str)->bytes:
 p=H/n;i=p.lstat();need(stat.S_ISREG(i.st_mode)and not p.is_symlink()and i.st_nlink==1,"regular:"+n);b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==P[n],"pin:"+n);return b
def load(n:str)->dict[str,Any]:
 d=json.loads(raw(n));need(set(d)=={"schema","result","result_sha256"}and dg(d["result"])==d["result_sha256"],"envelope:"+n);return d["result"]
def write(b:bytes)->None:
 f,n=tempfile.mkstemp(prefix=".r239v.",suffix=".tmp",dir=H);p=Path(n)
 try:
  with os.fdopen(f,"wb")as h:h.write(b);h.flush();os.fsync(h.fileno())
  os.replace(p,OUT)
 finally:
  if p.exists():p.unlink()
def verify()->dict[str,Any]:
 for n in P:raw(n)
 r230=load("cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json");r232=load("cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json");r233=load("cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json");r236=load("cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json");r237=load("cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json");r238=load("cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json");candidate=load("cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json");rows=[]
 def add(iid:str,kind:str,round_number:int,ordinals:list[int],ids:list[str])->None:rows.append({"classification_ledger_row_id":"round239:"+dg(iid),"Round220_split_interface_id":iid,"classification_type":kind,"source_round":round_number,"candidate_exact_key_ordinals":ordinals,"candidate_exact_key_ids":ids,"whole_origin_local_classification_credit":1,"known_block_incidence_credit":0})
 for r in r232["whole_origin_promotion_rows"]:s=r["local_return_signature"];add(r["Round220_split_interface_id"],"OUTGOING_SEAM_WHOLE_SIGNATURE",232,[s["official_key_ordinal"]],[s["official_key_id"]])
 for r in r233["parametric_graph_key_partition_rows"]:add(r["Round220_split_interface_id"],"OUTGOING_SEAM_GRAPH_SHARED_KEY",233,[r["shared_official_key_ordinal"]],[r["shared_official_key_id"]])
 for r in r236["whole_root_finite_key_partition_rows"]:add(r["Round220_split_interface_id"],"WALL_ENDPOINT_FINITE_KEY_PARTITION",236,r["candidate_exact_key_ordinals"],r["candidate_exact_key_ids"])
 for r in r237["whole_origin_promotion_rows"]:s=r["whole_origin_local_return_signature"];add(r["Round220_split_interface_id"],"WALL_CROSSING_TIME_WHOLE_SIGNATURE",237,[s["official_key_ordinal"]],[s["official_key_id"]])
 for r in r238["whole_origin_promotion_rows"]:s=r["whole_box_signature_recomputation_ignoring_chart_class_precheck"];add(r["Round220_split_interface_id"],"SOURCE_CHART_SEAM_WHOLE_SIGNATURE",238,[s["official_key_ordinal"]],[s["official_key_id"]])
 rows.sort(key=lambda r:r["classification_ledger_row_id"]);accepted={r["Round220_split_interface_id"]for r in r230["formal_certified_local_bulk_bridge_star_ledger"]["rows"]};ids={r["Round220_split_interface_id"]for r in rows};need(len(rows)==len(ids)==8512 and len(accepted)==448 and not(ids&accepted),"partition");need(candidate["classification_ledger_rows"]==rows and candidate["classification_ledger_rows_sha256"]==dg(rows),"rows");types=Counter(r["classification_type"]for r in rows);hist=Counter(len(r["candidate_exact_key_ids"])for r in rows);keys={x for r in rows for x in r["candidate_exact_key_ordinals"]};need(candidate["census"]["classification_type_histogram"]==dict(sorted(types.items()))and candidate["census"]["candidate_key_count_histogram"]=={str(k):v for k,v in sorted(hist.items())}and candidate["census"]["distinct_candidate_exact_key_count"]==len(keys)and candidate["census"]["combined_Round220_interface_count"]==8960,"census");need(candidate["strict_nonpromotion"]["CM2"]=="NO-GO_FOR_CLAIM","no-go");return{"status":"PASS_INDEPENDENT_ROUND239","candidate_sha256":P["cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json"],"candidate_result_sha256":dg(candidate),"producer_imported_or_executed":False,"independently_reconstructed_ledger_count":8512,"Round230_disjoint_accepted_count":448,"combined_interface_count":8960,"distinct_candidate_exact_key_count":len(keys),"strict_nonpromotion_reconfirmed":True}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--no-write",action="store_true");x=p.parse_args();r=verify();d={"schema":"cm2.round239.source-g-unaccepted-interface-local-classification-ledger.verification.v1","result":r,"result_sha256":dg(r)};b=can(d)+b"\n"
 if not x.no_write:write(b)
 print(r["status"]);print(json.dumps(r,sort_keys=True));print("verification_result_sha256="+d["result_sha256"]);return 0
if __name__=="__main__":raise SystemExit(main())
