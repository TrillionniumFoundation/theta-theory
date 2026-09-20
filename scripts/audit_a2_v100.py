#!/usr/bin/env python3
"""Bind actual v100 source/input graphs, exact diagnostics and native PDFs to HEAD."""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from build_a2_v100 import PAPER, ROOT, tex_graph, text_without_comments

REVIEW_HEAD = '5485ed6d127b8443fce059db118dc215b68e283a'
REVIEWED_PAPER_HEAD = 'c49c6d0604f83badf47b32dfdf25dc043b4117ef'
REVIEW_PATH = 'reviews/a2-v99-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md'
REVIEW_BLOB = 'abd7744408a5db2e44b1a6ca46c48271a8c163eb'


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(source_only: bool) -> dict:
    head = git('rev-parse', 'HEAD')
    expected = os.environ.get('EXPECTED_HEAD', head)
    if head != expected:
        raise AssertionError(f'Checked out {head}, expected {expected}')
    subprocess.run(['git', 'merge-base', '--is-ancestor', REVIEW_HEAD, head], cwd=ROOT, check=True)
    changes = git('diff', '--name-status', REVIEW_HEAD, head).splitlines()
    if any(not line.startswith('A\t') for line in changes):
        raise AssertionError('An inherited file was modified or deleted: '+repr(changes))
    if git('rev-parse', f'{head}:{REVIEW_PATH}') != REVIEW_BLOB:
        raise AssertionError('Controlling referee report changed')
    tracked = set(git('ls-files', '-z').split('\0'))
    manifest = json.loads((ROOT/'revisions/a2-v100/SOURCE_MANIFEST.json').read_text())
    for relative, sha in manifest['new_source_sha256'].items():
        if digest(ROOT/relative) != sha:
            raise AssertionError(f'Manifest mismatch: {relative}')
    principal = PAPER/'rigidity_v100.tex'
    graph = tex_graph(principal)
    contents = '\n'.join(text_without_comments(path) for path in graph)
    labels = re.findall(r'\\label\{([^{}]+)\}', contents)
    duplicates = [key for key, count in collections.Counter(labels).items() if count > 1]
    references = set(re.findall(r'\\(?:eqref|ref|autoref)\{([^{}]+)\}', contents))
    missing = sorted(key for key in references-set(labels) if '#' not in key and '\\' not in key)
    bib = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}', contents))
    citations = set()
    for group in re.findall(r'\\cite[a-zA-Z]*(?:\[[^\]]*\])*\{([^{}]+)\}', contents):
        citations.update(k.strip() for k in group.split(','))
    if duplicates or missing or citations-bib:
        raise AssertionError({'duplicate_labels': duplicates, 'missing_labels': missing,
                              'missing_citations': sorted(citations-bib)})
    graph_record = {}
    for path, children in graph.items():
        relative = path.relative_to(ROOT).as_posix()
        if relative not in tracked:
            raise AssertionError(f'Untracked principal source: {relative}')
        if subprocess.check_output(['git', 'show', f'{head}:{relative}'], cwd=ROOT) != path.read_bytes():
            raise AssertionError(f'Working-tree source differs from HEAD: {relative}')
        graph_record[relative] = {'sha256': digest(path),
                                 'inputs': [p.relative_to(ROOT).as_posix() for p in children]}
    result = {'schema': 'a2-v100-runtime-1', 'source_head': head,
              'review_head': REVIEW_HEAD, 'reviewed_paper_head': REVIEWED_PAPER_HEAD,
              'preservation': 'addition-only relative to controlling review',
              'changed_paths': changes, 'principal_input_graph': graph_record,
              'source_only': source_only,
              'exact_record_sha256': digest(ROOT/'revisions/a2-v100/EXACT_DIAGNOSTICS.json'),
              'native_build_verified': False}
    if source_only:
        return result
    plan = json.loads((ROOT/'a2-v100-artifacts/BUILD_PLAN.json').read_text())
    if plan['source_head'] != head or plan['dry_run']:
        raise AssertionError('No actual native build plan for the checked-out head')
    actual = json.loads((ROOT/'a2-v100-artifacts/EXACT_DIAGNOSTICS.json').read_text())
    expected_record = json.loads((ROOT/'revisions/a2-v100/EXACT_DIAGNOSTICS.json').read_text())
    if actual != expected_record:
        raise AssertionError('Runtime exact diagnostics do not match committed record')
    builds = []
    for relative in plan['native_build_order']:
        tex = PAPER/relative
        pdf, log, fls = [tex.with_suffix(s) for s in ('.pdf', '.log', '.fls')]
        if not all(p.is_file() for p in (pdf, log, fls)):
            raise AssertionError(f'Missing native build output for {relative}')
        warnings = log.read_text(errors='replace')
        if re.search(r'(?:LaTeX Warning: (?:Reference|Citation).*undefined|There were undefined references|multiply defined|^! )', warnings, re.M):
            raise AssertionError(f'Unresolved native TeX diagnostic in {log}')
        observed = {}
        for line in fls.read_text(errors='replace').splitlines():
            if not line.startswith('INPUT '):
                continue
            path = Path(line[6:])
            if not path.is_absolute():
                path = PAPER/path
            path = path.resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                continue
            name = path.relative_to(ROOT).as_posix()
            role = 'tracked-source' if name in tracked else 'generated-build-input'
            if role == 'tracked-source' and path.suffix not in {'.pdf', '.aux', '.out', '.toc'}:
                original = subprocess.check_output(['git', 'show', f'{head}:{name}'], cwd=ROOT)
                if original != path.read_bytes():
                    raise AssertionError(f'Actual TeX input is not at HEAD: {name}')
            observed[name] = {'role': role, 'sha256': digest(path)}
        info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
        pages = re.search(r'^Pages:\s+(\d+)', info, re.M)
        if not pages:
            raise AssertionError(f'No page count for {pdf}')
        builds.append({'entry': relative, 'pdf_sha256': digest(pdf), 'pages': int(pages.group(1)),
                       'log_sha256': digest(log), 'fls_sha256': digest(fls),
                       'actual_repository_inputs': observed,
                       'overfull_box_count': len(re.findall(r'Overfull \\[hv]box', warnings))})
    result.update(native_build_verified=True, builds=builds,
                  pdflatex_version=subprocess.check_output(['pdflatex', '--version'], text=True).splitlines()[0])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-only', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source_only)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
