#!/usr/bin/env python3
"""Reconcile immutable historical source census with the fresh ref snapshot."""
from pathlib import Path
import collections, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / name).read_text())
def identity(name):
    raw = (ROOT / name).read_bytes()
    return {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

old = read('baseline/audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json')
fresh = read('research/refs_snapshot.json')
previous = {x['ref']: x['sha'] for x in old['refs']}
current = {x['ref']: x['sha'] for x in fresh['refs'] if 'a2-dyn' in x['ref'].lower()}
added = {k: v for k, v in current.items() if k not in previous}
removed = {k: v for k, v in previous.items() if k not in current}
changed = {k: {'old': v, 'new': current[k]} for k, v in previous.items()
           if k in current and current[k] != v}
assert len(previous) == 435 and len(current) == 436
assert not removed and not changed
assert added == {'refs/heads/revision/a2-dyn-section-multipliers-exact-inversion-2026-10-23':
                 'd6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28'}

lookup_failures = []
for ref, sha in previous.items():
    c = old['commits'].get(sha)
    if c is None:
        lookup_failures.append([ref, 'commit'])
        continue
    for kind, section, leaf in [('papers_tree','paper_sets','article_trees'),
                                ('reviews_tree','review_sets','report_directory_trees')]:
        tree = c.get(kind)
        if tree is None:
            continue
        entries = old[section].get(tree)
        if entries is None:
            lookup_failures.append([ref, kind, tree])
            continue
        for path, sub in entries.items():
            if sub not in old[leaf]:
                lookup_failures.append([ref, path, sub])
assert not lookup_failures

archive = read('baseline/audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json')
checks = []
for item in archive:
    f = ROOT / 'research/historical-native' / (item['oid'] + '.tex')
    raw = f.read_bytes()
    git = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    sha = hashlib.sha256(raw).hexdigest()
    assert git == item['oid'] and sha == item['sha256'] and len(raw) == item['bytes'], item['oid']
    checks.append({'git_blob': git, 'bytes': len(raw), 'sha256': sha})
assert len(checks) == 660
verified = {x['git_blob'] for x in checks}
mains = []
no_main = []
for tree, article in old['article_trees'].items():
    entry = article['direct_entries'].get('main.tex')
    if entry is None:
        no_main.append({'article_tree': tree, 'first_seen_path': article['first_seen_path']})
    else:
        assert entry['type'] == 'blob' and entry['sha'] in verified
        mains.append({'article_tree': tree, 'main_blob': entry['sha']})
assert len(mains) == 120 and len(no_main) == 2

papers = read('research/LATEST_PAPERS_TREE.json')
article = read('research/latest_article_tree.json')
assert not papers['truncated'] and not article['truncated']
packet = 'A2-DYN-section-multipliers-exact-inversion-author-revision'
direct = {e['path']: e for e in papers['tree']}
assert direct[packet]['sha'] == article['sha'] == '381d0aa576a93d874bf974b0edcf090378aaa41b'
compare = read('research/SOURCE_TO_CARRIER_COMPARE.json')
assert (compare['ahead_by'], compare['behind_by'], compare['total_commits']) == (1, 0, 1)
files = [f.get('filename', f.get('path')) for f in compare['files']]
prefix = 'papers/' + packet + '/'
assert len(files) == 30
assert all(f in (prefix+'PUBLICATION_STATUS.json', prefix+'VALIDATION_REPORT.md') or
           f.startswith(prefix+'evidence/github/') for f in files)

result = {
 'schema': 'a2-dyn-fresh-source-census-reconciliation-v1',
 'snapshot_utc': fresh['captured_at'],
 'scope': 'All A2-DYN refs in fresh 1306-ref snapshot; immutable reconciliation of prior census plus fresh new-head trees and source/carrier compare. Does not claim a second download of all 645 historical tree objects.',
 'input_identities': [identity(x) for x in [
     'baseline/audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json', 'research/refs_snapshot.json',
     'baseline/audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json', 'research/LATEST_PAPERS_TREE.json',
     'research/latest_article_tree.json', 'research/SOURCE_TO_CARRIER_COMPARE.json']],
 'historical_ref_count': len(previous), 'current_ref_count': len(current),
 'current_role_hints': dict(collections.Counter(k.split('/')[2] for k in current)),
 'unchanged_historical_refs': len(previous), 'added_refs': added,
 'removed_refs': removed, 'changed_refs': changed, 'lookup_failures': lookup_failures,
 'historical_native_bodies_freshly_hashed': len(checks),
 'historical_direct_article_trees': len(old['article_trees']),
 'historical_direct_main_blobs_in_verified_archive': mains,
 'historical_packets_without_main': no_main,
 'latest_source': {
   'source_commit': compare['base'], 'source_root_tree': '0a5bc8a95de43e7c4d381684f7ffa70b04cdbb4e',
   'source_article_tree': 'e4ddb6fd11e570dfc7bba9d5fd5a2fed051e78c7',
   'carrier_commit': compare['head'], 'carrier_root_tree': '5ec7da36366d703d9e59a68245e90912639d18a0',
   'carrier_papers_tree': papers['sha'], 'carrier_article_tree': article['sha'],
   'carrier_reviews_tree': 'a32951262deb210cc1028270fd8bf7bf982beffa',
   'packet': 'papers/'+packet, 'native_additions': ['333','334','335'],
   'source_to_carrier_only_evidence_paths': True, 'changed_paths': files,
   'scientific_status': 'Readable native author source; full target raw pointwise LLT remains open. Completeness of the source packet and successful compilation do not certify the unresolved mathematical inputs.'
 },
 'all_refs': [{'ref': k, 'sha': v, 'identity_basis': 'historical immutable commit/tree census' if k in previous else 'fresh direct trees and source-to-carrier compare'} for k,v in sorted(current.items())],
 'native_body_checks': checks
}
(ROOT/'research/CURRENT_SOURCE_CENSUS_DELTA.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['historical_ref_count','current_ref_count','unchanged_historical_refs','historical_native_bodies_freshly_hashed','historical_direct_article_trees','current_role_hints']}))
