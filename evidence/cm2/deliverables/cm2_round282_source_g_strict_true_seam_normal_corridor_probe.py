#!/usr/bin/env python3
"""Materialize strict-signature normal corridors for Round268 true seams.

This is deliberately ZERO-CREDIT: unresolved outgoing-chart-seam arrangement
tails remain fail-closed and no cross-chart DSU edge is emitted.
"""
from __future__ import annotations

import argparse, gzip, hashlib, io, json, os, tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round273_source_g_reverse_rechart_probe as r273
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274

HERE=Path(__file__).resolve().parent
PREFIX="cm2_round282_source_g_strict_true_seam_normal_corridor_probe"
LEDGER=HERE/f"{PREFIX}_ledger.json.gz"; OUTPUT=HERE/f"{PREFIX}_result.json"
SCHEMA="cm2.round282.source-g-strict-true-seam-normal-corridor-probe.v1"
PINS={
"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":"3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
"cm2_round273_source_g_reverse_rechart_probe.py":"40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c",
"cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py":"677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
"cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz":"074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814",
}
ENC=json.JSONEncoder(sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def canonical(x): return ENC.encode(x).encode()
def digest(x): return hashlib.sha256(canonical(x)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def need(x,label):
 if not x: raise RuntimeError(label)
def area(r):return (r[1]-r[0])*(r[3]-r[2])
def union_area(rs):
 if not rs:return Q(0)
 ps=sorted({v for r in rs for v in r[:2]});ss=sorted({v for r in rs for v in r[2:]});z=Q(0)
 for a,b in zip(ps,ps[1:]):
  for c,d in zip(ss,ss[1:]):
   if any(r[0]<=a and b<=r[1] and r[2]<=c and d<=r[3] for r in rs):z+=(b-a)*(d-c)
 return z
def qstr(x):return str(x.numerator) if x.denominator==1 else str(x)
def close(x):
 y=dict(x);y['row_sha256']=digest(y);return y
def gzip_bytes(x):
 b=io.BytesIO()
 with gzip.GzipFile(filename='',mode='wb',fileobj=b,mtime=0) as f:f.write(canonical(x))
 return b.getvalue()
def atomic(p,data):
 fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',dir=p.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)

def build():
 for n,h in PINS.items():need(fsha(HERE/n)==h,'pin:'+n)
 r275=json.load(open(HERE/'cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json'))['result']
 strict={x['reverse_rechart_region_row_id']:x for x in r275['strict_region_ledger']['rows']}
 arrangement={x['reverse_rechart_region_row_id']:x for x in r275['arrangement_region_ledger']['rows']}
 with gzip.open(HERE/'cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz','rt') as f:patches=json.load(f)['rows']
 tables=r174.registry_tables(r174.load_inputs()['gate5']); lo,hi=r273.sqrt_dyadic_bounds(Q(1,2),128)
 rows=[];side_hist=Counter();patch_hist=Counter();total_pass=total_fail=0
 for patch in patches:
  pr=tuple(map(Q,[*patch['exact_common_p_interval'],*patch['exact_common_s_interval']]))
  side_rows=[]
  for side in patch['side_channel_rows']:
   accepted=[];fail_reasons=Counter();arrangement_count=0
   for rid in side['candidate_Round275_region_ids']:
    if rid in arrangement:
     arrangement_count+=1;fail_reasons['EXPLICIT_OUTGOING_OR_WALL_ARRANGEMENT_REGION']+=1;continue
    z=strict[rid];b=list(map(Q,z['adjacent_rational_region_box']))
    footprint=(max(pr[0],b[2]),min(pr[1],b[3]),max(pr[2],b[4]),min(pr[3],b[5]))
    if area(footprint)<=0:continue
    cell=(r174.atlas.AtlasBox(b[0],hi,*footprint,0,'seam-corridor') if b[0]>=0
          else r174.atlas.AtlasBox(-hi,b[1],*footprint,0,'seam-corridor'))
    sig,reasons=r174.dynamic_signature(z['adjacent_chart'],cell,z['owner_target'],tables)
    if sig is None:
     fail_reasons.update('DYNAMIC_SIGNATURE:'+x for x in reasons);continue
    local=r274.signature_payload(sig,z['adjacent_chart'])
    need(local==z['local_return_signature'],'signature mismatch')
    accepted.append({
      'Round275_region_id':rid,'source_guard_row_id':z['source_guard_row_id'],
      'source_round':z['source_round'],'parent_id':z['parent_id'],'owner_target':z['owner_target'],
      'adjacent_chart':z['adjacent_chart'],'corridor_rational_outer_box':[qstr(cell.t0),qstr(cell.t1),qstr(cell.p0),qstr(cell.p1),qstr(cell.s0),qstr(cell.s1)],
      'seam_root_sign':'POSITIVE' if b[0]>=0 else 'NEGATIVE',
      'seam_algebraic_endpoint':'t=+sqrt(1/2)' if b[0]>=0 else 't=-sqrt(1/2)',
      'seam_dyadic_outer_endpoint':qstr(hi if b[0]>=0 else -hi),
      'positive_ps_footprint':[qstr(x) for x in footprint],'positive_ps_area':qstr(area(footprint)),
      'complete_10_field_return_signature_sha256':z['complete_10_field_return_signature_sha256'],
      'whole_outer_corridor_dynamic_signature_strict':True,
      'analytic_half_open_restriction_touches_true_seam':True,
    })
   covered=union_area([tuple(map(Q,x['positive_ps_footprint'])) for x in accepted])
   full=covered==area(pr);classification=('FULL_STRICT_NORMAL_CORRIDOR_COVER' if full else 'PARTIAL_STRICT_COVER__ARRANGEMENT_TAIL_FAIL_CLOSED')
   side_hist[classification]+=1;total_pass+=len(accepted);total_fail+=sum(fail_reasons.values())
   side_rows.append({'side':side['side'],'source_chart':side['source_chart'],'adjacent_chart':side['adjacent_chart'],'local_t_root':side['local_t_root'],
    'classification':classification,'patch_area':qstr(area(pr)),'strict_corridor_covered_area':qstr(covered),'unresolved_area':qstr(area(pr)-covered),
    'accepted_strict_corridor_count':len(accepted),'accepted_strict_corridors':accepted,
    'rejected_or_deferred_candidate_count':sum(fail_reasons.values()),'rejected_or_deferred_reason_histogram':dict(sorted(fail_reasons.items())),
    'arrangement_candidate_count':arrangement_count,'component_edge_credit':0})
  pclass='FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER' if all(x['classification'].startswith('FULL') for x in side_rows) else 'SEAM_PATCH_REMAINS_FAIL_CLOSED_FOR_ARRANGEMENT_TAIL'
  patch_hist[pclass]+=1
  rows.append(close({'Round282_seam_corridor_row_id':'round282-seam-corridor:'+digest(patch['Round268_true_seam_patch_row_id']),
   'Round268_true_seam_patch_row_id':patch['Round268_true_seam_patch_row_id'],'cyclic_transition_identity':patch['cyclic_transition_identity'],
   'exact_common_p_interval':patch['exact_common_p_interval'],'exact_common_s_interval':patch['exact_common_s_interval'],'exact_positive_common_area':patch['exact_positive_common_area'],
   'classification':pclass,'side_corridors':side_rows,'cross_chart_component_edge_credit':0,'maximality_credit':0,'Jx_Jy_same_point_glue_credit':0}))
 rows=sorted(rows,key=lambda x:x['Round282_seam_corridor_row_id'])
 need(len(rows)==152 and side_hist['FULL_STRICT_NORMAL_CORRIDOR_COVER']==264 and patch_hist['FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER']==128,'census')
 ledger={'schema':SCHEMA+'.ledger','rows':rows,'row_count':len(rows),'rows_sha256':digest(rows),'row_ids_sha256':digest([x['Round282_seam_corridor_row_id'] for x in rows]),'row_hashes_sha256':digest([x['row_sha256'] for x in rows])}
 result={'schema':SCHEMA,'status':'PASS_ROUND282_STRICT_TRUE_SEAM_NORMAL_CORRIDOR_COVER__24_PATCHES_FAIL_CLOSED__ZERO_CREDIT','pins':PINS,
  'census':{'input_patch_count':152,'directed_patch_side_count':304,'side_classification_histogram':dict(sorted(side_hist.items())),'patch_classification_histogram':dict(sorted(patch_hist.items())),'accepted_strict_corridor_candidate_count':total_pass,'rejected_or_deferred_candidate_count':total_fail,'fully_resolved_patch_count':128,'remaining_arrangement_tail_patch_count':24},
  'ledger':{'filename':LEDGER.name,'row_count':len(rows),'rows_sha256':ledger['rows_sha256']},
  'strict_nonpromotion':{'expanded_occurrence_credit':0,'component_edge_credit':0,'maximality_credit':0,'exact_key_fibre_credit':0,'global_disposition_credit':0,'Jx_Jy_same_point_glue_credit':0,'quotient':63224,'expanded_occurrences':126468,'Gate5':'10/18','D02':'BLOCKED','CM2':'NO-GO_FOR_CLAIM'},
  'next_gate':'Resolve the 24 outgoing-chart-seam arrangement tails by exact regular-graph side corridors, then pair both chart sides and only then emit the 152 true-seam DSU edges.'}
 result['result_sha256']=digest(result);return ledger,result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ledger',type=Path,default=LEDGER);ap.add_argument('--output',type=Path,default=OUTPUT);ap.add_argument('--seed',default='282071');a=ap.parse_args();l,r=build();lb=gzip_bytes(l);r['ledger']['file_sha256']=hashlib.sha256(lb).hexdigest();r['result_sha256']=digest({k:v for k,v in r.items() if k!='result_sha256'});atomic(a.ledger,lb);atomic(a.output,canonical(r)+b'\n')
if __name__=='__main__':main()
