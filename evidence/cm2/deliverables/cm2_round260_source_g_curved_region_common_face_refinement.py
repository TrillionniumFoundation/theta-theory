#!/usr/bin/env python3
"""Certify dyadic common-face patches for curved Source-G regions."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib, importlib, json, multiprocessing as mp, os
from pathlib import Path
import stat, sys, tempfile
from typing import Any
HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'cm2_round260_source_g_curved_region_common_face_refinement_certificate.json'
SCHEMA='cm2.round260.source-g-curved-region-common-face-refinement.v1'
PINS={
'cm2_round179_source_g_residual_tube_arrangement_rows.json':'f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42',
'cm2_round204_source_g_wall_return_signature_local_replacement.py':'7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77',
'cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json':'e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818',
'cm2_round208_source_g_outgoing_direct_signature_materialization.py':'c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913',
'cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json':'4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938',
'cm2_round259_source_g_curved_region_full_face_saturation_certificate.json':'799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039'}
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
def load_geometry()->None:
 read_pinned('cm2_round204_source_g_wall_return_signature_local_replacement.py');read_pinned('cm2_round208_source_g_outgoing_direct_signature_materialization.py')
 if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))
 r208=importlib.import_module('cm2_round208_source_g_outgoing_direct_signature_materialization');r204=importlib.import_module('cm2_round204_source_g_wall_return_signature_local_replacement')
 r207,_=r208.load_evaluator();r198=r207.r203.r198;r195=r198.r195;r174=r195.r191.r189.r188.r186.r179.r174;_,collars208,_=r195.r191.r189.load_scope()
 formal=r204.load_formal_inputs();r179=formal['evaluator'].r179;r174_204=r179.r174;scope182=r204.extract_round182_scope(formal['attachment182']);scope179=r204.extract_round179_scope(formal['source179'],scope182['occurrence_ids'],scope182['origin_ids'])
 c204=load_result('cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json');c208=load_result('cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json')
 reg204={r['region_row_id']:r for r in c204['formal_local_open_3D_region_ledger']['rows']};reg208={r['region_row_id']:r for r in c208['formal_local_open_3D_signature_ledger']['rows']};boxes={rid:tuple(Fraction(x) for x in r['leaf_exact_box']) for rid,r in reg204.items()};boxes.update({rid:tuple(Fraction(x) for x in r['Round182_leaf_box']) for rid,r in reg208.items()})
 rows179=load_result('cm2_round179_source_g_residual_tube_arrangement_rows.json');cols=rows179['row_column_schemas']['resolved_3d_child_rows']
 for packed in rows179['resolved_3d_child_rows']:
  row=dict(zip(cols,packed));boxes[row['row_id']]=tuple(Fraction(x) for x in row['box'])
 need(len(boxes)==53_968,'box census');G.update(r198=r198,r174=r174,collars208=collars208,r204=r204,r179=r179,r174_204=r174_204,scope182=scope182,scope179=scope179,reg204=reg204,reg208=reg208,boxes=boxes)
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
def build()->dict[str,Any]:
 r259=load_result('cm2_round259_source_g_curved_region_full_face_saturation_certificate.json');need(r259['census']['remaining_common_face_refinement_count']==11_848 and r259['census']['post_Round259_unified_quotient_component_count']==72_064,'Round259 baseline');load_geometry();source_rows=r259['formal_deferred_common_face_refinement_ledger']['rows'];need(len(source_rows)==11_848,'source rows')
 with mp.get_context('fork').Pool(processes=10) as pool:results=list(pool.imap(classify,enumerate(source_rows,1),chunksize=8))
 by_id={r['Round258_boundary_face_candidate_id']:r for r in source_rows};map259={r['Round258_quotient_component_id']:r['post_Round259_quotient_component_id'] for r in r259['formal_Round258_to_Round259_component_map_ledger']['rows']};accepted=[];deferred=[];pairs=set();counts=Counter();face_depths=Counter();normal_depths=Counter();area_sum=Fraction();volume_sum=Fraction()
 for result in results:
  source=by_id[result['source_id']];counts[result['status']]+=1;counts[result['channel']+'_'+result['status']]+=1
  if result['status']=='ACCEPT':
   current=tuple(sorted(map259[x] for x in source['pre_Round259_component_ids']));
   if current[0]!=current[1]:pairs.add(current)
   patch_area=Fraction(source['exact_common_face_area'])/(4**result['face_depth']);area_sum+=patch_area;face_depths[(result['channel'],result['face_depth'])]+=1
   for c in result['corridors']:normal_depths[c['dyadic_normal_depth']]+=1;volume_sum+=patch_area*Fraction(c['exact_normal_depth'])
   accepted.append(closed({'accepted_common_face_patch_row_id':'round260-accepted-common-face:'+digest([result['source_id']]),'Round258_boundary_face_candidate_id':result['source_id'],'official_key_id':source['official_key_id'],'source_chart':source['source_chart'],'identity_chart_transition':True,'face_axis':source['face_axis'],'face_coordinate':source['face_coordinate'],'occurrence_row_ids':source['occurrence_row_ids'],'pre_Round260_component_ids':list(current),'geometry_channel':result['channel'],'parent_exact_common_face_area':source['exact_common_face_area'],'dyadic_face_refinement_depth':result['face_depth'],'dyadic_face_cell_index':result['cell_index'],'exact_common_face_patch_box':result['cell'],'exact_common_face_patch_area':text(patch_area),'strict_two_sided_corridor_proofs':result['corridors'],'disposition':'ACCEPT_STRICT_DYADIC_COMMON_FACE_PATCH_WITH_TWO_SIDED_CORRIDOR','physical_glue_credit':1,'maximality_credit':0}))
  else:deferred.append(closed({'Round260_deferred_face_row_id':'round260-deferred-face:'+digest([result['source_id']]),'Round258_boundary_face_candidate_id':result['source_id'],'official_key_id':source['official_key_id'],'source_chart':source['source_chart'],'face_axis':source['face_axis'],'face_coordinate':source['face_coordinate'],'occurrence_row_ids':source['occurrence_row_ids'],'pre_Round260_component_ids':sorted(map259[x] for x in source['pre_Round259_component_ids']),'geometry_channel':result['channel'],'parent_exact_common_face_area':source['exact_common_face_area'],'tested_dyadic_face_depths':[1,2,3,4],'depth_4_cell_count':256,'disposition':result['status'],'physical_glue_credit':0,'maximality_credit':0}))
 accepted.sort(key=lambda r:r['accepted_common_face_patch_row_id']);deferred.sort(key=lambda r:r['Round260_deferred_face_row_id'])
 need(counts==Counter({'ACCEPT':6728,'ROUND208_FACTOR_COMMON_FACE_ACCEPT':6168,'DEFER_NO_COMMON_STRICT_DYADIC_FACE_PATCH_AT_DEPTH_LE_4':5120,'ROUND208_FACTOR_COMMON_FACE_DEFER_NO_COMMON_STRICT_DYADIC_FACE_PATCH_AT_DEPTH_LE_4':4616,'ROUND204_TARGET_GRAPH_COMMON_FACE_ACCEPT':560,'ROUND204_TARGET_GRAPH_COMMON_FACE_DEFER_NO_COMMON_STRICT_DYADIC_FACE_PATCH_AT_DEPTH_LE_4':504}),'classification census');need(digest(sorted(r['Round258_boundary_face_candidate_id'] for r in accepted))=='38264e05a81d55c5ebfed86211237ce20d4bb2bb571ed624c7fdffb26588114e','accepted commitment');need(area_sum==Fraction(59_341_379,13_107_200_000) and volume_sum==Fraction(5_893_262_088_549,879_609_302_220_800_000),'exact measures');need(len(pairs)==3828,'pair census')
 source_components=r259['formal_post_Round259_component_commitment_ledger']['rows'];keys={r['post_Round259_quotient_component_id']:(r['official_key_id'],r['official_key_ordinal']) for r in source_components};dsu=DSU(sorted(keys));rank=0
 for a,b in sorted(pairs):need(keys[a]==keys[b],f'key pair:{a}:{b}');rank+=int(dsu.union(a,b))
 need(rank==3188,'rank');members=defaultdict(list)
 for cid in sorted(keys):members[dsu.find(cid)].append(cid)
 need(len(members)==68876,'post components');post_by_old={};component_rows=[]
 for values in sorted(members.values(),key=lambda x:x[0]):
  ks={keys[x] for x in values};need(len(ks)==1,'key purity');key_id,ordinal=next(iter(ks));post=values[0] if len(values)==1 else 'round260-common-face-component:'+digest(values)
  for old in values:post_by_old[old]=post
  component_rows.append(closed({'post_Round260_component_row_id':'round260-component-row:'+digest([post]),'post_Round260_quotient_component_id':post,'official_key_id':key_id,'official_key_ordinal':ordinal,'constituent_Round259_component_count':len(values),'constituent_Round259_component_ids':values,'constituent_Round259_component_ids_sha256':digest(values),'common_face_patch_edge_count':sum(1 for pair in pairs if pair[0] in values and pair[1] in values),'certified_known_connectivity_only':True,'maximal_physical_component_claimed':False}))
 component_rows.sort(key=lambda r:r['post_Round260_quotient_component_id']);map_rows=[closed({'Round259_to_Round260_component_map_row_id':'round260-component-map:'+digest([old]),'Round259_quotient_component_id':old,'post_Round260_quotient_component_id':post_by_old[old],'component_rank_reduction_credit':int(old!=post_by_old[old])}) for old in sorted(keys)]
 frontier=[]
 for row in r259['formal_post_Round259_occurrence_quotient_frontier_ledger']['rows']:
  out=dict(row);out.pop('row_sha256');old=row['post_Round259_quotient_component_id'];out['post_Round260_quotient_component_id']=post_by_old[old];out['Round260_common_face_patch_attachment_credit']=int(old!=post_by_old[old]);frontier.append(closed(out))
 frontier.sort(key=lambda r:r['post_frontier_row_id']);component_count=Counter(r['official_key_id'] for r in component_rows);accepted_key=Counter(r['official_key_id'] for r in accepted);deferred_key=Counter(r['official_key_id'] for r in deferred);key_rows=[]
 for source in r259['formal_post_Round259_key_quotient_frontier_ledger']['rows']:
  kid=source['official_key_id'];key_rows.append(closed({'post_Round260_key_frontier_row_id':'round260-key-frontier:'+digest([kid]),'official_key_id':kid,'official_key_ordinal':source['official_key_ordinal'],'local_occurrence_count':source['local_occurrence_count'],'post_Round260_quotient_component_count':component_count[kid],'accepted_common_face_patch_count':accepted_key[kid],'deferred_deeper_common_face_count':deferred_key[kid],'occurrence_quotient_assignment_complete':True,'all_quotient_components_proved_maximal':False,'global_exact_key_fibre_exhausted':False,'maximal_physical_component_credit':0,'global_exact_key_fibre_credit':0}))
 key_rows.sort(key=lambda r:r['official_key_ordinal']);need(len(frontier)==53968 and len(key_rows)==116,'frontiers')
 census={'Round259_common_face_refinement_candidate_count':11848,'accepted_common_face_patch_count':6728,'accepted_Round208_common_face_patch_count':6168,'accepted_Round204_common_face_patch_count':560,'remaining_deeper_common_face_refinement_count':5120,'remaining_Round208_deeper_refinement_count':4616,'remaining_Round204_deeper_refinement_count':504,'face_refinement_depth_histogram':{f'{channel}:{depth}':count for (channel,depth),count in sorted(face_depths.items())},'normal_corridor_depth_histogram':{str(k):normal_depths[k] for k in sorted(normal_depths)},'accepted_distinct_current_component_pair_count':3828,'rank_reducing_component_pair_count':3188,'redundant_certified_component_pair_count':640,'post_Round259_unified_quotient_component_count':72064,'post_Round260_unified_quotient_component_count':68876,'exact_accepted_patch_area_sum':text(area_sum),'exact_two_sided_corridor_volume_sum':text(volume_sum),'accepted_Round258_candidate_ids_sha256':'38264e05a81d55c5ebfed86211237ce20d4bb2bb571ed624c7fdffb26588114e','occurrence_quotient_assignment_count':53968,'observed_exact_key_count':116,'maximal_physical_component_assignment_count':0,'globally_exhausted_exact_key_fibre_count':0,'global_exact_key_disposition_count':0}
 return {'status':'CERTIFIED_6728_STRICT_DYADIC_COMMON_FACE_PATCHES__3188_RANK_REDUCTIONS__QUOTIENT_72064_TO_68876','census':census,'formal_input_binding':{n:PINS[n] for n in sorted(PINS)},'formal_accepted_common_face_patch_ledger':ledger(accepted,'accepted_common_face_patch_row_id'),'formal_deferred_deeper_common_face_refinement_ledger':ledger(deferred,'Round260_deferred_face_row_id'),'formal_Round259_to_Round260_component_map_ledger':ledger(map_rows,'Round259_to_Round260_component_map_row_id'),'formal_post_Round260_component_commitment_ledger':ledger(component_rows,'post_Round260_component_row_id'),'formal_post_Round260_occurrence_quotient_frontier_ledger':ledger(frontier,'post_frontier_row_id'),'formal_post_Round260_key_quotient_frontier_ledger':ledger(key_rows,'post_Round260_key_frontier_row_id'),'scope_contract':{'canonical_patch_is_shallowest_then_lexicographically_first':True,'all_accepted_patches_have_exact_positive_area':True,'all_accepted_patches_have_strict_two_sided_3D_corridors':True,'all_5120_unresolved_faces_remain_fail_closed':True,'box_contact_or_key_equality_alone_is_never_glue':True,'common_face_saturation_is_not_component_maximality':True},'strict_nonpromotion':{'maximal_physical_component_credit':0,'global_exact_key_fibre_credit':0,'global_exact_key_disposition_credit':0,'Gate5_filled_field_slot_count':10,'Gate5_total_field_slot_count':18,'CM2':'NO-GO_FOR_CLAIM'},'required_next':'deepen the remaining 4616 Round208 and 504 Round204 common-face refinements beyond depth 4, then audit pinned cross-chart transitions'}
def safe_write(raw:bytes)->None:
 fd,name=tempfile.mkstemp(prefix=f'.{OUTPUT.name}.',dir=OUTPUT.parent);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as h:h.write(raw);h.flush();os.fsync(h.fileno())
  os.replace(p,OUTPUT)
 finally:
  if p.exists():p.unlink()
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument('--no-write',action='store_true');a=parser.parse_args();result=build();doc={'schema':SCHEMA,'result':result,'result_sha256':digest(result)};raw=canonical(doc)+b'\n'
 if not a.no_write:safe_write(raw)
 print(result['status']);print(json.dumps(result['census'],sort_keys=True));print(f"result_sha256={doc['result_sha256']}");print(f'certificate_sha256={hashlib.sha256(raw).hexdigest()}');return 0
if __name__=='__main__':raise SystemExit(main())
