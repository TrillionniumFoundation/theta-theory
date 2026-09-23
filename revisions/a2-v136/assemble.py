#!/usr/bin/env python3
"""Assemble only v136 from immutable reviewed source and readable overlays."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, re, shutil, subprocess, tarfile, tempfile
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='9fb3a5b9b27d4f6c6df2f3e557b4fc709c3a546d'
REVIEWED='003fb13458c8ed11e2973963493a662f31c700c0'
R1='9f246bef692ee715851c4b200041c5cfe76da7d9'
SOURCE=Path('papers/A2-v17-boundary-information-coarsening/article/v135');DEST=SOURCE.with_name('v136')
REVIEW='reviews/a2-v135-independent-harsh-top4-r2-2026-09-23/REFEREE_REPORT.md'
REVIEW1='reviews/a2-v135-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'
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
    with tempfile.TemporaryDirectory(prefix='a2-v136-') as td:
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
        for src in (HERE/'overlay').rglob('*'):
            if src.is_file():
                d=target/src.relative_to(HERE/'overlay');d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,d)
        for n,h in oldtex.items():
            if not(target/n).exists() or sha(target/n)!=h:
                d=target/'history/v135-modified-source'/n;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/n,d)
        reviewhash={}
        if not args.base_dir:
            for ref,path,name in [(BASE,REVIEW,'R2'),(R1,REVIEW1,'R1')]:
                data=subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
                d=target/'review_inputs'/('V135_'+name+'_REFEREE_REPORT.md');d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(data)
                reviewhash[str(d.relative_to(target))]=sha(d)
        newlabels=labels(target)
        if len(newlabels)!=len(set(newlabels)) or not set(oldlabels)<=set(newlabels):raise RuntimeError('Compiled label preservation failed')
        unchanged={n:h for n,h in oldtex.items() if (target/n).exists() and sha(target/n)==h}
        static={str(f.relative_to(target)):sha(f) for f in target.rglob('*') if f.is_file() and f.suffix in ('.tex','.py','.sh','.md','.json') and f.name!='PROVENANCE_MANIFEST.json' and 'evidence' not in f.relative_to(target).parts and '__pycache__' not in f.parts}
        m={'revision':136,'assembly_commit':commit,'reviewed_commit':REVIEWED,'controlling_review_commit':BASE,'additional_review_commit':R1,'controlling_review':REVIEW,'inherited_mathematical_labels':sorted(set(oldlabels)),'unchanged_inherited_tex_sha256':unchanged,'reviewed_tex_sha256':oldtex,'assembled_sha256':static,'review_input_sha256':reviewhash,'full_Ballico_1993_comparison_completed':False,'formal_proof_verified':False}
        (target/'PROVENANCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
        final=ROOT/DEST
        if final.exists():shutil.rmtree(final)
        final.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(target,final)
        print(json.dumps({'revision':136,'assembly_commit':commit,'retained_labels':len(set(oldlabels)),'current_labels':len(newlabels),'unchanged_tex':len(unchanged)},indent=2))
if __name__=='__main__':main()
