"""Rebuild the two focused manuscripts from a minimal journal package only."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
import fitz

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def page_hashes(path):
    with fitz.open(path) as doc:
        return [{'page':i+1,'text_sha256':hashlib.sha256(p.get_text().encode()).hexdigest(),
                 'raster_sha256':hashlib.sha256(p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples).hexdigest()}
                for i,p in enumerate(doc)]
def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'JOURNAL_MANIFEST.json').read_text())
    require(manifest['schema']=='gtf63.journal-manifest/1','Wrong journal manifest')
    actual={str(p.relative_to(root/'source')) for p in (root/'source').rglob('*') if p.is_file()}
    require(actual==set(manifest['source_sha256']),'Unexpected journal source files')
    for name,value in manifest['source_sha256'].items():
        path=Path(name)
        require(not path.is_absolute() and '..' not in path.parts,'Unsafe source path')
        require(digest(root/'source'/path)==value,'Journal source digest mismatch: '+name)
    for item in manifest['documents'].values():
        require(digest(root/item['pdf'])==item['pdf_sha256'],'Published journal PDF mismatch')
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790467200',FORCE_SOURCE_DATE='1',TZ='UTC',PYTHONHASHSEED='0')
    with tempfile.TemporaryDirectory(prefix='gtf63-journal-only-') as temp:
        work=Path(temp)/'source';shutil.copytree(root/'source',work)
        for kind,item in manifest['documents'].items():
            for _ in range(3):
                result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',item['tex']],cwd=work,env=env,
                                      text=True,capture_output=True,timeout=180)
                require(result.returncode==0,'Journal typesetting failed: '+kind+'\n'+result.stdout[-6000:])
            stem=Path(item['tex']).stem;log=(work/(stem+'.log')).read_text(errors='replace')
            require(not re.search(r'(Reference|Citation).*undefined|There were undefined|Overfull \\[hv]box|Token not allowed in a PDF string',log),
                    'Journal typesetting warnings: '+kind)
            require(page_hashes(work/(stem+'.pdf'))==item['pages'],'Journal page text/raster mismatch: '+kind)
    print(json.dumps({'schema':'gtf63.journal-verification/1','status':'success','active_tex_files':len(actual),
                      'documents':list(manifest['documents']),'all_page_text_and_raster_equal':True,
                      'historical_sources_required':False,'repository_or_network_required':False},sort_keys=True))
if __name__=='__main__':main()
