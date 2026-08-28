#!/usr/bin/env python3
"""Classify all R275 regions against the frozen R279 atom support universe.

ZERO-CREDIT semantic probe: containment is an alias candidate, positive-volume
partial overlap requires exact refinement, and absence of positive-volume
overlap is a new-disjoint candidate.  Face contact never creates identity.
"""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent;PREFIX='cm2_round284_source_g_rechart_occurrence_overlap_contract_probe';LEDGER=HERE/f'{PREFIX}_ledger.json.gz';OUTPUT=HERE/f'{PREFIX}_result.json'
PINS={
'cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json':'e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386',
'cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz':'283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe',
'cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz':'8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b',
'cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json':'873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc'}
ENC=json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def canonical(x):return ENC.encode(x).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def fsha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def need(x,s):
 if not x:raise RuntimeError(s)
def relation(region,atom):
 inter=[(max(region[2*i],atom[2*i]),min(region[2*i+1],atom[2*i+1])) for i in range(3)];pos=[b>a for a,b in inter]
 if all(pos):
  if region==atom:return 'EXACT_EQUAL_BOX'
  rc=all(atom[2*i]<=region[2*i] and region[2*i+1]<=atom[2*i+1] for i in range(3))
  ac=all(region[2*i]<=atom[2*i] and atom[2*i+1]<=region[2*i+1] for i in range(3))
  return 'REGION_STRICTLY_CONTAINED_IN_ATOM' if rc else 'ATOM_STRICTLY_CONTAINED_IN_REGION' if ac else 'PARTIAL_POSITIVE_VOLUME_OVERLAP'
 if sum(pos)==2 and sum(b==a for a,b in inter)==1:return 'POSITIVE_AREA_COMMON_FACE_ONLY'
 return None
def gzbytes(x):
 b=io.BytesIO()
 with gzip.GzipFile(filename='',mode='wb',fileobj=b,mtime=0) as f:f.write(canonical(x))
 return b.getvalue()
def atomic(p,d):
 fd,t=tempfile.mkstemp(prefix='.'+p.name+'.',dir=p.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(d);f.flush();os.fsync(f.fileno())
  os.replace(t,p)
 finally:
  if os.path.exists(t):os.unlink(t)
def build():
 for n,h in PINS.items():need(fsha(HERE/n)==h,'pin:'+n)
 r=json.load(open(HERE/'cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json'))['result'];regions={x['reverse_rechart_region_row_id']:x for k in ['strict_region_ledger','arrangement_region_ledger'] for x in r[k]['rows']}
 with gzip.open(HERE/'cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz','rt') as f:atoms={x['canonical_atom_id']:x for x in json.load(f)['rows']}
 with gzip.open(HERE/'cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz','rt') as f:bindings=json.load(f)['rows']
 rows=[];hist=Counter();relhist=Counter();face_only=0
 for b in bindings:
  reg=regions[b['Round275_reverse_rechart_region_row_id']];rb=tuple(map(Q,reg['adjacent_rational_region_box']));rels=[]
  for aid in b['matching_atom_ids']:
   for bi,vals in enumerate(atoms[aid]['frozen_true_support_boxes']):
    k=relation(rb,tuple(map(Q,vals)))
    if k:rels.append({'canonical_atom_id':aid,'atom_support_box_index':bi,'relation':k});relhist[k]+=1
  kinds={x['relation'] for x in rels};need('EXACT_EQUAL_BOX' not in kinds and 'ATOM_STRICTLY_CONTAINED_IN_REGION' not in kinds,'unexpected identity direction')
  if 'PARTIAL_POSITIVE_VOLUME_OVERLAP' in kinds:state='PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED'
  elif 'REGION_STRICTLY_CONTAINED_IN_ATOM' in kinds:state='CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED'
  else:state='NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED'
  face= 'POSITIVE_AREA_COMMON_FACE_ONLY' in kinds;face_only+=face;hist[state]+=1
  row={'Round284_region_overlap_row_id':'round284-region-overlap:'+digest(b['Round275_reverse_rechart_region_row_id']),'Round275_region_id':b['Round275_reverse_rechart_region_row_id'],'source_chart':reg['source_chart'],'adjacent_chart':reg['adjacent_chart'],'parent_id':reg['parent_id'],'owner_target':reg['owner_target'],'complete_10_field_return_signature_sha256':reg['complete_10_field_return_signature_sha256'],'classification':state,'positive_area_face_contact_present':face,'relation_count':len(rels),'relations':sorted(rels,key=lambda x:(x['canonical_atom_id'],x['atom_support_box_index'],x['relation'])),'formal_occurrence_credit':0,'formal_component_credit':0,'formal_maximality_credit':0,'Jx_Jy_same_point_glue_credit':0};row['row_sha256']=digest(row);rows.append(row)
 rows=sorted(rows,key=lambda x:x['Round284_region_overlap_row_id']);need(len(rows)==13788 and hist=={'CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED':2476,'PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED':2184,'NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED':9128},'census')
 ledger={'schema':'cm2.round284.source-g-rechart-occurrence-overlap-contract.ledger.v1','row_count':len(rows),'rows':rows,'rows_sha256':digest(rows),'row_ids_sha256':digest([x['Round284_region_overlap_row_id'] for x in rows]),'row_hashes_sha256':digest([x['row_sha256'] for x in rows])}
 result={'schema':'cm2.round284.source-g-rechart-occurrence-overlap-contract-probe.v1','status':'PASS_ROUND284_RECHART_OCCURRENCE_OVERLAP_CONTRACT_PROBE__ZERO_CREDIT','pins':PINS,'census':{'Round275_region_count':len(rows),'classification_histogram':dict(sorted(hist.items())),'relation_histogram':dict(sorted(relhist.items())),'region_with_any_face_contact_count':face_only,'exact_equal_box_count':0,'atom_contained_in_region_count':0},'semantic_contract':{'contained_region_is_alias_candidate_not_new_occurrence':True,'partial_positive_volume_overlap_requires_exact_refinement':True,'face_contact_never_implies_occurrence_identity':True,'disjoint_region_is_only_a_new_occurrence_candidate_until_seam_and_frontier_closure':True},'strict_nonpromotion':{'occurrence_credit':0,'component_credit':0,'maximality_credit':0,'fibre_credit':0,'global_disposition_credit':0,'Jx_Jy_same_point_glue_credit':0,'quotient':63224,'expanded_occurrences':126468,'Gate5':'10/18','D02':'BLOCKED','CM2':'NO-GO_FOR_CLAIM'},'ledger':{'filename':LEDGER.name,'row_count':len(rows),'rows_sha256':ledger['rows_sha256']}}
 result['result_sha256']=digest(result);return ledger,result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ledger',type=Path,default=LEDGER);ap.add_argument('--output',type=Path,default=OUTPUT);ap.add_argument('--seed',default='284071');a=ap.parse_args();l,r=build();lb=gzbytes(l);r['ledger']['file_sha256']=hashlib.sha256(lb).hexdigest();r['result_sha256']=digest({k:v for k,v in r.items() if k!='result_sha256'});atomic(a.ledger,lb);atomic(a.output,canonical(r)+b'\n')
if __name__=='__main__':main()
