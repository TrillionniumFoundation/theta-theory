from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
O=H.parent/'GTF-I-v25-controlled-minimax'
raw=(O/'main.tex').read_bytes(); text=raw.decode()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
if blob!='4b793be9f45326fab51d44b66877f5a8bf61667c': raise RuntimeError('Predecessor source pin failed')
pre=text.split('\\begin{abstract}',1)[0]
pre=pre.replace('Controlled Experiment Duality and Exact Marked Minimax Laws','Causal Experiments, Finite-Memory Control, and Exact Minimax Laws').replace('[Controlled statistical minimax]','[Causal experiments and finite memory]').replace('Revision 25','Revision 26')
marker='\\section{Experiments, architectures and attainable resources}'
body=text[text.index(marker):text.index('\\begin{thebibliography}')]
patches=[]
def patch(a,b):
 global body
 if body.count(a)!=1:raise RuntimeError((a[:80],body.count(a)))
 body=body.replace(a,b,1);patches.append({'old':a,'new':b})
patch('\\input{controlled-dual}', '\\input{controlled-dual}\n\\input{controlled-memory}')
patch('\\input{physical-improvement}', '\\input{physical-improvement}\n\\input{two-preparation-saddle}\n\\input{two-preparation-family}')
patch('\\input{joint-revelation}', '\\input{joint-revelation}\n\\input{integer-revelation}')
patch('The theorem evaluates the minimum preparation coordinate for $W\\ge12$.\nIt does not determine $N_c^{\\rm phys}(W,Q)$ for $3\\le W\\le11$, the\nmaximum score with two preparations, or the least peak width at $N=2$.',
'The deterministic theorem evaluates the minimum preparation coordinate\nfor $W\\ge12$. Theorem~\\ref{thm:two-saddle} and\nCorollary~\\ref{cor:two-physical-exact} below additionally determine the\nideal maximum score with two preparations on this width range. The\nleast peak width at $N=2$ and the full boundary for $3\\le W\\le11$\nremain separate questions.')
patch('\\section{Dependencies, retained results and remaining distinctions}', '\\input{consumer-transfer}\n\n\\section{Dependencies, retained results and remaining distinctions}')
bib=text[text.index('\\begin{thebibliography}'):]
extra=r'''
\bibitem{Chernoff} H. Chernoff, Sequential design of experiments,
\emph{Ann. Math. Statist.} \textbf{30} (1959), 755--770.
\bibitem{NJ} M. Naghshvar and T. Javidi, Active sequential hypothesis
testing, \emph{Ann. Statist.} \textbf{41} (2013), 2703--2738,
doi:10.1214/13-AOS1144.
\bibitem{NAV} S. Nitinawarat, G. K. Atia and V. V. Veeravalli,
Controlled sensing for multihypothesis testing,
\emph{IEEE Trans. Automat. Control} \textbf{58} (2013), 2451--2464,
arXiv:1205.0858v6.
\bibitem{ZSV} R. Zheng, R. Sim and A. Varvitsiotis,
Solving imperfect-recall games via sum-of-squares optimization,
arXiv:2602.21722v1 (2026).
'''
bib=bib.replace('\\end{thebibliography}',extra+'\n\\end{thebibliography}')
reconstructed=body
for pp in reversed(patches): reconstructed=reconstructed.replace(pp['new'],pp['old'],1)
if reconstructed!=text[text.index(marker):text.index('\\begin{thebibliography}')]:raise RuntimeError('Old mathematical body not fully retained')
(H/'main.tex').write_text(pre+(H/'introduction.tex').read_text()+'\n\\input{foundations}\n'+body+bib)
manifest={'old_main_git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'patches':patches,'old_substantive_proof_blocks':body.count('\\begin{proof}'),'unchanged_modules':[p.name for p in H.glob('*.tex') if (O/p.name).exists() and p.read_bytes()==(O/p.name).read_bytes()]}
(H/'ASSEMBLY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')

