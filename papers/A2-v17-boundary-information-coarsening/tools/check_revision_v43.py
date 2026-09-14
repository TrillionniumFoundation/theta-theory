#!/usr/bin/env python3
"""Check the v43 source delta and references, not mathematical correctness.

The immutable v42 active-blob ledger came from the authenticated, exact-head
native build. Historical files are checked before comparison. This program
neither calls TeX nor calls a numerical test a proof.
"""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import re
from source_provenance import blob_id, graph, require, strip_comments

ROOT = Path(__file__).resolve().parents[1]
BASE = 'history/v42-review-baseline/main.tex'
REPLACEMENTS = {
    'article/01c_geometric_setup_v18.tex': 'article/01c_geometric_setup_v43.tex',
    'article/18b0_anchored_realization_v22.tex': 'article/18b0_anchored_realization_v43.tex',
    'article/18d1_intrinsic_count_geometry_v24.tex': 'article/18d1_intrinsic_count_geometry_v43.tex',
    'article/18c1_endpoint_time_deficiency_v25.tex': 'article/18c1_endpoint_time_deficiency_v43.tex',
    'article/23d_rank_two_lattice_recovery_v24.tex': 'article/23d_rank_two_lattice_recovery_v43.tex',
    'v5/references_v41.tex': 'v5/references_v43.tex',
}
STATEMENTS = re.compile(
    r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}'
    r'.*?\\end\{\1\}', re.S)
LABEL = re.compile(r'\\label\{([^}]+)\}')
REFERENCE = re.compile(r'\\(?:eqref|ref|pageref|autoref)\*?\{([^}]+)\}')
CITATION = re.compile(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}')
BIBITEM = re.compile(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}')
INPUT = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')


def statements(text: str) -> list[tuple[str, str]]:
    return [(m[1], m[0]) for m in STATEMENTS.finditer(text)]


def audit() -> dict:
    ledger = json.loads((ROOT/'history/v42-review-baseline/ACTIVE_BLOBS.json').read_text())
    for name, expected in ledger['active_blobs'].items():
        path = ROOT / (BASE if name == 'main.tex' else name)
        require(path.is_file() and blob_id(path.read_bytes()) == expected,
                'Historical active blob changed: ' + name)
    old_graph = graph(ROOT, BASE)
    current_graph = graph(ROOT, 'main.tex')
    transported = {('main.tex' if name == BASE else REPLACEMENTS.get(name, name))
                   for name in old_graph}
    require(transported == current_graph, 'The full input closure was not preserved')
    old_main = (ROOT/BASE).read_text()
    new_main = (ROOT/'main.tex').read_text()
    old_inputs = INPUT.findall(strip_comments(old_main))
    expected_inputs = [REPLACEMENTS.get(name + '.tex', name + '.tex')[:-4]
                       for name in old_inputs]
    require(expected_inputs == INPUT.findall(strip_comments(new_main)),
            'Native direct input order changed beyond the declared substitutions')
    total = collections.Counter()
    before_lines = after_lines = 0
    for old in sorted(old_graph):
        new = 'main.tex' if old == BASE else REPLACEMENTS.get(old, old)
        a, b = (ROOT/old).read_text(), (ROOT/new).read_text()
        require(statements(a) == statements(b), 'A mathematical statement changed: ' + old)
        total.update(kind for kind, _ in statements(a))
        before_lines += len(a.splitlines())
        after_lines += len(b.splitlines())
    original_bib = (ROOT/'v5/references_v41.tex').read_text()
    revised_bib = (ROOT/'v5/references_v43.tex').read_text()
    require(revised_bib.replace('\\allowbreak ', '') == original_bib,
            'Bibliography changed beyond invisible line-break opportunities')
    old_rank = (ROOT/'article/23d_rank_two_lattice_recovery_v24.tex').read_text()
    new_rank = (ROOT/'article/23d_rank_two_lattice_recovery_v43.tex').read_text()
    require('\\ref{lem:v40-signature-rigid-rerooting}' in new_rank,
            'The detailed common-frame cross-reference is missing')
    require(len(new_rank) > len(old_rank), 'The detailed proof was shortened')
    text = '\n'.join(strip_comments((ROOT/p).read_text()) for p in sorted(current_graph))
    labels = LABEL.findall(text)
    duplicates = sorted(k for k,v in collections.Counter(labels).items() if v > 1)
    companion_labels = {'TC-' + k for k in LABEL.findall(
        strip_comments((ROOT/'two_collision.tex').read_text()))}
    missing = sorted(set(REFERENCE.findall(text)) - set(labels) - companion_labels)
    cited = {key.strip() for item in CITATION.findall(text) for key in item.split(',')}
    missing_citations = sorted(cited - set(BIBITEM.findall(text)))
    require(not duplicates, 'Duplicate static labels: ' + ', '.join(duplicates))
    require(not missing, 'Unresolved static references: ' + ', '.join(missing))
    require(not missing_citations, 'Unresolved static citations: ' + ', '.join(missing_citations))
    require('A2 revision 43; complete native manuscript' in new_main,
            'Incorrect current PDF version metadata')
    return {
        'revision': 'A2 v43', 'status': 'passed',
        'reviewed_source_commit': ledger['reviewed_source_commit'],
        'review_commit': ledger['review_commit'],
        'verified_historical_active_blobs': len(ledger['active_blobs']),
        'main_recursive_tex_files': len(current_graph),
        'companion_recursive_tex_files': len(graph(ROOT, 'two_collision.tex')),
        'main_direct_inputs': len(old_inputs),
        'auxiliary_direct_inputs': len(INPUT.findall(strip_comments(
            (ROOT/'article/99_auxiliary_compendium_v19.tex').read_text()))),
        'source_statements_byte_identical': dict(sorted(total.items())),
        'source_statement_total': sum(total.values()),
        'active_main_source_lines_before': before_lines,
        'active_main_source_lines_after': after_lines,
        'replaced_inputs': REPLACEMENTS,
        'bibliography_content': 'unchanged; only invisible allowbreak tokens inserted',
        'static_labels': len(labels), 'static_citations': len(cited),
        'duplicate_static_labels': duplicates, 'missing_static_references': missing,
        'missing_static_citations': missing_citations,
        'optimization_independence': 'Explicit exceptions, not assert statements',
        'scope': 'Source preservation and static reference diagnostics only; not a TeX run, PDF inspection, or mathematical proof certificate',
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
