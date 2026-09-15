#!/usr/bin/env python3
"""Read-only artifact/source/build checks for the A2 v52 review.
Layout: ROOT/native (workflow ZIP extracted), ROOT/source (native-source.zip
extracted), ROOT/rebuild (complete independent LaTeX build), ROOT/report.
Requires Python 3 and PyMuPDF. Does not build or execute author sources.
Usage: python verify_snapshot.py ROOT WORKFLOW_ARTIFACT.zip
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import fitz


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git_object(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def check_file(path, info):
    raw = path.read_bytes()
    require(len(raw) == info['bytes'], 'Size mismatch: ' + str(path))
    require(digest(raw) == info['sha256'], 'SHA-256 mismatch: ' + str(path))
    if 'git_blob' in info:
        require(git_object('blob', raw) == info['git_blob'], 'Git blob mismatch: ' + str(path))


def tree_sha(entries):
    chunks = []
    for name in sorted(entries, key=lambda n: (n + ('/' if isinstance(entries[n], dict) else '')).encode()):
        value = entries[name]
        if isinstance(value, dict):
            mode, sha = '40000', tree_sha(value)
        else:
            mode, sha = value
        chunks.append(mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(sha))
    return git_object('tree', b''.join(chunks))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('artifact', type=Path)
    args = ap.parse_args()
    root, native, source = args.root, args.root/'native', args.root/'source'/'source'
    artifact_hash = digest(args.artifact.read_bytes())
    require(artifact_hash == 'cfb7b4c2b5cf1cb4f32f06111a6ff3a9ea597c0621f1a95a189f0809bc9735e9', 'Artifact digest mismatch')
    manifest = json.loads((root/'source'/'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_commit'] == '9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6', 'Wrong source commit')
    require(not manifest['excluded_tracked_products'], 'Unexpected excluded entries')
    tree = {}
    for name, info in manifest['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe manifest path')
        check_file(source/name, info)
        node = tree
        parts = name.split('/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (info['mode'], info['git_blob'])
    reconstructed = tree_sha(tree)
    require(reconstructed == manifest['source_tree'] == 'ba34d61e1eda687d1257be33d1cbae9758127d94', 'Source tree mismatch')
    active = json.loads((native/'active-source-manifest.json').read_text())
    active_union = {name: info for group in active.values() for name, info in group.items()}
    for name, info in active_union.items():
        check_file(source/name, info)
        check_file(root/'rebuild'/name, info)
    build = json.loads((native/'build-report.json').read_text())
    require(digest((native/'native-source.zip').read_bytes()) == build['source_archive_sha256'], 'Source ZIP mismatch')
    for name, info in build['evidence_files'].items():
        check_file(native/name, info)
    pdfs = {}
    for entry in ('main', 'two_collision'):
        left, right = native/(entry+'.pdf'), root/'rebuild'/(entry+'.pdf')
        a, b = fitz.open(left), fitz.open(right)
        require(len(a) == len(b), 'Page count mismatch: ' + entry)
        text_diff, pixel_diff = [], []
        for i in range(len(a)):
            if a[i].get_text() != b[i].get_text():
                text_diff.append(i+1)
            pa = a[i].get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csRGB, alpha=False)
            pb = b[i].get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csRGB, alpha=False)
            if (pa.width, pa.height, pa.samples) != (pb.width, pb.height, pb.samples):
                pixel_diff.append(i+1)
        log = (root/'rebuild'/(entry+'.log')).read_text(errors='replace')
        warnings = [line for line in log.splitlines() if re.search(r'Underfull|Overfull|undefined|Rerun to get', line)]
        pdfs[entry] = dict(pages=len(a), native_sha256=digest(left.read_bytes()),
            rebuild_sha256=digest(right.read_bytes()), text_different_pages=text_diff,
            rgb_72dpi_different_pages=pixel_diff, final_log_warnings=warnings)
        require(not text_diff and not pixel_diff, 'PDF content mismatch: ' + entry)
        a.close(); b.close()
    out = dict(status='passed', mathematical_certification=False,
        review_ready_commit='95046e3b4fce025e5763b555c38180339d4869a0',
        actual_compiled_source=manifest['source_commit'], artifact_sha256=artifact_hash,
        source_archive_sha256=build['source_archive_sha256'],
        reconstructed_source_tree=reconstructed, verified_source_files=len(manifest['files']),
        verified_active_inputs=len(active_union), verified_native_evidence_files=len(build['evidence_files']),
        pdfs=pdfs, renderer=fitz.VersionBind,
        author_check_rerun_matches_native=(root/'report/AUTHOR_CHECKS_RERUN.json').read_bytes()==(native/'check_revision_v52-normal.json').read_bytes(),
        author_check_optimized_identical=(root/'report/AUTHOR_CHECKS_RERUN.json').read_bytes()==(root/'report/AUTHOR_CHECKS_OPTIMIZED.json').read_bytes(),
        independent_check_optimized_identical=(root/'report/INDEPENDENT_CHECKS.json').read_bytes()==(root/'report/INDEPENDENT_CHECKS_OPTIMIZED.json').read_bytes())
    for key in ('author_check_rerun_matches_native', 'author_check_optimized_identical', 'independent_check_optimized_identical'):
        require(out[key], 'Diagnostic output mismatch: ' + key)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
