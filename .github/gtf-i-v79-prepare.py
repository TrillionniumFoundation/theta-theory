from pathlib import Path
import hashlib, json, re, shutil, importlib.util
REPO=Path(__file__).resolve().parents[1]
P=REPO/'papers/GTF-I-v78-block-resource-learning'; R=REPO/'papers/GTF-I-v79-joint-interior-coding'
spec=importlib.util.spec_from_file_location('oldbuild', P/'build_revision.py'); old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
inv=old.sources(P)
assert len(inv)==360
changed=['main.tex','quantitative.tex','build_revision.py','journal_verify.py','publish_revision.py','README.md','RESPONSE_TO_REFEREE.md','HISTORY_AND_PIPELINE_AUDIT.md','LITERATURE_AUDIT.md','INDEPENDENT_REVIEW_BRIEF.md','PROOF_AUDIT.md','PROOF_STATUS.json','RESOURCE_LEDGER.json','RESOURCE_LEDGER.md','CONTROLLING_REPORTS.json','PRESERVATION_MANIFEST.json','PROOF_TEXT_PRESERVATION.json']
for name in changed:
 p=R/'predecessor-v78-audit'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/name,p)
intro=(P/'editions/operational-introduction78.tex').read_text()
new=r'''
\subsection{Dimension-uniform operational descriptions}
The interior learning result has a matching description theory.
For $\mathfrak I_d=[I_d/4,3I_d/4]$, all $d,N\ge1$ and
$0<\delta\le2^{-13}$, Theorem~\ref{thm:interiorentropy79} gives
\begin{equation}\label{eq:introinteriorentropy79}
 \left(\frac{\sqrt N}{2048\delta}\right)^{d^2}
 \le\mathcal C_N(\mathfrak I_d,\delta)
 \le\left(\frac{25\sqrt N}{\delta}\right)^{d^2}.
\end{equation}
The constants are absolute and the lower bound allows arbitrary
legal binary centres.  Theorem~\ref{thm:interiorcodec79} realizes
the upper bound by finite exact rational comparison and public
reconstruction.  Unlike entrywise transmission, its index does not
incur a $d^2\log d$ penalty.  Its length is
\[
 A_d(N,\delta)+O(d^2),\qquad
 A_d(N,\delta)=\tfrac12d^2\log_2N+d^2\log_2(1/\delta),
\]
uniformly in dimension, horizon and accuracy.

If shared randomness and a worst-target failure probability $\eta$
are allowed, Theorem~\ref{thm:prefixrate79} determines the optimal
expected one-way prefix length as
$(1-\eta)A_d(N,\delta)+O(d^2)$, uniformly for $0\le\eta\le1/8$.
The lower bound allows a randomized decoder and counts all nonpublic
information.  The upper bound uses a public target-independent
abort event; its flag is not a hidden transmission.
Finally, Theorem~\ref{thm:interiorlearnedcode79} gives one common
finite-output learner with the joint optimal orders
$M=\Theta(d^2N\delta^{-2})$ and $B=A_d(N,\delta)+O(d^2)$ at
failure $1/8$, using independent one-call acquisitions.  This is a
query and communication result; trusted tomography synthesis and
exhaustive decoder computation are separate costs.
The absence of the endpoint logarithm in
\eqref{eq:introinteriorentropy79} identifies the different interior
law without changing the retained complete-body theorem.

'''
intro=intro.replace(r'\subsection{Prior work and organization}',new+r'\subsection{Prior work and organization}')
intro=intro.replace('joint dimension bounds, and finite-control\nconstruction then identify', 'joint dimension bounds, uniform interior descriptions, and finite-control\nconstruction then identify')
(R/'editions/operational-introduction79.tex').write_text(intro)
comp=(P/'editions/operational-comparison78.tex').read_text()
comp=comp.replace('All matrix entropy constants are fixed-dimensional and the\nmatching entropy and payload orders have a small-error range.', 'The closed-body entropy constants remain fixed-dimensional and its\nmatching entropy and payload orders have a small-error range.\nIn contrast, Theorem~\\ref{thm:interiorentropy79} has explicit\ndimension-uniform constants on $[I/4,3I/4]$. Its norm-ball volume\nargument and the Fano--Kraft proof of\nTheorem~\\ref{thm:prefixrate79} use standard mechanisms. Their role\nis to derive the precise future-loss description statements, not to\nclaim priority for volume comparison or information inequalities.\nThe learned-description theorem credits the Mele--Bittel estimator\nand retains its ideal trusted operations; it adds finite-output\ncoarsening and a public dictionary without extra device calls.')
(R/'editions/operational-comparison79.tex').write_text(comp)
for name in ['main.tex','quantitative.tex']:
 s=(P/name).read_text().replace('operational-introduction78','operational-introduction79').replace('operational-comparison78','operational-comparison79')
 s=s.replace(r'\input{sections/60-dimension-accuracy-learning}',r'\input{sections/60-dimension-accuracy-learning}'+'\n'+r'\input{sections/61-joint-interior-coding}')
 if name=='quantitative.tex':
  s=s.replace('Thus independent one-call acquisition has linear future-horizon cost', 'On the same interior we prove a dimension-uniform covering law,\na finite exact index length\n$(d^2/2)\\log_2N+d^2\\log_2(1/\\delta)+O(d^2)$,\nand simultaneous query-optimal learning and transmission.\nAllowing shared randomness and failure probability $\\eta$ changes\nthe leading optimal expected prefix length by the factor $1-\\eta$.\nThus independent one-call acquisition has linear future-horizon cost')
 else:
  s=s.replace('and Theorem~\\ref{thm:finitecontrollearning78}', 'Theorems~\\ref{thm:interiorentropy79}--\\ref{thm:interiorlearnedcode79}\n(joint interior descriptions and learning),\nand Theorem~\\ref{thm:finitecontrollearning78}')
 (R/name).write_text(s)
# Registry manifests preserve the actual immediate baseline, distinct from reviewed v77.
graphs={entry:{'files':sorted(old.graph(P,entry)[0]),'labels':old.graph(P,entry)[1]} for entry in old.DOCUMENTS}
manifest={'schema':'gtf79.preservation/1','base_commit':'1906166f98f47f4fe387143617948766395ba186','native_source_commit':'f893d00e51bf008c530de6046b008a3237001f81','source_root':'papers/GTF-I-v78-block-resource-learning', 'source_inventory_sha256':hashlib.sha256((json.dumps(inv,indent=2,sort_keys=True)+'\n').encode()).hexdigest(),'files':inv,'archived_originals':{n:'predecessor-v78-audit/'+n for n in changed},'prior_labels':graphs['main.tex']['labels'],'prior_proof_graphs':graphs,'focused_relocations':{},'editorial_reordering':'No inherited proof section or active label is removed or relocated. New Section 61 is active in both mathematical editions; changed front matter and metadata have byte-exact archived originals.'}
(R/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
proof={'schema':'gtf79.proof-text-preservation/1','predecessor':manifest['base_commit'],'byte_identical_sections':sorted(str(p.relative_to(P)) for p in (P/'sections').glob('*.tex')),'new_sections':['sections/61-joint-interior-coding.tex'],'removed_proof_sections':[],'reviewed_additive_changes':[],'editorial_changes':{'main.tex':'Add full new section without changing inherited section text.','quantitative.tex':'Integrate uniform coding and retained full-body results.','editions/operational-introduction79.tex':'Preserve all predecessor introduction labels in a new edition and add statements.','editions/operational-comparison79.tex':'Preserve comparison labels and update the now false universal fixed-dimensional-entropy sentence.'},'scope':'Byte preservation and active graph identity, not independent validation of every historical proof.'}
(R/'PROOF_TEXT_PRESERVATION.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
controls=json.loads((P/'CONTROLLING_REPORTS.json').read_text());controls['revision']=79;controls['source_baseline_head']=manifest['base_commit'];controls['source_baseline_native']=manifest['native_source_commit'];controls['relationship']='Further response to the same R51 reports on v77, building on already-landed v78; no R52 or review of v78 is invented.'
(R/'CONTROLLING_REPORTS.json').write_text(json.dumps(controls,indent=2,sort_keys=True)+'\n')
status=json.loads((P/'PROOF_STATUS.json').read_text());status['revision']=79
status['external_status']['review_round']+=' Revision 79 further responds to those same reports; no external review of v79 has been obtained.'
status['evidence_boundary']='Written proofs, exact finite regression, build identity and human specialist review remain distinct. No new independent agent or human review is claimed for v79.'
status['new_revision_79']={'interior_entropy':'Explicit dimension-free constants; arbitrary legal lower centres; d,N>=1 and delta<=2^-13.','exact_interior_codec':'Finite exact PSD decisions, complete reconstruction and 5delta/16 error; supplied Gaussian-rational target or certified approximation; no polynomial-time claim.','prefix_rate':'Shared and private randomness allowed; one-way seedwise prefix-free words; expected worst-target length; Fano--Kraft lower and public-erasure upper.','learned_word':'Existing Mele--Bittel tomography plus interior clipping and finite-output coarse graining; ideal trusted operations, risk1/8; jointly optimal query and fixed-decoder length orders.'}
status['current_execution_evidence']['historical_v78_final_run']='37209850660, predecessor only'
(R/'PROOF_STATUS.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
print('predecessor',len(inv),'labels',{k:len(v['labels']) for k,v in graphs.items()},'sections',len(proof['byte_identical_sections']))
