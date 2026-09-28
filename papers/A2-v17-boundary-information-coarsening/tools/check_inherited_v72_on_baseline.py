#!/usr/bin/env python3
"""Run the unchanged v72 checker with its original active sources restored.

The v72 checker intentionally rejects later edits. Restore the seven v73-edited
paths from their byte-preserved copies in an isolated temporary tree, then run
that unchanged checker, including its authentic v71 reconstruction. Later
inactive additions remain in this temporary tree and are not passed off as
reviewed v72 content. Revision-73 preservation is checked separately.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from source_provenance import require
ROOT=Path(__file__).resolve().parents[1]
EDITED=('README.md','main.tex','rigidity.tex','article/00i_main_thesis_v70.tex',
        'article/10g_uncalibrated_single_law_v72.tex','journal/references_v56.tex','v5/references_v43.tex')

def main():
    with tempfile.TemporaryDirectory(prefix='a2-v72-active-baseline-') as temp:
        target=Path(temp)/'source'
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('.git','__pycache__'))
        for name in EDITED:
            original=ROOT/'history/v72-review-baseline'/name
            require(original.is_file(),'Missing retained original: '+name)
            dest=target/name;dest.chmod(0o644);dest.write_bytes(original.read_bytes())
            dest.chmod(original.stat().st_mode & 0o777)
        command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        cp=subprocess.run(command+[str(target/'tools/check_revision_v72.py')],cwd=target,capture_output=True,text=True)
        require(cp.returncode==0,'Unchanged v72 checker failed on restored sources: '+cp.stderr)
        result=json.loads(cp.stdout)
    print(json.dumps({'scope':'Unchanged v72 checker on restored v72 active sources; later inactive additions not audited as historical content. Includes its exact v71 reconstruction.', 'result':result},indent=2,sort_keys=True))
if __name__=='__main__':main()
