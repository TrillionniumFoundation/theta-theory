#!/usr/bin/env python3
"""Verify and expand immutable-base source edits into readable v137 files."""
from pathlib import Path, PurePosixPath
import argparse, base64, hashlib, json, lzma, subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='d15c9bcabdfc31070b773e2c8014601e75d4e641'
EXPECTED='5a14c2d9e25034d0769b52a2b2f9470c1e12bd285eeb96abfe320cb3f355a5bd'
ap=argparse.ArgumentParser();ap.add_argument('--base-root',type=Path);args=ap.parse_args()
parts=sorted(HERE.glob('transport-*.b64'))
if not parts:raise SystemExit('Missing source transport')
packed=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True)
if hashlib.sha256(packed).hexdigest()!=EXPECTED:raise SystemExit('Source transport checksum mismatch')
files=json.loads(lzma.decompress(packed))
if not isinstance(files,dict):raise SystemExit('Invalid source table')
def safe(name):
    q=PurePosixPath(name)
    if q.is_absolute() or '..' in q.parts:raise SystemExit('Unsafe path')
for name,entry in files.items():
    safe(name)
    if name!='assemble.py' and not name.startswith('overlay/'):raise SystemExit('Unexpected destination')
    if 'content' in entry:text=entry['content']
    else:
        source=entry['base_path'];safe(source)
        data=(args.base_root/source).read_bytes() if args.base_root else subprocess.check_output(['git','show',BASE+':'+source],cwd=ROOT)
        if hashlib.sha256(data).hexdigest()!=entry['base_sha256']:raise SystemExit('Immutable source mismatch: '+source)
        lines=data.decode().splitlines(keepends=True);last=0
        for i,j,replacement in entry['edits']:
            if not(last<=i<=j<=len(lines)) or not isinstance(replacement,str):raise SystemExit('Invalid edit ranges')
            last=j
        for i,j,replacement in reversed(entry['edits']):lines[i:j]=[replacement]
        text=''.join(lines)
    if not isinstance(text,str):raise SystemExit('Invalid text')
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
print(json.dumps({'sha256':EXPECTED,'readable_files_materialized':len(files),'immutable_base':BASE},indent=2))
