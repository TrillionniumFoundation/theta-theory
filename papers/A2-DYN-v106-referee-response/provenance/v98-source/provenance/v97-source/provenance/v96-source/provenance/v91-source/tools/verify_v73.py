#!/usr/bin/env python3
"""Exact-source preservation and finite fixtures; not proof certification."""
from __future__ import annotations
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from fractions import Fraction as F

PAPER = Path(__file__).resolve().parents[1]
BASE_TREE = 'bd761b97e603b666ed97b27241f9ab83c7f2550b'
REVIEW_BLOB = 'f10920ea44a658b3b0ab75eac1f1d910a0946417'
MAIN_BLOB = '1856ee44ca1d30b4093926d27604858e7f887694'
MANIFEST_BLOB = 'f4831b9d8a5ca7b42c5c8a5a5c50e00f9a9362c9'
REVIEW_PATH = 'reviews/a2-dyn-v72-external-top4-review-2026-10-11/REFEREE_REPORT.md'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=PAPER, text=True).strip()


def finite_checks() -> dict[str, int]:
    counts = dict(threshold=0, paired=0, primitive=0, allocation=0, path=0, negative_controls=0)
    # Discrete signed Stieltjes fixtures test the algebra, not smooth geometry.
    for weights in [(F(1, 4), F(1, 2), F(1, 4)), (F(3, 4), F(-1, 2), F(3, 4))]:
        support = (F(1), F(3, 2), F(2))
        choices = (F(0), F(5, 4), F(7, 4), F(3))
        for n in range(1, 5):
            for margins in itertools.product(choices, repeat=n):
                product = F(1)
                for a in margins:
                    product *= sum((w for y, w in zip(support, weights) if y < a), F(0))
                mixture = F(0)
                for indices in itertools.product(range(3), repeat=n):
                    mass = F(1)
                    good = True
                    for a, i in zip(margins, indices):
                        mass *= weights[i]
                        good = good and a > support[i]
                    mixture += mass * (1 - int(good))
                require(mixture == 1 - product, 'threshold identity')
                counts['threshold'] += 1

    def value(v: tuple[F, ...], t: F) -> F:
        return next((h for i, h in enumerate(v) if i < t < i + 1), F(0))

    def integral(v: tuple[F, ...], lo: F, hi: F) -> F:
        return sum((h * max(F(0), min(hi, F(i + 1)) - max(lo, F(i)))
                    for i, h in enumerate(v)), F(0))

    def kappa(s: F, d: F) -> F:
        if -d < s < 0:
            return -(d + s) / (2 * d)
        if 0 < s < d:
            return (d - s) / (2 * d)
        return F(0)

    for raw in itertools.product(range(3), repeat=4):
        v = tuple(map(F, raw))
        jumps = (v[0], v[1] - v[0], v[2] - v[1], v[3] - v[2], -v[3])
        require(sum(jumps) == 0, 'entry and exit balance')
        for d in (F(1, 4), F(1, 2), F(1), F(2)):
            for j in range(-8, 41):
                t = F(2 * j + 1, 16)
                f = value(v, t)
                avg = integral(v, t - d, t + d) / (2 * d)
                incoming = sum((max(z, F(0)) for i, z in enumerate(jumps) if t-d <= i <= t), F(0))
                outgoing = sum((max(-z, F(0)) for i, z in enumerate(jumps) if t <= i <= t+d), F(0))
                for reserve in (F(2), F(5, 2), F(3)):
                    require(max(f - reserve * avg, F(0)) <= min(incoming, outgoing), 'paired inequality')
                    counts['paired'] += 1
                current = sum((z * kappa(t - i, d) for i, z in enumerate(jumps)), F(0))
                require(current == f - avg, 'compact primitive and signs')
                counts['primitive'] += 1

    for b, q, reserve in itertools.product(range(5), range(5), range(1, 4)):
        for s in range(b + 1):
            r = F(b - s)
            alpha = min(F(1), max(F(reserve*q-s), F(0)) / r) if r else F(0)
            controlled = F(s) + alpha*r
            residual = (1-alpha)*r
            require(controlled == min(b, max(s, reserve*q)), 'preserved allocation')
            require(controlled + residual == b, 'source completeness')
            require(0 <= residual <= max(0, b-reserve*q), 'allocation excess')
            counts['allocation'] += 1

    # A two-point space with distance two: the BL dual norm is the l1 norm.
    W = (F(1, 3), F(2, 3))
    for G, b0, b1, e0, e1 in itertools.product(range(3), range(3), range(3), range(-2, 3), range(-2, 3)):
        b = (F(b0), F(b1)); e = (F(e0, 2), F(e1, 2))
        p = tuple(G*w + z + h for w, z, h in zip(W, b, e))
        if min(p) < 0:
            continue
        scalar = abs(sum(p)-G)
        path = sum(abs(x-G*w) for x, w in zip(p, W))
        error = sum(map(abs, e))
        require(scalar <= path <= scalar+2*error, 'positive path comparison')
        counts['path'] += 1

    # Narrow pulses must survive; isolated edges need not contribute in pairs.
    width = F(1, 4); d = F(1); height = F(1)
    require(height-height*width/d == F(3, 4) > 0, 'narrow pulse not discarded')
    counts['negative_controls'] += 1
    require((-1)+1 == 0 and abs(-1)+abs(1) > 0, 'combine before Jordan')
    counts['negative_controls'] += 1
    # Signed b=(1,-1), G=2, W=(1/2,1/2), P=(2,0): scalar 0, norm 2.
    require(abs((2+0)-2) == 0 and abs(2-1)+abs(0-1) == 2, 'positivity is indispensable')
    counts['negative_controls'] += 1
    require(max(F(1)-2*F(0), F(0)) > max(F(1)-2*F(1), F(0)), 'no label pooling')
    counts['negative_controls'] += 1
    require(F(1,12)*F(1,16) == F(1,192), 'band exponent')
    for q, beta, a in ((F(0),F(1),F(1)), (F(2),F(1,2),F(3,4))):
        require(-q + ((q+a)/beta)*beta == a, 'paired power substitution')
    return counts


def source_checks() -> dict:
    require(git('rev-parse', 'HEAD:papers/A2-DYN-v72-referee-response') == BASE_TREE, 'v72 tree changed')
    require(git('rev-parse', 'HEAD:'+REVIEW_PATH) == REVIEW_BLOB, 'controlling review changed')
    head = git('rev-parse', 'HEAD')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'), 'qualification not at checkout SHA')
    old_bytes = (PAPER/'provenance/v72-main.tex').read_bytes()
    old_manifest = (PAPER/'provenance/v72-SOURCE_MANIFEST.json').read_bytes()
    require(git_blob(old_bytes) == MAIN_BLOB, 'old master snapshot changed')
    require(git_blob(old_manifest) == MANIFEST_BLOB, 'old manifest snapshot changed')
    base = PAPER.parent/'A2-DYN-v72-referee-response'
    preserved = {}
    for folder, pattern in [('core','*.tex'), ('appendices','*.tex'), ('tools','*.py')]:
        originals = sorted((base/folder).rglob(pattern))
        require(bool(originals), 'empty inherited source class: '+folder)
        for original in originals:
            copy = PAPER/original.relative_to(base)
            require(copy.is_file() and copy.read_bytes() == original.read_bytes(), 'inherited source modified: '+str(original))
        preserved[folder] = len(originals)
    require(preserved['core'] == 159, 'wrong inherited core count')
    require(len(list((PAPER/'core').glob('*.tex'))) == 163, 'wrong active core count')
    require((PAPER/'references.tex').read_bytes() == (base/'references.tex').read_bytes(), 'bibliography changed')
    active = json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    old = json.loads(old_manifest)
    authorized = {'lorentz_full_source_finite_measure_current_proved'}
    for key, value in old.items():
        if isinstance(value, bool) and key not in authorized:
            require(active.get(key) is value, 'unjustified inherited status change: '+key)
    require(active.get('lorentz_full_source_finite_measure_current_proved') is True, 'finite BV status missing')
    for key in ['lorentz_complete_current_excess_decay_proved', 'lorentz_directed_flux_power_bound_proved',
                'full_raw_return_LLT_proved', 'pointwise_roof_density_LLT_proved', 'independent_human_review',
                'formal_proof_certificate', 'lorentz_collision_uniform_current_variation_proved', 'lorentz_paired_flux_decay_proved']:
        require(active.get(key) is False, 'unproved endpoint status: '+key)

    old_text = old_bytes.decode()
    marker = '\\part{The complete physical current and source recovery}'
    require(old_text.count(marker) == 1, 'ambiguous inherited body boundary')
    before, after = old_text.split(marker)
    body = marker + after.split('\\input{references}', 1)[0]
    abstract = before.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0]
    opening = before.split('\\maketitle', 1)[1]
    front = ('\\section{The retained opening of revision 72}\n\\label{app:v73-retained-front}\n'
             'The following opening is retained as a historical statement of the preceding route. '
             'Its finite-measure qualification is superseded by Theorem~\\ref{thm:v73-full-source-bv}; '
             'its collision-uniform qualification is not. In its source notation, $e_{70}$ means '
             'first clearance outside the selected disks, with incidence separate.\n'
             '\\paragraph{Preceding abstract.}\n' + abstract + '\n' + opening)
    build = PAPER/'build'; build.mkdir(exist_ok=True)
    (build/'v72-body.tex').write_text(body)
    (build/'v72-frontmatter.tex').write_text(front)
    old_inputs = re.findall(r'\\input\{(core/[^}]+)\}', old_text)
    require(len(old_inputs) == 159 and len(set(old_inputs)) == 159, 'old input chain incomplete')
    require(re.findall(r'\\input\{(core/[^}]+)\}', body) == old_inputs, 'inherited input order changed')
    require(set(re.findall(r'\\label\{([^}]+)\}', before)) <= set(re.findall(r'\\label\{([^}]+)\}', front)), 'old front labels lost')
    master = (PAPER/'main.tex').read_text()
    require('revision 73' in master and '\\input{build/v72-body}' in master and '\\input{build/v72-frontmatter}' in master, 'wrong new master')
    for name in sorted((PAPER/'core').glob('1[6][0-3]_*.tex')):
        require('\\input{core/'+name.stem+'}' in master, 'new core not compiled: '+name.name)
    return dict(checkout_sha=head, baseline_tree=BASE_TREE, controlling_review_blob=REVIEW_BLOB,
                preserved=preserved, active_core_count=163,
                generated_tex_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in (build/'v72-body.tex',build/'v72-frontmatter.tex')})


def main() -> None:
    args = sys.argv[1:]
    require(args in ([], ['--finite-only']), 'usage: verify_v73.py [--finite-only]')
    if args:
        require(os.environ.get('GITHUB_ACTIONS') != 'true', 'finite-only mode forbidden in CI')
    result = {'revision':73, 'scope':'source preservation and finite fixtures only',
              'formal_proof_certificate':False, 'independent_human_review':False,
              'finite_checks':finite_checks()}
    if not args:
        result['source'] = source_checks()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
