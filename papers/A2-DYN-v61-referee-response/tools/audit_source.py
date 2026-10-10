#!/usr/bin/env python3
"""Validate exact retained source and TeX reachability; not continuum proofs."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'f0c2f6c9044a9e76e487329dbf7791f865ee7b8c'
REVIEW = 'a81eb226c013ca062a6901bb472a90668de29eec'
RETAINED = {
 '01_interfaces.tex':'6d7437828de55373504019af8d56f2741a0ee51d',
 '02_physical_records.tex':'2dde4cf4e4e3f9856ae46e4d215a3e239c9089c5',
 '03_periodic_geometry.tex':'5bc9bde1b82796b1035f631b56812d909b6ecc97',
 '04_raw_edges.tex':'5255764d8c689ba808469a88352628e95dcfb441',
 '05_residual_inversion.tex':'c3dafc712fe3750b59106e9d91fdc62860c9d339',
 '06_downstream.tex':'20df3335f2c8e2819e23dc1bfdc70d6f3bc96c4b',
 '08_joint_arithmetic.tex':'4c0fed9a31b76b24a31280767a147d3785a9e4c6',
 '09_localized_inversion.tex':'02346db8f99a7e38d8e200e91967110ca314e1c6',
 '10_exact_clock.tex':'afc3774205f8ae47df86975b6035c6db28756744',
 '11_return_stability.tex':'efb0441fcb9c2c0592d7125948a06fec7c562abf',
 '12_quantitative_periods.tex':'45dffec67f3ed39a841c5084377928cf317d77fc',
 '13_uniform_physical_clock.tex':'05a9c639ecaedebd07a7cd9677098d29bb987093',
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def main() -> None:
    seen = set()
    def visit(name: str) -> None:
        path = (ROOT/name).resolve()
        require(path.is_relative_to(ROOT), 'external TeX input')
        require(path.is_file(), 'missing TeX input: '+name)
        rel = path.relative_to(ROOT).as_posix()
        require(rel not in seen, 'duplicate/cyclic TeX input: '+rel)
        seen.add(rel)
        for target in re.findall(r'\\input\{([^}]+)\}', path.read_text()):
            visit(target if target.endswith('.tex') else target+'.tex')
    visit('main.tex')
    for name, expected in RETAINED.items():
        rel = 'core/'+name
        require(rel in seen, 'retained file not active: '+rel)
        require(blob((ROOT/rel).read_bytes()) == expected, 'retained bytes changed: '+rel)
    require(blob((ROOT/'core/14_periodic_coercivity.tex').read_bytes()) ==
            '78732b7d250de8a97389e1016a61f1b8e5d2054c', 'recovered v5 core changed')
    texts = {name:(ROOT/name).read_text() for name in sorted(seen)}
    whole = '\n'.join(texts.values())
    labels = re.findall(r'\\label\{([^}]+)\}', whole)
    require(all(n == 1 for n in Counter(labels).values()), 'duplicate labels')
    refs = set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',whole))
    require(refs <= set(labels), 'undefined source reference: '+str(refs-set(labels)))
    cited = {k.strip() for item in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',whole)
             for k in item.split(',')}
    require(cited <= set(re.findall(r'\\bibitem\{([^}]+)\}',whole)), 'missing bibliography key')
    proofs = {name:len(re.findall(r'\\begin\{proof\}',text)) for name,text in texts.items()}
    retained_proofs = sum(proofs['core/'+name] for name in RETAINED)
    retained_labels = sum(len(re.findall(r'\\label\{([^}]+)\}',texts['core/'+name])) for name in RETAINED)
    require(retained_proofs == 37 and retained_labels == 107, 'baseline structure mismatch')
    require(sum(proofs.values()) == 58, 'unexpected active proof count')
    require('A2-DYN, revision 6' in texts['main.tex'], 'wrong version metadata')
    print(json.dumps({'status':'passed','scope':'source identity, reachability, preservation',
        'baseline_commit':BASE,'review_commit':REVIEW,
        'retained_proofs':retained_proofs,'retained_labels':retained_labels,
        'active_proofs':sum(proofs.values()),'active_labels':len(labels),
        'recovered_unpublished_v5_proofs':8,'new_v6_proofs':13,
        'active_inputs':sorted(seen),
        'git_blobs':{s:blob((ROOT/s).read_bytes()) for s in sorted(seen)},
        'sha256':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in sorted(seen)},
        'full_raw_LLT_verified':False,'independent_human_review':False},indent=2))

if __name__ == '__main__':
    main()
