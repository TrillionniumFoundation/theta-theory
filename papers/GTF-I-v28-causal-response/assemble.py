#!/usr/bin/env python3
"""Reversible assembly: old mathematical statements retained; only new paths written."""
from pathlib import Path
import hashlib,json,shutil
H=Path(__file__).resolve().parent;O=H.parent/'GTF-I-v27-resource-saddle'
raw=(O/'main.tex').read_bytes();text=raw.decode()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
# Pin the actual frozen predecessor artifact, not a mutable branch name.
expected='7339ba992cb3c2bf14fead1e02938f52bb68eaea'
if blob!=expected:raise RuntimeError('v27 main Git blob mismatch: '+blob)
pre=text.split('\\begin{abstract}',1)[0].replace('Saddle Geometry and the Memory of Causal Experiments','Robust Saddles, Causal Memory, and Validation Order').replace('Revision 27','Revision 28').replace('[Saddle geometry and causal memory]','[Robust saddles and causal memory]')
marker='\\input{foundations}'
oldbody=text[text.index(marker):text.index('\\begin{thebibliography}')];body=oldbody;patches=[]
def patch(a,b):
 global body
 if body.count(a)!=1:raise RuntimeError('Ambiguous main assembly: '+a)
 body=body.replace(a,b,1);patches.append({'old':a,'new':b})
patch('\\input{saddle-realization}','\\input{saddle-realization}\n\\input{facial-scheduling}')
patch('\\input{exact-memory}','\\input{exact-memory}\n\\input{positive-noise-saddle}\n\\input{physical-noise-law}\n\\input{validation-order}')
# Every predecessor mathematical module is retained. One is split expositionally below.
unchanged=[]
for p in O.glob('*.tex'):
 if p.name in ['main.tex','introduction.tex','saddle-realization.tex']:continue
 d=H/p.name
 if d.exists() and d.read_bytes()!=p.read_bytes():raise RuntimeError('Inherited module modified: '+p.name)
 shutil.copy2(p,d);unchanged.append(p.name)
src=(O/'saddle-realization.tex').read_text()
a=r'''\begin{theorem}[Saddle-face realization and exact resource loss]
\label{thm:saddle-realization}
Under the preceding assumptions, the constrained outer value satisfies
\begin{equation}\label{eq:resource-loss}
 U-V_{\mathbf K}=\min_{C\in\mathcal C_{\mathbf K}}
 \left\{U-\ell_*(C)+
                  \ell_*(C)-\min_\theta g_\theta(C)\right\}.
\end{equation}
Both summands are nonnegative. Consequently $V_{\mathbf K}=U$ if and
'''
b=r'''\begin{proposition}[Bayes loss and worst-case loss]
\label{prop:loss-decomposition}
Under the preceding assumptions,
\begin{equation}\label{eq:resource-loss}
 U-V_{\mathbf K}=\min_{C\in\mathcal C_{\mathbf K}}
 \left\{U-\ell_*(C)+
                  \ell_*(C)-\min_\theta g_\theta(C)\right\}.
\end{equation}
Both summands are nonnegative and the minimum is attained.
\end{proposition}
\begin{proof}
The prior average is at most $U$ and at least the minimum over fixed
parameters. The sum in braces equals $U-\min_\theta g_\theta(C)$.
Minimizing on the compact realization set proves the assertion.
\end{proof}

\begin{theorem}[Saddle-face contact and compatible realization]
\label{thm:saddle-realization}
Under the preceding assumptions, $V_{\mathbf K}=U$ if and
'''
if src.count(a)!=1:raise RuntimeError('Loss statement split mismatch')
src=src.replace(a,b,1)
c=r'''For every $C$, its prior average is at most $U$ and at least its minimum
over fixed parameters. The expression in braces in
\eqref{eq:resource-loss} is identically $U-\min_\theta g_\theta(C)$.
Taking its minimum over the compact set $\mathcal C_{\mathbf K}$ proves
the identity and attainment. Its two nonnegative summands vanish exactly
when $C$ belongs to $\mathcal S_*$. Proposition~\ref{prop:outer-normal-form}
then proves the realization criterion.'''
d=r'''By Proposition~\ref{prop:loss-decomposition}, the two nonnegative
losses vanish exactly when $C$ belongs to $\mathcal S_*$.
Proposition~\ref{prop:outer-normal-form} then proves the realization
criterion.'''
if src.count(c)!=1:raise RuntimeError('Loss proof split mismatch')
src=src.replace(c,d,1)
if src.replace(d,c,1).replace(b,a,1)!=(O/'saddle-realization.tex').read_text():raise RuntimeError('Cannot reconstruct predecessor statement and proof')
(H/'saddle-realization.tex').write_text(src)
bib=text[text.index('\\begin{thebibliography}'):]
bib=bib.replace('\\end{thebibliography}',r'''\bibitem{Reusch} B. Reusch and W. Merzenich, Minimal coverings for
incompletely specified sequential machines, \emph{Acta Informatica}
\textbf{22} (1986), 663--678, doi:10.1007/BF00263650.
\end{thebibliography}''')
recovered=body
for p in reversed(patches):recovered=recovered.replace(p['new'],p['old'],1)
if recovered!=oldbody:raise RuntimeError('Predecessor body changed')
(H/'main.tex').write_text(pre+(H/'introduction.tex').read_text()+'\n'+body+bib)
manifest={'predecessor_main_git_blob':blob,'predecessor_main_sha256':hashlib.sha256(raw).hexdigest(),'old_body_recovered_exactly':True,
 'reversible_main_insertions':patches,'unchanged_modules':sorted(unchanged),'expository_split':{'module':'saddle-realization.tex','old_statement':a,'new_statement':b,'old_proof':c,'new_proof':d,'exact_reconstruction_checked':True},
 'new_mathematics':['facial-scheduling.tex','positive-noise-saddle.tex','physical-noise-law.tex','validation-order.tex'],
 'scope':'All predecessor mathematical content retained. Loss identity moved to a proposition; original paths untouched.'}
(H/'ASSEMBLY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
