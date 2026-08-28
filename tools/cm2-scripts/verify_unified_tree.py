#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,hashlib,json,subprocess,tarfile,gzip,io,tempfile
from pathlib import Path
def sh(b):return hashlib.sha256(b).hexdigest()
def gh(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,default=Path('.'));x=a.parse_args();r=x.repo.resolve();m=json.loads((r/'provenance/cm2-unified-tree-2026-08-28/source-manifest.json').read_text())
 for e in m['remote_pr_exact_sources']:
  b=(r/e['path']).read_bytes()
  if (gh(b),len(b))!=(e['git_blob_sha1'],e['bytes']):raise SystemExit('FAIL remote '+e['path'])
 ar=m['local_library_exact_report_archive'];ps=sorted((r/ar['parts_dir']).glob(ar['part_glob']));b=base64.b64decode(''.join(p.read_text().strip() for p in ps),validate=True)
 if len(ps)!=ar['part_count'] or len(b)!=ar['decoded_bytes'] or sh(b)!=ar['decoded_sha256']:raise SystemExit('FAIL archive')
 with tempfile.TemporaryDirectory() as d:
  q=Path(d)
  with tarfile.open(fileobj=gzip.GzipFile(fileobj=io.BytesIO(b)),mode='r:') as tf:
   for z in tf.getmembers():
    p=Path(z.name)
    if z.issym() or z.islnk() or p.is_absolute() or '..' in p.parts or not z.isfile():raise SystemExit('FAIL unsafe archive')
   tf.extractall(q,filter='data')
  for e in m['local_library_sources']:
   if 'archive_member' in e:z=(q/e['archive_member']).read_bytes()
   else:
    z=(r/e['path']).read_bytes()
    if 'embedded_filename' in e:
     pos=z.find(e['embedded_filename'].encode());s=z.find(b'\n',pos)+1;end=z.find(b'<!-- END ',s);z=z[s:end]
     if z.endswith(b'\n') and len(z)==e['bytes']+1:z=z[:-1]
   if len(z)!=e['bytes'] or sh(z)!=e['sha256']:raise SystemExit('FAIL local '+e.get('archive_member',e.get('stage')))
 idx=(r/'canonical/CM2_UNIFIED_TREE_INDEX.md').read_text()
 for s in ['WITHDRAWN_LATEST_WINS','ACTUAL_LOCAL_PACKETS_REQUIRED','ExternalPeerReview: NOT_PERFORMED']:
  if s not in idx:raise SystemExit('FAIL status '+s)
 with tempfile.TemporaryDirectory() as d:
  p=Path(d);subprocess.run(['python3',str(r/'cm2/canonical/v83/build_v83.py'),'--out',str(p/'a'),'--self-test'],check=True);subprocess.run(['python3',str(r/'cm2/canonical/v83/build_v83.py'),'--out',str(p/'b')],check=True)
  if {z.name:sh(z.read_bytes()) for z in (p/'a').iterdir()}!={z.name:sh(z.read_bytes()) for z in (p/'b').iterdir()}:raise SystemExit('FAIL rebuild')
 print(json.dumps({'status':'PASS','remote_exact':len(m['remote_pr_exact_sources']),'local_sources':len(m['local_library_sources']),'terminal_package_hashes':len(m['terminal_packages_local_archive_only'])},sort_keys=True))
if __name__=='__main__':main()
