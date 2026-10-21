#!/usr/bin/env python3
"""Execute the current A2-DYN source, mathematical, and native TeX checks.

Extended from the preserved predecessor driver for the complete 260--322
native source. Every command receipt describes an actual execution. Passing
finite computations is not a continuum proof or an independent certification
of the inherited dynamical inputs.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PROGRAMS = [
    'check_finite', 'check_research', 'check_load', 'check_clearance',
    'check_critical_coarea', 'check_two_mark', 'check_cross_flight',
    'check_angular_source', 'check_uniform_growth', 'check_momentum_critical',
    'check_radial_coarea', 'check_endpoint_localization',
    'check_reflection_resolvent', 'check_physical_tubes',
    'check_critical_clock', 'check_global_variational', 'check_sublevel',
    'check_summable_source', 'verify_localization',
    'check_critical_tube_volume', 'check_physical_source_height',
    'check_explicit_optical', 'check_full_physical_source',
    'check_marked_source_kernel', 'check_marked_boundary_flux', 'check_cross_curve_distortion',
    'check_two_sided_marked_capacity', 'check_all_offset_boundary', 'check_transversal_capacity', 'check_positive_critical_source', 'check_positive_critical_fans',

]
DETAILS = set(PROGRAMS[9:])
OUTPUT_FLAG = {'check_sublevel', 'verify_localization', 'check_all_offset_boundary', 'check_positive_critical_fans'}
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           PYTHONDONTWRITEBYTECODE='1')

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n')

def source_identity():
    paths = sorted(list(ROOT.glob('*.tex')) + list((ROOT/'core').glob('*.tex'))
                   + list((ROOT/'tools').glob('*.py')) + [ROOT/'requirements.txt',ROOT/'build.sh'],
                   key=lambda p: p.relative_to(ROOT).as_posix())
    rows = [{'path':p.relative_to(ROOT).as_posix(), 'sha256':sha(p.read_bytes())}
            for p in paths]
    return {'sha256':sha(json.dumps(rows,sort_keys=True).encode()), 'files':rows}

def require(value, message):
    if not value:
        raise RuntimeError(message)

def run(command, tag, output, identity, cwd=ROOT):
    output.mkdir(parents=True, exist_ok=True)
    log = output / (tag + '.log')
    start = utc()
    monotonic = time.monotonic()
    with log.open('wb') as handle:
        proc = subprocess.run(command, cwd=cwd, env=ENV, stdout=handle,
                              stderr=subprocess.STDOUT, check=False)
    receipt = {
        'tag':tag, 'command':command, 'cwd':str(cwd),
        'started_utc':start, 'finished_utc':utc(),
        'elapsed_seconds':round(time.monotonic()-monotonic,6),
        'exit_code':proc.returncode,
        'current_mathematical_source_sha256':identity['sha256'],
        'log':log.name, 'log_bytes':log.stat().st_size,
        'log_sha256':sha(log.read_bytes()),
    }
    write_json(output/(tag+'.command.json'), receipt)
    require(proc.returncode == 0,
            f'Command failed with exit {proc.returncode}: {tag}; see {log}')
    return receipt

def source_checks(output, identity):
    spec = importlib.util.spec_from_file_location(
        'current_source_preservation', ROOT/'tools/check_source_preservation.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.verify(ROOT, manifest_required=True)
    publication=json.loads((ROOT/'PUBLICATION_STATUS.json').read_text())
    require(publication.get('full_raw_pointwise_llt_complete') is False
            and publication.get('four_coordinate_inversion_complete') is False,
            'Publication status overstates the remaining mathematical theorem')
    result.update({'mathematical_source':identity,
                   'mathematical_proof_certificate':False})
    write_json(output/'source-checks.json',result)
    return result

def math_checks(output, identity, workers):
    all_jobs=[(program,optimized) for program in PROGRAMS for optimized in (False,True)]
    def job(program, optimized):
        label=program+('-optimized' if optimized else '-normal')
        command=[sys.executable]+(['-O'] if optimized else [])+[
            str(ROOT/'tools'/(program+'.py'))]
        if program in DETAILS:
            command += [('--output' if program in OUTPUT_FLAG else '--details'),
                        str(output/(label+'.details.json'))]
        if program=='check_transversal_capacity':
            command += ['--source-root',str(ROOT),'--manuscript',str(ROOT/'core/321_all_class_transversal_capacity.tex')]
        if program=='check_positive_critical_fans':
            command += ['--source',str(ROOT/'core/322_positive_critical_marked_source.tex')]
        if program=='verify_localization':
            command += ['--source-root',str(ROOT/'core')]
        return run(command,label,output,identity)
    receipts=[]
    failures=[]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures={executor.submit(job,*pair):pair for pair in all_jobs}
        for future in as_completed(futures):
            try:
                receipts.append(future.result())
            except Exception as exc:
                failures.append({'job':futures[future], 'error':str(exc)})
    comparisons=[]
    for program in PROGRAMS:
        files=[('.log','stdout')]
        if program in DETAILS:
            files.append(('.details.json','details'))
        for suffix,scope in files:
            a=output/(program+'-normal'+suffix)
            b=output/(program+'-optimized'+suffix)
            comparison='byte-identical'
            same=a.is_file() and b.is_file() and a.read_bytes()==b.read_bytes()
            if program in ('check_all_offset_boundary','check_positive_critical_fans') and a.is_file() and b.is_file():
                # Preserve both actual execution records. Only runtime metadata
                # differs between this checker's normal and optimized invocations.
                left,right=json.loads(a.read_text()),json.loads(b.read_text())
                for payload in (left,right):
                    for key in ('executed_utc','optimized'):
                        payload.pop(key,None)
                same=left==right
                comparison='identical mathematical JSON; runtime timestamp and optimization flag excluded'
            comparisons.append({'program':program,'scope':scope,
                'comparison':comparison,'match':same,'sha256':sha(a.read_bytes()) if a.is_file() else None})
            if not same:
                failures.append({'program':program,'scope':scope,
                                 'error':'Normal/-O outputs missing or different'})
    result={'status':'failed' if failures else 'passed',
            'scope':'Finite exact inequalities, identities and actual-word diagnostics',
            'continuum_proof_certificate':False,
            'commands_completed':len(receipts),'commands_expected':len(all_jobs),
            'commands':sorted(receipts,key=lambda x:x['tag']),
            'normal_optimized_comparisons':comparisons,'failures':failures,
            'mathematical_source':identity}
    write_json(output/'mathematical-checks.json',result)
    require(not failures, 'One or more mathematical commands or -O comparisons failed')
    return result

def typeset_checks(output, identity):
    target=output/'native'
    target.mkdir(parents=True,exist_ok=True)
    commands=[]
    for index in range(1,4):
        command=['pdflatex','-recorder','-interaction=nonstopmode','-halt-on-error',
                 '-file-line-error','-output-directory='+str(target),'main.tex']
        commands.append(run(command,'pdflatex-pass'+str(index),target,identity))
    spec = importlib.util.spec_from_file_location('typeset_manifest', ROOT/'tools/check_source_preservation.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected=set(module.tex_closure(ROOT)['reachable_tex_files'])
    actual=set()
    for line in (target/'main.fls').read_text().splitlines():
        if not line.startswith('INPUT '):
            continue
        path=Path(line[6:])
        if not path.is_absolute():
            path=ROOT/path
        try:
            relative=path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if relative.endswith('.tex') and not relative.startswith(('history/', 'build/', 'evidence/')):
            actual.add(relative)
    require(actual==expected, 'Actual compiler recorder does not equal the declared native closure')
    final=(target/'main.log').read_text(errors='replace')
    problems=[]
    for pattern, description in [
        (r'LaTeX Warning:.*undefined', 'undefined references'),
        (r'Reference .+ undefined', 'undefined reference'),
        (r'Citation .+ undefined', 'undefined citation'),
        (r'multiply defined', 'multiply defined label'),
        (r'Overfull \\[hv]box', 'overfull box'),
        (r'Missing character:', 'missing font character'),
        (r'^!', 'TeX error'),
    ]:
        found=re.findall(pattern,final,re.M)
        if found:
            problems.append({'problem':description,'matches':found})
    command=['pdfinfo',str(target/'main.pdf')]
    commands.append(run(command,'pdfinfo',target,identity))
    info=(target/'pdfinfo.log').read_text()
    match=re.search(r'^Pages:\s+(\d+)',info,re.M)
    require(match is not None,'Could not determine actual PDF page count')
    result={
        'status':'failed' if problems else 'passed',
        'scope':'Actual native TeX compilation and document diagnostics',
        'mathematical_proof_certificate':False,'pages':int(match.group(1)),
        'actual_recorder_native_tex':sorted(actual),'actual_recorder_matches_declared_closure':True,
        'commands':commands,'main_tex_sha256':sha((ROOT/'main.tex').read_bytes()),
        'pdf_sha256':sha((target/'main.pdf').read_bytes()),
        'pdf_bytes':(target/'main.pdf').stat().st_size,
        'aux_sha256':sha((target/'main.aux').read_bytes()),
        'layout_or_reference_problems':problems,
        'advisories':re.findall(r'Package amsmath Warning:[^\n]*',final),
        'mathematical_source':identity,
    }
    write_json(output/'native-typeset.json',result)
    require(not problems,'Native typesetting diagnostics failed; see native-typeset.json')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('source','math','typeset','all'))
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/current-execution/native-current')
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    require(1<=args.workers<=8,'workers must be in 1..8')
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    identity=source_identity()
    started=utc()
    results={}
    try:
        if args.phase in ('source','all'):
            results['source']=source_checks(output,identity)
        if args.phase in ('math','all'):
            results['math']=math_checks(output,identity,args.workers)
        if args.phase in ('typeset','all'):
            results['typeset']=typeset_checks(output,identity)
        require(source_identity()==identity,'Mathematical source changed during execution')
        summary={'status':'passed','phase':args.phase,'started_utc':started,
                 'finished_utc':utc(),'mathematical_source':identity,
                 'completed':sorted(results),'continuum_proof_certificate':False}
        write_json(output/('PHASE_'+args.phase+'.json'),summary)
        print(json.dumps({'status':'passed','phase':args.phase,
              'output':str(output),'mathematical_source_sha256':identity['sha256']}))
        return 0
    except Exception as exc:
        write_json(output/('PHASE_'+args.phase+'.json'),
            {'status':'failed','phase':args.phase,'started_utc':started,
             'finished_utc':utc(),'mathematical_source':identity,
             'completed':sorted(results),'error':str(exc),'traceback':traceback.format_exc()})
        print(str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
