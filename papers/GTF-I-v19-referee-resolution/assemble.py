#!/usr/bin/env python3
"""Materialize unchanged inherited inputs and explicit release metadata.
Only the v19 directory is written. Existing new mathematical files are inputs.
The workflow commits this assembled source before compilation.
"""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent; O=P.parent/'GTF-I-v18-continuation-transport'
BASE='e7d020c49959009a775081ea9aa70c7e7fec5d52'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(path,x):path.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
for f in O.glob('*.tex'):
 if f.name not in {'introduction.tex','dependencies.tex','frontmatter.tex','main.tex'}:
  (P/f.name).write_bytes(f.read_bytes())
f=(O/'frontmatter.tex').read_text().replace('Continuation, Testing, and Microscopic Transport','Continuation Complexity and Stable Causal Certification').replace('Finite persistent resources, reset-audit duality, and changing collision dynamics','Streaming audit memory, exact continuation thresholds, and global backward transport')
abstract=r'''\begin{abstract}
We study marked causal experiments with separately charged simulator and
verifier memory. Compatible continuation responses characterize realizability
at a prescribed width profile. For Boolean streaming tests we turn a deficit
of continuation states into a quantitative statistical loss, and determine
exactly the widths attaining the optimal odd-sample binary reset value.
On a genuinely interacting two-sphere family, the private continuation
restriction yields one rational audit with $400$ training trials and a
nineteen-bit retained register whose expected discrepancy exceeds $2/5$.
The same audit remains valid while contact distance changes the collision
time and microscopic path. A common-preparation Gaussian comparison
transports likelihoods and posterior processes; a bounded terminal tilt
then gives global, rather than localized, convergence of the associated
entropic backward integrands and their martingale integrals. The certificate
and this conditional-law consumer are consequences of one microscopic
transport estimate. Hidden and visible selectors retain distinct costs,
and removing the collision makes the finite resource gaps vanish.
\end{abstract}'''
f=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda _:abstract,f,flags=re.S)
(P/'frontmatter.tex').write_text(f)
main=(O/'main.tex').read_text().replace('\\input{reset-audits}','\\input{reset-audits}\n\\input{streaming-complexity}').replace('\\input{gaussian-transport}','\\input{gaussian-transport}\n\\input{global-transport}').replace('\\input{microscopic-composition}','\\input{microscopic-composition}\n\\input{compressed-certificate}')
(P/'main.tex').write_text(main)
summary=re.search(r'\\begin\{theorem\}.*?\\end\{theorem\}',(O/'introduction.tex').read_text(),re.S).group()
(P/'baseline-summary.tex').write_text('\\subsection{Inherited baseline}\nThe following summary is retained from the predecessor. The present article\nstrengthens its memory and backward-integrand conclusions in\nTheorem~\\ref{thm:v19-main}; the earlier $2800$-trial audit remains valid.\n\n'+summary+'\n')
old=json.loads((O/'PIPELINE_GRAPH.json').read_text())
x={'schema':'gtf.namespaced-pipeline/2','edition':'v19','base_commit':BASE,'inherited_v18_graph_sha256':h(O/'PIPELINE_GRAPH.json'),'inherited_v18_graph':old,'current_credit':{'A2_primary_chain':'independent_not_consumed','C2_bounded_gaussian_global_consumer':'proof_supplied_physical_hypotheses_discharged_independent_review_pending','full_historical_program_closed_by_gtf_v19':False},'new_consumer':{'id':'C2:v19-bounded-global-backward','theorems':['thm:v19-global','thm:v19-composition'],'assumptions':['common preparation','bounded signals','fixed positive Gaussian noise','bounded scalar entropic terminal transform'],'physical_verification':'lem:v18-movingcollision and thm:v18-microscopic','conclusions':['global innovation H2','global entropic integrand H2','own-path coupled H2','innovation uniform probability convergence','backward integral S2'],'strengthens':['thm:v18-entropic'],'scoped_repair_of':['historical:thm:r17-c2-optional'],'does_not_certify':['historical:thm:r17-c2-main','historical:thm:r17-b4-main','A2 primary chain']},'new_edges':[['thm:v19-residual','thm:v19-binarywidth'],['thm:v18-continuation','lem:v19-counter'],['thm:v17-markedgap','lem:v19-counter'],['lem:v19-posterior','thm:v19-global'],['thm:v18-entropic','thm:v19-global'],['lem:v19-counter','thm:v19-composition'],['thm:v18-microscopic','thm:v19-composition'],['thm:v19-global','thm:v19-composition']],'verification_scope':'Exact source and declared dependency checks, not analytic truth or journal significance.'}
dump(P/'PIPELINE_STATUS.json',x)
rows=[]
for f in sorted(O.glob('*.tex')):
 identical=(P/f.name).exists()and h(P/f.name)==h(f)
 rows.append({'source':str(f.relative_to(P.parents[1])),'source_sha256':h(f),'canonical_copy':f.name if identical else None,'disposition':'reproduced_verbatim'if identical else 'reorganized_with_full_original_preserved_in_companion','original_commit':BASE})
dump(P/'PRESERVATION_MAP.json',{'base_commit':BASE,'files':rows,'unchanged_companion_pages':294,'companion_sha256':'f4a0c5d719b679bdb7d44111ddc3e9e36158744907b086448e0800900504cf7a','old_paths_modified':False})
(P/'requirements.txt').write_bytes((O/'requirements.txt').read_bytes())
print('Assembled local canonical inputs; no predecessor paths changed.')
