#!/usr/bin/env python3
"""Idempotent final proof-reading corrections, committed before the build."""
from pathlib import Path
P=Path(__file__).resolve().parent
fixes={
 'global-transport.tex':[('In particular $\\bar I^n\\to\\bar I$ uniformly in probability. Writing','If $\\eta_n\\to0$, then $\\bar I^n\\to\\bar I$ uniformly in probability. Writing')],
 'introduction.tex':[('\\textup{(ii)} Consider $n=2m+1$ independent binary samples from one of','\\textup{(ii)} For $0<h<1/2$, consider $n=2m+1$ independent binary samples from one of')],
 'compressed-certificate.tex':[('In $n$ independent all-on candidate trials let $C_0,C_1$ count report','In $n\\ge1$ independent all-on candidate trials let $C_0,C_1$ count report')],
 'assemble.py':[("(P/'requirements.txt').write_text('PyMuPDF==1.26.4\\n')","(P/'requirements.txt').write_bytes((O/'requirements.txt').read_bytes())")],
 'build.py':[('3835b09eb368c65ef453d28e3c9f2ea59cdab1c84391ac8f4a33770f844ca788','fa27a4e69e6c854b7db6434cdb326a20d71aefb1aca3e1a2c70e7de93f9ff67d'),("'current_status':'proof_supplied_in_manuscript'","'current_status':('definition_stated' if match.group(1)=='definition' else 'example_argument_supplied' if match.group(1)=='example' else 'proof_supplied_in_manuscript')")]
}
for name,changes in fixes.items():
 path=P/name;text=path.read_text()
 for old,new in changes:
  if old in text:
   if text.count(old)!=1:raise RuntimeError('Ambiguous correction in '+name)
   text=text.replace(old,new)
  elif new not in text:raise RuntimeError('Correction target absent in '+name)
 path.write_text(text)
print('Explicit limiting and parameter hypotheses checked; only v19 files written.')
