#!/usr/bin/env python3
"""Isolated, read-only mathematical builds; no network or repository writes."""
from __future__ import annotations
import argparse,json,lzma,os,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
from verify import ROOT,require,verify,sha256,git_hash
PAPER='General_Theta_Foundations_I_restart_R46.pdf'
PAPER_DIR=Path('papers/General-Theta-Foundations-I-restart')
EPOCH='1791763200'
def run(cmd,cwd=None,env=None):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    require(p.returncode==0,'command failed: '+repr(cmd)+'\n'+p.stdout[-25000:]);return p.stdout

def native(out:Path,source_sha:str|None)->dict:
    audit=verify();before=audit['ordinary_source_projection_tree_sha']
    if source_sha:require(audit['review_input_verified'],'bound build requires pinned review input')
    normal=run([sys.executable,str(ROOT/'regression.py')]);optimized=run([sys.executable,'-O',str(ROOT/'regression.py')])
    require(normal==optimized,'ordinary/optimized finite regression differs')
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH=EPOCH,FORCE_SOURCE_DATE='1',TZ='UTC',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text());products=[]
    for i in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-r46-native-') as td:
            work=Path(td)/'source';work.mkdir()
            for name in list(manifest['files'])+['SOURCE_MANIFEST.json']:
                dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            run([sys.executable,str(work/'verify.py')],cwd=work,env=env);output=work/'output';output.mkdir()
            for _ in range(3):run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory='+str(output),'main.tex'],cwd=work,env=env)
            log=(output/'main.log').read_text(errors='replace')
            for bad in ('There were undefined references','There were multiply-defined labels','Citation `','Reference `','Overfull \\hbox','Overfull \\vbox'):
                require(bad not in log,'LaTeX audit failure: '+bad)
            loaded=set()
            for line in (output/'main.fls').read_text().splitlines():
                if line.startswith('INPUT '):
                    p=Path(line[6:]);p=p if p.is_absolute() else work/p
                    try:rel=p.resolve().relative_to(work).as_posix()
                    except ValueError:continue
                    if rel.endswith('.tex'):loaded.add(rel)
            require(loaded==set(audit['native']['active_tex']),'actual TeX recorder inputs differ')
            info=run(['pdfinfo',str(output/'main.pdf')]);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
            text=' '.join(run(['pdftotext','-enc','UTF-8',str(output/'main.pdf'),'-']).split())
            aux=(output/'main.aux').read_text();labels={a:b for a,b in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}',aux)}
            products.append(((output/'main.pdf').read_bytes(),log,pages,text,labels))
    require(products[0][0]==products[1][0],'within-environment PDF byte mismatch')
    require(verify()['ordinary_source_projection_tree_sha']==before,'native source mutation')
    data,log,pages,text,labels=products[0];(out/PAPER).write_bytes(data);(out/'R46_LATEX_BUILD.log').write_text(log)
    return {'status':'PASS','source_commit':source_sha,'binding':'declared immutable source commit; external GitHub readback required' if source_sha else 'local uncommitted preflight only','ordinary_source_projection_tree_sha':before,'source_audit':audit,'regression':json.loads(normal),'normal_and_optimized_equal':True,'isolated_pdf_builds':2,'passes_per_build':3,'within_environment_byte_equal':True,'pdf_pages':pages,'pdf_sha256':sha256(data),'pdf_git_blob_sha':git_hash('blob',data),'normalized_text_sha256':sha256(text.encode()),'pdf_bytes':len(data),'tex_engine':run(['pdflatex','--version']).splitlines()[0],'python':sys.version.split()[0],'theorem_labels':{k:v for k,v in labels.items() if k.startswith(('thm:','prop:','lem:','cor:','def:'))},'undefined_references':0,'overfull_boxes':0,'source_mutation':False,'hosted_run_id':os.environ.get('GITHUB_RUN_ID'),'limitations':'finite checks and build provenance, not theorem correctness, priority or significance'}

def copy_inputs(original:Path,target:Path)->None:
    """Only copy; never modify a checked-out source or run an old publisher."""
    ignore=shutil.ignore_patterns('.git','artifacts','evidence','__pycache__','*.pdf','*.png','*.ttf','*.otf','*.woff','*.woff2')
    for name in [PAPER_DIR,Path('foundations/general-theta')]:
        if (original/name).is_dir():shutil.copytree(original/name,target/name,ignore=ignore)
    for f in original.glob('GENERAL_THETA*.md'):shutil.copyfile(f,target/f.name)
    # Only hash-pinned historical data and literal provenance files are copied.
    for sub in ['data','scripts']:
        parent=original/'.github'/sub
        if parent.exists():
            dest=target/'.github'/sub;dest.mkdir(parents=True,exist_ok=True)
            for pat in ['theta-r43*','theta-r44*','theta-r45*']:
                for f in parent.glob(pat):
                    if f.is_file() and not f.is_symlink():shutil.copyfile(f,dest/f.name)
    dest=target/PAPER_DIR/'r46-causal-stopping'
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(ROOT,dest,ignore=ignore)

def recover(target:Path)->list[dict]:
    """Static hash-checked historical text recovery; decoded code is not executed here."""
    pins=json.loads((ROOT/'RECOVERY_PINS.json').read_text());receipts=[]
    for item in pins:
        dest=target/item['destination']
        if not (dest/'main.tex').exists():
            parts=[]
            for path,expected in item['parts']:
                data=(target/path).read_bytes();require(git_hash('blob',data)==expected,'retained transport blob mismatch '+path);parts.append(data)
            raw=b''.join(parts);require(sha256(raw)==item['transport_sha256'],'retained transport digest mismatch')
            records=json.loads(lzma.decompress(raw))
            for name,record in records.items():
                rel=Path(name)
                require(not rel.is_absolute() and '..' not in rel.parts and not {'.git','artifacts','evidence','transport'}.intersection(rel.parts),'unsafe retained path')
                data=record['text'].encode();require(sha256(data)==record['sha256'],'retained file digest mismatch')
                f=dest/rel;require(not f.exists() or f.read_bytes()==data,'refusing a differing retained overwrite')
                f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
        # This is a documented read-only inventory program, not the publisher.
        check=json.loads(run([sys.executable,str(dest/'verify.py')]))
        require(check['ordinary_source_projection_tree_sha']==item['projection_tree'],'retained ordinary source projection mismatch')
        report=target/'GENERAL_THETA_FOUNDATIONS_I_RESTART_R32_BAYESIAN_CURVATURE_EXTERNAL_REFEREE_REPORT_R32.md'
        require(git_hash('blob',report.read_bytes())=='3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21','retained report mismatch')
        f=dest/'review_inputs/R32_EXTERNAL_REFEREE_REPORT.md';f.parent.mkdir(exist_ok=True);f.write_bytes(report.read_bytes())
        receipts.append({'destination':item['destination'],'projection_tree':item['projection_tree'],'transport_sha256':item['transport_sha256']})
    return receipts

def ordinary_snapshot(root:Path)->dict:
    out={}
    for f in sorted(root.rglob('*')):
        if not f.is_file():continue
        rel=f.relative_to(root)
        if set(rel.parts)&{'.git','.github','artifacts','evidence','__pycache__','transport'}:continue
        if f.suffix.lower() in {'.pdf','.png','.jpg','.zip','.xz','.gz','.ttf','.otf','.woff','.woff2'}:continue
        out[rel.as_posix()]=sha256(f.read_bytes())
    return out

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha');ap.add_argument('--prepared-root',type=Path);ap.add_argument('--retained',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.source_sha:require(bool(re.fullmatch('[0-9a-f]{40}',args.source_sha)),'full source SHA required')
    out=args.output.resolve();require(out!=ROOT and ROOT not in out.parents,'output must be outside native ordinary source');out.mkdir(parents=True,exist_ok=True)
    result=native(out,args.source_sha)
    result['total_isolated_pdf_builds']=2;result['retained_scope']='not requested'
    if args.retained:
        require(args.prepared_root is not None,'full retained build requires prepared-root')
        with tempfile.TemporaryDirectory(prefix='theta-r46-retained-') as td:
            prepared=Path(td)/'prepared';prepared.mkdir();copy_inputs(args.prepared_root.resolve(),prepared)
            recovery=recover(prepared);before=ordinary_snapshot(prepared)
            oldout=Path(td)/'retained-output';oldreceipt=Path(td)/'retained.json'
            cmd=[sys.executable,str(prepared/PAPER_DIR/'r45-adapted-stopping/build.py'),'--output',str(oldout),'--receipt',str(oldreceipt)]
            if args.source_sha:cmd+=['--source-sha',args.source_sha]
            env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
            log=run(cmd,env=env);(out/'RETAINED_BUILD.stdout').write_text(log)
            old=json.loads(oldreceipt.read_text());require(old['status']=='PASS','retained build failed')
            for f in oldout.glob('*.pdf'):
                name=f.name.replace('_R45_','_R46_')
                if f.name=='General_Theta_Foundations_I_restart_R45.pdf':name='General_Theta_Foundations_I_R46_Companion_AdaptedStopping.pdf'
                shutil.copyfile(f,out/name)
            require(ordinary_snapshot(prepared)==before,'retained ordinary inputs changed')
            export=out/'R46_prepared_sources.zip'
            with zipfile.ZipFile(export,'w',zipfile.ZIP_DEFLATED) as z:
                for name in before:z.write(prepared/name,name)
                z.writestr('R46_INPUT_BINDING.json',json.dumps({'source_commit':args.source_sha,'files':before,'retained_recovery':recovery},sort_keys=True,indent=2)+'\n')
            result.update(retained_complete_R45=old,retained_recovery=recovery,retained_scope='Full R45 native article and its complete retained chain; not every historical repository paper',total_isolated_pdf_builds=2+old['total_isolated_pdf_builds'],prepared_source_files=len(before),prepared_sources_zip_sha256=sha256(export.read_bytes()),prepared_source_mutation=False)
    from pypdf import PdfReader
    result['delivery_pdfs']={f.name:{'sha256':sha256(f.read_bytes()),'git_blob_sha':git_hash('blob',f.read_bytes()),'pages':len(PdfReader(f).pages),'bytes':f.stat().st_size,'normalized_text_sha256':sha256(' '.join(run(['pdftotext','-enc','UTF-8',str(f),'-']).split()).encode())} for f in sorted(out.glob('*.pdf'))}
    result['total_delivery_pages']=sum(v['pages'] for v in result['delivery_pdfs'].values())
    (out/'BUILD_RECEIPT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='retained_complete_R45'},sort_keys=True,indent=2))
if __name__=='__main__':main()
