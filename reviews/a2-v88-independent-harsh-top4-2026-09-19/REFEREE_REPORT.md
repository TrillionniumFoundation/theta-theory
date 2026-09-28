# Independent harsh referee report on A2 revision 88

**Review date:** 19 September 2026  
**Reviewed branch:** `revision/a2-v88-projective-polynomial-rigidity-2026-09-19`  
**Reviewed source commit:** `777a9c951d5ca94a5261a6585ab6548d267e21e4`  
**Review branch:** `review/a2-v88-independent-harsh-top4-2026-09-19`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/article/v88/paper.tex`  
**Principal source blob SHA:** `0118f5944d48d8d58d3140d5d6ebc690caa3afb6`  
**Response reviewed:** `reviews/a2-v88-response-to-v87-2026-09-19/RESPONSE_TO_REFEREE.md`  
**Literature audit reviewed:** `reviews/a2-v88-response-to-v87-2026-09-19/LITERATURE_AUDIT.md`  
**Controlling previous report:** `reviews/a2-v87-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`

## Editorial recommendation

**Reject in the present form at the standard of Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica.**

Revision 88 is a serious mathematical improvement over revision 87. It answers the most important structural request in the previous report rather than adding another unrelated regime. In particular, the new paper now contains:

1. a degree-(d) projective polynomial experiment;
2. an exact gcd/nullity description of the normalization defect;
3. positive local exact fibres associated with normalization nonuniqueness;
4. a sharp worst-case (2d+1) clock count inside the stated model;
5. an additive one-sided spectral modulus in which normalization and channel losses are not multiplied;
6. an observable affine residue quantity (eta) with a proved zero set and semicontinuity;
7. a direct least-squares/SVD/matrix-polynomial estimator;
8. honest confidence sets and adaptive-design minimax lower bounds on observable affine signal classes.

I carefully checked the main proof route in Lemmas 2.1, 2.2 and 2.4, Proposition 2.3, Theorems 1.1, 3.2, 4.1, 5.2 and 5.4, together with the two least-favourable families. I did **not** find a short fatal counterexample or an obvious algebraic contradiction in those arguments.

The reason for rejection is therefore not that revision 88 has failed to produce real mathematics. It has. The issue is the level and unity of the contribution relative to the four leading general mathematics journals.

The paper now has two strong but only partially connected stories:

- a general degree-(d) normalization/rational-interpolation theorem whose condition is (	au(P)) together with latent channel conditioning (kappa); and
- a substantially more intrinsic affine ((d=1)) theory in which the latent fibre optimization is replaced by the observable residue quantity (eta(P)), followed by sharp inference.

The top-four-level structural problem is that the second story has **not** been lifted to the first. The genuinely observable singular invariant, direct sharp inverse, and minimax theory remain essentially affine. The degree-(d) theorem is elegant, but still reads as a highly structured matrix-valued rational interpolation / matrix-polynomial perturbation result for one simultaneously diagonalizable stochastic model.

My assessment is therefore: **strong specialist-level progress, but not yet a four-leading-general-journal theorem.**

---

## 1. What revision 88 genuinely fixes

Revision 87 was criticized for remaining tied to the one-pole affine curve
[
P(T)=A+rac{B}{T-h}.
]
Revision 88 does make a substantive conceptual move beyond that setting.

Theorem 1.1 replaces the affine numerator by
[
K(z)=Uoperatorname{diag}(alpha_b f_b(z))V^{mathsf T},
qquad
P(T)=K(T)/q(T),
qquad
q=sum_balpha_b f_b,
]
with monic degree-(d) component polynomials (f_b). The observable normalization operator (mathcal N_P) is defined directly from the sampled matrices, and Lemma 2.1 identifies
[
ker mathcal N_P
=
{(q/g)s:deg s<deg g},
qquad
g=gcd(f_1,ldots,f_k),
]
once (2d+1) clocks are present.

This is a meaningful structural statement. It explains the defect algebraically and connects exact normalization ambiguity with common-factor cancellation.

The proof also contains a genuinely useful cancellation in the perturbation step. After recovering the denominator coefficients, the normalization error remains diagonal in the true channel coordinates. Hence the coefficient perturbation is
[
O!left(delta(kappa^{-1}+	au^{-1})ight),
]
not (O(delta/(kappa	au))). That additive loss is the strongest part of the degree-(d) result.

The residue section also improves the affine theory materially. The quantity
[
eta(P)=left(sum_x|operatorname{Res}_{z=x}M(z)^{-1}|_{m op}
+gamma(P)^{-1}ight)^{-1}
]
is actually observable from the recovered pencil and no longer defined by optimizing over latent factorizations. The paper proves a zero set, one-sided inverse estimate, lower/upper semicontinuity statements in the correct directions, and an explicit jump example at a partial collision.

These are real advances over v87.

---

## 2. Audit of the normalization-defect theorem

### 2.1 Lemma 2.1 is mathematically credible

The gcd argument is sound-looking.

Full column rank of (U,V) allows constant left/right inverses and therefore reduces common divisors of the entries of (K) to common divisors of the scalar component polynomials. If (rinkermathcal N_P), the interpolating polynomial (H) satisfies
[
qH-rK=0
]
at (2d+1) nodes, hence identically. Cancelling the common gcd and using a Bézout identity for the entries of the reduced numerator gives the claimed divisibility of (r).

I found no short defect in this proof.

### 2.2 Lemma 2.2 is also basically correct, but one argument should be written more defensively

The positive local fibre construction is natural:
[
q_u=q+ur,qquad K_u=K+uH,
]
followed by renormalizing each scalar component polynomial by its leading coefficient.

For simple interior roots, sufficiently small coefficient perturbations preserve (d) real roots in disjoint brackets, and positivity of the weights persists.

The last paragraph says that if the aggregate root multiset stayed fixed then each component root “would have to equal that value.” Because cross-component collisions are explicitly allowed, this should be made precise. The clean statement is that every continuously tracked root path takes values in a fixed finite multiset and is therefore locally constant; hence every monic component polynomial is unchanged. The present wording is plausible, but the collision case deserves the explicit topological argument.

This is a proof-writing issue, not a counterexample.

---

## 3. The (2d+1) clock result is exact but less conceptually broad than the headline suggests

Proposition 2.3 is correct-looking as a worst-case statement, but its significance should be interpreted carefully.

For (k=2), the obstruction follows from a scalar residual-space dimension count. For arbitrary (k), the construction chooses
[
f_b=(1-s_b)f+s_bg,
]
so the whole numerator lies in the span of only two fixed matrices. After normalization, the observed curve lies on an affine line in matrix space. The arbitrary-(k) lower-bound example is therefore an embedding of an essentially scalar/two-function rational interpolation obstruction into a higher-capacity latent model.

That proves the proposition as stated. But it does **not** show that (2d+1) clocks are intrinsically necessary for a genuinely (k)-dimensional matrix-valued curve or for a generic full-complexity projective polynomial experiment.

At a top-four level, this distinction matters. “Sharp for every fixed latent capacity” is technically true, but the sharpness is inherited from a deliberately low-functional-rank submodel.

I would ask the authors either to emphasize this explicitly or to prove a stronger generic/sharp complexity statement for richer curves.

---

## 4. The central spectral perturbation lemma is plausible, but the novelty comparison is still not adversarial enough

Lemma 2.4 is the key gap-free root-matching statement.

The proof uses the diagonal resolvent estimate
[
|D_f(z)^{-1}|
lesssim operatorname{dist}(z,Lambda)^{-d}
]
and a homotopy/argument-principle count. Under within-component simple roots, the resolvent improves to first order in the distance even if roots from different components coincide. This is consistent with semisimple cross-component collisions: the repeated aggregate eigenvalue is block-diagonal with simple scalar roots in the individual blocks.

I do not see an immediate mathematical contradiction.

However, this is precisely where the manuscript must be compared to the strongest matrix-polynomial and generalized-eigenvalue perturbation theory. The revision now cites Chu, Tisseur--Higham, Higham--Mackey--Tisseur and Su--Bai, which is a substantial improvement. But the claim of conceptual novelty still depends on distinguishing:

1. classical semisimple/repeated-eigenvalue root perturbation for an already specified polynomial matrix; from
2. the new projective-normalization-to-coefficient conversion.

That distinction should be made theorem-by-theorem, not only in prose.

The paper's genuinely new candidate contribution is not “roots can be matched through collisions.” That mechanism is classical. The contribution is that the missing normalization is recovered from probability observations and its error enters additively before the classical spectral perturbation stage.

The exposition is close to saying this, but a top-four submission needs the novelty boundary to be completely unmistakable.

---

## 5. The largest remaining conceptual gap: the observable singular invariant exists only in degree one

This is the main mathematical reason I do not think v88 crosses the top-four threshold.

For the degree-(d) theorem, the inverse modulus still uses
[
kappa=sigma_k(U)sigma_k(V),
qquad
	au(P)=sigma_{min}(mathcal N_P).
]
Here (	au(P)) is observable, but (kappa) is a latent representation quantity.

For the affine theorem, the authors do much better: they replace the latent factor optimization by the residue quantity (eta(P)), which is constructed from the observable reduced pencil and is invariant under the choice of orthonormal frames.

Thus the paper does **not** yet possess one structural singular invariant for the polynomial experiment. It possesses:

- an observable normalization invariant (	au) in all degrees;
- a latent channel condition (kappa) in all degrees;
- and a fully observable residue condition (eta) only when (d=1).

This leaves the main conceptual request from the v87 report only partially resolved.

A genuinely stronger theorem would construct an observable degree-(d) condition—probably from the recovered matrix polynomial, its inverse/resolvent data, a structured smallest singular value, or an equivalent quotient metric—and prove the polynomial spectral modulus directly in terms of that condition.

Until that exists, the degree-(d) result and the affine singular-quotient result remain two adjacent layers rather than one unified theory.

---

## 6. (eta) is a useful observable certificate, but it is not yet shown to be *the* intrinsic condition number

Theorem 3.2 is careful and mostly avoids overclaiming. In particular, the paper explicitly states that (eta) is not asserted to be a distance-to-discriminant formula.

That caution is appropriate.

What is actually proved is:

- an observable construction;
- a precise positivity/zero-set statement inside the affine model;
- one-sided inverse control;
- lower semicontinuity of (eta);
- upper semicontinuity of (eta);
- continuity on fixed multiplicity strata;
- and (etage cartheta_*).

What is **not** proved is:

- a two-sided comparison between (eta) and the exact local modulus of the observation map;
- equality with a metric slope or inverse metric-regularity constant;
- comparison with distance to the nonidentifiable observation set;
- a pointwise lower bound showing that every datum has local difficulty of order (1/eta(P));
- or an analogue beyond affine pencils.

The jump example itself highlights this. When two actions collide, (eta) can jump from (9) to (6), so (eta) jumps upward. That is consistent with upper semicontinuity and may reflect a genuine simplification of the multiset target, but it also shows that (eta) is not behaving like an ordinary continuous distance-to-singularity function.

For a specialist paper, the present theorem is interesting. For a top-four theorem advertised as a singular invariant, I would want a sharper intrinsic characterization.

---

## 7. The direct estimator is a useful addition, but the computational contribution remains limited

Theorem 4.1 is a genuine improvement over an existence-only residual minimizer.

The proposed point estimator is explicit:

1. solve the observed normalization equation by least squares;
2. interpolate the cleared observations;
3. take leading singular subspaces;
4. reduce to a (k	imes k) matrix polynomial;
5. compute its (kd) roots.

The proof correctly mirrors the deterministic inverse theorem. In the affine case, the argument uses the observable residue bound rather than an a priori latent conditioning floor.

This is valuable.

But the computational statement remains an exact-arithmetic stability theorem, not a numerical complexity theorem. The manuscript explicitly admits this, which is correct. In particular:

- exact rank and singularity tests are not robust numerical stopping rules;
- no finite-precision thresholding theorem is proved;
- no bit-complexity bound is given;
- and the confidence region remains a global information-theoretic optimization.

Thus “constructive” should be read as “explicit algebraic procedure,” not as a full computational-statistical solution.

That is acceptable, but it limits how much additional general-journal weight the algorithmic section carries.

---

## 8. The statistical theory is still affine-only

Revision 88 extends the algebraic inverse problem to degree (d), but the sharp inference theorem remains in the (d=1) experiment.

Theorem 5.4 gives the class-sharp order
[
min{1,(Ns^2)^{-1}}
]
for (eta)- and (artheta_*)-signal classes, including adaptive clock selection. The product family and collapse family are well chosen, and the KL chain-rule argument is clean.

I found no immediate defect in the adaptive-design reduction. The clock kernels are parameter-independent conditional on the observed history, so the conditional KL contribution from clock selection is zero and the complete transcript entropy is controlled by the uniform single-clock bound.

But this remains a class-level theorem generated by two explicit least-favourable families in the affine model.

Revision 88 does **not** provide:

- minimax rates for the degree-(d) model;
- a rate depending on the multiplicity structure of repeated scalar roots;
- a stratified local minimax theorem at intersections of normalization defects, channel-rank loss and root multiplicity;
- or a pointwise equivalence between the local risk and (eta).

The final paragraph correctly says that the results are class-sharp and pathwise sharp rather than a complete classification. That limitation is important enough to be stated even more prominently near the abstract.

---

## 9. The literature audit is improved, but it still omits a very close rational-realization / matrix-GCD line of work

This is the strongest new literature objection in this review.

The revision now discusses Van Barel--Bultheel, Chu, Higham--Mackey--Tisseur, Tisseur--Higham, Su--Bai and Bhaskara--Charikar--Vijayaraghavan. That directly answers much of the v87 criticism.

However, the degree-(d) theorem is now so explicitly a **matrix-valued rational interpolation / common-denominator / finite-realization problem** that comparison to one vector-rational-interpolation paper is not enough.

At minimum the authors should compare to the rational-realization and matrix-interpolation literature represented by:

- B. D. O. Anderson and A. C. Antoulas, *Rational interpolation and state-variable realizations*, Linear Algebra Appl. 137/138 (1990), 479--509, DOI 10.1016/0024-3795(90)90140-8;
- B. Beckermann and G. Labahn, *Fraction-Free Computation of Matrix Rational Interpolants and Matrix GCDs*, SIAM J. Matrix Anal. Appl. 22 (2000), 114--144, DOI 10.1137/S0895479897326912;
- A. J. Mayo and A. C. Antoulas, *A framework for the solution of the generalized realization problem*, Linear Algebra Appl. 425 (2007), 634--662, DOI 10.1016/j.laa.2007.03.008;
- and the broader Loewner / simultaneous Padé / matrix rational interpolation literature.

These works are not cited here as counterexamples to Theorem 1.1. I am not asserting that they already prove the stochastic gcd/nullity identity or the additive observation modulus.

The problem is one of novelty control. Loewner and related realization frameworks recover rational matrix functions from finite interpolation data, encode minimal complexity through ranks of data matrices/pencils, and connect interpolation to generalized eigenvalue realizations. Matrix rational interpolation work also treats singular solution tables and matrix GCD structure.

A top-four paper whose first main theorem is a finite-sample common-denominator rank criterion with a gcd defect must explain exactly what is genuinely new relative to that literature.

The present audit does not yet do so.

---

## 10. The paper is still highly model-specific

The degree-(d) theorem sounds broad, but the model retains a long list of rigid assumptions:

- one scalar normalization (q(T));
- all component polynomials monic of the same known degree (d);
- simultaneous diagonal structure with fixed left and right stochastic channels;
- known latent capacity (k);
- a fixed positive weight floor;
- all component roots constrained to one known compact interval;
- controlled clocks outside that interval;
- finite-dimensional categorical matrices;
- fixed dimensions and fixed clock geometry;
- constants allowed to depend on all of the above.

These assumptions are not illegitimate. They define a coherent inverse problem.

But the theorem is not yet an abstract projective-polynomial quotient theorem. It is a theorem for a favorable simultaneously diagonalizable model.

The manuscript would become substantially more compelling if it identified an invariant formulation that survives after removing at least one of:

1. common degree and monicity;
2. simultaneous diagonalization;
3. the single scalar normalizer;
4. fixed finite dimension;
5. or the known latent capacity.

At present the phrase “projective polynomial observations” describes the model correctly, but it should not be read as a general theory of projective polynomial matrix inverse problems.

---

## 11. No dimension-uniform content has been added

As in v87, all constants may depend on
[
d,k,m_1,m_2,alpha_*,L,D,T_1,ldots,T_ell.
]

The paper now allows arbitrary fixed (d) and arbitrary fixed (k), but this is algebraic generality rather than a dimension-uniform theory.

There is no estimate showing how:

- (	au(P));
- (eta(P));
- the interpolation constants;
- the clock geometry;
- or the minimax constants

scale as degree or latent dimension grows.

This matters because the paper now uses phrases such as “degree-(d)” and “every fixed admissible capacity.” Those are correct, but they should not be allowed to suggest a stable high-dimensional theory.

A genuine dimension-uniform result would materially strengthen the submission.

---

## 12. Proof-level comments

These are not the primary reason for rejection, but they should be repaired.

### 12.1 Lemma 2.2 and cross-component collisions

Replace the sentence asserting that unchanged aggregate roots force each component root to stay equal to its original root by an explicit continuity argument for tracked roots taking values in a finite fixed multiset.

### 12.2 Proposition 2.3 should explicitly ensure a nonconstant affine-line curve

The arbitrary-(k) construction should state that the chosen channels and (s_b) make the two matrix coefficients genuinely distinct. Otherwise the reduction to a scalar residual obstruction is formally underexplained.

### 12.3 Lemma 2.4 deserves either a precise predecessor theorem or a more formal contour statement

The present disk-union argument is plausible. Because the gap-free collision claim is central, I would give a completely explicit Rouché/argument-principle formulation, including how multiplicities are counted when disk components touch in the limit.

### 12.4 The degree-(d) linear bound should be described as semisimple cross-component stability

When roots within each scalar (f_b) are simple, a collision between different components is a semisimple matrix-polynomial collision. Saying this explicitly would make the absence of an aggregate spectral gap much less mysterious and would improve the comparison with classical perturbation theory.

### 12.5 Theorem 3.2 should distinguish “observable invariant” from “sharp condition number”

The theorem itself is careful, but the surrounding prose occasionally invites the stronger interpretation. I would state explicitly near the theorem that only a one-sided modulus and familywise matching lower bounds are proved.

### 12.6 Numerical implementation of Theorem 4.1

The exact-arithmetic fallback conditions use exact rank/singularity tests. A practical implementation should use thresholds tied to the observed singular values. If no numerical theorem is intended, say this immediately in the estimator definition rather than only after the proof.

### 12.7 Statistical extension to (d>1)

The text says that Lemma 5.1 and Theorem 1.1 give an analogous polynomial confidence modulus. This is true at the deterministic-modulus level, but the paper does not supply matching degree-(d) lower bounds. The wording should avoid suggesting a sharp degree-(d) inference theory.

---

## 13. Reproducibility status

The repository evidence is organized responsibly.

I credit the following branch-local facts:

- `v88-local-verification.json` reports passed finite symbolic, numerical and source-structure diagnostics;
- the diagnostics include exact kernel cases in degrees one through three, a four-clock quadratic fibre, collision examples, reconstruction examples and least-favourable-family checks;
- `v88-local-build.json` records a successful local 16-page native build;
- source blob hashes and SHA-256 hashes are recorded;
- the records explicitly state that the diagnostics are not formal proof certification;
- the local preservation check is explicitly marked as not run in the manuscript-only workspace.

I do **not** credit an independent GitHub Actions build at the reviewed source commit. The v88 branch is one commit ahead of the controlling v87 review and contains the workflow definition plus local evidence, but not a subsequent workflow-generated publication commit containing the native PDF/evidence files.

This is not a mathematical objection.

The finite checks are useful regression evidence; they do not materially affect the top-four editorial assessment.

---

## 14. What would materially change my assessment

Another revision should not add one more special observation regime. The paper now needs one genuinely structural step.

### 14.1 Construct a degree-(d) observable singular condition

Replace the latent (kappa) in the polynomial theorem by an observable quantity derived from the recovered polynomial matrix, or prove equivalence between such a quantity and the exact quotient modulus.

This would unify the two halves of v88.

### 14.2 Prove a two-sided local conditioning theorem

Identify the exact local metric regularity / inverse modulus, at least on natural strata, rather than only giving an upper bound and two least-favourable paths.

### 14.3 Connect explicitly to rational realization and matrix interpolation

A precise comparison theorem with Loewner/rational-realization/matrix-GCD methods could itself be a significant contribution if it shows that the stochastic/projective structure yields a genuinely different rank defect or conditioning law.

### 14.4 Extend sharp inference beyond (d=1)

Determine how normalization defects and repeated roots alter minimax exponents for the degree-(d) model, and prove matching lower bounds.

### 14.5 Give a genuinely broader quotient theorem

Show that the normalization-defect/additive-loss mechanism survives for a natural class of rational or polynomial matrix curves not assumed simultaneously diagonalizable with one common scalar normalizer.

### 14.6 Add explicit dimension dependence

If arbitrary degree/rank is to carry major conceptual weight, derive quantitative dependence on (d,k,m_1,m_2,alpha_*) and clock geometry.

Any one of these, if done strongly, would justify another top-four-level review.

---

## 15. Final assessment

Revision 88 is the strongest A2 version I have reviewed.

It has crossed an important threshold: it is no longer merely an affine one-pole theorem plus an archive of other regimes. The degree-(d) normalization theorem is real, the gcd/nullity identity is clean, the additive conditioning mechanism is useful, and the observable affine residue construction is a genuine response to the previous referee report.

I found no short fatal proof error in the principal claims.

Nevertheless, the paper still falls short of the four leading general mathematics journals for a structural reason.

The most general theorem still depends on a latent channel condition and belongs naturally to the matrix-valued rational interpolation / matrix-polynomial perturbation world. The genuinely intrinsic observable condition and the sharp inference theory remain affine. The novelty audit has improved but still does not confront the matrix rational realization, Loewner and matrix-GCD literature closely enough. The sharp (2d+1) example for arbitrary latent capacity is obtained from an effectively one-dimensional rational submodel. No dimension-uniform or stratified degree-(d) inference theorem is present.

Accordingly my recommendation is:

**Reject in the present form at the stated top-four level.**

I would regard the current manuscript as a serious candidate for a strong specialist journal after the remaining literature and proof-presentation issues are repaired. A further four-leading-general-journal revision would require one of the structural advances listed in Section 14, not additional finite diagnostics or another collection of model-specific regimes.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*
