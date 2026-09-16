#!/usr/bin/env python3
"""Apply the checked v64 manuscript delta to the immutable v63 review baseline."""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'papers/A2-v17-boundary-information-coarsening'
P = ROOT / PREFIX
BASE = 'f5517519440b897707ddc60deeafba19e86bb5a5'
BASE_TREE = 'b042811c7ceb2c5fd841b2a03ab0b8c232c39dce'
EXPECTED_TREE = '513b2538cea797cb340e02e69f45543f8b4e9571'
PAYLOAD_HASH = '92dab7b4a5f9aa91868499976d19bbaa11df7b3c118dc3ee96643b2181dd7dfc'
MODIFIED = {'README.md','main.tex','rigidity.tex','article/00_structural_introduction_v48.tex','journal/00_principal_introduction_v61.tex'}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True)
    return p.stdout.decode().strip()


def safe(name):
    p = Path(name)
    require(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name,
            'Unsafe patch path')
    return p


def main():
    require(git('rev-parse','HEAD:'+PREFIX) == BASE_TREE, 'Unexpected mathematical baseline')
    delivery = ROOT / 'deliveries/a2-v63' / BASE
    mf_bytes = (delivery/'frozen-source-manifest.json').read_bytes()
    af_bytes = (delivery/'active-source-manifest.json').read_bytes()
    require(sha(mf_bytes) == '11fe9282b58ef9ea11f867259bed18a9a8025080b36c71aee1d6a7157bd53387', 'Baseline source manifest changed')
    require(sha(af_bytes) == '67c8039dca729978d2a0107ced2adce70ea4c44421583b5b1321920ae7ad2d4c', 'Baseline active manifest changed')
    mf = json.loads(mf_bytes)
    require(mf['source_commit'] == BASE and mf['source_tree'] == BASE_TREE and len(mf['files']) == 784, 'Manifest identity')
    for name, meta in mf['files'].items():
        path = P/safe(name)
        require(path.is_file() and not path.is_symlink(), 'Missing baseline path: '+name)
        data = path.read_bytes()
        require(len(data) == meta['bytes'] and sha(data) == meta['sha256'], 'Baseline byte mismatch: '+name)
        require(bool(path.stat().st_mode & 0o111) == (meta['mode']=='100755'), 'Baseline mode mismatch: '+name)
    parts = sorted(Path(__file__).parent.glob('a2-v64-payload-*.b64'))
    require([p.name for p in parts] == ['a2-v64-payload-%02d.b64'%i for i in range(4)], 'Payload inventory')
    packed = base64.b64decode(''.join(p.read_text().strip() for p in parts), validate=True)
    require(sha(packed) == PAYLOAD_HASH, 'Payload hash mismatch')
    obj = json.loads(lzma.decompress(packed))
    require(obj['schema'] == 'a2-v64-materialization-2', 'Unexpected payload schema')
    outputs = {}
    for name, item in obj['files'].items():
        safe(name)
        if 'edits' in item:
            require(name in MODIFIED, 'Unauthorized inherited edit')
            original = (P/name).read_bytes()
            require(sha(original) == item['base_sha256'], 'Patch base mismatch: '+name)
            lines = original.decode().splitlines(keepends=True)
            for edit in reversed(item['edits']):
                i,j=edit['start'],edit['end']
                require(0 <= i <= j <= len(lines) and ''.join(lines[i:j]) == edit['old'], 'Patch context mismatch: '+name)
                lines[i:j] = edit['new'].splitlines(keepends=True)
            data = ''.join(lines).encode()
        else:
            require(not (P/name).exists(), 'New payload path already exists: '+name)
            data = item['text'].encode()
        require(sha(data) == item['sha256'] and item['mode'] in ('100644','100755'), 'Output identity: '+name)
        outputs[name] = (data,item['mode'])
    require(set(n for n in outputs if n in mf['files']) == MODIFIED, 'Inherited edit set')
    archive = P/'history/v63-review-baseline'
    require(not archive.exists(), 'Refusing to overwrite v63 originals')
    for name in sorted(MODIFIED):
        dest=archive/name; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(P/name,dest)
    (archive/'SOURCE_MANIFEST.json').write_bytes(mf_bytes)
    (archive/'ACTIVE_MANIFEST.json').write_bytes(af_bytes)
    for name,(data,mode) in outputs.items():
        path=P/name; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data);path.chmod(0o755 if mode=='100755' else 0o644)
    old_readme=ROOT/'README.md'
    require(git('hash-object','README.md') == '6a0701524d5885c0fe44d314d3050fd1feecf0eb', 'Root README baseline changed')
    require(not (ROOT/'README_PRE_V64.md').exists(), 'Refusing to overwrite historical root index')
    shutil.copy2(old_readme,ROOT/'README_PRE_V64.md')
    (ROOT/'README.md').write_text('''# Theta-Theory — A2 revision 64\n\n**Boundary laws and rigidity of periodic dispersing billiards** — Qian Qi, September 16, 2026.\n\nThe full English source revision addresses the v63 report at `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc`. It extends the relative physical mechanism to selected nongrazing periodic itineraries, with exact periodic Jacobi normalization, restored oblique momenta and a three-obstacle realization. All original inverse and statistical conclusions remain.\n\n[Revision index](A2_REVISION_V64_INDEX.md) · [Point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V64.md) · [Complete principal source](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Full technical source](papers/A2-v17-boundary-information-coarsening/main.tex).\n\nThe immutable-source native workflow builds all three complete entries and publishes source-matched PDFs on a new native-products branch. Its result and the final next-review branch are recorded in the revision index after verification. This source commit alone does not assert that a later workflow has succeeded. The previous root index is preserved in `README_PRE_V64.md`; no default branch, review branch or A1 source is rewritten.\n''')
    (ROOT/'A2_REVISION_V64_INDEX.md').write_text('''# A2 revision 64 — source revision and native-build route\n\nReport addressed: `review/a2-v63-independent-harsh-top4-2026-09-16`, commit `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc`.\n\nSource branch: `revision/a2-v64-referee-response-2026-09-16`. Expected manuscript subtree: `513b2538cea797cb340e02e69f45543f8b4e9571`. The materialization commit is the mathematical source; the workflow records that exact commit before compilation.\n\nThe complete `rigidity.tex`, `main.tex` and `two_collision.tex` entries remain under `papers/A2-v17-boundary-information-coarsening/`. The shared v64 section contains the geometric periodic-itinerary relative theorem and all supporting proofs, the physical window law, nonlinear transmission and a nonnormal realization. See [response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V64.md), [cover letter](papers/A2-v17-boundary-information-coarsening/COVER_LETTER_V64.md) and [dependency ledger](papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V64.md).\n\nAll 784 inherited paths remain; 779 are byte-identical, five have archived originals. All 127 original active inputs and the unchanged complete finite-experiment module remain. The active union is 129. The next-review index will identify actual source-matched native products after a successful run and independent retrieval; this source-stage record makes no advance claim of workflow success.\n\nThe new general forward law does not extend the alternating two-contact inverse by assumption. The highest general-journal submission objective is unchanged, and significance remains for independent assessment.\n''')
    git('add','--',PREFIX,'README.md','README_PRE_V64.md','A2_REVISION_V64_INDEX.md')
    tree=git('write-tree')
    require(git('rev-parse',tree+':'+PREFIX) == EXPECTED_TREE, 'Materialized manuscript tree mismatch')
    print(json.dumps({'status':'passed','baseline_source':BASE,'baseline_files_verified':784,
                      'expected_manuscript_tree':EXPECTED_TREE,'payload_sha256':PAYLOAD_HASH,
                      'changed_or_new_payload_files':len(outputs),'archived_originals':5},indent=2,sort_keys=True))


if __name__=='__main__':main()
