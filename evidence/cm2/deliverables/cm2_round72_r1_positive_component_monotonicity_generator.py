#!/usr/bin/env python3
"""Arb derivative-sign generator for the 32 positive R1 components."""
from __future__ import annotations
import argparse,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
from flint import arb
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert
HERE=Path(__file__).resolve().parent
WITNESSES=HERE/'cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json'
SCHEMA='cm2.round72.r1-positive-component-monotonicity.v1'
def canonical(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(',',':'))
def digest(v:Any)->str:return hashlib.sha256(canonical(v).encode()).hexdigest()
class Jet:
 def __init__(self,value:arb,dt:arb|int=0,dp:arb|int=0):self.value,self.dt,self.dp=value,dt,dp
 def __add__(self,other:Any):
  other=other if isinstance(other,Jet) else Jet(other);return Jet(self.value+other.value,self.dt+other.dt,self.dp+other.dp)
 __radd__=__add__
 def __neg__(self):return Jet(-self.value,-self.dt,-self.dp)
 def __sub__(self,other:Any):return self+(-other if isinstance(other,Jet) else -other)
 def __rsub__(self,other:Any):return Jet(other)-self
 def __mul__(self,other:Any):
  other=other if isinstance(other,Jet) else Jet(other);return Jet(self.value*other.value,self.dt*other.value+self.value*other.dt,self.dp*other.value+self.value*other.dp)
 __rmul__=__mul__
 def inverse(self):return Jet(1/self.value,-self.dt/(self.value*self.value),-self.dp/(self.value*self.value))
 def __truediv__(self,other:Any):return self*(other.inverse() if isinstance(other,Jet) else 1/other)
 def __rtruediv__(self,other:Any):return Jet(other)*self.inverse()
 def sqrt(self):
  root=self.value.sqrt();return Jet(root,self.dt/(2*root),self.dp/(2*root))
def output(core:Any,destination:Any,t0:Q,t1:Q,p0:Q,p1:Q)->tuple[Jet,Jet]:
 t=Jet(core_cert.first_hit.arb_interval(t0,t1),arb(1),arb(0));p=Jet(core_cert.first_hit.arb_interval(p0,p1),arb(0),arb(1));one=arb(1);rn=(one-t*t).sqrt();rp=(one-p*p).sqrt();source,cell=core.chart_id.split(':')
 if cell=='E':nx,ny=rn,t
 elif cell=='W':nx,ny=-rn,t
 elif cell=='N':nx,ny=t,rn
 else:nx,ny=t,-rn
 ux=rp*nx-p*ny;uy=rp*ny+p*nx
 if source=='G':cx=cy=arb(0);radius=adaptive_cert.arbq(Q(9,25))
 else:cx=cy=adaptive_cert.arbq(Q(1,2));radius=adaptive_cert.arbq(Q(4,25))
 qx,qy=cx+radius*nx,cy+radius*ny;obstacle=core.target_id[0];ix,iy=map(int,core.target_id[2:-1].split(','));target_radius=adaptive_cert.arbq(Q(9,25) if obstacle=='G' else Q(4,25));ax=arb(ix)+(adaptive_cert.arbq(Q(1,2)) if obstacle=='W' else 0);ay=arb(iy)+(adaptive_cert.arbq(Q(1,2)) if obstacle=='W' else 0)
 dx,dy=ax-qx,ay-qy;ell=ux*dx+uy*dy;transverse=-uy*dx+ux*dy;root=ell-(target_radius*target_radius-transverse*transverse).sqrt();hx,hy=qx+root*ux,qy+root*uy;normal_x,normal_y=(hx-ax)/target_radius,(hy-ay)/target_radius;target_p=transverse/target_radius;destination_cell=destination.chart_id.split(':')[1];target_t=normal_y if destination_cell in ('E','W') else normal_x;return target_t,target_p
def sign(value:arb)->int:
 if bool(value>0):return 1
 if bool(value<0):return -1
 return 0
def split(core:Any,box:tuple[Q,Q,Q,Q,str])->tuple[tuple[Q,Q,Q,Q,str],...]:
 t0,t1,p0,p1,path=box
 if (t1-t0)/(core.t1-core.t0)>=(p1-p0)/(core.p1-core.p0):
  middle=(t0+t1)/2;return((t0,middle,p0,p1,path+'0'),(middle,t1,p0,p1,path+'1'))
 middle=(p0+p1)/2;return((t0,t1,p0,middle,path+'0'),(t0,t1,middle,p1,path+'1'))
def build()->dict[str,Any]:
 witness=json.loads(WITNESSES.read_text())['rows'];cores=core_cert.physical_cores();source_indices=sorted({r['source_core_index'] for r in witness});rows=[]
 for source_index in source_indices:
  core=cores[source_index];destination_indices={r['destination_core_index'] for r in witness if r['source_core_index']==source_index}
  if len(destination_indices)!=1:raise RuntimeError('destination uniqueness')
  destination=cores[destination_indices.pop()];stack=[(core.t0,core.t1,core.p0,core.p1,'',0)];leaves=[];tests=0
  while stack:
   t0,t1,p0,p1,path,depth=stack.pop();target_t,target_p=output(core,destination,t0,t1,p0,p1);determinant=target_t.dt*target_p.dp-target_t.dp*target_p.dt;signs=[sign(x) for x in (target_t.dt,target_t.dp,target_p.dt,target_p.dp,determinant)];tests+=1
   if 0 in signs:
    if depth>=12:raise RuntimeError(f'unresolved derivative signs {source_index}:{path}')
    for child in reversed(split(core,(t0,t1,p0,p1,path))):stack.append((*child,depth+1))
   else:leaves.append({'dyadic_path':path,'depth':depth,'signs':signs})
  leaves.sort(key=lambda row:row['dyadic_path']);patterns={tuple(row['signs']) for row in leaves}
  if len(patterns)!=1:raise RuntimeError('inconsistent signs')
  rows.append({'source_core_index':source_index,'source_core_id':adaptive_cert.core_id(core),'destination_core_id':adaptive_cert.core_id(destination),'derivative_order':['dt_target_t','dp_target_t','dt_target_p','dp_target_p','Jacobian_t_p'],'common_sign_pattern':list(next(iter(patterns))),'tree_test_count':tests,'leaf_count':len(leaves),'maximum_depth':max(row['depth'] for row in leaves),'leaf_rows':leaves,'leaf_rows_sha256':digest(leaves)})
 return {'schema':SCHEMA,'theorem':{'global_source_core_derivative_signs_certified':True,'every_target_face_level_strictly_monotone_in_source_p':True,'target_coordinate_Jacobian_never_zero':True,'each_clipped_positive_face_is_one_connected_graph_component':True,'connected_rank':0},'audit':{'positive_source_core_count':len(rows),'positive_face_count':len(witness),'total_tree_test_count':sum(r['tree_test_count'] for r in rows),'total_leaf_count':sum(r['leaf_count'] for r in rows),'global_maximum_depth':max(r['maximum_depth'] for r in rows),'source_rows_sha256':digest(rows),'source_rows':rows}}
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();payload=json.dumps(build(),indent=2,sort_keys=True)+'\n'
 if args.output:args.output.write_text(payload)
 else:print(payload,end='')
 return 0
if __name__=='__main__':raise SystemExit(main())
