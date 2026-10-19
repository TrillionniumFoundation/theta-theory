from pathlib import Path
import argparse,sys,json,importlib.util,concurrent.futures
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--workers',type=int,default=4);ap.add_argument('--typeset',action='store_true');a=ap.parse_args()
root=Path(a.root); spec=importlib.util.spec_from_file_location('qualification',root/'tools/qualify_revision.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
specroot=str(root/'tools');sys.path.insert(0,specroot)
q.source()
def task(args):
 name,opt=args;suffix='optimized' if opt else 'normal';tag=name+'-'+suffix
 cmd=[sys.executable]+(['-O'] if opt else [])+['tools/'+name+'.py']
 if name in q.DETAILS:cmd+=['--details',str(q.B/(name+'-cases-'+suffix+'.json'))]
 record=q.B/(tag+'.command.json');log=q.B/(tag+'.log')
 valid=False
 if record.exists() and log.exists():
  rec=json.loads(record.read_text());valid=rec['exit_code']==0 and rec['command']==cmd and rec['source_manifest_sha256']==q.digest(root/'SOURCE_MANIFEST.json') and rec['log_sha256']==q.digest(log)
  if name in q.DETAILS:valid=valid and (q.B/(name+'-cases-'+suffix+'.json')).exists()
 if not valid:q.run(cmd,tag)
 print('verified command',tag,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:
 list(ex.map(task,[(n,o) for n in q.PROGRAMS for o in [False,True]]))
def collect():
 results={}
 for name in q.PROGRAMS:
  logs=[q.B/(name+'-'+s+'.log') for s in ['normal','optimized']]
  q.require(logs[0].read_bytes()==logs[1].read_bytes(),'normal/-O mismatch '+name)
  results[name]=json.loads(logs[0].read_text())
  if name in q.DETAILS:q.require((q.B/(name+'-cases-normal.json')).read_bytes()==(q.B/(name+'-cases-optimized.json')).read_bytes(),'raw-case mismatch '+name)
 return {'programs':results,'normal_optimized_identical':True,'raw_case_sha256':{name:q.digest(q.B/(name+'-cases-normal.json')) for name in q.DETAILS}}
q.phase('checks',collect)
if a.typeset:q.phase('typeset',q.typeset);q.finalize()
