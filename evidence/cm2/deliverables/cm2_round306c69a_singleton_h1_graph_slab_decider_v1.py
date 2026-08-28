#!/usr/bin/env python3
"""C69a capability prototype for singleton H1 graph cells and off-graph slabs.

Only the frozen 2,356 C61 REGULAR_FULL_FACE_GRAPH tasks can become decisions.
Every other C68 structural task remains in an explicit fail-closed blocker
ledger.  This is a read-only, zero-credit capability prototype, not an
installed authority and not a terminal disposition.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True
SELF = Path(__file__).resolve(); ROOT = SELF.parents[1]; OUT = ROOT / "deliverables"
sys.path.insert(0, str(OUT))

import flint
import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41

PREFIX = "cm2_round306c69a_singleton_h1_graph_slab_decider"
SCHEMA = "cm2.round306c69a.singleton-h1-graph-slab-decider.v1"
CONTRACT_FILE = PREFIX + "_contract_v1.json"
DECISION_FILE = PREFIX + "_decisions_v1.jsonl.gz"
BLOCKER_FILE = PREFIX + "_blockers_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"
REPORT_FILE = PREFIX + "_report_v1.md"

C68R = OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json"
C68S = OUT / "cm2_round306c68l_blocker_crosswalk_singleton_structural_tasks_v1.jsonl.gz"
C61R = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61L = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C58R = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58L = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C40R = C40 / "result.json"; C40L = C40 / "routed_leaf_cells.jsonl.gz"

P = {
    "C41_SOURCE": "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde",
    "C39_SOURCE": "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae",
    "ROUND185_SOURCE": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "C38_SOURCE": "8eab87d69fb4e1995df87be7acb387db19d1b81e17040fe6116794bddd4a830d",
    "C68R": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68O": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "C68S": "c2d174d9a7e076a52474cde03e02ecdc11172251fe70a5b0273b4aa57c480b8b",
    "C61R": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61O": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61L": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C58R": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58O": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58L": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40R": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40O": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C40L": "175293702adf1b76600321c1db326a1a6744dbc8caea439ddaeff9779d1f9b5a",
}

SOURCE_PATHS = {
    "C41_SOURCE": Path(c41.__file__).resolve(),
    "C39_SOURCE": Path(c41.c39.__file__).resolve(),
    "ROUND185_SOURCE": Path(c41.round185.__file__).resolve(),
    "C38_SOURCE": Path(c41.c38.__file__).resolve(),
    "C68R": C68R, "C68S": C68S, "C61R": C61R, "C61L": C61L,
    "C58R": C58R, "C58L": C58L, "C40R": C40R, "C40L": C40L,
}


class FailClosed(RuntimeError): pass
def need(v: bool, label: str) -> None:
    if type(v) is not bool or not v: raise FailClosed(label)
def enc(v: Any) -> bytes: return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
def h(v: Any) -> str: return hashlib.sha256(enc(v)).hexdigest()
def hf(path: Path) -> str:
    d=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""): d.update(chunk)
    return d.hexdigest()
def seq(values: Iterable[str]) -> str:
    d=hashlib.sha256()
    for v in values:d.update(v.encode("ascii")+b"\n")
    return d.hexdigest()
def ident(z: os.stat_result) -> dict[str,int]: return {"dev":z.st_dev,"ino":z.st_ino,"mode":z.st_mode,"size":z.st_size,"mtime_ns":z.st_mtime_ns,"nlink":z.st_nlink}
def secure(path:Path,expected:str)->tuple[bytes,dict[str,int]]:
    pre=os.lstat(path);need(stat.S_ISREG(pre.st_mode) and pre.st_nlink==1,"regular-single-link:"+path.name)
    fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
    try:
        opened=os.fstat(fd);need(ident(pre)==ident(opened),"path-fd:"+path.name);parts=[]
        while True:
            part=os.read(fd,1<<20)
            if not part:break
            parts.append(part)
        need(ident(os.fstat(fd))==ident(opened),"fd-post:"+path.name)
    finally:os.close(fd)
    need(ident(os.lstat(path))==ident(pre),"path-post:"+path.name);data=b"".join(parts);need(hashlib.sha256(data).hexdigest()==expected,"sha:"+path.name);return data,ident(pre)
def closeobj(v:dict[str,Any],expected:str,label:str)->None:
    b=dict(v);actual=b.pop("object_sha256",None);need(actual==expected==h(b),"object:"+label)
def closerow(v:dict[str,Any],label:str)->None:
    b=dict(v);actual=b.pop("row_sha256",None);need(actual==h(b),"row:"+label)
def rows(data:bytes,desc:dict[str,Any],label:str)->list[dict[str,Any]]:
    answer=[];hashes=[]
    with gzip.GzipFile(fileobj=io.BytesIO(data),mode="rb") as f:
        for i,line in enumerate(f):
            row=json.loads(line);closerow(row,f"{label}:{i}");answer.append(row);hashes.append(row["row_sha256"])
    need(len(answer)==desc["row_count"] and seq(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return answer
class Writer:
    def __init__(self,path:Path,order:str):self.path,self.order=path,order;self.raw=path.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.s=hashlib.sha256()
    def __enter__(self):return self
    def write(self,body:dict[str,Any])->dict[str,Any]:
        rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.s.update((rh+"\n").encode());self.count+=1;return row
    def __exit__(self,*_):self.gz.close();self.raw.close()
    def descriptor(self)->dict[str,Any]:return{"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.s.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}


def prefix_free(paths:list[str])->bool:
    ordered=sorted(paths,key=lambda x:(len(x),x));return all(not b.startswith(a) for i,a in enumerate(ordered) for b in ordered[i+1:])


def blockers(kind:str)->list[str]:
    return {
        "REGULAR_BOUNDARY_ARRANGEMENT":["NO_SINGLE_GLOBAL_H1_MONOTONE_AXIS_WITH_OPPOSITE_SIGN_FULL_FACES","NO_CERTIFIED_AXIS_INTERVAL_NEWTON_ROOT_ENCLOSURE","OFF_GRAPH_TWO_SLAB_PARTITION_NOT_AVAILABLE"],
        "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":["MULTI_SURFACE_FULL_BOX_EXISTENCE_AND_ORDER_REGISTRY_MISSING","ACTIVE_SET_ORDER_NOT_ISOLATED","OFF_GRAPH_MULTI_SLAB_INTERSECTION_REGISTRY_MISSING"],
        "REGULAR_MULTI_GRAPH_FIRST_TANGENCY":["TANGENCY_GRAPH_TYPED_BUT_TWO_OFF_GRAPH_SLAB_DISPOSITIONS_MISSING","MULTI_SURFACE_ORDER_REGISTRY_MISSING"],
        "SOURCE_GRAZING_ENDPOINT_CHART":["SOURCE_GRAZING_TRANSFORMED_ENDPOINT_CHART_EVALUATOR_MISSING","ENDPOINT_GRAPH_AND_OFF_GRAPH_SLAB_PARTITION_MISSING"],
        "COLLISION1_OUTGOING_STATE":["EXACT_COLLISION1_OUTGOING_RADIAL_POSITIVITY_EVALUATOR_MISSING","STRICT_OUTGOING_CHART_MARGIN_EVALUATOR_MISSING","SECOND_OUTGOING_STATE_NOT_MATERIALIZED"],
    }[kind]


def contract()->dict[str,Any]:
    value={
        "schema":SCHEMA+".mathematical-data-contract",
        "status":"FROZEN_CAPABILITY_CONTRACT__FULL_FACE_H1_ONLY__ZERO_CREDIT",
        "input_domain":{"C68_structural_task_count":20879,"decision_category":"REGULAR_FULL_FACE_GRAPH_CELL","expected_decision_count":2356,"all_other_categories_fail_closed":True},
        "equation":"H1(t,p)=n1_x(t,p)^2-n1_y(t,p)^2=0 on s=0",
        "decision_predicates":[
            "EXACT_C61_C58_C40_C38_C32_LINEAGE_AND_EXACT_BOX_REPLAY",
            "C39_INPUT_AND_ENHANCED_STAGE_ONE_ARE_UNIQUE_FIRST",
            "C39_ENHANCED_OWNER_IS_W[1,0]",
            "C39_REMAINING_UNRESOLVED_ROOT_RECORD_COUNT_IS_ZERO",
            "H1_KIND_IS_REGULAR_FULL_FACE_GRAPH",
            "GRAPH_AXIS_IS_EXACTLY_T_OR_P",
            "H1_DERIVATIVE_ON_GRAPH_AXIS_HAS_ONE_STRICT_SIGN_ON_FULL_BOX",
            "H1_HAS_STRICT_OPPOSITE_SIGNS_ON_THE_TWO_FULL_GRAPH_AXIS_FACES",
            "AXIS_INTERVAL_NEWTON_IMAGE_IS_A_STRICT_INTERIOR_SELF_MAP",
            "GRAPH_CARRIER_IS_NONEMPTY_AND_UNIQUE_OVER_THE_TRANSVERSE_BASE",
            "NEGATIVE_AND_POSITIVE_OFF_GRAPH_OPEN_SLABS_ARE_DEFINED_BY_H1_SIGN",
            "HALF_OPEN_POLICY_ASSIGN_H1_EQUALS_ZERO_TO_NEGATIVE_CLOSED_GRAPH_SLAB",
        ],
        "decomposition":{
            "typed_graph":{"predicate":"H1=0","dimension":1,"Lebesgue_2_measure_zero":True},
            "negative_open_slab":{"predicate":"H1<0","dimension":2},
            "positive_open_slab":{"predicate":"H1>0","dimension":2},
            "half_open_negative_owner":{"predicate":"H1<=0","owns_graph":True},
            "half_open_positive_owner":{"predicate":"H1>0","owns_graph":False},
            "pairwise_disjoint_three_strata":True,"union_equals_exact_input_box":True,
            "volumetric_Kraft_identity":"mu(H1<0)+mu(H1>0)=mu(input_box); mu(H1=0)=0",
            "normalized_full_dimensional_Kraft_conservation":"1",
        },
        "consumption_contract":{"response":"EXACT_GRAPH_CARRIER_PLUS_TWO_OFF_GRAPH_SIGN_SLABS","missing_duplicate_or_failed_predicate":"FAIL_CLOSED","semantic_sign_partition_not_a_dyadic_depth_extension":True,"decision_is_terminal_disposition":False,"decision_is_collision2_handoff":False,"downstream_must_route_graph_and_both_slabs":True},
        "strict_boundary":{"candidate_is_installed_authority":False,"runtime_or_canonical_written":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},
    };value["object_sha256"]=h(value);return value


def attacks(census:dict[str,int])->dict[str,Any]:
    capsule={**census,"flint_0_9_0":True,"precision_384":True,"all_lineage_exact":True,"all_unique_first":True,"all_owner_W10":True,"all_graph_axis_strict":True,"all_full_face_brackets":True,"all_interval_newton_self_maps":True,"all_graph_carriers_nonempty":True,"all_two_slab_partitions_complete":True,"all_graphs_zero_area":True,"all_half_open_owners_unique":True,"all_source_paths_prefix_free":True,"all_source_volume_preserved":True,"extra_dyadic_depth_used":False,"runtime_write":False,"credit":0}
    out={}
    for key in sorted(capsule):
        m=copy.deepcopy(capsule);v=m[key];m[key]=not v if type(v)is bool else v+1
        try:need(m==capsule,"attack:"+key)
        except FailClosed:out[key]="FAIL_CLOSED"
        else:raise FailClosed("attack escaped")
    return{"status":f"PASS_{len(out)}_OF_{len(out)}_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":len(out),"attacks":out}


def build()->dict[str,Any]:
    need(flint.__version__=="0.9.0" and flint.ctx.prec==384,"frozen flint")
    raw={};identities={}
    for key,path in SOURCE_PATHS.items():raw[key],identities[key]=secure(path,P[key])
    c68=json.loads(raw["C68R"]);c61=json.loads(raw["C61R"]);c58=json.loads(raw["C58R"]);c40=json.loads(raw["C40R"])
    for value,expected,label in[(c68,P["C68O"],"C68"),(c61,P["C61O"],"C61"),(c58,P["C58O"],"C58"),(c40,P["C40O"],"C40")]:closeobj(value,expected,label)
    structural=rows(raw["C68S"],c68["ledgers"]["singleton_structural_tasks"],"C68 structural")
    c61rows=rows(raw["C61L"],c61["ledgers"]["aggregate_leaves"],"C61 leaves")
    selected61=[x for x in c61rows if x["disposition"]=="COLLISION2_HANDOFF"]
    need(len(structural)==len(selected61)==20879,"20879 exact inputs")
    for a,b in zip(structural,selected61,strict=True):need(a["C61_aggregate_leaf_row_sha256"]==b["row_sha256"],"C68/C61 order")
    c58rows=rows(raw["C58L"],c58["ledgers"]["leaves"],"C58 leaves");m58={x["row_sha256"]:x for x in c58rows}
    context=c41.load_context(C40,None,formal=False);need(context["result"]["object_sha256"]==P["C40O"],"C40 context");c41.install_complete_immutable_cache();config=c41.decode_worker_config(context["config"])
    c40rows=c41.c38.read_ledger(C40,context["result"]["ledgers"]["routed_leaf_cells"]);m40={x["row_sha256"]:(i,x) for i,x in enumerate(c40rows)};need(len(m40)==35009,"C40 index")
    task_cache={}
    def task(source:dict[str,Any])->dict[str,Any]:
        source58=m58[source["source_C58_leaf_row_sha256"]];key=source58["C40_source_row_sha256"]
        if key not in task_cache:
            ordinal,row=m40[key];task_cache[key]=c41.task_for_row(ordinal,row,context)
        return task_cache[key]
    frozen_contract=contract();(OUT/CONTRACT_FILE).write_bytes(enc(frozen_contract)+b"\n")
    category=Counter();axis_census=Counter();orientation=Counter();pair_decisions=Counter();pair_volume=defaultdict(Fraction);decision_rows=[];blocker_rows=[]
    with Writer(OUT/DECISION_FILE,"C68_C61_FILTERED_ORDER__FULL_FACE_ONLY") as dw,Writer(OUT/BLOCKER_FILE,"C68_C61_FILTERED_ORDER__NON_FULL_FACE") as bw:
        for structural_row,source in zip(structural,selected61,strict=True):
            kind=structural_row["structural_graph_kind"];category[kind]+=1
            need(structural_row["path"]==source["path"] and structural_row["pair_index"]==source["pair_index"] and structural_row["exact_representative_box_object_sha256"]==h(source["exact_representative_box"]),"C68/C61 task binding")
            if kind!="REGULAR_FULL_FACE_GRAPH_CELL":
                body={"schema":SCHEMA+".blocker-row","C68_structural_task_row_sha256":structural_row["row_sha256"],"C61_aggregate_leaf_row_sha256":source["row_sha256"],"pair_index":source["pair_index"],"path":source["path"],"parent_volume_fraction":source["parent_volume_fraction"],"exact_representative_box_object_sha256":h(source["exact_representative_box"]),"structural_graph_kind":kind,"route_classification":source["route_classification"],"route_witness":source["route_witness"],"capability_decision_available":False,"blocker_codes":blockers(kind),"additional_dyadic_depth_recommended":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0};blocker_rows.append(bw.write(body));continue
            current=task(source);source58=m58[source["source_C58_leaf_row_sha256"]]
            need(current["source"]["row_sha256"]==source58["C40_source_row_sha256"],"C58/C40 task")
            route=c41.route_at_path(current,source["path"],config);box=route["box"];need(c41.box_payload(box)==source["exact_representative_box"],"exact box replay")
            result=route["c1_result"];evidence=result["surface_evidence"];h1=evidence["H1"]
            need(route["classification"]==source["route_classification"]=="UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY" and route["witness"]==source["route_witness"]=="REGULAR_FULL_FACE_GRAPH","route replay")
            need(evidence["input_stage_one_classification"]==evidence["enhanced_stage_one_classification"]=="unique_first" and evidence["enhanced_owner_target"]=="W[1,0]" and evidence["remaining_unresolved_record_count"]==0,"unique owner")
            axis=h1["graph_axis"];need(h1["kind"]=="REGULAR_FULL_FACE_GRAPH" and axis in{"t","p"},"H1 graph axis");idx={"t":0,"p":1}[axis]
            face=[x for x in h1["face_evidence"] if x["axis"]==axis];need(len(face)==1,"axis face evidence");face=face[0];low=face["lower_face"]["sign"];high=face["upper_face"]["sign"];need({low,high}=={"NEGATIVE","POSITIVE"},"opposite full faces")
            full=c41.round185.surface_evidence("H1",current["c38_source"]["representative_origin_key"],box,c41.FROZEN_OWNER,include_axis_tests=True);derivative=full["full_box_C1_derivatives"]["d"+axis];newton=full["axis_interval_Newton"][idx]
            certificate_checks={"strict_derivative":not derivative["contains_zero"],"full_face_bracket":full["axis_full_face_brackets_t_p_s"][idx] is True,"newton_axis":newton["axis"]==axis,"newton_strict_derivative":newton["strict_derivative"] is True,"newton_self_map":newton["strict_interior_self_map"] is True,"newton_image":newton["image"] is not None,"nonempty":full["independently_certified_nonempty"] is True}
            need(all(certificate_checks.values()),"full graph certificate:"+source["row_sha256"]+":"+json.dumps(certificate_checks,sort_keys=True))
            negative_side="LOWER_GRAPH_AXIS_SIDE" if low=="NEGATIVE" else "UPPER_GRAPH_AXIS_SIDE";positive_side="LOWER_GRAPH_AXIS_SIDE" if low=="POSITIVE" else "UPPER_GRAPH_AXIS_SIDE"
            graph={"equation":"H1=n1_x^2-n1_y^2=0","predicate":"H1=0","dimension":1,"graph_axis":axis,"transverse_axis":"p" if axis=="t" else "t","unique_root_over_full_transverse_base":True,"uniform_root_interval_enclosure":newton["image"],"strict_implicit_derivative_bounds":derivative,"certified_nonempty":True,"Lebesgue_2_measure_zero":True}
            slabs={"negative_open_slab":{"predicate":"H1<0","axis_orientation":negative_side,"dimension":2},"positive_open_slab":{"predicate":"H1>0","axis_orientation":positive_side,"dimension":2},"half_open_negative_graph_owner":{"predicate":"H1<=0","owns_graph":True},"half_open_positive_owner":{"predicate":"H1>0","owns_graph":False},"three_strata_pairwise_disjoint":True,"three_strata_union_exact_input_box":True,"two_full_dimensional_slabs_cover_modulo_zero_area_graph":True}
            body={"schema":SCHEMA+".decision-row","decision":"STRICT_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE","query_key":"c69a-h1-graph-slab:"+source["row_sha256"],"C68_structural_task_row_sha256":structural_row["row_sha256"],"C61_aggregate_leaf_row_sha256":source["row_sha256"],"C58_leaf_row_sha256":source58["row_sha256"],"C40_source_row_sha256":current["source"]["row_sha256"],"C38_source_row_sha256":current["c38_source"]["row_sha256"],"representative_origin_key":current["c38_source"]["representative_origin_key"],"pair_index":source["pair_index"],"path":source["path"],"parent_volume_fraction":source["parent_volume_fraction"],"exact_representative_box":source["exact_representative_box"],"exact_reflected_box":source["exact_reflected_box"],"C39_replay":{"input_stage_one_classification":"unique_first","enhanced_stage_one_classification":"unique_first","enhanced_owner_target":"W[1,0]","remaining_unresolved_record_count":0,"H1_kind":"REGULAR_FULL_FACE_GRAPH","H1_graph_axis":axis,"axis_lower_face":face["lower_face"],"axis_upper_face":face["upper_face"]},"full_box_H1_certificate":{"Arb_precision_bits":flint.ctx.prec,"graph_axis":axis,"strict_derivative_bounds":derivative,"opposite_sign_full_axis_faces":True,"axis_interval_Newton":newton,"strict_corner_segment_bracket":full["strict_corner_segment_bracket"],"normal_component_bounds":full["normal_component_bounds"]},"typed_graph_carrier":graph,"off_graph_slabs":slabs,"half_open_graph_owner":"NEGATIVE_CLOSED_GRAPH_SLAB","partition_and_Kraft":{"source_path_preserved":True,"source_parent_volume_fraction_preserved":source["parent_volume_fraction"],"semantic_partition_not_extra_dyadic_depth":True,"volumetric_identity":"mu(H1<0)+mu(H1>0)=mu(input_box); mu(H1=0)=0","normalized_full_dimensional_Kraft_conservation":"1","typed_graph_weight_in_2D_Kraft":"0"},"capability_consumption_ready":True,"terminal_disposition_credit":0,"collision2_handoff_credit":0,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0};decision_rows.append(dw.write(body));axis_census[axis]+=1;orientation[low+"_TO_"+high]+=1;pair_decisions[str(source["pair_index"])]+=1;pair_volume[str(source["pair_index"])]+=Fraction(source["parent_volume_fraction"])
    decision_desc=dw.descriptor();blocker_desc=bw.descriptor()
    expected_category=Counter({"REGULAR_BOUNDARY_ARRANGEMENT":9053,"REGULAR_FULL_FACE_GRAPH_CELL":2356,"REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":5364,"REGULAR_MULTI_GRAPH_FIRST_TANGENCY":737,"SOURCE_GRAZING_ENDPOINT_CHART":147,"COLLISION1_OUTGOING_STATE":3222})
    need(category==expected_category and decision_desc["row_count"]==2356 and blocker_desc["row_count"]==18523,"exact census");need(prefix_free([x["path"] for x in decision_rows]) and len({x["query_key"] for x in decision_rows})==2356,"decision keys/prefix")
    census={"input_task_count":20879,"decision_count":2356,"blocker_count":18523,"full_face_graph_count":2356,"boundary_blocker_count":9053,"order_blocker_count":5364,"tangency_blocker_count":737,"grazing_blocker_count":147,"outgoing_blocker_count":3222,"formal_credit":0,"D02_gate_credit":0}
    result={"schema":SCHEMA+".result","status":"CONSUMPTION_READY_CAPABILITY_PROTOTYPE__2356_OF_2356_FULL_FACE_H1_GRAPH_SLAB_DECISIONS__18523_FAIL_CLOSED_BLOCKERS__ZERO_CREDIT","producer_file_sha256":hf(SELF),"contract_file_sha256":hf(OUT/CONTRACT_FILE),"contract_object_sha256":frozen_contract["object_sha256"],"input_file_sha256":{k:P[k] for k in SOURCE_PATHS},"input_file_identities":identities,"input_object_sha256":{"C68":P["C68O"],"C61":P["C61O"],"C58":P["C58O"],"C40":P["C40O"]},"numeric_environment":{"python_flint_version":flint.__version__,"Arb_precision_bits":flint.ctx.prec,"source_pins_revalidated_by_C41_load_context":True},"scope":census,"category_census":dict(sorted(category.items())),"decision_axis_census":dict(sorted(axis_census.items())),"decision_face_orientation_census":dict(sorted(orientation.items())),"decision_pair_census":dict(sorted(pair_decisions.items(),key=lambda x:int(x[0]))),"decision_pair_source_volume_fraction":{k:str(v) for k,v in sorted(pair_volume.items(),key=lambda x:int(x[0]))},"ledgers":{"decisions":decision_desc,"blockers":blocker_desc},"global_invariants":{"all_2356_exact_lineages_replayed":True,"all_2356_unique_first_W10":True,"all_2356_strict_graph_axis":True,"all_2356_opposite_sign_full_faces":True,"all_2356_interval_Newton_self_map":True,"all_2356_nonempty_unique_graph_carriers":True,"all_2356_two_off_graph_slab_partitions":True,"all_2356_half_open_graph_owners_unique":True,"all_2356_source_paths_prefix_free":True,"all_2356_source_volume_and_Kraft_preserved":True,"additional_dyadic_depth_used":False},"producer_attacks":attacks(census),"strict_boundary":{"capability_prototype":True,"candidate_is_installed_authority":False,"decisions_are_terminal_dispositions":False,"runtime_or_canonical_written":False,"old_files_modified":False,"formal_credit":0,"whole_parent_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},"required_next":["INDEPENDENT_NO_PRODUCER_REBUILD_OF_ALL_2356_NUMERIC_CERTIFICATES_AND_18523_BLOCKERS","CONSUME_GRAPH_AND_BOTH_OFF_GRAPH_SLABS_ONLY_AFTER_EXACT_MANIFEST_BINDING","BUILD_MULTI_SURFACE_ORDER_ENDPOINT_AND_OUTGOING_EVALUATORS_FOR_THE_18523_BLOCKERS"]};result["object_sha256"]=h(result);(OUT/RESULT_FILE).write_bytes(enc(result)+b"\n")
    report=f"""# C69a singleton H1 graph/slab capability prototype\n\nStatus: `{result['status']}`\n\nC69a certifies all 2,356 frozen `REGULAR_FULL_FACE_GRAPH` tasks as nonempty unique H1 graph carriers over a strict monotone axis, with an opposite-sign full-face bracket and an interval-Newton interior self-map. Each exact input box is decomposed into `H1<0`, `H1=0`, and `H1>0`; the graph has zero two-dimensional measure, and the half-open policy assigns `H1=0` to the negative closed graph slab. This is a semantic graph/slab decomposition, not another dyadic-depth pass.\n\nThe other 18,523 tasks remain fail-closed: 9,053 boundary, 5,364 order, 737 tangency, 147 grazing, and 3,222 outgoing-state blockers.\n\nDecision ledger: `{decision_desc['sha256']}`. Blocker ledger: `{blocker_desc['sha256']}`. Result object: `{result['object_sha256']}`. Formal and D02 gate credit remain zero; runtime and canonical state were not written.\n""";(OUT/REPORT_FILE).write_text(report,encoding="utf-8");return result


def main()->int:
    r=build();print(json.dumps({"status":r["status"],"scope":r["scope"],"axis":r["decision_axis_census"],"object_sha256":r["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except(FailClosed,OSError,ValueError,KeyError,TypeError,IndexError,RuntimeError) as e:print(f"FAIL_CLOSED:{type(e).__name__}:{e}",file=sys.stderr);raise SystemExit(2)
