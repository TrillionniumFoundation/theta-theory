#!/usr/bin/env python3
"""Build native A1 v28 in a separate directory, with label-only cross references.

No dependency is downloaded; no original manuscript source is rewritten.
Requires Python 3.10+, pdflatex and the packages in preamble.tex.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build-v28'

def digest(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git_blob(p:Path)->str:
    data=p.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def expand(root:Path,path:Path,stack:tuple[Path,...]=())->str:
    path=path.resolve()
    if not path.is_relative_to(root.resolve()) or path in stack:
        raise ValueError('Escaping or cyclic input: '+str(path))
    text=path.read_text(encoding='utf-8')
    # Input commands in commented-out lines are not active source dependencies.
    text=re.sub(r'(?m)(?<!\\)%[^\n]*','',text)
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m:expand(root,root/(m[1]+'.tex'),stack+(path,)),text)

def companion_bibliography(stage:Path)->None:
    """Flatten the same known inherited wrappers as the retained v24 builder.
    Unlike that builder, leave the active principal bibliography unchanged.
    """
    text=expand(stage,stage/'references-v23.tex')
    keep=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith(('\\begingroup','\\endgroup','\\let',
            '\\renewcommand{\\endthebibliography}','\\begin{thebibliography}',
            '\\end{thebibliography}','\\enlargethispage')):
            continue
        if re.fullmatch(r'\\[A-Za-z]+EndBibliography\}',s):
            continue
        keep.append(line)
    text='\n'.join(keep)+'\n'
    starts=list(re.finditer(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    entries={}
    for i,m in enumerate(starts):
        if m[1] in entries:
            raise ValueError('Duplicate inherited bibliography key: '+m[1])
        entries[m[1]]=text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)].strip()
    if not entries:
        raise ValueError('Empty inherited companion bibliography')
    ordered=sorted(entries,key=lambda k:re.sub(r'\\[A-Za-z]+|[{}\\\s]','',entries[k].split('\n',1)[1]).lower())
    (stage/'references-companions.tex').write_text('\\begin{thebibliography}{99}\n'+
        '\n\n'.join(entries[k] for k in ordered)+'\n\\end{thebibliography}\n',encoding='utf-8')

def source_audit(stage:Path)->dict:
    texts={d:expand(stage,stage/(d+'.tex')) for d in ('main','companions')}
    labels={d:re.findall(r'\\label\{([^}]+)\}',t) for d,t in texts.items()}
    union=labels['main']+labels['companions']
    duplicates={k:v for k,v in Counter(union).items() if v>1}
    refs=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}','\n'.join(texts.values())))
    missing=sorted(refs-set(union))
    if duplicates or missing:
        raise ValueError(f'Label audit failed: duplicate={duplicates}, missing={missing}')
    for d,t in texts.items():
        cites={k.strip() for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',t) for k in m[1].split(',')}
        bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',t))
        if cites-bib:
            raise ValueError(f'Unresolved {d} citations: {sorted(cites-bib)}')
        (OUT/(d+'-expanded.tex')).write_text(t,encoding='utf-8')
    return {'labels':{d:len(v) for d,v in labels.items()},
            'unresolved_labels':missing,'duplicate_labels':duplicates,
            'source_sha256':{str(p.relative_to(stage)):digest(p) for p in sorted(stage.rglob('*.tex'))}}

def export_labels(stage:Path,doc:str,allowed:set[str])->None:
    src=stage/(doc+'.aux')
    lines=[]
    if src.exists():
        for line in src.read_text(encoding='utf-8').splitlines():
            m=re.match(r'\\newlabel\{([^}]+)\}',line)
            if m and m[1] in allowed:
                if doc=='main':
                    line=re.sub(r'^(\\newlabel\{[^}]+\}\{\{)([^}]+)(\})',lambda x:x[1]+'M.'+x[2]+x[3],line)
                lines.append(line)
    (stage/(doc+'-external.aux')).write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prepare-only',action='store_true')
    args=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    target=OUT/'BUILD_RECORD_V28.json'
    record={'version':28,'status':'started','full_two_volume_build':False,
            'tex_passes':[],'scope':'Executed source, finite diagnostics and typesetting only; no mathematical or journal certification.'}
    try:
        pins=json.loads((ROOT/'NATIVE_SOURCE_RECORD_V28.json').read_text())['pinned_blobs']
        for name,sha in pins.items():
            if git_blob(ROOT/name)!=sha:
                raise ValueError('Pinned source differs: '+name)
        results=[]
        for opts in ([],['-O']):
            p=subprocess.run([sys.executable,*opts,str(ROOT/'diagnostics_v28.py')],
                             capture_output=True,text=True,check=True,timeout=120)
            results.append(p.stdout)
        if results[0]!=results[1]:
            raise ValueError('Normal and optimized diagnostics differ')
        record['diagnostics']=json.loads(results[0])
        record['normal_optimized_identical']=True
        stage=OUT/'native'
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(ROOT,stage,ignore=shutil.ignore_patterns(
            'build-v28','build','__pycache__','*.pdf','*.aux','*.log','*.out','*.toc'))
        companion_bibliography(stage)
        record['source_audit']=source_audit(stage)
        # Old xr-hyper does not accept the second optional nocite argument.
        # Bibliography entries are excluded from both exported auxiliary files.
        conversions=[]
        for name in ('main.tex','companions.tex'):
            p=stage/name; text=p.read_text()
            count=text.count(r'\externaldocument[][nocite]')
            if count:
                p.write_text(text.replace(r'\externaldocument[][nocite]',r'\externaldocument'))
                conversions.append({'file':name,'occurrences':count})
        record['staging_only_xr_compatibility']=conversions
        if args.prepare_only:
            record['status']='source-and-diagnostics-passed; TeX not requested'
        else:
            engine=shutil.which('pdflatex')
            if not engine:
                raise RuntimeError('pdflatex unavailable; full build not executed')
            record['engine']=subprocess.run([engine,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
            allowed={d:set(re.findall(r'\\label\{([^}]+)\}',expand(stage,stage/(d+'.tex')))) for d in ('main','companions')}
            for doc in allowed:
                export_labels(stage,doc,allowed[doc])
            for iteration in range(1,6):
                for doc in ('main','companions'):
                    cmd=[engine,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',doc+'.tex']
                    p=subprocess.run(cmd,cwd=stage,capture_output=True,text=True,timeout=180)
                    (OUT/f'{doc}-pass-{iteration}.txt').write_text(p.stdout+p.stderr)
                    record['tex_passes'].append({'document':doc,'pass':iteration,'returncode':p.returncode})
                    if p.returncode:
                        raise RuntimeError(f'{doc} TeX pass {iteration} failed')
                    export_labels(stage,doc,allowed[doc])
            record['final_log_messages']={}
            bad=re.compile(r'undefined|multiply defined|Rerun to get cross-references right|Label\(s\) may have changed|Overfull \\[hv]box',re.I)
            for doc in allowed:
                log=(stage/(doc+'.log')).read_text(errors='replace')
                warnings=[line for line in log.splitlines() if 'Warning:' in line or 'Underfull' in line or 'Overfull' in line]
                record['final_log_messages'][doc]=warnings
                if bad.search(log):
                    raise RuntimeError(f'{doc}: unresolved, duplicate, unsettled reference or overfull box; inspect final log')
            record['pdf_sha256']={d:digest(stage/(d+'.pdf')) for d in allowed}
            record['full_two_volume_build']=True
            record['status']='native-two-volume-build-passed; visual inspection still separate'
    except Exception as exc:
        record['status']='failed'
        record['error']=str(exc)
        raise
    finally:
        target.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
