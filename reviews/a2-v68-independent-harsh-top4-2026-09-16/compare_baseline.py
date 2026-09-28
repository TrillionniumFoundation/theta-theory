#!/usr/bin/env python3
"""Independent byte/mode comparison of v67 and v68 native source archives.
Usage: python compare_baseline.py BASELINE_WORKFLOW_ZIP CURRENT_WORK_ROOT
The current root must contain artifact/native-source.zip. No author code is used.
"""
from pathlib import Path
from io import BytesIO
import hashlib,json,sys,zipfile


def require(ok,msg):
    if not ok: raise RuntimeError(msg)


def h(data,kind='sha256'): return hashlib.new(kind,data).hexdigest()

def inspect(z):
    manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
    blobs={}; mode_mismatches=[]
    for name,record in manifest['files'].items():
        path='source/'+name; data=z.read(path)
        require(len(data)==record['bytes'] and h(data)==record['sha256'], 'File integrity: '+name)
        blob=h(b'blob '+str(len(data)).encode()+b'\0'+data,'sha1')
        require(blob==record['git_blob'],'Blob integrity: '+name)
        mode=z.getinfo(path).external_attr>>16
        if mode!=int(record['mode'],8):
            mode_mismatches.append({'path':name,'zip_mode':oct(mode),'recorded_git_mode':record['mode']})
        blobs[name]=data
    return manifest,blobs,mode_mismatches


def main():
    base,root=Path(sys.argv[1]),Path(sys.argv[2])
    with zipfile.ZipFile(base) as outer:
        ba=json.loads(outer.read('active-source-manifest.json'))
        with zipfile.ZipFile(BytesIO(outer.read('native-source.zip'))) as z: bm,bb,bmode=inspect(z)
    with zipfile.ZipFile(root/'artifact/native-source.zip') as z: cm,cb,cmode=inspect(z)
    ca=json.loads((root/'artifact/active-source-manifest.json').read_text())
    changed=[];same=0
    for name,data in bb.items():
        require(name in cb,'Lost baseline path '+name)
        require(bm['files'][name]['mode']==cm['files'][name]['mode'],'Changed mode '+name)
        if data==cb[name]:same+=1
        else:
            archived='history/v67-review-baseline/'+name
            require(cb.get(archived)==data,'Missing byte-exact original: '+name)
            changed.append(name)
    bu=set().union(*(set(v) for v in ba.values()));cu=set().union(*(set(v) for v in ca.values()))
    require(bu<=cu,'Lost inherited active inputs')
    report={'baseline_files_verified':len(bb),'current_files_verified':len(cb),
            'unchanged_in_place':same,'modified_with_exact_archives':changed,
            'new_source_paths':sorted(set(cb)-set(bb)),
            'baseline_active_union':len(bu),'current_active_union':len(cu),
            'new_active_paths':sorted(cu-bu),'all_inherited_modes_unchanged':True,
            'raw_zip_mode_mismatches':{'baseline':bmode,'current':cmode},
            'source_modes':'Git tree is reconstructed using the manifest modes; ZIP headers differ at listed paths.',
            'imports_author_checker':False}
    (root/'SOURCE_DIFF.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
