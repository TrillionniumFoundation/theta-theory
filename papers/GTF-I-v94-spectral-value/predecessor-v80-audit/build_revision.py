#!/usr/bin/env python3
"""Build and verify source-bound v80 manuscripts and finite evidence.

Production runs use the actual committed native source. --isolated additionally
reconstructs that source ZIP and the standalone journal package in empty folders.
--verify-published is read-only: it validates a direct native-to-publication Git
chain, hashes the published objects, and rebuilds in temporary directories.
--check-source checks preservation and active inputs without compiling or running
regressions. Archived predecessor builders are historical source, not imports.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import fitz

ROOT = Path(__file__).resolve().parent
DOCS = {'quantitative.tex': 'paper.pdf', 'structural.tex': 'STRUCTURAL_PAPER.pdf',
        'main.tex': 'COMPLETE_REVISION.pdf'}
EPOCH = '1791158400'  # 5 October 2026, 00:00 UTC
WORKFLOW = '.github/workflows/gtf-i-v80-exact-head.yml'
BASE_COMMIT = '0daec5b3e20e5bf778caa90a0cf54f26c1ea53fe'
BASE_NATIVE = '4b6b43020067df10a4a21e3258c6641698b9cbc0'
BASE_ROOT = 'papers/GTF-I-v79-joint-interior-coding'
BASE_INVENTORY_SHA256 = 'fc5db99d57c4ba72506068dd684fa5c0e0bd3620da9a9215e1efa3404cd45ac2'
BASE_LABEL_COUNTS = {'main.tex': 759, 'quantitative.tex': 260, 'structural.tex': 116}
STRUCTURAL_SIGNATURE_SHA256 = 'd323ba82482bf7ec71ac8256f3a28f7453f28bbecd8c66d0407471f89337b0e2'
NEW_SECTIONS = ('sections/62-confidence-optimal-learning.tex',
                'sections/63-effective-optimal-learning.tex')
NEW_LABELS = ('lem:diagonalconfidence80', 'lem:binaryconfidenceupper80',
              'thm:interiorconfidence80', 'cor:operatorconfidence80',
              'cor:interiorconfidencecode80', 'lem:algebraicreadout80',
              'thm:effectiveinterior80')
REGRESSION_SCRIPTS = (
    'check_matrix_geometry.py', 'matrix_codec_check.py', 'check_common_learning.py',
    'check_biased_geometry.py', 'check_coupled_geometry.py', 'check_noisy_readout.py',
    'check_readout.py', 'check_conditional.py', 'check_coherent.py',
    'check_preparation.py', 'check_codec.py', 'check_choi.py',
    'check_instruments.py', 'check_streaming.py', 'inherited_check_v63.py',
    'block_resource_check.py', 'interior_codec_check.py', 'confidence_readout_check.py')
SCRIPTS = REGRESSION_SCRIPTS
JOURNAL_ENTRIES = ('quantitative.tex', 'structural.tex')
JOURNAL_EXTRAS = ('paper.pdf', 'STRUCTURAL_PAPER.pdf', 'RESPONSE_TO_REFEREE.md',
                  'LITERATURE_AUDIT.md', 'INDEPENDENT_REVIEW_BRIEF.md',
                  'JOURNAL_README.md', 'journal_verify.py')
RESEARCH_EVIDENCE = ('BUILD_RECEIPT.json', 'SOURCE_HASHES.json', 'PAGE_CHECKS.json',
                     'THEOREM_LOCATIONS.json', 'REGRESSION_RESULTS.json')
PACKAGES = ('NATIVE_SOURCE.zip', 'JOURNAL_PACKAGE.zip', 'RESEARCH_PACKAGE.zip')
BIBLIOGRAPHIES = ('editions/coding-bibliography.tex', 'sections/44-bibliography-v70.tex')
REPORT_IDENTITIES = {
    'external': ('96a3666ed516ea12fcdb8ede341b7082e4ff2c78',
                 '12b14374e33fc698a233b14b9735fd6f43db3df1',
                 'be4b4f4ec9fe2332cf11f3bc842e63df1527ed49a56a1ec6af7575ed35c1caa2'),
    'pipeline': ('d01b5b4d48955e8c6f0c5592213b8628e12a66dd',
                 'bb9948c12d89a476f5106f504dce745618d8952f',
                 '301315df3fc5ea3d0a0369a338565fc13de77523620149f6e820e41e7f541713')}

def sha(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()


def put(path:Path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def require(ok:bool,message:str):
    if not ok:raise RuntimeError(message)


def safe_relative(name:str)->Path:
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and name==p.as_posix(),
            'unsafe or noncanonical relative path '+name)
    return p


def git_blob(data:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def sources(root:Path)->dict[str,str]:
    out={}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if not p.is_file() or any(x in {'build','evidence','__pycache__','.git'} for x in rel.parts):continue
        if p.suffix.lower() in {'.tex','.py','.json','.md','.txt'}:out[str(rel)]=sha(p.read_bytes())
    return out


def pdf_signature(path:Path):
    pages=[]
    with fitz.open(path) as d:
        for p in d:
            text=p.get_text(sort=True)
            pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
            # Detect actual geometric clipping, not normal right-margin math indentation.
            for block in p.get_text('blocks'):
                x0,y0,x1,y1=block[:4]
                require(x0>=-1 and y0>=-1 and x1<=p.rect.width+1 and y1<=p.rect.height+1,
                        f'clipped block in {path.name} page {p.number+1}')
            pages.append({'page':p.number+1,'text_sha256':sha(text.encode()),'raster_sha256':sha(pix.samples),
                          'width':pix.width,'height':pix.height,'characters':len(text)})
    return {'pages':len(pages),'page_checks':pages}


def run_checks(root:Path, evidence:Path):
    result={}
    for script in REGRESSION_SCRIPTS:
        print('exact regression: '+script, file=sys.stderr, flush=True)
        expected_status='pass' if script=='matrix_codec_check.py' else 'success'
        outputs=[]
        for opt in [False,True]:
            cmd=[sys.executable]+(['-O'] if opt else [])+[str(root/script)]
            p=subprocess.run(cmd,cwd=root,capture_output=True,check=True,timeout=180)
            obj=json.loads(p.stdout)
            require(obj['status']==expected_status,script+' did not report '+expected_status)
            outputs.append(obj)
        require(outputs[0]==outputs[1],script+' changes under optimization')
        result[script]=outputs[0]
    # This is a completed scalar codebook and exact supplied-source example.
    # Higher-dimensional prefix audits remain explicitly finite in the regression.
    scalar_source=root/'examples/matrix-codec-scalar-source.json'
    require(scalar_source.is_file(),'missing complete scalar codec example')
    scalar_raw=json.loads(scalar_source.read_text())
    require(scalar_raw['schema']=='gtf77.matrix-effect/1' and scalar_raw['dimension']==1,
            'the completed codec example must have scalar input dimension')
    scalar_code=evidence/'MATRIX_CODEC_SCALAR_CODE.json'
    encoded=subprocess.run([sys.executable,str(root/'matrix_codec.py'),'encode',
        '--input',str(scalar_source),'--horizon','1','--accuracy','1/2'],
        cwd=root,capture_output=True,check=True,timeout=180)
    scalar_code.write_bytes(encoded.stdout)
    decoded=subprocess.run([sys.executable,str(root/'matrix_codec.py'),'decode',
        '--input',str(scalar_code)],cwd=root,capture_output=True,check=True,timeout=180)
    (evidence/'MATRIX_CODEC_SCALAR_DECODED.json').write_bytes(decoded.stdout)
    summary=subprocess.run([sys.executable,str(root/'matrix_codec.py'),'summary',
        '--dimension','1','--horizon','1','--accuracy','1/2'],
        cwd=root,capture_output=True,check=True,timeout=180)
    (evidence/'MATRIX_CODEC_SCALAR_SUMMARY.json').write_bytes(summary.stdout)
    code_data=json.loads(encoded.stdout)
    decoded_data=json.loads(decoded.stdout)
    summary_data=json.loads(summary.stdout)
    require(code_data['schema']=='gtf77.matrix-effect-code/1'
            and code_data['dimension']==1 and code_data['horizon']==1
            and code_data['accuracy']=='1/2','scalar code public parameters changed')
    require(decoded_data['schema']=='gtf77.matrix-effect/1'
            and decoded_data['dimension']==1,'scalar decoder returned the wrong interface')
    require(summary_data['schema']=='gtf77.matrix-effect-codebook-summary/1'
            and summary_data['complete'] is True
            and summary_data['dimension']==1 and summary_data['horizon']==1
            and summary_data['accuracy']=='1/2','scalar codebook was not completely reconstructed')
    require(len(code_data['payload'])==summary_data['payload_bits'],
            'scalar example has the wrong fixed payload length')
    require(scalar_raw['effect'][0][0][1]=='0'
            and decoded_data['effect'][0][0][1]=='0','scalar effect must be real')
    source_probability=Fraction(scalar_raw['effect'][0][0][0])
    decoded_probability=Fraction(decoded_data['effect'][0][0][0])
    require(0<=source_probability<=1 and 0<=decoded_probability<=1,
            'scalar source or decoded effect is illegal')
    scalar_error=2*abs(source_probability-decoded_probability)
    require(scalar_error<=Fraction(11,32),'scalar exact one-use error exceeds the codec bound')
    put(evidence/'MATRIX_CODEC_SCALAR_EXAMPLE.json',{
        'schema':'gtf80.matrix-effect-codec-example/1','status':'success',
        'inherited_codec_schema_revision':77,
        'source_file':str(scalar_source.relative_to(root)),
        'source_sha256':sha(scalar_source.read_bytes()),
        'dimension':1,'horizon':1,'accuracy':'1/2',
        'complete_dictionary_executed':True,
        'payload_bits':summary_data['payload_bits'],
        'exact_unhalved_operational_error':str(scalar_error),
        'source_is_unknown_device':False,'unknown_device_learning_executed':False,
        'scope':'Complete scalar supplied-matrix encode/decode and exact Bernoulli error; '
                'no higher-dimensional complete dictionary or physical learner run.'})
    codec=subprocess.run([sys.executable,str(root/'instrument_codec.py'),'encode','--input',str(root/'inputs/rectangular-choi.json'),'--grid','4096'],capture_output=True,check=True,timeout=30)
    (evidence/'INTRINSIC_CODE.json').write_bytes(codec.stdout)
    adaptive=subprocess.run([sys.executable,str(root/'instrument_codec.py'),'adaptive','--input',str(root/'inputs/interior-codec.json'),'--horizon','100','--margin','1/8','--error','1/4'],capture_output=True,check=True,timeout=30)
    (evidence/'ADAPTIVE_CODE.json').write_bytes(adaptive.stdout)
    prep=subprocess.run([sys.executable,str(root/'preparation_codec.py'),'adaptive','--input',str(root/'inputs/preparation-boundary.json'),'--horizon','1000','--error','1/1000','--ranks','[2,1,0]'],capture_output=True,check=True,timeout=30)
    (evidence/'PREPARATION_CODE.json').write_bytes(prep.stdout)
    prepared=subprocess.run([sys.executable,str(root/'preparation_codec.py'),'decode','--input',str(evidence/'PREPARATION_CODE.json')],capture_output=True,check=True,timeout=30)
    (evidence/'PREPARATION_DECODED.json').write_bytes(prepared.stdout)
    checked=subprocess.run([sys.executable,str(root/'preparation_codec.py'),'verify','--input',str(root/'inputs/preparation-boundary.json'),'--certificate',str(evidence/'PREPARATION_CODE.json')],capture_output=True,check=True,timeout=30)
    (evidence/'PREPARATION_VERIFIED.json').write_bytes(checked.stdout)
    coherent=subprocess.run([sys.executable,str(root/'coherent_codec.py'),'encode','--input',str(root/'inputs/preparation-boundary.json'),'--quaternion','["1/2","1/2","1/2","1/2"]','--horizon','100','--error','1/1000','--ranks','[2,1,0]'],capture_output=True,check=True,timeout=60)
    (evidence/'COHERENT_CODE.json').write_bytes(coherent.stdout)
    decoded=subprocess.run([sys.executable,str(root/'coherent_codec.py'),'decode','--input',str(evidence/'COHERENT_CODE.json')],capture_output=True,check=True,timeout=60)
    (evidence/'COHERENT_DECODED.json').write_bytes(decoded.stdout)
    verified=subprocess.run([sys.executable,str(root/'coherent_codec.py'),'verify','--input',str(root/'inputs/preparation-boundary.json'),'--quaternion','["1/2","1/2","1/2","1/2"]','--certificate',str(evidence/'COHERENT_CODE.json')],capture_output=True,check=True,timeout=60)
    (evidence/'COHERENT_VERIFIED.json').write_bytes(verified.stdout)
    retracted=subprocess.run([sys.executable,str(root/'coherent_codec.py'),'retract','--input',str(evidence/'COHERENT_DECODED.json')],capture_output=True,check=True,timeout=60)
    (evidence/'RETRACTED_CENTRE.json').write_bytes(retracted.stdout)
    conditional=subprocess.run([sys.executable,str(root/'conditional_codec.py'),'encode','--input',str(root/'inputs/conditional-boundary.json'),'--horizon','100','--error','1/1000','--ranks','[[1,1,0],[0,1,2]]'],capture_output=True,check=True,timeout=60)
    (evidence/'CONDITIONAL_CODE.json').write_bytes(conditional.stdout)
    for action,out in [('decode','CONDITIONAL_DECODED.json'),('verify','CONDITIONAL_VERIFIED.json')]:
        cmd=[sys.executable,str(root/'conditional_codec.py'),action,'--input',str(evidence/'CONDITIONAL_CODE.json')]
        if action=='verify':cmd=[sys.executable,str(root/'conditional_codec.py'),action,'--input',str(root/'inputs/conditional-boundary.json'),'--certificate',str(evidence/'CONDITIONAL_CODE.json')]
        rr=subprocess.run(cmd,capture_output=True,check=True,timeout=60)
        (evidence/out).write_bytes(rr.stdout)
    for name,ranks in [('qubit',[[1,0],[0,1]]),('qutrit',[[1,0],[0,1],[1,0]])]:
        target=root/('inputs/varying-readout-'+name+'.json')
        path=evidence/('READOUT_'+name.upper()+'_CODE.json')
        cmd=[sys.executable,str(root/'readout_codec.py'),'encode','--input',str(target),
             '--horizon','12','--error','1/100','--ranks',json.dumps(ranks)]
        p=subprocess.run(cmd,capture_output=True,check=True,timeout=60);path.write_bytes(p.stdout)
        for action in ['decode','verify']:
            cmd=[sys.executable,str(root/'readout_codec.py'),action,'--input',str(path)]
            if action=='verify':cmd=[sys.executable,str(root/'readout_codec.py'),action,'--input',str(target),'--certificate',str(path)]
            out=subprocess.run(cmd,capture_output=True,check=True,timeout=60)
            (evidence/('READOUT_'+name.upper()+'_'+action.upper()+'.json')).write_bytes(out.stdout)
    for name,ranks in [('readout',None),('conditional',[1,3])]:
        target=root/('inputs/noisy-'+name+'.json')
        path=evidence/('NOISY_'+name.upper()+'_CODE.json')
        cmd=[sys.executable,str(root/'noisy_readout_codec.py'),'encode','--input',str(target),
             '--horizon','257','--error','1/1024']
        if ranks is not None: cmd+=['--ranks',json.dumps(ranks)]
        p=subprocess.run(cmd,capture_output=True,check=True,timeout=60);path.write_bytes(p.stdout)
        for action in ['decode','verify']:
            cmd=[sys.executable,str(root/'noisy_readout_codec.py'),action,'--input',str(path)]
            if action=='verify':cmd=[sys.executable,str(root/'noisy_readout_codec.py'),action,'--input',str(target),'--certificate',str(path)]
            out=subprocess.run(cmd,capture_output=True,check=True,timeout=60)
            (evidence/('NOISY_'+name.upper()+'_'+action.upper()+'.json')).write_bytes(out.stdout)
    for d in [2,3]:
        target=root/('inputs/coupled-ball-'+str(d)+'.json')
        path=evidence/('COUPLED_'+str(d)+'_CODE.json')
        p=subprocess.run([sys.executable,str(root/'coupled_codec.py'),'encode','--input',str(target),
                          '--horizon','7','--error','1/128'],capture_output=True,check=True,timeout=60)
        path.write_bytes(p.stdout)
        for action in ['decode','verify']:
            cmd=[sys.executable,str(root/'coupled_codec.py'),action,'--input',str(path)]
            if action=='verify':cmd=[sys.executable,str(root/'coupled_codec.py'),action,'--input',str(target),'--certificate',str(path)]
            p=subprocess.run(cmd,capture_output=True,check=True,timeout=60)
            (evidence/('COUPLED_'+str(d)+'_'+action.upper()+'.json')).write_bytes(p.stdout)
    for name in ['measurement-2','measurement-3','boundary','coin']:
        target=root/('inputs/biased-'+name+'.json')
        require(target.is_file(), 'missing biased example '+name)
        code=evidence/('BIASED_'+name.upper().replace('-','_')+'_CODE.json')
        p=subprocess.run([sys.executable,str(root/'biased_codec.py'),'encode','--input',str(target),
            '--horizon','1','--error','1/4'],capture_output=True,check=True,timeout=180)
        code.write_bytes(p.stdout)
        for action in ['decode','verify']:
            cmd=[sys.executable,str(root/'biased_codec.py'),action,'--input',str(code)]
            if action=='verify':cmd=[sys.executable,str(root/'biased_codec.py'),action,'--input',str(target),'--certificate',str(code)]
            p=subprocess.run(cmd,capture_output=True,check=True,timeout=180)
            (evidence/('BIASED_'+name.upper().replace('-','_')+'_'+action.upper()+'.json')).write_bytes(p.stdout)
    for d in [1,2,3,4]:
        target=root/('inputs/matrix-effect-'+str(d)+'.json')
        certificate=evidence/('MATRIX_'+str(d)+'_BOUND.json')
        p=subprocess.run([sys.executable,str(root/'matrix_metric.py'),'compute','--input',str(target),
                          '--horizon','7'],capture_output=True,check=True,timeout=60)
        certificate.write_bytes(p.stdout)
        p=subprocess.run([sys.executable,str(root/'matrix_metric.py'),'verify','--input',str(target),
                          '--certificate',str(certificate),'--horizon','7'],capture_output=True,check=True,timeout=60)
        (evidence/('MATRIX_'+str(d)+'_VERIFIED.json')).write_bytes(p.stdout)
    put(evidence/'REGRESSION_RESULTS.json',result)
    compiled=subprocess.run([sys.executable,str(root/'choi_streaming.py'),'compile','--input',
        str(root/'inputs/rectangular-choi.json'),'--grid','4096'],capture_output=True,check=True,timeout=30)
    (evidence/'CHOI_COMPILATION.json').write_bytes(compiled.stdout)
    channel=subprocess.run([sys.executable,str(root/'choi_streaming.py'),'stream','--input',
        str(root/'inputs/choi-channel-stream.json')],input=b'8\n2\nxxxxxxxx\n',capture_output=True,check=True,timeout=30)
    (evidence/'CHOI_STREAM.jsonl').write_bytes(channel.stdout)
    payload=b'32\n2\n'+b'xyXZ'*8+b'\n'
    cli=subprocess.run([sys.executable,str(root/'streaming.py')],input=payload,capture_output=True,check=True,timeout=30)
    (evidence/'STREAMING_EXAMPLE.json').write_bytes(cli.stdout)
    instrument=subprocess.run(
        [sys.executable,str(root/'instrument_streaming.py')],
        input=b'32\n2\n'+b'uvdi'*8+b'\n',cwd=root,capture_output=True,check=True,timeout=30)
    (evidence/'INSTRUMENT_EXAMPLE.jsonl').write_bytes(instrument.stdout)
    cert=subprocess.run([sys.executable,str(root/'accuracy_profile.py'),'--horizon','100','--width','10',
                         '--error','1/931322574615478515625','--block-length','10','--terms','8'],
                        cwd=root,capture_output=True,check=True,timeout=30)
    (evidence/'ACCURACY_EXAMPLE.json').write_bytes(cert.stdout)
    return result


def git_output(root:Path,*args:str)->str:
    return subprocess.run(['git',*args],cwd=root,capture_output=True,text=True,
                          check=True,timeout=120).stdout.strip()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True)+'\n').encode()


def graph_reader(read_text, entry: str, seen=None):
    """Use the same explicit input graph for current and retained original TeX."""
    if seen is None:
        seen = set()
    entry = safe_relative(str(Path(entry).with_suffix('.tex'))).as_posix()
    require(entry not in seen, 'duplicate or recursive TeX input: '+entry)
    seen.add(entry)
    text = read_text(entry)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    for sub in re.findall(r'\\input\{([^}]+)\}', text):
        labels += graph_reader(read_text, sub, seen)[1]
    return seen, labels


def graph(root: Path, entry: str):
    return graph_reader(lambda n: (root/safe_relative(n)).read_text(), entry)


def bibliography_entries(text: str):
    matches = list(re.finditer(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text))
    require(matches and '\\end{thebibliography}' in text, 'malformed bibliography')
    entries = {}
    for i, match in enumerate(matches):
        key = match.group(1)
        require(key not in entries, 'duplicate bibliography key: '+key)
        end = matches[i+1].start() if i+1 < len(matches) else text.index('\\end{thebibliography}')
        entries[key] = text[match.start():end].strip()
    return entries


def check_source(root: Path):
    """Reconstruct v79 preservation from retained bytes, independently of claims."""
    inv = sources(root)
    p = json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    require(p['schema'] == 'gtf80.preservation/1', 'v80 preservation manifest required')
    require(p['base_commit'] == BASE_COMMIT and p['native_source_commit'] == BASE_NATIVE
            and p['source_root'] == BASE_ROOT, 'the immediate source baseline must be v79')
    require(len(p['files']) == 383 and p['source_inventory_sha256'] == BASE_INVENTORY_SHA256
            and sha(json_bytes(p['files'])) == BASE_INVENTORY_SHA256,
            'the exact 383-file v79 native inventory is required')
    require(not p.get('focused_relocations'), 'v80 does not relocate inherited focused labels')
    archived = p['archived_originals']
    require(set(archived) <= set(p['files']), 'archive mapping invents a predecessor file')
    changed = []
    for name, digest in p['files'].items():
        current = root/safe_relative(name)
        require(current.is_file(), 'predecessor native path removed: '+name)
        if sha(current.read_bytes()) != digest:
            require(name in archived, 'changed predecessor lacks an archived original: '+name)
            changed.append(name)
    for name, archive in archived.items():
        require(archive == 'predecessor-v79-audit/'+name,
                'original must be retained at its exact v79 archive path: '+name)
        path = root/safe_relative(archive)
        require(path.is_file() and sha(path.read_bytes()) == p['files'][name],
                'archived v79 bytes differ: '+name)

    def original(name):
        require(name in p['files'], 'prior graph invents a native file: '+name)
        path = archived[name] if name in changed else name
        data = (root/safe_relative(path)).read_bytes()
        require(sha(data) == p['files'][name], 'retained predecessor mismatch: '+name)
        return data

    require(set(p['prior_proof_graphs']) == set(DOCS), 'prior document set differs')
    prior_graphs = {}
    graphs = {}
    for entry in DOCS:
        old_files, old_labels = graph_reader(lambda n: original(n).decode(), entry)
        require(len(old_labels) == len(set(old_labels)) == BASE_LABEL_COUNTS[entry],
                'v79 label inventory differs: '+entry)
        prior_graphs[entry] = {'files': sorted(old_files), 'labels': old_labels}
        require(p['prior_proof_graphs'][entry] == prior_graphs[entry],
                'declared predecessor graph differs from retained original TeX: '+entry)
        active, labels = graph(root, entry)
        require(len(labels) == len(set(labels)), 'duplicate active label: '+entry)
        require(set(old_labels) <= set(labels), 'predecessor active label removed: '+entry)
        graphs[entry] = {'files': sorted(active), 'labels': labels}
    require(p['prior_labels'] == prior_graphs['main.tex']['labels'],
            'complete predecessor labels differ from the original graph')
    proof = json.loads((root/'PROOF_TEXT_PRESERVATION.json').read_text())
    require(proof['schema'] == 'gtf80.proof-text-preservation/1'
            and proof['predecessor'] == BASE_COMMIT, 'proof preservation identity differs')
    require(not proof['removed_proof_sections'] and not proof['reviewed_additive_changes'],
            'inherited mathematical proof sections must remain byte-identical')
    prior_sections = {n for n in p['files'] if n.startswith('sections/') and n.endswith('.tex')}
    required_sections = prior_sections - {'sections/44-bibliography-v70.tex'}
    require(len(prior_sections) == 62 and len(proof['byte_identical_sections']) == len(required_sections)
            and set(proof['byte_identical_sections']) == required_sections,
            'the unchanged inherited section inventory is incomplete')
    for name in required_sections:
        require(inv.get(name) == p['files'][name], 'inherited section text changed: '+name)
        for entry in DOCS:
            if name in prior_graphs[entry]['files']:
                require(name in graphs[entry]['files'], 'inherited active section removed: '+entry+': '+name)
    for name in BIBLIOGRAPHIES:
        before = bibliography_entries(original(name).decode())
        after = bibliography_entries((root/name).read_text())
        require(all(after.get(key) == text for key, text in before.items()),
                'an inherited bibliography entry changed or disappeared: '+name)
    require(graphs['structural.tex'] == prior_graphs['structural.tex']
            and all(inv[n] == p['files'][n] for n in graphs['structural.tex']['files']),
            'the independent structural companion must remain unchanged')
    structural = p['structural_companion']
    require(structural['pages'] == 41
            and structural['page_checks_sha256'] == STRUCTURAL_SIGNATURE_SHA256,
            'structural companion page baseline differs')
    require(len(proof['new_sections']) == len(NEW_SECTIONS)
            and set(proof['new_sections']) == set(NEW_SECTIONS), 'new section inventory differs')
    new_labels = []
    for name in NEW_SECTIONS:
        require(all(name in graphs[entry]['files'] for entry in ('main.tex', 'quantitative.tex')),
                'new section absent from complete or focused article: '+name)
        labels = re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}', (root/name).read_text())
        require(labels and all(label.endswith('80') for label in labels),
                'new theorem labels must identify revision 80: '+name)
        new_labels += labels
    require(len(new_labels) == len(set(new_labels)) and set(new_labels) == set(NEW_LABELS),
            'new theorem set differs from the seven specified results')
    controls = json.loads((root/'CONTROLLING_REPORTS.json').read_text())
    require(controls['revision'] == 80 and controls['review_round'] == 51
            and controls['source_baseline_head'] == BASE_COMMIT
            and controls['source_baseline_native'] == BASE_NATIVE, 'wrong current source baseline')
    require(controls['reviewed_head'] == '5650842e0bc89ca6a8b6d6730115784f0d9ecc12'
            and controls['reviewed_native_source'] == '91df620ec7b6e02a6f0fe1c7798639c2626c742b',
            'R51 reviewed v77, not the later v79 or v80 objects')
    require(len(controls['reports']) == 2
            and {r['kind'] for r in controls['reports']} == set(REPORT_IDENTITIES),
            'both controlling R51 reports are required')
    for report in controls['reports']:
        require((report['commit'], report['git_blob'], report['sha256']) == REPORT_IDENTITIES[report['kind']],
                'controlling report identity differs: '+report['kind'])
        data = (root/safe_relative(report['frozen'])).read_bytes()
        require(sha(data) == report['sha256'] and git_blob(data) == report['git_blob'],
                'frozen R51 report bytes differ: '+report['kind'])
    status = json.loads((root/'PROOF_STATUS.json').read_text())
    require(status['analytic_pipeline_closure']
            and all(v is False for v in status['analytic_pipeline_closure'].values()),
            'finite evidence cannot promote independent analytic pipeline flags')
    require(all(name in inv for name in SCRIPTS), 'missing registered finite regression')
    require(all(name in inv or name in DOCS.values() for name in JOURNAL_EXTRAS),
            'missing standalone journal source or instructions')
    return {'schema': 'gtf80.source-check/1', 'status': 'success', 'source_files': len(inv),
            'base_commit': BASE_COMMIT, 'predecessor_native_files': len(p['files']),
            'preserved_complete_labels': BASE_LABEL_COUNTS['main.tex'],
            'preserved_active_labels': BASE_LABEL_COUNTS,
            'changed_predecessor_files': sorted(changed),
            'byte_identical_sections': len(required_sections),
            'byte_identical_active_section_files': len(required_sections & set(prior_graphs['main.tex']['files'])),
            'regression_suites': len(SCRIPTS), 'new_theorems': list(NEW_LABELS),
            'structural_companion_unchanged': True,
            'historical_evidence_reused_as_current_qualification': False,
            'documents': {e: {'active_files': len(g['files']), 'active_labels': len(g['labels'])}
                          for e, g in graphs.items()}, 'graphs': graphs}, inv


def committed_source(root: Path, source: str, inv):
    require(re.fullmatch(r'[0-9a-f]{40}', source) is not None, 'full source commit SHA required')
    repo = Path(git_output(root, 'rev-parse', '--show-toplevel'))
    prefix = root.relative_to(repo).as_posix()+'/'
    raw = subprocess.run(['git', 'ls-tree', '-r', '-z', source, '--', prefix],
                         cwd=repo, capture_output=True, check=True, timeout=120).stdout
    blobs = {}
    for item in raw.split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            mode, kind, digest = meta.decode().split()
            require(kind == 'blob' and mode in {'100644', '100755'}, 'nonregular native Git object')
            blobs[name.decode()] = digest
    expected = {prefix+n: git_blob((root/safe_relative(n)).read_bytes()) for n in inv}
    require(blobs == expected, 'native commit must contain exactly the native source inventory')
    require(sources(root) == inv, 'native source bytes changed')
    require(git_output(repo, 'rev-parse', source+':'+WORKFLOW)
            == git_blob((repo/WORKFLOW).read_bytes()), 'workflow differs from the native source object')
    return repo


def make_zip(path: Path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            safe_relative(name)
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 5, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def archive_names(archive):
    names = archive.namelist()
    require(len(names) == len(set(names)), 'archive contains duplicate entries')
    for name in names:
        safe_relative(name)
        require(not name.endswith('/'), 'archive must contain regular files only')
    return set(names)


def journal_names(root: Path):
    names = set(JOURNAL_EXTRAS)
    for entry in JOURNAL_ENTRIES:
        names.update(graph(root, entry)[0])
    return names


def diagnostics(log: str, entry: str):
    for text in ['There were undefined references', 'There were undefined citations',
                 'multiply defined', 'Undefined control sequence', 'Rerun to get cross-references right']:
        require(text not in log, 'unresolved LaTeX diagnostic '+entry+': '+text)
    boxes = re.findall(r'(?:Overfull|Underfull) \\[^\n]+', log)
    require(not boxes, 'typesetting boxes '+entry+': '+repr(boxes))
    return {'unresolved_references_or_citations': False, 'boxes': boxes,
            'raw_engine_warnings': [line for line in log.splitlines() if 'warning' in line.lower()]}


def verify_journal(root: Path, source: str):
    with tempfile.TemporaryDirectory(prefix='gtf80-journal-') as directory:
        temp = Path(directory)
        with zipfile.ZipFile(root/'evidence/JOURNAL_PACKAGE.zip') as archive:
            archive_names(archive)
            archive.extractall(temp)
        run = subprocess.run([sys.executable, str(temp/'journal_verify.py')], cwd=temp,
                             capture_output=True, check=True, timeout=900)
        result = json.loads(run.stdout)
        require(result['schema'] == 'gtf80.journal-rebuild/1' and result['status'] == 'success'
                and result['source_commit'] == source and result['read_only'] is True,
                'standalone journal reconstruction identity differs')
        return result


def build(root: Path, *, isolated: bool = False, source_commit=None, reconstruction: bool = False):
    checked, inv = check_source(root)
    if reconstruction:
        require(re.fullmatch(r'[0-9a-f]{40}', source_commit or '') is not None,
                'temporary reconstruction needs its original source identity')
        require(not isolated, 'a reconstruction must not recursively qualify itself')
        source = source_commit
        source_tree = None
    else:
        require(source_commit is None, 'production cannot assert an alternate source commit')
        source = git_output(root, 'rev-parse', 'HEAD')
        committed_source(root, source, inv)
        source_tree = git_output(root, 'rev-parse', source+'^{tree}')
    evidence, bdir = root/'evidence', root/'build'
    evidence.mkdir(exist_ok=True)
    bdir.mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE='1', TZ='UTC')
    docs, locations, latex = {}, {}, {}
    for entry, pdf in DOCS.items():
        print('typeset three passes: '+entry, file=sys.stderr, flush=True)
        for _ in range(3):
            run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                  '-file-line-error', '-output-directory='+str(bdir), entry],
                                 cwd=root, env=env, capture_output=True, timeout=180)
            require(run.returncode == 0, run.stdout.decode(errors='replace')[-7000:])
        stem = Path(entry).stem
        log = (bdir/(stem+'.log')).read_text(errors='replace')
        latex[entry] = diagnostics(log, entry)
        (evidence/(stem.upper()+'_LATEX_LOG.txt')).write_text(log)
        shutil.copy2(bdir/(stem+'.pdf'), root/pdf)
        docs[pdf] = {**pdf_signature(root/pdf), 'sha256': sha((root/pdf).read_bytes())}
        aux = (bdir/(stem+'.aux')).read_text()
        locations[entry] = {m[0]: {'number': m[1], 'page': m[2]} for m in
                           re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}', aux)}
        require(set(checked['graphs'][entry]['labels']) <= set(locations[entry]),
                'an active label was not compiled: '+entry)
    require(docs['STRUCTURAL_PAPER.pdf']['pages'] == 41
            and sha(json_bytes(docs['STRUCTURAL_PAPER.pdf']['page_checks'])) == STRUCTURAL_SIGNATURE_SHA256,
            'unchanged structural companion text or raster signature differs from v79')
    # A fresh output directory distinguishes files actually produced by this
    # execution from editorial evidence or stale files already in evidence/.
    with tempfile.TemporaryDirectory(prefix='gtf80-finite-output-', dir=bdir) as directory:
        finite_output = Path(directory)
        regression = run_checks(root, finite_output)
        finite_evidence = {}
        for path in sorted(finite_output.rglob('*')):
            if path.is_file():
                name = path.relative_to(finite_output).as_posix()
                safe_relative(name)
                finite_evidence[name] = sha(path.read_bytes())
                (evidence/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, evidence/name)
        require('REGRESSION_RESULTS.json' in finite_evidence,
                'finite execution did not produce its regression receipt')
    put(evidence/'SOURCE_HASHES.json', inv)
    put(evidence/'PAGE_CHECKS.json', docs)
    put(evidence/'THEOREM_LOCATIONS.json', locations)
    require(sources(root) == inv, 'build modified native sources')
    native = {n: (root/n).read_bytes() for n in inv}
    make_zip(evidence/'NATIVE_SOURCE.zip', native)
    receipt = {'schema': 'gtf80.build/1', 'status': 'success', 'source_commit': source,
               'source_git_tree': source_tree, 'source_date_epoch': int(EPOCH),
               'qualified_git_source': not reconstruction,
               'temporary_reconstruction': reconstruction,
               'base_commit': BASE_COMMIT, 'source_files': len(inv),
               'source_inventory_sha256': sha((evidence/'SOURCE_HASHES.json').read_bytes()),
               'native_source_sha256': sha((evidence/'NATIVE_SOURCE.zip').read_bytes()),
               'source_check': {k: v for k, v in checked.items() if k != 'graphs'},
               'documents': {n: {'pages': v['pages'], 'sha256': v['sha256']} for n, v in docs.items()},
               'latex_diagnostics': latex, 'regression': regression,
               'finite_evidence_sha256': finite_evidence,
               'normal_optimized_identical': True, 'isolated_native_rebuild': False,
               'standalone_journal_rebuild': False,
               'historical_evidence_reused_as_current_qualification': False,
               'scope': 'Native identity, finite exact tests and page reconstruction; no executed full '
                        'quantifier-elimination learner, independent proof certification or priority certification.',
               'tools': {'python': sys.version.split()[0], 'pymupdf': fitz.VersionBind,
                         'pdflatex': subprocess.run(['pdflatex', '--version'], capture_output=True,
                                                   text=True, check=True).stdout.splitlines()[0]}}
    journal = {n: (root/n).read_bytes() for n in journal_names(root)}
    manifest = {'schema': 'gtf80.journal/1', 'source_commit': source,
                'source_date_epoch': int(EPOCH),
                'files': {n: sha(data) for n, data in journal.items()},
                'documents': {DOCS[e]: docs[DOCS[e]] for e in JOURNAL_ENTRIES},
                'historical_PDF_dependencies': False, 'repository_dependencies': False}
    journal['JOURNAL_MANIFEST.json'] = json_bytes(manifest)
    make_zip(evidence/'JOURNAL_PACKAGE.zip', journal)
    if isolated:
        print('isolated native-source reconstruction', file=sys.stderr, flush=True)
        with tempfile.TemporaryDirectory(prefix='gtf80-native-') as directory:
            temp = Path(directory)
            with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as archive:
                archive_names(archive)
                archive.extractall(temp)
            rebuilt = build(temp, source_commit=source, reconstruction=True)
            other = json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
            for name in docs:
                require(docs[name]['page_checks'] == other[name]['page_checks'],
                        'isolated page signatures differ: '+name)
            require(rebuilt['regression'] == regression, 'isolated finite regressions differ')
            require(rebuilt['finite_evidence_sha256'] == finite_evidence,
                    'isolated auxiliary finite-evidence inventory or bytes differ')
            require((temp/'evidence/THEOREM_LOCATIONS.json').read_bytes()
                    == (evidence/'THEOREM_LOCATIONS.json').read_bytes(), 'isolated theorem locations differ')
            require(sources(temp) == inv, 'isolated native sources differ')
        receipt['isolated_native_rebuild'] = True
        print('standalone focused and structural journal reconstruction', file=sys.stderr, flush=True)
        journal_receipt = verify_journal(root, source)
        require(journal_receipt['documents'] == {DOCS[e]: receipt['documents'][DOCS[e]] for e in JOURNAL_ENTRIES},
                'standalone reconstructed document inventory differs')
        put(evidence/'JOURNAL_REBUILD.json', journal_receipt)
        receipt['standalone_journal_rebuild'] = True
    require(sources(root) == inv, 'qualification modified native sources')
    put(evidence/'BUILD_RECEIPT.json', receipt)
    research = {**native, **{n: (root/n).read_bytes() for n in DOCS.values()}}
    for name in RESEARCH_EVIDENCE:
        research['evidence/'+name] = (evidence/name).read_bytes()
    make_zip(evidence/'RESEARCH_PACKAGE.zip', research)
    put(evidence/'PACKAGE_MANIFEST.json', {'schema': 'gtf80.packages/1', 'source_commit': source,
         'packages': {n: sha((evidence/n).read_bytes()) for n in PACKAGES},
         'documents': receipt['documents']})
    return receipt


def verify_artifacts(root: Path):
    """Validate all published packages and evidence without running another build."""
    checked, inv = check_source(root)
    ev = root/'evidence'
    receipt = json.loads((ev/'BUILD_RECEIPT.json').read_text())
    require(receipt['schema'] == 'gtf80.build/1' and receipt['status'] == 'success'
            and receipt['qualified_git_source'] is True
            and receipt['temporary_reconstruction'] is False
            and receipt['isolated_native_rebuild'] is True
            and receipt['standalone_journal_rebuild'] is True
            and receipt['normal_optimized_identical'] is True,
            'a qualified current production receipt is required')
    require(receipt['historical_evidence_reused_as_current_qualification'] is False
            and receipt['source_date_epoch'] == int(EPOCH), 'qualification scope or epoch differs')
    require(re.fullmatch(r'[0-9a-f]{40}', receipt['source_commit']) is not None,
            'receipt source identity is not a full commit SHA')
    require(receipt['source_check'] == {k: v for k, v in checked.items() if k != 'graphs'}
            and receipt['base_commit'] == BASE_COMMIT and receipt['source_files'] == len(inv),
            'source-check receipt differs from the actual native files and graph')
    require(inv == json.loads((ev/'SOURCE_HASHES.json').read_text())
            and sha((ev/'SOURCE_HASHES.json').read_bytes()) == receipt['source_inventory_sha256'],
            'source inventory digest or contents differ')
    require(sha((ev/'NATIVE_SOURCE.zip').read_bytes()) == receipt['native_source_sha256'],
            'native archive digest differs')
    with zipfile.ZipFile(ev/'NATIVE_SOURCE.zip') as archive:
        require(archive_names(archive) == set(inv), 'native archive inventory differs')
        require(all(sha(archive.read(n)) == h for n, h in inv.items()), 'native archive bytes differ')
    packages = json.loads((ev/'PACKAGE_MANIFEST.json').read_text())
    require(packages['schema'] == 'gtf80.packages/1'
            and packages['source_commit'] == receipt['source_commit']
            and packages['documents'] == receipt['documents']
            and set(packages['packages']) == set(PACKAGES), 'package manifest differs')
    for name, digest in packages['packages'].items():
        require(sha((ev/name).read_bytes()) == digest, 'package digest differs: '+name)
    pages = json.loads((ev/'PAGE_CHECKS.json').read_text())
    require(set(pages) == set(receipt['documents']) == set(DOCS.values()), 'published document set differs')
    for name, document in receipt['documents'].items():
        require(sha((root/name).read_bytes()) == document['sha256'] == pages[name]['sha256'],
                'PDF digest differs: '+name)
        signature = pdf_signature(root/name)
        require(signature['pages'] == document['pages'] == pages[name]['pages']
                and signature['page_checks'] == pages[name]['page_checks'], 'PDF page signature differs: '+name)
    require(sha(json_bytes(pages['STRUCTURAL_PAPER.pdf']['page_checks'])) == STRUCTURAL_SIGNATURE_SHA256,
            'structural companion no longer matches its v79 pages')
    require(set(receipt['latex_diagnostics']) == set(DOCS), 'LaTeX diagnostic inventory differs')
    for entry in DOCS:
        log = (ev/(Path(entry).stem.upper()+'_LATEX_LOG.txt')).read_text(errors='replace')
        require(diagnostics(log, entry) == receipt['latex_diagnostics'][entry], 'LaTeX receipt differs: '+entry)
    needed = journal_names(root)
    with zipfile.ZipFile(ev/'JOURNAL_PACKAGE.zip') as archive:
        require(archive_names(archive) == needed | {'JOURNAL_MANIFEST.json'},
                'journal is not the minimal standalone two-article package')
        manifest = json.loads(archive.read('JOURNAL_MANIFEST.json'))
        require(manifest['schema'] == 'gtf80.journal/1'
                and manifest['source_commit'] == receipt['source_commit']
                and manifest['source_date_epoch'] == int(EPOCH)
                and set(manifest['files']) == needed
                and manifest['documents'] == {DOCS[e]: pages[DOCS[e]] for e in JOURNAL_ENTRIES}
                and manifest['historical_PDF_dependencies'] is False
                and manifest['repository_dependencies'] is False, 'journal manifest differs')
        for name in needed:
            require(archive.read(name) == (root/name).read_bytes()
                    and sha(archive.read(name)) == manifest['files'][name], 'journal bytes differ: '+name)
    research_names = set(inv) | set(DOCS.values()) | {'evidence/'+n for n in RESEARCH_EVIDENCE}
    with zipfile.ZipFile(ev/'RESEARCH_PACKAGE.zip') as archive:
        require(archive_names(archive) == research_names, 'research archive inventory differs')
        for name in research_names:
            require(archive.read(name) == (root/name).read_bytes(), 'research archive bytes differ: '+name)
    require(json.loads((ev/'REGRESSION_RESULTS.json').read_text()) == receipt['regression']
            and set(receipt['regression']) == set(SCRIPTS), 'finite regression receipt differs')
    finite_evidence = receipt['finite_evidence_sha256']
    require(isinstance(finite_evidence, dict) and 'REGRESSION_RESULTS.json' in finite_evidence,
            'production must identify its actually executed finite-evidence outputs')
    for name, digest in finite_evidence.items():
        path = safe_relative(name)
        require(len(path.parts) == 1 and path.suffix in {'.json', '.jsonl'}
                and re.fullmatch(r'[0-9a-f]{64}', digest) is not None,
                'invalid finite-evidence output identity: '+name)
        require(sha((ev/path).read_bytes()) == digest,
                'current finite-evidence output differs from production: '+name)
    journal_receipt = json.loads((ev/'JOURNAL_REBUILD.json').read_text())
    require(journal_receipt['schema'] == 'gtf80.journal-rebuild/1' and journal_receipt['status'] == 'success'
            and journal_receipt['source_commit'] == receipt['source_commit']
            and journal_receipt['source_date_epoch'] == int(EPOCH)
            and journal_receipt['read_only'] is True
            and journal_receipt['documents'] == {DOCS[e]: receipt['documents'][DOCS[e]] for e in JOURNAL_ENTRIES},
            'actual standalone reconstruction receipt differs')
    locations = json.loads((ev/'THEOREM_LOCATIONS.json').read_text())
    require(set(locations) == set(DOCS), 'theorem-location document set differs')
    for entry, info in checked['graphs'].items():
        require(set(info['labels']) <= set(locations[entry]), 'theorem map omits active labels: '+entry)
    return receipt, inv, pages


def generated_inventory(root: Path):
    out = {name: sha((root/name).read_bytes()) for name in DOCS.values()}
    for path in sorted((root/'evidence').rglob('*')):
        if path.is_file():
            out[path.relative_to(root).as_posix()] = sha(path.read_bytes())
    return out


def verify_exact_head(root: Path, receipt, inv, requested_head: str):
    actual = git_output(root, 'rev-parse', 'HEAD')
    require(actual == requested_head, 'checkout is not the exact requested commit')
    require(not git_output(root, 'status', '--porcelain', '--untracked-files=no'),
            'tracked checkout is dirty before verification')
    repo = committed_source(root, receipt['source_commit'], inv)
    require(git_output(repo, 'rev-parse', receipt['source_commit']+'^{tree}') == receipt['source_git_tree'],
            'native source Git tree differs from the qualified receipt')
    chain = git_output(repo, 'rev-list', '--parents', '-n', '1', actual).split()
    require(chain == [actual, receipt['source_commit']],
            'publication must have exactly one parent, the qualified native source')
    prefix = root.relative_to(repo).as_posix()+'/'
    generated = {prefix+name for name in DOCS.values()}

    def metadata(name):
        path = Path(name)
        return (len(path.parts) == 1 and name.startswith('GENERAL_THETA_FOUNDATIONS_I_V80_')
                and path.suffix in {'.json', '.md', '.txt'})

    changes = git_output(repo, 'diff', '--name-only', '-z', receipt['source_commit'], actual).split(chr(0))
    require(all(not name or name in generated or name.startswith(prefix+'evidence/') or metadata(name)
                for name in changes), 'publication modified a source or unrelated repository path')
    require(git_output(repo, 'rev-parse', actual+':'+WORKFLOW)
            == git_output(repo, 'rev-parse', receipt['source_commit']+':'+WORKFLOW),
            'read-only workflow changed after native-source qualification')
    preservation = json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    prior = repo/BASE_ROOT
    original_inventory = (prior/'evidence/SOURCE_HASHES.json').read_bytes()
    require(sha(original_inventory) == BASE_INVENTORY_SHA256
            and json.loads(original_inventory) == preservation['files'], 'remote v79 inventory differs')
    for name, digest in preservation['files'].items():
        require(sha((prior/safe_relative(name)).read_bytes()) == digest, 'remote v79 native bytes differ: '+name)
    for entry in DOCS:
        files, labels = graph(prior, entry)
        require({'files': sorted(files), 'labels': labels} == preservation['prior_proof_graphs'][entry],
                'remote predecessor proof graph differs: '+entry)
    return {'head': actual, 'candidate_publication': actual,
            'chain': 'native-source -> publication', 'exact_git_head_checked': True}


def verify_published(root: Path):
    receipt, inv, pages = verify_artifacts(root)
    before = generated_inventory(root)
    head = os.environ.get('GITHUB_SHA') or git_output(root, 'rev-parse', 'HEAD')
    identity = verify_exact_head(root, receipt, inv, head)
    print('read-only exact-head native reconstruction', file=sys.stderr, flush=True)
    with tempfile.TemporaryDirectory(prefix='gtf80-exact-head-') as directory:
        temp = Path(directory)
        with zipfile.ZipFile(root/'evidence/NATIVE_SOURCE.zip') as archive:
            archive_names(archive)
            archive.extractall(temp)
        rebuilt = build(temp, source_commit=receipt['source_commit'], reconstruction=True)
        other = json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
        require(rebuilt['regression'] == receipt['regression'], 'finite regression reconstruction differs')
        require(rebuilt['finite_evidence_sha256'] == receipt['finite_evidence_sha256'],
                'auxiliary finite-evidence inventory or reconstruction bytes differ')
        for name in pages:
            require(pages[name]['page_checks'] == other[name]['page_checks'],
                    'page reconstruction differs: '+name)
        require((temp/'evidence/THEOREM_LOCATIONS.json').read_bytes()
                == (root/'evidence/THEOREM_LOCATIONS.json').read_bytes(), 'theorem locations differ')
        require(sources(temp) == inv, 'reconstructed native inventory differs')
    print('read-only standalone two-article journal reconstruction', file=sys.stderr, flush=True)
    journal = verify_journal(root, receipt['source_commit'])
    require(journal == json.loads((root/'evidence/JOURNAL_REBUILD.json').read_text()),
            'standalone journal qualification differs on reconstruction')
    require(sources(root) == inv and generated_inventory(root) == before,
            'read-only verification changed submitted source or artifact bytes')
    require(not git_output(root, 'status', '--porcelain', '--untracked-files=no'),
            'read-only verification modified tracked files')
    return {'schema': 'gtf80.final-head/1', 'status': 'success', **identity,
            'source_commit': receipt['source_commit'], 'source_git_tree': receipt['source_git_tree'],
            'source_date_epoch': int(EPOCH), 'documents': receipt['documents'],
            'read_only': True, 'native_rebuild_text_and_rasters_match': True,
            'regression_suites': len(SCRIPTS), 'normal_optimized_identical': True,
            'theorem_locations_match': True, 'standalone_journal': journal,
            'historical_evidence_reused_as_current_qualification': False,
            'independent_mathematical_or_priority_certification': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check-source', action='store_true')
    mode.add_argument('--isolated', action='store_true')
    mode.add_argument('--verify-published', action='store_true')
    args = parser.parse_args()
    if args.check_source:
        result, _ = check_source(ROOT)
        result.pop('graphs')
    elif args.verify_published:
        result = verify_published(ROOT)
    else:
        result = build(ROOT, isolated=args.isolated)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
