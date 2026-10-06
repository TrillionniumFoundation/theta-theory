#!/usr/bin/env python3
"""Complete the unpublished v90 response without changing earlier paper editions."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) == 2 else Path('papers/GTF-I-v90-operational-memory')
BASELINE = json.loads((ROOT / 'V89_BASELINE.json').read_text())['files']
CHANGES = {}

def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('Patch anchor is absent or ambiguous: ' + old[:100])
    return text.replace(old, new, 1)

def write(name, text):
    path = ROOT / name
    old = path.read_bytes()
    digest = hashlib.sha256(old).hexdigest()
    archive = ROOT / 'staged-v90-audit' / name
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        raise RuntimeError('Refusing to overwrite staged source archive: ' + name)
    archive.write_bytes(old)
    if name in BASELINE and digest == BASELINE[name]:
        predecessor = ROOT / 'predecessor-v89-audit' / name
        predecessor.parent.mkdir(parents=True, exist_ok=True)
        if predecessor.exists() and predecessor.read_bytes() != old:
            raise RuntimeError('Predecessor collision: ' + name)
        predecessor.write_bytes(old)
    path.write_text(text)
    CHANGES[name] = {'staged_sha256': digest, 'completed_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

name = 'sections/82-operational-memory-hierarchy.tex'
s = (ROOT / name).read_text()
s = replace_once(s, 'has two decisions, not a request to identify every member of the ensemble.',
                 'has a binary hypothesis decision, not a request to identify every member\nof the ensemble.')
s = replace_once(s, 'Every effect is strictly positive for $t<1$.', r'''Every effect is strictly positive for $t<1$.
Taking the partial trace in \eqref{eq:basismoments90} gives
$\sum_b w_bE_y^b(t)=C_y$.  Thus the two hypotheses have identical
one-call channels, including on entangled inputs, and the one-call
optimum is $p_E$.  The two-call signal concerns a device chosen once;
it is absent if the alternative is independently redrawn at each call.''')
s = replace_once(s, 'when $U^*U=A$ and $V^*V=B$, even if the receiving spaces are larger.', r'''when $U^*U=A$ and $V^*V=B$, even if the receiving spaces are larger.
If $\tr A\tr B>0$, equality in the upper bound holds if and only if
$A=(\tr A)I/d$ and $B=(\tr B)I/d$.''')
s = replace_once(s, '''eigenvalues in the orthogonal complement.
\\end{proof}''', r'''eigenvalues in the orthogonal complement.
For the equality assertion, put $f=\|\sqrt A\sqrt B\|_1$ and
$a=\tr A$, $b=\tr B$.  Equality in the stated bound, with $ab>0$,
forces equality in both $\tr(AB)\ge f^2/d$ and $f^2\le ab$.
The variational formula for the trace norm and equality in
Hilbert--Schmidt Cauchy--Schwarz imply $B=(b/a)A$: indeed a maximizing
unitary $U$ has $\sqrt B U=c\sqrt A$, and multiplication by its
adjoint gives this proportionality.  Equality in the first inequality
makes all eigenvalues of $\sqrt A B\sqrt A$ equal and positive.
Consequently $A=(a/d)I$ and $B=(b/d)I$.  These scalar matrices plainly
attain the bound.  This also excludes equality at nonzero singular
factors.
\end{proof}''')
s = replace_once(s, '''entered the upper bound.

For attainment,''', r'''entered the upper bound.
For $t>0$, the equality case of Lemma~\ref{lem:swapfilter90} also shows
that a nonrandomized protocol attaining this bound in the displayed
purified normal form must satisfy
$A_{yh}=(\tr A_{yh})I/d$ and $B_{yh}=I/d$ on every nonzero branch.
All deficits in the summed upper bound are nonnegative, so equality
forces their branchwise vanishing.  Summing over $h$ then gives
$C_0^*C_0=I/d$.  Maximal mixing is thus a consequence of equality,
not a restriction imposed on the competing protocols.  This statement
concerns the purified normal form, not uniqueness of its dilations
or of the final readout.

For attainment,''')
s = replace_once(s, '''This is the usual two-step causal trace constraint, unchanged by full
transpose; it also follows by applying normalization successively to
the second and first channel slots.  In particular,
$0\\preceq T_{0,yy}\\preceq\\Xi_y$ and $\\tr\\Xi_y=1$.''', r'''Here is a direct realization of these constraints in the present
classical-output interface.  Purify the initial state as
$|\psi\rangle\in I_1\otimes R$, and let $\mathcal A_y$ be the
trace-preserving intervening map from $R$ to $I_2\otimes R'$ after
observing $y$.  Put
\[
 X_y=(\operatorname{Id}_{I_1}\otimes\mathcal A_y)
                 (|\psi\rangle\langle\psi|),\qquad
 \Xi_y=\tr_{R'}X_y,\qquad
 \rho=\tr_R|\psi\rangle\langle\psi|.
\]
Positivity and trace preservation give the displayed marginal equations.
If $F_{yz}$ is the final receiver effect for decision $C$, then
\[
 T_{0,yz}=\tr_{R'}\bigl[(I_{I_1I_2}\otimes\sqrt{F_{yz}})
           X_y(I_{I_1I_2}\otimes\sqrt{F_{yz}})\bigr].
\]
The Choi contraction \eqref{eq:choiconvention90} gives its Born
probability, and $0\preceq F_{yz}\preceq I$ gives
$0\preceq T_{0,yz}\preceq\Xi_y$.  This also proves positivity of the
complement, without an input-dimension factor from a normalized Choi
state.  In particular $\tr\Xi_y=1$.''')
write(name, s)

name = 'memory_check.py'
s = (ROOT / name).read_text()
s = replace_once(s, "    S=swap(2); minus=(s.eye(4)-S)/2", """    S=swap(2); minus=(s.eye(4)-S)/2
    for y in range(2):
        require(sum((E[y] for E in B),s.zeros(2))/6==I/2,'one-call averaged channel')
        checks+=1""")
s = replace_once(s, "        checks+=2\n    for t in", """        bound=s.Rational(d-1,2*d)*sum(a)*sum(b)
        scalar=(len(set(a))==1 and len(set(b))==1 and a[0]>0 and b[0]>0)
        require(bool(negative==bound)==scalar,'filtered-swap equality characterization')
        checks+=3
    for t in""")
s = replace_once(s, "    checks+=1\nsinglet=", """    require(bool(s.sqrt(AB.det())<s.trace(A)*s.trace(B)/4),'noncommuting factors are not equality cases')
    checks+=2
singlet=""")
write(name, s)

name = 'README.md'
write(name, '''# General Theta Foundations I — Revision 90

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This is the completed response to R59. The controlling external report is pinned at `a7d030d635a2bb40c8b4f7f2265df877bad95492`; its companion proof/pipeline audit is pinned at `994c41dbeec1da13b6b6486876855fa30ad7cfd5`. Both are frozen verbatim in this directory. The reviewed v89 is `df7ed618813224b058b97c6cbda720ad936e2c53`. The paper topic and four-leading-general-mathematics-journal objective are unchanged.

### Mathematical contribution and reading route

The primary retains the fixed-tube discrimination trichotomy, the complete profile second moment `V=sum n_r^2`, and the hard reset-policy square budget `Q`. Its new Section 82 proves a finite-ensemble operational separation, not merely strict inclusion of tester sets. For a once-selected basis device, input dimension `d>=2`, deformation `0<=t<=1`, and `L=2(d+1)-t^2`, the three exact optimal Bayes values are

```
classical complete-measure-and-reprepare: (d+1)/L
unit reset, unrestricted receiver:       (d+1)/L+t^2(d-1)/(2dL)
all two-call adaptive protocols:         (d+1+t^2)/L.
```

The qubit instance gives `3/5 < 13/20 < 4/5`. The upper for unit reset includes arbitrary receiver instruments and classical feedback. A filtered-swap identity, with its exact equality condition, proves the upper; independent maximally entangled pairs attain it. The all-adaptive upper now has a direct circuit-to-tester derivation of positivity, complement positivity and causal marginals. A first-moment identity explains why a single call, or independently redrawing the alternative each call, cannot supply the same signal.

Read `paper.pdf` / `quantitative.tex` first; `BINARY_SUPPLEMENT.pdf` / `supplement.tex` contains the linked current dependency proofs and preserved auxiliary consequences. `STRUCTURAL_PAPER.pdf` / `structural.tex` is the source-unchanged independent structural article. `COMPLETE_REVISION.pdf` / `main.tex` is the complete research archive, not a second submission. `RESPONSE_TO_REFEREE.md` answers R01–R15 and D01–D30; `PIPELINE_DERIVATION_V90.md` gives the proof chain, and `LITERATURE_AUDIT.md` records the primary-source comparisons.

### Preservation and verification

All 710 predecessor native files are preserved at their active paths or in the byte-identical `predecessor-v89-audit` records. All 998 predecessor complete-edition labels remain active. The earlier mathematical sections retain their complete text, with only registered additive convention paragraphs; relocating auxiliary sections to the linked supplement does not delete them. `staged-v90-audit` preserves the exact v90 staging files subsequently refined during completion.

```sh
python build_revision.py --check-source
python memory_check.py
python budget_domain_check.py
python build_revision.py --preflight         # local check, not publication qualification
python build_revision.py --isolated          # run at the exact native-source Git commit
python build_revision.py --verify-published  # read-only publication/final-head reconstruction
```

The production build runs all 30 regression suites normally and under `python -O`, reconstructs the complete native archive, and rebuilds the standalone journal package. Exact source, page and artifact identities are in `evidence/BUILD_RECEIPT.json` and its linked manifests. The root final-head request is only a request; only the separately observed read-only Actions receipt qualifies the exact final SHA.

The finite game is a binary decision on a finite ensemble with a shared hidden device index across its two uses. It is not an arbitrary fixed-pair theorem or a complete ancillary-memory-dimension hierarchy. Fixed-tube constants are still fixed-object dependent. Regression and reconstruction do not certify mathematical originality, physical reset calibration, independent human review, or the separate A2/B4/C2/eleven-paper/whole-program analytic closures.
''')

name = 'RELEASE_PROVENANCE.md'
s = (ROOT / name).read_text()
s += '''

## R59 completion and the previously unpublished v90

The original v90 staging commit `3d5192c15146a69083ade48cf1a249b836eef936` triggered run `37344375428`. Its local native commit and reconstructed PDFs were archived in artifact `11360597012`, but the publication step failed because the PDF paths were ignored by Git. No native v90 paper was pushed by that run. The recovered artifact is an inspected input, not the new publication's qualification.

The completion branch is `revision/general-theta-foundations-i-v90-r59-completion-2026-10-06`. It retains the staging payload and adds exact patch anchors, a source-preserving completion audit, the filtered-swap equality proof, a direct adaptive tester normalization, fresh first-moment/equality regressions and corrected current-version documentation. A new actual native Git commit must be built and reconstructed from scratch. Its publication child adds only the four PDFs and evidence files, using explicit force-add for those ignored publication outputs. The native and publication aliases have `completion` in their names and do not replace the old response branch.

A separate metadata-only request triggers the read-only final-head job. That job checks out its triggering SHA with no write credentials, verifies the publication against its native parent, reconstructs both archives and uploads an external receipt. The read-only final-head artifact is deliberately not committed back to the very head it verifies. Neither this document nor an in-progress workflow is a success receipt. Native and publication pushes are atomic and non-force; unrelated paper paths and review branches are untouched.
'''
write(name, s)

name = 'RESPONSE_TO_REFEREE.md'
s = (ROOT / name).read_text()
s += '''

## Completion of the unpublished v90 response

The completion retains the exact staged Section 82 under `staged-v90-audit/` and strengthens the written argument rather than reusing the failed publication as evidence. Lemma `lem:swapfilter90` now proves that its nonzero equality cases are exactly scalar positive factors; the reset proof explains the resulting branchwise isotropy in its purified normal form. The arbitrary-adaptive upper constructs its positive tester blocks, positive complements and causal marginals directly from the initial purification and intervening trace-preserving maps. The first-moment identity explicitly distinguishes a once-selected alternative device from independently redrawn alternatives. The exact finite suite checks the added identities and equality counterexamples under both Python modes.

The current README and release account supersede inherited v89 headings without erasing the original records. The controlling R59 report and full pipeline audit remain byte-identical. Contemporary literature was checked again against the original arXiv texts (Zonnios–Binder, Proposition 2, Theorem 1, Corollary 1; Ohst et al., Definition 23, equation (64), Theorem 24 and Section 6.2; Eid–Quintino's classical-label-plus-Lueders-state interface). This is a documented source comparison, not an independent human priority opinion. Publication and exact-final-head qualification must be newly observed for the completion commit.
'''
write(name, s)

(ROOT / 'COMPLETION_AUDIT.json').write_text(json.dumps({
    'schema': 'gtf90.completion/1',
    'controlling_report_commit': 'a7d030d635a2bb40c8b4f7f2265df877bad95492',
    'controlling_pipeline_commit': '994c41dbeec1da13b6b6486876855fa30ad7cfd5',
    'staging_commit': '3d5192c15146a69083ade48cf1a249b836eef936',
    'recovered_artifact_id': 11360597012,
    'recovered_artifact_is_current_qualification': False,
    'changes': CHANGES,
    'external_human_priority_clearance': False,
    'new_build_and_exact_final_head_required': True
}, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': 'success', 'changed': sorted(CHANGES)}, sort_keys=True))
