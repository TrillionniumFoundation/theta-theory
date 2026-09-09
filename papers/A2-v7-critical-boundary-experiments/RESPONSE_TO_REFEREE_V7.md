# A2 v7: response to the independent v6 referee report

**Manuscript:** Relative boundary laws and statistical reconstruction in periodic dispersing billiards.  
**Author:** Qian Qi.  
**Revision date:** September 9, 2026.  
**New manuscript directory:** `papers/A2-v7-critical-boundary-experiments/`.  
**Controlling report:** `reviews/a2-v6-relative-transfer-harsh-independent-2026-09-09/REFEREE_REPORT.md` at `f1728f5d96ea01b1326daf9a6a36352b2e270be1`.  
**Reviewed author baseline:** `4ca186258c92dcbc75accc4eb576e307cc612189`, manuscript tree `50f7fdb275a23d7a74234f4e1347c4934be8b8b8`.

The revision preserves the entire previous repository and clones the complete v6 manuscript tree into a new directory. All previously active mathematical chapters and the independent two-collision companion remain active. The only changes to inherited active TeX files are the article's abstract and input list, an additional introductory paragraph, and the two table packages. No previous proof chapter is replaced by a summary. New arguments appear in the five `v7/` files.

We understand the report's distinction between mathematical correctness and editorial significance. It reports no identified fatal defect in the principal chains it audited, closes the previous concrete objections, and nevertheless withholds a top-four recommendation. We do not reinterpret that recommendation as a theorem that the work is false or impossible. Conversely, completion of the requests below is not an acceptance certificate. This revision answers them through committed theorem statements and proofs, while leaving the venue judgment to renewed independent review.

## V6-R1 — one observation and asymptotic statement

**Response:** Section 1.6 and Table 1, source `v7/00_scope.tex`, separate five experiments: long-bridge endpoint/residual comparison; fixed-order contact-coefficient inversion; fixed-J count acquisition from a supplied shrinking bracket; count acquisition from a fixed local bracket; and odd-flight selected-position acquisition. Each row states the observations, supplied information, unknown quantities, varying parameters, error topology, preparation cost, and variables in which the constants are uniform.

In particular, conditional successes and raw preparations are not interchangeable; the former have expected cost proportional to the inverse rare-event mass. Position observations do not give the count-only cube-root rate for free. The full embedded growing collision array retains bounded-Lipschitz control, not total variation. Fixed-order inverse uniformity in flight number is not uniformity in the number of recovered jets. The fixed local family in the acquisition theorem supplies uniform design bounds, not the unknown table itself.

The added paragraph near the beginning of the original introduction places the one-flight identifiability fact and the fixed-J nature of amplitude acquisition alongside the motivation for the long-bridge theorem, rather than relegating them to a final caveat.

## V6-R2 — statistical content with correct quantifiers

**Response:** We adopt the report's two useful benchmarks, supply their proofs in the manuscript, and explicitly acknowledge their origin. Their roles are separated from the extensions below.

### Support overlap and the actual physical joint limit

`thm:v7-exact-tv` (Theorem 7.1; `v7/10_critical_experiments.tex`) extends the quadratic overlap calculation to unequal facing curvatures and both parities. The finite and boundary Hessians have the common factorization `H_j = D M_j D`, `H_boundary = D^2`; whitening is applied to both laws. Their exact conditional total variation is

`delta_j = (2/pi) arcsin(exp(-j gamma))`.

The theorem proves the exact nonidentical-product formulas, restores the common failure atom, and constructs both directions of a hypothesis-independent randomization to an erasure experiment. This equivalence is for a specified simple binary pair at a fixed table. Its reverse kernel is not advertised as a simulator for an unknown table.

`lem:v7-tangent` (Lemma 7.2) proves uniform tangent approximation in the same topology before taking any growing-sample limit. The conditional error is `O(sqrt(d))`, improving to `O(d)` when both contact graphs are even, without requiring them to be identical. The raw error retains the factor `p0 = d^2/[2A sinh(j gamma)]`. The proof uses uniformly coercive supports, Taylor bounds, and residual intervals sharing a lower endpoint.

`thm:v7-critical` (Theorem 7.3) then establishes the joint limit for actual nonlinear positive-offset physical laws. For conditional records, `k exp(-j gamma) -> b` and `k sqrt(d) -> 0` give total variation `1-exp(-2b/pi)`. For raw preparations the conditions are `n p0 exp(-j gamma) -> b` and `n p0 sqrt(d) -> 0`. The minimum equal-prior testing error tends to `exp(-2b/pi)/2`. Explicit nonempty choices of offsets and a nonidentical triangular-schedule version are proved. The even-graph improvement is stated with its own assumptions.

These conditions prevent an unjustified interchange of the small-offset and growing-sample limits. They do not prove that the nonlinear fixed-offset rate tau is optimal, or replace linear accumulation by a Gaussian square-root rule. At fixed positive offset the original nonlinear relative transfer theorem remains the applicable statement.

### Physical count indistinguishability

`lem:v7-cubic` and `thm:v7-lower` (Lemma 20.1 and Theorem 20.2; `v7/30_count_lower_bounds.tex`) use rotation invariance of the actual support-function family at fixed `R=1/4`, not just an amplitude surrogate. The normalized finite-offset count probabilities have bounded third parameter derivatives; the invariant first derivative vanishes. The two physical alternatives have probability difference `O(d^2 s^3)` and matching curvature separation comparable to `|s|`.

The proof derives the Bernoulli divergence estimate, adds divergences along predetermined or stopped adaptive queries, and gives the two-point testing argument with its metric and confidence conventions. It yields a weighted-exposure bound and, for all-history offsets `d_i <= L_m h`, the preparation lower bound `c h^-2 epsilon^-6`. The matching fixed-m power is restricted to bounded-flight Bernoulli queries in the shrinking collar. No global all-schedule minimax conclusion, or exponent six obtained by sending m to infinity, is stated.

## V6-R3 — importance of the relative mechanism

**Response:** The significance case now concerns a specific statement which genuinely varies both bridge length and experimental sample size. Sections 1.6 and 7 explain why a positive endpoint Hessian or separate fixed-flight expansions cannot provide relative control of the exponentially small mixed derivative. That missing scale enters the prepared raw experiment as well as the successful conditional law.

The new critical profile identifies a support-driven testing transition in an explicit regime of actual physical experiments. At that scale the number of successes is of order `exp(j gamma)`, while the number of raw preparations is of order `d^-2 exp(2j gamma)`. The erasure interpretation follows from common and exclusive support, not from an asserted central limit theorem. Unequal contacts and both parities remain included. The joint limit is not represented as a new global billiard rigidity theorem.

The finite inverse consequences are retained with their proper independent roles. In addition, the acquisition side is strengthened rather than reduced: `lem:v7-bracket` and `thm:v7-fixed-bracket` (Lemma 21.1 and Theorem 21.2; `v7/40_fixed_bracket_acquisition.tex`) acquire the previously supplied shrinking bracket from a fixed local gap interval. A binary count search is proved to have an all-history deterministic cost. Every later waiting time is capped; failure of the search therefore cannot cause an infinite waiting cost. The same fixed-m upper order is obtained including coarse search, fine calibration, and amplitude estimation.

This stronger acquisition theorem still uses a specified local physical family and noiseless recording. Its preliminary queries may use wider offsets, so the shrinking-collar lower bound is not repurposed as a global optimality theorem for the enlarged design. The count theorem is not claimed to require long bridges.

## V6-R4 — measurable estimators and reproducibility

**Response:** `lem:v7-selection` (Lemma 8.1; `v7/20_measurable_reconstruction.tex`) supplies a specific Borel exact minimizing selection. Ordered finite closed-ball covers of a compact parameter set give nested nonempty compact sets of minimizers; their unique limiting point is Borel. The feasibility tests are Borel because minima over fixed compact subsets equal infima over fixed countable dense subsets. This convention applies to all subsequent compact discrepancy fits. The polynomial root-or-zero pilot rule is separately shown to be Borel, including degenerate coefficients and endpoint roots. Computational efficiency is not inferred from existence.

The article does not contain diagnostic counts as evidence for a theorem. `PROOF_LEDGER_V7.md` records dependencies and scope; `SOURCE_PINS_V7.json` records immutable input identities; `VERIFICATION_V7.json` records observed runs and hashes. `tools-v7/build.py` builds in an empty auxiliary state, companion first. The local result is a 72-page article and a 7-page companion, with no unresolved references or overfull boxes. Harmless engine font-expansion notices and an underfull vertical box are reported rather than silently renamed a warning-free build.

Executed finite diagnostics are separated: the new v7 script passes 134 checks (98 exact and 36 ordinary floating); the unchanged controlling referee script passes 190 (162 exact and 28 ordinary floating); the unchanged v6 author script passes 147 (112 exact and 35 ordinary floating). Each was run normally and with `python -O`; each pair of outputs is byte-identical in the recorded environment. The scripts use explicit exceptions. These are local executions, not remote CI, interval arithmetic, global billiard simulation, or formal proof certification. The PDFs were also rendered and inspected for layout; that inspection does not certify the mathematics.

## Historical derivations and retained results

The revision uses the committed v3 geometric localization, Jacobi reduction, trace-norm flux, and physical integration; the v4 half-line determinant and nonlinear law; the v5 differentiated operators, contact jets, coalescing inverse, and calibration; and the five v6 source chapters. Their active source bytes were checked against the frozen GitHub objects before revision. The Library source packet omitted the inactive `v5/00_introduction.tex`; we did not mistake that omission for a full-tree match. The new GitHub manuscript is built on the complete remote v6 tree, so that inactive file and the rest of the historical material are preserved as well.

The earlier v5 reports at `9975aa037d5d9eb1f339b9220f9cd21fb54c0876` and `0421836a5868967f90093281c7ca43aab9815a0d` remain source-pinned historical context. The latest report's resolved issues are not reopened by reverting to an earlier branch. Arbitrary-itinerary dynamics, global noise-stable analytic continuation, and global minimax reconstruction are not substituted for the actual requests. The original broad smooth forward assumptions, actual/effective-curvature distinction, horizontal-channel realization, finite-flight inverses, all coalescence strata, record response, circular appendix, and two-collision companion remain intact.
