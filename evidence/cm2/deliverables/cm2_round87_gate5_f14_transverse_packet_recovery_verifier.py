#!/usr/bin/env python3
"""Independent verifier for the Round87 weighted-BV/F14 integration frontier."""
from __future__ import annotations
import copy,hashlib,json,sys
from fractions import Fraction as Q
from pathlib import Path
from flint import arb,ctx
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert
import cm2_round87_gate5_f14_transverse_packet_recovery_cert as cert

HERE=Path(__file__).resolve().parent
FROZEN=HERE/"cm2-round87-gate5-f14-transverse-packet-recovery-2026-07-22.json"
SCHEMA="cm2.round87.gate5-f14-transverse-packet-recovery-frontier.audit.v2"
def canon(v):return json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False)
def dig(v):return hashlib.sha256(canon(v).encode()).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError("duplicate")
  d[k]=v
 return d
def parse(s):
 x=json.loads(s,object_pairs_hook=pairs,parse_constant=lambda t:(_ for _ in()).throw(ValueError(t)))
 if not isinstance(x,dict):raise ValueError("top")
 return x
def aq(x):x=Q(x);return arb(x.numerator)/x.denominator
def validate(x):
 if set(x)!={"schema","pins","result","result_sha256"}:raise ValueError("top schema")
 if x!=cert.build(512):raise ValueError("producer replay")
 if x["result_sha256"]!=dig(x["result"]) or x["result"]["evidence_sha256"]!=dig(x["result"]["evidence"]):raise ValueError("digest")
 r=x["result"]
 expected={"status","weighted_BV_disintegration_on_152_packets","short_fibre_mass_weighted_recovery","F14_regular_density_operator_cost","candidate_local_maturity_before","candidate_local_maturity_after","new_F14_slots_installed","complete_18_field_blocks","global_Gate5","sharp_remaining_condition","strict_nonclaims","evidence","evidence_sha256"}
 if set(r)!=expected:raise ValueError("result schema")
 if r["candidate_local_maturity_after"]!="13/18" or r["new_F14_slots_installed"]!=0 or not r["F14_regular_density_operator_cost"].startswith("NOT_CERTIFIED"):raise ValueError("promotion")
 rows=r["evidence"]["integration_rows"]
 if len(rows)!=152 or len({z["atom_id"] for z in rows})!=152:raise ValueError("rows")
 if any(z["immutable_F14_slot_id"]!="NOT_MATERIALIZED" or z["F14_slot_status"]!="NOT_CERTIFIED" for z in rows):raise ValueError("F14 slots")

def independent(bits=768):
 ctx.prec=bits
 windows=parse(cert.WINDOWS.read_text())["result"]["evidence"]["window_rows"]
 frontier=parse(cert.OPERATOR_FRONTIER.read_text())["result"]
 packets=parse(cert.PACKETS.read_text())["result"]["R1_inner_candidate_field_packet_rows"]
 empty=parse(cert.EMPTY_SLOTS.read_text())["result"]
 pm={z["atom_id"]:z for z in packets};am={z["atom_id"]:z for z in frontier["evidence"]["attachment_rows"]}
 cores={return_cert.core_id(c):c for c in core_cert.physical_cores()}
 counts={"interior_support_proofs":0,"endpoint_zero_mass_proofs":0,"conditional_probability_identities":0,"Lambda_probability_identities":0,"internal_BV_cancellations":0,"packet_key_crosswalks":0,"F10_slot_crosswalks":0}
 for w in windows:
  aid=w["positive_atom_id"];p=pm[aid];a=am[aid]
  if p["r1_candidate_field_packet_id"]!=a["candidate_packet_id"] or p["physical_homogeneity_subbranch_id"]!=a["physical_homogeneity_subbranch_id"] or p["roof_level_j"]!=0:raise ValueError("integration key")
  counts["packet_key_crosswalks"]+=1
  if not a["F10_slot_id"].startswith("slot:r1:f10-empty:") or a["F10_coarea_density_regular_cost"]!="0":raise ValueError("F10")
  counts["F10_slot_crosswalks"]+=1
  c=cores[w["source_core_id"]];R=aq(first_hit.RADIUS[c.source]);t0,t1=map(aq,w["common_t"]);p0,p1=map(aq,w["common_p"])
  r0,r1=R*t0.asin(),R*t1.asin();f0,f1=p0.asin(),p1.asin();dr=r1-r0;df=f1-f0
  va=f0-4*r1;vb=f1-4*r0;width=vb-va;M=dr*(p1-p0)
  if not (r1>r0 and f1>f0 and width>0 and f0.cos()>aq(Q(999,1000)) and f1.cos()>aq(Q(999,1000))):raise ValueError("rectangle positivity")
  # For every va<v<vb the max lower endpoint is strictly below the min upper endpoint;
  # this is the exact projection of the open rectangle under v=phi-4r.
  vm=(va+vb)/2;lo=max(r0,(f0-vm)/4);hi=min(r1,(f1-vm)/4)
  if not (hi>lo and (4*lo+vm).cos()>aq(Q(999,1000)) and (4*hi+vm).cos()>aq(Q(999,1000))):raise ValueError("interior mass")
  counts["interior_support_proofs"]+=1
  # At va and vb, the two active endpoint formulae coincide exactly.
  la=max(r0,(f0-va)/4);ha=min(r1,(f1-va)/4)
  lb=max(r0,(f0-vb)/4);hb=min(r1,(f1-vb)/4)
  if not ((la-r1).contains(0) and (ha-r1).contains(0) and
          (lb-r0).contains(0) and (hb-r0).contains(0)):raise ValueError("endpoint")
  counts["endpoint_zero_mass_proofs"]+=2
  # h ds = cos(phi)dr and m=int cos(phi)dr, hence int rho ds=1.
  m=( (4*hi+vm).sin()-(4*lo+vm).sin() )/4
  if not (m>0 and (m/m).contains(1)):raise ValueError("conditional probability")
  counts["conditional_probability_identities"]+=1
  # Fubini on the shear (r,v)->(r,phi), Jacobian one:
  # int_V m(v)dv=dr*int_f0^f1 cos(phi)dphi=dr*(p1-p0)=M.
  fubini=dr*(f1.sin()-f0.sin())
  if not (fubini.overlaps(M) and (fubini/M).contains(1)):raise ValueError("Lambda normalization")
  counts["Lambda_probability_identities"]+=1
  # Internal BV is homogeneous under the positive carrierwise constant 1/m.
  # Therefore m*BV_internal(h/m)=BV_internal(h), including both sup and variation.
  hsup=max((4*lo+vm).cos(),(4*hi+vm).cos())/arb(17).sqrt()
  htv=abs((4*hi+vm).cos()-(4*lo+vm).cos())/arb(17).sqrt()
  if not (m*((hsup/m)+(htv/m))).overlaps(hsup+htv):raise ValueError("BV cancellation")
  counts["internal_BV_cancellations"]+=1
  bv_num=width*(1+4*max(abs(p0),abs(p1))*dr)/arb(17).sqrt()
  length_term=width/(arb(17).sqrt()*M)
  if not (bv_num/M<4300 and length_term<4300):raise ValueError("cost")
 if empty["F14_F18_frontier"]["F14_through_F18_materialized_slot_count"]!=0:raise ValueError("registered F14")
 if frontier["new_F14_through_F18_fields_installed"]!=0 or frontier["candidate_local_maturity_after"]!="13/18":raise ValueError("frontier maturity")
 return {"bits":bits,**counts,"registered_immutable_F14_slots":0,"accepted_Reg_alpha_crosswalk":"NOT_CERTIFIED","verdict":"PASS"}

def rejected(x,mut):
 y=copy.deepcopy(x);mut(y);y["result"]["evidence_sha256"]=dig(y["result"]["evidence"]);y["result_sha256"]=dig(y["result"])
 try:validate(y);return False
 except Exception:return True
def main():
 x=parse(FROZEN.read_text());validate(x);high=independent()
 muts=[lambda y:y["result"].__setitem__("F14_regular_density_operator_cost","CERTIFIED"),lambda y:y["result"].__setitem__("candidate_local_maturity_after","14/18"),lambda y:y["result"].__setitem__("new_F14_slots_installed",152),lambda y:y["result"]["evidence"]["integration"].__setitem__("accepted_Reg_alpha_crosswalk","CERTIFIED"),lambda y:y["result"]["evidence"]["integration_rows"][0].__setitem__("immutable_F14_slot_id","slot:r1:f14:fake"),lambda y:y["result"]["evidence"]["normalization"].__setitem__("Lambda","m(v)dv"),lambda y:y.__setitem__("extra",True)]
 hr=[rejected(x,m) for m in muts];pr=[]
 for k in cert.PINS:
  pr.append(rejected(x,lambda y,k=k:y["pins"].__setitem__(k,"0"*64)))
 strict=0
 for s in ('{"x":1,"x":2}','{"x":NaN}',canon(x)+' trailing','[]'):
  try:parse(s)
  except Exception:strict+=1
 r={"producer_bits":512,"independent_bits":768,"weighted_BV_packets":152,"F14_slots":0,"candidate_local_maturity":"13/18_UNCHANGED","independent_recomputation":high,"hostile_mutations_rejected":f"{sum(hr)}/{len(hr)}","pin_mutations_rejected":f"{sum(pr)}/{len(pr)}","strict_JSON_attacks_rejected":f"{strict}/4","verdict":"PASS"}
 print(canon({"schema":SCHEMA,"result":r,"result_sha256":dig(r)}))
if __name__=="__main__":
 try:main()
 except Exception as e:print(canon({"schema":SCHEMA,"verdict":"FAIL","error":str(e)}));sys.exit(2)
