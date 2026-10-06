#!/usr/bin/env python3
"""Create v92 from the exact published v91 native tree without altering it."""
from pathlib import Path
import argparse, base64, gzip, hashlib, importlib.util, json, re, shutil

p=argparse.ArgumentParser()
p.add_argument('--source',default='papers/GTF-I-v91-reset-variational')
p.add_argument('--dest',default='papers/GTF-I-v92-rank-memory')
p.add_argument('--patch',default=str(Path(__file__).parent/'patch'))
a=p.parse_args()
src=Path(a.source).resolve(); dst=Path(a.dest).resolve(); patch=Path(a.patch).resolve()
if dst.exists():raise RuntimeError('refusing to overwrite an existing native revision')
if not patch.exists():
    # Repair exactly the identified three-character transcription defect before
    # digest verification. The corrected transport is committed with the native
    # source. Unknown mutations are never accepted or guessed.
    last=Path(__file__).parent/'payload-3.b64'
    text=last.read_text().strip();data=text.encode()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if digest=='e639497499d7906a92246ab4cffbe74b46cf4542':
        text=text.replace('FRZFZFxxz0','FRZFxxz0').replace('7/aQDTa/c','7/aDTa/c')
        data=text.encode()
        if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!='6cd39c317a0a5e3559ef9cb6c0a6a558f7f514e8':
            raise RuntimeError('transport normalization failed')
        last.write_text(text)
    packed=base64.b64decode(''.join((Path(__file__).parent/f'payload-{i}.b64').read_text().strip() for i in range(4)),validate=True)
    if hashlib.sha256(packed).hexdigest()!='38dbfcb4d5a526f49f0414243882c0f859d49b8faad3b5505cd7fd31cff52689':raise RuntimeError('revision payload digest mismatch')
    entries=json.loads(gzip.decompress(packed))
    for name,item in entries.items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('unsafe payload entry')
        if 'text' in item:text=item['text']
        else:
            base=Path(item['base'])
            if base.is_absolute() or '..' in base.parts:raise RuntimeError('unsafe base path')
            lines=(src/base).read_text().splitlines(keepends=True)
            for lo,hi,replacement in reversed(item['edits']):lines[lo:hi]=[replacement]
            text=''.join(lines)
        if hashlib.sha256(text.encode()).hexdigest()!=item['sha256']:raise RuntimeError('expanded file digest mismatch: '+name)
        target=patch/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
spec=importlib.util.spec_from_file_location('v91_build',src/'build_revision.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
inv=b.sources(src)
b.require(inv==json.loads((src/'evidence/SOURCE_HASHES.json').read_text()),'v91 complete native inventory differs')
for name in inv:
    target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,target)
baseline={'commit':'ce2616a9f5d870d5cf4c8ee254a728544a0bea6a',
          'source_commit':'e7ea7aa87c77d79119fe9f4cad273ac97997089e','files':inv,'graphs':{}}
for entry in b.DOCS:
    files,labels=b.graph(src,entry);baseline['graphs'][entry]={'files':sorted(files),'labels':sorted(labels)}
b.put(dst/'V91_BASELINE.json',baseline)
def put(name,text):
    target=dst/name
    if name in inv and (src/name).read_text()!=text:
        backup=dst/'predecessor-v91-audit'/name
        if not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,backup)
        elif backup.read_bytes()!=(src/name).read_bytes():raise RuntimeError('predecessor copy collision: '+name)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
for f in sorted(patch.rglob('*')):
    if f.is_file() and f.name!='source_check92.txt':put(f.relative_to(patch).as_posix(),f.read_text())
section='sections/85-rank-resolved-reset-memory'
for entry in ('main.tex','quantitative.tex'):
    text=(src/entry).read_text()
    anchor='\\input{sections/84-equal-prior-memory-hierarchy}'
    b.require(text.count(anchor)==1,'new section insertion anchor missing')
    text=text.replace(anchor,anchor+'\n\\input{'+section+'}')
    if entry=='quantitative.tex':
        text=text.replace('operational-introduction91','operational-introduction92').replace('current-comparison91','current-comparison92').replace('bibliography91','bibliography92')
        text=text.replace('These results require neither a symmetric ensemble nor a special prior.',r'''Rank-bounded atom domains resolve the dimensions of the complete old
receiver and the fresh reference at the reset cut, without enlarging
either by purification.  The resulting attained primal and dual
characterize every pair of these dimensions.  For the basis experiment
and equal priors their exact value is
$1/2+t^2(dr-1)/(2dr(d+1))$, where $r$ is the smaller dimension;
every adjacent increase of $r$ gives a strict gain when $t>0$.
The rank-envelope principle requires neither a symmetric ensemble
nor a special prior.''')
    else:
        text=text.replace('\\end{abstract}',r'''We also obtain attained rank-constrained variational formulas for both
retained receiver dimensions and determine every level of this two-cut
hierarchy on the same finite basis experiment, with strict adjacent
gains and finite attaining instruments.
\end{abstract}''')
    put(entry,text)
build=(src/'build_revision.py').read_text()
start=build.index('def check_source():');end=build.index('def source_commit_inventory(',start)
build=build[:start]+(patch/'source_check92.txt').read_text()+build[end:]
build=build.replace("BASE='906e6e12841816f07e4ca31137690fd18bb65853'", "BASE='ce2616a9f5d870d5cf4c8ee254a728544a0bea6a'")
build=build.replace('gtf91','gtf92').replace('v91 build','v92 build').replace('Source-bound v91','Source-bound v92').replace('GENERAL_THETA_FOUNDATIONS_I_V91_','GENERAL_THETA_FOUNDATIONS_I_V92_')
build=re.sub(r'NEW_SECTIONS=.*\n',"NEW_SECTIONS=['"+section+".tex']\n",build,count=1)
labels=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(dst/(section+'.tex')).read_text())
build=re.sub(r'NEW_LABELS=.*\n','NEW_LABELS='+repr(labels)+'\n',build,count=1)
build=build.replace("'rigidity_check.py')","'rigidity_check.py','rank_hierarchy_check.py')")
put('build_revision.py',build)
put('journal_verify.py',(src/'journal_verify.py').read_text().replace('gtf91','gtf92').replace('v91','v92'))
status=json.loads((dst/'PROOF_STATUS.json').read_text());status['new_labels']=labels
put('PROOF_STATUS.json',json.dumps(status,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'staged','destination':str(dst),'base_native_files':len(inv),'new_theorems':labels},indent=2))
