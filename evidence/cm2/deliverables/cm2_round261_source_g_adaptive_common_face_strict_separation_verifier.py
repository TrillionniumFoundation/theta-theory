#!/usr/bin/env python3
"""Independent verifier for Round261 adaptive strict separation."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib, importlib, json, multiprocessing as mp, os
from pathlib import Path
import stat, sys, tempfile
from typing import Any
HERE=Path(__file__).resolve().parent
DEFAULT_CANDIDATE=HERE/'cm2_round261_source_g_adaptive_common_face_strict_separation_certificate.json'
OUTPUT=HERE/'cm2_round261_source_g_adaptive_common_face_strict_separation_verification.json'
SCHEMA='cm2.round261.source-g-adaptive-common-face-strict-separation.verification.v1'
CANDIDATE_SCHEMA='cm2.round261.source-g-adaptive-common-face-strict-separation.v1'
EXPECTED_CANDIDATE_SHA256='6b69453c869d07737152c851d7716434dca16184433ef8be9023cb56027b162c'
PINS={'cm2_round179_source_g_residual_tube_arrangement_rows.json':'f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42','cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json':'e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818','cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py':'6bcfbb794005e5a92590b7bb60ffceda34db3441ced143a15ceb23e15d5c035e','cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json':'4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938','cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py':'718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36','cm2_round260_source_g_curved_region_common_face_refinement_certificate.json':'a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b','cm2_round261_source_g_adaptive_common_face_strict_separation.py':'f667e08481bea34dacf34c82b5b5fa2f19ce7e87fd476a10a1265b2f3a7f289f'}
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
def check_ledger(v:dict[str,Any],field:str)->None:
 rows=v['rows'];need(v['row_count']==len(rows) and v['rows_sha256']==digest(rows) and v['row_ids_sha256']==digest([r[field] for r in rows]) and v['row_hashes_sha256']==digest([r['row_sha256'] for r in rows]) and len(rows)==len({r[field] for r in rows}),'ledger:'+field)
 for row in rows:
  body=dict(row);actual=body.pop('row_sha256');need(actual==digest(body),'row:'+field)
def load_geometry()->None:
 read_pinned('cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py');read_pinned('cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py');read_pinned('cm2_round261_source_g_adaptive_common_face_strict_separation.py');need('cm2_round261_source_g_adaptive_common_face_strict_separation' not in sys.modules,'producer absent')
 if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))
 v208=importlib.import_module('cm2_round208_source_g_outgoing_direct_signature_materialization_verifier');v204=importlib.import_module('cm2_round204_source_g_wall_return_signature_local_replacement_verifier');_r195,r198,r174,_registry,_outgoing,collars208,_chain=v208.load_evaluator();formal=v204.load_formal_inputs();r179=formal['evaluator'].r179;r174_204=r179.r174;scope182=v204.extract_round182_scope(formal['attachment182']);scope179=v204.extract_round179_scope(formal['source179'],scope182['occurrence_ids'],scope182['origin_ids']);c204=load_result('cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json');c208=load_result('cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json');reg204={r['region_row_id']:r for r in c204['formal_local_open_3D_region_ledger']['rows']};reg208={r['region_row_id']:r for r in c208['formal_local_open_3D_signature_ledger']['rows']};boxes={rid:tuple(Fraction(x) for x in r['leaf_exact_box']) for rid,r in reg204.items()};boxes.update({rid:tuple(Fraction(x) for x in r['Round182_leaf_box']) for rid,r in reg208.items()});rows179=load_result('cm2_round179_source_g_residual_tube_arrangement_rows.json');cols=rows179['row_column_schemas']['resolved_3d_child_rows']
 for packed in rows179['resolved_3d_child_rows']:
  row=dict(zip(cols,packed));boxes[row['row_id']]=tuple(Fraction(x) for x in row['box'])
 need(len(boxes)==53968,'boxes');G.update(r198=r198,r174=r174,collars208=collars208,r204=v204,r179=r179,r174_204=r174_204,scope182=scope182,scope179=scope179,reg204=reg204,reg208=reg208,boxes=boxes)
STRICT={'STRICT_POSITIVE','STRICT_NEGATIVE'}
def state208(oid:str,vals:list[Fraction],label:str)->str:
 reg=G['reg208'][oid];p=G['r198'].selected_factor_profiles(G['collars208'][reg['occurrence_row_id']],G['r174'].atlas.AtlasBox(*vals,0,label));actual=(p['HPLUS']['selected_sign'],p['HMINUS']['selected_sign']);expected=(reg['HPLUS_sign'],reg['HMINUS_sign'])
 if actual==expected:return 'MATCH'
 if any(a in STRICT and a!=e for a,e in zip(actual,expected)):return 'EXCLUDE'
 return 'UNRESOLVED'
def state204(oid:str,vals:list[Fraction],label:str)->str:
 reg=G['reg204'][oid];collar=G['scope182']['collars'][reg['occurrence_row_id']];wall=G['scope179']['walls'][reg['occurrence_row_id']];r179=G['r179'];geo=r179.independent_geometry(collar['chart'],collar['owner_target'],G['r174_204'].atlas.AtlasBox(*vals,0,label));sn=G['r204'].CHART_CONTRACT[collar['chart']][2];tn='hit_x' if wall['axis']=='X' else 'hit_y';actual=(r179.arb_sign(r179.subtract_wall(geo[sn],0)[0]),r179.arb_sign(r179.subtract_wall(geo[tn],wall['integer_wall'])[0]));expected=('STRICT_'+reg['source_sign'],'STRICT_'+reg['target_factor_sign'])
 if actual==expected:return 'MATCH'
 if any(a in STRICT and a!=e for a,e in zip(actual,expected)):return 'EXCLUDE'
 return 'UNRESOLVED'
def face(row:dict[str,Any])->list[Fraction]:
 ids=row['occurrence_row_ids'];axis=row['face_axis'];coord=Fraction(row['face_coordinate']);a=G['boxes'][ids[0]];b=G['boxes'][ids[1]];out=[]
 for k in range(3):out += [coord,coord] if k==axis else [max(a[2*k],b[2*k]),min(a[2*k+1],b[2*k+1])]
 return out
def cell(face_values:list[Fraction],axis:int,depth:int,i:int,j:int)->list[Fraction]:
 out=list(face_values);trans=[k for k in range(3) if k!=axis];n=2**depth
 for k,index in zip(trans,(i,j)):
  lo=face_values[2*k];step=(face_values[2*k+1]-lo)/n;out[2*k]=lo+index*step;out[2*k+1]=lo+(index+1)*step
 return out
def classify(args:tuple[int,dict[str,Any]])->dict[str,Any]:
 idx,row=args;ids=row['occurrence_row_ids'];axis=row['face_axis'];coord=Fraction(row['face_coordinate']);fv=face(row);is208=row['geometry_channel']=='ROUND208_FACTOR_COMMON_FACE';state=state208 if is208 else state204;channel='ROUND208_FACTOR_ADAPTIVE_FACE' if is208 else 'ROUND204_TARGET_GRAPH_ADAPTIVE_FACE';eligible=[(0,0)];evaluations=0
 for depth in range(1,9):
  children=[]
  for pi,pj in eligible:
   for di,dj in ((0,0),(0,1),(1,0),(1,1)):
    i=2*pi+di;j=2*pj+dj;box=cell(fv,axis,depth,i,j);states=[state(oid,box,f'round261:{idx}:{depth}:{i}:{j}:{oid}') for oid in ids];evaluations+=2
    if states==['MATCH','MATCH']:
     corridors=[]
     for oid in ids:
      source=G['boxes'][oid];found=None
      for normal_depth in range(1,33):
       cb=list(box);span=source[2*axis+1]-source[2*axis];normal=span/(2**normal_depth)
       if source[2*axis+1]==coord:cb[2*axis:2*axis+2]=[coord-normal,coord];side='LOWER_SIDE_CORRIDOR'
       elif source[2*axis]==coord:cb[2*axis:2*axis+2]=[coord,coord+normal];side='UPPER_SIDE_CORRIDOR'
       else:raise RuntimeError(f'incidence:{oid}')
       if state(oid,cb,f'round261-corridor:{idx}:{depth}:{i}:{j}:{oid}:{normal_depth}')=='MATCH':found={'occurrence_row_id':oid,'corridor_side':side,'dyadic_normal_depth':normal_depth,'exact_normal_depth':text(normal),'exact_corridor_box':[text(x) for x in cb]};break
      need(found is not None,f'corridor depth32:{idx}:{oid}');corridors.append(found)
     return {'source_id':row['Round258_boundary_face_candidate_id'],'status':'ACCEPT','channel':channel,'face_depth':depth,'cell_index':[i,j],'cell':[text(x) for x in box],'corridors':corridors,'evaluated_cell_side_count':evaluations}
    if 'EXCLUDE' not in states:children.append((i,j))
  eligible=children
  if not eligible:return {'source_id':row['Round258_boundary_face_candidate_id'],'status':'REJECT_STRICT_SEPARATION_TREE_EXHAUSTED','channel':channel,'exhaustion_depth':depth,'evaluated_cell_side_count':evaluations}
 return {'source_id':row['Round258_boundary_face_candidate_id'],'status':'DEFER_UNRESOLVED_AFTER_ADAPTIVE_DEPTH_8','channel':channel,'unresolved_depth_8_cell_count':len(eligible),'evaluated_cell_side_count':evaluations}
def verify(candidate:dict[str,Any])->dict[str,Any]:
 for v,f in ((candidate['formal_accepted_adaptive_face_patch_ledger'],'accepted_adaptive_face_patch_row_id'),(candidate['formal_strictly_separated_face_ledger'],'strictly_rejected_face_row_id'),(candidate['formal_deferred_depth_8_face_ledger'],'Round261_deferred_face_row_id'),(candidate['formal_Round260_to_Round261_component_map_ledger'],'Round260_to_Round261_component_map_row_id'),(candidate['formal_post_Round261_component_commitment_ledger'],'post_Round261_component_row_id'),(candidate['formal_post_Round261_occurrence_frontier_ledger'],'post_frontier_row_id'),(candidate['formal_post_Round261_key_frontier_ledger'],'post_Round261_key_frontier_row_id')):check_ledger(v,f)
 r260=load_result('cm2_round260_source_g_curved_region_common_face_refinement_certificate.json');load_geometry();sources=r260['formal_deferred_deeper_common_face_refinement_ledger']['rows']
 with mp.get_context('fork').Pool(32) as pool:results=list(pool.imap(classify,enumerate(sources,1),chunksize=4))
 aa={r['Round258_boundary_face_candidate_id']:r for r in candidate['formal_accepted_adaptive_face_patch_ledger']['rows']};rr={r['Round258_boundary_face_candidate_id']:r for r in candidate['formal_strictly_separated_face_ledger']['rows']};dd={r['Round258_boundary_face_candidate_id']:r for r in candidate['formal_deferred_depth_8_face_ledger']['rows']};by={r['Round258_boundary_face_candidate_id']:r for r in sources};m={r['Round259_quotient_component_id']:r['post_Round260_quotient_component_id'] for r in r260['formal_Round259_to_Round260_component_map_ledger']['rows']};ea=set();er=set();ed=set();pairs=set();area=Fraction();volume=Fraction()
 for x in results:
  source=by[x['source_id']];current=tuple(sorted(m[v] for v in source['pre_Round260_component_ids']))
  if x['status']=='ACCEPT':
   ea.add(x['source_id']);row=aa[x['source_id']];need(row['dyadic_face_refinement_depth']==x['face_depth'] and row['dyadic_face_cell_index']==x['cell_index'] and row['exact_common_face_patch_box']==x['cell'] and row['strict_two_sided_corridor_proofs']==x['corridors'],'accept proof');patch=Fraction(source['parent_exact_common_face_area'])/(4**x['face_depth']);area+=patch
   for c in x['corridors']:volume+=patch*Fraction(c['exact_normal_depth'])
   if current[0]!=current[1]:pairs.add(current)
  elif x['status'].startswith('REJECT'):
   er.add(x['source_id']);need(rr[x['source_id']]['strict_separation_tree_exhaustion_depth']==x['exhaustion_depth'],'reject proof')
  else:
   ed.add(x['source_id']);need(dd[x['source_id']]['unresolved_depth_8_cell_count']==x['unresolved_depth_8_cell_count'],'defer proof')
 need(set(aa)==ea and set(rr)==er and set(dd)==ed and len(ea)==3280 and len(er)==224 and len(ed)==1616,'partition');need(digest(sorted(ea))=='2ea175fe5441bd25f832ed348c63689155597990e7700f763b5235ffacf0649b' and area==Fraction(186865401,53687091200000) and volume==Fraction(8464695485090211,1844674407370955161600000) and len(pairs)==224,'geometry census')
 source_components=r260['formal_post_Round260_component_commitment_ledger']['rows'];keys={r['post_Round260_quotient_component_id']:(r['official_key_id'],r['official_key_ordinal']) for r in source_components};dsu=DSU(sorted(keys));rank=0
 for a,b in sorted(pairs):need(keys[a]==keys[b],'key purity');rank+=int(dsu.union(a,b))
 members=defaultdict(list)
 for cid in sorted(keys):members[dsu.find(cid)].append(cid)
 need(rank==128 and len(members)==68748,'DSU');post={};em={}
 for values in members.values():
  pid=values[0] if len(values)==1 else 'round261-adaptive-face-component:'+digest(values);em[pid]=values
  for old in values:post[old]=pid
 am={r['Round260_quotient_component_id']:r['post_Round261_quotient_component_id'] for r in candidate['formal_Round260_to_Round261_component_map_ledger']['rows']};need(am==post,'map');need({r['post_Round261_quotient_component_id']:r['constituent_Round260_component_ids'] for r in candidate['formal_post_Round261_component_commitment_ledger']['rows']}==em,'members')
 for row in candidate['formal_post_Round261_occurrence_frontier_ledger']['rows']:need(row['post_Round261_quotient_component_id']==post[row['post_Round260_quotient_component_id']],'frontier')
 c=candidate['census'];need(c['accepted_adaptive_common_face_patch_count']==3280 and c['strictly_separated_face_count']==224 and c['deferred_after_depth_8_face_count']==1616 and c['rank_reducing_component_pair_count']==128 and c['post_Round261_component_count']==68748,'census');need(candidate['strict_nonpromotion']['CM2']=='NO-GO_FOR_CLAIM','nonpromotion')
 return {'status':'PASS_INDEPENDENT_ROUND261','independent_geometry_recomputed':True,'producer_imported_or_executed':False,'accepted_patch_count':3280,'strictly_separated_face_count':224,'remaining_fail_closed_face_count':1616,'rank_reduction_count':128,'post_component_count':68748,'occurrence_frontier_count':53968,'exact_key_frontier_count':116,'CM2':'NO-GO_FOR_CLAIM'}
def safe_write(raw:bytes)->None:
 fd,name=tempfile.mkstemp(prefix=f'.{OUTPUT.name}.',dir=OUTPUT.parent);p=Path(name)
 try:
  with os.fdopen(fd,'wb') as h:h.write(raw);h.flush();os.fsync(h.fileno())
  os.replace(p,OUTPUT)
 finally:
  if p.exists():p.unlink()
def main()->int:
 a=argparse.ArgumentParser();a.add_argument('candidate',nargs='?',type=Path,default=DEFAULT_CANDIDATE);a.add_argument('--no-write',action='store_true');args=a.parse_args();raw=args.candidate.read_bytes();need(hashlib.sha256(raw).hexdigest()==EXPECTED_CANDIDATE_SHA256,'candidate hash');doc=json.loads(raw);need(doc['schema']==CANDIDATE_SCHEMA and digest(doc['result'])==doc['result_sha256'],'envelope');result=verify(doc['result']);out={'schema':SCHEMA,'result':result,'result_sha256':digest(result)};encoded=canonical(out)+b'\n'
 if not args.no_write:safe_write(encoded)
 print(result['status']);print(json.dumps(result,sort_keys=True));print(f"result_sha256={out['result_sha256']}");print(f'verification_sha256={hashlib.sha256(encoded).hexdigest()}');return 0
if __name__=='__main__':raise SystemExit(main())
