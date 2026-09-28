#!/usr/bin/env python3
"""Independent v70 delivery/retention checks; no author code is imported.
Usage: python verify_delivery.py V70_ARTIFACT_ZIP V69_ARTIFACT_ZIP
Checks archive bytes and raw Unix modes, reconstructs Git trees, follows literal
active TeX inputs, and checks retention. It does not certify any theorem.
"""
from __future__ import annotations
import hashlib, io, json, re, stat, sys, zipfile
from pathlib import Path, PurePosixPath

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(f'{kind} {len(data)}\0'.encode()+data).hexdigest()

def entries(data: bytes) -> dict[str, tuple[bytes, int]]:
    result = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            require(not p.is_absolute() and '..' not in p.parts, 'unsafe ZIP path')
            require(item.filename not in result, 'duplicate ZIP path')
            mode = item.external_attr >> 16
            require(not stat.S_ISLNK(mode), 'ZIP symlink not permitted')
            if not item.is_dir():
                result[item.filename] = (z.read(item), mode)
    return result

def tree_hash(files: dict) -> str:
    root = {}
    for path, metadata in files.items():
        parts = path.split('/')
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (metadata['mode'], metadata['git_blob'])
    def recurse(node):
        ordered = sorted(node.items(), key=lambda kv: (kv[0]+('/' if isinstance(kv[1],dict) else '')).encode())
        payload = bytearray()
        for name, value in ordered:
            mode, digest = ('40000', recurse(value)) if isinstance(value,dict) else value
            payload.extend(f'{mode} {name}\0'.encode()+bytes.fromhex(digest))
        return git_hash('tree', bytes(payload))
    return recurse(root)

def active_inputs(source: dict, entry: str) -> set[str]:
    visited = set()
    def follow(path):
        require(path in source, f'missing TeX input {path}')
        if path in visited:
            return
        visited.add(path)
        text = source[path][0].decode()
        text = re.sub(r'(?<!\\)%[^\n]*', '', text)
        for inc in re.findall(r'\\(?:input|include)\s*\{([^{}]+)\}', text):
            require('\\' not in inc and '#' not in inc, 'nonliteral input needs manual audit')
            follow(inc if inc.endswith('.tex') else inc+'.tex')
    follow(entry+'.tex')
    # Include the entry and all recursively reachable literal inputs.
    return visited

def audit(path: Path):
    raw = path.read_bytes(); outer = entries(raw)
    native = outer['native-source.zip'][0]; inner = entries(native)
    manifest = json.loads(outer['frozen-source-manifest.json'][0])
    require(json.loads(inner['SOURCE_MANIFEST.json'][0])==manifest,'inner/outer manifest mismatch')
    files = manifest['files']
    source = {p.removeprefix('source/'): v for p,v in inner.items() if p.startswith('source/')}
    require(set(source)==set(files),'source inventory mismatch')
    for p, meta in files.items():
        b, mode = source[p]
        require(len(b)==meta['bytes'],f'length mismatch {p}')
        require(sha256(b)==meta['sha256'],f'SHA-256 mismatch {p}')
        require(git_hash('blob',b)==meta['git_blob'],f'Git blob mismatch {p}')
        require(mode==int(meta['mode'],8),f'raw mode mismatch {p}')
    tree = tree_hash(files)
    require(tree==manifest['source_tree'],'Git tree mismatch')
    build = json.loads(outer['build-report.json'][0])
    for p, meta in build['evidence_files'].items():
        b=outer[p][0]
        require(len(b)==meta['bytes'] and sha256(b)==meta['sha256'],f'evidence mismatch {p}')
    active_recorded=json.loads(outer['active-source-manifest.json'][0])
    parsed={e:active_inputs(source,e) for e in active_recorded}
    for e, listed in active_recorded.items():
        require(set(listed)<=parsed[e],f'inactive declared input in {e}')
        for p,meta in listed.items():
            require(meta==files[p],f'active manifest metadata mismatch {p}')
    pairs={}
    for p in outer:
        if p.endswith('-normal.json'):
            opt=p.replace('-normal.json','-optimized.json')
            pairs[p]=outer[p][0]==outer[opt][0]
            require(pairs[p],f'author recorded diagnostic mismatch {p}')
    summary={
        'artifact_sha256':sha256(raw), 'source_zip_sha256':sha256(native),
        'source_commit':manifest['source_commit'], 'source_tree_reconstructed':tree,
        'source_files_verified':len(files), 'source_raw_modes_verified':len(files),
        'evidence_files_verified':len(build['evidence_files']),
        'active_declared':{e:len(a) for e,a in active_recorded.items()},
        'active_literal_including_entry_and_preamble':{e:len(a) for e,a in parsed.items()},
        'active_declared_union':len(set().union(*(set(a) for a in active_recorded.values()))),
        'literal_only_inputs':{e:sorted(parsed[e]-set(active_recorded[e])) for e in parsed},
        'recorded_author_normal_optimized_pairs_match':pairs,
        'author_diagnostic_programs_rerun':False,
        'native_products':{e:v['product'] for e,v in build['entries'].items()}
    }
    return summary,source,manifest,parsed

def main():
    if len(sys.argv)!=3:
        raise SystemExit(__doc__)
    current,source,manifest,active=audit(Path(sys.argv[1]))
    previous,old,oldmanifest,oldactive=audit(Path(sys.argv[2]))
    require(set(old)<=set(source),'source deletion')
    changed=[p for p in old if old[p]!=source[p]]
    for p in changed:
        saved='history/v69-review-baseline/'+p
        require(saved in source and source[saved]==old[p],f'original not retained byte/mode exact: {p}')
    old_union=set().union(*oldactive.values());new_union=set().union(*active.values())
    require(old_union<=new_union,'previous active input removed')
    cores=sorted(p for p in old if re.match(r'article/10[a-e]_.*\.tex$',p))
    require(len(cores)==5,'unexpected core inventory')
    require(all(old[p]==source[p] for p in cores),'core source changed')
    # Primary literature name/identifier search in all current TeX/bibliography bytes.
    pattern=re.compile(r'Noakes|Stoyanov|1803\.02542|1402\.6445|lens rigidity|travell?ing times',re.I)
    found={p:pattern.findall(b.decode()) for p,(b,mode) in source.items()
           if p.endswith(('.tex','.bib')) and pattern.search(b.decode())}
    result={'v70':current,'v69':previous,
        'retention':{'old_files':len(old),'unchanged':len(old)-len(changed),'changed':changed,
            'changed_originals_bytes_and_modes_preserved':True,'five_core_modules_unchanged':cores,
            'all_previous_literal_inputs_retained':True,
            'new_literal_inputs':sorted(new_union-old_union)},
        'lens_scattering_keyword_matches_all_frozen_tex_bib':found,
        'scope':'Archive/hash/mode/input evidence only; no theorem certification and no author checker execution.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    main()
