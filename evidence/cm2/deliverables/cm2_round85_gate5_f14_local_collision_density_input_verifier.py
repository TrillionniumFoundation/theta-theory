#!/usr/bin/env python3
import copy,json,math,sys
from fractions import Fraction as Q
from pathlib import Path
import cm2_round85_gate5_f14_local_collision_density_input_cert as cert
HERE=Path(__file__).resolve().parent;INPUT=HERE/"cm2-round85-gate5-f14-local-collision-density-input-2026-07-22.json"
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
def validate(x,e):
 if not isinstance(x,dict) or set(x)!={"schema","pins","result","result_sha256"}:raise ValueError("schema")
 if x["result_sha256"]!=cert.digest(x["result"]) or x["result"]["evidence_sha256"]!=cert.digest(x["result"]["evidence"]):raise ValueError("digest")
 if x!=e:raise ValueError("replay")
def reject(x,e):
 try:validate(x,e)
 except (ValueError,KeyError,TypeError,IndexError):return True
 return False
def main(argv):
 p=Path(argv[1]).resolve() if len(argv)>1 else INPUT;x=loads(p.read_text());e=cert.build(512);validate(x,e)
 h=cert.build(768)
 for k in ("formula_row_count","strict_denominator_rows","strict_two_half_slab_flight_owner_landing_replays","uniform_one_minus_t_squared_lower","uniform_q_a_lower","uniform_q_a_strict_upper","uniform_rho_upper","lambda_exact","J_exact"):
  if h["result"]["evidence"][k]!=x["result"]["evidence"][k]:raise ValueError("768 invariant")
 rows=x["result"]["evidence"]["formula_rows"]
 if len(rows)!=152 or len({r["atom_id"] for r in rows})!=152:raise ValueError("rows")
 if any(Q(r["one_minus_t_squared_lower"])<Q(51,100) or r["lambda_J_exact"]!="1" for r in rows):raise ValueError("bounds")
 muts=(lambda y:y["result"].__setitem__("F14_regular_density_operator_cost","CERTIFIED"),lambda y:y["result"].__setitem__("candidate_local_maturity","14/18"),
  lambda y:y["result"]["evidence"].__setitem__("uniform_rho_upper","1"),lambda y:y["result"]["evidence"]["formula_rows"][0].__setitem__("J","2"),lambda y:y.__setitem__("extra_claim",True))
 aa=[]
 for m in muts:
  y=copy.deepcopy(x);m(y);y["result"]["evidence_sha256"]=cert.digest(y["result"]["evidence"]);y["result_sha256"]=cert.digest(y["result"]);aa.append(reject(y,e))
 pp=[]
 for k in x["pins"]:
  y=copy.deepcopy(x);y["pins"][k]="0"*64;pp.append(reject(y,e))
 strict=0
 for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}','{"x":1e9999}'):
  try:loads(raw)
  except ValueError:strict+=1
 if not all(aa) or not all(pp) or strict!=4:raise ValueError("hostile")
 r={"producer_precision_bits":512,"independent_precision_bits":768,"formula_rows":152,"half_slab_physical_replays":304,"rho_upper":"20000","lambda_J":"1",
  "F14_input":"CERTIFIED","F14_operator_cost":"NOT_CERTIFIED","hostile_mutations_rejected":f"{sum(aa)}/{len(aa)}","pin_mutations_rejected":f"{sum(pp)}/{len(pp)}","strict_json":f"{strict}/4","verdict":"PASS"}
 out={"schema":"cm2.round85.gate5-f14-local-collision-density-input-audit.v1","result":r,"result_sha256":cert.digest(r)};json.dump(out,sys.stdout,sort_keys=True,indent=2);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main(sys.argv))
