#!/usr/bin/env python3
"""Two immutable native builds; finite checks do not certify continuum proofs."""
from __future__ import annotations
import argparse,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from verify import ROOT,require,verify,sha256,git_hash
PAPER='General_Theta_Foundations_I_restart_R24.pdf'
def run(cmd,cwd=None,env=None):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    require(p.returncode==0,'command failed: '+repr(cmd)+'\n'+p.stdout[-20000:]);return p.stdout
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--expected-tree');ap.add_argument('--output',default=str(ROOT/'artifacts'));ap.add_argument('--receipt',default=str(ROOT/'evidence'/'NATIVE_BUILD_RECEIPT.json'));args=ap.parse_args()
    if args.source_sha:require(bool(re.fullmatch('[0-9a-f]{40}',args.source_sha)),'full source SHA required')
    audit=verify();before=audit['native_source_tree_sha']
    if args.expected_tree:require(before==args.expected_tree,'source-tree binding mismatch')
    normal=run([sys.executable,str(ROOT/'regression.py')]);optimized=run([sys.executable,'-O',str(ROOT/'regression.py')]);require(normal==optimized,'ordinary/optimized regression differs')
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791504000',FORCE_SOURCE_DATE='1',TZ='UTC',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text());products=[]
    for i in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-r24-native-') as td:
            work=Path(td)/'source';work.mkdir()
            for name in list(manifest['files'])+['SOURCE_MANIFEST.json']:
                dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            run([sys.executable,str(work/'verify.py')],cwd=work,env=env);out=work/'output';out.mkdir()
            for _ in range(3):run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory='+str(out),'main.tex'],cwd=work,env=env)
            log=(out/'main.log').read_text(errors='replace')
            for bad in ('There were undefined references','There were multiply-defined labels','Citation `','Reference `','Overfull \\hbox','Overfull \\vbox'):require(bad not in log,'LaTeX audit failure: '+bad)
            loaded=set()
            for line in (out/'main.fls').read_text().splitlines():
                if line.startswith('INPUT '):
                    p=Path(line[6:]);p=p if p.is_absolute() else work/p
                    try:rel=p.resolve().relative_to(work).as_posix()
                    except ValueError:continue
                    if rel.endswith('.tex'):loaded.add(rel)
            require(loaded==set(audit['active_tex']),'actual TeX recorder inputs differ')
            info=run(['pdfinfo',str(out/'main.pdf')]);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
            text=run(['pdftotext','-enc','UTF-8',str(out/'main.pdf'),'-']);normalized=' '.join(text.split())
            aux=(out/'main.aux').read_text();labels={a:b for a,b in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}',aux)}
            products.append(((out/'main.pdf').read_bytes(),log,pages,normalized,labels))
    require(products[0][0]==products[1][0],'within-environment PDF byte mismatch');require(verify()['native_source_tree_sha']==before,'source mutation')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);data,log,pages,text,labels=products[0]
    (out/PAPER).write_bytes(data);(out/'R24_LATEX_BUILD.log').write_text(log)
    result={'status':'PASS','source_commit':args.source_sha,'binding':'ordinary remote source commit and native directory tree' if args.source_sha else 'uncommitted local preflight only','native_source_tree_sha':before,'source_audit':audit,'regression':json.loads(normal),'normal_and_optimized_equal':True,'isolated_rebuilds':2,'passes_per_rebuild':3,'pdf_byte_identical_within_environment':True,'pdf_pages':pages,'pdf_sha256':sha256(data),'pdf_git_blob_sha':git_hash('blob',data),'normalized_text_sha256':sha256(text.encode()),'pdf_bytes':len(data),'tex_engine':run(['pdflatex','--version']).splitlines()[0],'python':sys.version.split()[0],'theorem_labels':{k:v for k,v in labels.items() if k.startswith(('thm:','prop:','lem:','cor:','def:'))},'overfull_boxes':0,'undefined_references':0,'source_mutation':False,'hosted_run_id':os.environ.get('GITHUB_RUN_ID'),'limitations':'native build and finite arithmetic only; not a mathematical or priority certificate'}
    rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
