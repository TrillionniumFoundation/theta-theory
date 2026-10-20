#!/usr/bin/env python3
"""Strict source/retained-proof gate; not a mathematical proof checker."""
from __future__ import annotations
import hashlib,json,re,zipfile
from pathlib import Path
from check_radial_source import restore_preserved_inventory
P=Path(__file__).resolve().parents[1]
def require(x,m):
    if not x: raise RuntimeError(m)
def identity_bytes(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def identity(p):return identity_bytes(p.read_bytes())
def main():
    M=json.loads((P/'SOURCE_MANIFEST.json').read_text())
    restore_presved=M.get('preserved_inventory_lossless_transport')
    require(restore_presved is True,'missing inherited transport commitment')
    restore_preserved_inventory(M)
    for name,expected in M['current_files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe path')
        require((P/name).is_file(),'missing required file '+name)
        require(identity(P/name)==expected,'changed required bytes '+name)
    require(M['full_raw_pointwise_LLT_proved'] is False and M['full_four_coordinate_inversion_completed'] is False,'unsupported completion flag')
    z=zipfile.ZipFile(P/'provenance/radial-frozen/native-source.zip')
    preserved=M['unchanged_original_files']
    require(len(preserved)==35,'incomplete 28+7 preservation map')
    for name,expected in preserved.items():
        raw=z.read('A2DYN-radial-native/'+name)
        require(identity_bytes(raw)['git_blob']==expected,'archive disagrees with frozen identity '+name)
        require((P/name).read_bytes()==raw,'inherited proof/interface changed '+name)
    core=[]
    for n in sorted(k for k in z.namelist() if '/core/' in k and k.endswith('.tex')):
        name=Path(n).name;raw=z.read(n);h=identity_bytes(raw)['git_blob']
        core.append(b'100644 '+name.encode()+b'\0'+bytes.fromhex(h))
    payload=b''.join(core)
    require(hashlib.sha1(b'tree '+str(len(payload)).encode()+b'\0'+payload).hexdigest()=='e189a16ded4a1913ba286d5b01f57e7e42c2eb72','predecessor core tree mismatch')
    require(identity(P/'provenance/REFEREE_REPORT_v115.md')['git_blob']=='9c68b0e8b31cd196c732514a29ebd44d95964243','governing report identity mismatch')
    queue=['main.tex'];seen=set();labels=[];refs=[]
    while queue:
        name=queue.pop()
        if name in seen:continue
        require(name in M['current_files'],'ungated TeX file '+name);seen.add(name)
        s=(P/name).read_text();require(not any(ord(c)<32 and c not in '\n\t\r' for c in s),'control character')
        s=re.sub(r'(?<!\\)%[^\n]*','',s)
        labels+=re.findall(r'\\label\{([^}]+)\}',s)
        refs+=re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',s)
        for target in re.findall(r'\\input\{([^}]+)\}',s):
            require(not Path(target).is_absolute() and '..' not in Path(target).parts,'unsafe TeX input')
            queue.append(target if target.endswith('.tex') else target+'.tex')
    require(len(labels)==len(set(labels)),'duplicate labels')
    require(set(refs)<=set(labels),'unresolved labels '+str(set(refs)-set(labels)))
    numbered=sorted(int(Path(n).name.split('_')[0]) for n in seen if n.startswith('core/'))
    require(numbered==list(range(260,290)),'missing current native proof body')
    require(len(M['required_diagnostic_programs'])==12,'missing diagnostic requirement')
    for name in M['required_diagnostic_programs']:require('tools/'+name+'.py' in M['current_files'],'ungated diagnostic')
    print(json.dumps({'status':'passed','manifest_sha256':hashlib.sha256((P/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
        'required_files':len(M['current_files']),'diagnostic_programs':12,'native_tex_inputs':len(seen),'native_labels':len(labels),
        'active_numbered_proofs':30,'unchanged_numbered_proofs':28,'unchanged_interfaces':7,'unresolved_labels':0,
        'baseline_core_tree_verified':True,'governing_report_blob_verified':True,
        'scope':'byte and native-structure verification only; not proof certification'},indent=2,sort_keys=True))
if __name__=='__main__':main()
