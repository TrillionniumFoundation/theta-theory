#!/usr/bin/env python3
"""Check downloaded v71 evidence without importing manuscript diagnostic programs."""
from pathlib import Path
import hashlib,json,zipfile,re,argparse
import fitz
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--native-dir',type=Path,required=True)
parser.add_argument('--local-dir',type=Path,required=True)
parser.add_argument('--artifact',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
P=args.native_dir
LOCAL=args.local_dir

def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def obj(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree(node):
    parts=[]
    for name,v in sorted(node.items(),key=lambda kv:(kv[0]+('/' if isinstance(kv[1],dict) else '')).encode()):
        mode,identity=('40000',tree(v)) if isinstance(v,dict) else v
        parts.append(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(identity))
    return obj('tree',b''.join(parts))
frozen=json.loads((P/'frozen-source-manifest.json').read_text())
report=json.loads((P/'build-report.json').read_text())
check(report['status']=='passed' and not report['errors'],'Native build failed')
check(report['source_tree']=='8549bb0789d5e6cdce8ae12f70ed7c100f81510b','Source tree')
for name,entry in report['evidence_files'].items():
    b=(P/name).read_bytes();check(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'Evidence: '+name)
files=frozen['files'];nodes={}
with zipfile.ZipFile(P/'native-source.zip') as z:
    expected={'SOURCE_MANIFEST.json'}|{'source/'+n for n in files}
    check(set(z.namelist())==expected and len(z.namelist())==len(expected),'ZIP inventory')
    check(z.read('SOURCE_MANIFEST.json')==(P/'frozen-source-manifest.json').read_bytes(),'Manifest')
    for name,entry in files.items():
        i=z.getinfo('source/'+name);b=z.read(i)
        check(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'Source bytes: '+name)
        check(obj('blob',b)==entry['git_blob'],'Git blob: '+name)
        check(i.external_attr>>16==int(entry['mode'],8),'Raw mode: '+name)
        cur=nodes
        chunks=name.split('/')
        for c in chunks[:-1]:cur=cur.setdefault(c,{})
        cur[chunks[-1]]=(entry['mode'],entry['git_blob'])
    reviewed=json.loads(z.read('source/history/v70-review-baseline/SOURCE_MANIFEST.json'))['files']
    changed=[];same=[]
    for n,e in reviewed.items():
        check(n in files,'Removed inherited source: '+n)
        if files[n]==e:same.append(n)
        else:
            changed.append(n);archived='history/v70-review-baseline/'+n
            check(files[archived]==e,'Changed original was not archived exactly: '+n)
    root=tree(nodes);check(root==frozen['source_tree'],'Reconstructed Git tree')
pairs={}
for name in ('check_adaptive','check_revision_v32','check_revision_v38','check_revision_v71'):
    pairs[name]=(P/(name+'-normal.json')).read_bytes()==(P/(name+'-optimized.json')).read_bytes()
check(all(pairs.values()),'Normal/optimized outputs differ')
newdiag=json.loads((P/'check_revision_v71-normal.json').read_text())
for n in newdiag['source']['five_core_modules_unchanged']:check(n in same,'Core changed')
products={};comparisons={}
for entry in ('main','rigidity','two_collision'):
    b=(P/(entry+'.pdf')).read_bytes();r=report['entries'][entry]['product']
    check(len(b)==r['bytes'] and sha(b)==r['sha256'],'PDF digest')
    log=(P/(entry+'.log')).read_text()
    bad=re.findall(r'Overfull|LaTeX Error|Missing character:|There were undefined references|There were undefined citations|multiply defined',log)
    check(not bad,'Final-log failure')
    remote=fitz.open(P/(entry+'.pdf'));local=fitz.open(LOCAL/(entry+'.pdf'))
    check(len(remote)==len(local)==r['pages'],'Page count')
    different_text=[];different_rgb=[]
    for idx,(a,bpage) in enumerate(zip(remote,local),1):
        if a.get_text()!=bpage.get_text():different_text.append(idx)
        a1=a.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
        b1=bpage.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
        if (a1.width,a1.height,a1.samples)!=(b1.width,b1.height,b1.samples):different_rgb.append(idx)
    products[entry]={**r,'git_blob':obj('blob',b)}
    comparisons[entry]={'pages':len(remote),'different_text_pages':different_text,'different_rgb_pages_at_72_dpi':different_rgb,'pdf_bytes_equal':(P/(entry+'.pdf')).read_bytes()==(LOCAL/(entry+'.pdf')).read_bytes()}
result={
 'status':'passed','role':'author-side post-download verification; not an independent referee certification',
 'repository':'TrillionniumFoundation/theta-theory','revision_date':'2026-09-17',
 'review_commit':'f1d516c0033256d50ca23d87cc5a40fef8f72d45',
 'source_commit':report['source_commit'],'source_tree':root,
 'products_head':'5826d4abdd4c63c4c338422ef10b57d09dae6f20',
 'run_id':35133556116,'run_attempt':1,'artifact_id':10462291207,
 'artifact_sha256':sha(args.artifact.read_bytes()),
 'source_archive_sha256':sha((P/'native-source.zip').read_bytes()),
 'hash_listed_native_evidence_files_verified':len(report['evidence_files']),
 'source_files_bytes_blob_hashes_and_raw_modes_verified':len(files),
 'retention':{'inherited':len(reviewed),'unchanged':len(same),'changed_originals_byte_mode_exact':changed,'removed':[],
              'five_core_modules_unchanged':newdiag['source']['five_core_modules_unchanged'],
              'main_theorem_statements_unchanged':newdiag['source']['main_theorem_statements_unchanged'],
              'old_active_inputs_retained':newdiag['source']['old_active_union'],'current_active_inputs':newdiag['source']['active_union']},
 'products':products,'normal_optimized_pairs_identical':pairs,
 'final_log_failure_patterns':[], 'underfull_notices':{k:len(v['warnings']) for k,v in report['entries'].items()},
 'local_native_comparison':comparisons,'renderer':fitz.VersionBind,
 'comparison_scope':'Text and RGB comparison is automated and does not imply all-page visual or mathematical inspection.',
 'visual_inspection':{'status':'pending separate rendered-page inspection'},
 'does_not_certify':['all retained theorems','optimal rates','efficient reconstruction','exhaustive prior-art search','journal acceptance']}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
