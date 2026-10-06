#!/usr/bin/env python3
"""One-time source assembly. Create immutable objects only, never refs or commits."""
from pathlib import Path
import base64,hashlib,json,os,sys,urllib.request

repo=Path.cwd()
root=repo/'papers/A2-DYN-v24-referee-response'
base=repo/'papers/A2-DYN-v23-referee-response'
sys.path.insert(0,str(root/'tools'))
import verify_v24 as verify

PROVISIONAL='527c500456ba3e622237e3983383ede1893d7b24'
BASE_TREE='37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9'
if verify.tree_hash(base).hex()!=BASE_TREE:
    raise RuntimeError('recovered baseline tree mismatch')

abstract_add=r'''
A multiscale comparison over the actual return-clock deviations gives
fourth-root stopping errors in every fixed finite moment and Gaussian
polynomial moments with one actual-return insertion. Combined with
finite-order damped unsmoothing, it preserves the original marked
central error rate on a wider prescribed-count Fourier band.
'''
intro=r'''
\begin{maintheorem}[Multiscale stopping and a rate-preserving band]
\label{thm:intro-multiscale-stopping}
For the actual return record and insertion convention of Theorems C and D,
let $\mathcal G_d(D)$ denote the degree-$d$ moment tensor of $N(0,D)$.
For every fixed integer $d\ge1$, put $\rho_d=1/2$ for odd $d$ and
$\rho_d=1$ for even $d$. Then
\begin{align*}
 &\left\|\int_{Y_R^*}a((F_R^*)^kx)
       \left(\frac{U_{n,R}(x)}{\sqrt n}\right)^{\otimes d}\dd\nu(x)
                      -\alpha_a\mathcal G_d(D_R)\right\|\\
 &\hspace{15mm}\le C_d\left(M_an^{-1/4}+(M_a+V_a)n^{-\rho_d}\right).
\end{align*}
In particular, the actual normalized covariance and its induced Cesaro
formula converge to $D_R$ at rate $O(n^{-1/4})$. Moreover,
\begin{align*}
 &n^2\int_{2n^{-99/200}\le|z|\le2n^{-633/1400}}
                    |\Phi^{[k],a}_{n,R}(z)|\dd z
      \le C\left(M_an^{-3/280}+V_an^{-983/350}\right),\\
 &\int_{|v|\le2n^{67/1400}}
       |C^{[k],a}_{n,R}(v)-\alpha_a e^{-v^{\mathsf T}D_Rv/2}|\dd v\\
 &\hspace{15mm}\le C\left(M_an^{-3/280}\sqrt{\log(2+n)}
                                   +V_an^{-9/175}\right).
\end{align*}
The estimates are uniform in $R$, the prescribed sufficiently large
return count $n$, and one arbitrary mark $0\le k\le n$. The two support
radii are $2n^{-633/1400}$ physically and $2n^{67/1400}$ after rescaling.
No return-count averaging or normalization by annular volume is used.
The same-event consequence retains the original probability and variation
budget of Theorem C on this larger band.
\end{maintheorem}
\begin{proof}
Apply Theorems~\ref{thm:multiscale-marked-stopping},
\ref{thm:all-marked-gaussian-moments}, and
\ref{thm:rate-preserving-annulus}, together with
Corollary~\ref{cor:rate-preserving-same-event}.
\end{proof}

'''
route=r'''
Sections~\ref{sec:multiscale-stopping} and~\ref{sec:rate-preserving-band}
replace a single stopping window by disjoint dyadic deviation shells.
A deterministic maximal estimate and the actual clock tails yield a
fourth-root comparison in every fixed finite moment. Anchored mixed
cumulants then identify every fixed marked Gaussian moment. Combining
the same stopping estimate with damped cubic unsmoothing proves Theorem N:
the wider band retains the original central rate. Its weighted raw
identity uses a newly defined kernel and keeps the remaining local edge,
complementary residual, and long-time derivative terms explicit.

'''
changes=[
 ('revision identity','A2-DYN, revision 23','A2-DYN, revision 24'),
 ('abstract addition',r'\end{abstract}',abstract_add+r'\end{abstract}'),
 ('Theorem N synopsis',r'\paragraph{From Gaussian laws to raw local inversion.}',intro+r'\paragraph{From Gaussian laws to raw local inversion.}'),
 ('proof route',r'\paragraph{Relation to the limit theory of billiards.}',route+r'\paragraph{Relation to the limit theory of billiards.}'),
 ('new proof inclusions',r'\input{core/49_wider_fixed_count_band}',r'\input{core/49_wider_fixed_count_band}'+'\n'+r'\input{core/50_multiscale_stopping}'+'\n'+r'\input{core/51_rate_preserving_band}')
]
text=(base/'main.tex').read_text()
edits=[]
for reason,before,after in changes:
    if text.count(before)!=1:
        raise RuntimeError('nonunique introduction edit: '+reason)
    text=text.replace(before,after,1)
    edits.append({'path':'main.tex','reason':reason,'before':before,'after':after})
(root/'main.tex').write_text(text)
ledger={'revision':24,'baseline_recovery_commit':'699f17e6bd75c3c8a741a9f00837ab4654e8c3d1',
 'baseline_paper_tree':BASE_TREE,'edits':edits}
(root/'INHERITED_EDITS.json').write_text(json.dumps(ledger,indent=2,sort_keys=True)+'\n')
manifest={
 'revision':24,'active_directory':'papers/A2-DYN-v24-referee-response',
 'baseline_directory':'papers/A2-DYN-v23-referee-response','baseline_paper_tree':BASE_TREE,
 'baseline_recovery_commit':'699f17e6bd75c3c8a741a9f00837ab4654e8c3d1',
 'staged_v23_commit':'ca2b585c126a0f100d6ab16cb491615f7cd7c770',
 'controlling_review_commit':'d21f74a59eed269c4b215c53b85434a3a449c779',
 'controlling_review_blob':'b5e96b424ca9d73fc1c113142556cc8913281ca7',
 'reviewed_v22_author_commit':'a656998fee8176316850ef87ac447970d712aae2',
 'baseline_sha256':{p.relative_to(base).as_posix():verify.digest(p) for p in verify.ordinary(base)},
 'source_sha256':{p.relative_to(root).as_posix():verify.digest(p) for p in verify.ordinary(root) if p.name!='SOURCE_MANIFEST.json'},
 'preservation':'All 49 recovered core files, all inherited Python sources and references.tex are byte-identical. Five exact edits affect main.tex only. All old labels remain.',
 'quarter_order_stopping_proved':True,'all_fixed_marked_moments_proved':True,'rate_preserving_band_proved':True,
 'full_raw_LLT_proved':False,'full_fixed_return_complementary_integral_proved':False,
 'uniform_long_time_raw_derivative_bound_proved':False,'exact_physical_event_replacement_proved':False,
 'independent_human_review':False,'formal_proof_certificate':False
}
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
checks=verify.source_checks()
finite=verify.finite_checks()
expected=verify.tree_hash(root).hex()

api='https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/'
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json',
 'Content-Type':'application/json','User-Agent':'a2-dyn-exact-source-assembly'}
def post(endpoint,body):
    if endpoint not in ('blobs','trees'):
        raise RuntimeError('immutable Git objects only')
    request=urllib.request.Request(api+endpoint,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(request,timeout=60) as response:
        return json.load(response)
entries=[]
for name in ('main.tex','INHERITED_EDITS.json','SOURCE_MANIFEST.json'):
    data=(root/name).read_bytes()
    actual_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    created=post('blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})
    if created['sha']!=actual_blob:raise RuntimeError('uploaded blob mismatch '+name)
    entries.append({'path':name,'mode':'100644','type':'blob','sha':created['sha']})
created=post('trees',{'base_tree':PROVISIONAL,'tree':entries})
if created['sha']!=expected:raise RuntimeError('completed tree differs from verified source')
receipt={'paper_tree':created['sha'],'baseline_tree':BASE_TREE,'assembly_event_sha':os.environ.get('GITHUB_SHA'),
 'assembly_run_id':os.environ.get('GITHUB_RUN_ID'),'changed_blobs':entries,
 'source_summary':{k:v for k,v in checks.items() if k!='source_sha256'},'new_finite_checks':finite,
 'ordinary_source_created':True,'branch_refs_changed':False,'commits_created':False,
 'native_final_build_certified':False,'continuum_proof_certified':False}
Path('v24-assembly-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
