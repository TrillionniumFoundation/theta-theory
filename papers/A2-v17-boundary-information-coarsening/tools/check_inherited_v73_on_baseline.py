#!/usr/bin/env python3
"""Execute unchanged inherited diagnostics on byte-restored v73 sources."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from source_provenance import require
ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    edited=json.loads((ROOT/'REVISION_V74_EDITED_PATHS.json').read_text())
    results={}
    with tempfile.TemporaryDirectory(prefix='a2-v73-baseline-') as tmp:
        target=Path(tmp)/'source'
        shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('.git','__pycache__'))
        for name in edited:
            original=ROOT/'history/v73-review-baseline'/name
            require(original.is_file(),'Missing preserved original: '+name)
            dest=target/name
            dest.chmod(0o644)
            shutil.copy2(original,dest)
        for script in ('check_inherited_v72_on_baseline.py','check_revision_v73.py'):
            command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
            cp=subprocess.run(command+[str(target/'tools'/script)],cwd=target,capture_output=True,text=True)
            require(cp.returncode==0,script+' failed on restored v73 baseline: '+cp.stderr)
            results[script]=json.loads(cp.stdout)
    print(json.dumps({'scope':'Unchanged v73 diagnostics and its inherited v72/v71 checks on restored v73 active source bytes; new v74 modules are not historical proof certificates.','results':results},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
