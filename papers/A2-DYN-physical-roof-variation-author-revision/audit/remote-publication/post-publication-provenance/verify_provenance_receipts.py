#!/usr/bin/env python3
"""Reconstruct the R75 scope and post-publication head census from saved reads."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from collections import Counter

ROOT = Path(__file__).resolve().parent
R74 = 'c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0'
R75 = 'bc2952aa9a9695fe9985d491a4156b8975024285'
SOURCE = '6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9'


def load(path):
    return json.loads(path.read_text())


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def commit(sha):
    tool = load(ROOT / f'COMMIT_{sha}.tool.json')
    if tool.get('isError', False):
        raise RuntimeError('Saved commit retrieval failed.')
    result = json.loads(tool['structuredContent']['content'])
    if result['sha'] != sha:
        raise RuntimeError('Commit receipt identity mismatch.')
    return result


def tree(sha):
    receipt = load(ROOT / f'TREE_{sha}.json')
    result = receipt['response']
    if receipt['recursive'] or result['truncated'] or result['sha'] != sha:
        raise RuntimeError('Tree read is not a complete nonrecursive receipt.')
    entries = sorted(result['tree'], key=lambda e: e['path'].encode() + (b'/' if e['type'] == 'tree' else b''))
    raw = b''.join((('40000' if e['type'] == 'tree' else e['mode']).encode() + b' ' + e['path'].encode()
                    + b'\0' + bytes.fromhex(e['sha'])) for e in entries)
    calculated = hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if calculated != sha:
        raise RuntimeError('Git tree serialization identity mismatch.')
    return {entry['path']: {key: entry[key] for key in ('path', 'mode', 'type', 'sha')} for entry in entries}


def differences(before, after, prefix):
    return [{'path': prefix + name, 'before': before.get(name), 'after': after.get(name)}
            for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]


def main():
    old, new = commit(R74), commit(R75)
    chain = []
    sha = R75
    while sha != R74:
        item = commit(sha)
        if len(item['parents']) != 1 or len(chain) >= 16:
            raise RuntimeError('Unexpected ancestry shape.')
        chain.append({'sha': item['sha'], 'tree': item['tree']['sha'], 'parent': item['parents'][0]['sha'],
                      'committer_date_utc': item['committer']['date'], 'title': item['message'].split('\n')[0]})
        sha = item['parents'][0]['sha']
    root_before, root_after = tree(old['tree']['sha']), tree(new['tree']['sha'])
    root_delta = differences(root_before, root_after, '')
    if [r['path'] for r in root_delta] != ['papers']:
        raise RuntimeError('R75 modifies another root path.')
    papers_before, papers_after = tree(root_before['papers']['sha']), tree(root_after['papers']['sha'])
    papers_delta = differences(papers_before, papers_after, 'papers/')
    only = 'General-Theta-Foundations-I-restart'
    if [r['path'] for r in papers_delta] != ['papers/' + only]:
        raise RuntimeError('R75 modifies another paper subtree.')
    general_before, general_after = tree(papers_before[only]['sha']), tree(papers_after[only]['sha'])
    general_delta = differences(general_before, general_after, 'papers/' + only + '/')
    new_name = 'r75-nonabelian-stationary-memory'
    if len(general_delta) != 1 or general_delta[0]['path'] != 'papers/' + only + '/' + new_name or general_delta[0]['before'] is not None:
        raise RuntimeError('R75 final delta is not solely the expected added subtree.')
    census = load(ROOT / 'REMOTE_REF_DELTA.json')
    heads_receipt = load(ROOT / 'POST_PUBLICATION_HEADS_RECEIPT.json')
    raw_heads = (ROOT / 'POST_PUBLICATION_HEADS.tsv').read_bytes()
    if hashlib.sha256(raw_heads).hexdigest() != heads_receipt['stdout_sha256']:
        raise RuntimeError('Post-publication full head receipt hash mismatch.')
    snapshots = {}
    for label, filename in (('initial', 'INITIAL_HEADS.tsv'), ('pre', 'PRE_PUSH_HEADS.tsv'), ('post', 'POST_PUBLICATION_HEADS.tsv')):
        pairs = [line.split() for line in (ROOT / filename).read_text().splitlines()]
        refs = {ref: sha for sha, ref in pairs}
        if len(refs) != len(pairs):
            raise RuntimeError('Duplicate remote ref in a full snapshot.')
        snapshots[label] = refs
    def ref_delta(left, right):
        return {'added': {r: right[r] for r in sorted(set(right) - set(left))},
                'removed': {r: left[r] for r in sorted(set(left) - set(right))},
                'changed': {r: {'before': left[r], 'after': right[r]} for r in sorted(set(left) & set(right)) if left[r] != right[r]}}
    if ref_delta(snapshots['pre'], snapshots['post']) != census['from_pre_push'] or ref_delta(snapshots['initial'], snapshots['post']) != census['from_initial']:
        raise RuntimeError('Stored remote delta does not reproduce from all three raw snapshots.')
    a2_refs = {ref: sha for ref, sha in snapshots['post'].items() if 'a2-dyn' in ref.lower()}
    if (len(a2_refs) != census['a2_dyn_named_heads'] or len(set(a2_refs.values())) != census['a2_dyn_unique_head_commits']
            or dict(Counter(ref.split('/')[2] for ref in a2_refs)) != census['a2_dyn_classes']):
        raise RuntimeError('A2-DYN census does not reproduce from the raw snapshot.')
    if census['from_pre_push']['added'] != {'refs/heads/revision/a2-dyn-physical-roof-variation-2026-10-21': SOURCE}:
        raise RuntimeError('Unexpected post-publication ref addition.')
    if any(census['from_pre_push'][k] for k in ('changed', 'removed')):
        raise RuntimeError('An old remote head moved or disappeared; update report explicitly.')
    scope = {
        'schema': 'a2-dyn-concurrent-r75-exact-tree-scope-v1',
        'r74_commit': R74, 'r74_root_tree': old['tree']['sha'],
        'r75_commit': R75, 'r75_root_tree': new['tree']['sha'],
        'first_parent_commits_after_r74': list(reversed(chain)),
        'new_commit_count': len(chain), 'nonrecursive_tree_reads': 6,
        'complete_tree_hashes_reconstructed_and_verified': True,
        'root_delta': root_delta, 'papers_delta': papers_delta, 'general_theta_delta': general_delta,
        'unchanged_other_root_entries': len(root_before) - 1,
        'unchanged_other_papers_siblings': len(papers_before) - 1,
        'unchanged_existing_general_theta_entries': len(general_before),
        'a2_dyn_source_review_workflow_changes': False,
        'a2_dyn_named_paper_entries_in_these_old_general_theta_roots': [n for n in papers_before if 'a2-dyn' in n.lower()],
        'a2_geometry_sibling': papers_before['A2-sinai-homological-pressure'],
        'applicability': 'The R75 addition belongs only to General Theta. Its roots do not contain the contemporary A2-DYN article directory; it is neither an A2-DYN author baseline nor an A2-DYN referee report.',
        'mathematical_or_ci_validation_of_r75_performed': False,
        'repository_or_remote_mutations_by_this_audit': False,
    }
    save('R75_SCOPE.json', scope)
    summary = {'schema': 'a2-dyn-post-source-publication-provenance-v1',
               'source_commit': SOURCE, 'source_branch': 'revision/a2-dyn-physical-roof-variation-2026-10-21',
               'source_article_tree_as_published_by_author': '4f41b3a98487a1ae0507d40390aca030c5520e19',
               'snapshot_started_utc': heads_receipt['started_utc'], 'snapshot_completed_utc': heads_receipt['completed_utc'],
               'post_publication_heads_sha256': heads_receipt['stdout_sha256'], **census,
               'all_1299_pre_push_heads_unchanged': True, 'all_433_preexisting_a2_dyn_heads_unchanged': True,
               'all_178_review_heads_unchanged': True, 'r75_scope_file': 'R75_SCOPE.json',
               'r75_only_added_path': general_delta[0]['path'], 'r75_added_subtree': general_delta[0]['after']['sha'],
               'no_recursive_repository_tree_query': True, 'repository_or_remote_mutations_by_this_audit': False,
               'ci_scope': 'CI status and artifacts are handled by the author and CI-readback agents; this provenance audit makes no new CI completion claim.'}
    save('POST_PUBLICATION_PROVENANCE.json', summary)
    report = f'''# Post-publication provenance and concurrent General Theta R75 scope

## Result

The fresh remote snapshot taken from **{heads_receipt['started_utc']} to {heads_receipt['completed_utc']}** contains **1,300 branch heads**. Relative to the 1,299-head pre-push snapshot, its only addition is `revision/a2-dyn-physical-roof-variation-2026-10-21` at `{SOURCE}`. No pre-push head moved or disappeared. The full raw head receipt has SHA256 `{heads_receipt['stdout_sha256']}`.

Relative to the initial 1,298-head snapshot, exactly two branches were added: the concurrent General Theta R75 branch at `{R75}` and this A2-DYN source branch. All 1,298 initial heads are unchanged. The intermediate General Theta addition was already present in the pre-push snapshot and was not created by this A2-DYN publication.

## A2-DYN scope

There are **434 A2-DYN-named refs and 218 distinct head commits**: 247 revision refs, 178 review refs, four referee-copy refs, four referee-response refs and one research ref. All 433 pre-existing A2-DYN heads, including all 178 review heads, are unchanged. The only new A2-DYN ref points to the published source commit above. No newer controlling A2-DYN report is introduced by the concurrent R75 branch.

## Exact General Theta R75 delta

The verified first-parent chain is:

`{R74}` → `a05bed516b86ea1273ff542e1b2988cd326da214` → `c09682b410148263268a4e7ca3e9a6fed54ed9b9` → `20a3e069a9d7c2dfc0c09852c835ed1863748600` → `{R75}`.

The R74 root is `{old['tree']['sha']}`; the R75 root is `{new['tree']['sha']}`. Six complete, nonrecursive tree reads, independently rehashed from their Git entries, establish the entire final delta:

**Added:** `{general_delta[0]['path']}`, tree `{general_delta[0]['after']['sha']}`.

All **139 other root entries**, all **55 other `papers/` siblings**, and all **29 pre-existing General Theta child entries** have identical mode, type and object SHA. In particular, the `reviews/`, `revision/`, `.github/`, archive and other paper subtrees are unchanged. There is no A2-DYN source, referee, response, CI or publication modification in this R74-to-R75 delta.

The General Theta roots retain the older `A2-sinai-homological-pressure` sibling at tree `{papers_before['A2-sinai-homological-pressure']['sha']}`. They contain no contemporary A2-DYN article directory. They therefore cannot be substituted for the actual A2-DYN author baseline, and their mathematical or review status is not imported into A2-DYN.

This audit establishes tree scope and ref preservation. It does not certify the General Theta mathematics, builds or CI. The commit messages are retained as metadata, not adopted as proof.

## Receipts and method

`POST_PUBLICATION_HEADS.tsv` is the complete 1,300-ref snapshot; `POST_PUBLICATION_HEADS_RECEIPT.json` records its actual command, start/end times, exit code and SHA256. The exact initial and pre-push raw snapshots and their receipts are retained alongside it as `INITIAL_HEADS.*` and `PRE_PUSH_HEADS.*`. `REMOTE_REF_DELTA.json` compares both earlier snapshots. `POST_PUBLICATION_A2_DYN_HEADS.json` records all 434 A2-DYN refs. `R75_SCOPE.json` records the exact ancestry and three-level tree comparison; `TREE_*.json` retains all six untruncated responses. `COMMIT_*.tool.json` retains the five GitHub commit read responses.

The local missing-object read failed because the sandbox proxy connection was unavailable. The successful GitHub-plugin reads replaced that read attempt; `LOCAL_READ_ATTEMPT.json` retains the distinction. The fresh head census used read-only public `git ls-remote --heads`. No ref, index, commit, manuscript or repository file was changed by this audit, and no whole-repository recursive query was made.

`verify_provenance_receipts.py` reconstructs the saved ancestry, all six tree hashes, the scope comparison and head receipt identity. CI is audited separately; this report makes no claim that the newly queued run has completed.
'''
    (ROOT / 'POST_PUBLICATION_PROVENANCE.md').write_text(report)
    manifest = []
    for path in sorted(ROOT.iterdir()):
        if path.is_file() and path.name != 'RECEIPTS_MANIFEST.json':
            data = path.read_bytes()
            manifest.append({'path': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    save('RECEIPTS_MANIFEST.json', {'schema': 'a2-dyn-post-publication-receipt-manifest-v1', 'files': manifest,
                                   'file_count': len(manifest), 'bytes': sum(r['bytes'] for r in manifest)})
    print(json.dumps({'post_heads': census['post_publication_heads'], 'a2_dyn_heads': census['a2_dyn_named_heads'],
                      'only_added_since_pre_push': census['from_pre_push']['added'], 'old_heads_changed': 0,
                      'r75_only_added_path': general_delta[0]['path'], 'six_tree_hashes_verified': True,
                      'receipt_files': len(manifest), 'receipt_bytes': sum(r['bytes'] for r in manifest)}, indent=2))


if __name__ == '__main__':
    main()
