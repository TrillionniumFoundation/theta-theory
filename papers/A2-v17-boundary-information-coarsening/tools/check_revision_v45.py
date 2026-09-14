#!/usr/bin/env python3
"""Exact inherited-input preservation and static cross-reference diagnostics.

These checks establish source identity and native input closure, not proofs.
No Python assertion is used for a validity decision.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
BASE = P / 'history/v44-review-baseline'
ADDED = {'article/01f_generic_rigidity_overview_v45.tex',
         'article/23j_generic_finite_channel_rigidity_v45.tex'}

def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def closure(entry: str) -> dict[str, str]:
    out: dict[str, str] = {}
    def visit(name: str) -> None:
        if name in out:
            return
        require('..' not in Path(name).parts, 'Unsafe input path')
        text = (P / name).read_text()
        out[name] = text
        plain = re.sub(r'(?<!\\)%[^\n]*', '', text)
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', plain):
            visit(child if child.endswith('.tex') else child+'.tex')
    visit(entry)
    return out

def main() -> None:
    baseline = json.loads((BASE/'active-source-manifest.json').read_text())
    checked = 0
    for entry, files in baseline.items():
        for name, identity in files.items():
            path = BASE/'main.tex' if name == 'main.tex' else P/name
            data = path.read_bytes()
            require(blob(data) == identity['git_blob'], 'Inherited input changed: '+name)
            require(hashlib.sha256(data).hexdigest() == identity['sha256'], 'SHA mismatch: '+name)
            checked += 1
    current = closure('main.tex')
    require(set(current) == set(baseline['main']) | ADDED, 'Unexpected input closure')
    old = (BASE/'main.tex').read_text()
    new = current['main.tex']
    inputs = lambda s: re.findall(r'\\input\{([^}]+)\}', s)
    require([x for x in inputs(new) if x+'.tex' not in ADDED] == inputs(old),
            'Inherited direct input order changed')
    all_text = '\n'.join(current.values())
    plain = re.sub(r'(?<!\\)%[^\n]*', '', all_text)
    labels = re.findall(r'\\label\{([^}]+)\}', plain)
    require(len(labels) == len(set(labels)), 'Duplicate labels')
    refs = set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', plain))
    require(not {r for r in refs-set(labels) if not r.startswith('TC-')}, 'Unknown reference')
    citations = set(c.strip() for m in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', plain) for c in m.split(','))
    bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', plain))
    require(citations <= bib, 'Unknown citation')
    envs = r'\\begin\{(?:theorem|lemma|proposition|corollary|definition)\}'
    count_new = sum(len(re.findall(envs, current[n])) for n in ADDED)
    old_envs = sum(len(re.findall(envs, old if n=='main.tex' else current[n])) for n in baseline['main'])
    print(json.dumps({'status':'passed', 'baseline_source':'b229bfa2df2962ea2ebfd0fb2fd11531036d33a6',
        'baseline_manifest_entries_verified': checked, 'main_inputs':len(current),
        'companion_inputs':len(closure('two_collision.tex')), 'retained_theorem_style_environments':old_envs,
        'added_theorem_style_environments':count_new,
        'retained_remark_environments':sum(len(re.findall(r'\\begin\{remark\}', old if n=='main.tex' else current[n])) for n in baseline['main']),
        'new_modules':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in sorted(ADDED)},
        'proof_certification':False}, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
