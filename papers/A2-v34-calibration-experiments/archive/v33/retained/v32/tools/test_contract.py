#!/usr/bin/env python3
"""Finite failure-mode tests for source qualification and exact solver contracts."""
from __future__ import annotations
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import tempfile
import adaptive_scalar as a
import validate_v32 as v

COUNT = 0

def require(ok: bool) -> None:
    global COUNT
    if not ok: raise RuntimeError('contract expectation failed')
    COUNT += 1

def rejects(fn) -> None:
    try: fn()
    except (ValueError, TypeError, RuntimeError, KeyError): require(True)
    else: require(False)

def main() -> None:
    sha='1'*40
    require(v.execution_kind(None,False,{})=='source_content')
    require(v.execution_kind(sha,False,{})=='source_content')
    require(v.execution_kind(sha,True,{})=='local_exact_checkout')
    require(v.execution_kind(sha,True,{'GITHUB_ACTIONS':'true','GITHUB_RUN_ID':'9','GITHUB_SHA':sha})=='hosted_exact_checkout')
    require(v.execution_kind(sha,True,{'GITHUB_ACTIONS':'true','GITHUB_RUN_ID':'9','GITHUB_SHA':'2'*40})!='hosted_exact_checkout')
    v.require_commit(sha,sha); require(True)
    for expected in ('bad','2'*40): rejects(lambda:v.require_commit(sha,expected))
    rejects(lambda:v.require_commit(None,sha))
    doc={'pages':1,'pdf_sha256':'a'*64}
    receipt={'status':'passed','full_package_qualified':True,'scope':'all_declared_volumes',
             'source_commit':sha,'declared_document_count':14,'documents':[doc],
             'retained_documents':[copy.deepcopy(doc) for _ in range(13)]}
    require(len(v.retained_documents(receipt,sha))==14)
    for key,value in [('status','failed'),('full_package_qualified',False),
                      ('scope','primary_only'),('source_commit','2'*40),('declared_document_count',13)]:
        wrong=copy.deepcopy(receipt);wrong[key]=value
        rejects(lambda:v.retained_documents(wrong,sha))
    for bad in (0,True,None,-1):
        wrong=copy.deepcopy(receipt);wrong['documents'][0]['pages']=bad
        rejects(lambda:v.retained_documents(wrong,sha))
    wrong=copy.deepcopy(receipt);wrong['documents'][0]['pdf_sha256']='bad'
    rejects(lambda:v.retained_documents(wrong,sha))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name in (*v.REQUIRED,'SOURCE_PINS.json'):
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(v.ROOT/name,p)
        pins=json.loads((root/'SOURCE_PINS.json').read_text())
        require(v.check_sources(root)['schema']=='a2-v32-source-pins-1')
        for key,value in [('schema','old'),('review_commit','2'*40),('retained_v31_tree','2'*40),
                          ('workflow_sha256','bad'),('full_package_document_count',14),('source_sha256',{})]:
            wrong=copy.deepcopy(pins);wrong[key]=value
            (root/'SOURCE_PINS.json').write_text(json.dumps(wrong))
            rejects(lambda:v.check_sources(root))
        (root/'SOURCE_PINS.json').write_text(json.dumps(pins))
        (root/'main.tex').write_text('altered')
        rejects(lambda:v.check_sources(root))
        (root/'main.tex').unlink()
        rejects(lambda:v.check_sources(root))
        require(v.output_path(root,'verification/current').is_relative_to(root))
        rejects(lambda:v.output_path(root,'../escape'))
        rejects(lambda:v.output_path(root,'main.tex'))
    rejects(lambda:a.Interval(F(2),F(1)))
    rejects(lambda:a.Interval(0,1))
    rejects(lambda:a.local_interval({},0,lambda p:True,F(0)))
    rejects(lambda:a.local_interval({},1,lambda p:True,F(0)))
    rejects(lambda:a.local_interval({},1,lambda p:False,F(0)))
    rejects(lambda:a.local_interval({},1,lambda p:True,F(2)))
    rejects(lambda:a.fuzzy_bisect(lambda x:1,F(0),F(1),F(0),1))
    rejects(lambda:a.fuzzy_bisect(lambda x:True,F(1),F(0),F(0),1))
    rejects(lambda:a.lagrange_weights(F(0),7))
    rejects(lambda:a.radial_interpolate([1.]*8,0.))
    print(json.dumps({'status':'passed','contract_checks':COUNT,
                      'formal_proof_certificate':False},sort_keys=True))

if __name__=='__main__': main()
