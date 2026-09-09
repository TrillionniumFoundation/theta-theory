#!/usr/bin/env python3
"""Run current and inherited finite diagnostics in a disposable source copy.
The manuscript itself is native TeX and needs no restoration. Two historical
verification inputs can be read from the pinned v9 publication already in the
repository. No network or persistent source mutation is performed.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
PINS={'tools/verify_v9.py': 'fab73939adf284f3d14d45181570a8875e71c9f55fe7128f4dbf91f735a6656f', 'history/v8-source-baseline.json': '94884220b576e94d3f70d9d7c37d9471dd9526cceb30b23d06bf92d0da89525f'}
PAYLOAD_SHA256='eeba93cc4d5e0bc4f03d7dd2604bcdc13e62fd885b6cb8fe8195f3b367e687d0'
XZ_SHA256='ef947b9ee98acd7348d4e6d3b76a8d9f0384e63a9ea062afd30f30d48fff9a91'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def historical_inputs(source_dir=None):
    candidates=[source_dir] if source_dir else []
    candidates += [ROOT]
    for ancestor in ROOT.parents:
        candidates += [ancestor/'reference_v9']
    for base in candidates:
        if base is not None and all((base/p).is_file() for p in PINS):
            result={p:(base/p).read_bytes() for p in PINS}
            if all(digest(result[p])==expected for p,expected in PINS.items()):
                return result, 'authenticated_uncompressed_inputs'
    publication=next((a/'.publication/a2-v9' for a in ROOT.parents
                      if (a/'.publication/a2-v9/chunk-00.b64').is_file()),None)
    if publication is None:
        raise RuntimeError('Pinned v9 verification inputs not found. Use a full repository checkout, or --v9-source-dir PATH to an authenticated v9 source folder.')
    encoded=''.join(''.join((publication/f'chunk-{i:02d}.b64').read_text().split()) for i in range(8))
    compressed=base64.b64decode(encoded,validate=True)
    if digest(compressed)!=XZ_SHA256:
        raise RuntimeError('Original v9 XZ digest mismatch.')
    raw=lzma.decompress(compressed)
    if digest(raw)!=PAYLOAD_SHA256:
        raise RuntimeError('Original v9 JSON digest mismatch.')
    payload=json.loads(raw)
    result={p:payload['text'][p].encode('utf-8') for p in PINS}
    if not all(digest(result[p])==expected for p,expected in PINS.items()):
        raise RuntimeError('Historical diagnostic input digest mismatch.')
    return result,'authenticated_repository_publication'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--v9-source-dir',type=Path)
    args=parser.parse_args()
    data,origin=historical_inputs(args.v9_source_dir)
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    result={'schema':'a2-v10-suite-run-v1','historical_input_mode':origin,
            'historical_sha256':PINS,'remote_ci':False,'formal_proof_verification':False,'suites':{}}
    with tempfile.TemporaryDirectory(prefix='a2-v10-checks-') as tmp:
        work=Path(tmp)
        for p in ROOT.rglob('*'):
            if p.is_file() and p.suffix in ('.tex','.py','.json','.bib','.sty','.cls') and 'verification' not in p.relative_to(ROOT).parts:
                dest=work/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        for rel,content in data.items():
            dest=work/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
        for name,script in [('inherited','verify_revision.py'),('v9','verify_v9.py'),('v10','verify_v10.py')]:
            outputs=[]
            for optimized in (False,True):
                label='optimized' if optimized else 'normal'
                target=work/f'{name}.{label}.json'
                command=[sys.executable]+(['-O'] if optimized else [])+[str(work/'tools'/script),'--output',str(target)]
                run=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
                if run.returncode:
                    raise RuntimeError(name+': '+run.stdout)
                content=target.read_bytes();outputs.append(content)
                (out/f'{name}.{label}.json').write_bytes(content)
            if outputs[0]!=outputs[1]:
                raise RuntimeError(name+': normal and optimized outputs differ.')
            parsed=json.loads(outputs[0])
            result['suites'][name]={'status':parsed['status'],'counts':parsed['counts'],
                'normal_optimized_byte_identical':True,'result_sha256':digest(outputs[0])}
    result['status']='pass'
    (out/'ALL_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
