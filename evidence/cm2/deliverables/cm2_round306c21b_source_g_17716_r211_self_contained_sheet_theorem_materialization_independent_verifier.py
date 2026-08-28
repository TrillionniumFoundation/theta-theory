#!/usr/bin/env python3
from __future__ import annotations
import argparse,gzip,hashlib,json,sys
from collections import Counter
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
def source_rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"source newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"source canonical");closed(r,"source closure");yield r
def ledger_rows(q):
 with gzip.open(q,"rb")as f:
  for line in f:
   need(line.endswith(b"\n"),"ledger newline");raw=line[:-1];r=json.loads(raw);need(c(r)==raw,"ledger canonical");closed(r,"ledger closure");yield r
def K(v):return{"op":"RAT","value":str(Q(v))}
def V(v):return{"op":"VAR","name":v}
def kr(v,q=None):return v["op"]=="RAT"and(q is None or Q(v["value"])==Q(q))
def N(v):
 if kr(v):return K(-Q(v["value"]))
 if v["op"]=="NEG":return v["arg"]
 return{"op":"NEG","arg":v}
def A(a,b):
 if kr(a,0):return b
 if kr(b,0):return a
 if kr(a)and kr(b):return K(Q(a["value"])+Q(b["value"]))
 return{"op":"ADD","left":a,"right":b}
def S(a,b):return A(a,N(b))
def M(a,b):
 if kr(a,0)or kr(b,0):return K(0)
 if kr(a,1):return b
 if kr(b,1):return a
 if kr(a,-1):return N(b)
 if kr(b,-1):return N(a)
 if kr(a)and kr(b):return K(Q(a["value"])*Q(b["value"]))
 return{"op":"MUL","left":a,"right":b}
def D(a,b):
 if kr(a,0):return K(0)
 if kr(b,1):return a
 if kr(a)and kr(b):return K(Q(a["value"])/Q(b["value"]))
 return{"op":"DIV","numerator":a,"denominator":b}
def SQ(a):return{"op":"SQRT","arg":a}
def derivative(v,name,memo=None):
 if memo is None:memo={}
 key=id(v)
 if key in memo:return memo[key]
 op=v["op"]
 if op=="RAT":z=K(0)
 elif op=="VAR":z=K(v["name"]==name)
 elif op=="NEG":z=N(derivative(v["arg"],name,memo))
 elif op=="ADD":z=A(derivative(v["left"],name,memo),derivative(v["right"],name,memo))
 elif op=="MUL":z=A(M(derivative(v["left"],name,memo),v["right"]),M(v["left"],derivative(v["right"],name,memo)))
 elif op=="DIV":z=D(S(M(derivative(v["numerator"],name,memo),v["denominator"]),M(v["numerator"],derivative(v["denominator"],name,memo))),M(v["denominator"],v["denominator"]))
 elif op=="SQRT":z=D(derivative(v["arg"],name,memo),M(K(2),SQ(v["arg"])))
 else:raise E("unknown AST")
 memo[key]=z;return z
def aq(v):v=Q(v);return arb(v.numerator)/v.denominator
def hull(a,b):
 a,b=Q(a),Q(b);need(a<=b,"hull");m=(a+b)/2;r=(b-a)/2;return aq(m)+arb(0,aq(r).upper())
def sg(v):return"STRICT_POSITIVE"if bool(v>0)else"STRICT_NEGATIVE"if bool(v<0)else"OVERWRAP"
def scalar(v,env,memo=None,roots=None):
 if memo is None:memo={}
 if roots is None:roots=set()
 key=id(v)
 if key in memo:return memo[key]
 op=v["op"]
 if op=="RAT":z=aq(v["value"])
 elif op=="VAR":z=env[v["name"]]
 elif op=="NEG":z=-scalar(v["arg"],env,memo,roots)
 elif op=="ADD":z=scalar(v["left"],env,memo,roots)+scalar(v["right"],env,memo,roots)
 elif op=="MUL":z=scalar(v["left"],env,memo,roots)*scalar(v["right"],env,memo,roots)
 elif op=="DIV":z=scalar(v["numerator"],env,memo,roots)/scalar(v["denominator"],env,memo,roots)
 elif op=="SQRT":
  a=scalar(v["arg"],env,memo,roots);need(bool(a>0),"sqrt positivity");roots.add(key);z=a.sqrt()
 else:raise E("scalar AST")
 memo[key]=z;return z
def dual(v,env,memo=None):
 if memo is None:memo={}
 key=id(v)
 if key in memo:return memo[key]
 op=v["op"]
 if op=="RAT":z=(aq(v["value"]),arb(0))
 elif op=="VAR":z=(env[v["name"]],arb(v["name"]=="t"))
 elif op=="NEG":
  a=dual(v["arg"],env,memo);z=(-a[0],-a[1])
 elif op=="ADD":
  a=dual(v["left"],env,memo);b=dual(v["right"],env,memo);z=(a[0]+b[0],a[1]+b[1])
 elif op=="MUL":
  a=dual(v["left"],env,memo);b=dual(v["right"],env,memo);z=(a[0]*b[0],a[1]*b[0]+a[0]*b[1])
 elif op=="DIV":
  a=dual(v["numerator"],env,memo);b=dual(v["denominator"],env,memo);z=(a[0]/b[0],(a[1]*b[0]-a[0]*b[1])/(b[0]*b[0]))
 elif op=="SQRT":
  a=dual(v["arg"],env,memo);need(bool(a[0]>0),"dual sqrt");root=a[0].sqrt();z=(root,a[1]/(2*root))
 else:raise E("dual AST")
 memo[key]=z;return z
def target(v):need(v.startswith("W[")and v.endswith("]"),"target");a,b=v[2:-1].split(",");return int(a),int(b)
def expressions(chart,lift,sigma=None):
 t=V("t");s=V("s");one=K(1);rt=SQ(S(one,M(t,t)))
 if sigma is None:p=V("p");rp=SQ(S(one,M(p,p)));mapping={"kind":"IDENTITY_TPS","coordinates":["t","p","s"]}
 else:
  u=V("u");u2=M(u,u);den=A(one,u2);p=M(K(sigma),D(S(one,u2),den));rp=D(M(K(2),u),den);mapping={"kind":"RATIONAL_STEREOGRAPHIC_P_ENDPOINT_CHART","coordinates":["t","u","s"],"sigma":sigma,"p_of_u_ast":p,"sqrt_one_minus_p_squared_of_u_ast":rp,"exact_unit_circle_identity":True}
 cell=chart.split(":")[1];need(cell in{"E","W","N","S"},"cell")
 if cell=="E":nx,ny=rt,t
 elif cell=="W":nx,ny=N(rt),t
 elif cell=="N":nx,ny=t,rt
 else:nx,ny=t,N(rt)
 ux=S(M(rp,nx),M(p,ny));uy=A(M(rp,ny),M(p,nx));sx=M(K(Q(9,25)),nx);sy=M(K(Q(9,25)),ny);ix,iy=target(lift);cx=A(K(Q(ix)+Q(1,2)),s);cy=K(Q(iy)+Q(1,2));dx=S(cx,sx);dy=S(cy,sy);tr=A(N(M(uy,dx)),M(ux,dy));rad=SQ(S(K(Q(16,625)),M(tr,tr)));ox=D(A(N(M(rad,ux)),M(tr,uy)),K(Q(4,25)));oy=D(S(N(M(rad,uy)),M(tr,ux)),K(Q(4,25)));return{"HPLUS":A(ox,oy),"HMINUS":S(ox,oy),"NX":ox,"NY":oy,"coordinate_map":mapping}
def sqrt_cover(v,bits=192):
 v=Q(v);d=1<<bits;n=v.numerator<<(2*bits);r=isqrt(n//v.denominator)
 while r*r*v.denominator<n:r+=1
 while r and(r-1)*(r-1)*v.denominator>=n:r-=1
 z=Q(r,d);need(z*z>=v,"sqrt cover");return z
def core(v):return{k:x for k,x in v.items()if k not in{"outgoing_cell","target_chart"}}
def probe(sheet,leaf,owner,shadow):
 cr=core(owner["local_return_signature"]);need(cr==core(shadow["local_return_signature"]),"core");cs=h(cr);identity={"leaf_row_id":leaf["leaf_row_id"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"rule":"E_OR_W_OWNS__N_OR_S_SHADOWS"};pid="round209-half-open-sheet:"+h(identity);relation="HMINUS=2*Nx_ON_HPLUS_ZERO_SHEET"if sheet["active_factor"]=="HPLUS"else"HPLUS=2*Nx_ON_HMINUS_ZERO_SHEET";body={"sheet_row_id":pid,"leaf_row_id":leaf["leaf_row_id"],"origin_row_id":leaf["origin_row_id"],"occurrence_row_id":leaf["occurrence_row_id"],"retained_child_row_id":leaf["retained_child_row_id"],"leaf_classification":leaf["final_graph_classification"],"active_factor":sheet["active_factor"],"inactive_factor":sheet["inactive_factor"],"inactive_factor_whole_box_C0_proof":"DIRECT_WHOLE_BOX_C0","inactive_factor_whole_box_strict_sign":sheet["inactive_factor_whole_box_strict_sign"],"factor_identity_on_sheet":relation,"Nx_sign_on_sheet":sheet["inactive_factor_whole_box_strict_sign"],"owner_region_row_id":owner["region_row_id"],"shadow_region_row_id":shadow["region_row_id"],"owner_outgoing_cell":owner["outgoing_cell"],"shadow_outgoing_cell":shadow["outgoing_cell"],"owner_signature_core_sha256":cs,"shadow_signature_core_sha256":cs,"signature_difference_field_allowlist":["outgoing_cell","target_chart"],"Round173_half_open_rule":"E or W owns; N or S excludes","deterministic_unique_owner_lineage":True,"incidence_is_not_a_global_component":True,"formal_half_open_owner_credit":0,"whole_original_tube_credit":0,"global_exact_key_disposition_credit":0};return{**body,"row_sha256":h(body)}
def envelope(name):
 d=json.loads((ROOT/name).read_bytes());need(set(d)=={"schema","result","result_sha256"}and d["result_sha256"]==h(d["result"]),"envelope");return d["result"]
def verify(q):
 ctx.prec=256
 for n,x in PINS.items():need(fh(ROOT/n)==x,"pin:"+n)
 raw=(q/R).read_bytes();z=json.loads(raw);need(c(z)==raw,"result canonical");body=dict(z);claimed=body.pop("result_sha256");need(claimed==h(body),"result closure");need(z["status"]=="PASS_17716_R211_SELF_CONTAINED_SHEET_THEOREM_MATERIALIZATIONS__A1_CREDIT_DEFERRED"and(z["sheet_theorem_materialization_credit"],z["A1_obligation_discharge_credit"],z["remaining_preserved_A1_A2_obligation_debt"],z["ledger"]["row_count"])==(17716,0,79084,17716),"result census");need(z["proof_chart_census"]=={"DIRECT_TPS":17460,"STEREOGRAPHIC_TUS":256}and z["active_factor_census"]=={"HMINUS":8858,"HPLUS":8858}and z["active_factor_t_derivative_sign_census"]=={"STRICT_NEGATIVE":5814,"STRICT_POSITIVE":11902}and z["inactive_factor_sign_census"]=={"STRICT_NEGATIVE":8858,"STRICT_POSITIVE":8858},"proof census");need(z["leaf_classification_census"]=={"CLIPPED_2D_BOUNDARY_1D":17308,"FULL_2D":408}and z["owner_cell_census"]=={"E":8858,"W":8858}and z["symbolic_differentiation_rules_sha256"]==h(RULES),"geometry census");need(z["input_pins"]==[{"filename":n,"sha256":x}for n,x in sorted(PINS.items())]and z["strict_nonpromotion"]=={"new_DSU_edges":0,"new_DSU_unions":0,"A1":0,"A2":0,"B1A":0,"B2":0,"maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"boundary");need(fh(q/L)==z["ledger"]["sha256"]and(q/L).stat().st_size==z["ledger"]["size"],"descriptor")
 r173=envelope(R173);need(r173["outgoing_chart_contract"]["diagonal_seam_rule"]=="E or W owns; N or S excludes","R173");r208=envelope(R208);r211=envelope(R211);leaves={r["leaf_row_id"]:r for r in r208["formal_leaf_geometry_ledger"]["rows"]};regions={r["region_row_id"]:r for r in r208["formal_local_open_3D_signature_ledger"]["rows"]};supports={r["member_id"]:r for r in source_rows(ROOT/C20)if r["fine_family"]=="ROUND208_REGION"};need(len(leaves)==18324 and len(regions)==len(supports)==36040,"inputs");sheets=sorted(r211["formal_2D_sheet_owner_ledger"]["rows"],key=lambda r:r["sheet_row_id"].encode());need(len(sheets)==17716,"sheets");cache={};counts=Counter();seen=0
 iterator=ledger_rows(q/L)
 for ordinal,sheet in enumerate(sheets):
  row=next(iterator,None);need(row is not None and row["ordinal"]==ordinal,"ledger order");closed(sheet,"sheet");leaf=leaves[sheet["leaf_row_id"]];owner=regions[sheet["owner_region_row_id"]];shadow=regions[sheet["shadow_region_row_id"]];closed(leaf,"leaf");closed(owner,"owner");closed(shadow,"shadow");need(owner["leaf_row_id"]==leaf["leaf_row_id"]==shadow["leaf_row_id"]and owner["F_sign"]=="STRICT_POSITIVE"and shadow["F_sign"]=="STRICT_NEGATIVE","pair");reprobe=probe(sheet,leaf,owner,shadow);need(sheet["probe_sheet_row_id"]==reprobe["sheet_row_id"]and sheet["probe_sheet_row_sha256"]==reprobe["row_sha256"],"probe");os=supports[owner["region_row_id"]];ss=supports[shadow["region_row_id"]];chart=owner["local_return_signature"]["source_chart"];lift=owner["local_return_signature"]["target_lift"];need(os["support_ast"]==ss["support_ast"]and os["support_ast"]["bounds"]==leaf["box"]and os["support_ast"]["coordinate_chart"]==chart,"support")
  box=leaf["box"];left,right=Q(box[2]),Q(box[3]);endpoint=left==-1 or right==1;sigma=(-1 if left==-1 else 1)if endpoint else None;key=(chart,lift,sheet["active_factor"],sigma)
  if key not in cache:
   fs=expressions(chart,lift,sigma);active=fs[sheet["active_factor"]];inactive=fs[sheet["inactive_factor"]];cache[key]=(fs,active,inactive,derivative(active,"t"))
  fs,active,inactive,dt=cache[key]
  if sigma is None:env={"t":hull(box[0],box[1]),"p":hull(box[2],box[3]),"s":hull(box[4],box[5])};mode="DIRECT_TPS";proof_chart={"kind":"DIRECT_TPS","coordinates":["t","p","s"],"closed_interval_hull":box}
  else:
   inner=right if sigma==-1 else left;um2=(1-sigma*inner)/(1+sigma*inner);upper=sqrt_cover(um2);env={"t":hull(box[0],box[1]),"u":hull(0,upper),"s":hull(box[4],box[5])};mode="STEREOGRAPHIC_TUS";proof_chart={**fs["coordinate_map"],"physical_p_endpoint":str(Q(sigma)),"physical_p_inner":str(inner),"exact_u_max_squared":str(um2),"exact_u_domain":"0<=u<=sqrt(exact_u_max_squared)","interval_proof_u_upper_dyadic":str(upper),"closed_interval_hull":[box[0],box[1],"0",str(upper),box[4],box[5]]}
  roots=set();dt_value=scalar(dt,env,{},roots);inactive_value=scalar(inactive,env,{},roots);dt_sign=sg(dt_value);inactive_sign=sg(inactive_value);active_dual=dual(active,env);need(dt_sign in STRICT and inactive_sign==sheet["inactive_factor_whole_box_strict_sign"]and sg(active_dual[1])==dt_sign and bool(active_dual[1].overlaps(dt_value)),"independent derivative crosscheck");theorem={"kind":"SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET","physical_source_chart":chart,"target_lift":lift,"exact_open_leaf_box":box,"proof_coordinate_chart":proof_chart,"active_factor":sheet["active_factor"],"inactive_factor":sheet["inactive_factor"],"active_factor_equation_ast":active,"active_factor_equation_ast_sha256":h(active),"inactive_factor_ast":inactive,"inactive_factor_ast_sha256":h(inactive),"active_factor_t_derivative_ast":dt,"active_factor_t_derivative_ast_sha256":h(dt),"symbolic_differentiation":{"variable":"t","rules":RULES,"rules_sha256":h(RULES),"producer_imported_upstream_evaluator":False},"interval_proof":{"arb_precision_bits":256,"active_factor_t_derivative_interval":str(dt_value),"active_factor_t_derivative_sign":dt_sign,"inactive_factor_interval":str(inactive_value),"inactive_factor_sign":inactive_sign,"all_encountered_sqrt_radicands_strict_positive":True,"encountered_sqrt_node_count":len(roots)},"exact_factorization_identity":"F=HPLUS*HMINUS=NX^2-NY^2","exact_identity_on_active_sheet":sheet["factor_identity_on_sheet"],"regular_zero_sheet_where_nonempty":True,"R208_nonempty_leaf_classification":leaf["final_graph_classification"],"A1_obligation_discharge_deferred_until_A2_boundary_incidence_closure":True};body={"schema":"cm2.round306c21b.source-g-17716-r211-self-contained-sheet-theorem-materialization.v1.row.v1","ordinal":ordinal,"R211_sheet_row_id":sheet["sheet_row_id"],"leaf_row_id":leaf["leaf_row_id"],"owner_member_id":owner["region_row_id"],"shadow_member_id":shadow["region_row_id"],"owner_fresh_component_id":os["fresh_component_id"],"shadow_fresh_component_id":ss["fresh_component_id"],"theorem_ast":theorem,"theorem_ast_sha256":h(theorem),"source_bindings":{"R208_leaf_row_sha256":leaf["row_sha256"],"R208_owner_region_row_sha256":owner["row_sha256"],"R208_shadow_region_row_sha256":shadow["row_sha256"],"reconstructed_R209_probe_sheet_row_sha256":reprobe["row_sha256"],"R211_sheet_owner_row_sha256":sheet["row_sha256"],"C20a_owner_support_ast_sha256":os["support_ast_sha256"],"C20a_shadow_support_ast_sha256":ss["support_ast_sha256"]},"formal_credit":{"self_contained_sheet_theorem_materialization":1,"A1_obligation_discharge":0,"A2_obligation_discharge":0},"strict_nonpromotion":{"DSU_edge":0,"DSU_union":0,"B1A":0,"B2":0,"maximality":0,"CM2":0}};expected={**body,"row_sha256":h(body)};need(row==expected,"full independent row reconstruction");counts[(mode,sheet["active_factor"],dt_sign,inactive_sign,leaf["final_graph_classification"],owner["outgoing_cell"])]+=1;seen+=1
 need(next(iterator,None)is None and seen==17716,"ledger exhaustion");return{"status":"PASS_INDEPENDENT_C21B_17716_SELF_CONTAINED_SHEET_THEOREMS__SYMBOLIC_DIFF_AND_DUAL_CROSSCHECK","result_sha256":claimed,"rows":seen,"joint_census_sha256":h(sorted((list(k),v)for k,v in counts.items()))}
def main():
 need(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"flags");p=argparse.ArgumentParser();p.add_argument("--candidate-dir");a=p.parse_args();q=ROOT if a.candidate_dir is None else Path(a.candidate_dir).resolve();print(c(verify(q)).decode());return 0
if __name__=="__main__":raise SystemExit(main())
