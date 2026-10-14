#!/usr/bin/env python3
"""Exact committed-source verification. No bypass modes; requires a Git checkout."""
from pathlib import Path
import json
import os
import subprocess
from check_manifest import check, require

P = Path(__file__).resolve().parents[1]
ACTIVE = 'papers/A2-DYN-v111-referee-response'
OLD = 'papers/A2-DYN-v110-referee-response'
TREE = '89ec727b370bf21d66d7086041f75d7868671d4b'
BASE = 'fb1240d2f8c0562a148d559df5a8d9c3bd2d5e39'
REPORT = 'reviews/a2-dyn-v110-persistent-guard-external-top4-review-2026-10-14/REFEREE_REPORT.md'
REPORT_BLOB = 'd57761aeb65b42940a974c8009f13ee47ffd6fce'
WORKFLOW = '.github/workflows/a2-dyn-v111-source-and-manuscript.yml'
ANCHORS = {
    '238_global_momentum_uniqueness_and_stable_weight.tex': 'c79fb9d660ab90370700c4fbfe4d4311175ac60f',
    '239_marked_pressure_comparison_and_growth.tex': 'fc76d61faeb70c0eeca6217c2c09daea4c3b2bde',
    '241_uniform_geometric_pressure_by_finite_tests.tex': 'fa0f71468d1f304da492687d949ad00c953402e7',
}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=P, text=True).strip()


def run():
    result = check()
    head = git('rev-parse', 'HEAD')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'), 'incorrect checkout SHA')
    require(git('rev-parse', 'HEAD:' + OLD) == TREE, 'original v110 packet changed')
    require(git('rev-parse', 'HEAD:' + ACTIVE + '/archive/v110') == TREE, 'historical archive differs')
    require(git('rev-parse', 'HEAD:' + REPORT) == REPORT_BLOB, 'controlling referee report changed')
    require(git('rev-parse', 'HEAD:' + ACTIVE + '/provenance/REFEREE_REPORT_v110.md') == REPORT_BLOB,
            'frozen report copy differs')
    for name, sha in ANCHORS.items():
        require(git('rev-parse', 'HEAD:' + ACTIVE + '/provenance/' + name) == sha,
                'historical proof anchor differs: ' + name)
    changes = git('diff', '--no-renames', '--name-status', BASE, head).splitlines()
    for line in changes:
        status, path = line.split('\t', 1)
        require(status == 'A', 'an inherited path was changed: ' + line)
        require(path.startswith(ACTIVE + '/') or path == WORKFLOW, 'unrelated path: ' + path)
    result.update(checkout_sha=head, original_and_archive_tree=TREE,
                  controlling_report_blob=REPORT_BLOB, added_paths=len(changes),
                  inherited_paths_modified=False, checked_historical_proof_anchors=len(ANCHORS),
                  scope='exact committed source provenance; not independent proof certification')
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
