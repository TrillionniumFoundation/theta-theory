# Response to the referee of A2 v82

**Revision:** A2 v83, *Action rigidity with selective detection*  
**Controlling report:** `reviews/a2-v82-selective-detector-rigidity-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md` at `b7075ecdeacb42befd55d4c732cbff4706fb4aca`.  
**Reviewed source:** v82 head `0ae206f918edd06f233e1c6493fb20a598cdda89`.  
**New branch:** `revision/a2-v83-sharp-clocks-global-quotient-2026-09-18`.

We thank the referee for distinguishing the exact identification argument from the unsupported global interpretation of its local perturbation charts. The revision replaces that interpretation by a quantitative synchronization theorem. It also resolves the four-deadline question and replaces the nonsharp polynomial extension by a sharp theorem and a detector-space criterion. The absolute-action conclusion is strengthened, not replaced by recovery up to an additive constant.

The principal article is now self-contained: `papers/A2-v17-boundary-information-coarsening/rigidity_v83.tex`. Its expanded edition, `rigidity_v83_full.tex`, includes the same principal article and every mathematical input of the preceding integrated manuscript, including the entire v82 selective-detector proof. No previous manuscript, review, derivation, or default-branch file is rewritten. References below use stable source labels; the principal PDF also supplies ordinary numbered statements.

## Principal mathematical changes

Theorem `thm:v83-main` proves that **q+3 deadlines suffice globally and are optimal in the worst case** when the branchwise log-detector has degree at most q. In particular four, not five, suffice for the log-affine model, without an added action-order assumption. The lower bound is an action-changing level set within the same positive, full-rank two-component observation class.

Theorem `thm:v83-classification` gives an invariant necessary-and-sufficient condition for sampled nuisance spaces of codimension two whose annihilator contains a positive Cauchy kernel. It is a strict two-function Chebyshev condition. Proposition `prop:v83-exponential` gives a genuinely nonpolynomial application, with log-detector beta times exp(lambda T), unknown beta, and known positive lambda: four equally spaced deadlines are again sufficient and worst-case necessary. Spectral separation for that family is proved, not silently inherited from the polynomial case.

Theorem `thm:v83-global` constructs an open-neighborhood inverse modulo the common detector gauge and component-covering isomorphisms. Nearest-column matching first produces an exact permutation cocycle under noise; fibrewise centering removes the gauge; only then are the local outputs glued. A three-cycle example shows why connectedness cannot replace simple connectedness in a global enumeration claim.

Theorem `thm:v83-unobserved` gives a localized Hamiltonian ambiguity outside a sampled orbit tube, even if the observed lifted iterates themselves are supplied. It explains a specific necessity for phase-domain information in the smooth class. The positive covered-domain return theorem and nonconvex action-crossing example remain, with a persistence argument for a neighborhood of exact lifts.

## Major comments

### R82-M1 — Noisy permutation and gauge gluing

Addressed by Lemmas `lem:v83-local` and `lem:v83-match`, followed by Theorem `thm:v83-global`. The signature is the recovered channel column in the original readout space, not an eigenvector in a changing minor basis. With true column gap s_* and local errors e<s_*/4, corresponding columns are at distance at most 2e and noncorresponding columns at least s_*-2e>2e. The unique match identifies the same true column on every overlap; hence the transition permutations satisfy the exact cocycle on triple overlaps. We center log-weights and every detector coefficient before applying a partition of unity. Arbitrary off-model outputs need not be exact latent matrices, and we do not assert otherwise.

### R82-M2 — An invariant error metric

Equation `eq:v83-quotient-metric` minimizes the C^m distance between centered fields over covering isomorphisms over the identity of the endpoint domain. There are finitely many such isomorphisms. On a simply connected gate this reduces to one minimum over constant permutations. It is not a pointwise, independently chosen permutation loss. The estimate compares any two nearby off-model data fields on the fixed local covering stratum.

### R82-M3 — Changing spectral choices

Equation `eq:v83-finite-combinations` supplies a deterministic finite candidate set. The local-extension proof derives a separating gap from a finite inverse-Vandermonde bound. Different minors and combinations are compared through their original-space channel signatures. Lemma `lem:v83-match` supplies the required quantitative overlap argument even though the perturbed reduced operators need not commute.

### R82-M4 — Local and global stability

These are now separate statements. Lemma `lem:v83-local` is the local finite-dimensional extension and C^m estimate. Theorem `thm:v83-global` adds matching, gauge compatibility, covering topology, fixed transition permutations, and the global partition-of-unity estimate. Neither is used as a substitute for the other.

### R82-M5 — Connectedness and global enumeration

The exact output on a general connected domain is a component covering. Simple connectedness trivializes that covering by path lifting. Mere connectedness only makes two already existing global enumerations differ by a constant permutation. Proposition `prop:v83-monodromy` constructs a positive full-rank example over a circle with a genuine three-cycle. The noisy theorem preserves its monodromy rather than pretending to eliminate it.

### R82-M6 — Local action recovery versus the supplied phase cover

Theorem `thm:v83-return` states the endpoint gates, canonical coordinates, return counts, common deterministic lift, inverse-factor domains and collars explicitly. The supplied/recovered table distinguishes these inputs from recovered counts, channels, actions, graph pairing and primitives. Its noisy proof fixes phase-coordinate charts before averaging map-valued extensions. This does not infer a global section from endpoint matrices.

### R82-M7 — Global geometric information

We provide a necessity result rather than rename the covered theorem as an unmarked global theorem. In `thm:v83-unobserved`, a compactly supported Hamiltonian perturbation away from every observed finite orbit segment preserves the full lifted observations, including primitive constants, but changes a designated unsampled target. The proof is exact. It applies to the declared smooth exact-lift class and restricted orbit observations, not automatically to every billiard subclass. It establishes a concrete obstruction, not necessity of every individual sufficient hypothesis in the return theorem.

### R82-M8 — A structural detector criterion

Theorem `thm:v83-classification` describes the sampled nuisance subspace through its annihilator kernels. Within the stated positive-kernel class, ordered unequal actions are identifiable exactly when the ratio of two kernels is strictly monotone, equivalently when their two-point determinant has one strict sign. The criterion is invariant under a change of annihilator basis. Spectral separation and injectivity of an underlying function-space evaluation map remain separate requirements where relevant.

### R82-M9 — Beyond polynomial interpolation counting

The proof now uses an oriented interval with a known positive density. Two consecutive contrasts are its weighted moments; their kernel ratio is strictly monotone. Lemma `lem:v83-interval` proves both sufficiency and necessity for this interval problem. The polynomial theorem follows as one application. Proposition `prop:v83-exponential` supplies a nonpolynomial application and proves its own latent separation and lower bound. We identify the classical Chebyshev terminology rather than claiming new general moment theory.

### R82-M10 — Four versus five deadlines

Resolved by `thm:v83-scalar` and `thm:v83-main`. Four are globally sufficient in the unrestricted stated log-affine class with an unequal-action anchor. Three have an action-changing ambiguity. More generally q+3 is the sharp worst-case polynomial count. No extra ordering of actions is assumed; the orientation is obtained from the sign of a positive-kernel contrast. The old five-clock proof remains valid and retained, but is no longer the sharp principal result.

### R82-M11 — The engineered shear

The explicit example is retained and strengthened by a persistence argument for small exact perturbations on fixed finite orbit tubes. The outer action crossing is transverse, with derivative 2 in the endpoint difference at the reference diagonal; regularity, rank, detector separation and coverage persist on smaller fixed domains. We do not present this as a theorem for all billiards. The new conceptual contribution is the sharp observation theorem and detector classification; the smooth geometric limitation is separately proved by localized perturbation.

### R82-M12 — Marked billiard consequences

The marked/reference-atlas derivations are retained in the expanded edition with their actual semantic marks, scalar registrations and hypotheses. Recovered latent indices are not identified with word or lift names. No universal unmarked billiard invariant, unobserved caustic continuation, or optimal geometric sampling exponent is claimed. These are retained boundaries of the geometric statements, not a weakening of the new absolute-action theorem.

### R82-M13 — Comparison with Chebyshev and interpolation methods

The introduction and the detector-quotient section cite de Boor on divided differences and Karlin--Studden on Chebyshev systems. The new proof explicitly distinguishes an interval with known density from an arbitrary measure. The two-moment criterion, its necessity proof, the sharp polynomial count and the nonpolynomial application replace an informal appeal to rational zero counting. The literature comparison identifies close mechanisms; it does not claim an exhaustive priority certification.

### R82-M14 — Latent-variable priority

The matrix recovery is attributed to the classical latent/spectral tradition, including Allman--Matias--Rhodes, Anandkumar--Hsu--Kakade and Bonhomme--Jochmans--Robin. Its explicit formulas are retained because normalization and chart changes matter to this problem. Generic tensor uniqueness and joint diagonalization are not advertised as new results.

### R82-M15 — Theorem-level positioning

The introduction now contains a predecessor/input/conclusion table. The proof ledger separates classical ingredients, the new scalar and quotient conclusions, and retained geometric assumptions. The deterministic lift identity is identified as elementary, not the source of a purported new global rigidity theorem by itself.

### R82-M16 — A coherent principal article

The principal entry has one central theorem, followed by its scalar proof, exact component reconstruction, global noisy inverse, and geometric consequences. It contains all proofs needed for its claims and its own bibliography. It is not a ten-page extract relying on absent companion proofs. Delivery status and referee process discussion are outside this principal article.

### R82-M17 — Preservation without revision-history overload

The expanded entry includes the complete new article and every previous mathematical input, with a short appendix notice identifying the stronger clock count and the repaired global noisy inverse. The previous source files are inherited unchanged. Thus the focused principal reading order does not delete the conditional quotient, calibrated statistics, convex regularity, physical compensation, marked billiard reconstruction or the old five-clock argument.

## Technical comments

| Comment | Revision and exact location |
|---|---|
| R82-T1 | Covering formulation and simple-connectedness argument in the proof of `thm:v83-main`; nontrivial example `prop:v83-monodromy`. |
| R82-T2 | Centered quotient metric `eq:v83-quotient-metric` and global estimate `eq:v83-global-estimate`. |
| R82-T3 | Exact cocycles versus unequal off-model chart values are separated before `eq:v83-gluing`; exactness holds on the fixed visible-rank model stratum. |
| R82-T4 | Explicit anchor threshold a_0=gamma/R^(q+2), contrast-error allowance a_0/4, acceptance threshold a_0/2, and induced action-separation bound in `lem:v83-local`. |
| R82-T5 | Observable rank/minor/spectrum/contrast selection is distinguished from compactness and from finite-mesh certification in the quantitative-chart subsection. |
| R82-T6 | Off-model local projectors are extended separately; channel matching supplies exact transition permutations before averaging. |
| R82-T7 | Only centered detector coefficients are bounded. The common polynomial gauge is removed, not estimated. |
| R82-T8 | The constant polynomial coefficient is log a_b; the nonconstant sum begins at degree 1. Both are centered fibrewise. |
| R82-T9 | `cor:v83-error` uses a singular-value signal margin. The following discussion explicitly excludes exact discovery of arbitrarily weak extra components under unrestricted misspecification. |
| R82-T10 | Sharp q+3 theorem; in particular a global four-clock inverse and three-clock ambiguity for q=1. |
| R82-T11 | `prop:v83-physical` specifies separate independent randomizations conditional on the trajectory and deadline-invariant channels. Copying a noisy reading is not sufficient. |
| R82-T12 | The detector is unknown within a prescribed finite-dimensional family. `prop:v83-obstructions` retains the exact unrestricted-detector compensation. |
| R82-T13 | Supplied/recovered table following `cor:v83-contact`, with phase-domain and section assumptions explicitly on the supplied side. |
| R82-T14 | The complete self-contained 16-page principal article was natively built, including references. Normal and optimized runs each passed 22 checks. The retained expanded edition has a separate build target and preservation audit; its native build is not represented by the principal build. See `VERIFICATION.md` for the exact executed status. |
| R82-T15 | Process and verification language is confined to the response, ledger and handoff. The principal article uses mathematical hypotheses, statements, proofs, examples and literature attribution. |

## Verification and remaining review questions

The regression suite checks algebra, monotone inverses, sharpness examples, spectral recovery through an action coincidence, overlap cocycles, error scaling, rank thresholds and the nonpolynomial kernels. These checks are not independent certification of the general theorems. The manuscript contains the proofs.

The remaining editorial question is whether the sharp detector-quotient and global reconstruction theorems meet the journal's significance threshold. We do not answer that by self-rating or by changing the target. The mathematical statements continue to recover absolute actions. A universal unmarked billiard theorem, global-section discovery and recovery through unsampled caustics are not silently added to their conclusions. The new revision is offered for another independent examination of the stated stronger results.
