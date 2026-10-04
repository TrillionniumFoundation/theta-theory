#!/usr/bin/env python3
"""Source-bound v79 build, exact regressions and read-only reconstruction.

The archived v78 builder provides unchanged graph, PDF, archive and finite-test
helpers; current identity, preservation and publication checks are defined here.
--preview is explicitly unqualified and never asserts a Git source identity.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('gtf78_build_helpers', ROOT/'predecessor-v78-audit/build_revision.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
DOCS = legacy.DOCUMENTS
SCRIPTS = tuple(legacy.REGRESSION_SCRIPTS) + ('interior_codec_check.py',)
legacy.REGRESSION_SCRIPTS = SCRIPTS
NEW_LABELS = ('thm:interiorentropy79', 'thm:interiorcodec79',
              'thm:prefixrate79', 'thm:interiorlearnedcode79')
WORKFLOW = '.github/workflows/gtf-i-v79-exact-head.yml'
sha, put, require, graph = legacy.sha, legacy.put, legacy.require, legacy.graph
sources, git_output, git_blob = legacy.sources, legacy.git_output, legacy.git_blob
make_zip, pdf_signature = legacy.make_zip, legacy.pdf_signature


def check_source(root: Path):
    inv = sources(root)
    p = json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    require(p['schema'] == 'gtf79.preservation/1', 'v79 preservation required')
    require(len(p['files']) == 360 and len(p['prior_labels']) == 745,
            'the immediate baseline must be v78, not reviewed v77')
    changed = []
    for name, digest in p['files'].items():
        current = root/legacy.safe_relative(name)
        require(current.is_file(), 'predecessor path removed: '+name)
        if sha(current.read_bytes()) != digest:
            require(name in p['archived_originals'], 'unarchived change: '+name)
            archive = root/legacy.safe_relative(p['archived_originals'][name])
            require(archive.is_file() and sha(archive.read_bytes()) == digest,
                    'predecessor original mismatch: '+name)
            changed.append(name)
    for name, original in p['archived_originals'].items():
        require(sha((root/legacy.safe_relative(original)).read_bytes()) == p['files'][name],
                'archived original changed: '+name)
    proof = json.loads((root/'PROOF_TEXT_PRESERVATION.json').read_text())
    require(proof['schema'] == 'gtf79.proof-text-preservation/1'
            and proof['predecessor'] == p['base_commit'], 'proof preservation mismatch')
    require(not proof['removed_proof_sections'] and not proof['reviewed_additive_changes'],
            'inherited mathematical sections must be byte-identical')
    for name in proof['byte_identical_sections']:
        require(inv[name] == p['files'][name], 'inherited proof text changed: '+name)
    graphs = {}
    for entry in DOCS:
        active, labels = graph(root, entry)
        require(len(labels) == len(set(labels)), 'duplicate label: '+entry)
        require(set(p['prior_proof_graphs'][entry]['labels']) <= set(labels),
                'predecessor active label removed: '+entry)
        if entry != 'structural.tex':
            require(set(NEW_LABELS) <= set(labels), 'new theorem absent: '+entry)
        graphs[entry] = {'files': sorted(active), 'labels': labels}
    for name in proof['byte_identical_sections']:
        if name in p['prior_proof_graphs']['main.tex']['files']:
            require(name in graphs['main.tex']['files'], 'inherited section is no longer active: '+name)
    controls = json.loads((root/'CONTROLLING_REPORTS.json').read_text())
    require(controls['revision'] == 79 and controls['review_round'] == 51
            and controls['source_baseline_head'] == p['base_commit'], 'wrong controlling baseline')
    require(controls['reviewed_head'] == '5650842e0bc89ca6a8b6d6730115784f0d9ecc12',
            'R51 reviewed v77, not the later v78/v79')
    require(len(controls['reports']) == 2 and {r['kind'] for r in controls['reports']} == {'external', 'pipeline'},
            'both controlling reports are required')
    for r in controls['reports']:
        data = (root/r['frozen']).read_bytes()
        require(sha(data) == r['sha256'] and git_blob(data) == r['git_blob'], 'report bytes changed')
    status = json.loads((root/'PROOF_STATUS.json').read_text())
    require(all(v is False for v in status['analytic_pipeline_closure'].values()),
            'independent analytic pipeline flags must not be promoted by this paper')
    require(all(s in inv for s in SCRIPTS), 'missing registered regression')
    return {'schema': 'gtf79.source-check/1', 'status': 'success', 'source_files': len(inv),
            'predecessor_native_files': 360, 'preserved_complete_labels': 745,
            'changed_predecessor_files': changed, 'byte_identical_sections': len(proof['byte_identical_sections']),
            'base_commit': p['base_commit'], 'new_theorems': list(NEW_LABELS),
            'documents': {e: {'active_files': len(g['files']), 'active_labels': len(g['labels'])}
                          for e, g in graphs.items()}, 'graphs': graphs}, inv


def committed_source(root: Path, source: str, inv):
    require(re.fullmatch(r'[0-9a-f]{40}', source) is not None, 'full source SHA required')
    repo = Path(git_output(root, 'rev-parse', '--show-toplevel'))
    prefix = root.relative_to(repo).as_posix()+'/'
    raw = subprocess.run(['git', 'ls-tree', '-r', '-z', source, '--', prefix],
                         cwd=repo, capture_output=True, check=True).stdout
    blobs = {}
    for item in raw.split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            mode, kind, digest = meta.decode().split()
            require(kind == 'blob', 'non-file native object')
            blobs[name.decode()] = digest
    expected = {prefix+n: git_blob((root/n).read_bytes()) for n in inv}
    require(blobs == expected, 'native commit must contain exactly the committed native inventory')
    for name, digest in inv.items():
        require(sha((root/name).read_bytes()) == digest, 'native bytes changed')
    return repo


def build(root: Path, *, isolated: bool = False, preview: bool = False, source: str | None = None):
    checked, inv = check_source(root)
    if source is None and not preview:
        source = git_output(root, 'rev-parse', 'HEAD')
        committed_source(root, source, inv)
    evidence, bdir = root/'evidence', root/'build'
    evidence.mkdir(exist_ok=True); bdir.mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH='1791072000', FORCE_SOURCE_DATE='1', TZ='UTC')
    docs, locations, diagnostic = {}, {}, {}
    for entry, pdf in DOCS.items():
        for _ in range(3):
            run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                  '-file-line-error', '-output-directory='+str(bdir), entry],
                                 cwd=root, env=env, capture_output=True, timeout=180)
            require(run.returncode == 0, run.stdout.decode(errors='replace')[-7000:])
        stem = Path(entry).stem
        log = (bdir/(stem+'.log')).read_text(errors='replace')
        for text in ['There were undefined references', 'There were undefined citations',
                     'multiply defined', 'Undefined control sequence', 'Rerun to get cross-references right']:
            require(text not in log, 'unresolved LaTeX diagnostic '+entry+': '+text)
        boxes = re.findall(r'(?:Overfull|Underfull) \\[^\n]+', log)
        require(not boxes, 'typesetting boxes '+entry+': '+repr(boxes))
        diagnostic[entry] = {'unresolved_references_or_citations': False, 'boxes': boxes,
                             'raw_engine_warnings': [s for s in log.splitlines() if 'warning' in s.lower()]}
        (evidence/(stem.upper()+'_LATEX_LOG.txt')).write_text(log)
        shutil.copy2(bdir/(stem+'.pdf'), root/pdf)
        docs[pdf] = pdf_signature(root/pdf)
        docs[pdf]['sha256'] = sha((root/pdf).read_bytes())
        aux = (bdir/(stem+'.aux')).read_text()
        locations[entry] = {m[0]: {'number': m[1], 'page': m[2]} for m in
                           re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}', aux)}
        require(set(checked['graphs'][entry]['labels']) <= set(locations[entry]), 'uncompiled active labels')
    regression = legacy.run_checks(root, evidence)
    put(evidence/'SOURCE_HASHES.json', inv)
    put(evidence/'PAGE_CHECKS.json', docs)
    put(evidence/'THEOREM_LOCATIONS.json', locations)
    require(sources(root) == inv, 'build modified native files')
    native = {n: (root/n).read_bytes() for n in inv}
    make_zip(evidence/'NATIVE_SOURCE.zip', native)
    receipt = {'schema': 'gtf79.build/1', 'status': 'success', 'source_commit': source,
               'qualified_git_source': not preview and source is not None,
               'workflow_trigger_commit': os.environ.get('GITHUB_SHA'),
               'base_commit': checked['base_commit'], 'source_files': len(inv),
               'source_inventory_sha256': sha((evidence/'SOURCE_HASHES.json').read_bytes()),
               'native_source_sha256': sha((evidence/'NATIVE_SOURCE.zip').read_bytes()),
               'source_check': {k: v for k, v in checked.items() if k != 'graphs'},
               'documents': {n: {'pages': v['pages'], 'sha256': v['sha256']} for n, v in docs.items()},
               'latex_diagnostics': diagnostic, 'regression': regression,
               'normal_optimized_identical': True, 'isolated_native_rebuild': False,
               'standalone_journal_rebuild': False,
               'historical_evidence_reused_as_current_qualification': False,
               'scope': 'Native identity, finite exact tests and page reconstruction, not proof or priority certification.',
               'tools': {'python': sys.version.split()[0], 'pymupdf': legacy.fitz.VersionBind,
                         'pdflatex': subprocess.run(['pdflatex', '--version'], capture_output=True,
                                                   text=True, check=True).stdout.splitlines()[0]}}
    journal_names = graph(root, 'quantitative.tex')[0] | {'paper.pdf', 'journal_verify.py', 'JOURNAL_README.md'}
    journal = {n: (root/n).read_bytes() for n in journal_names}
    jm = {'schema': 'gtf79.journal/1', 'source_commit': source,
          'files': {n: sha(data) for n, data in journal.items()}, 'document': docs['paper.pdf'],
          'historical_PDF_dependencies': False, 'repository_dependencies': False}
    journal['JOURNAL_MANIFEST.json'] = (json.dumps(jm, indent=2, sort_keys=True)+'\n').encode()
    make_zip(evidence/'JOURNAL_PACKAGE.zip', journal)
    if isolated:
        with tempfile.TemporaryDirectory(prefix='gtf79-native-') as t:
            temp = Path(t)
            with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as z: z.extractall(temp)
            rebuilt = build(temp, preview=preview, source=source)
            other = json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
            for name in docs:
                require(docs[name]['page_checks'] == other[name]['page_checks'], 'isolated pages differ: '+name)
            require(rebuilt['regression'] == regression, 'isolated regressions differ')
            require(sources(temp) == inv, 'isolated source differs')
        receipt['isolated_native_rebuild'] = True
        with tempfile.TemporaryDirectory(prefix='gtf79-journal-') as t:
            temp = Path(t)
            with zipfile.ZipFile(evidence/'JOURNAL_PACKAGE.zip') as z: z.extractall(temp)
            run = subprocess.run([sys.executable, str(temp/'journal_verify.py')], cwd=temp,
                                 capture_output=True, check=True, timeout=600)
            j = json.loads(run.stdout)
            require(j['status'] == 'success' and j['source_commit'] == source, 'journal rebuild mismatch')
            (evidence/'JOURNAL_REBUILD.json').write_bytes(run.stdout)
        receipt['standalone_journal_rebuild'] = True
    put(evidence/'BUILD_RECEIPT.json', receipt)
    research = {**native, **{n: (root/n).read_bytes() for n in DOCS.values()}}
    for name in ['BUILD_RECEIPT.json', 'SOURCE_HASHES.json', 'PAGE_CHECKS.json', 'THEOREM_LOCATIONS.json', 'REGRESSION_RESULTS.json']:
        research['evidence/'+name] = (evidence/name).read_bytes()
    make_zip(evidence/'RESEARCH_PACKAGE.zip', research)
    put(evidence/'PACKAGE_MANIFEST.json', {'schema': 'gtf79.packages/1', 'source_commit': source,
         'packages': {n: sha((evidence/n).read_bytes()) for n in ['NATIVE_SOURCE.zip', 'JOURNAL_PACKAGE.zip', 'RESEARCH_PACKAGE.zip']},
         'documents': receipt['documents']})
    return receipt


def verify_published(root: Path):
    checked, inv = check_source(root)
    ev = root/'evidence'
    r = json.loads((ev/'BUILD_RECEIPT.json').read_text())
    require(r['schema'] == 'gtf79.build/1' and r['status'] == 'success'
            and r['qualified_git_source'] and r['isolated_native_rebuild']
            and r['standalone_journal_rebuild'], 'qualified current production receipt required')
    require(r['source_check'] == {k: v for k, v in checked.items() if k != 'graphs'}, 'source check receipt mismatch')
    require(inv == json.loads((ev/'SOURCE_HASHES.json').read_text())
            and sha((ev/'SOURCE_HASHES.json').read_bytes()) == r['source_inventory_sha256'], 'source inventory mismatch')
    require(sha((ev/'NATIVE_SOURCE.zip').read_bytes()) == r['native_source_sha256'], 'native archive mismatch')
    pm = json.loads((ev/'PACKAGE_MANIFEST.json').read_text())
    require(pm['schema'] == 'gtf79.packages/1' and pm['source_commit'] == r['source_commit']
            and pm['documents'] == r['documents'], 'package metadata mismatch')
    for n, h in pm['packages'].items(): require(sha((ev/n).read_bytes()) == h, 'package digest mismatch '+n)
    with zipfile.ZipFile(ev/'NATIVE_SOURCE.zip') as z:
        require(len(z.namelist()) == len(inv) and set(z.namelist()) == set(inv), 'native archive inventory mismatch')
        require(all(sha(z.read(n)) == h for n, h in inv.items()), 'native archive bytes mismatch')
    pages = json.loads((ev/'PAGE_CHECKS.json').read_text())
    for name, d in r['documents'].items():
        require(sha((root/name).read_bytes()) == d['sha256'] == pages[name]['sha256'], 'PDF digest mismatch')
        require(pdf_signature(root/name)['page_checks'] == pages[name]['page_checks'], 'published page mismatch')
    journal_names = graph(root, 'quantitative.tex')[0] | {'paper.pdf', 'journal_verify.py', 'JOURNAL_README.md'}
    with zipfile.ZipFile(ev/'JOURNAL_PACKAGE.zip') as z:
        require(len(z.namelist()) == len(journal_names)+1 and
                set(z.namelist()) == journal_names | {'JOURNAL_MANIFEST.json'}, 'journal inventory mismatch')
        jm = json.loads(z.read('JOURNAL_MANIFEST.json'))
        require(jm['schema'] == 'gtf79.journal/1' and jm['source_commit'] == r['source_commit']
                and set(jm['files']) == journal_names and jm['document'] == pages['paper.pdf']
                and not jm['historical_PDF_dependencies'] and not jm['repository_dependencies'],
                'journal manifest differs from published source')
        for n in journal_names:
            require(z.read(n) == (root/n).read_bytes() and sha(z.read(n)) == jm['files'][n],
                    'journal embedded file differs: '+n)
    embedded = ['BUILD_RECEIPT.json', 'SOURCE_HASHES.json', 'PAGE_CHECKS.json', 'THEOREM_LOCATIONS.json', 'REGRESSION_RESULTS.json']
    research_names = set(inv) | set(DOCS.values()) | {'evidence/'+n for n in embedded}
    with zipfile.ZipFile(ev/'RESEARCH_PACKAGE.zip') as z:
        require(len(z.namelist()) == len(research_names) and set(z.namelist()) == research_names,
                'research inventory mismatch')
        for n in research_names: require(z.read(n) == (root/n).read_bytes(), 'research embedded file differs: '+n)
    require(json.loads((ev/'REGRESSION_RESULTS.json').read_text()) == r['regression']
            and set(r['regression']) == set(SCRIPTS) and r['normal_optimized_identical'],
            'regression receipt mismatch')
    j = json.loads((ev/'JOURNAL_REBUILD.json').read_text())
    require(j['schema'] == 'gtf79.journal-rebuild/1' and j['status'] == 'success'
            and j['source_commit'] == r['source_commit'], 'missing actual standalone qualification')
    head = os.environ.get('GITHUB_SHA')
    if head:
        actual = git_output(root, 'rev-parse', 'HEAD')
        require(actual == head, 'checkout is not exact triggering SHA')
        repo = committed_source(root, r['source_commit'], inv)
        require(git_output(root, 'rev-parse', 'HEAD^') == r['source_commit'], 'publication must be direct source child')
        prefix = root.relative_to(repo).as_posix()+'/'
        allowed = {prefix+n for n in DOCS.values()}
        changes = git_output(root, 'diff', '--name-only', r['source_commit'], head).splitlines()
        require(all(n in allowed or n.startswith(prefix+'evidence/') or
                    ('/' not in n and n.startswith('GENERAL_THETA_FOUNDATIONS_I_V79_')) for n in changes),
                'publication altered non-generated sources')
        require(git_output(root, 'rev-parse', head+':'+WORKFLOW) ==
                git_output(root, 'rev-parse', r['source_commit']+':'+WORKFLOW), 'verifier workflow changed')
        preservation = json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
        prior = repo/preservation['source_root']
        require(sha((prior/'evidence/SOURCE_HASHES.json').read_bytes()) == preservation['source_inventory_sha256'],
                'remote predecessor inventory mismatch')
        for name, h in preservation['files'].items():
            require(sha((prior/name).read_bytes()) == h, 'remote predecessor changed: '+name)
        require(not git_output(root, 'status', '--porcelain', '--untracked-files=no'), 'tracked checkout dirty')
    with tempfile.TemporaryDirectory(prefix='gtf79-exact-head-') as t:
        temp = Path(t)
        with zipfile.ZipFile(ev/'NATIVE_SOURCE.zip') as z: z.extractall(temp)
        rebuilt = build(temp, source=r['source_commit'], isolated=True)
        other = json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
        require(rebuilt['regression'] == r['regression'], 'regression reconstruction differs')
        for name in pages: require(pages[name]['page_checks'] == other[name]['page_checks'], 'page reconstruction differs')
        require((temp/'evidence/THEOREM_LOCATIONS.json').read_bytes() == (ev/'THEOREM_LOCATIONS.json').read_bytes(),
                'theorem positions changed')
    require(sources(root) == inv, 'verifier mutated native files')
    if head: require(not git_output(root, 'status', '--porcelain', '--untracked-files=no'), 'verifier modified tracked files')
    return {'schema': 'gtf79.final-head/1', 'status': 'success', 'head': head,
            'source_commit': r['source_commit'], 'exact_git_head_checked': bool(head), 'read_only': True,
            'native_rebuild_text_and_rasters_match': True, 'documents': r['documents'],
            'independent_mathematical_or_human_priority_certification': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check-source', action='store_true')
    ap.add_argument('--preview', action='store_true')
    ap.add_argument('--isolated', action='store_true')
    ap.add_argument('--verify-published', action='store_true')
    args = ap.parse_args()
    if args.check_source:
        result, _ = check_source(ROOT); result.pop('graphs')
    elif args.verify_published:
        require(not args.preview, 'published verification cannot be a preview')
        result = verify_published(ROOT)
    else: result = build(ROOT, preview=args.preview, isolated=args.isolated)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__': main()
