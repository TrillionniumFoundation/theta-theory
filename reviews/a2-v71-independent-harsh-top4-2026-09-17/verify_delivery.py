#!/usr/bin/env python3
"""Independent A2-v71 artifact/retention audit; never imports manuscript code.

Python 3.10+; optional PDF comparison needs PyMuPDF. This checks bytes, modes,
Git objects and finite render equality, not mathematical truth or all-page vision.
"""
from __future__ import annotations
import argparse, hashlib, io, json, re, zipfile
from pathlib import Path
from typing import Any

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def digest(data: bytes, kind: str = 'sha256') -> str:
    return hashlib.new(kind, data).hexdigest()

def git_object(kind: str, data: bytes) -> str:
    return digest(f'{kind} {len(data)}\0'.encode() + data, 'sha1')

def tree_hash(files: dict[str, dict[str, Any]]) -> str:
    tree: dict[str, Any] = {}
    for path, item in files.items():
        node = tree
        parts = path.split('/')
        require(all(p not in ('', '.', '..') for p in parts), f'Unsafe path {path}')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (item['mode'], item['git_blob'])
    def encode(node: dict[str, Any]) -> str:
        body = bytearray()
        for name, value in sorted(node.items(), key=lambda kv: (kv[0] + ('/' if isinstance(kv[1], dict) else '')).encode()):
            mode, sha = ('40000', encode(value)) if isinstance(value, dict) else value
            body += f'{mode} {name}\0'.encode() + bytes.fromhex(sha)
        return git_object('tree', bytes(body))
    return encode(tree)

def read_artifact(path: Path) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any], dict[str, Any]]:
    with zipfile.ZipFile(path) as outer:
        require(len(outer.namelist()) == len(set(outer.namelist())), 'Duplicate artifact entries')
        contents = {i.filename: outer.read(i) for i in outer.infolist() if not i.is_dir()}
    report = json.loads(contents['build-report.json'])
    manifest = json.loads(contents['frozen-source-manifest.json'])
    for name, item in report['evidence_files'].items():
        data = contents[name]
        require(len(data) == item['bytes'] and digest(data) == item['sha256'], f'Evidence mismatch {name}')
    require(digest(contents['native-source.zip']) == report['source_archive_sha256'], 'Source ZIP hash mismatch')
    with zipfile.ZipFile(io.BytesIO(contents['native-source.zip'])) as archive:
        require(len(archive.namelist()) == len(set(archive.namelist())), 'Duplicate source entries')
        embedded = json.loads(archive.read('SOURCE_MANIFEST.json'))
        require(embedded == manifest, 'Inner/outer manifests differ')
        source = {}
        actual = {n[len('source/'):] for n in archive.namelist() if n.startswith('source/') and not n.endswith('/')}
        require(actual == set(manifest['files']), 'Manifest source coverage mismatch')
        for name, item in manifest['files'].items():
            info = archive.getinfo('source/' + name)
            data = archive.read(info)
            require(len(data) == item['bytes'], f'Length mismatch {name}')
            require(digest(data) == item['sha256'], f'SHA256 mismatch {name}')
            require(git_object('blob', data) == item['git_blob'], f'Git blob mismatch {name}')
            require(info.external_attr >> 16 == int(item['mode'], 8), f'Raw mode mismatch {name}')
            source[name] = data
    reconstructed = tree_hash(manifest['files'])
    require(reconstructed == manifest['source_tree'] == report['source_tree'], 'Git subtree mismatch')
    active = json.loads(contents['active-source-manifest.json'])
    input_counts = {}
    for entry, declared in active.items():
        visited: set[str] = set()
        def visit(name: str) -> None:
            if name in visited:
                return
            require(name in source, f'Missing literal TeX input {name}')
            visited.add(name)
            text = re.sub(r'(?m)(?<!\\)%.*$', '', source[name].decode())
            for child in re.findall(r'\\(?:input|include)\{([^{}]+)\}', text):
                visit(child if child.endswith('.tex') else child + '.tex')
        visit(entry + '.tex')
        require(visited == set(declared), f'Literal inputs differ for {entry}')
        for name, item in declared.items():
            require(item == manifest['files'][name], f'Active metadata mismatch {name}')
        input_counts[entry] = len(visited)
    pairs = {}
    for name in contents:
        if name.endswith('-normal.json'):
            opt = name.replace('-normal.json', '-optimized.json')
            require(json.loads(contents[name]) == json.loads(contents[opt]), f'Diagnostic output mismatch {name}')
            pairs[name] = True
    result = {
        'artifact_sha256': digest(path.read_bytes()),
        'source_commit': report['source_commit'], 'source_tree_reconstructed': reconstructed,
        'source_zip_sha256': digest(contents['native-source.zip']),
        'source_files_bytes_blobs_and_raw_modes_verified': len(source),
        'evidence_files_verified': len(report['evidence_files']),
        'active_literal_input_counts': input_counts,
        'active_literal_input_union': len(set().union(*(set(x) for x in active.values()))),
        'recorded_normal_optimized_pairs_match': pairs,
        'author_diagnostic_code_executed': False,
        'products': {e: {'sha256': digest(contents[e+'.pdf']), 'bytes': len(contents[e+'.pdf']),
                         'git_blob': git_object('blob', contents[e+'.pdf'])} for e in active},
    }
    return result, source, manifest, active

def compare_build(native: Path, rebuilt: Path) -> dict[str, Any]:
    import fitz
    result: dict[str, Any] = {'renderer': fitz.VersionBind, 'rgb_dpi': 72, 'entries': {}}
    patterns = {
        'overfull': r'Overfull \\[hv]box',
        'undefined': r'(?:Reference|Citation) .* undefined|There were undefined',
        'missing_character': r'Missing character:',
        'multiply_defined': r'multiply defined',
        'latex_error': r'^!|LaTeX Error:',
        'underfull': r'Underfull \\[hv]box',
    }
    for entry in ('two_collision', 'main', 'rigidity'):
        a, b = native / (entry+'.pdf'), rebuilt / (entry+'.pdf')
        with fitz.open(a) as doc_a, fitz.open(b) as doc_b:
            require(len(doc_a) == len(doc_b), f'Page count differs {entry}')
            text_diff, rgb_diff = [], []
            for i, (pa, pb) in enumerate(zip(doc_a, doc_b)):
                if pa.get_text() != pb.get_text(): text_diff.append(i+1)
                xa, xb = pa.get_pixmap(dpi=72, colorspace=fitz.csRGB, alpha=False), pb.get_pixmap(dpi=72, colorspace=fitz.csRGB, alpha=False)
                if (xa.width, xa.height, digest(xa.samples)) != (xb.width, xb.height, digest(xb.samples)): rgb_diff.append(i+1)
            log = (rebuilt / (entry+'.log')).read_text(errors='replace')
            result['entries'][entry] = {'pages': len(doc_a), 'text_difference_pages': text_diff,
                'rgb_difference_pages': rgb_diff, 'rebuilt_sha256': digest(b.read_bytes()),
                'native_sha256': digest(a.read_bytes()), 'pdf_bytes_equal': a.read_bytes() == b.read_bytes(),
                'final_log_counts': {name:len(re.findall(pattern, log, re.M)) for name,pattern in patterns.items()}}
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--native-dir', type=Path)
    parser.add_argument('--rebuilt-dir', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    current, source, manifest, active = read_artifact(args.current)
    old, prior, prior_manifest, prior_active = read_artifact(args.previous)
    changed = [p for p in prior if source.get(p) != prior[p] or manifest['files'].get(p, {}).get('mode') != prior_manifest['files'][p]['mode']]
    require(set(prior) <= set(source), 'Inherited path deleted')
    for name in changed:
        archived = 'history/v70-review-baseline/' + name
        require(source.get(archived) == prior[name], f'Changed original not byte-exact {name}')
        require(manifest['files'][archived]['mode'] == prior_manifest['files'][name]['mode'], f'Changed original mode differs {name}')
    a, b = set().union(*(set(x) for x in prior_active.values())), set().union(*(set(x) for x in active.values()))
    require(a <= b, 'Former active input omitted')
    core = ['article/' + n for n in ['10a_periodic_itinerary_relative_v64.tex','10b_periodic_contact_inverse_v65.tex','10c_global_curvature_inverse_v66.tex','10d_smooth_contact_rigidity_v68.tex','10e_sampled_smooth_recovery_v69.tex']]
    require(all(source[p] == prior[p] for p in core), 'Core module changed')
    result = {'scope':'Bytes/modes/Git objects/literal inputs and optional PDF comparison, not proof certification.',
              'current':current, 'previous':old,
              'retention':{'inherited':len(prior), 'unchanged_in_place':len(prior)-len(changed),
              'changed_originals_preserved_bytes_and_modes':changed, 'core_modules_unchanged':core,
              'old_active_inputs':len(a), 'new_active_inputs':sorted(b-a), 'old_active_inputs_retained':True}}
    if args.native_dir or args.rebuilt_dir:
        require(bool(args.native_dir and args.rebuilt_dir), 'Both PDF directories required')
        result['independent_build_comparison'] = compare_build(args.native_dir, args.rebuilt_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
