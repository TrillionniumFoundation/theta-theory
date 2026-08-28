#!/usr/bin/env python3
"""Parallel zero-credit common-face patch/corridor probe for Round276 edges."""
from __future__ import annotations
import argparse,collections,hashlib,json,multiprocessing as mp,sys
from fractions import Fraction as Q
from pathlib import Path
import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as R
import cm2_round276_source_g_collar_region_face_binding_probe as P

HERE=Path(__file__).resolve().parent;CAND=[];BOX={};TABLES=None;FACE_DEPTH=8
def payload(s,ch):return {'official_key_id':s['key']['identifier'],'official_key_ordinal':s['key']['ordinal'],'official_key_row':s['key']['row'],'ordered_integer_wall_events':s['events'],'outgoing_cell':s['outgoing_cell'],'roof':s['roof'],'signed_wall_word':list(s['pattern']),'source_chart':ch,'target_chart':s['target_chart'],'target_lift':s['target']}
def evaluate(ch,target,h,q,label):
 s,_=R.dynamic_signature(ch,R.atlas.AtlasBox(*q,0,label),target,TABLES);return s is not None and P.digest(payload(s,ch))==h
def worker(i):
 a,b,h,ch,target,axis,coordinate,overlap=CAND[i];pending=[(overlap,0,[])];patch=None
 while pending:
  rect,depth,path=pending.pop();q=[];j=0
  for k in range(3):
   if k==axis:q += [coordinate,coordinate]
   else:q += list(rect[j]);j+=1
  if evaluate(ch,target,h,q,f'r277:{i}:f:{depth}'):
   patch=(q,path);break
  if depth==FACE_DEPTH:continue
  widths=[x[1]-x[0] for x in rect];split=0 if widths[0]>=widths[1] else 1;mid=(rect[split][0]+rect[split][1])/2
  for side,z in enumerate(((rect[split][0],mid),(mid,rect[split][1]))):
   child=list(rect);child[split]=z;pending.append((tuple(child),depth+1,path+[f'{split}:{side}']))
 if patch is None:return ('FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT',i,None)
 q,path=patch;depths=[]
 endpoint_sides=[]
 for rid in (a,b):
  box=BOX[rid]
  is_negative=box[2*axis+1]==coordinate
  is_positive=box[2*axis]==coordinate
  if is_negative==is_positive:
   return ('FAILCLOSED_INVALID_FACE_ORIENTATION',i,None)
  endpoint_sides.append((rid,is_negative))
 for rid,negative in endpoint_sides:
  box=BOX[rid];span=box[2*axis+1]-box[2*axis];ok=None
  for d in range(1,25):
   z=list(q);width=span/(2**d);z[2*axis:2*axis+2]=[coordinate-width,coordinate] if negative else [coordinate,coordinate+width]
   if evaluate(ch,target,h,z,f'r277:{i}:c:{d}'):
    ok=d;break
  if ok is None:return ('FAILCLOSED_NO_TWO_SIDED_CORRIDOR',i,None)
  depths.append(ok)
 return ('ACCEPT_POSITIVE_MATCH_PATCH_AND_TWO_CORRIDORS',i,(path,depths))
def build():
 global CAND,BOX,TABLES
 leaf_sig=collections.defaultdict(dict)
 for rnd,name,ledger,lf,idf in P.SOURCES:
  for x in P.load(name)[ledger]['rows']:
   sig=x['local_return_signature'];h=x.get('complete_10_field_return_signature_sha256',P.digest(sig));leaf_sig[x[lf]][h]=sig
 data=P.load('cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json');leaves=P.unpack(data,'collar_leaf_rows');occs={x['Round179_occurrence_row_id']:x for x in P.unpack(data,'collar_occurrence_rows')};faces=collections.defaultdict(lambda:[[],[]]);BOX={x['row_id']:tuple(map(Q,x['box'])) for x in leaves}
 for x in leaves:
  box=BOX[x['row_id']];o=occs[x['occurrence_row_id']]
  for axis in range(3):
   tang=tuple((box[2*k],box[2*k+1]) for k in range(3) if k!=axis)
   for side in (0,1):faces[(o['origin_row_id'],o['chart'],o['owner_target'],axis,box[2*axis+side])][side].append((x['row_id'],tang,leaf_sig.get(x['row_id'],{})))
 candidates=set()
 for (origin,ch,target,axis,coordinate),(lower,upper) in faces.items():
  for a,ta,sa in upper:
   for b,tb,sb in lower:
    if a==b:continue
    overlap=tuple((max(x[0],y[0]),min(x[1],y[1])) for x,y in zip(ta,tb,strict=True))
    if not all(x<y for x,y in overlap):continue
    for h in set(sa)&set(sb):
     if a<b:candidates.add((a,b,h,ch,target,axis,coordinate,overlap))
     else:candidates.add((b,a,h,ch,target,axis,coordinate,overlap))
 CAND=sorted(candidates,key=str);assert len(CAND)==330724;TABLES=R.registry_tables(R.load_inputs()['gate5'])
def main():
 global FACE_DEPTH
 ap=argparse.ArgumentParser();ap.add_argument('--processes',type=int,default=min(40,mp.cpu_count()));ap.add_argument('--limit',type=int);ap.add_argument('--face-depth',type=int,default=8);a=ap.parse_args();FACE_DEPTH=a.face_depth;build();n=len(CAND) if a.limit is None else min(a.limit,len(CAND));ctx=mp.get_context('fork');counts=collections.Counter();depths=collections.Counter();accepted=[]
 with ctx.Pool(a.processes) as pool:
  for status,i,detail in pool.imap_unordered(worker,range(n),chunksize=32):
   counts[status]+=1
   if detail is not None:
    path,corr=detail;depths.update(corr);accepted.append((i,path,corr))
   done=sum(counts.values())
   if done%10000==0:print(json.dumps({'progress':done,'total':n,'histogram':dict(counts)},sort_keys=True),flush=True)
 failclosed=sum(v for k,v in counts.items() if k.startswith('FAILCLOSED_'))
 result={'status':'ROUND277_COLLAR_COMMON_FACE_MATCH_PROBE__ZERO_CREDIT','input_candidate_edge_count':n,'face_refinement_depth_limit':FACE_DEPTH,'disposition_histogram':dict(sorted(counts.items())),'corridor_depth_histogram':dict(sorted(depths.items())),'accepted_edge_witnesses_sha256':P.digest(sorted(accepted)),'remaining_failclosed_edge_count':failclosed,'strict_nonpromotion':{'expanded_occurrence_credit':0,'component_edge_credit':0,'maximality_credit':0,'CM2':'NO-GO_FOR_CLAIM'}};print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
