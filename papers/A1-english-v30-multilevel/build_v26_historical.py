#!/usr/bin/env python3
"""Build the native v26 main article and unchanged complete companion offline.

Python 3.10+. With --prepare-only, check history, routing, preservation and
exact diagnostics without TeX. Otherwise require pdflatex and pdfinfo.
No dependency is fetched and no older manuscript directory is modified.
"""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
REVIEW = 'ab0ebddd80f1e46712650eb6730e113e5c66562f'
SUBMISSION = '8a84075ee518035069d38fd9262bd455aff4ac86'
PINNED = {
    'baseline-v25-main.tex': '762cb14ad639e84251375a8f5cdea10dc2aad40f',
    'v25/graph_model.tex': '71275d8777c853fb4bc4b4cb8cb6c4edaf14beeb',
    'v25/adaptive_proof.tex': 'bfdcfe0ee88ecedfd7cc8d4d5e3a1e73d62c927d',
    'v25/graph_consequences.tex': 'e1290c9239611c067f08dd848c5ba88fe88e5fad',
    'review-basis-v25/REFEREE_REPORT.md': 'ef18197ba6213d92d41ac197bd23aa5f7e5194a9',
}


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot import ' + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bootstrap(legacy: Any) -> dict[str, Any]:
    """Reconstruct only the same redundant audit copies as the v24 builder."""
    materializer = load('_theta_v24_materializer', ROOT / 'materialize_legacy_v24.py')
    previous = sys.modules.get('build')
    sys.modules['build'] = legacy
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            materializer.main()
    finally:
        if previous is None:
            sys.modules.pop('build', None)
        else:
            sys.modules['build'] = previous
    return json.loads(output.getvalue())


def preservation(legacy: Any) -> dict[str, Any]:
    before = legacy.expand(ROOT / 'baseline-v25-main.tex') + '\n' + legacy.expand(ROOT / 'companions.tex')
    after = legacy.expand(ROOT / 'main.tex') + '\n' + legacy.expand(ROOT / 'companions.tex')
    result: dict[str, Any] = {}
    for name, environments in [('statements', legacy.FORMAL), ('proofs', ('proof',)),
                               ('definitions_and_remarks', ('definition', 'remark'))]:
        old, new = legacy.blocks(before, environments), legacy.blocks(after, environments)
        if old - new or any(new[key] != count for key, count in old.items()):
            raise ValueError('An inherited block changed, disappeared or was duplicated: ' + name)
        result[name] = {'preserved_byte_identical': sum(old.values()),
                        'added': sum((new-old).values())}
    old_labels = set(legacy.labels(before))
    if old_labels-set(legacy.labels(after)):
        raise ValueError('An inherited label disappeared')
    result['inherited_labels_preserved'] = len(old_labels)
    result['scope'] = 'Expanded source identity and exact multiplicity, not theorem correctness.'
    return result


def diagnostics() -> dict[str, Any]:
    outputs = []
    for options in ([], ['-O']):
        command = [sys.executable, *options, str(ROOT / 'diagnostics.py')]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 timeout=180, check=False)
        if process.returncode:
            raise RuntimeError('Diagnostics failed: ' + process.stderr)
        outputs.append(process.stdout)
    if outputs[0] != outputs[1]:
        raise RuntimeError('Normal and optimized diagnostic outputs differ')
    receipt = json.loads(outputs[0])
    if receipt.get('status') != 'passed':
        raise RuntimeError('Diagnostics did not return a success result')
    (ROOT / 'DIAGNOSTICS.json').write_text(outputs[0], encoding='utf-8')
    return {'normal_and_optimized_byte_identical': True, 'receipt': receipt}


def execute(prepare_only: bool) -> dict[str, Any]:
    for name, expected in PINNED.items():
        if blob((ROOT/name).read_bytes()) != expected:
            raise ValueError('Pinned source identity mismatch: ' + name)
    legacy = load('_theta_v24_build', ROOT / 'build_legacy_v24.py')
    inherited = bootstrap(legacy)
    retained = preservation(legacy)
    tests = diagnostics()
    latex = None if prepare_only else legacy.build()
    paths = [ROOT/'main.tex', ROOT/'build.py', ROOT/'diagnostics.py',
             *sorted((ROOT/'v26').glob('*.tex')), ROOT/'v25/references.tex']
    return {'version': 26, 'status': 'passed', 'build_executed': not prepare_only,
            'controlling_review_commit': REVIEW, 'reviewed_submission_commit': SUBMISSION,
            'pinned_git_blobs': PINNED, 'v25_and_companion_preservation': retained,
            'inherited_materialization_and_v23_audit': inherited,
            'diagnostics': tests, 'two_volume_latex_receipt': latex,
            'source_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in paths},
            'scope': 'Only executed source/tests/build checks; nested v24/v23 labels retain their historical meaning. Not independent peer review, a priority judgment, or formal proof certification.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    target = ROOT / ('PRESERVATION_REPORT_V26.json' if args.prepare_only else 'BUILD_REPORT_V26.json')
    target.unlink(missing_ok=True)
    try:
        report = execute(args.prepare_only)
    except Exception as exc:
        failure = {'version':26,'status':'failed','error':str(exc),
                   'scope':'No successful build is asserted by this failure record.'}
        (ROOT/'BUILD_FAILURE_V26.json').write_text(json.dumps(failure,indent=2)+'\n')
        raise
    target.write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'BUILD_FAILURE_V26.json').unlink(missing_ok=True)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
