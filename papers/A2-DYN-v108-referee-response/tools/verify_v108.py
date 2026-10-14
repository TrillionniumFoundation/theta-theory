#!/usr/bin/env python3
"""Verify the exact v108 checkout and every inherited blob and mode."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
from check_v108 import require, checks

P = Path(__file__).resolve().parents[1]
BASE = '6811140ec51276247d75057980692d4a4d5e77b6'
BASE_PATH = 'papers/A2-DYN-v107-referee-response'
BASE_TREE = '7f6fcd70afa7a54f6891d4d399bf370c302eb526'
ACTIVE = 'papers/A2-DYN-v108-referee-response'
REVIEW = 'reviews/a2-dyn-v107-positive-source-external-top4-review-2026-10-14/REFEREE_REPORT.md'
REVIEW_BLOB = '82cff2e2fc14e6a1eaa12b75fb41012dd155bdae'
REPLACED = {'main.tex','build.sh','README.md','SOURCE_MANIFEST.json',
            'PUBLICATION_STATUS.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md'}


def git(*args):
    return subprocess.check_output(['git',*args],cwd=P,text=True).strip()


def entries(tree):
    raw = subprocess.check_output(['git','ls-tree','-rz','--full-tree',tree],cwd=P)
    result = {}
    for item in raw.split(b'\0'):
        if item:
            meta,name = item.split(b'\t',1)
            mode,kind,sha = meta.decode().split()
            require(kind == 'blob','unexpected non-blob')
            result[name.decode()] = (mode,sha)
    require(bool(result),'empty tree')
    return result


def verify():
    require(not sys.argv[1:],'no bypass mode')
    head = git('rev-parse','HEAD')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'),'wrong exact checkout')
    require(git('rev-parse','HEAD:'+BASE_PATH) == BASE_TREE,'changed v107 directory')
    require(git('rev-parse','HEAD:'+REVIEW) == REVIEW_BLOB,'changed controlling report')
    require(git('rev-parse','HEAD:papers/A2-DYN-v106-referee-response') ==
            '6acebbc6669612b32171bb9f50b5bbbd7b77459f','changed historical v106 tree')
    allowed = {'A2_DYN_V108_REVISION_INDEX.md',
               '.github/workflows/a2-dyn-v108-canonical-capacity-qualification.yml'}
    changed = git('diff','--name-only',BASE,head).splitlines()
    require(all(p.startswith(ACTIVE+'/') or p in allowed for p in changed),'unrelated changes')
    old,new = entries(BASE_TREE),entries('HEAD:'+ACTIVE)
    for name,record in old.items():
        if name not in REPLACED:
            require(new.get(name) == record,'inherited file or mode changed: '+name)
    require(new['provenance/v107-main.tex'] == old['main.tex'],'wrong article snapshot')
    old_core = {n:v for n,v in old.items() if n.startswith('core/') and n.endswith('.tex')}
    new_core = {n:v for n,v in new.items() if n.startswith('core/') and n.endswith('.tex')}
    require(len(old_core) == 257 and len(new_core) == 259,'wrong core counts')
    require(all(new_core.get(n) == v for n,v in old_core.items()),'changed inherited core')
    for name,(mode,sha) in new.items():
        path = P/name
        data = path.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(actual == sha,'working bytes differ from HEAD: '+name)
        require(bool(path.stat().st_mode & 0o111) == (mode == '100755'),'mode: '+name)
    manifest = json.loads((P/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 108 and manifest['active_core_count'] == 259,'active manifest')
    require(manifest['baseline_paper_tree'] == BASE_TREE,'manifest baseline')
    require(set(manifest['replaced_root_files']) == REPLACED,'replacement list')
    for flag in ('full_raw_return_LLT_proved','primary_referee_request_closed',
                 'canonical_residual_height_decay_proved',
                 'complete_lorentz_comparison_interval_coverage_proved',
                 'collision_uniform_logarithmic_insertion_proved',
                 'independent_human_review','formal_proof_certificate'):
        require(manifest['claims'][flag] is False,'unsupported claim: '+flag)
    status = json.loads((P/'PUBLICATION_STATUS.json').read_text())
    require(status == {k:manifest[k] for k in ('inherited_packet','claims','superseded_claims')},
            'status differs from manifest')
    main = (P/'main.tex').read_text()
    require('\\input{provenance/v107-main}' in main,'inherited article is not included')
    for module in manifest['new_core_modules']:
        require('\\input{'+module[:-4]+'}' in main,'new proof not included')
    repair = json.loads((P/'provenance/v106-metadata-supersession.json').read_text())
    require(repair['corrected_identity']['revision'] == 106,'v106 supersession revision')
    require(repair['frozen_paper_tree'] ==
            git('rev-parse','HEAD:papers/A2-DYN-v106-referee-response'),'v106 supersession tree')
    from assemble_v105 import assemble
    assemble()
    math_commit = git('log','-1','--format=%H','--',str(P/'main.tex'),str(P/'core/258_canonical_roofwise_comparison_capacity.tex'),
                      str(P/'core/259_maximal_capacity_and_original_microscopic_residual.tex'))
    return {'revision':108,'checkout_sha':head,'theorem_bearing_commit':math_commit,
            'baseline_tree':BASE_TREE,'paper_tree':git('rev-parse','HEAD:'+ACTIVE),
            'inherited_core_count':257,'active_core_count':259,
            'preserved_inherited_files':len(old)-len(REPLACED),
            'source_scope_verified':True,'finite_checks':checks(),
            'formal_proof_certificate':False,'independent_human_review':False}


if __name__ == '__main__':
    print(json.dumps(verify(),sort_keys=True,indent=2))
