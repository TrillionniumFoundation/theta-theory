#!/usr/bin/env python3
"""Independent delivery audit. Requires PyMuPDF; takes artifact ZIP and rebuild directory.
It checks reproducibility, not correctness of mathematical assertions.
"""
from pathlib import Path
import hashlib, json, re, sys, zipfile, tempfile
import fitz

def digest(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree_sha(node):
    entries=[]
    for name,value in node.items():
        if isinstance(value,dict): mode,sha,key='40000',tree_sha(value),name+'/'
        else: mode,sha=value;key=name
        entries.append((key.encode(),mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
    raw=b''.join(x[1] for x in sorted(entries))
    return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def check(condition,msg):
    if not condition: raise ValueError(msg)
def main():
    zpath=Path(sys.argv[1]); rebuilt=Path(sys.argv[2]); out=Path(sys.argv[3])
    with tempfile.TemporaryDirectory() as td:
        a=Path(td)
        with zipfile.ZipFile(zpath) as z:
            for name in z.namelist(): check(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe ZIP path')
            z.extractall(a)
        fm=json.loads((a/'frozen-source-manifest.json').read_text())
        am=json.loads((a/'active-source-manifest.json').read_text())
        with zipfile.ZipFile(a/'native-source.zip') as nz:
            data={name.removeprefix('source/'):nz.read(name) for name in nz.namelist() if not name.endswith('/') and name!='SOURCE_MANIFEST.json'}
        # Native ZIP also includes top-level metadata, deliberately outside the tracked source tree.
        check(set(data)==set(fm['files']),'source ZIP/manifest path mismatch')
        tree={}
        for path,m in fm['files'].items():
            b=data[path]
            check(len(b)==m['bytes'] and digest(b)==m['sha256'] and blob(b)==m['git_blob'],f'source mismatch: {path}')
            ptr=tree
            pp=Path(path).parts
            for part in pp[:-1]:ptr=ptr.setdefault(part,{})
            ptr[pp[-1]]=(m['mode'],m['git_blob'])
        tsha=tree_sha(tree);check(tsha==fm['source_tree'],'source Git subtree mismatch')
        for entry,files in am.items():
            for path,m in files.items():
                b=data[path];check(digest(b)==m['sha256'] and blob(b)==m['git_blob'],f'active source mismatch: {entry}/{path}')
        unions=set().union(*(set(x) for x in am.values()))
        bm=json.loads((a/'build-report.json').read_text())
        products={}
        for entry in ['two_collision','main','rigidity']:
            native=fitz.open(a/(entry+'.pdf'));other=fitz.open(rebuilt/(entry+'.pdf'))
            check(len(native)==len(other),f'page count mismatch: {entry}')
            tm=[];rm=[]
            for i in range(len(native)):
                if native[i].get_text()!=other[i].get_text():tm.append(i+1)
                x=native[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                y=other[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
                if (x.width,x.height,x.samples)!=(y.width,y.height,y.samples):rm.append(i+1)
            nb=(a/(entry+'.pdf')).read_bytes();rb=(rebuilt/(entry+'.pdf')).read_bytes()
            products[entry]={'pages':len(native),'native_sha256':digest(nb),'rebuilt_sha256':digest(rb),'byte_identical':nb==rb,
              'text_mismatch_pages':tm,'rgb_72dpi_mismatch_pages':rm}
        # Report explicit external theorem occurrences, irrespective of whether a label is in a proof.
        aliases=re.findall(r'\\vFullAlias\{([^}]+)\}',data['journal/full_reference_routes_v56.tex'].decode())
        ext={k:[] for k in aliases}
        for path in am['rigidity']:
            text=data[path].decode()
            for n,line in enumerate(text.splitlines(),1):
                for key in aliases:
                    if key in line and path!='journal/full_reference_routes_v56.tex':ext[key].append({'path':path,'line':n,'text':line.strip()})
        result={'scope':'Independent frozen-source, active-input, native-vs-rebuild audit; not a mathematical certificate.',
          'source_commit':fm['source_commit'],'source_tree':tsha,'artifact_id':10389393610,
          'artifact_sha256':digest(zpath.read_bytes()),'frozen_files_verified':len(data),
          'source_inputs_by_entry':{k:len(v) for k,v in am.items()},'unique_active_source_inputs':len(unions),
          'full_and_companion_unique_sources':len(set(am['main'])|set(am['two_collision'])),
          'products':products,'all_page_comparison_renderer':{'library':'PyMuPDF','version':fitz.VersionBind,'dpi':72,'colorspace':'RGB','alpha':False},
          'external_comparison_labels':ext,'limitations':['No proof-correctness conclusion follows from these checks.',
          'All-page computational comparison is not all-page visual review.','No PDF byte identity is assumed.']}
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='external_comparison_labels'},indent=2))
if __name__=='__main__':main()
