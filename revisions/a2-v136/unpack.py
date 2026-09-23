#!/usr/bin/env python3
"""Verify the source transport; expand readable overlays without altering v135."""
from pathlib import Path, PurePosixPath
import argparse, base64, hashlib, io, json, lzma, shutil, subprocess, tarfile, tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='9fb3a5b9b27d4f6c6df2f3e557b4fc709c3a546d'
SOURCE='papers/A2-v17-boundary-information-coarsening/article/v135'
EXPECTED='f42775f2d56c725979b6df839615cf245632272f5b771deff74a408ad2269a6a'
def safe(n):
    p=PurePosixPath(n)
    if p.is_absolute() or '..' in p.parts or not p.parts:raise RuntimeError('Unsafe path: '+n)
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base-dir',type=Path);args=ap.parse_args()
    parts=sorted(HERE.glob('transport-*.b64'))
    if [p.name for p in parts]!=['transport-01.b64','transport-02.b64','transport-03.b64']:raise RuntimeError('Transport part list differs')
    data=lzma.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True))
    if hashlib.sha256(data).hexdigest()!=EXPECTED:raise RuntimeError('Transport SHA256 mismatch')
    bundle=json.loads(data)
    with tempfile.TemporaryDirectory(prefix='a2-v136-overlay-') as td:
        td=Path(td)
        if args.base_dir:shutil.copytree(args.base_dir,td/'base')
        else:
            arbytes=subprocess.check_output(['git','archive',BASE,SOURCE],cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(arbytes)) as ar:
                for m in ar.getmembers():
                    p=safe(m.name)
                    if not (m.isfile() or m.isdir()):raise RuntimeError('Unexpected archive member')
                    d=td/'archive'/p
                    if m.isdir():d.mkdir(parents=True,exist_ok=True)
                    else:d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(ar.extractfile(m).read())
            shutil.move(str(td/'archive'/SOURCE),td/'base')
        for line in bundle['patch'].splitlines():
            if line.startswith(('--- a/','+++ b/')):safe(line[6:])
        subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1'],cwd=td/'base',input=bundle['patch'],text=True,check=True)
        for n,h in bundle['files_sha256'].items():
            safe(n);src=td/'base'/n
            if hashlib.sha256(src.read_bytes()).hexdigest()!=h:raise RuntimeError('Expanded source hash mismatch: '+n)
        # No user or reviewed file is changed: expansion is confined to this revision.
        for n in bundle['files_sha256']:
            dest=HERE/'overlay'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(td/'base'/n,dest)
    (HERE/'assemble.py').write_text(bundle['assemble.py'])
    (HERE/'SOURCE_TRANSPORT_RECEIPT.json').write_text(json.dumps({'sha256_uncompressed':EXPECTED,'overlay_files_sha256':bundle['files_sha256'],'ok':True},indent=2)+'\n')
    print('Verified and expanded',len(bundle['files_sha256']),'readable source overlays')
if __name__=='__main__':main()
