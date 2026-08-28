#!/usr/bin/env python3
"""Exact common refinement of the 2,184 Round284 partial-overlap regions.

ZERO CREDIT: cells are only relative alias/new candidates until occurrence IDs
and the seam/component frontier are formally frozen.
"""
from __future__ import annotations
import argparse,gzip,hashlib,io,json,os,tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent;PREFIX='cm2_round286_source_g_partial_overlap_exact_refinement_probe';LEDGER=HERE/f'{PREFIX}_ledger.json.gz';OUTPUT=HERE/f'{PREFIX}_result.json'
PINS={
'cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json':'e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386',
'cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz':'283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe',
'cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz':'8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b',
'cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json':'e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692',
'cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz':'39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92'}
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
def qstr(x):return str(x.numerator) if x.denominator==1 else str(x)
def volume(b):return (b[1]-b[0])*(b[3]-b[2])*(b[5]-b[4])
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
 with gzip.open(HERE/'cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz','rt') as f:bindings={x['Round275_reverse_rechart_region_row_id']:x for x in json.load(f)['rows']}
 with gzip.open(HERE/'cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz','rt') as f:r284=json.load(f)['rows']
 partial=[x for x in r284 if x['classification']=='PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED'];need(len(partial)==2184,'partial census')
 rows=[];cell_hist=Counter();region_hist=Counter();covered_volume=uncovered_volume=Q(0)
 for pr in partial:
  rid=pr['Round275_region_id'];reg=regions[rid];rb=tuple(map(Q,reg['adjacent_rational_region_box']));b=bindings[rid];clips=[]
  for aid in b['matching_atom_ids']:
   for bi,vals in enumerate(atoms[aid]['frozen_true_support_boxes']):
    ab=tuple(map(Q,vals));clip=tuple(y for i in range(3) for y in (max(rb[2*i],ab[2*i]),min(rb[2*i+1],ab[2*i+1])))
    if all(clip[2*i]<clip[2*i+1] for i in range(3)):clips.append((aid,bi,clip))
  need(clips and all(c[2]!=rb for c in clips),'proper partial clips')
  axes=[sorted({rb[2*i],rb[2*i+1],*(v for _a,_bi,c in clips for v in c[2*i:2*i+2])}) for i in range(3)];region_rows=[];local=Counter()
  for t0,t1 in zip(axes[0],axes[0][1:]):
   for p0,p1 in zip(axes[1],axes[1][1:]):
    for s0,s1 in zip(axes[2],axes[2][1:]):
     cell=(t0,t1,p0,p1,s0,s1);owners=sorted({aid for aid,_bi,c in clips if c[0]<=t0 and t1<=c[1] and c[2]<=p0 and p1<=c[3] and c[4]<=s0 and s1<=c[5]});need(len(owners)<=1,'multi atom occupancy')
     state='UNIQUE_ATOM_ALIAS_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED' if owners else 'NEW_DISJOINT_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED';v=volume(cell);local[state]+=1;cell_hist[state]+=1
     if owners:covered_volume+=v
     else:uncovered_volume+=v
     row={'Round286_refinement_cell_id':'round286-refinement-cell:'+digest([rid,[qstr(x) for x in cell]]),'Round275_region_id':rid,'source_chart':reg['source_chart'],'adjacent_chart':reg['adjacent_chart'],'parent_id':reg['parent_id'],'owner_target':reg['owner_target'],'complete_10_field_return_signature_sha256':reg['complete_10_field_return_signature_sha256'],'cell_exact_box':[qstr(x) for x in cell],'cell_coordinate_volume':qstr(v),'classification':state,'unique_alias_atom_id':owners[0] if owners else None,'atom_occupancy_count':len(owners),'formal_occurrence_credit':0,'formal_component_credit':0,'formal_maximality_credit':0,'Jx_Jy_same_point_glue_credit':0};row['row_sha256']=digest(row);region_rows.append(row)
  need(sum(Q(x['cell_coordinate_volume']) for x in region_rows)==volume(rb),'region volume cover');region_hist[(len(region_rows),local['UNIQUE_ATOM_ALIAS_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED'],local['NEW_DISJOINT_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED'])]+=1;rows.extend(region_rows)
 rows=sorted(rows,key=lambda x:x['Round286_refinement_cell_id']);need(len(rows)==7616 and cell_hist=={'UNIQUE_ATOM_ALIAS_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED':5700,'NEW_DISJOINT_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED':1916},'cell census')
 ledger={'schema':'cm2.round286.source-g-partial-overlap-exact-refinement.ledger.v1','row_count':len(rows),'rows':rows,'rows_sha256':digest(rows),'row_ids_sha256':digest([x['Round286_refinement_cell_id'] for x in rows]),'row_hashes_sha256':digest([x['row_sha256'] for x in rows])}
 result={'schema':'cm2.round286.source-g-partial-overlap-exact-refinement-probe.v1','status':'PASS_ROUND286_PARTIAL_OVERLAP_EXACT_REFINEMENT__ZERO_CREDIT','pins':PINS,'census':{'input_partial_region_count':2184,'output_refinement_cell_count':len(rows),'cell_classification_histogram':dict(sorted(cell_hist.items())),'region_partition_histogram':{'|'.join(map(str,k)):v for k,v in sorted(region_hist.items())},'region_with_uncovered_new_subcells_count':sum(v for (n,a,u),v in region_hist.items() if u>0),'region_fully_covered_by_multiple_unique_atom_subcells_count':sum(v for (n,a,u),v in region_hist.items() if u==0),'multi_atom_occupancy_cell_count':0,'covered_alias_coordinate_volume':qstr(covered_volume),'uncovered_new_coordinate_volume':qstr(uncovered_volume)},'semantic_contract':{'cells_are_pairwise_interior_disjoint_within_each_region':True,'each_cell_has_zero_or_one_atom_owner':True,'unique_atom_subcell_is_relative_alias_candidate':True,'uncovered_subcell_is_relative_new_candidate':True,'cells_of_one_connected_region_retain_internal_component_frontier':True},'strict_nonpromotion':{'occurrence_credit':0,'component_credit':0,'maximality_credit':0,'fibre_credit':0,'global_disposition_credit':0,'Jx_Jy_same_point_glue_credit':0,'quotient':63224,'expanded_occurrences':126468,'Gate5':'10/18','D02':'BLOCKED','CM2':'NO-GO_FOR_CLAIM'},'ledger':{'filename':LEDGER.name,'row_count':len(rows),'rows_sha256':ledger['rows_sha256']}};result['result_sha256']=digest(result);return ledger,result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ledger',type=Path,default=LEDGER);ap.add_argument('--output',type=Path,default=OUTPUT);ap.add_argument('--seed',default='286071');a=ap.parse_args();l,r=build();lb=gzbytes(l);r['ledger']['file_sha256']=hashlib.sha256(lb).hexdigest();r['result_sha256']=digest({k:v for k,v in r.items() if k!='result_sha256'});atomic(a.ledger,lb);atomic(a.output,canonical(r)+b'\n')
if __name__=='__main__':main()
