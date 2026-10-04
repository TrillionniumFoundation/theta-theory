#!/usr/bin/env python3
"""Native v43 source/diagnostic/two-document qualification; no source rewriting.

--freeze updates only SOURCE_PINS.json in the working copy.
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
PACKAGE='papers/A2-v43-journal-package'
WORKFLOW='.github/workflows/a2-v43-verify.yml'
PINS='SOURCE_PINS.json'
BASE='74787c9c353b72983fe1bb43af467e31d3eb0f2a'
OLD='papers/A2-v42-proof-completion'
OLD_TREE='be6f133ceb1924243165076b2aaec4801a80c9c1'
EXTERNAL={doc:[{**entry,'pdf':entry['pdf'].replace('v41','v43')} for entry in entries]
          for doc,entries in inherited.EXTERNAL_DOCUMENTS.items()}
inherited.EXTERNAL_DOCUMENTS=EXTERNAL


def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def git(repo:Path,*args:str)->str:
    return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()


def sources(repo:Path)->dict[str,str]:
    paths=[p for p in ROOT.rglob('*') if p.is_file() and
           not set(p.relative_to(ROOT).parts)&{'build','verification','__pycache__'} and
           (p.suffix in {'.tex','.md','.py','.json','.sh'} or p.name=='.gitignore') and p!=ROOT/PINS]
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
    manifest={'schema':'a2-v43-source-pins-1','base_commit':BASE,'paper_directory':PACKAGE,
              'sources':current,'scope':'Source hashes, not proof certification.'}
    if args.freeze:
        (ROOT/PINS).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');return 0
    out=ROOT/'verification'/'v43';out.mkdir(parents=True,exist_ok=True)
    receipt={'schema':'a2-v43-qualification-1','status':'started','exact_commit_qualified':False,
             'development':args.development,'formal_proof_certificate':False,
             'human_specialist_review':False,'commands':[]}
    try:
        if json.loads((ROOT/PINS).read_text())!=manifest:
            raise ValueError('v43 source manifest mismatch; freeze only after editing')
        all_hashes={**current,PACKAGE+'/'+PINS:digest((ROOT/PINS).read_bytes())}
        head=git(repo,'rev-parse','HEAD');receipt['head_sha']=head
        if not args.development:
            if not args.expected_head:raise ValueError('publication requires --expected-head')
            committed(repo,args.expected_head,all_hashes)
            receipt['preserved_trees']=inherited.verify_preserved_trees(repo)
            if git(repo,'rev-parse','HEAD:'+OLD)!=OLD_TREE:
                raise ValueError('the reviewed v42 directory changed')
            receipt['preserved_trees']['retained_v42']=OLD_TREE
            if git(repo,'rev-parse','HEAD^')!=BASE:
                raise ValueError('revision parent is not the controlling review')
            changes=git(repo,'diff','--name-status',BASE,'HEAD').splitlines()
            for change in changes:
                status,name=change.split('\t',1)
                if status!='A' or not (name.startswith(PACKAGE+'/') or name==WORKFLOW):
                    raise ValueError('change outside the new revision scope: '+change)
            receipt['scoped_additions']=len(changes)
        closure=inherited.tex_document_inputs(ROOT)
        texts={name:(ROOT/name).read_bytes().decode() for name in set().union(*map(set,closure.values()))}
        receipt['document_partition']=inherited.verify_document_partition(closure,texts)
        receipt['external_documents']=inherited.verify_external_declarations(ROOT,closure)
        if args.development:
            base_dir=repo/OLD
            old_closure=inherited.tex_document_inputs(base_dir)
            old_texts={n:(base_dir/n).read_bytes().decode() for n in set().union(*map(set,old_closure.values()))}
            receipt['v42_preservation']=inherited.verify_preservation(old_texts,texts)
        else:
            receipt['v42_preservation']=inherited.verify_preservation(read_old(repo,OLD),texts)
            receipt['v41_preservation']=inherited.verify_preservation(read_old(repo,'papers/A2-v41-referee-response'),texts)
            receipt['v40_preservation']=inherited.verify_preservation(inherited.read_reviewed_inputs(repo),texts)
        from verify_v43 import inspect as inspect_contract
        contract=json.loads((ROOT/'JOURNAL_INTERFACE.json').read_text())
        inspect_contract(texts,{n:(ROOT/n).read_bytes() for n in set(texts)|set(contract['journal_front_matter'])},contract)
        receipt['journal_interface_frozen']=True
        inherited.deterministic_zip(out/'A2-v43-repository-source.zip',repo,
                                    {name:(name,h) for name,h in all_hashes.items()})
        inherited.deterministic_zip(out/'A2-v43-journal-source.zip',repo,
                                    {name:(PACKAGE+'/'+name,current[PACKAGE+'/'+name]) for name in sorted(set(texts)|set(contract['journal_front_matter'])|{'JOURNAL_INTERFACE.json','build_journal.sh','verify_package.py'})})
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
        for script in ('verify_v41.py','verify_v42.py','verify_v43.py'):
            normal=run([sys.executable,'tools/'+script],script+'-normal')
            optimized=run([sys.executable,'-O','tools/'+script],script+'-optimized')
            if normal!=optimized:raise ValueError('optimized diagnostics differ')
            result=json.loads(normal)
            if result.get('status')!='passed':raise ValueError('diagnostics did not pass')
            receipt['diagnostics'].append({'script':script,'normal_optimized_identical':True,'result':result})
        run(['pdflatex','--version'],'tex-version')
        run(['latexmk','-v'],'latexmk-version')
        (ROOT/'build').mkdir(exist_ok=True)
        build=Path(tempfile.mkdtemp(prefix='v43-',dir=ROOT/'build'))
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
            target=out/('A2-v43-'+tag+'.pdf');shutil.copyfile(build/(stem+'.pdf'),target)
            for suffix in ('.log','.fls','.aux'):shutil.copyfile(build/(stem+suffix),out/('final-'+stem+suffix))
            receipt['documents'].append({'source':doc,'artifact':target.name,'pages':int(pages[1]),
                'sha256':digest(target.read_bytes()),'final_tex_findings':[],
                'recorded_input_closure':recorded})
        staging=Path(tempfile.mkdtemp(prefix='journal-',dir=ROOT/'build'))
        journal_names=sorted(set(texts)|set(contract['journal_front_matter'])|{'JOURNAL_INTERFACE.json','build_journal.sh','verify_package.py'})
        for name in journal_names:
            target=staging/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        for name in contract['pdf_pair']:
            shutil.copyfile(out/name,staging/name)
        members={str(q.relative_to(staging)):digest(q.read_bytes()) for q in sorted(staging.rglob('*')) if q.is_file()}
        package_manifest={'schema':'a2-v43-journal-package-1','source_commit':head,'source_tree':git(repo,'rev-parse','HEAD^{tree}'),'development':args.development,'pdf_pair':contract['pdf_pair'],'files':members,'human_specialist_review':False}
        (staging/'JOURNAL_PACKAGE.json').write_text(json.dumps(package_manifest,indent=2,sort_keys=True)+'\n')
        members['JOURNAL_PACKAGE.json']=digest((staging/'JOURNAL_PACKAGE.json').read_bytes())
        archive=out/'A2-v43-journal-package.zip'
        inherited.deterministic_zip(archive,staging,{n:(n,h) for n,h in members.items()})
        with zipfile.ZipFile(archive) as check:
            if set(check.namelist())!=set(members):raise ValueError('journal membership differs')
            for name,sha in members.items():
                if digest(check.read(name))!=sha:raise ValueError('journal member mismatch')
            if any(n.startswith('provenance/') for n in check.namelist()):raise ValueError('historical front matter in journal archive')
        check=subprocess.run([sys.executable,str(staging/'verify_package.py')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if check.returncode:raise ValueError('standalone package verification failed: '+check.stdout.decode())
        (out/'verify-package.log').write_bytes(check.stdout)
        receipt['journal_package']={'artifact':archive.name,'sha256':digest(archive.read_bytes()),'members':len(members),'paired_pdfs':True,'current_front_matter_only':True}
        shutil.copyfile(staging/'JOURNAL_PACKAGE.json',out/'JOURNAL_PACKAGE.json')
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
