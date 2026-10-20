#!/usr/bin/env python3
"""Read-only second reconstruction of the artifact-data audit's main claims."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
CI = HERE.parents[3] / 'current-ci/actual-c2-ci'
RESULT = HERE / 'data-result'


def read(path):
    return json.loads(path.read_bytes())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_identity(data):
    return {'bytes': len(data), 'sha256': sha(data),
            'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}


def identity(path):
    data = path.read_bytes()
    return {'file': str(path.resolve()), 'bytes': len(data), 'sha256': sha(data)}


started = datetime.now(timezone.utc).isoformat()
checks = []


def require(value, description):
    checks.append({'check': description, 'passed': bool(value)})
    if not value:
        raise RuntimeError(description)


script = CI / 'verify_actual_artifact_data_only_v2.py'
strict_script = CI / 'verify_actual_ci_artifact.py'
require(sha(script.read_bytes()) == '333214be9f891b8dab1518ad2311899d94f25fe457708e6025678efe8a5a52cd',
        'Exact independent checker v2 source')
require(sha(strict_script.read_bytes()) == 'e44db871d6afaea2aaac23ec836ceb1e57993ecb464afcf884475530b1e7b42f',
        'Original strict checker byte identity is unchanged')
parsed = ast.parse(script.read_bytes())
mutations = [ast.unparse(n) for n in ast.walk(parsed) if
             isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store)
             and isinstance(n.value, ast.Name) and n.value.id == 'helpers']
main_calls = [ast.unparse(n) for n in ast.walk(parsed) if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
              and n.func.value.id == 'helpers' and n.func.attr == 'main']
require(not mutations and not main_calls, 'No helper attribute overwritten and strict main is not invoked')
observation = read(CI / 'ACTUAL_STRUCTURED_OBSERVATION_QUEUED_161007.json')
provenance = read(CI / 'ACTUAL_STRUCTURED_OBSERVATION_QUEUED_161007_PROVENANCE.json')
for key in ('run', 'jobs'):
    source = provenance['sources'][key]
    raw_path = Path(source['raw']['file'])
    parsed_path = Path(source['parsed']['file'])
    require(identity(raw_path) == source['raw'] and identity(parsed_path) == source['parsed'],
            'Exact actual API raw and parsed object identities: ' + key)
    require(read(raw_path) == read(parsed_path) == observation[key],
            'No assembled API field changed: ' + key)
artifacts_source = provenance['sources']['artifacts']
artifact_receipt = Path(artifacts_source['receipt']['file'])
require(identity(artifact_receipt) == artifacts_source['receipt'], 'Exact actual artifact GET record identity')
artifact_records = [x for x in read(artifact_receipt) if x['kind'] == 'artifacts']
require(len(artifact_records) == 1 and not artifact_records[0]['isError'], 'Exactly one actual successful artifact GET record')
require(sha(artifact_records[0]['response_text'].encode()) == artifacts_source['response_text_sha256']
        and json.loads(artifact_records[0]['response_text']) == observation['artifacts'],
        'No assembled artifact API field changed')
log_raw = read(CI / 'CI_JOB_LOG_RAW_RESPONSE.json')
log = (CI / 'CI_JOB_LOG_EXACT.log').read_bytes()
require(log_raw['response_text'].encode('utf-8') == log and log.startswith(b'\xef\xbb\xbf'),
        'Exact original job-log bytes including initial BOM')
own = read(RESULT / 'ARTIFACT_DATA_ONLY_VERIFICATION.json')
peer = read(CI / 'artifact-data-only-verification-v2/ARTIFACT_DATA_ONLY_VERIFICATION.json')
normalized_own = {k: v for k, v in own.items() if k not in {'started_utc', 'finished_utc'}}
normalized_peer = {k: v for k, v in peer.items() if k not in {'started_utc', 'finished_utc'}}
require(normalized_own == normalized_peer, 'Independent actual executions agree on every non-clock report field')
require(own['data_checks_status'] == 'passed' and own['workflow_completion_verified'] is False
        and own['actual_run_status'] == own['actual_job_status'] == 'queued'
        and own['actual_run_conclusion'] is own['actual_job_conclusion'] is None
        and own['actual_job_steps'] == [] and own['job_steps_completion_verified'] is False
        and own['synthetic_status_steps_or_timestamps_used'] is False,
        'Data validation and the fixed unresolved 16:10 API observation are explicitly separated')
first_log_timestamp = log.decode('utf-8-sig').split(' ', 1)[0]
require(first_log_timestamp == own['actual_job_log_first_timestamp'] == '2026-10-19T15:55:55.6914264Z',
        'Exact true first job-log timestamp is retained after BOM parsing correction')
strict_execution_path = CI / 'strict-verification-queued-161007/ACTUAL_VERIFIER_EXECUTION.json'
strict = read(strict_execution_path)
require(strict['exit_code'] == 1 and strict['status'] == 'failed'
        and identity(Path(strict['stderr']['file'])) == strict['stderr']
        and identity(Path(strict['stdout']['file'])) == strict['stdout'],
        'Original actual strict failure and exact stdout/stderr are retained')
require(b'RuntimeError: Actual run completed successfully' in Path(strict['stderr']['file']).read_bytes(),
        'The original completed/success gate failed, not a softened or replaced gate')
archive_path = CI / 'a2-dyn-marked-boundary-source-39281615689.zip'
require(sha(archive_path.read_bytes()) == own['artifact_sha256'], 'Exact downloaded ZIP identity')
manifest = read(RESULT / 'ARTIFACT_MEMBER_IDENTITIES.json')
with zipfile.ZipFile(archive_path) as archive:
    members = archive.infolist()
    require(len(members) == len({m.filename for m in members}) == len(manifest['files']) == 249
            and archive.testzip() is None, 'All 249 actual unique ZIP members and CRCs')
    for item in manifest['files']:
        require(file_identity(archive.read(item['path'])) == {k: item[k] for k in ('bytes', 'sha256', 'git_blob')},
                'Independently recomputed actual member identity: ' + item['path'])
    load_member = lambda name: json.loads(archive.read('build/current/' + name))
    math = load_member('mathematical-checks.json')
    require(len(math['commands']) == len({c['tag'] for c in math['commands']}) == 52,
            'Exactly 52 distinct archived mathematical commands')
    for command in math['commands']:
        log_bytes = archive.read('build/current/' + command['log'])
        require(command['exit_code'] == 0 and len(log_bytes) == command['log_bytes']
                and sha(log_bytes) == command['log_sha256']
                and load_member(command['tag'] + '.command.json') == command,
                'Actual command receipt, exit and exact output: ' + command['tag'])
    require(len(math['normal_optimized_comparisons']) == 43, 'Exactly 43 declared output comparisons')
    for item in math['normal_optimized_comparisons']:
        suffix = '.log' if item['scope'] == 'stdout' else '.details.json'
        a = archive.read('build/current/' + item['program'] + '-normal' + suffix)
        b = archive.read('build/current/' + item['program'] + '-optimized' + suffix)
        require(a == b and sha(a) == item['sha256'], 'Independent exact paired bytes: ' + item['program'] + '/' + item['scope'])
    pdf = archive.read('build/current/native/main.pdf')
    pdfinfo = subprocess.run(['pdfinfo', '-'], input=pdf, capture_output=True)
    require(pdfinfo.returncode == 0 and re.search(rb'^Pages:\s+195\s*$', pdfinfo.stdout, re.M) is not None
            and file_identity(pdf) == own['native_pdf'], 'Actual CI PDF identity and independent 195-page count')
    aux = archive.read('build/current/native/main.aux')
    require(sha(aux) == own['native_aux_sha256'] == 'ca813cb5f7103352269d49f2f67b30d33464d8fae19a4676db87228253a3a914',
            'Actual CI auxiliary-file identity matches the final local native source build')
receipt = {'schema': 1, 'scope': 'Independent read-only reconstruction of fixed artifact-data claims; no final workflow-completion assertion',
           'status': 'passed', 'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
           'program': identity(Path(__file__)), 'data_checker': identity(script), 'strict_checker': identity(strict_script),
           'strict_execution': identity(strict_execution_path), 'own_data_report': identity(RESULT / 'ARTIFACT_DATA_ONLY_VERIFICATION.json'),
           'checks': checks, 'checks_count': len(checks), 'workflow_completion_verified': False,
           'API_observation_scope': 'The unmodified 16:10:07 UTC objects. Later API observations are separate evidence, not replacements for these fields.',
           'current_commit_CI_tested': 'efde9fa6c45e7835989b653622a9870e59027530',
           'science_or_remote_modified': False, 'archive_code_executed': False}
(HERE / 'INDEPENDENT_DATA_SCOPE_CHECK.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'status': 'passed', 'checks': len(checks), 'workflow_completion_verified': False}))
