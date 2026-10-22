#!/usr/bin/env python3
"""Independently verify actual new CI receipts and bytes; never rerun source checks.

This is an evidence readback, not a mathematical diagnostic, a compiler rerun,
an external expert reconstruction, or a continuum proof certificate.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE_SHA = '6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9'
ARTICLE = 'papers/A2-DYN-physical-roof-variation-author-revision'
MATH_SHA = '52e7443237ebdcc1b2feb6a845c56ab0d87fb61312a781e13572371992bdb5c9'
MANIFEST_SHA = '6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86'
RUN_ID = 39526895726
JOB_ID = 118983561729


def read_json(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact-id', required=True, type=int)
    parser.add_argument('--zip', required=True, type=Path)
    parser.add_argument('--artifact-root', type=Path, default=ROOT/'artifact')
    parser.add_argument('--details', type=Path, default=ROOT/'ARTIFACT_VERIFICATION.json')
    args = parser.parse_args()
    artifact_root = args.artifact_root.resolve()
    checks = []

    def require(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def verify_bytes(path, size, expected_sha, label):
        require(path.is_file(), label+': file present')
        require(path.stat().st_size == size, label+': byte count')
        require(digest(path) == expected_sha, label+': SHA256')

    run = read_json(ROOT/f'run-{RUN_ID}.json')
    jobs = read_json(ROOT/f'jobs-{RUN_ID}.json')
    artifacts = read_json(ROOT/f'artifacts-{RUN_ID}.json')
    require(run['id'] == RUN_ID and run['run_attempt'] == 1, 'actual run and attempt identity')
    require(run['head_sha'] == SOURCE_SHA and run['event'] == 'push', 'actual push tests exact published source')
    require(run['head_branch'] == 'revision/a2-dyn-physical-roof-variation-2026-10-21', 'actual revision branch')
    require(run['path'] == '.github/workflows/a2-dyn-physical-roof-variation-20261021.yml', 'actual new workflow path')
    require(run['status'] == 'completed' and run['conclusion'] == 'success', 'actual run completed successfully')
    require(jobs['total_count'] == len(jobs['jobs']) == 1, 'jobs metadata is exhaustive')
    job = jobs['jobs'][0]
    require(job['id'] == JOB_ID and job['head_sha'] == SOURCE_SHA, 'job identity and exact checkout source')
    require(job['status'] == 'completed' and job['conclusion'] == 'success', 'job completed successfully')
    require(bool(job['steps']) and all(s['status'] == 'completed' and s['conclusion'] == 'success' for s in job['steps']), 'every actual reported step succeeded')
    required_step_names = {
        'Check out the exact author revision', 'Record the actual checkout',
        'Install native TeX and pinned mathematical dependencies',
        'Rebuild and verify the complete native author revision',
        'Retain the actual run outcome',
        'Upload actual current and historical build records',
    }
    require(required_step_names <= {s['name'] for s in job['steps']}, 'all substantive requested workflow steps exist')
    require(artifacts['total_count'] == len(artifacts['artifacts']) == 1, 'artifact metadata is exhaustive')
    artifact = artifacts['artifacts'][0]
    require(artifact['id'] == args.artifact_id and not artifact['expired'], 'actual retained artifact identity')
    require(artifact['workflow_run']['id'] == RUN_ID and artifact['workflow_run']['head_sha'] == SOURCE_SHA, 'artifact belongs to this run and exact source')
    require(artifact['name'] == f'a2-dyn-physical-roof-variation-{SOURCE_SHA}-{RUN_ID}-1', 'artifact name binds source, run and attempt')
    verify_bytes(args.zip, artifact['size_in_bytes'], artifact['digest'].removeprefix('sha256:'), 'downloaded actual ZIP')
    with zipfile.ZipFile(args.zip) as archive:
        require(archive.testzip() is None, 'all downloaded ZIP member CRCs agree')
        names = [i.filename for i in archive.infolist()]
        require(len(names) == len(set(names)), 'ZIP contains no duplicate member path')
        members = 0
        for info in archive.infolist():
            p = PurePosixPath(info.filename)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename, 'safe archive path: '+info.filename)
            require((info.external_attr >> 16) & 0o170000 != 0o120000, 'archive is not a symlink: '+info.filename)
            if info.is_dir():
                continue
            members += 1
            path = artifact_root/info.filename
            require(path.is_file() and path.read_bytes() == archive.read(info.filename), 'extracted exact ZIP bytes: '+info.filename)

    current = artifact_root/'current'
    require((current/'CI_CHECKOUT_SHA.txt').read_text().strip() == SOURCE_SHA, 'retained checkout equals actual tested SHA')
    require((current/'CI_BUILD_OUTCOME.txt').read_text().strip() == 'success', 'retained actual build outcome is success')
    require((current/'CI_POST_RUN_STATUS.txt').read_text().strip() in ('', '?? '+ARTICLE+'/build/'), 'actual job reports clean status or only generated build output as untracked')
    entrypoint_rows = {}
    for line in (current/'CI_ENTRYPOINT_SHA256.txt').read_text().splitlines():
        h, path = line.split(None, 1)
        entrypoint_rows[path.strip()] = h
    for name in ['build.sh', 'requirements.txt', 'ci/a2-dyn-physical-roof-variation-20261021.yml']:
        require(entrypoint_rows[name] == digest(ROOT/'tested-source'/name), 'actual recorded entrypoint equals committed source: '+name)
    require(digest(ROOT/'tested-workflow-6708e30.yml') == entrypoint_rows['ci/a2-dyn-physical-roof-variation-20261021.yml'], 'actual public root workflow equals recorded frozen copy')
    require(digest(ROOT/'tested-SOURCE_MANIFEST-6708e30.json') == MANIFEST_SHA, 'published frozen manifest exact hash')
    manifest = read_json(ROOT/'tested-SOURCE_MANIFEST-6708e30.json')
    published = read_json(ROOT/'PUBLISHED_SOURCE_READBACK.json')
    require(published['status'] == 'passed' and published['source_commit'] == SOURCE_SHA, 'published source identity was independently checked')
    require(published['frozen_files'] == len(manifest['files']) == 130, 'all 130 frozen inputs retained')

    phase = read_json(current/'PHASE_all.json')
    source = read_json(current/'source-checks.json')
    math = read_json(current/'mathematical-checks.json')
    native = read_json(current/'native-typeset.json')
    expected_identity = [{'path':r['path'], 'sha256':r['sha256']} for r in manifest['files'] if not r['path'].startswith('ci/')]
    require(hashlib.sha256(json.dumps(expected_identity, sort_keys=True).encode()).hexdigest() == MATH_SHA, 'independent exact mathematical source digest')
    for name, payload in [('all-phase',phase),('source',source),('mathematics',math),('typeset',native)]:
        require(payload['status'] == 'passed', name+' actual receipt passed')
        require(payload['mathematical_source']['sha256'] == MATH_SHA, name+' exact source digest')
        require(payload['mathematical_source']['files'] == expected_identity, name+' all 129 driver input identities agree')
    require(phase['phase'] == 'all' and set(phase['completed']) == {'source','math','typeset'}, 'actual complete all-phase receipt')
    require(phase['continuum_proof_certificate'] is False and math['continuum_proof_certificate'] is False and native['mathematical_proof_certificate'] is False, 'actual receipts do not claim continuous mathematical proof')
    require(source['original_files_preserved'] == 4393 and source['original_bytes_preserved'] == 544226975, 'actual complete 4d83 predecessor preservation gate')
    require(source['source_article_tree'] == '7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa' and source['reconstructed_original_tree'] == source['source_article_tree'], 'actual predecessor article tree reconstruction')

    tree = ast.parse((ROOT/'tested-source/tools/validate_revision.py').read_text())
    programs = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'PROGRAMS' for t in n.targets))
    require(len(programs) == len(set(programs)) == 34, 'committed driver has 34 distinct programs')
    expected_tags = {p+'-'+m for p in programs for m in ('normal','optimized')}
    require(math['commands_completed'] == math['commands_expected'] == len(math['commands']) == 68, 'all 68 actual finite-check commands completed')
    require({c['tag'] for c in math['commands']} == expected_tags, 'all expected normal and optimized invocations appear exactly once')
    require(not math['failures'], 'no actual mathematical command or comparison failure')
    for kind, payload, folder in [('mathematics',math,current),('native',native,current/'native')]:
        for command in payload['commands']:
            require(command['exit_code'] == 0, kind+' command exit zero: '+command['tag'])
            require(command['current_mathematical_source_sha256'] == MATH_SHA, kind+' command source binding: '+command['tag'])
            verify_bytes(folder/command['log'], command['log_bytes'], command['log_sha256'], kind+' actual log: '+command['tag'])
    require(len(native['commands']) == 4 and {c['tag'] for c in native['commands']} == {'pdflatex-pass1','pdflatex-pass2','pdflatex-pass3','pdfinfo'}, 'three actual native TeX passes and actual pdfinfo')
    expected_comparisons = {(p,'stdout') for p in programs} | {(p,'details') for p in programs[9:]}
    require(len(math['normal_optimized_comparisons']) == 59, '59 actual normal/optimized comparisons')
    require({(c['program'],c['scope']) for c in math['normal_optimized_comparisons']} == expected_comparisons, 'normal/optimized comparison coverage is exact')
    for comparison in math['normal_optimized_comparisons']:
        require(comparison['match'], 'recorded normal/optimized match: '+comparison['program']+'/'+comparison['scope'])
        suffix = '.log' if comparison['scope'] == 'stdout' else '.details.json'
        left_path = current/(comparison['program']+'-normal'+suffix)
        right_path = current/(comparison['program']+'-optimized'+suffix)
        require(digest(left_path) == comparison['sha256'], 'normal comparison digest: '+comparison['program']+'/'+comparison['scope'])
        if comparison['program'] in ('check_all_offset_boundary','check_positive_critical_fans'):
            left, right = read_json(left_path), read_json(right_path)
            for payload in (left,right):
                for key in ('executed_utc','optimized'):
                    payload.pop(key,None)
            require(left == right, 'independent JSON comparison with only declared runtime fields removed: '+comparison['program']+'/'+comparison['scope'])
        else:
            require(comparison['comparison'] == 'byte-identical' and left_path.read_bytes() == right_path.read_bytes(), 'independent byte comparison: '+comparison['program']+'/'+comparison['scope'])
    for program, module in [('check_complete_roof_variation','323_complete_physical_roof_variation.tex'),('check_326_boundary_pressure','326_physical_boundary_stopping_pressure.tex')]:
        payload = read_json(current/(program+'-normal.details.json'))
        require(payload.get('source_sha256') == digest(ROOT/'tested-source/core'/module), 'new auxiliary diagnostic exact native source: '+program)

    verify_bytes(current/'native/main.pdf', native['pdf_bytes'], native['pdf_sha256'], 'actual native PDF')
    require(digest(current/'native/main.aux') == native['aux_sha256'], 'actual native auxiliary digest')
    require(native['pages'] == 233 and len(native['actual_recorder_native_tex']) == 78, 'actual 233-page native document and 78-file TeX closure')
    require(native['actual_recorder_matches_declared_closure'] is True, 'actual recorder explicitly matches declared closure')
    require(set(native['actual_recorder_native_tex']) == set(manifest['reachable_tex_files']), 'actual recorder closure equals exact committed manifest')
    require(not native['layout_or_reference_problems'], 'no reported native layout or reference problem')
    final_log = (current/'native/main.log').read_text(errors='replace')
    require(not re.search(r'LaTeX Warning:.*undefined|Reference .+ undefined|Citation .+ undefined|multiply defined|Overfull \\[hv]box|Missing character:|^!',final_log,re.M), 'independent native final-log diagnostic scan')
    fls_inputs = set()
    for line in (current/'native/main.fls').read_text().splitlines():
        if not line.startswith('INPUT '):
            continue
        p = line[6:]
        marker = ARTICLE+'/'
        if marker in p:
            p = p.split(marker,1)[1]
        elif p.startswith('./'):
            p = p[2:]
        elif p.startswith('/'):
            continue
        if p.endswith('.tex') and not p.startswith(('history/','build/','evidence/')):
            fls_inputs.add(p)
    require(fls_inputs == set(manifest['reachable_tex_files']), 'independently parsed compiler recorder equals all declared native files')

    historical = artifact_root/'current-history'
    history = read_json(historical/'REBUILD_SUMMARY.json')
    require(history['exit_code'] == 0, 'actual historical rebuild completed successfully')
    require(history['historical_repository_wide_gate_executed'] is False, 'historical repository-wide gate remains explicitly unexecuted')
    verify_bytes(historical/'rebuild.stdout.log', history['log']['bytes'], history['log']['sha256'], 'actual historical rebuild stdout')
    receipt_paths = list(historical.glob('execution/*/REBUILD_RECEIPT.json'))
    require(len(receipt_paths) == 1, 'exactly one retained actual historical attempt')
    receipt_path = receipt_paths[0]
    receipt = read_json(receipt_path)
    require(receipt['success'] is True and receipt['source_files_checked'] == 390, 'actual 390-source historical assembly succeeded')
    for command in receipt['commands']:
        require(command['returncode'] == 0, 'actual historical command exit zero: '+Path(command['output']).name)
        identity = command['output_identity']
        verify_bytes(receipt_path.parent/Path(command['output']).name, identity['bytes'], identity['sha256'], 'actual historical command log: '+Path(command['output']).name)
    for document in receipt['documents']:
        identity = document['pdf']
        verify_bytes(historical/('historical-'+document['document']+'.pdf'), identity['bytes'], identity['sha256'], 'actual historical PDF: '+document['document'])
        identity = document['log']
        verify_bytes(receipt_path.parent/(document['document']+'.final.log'), identity['bytes'], identity['sha256'], 'actual historical final log: '+document['document'])
    require([d['pages'] for d in receipt['documents']] == [26,883], 'actual historical main and supplement pages 26 and 883')
    result = {
        'status':'passed',
        'scope':'Independent readback of actual remote CI metadata, logs and downloaded artifact bytes; no source test/compiler rerun and no mathematical proof certificate.',
        'remote_run':run['html_url'], 'run_id':RUN_ID, 'attempt':run['run_attempt'],
        'tested_sha':SOURCE_SHA, 'root_tree':'ad34fd91ad2f1c6e594d3bbe437417aba524bf87',
        'article_tree':'4f41b3a98487a1ae0507d40390aca030c5520e19',
        'job_id':JOB_ID, 'job_conclusion':job['conclusion'], 'steps':len(job['steps']),
        'artifact_id':artifact['id'], 'artifact_bytes':artifact['size_in_bytes'],
        'artifact_sha256':digest(args.zip), 'artifact_file_members':members,
        'mathematical_source_sha256':MATH_SHA, 'frozen_manifest_sha256':MANIFEST_SHA,
        'finite_check_commands':len(math['commands']), 'normal_optimized_comparisons':len(math['normal_optimized_comparisons']),
        'native_pages':native['pages'], 'native_tex_files':len(native['actual_recorder_native_tex']),
        'native_pdf_sha256':native['pdf_sha256'], 'historical_pages':[d['pages'] for d in receipt['documents']],
        'native_compile_advisories':native['advisories'],
        'historical_compile_advisories':{d['document']:d['diagnostics'] for d in receipt['documents']},
        'historical_repository_wide_gate_executed':False, 'continuum_proof_certificate':False,
        'ci_blocker_observed':False, 'source_or_workflow_repair_required':False,
        'checks_completed':len(checks), 'checks':checks,
    }
    args.details.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'checks'},indent=2))


if __name__ == '__main__':
    main()
