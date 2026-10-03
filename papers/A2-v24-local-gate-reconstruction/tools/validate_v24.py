#!/usr/bin/env python3
"""Read-only qualification with explicitly recorded legacy layout adjustments.

Retained repository sources remain byte-identical. Historical raw v18 and S
PDFs/logs are archived before disclosed staged layout adjustments.
All delivered layout-qualified PDFs must pass the strict diagnostics gate.
A local source-content execution is not an authenticated Git checkout.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOTS={'retained/v23':'357f5bf8c60f73597ccbd503aaf7235d53cda1e6',
           'complete':'14b2e5379e5b223bc0bdc823c97fd77c2dca2cda'}
LAYOUT='\\addtolength{\\textheight}{8pt}\n\\raggedbottom\n'
S_LAYOUT='\\raggedbottom\n'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None


def manifest() -> dict[str,str]:
    paths=[ROOT/'main.tex',ROOT/'references.tex']
    paths+=sorted((ROOT/'core').glob('*.tex'))
    paths+=sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)):sha(p) for p in paths}


def diagnostics(log: Path) -> list[str]:
    return re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                      log.read_text(errors='replace'),re.M)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--output-dir',default='verification/current')
    args=ap.parse_args()
    out=(ROOT/args.output_dir).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output must be below verification/')
    out.mkdir(parents=True,exist_ok=True)
    before=manifest()
    receipt={'schema':'a2-v24-source-validation-1','status':'running',
      'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'execution_kind':'git_checkout' if git('rev-parse','HEAD') else 'source_content_not_git_checkout',
      'scope':'all_declared_volumes_with_disclosed_layout_adjustments' if args.all_volumes else 'primary_only',
      'source_commit':git('rev-parse','HEAD'),'source_tree':git('rev-parse','HEAD^{tree}'),
      'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
      'runner_image':os.getenv('ImageOS'),'runner_image_version':os.getenv('ImageVersion'),
      'platform':platform.platform(),'python':sys.version,
      'packages':{p:importlib.metadata.version(p) for p in ['numpy','scipy']},
      'commands':[],'documents':[],'raw_historical_documents':[],
      'source_manifest':before,'executed_physical_sensor':False,
      'formal_proof_certificate':False,'raw_retained_v18_warning_free_asserted':False,
      'raw_supplement_s_warning_free_asserted':False}

    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        path=out/(label+'.log');path.write_text(p.stdout)
        receipt['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
          'exit_code':p.returncode,'log':path.name,'log_sha256':sha(path)})
        if p.returncode: raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout

    def document(directory: Path,stem: str,source: str,label: str,strict: bool=True) -> None:
        pdf=directory/(stem+'.pdf');log=directory/(stem+'.log')
        problems=diagnostics(log)
        info=run(['pdfinfo',str(pdf)],ROOT,label+'-pdfinfo')
        match=re.search(r'^Pages:\s+(\d+)',info,re.M)
        item={'source':source,'pages':int(match.group(1)) if match else None,
          'pdf':str(pdf.relative_to(ROOT)),'pdf_sha256':sha(pdf),'tex_log_sha256':sha(log),
          'final_tex_diagnostics':problems,'layout_wrapper_applied':label in ('retained-3','retained-5')}
        receipt['documents' if strict else 'raw_historical_documents'].append(item)
        if strict and problems: raise RuntimeError(source+': final TeX diagnostics remain')

    def compile_tex(directory: Path,stem: str,label: str,outdir: str | None=None) -> None:
        cmd=['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error']
        if outdir: cmd.append('-outdir='+outdir)
        run(cmd+[stem+'.tex'],directory,label)

    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        if pins['source_sha256']!=before:
            raise RuntimeError('source pins do not exactly cover the current mathematical/tool manifest')
        receipt['source_pins_sha256']=sha(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('all-volume qualification requires --require-checkout')
        if args.require_checkout:
            if not receipt['source_commit']: raise RuntimeError('no Git checkout')
            if git('diff','--name-only','HEAD','--','.')!='':
                raise RuntimeError('tracked sources differ from checkout')
            if receipt['github_sha'] and receipt['github_sha']!=receipt['source_commit']:
                raise RuntimeError('triggering SHA and checkout differ')
            prefix=git('rev-parse','--show-prefix') or ''
            for path,want in SNAPSHOTS.items():
                if git('rev-parse','HEAD:'+prefix+path)!=want:
                    raise RuntimeError('retained tree differs: '+path)
            receipt['verified_retained_trees']=SNAPSHOTS
        normal=run([sys.executable,'tools/verify_v24.py'],ROOT,'v24-normal')
        optimized=run([sys.executable,'-O','tools/verify_v24.py'],ROOT,'v24-optimized')
        if normal!=optimized: raise RuntimeError('normal and optimized outputs differ')
        receipt['diagnostics']=json.loads(normal)
        receipt['normal_optimized_identical']=True
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        compile_tex(ROOT,'main','primary-build','build')
        document(ROOT/'build','main','main.tex','primary')
        if args.all_volumes:
            stage=out/'retained-build'
            if stage.exists(): shutil.rmtree(stage)
            shutil.copytree(ROOT/'retained/v23',stage)
            for label,directory,script,extra in [
                ('v23',stage,'verify_v23.py',['--geometry']),
                ('v22',stage/'retained/v22','verify_v22.py',[])]:
                n=run([sys.executable,'tools/'+script]+extra,directory,'retained-'+label+'-normal')
                o=run([sys.executable,'-O','tools/'+script]+extra,directory,'retained-'+label+'-optimized')
                if n!=o: raise RuntimeError('retained normal/optimized mismatch: '+label)
                receipt['retained_'+label+'_diagnostics']=json.loads(n)
            v21=stage/'retained/v22/retained/v21'
            v18=v21/'retained/v18'
            original=(v18/'main.tex').read_text()
            if original.count('\\begin{document}')!=1:
                raise RuntimeError('unexpected retained v18 document anchor')
            # Preserve the actual raw historical build; warnings are not erased.
            compile_tex(v18,'main','raw-v18-build','raw-build')
            document(v18/'raw-build','main','retained/v23/retained/v22/retained/v21/retained/v18/main.tex',
                     'raw-v18',strict=False)
            adjusted=original.replace('\\begin{document}',LAYOUT+'\\begin{document}',1)
            if adjusted.replace(LAYOUT,'',1)!=original:
                raise RuntimeError('layout wrapper changed other source content')
            (v18/'main.tex').write_text(adjusted)
            receipt['v18_layout_wrapper']={'source_sha256':hashlib.sha256(original.encode()).hexdigest(),
                'staged_source_sha256':sha(v18/'main.tex'),'inserted_before_begin_document':LAYOUT,
                'repository_source_changed':False,'mathematical_body_changed':False,
                'raw_diagnostics_archived':True}
            (out/'v18-layout-wrapper.json').write_text(json.dumps(receipt['v18_layout_wrapper'],indent=2)+'\n')
            targets=[(stage,'main','retained/v23/main.tex'),
                     (stage/'retained/v22','main','retained/v23/retained/v22/main.tex'),
                     (v21,'main','retained/v23/retained/v22/retained/v21/main.tex'),
                     (v18,'main','retained/v23/retained/v22/retained/v21/retained/v18/main.tex'),
                     (v21/'complete','two_collision','complete/two_collision.tex'),
                     (v21/'complete','main','complete/main.tex')]
            for pass_no in range(2):
                for i,(directory,stem,source) in enumerate(targets):
                    compile_tex(directory,stem,f'retained-{i}-pass-{pass_no}')
            # Archive raw S after cross-references have stabilized, before reflow.
            supplement=v21/'complete'
            raw_s=out/'raw-supplement-s'
            raw_s.mkdir(exist_ok=True)
            for suffix in ('.pdf','.log'):
                shutil.copy2(supplement/('main'+suffix),raw_s/('main'+suffix))
            document(raw_s,'main','complete/main.tex','raw-supplement-s',strict=False)
            s_main=supplement/'main.tex'
            s_bib=supplement/'v5/references.tex'
            originals={s_main:s_main.read_text(),s_bib:s_bib.read_text()}
            if originals[s_main].count('\\begin{document}')!=1:
                raise RuntimeError('unexpected S document anchor')
            bib_anchor='\\begin{thebibliography}{99}'
            if originals[s_bib].count(bib_anchor)!=1:
                raise RuntimeError('unexpected S bibliography anchor')
            changes={s_main:originals[s_main].replace('\\begin{document}',
                        S_LAYOUT+'\\begin{document}',1),
                     s_bib:originals[s_bib].replace(bib_anchor,
                        bib_anchor+'\n\\raggedright',1)}
            if changes[s_main].replace(S_LAYOUT,'',1)!=originals[s_main]:
                raise RuntimeError('S main layout changed other content')
            if changes[s_bib].replace(bib_anchor+'\n\\raggedright',bib_anchor,1)!=originals[s_bib]:
                raise RuntimeError('S bibliography layout changed other content')
            adjustments=[]
            for path,text in changes.items():
                path.write_text(text)
                adjustments.append({'path':str(path.relative_to(supplement)),
                    'source_sha256':hashlib.sha256(originals[path].encode()).hexdigest(),
                    'staged_source_sha256':sha(path)})
            receipt['supplement_s_layout']={'adjustments':adjustments,
                'main_insertion':S_LAYOUT,'bibliography_insertion':'\\raggedright',
                'repository_source_changed':False,'mathematical_text_changed':False,
                'raw_diagnostics_archived':True}
            (out/'supplement-s-layout.json').write_text(json.dumps(receipt['supplement_s_layout'],indent=2)+'\n')
            compile_tex(supplement,'main','supplement-s-layout-build')
            for i,(directory,stem,source) in enumerate(targets):
                document(directory,stem,source,f'retained-{i}')
        if manifest()!=before: raise RuntimeError('mathematical/tool sources changed during validation')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('tracked sources changed during validation')
        receipt['source_unchanged']=True
        receipt['status']='passed'
    except Exception as exc:
        receipt['status']='failed';receipt['error']=str(exc)
    finally:
        receipt['source_manifest_sha256']=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        receipt['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
        print(json.dumps(receipt,sort_keys=True,indent=2))
    return 0 if receipt['status']=='passed' else 1

if __name__=='__main__': raise SystemExit(main())
