#!/usr/bin/env python3
"""Adversarial tests of source and nested-receipt qualification gates."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT/'tools/validate_v29.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
COUNT = 0


def require(ok: bool) -> None:
    global COUNT
    if not ok: raise RuntimeError('validation contract failed')
    COUNT += 1


def rejects(call) -> None:
    try: call()
    except (RuntimeError, KeyError, ValueError, OSError): require(True)
    else: require(False)


def main() -> None:
    v.require_commit('a'*40, 'a'*40); require(True)
    rejects(lambda: v.require_commit(None, 'a'*40))
    rejects(lambda: v.require_commit('b'*40, 'a'*40))
    rejects(lambda: v.require_commit('bad', 'bad'))
    doc = {'pages':1, 'pdf_sha256':'c'*64}
    base = {'status':'passed','scope':'all_declared_volumes',
            'full_package_qualified':True,'source_commit':'a'*40,
            'declared_document_count':11,'documents':[doc], 'retained_documents':[doc]*10}
    require(len(v.retained_documents(base, 'a'*40)) == 11)
    for key, value in [('status','failed'),('scope','primary_only'),
                        ('full_package_qualified',False),('source_commit','b'*40),
                        ('declared_document_count',10),('retained_documents',[])]:
        broken = copy.deepcopy(base); broken[key] = value
        rejects(lambda: v.retained_documents(broken, 'a'*40))
    broken = copy.deepcopy(base); broken['documents'][0]['pages'] = None
    rejects(lambda: v.retained_documents(broken, 'a'*40))
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for name in ('main.tex','references.tex','SOURCE_PINS.json'):
            shutil.copy2(ROOT/name, root/name)
        for name in ('core','tools'): shutil.copytree(ROOT/name, root/name)
        require(v.check_sources(root)['retained_v28_tree'] == v.RETAINED_TREE)
        pins_path = root/'SOURCE_PINS.json'; good_pins = pins_path.read_text()
        original = (root/'core/01_reversal.tex').read_text()
        (root/'core/01_reversal.tex').write_text(original+'% modification\n')
        rejects(lambda: v.check_sources(root))
        (root/'core/01_reversal.tex').write_text(original)
        (root/'core/unpinned.tex').write_text('unlisted mathematical input\n')
        rejects(lambda: v.check_sources(root)); (root/'core/unpinned.tex').unlink()
        for key, value in [('schema','old'),('retained_v28_tree','0'*40),('source_sha256',{})]:
            pins = json.loads(good_pins); pins[key] = value
            pins_path.write_text(json.dumps(pins)); rejects(lambda: v.check_sources(root))
        pins_path.write_text(good_pins)
        (root/'tools/verify_v29.py').unlink(); rejects(lambda: v.check_sources(root))
    print(json.dumps({'schema':'a2-v29-validation-contract-1','status':'passed',
                      'checks':COUNT,'formal_proof_certificate':False},sort_keys=True))

if __name__=='__main__': main()
