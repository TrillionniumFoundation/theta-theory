#!/usr/bin/env python3
"""Revalidate actual recovery observations and immutable retained B evidence.

This program performs no network request, changes no article, and runs no CI.
Fresh GitHub observations and retained historical observations remain distinct.
"""
from __future__ import annotations
import argparse
import collections
import datetime
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

REPO = 'TrillionniumFoundation/theta-theory'
BASE = '0933e9b44f5b0fd1d1a624d37ffd881d352496f8'
ROOT = 'dba7d9a6e14d2509291f03cbf269b4ceb78b9549'
ARTICLE = 'ff4daf7f42d868bd9b41b0b9fe4033489f99bd21'
TESTED = '228ec6a639d4d195a1a8b869a04dae6f49fece0e'
CONTROL = 'f01482035a0b945b50f1f9c30f30ef35077558dc'
REVIEWED = '31792379408c5ace2c09284c2eb22d2331023433'
V73 = '5e9877a6677300615f909b47661775451f543817'
V73_BLOB = 'c06ffcf46059987264935f497d8b4e2564571936'
PREFIX = 'https://api.github.com/repos/' + REPO


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def tree(rows):
    names = [x['path'] for x in rows]
    need(len(names) == len(set(names)), 'duplicate Git tree entries')
    need(all('/' not in n and '\0' not in n for n in names), 'nonlocal tree entry')
    ordered = sorted(rows, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    body = b''.join(x['mode'].lstrip('0').encode() + b' ' + x['path'].encode() + b'\0' + bytes.fromhex(x['sha']) for x in ordered)
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def identity(path, relative=None):
    data = path.read_bytes()
    return {'path': str(relative if relative is not None else path), 'bytes': len(data),
            'sha256': sha(data), 'git_blob': blob(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', required=True, type=Path)
    parser.add_argument('--audit', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    b, a = args.baseline.resolve(), args.audit.resolve()
    need(b.name == 'A2-DYN-full-physical-source-author-revision', 'wrong baseline article')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    outputs = {}

    def emit(name, value):
        (a / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        outputs[name] = identity(a / name, name)

    def fresh(key):
        rec = load(a / 'readbacks' / (key + '.json'))
        need(rec['tool'] == 'mcp__codex_apps__github_fetch' and rec['isError'] is False, 'unsuccessful actual observation: ' + key)
        if 'response' in rec:
            need(json.loads(rec['response_text']) == rec['response'], 'raw/parsed response disagreement: ' + key)
        need(rec['requested_at'] <= rec['observed_at'], 'observation time ordering: ' + key)
        need(rec['url'].startswith(PREFIX + '/'), 'wrong repository observation: ' + key)
        return rec

    census = load(a / 'ALL_BRANCHES_READBACK.json')
    collected = []
    page_identities = []
    for page_number, entry in enumerate(census['pages'], 1):
        need(entry['page'] == page_number, 'nonconsecutive branch pages')
        rec = fresh('branches_' + str(page_number))
        rows = rec['response']
        need(rec['page'] == page_number and rec['url'] == PREFIX + '/branches?per_page=100&page=' + str(page_number), 'wrong branch URL')
        need(isinstance(rows, list) and len(rows) == entry['records'] <= 100, 'invalid page length')
        need(census['observed_started_utc'] <= rec['requested_at'] <= rec['observed_at'] <= census['observed_finished_utc'], 'unbounded page timestamp')
        if page_number < len(census['pages']) - 1:
            need(len(rows) == 100, 'page skipped after short page')
        collected.extend(rows)
        page_identities.append(identity(a / entry['receipt'], entry['receipt']))
    need(census['pages'][-1]['records'] == 0 and collected == census['branches'], 'missing explicit empty page or different concatenation')
    current = {x['name']: x['commit']['sha'] for x in collected}
    need(len(current) == census['count'] == len(collected), 'duplicate or missing refs')
    historical_census_path = b / 'audit/full-physical-source-20261019/source-census/ALL_BRANCHES_READBACK.json'
    old = {x['name']: x['commit']['sha'] for x in load(historical_census_path)['branches']}
    added = sorted(current.keys() - old.keys())
    removed = sorted(old.keys() - current.keys())
    moved = sorted(x for x in current.keys() & old.keys() if current[x] != old[x])
    expected_added = sorted(p + '/a2-dyn-full-physical-source-2026-10-19' for p in ('revision', 'referee-copy', 'referee-response'))
    need(added == expected_added and not removed and not moved, 'unexpected ref delta: inspect before choosing baseline')
    need(all(current[x] == BASE for x in added), 'published B aliases do not resolve to baseline')
    dyn = {k: v for k, v in current.items() if re.search(r'a2-?dyn', k, re.I)}
    review = {k: v for k, v in dyn.items() if k.startswith('review/')}
    author = {k: v for k, v in dyn.items() if not k.startswith('review/')}
    need((len(current), len(dyn), len(author), len(review), len(set(author.values()))) == (1293, 429, 251, 178, 130), 'fresh census class count differs')
    need(not any('marked-boundary-source-2026-10-19' in k for k in current), 'current C refs now exist: update publication scope')
    emit('BRANCH_DELTA_FROM_PUBLISHED_B_CENSUS.json', {
        'old_census': identity(historical_census_path), 'current_census': identity(a / 'ALL_BRANCHES_READBACK.json'),
        'old_count': len(old), 'current_count': len(current), 'added': [{'name': x, 'sha': current[x]} for x in added],
        'removed': removed, 'moved': moved, 'all_old_refs_unchanged': True, 'a2_dyn_refs': len(dyn),
        'author_research_copy_response_refs': len(author), 'distinct_author_heads': len(set(author.values())),
        'review_refs': len(review), 'distinct_review_heads': len(set(review.values())),
        'prefix_counts': dict(sorted(collections.Counter(k.split('/')[0] for k in dyn).items())),
        'pre_loss_1037_summary_counts_reproduced': True,
        'pre_loss_1037_raw_receipt_recovered_or_claimed_identical': False,
        'fresh_page_identities': page_identities, 'new_C_publication_refs_present': False,
    })

    commit = fresh('baseline_commit')['response']
    parent = fresh('tested_parent_commit')['response']
    need(commit['sha'] == BASE and commit['tree']['sha'] == ROOT, 'baseline commit/root mismatch')
    need([x['sha'] for x in commit['parents']] == [TESTED] and parent['sha'] == TESTED, 'wrong tested parent')
    need([x['sha'] for x in parent['parents']] == ['694952d7d6b886d0087e8560da721bfc980adbc3'], 'wrong complete-source ancestor')

    trees = {}
    tree_checks = []

    def add_tree(data, expected, origin):
        need(data.get('truncated') is False, 'truncated/unspecified tree: ' + origin)
        actual = tree(data['tree'])
        need(actual == expected, 'canonical tree mismatch: ' + origin)
        if actual in trees:
            signature = lambda rows: sorted((x['path'], x['mode'], x['type'], x['sha']) for x in rows)
            need(signature(trees[actual]['tree']) == signature(data['tree']), 'same SHA, different rows')
        trees[actual] = data
        tree_checks.append({'origin': origin, 'sha': expected, 'entries': len(data['tree']), 'verified': True})

    inherited_root = b / 'audit/current-iteration/source-census'
    files = ['ALL_AUTHOR_ROOT_TREE_READBACKS.json', 'ALL_AUTHOR_PAPERS_TREE_READBACKS.json',
             'ALL_AUTHOR_ARTICLE_TREE_READBACKS.json', 'ALL_AUTHOR_CORE_TREE_READBACKS.json',
             'BASELINE_ARTICLE_NONRECURSIVE_TREES.json', 'SUMMABLE_PREDECESSOR_COMPLETE_TREE_READBACK.json']
    inherited_inputs = []
    for name in files:
        path = inherited_root / name
        inherited_inputs.append(identity(path))
        for row in load(path)['trees']:
            add_tree(row['response'], row.get('canonical_tree_sha', row['requested_sha']), 'retained B: ' + name)
    b_fixed = b / 'audit/full-physical-source-20261019/source-census/readbacks/fixed'
    for path in sorted(b_fixed.glob('*.json')):
        d = load(path)['response']
        if isinstance(d, dict) and isinstance(d.get('tree'), list):
            add_tree(d, d['sha'], 'retained B: ' + str(path.relative_to(b)))
    for key in ['baseline_root', 'baseline_papers', 'baseline_github', 'baseline_workflows', 'baseline_article', 'baseline_core',
                'v73_review_root', 'v73_reviews_tree', 'v73_report_directory']:
        d = fresh(key)['response']
        add_tree(d, d['sha'], 'fresh readbacks/' + key + '.json')

    old_commits = load(inherited_root / 'ALL_AUTHOR_COMMIT_READBACKS.json')['commits']
    commits = {x['response']['sha']: x['response'] for x in old_commits}
    for key in ['global_minimizer_commit', 'physical_tube_commit', 'baseline_commit']:
        d = fresh(key)['response']
        if d['sha'] in commits:
            need(d['tree'] == commits[d['sha']]['tree'], 'fresh commit tree differs from retained commit')
        commits[d['sha']] = d
    need(set(commits) == set(author.values()), 'historical plus fresh author commit coverage mismatch')
    roots, papers, articles, cores = set(), set(), set(), set()
    occurrences = collections.defaultdict(list)
    def named(data, name):
        rows = [x for x in data['tree'] if x['path'] == name]
        need(len(rows) == 1, 'missing or duplicate tree entry: ' + name)
        return rows[0]
    for c, d in sorted(commits.items()):
        root_sha = d['tree']['sha']; roots.add(root_sha)
        need(root_sha in trees, 'missing retained author root: ' + root_sha)
        p = named(trees[root_sha], 'papers')['sha']; papers.add(p)
        need(p in trees, 'missing author papers tree: ' + p)
        for entry in trees[p]['tree']:
            if entry['type'] == 'tree' and entry['path'].startswith('A2-DYN'):
                art = entry['sha']; articles.add(art)
                need(art in trees, 'missing article tree: ' + art)
                occurrences[art].append({'commit': c, 'root_tree': root_sha, 'papers_tree': p,
                                         'path': 'papers/' + entry['path'],
                                         'refs': sorted(k for k, v in author.items() if v == c)})
                for ce in trees[art]['tree']:
                    if ce['path'] == 'core' and ce['type'] == 'tree':
                        cores.add(ce['sha'])
                        need(ce['sha'] in trees, 'missing native core tree: ' + ce['sha'])
    numbered = {}
    for c in sorted(cores):
        for x in trees[c]['tree']:
            if x['type'] == 'blob' and re.match(r'^\d+.*\.tex$', x['path']):
                numbered.setdefault(x['sha'], {'sha': x['sha'], 'path': x['path'], 'bytes': x.get('size'), 'core_witnesses': []})['core_witnesses'].append(c)
    emit('SOURCE_GRAPH_REVALIDATION.json', {
        'scope': 'Fresh ref identities plus independently recomputed canonical hashes of retained immutable B trees and fresh baseline trees; historical HTTP observations are not relabelled as newly fetched.',
        'current_author_refs': len(author), 'distinct_author_commits': len(commits), 'distinct_roots': len(roots),
        'distinct_papers_trees': len(papers), 'distinct_article_trees': len(articles), 'distinct_core_trees': len(cores),
        'numbered_native_blob_union': len(numbered), 'canonical_tree_checks': len(tree_checks),
        'tree_checks': tree_checks, 'inherited_inputs': inherited_inputs,
        'commits': [{'commit': c, 'root_tree': d['tree']['sha'], 'committer_utc': d['committer']['date'],
                     'refs': sorted(k for k, v in author.items() if v == c)} for c, d in sorted(commits.items())],
        'articles': [{'tree': c, 'main_tex_present': any(x['path'] == 'main.tex' for x in trees[c]['tree']),
                      'core_trees': [x['sha'] for x in trees[c]['tree'] if x['path'] == 'core' and x['type'] == 'tree'],
                      'occurrences': occurrences[c]} for c in sorted(articles)],
        'numbered_variants': list(numbered.values()), 'source_presence_does_not_establish_build_or_theorem_completion': True,
    })

    recursive = fresh('baseline_article_recursive')['response']
    need(recursive['sha'] == ARTICLE and recursive.get('truncated') is False, 'bad complete article tree')
    groups = collections.defaultdict(list)
    expected_subtrees = {'': ARTICLE}
    rows = []
    for item in recursive['tree']:
        p = PurePosixPath(item['path']); parent_path = '' if str(p.parent) == '.' else str(p.parent)
        groups[parent_path].append(dict(item, path=p.name))
        if item['type'] == 'tree': expected_subtrees[item['path']] = item['sha']
        elif item['type'] == 'blob':
            path = b / item['path']; need(path.is_file() and not path.is_symlink(), 'missing baseline file: ' + item['path'])
            data = path.read_bytes(); mode = '100755' if path.stat().st_mode & 0o111 else '100644'
            need(len(data) == item['size'] and blob(data) == item['sha'] and mode == item['mode'], 'baseline bytes or mode differ: ' + item['path'])
            rows.append({'path': item['path'], 'bytes': len(data), 'sha256': sha(data), 'sha': item['sha'], 'mode': mode, 'type': 'blob'})
        else: raise RuntimeError('unexpected non-blob article leaf')
    for p, h in expected_subtrees.items(): need(tree(groups[p]) == h, 'recursive subtree mismatch: ' + p)
    local_files = {str(x.relative_to(b)) for x in b.rglob('*') if x.is_file()}
    need(local_files == {x['path'] for x in rows}, 'baseline contains extra local files')
    need((len(rows), sum(x['bytes'] for x in rows)) == (2765, 318080854), 'wrong actual B full-source size')
    emit('BASELINE_FILE_IDENTITIES.json', {'commit': BASE, 'root_tree': ROOT, 'article_tree': ARTICLE,
                                          'file_count': len(rows), 'bytes': sum(x['bytes'] for x in rows),
                                          'canonical_subtrees': len(expected_subtrees), 'all_match': True, 'files': sorted(rows, key=lambda x: x['path'])})

    reports = load(b / 'audit/reports_index.json')
    report_checks = []
    for item in reports:
        path = b / item['artifact_relative_report_path']; d = path.read_bytes()
        need((len(d), sha(d), blob(d)) == (item['bytes'], item['sha256'], item['blob_sha']), 'historical report changed: ' + str(path))
        need(current[item['branch']] == item['review_commit_sha'], 'historical review ref moved')
        report_checks.append(dict(item, actual_bytes_verified=True))
    need(len(report_checks) == 90, 'wrong original report count')
    canonical_commits = {x['review_commit_sha'] for x in reports}
    uncatalogued = {k: v for k, v in review.items() if v not in canonical_commits}
    need(uncatalogued == {'review/a2-dyn-v73-external-top4-review-copy-2026-10-11': V73}, 'new unscoped report')
    v73 = (a / 'HISTORICAL_V73_ORIGINAL_REFEREE_COPY_REPORT.md').read_bytes()
    need((len(v73), sha(v73), blob(v73)) == (35703, '9cc4deedfec565ae19c7bcd2030b54226c4913053e3f64fc58b2367ae6de7f38', V73_BLOB), 'recovered report byte identity mismatch')
    need(named(fresh('v73_report_directory')['response'], 'REFEREE_REPORT.md')['sha'] == V73_BLOB, 'v73 path/blob mismatch')
    v73commit = fresh('v73_original_commit')['response']
    need(v73commit['sha'] == V73 and v73commit['tree']['sha'] == fresh('v73_review_root')['response']['sha'], 'v73 commit/root mismatch')
    ct = fresh('controlling_commit')['response']; cb = (a / 'CONTROLLING_REFEREE_REPORT.md').read_bytes()
    cr = next(x for x in reports if x['review_commit_sha'] == CONTROL)
    need(ct['sha'] == CONTROL and [x['sha'] for x in ct['parents']] == [REVIEWED], 'controlling report has wrong reviewed parent')
    need((len(cb), sha(cb), blob(cb)) == (cr['bytes'], cr['sha256'], cr['blob_sha']), 'controller source identity mismatch')
    need(fresh('controlling_report_directory')['response'][0]['sha'] == blob(cb), 'controller path/blob mismatch')
    need(max(reports, key=lambda x: x['review_commit_utc'])['review_commit_sha'] == CONTROL, 'a later original report needs scope review')
    emit('REFEREE_SCOPE_AND_91ST_REPORT.json', {
        'scope': 'Author-side provenance and applicability revalidation; no new referee review or endorsement.',
        'current_review_ref_count': len(review), 'distinct_report_commit_count': len(set(review.values())),
        'original_90_reports_preserved_and_byte_verified': report_checks,
        'additional_distinct_historical_report': {'commit': V73, 'tree': v73commit['tree']['sha'],
            'path': 'reviews/a2-dyn-v73-external-top4-review-2026-10-11/REFEREE_REPORT.md',
            **identity(a / 'HISTORICAL_V73_ORIGINAL_REFEREE_COPY_REPORT.md'), 'reviewed_author_commit': '39575228f055862103edbebdd984bd6764fa0ad9',
            'reviewed_root': '73fba91196dffb2714685a55706545124aea3ba0', 'substantive_modules': [160, 161, 162, 163],
            'already_credited': 'fixed-count full-source BV and scalar/path endpoint equality',
            'still_applicable_request': 'collision-uniform paired signed flux and original ordered pointwise endpoint; fixed-count BV does not close it'},
        'controlling_report': {'commit': CONTROL, 'tree': ct['tree']['sha'], 'report_path': cr['report_path'],
            'blob': blob(cb), 'sha256': sha(cb), 'bytes': len(cb), 'reviewed_author_commit': REVIEWED,
            'reviewed_root': '008dba443ce2ca29b3e276b1bf05bcf7021011c1', 'active_native_scope': '260--276',
            'substantive_increment_reviewed': '270--276', 'later_277_318_reviewed_by_this_report': False,
            'status': 'author-requested AI-assisted assessment, not independent human journal review'},
        'new_report_since_published_B_census': False, 'A2_geometry_favorable_review_used': False,
        'original_historical_obstruction_navigation': identity(b / 'audit/review_status_matrix.json'),
    })

    run = fresh('prior_ci_run')['response']; jobs = fresh('prior_ci_jobs')['response']; artifacts = fresh('prior_ci_artifacts')['response']
    need((run['id'], run['head_sha'], run['status'], run['conclusion'], run['event'], run['path']) ==
         (39229329979, TESTED, 'completed', 'success', 'push', '.github/workflows/a2-dyn-full-physical-source-20261019.yml'), 'wrong successful CI identity')
    need(jobs['total_count'] == len(jobs['jobs']) == 1 and artifacts['total_count'] == len(artifacts['artifacts']) == 1, 'incomplete CI collections')
    job = jobs['jobs'][0]; artifact = artifacts['artifacts'][0]
    need((job['id'], job['head_sha'], job['status'], job['conclusion']) == (117983194322, TESTED, 'completed', 'success'), 'job identity/state mismatch')
    need(all(s['status'] == 'completed' and s['conclusion'] == 'success' for s in job['steps']), 'unsuccessful actual step')
    ci = b / 'delivery/publication/full-physical-source-20261019/actual-C2-ci'
    original = load(ci / 'CURRENT_CI_ARTIFACT_VERIFICATION.json')
    archive = ci / 'CI_ARTIFACT_12176597487.zip'; archive_data = archive.read_bytes()
    need(artifact['id'] == 12176597487 and not artifact['expired'], 'prior artifact unavailable/changed')
    need((artifact['size_in_bytes'], artifact['digest']) == (len(archive_data), 'sha256:' + sha(archive_data)), 'advertised artifact digest differs from retained bytes')
    need((len(archive_data), sha(archive_data)) == (original['artifact_bytes'], original['artifact_sha256']), 'retained archive differs from prior verification')
    member_index = load(ci / 'CURRENT_CI_ARTIFACT_FILE_MANIFEST.json')
    expected_members = {x['path']: x for x in member_index['files']}; actual_members = []
    with zipfile.ZipFile(archive) as z:
        need(z.testzip() is None, 'bad ZIP CRC')
        names = [x.filename for x in z.infolist() if not x.is_dir()]
        need(len(names) == len(set(names)) and set(names) == set(expected_members), 'ZIP member name set mismatch')
        for name in names:
            d = z.read(name); row = {'path': name, 'bytes': len(d), 'sha256': sha(d), 'git_blob': blob(d)}
            need(row == expected_members[name], 'archive member bytes differ: ' + name)
            actual_members.append(row)
        phase = json.loads(z.read('build/current/PHASE_all.json'))
        historical = json.loads(z.read(original['fresh_historical_receipt']))
    log = ci / original['exact_job_log']['file']; logdata = log.read_bytes()
    need((len(logdata), sha(logdata)) == (original['exact_job_log']['bytes'], original['exact_job_log']['sha256']), 'raw job log byte mismatch')
    need(original['exact_head'] == TESTED and original['run_id'] == run['id'] and original['actual_current_ci_success_verified'] is True, 'old verified receipt scope mismatch')
    need((original['math_commands_verified'], original['normal_optimized_actual_pairs_verified'], original['actual_pdflatex_passes'], original['native_pages'], original['fresh_historical_commands_verified'], original['fresh_historical_sources_verified']) == (46, 37, 3, 174, 9, 390), 'prior actual execution summary changed')
    emit('PRIOR_CI_REVALIDATION.json', {
        'scope': 'Fresh GitHub run/jobs/artifact observations and actual byte revalidation of the immutable published B archive. No new download, CI run or mathematical proof is claimed.',
        'run': run, 'jobs': jobs, 'artifacts': artifacts, 'tested_commit': TESTED, 'baseline_metadata_child': BASE,
        'baseline_child_was_not_the_tested_CI_head': True, 'retained_receipt': identity(ci / 'CURRENT_CI_ARTIFACT_VERIFICATION.json'),
        'archive': identity(archive), 'artifact_digest_matches_fresh_GitHub': True, 'all_actual_archive_members_revalidated': actual_members,
        'actual_job_log': identity(log), 'job_log_bytes_unchanged': True, 'actual_current_phase_receipt': phase,
        'actual_B_historical_receipt_path': original['fresh_historical_receipt'], 'actual_B_historical_receipt': historical,
        'original_verified_counts': {k: original[k] for k in ['native_tool_inputs_verified_against_tested_head', 'frozen_inputs_verified_against_tested_head', 'math_commands_verified', 'normal_optimized_actual_pairs_verified', 'actual_pdflatex_passes', 'native_pages', 'fresh_historical_commands_verified', 'fresh_historical_sources_verified', 'historical_documents']},
        'no_new_C_CI_executed': True, 'continuum_mathematical_certificate': False,
    })
    emit('FRESH_SOURCE_REPORT_CI_REVALIDATION.json', {
        'status': 'passed', 'started_utc': started, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'baseline': {'commit': BASE, 'root': ROOT, 'article_tree': ARTICLE, 'files': len(rows), 'bytes': sum(x['bytes'] for x in rows)},
        'counts': {'refs': len(current), 'a2dyn': len(dyn), 'author_refs': len(author), 'author_heads': len(commits),
                   'review_refs': len(review), 'distinct_reports': len(set(review.values())), 'article_trees': len(articles), 'core_trees': len(cores), 'numbered_variants': len(numbered)},
        'old_B_refs_unchanged': True, 'controlling_report': CONTROL, 'controller_scope': '260--276 only',
        'prior_CI_run': run['id'], 'prior_CI_head': TESTED, 'prior_CI_completed_success': True,
        'retained_actual_archive_members_verified': len(actual_members),
        'pre_loss_execution_receipts_recreated': False, 'baseline_rebuilt_in_this_program': False,
        'new_C_remote_commit_or_CI_claimed': False, 'outputs': list(outputs.values()),
    })
    print(json.dumps({'status': 'passed', 'output': str(a / 'FRESH_SOURCE_REPORT_CI_REVALIDATION.json'),
                      'refs': len(current), 'reports': len(set(review.values())), 'author_heads': len(commits),
                      'article_trees': len(articles), 'core_trees': len(cores), 'numbered_variants': len(numbered),
                      'canonical_tree_checks': len(tree_checks), 'baseline_files': len(rows), 'archive_members': len(actual_members)}, indent=2))


if __name__ == '__main__':
    main()
