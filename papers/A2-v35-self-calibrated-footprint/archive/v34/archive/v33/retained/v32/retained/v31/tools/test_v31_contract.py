#!/usr/bin/env python3
"""Adversarial input and qualification contracts, counted separately from math."""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import tempfile
from reciprocal_intervals import (KilledKernel, compass_kernel, enclose, rational,
                                  solve_payload, geometric_tail)
from validate_v31 import (ROOT, check_sources, retained_documents, require_commit,
                          execution_kind, output_path)

COUNT=0

def require(ok, label):
    global COUNT
    if not ok: raise RuntimeError(label)
    COUNT+=1


def reject(fn, label):
    global COUNT
    try:
        fn()
    except (ValueError,RuntimeError,KeyError,FileNotFoundError,TypeError):
        COUNT+=1
    else:
        raise RuntimeError('accepted invalid input: '+label)


def main():
    check_sources(); require(True,'complete source map')
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name in ['main.tex','references.tex','SOURCE_PINS.json']:
            shutil.copy2(ROOT/name,root/name)
        for name in ['core','tools']:
            shutil.copytree(ROOT/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
        check_sources(root); require(True,'copied complete source')
        original=(root/'SOURCE_PINS.json').read_text()
        for key,value in [('schema','old'),('retained_v30_tree','0'*40),
                          ('workflow_sha256','bad'),('retained_active_core_sha256',{})]:
            pins=json.loads(original); pins[key]=value
            (root/'SOURCE_PINS.json').write_text(json.dumps(pins))
            reject(lambda:check_sources(root),'modified '+key)
        pins=json.loads(original); pins['source_sha256'].pop('core/09_mean_exit_inverse.tex')
        (root/'SOURCE_PINS.json').write_text(json.dumps(pins))
        reject(lambda:check_sources(root),'incomplete mathematical manifest')
        (root/'SOURCE_PINS.json').write_text(original)
        path=root/'core/09_mean_exit_inverse.tex'; data=path.read_bytes()
        path.write_bytes(data+b'\n'); reject(lambda:check_sources(root),'modified math')
        path.unlink(); reject(lambda:check_sources(root),'missing math')
        path.write_bytes(data)
        extra=root/'tools/unpinned.py'; extra.write_text('pass\n')
        reject(lambda:check_sources(root),'unlisted tool'); extra.unlink()
    sha='a'*40
    for actual,expected in [(None,sha),('b'*40,sha),(sha,'a'*39),(sha,'A'*40)]:
        reject(lambda a=actual,e=expected:require_commit(a,e),'source mismatch')
    require_commit(sha,sha); require(True,'exact commit')
    env={'GITHUB_ACTIONS':'true','GITHUB_SHA':sha,'GITHUB_RUN_ID':'42'}
    require(execution_kind(sha,True,env)=='hosted_exact_checkout','hosted classification')
    require(execution_kind(None,False,env)=='source_content','no invented source checkout')
    require(execution_kind(sha,True,{})=='local_exact_checkout','local classification')
    receipt={'status':'passed','full_package_qualified':True,'scope':'all_declared_volumes',
             'source_commit':sha,'declared_document_count':13,
             'documents':[{'pages':1,'pdf_sha256':'0'*64} for _ in range(13)]}
    require(len(retained_documents(receipt,sha))==13,'thirteen inherited documents')
    for key,value in [('status','failed'),('full_package_qualified',False),
                      ('scope','primary_only'),('source_commit','b'*40),
                      ('declared_document_count',12)]:
        wrong=copy.deepcopy(receipt); wrong[key]=value
        reject(lambda w=wrong:retained_documents(w,sha),'historical/incomplete receipt')
    for patch in [{'pages':0},{'pages':True},{'pdf_sha256':''}]:
        wrong=copy.deepcopy(receipt); wrong['documents'][0].update(patch)
        reject(lambda w=wrong:retained_documents(w,sha),'invalid PDF record')
    wrong=copy.deepcopy(receipt); wrong['documents'].pop()
    reject(lambda:retained_documents(wrong,sha),'missing volume')
    reject(lambda:output_path(ROOT,'../../escape'),'output traversal')
    for bad in (True,1.25,object(),'1/0','nan'):
        reject(lambda b=bad:rational(b),'nonexact rational')
    for args in [(0,2,1),(2,-1,1),(2,3,0),(True,2,1)]:
        reject(lambda a=args:compass_kernel(*a),'invalid grid')
    reject(lambda:KilledKernel((((0,F(2)),),)),'row exceeds one')
    reject(lambda:KilledKernel((((1,F(1)),),)),'index out of range')
    reject(lambda:KilledKernel((((0,F(-1)),),)),'negative weight')
    k=compass_kernel(2,2)
    reject(lambda:enclose(k,[F(0)]*3,[F(0)]*4,1),'forcing shape')
    reject(lambda:enclose(k,[F(1)]*4,[F(0)]*4,1),'reversed interval')
    reject(lambda:enclose(k,[F(0)]*4,[F(0)]*4,-1),'negative depth')
    reject(lambda:enclose(k,[F(0)]*4,[F(0)]*4,1,F(2)),'invalid tail')
    reject(lambda:geometric_tail(1,0),'invalid tail block')
    payload={'width':2,'height':2,'step':1,'iterations':2,
             'forcing_lower':['-1/2']*4,'forcing_upper':['-1/2']*4,
             'certified_survival_upper':'1/4'}
    answer=solve_payload(payload)
    require(answer['bounds']['iterate_lower']==['3/4']*4,'JSON exact round trip')
    require(answer['bounds']['occupation_upper']==['1']*4,'conditional JSON enclosure')
    reject(lambda:solve_payload({**payload,'claim':'unconditional'}),'unknown claim key')
    print(json.dumps({'schema':'a2-v31-validation-contract-1','status':'passed',
                      'total_checks':COUNT,'formal_proof_certificate':False},sort_keys=True))


if __name__=='__main__': main()
