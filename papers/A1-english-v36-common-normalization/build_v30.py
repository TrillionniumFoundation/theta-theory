#!/usr/bin/env python3
"""Offline native two-volume build; preserve inherited proofs and report actual execution."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'build-v30'
BASE = ROOT.parent / 'A1-english-v29'
CHANGED_TEX = {'main.tex','v25/graph_consequences.tex','v27/policy_menus.tex'}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def refs(text: str) -> set[str]:
    out = set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}', text))
    out.update(re.findall(r'\\upref\{[^}]+\}\{([^}]+)\}', text))
    return {s for s in out if '#' not in s}

def proof_bodies(text: str) -> Counter[str]:
    return Counter(hashlib.sha256(m.encode()).hexdigest()
                   for m in re.findall(r'\\begin\{proof\}(?:\[[^]]*\])?(.*?)\\end\{proof\}',
                                       text, flags=re.S))

def audit(stage: Path, helpers) -> dict:
    if not (BASE/'main.tex').is_file():
        raise FileNotFoundError('The preserved adjacent A1-english-v29 baseline is required')
    retained = {}
    for path in sorted(BASE.rglob('*.tex')):
        name = path.relative_to(BASE).as_posix()
        if any(part.startswith('build') for part in path.relative_to(BASE).parts):
            continue
        target = ROOT/name
        if name not in CHANGED_TEX:
            if not target.is_file() or target.read_bytes() != path.read_bytes():
                raise ValueError('Inherited TeX changed or missing: '+name)
            retained[name] = digest(path)
    original = '\n'.join(helpers.expand(BASE,BASE/(doc+'.tex')) for doc in ('main','companions'))
    texts = {doc:helpers.expand(stage,stage/(doc+'.tex')) for doc in ('main','companions')}
    new = '\n'.join(texts.values())
    lost_proofs = proof_bodies(original)-proof_bodies(new)
    old_labels = set(re.findall(r'\\label\{([^}]+)\}',original))
    labels = {doc:re.findall(r'\\label\{([^}]+)\}',text) for doc,text in texts.items()}
    counts = Counter(labels['main']+labels['companions'])
    missing_labels = old_labels-set(counts)
    duplicate = {k:v for k,v in counts.items() if v>1}
    missing_refs = sorted(refs(new)-set(counts))
    if lost_proofs or missing_labels or duplicate or missing_refs:
        raise ValueError(f'Source audit: lost_proofs={dict(lost_proofs)}, '
                         f'lost_labels={sorted(missing_labels)}, duplicates={duplicate}, '
                         f'unresolved={missing_refs}')
    for doc,text in texts.items():
        cited = {key.strip() for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',text)
                 for key in m[1].split(',')}
        bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
        if cited-bib:
            raise ValueError(f'{doc}: unresolved bibliography {sorted(cited-bib)}')
        (OUT/(doc+'-expanded.tex')).write_text(text)
    return {'unchanged_inherited_tex':retained,
            'old_active_proof_environments':sum(proof_bodies(original).values()),
            'new_active_proof_environments':sum(proof_bodies(new).values()),
            'lost_proof_bodies':dict(lost_proofs),'lost_labels':sorted(missing_labels),
            'duplicate_labels':duplicate,'unresolved_references':missing_refs,
            'label_counts':{d:len(v) for d,v in labels.items()}}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only',action='store_true')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    record = {'schema':'A1-v30-multilevel-native-build-1','status':'started',
              'full_two_volume_build':False,'tex_passes':[],
              'review_commit':'90c7acd0e4efe3280eb1a8faa3c6d9461870c36f',
              'scope':'Source preservation, finite diagnostics and typesetting; not a mathematical or venue certificate.'}
    try:
        import build_v28 as helpers
        helpers.OUT = OUT
        stage = OUT/'native'
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(ROOT,stage,ignore=shutil.ignore_patterns(
            'build-v*','build','__pycache__','*.pdf','*.aux','*.log','*.out','*.toc'))
        helpers.companion_bibliography(stage)
        record['source_audit'] = audit(stage,helpers)
        record['diagnostics'] = {}
        for name in ('diagnostics.py','diagnostics_v27.py','diagnostics_v28.py',
                     'diagnostics_v29.py','diagnostics_v30.py'):
            outputs = []
            for opts in ([],['-O']):
                p = subprocess.run([sys.executable,*opts,str(ROOT/name)],
                                   capture_output=True,text=True,check=True,timeout=180)
                outputs.append(p.stdout)
            if outputs[0] != outputs[1]:
                raise ValueError('Normal/optimized diagnostic mismatch: '+name)
            record['diagnostics'][name] = {'sha256':digest(ROOT/name),
                                          'normal_optimized_identical':True,
                                          'result':json.loads(outputs[0])}
        record['staging_only_xr_compatibility'] = []
        for doc in ('main','companions'):
            path = stage/(doc+'.tex'); text = path.read_text()
            old = r'\externaldocument[][nocite]'
            if old in text:
                record['staging_only_xr_compatibility'].append(doc)
                path.write_text(text.replace(old,r'\externaldocument'))
        if args.prepare_only:
            record['status'] = 'source-and-diagnostics-passed; TeX not requested'
            return
        engine = shutil.which('pdflatex')
        if not engine:
            raise RuntimeError('pdflatex unavailable; full build not performed')
        record['engine'] = subprocess.run([engine,'--version'],capture_output=True,
                                          text=True,check=True).stdout.splitlines()[0]
        allowed = {doc:set(re.findall(r'\\label\{([^}]+)\}',
                                      helpers.expand(stage,stage/(doc+'.tex'))))
                   for doc in ('main','companions')}
        for doc in allowed:
            helpers.export_labels(stage,doc,allowed[doc])
        for iteration in range(1,6):
            for doc in allowed:
                p = subprocess.run([engine,'-no-shell-escape','-interaction=nonstopmode',
                                    '-halt-on-error',doc+'.tex'],cwd=stage,
                                   capture_output=True,text=True,timeout=180)
                (OUT/f'{doc}-pass-{iteration}.txt').write_text(p.stdout+p.stderr)
                record['tex_passes'].append({'document':doc,'pass':iteration,'returncode':p.returncode})
                if p.returncode:
                    raise RuntimeError(f'{doc}: TeX pass {iteration} failed')
                helpers.export_labels(stage,doc,allowed[doc])
        record['final_log_messages'] = {}
        bad = re.compile(r'undefined|multiply defined|Rerun to get cross-references right|Label\(s\) may have changed|Overfull \\[hv]box',re.I)
        for doc in allowed:
            log = (stage/(doc+'.log')).read_text(errors='replace')
            record['final_log_messages'][doc] = [line for line in log.splitlines()
                                                if any(w in line for w in ('Warning:','Underfull','Overfull'))]
            if bad.search(log):
                raise RuntimeError(f'{doc}: unresolved reference or layout warning')
        record['pdf_sha256'] = {doc:digest(stage/(doc+'.pdf')) for doc in allowed}
        record['full_two_volume_build'] = True
        record['status'] = 'native-two-volume-build-passed; visual inspection separate'
    except Exception as exc:
        record['status'] = 'failed'
        record['error'] = str(exc)
        raise
    finally:
        (OUT/'BUILD_RECORD_V30.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
