#!/usr/bin/env python3
"""Audit only the v28 changed sources, not the full recursive native graph."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parents[1]
BASE = 'e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864'
MATH = '6d8f158c60f3636c572daa64779f57c9c9ec757b'
OLD = {
    'main_pre_v28.tex': '2133039c3a220a923b232db9f1c5a5661938773c',
    'article/01b_observation_hierarchy_v23.tex': '4b747a51deb4e4bd2def93da7d73d8fd841041f5',
    'article/23b_intrinsic_multichannel_rigidity_v23.tex': '0146f25a95d9cdb92cb09f4b6916d4d153cedeaf',
    'preamble.tex': '7e0de97c08dd2e12187193aff89f3ca4712f430f',
}
REPLACE = {
    'article/01b_observation_hierarchy_v23': 'article/01b_observation_hierarchy_v28',
    'article/23b_intrinsic_multichannel_rigidity_v23': 'article/23b_intrinsic_multichannel_rigidity_v28',
}
ADDED = 'article/23h_global_orientation_quotient_v28'
FILES = ['main.tex', *(s+'.tex' for s in REPLACE.values()), ADDED+'.tex',
         'tools/check_revision_v28.py', 'diagnostics/v28-finite-checks.json']


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def identity(path: str) -> dict:
    b = (P/path).read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def read(path: str) -> str:
    return (P/path).read_text(encoding='utf-8')


def main() -> None:
    for p, sha in OLD.items():
        require(identity(p)['git_blob'] == sha, 'Base identity mismatch: '+p)
    old, new = read('main_pre_v28.tex'), read('main.tex')
    inputs = re.compile(r'\\input\{([^}]+)\}')
    oi, ni = inputs.findall(old), inputs.findall(new)
    require([REPLACE.get(s, s) for s in oi] == [s for s in ni if s != ADDED],
            'Input preservation/order failure')
    require(ni.count(ADDED) == 1 and len(ni) == len(oi)+1, 'New input multiplicity')
    label = re.compile(r'\\label\{([^}]+)\}')
    before = read('article/23b_intrinsic_multichannel_rigidity_v23.tex')
    after = read('article/23b_intrinsic_multichannel_rigidity_v28.tex')
    labels = label.findall(before)
    require(labels == label.findall(after), 'Inherited multichannel labels changed')
    old_sentence = ('If every transverse sign is simultaneously forgotten, the corresponding\n'
                    'statement is modulo \\(\\mathrm E(2)\\), with one unavoidable global reflection.')
    new_sentence = ('For the common-orientation orbit of the entire marked datum, as defined in\n'
                    'Definition~\\ref{def:v28-common-orientation-datum}, the corresponding\n'
                    'classification is modulo \\(\\mathrm E(2)\\), by\n'
                    'Theorem~\\ref{thm:v28-unoriented-classification}.  This assertion concerns one\n'
                    'common orientation choice, not pointwise deletion of endpoint signs.')
    require(before.count(old_sentence) == 1, 'Ambiguous old replacement location')
    require(before.replace(old_sentence, new_sentence).rstrip('\n') == after.rstrip('\n'),
            'Unexpected alteration of inherited multichannel mathematics')
    require(read('article/01b_observation_hierarchy_v28.tex').startswith(
            read('article/01b_observation_hierarchy_v23.tex')), 'Old hierarchy not retained')
    changed = '\n'.join(read(p) for p in FILES if p.endswith('.tex'))
    defined = label.findall(changed)
    require(not [k for k,v in Counter(defined).items() if v > 1], 'Duplicate changed-source label')
    refs = sorted(set(re.findall(r'\\(?:eqref|ref)\{(.*?v28[^}]*)\}', changed)))
    require(all(r in defined for r in refs), 'Unresolved new-label reference')
    result = {
        'status': 'passed', 'base_commit': BASE, 'mathematical_source_commit': MATH,
        'scope': 'Changed-source preservation only; not the full recursive native audit',
        'base_native_git_blobs': OLD, 'changed_files': {p: identity(p) for p in FILES},
        'old_direct_inputs': len(oi), 'new_direct_inputs': len(ni),
        'replaced_inputs': REPLACE, 'added_input': ADDED,
        'all_other_input_order_preserved': True, 'preserved_multichannel_labels': labels,
        'only_ambiguous_sentence_replaced': True,
        'new_references_resolved_in_changed_modules': refs,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
