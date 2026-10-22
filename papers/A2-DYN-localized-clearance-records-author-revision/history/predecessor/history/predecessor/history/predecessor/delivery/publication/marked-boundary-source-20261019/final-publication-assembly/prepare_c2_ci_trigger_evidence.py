#!/usr/bin/env python3
"""Archive actual C1 facts and prepare an evidence-only ordinary-push CI trigger."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path('/workspace/scratch/b5cc344d4c8e')
REC = ROOT / 'iteration-20261019c-recovery'
ART = ROOT / 'theta-theory/papers/A2-DYN-marked-boundary-source-author-revision'
OUT = ART / 'delivery/publication/marked-boundary-source-20261019/c1-ref-creation'
C1 = '409fc85c84a5f239d071b8452da48cb73694365f'
TREE = '753cfd8589bc0b7c93942a727ed6925abc214bc2'
ARTICLE = '1c4fe72a8217c590568844d6d69f00e428193049'
MANIFEST = '0d4439dc86fab1f1226b41506c67a0069edbe21ea9bfd741a099d725fd94f143'
assert not OUT.exists()
assert hashlib.sha256((ART / 'SOURCE_MANIFEST.json').read_bytes()).hexdigest() == MANIFEST
OUT.mkdir(parents=True)

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())

def archive(source, relative):
    target = OUT / relative
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    target.write_bytes(data)
    return {'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

rows = []
for name in ('PUBLICATION_STATUS.json', 'PUBLICATION_RECEIPT.json', 'REMOTE_TRANSPORT_STATUS.md'):
    rows.append(archive(ART / name, 'prepublication-metadata/' + name))
for name in ('C1_CREATE_COMMIT.json', 'C1_CREATE_BRANCHES.json', 'C1_INITIAL_REMOTE_READBACK.json', 'C1_NESTED_PATH_ROOT_RETRY.json'):
    rows.append(archive(REC / 'current-transport-operations' / name, name))
for name in ('C1_RUNS_20261019T154946Z.json', 'ACTUAL_C1_REFERENCE_IDENTITIES.json'):
    rows.append(archive(REC / 'current-ci/actual-c1-ci' / name, name))

readback = json.loads((OUT / 'C1_INITIAL_REMOTE_READBACK.json').read_bytes())
commit = json.loads(readback[0]['response']['structuredContent']['content'])
assert commit['sha'] == C1 and commit['tree']['sha'] == TREE
assert [r['sha'] for r in commit['parents']] == ['0933e9b44f5b0fd1d1a624d37ffd881d352496f8']
refs = []
for row in readback[2:]:
    actual = json.loads(row['response']['structuredContent']['content'])
    assert actual['object']['sha'] == C1 and actual['object']['type'] == 'commit'
    refs.append({'ref': actual['ref'], 'sha': actual['object']['sha']})
assert len(refs) == 3
runs = json.loads((OUT / 'C1_RUNS_20261019T154946Z.json').read_bytes())
assert runs['response'] == {'total_count': 0, 'workflow_runs': []}

status = json.loads((ART / 'PUBLICATION_STATUS.json').read_bytes())
status.update({
    'current_remote_publication': 'C1 was created and all three new refs read back at the actual C1 commit; this evidence-only descendant is prepared for an ordinary push.',
    'actual_source_commit': C1,
    'actual_source_root_tree': TREE,
    'actual_source_article_tree': ARTICLE,
    'current_ci': 'Actual C1 head query returned zero runs at 2026-10-19T15:49:46.658Z. No completed current CI is claimed. An evidence-only branch update is prepared to trigger the unchanged dedicated workflow.',
    'publication_fact_recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'self_identity_scope': 'These are actual C1 facts, not a prediction of the commit containing this receipt. Later publication evidence will identify any tested descendant and final evidence head.',
    'c1_actual_receipts': 'delivery/publication/marked-boundary-source-20261019/c1-ref-creation/'
})
save(ART / 'PUBLICATION_STATUS.json', status)
save(ART / 'PUBLICATION_RECEIPT.json', {
    'status': 'C1 source and three new refs actually published; current remote CI not yet observed',
    'actual_current_remote_commit_at_observation': C1,
    'actual_root_tree': TREE,
    'actual_article_tree': ARTICLE,
    'actual_ref_readback': refs,
    'actual_ci_observation': {'head_sha': C1, 'observed_at': runs['observed_at'], 'total_count': 0},
    'scope': 'C1 publication facts. This evidence-only descendant does not change the frozen scientific source or workflow. No future commit SHA, CI execution, or theorem completion is asserted.',
    'evidence_directory': 'delivery/publication/marked-boundary-source-20261019/c1-ref-creation/'
})
(ART / 'REMOTE_TRANSPORT_STATUS.md').write_bytes(('''# Actual C1 publication and CI trigger

The complete native author source was published as C1 `409fc85c84a5f239d071b8452da48cb73694365f`, with root tree `753cfd8589bc0b7c93942a727ed6925abc214bc2` and article tree `1c4fe72a8217c590568844d6d69f00e428193049`. The three newly created revision, referee-copy and referee-response refs were read back at this commit. The parent is the preserved complete B author source `0933e9b44f5b0fd1d1a624d37ffd881d352496f8`.

At 2026-10-19T15:49:46.658Z, the actual GitHub Actions query for C1 returned zero workflow runs. This timed observation is preserved verbatim. It does not assert that no later run can appear. This evidence-only descendant records the actual C1 facts and enables an ordinary branch update to trigger the existing dedicated workflow. No CI success is claimed here.

The new evidence is under `delivery/publication/marked-boundary-source-20261019/c1-ref-creation/`. It includes the exact prepublication metadata, actual commit/ref creation and readback, the successful nested-path tree request and response, and the actual empty Actions query. The frozen source manifest and all scientific source and workflow bytes remain unchanged. The commit containing this record is not predicted within its own content.

The original raw pointwise local limit theorem and four-coordinate inversion remain explicitly open in their original physical scope. Finite checks, native compilation and any later CI result do not prove those dynamical conclusions.
''').encode())
save(OUT / 'ARCHIVE_IDENTITIES.json', {'scope': 'Exact existing bytes archived before the evidence-only C2 trigger preparation; no CI result', 'files': rows})
print(json.dumps({'status': 'prepared', 'evidence_directory': str(OUT), 'archived_files': len(rows), 'source_manifest_unchanged': hashlib.sha256((ART / 'SOURCE_MANIFEST.json').read_bytes()).hexdigest() == MANIFEST}, indent=2))
