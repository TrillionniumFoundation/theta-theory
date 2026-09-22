#!/usr/bin/env python3
"""Rerun the frozen v115 diagnostics in a disposable standalone directory."""
from pathlib import Path
import shutil, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent

def main():
    evidence=HERE/'evidence'; evidence.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a2-v115-rerun-') as name:
        temp=Path(name)
        shutil.copytree(HERE/'history/v115_source',temp,dirs_exist_ok=True)
        shutil.copy2(HERE/'history/v115_verify_revision.py',temp/'verify_revision.py')
        (temp/'history').mkdir(exist_ok=True)
        shutil.copytree(HERE/'history/v114_source',temp/'history/v114_source')
        for source in HERE.glob('history/v114_*.py'):
            shutil.copy2(source,temp/'history'/source.name)
        (temp/'evidence').mkdir(exist_ok=True)
        shutil.copy2(HERE/'history/v115_V114_SOURCE_MANIFEST.json',temp/'evidence/V114_SOURCE_MANIFEST.json')
        result=subprocess.run([sys.executable,str(temp/'verify_revision.py')],cwd=temp,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (evidence/'V115_RERUN.log').write_text(result.stdout)
        if result.returncode:
            raise RuntimeError('Inherited v115 diagnostics failed; see evidence/V115_RERUN.log')
        output=temp/'evidence/DIAGNOSTICS.json'
        if not output.exists(): raise RuntimeError('Inherited diagnostics produced no receipt')
        shutil.copy2(output,evidence/'V115_RERUN_DIAGNOSTICS.json')
        print('PASS: frozen v115 diagnostics rerun in a disposable directory')
if __name__=='__main__': main()
