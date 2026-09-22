#!/usr/bin/env python3
"""Materialize the reviewed A2 v121 source overlay without touching v120."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, lzma, shutil

ROOT = Path(__file__).resolve().parents[2]
BOOT = Path(__file__).resolve().parent
REL = Path('papers/A2-v17-boundary-information-coarsening/article')
OLD, NEW = ROOT / REL / 'v120', ROOT / REL / 'v121'
EXPECTED = '483532a05e00ff8337b31a425d66f95fda6ae4973ecf81e0858431b0cde6fa95'
raw = base64.b64decode(''.join((BOOT / f'overlay-{i}.b64').read_text().strip() for i in range(5)), validate=True)
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise RuntimeError('Source-overlay checksum mismatch')
payload = lzma.decompress(raw)
if len(payload) > 2_000_000:
    raise RuntimeError('Unexpected source-overlay size')
overlay = json.loads(payload)
if len(overlay) != 19 or not OLD.is_dir():
    raise RuntimeError('Unexpected overlay or missing immutable v120 base')
for name, text in overlay.items():
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not isinstance(text, str):
        raise ValueError('Unsafe source path')
if NEW.exists():
    raise RuntimeError('v121 already exists; refusing to replace a revision')
shutil.copytree(OLD, NEW)
# Remove only copied active products and receipts; never alter the v120 archive.
for name in ('evidence', 'crossrefs'):
    p = NEW / name
    if p.exists():
        shutil.rmtree(p)
for p in NEW.iterdir():
    if p.is_file() and p.suffix in ('.pdf', '.log', '.aux', '.out', '.toc', '.fls', '.fdb_latexmk'):
        p.unlink()
for p in list(NEW.rglob('__pycache__')):
    shutil.rmtree(p)
for name, text in overlay.items():
    p = NEW / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
(ROOT / 'A2_REVISION_V121_INDEX.md').write_text('''# A2 revision 121 — referee reading index

**Title:** Determinantal flags and primary boundaries in multiplication failure.

**Revision branch:** `revision/a2-v121-determinantal-flags-elliptic-boundary-2026-09-22`.

**Controlling review:** `review/a2-v120-independent-harsh-top4-2026-09-22`, commit `b20eafa006fd3abe650ad7478542d637327b1094`.

All revision files are in `papers/A2-v17-boundary-information-coarsening/article/v121/`.

- Main journal manuscript: [geometry.pdf](papers/A2-v17-boundary-information-coarsening/article/v121/geometry.pdf), source `geometry.tex`.
- Complete preserved companion: [paper.pdf](papers/A2-v17-boundary-information-coarsening/article/v121/paper.pdf), source `paper.tex`.
- Applications edition: [applications.pdf](papers/A2-v17-boundary-information-coarsening/article/v121/applications.pdf).
- [Point-by-point reply to E120.1–E120.7](papers/A2-v17-boundary-information-coarsening/article/v121/RESPONSE_TO_R120.md).
- [Literature audit](papers/A2-v17-boundary-information-coarsening/article/v121/LITERATURE_AUDIT.md) and [dependency map](papers/A2-v17-boundary-information-coarsening/article/v121/DEPENDENCY_MAP.md).
- Source/product hashes and page counts: `evidence/BUILD_RECEIPT.json`; exact regressions: `evidence/DIAGNOSTICS.json`; preservation: `evidence/PRESERVATION.json`.

The universal corank-one theorem has explicit hypotheses. The non-isotrivial (1,3,3) family has a separate local-ring proof. No theorem claims arbitrary-specialization compatibility of embedded primary components. Every old mathematical section and theorem label is retained.

**Uncompleted documentary item:** E120.1, the theorem-level comparison with the complete Ballico 1993 article. Metadata and citations are not a substitute for reading its full text. No priority or journal-acceptance certification is claimed.

PDF links become available with the separate successful product commit; the source commit precedes the build. The original review and v120 files are unchanged.
''', encoding='utf-8')
print(f'Materialized {len(overlay)} verified source changes over the immutable v120 base.')
