#!/usr/bin/env python3
"""Native v42 source/diagnostic/two-document qualification; no source rewriting.

--freeze updates only V42_SOURCE_PINS.json in the working copy.
--development never certifies a remote commit. Publication requires
--expected-head, committed-byte checks, and unchanged historical Git trees.
--capture-source runs the same source checks without claiming a PDF build.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import validate_v41 as inherited

ROOT=Path(__file__).resolve().parents[1]
PACKAGE='papers/A2-v42-proof-completion'
WORKFLOW='.github/workflows/a2-v42-verify.yml'
PINS='V42_SOURCE_PINS.json'
BASE='d81e4053bfba1703c4086ea8f9c69ed32c3537b6'
OLD='papers/A2-v41-referee-response'
OLD_TREE='254376f3ceee96b7f7ce24010fd9c62d7cde7f69'
EXTERNAL={doc:[{**entry,'pdf':entry['pdf'].replace('v41','v42')} for entry in entries]
          for doc,entries in inherited.EXTERNAL_DOCUMENTS.items()}
inherited.EXTERNAL_DOCUMENTS=EXTERNAL


def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def git(repo:Path,*args:str)->str:
    return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()


def sources(repo:Path)->dict[str,str]:
    paths=[p for p in ROOT.rglob('*') if p.is_file() and
           not set(p.relative_to(ROOT).parts)&{'build','verification','__pycache__'} and
           (p.suffix in {'.tex','.md','.py','.json'} or p.name=='.gitignore') and p.name!=PINS]
    paths.append(repo/WORKFLOW)
    result={}
    for p in sorted(paths):
        if p.is_symlink() or not p.is_file():
            raise ValueError('nonregular or missing source: '+str(p))
        result[p.relative_to(repo).as_posix()]=digest(p.read_bytes())
    return result


def read_old(repo:Path,directory:str)->dict[str,str]:
    pending=['main.tex','companion.tex']; found={}
    while pending:
        name=pending.pop()
        if name in found: continue
        if '..' in Path(name).parts or Path(name).is_absolute():
            raise ValueError('unsafe historical input')
        text=subprocess.check_output(['git','-C',str(repo),'show','HEAD:'+directory+'/'+name]).decode()
        found[name]=text
        clean=re.sub(r'(?<!\\)%[^\n]*','',text)
        for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',clean):
            if '\\' in name: raise ValueError('nonliteral historical input')
            pending.append(name if name.endswith('.tex') else name+'.tex')
    return found


def committed(repo:Path,expected:str,hashes:dict[str,str])->None:
    if not re.fullmatch('[0-9a-f]{40}',expected) or git(repo,'rev-parse','HEAD')!=expected:
        raise ValueError('HEAD does not equal the required exact commit')
    if git(repo,'status','--porcelain','--untracked-files=no'):
        raise ValueError('tracked checkout is dirty')
    entries=git(repo,'ls-tree','-r',expected,'--',PACKAGE,WORKFLOW).splitlines()
    tracked={line.split('\t',1)[1] for line in entries}
    if tracked!=set(hashes):
        raise ValueError('tracked-source inventory differs from the qualification inventory')
    for line in entries:
        meta,name=line.split('\t',1); mode,kind,sha=meta.split()
        data=(repo/name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if mode!='100644' or kind!='blob' or actual!=sha or digest(data)!=hashes[name]:
            raise ValueError('committed bytes differ: '+name)


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    parser.add_argument('--expected-head')
    parser.add_argument('--development',action='store_true')
    parser.add_argument('--capture-source',action='store_true')
    args=parser.parse_args()
    repo=Path(git(ROOT,'rev-parse','--show-toplevel'))
    current=sources(repo)
    manifest={'schema':'a2-v42-source-pins-1','base_commit':BASE,'paper_directory':PACKAGE,
              'sources':current,'scope':'Source hashes, not proof certification.'}
    if args.freeze:
        (ROOT/PINS).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');return 0
    out=ROOT/'verification'/'v42';out.mkdir(parents=True,exist_ok=True)
    receipt={'schema':'a2-v42-qualification-1','status':'started','exact_commit_qualified':False,
             'development':args.development,'formal_proof_certificate':False,
             'human_specialist_review':False,'commands':[]}
    try:
        if json.loads((ROOT/PINS).read_text())!=manifest:
            raise ValueError('v42 source manifest mismatch; freeze only after editing')
        all_hashes={**current,PACKAGE+'/'+PINS:digest((ROOT/PINS).read_bytes())}
        head=git(repo,'rev-parse','HEAD');receipt['head_sha']=head
        if not args.development:
            if not args.expected_head:raise ValueError('publication requires --expected-head')
            committed(repo,args.expected_head,all_hashes)
            receipt['preserved_trees']=inherited.verify_preserved_trees(repo)
            if git(repo,'rev-parse','HEAD:'+OLD)!=OLD_TREE:
                raise ValueError('the v41 directory changed')
            receipt['preserved_trees']['retained_v41']=OLD_TREE
        closure=inherited.tex_document_inputs(ROOT)
        texts={name:(ROOT/name).read_bytes().decode() for name in set().union(*map(set,closure.values()))}
        receipt['document_partition']=inherited.verify_document_partition(closure,texts)
        receipt['external_documents']=inherited.verify_external_declarations(ROOT,closure)
        if args.development:
            base_dir=repo/OLD
            old_closure=inherited.tex_document_inputs(base_dir)
            old_texts={n:(base_dir/n).read_bytes().decode() for n in set().union(*map(set,old_closure.values()))}
            receipt['v41_preservation']=inherited.verify_preservation(old_texts,texts)
        else:
            receipt['v41_preservation']=inherited.verify_preservation(read_old(repo,OLD),texts)
            receipt['v40_preservation']=inherited.verify_preservation(inherited.read_reviewed_inputs(repo),texts)
        inherited.deterministic_zip(out/'A2-v42-repository-source.zip',repo,
                                    {name:(name,h) for name,h in all_hashes.items()})
        inherited.deterministic_zip(out/'A2-v42-journal-source.zip',repo,
                                    {name:(PACKAGE+'/'+name,current[PACKAGE+'/'+name]) for name in texts})
        shutil.copyfile(ROOT/PINS,out/'source-pins.json')
        receipt['source_captured']=True
        if args.capture_source:
            receipt['status']='source_captured';return 0
        epoch=git(repo,'show','-s','--format=%ct','HEAD')
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','LC_ALL':'C','TZ':'UTC',
             'SOURCE_DATE_EPOCH':epoch,'FORCE_SOURCE_DATE':'1'}
        def run(argv,label,timeout=600):
            process=subprocess.run(argv,cwd=ROOT,env=env,stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,timeout=timeout)
            (out/(label+'.log')).write_bytes(process.stdout)
            receipt['commands'].append({'argv':argv,'log':label+'.log','exit_code':process.returncode})
            if process.returncode:raise ValueError('command failed: '+label)
            return process.stdout
        receipt['diagnostics']=[]
        for script in ('verify_v41.py','verify_v42.py'):
            normal=run([sys.executable,'tools/'+script],script+'-normal')
            optimized=run([sys.executable,'-O','tools/'+script],script+'-optimized')
            if normal!=optimized:raise ValueError('optimized diagnostics differ')
            result=json.loads(normal)
            if result.get('status')!='passed':raise ValueError('diagnostics did not pass')
            receipt['diagnostics'].append({'script':script,'normal_optimized_identical':True,'result':result})
        run(['pdflatex','--version'],'tex-version')
        run(['latexmk','-v'],'latexmk-version')
        (ROOT/'build').mkdir(exist_ok=True)
        build=Path(tempfile.mkdtemp(prefix='v42-',dir=ROOT/'build'))
        env['TEXINPUTS']=str(build)+os.pathsep+env.get('TEXINPUTS','')+os.pathsep
        previous={};stable=False
        for iteration in range(1,7):
            for doc in ('companion.tex','main.tex'):
                run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
                     '-file-line-error','-latexoption=-no-shell-escape','-outdir='+str(build),doc],
                    doc+'-round-'+str(iteration))
            auxiliary=inherited.auxiliary_state(build)
            if auxiliary==previous and len(auxiliary)>=2:
                stable=True;break
            previous=auxiliary
        if not stable:raise ValueError('cross-document auxiliaries failed to stabilize')
        receipt['cross_document_auxiliaries_stable']=True
        receipt['documents']=[]
        for doc,tag in (('main.tex','primary'),('companion.tex','companion')):
            stem=Path(doc).stem
            log=(build/(stem+'.log')).read_text(errors='replace')
            findings=inherited.inspect_tex_log(log)
            if findings:raise ValueError('final TeX findings: '+repr(findings))
            recorded=inherited.verify_recorded_inputs(build/(stem+'.fls'),ROOT,repo,build,
                all_hashes,closure[doc],EXTERNAL[doc],log)
            info=run(['pdfinfo',str(build/(stem+'.pdf'))],stem+'-pdfinfo').decode()
            pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
            if not pages:raise ValueError('missing PDF page count')
            target=out/('A2-v42-'+tag+'.pdf');shutil.copyfile(build/(stem+'.pdf'),target)
            for suffix in ('.log','.fls','.aux'):shutil.copyfile(build/(stem+suffix),out/('final-'+stem+suffix))
            receipt['documents'].append({'source':doc,'artifact':target.name,'pages':int(pages[1]),
                'sha256':digest(target.read_bytes()),'final_tex_findings':[],
                'recorded_input_closure':recorded})
        if sources(repo)!=current or digest((ROOT/PINS).read_bytes())!=all_hashes[PACKAGE+'/'+PINS]:
            raise ValueError('source changed during execution')
        if not args.development:committed(repo,args.expected_head,all_hashes)
        receipt['source_unchanged']=True
        receipt['exact_commit_qualified']=not args.development
        receipt['status']='passed';return 0
    except Exception as error:
        receipt['status']='failed';receipt['error']=str(error)
        print(str(error),file=sys.stderr);return 1
    finally:
        receipt['artifact_sha256']={p.name:digest(p.read_bytes()) for p in sorted(out.iterdir())
                                   if p.is_file() and p.name!='receipt.json'}
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'status':receipt['status'],'receipt':str(out/'receipt.json')}))


if __name__=='__main__':
    sys.exit(main())
