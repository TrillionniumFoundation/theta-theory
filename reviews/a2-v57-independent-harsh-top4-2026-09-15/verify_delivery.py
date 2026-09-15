#!/usr/bin/env python3
"""Independent byte/manifest/tree and native-rebuild checks; not a proof certificate."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from zipfile import ZipFile

def require(test, message):
    if not test: raise RuntimeError(message)

def gh(kind, data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()

def tree_hash(items):
    tree={}
    for name, record in items.items():
        parts=name.split('/'); d=tree
        for part in parts[:-1]: d=d.setdefault(part,{})
        d[parts[-1]]=(record['mode'],record['git_blob'])
    def walk(d):
        out=[]
        for name,value in d.items():
            mode,sha=('40000',walk(value)) if isinstance(value,dict) else value
            out.append((name.encode()+(b'/' if mode=='40000' else b''),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
        return gh('tree',b''.join(v for _,v in sorted(out)))
    return walk(tree)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('artifact',type=Path);ap.add_argument('--rebuild',action='store_true');ap.add_argument('--output',type=Path,default=Path('DELIVERY_VERIFICATION.json')); a=ap.parse_args()
    native=a.artifact.resolve(); output=a.output.resolve(); root=output.parent
    f=json.loads((native/'frozen-source-manifest.json').read_text()); active=json.loads((native/'active-source-manifest.json').read_text()); b=json.loads((native/'build-report.json').read_text())
    require(f['source_commit']=='e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6','wrong source')
    with ZipFile(native/'native-source.zip') as z:
        require(json.loads(z.read('SOURCE_MANIFEST.json'))==f,'archive manifest mismatch')
        for name, r in f['files'].items():
            raw=z.read('source/'+name)
            require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'] and gh('blob',raw)==r['git_blob'],'source mismatch '+name)
        require(len(z.namelist())==1+len(f['files']),'extra archive members')
        build=root/'rebuild'; require(not build.exists(),'rebuild directory already exists')
        build.mkdir()
        for name,r in f['files'].items():
            require(not name.startswith('/') and '..' not in Path(name).parts,'unsafe path')
            p=build/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read('source/'+name))
    actual=tree_hash(f['files']);require(actual==f['source_tree'],'source tree mismatch')
    union=set()
    for entry,files in active.items():
        union.update(files)
        for name,r in files.items(): require(r==f['files'][name],'active manifest mismatch '+name)
    for name,r in b['evidence_files'].items():
        raw=(native/name).read_bytes(); require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'evidence mismatch '+name)
    out={'source_commit':f['source_commit'],'source_tree':actual,'frozen_source_files':len(f['files']),'active_source_counts':{k:len(v) for k,v in active.items()},'distinct_active_sources':len(union),'verified_evidence_files':len(b['evidence_files']),'source_archive_sha256':hashlib.sha256((native/'native-source.zip').read_bytes()).hexdigest(),'proof_certificate':False,'rebuilds':{}}
    if a.rebuild:
        import fitz
        for entry in ['two_collision','main','rigidity']:
            command=['latexmk','-norc','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-pdflatex=pdflatex -no-shell-escape -recorder %O %S',entry+'.tex']
            run=subprocess.run(command,cwd=build,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
            (root/(entry+'-independent-build.txt')).write_bytes(run.stdout);require(run.returncode==0,'build failure '+entry)
            n=fitz.open(native/(entry+'.pdf')); r=fitz.open(build/(entry+'.pdf'));require(len(n)==len(r),'page count mismatch')
            text=[];pixels=[]
            for i in range(len(n)):
                if n[i].get_text()!=r[i].get_text():text.append(i+1)
                np=n[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);rp=r[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                if (np.width,np.height,np.samples)!=(rp.width,rp.height,rp.samples):pixels.append(i+1)
            log=(build/(entry+'.log')).read_text(errors='replace')
            bad=re.findall(r'[^\n]*(?:undefined references|undefined citations|Missing character|Overfull \\|LaTeX Error)[^\n]*',log)
            warnings=re.findall(r'[^\n]*Underfull[^\n]*',log)
            out['rebuilds'][entry]={'pages':len(n),'returncode':run.returncode,'text_mismatch_pages':text,'rgb_72dpi_mismatch_pages':pixels,'byte_identical':(native/(entry+'.pdf')).read_bytes()==(build/(entry+'.pdf')).read_bytes(),'warning_or_error_matches':bad,'underfull_notices':warnings}
            require(not text and not pixels and not bad,'product mismatch or warning '+entry)
    out['status']='passed';output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
