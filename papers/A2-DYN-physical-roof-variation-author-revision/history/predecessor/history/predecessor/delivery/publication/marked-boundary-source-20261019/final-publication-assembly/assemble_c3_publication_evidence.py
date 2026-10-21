#!/usr/bin/env python3
"""Append actual, sealed publication evidence; never change scientific inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=Path, required=True)
parser.add_argument('--supplement', required=True, help='New publication subdirectory containing LATEST_CI_SCOPE.json')
args = parser.parse_args()
workspace = args.workspace.resolve()
repo = workspace / 'theta-theory'
recovery = workspace / 'iteration-20261019c-recovery'
article_path = 'papers/A2-DYN-marked-boundary-source-author-revision'
article = repo / article_path
prefix = 'delivery/publication/marked-boundary-source-20261019'
publication = article / prefix
assembly = publication / 'final-publication-assembly'
assert not assembly.exists(), 'Do not replace an existing evidence assembly'
assert '/' not in args.supplement and args.supplement not in ('', '.', '..')
C1 = '409fc85c84a5f239d071b8452da48cb73694365f'
C2 = 'efde9fa6c45e7835989b653622a9870e59027530'
C2_ROOT = 'b5d618b8a4b356f8ca07f1c9f1238e35d879ede8'
C2_ARTICLE = 'b4add0580cc8211223dfa57e6e618e2bf9546d09'
FROZEN = '0d4439dc86fab1f1226b41506c67a0069edbe21ea9bfd741a099d725fd94f143'
MATH = 'ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5'
MUTABLE = {'PUBLICATION_STATUS.json', 'PUBLICATION_RECEIPT.json', 'REMOTE_TRANSPORT_STATUS.md'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode()
    path.write_bytes(data)
    assert path.read_bytes() == data

def identity(path):
    data = path.read_bytes()
    return {'path': path.relative_to(article).as_posix(), 'bytes': len(data), 'sha256': sha(data), 'git_blob': git_blob(data)}

def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=repo)

assert git('rev-parse', C2 + '^{tree}').decode().strip() == C2_ROOT
assert git('rev-parse', C2 + ':' + article_path).decode().strip() == C2_ARTICLE
assert sha((article / 'SOURCE_MANIFEST.json').read_bytes()) == FROZEN
before = []
for record in git('ls-tree', '-rz', C2 + ':' + article_path).split(b'\0'):
    if not record:
        continue
    head, raw_path = record.split(b'\t', 1)
    mode, kind, expected = head.decode().split()
    relative = raw_path.decode()
    assert kind == 'blob' and mode in ('100644', '100755')
    path = article / relative
    data = path.read_bytes()
    assert git_blob(data) == expected, ('C2 input changed before evidence assembly', relative)
    before.append({'path': relative, 'mode': mode, 'git_blob': expected})
assert len(before) == 3596
for name in MUTABLE:
    assert (article / name).read_bytes() == (publication / 'metadata-at-tested-C2' / name).read_bytes()
workflow = repo / '.github/workflows/a2-dyn-marked-boundary-source-20261019.yml'
assert git_blob(workflow.read_bytes()) == '56e44c7a4e978494c5dba8df023bef5fc8b7cfa4'

summary_path = publication / 'actual-c2-ci/CURRENT_CI_SCOPE_SUMMARY.json'
assert sha(summary_path.read_bytes()) == 'b553a1c4e6fe4e822df3a51fcdd5e6b6d434c2923456f0ce167095114ad50e93'
summary = json.loads(summary_path.read_bytes())
late_path = publication / args.supplement / 'LATEST_CI_SCOPE.json'
late = json.loads(late_path.read_bytes())
assert late['head_sha'] == C2
assert late['run_id'] == 39281615689 and late['job_id'] == 118156848926 and late['artifact_id'] == 12201151164
assert summary['exact_head'] == C2 and summary['mathematical_source_sha256'] == MATH
assert summary['data_checks_status'] == 'passed' and summary['workflow_completion_verified'] is False
complete = late['workflow_completion_verified']
assert isinstance(complete, bool)
if complete:
    assert late['run_status'] == late['job_status'] == 'completed'
    assert late['run_conclusion'] == late['job_conclusion'] == 'success'
    assert late['strict_execution']['exit_code'] == 0

actual_c2 = json.loads((publication / 'actual-c2-publication-audit/INDEPENDENT_C2_PUBLICATION_AUDIT.json').read_bytes())
assert actual_c2['status'] == 'passed' and actual_c2['commit'] == C2
assert len(actual_c2['three_refs_as_observed']) == 3 and set(actual_c2['three_refs_as_observed'].values()) == {C2}
assembly.mkdir(parents=True)
helpers = [
    'append_sealed_publication_packet.py',
    'prepare_c2_ci_trigger_evidence.py',
    'preserve_tested_c2_publication_metadata.py',
    'assemble_c3_publication_evidence.py',
]
for name in helpers:
    save(assembly / name, (recovery / name).read_bytes())

now = datetime.now(timezone.utc).isoformat()
completion_text = ('The later actual completed/success metadata and an unchanged strict-verifier execution both passed.' if complete else
                   'The aggregate workflow completion is still unverified; no completed current CI is claimed.')
ci_text = (f"Actual C2 artifact data passed, including all 249 members, 52 mathematical commands, 43 paired outputs, three TeX passes, the 195-page PDF, and the fresh 9-command historical rebuild. "
           f"Latest actual metadata at {late['observed_at']}: run {late['run_status']}/{late['run_conclusion']}, job {late['job_status']}/{late['job_conclusion']}; "
           f"{late['actual_step_count']} actual steps, all successful={late['all_actual_steps_completed_successfully']}. " + completion_text)
status = json.loads((article / 'PUBLICATION_STATUS.json').read_bytes())
status.update({
    'current_remote_publication': 'C1 source and the C2 tested descendant were actually published on all three new refs. This evidence-only descendant appends sealed actual records; Git supplies its own final commit identity.',
    'actual_tested_commit': C2,
    'actual_tested_root_tree': C2_ROOT,
    'actual_tested_article_tree': C2_ARTICLE,
    'current_ci': ci_text,
    'current_ci_artifact_data_verified': True,
    'current_ci_workflow_completion_verified': complete,
    'current_ci_scope': late,
    'current_ci_original_sealed_scope': str(summary_path.relative_to(article)),
    'current_ci_later_scope': str(late_path.relative_to(article)),
    'publication_fact_recorded_at_utc': now,
    'self_identity_scope': 'Actual C1/C2 and time-stamped CI facts only. The identity of the commit containing these records is not predicted within its content. Evidence-only publication is not a new execution of the scientific source.',
    'publication_evidence_directory': prefix + '/',
    'previous_tested_metadata': prefix + '/metadata-at-tested-C2/',
})
save(article / 'PUBLICATION_STATUS.json', status)
save(article / 'PUBLICATION_RECEIPT.json', {
    'status': 'Actual C1/C2 publication and artifact data archived; ' + ('later strict CI completion verified' if complete else 'aggregate CI completion unverified'),
    'recorded_at_utc': now,
    'actual_source_commit': C1,
    'actual_tested_commit': C2,
    'actual_tested_root_tree': C2_ROOT,
    'actual_tested_article_tree': C2_ARTICLE,
    'actual_c2_refs_at_archived_observation': actual_c2['three_refs_as_observed'],
    'actual_ci_latest_observation': late,
    'artifact_data_checks_status': summary['data_checks_status'],
    'artifact': summary['artifact'],
    'original_strict_failure_preserved': summary['strict_full_verifier'],
    'data_only_verification': summary['current_data_only'],
    'mathematical_source_sha256': MATH,
    'frozen_source_manifest_sha256': FROZEN,
    'scope': 'The actual tested head is C2. Later publication only archives evidence and changes these three explicitly mutable metadata files. No future publication SHA is self-predicted. Execution checks do not certify the continuous raw local limit theorem.',
    'evidence_directory': prefix + '/',
    'later_ci_scope': str(late_path.relative_to(article)),
    'full_raw_pointwise_llt_complete': False,
    'four_coordinate_inversion_complete': False,
})

transport = f'''# Actual author-source publication and execution evidence

The complete native revision was published as C1 `{C1}`, parent
`0933e9b44f5b0fd1d1a624d37ffd881d352496f8`. C1 has root
`753cfd8589bc0b7c93942a727ed6925abc214bc2` and article tree
`1c4fe72a8217c590568844d6d69f00e428193049`. C2 `{C2}` is its actual tested
evidence-only descendant, with root `{C2_ROOT}` and article `{C2_ARTICLE}`.
All three new refs were independently read back at both actual commits.

{ci_text}

The original sealed CI packet and the later observation remain distinct in
`{prefix}/actual-c2-ci/` and `{prefix}/{args.supplement}/`.
The original full verifier's actual exit 1 is retained at its unchanged completion
gate. The separate data-only pass, its BOM timestamp correction, and an
independently written 366-check reconstruction are preserved with their actual
commands, output identities and limited scope. No metadata field has been
invented to make a gate pass.

The C1 and C2 full remote-tree audits are in `actual-c1-publication-audit/` and
`actual-c2-publication-audit/` below the publication directory. The exact 957-file
transport snapshot is preserved as eight reconstructible binary parts in
`transport-c1-c2/`, with actual reconstruction and all original request/error
receipts. The initial timed zero-run query, public API observations and the exact
three C2 metadata blobs remain separately preserved. The final-remote verifier
and its immutable inputs are explicitly labelled preparation only; any final
readback occurs after this evidence descendant has a real Git identity.

This descendant changes only `PUBLICATION_STATUS.json`, `PUBLICATION_RECEIPT.json`,
`REMOTE_TRANSPORT_STATUS.md`, and newly appended files below `delivery/publication/`.
The 107 mathematical native/tool inputs, all 1,837 frozen source files, all
previously archived evidence and the dedicated workflow remain byte-identical
to C2. It records no new mathematical revision or new CI execution of its own.
The source and actual tested commit identities above are historical facts;
the commit containing this record is identified by Git rather than a circular
self-predicted SHA.

The original raw pointwise local limit theorem and four-coordinate inversion
remain open in their original physical scope, exactly as stated in the current
proof ledger. Finite checks, successful command execution and publication do not
settle the remaining normalized source, full-cell capacity and spectral inputs.
'''
save(article / 'REMOTE_TRANSPORT_STATUS.md', transport.encode())
overview = f'''# Publication evidence for the marked boundary-source author revision

This is the completed evidence assembly for the actual source C1 `{C1}` and
tested C2 `{C2}`. It does not rename an earlier mathematical iteration or claim
that a future evidence commit was independently tested.

## Current execution status

{ci_text}

The exact job log, ZIP and all original command receipts are in
[the sealed C2 packet](actual-c2-ci/README.md). The later actual observation is
[`LATEST_CI_SCOPE.json`]({args.supplement}/LATEST_CI_SCOPE.json).
The complete local manuscript is 195 pages. The CI manuscript is also 195 pages
with matching native auxiliary bytes; its PDF binary hash is separately recorded
because the two actual PDF files are not byte-identical.

## Evidence map

| Directory | Exact scope |
| --- | --- |
| `actual-c1-publication-audit/` | Actual C1 full article-tree audit and timed full 1,293-old/3-new branch census |
| `actual-c2-publication-audit/` | Actual tested C2 tree; 3,596 file identities, 156 reconstructed subtrees and the permitted 13-path C1-to-C2 delta |
| `actual-c2-ci/` | Original actual metadata, 11,125,810-byte ZIP, exact log, original strict failure, data-only v1/v2 and independent 366-check reconstruction |
| `{args.supplement}/` | One separate later metadata observation and any actual unchanged strict-verifier execution, with its own scope |
| `transport-c1-c2/` | Reconstructible exact 957-file transport snapshot, original requests/results and successful nested-root operations |
| `actual-c1-zero-run/` | Exact timed empty C1 workflow query; no assertion about later runs |
| `public-ci-status-observations/` | Original failed/rate-limited and subsequent successful public readbacks, without replacing their statuses |
| `metadata-at-tested-C2/` | Exact three metadata blobs from the tested C2 source, before this evidence assembly |
| `final-remote-audit-preparation/` | Prepared standalone final verifier and immutable inputs; no fabricated final-audit pass |
| `final-publication-assembly/` | Actual assembler, prior append helpers and exact validation of the C2-to-evidence scope |

All seals enumerate complete file bytes and SHA-256 identities. The source
manifest and native mathematics are unchanged. The complete author response,
proof ledger, history audit and literature audit are at the article root.
Their open interfaces remain controlling; these execution records are auxiliary
evidence rather than continuous dynamical proofs.
'''
save(publication / 'PUBLICATION_EVIDENCE.md', overview.encode())

for row in before:
    if row['path'] not in MUTABLE:
        assert git_blob((article / row['path']).read_bytes()) == row['git_blob'], row['path']
assert sha((article / 'SOURCE_MANIFEST.json').read_bytes()) == FROZEN
assert git_blob(workflow.read_bytes()) == '56e44c7a4e978494c5dba8df023bef5fc8b7cfa4'
prior = {row['path'] for row in before}
new_rows = []
for path in sorted(publication.rglob('*')):
    if path.is_file() and path.relative_to(article).as_posix() not in prior:
        new_rows.append(identity(path))
receipt = {
    'schema': 1, 'status': 'passed', 'recorded_at_utc': now,
    'source_commit': C1, 'tested_commit': C2, 'tested_root': C2_ROOT,
    'tested_article': C2_ARTICLE, 'existing_c2_files_checked': len(before),
    'unchanged_existing_files': len(before) - len(MUTABLE),
    'changed_metadata': [identity(article / name) for name in sorted(MUTABLE)],
    'exact_c2_metadata_preserved': True,
    'frozen_manifest_sha256': FROZEN, 'mathematical_source_sha256': MATH,
    'workflow_byte_identical': True, 'workflow_completion_verified': complete,
    'new_publication_files_before_this_receipt': new_rows,
    'future_commit_identity_claimed': False,
    'continuum_proof_certificate': False,
}
save(assembly / 'ACTUAL_ASSEMBLY_RECEIPT.json', receipt)
print(json.dumps({'status': 'passed', 'checked_c2_files': len(before),
                  'new_files_before_receipt': len(new_rows),
                  'new_bytes_before_receipt': sum(r['bytes'] for r in new_rows),
                  'workflow_completion_verified': complete,
                  'receipt': str(assembly / 'ACTUAL_ASSEMBLY_RECEIPT.json')}, indent=2))
