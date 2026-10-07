#!/usr/bin/env python3
"""One-time, hash-pinned transport. Commit ordinary sources before building them.
Transport data is parsed as literals, not executed. Never writes the R7/R6 inputs.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PAPER = Path('papers/General-Theta-Foundations-I-restart')
OLD_NAME = 'r7-acquisition-compatible'
NEW_NAME = 'r8-continuation-geometry'
EXPECTED = '057f318118224e615ea812214608eb3c79ab98ae'
PAYLOADS = {
 'transport_math.py': '3a96131355dbe90996e2ee036895ff7d63088449',
 'transport_docs1.py': '555b761efa8331fffb0aa248ff5fa43564a44c14',
 'transport_docs2.py': 'c5919a19caacaeeb05655078b9bc39984bd288e1',
 'transport_build.py': '48d58b98227d9279a44b0e8063b3b62e221adeae',
}
TREES = {
 'r4-causal-resolvent':'39efc9cf1199031fd6cce40690c1eb617e80af4c',
 'r5-intrinsic-recursion':'44fff54beca2eca58133d67a21306822b26bc887',
 'r6-operational-transfer':'e449fa84cb6a83589e8b20831230825c19c2e050',
 OLD_NAME:'b39a6d0b4704bba93d75176280e936cba6282dcb',
}
CONTROLS = {
 'foundations/general-theta/General_Theta_Foundations_v0.1.md':'2f07620415114d870ac80b7feeffb9cbb514c6a1',
 'foundations/general-theta/RESTART_CHARTER.md':'863318cd21012e4259aa26538d7c99c21e615666',
 'foundations/general-theta/REALIZATION_REGISTRY.md':'7da262b0564aad606dc06daada2cbaf76b8fbfa7',
 str(PAPER/'THEOREM_TARGETS.md'):'ce06d7e4b738bfd489df2d073e4303fd79cfaac6',
 str(PAPER/'review-inputs/R7_EXTERNAL_REFEREE_REPORT.md'):'637f674f3e074c9f9d82f1d0e7ac61bb7aab3f5d',
}
NEW_PROOFS = {
 'sections/08_continuation.tex':'076541afa61ebee873b2deb46761fd374f3899a3',
 'sections/09_noisy.tex':'23e705bc2be1ffc1fb16ed3702562376c9f13b01',
}

def require(ok, message):
 if not ok: raise RuntimeError(message)

def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def run(args, root):
 return subprocess.check_output(args,cwd=root,text=True).strip()

def safe(name):
 p=Path(name)
 require(not p.is_absolute() and '..' not in p.parts and p.parts, 'unsafe transport path')
 return p

def literals(path):
 data=path.read_bytes()
 require(blob(data)==PAYLOADS[path.name], 'transport hash mismatch: '+path.name)
 result={}
 for node in ast.parse(data.decode()).body:
  require(isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name),'nonliteral transport statement')
  name=node.targets[0].id
  require(name in ('TEXTS','EDITS') and name not in result,'unexpected transport name')
  result[name]=ast.literal_eval(node.value)
 return result

def apply(root, payload_dir):
 old=root/PAPER/OLD_NAME; new=root/PAPER/NEW_NAME
 manifest=json.loads((old/'SOURCE_MANIFEST.json').read_text())
 original={}
 for name,record in manifest['files'].items():
  data=(old/safe(name)).read_bytes()
  require(blob(data)==record['git_blob_sha'],'R7 original blob mismatch: '+name)
  original[name]=data.decode()
 for name,expected in NEW_PROOFS.items():
  require(blob((new/name).read_bytes())==expected,'new proof transport mismatch: '+name)
 for name,text in original.items():
  path=new/safe(name);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
 touched=set()
 for payload in PAYLOADS:
  values=literals(payload_dir/payload)
  for name,(base,edits) in values.get('EDITS',{}).items():
   require(name not in touched, 'duplicate destination '+name);touched.add(name)
   lines=original[base].splitlines(keepends=True)
   end=0
   for lo,hi,text in edits:
    require(isinstance(text,str) and end<=lo<=hi<=len(lines),'invalid edit range')
    end=hi
   for lo,hi,text in reversed(edits):lines[lo:hi]=text.splitlines(keepends=True)
   p=new/safe(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(lines))
  for name,text in values.get('TEXTS',{}).items():
   require(name not in touched and isinstance(text,str),'duplicate/invalid text '+name);touched.add(name)
   p=new/safe(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 subprocess.check_call([sys.executable,str(new/'refresh_manifest.py')])
 audit=json.loads(run([sys.executable,str(new/'verify.py')],root))
 require(audit['native_source_tree_sha']==EXPECTED,'materialized source tree differs from reviewed preflight')
 return audit

def main():
 here=Path(__file__).resolve().parent;root=here.parents[1]
 for name,sha in TREES.items():
  require(run(['git','rev-parse','HEAD:'+str(PAPER/name)],root)==sha,'historical tree mismatch '+name)
 for name,sha in CONTROLS.items():require(blob((root/name).read_bytes())==sha,'control/review mismatch '+name)
 audit=apply(root,here)
 audit['transport']='literal data; ordinary source tree committed before build'
 print(json.dumps(audit,sort_keys=True,indent=2))

if __name__=='__main__':main()
