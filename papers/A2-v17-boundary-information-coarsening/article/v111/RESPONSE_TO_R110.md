# Response to the independent v110 referee report

Manuscript: **Recovery of information metrics: contact multiplication and global degeneracy**.
Controlling report: `reviews/a2-v110-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md`, at `043495e949f535554c5540c24b679b4aafa6a31d`.
Revision: v111, on the separate branch `revision/a2-v111-global-degeneracy-boundary-experiment-2026-09-21`.

We thank the referee for distinguishing the now-sharp native threshold from the further depth needed in its geometry and statistical interpretation. This revision keeps that threshold and the earlier conclusions, but changes the principal mathematical contribution. It supplies a global degeneracy theorem, an exact fixed-space realization criterion, and a direct raw-count experiment comparison. It is not a revision consisting only of new finite witnesses or renamed plug-in estimators. The mathematical article is written independently of the revision history; this response contains the process record.

## 1. Global failure geometry and multiple contacts — report Sections 7, 19, 21.1–21.2

**Theorem 1.1 (proved in Section 4)** determines the codimension of the entire reduced failure set on `Gr(c,V_n)^L`, for `k=n+1`, `4 <= c < k`, and `L*q >= p`, where `q=c(c+1)/2`, `p=2k-1`:

`codim Delta^(L) = min{L*q - p + 1, L*c - 3}`.

This is not an expected-codimension assertion. The proof treats every rank of the annihilating Hankel form. Lemma 4.2 counts all isotropic Grassmannian strata, including their radical intersections, and gives `D_(r,s)=(c-s)(r-s)+s(s+1)/2`. Lemma 4.3 proves the required optimization over every feasible `(r,s)`, including the small exceptional arithmetic cases. Proposition 4.4 constructs the common-secant family and proves that its projection is generically one-to-one, rather than merely counting an incidence before projection. Classical Hankel rank-stratum dimensions and the classical maximal-minor height bound supply the explicitly identified external inputs.

The common-secant family has codimension `L*c-3`. When this is the smaller bound, it is a maximal-dimensional irreducible component. Corollary 4.5 proves that the old base-point family is properly contained in this larger irreducible set and is not itself a component. This answers one of the concrete global questions left open in v110, not just its tangent-space formulation.

The same argument proves the sharp generic number of independently designed contacts, `ceil((2*k-1)/q)`. There are no cross-contact products. The subspaces share a single annihilating Hankel functional in the incidence; the multi-space theorem is not an assumption that separately generic images have independent sums. Corollary 5.3 transfers the assertion to independently chosen native loadings with common `J`. It does not claim that several points of one fixed loading can be selected independently.

The saturated generic-rank assertion, and hence the retained sharp single-contact threshold, now follow from this global proof without invoking rational-curve maximal rank as a black box. The classical general single-space theorem, including its injective range, remains explicitly attributed and proved by a precise reduction in Proposition A.1.

We do not claim a classification of every irreducible component, reducedness of the determinantal scheme, or a random condition-number tail. The report requested at least one substantial global result; this revision takes the exact-dominant-codimension and explicit-component route. The complex codimension statement is separated from the real native realizability result.

## 2. Positive realization at a fixed space — report Sections 4–5 and 22

**Theorem 5.1** strengthens the earlier submersion result. For a prescribed normal-polynomial space `U`, put `T=J U^perp`. Local positive realization is equivalent to `T` containing a strictly positive vector. Positive realization with the exact global fibre `{e1,-e1}` is equivalent to that condition together with `D_s T != T` for every nonconstant coordinate-sign matrix.

The additional obstruction is exactly a decomposition of `T` over a nontrivial coordinate partition. The proof constructs the loading from a positive `t` outside a finite union of proper sign-incidence subspaces. Thus the distinction between local realizability and global separation is now classified at the fixed space, rather than only preserved as a caveat about intersecting generic open sets.

Lemma 5.2 identifies the ambient irreducible affine loading space and the removed open conditions. It uses evenness to identify the germs at the two preimages, and records that the projection tube depends on the fixed loading and compact positive metric family. No uniform tube over all generic loadings is asserted.

## 3. A direct statistical contact reduction — report Sections 10–12 and 21.3

The referee is correct that the old `raw sample -> theta-hat -> computed contact -> reconstruction` pipeline is deterministic re-encoding. We retain its mathematical bound in **Theorem C.1**, name it accordingly, and do not use it as evidence for a distinct contact observation model.

**Section 9 is a different construction.** In the explicitly observed Poisson-exposure protocol with known mark laws, fix the calibration centre before observing data. The least-favourable local target submodel has all `p` moment directions and information `Sigma^-1`. Formula (9.2) forms a normal-compression score statistic by fixed linear weights directly on the observed counts, followed by a specified vanishing jitter. It never first constructs an estimator of the complete moment parameter.

**Lemma 9.1** proves uniform total-variation comparison by jittered Poisson local approximation and explicit Markov kernels. **Theorem 9.2** gives the limiting contact experiment and its exact information:

`I_contact = L^T (L Sigma L^T)^dagger L`

`= Sigma^(-1/2) P_range(Sigma^(1/2) L^T) Sigma^(-1/2)`.

Its kernel is exactly `ker L`. The reduction is locally asymptotically equivalent to the raw target experiment if and only if the within-contact products span the moment space. The deficient case is proved by a two-parameter experiment-comparison obstruction, not just by counting a limiting covariance rank.

The jitter is substantive. An infinite-precision real encoding of integer counts can remain injective even when its linear map has deficient real rank. A central limit theorem alone would therefore not establish information loss. The protocol retains only the jittered compressed statistic, not the auxiliary randomization values, and the proof uses total variation rather than weak convergence alone.

The theorem is explicitly local, with a fixed centre, known marks and a stated full-dimensional target subexperiment. It does not assert global equivalence for jointly unknown marks and exposures, nor pretend that these score statistics are independently measured distance values. Those qualifications identify the experiment actually proved; they are not supplied after the theorem. The optional shrinking-singular-value/high-contact-order minimax problem is not represented as solved by a regular plug-in risk bound.

## 4. The physical coalescence boundary — report Sections 13–14 and 21.4

**Theorem 8.1** specifies the physical alternatives `v=h/sqrt(N)`, `h>=0`, and unrestricted local nuisance directions. The smooth two-sided positive likelihood extension is used only to calculate derivatives. The actual efficient quotient is `Y ~ N(h,R)` with the parameter restricted to the physical cone. Its constrained estimator is a metric projection and need not be normal.

For the synchronized image `h=q_A(zeta)`, profiling produces exactly the Gaussian distance value `C_R(Y)`, after nuisance removal and an explicit compact-localization argument. Physical root displacement has scale `N^-1/4`. **Corollary 8.2** proves matching upper and two-point lower squared-risk bounds of order `N^-1/2` on a labelled nonnegative amplitude ray. This does not assert recovery of an unidentifiable sign.

This section reconnects the earlier repository derivation in `article/v104/parts/05-experiment.tex` to the native information model; the older cone-LAN argument and scaling are not claimed as new general asymptotic principles. The native specialization, synchronized profile and stated risk result are now in the principal mathematical narrative, where the interpretation issue arose.

Target-design weights, actual sample proportions and unknown observed exposures are separated in Section 3 and at the beginning of Appendix B. Constants are for fixed separated compact designs, not uniform collision limits.

## 5. Structured families, attribution and architecture — report Sections 9, 16, 20, 21.5

The uncomputed arbitrary-family statement is now **Proposition 7.1, Generic transfer**. **Theorem 7.2** computes `rho` for block-spectral families with arbitrary eigenspace multiplicities, giving the real symmetric circulant family as a non-diagonal example. Column-orthonormalization is explicitly a simultaneous invertible congruence. The diagonal example and its sharp threshold remain intact. This section is not advertised as a solution for every Toeplitz or graph-sparse family.

The introduction distinguishes Hankel duality, Gram product spaces, rational maximal rank, quadratic sensing, complete-conormal duality, boundary asymptotics and the new experiment comparison. Proposition A.1 identifies Larson's Theorem 1.2 and checks genus, degree, ambient projective dimension, Brill–Noether number and the restriction-of-quadrics map. Section 4 identifies the precise Hankel and determinantal inputs it actually uses. The principal novelty paragraph is mathematical rather than a claim about a target venue.

The article uses a conventional theorem–proof structure, with no commit hashes, CI receipts, revision numbers or preservation promises in the abstract or mathematical exposition. All old files remain unchanged, and retained technical results appear in Appendices A–D with the historical full proof closure separately available. The broader title reflects the new global and multi-contact theorem while keeping the subject information-metric recovery, not an unqualified tomography claim.

## 6. Detailed response to the 35 proof and presentation comments

| Comment | Revision location and action |
|---|---|
| 1 | Proposition A.1: exact Larson Theorem 1.2 and all specialization hypotheses. Section 4 uses separately identified classical Hankel and height inputs. |
| 2 | Introduction's method paragraph and proof of Theorem 1.2 separate obstruction, internal global incidence theorem, and native realization. |
| 3 | Abstract states the proved codimension and realization results; no claim to invent classical rational maximal rank. |
| 4 | Theorem 5.1 and threshold proof give the real-chart nonvanishing argument. |
| 5 | Theorem 5.1 strengthens the local/global distinction to an exact fixed-space criterion. |
| 6 | Lemma 5.2 specifies the irreducible affine space R^(kd), rank and first-coordinate open conditions. |
| 7 | Lemma 5.2 explicitly uses evenness to identify the two image germs. |
| 8 | Lemma 5.2 gives dependence on fixed A, its germ and a compact positive metric set. |
| 9 | Proposition A.1 consistently distinguishes vector dimension c from projective dimension c-1. |
| 10 | Appendix A retains the strict monomial gap and economical construction without adding a witness catalogue to the article. |
| 11 | Section 6 states rank exactly r before the kernel-to-cokernel differential. |
| 12 | Corollary 4.5 proves that the base-point family lies properly in the common-secant family and is not a component. |
| 13 | Coefficient, tensor, Frobenius and Grassmannian norm conventions precede Theorem 6.2; lower constants are local. |
| 14 | The paragraph after Theorem 6.2 identifies compactness away from failure as continuity, not a quantitative tail bound. |
| 15 | Arbitrary-family transfer is Proposition 7.1; Theorem 7.2 supplies explicit block-spectral and circulant ranks. |
| 16 | Theorem 7.2 explicitly proves preservation under column-orthonormalization by simultaneous congruence. |
| 17 | Appendix B distinguishes prespecified target weights and realized allocations before Theorem B.1. |
| 18 | Appendix B states that constants need not remain bounded near root/clock/probability collisions. |
| 19 | Theorem B.2 is titled an additional observed-exposure protocol. |
| 20 | Sections 9 and Appendix B explicitly restrict efficient covariance claims to known marks. |
| 21 | Theorem C.1 is titled Computed finite-offset encoding and inversion. |
| 22 | Appendix C identifies the inherited K/N term and denies a new minimax interpretation of that re-encoding. |
| 23 | Appendix C separates deterministic offset bias from the independent Gaussian experiment's h^(-4) variance. |
| 24 | Section 8 derives the physical cone likelihood and synchronized profile. |
| 25 | Independent Gaussian contact noise remains a separate experiment in Appendix C. |
| 26 | Commit and workflow details appear only in repository documents and execution receipts. |
| 27 | Abstract contains no historical-preservation language. |
| 28 | Title is broadened only to the proved global and multi-contact degeneracy theory. |
| 29 | The paragraph after Theorem 1.2 specifies comparison across calibrated families as k varies. |
| 30 | The same paragraph distinguishes native sharpness from universal information-model thresholds. |
| 31 | Abstract's geometry claim is now the exact global codimension theorem, not merely local tangent information. |
| 32 | Finite diagnostics and source receipts remain outside the mathematical correctness proof. |
| 33 | No enlarged finite witness table is used to prove the universal theorem; Section 4 contains the all-rank proof. |
| 34 | Introduction starts from the inverse problem and literature, without presupposing earlier reviews. |
| 35 | Introduction's method paragraph isolates the global incidence optimization and fixed-space realization from all classical inputs. |

## 7. Verification and next review

The principal source has been locally compiled to 20 pages with no undefined references/citations, multiply-defined references or overfull boxes. Local exact diagnostics passed for 9,920 dimension triples and 2,106,240 feasible rank strata, together with ten product witnesses, three native loading witnesses, an exact corank-one secant example and rational statistical/normalization identities. These are reproducible checks, not a substitute for reading the proofs.

The branch-only workflow performs a separate exact-source four-volume build, preservation check and receipt publication. Execution status must be read from its actual receipt and run, not inferred from this response. All historical proofs and the controlling report remain in place for comparison. We request independent re-review of the new global theorem and the explicitly specified statistical reduction; neither build success nor this response predetermines the referee's assessment of correctness, originality or journal significance.
