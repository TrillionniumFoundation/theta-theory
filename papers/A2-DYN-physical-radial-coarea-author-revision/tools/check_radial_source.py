#!/usr/bin/env python3
"""Fail closed on required source identity and native closure, not prove math."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def require(x,m):
    if not x:raise RuntimeError(m)
def identity(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def main():
    M=json.loads((P/'SOURCE_MANIFEST.json').read_text())
    for name,expected in M['current_files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe manifest path')
        p=P/name;require(p.is_file(),'missing required source '+name)
        require(identity(p)==expected,'source bytes changed '+name)
    for name,h in M['unchanged_original_files'].items():
        require(identity(P/name)['git_blob']==h,'inherited proof/interface changed '+name)
    for name in M['required_diagnostic_programs']:
        require(('tools/'+name+'.py') in M['current_files'],'ungated diagnostic '+name)
        require((P/'tools'/(name+'.py')).is_file(),'missing required diagnostic '+name)
    queue=[P/'main.tex'];seen=set();labels=[];refs=[]
    while queue:
        p=queue.pop();name=p.relative_to(P).as_posix()
        if name in seen:continue
        require(name in M['current_files'],'undeclared native source '+name)
        require(p.is_file(),'missing TeX input '+name);seen.add(name)
        s=p.read_text();require(not any(ord(c)<32 and c not in '\n\t\r' for c in s),'control character '+name)
        s=re.sub(r'(?<!\\)%[^\n]*','',s)
        labels+=re.findall(r'\\label\{([^}]+)\}',s)
        refs+=re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',s)
        for target in re.findall(r'\\input\{([^}]+)\}',s):
            require(not Path(target).is_absolute() and '..' not in Path(target).parts,'external TeX input')
            queue.append(P/(target if target.endswith('.tex') else target+'.tex'))
    require(len(labels)==len(set(labels)),'duplicate native label')
    require(set(refs)<=set(labels),'unresolved native labels '+str(sorted(set(refs)-set(labels))))
    core=sorted(name for name in seen if name.startswith('core/'))
    require([int(Path(name).name.split('_',1)[0]) for name in core]==list(range(260,288)),
            'missing active proof body 260-287')
    require(len(M['unchanged_original_files'])==33,'incomplete original preservation map')
    require(M['full_raw_pointwise_LLT_proved'] is False and M['full_four_coordinate_inversion_completed'] is False,
            'misstated final theorem completion')
    print(json.dumps({'status':'passed','scope':'byte and native-structure check, not mathematical certification',
         'manifest_sha256':hashlib.sha256((P/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
         'required_files':len(M['current_files']),'required_diagnostic_programs':len(M['required_diagnostic_programs']),
         'active_numbered_proof_bodies':len(core),'native_tex_inputs':len(seen),'native_labels':len(labels),
         'unchanged_numbered_proofs':26,'unchanged_interfaces':7,'unresolved_labels':0,
         'all_historical_branches_independently_audited':False,'independent_proof_certificate':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
