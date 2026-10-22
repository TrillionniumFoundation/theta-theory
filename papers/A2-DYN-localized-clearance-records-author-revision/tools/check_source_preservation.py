#!/usr/bin/env python3
"""Check exact predecessor, untouched inherited proofs and complete native closure.

This is an identity check, not a certificate of a continuous mathematical proof.
Every check raises explicitly and remains active in optimized Python.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = '03d651b8709d28d90aa435fc12d608ad9c945e23'
BASE_ROOT_TREE = 'd65973a6db0eb2c477359d10b43194cc5f99fa2f'
BASE_ARTICLE_TREE = '3010c90e2363dfe1808101a3e992eb02643c28f1'
ANCHOR_SHA256 = 'ca3d5e4d2204230a21e3e3e6ed8439d5b79484a38a98ff3ab8456db03394ae6c'
ARCHIVE = 'history/predecessor'
spec = importlib.util.spec_from_file_location('immutable_roof_variation_verifier', ROOT/ARCHIVE/'tools/check_source_preservation.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
VerificationError = legacy.VerificationError
require = legacy.require
identity = legacy.identity
checked_path = legacy.checked_path
git_tree = legacy.git_tree
tex_closure = legacy.tex_closure
strip_comments = legacy.strip_comments

def same(actual, expected, name):
    for key in ('bytes','sha256','git_blob','mode'):
        require(actual[key] == expected[key], f'{key} mismatch: {name}')

def check_manifest(root, closure, required):
    path = root/'SOURCE_MANIFEST.json'
    if not path.exists():
        require(not required, 'Current mathematical source has not been frozen')
        return {'status':'not_frozen'}
    manifest = json.loads(path.read_text())
    require(manifest['schema']=='a2-dyn-frozen-mathematical-source-v1', 'Wrong source-manifest schema')
    require(manifest['complete_author_parent']==BASE_COMMIT, 'Wrong manifest parent')
    paths = {p.relative_to(root).as_posix() for pattern in ('*.tex','core/*.tex','tools/*.py','ci/*.yml') for p in root.glob(pattern)} | {'requirements.txt','build.sh'}
    rows = manifest['files']
    require(len(rows)==len({r['path'] for r in rows}) and {r['path'] for r in rows}==paths, 'Frozen mathematical/build input set changed')
    for row in rows:same(identity(checked_path(root,row['path'])),row,row['path'])
    for key in ('active_core_files','reachable_tex_files','active_core_start','active_core_end'):
        require(manifest[key]==closure[key], 'Frozen native closure changed: '+key)
    return {'status':'passed','files':len(rows),'bytes':sum(r['bytes'] for r in rows),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def verify(root: Path, manifest_required=True):
    root=Path(root).resolve()
    anchor_path=checked_path(root,'CURRENT_SOURCE_ANCHOR.json')
    require(identity(anchor_path)['sha256']==ANCHOR_SHA256,'Immutable predecessor anchor changed')
    anchor=json.loads(anchor_path.read_text())
    require((anchor['source_commit'],anchor['source_root_tree'],anchor['source_article_tree'],anchor['archive_root'])==(BASE_COMMIT,BASE_ROOT_TREE,BASE_ARTICLE_TREE,ARCHIVE),'Wrong complete predecessor identity')
    rows=anchor['files']
    require(len(rows)==anchor['file_count']==5938,'Incomplete predecessor file map')
    require(sum(r['bytes'] for r in rows)==anchor['bytes']==688244624,'Predecessor byte count changed')
    require(git_tree(rows)==BASE_ARTICLE_TREE,'Predecessor paths/modes/blobs do not reconstruct its actual tree')
    expected={r['path'] for r in rows}
    actual={p.relative_to(root).as_posix() for p in (root/ARCHIVE).rglob('*') if p.is_file() or p.is_symlink()}
    require(len(expected)==len(rows) and actual==expected,'Predecessor archive path set changed')
    for row in rows:
        require(row['path']==ARCHIVE+'/'+row['original_path'],'Relocated predecessor file')
        same(identity(checked_path(root,row['path'])),row,row['path'])
    inherited={r['original_path'] for r in rows if r['original_path'] in {'model.tex','inputs.tex'} or re.fullmatch(r'core/\d+_[^/]+\.tex',r['original_path'])}
    require(inherited==set(anchor['inherited_active_paths']) and len(inherited)==69,'Inherited active proof/model set changed')
    lookup={r['original_path']:r for r in rows}
    for name in sorted(inherited):same(identity(checked_path(root,name)),lookup[name],name)
    predecessor=legacy.verify(root/ARCHIVE,True)
    closure=tex_closure(root)
    require(closure['active_core_start']==260 and closure['active_core_end']==332,'Incomplete current native260--332 chain')
    manifest=check_manifest(root,closure,manifest_required)
    return {'status':'passed','scope':'Exact source identities and native closure; not a mathematical or expert certificate',
            'source_commit':BASE_COMMIT,'source_root_tree':BASE_ROOT_TREE,'source_article_tree':BASE_ARTICLE_TREE,
            'original_files_preserved':len(rows),'original_bytes_preserved':anchor['bytes'],
            'immutable_active_proof_and_model_files':len(inherited),'current_source_anchor_sha256':ANCHOR_SHA256,
            'predecessor_verification':predecessor,'tex_closure':closure,'source_manifest':manifest}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--allow-unfrozen',action='store_true')
    args=parser.parse_args()
    try:result=verify(args.root,not args.allow_unfrozen)
    except (VerificationError,OSError,ValueError,KeyError,TypeError) as exc:
        result={'status':'failed','scope':'Source identity and closure only','error':str(exc)}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    print(data,end='')
    return 0 if result['status']=='passed' else 1

if __name__=='__main__':raise SystemExit(main())
