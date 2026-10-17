#!/usr/bin/env python3
"""Read-only native builds and finite diagnostics; not a proof certificate."""
from __future__ import annotations
import argparse,hashlib,json,os,platform,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run(command,cwd,log,env):
    with Path(log).open('wb') as f:
        result=subprocess.run(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError(f'Command failed: {command}; see {log}')

def git_tree(path):
    payload=b''
    for item in sorted(path.iterdir(),key=lambda f:(f.name+('/' if f.is_dir() else '')).encode()):
        if item.name=='__pycache__':continue
        if item.is_symlink():raise RuntimeError('Symlinks not permitted in this source manifest')
        if item.is_dir():mode='40000';sha=git_tree(item)
        else:
            mode='100644';raw=item.read_bytes()
            sha=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
        payload+=f'{mode} {item.name}'.encode()+b'\0'+bytes.fromhex(sha)
    return hashlib.sha1(f'tree {len(payload)}\0'.encode()+payload).hexdigest()

def verify_source():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    base=ROOT/manifest['inherited_tree']['path']
    if git_tree(base)!=manifest['inherited_tree']['git_tree']:
        raise RuntimeError('Retained R62 source tree differs from its locked Git object')
    expected={str(f.relative_to(base)):digest(f) for f in base.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
    expected.pop('SOURCE_MANIFEST.json')
    expected.update({r['path']:r['sha256'] for r in manifest['overrides']})
    for relative,sha in expected.items():
        file=ROOT/relative
        if not file.is_file() or file.is_symlink() or digest(file)!=sha:
            raise RuntimeError(f'Source mismatch: {relative}')
    retained={str(f.relative_to(ROOT)) for f in base.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
    actual={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
    if actual!=set(expected)|retained|{'SOURCE_MANIFEST.json'}:
        raise RuntimeError('Unexpected or missing source paths')
    return manifest,expected,len(actual)-1

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--source-commit',default='local-source-not-yet-committed')
    args=ap.parse_args();out=args.out.resolve()
    if out==ROOT or ROOT in out.parents: raise ValueError('Output must be outside the source tree')
    out.mkdir(parents=True,exist_ok=True)
    for tool in ('pdflatex','pdftotext','pdfinfo'):
        if not shutil.which(tool):raise RuntimeError(f'Missing required tool {tool}')
    manifest,expected,file_count=verify_source()
    report=ROOT/'inputs/review/R59_REFEREE_REPORT.md'
    raw=report.read_bytes()
    if hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!='0f25939c7028ef09519f82ca67eef92852444985':
        raise RuntimeError('R59 referee report identity mismatch')
    round2=ROOT/'inputs/review/R59_ROUND2_REFEREE_REPORT.md'
    raw2=round2.read_bytes()
    if hashlib.sha1(f'blob {len(raw2)}\0'.encode()+raw2).hexdigest()!='d853a5196f0f67ffbdcba49e78246437cc6d6a1c':
        raise RuntimeError('R59 round-2 report identity mismatch')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
             PYTHONDONTWRITEBYTECODE='1',SOURCE_DATE_EPOCH='1792022400')
    diagnostics={}
    for name,file in [('r61','diagnostics.py'),('r62','diagnostics_r62.py'),('r63','diagnostics_r63.py')]:
        normal=out/f'{name}-normal.json';optimized=out/f'{name}-optimized.json'
        run([sys.executable,file],ROOT,normal,env)
        run([sys.executable,'-O',file],ROOT,optimized,env)
        if normal.read_bytes()!=optimized.read_bytes():raise RuntimeError(f'Optimized mismatch: {name}')
        diagnostics[name]=json.loads(normal.read_text())
    docs=[]
    for key,cwd,tex,filename in [
        ('manuscript',ROOT,'main.tex','General_Theta_Foundations_I_R63.pdf'),
        ('supplement',ROOT,'supplement.tex','General_Theta_Foundations_I_R63_Supplement.pdf'),
        ('companion',ROOT/'retained/r58-native','main.tex','General_Theta_Complete_Companion_R58.pdf')]:
        build=out/key;build.mkdir(exist_ok=True)
        cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
             '-recorder','-no-shell-escape',f'-output-directory={build}',tex]
        for n in range(1,4):run(cmd,cwd,build/f'pass-{n}.txt',env)
        log=(build/(Path(tex).stem+'.log')).read_text(errors='replace')
        problems=[term for term in ['undefined references','undefined citations','multiply defined','Overfull \\hbox','Overfull \\vbox'] if term in log]
        if problems:raise RuntimeError(f'Final TeX diagnostics in {key}: {problems}')
        if key in ('manuscript','supplement'):
            aux=(build/(Path(tex).stem+'.aux')).read_text()
            resolved={m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',aux)}
            for line in (ROOT/'THEOREM_MAP.md').read_text().splitlines():
                parts=line.split('|')
                if len(parts)>=7 and parts[4].strip().startswith('`'):
                    label=parts[4].strip().strip('`')
                    source=parts[3].strip().strip('`')
                    if (key=='manuscript' and source=='supplement.tex') or (key=='supplement' and source!='supplement.tex'):
                        continue
                    if label not in resolved or resolved[label]!=(parts[1].strip(),parts[2].strip()):
                        raise RuntimeError(f'Theorem map differs from build: {label}')
        pdf=out/filename;shutil.copyfile(build/(Path(tex).stem+'.pdf'),pdf)
        text=out/(Path(filename).stem+'.txt')
        run(['pdftotext','-layout',str(pdf),str(text)],ROOT,build/'text-extraction.txt',env)
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        (build/'pdfinfo.txt').write_text(info)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        docs.append({'document':key,'file':filename,'pages':pages,'sha256':digest(pdf),
                     'text_sha256':digest(text),'passes':3,'command':cmd})
    verify_source()
    checkout=None
    try:checkout=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except (FileNotFoundError,subprocess.CalledProcessError):pass
    if checkout and not args.source_commit.startswith('local-') and checkout!=args.source_commit:
        raise RuntimeError('Checked-out commit mismatch')
    receipt={'schema':'theta.r63.native-verification.v1','status':'PASS',
        'declared_source_commit':args.source_commit,'checkout_head_verified':checkout,
        'source_manifest_sha256':digest(ROOT/'SOURCE_MANIFEST.json'),
        'source_git_tree':git_tree(ROOT),
        'exact_finite_checks':sum(sum(n for k,n in r['checks_by_group'].items() if k.startswith('exact')) for r in diagnostics.values()),
        'floating_finite_checks':sum(sum(n for k,n in r['checks_by_group'].items() if k.startswith('float')) for r in diagnostics.values()),
        'source_files_verified':file_count,'latest_report_bytes_verified_locally':True,
        'documents':docs,'diagnostics':diagnostics,'ordinary_optimized_identity':True,
        'total_checks':sum(r['total_checks'] for r in diagnostics.values()),
        'python':sys.version,'platform':platform.platform(),
        'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'limits':'Finite checks and native source reproducibility, not formal proof, human assessment or editorial acceptance. A declared SHA is not a local checkout proof when checkout_head_verified is null. Both R59 reports are byte-verified against their separate locked Git blobs. This local record does not assert a remote commit, push or CI run.'}
    (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','documents':docs,'checks':receipt['total_checks']},indent=2))
if __name__=='__main__':main()
