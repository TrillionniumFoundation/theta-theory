#!/usr/bin/env python3
"""Assemble only v138 from immutable reviewed source and readable overlays."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, re, shutil, subprocess, tarfile, tempfile
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='ba24a0b2d062897ee2d7a6b02add81c504fe0e71'
REVIEWED='d4f45624e91456ff135434a1236d8de2549ff0b9'
R1=None
SOURCE=Path('papers/A2-v17-boundary-information-coarsening/article/v137');DEST=SOURCE.with_name('v138')
REVIEW='reviews/a2-v137-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'
REVIEW1=None
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def labels(root):
    seen=set();texts=[]
    def visit(n):
        if n in seen:return
        if Path(n).is_absolute() or '..' in Path(n).parts:raise RuntimeError(n)
        seen.add(n);s=(root/n).read_text();texts.append(s)
        for c in re.findall(r'\\input\{([^}]+)\}',s):visit(c)
    visit('complete.tex');return re.findall(r'\\label\{([^}]+)\}','\n'.join(texts))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base-dir',type=Path);args=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='a2-v138-') as td:
        td=Path(td)
        if args.base_dir:base=args.base_dir.resolve();commit='local-preflight-not-a-remote-commit'
        else:
            subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
            data=subprocess.check_output(['git','archive',BASE,str(SOURCE)],cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(data)) as ar:
                for m in ar.getmembers():
                    q=PurePosixPath(m.name)
                    if q.is_absolute() or '..' in q.parts or not(m.isfile() or m.isdir()):raise RuntimeError('Unsafe archive')
                    d=td/'base'/m.name
                    if m.isdir():d.mkdir(parents=True,exist_ok=True)
                    else:d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(ar.extractfile(m).read())
            base=td/'base'/SOURCE;commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        prior=json.loads((base/'PROVENANCE_MANIFEST.json').read_text())
        for n,h in prior['assembled_sha256'].items():
            if sha(base/n)!=h:raise RuntimeError('Reviewed source hash mismatch: '+n)
        oldlabels=labels(base);oldtex={str(f.relative_to(base)):sha(f) for f in base.rglob('*.tex')}
        target=td/'new';shutil.copytree(base,target);shutil.rmtree(target/'evidence',ignore_errors=True)
        for f in list(target.rglob('__pycache__')):shutil.rmtree(f)
        for f in list(target.iterdir()):
            if f.suffix in ('.pdf','.aux','.out','.toc','.log'):f.unlink()
        for src in sorted((HERE/'overlay').rglob('*')):
            if src.is_file() and '__pycache__' not in src.parts and 'evidence' not in src.relative_to(HERE/'overlay').parts:
                rel=src.relative_to(HERE/'overlay');d=target/rel
                if d.is_file() and d.read_bytes()!=src.read_bytes():
                    archived=target/'history/v137-modified-source'/rel
                    archived.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(d,archived)
                d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,d)
        for n,h in oldtex.items():
            if not(target/n).exists() or sha(target/n)!=h:
                d=target/'history/v137-modified-source'/n;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/n,d)
        reviewhash={}
        if not args.base_dir:
            for ref,path,name in [(BASE,REVIEW,'CONTROLLING')]:
                data=subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
                d=target/'review_inputs'/('V137_'+name+'_REFEREE_REPORT.md');d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(data)
                reviewhash[str(d.relative_to(target))]=sha(d)
        newlabels=labels(target)
        if len(newlabels)!=len(set(newlabels)) or not set(oldlabels)<=set(newlabels):raise RuntimeError('Compiled label preservation failed')
        unchanged={n:h for n,h in oldtex.items() if (target/n).exists() and sha(target/n)==h}
        static={str(f.relative_to(target)):sha(f) for f in target.rglob('*') if f.is_file() and f.suffix in ('.tex','.py','.sh','.md','.json') and f.name!='PROVENANCE_MANIFEST.json' and 'evidence' not in f.relative_to(target).parts and '__pycache__' not in f.parts}
        m={'revision':138,'assembly_commit':commit,'reviewed_commit':REVIEWED,'controlling_review_commit':BASE,'additional_review_commit':R1,'controlling_review':REVIEW,'inherited_mathematical_labels':sorted(set(oldlabels)),'unchanged_inherited_tex_sha256':unchanged,'reviewed_tex_sha256':oldtex,'assembled_sha256':static,'review_input_sha256':reviewhash,'full_Ballico_1993_comparison_completed':False,'formal_proof_verified':False}
        (target/'PROVENANCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
        final=ROOT/DEST
        if final.exists():shutil.rmtree(final)
        final.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(target,final)
        print(json.dumps({'revision':138,'assembly_commit':commit,'retained_labels':len(set(oldlabels)),'current_labels':len(newlabels),'unchanged_tex':len(unchanged)},indent=2))
if __name__=='__main__':main()
