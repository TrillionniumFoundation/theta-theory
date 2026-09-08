#!/usr/bin/env python3
"""Recreate redundant v23 audit expansions and v24 bibliographies offline.

All mathematical input files are ordinary repository files. This step expands
those files without fetching data or changing statements/proofs. The historical
expanded baseline is checked against the delivered v24 package's SHA-256.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / 'history/v23-source'
GENERATED = ROOT / 'history/v23-generated'


def expand(name: str, stack: tuple[Path, ...] = ()) -> str:
    p = (GENERATED / (name[6:] + '.tex') if name.startswith('build/')
         else HISTORY / (name + '.tex')).resolve()
    if p in stack or not p.is_relative_to(ROOT / 'history'):
        raise ValueError('Invalid historical input: ' + name)
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m: expand(m[1], stack + (p,)), p.read_text())


def demote(text: str) -> str:
    return (text.replace(r'\subsubsection{', r'\paragraph{')
                .replace(r'\subsection{', r'\subsubsection{')
                .replace(r'\section{', r'\subsection{'))


def main() -> None:
    baseline = expand('main').encode()
    expected = 'dd1c2a35fcdcd132d31eef01dfe5c326d0ffaf9bae05b229f25f37114aadba12'
    if hashlib.sha256(baseline).hexdigest() != expected:
        raise ValueError('Historical expanded baseline does not match v24 delivery')
    (ROOT / 'history/v23-expanded.tex').write_bytes(baseline)
    routes = {
        'structural': ['sections/structural_classification', 'sections/affine_geometry'],
        'pairings': ['sections/kernel_feasibility', 'sections/universal_attainment',
                     'sections/rectangular_attainment', 'sections/exact_kernels',
                     'sections/finite_pairing_comparison', 'sections/positive_history',
                     'sections/covariance_degenerations'],
        'additional_geometry': ['sections/circular', 'sections/operational_reconstruction',
                                'sections/directional_geometry', 'sections/uncertainty_geometry'],
        'complete_routes': ['build/collision_direct', 'build/05_confluence',
                            'build/06_streaming', 'build/06a_attainable_filtration'],
        'decisions': ['core/04_observation_algebra', 'core/07_uniform_resolution',
                      'core/08_sequential_value', 'core/09_common_risk'],
        'effective': ['sections/effective', 'build/effective_overview',
                      'sections/certified_resources', 'sections/construction_stability',
                      'sections/request_conformance'],
        'comparison': ['sections/pairing_comparison', 'sections/structural_comparison',
                       'sections/comparison'],
    }
    reconstructed = {}
    for group, sources in routes.items():
        parts = [expand(s) if group == 'comparison' or s == 'build/collision_direct'
                 else demote(expand(s)) for s in sources]
        data = '\n\n'.join(parts).encode()
        name = 'app_' + group + '.tex'
        for directory in (GENERATED, ROOT / 'text'):
            (directory / name).write_bytes(data)
        reconstructed[name] = hashlib.sha256(data).hexdigest()
    import build
    build.write_bibliographies()
    report = build.prepare()
    print(json.dumps({'historical_expansion_sha256': expected,
                      'reconstructed_audit_copies': reconstructed,
                      'preservation': report}, indent=2))


if __name__ == '__main__':
    main()
