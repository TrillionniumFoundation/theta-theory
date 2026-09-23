# Response to the v17 referees — revision v18

We thank the referees for separating correctness, information conventions, and structural significance. The controlling report is the third independent report at `a94ec98d6e33d9719f72deec160f5c8270ce006f` (report blob `b1515103564c6c0de02b1751dad24ea23bee1f5f`). The pipeline report at `9f4787221c086e25f7d95b36e97aff870bd2b0c5` (blob `09646a80c6b6fc9f89a3e575d6e2dd2a832a200f`) is addressed as well. Both concern the frozen v17 submission `e5a81e26e9a1b366f5863b00e09d62512f32f5ea`. The earlier independent review is known through these reports and is not represented as a separate full original-text audit in this revision.

The revision adds an organizing theorem rather than claiming that a longer ledger answers the significance objection. The canonical article retains the complete comparison, nonlinear testing, revealed-behavior hierarchy, collision and posterior proofs that it uses. The remaining predecessor mathematics is preserved without changes in the complete development. None of the historical program targets is deleted. All new theorem claims remain subject to independent review.

## E17-R3.1 — Revealed behavior versus constrained tests

The inherited result is now titled **Revealed-behavior adaptive representation**. Its discussion explicitly says that compactness and continuity suffice and that a point mass minimizes its infinite-level measure formulation. We do not claim that this partition-of-unity identity is a new causal randomization theorem.

Theorem `thm:v18-audit` instead constrains the verifier to finitely many reset trials and a charged count register. The candidate law and private state are unavailable. Its dual integrates replicated laws for one fixed candidate over the original nonconvex image. The binary theorem `thm:v18-auditlower` proves that no Dirac measure minimizes this finite-data dual and that replacing it by its barycenter gives the wrong value. This is an operationally different theorem, not a relabeling of v17. Access to completed marks, resets, parameters/feedback rows, and independent validation is stated at the definition; it is not attributed to the online simulator.

## E17-R3.2 — A structural criterion and lower bounds

Theorem `thm:v18-continuation` gives a necessary and sufficient simultaneous shift-stable continuation-cover criterion with a prescribed width profile. Independent cutwise rank bounds alone are explicitly not sufficient. Theorem `thm:v18-cut` computes the exact erasure-cut spectrum `1 - sum(top K preparation masses)` for private, hidden-independent and visible-independent signatures. For an equiprobable m-bit message it implies the sharp retained-width requirement `K >= (1-epsilon) 2^m` at the cut.

Theorem `thm:v18-auditlower` gives the exact binary audit value and the uniform lower bound `delta-v_n >= 1/(16 sqrt(n))`. Together with `delta-v_n <= sqrt(D/n)`, this establishes the sharp sampling exponent for this reset information budget. It is not advertised as sharpness of the inherited revealed-polynomial degree bound, nor as a bit-complexity result. The lower-bound family is a compact restricted candidate class; it is not falsely identified with every unrestricted private-row image.

## E17-R3.3 — Exact chart input and output

Proposition `prop:v18-chart` starts with rational polynomial row data and rational affine event discrepancies. It computes the observable quotient dimension from the coefficient span after simplex equalities are eliminated, computes a rational quotient basis by Gaussian elimination, enumerates rational independent samples, and decides the squared determinant bound by a first-order real formula. Cramer's rule provides the bounded rational chart; explicit substitution provides the rational certificate pullback. Termination is proved by density and a strict half-maximum determinant margin. The dimension is computed, not assumed known. No unproved numerical maximum oracle or polynomial-time assertion is used.

## E17-R3.4 — One composition theorem

Theorem `thm:v18-microscopic` uses the exact marked scattering gap, the finite-reset audit theorem, the moving-collision estimate, the inherited TV-to-posterior inequality, and the new likelihood/entropic transport results. It constructs one rational rule with 2,800 training trials on the all-on eight-atom marked row. Uniformly over contact distance in `[9/10,11/10]`, its expected signed score is greater than `2/5` against every width-one private candidate. The target law is the physical law in validation, not an artificially substituted ideal law. The physical private/visible deficiency exceeds `9/20`, while a hidden two-selector implementation has deficiency less than `13/100`.

The same proof treats genuinely different microscopic collision times and trajectories. Lemma `lem:v18-movingcollision` gives

`eta^2 <= |d'-d| + 2700 |d'-d|^2`,

as well as a pathwise Skorokhod bound. These estimates give likelihood, projected likelihood, posterior and bounded entropic backward convergence in the same experiment. Because the source is blind, the *same* finite audit changes in expected score by at most `eta/(2 sigma)`, not by a reset-count-amplified error. The effective chart is used for the rational finite presentation/certificate part. The appendix supplies the canonical dependency diagram.

## E17-R3.5 — What the collision does

The main theorem and introduction state that B--W correlation is prepared, while collision transduces B into a nonzero transverse observed velocity. Neither correlation creation nor a many-particle memory principle is asserted. The model has two labeled spheres and a single nongrazing collision. The feedback is an acquisition gate, not a force. Contact-distance variation changes actual trajectories; it is not presented as kinetic scaling. The no-collision control is retained in the main theorem: at `d <= 2/5` the signal vanishes and every compared deficiency is zero.

## E17-R3.6 — Beyond the fixed-flow posterior statement

The inherited physical theorem is now titled **Fixed-flow observation-approximation limit**. The new Theorem `thm:v18-gaussian` permits different microscopic trajectories and even different phase spaces pulled back to a common preparation, with bounded Gaussian observation signals. It proves full and projected likelihood S2 estimates before identifying the projected stochastic exponential. Proposition `prop:v18-innovation`, Theorem `thm:v18-entropic`, and Corollary `cor:v18-stopping` give explicit downstream consumers. The physical theorem verifies their hypotheses by changing the hard-sphere contact distance.

This is a proved changing-path, likelihood, filtration, Girsanov and bounded entropic-backward result in the stated model. It does not infer arbitrary historical C2 response/rigidity conclusions or a zero-noise limit. The common preparation, bounded signals and positive noise are adjacent to the statements. The conditional maximal coupling remains a convergence device, not an executable simulator.

## E17-R3.7 — Theorem-status conflicts

`PROOF_STATUS.json` identifies the canonical statements by label and SHA-256 of the statement body and source file. `evidence/BOUND_PROOF_STATUS.json` binds new source identities to the actual source commit. `PIPELINE_GRAPH.json` preserves all eleven historical components while distinguishing source assertion, current proof credit, review state, supersession, and consumer edges. No Boolean called simply "closed" is used as program-wide mathematical authority.

The historical C2 optional-projection inference is explicitly replaced in the bounded Gaussian class by the new chain. The old full C2 conclusion is not an input. Example `ex:v18-fiditightness` shows why finite-dimensional convergence and maximal amplitude bounds alone do not establish Skorokhod tightness. It is a counterexample to that inference, not a claimed counterexample to every possible strengthened conditional-kernel hypothesis.

The B4 audit also identifies a concrete normalization issue: the displayed resolvent identity in `thm:r17-b4-nisio` fails on the constant-one payoff for its normalized discounted definition. Correcting a displayed identity is not sufficient to prove the downstream range and generator assertions. Those historical sources remain present and are marked as derivations requiring their own validation, not as completed inputs to this paper.

## E17-R3.8 — Actual downstream consumption

The C2 consumer now has an explicit proof chain: moving microscopic collision paths -> Gaussian likelihood S2 transport -> projected stochastic exponential and posterior transport -> bounded entropic backward equation and stopping values. The last applications use the marked-law estimates and are not a renamed version of the collision calculation. The changed-path hypotheses are discharged in the physical model.

We do not manufacture an A2 dependency. A2's primary geometric results remain independent, and neither the title nor the abstract asserts that all eleven analytic chains are consequences of one finite-state theorem. The program's general objective is retained; the new theorem supplies an actual C2 branch rather than claiming universal logical ancestry from repository ordering.

## E17-R3.9 — Norberg proof-level crosswalk

**Not represented as completed.** The original Norberg proof text was not obtained. The publisher PDF and national-library routes were tried; searchable secondary excerpts and catalog metadata do not establish the original operator class, all equivalences or its proof. `LITERATURE_COMPARISON.md` records the exact unresolved checklist, without claiming that Norberg lacks our theorem.

The new continuation theorem raised an additional close antecedent. We obtained and read Fliess's original 1975 paper, specifically Theorem 3.1 and its proof on pp. 8--9, and the stochastic specialization Theorem 5.4 and Corollary 2 on pp. 18--19. The paper explicitly credits the stable positive-cone mechanism. Our present theorem supplies finite controlled normalization and matched persistent-resource signatures; it is not claimed to invent positive realization. This comparison does not substitute for the separate Norberg audit.

## E17-R3.10 — A canonical theorem chain without deleting content

The new article contains only definitions and full proofs used in the principal comparison/transport architecture, plus the independent structural lower-bound branch. The old task, domain, presentation and physical modules remain in the unchanged 256-page predecessor development, attached after the new article. `PRESERVATION_MAP.json` identifies every v17 TeX file and whether it is reproduced canonically, qualified locally, or retained in the companion. All predecessor source paths and branch references remain unchanged. Historical proof labels and derivations are not silently removed merely to shorten the journal-facing article.

## E17-R3.11 — Novelty subtraction

The introduction and `PROOF_LEDGER.md` give, for each principal result, its classical mechanism, inherited GTF input, new statement and new consequence. Positive realization, minimax, Caratheodory, two-point testing, Bernstein approximation, elastic scattering, Girsanov and martingale inequalities are not claimed as discoveries. The organizing contribution offered for review is the proved information-budgeted chain and its explicit stable microscopic certificate, together with exact resource and sample obstructions.

## E17-R3.12 — Reproducibility is separate from proof

The build receipt records only operations actually executed. Exact arithmetic, negative controls, source hashes, resolved labels and a successful typesetting run are evidence about reproducibility and particular identities, not an independent analytic certification. Every new statement remains labeled as awaiting external review. The proof text, not the count of successful diagnostics, is the mathematical argument.

## Pipeline report E17-P1 through E17-P8

| Requirement | Disposition |
|---|---|
| P1: namespaced status for A1--D1 | `PIPELINE_GRAPH.json`, `PIPELINE_STATUS.md`, statement/source hashes; unreviewed historical assertions are not silently upgraded. |
| P2: old C2 optional supersession | Explicit scoped replacement by `thm:v18-gaussian`, `prop:v18-innovation`, `thm:v18-entropic`, `cor:v18-stopping`; no blanket credit for the old `thm:r17-c2-main`. |
| P3: actual foundational consumption | The new C2 Gaussian/entropic consumer uses the main microscopic chain; A2 is not made artificially dependent. |
| P4: unite the v17 modules | `thm:v18-microscopic`, with a fixed finite-data certificate and changing-trajectory process convergence. |
| P5: constrain the tester or rename | Both: revealed-behavior representation is accurately named; reset-audit information and memory are explicitly priced. |
| P6: lower bound/classification | Simultaneous continuation cover, exact erasure cut, and matching uniform sampling exponent. |
| P7: Norberg original | Still an unresolved priority audit; no negative or absolute priority claim is made. |
| P8: audit downstream closure sources | The cited B4/C2 Round-Seventeen files were read, concrete problematic steps identified, and their aggregate conclusions excluded from the proof inputs. |

The revision addresses the mathematical requirements constructively rather than equating compliance with acceptance. Whether the resulting structural theorem meets the requested journal's significance standard is a matter for the next independent referee, not a conclusion of this response.
