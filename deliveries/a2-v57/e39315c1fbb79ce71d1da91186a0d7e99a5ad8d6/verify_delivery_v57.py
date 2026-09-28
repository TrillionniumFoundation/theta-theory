#!/usr/bin/env python3
"""Verify frozen sources, three native entries and an optional separate rebuild.

Requires PyMuPDF. This program imports no manuscript checking code and performs
no download, compilation, Git write or mathematical proof certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import fitz

FONTS={'.ttf','.otf','.pfb','.pfa','.woff','.woff2'}
ENTRIES=('two_collision','main','rigidity')

def need(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def safe(name: str) -> None:
    p=Path(name)
    need(bool(name) and not p.is_absolute() and '..' not in p.parts,'Unsafe path: '+name)
    need(p.suffix.lower() not in FONTS,'Standalone font file: '+name)

def tree_hash(files: dict) -> str:
    tree={}
    for name,info in files.items():
        node=tree; parts=Path(name).parts
        for part in parts[:-1]:node=node.setdefault(part,{})
        node[parts[-1]]=(info['mode'],info['git_blob'])
    def visit(node):
        entries=[]
        for name,value in node.items():
            mode,h=('40000',visit(value)) if isinstance(value,dict) else value
            entries.append((name+('/' if mode=='40000' else ''),mode,name,h))
        data=b''.join(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(h)
          for _,mode,name,h in sorted(entries))
        return git_hash('tree',data)
    return visit(tree)

def verify(native: Path, source_commit: str, expected_tree: str,
           rebuilt: Path|None, artifact: Path|None, artifact_digest: str|None) -> dict:
    need(re.fullmatch(r'[0-9a-f]{40}',source_commit) is not None,'Invalid source commit')
    report=json.loads((native/'build-report.json').read_text())
    frozen=json.loads((native/'frozen-source-manifest.json').read_text())
    need(report['status']=='passed' and report['source_commit']==source_commit==frozen['source_commit'],
         'Wrong or failed source build')
    need(report['source_tree']==frozen['source_tree']==expected_tree,'Wrong source subtree')
    out={'source_commit':source_commit,'source_tree':expected_tree,
         'mathematical_certification':False,'visual_inspection':'Not performed by this script',
         'renderer':'PyMuPDF '+fitz.VersionBind,'rebuild_checked':rebuilt is not None}
    if artifact is not None:
        need(artifact_digest is not None,'Artifact digest is required')
        data=artifact.read_bytes();need(sha(data)==artifact_digest,'Outer artifact digest mismatch')
        with zipfile.ZipFile(artifact) as z:
            names=[x for x in z.namelist() if not x.endswith('/')]
            need(len(names)==len(set(names)),'Duplicate outer ZIP members')
            for name in names:
                safe(name); need(z.read(name)==(native/name).read_bytes(),'Extracted artifact mismatch: '+name)
        out['artifact']={'bytes':len(data),'sha256':sha(data),'files':len(names)}
    for name,info in report['evidence_files'].items():
        safe(name);data=(native/name).read_bytes()
        need(len(data)==info['bytes'] and sha(data)==info['sha256'],'Native evidence mismatch: '+name)
    active=json.loads((native/'active-source-manifest.json').read_text())
    union={name:info for group in active.values() for name,info in group.items()}
    with zipfile.ZipFile(native/'native-source.zip') as z:
        names=z.namelist();need(len(names)==len(set(names)),'Duplicate source ZIP members')
        need(json.loads(z.read('SOURCE_MANIFEST.json'))==frozen,'Nested manifest mismatch')
        need(set(names)=={'SOURCE_MANIFEST.json'}|{'source/'+n for n in frozen['files']},'Unexpected archive members')
        for name,info in frozen['files'].items():
            safe(name);data=z.read('source/'+name)
            need(len(data)==info['bytes'] and sha(data)==info['sha256']
                 and git_hash('blob',data)==info['git_blob'],'Frozen source mismatch: '+name)
        for name,info in union.items():
            need(info==frozen['files'][name],'Active/frozen identity mismatch: '+name)
            if rebuilt is not None:
                need((rebuilt/name).read_bytes()==z.read('source/'+name),'Rebuild source mismatch: '+name)
    need(not frozen['excluded_tracked_products'],'Unaccounted excluded tree entries')
    need(tree_hash(frozen['files'])==expected_tree,'Reconstructed Git source tree mismatch')
    out.update({'frozen_source_files':len(frozen['files']),
                'active_source_counts':{e:len(active[e]) for e in ENTRIES},
                'unique_active_sources':len(union),'source_tree_reconstructed':True,
                'native_evidence_files':len(report['evidence_files'])})
    pairs=[]
    for p in sorted(native.glob('check_*-normal.json')):
        q=p.with_name(p.name.replace('-normal','-optimized'))
        need(q.is_file() and p.read_bytes()==q.read_bytes(),'Python mode mismatch: '+p.name)
        pairs.append(p.stem.removesuffix('-normal'))
    need(len(pairs)==5,'Expected five diagnostic pairs');out['diagnostic_pairs']=pairs
    imports={}
    for consumer,producers in (('main',('two_collision',)),('rigidity',('two_collision','main'))):
        imported=json.loads((native/(consumer+'-imported-generated-inputs.json')).read_text())
        recorder=json.loads((native/(consumer+'-recorder-inputs.json')).read_text())
        need(set(imported)=={e+'.aux' for e in producers},'Wrong producer set')
        for producer in producers:
            aux=producer+'.aux';i=imported[aux]
            need(i['producer_source_commit']==source_commit and i['sha256']==sha((native/aux).read_bytes())
                 and i['producer_pdf_sha256']==report['entries'][producer]['product']['sha256']
                 and i['producer_recorder_sha256']==sha((native/(producer+'-recorder-inputs.json')).read_bytes())
                 and recorder['generated_inputs'][aux]['sha256']==i['sha256'],'Unmatched imported auxiliary')
        imports[consumer]=list(producers)
    out['source_matched_auxiliary_producers']=imports;out['products']={}
    for stem in ENTRIES:
        data=(native/(stem+'.pdf')).read_bytes();entry=report['entries'][stem]
        need(entry['status']=='passed' and entry['source_integrity']=='verified','Unverified native entry')
        need(sha(data)==entry['product']['sha256'],'Product digest mismatch')
        with fitz.open(stream=data,filetype='pdf') as d:
            need(len(d)==entry['product']['pages'],'Wrong page count')
            item={'pages':len(d),'bytes':len(data),'sha256':sha(data),'git_blob':git_hash('blob',data)}
            outside=[]
            for n,p in enumerate(d,1):
                for b in p.get_text('dict')['blocks']:
                    if b['type']!=0:continue
                    for line in b['lines']:
                        for s in line['spans']:
                            if not p.rect.contains(fitz.Rect(s['bbox'])):outside.append(n)
            item['outside_page_text_span_pages']=sorted(set(outside))
            if rebuilt is not None:
                local=rebuilt/(stem+'.pdf');item['rebuild_sha256']=sha(local.read_bytes())
                badtext=[];badpixels=[]
                with fitz.open(local) as e:
                    need(len(e)==len(d),'Rebuilt pagination differs')
                    for n,(a,b) in enumerate(zip(d,e),1):
                        if a.get_text()!=b.get_text():badtext.append(n)
                        x=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        y=b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                        if (x.width,x.height,x.samples)!=(y.width,y.height,y.samples):badpixels.append(n)
                need(not badtext and not badpixels,'Rebuild text/raster differs: '+stem)
                item.update({'text_and_72dpi_RGB_equal_pages':len(d),'byte_identical':sha(data)==item['rebuild_sha256']})
            out['products'][stem]=item
    out['source_archive']={'bytes':(native/'native-source.zip').stat().st_size,
       'sha256':sha((native/'native-source.zip').read_bytes())}
    out['status']='passed';return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native',type=Path,required=True);p.add_argument('--source-commit',required=True)
    p.add_argument('--source-tree',required=True);p.add_argument('--rebuild',type=Path)
    p.add_argument('--artifact',type=Path);p.add_argument('--artifact-sha256');p.add_argument('--output',type=Path)
    a=p.parse_args();result=json.dumps(verify(a.native,a.source_commit,a.source_tree,a.rebuild,a.artifact,a.artifact_sha256),indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(result)
    else:print(result,end='')

if __name__=='__main__':main()
