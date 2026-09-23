#!/usr/bin/env python3
"""Assemble native v141 from the byte-verified native v140 tree and UTF-8 overlay."""
from pathlib import Path
import hashlib,json,re,shutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
P=ROOT/'papers/A2-v17-boundary-information-coarsening/article'
SRC=P/'v140';DST=P/'v141';OVERLAY=HERE/'overlay'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((SRC/'PROVENANCE_MANIFEST_V140.json').read_text())
for n,h in base['source_sha256'].items():
 p=SRC/n
 if not p.is_file() or sha(p)!=h:raise RuntimeError('Predecessor mismatch: '+n)
if DST.exists():raise RuntimeError('Refusing to overwrite an existing native v141 tree')
ignore=shutil.ignore_patterns('*.pdf','*.aux','*.log','*.out','*.toc','__pycache__','evidence')
shutil.copytree(SRC,DST,ignore=ignore)
changed={}
for p in sorted(OVERLAY.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or 'evidence' in p.relative_to(OVERLAY).parts:continue
 n=p.relative_to(OVERLAY);target=DST/n
 if target.exists() and target.read_bytes()!=p.read_bytes():
  archive=Path('history/v140')/n;(DST/archive).parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(target,DST/archive)
  changed[str(n)]={'archive':str(archive),'sha256':sha(target)}
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
def labels(root):
 seen=set();answer=[]
 def visit(n):
  if n in seen:return
  if Path(n).is_absolute() or '..' in Path(n).parts:raise RuntimeError(n)
  seen.add(n);text=(root/n).read_text();answer.extend(re.findall(r'\\label\{([^}]+)\}',text))
  for f in re.findall(r'\\input\{([^}]+)\}',text):visit(f)
 visit('complete.tex');return answer
inherited=labels(SRC);current=labels(DST)
assert len(inherited)==len(set(inherited))
assert set(inherited)<=set(current) and len(current)==len(set(current))
unchanged={}
for p in sorted(SRC.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or 'evidence' in p.relative_to(SRC).parts or p.suffix in ['.pdf','.aux','.log','.out','.toc']:continue
 n=str(p.relative_to(SRC))
 if n not in changed:
  assert (DST/n).is_file() and sha(DST/n)==sha(p),n
  unchanged[n]=sha(p)
nondeletion={'revision':141,'predecessor':'v140','all_inherited_labels':inherited,'inherited_label_count':len(inherited),'current_label_count':len(current),'changed_predecessor':changed,'unchanged_predecessor_sha256':unchanged,'deleted_predecessor_sources':[]}
(DST/'NONDELETION_V141.json').write_text(json.dumps(nondeletion,indent=2)+'\n')
m={'revision':141,'review_commit':'17e039fe55fc0d060b443d486421d937f637439a','reviewed_v140_head':'6bac73f9ebcaadcfa135e4960de19c93323bbfd7','native_predecessor_commit':'bf0d9be9e2624058d24a57c48b19ec4c38105c1f','predecessor_manifest_sha256':sha(SRC/'PROVENANCE_MANIFEST_V140.json'),'inherited_labels':inherited,'current_label_count':len(current),'changed_predecessor':changed,'unchanged_predecessor_sha256':unchanged,'inherited_check_sha256':{str(p.relative_to(SRC)):sha(p) for p in sorted((SRC/'checks').glob('*.py'))},'Ballico_1993_full_text_obtained':False,'exhaustive_priority_verified':False,'formal_proof_verified':False}
m['source_sha256']={str(p.relative_to(DST)):sha(p) for p in sorted(DST.rglob('*')) if p.is_file()}
(DST/'PROVENANCE_MANIFEST_V141.json').write_text(json.dumps(m,indent=2)+'\n')
(DST/'evidence').mkdir()
print(json.dumps({'native_directory':str(DST),'inherited_labels':len(inherited),'current_labels':len(current),'source_files':len(m['source_sha256']),'changed_predecessor_files':len(changed),'deleted_predecessor_sources':0},indent=2))
