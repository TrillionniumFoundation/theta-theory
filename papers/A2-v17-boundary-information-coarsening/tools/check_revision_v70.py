#!/usr/bin/env python3
"""v70 source conservation and authentic v69 finite controls; not proof certification."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from source_provenance import INPUT, blob_id, require, safe_relative, strip_comments

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'history/v69-review-baseline'
EDITED = {'README.md', 'main.tex', 'rigidity.tex',
          'journal/00_principal_introduction_v61.tex',
          'article/00_structural_introduction_v48.tex'}
CORE = ('article/10a_periodic_itinerary_relative_v64.tex',
        'article/10b_periodic_contact_inverse_v65.tex',
        'article/10c_global_curvature_inverse_v66.tex',
        'article/10d_smooth_contact_rigidity_v68.tex',
        'article/10e_sampled_smooth_recovery_v69.tex')
ENTRIES = ('main.tex', 'rigidity.tex', 'two_collision.tex')


def baseline_path(name: str) -> Path:
    return (BASE if name in EDITED else ROOT) / safe_relative(name)


def active(entry: str, old: bool = False, found: set[str] | None = None) -> set[str]:
    found = set() if found is None else found
    if entry in found:
        return found
    found.add(entry)
    path = baseline_path(entry) if old else ROOT / safe_relative(entry)
    require(path.is_file() and not path.is_symlink(), 'Missing TeX input: ' + entry)
    for child in INPUT.findall(strip_comments(path.read_text(encoding='utf-8'))):
        active(child if child.endswith('.tex') else child + '.tex', old, found)
    return found


def matches(data: bytes, record: dict) -> bool:
    return (len(data) == record['bytes'] and blob_id(data) == record['git_blob']
            and hashlib.sha256(data).hexdigest() == record['sha256'])


def source_checks(records: dict) -> dict:
    require(len(records) == 895, 'Wrong reviewed source inventory')
    changed = []
    for name, record in records.items():
        current, original = ROOT / name, baseline_path(name)
        require(current.is_file() and not current.is_symlink(), 'Removed source: ' + name)
        require(original.is_file() and not original.is_symlink(), 'Missing original: ' + name)
        require(matches(original.read_bytes(), record), 'Original identity changed: ' + name)
        expected_mode = int(record['mode'], 8) & 0o777
        for path in (current, original):
            mode = stat.S_IMODE(path.stat().st_mode)
            require(mode in (expected_mode, 0o444), 'Changed source mode: ' + name)
        if not matches(current.read_bytes(), record):
            changed.append(name)
    require(set(changed) == EDITED, 'Unexpected inherited edits: ' + repr(changed))
    for name in CORE:
        require(matches((ROOT / name).read_bytes(), records[name]), 'Changed core proof: ' + name)
    old = {e: active(e, True) for e in ENTRIES}
    new = {e: active(e) for e in ENTRIES}
    old_union, new_union = set().union(*old.values()), set().union(*new.values())
    require(len(old_union) == 136 and old_union <= new_union, 'Lost inherited active input')
    added = {'article/00i_main_thesis_v70.tex', 'article/00j_abstract_v70.tex'}
    require(new_union - old_union == added, 'Unexpected new active input')
    require(old['two_collision.tex'] == new['two_collision.tex'], 'Changed companion input graph')
    require(old['main.tex'] <= new['main.tex'], 'Lost complete-manuscript input')
    principal_except_old_abstract = old['rigidity.tex'] - {'article/00h_abstract_v66.tex'}
    require(principal_except_old_abstract <= new['rigidity.tex'], 'Lost principal proof input')
    for entry in ('main.tex', 'rigidity.tex'):
        text = (ROOT / entry).read_text(encoding='utf-8')
        positions = [text.index('\\input{' + x[:-4] + '}') for x in CORE]
        require(positions == sorted(positions), 'Core proof order changed')
        require(text.index('\\input{article/00i_main_thesis_v70}') < positions[0], 'Missing lead')
        require(positions[-1] < text.index('\\input{article/01c_geometric_setup_v43}'),
                'Core no longer precedes foundations')
        intro = ('journal/00_principal_introduction_v61' if entry == 'rigidity.tex'
                 else 'article/00_structural_introduction_v48')
        require(text.index('\\appendix') < text.index('\\input{' + intro + '}'),
                'Retained introduction is not in the printed appendix')
    for name in ('journal/00_principal_introduction_v61.tex',
                 'article/00_structural_introduction_v48.tex'):
        old_text = baseline_path(name).read_text(encoding='utf-8')
        require((ROOT / name).read_text(encoding='utf-8') == old_text.replace(
            '\\section{Introduction}', '\\section{Further formulations and comparisons}', 1),
            'More than the retained introductory section heading changed')
    example = records[CORE[0]]
    require(not matches((ROOT / CORE[0]).read_bytes() + b'corruption', example),
            'Byte-corruption control not detected')
    require(not (old_union <= new_union - {CORE[0]}), 'Input-deletion control not detected')
    return {'review_commit': 'ba42d7a3a7873739c596497c5b2b884452f130d1',
            'reviewed_source_commit': '1a46fd69a508bccb90c6d2553892124f068f4657',
            'reviewed_source_tree': 'e0c2434849fe72a715cec1fae5e6e36bf90b5669',
            'inherited_files': len(records), 'inherited_unchanged': len(records)-len(changed),
            'edited_originals_archived_exactly': sorted(changed),
            'unchanged_core_proof_modules': list(CORE),
            'old_active_union': len(old_union), 'active_union': len(new_union),
            'active_by_entry': {e: len(v) for e, v in new.items()},
            'added_active_inputs': sorted(added),
            'negative_controls': {'byte_corruption': 'detected', 'input_deletion': 'detected'},
            'mode_scope': 'Git modes on materialized sources; read-only copies allowed only for build snapshots'}


def authentic_v69_controls(records: dict) -> dict:
    # Reconstruct the reviewed bytes instead of running an old structural
    # checker against the reorganized v70 entry points or editing that checker.
    with tempfile.TemporaryDirectory(prefix='a2-v69-controls-') as temporary:
        root = Path(temporary)
        for name, record in records.items():
            path = root / safe_relative(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            data = baseline_path(name).read_bytes()
            require(matches(data, record), 'Unverified historical diagnostic input: ' + name)
            path.write_bytes(data)
            path.chmod(int(record['mode'], 8) & 0o777)
        command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
        cp = subprocess.run(command + [str(root / 'tools/check_revision_v69.py')],
                            cwd=root, capture_output=True, text=True, check=False)
        require(cp.returncode == 0, 'Authentic v69 diagnostic failed: ' + cp.stderr)
        result = json.loads(cp.stdout)
    return {'execution_scope': 'unchanged v69 checker in reconstructed reviewed source bytes and modes',
            'result': result}


def main() -> None:
    records = json.loads((BASE / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))['files']
    print(json.dumps({'scope': 'Author-side source conservation and finite controls, not theorem certification',
                      'source': source_checks(records),
                      'authentic_v69': authentic_v69_controls(records)}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
