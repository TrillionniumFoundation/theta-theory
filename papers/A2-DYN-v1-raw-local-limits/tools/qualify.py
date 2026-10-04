#!/usr/bin/env python3
"""Exact-source checks, finite evidence and article build; not proof certification."""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACKAGE='papers/A2-DYN-v1-raw-local-limits'
WORKFLOW='.github/workflows/a2-dyn-v1-verify.yml'
BASE='af2390e3073acf8ccd90b10d7566e30cbf18c425'
GEOM='papers/A2-v43-journal-package'
REQUIRED=['prop:marked','lem:winding','prop:lattice','lem:hessian','thm:edge',
          'prop:general-edge','cor:raw-density','cor:nonLone','prop:subtract',
          'thm:LLT','lem:splice','prop:conditioning','prop:clock',
          'lem:covariance','prop:prediction']
EXCLUSIONS={'build','evidence','__pycache__'}

def sha(data):return hashlib.sha256(data).hexdigest()
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
def inventory(workflow):
    result={}
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if set(rel.parts)&EXCLUSIONS or p.suffix=='.pyc':continue
        if p.is_symlink():raise ValueError('source symlink: '+str(rel))
        if p.is_file():result[rel.as_posix()]=p.read_bytes()
    result['workflow.yml']=workflow.read_bytes()
    return result

def tex_inputs(data):
    texts=[];active=set();visiting=set()
    def visit(name):
        if name in visiting:raise ValueError('cyclic TeX input')
        if name in active:return
        if name not in data:raise ValueError('missing TeX input '+name)
        visiting.add(name);text=data[name].decode()
        if re.search(r'\\(?:include|write18|externaldocument)\b',text):raise ValueError('unsupported external input')
        refs=re.findall(r'\\input\{([A-Za-z0-9_./-]+)\}',text)
        if len(refs)!=len(re.findall(r'\\input\b',text)):raise ValueError('nonliteral TeX input')
        texts.append(text)
        for ref in refs:
            target=ref if ref.endswith('.tex') else ref+'.tex'
            if Path(target).is_absolute() or '..' in Path(target).parts:raise ValueError('unsafe TeX input')
            visit(target)
        visiting.remove(name);active.add(name)
    visit('main.tex')
    if active!={n for n in data if n.endswith('.tex')}:raise ValueError('inactive mathematical source')
    return '\n'.join(texts),sorted(active)

def contract(data):
    status=json.loads(data['STATUS.json'])
    for key in ('full_billiard_LLT_verified','A3_full_dependency_released','independent_human_review_completed'):
        if status.get(key) is not False:raise ValueError('unsupported completion claim: '+key)
    if status.get('base_sha')!=BASE:raise ValueError('wrong source base')
    text,active=tex_inputs(data)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    if len(labels)!=len(set(labels)) or set(refs)-set(labels):raise ValueError('label/reference mismatch')
    if not set(REQUIRED)<=set(labels):raise ValueError('missing core result')
    if '\\section{Analytical realization still required}' not in text:raise ValueError('missing realization boundary')
    for name in ('README.md','PROOF_LEDGER.md','SOURCE_AUDIT.md','P0_P5_STATUS.md','LITERATURE_AUDIT.md','SPECIALIST_REVIEW_BRIEF.md','build.sh'):
        if name not in data:raise ValueError('missing journal source '+name)
    return {'active_tex':active,'labels':len(labels),'proof_bodies':text.count('\\begin{proof}'),
            'formal_results':len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}',text)),
            'full_billiard_LLT_verified':False,'independent_human_review_completed':False}

def committed(repo,head,data):
    if not re.fullmatch('[0-9a-f]{40}',head or '') or git(repo,'rev-parse','HEAD')!=head:raise ValueError('wrong exact head')
    subprocess.check_call(['git','-C',str(repo),'merge-base','--is-ancestor',BASE,head])
    changes=git(repo,'diff','--name-status',BASE,head).splitlines()
    if not changes:raise ValueError('empty research diff')
    for row in changes:
        fields=row.split('\t')
        if len(fields)!=2 or fields[0]!='A' or not(fields[1].startswith(PACKAGE+'/') or fields[1]==WORKFLOW):
            raise ValueError('historical or unrelated path changed: '+row)
    entries=git(repo,'ls-tree','-r',head,'--',PACKAGE,WORKFLOW).splitlines()
    expected={WORKFLOW if p=='workflow.yml' else PACKAGE+'/'+p:raw for p,raw in data.items()}
    found=set()
    for row in entries:
        meta,path=row.split('\t',1);mode,kind,blob=meta.split();found.add(path)
        if path not in expected:raise ValueError('unaccounted tracked source '+path)
        raw=expected[path];actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if mode!='100644' or kind!='blob' or actual!=blob:raise ValueError('committed byte mismatch '+path)
    if found!=set(expected):raise ValueError('missing tracked source')
    oldtree=git(repo,'rev-parse',BASE+':'+GEOM)
    if git(repo,'rev-parse',head+':'+GEOM)!=oldtree:raise ValueError('geometric submission changed')
    return {'base_sha':BASE,'geom_tree_preserved':oldtree,'added_files':len(changes),'historical_paths_unchanged':True}

def archive(path,data):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(data.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,raw)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--expected-head');p.add_argument('--development',action='store_true');p.add_argument('--capture-source',action='store_true');p.add_argument('--workflow',type=Path)
    args=p.parse_args();out=ROOT/'evidence';out.mkdir(exist_ok=True)
    receipt={'schema':'a2-dyn-v1-qualification-1','status':'started','exact_commit_qualified':False,
             'full_billiard_LLT_verified':False,'independent_human_review_completed':False,'commands':[]}
    try:
        repo=None
        if args.development:
            if args.workflow is None:raise ValueError('development requires the workflow path')
            workflow=args.workflow;head='development';epoch='1791072000'
        else:
            repo=Path(git(ROOT,'rev-parse','--show-toplevel'));workflow=repo/WORKFLOW;head=args.expected_head
            epoch=git(repo,'show','-s','--format=%ct','HEAD')
        data=inventory(workflow);receipt['head_sha']=head;receipt['source_contract']=contract(data)
        rejected=0
        for key in ('full_billiard_LLT_verified','A3_full_dependency_released','independent_human_review_completed'):
            altered=dict(data);s=json.loads(data['STATUS.json']);s[key]=True;altered['STATUS.json']=json.dumps(s).encode()
            try:contract(altered)
            except ValueError:rejected+=1
            else:raise ValueError('contract accepted unsupported status')
        for name in ('main.tex','PROOF_LEDGER.md','SPECIALIST_REVIEW_BRIEF.md'):
            altered=dict(data);del altered[name]
            try:contract(altered)
            except (ValueError,KeyError):rejected+=1
            else:raise ValueError('contract accepted missing source')
        receipt['negative_contract_cases_rejected']=rejected
        if repo:receipt['preservation']=committed(repo,head,data)
        hashes={n:sha(raw) for n,raw in data.items()}
        (out/'SOURCE_SHA256.json').write_text(json.dumps(hashes,indent=2,sort_keys=True)+'\n')
        archive(out/'A2-DYN-v1-source.zip',data)
        if args.capture_source:receipt['status']='source_captured';return 0
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','LC_ALL':'C','TZ':'UTC','SOURCE_DATE_EPOCH':epoch,'FORCE_SOURCE_DATE':'1'}
        def run(argv,label,timeout=600):
            proc=subprocess.run(argv,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
            (out/(label+'.log')).write_bytes(proc.stdout)
            receipt['commands'].append({'argv':argv,'log':label+'.log','exit_code':proc.returncode})
            if proc.returncode:raise ValueError('failed '+label)
            return proc.stdout
        receipt['finite_evidence']=[]
        for script in ('certify_winding.py','verify.py'):
            normal=run([sys.executable,'tools/'+script],script+'-normal');optimized=run([sys.executable,'-O','tools/'+script],script+'-optimized')
            result=json.loads(normal)
            if normal!=optimized or result.get('status')!='passed':raise ValueError('diagnostic result mismatch')
            (out/(script+'.json')).write_bytes(normal)
            receipt['finite_evidence'].append({'script':script,'normal_optimized_identical':True,'sha256':sha(normal),
                'total_checks':result.get('total_checks'),'rational_slabs':len(result.get('slabs',[]))})
        run(['pdflatex','--version'],'tex-version');run([sys.executable,'--version'],'python-version')
        (ROOT/'build').mkdir(exist_ok=True);build=Path(tempfile.mkdtemp(prefix='qualified-',dir=ROOT/'build'))
        run(['latexmk','-pdf','-g','-interaction=nonstopmode','-halt-on-error','-file-line-error','-latexoption=-no-shell-escape','-outdir='+str(build),'main.tex'],'article-build')
        log=(build/'main.log').read_text(errors='replace')
        findings=[line for line in log.splitlines() if re.search(r'Warning|Overfull|Underfull|^!',line)]
        if findings:raise ValueError('final TeX findings: '+repr(findings))
        info=run(['pdfinfo',str(build/'main.pdf')],'pdfinfo').decode();m=re.search(r'^Pages:\s+(\d+)',info,re.M)
        if not m:raise ValueError('missing page count')
        pdf=(build/'main.pdf').read_bytes();(out/'A2-DYN-v1-primary.pdf').write_bytes(pdf)
        for ext in ('log','fls','aux'):shutil.copyfile(build/('main.'+ext),out/('final-main.'+ext))
        if inventory(workflow)!=data:raise ValueError('source changed during qualification')
        if repo:committed(repo,head,data)
        receipt['document']={'pages':int(m[1]),'sha256':sha(pdf),'final_tex_findings':[]}
        package=dict(data);package['A2-DYN-v1-primary.pdf']=pdf
        package['SOURCE_COMMIT.txt']=(str(head)+'\n').encode()
        for name in ('SOURCE_SHA256.json','certify_winding.py.json','verify.py.json'):
            package['evidence/'+name]=(out/name).read_bytes()
        package['MANIFEST.json']=(json.dumps({n:sha(raw) for n,raw in package.items()},indent=2,sort_keys=True)+'\n').encode()
        archive(out/'A2-DYN-v1-research-package.zip',package)
        receipt['source_unchanged']=True;receipt['exact_commit_qualified']=not args.development;receipt['status']='passed';return 0
    except Exception as e:
        receipt['status']='failed';receipt['error']=str(e);print(str(e),file=sys.stderr);return 1
    finally:
        receipt['artifacts']={p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file() and p.name!='receipt.json'}
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'status':receipt['status'],'receipt':str(out/'receipt.json')}))
if __name__=='__main__':sys.exit(main())
