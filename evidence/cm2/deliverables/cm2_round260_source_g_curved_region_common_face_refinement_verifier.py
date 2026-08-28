#!/usr/bin/env python3
"""Independent verifier for Round260 common-face refinement."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib, importlib, json, multiprocessing as mp, os
from pathlib import Path
import stat, sys, tempfile
from typing import Any
HERE=Path(__file__).resolve().parent
DEFAULT_CANDIDATE=HERE/'cm2_round260_source_g_curved_region_common_face_refinement_certificate.json'
OUTPUT=HERE/'cm2_round260_source_g_curved_region_common_face_refinement_verification.json'
SCHEMA='cm2.round260.source-g-curved-region-common-face-refinement.verification.v1'
CANDIDATE_SCHEMA='cm2.round260.source-g-curved-region-common-face-refinement.v1'
EXPECTED_CANDIDATE_SHA256='a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b'
PINS={
'cm2_round179_source_g_residual_tube_arrangement_rows.json':'f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42',
'cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json':'e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818',
'cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py':'6bcfbb794005e5a92590b7bb60ffceda34db3441ced143a15ceb23e15d5c035e',
'cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json':'4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938',
'cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py':'718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36',
'cm2_round259_source_g_curved_region_full_face_saturation_certificate.json':'799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039',
'cm2_round260_source_g_curved_region_common_face_refinement.py':'7edc6e5978e2c0570522d90314be2945187ffa279fa85f345c66fa126b60552f'}
G:dict[str,Any]={}
def need(v:bool,label:str)->None:
 if not v:raise RuntimeError(label)
def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(v:Any)->str:return hashlib.sha256(canonical(v)).hexdigest()
def text(v:Fraction)->str:return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def read_pinned(name:str)->bytes:
 p=HERE/name;i=p.lstat();need(stat.S_ISREG(i.st_mode) and not p.is_symlink() and 0<i.st_size<=500_000_000,f'regular:{name}');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[name],f'pin:{name}');return raw
def load_result(name:str)->dict[str,Any]:
 d=json.loads(read_pinned(name));need(set(d)=={'schema','result','result_sha256'} and digest(d['result'])==d['result_sha256'],f'envelope:{name}');return d['result']
def closed(row:dict[str,Any])->dict[str,Any]:
 out=dict(row);out['row_sha256']=digest(out);return out
def ledger(rows:list[dict[str,Any]],field:str)->dict[str,Any]:
 need(len(rows)==len({r[field] for r in rows}),f'unique:{field}');return {'row_count':len(rows),'rows_sha256':digest(rows),'row_ids_sha256':digest([r[field] for r in rows]),'row_hashes_sha256':digest([r['row_sha256'] for r in rows]),'every_row_closed_by_own_SHA256':True,'rows':rows}
class DSU:
 def __init__(self,values:list[str])->None:self.parent={v:v for v in values}
 def find(self,v:str)->str:
  if self.parent[v]!=v:self.parent[v]=self.find(self.parent[v])
  return self.parent[v]
 def union(self,a:str,b:str)->bool:
  a=self.find(a);b=self.find(b)
  if a==b:return False
  if a>b:a,b=b,a
  self.parent[b]=a;return True
def check_ledger(value:dict[str,Any],field:str)->None:
 rows=value['rows'];need(value['row_count']==len(rows) and len(rows)==len({r[field] for r in rows}) and value['rows_sha256']==digest(rows) and value['row_ids_sha256']==digest([r[field] for r in rows]) and value['row_hashes_sha256']==digest([r['row_sha256'] for r in rows]) and value['every_row_closed_by_own_SHA256'] is True,f'ledger:{field}')
 for row in rows:
  body=dict(row);actual=body.pop('row_sha256');need(actual==digest(body),f'row:{field}:{row[field]}')
def load_geometry()->None:
 read_pinned('cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py');read_pinned('cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py');read_pinned('cm2_round260_source_g_curved_region_common_face_refinement.py')
 need('cm2_round260_source_g_curved_region_common_face_refinement' not in sys.modules,'producer absent')
 if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))
 v208=importlib.import_module('cm2_round208_source_g_outgoing_direct_signature_materialization_verifier');v204=importlib.import_module('cm2_round204_source_g_wall_return_signature_local_replacement_verifier')
 _r195,r198,r174,_registry,_outgoing,collars208,_chain=v208.load_evaluator();formal=v204.load_formal_inputs();r179=formal['evaluator'].r179;r174_204=r179.r174;scope182=v204.extract_round182_scope(formal['attachment182']);scope179=v204.extract_round179_scope(formal['source179'],scope182['occurrence_ids'],scope182['origin_ids'])
 c204=load_result('cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json');c208=load_result('cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json');reg204={r['region_row_id']:r for r in c204['formal_local_open_3D_region_ledger']['rows']};reg208={r['region_row_id']:r for r in c208['formal_local_open_3D_signature_ledger']['rows']};boxes={rid:tuple(Fraction(x) for x in r['leaf_exact_box']) for rid,r in reg204.items()};boxes.update({rid:tuple(Fraction(x) for x in r['Round182_leaf_box']) for rid,r in reg208.items()})
 rows179=load_result('cm2_round179_source_g_residual_tube_arrangement_rows.json');cols=rows179['row_column_schemas']['resolved_3d_child_rows']
 for packed in rows179['resolved_3d_child_rows']:
  row=dict(zip(cols,packed));boxes[row['row_id']]=tuple(Fraction(x) for x in row['box'])
 need(len(boxes)==53968,'box census');G.update(r198=r198,r174=r174,collars208=collars208,r204=v204,r179=r179,r174_204=r174_204,scope182=scope182,scope179=scope179,reg204=reg204,reg208=reg208,boxes=boxes)
def eval208(oid:str,vals:list[Fraction],label:str)->bool:
 reg=G['reg208'][oid];p=G['r198'].selected_factor_profiles(G['collars208'][reg['occurrence_row_id']],G['r174'].atlas.AtlasBox(*vals,0,label));return p['HPLUS']['selected_sign']==reg['HPLUS_sign'] and p['HMINUS']['selected_sign']==reg['HMINUS_sign']
def eval204(oid:str,vals:list[Fraction],label:str)->bool:
 reg=G['reg204'][oid];collar=G['scope182']['collars'][reg['occurrence_row_id']];wall=G['scope179']['walls'][reg['occurrence_row_id']];r179=G['r179'];geo=r179.independent_geometry(collar['chart'],collar['owner_target'],G['r174_204'].atlas.AtlasBox(*vals,0,label));sn=G['r204'].CHART_CONTRACT[collar['chart']][2];tn='hit_x' if wall['axis']=='X' else 'hit_y';return r179.arb_sign(r179.subtract_wall(geo[sn],0)[0])=='STRICT_'+reg['source_sign'] and r179.arb_sign(r179.subtract_wall(geo[tn],wall['integer_wall'])[0])=='STRICT_'+reg['target_factor_sign']
def face_values(row:dict[str,Any])->list[Fraction]:
 ids=row['occurrence_row_ids'];axis=row['face_axis'];coord=Fraction(row['face_coordinate']);a=G['boxes'][ids[0]];b=G['boxes'][ids[1]];out=[]
 for k in range(3):out += [coord,coord] if k==axis else [max(a[2*k],b[2*k]),min(a[2*k+1],b[2*k+1])]
 return out
def cells(face:list[Fraction],axis:int,depth:int):
 trans=[k for k in range(3) if k!=axis];n=2**depth
 for i in range(n):
  for j in range(n):
   out=list(face)
   for k,index in zip(trans,(i,j)):
    lo=face[2*k];step=(face[2*k+1]-lo)/n;out[2*k]=lo+index*step;out[2*k+1]=lo+(index+1)*step
   yield (i,j),out
def classify(args:tuple[int,dict[str,Any]])->dict[str,Any]:
 idx,row=args;ids=row['occurrence_row_ids'];axis=row['face_axis'];coord=Fraction(row['face_coordinate']);face=face_values(row);is208=row['disposition']=='DEFER_R208_COMMON_FACE_REFINEMENT_REQUIRED';ev=eval208 if is208 else eval204;channel='ROUND208_FACTOR_COMMON_FACE' if is208 else 'ROUND204_TARGET_GRAPH_COMMON_FACE';chosen=None;face_depth=None;cell_index=None
 for depth in range(1,5):
  for index,cell in cells(face,axis,depth):
   if all(ev(oid,cell,f'round260-face:{idx}:{depth}:{index}:{oid}') for oid in ids):chosen=cell;face_depth=depth;cell_index=index;break
  if chosen is not None:break
 source_id=row['Round258_boundary_face_candidate_id']
 if chosen is None:return {'source_id':source_id,'status':'DEFER_NO_COMMON_STRICT_DYADIC_FACE_PATCH_AT_DEPTH_LE_4','channel':channel}
 corridors=[]
 for oid in ids:
  source=G['boxes'][oid];found=None
  for depth in range(1,25):
   box=list(chosen);span=source[2*axis+1]-source[2*axis];normal=span/(2**depth)
   if source[2*axis+1]==coord:box[2*axis:2*axis+2]=[coord-normal,coord];side='LOWER_SIDE_CORRIDOR'
   elif source[2*axis]==coord:box[2*axis:2*axis+2]=[coord,coord+normal];side='UPPER_SIDE_CORRIDOR'
   else:raise RuntimeError(f'incidence:{oid}')
   if ev(oid,box,f'round260-corridor:{idx}:{face_depth}:{cell_index}:{oid}:{depth}'):
    found={'occurrence_row_id':oid,'corridor_side':side,'dyadic_normal_depth':depth,'exact_normal_depth':text(normal),'exact_corridor_box':[text(x) for x in box]};break
  need(found is not None,f'normal depth 24:{source_id}:{oid}');corridors.append(found)
 return {'source_id':source_id,'status':'ACCEPT','channel':channel,'face_depth':face_depth,'cell_index':list(cell_index),'cell':[text(x) for x in chosen],'corridors':corridors}
def verify(candidate:dict[str,Any])->dict[str,Any]:
 for value,field in ((candidate['formal_accepted_common_face_patch_ledger'],'accepted_common_face_patch_row_id'),(candidate['formal_deferred_deeper_common_face_refinement_ledger'],'Round260_deferred_face_row_id'),(candidate['formal_Round259_to_Round260_component_map_ledger'],'Round259_to_Round260_component_map_row_id'),(candidate['formal_post_Round260_component_commitment_ledger'],'post_Round260_component_row_id'),(candidate['formal_post_Round260_occurrence_quotient_frontier_ledger'],'post_frontier_row_id'),(candidate['formal_post_Round260_key_quotient_frontier_ledger'],'post_Round260_key_frontier_row_id')):check_ledger(value,field)
 r259=load_result('cm2_round259_source_g_curved_region_full_face_saturation_certificate.json');load_geometry();sources=r259['formal_deferred_common_face_refinement_ledger']['rows']
 with mp.get_context('fork').Pool(processes=10) as pool:results=list(pool.imap(classify,enumerate(sources,1),chunksize=8))
 actual_accept={r['Round258_boundary_face_candidate_id']:r for r in candidate['formal_accepted_common_face_patch_ledger']['rows']};actual_defer={r['Round258_boundary_face_candidate_id']:r for r in candidate['formal_deferred_deeper_common_face_refinement_ledger']['rows']};source_by={r['Round258_boundary_face_candidate_id']:r for r in sources};map259={r['Round258_quotient_component_id']:r['post_Round259_quotient_component_id'] for r in r259['formal_Round258_to_Round259_component_map_ledger']['rows']};expected_accept=set();expected_defer=set();pairs=set();counts=Counter();face_depths=Counter();normal_depths=Counter();area=Fraction();volume=Fraction()
 for result in results:
  source=source_by[result['source_id']];counts[result['status']]+=1;counts[result['channel']+'_'+result['status']]+=1
  if result['status']=='ACCEPT':
   expected_accept.add(result['source_id']);row=actual_accept[result['source_id']];need(row['dyadic_face_refinement_depth']==result['face_depth'] and row['dyadic_face_cell_index']==result['cell_index'] and row['exact_common_face_patch_box']==result['cell'] and row['strict_two_sided_corridor_proofs']==result['corridors'],'canonical accepted proof')
   current=tuple(sorted(map259[x] for x in source['pre_Round259_component_ids']));need(row['pre_Round260_component_ids']==list(current),'accepted current pair')
   if current[0]!=current[1]:pairs.add(current)
   patch=Fraction(source['exact_common_face_area'])/(4**result['face_depth']);area+=patch;face_depths[(result['channel'],result['face_depth'])]+=1
   for c in result['corridors']:normal_depths[c['dyadic_normal_depth']]+=1;volume+=patch*Fraction(c['exact_normal_depth'])
  else:
   expected_defer.add(result['source_id']);need(actual_defer[result['source_id']]['disposition']==result['status'],'deferred disposition')
 need(set(actual_accept)==expected_accept and set(actual_defer)==expected_defer,'partition');need(len(expected_accept)==6728 and len(expected_defer)==5120 and counts['ROUND208_FACTOR_COMMON_FACE_ACCEPT']==6168 and counts['ROUND204_TARGET_GRAPH_COMMON_FACE_ACCEPT']==560,'classification census');need(digest(sorted(expected_accept))=='38264e05a81d55c5ebfed86211237ce20d4bb2bb571ed624c7fdffb26588114e','accepted commitment');need(area==Fraction(59341379,13107200000) and volume==Fraction(5893262088549,879609302220800000) and len(pairs)==3828,'measure/pair census')
 source_components=r259['formal_post_Round259_component_commitment_ledger']['rows'];keys={r['post_Round259_quotient_component_id']:(r['official_key_id'],r['official_key_ordinal']) for r in source_components};dsu=DSU(sorted(keys));rank=0
 for a,b in sorted(pairs):need(keys[a]==keys[b],'key purity');rank+=int(dsu.union(a,b))
 members=defaultdict(list)
 for cid in sorted(keys):members[dsu.find(cid)].append(cid)
 need(rank==3188 and len(members)==68876,'DSU census');post={};expected_members={}
 for values in members.values():
  pid=values[0] if len(values)==1 else 'round260-common-face-component:'+digest(values);expected_members[pid]=values
  for old in values:post[old]=pid
 actual_map={r['Round259_quotient_component_id']:r['post_Round260_quotient_component_id'] for r in candidate['formal_Round259_to_Round260_component_map_ledger']['rows']};need(actual_map==post,'component map');actual_members={r['post_Round260_quotient_component_id']:r['constituent_Round259_component_ids'] for r in candidate['formal_post_Round260_component_commitment_ledger']['rows']};need(actual_members==expected_members,'component commitments')
 for row in candidate['formal_post_Round260_occurrence_quotient_frontier_ledger']['rows']:need(row['post_Round260_quotient_component_id']==post[row['post_Round259_quotient_component_id']],'occurrence frontier')
 component_count=Counter(r['official_key_id'] for r in candidate['formal_post_Round260_component_commitment_ledger']['rows'])
 for row in candidate['formal_post_Round260_key_quotient_frontier_ledger']['rows']:need(row['post_Round260_quotient_component_count']==component_count[row['official_key_id']] and row['all_quotient_components_proved_maximal'] is False and row['global_exact_key_fibre_exhausted'] is False,'key frontier')
 census=candidate['census'];need(census['accepted_common_face_patch_count']==6728 and census['remaining_deeper_common_face_refinement_count']==5120 and census['rank_reducing_component_pair_count']==3188 and census['post_Round260_unified_quotient_component_count']==68876 and census['exact_accepted_patch_area_sum']=='59341379/13107200000' and census['exact_two_sided_corridor_volume_sum']=='5893262088549/879609302220800000','candidate census');need(candidate['strict_nonpromotion']['CM2']=='NO-GO_FOR_CLAIM' and candidate['strict_nonpromotion']['Gate5_filled_field_slot_count']==10,'nonpromotion')
 return {'status':'PASS_INDEPENDENT_ROUND260','independent_geometry_recomputed':True,'producer_imported_or_executed':False,'accepted_patch_count':6728,'remaining_fail_closed_face_count':5120,'rank_reduction_count':3188,'post_component_count':68876,'occurrence_frontier_count':53968,'exact_key_frontier_count':116,'CM2':'NO-GO_FOR_CLAIM'}
def safe_write(raw:bytes)->None:
 fd,name=tempfile.mkstemp(prefix=f'.{OUTPUT.name}.',dir=OUTPUT.parent);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as h:h.write(raw);h.flush();os.fsync(h.fileno())
  os.replace(p,OUTPUT)
 finally:
  if p.exists():p.unlink()
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument('candidate',nargs='?',type=Path,default=DEFAULT_CANDIDATE);parser.add_argument('--no-write',action='store_true');a=parser.parse_args();raw=a.candidate.read_bytes();need(hashlib.sha256(raw).hexdigest()==EXPECTED_CANDIDATE_SHA256,'candidate SHA256');doc=json.loads(raw);need(doc['schema']==CANDIDATE_SCHEMA and digest(doc['result'])==doc['result_sha256'],'candidate envelope');result=verify(doc['result']);out={'schema':SCHEMA,'result':result,'result_sha256':digest(result)};encoded=canonical(out)+b'\n'
 if not a.no_write:safe_write(encoded)
 print(result['status']);print(json.dumps(result,sort_keys=True));print(f"result_sha256={out['result_sha256']}");print(f'verification_sha256={hashlib.sha256(encoded).hexdigest()}');return 0
if __name__=='__main__':raise SystemExit(main())
