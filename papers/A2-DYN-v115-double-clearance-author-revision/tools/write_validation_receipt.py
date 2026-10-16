#!/usr/bin/env python3
"""Executed only after all build gates succeed."""
import datetime,hashlib,json,platform,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
scripts=['check_manifest','check_source','check_finite','check_research','check_load','check_clearance','check_critical_coarea','check_two_mark']
checks={}
for s in scripts:
    a=(P/f'build/{s}.json').read_bytes();b=(P/f'build/{s}-optimized.json').read_bytes()
    if a!=b: raise RuntimeError('optimized output mismatch: '+s)
    checks[s]={'sha256':hashlib.sha256(a).hexdigest(),'ordinary_equals_optimized':True}
result={'status':'passed','executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_manifest_sha256':hashlib.sha256((P/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
        'python':platform.python_version(),'system':platform.platform(),
        'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'checks':checks,'baseline_typesetting':json.loads((P/'build/baseline-typesetting.json').read_text()),
        'revised_typesetting':json.loads((P/'build/typesetting.json').read_text()),
        'latex_passes_each':3,'remote_ci_for_this_source':False,'remote_push':False,
        'scope':'Local source/finite-diagnostic/typesetting execution, not mathematical proof certification.'}
(P/'evidence/current/current-validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
