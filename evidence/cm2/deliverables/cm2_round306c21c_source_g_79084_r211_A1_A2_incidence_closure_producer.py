#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
from flint import arb,ctx
ROOT=Path(__file__).resolve().parent;P="cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R173="cm2_round173_source_g_exact_return_signature_transport_certificate.json";R208="cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json";R211="cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";C21BL="cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization_ledger.jsonl.gz";C21BR="cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization_result.json";PINS={R173:"5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",R208:"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",R211:"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",C20:"bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",C21BL:"1500052cf49cfa7a22388567173a912be6b79d2ba647ad5d1906f9e170dc26bb",C21BR:"bcf5d1f2b04faca4b5e5b74e79ec0b21a7e91f4aa6ffa7fe23d3b5e13fdbc73a"};STRICT={"STRICT_NEGATIVE","STRICT_POSITIVE"};OPPOSITE={"STRICT_NEGATIVE":"STRICT_POSITIVE","STRICT_POSITIVE":"STRICT_NEGATIVE"}
class E(RuntimeError):pass
def need(v,l):
 if type(v)is not bool or not v:raise E(l)
def c(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def h(v):return hashlib.sha256(c(v)).hexdigest()
def fh(q):
 x=hashlib.sha256()
 with q.open("rb")as f:
  while b:=f.read(1048576):x.update(b)
 return x.hexdigest()
def closed(r,l):b=dict(r);need(b.pop("row_sha256",None)==h(b),l)
def rows(q,verify=True):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw)
   if verify:need(c(r)==raw,"canonical");closed(r,"row closure")
   yield r
def envelope(name):
 d=json.loads((ROOT/name).read_bytes());need(set(d)=={"schema","result","result_sha256"}and d["result_sha256"]==h(d["result"]),"envelope:"+name);return d["result"]
def aq(v):v=Q(v);return arb(v.numerator)/v.denominator
def interval(a,b):
 a,b=Q(a),Q(b);need(a<=b,"interval");m=(a+b)/2;r=(b-a)/2;return aq(m)+arb(0,aq(r).upper())
def sign(v):return"STRICT_POSITIVE"if bool(v>0)else"STRICT_NEGATIVE"if bool(v<0)else"OVERWRAP"
def add(a,b):return a[0]+b[0],tuple(x+y for x,y in zip(a[1],b[1]))
def neg(a):return-a[0],tuple(-x for x in a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return a[0]*b[0],tuple(x*b[0]+a[0]*y for x,y in zip(a[1],b[1]))
def scale(a,v):v=aq(v);return a[0]*v,tuple(x*v for x in a[1])
def div(a,b):return mul(a,(1/b[0],tuple(-x/(b[0]*b[0])for x in b[1])))
def const(v):return aq(v),(arb(0),arb(0),arb(0))
def sqrt(a):v=a[0].sqrt();return v,tuple(x/(2*v)for x in a[1])
def parse_target(v):need(v.startswith("W[")and v.endswith("]"),"target");a,b=v[2:-1].split(",");return int(a),int(b)
def geometry(chart,target,t,p_or_u,s,sigma=None):
 t=(t,(arb(1),arb(0),arb(0)));s=(s,(arb(0),arb(0),arb(1)));one=const(1)
 if sigma is None:p=(p_or_u,(arb(0),arb(1),arb(0)));rp=sqrt(sub(one,mul(p,p)))
 else:u=(p_or_u,(arb(0),arb(1),arb(0)));u2=mul(u,u);den=add(one,u2);p=scale(div(sub(one,u2),den),sigma);rp=div(scale(u,2),den)
 rt=sqrt(sub(one,mul(t,t)));cell=chart.split(":")[1];need(cell in{"E","W","N","S"},"chart")
 if cell=="E":nx,ny=rt,t
 elif cell=="W":nx,ny=neg(rt),t
 elif cell=="N":nx,ny=t,rt
 else:nx,ny=t,neg(rt)
 ux=sub(mul(rp,nx),mul(p,ny));uy=add(mul(rp,ny),mul(p,nx));sx=scale(nx,Q(9,25));sy=scale(ny,Q(9,25));ix,iy=parse_target(target);cx=add(const(Q(ix)+Q(1,2)),s);cy=const(Q(iy)+Q(1,2));dx=sub(cx,sx);dy=sub(cy,sy);tr=add(neg(mul(uy,dx)),mul(ux,dy));radicand=sub(const(Q(16,625)),mul(tr,tr));need(bool(radicand[0]>0),"discriminant");rad=sqrt(radicand);ox=scale(add(neg(mul(rad,ux)),mul(tr,uy)),Q(25,4));oy=scale(sub(neg(mul(rad,uy)),mul(tr,ux)),Q(25,4));return{"HPLUS":add(ox,oy),"HMINUS":sub(ox,oy)}
def sqrt_upper(v,bits=192):
 v=Q(v);d=1<<bits;n=v.numerator<<(2*bits);r=isqrt(n//v.denominator)
 while r*r*v.denominator<n:r+=1
 while r and(r-1)*(r-1)*v.denominator>=n:r-=1
 z=Q(r,d);need(z*z>=v,"sqrt upper");return z
def face_box(box,side):v=box[0]if side=="LOWER"else box[1];return[v,v,*box[2:]]
def fixed_box(box,axis,upper):
 out=list(box);i={"t":0,"p":1,"s":2}[axis]*2;v=out[i+1]if upper else out[i];out[i]=out[i+1]=v;return out
def direct_eval(chart,target,box,factor):return geometry(chart,target,interval(box[0],box[1]),interval(box[2],box[3]),interval(box[4],box[5]))[factor]
def centered_direct(chart,target,box,factor):
 mids=[(Q(box[i])+Q(box[i+1]))/2 for i in(0,2,4)];point=[str(mids[0]),str(mids[0]),str(mids[1]),str(mids[1]),str(mids[2]),str(mids[2])];full=direct_eval(chart,target,box,factor);value=direct_eval(chart,target,point,factor)[0];env=[interval(box[0],box[1]),interval(box[2],box[3]),interval(box[4],box[5])];return value+sum((full[1][i]*(env[i]-aq(mids[i]))for i in range(3)),arb(0))
def stereo_data(box):
 left,right=Q(box[2]),Q(box[3]);sigma=-1 if left==-1 else 1;need(left==-1 or right==1,"stereo endpoint");inner=right if sigma==-1 else left;u2=(1-sigma*inner)/(1+sigma*inner);return sigma,inner,u2,aq(u2).sqrt(),sqrt_upper(u2)
def centered_stereo(chart,target,factor,sigma,t,u,s,u_center,s_center):
 full=geometry(chart,target,t,u,s,sigma)[factor];point=geometry(chart,target,t,u_center,s_center,sigma)[factor][0];return point+full[1][1]*(u-u_center)+full[1][2]*(s-s_center)
def curve_proof(sheet,leaf,curve,owner,c21b):
 chart=owner["local_return_signature"]["source_chart"];target=owner["local_return_signature"]["target_lift"];box=leaf["box"];factor=sheet["active_factor"];side=curve["face_side"];tq=Q(box[0]if side=="LOWER"else box[1]);endpoint=Q(box[2])==-1 or Q(box[3])==1;corners={};edges={}
 if not endpoint:
  proof_mode="DIRECT_TPS";face=face_box(box,side);full=direct_eval(chart,target,face,factor);graph_interval=full[1][1];graph_axis="p";corner_specs={"SW":(face[2],face[4]),"SE":(face[3],face[4]),"NE":(face[3],face[5]),"NW":(face[2],face[5])}
  for label,(p,s)in corner_specs.items():
   value=direct_eval(chart,target,[str(tq),str(tq),p,p,s,s],factor)[0];corners[label]={"physical_TPS_point":[str(tq),p,s],"value_interval":str(value),"sign":sign(value)}
  specs={"S":(("SW","SE"),"s",False,1,"p"),"E":(("SE","NE"),"p",True,2,"s"),"N":(("NW","NE"),"s",True,1,"p"),"W":(("SW","NW"),"p",False,2,"s")}
  for edge,(pair,axis,upper,index,tangent)in specs.items():
   edge_box=fixed_box(face,axis,upper);dual=direct_eval(chart,target,edge_box,factor);centered=centered_direct(chart,target,edge_box,factor);direct_sign=sign(dual[0]);centered_sign=sign(centered);selected=direct_sign if direct_sign in STRICT else centered_sign;derivative_sign=sign(dual[1][index]);end_signs=[corners[pair[0]]["sign"],corners[pair[1]]["sign"]]
   if selected in STRICT:need(end_signs==[selected,selected],"edge C0/corner");disposition="STRICT_C0_ZERO_ABSENT"
   elif derivative_sign in STRICT:disposition="UNIQUE_BRACKETED_ZERO"if set(end_signs)==STRICT else"STRICT_MONOTONE_ZERO_ABSENT"
   else:disposition="EDGE_ZERO_SET_UNRESOLVED"
   edges[edge]={"edge":edge,"proof_coordinate_system":"TPS","exact_closed_edge_box":edge_box,"tangent_coordinate":tangent,"endpoint_corner_labels":list(pair),"endpoint_corner_signs":end_signs,"direct_C0_interval":str(dual[0]),"direct_C0_sign":direct_sign,"centered_C0_interval":str(centered),"centered_C0_sign":centered_sign,"selected_C0_sign":selected,"tangent_derivative_interval":str(dual[1][index]),"tangent_derivative_sign":derivative_sign,"disposition":disposition}
  chart_data={"kind":"DIRECT_TPS","closed_face_box":face}
 else:
  proof_mode="STEREOGRAPHIC_TUS";sigma,inner,u2,u_max,u_upper=stereo_data(box);t=aq(tq);u_range=interval(0,u_upper);s_range=interval(box[4],box[5]);s_center=aq((Q(box[4])+Q(box[5]))/2);full=geometry(chart,target,t,u_range,s_range,sigma)[factor];graph_interval=full[1][1];graph_axis="u";corner_specs={"SW":(arb(0),aq(box[4]),str(Q(sigma)),box[4]),"SE":(u_max,aq(box[4]),str(inner),box[4]),"NE":(u_max,aq(box[5]),str(inner),box[5]),"NW":(arb(0),aq(box[5]),str(Q(sigma)),box[5])}
  for label,(u,s,p_exact,s_exact)in corner_specs.items():
   value=geometry(chart,target,t,u,s,sigma)[factor][0];corners[label]={"proof_TUS_point":[str(tq),("0"if label in{"SW","NW"}else"sqrt("+str(u2)+")"),s_exact],"physical_TPS_point":[str(tq),p_exact,s_exact],"value_interval":str(value),"sign":sign(value)}
  specs={"S":(("SW","SE"),u_range,aq(box[4]),u_max/2,aq(box[4]),1,"u"),"E":(("SE","NE"),u_max,s_range,u_max,s_center,2,"s"),"N":(("NW","NE"),u_range,aq(box[5]),u_max/2,aq(box[5]),1,"u"),"W":(("SW","NW"),arb(0),s_range,arb(0),s_center,2,"s")}
  for edge,(pair,u,s,u_center,sc,index,tangent)in specs.items():
   dual=geometry(chart,target,t,u,s,sigma)[factor];centered=centered_stereo(chart,target,factor,sigma,t,u,s,u_center,sc);direct_sign=sign(dual[0]);centered_sign=sign(centered);selected=direct_sign if direct_sign in STRICT else centered_sign;derivative_sign=sign(dual[1][index]);end_signs=[corners[pair[0]]["sign"],corners[pair[1]]["sign"]]
   if selected in STRICT:need(end_signs==[selected,selected],"stereo C0/corner");disposition="STRICT_C0_ZERO_ABSENT"
   elif derivative_sign in STRICT:disposition="UNIQUE_BRACKETED_ZERO"if set(end_signs)==STRICT else"STRICT_MONOTONE_ZERO_ABSENT"
   else:disposition="EDGE_ZERO_SET_UNRESOLVED"
   edges[edge]={"edge":edge,"proof_coordinate_system":"TUS","tangent_coordinate":tangent,"endpoint_corner_labels":list(pair),"endpoint_corner_signs":end_signs,"direct_C0_interval":str(dual[0]),"direct_C0_sign":direct_sign,"centered_C0_interval":str(centered),"centered_C0_sign":centered_sign,"selected_C0_sign":selected,"tangent_derivative_interval":str(dual[1][index]),"tangent_derivative_sign":derivative_sign,"disposition":disposition}
  chart_data={"kind":"RATIONAL_STEREOGRAPHIC_TUS","sigma":sigma,"physical_p_endpoint":str(Q(sigma)),"physical_p_inner":str(inner),"exact_u_max_squared":str(u2),"interval_proof_u_upper_dyadic":str(u_upper),"closed_face_hull":[str(tq),str(tq),"0",str(u_upper),box[4],box[5]]}
 graph_sign=sign(graph_interval);need(graph_axis==curve["graph_axis"]and graph_sign in STRICT and all(x["sign"]in STRICT for x in corners.values()),"curve regularity");bracketed=sorted(edge for edge,evidence in edges.items()if evidence["disposition"]=="UNIQUE_BRACKETED_ZERO");need(all(evidence["disposition"]!="EDGE_ZERO_SET_UNRESOLVED"for evidence in edges.values())and"|".join(bracketed)==curve["boundary_edge_pair"],"edge exhaustion");theorem={"kind":"A2_UNIQUE_TWO_ENDPOINT_ACTIVE_FACTOR_BOUNDARY_CURVE","C21b_sheet_theorem_row_sha256":c21b["row_sha256"],"C21b_sheet_theorem_ast_sha256":c21b["theorem_ast_sha256"],"active_factor":factor,"face_side":side,"exact_t_face_coordinate":str(tq),"proof_chart":chart_data,"graph_axis":graph_axis,"graph_derivative_interval":str(graph_interval),"graph_derivative_sign":graph_sign,"corner_evidence":corners,"edge_evidence":[edges[key]for key in sorted(edges)],"bracketed_boundary_edges":bracketed,"boundary_edge_pair":curve["boundary_edge_pair"],"each_boundary_endpoint_unique_by_strict_edge_derivative":True,"all_four_edges_exhaustively_resolved":True,"curve_regular_and_single_valued_in_selected_graph_axis":True,"inactive_factor_excludes_simultaneous_factor_zero":True};return theorem,edges,proof_mode,graph_sign
def signature_core(v):return{k:x for k,x in v.items()if k not in{"outgoing_cell","target_chart"}}
def probe_sheet(sheet,leaf,owner,shadow):
 core=signature_core(owner["local_return_signature"]);need(core==signature_core(shadow["local_return_signature"]),"signature");cs=h(core);identity={"leaf_row_id":leaf["leaf_row_id"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"rule":"E_OR_W_OWNS__N_OR_S_SHADOWS"};pid="round209-half-open-sheet:"+h(identity);relation="HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"if sheet["active_factor"]=="HPLUS"else"HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET";body={"sheet_row_id":pid,"leaf_row_id":leaf["leaf_row_id"],"origin_row_id":leaf["origin_row_id"],"occurrence_row_id":leaf["occurrence_row_id"],"retained_child_row_id":leaf["retained_child_row_id"],"leaf_classification":leaf["final_graph_classification"],"active_factor":sheet["active_factor"],"inactive_factor":sheet["inactive_factor"],"inactive_factor_whole_box_C0_proof":"DIRECT_WHOLE_BOX_C0","inactive_factor_whole_box_strict_sign":sheet["inactive_factor_whole_box_strict_sign"],"factor_identity_on_sheet":relation,"Nx_sign_on_sheet":sheet["inactive_factor_whole_box_strict_sign"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"owner_outgoing_cell":owner["outgoing_cell"],"shadow_outgoing_cell":shadow["outgoing_cell"],"owner_signature_core_sha256":cs,"shadow_signature_core_sha256":cs,"signature_difference_field_allowlist":["outgoing_cell","target_chart"],"Round173_half_open_rule":"E or W owns; N or S excludes","deterministic_unique_owner_lineage":True,"incidence_is_not_a_global_component":True,"formal_half_open_owner_credit":0,"whole_original_tube_credit":0,"global_exact_key_disposition_credit":0};return{**body,"row_sha256":h(body)}
def probe_curve(curve,sheet,leaf,owner,shadow):
 ps=probe_sheet(sheet,leaf,owner,shadow);identity={"sheet_row_id":ps["sheet_row_id"],"face_side":curve["face_side"],"boundary_edge_pair":curve["boundary_edge_pair"],"graph_axis":curve["graph_axis"],"provenance":curve["geometry_provenance"]};pid="round209-half-open-curve-incidence:"+h(identity);body={"curve_row_id":pid,"sheet_row_id":ps["sheet_row_id"],"sheet_row_sha256":ps["row_sha256"],"leaf_row_id":leaf["leaf_row_id"],"face_side":curve["face_side"],"graph_axis":curve["graph_axis"],"boundary_edge_pair":curve["boundary_edge_pair"],"geometry_provenance":curve["geometry_provenance"],"owner_region_row_id":owner["region_row_id"],"owner_outgoing_cell":owner["outgoing_cell"],"shadow_region_row_id":shadow["region_row_id"],"shadow_outgoing_cell":shadow["outgoing_cell"],"owner_signature_core_sha256":h(signature_core(owner["local_return_signature"])),"deterministic_owner_lineage_inherited_from_sheet":True,"incidence_is_not_a_global_component":True,"formal_half_open_owner_credit":0,"whole_original_tube_credit":0,"global_exact_key_disposition_credit":0};return{**body,"row_sha256":h(body)}
def probe_endpoint(endpoint,probe):
 identity={"curve_row_id":probe["curve_row_id"],"endpoint_ordinal":endpoint["endpoint_ordinal"],"boundary_edge":endpoint["boundary_edge"]};pid="round209-half-open-endpoint-incidence:"+h(identity);body={"endpoint_row_id":pid,"curve_row_id":probe["curve_row_id"],"curve_row_sha256":probe["row_sha256"],"sheet_row_id":probe["sheet_row_id"],"leaf_row_id":probe["leaf_row_id"],"face_side":probe["face_side"],"endpoint_ordinal":endpoint["endpoint_ordinal"],"boundary_edge":endpoint["boundary_edge"],"owner_region_row_id":probe["owner_region_row_id"],"owner_outgoing_cell":probe["owner_outgoing_cell"],"shadow_region_row_id":probe["shadow_region_row_id"],"shadow_outgoing_cell":probe["shadow_outgoing_cell"],"owner_signature_core_sha256":probe["owner_signature_core_sha256"],"deterministic_owner_lineage_inherited_from_curve":True,"incidence_is_not_a_global_component":True,"formal_half_open_owner_credit":0,"whole_original_tube_credit":0,"global_exact_key_disposition_credit":0};return{**body,"row_sha256":h(body)}
def c21b_index():
 out={}
 for r in rows(ROOT/C21BL,False):
  need(r["R211_sheet_row_id"]not in out,"C21b duplicate");out[r["R211_sheet_row_id"]]={"row_sha256":r["row_sha256"],"theorem_ast_sha256":r["theorem_ast_sha256"],"active_factor_equation_ast_sha256":r["theorem_ast"]["active_factor_equation_ast_sha256"],"proof_chart_kind":r["theorem_ast"]["proof_coordinate_chart"]["kind"],"active_factor_t_derivative_sign":r["theorem_ast"]["interval_proof"]["active_factor_t_derivative_sign"]}
 need(len(out)==17716,"C21b index");return out
def full_face_certificate(sheet,leaf,owner):
 chart=owner["local_return_signature"]["source_chart"];target=owner["local_return_signature"]["target_lift"];need(not(Q(leaf["box"][2])==-1 or Q(leaf["box"][3])==1),"full stereo");faces=[]
 for side in("LOWER","UPPER"):
  initial=face_box(leaf["box"],side);stack=[(initial,0,0)];cells=[];overall=None
  while stack:
   box,dp,ds=stack.pop();dual=direct_eval(chart,target,box,sheet["active_factor"]);center=centered_direct(chart,target,box,sheet["active_factor"]);direct_sign=sign(dual[0]);center_sign=sign(center);selected=direct_sign if direct_sign in STRICT else center_sign
   if selected in STRICT:
    if overall is None:overall=selected
    need(selected==overall,"full face mixed");cells.append({"exact_closed_subbox":box,"direct_C0_interval":str(dual[0]),"direct_C0_sign":direct_sign,"centered_C0_interval":str(center),"centered_C0_sign":center_sign,"selected_sign":selected});continue
   need(dp+ds<16,"full face depth");axis=1 if dp<=ds else 2;i=axis*2;mid=(Q(box[i])+Q(box[i+1]))/2;left=list(box);right=list(box);left[i+1]=str(mid);right[i]=str(mid);stack.append((right,dp+(axis==1),ds+(axis==2)));stack.append((left,dp+(axis==1),ds+(axis==2)))
  cells.sort(key=lambda r:c(r["exact_closed_subbox"]));faces.append({"face_side":side,"strict_active_factor_sign":overall,"subdivision_leaf_count":len(cells),"subdivision_certificate_rows":cells,"subdivision_certificate_rows_sha256":h(cells)})
 need({faces[0]["strict_active_factor_sign"],faces[1]["strict_active_factor_sign"]}==STRICT,"full face bracket");return{"kind":"FULL_BASE_UNIQUE_GRAPH_BY_OPPOSITE_T_FACE_SIGNS_AND_C21B_STRICT_T_DERIVATIVE","face_certificates":faces,"opposite_face_signs":True}
def build(q):
 ctx.prec=256
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 r173=envelope(R173);need(r173["outgoing_chart_contract"]["diagonal_seam_rule"]=="E or W owns; N or S excludes","R173");r208=envelope(R208);r211=envelope(R211);c21br=json.loads((ROOT/C21BR).read_bytes());need(c21br["result_sha256"]=="d51822cd828c6911f931b5d7cc96061a9d349407b038c23b31e2924d0fbee51f","C21b result");c21b=c21b_index();leaves={r["leaf_row_id"]:r for r in r208["formal_leaf_geometry_ledger"]["rows"]};regions={r["region_row_id"]:r for r in r208["formal_local_open_3D_signature_ledger"]["rows"]};supports={r["member_id"]:r for r in rows(ROOT/C20)if r["fine_family"]=="ROUND208_REGION"};sheets={r["sheet_row_id"]:r for r in r211["formal_2D_sheet_owner_ledger"]["rows"]};curves=sorted(r211["formal_1D_curve_incidence_owner_ledger"]["rows"],key=lambda r:r["curve_row_id"].encode());curve_source={r["curve_row_id"]:r for r in curves};endpoints=sorted(r211["formal_0D_endpoint_incidence_owner_ledger"]["rows"],key=lambda r:r["endpoint_row_id"].encode());need(len(sheets)==len(c21b)==17716 and len(curves)==len(curve_source)==20456 and len(endpoints)==40912,"source census");curves_by_sheet=defaultdict(list);curve_rows={};edge_maps={};probe_curves={};mode_count=Counter();graph_signs=Counter();pair_count=Counter();provenance=Counter()
 for curve in curves:
  closed(curve,"R211 curve");sheet=sheets[curve["sheet_row_id"]];leaf=leaves[sheet["leaf_row_id"]];owner=regions[sheet["owner_region_row_id"]];shadow=regions[sheet["shadow_region_row_id"]];probe=probe_curve(curve,sheet,leaf,owner,shadow);need(curve["probe_curve_row_id"]==probe["curve_row_id"]and curve["probe_curve_row_sha256"]==probe["row_sha256"],"probe curve");theorem,edges,mode,graph_sign=curve_proof(sheet,leaf,curve,owner,c21b[sheet["sheet_row_id"]]);body={"schema":"cm2.round306c21c.source-g-79084-r211-A1-A2-incidence-closure.v1.row.v1","obligation_kind":"A2_R211_OWNER_CURVE","feature_row_id":curve["curve_row_id"],"R211_sheet_row_id":sheet["sheet_row_id"],"owner_member_id":sheet["owner_region_row_id"],"owner_fresh_component_id":supports[sheet["owner_region_row_id"]]["fresh_component_id"],"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"reconstructed_R209_probe_curve_row_sha256":probe["row_sha256"],"R211_curve_owner_row_sha256":curve["row_sha256"],"C21b_sheet_theorem_row_sha256":c21b[sheet["sheet_row_id"]]["row_sha256"]},"formal_credit":{"A1":0,"A2":1},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};row={**body,"row_sha256":h(body)};curve_rows[curve["curve_row_id"]]=row;edge_maps[curve["curve_row_id"]]=edges;probe_curves[curve["curve_row_id"]]=probe;curves_by_sheet[sheet["sheet_row_id"]].append(row);mode_count[mode]+=1;graph_signs[graph_sign]+=1;pair_count[curve["boundary_edge_pair"]]+=1;provenance[curve["geometry_provenance"]]+=1
 endpoint_rows=[]
 for endpoint in endpoints:
  closed(endpoint,"R211 endpoint");curve=curve_source[endpoint["curve_row_id"]];probe=probe_endpoint(endpoint,probe_curves[curve["curve_row_id"]]);need(endpoint["probe_endpoint_row_id"]==probe["endpoint_row_id"]and endpoint["probe_endpoint_row_sha256"]==probe["row_sha256"],"probe endpoint");edge=edge_maps[curve["curve_row_id"]][endpoint["boundary_edge"]];need(edge["disposition"]=="UNIQUE_BRACKETED_ZERO"and curve["boundary_edge_pair"].split("|")[endpoint["endpoint_ordinal"]-1]==endpoint["boundary_edge"],"endpoint theorem");theorem={"kind":"A2_UNIQUE_ALGEBRAIC_BOUNDARY_ENDPOINT","curve_theorem_row_sha256":curve_rows[curve["curve_row_id"]]["row_sha256"],"curve_theorem_ast_sha256":curve_rows[curve["curve_row_id"]]["theorem_ast_sha256"],"endpoint_ordinal":endpoint["endpoint_ordinal"],"boundary_edge":endpoint["boundary_edge"],"edge_evidence_sha256":h(edge),"endpoint_exists_and_is_unique":True,"uniqueness_authority":"STRICT_TANGENT_DERIVATIVE_PLUS_OPPOSITE_STRICT_CORNER_SIGNS"};sheet=sheets[curve["sheet_row_id"]];body={"schema":"cm2.round306c21c.source-g-79084-r211-A1-A2-incidence-closure.v1.row.v1","obligation_kind":"A2_R211_OWNER_ENDPOINT","feature_row_id":endpoint["endpoint_row_id"],"R211_sheet_row_id":sheet["sheet_row_id"],"R211_curve_row_id":curve["curve_row_id"],"owner_member_id":sheet["owner_region_row_id"],"owner_fresh_component_id":supports[sheet["owner_region_row_id"]]["fresh_component_id"],"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"reconstructed_R209_probe_endpoint_row_sha256":probe["row_sha256"],"R211_endpoint_owner_row_sha256":endpoint["row_sha256"],"C21c_curve_theorem_row_sha256":curve_rows[curve["curve_row_id"]]["row_sha256"]},"formal_credit":{"A1":0,"A2":1},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};endpoint_rows.append({**body,"row_sha256":h(body)})
 a1_rows=[];class_count=Counter();full_cells=0
 for sheet_id in sorted(sheets,key=lambda x:x.encode()):
  sheet=sheets[sheet_id];closed(sheet,"sheet");leaf=leaves[sheet["leaf_row_id"]];owner=regions[sheet["owner_region_row_id"]];incident=sorted(curves_by_sheet[sheet_id],key=lambda r:r["feature_row_id"].encode());need(len(incident)==leaf["one_dimensional_clipping_curve_segment_count"],"sheet curve census")
  if leaf["final_graph_classification"]=="FULL_2D":need(not incident,"full incidence");existence=full_face_certificate(sheet,leaf,owner);full_cells+=sum(x["subdivision_leaf_count"]for x in existence["face_certificates"])
  else:need(leaf["final_graph_classification"]=="CLIPPED_2D_BOUNDARY_1D"and bool(incident),"clipped incidence");existence={"kind":"CLIPPED_REGULAR_SHEET_WITH_EXHAUSTIVE_VERIFIED_T_FACE_BOUNDARY_CURVES","verified_boundary_curve_row_sha256s":[r["row_sha256"]for r in incident],"boundary_curve_count":len(incident),"endpoint_count":2*len(incident),"C21b_strict_t_derivative_plus_A2_boundary_curves_implies_nonempty_regular_sheet":True}
  theorem={"kind":"A1_R211_REGULAR_ACTIVE_FACTOR_ZERO_SHEET_DISCHARGE","C21b_sheet_theorem_row_sha256":c21b[sheet_id]["row_sha256"],"C21b_sheet_theorem_ast_sha256":c21b[sheet_id]["theorem_ast_sha256"],"leaf_classification":leaf["final_graph_classification"],"existence_and_boundary_closure":existence,"all_R211_curve_obligations_exhausted":True,"all_incident_curve_endpoints_exhausted":True};body={"schema":"cm2.round306c21c.source-g-79084-r211-A1-A2-incidence-closure.v1.row.v1","obligation_kind":"A1_R211_OWNER_SHEET","feature_row_id":sheet_id,"owner_member_id":sheet["owner_region_row_id"],"owner_fresh_component_id":supports[sheet["owner_region_row_id"]]["fresh_component_id"],"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"R211_sheet_owner_row_sha256":sheet["row_sha256"],"C21b_sheet_theorem_row_sha256":c21b[sheet_id]["row_sha256"]},"formal_credit":{"A1":1,"A2":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};a1_rows.append({**body,"row_sha256":h(body)});class_count[leaf["final_graph_classification"]]+=1
 all_rows=[*a1_rows,*curve_rows.values(),*endpoint_rows];all_rows.sort(key=lambda r:(r["obligation_kind"].encode(),r["feature_row_id"].encode()));q.mkdir(parents=True,exist_ok=True)
 with(q/L).open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as gz:
   for row in all_rows:gz.write(c(row)+b"\n")
 need(len(all_rows)==79084 and mode_count=={"DIRECT_TPS":20200,"STEREOGRAPHIC_TUS":256}and graph_signs=={"STRICT_NEGATIVE":10228,"STRICT_POSITIVE":10228}and pair_count=={"E|N":3959,"E|S":3959,"N|S":4620,"N|W":3959,"S|W":3959}and provenance=={"ROUND182_FULL_BASE_UNIQUE_GRAPH_FACE":3252,"ROUND186_ONE_ACTIVE_FACTOR_FULL_GRAPH":1104,"ROUND188_UNIQUE_TWO_ENDPOINT_FACTOR_CURVE":15844,"ROUND191_UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE":256}and class_count=={"CLIPPED_2D_BOUNDARY_1D":17308,"FULL_2D":408},"final census");desc={"filename":L,"row_count":79084,"size":(q/L).stat().st_size,"sha256":fh(q/L)};body={"schema":"cm2.round306c21c.source-g-79084-r211-A1-A2-incidence-closure.v1","status":"PASS_ALL_79084_R211_A1_A2_OBLIGATIONS__PRESERVED_SEMANTIC_KERNEL_CLOSED","A1_credit":17716,"A2_curve_credit":20456,"A2_endpoint_credit":40912,"total_A1_A2_credit":79084,"remaining_preserved_A1_A2_obligation_debt":0,"PRESERVED_semantic_kernel_closed":True,"curve_proof_chart_census":dict(mode_count),"curve_graph_derivative_sign_census":dict(graph_signs),"curve_boundary_pair_census":dict(pair_count),"curve_provenance_census":dict(provenance),"sheet_classification_census":dict(class_count),"full_sheet_subdivision_certificate_leaf_count":full_cells,"cumulative_member_support_credit":182072,"remaining_global_member_support_debt":320132,"input_pins":[{"filename":n,"sha256":x}for n,x in sorted(PINS.items())],"ledger":desc,"strict_nonpromotion":{"new_DSU_edges":0,"new_DSU_unions":0,"typed_global_support_ledger":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**body,"result_sha256":h(body)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
