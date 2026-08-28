#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,gzip,hashlib,json,shutil,tarfile,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2];REP=H/'sources'/'reports';MAN=R/'provenance/cm2-unified-tree-2026-08-28/source-manifest.json';IDX=R/'canonical/CM2_UNIFIED_TREE_INDEX.md';BASE=R/'canonical'/'CM2_无条件攻坚_Canonical_Latest-Wins_非递归单一总卷_through_r63bd_2026-08-26.md';INT=H/'sources/intermediate/CM2_v74_intermediate_sources.md';REC=H/'sources/reconstructed/CM2_missing_stages_RECONSTRUCTED.md'
def sh(b):return hashlib.sha256(b).hexdigest()
def gh(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def archive(m):
 a=m['local_library_exact_report_archive'];d=R/a['parts_dir'];ps=sorted(d.glob(a['part_glob']))
 if len(ps)!=a['part_count']:raise RuntimeError('archive part count')
 b=base64.b64decode(''.join(p.read_text().strip() for p in ps),validate=True)
 if len(b)!=a['decoded_bytes'] or sh(b)!=a['decoded_sha256']:raise RuntimeError('archive hash')
 return b
def unpack(b,d):
 d.mkdir(parents=True,exist_ok=True)
 with tarfile.open(fileobj=gzip.GzipFile(fileobj=__import__('io').BytesIO(b)),mode='r:') as tf:
  for x in tf.getmembers():
   p=Path(x.name)
   if x.issym() or x.islnk() or p.is_absolute() or '..' in p.parts or not x.isfile():raise RuntimeError('unsafe archive member')
  tf.extractall(d,filter='data')
def verify(tmp):
 m=json.loads(MAN.read_text())
 for e in m['remote_pr_exact_sources']:
  b=(R/e['path']).read_bytes()
  if (gh(b),len(b))!=(e['git_blob_sha1'],e['bytes']):raise RuntimeError('remote pin '+e['path'])
 b=archive(m);unpack(b,tmp)
 for e in m['local_library_sources']:
  if 'archive_member' in e:p=tmp/e['archive_member'];z=p.read_bytes()
  else:
   p=R/e['path'];z=p.read_bytes()
   if 'embedded_filename' in e:
    tag=e['embedded_filename'].encode();pos=z.find(tag);s=z.find(b'\n',pos)+1;end=z.find(b'<!-- END ',s);z=z[s:end]
    if z.endswith(b'\n') and len(z)==e['bytes']+1:z=z[:-1]
  if len(z)!=e['bytes'] or sh(z)!=e['sha256']:raise RuntimeError('local source '+e.get('archive_member',e.get('embedded_filename',e.get('path','?'))))
 return m
def dtar(o,items):
 with o.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as z:
   with tarfile.open(fileobj=z,mode='w',format=tarfile.PAX_FORMAT) as tf:
    for p,a in sorted(items,key=lambda x:x[1]):
     i=tf.gettarinfo(str(p),arcname=a);i.uid=i.gid=0;i.uname=i.gname='';i.mtime=0;i.mode=0o644
     with p.open('rb') as f:tf.addfile(i,f)
def build(o):
 if o.exists():shutil.rmtree(o)
 o.mkdir(parents=True)
 with tempfile.TemporaryDirectory() as d:
  x=Path(d);m=verify(x)
  order=[R/e['path'] for e in m['remote_pr_exact_sources']]
  local=[]
  for e in m['local_library_sources']:
   if 'archive_member' in e:local.append(x/e['archive_member'])
   elif e.get('stage')=='v75V2':local.append(R/e['path'])
  paths=[IDX,BASE]+order+local+[INT,REC,MAN];uniq=[]
  for p in paths:
   if p not in uniq:uniq.append(p)
  master=o/'CM2_v83_Canonical_LatestWins_AllChat_Through_v82_2026-08-28.md'
  with master.open('wb') as w:
   for p in uniq:w.write(f'\n\n<!-- SOURCE {p.name} SHA256={sh(p.read_bytes())} -->\n'.encode());w.write(p.read_bytes())
  source=o/'CM2_v83_source_bundle.tar.gz';dtar(source,[(p,p.name) for p in uniq]);release=o/'CM2_v83_release_package.tar.gz';dtar(release,[(master,master.name),(source,source.name),(MAN,'source-manifest.json')])
  rec={'status':'PASS','master_sha256':sh(master.read_bytes()),'master_bytes':master.stat().st_size,'source_sha256':sh(source.read_bytes()),'release_sha256':sh(release.read_bytes())};(o/'CM2_v83_BUILD_RECEIPT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');return rec
def hs(p):return{x.name:sh(x.read_bytes()) for x in p.iterdir() if x.is_file()}
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=H/'generated');a.add_argument('--self-test',action='store_true');x=a.parse_args();r=build(x.out)
 if x.self_test:
  with tempfile.TemporaryDirectory() as d:
   q=Path(d)/'x';build(q)
   if hs(x.out)!=hs(q):raise SystemExit('deterministic mismatch')
 print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
