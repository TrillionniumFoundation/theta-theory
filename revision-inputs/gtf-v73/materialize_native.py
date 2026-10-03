#!/usr/bin/env python3
"""One-time, hash-pinned native source transfer before manuscript qualification.

This is transport, not proof evidence. No previous paper path is modified.
"""
from pathlib import Path, PurePosixPath
import hashlib,json,lzma,os,re,subprocess,zipfile

BRANCH='revision/general-theta-foundations-i-v73-noisy-readout-crossover-2026-10-04'
PREFIX='papers/GTF-I-v73-noisy-readout-crossover'
BASE='papers/GTF-I-v72-varying-readout'

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def safe(name):
    p=PurePosixPath(name)
    require(not p.is_absolute() and bool(p.parts) and '..' not in p.parts and str(p)==name,'unsafe source path')
    require(p.suffix in {'.tex','.py','.json','.md'},'unexpected native source type')
    return name

def reconstruct(repo,transfer):
    manifest=json.loads((transfer/'TRANSFER_MANIFEST.json').read_text())
    parts=[]
    for item in manifest['parts']:
        n=item['path'];require(PurePosixPath(n).name==n,'unsafe part path')
        b=(transfer/n).read_bytes();require(len(b)==item['size'] and sha(b)==item['sha256'],'transfer part mismatch: '+n);parts.append(b)
    zipped=b''.join(parts);require(sha(zipped)==manifest['delta_xz_sha256'],'compressed delta mismatch')
    data=lzma.decompress(zipped);require(len(data)<2000000 and sha(data)==manifest['delta_json_sha256'],'decoded delta mismatch')
    change=json.loads(data);require(change['schema']=='gtf73.native-delta/1' and change['base_commit']==manifest['base_commit'],'wrong delta base/schema')
    path=repo/BASE/'evidence/NATIVE_SOURCE.zip';require(sha(path.read_bytes())==manifest['base_native_zip_sha256'],'predecessor native ZIP mismatch')
    with zipfile.ZipFile(path) as z:
        require(len(set(z.namelist()))==len(z.namelist()),'duplicate predecessor source')
        old={safe(n):z.read(n) for n in z.namelist()}
    source=dict(old)
    for name,oldname in change['copied_predecessor_paths'].items():
        source[safe(name)]=old[safe(oldname)]
    for name,text in change['files'].items():
        require(type(text) is str,'native file must be UTF-8 text');source[safe(name)]=text.encode()
    def graph(entry,seen=None):
        seen=set() if seen is None else seen
        entry=str(PurePosixPath(entry).with_suffix('.tex'));require(entry not in seen,'duplicate/recursive predecessor input');seen.add(entry)
        text=old[entry].decode();labels=re.findall(r'\\label\{([^}]+)\}',text)
        for sub in re.findall(r'\\input\{([^}]+)\}',text):labels+=graph(sub,seen)[1]
        return seen,labels
    preserve=dict(change['generated_preservation']);preserve['files']={n:sha(b) for n,b in sorted(old.items())}
    preserve['prior_proof_graphs']={n:{'files':sorted(graph(n)[0]),'labels':sorted(graph(n)[1])} for n in ['quantitative.tex','structural.tex','main.tex']}
    preserve['prior_labels']=sorted(set(graph('main.tex')[1]))
    pb=(json.dumps(preserve,indent=2,sort_keys=True)+'\n').encode()
    require(sha(pb)==change['generated_preservation_sha256'],'generated preservation inventory differs')
    source['PRESERVATION_MANIFEST.json']=pb
    inventory={n:sha(b) for n,b in sorted(source.items())}
    digest=sha((json.dumps(inventory,indent=2,sort_keys=True)+'\n').encode())
    require(len(source)==change['native_source_count']==manifest['source_files'] and digest==change['native_inventory_sha256']==manifest['native_inventory_sha256'],'native source inventory mismatch')
    root=repo/PREFIX;root.mkdir(parents=True,exist_ok=True)
    for n,b in source.items():
        dest=root/n;dest.parent.mkdir(parents=True,exist_ok=True);require(not dest.is_symlink(),'source symlink');dest.write_bytes(b)
    actual={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and p.suffix in {'.tex','.py','.json','.md'} and not set(p.relative_to(root).parts)&{'build','evidence','__pycache__','.git'}}
    require(actual==inventory,'extra or altered native files after transfer')
    return {'native_files':len(source),'native_inventory_sha256':digest,'predecessor_files':len(old),'preserved_labels':len(preserve['prior_labels']),'transfer_sha256':manifest['delta_xz_sha256']}

def main():
    repo=Path(os.environ['GITHUB_WORKSPACE']);transfer=repo/'revision-inputs/gtf-v73'
    def git(*a):return subprocess.check_output(['git',*a],cwd=repo,text=True).strip()
    trigger=os.environ['GITHUB_SHA'];require(os.environ['GITHUB_REF']=='refs/heads/'+BRANCH,'wrong branch')
    require(git('rev-parse','HEAD')==trigger,'wrong triggering checkout')
    require(git('ls-remote','--heads','origin','refs/heads/'+BRANCH).split()[0]==trigger,'remote moved; refusing native transfer')
    require(not git('status','--porcelain','--untracked-files=no'),'dirty tracked checkout')
    result=reconstruct(repo,transfer)
    for name in git('diff','--name-only').splitlines():require(name.startswith(PREFIX+'/'),'transfer altered a predecessor path')
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    subprocess.run(['git','add',PREFIX],cwd=repo,check=True)
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=repo).returncode:
        subprocess.run(['git','commit','-m','feat(gtf-i): materialize complete v73 noise-uniform proofs and exact rational codec'],cwd=repo,check=True)
        subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=repo,check=True)
    source=git('rev-parse','HEAD')
    result.update(source_commit=source,workflow_trigger=trigger,branch=BRANCH,qualification='not yet run')
    (Path(os.environ['RUNNER_TEMP'])/'gtf73-native-transfer.json').write_text(json.dumps(result,indent=2)+'\n')
    with open(os.environ['GITHUB_OUTPUT'],'a') as out:out.write('source='+source+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
