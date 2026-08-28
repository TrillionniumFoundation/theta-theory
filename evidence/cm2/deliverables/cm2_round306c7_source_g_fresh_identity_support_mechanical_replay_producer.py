#!/usr/bin/env python3
"""Produce the zero-credit Round306C7 fresh identity/support replay."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
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
PREFIX: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay"
SCHEMA: Final = "cm2.round306c7.source-g-fresh-identity-support-mechanical-replay.v1"
FIXED_SPILL: Final = "/tmp/cm2-round306c7-spill"
FAMILIES: Final = ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")
OUTPUTS: Final = {
    "family_census": PREFIX + "_family_census.jsonl.gz",
    "member": PREFIX + "_member_identity_support_ledger.jsonl.gz",
    "representation": PREFIX + "_representation_ledger.jsonl.gz",
    "physical_incidence": PREFIX + "_physical_incidence_statement_ledger.jsonl.gz",
    "gap": PREFIX + "_semantic_gap_ledger.jsonl.gz",
    "component_rebind": PREFIX + "_component_rebind_ledger.jsonl.gz",
    "transition_handle": PREFIX + "_transition_ready_handle_ledger.jsonl.gz",
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
    Pin("C1_MANIFEST", "cm2_round306c1_source_g_corrected_identity_support_replay_manifest.sha256", 2_398, "9adfc1499f2c376085b1e7166cce43e41374ac81f4f10ad87409b0d9b14e4b7c"),
    Pin("C1_RESULT", "cm2_round306c1_source_g_corrected_identity_support_replay_result.json", 6_534, "fc23235883e7c97dd63e1324114b9e8a17e21c3ec9383e6bfab60a078215ea09"),
    Pin("C1_MEMBER", "cm2_round306c1_source_g_corrected_identity_support_replay_member_identity_support_ledger.jsonl.gz", 245_137_577, "7833d0bf74b3252a4258695972b4e92845defb2640dace6b9bd1850a0db89497"),
    Pin("C1_REPRESENTATION", "cm2_round306c1_source_g_corrected_identity_support_replay_representation_ledger.jsonl.gz", 217_157_865, "2cc7f2baa97d0cc0579663d5ab7d67c17eb0f9aaccb1489e5c8073382118fd94"),
    Pin("C1_INCIDENCE", "cm2_round306c1_source_g_corrected_identity_support_replay_physical_incidence_statement_ledger.jsonl.gz", 53_797_275, "9cb4ed9467f13f0cec9199a5ad29b716457465bc1c6fb2a77bbaa7aba2a27f04"),
    Pin("C1_GAP", "cm2_round306c1_source_g_corrected_identity_support_replay_semantic_gap_ledger.jsonl.gz", 43_187_989, "feb43759887a642a1d00350218015c801d1a8e1d0b410aa873db3415d9913aa3"),
    Pin("C1_HANDLE", "cm2_round306c1_source_g_corrected_identity_support_replay_transition_ready_handle_ledger.jsonl.gz", 203_902_224, "6511933445169756b8d409d3a8dd57cfd1b894a77e758f301481679ea31306f9"),
    Pin("C4_MANIFEST", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_manifest.sha256", 1_177, "5550eb9cf4e474a8d08086062e28538e909f6e1c7e499ba10a78a2d24e683de6"),
    Pin("C4_RESULT", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_result.json", 6_204, "1396fadf4ef85340bdc0b1ca3b191a67a8266ed40cc3ee9a3dcc8f9650ffb8da"),
    Pin("C4_BRIDGE", "cm2_round306c4_source_g_r235d_to_g2_orphan_graph_semantic_bridge_row_ledger.jsonl.gz", 101_147, "3b273e7637af99e19a23ec62a29999023d73aba9a901fe4311fc631aae0cc6db"),
    Pin("C5_MANIFEST", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_manifest.sha256", 1_193, "aefe82ef88c2ddf5f241d76e0f0f7483e230d68219ace6639f7389adbcb14134"),
    Pin("C5_RESULT", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_result.json", 6_975, "0da7931e1a46d68ae8da69a7de1534a3955c83a8d6f5d8ab0170be7a34dc6320"),
    Pin("C5_SEMANTIC", "cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", 78_082_824, "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    Pin("C6_MANIFEST", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256", 2_211, "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
    Pin("C6_RESULT", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_result.json", 9_329, "3f4e3e666dfe0b5b3a163c866057031b42dac09000175f4bc0b32ec353c5e4c5"),
    Pin("C6_MEMBER", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213_125_489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
)

EXPECTED_MEMBERS: Final = {"PRESERVED":126_468,"NON_GRAPH":51_172,"R2":295_336,"R292":9_404,"G2A":5_264,"G2B":10_128}
EXPECTED_REPS: Final = {"PRESERVED":165_744,"NON_GRAPH":51_172,"R2":302_624,"R292":10_252,"G2A":5_264,"G2B":10_128}
EXPECTED_PHYSICAL: Final = {"G2A":5_264,"G2B":10_128}
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
                value=json.loads(line);need(type(value)is dict and canonical(value)+b"\n"==line,"canonical:"+role+":"+str(ordinal))
                need(type(value.get("row_sha256")) is str,"closed row fields:"+role+":"+str(ordinal))
                body={key:item for key,item in value.items() if key!="row_sha256"};need(objsha(body)==value["row_sha256"],"closed row sha:"+role+":"+str(ordinal));yield value
    finally:
        try:os.close(fd)
        except OSError:pass


def plain_document(snapshot:Snapshot,role:str)->dict[str,Any]:
    fd=snapshot.dup(role)
    try:
        with os.fdopen(fd,"rb",closefd=True) as stream:raw=stream.read()
        value=json.loads(raw);need(type(value)is dict and canonical(value)==raw,"document:"+role);return value
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
    body={"schema":SCHEMA+"."+kind+"-row.v1",**payload};row_id="round306c7-"+kind+":"+objsha(body);row={**body,"row_id":row_id};return {**row,"row_sha256":objsha(row)}


def support_ast(member_id:str,family:str)->dict[str,Any]:
    return {"ast_kind":"TYPED_FULL_SUPPORT_OBLIGATION","coarse_family":family,"member_id":member_id,"fresh_member_universe":"ROUND306C6","full_support_materialized":False,"outer_envelope_sufficient":False,"inner_witness_sufficient":False}


def grammar(family:str)->dict[str,Any]:
    return {"grammar":"C7_FRESH_TYPED_SUPPORT_CERTIFICATE_V1","coarse_family":family,"requires":["C6_FRESH_MEMBER_AND_COMPONENT_AUTHORITY","SOURCE_AUTHORITY","A1_A2_WHERE_APPLICABLE","PHYSICAL_INCIDENCE_EQUIVALENCE","REPRESENTATION_PULLBACK"],"complete":False}


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
    c1_result=plain_document(snapshot,"C1_RESULT");c4_result=plain_document(snapshot,"C4_RESULT");c5_result=plain_document(snapshot,"C5_RESULT");c6_result=plain_document(snapshot,"C6_RESULT")
    need(c1_result["schema"]=="cm2.round306c1.source-g-corrected-identity-support-replay.v1.result.v1","C1 result schema")
    need(c1_result["status"]=="PASS_CORRECTED_SIX_FAMILY_MECHANICAL_REPLAY_CANDIDATE__ZERO_SUPPORT_CREDIT","C1 result status")
    need(c1_result["corrected_census"]["member_count"]==564_460 and c1_result["corrected_census"]["representation_count"]==611_872,"C1 result census")
    need(c4_result["schema"]=="cm2.round306c4.source-g-r235d-to-g2-orphan-graph-semantic-bridge.v1","C4 result schema")
    need(c4_result["status"]=="PASS_16_R235D_TO_G2_ORPHAN_TARGET_GRAPH_EMPTY_DISPOSITIONS__ZERO_INCIDENCE_PULLBACK_TRACE_SUPPORT_CREDIT","C4 result status")
    need(c5_result["schema"]=="cm2.round306c5.source-g-corrected-g2-graph-semantic-classification.v1","C5 result schema")
    need(c5_result["status"]=="PASS_5264_POSITIVE_G2_GRAPH_DEFINITIONS__33344_R235_EMPTY_GRAPH_DISPOSITIONS__FRESH_DSU_REQUIRED","C5 result status")
    need(c6_result["schema"]=="cm2.round306c6.source-g-corrected-g2-invalidation-fresh-dsu-freeze.v1","C6 result schema")
    need(c6_result["status"]=="PASS_66688_G2_MEMBER_INVALIDATIONS__476118_RETAINED_EDGES__61928_FRESH_COMPONENTS__ZERO_CREDIT_PENDING_INDEPENDENT_VERIFICATION","C6 result status")
    producer_commit={"filename":Path(__file__).name,"size":os.stat(__file__,follow_symlinks=False).st_size,"sha256":producer_sha}

    c6_members:dict[str,dict[str,str]]={}
    for old in jsonl(snapshot,"C6_MEMBER"):
        member=old["registry_member_id"];need(member not in c6_members,"duplicate C6 member")
        c6_members[member]={"component":old["fresh_component_id"],"row_id":old["row_id"],"row_sha256":old["row_sha256"],"root":old["new_base_root_id"]}
    need(len(c6_members)==497_772,"C6 member count")

    orphan_graphs:dict[str,dict[str,str]]={}
    for old in jsonl(snapshot,"C4_BRIDGE"):
        disposition=old["G2_orphan_graph_disposition"];graph=disposition["C3_orphan_target_graph_id"]
        need(graph not in orphan_graphs and disposition["disposition"]=="EMPTY_GRAPH_ON_COMPLETE_PARAMETER_DOMAIN" and disposition["C3_graph_definition_blocker_resolved"]==1,"C4 orphan disposition")
        orphan_graphs[graph]={"row_id":old["bridge_row_id"],"row_sha256":old["row_sha256"],"graph_id":graph,"graph_inventory_row_id":disposition["C3_orphan_target_graph_inventory_row_id"]}
    need(len(orphan_graphs)==16,"C4 orphan graph count")

    positive_graphs:dict[str,dict[str,str]]={};empty_surviving:dict[str,dict[str,str]]={};invalid_candidates:set[str]=set();c5_counts=Counter()
    for old in jsonl(snapshot,"C5_SEMANTIC"):
        graph=old["graph_id"];semantic=old["semantic_classification"];classification=semantic["classification"];c5_counts[classification]+=1
        ref={"row_id":old["semantic_row_id"],"row_sha256":old["row_sha256"],"graph_id":graph}
        if classification=="POSITIVE_GRAPH":
            need(graph not in positive_graphs,"duplicate positive graph");need(semantic["graph_definition_credit"]==1,"positive graph credit")
            positive_graphs[graph]=ref
        elif classification=="EMPTY_GRAPH":
            need(semantic["graph_definition_disposition_credit"]==1,"empty graph credit")
            sheet=semantic["invalid_sheet_member_candidate"];invalid_side=semantic["invalid_side_member_candidate"];survivor=semantic["surviving_side_member"]
            need(sheet!=invalid_side and sheet!=survivor and invalid_side!=survivor,"empty member roles")
            invalid_candidates.add(sheet);invalid_candidates.add(invalid_side);need(survivor not in empty_surviving,"duplicate empty survivor")
            empty_surviving[survivor]={**ref,"surviving_side_role":semantic["surviving_side_role"]}
        else:raise Blocked("unknown C5 classification")
    need(dict(c5_counts)=={"POSITIVE_GRAPH":5_264,"EMPTY_GRAPH":33_344},"C5 classification census")
    need(len(positive_graphs)==5_264 and len(empty_surviving)==33_344 and len(invalid_candidates)==66_688,"C5 member effects")
    need(invalid_candidates.isdisjoint(c6_members) and set(empty_surviving).issubset(c6_members),"C5/C6 survivor partition")

    meta:dict[str,dict[str,Any]]={}
    member_writer=LedgerWriter(directory/OUTPUTS["member"]);member_refs:dict[str,dict[str,Any]]={};member_counts=Counter();legacy_member_counts=Counter()
    family_member_ids={family:SequenceHash() for family in FAMILIES};family_member_sources={family:SequenceHash() for family in FAMILIES};missing:set[str]=set()
    for old in jsonl(snapshot,"C1_MEMBER"):
        member=old["member_id"];legacy_family=old["coarse_family"];legacy_member_counts[legacy_family]+=1
        c6=c6_members.get(member)
        if c6 is None:missing.add(member);continue
        family="NON_GRAPH" if member in empty_surviving else legacy_family
        if family!=legacy_family:need(legacy_family=="G2B","only G2B may be reclassified")
        ast=support_ast(member,family);cert=grammar(family);semantic_ref=empty_surviving.get(member)
        commitment=input_commit("member-input.v1",{"C1_row_sha256":old["row_sha256"],"C6_row_sha256":c6["row_sha256"],"C5_empty_graph_row_sha256":None if semantic_ref is None else semantic_ref["row_sha256"],"member_id":member,"fresh_family":family,"producer_sha256":producer_sha})
        payload={"member_id":member,"coarse_family":family,"legacy_C1_coarse_family":legacy_family,"family_transition":"G2B_TO_NON_GRAPH_BY_C5_EMPTY_GRAPH_DISPOSITION" if family!=legacy_family else "PRESERVED_FROM_C1","primitive_source_kind":"C5_EMPTY_GRAPH_SURVIVING_SIDE_NON_GRAPH_SOURCE" if family!=legacy_family else old["primitive_source_kind"],"source_authority_role":old["source_authority_role"],"source_filename":old["source_filename"],"source_table":old["source_table"],"source_path":old["source_path"],"source_row_id":old["source_row_id"],"source_row_sha256":old["source_row_sha256"],"C1_member_row_id":old["row_id"],"C1_member_row_sha256":old["row_sha256"],"C6_member_component_row_id":c6["row_id"],"C6_member_component_row_sha256":c6["row_sha256"],"fresh_component_id":c6["component"],"fresh_base_root_id":c6["root"],"C5_empty_graph_semantic_row_id":None if semantic_ref is None else semantic_ref["row_id"],"C5_empty_graph_semantic_row_sha256":None if semantic_ref is None else semantic_ref["row_sha256"],"typed_support_ast":ast,"certificate_grammar":cert,"mechanical_representation_count":old["mechanical_representation_count"],"mechanical_representation_ids_sha256":old["mechanical_representation_ids_sha256"],"primary_mechanical_representation_id":old["primary_mechanical_representation_id"],"support_semantic_state":"FRESH_MECHANICAL_IDENTITY_ONLY__FULL_SUPPORT_NOT_PROVED","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("member-identity-support",payload);member_writer.write(row);member_counts[family]+=1;family_member_ids[family].add(member);family_member_sources[family].add(old["row_sha256"])
        need(member not in member_refs,"duplicate C1 survivor")
        member_refs[member]={"family":family,"legacy_family":legacy_family,"row_id":row["row_id"],"row_sha256":row["row_sha256"],"component":c6["component"],"c6_row_id":c6["row_id"],"c6_row_sha256":c6["row_sha256"],"old_component":old["corrected_component_id"],"old_row_id":old["row_id"],"old_row_sha256":old["row_sha256"],"ast_sha256":objsha(ast),"representation_set_sha256":old["mechanical_representation_ids_sha256"]}
    need(dict(legacy_member_counts)=={"PRESERVED":126_468,"NON_GRAPH":17_828,"R2":295_336,"R292":9_404,"G2A":38_608,"G2B":76_816},"legacy member census")
    need(missing==invalid_candidates,"exact C5 invalid set");need(set(member_refs)==set(c6_members),"C1/C6 survivor equality");need(dict(member_counts)==EXPECTED_MEMBERS,"fresh member census")
    meta["member"]=member_writer.close();need(meta["member"]["row_count"]==497_772,"member rows")

    rep_writer=LedgerWriter(directory/OUTPUTS["representation"]);rep_counts=Counter();legacy_rep_counts=Counter()
    family_rep_ids={family:SequenceHash() for family in FAMILIES};family_rep_sources={family:SequenceHash() for family in FAMILIES}
    for old in jsonl(snapshot,"C1_REPRESENTATION"):
        owner=old["owner_member_id"];legacy_rep_counts[old["coarse_family"]]+=1;member_ref=member_refs.get(owner)
        if member_ref is None:continue
        family=member_ref["family"];need(old["coarse_family"]==member_ref["legacy_family"],"representation legacy family")
        rep=old["representation_id"];commitment=input_commit("representation-input.v1",{"C1_row_sha256":old["row_sha256"],"owner_member_row_sha256":member_ref["row_sha256"],"fresh_family":family,"representation_id":rep})
        payload={"representation_id":rep,"owner_member_id":owner,"coarse_family":family,"legacy_C1_coarse_family":old["coarse_family"],"representation_role":old["representation_role"],"source_authority_role":old["source_authority_role"],"source_filename":old["source_filename"],"source_table":old["source_table"],"source_path":old["source_path"],"source_row_id":old["source_row_id"],"source_row_sha256":old["source_row_sha256"],"C1_representation_row_id":old["row_id"],"C1_representation_row_sha256":old["row_sha256"],"owner_member_row_id":member_ref["row_id"],"owner_member_row_sha256":member_ref["row_sha256"],"typed_representation_ast":{"ast_kind":"TYPED_MECHANICAL_REPRESENTATION","representation_id":rep,"owner_member_id":owner,"role":old["representation_role"],"fresh_member_universe":"ROUND306C6"},"certificate_grammar":grammar(family),"pullback_semantic_state":"PULLBACK_EQUIVALENCE_NOT_PROVED","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("representation",payload);rep_writer.write(row);rep_counts[family]+=1;family_rep_ids[family].add(rep);family_rep_sources[family].add(old["row_sha256"])
    need(dict(legacy_rep_counts)=={"PRESERVED":165_744,"NON_GRAPH":17_828,"R2":302_624,"R292":10_252,"G2A":38_608,"G2B":76_816},"legacy representation census")
    need(dict(rep_counts)==EXPECTED_REPS,"fresh representation census");meta["representation"]=rep_writer.close();need(meta["representation"]["row_count"]==545_184,"representation rows")

    incidence_writer=LedgerWriter(directory/OUTPUTS["physical_incidence"]);incidence_refs:dict[str,dict[str,str]]={};incidence_counts=Counter();incidence_relations:set[tuple[str,str,str,str]]=set()
    family_incidence_ids={family:SequenceHash() for family in FAMILIES};family_incidence_sources={family:SequenceHash() for family in FAMILIES};valid_nonpositive_relations=0;semantic_authority_counts=Counter()
    for old in jsonl(snapshot,"C1_INCIDENCE"):
        member=old["member_id"];member_ref=member_refs.get(member)
        if member_ref is None:continue
        semantic_ref=positive_graphs.get(old["graph_id"]);bridge_ref=orphan_graphs.get(old["graph_id"])
        if semantic_ref is None and bridge_ref is None:valid_nonpositive_relations+=1;need(member in empty_surviving and old["incidence_role"]=="GRAPH_TO_SIDE","valid nonpositive relation");continue
        need(not (semantic_ref is not None and bridge_ref is not None),"disjoint graph authority");family=member_ref["family"];need(family in {"G2A","G2B"} and old["coarse_family"]==family,"retained incidence family")
        if bridge_ref is not None:need(family=="G2B" and old["source_graph_row_id"]==bridge_ref["graph_inventory_row_id"],"C4 bridge incidence binding")
        relation=(old["graph_id"],old["incidence_role"],old["source_incidence_row_id"],member);need(relation not in incidence_relations,"duplicate incidence relation");incidence_relations.add(relation)
        authority_kind="C5_POSITIVE_GRAPH_DEFINITION" if semantic_ref is not None else "C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION";authority_ref=semantic_ref if semantic_ref is not None else bridge_ref;semantic_authority_counts[authority_kind]+=1
        commitment=input_commit("physical-incidence-input.v1",{"C1_incidence_row_sha256":old["row_sha256"],"graph_semantic_authority_kind":authority_kind,"graph_semantic_authority_row_sha256":authority_ref["row_sha256"],"member_row_sha256":member_ref["row_sha256"]})
        payload={"graph_id":old["graph_id"],"incidence_role":old["incidence_role"],"member_id":member,"coarse_family":family,"source_graph_row_id":old["source_graph_row_id"],"source_graph_row_sha256":old["source_graph_row_sha256"],"source_incidence_row_id":old["source_incidence_row_id"],"source_incidence_row_sha256":old["source_incidence_row_sha256"],"C1_incidence_row_id":old["row_id"],"C1_incidence_row_sha256":old["row_sha256"],"graph_semantic_authority_kind":authority_kind,"graph_semantic_authority_row_id":authority_ref["row_id"],"graph_semantic_authority_row_sha256":authority_ref["row_sha256"],"member_row_id":member_ref["row_id"],"member_row_sha256":member_ref["row_sha256"],"incidence_statement_ast":{**old["incidence_statement_ast"],"proved":False,"fresh_member_universe":"ROUND306C6"},"positive_graph_definition_credit":1 if semantic_ref is not None else 0,"empty_graph_disposition_credit":0 if semantic_ref is not None else 1,"physical_incidence_credit":0,"theorem_semantic_state":old["theorem_semantic_state"],"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("physical-incidence-statement",payload);incidence_writer.write(row);need(old["row_id"] not in incidence_refs,"duplicate C1 incidence row")
        incidence_refs[old["row_id"]]={"row_id":row["row_id"],"row_sha256":row["row_sha256"]};incidence_counts[family]+=1;family_incidence_ids[family].add(row["row_id"]);family_incidence_sources[family].add(old["row_sha256"])
    need(dict(incidence_counts)==EXPECTED_PHYSICAL and len(incidence_relations)==15_392,"physical relation census");need(valid_nonpositive_relations==33_344,"empty survivor relation census");need(dict(semantic_authority_counts)=={"C5_POSITIVE_GRAPH_DEFINITION":15_382,"C4_ORPHAN_TARGET_EMPTY_GRAPH_DISPOSITION":10},"incidence semantic authority census")
    meta["physical_incidence"]=incidence_writer.close();need(meta["physical_incidence"]["row_count"]==15_392,"physical rows")

    gap_writer=LedgerWriter(directory/OUTPUTS["gap"]);gap_counts=Counter();graph_definition_gaps=0;discarded_physical_gaps=0
    family_gap_ids={family:SequenceHash() for family in FAMILIES};family_gap_sources={family:SequenceHash() for family in FAMILIES}
    for old in jsonl(snapshot,"C1_GAP"):
        if old["gap_kind"]=="SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING":graph_definition_gaps+=1;continue
        incidence_ref=incidence_refs.get(old["subject_row_id"])
        if incidence_ref is None:discarded_physical_gaps+=1;continue
        member=old["member_id"];member_ref=member_refs[member];family=member_ref["family"];need(family in {"G2A","G2B"},"physical gap family")
        commitment=input_commit("semantic-gap-input.v1",{"C1_gap_row_sha256":old["row_sha256"],"C7_incidence_row_sha256":incidence_ref["row_sha256"],"member_row_sha256":member_ref["row_sha256"]})
        payload={"gap_kind":old["gap_kind"],"subject_kind":"PHYSICAL_INCIDENCE","subject_row_id":incidence_ref["row_id"],"member_id":member,"coarse_family":family,"required_closure":old["required_closure"],"C1_gap_row_id":old["row_id"],"C1_gap_row_sha256":old["row_sha256"],"blocking_credit_kinds":["normalized_support","physical_incidence","representation_cover","B1A"],"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("semantic-gap",payload);gap_writer.write(row);gap_counts[family]+=1;family_gap_ids[family].add(row["row_id"]);family_gap_sources[family].add(old["row_sha256"])
    need(graph_definition_gaps==38_608 and discarded_physical_gaps==100_032,"closed/discarded gap census")
    need(dict(gap_counts)==EXPECTED_PHYSICAL,"fresh gap census");meta["gap"]=gap_writer.close();need(meta["gap"]["row_count"]==15_392,"gap rows")

    rebind_writer=LedgerWriter(directory/OUTPUTS["component_rebind"]);rebind_counts=Counter();changed_components=0
    family_rebind_ids={family:SequenceHash() for family in FAMILIES}
    for member,member_ref in member_refs.items():
        need(member_ref["old_component"]!=member_ref["component"],"C1 component unexpectedly current");changed_components+=1;family=member_ref["family"]
        commitment=input_commit("component-rebind-input.v1",{"member_id":member,"C1_component_id":member_ref["old_component"],"C6_component_id":member_ref["component"],"C6_row_sha256":member_ref["c6_row_sha256"]})
        payload={"member_id":member,"coarse_family":family,"C1_component_id_provenance_only":member_ref["old_component"],"C1_member_row_id":member_ref["old_row_id"],"C1_member_row_sha256":member_ref["old_row_sha256"],"C6_member_component_row_id":member_ref["c6_row_id"],"C6_member_component_row_sha256":member_ref["c6_row_sha256"],"fresh_component_id":member_ref["component"],"rebind_reason":"ALL_SURVIVING_MEMBERS_REBOUND_AFTER_C5_INVALIDATION_AND_C6_FRESH_DSU","canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("component-rebind",payload);rebind_writer.write(row);rebind_counts[family]+=1;family_rebind_ids[family].add(row["row_id"])
    need(changed_components==497_772 and dict(rebind_counts)==EXPECTED_MEMBERS,"full rebind census");meta["component_rebind"]=rebind_writer.close()

    handle_writer=LedgerWriter(directory/OUTPUTS["transition_handle"]);handle_counts=Counter();seen_handles:set[str]=set();family_handle_ids={family:SequenceHash() for family in FAMILIES}
    for old in jsonl(snapshot,"C1_HANDLE"):
        member=old["member_id"];member_ref=member_refs.get(member)
        if member_ref is None:continue
        need(member not in seen_handles,"duplicate C1 handle");seen_handles.add(member);family=member_ref["family"]
        commitment=input_commit("transition-handle-input.v1",{"C1_handle_row_sha256":old["row_sha256"],"member_row_sha256":member_ref["row_sha256"],"fresh_component_id":member_ref["component"]})
        payload={"member_id":member,"coarse_family":family,"member_row_id":member_ref["row_id"],"member_row_sha256":member_ref["row_sha256"],"typed_support_ast_sha256":member_ref["ast_sha256"],"representation_set_sha256":member_ref["representation_set_sha256"],"fresh_component_id":member_ref["component"],"C1_handle_row_id":old["row_id"],"C1_handle_row_sha256":old["row_sha256"],"transition_syntax_ready":True,"transition_semantics_ready":False,"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        row=make_row("transition-ready-handle",payload);handle_writer.write(row);handle_counts[family]+=1;family_handle_ids[family].add(row["row_id"])
    need(seen_handles==set(member_refs) and dict(handle_counts)==EXPECTED_MEMBERS,"fresh handle census");meta["transition_handle"]=handle_writer.close()

    family_writer=LedgerWriter(directory/OUTPUTS["family_census"])
    for family in FAMILIES:
        source_commit=objsha({"C1_member_rows_sha256":family_member_sources[family].finish(),"C1_representation_rows_sha256":family_rep_sources[family].finish(),"C1_incidence_rows_sha256":family_incidence_sources[family].finish(),"C1_gap_rows_sha256":family_gap_sources[family].finish()})
        commitment=input_commit("family-census-input.v1",{"family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"physical_incidence_count":incidence_counts[family],"semantic_gap_count":gap_counts[family],"source_commitment_sha256":source_commit})
        payload={"coarse_family":family,"member_count":member_counts[family],"representation_count":rep_counts[family],"physical_incidence_count":incidence_counts[family],"semantic_gap_count":gap_counts[family],"component_rebind_count":rebind_counts[family],"transition_handle_count":handle_counts[family],"C5_empty_graph_side_reclassification_count":33_344 if family=="NON_GRAPH" else 0,"member_ids_sha256":family_member_ids[family].finish(),"representation_ids_sha256":family_rep_ids[family].finish(),"physical_incidence_row_ids_sha256":family_incidence_ids[family].finish(),"semantic_gap_row_ids_sha256":family_gap_ids[family].finish(),"component_rebind_row_ids_sha256":family_rebind_ids[family].finish(),"transition_handle_row_ids_sha256":family_handle_ids[family].finish(),"source_rows_commitment_sha256":source_commit,"canonical_input_commitment_sha256":commitment,"formal_credit":dict(ZERO_CREDIT)}
        family_writer.write(make_row("family-census",payload))
    meta["family_census"]=family_writer.close();need(meta["family_census"]["row_count"]==6,"family rows")

    descriptors=[]
    for role in OUTPUT_ORDER[:-1]:
        value=meta[role];descriptors.append({"role":role,"filename":OUTPUTS[role],"size":value["size"],"sha256":value["sha256"]})
    result_body={"schema":SCHEMA+".result.v1","status":"PASS_497772_FRESH_MEMBERS__545184_REPRESENTATIONS__15392_INCIDENCES__15392_OPEN_PHYSICAL_GAPS__ZERO_SUPPORT_CREDIT","producer_source":producer_commit,"source_pins":[pin.__dict__ for pin in PINS],"fresh_base":{"member_count":497_772,"root_count":334_604,"component_count":61_928,"cross_component_pair_denominator":123_410_984_634},"fresh_census":{"family_member_counts":dict(member_counts),"family_representation_counts":dict(rep_counts),"member_count":497_772,"representation_count":545_184,"physical_incidence_count":15_392,"semantic_gap_count":15_392,"component_rebind_count":497_772,"transition_handle_count":497_772,"family_census_rows":6},"C4_semantic_effect":{"orphan_target_empty_graph_disposition_count":16,"retained_distinct_side_relation_count":10,"positive_graph_definition_credit":0,"physical_incidence_credit":0},"C5_semantic_effect":{"positive_graph_definition_count":5_264,"empty_graph_disposition_count":33_344,"invalid_member_count":66_688,"empty_graph_surviving_side_reclassified_to_NON_GRAPH_count":33_344,"closed_graph_definition_gap_count":38_608},"physical_relation_semantic_authority_counts":dict(semantic_authority_counts),"C1_component_bindings_replaced_count":changed_components,"old_component_ids_are_provenance_only":True,"physical_incidence_relations_not_legacy_member_denominator":True,"legacy_115440_incidence_denominator_reused":False,"legacy_76832_side_member_denominator_reused":False,"ledger_receipts":{role:{key:item for key,item in value.items() if key not in {"size","sha256"}} for role,value in meta.items()},"output_artifacts_in_publication_order_before_result":descriptors,"formal_credit":dict(ZERO_CREDIT),"normalized_support_sealed":False,"B1A_permitted":False,"B2_permitted":False,"CM2":"NO-GO_FOR_CLAIM","seed_serialized_or_semantically_used":False}
    result={**result_body,"result_sha256":objsha(result_body)};meta["result"]=write_json(directory/OUTPUTS["result"],result)
    return {"descriptors":meta,"result_sha256":result["result_sha256"],"fresh_partition_basis":"C6_MANIFEST:"+next(pin.sha256 for pin in PINS if pin.role=="C6_MANIFEST")}

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
            return {"status":"PASS_C7_RESULT_LAST_PUBLICATION_REVERSE_REVALIDATED","artifact_count":8,"artifact_sha256":hashes}
        finally:os.close(dirfd)
    finally:os.close(parent_fd)


def production(candidate:str|None,no_write:bool,seed:int)->dict[str,Any]:
    producer_sha=source_sha();Path(FIXED_SPILL).mkdir(mode=0o700,parents=True,exist_ok=True);first=Path(tempfile.mkdtemp(prefix="seed-a.",dir=FIXED_SPILL));second=Path(tempfile.mkdtemp(prefix="seed-b.",dir=FIXED_SPILL))
    with Snapshot() as snapshot:
        try:
            a=build_candidate(snapshot,first,seed,producer_sha);build_candidate(snapshot,second,seed^0x5A5A5A5A5A5A5A5A,producer_sha);compare_dirs(first,second);snapshot.final()
            if no_write:return {"status":"PASS_C7_DUAL_SEED_BYTE_IDENTICAL_NO_WRITE","artifact_count":8,"result_sha256":a["result_sha256"],"candidate_publication_attempted":False}
            need(type(candidate)is str and candidate!="","candidate required");return publish(first,candidate)
        finally:cleanup(first);cleanup(second)


def main()->int:
    need(type(sys.flags.isolated)is int and sys.flags.isolated==1,"python -I required");need(sys.dont_write_bytecode is True,"python -B required")
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--candidate-dir");parser.add_argument("--no-write",action="store_true");parser.add_argument("--seed",type=int,default=0);args=parser.parse_args();need((args.candidate_dir is not None)!=args.no_write,"one mode");need(type(args.seed)is int and 0<=args.seed<2**63,"seed")
    print(json.dumps(production(args.candidate_dir,args.no_write,args.seed),sort_keys=True,separators=(",",":")));return 0


if __name__=="__main__":raise SystemExit(main())
