#!/usr/bin/env python3
"""Verify and retain an actual A2 native artifact; do not certify its mathematics."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
from source_provenance import require, safe_relative, sha256, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--run-attempt', required=True)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{40}', args.source_commit) is not None,
            'Invalid source commit')
    expected_destination = Path('deliveries/a2-v43') / args.source_commit
    require(args.destination == expected_destination, 'Unexpected repository destination')
    require(not args.destination.exists(), 'Refusing to overwrite a retained product')
    evidence = args.evidence.resolve()
    report = json.loads((evidence/'build-report.json').read_text())
    require(report['status'] == 'passed' and report['source_commit'] == args.source_commit,
            'The artifact is not a passing build of the stated source')
    for name, item in report['evidence_files'].items():
        path = evidence/safe_relative(name)
        require(path.is_file() and not path.is_symlink() and
                path.stat().st_size == item['bytes'] and sha256(path) == item['sha256'],
                'Artifact file differs from the build report: ' + name)
    for stem in ('main', 'two_collision'):
        entry = report['entries'][stem]
        require(entry['status'] == 'passed' and entry['returncode'] == 0 and
                entry['source_integrity'] == 'verified', 'Native entry failed: ' + stem)
        require(sha256(evidence/(stem+'.pdf')) == entry['product']['sha256'],
                'Native PDF differs from its recorded product')
    normal = evidence/'a2-v43-preservation-normal.json'
    optimized = evidence/'a2-v43-preservation-optimized.json'
    require(normal.read_bytes() == optimized.read_bytes(), 'Preservation diagnostic mismatch')
    require(json.loads(normal.read_text())['status'] == 'passed', 'Preservation diagnostic failed')
    imported = json.loads((evidence/'main-imported-generated-inputs.json').read_text())['two_collision.aux']
    recorder = json.loads((evidence/'main-recorder-inputs.json').read_text())
    require(imported['producer_source_commit'] == args.source_commit and
            imported['sha256'] == sha256(evidence/'two_collision.aux') and
            recorder['generated_inputs']['two_collision.aux']['sha256'] == imported['sha256'],
            'Companion auxiliary producer/consumer mismatch')
    files = {}
    for path in sorted(evidence.iterdir()):
        require(path.is_file() and not path.is_symlink(), 'Unexpected artifact entry')
        require(path.suffix.lower() not in ('.ttf', '.otf', '.pfb', '.pfa', '.woff', '.woff2'),
                'Standalone font files are not distributed')
        files[path.name] = {'bytes': path.stat().st_size, 'sha256': sha256(path)}
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(evidence, args.destination)
    receipt = {
        'source_commit': args.source_commit, 'run_id': args.run_id,
        'run_attempt': args.run_attempt, 'native_build_status': 'passed',
        'visual_inspection': 'Recorded separately after the actual PDFs are rendered and examined',
        'mathematical_certification': False,
        'retention': 'Git objects on a new products-only revision branch; no existing branch overwritten',
        'files': files,
    }
    write_json(args.destination/'REPOSITORY_RETENTION.json', receipt)
    (args.destination/'README.md').write_text(
        '# A2 v43 complete native products\n\n'
        'Source commit: `' + args.source_commit + '`.\n\n'
        'This directory retains both complete native PDFs, the complete source archive, '
        'raw compiler logs and recorders, generated companion-auxiliary provenance, '
        'tool versions and finite diagnostics. `build-report.json` records the native '
        'execution; `REPOSITORY_RETENTION.json` independently hashes the retrieved artifact.\n\n'
        'These products were not made by a reduced manuscript or an integration fixture. '
        'Visual inspection is a separate signed-off record, not an assertion made by this script. '
        'A passing build and finite diagnostics do not certify the mathematical theorems '
        'or a journal acceptance decision.\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
