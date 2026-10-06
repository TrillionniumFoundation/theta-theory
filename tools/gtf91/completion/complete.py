#!/usr/bin/env python3
"""Complete the pinned native R60 response; never overwrite prior audit bytes."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path('papers/GTF-I-v91-reset-variational').resolve()
HERE = Path(__file__).resolve().parent
PINNED = 'd28546aad99cd1ce3846ca74ccedb90c24ebd37b'
EXPECTED = {
 'sections/83-reset-variational-principle.tex':'df1a88a48e6d4fb3fdd550108f9a987084d4915842355d23a130cc81d687615c',
 'sections/84-equal-prior-memory-hierarchy.tex':'687049a2cba6221a9cbf9216d65405e82b7a76978f5508bec18f94de37eaa554',
 'editions/operational-introduction91.tex':'fe75f9b3b984e42a377cd1f0ecbde62180964eccef319d0659136dfcc011809b',
 'quantitative.tex':'1c67c7623db71f6b48b57d29782cdf4ea47f8b7f711372a2fab4897237423097',
 'README.md':'cfba43b416cb1cfdb4d8cad28ad02a2dbf0170e32c677262adf465805c959cb2',
 'RESPONSE_TO_REFEREE.md':'bed10d941bc3efc0f9f95c5bad4072cd961f26cbe0aff050ebf9cce5cfc33c84',
 'PROOF_AUDIT.md':'2fb1917806fe67f532bed2e310855b085a4b247d16dcdd767174b13d1ce69bf8',
 'HISTORY_AND_PIPELINE_AUDIT.md':'275e7b4e6528d0dde13528f5ee8c5772a3fd99e0c88d4961cdd442a37f504100',
 'INTERNAL_MATHEMATICAL_REVIEW.md':'6fb2d2bd69814098cfe0f62e938b134b461f74741b71a86062c124df805693dc',
 'PROOF_STATUS.json':'c9e22654a4597489af3e47e936ed4a5fa6bdbf8cfab2402db07b89d927f3233f',
 'build_revision.py':'b95502ce8c723710b7c86ab464e92c01b3e851b3c96f1e64f34dbe658ee77ea8',
 'RELEASE_PROVENANCE.md':'f57fc5de771f7d1935e3b47424446954032f4e1d4807992f479598481eabd803',
 'LITERATURE_AUDIT.md':'d5e7e457028856cfb7131e8e27ea0ed0d608b86ce7b571f1641a151b3ce0d1a8',
}
sha=lambda data:hashlib.sha256(data).hexdigest()
if (ROOT/'STAGED_V91_BASELINE.json').exists():
    raise RuntimeError('Completion has already been applied')
for name,digest in EXPECTED.items():
    if sha((ROOT/name).read_bytes()) != digest:
        raise RuntimeError('Pinned staging file changed: '+name)
spec=importlib.util.spec_from_file_location('staged_v91_build',ROOT/'build_revision.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
baseline={'commit':PINNED,'files':old.sources(ROOT),'graphs':{}}
for entry in old.DOCS:
    files,labels=old.graph(ROOT,entry)
    baseline['graphs'][entry]={'files':sorted(files),'labels':sorted(labels)}
changes={}
def replace(text,anchor,new):
    if text.count(anchor)!=1:raise RuntimeError('Ambiguous patch anchor: '+anchor[:90])
    return text.replace(anchor,new,1)
def write(name,text):
    path=ROOT/name;previous=path.read_bytes();archive=ROOT/'staged-v91-audit'/name
    if archive.exists():raise RuntimeError('Audit path already exists: '+name)
    archive.parent.mkdir(parents=True,exist_ok=True);archive.write_bytes(previous)
    path.write_text(text)
    changes[name]={'before':sha(previous),'after':sha(path.read_bytes())}

name='sections/83-reset-variational-principle.tex'
s=(ROOT/name).read_text()
s=replace(s,'all classical records are retained.  Public randomization and the',
          'all classical records are retained.  Finite or countable public\nrandomization and the')
s=replace(s,'Choi tester tuples are included in each class.  Early stopping is',
 r'''Choi tester tuples are included in each class.  General public seed laws
are included through this closure: their finitely many tester coordinates
are limits of finite convex combinations.  Early stopping is''')
s=replace(s,'Every unit-reset strategy has a purification, still respecting the reset',
          'Every implemented unit-reset strategy has a purification, still respecting the reset')
s=replace(s,'Zero-probability histories require no extra assumption.\n\\end{lemma}',
 r'''Zero-probability histories require no extra assumption.
The tester closure in Definition~\ref{def:classes91} is used by continuity
of decision values; no physical dilation is assumed for an abstract
limit before its value has been realized by the finite optimization.
\end{lemma}''')
s=replace(s,'cannot increase the supremum of a linear reward.  Countable records\nand tester limits follow from the preceding lemma and continuity.',
 r'''cannot increase the supremum of a linear reward.  More explicitly,
for seed law $q_s$ and first coefficient maps $C_{0,s}$, take
$C_0=\bigoplus_s\sqrt{q_s}C_{0,s}$ and measure the seed register
as part of the first receiver instrument.  The branch maps are
$C_{y,(s,h)}=\sqrt{q_s}V_{ysh}C_{0,s}$, and their Gram sum is
$\sum_sq_sC_{0,s}^*C_{0,s}=C_0^*C_0$ for every $y$.
The fresh rule retains its dependence on $(s,y,h)$, entirely on the
fresh side of the cut.  Thus the original seeded decision statistics
are recovered.  Countable records and tester limits follow from the
preceding lemma and continuity.''')
s=replace(s,'\\begin{corollary}[Label feedback versus receiver feedback]',
          (HERE/'contact.tex').read_text()+'\\begin{corollary}[Label feedback versus receiver feedback]')
write(name,s)
name='sections/84-equal-prior-memory-hierarchy.tex'
write(name,(ROOT/name).read_text()+(HERE/'rigidity.tex').read_text())
name='editions/operational-introduction91.tex'
s=(ROOT/name).read_text().replace('Both statements concern the same classical-output','These results concern the same classical-output')
s=replace(s,'\\subsection{Notation, organization and scope}',r'''The variational and equality statements also have quantitative forms.
Corollary~\ref{cor:contactdefect91} decomposes a certified reward loss
into nonnegative spectral, majorization, and leaf-decision defects.
Lemma~\ref{lem:stableswap91} and Corollary~\ref{cor:resetstability91}
control, at the relative scale $\varepsilon/t^2$, the deviation of
near-optimal reset Gram matrices from scalar matrices.  This concerns
the selected normal form, not unique dilations or physical calibration.

\subsection{Notation, organization and scope}''')
write(name,s)
name='quantitative.tex'
s=(ROOT/name).read_text()
s=replace(s,'the shared latent law.  We retain the complementary local geometric',
 r'''the shared latent law.  A quantitative equality estimate controls the
Gram marginals of near-optimal reset strategies.  We retain the complementary local geometric''')
write(name,s)

name='build_revision.py';s=(ROOT/name).read_text()
labels=[]
for n in old.NEW_SECTIONS:
    labels+=re.findall(r'\\label\{((?:thm|lem|prop|cor):[^}]+)\}',(ROOT/n).read_text())
s=re.sub(r'^NEW_LABELS=.*$', 'NEW_LABELS='+repr(labels),s,count=1,flags=re.M)
s=replace(s,"'equal_prior_check.py')","'equal_prior_check.py','rigidity_check.py')")
s=replace(s,"    require(not(set(graphs['quantitative.tex']['labels'])&set(graphs['supplement.tex']['labels'])),",'''    staged=json.loads((ROOT/'STAGED_V91_BASELINE.json').read_text())
    require(staged['commit']=='d28546aad99cd1ce3846ca74ccedb90c24ebd37b','wrong staged v91 identity')
    for name,digest in staged['files'].items():
        require(name in inv,'staged native file removed: '+name)
        if inv[name]!=digest:
            require(sha((ROOT/'staged-v91-audit'/name).read_bytes())==digest,
                    'staged native file not preserved: '+name)
    for entry,prior in staged['graphs'].items():
        require(set(prior['labels'])<=set(graphs[entry]['labels']),
                'staged v91 active label lost: '+entry)
    require(not(set(graphs['quantitative.tex']['labels'])&set(graphs['supplement.tex']['labels'])),''')
s=replace(s,"'new_theorems':NEW_LABELS,'regression_suites':len(SCRIPTS),'graphs':graphs}",
 "'new_theorems':NEW_LABELS,'regression_suites':len(SCRIPTS),'graphs':graphs,\n      'staged_v91_source_files':len(staged['files']),'staged_v91_source_preserved':True}")
write(name,s)
shutil.copy2(HERE/'rigidity_check.py',ROOT/'rigidity_check.py')
name='PROOF_STATUS.json';status=json.loads((ROOT/name).read_text())
status['new_labels']=labels;status['executed_scope']['regression_suites']=33
status['new_claims'].update({'quantitative_primal_dual_defect_identity':True,
 'stable_centered_swap_equality':True,'near_optimal_reset_gram_rigidity':True,
 'gram_weights_are_history_probabilities':False,'unique_instrument_dilation_rigidity':False})
write(name,json.dumps(status,indent=2,sort_keys=True)+'\n')
summary='''

## R60 completion: quantitative optimality and normalization

The already landed v91 native source at `d28546aad99cd1ce3846ca74ccedb90c24ebd37b` is preserved by `STAGED_V91_BASELINE.json` and `staged-v91-audit/`. Its existing general variational theorem, classical pure-atom criterion, and both exact hierarchies remain active. The completion adds Corollary `contactdefect91` in Primary Section 15 and Lemma `stableswap91` / Corollary `resetstability91` in Primary Section 17. Printed numbers and pages are generated from the actual manuscript, not inferred from source-module numbers.

The general defect identity separates spectral slack, all-density majorization slack and leaf optimization loss, each nonnegative. The stable centered-swap equality bounds the squared trace distances of both normalized Gram factors from the scalar density by `K_d Delta`, with `c_d=d-1-1/d` and `K_d=d(1+9/(2c_d))`. The proof keeps the two nonnegative defects `1-f^2` and `tr(ab)-f^2/d` and handles singular states using a unitary extension of the polar factor. Summation over the complete reset normal form gives weighted near-optimal rigidity at the explicit relative scale `epsilon/t^2`. Gram weights, actual history probabilities, uniqueness of dilations and physical reset calibration are explicitly distinguished.

The normal-form text also gives an explicit direct-sum realization of public seeds and distinguishes implemented protocols from abstract norm-closure limits. This does not narrow the optimized class: general seed laws and tester limits retain their continuous values, and the finite maximizing realization still attains the full class optimum. The added `rigidity_check.py` has exact diagonal, singular, complex noncommuting, dual-defect and normalization fixtures; no finite check replaces a universal proof. There are now 33 production regression suites, with actual execution status recorded only in the build receipt.
'''
for name in ['README.md','RESPONSE_TO_REFEREE.md','PROOF_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md','INTERNAL_MATHEMATICAL_REVIEW.md']:
    s=(ROOT/name).read_text().replace('32 suites','33 suites').replace('32 regression suites','33 regression suites')
    write(name,s+summary)
name='RELEASE_PROVENANCE.md';s=(ROOT/name).read_text().replace('32 regression suites','33 regression suites')
s+='''

## Completion branch and actual prior-run status

The preceding v91 workflow run `37402552173` was cancelled after its native source had reached the remote as `d28546aad99cd1ce3846ca74ccedb90c24ebd37b`; it did not establish a qualified publication. The new branch `revision/general-theta-foundations-i-v91-r60-completion-2026-10-06` starts from that exact source. It preserves it, adds quantitative contact and near-optimality proofs, and creates a new native commit before reconstructing the manuscripts. No old artifact or cancelled run supplies current qualification.

The completion workflow pushes a single existing revision ref, without force and with its expected remote head checked, before the slow build. An artifact-only publication child is pushed after the isolated and standalone reconstructions. Native/publication aliases are separate API operations after their objects have been confirmed. A metadata-only final request then verifies its exact triggering head in a read-only job. Its receipt is external to the commit it verifies. The eventual root review entry must report actual job conclusions, SHA identities and any transport recovery; no prospective text here represents success.
'''
write(name,s)
name='LITERATURE_AUDIT.md';s=(ROOT/name).read_text()
s+='''

## Completion source recheck — 6 October 2026

The original texts were checked again: Ohst et al., arXiv:2411.08110v2, Definition 23 / equation (64) and Theorem 24; Zonnios–Binder, arXiv:2606.19511v1, Proposition 2, Theorem 1 and Corollary 1; Uhlmann, arXiv:1108.3218, with the Entropy 2010 journal record; and Boyd–Vandenberghe's official book, Sections 5.2.3 and 5.9.1. The current dual uses proper closed homogeneous hypograph cones, a positive-definite common barycenter and strictly negative heights, so its Slater step supplies dual attainment rather than just formal weak duality. The quantum/classical receiver comparison is not a first claim of memory-constrained optimization: the constrained-separability and autonomous-memory antecedents remain explicit.

The completion's quantitative contact identity is a nonnegative-slack refinement of the attained dual. The near-optimality estimate is proved directly from the centered-swap defect, polar decomposition and Hilbert–Schmidt inequalities. It does not claim a universal self-testing theorem or an identification of the physical implementation. Independent specialist assessment of the exact envelope and hierarchy statements remains outstanding; it is not supplied by the current source recheck or regression results.
'''
write(name,s)
(ROOT/'STAGED_V91_BASELINE.json').write_text(json.dumps(baseline,indent=2,sort_keys=True)+'\n')
(ROOT/'R60_COMPLETION_AUDIT.json').write_text(json.dumps({'schema':'gtf91.completion/1',
 'staged_source_commit':PINNED,'staged_source_files':len(baseline['files']),
 'controlling_external_commit':'cf13712c54e9ef0c9c54a240b1f26efc78cc3568',
 'controlling_pipeline_commit':'e4e72a512bf747e7bd190196cd8dc3db35689e3c',
 'changes':changes,'new_labels':['cor:contactdefect91','lem:stableswap91','cor:resetstability91'],
 'new_regression':'rigidity_check.py','production_suites':33,
 'current_publication_qualified_by_this_script':False,
 'independent_human_priority_clearance':False},indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'success','preserved_staged_files':len(baseline['files']),
 'changed_files':sorted(changes),'regression_suites':33},sort_keys=True))
