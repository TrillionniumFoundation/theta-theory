#!/usr/bin/env python3
"""Activate the reviewed v65 proof without replacing any inherited proof body.

All new proof/doc/test files are already ordinary Git objects. Only the seven
listed entry/framing files are derived from their byte-exact v64 archives.
The workflow rejects any resulting paper tree other than the locally checked one.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

PAPER = Path('papers/A2-v17-boundary-information-coarsening')
ARCHIVE = PAPER/'history/v64-review-baseline'
EXPECTED_TREE = '469aba06035399f96f07417b172653228df36114'
TARGETS = {
 'main.tex': 'ad6a211d56a752580cee1ba3d96e1b8ce47bb32c',
 'rigidity.tex': '9b47898e7094344b455b239d2ea06b1132225bcf',
 'article/00_structural_introduction_v48.tex': 'ba0516f2070f81c3905ec2923104b51cc7df8fa4',
 'journal/00_principal_introduction_v61.tex': 'dddd3eb5aa01b4bd460d8c7b49179e2bcfbb9f60',
 'article/00e_periodic_mechanism_overview_v64.tex': 'afb10b8171f3a8bba3c5d3084ccd1a1331ad04f1',
 'journal/references_v56.tex': '8b05edb41c57dfb532b0465be01ea17798740336',
 'README.md': '4729f24cdfcd2371e490f719fa11b0dc96158579',
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def old(name: str) -> str:
    return (ARCHIVE/name).read_text()


def main() -> None:
    mbytes = (ARCHIVE/'SOURCE_MANIFEST.json').read_bytes()
    require(blob(mbytes) == '29bc91d07155eedb60b1cdafcd1b89ff2fc891a2', 'Wrong frozen baseline manifest')
    manifest = json.loads(mbytes)
    require(manifest['source_commit'] == 'ee2380ceb76808dd2969d6b5faaa180737020eff', 'Wrong mathematical baseline')
    for name, info in manifest['files'].items():
        data = (ARCHIVE/name if name in TARGETS else PAPER/name).read_bytes()
        require(blob(data) == info['git_blob'] and len(data) == info['bytes']
                and hashlib.sha256(data).hexdigest() == info['sha256'], 'Baseline mismatch: '+name)
        current = blob((PAPER/name).read_bytes())
        require(current == info['git_blob'] or current == TARGETS.get(name), 'Unexpected current source: '+name)

    addition = '''For a fixed marked periodic polygon, phase-resolved endpoint laws at two
positive offsets recover unequal future and past actions without flux
amplitudes.  Their actual contact response is a signed cyclic Cayley
transform at every order.  It gives a local inverse including the unknown
curvatures and, on a small complex disc, a biholomorphic inverse of the
complete analytic contact action.  A bounded analytic prior gives
conditional stability from real laws, and an orbit visiting every
labelled obstacle yields exact fixed-lattice analytic table rigidity.
'''
    for name in ('main.tex', 'rigidity.tex'):
        text = old(name).replace('revision 64', 'revision 65').replace('A2 v64', 'A2 v65')
        needle = r'\input{article/10a_periodic_itinerary_relative_v64}'
        require(text.count(needle) == 1, 'Periodic forward input must remain unique')
        text = text.replace(needle, needle+'\n'+r'\input{article/10b_periodic_contact_inverse_v65}')
        require('For alternating channels,' in text, 'Missing baseline abstract anchor')
        text = text.replace('For alternating channels,', addition+'For alternating channels,', 1)
        if name == 'rigidity.tex':
            text = text.replace(r'\enlargethispage{2pt}', r'\enlargethispage{6pt}')
        (PAPER/name).write_text(text)
    for name in ('article/00_structural_introduction_v48.tex', 'journal/00_principal_introduction_v61.tex'):
        needle = r'\input{article/00e_periodic_mechanism_overview_v64}'
        text = old(name)
        require(text.count(needle) == 1, 'Shared overview anchor')
        (PAPER/name).write_text(text.replace(needle, needle+'\n'+r'\input{article/00f_periodic_contact_overview_v65}'))
    name = 'article/00e_periodic_mechanism_overview_v64.tex'
    (PAPER/name).write_text(old(name).replace(
        'The inversion below exploits the additional geometry of an alternating\npair.',
        'The alternating inversion below exploits the additional geometry of a\ntwo-contact pair.'))
    entry = (PAPER/'v5/references_v43.tex').read_text().split(r'\bibitem{BDKL}', 1)[1].split(r'\bibitem{Hill}', 1)[0]
    name = 'journal/references_v56.tex'
    (PAPER/name).write_text(old(name).replace('\\begin{thebibliography}{99}\n', '\\begin{thebibliography}{99}\n\\bibitem{BDKL}'+entry, 1))
    (PAPER/'README.md').write_text('''# A2 revision 65: periodic contact reconstruction

The current complete English manuscripts are `rigidity.tex` (principal article),
`main.tex` (complete technical manuscript), and the retained `two_collision.tex`
companion. The principal and complete entries both include the entire new
`article/10b_periodic_contact_inverse_v65.tex` proof and its shared introduction.

Revision 65 responds to the v64 independent AI-assisted referee-style report at
`838e62dd0435f350ca9f398df09374e189a6e44c`, preserving the reviewed mathematical
source `ee2380ceb76808dd2969d6b5faaa180737020eff`. The report found no mandatory
new core correction; its principal reservation concerned exceptional significance.
This revision supplies a general-period marked contact inverse rather than
representing that editorial reservation as an arithmetic defect.

The new data are a fixed marked collision polygon, phase-resolved scaled tangent
projections, and two positive offsets. Curvatures, normal graph values and flux
amplitudes are not supplied. The inverse is local; its full analytic statement
uses a bounded-holomorphic norm. The previous gap-only alternating inverse and
all global and charged statistical results remain with their original hypotheses.

Read `RESPONSE_TO_REFEREE_V65.md`, `HISTORICAL_DERIVATION_AUDIT_V65.md`,
`LITERATURE_CHECK_V65.md`, and `journal/DEPENDENCY_LEDGER_V65.md` for the exact
claim and provenance distinctions. Source preservation and finite diagnostics
are checked by `tools/check_revision_v65.py`; numerical checks do not prove the
infinite-dimensional theorems. Native products and their exact source commit
are identified by the repository-level v65 review-ready entry after publication.

## Retained revision-64 entry (unchanged original below)

'''+old('README.md'))
    # Correct a draft literature-note given name against the primary arXiv record.
    lit = PAPER/'LITERATURE_CHECK_V65.md'
    lit.write_text(lit.read_text().replace('Jonathan Finamore', 'Douglas Finamore'))
    require(blob(lit.read_bytes()) == 'fc8e2624712ffce32851a238e75898fbc5f85215', 'Literature-note identity')
    for name, expected in TARGETS.items():
        require(blob((PAPER/name).read_bytes()) == expected, 'Derived entry mismatch: '+name)

    readme = Path('README.md'); saved = Path('README_PRE_V65.md')
    prefix = '''# A2 revision 65: marked periodic contact reconstruction

The current A2 revision is indexed in [A2_REVISION_V65_INDEX.md](A2_REVISION_V65_INDEX.md).
The principal article, full technical manuscript and companion are retained in
`papers/A2-v17-boundary-information-coarsening/`. Both principal and full entries
contain the complete new periodic contact inverse. Exact native source and product
identities are recorded in the versioned delivery and subsequent review-ready index.

The complete preceding repository entry is preserved below and in `README_PRE_V65.md`.

---

'''
    if saved.exists():
        require(readme.read_text() in (saved.read_text(), prefix+saved.read_text()), 'Unexpected repository README')
    else:
        saved.write_bytes(readme.read_bytes())
    readme.write_text(prefix+saved.read_text())
    print(json.dumps({'status': 'passed', 'baseline_files': len(manifest['files']),
        'baseline_source': manifest['source_commit'], 'expected_paper_tree': EXPECTED_TREE,
        'derived_entries': TARGETS, 'scope': 'Source activation and preservation, not proof certification.'},
        indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
