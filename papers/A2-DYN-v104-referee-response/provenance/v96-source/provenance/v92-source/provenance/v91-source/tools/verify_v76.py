#!/usr/bin/env python3
"""Pin v75, preserve inherited mathematics, and assemble the full supplement."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v76 import checks, require

PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER.parent / 'A2-DYN-v75-referee-response'
BASE_TREE = '3787ef425f38505c6d715161bc045ac2eebf0609'
REVIEW = 'reviews/a2-dyn-v75-external-top4-review-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB = '01355269b3c3984bb51dca20e64dc46daa329743'
NEW = ['171_stopped_physical_roof_transport.tex', '172_optical_weights_and_morse_transport.tex',
       '173_complete_source_persistence.tex']


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=PAPER, text=True).strip()


def assemble() -> None:
    import verify_v75 as inherited
    inherited.assemble()
    target = PAPER / 'build/supplement-source.tex'
    master = target.read_text()
    old = (PAPER / 'provenance/v75-main.tex').read_text()
    abstract = old.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0]
    body = old.split('\\maketitle', 1)[1].split('\\input{journal-references}', 1)[0]
    marker = '\\part{The retained complete source and short excursions}'
    require(master.count(marker) == 1, 'inherited supplement insertion boundary')
    insert = ('\\part{Convex support and the complete physical Gauss trace}\n'
              '\\paragraph{Retained revision-75 abstract.}\n' + abstract + '\n' + body + '\n')
    master = master.replace(marker, insert + marker)
    master = master.replace('A2-DYN, revision 75; retained revision-73 and revision-74 sources',
                            'A2-DYN, revision 76; complete retained source through revision 75')
    target.write_text(master)


def source_check() -> dict:
    manifest = json.loads((PAPER / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 76 and manifest['active_core_count'] == 173, 'active revision')
    head = git('rev-parse', 'HEAD')
    require(git('rev-parse', 'HEAD:papers/A2-DYN-v75-referee-response') == BASE_TREE, 'frozen v75 tree changed')
    require(git('rev-parse', 'HEAD:' + REVIEW) == REVIEW_BLOB, 'controlling review changed')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'), 'checkout/qualification SHA mismatch')
    preserved = {}
    for folder, pattern in [('core', '*.tex'), ('appendices', '*.tex'), ('tools', '*.py')]:
        files = sorted((BASE / folder).rglob(pattern))
        for src in files:
            require(src.read_bytes() == (PAPER / src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: ' + str(src.relative_to(BASE)))
        preserved[folder] = len(files)
    require(preserved['core'] == 170, 'baseline core count')
    require(len(list((PAPER / 'core').glob('*.tex'))) == 173, 'active core count')
    for name in ('references.tex', 'journal-references.tex'):
        require((BASE / name).read_bytes() == (PAPER / name).read_bytes(), 'bibliography changed: ' + name)
    require((PAPER / 'provenance/v75-main.tex').read_bytes() == (BASE / 'main.tex').read_bytes(), 'v75 article snapshot')
    inherited = json.loads((BASE / 'SOURCE_MANIFEST.json').read_text())
    effective = {k: v for k, v in inherited.items() if isinstance(v, bool)}
    for key, value in manifest['claims'].items():
        if key in effective:
            require(value is effective[key], 'inherited claim changed: ' + key)
        effective[key] = value
    for key in ('primary_referee_request_closed', 'full_raw_return_LLT_proved',
                'collision_uniform_weighted_word_trace_decay_proved', 'independent_human_review', 'formal_proof_certificate'):
        require(effective[key] is False, 'unproved claim promoted: ' + key)
    require(json.loads((PAPER / 'PUBLICATION_STATUS.json').read_text()) == manifest['claims'], 'stale status file')
    for name in NEW:
        require((PAPER / 'core' / name).is_file(), 'missing new proof module')
    assemble()
    (PAPER / 'evidence/effective-claims.json').write_text(json.dumps(effective, indent=2, sort_keys=True) + '\n')
    hashes = {str(f.relative_to(PAPER)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in sorted(PAPER.rglob('*')) if f.is_file()
              and not set(f.relative_to(PAPER).parts) & {'build', 'evidence', '__pycache__'}}
    return {'checkout_sha': head, 'baseline_tree': BASE_TREE, 'review_blob': REVIEW_BLOB,
            'preserved': preserved, 'active_core_count': 173, 'source_sha256': hashes}


def main() -> None:
    args = sys.argv[1:]
    require(args in ([], ['--journal-only']), 'unknown verifier arguments')
    local = bool(args)
    require(not (local and os.environ.get('GITHUB_ACTIONS') == 'true'), 'journal-only mode forbidden in CI')
    (PAPER / 'build').mkdir(exist_ok=True)
    (PAPER / 'evidence').mkdir(exist_ok=True)
    result = {'revision': 76, 'finite_checks': checks(), 'formal_proof_certificate': False,
              'independent_human_review': False}
    if local:
        result['source'] = {'scope': 'local new journal files only; inherited archive and remote checkout not verified'}
    else:
        from check_v75_geometry import checks as previous_checks
        import verify_v74
        result['inherited_v75_finite_checks'] = previous_checks()
        result['inherited_v74_finite_checks'] = verify_v74.finite_checks()
        result['source'] = source_check()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
