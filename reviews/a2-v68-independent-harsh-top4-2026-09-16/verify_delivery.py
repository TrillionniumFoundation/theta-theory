#!/usr/bin/env python3
"""Independent source/evidence and fresh-PDF verifier. No author checker is imported.
Run: python verify_delivery.py WORK_ROOT [--build ENTRY | --compare]
WORK_ROOT contains artifact/ and source/source/ from the downloaded native artifact.
Requires Python 3, PyMuPDF, pdflatex and latexmk for the optional build checks.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess

def require(ok, message):
    if not ok: raise RuntimeError(message)

def digest(data, kind='sha256'):
    return hashlib.new(kind,data).hexdigest()

def git_object(kind,data):
    return digest(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data,'sha1')

def check_file(path,record):
    b=path.read_bytes()
    require(len(b)==record['bytes'],f'Length mismatch: {path}')
    require(digest(b)==record['sha256'],f'SHA256 mismatch: {path}')
    if 'git_blob' in record:
        require(git_object('blob',b)==record['git_blob'],f'Git blob mismatch: {path}')

def tree_hash(node):
    entries=[]
    for name,value in node.items():
        if isinstance(value,dict):
            entries.append((name+'/',b'40000 '+name.encode()+b'\0'+bytes.fromhex(tree_hash(value))))
        else:
            mode,sha=value
            entries.append((name,mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
    return git_object('tree',b''.join(e[1] for e in sorted(entries)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path)
    ap.add_argument('--build',choices=['two_collision','main','rigidity']);ap.add_argument('--compare',action='store_true')
    args=ap.parse_args();root=args.root.resolve();src=root/'source/source';art=root/'artifact'
    out=root/'REPRODUCTION_RESULTS.json'
    report=json.loads((art/'build-report.json').read_text())
    result=json.loads(out.read_text()) if out.exists() else {}
    if args.build:
        work=root/'rebuild'
        if not work.exists(): shutil.copytree(src,work)
        cmd=['latexmk','-norc','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-pdflatex=pdflatex -no-shell-escape -recorder %O %S',args.build+'.tex']
        proc=subprocess.run(cmd,cwd=work,capture_output=True,text=True,timeout=120)
        (root/(args.build+'-fresh-build.txt')).write_text(proc.stdout+proc.stderr)
        require(proc.returncode==0,'Build failed; see retained build output')
        log=(work/(args.build+'.log')).read_text(errors='replace')
        critical=[l for l in log.splitlines() if re.search(r'undefined|Missing character|Overfull|LaTeX Error',l,re.I)]
        result.setdefault('fresh_builds',{})[args.build]={'returncode':proc.returncode,'command':cmd,'critical_log_matches':critical,'underfull_notices':sum('Underfull' in l for l in log.splitlines())}
    elif args.compare:
        import fitz
        result['pdf_comparison']={}
        for name in ['two_collision','main','rigidity']:
            original=art/(name+'.pdf');fresh=root/'rebuild'/(name+'.pdf')
            a=fitz.open(original);b=fitz.open(fresh)
            require(len(a)==len(b),name+': page-count mismatch')
            text_mismatch=[];render_mismatch=[]
            for i in range(len(a)):
                if a[i].get_text()!=b[i].get_text(): text_mismatch.append(i+1)
                pa=a[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                pb=b[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                if (pa.width,pa.height,pa.samples)!=(pb.width,pb.height,pb.samples): render_mismatch.append(i+1)
            result['pdf_comparison'][name]={'pages':len(a),'text_mismatch_pages':text_mismatch,'same_renderer_72dpi_rgb_mismatch_pages':render_mismatch,'pdf_byte_identity':original.read_bytes()==fresh.read_bytes(),'native_sha256':digest(original.read_bytes()),'fresh_sha256':digest(fresh.read_bytes())}
        result['renderer']=fitz.VersionBind
        result['scope']='Mechanical equality at the stated renderer/resolution is not visual inspection or proof verification.'
    else:
        manifest=json.loads((root/'source/SOURCE_MANIFEST.json').read_text());tree={}
        for name,rec in manifest['files'].items():
            check_file(src/name,rec);node=tree;parts=name.split('/')
            for part in parts[:-1]: node=node.setdefault(part,{})
            node[parts[-1]]=(rec['mode'],rec['git_blob'])
        computed=tree_hash(tree)
        expected=report['source_tree']
        require(computed==expected,f'Manuscript tree {computed} != {expected}')
        active=json.loads((art/'active-source-manifest.json').read_text());union=set()
        for entry,files in active.items():
            for name,rec in files.items(): check_file(src/name,rec);union.add(name)
        for name,rec in report['evidence_files'].items(): check_file(art/name,rec)
        for name,entry in report['entries'].items(): check_file(art/(name+'.pdf'),entry['product'])
        result.update({'actual_source':report.get('source_commit'), 'manuscript_tree':computed,'frozen_files_verified':len(manifest['files']),'active_files_per_entry':{n:len(v) for n,v in active.items()},'active_union':len(union),'build_evidence_files_verified':len(report['evidence_files']),'native_source_zip_sha256':digest((art/'native-source.zip').read_bytes()),'imports_author_checker':False})
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__': main()
