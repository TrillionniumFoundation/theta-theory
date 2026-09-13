#!/usr/bin/env python3
"""Check the narrowly specified v39 source edits; this is not a TeX build.

The default mode reads only the edited files and the named reference targets.
--full-graph additionally requires both complete recursive native input graphs.
Neither mode claims typeset or mathematical verification.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

OLD = {
    'main.tex': 'd0f57adda8474428024d587dd102971efd1fae24',
    'article/65_envelope_minimax.tex': 'be7952808b26900ffa069c6d3788ca19d0fa1d86',
    'article/15_operator_comparison.tex': '886adb2d68e105723f41f6554eeec59391cab44c',
}
NEW = {
    'main.tex': 'f75f887804e494df63cf3fa12591cc9ccbd66409',
    'article/65_envelope_minimax.tex': '298e83b3428d595f12cc62265deb6bf61b37c892',
    'article/15_operator_comparison.tex': 'f5b656ed89bb8813f48e0e192d8222d7196a334a',
    'article/01d_proof_architecture_v39.tex': '907ec8811c103f4ba1c16d6e7295a13d5eee5547',
}
TARGETS = {
    'lem:g-relative': 'v3/10_geometry_action.tex',
    'thm:v4-factorization': 'v4/10_boundary_layers.tex',
    'thm:v8-main-relative': 'article/01c_geometric_setup_v18.tex',
    'thm:v26-density-inverse': 'article/23f_single_offset_law_inverse_v26.tex',
    'thm:v22-signed-rigidity': 'article/23a_signed_endpoint_rigidity_v27.tex',
    'eq:v25-intro-jet-block': 'article/01_introduction_v27.tex',
    'sec:v9-envelope-minimax': 'article/65_envelope_minimax.tex',
}
INPUT = re.compile(r'\\input\{([^}]+)\}')
LABEL = re.compile(r'\\label\{([^}]+)\}')
REF = re.compile(r'\\(?:eqref|ref)\{([^}]+)\}')


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_checked(path: Path, expected: str) -> str:
    raw = path.read_bytes()
    need(blob(raw) == expected, 'Unexpected source identity: ' + str(path))
    return raw.decode('utf-8')


def blocks(text: str, env: str) -> list[str]:
    return re.findall(r'\\begin\{' + env + r'\}.*?\\end\{' + env + r'\}', text, re.S)


def check(root: Path, full_graph: bool = False) -> dict:
    old = {name: read_checked(root / 'revision_history/v38' / Path(name).name, sha)
           for name, sha in OLD.items()}
    new = {name: read_checked(root / name, sha) for name, sha in NEW.items()}
    old_inputs = Counter(INPUT.findall(old['main.tex']))
    new_inputs = Counter(INPUT.findall(new['main.tex']))
    need(sum(old_inputs.values()) == 52, 'Unexpected predecessor entry count')
    need(new_inputs == old_inputs + Counter({'article/01d_proof_architecture_v39': 1}),
         'An inherited main input was removed or duplicated')
    need(blocks(old['main.tex'], 'abstract') == blocks(new['main.tex'], 'abstract'),
         'The abstract changed')
    need('\\tableofcontents' in new['main.tex'], 'Missing navigation')
    part_ii = new['main.tex'].index('\\part{Boundary information and physical local experiments}')
    for name in ('v6/10_experiment_transfer', 'article/17_adaptive_experiments_v31'):
        need(new['main.tex'].index('\\input{' + name + '}') > part_ii,
             'Statistical transfer was not placed in Part II')
    unchanged = {}
    for name in ('article/65_envelope_minimax.tex', 'article/15_operator_comparison.tex'):
        need(LABEL.findall(old[name]) == LABEL.findall(new[name]), 'Labels changed: ' + name)
        counts = {}
        for env in ('theorem', 'lemma', 'proposition', 'corollary', 'definition', 'proof'):
            a, b = blocks(old[name], env), blocks(new[name], env)
            need(a == b, 'A mathematical environment changed: ' + name + ':' + env)
            if a:
                counts[env] = len(a)
        unchanged[name] = {'labels': len(LABEL.findall(old[name])), 'environments': counts}
    name = 'article/65_envelope_minimax.tex'
    marker = 'Use the sum convention'
    need(old[name][old[name].index(marker):] == new[name][new[name].index(marker):],
         'The envelope proof or model tail changed')
    need('\\cite{A2ReviewV8}' in new['main.tex'], 'Required attribution was removed')
    need('not asserted to be exact finite-offset' in new[name], 'Model distinction is missing')
    name = 'article/15_operator_comparison.tex'
    before = ('resulting law has, in addition to the experiment comparison already\n'
              'proved, the nonlinear parity consequence established next. This\n')
    after = ('resulting law has, in addition to the experiment comparison in Part II,\n'
             'the nonlinear parity consequence established below. This\n')
    need(new[name] == old[name].replace(before, after), 'Unexpected operator-section edit')
    aux = read_checked(root / 'article/99_auxiliary_compendium_v19.tex',
                       'a596f344cd660eeaacc8e4e3eb21a0cb39610a9e')
    need(len(INPUT.findall(aux)) == 36, 'Auxiliary compendium changed')
    roadmap = new['article/01d_proof_architecture_v39.tex']
    need(set(REF.findall(roadmap)) == set(TARGETS), 'Unexpected roadmap reference set')
    for label, path in TARGETS.items():
        need(label in LABEL.findall((root / path).read_text()), 'Missing target: ' + label)
    graphs = None
    if full_graph:
        from source_provenance import graph
        graphs = {name: sorted(graph(root, name)) for name in ('main.tex', 'two_collision.tex')}
    return {
        'status': 'passed', 'scope': 'Specified source edits and named reference targets only; no TeX/PDF build',
        'old_main_direct_inputs': 52, 'new_main_direct_inputs': 53,
        'unchanged_auxiliary_direct_inputs': 36, 'abstract_byte_identical': True,
        'unchanged_mathematical_environments': unchanged,
        'new_roadmap_reference_targets_checked': sorted(TARGETS),
        'native_input_graphs': graphs, 'complete_input_graph_checked': full_graph,
        'native_build_performed': False, 'pdf_pages_visually_inspected': 0,
        'current_source_blobs': NEW, 'archived_predecessor_blobs': OLD,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--full-graph', action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.root.resolve(), args.full_graph), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
