#!/usr/bin/env python3
"""Verify the downloaded A2 v68 native delivery against the separately built source.

Usage: python verify_download.py ARTIFACT_ZIP LOCAL_BUILD_DIRECTORY OUTPUT_JSON
Requires PyMuPDF. This is a byte/input/PDF parity check, not a proof certificate.
The expected native identities are pinned to the completed GitHub run.
"""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile
import fitz

SOURCE = 'de0deffc2ca7b0fd2f0d2d5ad5fbdff1eee0f0a6'
TREE = '23f07201ea4c6a33270cf4d4a977da1eddf8e8fe'
ARTIFACT = 'd4544c5f2b523877bb660835d1162afed4ccccfb9cd6066548b53934c08bc5c6'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def git_tree(records: dict) -> str:
    root = {}
    for name, item in records.items():
        node = root
        parts = name.split('/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (item['mode'], item['git_blob'])
    def calculate(node):
        out = []
        for name, item in node.items():
            if isinstance(item, dict):
                mode, oid, key = '40000', calculate(item), name + '/'
            else:
                mode, oid = item
                key = name
            out.append((key.encode(), mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(oid)))
        data = b''.join(value for _, value in sorted(out))
        return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    return calculate(root)


def main() -> None:
    require(len(sys.argv) == 4, __doc__ or 'Invalid arguments')
    artifact, local, output = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    archive_bytes = artifact.read_bytes()
    require(sha(archive_bytes) == ARTIFACT, 'Wrong workflow artifact digest')
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    require(len(archive.namelist()) == len(set(archive.namelist())), 'Duplicate artifact paths')
    report = json.loads(archive.read('build-report.json'))
    require(report['status'] == 'passed' and not report['errors'], 'Native build did not pass')
    require(report['source_commit'] == SOURCE and report['source_tree'] == TREE, 'Wrong compiled source')
    for name, rec in report['evidence_files'].items():
        data = archive.read(name)
        require(len(data) == rec['bytes'] and sha(data) == rec['sha256'], 'Evidence mismatch: ' + name)
    frozen = json.loads(archive.read('frozen-source-manifest.json'))
    source_zip_bytes = archive.read('native-source.zip')
    require(sha(source_zip_bytes) == report['source_archive_sha256'], 'Source ZIP mismatch')
    source_zip = zipfile.ZipFile(io.BytesIO(source_zip_bytes))
    require(source_zip.read('SOURCE_MANIFEST.json') == archive.read('frozen-source-manifest.json'), 'Embedded manifest mismatch')
    files = frozen['files']
    require(len(files) == 876 and not frozen['excluded_tracked_products'], 'Unexpected complete source inventory')
    local_manifest = json.loads((local / 'frozen-source-manifest.json').read_text())
    require(files == local_manifest['files'], 'Remote and intended local source records differ')
    local_zip = zipfile.ZipFile(local / 'native-source.zip')
    require(set(source_zip.namelist()) == {'SOURCE_MANIFEST.json'} | {'source/' + name for name in files}, 'Unexpected source archive entries')
    for name, rec in files.items():
        data = source_zip.read('source/' + name)
        require(len(data) == rec['bytes'] and sha(data) == rec['sha256'] and git_blob(data) == rec['git_blob'], 'Source mismatch: ' + name)
        require(rec['mode'] in ('100644', '100755'), 'Unsupported recorded Git mode')
        require(data == local_zip.read('source/' + name), 'Local source byte mismatch: ' + name)
    computed_tree = git_tree(files)
    require(computed_tree == TREE, 'Reconstructed manuscript tree differs')
    baseline = json.loads(source_zip.read('source/history/v67-review-baseline/SOURCE_MANIFEST.json'))['files']
    unchanged, edited = [], []
    for name, rec in baseline.items():
        require(name in files and files[name]['mode'] == rec['mode'], 'Removed inherited path or changed Git mode: ' + name)
        data = source_zip.read('source/' + name)
        if sha(data) == rec['sha256']:
            unchanged.append(name)
        else:
            old = source_zip.read('source/history/v67-review-baseline/' + name)
            require(len(old) == rec['bytes'] and sha(old) == rec['sha256'] and git_blob(old) == rec['git_blob'], 'Archived original mismatch: ' + name)
            edited.append(name)
    require(len(baseline) == 855 and len(unchanged) == 846 and len(edited) == 9, 'Unexpected preservation inventory')
    active = json.loads(archive.read('active-source-manifest.json'))
    union = set()
    for entry, records in active.items():
        for name, rec in records.items():
            require(name in files and rec == files[name], 'Active input mismatch: ' + name)
            union.add(name)
    require(len(union) == 135 and {k: len(v) for k,v in active.items()} == {'main':124,'rigidity':56,'two_collision':1}, 'Unexpected input graph')
    normal_outputs = [n for n in archive.namelist() if n.endswith('-normal.json')]
    for name in normal_outputs:
        require(archive.read(name) == archive.read(name.replace('-normal.json','-optimized.json')), 'Normal/-O mismatch: ' + name)
        require(archive.read(name) == (local / name).read_bytes(), 'Diagnostic/local mismatch: ' + name)
    entries = {}
    for stem in ('main','rigidity','two_collision'):
        raw = archive.read(stem + '.pdf')
        native = fitz.open(stream=raw, filetype='pdf')
        comparison = fitz.open(local / (stem + '.pdf'))
        product = report['entries'][stem]['product']
        require(len(native) == len(comparison) == product['pages'] and sha(raw) == product['sha256'], 'PDF manifest mismatch: ' + stem)
        text_mismatch, pixel_mismatch = [], []
        for i in range(len(native)):
            if native[i].get_text() != comparison[i].get_text():
                text_mismatch.append(i+1)
            a = native[i].get_pixmap(matrix=fitz.Matrix(1,1), colorspace=fitz.csRGB, alpha=False)
            b = comparison[i].get_pixmap(matrix=fitz.Matrix(1,1), colorspace=fitz.csRGB, alpha=False)
            if (a.width,a.height,a.samples) != (b.width,b.height,b.samples):
                pixel_mismatch.append(i+1)
        log = archive.read(stem + '.log').decode()
        critical = [line for line in log.splitlines() if re.search(r'Overfull|LaTeX Error|Missing character:|undefined (?:references|citations)|multiply defined',line)]
        require(not critical, 'Critical final log diagnostic: ' + stem)
        require(not text_mismatch and not pixel_mismatch, 'Local/native PDF parity failed: ' + stem)
        entries[stem] = {'pages':len(native),'native_sha256':sha(raw),'native_git_blob':git_blob(raw),
                         'local_sha256':sha((local/(stem+'.pdf')).read_bytes()),
                         'text_mismatch_pages':text_mismatch,'same_renderer_72dpi_rgb_mismatch_pages':pixel_mismatch,
                         'critical_log_matches':critical,'underfull_notices':len(re.findall('Underfull',log))}
    result = {'status':'passed','scope':'Downloaded artifact integrity, source bytes and recorded Git-mode tree, preservation, active manifests, diagnostic parity and all-page mechanical PDF comparison; no mathematical proof certification or all-page visual inspection.',
              'source_commit':SOURCE,'source_tree':computed_tree,'review_head':'2786efc1351e82f61a24ba4f827712e3e04ca39f',
              'workflow_run':35088239966,'workflow_attempt':1,'artifact_id':10442234606,'artifact_sha256':ARTIFACT,
              'artifact_files':len(archive.namelist()),'build_evidence_entries_verified':len(report['evidence_files']),
              'source_zip_sha256':sha(source_zip_bytes),'frozen_files_verified':len(files),
              'all_source_files_equal_separately_built_local_source':True,
              'inherited_files':len(baseline),'inherited_unchanged':len(unchanged),'edited_originals_verified':edited,
              'active_by_entry':{k:len(v) for k,v in active.items()},'active_union':len(union),
              'normal_optimized_diagnostic_pairs':len(normal_outputs),'pdf_comparison':entries,
              'renderer':fitz.VersionBind,'all_pages_compared':sum(v['pages'] for v in entries.values()),
              'native_publication_attestation':'COMMITTED_OBJECTS_VERIFIED.json, retained at products head fe06224202e1b1ec84962156d5ca20291193b822, records 48 Git blobs fetched at first products commit 6e5caf16d584923f475e369fb9b4c57fc995a9a9; this local script does not access GitHub.'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
