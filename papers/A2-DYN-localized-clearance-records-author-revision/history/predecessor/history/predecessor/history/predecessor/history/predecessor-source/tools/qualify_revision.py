#!/usr/bin/env python3
"""Execute the exact native revision, retaining actual command and failure receipts."""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,platform,re,shutil,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[1]; B=P/'build/revision'
ENV=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',
         CUA_DD_PYTHON_TOOL_WARM_SPREADSHEET_RUNTIME='false')
PROGRAMS=['check_finite','check_research','check_load','check_clearance','check_critical_coarea',
 'check_two_mark','check_cross_flight','check_angular_source','check_uniform_growth',
 'check_momentum_critical','check_radial_coarea','check_endpoint_localization','check_reflection_resolvent','check_physical_tubes','check_historical_census','check_critical_clock','check_current_census','check_global_variational','check_sublevel','check_summable_source']
DETAILS=PROGRAMS[9:]
def require(ok,message):
    if not ok: raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source():
    manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text())
    seen=set()
    for entry in manifest['files']:
        rel=Path(entry['path']);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe manifest path')
        require(str(rel) not in seen,'duplicate required source');seen.add(str(rel))
        f=P/rel;require(f.is_file(),'missing required source '+str(rel));d=f.read_bytes()
        require(len(d)==entry['bytes'] and hashlib.sha256(d).hexdigest()==entry['sha256'],'source mismatch '+str(rel))
        require(hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==entry['git_blob'],'Git blob mismatch '+str(rel))
    core=sorted(P.glob('core/*.tex'))
    require([int(f.name[:3]) for f in core]==list(range(260,304)),'active native proof chain not exactly 260--303')
    main=(P/'main.tex').read_text()
    for f in core:require(any('\\input{core/'+n+'}' in main for n in [f.name,f.stem]),'main omits native proof '+f.name)
    require(manifest['full_raw_pointwise_LLT_proved'] is False,'unverified target flag')
    preserved=json.loads((P/'PRESERVED_ACTIVE_BODIES.json').read_text())
    for entry in preserved['files']:
        require(digest(P/entry['path'])==entry['sha256'],'changed inherited proof '+entry['path'])
    old=json.loads((P/'INHERITED_FILE_MAP.json').read_text())
    require(old['file_count']==460 and len(old['files'])==460,'incomplete immediate predecessor map')
    for entry in old['files']:
        rel=Path(entry['retained']);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe retained path')
        require(digest(P/rel)==entry['sha256'],'lost predecessor file '+entry['original'])
    full=json.loads((P/'GLOBAL_PREDECESSOR_FILE_MAP.json').read_text())
    require(len(full['files'])==full['file_count'],'incomplete latest predecessor inventory')
    for entry in full['files']:
        require(digest(P/entry['retained'])==entry['sha256'],'lost latest predecessor '+entry['original'])
    for f in sorted((P/'provenance/sublevel-continuation-freeze/core').glob('*.tex')):
        require(digest(f)==digest(P/'core'/f.name),'altered inherited 300--301')
    return {'status':'passed','preserved_latest_predecessor_files':full['file_count'],'required_files':len(seen),'native_core_bodies':len(core),
            'preserved_mathematical_files':len(preserved['files']),'preserved_predecessor_files':460,
            'manifest_sha256':digest(P/'SOURCE_MANIFEST.json')}
def run(cmd,tag):
    B.mkdir(parents=True,exist_ok=True);f=B/(tag+'.log');start=now();t=time.monotonic()
    with f.open('wb') as out:r=subprocess.run([str(x) for x in cmd],cwd=P,env=ENV,stdout=out,stderr=subprocess.STDOUT)
    record={'command':list(map(str,cmd)),'cwd':str(P),'started_utc':start,'completed_utc':now(),
     'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'log':f.name,'log_sha256':digest(f),
     'source_manifest_sha256':digest(P/'SOURCE_MANIFEST.json')}
    (B/(tag+'.command.json')).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    require(r.returncode==0,'command failed; retained '+str(f));return f

def source_phase():
    files=[run([sys.executable]+(['-O'] if opt else [])+['tools/qualify_revision.py','verify'],
               'source-'+('optimized' if opt else 'normal')) for opt in [False,True]]
    require(files[0].read_bytes()==files[1].read_bytes(),'source normal/-O disagreement')
    return json.loads(files[0].read_text())
def command_for(name,opt):
    suffix='optimized' if opt else 'normal'
    cmd=[sys.executable]+(['-O'] if opt else [])+['tools/'+name+'.py']
    if name in DETAILS:cmd+=[('--output' if name=='check_sublevel' else '--details'),str(B/(name+'-cases-'+suffix+'.json'))]
    return cmd,suffix

def verified_log(name,opt):
    cmd,suffix=command_for(name,opt);tag=name+'-'+suffix
    rec=B/(tag+'.command.json');log=B/(tag+'.log')
    require(rec.is_file() and log.is_file(),'missing command receipt '+tag)
    r=json.loads(rec.read_text())
    require(r['exit_code']==0 and r['command']==cmd and r['cwd']==str(P),'command identity/failure '+tag)
    require(r['source_manifest_sha256']==digest(P/'SOURCE_MANIFEST.json') and r['log_sha256']==digest(log),'stale execution '+tag)
    if name in DETAILS:
        detail=B/(name+'-cases-'+suffix+'.json')
        require(detail.is_file() and r.get('detail_sha256')==digest(detail),'missing/stale detailed cases '+tag)
    return log

def check_one(name):
    require(name in PROGRAMS,'unrecognized mathematical program');source()
    for opt in [False,True]:
        cmd,suffix=command_for(name,opt);tag=name+'-'+suffix
        log=run(cmd,tag)
        if name in DETAILS:
            rf=B/(tag+'.command.json');r=json.loads(rf.read_text())
            r['detail_sha256']=digest(B/(name+'-cases-'+suffix+'.json'))
            rf.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    logs=[verified_log(name,opt) for opt in [False,True]]
    require(logs[0].read_bytes()==logs[1].read_bytes(),'normal/-O disagreement '+name)
    if name in DETAILS:require((B/(name+'-cases-normal.json')).read_bytes()==(B/(name+'-cases-optimized.json')).read_bytes(),'raw case disagreement '+name)
    return json.loads(logs[0].read_text())

def seal_checks():
    source();results={}
    for name in PROGRAMS:
        logs=[verified_log(name,opt) for opt in [False,True]]
        require(logs[0].read_bytes()==logs[1].read_bytes(),'normal/-O disagreement '+name)
        if name in DETAILS:require((B/(name+'-cases-normal.json')).read_bytes()==(B/(name+'-cases-optimized.json')).read_bytes(),'raw case disagreement '+name)
        results[name]=json.loads(logs[0].read_text())
    return {'programs':results,'normal_optimized_identical':True,
            'raw_case_sha256':{name:digest(B/(name+'-cases-normal.json')) for name in DETAILS}}

def checks():
    for name in PROGRAMS:check_one(name)
    return seal_checks()
def typeset():
    require(shutil.which('pdflatex') is not None,'missing pdflatex: install TeX Live')
    require(shutil.which('pdfinfo') is not None,'missing pdfinfo: install poppler-utils; remote predecessor failed this precondition')
    dest=B/'native';dest.mkdir(exist_ok=True)
    for i in [1,2,3]:run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape',
              '-file-line-error','-recorder','-output-directory='+str(dest),'main.tex'],'native-pass'+str(i))
    audit=run([sys.executable,'tools/audit_tex.py','--build-dir',str(dest)],'native-audit')
    run([sys.executable,'tools/qualify_revision.py','verify'],'after-build-source')
    return json.loads(audit.read_text())
def phase(name,fn):
    B.mkdir(parents=True,exist_ok=True);f=B/(name+'-phase.json');f.unlink(missing_ok=True)
    start=now();result=fn();obj={'status':'passed','phase':name,'source_manifest_sha256':digest(P/'SOURCE_MANIFEST.json'),
                               'started_utc':start,'completed_utc':now(),'results':result}
    f.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');print('COMPLETED '+name,flush=True)
def finalize():
    # The label index is a derived output, not an input trusted by the source gate.
    index=[]
    for f in sorted(P.glob('core/*.tex'))+sorted(P.glob('*.tex')):
        for line,text in enumerate(f.read_text().splitlines(),1):
            for label in re.findall(r'\\label\{([^}]+)\}',text):
                index.append({'label':label,'path':str(f.relative_to(P)),'line':line})
    (P/'PROOF_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
    run([sys.executable,'tools/qualify_revision.py','verify'],'after-finalization-source')
    mh=digest(P/'SOURCE_MANIFEST.json')
    phases={n:json.loads((B/(n+'-phase.json')).read_text()) for n in ['source','checks','typeset']}
    require(all(v['status']=='passed' and v['source_manifest_sha256']==mh for v in phases.values()),'stale/missing phase')
    import numpy,sympy,scipy
    receipt={'status':'passed','record_kind':'actual native execution; remote CI status requires a separate exact-SHA read',
       'source_manifest_sha256':mh,'completed_utc':now(),'phases':phases,
       'versions':{'python':sys.version,'numpy':numpy.__version__,'sympy':sympy.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
         'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0]},
       'commands':{f.name:json.loads(f.read_text()) for f in sorted(B.glob('*.command.json'))},
       'pdf_sha256':digest(B/'native/main.pdf'),'full_raw_pointwise_LLT_proved':False,
       'four_coordinate_inversion_completed':False,'formal_proof_certificate':False,
       'independent_human_review':False,'remote_CI_success_inferred':False}
    (B/'current-validation.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','pages':phases['typeset']['results']['pages'],'commands':len(receipt['commands']),
        'receipt':str(B/'current-validation.json')},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['all','verify','source','checks','typeset','finalize','check-one','seal-checks'],nargs='?',default='all');ap.add_argument('--program',choices=PROGRAMS);a=ap.parse_args()
    funcs={'source':source_phase,'checks':checks,'typeset':typeset}
    if a.phase=='verify':print(json.dumps(source(),indent=2,sort_keys=True))
    elif a.phase=='all':
        if B.exists():shutil.rmtree(B)
        for name,fn in funcs.items():phase(name,fn)
        finalize()
    elif a.phase=='finalize':finalize()
    elif a.phase=='check-one':print(json.dumps(check_one(a.program),indent=2,sort_keys=True))
    elif a.phase=='seal-checks':phase('checks',seal_checks)
    else:phase(a.phase,funcs[a.phase])
