#!/usr/bin/env python3
"""Independent byte/mode/tree and native evidence checks; no theorem certification."""
from __future__ import annotations
import argparse, hashlib, io, json, re, zipfile
from pathlib import Path, PurePosixPath

def need(test: bool, msg: str) -> None:
    if not test: raise ValueError(msg)

def sha(data: bytes, kind: str = 'sha256') -> str:
    return hashlib.new(kind, data).hexdigest()

def git_object(kind: str, data: bytes) -> str:
    return sha(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data, 'sha1')

def tree_hash(files: dict) -> str:
    root: dict = {}
    for path, row in files.items():
        node=root
        *parents, name=path.split('/')
        for parent in parents: node=node.setdefault(parent,{})
        need(name not in node, 'Duplicate tree path')
        node[name]=(row['mode'], row['git_blob'])
    def rec(node: dict) -> str:
        entries=[]
        for name, value in node.items():
            if isinstance(value,dict): mode, obj, key='40000',rec(value),name.encode()+b'/'
            else: mode,obj=value;key=name.encode()
            entries.append((key, mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(obj)))
        return git_object('tree',b''.join(x[1] for x in sorted(entries)))
    return rec(root)

def verify(artifact: Path, baseline_artifact: Path | None = None) -> dict:
    with zipfile.ZipFile(artifact) as outer:
        need(len(outer.namelist())==len(set(outer.namelist())), 'Duplicate artifact entry')
        source_bytes=outer.read('native-source.zip')
        build=json.loads(outer.read('build-report.json'))
        manifest=json.loads(outer.read('frozen-source-manifest.json'))
        with zipfile.ZipFile(io.BytesIO(source_bytes)) as source:
            need(json.loads(source.read('SOURCE_MANIFEST.json'))==manifest,'Two manifests differ')
            files=manifest['files']
            need(set(source.namelist())=={'SOURCE_MANIFEST.json'}|{'source/'+p for p in files}, 'Archive member mismatch')
            mode_errors=[]
            for name, row in files.items():
                pp=PurePosixPath(name)
                need(not pp.is_absolute() and '..' not in pp.parts and '\\' not in name,'Unsafe path')
                data=source.read('source/'+name); zi=source.getinfo('source/'+name)
                need(len(data)==row['bytes'] and sha(data)==row['sha256'] and git_object('blob',data)==row['git_blob'], 'Byte mismatch: '+name)
                if zi.create_system!=3 or ((zi.external_attr>>16)&0xffff)!=int(row['mode'],8): mode_errors.append(name)
            need(not mode_errors,'Raw ZIP modes mismatch')
            reconstructed=tree_hash(files)
            need(reconstructed==manifest['source_tree'], 'Reconstructed subtree mismatch')
            baseline=json.loads(source.read('source/history/v68-review-baseline/SOURCE_MANIFEST.json'))
            changed=[];unchanged=0
            for name, old in baseline['files'].items():
                need(name in files,'Deleted baseline file '+name)
                if files[name]==old: unchanged+=1
                else:
                    changed.append(name)
                    archived='history/v68-review-baseline/'+name
                    need(archived in files and files[archived]==old,'Old bytes/mode not retained '+name)
            active=json.loads(outer.read('active-source-manifest.json'))
            union=set()
            for stem, rows in active.items():
                seen=set()
                def walk(name):
                    if name in seen: return
                    seen.add(name)
                    text=source.read('source/'+name).decode()
                    text=re.sub(r'(?<!\\)%[^\n]*', '', text)
                    for child in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', text):
                        walk(child if child.endswith('.tex') else child+'.tex')
                walk(stem+'.tex')
                need(seen==set(rows), 'Active input graph mismatch '+stem)
                need(all(files[k]==v for k,v in rows.items()), 'Active input identities mismatch')
                union.update(seen)
            baseline_authentication=None
            if baseline_artifact is not None:
                with zipfile.ZipFile(baseline_artifact) as old_outer:
                    old_manifest=json.loads(old_outer.read('frozen-source-manifest.json'))
                    need(old_manifest==baseline,'Embedded baseline differs from downloaded old artifact')
                    old_mode_errors=[]
                    with zipfile.ZipFile(io.BytesIO(old_outer.read('native-source.zip'))) as old_source:
                        old_active=json.loads(old_outer.read('active-source-manifest.json'))
                        old_union=set().union(*(set(v) for v in old_active.values()))
                        need(old_union<=union,'An inherited active input was removed')
                        for name,row in old_manifest['files'].items():
                            data=old_source.read('source/'+name)
                            need(len(data)==row['bytes'] and sha(data)==row['sha256'] and git_object('blob',data)==row['git_blob'],'Old artifact byte mismatch '+name)
                            mode=(old_source.getinfo('source/'+name).external_attr>>16)&0xffff
                            if mode!=int(row['mode'],8):old_mode_errors.append(name)
                    need(tree_hash(old_manifest['files'])==old_manifest['source_tree'],'Old tree reconstruction fails')
                    baseline_authentication=dict(artifact_sha256=sha(baseline_artifact.read_bytes()),source_commit=old_manifest['source_commit'],reconstructed_tree=old_manifest['source_tree'],all_old_bytes_verified=True,raw_mode_mismatches=old_mode_errors,old_active_inputs_retained=len(old_union))
            native=[]
            import fitz
            for stem, info in build['entries'].items():
                data=outer.read(stem+'.pdf'); doc=fitz.open(stream=data,filetype='pdf')
                need(sha(data)==info['product']['sha256'] and len(data)==info['product']['bytes'] and len(doc)==info['product']['pages'], 'PDF identity mismatch '+stem)
                log=outer.read(stem+'.log').decode(errors='replace')
                patterns=[r'Overfull \\[hv]box',r'LaTeX Error',r'Missing character:',r'LaTeX Warning: (?:Reference|Citation).*undefined',r'There were undefined references',r'multiply[- ]defined']
                matches=[p for p in patterns if re.search(p,log,re.I)]
                need(not matches,'Final log errors '+stem+str(matches))
                native.append({'entry':stem,'pages':len(doc),'sha256':sha(data),'underfull_notices':len(re.findall(r'Underfull \\[hv]box',log)),'fatal_scan':matches})
            for name,row in build['evidence_files'].items():
                data=outer.read(name)
                need(len(data)==row['bytes'] and sha(data)==row['sha256'],'Evidence mismatch '+name)
            pairs=[]
            for n in ['check_adaptive','check_revision_v32','check_revision_v38','check_revision_v69']:
                need(outer.read(n+'-normal.json')==outer.read(n+'-optimized.json'),'Recorded diagnostic pair differs')
                pairs.append(n)
            return {'status':'passed','scope':'Independent archive bytes, raw modes, tree reconstruction, active-input graph, downloaded-baseline comparison and native evidence; not proof certification; author diagnostic programs not rerun.', 'artifact_sha256':sha(artifact.read_bytes()),'source_zip_sha256':sha(source_bytes),'source_commit':manifest['source_commit'],'reconstructed_manuscript_tree':reconstructed,'frozen_files':len(files),'raw_modes':'all match','active_tex_by_entry':{k:len(v) for k,v in active.items()},'active_tex_union':len(union),'baseline_authentication':baseline_authentication,'baseline_files':len(baseline['files']),'baseline_unchanged':unchanged,'baseline_modified_with_exact_archives':changed,'native_evidence_files':len(build['evidence_files']),'recorded_normal_optimized_pairs_equal':pairs,'pdfs':native}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);p.add_argument('--baseline',type=Path);args=p.parse_args()
    print(json.dumps(verify(args.artifact,args.baseline),indent=2,sort_keys=True))
