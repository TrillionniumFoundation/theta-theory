#!/usr/bin/env python3
"""Make the flat-testing threshold explicit, then verify the complete source."""
from pathlib import Path
import hashlib
import subprocess

root=Path('papers/A2-v17-boundary-information-coarsening')
p=root/'article/10e_sampled_smooth_recovery_v69.tex'
text=p.read_text()
old="$\\Delta=\\varepsilon e^{-1/u_*^2}$.  If the right side of\n\\eqref{eq:v69-budget-rate} is less than $\\Delta/3$, comparing the\nestimated profile's distance to these two candidates gives a test whose\nerror at either table is at most $2\\zeta$.  The remote area correction"
new="$\\Delta=\\varepsilon e^{-1/u_*^2}$.  Whenever\n$C\\{(L_B/B)^\\beta+\\delta^\\gamma\\}<\\Delta/3$,\n\\eqref{eq:v69-budget-rate} and comparison of the estimated profile's\ndistance to these two candidates give a test whose error at either table\nis at most $2\\zeta$.  The remote area correction"
if old in text:
    if text.count(old)!=1:
        raise RuntimeError('Ambiguous testing-threshold anchor')
    text=text.replace(old,new)
data=text.encode()
blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob!='bed40ae54fc3b8da8c78cf286a6d3776374dfd79':
    raise RuntimeError('Unexpected complete proof module')
p.write_bytes(data)
subprocess.run(['git','add','--',str(p)],check=True)
tree=subprocess.check_output(['git','write-tree'],text=True).strip()
subtree=subprocess.check_output(['git','rev-parse',tree+':'+str(root)],text=True).strip()
if subtree!='3e06abdeb4fc77251fa3e0b536886dbc1dbb48bd':
    raise RuntimeError('Complete manuscript tree differs: '+subtree)
print('Complete source verified: '+subtree)
