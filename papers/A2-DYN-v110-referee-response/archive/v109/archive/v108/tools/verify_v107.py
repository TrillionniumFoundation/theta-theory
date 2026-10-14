#!/usr/bin/env python3
"""Exact-SHA and inherited-source verification for the active v107 packet."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
from check_v107 import require, checks

PAPER = Path(__file__).resolve().parents[1]
BASE_COMMIT = 'd1aa59cefb5d1158a05f556ab9c7c38398f2e4fd'
BASE_PATH = 'papers/A2-DYN-v106-referee-response'
BASE_TREE = '6acebbc6669612b32171bb9f50b5bbbd7b77459f'
ACTIVE = 'papers/A2-DYN-v107-referee-response'
REVIEW = 'reviews/a2-dyn-v104-positive-interval-external-top4-review-2026-10-14/REFEREE_REPORT.md'
REVIEW_BLOB = 'a22f11ea053a7e22dbfcf2cd98b0489d6ef4bfc1'
REPLACED = {'main.tex', 'build.sh', 'README.md', 'SOURCE_MANIFEST.json',
            'PUBLICATION_STATUS.json', 'RESPONSE_TO_REFEREE.md', 'PROOF_LEDGER.md'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=PAPER, text=True).strip()


def entries(tree):
    raw = subprocess.check_output(['git', 'ls-tree', '-rz', '--full-tree', tree], cwd=PAPER)
    result = {}
    for item in raw.split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            require(kind == 'blob', 'unexpected non-blob entry')
            result[name.decode()] = (mode, sha)
    require(bool(result), 'empty tree cannot certify preservation')
    return result


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def verify():
    require(not sys.argv[1:], 'no preview or bypass mode')
    head = git('rev-parse', 'HEAD')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'), 'wrong exact checkout')
    require(git('rev-parse', 'HEAD:'+BASE_PATH) == BASE_TREE, 'changed baseline directory')
    require(git('rev-parse', 'HEAD:'+REVIEW) == REVIEW_BLOB, 'changed substantive report')
    for version in (104, 105, 106):
        path = 'papers/A2-DYN-v%d-referee-response' % version
        require(git('rev-parse', 'HEAD:'+path) == git('rev-parse', BASE_COMMIT+':'+path),
                'historical author directory changed')
    root = git('rev-parse', '--show-toplevel')
    changed = subprocess.check_output(['git', 'diff', '--name-only', BASE_COMMIT, head],
                                      cwd=root, text=True).splitlines()
    allowed = {'A2_DYN_V107_REVISION_INDEX.md',
               '.github/workflows/a2-dyn-v107-positive-source-qualification.yml'}
    require(all(p.startswith(ACTIVE+'/') or p in allowed for p in changed), 'unrelated repository changes')
    old, new = entries(BASE_TREE), entries('HEAD:'+ACTIVE)
    for name, record in old.items():
        if name not in REPLACED:
            require(new.get(name) == record, 'inherited source changed: '+name)
    require(new['provenance/v106-main.tex'][1] == old['main.tex'][1], 'wrong main snapshot')
    old_core = {n: v for n, v in old.items() if n.startswith('core/') and n.endswith('.tex')}
    new_core = {n: v for n, v in new.items() if n.startswith('core/') and n.endswith('.tex')}
    require(len(old_core) == 255 and len(new_core) == 257, 'inherited/active core count')
    require(all(new_core.get(n) == v for n, v in old_core.items()), 'an inherited core was modified')
    for name, (mode, sha) in new.items():
        require(blob(PAPER/name) == sha, 'working bytes differ from HEAD: '+name)
        require(bool((PAPER/name).stat().st_mode & 0o111) == (mode == '100755'), 'file mode: '+name)
    manifest = json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 107 and manifest['active_core_count'] == 257, 'active manifest')
    require(manifest['baseline_paper_tree'] == BASE_TREE, 'manifest baseline pin')
    require(set(manifest['replaced_root_files']) == REPLACED, 'unexpected source replacement list')
    for flag in ('full_raw_return_LLT_proved', 'primary_referee_request_closed',
                 'full_comparison_deficit_height_decay_proved',
                 'complete_lorentz_comparison_interval_coverage_proved',
                 'independent_human_review', 'formal_proof_certificate'):
        require(manifest['claims'][flag] is False, 'unsupported completion claim: '+flag)
    status = json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())
    require(status == {k: manifest[k] for k in ('inherited_packet','claims','superseded_claims')},
            'publication status does not match manifest')
    tex = (PAPER/'main.tex').read_text()
    for module in manifest['new_core_modules']:
        require('\\input{'+module[:-4]+'}' in tex, 'new proof not included in main')
    require('ef{thm:v104-paid-arms}' not in tex.replace('\\ref{thm:v104-paid-arms}', ''),
            'malformed paid-arm reference')
    from assemble_v105 import assemble
    assemble()
    return {'revision': 107, 'checkout_sha': head, 'baseline_tree': BASE_TREE,
            'paper_tree': git('rev-parse', 'HEAD:'+ACTIVE),
            'inherited_core_count': len(old_core), 'active_core_count': len(new_core),
            'preserved_inherited_files': len(old)-len(REPLACED),
            'source_scope_verified': True, 'finite_checks': checks(),
            'formal_proof_certificate': False, 'independent_human_review': False}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
