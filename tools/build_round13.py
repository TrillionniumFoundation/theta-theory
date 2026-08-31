#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json,re,subprocess,sys
from round13_config import PAPERS
ROOT=Path(__file__).resolve().parents[1]
LOGDIR=ROOT/'ROUND13_BUILD_LOGS';LOGDIR.mkdir(exist_ok=True)
UNDEFINED=re.compile(r'LaTeX Warning: (?:Reference|Citation).+undefined|There were undefined references|There were undefined citations')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(folder):
    p=ROOT/'papers'/folder;transcript=LOGDIR/f'{folder}.log'
    subprocess.run(['latexmk','-C','main.tex'],cwd=p,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    proc=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=p,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=300)
    transcript.write_text(proc.stdout,errors='replace')
    pdf=p/'main.pdf';log=p/'main.log';undefined=[]
    if log.is_file():undefined=[x for x in log.read_text(errors='replace').splitlines() if UNDEFINED.search(x)]
    pages=0
    if pdf.is_file() and pdf.stat().st_size:
        info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True);m=re.search(r'^Pages:\s+(\d+)',info.stdout,re.M);pages=int(m.group(1)) if m else 0
    ok=proc.returncode==0 and pdf.is_file() and pdf.stat().st_size>0 and pages>0 and not undefined
    return folder,{'returncode':proc.returncode,'status':'PASS' if ok else 'FAIL','pdf_bytes':pdf.stat().st_size if pdf.is_file() else 0,'pdf_pages':pages,'pdf_sha256':sha(pdf) if pdf.is_file() and pdf.stat().st_size else None,'undefined_reference_lines':undefined,'transcript':str(transcript.relative_to(ROOT)),'tail':proc.stdout[-5000:] if not ok else ''}
results={}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs={ex.submit(build,f):f for f in PAPERS}
    for fut in as_completed(futs):
        folder,entry=fut.result();results[folder]=entry;print('ROUND13_BUILD',folder,entry['status'])
failed=[f for f in PAPERS if results[f]['status']!='PASS']
summary={'schema':'theta-theory-round13-build-summary-v1','papers':{f:results[f] for f in PAPERS},'failed':failed,'paper_count':11,'passed':11-len(failed),'total_pdf_pages':sum(results[f]['pdf_pages'] for f in PAPERS),'status':'PASS' if not failed else 'FAIL'}
serial={f:dict(results[f]) for f in PAPERS}
for e in serial.values():e.pop('tail',None)
summary['papers']=serial
(ROOT/'ROUND13_BUILD_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
if failed:
    for f in failed:print(f'ROUND13_BUILD_FAIL {f}\n{results[f]["tail"]}',file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND13_BUILD_PASS 11/11 pages={summary['total_pdf_pages']}")
