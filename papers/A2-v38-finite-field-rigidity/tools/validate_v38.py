#!/usr/bin/env python3
"""Qualify an exact committed A2 v38 source; finite checks are not proofs."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile

PAPER = pathlib.Path(__file__).resolve().parents[1]
OUT = PAPER / 'verification' / 'current'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def run(args, cwd=PAPER):
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError('Command failed: '+repr(args)+'\n'+result.stdout[-14000:])
    return result.stdout

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-head', required=True)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {'schema':'a2-v38-qualification-1', 'status':'failed',
               'expected_head':args.expected_head, 'exact_commit_qualified':False,
               'formal_proof_certificate':False, 'physical_sensor_executed':False}
    try:
        repo = pathlib.Path(run(['git','rev-parse','--show-toplevel']).strip())
        head = run(['git','rev-parse','HEAD']).strip()
        receipt['source_commit'] = head
        require(head == args.expected_head, 'Checkout is not the expected commit')
        require(not run(['git','status','--porcelain','--untracked-files=no']).strip(),
                'Tracked worktree is dirty')
        pins = json.loads((PAPER/'SOURCE_PINS.json').read_text())
        oldrel = pins['retained_core_directory']
        require(run(['git','rev-parse','HEAD:'+oldrel]).strip() == pins['retained_core_tree'],
                'Retained core tree changed')
        require(run(['git','rev-parse','HEAD:'+pins['controlling_report_path']]).strip()
                == pins['controlling_report_blob'], 'Controlling report changed')
        old = repo/oldrel
        oldfiles = sorted(old.glob('*.tex'))
        require(len(oldfiles) == pins['retained_core_files'], 'Old core count differs')
        for p in oldfiles:
            require(p.read_bytes() == (PAPER/'core'/p.name).read_bytes(),
                    'Inherited source differs: '+p.name)
        visited = []
        def flatten(name):
            path = PAPER/name
            require(path.is_file(), 'Missing input: '+name)
            require(name not in visited, 'Repeated input: '+name)
            visited.append(name)
            text = path.read_text()
            return re.sub(r'\\input\{([^}]+)\}',
                          lambda m: flatten(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),
                          text)
        full = flatten('main.tex')
        for p in oldfiles:
            require('core/'+p.name in visited, 'Inherited core is inactive: '+p.name)
        require(all(x in visited for x in pins['new_core_inputs']), 'New input inactive')
        labels = re.findall(r'\\label\{([^}]+)\}', full)
        require(len(labels) == len(set(labels)), 'Duplicate labels')
        refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', full)
        require(not (set(refs)-set(labels)), 'Undefined source references: '+str(set(refs)-set(labels)))
        bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',full))
        cites = set()
        for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', full):
            cites.update(x.strip() for x in group.split(','))
        require(cites <= bib, 'Undefined source citations: '+str(cites-bib))
        receipt.update(retained_core_files=len(oldfiles), active_tex_files=len(visited),
                       labels=len(labels), proofs=len(re.findall(r'\\begin\{proof\}',full)))
        outputs = []
        for flags in [[],['-O']]:
            outputs.append(run([sys.executable]+flags+['tools/verify_v38.py']))
        require(outputs[0] == outputs[1], 'Ordinary and optimized diagnostics differ')
        (OUT/'finite-diagnostics.json').write_text(outputs[0])
        receipt['diagnostics'] = json.loads(outputs[0])
        inherited = 'papers/A2-v37-stationary-rigidity/tools/verify_v37.py'
        require(run(['git','rev-parse','HEAD:'+inherited]).strip()
                == '5cab78b7f6ea455b675dd4001a9ebf0d1c7dde2b',
                'Inherited diagnostic script changed')
        previous = [run([sys.executable]+flags+[str(repo/inherited)])
                    for flags in [[],['-O']]]
        require(previous[0] == previous[1], 'Inherited diagnostics differ under -O')
        (OUT/'retained-finite-diagnostics.json').write_text(previous[0])
        receipt['retained_diagnostics'] = json.loads(previous[0])
        # Source hashes and archive are taken only from the committed path list.
        rel = PAPER.relative_to(repo).as_posix()
        tracked = run(['git','ls-files','--',rel],cwd=repo).splitlines()
        hashes = {}
        for name in tracked:
            p = repo/name
            committed = subprocess.check_output(['git','show','HEAD:'+name],cwd=repo)
            require(committed == p.read_bytes(), 'Uncommitted source bytes: '+name)
            hashes[str(p.relative_to(PAPER))] = digest(p)
        (OUT/'source-sha256.json').write_text(json.dumps(hashes,indent=2,sort_keys=True)+'\n')
        with tarfile.open(OUT/'A2-v38-source.tar.gz','w:gz') as archive:
            for name in tracked:
                archive.add(repo/name,arcname='A2-v38/'+str((repo/name).relative_to(PAPER)))
        build = OUT/'build'
        build.mkdir(exist_ok=True)
        command = ['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
                   '-file-line-error','-outdir='+str(build),'main.tex']
        process = subprocess.run(command,cwd=PAPER,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (OUT/'build-output.log').write_text(process.stdout)
        require(process.returncode == 0, 'Primary build failed; see build-output.log')
        log = (build/'main.log').read_text(errors='replace')
        bad = [line for line in log.splitlines() if
               ('undefined' in line.lower() and ('reference' in line.lower() or 'citation' in line.lower()))
               or 'multiply defined' in line or 'Overfull \\hbox' in line or 'Overfull \\vbox' in line]
        (OUT/'layout-findings.json').write_text(json.dumps(bad,indent=2)+'\n')
        if bad:
            lines = log.splitlines()
            contexts = []
            for index, line in enumerate(lines):
                if line in bad:
                    contexts.append('\n'.join(lines[max(0,index-16):index+12]))
            receipt['layout_context'] = contexts
        require(not bad, 'Primary has reference or layout findings: '+repr(bad))
        shutil.copy2(build/'main.pdf',OUT/'main.pdf')
        metadata = run(['pdfinfo',str(OUT/'main.pdf')])
        (OUT/'pdfinfo.txt').write_text(metadata)
        pages = re.search(r'^Pages:\s+(\d+)',metadata,re.M)
        require(pages is not None,'PDF page count missing')
        receipt['pages'] = int(pages[1])
        receipt['status'] = 'passed'
        receipt['exact_commit_qualified'] = True
    except Exception as exc:
        receipt['error'] = str(exc)
    finally:
        (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        binding = {'source_commit':receipt.get('source_commit'),
                   'expected_head':args.expected_head,'status':receipt['status'],
                   'sha256':{p.name:digest(p) for p in sorted(OUT.iterdir())
                             if p.is_file() and p.name != 'artifact-binding.json'},
                   'formal_proof_certificate':False}
        (OUT/'artifact-binding.json').write_text(json.dumps(binding,indent=2,sort_keys=True)+'\n')
        print(json.dumps(receipt,indent=2,sort_keys=True))
    if receipt['status'] != 'passed':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
