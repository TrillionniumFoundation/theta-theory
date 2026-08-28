#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
from flint import arb,ctx
ROOT=Path(__file__).resolve().parent;P="cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization";L=P+"_ledger.jsonl.gz";R=P+"_result.json";R173="cm2_round173_source_g_exact_return_signature_transport_certificate.json";R208="cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json";R211="cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json";C20="cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz";PINS={R173:"5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",R208:"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",R211:"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f",C20:"bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"};STRICT={"STRICT_NEGATIVE","STRICT_POSITIVE"};RULES=["D(c)=0","D(x)=1","D(-a)=-D(a)","D(a+b)=D(a)+D(b)","D(a*b)=D(a)*b+a*D(b)","D(a/b)=(D(a)*b-a*D(b))/(b*b)","D(sqrt(a))=D(a)/(2*sqrt(a))"]
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
def rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"canonical");closed(r,"row closure");yield r
def rat(v):return{"op":"RAT","value":str(Q(v))}
def var(v):return{"op":"VAR","name":v}
def israt(v,q=None):return v["op"]=="RAT"and(q is None or Q(v["value"])==Q(q))
def neg(v):
 if israt(v):return rat(-Q(v["value"]))
 if v["op"]=="NEG":return v["arg"]
 return{"op":"NEG","arg":v}
def add(a,b):
 if israt(a,0):return b
 if israt(b,0):return a
 if israt(a)and israt(b):return rat(Q(a["value"])+Q(b["value"]))
 return{"op":"ADD","left":a,"right":b}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 if israt(a,0)or israt(b,0):return rat(0)
 if israt(a,1):return b
 if israt(b,1):return a
 if israt(a,-1):return neg(b)
 if israt(b,-1):return neg(a)
 if israt(a)and israt(b):return rat(Q(a["value"])*Q(b["value"]))
 return{"op":"MUL","left":a,"right":b}
def div(a,b):
 if israt(a,0):return rat(0)
 if israt(b,1):return a
 if israt(a)and israt(b):return rat(Q(a["value"])/Q(b["value"]))
 return{"op":"DIV","numerator":a,"denominator":b}
def sqrt(a):return{"op":"SQRT","arg":a}
def diff(v,name,memo=None):
 if memo is None:memo={}
 key=id(v)
 if key in memo:return memo[key]
 op=v["op"]
 if op=="RAT":z=rat(0)
 elif op=="VAR":z=rat(v["name"]==name)
 elif op=="NEG":z=neg(diff(v["arg"],name,memo))
 elif op=="ADD":z=add(diff(v["left"],name,memo),diff(v["right"],name,memo))
 elif op=="MUL":z=add(mul(diff(v["left"],name,memo),v["right"]),mul(v["left"],diff(v["right"],name,memo)))
 elif op=="DIV":z=div(sub(mul(diff(v["numerator"],name,memo),v["denominator"]),mul(v["numerator"],diff(v["denominator"],name,memo))),mul(v["denominator"],v["denominator"]))
 elif op=="SQRT":z=div(diff(v["arg"],name,memo),mul(rat(2),sqrt(v["arg"])))
 else:raise E("AST op")
 memo[key]=z;return z
def aq(v):v=Q(v);return arb(v.numerator)/v.denominator
def interval(a,b):
 a,b=Q(a),Q(b);need(a<=b,"interval order");m=(a+b)/2;r=(b-a)/2;return aq(m)+arb(0,aq(r).upper())
def sign(v):return"STRICT_POSITIVE"if bool(v>0)else"STRICT_NEGATIVE"if bool(v<0)else"OVERWRAP"
def evaluate(v,env,memo=None,roots=None):
 if memo is None:memo={}
 if roots is None:roots=set()
 key=id(v)
 if key in memo:return memo[key]
 op=v["op"]
 if op=="RAT":z=aq(v["value"])
 elif op=="VAR":z=env[v["name"]]
 elif op=="NEG":z=-evaluate(v["arg"],env,memo,roots)
 elif op=="ADD":z=evaluate(v["left"],env,memo,roots)+evaluate(v["right"],env,memo,roots)
 elif op=="MUL":z=evaluate(v["left"],env,memo,roots)*evaluate(v["right"],env,memo,roots)
 elif op=="DIV":z=evaluate(v["numerator"],env,memo,roots)/evaluate(v["denominator"],env,memo,roots)
 elif op=="SQRT":
  q=evaluate(v["arg"],env,memo,roots);need(bool(q>0),"sqrt radicand");roots.add(key);z=q.sqrt()
 else:raise E("eval op")
 memo[key]=z;return z
def parse_target(v):
 need(v.startswith("W[")and v.endswith("]"),"target");a,b=v[2:-1].split(",");return int(a),int(b)
def formula(chart,target,sigma=None):
 t=var("t");s=var("s");one=rat(1);rt=sqrt(sub(one,mul(t,t)))
 if sigma is None:p=var("p");rp=sqrt(sub(one,mul(p,p)));coordinate_map={"kind":"IDENTITY_TPS","coordinates":["t","p","s"]}
 else:
  u=var("u");u2=mul(u,u);den=add(one,u2);p=mul(rat(sigma),div(sub(one,u2),den));rp=div(mul(rat(2),u),den);coordinate_map={"kind":"RATIONAL_STEREOGRAPHIC_P_ENDPOINT_CHART","coordinates":["t","u","s"],"sigma":sigma,"p_of_u_ast":p,"sqrt_one_minus_p_squared_of_u_ast":rp,"exact_unit_circle_identity":True}
 cell=chart.split(":")[1];need(cell in{"E","W","N","S"},"chart")
 if cell=="E":nx,ny=rt,t
 elif cell=="W":nx,ny=neg(rt),t
 elif cell=="N":nx,ny=t,rt
 else:nx,ny=t,neg(rt)
 ux=sub(mul(rp,nx),mul(p,ny));uy=add(mul(rp,ny),mul(p,nx));source_x=mul(rat(Q(9,25)),nx);source_y=mul(rat(Q(9,25)),ny);ix,iy=parse_target(target);cx=add(rat(Q(ix)+Q(1,2)),s);cy=rat(Q(iy)+Q(1,2));dx=sub(cx,source_x);dy=sub(cy,source_y);transverse=add(neg(mul(uy,dx)),mul(ux,dy));radical=sqrt(sub(rat(Q(16,625)),mul(transverse,transverse)));out_x=div(add(neg(mul(radical,ux)),mul(transverse,uy)),rat(Q(4,25)));out_y=div(sub(neg(mul(radical,uy)),mul(transverse,ux)),rat(Q(4,25)));return{"HPLUS":add(out_x,out_y),"HMINUS":sub(out_x,out_y),"NX":out_x,"NY":out_y,"coordinate_map":coordinate_map}
def sqrt_upper(v,bits=192):
 v=Q(v);need(v>0,"sqrt upper");d=1<<bits;n=v.numerator<<(2*bits);r=isqrt(n//v.denominator)
 while r*r*v.denominator<n:r+=1
 while r and(r-1)*(r-1)*v.denominator>=n:r-=1
 z=Q(r,d);need(z*z>=v,"sqrt cover");return z
def signature_core(v):return{k:x for k,x in v.items()if k not in{"outgoing_cell","target_chart"}}
def probe_sheet(sheet,leaf,owner,shadow):
 core=signature_core(owner["local_return_signature"]);need(core==signature_core(shadow["local_return_signature"]),"signature core");core_sha=h(core);identity={"leaf_row_id":leaf["leaf_row_id"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"rule":"E_OR_W_OWNS__N_OR_S_SHADOWS"};probe_id="round209-half-open-sheet:"+h(identity);relation="HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"if sheet["active_factor"]=="HPLUS"else"HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET";body={"sheet_row_id":probe_id,"leaf_row_id":leaf["leaf_row_id"],"origin_row_id":leaf["origin_row_id"],"occurrence_row_id":leaf["occurrence_row_id"],"retained_child_row_id":leaf["retained_child_row_id"],"leaf_classification":leaf["final_graph_classification"],"active_factor":sheet["active_factor"],"inactive_factor":sheet["inactive_factor"],"inactive_factor_whole_box_C0_proof":"DIRECT_WHOLE_BOX_C0","inactive_factor_whole_box_strict_sign":sheet["inactive_factor_whole_box_strict_sign"],"factor_identity_on_sheet":relation,"Nx_sign_on_sheet":sheet["inactive_factor_whole_box_strict_sign"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"owner_outgoing_cell":owner["outgoing_cell"],"shadow_outgoing_cell":shadow["outgoing_cell"],"owner_signature_core_sha256":core_sha,"shadow_signature_core_sha256":core_sha,"signature_difference_field_allowlist":["outgoing_cell","target_chart"],"Round173_half_open_rule":"E or W owns; N or S excludes","deterministic_unique_owner_lineage":True,"incidence_is_not_a_global_component":True,"formal_half_open_owner_credit":0,"whole_original_tube_credit":0,"global_exact_key_disposition_credit":0};return{**body,"row_sha256":h(body)}
def envelope(name):
 raw=(ROOT/name).read_bytes();d=json.loads(raw);need(set(d)=={"schema","result","result_sha256"}and d["result_sha256"]==h(d["result"]),"envelope:"+name);return d["result"]
def build(q):
 ctx.prec=256
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 r173=envelope(R173);need(r173["outgoing_chart_contract"]["diagonal_seam_rule"]=="E or W owns; N or S excludes","R173 rule");r208=envelope(R208);r211=envelope(R211);leaves={r["leaf_row_id"]:r for r in r208["formal_leaf_geometry_ledger"]["rows"]};regions={r["region_row_id"]:r for r in r208["formal_local_open_3D_signature_ledger"]["rows"]};supports={r["member_id"]:r for r in rows(ROOT/C20)if r["fine_family"]=="ROUND208_REGION"};need(len(leaves)==18324 and len(regions)==len(supports)==36040,"input census")
 for r in leaves.values():closed(r,"leaf")
 for r in regions.values():closed(r,"region")
 sheets=r211["formal_2D_sheet_owner_ledger"]["rows"];need(len(sheets)==17716 and len({r["sheet_row_id"]for r in sheets})==17716,"sheet census");cache={};mode_count=Counter();factor_count=Counter();derivative_count=Counter();inactive_count=Counter();class_count=Counter();owner_count=Counter();q.mkdir(parents=True,exist_ok=True)
 with(q/L).open("wb")as raw:
  with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0)as gz:
   for ordinal,sheet in enumerate(sorted(sheets,key=lambda r:r["sheet_row_id"].encode())):
    closed(sheet,"R211 sheet");leaf=leaves[sheet["leaf_row_id"]];owner=regions[sheet["owner_region_row_id"]];shadow=regions[sheet["shadow_region_row_id"]];need(owner["leaf_row_id"]==leaf["leaf_row_id"]==shadow["leaf_row_id"]and owner["F_sign"]=="STRICT_POSITIVE"and shadow["F_sign"]=="STRICT_NEGATIVE","region pair");need(owner["outgoing_cell"]in{"E","W"}and shadow["outgoing_cell"]in{"N","S"}and owner["inactive_factor"]==sheet["inactive_factor"]==shadow["inactive_factor"],"owner pair");probe=probe_sheet(sheet,leaf,owner,shadow);need(sheet["probe_sheet_row_id"]==probe["sheet_row_id"]and sheet["probe_sheet_row_sha256"]==probe["row_sha256"],"probe reconstruction");need(sheet["formal_half_open_owner_credit"]==1 and sheet["local_dimensional_owner_materialized"]is True and sheet["component_deduplication_credit"]==sheet["global_exact_key_disposition_credit"]==sheet["whole_leaf_credit"]==sheet["whole_origin_credit"]==sheet["whole_original_tube_credit"]==0,"R211 boundary")
    owner_support=supports[owner["region_row_id"]];shadow_support=supports[shadow["region_row_id"]];chart=owner["local_return_signature"]["source_chart"];target=owner["local_return_signature"]["target_lift"];need(signature_core(owner["local_return_signature"])==signature_core(shadow["local_return_signature"]),"signature equality");need(owner_support["support_ast"]==shadow_support["support_ast"]and owner_support["support_ast"]["bounds"]==leaf["box"]and owner_support["support_ast"]["coordinate_chart"]==chart,"support join")
    box=leaf["box"];left,right=Q(box[2]),Q(box[3]);endpoint=(left==-1)or(right==1);need(not(endpoint and left==-1 and right==1),"endpoint span");sigma=(-1 if left==-1 else 1)if endpoint else None;key=(chart,target,sheet["active_factor"],sigma)
    if key not in cache:
     factors=formula(chart,target,sigma);active=factors[sheet["active_factor"]];inactive=factors[sheet["inactive_factor"]];cache[key]=(factors,active,inactive,diff(active,"t"))
    factors,active_ast,inactive_ast,dt_ast=cache[key]
    if sigma is None:env={"t":interval(box[0],box[1]),"p":interval(box[2],box[3]),"s":interval(box[4],box[5])};mode="DIRECT_TPS";proof_chart={"kind":"DIRECT_TPS","coordinates":["t","p","s"],"closed_interval_hull":box}
    else:
     inner=right if sigma==-1 else left;um2=(1-sigma*inner)/(1+sigma*inner);upper=sqrt_upper(um2);env={"t":interval(box[0],box[1]),"u":interval(0,upper),"s":interval(box[4],box[5])};mode="STEREOGRAPHIC_TUS";proof_chart={**factors["coordinate_map"],"physical_p_endpoint":str(Q(sigma)),"physical_p_inner":str(inner),"exact_u_max_squared":str(um2),"exact_u_domain":"0<=u<=sqrt(exact_u_max_squared)","interval_proof_u_upper_dyadic":str(upper),"closed_interval_hull":[box[0],box[1],"0",str(upper),box[4],box[5]]}
    roots=set();dt_value=evaluate(dt_ast,env,{},roots);inactive_value=evaluate(inactive_ast,env,{},roots);dt_sign=sign(dt_value);inactive_sign=sign(inactive_value);need(dt_sign in STRICT and inactive_sign==sheet["inactive_factor_whole_box_strict_sign"],"independent interval theorem");need(sheet["factor_identity_on_sheet"]==("HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"if sheet["active_factor"]=="HPLUS"else"HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET"),"factor identity")
    theorem={"kind":"SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET","physical_source_chart":chart,"target_lift":target,"exact_open_leaf_box":box,"proof_coordinate_chart":proof_chart,"active_factor":sheet["active_factor"],"inactive_factor":sheet["inactive_factor"],"active_factor_equation_ast":active_ast,"active_factor_equation_ast_sha256":h(active_ast),"inactive_factor_ast":inactive_ast,"inactive_factor_ast_sha256":h(inactive_ast),"active_factor_t_derivative_ast":dt_ast,"active_factor_t_derivative_ast_sha256":h(dt_ast),"symbolic_differentiation":{"variable":"t","rules":RULES,"rules_sha256":h(RULES),"producer_imported_upstream_evaluator":False},"interval_proof":{"arb_precision_bits":256,"active_factor_t_derivative_interval":str(dt_value),"active_factor_t_derivative_sign":dt_sign,"inactive_factor_interval":str(inactive_value),"inactive_factor_sign":inactive_sign,"all_encountered_sqrt_radicands_strict_positive":True,"encountered_sqrt_node_count":len(roots)},"exact_factorization_identity":"F=HPLUS*HMINUS=NX^2-NY^2","exact_identity_on_active_sheet":sheet["factor_identity_on_sheet"],"regular_zero_sheet_where_nonempty":True,"R208_nonempty_leaf_classification":leaf["final_graph_classification"],"A1_obligation_discharge_deferred_until_A2_boundary_incidence_closure":True};body={"schema":"cm2.round306c21b.source-g-17716-r211-self-contained-sheet-theorem-materialization.v1.row.v1","ordinal":ordinal,"R211_sheet_row_id":sheet["sheet_row_id"],"leaf_row_id":leaf["leaf_row_id"],"owner_member_id":owner["region_row_id"],"shadow_member_id":shadow["region_row_id"],"owner_fresh_component_id":owner_support["fresh_component_id"],"shadow_fresh_component_id":shadow_support["fresh_component_id"],"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"R208_leaf_row_sha256":leaf["row_sha256"],"R208_owner_region_row_sha256":owner["row_sha256"],"R208_shadow_region_row_sha256":shadow["row_sha256"],"reconstructed_R209_probe_sheet_row_sha256":probe["row_sha256"],"R211_sheet_owner_row_sha256":sheet["row_sha256"],"C20a_owner_support_ast_sha256":owner_support["support_ast_sha256"],"C20a_shadow_support_ast_sha256":shadow_support["support_ast_sha256"]},"formal_credit":{"self_contained_sheet_theorem_materialization":1,"A1_obligation_discharge":0,"A2_obligation_discharge":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};row={**body,"row_sha256":h(body)};gz.write(c(row)+b"\n");mode_count[mode]+=1;factor_count[sheet["active_factor"]]+=1;derivative_count[dt_sign]+=1;inactive_count[inactive_sign]+=1;class_count[leaf["final_graph_classification"]]+=1;owner_count[owner["outgoing_cell"]]+=1
 desc={"filename":L,"row_count":17716,"size":(q/L).stat().st_size,"sha256":fh(q/L)};expected_mode={"DIRECT_TPS":17460,"STEREOGRAPHIC_TUS":256};need(mode_count==Counter(expected_mode)and factor_count=={"HPLUS":8858,"HMINUS":8858}and derivative_count=={"STRICT_NEGATIVE":5814,"STRICT_POSITIVE":11902}and inactive_count=={"STRICT_NEGATIVE":8858,"STRICT_POSITIVE":8858}and class_count=={"CLIPPED_2D_BOUNDARY_1D":17308,"FULL_2D":408}and owner_count=={"E":8858,"W":8858},"result census");body={"schema":"cm2.round306c21b.source-g-17716-r211-self-contained-sheet-theorem-materialization.v1","status":"PASS_17716_R211_SELF_CONTAINED_SHEET_THEOREM_MATERIALIZATIONS__A1_CREDIT_DEFERRED","sheet_theorem_materialization_credit":17716,"A1_obligation_discharge_credit":0,"remaining_preserved_A1_A2_obligation_debt":79084,"proof_chart_census":dict(mode_count),"active_factor_census":dict(factor_count),"active_factor_t_derivative_sign_census":dict(derivative_count),"inactive_factor_sign_census":dict(inactive_count),"leaf_classification_census":dict(class_count),"owner_cell_census":dict(owner_count),"symbolic_differentiation_rules_sha256":h(RULES),"input_pins":[{"filename":n,"sha256":x}for n,x in sorted(PINS.items())],"ledger":desc,"strict_nonpromotion":{"new_DSU_edges":0,"new_DSU_unions":0,"A1":0,"A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"}};z={**body,"result_sha256":h(body)};(q/R).write_bytes(c(z));return z
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidate-dir",required=True);a=p.parse_args();z=build(Path(a.candidate_dir).resolve());print(c({"status":z["status"],"result_sha256":z["result_sha256"]}).decode());return 0
if __name__=="__main__":raise SystemExit(main())
