#!/usr/bin/env python3
"""Materialize the exact locally validated v23 sources in a new directory only."""
from pathlib import Path, PurePosixPath
import hashlib, json, lzma, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
TARGET=ROOT/'papers/A1-english-v23'
BASE=ROOT/'papers/A1-english-v22'
REVIEW='325e89b9c012830cbd219fec0cff7c52b8e8d321'
PATCH_HASH='a7830e44205efd57b0777c34f45c12786b5a75fa2a82e7dd2cdb5e4e988f24ce'
MANIFEST_HASH='7f6ec60f20d0a8fbedc47d6d3c8be63fa1b61b001ff53d7b480e1384cc57941e'
def digest(data): return hashlib.sha256(data).hexdigest()
def main():
    subprocess.run(['git','merge-base','--is-ancestor',REVIEW,'HEAD'],cwd=ROOT,check=True)
    compressed=b''.join((HERE/f'patch-{i}.xzpart').read_bytes() for i in (1,2))
    raw=lzma.decompress(compressed)
    if digest(raw)!=PATCH_HASH: raise ValueError('Revision payload identity mismatch')
    changes=json.loads(raw)
    if len(changes)!=17: raise ValueError('Unexpected revision file count')
    if TARGET.exists():
        subprocess.run([sys.executable,'manifest.py'],cwd=TARGET,check=True)
        if digest((TARGET/'SOURCE_MANIFEST.json').read_bytes())!=MANIFEST_HASH:
            raise ValueError('Refusing to overwrite a different existing v23 revision')
        return
    shutil.copytree(BASE,TARGET)
    for name in ('build','validation','__pycache__'):
        shutil.rmtree(TARGET/name,ignore_errors=True)
    for name in ('main.pdf','main.log','main.aux','main.out','main.toc',
                 'BUILD_REPORT.json','PRESERVATION_REPORT.json','SOURCE_MANIFEST.json'):
        (TARGET/name).unlink(missing_ok=True)
    for name,item in changes.items():
        rel=PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('Unsafe revision path')
        target=TARGET/name
        if 'text' in item:
            if target.exists(): raise ValueError('New source already exists: '+name)
            result=item['text']
        else:
            source=target.read_bytes()
            if digest(source)!=item['base_sha256']: raise ValueError('Base source mismatch: '+name)
            lines=source.decode().splitlines(keepends=True)
            for i,j,replacement in reversed(item['edits']): lines[i:j]=replacement
            result=''.join(lines)
        if digest(result.encode())!=item['sha256']: raise ValueError('Result source mismatch: '+name)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(result,encoding='utf-8')
    subprocess.run([sys.executable,'manifest.py','--write'],cwd=TARGET,check=True)
    if digest((TARGET/'SOURCE_MANIFEST.json').read_bytes())!=MANIFEST_HASH:
        raise ValueError('Materialized sources differ from the locally validated revision')
    (TARGET/'validation').mkdir(exist_ok=True)
    (TARGET/'validation/MATERIALIZATION_V23.json').write_text(json.dumps({
        'version':23,'controlling_review':REVIEW,'patch_sha256':PATCH_HASH,
        'source_manifest_sha256':MANIFEST_HASH,'changed_or_new_source_files':17,
        'source_files':772,'scope':'Source identity, not mathematical certification.'},indent=2)+'\n')
    print('Exact v23 source materialized; inherited revisions unchanged.')
if __name__=='__main__': main()
