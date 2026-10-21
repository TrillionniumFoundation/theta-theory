#!/usr/bin/env python3
"""Record actual local receiving/restoration and seal the publication inventory."""
from pathlib import Path
import hashlib
import json
import shutil

BASE = Path('/workspace/scratch/f856e3d63ac5')
DELIVERY = BASE / 'r76-delivery'
PUB = BASE / 'theta-r76-work/papers/General-Theta-Foundations-I-restart/r76-robust-memory-realization-publication'
SHA = '891643799f2dfb2737ad5c147bf8def2d460630b'
TREE = '38930b53fb64ca4ca1ebcc7e20919f2ed0ba74ae'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

old_manifest = PUB / 'DELIVERY_MANIFEST.json'
manifest = json.loads(old_manifest.read_text())
evidence = PUB / 'evidence/local-receiving'
if evidence.exists():
    raise RuntimeError('Finalization already started; inspect rather than overwrite evidence.')
evidence.mkdir()
shutil.copy2(old_manifest, evidence / 'ASSEMBLY_MANIFEST_CHECKED.json')
receipt_names = [
    'LOCAL_RECEIVER_CHECK_01.json', 'LOCAL_RECEIVER_CHECK_01.stderr',
    'LOCAL_ARCHIVE_RESTORE_01.json', 'LOCAL_ARCHIVE_RESTORE_01.stderr',
    'PUBLICATION_ASSEMBLY_RECEIPT.json',
]
for name in receipt_names:
    src = DELIVERY / name
    if name.endswith('.stderr'):
        if src.read_bytes():
            raise RuntimeError('Nonempty receiving stderr: ' + name)
    elif name != 'PUBLICATION_ASSEMBLY_RECEIPT.json':
        record = json.loads(src.read_text())
        if record['status'] != 'PASS' or record['source_commit'] != SHA or record['source_paper_tree'] != TREE:
            raise RuntimeError('Wrong or unsuccessful receipt: ' + name)
    shutil.copy2(src, evidence / name)

path = PUB / 'START_HERE.md'
value = path.read_text()
for number in (34, 181, 37):
    value = value.replace(f'{number}pages', f'{number} pages')
path.write_text(value)
path = PUB / 'evidence/EXECUTION_NOTES.md'
value = path.read_text().replace('all1,300', 'all 1,300')
value = value.replace('without changing theorem numbers/pages.',
    'without changing the indexed theorem numbers or their pages; removal of the orphan bibliography page shortened the main article from 35 to 34 pages.')
path.write_text(value)
path = PUB / 'VISUAL_QA_RECEIPT.json'
visual = json.loads(path.read_text())
visual['coverage'] = ('All 252 current pages at overview scale; 39 enlarged page inspections across the main, '
    'supplement and companion. See individual logs for exact coverage and inherited-pixel comparison.')
write_json(path, visual)
shutil.copy2(Path(__file__), PUB / 'evidence/finalize_publication.py')
write_json(evidence / 'RECEIVING_SCOPE.json', {
    'schema': 'theta.r76.local-publication-receiving.v1',
    'source_commit': SHA,
    'source_paper_tree': TREE,
    'manifest_actually_checked_sha256': digest(evidence / 'ASSEMBLY_MANIFEST_CHECKED.json'),
    'complete_receiver_status': 'PASS',
    'complete_archives_actually_reconstructed': 3,
    'archive_restore_status': 'PASS',
    'later_changes': ['Entry-document spacing and exact layout explanation.',
        'Visual coverage prose spacing.', 'Addition of original receiving/restoration/assembly evidence and this finalization script.'],
    'unchanged_payloads': ['All 507 sealed source files.', 'All three complete archive byte streams and their 31 parts.',
        'All three final PDFs and extracted texts.', 'Actual strict build receipt and native theorem index.'],
    'scope': 'These receipts bind the saved assembly manifest. A final receiving check and a post-push fresh download are separate actual executions, never self-attested here.'
})
manifest['files'] = []
for path in sorted(PUB.rglob('*')):
    if not path.is_file() or '__pycache__' in path.parts or path == old_manifest:
        continue
    if path.is_symlink():
        raise RuntimeError('Symlink in publication: ' + str(path))
    manifest['files'].append({'path': path.relative_to(PUB).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest(path)})
write_json(old_manifest, manifest)
print(json.dumps({'publication_files': len(manifest['files']) + 1,
    'delivery_manifest_sha256': digest(old_manifest), 'source_commit': SHA,
    'source_paper_tree': TREE, 'publication_bytes': sum(x['bytes'] for x in manifest['files']) + old_manifest.stat().st_size}, indent=2))
