#!/usr/bin/env python3
"""A2 v69 retention and finite mathematical/ZIP controls; not a proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import math
import re
import stat
import tempfile
import zipfile

from check_revision_v68 import (
    require, blob, inverse, weighted_controls, nonlinear_visit_controls,
    polynomial_and_quotient_controls, flat_controls,
    preceding_mathematical_controls,
)
from source_provenance import source_archive
from verify_source_zip_v69 import verify as verify_zip, extract as extract_zip

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'history/v68-review-baseline'
NEW = 'article/10e_sampled_smooth_recovery_v69.tex'
EDITED = {
    'README.md', 'main.tex', 'rigidity.tex',
    'article/00h_abstract_v66.tex', 'article/00g_contact_synthesis_v66.tex',
    'journal/references_v56.tex', 'v5/references_v43.tex',
    'tools/source_provenance.py',
}

def active(entry: str, old: bool = False, found: set[str] | None = None) -> set[str]:
    found = set() if found is None else found
    if entry in found:
        return found
    found.add(entry)
    path = (BASE if old and entry in EDITED else ROOT) / entry
    require(path.is_file(), 'Missing native input: ' + entry)
    text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text())
    for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', text):
        active(name if name.endswith('.tex') else name + '.tex', old, found)
    return found


def source_checks() -> dict:
    records = json.loads((BASE / 'SOURCE_MANIFEST.json').read_text())['files']
    require(len(records) == 876, 'Unexpected v68 baseline size')
    unchanged, archived, labels, readonly = 0, [], 0, 0
    for name, rec in records.items():
        current = ROOT / name
        require(current.is_file() and not current.is_symlink(), 'Removed inherited source: ' + name)
        expected = BASE / name if name in EDITED else current
        data = expected.read_bytes()
        require(len(data) == rec['bytes'] and hashlib.sha256(data).hexdigest() == rec['sha256']
                and blob(data) == rec['git_blob'], 'Baseline byte identity failed: ' + name)
        mode = int(rec['mode'], 8) & 0o777
        actual_mode = stat.S_IMODE(current.stat().st_mode)
        archive_mode = stat.S_IMODE(expected.stat().st_mode)
        if actual_mode == 0o444 and archive_mode == 0o444:
            readonly += 1  # freeze_git_source deliberately makes every snapshot file read-only.
        else:
            require(actual_mode == mode and archive_mode == mode, 'Mode changed: ' + name)
        if name in EDITED:
            require(current.read_bytes() != data, 'Unnecessarily archived unedited path: ' + name)
            archived.append(name)
            if name.endswith('.tex'):
                now = current.read_text()
                for label in re.findall(r'\\label\{([^}]+)\}', data.decode()):
                    require('\\label{' + label + '}' in now, 'Removed inherited label: ' + label)
                    labels += 1
        else:
            unchanged += 1
    require(set(archived) == EDITED, 'Archive inventory mismatch')
    require(readonly in (0, len(records)), 'Mixed immutable/working-tree mode policy')
    old = {e: active(e + '.tex', True) for e in ('main', 'rigidity', 'two_collision')}
    new = {e: active(e + '.tex') for e in old}
    for e in old:
        expected = {NEW} if e != 'two_collision' else set()
        require(old[e] <= new[e] and new[e] - old[e] == expected,
                'Unintended active-input change: ' + e)
    smooth = (ROOT / NEW).read_text()
    needed = ('lem:v69-density-estimation', 'thm:v69-successful-samples',
              'thm:v69-charged-recovery', 'eq:v69-selection',
              'eq:v69-density-bound', 'eq:v69-budget-rate')
    for label in needed:
        require('\\label{' + label + '}' in smooth, 'Missing new proof statement: ' + label)
    old_correction = (ROOT / 'article/10c_global_curvature_inverse_v66.tex').read_text()
    for label in ('eq:v67-residual-error', 'eq:v67-complete-stopping-error',
                  'eq:v67-off-fixed-recursion', 'eq:v67-propagation-constants'):
        require('\\label{' + label + '}' in old_correction, 'Lost v67 correction: ' + label)
    return {'inherited_files': len(records), 'inherited_unchanged': unchanged,
            'edited_originals_archived_exactly': sorted(archived),
            'inherited_labels_retained_in_edited_tex': labels,
            'active_by_entry': {e: len(v) for e, v in new.items()},
            'active_union': len(set().union(*new.values())),
            'old_active_union': len(set().union(*old.values())),
            'sole_added_active_input': NEW,
            'mode_scope': ('Read-only frozen copies; original Git modes checked by the source manifest and materializer'
                           if readonly else 'Original filesystem modes verified against the reviewed manifest')}


def moment_controls() -> dict:
    # Rational moments of (1-t^2)^8 on [-1,1], sufficient for finite controls.
    # The paper uses an infinitely smooth bump; these computations test the
    # moment algebra, not regularity of that separate kernel construction.
    def moment(k):
        if k % 2:
            return F(0)
        return sum((F((-1)**j * math.comb(8, j) * 2, k + 2*j + 1)
                    for j in range(9)), F(0))
    cases = 0
    for order in range(1, 7):
        matrix = [[moment(i+j) for j in range(order)] for i in range(order)]
        inv = inverse(matrix)
        c = [row[0] for row in inv]
        for degree in range(order):
            value = sum((c[j]*moment(degree+j) for j in range(order)), F(0))
            require(value == (1 if degree == 0 else 0), 'Moment cancellation failed')
            cases += 1
    return {'orders': 6, 'exact_moment_equalities': cases,
            'scope': 'finite rational kernel algebra, not density-estimation proof'}


def exponent_controls() -> dict:
    count = 0
    for m in range(3, 11):
        for s in range(1, 6):
            D = F(2*(m+s)+2)
            alpha = F(s)/D
            gamma = F(s, m+s+3)
            require(F(1,2)-F(m+1)/D == alpha, 'Variance balance')
            require(1-F(m+2)/D >= alpha, 'Linear term not dominated')
            require(1-F(m+3, m+s+3) == gamma, 'Noise balance')
            for omega in (F(1,10), F(1), F(3)):
                for rare in (F(1,5), F(2), F(7)):
                    beta = alpha*omega/(omega+alpha*rare)
                    length = alpha/(omega+alpha*rare)
                    require(omega*length == beta, 'Truncation budget exponent')
                    require(alpha*(1-rare*length) == beta, 'Charged sample exponent')
                    require(0 < beta < alpha < 1, 'Invalid rate exponent')
                    count += 1
    # A deliberately uncharged exponent must fail the charged balance.
    a = F(1,10)
    require(a != a/(1+2*a), 'Rarity-negative control did not distinguish exponents')
    return {'exact_parameter_cases': count, 'uncharged_rate_negative_control': 'detected'}


def mixture_controls() -> dict:
    # Enumerate finite independent trials with failure/A/B outcomes.  Conditional
    # on any adequate success-indicator sequence, the first two marks have the
    # same product distribution.  No simulation or removable assertion is used.
    count = 0
    for B in range(2, 7):
        for p, q in ((F(1,3),F(2,5)), (F(3,4),F(1,7))):
            masses = {}
            probabilities = (1-p, p*q, p*(1-q))
            for seq in itertools.product(range(3), repeat=B):
                indicators = tuple(x != 0 for x in seq)
                if sum(indicators) < 2:
                    continue
                marks = tuple(x for x in seq if x != 0)[:2]
                probability = math.prod(probabilities[x] for x in seq)
                key = (indicators, marks)
                masses[key] = masses.get(key, F(0)) + probability
            for indicators in {key[0] for key in masses}:
                k = sum(indicators)
                base = p**k*(1-p)**(B-k)
                for marks in itertools.product((1,2), repeat=2):
                    target = base*math.prod(q if x == 1 else 1-q for x in marks)
                    require(masses.get((indicators, marks), F(0)) == target,
                            'Conditional successful marks not product distributed')
                    count += 1
    return {'exact_conditional_mark_equalities': count,
            'scope': 'finite mixture identity; not a billiard or infinite-sequence simulation'}


def zip_controls() -> dict:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        snap = root/'snapshot'
        snap.mkdir()
        files = {}
        for name, data, mode in (
            ('script.py', b'print("control")\n', '100755'),
            ('plain.tex', b'control\n', '100644'),
        ):
            path = snap/name
            path.write_bytes(data)
            path.chmod(0o444)
            files[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                           'git_blob': blob(data), 'mode': mode}
        archive = root/'source.zip'
        source_archive(snap, {'files': files}, archive)
        report = verify_zip(archive)
        require(report['executable_paths'] == ['script.py'], 'Executable mode not retained')
        extract_zip(archive, root/'restored')
        require(stat.S_IMODE((root/'restored/source/script.py').stat().st_mode) == 0o755,
                'Executable extraction failed')
        corrupted = root/'corrupted.zip'
        with zipfile.ZipFile(archive) as src, zipfile.ZipFile(corrupted,'w') as dst:
            for info in src.infolist():
                if info.filename == 'source/script.py':
                    info.external_attr = 0o100644 << 16
                dst.writestr(info, src.read(info))
        caught = False
        try:
            verify_zip(corrupted)
        except ValueError as exc:
            caught = 'ZIP mode discrepancies' in str(exc)
        require(caught, 'Incorrect raw ZIP mode was not rejected')
    return {'readonly_snapshot_modes': 'preserved from manifest',
            'mode_restoration': 'verified', 'corrupted_header_negative_control': 'detected'}


def main() -> None:
    report = {
        'scope': 'Author-side exact finite controls and source retention; not proof certification',
        'source': source_checks(),
        'kernel_moments': moment_controls(),
        'rate_algebra': exponent_controls(),
        'successful_mark_mixture': mixture_controls(),
        'zip_permissions': zip_controls(),
        'retained_v68': {
            'preceding': preceding_mathematical_controls(),
            'weighted': weighted_controls(),
            'nonlinear_visits': nonlinear_visit_controls(),
            'polynomial_quotient': polynomial_and_quotient_controls(),
            'flat': flat_controls(),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
