# Independent harsh referee report on A2 revision 86

**Review date:** 18 September 2026  
**Reviewed branch:** `revision/a2-v86-shared-nuisance-singular-transition-2026-09-18`  
**Reviewed head:** `bf67e3f33d394c80d7d7daeb51e52de12ec3d180`  
**Principal manuscript:** `papers/A2-v17-boundary-information-coarsening/rigidity_v86.tex`  
**Core new-results extract:** `papers/A2-v17-boundary-information-coarsening/rigidity_v86_core.tex`  
**Controlling previous report:** `reviews/a2-v85-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`

## Editorial recommendation

**Reject in the present form at the standard of a four-leading-general-mathematics journal.**

Revision 86 is a real mathematical improvement over revision 85. It does not merely repackage the previous manuscript or improve exposition. In particular, it closes two of the strongest objections in the preceding report: it gives a genuinely structured shared-nuisance clock threshold, and it computes a nonregular rank-degenerate statistical transition with matching upper and lower orders. The compact-Riemann-surface extension is also mathematically legitimate and broader than the earlier rational partial-fraction theorem.

Nevertheless, I do not think the paper has crossed the threshold for a leading general mathematics journal. I do **not** base this recommendation on a short counterexample to the new principal theorems. The main problem is scale and architecture: the new advances are still confined to rather special observation models, the meromorphic clock counts are sufficient rather than sharp, the geometric consequence still imports the hard rigidity theorem, and the manuscript continues to accumulate several largely parallel mechanisms without a theorem that genuinely unifies them.

The new results would merit serious consideration in a strong specialist venue. For the stated target, another revision would need at least one theorem whose generality and conceptual force reorganize the rest of the paper around it.

## 1. What v86 genuinely fixes

The previous report asked for changes of mathematical scale rather than more source engineering. Revision 86 does make such changes.

First, Theorem `thm:v86-shared` changes the nuisance structure rather than merely increasing a pointwise clock budget. The proof uses the spatial domain to remove the clock-only nuisance while controlling the residual label inversion. The linear-versus-quadratic obstruction calculation is clean and produces a sharp exact-identification contrast between two clocks and one clock in the geometric corollary.

Second, Theorems `thm:v86-product-modulus`, `thm:v86-adaptive`, and `thm:v86-singular-lower` replace the vague statement that conditioning deteriorates near rank loss by an explicit product modulus
[
ho=|det U,det V|.
]
The determinant-after-pole-clearing argument is the strongest new proof in the revision. The exact marginal-preserving least-favourable family also shows that the product is not an artefact of a crude spectral estimate.

Third, Theorems `thm:v86-divisor` and `thm:v86-divisor-budget` move the detector classification from rational partial fractions to normalized meromorphic differentials on compact real Riemann surfaces. The positive-genus period correction is a genuine extension of the earlier principal-part discussion.

These are substantive repairs. A harsh report should credit them.

## 2. The shared-apparatus theorem is elegant but still too model-specific

Theorem `thm:v86-shared` is probably the cleanest conceptual theorem in the revision. With two clocks, unknown site-dependent full-rank channels, and two shared positive constants (k_1,k_2), the action field is identified from the matrix fields under the nowhere-local-constancy assumption.

The proof is persuasive. At a regular site the observable pencil identifies the two weights up to simultaneous inversion. A false direct calibration can persist at only one action value and a false swapped calibration at only two action values. A nowhere locally constant field cannot live on this finite obstruction set. I found no immediate gap in this argument.

The limitation is that the exact threshold depends heavily on all of the following simultaneously:

- two latent components;
- exactly two clocks;
- a nuisance that is shared only through two scalar clock constants;
- full-rank channels at every site;
- a spatial action with no open plateau;
- exact noiseless matrix fields.

The theorem does not yet provide a quantitative global stability theory for this shared-nuisance problem. Proposition `prop:v86-calibration` gives a local inverse after the correct labels have been fixed and gives a finite four-site calibration procedure, but it does not compute the stability modulus as one approaches profile collisions, nearly repeated action levels, or nearly admissible swapped calibrations.

For a leading general journal, the natural next theorem would not merely be another exact threshold. It would identify the **quantitative condition number or modulus of the shared quotient itself**, including how it degenerates near the finite obstruction set, and then prove matching statistical lower bounds. At present the shared theorem and the singular-statistical theorem are separate modules; the paper has not yet derived one from the other.

## 3. The one-clock geometric lower bound is legitimate, but the geometry is still imported

Corollary `cor:v86-shared-geometry` is materially stronger than the v85 endpointwise-free nuisance construction. The reference delay and detector law are held fixed, and the metric alternatives are actual scaling metrics. The channel transformation then absorbs the one-clock change while preserving positivity and full rank for small perturbations.

I do not see a short algebraic defect in the transformation
[
S_t=I+(w_0-w_t)mathbf 1^{mathsf T},
quad
U_t=US_t,
quad
V_t=Voperatorname{diag}(w_0)S_t^{-mathsf T}
      operatorname{diag}(w_t)^{-1}.
]
The proof correctly distinguishes the auxiliary matrix (S_t), which need not be stochastic, from the actual channel matrices.

However, after the boundary distance has been identified, the metric conclusion is exactly the classical simple-surface rigidity input. The revision is explicit about this, which is good. It also means that the geometric part still does not create a new rigidity mechanism, a partial-data theorem, a non-simple theorem, or a weaker-regularity theorem.

At the stated editorial level, the two-clock acquisition threshold is interesting, but the geometric consequence remains a transfer theorem. The hard geometry is not new mathematics of this paper.

## 4. The determinant-product modulus is the strongest new result, but it is confined to one low-dimensional singular stratum

Theorem `thm:v86-product-modulus` is the principal reason I regard v86 as substantially stronger than v85.

The representation
[
P(T)=A+rac{B}{T-h}
]
extracts the common pole from the three-clock binary model. The first ratio identifies (h) at visible-contrast scale. The determinant of
[
K(T)=(T-h)P(T)
]
then factors as
[
det K(T)
=
r(1-r)det U,det V,(T-x)(T-	au).
]
The proof avoids multiplying two generic inverse singular values and retains exactly one inverse power of (ho). This is a meaningful cancellation.

I checked the key steps at theorem level and did not find an immediate contradiction:

- the true matrix contrast controls the pole ratio;
- in the small-error regime the candidate contrast remains nonzero;
- the determinant coefficient perturbation can be bounded before division by (ho);
- the ordered roots remain separated by the fixed apparatus gap;
- the recovery of (r), hence (log a), follows from the recovered roots and pole.

This part is substantially more than a routine application of a generic inverse function theorem.

The problem is scope. The singular theory is proved for:

- binary (2	imes2) channels;
- a constant relative detector;
- exactly three clocks;
- a scalar action/reference/throughput triple;
- one particular rank-degenerate boundary.

The manuscript does not yet classify singular strata for higher latent rank, higher-degree detector spaces, repeated components, shared apparatus over space, or the larger observation models treated elsewhere in the paper.

For a general-journal theorem, I would expect a result that explains **why the exponent is the product of the vanishing channel contrasts as an invariant of the observation quotient**, and then extends that mechanism beyond the (2	imes2) calculation. Right now the proof is excellent local mathematics inside one specially chosen model, but it has not become a general singular theory.

## 5. The adaptive confidence result is honest, but the paper should be precise about what has been generalized

Theorem `thm:v86-adaptive` is carefully stated. It gives coverage over the full closed model, uses no supplied rank floor, and obtains the expected-length and risk bounds
[
mathbb E wlesssim
min{1,(sqrt Nho)^{-1}},
qquad
mathbb E|widehat x-x|^2
lesssim
min{1,(Nho^2)^{-1}}.
]
The lower-bound theorem supplies matching orders.

This does address the most serious statistical objection in v85. The exact lower-bound family is especially useful because both marginals are fixed and only a joint interaction changes.

Still, the result should not be advertised as a general theory of honest adaptation near nonidentification. It is a sharp solution to one nonlinear finite categorical experiment. The references to Donoho, Cai--Low, and Dufour appropriately acknowledge the classical modulus and weak-identification principles, but the paper has not yet identified the analogue of the determinant-product modulus for its other detector or geometric models.

A genuinely unifying statistical theorem would characterize the modulus for a family of observation quotients and recover the present product law as one stratum. That would be a much more convincing reason for a broad mathematics audience to engage with the statistical part.

## 6. The divisor--period theorem is correct-looking but conceptually close to classical meromorphic bookkeeping

Theorem `thm:v86-divisor` is a natural and valid extension of the rational classification.

The proof separates two issues:

1. secant collisions, whose differentiated action difference is a normalized third-kind differential with an integral charge divisor;
2. tangent degeneracies, whose action derivatives have normalized second-kind double poles.

Membership in the detector differential space then gives finite obstruction tests. The positive-genus period correction means that principal parts alone are indeed insufficient.

I found the normalization lemma internally coherent. The real-period map on holomorphic differentials has the correct real dimension, and the harmonic-function argument gives injectivity. The independence of (B_x) from the auxiliary base pole also follows from uniqueness of the normalized differential.

The difficulty is editorial rather than elementary correctness. Once the action curve is built from normalized third-kind differentials, the classification is very close to the divisor/period structure one would naturally write down. The clock budget then follows from Rolle plus the degree of the canonical divisor.

That is elegant, but at the target level I would want one of the following:

- an optimal or near-optimal intrinsic sampling number, with lower bounds;
- a new invariant characterizing when arbitrary finite-dimensional meromorphic spaces are unisolvent for the action quotient;
- a theorem on degenerating surfaces or varying divisors in which the period geometry produces genuinely new asymptotics;
- a structural result that simultaneously explains the rational, meromorphic, and branched-clock cases.

At present the theorem is broader than v85 but still feels like the natural compact-surface reformulation rather than a major new piece of Riemann-surface theory.

## 7. The intrinsic clock budget remains only sufficient

Theorem `thm:v86-divisor-budget` gives
[
N=deg D+2g+4,
]
and Theorem `thm:v86-branched` gives
[
N=deg D+4m+2g.
]

The zero-count proofs are correct-looking as upper bounds. The manuscript is commendably explicit that these counts are not claimed to be universally optimal.

That explicit disclaimer, however, leaves the principal v85 objection only partly closed. The paper still has several clock-count mechanisms whose numerical values come from different proof devices:

- the sharp polynomial threshold;
- generic analytic dimension-type thresholds;
- rational pole-degree bounds;
- compact-surface divisor bounds;
- branched pullback bounds;
- the exact two-clock threshold under shared nuisance.

The manuscript now explains why these belong to different experiments, but it does not produce a single complexity invariant that predicts the optimal count in each experiment.

For a leading general journal, a theorem identifying that invariant would be much more important than another sufficient count.

## 8. The branched-clock theorem preserves the physical logarithmic law, but it does not remove the scale objection

Theorem `thm:v86-branched` is useful because it answers the obvious objection that the compact-surface theorem changed the action curve itself. Pulling back the original logarithmic law through a finite meromorphic clock map genuinely permits nonrational detector primitives.

The proof by fibre poles and tangent pole orders appears internally consistent, including ramified action values. The elliptic example is a legitimate positive-genus example.

But again the mathematics is mostly the divisor calculation after pullback:

- secants contribute at most four action fibres;
- tangents contribute at most two fibres with ramification-dependent pole order;
- zero counting gives a sufficient design size.

This broadens the class, but it does not yet give the kind of sharp structural theorem that would make the compact-surface section the conceptual centre of the paper.

## 9. The manuscript still does not have one theorem that organizes its many regimes

The introduction now speaks explicitly in terms of three observation quotients:

- pointwise detector quotients;
- shared clock-only nuisance on a product domain;
- finite-sample matrix moduli.

This is a much better conceptual organization than earlier versions.

But “observation quotient” is still mostly a language for placing several results next to each other. There is no theorem saying, for example, that a common tangent/secant/singularity invariant controls exact identification, finite clock complexity, local stability, and minimax rates across these regimes.

As a consequence, the principal manuscript remains an accumulation of:

- latent matrix-pencil identification;
- pointwise polynomial inversion;
- rational and meromorphic obstruction tests;
- shared spatial calibration;
- singular statistical theory;
- finite covering reconstruction;
- imported boundary rigidity and stability;
- exact return-lift constructions;
- raw acquisition thinning.

Many of these components are individually sound. Their coexistence is not yet the same as a unified theory.

This was the central editorial problem in v85, and v86 improves but does not fully solve it.

## 10. The paper would benefit from a sharper distinction between a theorem paper and an archival research program

The repository preservation policy is excellent for reproducibility, but it is not automatically good article architecture.

The new v86 core is about 15 pages and contains the genuinely new theorem groups. The principal manuscript then prepends those results to the full v85 principal body, while the expanded edition preserves additional historical regimes.

For an actual top-journal submission, I would strongly consider making the new conceptual theorem spine the article and moving the inherited regime catalogue to a companion or appendix structure whose only purpose is to support the main theorems. This is not a request to delete mathematics. It is a request to distinguish the article's mathematical claim from the repository's historical completeness.

At present the reader still has to decide which of many technically correct regimes is supposed to be the reason the paper belongs in a broad journal.

## 11. Literature positioning is still too thin for the breadth of the claims

The revision adds useful predecessor paragraphs, and I appreciate the explicit statement of what is not being claimed.

Nevertheless, the literature map remains sparse relative to the breadth of the manuscript. The new paper spans:

- finite-mixture/matrix-pencil identifiability;
- shared calibration and nuisance elimination;
- weak identification and honest confidence sets;
- nonlinear finite-experiment minimax theory;
- meromorphic interpolation and divisor geometry;
- finite measurement inverse problems;
- boundary rigidity and stability.

The compact-surface section, for example, is positioned mainly against a Riemann-surface text and a real-normalized-differentials reference. That is not enough to establish that the finite obstruction and sampling theorems are new relative to interpolation/unisolvence results for meromorphic spaces.

Likewise, the statistical section cites the general modulus/adaptation precedents but does not yet compare the product singularity with the closest finite-mixture, latent-variable, weak-instrument, or algebraic-statistical singularity results.

A general-journal submission needs a much more adversarial novelty audit: each principal theorem should identify the closest theorem that an expert from the adjacent field would cite against it.

## 12. Specific proof-level points that should be tightened even though I do not regard them as fatal

I did not find a short counterexample to the new principal results, but several arguments should be written more defensively.

### 12.1 Shared-nuisance global proof

The proof of `thm:v86-shared` is correct-looking, but the global step should explicitly isolate the topological lemma being used: a continuous nowhere-locally-constant action cannot have image contained in the finite union of the direct and swapped obstruction levels on a dense open subset. The current prose is short enough that readers may wonder whether label choices can oscillate on arbitrarily fine sets. The proof does not require continuation of eigenvectors, and this should be emphasized as a separate lemma.

### 12.2 Quantitative behaviour near mixture-profile collisions

The exact theorem allows isolated or thin profile collisions, but the local stability proposition excludes them. The paper should state plainly that no global Lipschitz constant is proved as one approaches the collision set. Otherwise the exact two-clock threshold can be misread as a robust two-clock theorem.

### 12.3 Product-modulus determinant perturbation

The coefficient perturbation argument around
[
widetilde K=K-(h'-h)Q
]
is the technical heart of the proof and deserves more detail. In particular, the manuscript should explicitly write the affine scalar coefficients of (K) and (Q), show the determinant difference term by term, and then state the uniform bounded-set Lipschitz constant for the second perturbation. The current argument is plausible, but this is exactly the place where a hidden extra inverse power could enter if bookkeeping were wrong.

### 12.4 Confidence radius bookkeeping

The stated Hoeffding radius is consistent with controlling the Frobenius norms of the four-cell empirical matrices, but the factor-of-two conversion from entrywise bounds to Frobenius bounds should be shown explicitly rather than hidden in the union-bound sentence.

### 12.5 Compact-surface terminology

The manuscript uses “imaginary-period normalization” and explains its relation to real-normalized differentials. For readers from the Riemann-surface literature, the paper should fix this convention once and state explicitly whether all periods include the small loops around poles or only a homology basis on the punctured surface plus the residue loops. Nothing appears wrong, but the normalization should be impossible to misread.

### 12.6 Branched-clock divisor support

The criterion correctly uses membership in (E), which automatically sees whether the whole fibre over an action value is allowed by the divisor (D). It would still help to state explicitly that (S_pi=pi(operatorname{supp}D)cap I_0) is only a candidate action set; belonging to (S_pi) is not by itself enough for the pulled-back pole divisor to be bounded by (D).

These are revision points, not the main editorial reason for rejection.

## 13. Reproducibility and source status at the reviewed head

The source preparation is substantially more disciplined than in early revisions.

At the reviewed head:

- `verification/v86-core-verification.json` records a passed new-core diagnostic run;
- the verification script explicitly says that it is not proof certification;
- the core source graph has no missing or duplicate references/citations;
- the source commit is pinned.

However, the full native evidence described by the branch workflow had **not yet been committed at the reviewed head**. In particular, the following expected branch products were absent when I reviewed the branch:

- `verification/v86-native-verification.json`;
- `verification/v86-native-source-commit.txt`;
- `verification/v86-native-pdf-sha256.txt`;
- the compiled `rigidity_v86.pdf`.

Thus the only positive build statement I credit is the explicitly recorded new-core build. This is a source-readiness issue, not a mathematical reason for the negative editorial recommendation.

## 14. What would justify another review at this level

I would regard a further top-level review as justified if a new revision changes the mathematical scale in at least one of the following ways.

1. **A unified singular-quotient theorem.**  
   Develop a general stratified theory of the observation map in which the determinant-product law is one instance, with higher latent rank or detector complexity and sharp local minimax exponents.

2. **A sharp intrinsic clock-complexity theorem.**  
   Replace the sufficient divisor counts by an invariant that is optimal, or provably near-optimal, on a natural class of meromorphic detector spaces, with matching lower bounds.

3. **A quantitative shared-nuisance theory.**  
   Compute the global stability/minimax modulus for the two-clock spatial quotient, including degeneration near label collisions and near-obstruction action levels, instead of stopping at exact identification plus a correctly labelled local inverse.

4. **A genuinely new geometric theorem.**  
   Move beyond transfer to classical simple-surface boundary rigidity: partial data, non-simple geometry, weaker regularity, a larger global class, or a new stability mechanism.

5. **A theorem that actually unifies the manuscript.**  
   Produce one structural principle from which several of the current pointwise, shared, singular, and finite-clock results emerge as corollaries rather than parallel constructions.

Without such a step, another cycle of adding adjacent regimes would make the paper longer without changing the editorial conclusion.

## 15. Final assessment

Revision 86 is mathematically better than revision 85 in exactly the places where the previous report demanded real progress.

The two-clock shared-apparatus theorem is a genuine structured-nuisance result. The determinant-product singular transition is a nontrivial sharp calculation with matching upper and lower statistical consequences. The divisor--period extension is a valid positive-genus generalization. I did not identify a fatal short proof error in these new theorem groups.

But a four-leading-general-mathematics-journal paper needs more than a collection of strong specialist results. The central advances here remain tied to different, narrow models, and the manuscript still lacks one theorem with enough generality to make the rest of the architecture inevitable.

Accordingly, my recommendation is:

**Reject in the present form for the stated journal level.**

This is a judgment about conceptual scale and unification, not a claim that the new principal theorems are false.

---

*This is an owner-requested, independent external-referee-style assessment of the pinned repository revision, not a journal-commissioned report.*
