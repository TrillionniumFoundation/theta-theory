#!/usr/bin/env python3
"""Read-only source verification, native TeX builds, and finite diagnostics.
The output is reproducibility evidence, not a mathematical proof certificate.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args: list[str], cwd: Path, log: Path, env: dict[str,str]) -> None:
    with log.open('wb') as stream:
        result = subprocess.run(args, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {args}; see {log}')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source-commit', default='uncommitted-local-source')
    args = parser.parse_args()
    out = args.out.resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Build output must be outside the immutable source directory')
    out.mkdir(parents=True, exist_ok=True)
    for tool in ['pdflatex','pdftotext','pdfinfo']:
        if not shutil.which(tool):
            raise RuntimeError(f'Missing required native build tool: {tool}')
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for row in manifest['files']:
        path = ROOT/row['path']
        if not path.is_file() or sha(path) != row['sha256']:
            raise RuntimeError(f'Source identity mismatch: {row["path"]}')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1', SOURCE_DATE_EPOCH='1792022400')
    normal, optimized = out/'diagnostics-normal.json', out/'diagnostics-optimized.json'
    run([sys.executable,'diagnostics.py'], ROOT, normal, env)
    run([sys.executable,'-O','diagnostics.py'], ROOT, optimized, env)
    if normal.read_bytes() != optimized.read_bytes():
        raise RuntimeError('Normal and optimized diagnostic results differ')
    diagnostic = json.loads(normal.read_text())
    products = []
    for key, cwd, filename, product in [
        ('manuscript',ROOT,'main.tex','General_Theta_Foundations_I_R61.pdf'),
        ('supplement',ROOT,'supplement.tex','General_Theta_Foundations_I_R61_Supplement.pdf'),
        ('companion',ROOT/'retained/r58-native','main.tex','General_Theta_Complete_Companion_R58.pdf')]:
        build = out/key; build.mkdir(exist_ok=True)
        command = ['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                   '-recorder','-no-shell-escape',f'-output-directory={build}',filename]
        for n in range(1,4):
            run(command,cwd,build/f'pass-{n}.txt',env)
        log = (build/(Path(filename).stem+'.log')).read_text(errors='replace')
        bad = [x for x in ['undefined references','undefined citations','multiply defined','Overfull \\hbox'] if x in log]
        if bad:
            raise RuntimeError(f'Unresolved final TeX diagnostics in {key}: {bad}')
        pdf = out/product; shutil.copyfile(build/(Path(filename).stem+'.pdf'),pdf)
        text = out/(Path(product).stem+'.txt')
        run(['pdftotext','-layout',str(pdf),str(text)],ROOT,build/'pdftotext.txt',env)
        info = subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        (build/'pdfinfo.txt').write_text(info)
        pages = int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        products.append({'document':key,'file':product,'pages':pages,'sha256':sha(pdf),
                         'text_sha256':sha(text),'passes':3,'command':command})
    # Record a real Git check only when this source is in an actual checkout.
    git_head = None
    try:
        git_head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except (subprocess.CalledProcessError,FileNotFoundError):
        pass
    if git_head and args.source_commit != 'uncommitted-local-source' and git_head != args.source_commit:
        raise RuntimeError('Requested source SHA does not match checkout HEAD')
    receipt = {'schema':'theta.r61.native-verification.v1','status':'PASS',
        'declared_source_commit':args.source_commit,'checkout_head_verified':git_head,
        'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),
        'source_files_verified':len(manifest['files']),'documents':products,
        'diagnostics':diagnostic,'normal_optimized_byte_identity':True,
        'python':sys.version,'platform':platform.platform(),
        'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'limitations':'Local declared SHA is not a Git checkout proof when checkout_head_verified is null. Compare SOURCE_MANIFEST Git blob identities with the remote tree separately. Finite diagnostics and compilation are not formal proof, independent human review, priority certification, or editorial acceptance.'}
    (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','documents':products,'checks':diagnostic['total_checks']},indent=2))

if __name__ == '__main__':
    main()
