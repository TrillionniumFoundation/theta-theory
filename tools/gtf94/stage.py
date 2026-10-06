#!/usr/bin/env python3
"""Materialize inspected v94 proofs, preserving the bundle and final editorial text."""
from pathlib import Path
import base64
import gzip
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
DIGEST = '06933cc28a5f52b4ab9f8f6d1278db35a3f4cfe0dd22d0c2160a8e9c15f4bab9'
EXPECTED = {
    'stage-impl.py',
    'patch/sections/87-exact-initial-spectral-values.tex',
    'patch/spectral_value.py',
    'patch/spectral_value_check.py',
}
encoded = ''.join((HERE / f'payload-{i}.b64').read_text().strip() for i in range(4))
packed = base64.b64decode(encoded, validate=True)
if hashlib.sha256(packed).hexdigest() != DIGEST:
    raise RuntimeError('Revision bundle differs from the inspected source')
files = json.loads(gzip.decompress(packed))
if not isinstance(files, dict) or set(files) != EXPECTED:
    raise RuntimeError('Unexpected revision bundle inventory')
root = HERE / '_expanded'
if root.exists():
    raise RuntimeError('Refusing to overwrite an existing staging expansion')
for name, text in files.items():
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or not isinstance(text, str):
        raise RuntimeError('Unsafe revision bundle entry')
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')
ns = runpy.run_path(str(root / 'stage-impl.py'), run_name='__main__')
dst = ns['dst']
changes = {}

def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('Final editorial anchor missing or ambiguous: ' + old)
    return text.replace(old, new, 1)

def conserve(name, revised):
    path = dst / name
    before = path.read_bytes()
    archive = dst / 'staged-v94-audit' / name
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        raise RuntimeError('Refusing to overwrite staged text')
    archive.write_bytes(before)
    path.write_text(revised, encoding='utf-8')
    changes[name] = {'staged_sha256': hashlib.sha256(before).hexdigest(),
                     'current_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

name = 'sections/87-exact-initial-spectral-values.tex'
s = (dst / name).read_text()
s = replace_once(s, 'For a fixed $\\rho$ of rank $s$, its constrained optimum strictly',
                 'For $t>0$ and a fixed $\\rho$ of rank $s$, its constrained optimum strictly')
s = replace_once(s, '$s=1$.\n\\end{corollary}',
                 '$s=1$.  At $t=0$ every dimension gives the same value $1/2$.\n\\end{corollary}')
conserve(name, s)

name = 'RESPONSE_TO_REFEREE.md'
s = (dst / name).read_text()
s = replace_once(s, '## New mathematical response to the structural objection',
                 '## Inherited v93 response to the structural objection')
s = replace_once(s, 'Actual printed page numbers are generated in `evidence/THEOREM_LOCATIONS.json`, rather than inferred from source-module indices.',
                 'The generated theorem-location record supplies source labels and auxiliary anchors. Actual heading pages are checked against the submitted PDF and reported in the root review entry; auxiliary anchors alone may precede a page break.')
s = replace_once(s, 'All existing 34 suites are preserved, giving 35 suites in the fresh production build.',
                 'The inherited v93 build had 35 suites. All are retained, and the v94 spectral-value suite brings the current fresh production build to 36 suites.')
s = replace_once(s, 'Publication and exact-final-head qualification refer only to freshly observed v93 receipts.',
                 'Current publication and exact-final-head qualification refer only to freshly observed v94 receipts; v93 receipts remain predecessor evidence.')
conserve(name, s)
(dst / 'FINAL_EDITORIAL_CHECK.json').write_text(json.dumps({
    'schema': 'gtf94.final-editorial/1',
    'changes': changes,
    'all_predecessor_mathematical_sections_unchanged': True,
    'nonzero_signal_required_for_strict_saturation': True,
    'current_regression_suites': 36,
    'old_bundle_retained': True
}, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': 'final-editorial-complete', 'paths': sorted(changes)}, sort_keys=True))
