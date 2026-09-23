#!/usr/bin/env python3
"""Materialize the hash-bound v18 plaintext payload; never alter predecessor files."""
from pathlib import Path
import base64,hashlib,json,lzma,sys
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'papers/GTF-I-v18-continuation-transport'
O=ROOT/'papers/GTF-I-v17-intrinsic-adaptive-testing'
EXPECTED='10c4739e5453842c0c308ed71ae89cf9e0da5f0c389e764b86ce07477a52662c'
parts=sorted((P/'transport').glob('part-*.b64'))
if len(parts)!=6:raise RuntimeError('Expected six transport parts')
packed=base64.b64decode(''.join(x.read_text().strip() for x in parts),validate=True)
if hashlib.sha256(packed).hexdigest()!=EXPECTED:raise RuntimeError('Transport digest mismatch')
raw=lzma.decompress(packed)
if len(raw)>2_000_000:raise RuntimeError('Unexpected payload size')
files=json.loads(raw)
for name in files:
 if Path(name).name!=name or Path(name).suffix not in {'.tex','.py','.md','.txt','.json'}:raise RuntimeError('Unsafe payload path')
for name in ('preamble.tex','intrinsic-deficiency.tex','nonlinear-testing.tex','collision-resource-gap.tex'):
 files[name]=(O/name).read_text()
s=(O/'adaptive-testing.tex').read_text()
a=r'\begin{theorem}[Independent adaptive testing duality]';b=r'\begin{theorem}[Revealed-behavior adaptive representation]'
if s.count(a)!=1:raise RuntimeError('Adaptive source anchor mismatch')
s=s.replace(a,b)
a=r'\subsection{Strict certificates and effective physical input}'
b=r'''The infinite-dimensional representation above holds for continuous $f_i$
on any compact metric space: its proof uses a partition of unity, not causal
factorization. The measure minimum is attained at a Dirac mass at a minimizer
of $F$. The finite-level polynomial theorem has a different content. It is
an existence-size bound for revealed-law verification; the reset-audit theorem
of Section~\ref{sec:v18-audit} imposes an explicit finite-data restriction.

'''+a
if s.count(a)!=1:raise RuntimeError('Adaptive insertion anchor mismatch')
files['adaptive-testing.tex']=s.replace(a,b)
s=(O/'optional-stability.tex').read_text();a=r'\begin{theorem}[Collision-observation optional-projection limit]';b=r'\begin{theorem}[Fixed-flow observation-approximation limit]'
if s.count(a)!=1:raise RuntimeError('Optional source anchor mismatch')
files['optional-stability.tex']=s.replace(a,b)
old={**json.loads((O/'INHERITED_INPUTS.json').read_text())['files'],**json.loads((O/'SOURCE_MANIFEST.json').read_text())['files']}
old[str((O/'SOURCE_MANIFEST.json').relative_to(ROOT))]=hashlib.sha256((O/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()
files['INHERITED_SOURCES.json']=json.dumps({'source_commit':'f93ab1a6c8c5255a3398f1884c5af05d65ced73a','files':dict(sorted(old.items()))},indent=2)+'\n'
manifest=json.loads(files['SOURCE_MANIFEST.json'])['files']
for rel,h in manifest.items():
 path=Path(rel)
 if path.parent!=P.relative_to(ROOT):raise RuntimeError('Manifest escaped revision directory')
 if hashlib.sha256(files[path.name].encode()).hexdigest()!=h:raise RuntimeError('Plaintext digest mismatch '+path.name)
if set(files)!={Path(x).name for x in manifest}|{'SOURCE_MANIFEST.json'}:raise RuntimeError('Payload/manifest mismatch')
if '--check-only' not in sys.argv:
 for name,data in files.items(): (P/name).write_text(data)
print(json.dumps({'materialized_files':len(files),'manifest_inputs':len(manifest),'inherited_source_count':len(old),'payload_sha256':EXPECTED,'scope':'byte identity only; not mathematical certification'},indent=2))
