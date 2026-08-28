import sys,json,math,argparse,hashlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any
sys.path.insert(0,'deliverables')
from flint import arb
import cm2_gate25_physical_return_core_registry_cert as cc
import cm2_gate34_full_core_return_adaptive_frontier_cert as ac
class J:
 def __init__(self,v,g=None,h=None):self.v=v;self.g=g or [arb(0) for _ in range(3)];self.h=h or [[arb(0) for _ in range(3)] for _ in range(3)]
 @staticmethod
 def var(v,i):g=[arb(0) for _ in range(3)];g[i]=arb(1);return J(v,g)
 def __add__(self,o):o=o if isinstance(o,J) else J(o);return J(self.v+o.v,[self.g[i]+o.g[i] for i in range(3)],[[self.h[i][j]+o.h[i][j] for j in range(3)] for i in range(3)])
 __radd__=__add__
 def __neg__(self):return J(-self.v,[-x for x in self.g],[[-x for x in row] for row in self.h])
 def __sub__(self,o):return self+(-o if isinstance(o,J) else -o)
 def __rsub__(self,o):return J(o)-self
 def __mul__(self,o):
  o=o if isinstance(o,J) else J(o);g=[self.g[i]*o.v+self.v*o.g[i] for i in range(3)];h=[[self.h[i][j]*o.v+self.v*o.h[i][j]+self.g[i]*o.g[j]+o.g[i]*self.g[j] for j in range(3)] for i in range(3)];return J(self.v*o.v,g,h)
 __rmul__=__mul__
 def unary(self,fv,fp,fpp):return J(fv,[fp*x for x in self.g],[[fp*self.h[i][j]+fpp*self.g[i]*self.g[j] for j in range(3)] for i in range(3)])
 def inv(self):return self.unary(1/self.v,-1/(self.v*self.v),2/(self.v*self.v*self.v))
 def __truediv__(self,o):return self*(o.inv() if isinstance(o,J) else 1/o)
 def __rtruediv__(self,o):return J(o)*self.inv()
 def sqrt(self):
  r=self.v.sqrt();return self.unary(r,1/(2*r),-1/(4*r*r*r))
def iv(a,b):return cc.first_hit.arb_interval(a,b)
def jetout(c,d,t0,t1,p0,p1,s0,s1):
 t=J.var(iv(t0,t1),0);p=J.var(iv(p0,p1),1);s=J.var(iv(s0,s1),2);one=arb(1);rn=(one-t*t).sqrt();rp=(one-p*p).sqrt();src,cell=c.chart_id.split(':')
 if cell=='E':nx,ny=rn,t
 elif cell=='W':nx,ny=-rn,t
 elif cell=='N':nx,ny=t,rn
 else:nx,ny=t,-rn
 ux=rp*nx-p*ny;uy=rp*ny+p*nx
 if src=='G':cx=cy=arb(0);R=ac.arbq(Q(9,25))
 else:cx=ac.arbq(Q(1,2))+s;cy=ac.arbq(Q(1,2));R=ac.arbq(Q(4,25))
 qx,qy=cx+R*nx,cy+R*ny;obs=c.target_id[0];ix,iy=map(int,c.target_id[2:-1].split(','));Rt=ac.arbq(Q(9,25) if obs=='G' else Q(4,25));ax=arb(ix)+(ac.arbq(Q(1,2))+s if obs=='W' else 0);ay=arb(iy)+(ac.arbq(Q(1,2)) if obs=='W' else 0)
 dx,dy=ax-qx,ay-qy;ell=ux*dx+uy*dy;tr=-uy*dx+ux*dy;root=ell-(Rt*Rt-tr*tr).sqrt();hx,hy=qx+root*ux,qy+root*uy;ox,oy=(hx-ax)/Rt,(hy-ay)/Rt;pt=tr/Rt;dc=d.chart_id.split(':')[1];tt=oy if dc in ('E','W') else ox;return tt,pt
def absub(x):return x.abs_upper()
def ceil_arb(x):
 n=max(1,math.ceil(float(x)))
 while not bool(arb(n)>x):n+=1
 return n
def sgn(x):return 1 if bool(x>0) else -1 if bool(x<0) else 0

HERE=Path(__file__).resolve().parent
WITNESSES=HERE/'cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json'
SCHEMA='cm2.round72.r1-component-f10-f13-f16.v1'
def canonical(value:Any)->str:return json.dumps(value,sort_keys=True,separators=(',',':'))
def digest(value:Any)->str:return hashlib.sha256(canonical(value).encode()).hexdigest()
def build()->dict[str,Any]:
 rows=json.loads(WITNESSES.read_text())['rows'];cs=cc.physical_cores();output_rows=[]
 t_radius=Q(1,10**10);s_radius=Q(1,10**10);p_radius=Q(1,10**6);simple_variation=Q(1,10**9)
 for row in rows:
  source,destination=cs[row['source_core_index']],cs[row['destination_core_index']];minus,plus=row['witness_minus'],row['witness_plus'];t_center=(Q(minus['t'])+Q(plus['t']))/2;p_center=(Q(minus['p'])+Q(plus['p']))/2;level=Q(row['level_value']);coordinate=0 if row['level_coordinate']=='t' else 1
  lower=jetout(source,destination,t_center-t_radius,t_center+t_radius,p_center-p_radius,p_center-p_radius,-s_radius,s_radius)[coordinate].v-ac.arbq(level);upper=jetout(source,destination,t_center-t_radius,t_center+t_radius,p_center+p_radius,p_center+p_radius,-s_radius,s_radius)[coordinate].v-ac.arbq(level)
  if sgn(lower)*sgn(upper)!=-1:raise RuntimeError('parameter germ bracket')
  function=jetout(source,destination,t_center-t_radius,t_center+t_radius,p_center-p_radius,p_center+p_radius,-s_radius,s_radius)[coordinate];fp=function.g[1]
  if sgn(fp)==0:raise RuntimeError('F_p')
  p_t=-function.g[0]/fp;p_s=-function.g[2]/fp
  p_ts=-(function.h[0][2]+function.h[0][1]*p_s+function.h[1][2]*p_t+function.h[1][1]*p_t*p_s)/fp
  p_ss=-(function.h[2][2]+2*function.h[1][2]*p_s+function.h[1][1]*p_s*p_s)/fp
  t_interval=iv(t_center-t_radius,t_center+t_radius);radius=Q(9,25) if source.source=='G' else Q(4,25);weight=ac.arbq(radius)/(1-t_interval*t_interval).sqrt();weight_t=ac.arbq(radius)*t_interval/((1-t_interval*t_interval).sqrt()**3)
  rho=weight*p_s;rho_t=weight_t*p_s+weight*p_ts;rho_s=weight*p_ss;arclength_factor=ac.arbq(1/radius);f10_bound=absub(rho)+arclength_factor*absub(rho_t)+absub(rho_s);integer=ceil_arb(f10_bound);variation=2*ac.arbq(t_radius)*absub(rho)
  if not bool(ac.arbq(simple_variation)>variation):raise RuntimeError('simple variation')
  component_id='physical-r1-face-component:'+digest({'candidate_family_id':row['candidate_family_id'],'base_parameter':'s=0','witness_minus':row['witness_minus'],'witness_plus':row['witness_plus']})
  output_rows.append({'component_id':component_id,'candidate_family_id':row['candidate_family_id'],'source_core_index':row['source_core_index'],'side':row['side'],'t_center':str(t_center),'p_center':str(p_center),'t_radius':str(t_radius),'p_bracket_radius':str(p_radius),'s_radius':str(s_radius),'lower_p_level_sign':sgn(lower),'upper_p_level_sign':sgn(upper),'F_p_sign':sgn(fp),'F10_integer_upper':integer,'F13_current_variation_strict_upper':str(simple_variation),'F16_Piola_flux_cost_strict_upper':str(simple_variation)})
 output_rows.sort(key=lambda row:row['component_id'])
 return {'schema':SCHEMA,'construction':{'canonical_germ_radii':{'t':'1/10000000000','p_bracket':'1/1000000','s':'1/10000000000'},'signed_current_density':'rho=(R_source/sqrt(1-t^2))*partial_s p_graph','F10_integrand':'abs(rho)+abs(partial_tau rho)+abs(partial_s rho)','arclength_derivative_factor_upper':'1/R_source','F16_source':'exact area-preserving Piola flux identity'},'result':{'component_count':len(output_rows),'F10_numeric_row_count':len(output_rows),'F10_integer_minimum':min(row['F10_integer_upper'] for row in output_rows),'F10_integer_maximum':max(row['F10_integer_upper'] for row in output_rows),'F10_integer_sum':sum(row['F10_integer_upper'] for row in output_rows),'F13_numeric_row_count':len(output_rows),'F13_per_face_current_variation_strict_upper':'1/1000000000','F13_32_face_current_variation_strict_upper':'4/125000000','F16_numeric_Piola_row_count':len(output_rows),'F16_32_face_flux_cost_strict_upper':'4/125000000','rows_sha256':digest(output_rows),'rows':output_rows}}
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();payload=json.dumps(build(),indent=2,sort_keys=True)+'\n'
 if args.output:args.output.write_text(payload)
 else:print(payload,end='')
 return 0
if __name__=='__main__':raise SystemExit(main())
