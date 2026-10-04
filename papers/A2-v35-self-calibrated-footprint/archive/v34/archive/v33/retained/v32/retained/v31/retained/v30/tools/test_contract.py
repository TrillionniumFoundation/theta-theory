#!/usr/bin/env python3
"""Adversarial tests of source binding, receipt inventory and public interfaces."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import tempfile
import numpy as np
from validate_v30 import (ROOT, check_sources, require_commit, retained_documents,
                          execution_kind, output_path)
from reconstruct_scalar import chain_inverse, bellman_inverse, threshold_hulls, lock_rational
CHECKS = 0


def expect_failure(fn, label):
    global CHECKS
    try:
        fn()
    except (ValueError,RuntimeError,KeyError,FileNotFoundError):
        CHECKS += 1
    else:
        raise RuntimeError('accepted invalid input: '+label)


def require(ok, label):
    global CHECKS
    if not ok:
        raise RuntimeError(label)
    CHECKS += 1


def main():
    check_sources(); require(True,'current manifest')
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name in ['main.tex','references.tex','SOURCE_PINS.json']:
            shutil.copy2(ROOT/name,root/name)
        for directory in ['core','tools']:
            shutil.copytree(ROOT/directory,root/directory,ignore=shutil.ignore_patterns('__pycache__'))
        check_sources(root); require(True,'copied manifest')
        original=(root/'SOURCE_PINS.json').read_text()
        for key,value in [('schema','wrong'),('retained_v29_tree','0'*40),('workflow_sha256','x')]:
            pins=json.loads(original); pins[key]=value
            (root/'SOURCE_PINS.json').write_text(json.dumps(pins))
            expect_failure(lambda:check_sources(root),'pin '+key)
        pins=json.loads(original); pins['source_sha256'].pop('main.tex')
        (root/'SOURCE_PINS.json').write_text(json.dumps(pins))
        expect_failure(lambda:check_sources(root),'incomplete source map')
        (root/'SOURCE_PINS.json').write_text(original)
        path=root/'core/06_calibrated_launches.tex'; data=path.read_bytes()
        path.write_bytes(data+b'\n')
        expect_failure(lambda:check_sources(root),'modified mathematical source')
        path.unlink(); expect_failure(lambda:check_sources(root),'missing mathematical source')
        path.write_bytes(data)
        extra=root/'core/unpinned.tex'; extra.write_text('unqualified')
        expect_failure(lambda:check_sources(root),'unlisted mathematical input')
        extra.unlink()
    sha='a'*40
    for actual,expected in [(None,sha),('b'*40,sha),(sha,'a'*39),(sha,'A'*40)]:
        expect_failure(lambda a=actual,e=expected:require_commit(a,e),'commit mismatch')
    require_commit(sha,sha); require(True,'matching commit')
    env={'GITHUB_ACTIONS':'true','GITHUB_SHA':sha,'GITHUB_RUN_ID':'123'}
    require(execution_kind(sha,True,env)=='hosted_exact_checkout','hosted classification')
    require(execution_kind(None,False,env)=='source_content','no invented checkout')
    require(execution_kind(sha,True,{})=='local_exact_checkout','local classification')
    require(execution_kind(sha,True,{**env,'GITHUB_SHA':'b'*40})!='hosted_exact_checkout',
            'mismatched hosting cannot pass')
    receipt={'status':'passed','full_package_qualified':True,'scope':'all_declared_volumes',
             'source_commit':sha,'declared_document_count':12,
             'documents':[{'pages':1,'pdf_sha256':'0'*64} for _ in range(12)]}
    require(len(retained_documents(receipt,sha))==12,'valid inventory')
    for key,value in [('status','failed'),('full_package_qualified',False),
                      ('scope','primary_only'),('source_commit','b'*40),('declared_document_count',11)]:
        bad=copy.deepcopy(receipt); bad[key]=value
        expect_failure(lambda b=bad:retained_documents(b,sha),'receipt '+key)
    for patch in [{'pages':0},{'pages':True},{'pdf_sha256':''}]:
        bad=copy.deepcopy(receipt); bad['documents'][0].update(patch)
        expect_failure(lambda b=bad:retained_documents(b,sha),'incomplete PDF')
    bad=copy.deepcopy(receipt); bad['documents'].pop()
    expect_failure(lambda:retained_documents(bad,sha),'missing retained document')
    expect_failure(lambda:output_path(ROOT,'../../escape'),'output traversal')
    expect_failure(lambda:chain_inverse(np.array([1.,2.])),'chain shape')
    expect_failure(lambda:chain_inverse(np.array([[float('nan')]])),'nonfinite chain')
    expect_failure(lambda:bellman_inverse([[.9]],[0],1),'nonstochastic operator')
    expect_failure(lambda:threshold_hulls(np.zeros((2,2)),np.zeros(1),.1),'point/value mismatch')
    expect_failure(lambda:lock_rational(.5,5,.1),'unseparated rational interval')
    print(json.dumps({'schema':'a2-v30-validation-contract-1','status':'passed',
                      'total_checks':CHECKS,'formal_proof_certificate':False},sort_keys=True))

if __name__ == '__main__':
    main()
