#!/usr/bin/env python3
"""Verify the publication edition against the pinned v36 native inputs.

This is a source-integrity and regression check, not a mathematical proof.
Run python v37/verify_publication.py from any working directory.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = '8f074b8027627a71a81a362b9d15f47975e1f3ae'
PINNED = {
    'verification-v35/NATIVE_BUILD_V35.json': '1e5f92cf41b563779ad702c85ee440a470a689fe',
    'verification-v36/NATIVE_BUILD_V36.json': 'f4dbd653b585f0fa446d95653b247b3bffd14268',
    'verification-v36/EXECUTION_RECORD.json': '48bd7a55894b749ed3801585ef225ec9676c79fe',
    'v35/build_native.py': '66e5fa5a5fe7ba7c551b62bc38afb4c5951823a4',
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blocks(text: str) -> Counter:
    pattern = r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}(.*?)\\end\{\1\}'
    return Counter((kind, body) for kind, body in re.findall(pattern, text, re.S))


def verify() -> dict:
    for name, expected in PINNED.items():
        require(blob((ROOT/name).read_bytes()) == expected, 'Changed baseline or builder: '+name)
    manifest = json.loads((ROOT/'verification-v35/NATIVE_BUILD_V35.json').read_text())['source_git_blob'].copy()
    delta = json.loads((ROOT/'verification-v36/NATIVE_BUILD_V36.json').read_text())['source_manifest']
    for name in delta['delete']:
        del manifest[name]
    manifest.update(delta['replace_or_add'])
    spec = importlib.util.spec_from_file_location('native', ROOT/'v35/build_native.py')
    require(spec is not None and spec.loader is not None, 'Cannot load verified native builder')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    current = native.sources(ROOT, 'main') | native.sources(ROOT, 'companions')
    require(current == set(manifest), 'Native source closure differs from v36')
    old_blocks, new_blocks = Counter(), Counter()
    changed = []
    for name in sorted(current):
        data = (ROOT/name).read_bytes()
        baseline = data
        if name == 'main.tex':
            old = b'\\date{September 8, 2026}'
            new = b'\\date{September 9, 2026}'
            require(data.count(new) == 1, 'Expected exactly one new edition date')
            baseline = data.replace(new, old)
        require(blob(baseline) == manifest[name], 'Non-editorial source change: '+name)
        if baseline != data:
            changed.append(name)
        old_blocks.update(blocks(baseline.decode()))
        new_blocks.update(blocks(data.decode()))
    require(old_blocks == new_blocks, 'A mathematical statement or proof changed')
    counts = Counter()
    for (kind, _), count in new_blocks.items():
        counts[kind] += count
    out = ROOT/'verification-v37'
    out.mkdir(exist_ok=True)
    replays = []
    previous = json.loads((ROOT/'verification-v36/EXECUTION_RECORD.json').read_text())['executed_programs']
    for record in previous:
        name = record['program']
        code = (ROOT/name).read_bytes()
        require(blob(code) == record['program_git_blob'], 'Changed diagnostic: '+name)
        outputs = []
        for optimized in (False, True):
            command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/name)]
            proc = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=90)
            require(proc.returncode == 0, 'Diagnostic failed: '+name+'; '+proc.stderr.decode(errors='replace'))
            require(sha256(proc.stdout) == record['output_sha256'], 'Regression output changed: '+name)
            dest = record['output_file'].replace('.json', '.optimized.json') if optimized else record['output_file']
            (out/dest).write_bytes(proc.stdout)
            outputs.append(proc.stdout)
        require(outputs[0] == outputs[1], 'Ordinary and optimized executions disagree: '+name)
        replays.append({'program': name, 'program_git_blob': blob(code),
            'output_sha256': sha256(outputs[0]), 'ordinary_returncode': 0,
            'optimized_returncode': 0, 'ordinary_optimized_byte_identical': True,
            'matches_v36_record': True})
    return {
        'status': 'PASS', 'baseline_commit': BASE_COMMIT,
        'baseline_identity': 'Pinned content-addressed v35/v36 manifests',
        'active_tex_inputs': len(current), 'byte_identical_inputs': len(current)-len(changed),
        'metadata_only_changes': changed,
        'all_mathematical_blocks_verbatim': True,
        'preserved_blocks_by_type': dict(sorted(counts.items())),
        'preserved_statement_blocks': sum(v for k,v in counts.items() if k != 'proof'),
        'preserved_proof_blocks': counts['proof'], 'executed_programs': replays,
        'formal_proof_assistant': False, 'global_controller_optimization': False,
        'scope': 'Source preservation and finite diagnostic replay; no inference of mathematical priority or journal acceptance',
    }


if __name__ == '__main__':
    try:
        result = verify()
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, indent=2, sort_keys=True))
