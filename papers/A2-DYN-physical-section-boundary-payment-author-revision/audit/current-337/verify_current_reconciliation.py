#!/usr/bin/env python3
"""Reconcile frozen complete A2-DYN provenance with newly retrieved 337 delta.

Read-only with respect to all manuscript sources. This checks identities,
native input closure, and observed CI state, not mathematical truth.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re


def need(value, description):
    if not value:
        raise ValueError(description)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def run(baseline, snapshot, evidence):
    evidence = evidence.resolve()
    baseline = baseline.resolve()
    read = lambda p: json.loads(p.read_bytes())
    raw_refs = read(snapshot)
    current_all = {r['ref']: r['sha'] for r in raw_refs}
    need(len(current_all) == len(raw_refs) == 1309, 'Fresh remote ref identity/count')
    current = {r:s for r,s in current_all.items() if 'a2-dyn' in r.lower()}
    prior = read(baseline/'audit/CURRENT_SOURCE_CENSUS_DELTA.json')
    prior_refs = {r['ref']: r['sha'] for r in prior['all_refs']}
    inherited = read(baseline/'audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json')
    need(len(current) == 437 and len(prior_refs) == 436, 'Scoped ref counts')
    added = {r:s for r,s in current.items() if r not in prior_refs}
    changed = {r:{'old':s,'new':current[r]} for r,s in prior_refs.items()
               if r in current and current[r] != s}
    removed = {r:s for r,s in prior_refs.items() if r not in current}
    source = '1cd52fd00675f10f08182f670a42fbbf9e0d1a96'
    carrier = '1e44e7a3360aa1ff41de4fc8f8b71fd173f6ba2a'
    parent = 'd6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28'
    ref = 'refs/heads/revision/a2-dyn-physical-roof-jump-spectrum-2026-10-23'
    article = 'papers/A2-DYN-physical-roof-jump-spectrum-author-revision'
    need(not changed and not removed and added == {ref:carrier}, 'Unexpected scoped ref delta')

    spec = importlib.util.spec_from_file_location('inherited_provenance',baseline/'tools/verify_source_census.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    old_check = module.verify()
    need(old_check['all_passed'], 'Inherited scoped DAG verification')
    old_evidence = read(evidence/'INHERITED_CENSUS_REVALIDATION.json')
    need(old_check == old_evidence, 'Fresh inherited verification differs from saved execution')

    trees = {}
    fresh_tree_count = 0
    for stage in ['SOURCE','CARRIER']:
        commit = read(evidence/f'CURRENT_337_{stage}_COMMIT.json')
        need(commit['sha'] == (source if stage == 'SOURCE' else carrier), 'Wrong commit')
        need([p['sha'] for p in commit['parents']] == ([parent] if stage == 'SOURCE' else [source]),
             'Wrong direct parent')
        for level in ['ROOT','PAPERS','ARTICLE']:
            payload = read(evidence/f'CURRENT_337_{stage}_{level}_TREE.json')
            entries, expected = module.verify_api_tree(payload, level == 'ARTICLE')
            trees[(stage,level)] = (payload, entries)
            fresh_tree_count += len(expected)
        root, papers, packet = [trees[(stage,k)] for k in ['ROOT','PAPERS','ARTICLE']]
        need(commit['tree']['sha'] == root[0]['sha'], 'Root tree mismatch')
        need(root[1]['papers']['sha'] == papers[0]['sha'], 'Papers tree mismatch')
        need(papers[1][article.split('/')[-1]]['sha'] == packet[0]['sha'], 'Article tree mismatch')
    def tree_changes(level):
        a,b = trees[('SOURCE',level)][1],trees[('CARRIER',level)][1]
        return [p for p in sorted(set(a)|set(b)) if a.get(p,{}).get('sha') != b.get(p,{}).get('sha')]
    need(tree_changes('ROOT') == ['papers'], 'Carrier changes outside papers')
    need(tree_changes('PAPERS') == [article.split('/')[-1]], 'Carrier changes other papers')

    cmp = read(evidence/'CURRENT_337_SOURCE_TO_CARRIER_COMPARE.json')
    need(cmp['base'] == source and cmp['head'] == carrier and cmp['ahead_by'] == 1
         and cmp['behind_by'] == 0 and cmp['total_commits'] == 1, 'Source/carrier comparison')
    api_delta = {r['filename'][len(article)+1:]:r for r in cmp['files']}
    need(len(api_delta) == len(cmp['files']) == 14, 'Carrier changed-file count')
    need(all(r['filename'].startswith(article+'/') for r in cmp['files']), 'Carrier isolation')
    a,b = trees[('SOURCE','ARTICLE')][1],trees[('CARRIER','ARTICLE')][1]
    actual_delta = {p for p in set(a)|set(b) if (a.get(p,{}).get('type') == 'blob'
                    or b.get(p,{}).get('type') == 'blob') and a.get(p,{}).get('sha') != b.get(p,{}).get('sha')}
    need(actual_delta == set(api_delta), 'Comparison disagrees with full selected article trees')
    allowed = lambda p: p in {'PUBLICATION_STATUS.json','VALIDATION_REPORT.md','evidence/local/CHANGE_SCOPE.json',
                              'evidence/preliminary/PREPUBLICATION_CHANGE_SCOPE.json'} or p.startswith('evidence/github/')
    need(all(allowed(p) for p in actual_delta), 'Carrier changed sealed mathematical content')
    for p,r in api_delta.items():
        need(r['status'] == ('modified' if p in a else 'added'), 'Carrier status mismatch')
    source_cmp = read(evidence/'CURRENT_337_PARENT_TO_SOURCE_COMPARE.json')
    need(source_cmp['base'] == parent and source_cmp['head'] == source
         and source_cmp['ahead_by'] == 1 and source_cmp['behind_by'] == 0
         and source_cmp['total_commits'] == 1, 'Source/parent comparison')
    source_files = source_cmp['files']
    need(len(source_files) == 286 and all(r['status'] == 'added' for r in source_files), 'Source additions scope')
    outside = [r['filename'] for r in source_files if not r['filename'].startswith(article+'/')]
    need(outside == ['.github/workflows/a2-dyn-physical-roof-jump-spectrum-20261023.yml'], 'Source changed unrelated files')
    need({r['filename'][len(article)+1:] for r in source_files if r['filename'].startswith(article+'/')}
         == {p for p,r in a.items() if r['type'] == 'blob'}, 'Source addition/tree mismatch')

    manifest = read(baseline/'SOURCE_MANIFEST.json')
    checked = []
    for row in manifest['files']:
        data = (baseline/row['path']).read_bytes()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'] and blob(data) == row['git_blob'],
             'Local manifest content mismatch: '+row['path'])
        need(a[row['path']]['sha'] == b[row['path']]['sha'] == row['git_blob'],
             'Source/carrier manifest blob mismatch: '+row['path'])
        checked.append(row)
    native = [r for r in checked if r['path'].endswith('.tex') and not r['path'].startswith('history/')]
    need(native == sorted(native,key=lambda r:r['path']), 'Native hash order')
    native_hash = digest(''.join(r['path']+'\0'+r['sha256']+'\n' for r in native).encode())
    need(len(native) == manifest['active_native_files'] == 90
         and native_hash == manifest['mathematical_source_sha256'], 'Active mathematical source hash')
    seen, pending = set(), ['main.tex']
    while pending:
        p = pending.pop()
        if p in seen:
            continue
        seen.add(p)
        text = re.sub(r'(?<!\\)%[^\n]*','',(baseline/p).read_text())
        for child in re.findall(r'\\(?:input|include)\s*\{([^{}]+)\}',text):
            need('\\' not in child and not child.startswith('/') and '..' not in Path(child).parts,
                 'Unresolved or unsafe native input')
            q = child if child.endswith('.tex') else child+'.tex'
            need((baseline/q).is_file(), 'Missing native input '+q)
            pending.append(q)
    need(seen == {r['path'] for r in native}, 'Native main input closure differs from manifest')
    inherited_bodies = read(baseline/'audit/IMMEDIATE_PREDECESSOR_FILE_IDENTITIES.json')
    inherited_core = 0
    for r in inherited_bodies:
        need(digest((baseline/r['preserved_copy']).read_bytes()) == r['sha256'], 'Missing predecessor body')
        if r['active_byte_identical']:
            need(digest((baseline/r['path']).read_bytes()) == r['sha256'], 'Modified inherited proof')
            inherited_core += r['path'].startswith('core/') and r['path'].endswith('.tex')
    need(inherited_core == 76, 'Inherited complete core count')

    incomplete = []
    for oid,r in inherited['article_trees'].items():
        if not r['native_main_present']:
            incomplete.append({'path':r['first_seen_path'],'article_tree':oid,'main_tex_present':False,
                               'classification':'preparatory or incomplete direct packet, not a complete native manuscript'})
    special = []
    names = ['refs/heads/revision/a2-dyn-v50-referee-response-2026-10-09',
             'refs/heads/revision/a2-dyn-clearance-jacobi-2026-10-15',
             'refs/heads/revision/a2-dyn-v113-clearance-geometry-2026-10-15']
    for r in names:
        c = inherited['commits'][current[r]]
        special.append({'ref':r,'sha':current[r],'root_tree':c['root_tree'],'subject':c['subject']})
    ci = read(evidence/'CURRENT_337_SOURCE_CI_RUN.json')
    jobs = read(evidence/'CURRENT_337_SOURCE_CI_JOBS.json')
    artifacts = read(evidence/'CURRENT_337_SOURCE_CI_ARTIFACTS.json')
    need(ci['head_sha'] == source and ci['id'] == 39920538196, 'Wrong CI source identity')
    need(jobs['total_count'] == len(jobs['jobs']) == 1 and jobs['jobs'][0]['head_sha'] == source, 'Wrong CI job')
    job = jobs['jobs'][0]
    verification_step = next(s for s in job['steps'] if s['name'].startswith('Verify exact source objects'))
    need(ci['status'] == 'completed' and ci['conclusion'] == 'cancelled'
         and verification_step['conclusion'] == 'skipped', 'CI conclusion changed; update retrieved evidence')
    input_paths = [snapshot, baseline/'audit/CURRENT_SOURCE_CENSUS_DELTA.json',
                   baseline/'audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json',baseline/'SOURCE_MANIFEST.json',
                   baseline/'tools/verify_source_census.py']
    input_paths += sorted(evidence.glob('CURRENT_337_*.json'))
    input_paths += [evidence/'INHERITED_CENSUS_REVALIDATION.json',Path(__file__).resolve()]
    identities = [{'path':str(p.relative_to(evidence)) if p.is_relative_to(evidence)
                   else ('baseline/'+str(p.relative_to(baseline)) if p.is_relative_to(baseline) else p.name),
                   'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in input_paths]
    refs = [{'ref':r,'sha':s,'role_hint':r.split('/')[2],
             'identity_basis':'fresh source/carrier/tree comparison' if r in added else 'unchanged validated immutable 436-ref census'}
            for r,s in sorted(current.items())]
    return {
        'schema':'a2-dyn-437-ref-current-reconciliation-v1','status':'PASS',
        'scope':'Frozen remote snapshot reconciliation, validated inherited scoped DAG and fresh 337 delta; not a full historical rebuild, proof reconstruction, or mathematical validity certificate.',
        'remote_total_refs':len(current_all),'scoped_refs':len(current),'prior_scoped_refs':len(prior_refs),
        'unchanged_prior_scoped_refs':len(prior_refs),'added_refs':added,'changed_refs':changed,'removed_refs':removed,
        'role_hints':dict(sorted(Counter(r['role_hint'] for r in refs).items())),
        'inherited_validation':{'status':old_check['status'],'check_groups':len(old_check['checks']),
            'historical_refs':435,'recorded_head_commits':219,'scoped_tree_objects_rehashed':950,
            'scoped_blob_metadata':5631,'preserved_native_blobs_rehashed':660,
            'direct_article_trees':122,'direct_main_entries':120,
            'qualification':'Commit headers are reconciled, not rehashed as absent full commit bodies. Historical immutable trees were rehashed locally, not downloaded again. Direct main presence alone does not certify build closure.'},
        'selected_source':{'branch':ref,'source_commit':source,'source_root_tree':trees[('SOURCE','ROOT')][0]['sha'],
            'source_papers_tree':trees[('SOURCE','PAPERS')][0]['sha'],'source_article_tree':trees[('SOURCE','ARTICLE')][0]['sha'],
            'carrier_commit':carrier,'carrier_root_tree':trees[('CARRIER','ROOT')][0]['sha'],
            'carrier_papers_tree':trees[('CARRIER','PAPERS')][0]['sha'],'carrier_article_tree':trees[('CARRIER','ARTICLE')][0]['sha'],
            'article_path':article,'identical_core_tree':a['core']['sha'],'identical_main_blob':a['main.tex']['sha'],
            'active_native_closure_files':len(native),'inherited_core_bodies_byte_identical':inherited_core,
            'mathematical_source_sha256':native_hash,'source_manifest_sha256':digest((baseline/'SOURCE_MANIFEST.json').read_bytes()),
            'source_file_additions':len(source_files),'carrier_changed_evidence_paths':len(api_delta),
            'manifest_files_locally_rehashed_and_compared_to_both_remote_trees':len(checked),
            'fresh_selected_tree_hashes_recomputed_with_repetitions':fresh_tree_count,
            'scientific_scope':'Complete native 336-337 author increment: physical roof SBV and fixed-m signed jump-spectrum/necessary raw jump condition. Does not prove full raw pointwise LLT or four-coordinate inverse.'},
        'incomplete_direct_packets':incomplete,'special_preparatory_heads':special,
        'source_ci':{'run_id':ci['id'],'head_sha':ci['head_sha'],'status':ci['status'],'conclusion':ci['conclusion'],
            'updated_at':ci['updated_at'],'job_id':job['id'],'validation_step_conclusion':verification_step['conclusion'],
            'artifact_count':artifacts['total_count'],'artifact_sizes':[x['size_in_bytes'] for x in artifacts['artifacts']],
            'qualification':'Successful setup/status/upload steps and a small artifact do not certify validation or build; the mathematical validation/build step was skipped.'},
        'input_identities':identities,'all_refs':refs,'active_native_files':native,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--snapshot',type=Path,required=True)
    parser.add_argument('--evidence',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = run(args.baseline,args.snapshot,args.evidence)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','remote_total_refs','scoped_refs','unchanged_prior_scoped_refs','added_refs']}))
