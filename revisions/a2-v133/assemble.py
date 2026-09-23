#!/usr/bin/env python3
"""Expand an immutable reviewed manuscript and a hash-checked revision payload.

Only the new article/v133 destination is generated. Original sources/reviews
are never modified. All compiled mathematical inputs and labels are retained.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='d76f34db1aaa8e196a7b50f4ec04be381d45236e'
REVIEWED='6d8fcb430efa95624a15aa684cfccab79c793350'
SOURCE=Path('papers/A2-v17-boundary-information-coarsening/article/v132')
DEST=SOURCE.with_name('v133')
PAYLOAD_SHA='04950ce2be79ef4f550a64de7e6041a6a21897fc5fdb6a95a4cdb34867bd1e9b'
REVIEW='reviews/a2-v132-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'
sha=lambda b:hashlib.sha256(b).hexdigest()

def safe_unpack(data:bytes, destination:Path):
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as archive:
        for member in archive.getmembers():
            p=PurePosixPath(member.name)
            if p.is_absolute() or '..' in p.parts or not (member.isfile() or member.isdir()):
                raise RuntimeError(f'Unsafe archive member: {member.name}')
            if member.isdir():
                (destination/member.name).mkdir(parents=True,exist_ok=True)
            else:
                target=destination/member.name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())

def compiled(root:Path):
    seen=set(); text=[]
    def visit(name):
        if name in seen:return
        if '..' in Path(name).parts:raise RuntimeError(name)
        seen.add(name)
        s=(root/name).read_text(); text.append(s)
        for child in re.findall(r'\\input\{([^}]+)\}',s):visit(child)
    visit('geometry.tex')
    return seen,set(re.findall(r'\\label\{([^}]+)\}','\n'.join(text)))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--local',action='store_true',help='Use the locally downloaded reviewed artifact for preflight only')
    args=parser.parse_args()
    payload=(HERE/'payload.part0').read_bytes()+b''.join(
        (HERE/f'payload.part1.{i}').read_bytes() for i in range(6))
    if sha(payload)!=PAYLOAD_SHA:raise RuntimeError('Transfer payload hash mismatch')
    with tempfile.TemporaryDirectory(prefix='a2-v133-') as tmp:
        tmp=Path(tmp)
        if args.local:
            base=ROOT/SOURCE
            assembly='local-preflight-not-a-remote-commit'
        else:
            subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
            archive=subprocess.check_output(['git','archive',BASE,str(SOURCE)],cwd=ROOT)
            safe_unpack(archive,tmp/'reviewed')
            base=tmp/'reviewed'/SOURCE
            assembly=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        prior=json.loads((base/'PROVENANCE_MANIFEST.json').read_text())
        for name, expected in prior['assembled_sha256'].items():
            if sha((base/name).read_bytes())!=expected:
                raise RuntimeError(f'Reviewed source hash mismatch: {name}')
        original_inputs,original_labels=compiled(base)
        target=tmp/'article'
        shutil.copytree(base,target)
        # Only inherited generated products in the new copy are removed.
        shutil.rmtree(target/'evidence',ignore_errors=True)
        for p in list(target.rglob('__pycache__')):shutil.rmtree(p)
        for ext in ['pdf','aux','out','log']:
            (target/f'geometry.{ext}').unlink(missing_ok=True)
        safe_unpack(payload,tmp/'payload')
        spec=importlib.util.spec_from_file_location('a2_v133_transform',tmp/'payload/transform.py')
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        module.transform(target)
        for p in (tmp/'payload/overlays').rglob('*'):
            if p.is_file():
                out=target/p.relative_to(tmp/'payload/overlays')
                out.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,out)
        current_inputs,current_labels=compiled(target)
        if not original_inputs<=current_inputs:raise RuntimeError('An inherited compiled input was lost')
        if not original_labels<=current_labels:raise RuntimeError('An inherited mathematical label was lost')
        sources={str(p.relative_to(target)):sha(p.read_bytes())
                 for p in sorted(target.rglob('*')) if p.is_file()
                 and p.suffix in {'.tex','.py','.sh','.md','.json'}
                 and p.name not in {'PROVENANCE_MANIFEST.json','PROVENANCE_MANIFEST.md'}
                 and 'evidence' not in p.parts}
        unchanged={str(p.relative_to(base)):sha(p.read_bytes())
                   for p in sorted(base.rglob('*.tex'))
                   if (target/p.relative_to(base)).read_bytes()==p.read_bytes()}
        manifest={'revision':133,'assembly_commit':assembly,'reviewed_commit':REVIEWED,
          'controlling_review_commit':BASE,'controlling_review':REVIEW,
          'payload_sha256':PAYLOAD_SHA,'inherited_compiled_inputs':sorted(original_inputs),
          'inherited_mathematical_labels':sorted(original_labels),
          'unchanged_inherited_tex_sha256':unchanged,'assembled_sha256':sources}
        (target/'PROVENANCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (target/'PROVENANCE_MANIFEST.md').write_text(
          '# A2 v133 source provenance\n\nComplete v132 source at review commit `'+BASE+
          '`; prior source hashes verified before modification.\n'
          'All inherited compiled LaTeX inputs and mathematical labels are preserved.\n'
          'The JSON manifest binds the exact resulting source and immutable transfer payload.\n'
          'The executed build receipt distinguishes finite tests from written mathematical proofs.\n')
        final=ROOT/DEST
        if final.exists():
            old=final/'PROVENANCE_MANIFEST.json'
            if not old.exists() or json.loads(old.read_text()).get('revision')!=133:
                raise RuntimeError('Refusing to overwrite an unrecognized destination')
            shutil.rmtree(final)
        shutil.copytree(target,final)
        print(json.dumps({'destination':str(DEST),'assembly_commit':assembly,
          'inherited_compiled_inputs':len(original_inputs),'inherited_labels':len(original_labels),
          'unchanged_tex_files':len(unchanged),'source_files':len(sources)},indent=2))
if __name__=='__main__':main()
