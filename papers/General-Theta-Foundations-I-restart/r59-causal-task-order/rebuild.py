#!/usr/bin/env python3
"""Rebuild only committed source from a fresh, read-only Git archive export."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,io,json,os,shutil,subprocess,sys,tarfile,tempfile
ROOT=Path(__file__).resolve().parent

def run(args,**kw):
    p=subprocess.run(args,capture_output=True,text=True,**kw)
    if p.returncode:raise RuntimeError(repr(args)+'\n'+p.stdout[-8000:]+p.stderr[-8000:])
    return p.stdout

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--against',type=Path);ap.add_argument('--source',default='HEAD');args=ap.parse_args()
    repo=Path(run(['git','rev-parse','--show-toplevel'],cwd=ROOT).strip())
    source=run(['git','rev-parse',args.source+'^{commit}'],cwd=repo).strip()
    prefix=ROOT.relative_to(repo).as_posix()
    archive=subprocess.check_output(['git','archive','--format=tar',source+':'+prefix],cwd=repo)
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    if out==ROOT:raise RuntimeError('separate output directory required')
    env=os.environ.copy();env.update({'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
    with tempfile.TemporaryDirectory(prefix='theta-r59-clean-') as tmp:
        clean=Path(tmp)/'source';clean.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
            for member in tf.getmembers():
                path=Path(member.name)
                if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                    raise RuntimeError('unsafe source archive member: '+member.name)
            tf.extractall(clean,filter='data')
        # Read-only source files and directories, while output remains separate.
        for p in clean.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
        clean.chmod(0o555)
        try:
            audit=json.loads(run([sys.executable,str(clean/'verify.py')],env=env))
            normal=run([sys.executable,str(clean/'regression.py')],env=env)
            optimized=run([sys.executable,'-O',str(clean/'regression.py')],env=env)
            if normal!=optimized:raise RuntimeError('clean normal/optimized results differ')
            (out/'regression-normal.json').write_text(normal)
            (out/'regression-optimized.json').write_text(optimized)
            built=json.loads(run([sys.executable,str(clean/'build.py'),'--out',str(out/'build')],env=env))
            after=json.loads(run([sys.executable,str(clean/'verify.py')],env=env))
            if audit!=after:raise RuntimeError('source audit changed during read-only rebuild')
            comparisons={}
            if args.against:
                original=json.loads((args.against/'BUILD_RECEIPT.json').read_text())
                if original['source_manifest_sha256']!=built['source_manifest_sha256']:raise RuntimeError('source manifest differs from primary build')
                for name,doc in built['documents'].items():
                    prior=original['documents'][name]
                    same=doc['sha256']==prior['sha256'] and doc['text_sha256']==prior['text_sha256']
                    comparisons[name]={'pdf_and_text_identical':same,'sha256':doc['sha256']}
                    if not same:raise RuntimeError('rebuild differs from primary: '+name)
            receipt={'status':'PASS','source_commit':source,'source_subtree':prefix,'git_archive_sha256':hashlib.sha256(archive).hexdigest(),'source_manifest_sha256':built['source_manifest_sha256'],'readonly_export_verified':True,'normal_optimized_identical':True,'regression_sha256':hashlib.sha256(normal.encode()).hexdigest(),'audit':audit,'build':built,'same_host_primary_comparison':comparisons,'limitations':'Clean read-only committed-source rebuild, not independent mathematical review. Cross-host toolchains may legitimately produce different PDF bytes; same-host comparison is exact when --against is supplied.'}
            (out/'CLEAN_REBUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
            print(json.dumps(receipt,sort_keys=True,indent=2))
        finally:
            clean.chmod(0o755)
            for p in clean.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
if __name__=='__main__':main()
