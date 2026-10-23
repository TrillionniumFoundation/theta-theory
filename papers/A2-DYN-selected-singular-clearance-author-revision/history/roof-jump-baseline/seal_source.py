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
             and p.relative_to(ROOT).as_posix() not in EXCLUDED and '__pycache__' not in p.parts]
    records = [identity(p) for p in sorted(files)]
    native = [r for r in records if r['path'].endswith('.tex')
              and not r['path'].startswith('history/')]
    payload = ''.join(r['path']+'\0'+r['sha256']+'\n' for r in native).encode()
    manifest = {
        'schema': 2,
        'repository': 'TrillionniumFoundation/theta-theory',
        'base_commit': 'd6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28',
        'base_repository_tree': '5ec7da36366d703d9e59a68245e90912639d18a0',
        'base_article_tree': '381d0aa576a93d874bf974b0edcf090378aaa41b',
        'continued_mathematical_commit': '85f206907f56773e32fae9b61302924ca16603aa',
        'continued_mathematical_article_tree': 'e4ddb6fd11e570dfc7bba9d5fd5a2fed051e78c7',
        'continued_mathematical_source_sha256': 'a1b162cec833de28f138c2ba1e353b39be9a6d1d21a4398480afa8c7b38f9bd2',
        'controlling_report_commit': 'f01482035a0b945b50f1f9c30f30ef35077558dc',
        'controlling_report_blob': '9c68b0e8b31cd196c732514a29ebd44d95964243',
        'mathematical_source_sha256': hashlib.sha256(payload).hexdigest(),
        'mathematical_source_hash_algorithm': 'SHA256 of sorted active .tex path, NUL, content SHA256, LF; history excluded',
        'active_native_files': len(native),
        'exclusions': ['build/**', 'evidence/**', *sorted(EXCLUDED), '**/__pycache__/**'],
        'exclusion_reason': 'Manifest cannot hash itself; publication receipts and execution products are independently hashed by their records. The committed source SHA is pinned by a later receipt, never invented self-referentially.',
        'files': records,
    }
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'sealed','files':len(records),'active_native_files':len(native),
                      'mathematical_source_sha256':manifest['mathematical_source_sha256']}))

if __name__ == '__main__': main()
