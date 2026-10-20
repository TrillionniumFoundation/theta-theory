#!/usr/bin/env python3
"""Run actual source checks, diagnostics and native builds with command receipts."""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,platform,shutil,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=P/'build/radial'
ENV=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
PROGRAMS=['check_finite','check_research','check_load','check_clearance','check_critical_coarea',
          'check_two_mark','check_cross_flight','check_angular_source','check_uniform_growth','check_momentum_critical','check_radial_coarea']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(x,m):
    if not x:raise RuntimeError(m)
def run(cmd,tag,cwd=P):
    B.mkdir(parents=True,exist_ok=True);log=B/(tag+'.log');start=now();t=time.monotonic()
    with log.open('wb') as f:r=subprocess.run([str(x) for x in cmd],cwd=cwd,env=ENV,stdout=f,stderr=subprocess.STDOUT)
    record={'command':[str(x) for x in cmd],'cwd':str(cwd),'started_utc':start,'completed_utc':now(),
            'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'log':log.name,'log_sha256':digest(log)}
    (B/(tag+'.command.json')).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    require(r.returncode==0,'command failed; retained log '+str(log))
    return log

def source():
    a=run([sys.executable,'tools/check_radial_source.py'],'source-normal')
    b=run([sys.executable,'-O','tools/check_radial_source.py'],'source-optimized')
    require(a.read_bytes()==b.read_bytes(),'optimized source-check differs')
    return json.loads(a.read_text())
def checks():
    out={}
    for name in PROGRAMS:
        logs=[]
        for optimized in [False,True]:
            cmd=[sys.executable]+(['-O'] if optimized else [])+['tools/'+name+'.py']
            if name in ['check_momentum_critical','check_radial_coarea']:cmd+=['--details',str(B/(name+'-actual-cases'+('-optimized' if optimized else '')+'.json'))]
            logs.append(run(cmd,name+('-optimized' if optimized else '-normal')))
        require(logs[0].read_bytes()==logs[1].read_bytes(),'normal/optimized mismatch '+name)
        out[name]=json.loads(logs[0].read_text())
    for name in ['check_momentum_critical','check_radial_coarea']:
        require((B/(name+'-actual-cases.json')).read_bytes()==(B/(name+'-actual-cases-optimized.json')).read_bytes(),'raw actual-case mismatch '+name)
    return {'programs':out,'normal_optimized_identical':True,'raw_actual_cases_sha256':digest(B/'check_radial_coarea-actual-cases.json')}
def typeset():
    results={}
    for name in ['momentum-baseline','current']:
        src=P if name=='current' else B/'baseline-source'
        target=B/(name+'-typeset');target.mkdir(exist_ok=True)
        if name!='current':
            if src.exists():shutil.rmtree(src)
            src.mkdir()
            for p in P.glob('*.tex'):shutil.copy2(p,src/p.name)
            shutil.copytree(P/'core',src/'core')
            shutil.copy2(P/'provenance/momentum-main.tex',src/'main.tex')
        for i in [1,2,3]:run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                       '-recorder','-output-directory='+str(target),'main.tex'],name+'-pass'+str(i),src)
        audit=run([sys.executable,str(P/'tools/audit_tex.py'),'--build-dir',str(target)],name+'-audit')
        results[name]=json.loads(audit.read_text())
    run([sys.executable,'tools/check_radial_source.py'],'after-build-source')
    return results
def phase(name,fn):
    B.mkdir(parents=True,exist_ok=True);f=B/(name+'-phase.json');f.unlink(missing_ok=True)
    r={'status':'passed','phase':name,'manifest_sha256':digest(P/'SOURCE_MANIFEST.json'),
       'started_utc':now(),'results':fn(),'completed_utc':now()}
    f.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('COMPLETED '+name,flush=True)
def finalize():
    phases={name:json.loads((B/(name+'-phase.json')).read_text()) for name in ['source','checks','typeset']}
    mh=digest(P/'SOURCE_MANIFEST.json')
    require(all(p['status']=='passed' and p['manifest_sha256']==mh for p in phases.values()),'missing/stale qualification phase')
    import numpy,sympy
    receipt={'status':'passed','record_kind':'actual local/native qualification, not remote CI or proof certificate',
       'source_manifest_sha256':mh,'completed_utc':now(),'phases':phases,
       'versions':{'python':sys.version,'numpy':numpy.__version__,'sympy':sympy.__version__,
                   'platform':platform.platform(),'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0]},
       'full_raw_pointwise_LLT_proved':False,'full_four_coordinate_inversion_completed':False,
       'independent_expert_certificate':False,'new_remote_CI_completed_by_this_script':False,
       'commands':{p.name:json.loads(p.read_text()) for p in sorted(B.glob('*.command.json'))},
       'current_pdf_sha256':digest(B/'current-typeset/main.pdf'),
       'baseline_pdf_sha256':digest(B/'momentum-baseline-typeset/main.pdf'),
       'actual_cases_sha256':digest(B/'check_radial_coarea-actual-cases.json')}
    (B/'current-validation.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','pages':phases['typeset']['results']['current']['pages'],
                     'receipt':str(B/'current-validation.json')},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['all','source','checks','typeset','finalize'],default='all',nargs='?');a=ap.parse_args()
    functions={'source':source,'checks':checks,'typeset':typeset}
    if a.phase=='all':
        # A full run never inherits stale phase or command receipts.
        if B.exists():shutil.rmtree(B)
        for name,fn in functions.items():phase(name,fn)
        finalize()
    elif a.phase=='finalize':finalize()
    else:phase(a.phase,functions[a.phase])
