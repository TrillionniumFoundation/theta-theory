#!/usr/bin/env python3
"""Build the new manuscript and byte-preserved complete mathematical companion."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,os,platform,re,subprocess,sys
import verify
ROOT=Path(__file__).resolve().parent
EPOCH='1791979200'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(args,cwd=None,env=None):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
    if p.returncode:raise RuntimeError('command failed: '+repr(args)+'\n'+p.stdout[-12000:]+p.stderr[-3000:])
    return p.stdout

def build(root,out):
    audit=verify.verify(root);out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.update({'SOURCE_DATE_EPOCH':EPOCH,'FORCE_SOURCE_DATE':'1','TZ':'UTC','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
    result={}
    for name,src in [('General_Theta_Foundations_I_R59',root),('General_Theta_Complete_Companion_R58',root/'retained/r58-native')]:
        logs=out/(name+'-logs');logs.mkdir(exist_ok=True)
        for iteration in range(1,4):
            args=['pdflatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-recorder','-output-directory='+str(logs),'main.tex']
            run=subprocess.run(args,cwd=src,env=env,capture_output=True,text=True)
            (logs/f'pass-{iteration}.txt').write_text(run.stdout+run.stderr)
            if run.returncode:raise RuntimeError(name+' TeX failure:\n'+run.stdout[-6000:])
        log=(logs/'main.log').read_text(errors='replace')
        failures=[]
        for pattern in [r'LaTeX Warning:.*undefined',r'There were undefined',r'Multiply defined',r'Label\(s\) may have changed',r'Citation .+ undefined']:
            if re.search(pattern,log,re.I):failures.append(pattern)
        if failures:raise RuntimeError(name+' unresolved TeX warnings '+repr(failures))
        overfull=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt too wide\)',log)]
        # A byte-preserved historical document is reported, not silently restyled.
        if name.endswith('R59') and any(x>0.5 for x in overfull):raise RuntimeError('native overfull box: '+repr(overfull))
        pdf=out/(name+'.pdf');pdf.write_bytes((logs/'main.pdf').read_bytes())
        text=out/(name+'.txt');command(['pdftotext','-layout',str(pdf),str(text)])
        info=command(['pdfinfo',str(pdf)]);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        result[name]={'pdf':pdf.name,'sha256':sha(pdf),'bytes':pdf.stat().st_size,'pages':pages,'text_sha256':sha(text),'overfull_hbox_pt':overfull}
    try:head=command(['git','rev-parse','HEAD'],cwd=root).strip()
    except RuntimeError:head=None
    receipt={'schema':1,'status':'PASS','checkout_head':head,'source_manifest_sha256':sha(root/'SOURCE_MANIFEST.json'),'source_date_epoch':EPOCH,'python':platform.python_version(),'platform':platform.platform(),'pdflatex':command(['pdflatex','--version']).splitlines()[0],'audit':audit,'documents':result,'limitations':'A successful build does not certify theorem proofs, originality, journal significance or exhaustive historical mathematical audit.'}
    (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    return receipt

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
    out=a.out.expanduser().resolve()
    if out==ROOT:raise RuntimeError('output must not overwrite source root')
    print(json.dumps(build(ROOT,out),sort_keys=True,indent=2))
if __name__=='__main__':main()
