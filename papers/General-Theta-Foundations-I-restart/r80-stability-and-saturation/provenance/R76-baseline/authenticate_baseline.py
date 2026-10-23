#!/usr/bin/env python3
"""Authenticate the completed R75 source/publication as an R76 baseline."""
import datetime,hashlib,json,pathlib,re,subprocess
ROOT=pathlib.Path('/workspace/scratch/f856e3d63ac5'); REPO=ROOT/'theta-r76-work'; OUT=ROOT/'r76-audit'
SOURCE_SHA='bc2952aa9a9695fe9985d491a4156b8975024285'; PUBLICATION_SHA='2c103f924720435700e947cc8df31b8b648f61e9'
SOURCE_PATH='papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory'; SOURCE=REPO/SOURCE_PATH; PUB=pathlib.Path(str(SOURCE)+'-publication')
def require(c,m):
    if not c:raise ValueError(m)
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def ident(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}
def tree(sha,path):return git('rev-parse',sha+':'+path).decode().strip()
def inventory(sha,path):
    result=[]
    for line in git('ls-tree','-rz','--full-tree',sha,path).split(b'\0'):
        if not line:continue
        meta,p=line.split(b'\t',1);mode,kind,obj=meta.decode().split();require(kind=='blob','Unexpected object type')
        name=p.decode();data=(REPO/name).read_bytes();row=ident(data);require(row['git_blob']==obj,'Checked-out file does not match immutable Git tree: '+name)
        result.append({'path':name.removeprefix(path+'/'),'mode':mode,**row})
    return result
def main():
    source=inventory(SOURCE_SHA,SOURCE_PATH);pub=inventory(PUBLICATION_SHA,SOURCE_PATH+'-publication')
    require(len(source)==386 and len(pub)==64,'Baseline file count mismatch')
    manifest=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_text());require({r['path'] for r in source}=={r['path'] for r in manifest['files']}|{'SOURCE_MANIFEST.json'},'Source manifest membership mismatch')
    actual={r['path']:r for r in source}
    for row in manifest['files']:require(all(actual[row['path']][k]==row[k] for k in ('bytes','sha256','git_blob','mode')),'Source manifest bytes mismatch')
    require(tree(SOURCE_SHA,SOURCE_PATH)==tree(PUBLICATION_SHA,SOURCE_PATH)=='497886b8961cf12001bbea66909757f93bb8d1ee','Wrong source tree')
    require(git('rev-list','--parents','-n','1',PUBLICATION_SHA).decode().strip().split()==[PUBLICATION_SHA,SOURCE_SHA],'Publication is not sole-parent source child')
    identity=json.loads((PUB/'PUBLICATION_IDENTITY.json').read_text());receipt=json.loads((PUB/'BUILD_RECEIPT.json').read_text())
    require(identity['source_commit']==receipt['declared_source_commit']==SOURCE_SHA,'Stored execution source mismatch')
    require(receipt['status']=='PASS' and receipt['source_commit_verified'] and receipt['source_unchanged_during_build'],'Stored strict result incomplete')
    closures={}
    for name in ['main.tex','supplement.tex','companion-r58/main.tex']:
        base=SOURCE/('companion-r58' if name.startswith('companion-r58') else '');seen=set()
        def visit(path):
            rel=path.relative_to(SOURCE).as_posix()
            if rel in seen:return
            require(path.is_file(),'Missing native input '+rel);seen.add(rel)
            text=re.sub(r'(?<!\\)%[^\n]*','',path.read_text())
            for child in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',text):
                p=base/child
                if not p.suffix:p=p.with_suffix('.tex')
                visit(p)
        visit(SOURCE/name);closures[name]=sorted(seen)
    docs=[]
    for row in identity['documents']:
        p=PUB/row['file'];info=subprocess.check_output(['pdfinfo',str(p)]).decode();pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1));text=subprocess.check_output(['pdftotext','-layout',str(p),'-'])
        require(pages==row['pages'],'PDF page mismatch');require(ident(p.read_bytes())['sha256']==row['sha256'],'PDF hash mismatch');require(len(text)>1000,'PDF unreadable');text.decode('utf-8')
        docs.append({'file':row['file'],'pages':pages,**ident(p.read_bytes()),'fresh_text_bytes':len(text),'fresh_text_sha256':hashlib.sha256(text).hexdigest(),'first_text_lines':text.decode().splitlines()[:8],'fresh_native_build':False})
    report=(SOURCE/'provenance/R65_REFEREE_REPORT.md').read_bytes();require(ident(report)['git_blob']=='d1ff9c5662390156ee212c82b173e86a21180e84','Controlling report mismatch')
    require(git('rev-parse','358481b21ceeeedb1205ebd30f86982e32a2cb04:GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md').decode().strip()==ident(report)['git_blob'],'Report commit path mismatch')
    response=(SOURCE/'RESPONSE_TO_REFEREE.md').read_text();ids=re.findall(r'^### (R65-(?:17|18)\.\d+)\b',response,re.M);expected=['R65-17.'+str(i) for i in range(1,11)]+['R65-18.'+str(i) for i in range(1,41)]
    require(sorted(ids)==sorted(expected),'Response IDs incomplete or repeated')
    oldlock=json.loads((SOURCE/'provenance/R75-baseline/BASELINE_LOCK_R75.json').read_text());deps=oldlock['historical_dependencies']
    for d in deps:
        if 'path' in d:require(tree(d['commit'],d['path'])==d['tree'],'Historical dependency subtree mismatch')
        else:require(git('rev-parse',d['commit']+'^{tree}').decode().strip()==d['repository_tree'],'Historical dependency repository tree mismatch')
    result={'schema':'theta.r76.baseline-content-authentication.v1','status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':SOURCE_SHA,'publication_commit':PUBLICATION_SHA,'source_tree':tree(SOURCE_SHA,SOURCE_PATH),'publication_tree':tree(PUBLICATION_SHA,SOURCE_PATH+'-publication'),'source_files':source,'publication_files':pub,'native_input_closures':closures,'documents':docs,'stored_build_receipt':ident((PUB/'BUILD_RECEIPT.json').read_bytes()),'report':{'commit':'358481b21ceeeedb1205ebd30f86982e32a2cb04',**ident(report)},'response':{'ids':ids,**ident(response.encode())},'historical_dependencies':deps,'current_indexed_statements':manifest['current_indexed_statement_count'],'limits':['Fresh byte and native-input/PDF-readability authentication; does not rerun R75 theorem diagnostics or native compilation.','Stored strict PASS is authenticated at its exact source; not a new R76 PASS.','Deposited referee identity, journal commission and editorial approval not independently verified.']}
    (OUT/'BASELINE_CONTENT_AUTHENTICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print({'status':result['status'],'source_files':len(source),'publication_files':len(pub),'native_closure_sizes':{k:len(v) for k,v in closures.items()},'pages':[r['pages'] for r in docs],'response_ids':len(ids),'historical_dependencies':len(deps)})
if __name__=='__main__':main()
