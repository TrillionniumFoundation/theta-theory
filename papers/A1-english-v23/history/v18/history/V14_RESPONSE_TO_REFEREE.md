# Response to the referee of A1 v13

**Revised manuscript:** *Attainable information geometry across exponent collisions*  
**Controlling review:** `00b0844a7c2fb16b3231abf163d5004fd9e253cd`  
**Reviewed submission:** `fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6`  
**New directory:** `papers/A1-english-v14/`  
**New branch:** `revision/a1-english-v14-geometric-response-2026-09-06`

We thank the referee for distinguishing the mathematical findings from the
editorial judgment. The report identifies no new blocking mathematical or
implementation defect in the examined v13 chain. It closes P12.1--P12.3 and the
uniformity issue behind E12.2. We have not presented these closed items as new
objections, changed their scope, or substituted further implementation tests
for the outstanding mathematical and expository questions.

The revision has two connected purposes. First, the attainable collision
classification now governs the statement hierarchy and the principal proof.
Second, we distinguish the geometry of an acquired-history image from the
geometry of unresolved prior information. The latter is described through
all of its collision widths, rather than solely its largest uncertainty
floor. The common-name theorem and the complete numerical realization remain
intact, with all their hypotheses and proofs.

## E13.1: the isotropic uncertainty floor does not classify weak directions

We agree with the referee's account of the v13 proof. Its prior tilt uses a
uniformly visible direction. The reduction from separate memory and
uncertainty lower bounds and a stable upper construction to a sum law is not
an additional classification of vanishing collision directions. Section 7
retains that correct theorem; the introduction no longer uses its existence
as a substitute for explaining the central geometry.

**New result.** Section 6, `sections/directional_geometry.tex`, describes the
entire local prior ambiguity body at a fixed history. Write the raw future
moment vector as

\[
 X_a(\nu)=L_aD_a\nu\phi_a,\qquad D_a=\operatorname{diag}(d_1,\ldots,d_q),
\]

where the complete Newton functions retain their Hermite values at repeated
formal nodes. For the relative prior neighborhood

\[
 \mathcal B_\varepsilon(\mu)
 =\{(1+u)\mu:\mu u=0,\ \|u\|_\infty\le\varepsilon\},
\]

and one specified actual history h, Proposition 6.2 proves

\[
 c\varepsilon L_aD_a[-1,1]^q
 \subset \mathcal A_h(a,\varepsilon)
 \subset C\varepsilon L_aD_a[-1,1]^q.
\]

Consequently its k-th linear width is comparable to
\(\varepsilon d_{k+1}\), including zero widths at exact collisions. This is a
simultaneous body statement, not separate two-point witnesses whose constants
or feasible sets change with the direction. Its constants are uniform over
the compact calibration chamber, actual histories of the fixed horizon, all
node orders and their collision limits, for each fixed full-support prior or
for a fixed dominated family with a positive lower envelope.

**Proof mechanism.** Lemma 6.1 proves that the covariance of the complete
normalized test flag is uniformly invertible. Complete Hermite blocks plus
the constant are independent under a full-support probability; compactness
and a posterior lower domination give the uniform bound. For every cube
vector v, the bounded dual

\[
 f_v=v^{\mathsf T}\Gamma_{a,h}^{-1}(\phi_a-\nu_h\phi_a)
\]

has zero posterior mean and covariance v. It is important to pull this
posterior perturbation back to a normalized prior:

\[
 d\mu'=\frac{1+s f_v}{1+s\mu f_v}\,d\mu,
 \qquad s=\varepsilon/(4C_0).
\]

The denominator is not dispensable for nonconstant histories. This measure
has total mass one, stays in the declared relative envelope and has posterior
exactly \((1+s f_v)\nu_h\). Thus its complete normalized moment displacement
is exactly sv. This proves the inner body inclusion. Direct Bayesian
normalization proves the outer inclusion. The linear widths then follow from
the uniformly conditioned active block of L, with zero pivots never inverted.

**A sharp direction-specific decision statement.** Corollary 6.3 fixes the
first k distinct raw future moments in the Leja order. Exact triangular
back-substitution fixes precisely the first k normalized moments. The
remaining squared minimax query radius is

\[
 \mathfrak a_{h,k}(a,\varepsilon)\asymp
                 \varepsilon^2 d_{k+1}^2.
\]

At a constant-failure history this also gives an unconditional event-weighted
physical decision problem: the same event has probability \(2^{-n}\) under
every compatible prior; prior-moment advice is fixed before acquisition; all
trials and the event's probability remain charged. The payoff is explicitly
zero off that event. We do not infer the same formula for a different payoff
on all other report histories.

**Scope.** Section 6 assumes a known calibration and a local relative prior
neighborhood. Its prefix constraints are exact conditional moments at the
specified history, or exact prior moments for the constant-history experiment.
They are not the imperfect absolute-error pre-acquisition moment name in
Theorem 7.1. The result does not assert calibration-only uncertainty, stable
inversion of noisy small pivots, or the use of a different prior after each
observed history in a single statistical experiment. These distinctions are
printed in the manuscript immediately next to the definitions and conclusion.
The original joint prior-and-calibration common-name theorem is not weakened
or replaced by this local problem.

## E13.2: the attainable classification must carry the submission

The revised title, abstract and opening theorem center the distinction
between ambient test rank and actually attainable information. Section 1
states the exterior-volume profile and explains its three noninterchangeable
steps: positive-history flag attainment, a global bounded-format cover, and a
causal realization. The full proofs of these steps occupy Sections 3--5.

A spectral estimate by itself does not put an information cube into the
physical history image. The common interior binomial history has separated
past tangent exponents, while the complete future confluent flag survives
arbitrary additive collisions. Their pairing remains nondegenerate after
normalization removes exactly the evidence direction. Uniform local inversion
retains the kernel variables, and the lower all-failure likelihood gives an
unconditional subprobability minorization under one exploration law. This is
Lemma 5.2, not an assertion deduced solely from a Vandermonde determinant.

Nor does that local image imply the global cover. Theorem 5.3 uses the
coefficient-independent bounded-format estimate for the entire attainable
image in its anisotropic rectangle. Theorem 5.4 then respects causality by
updating attainable representatives and bounding the finite-horizon error
recurrence. The proof treats these as separate obligations rather than
compressing them into a general appeal to dimension.

Section 6 adds a distinction not recoverable by merely inverting the memory
profile. Acquired histories excite only its truncated prefix; admissible prior
perturbations can occupy all future directions. For example, with
\(A_\theta=\{0,1,2+\theta\}\), N=3, n=1 and m=2,

\[
 \Xi_3(M,A_\theta)\asymp M^{-1},\qquad
 \mathfrak a_{h,4}(A_\theta,\varepsilon)
                         \asymp\varepsilon^2\theta^2.
\]

There are four separated future groups and one merging pair. The fifth
Newton scale vanishes like |theta|, but neither memory checkpoint reaches that
fifth direction. The memory exponent therefore does not see this collision,
whereas residual prior uncertainty does. At the exact collision the latter
radius is zero. This is an example separating two geometries on the same
experiment, rather than another evaluation of a saturation threshold.

We continue to state the fixed sparse-monomial format and fixed-horizon
uniformity openly. We have not claimed an infinite-horizon theorem, a theorem
for every positive function algebra, or universal optimality of numerical
advice and program length. The present significance case rests on the proved
attainable classification and the newly separated full ambiguity geometry.
Its evaluation at a particular journal remains an editorial judgment; a
revision cannot certify that judgment by self-description or test counts.

## E13.3: one theorem hierarchy, with complete supporting appendices

The principal hierarchy is now explicit:

| Level | Revised location | Role |
|---|---|---|
| Geometric classification | Theorem 1.1; Lemma 5.2; Theorems 5.3--5.4 | Exact collision-uniform attainable memory profile and its physical/causal proof. |
| Direction-resolved prior geometry | Lemma 6.1, Proposition 6.2, Corollary 6.3 | All ambiguity widths and exact-prefix residual risk; distinguished from acquired-history truncation. |
| Common-name minimax consequence | Theorem 7.1 | Joint prior-and-calibration uncertainty with the original interior, domination and name-slack hypotheses. |
| Finite numerical realization | Theorem H.9; Appendices H--K | Full integer-table construction, numerical interfaces, sufficient precision and independently bound acceptance request. |

The three main levels requested by the referee are therefore the geometric
classification, the common-name consequence and the numerical implementation;
Section 6 is part of the first geometric level, not a new competing compiler
hierarchy. The exact-information statement remains in Section 2. Supporting
algebraic, confluent, sequential-value and common-risk results are fully
compiled in Appendices A--G. Detailed comparisons are in Appendix L.

Every complete v13 proof block and every complete v13 named mathematical
statement is preserved byte for byte in the expanded manuscript. Merely
moving a theorem label would not pass the new preservation check: it hashes
the whole statement as well as the whole proof. In particular the v13
uncertainty proof, its hypotheses, the construction bounds and the request
acceptance proof have not been shortened. The 74 original complete proofs
and 77 original complete statements are retained; the three new proved
results produce 77 complete proofs and 80 named results. Replaced introductory
prose and editorial records are preserved under `history/V13_*`.

The manuscript distinguishes persistent M-state labels, numerical advice and
read-only program length. The intrinsic lower bound concerns the first of
these; the other two retain sufficient constructive bounds without an
unstated universal coding converse. The source has been reorganized, not
weakened to avoid the referee's question.

## Evidence and remaining evaluation

The source artifact was anchored to the reviewed submission by the Git blob
of its manifest and all 62 source SHA-256 entries before revision. The four
unchanged author test suites have been rerun (7,904; 8,207; 26,158; 12,944
assertions). The new directional suite performs 7,400 exact-rational checks
of confluent identities, dual covariances, prior normalization and physical
moment/query shifts. These are author-side diagnostics, not 62,613 independent
proofs. Execution receipts and their exact scope are deposited separately.

The original v13 independent probe remains available against its own pinned
submission; the optional full-repository validation path reruns it separately
and never silently points its source-integrity checks at the altered v14 tree.
The standalone package supports all current author suites and the full build.

The local three-pass build produces 72 pages with no undefined-reference or
overfull warnings. All pages were surveyed in rendered contact sheets;
selected new-proof pages were inspected at readable scale. Neither source
preservation nor successful arithmetic diagnostics constitute formal proof
verification. The new arguments, their distinction between local and common
input, and the significance of the principal classification remain fully
exposed for the next referee's assessment.
