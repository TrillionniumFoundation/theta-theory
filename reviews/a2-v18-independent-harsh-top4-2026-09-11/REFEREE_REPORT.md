# Independent harsh referee-style report on A2 v18

**Manuscript:** Qian Qi, *Boundary laws, information loss, and two-contact rigidity in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society  
**Author revision branch:** `revision/a2-v18-integrated-boundary-information-2026-09-11`  
**Immutable author head reviewed:** `af5ef2f67a0e2d8313191bfc3bc53b253fa46b79`  
**Immediate predecessor:** `revision/a2-v17-boundary-information-coarsening-2026-09-11`, base head `106836283ebe3fabee0479df8976d24f6dbe0bf6`  
**Previous referee report used only as historical context:** `reviews/a2-v17-independent-harsh-boundary-information-2026-09-11/REFEREE_REPORT.md`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any of the journals named above. I distinguish mathematical correctness, novelty/significance, exposition/architecture, and submission readiness. I do not treat finite diagnostics, source manifests, proof ledgers, response letters, or an unexecuted CI workflow as proof certificates.

## 1. Recommendation to the editor

**Recommendation: reject at the requested four-journal level.**

I would not recommend acceptance, conditional acceptance, or a routine major revision carrying an implied route to acceptance at this level.

The v18 revision is materially better organized than v17. It fixes the concrete quantifier defect in the boundary-information theorem, gives the nonlinear relative law an explicit formal front-matter statement, separates the known one-dimensional nonregular moving-support phenomenon from the claims actually made here, and makes the observation-coarsening mechanism much easier to identify. The revised title and introduction are substantially more coherent.

I nevertheless do not think v18 crosses the decisive significance threshold for Annals/Acta/Inventiones/JAMS. The statistical addition is a legitimate theorem, but its logarithmic mechanism is a multidimensional/coarea realization of the classical linearly vanishing moving-boundary regime; the billiard specialization is an exact determinant-one whitening and a sharp comparison of three coarsenings of a **fixed-table finite-versus-boundary simple experiment**. The strongest geometric conclusion still stops at a function-valued symmetrized boundary invariant in the general smooth case, while the independent-contact finite-jet inverse uses additional evenness and supplied leading geometry. This is serious mathematics, but in my judgment it does not amount to a conceptual advance of the breadth, depth, or rigidity strength normally required to reverse the preceding four-journal-level rejection.

A harsh report should not manufacture a proof failure merely because the editorial recommendation is negative. **I did not find a fatal mathematical error in the newly revised v18 boundary-information/endpoint-critical core under its printed hypotheses.** The previously identified `b=+infinity` scope defect is correctly repaired. The Hellinger coefficient, the `I_Sigma=1` billiard computation, the conversion from `zeta_j` to `q_j`, and the Gaussian total-variation constants are mutually consistent. The negative recommendation is therefore primarily a significance-and-submission judgment, accompanied by several real but nonfatal readiness and notation defects described below.

## 2. Scope of this review

I audited the v17-to-v18 diff and the active v18 entry point, then traced the main theorem dependencies through the core retained modules. In particular I inspected:

- `main.tex` and the new `article/01_introduction_v18.tex`;
- the new formal setup `article/01c_geometric_setup_v18.tex`;
- `v3/10_geometry_action.tex` and `v3/20_integration.tex` for the Jacobi reduction, cofactor identity, full-phase flux and common Morse domain;
- `v4/10_boundary_layers.tex` for the half-line actions/amplitudes, trace-class factorization and fixed-offset law;
- `article/16_hyperbolic_coordinates.tex` for the intrinsic scalar transport and the equality between the physical half-line determinant amplitude and the normalized scalar linearizing density;
- the revised `article/18_boundary_information_v18.tex`;
- `article/19_endpoint_critical.tex` and the retained `v7/10_critical_experiments.tex` for the exact tangent experiments and positive-offset transfer;
- `RESPONSE_TO_REFEREE_V18.md`, `PROOF_LEDGER_V18.md`, `HISTORICAL_DERIVATION_AUDIT_V18.md`, `LITERATURE_VERIFICATION_V18.md`, and `VERIFICATION_V18.json` as author-supplied audit records, without treating those records as proofs;
- the root and manuscript-directory README files and the v18 GitHub Actions evidence.

The v18 revision deliberately retains the older theorem modules rather than rewriting the entire manuscript. I therefore treated previously unchanged chains as retained claims and spot-checked the central dependencies that v18 promotes. I did not re-prove every auxiliary acquisition/minimax appendix from first principles in this round. That limitation should be read together with the fact that those appendices remain active in the submitted `main.tex`.

I also independently checked the publisher-level literature positioning for the classical nonregular-support mechanism. Richard L. Smith's 1985 Biometrika paper explicitly states that the linearly vanishing (`alpha=2`) moving-endpoint case is asymptotically normal at a different rate; Hirano--Porter (Econometrica 2003) explicitly studies parameter-dependent support through limits of experiments and local asymptotic minimax ideas. I did not find, in the search performed for this review, a source that obviously contains the manuscript's exact multidimensional hypersurface coefficient plus this billiard realization. That is not the same as an exhaustive priority search.

## 3. What v18 genuinely improves

### 3.1 The previous mathematical scope defect is closed

The v17 theorem grammatically exposed support-exclusive negligibility to the `b=+infinity` regime although its proof only established `np t^2 -> 0` at finite information scale. V18 now states the scopes separately:

- the total-variation transition is asserted for `b in [0,+infinity]`;
- the Gaussian log-likelihood limit is asserted for `0<b<+infinity`;
- support-exclusive observations are asserted negligible only for `b<+infinity`;
- the supercritical `TV -> 1` conclusion is proved through multiplicative Hellinger affinity without assuming `np t^2 -> 0`.

This is the correct repair. I regard C17-M1 as closed.

### 3.2 The formal theorem graph is clearer

The new `article/01c_geometric_setup_v18.tex` is useful. It places the general periodic dispersing-billiard geometry, unequal contact curvatures, multiplier conventions, the half-line quantities, and the principal relative boundary law in one place. The theorem now makes explicit the fixed endpoint box, the nonshrinking physical offset collar, the relative twist normalization, mixed geometric/offset derivatives, and the conditional endpoint--residual law.

This is a presentational improvement, not a new proof. The proof still lives in the historical modules. That is acceptable mathematically, but relevant to the architecture objection below.

### 3.3 The revised novelty statement is more responsible

The introduction no longer suggests that nonregular normality or the existence of a logarithmically modified endpoint rate is itself new. The manuscript now isolates the claims as:

1. an intrinsic regular-hypersurface coefficient;
2. an independently thinned simple-experiment law retaining the failure atom;
3. determinant-one billiard whitening giving coefficient one across unequal curvatures/parities;
4. the resulting three-level observation hierarchy.

This is much better positioning than the earlier broad significance language.

## 4. Mathematical audit of the promoted core

### 4.1 Nonlinear relative boundary law

The core Jacobi reduction is internally consistent. With `c=sqrt(c_0 c_1)` and `gamma=arcosh(c)`, the alternating quadratic recurrence is reduced to the constant-coefficient hyperbolic recurrence, and the endpoint Hessian gives

`d_j^0 / sqrt(det H_j) = csch(j gamma)`.

The nonlinear bridge lemma avoids division by this exponentially small twist: it controls the bridge in weighted endpoint spaces, uses a cofactor identity

`-W_uv = product(edge twists) / det(H_int)`,

and normalizes before passing to logarithms. The trace-norm argument is the right mechanism for avoiding a spurious factor proportional to the number of collisions.

The half-line construction and the two-end gluing argument also appear mathematically coherent. In particular, the determinant comparison is localized to trace-class perturbations near the two endpoints; the finite Green matrix converges to the direct sum of the two half-line Green operators after removing the remote-boundary reflections; fixed parameter derivatives only introduce polynomial factors that can be absorbed into a strict exponential margin.

The fixed-offset law uses a common Morse map rather than differentiating a moving sharp boundary formally. After radialization, odd Taylor terms cancel and the normalized residual-time integral has a smooth right extension to `d=0`. I did not find a contradiction in the claimed smooth `C^k` extension or in the value `F_p(0)=1`.

This is, in my view, the strongest mathematical part of the paper.

### 4.2 Intrinsic determinant/scalar transport

The retained smooth scalar-transport theorem is conceptually useful and the proof route is appropriate. The finite Schur concatenation yields an exact one-flight cocycle for the limiting amplitudes; integrating that cocycle produces normalized scalar linearizing coordinates on the physical stable branches. The manuscript correctly avoids claiming that the classical existence of a one-dimensional linearizing coordinate itself proves the nonlinear finite-bridge theorem.

The distinction between the analytic two-dimensional normal-form comparison and the smooth physical half-line construction is also stated carefully. I found no new v18 defect in this portion.

### 4.3 Logarithmic boundary information

For `f_t=a_t(w_t)_+` with a regular moving hypersurface, the displayed coefficient

`I_Sigma = integral_Sigma a_0 v^2 / |grad w_0| d sigma`

is the correct coefficient generated by the `v/w_0` singularity of the score. The coarea estimate gives a logarithmic second moment, while the collar mass is quadratic. The proof's choice `h=C|t|` for Hellinger and `h=|t| log(1/|t|)^(1/4)` for the finite-critical likelihood expansion is appropriate.

The triangular-array CLT bookkeeping is also consistent at the displayed scale. At finite information scale, `np t^2 -> 0`; the omitted collar and support-exclusive events are therefore negligible, the truncated score satisfies Lindeberg because the largest normalized summand is `O(log(1/|t|)^(-1/4))`, and the quadratic score term concentrates. The limiting null log likelihood

`N(-I_Sigma b/2, I_Sigma b)`

and the resulting total-variation profile are consistent.

For `b=0` and `b=+infinity`, the multiplicative Hellinger-affinity argument is sufficient and does not require support exclusivity to vanish. This is exactly where v18 improves the v17 wording.

### 4.4 Exact billiard endpoint experiment

The endpoint calculation is clean. After common whitening, the finite tangent endpoint density is

`(2/pi)(1-exp(-zeta)x_1^2-exp(zeta)x_2^2)_+`.

The determinant-one coordinate change proves normalization. At `zeta=0`, the normal velocity is `x_1^2-x_2^2`, and the boundary integral on the unit circle gives `I_Sigma=1`. Since

`zeta_j = 2 q_j + O(q_j^3)`, `q_j=exp(-j gamma)`,

the Hellinger distance satisfies

`H^2 = q_j^2 log(1/q_j) + O(q_j^2)`.

The conversion of the general theorem to the endpoint testing profile is therefore correct: if `k_j r_j -> b`, `r_j=q_j^2 log(1/q_j)`, then the Gaussian variance parameter is `4b`, and the displayed limit `2 Phi(sqrt(b))-1` follows.

The positive-offset transfer is also logically sound in its printed, very narrow regime. The condition `omega(d_j)=o(r_j)` makes the accumulated tangent approximation negligible at the endpoint-critical scale; the supercritical case is handled by projecting to a fixed critical subsample rather than incorrectly requiring the approximation error to vanish over the entire supercritical sample.

### 4.5 What this audit does *not* establish

The absence of a fatal defect in the promoted core is not a global machine proof of the roughly sixty-input manuscript. The active entry point still includes a large historical collection of inverse, acquisition, calibration, adaptive, minimax, and comparison modules. Many have been reviewed in prior rounds, but v18 itself does not newly re-prove all of them. This matters because the manuscript continues to present them as part of one active article rather than as an external companion library.

## 5. Decisive four-journal objections

### C18-E1 — the significance objection remains open

The revision improves the *statement* of significance but not enough, in my judgment, the underlying level of the main advance.

The new general statistical theorem packages a classical nonregular mechanism in a useful multidimensional form. Smith's 1985 result already identifies the linearly vanishing moving-endpoint case as a nonstandard-rate asymptotically normal regime. Hirano--Porter place parameter-dependent support within limits-of-experiments and efficiency theory. The manuscript's regular-hypersurface coefficient and thinning formulation are legitimate additions, but the proof is a local tubular/coarea reduction followed by a truncated-score triangular-array CLT and Hellinger affinity. This is elegant and correct; it is not a new foundational principle of nonregular asymptotics.

The billiard specialization is sharper than a generic application because the determinant-one whitening makes the coefficient exactly one and because the same physical model exhibits three different comparison scales under coarsening. Still, the central statistical comparison is between the finite bridge and its boundary model for the **same fixed table**. It is a sharp theorem about validity/model comparison under observation coarsening, not a theorem that estimates or reconstructs an unknown smooth billiard table at the new scale.

The general smooth geometric result determines a symmetrized function-valued boundary invariant. The manuscript explicitly acknowledges that a general asymmetric contact is not reconstructed from that width/profile. The independent-contact jet inverse requires individually even contacts and supplied labelled leading geometry. The two-flight benchmark already recovers finite jets in that restricted setting. Thus v18 does not turn the paper into an unrestricted rigidity theorem.

For a specialist dynamics/statistical-inverse journal, the combination may be compelling. At the requested four-journal level, I still do not see a single conclusion whose conceptual reach dominates the existing rigidity and nonregular-statistics landscapes strongly enough.

### C18-E2 — the observation hierarchy is sharp but intrinsically a simple known-table comparison

The three-level hierarchy is one of the paper's best results:

- complete endpoint--residual records separate at the `q_j` scale;
- endpoints without residual time separate at the `q_j^2 log(1/q_j)` scale;
- the tangent success bit is exactly uninformative.

But this theorem compares two known simple laws, and the common whitening is allowed to depend on the fixed table. The manuscript is commendably explicit about that. Consequently the theorem does **not** establish an implementable unknown-table decision rule at the same scale, a local asymptotic equivalence theorem for a smooth family of billiards, a semiparametric information bound for unknown geometry, or a sharp minimax inverse theorem.

This is a correctness strength—no overclaim is hidden—but an editorial limitation. The statistical theorem explains how one approximation loses information; it does not yet solve the harder inverse problem suggested by the word “rigidity” in the title.

### C18-E3 — the dossier architecture is only narratively, not structurally, repaired

The v18 title, abstract and introduction are markedly better. However the active `main.tex` still includes roughly sixty direct source modules. The author audit explicitly says that no historical theorem module is deleted. The revision therefore changes the order in which the reader is told to value the results, but not the mathematical object being submitted.

The paper still simultaneously contains:

1. nonlinear long-bridge relative laws;
2. determinant/scalar transport;
3. profile/Volterra/Abel inversion;
4. even-contact finite-jet rigidity;
5. two-flight reconstruction;
6. profile acquisition and calibration;
7. adaptive and stopped experiments;
8. complete-record erasure limits;
9. endpoint nonregular Gaussian limits;
10. supercritical, minimax and comparison appendices.

Length alone is not the objection. The problem is that several of these are logically downstream and editorially independent research directions, while the top-four case is supposed to be carried by a small number of dominant ideas. Keeping every historical consequence active makes the source graph look like an accumulating research dossier rather than a final article whose proof architecture has been optimized around its main theorem.

The new front theorem improves navigability but does not close this objection.

### C18-E4 — the novelty audit remains expressly non-exhaustive

`LITERATURE_VERIFICATION_V18.md` explicitly says that it is “not a claim to have exhaustively searched all nonregular statistics literature.” That is an honest and appropriate disclaimer for a working revision, but it is weak evidence for a four-journal originality claim centered on a general statistical theorem.

The revised references to Akahira, Ibragimov--Has'minskii, Smith, and Hirano--Porter are useful. They establish that the authors understand the classical mechanism and are no longer claiming the `alpha=2` rate itself. What remains to be justified at the requested level is whether the exact hypersurface Hellinger coefficient / thinning formulation is genuinely absent from the broader asymptotic-statistics literature, not merely absent from four checked references.

I do not assert prior art that I have not found. I instead regard the present novelty verification as incomplete relative to the editorial burden created by the generality of the claim.

## 6. Concrete mathematical/expository defects

### C18-M1 — `lambda` is reused for two incompatible objects in the same formal setup

In `article/01c_geometric_setup_v18.tex`, an oriented lattice pair is written

`e=(a,b,lambda)`

where `lambda` is a lattice translation vector. A few paragraphs later, in the same formal setup, the local multiplier convention defines

`lambda = varrho^2 = exp(-2 gamma)`.

The same symbol therefore denotes both a lattice vector and a positive scalar hyperbolic multiplier. Because subsequent formulas use channel indices and multipliers simultaneously, this is more than a stylistic annoyance. Rename one of them (for example use `ell` or `nu` for the lattice translate and reserve `lambda` for the multiplier).

This is a minor mathematical notation defect, not a failure of the theorem.

### C18-M2 — the new principal theorem should distinguish more explicitly between fixed-offset geometric derivatives and fixed physical-time derivatives

The v18 setup says `t=j g_e+d` and then declares that offset derivatives hold `d` fixed as an independent coordinate. Thus a geometric derivative at fixed `d` moves the physical observation time with the channel threshold. That is a legitimate and useful centered coordinate, and it is what the proof controls. But a reader can easily interpret “mixed geometric and offset derivatives of the exact selected-channel probabilities” as derivatives at fixed physical `t`.

The theorem should state in one sentence that all geometric derivatives in the normalized law are taken in the channel-centered coordinates `(xi,d)` with `t=j g_e(xi)+d`, unless a later statement explicitly returns to fixed physical time. This does not appear to invalidate the proof; it prevents a stronger interpretation than the argument establishes.

## 7. Submission-readiness blockers

### C18-R1 — no successful complete native build is established

The new workflow is well designed in principle: it checks out the exact source, preserves an archive, installs a native TeX toolchain, builds the original companion before the main article, runs the boundary diagnostics in ordinary and optimized Python modes, and records PDF hashes on success.

But the latest v18 workflow run on the reviewed head is GitHub Actions run `34573957731`, and it completed with conclusion `failure` before any step executed. Its only job has:

- `steps: []`;
- `runner_id: 0`;
- empty runner name;
- a lifetime of only a few seconds.

This is not evidence of a LaTeX failure. It is equally not evidence of a successful full build. `VERIFICATION_V18.json` correctly records the status as not yet verified. Therefore the reproducibility blocker from the previous round remains open.

A submission containing this many active inputs should not be represented as final until an actual companion-first/full-main build has completed on the immutable source and unresolved references, duplicate labels, missing inputs and citation failures have been checked in the executed environment.

### C18-R2 — the repository discovery pointers have regressed to v17

On the v18 revision branch, the root `README.md` still says:

`Latest A2 author revision: v17 — boundary information and observation coarsening`

and still links the v17 response, proof ledger and verification record. The manuscript-directory `README.md` likewise identifies itself as A2 v17, points to the v17 branch, and calls `article/18_boundary_information.tex` the new core proof rather than the active v18 replacement.

This is a direct submission-navigation regression. A reader entering the v18 branch through the repository's advertised index is sent to stale metadata.

Before any renewed submission, both discovery pointers should identify v18, the reviewed immutable source, the active v18 response/proof-ledger/verification files, and the actual build status.

### C18-R3 — version provenance is unnecessarily confusing

The v18 manuscript lives inside the directory named `A2-v17-boundary-information-coarsening`, while both v17 and v18 versions of the front matter and boundary-information source coexist there. Provenance preservation is valuable, but the active submission package should have an unambiguous version manifest. At minimum the README/build map should enumerate which files are active and which are historical; ideally the submission artifact should be generated into a clean v18 source package containing only the active dependency closure plus intentionally included historical appendices.

This is not a mathematical objection, but it matters for external refereeing and archival reproducibility.

## 8. Status of the v17 objections after v18

| Previous item | v18 assessment |
| --- | --- |
| C17-M1: support-exclusive statement exposed to `b=+infinity` | **Closed.** The theorem now scopes it to finite information and uses Hellinger affinity for the supercritical TV conclusion. |
| C17-E1: significance / genuine novelty | **Improved in wording; still open and decisive.** The revision states the contribution more responsibly, but I still judge it below the requested four-journal threshold. |
| C17-E2: moving-support literature positioning | **Substantially improved, but the priority audit remains non-exhaustive.** No false broad priority claim is made. |
| C17-E3: accumulating dossier / contribution hierarchy | **Partially improved, not closed.** The front matter is much better; the active source graph remains essentially the full historical dossier. |
| C17-R1: complete native build | **Open.** The v18 run again failed before a runner executed any step. |
| Earlier stale root discovery pointer | **Regressed.** The v18 branch root and manuscript README still advertise v17 as current. |
| Fatal new v18 core correctness error | **None established in this audit.** |

## 9. What would materially change my assessment

A further revision would need more than another auxiliary theorem or another response document. The changes that would materially affect the four-journal evaluation are conceptual:

1. **Strengthen the central geometric theorem.** For example, remove a major symmetry/supplied-geometry restriction from the independent-contact inverse, or obtain a genuinely stronger rigidity statement from the near-onset probability data rather than another calibration consequence.
2. **Upgrade the statistical result from fixed simple-model comparison to an unknown-geometry experiment.** A local asymptotic experiment, efficient information bound, or sharp minimax theorem for a nontrivial smooth billiard family would substantially change the role of the endpoint information calculation.
3. **Produce a genuinely comprehensive novelty audit** for the multidimensional moving-support theorem before using it as a principal significance pillar.
4. **Refactor the submission around the dominant theorem chain.** The historical modules may remain in the repository, but a final article should make clear which results are main, which are indispensable lemmas, and which belong in companions.
5. **Close the mechanical readiness blockers:** successful full native build, correct v18 navigation, clean active-source manifest, and the small notation/coordinate clarifications above.

Items 4--5 alone would make the paper easier to referee but would not reverse my current significance judgment. Items 1--2 are the sort of mathematical strengthening that could.

## 10. Final editorial assessment

V18 is a real improvement over v17. The authors have responded correctly to the one concrete statement-level error, stopped overclaiming the classical moving-boundary phenomenon, and made the geometry-to-information mechanism visible. The principal relative law remains technically interesting, and the endpoint observation hierarchy is sharp within its stated experiment.

But the question at the requested level is not whether the paper contains correct and sophisticated mathematics; it clearly does. The question is whether the final theorem package has the singular conceptual force expected of the four journals named above. My answer remains **no**. The new statistical theorem refines the interpretation of the boundary law rather than transforming the underlying rigidity problem, and the manuscript still carries a very large accumulation of downstream modules whose presence does not compensate for that gap.

**Final recommendation: reject at Annals/Acta/Inventiones/JAMS level.**

I would view a substantially refocused version as potentially strong for a specialist journal in dynamical systems, mathematical physics, inverse problems, or asymptotic statistics, depending on which theorem chain is made primary. That is not a statement that the current mathematics should be discarded; it is a judgment about the level and shape of the present submission.