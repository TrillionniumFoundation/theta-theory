#!/usr/bin/env python3
"""Reconstruct the saved R75 descendant scope and 01:48 UTC ref census."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OLD = 'bc2952aa9a9695fe9985d491a4156b8975024285'
NEW = '2c103f924720435700e947cc8df31b8b648f61e9'
SOURCE = '6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9'
CARRIER = 'd46ba004ff1ac8d44dab04549daff7e3c0e5f205'
A2_REF = 'refs/heads/revision/a2-dyn-physical-roof-variation-2026-10-21'
R75_REF = 'refs/heads/revision/general-theta-r75-nonabelian-stationary-memory-20261021'


def load(name):
    return json.loads((ROOT / name).read_text())


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def commit(sha):
    tool = load(f'COMMIT_{sha}.tool.json')
    require(not tool.get('isError', False), 'Failed commit read.')
    result = json.loads(tool['structuredContent']['content'])
    require(result['sha'] == sha, 'Wrong commit identity.')
    return result


def tree(sha):
    receipt = load(f'TREE_{sha}.json')
    result = receipt['response']
    require(not receipt['recursive'] and not result['truncated'] and result['sha'] == sha,
            'Tree response is not a complete nonrecursive receipt.')
    entries = sorted(result['tree'], key=lambda e: e['path'].encode() + (b'/' if e['type'] == 'tree' else b''))
    raw = b''.join((('40000' if e['type'] == 'tree' else e['mode']).encode() + b' ' + e['path'].encode()
                    + b'\0' + bytes.fromhex(e['sha'])) for e in entries)
    calculated = hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(calculated == sha, 'Git tree identity failed independent serialization.')
    return {e['path']: {key: e[key] for key in ('path', 'mode', 'type', 'sha')} for e in entries}


def delta(before, after, prefix=''):
    return [{'path': prefix + name, 'before': before.get(name), 'after': after.get(name)}
            for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]


def refs(filename):
    pairs = [line.split() for line in (ROOT / filename).read_text().splitlines()]
    rows = {ref: sha for sha, ref in pairs}
    require(len(rows) == len(pairs), 'Duplicate ref.')
    return rows


def ref_delta(before, after):
    return {'added': {r: after[r] for r in sorted(set(after) - set(before))},
            'removed': {r: before[r] for r in sorted(set(before) - set(after))},
            'changed': {r: {'before': before[r], 'after': after[r]}
                        for r in sorted(set(before) & set(after)) if before[r] != after[r]},
            'unchanged': sum(before[r] == after[r] for r in set(before) & set(after))}


def main():
    before, after = commit(OLD), commit(NEW)
    require([p['sha'] for p in after['parents']] == [OLD], 'New R75 head is not the direct expected descendant.')
    r0, r1 = tree(before['tree']['sha']), tree(after['tree']['sha'])
    root_delta = delta(r0, r1)
    require([d['path'] for d in root_delta] == ['papers'], 'Unexpected root scope.')
    p0, p1 = tree(r0['papers']['sha']), tree(r1['papers']['sha'])
    papers_delta = delta(p0, p1, 'papers/')
    general = 'General-Theta-Foundations-I-restart'
    require([d['path'] for d in papers_delta] == ['papers/' + general], 'Unexpected papers scope.')
    g0, g1 = tree(p0[general]['sha']), tree(p1[general]['sha'])
    general_delta = delta(g0, g1, 'papers/' + general + '/')
    added_name = 'r75-nonabelian-stationary-memory-publication'
    require(len(general_delta) == 1 and general_delta[0]['path'] == 'papers/' + general + '/' + added_name
            and general_delta[0]['before'] is None, 'R75 delta is not exactly the new publication directory.')
    source_name = 'r75-nonabelian-stationary-memory'
    require(g0[source_name] == g1[source_name], 'Original R75 source changed.')
    scope = {
        'schema': 'a2-dyn-r75-publication-descendant-scope-v1',
        'before_commit': OLD, 'after_commit': NEW, 'direct_parent': OLD,
        'before_root_tree': before['tree']['sha'], 'after_root_tree': after['tree']['sha'],
        'new_commit_author_date_utc': after['author']['date'],
        'new_commit_committer_date_utc': after['committer']['date'],
        'complete_nonrecursive_trees_reconstructed': 6,
        'new_tree_reads': 3, 'retained_verified_tree_receipts': 3,
        'root_delta': root_delta, 'papers_delta': papers_delta, 'general_theta_delta': general_delta,
        'unchanged_other_root_entries': len(r0) - 1,
        'unchanged_other_papers_siblings': len(p0) - 1,
        'unchanged_existing_general_theta_entries': len(g0),
        'original_r75_source_tree_unchanged': g0[source_name],
        'contemporary_a2_dyn_named_articles_in_these_old_roots': [n for n in p1 if 'a2-dyn' in n.lower()],
        'unchanged_a2_geometry_sibling': p0['A2-sinai-homological-pressure'],
        'a2_dyn_source_review_response_workflow_publication_delta': [],
        'mathematical_or_ci_validation_of_r75_performed': False,
        'repository_index_or_ref_mutations': False,
        'method': 'Compare mode/type/SHA at each ancestor; unchanged tree identities cover all descendants. No recursive root request.'
    }
    save('R75_FOLLOWUP_SCOPE.json', scope)
    snapshots = {name: refs(file) for name, file in [
        ('initial', 'INITIAL_HEADS.tsv'), ('pre_push', 'PRE_PUSH_HEADS.tsv'),
        ('post_source', 'POST_PUBLICATION_HEADS.tsv'), ('final_carrier', 'FINAL_REMOTE_HEADS.tsv')]}
    receipt = load('FINAL_REMOTE_HEADS_RECEIPT.json')
    raw = (ROOT / 'FINAL_REMOTE_HEADS.tsv').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == receipt['sha256'] and receipt['exit_code'] == 0, 'Final census receipt identity failed.')
    final = snapshots['final_carrier']
    require(len(final) == receipt['head_count'] == 1300, 'Final census count differs.')
    deltas = {name: ref_delta(heads, final) for name, heads in snapshots.items() if name != 'final_carrier'}
    actual = deltas['post_source']
    require(actual['changed'] == receipt['changed'] and actual['added'] == receipt['added']
            and actual['removed'] == receipt['removed'], 'Recorded final ref delta does not reproduce.')
    expected_moves = {A2_REF: {'before': SOURCE, 'after': CARRIER}, R75_REF: {'before': OLD, 'after': NEW}}
    require(actual['changed'] == expected_moves and not actual['added'] and not actual['removed'],
            'Final census has another change requiring explicit analysis.')
    a2 = {r: s for r, s in final.items() if 'a2-dyn' in r.lower()}
    a2_initial = {r: s for r, s in snapshots['initial'].items() if 'a2-dyn' in r.lower()}
    a2_post = {r: s for r, s in snapshots['post_source'].items() if 'a2-dyn' in r.lower()}
    reviews = {r: s for r, s in a2_initial.items() if r.startswith('refs/heads/review/')}
    require(all(final.get(r) == s for r, s in reviews.items()), 'A pre-existing review ref changed.')
    require(not deltas['initial']['changed'] and not deltas['initial']['removed'], 'An initial old ref changed.')
    require(set(deltas['initial']['added']) == {A2_REF, R75_REF}, 'Unexpected additions since initial snapshot.')
    a2_record = [{'ref': r, 'sha': s} for r, s in sorted(a2.items())]
    save('FINAL_A2_DYN_HEADS.json', {'count': len(a2_record), 'heads': a2_record})
    census = {
        'schema': 'a2-dyn-final-carrier-ref-reconciliation-v1',
        'snapshot_started_utc': receipt['started_utc'], 'snapshot_finished_utc': receipt['finished_utc'],
        'final_snapshot_sha256': digest, 'snapshot_head_counts': {name: len(heads) for name, heads in snapshots.items()},
        'from_initial': deltas['initial'], 'from_pre_push': deltas['pre_push'], 'from_post_source': actual,
        'a2_dyn_named_refs': len(a2), 'a2_dyn_distinct_head_commits': len(set(a2.values())),
        'a2_dyn_classes': dict(Counter(r.split('/')[2] for r in a2)),
        'a2_dyn_from_initial': ref_delta(a2_initial, a2),
        'a2_dyn_from_post_source': ref_delta(a2_post, a2),
        'all_initial_a2_dyn_refs_unchanged': all(final.get(r) == s for r, s in a2_initial.items()),
        'initial_a2_dyn_refs_preserved': len(a2_initial),
        'review_refs_preserved': len(reviews),
        'own_carrier_head_observed': CARRIER,
        'concurrent_r75_head_observed': NEW,
        'scope_boundary': 'Census is the exact retained 01:48:10 UTC observation, not a claim about later movements. This audit verifies neither the carrier mathematics nor CI; separate author receipts cover those.',
        'repository_index_or_ref_mutations': False
    }
    save('FINAL_CENSUS_RECONCILIATION.json', census)
    report = f"""# R75 publication descendant and final carrier census

## Exact result

The concurrent General-Theta R75 movement is a direct descendant:
`{OLD}` → `{NEW}`.
Its entire change is the addition of
`{general_delta[0]['path']}`,
tree `{general_delta[0]['after']['sha']}`.
There is no A2-DYN source, review, response, workflow or publication change in this delta.

Six complete nonrecursive tree receipts were reconstructed by canonical Git serialization: three retained before-trees and three newly read after-trees. All **{len(r0)-1} other root entries**, all **{len(p0)-1} other papers siblings**, and all **{len(g0)} existing General-Theta children** are unchanged in mode, type and object identity. The original R75 source subtree remains `{g0[source_name]['sha']}`.

The root moves from `{before['tree']['sha']}` to `{after['tree']['sha']}`. The new commit's recorded author and committer time is `{after['committer']['date']}`; this is distinct from the ref-observation time below. Commit-message claims about General-Theta mathematics, compilation or checking are retained only as metadata. This audit does not independently certify them.

## Exact census observation

The complete read-only remote-head snapshot ran from **{receipt['started_utc']}** through **{receipt['finished_utc']}**, exited 0, and contains **{len(final):,} heads**. Its SHA256 is `{digest}`.

Relative to the prior post-source 1,300-head observation, there are **no additions or removals**, **two moved heads**, and **{actual['unchanged']:,} unchanged heads**:

| Ref | Previous head | Observed head |
|---|---|---|
| `{A2_REF}` | `{SOURCE}` | `{CARRIER}` |
| `{R75_REF}` | `{OLD}` | `{NEW}` |

The first is the author's evidence carrier; the second is the concurrent General-Theta publication addition audited above. Therefore a statement that only the A2-DYN branch moved would be false for this snapshot.

Relative to the initial 1,298-head snapshot, all **1,298 initial heads remain unchanged**. Exactly the A2-DYN revision branch and the General-Theta R75 branch were added. Relative to the 1,299-head pre-push snapshot, the A2-DYN branch was added and the R75 branch advanced; all other old heads remain unchanged.

There are **{len(a2)} A2-DYN-named refs** and **{len(set(a2.values()))} distinct head commits**: {census['a2_dyn_classes']['revision']} revision, {census['a2_dyn_classes']['review']} review, {census['a2_dyn_classes']['referee-copy']} referee-copy, {census['a2_dyn_classes']['referee-response']} referee-response and {census['a2_dyn_classes']['research']} research. All **{len(a2_initial)} A2-DYN refs present initially**, including all **{len(reviews)} review refs**, are unchanged. Within A2-DYN, the only movement since source publication is the author's newly created branch advancing from its source commit to the evidence carrier.

## Applicability and retained evidence

The General-Theta roots contain the older `A2-sinai-homological-pressure` sibling, unchanged at tree `{p0['A2-sinai-homological-pressure']['sha']}`. They contain no contemporary A2-DYN-named article directory. The General-Theta source and publication are not an A2-DYN author baseline or controlling referee report.

`R75_FOLLOWUP_SCOPE.json` records the complete ancestor-tree comparison. `FINAL_CENSUS_RECONCILIATION.json` gives exact comparisons to all three earlier snapshots; all four raw head snapshots and their original command receipts are retained. `FINAL_A2_DYN_HEADS.json` lists the current A2-DYN refs. `verify_r75_followup.py` reconstructs the saved evidence without network or repository writes. `RECEIPTS_MANIFEST.json` binds the resulting packet.

This audit is limited to exact source/ref scope at the quoted observation. The newly completed source CI and its artifact are verified separately; no CI outcome is inferred from a branch name or this census. No article, index, commit or remote ref was changed, and no whole-repository recursive tree request was made.
"""
    (ROOT / 'R75_FOLLOWUP.md').write_text(report)
    output = {'status': 'verified', 'completed_utc': datetime.now(timezone.utc).isoformat(),
              'six_tree_hashes_reconstructed': True, 'direct_descendant': True,
              'only_added_subtree': general_delta[0]['path'], 'a2_dyn_delta': [],
              'remote_heads': len(final), 'changed_since_post_source': actual['changed'],
              'unchanged_since_post_source': actual['unchanged'],
              'a2_dyn_refs': len(a2), 'initial_a2_dyn_refs_unchanged': len(a2_initial),
              'review_refs_unchanged': len(reviews)}
    save('RECONSTRUCTION_RESULT.json', output)
    rows = []
    for path in sorted(ROOT.iterdir()):
        if path.is_file() and path.name != 'RECEIPTS_MANIFEST.json':
            data = path.read_bytes()
            rows.append({'path': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    save('RECEIPTS_MANIFEST.json', {'schema': 'a2-dyn-r75-followup-receipt-manifest-v1',
                                  'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows), 'files': rows})
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()

