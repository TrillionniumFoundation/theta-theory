#!/usr/bin/env python3
"""Read-only consistency audit of retrieved CI bytes, not a source or proof rerun."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ART = ROOT / 'artifact'
EXPECTED_SHA = '86c947eccea6029258d9a362624866a475118a66'
checks = []

def require(condition, label):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)

def read_json(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_identity(path, size, sha, label):
    require(path.stat().st_size == size, label + ': byte count')
    require(digest(path) == sha, label + ': SHA256')

run = read_json(ROOT / 'run-39424256218.json')
jobs = read_json(ROOT / 'jobs-39424256218.json')
artifacts = read_json(ROOT / 'artifacts-39424256218.json')
require(run['id'] == 39424256218 and run['run_attempt'] == 1, 'actual run and attempt')
require(run['status'] == 'completed' and run['conclusion'] == 'success', 'run completed successfully')
require(run['head_sha'] == EXPECTED_SHA, 'run tested the exact source commit')
require(jobs['total_count'] == len(jobs['jobs']) == 1, 'jobs page is exhaustive')
job = jobs['jobs'][0]
require(job['id'] == 118632668769 and job['head_sha'] == EXPECTED_SHA, 'job identity and source agree')
require(job['status'] == 'completed' and job['conclusion'] == 'success', 'job completed successfully')
require(all(s['status'] == 'completed' and s['conclusion'] == 'success' for s in job['steps']), 'every returned step succeeded')
require(artifacts['total_count'] == len(artifacts['artifacts']) == 1, 'artifacts page is exhaustive')
artifact = artifacts['artifacts'][0]
require(artifact['id'] == 12268508880 and not artifact['expired'], 'actual retained artifact identity')
zip_path = ROOT / 'a2-dyn-39424256218-12268508880.zip'
verify_identity(zip_path, artifact['size_in_bytes'], artifact['digest'].removeprefix('sha256:'), 'downloaded ZIP')
with zipfile.ZipFile(zip_path) as archive:
    require(archive.testzip() is None, 'all ZIP CRCs agree')
    require(len(archive.infolist()) == 207, '207 uploaded archive members')
    for item in archive.infolist():
        if not item.is_dir():
            require((ART / item.filename).read_bytes() == archive.read(item.filename), 'extracted exact bytes: ' + item.filename)
require((ART / 'current/CI_CHECKOUT_SHA.txt').read_text().strip() == EXPECTED_SHA, 'artifact checkout equals actual tested SHA')
require((ART / 'current/CI_BUILD_OUTCOME.txt').read_text().strip() == 'success', 'retained build outcome is success')
require((ART / 'current/CI_POST_RUN_STATUS.txt').read_text().strip() == '?? papers/A2-DYN-critical-source-transport-author-revision/build/', 'no source modifications reported by actual checkout')
entrypoints = (ART / 'current/CI_ENTRYPOINT_SHA256.txt').read_text()
require(digest(ROOT / 'tested-workflow-86c947ec.yml') + '  ci/a2-dyn-critical-source-transport-20261020.yml' in entrypoints, 'retrieved tested workflow equals recorded in-article workflow')

phase = read_json(ART / 'current/PHASE_all.json')
source = read_json(ART / 'current/source-checks.json')
math = read_json(ART / 'current/mathematical-checks.json')
native = read_json(ART / 'current/native-typeset.json')
for name, payload in [('phase', phase), ('source', source), ('math', math), ('typeset', native)]:
    require(payload['status'] == 'passed', name + ' receipt passed')
    require(payload['mathematical_source']['sha256'] == phase['mathematical_source']['sha256'], name + ' source identity agrees')
require(phase['continuum_proof_certificate'] is False, 'phase does not claim continuum proof')
require(math['commands_completed'] == math['commands_expected'] == len(math['commands']) == 62, '62 actual finite-check commands completed')
require(not math['failures'], 'no recorded finite-check failure')
for kind, payload, base in [('mathematics', math, ART / 'current'), ('native', native, ART / 'current/native')]:
    for command in payload['commands']:
        require(command['exit_code'] == 0, kind + ' command exit zero: ' + command['tag'])
        verify_identity(base / command['log'], command['log_bytes'], command['log_sha256'], kind + ' log: ' + command['tag'])
for comparison in math['normal_optimized_comparisons']:
    require(comparison['match'], 'recorded normal/optimized match: ' + comparison['program'] + '/' + comparison['scope'])
    suffix = '.log' if comparison['scope'] == 'stdout' else '.details.json'
    normal = ART / 'current' / (comparison['program'] + '-normal' + suffix)
    optimized = ART / 'current' / (comparison['program'] + '-optimized' + suffix)
    if comparison['comparison'] == 'byte-identical':
        require(normal.read_bytes() == optimized.read_bytes(), 'independent byte comparison: ' + comparison['program'] + '/' + comparison['scope'])
    else:
        left, right = read_json(normal), read_json(optimized)
        for key in ('executed_utc', 'optimized'):
            left.pop(key, None)
            right.pop(key, None)
        require(left == right, 'independent JSON comparison excluding only runtime timestamp/optimization: ' + comparison['program'] + '/' + comparison['scope'])
verify_identity(ART / 'current/native/main.pdf', native['pdf_bytes'], native['pdf_sha256'], 'native PDF')
require(digest(ART / 'current/native/main.aux') == native['aux_sha256'], 'native auxiliary digest')
require(native['pages'] == 211 and len(native['actual_recorder_native_tex']) == 74, 'actual 211-page native paper and 74-file TeX closure')
require(native['actual_recorder_matches_declared_closure'], 'actual TeX recorder matches closure')
require(not native['layout_or_reference_problems'], 'no driver-reported native layout/reference problems')

history = read_json(ART / 'current-history/REBUILD_SUMMARY.json')
require(history['exit_code'] == 0, 'historical assembly and build succeeded')
require(history['historical_repository_wide_gate_executed'] is False, 'historical repository-wide gate remains explicitly not executed')
verify_identity(ART / 'current-history/rebuild.stdout.log', history['log']['bytes'], history['log']['sha256'], 'historical rebuild stdout')
receipt_path, = tuple(ART.glob('current-history/execution/*/REBUILD_RECEIPT.json'))
receipt = read_json(receipt_path)
require(receipt['success'] is True and receipt['source_files_checked'] == 390, 'historical 390-source receipt succeeded')
for command in receipt['commands']:
    require(command['returncode'] == 0, 'historical command succeeded: ' + Path(command['output']).name)
    ident = command['output_identity']
    verify_identity(receipt_path.parent / Path(command['output']).name, ident['bytes'], ident['sha256'], 'historical command log: ' + Path(command['output']).name)
for document in receipt['documents']:
    ident = document['pdf']
    verify_identity(ART / 'current-history' / ('historical-' + document['document'] + '.pdf'), ident['bytes'], ident['sha256'], 'historical PDF: ' + document['document'])
    ident = document['log']
    verify_identity(receipt_path.parent / (document['document'] + '.final.log'), ident['bytes'], ident['sha256'], 'historical final log: ' + document['document'])
require([d['pages'] for d in receipt['documents']] == [26, 883], 'historical document pages 26 and 883')

summary = {
    'status': 'passed',
    'scope': 'Readback and independent byte consistency of the actual completed remote CI artifact; no source/build rerun, no continuous mathematical proof certificate.',
    'remote_run': run['html_url'],
    'run_id': run['id'], 'attempt': run['run_attempt'], 'tested_sha': EXPECTED_SHA,
    'job_id': job['id'], 'job_conclusion': job['conclusion'],
    'artifact_id': artifact['id'], 'artifact_bytes': artifact['size_in_bytes'], 'artifact_sha256': digest(zip_path),
    'mathematical_source_sha256': phase['mathematical_source']['sha256'],
    'finite_check_commands': len(math['commands']), 'normal_optimized_comparisons': len(math['normal_optimized_comparisons']),
    'native_pages': native['pages'], 'native_pdf_sha256': native['pdf_sha256'],
    'historical_pages': [d['pages'] for d in receipt['documents']],
    'native_compile_advisories': native['advisories'],
    'historical_compile_advisories': {d['document']:d['diagnostics'] for d in receipt['documents']},
    'ci_blocker_observed': False, 'source_or_workflow_repair_required': False,
    'checks_completed': len(checks), 'checks': checks,
}
(ROOT / 'ARTIFACT_VERIFICATION.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({key:value for key,value in summary.items() if key != 'checks'}, indent=2))
