#!/usr/bin/env python3
"""Strict exact-checkout provenance check. Run inside the committed repository."""
from pathlib import Path
import json
import os
import subprocess
from check_manifest import check, require

P = Path(__file__).resolve().parents[1]
ACTIVE = 'papers/A2-DYN-v110-referee-response'
OLD = 'papers/A2-DYN-v109-referee-response'
TREE = '99e677d4a40f087fc21a2c050e1cc4f43e3ef155'
BASE = 'cdf0149246de7dd6b68b0b276d9dc1c4ca5537c2'
REPORT = 'reviews/a2-dyn-v109-capacity-abundance-external-top4-review-2026-10-14/REFEREE_REPORT.md'
REPORT_BLOB = 'dac29f62397ea98f43d6229928d45faced6dbc2a'
WORKFLOW = '.github/workflows/a2-dyn-v110-source-and-manuscript.yml'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=P, text=True).strip()


def run():
    result = check()
    head = git('rev-parse', 'HEAD')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(head == os.environ.get('GITHUB_SHA'), 'not the exact requested checkout')
    require(git('rev-parse', 'HEAD:' + OLD) == TREE, 'changed original v109 tree')
    require(git('rev-parse', 'HEAD:' + ACTIVE + '/archive/v109') == TREE, 'inexact historical archive')
    require(git('rev-parse', 'HEAD:' + REPORT) == REPORT_BLOB, 'changed controlling referee report')
    require(git('rev-parse', 'HEAD:' + ACTIVE + '/provenance/REFEREE_REPORT_v109.md') == REPORT_BLOB,
            'inexact frozen referee report')
    changes = git('diff', '--no-renames', '--name-status', BASE, head).splitlines()
    for line in changes:
        status, path = line.split('\t', 1)
        require(status == 'A', 'an inherited path was modified: ' + line)
        require(path.startswith(ACTIVE + '/') or path == WORKFLOW, 'unrelated path: ' + path)
    result.update(checkout_sha=head, original_and_archive_tree=TREE,
                  controlling_report_blob=REPORT_BLOB, added_paths=len(changes),
                  historical_content_verified_by_exact_git_tree=True,
                  inherited_paths_modified=False,
                  scope='exact committed tree provenance and active bytes; not a proof certificate')
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
