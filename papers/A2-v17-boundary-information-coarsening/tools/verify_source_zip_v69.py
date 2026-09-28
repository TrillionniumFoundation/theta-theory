#!/usr/bin/env python3
"""Check source bytes, Git blobs and raw Unix ZIP modes; optionally extract.

Extraction is only into a new directory and restores manifest modes explicitly.
Hashes establish object consistency, not authenticity or mathematical truth.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import os
import zipfile


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def verify(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP members')
        require('SOURCE_MANIFEST.json' in names, 'Missing source manifest')
        manifest = json.loads(archive.read('SOURCE_MANIFEST.json'))
        files = manifest['files']
        require(set(names) == {'SOURCE_MANIFEST.json'} | {'source/' + p for p in files},
                'Unexpected or missing archive member')
        errors = []
        executable = []
        for name in names:
            parts = PurePosixPath(name)
            require(not parts.is_absolute() and '..' not in parts.parts and '\\' not in name,
                    'Unsafe archive path: ' + name)
            info = archive.getinfo(name)
            data = archive.read(name)
            mode = 0o100644
            if name != 'SOURCE_MANIFEST.json':
                record = files[name[len('source/'):]]
                mode = int(record['mode'], 8)
                require(mode in (0o100644, 0o100755), 'Unsupported Git mode: ' + name)
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                require(len(data) == record['bytes'] and
                        hashlib.sha256(data).hexdigest() == record['sha256'] and
                        blob == record['git_blob'], 'Source byte identity failed: ' + name)
                if mode == 0o100755:
                    executable.append(name[len('source/'):])
            raw = (info.external_attr >> 16) & 0xffff
            if info.create_system != 3 or raw != mode:
                errors.append({'path': name, 'expected': format(mode, '06o'),
                               'raw': format(raw, '06o'), 'system': info.create_system})
        require(not errors, 'ZIP mode discrepancies: ' + json.dumps(errors, sort_keys=True))
        return {'status': 'passed', 'files': len(files),
                'executable_paths': sorted(executable),
                'raw_zip_modes': 'all match recorded Git modes',
                'archive_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def extract(path: Path, destination: Path) -> None:
    verify(path)
    require(not destination.exists(), 'Extraction destination must not exist')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            target = destination.joinpath(*PurePosixPath(info.filename).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(archive.read(info))
            os.chmod(target, (info.external_attr >> 16) & 0o777)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--extract', type=Path)
    args = parser.parse_args()
    result = verify(args.archive)
    if args.extract is not None:
        extract(args.archive, args.extract)
        result['extraction'] = 'completed with explicit manifest-equivalent modes'
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
