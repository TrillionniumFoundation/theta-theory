#!/usr/bin/env python3
"""Verify identities, execute finite mathematics checks, and compile native TeX.

This program is a reproducibility instrument, not a continuous-dynamics proof.
It never promotes CI success to a completed raw local limit theorem.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, platform, re, subprocess, sys, tarfile, time

ROOT = Path(__file__).resolve().parents[1]

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def require(condition, message):
    if not condition: raise RuntimeError(message)
def write(path, value): path.write_text(json.dumps(value,indent=2)+'\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def source_checks(output):
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    excluded={'SOURCE_MANIFEST.json','PUBLICATION_STATUS.json','VALIDATION_REPORT.md'}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and p.relative_to(ROOT).parts[0] not in {'build','evidence'}
            and p.relative_to(ROOT).as_posix() not in excluded and '__pycache__' not in p.parts}
    require(actual=={r['path'] for r in manifest['files']},'Incomplete or stale manifest file set')
    for row in manifest['files']:
        p=ROOT/row['path']; require(p.is_file(), 'Missing '+row['path'])
        data=p.read_bytes()
        require(len(data)==row['bytes'] and digest(p)==row['sha256'] and blob(data)==row['git_blob'],
                'Manifest mismatch '+row['path'])
    native=[r for r in manifest['files'] if r['path'].endswith('.tex') and not r['path'].startswith('history/')]
    payload=''.join(r['path']+'\0'+r['sha256']+'\n' for r in native).encode()
    require(hashlib.sha256(payload).hexdigest()==manifest['mathematical_source_sha256'],'Native source hash mismatch')
    inherited=json.loads((ROOT/'audit/INHERITED_ACTIVE_SOURCE_IDENTITIES.json').read_text())
    for row in inherited:
        p=ROOT/row['preserved_copy'];require(digest(p)==row['sha256'],'Lost preserved predecessor '+row['path'])
        if row['active_byte_identical']:
            require(digest(ROOT/row['path'])==row['sha256'],'Modified inherited proof '+row['path'])
    immediate=json.loads((ROOT/'audit/IMMEDIATE_PREDECESSOR_FILE_IDENTITIES.json').read_text())
    for row in immediate:
        data=(ROOT/row['preserved_copy']).read_bytes()
        require(hashlib.sha256(data).hexdigest()==row['sha256'] and blob(data)==row['git_blob'],
                'Lost immediate predecessor file '+row['path'])
        if row['active_byte_identical']:
            require(digest(ROOT/row['path'])==row['sha256'],'Modified immediate predecessor '+row['path'])
    current_native=[r for r in immediate if r['path'].endswith('.tex') and not r['path'].startswith('history/')]
    require(len(current_native)==87,'Immediate predecessor native identity set incomplete')
    require(all(r['active_byte_identical'] for r in current_native if r['path'].startswith('core/')),
            'An inherited native proof body was changed')
    expected={r['oid']:r for r in json.loads((ROOT/'audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json').read_text())}
    seen=set(); total=0
    with tarfile.open(ROOT/'history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz','r:gz') as tf:
        for member in tf:
            require(member.isfile() and re.fullmatch(r'[0-9a-f]{40}\.tex',member.name) is not None,'Unexpected historical member')
            data=tf.extractfile(member).read(); oid=member.name[:-4]
            require(oid in expected and oid not in seen,'Duplicate or unknown native source')
            row=expected[oid]
            require(blob(data)==oid and hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'],'Historical blob identity mismatch '+oid)
            seen.add(oid);total+=len(data)
    require(seen==set(expected) and len(seen)==660,'Incomplete historical native archive')
    report=(ROOT/'history/reviews/CONTROLLING_V115_REPORT.md').read_bytes()
    require(blob(report)==manifest['controlling_report_blob'],'Controlling report copy is not exact')
    closure=[]; visited=set()
    def visit(rel):
        require(rel not in visited,'Repeated or cyclic native input '+rel)
        visited.add(rel);p=ROOT/rel; require(p.is_file(),'Missing native input '+rel);closure.append(rel)
        for name in re.findall(r'\\(?:input|include)\{([^}]+)\}',p.read_text()):
            require('..' not in Path(name).parts and not Path(name).is_absolute(),'External native input '+name)
            visit(name if name.endswith('.tex') else name+'.tex')
    visit('main.tex')
    source='\n'.join((ROOT/p).read_text() for p in closure)
    labels=re.findall(r'\\label\{([^}]+)\}',source)
    require(len(labels)==len(set(labels)),'Duplicate native theorem/equation labels')
    references=re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}',source)
    require(not (set(references)-set(labels)),'Undefined native references '+str(sorted(set(references)-set(labels))))
    active_cores=sorted(p for p in closure if p.startswith('core/'))
    require(len(active_cores)==78,'Expected all 76 inherited and two new continuation core files')
    require(all(any(p.startswith('core/'+str(i)+'_') for p in active_cores) for i in range(260,338)),'Missing proof body in 260--337')
    require(len(closure)==90 and set(closure)=={r['path'] for r in native},'Unexpected or unused active native input')
    census_result=output/'source-census.results.json'
    census_receipt=execute([sys.executable,'-B',str(ROOT/'tools/verify_source_census.py'),
                            '--output',str(census_result)],'verify_source_census',output)
    census=json.loads(census_result.read_text())
    require(census.get('status') in ['PASS','passed'],'Failed portable source census')
    result={'status':'passed','manifest_files':len(manifest['files']), 'native_closure_files':len(closure),
            'native_core_files':len(active_cores),'labels':len(labels),'inherited_active_files_unchanged':sum(r['active_byte_identical'] for r in inherited),
            'historical_native_objects_verified':len(seen),'historical_native_bytes':total,
            'mathematical_source_sha256':manifest['mathematical_source_sha256'], 'native_closure':closure,
            'immediate_predecessor_files_verified':len(immediate),
            'immediate_predecessor_native_files_unchanged':sum(r['active_byte_identical'] for r in current_native),
            'immediate_predecessor_core_files_unchanged':sum(r['active_byte_identical'] for r in current_native if r['path'].startswith('core/')),
            'source_census_receipt':census_receipt,
            'source_census_result_sha256':digest(census_result),
            'scope':'Exact identity and dependency checks; no inference of mathematical correctness.'}
    write(output/'source-checks.json',result);return result

def execute(command,name,output):
    start=utc(); t=time.monotonic()
    env=os.environ.copy();env.update({'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
    env.pop('PYTHONOPTIMIZE',None)
    proc=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    log=output/(name+'.log');log.write_text(proc.stdout)
    receipt={'command':command,'cwd':str(ROOT),'started_utc':start,'finished_utc':utc(),
             'elapsed_seconds':time.monotonic()-t,'exit_code':proc.returncode,'log_sha256':digest(log)}
    write(output/(name+'.command.json'),receipt)
    require(proc.returncode==0,name+' failed; see '+str(log))
    return receipt

def mathematics(output):
    scripts=['verify_section_constants.py','verify_exact_interval_inversion.py','verify_endpoint_kernel_algebra.py','check_historical_analytic_arithmetic.py','verify_physical_sbv.py','verify_roof_jump_spectrum.py']
    results=[]
    for script in scripts:
        name=script[:-3];result=output/(name+'.results.json')
        receipt=execute([sys.executable,'-B',str(ROOT/'tools'/script),'--output',str(result)],name,output)
        value=json.loads(result.read_text())
        require(value.get('status') in ['PASS','passed'] or value.get('all_passed') is True,'Failed mathematical program '+script)
        results.append({'script':script,'script_sha256':digest(ROOT/'tools'/script),'receipt':receipt,'result':value})
    combined={'status':'passed','executions':len(results),'python_optimization':0,
              'scope':'Finite exact arithmetic, symbolic formulae and high-precision examples only; proof bodies carry continuum assertions.',
              'results':results}
    write(output/'mathematical-checks.json',combined);return combined

def typeset(output,closure):
    native=output/'native';native.mkdir(parents=True,exist_ok=True)
    receipts=[]
    for passnum in range(1,4):
        receipts.append(execute(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(native),'main.tex'], 'pdflatex-pass-'+str(passnum),output))
    log=(native/'main.log').read_text(errors='replace')
    forbidden=['LaTeX Warning: There were undefined references','LaTeX Warning: Label(s) may have changed','multiply defined','Missing character:','Overfull \\hbox','Overfull \\vbox']
    found=[s for s in forbidden if s in log]
    require(not found,'Unresolved native typesetting diagnostics: '+str(found))
    inputs=set()
    for line in (native/'main.fls').read_text().splitlines():
        if line.startswith('INPUT '):
            p=Path(line[6:]);p=(ROOT/p).resolve() if not p.is_absolute() else p.resolve()
            try:rel=p.relative_to(ROOT).as_posix()
            except ValueError:continue
            if rel.endswith('.tex'):inputs.add(rel)
    require(inputs==set(closure),'Actual TeX recorder/native closure disagreement '+str(inputs.symmetric_difference(closure)))
    execute(['pdftotext','-layout',str(native/'main.pdf'),str(native/'main.txt')],'pdftotext',output)
    from pypdf import PdfReader
    reader=PdfReader(native/'main.pdf')
    aux=(native/'main.aux').read_text()
    labels={m.group(1):{'number':m.group(2),'page':m.group(3)} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux)}
    continuation_labels=set()
    for number in [336,337]:
        paths=list((ROOT/'core').glob(str(number)+'_*.tex'))
        require(len(paths)==1,'Ambiguous continuation module '+str(number))
        continuation_labels.update(re.findall(r'\\label\{([^}]+)\}',paths[0].read_text()))
    proofindex={'labels':labels,'new_module_labels':{k:v for k,v in labels.items() if k in continuation_labels}}
    write(output/'PROOF_INDEX.json',proofindex)
    result={'status':'passed','pages':len(reader.pages),'pdf_sha256':digest(native/'main.pdf'),
            'recorded_native_inputs':len(inputs),'passes':receipts,'forbidden_diagnostics':found,
            'visual_review':'Separate visual QA record; this automated phase does not claim visual inspection.'}
    write(output/'native-typeset.json',result);return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'build/current')
    parser.add_argument('--phase',choices=['all','source','math','native'],default='all')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    require(sys.flags.optimize==0,'Run validation without -O; auxiliary scripts use assertions.')
    summary={'started_utc':utc(),'python':sys.version,'platform':platform.platform(),'phase':args.phase,
             'status':'running','raw_pointwise_theorem_complete':False,'full_four_coordinate_inverse_complete':False}
    try:
        summary['source']=source_checks(out)
        if args.phase in ['all','math']:summary['mathematics']=mathematics(out)
        if args.phase in ['all','native']:summary['native']=typeset(out,summary['source']['native_closure'])
        summary['status']='passed'
    except Exception as exc:
        summary['status']='failed';summary['error']=repr(exc);raise
    finally:
        summary['finished_utc']=utc();write(out/'VALIDATION_SUMMARY.json',summary)
        print(json.dumps({k:summary[k] for k in ['status','phase','started_utc','finished_utc']},indent=2))

if __name__=='__main__':main()
