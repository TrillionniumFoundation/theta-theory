#!/usr/bin/env python3
"""Additive, source-pinned assembly of the v27 article."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v26-controlled-memory-foundations'
raw=(O/'main.tex').read_bytes(); text=raw.decode()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
if blob!='c6dcd5f60dfbd34c679961e6afeded933cda3ba4':
    raise RuntimeError('v26 main source pin failed: '+blob)
pre=text.split('\\begin{abstract}',1)[0]
pre=pre.replace('Causal Experiments, Finite-Memory Control, and Exact Minimax Laws',
                'Saddle Geometry and the Memory of Causal Experiments')
pre=pre.replace('[Causal experiments and finite memory]', '[Saddle geometry and causal memory]').replace('Revision 26','Revision 27')
marker='\\input{foundations}'
body=text[text.index(marker):text.index('\\begin{thebibliography}')]
patches=[]
def patch(a,b):
    global body
    if body.count(a)!=1: raise RuntimeError(('Ambiguous assembly patch',a,body.count(a)))
    body=body.replace(a,b,1); patches.append({'old':a,'new':b})
patch('\\input{controlled-memory}', '\\input{controlled-memory}\n\\input{saddle-realization}')
patch('\\input{two-preparation-family}', '\\input{two-preparation-family}\n\\input{exact-memory}\n\\input{preparation-localization}')
# Earlier qualified claims remain valid; point to the new order-specific converse explicitly.
patch('least peak width at $N=2$ and the full boundary for $3\\le W\\le11$\nremain separate questions.',
      'least peak width over all validation orders and the full boundary for\n$3\\le W\\le11$ remain separate questions. Theorem~\\ref{thm:serial-twelve}\nbelow determines the peak for forward serial validation, and\nTheorem~\\ref{thm:five-memory} determines the order-independent decision cut.')
bib=text[text.index('\\begin{thebibliography}'):]
extra=r'''
\bibitem{Heller} A. Heller, On stochastic processes derived from Markov chains,
\emph{Ann. Math. Statist.} \textbf{36} (1965), 1286--1291,
doi:10.1214/aoms/1177700000.
\bibitem{Vidyasagar} M. Vidyasagar, The complete realization problem for
hidden Markov models: a survey and some new results,
\emph{Math. Control Signals Systems} \textbf{23} (2011), 1--65,
doi:10.1007/s00498-011-0066-7.
\bibitem{GG} N. Gillis and F. Glineur, On the geometric interpretation of
the nonnegative rank, \emph{Linear Algebra Appl.} \textbf{437} (2012),
2685--2712, arXiv:1009.0880.
'''
bib=bib.replace('\\end{thebibliography}',extra+'\n\\end{thebibliography}')
recovered=body
for p in reversed(patches): recovered=recovered.replace(p['new'],p['old'],1)
if recovered!=text[text.index(marker):text.index('\\begin{thebibliography}')]:
    raise RuntimeError('Predecessor mathematical body is not fully recoverable')
unchanged=[]
for p in O.glob('*.tex'):
    if p.name in {'main.tex','introduction.tex'}:continue
    q=H/p.name
    if not q.exists() or q.read_bytes()!=p.read_bytes():raise RuntimeError('Inherited module changed: '+p.name)
    unchanged.append(p.name)
(H/'main.tex').write_text(pre+(H/'introduction.tex').read_text()+'\n'+body+bib)
manifest={'predecessor_main_git_blob':blob,'predecessor_main_sha256':hashlib.sha256(raw).hexdigest(),
          'reversible_patches':patches,'unchanged_modules':sorted(unchanged),
          'old_body_recovered_exactly':True,'new_modules':['saddle-realization.tex','exact-memory.tex','preparation-localization.tex'],
          'exposition':'Introduction rewritten; predecessor introduction retained at its unchanged path and in both complete volumes.'}
(H/'ASSEMBLY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
