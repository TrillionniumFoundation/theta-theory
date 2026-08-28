#!/usr/bin/env python3
import copy,json,math,sys
from pathlib import Path
import cm2_round85_gate5_f14_typed_standard_pair_frontier_cert as cert
HERE=Path(__file__).resolve().parent;INPUT=HERE/"cm2-round85-gate5-f14-typed-standard-pair-frontier-2026-07-22.json"
def uniq(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError("dup")
  d[k]=v
 return d
def loads(raw):
 x=json.loads(raw,object_pairs_hook=uniq,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
 def w(v):
  if isinstance(v,float) and not math.isfinite(v):raise ValueError("nonfinite")
  if isinstance(v,dict):
   for c in v.values():w(c)
  elif isinstance(v,list):
   for c in v:w(c)
 w(x);return x
def val(x,e):
 if not isinstance(x,dict) or set(x)!={"schema","pins","result","result_sha256"}:raise ValueError("schema")
 if x["result_sha256"]!=cert.dig(x["result"]) or x["result"]["evidence_sha256"]!=cert.dig(x["result"]["evidence"]):raise ValueError("digest")
 if x!=e:raise ValueError("replay")
def rej(x,e):
 try:val(x,e)
 except (ValueError,KeyError,TypeError,IndexError):return True
 return False
def main(a):
 p=Path(a[1]).resolve() if len(a)>1 else INPUT;x=loads(p.read_text());e=cert.build(512);val(x,e);h=cert.build(768)
 for k in ("cone_aligned_central_standard_pair_count","uniform_slope","uniform_endpoint_p_margin_strict_lower","uniform_density_bounds","local_BV_probability_norm_strict_upper"):
  if x["result"]["evidence"][k]!=h["result"]["evidence"][k]:raise ValueError("768")
 rows=x["result"]["evidence"]["standard_pair_rows"]
 if len(rows)!=152 or any(r["unstable_slope_dphi_dr"]!="4" or not r["p_strictly_monotone"] for r in rows):raise ValueError("rows")
 muts=(lambda y:y["result"].__setitem__("full_packet_F14_regular_density_operator_cost","CERTIFIED"),lambda y:y["result"].__setitem__("candidate_packet_maturity","14/18"),lambda y:y["result"]["evidence"]["full_rectangle_parallel_foliation"].__setitem__("infimum_nonempty_fibre_length","1"),lambda y:y["result"]["evidence"]["standard_pair_rows"][0].__setitem__("unstable_slope_dphi_dr","0"),lambda y:y.__setitem__("extra",True))
 aa=[]
 for m in muts:
  z=copy.deepcopy(x);m(z);z["result"]["evidence_sha256"]=cert.dig(z["result"]["evidence"]);z["result_sha256"]=cert.dig(z["result"]);aa.append(rej(z,e))
 pp=[]
 for k in x["pins"]:
  z=copy.deepcopy(x);z["pins"][k]="0"*64;pp.append(rej(z,e))
 strict=0
 for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}','{"x":1e9999}'):
  try:loads(raw)
  except ValueError:strict+=1
 if not all(aa) or not all(pp) or strict!=4:raise ValueError("hostile")
 r={"producer_bits":512,"independent_bits":768,"typed_central_standard_pairs":152,"central_BV_synthesis_cost_strict_upper":"16/15","full_packet_F14":"NOT_CERTIFIED","hostile":f"{sum(aa)}/{len(aa)}","pins":f"{sum(pp)}/{len(pp)}","strict_json":f"{strict}/4","verdict":"PASS"}
 out={"schema":"cm2.round85.gate5-f14-typed-standard-pair-frontier-audit.v1","result":r,"result_sha256":cert.dig(r)};json.dump(out,sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main(sys.argv))
