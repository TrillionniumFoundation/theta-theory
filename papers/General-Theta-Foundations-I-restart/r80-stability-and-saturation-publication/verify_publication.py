from pathlib import Path
import hashlib
import json
import tarfile

root = Path(__file__).resolve().parent
receipt = json.loads((root / 'PUBLICATION_RECEIPT.json').read_text())
def require(value, message):
    if not value:
        raise RuntimeError(message)
def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
files = receipt['artifacts']
expected = {x['path'] for x in files}
actual = {x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and '__pycache__' not in x.parts and x.name != 'PUBLICATION_RECEIPT.json'}
require(actual == expected, 'Publication file inventory differs')
for item in files:
    require(identity((root / item['path']).read_bytes()) == {k: item[k] for k in ('bytes', 'sha256')}, 'File identity mismatch: ' + item['path'])
build = json.loads((root / 'BUILD_RECEIPT.json').read_text())
require(build['status'] == 'PASS' and build['source_commit_verified'], 'No strict source identity PASS')
require(build['declared_source_commit'] == receipt['source']['commit'], 'Source identity disagreement')
require(build['total_checks'] == build['exact_finite_checks'] + build['floating_finite_checks'], 'Diagnostic totals inconsistent')
require(build['ordinary_optimized_identity'] and build['source_unchanged_during_build'], 'Strict invariants absent')
for doc in build['documents']:
    require(identity((root / doc['file']).read_bytes()) == {k: doc[k] for k in ('bytes', 'sha256')}, 'PDF identity mismatch')
contents = json.loads((root / 'VALIDATION_CONTENTS.json').read_text())
archive = root / contents['archive']['file']
require(identity(archive.read_bytes()) == {k: contents['archive'][k] for k in ('bytes', 'sha256')}, 'Archive identity mismatch')
members = {x['path']: x for x in contents['files']}
require(len(members) == len(contents['files']), 'Duplicate manifest entry')
seen = set()
with tarfile.open(archive, 'r:gz') as tar:
    for member in tar:
        require(member.isfile() and not member.name.startswith('/') and '..' not in Path(member.name).parts, 'Unsafe or non-regular archive member')
        require(member.name not in seen and member.name in members, 'Duplicate or unlisted archive member')
        seen.add(member.name)
        data = tar.extractfile(member).read()
        require(identity(data) == {k: members[member.name][k] for k in ('bytes', 'sha256')}, 'Archived file mismatch: ' + member.name)
require(seen == set(members), 'Missing archive member')
print(json.dumps({'status': 'FILE_INTEGRITY_PASS', 'source_commit': receipt['source']['commit'], 'publication_files_checked': len(files), 'archive_files_checked': len(seen), 'scope': 'Cryptographic file integrity and receipt consistency only; no theorem proof, new build, hosted CI, human assessment or editorial decision.'}, indent=2, sort_keys=True))
