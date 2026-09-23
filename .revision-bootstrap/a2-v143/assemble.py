#!/usr/bin/env python3
"""Deterministically materialize native A2 v143 from the pinned v142 tree."""
from pathlib import Path
import base64,gzip,hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[2]
PIN='4deb7a35f4488a0c8b686261569ce4ef324ca750'
TREE='5dbfd6fdf6b7ad07c4f4dbba571249dac26857e5'
PREFIX='papers/A2-v17-boundary-information-coarsening/article'
OLD=ROOT/PREFIX/'v142';NEW=ROOT/PREFIX/'v143'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse',PIN+':'+PREFIX+'/v142'],cwd=ROOT,text=True).strip()==TREE
subprocess.run(['git','diff','--exit-code',PIN,'--',PREFIX+'/v142'],cwd=ROOT,check=True)
expected=['428349a168cd66e54ca15177bd627e765987690b','8fd14436fab45413ab0e75d35f03bb9bb0298835','a42093f0ee0622ed5332c7bd3ae5c0274c7f0acd','7d39fb83590a29317f9602dccaba78f89bdfca1b']
chunks=[]
for i in range(1,5):
 b=(Path(__file__).parent/f'payload-{i}.b64').read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected[i-1]
 chunks.append(b.decode().strip())
# Correct two identified transport transcription slips before the immutable
# gzip checksum and every reconstructed native file checksum are verified.
assert chunks[0].count('HPT9fpQI')==1 and chunks[0].count('TzrFFgZs0DX')==1
chunks[0]=chunks[0].replace('HPT9fpQI','HPT9fjQI').replace('TzrFFgZs0DX','TzrFFgZ0DX')
raw=base64.b64decode(''.join(chunks),validate=True)
assert sha(raw)=='87b12e243ad4b55b6ee35fc9070885a380dc24ec8a190c0db56ba0e1efdaf027'
patch=json.loads(gzip.decompress(raw));assert patch['schema']==1 and patch['predecessor']==PIN
assert not NEW.exists(), 'Do not overwrite an existing native revision'
shutil.copytree(OLD,NEW,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copytree(OLD,NEW/'history/v142',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.rmtree(NEW/'evidence',ignore_errors=True)
for p in NEW.iterdir():
 if p.is_file() and p.suffix in {'.pdf','.aux','.out','.log','.toc','.fls','.fdb_latexmk'}:p.unlink()
for name in ['PROVENANCE_MANIFEST.json','PROVENANCE_MANIFEST.md']:(NEW/name).unlink(missing_ok=True)
for name,record in patch['files'].items():
 rel=Path(name);assert not rel.is_absolute() and '..' not in rel.parts
 if 'text' in record:text=record['text']
 else:
  br=Path(record['base']);assert not br.is_absolute() and '..' not in br.parts
  b=(OLD/br).read_bytes();assert sha(b)==record['base_sha256'],str(br)
  lines=b.decode('utf-8').splitlines(True)
  text=''.join(''.join(lines[x[0]:x[1]]) if isinstance(x,list) else x for x in record['ops'])
 assert sha(text.encode())==record['sha256'],name
 p=NEW/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
(NEW/'NATIVE_DELTA_V143.json').write_text(json.dumps({'predecessor':PIN,'transport_sha256':sha(raw),'native_file_sha256':{k:v['sha256'] for k,v in patch['files'].items()}},indent=2)+'\n')
archive=ROOT/'revisions/a2-v143/history';archive.mkdir(parents=True,exist_ok=True)
for name in ['README.md','CURRENT_REVIEW_ENTRY.md']:shutil.copy2(ROOT/name,archive/('ROOT_'+name))
(ROOT/'CURRENT_REVIEW_ENTRY.md').write_text('# Current A2 revision: 143\n\nNative manuscript: `'+PREFIX+'/v143/geometry.tex`.\n\nThe controlling report is the second v141 report at `3afecca5e65d7fe9c6784020ea6e813122938140`, reviewing `8cd389f4048a1047be9aa8e8e4f642595175a555`. The v142 predecessor is `'+PIN+'`.\n\nBuild publication is pending. The subsequent source-bound SOURCE_LOCK_V143.json and BUILD_RECEIPT_V143.json will identify the exact native source SHA and generated PDFs. No prior receipt certifies this source.\n')
(ROOT/'README.md').write_text('# Theta-Theory — A2 revision 143\n\nThe canonical entry is [CURRENT_REVIEW_ENTRY.md](CURRENT_REVIEW_ENTRY.md).\n\nThe native manuscript **Finite failure schemes and the reconstruction of quadratic pencils** and its complete technical supplement are in ['+PREFIX+'/v143]('+PREFIX+'/v143/README.md). The exact source commit and build result are identified by the canonical entry, not by a moving branch name.\n\nAll predecessor mathematics and review branches are preserved. The earlier root routing files are archived in [revisions/a2-v143/history](revisions/a2-v143/history).\n')
print('Materialized',len(patch['files']),'verified native delta files; preserved the complete v142 source archive.')
