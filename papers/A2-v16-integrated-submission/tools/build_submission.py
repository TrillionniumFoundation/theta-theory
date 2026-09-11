#!/usr/bin/env python3
"""Build the complete native A2 v16 source graph, never a shortened smoke test."""
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

SOURCE = Path(__file__).resolve().parents[1]
INPUT = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(cmd: list[str], cwd: Path, env: dict, output: Path) -> None:
    with output.open('wb') as f:
        completed = subprocess.run(cmd, cwd=cwd, env=env, stdout=f,
                                   stderr=subprocess.STDOUT, check=False)
    if completed.returncode:
        raise RuntimeError(f'Command failed ({completed.returncode}); see {output.name}')

def graph(entry: str, visited: set[str]) -> None:
    if entry in visited:
        return
    file = SOURCE / entry
    if not file.is_file():
        raise FileNotFoundError('Missing native TeX input: ' + entry)
    visited.add(entry)
    # This manuscript uses ordinary literal braced inputs and percent comments.
    text = re.sub(r'(?<!\\)%[^\n]*', '', file.read_text(encoding='utf-8'))
    for raw in INPUT.findall(text):
        rel = raw if raw.endswith('.tex') else raw+'.tex'
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError('Nonlocal TeX input: ' + rel)
        graph(rel, visited)

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    args=parser.parse_args()
    out=args.output_dir.resolve()
    if out == SOURCE or SOURCE in out.parents:
        raise ValueError('Output directory must be outside the manuscript tree')
    out.mkdir(parents=True,exist_ok=True)
    report={'status':'started','entrypoints':['two_collision.tex','main.tex'],
            'scope':'Complete native companion and main, including every active appendix and bibliography.',
            'source_commit':None,'warnings':{},'products':{}}
    env=os.environ.copy()
    env.update({'SOURCE_DATE_EPOCH':'1789084800','FORCE_SOURCE_DATE':'1',
                'TZ':'UTC','LC_ALL':'C.UTF-8'})
    try:
        for tool in ('latexmk','pdflatex','pdfinfo'):
            if not shutil.which(tool):
                raise RuntimeError('Required build executable unavailable: '+tool)
        cp=subprocess.run(['git','rev-parse','HEAD'],cwd=SOURCE,
                          capture_output=True,text=True,check=False)
        if cp.returncode==0:
            report['source_commit']=cp.stdout.strip()
        visited=set()
        graph('two_collision.tex',visited)
        graph('main.tex',visited)
        manifest={p:{'bytes':(SOURCE/p).stat().st_size,
                     'sha256':sha256(SOURCE/p)} for p in sorted(visited)}
        (out/'active-source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        report['active_tex_files']=len(visited)
        for tool in ('latexmk','pdflatex','pdfinfo'):
            cp=subprocess.run([tool,'--version' if tool!='pdfinfo' else '-v'],
                              capture_output=True,text=True,check=False)
            (out/(tool+'-version.txt')).write_text(cp.stdout+cp.stderr)
        for opt,name in (([],'normal'),(['-O'],'optimized')):
            run([sys.executable,*opt,str(SOURCE/'tools/check_adaptive.py')],
                SOURCE,env,out/('adaptive-'+name+'.json'))
        if (out/'adaptive-normal.json').read_bytes() != (out/'adaptive-optimized.json').read_bytes():
            raise RuntimeError('Ordinary and optimized diagnostic outputs differ')
        report['finite_diagnostics']=json.loads((out/'adaptive-normal.json').read_text())
        with tempfile.TemporaryDirectory(prefix='a2-v16-build-') as tmp:
            work=Path(tmp)/'paper'
            shutil.copytree(SOURCE,work,ignore=shutil.ignore_patterns(
                '*.pdf','*.aux','*.log','*.fls','*.fdb_latexmk','*.out','*.toc','__pycache__'))
            for stem in ('two_collision','main'):
                run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
                     '-file-line-error','-pdflatex=pdflatex -no-shell-escape %O %S',stem+'.tex'],
                    work,env,out/(stem+'-build.txt'))
                log=(work/(stem+'.log')).read_text(errors='replace')
                bad=re.findall(r'.*(?:undefined references|undefined citations|Reference .+ undefined|Citation .+ undefined|multiply[- ]defined|Missing character:).*',log,re.I)
                warnings=re.findall(r'.*(?:Warning:|Overfull \\[hv]box|Underfull \\[hv]box).*',log)
                report['warnings'][stem]=warnings
                for suffix in ('.pdf','.log','.aux','.fls','.fdb_latexmk','.out'):
                    p=work/(stem+suffix)
                    if p.exists():
                        shutil.copy2(p,out/p.name)
                if bad:
                    raise RuntimeError(stem+': unresolved references, duplicate labels, or missing glyphs: '+repr(bad))
                pdf=out/(stem+'.pdf')
                cp=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True)
                (out/(stem+'-pdfinfo.txt')).write_text(cp.stdout)
                match=re.search(r'^Pages:\s*(\d+)',cp.stdout,re.M)
                if match is None:
                    raise RuntimeError('Could not read PDF page count: '+stem)
                report['products'][stem]={'pages':int(match.group(1)),
                    'bytes':pdf.stat().st_size,'sha256':sha256(pdf)}
        report['status']='passed'
    except Exception as exc:
        report['status']='failed'
        report['error']=str(exc)
        raise
    finally:
        (out/'build-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
