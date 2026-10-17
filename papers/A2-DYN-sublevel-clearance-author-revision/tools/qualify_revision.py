#!/usr/bin/env python3
"""Fail-closed source, diagnostics and native CONTINUATION build; not the full article."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence'/'current'
BASE='b47b3a86bbd4dda39bf2f0db166626e0102903fd'
PREFIX='papers/A2-DYN-sublevel-clearance-author-revision/'
WORKFLOW='.github/workflows/a2-dyn-sublevel-clearance-20261017.yml'
COMMANDS=[]


def require(ok: bool, text: str):
    if not ok: raise RuntimeError(text)


def sha(data: bytes): return hashlib.sha256(data).hexdigest()


def write_json(name, value):
    (OUT/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')


def command(name, argv, cwd=ROOT):
    start=dt.datetime.now(dt.timezone.utc).isoformat(); clock=time.monotonic()
    proc=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
    log=OUT/(name+'.log');log.write_bytes(proc.stdout)
    record={'name':name,'argv':argv,'cwd':str(cwd),'started_utc':start,'seconds':time.monotonic()-clock,
            'exit_code':proc.returncode,'log':log.name,'log_sha256':sha(proc.stdout)}
    COMMANDS.append(record);write_json('COMMANDS.json',COMMANDS)
    require(proc.returncode==0,'failed command '+name+'; see '+str(log))
    return proc.stdout.decode('utf-8',errors='replace')


def run():
    require(not OUT.exists(),'refuse to overwrite an existing execution directory')
    OUT.mkdir(parents=True)
    result={'status':'started','complete_latest_manuscript_reassembled':False,
            'full_raw_pointwise_LLT_proved':False,'independent_human_audit':False,'formal_proof_certificate':False,
            'scope':'only the new native continuation and its auxiliary diagnostics'}
    try:
        for executable in ('pdflatex','pdfinfo','git'):
            require(shutil.which(executable) is not None,'required executable missing: '+executable)
        result['commit']=command('commit',['git','rev-parse','HEAD']).strip()
        result['tree']=command('tree',['git','rev-parse','HEAD^{tree}']).strip()
        # The exact base is fetched by the workflow. Refuse unscoped modifications.
        diff=command('scope',['git','diff','--name-status',BASE,'HEAD','--']).splitlines()
        for row in diff:
            status,path=row.split('\t',1)
            require(status=='A' and (path.startswith(PREFIX) or path==WORKFLOW),'out-of-scope change '+row)
        result['added_paths']=len(diff)
        command('all-heads',['git','ls-remote','--heads','origin'])
        names=[row.split('\t')[-1] for row in (OUT/'all-heads.log').read_text().splitlines() if 'a2-dyn' in row.lower() or 'a2_dyn' in row.lower()]
        result['named_A2_DYN_heads_at_run']=len(names)
        require((ROOT/'main.tex').is_file(),'native continuation is missing')
        source=[]
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file() or 'evidence' in path.relative_to(ROOT).parts or '__pycache__' in path.parts: continue
            data=path.read_bytes()
            source.append({'path':path.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':sha(data),
                           'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
        expected={'provenance/287-original.tex':'84a26829f33c15506aec1825b2c54ad052707ff7',
                  'provenance/controlling-v115-report.md':'9c68b0e8b31cd196c732514a29ebd44d95964243',
                  'provenance/controlling-v112-report.md':'0ad9f500c92db32ea4fc9f6d9ee28630b4484699'}
        by_path={s['path']:s for s in source}
        for p,blob in expected.items(): require(by_path[p]['git_blob']==blob,'preserved source identity '+p)
        write_json('SOURCE_MANIFEST.json',{'commit':result['commit'],'tree':result['tree'],'files':source,
                                          'complete_local_predecessor_transported':False})
        result['source_manifest_sha256']=sha((OUT/'SOURCE_MANIFEST.json').read_bytes())
        active=['main.tex','retained-geometric-input.tex']+[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'core').glob('*.tex'))]
        labels={}; references=[]
        for name in active:
            for line_no,line in enumerate((ROOT/name).read_text().splitlines(),1):
                for label in re.findall(r'\\label\{([^}]+)\}',line):
                    require(label not in labels,'duplicate native label '+label)
                    labels[label]={'file':name,'line':line_no}
                references.extend(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',line))
        require(all(r in labels for r in references),'missing native cross reference')
        write_json('PROOF_INDEX.json',labels)
        command('python-version',[sys.executable,'--version'])
        command('diagnostics-normal',[sys.executable,'tools/check_sublevel.py','--output',str(OUT/'diagnostics-normal.json')])
        command('diagnostics-optimized',[sys.executable,'-O','tools/check_sublevel.py','--output',str(OUT/'diagnostics-optimized.json')])
        a=(OUT/'diagnostics-normal.json').read_bytes(); b=(OUT/'diagnostics-optimized.json').read_bytes()
        require(a==b,'normal and optimized diagnostics differ')
        result['diagnostics_sha256']=sha(a);result['normal_optimized_identical']=True
        diagnostic=json.loads(a)
        result['real_records']=len(diagnostic['real_records'])
        result['real_flights']=sum(x['flights'] for x in diagnostic['real_records'])
        result['exact_transverse_cases']=diagnostic['exact']['transverse_identity_cases']
        build=OUT/'typeset';build.mkdir()
        command('pdflatex-version',['pdflatex','--version'])
        for i in (1,2,3):
            command('pdflatex-pass'+str(i),['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(build),'main.tex'])
        tex_log=(build/'main.log').read_text(errors='replace')
        forbidden={'undefined':r'(?:Reference|Citation) .* undefined|There were undefined references',
                   'duplicate_labels':r'multiply defined|multiply-defined',
                   'overfull_boxes':r'Overfull \\[hv]box'}
        result['typesetting_audit']={name:len(re.findall(pattern,tex_log)) for name,pattern in forbidden.items()}
        require(all(v==0 for v in result['typesetting_audit'].values()),'native typeset audit failed')
        info=command('pdfinfo',['pdfinfo',str(build/'main.pdf')])
        match=re.search(r'^Pages:\s+(\d+)',info,re.M);require(match is not None,'page count not found')
        result['pages']=int(match.group(1));result['pdf_sha256']=sha((build/'main.pdf').read_bytes())
        result['status']='continuation_source_diagnostics_and_native_build_passed'
    except Exception as exc:
        result['status']='failed';result['error']=repr(exc)
        (OUT/'exception.log').write_text(traceback.format_exc())
        raise
    finally:
        result['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        result['completed_commands']=len(COMMANDS)
        write_json('VALIDATION.json',result)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__': run()
