#!/usr/bin/env python3
"""Build current technical documents without altering their mathematical text."""
import argparse,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import fitz
ROOT=Path(__file__).resolve().parents[1]
SOURCE_FILES=['research/A2_Two_Collision_Response.tex','research/B2_Chronological_Contact_Reduction.tex']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--include-audit',action='store_true');args=parser.parse_args()
 selected=list(SOURCE_FILES)
 if args.include_audit:selected.append('audit/DYN_A1_Proof_Audit.tex')
 if shutil.which('pdflatex') is None:raise RuntimeError('pdflatex is required')
 records=[]
 for rel in selected:
  source=ROOT/rel;before=sha(source);data=source.read_bytes()
  if any(c<32 and c not in (9,10,13) for c in data):raise ValueError('Source control byte: '+rel)
  out=ROOT/'evidence/build'/source.stem;out.mkdir(parents=True,exist_ok=True)
  for i in range(1,4):
   command=['pdflatex','-no-shell-escape','-recorder','-interaction=nonstopmode','-halt-on-error','-file-line-error',f'-output-directory={out}',str(source)]
   proc=subprocess.run(command,cwd=source.parent,capture_output=True,text=True,timeout=120)
   (out/f'pass-{i}.txt').write_text(proc.stdout+'\n'+proc.stderr)
   if proc.returncode:raise RuntimeError(f'Build failed: {rel}, pass {i}')
  log=(out/(source.stem+'.log')).read_text(errors='replace')
  bad=[p for p in ['Undefined control sequence','There were undefined references','Missing character:','Overfull \\hbox','Overfull \\vbox','multiply defined'] if p in log]
  if bad:raise RuntimeError(f'Diagnostics {rel}: {bad}')
  if sha(source)!=before:raise RuntimeError('Source was modified by build')
  pdf=out/(source.stem+'.pdf');doc=fitz.open(pdf)
  for page in doc:
   for block in page.get_text('dict')['blocks']:
    for line in block.get('lines',[]):
     for span in line['spans']:
      x0,y0,x1,y1=span['bbox']
      if x0<-.5 or y0<-.5 or x1>page.rect.width+.5 or y1>page.rect.height+.5:raise RuntimeError('Out-of-page text')
  target=source.with_suffix('.pdf');shutil.copyfile(pdf,target)
  records.append({'source':rel,'source_sha256':before,'pdf':str(target.relative_to(ROOT)),'pages':len(doc),'pdf_sha256':sha(target),'passes':3,'final_diagnostics':bad,'source_unchanged':True})
 receipt={'status':'PASS','execution_utc':datetime.now(timezone.utc).isoformat(),'documents':records,'scope':'Build and text-boundary checks; not mathematical proof verification. Manual rendering audit recorded separately.'}
 (ROOT/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
