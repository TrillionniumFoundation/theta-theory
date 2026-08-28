#!/usr/bin/env python3
"""Produce the zero-credit corrected Round306C1 identity/support replay."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterable, Iterator


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c1_source_g_corrected_identity_support_replay"
SCHEMA: Final = "cm2.round306c1.source-g-corrected-identity-support-replay.v1"
FIXED_SPILL: Final = "/tmp/cm2-round306c1-spill"
FAMILIES: Final = ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")
OUTPUTS: Final = {
    "authority_frontier": PREFIX + "_authority_frontier.json",
    "family_census": PREFIX + "_family_census.jsonl.gz",
    "member": PREFIX + "_member_identity_support_ledger.jsonl.gz",
    "representation": PREFIX + "_representation_ledger.jsonl.gz",
    "physical_incidence": PREFIX + "_physical_incidence_statement_ledger.jsonl.gz",
    "gap": PREFIX + "_semantic_gap_ledger.jsonl.gz",
    "component_rebind": PREFIX + "_affected_component_rebind_ledger.jsonl.gz",
    "transition_handle": PREFIX + "_transition_ready_handle_ledger.jsonl.gz",
    "obligation_census": PREFIX + "_theorem_obligation_census.json",
    "result": PREFIX + "_result.json",
}
OUTPUT_ORDER: Final = tuple(OUTPUTS)


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C1_CONTRACT", "cm2_round306c1_source_g_corrected_identity_support_replay_contract.py", 63_460, "5724bff115289d3ace2a574b04028ce90842be0d629aa35c45fc9b1b8c85ad11"),
    Pin("C1_PREFLIGHT_SOURCE", "cm2_round306c1_source_g_corrected_identity_support_migration_preflight.py", 17_798, "f0acf40806ec9b7d7fa06edb98bc0709841f1136a5fa90b4c00118bfb2f6a63c"),
    Pin("C1_PREFLIGHT_RESULT", "cm2_round306c1_source_g_corrected_identity_support_migration_preflight_result.json", 6_698, "fc65ad5c78acddd61decbca9b9057cca0d6d59849ee3921c5433401cd581dacb"),
    Pin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    Pin("C0_INVALIDATION", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    Pin("C0_ROOT_DISPOSITION", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_base_root_disposition_ledger.jsonl.gz", 115_696_187, "6c8e84a6f247a00470f4abd2b6bb7c4caff6ff813236c3e63f04b884998eccdb"),
    Pin("C0_MEMBER_COMPONENT", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    Pin("I4_MANIFEST", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_manifest.sha256", 2_176, "53b84967618f80c0781c6728ceef4f0e88df7862bd37c5f4cae4055caf960051"),
    Pin("I4_MEMBER", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_member_ledger.jsonl.gz", 245_580_399, "0fbdbbb35b833272429499c005e3d24eb1c669cd5d557898e72605668347b4c8"),
    Pin("I4_REPRESENTATION", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_representation_ledger.jsonl.gz", 162_325_503, "3adcddcf414d2aedc23dab6770cd11ba3dbcf1f911573d5686a7d287b7094712"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    Pin("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("B1G0_GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
)

EXPECTED_MEMBERS: Final = {"PRESERVED":126_468,"NON_GRAPH":17_828,"R2":295_336,"R292":9_404,"G2A":38_608,"G2B":76_816}
EXPECTED_REPS: Final = {"PRESERVED":165_744,"NON_GRAPH":17_828,"R2":302_624,"R292":10_252,"G2A":38_608,"G2B":76_816}
EXPECTED_REBINDS: Final = {"PRESERVED":14_400,"NON_GRAPH":1_776,"R2":800,"R292":3_776,"G2A":584,"G2B":512}
ZERO_CREDIT: Final = {"normalized_support":0,"representation_cover":0,"A1_A2":0,"physical_incidence":0,"pullback_equivalence":0,"transition":0,"B1A":0,"B2":0,"maximality":0,"fibre":0,"global_disposition":0,"CM2":0}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev,info.st_ino,info.st_mode,info.st_nlink,info.st_size,info.st_mtime_ns,info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd,0,os.SEEK_SET); h=hashlib.sha256()
    while True:
        chunk=os.read(fd,1_048_576)
        if not chunk:return h.hexdigest()
        h.update(chunk)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd=-1; self.fds:dict[str,int]={}; self.ids:dict[str,tuple[int,...]]={}
    def __enter__(self) -> "Snapshot":
        before=os.stat(ROOT,follow_symlinks=False); need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(),"root")
        self.dirfd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        for pin in PINS:
            info=os.stat(pin.filename,dir_fd=self.dirfd,follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_size==pin.size,"pin stat:"+pin.role)
            fd=os.open(pin.filename,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.dirfd)
            opened=os.fstat(fd); need(identity(opened)==identity(info),"pin race:"+pin.role)
            need(hash_fd(fd)==hash_fd(fd)==pin.sha256,"pin sha:"+pin.role)
            self.fds[pin.role]=fd; self.ids[pin.role]=identity(opened)
        return self
    def dup(self,role:str)->int:
        fd=os.dup(self.fds[role]);os.lseek(fd,0,os.SEEK_SET);return fd
    def final(self)->None:
        for pin in reversed(PINS):
            fd=self.fds[pin.role]
            need(identity(os.fstat(fd))==self.ids[pin.role],"held:"+pin.role)
            need(identity(os.stat(pin.filename,dir_fd=self.dirfd,follow_symlinks=False))==self.ids[pin.role],"path:"+pin.role)
            need(hash_fd(fd)==pin.sha256,"final sha:"+pin.role)
    def __exit__(self,*_:Any)->None:
        for fd in self.fds.values():
            try:os.close(fd)
            except OSError:pass
        if self.dirfd>=0:os.close(self.dirfd)


def jsonl(snapshot:Snapshot,role:str)->Iterator[dict[str,Any]]:
    fd=snapshot.dup(role)
    try:
        with os.fdopen(fd,"rb",closefd=True) as raw, gzip.GzipFile(fileobj=raw,mode="rb") as stream:
            for ordinal,line in enumerate(stream):
                need(line.endswith(b"\n") and len(line)<=8_388_609,"wire:"+role)
                value=json.loads(line);need(type(value)is dict and canonical(value)+b"\n"==line,"canonical:"+role+":"+str(ordinal));yield value
    finally:
        try:os.close(fd)
        except OSError:pass


def document(snapshot:Snapshot,role:str)->dict[str,Any]:
    fd=snapshot.dup(role)
    try:
        with os.fdopen(fd,"rb",closefd=True) as raw, gzip.GzipFile(fileobj=raw,mode="rb") as stream:value=json.load(stream)
        need(type(value)is dict,"document:"+role);return value
    finally:
        try:os.close(fd)
        except OSError:pass


class SequenceHash:
    def __init__(self)->None:self.h=hashlib.sha256();self.h.update(b"[");self.count=0
    def add(self,value:str)->None:
        if self.count:self.h.update(b",")
        self.h.update(canonical(value));self.count+=1
    def finish(self)->str:
        copy=self.h.copy();copy.update(b"]");return copy.hexdigest()


class LedgerWriter:
    def __init__(self,path:Path)->None:
        self.path=path;self.count=0;self.ids=SequenceHash();self.hashes=SequenceHash();self.rows=hashlib.sha256();self.uncompressed=hashlib.sha256();self.uncompressed_size=0
        raw_fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600);self.raw=os.fdopen(raw_fd,"wb",buffering=0);self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.raw,compresslevel=9,mtime=0)
    def write(self,row:dict[str,Any])->None:
        wire=canonical(row)+b"\n";need(len(wire)<=8_388_609,"output row cap")
        row_id=row["row_id"];row_sha=row["row_sha256"]
        self.gz.write(wire);self.count+=1;self.ids.add(row_id);self.hashes.add(row_sha);self.rows.update(wire);self.uncompressed.update(wire);self.uncompressed_size+=len(wire)
    def close(self)->dict[str,Any]:
        self.gz.close();self.raw.close();raw=self.path.read_bytes()
        return {"row_count":self.count,"row_ids_sha256":self.ids.finish(),"row_hashes_sha256":self.hashes.finish(),"rows_sha256":self.rows.hexdigest(),"uncompressed_jsonl_sha256":self.uncompressed.hexdigest(),"uncompressed_jsonl_size":self.uncompressed_size,"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}


def make_row(kind:str,payload:dict[str,Any])->dict[str,Any]:
    body={"schema":SCHEMA+"."+kind+"-row.v1",**payload};row_id="round306c1-"+kind+":"+objsha(body);row={**body,"row_id":row_id};return {**row,"row_sha256":objsha(row)}


def support_ast(member_id:str,family:str)->dict[str,Any]:
    return {"ast_kind":"TYPED_FULL_SUPPORT_OBLIGATION","coarse_family":family,"member_id":member_id,"full_support_materialized":False,"outer_envelope_sufficient":False,"inner_witness_sufficient":False}


def grammar(family:str)->dict[str,Any]:
    return {"grammar":"C1_TYPED_SUPPORT_CERTIFICATE_V1","coarse_family":family,"requires":["SOURCE_AUTHORITY","A1_A2_WHERE_APPLICABLE","PHYSICAL_INCIDENCE_EQUIVALENCE","REPRESENTATION_PULLBACK"],"complete":False}


def input_commit(domain:str,payload:dict[str,Any])->str:return objsha({"domain":SCHEMA+"."+domain,**payload})


def source_sha()->str:
    path=Path(__file__);info=os.stat(path,follow_symlinks=False);need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,"source stat")
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:need(identity(os.fstat(fd))==identity(info),"source race");a=hash_fd(fd);b=hash_fd(fd);need(a==b,"source digest");return a
    finally:os.close(fd)


def write_json(path:Path,value:dict[str,Any])->dict[str,Any]:
    raw=canonical(value);fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
    try:os.write(fd,raw);os.fsync(fd)
    finally:os.close(fd)
    return {"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}


def build_candidate(snapshot:Snapshot,directory:Path,seed:int,producer_sha:str)->dict[str,Any]:
    need(type(seed)is int,"seed type")
    invalid=sorted(row["registry_member_id"] for row in jsonl(snapshot,"C0_INVALIDATION"));need(len(invalid)==len(set(invalid))==32,"invalid census")
    invalid_set=set(invalid);rekey_components=set()
    for row in jsonl(snapshot,"C0_ROOT_DISPOSITION"):
        if row["disposition"]=="REKEY_ROOT":rekey_components.add(row["old_component_id"])
    need(len(rekey_components)==4,"rekey components")
    c0:dict[str,tuple[str,str,str]]={}
    for row in jsonl(snapshot,"C0_MEMBER_COMPONENT"):
        member=row["registry_member_id"];need(member not in c0,"duplicate C0 member");c0[member]=(row["corrected_component_id"],row["row_id"],row["row_sha256"])
    need(len(c0)==564_460,"C0 member count")

    producer_commit={"filename":Path(__file__).name,"size":os.stat(__file__,follow_symlinks=False).st_size,"sha256":producer_sha}
    frontier_body={"schema":SCHEMA+".authority-frontier.v1","producer_source":producer_commit,"source_precedence":["SEALED_C0_CORRECTED_MEMBER_COMPONENT_AUTHORITY","DIRECT_I0_I1_I2_I3_IDENTITY_PROVENANCE_VIA_I4_MIGRATION_ROWS","B1G0_GRAPH_INCIDENCE_STATEMENTS_MIGRATION_ONLY","C1_NEW_ROWS_ZERO_CREDIT"],"pins":[pin.__dict__ for pin in PINS],"old_component_ids_are_provenance_only":True,"old_I4_or_B1G0_rows_have_formal_support_authority":False}
    frontier={**frontier_body,"authority_frontier_sha256":objsha(frontier_body)};meta:dict[str,dict[str,Any]]={"authority_frontier":write_json(directory/OUTPUTS["authority_frontier"],frontier)}
    obligation_body={"schema":SCHEMA+".theorem-obligation-census.v1","status":"EXACT_OBLIGATION_CENSUS_NOT_FEATURE_LEDGER_ROWS","root":{"preserved_non_graph_A1_A2":17_940,"R2_predicate_cells":295_340,"G2_graph_definitions":38_608,"total":351_888},"dependent":{"preserved_non_graph_A1_A2":62_152,"R2_member_pullbacks":295_336,"G2_graph_sheet_identifications":38_608,"G2_graph_side_incidences":76_816,"total":472_912},"corrected_total":824_800,"known_final_feature_ledger_row_count":None,"formal_credit":dict(ZERO_CREDIT)}
    obligation={**obligation_body,"obligation_census_sha256":objsha(obligation_body)};meta["obligation_census"]=write_json(directory/OUTPUTS["obligation_census"],obligation)

    member_writer=LedgerWriter(directory/OUTPUTS["member"]);member_refs:dict[str,dict[str,Any]]={};family_member_ids={f:SequenceHash() for f in FAMILIES};family_member_sources={f:SequenceHash() for f in FAMILIES};member_counts=Counter();missing=[]
    for old in jsonl(snapshot,"I4_MEMBER"):
        family=old["coarse_family"];member=old["member_id"]
        if member not in c0:missing.append(member);continue
        component,c0_row,c0_sha=c0[member];ci=old["canonical_input_commitment"]
        ast=support_ast(member,family);cert=grammar(family)
        commitment=input_commit("member-input.v1",{"legacy_I4_row_sha256":old["row_sha256"],"member_id":member,"family":family,"c0_member_row_sha256":c0_sha,"producer_sha256":producer_sha})
        payload={"member_id":member,"coarse_family":family,"primitive_source_kind":family+"_PRIMITIVE_SOURCE","source_authority_role":"I4_MIGRATION_REFERENCE_TO_"+ci["source_lane"],"source_filename":ci["source_member_file"],"source_table":"JSONL_MEMBER_INDEX","source_path":"/member_id/"+member,"source_row_id":member,"source_row_sha256":old["row_sha256"],"r235d_disposition":"SURVIVES_C0_CORRECTED_MEMBER_UNIVERSE","c0_member_component_row_id":c0_row,"c0_member_component_row_sha256":c0_sha,"corrected_component_id":component,"typed_support_ast":ast,"certificate_grammar":cert,"mechanical_representation_count":old["mechanical_representation_count"],"mechanical_representation_ids_sha256":old["mechanical_representation_set_sha256"],"primary_mechanical_representation_id":old["primary_mechanical_representation_id"],"support_semantic_state":"MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("member-identity-support",payload);member_writer.write(row);member_counts[family]+=1;family_member_ids[family].add(member);family_member_sources[family].add(old["row_sha256"])
        member_refs[member]={"family":family,"row_id":row["row_id"],"row_sha256":row["row_sha256"],"component":component,"ast_sha":objsha(ast),"representation_sha":old["mechanical_representation_set_sha256"],"old_component":old["Round306A_component_id"],"old_row_sha":old["row_sha256"],"c0_row":c0_row,"c0_sha":c0_sha}
    need(sorted(missing)==invalid,"missing exact invalid set");need(dict(member_counts)==EXPECTED_MEMBERS,"member family census");meta["member"]=member_writer.close()

    rep_writer=LedgerWriter(directory/OUTPUTS["representation"]);rep_counts=Counter();family_rep_ids={f:SequenceHash() for f in FAMILIES};family_rep_sources={f:SequenceHash() for f in FAMILIES}
    for old in jsonl(snapshot,"I4_REPRESENTATION"):
        owner=old["owner_member_id"]
        if owner not in member_refs:continue
        family=old["coarse_family"];ci=old["canonical_input_commitment"];owner_ref=member_refs[owner];rep=old["representation_id"]
        commitment=input_commit("representation-input.v1",{"legacy_I4_row_sha256":old["row_sha256"],"representation_id":rep,"owner_member_id":owner,"owner_member_row_sha256":owner_ref["row_sha256"],"producer_sha256":producer_sha})
        payload={"representation_id":rep,"owner_member_id":owner,"coarse_family":family,"representation_role":old["representation_role"],"source_authority_role":"I4_MIGRATION_REFERENCE_TO_"+ci["source_lane"],"source_filename":ci["source_representation_file"],"source_table":"JSONL_REPRESENTATION_INDEX","source_path":"/representation_id/"+rep,"source_row_id":rep,"source_row_sha256":old["row_sha256"],"typed_representation_ast":{"ast_kind":"TYPED_MECHANICAL_REPRESENTATION","representation_id":rep,"owner_member_id":owner,"role":old["representation_role"]},"certificate_grammar":grammar(family),"pullback_semantic_state":"PULLBACK_EQUIVALENCE_NOT_PROVED","owner_member_row_id":owner_ref["row_id"],"owner_member_row_sha256":owner_ref["row_sha256"],"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("representation",payload);rep_writer.write(row);rep_counts[family]+=1;family_rep_ids[family].add(rep);family_rep_sources[family].add(old["row_sha256"])
    need(dict(rep_counts)==EXPECTED_REPS,"representation family census");meta["representation"]=rep_writer.close()

    family_writer=LedgerWriter(directory/OUTPUTS["family_census"])
    for family in FAMILIES:
        source_commit=objsha({"member_source_rows_sha256":family_member_sources[family].finish(),"representation_source_rows_sha256":family_rep_sources[family].finish()})
        commitment=input_commit("family-input.v1",{"family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"source_authority_commitment_sha256":source_commit})
        family_writer.write(make_row("family-census",{"coarse_family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"member_ids_sha256":family_member_ids[family].finish(),"representation_ids_sha256":family_rep_ids[family].finish(),"source_authority_commitment_sha256":source_commit,"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}))
    meta["family_census"]=family_writer.close();need(meta["family_census"]["row_count"]==6,"family rows")

    graph_doc=document(snapshot,"B1G0_GRAPH");graph_rows=graph_doc["graph_source_inventory_rows"];graph_map={row["Round306B1G0_graph_source_inventory_row_id"]:row for row in graph_rows};need(len(graph_map)==38_624,"graph map")
    incidence_writer=LedgerWriter(directory/OUTPUTS["physical_incidence"]);incidence_refs:dict[str,dict[str,str]]={}
    sheet_doc=document(snapshot,"B1G0_SHEET");sheet_selected=[row for row in sheet_doc["graph_sheet_join_rows"] if row["sheet_member_id"] in member_refs];need(len(sheet_selected)==38_608,"sheet selected")
    for old in sheet_selected:
        member=old["sheet_member_id"];m=member_refs[member];g=graph_map[old["graph_source_inventory_row_id"]];source_id=old["Round306B1G0_graph_sheet_join_row_id"]
        commitment=input_commit("incidence-input.v1",{"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_sha256":old["row_sha256"],"member_row_sha256":m["row_sha256"]})
        row=make_row("physical-incidence-statement",{"graph_id":old["graph_id"],"incidence_role":"GRAPH_TO_SHEET","member_id":member,"coarse_family":"G2A","source_graph_row_id":g["Round306B1G0_graph_source_inventory_row_id"],"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_id":source_id,"source_incidence_row_sha256":old["row_sha256"],"member_row_id":m["row_id"],"member_row_sha256":m["row_sha256"],"incidence_statement_ast":{"ast_kind":"GRAPH_SHEET_INCIDENCE_STATEMENT","graph_id":old["graph_id"],"member_id":member,"proved":False},"theorem_semantic_state":"PHYSICAL_IDENTIFICATION_THEOREM_PENDING","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)});incidence_writer.write(row);incidence_refs[source_id]={"row_id":row["row_id"],"row_sha256":row["row_sha256"]}
    del sheet_doc,sheet_selected
    side_doc=document(snapshot,"B1G0_SIDE");side_by_member:dict[str,dict[str,Any]]={};valid_side_refs=0
    for old in side_doc["graph_side_join_rows"]:
        member=old["side_member_id"]
        if member not in member_refs:continue
        valid_side_refs+=1;prior=side_by_member.get(member)
        if prior is None or old["Round306B1G0_graph_side_join_row_id"]<prior["Round306B1G0_graph_side_join_row_id"]:side_by_member[member]=old
    need(valid_side_refs==76_832 and len(side_by_member)==76_816,"side dedupe")
    for member in sorted(side_by_member):
        old=side_by_member[member];m=member_refs[member];g=graph_map[old["graph_source_inventory_row_id"]];source_id=old["Round306B1G0_graph_side_join_row_id"]
        commitment=input_commit("incidence-input.v1",{"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_sha256":old["row_sha256"],"member_row_sha256":m["row_sha256"]})
        row=make_row("physical-incidence-statement",{"graph_id":old["graph_id"],"incidence_role":"GRAPH_TO_SIDE","member_id":member,"coarse_family":"G2B","source_graph_row_id":g["Round306B1G0_graph_source_inventory_row_id"],"source_graph_row_sha256":g["row_sha256"],"source_incidence_row_id":source_id,"source_incidence_row_sha256":old["row_sha256"],"member_row_id":m["row_id"],"member_row_sha256":m["row_sha256"],"incidence_statement_ast":{"ast_kind":"GRAPH_SIDE_INCIDENCE_STATEMENT","graph_id":old["graph_id"],"member_id":member,"side_role":old["side_role"],"proved":False},"theorem_semantic_state":"POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)});incidence_writer.write(row);incidence_refs[source_id]={"row_id":row["row_id"],"row_sha256":row["row_sha256"]}
    meta["physical_incidence"]=incidence_writer.close();need(meta["physical_incidence"]["row_count"]==115_424,"incidence count");del side_doc

    gap_doc=document(snapshot,"B1G0_GAP");ordinary=[];side_gaps:dict[str,dict[str,Any]]={}
    for old in gap_doc["gap_rows"]:
        member=old["member_id"]
        if member not in member_refs:continue
        if old["gap_kind"]=="GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING":
            if old["incidence_join_row_id"]!=side_by_member[member]["Round306B1G0_graph_side_join_row_id"]:continue
            prior=side_gaps.get(member)
            if prior is None or old["Round306B1G0_gap_row_id"]<prior["Round306B1G0_gap_row_id"]:side_gaps[member]=old
        else:ordinary.append(old)
    selected_gaps=ordinary+[side_gaps[m] for m in sorted(side_gaps)];selected_gaps.sort(key=lambda row:(FAMILIES.index(member_refs[row["member_id"]]["family"]),row["Round306B1G0_gap_row_id"]))
    need(len(selected_gaps)==154_032,"gap count");gap_writer=LedgerWriter(directory/OUTPUTS["gap"])
    for old in selected_gaps:
        member=old["member_id"];m=member_refs[member];source_incidence=old["incidence_join_row_id"]
        if source_incidence is None:subject_kind="GRAPH_DEFINITION";subject_row=old["graph_source_inventory_row_id"]
        else:subject_kind="PHYSICAL_INCIDENCE";need(source_incidence in incidence_refs,"selected incidence gap binding");subject_row=incidence_refs[source_incidence]["row_id"]
        commitment=input_commit("gap-input.v1",{"source_gap_row_sha256":old["row_sha256"],"subject_row_id":subject_row,"member_row_sha256":m["row_sha256"]})
        gap_writer.write(make_row("semantic-gap",{"gap_kind":old["gap_kind"],"subject_kind":subject_kind,"subject_row_id":subject_row,"member_id":member,"coarse_family":m["family"],"required_closure":old["required_closure"],"source_statement_row_id":old["Round306B1G0_gap_row_id"],"source_statement_row_sha256":old["row_sha256"],"blocking_credit_kinds":["normalized_support","physical_incidence","representation_cover","B1A"],"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}))
    meta["gap"]=gap_writer.close();del gap_doc,selected_gaps,ordinary,side_gaps,graph_doc,graph_rows,graph_map,incidence_refs

    rebind_writer=LedgerWriter(directory/OUTPUTS["component_rebind"]);transition_writer=LedgerWriter(directory/OUTPUTS["transition_handle"]);rebind_counts=Counter()
    for member,m in member_refs.items():
        if m["old_component"] in rekey_components:
            commitment=input_commit("rebind-input.v1",{"member_id":member,"old_component_id":m["old_component"],"c0_member_row_sha256":m["c0_sha"],"corrected_component_id":m["component"]})
            rebind_writer.write(make_row("affected-component-rebind",{"member_id":member,"coarse_family":m["family"],"old_component_id_provenance_only":m["old_component"],"old_component_row_sha256":m["old_row_sha"],"c0_member_component_row_id":m["c0_row"],"c0_member_component_row_sha256":m["c0_sha"],"corrected_component_id":m["component"],"rebind_reason":"SURVIVOR_OF_R235D_AFFECTED_OLD_COMPONENT_REBOUND_TO_FRESH_C0_COMPONENT","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}));rebind_counts[m["family"]]+=1
        commitment=input_commit("transition-handle-input.v1",{"member_id":member,"member_row_sha256":m["row_sha256"],"typed_support_ast_sha256":m["ast_sha"],"representation_set_sha256":m["representation_sha"],"corrected_component_id":m["component"]})
        transition_writer.write(make_row("transition-ready-handle",{"member_id":member,"coarse_family":m["family"],"member_row_id":m["row_id"],"member_row_sha256":m["row_sha256"],"typed_support_ast_sha256":m["ast_sha"],"representation_set_sha256":m["representation_sha"],"corrected_component_id":m["component"],"transition_syntax_ready":True,"transition_semantics_ready":False,"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}))
    need(dict(rebind_counts)==EXPECTED_REBINDS,"rebind family counts");meta["component_rebind"]=rebind_writer.close();meta["transition_handle"]=transition_writer.close();need(meta["component_rebind"]["row_count"]==21_848 and meta["transition_handle"]["row_count"]==564_460,"rebind/transition counts")

    descriptors=[]
    for role in OUTPUT_ORDER[:-1]:
        if role not in meta:
            raw=(directory/OUTPUTS[role]).read_bytes();meta[role]={"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
        descriptors.append({"role":role,"filename":OUTPUTS[role],"size":meta[role]["size"],"sha256":meta[role]["sha256"]})
    result_body={"schema":SCHEMA+".result.v1","status":"PASS_CORRECTED_SIX_FAMILY_MECHANICAL_REPLAY_CANDIDATE__ZERO_SUPPORT_CREDIT","producer_source":producer_commit,"authority_frontier_sha256":frontier["authority_frontier_sha256"],"corrected_census":{"member_count":564_460,"representation_count":611_872,"physical_incidence_count":115_424,"semantic_gap_count":154_032,"affected_component_rebind_count":21_848,"transition_handle_count":564_460,"family_member_counts":dict(member_counts),"family_representation_counts":dict(rep_counts)},"exact_C0_invalid_member_ids_sha256":objsha(invalid),"valid_side_reference_count":valid_side_refs,"unique_side_member_count":len(side_by_member),"duplicate_side_reference_excess":valid_side_refs-len(side_by_member),"ledger_receipts":{role:{k:v for k,v in value.items() if k not in {"size","sha256"}} for role,value in meta.items() if "row_count" in value},"output_artifacts_in_publication_order_before_result":descriptors,"formal_credit":dict(ZERO_CREDIT),"normalized_support_sealed":False,"B1A_permitted":False,"B2_permitted":False,"CM2":"NO-GO_FOR_CLAIM","seed_serialized_or_semantically_used":False}
    result={**result_body,"result_sha256":objsha(result_body)};meta["result"]=write_json(directory/OUTPUTS["result"],result)
    return {"descriptors":meta,"result_sha256":result["result_sha256"],"corrected_partition_basis":"C0_MANIFEST:"+next(pin.sha256 for pin in PINS if pin.role=="C0_MANIFEST")}


def compare_dirs(left:Path,right:Path)->None:
    need(set(os.listdir(left))==set(OUTPUTS.values())==set(os.listdir(right)),"dual candidate names")
    for role in OUTPUT_ORDER:
        a=(left/OUTPUTS[role]).read_bytes();b=(right/OUTPUTS[role]).read_bytes();need(a==b,"dual seed bytes:"+role)


def cleanup(path:Path)->None:
    if path.exists():
        for entry in path.iterdir():entry.unlink()
        path.rmdir()


def publish(source:Path,target_value:str)->dict[str,Any]:
    target=Path(os.path.abspath(target_value));deliverables=ROOT.resolve(strict=True);need(os.path.commonpath((str(target),str(deliverables)))!=str(deliverables),"candidate outside deliverables")
    parent=target.parent;parent_fd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        os.mkdir(target.name,0o700,dir_fd=parent_fd);dirfd=os.open(target.name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent_fd)
        try:
            for role in OUTPUT_ORDER:os.rename(source/OUTPUTS[role],OUTPUTS[role],dst_dir_fd=dirfd)
            need(set(os.listdir(dirfd))==set(OUTPUTS.values()),"published exact set")
            hashes={}
            for role in reversed(OUTPUT_ORDER):
                info=os.stat(OUTPUTS[role],dir_fd=dirfd,follow_symlinks=False);need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,"published regular:"+role)
                fd=os.open(OUTPUTS[role],os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=dirfd)
                try:hashes[role]=hash_fd(fd)
                finally:os.close(fd)
            return {"status":"PASS_C1_RESULT_LAST_PUBLICATION_REVERSE_REVALIDATED","artifact_count":10,"artifact_sha256":hashes}
        finally:os.close(dirfd)
    finally:os.close(parent_fd)


def production(candidate:str|None,no_write:bool,seed:int)->dict[str,Any]:
    producer_sha=source_sha();Path(FIXED_SPILL).mkdir(mode=0o700,parents=True,exist_ok=True);first=Path(tempfile.mkdtemp(prefix="seed-a.",dir=FIXED_SPILL));second=Path(tempfile.mkdtemp(prefix="seed-b.",dir=FIXED_SPILL))
    with Snapshot() as snapshot:
        try:
            a=build_candidate(snapshot,first,seed,producer_sha);build_candidate(snapshot,second,seed^0x5A5A5A5A5A5A5A5A,producer_sha);compare_dirs(first,second);snapshot.final()
            if no_write:return {"status":"PASS_C1_DUAL_SEED_BYTE_IDENTICAL_NO_WRITE","artifact_count":10,"result_sha256":a["result_sha256"],"candidate_publication_attempted":False}
            need(type(candidate)is str and candidate!="","candidate required");return publish(first,candidate)
        finally:cleanup(first);cleanup(second)


def main()->int:
    need(type(sys.flags.isolated)is int and sys.flags.isolated==1,"python -I required");need(sys.dont_write_bytecode is True,"python -B required")
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--candidate-dir");parser.add_argument("--no-write",action="store_true");parser.add_argument("--seed",type=int,default=0);args=parser.parse_args();need((args.candidate_dir is not None)!=args.no_write,"one mode");need(type(args.seed)is int and 0<=args.seed<2**63,"seed")
    print(json.dumps(production(args.candidate_dir,args.no_write,args.seed),sort_keys=True,separators=(",",":")));return 0


if __name__=="__main__":raise SystemExit(main())
