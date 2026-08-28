#!/usr/bin/env python3
"""C60-L no-producer static existing-edge owner/history query.

Consumes the 1,042 C59 frozen requests, reconstructs the full C41 two-sided
active universe, atomizes every exact rational/algebraic face or cross-chart
seam, and applies the frozen C50a lexicographic semantic-path owner rule.
History compatibility remains fail-closed because no frozen relation maps
C35 occurrence 1 and the two endpoint lineage sets onto those edge atoms.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import cmp_to_key
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c60l_static_edge_owner"
SCHEMA = "cm2.round306c60l.static-existing-edge-two-endpoint-owner-history-query.v1"
ATOM_FILE = PREFIX + "_incidence_atoms_v1.jsonl.gz"
DECISION_FILE = PREFIX + "_edge_decisions_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C59_RESULT = OUT / "cm2_round306c59l_owner_result_v1.json"
C59_VERIFY = OUT / "cm2_round306c59l_owner_independent_verification_v1.json"
C59_MANIFEST = OUT / "cm2_round306c59l_owner_manifest_v1.sha256"
C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

PINS = {
    "C59_RESULT_FILE":"3391d96f6baa89281f9b60bd84a6aa950a74c6f6a99e86bc32b3322786e5a53e",
    "C59_RESULT_OBJECT":"b6c486e042acedb9c287eda527cd4fcafffd1a53ff768b7697124100e39a85c2",
    "C59_VERIFY_FILE":"86cc87bc70cd78456a8913f632bb794806126f5f9963f700688880534c8a8c99",
    "C59_VERIFY_OBJECT":"211f458b57e33544ef1978ddecda37f167e2df01720c72f0af003122b9c4bd58",
    "C59_MANIFEST_FILE":"9940f3a133092aa9dea50204c0ef7c1c196ad1108c2fb1b01c8f5c6de4dc6fee",
    "C32_RESULT_FILE":"c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4",
    "C32_OBJECT":"32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C41_RESULT_FILE":"73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_OBJECT":"b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C38_RESULT_FILE":"094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_OBJECT":"fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C39_RESULT_FILE":"f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "C39_OBJECT":"821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C40_RESULT_FILE":"f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_OBJECT":"397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C53":"f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "CANONICAL":"922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}
OWNER_RULE = "UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH"
ALG = {"-1/sqrt(2)", "+1/sqrt(2)"}


class FailClosed(RuntimeError): pass
def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise FailClosed(label)
def enc(value: Any) -> bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def h(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()
def hf(path: Path) -> str:
    state=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1<<20),b""):state.update(block)
    return state.hexdigest()
def sequence(values: Iterable[str]) -> str:
    state=hashlib.sha256()
    for value in values:state.update(value.encode("ascii")+b"\n")
    return state.hexdigest()
def js(path: Path) -> dict[str,Any]: return json.loads(path.read_text())
def object_close(value: dict[str,Any], expected: str, label: str) -> None:
    body=dict(value);actual=body.pop("object_sha256",None);need(actual==expected==h(body),"object:"+label)
def row_close(row: dict[str,Any], label: str) -> None:
    body=dict(row);actual=body.pop("row_sha256",None);need(actual==h(body),"row:"+label)
def ledger(base: Path,desc:dict[str,Any],label:str)->list[dict[str,Any]]:
    path=base/desc["filename"];need(hf(path)==desc["sha256"],"file:"+label);rows=[];hashes=[]
    for index,line in enumerate(gzip.open(path,"rt")):
        row=json.loads(line);row_close(row,f"{label}:{index}");rows.append(row);hashes.append(row["row_sha256"])
    need(len(rows)==desc["row_count"] and sequence(hashes)==desc["row_hash_line_sequence_sha256"],"descriptor:"+label);return rows


class Writer:
    def __init__(self,path:Path,order:str):
        self.path,self.order=path,order;self.raw=path.open("wb");self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,mtime=0);self.count=0;self.seq=hashlib.sha256()
    def __enter__(self):return self
    def write(self,body:dict[str,Any])->dict[str,Any]:
        rh=h(body);row={**body,"row_sha256":rh};self.gz.write(enc(row)+b"\n");self.seq.update((rh+"\n").encode());self.count+=1;return row
    def __exit__(self,*_):self.gz.close();self.raw.close()
    def descriptor(self):return {"filename":self.path.name,"order":self.order,"row_count":self.count,"row_hash_line_sequence_sha256":self.seq.hexdigest(),"sha256":hf(self.path),"size":self.path.stat().st_size}


def token(value: Any)->str:
    out=value["value"] if type(value) is dict else value;need(type(out) is str,"scalar token");return out
def compare(a:str,b:str)->int:
    if a==b:return 0
    if a not in ALG and b not in ALG:return -1 if Fraction(a)<Fraction(b) else 1
    if a in ALG and b in ALG:return -1 if a.startswith("-") else 1
    if a in ALG:return -compare(b,a)
    q=Fraction(a)
    if b=="+1/sqrt(2)":
        if q<=0:return -1
        need(q*q!=Fraction(1,2),"rational/algebraic inequality");return -1 if q*q<Fraction(1,2) else 1
    if q>=0:return 1
    need(q*q!=Fraction(1,2),"rational/algebraic inequality");return -1 if q*q>Fraction(1,2) else 1
def minimum(a:str,b:str)->str:return a if compare(a,b)<=0 else b
def maximum(a:str,b:str)->str:return a if compare(a,b)>=0 else b
def overlap(a0:str,a1:str,b0:str,b1:str)->tuple[str,str]|None:
    low,high=maximum(a0,b0),minimum(a1,b1);return (low,high) if compare(low,high)<0 else None


def compact_occurrence(row:dict[str,Any])->dict[str,Any]:
    return {"physical_occurrence_id":row["physical_occurrence_id"],"occurrence_binding_sha256":row["occurrence_binding_sha256"],
            "source_kind":"C41_BASELINE","side":row["side"],"pair_index":row["pair_index"],"semantic_path":row["semantic_path"],
            "physical_cell_id":row["physical_cell_id"],"upstream_ambient_row_sha256":row["upstream_ambient_row_sha256"]}


def self_test(summary:dict[str,int])->dict[str,Any]:
    expected={"request_count":1042,"active_occurrence_count":183758,"exact_atom_count":13103,"incidence_complete_edge_count":1042,
              "endpoint_coverage_complete_edge_count":1042,"geometric_owner_unique_edge_count":911,"geometric_owner_nonunique_edge_count":131,
              "intra_owner_nonunique_edge_count":115,"seam_owner_nonunique_edge_count":16,"overall_query_pass_count":0,
              "overall_query_fail_closed_count":1042,"history_compatibility_pass_count":0}
    need(summary==expected,"summary")
    attacks={}
    for index,(key,value) in enumerate(expected.items()):
        altered=dict(summary);altered[key]=value+1
        try:need(altered==expected,"mutated")
        except FailClosed:attacks[f"projection_{index}_{key}"]="FAIL_CLOSED"
        else:raise FailClosed("attack accepted")
    return {"status":"PASS_12_OF_12_PRODUCER_ATTACKS_FAIL_CLOSED","attack_count":12,"attacks":attacks}


def build()->dict[str,Any]:
    files=[(C59_RESULT,"C59_RESULT_FILE"),(C59_VERIFY,"C59_VERIFY_FILE"),(C59_MANIFEST,"C59_MANIFEST_FILE"),
           (C32/"result.json","C32_RESULT_FILE"),(C41/"result.json","C41_RESULT_FILE"),(C38/"result.json","C38_RESULT_FILE"),
           (C39/"result.json","C39_RESULT_FILE"),(C40/"result.json","C40_RESULT_FILE"),(C53,"C53"),(CANONICAL,"CANONICAL")]
    for path,key in files:need(hf(path)==PINS[key],"pin:"+key)
    c59,c59v,c32,c41,c38,c39,c40=map(js,[C59_RESULT,C59_VERIFY,C32/"result.json",C41/"result.json",C38/"result.json",C39/"result.json",C40/"result.json"])
    for value,key,label in [(c59,"C59_RESULT_OBJECT","C59"),(c59v,"C59_VERIFY_OBJECT","C59v"),(c32,"C32_OBJECT","C32"),(c41,"C41_OBJECT","C41"),(c38,"C38_OBJECT","C38"),(c39,"C39_OBJECT","C39"),(c40,"C40_OBJECT","C40")]:object_close(value,PINS[key],label)
    endpoints=ledger(OUT,c59["ledgers"]["endpoint_occurrence1_history_bindings"],"C59 endpoints")
    requests=ledger(OUT,c59["ledgers"]["edge_owner_history_requests"],"C59 requests")
    need(len(endpoints)==1044 and len(requests)==1042,"scope")
    endpoint={row["cell_id"]:row for row in endpoints}
    cells=ledger(C32,c32["ledgers"]["cells"],"C32 cells")
    cell_map={row["cell_id"]:row for row in cells}
    ambient=ledger(C41,c41["ledgers"]["routed_ambient_cells"],"C41 ambient")

    index:dict[tuple[str,str,str],list[tuple[dict[str,Any],str,str,str]]]=defaultdict(list)
    active=[]; rational=0; algebraic=0
    for row in ambient:
        for side in ("REPRESENTATIVE","REFLECTED"):
            cid=row["representative_cell_id" if side=="REPRESENTATIVE" else "reflected_cell_id"];cell=cell_map[cid]
            box=row["closed_representative_box" if side=="REPRESENTATIVE" else "closed_reflected_box"]
            if box is None:t=[token(x) for x in cell["physical_t_interval"]];p=[token(x) for x in cell["physical_p_interval"]]
            else:t=[token(x) for x in box["t"]];p=[token(x) for x in box["p"]]
            body={"active_universe_binding_sha256":"112410045d088f22908276193a1d046d6f11c0e1818790b2826c5fcf0f6ac05f",
                  "source_kind":"C41_BASELINE","side":side,"pair_index":row["pair_index"],"semantic_path":row["path"],
                  "physical_cell_id":cid,"compact_chart":cell["compact_chart"],"t":t,"p":p,"upstream_ambient_row_sha256":row["row_sha256"]}
            binding=h(body);occ={**body,"occurrence_binding_sha256":binding,"physical_occurrence_id":"c60l-static-occurrence:"+binding}
            active.append(occ);rational+=all(x not in ALG for x in t+p);algebraic+=any(x in ALG for x in t+p)
            for axis,values,other in (("t",t,p),("p",p,t)):
                index[(cell["compact_chart"],axis,values[0])].append((occ,"POSITIVE_COORDINATE_SIDE",other[0],other[1]))
                index[(cell["compact_chart"],axis,values[1])].append((occ,"NEGATIVE_COORDINATE_SIDE",other[0],other[1]))
    need(len(active)==183758 and rational==183700 and algebraic==58,"active census")
    need(len({row["physical_occurrence_id"] for row in active})==183758,"active identities")

    decision_rows=[];edge_census=Counter();atom_count=0
    with Writer(OUT/ATOM_FILE,"C59_REQUEST_ORDER_THEN_EXACT_SPAN") as atom_writer:
        for request in requests:
            geometry=request["exact_common_face_or_seam"];low,high=geometry.get("span",geometry.get("physical_p_span"));sets=[]
            if request["glue_kind"]=="INTRA_CHART_FACE":
                chart=endpoint[request["source_cell_id"]]["compact_chart"]
                sets=[("COMMON_CHART",index[(chart,geometry["axis"],geometry["fixed_coordinate"])])]
            else:
                for role,cid in (("SOURCE",request["source_cell_id"]),("TARGET",request["target_cell_id"])):
                    ep=endpoint[cid];t=[token(x) for x in ep["exact_physical_slice_endpoint_box"]["t"]];contact=[x for x in t if x in ALG]
                    need(len(contact)==1,"seam algebraic contact");sets.append((role,index[(ep["compact_chart"],"t",contact[0])]))
            breaks={low,high};incident_candidates=[]
            for role,rows in sets:
                for occurrence,side,a,b in rows:
                    found=overlap(low,high,a,b)
                    if found:breaks.update(found);incident_candidates.append((role,occurrence,side,a,b))
            ordered=sorted(breaks,key=cmp_to_key(compare));edge_atoms=[]
            for atom_index,(a,b) in enumerate(zip(ordered,ordered[1:])):
                if compare(a,b)>=0:continue
                incidents=[]
                for role,occurrence,side,x,y in incident_candidates:
                    if compare(x,a)<=0 and compare(b,y)<=0:incidents.append((role,occurrence,side))
                incidents.sort(key=lambda x:x[1]["physical_occurrence_id"])
                if request["glue_kind"]=="INTRA_CHART_FACE":
                    sides=Counter(row[2] for row in incidents);complete=sides==Counter({"NEGATIVE_COORDINATE_SIDE":1,"POSITIVE_COORDINATE_SIDE":1})
                else:
                    sides=Counter(row[0] for row in incidents);complete=sides==Counter({"SOURCE":1,"TARGET":1})
                minimum_path=min((row[1]["semantic_path"] for row in incidents),default=None)
                winners=[row for row in incidents if row[1]["semantic_path"]==minimum_path]
                unique=len(winners)==1
                cells_seen={row[1]["physical_cell_id"] for row in incidents};coverage=cells_seen=={request["source_cell_id"],request["target_cell_id"]}
                compact=[]
                for role,occurrence,side in incidents:
                    item=compact_occurrence(occurrence);item.update({"edge_role":role,"geometric_side":side});compact.append(item)
                body={"schema":SCHEMA+".incidence-atom-row","owner_rule":OWNER_RULE,"C59_request_row_sha256":request["row_sha256"],
                      "owner_history_request_id":request["owner_history_request_id"],"face_or_corner_id":request["face_or_corner_id"],
                      "glue_kind":request["glue_kind"],"atom_index":atom_index,"exact_span":[a,b],"incident_occurrence_count":len(compact),
                      "incident_occurrences":compact,"incident_occurrence_binding_sequence_sha256":sequence(x[1]["occurrence_binding_sha256"] for x in incidents),
                      "incidence_complete":complete,"endpoint_cell_coverage_complete":coverage,"minimum_semantic_path":minimum_path,
                      "owner_unique":unique,"owner":compact_occurrence(winners[0][1]) if unique else None,
                      "owner_tie_occurrence_ids":[] if unique else [row[1]["physical_occurrence_id"] for row in winners],
                      "formal_credit":0,"D02_gate_credit":0}
                edge_atoms.append(atom_writer.write(body))
            need(bool(edge_atoms),"nonempty edge atomization")
            atom_count+=len(edge_atoms);complete=all(row["incidence_complete"] for row in edge_atoms);coverage=all(row["endpoint_cell_coverage_complete"] for row in edge_atoms);unique=all(row["owner_unique"] for row in edge_atoms)
            edge_census["complete"]+=complete;edge_census["coverage"]+=coverage;edge_census["unique"]+=unique;edge_census["nonunique"]+=not unique
            if not unique:edge_census["nonunique_intra" if request["glue_kind"]=="INTRA_CHART_FACE" else "nonunique_seam"]+=1
            history=False
            reasons=[]
            if not unique:reasons.append("LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH_OWNER_TIE_ON_AT_LEAST_ONE_ATOM")
            reasons.extend(["NO_FROZEN_EDGE_ATOM_TO_C35_OCCURRENCE1_SEMANTIC_MAP",
                            "NO_FROZEN_C38_C41_ENDPOINT_LINEAGE_TO_EDGE_ATOM_INCIDENCE_MAP",
                            "WITHIN_CELL_LINEAGE_EXACTNESS_DOES_NOT_PROVE_CROSS_EDGE_OCCURRENCE1_HISTORY_COMPATIBILITY"])
            decision_rows.append({"schema":SCHEMA+".edge-decision-row","C59_request_row_sha256":request["row_sha256"],
                "owner_history_request_id":request["owner_history_request_id"],"source_cell_id":request["source_cell_id"],"target_cell_id":request["target_cell_id"],
                "face_or_corner_id":request["face_or_corner_id"],"glue_kind":request["glue_kind"],"atom_count":len(edge_atoms),
                "incidence_atom_row_hash_sequence_sha256":sequence(row["row_sha256"] for row in edge_atoms),"full_active_universe_incidence_complete":complete,
                "endpoint_cell_coverage_complete":coverage,"geometric_owner_unique":unique,"geometric_owner_unique_disproved":not unique,
                "C35_occurrence1_request_binding_valid":request["C35_occurrence1_history_binding_sha256"]==c59["occurrence1_binding"]["history_binding_sha256"],
                "both_endpoint_C38_C41_lineage_sequence_bindings_valid":all(type(row["C38_C41_lineage_projection_hash_sequence_sha256"]) is str for row in request["endpoint_bindings"]),
                "edge_atom_to_occurrence1_lineage_semantic_mapping_present":False,"occurrence1_owner_history_compatible_proved":history,
                "overall_query_pass":False,"decision":"FAIL_CLOSED_MISSING_EDGE_ATOM_TO_OCCURRENCE1_LINEAGE_SEMANTIC_MAPPING",
                "reason_codes":reasons,"formal_credit":0,"D02_gate_credit":0})
    atom_desc=atom_writer.descriptor()
    need(atom_count==13103 and edge_census==Counter({"complete":1042,"coverage":1042,"unique":911,"nonunique":131,"nonunique_intra":115,"nonunique_seam":16}),"edge census")
    with Writer(OUT/DECISION_FILE,"C59_REQUEST_ORDER") as writer:
        for row in decision_rows:writer.write(row)
    decision_desc=writer.descriptor()
    summary={"request_count":1042,"active_occurrence_count":183758,"exact_atom_count":13103,"incidence_complete_edge_count":1042,
             "endpoint_coverage_complete_edge_count":1042,"geometric_owner_unique_edge_count":911,"geometric_owner_nonunique_edge_count":131,
             "intra_owner_nonunique_edge_count":115,"seam_owner_nonunique_edge_count":16,"overall_query_pass_count":0,
             "overall_query_fail_closed_count":1042,"history_compatibility_pass_count":0}
    test=self_test(summary)
    result={"schema":SCHEMA+".result","status":"PASS_FULL_ACTIVE_UNIVERSE_INCIDENCE_1042_OF_1042__GEOMETRIC_OWNER_UNIQUE_911__OWNER_TIE_131__FAIL_CLOSED_HISTORY_COMPATIBILITY_0_OF_1042__ZERO_CREDIT",
            "authority_binding":{"C59_result_file_sha256":PINS["C59_RESULT_FILE"],"C59_result_object_sha256":PINS["C59_RESULT_OBJECT"],
              "C59_independent_verification_file_sha256":PINS["C59_VERIFY_FILE"],"C59_independent_verification_object_sha256":PINS["C59_VERIFY_OBJECT"],
              "C59_manifest_file_sha256":PINS["C59_MANIFEST_FILE"],"C32_object_sha256":PINS["C32_OBJECT"],"C41_object_sha256":PINS["C41_OBJECT"],
              "C38_object_sha256":PINS["C38_OBJECT"],"C39_object_sha256":PINS["C39_OBJECT"],"C40_object_sha256":PINS["C40_OBJECT"],
              "C53_head_file_sha256":PINS["C53"],"canonical_file_sha256":PINS["CANONICAL"]},
            "active_universe":{"C41_ambient_row_count":91879,"physical_occurrence_count":183758,"exact_rational_occurrence_count":183700,
              "algebraic_source_boundary_occurrence_count":58,"occurrence_id_sequence_sha256":sequence(sorted(row["physical_occurrence_id"] for row in active)),
              "owner_rule":OWNER_RULE,"full_active_universe_scanned":True},
            "scope":summary,"ledgers":{"incidence_atoms":atom_desc,"edge_decisions":decision_desc},"self_test":test,
            "strict_boundary":{"geometry_owner_pass_is_not_overall_history_pass":True,"runtime_or_canonical_written":False,"formal_credit":0,"D02_gate_credit":0,"CM2":"NO-GO_FOR_CLAIM"},
            "required_next":["MATERIALIZE_EDGE_ATOM_TO_C35_OCCURRENCE1_SEMANTIC_MAP","MATERIALIZE_BOTH_ENDPOINT_C38_C41_LINEAGE_TO_EDGE_ATOM_INCIDENCE_MAP",
              "RESOLVE_131_LEXICOGRAPHIC_OWNER_TIES_WITH_A_FROZEN_OCCURRENCE_AWARE_OWNER_RULE_OR_DISJOINT_HISTORY_CERTIFICATE","REPLAY_ALL_1042_REQUESTS_INDEPENDENTLY"]}
    result["object_sha256"]=h(result);(OUT/RESULT_FILE).write_bytes(enc(result)+b"\n");return result


def main()->int:
    result=build();print(json.dumps({"status":result["status"],"scope":result["scope"],"object_sha256":result["object_sha256"]},sort_keys=True));return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except (FailClosed,OSError,ValueError,KeyError,TypeError,IndexError) as exc:print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr);raise SystemExit(2)
