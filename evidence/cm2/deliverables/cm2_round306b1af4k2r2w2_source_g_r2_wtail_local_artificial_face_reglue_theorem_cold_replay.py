#!/usr/bin/env python3
"""Manifest-first cold replay for the sealed K2R2W2 local theorem package."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Final


class FailClosed(RuntimeError): pass


def need(ok: bool, label: str) -> None:
    if not ok: raise FailClosed(label)


HERE: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306b1af4k2r2w2_source_g_r2_wtail_local_artificial_face_reglue_theorem_"
MANIFEST: Final = PREFIX + "manifest.sha256"
NAMES: Final = (
    PREFIX + "producer.py",
    PREFIX + "theorem_ledger.json",
    PREFIX + "result.json",
    PREFIX + "independent_verifier.py",
    PREFIX + "attack_suite.json",
    PREFIX + "verification.json",
    PREFIX + "report.md",
    PREFIX + "cold_replay.py",
)


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev,info.st_ino,info.st_mode,info.st_nlink,info.st_size,info.st_mtime_ns,info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd,0,os.SEEK_SET); state=hashlib.sha256()
    while True:
        block=os.read(fd,1<<20)
        if not block:
            os.lseek(fd,0,os.SEEK_SET); return state.hexdigest()
        state.update(block)


def main() -> int:
    need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.no_site==1 and sys.dont_write_bytecode is True,"cold replay requires python3 -I -B -S")
    before_dir=os.stat(HERE,follow_symlinks=False)
    need(stat.S_ISDIR(before_dir.st_mode) and not HERE.is_symlink(),"deliverables directory")
    dirfd=os.open(HERE,os.O_RDONLY|getattr(os,"O_DIRECTORY",0)|getattr(os,"O_NOFOLLOW",0))
    held: list[tuple[str,int,os.stat_result,str]]=[]; manifest_fd=-1
    try:
        opened_dir=os.fstat(dirfd)
        need((before_dir.st_dev,before_dir.st_ino,before_dir.st_mode)==(opened_dir.st_dev,opened_dir.st_ino,opened_dir.st_mode),"directory race")
        manifest_named=os.stat(MANIFEST,dir_fd=dirfd,follow_symlinks=False)
        need(stat.S_ISREG(manifest_named.st_mode) and manifest_named.st_nlink==1 and manifest_named.st_size<=4096,"manifest identity")
        manifest_fd=os.open(MANIFEST,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_CLOEXEC",0),dir_fd=dirfd)
        manifest_opened=os.fstat(manifest_fd); need(identity(manifest_named)==identity(manifest_opened),"manifest open race")
        manifest_sha_a=hash_fd(manifest_fd); manifest_sha_b=hash_fd(manifest_fd); need(manifest_sha_a==manifest_sha_b,"manifest two-pass")
        raw=os.read(manifest_fd,manifest_opened.st_size); os.lseek(manifest_fd,0,os.SEEK_SET)
        need(len(raw)==manifest_opened.st_size and raw.endswith(b"\n") and b"\x00" not in raw,"manifest bytes")
        try: text=raw.decode("ascii")
        except UnicodeDecodeError as exc: raise FailClosed("manifest ASCII") from exc
        lines=text.splitlines(); need(len(lines)==len(NAMES),"manifest exact row count")
        rows: list[tuple[str,str]]=[]
        for line,expected_name in zip(lines,NAMES,strict=True):
            match=re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)",line)
            need(match is not None and match.group(2)==expected_name,"manifest ordered membership")
            rows.append((match.group(1),match.group(2)))
        namespace={path.name for path in HERE.iterdir() if path.is_file() and path.name.startswith(PREFIX)}
        need(namespace==set(NAMES)|{MANIFEST},"exact R2W2 namespace membership")
        for expected_sha,name in rows:
            named=os.stat(name,dir_fd=dirfd,follow_symlinks=False)
            need(stat.S_ISREG(named.st_mode) and named.st_nlink==1,"member identity:"+name)
            fd=os.open(name,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_CLOEXEC",0),dir_fd=dirfd)
            opened=os.fstat(fd); need(identity(named)==identity(opened),"member open race:"+name)
            need(hash_fd(fd)==expected_sha and hash_fd(fd)==expected_sha,"member two-pass:"+name)
            need(identity(opened)==identity(os.stat(name,dir_fd=dirfd,follow_symlinks=False)),"member rebound:"+name)
            held.append((name,fd,opened,expected_sha))
        verification_bytes=next(os.pread(fd,info.st_size,0) for name,fd,info,_sha in held if name==PREFIX+"verification.json")
        verification=json.loads(verification_bytes.decode("utf-8"),parse_float=lambda token:(_ for _ in ()).throw(FailClosed("float:"+token)),parse_constant=lambda token:(_ for _ in ()).throw(FailClosed("constant:"+token)))
        need(verification["status"]=="PASS_INDEPENDENT_REPLAY__4_LOCAL_REGLUES__4_COMPLETE_FACES__8_INWARD_CORRIDORS__ZERO_NORMALIZED_OR_GLOBAL_CREDIT","verification status")
        need(verification["credit"]=={"B1A":0,"B2":0,"CM2":"NO-GO_FOR_CLAIM","normalized_support":0,"r2_artificial_face_reglue":4,"representation_cover":0},"verification exact credit")
        need(verification["verifier_runtime"]=={"launcher_flags":["-I","-B","-S"],"sys_flags_isolated":1,"sys_flags_dont_write_bytecode":1,"sys_flags_no_site":1,"sys_dont_write_bytecode":True},"verification isolated runtime")
        need(verification["replay"]["producer_runtime"]=={"launcher_flags":["-I","-B","-S"],"isolated":True,"dont_write_bytecode":True,"no_site":True,"python_environment_neutralized":True},"producer isolated runtime")
        need(verification["replay"]["nondeterministic_timing_excluded_from_sealed_receipt"] is True,"deterministic receipt")
        before={(path.name,path.stat().st_size,path.stat().st_mtime_ns) for path in HERE.iterdir() if path.is_file() and path.name.startswith(PREFIX)}
        env={"PATH":"/usr/bin:/bin","LANG":"C","LC_ALL":"C","TZ":"UTC","TMPDIR":str(HERE)}
        verifier=HERE/(PREFIX+"independent_verifier.py")
        run=subprocess.run([sys.executable,"-I","-B","-S",str(verifier),"--verify","--input-dir",str(HERE)],cwd="/tmp",env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1200,check=False)
        need(run.returncode==0 and run.stderr==b"" and run.stdout==verification_bytes,"isolated deterministic verifier replay")
        after={(path.name,path.stat().st_size,path.stat().st_mtime_ns) for path in HERE.iterdir() if path.is_file() and path.name.startswith(PREFIX)}
        need(before==after,"R2W2 namespace changed")
        current_dir=os.stat(HERE,follow_symlinks=False)
        need((current_dir.st_dev,current_dir.st_ino,current_dir.st_mode)==(opened_dir.st_dev,opened_dir.st_ino,opened_dir.st_mode),"final directory")
        need(identity(os.fstat(manifest_fd))==identity(os.stat(MANIFEST,dir_fd=dirfd,follow_symlinks=False))==identity(manifest_opened) and hash_fd(manifest_fd)==manifest_sha_a,"final manifest")
        for name,fd,opened,expected_sha in held:
            named=os.stat(name,dir_fd=dirfd,follow_symlinks=False)
            need(identity(os.fstat(fd))==identity(named)==identity(opened) and named.st_nlink==1 and hash_fd(fd)==expected_sha,"final member:"+name)
        output={"schema":"cm2.round306b1af4k2r2w2.manifest-first-cold-replay.v1","status":"PASS_MANIFEST_FIRST_EXACT_8_MEMBER_SEAL_AND_FULL_ISOLATED_DETERMINISTIC_INDEPENDENT_COLD_REPLAY","runtime":{"launcher_flags":["-I","-B","-S"],"isolated":True,"dont_write_bytecode":True,"no_site":True,"python_environment_neutralized":True},"manifest_sha256":manifest_sha_a,"manifest_exact_ordered_members":8,"verifier_self_hash_pinned":True,"verification_stdout_byte_identical":True,"R2W2_namespace_unchanged":True,"entire_deliverables_unchanged_claimed":False,"credit":{"r2_artificial_face_reglue":4,"normalized_support":0,"B1A":0,"B2":0,"CM2":"NO-GO_FOR_CLAIM"}}
        sys.stdout.write(json.dumps(output,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\n"); return 0
    finally:
        for _name,fd,_info,_sha in held:
            try: os.close(fd)
            except OSError: pass
        if manifest_fd>=0: os.close(manifest_fd)
        os.close(dirfd)


if __name__=="__main__": raise SystemExit(main())
