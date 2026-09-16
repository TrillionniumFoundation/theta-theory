#!/usr/bin/env python3
"""Activate v66 from seven exact v65 files; preserve all original bytes.

This is a deterministic source transformation, not a deferred proof generator.
All new mathematical text is already present as committed TeX input.
"""
from pathlib import Path
import hashlib, json, re
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'papers/A2-v17-boundary-information-coarsening'
EXPECTED={'main.tex': '8cf415ef1a8770b520f8364188006321d6f39a64bf76d7a117803606c5a5074e', 'rigidity.tex': 'd7e9076dd57809b2e957f76f50121ae05dce6c82742b1e3380b85e5659a7ed3a', 'article/00_structural_introduction_v48.tex': '70c38314240b7f987891f9e30e907fbfdc7c6cf6b86d8e00b9a39020b01df48a', 'journal/00_principal_introduction_v61.tex': '5ff097cbbf39fff26994713ab2e8dc8d985fc9b0495e7a1153033060e03d54b4', 'v5/references_v43.tex': '628c47b3272c9b2e40505b3a7f26cd404fa4892b6d87313e72fd7f817bf20d0b', 'journal/references_v56.tex': '56885b2222625e5fb862a69d330fe9e3afde494aacf8f5496ebba540e2189d7b', 'README.md': '470a0a9c6306d014f61f483e16c793f5a71850356adfa6db4b3ac78dcd24ddba'}

def require(ok, message):
    if not ok: raise RuntimeError(message)

def replace_once(text, old, new):
    require(text.count(old)==1, 'Nonunique source marker: '+old[:90])
    return text.replace(old,new,1)

def activate():
    archive=P/'history/v65-review-baseline'
    pending={}
    for name,digest in EXPECTED.items():
        data=(P/name).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest, 'Unexpected v65 source: '+name)
        pending[name]=data
    manifest=archive/'SOURCE_MANIFEST.json'
    require(hashlib.sha256(manifest.read_bytes()).hexdigest()=='d0a70195757be19de9b4cda07fb1daea1fd37a95d224ede4906f5226a344ce9d', 'Wrong frozen baseline manifest')
    for name,data in pending.items():
        target=archive/name
        target.parent.mkdir(parents=True,exist_ok=True)
        require(not target.exists() or target.read_bytes()==data, 'Archive collision: '+name)
        target.write_bytes(data)
    for name in ('main.tex','rigidity.tex'):
        s=pending[name].decode()
        s,count=re.subn(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:r'\begin{abstract}'+'\n'+r'\input{article/00h_abstract_v66}'+'\n'+r'\end{abstract}',s,flags=re.S)
        require(count==1, 'Abstract marker: '+name)
        s=replace_once(s,r'\input{article/10b_periodic_contact_inverse_v65}',r'\input{article/10b_periodic_contact_inverse_v65}'+'\n'+r'\input{article/10c_global_curvature_inverse_v66}')
        s=s.replace('A2 revision 65','A2 revision 66').replace('% A2 v65.','% A2 v66.')
        acknowledgement=(r'The quadratic Riccati comparison in the author-requested AI-assisted'+'\n'+r'memorandum~\cite{A2ReviewV65} suggested the global curvature argument'+'\n'+r'developed here.  That memorandum is not a commissioned journal report.'+'\n\n')
        s=replace_once(s,r'\appendix',acknowledgement+r'\appendix')
        (P/name).write_text(s)
    for name,label in (('article/00_structural_introduction_v48.tex','v48'),('journal/00_principal_introduction_v61.tex','v56')):
        s=pending[name].decode()
        anchor=r'\label{sec:'+label+'-introduction}'+'\n\n'
        start=s.index(anchor)+len(anchor)
        marker=r'\input{article/00e_periodic_mechanism_overview_v64}'
        stop=s.index(marker,start)
        lead=s[start:stop]
        s=s[:start]+r'\input{article/00g_contact_synthesis_v66}'+'\n\n'+s[stop:]
        marker=r'\input{article/00f_periodic_contact_overview_v65}'
        s=replace_once(s,marker,marker+'\n\n'+r'\subsection{The alternating channel and its geometric content}'+'\n\n'+lead)
        (P/name).write_text(s)
    bib=r"""\bibitem{A2ReviewV65}
\emph{Independent referee report on A2, revision 65},
author-requested AI-assisted memorandum, September 16, 2026,
Section R65-M5. Repository
\texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/7f4603531f7b97a23ce627fec47b7ddc5f4f9912/reviews/a2-v65-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md}{frozen memorandum}.
Cited for the Riccati derivative comparison, not for a global inverse
or a commissioned journal decision.

"""
    for name in ('v5/references_v43.tex','journal/references_v56.tex'):
        (P/name).write_text(replace_once(pending[name].decode(),r'\end{thebibliography}',bib+r'\end{thebibliography}'))
    front="""# A2 revision 66: global marked contact identification

The current revision answers the v65 report at immutable head
`7f4603531f7b97a23ce627fec47b7ddc5f4f9912`.
Read `RESPONSE_TO_REFEREE_V66.md` and `HISTORICAL_DERIVATION_AUDIT_V66.md`.
Both `rigidity.tex` and `main.tex` contain the complete new proof in
`article/10c_global_curvature_inverse_v66.tex`.  The curvature inverse
is globally single-valued on the positive class; exact analytic marked
identification no longer needs nearby candidates.  The supplied polygon,
shared two-offset amplitudes, fixed lattice and full-visitation clauses
remain explicit.  Analytic norm and real-noise estimates retain their
local priors and radius loss.  All inherited proofs remain active.

The previous entry is retained below and byte-exact in
`history/v65-review-baseline/README.md`.

---

"""
    (P/'README.md').write_text(front+pending['README.md'].decode())
    print(json.dumps({'baseline_source':'06a197e4d11bc3d4193e9f0b7904105df35875fa','changed_originals_preserved':sorted(EXPECTED),'new_proofs_generated_by_script':False},indent=2,sort_keys=True))
if __name__=='__main__': activate()
