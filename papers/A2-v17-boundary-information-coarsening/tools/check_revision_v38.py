#!/usr/bin/env python3
"""Finite source-provenance regression tests; no native-paper build is claimed.

The driver fixtures mock TeX and pdfinfo. Separate real-build evidence, when
available, is recorded outside this test. Explicit exceptions remain active
under Python -O. Output contains no temporary paths or timing-dependent data.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from unittest.mock import patch
import zipfile

import build_submission as driver
from source_provenance import (blob_id, freeze_git_source, git, graph,
                               recorder_inputs, require, sha256, source_archive,
                               strip_comments, verify_copy)

HERE = Path(__file__).resolve().parent
RESULTS: dict[str, dict] = {}


def passed(name: str, **details: object) -> None:
    require(name not in RESULTS, 'Duplicate test name: ' + name)
    RESULTS[name] = {'status': 'passed', **details}


def rejected(name: str, action, message: str) -> None:
    try:
        action()
    except (RuntimeError, FileNotFoundError) as exc:
        require(message.lower() in str(exc).lower(), name + ': unexpected rejection: ' + str(exc))
        passed(name, expected_rejection=True)
    else:
        raise RuntimeError(name + ': forbidden input was accepted')


def manifest_for(work: Path, names: tuple[str, ...]) -> dict:
    return {name: {'bytes': (work/name).stat().st_size, 'sha256': sha256(work/name),
                   'git_blob': blob_id((work/name).read_bytes()), 'mode': '100644'}
            for name in names}


def mini_source(work: Path) -> dict:
    work.mkdir(parents=True)
    (work/'main.tex').write_text('\\documentclass{article}\n\\input{shared}\n'
                                '\\begin{document}Provenance fixture.\\end{document}\n')
    (work/'two_collision.tex').write_bytes((work/'main.tex').read_bytes())
    (work/'shared.tex').write_text('% A genuine shared source file.\n')
    return manifest_for(work, ('main.tex', 'two_collision.tex', 'shared.tex'))


def fls(work: Path, extra: str = '', *, entry: bool = True, shared: bool = True,
        pwd: bool = True) -> None:
    lines = ([f'PWD {work.resolve()}'] if pwd else [])
    lines += (['INPUT ./main.tex'] if entry else [])
    lines += (['INPUT shared.tex'] if shared else [])
    (work/'main.fls').write_text('\n'.join(lines) + '\n' + extra)


def recorder_tests(base: Path) -> None:
    expected = {'main.tex', 'shared.tex'}
    for case in ('control', 'mutated', 'missing-recorder', 'empty-recorder',
                 'missing-entry', 'missing-recursive', 'missing-pwd', 'wrong-pwd',
                 'unmapped', 'generated', 'unexplained-generated', 'wrong-stem',
                 'external', 'external-reject', 'symlink-file', 'symlink-escape',
                 'missing-snapshot', 'imported-generated', 'imported-mutated', 'imported-unrecorded'):
        work = base/case
        files = mini_source(work)
        fls(work)
        run = lambda: recorder_inputs('main', work, files, expected, [])
        if case == 'control':
            got = run()
            require(set(got['source_inputs']) == expected, 'Control source inventory')
            for name, value in got['source_inputs'].items():
                require(value['sha256'] == sha256(work/name), 'Control actual-byte hash')
            passed('recorder-control', source_files=2, actual_hashes_verified=True)
        elif case == 'mutated':
            (work/'shared.tex').write_text('Different compilation bytes.\n')
            rejected('mutated-compilation-copy', run, 'Snapshot bytes differ')
        elif case == 'missing-recorder':
            (work/'main.fls').unlink()
            rejected(case, run, 'recorder')
        elif case == 'empty-recorder':
            (work/'main.fls').write_text('')
            rejected(case, run, 'recorder')
        elif case == 'missing-entry':
            fls(work, entry=False)
            rejected(case, run, 'entry is absent')
        elif case == 'missing-recursive':
            fls(work, shared=False)
            rejected(case, run, 'Recursive native inputs absent')
        elif case == 'missing-pwd':
            fls(work, pwd=False)
            rejected(case, run, 'working directory')
        elif case == 'wrong-pwd':
            fls(work, f'PWD {base}\n')
            rejected(case, run, 'working directory')
        elif case == 'unmapped':
            (work/'injected.tex').write_text('% not frozen\n')
            fls(work, 'INPUT injected.tex\n')
            rejected(case, run, 'Unexplained local')
        elif case in ('generated', 'unexplained-generated', 'wrong-stem'):
            name = 'other.aux' if case == 'wrong-stem' else 'main.aux'
            (work/name).write_text('\\relax\n')
            extra = f'INPUT {name}\n'
            if case != 'unexplained-generated':
                extra += f'OUTPUT {name}\n'
            fls(work, extra)
            if case == 'generated':
                got = run()
                require(set(got['generated_inputs']) == {'main.aux'} and
                        'main.aux' not in got['source_inputs'], 'Generated/source separation')
                passed('generated-input-separated')
            else:
                rejected(case, run, 'Unexplained local')
        elif case in ('external', 'external-reject'):
            external = base/('tex-install-'+case)
            external.mkdir()
            (external/'fixture.sty').write_text('% mock installation file; not a font\n')
            fls(work, f'INPUT {external}/fixture.sty\n')
            if case == 'external':
                got = recorder_inputs('main', work, files, expected, [external])
                require(len(got['external_inputs']) == 1, 'External inventory')
                passed('declared-external-input-hashed')
            else:
                rejected('undeclared-external-input', run, 'outside declared')
        elif case == 'symlink-file':
            (work/'shared.tex').unlink()
            (work/'shared.tex').symlink_to(work/'two_collision.tex')
            rejected(case, run, 'symlinked snapshot')
        elif case == 'symlink-escape':
            outside = base/'outside.tex'
            outside.write_text('% outside\n')
            (work/'escape.tex').symlink_to(outside)
            fls(work, 'INPUT escape.tex\n')
            rejected(case, lambda: recorder_inputs('main',work,files,expected,[base]),
                     'escapes compilation tree')
        elif case.startswith('imported-'):
            aux = work/'two_collision.aux'
            aux.write_text('\\relax\n')
            imported = {aux.name: {'bytes':aux.stat().st_size,'sha256':sha256(aux),
                                   'producer_entry':'two_collision.tex'}}
            if case != 'imported-unrecorded':
                fls(work,'INPUT two_collision.aux\n')
            run_imported = lambda: recorder_inputs('main',work,files,expected,[],imported)
            if case == 'imported-generated':
                got = run_imported()
                require(got['generated_inputs'][aux.name]['producer_entry'] == 'two_collision.tex',
                        'Missing generated-input producer identity')
                passed('verified-companion-auxiliary-input')
            elif case == 'imported-mutated':
                aux.write_text('Altered output from another producer\n')
                rejected(case,run_imported,'differs from producer')
            else:
                rejected(case,run_imported,'absent from recorder')
        elif case == 'missing-snapshot':
            (work/'shared.tex').unlink()
            rejected(case, run, 'Missing or symlinked')


def graph_tests(base: Path) -> None:
    work = base/'graph'
    mini_source(work)
    require(graph(work,'main.tex') == {'main.tex','shared.tex'}, 'Recursive graph inventory')
    passed('recursive-input-graph')
    (work/'shared.tex').write_text('% \\input{absent}\n\\input{main}\n')
    require(graph(work,'main.tex') == {'main.tex','shared.tex'}, 'Comment/cycle handling')
    passed('comment-and-cycle-handling')
    (work/'shared.tex').write_text('\\input{../outside}\n')
    rejected('traversal-input',lambda: graph(work,'main.tex'),'Unsafe relative')
    (work/'shared.tex').write_text('\\input{\\dynamic}\n')
    rejected('dynamic-input',lambda: graph(work,'main.tex'),'dynamic TeX input')
    (work/'shared.tex').write_text('\\input{absent}\n')
    rejected('absent-recursive-input',lambda: graph(work,'main.tex'),'Missing regular')
    require(strip_comments(r'\% retained % removed') == r'\% retained ', 'Escaped percent')
    require(strip_comments(r'\\% removed') == r'\\', 'Even escape count')
    passed('tex-comment-parity')


def git_tests(base: Path) -> None:
    repo = base/'fixture-repository'
    repo.mkdir()
    source = repo/'paper'
    mini_source(source)
    (source/'tools').mkdir()
    for name in ('build_submission.py','source_provenance.py'):
        shutil.copyfile(HERE/name, source/'tools'/name)
    (source/'.gitignore').write_text('ignored.tex\n')
    (source/'main.pdf').write_bytes(b'%PDF-old-tracked-product\n')
    git(repo,'init','-q')
    git(repo,'config','user.name','A2 provenance fixture')
    git(repo,'config','user.email','fixture@example.invalid')
    git(repo,'add','paper')
    env = dict(os.environ, GIT_AUTHOR_DATE='2026-09-13T00:00:00+0000',
               GIT_COMMITTER_DATE='2026-09-13T00:00:00+0000')
    cp = subprocess.run(['git','-c','commit.gpgsign=false','commit','-q','-m','Fixture'],
                        cwd=repo,env=env,capture_output=True)
    require(cp.returncode == 0, 'Fixture commit failed')
    snap = base/'git-snapshot'
    mf = freeze_git_source(source,snap,('two_collision','main'))
    require(mf['source_commit'] == git(repo,'rev-parse','HEAD').decode().strip(), 'Commit binding')
    require(mf['source_tree'] == git(repo,'rev-parse','HEAD:paper').decode().strip(), 'Tree binding')
    verify_copy(snap,mf['files'])
    require('main.pdf' not in mf['files'] and 'main.pdf' in mf['excluded_tracked_products'],
            'Tracked product exclusion')
    passed('git-object-snapshot', commit_and_tree_bound=True, all_blob_bytes_verified=True)
    passed('tracked-product-exclusion')
    archive1, archive2 = base/'source1.zip', base/'source2.zip'
    source_archive(snap,mf,archive1)
    source_archive(snap,mf,archive2)
    require(archive1.read_bytes() == archive2.read_bytes(), 'Nondeterministic archive')
    with zipfile.ZipFile(archive1) as z:
        require(json.loads(z.read('SOURCE_MANIFEST.json')) == mf, 'Archive manifest')
        for name,item in mf['files'].items():
            require(hashlib.sha256(z.read('source/'+name)).hexdigest() == item['sha256'],
                    'Archive bytes differ')
    passed('deterministic-retrievable-source-archive')
    original = (source/'shared.tex').read_bytes()
    (source/'shared.tex').write_text('Dirty source\n')
    rejected('dirty-tracked-source',lambda: freeze_git_source(source,base/'dirty',('main',)),
             'not clean')
    (source/'shared.tex').write_bytes(original)
    (source/'untracked.tex').write_text('Untracked source\n')
    rejected('untracked-source',lambda: freeze_git_source(source,base/'untracked',('main',)),
             'not clean')
    (source/'untracked.tex').unlink()
    (source/'ignored.tex').write_text('Ignored data must not enter the snapshot\n')
    ignored = freeze_git_source(source,base/'ignored-snapshot',('main','two_collision'))
    require('ignored.tex' not in ignored['files'], 'Ignored source leaked into snapshot')
    passed('ignored-files-excluded-by-git-object-snapshot')
    (source/'link.tex').symlink_to(source/'shared.tex')
    git(repo,'add','paper/link.tex')
    cp = subprocess.run(['git','-c','commit.gpgsign=false','commit','-q','-m','Symlink fixture'],
                        cwd=repo,env=env,capture_output=True)
    require(cp.returncode == 0,'Symlink commit failed')
    rejected('git-symlink-object',lambda: freeze_git_source(source,base/'symlink-snapshot',('main',)),
             'Nonregular object')


def exact_driver_tests(base: Path) -> None:
    for case in ('control','divergent-copy','absent-recorder','absent-entry',
                 'absent-log','latex-failure','undefined-reference','missing-glyph'):
        work, out = base/('driver-'+case), base/('output-'+case)
        files = mini_source(work)
        out.mkdir()
        def mock_run(cmd, cwd, env, output):
            output.write_text('MOCKED external process; not TeX execution.\n')
            if case != 'absent-log':
                log = 'Mock TeX log for source-provenance unit fixture.\n'
                if case == 'undefined-reference':
                    log += "LaTeX Warning: Reference `missing' on page 1 undefined.\n"
                if case == 'missing-glyph':
                    log += 'Missing character: There is no X in font mock!\n'
                (cwd/'main.log').write_text(log)
            (cwd/'main.pdf').write_bytes(b'%PDF-MOCK-NOT-A-GENUINE-PDF\n')
            if case != 'absent-recorder':
                fls(cwd, entry=case != 'absent-entry')
            if case == 'divergent-copy':
                (cwd/'shared.tex').write_text('Actual compilation copy diverges.\n')
            return 1 if case == 'latex-failure' else 0
        def mock_pdfinfo(cmd, **kwargs):
            require(cmd[0] == 'pdfinfo','Unexpected mocked command')
            return subprocess.CompletedProcess(cmd,0,'Pages: 1\n','')
        with patch.object(driver,'run',side_effect=mock_run), \
             patch.object(driver.subprocess,'run',side_effect=mock_pdfinfo):
            result = driver.build_entry('main',work,out,dict(os.environ),files,
                                        {'main.tex','shared.tex'},[])
        require(result['status'] == ('passed' if case == 'control' else 'failed'),
                'Exact driver regression: '+case+' '+str(result))
        if case == 'control':
            actual = json.loads((out/'main-recorder-inputs.json').read_text())
            require(actual['source_inputs']['main.tex']['sha256'] == sha256(work/'main.tex'),
                    'Exact driver recorded wrong input hash')
        else:
            require('product' not in result, 'Failed verification issued product certificate')
        require((out/'main.pdf').exists(), 'Failed product not retained as evidence')
        passed('exact-driver-'+case, mocked_external_processes=True,
               expected_status=result['status'], genuine_pdf=False)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix='a2-v38-regression-') as tmp:
        base = Path(tmp)
        recorder_tests(base)
        graph_tests(base)
        git_tests(base)
        exact_driver_tests(base)
    report = {'status':'passed','test_count':len(RESULTS),'tests':RESULTS,
              'scope':'Finite provenance regression tests, including the exact new driver; not a native-paper build',
              'external_process_fixture':'Driver unit cases mock TeX/pdfinfo and do not produce genuine PDFs',
              'mathematical_proof_certificate':False,'complete_main_build':False,
              'driver_sha256':sha256(HERE/'build_submission.py'),
              'provenance_module_sha256':sha256(HERE/'source_provenance.py')}
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
