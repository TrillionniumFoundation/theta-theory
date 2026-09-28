#!/usr/bin/env python3
"""Build both complete native A2 entries; preserve logs even on a failed build."""
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
ENTRIES = ('two_collision', 'main')
INPUT = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')
PRODUCT_SUFFIXES = ('.pdf','.log','.aux','.fls','.fdb_latexmk','.out','.toc')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str], cwd: Path, env: dict[str,str], output: Path) -> int:
    with output.open('wb') as stream:
        return subprocess.run(cmd,cwd=cwd,env=env,stdout=stream,
                              stderr=subprocess.STDOUT,check=False).returncode


def graph(entry: str, visited: set[str]) -> None:
    if entry in visited:
        return
    file = SOURCE/entry
    if not file.is_file():
        raise FileNotFoundError('Missing native TeX input: '+entry)
    visited.add(entry)
    text = re.sub(r'(?<!\\)%[^\n]*','',file.read_text(encoding='utf-8'))
    for raw in INPUT.findall(text):
        rel = raw if raw.endswith('.tex') else raw+'.tex'
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError('Nonlocal TeX input: '+rel)
        graph(rel,visited)


def copy_ignore(directory: str, names: list[str]) -> list[str]:
    ignored = [name for name in names if name in ('__pycache__','.git')]
    if Path(directory).resolve() == SOURCE.resolve():
        generated = {stem+suffix for stem in ENTRIES for suffix in PRODUCT_SUFFIXES}
        ignored.extend(name for name in names if name in generated)
    return ignored


def build_entry(stem: str, work: Path, out: Path, env: dict[str,str]) -> dict:
    result = {'status':'started','entry':stem+'.tex','layout_review':'not performed by this script'}
    cmd = ['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
           '-file-line-error','-pdflatex=pdflatex -no-shell-escape %O %S',stem+'.tex']
    result['command'] = cmd
    try:
        code = run(cmd,work,env,out/(stem+'-build.txt'))
        result['returncode'] = code
        log_file = work/(stem+'.log')
        log = log_file.read_text(errors='replace') if log_file.exists() else ''
        # TeX wraps diagnostic words, not only lines between words.
        flat = ''.join(log.splitlines())
        fatal = re.search(r'undefined references|undefined citations|'
                          r'(?:Reference|Citation) `.{0,250}?undefined|'
                          r'multiply[- ]defined|Missing character:',flat,re.I)
        result['warnings'] = re.findall(r'.*(?:Warning:|Overfull \\[hv]box|Underfull \\[hv]box).*',log)
        if code:
            raise RuntimeError('latexmk failed; complete available logs are preserved')
        if fatal:
            raise RuntimeError('Unresolved references/citations, duplicate labels, or missing glyphs')
        pdf = work/(stem+'.pdf')
        cp = subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True)
        (out/(stem+'-pdfinfo.txt')).write_text(cp.stdout)
        pages = re.search(r'^Pages:\s*(\d+)',cp.stdout,re.M)
        if pages is None:
            raise RuntimeError('Could not read native PDF page count')
        result['product'] = {'pages':int(pages.group(1)), 'bytes':pdf.stat().st_size,
                             'sha256':sha256(pdf)}
        fls = work/(stem+'.fls')
        actual = {}
        if fls.exists():
            for line in fls.read_text(errors='replace').splitlines():
                if not line.startswith('INPUT '):
                    continue
                candidate = Path(line[6:])
                if not candidate.is_absolute():
                    candidate = work/candidate
                try:
                    rel = candidate.resolve().relative_to(work.resolve())
                except ValueError:
                    continue
                original = SOURCE/rel
                if original.is_file():
                    actual[rel.as_posix()] = sha256(original)
        (out/(stem+'-recorder-source-inputs.json')).write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
        result['status'] = 'passed'
    except Exception as exc:
        result['status'] = 'failed'
        result['error'] = str(exc)
    finally:
        # Run this before TemporaryDirectory cleanup, including on latexmk failure.
        for suffix in PRODUCT_SUFFIXES:
            path = work/(stem+suffix)
            if path.exists():
                shutil.copy2(path,out/path.name)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True,type=Path)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    if out == SOURCE or SOURCE in out.parents:
        raise ValueError('Output directory must be outside the manuscript tree')
    out.mkdir(parents=True,exist_ok=True)
    report = {'status':'started','entrypoints':[s+'.tex' for s in ENTRIES],
              'scope':'Complete native companion and main; all active inputs, appendices and bibliography. No shortened fixture.',
              'source_commit':None,'errors':[],'entries':{},'finite_diagnostics':{}}
    env = os.environ.copy()
    env.update({'SOURCE_DATE_EPOCH':'1789084800','FORCE_SOURCE_DATE':'1',
                'TZ':'UTC','LC_ALL':'C.UTF-8'})
    try:
        cp = subprocess.run(['git','rev-parse','HEAD'],cwd=SOURCE,
                            capture_output=True,text=True,check=False)
        if cp.returncode == 0:
            report['source_commit'] = cp.stdout.strip()
        visited = set()
        for stem in ENTRIES:
            try:
                graph(stem+'.tex',visited)
            except Exception as exc:
                report['errors'].append(str(exc))
        manifest = {p:{'bytes':(SOURCE/p).stat().st_size,'sha256':sha256(SOURCE/p)}
                    for p in sorted(visited)}
        (out/'active-source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
        report['active_tex_files'] = len(visited)
        for tool in ('latexmk','pdflatex','pdfinfo'):
            if not shutil.which(tool):
                raise RuntimeError('Required native build executable unavailable: '+tool)
            cp = subprocess.run([tool,'-v' if tool=='pdfinfo' else '--version'],
                                capture_output=True,text=True,check=False)
            (out/(tool+'-version.txt')).write_text(cp.stdout+cp.stderr)
        for script in ('check_adaptive.py','check_revision_v32.py'):
            outputs = []
            for opt,name in (([],'normal'),(['-O'],'optimized')):
                target = out/(Path(script).stem+'-'+name+'.json')
                code = run([sys.executable,*opt,str(SOURCE/'tools'/script)],SOURCE,env,target)
                outputs.append(target)
                if code:
                    report['errors'].append(script+' '+name+' failed; see '+target.name)
            if outputs[0].read_bytes() != outputs[1].read_bytes():
                report['errors'].append(script+': ordinary/optimized outputs differ')
            try:
                report['finite_diagnostics'][script] = json.loads(outputs[0].read_text())
            except (ValueError,UnicodeError):
                report['errors'].append(script+': diagnostic output is not JSON')
        with tempfile.TemporaryDirectory(prefix='a2-complete-native-') as temporary:
            work = Path(temporary)/'paper'
            shutil.copytree(SOURCE,work,ignore=copy_ignore)
            for stem in ENTRIES:
                report['entries'][stem] = build_entry(stem,work,out,env)
                if report['entries'][stem]['status'] != 'passed':
                    report['errors'].append(stem+': '+report['entries'][stem]['error'])
        report['status'] = 'failed' if report['errors'] else 'passed'
    except Exception as exc:
        report['status'] = 'failed'
        report['errors'].append(str(exc))
    finally:
        (out/'build-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))
    if report['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
