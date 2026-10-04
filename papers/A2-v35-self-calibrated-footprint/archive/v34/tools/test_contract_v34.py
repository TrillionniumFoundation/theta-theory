#!/usr/bin/env python3
"""Executable rejection tests for publication binding and journal scope."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
from validate_v34 import ARCHIVE_TREE, validate_contract, git_tree

checks=0
actual={'main.tex':'a'*64,'core/proof.tex':'b'*64}
pins={'schema':'a2-v34-source-pins-1','journal_documents':['main.tex'],
      'source_sha256':actual.copy(),'archive_v33_tree':ARCHIVE_TREE}

def call(p, m=actual, a=ARCHIVE_TREE, expected=None, commit=None, required=False):
    validate_contract(p,m,a,expected,commit,required)

def reject(fn):
    global checks
    try:
        fn()
    except ValueError:
        checks+=1
    else:
        raise RuntimeError('invalid contract accepted')

call(pins); checks+=1
call(pins,expected='c'*40,commit='c'*40,required=True); checks+=1
for field in pins:
    bad=copy.deepcopy(pins); del bad[field]
    reject(lambda:call(bad))
for docs in [[],['archive/v33/main.tex'],['main.tex','archive/v33/main.tex']]:
    bad=copy.deepcopy(pins); bad['journal_documents']=docs
    reject(lambda:call(bad))
for m in [{},{'main.tex':'a'*64},{**actual,'hidden.py':'d'*64},{**actual,'main.tex':'e'*64}]:
    reject(lambda:call(pins,m=m))
reject(lambda:call(pins,a='0'*40))
reject(lambda:call(pins,required=True))
reject(lambda:call(pins,expected='a'*40,commit='b'*40,required=True))
reject(lambda:call(pins,expected='a'*40,commit=None))
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    if git_tree(root)!='4b825dc642cb6eb9a060e54bf8d69288fbee4904':
        raise RuntimeError('incorrect empty Git tree')
    checks+=1
    (root/'proof.tex').write_text('proof\n'); original=git_tree(root)
    (root/'proof.tex').write_text('changed\n')
    if git_tree(root)==original:
        raise RuntimeError('content modification undetected')
    checks+=1
    (root/'proof.tex').write_text('proof\n'); (root/'proof.tex').chmod(0o755)
    if git_tree(root)==original:
        raise RuntimeError('mode modification undetected')
    checks+=1
    (root/'alias').symlink_to(root/'proof.tex')
    reject(lambda:git_tree(root))
print(json.dumps({'schema':'a2-v34-contract-tests-1','status':'passed',
                  'contract_checks':checks,'formal_proof_certificate':False},sort_keys=True))
