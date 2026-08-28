#!/usr/bin/env python3
"""Run eight coherent attacks against the C13 independent verifier."""
from __future__ import annotations
import argparse,gzip,hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
from typing import Any,Callable
ROOT=Path(__file__).parent;PREFIX="cm2_round306c13_source_g_blocked_relation_empty_carrier_disposition";LEDGER=PREFIX+"_ledger.jsonl.gz";RESULT=PREFIX+"_result.json";VERIFIER=ROOT/(PREFIX+"_independent_verifier.py")
def canonical(x:Any)->bytes:return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def obj(x:Any)->str:return hashlib.sha256(canonical(x)).hexdigest()
def close_row(r:dict[str,Any])->None:r.pop("row_sha256",None);r["row_sha256"]=obj(r)
def close_result(r:dict[str,Any])->None:r.pop("result_sha256",None);r["result_sha256"]=obj(r)
def rewrite(d:Path,mutate:Callable[[list[dict[str,Any]]],None])->None:
 with gzip.open(d/LEDGER,"rt") as f:rows=[json.loads(x) for x in f]
 mutate(rows)
 for r in rows:close_row(r)
 plain=b"".join(canonical(r)+b"\n" for r in rows);wire=gzip.compress(plain,compresslevel=9,mtime=0);(d/LEDGER).write_bytes(wire);result=json.loads((d/RESULT).read_bytes());desc=result["disposition_ledger"];desc.update({"compressed_size":len(wire),"compressed_sha256":hashlib.sha256(wire).hexdigest(),"uncompressed_size":len(plain),"uncompressed_sha256":hashlib.sha256(plain).hexdigest(),"ordered_rows_sha256":obj(rows)});close_result(result);(d/RESULT).write_bytes(canonical(result))
def rmut(kind:str):
 def m(rows):
  r=rows[0]
  if kind=="empty":r["empty_carrier_certificate"]["strict_branch_intersection_with_carrier"]="NONEMPTY"
  elif kind=="carrier":r["empty_carrier_certificate"]["carrier_t_interval"][1]="999"
  elif kind=="geometry":r["empty_carrier_certificate"]["R248_null_positive_box_not_used_as_geometry"]=False
  elif kind=="physical":r["local_graph_side_physical_incidence_proved"]=True
  elif kind=="edge":r["DSU_edge_or_union_authorized"]=True
  elif kind=="credit":r["relation_nonincidence_disposition_credit"]=0
  elif kind=="ref":r["C11_blocked_ref"]=rows[1]["C11_blocked_ref"]
  else:raise AssertionError(kind)
 return m
def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir",required=True);a=ap.parse_args();src=Path(a.candidate_dir).resolve();attacks=[("denominator",None)]+[(x,rmut(x)) for x in ("empty","carrier","geometry","physical","edge","credit","ref")];out=[]
 for name,mut in attacks:
  with tempfile.TemporaryDirectory(prefix="c13-attack-") as t:
   d=Path(t);shutil.copy2(src/LEDGER,d/LEDGER);shutil.copy2(src/RESULT,d/RESULT)
   if name=="denominator":
    r=json.loads((d/RESULT).read_bytes());r["corrected_physical_relation_census"]["corrected_physical_denominator"]=15392;close_result(r);(d/RESULT).write_bytes(canonical(r))
   else:rewrite(d,mut)
   p=subprocess.run(["python","-I","-B",str(VERIFIER),"--candidate-dir",str(d)],stdout=subprocess.PIPE,stderr=subprocess.PIPE);rejected=p.returncode!=0;out.append({"attack":name,"rejected":rejected})
   if not rejected:raise RuntimeError("attack accepted:"+name)
 print(json.dumps({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","outcomes":out},sort_keys=True,separators=(",",":")));return 0
if __name__=="__main__":raise SystemExit(main())
