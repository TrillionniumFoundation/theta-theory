#!/usr/bin/env python3
"""Build/check the v78 native manuscripts and source-bound evidence.

Requires pdflatex, PyMuPDF and SymPy. Does not modify predecessor files.
--isolated additionally rebuilds the native ZIP in an empty directory.
--verify-published never rewrites the published tree: it hashes it, builds
in a temporary directory and compares every page's text and raster.
--check-source performs the preservation and active-input checks without a build.
Production builds require an actual committed, byte-matching native source.
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

ROOT=Path(__file__).resolve().parent
DOCUMENTS={'quantitative.tex':'paper.pdf','structural.tex':'STRUCTURAL_PAPER.pdf','main.tex':'COMPLETE_REVISION.pdf'}
REVISION=78
NEW_SECTIONS=('sections/58-block-resource-learning.tex','sections/59-finite-control-learning.tex',
              'sections/60-dimension-accuracy-learning.tex')
NEW_LABELS=('thm:blocklearning78','lem:blockhybrid78','lem:blockfidelity78',
            'cor:onecallseparation78','cor:blocklearnedcode78',
            'lem:controlhybrid78','thm:finitecontrollearning78',
            'lem:weakmeasurementinfo78','thm:dimensionlower78','cor:binaryoperatorlearning78',
            'lem:interiormetric78','thm:interiorlearning78')
REGRESSION_SCRIPTS=('check_matrix_geometry.py','matrix_codec_check.py','check_common_learning.py',
        'check_biased_geometry.py','check_coupled_geometry.py','check_noisy_readout.py',
        'check_readout.py','check_conditional.py','check_coherent.py','check_preparation.py',
        'check_codec.py','check_choi.py','check_instruments.py','check_streaming.py',
        'inherited_check_v63.py','block_resource_check.py')
JOURNAL_EXTRAS=('paper.pdf','STRUCTURAL_PAPER.pdf','RESPONSE_TO_REFEREE.md',
                'journal_verify.py','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md')
RESEARCH_EVIDENCE=('BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json',
                   'REGRESSION_RESULTS.json','PAGE_CHECKS.json')
FINAL_REQUEST='GENERAL_THETA_FOUNDATIONS_I_V78_FINAL_HEAD_REQUEST.json'
WORKFLOW='.github/workflows/gtf-i-v78-exact-head.yml'
EPOCH='1791072000'  # 4 October 2026, 00:00 UTC


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


def graph(root:Path,entry:str,seen=None):
    if seen is None:seen=set()
    entry=str(Path(entry).with_suffix('.tex'))
    require(entry not in seen,'duplicate/recursive input in '+entry)
    seen.add(entry)
    p=root/safe_relative(entry)
    require(p.is_file(),'missing active TeX input '+entry)
    text=p.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    for sub in re.findall(r'\\input\{([^}]+)\}',text):
        labels+=graph(root,sub,seen)[1]
    return seen,labels


def check_source(root:Path,inventory=None):
    """Check v77 identity separately from v78 active proof and report content."""
    inventory=sources(root) if inventory is None else inventory
    p=json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    require(p['schema']=='gtf78.preservation/1','v78 preservation manifest required')
    require(len(p['files'])==330 and len(p['prior_labels'])==707,
            'v77 baseline must contain 330 native files and 707 complete labels')
    require(not p.get('focused_relocations'),'v78 does not relocate predecessor focused labels')
    archived=p.get('archived_originals',{})
    require(set(archived)<=set(p['files']),'archive mapping invents a predecessor file')
    changed=[]
    for name,digest in p['files'].items():
        current=root/safe_relative(name)
        require(current.is_file(),'predecessor native path removed: '+name)
        if sha(current.read_bytes())!=digest:
            require(name in archived,'changed predecessor lacks an archived original: '+name)
            original=root/safe_relative(archived[name])
            require(original.is_file() and sha(original.read_bytes())==digest,
                    'changed predecessor original mismatch: '+name)
            changed.append(name)
    for name,archive in archived.items():
        original=root/safe_relative(archive)
        require(original.is_file() and sha(original.read_bytes())==p['files'][name],
                'archived predecessor mismatch: '+name)
    proof=json.loads((root/'PROOF_TEXT_PRESERVATION.json').read_text())
    require(proof['schema']=='gtf78.proof-text-preservation/1','v78 proof preservation required')
    require(proof['predecessor']==p['base_commit'],'proof preservation predecessor mismatch')
    require(not proof['removed_proof_sections'] and not proof['reviewed_additive_changes'],
            'v78 must retain every inherited mathematical section unchanged')
    graphs={}
    for entry in DOCUMENTS:
        active,labels=graph(root,entry)
        require(len(labels)==len(set(labels)),entry+' duplicates labels')
        require(set(p['prior_proof_graphs'][entry]['labels'])<=set(labels),
                'prior active proof label missing from '+entry)
        graphs[entry]={'files':sorted(active),'labels':labels}
    for name in proof['byte_identical_sections']:
        require(name in p['files'] and inventory.get(name)==p['files'][name],
                'inherited proof text changed: '+name)
        if name in p['prior_proof_graphs']['main.tex']['files']:
            require(name in graphs['main.tex']['files'],'inherited active proof section removed: '+name)
    require(set(proof['new_sections'])==set(NEW_SECTIONS),'unexpected new proof section inventory')
    new_labels=[]
    for name in NEW_SECTIONS:
        require(name in graphs['main.tex']['files'] and name in graphs['quantitative.tex']['files'],
                'new proof section absent from complete or focused edition: '+name)
        labels=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(root/name).read_text())
        require(labels and all(label.endswith('78') for label in labels),
                'new section must declare v78 theorem labels: '+name)
        new_labels+=labels
    require(len(new_labels)==len(set(new_labels)),'new theorem labels duplicate')
    require(set(new_labels)==set(NEW_LABELS),'required v78 theorem set differs from the specified new results')
    controls=json.loads((root/'CONTROLLING_REPORTS.json').read_text())
    require(controls['revision']==78 and controls['review_round']==51,
            'v78 must be controlled by the R51 reports')
    require(controls['reviewed_head']==p['base_commit']
            and controls['reviewed_native_source']==p['native_source_commit'],
            'controlling reviewed object differs from preservation baseline')
    require({r['kind'] for r in controls['reports']}=={'external','pipeline'},
            'both independent R51 controls are required')
    for report in controls['reports']:
        data=(root/safe_relative(report['frozen'])).read_bytes()
        require(sha(data)==report['sha256'] and git_blob(data)==report['git_blob'],
                'frozen R51 report bytes changed: '+report['kind'])
    require(all(script in inventory for script in REGRESSION_SCRIPTS),
            'a registered exact regression script is missing from native sources')
    return {'schema':'gtf78.source-check/1','status':'success','source_files':len(inventory),
            'base_commit':p['base_commit'],
            'predecessor_native_files':330,'preserved_native_labels':707,
            'changed_predecessor_files':changed,'new_theorems':new_labels,
            'documents':{entry:{'active_files':len(g['files']),'active_labels':len(g['labels'])}
                         for entry,g in graphs.items()},
            'active_graphs':graphs,'proof_sections_byte_identical':len(proof['byte_identical_sections']),
            'byte_identical_active_section_files':len(set(proof['byte_identical_sections'])
                    &set(p['prior_proof_graphs']['main.tex']['files'])),
            'regression_suites':len(REGRESSION_SCRIPTS),
            'historical_evidence_reused_as_v78_qualification':False}


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
        'schema':'gtf78.matrix-effect-codec-example/1','status':'success',
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


def committed_inventory(root:Path,commit:str,inventory):
    """Tie every native byte to the named Git source object, without checkout edits."""
    require(re.fullmatch(r'[0-9a-f]{40}',commit) is not None,'full native-source SHA required')
    repo=Path(git_output(root,'rev-parse','--show-toplevel'))
    prefix=root.relative_to(repo).as_posix()+'/'
    listing=subprocess.run(['git','ls-tree','-r','-z',commit,'--',prefix],cwd=repo,
                           capture_output=True,check=True,timeout=120).stdout
    blobs={}
    for item in listing.split(b'\0'):
        if not item:continue
        meta,path=item.split(b'\t',1)
        mode,kind,digest=meta.decode().split()
        require(kind=='blob','non-file source tree entry')
        blobs[path.decode()]=digest
    generated_pdfs={prefix+name for name in DOCUMENTS.values()}
    require(not any(name.startswith(prefix+'evidence/') or name in generated_pdfs for name in blobs),
            'the native-source object must precede generated v78 PDFs and evidence')
    for name,digest in inventory.items():
        data=(root/safe_relative(name)).read_bytes()
        require(sha(data)==digest and blobs.get(prefix+name)==git_blob(data),
                'native source does not match commit '+commit+': '+name)
    return repo


def source_identity(root:Path,inventory):
    actual=git_output(root,'rev-parse','HEAD')
    source=os.environ.get('GTF78_SOURCE_COMMIT',actual)
    require(source==actual,'build at the actual native-source commit, not an asserted older SHA')
    committed_inventory(root,source,inventory)
    return source


def make_zip(path:Path,files:dict[str,bytes]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644 << 16
            z.writestr(info,data)


def build(root:Path,isolated:bool=False,source_commit:str|None=None):
    inventory=sources(root)
    checked=check_source(root,inventory)
    if source_commit is None:source_commit=source_identity(root,inventory)
    require(re.fullmatch(r'[0-9a-f]{40}',source_commit) is not None,'full source commit required')
    evidence=root/'evidence';evidence.mkdir(exist_ok=True)
    bdir=root/'build';bdir.mkdir(exist_ok=True)
    preservation=json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    prior=set(preservation['prior_labels'])
    complete=checked['active_graphs']['main.tex']['labels']
    maps={};docs={};warnings={}
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH=EPOCH,FORCE_SOURCE_DATE='1',TZ='UTC')
    for entry,target in DOCUMENTS.items():
        _,labs=graph(root,entry)
        require(len(labs)==len(set(labs)),entry+' duplicates labels')
        for i in range(3):
            proc=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                                 '-output-directory='+str(bdir),entry],cwd=root,env=env,capture_output=True,timeout=180)
            if proc.returncode:
                raise RuntimeError(proc.stdout.decode(errors='replace')[-6000:])
        stem=Path(entry).stem
        log=(bdir/(stem+'.log')).read_text(errors='replace')
        forbidden=['There were undefined references','There were undefined citations','multiply defined','Undefined control sequence','Rerun to get cross-references right']
        require(not any(t in log for t in forbidden),'unresolved LaTeX diagnostics: '+entry)
        (evidence/(stem.upper()+'_LATEX_LOG.txt')).write_text(log)
        warnings[entry]=re.findall(r'(?:Overfull|Underfull) \\[^\n]+',log)
        require(not warnings[entry],'unresolved overfull/underfull typesetting boxes: '+entry)
        shutil.copy2(bdir/(stem+'.pdf'),root/target)
        docs[target]=pdf_signature(root/target)
        docs[target]['sha256']=sha((root/target).read_bytes())
        unchanged=preservation.get('unchanged_documents',{}).get(entry)
        if unchanged:
            require(docs[target]['pages']==unchanged['pages'],'unchanged companion page count differs')
            require(sha(json.dumps(docs[target]['page_checks'],sort_keys=True,separators=(',',':')).encode())
                    ==unchanged['page_checks_sha256'],'unchanged companion text or rasters differ')
        aux=(bdir/(stem+'.aux')).read_text()
        maps[entry]={}
        for match in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux):
            label,num,page=match.groups();maps[entry][label]={'number':num,'page':page}
        require(set(labs)<=set(maps[entry]),'some labels absent from compiled aux: '+entry)
    regression=run_checks(root,evidence)
    put(evidence/'SOURCE_HASHES.json',inventory)
    put(evidence/'THEOREM_LOCATIONS.json',maps)
    put(evidence/'PAGE_CHECKS.json',docs)
    require(sources(root)==inventory,'native sources changed during the build')
    native={name:(root/name).read_bytes() for name in inventory}
    make_zip(evidence/'NATIVE_SOURCE.zip',native)
    receipt={
        'schema':'gtf78.build/1','status':'success','source_commit':source_commit,
        'base_commit':preservation['base_commit'],'workflow_trigger_commit':os.environ.get('GTF78_TRANSFER_COMMIT'),'source_files':len(inventory),
        'source_inventory_sha256':sha((evidence/'SOURCE_HASHES.json').read_bytes()),
        'native_source_sha256':sha((evidence/'NATIVE_SOURCE.zip').read_bytes()),
        'predecessor_native_files':len(preservation['files']),
        'preserved_native_labels':len(prior),'complete_active_labels':len(complete),
        'focused_relocations':preservation.get('focused_relocations',{}),
        'new_theorems':checked['new_theorems'],'documents':{k:{'pages':v['pages'],'sha256':v['sha256']} for k,v in docs.items()},
        'active_document_labels':{entry:value['active_labels'] for entry,value in checked['documents'].items()},
        'changed_predecessor_files':checked['changed_predecessor_files'],
        'proof_sections_byte_identical':checked['proof_sections_byte_identical'],
        'byte_identical_active_section_files':checked['byte_identical_active_section_files'],
        'historical_evidence_reused_as_v78_qualification':False,
        'regression':regression,'normal_optimized_identical':True,'latex_diagnostics':warnings,
        'latex_diagnostic_scope':'No unresolved references/citations, multiply defined labels, or '
                'overfull/underfull boxes; raw engine and font warnings remain in the saved logs.',
        'tools':{'python':sys.version.split()[0],'pymupdf':fitz.VersionBind,
                 'pdflatex':subprocess.run(['pdflatex','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]},
        'scope':'Source identity, exact finite regression, complete typesetting and optional isolated reproduction. Not a mathematical proof certificate or independent priority opinion.',
        'isolated_rebuild':False,'standalone_journal_rebuild':False}
    if isolated:
        with tempfile.TemporaryDirectory(prefix='gtf78-isolated-') as tmp:
            temp=Path(tmp)
            with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as z:z.extractall(temp)
            got=build(temp,False,source_commit=receipt['source_commit'])
            other=json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
            for name in docs:
                require(docs[name]['page_checks']==other[name]['page_checks'],'isolated page mismatch '+name)
            require(regression==got['regression'],'isolated regression mismatch')
            require(sources(temp)==inventory,'isolated source inventory mismatch')
        receipt['isolated_rebuild']=True
    put(evidence/'BUILD_RECEIPT.json',receipt)
    # The focused archive contains only active inputs of the two journal articles.
    needed=set()
    for e in ['quantitative.tex','structural.tex']:needed.update(graph(root,e)[0])
    jf={n:(root/n).read_bytes() for n in needed}
    for n in JOURNAL_EXTRAS:
        jf[n]=(root/n).read_bytes()
    jm={'schema':'gtf78.journal/1','source_commit':receipt['source_commit'],
        'files':{n:sha(b) for n,b in jf.items()},
        'documents':{n:docs[n] for n in ['paper.pdf','STRUCTURAL_PAPER.pdf']},
        'build_command':'python journal_verify.py','historical_PDF_dependencies':False,
        'repository_dependencies':False,
        'tools':{'pdflatex':receipt['tools']['pdflatex'],'pymupdf':fitz.VersionBind}}
    jf['JOURNAL_MANIFEST.json']=(json.dumps(jm,indent=2,sort_keys=True)+'\n').encode()
    make_zip(evidence/'JOURNAL_PACKAGE.zip',jf)
    if isolated:
        with tempfile.TemporaryDirectory(prefix='gtf78-journal-isolated-') as tmp:
            temp=Path(tmp)
            with zipfile.ZipFile(evidence/'JOURNAL_PACKAGE.zip') as z:z.extractall(temp)
            result=subprocess.run([sys.executable,str(temp/'journal_verify.py')],cwd=temp,
                                  capture_output=True,check=True,timeout=600)
            journal=json.loads(result.stdout)
            require(journal['schema']=='gtf78.journal-rebuild/1' and journal['status']=='success'
                    and journal['source_commit']==source_commit,'standalone journal qualification failed')
            (evidence/'JOURNAL_REBUILD.json').write_bytes(result.stdout)
        receipt['standalone_journal_rebuild']=True
        put(evidence/'BUILD_RECEIPT.json',receipt)
    rf={**native,**{n:(root/n).read_bytes() for n in DOCUMENTS.values()}}
    for n in RESEARCH_EVIDENCE:
        rf['evidence/'+n]=(evidence/n).read_bytes()
    make_zip(evidence/'RESEARCH_PACKAGE.zip',rf)
    put(evidence/'PACKAGE_MANIFEST.json',{
        'schema':'gtf78.packages/1','source_commit':receipt['source_commit'],
        'packages':{n:sha((evidence/n).read_bytes()) for n in
                    ['NATIVE_SOURCE.zip','JOURNAL_PACKAGE.zip','RESEARCH_PACKAGE.zip']},
        'documents':receipt['documents'],
        'scope':'Digest inventory of actual built artifacts; not an author signature.'})
    return receipt


def archive_names(archive):
    names=archive.namelist()
    require(len(names)==len(set(names)), 'archive contains duplicate names')
    for name in names:safe_relative(name)
    return set(names)


def verify_artifacts(root:Path):
    """Hash and cross-check the actual published objects; do not regenerate them."""
    evidence=root/'evidence'
    receipt=json.loads((evidence/'BUILD_RECEIPT.json').read_text())
    require(receipt['schema']=='gtf78.build/1' and receipt['status']=='success',
            'fresh v78 production receipt required')
    require(receipt['isolated_rebuild'] and receipt['normal_optimized_identical']
            and receipt['standalone_journal_rebuild'],
            'production receipt lacks isolated, standalone-journal, or optimized-mode qualification')
    require(receipt['historical_evidence_reused_as_v78_qualification'] is False,
            'historical evidence cannot qualify the v78 object')
    require(set(receipt['latex_diagnostics'])==set(DOCUMENTS)
            and all(not warning for warning in receipt['latex_diagnostics'].values()),
            'production receipt contains unresolved typesetting boxes')
    inv=json.loads((evidence/'SOURCE_HASHES.json').read_text())
    require(sources(root)==inv,'published native source hash mismatch')
    require(sha((evidence/'SOURCE_HASHES.json').read_bytes())==receipt['source_inventory_sha256'],
            'receipt source-inventory digest mismatch')
    checked=check_source(root,inv)
    require(receipt['source_files']==len(inv) and receipt['base_commit']==checked['base_commit']
            and receipt['predecessor_native_files']==checked['predecessor_native_files']
            and receipt['preserved_native_labels']==checked['preserved_native_labels']
            and receipt['changed_predecessor_files']==checked['changed_predecessor_files']
            and receipt['proof_sections_byte_identical']==checked['proof_sections_byte_identical']
            and receipt['byte_identical_active_section_files']==checked['byte_identical_active_section_files']
            and receipt['focused_relocations']=={}
            and receipt['complete_active_labels']==checked['documents']['main.tex']['active_labels']
            and receipt['active_document_labels']=={entry:info['active_labels']
                    for entry,info in checked['documents'].items()}
            and receipt['new_theorems']==checked['new_theorems'],
            'receipt source-graph inventory mismatch')
    require(sha((evidence/'NATIVE_SOURCE.zip').read_bytes())==receipt['native_source_sha256'],
            'native archive mismatch')
    with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as z:
        require(archive_names(z)==set(inv),'native archive inventory mismatch')
        require(all(sha(z.read(n))==h for n,h in inv.items()),'native archive source mismatch')
    pm=json.loads((evidence/'PACKAGE_MANIFEST.json').read_text())
    require(pm['schema']=='gtf78.packages/1' and pm['source_commit']==receipt['source_commit'],
            'package revision or source mismatch')
    require(set(pm['packages'])=={'NATIVE_SOURCE.zip','JOURNAL_PACKAGE.zip','RESEARCH_PACKAGE.zip'},
            'package inventory mismatch')
    require(pm['documents']==receipt['documents'],'package document inventory mismatch')
    for n,h in pm['packages'].items():
        require(sha((evidence/n).read_bytes())==h,'published package hash mismatch '+n)
    pages=json.loads((evidence/'PAGE_CHECKS.json').read_text())
    require(set(pages)==set(DOCUMENTS.values())==set(receipt['documents']),
            'document set differs from the three intended editions')
    for name,data in receipt['documents'].items():
        require(sha((root/name).read_bytes())==data['sha256']==pages[name]['sha256'],
                'published PDF hash mismatch '+name)
        signature=pdf_signature(root/name)
        require(signature['pages']==data['pages']==pages[name]['pages']
                and signature['page_checks']==pages[name]['page_checks'],
                'published page signature mismatch '+name)
    with zipfile.ZipFile(evidence/'RESEARCH_PACKAGE.zip') as z:
        expected=set(inv)|set(DOCUMENTS.values())|{'evidence/'+n for n in RESEARCH_EVIDENCE}
        require(archive_names(z)==expected,'research archive inventory mismatch')
        for n,h in inv.items():require(sha(z.read(n))==h,'research source mismatch '+n)
        for n,d in receipt['documents'].items():
            require(sha(z.read(n))==d['sha256'],'research PDF mismatch '+n)
        for n in RESEARCH_EVIDENCE:
            require(z.read('evidence/'+n)==(evidence/n).read_bytes(),
                    'research embedded evidence differs '+n)
    with zipfile.ZipFile(evidence/'JOURNAL_PACKAGE.zip') as z:
        needed=set(JOURNAL_EXTRAS)
        for entry in ('quantitative.tex','structural.tex'):needed.update(graph(root,entry)[0])
        require(archive_names(z)==needed|{'JOURNAL_MANIFEST.json'},
                'journal package is not the minimal standalone active-source package')
        jm=json.loads(z.read('JOURNAL_MANIFEST.json'))
        require(jm['schema']=='gtf78.journal/1' and jm['source_commit']==receipt['source_commit']
                and jm['historical_PDF_dependencies'] is False
                and jm['repository_dependencies'] is False,'journal identity or scope mismatch')
        require(set(jm['files'])==needed,'journal file inventory mismatch')
        for name,digest in jm['files'].items():
            require(sha(z.read(name))==digest==sha((root/name).read_bytes()),
                    'journal source or PDF mismatch '+name)
        require(jm['documents']=={name:pages[name] for name in ('paper.pdf','STRUCTURAL_PAPER.pdf')},
                'journal page inventory mismatch')
    require(set(receipt['regression'])==set(REGRESSION_SCRIPTS)
            and json.loads((evidence/'REGRESSION_RESULTS.json').read_text())==receipt['regression'],
            'regression evidence differs from production receipt')
    journal_receipt=json.loads((evidence/'JOURNAL_REBUILD.json').read_text())
    require(journal_receipt['schema']=='gtf78.journal-rebuild/1'
            and journal_receipt['status']=='success'
            and journal_receipt['source_commit']==receipt['source_commit']
            and journal_receipt['documents']=={name:receipt['documents'][name]
                    for name in ('paper.pdf','STRUCTURAL_PAPER.pdf')},
            'standalone journal reconstruction receipt differs')
    locations=json.loads((evidence/'THEOREM_LOCATIONS.json').read_text())
    for entry,data in checked['active_graphs'].items():
        require(set(data['labels'])<=set(locations[entry]),'theorem locations omit active labels '+entry)
    return receipt,inv,pages


def verify_exact_head(root:Path,receipt,inventory,requested_head:str):
    """Enforce source -> publication -> optional metadata-only final child."""
    actual=git_output(root,'rev-parse','HEAD')
    require(actual==requested_head,'checkout is not the triggering exact SHA')
    require(not git_output(root,'status','--porcelain','--untracked-files=no'),
            'tracked checkout was dirty before verification')
    repo=committed_inventory(root,receipt['source_commit'],inventory)
    prefix=root.relative_to(repo).as_posix()+'/'
    def parent(commit):
        chain=git_output(root,'rev-list','--parents','-n','1',commit).split()
        require(len(chain)==2,'publication chain must have one direct parent per commit')
        return chain[1]
    def metadata_name(name):
        path=Path(name)
        return (len(path.parts)==1 and path.name.startswith('GENERAL_THETA_FOUNDATIONS_I_V78_')
                and path.suffix in {'.json','.md','.txt'})
    request_path=repo/FINAL_REQUEST
    if request_path.is_file():
        request=json.loads(request_path.read_text())
        require(request['schema']=='gtf78.final-head-request/1','v78 final-head request required')
        publication=parent(actual)
        require(request['candidate_publication']==publication,
                'final request is not the direct child of its named publication')
        require(request['native_source']==receipt['source_commit']
                and request['manuscript_and_package_bytes_changed'] is False,
                'final request source or immutable-artifact assertion differs')
        changes=git_output(root,'diff','--name-only','-z',publication,actual).split(chr(0))
        allowed_evidence=prefix+'evidence/FINAL_HEAD_REQUEST.json'
        require(all(not name or metadata_name(name) or name==allowed_evidence for name in changes),
                'final child changes files outside permitted review metadata')
        evidence_request=root/'evidence/FINAL_HEAD_REQUEST.json'
        if evidence_request.is_file():
            require(json.loads(evidence_request.read_text())==request,
                    'root and evidence final-head requests differ')
        chain_kind='native-source -> publication -> metadata-only final child'
    else:
        publication=actual
        chain_kind='native-source -> publication'
    require(parent(publication)==receipt['source_commit'],
            'publication is not a direct successor of the qualified native source')
    changes=git_output(root,'diff','--name-only','-z',receipt['source_commit'],publication).split(chr(0))
    generated={prefix+name for name in DOCUMENTS.values()}
    require(all(not name or name in generated or name.startswith(prefix+'evidence/')
                or metadata_name(name) for name in changes),
            'publication changes files outside generated artifacts and v78 review metadata')
    # The verifying workflow must be fixed in the native object and remain unchanged.
    workflow_source=git_output(root,'rev-parse',receipt['source_commit']+':'+WORKFLOW)
    require(git_output(root,'rev-parse',actual+':'+WORKFLOW)==workflow_source,
            'exact-head workflow changed after native-source qualification')
    preserve=json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    predecessor=repo/preserve['source_root']
    predecessor_inventory=(predecessor/'evidence/SOURCE_HASHES.json').read_bytes()
    require(sha(predecessor_inventory)==preserve['source_inventory_sha256']
            and json.loads(predecessor_inventory)==preserve['files'],
            'preservation file inventory differs from the reviewed v77 native inventory')
    for name,digest in preserve['files'].items():
        previous=predecessor/safe_relative(name)
        require(previous.is_file() and sha(previous.read_bytes())==digest,
                'predecessor native changed: '+name)
    return {'head':actual,'candidate_publication':publication,'chain':chain_kind}


def verify_published(root:Path):
    receipt,inv,pages=verify_artifacts(root)
    envsha=os.environ.get('GITHUB_SHA')
    identity=verify_exact_head(root,receipt,inv,envsha) if envsha else {
        'head':'local-artifact-check','candidate_publication':None,'chain':'not asserted locally'}
    with tempfile.TemporaryDirectory(prefix='gtf78-published-check-') as tmp:
        temp=Path(tmp)
        with zipfile.ZipFile(root/'evidence/NATIVE_SOURCE.zip') as z:z.extractall(temp)
        got=build(temp,False,source_commit=receipt['source_commit'])
        other=json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
        for name in pages:
            require(pages[name]['page_checks']==other[name]['page_checks'],'rebuilt PDF differs '+name)
        require(got['regression']==receipt['regression'],'rebuilt regression differs')
        require(json.loads((temp/'evidence/THEOREM_LOCATIONS.json').read_text())
                ==json.loads((root/'evidence/THEOREM_LOCATIONS.json').read_text()),
                'rebuilt theorem numbers or page locations differ')
        require(sources(temp)==inv,'rebuilt native inventory differs')
    require(sources(root)==inv,'verifier changed native source files')
    if envsha:
        require(not git_output(root,'status','--porcelain','--untracked-files=no'),
                'verifier modified tracked files')
    return {'schema':'gtf78.final-head/1','status':'success',**identity,
            'source_commit':receipt['source_commit'],'documents':receipt['documents'],
            'read_only':True,'native_rebuild_text_and_rasters_match':True,
            'exact_git_head_checked':bool(envsha),
            'historical_evidence_reused_as_v78_qualification':False,
            'independent_mathematical_or_priority_certification':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument('--isolated',action='store_true')
    mode.add_argument('--verify-published',action='store_true')
    mode.add_argument('--check-source',action='store_true')
    args=ap.parse_args()
    if args.check_source:
        result=check_source(ROOT)
        result.pop('active_graphs')
    elif args.verify_published:result=verify_published(ROOT)
    else:result=build(ROOT,args.isolated)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
