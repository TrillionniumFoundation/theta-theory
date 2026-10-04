#!/usr/bin/env python3
"""Build/check the v77 native manuscripts and source-bound evidence.

Requires pdflatex, PyMuPDF and SymPy. Does not modify predecessor files.
--isolated additionally rebuilds the native ZIP in an empty directory.
--verify-published never rewrites the published tree: it hashes it, builds
in a temporary directory and compares every page's text and raster.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
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
NEW_LABELS=['thm:matrixmetric76','lem:matrixpath76','cor:matrixadaptivity76','lem:matrixspectral76','lem:matrixlocal76','lem:matrixball76','prop:matrixvolume76','thm:matrixcover76','thm:commonlearn76','cor:learncode76','thm:matrixlearning77','lem:matrixcalibration77','lem:matrixcompression77','thm:matrixcodec77','cor:matrixlearnedcode77']
EPOCH='1791072000'  # 4 October 2026, 00:00 UTC


def sha(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()


def put(path:Path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def require(ok:bool,message:str):
    if not ok:raise RuntimeError(message)


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
    p=root/entry
    text=p.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    for sub in re.findall(r'\\input\{([^}]+)\}',text):
        labels+=graph(root,sub,seen)[1]
    return seen,labels


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
    for script in ['check_matrix_geometry.py','matrix_codec_check.py','check_common_learning.py','check_biased_geometry.py','check_coupled_geometry.py','check_noisy_readout.py','check_readout.py','check_conditional.py','check_coherent.py','check_preparation.py','check_codec.py','check_choi.py','check_instruments.py','check_streaming.py','inherited_check_v63.py']:
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
        'schema':'gtf77.matrix-effect-codec-example/1','status':'success',
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


def source_identity():
    env=os.environ.get('GTF77_SOURCE_COMMIT')
    if env:return env
    try:
        p=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True)
        return p.stdout.strip()
    except (subprocess.CalledProcessError,FileNotFoundError):return 'uncommitted-working-source'


def make_zip(path:Path,files:dict[str,bytes]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644 << 16
            z.writestr(info,data)


def build(root:Path,isolated:bool=False,source_commit:str|None=None):
    evidence=root/'evidence';evidence.mkdir(exist_ok=True)
    bdir=root/'build';bdir.mkdir(exist_ok=True)
    inventory=sources(root)
    preservation=json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
    prior=set(preservation['prior_labels'])
    _,complete=graph(root,'main.tex')
    # Main proof labels are a subset of the retained TeX inventory. Unused alternative
    # editions are preserved as source too, rather than falsely described as typeset.
    all_labels=[]
    for name in inventory:
        if name.endswith('.tex'):all_labels+=re.findall(r'\\label\{([^}]+)\}',(root/name).read_text())
    require(prior<=set(all_labels),'a prior mathematical label was removed from active native TeX')
    require(set(NEW_LABELS)<=set(complete),'new theorem absent from complete edition')
    maps={};docs={};warnings={}
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH=EPOCH,FORCE_SOURCE_DATE='1',TZ='UTC')
    for entry,target in DOCUMENTS.items():
        _,labs=graph(root,entry)
        require(len(labs)==len(set(labs)),entry+' duplicates labels')
        required=set(preservation['prior_proof_graphs'][entry]['labels'])
        relocation=preservation.get('focused_relocations',{}).get(entry,{})
        moved=set(relocation.get('labels',[]))
        require((required-moved)<=set(labs),'prior proof label missing from '+entry)
        require(moved<=required,'relocation invents a prior label')
        for destination in relocation.get('destination_entries',[]):
            require(moved<=set(graph(root,destination)[1]),'relocated proof absent from '+destination)
        if entry=='main.tex':
            require(required<=set(labs),'complete edition lost predecessor labels')
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
        aux=(bdir/(stem+'.aux')).read_text()
        maps[entry]={}
        for match in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux):
            label,num,page=match.groups();maps[entry][label]={'number':num,'page':page}
        require(set(labs)<=set(maps[entry]),'some labels absent from compiled aux: '+entry)
    regression=run_checks(root,evidence)
    put(evidence/'SOURCE_HASHES.json',inventory)
    put(evidence/'THEOREM_LOCATIONS.json',maps)
    put(evidence/'PAGE_CHECKS.json',docs)
    native={name:(root/name).read_bytes() for name in inventory}
    make_zip(evidence/'NATIVE_SOURCE.zip',native)
    receipt={
        'schema':'gtf77.build/1','status':'success','source_commit':source_commit or source_identity(),
        'base_commit':preservation['base_commit'],'workflow_trigger_commit':os.environ.get('GTF77_TRANSFER_COMMIT'),'source_files':len(inventory),
        'source_inventory_sha256':sha((evidence/'SOURCE_HASHES.json').read_bytes()),
        'native_source_sha256':sha((evidence/'NATIVE_SOURCE.zip').read_bytes()),
        'predecessor_native_files':len(preservation['files']),
        'preserved_native_labels':len(prior),'complete_active_labels':len(complete),
        'focused_relocations':preservation.get('focused_relocations',{}),
        'new_theorems':NEW_LABELS,'documents':{k:{'pages':v['pages'],'sha256':v['sha256']} for k,v in docs.items()},
        'regression':regression,'normal_optimized_identical':True,'latex_diagnostics':warnings,
        'tools':{'python':sys.version.split()[0],'pymupdf':fitz.VersionBind,
                 'pdflatex':subprocess.run(['pdflatex','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]},
        'scope':'Source identity, exact finite regression, complete typesetting and optional isolated reproduction. Not a mathematical proof certificate or independent priority opinion.',
        'isolated_rebuild':False}
    if isolated:
        with tempfile.TemporaryDirectory(prefix='gtf77-isolated-') as tmp:
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
    for n in ['paper.pdf','STRUCTURAL_PAPER.pdf','RESPONSE_TO_REFEREE.md','journal_verify.py','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md']:
        jf[n]=(root/n).read_bytes()
    jm={'schema':'gtf77.journal/1','source_commit':receipt['source_commit'],
        'files':{n:sha(b) for n,b in jf.items()},
        'documents':{n:docs[n] for n in ['paper.pdf','STRUCTURAL_PAPER.pdf']},
        'build_command':'python journal_verify.py','historical_PDF_dependencies':False}
    jf['JOURNAL_MANIFEST.json']=(json.dumps(jm,indent=2,sort_keys=True)+'\n').encode()
    make_zip(evidence/'JOURNAL_PACKAGE.zip',jf)
    rf={**native,**{n:(root/n).read_bytes() for n in DOCUMENTS.values()}}
    for n in ['BUILD_RECEIPT.json','SOURCE_HASHES.json','THEOREM_LOCATIONS.json','REGRESSION_RESULTS.json','PAGE_CHECKS.json']:
        rf['evidence/'+n]=(evidence/n).read_bytes()
    make_zip(evidence/'RESEARCH_PACKAGE.zip',rf)
    put(evidence/'PACKAGE_MANIFEST.json',{
        'schema':'gtf77.packages/1','source_commit':receipt['source_commit'],
        'packages':{n:sha((evidence/n).read_bytes()) for n in
                    ['NATIVE_SOURCE.zip','JOURNAL_PACKAGE.zip','RESEARCH_PACKAGE.zip']},
        'documents':receipt['documents'],
        'scope':'Digest inventory of actual built artifacts; not an author signature.'})
    return receipt


def verify_published(root:Path):
    evidence=root/'evidence'
    receipt=json.loads((evidence/'BUILD_RECEIPT.json').read_text())
    inv=json.loads((evidence/'SOURCE_HASHES.json').read_text())
    require(sources(root)==inv,'published native source hash mismatch')
    require(sha((evidence/'NATIVE_SOURCE.zip').read_bytes())==receipt['native_source_sha256'],'native archive mismatch')
    with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as z:
        require(set(z.namelist())==set(inv),'native archive inventory mismatch')
        require(all(sha(z.read(n))==h for n,h in inv.items()),'native archive source mismatch')
    pm=json.loads((evidence/'PACKAGE_MANIFEST.json').read_text())
    require(pm['source_commit']==receipt['source_commit'],'package source mismatch')
    for n,h in pm['packages'].items():
        require(sha((evidence/n).read_bytes())==h,'published package hash mismatch '+n)
    with zipfile.ZipFile(evidence/'RESEARCH_PACKAGE.zip') as z:
        for n,h in inv.items():
            require(sha(z.read(n))==h,'research source mismatch '+n)
        for n,d in receipt['documents'].items():
            require(sha(z.read(n))==d['sha256'],'research PDF mismatch '+n)
    pages=json.loads((evidence/'PAGE_CHECKS.json').read_text())
    for name,data in receipt['documents'].items():
        require(sha((root/name).read_bytes())==data['sha256'],'published PDF hash mismatch')
        require(pdf_signature(root/name)['page_checks']==pages[name]['page_checks'],'published page signature mismatch')
    envsha=os.environ.get('GITHUB_SHA')
    if envsha:
        actual=subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
        parent=subprocess.run(['git','rev-parse','HEAD^'],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
        require(actual==envsha,'checkout is not the triggering SHA')
        request_path=root.parent.parent/'GENERAL_THETA_FOUNDATIONS_I_V77_FINAL_HEAD_REQUEST.json'
        if request_path.is_file():
            request=json.loads(request_path.read_text())
            require(request['candidate_publication']==parent,'request is not direct successor of publication')
            require(request['native_source']==receipt['source_commit'],'request source differs from receipt')
            native_parent=subprocess.run(['git','rev-parse',parent+'^'],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
            require(native_parent==receipt['source_commit'],'publication is not direct successor of native source')
        else:
            require(parent==receipt['source_commit'],'publication is not direct successor of native source')
        before=subprocess.run(['git','status','--porcelain','--untracked-files=no'],cwd=root,capture_output=True,text=True,check=True).stdout
        require(not before,'tracked checkout was dirty before verification')
        preserve=json.loads((root/'PRESERVATION_MANIFEST.json').read_text())
        pred=root.parent.parent/preserve['source_root']
        for name,h in preserve['files'].items():
            require((pred/name).is_file() and sha((pred/name).read_bytes())==h,'predecessor native changed: '+name)
    with tempfile.TemporaryDirectory(prefix='gtf77-published-check-') as tmp:
        temp=Path(tmp)
        with zipfile.ZipFile(evidence/'NATIVE_SOURCE.zip') as z:z.extractall(temp)
        got=build(temp,False,source_commit=receipt['source_commit'])
        other=json.loads((temp/'evidence/PAGE_CHECKS.json').read_text())
        for name in pages:require(pages[name]['page_checks']==other[name]['page_checks'],'rebuilt PDF differs '+name)
        require(got['regression']==receipt['regression'],'rebuilt regression differs')
    if envsha:
        after=subprocess.run(['git','status','--porcelain','--untracked-files=no'],cwd=root,capture_output=True,text=True,check=True).stdout
        require(not after,'verifier modified tracked files')
    return {'schema':'gtf77.final-head/1','status':'success','head':envsha or 'local',
            'source_commit':receipt['source_commit'],'documents':receipt['documents'],
            'read_only':True,'native_rebuild_text_and_rasters_match':True,
            'independent_mathematical_or_priority_certification':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--isolated',action='store_true')
    ap.add_argument('--verify-published',action='store_true')
    args=ap.parse_args()
    result=verify_published(ROOT) if args.verify_published else build(ROOT,args.isolated)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
