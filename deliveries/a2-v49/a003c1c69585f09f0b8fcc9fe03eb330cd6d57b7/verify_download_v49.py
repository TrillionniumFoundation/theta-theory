#!/usr/bin/env python3
"""Check v49 native evidence, archived sources, and optional all-page local parity.

Uses PyMuPDF for PDF comparisons. Does not perform visual review or certify
mathematics. No network access, no repository writes, no executable TeX input.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import fitz

SOURCE = 'a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7'
ARTIFACT_SHA256 = 'c136941451a73a04380692edfc569f510e0de5dd85ec82664f58f3758ddd3390'


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def safe_name(name: str) -> None:
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,
            'Unsafe relative path: ' + name)


def regular(root: Path, name: str) -> Path:
    safe_name(name)
    p = root/name
    require(p.is_file() and not p.is_symlink(), 'Not a regular file: ' + name)
    return p


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def check_bytes(data: bytes, info: dict, name: str) -> None:
    require(len(data) == info['bytes'] and sha(data) == info['sha256'],
            'Size or SHA-256 mismatch: ' + name)
    if 'git_blob' in info:
        require(blob(data) == info['git_blob'], 'Git blob mismatch: ' + name)


def verify(root: Path, local: Path | None, artifact: Path | None) -> dict:
    report = json.loads(regular(root, 'build-report.json').read_text())
    require(report['status'] == 'passed' and report['source_commit'] == SOURCE,
            'Unexpected or failed source build')
    for name, info in report['evidence_files'].items():
        check_bytes(regular(root, name).read_bytes(), info, name)
    frozen = json.loads(regular(root, 'frozen-source-manifest.json').read_text())
    require(frozen['source_commit'] == SOURCE and frozen['source_tree'] == report['source_tree'],
            'Frozen source identity mismatch')
    manifest = json.loads(regular(root, 'active-source-manifest.json').read_text())
    active = {name: info for group in manifest.values() for name, info in group.items()}
    require(len(active) == 106, 'Unexpected active-source count')
    with zipfile.ZipFile(regular(root, 'native-source.zip')) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'Duplicate archive names')
        for name in names:
            safe_name(name)
        for name, info in frozen['files'].items():
            check_bytes(z.read('source/'+name), info, name)
        for name, info in active.items():
            data = z.read('source/'+name)
            check_bytes(data, info, name)
            if local is not None:
                require(data == regular(local, name).read_bytes(),
                        'Local compiled input differs: ' + name)
    modes = []
    for p in sorted(root.glob('check_*-normal.json')):
        optimized = regular(root, p.name.replace('-normal', '-optimized'))
        require(p.read_bytes() == optimized.read_bytes(), 'Python-mode mismatch: ' + p.name)
        modes.append(p.stem.removesuffix('-normal'))
    require(len(modes) == 5, 'Expected five dual-mode diagnostic families')
    out = {'source_commit': SOURCE, 'source_tree': report['source_tree'],
           'evidence_entries_verified': len(report['evidence_files']),
           'frozen_source_files_verified': len(frozen['files']),
           'active_source_files_verified': len(active), 'ordinary_optimized_parity': modes,
           'local_compilation_compared': local is not None, 'entries': {},
           'mathematical_certification': False, 'visual_review': 'Not performed by this script'}
    if artifact is not None:
        data = artifact.read_bytes()
        require(sha(data) == ARTIFACT_SHA256, 'Actions artifact ZIP digest mismatch')
        out['actions_zip'] = {'bytes': len(data), 'sha256': sha(data), 'matches_github_digest': True}
    for stem in ('main', 'two_collision'):
        file = regular(root, stem+'.pdf')
        data = file.read_bytes()
        check_bytes(data, report['entries'][stem]['product'], stem+'.pdf')
        with fitz.open(file) as native:
            require(len(native) == report['entries'][stem]['product']['pages'], 'Page-count mismatch')
            outside = set()
            for i, page in enumerate(native, 1):
                for b in page.get_text('dict')['blocks']:
                    if b['type'] != 0:
                        continue
                    for line in b['lines']:
                        for span in line['spans']:
                            if not page.rect.contains(fitz.Rect(span['bbox'])):
                                outside.add(i)
            item = {'pages': len(native), 'bytes': len(data), 'sha256': sha(data),
                    'git_blob': blob(data), 'outside_page_text_spans_on_pages': sorted(outside),
                    'native_build_warnings': report['entries'][stem]['warnings']}
            if local is not None:
                otherfile = regular(local, stem+'.pdf')
                with fitz.open(otherfile) as other:
                    require(len(native) == len(other), 'Local page-count mismatch')
                    for i, (a, b) in enumerate(zip(native, other), 1):
                        require(a.get_text() == b.get_text(), f'{stem} text differs, page {i}')
                        x = a.get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
                        y = b.get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
                        require((x.width,x.height,x.samples) == (y.width,y.height,y.samples),
                                f'{stem} raster differs, page {i}')
                    item['same_renderer_text_and_72dpi_pixel_parity_pages'] = len(native)
                item['local_pdf_byte_identical'] = data == otherfile.read_bytes()
            out['entries'][stem] = item
    out['status'] = 'passed'
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--local-build', type=Path)
    p.add_argument('--artifact-zip', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    text = json.dumps(verify(args.native,args.local_build,args.artifact_zip),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')

if __name__ == '__main__':
    main()
