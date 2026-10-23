# External top-four referee report on A2-DYN revision 102

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v102-referee-response-2026-10-13`, `revision/a2-dyn-v102-referee-copy-2026-10-13`  
**Reviewed author commit:** `0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`  
**Reviewed repository tree:** `318f81a76c47dd69b7429bd205223ea5130bede9`  
**Active manuscript directory:** `papers/A2-DYN-v102-referee-response`  
**Active mathematical source:** 246 numbered core modules; revision 102 adds modules 244--246  
**Actual author baseline:** revision 100 uniform capacity, commit `7b2d9c999e987f61a38e9fcadd7fd7605192f35a`  
**Frozen baseline paper tree:** `7b8524304ab2eebc935e4c25f74b30d39f80c995`  
**Latest controlling report:** `reviews/a2-dyn-v101-submission-state-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `35f4a36f5b14d93a9716029ddc03226cf86a5834` / `d64268f21394e8edf9e5b9bd2408ed94360966b6`  
**Substantive mathematical report:** `reviews/a2-dyn-v100-uniform-capacity-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Substantive report commit / blob:** `61db130152c4f238f9bdd9f01c8d01bc049989fe` / `b44278830cf52568a010a659dc8e38d348b5d1a4`  
**Fresh qualification status at review freeze:** response run `38374168103` queued; referee-copy run `38374176852` queued  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimal-geometry, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 102 is an actual theorem-bearing author revision. It repairs the submission-state defect identified in the revision-101 report: both named author branches point to the same new author commit, the active manuscript directory exists, and the packet contains a new article, three new proof modules, a source manifest, an itemized response and a dedicated exact-SHA workflow.

The mathematical response is also genuine. Revision 100 had reduced the unresolved upper pointwise problem to the positive same-segment minimum of two physical endpoint traces. That quantity could remain large even when the outgoing-minus-incoming trace difference and the associated volume source were small. Revision 102 now acts on this **positive minimum itself**. It introduces the barycentric representation

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

It then uses the transverse field

\[
 V^\perp=(\partial_\theta\mathscr F)^{-1}\partial_\theta
\]

on regular pairing chambers, computes the paired-measure Jacobian, and proves a finite-count capped-clock comparison for the positive admitted source after physical sheets have been summed. Under the inherited schedule, the admitted source has normalized essential height

\[
 O(B^{-1/384}).
\]

This is substantive progress. It is not merely a renamed trace-difference estimate, a volume collar, a signed Jordan component or an averaged version of the target.

I audited the new modules

- `core/244_barycentric_positive_trace_coarea.tex`;
- `core/245_transverse_clock_and_pointwise_trace_height.tex`;
- `core/246_transverse_certificates_and_scalar_schedule.tex`;

and their dependence on the focused inputs, the revision-100 report, the response, the proof ledger, the source manifest and the principal pointwise target. Within the stated admitted scope, I found no decisive sign error, missing factor of the segment length, reversed transverse speed, exponent error, illegal collision-dependent cutoff, or hidden word-count factor.

The negative recommendation is nevertheless forced by the exact endpoint of the new argument. The scalar theorem is now

\[
 \mathcal E_M
 \le \mathcal H_M(\mathsf U_B)+C_MB^{-1/384},
\]

where \(\mathsf U_B\) is the complete positive paired source on which the transverse clock fails. The manuscript explicitly retains in \(\mathsf U_B\):

- zero transverse speed;
- insufficient one-sided transverse reach;
- actual loss of pairing regularity;
- nonregular pairing strata carrying positive paired mass;
- uncontrolled logarithmic variation of the residence, paired weight or speed;
- folds of the endpoint roof maps; and
- positive backward-critical traces which are not admitted near the critical corner.

No estimate proves

\[
 \mathcal H_M(\mathsf U_B)\longrightarrow0.
\]

Indeed the manuscript proves that, along the unchanged outer schedule, the original pointwise theorem is equivalent to this limit. Thus the unresolved failure source is not a secondary remainder after the principal theorem. It is exactly the remaining upper obstruction.

The conditional certificate in module 246 is useful, but it is not verified uniformly on the complete physical pairing family. It gives a sufficient local criterion, not a theorem that the complement of the criterion has small mass or small essential height. The failure source could still carry the entire upper spike allowed by the previous reduction.

Consequently revision 102 does not prove the upper pointwise half, the unrestricted exact-label raw local limit theorem, or the unrestricted point-conditioned consequences organized by that theorem. At the requested benchmark, replacing one explicit positive source by a smaller explicit positive source is valuable progress but not closure of the governing result.

## 2. Frozen source and chronology

The two author branches named above both resolve to

`0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`.

The repository tree is

`318f81a76c47dd69b7429bd205223ea5130bede9`.

The active article is

`papers/A2-DYN-v102-referee-response/main.tex`.

The complete inherited archive is compiled through

`papers/A2-DYN-v102-referee-response/supplement.tex`.

The immediate mathematical baseline is revision 100 uniform capacity at

`7b2d9c999e987f61a38e9fcadd7fd7605192f35a`.

Revision 101 was a submission-state alias for the existing revision-100 review commit. Revision 102 correctly treats that alias as historical review state rather than as an author manuscript. It starts from the latest review history, preserves the frozen revision-100 source and both controlling reports, and adds a new author directory.

The three new modules are

- `core/244_barycentric_positive_trace_coarea.tex`;
- `core/245_transverse_clock_and_pointwise_trace_height.tex`;
- `core/246_transverse_certificates_and_scalar_schedule.tex`.

The source manifest declares preservation of all 243 inherited cores, Python sources, appendices, bibliography files, provenance files, executable modes and revision-100 top-level snapshots. It also accurately leaves the following flags false:

- uniform admission of all physical pairing chambers;
- decay of the positive transverse-failure trace height;
- decay of the complete positive paired short-trace height;
- the full raw return LLT;
- closure of the primary referee request;
- independent human review; and
- formal proof certification.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v102-external-top4-review-2026-10-13/`.

No author source, author revision ref, workflow, historical report, preserved source variant or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v102-qualification.yml`.

At the review freeze the fresh runs at the final author SHA were:

- response branch run `38374168103`: `queued`, conclusion `null`;
- referee-copy branch run `38374176852`: `queued`, conclusion `null`.

I therefore do not describe the remote revision-102 qualification as completed at the freeze.

The author reports successful local validation of a nine-page focused article, an 852-page complete archive, all 246 recorder-visible core modules and 3,364 new finite fixtures, with ordinary and optimized Python outputs matched and native TeX warning/page gates passed. The validation contract is designed to pin the revision-100 tree, both reports, both revision-88 variants, inherited bytes and modes, top-level snapshots and complete recorder coverage.

These checks are meaningful source and build evidence. They do not certify:

1. the definable decomposition into regular physical pairing chambers;
2. one-sided endpoint-trace regularity at backward-critical directions;
3. the exact positive paired coarea identity as a continuum statement;
4. the transverse Jacobian orientation and disintegration convention;
5. multiplicity one after all physical sheets and compatible chart seams are summed;
6. the Borel stopped-flow construction on every relevant chamber;
7. the relative two-ended certificate on the actual Lorentz family;
8. uniform admission of the full physical paired source;
9. decay of the failure source; or
10. the inherited uniform-pressure, four-record spectral, coarea and trace chains.

A later completed workflow run would improve the source record but would not change the mathematical recommendation unless the remaining positive source were controlled.

## 4. Scope of this review

The substantive audit concentrates on:

1. the exact relation between the original paired trace and the barycentric measure;
2. the fixed-count regular pairing chambers;
3. the transverse coordinate and the sign of its Jacobian;
4. the disintegration on roof fibers;
5. the multiplicity-one physical summation;
6. the derivation of the averaged complete paired-source bound;
7. the capped-clock finite-count inequality;
8. the distinction between admitted and failed positive sources;
9. the relative two-ended certificate;
10. the outer schedule and exponent arithmetic;
11. the claimed scalar equivalence; and
12. the exact claims which remain unproved.

The 243 inherited modules are treated as the frozen source-pinned baseline of revision 100. This report does not independently re-prove that complete historical pipeline.

## 5. The inherited obstruction

Revision 100 had established, subject to its inherited inputs and its new geometric pressure theorem, a scalar reduction of the form

\[
 \mathcal E_M
 \le
 \mathcal H_M(T_{\mathsf S}^{\varepsilon(B)})
 +C_MB^{-1/192}
 +C(qr)^{257/256}
 +C(1+\varepsilon(B)^{-1})qr.
\]

Here \(T_{\mathsf S}^\varepsilon\) is the positive minimum of the two original weighted endpoint traces on each selected short physical segment. The previous report emphasized that this is not the positive part of a projected signed current. Both endpoint traces can be large and almost equal, so their difference can be small while their minimum has a pointwise spike.

The revision-100 report asked for a theorem controlling that positive minimum itself, after physical summation or with a proved bounded-overlap theorem, at a rate compatible with the outer schedule.

Revision 102 addresses this request directly on an admitted subfamily. This is the correct object and the correct direction of attack.

## 6. Regular pairing chambers

Module 244 fixes collision count, radius and exact label. It uses the finite physical graph, the exact section decisions and the retained endpoint-momentum injectivity to decompose the original paired measure into angular chambers on which the two roof endpoints

\[
 a(\theta),\qquad b(\theta)
\]

are \(C^2\), and the positive paired trace

\[
 c^\varepsilon(\theta)
\]

is locally Lipschitz.

At fixed collision count, definable cell decomposition can provide finitely many such intervals after further subdivision. The manuscript does not claim a collision-uniform bound on their number or derivatives. That restraint is appropriate: the subsequent positive coarea argument does not multiply by the number of chambers.

The treatment of chamber subdivision points is also structurally reasonable. They form a transverse-null set in \(\theta\), hence have zero mass for

\[
 c^\varepsilon(\theta)\ell(\theta)\,d\theta\,ds.
\]

Compatible Borel seams are assignments rather than new physical copies, and actual loss of regularity is put into the failure source rather than silently removed.

The most delicate part of this lemma is the asserted local Lipschitz regularity of the endpoint trace at a backward-critical entrance, where the trace need not vanish. The proof invokes the positive endpoint Hessian, a local inverse in the momentum variable, a lower tangential Hessian factor and the ordinary optical density. This is plausible in the declared physical coordinates, but it is compressed relative to its importance. A specialist should reconstruct this passage, including the precise source of the locally Lipschitz angular factor and the compatibility with the one-sided trace convention.

I do not identify a counterexample from the written argument. I do regard this as a load-bearing continuum point which finite definability checks cannot certify.

## 7. Exact barycentric representation

On one regular chamber set

\[
 \ell=b-a,
 \qquad
 \mathscr F(\theta,s)=a(\theta)+s\ell(\theta),
 \qquad 0<s<1.
\]

The measure

\[
 d\pi^\varepsilon
 =c^\varepsilon(\theta)\ell(\theta)\,d\theta\,ds
\]

is exactly the paired source. Indeed the substitution

\[
 u=a+s\ell,
 \qquad du=\ell\,ds
\]

gives

\[
 c^\varepsilon\ell\,ds\,d\theta
 =c^\varepsilon\,du\,d\theta.
\]

Therefore the roof pushforward with the original Borel selector is the original trace density \(T_H^\varepsilon\). The segment length is not lost, and the minimum is taken before physical projection and before any norm.

This is the right positive representation. It does not replace the original collision probability or alter the guard, section, labels or target selector.

## 8. The transverse Jacobian

Put

\[
 v(\theta,s)=\partial_\theta\mathscr F
 =(1-s)a'(\theta)+s b'(\theta).
\]

On \(v\ne0\), the field

\[
 V^\perp=v^{-1}\partial_\theta
\]

satisfies

\[
 \frac{d}{dh}\mathscr F(\Theta_h^\perp y)=1
\]

and preserves \(s\). In the coordinates

\[
 (t,s)=(\mathscr F,s)
\]

the paired measure is

\[
 d\pi^\varepsilon
 =\varrho^\varepsilon(t,s)\,dt\,ds,
 \qquad
 \varrho^\varepsilon=\frac{c^\varepsilon\ell}{|v|}.
\]

The displayed ratio

\[
 J_h^\perp(y)
 =\frac{\varrho^\varepsilon(\Theta_h^\perp y)}
        {\varrho^\varepsilon(y)}
\]

is consistent with the **pullback** Jacobian convention used in module 245:

\[
 J_h^\perp(y)\,d\pi^arepsilon(y)
\]

transforms to the paired measure at the translated roof. Under this convention the direction of the ratio is correct. The absolute value in \(|v|\) is essential and is correctly retained.

The manuscript should state explicitly that this is the pullback Jacobian, or write the precise integral covariance immediately beside its definition. Without that convention, readers often use the reciprocal Radon--Nikodym convention for a pushforward Jacobian. The subsequent proof makes the intended convention recoverable, but this should not remain implicit in a load-bearing theorem.

The transverse flow is a comparison between actual trajectories inside the same exact-event chamber. It is not the physical roof flow. This distinction is stated correctly.

## 9. Multiplicity and physical summation

The new estimate must work after physical summation; a sheetwise modulus followed by an uncontrolled sum would not answer the previous report.

The manuscript relies on the inherited Borel bijection of actual maximal segments. Chamber interiors are counted once, compatible coordinate seams are continued, and the stopped flow is one-to-one on its graph. Since the positive covariance is applied before the uniform norm, the proof does not introduce the number of symbolic words, the number of chambers or a transverse-overlap factor.

This is the correct architecture. The principal specialist question is whether the one-to-one statement remains valid across every compatible continuation and whether every genuine loss of uniqueness or chamber regularity is indeed sent to the failure source. The proof says so and does not discard that failure source. I found no explicit double count in the formulas.

## 10. The averaged complete paired source

Let \(\mathsf T_\Delta^\varepsilon\) be the complete paired source on

\[
 0<\ell<\Delta
\]

inside the original exact event, with no additional target selection.

The inherited trace comparison gives, schematically,

\[
 \mathsf T_\Delta^\varepsilon
 \le b^\varepsilon
 +C(1+\varepsilon^{-1})
       \mathbf 1_{[-\Delta,\Delta]}*v^0.
\]

Applying the fixed-width averaging operator

\[
 A_rh(t)=\frac1{2r}\int_{t-r}^{t+r}h(u)\,du
\]

and using translation invariance yields

\[
 \|A_r(\mathbf1_{[-\Delta,\Delta]}*v^0)\|_\infty
 \le 2\Delta\|A_rv^0\|_\infty.
\]

Together with the inherited bounds for \(A_rb^\varepsilon\) and \(A_rv^0\), this gives

\[
 \limsup_m\sup_{R,n,k}m^2
 \|A_r\mathsf T_\Delta^\varepsilon\|_\infty
 \le C\{\varepsilon^{1/16}+(1+\varepsilon^{-1})\Delta\}.
\]

This derivation does not require a pointwise bound for \(v^0\). The factor \(2\Delta\) is harmless and can be absorbed in the universal constant. The constants are asserted independent of the previously fixed widths, exactly as required by the later schedule.

## 11. The capped transverse clock

The clock is

\[
 k_{r,\Delta}^\perp(y)
 =\frac1r\int_{-r}^{r}
   \mathbf1_{\{\Theta_h^\perp y\text{ exists}\}}
   \min\{1,J_h^\perp(y)\}\,dh.
\]

Its range is \([0,2]\), because the normalization is \(1/r\), not \(1/(2r)\). The admission threshold is chosen in \((0,1]\).

For an admitted starting point,

\[
 q_\perp\le k_{r,\Delta}^\perp.
\]

Multiplication by the target-fiber paired kernel and integration in \(h\) gives

\[
 q_\perp T_{H,\mathrm{adm}}^arepsilon(t)
 \le \frac1r\int_{-r}^{r}
 \mathsf T_\Delta^arepsilon(t+h)\,dh.
\]

Equivalently,

\[
 T_{H,\mathrm{adm}}^arepsilon(t)
 \le \frac1{q_\perp r}
 \int_{t-r}^{t+r}\mathsf T_\Delta^arepsilon(u)\,du.
\]

The proof uses

\[
 \min\{1,J_h^\perp\}\le J_h^\perp
\]

and the target-direction covariance on the one-to-one survivor graph. The starting selector is held at the original roof. After transport, the selector is dropped only for a positive upper bound by the complete short paired source; the exact displacement, occupation, collision count and section event are not enlarged.

The factor relating the right-hand side to \(A_r\mathsf T_\Delta^arepsilon\) is \(2/q_\perp\). It is correctly absorbed into the constant in the stated height theorem.

Thus, at its stated scope, module 245 genuinely estimates the positive common trace itself on the admitted set.

## 12. The relative two-ended certificate

The certificate assumes on one angular side, at fixed relative position \(s\), that

\[
 |v|\ge\nu>0,
\]

and that

\[
 |\partial_	heta\log\ell|,
 \quad |\partial_	heta\log c^arepsilon|,
 \quad |\partial_	heta\log|v||
 \le A.
\]

If

\[
 r\le \nu\min\{L_	heta,\log2/(3A)\},
\]

then the required roof displacement is reached before leaving the angular interval, and

\[
 \ell(\theta)\le 2^{1/3}\delta<2\delta,
 \qquad
 \frac{\varrho^arepsilon(\theta,s)}
      {\varrho^arepsilon(\theta_0,s)}
 \ge\frac12.
\]

One full one-sided interval of roof length \(r\) therefore contributes at least

\[
 \frac1r\cdot r\cdot\frac12=\frac12
\]

to the clock.

The calculation is correct and explains why a lower bound on the original residence \(\ell(\theta_0)\) is not intrinsically necessary. Parallel moving endpoint roofs provide a useful model of that cancellation.

The limitation is decisive. The certificate requires a positive transverse speed, sufficient one-sided angular reach and relative logarithmic control of three quantities. None of those conditions is proved uniformly on the full physical pairing family. In particular, when a backward-critical entrance has \(a'=0\), one has

\[
 v=s b'.
\]

The certificate may work for interior \(s\), but degenerates as \(s\downarrow0\). The potentially positive critical trace at that corner remains in the failure source.

A conditional certificate is not a deconcentration theorem for its complement.

## 13. Schedule and exponent audit

The inherited outer schedule is

\[
 \varepsilon(B)=A_0B^{-1/12},
 \qquad q_0^*=1/8,
 \qquad r_0=c\varepsilon^4,
 \qquad \delta=6q_0^*r_0.
\]

The new choices are

\[
 \Delta=2\delta,
 \qquad r_\perp=\delta,
 \qquad q_\perp=\varepsilon^{1/32}.
\]

Substitution into the admitted-height estimate gives

\[
 q_\perp^{-1}\varepsilon^{1/16}
 =\varepsilon^{1/32}
\]

and

\[
 q_\perp^{-1}(1+\varepsilon^{-1})\Delta
 =O(\varepsilon^{95/32}).
\]

Since \(\varepsilon=B^{-1/12}\), the first term is

\[
 B^{-1/384}.
\]

The retained terms

\[
 B^{-1/192},
 \qquad \varepsilon^{257/64},
 \qquad \varepsilon^3
\]

all decay faster. I found no exponent error in the displayed schedule.

Every new threshold is fixed as a function of the outer reconstruction parameter before the collision limit. No new cutoff depends on the collision count.

## 14. The remaining failure source

Define

\[
 \mathsf U_B
 =T_{\mathsf S,\mathrm{fail}}^{\varepsilon(B)}.
\]

The exact positive split is

\[
 T_{\mathsf S}^{\varepsilon(B)}
 =T_{\mathsf S,\mathrm{adm}}^{\varepsilon(B)}+\mathsf U_B.
\]

The new theorem proves

\[
 \mathcal H_M(T_{\mathsf S,\mathrm{adm}}^{\varepsilon(B)})
 \le C\bigl(\varepsilon^{1/32}+arepsilon^{95/32}\bigr)
\]

and hence

\[
 \mathcal E_M
 \le \mathcal H_M(\mathsf U_B)+C_MB^{-1/384}.
\]

No bound is proved for \(\mathsf U_B\). It is not shown to have small total mass, small weak type, bounded overlap, a vanishing residence factor, or any positive power compatible with the outer schedule. Even a small mass estimate would not by itself imply the required essential-height decay.

The failure source can include the most singular configurations: stationary endpoint roofs, folds, short comparison lifetimes, critical corners and rapidly varying positive trace weights. These are precisely the configurations capable of producing a pointwise upper spike.

The theorem that the original pointwise assertion is equivalent to

\[
 \mathcal H_M(\mathsf U_B)\to0
\]

is useful and internally consistent with the inherited positive scalar decomposition. It also confirms that the principal theorem remains open.

## 15. What revision 102 establishes

Subject to the inherited revision-100 inputs and to the continuum points identified above, revision 102 establishes:

- a fixed-count definable decomposition into regular pairing chambers;
- an exact barycentric representation of the original positive same-segment trace minimum;
- a transverse coordinate preserving relative endpoint position;
- the correct paired-measure density \(c^\varepsilon\ell/|v|\) in roof coordinates;
- a multiplicity-one target-direction comparison after physical summation;
- a capped-clock finite-count inequality at the original target roof;
- an essential-height bound for the complete admitted positive trace;
- a relative two-ended sufficient admission criterion with no lower residence cutoff;
- a legal schedule giving admitted height \(O(B^{-1/384})\); and
- an exact scalar reduction to the positive transverse-failure source.

These are real advances over revision 100.

## 16. What revision 102 does not establish

Revision 102 does not establish:

- uniform admission of all nongrazing physical paired segments;
- small essential height of the nonadmitted paired source;
- a quantitative bound on zero-speed or fold strata;
- control of backward-critical corner mass;
- a collision-uniform relative derivative certificate;
- decay of the complete positive paired short trace;
- vanishing of the complete residual upper source;
- unconditional upper-spike persistence;
- the upper pointwise half of the exact-label theorem;
- the unrestricted exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- unrestricted total-variation or entropy consequences;
- independent human specialist approval; or
- formal proof certification.

These boundaries are represented accurately in the source manifest and publication-status file.

## 17. Required changes before another top-four review

### 17.1. Control the entire failure source

The next revision must prove

\[
 \mathcal H_M(\mathsf U_B)\longrightarrow0
\]

under a legal outer schedule, or replace this quantity by a strictly smaller remainder whose decay is proved. Renaming or repartitioning the positive failure source is not enough.

### 17.2. Prove uniform admission or quantitative failure decay

A successful theorem could take either of two forms:

1. prove that the relative two-ended certificate holds, with quantitative constants, on all physical pairs selected by the original source except a part already known to have vanishing ordered height; or
2. prove directly that failure of the certificate forces a geometric degeneracy whose physically summed positive trace has a vanishing essential-height bound.

The proof must address zero speed, short angular reach, folds and rapid relative variation rather than assigning them to an uncontrolled remainder.

### 17.3. Treat backward-critical corners explicitly

At a critical entrance the positive trace is retained, and \(v=s b'\) may vanish as \(s\downarrow0\). The next argument should either:

- establish a separate two-parameter coarea gain near that corner;
- prove an integrable or maximal estimate strong enough for ordered height;
- find a second transverse direction;
- derive a quantitative critical stratification with a schedule-compatible power; or
- show by a physical identity that the corresponding positive source is already paid elsewhere.

It may not set the backward-critical trace to zero.

### 17.4. Remain after physical summation

Any sheetwise estimate must either be formulated directly for the physically summed paired measure or be accompanied by a collision-uniform bounded-overlap/capacity theorem. No unweighted word count or uncontrolled chamber count should enter.

### 17.5. Retain a pointwise norm and explicit rate

A finite-mass, weak-convergence, fixed finite-\(p\), or averaged-roof estimate does not close the theorem. The result must imply essential-height decay with an explicit exponent compatible with

\[
 \varepsilon(B)\asymp B^{-1/12},
 \qquad \delta\asymp\varepsilon^4.
\]

### 17.6. Clarify the Jacobian convention

State explicitly that \(J_h^\perp\) is the pullback Jacobian used in

\[
 J_h^\perp(y)d\pi^arepsilon(y)
 \mapsto d\pi^arepsilon(\Theta_h^\perp y),
\]

or print the exact covariance formula in the theorem statement. This will remove an otherwise unnecessary reciprocal-convention ambiguity.

### 17.7. Complete exact-SHA qualification

Both author refs should complete the dedicated workflow successfully at the final author SHA before the packet is described as remotely qualified. The resulting receipts should identify the same source tree, article, archive and PDF hashes.

### 17.8. Obtain independent specialist verification

Independent specialists should reconstruct at least:

- the fixed-count physical chamber decomposition;
- critical one-sided trace regularity;
- the positive barycentric coarea identity;
- the transverse Jacobian and stopped-flow orientation;
- multiplicity one across physical summation and compatible seams;
- the capped-clock disintegration;
- the two-ended logarithmic certificate;
- the inherited uniform-pressure and uncut-gradient theorems; and
- the final theorem controlling \(\mathsf U_B\).

### 17.9. Consolidate after scalar closure

The focused nine-page article is much clearer than the complete archive. If the failure source is closed, the final submission should present a compact proof dependency graph for the current theorem, with the historical 852-page pipeline retained as a technical supplement rather than as the primary reading route.

## 18. Exposition

The revision is candid about its scope, which is welcome. The following distinctions should remain prominent:

1. admitted positive trace is not the full positive trace;
2. the transverse clock is not the physical roof flow;
3. the Jacobian is for the paired measure, not the original volume source;
4. the certificate is sufficient, not necessary;
5. lack of a lower residence cutoff does not imply uniform admission;
6. the failure source is positive and may carry the whole upper obstruction;
7. a backward-critical trace may be nonzero;
8. the new rate applies only to the admitted part;
9. exact-SHA build qualification is not proof certification; and
10. unrestricted downstream claims remain subordinate to scalar closure.

The title “Complete transverse-clock trace estimate” should be read as completeness of the finite-count inequality on the admitted part, not as completeness of the original paired-source theorem. A more explicit title such as “Transverse-clock estimate for the admitted paired source” would avoid possible confusion.

## 19. Significance and venue assessment

Revision 102 contributes several potentially reusable ideas:

- a barycentric measure for the positive minimum of two boundary traces;
- a transverse comparison preserving relative endpoint position;
- a paired-measure Jacobian rather than a volume Jacobian;
- multiplicity-one comparison after physical summation;
- a capped-clock pointwise inequality for an admitted positive trace; and
- a residence-free relative endpoint certificate.

If independently verified, these results could form a strong specialized contribution to singular transport, coarea methods and pointwise inversion in dispersing billiards. The focused presentation is also a substantial editorial improvement over asking the reader to locate the active chain among hundreds of historical modules.

At the requested *Annals/Acta/Inventiones/JAMS* benchmark, however, the manuscript continues to be organized around the unrestricted exact-label pointwise raw local limit theorem. The current endpoint is an exact equivalence with the unproved decay of \(\mathsf U_B\). That positive source is capable of carrying the complete remaining upper obstruction.

Even if the new coarea construction is correct, the governing theorem is therefore incomplete. The unresolved scalar endpoint alone is decisive for the present recommendation.

## 20. Final assessment

Revision 102 responds positively and mathematically to the revision-100 report. It no longer estimates only a trace difference. It represents the original positive paired minimum exactly, constructs a transverse paired measure, proves a physically summed capped-clock inequality, supplies an explicit local admission certificate and obtains a legal \(B^{-1/384}\) rate for the admitted source.

I found no decisive internal error in modules 244--246 at their stated scope. The new Jacobian and exponent bookkeeping are coherent, subject to the specialist checks listed above.

Nevertheless, the manuscript retains the complete nonadmitted positive source and proves no decay for it. The original pointwise theorem is explicitly equivalent to the vanishing of that source. The principal referee request, upper pointwise theorem, full exact-label raw local limit theorem and unrestricted downstream consequences therefore remain open.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
