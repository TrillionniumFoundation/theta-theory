#!/usr/bin/env python3
"""Independent terminal replay of the scoped G2A zero-credit seal."""
from __future__ import annotations
import argparse,hashlib,json,os,stat
from pathlib import Path

WORK=Path(__file__).resolve().parent.parent
class Failure(RuntimeError):pass
def need(v,label):
 if type(v)is not bool or not v:raise Failure(label)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("ascii")
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def fp(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_uid,s.st_gid)
def stable(path,expected=None):
 p=Path(path).resolve();fd=os.open(p,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0))
 try:
  s=os.fstat(fd);need(stat.S_ISREG(s.st_mode),"regular:"+str(p));h=hashlib.sha256();chunks=[]
  while b:=os.read(fd,4<<20):h.update(b);chunks.append(b)
  got=h.hexdigest();need(expected is None or got==expected,"sha256:"+str(p));need(fp(os.fstat(fd))==fp(s),"stable-stat:"+str(p));return b"".join(chunks),got
 finally:os.close(fd)
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--seal-dir",required=True);p.add_argument("--expected-receipt-sha256",required=True);p.add_argument("--expected-payload-manifest-sha256",required=True);p.add_argument("--out-dir",required=True);a=p.parse_args();seal=Path(a.seal_dir).resolve();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=False)
 root_wire,root_sha=stable(seal/"root_manifest.sha256");lines=root_wire.decode("ascii").splitlines();need(len(lines)==2 and lines==sorted(lines,key=lambda x:x.split("  ",1)[1]),"root manifest order")
 root={path:sha for sha,path in(line.split("  ",1)for line in lines)};need(set(root)=={"payload_manifest.sha256","receipt.json"}and root["payload_manifest.sha256"]==a.expected_payload_manifest_sha256 and root["receipt.json"]==a.expected_receipt_sha256,"root manifest pins")
 payload_wire,payload_sha=stable(seal/"payload_manifest.sha256",a.expected_payload_manifest_sha256);receipt_wire,receipt_sha=stable(seal/"receipt.json",a.expected_receipt_sha256);receipt=json.loads(receipt_wire);need(canonical(receipt)+b"\n"==receipt_wire,"receipt canonical");body=dict(receipt);claimed=body.pop("result_sha256",None);need(claimed==digest(body),"receipt closure")
 entries=payload_wire.decode("ascii").splitlines();need(entries==sorted(entries,key=lambda x:x.split("  ",1)[1])and len(entries)==len(set(entries))==receipt["payload_manifest"]["entry_count"],"payload manifest order/count")
 for line in entries:
  sha,rel=line.split("  ",1);path=Path(rel);need(not path.is_absolute()and".."not in path.parts,"safe relative payload path");stable(WORK/path,sha)
 need(receipt["status"]=="PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__SCOPED_G2A_5264_CLOSED__POSITIVE_C19_AND_GLOBAL_THREE_TERMINAL_OPEN__ZERO_CREDIT"and receipt["formal_credit"]==0 and receipt["manifest_authorized"]is False,"zero-credit receipt status")
 need(receipt["headline"]=={"G2A_graphs":5264,"scoped_unique_routes":5264,"contact_aliases":9408,"positive_sides":9408,"reverse_empty":9392,"single_side_no_reverse":16,"complement":552,"C23_candidates":0,"same_C15":8812,"cross_C15":596,"unique_cross_C15_component_edges":144,"raw_SIGNED_COMPLETE_intersections":0},"headline")
 need(receipt["double_seed"]["all_materialized_ledgers_byte_identical"]is True and receipt["coherent_attacks"]=={"control_pass":True,"accepted":0,"rejected":15,"receipt_file_sha256":receipt["coherent_attacks"]["receipt_file_sha256"]},"double seed/attacks")
 need(receipt["authority_scope"]["scoped_G2A_route_assignment"]is True and receipt["authority_scope"]["POSITIVE_C19_91672"].startswith("OPEN")and receipt["authority_scope"]["global_three_terminal_unique_assignment"]is False and receipt["strict_nonpromotion"]=={"C27_transition_totality":0,"C28_pair_routing":0,"C29_physical_maximality":0,"CM2":"NO-GO_FOR_CLAIM"},"scoped authority")
 result={"schema":"cm2.c27-independent.g2a-relative2d-primitive-totality-terminal-replay.v2","status":"PASS_INDEPENDENT_ROOT_PAYLOAD_AND_SCOPED_RECEIPT_REPLAY__ZERO_CREDIT","root_manifest_file_sha256":root_sha,"payload_manifest_file_sha256":payload_sha,"payload_entry_count":len(entries),"receipt_file_sha256":receipt_sha,"receipt_result_sha256":claimed,"global_three_terminal_unique_assignment":False,"positive_C19_91672_gate":"OPEN","formal_credit":0,"manifest_authorized":False,"CM2":"NO-GO_FOR_CLAIM"};result["result_sha256"]=digest(result);(out/"terminal_replay.json").write_bytes(canonical(result)+b"\n");print(canonical({"status":result["status"],"result_sha256":result["result_sha256"]}).decode());return 0
if __name__=="__main__":
 try:raise SystemExit(main())
 except(Failure,KeyError,TypeError,ValueError,OSError)as e:print("FAIL:"+str(e));raise SystemExit(2)
