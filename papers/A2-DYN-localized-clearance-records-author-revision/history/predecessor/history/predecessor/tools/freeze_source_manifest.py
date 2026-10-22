#!/usr/bin/env python3
"""Freeze the explicit mathematical build inputs; execution evidence is separate."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    target = args.output or root/'SOURCE_MANIFEST.json'
    if target.exists():
        raise RuntimeError('Refusing to overwrite an existing frozen source manifest')
    spec = importlib.util.spec_from_file_location('source_check', root/'tools/check_source_preservation.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    closure = module.tex_closure(root)
    paths = sorted({p for pattern in ('*.tex', 'core/*.tex', 'tools/*.py', 'ci/*.yml')
                    for p in root.glob(pattern)} | {root/'requirements.txt', root/'build.sh'},
                   key=lambda p: p.relative_to(root).as_posix())
    rows=[]
    for path in paths:
        item=module.identity(path)
        item['path']=path.relative_to(root).as_posix()
        rows.append(item)
    payload = {'schema':'a2-dyn-frozen-mathematical-source-v1',
               'scope':'Native mathematical and execution source; separately anchored history, audits and evidence are excluded',
               'complete_author_parent':'6cdd9ae88cd358d524ecb89092361ac1522ba351',
               'files':rows,
               'active_core_files':closure['active_core_files'],
               'reachable_tex_files':closure['reachable_tex_files'],
               'active_core_start':closure['active_core_start'],
               'active_core_end':closure['active_core_end']}
    target.write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':'frozen','source_files':len(rows),
                      'core_files':len(closure['active_core_files']),
                      'reachable_tex_files':len(closure['reachable_tex_files']),
                      'manifest_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
if __name__=='__main__':
    main()
