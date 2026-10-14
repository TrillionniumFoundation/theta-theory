#!/usr/bin/env python3
"""Fail-closed source/TeX/provenance checks; not a mathematical proof checker."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
class AuditFailure(RuntimeError):pass
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):
    # Retained historical manifests are ordinary source inputs; only the outer manifest is excluded.
    ans={}
    for p in sorted(root.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(root)
        if any(x in {'artifacts','evidence','__pycache__','.build'} for x in rel.parts):continue
        if rel.as_posix()=='SOURCE_MANIFEST.json' or p.suffix=='.pyc':continue
        if p.is_symlink():raise AuditFailure('source symlink not permitted: '+str(rel))
        ans[rel.as_posix()]={'sha256':digest(p),'bytes':p.stat().st_size}
    return ans
def tex_audit(root):
    root=root.resolve();seen=set();stack=[];alltext=[]
    def walk(rel):
        p=(root/rel).resolve()
        if root not in p.parents:raise AuditFailure('escaping TeX input: '+str(rel))
        if not p.is_file():raise AuditFailure('missing TeX input: '+str(rel))
        if p in stack:raise AuditFailure('cyclic TeX input')
        if p in seen:return
        stack.append(p);seen.add(p)
        text=re.sub(r'(?<!\\)%[^\n]*','',p.read_text())
        if re.search(r'\\(?:write18|openout)\b',text):raise AuditFailure('unexpected TeX output primitive')
        alltext.append(text)
        for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',text):
            if not name.endswith('.tex'):name+='.tex'
            walk(name)
        stack.pop()
    walk('main.tex');text='\n'.join(alltext)
    labels=Counter(re.findall(r'\\label\{([^}]+)\}',text))
    refs=re.findall(r'\\(?:ref|eqref|pageref|autoref|nameref)\{([^}]+)\}',text)
    bibs=Counter(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    cites=[key.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text) for key in group.split(',')]
    errors=[]
    for what,counts in [('label',labels),('bibliography key',bibs)]:
        errors.extend('duplicate '+what+': '+k for k,v in counts.items() if v!=1)
    errors.extend('undefined reference: '+r for r in sorted(set(refs)-set(labels)))
    errors.extend('undefined citation: '+r for r in sorted(set(cites)-set(bibs)))
    if errors:raise AuditFailure('; '.join(errors))
    return {'tex_files':len(seen),'labels':len(labels),'references':len(refs),'bibliography_entries':len(bibs),'citations':len(cites),'unused_labels':sorted(set(labels)-set(refs)),'input_sha256':hashlib.sha256('\n'.join(str(p.relative_to(root))+':'+digest(p) for p in sorted(seen)).encode()).hexdigest()}
def verify(root=ROOT,require_manifest=True):
    actual=inventory(root)
    if require_manifest:
        expected=json.loads((root/'SOURCE_MANIFEST.json').read_text())['files']
        if actual!=expected:
            missing=sorted(set(expected)-set(actual));extra=sorted(set(actual)-set(expected))
            changed=sorted(k for k in set(actual)&set(expected) if actual[k]!=expected[k])
            raise AuditFailure(f'manifest mismatch: missing={missing}, extra={extra}, changed={changed}')
    provenance=json.loads((root/'PROVENANCE.json').read_text())
    for row in provenance['retained_files']:
        if digest(root/row['local_path'])!=row['sha256']:raise AuditFailure('retained source changed: '+row['local_path'])
    for row in provenance['review_inputs']+provenance['control_inputs']:
        if digest(root/row['local_path'])!=row['sha256']:raise AuditFailure('pinned input changed: '+row['local_path'])
    return {'status':'PASS','source_files':len(actual),'native':tex_audit(root),'companion':tex_audit(root/'retained/r58-native'),'retained_files_verified':len(provenance['retained_files']),'pinned_inputs_verified':len(provenance['review_inputs'])+len(provenance['control_inputs']),'limitations':'Structural source, labels, citations and identity checks only; no claim of mathematical validity.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--seal',action='store_true');a=p.parse_args()
    if a.seal:
        verify(ROOT,False)
        (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps({'schema':1,'files':inventory(ROOT)},indent=2,sort_keys=True)+'\n')
    print(json.dumps(verify(),indent=2,sort_keys=True))
if __name__=='__main__':main()
