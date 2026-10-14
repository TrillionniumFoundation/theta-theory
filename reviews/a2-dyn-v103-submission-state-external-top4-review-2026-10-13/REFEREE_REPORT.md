# External top-four submission-state and supplementary referee report on A2-DYN v103

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Latest visible revision branch:** `revision/a2-dyn-v103-referee-response-2026-10-13`  
**Latest visible branch head:** `37faf38478a5b561c3aa4a1faf63da378caf8189`  
**Nature of that head:** existing external-review commit for revision 102, not a new author manuscript  
**Latest actual theorem-bearing author branches:** `revision/a2-dyn-v102-referee-response-2026-10-13`, `revision/a2-dyn-v102-referee-copy-2026-10-13`  
**Reviewed mathematical commit:** `0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`  
**Reviewed author repository tree:** `318f81a76c47dd69b7429bd205223ea5130bede9`  
**Active manuscript directory:** `papers/A2-DYN-v102-referee-response`  
**Existing full mathematical report:** `reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Existing report commit / blob:** `37faf38478a5b561c3aa4a1faf63da378caf8189` / `6c6bbd2fc9fd5e6da575ac6db9827448e091af3d`  
**Fresh exact-SHA qualification now observed:** response run `38374168103`, success; referee-copy run `38374176852`, success  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimal-geometry, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

There is no new revision-103 mathematical manuscript to review.

The only visible branch carrying the revision-103 label resolves to

`37faf38478a5b561c3aa4a1faf63da378caf8189`,

whose commit message is

`Review A2-DYN v102 at the top-four mathematics benchmark`.

Relative to the actual revision-102 author commit

`0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`,

that head is one commit ahead and adds exactly one file:

`reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md`.

It does not add a directory `papers/A2-DYN-v103-referee-response`, a revision-103 source manifest, a revision-103 qualification workflow, a revision-103 referee-copy author branch, or any theorem-bearing source. There is also no GitHub Actions run for the visible revision-103 branch. The revision-103 label is therefore a branch alias for an external-review commit, not a mathematical revision.

The latest actual author manuscript remains revision 102 at

`0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`.

That manuscript has already received a full 732-line top-four referee report. The report found substantial progress in the positive same-segment trace problem but identified one exact unresolved positive source. I have repeated a focused supplementary audit of the submission identity, the central scalar reduction, the final schedule, and the qualification evidence which was incomplete at the freeze of the existing report.

The mathematical assessment does not change. Revision 102 proves an essential-height estimate for the **admitted** positive paired trace, with rate

\[
O(B^{-1/384}),
\]

but leaves the complete positive transverse-failure source

\[
\mathsf U_B
\]

uncontrolled. Its final scalar theorem is

\[
\mathcal E_M
\le \mathcal H_M(\mathsf U_B)+C_MB^{-1/384}.
\]

No theorem proves

\[
\mathcal H_M(\mathsf U_B)\longrightarrow0.
\]

The manuscript further proves that, along the unchanged outer schedule, the original pointwise theorem is equivalent to this missing limit. The unresolved source is therefore the remaining upper obstruction itself, not a harmless remainder after the main theorem.

Successful completion of both exact-SHA qualification runs strengthens the source and build record. It does not supply the missing positive deconcentration theorem and does not alter the top-four recommendation.

## 2. Submission identity and chronology

The current submission state must be described by Git objects rather than by branch numbering alone.

### 2.1. Latest actual author source

The paired author branches

- `revision/a2-dyn-v102-referee-response-2026-10-13`;
- `revision/a2-dyn-v102-referee-copy-2026-10-13`

both resolve to

`0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`.

The active article is

`papers/A2-DYN-v102-referee-response/main.tex`.

The complete inherited article is compiled through

`papers/A2-DYN-v102-referee-response/supplement.tex`.

The author repository tree is

`318f81a76c47dd69b7429bd205223ea5130bede9`.

Revision 102 adds the three proof modules

- `core/244_barycentric_positive_trace_coarea.tex`;
- `core/245_transverse_clock_and_pointwise_trace_height.tex`;
- `core/246_transverse_certificates_and_scalar_schedule.tex`.

Its actual mathematical baseline is revision 100 uniform capacity at

`7b2d9c999e987f61a38e9fcadd7fd7605192f35a`.

### 2.2. Existing review commit

The full revision-102 report was added at

`37faf38478a5b561c3aa4a1faf63da378caf8189`.

That commit contains no author-source changes. It adds only

`reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md`.

The visible revision-103 response branch points to this review commit. A review commit must not be relabeled as evidence of a new author response.

### 2.3. Missing revision-103 author objects

At the freeze of this report there is no:

- `papers/A2-DYN-v103-referee-response` directory;
- revision-103 `main.tex`;
- revision-103 `SOURCE_MANIFEST.json`;
- revision-103 `RESPONSE_TO_REFEREE.md`;
- revision-103 qualification workflow;
- revision-103 referee-copy author branch;
- revision-103 exact-SHA qualification run; or
- commit containing revision-103 theorem-bearing changes.

The branch number alone cannot create a mathematical revision.

### 2.4. Consequence for this report

This report starts from the revision-103 alias head so that the complete revision-102 report remains in history. It adds only the present submission-state and supplementary assessment under

`reviews/a2-dyn-v103-submission-state-external-top4-review-2026-10-13/`.

No author paper, author revision ref, workflow, historical report, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Updated qualification evidence

The existing revision-102 report froze while the two dedicated exact-SHA workflows were queued:

- response run `38374168103`;
- referee-copy run `38374176852`.

Both have now completed successfully at the reviewed author SHA

`0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`.

Thus the current evidence establishes that both paired author branches were checked at the same exact SHA and passed the source-preservation, finite-fixture, native-build, archive, recorder-coverage, warning-gate and rendering protocol encoded in

`.github/workflows/a2-dyn-v102-qualification.yml`.

This corrects only the evidentiary timing statement in the existing report. It does not change any mathematical conclusion.

In particular, successful qualification does not certify:

1. the fixed-count decomposition into regular physical pairing chambers;
2. critical one-sided trace regularity;
3. the positive barycentric coarea identity on all relevant strata;
4. the transverse stopped-flow orientation and Jacobian convention;
5. multiplicity one after physical sheet summation and across compatible seams;
6. the capped-clock disintegration at the original target roof;
7. the relative two-ended certificate on the complete physical pairing family;
8. the inherited family-uniform pressure and uncut-gradient estimates;
9. decay of the positive transverse-failure source; or
10. the unrestricted exact-label raw local limit theorem.

The manuscript and validation contract correctly distinguish build qualification from proof certification.

## 4. Scope of this supplementary audit

The existing revision-102 report gives the detailed proof review. I repeated the portions most likely to change the recommendation or reveal a decisive internal error:

1. the exact positive same-segment trace minimum;
2. the barycentric representation of the paired source;
3. the transverse coordinate preserving relative endpoint position;
4. the paired-measure Jacobian;
5. the stopped transverse clock and multiplicity-one comparison;
6. the capped-clock finite-count inequality;
7. the relative two-ended sufficient certificate;
8. the inherited outer schedule and exponent arithmetic;
9. the exact definition of the nonadmitted failure source; and
10. the claimed equivalence between its height decay and the original upper pointwise theorem.

I found no new decisive sign contradiction, exponent error, missing segment-length factor, illegal collision-dependent cutoff, or hidden unweighted chamber-count factor within the admitted scope. The conclusion of the existing mathematical report therefore remains the controlling assessment.

## 5. The positive barycentric source

Revision 102 acts on the positive common boundary trace itself, rather than only on a signed trace difference. On a regular pairing chamber it writes

\[
 d\pi^\varepsilon
 =c^\varepsilon(\theta)\ell(\theta)\,d\theta\,ds,
 \qquad
 \mathscr F(\theta,s)=a(\theta)+s\ell(\theta),
\]

where

\[
 c^\varepsilon(\theta)
 =\min\{f^\varepsilon(a+,\theta),f^\varepsilon(b-,\theta)\}.
\]

This representation is materially stronger than a volume-collar estimate. It retains the positive minimum of the two endpoint traces and parametrizes the entire same-segment paired source by the relative position \(s\in[0,1]\).

On a regular chamber the transverse vector field is

\[
 V^\perp=(\partial_\theta\mathscr F)^{-1}\partial_\theta.
\]

If

\[
 v(\theta,s)=\partial_\theta\mathscr F(	heta,s)
\]

is nonzero, the paired measure in target-roof coordinates has density proportional to

\[
 \frac{c^\varepsilon(\theta)\ell(\theta)}{|v(\theta,s)|}.
\]

Within the stated regular scope, the factor of \(\ell\), the reciprocal transverse speed and the orientation of the stopped flow are consistent with the change of variables. I found no missing residence factor in this calculation.

## 6. What the transverse clock proves

The capped transverse clock averages the positive paired source over a bounded roof interval while preserving relative endpoint position. After physical sheets are summed, the manuscript obtains multiplicity one in the target direction and avoids an unweighted symbolic-word count.

For the admitted source it proves an estimate of the schematic form

\[
 \mathcal H_M(T_{\mathsf S,\mathrm{adm}}^\varepsilon)
 \le C\left(q_\perp^{-1}\varepsilon^{1/16}
 +q_\perp^{-1}(1+\varepsilon^{-1})\Delta\right)
\]

plus inherited faster-decaying terms.

This is genuinely a pointwise essential-height estimate for the positive admitted trace, not merely a mass estimate, a signed cancellation, a finite-\(p\) norm or an averaged-roof statement.

The theorem remains conditional on admission. The clock does not show that all physical paired mass is admitted, and it does not estimate the positive complement.

## 7. The two-ended certificate

The local certificate assumes on one angular side, at fixed relative position \(s\), that

\[
 |v|\ge\nu>0
\]

and that the logarithmic derivatives of the residence, the positive paired weight and the transverse speed are bounded by a constant \(A\). If the required transverse roof displacement is smaller than both the available angular reach and the logarithmic-control scale, then the clock accumulates a definite amount before leaving the regular side.

This explains an important feature: no lower bound on the original residence \(\ell(\theta_0)\) is intrinsically needed, because the residence factor in the paired density cancels against the time needed to traverse the target roof interval.

The certificate is a useful sufficient criterion. It is not a theorem that the criterion holds uniformly on the complete physical pairing family, and it does not show that failure of the criterion has small essential height.

In particular, at a backward-critical entrance one can have

\[
 v=s b'.
\]

The transverse speed may therefore vanish as \(s\downarrow0\). The corresponding positive critical trace is not removed and remains part of the failure source.

## 8. Schedule and exponent check

The inherited outer schedule is

\[
 \varepsilon(B)=A_0B^{-1/12},
 \qquad q_0^*=1/8,
 \qquad r_0=c\varepsilon^4,
 \qquad \delta=6q_0^*r_0.
\]

Revision 102 takes

\[
 \Delta=2\delta,
 \qquad r_\perp=\delta,
 \qquad q_\perp=\varepsilon^{1/32}.
\]

Then

\[
 q_\perp^{-1}\varepsilon^{1/16}
 =\varepsilon^{1/32}
 =O(B^{-1/384}),
\]

while

\[
 q_\perp^{-1}(1+\varepsilon^{-1})\Delta
 =O(\varepsilon^{95/32})
\]

and the inherited terms decay faster. Every threshold is fixed from the outer reconstruction parameter before the collision limit. I found no exponent or order-of-limits error in this scalar schedule.

The rate applies only to the admitted positive source.

## 9. The unresolved positive failure source

The complete positive trace is split exactly as

\[
 T_{\mathsf S}^{\varepsilon(B)}
 =T_{\mathsf S,\mathrm{adm}}^{\varepsilon(B)}+\mathsf U_B.
\]

The unresolved source \(\mathsf U_B\) can contain:

- zero transverse speed;
- insufficient one-sided angular reach;
- loss of pairing regularity;
- nonregular strata carrying positive paired mass;
- folds of endpoint roof maps;
- rapid logarithmic variation of residence, weight or speed;
- short comparison lifetimes; and
- positive backward-critical traces near the critical corner.

No estimate proves that this source has small total mass, weak type, bounded overlap, vanishing residence factor or essential height. Even a small total-mass statement would not by itself close the pointwise upper theorem.

The exact final reduction is

\[
 \mathcal E_M
 \le \mathcal H_M(\mathsf U_B)+C_MB^{-1/384}.
\]

The manuscript identifies the original upper pointwise assertion with

\[
 \mathcal H_M(\mathsf U_B)\to0.
\]

This is a useful sharpening of the obstruction. It is not its solution.

## 10. Consequences for the principal theorem

Because the positive failure source remains uncontrolled, revision 102 does not prove:

- the upper pointwise half of the exact-label theorem;
- the unrestricted exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- unrestricted forward essential-likelihood convergence;
- unrestricted total-variation or entropy consequences;
- arbitrary downstream point-conditioned laws whose normalization uses the missing upper theorem; or
- formal closure of the primary referee request.

No revision-103 source changes any item in this list.

## 11. Required changes before another substantive top-four review

### 11.1. Land an actual theorem-bearing author revision

The next revision label must point to an author commit containing a new manuscript directory or explicit in-place author-source changes. The author response and referee-copy branches, source manifest, article date, active directory and qualification workflow should identify the same mathematical SHA.

A review commit must not be relabeled as an author revision.

### 11.2. Control the entire failure source

The next mathematical revision must prove

\[
 \mathcal H_M(\mathsf U_B)\longrightarrow0
\]

under a legal outer schedule, or replace \(\mathsf U_B\) by a strictly smaller positive remainder whose decay is actually proved.

Renaming, repartitioning or adding another conditional admission layer is not enough.

### 11.3. Prove uniform admission or quantitative failure decay

A successful route could either:

1. prove that the relative two-ended certificate holds quantitatively on all physical pairs selected by the original source except a part already known to have vanishing ordered height; or
2. prove that failure of the certificate forces a geometric degeneracy whose physically summed positive trace has a schedule-compatible essential-height bound.

The proof must address zero speed, short angular reach, folds and rapid relative variation rather than assigning them to an uncontrolled positive remainder.

### 11.4. Treat backward-critical corners explicitly

At a critical entrance the positive trace is retained and \(v=s b'\) can vanish as \(s\downarrow0\). A successful argument should provide one of the following:

- a second transverse direction;
- a two-parameter coarea gain;
- a quantitative critical stratification;
- a maximal estimate strong enough for essential height;
- a schedule-compatible corner-capacity theorem; or
- a physical identity showing that the critical positive source is already paid elsewhere.

The backward-critical trace may not simply be set to zero.

### 11.5. Work after physical summation

Any sheetwise estimate must be formulated after physical summation or accompanied by a collision-uniform bounded-overlap or capacity theorem. An unweighted symbolic-word count or chamber count cannot appear in the final bound.

### 11.6. Retain the pointwise norm

A mass estimate, weak convergence, fixed finite-\(p\) control or averaged-roof statement does not close the theorem. The conclusion must imply essential-height decay with a rate compatible with

\[
 \varepsilon(B)\asymp B^{-1/12},
 \qquad \delta\asymp\varepsilon^4.
\]

### 11.7. Obtain independent specialist verification

Independent specialists should reconstruct at least:

- the regular physical chamber decomposition;
- one-sided critical trace regularity;
- the positive barycentric coarea identity;
- the transverse paired-measure Jacobian;
- the stopped-clock covariance convention;
- multiplicity one across physical summation and seams;
- the capped-clock disintegration;
- the two-ended logarithmic certificate;
- the inherited uniform pressure and uncut-gradient theorems; and
- the final argument controlling the complete failure source.

### 11.8. Preserve source and review identity

Future revision branches should begin from the latest report history if desired, but their final heads must be new author commits. Historical reports should remain immutable. New review branches should add reports only after freezing the author SHA.

## 12. Exposition and editorial strategy

The focused revision-102 article is substantially clearer than the complete 852-page archive. The following distinctions should remain explicit in any future revision:

1. admitted positive trace is not the full positive trace;
2. the transverse clock is not the physical roof flow;
3. the paired-measure Jacobian is not a volume Jacobian;
4. the two-ended certificate is sufficient, not necessary;
5. absence of a lower residence cutoff does not imply uniform admission;
6. the failure source is positive and may carry the complete upper obstruction;
7. a backward-critical trace may be nonzero;
8. the rate \(B^{-1/384}\) applies only to the admitted part;
9. exact-SHA qualification is not proof certification; and
10. unrestricted downstream claims remain subordinate to scalar closure.

Once the positive failure source is closed, the final submission should present a short proof dependency graph for the current theorem and retain the historical pipeline as a technical supplement rather than as the primary reading route.

## 13. Significance and venue assessment

Revision 102 contains potentially reusable ideas:

- a barycentric measure for the positive minimum of two boundary traces;
- a transverse comparison preserving relative endpoint position;
- a paired-measure Jacobian;
- multiplicity one after physical summation;
- a capped-clock essential-height estimate; and
- a residence-free relative endpoint certificate.

If independently verified and completed, these ideas could support a strong contribution to pointwise inversion and singular transport in dispersing billiards.

At the requested *Annals/Acta/Inventiones/JAMS* benchmark, however, the paper remains organized around the unrestricted exact-label pointwise raw local limit theorem. Its current endpoint is an exact equivalence with the unproved decay of the positive source \(\mathsf U_B\). No revision-103 author mathematics changes that endpoint.

The appropriate editorial assessment is therefore unchanged.

## 14. Final assessment

The visible revision-103 branch is not a new manuscript. It is an alias for the existing revision-102 review commit.

The latest actual mathematical source is revision 102. Its dedicated response and referee-copy workflows have now completed successfully, strengthening the provenance and build evidence. Its admitted transverse-clock estimate is a genuine advance, and I found no new decisive inconsistency in the focused chain.

The complete positive transverse-failure source remains uncontrolled. Therefore the upper pointwise theorem, the unrestricted exact-label raw local limit theorem and their unrestricted downstream consequences remain unproved.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A new substantive review should begin only after a genuine author SHA is landed and either the complete positive failure source is controlled or the governing theorem is replaced by a completed result of comparable independent significance.