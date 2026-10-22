#!/usr/bin/env python3
"""Seal current refs, immutable author-source coverage, fresh readability, and actual baseline build."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, re

WORK=Path('/workspace/scratch/b5cc344d4c8e')
OUT=WORK/'iteration-20261019b/source-audit'
BASE=WORK/'theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision'
PRIOR=BASE/'audit/current-iteration/source-census'
COMMIT='fdf2603c8bf422314f199fa431086485a0d1ebb5'
ROOT='d90e88848644a25b2d9f2e3a28383f4908d2a646'
ARTICLE='f5c90ecd279dd116330c5d90fa31cae2b0d6f61e'
ARTICLE_PATH='papers/A2-DYN-physical-tube-source-height-author-revision'


def read(p):return json.loads(p.read_text())
def require(test,msg):
    if not test:raise ValueError(msg)
def gid(kind,body):return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\0'+body).hexdigest()
def identity(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':gid('blob',b)}
def canonical(response):
    require(response.get('truncated') is False,'Truncated or undocumented tree response')
    entries=[];seen=set()
    for e in response['tree']:
        require(e['path'] not in seen and '/' not in e['path'],'Not a unique nonrecursive tree entry');seen.add(e['path'])
        n=e['path'].encode();mode=e['mode'].lstrip('0');key=n+(b'/' if e['type']=='tree' else b'')
        entries.append((key,mode.encode()+b' '+n+b'\0'+bytes.fromhex(e['sha'])))
    return gid('tree',b''.join(v for _,v in sorted(entries)))
def a2(name):return re.search(r'a2[-_]dyn',name,re.I) is not None


census=read(OUT/'ALL_BRANCHES_READBACK.json')
require(census['count']==1290==len(census['branches']),'Current census count')
current={r['name']:r['commit']['sha'] for r in census['branches']}
require(len(current)==1290,'Duplicate current refs')
raw_pages=[]
for p in sorted((OUT/'readbacks/branches').glob('*.json'),key=lambda p:int(p.stem)):
    row=read(p);raw_pages.append(row)
require([int(r['name']) for r in raw_pages]==list(range(1,15)),'Branch page coverage')
require(len(raw_pages[-1]['response'])==0,'Branch pagination did not reach empty exhaustion')
require([x for r in raw_pages for x in r['response']]==census['branches'],'Combined branch census differs from actual page bodies')
prior_census=read(WORK/'iteration-20261019/remote-verification/ALL_BRANCHES_AFTER_C1.json')
prior_heads={r['name']:r['commit']['sha'] for r in prior_census['branches']}
prior_final=read(WORK/'iteration-20261019/C3_FINAL_REMOTE_READBACKS.json')
prior_published=dict(prior_heads)
for item in prior_final['readbacks']:
    if item['key'].startswith('ref:'):
        name=item['data']['ref'].removeprefix('refs/heads/')
        require(item['data']['object']['sha']==COMMIT,'Prior final publication ref does not name baseline')
        prior_published[name]=item['data']['object']['sha']
require(current==prior_published,'Uninspected current ref change after actual prior final publication')
a2refs=[r for r in census['branches'] if a2(r['name'])]
authors=[r for r in a2refs if r['name'].split('/')[0] in ('revision','research','referee-copy','referee-response')]
reports=[r for r in a2refs if r['name'].split('/')[0]=='review']
require(len(a2refs)==426 and len(authors)==248 and len(reports)==178,'A2-DYN ref classification')

pinned=read(OUT/'BASELINE_EXPECTED_FILE_IDENTITIES.json')
filemap={r['path']:r for r in pinned['files']}
require(pinned['article_tree_sha']==ARTICLE and len(filemap)==2088,'Wrong baseline file identity list')
reuse_names=['ALL_AUTHOR_COMMIT_READBACKS.json','ALL_AUTHOR_ROOT_TREE_READBACKS.json','ALL_AUTHOR_PAPERS_TREE_READBACKS.json',
            'ALL_AUTHOR_ARTICLE_TREE_READBACKS.json','ALL_AUTHOR_CORE_TREE_READBACKS.json','NUMBERED_NATIVE_VARIANT_WITNESSES.json',
            'SOURCE_CENSUS_VERIFICATION.json','PUBLICATION_CHAIN_AND_UNAVAILABLE_OBJECT_READBACKS.json',
            'SUMMABLE_PREDECESSOR_COMPLETE_TREE_READBACK.json','BASELINE_NATIVE_MANIFEST_RECHECK.json']
reused=[]
for name in reuse_names:
    path=PRIOR/name;rel=path.relative_to(BASE).as_posix();actual=identity(path);want=filemap[rel]
    require((actual['bytes'],actual['sha256'],actual['git_blob'])==(want['bytes'],want['sha256'],want['sha']),'Inherited receipt identity changed: '+name)
    reused.append({'path_in_pinned_baseline_article':rel,'identity':actual,
                   'reuse_scope':'Exact immutable receipt already carried by the pinned C3 article; its original API observation time is retained. It is not relabelled as a new remote fetch.'})

commits={r['requested_sha']:r['response'] for r in read(PRIOR/'ALL_AUTHOR_COMMIT_READBACKS.json')['commits']}
roots={r['requested_sha']:r for r in read(PRIOR/'ALL_AUTHOR_ROOT_TREE_READBACKS.json')['trees']}
papers={r['requested_sha']:r['response'] for r in read(PRIOR/'ALL_AUTHOR_PAPERS_TREE_READBACKS.json')['trees']}
articles={r['requested_sha']:r for r in read(PRIOR/'ALL_AUTHOR_ARTICLE_TREE_READBACKS.json')['trees']}
cores={r['requested_sha']:r['response'] for r in read(PRIOR/'ALL_AUTHOR_CORE_TREE_READBACKS.json')['trees']}
old_variant_receipt=read(PRIOR/'NUMBERED_NATIVE_VARIANT_WITNESSES.json')
fresh={p.stem:read(p) for p in (OUT/'readbacks/fixed').glob('*.json')}
commits[COMMIT]=fresh['baseline_commit']['response']
require(commits[COMMIT]['tree']['sha']==ROOT,'Fresh baseline commit/root mismatch')
roots[COMMIT]={'requested_sha':COMMIT,'canonical_tree_sha':ROOT,'response':fresh['baseline_root']['response']}
papers_sha=fresh['baseline_papers']['response']['sha'];papers[papers_sha]=fresh['baseline_papers']['response']
articles[ARTICLE]={'requested_sha':ARTICLE,'response':fresh['baseline_article']['response'],
                   'occurrences':[{'path':ARTICLE_PATH,'papers_tree':papers_sha,'commits':[COMMIT]}]}
core_sha=fresh['baseline_core']['response']['sha'];cores[core_sha]=fresh['baseline_core']['response']
fresh_canonical=[]
for key,item in fresh.items():
    response=item['response']
    if 'tree' in response and isinstance(response['tree'],list):
        sha=canonical(response);require(sha==response['sha'],'Fresh tree canonical mismatch: '+key)
        fresh_canonical.append({'role':key,'sha':sha,'entries':len(response['tree']),'requested_at':item['requested_at'],'observed_at':item['observed_at']})
require(len(fresh_canonical)==6,'Expected six fresh current-source control trees')
require(next(e['sha'] for e in fresh['baseline_root']['response']['tree'] if e['path']=='papers')==papers_sha,'Fresh root/papers link')
require(next(e['sha'] for e in papers[papers_sha]['tree'] if e['path']==ARTICLE_PATH.split('/')[-1])==ARTICLE,'Fresh papers/article link')
require(next(e['sha'] for e in articles[ARTICLE]['response']['tree'] if e['path']=='core')==core_sha,'Fresh article/core link')

head_rows=[]
for sha in sorted({r['commit']['sha'] for r in authors}):
    require(sha in commits and sha in roots,'Current author head lacks immutable commit/root coverage: '+sha)
    commit=commits[sha];root=roots[sha]['response']
    require(commit['tree']['sha']==roots[sha]['canonical_tree_sha'],'Commit and saved canonical root identity differ')
    paper_entry=next((e for e in root['tree'] if e['path']=='papers'),None)
    candidate_refs=[]
    if paper_entry:
        require(paper_entry['sha'] in papers,'Author papers tree lacks source coverage')
        for entry in papers[paper_entry['sha']]['tree']:
            if entry['type']=='tree' and a2(entry['path']):
                require(entry['sha'] in articles,'A2-DYN article tree lacks immutable coverage: '+entry['path'])
                candidate_refs.append({'path':'papers/'+entry['path'],'article_tree':entry['sha']})
    head_rows.append({'commit':sha,'commit_date':commit['committer']['date'],'root_tree':commit['tree']['sha'],
                      'papers_tree':paper_entry['sha'] if paper_entry else None,
                      'refs':[r['name'] for r in authors if r['commit']['sha']==sha],
                      'source_observation':'Fresh current commit/root/papers/article/core GET and complete native-byte fetch' if sha==COMMIT else 'Current ref head freshly confirmed; matching immutable earlier commit/root/source responses reused by pinned identity',
                      'a2dyn_article_candidates':candidate_refs,
                      'root_a2dyn_source_publication_entries':[e for e in root['tree'] if a2(e['path'])],
                      'rebuilt_this_iteration':sha==COMMIT})
require(len(head_rows)==129,'Current author-head coverage count')
article_rows=[]
for sha,row in sorted(articles.items()):
    response=row['response'];entries={e['path']:e for e in response['tree']};core=entries.get('core')
    numbered=[]
    if core:
        require(core['sha'] in cores,'Missing inherited or fresh core tree')
        numbered=[e for e in cores[core['sha']]['tree'] if e['type']=='blob' and re.match(r'\d+_.*\.tex$',e['path'])]
    article_rows.append({'article_tree':sha,'observed_paths':sorted({x['path'] for x in row.get('occurrences',[])}),
                         'main_tex':entries.get('main.tex'),'source_manifest':entries.get('SOURCE_MANIFEST.json'),
                         'proof_ledger':entries.get('PROOF_LEDGER.md'),'referee_response':entries.get('RESPONSE_TO_REFEREE.md'),
                         'publication_status':entries.get('PUBLICATION_STATUS.json'),
                         'core_tree':core['sha'] if core else None,'numbered_core_files':len(numbered),
                         'native_structural_scope':'Entry presence and exact source identities; this alone does not establish complete TeX closure, successful build, or mathematical validity.',
                         'selected_complete_baseline':sha==ARTICLE})
variants={row['sha']:dict(row) for row in old_variant_receipt['variants']}
for entry in cores[core_sha]['tree']:
    if entry['type']=='blob' and re.match(r'\d+_.*\.tex$',entry['path']):
        if entry['sha'] not in variants:variants[entry['sha']]={**entry,'witnesses':[core_sha]}
        elif core_sha not in variants[entry['sha']].get('witnesses',[]):variants[entry['sha']].setdefault('witnesses',[]).append(core_sha)
require(len(variants)==365,'Expected inherited361 plus four physical-tube numbered variants')

native=read(OUT/'FRESH_NATIVE_BLOB_READBACK_VERIFICATION.json')
require(native['all_match'] and native['actual_native_tex_blob_reads']==64 and native['actual_metadata_blob_reads']==2,'Fresh native source readability incomplete')
build=read(OUT/'baseline-build/REBUILD_RECEIPT.json')
require(build['status']=='passed' and build['commit']==COMMIT and build['pages']==164,'Actual native baseline build did not pass')
require(build['before_and_after_published_files_unchanged']==2088,'Prior article changed during audit')
manifest=read(BASE/'SOURCE_MANIFEST.json')
require(manifest['source_count']==1408 and len(manifest['native_tex_closure']['active_core_files'])==54,'Current complete native manifest')
agent_hits=[]
for sha,row in roots.items():
    for entry in row['response']['tree']:
        if entry['path'].lower()=='agents.md':agent_hits.append({'scope':'author_root','commit':sha,'entry':entry})
for kind,collection in [('papers',papers),('article',{k:v['response'] for k,v in articles.items()}),('core',cores)]:
    for sha,response in collection.items():
        for entry in response['tree']:
            if entry['path'].lower()=='agents.md':agent_hits.append({'scope':kind,'tree':sha,'entry':entry})
for path in filemap:
    if Path(path).name.lower()=='agents.md':agent_hits.append({'scope':'complete_baseline_article','path':path})
require(not agent_hits,'An applicable AGENTS source needs to be read before continuing')
local_agents=[str(p) for p in [WORK/'AGENTS.md',WORK/'theta-theory/AGENTS.md',WORK/'theta-theory/papers/AGENTS.md',BASE/'AGENTS.md'] if p.exists()]
require(not local_agents,'An applicable local AGENTS instruction needs to be read')

unavailable=read(OUT/'HISTORICAL_UNAVAILABLE_OBJECT_RECHECKS.json')
for row in unavailable['reads']:
    require(row['raw_result']['isError'] and row['raw_result']['structuredContent']['error_code']=='NOT_FOUND','A previously missing historical object changed availability; inspect it')
chain=[]
for name,role in [('complete_source_C1','Complete native source publication'),('tested_carrier_C2','Same frozen mathematical source with publication receipts; actual tested carrier')]:
    item=read(OUT/'readbacks/publication'/f'{name}.json');r=item['response']
    chain.append({'role':role,'commit':r['sha'],'root_tree':r['tree']['sha'],'parents':[p['sha'] for p in r['parents']],
                  'commit_date':r['committer']['date'],'commit_message':r['message'],'fresh_receipt':f'readbacks/publication/{name}.json'})
chain.append({'role':'Complete latest author carrier with post-CI evidence; metadata-only [skip ci] successor',
              'commit':COMMIT,'root_tree':ROOT,'article_tree':ARTICLE,'parents':[p['sha'] for p in commits[COMMIT]['parents']],
              'commit_date':commits[COMMIT]['committer']['date'],'fresh_receipt':'readbacks/fixed/baseline_commit.json'})
require(chain[1]['parents']==[chain[0]['commit']] and chain[2]['parents']==[chain[1]['commit']],'Broken latest source/publication ancestry')

result={'schema':'A2-DYN-current-author-source-census-v3','sealed_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS','census_observation_range':[census['observed_started_utc'],census['observed_finished_utc']],
        'branch_counts':{'all':1290,'a2dyn':426,'author_research_copy_response':248,'review':178,'distinct_author_heads':129},
        'current_matches_prior_final_published_heads':True,
        'changes_since_prior_complete_census':'Only the three already-published physical-tube refs advanced from C1 to final C3; after applying their independently saved actual final readbacks, every current head agrees and there are no new/deleted refs.',
        'new_or_changed_review_refs':[],
        'selected_baseline':{'commit':COMMIT,'root_tree':ROOT,'article_path':ARTICLE_PATH,'article_tree':ARTICLE,
                            'published_files':2088,'published_bytes':sum(r['bytes'] for r in filemap.values()),
                            'frozen_inputs':1408,'frozen_input_bytes':manifest['source_bytes'],'manifest_identity':identity(BASE/'SOURCE_MANIFEST.json'),
                            'native_tex_files':64,'active_core_files':54,'active_core_range':[260,313],
                            'fresh_native_and_metadata_blob_reads':66,'actual_fresh_native_build_pages':164,
                            'build_receipt':'baseline-build/REBUILD_RECEIPT.json',
                            'selection_reason':'All current author heads are covered by fresh ref enumeration plus pinned complete source catalogs; no later candidate ref appeared. This source has a fresh exact 2,088-file identity check, all64 native TeX blobs actually readable remotely, both manifest/history anchors verified, and a real isolated three-pass rebuild. Version numbers, wrappers, queued workflows and finite simulations do not determine the selection.'},
        'inherited_catalog_counts':{'commit_heads':128,'root_trees':128,'papers_trees':114,'article_trees':116,'core_trees':112,'numbered_variants':361},
        'merged_catalog_counts':{'commit_heads':len(head_rows),'root_trees':len(roots),'papers_trees':len(papers),'article_trees':len(articles),'core_trees':len(cores),'numbered_variants':len(variants)},
        'fresh_canonical_git_tree_readbacks':fresh_canonical,'reused_immutable_receipts':reused,
        'author_heads':head_rows,'article_sources':article_rows,'publication_chain':chain,
        'applicable_AGENTS_hits':agent_hits,'applicable_local_AGENTS':local_agents,
        'historical_unavailable_objects':{'fresh_not_found_count':4,'receipt':'HISTORICAL_UNAVAILABLE_OBJECT_RECHECKS.json'},
        'processing_event_scope':'FETCH_PROCESSING_EVENTS.json preserves three corrected local JSON-extraction mistakes after successful UTF-8 blob GETs; all affected documents have successful exact subsequent body readbacks. No current source is missing.',
        'mathematical_scope':'Source identity and actual native-build audit only. No new referee review, no new mathematical proof, no claim of an independent human report, and no new CI run. The actual prior CI belongs to C2, not the metadata-only C3 carrier.'}
(OUT/'CURRENT_AUTHOR_SOURCE_CENSUS.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'CURRENT_NUMBERED_NATIVE_VARIANTS.json').write_text(json.dumps({'count':len(variants),'scope':'Immutable historical361 variants plus the four previously published310–313 native bodies; inherited results are not described as new mathematical contributions.','variants':list(variants.values())},indent=2)+'\n')
(OUT/'SOURCE_HISTORY_REUSE_MANIFEST.json').write_text(json.dumps({'pinned_baseline':COMMIT,'article_tree':ARTICLE,'receipts':reused},indent=2)+'\n')
summary=f'''# Current A2-DYN author-source baseline — 19 October 2026, second iteration\n\n**Selected complete author baseline: `{COMMIT}`**, root tree `{ROOT}`, article tree `{ARTICLE}` at `{ARTICLE_PATH}`. This is an author-source audit, not a new referee review.\n\n## Current ref census and source coverage\n\nThe actual GitHub branch collection was exhausted through fourteen pages, with the last page empty: **1,290 refs**, including **426 A2-DYN refs**. These comprise 243 revision refs, one research ref, two referee-copy refs, two referee-response refs, and 178 review refs. The 248 author/research/copy/response refs map to **129 distinct author heads**, each mapped to its exact root and applicable article source trees in `CURRENT_AUTHOR_SOURCE_CENSUS.json`.\n\nNo ref was added or removed after the previous 1,290-ref census. Its only later movements are the three already-published physical-tube refs from C1 to final C3. Applying the saved actual final C3 ref readbacks leaves **every current repository ref unchanged** relative to that documented last publication state. All review refs remain unchanged; no new report candidate appears. This time-scoped statement does not erase the unrelated General Theta movement recorded during the earlier iteration.\n\nThe earlier immutable catalog covers 128 author heads, 114 papers trees, 116 article trees, 112 core trees and 361 numbered native variants. Each reused receipt is pinned by its exact Git blob, SHA-256 and byte count inside the complete baseline article. Its earlier API observation scope is preserved. The newly merged catalog covers {len(papers)} papers trees, {len(articles)} article trees, {len(cores)} core trees and **365 numbered variants**; the four additions are already-published bodies 310–313. They are inherited baseline results for this iteration.\n\n## Actual completeness, readability and build\n\nAll **2,088 published files**, totaling **{sum(r['bytes'] for r in filemap.values()):,} bytes**, match the pinned final article identities before and after this audit. All **64 native TeX sources** and the two metadata documents `SOURCE_MANIFEST.json` and `SOURCE_IDENTITIES.json` were actually fetched from GitHub and compared byte for byte with their pinned blobs. Six current control trees were freshly fetched and canonically recomputed.\n\nThe unchanged manifest covers **1,408 frozen inputs / 105,914,630 bytes**; both immutable history anchors pass read-only verification. The active native chain remains **260–313, 54 complete bodies**. The manuscript was actually rebuilt into `baseline-build/` with three successful pdflatex passes, and pdfinfo reports **164 pages**. The actual TeX recorder observes every declared native input. No blocking missing-reference/citation, duplicate-destination, overfull-box, missing-glyph or TeX-error diagnostic is present. The retained AMS advisory lines are recorded without rewriting the baseline. The existing article and its published files were not modified.\n\nThis identifies the selected source by complete byte evidence and an actual build. Higher numbered partial wrappers, incomplete source manifests, queued workflow states, finite scripts and simulated qualification results are not classified as complete or mathematically validated manuscripts. Entry presence in the historical article catalog is explicitly weaker than a completed source/build claim.\n\n## Publication and review scope\n\nC1 `706aa8d1bca33b0d6268806cca873d57511ad8d9` contains the complete new native source. C2 `8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2` carries the same frozen inputs and is the actual tested head of run 39187286448. Final C3 `{COMMIT}` adds post-CI publication evidence with `[skip ci]`. The fresh commit ancestry is saved. C3 is selected as the latest complete author carrier while its independent build in this audit and the earlier exact C2 CI remain distinct observations.\n\nThe controlling-report determination is handled by the separate review/CI audit. The unchanged review census supplies no later report claiming to assess this source. The prior controlling report at `f01482035a0b945b50f1f9c30f30ef35077558dc` explicitly assessed author `31792379408c5ace2c09284c2eb22d2331023433`, with direct core scope 260–276. It is not a human journal verdict and is not an A2 geometry endorsement of A2-DYN. Its later applicability concerns inherited unresolved objections, not an invented direct review of bodies 277–313.\n\n## History, unavailable objects and instructions\n\nThe original source/manifests, all retained review/proof/response material, failed attempts and earlier actual execution receipts remain at their exact baseline identities. The four historically unavailable Git objects were freshly requested again and all still return explicit 404s; their actual error receipts are preserved separately. They are not used to manufacture missing source content. The historical fb99 manifest inconsistency and its recovered-source scope remain in the pinned original audits.\n\nNo applicable `AGENTS.md` appears in the current root/papers/article/core trees, the complete current article file inventory, the inherited author root/source catalog or the local article ancestors.\n\n`FETCH_PROCESSING_EVENTS.json` also records a local extraction correction: this GitHub connector returns UTF-8 blob bodies, so an initial JSON-parser assumption failed for three TeX files after successful GETs. Subsequent exact-body readbacks of every native source resolved those events; no current manuscript source is unavailable.\n\nThe full raw pointwise local limit theorem and four-coordinate inversion retain their original stated mathematical obligations. Source identity, successful compilation, and CI do not close those proofs.\n'''
(OUT/'BASELINE_SELECTION_AND_HISTORY_SCOPE.md').write_text(summary)
print(json.dumps({'status':'PASS','baseline':COMMIT,'branch_counts':result['branch_counts'],'merged_catalog_counts':result['merged_catalog_counts'],'fresh_canonical_trees':len(fresh_canonical),'native_remote_reads':66,'native_pages':164,'current_AGENTS_hits':0,'fresh_historical_404s':4},sort_keys=True))
