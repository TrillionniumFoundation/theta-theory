#!/usr/bin/env python3
"""Verify pinned baseline bytes and rebuild native TeX outside the old article."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, shutil, stat, subprocess, sys

WORK = Path('/workspace/scratch/b5cc344d4c8e')
AUDIT = WORK / 'iteration-20261019b/source-audit'
ARTICLE = WORK / 'theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision'
PIN = WORK / 'iteration-20261019/C3_FILE_IDENTITIES.json'
COMMIT = 'fdf2603c8bf422314f199fa431086485a0d1ebb5'
ROOT = 'd90e88848644a25b2d9f2e3a28383f4908d2a646'
TREE = 'f5c90ecd279dd116330c5d90fa31cae2b0d6f61e'


def now():
    return datetime.now(timezone.utc).isoformat()


def blob(body):
    return hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def identity(path):
    before = path.stat()
    body = path.read_bytes()
    after = path.stat()
    if (before.st_size,before.st_mtime_ns,before.st_ino) != (after.st_size,after.st_mtime_ns,after.st_ino):
        raise ValueError('Concurrent file mutation: ' + str(path))
    if not stat.S_ISREG(after.st_mode):
        raise ValueError('Not a regular file: ' + str(path))
    return {'sha':blob(body),'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),
            'mode':'100755' if after.st_mode & 0o111 else '100644','type':'blob'}


def scan(rows):
    result=[]
    for row in rows:
        actual=identity(ARTICLE/row['path'])
        expected={k:row[k] for k in ('sha','sha256','bytes','mode','type')}
        result.append({'path':row['path'],'expected':expected,'actual':actual,'matches':actual==expected})
    return result


def run(argv, basename, cwd=ARTICLE):
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    started=now()
    with (AUDIT/(basename+'.stdout.txt')).open('wb') as stdout, (AUDIT/(basename+'.stderr.txt')).open('wb') as stderr:
        proc=subprocess.run(argv,cwd=cwd,stdout=stdout,stderr=stderr,env=env,check=False)
    receipt={'argv':argv,'cwd':str(cwd),'started_utc':started,'finished_utc':now(),'exit_code':proc.returncode,
             'stdout':basename+'.stdout.txt','stderr':basename+'.stderr.txt'}
    if proc.returncode:
        (AUDIT/'FAILED_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        raise RuntimeError('Baseline command failed; actual failure retained: '+basename)
    return receipt


def main():
    started=now();AUDIT.mkdir(parents=True,exist_ok=True)
    expected=json.loads(PIN.read_text())
    if expected['article_tree_sha']!=TREE or len(expected['files'])!=2088:
        raise ValueError('Wrong baseline source identity')
    shutil.copyfile(PIN,AUDIT/'BASELINE_EXPECTED_FILE_IDENTITIES.json')
    before=scan(expected['files'])
    if any(not row['matches'] for row in before):
        (AUDIT/'BASELINE_LOCAL_MISMATCHES.json').write_text(json.dumps(before,indent=2)+'\n')
        raise ValueError('Pinned baseline byte mismatch')
    full={'observed_utc':now(),'commit':COMMIT,'root_tree':ROOT,'article_tree':TREE,'file_count':len(before),
          'bytes':sum(row['expected']['bytes'] for row in before),'all_match':True,'files':before}
    (AUDIT/'BASELINE_LOCAL_REMOTE_BYTE_VERIFICATION.json').write_text(json.dumps(full,indent=2)+'\n')
    source_checks=[]
    for phase in ('history','verify'):
        source_checks.append(run([sys.executable,'tools/package_source_manifest.py','.',phase],'baseline-'+phase))
    (AUDIT/'BASELINE_MANIFEST_HISTORY_EXECUTION.json').write_text(json.dumps({'started_utc':started,'finished_utc':now(),
        'scope':'Read-only verification of current manifest and both fixed history anchors; no freeze and no mathematical execution',
        'commands':source_checks},indent=2)+'\n')
    build=AUDIT/'baseline-build';build.mkdir(exist_ok=True)
    version=run(['pdflatex','--version'],'baseline-build/pdflatex-version')
    commands=[]
    for number in range(1,4):
        commands.append(run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                             '-recorder','-output-directory='+str(build),'main.tex'],'baseline-build/pass'+str(number)))
    commands.append(run(['pdfinfo',str(build/'main.pdf')],'baseline-build/pdfinfo'))
    commands.append(run(['pdftotext','-layout',str(build/'main.pdf'),str(build/'main.txt')],'baseline-build/pdftotext'))
    info=(build/'pdfinfo.stdout.txt').read_text();match=re.search(r'^Pages:\s*(\d+)',info,re.M)
    if not match:raise ValueError('No actual PDF page count')
    log=(build/'main.log').read_text(errors='replace')
    patterns={'undefined_references':r'There were undefined references|Reference .* undefined|Citation .* undefined',
              'duplicate_destinations':r'destination with the same identifier',
              'overfull_boxes':r'Overfull \\[hv]box',
              'missing_glyphs':r'Missing character:',
              'latex_errors':r'^!|LaTeX Error|Emergency stop|Fatal error'}
    diagnostics={name:re.findall(pattern,log,re.M) for name,pattern in patterns.items()}
    advisories=[line.strip() for line in log.splitlines() if 'Warning:' in line]
    if any(diagnostics.values()):
        (build/'DIAGNOSTICS.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
        raise ValueError('Baseline build has an unresolved blocking diagnostic')
    manifest=json.loads((ARTICLE/'SOURCE_MANIFEST.json').read_text())
    tex_paths=manifest['native_tex_closure']['reachable_tex_files']
    fls=(build/'main.fls').read_text(errors='replace')
    observed=set()
    for line in fls.splitlines():
        if line.startswith('INPUT '):
            path=Path(line[6:]);path=(ARTICLE/path).resolve() if not path.is_absolute() else path.resolve()
            if ARTICLE in path.parents and path.suffix=='.tex':observed.add(path.relative_to(ARTICLE).as_posix())
    missing=sorted(set(tex_paths)-observed)
    if missing:raise ValueError('Declared native source not observed in actual TeX recorder: '+str(missing))
    after=scan(expected['files'])
    if any(not row['matches'] for row in after):raise ValueError('Existing article changed during isolated rebuild')
    receipt={'status':'passed','started_utc':started,'finished_utc':now(),'commit':COMMIT,'root_tree':ROOT,'article_tree':TREE,
             'scope':'Actual current native baseline rebuild and source-preservation checks; not a continuum theorem certificate or new CI run',
             'before_and_after_published_files_unchanged':2088,'main_source':identity(ARTICLE/'main.tex'),
             'source_manifest':identity(ARTICLE/'SOURCE_MANIFEST.json'),'frozen_input_count':manifest['source_count'],
             'frozen_input_bytes':manifest['source_bytes'],'native_tex_paths':tex_paths,'native_tex_count':len(tex_paths),
             'active_core_files':manifest['native_tex_closure']['active_core_files'],'tex_recorder_observed_native_paths':sorted(observed),
             'missing_native_tex_in_actual_recorder':missing,'pdflatex_version_command':version,'commands':commands,
             'pages':int(match.group(1)),'pdf':identity(build/'main.pdf'),'aux':identity(build/'main.aux'),
             'blocking_diagnostics':diagnostics,'advisories':advisories,'mathematical_validation_rerun':False}
    (build/'REBUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('status','commit','article_tree','pages','native_tex_count','before_and_after_published_files_unchanged','finished_utc')},sort_keys=True))


if __name__=='__main__':main()
