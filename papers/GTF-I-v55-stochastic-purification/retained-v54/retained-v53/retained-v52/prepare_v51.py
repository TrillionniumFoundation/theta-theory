"""Assemble v51 from the verified v50 source plus the new native modules.

Only this revision directory is written. Run once on its work branch before
creating the native-source commit; an isolated core needs only build.py.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

HOME=Path(__file__).resolve().parent
OLD=HOME.parent/'GTF-I-v50-compatible-simplex'
REVIEW='ca5efb0e6e50c1deb267f8b6f98551ff56197890'
BASE='2024b419eab2e6e6d34a21c9bec2a18b6afb6222'
PIN='1576f10fdf0b7000dde3ee02acc7499e5076effd979e10967756aed8a14ce4eb'

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name:str,obj:object)->None:(HOME/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def loaded(root:Path)->list[Path]:
    seen:set[Path]=set();out:list[Path]=[]
    def visit(p:Path)->None:
        if p in seen:raise ValueError('Repeated active input '+str(p))
        seen.add(p);out.append(p)
        for n in re.findall(r'\\input\{([^}]+)\}',p.read_text()):
            q=root/n
            if not q.suffix:q=q.with_suffix('.tex')
            if not q.is_relative_to(root):raise ValueError('Input outside manuscript')
            visit(q)
    visit(root/'main.tex');return out

def main()->None:
    manifest=OLD/'evidence/SOURCE_HASHES.json'
    if digest(manifest)!=PIN:raise ValueError('Frozen source manifest changed')
    original=json.loads(manifest.read_text())
    for n,h in original.items():
        if digest(OLD/n)!=h:raise ValueError('Frozen source mismatch: '+n)
    oldactive=loaded(OLD)
    labels=sorted(set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in oldactive))))
    dump('EXPECTED_V50.json',{'publication':BASE,'validated_source':'ee887bf04d8265cfbc23e4b4693dd1a8645a7505','source_manifest_sha256':PIN,'loaded_files':[str(p.relative_to(OLD)) for p in oldactive],'loaded_labels':labels})
    copied:dict[str,dict]={}
    names=[n for n in original if n.startswith('inherited/') and Path(n).suffix in {'.tex','.py'}]
    names+=['compatible-simplex.tex','orthogonal-circuit.tex','certificate-complexity.tex']
    for n in names:
        dest=HOME/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((OLD/n).read_bytes())
        copied[n]={'v50_sha256':original[n],'amendments':[]}
    (HOME/'check_v50.py').write_bytes((OLD/'check_revision.py').read_bytes())
    copied['check_v50.py']={'v50_path':'check_revision.py','v50_sha256':original['check_revision.py'],'amendments':[]}
    def patch(n:str,a:str,b:str,why:str)->None:
        p=HOME/n;text=p.read_text()
        if a not in text:raise ValueError('Expected editorial anchor absent: '+n+' '+a[:60])
        p.write_text(text.replace(a,b));copied[n]['amendments'].append(why)
    patch('compatible-simplex.tex',r'\eta_N',r'\eta_N(\calA,\rho)','Expose alphabet and signal dependence of the compactness threshold')
    patch('compatible-simplex.tex','The theorem does not assert all-width classification.','A single reflection is not a half-turn: the latter cannot preserve a triangle. Two distinct reflections in the triangular group have product of order three. The arbitrary-width counterpart is Theorem~\\ref{thm:finitegroup51}.','Clarify reflection classification and cross-reference the new all-width theorem')
    p=HOME/'compatible-simplex.tex'
    text=p.read_text().replace('number of command cuts whose available width is $D+1$.','number of command cuts whose available width is $D+1$, including cuts $0$ and $N$ when they have that width.')
    text=text.replace('a word with exactly one $-I$ exist.','a word with exactly one $-I$ and all other letters equal to $I$ exist.')
    text=text.replace('a binary outcome pair forces the sum of its coefficients to be one.','each binary outcome pair forces the sum of its coefficients to be one.')
    text=text.replace('The rank hypothesis is decisive.','At a rank-tight cut, full column rank of $E_t$ also excludes a label unreachable from every prefix: such a label would give a zero column. The rank hypothesis is decisive.')
    text=text.replace('The enclosed crosspolytope prevents degeneracy.','This first extraction runs over horizons. The enclosed crosspolytope prevents degeneracy.')
    text=text.replace('choose a convergent subsequence of the bounded vertex\ntuples.','choose a convergent subsequence of the bounded vertex\ntuples along this one nested chain. This is the second extraction.')
    text=text.replace('Nevertheless, for every $0<a\\le1/D$','Here $a$ is an inradius parameter, not a command letter. Nevertheless, for every $0<a\\le1/D$')
    p.write_text(text);copied[p.name]['amendments'].append('Clarify binary normalization, charged unused labels, endpoints, identity padding, two extractions and inradius notation')
    patch('orthogonal-circuit.tex','Every separate matricization','Every nontrivial separate matricization','Exclude trivial flattenings')
    patch('orthogonal-circuit.tex','query is $e_{000}$.','query is $e_{000}$; the fixed ninth coordinate is never queried.','State the unqueried coordinate explicitly')
    patch('orthogonal-circuit.tex','$c\\rho/5$, strictly smaller','$c\\rho/5=40\\rho/357$ (binary-TV error $20\\rho/357$), strictly smaller','Separate scaled mean and TV flattening bounds')
    p=HOME/'orthogonal-circuit.tex';text=p.read_text();text+='\nThe spherical embedding uses $2|F_w|\\le1+F_w^2\\le1+\\sum_vF_v^2$, so $|cF_w|\\le1$. Its dimension $2^n+1$ prices the full binary word table; it is not a polynomial-size encoding in $n$.\n';p.write_text(text)
    copied[p.name]['amendments'].append('Spell out the spherical-coordinate bound and exponential representation size')
    patch('certificate-complexity.tex','bits. This bound is on the record data, not a polynomial-time search.','bits. This record bound excludes the input, sign-coverage data, bases and algebraic isolating intervals; each must also be supplied and charged. It is not a polynomial-time search bound.','Price the auxiliary data excluded by the record count')
    patch('inherited/hankel-compatibility.tex',r'\cite{GTF33}',r'\cite{BF03,BF04}','Use the classical positive-intertwining antecedent; internal genealogy is in the audit')
    p=HOME/'inherited/hankel-compatibility.tex';text=p.read_text().replace('issue was already explicit in the earlier lift formulation','issue is the classical positive-intertwining requirement');p.write_text(text)
    patch('inherited/word-profiles.tex','This is the conditional-centroid mechanism of \\cite{GTF35,GTF42}, now applied to the optimized finite word datum.','This is the conditional-centroid mechanism just proved, applied to the optimized finite word datum.','Replace internal citation with the complete local proof')
    patch('inherited/word-profiles.tex','The cap union estimate below is the geometric certificate already used in the predecessor packet method \\cite{GTF35}.','The cap union estimate below supplies a direct geometric certificate.','Move predecessor genealogy to the audit')
    patch('inherited/arithmetic-scales.tex','This is the previously established matched law \\cite{GTF42}.','The following proof derives this matched law from the stated finite-scale estimates.','Reference the retained proof instead of the revision identifier')
    patch('inherited/encoding-and-comparison.tex',r'\cite{BF04,GTF33}',r'\cite{BF03,BF04}','Conventional positive-realization comparison')
    patch('inherited/encoding-and-comparison.tex','Scalar reduction and sign obstruction in revision 47\n\\cite{GTF47}','Scalar reduction and sign obstruction in\nSection~\\ref{sec:binary47}','Use the active local proof reference')
    patch('inherited/encoding-and-comparison.tex','Prior packet and Diophantine proofs\n\\cite{GTF35,GTF42,GTF43}','Packet and Diophantine proofs in\nSections~\\ref{sec:profiles} and~\\ref{sec:arithmetic}','Use the retained active arithmetic proofs')
    # Bibliography changes are editorial; no mathematical statement is removed.
    p=HOME/'inherited/references.tex';text=p.read_text()
    text=re.sub(r'\\bibitem\{GTF(?:33|35|42|43|47)\}.*?(?=\\bibitem|\\end\{thebibliography\})','',text,flags=re.S)
    additions=r'''
\bibitem{BF03} L. Benvenuti and L. Farina,
Minimal positive realizations: A survey of recent results and open problems,
\emph{Kybernetika} \textbf{39} (2003), 217--228.
\bibitem{BF99} L. Benvenuti and L. Farina,
An example of how positivity may force realizations of ``large'' dimension,
\emph{Systems Control Lett.} \textbf{36} (1999), 261--266.
\bibitem{Yannakakis} M. Yannakakis,
Expressing combinatorial optimization problems by linear programs,
\emph{J. Comput. System Sci.} \textbf{43} (1991), 441--466.
\bibitem{RogersShephard} C. A. Rogers and G. C. Shephard,
The difference body of a convex body,
\emph{Arch. Math.} \textbf{8} (1957), 220--233.
\bibitem{NTZ26} J. Nie, X. Tang and J. Zhou,
Robust completion for rank-1 tensors with noises,
\emph{J. Sci. Comput.} \textbf{107} (2026), Art. 100,
doi:10.1007/s10915-026-03306-8.
'''
    p.write_text(text.replace(r'\end{thebibliography}',additions+'\n'+r'\end{thebibliography}'))
    copied['inherited/references.tex']['amendments'].append('Move internal version bibliography to history; add named classical and current primary comparisons')
    # Correct native cross-reference and reuse the existing bibliography keys.
    p=HOME/'reachable-lifts.tex';p.write_text(p.read_text().replace(r'\ref{sec:machine}',r'\ref{sec:model}'))
    p=HOME/'literature-and-resources.tex';p.write_text(p.read_text().replace('{KKKR}','{KKKR17}').replace('{GS}','{GS19}'))
    preamble=(OLD/'main.tex').read_text().split(r'\title[')[0]
    maintext=preamble+r'''\title[Compatible lifts and stochastic width]{General Theta Foundations I: \\
Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width}
\author{Qian Qi}
\date{27 September 2026; revision 51}
\subjclass[2020]{Primary 93B15, 52B05; Secondary 68Q45, 60J10}
\keywords{Positive realization, stochastic width, compatible lifts, finite groups, quantitative stability}
\begin{document}
\begin{abstract}
We study finite stochastic realizations of controlled orthogonal experiments
with signed spanning seeds and coordinate readout. Reachable probability
sections give a rank-sensitive polyhedral description at arbitrary width
and a local cubic real-algebraic realization criterion. Exact clocked
width is bounded over all horizons if and only if the command group is
finite; a stationary permutation realization then exists. A one-surplus
rank decomposition yields an eventual exact six-state frontier for
three-dimensional signed-permutation alphabets containing the identity
and antipodal maps. At rank-tight cuts, explicit recovery from the seed
anchor matrix makes the simplex occupation bound stable under positive
error, without accumulation over the horizon. In dimension two this
proves a four-state frontier on a horizon-independent error interval.
The complete two-state sign--magnitude alternative, a rational orthogonal
example with a cubic optimum beyond separate flattenings, and the
arithmetic and finite-bit realization theorems are retained. All width
statements distinguish persistent labels from the description and
computational cost of the transition rows.
\end{abstract}
\maketitle
'''
    order=['introduction.tex','inherited/machine-model.tex','inherited/hankel-compatibility.tex','reachable-lifts.tex','all-width-rigidity.tex','compatible-simplex.tex','stable-occupation.tex','orthogonal-circuit.tex','inherited/introduction.tex','inherited/two-state-compatibility.tex','inherited/magnitude-duality.tex','inherited/exact-error-examples.tex','certificate-complexity.tex','inherited/encoding-and-comparison.tex','literature-and-resources.tex']
    appendices=['inherited/inherited-statements.tex','inherited/finite-horizon-certificates.tex','inherited/word-profiles.tex','inherited/distortion-rate.tex','inherited/circle-optimization.tex','inherited/arithmetic-scales.tex','inherited/metric-width.tex','inherited/irrational-fluctuations.tex','inherited/finite-bit-memory.tex','inherited/comparison.tex']
    maintext+=''.join('\\input{'+n+'}\n' for n in order)+'\\appendix\n'+''.join('\\input{'+n+'}\n' for n in appendices)+'\\input{inherited/references.tex}\n\\end{document}\n'
    (HOME/'main.tex').write_text(maintext)
    for n,entry in copied.items():entry['v51_sha256']=digest(HOME/n)
    dump('PRESERVATION_MANIFEST.json',{'schema':'gtf51.preservation/1','review_commit':REVIEW,'v50_publication':BASE,'policy':'All original mathematical modules are loaded; copied-file edits are disclosed. Old repository paths and branches are not modified. The old introductory summary is replaced, preserving its equation labels.','files':copied})
    # Adapt the previously executed build engine; use the actual input graph for preservation.
    build=(OLD/'build.py').read_text().replace('v50','v51').replace('V50','V51').replace('gtf50','gtf51')
    build=build.replace("REVIEW='d9f3273b3575517cc54054a79412fe3d09378fa7'",'REVIEW='+repr(REVIEW)).replace("BASE='0a33f027a9088c4a55542efcd2784de95f43f557'",'BASE='+repr(BASE))
    build=build.replace("sha(HOME/'inherited'/name)","sha(HOME/name)").replace("EXPECTED_V49.json","EXPECTED_V50.json")
    oldline="current_tex='\\n'.join(p.read_text() for p in sources() if p.suffix=='.tex' and p.name!='main.tex')"
    newlines="""def active(p:Path,seen:set[Path])->list[Path]:
        if p in seen:raise RuntimeError('Repeated manuscript input '+str(p))
        seen.add(p);out=[p]
        for n in re.findall(r'\\\\input\\{([^}]+)\\}',p.read_text()):
            q=HOME/n
            if not q.suffix:q=q.with_suffix('.tex')
            if not q.is_relative_to(HOME):raise RuntimeError('Input outside manuscript')
            out.extend(active(q,seen))
        return out
    actual_inputs=active(HOME/'main.tex',set())
    current_tex='\\n'.join(p.read_text() for p in actual_inputs)
    save('ACTIVE_INPUTS.json',[str(p.relative_to(HOME)) for p in actual_inputs])"""
    if oldline not in build:raise ValueError('Build input-graph anchor changed')
    build=build.replace(oldline,newlines)
    build=build.replace("[('v51','check_revision.py',HOME),('v49'","[('v51','check_revision.py',HOME),('v50','check_v50.py',HOME),('v49'")
    build=build.replace("args=parser.parse_args();EV.mkdir(exist_ok=True)","args=parser.parse_args();EV.mkdir(exist_ok=True)\n    for stale in EV.glob('page-*.png'):stale.unlink()")
    build=build.replace("'v49_publication':BASE","'v50_publication':BASE").replace("v49 publication: `{BASE}`","v50 publication: `{BASE}`").replace('Controlling r31','Controlling r32').replace('Response to r31','Response to r32')
    build=build.replace('Compatible Simplices and Exact Stochastic Width','Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width')
    build=build.replace('New results: rank-tight simplex equivalence; a dimension-dependent occupation bound for separated minimal-rank cuts; an exact four-state planar frontier; all-horizon invariant-simplex rigidity; exact distortion/enclosure separation; a noncommuting three-epoch orthogonal cubic optimum exceeding every separate flattening bound; explicit sign-certificate and algebraic-output bounds.','New results: arbitrary-width reachable sections and a local cubic realization criterion; all-width finite-group rigidity and stationarization; a one-surplus occupation bound and eventual exact six-state frontier; explicit stable rank-tight occupation and a horizon-independent positive-error four-state interval. The earlier exact finite, arithmetic and finite-bit results remain loaded.')
    build=build.replace('Generic all-width optimization, uniform exact algebraic sampling, independent priority certification and A2/B4/C2/eleven-paper closure are not inferred.','A general optimization engine, sharp variational constants, a noisy all-width classification, uniform exact algebraic sampling, independent priority certification and unrelated analytic-pipeline closure are not inferred.')
    (HOME/'build.py').write_text(build)
    docs={
    'README.md':'''# General Theta Foundations I — Revision 51

**Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width**  
Qian Qi · 27 September 2026

[Article](paper.pdf) · [Native source](main.tex) · [Response to r32](RESPONSE_TO_REFEREE.md) · [Build receipt](evidence/BUILD_RECEIPT.json) · [Referee package](evidence/REFEREE_PACKAGE.zip)

The new proofs give reachable sections at arbitrary width, a local cubic real-algebraic characterization of prescribed profiles, an all-width finite-group criterion for bounded exact clocked width, an eventual exact six-state frontier in dimension three, and an explicit positive-error four-state frontier in dimension two. The precise seed, command and error hypotheses are stated in each theorem. The variational six-state gap is not assigned an unproved numerical value. The real-algebraic criterion is not an implemented general optimizer.

For planar signed-permutation alphabets containing I and −I, signal 1/10, horizon at least 16 and binary-TV error at most 1/200000, the optimal width is exactly four. The zero-error horizon-14 sufficient bound remains in the article. Neither first horizon is claimed sharp.

Build with Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7 and TeX Live with AMS, Latin Modern, microtype, mathtools, geometry, booktabs and hyperref:

```sh
python check_revision.py
python -O check_revision.py
python build.py --check-core
```

Extract `evidence/CORE_SOURCES.zip` and run `python GTF-I-v51-compatible-lifts/build.py --core-only` for an isolated build. No earlier revision is needed for that command. `prepare.py` is the repository-only assembly step and is not required in the isolated core.

The old paper and all historical branches remain unchanged. Every original active mathematical module is retained; copied-file editorial edits and hashes are listed in the preservation manifest. The actual input graph is checked, not an unloaded archive. All sources are readable native text, not an opaque payload. The final receipt records executed checks, not an advance assertion of success.
''',
    'HISTORY_AUDIT.md':'''# Historical derivation and preservation audit — v51

The controlling r32 review is ca5efb0e6e50c1deb267f8b6f98551ff56197890; v50 publication is 2024b419eab2e6e6d34a21c9bec2a18b6afb6222 and its validated source is ee887bf04d8265cfbc23e4b4693dd1a8645a7505. The v50 source manifest is pinned by SHA-256 before assembly.

## Directly inspected mathematical ancestry

The v50 article and r32 report were read, including the rank-tight proof, both compactness extractions, the exact four-state bound, the orthogonal cubic example, and the complete response/certificate pipeline. All active mathematical modules are retained in this revision.

Revision 33, `papers/GTF-I-v33-compatible-lifts/`, was inspected in the controlling review tree: README, main, machine-model, compatible-lifts, literature-and-scope, and references. Its reachable affine sections, stochastic extension alternative, exact quarter-defect example, and rational-rotation lower bound are genuine predecessors. The reachable-section principle and the fixed-section linear dual are therefore not claimed as v51 inventions. The present additions are the arbitrary-dimensional controlled rank stratification, the binomial vertex count, the bounded projector formula, all-width finite-group rigidity, one-surplus occupation and the explicit robust anchor argument. The earlier commuting irrational/rational rotation obstruction is not relabelled as a new example; the new fixed-dimensional noncommuting family illustrates the broader theorem.

Internal article references to revisions 33, 35, 42, 43 and 47 are replaced by active local proof references or properly identified classical antecedents. Their original papers remain in the repository. The v50 preservation chain retains the v49 two-state duality, v47 scalar/compatibility results and v44 arithmetic/word-profile/finite-bit source. No original theorem label is removed from the loaded mathematical article.

## Analytic pipeline examined, not silently certified

`ROUND17_PROOF_DEPENDENCY_LEDGER.md` was inspected at the controlling review commit. Its principal chains are A2 → A3 → A4 → C2 → D1, and B2-GC → B1 → B2-MC → B3 → B4 → C1 → C2 → D1, with A1 independent. The raw returned Fourier estimates, stopped entropy-controlled LDP, one global past kernel, source-dependent canonical saddle, process Gaussian/Mosco limit, nonlinear resolvent and graph-core construction, regular filter/QMD, operator-domain response and latent-phase contraction remain separate model-specific obligations.

`ROUND12_HISTORICAL_DERIVATION_AUDIT.md` was also inspected. Its local mechanisms and interface warnings are retained as history, not imported by status words into a finite-dimensional theorem. The new manuscript neither deletes those papers nor uses its finite tests to assert their analytic closure.

## Reproducibility boundary

`EXPECTED_V50.json` is generated from the actual v50 input graph. `PRESERVATION_MANIFEST.json` records hashes and edits of copied sources. The build rejects loss of any original active label, validates all named finite examples in normal and optimized Python, and rebuilds the isolated core. This is a reproducibility audit, not proof-assistant certification or an exhaustive review of every historical archive.
''',
    'LITERATURE_AUDIT.md':'''# Primary literature comparison — v51

The conventional comparison is in the article, Section `sec:resources51`, not only in this process record. The following primary texts or their author versions were inspected for the named statements; bibliographic metadata alone is not treated as a theorem audit.

* Benvenuti–Farina, Kybernetika 39 (2003), 217–228: Section 3, Example 4 and Theorem 2. The periodic Hankel counterexample and nonnegative intertwining condition directly precede the compatibility issue. Original publisher PDF: https://www.kybernetika.cz/content/2003/2/217/paper.pdf . Parsed theorem and example text were read; the attempted web screenshot failed. The 1999 fixed-degree/unbounded-order result is credited through its original bibliographic reference and the inspected 2003 discussion, not falsely described as a fresh full-proof audit of the 1999 paper.
* Benvenuti–Farina, IEEE TAC 49 (2004), 651–664: Theorem 2 and the invariant-cone reconstruction, read in the full author PDF at https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf . The stationary cone criterion is distinguished from independently chosen clocked multi-command realizations.
* Yannakakis, JCSS 43 (1991), 441–466: the slack-factorization theorem is credited as classical. Its explicit statement and bounded-extension proof were inspected in the primary author exposition of Faenza–Fiorini–Grappe–Tiwary, https://arxiv.org/pdf/1105.4127, Theorem 1 and Lemma 1. No full original-Yannakakis proof audit is asserted.
* Kahle–Kubjas–Kummer–Rosen, SIAM J. Applied Algebra and Geometry 1 (2017), 200–221: https://arxiv.org/pdf/1605.01678, Proposition 2.2, Remarks 2.3 and 2.5, Proposition 2.7. Zero consistency, toric relations, nonsquare-free tensor circuits and real signs are compared with the bounded interval problem, not claimed as new algebra.
* Gillis–Shitov, LAA 581 (2019), 367–382: https://arxiv.org/pdf/1706.00078, Lemma 1 and Theorem 3, including a rendered page of the fixed-sign argument. Fixed-sign matrix feasibility and unrestricted NP-completeness are credited; the tensor extensions are not described as a new matrix LP or a polynomial sign-search algorithm.
* Nie–Tang–Zhou, Journal of Scientific Computing 107 (2026), article 100, published 12 May 2026: https://link.springer.com/article/10.1007/s10915-026-03306-8, Theorem 3.1, proof and Remark 3.2(i). Local noisy observed-tensor recovery under identifiability assumptions is distinguished from an all-machine width lower bound with explicit seed-derived constants.

Rogers–Shephard's classical simplex difference-body identity is explicitly credited and its elementary proof is included in the manuscript. Real-algebraic elimination, Farkas separation and static extension principles are tools, not claimed inventions. This targeted audit is not exhaustive priority clearance, and it makes no claim about papers not inspected.
''',
    'RESOURCE_LEDGER.md':'''# Resource ledger — v51

The same five distinctions appear in the article: atomic-row label existence; real-algebraic synthesis; rational description length; finite-bit implementation; uniform computation and exact sampling. A persistent private selector is always charged. The clock, horizon-specific transition program and exact real rows are not automatically charged by W_N,epsilon. Algebraic input and output require an explicit representation when computational claims are made.

The local projector system has polynomial description size in an explicitly expanded clock and profile, not polynomial elimination time. The new checker verifies supplied finite identities and examples, not an optimizer over unknown lifts. The two-state sign procedure takes the full response table. The full binary-table orthogonal embedding has dimension 2^n+1. Circuit-record bit counts exclude input, sign coverage, bases and isolating intervals, whose costs remain additional.

Exact width does not imply a uniform bounded-time sampler for arbitrary real probabilities. The retained finite-bit theorems have their own assumptions and are not silently substituted for atomic exact-row results.
''',
    'REVISION_SCOPE.md':'''# Scope and theorem status

The new article enlarges the mathematics rather than replacing it with a narrower venue recommendation. It proves arbitrary-width section geometry and a local exact criterion, all-width finite-group rigidity, a one-surplus exact six-state frontier, and quantitative rank-tight stability with a uniform positive-error four-state interval. Every theorem keeps its seed, query, alphabet, signal, dimension and exact/approximate hypotheses.

The all-width and six-state expansion constants are strictly positive variational gaps, not closed-form sharp rates. The local real-algebraic existence/synthesis theorem is not an implemented general optimizer. The approximate result is rank-tight; an approximate arbitrary-width group classification is not asserted. All prior active mathematical results are preserved in the body and appendices. Build success does not imply independent mathematical certification, exhaustive priority clearance, journal acceptance or analytic closure of the other papers.
'''}
    for n,text in docs.items():(HOME/n).write_text(text)
    dump('PIPELINE_STATUS.json',{'schema':'gtf51.pipeline/1','review_commit':REVIEW,'finite_theorems_self_contained':True,'analytic_closure_inferred':False,'other_paper_paths_modified':False,'inspected_ledgers':['ROUND17_PROOF_DEPENDENCY_LEDGER.md','ROUND12_HISTORICAL_DERIVATION_AUDIT.md'],'analytic_obligations':['returned Fourier','stopped LDP','global past kernel','canonical conditioning','process Gaussian and Mosco','nonlinear resolvent','regular filter and QMD','operator-domain response','latent-phase contraction']})
    dump('PROOF_STATUS.json',{'schema':'gtf51.proofs/1','new_labels':['thm:section51','cor:surplus51','thm:local51','prop:dual51','lem:compact51','thm:occupation51','thm:finitegroup51','cor:rational51','thm:surplus-budget51','lem:anchor51','thm:robust51','cor:robust-four51'],'proofs_in_native_manuscript':True,'general_optimizer_implemented':False,'variational_constants_numerically_evaluated':False,'independent_certification':False,'execution_receipt':'evidence/BUILD_RECEIPT.json'})
    now='\n'.join(p.read_text() for p in loaded(HOME))
    missing=set(labels)-set(re.findall(r'\\label\{([^}]+)\}',now))
    if missing:raise ValueError('Lost active labels: '+repr(missing))
    print(json.dumps({'status':'native-source-prepared','copied_sources':len(copied),'original_active_labels':len(labels),'new_active_files':len(loaded(HOME))}))

if __name__=='__main__':main()
