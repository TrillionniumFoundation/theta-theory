#!/usr/bin/env python3
"""Prepare amended copies, never edit the preserved A2 sources."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTICLE = HERE.parent


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f'Expected one source anchor, got {text.count(old)}: {old[:90]}')
    return text.replace(old, new, 1)


def prepare() -> dict:
    out = HERE / 'prepared'
    out.mkdir(exist_ok=True)
    records = {}
    for name, source in {
        'synchronized.tex': '01-critical-contact.tex',
        'geometry.tex': '03-geometry.tex',
        'endpoint-completion.tex': '04-endpoint-completion.tex',
        'positioning.tex': '05-positioning.tex',
    }.items():
        src = ARTICLE / 'v107' / 'parts' / source
        old = src.read_text()
        text = old
        if name == 'synchronized.tex':
            text = replace_once(text,
                'Let the clock and root separation, probability, and exposure margins be positive. Then the following assertions hold.',
                r'Let the clock and root separation, probability, and exposure margins be positive. For uniform assertions, fix the dimensions, take the loadings and targets in bounded sets with $b\ge0$, keep metric eigenvalues in a compact subinterval of $(0,\infty)$, and require $\mu(A)=\min_{\|S\|_F=1}\|\mathcal A_A(S)\|_2\ge\mu_0>0$. The nonlinear perturbations are defined on one fixed ball, vanish at zero, have derivative $a_i^{\mathsf T}$ there, and have a common $C^2$ bound, as specified in Section~\ref{sec:uniform-class}. Then the following assertions hold.')
            text = text.replace('for every $A,b$.', r'for every allowed $A$ and $b\in\R_+^k$.')
        elif name == 'geometry.tex':
            text = replace_once(text, r'Let $\Gamma$ be the compact closure of the positive-time graph',
                r'Assume a compact semialgebraic source, polynomial or analytic-semialgebraic observation maps, and semialgebraic marked arcs and tube data with the stated positive-time analytic regularity. Assume $J\ne0$ on the positive-time tube. Uniformization and every pruning below retain a surjective preimage of the positive-time graph closure. Let $\Gamma$ be that compact closure, namely the closure of')
        elif name == 'endpoint-completion.tex':
            anchor = r'\label{thm:all-strata}'
            text = replace_once(text, anchor, anchor + '\n' +
                r'This is a reference-presentation equality theorem: the matrix $Q$ is supplied. The function-only minimal-fibre theorem is Theorem~\ref{thm:intrinsic-fibre}.')
        else:
            text = replace_once(text,
                'The contribution is the relation among a particular singular feasible set, a model-forced information matrix, and an inverse endpoint object.',
                r'The following background comparisons concern the retained companion results. The principal conormal interaction and its inverse-optimization and design-equivalence comparisons are stated separately in the introduction and Theorem~\ref{thm:general-tomography}.')
        for env in ('theorem', 'lemma', 'proposition', 'corollary', 'proof', 'example'):
            if old.count('\\begin{' + env + '}') != text.count('\\begin{' + env + '}'):
                raise AssertionError(f'Environment removed in {name}: {env}')
        target = out / name
        target.write_text('% Deterministically prepared from the preserved v107 source; see prepare.py.\n' + text)
        records[name] = {'input': str(src.relative_to(ARTICLE)),
                         'input_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
                         'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                         'proof_environments_preserved': old.count(r'\begin{proof}')}
    (out / 'preservation.json').write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')
    return records


if __name__ == '__main__':
    print(json.dumps(prepare(), indent=2))
