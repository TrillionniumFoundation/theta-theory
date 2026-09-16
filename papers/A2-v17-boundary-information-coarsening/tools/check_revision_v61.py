#!/usr/bin/env python3
"""Check source preservation for the v61 exposition; not a mathematical proof."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from source_provenance import blob_id, graph, require

P = Path(__file__).resolve().parents[1]
BASE = '1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5'
PREFIX = 'papers/A2-v17-boundary-information-coarsening'
OLD = 'journal/00_principal_introduction_v56.tex'
NEW = 'journal/00_principal_introduction_v61.tex'
ALLOWED = {'main.tex', 'rigidity.tex', 'README.md'}


def git(*args: str) -> bytes:
    cp = subprocess.run(['git', *args], cwd=P, capture_output=True)
    require(cp.returncode == 0, cp.stderr.decode(errors='replace'))
    return cp.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-manifest', type=Path)
    args = parser.parse_args()
    if args.baseline_manifest:
        manifest = json.loads(args.baseline_manifest.read_text())
        require(manifest['source_commit'] == BASE, 'Wrong frozen baseline')
        baseline = {n: x['git_blob'] for n, x in manifest['files'].items()}
    else:
        baseline = {}
        for row in git('ls-tree', '-r', '-z', BASE + ':' + PREFIX).split(b'\0'):
            if row:
                meta, name = row.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                require(kind == 'blob', 'Unexpected baseline object')
                baseline[name.decode()] = oid
    changed = []
    for name, oid in baseline.items():
        path = P / name
        require(path.is_file() and not path.is_symlink(), 'Lost source: ' + name)
        if blob_id(path.read_bytes()) != oid:
            require(name in ALLOWED, 'Changed historical proof source: ' + name)
            changed.append(name)
    for name in ('main.tex', 'rigidity.tex'):
        data = (P / 'history/v60-review-baseline' / name).read_bytes()
        require(blob_id(data) == baseline[name], 'Wrong entry archive: ' + name)
    old, new = (P / OLD).read_text(), (P / NEW).read_text()
    require(blob_id((P / OLD).read_bytes()) == baseline[OLD], 'Old introduction changed')
    pattern = r'\\begin\{(theorem|lemma|proposition|corollary|proof|equation|align)\}.*?\\end\{\1\}'
    blocks = [m.group(0) for m in re.finditer(pattern, old, re.S)]
    require(all(block in new for block in blocks), 'Lost mathematical environment')
    statement = r'\\begin\{(?:theorem|lemma|proposition|corollary|proof)\}'
    require(len(re.findall(statement, old)) == len(re.findall(statement, new)), 'New statement/proof environment')
    current = {stem: graph(P, stem + '.tex') for stem in ('main', 'rigidity', 'two_collision')}
    with tempfile.TemporaryDirectory() as directory:
        q = Path(directory)
        for name in baseline:
            if name.endswith('.tex'):
                target = q / name
                target.parent.mkdir(parents=True, exist_ok=True)
                origin = P / ('history/v60-review-baseline/' + name if name in ('main.tex', 'rigidity.tex') else name)
                target.write_bytes(origin.read_bytes())
        previous = {stem: graph(q, stem + '.tex') for stem in current}
    for stem in current:
        wanted = (previous[stem] - {OLD}) | ({NEW} if OLD in previous[stem] else set())
        require(current[stem] == wanted, 'Unintended active-source change: ' + stem)
    print(json.dumps({'baseline': BASE, 'inherited_files': len(baseline),
        'unchanged_inherited_files': len(baseline) - len(changed),
        'changed_inherited_paths': sorted(changed),
        'preserved_intro_mathematical_environments': len(blocks),
        'active_files_per_entry': {k: len(v) for k, v in current.items()},
        'active_union': len(set().union(*current.values())),
        'new_theorems': 0, 'proof_certification': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
