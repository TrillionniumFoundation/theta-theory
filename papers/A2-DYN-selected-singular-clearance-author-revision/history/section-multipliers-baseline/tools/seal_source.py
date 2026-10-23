#!/usr/bin/env python3
"""Write the auditable content manifest; run deliberately after source edits."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'SOURCE_MANIFEST.json', 'PUBLICATION_STATUS.json', 'VALIDATION_REPORT.md'}

def identity(path):
    content = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(content),
            'sha256': hashlib.sha256(content).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()}

def main():
    files = [p for p in ROOT.rglob('*') if p.is_file()
             and p.relative_to(ROOT).parts[0] not in {'build', 'evidence'}
             and p.name not in EXCLUDED and '__pycache__' not in p.parts]
    records = [identity(p) for p in sorted(files)]
    native = [r for r in records if r['path'].endswith('.tex')
              and not r['path'].startswith('history/')]
    payload = ''.join(r['path']+'\0'+r['sha256']+'\n' for r in native).encode()
    manifest = {
        'schema': 1,
        'repository': 'TrillionniumFoundation/theta-theory',
        'base_commit': 'e84c06c758bed5b2dc09222ad725cfe0ba0d58dd',
        'base_repository_tree': 'aec187ca1447ee525ce0c6906a54082688acfe94',
        'base_article_tree': '7d1a65637fd0178727d574494bf2963172aa9881',
        'continued_mathematical_commit': '9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761',
        'continued_mathematical_article_tree': '1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc',
        'controlling_report_commit': 'f01482035a0b945b50f1f9c30f30ef35077558dc',
        'controlling_report_blob': '9c68b0e8b31cd196c732514a29ebd44d95964243',
        'mathematical_source_sha256': hashlib.sha256(payload).hexdigest(),
        'mathematical_source_hash_algorithm': 'SHA256 of sorted active .tex path, NUL, content SHA256, LF; history excluded',
        'active_native_files': len(native),
        'exclusions': ['build/**', 'evidence/**', *sorted(EXCLUDED), '**/__pycache__/**'],
        'exclusion_reason': 'Manifest cannot hash itself; publication receipts and execution products are independently hashed by their records.',
        'files': records,
    }
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'sealed','files':len(records),'active_native_files':len(native),
                      'mathematical_source_sha256':manifest['mathematical_source_sha256']}))

if __name__ == '__main__': main()
