#!/usr/bin/env python3
"""Source-bound native paired builds and finite diagnostics, not formal proof."""
from __future__ import annotations
import argparse,hashlib,json,os,platform,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_tree(path: Path) -> str:
    payload=b''
    for item in sorted(path.iterdir(),key=lambda f:(f.name+('/' if f.is_dir() else '')).encode()):
        if item.name in ('__pycache__','.git'):continue
        if item.is_symlink():raise RuntimeError('Source symlinks are not permitted')
        if item.is_dir():mode='40000';sha=git_tree(item)
        else:
            mode='100644';raw=item.read_bytes()
            sha=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
        payload+=f'{mode} {item.name}'.encode()+b'\0'+bytes.fromhex(sha)
    return hashlib.sha1(f'tree {len(payload)}\0'.encode()+payload).hexdigest()

def run(command,cwd,log,env):
    with Path(log).open('wb') as stream:
        result=subprocess.run(command,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError(f'Command failed ({result.returncode}): {command}; see {log}')

def git_blob(path: Path) -> str:
    raw=path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()

def current_files():
    return {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
            if p.is_file() and p.relative_to(ROOT).parts[0]!='retained'
            and '__pycache__' not in p.parts and '.git' not in p.relative_to(ROOT).parts}

def verify_source():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    if manifest['schema']!='theta.r72.exact-source-manifest.v1':
        raise RuntimeError('Unexpected source manifest schema')
    expected={r['path']:r for r in manifest['files']}
    if current_files()!=set(expected)|{'SOURCE_MANIFEST.json'}:
        raise RuntimeError('Unlisted or missing current source files')
    for relative,row in expected.items():
        path=ROOT/relative
        if path.is_symlink() or digest(path)!=row['sha256'] or git_blob(path)!=row['git_blob']:
            raise RuntimeError('Current source identity mismatch: '+relative)
    retained_paths=set()
    for row in manifest['retained_trees']:
        path=ROOT/row['path'];retained_paths.add(path.name)
        if not path.is_dir() or git_tree(path)!=row['git_tree']:
            raise RuntimeError('Retained tree identity mismatch: '+row['path'])
    if {p.name for p in (ROOT/'retained').iterdir()}!=retained_paths:
        raise RuntimeError('Unlisted retained root')
    base=ROOT/'retained/r71-native'
    bodies=manifest['unchanged_current_theorem_bodies']
    for relative in bodies:
        if (ROOT/relative).read_bytes()!=(base/relative).read_bytes():
            raise RuntimeError('Inherited current theorem body changed: '+relative)
    count=sum(1 for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
              and '.git' not in p.relative_to(ROOT).parts)
    return count,manifest

def cross_labels(build: Path,name: str):
    # AMS writes non-reference tocindent dimensions through newlabel too; do not import them.
    lines=(build/(name+'.aux')).read_text().splitlines()
    keep=[x for x in lines if x.startswith(r'\newlabel{') and not x.startswith(r'\newlabel{tocindent')]
    (build/(name+'-refs.aux')).write_text('\n'.join(keep)+'\n')

def resolved(build: Path,name: str):
    text=(build/(name+'.aux')).read_text()
    return {a:(b,c) for a,b,c in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',text)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--source-commit',default='local-source-not-yet-committed')
    args=ap.parse_args();out=args.out.resolve()
    if out==ROOT or ROOT in out.parents:raise ValueError('Build output must be outside the immutable source')
    out.mkdir(parents=True,exist_ok=True)
    for tool in ('pdflatex','pdftotext','pdfinfo'):
        if not shutil.which(tool):raise RuntimeError(f'Missing native tool {tool}')
    file_count,manifest=verify_source();before=git_tree(ROOT)
    r66=json.loads((ROOT/'provenance/BASELINE_R67.json').read_text())['complete_native_mathematical_closure']
    for row in r66['files']:
        raw=(ROOT/'retained/r70-native'/r66['local_path']/row['path']).read_bytes()
        if hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!=row['git_blob']:
            raise RuntimeError('Retained R66 native input mismatch: '+row['path'])
    raw=(ROOT/'diagnostics_r66.py').read_bytes()
    if hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!='142b5a71eeccf559611b731d53479e6c69a5b75a':
        raise RuntimeError('Inherited R66 diagnostic source mismatch')
    inherited_reports={'R59_REFEREE_REPORT.md':'0f25939c7028ef09519f82ca67eef92852444985',
        'R59_ROUND2_REFEREE_REPORT.md':'d853a5196f0f67ffbdcba49e78246437cc6d6a1c',
        'R59_ROUND3_REFEREE_REPORT.md':'eb9e20db36ae1297f4ee13369be8460e786d7546'}
    for name,expected in inherited_reports.items():
        raw=(ROOT/'inputs/review'/name).read_bytes()
        if hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!=expected:raise RuntimeError(f'Review bytes differ: {name}')
    review=json.loads((ROOT/'inputs/review/R65_REFEREE_REFERENCE.json').read_text())
    if review['commit']!='358481b21ceeeedb1205ebd30f86982e32a2cb04' or review['git_blob']!='d1ff9c5662390156ee212c82b173e86a21180e84':
        raise RuntimeError('Controlling R65 review pointer differs')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
             PYTHONDONTWRITEBYTECODE='1',SOURCE_DATE_EPOCH='1792022400')
    diagnostics={}
    for name,file in [('r61','diagnostics.py'),('r62','diagnostics_r62.py'),('r63','diagnostics_r63.py'),('r64','diagnostics_r64.py'),('r65','diagnostics_r65.py'),('r66','diagnostics_r66.py'),('r67','diagnostics_r67.py'),('r68','diagnostics_r68.py'),('r69','diagnostics_r69.py'),('r70','diagnostics_r70.py'),('r71','diagnostics_r71.py'),('r72','diagnostics_r72.py')]:
        normal=out/f'{name}-normal.json';optimized=out/f'{name}-optimized.json'
        run([sys.executable,file],ROOT,normal,env);run([sys.executable,'-O',file],ROOT,optimized,env)
        if normal.read_bytes()!=optimized.read_bytes():raise RuntimeError(f'Normal/optimized mismatch: {name}')
        diagnostics[name]=json.loads(normal.read_text())
    paired=out/'paired';paired.mkdir(exist_ok=True)
    pairenv=dict(env,TEXINPUTS=str(paired)+os.pathsep+env.get('TEXINPUTS',''))
    commands={}
    for n in range(1,4):
        for name in ('main','supplement'):
            cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','-recorder',f'-output-directory={paired}',name+'.tex']
            run(cmd,ROOT,paired/f'{name}-pass-{n}.txt',pairenv);cross_labels(paired,name);commands[name]=cmd
    companion=out/'companion';companion.mkdir(exist_ok=True)
    ccwd=ROOT/'retained/r58-native'
    ccmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','-recorder',f'-output-directory={companion}','main.tex']
    for n in range(1,4):run(ccmd,ccwd,companion/f'pass-{n}.txt',env)
    labels={'main':resolved(paired,'main'),'supplement':resolved(paired,'supplement')}
    statement_map=json.loads((ROOT/'THEOREM_INDEX.json').read_text())
    for item in statement_map['statements']:
        got=labels[item['document']].get(item['label'])
        if got!=(item['number'],str(item['page'])):raise RuntimeError(f'Theorem map mismatch: {item["label"]} -> {got}')
    docs=[]
    for key,build,stem,filename,cmd in [
        ('manuscript',paired,'main','General_Theta_Foundations_I_R72.pdf',commands['main']),
        ('supplement',paired,'supplement','General_Theta_Foundations_I_R72_Supplement.pdf',commands['supplement']),
        ('companion',companion,'main','General_Theta_Foundations_I_R72_Retained_Companion_R58.pdf',ccmd)]:
        log=(build/(stem+'.log')).read_text(errors='replace')
        bad=[x for x in ('undefined references','undefined citations','multiply defined',r'Overfull \hbox',r'Overfull \vbox') if x in log]
        if bad:raise RuntimeError(f'Final native warnings in {key}: {bad}')
        pdf=out/filename;shutil.copyfile(build/(stem+'.pdf'),pdf)
        txt=out/(Path(filename).stem+'.txt')
        run(['pdftotext','-layout',str(pdf),str(txt)],ROOT,build/(stem+'-pdftotext.txt'),env)
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        (build/(stem+'-pdfinfo.txt')).write_text(info)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        docs.append({'document':key,'file':filename,'pages':pages,'sha256':digest(pdf),'text_sha256':digest(txt),'passes':3,'command':cmd})
    verify_source()
    if git_tree(ROOT)!=before:raise RuntimeError('Source mutated during verification')
    checkout=None
    try:checkout=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except (FileNotFoundError,subprocess.CalledProcessError):pass
    if checkout and not args.source_commit.startswith('local-') and checkout!=args.source_commit:raise RuntimeError('Checkout SHA mismatch')
    checkout_subtree=None
    if checkout:
        prefix=subprocess.check_output(['git','rev-parse','--show-prefix'],cwd=ROOT,text=True).strip().rstrip('/')
        object_spec=checkout+(':'+prefix if prefix else '^{tree}')
        checkout_subtree=subprocess.check_output(['git','rev-parse',object_spec],cwd=ROOT,text=True).strip()
        if checkout_subtree!=before:raise RuntimeError('Checked-out commit does not contain the verified source tree')
    receipt={'schema':'theta.r72.native-verification.v1','status':'PASS','declared_source_commit':args.source_commit,
        'checkout_head_verified':checkout,'checkout_paper_tree_verified':checkout_subtree,'source_git_tree':before,'source_manifest_sha256':digest(ROOT/'SOURCE_MANIFEST.json'),
        'source_files_verified':file_count,'inherited_review_bodies_verified':inherited_reports,
        'controlling_review_reference':{'commit':review['commit'],'blob':review['git_blob'],'local_body_verified':False},
        'documents':docs,'diagnostics':diagnostics,'ordinary_optimized_identity':True,
        'total_checks':sum(r['total_checks'] for r in diagnostics.values()),
        'exact_finite_checks':sum(sum(v for k,v in r['checks_by_group'].items() if k.startswith('exact')) for r in diagnostics.values()),
        'floating_finite_checks':sum(sum(v for k,v in r['checks_by_group'].items() if k.startswith('float')) for r in diagnostics.values()),
        'theorem_entries_verified':len(statement_map['statements']),'python':sys.version,'platform':platform.platform(),
        'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'limitations':'Native source reproducibility and finite exact/floating checks, not formal proof, human review, exhaustive priority or editorial acceptance. When checkout_head_verified is null, source identity is its recomputed Git tree, not a local checkout. The controlling R65 report is pinned and read remotely; this build verifies its pointer and does not claim local body verification or remote publication. Retained historical report bodies have their separate hash checks. Remote CI requires its own actual matching SHA and status.'}
    (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','documents':docs,'checks':receipt['total_checks'],'source_tree':before},indent=2))
if __name__=='__main__':main()
