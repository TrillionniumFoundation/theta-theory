"""Create immutable Git objects for the checksum-bound v17 source; never refs."""
from pathlib import Path, PurePosixPath
import base64
import hashlib
import json
import lzma
import os
import shutil
import tempfile
import urllib.request

EXPECTED = '0af99c96122be5032f1818feac344676ff31c705'
PACKET_SHA = '428e9f8029f2b46f1ee9275c2276bf5e498c68664cb4a0cdd7a1ff195d9eed31'
REPO = 'TrillionniumFoundation/theta-theory'
HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
BASE = ROOT / 'papers/A2-DYN-v16-referee-response'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


encoded = ''.join((HERE / ('part%d.b64' % j)).read_text().strip() for j in range(1, 6))
raw = lzma.decompress(base64.b64decode(encoded, validate=True))
require(hashlib.sha256(raw).hexdigest() == PACKET_SHA, 'transport checksum mismatch')
packet = json.loads(raw)
require(packet['expected_tree'] == EXPECTED, 'unexpected paper tree')
with tempfile.TemporaryDirectory(prefix='a2-dyn-v17-') as tmp:
    target = Path(tmp) / 'paper'
    shutil.copytree(BASE, target, ignore=shutil.ignore_patterns('build', 'evidence', '__pycache__'))
    entries = list(packet['tree'])
    for item in entries:
        rel = PurePosixPath(item['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe packet path')
        require(item['type'] == 'blob' and item['mode'] in ('100644', '100755'), 'bad entry')
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(item['content'].encode('utf-8'))
        dest.chmod(0o755 if item['mode'] == '100755' else 0o644)
    edits = json.loads((target / 'INHERITED_EDITS.json').read_text())['edits']
    require(len(edits) == 6, 'unexpected inherited edit count')
    main = (BASE / 'main.tex').read_text()
    for edit in edits:
        require(edit['path'] == 'main.tex' and main.count(edit['before']) == 1,
                'inherited edit is not exact')
        main = main.replace(edit['before'], edit['after'], 1)
    (target / 'main.tex').write_text(main)
    (target / 'build.sh').write_text((BASE / 'build.sh').read_text().replace('v16', 'v17'))
    (target / 'build.sh').chmod(0o755)
    receipt = (BASE / 'tools/receipt_v16.py').read_text()
    receipt = receipt.replace("'revision':16", "'revision':17").replace('v16-source', 'v17-source')
    (target / 'tools/receipt_v17.py').write_text(receipt)
    manifest = packet['manifest_metadata']
    old = sorted((BASE / 'core').glob('*.tex')) + [BASE / 'main.tex', BASE / 'references.tex']
    manifest['baseline_sha256'] = {p.relative_to(BASE).as_posix(): sha(p) for p in old}
    sources = sorted(p for p in target.rglob('*') if p.is_file()
                     and p.name != 'SOURCE_MANIFEST.json'
                     and not any(x in ('build', 'evidence', '__pycache__') for x in p.parts))
    manifest['source_sha256'] = {p.relative_to(target).as_posix(): sha(p) for p in sources}
    (target / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    for rel, expected in packet['generated_files_sha256'].items():
        require(sha(target / rel) == expected, 'regenerated file differs: ' + rel)
        entries.append({'path': rel, 'mode': '100755' if rel == 'build.sh' else '100644',
                        'type': 'blob', 'content': (target / rel).read_text()})
    for p in (BASE / 'core').glob('*.tex'):
        require(p.read_bytes() == (target / 'core' / p.name).read_bytes(), 'changed inherited core')
    for p in (BASE / 'tools').glob('*.py'):
        require(p.read_bytes() == (target / 'tools' / p.name).read_bytes(), 'changed inherited Python')
    require(len(entries) == len({e['path'] for e in entries}), 'duplicate tree entry')
    if os.environ.get('ASSEMBLY_DRY_RUN') == '1':
        result = {'sha': EXPECTED, 'dry_run': True}
    else:
        require(os.environ.get('GITHUB_REPOSITORY') == REPO, 'unexpected repository')
        payload = json.dumps({'base_tree': packet['base_tree'], 'tree': entries}).encode()
        request = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/trees',
            data=payload, method='POST', headers={
                'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json', 'User-Agent': 'A2-DYN-exact-source'})
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.load(response)
        require(result['sha'] == EXPECTED, 'created Git tree differs from validated source')
    out = {'event_sha': os.environ.get('GITHUB_SHA'), 'paper_tree': result['sha'],
           'packet_sha256': PACKET_SHA, 'tree_entries': len(entries),
           'ordinary_source_files': len(sources) + 1,
           'generated_files_sha256': packet['generated_files_sha256'],
           'run_id': os.environ.get('GITHUB_RUN_ID'),
           'created_commits': False, 'changed_refs': False,
           'dry_run': bool(result.get('dry_run'))}
    (HERE / 'assembly-receipt.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
