#!/usr/bin/env python3
"""Compare two downloaded native artifacts; no author checker imported.
Usage: python compare_baseline.py BASELINE_ZIP CURRENT_ZIP
Checks both frozen manifests, exact inherited-path preservation, archived
originals and five statement bodies. It does not count semantic theorems.
"""
from pathlib import Path
import io,json,re,sys,zipfile,hashlib

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def load(path):
    raw=Path(path).read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as a:
        report=json.loads(a.read('build-report.json'))
        active=json.loads(a.read('active-source-manifest.json'))
        with zipfile.ZipFile(io.BytesIO(a.read('native-source.zip'))) as s:
            manifest=json.loads(s.read('SOURCE_MANIFEST.json'))
            files={n:s.read('source/'+n) for n in manifest['files']}
    for n,b in files.items():
        d=manifest['files'][n]
        require(len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256'],'Mismatch '+n)
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['git_blob'],'Blob mismatch '+n)
    return files,manifest,active,report,hashlib.sha256(raw).hexdigest()

def main():
    old,om,oa,orr,oh=load(sys.argv[1]);new,nm,na,nrr,nh=load(sys.argv[2])
    missing=sorted(set(old)-set(new));require(not missing,'Missing inherited files')
    changed=[n for n in old if old[n]!=new[n] or om['files'][n]['mode']!=nm['files'][n]['mode']]
    archives=[]
    for n in changed:
        p='history/v63-review-baseline/'+n
        require(p in new and new[p]==old[n], 'Absent/different original '+n)
        archives.append(p)
    ou=set().union(*(set(v) for v in oa.values()));nu=set().union(*(set(v) for v in na.values()))
    require(ou<=nu,'Lost active path')
    path='article/23f2_finite_experiment_analytic_inverse_v62.tex'
    pattern=rb'\\begin\{(lemma|theorem|corollary)\}.*?\\end\{\1\}'
    a=[m.group() for m in re.finditer(pattern,old[path],re.S)]
    b=[m.group() for m in re.finditer(pattern,new[path],re.S)]
    require(len(a)==5 and a==b,'Five finite-experiment statement bodies changed')
    require(old[path]==new[path], 'Complete finite-experiment module changed')
    require(old['article/25a_common_observables_v25.tex']==new['article/25a_common_observables_v25.tex'], 'Position-pilot module changed')
    res={'complete_statistical_module_identical':True,'position_pilot_identical':True,'baseline_source':orr['source_commit'],'current_source':nrr['source_commit'],'baseline_artifact_sha256':oh,'current_artifact_sha256':nh,'baseline_files_verified':len(old),'current_files_verified':len(new),'unchanged_inherited_files':len(old)-len(changed),'changed_inherited_files':sorted(changed),'archived_originals_verified':archives,'new_paths':sorted(set(new)-set(old)),'baseline_active_union':len(ou),'current_active_union':len(nu),'new_active_paths':sorted(nu-ou),'five_finite_experiment_statement_bodies_identical':True,'scope':'Byte/mode and syntactic statement-body comparison; not a semantic theorem census.'}
    print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__':main()
