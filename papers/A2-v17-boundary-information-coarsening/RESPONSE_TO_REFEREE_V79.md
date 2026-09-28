# Response to the independent referee on A2 revision 78

**Revised manuscript:** *Clocked action reconstruction: robust quotients and convex twist suspensions*
**Author:** Qian Qi
**Revision:** 79, September 17, 2026
**Principal entry:** `rigidity_v79.tex` (35 pages in the accompanying build)

## Controlling source and nature of the revision

This response addresses `reviews/a2-v78-observation-quotient-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, whose Git blob is `5cdeebd441faf5ed4bf9305ab2cbe0a2b8ee6ea0`, at review commit `f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`. The reviewed manuscript head was `9b0b6c25a3194cb99ba719d118c00a23dfb8febe`, not the earlier nominal v77 branch. The substantive v77 source and the v78 sources imported by the principal article were also consulted. The prior v77 report was consulted for the history of the root-selection and principal/companion objections.

The report distinguishes correctness of the displayed mechanisms from the significance of the resulting inverse problem. We agree with that distinction. This revision does not answer the significance objection by claiming that exact normalized laws are weaker than absolute action data, nor by counting numerical checks as mathematical evidence. It adds two substantial theorem chains: a robust, statistically sharp analysis of the clock quotient and a class-wide return-clock inverse for unknown two-variable convex twist generators. These implement the report's Paths C and D, together with a contact-clock realization addressing the action-threshold objection. Their sufficiency for a general-journal contribution remains a matter for independent assessment.

All 24 proof bodies active in the reviewed principal article remain active, byte-for-byte, in the new principal article. Its 71 labels and four bibliography keys are retained. There are 12 additional proof bodies and six additional references. Four replacement source copies correct statements or their surrounding interpretation; the originals are untouched. The periodic companion remains separate and is not modified by this revision. This is not a new verification claim about the companion's complete mathematics.

## 1. The substantive mathematical changes

### A. The quotient now has an explicit ambient topology and normal coordinates

Proposition 4.1 identifies the quotient of all positive density tuples by common positive reweighting with a Banach space of anchored log-density contrasts. This is an ambient observation space, not just the exact model image. Its metric is explicit and complete.

Theorem 4.2 gives a global diffeomorphism on each nondegenerate inverse chart:

\[
 y\longmapsto (\mathcal R(y),\mathcal S(y)),\qquad
 y=\Gamma(\mathcal R(y))+\mathcal S(y).
\]

The residual belongs to a fixed complemented linear space. The inverse uses point evaluation and rational operations, with no spatial derivative loss. Corollary 4.3 compares the residual norm with distance from the shared-weight model on bounded smaller charts. Thus off-model data are not silently projected onto an undefined quotient.

### B. Misspecification, validation, and action risk are treated together

Theorem 4.4 proves a linear bias bound for clock-dependent log-weight discrepancies and characterizes all discrepancies that exactly impersonate another action. Proposition 4.5 gives the corresponding tangent/normal splitting. Proposition 5.1 turns the residual into a finite-record validation test; it does not claim optimal testing separation.

Theorem 5.2 proves matching upper and lower bounds on a specified nondegenerate Hölder class, with loss in the action's `C^m` norm:

\[
 \inf_{\widehat W}\sup \mathbb E\|\widehat W-W\|_{C^m}
 \asymp
 \left(\frac{\log n}{n}\right)^{(\beta-m)/(2\beta+d)}+\epsilon.
\]

The proof includes density-derivative estimation, a measurable bounded fallback estimator, a multiple-bump information lower bound, and an exactly indistinguishable misspecification pair. The statistical term is a classical nonparametric rate. The contribution here is its two-sided transfer through the precisely defined quotient and nuisance class, including the unavoidable linear misspecification term. This is not a minimax theorem for realizable billiard actions or for the recovered table.

### C. The generating class is genuinely two-variable, and its clock is specified

Section 10 takes an arbitrary smooth function `L(x,y)` with globally positive definite bounded Hessian and uniformly negative mixed derivative. Lemma 10.1 derives, rather than assumes, global deterministic twist dynamics, unique stationary trajectories, nonvanishing long-action twist, positive stationary Schur complements, and the physical-prefix interpretation of every matching root.

Proposition 10.2 constructs the contact suspension and proves that the action, plus a known constant per step, is its actual Reeb return time. This is classical contact infrastructure, explicitly attributed and proved here to fix the observation mechanism and sign conventions. The observer counts returns and compares their arrival with a deadline; the observer does not evaluate the unknown action.

Theorem 10.3 then constructs all endpoint gates, phase boxes, release-delay intervals and six deadlines from class bounds alone. The laws recover the complete unknown `L` on any prescribed compact square. The class includes nonseparable, nonanalytic smooth perturbations, not merely an unknown mass and scalar potential. The original mechanical inverse, with its sharper elementary bounds, remains in Section 11. The contact time is not identified with ordinary elapsed time of the unsuspended discrete system.

### D. Robustness reaches the retained geometric output

Definition 13.1 specifies the raw-launch observation model. Proposition 13.2 includes exact branch classification and entry rarity in acceptance probabilities, without double-counting entry mass when it is already present in the normalized raw source. Theorem 13.3 propagates approximate sharing through clock inversion, root solving, distance reconstruction, registration and blending. It adds a controlled linear bias term to the finite-record geometric radius while retaining an actual smooth, strictly convex, disjoint periodic output on the stated high-probability event.

## 2. Responses to the major comments

| Comment | Revision and precise extent of the answer |
|---|---|
| **R78-M1: equivalence with actions does not establish a deep statistical contribution** | The exact equivalence is retained, not denied. Sections 4–5 now treat arbitrary observations, specify the ambient quotient, prove a split model geometry, give model validation and prove two-sided action risk under misspecification. Section 10 supplies a second substantive inverse on a larger generating class. These are new results to assess, not a claim that a change of title settles journal significance. |
| **R78-M2: the billiard experiment remains marked and reference-dependent** | The revised abstract, Theorem 1.2 and Definition 13.1 explicitly retain obstacle/lift/word labels, supplied scalar charts and cross-clock sharing. The whole-table conclusion and nonanalytic examples are not removed. Uniform geometric risk is stated only on bounded fixed-atlas neighborhoods with positive margins. We do **not** claim a universal unmarked billiard protocol. The class-wide fixed observation theorem is Theorem 10.3 for convex twist suspensions; it is an alternative substantive strengthening, not a relabeling of the billiard theorem as universal. |
| **R78-M3: the mechanical device thresholds the unknown action** | Proposition 10.2 derives an independently specified flow and its return clock. Theorem 10.3 implements the event by externally delayed launch, counting returns and comparing with fixed deadlines. The identity with an action threshold is a consequence proved in the analysis, not an instruction supplied to the observer. The contact suspension is part of the observed system. We make no claim that the original unsuspended mechanical system has the same ordinary time. |
| **R78-M4: the abstract theorem repackages difficult hypotheses** | Lemma 10.1 verifies those hypotheses from intrinsic global Hessian and twist inequalities for a whole class of arbitrary two-variable functions. The proof includes global inverse maps, coercive minimization, tridiagonal cofactors, explicit twist bounds and actual-prefix determinism. Theorem 10.3 supplies uniform endpoint, phase and clock bounds and reconstructs the full compact restriction of `L`. The older scalar abstraction is retained as the composition tool, not advertised as newly deep by itself. |
| **R78-M5: no robustness to nonshared weights** | Theorem 4.4 gives the `C^m` bias estimate and the complete exact ambiguity formula. Proposition 4.5 separates tangent action error from normal model error. Proposition 5.1 gives validation, including extra-clock residuals. Theorem 5.2 proves the sharp linear ambiguity floor, even with arbitrarily many records at the fixed clocks. Theorem 13.3 propagates the upper bound to geometry. |
| **R78-M6: insufficient literature comparison** | Section 1.2 and the bibliography now engage Bálint–De Simoi–Kaloshin–Leguil (2020), De Simoi–Kaloshin–Leguil (2023), Marsden–West, Hutchings, Giné–Nickl and Tsybakov, in addition to the four retained references. The introduction distinguishes exterior lens data, periodic marked-length data, local canonical graphs, variational composition, contact action roofs, distance certificates and statistical rates. It makes no unsupported ordering of the billiard data spaces and no novelty claim for the classical suspension or generic distance-geometry theory. |
| **R78-M7: overbroad headline scope** | The abstract now states compact-square recovery for the larger generating class and bounded fixed-atlas neighborhoods for the geometric theorem. Section 11 retains exact recovery of `P` on a prescribed interval, not the whole real line from one finite protocol. The distinction between whole-target uniqueness and reference-dependent uniform acquisition is repeated in the main theorem discussion. No theorem is deleted to conceal a mismatch. |
| **R78-M8: hidden branch-resolution cost** | Definition 13.1 starts with a raw normalized source, records failures, and requires exact classification or rejection—not erroneous labels. Proposition 13.2 includes classification efficiency in retained mass. If a source is normalized only after branch entry, the entry probability multiplies that mass; when the source is already raw it does not multiply it again. Theorem 13.3 uses an actual success floor, not one inferred from conditional laws alone. |
| **R78-M9: undefined quotient stability** | Proposition 4.1 defines the ambient quotient topology and complete anchored-log metric. Theorem 4.2 proves its explicit split charts. The old exact quotient theorem is retained with a corrected representative-level stability statement and a reference to the actual quotient topology. The two different claims are no longer conflated. |
| **R78-M10: every root must be an actual physical match** | Theorem 7.2 now requires single-valued regular physical branch actions on the entire indicated product domains, the same initial embedding and scalar coordinate, the same unit-speed outgoing half-plane, and the prescribed word/extension. It explicitly excludes arbitrary stationary-value continuations. Lemma 10.1 independently derives the analogous property for the new convex class. |

## 3. Responses to the minor comments

| Comment | Location and answer |
|---|---|
| **R78-m1: absolute action** | Section 1 and Proposition 3.2 distinguish `dW`, its canonical graph and the additive constant recovered by absolute clocks. Section 10 explains that changing the primitive's constant changes the return roof. |
| **R78-m2: identification versus validation** | Exact model identification remains in Section 3. Sections 4–5 define off-model contrasts and prove a separate residual criterion and test. A zero residual validates the weighted-action representation on its chart, not physical realizability as a billiard. |
| **R78-m3: two-clock ambiguity** | Proposition 3.3 and its following qualification remain active: the ambiguity is in the unrestricted weighted-function model, not an exhibited pair of noncongruent billiards. The new statistical lower bound has the same explicit scope. |
| **R78-m4: fixed protocol versus fixed nuisance** | Theorem 10.3 specifies which settings are class-fixed and permits unknown source and efficiency functions subject to within-count sharing. The proof even constructs an available class-fixed source; it does not assume that every admissible experiment uses that source. |
| **R78-m5: scalar atlas and gauge** | Section 1.1, Theorem 1.2 and Definition 13.1 identify supplied labels and overlap maps separately from unknown Euclidean positions, speeds, tangents, normals and the common isometry gauge. |
| **R78-m6: classical generating-function sources** | The related-work discussion cites the billiard rigidity and discrete variational sources. The elementary first-variation, twist and composition proofs remain self-contained in Sections 6–7. |
| **R78-m7: verification artifacts** | The verification record labels its tests as algebraic/numerical diagnostics, not proof certification. Their role is to catch normalization, contact-sign, matching and conditioning regressions. No acceptance claim is based on the number of checks. |
| **R78-m8: response and roadmap** | This response, `PROOF_LEDGER_V79.md`, `REVISION_V79.md`, the source-preservation manifest and the build audit provide the active logical delta and reproducibility entry points. |

## 4. Preservation, validation, and remaining distinctions

The new principal article is an addition to the exact reviewed source tree, not a replacement of old branches. The original twelve principal-source files were checked against their Git blob identities. An input-graph audit verifies retention of every original proof body, label and bibliography key. The old principal article also compiles from these exact preserved bytes.

The accompanying local build has 35 pages, no undefined references, duplicate labels or overfull boxes. All 35 pages were rendered; montages were visually inspected, with selected mathematical pages inspected separately. Twelve newly written finite diagnostic groups pass both normally and with `python -O`, with identical output. These facts establish specific source, build and regression properties, not mathematical correctness of all arguments.

One initial diagnostic used an unjustified universal bound of 100 on bias divided by perturbation size at relatively large perturbations. That check failed. It was replaced by a direct test of the explicitly differentiated inverse and first-order remainder contraction. The replacement is not a relaxed theorem: the theorem has always required a sufficiently small chart neighborhood and margin-dependent constants. The revised test reports the actual directional condition number and verifies first-order convergence rather than concealing conditioning in an arbitrary cutoff.

There is no claim here of a universal unmarked billiard observation operator, ordinary-time equivalence for the unsuspended mechanical map, optimal billiard geometric risk, detection of action-confounded nuisance, or independent journal acceptance. The positive reconstruction theorems remain the purpose of the paper. The exact ambiguity characterization is used to prove a matching statistical bound, not to replace the reconstruction programme by a negative conclusion.

Finally, the revision source is now materialized on the independent remote branch `revision/a2-v79-robust-clock-quotient-contact-suspension-2026-09-17`, based directly on the pinned controlling review commit. This publication is an add-only source revision and does not modify `main` or the separate existing v79 branch. Remote CI is not called successful unless a run completes, and the remote publication is not a claim of proof certification, journal acceptance, or journal submission.
