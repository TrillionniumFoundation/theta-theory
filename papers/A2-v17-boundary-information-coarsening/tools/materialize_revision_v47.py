#!/usr/bin/env python3
"""Materialize the additive v47 revision, refusing any unexpected baseline."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[1]
BASE = '45b42eee377c7fd3cff81c24c95acb91d6f46ab6'
COMPILED = 'ab99196fadc20682c1ee44d6bb433a788c7274ab'
ARCHIVE = P / 'history/v46-review-baseline'
CLARIFICATION = r'''Here $b_j$ accounts only for finite-flight error in the exact signed
contact charts at the true offset $d_0$.  It does not include timing or
chart-calibration error.  Programming $j\widehat g_e+d_0$ instead gives
true offset $d_0+j(\widehat g_e-g_e)$; hard cells additionally require a
cell-edge crossing bound.  These contributions are treated separately in
Theorem~\ref{thm:v47-calibrated-confidence}.  The position pilot of
Theorem~\ref{thm:v25-observable-calibration} controls
$j|\widehat g_e-g_e|$ at this same final flight number.
'''
ABSTRACT_ADD = '''For acquisition in estimated contact frames, we separate finite-flight,
amplified onset, and cell-edge crossing errors, and obtain a charged
histogram reconstruction from a same-flight position pilot.
'''
OVERVIEW = r'''\subsection{Calibration and the finite transverse record}
\label{subsec:v47-intro-calibration}

The quantitative inverse also admits a physical acquisition in estimated
contact frames.  There are three distinct approximation errors.  A bridge
with $j$ flights contributes its relative-law error.  Programming its time
using an estimated gap contributes the amplified error
$j|\widehat g-g|$.  Replacing an exact transverse coordinate by one with
error $r$ contributes the probability of crossing a grid edge, including
an outer edge of the recorded square.  These last events are not bounded
by applying a Lipschitz test inequality to a cell indicator.

Theorem~\ref{thm:v47-calibrated-confidence} propagates the three errors
through the same law-to-table modulus, with explicit confidence and
preparation bounds.  Corollary~\ref{cor:v47-physical-histograms} gives a
finite joint prescription for the grid, the final even flight number,
the resolution of a pilot using that same flight number, and the number
of successful categories.  The post-pilot reconstruction retains only
the estimated gaps and transverse categories.  The richer physical
positions used by the pilot and the observable projection remain part
of its acquisition specification; they are not silently inserted into
the compressed inverse.

The structural input throughout is the nonlinear relative profile and
its signed finite-remainder inverse.  Offset normalization, categorical
coupling, concentration, and analytic continuation propagate this input
to different observation levels.  Their combination yields the stated
geometric and statistical consequences without identifying those
observation levels with each other.
'''
CHANGES = {
    'main.tex': '5b2b1cdff72c290674b0e910b0001dd35e202f44',
    'article/23k_quantized_law_stability_v46.tex': 'fcc9069b176ff6423652f3ad2b0812c6858137d7',
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def replace_one(text: str, old: str, new: str) -> str:
    require(text.count(old) == 1, 'Non-unique or missing edit anchor: ' + old[:80])
    return text.replace(old, new, 1)


def revised(name: str, old: str) -> str:
    if name == 'main.tex':
        text = replace_one(old, 'A2 revision 46.', 'A2 revision 47.')
        text = replace_one(text, 'A2 revision 46; complete native manuscript',
                           'A2 revision 47; complete native manuscript')
        anchor = 'modulus of the exact inverse.\n'
        text = replace_one(text, anchor, anchor + ABSTRACT_ADD)
        for anchor, addition in [
            (r'\input{article/01g_quantized_reconstruction_overview_v46}',
             r'\input{article/01h_calibration_overview_v47}'),
            (r'\input{article/23k_quantized_law_stability_v46}',
             r'\input{article/23l_calibrated_histograms_v47}')]:
            text = replace_one(text, anchor, anchor + '\n' + addition)
        return text
    anchor = (' \\Omega\\bigl(2v_g,\\,2(u_n+b_j)+C_{\\rm bin}\\delta\\bigr)\n'
              '\\end{equation}\n')
    return replace_one(old, anchor, anchor + CLARIFICATION)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-manifest', type=Path,
                        default=ROOT / 'deliveries/a2-v46' / COMPILED / 'active-source-manifest.json')
    args = parser.parse_args()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    records = {}
    for name, expected in CHANGES.items():
        source = P / name
        target = ARCHIVE / name
        original = target.read_bytes() if target.exists() else source.read_bytes()
        require(blob(original) == expected, 'Unexpected v46 object: ' + name)
        new = revised(name, original.decode()).encode()
        require(source.read_bytes() in (original, new), 'Refusing concurrent/unreviewed edit: ' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original)
        source.write_bytes(new)
        records[name] = {'before_git_blob': expected, 'after_git_blob': blob(new)}
    for source, name in [(ROOT / 'README.md', 'ROOT_README.md'), (P / 'README.md', 'README.md')]:
        target = ARCHIVE / name
        if source.exists() and not target.exists():
            target.write_bytes(source.read_bytes())
    target = ARCHIVE / 'active-source-manifest.json'
    if not target.exists():
        require(args.baseline_manifest.is_file(), 'Missing frozen active-source manifest')
        target.write_bytes(args.baseline_manifest.read_bytes())
    overview = P / 'article/01h_calibration_overview_v47.tex'
    require(not overview.exists() or overview.read_text() == OVERVIEW, 'Unexpected overview')
    overview.write_text(OVERVIEW)
    # Reuse the established Git-object retention implementation; only its
    # version-scoped CLI destination is adapted. No verifier is bypassed.
    retain = (P / 'tools/retain_native_v46.py').read_text().replace('v46', 'v47')
    (P / 'tools/retain_native_v47.py').write_text(retain)
    ledger = {'review_commit': BASE, 'compiled_baseline': COMPILED,
              'edits': records, 'new_active_modules': [
                  'article/01h_calibration_overview_v47.tex',
                  'article/23l_calibrated_histograms_v47.tex'],
              'scope': 'Additive acquisition refinement; no inherited theorem or proof removed.'}
    (ARCHIVE / 'identity.json').write_text(json.dumps(ledger, indent=2, sort_keys=True) + '\n')
    print(json.dumps(ledger, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
