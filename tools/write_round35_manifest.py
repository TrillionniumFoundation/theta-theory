#!/usr/bin/env python3
"""Explicit authoring utility. Never invoked by the verifier or CI."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=['README.md','ROUND35_REVIEW_INDEX.md','AUTHOR_RESPONSE_ROUND34.md','ROUND35_REVISION.tex',
       '.github/workflows/verify-round35.yml']
files += [str(p.relative_to(ROOT)) for p in (ROOT/'round35').rglob('*')
          if p.is_file() and p.name not in ('SOURCE_MANIFEST.json',) and '__pycache__' not in str(p)]
dirs=('B1-microcanonical-preparation','B3-hamilton-boltzmann-cotangents','C1-information-risk-sensitive-saddles','C2-cotangent-rigidity-tangent-representations')
files += ['papers/'+d+'/'+name for d in dirs for name in ('main.tex','ROUND35_REVISION.tex')]
files += ['tools/'+name for name in ('certify_round35.py','mechanical_benchmark.py','verify_round35.py','write_round35_manifest.py')]
files += ['tests/test_round35.py']
manifest={'base_commit':'9f5276233b63218a0d89df6611381975dc873232',
          'files':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in sorted(set(files))}}
(ROOT/'round35/SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(len(manifest['files']))
