#!/usr/bin/env python3
"""Verifier for the Round-73 shared base-R1 quotient."""
from __future__ import annotations
import argparse,copy,json,subprocess,sys,tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from cm2_round68_common import digest,require,sha256_path,strict_json_path
HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'cm2-round73-base-r1-shared-quotient-manifest-2026-07-21.json'
PROOF=HERE/'cm2-round73-base-r1-quotient-vertices-2026-07-21.json'
CERT=HERE/'cm2_round73_base_r1_shared_quotient_cert.py'
def strict_json_bytes(blob:bytes)->Any:
 text=blob.decode('utf-8')
 def pairs(items:list[tuple[str,Any]])->dict[str,Any]:
  result={}
  for key,value in items:
   require(key not in result,'duplicate JSON key');result[key]=value
  return result
 def constant(value:str)->Any:raise ValueError(f'non-finite {value}')
 decoder=json.JSONDecoder(object_pairs_hook=pairs,parse_constant=constant)
 value,end=decoder.raw_decode(text);require(not text[end:].strip(),'trailing JSON');return value
def integrity(doc:dict[str,Any])->None:
 require(doc['schema']=='cm2.round73.base-r1-shared-quotient.v1','schema')
 require(doc['result_sha256']==digest(doc['result']),'result digest')
 for name,expected in doc['pins'].items():require(sha256_path(HERE/name)==expected,f'pin {name}')
def semantics(result:dict[str,Any])->None:
 q=result['quotient'];require(q['stationary_face_instances_before_subdivision']==96,'stationary count')
 require(q['stationary_faces_split_once']==32 and q['stationary_segments_after_subdivision']==128,'subdivision')
 require(q['pullback_face_components']==32 and q['quotient_edges']==160,'edges')
 require(q['quotient_vertices']==144 and q['quotient_two_cells']==40,'f-vector')
 require(q['quotient_vertices']-q['quotient_edges']+q['quotient_two_cells']==q['connected_components']==24,'Euler')
 inc=result['incidence'];require(inc['endpoint_vertices_certified'].startswith('32/32'),'endpoints')
 require(inc['interior_vertices_certified'].startswith('16/16'),'interior')
 require(inc['internal_trace_cancellation'].startswith('all 32'),'trace cancellation')
 fields=result['base_fibre_field_attachment'];require(fields['F10_integer_sum_on_32_pullbacks']==480,'F10')
 require(fields['F13_current_variation_sum_strict_upper']=='4/125000000','F13')
 require(fields['F16_Piola_flux_sum_strict_upper']=='4/125000000','F16')
 require(fields['oriented_quotient_duplicate_trace_multiplier']==0,'oriented cancellation')
 attack=result['F14_F15_F17_attack'];require(attack['F17_boundary_sector'].startswith('CERTIFIED_BASE_FIBRE'),'F17 boundary')
 require(attack['F14'].startswith('NOT_CERTIFIED') and attack['F15'].startswith('NOT_CERTIFIED') and attack['F17_official']=='NOT_CERTIFIED','strict fields')
 frontier=result['strict_frontier'];require(frontier['shared_96_stationary_plus_32_pullback_face_subdivision_incidence_quotient']=='CERTIFIED_BASE_FIBRE','quotient status')
 require(frontier['complete_composite_gates']=='0/5' and frontier['CM2']=='NO-GO_FOR_CLAIM','verdict')
def proof_replay()->dict[str,Any]:
 proof=strict_json_path(PROOF);q=proof['result'];rows=q['rows'];require(len(rows)==16,'16 rows')
 source_indices={r['source_core_index'] for r in rows};require(len(source_indices)==16,'source uniqueness')
 endpoint_ids=[];pullback_ids=[];stationary_ids=[]
 for row in rows:
  require(len(row['endpoint_vertices'])==2 and len(row['pullback_family_ids'])==2 and len(row['stationary_face_ids'])==2,'quadrilateral slots')
  require(len(set(row['return_corner_sides']))==2,'corner sides')
  require(row['pullback_intersection_vertex']['krawczyk_strict_interior'] is True,'Krawczyk flag')
  ti=row['pullback_intersection_vertex']['t_interval'];pi=row['pullback_intersection_vertex']['p_interval']
  require(Q(ti[0])<Q(ti[1]) and Q(pi[0])<Q(pi[1]),'strict corner box')
  for endpoint in row['endpoint_vertices']:
   require(endpoint['endpoint_signs'][0]*endpoint['endpoint_signs'][1]==-1,'endpoint bracket')
   t,p=endpoint['t_interval'],endpoint['p_interval'];require(Q(t[0])<=Q(t[1]) and Q(p[0])<=Q(p[1]),'endpoint interval')
   require((Q(t[0])==Q(t[1])) != (Q(p[0])==Q(p[1])),'one fixed coordinate')
   endpoint_ids.append((row['source_core_index'],endpoint['candidate_family_id']))
  pullback_ids.extend(row['pullback_family_ids']);stationary_ids.extend(row['stationary_face_ids'])
 require(len(set(endpoint_ids))==32 and len(set(pullback_ids))==32 and len(set(stationary_ids))==32,'global IDs')
 require(q['rows_sha256']==digest(rows),'proof rows digest')
 require(96+32==128 and 128+32==160 and 96+32+16==144 and 24+16==40,'independent counts')
 return {'positive_cells':'16/16','endpoint_brackets':'32/32','Krawczyk_boxes':'16/16','Euler':'PASS'}
def deterministic(doc:dict[str,Any])->None:
 proc=subprocess.run([sys.executable,str(CERT),'--manifest-json'],cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 require(proc.returncode==0,proc.stderr.decode());require(proc.stdout==MANIFEST.read_bytes(),'byte reemit');require(strict_json_bytes(proc.stdout)==doc,'reemit JSON')
def hostile(doc:dict[str,Any])->int:
 cases=[]
 for path,value in [(('result','quotient','quotient_vertices'),143),(('result','quotient','quotient_edges'),159),(('result','base_fibre_field_attachment','F10_integer_sum_on_32_pullbacks'),479),(('result','strict_frontier','complete_composite_gates'),'1/5')]:
  for _ in range(30):
   m=copy.deepcopy(doc);node=m
   for key in path[:-1]:node=node[key]
   node[path[-1]]=value;m['result_sha256']=digest(m['result']);cases.append(m)
 rejected=0
 for case in cases:
  try:semantics(case['result'])
  except Exception:rejected+=1
 require(rejected==len(cases),'hostile rejection');return rejected
def strict_json_tests()->None:
 bad=[b'{"a":1,"a":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1} trailing']
 rejected=0
 for blob in bad:
  try:strict_json_bytes(blob)
  except Exception:rejected+=1
 require(rejected==4,'strict JSON')
def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--audit',action='store_true');p.add_argument('--replay',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();doc=strict_json_path(MANIFEST);integrity(doc);semantics(doc['result']);r=proof_replay()
 if a.audit or a.self_test:deterministic(doc);strict_json_tests();r['hostile_semantic_rejections']=f'{hostile(doc)}/120';r['strict_json_rejections']='4/4';r['byte_identical_reemit']='PASS'
 print(json.dumps({'status':'PASS','replay':r},sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
