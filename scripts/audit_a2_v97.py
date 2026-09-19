#!/usr/bin/env python3
"""Audit A2 v97 source identity and actual build inputs; not a proof verifier."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'revisions/a2-v97'
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
BASE = 'b4ab165062f3625e06717002fb419bd44ab8e7f7'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def actual_inputs(stem: str) -> list[str]:
    found = set()
    for line in (PAPER / f'{stem}.fls').read_text().splitlines():
        if not line.startswith('INPUT '):
            continue
        p = Path(line[6:])
        if not p.is_absolute():
            p = PAPER / p
        p = p.resolve()
        try:
            relative = p.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if p.suffix == '.tex':
            found.add(relative)
    return sorted(found)


def build_record(stem: str, strict: bool) -> dict:
    pdf, log, fls = (PAPER / f'{stem}.{suffix}' for suffix in ['pdf', 'log', 'fls'])
    for p in [pdf, log, fls]:
        if not p.is_file():
            raise RuntimeError(f'missing build artifact: {p}')
    text = log.read_text(errors='replace')
    if re.search(r'^!|Undefined control sequence|Fatal error', text, re.M):
        raise RuntimeError(f'fatal TeX diagnostic in {log}')
    warnings = re.findall(r'^.*(?:Warning|Overfull|Underfull).*$' , text, re.M)
    if strict and warnings:
        raise RuntimeError(f'principal manuscript has TeX warnings: {warnings}')
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    match = re.search(r'^Pages:\s+(\d+)', info, re.M)
    if not match:
        raise RuntimeError(f'cannot determine page count: {pdf}')
    return {'pages': int(match.group(1)), 'pdf_sha256': digest(pdf),
            'log_sha256': digest(log), 'fls_sha256': digest(fls),
            'warnings': warnings, 'tex_inputs': actual_inputs(stem)}


def main(repo: bool, build: bool, output: str | None) -> None:
    manifest = json.loads((PACKET / 'SOURCE_MANIFEST.json').read_text())
    if manifest['base_commit'] != BASE:
        raise RuntimeError('unexpected controlling-review base')
    for name, expected in manifest['sha256'].items():
        p = ROOT / name
        if not p.is_file() or digest(p) != expected:
            raise RuntimeError(f'source hash mismatch: {name}')
    receipt = {'role': 'source/build audit, not mathematical proof verification',
               'base_commit': BASE, 'source_files_verified': len(manifest['sha256']),
               'staging_hash_audit': 'passed', 'repository_audit': 'not executed',
               'build_audit': 'not executed'}
    if repo:
        head = git('rev-parse', 'HEAD')
        expected_head = os.environ.get('EXPECTED_HEAD')
        if expected_head and head != expected_head:
            raise RuntimeError(f'checkout {head} differs from requested head {expected_head}')
        subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', BASE, head], check=True)
        rows = git('diff', '--name-status', BASE, head).splitlines()
        actual = set()
        for row in rows:
            kind, name = row.split('\t', 1)
            if kind != 'A':
                raise RuntimeError(f'inherited file changed: {row}')
            actual.add(name)
        if actual != set(manifest['added_paths']):
            raise RuntimeError(f'addition manifest mismatch: {actual ^ set(manifest["added_paths"])}')
        subprocess.run(['git', '-C', str(ROOT), 'diff', '--exit-code'], check=True)
        receipt.update(head=head, repository_audit='passed: addition-only; inherited tree unchanged')
    if build:
        if not repo:
            raise RuntimeError('--build requires --repo for inherited-source checks')
        records = {stem: build_record(stem, stem == 'rigidity_v97') for stem in
                   ['rigidity_v97', 'rigidity_v97_archive', 'rigidity_v97_complete']}
        core = set(records['rigidity_v97']['tex_inputs'])
        if core != set(manifest['principal_tex_inputs']):
            raise RuntimeError(f'principal input graph mismatch: {core ^ set(manifest["principal_tex_inputs"])}')
        archive = records['rigidity_v97_archive']['tex_inputs']
        historical = [p for p in archive if not p.endswith('/rigidity_v97_archive.tex')]
        if len(historical) < 30 or not any(p.endswith('/rigidity_v96.tex') for p in historical):
            raise RuntimeError('archive did not compile the complete historical entrypoint')
        for name in historical:
            before = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{name}'])
            if before != (ROOT / name).read_bytes():
                raise RuntimeError(f'archival input differs from controlling base: {name}')
        if records['rigidity_v97_complete']['pages'] != (
                records['rigidity_v97']['pages'] + records['rigidity_v97_archive']['pages']):
            raise RuntimeError('assembled page count does not equal principal plus archive')
        receipt.update(build_audit='passed', builds=records,
                       inherited_active_tex_files_verified=len(historical))
    data = json.dumps(receipt, indent=2) + '\n'
    if output:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(data)
    print(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', action='store_true')
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--output')
    options = parser.parse_args()
    main(options.repo, options.build, options.output)
