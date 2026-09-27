# Response to referee r32 — General Theta Foundations I, revision 51

**Title:** Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width  
**Author:** Qian Qi  
**Date:** 27 September 2026  
**Controlling review:** `ca5efb0e6e50c1deb267f8b6f98551ff56197890`, branch `review/general-theta-foundations-i-v50-compatible-simplex-harsh-top4-r32-2026-09-27`.  
**Reviewed publication:** `2024b419eab2e6e6d34a21c9bec2a18b6afb6222`; validated mathematical source `ee887bf04d8265cfbc23e4b4693dd1a8645a7505`.

We thank the referee for distinguishing the substantive rank-tight result from the claims that it did not yet establish. We have addressed that distinction by adding proofs, rather than presenting the same theorem under a narrower ambition. The revision develops arbitrary-width reachable sections, a finite-group criterion for uniformly bounded clocked width, a one-surplus occupation theorem giving an eventual exact six-state frontier in dimension three, and an explicit stability bound giving a horizon-independent positive-error four-state frontier in dimension two. The full two-state, orthogonal-example, arithmetic and finite-bit mathematical material is retained. The analytic obligations of the other papers are neither deleted nor credited to these finite-dimensional arguments.

This response refers to stable LaTeX labels. The executed build supplies `evidence/THEOREM_LOCATIONS.json`, mapping labels to the theorem numbers and pages of the actual PDF. Build checks and exact finite regressions are reproducibility evidence; the proofs remain subject to independent mathematical review.

## 1. The new theorem chain

### 1.1 Reachability rank, not an unjustified projection of hidden states

Theorem `thm:section51` takes the actual reachable row span R_t, intersects it with the probability simplex, and only then applies the actual identity-suffix mean map. It proves all command identities on R_t, the positive section inclusions, the physical response constraints, and the vertex bound binomial(K_t, r_t−1). The affine observation kernel has dimension r_t−D−1. This states precisely which directions are unobservable and which ambient directions are not in the reachable span.

At width D+2, Corollary `cor:surplus51` distinguishes the two ranks: full reachability gives a polytope with at most D+2 vertices and a one-dimensional observation kernel; rank D+1 gives an affine-isomorphic D-dimensional section with at most D+2 facets. The old rank-tight simplex case is recovered, not assumed for the enlarged class.

The reachable-section idea and a fixed-section stochastic-extension alternative were already present in revision 33 and have classical positive-realization antecedents. We have restored and strengthened that material rather than claiming it as a new invention. The rank-sensitive count, projector characterization and subsequent occupation and stability conclusions are the additions in this revision.

### 1.2 Arbitrary profiles and all-width finite-group rigidity

Theorem `thm:local51` gives a necessary and sufficient finite polynomial system using orthogonal projectors, bounded mean matrices and stochastic transitions. It has degree at most three and a number of variables polynomial in the explicitly listed horizon, alphabet, dimension and profile. Necessity uses the actual reachable spaces; sufficiency is proved by induction with a legal decoder on every available state. For algebraic input this is a finite real-algebraic decision and synthesis statement. It is not a polynomial-time optimizer, and no implementation of a general elimination engine is claimed.

Theorem `thm:occupation51` applies to any selected cuts of width at most K, not just rank-tight cuts. It uses a compact family of physical polytopes with at most binomial(K, floor(K/2)) vertices and a variational expansion multiplier. If the command group is infinite, the multiplier is strictly greater than one; every fixed width can occur at only a bounded number of cuts, even with arbitrarily wide intermediate registers.

Theorem `thm:finitegroup51` proves that bounded exact clocked width over all horizons is equivalent to a finite orthogonal command group and to existence of a single finite permutation machine. The clocked machines may be independently chosen at every horizon. A uniform bound K gives a stationary machine with at most binomial(K, floor(K/2)) labels, not necessarily K. Conversely a finite group gives an orbit machine with at most 2D|G| labels. This is an all-width theorem; it does not assert the exact optimum at each finite horizon.

Corollary `cor:rational51` specializes the result to a fixed planar rational rotation R=((3,−4),(4,3))/5 and a reflection F, with alphabet {I,R,F}. The commands do not commute, R has infinite order, and W_N tends to infinity at fixed dimension and alphabet. The rational infinite-order observation itself is elementary and the commuting rotation already appeared in the historical pipeline. The broader controlled classification and arbitrary-width occupation statement are what is used here.

### 1.3 One surplus label and an exact six-state result

Theorem `thm:surplus-budget51` goes beyond the old simplex obstruction even for a finite group. For D≥3, a centrally symmetric full-dimensional polytope needs at least 2D vertices and 2D facets. The two possible width-D+2 geometries therefore cannot be centrally symmetric. Compactness, using polarity for the facet-bounded class, gives a strict variational antipodal volume gap beta_D(rho)>1. Selected cuts of width at most D+2 satisfy beta_D(rho)^(m−1)≤D! rho^(−D).

For D=3 and any signed-permutation alphabet containing I and −I, this excludes peak five at all sufficiently large horizons. The six signed coordinate states give the matching exact realization, so W_N,0=6 eventually. The threshold is given by beta_3(rho)^N>6 rho^(−3). We do not assign an unproved numerical value to beta_3 or call this the sharp first horizon. The statement is exact, not an asserted noisy six-state theorem.

### 1.4 Explicit approximate rank-tight occupation

Lemma `lem:anchor51` constructs an affine anchor matrix from the prescribed signed seeds. A Neumann-series estimate bounds its inverse by explicit expressions in D, rho and the mean error delta=2 epsilon. It recovers every hidden suffix row without dividing by an uncontrolled individual state probability. The estimate applies to a whole suffix, rather than accumulating one approximation error per command.

Theorem `thm:robust51` gives

`(c_D / Lambda^D)^(m−1) ≤ D! (rho−D delta)^(−D)`,

where `c_D=2^(−D) binomial(2D,D)` and

`Lambda = 1 + 2D(D+1)(1+sqrt(D)) delta / ((rho−2D delta)(rho−D delta))`,

for `0≤delta<rho/(2D)`. The m rank-tight cuts can include both endpoints; other cuts have arbitrary finite widths.

Corollary `cor:robust-four51` consequently proves that planar signed-permutation alphabets containing I and −I have W_N,epsilon=4 when

`epsilon≤rho^2/2000` and `(512/363)^N>2(500/499)^2 rho^(−2)`.

For rho=1/10 this holds for every N≥16 and epsilon≤1/200000. The interval does not shrink with N. These are explicit sufficient constants, not a claim that the old exact threshold N=14 is sharp or that the noise interval is maximal. The old fixed-horizon compactness threshold remains a separate, weaker conclusion.

## 2. Responses to the eight major revision requests in Section 10

| Request | Response and location |
|---|---|
| 10.1 State the precise range instead of treating minimal rank as all widths | The introduction states signed spanning seeds, all coordinate queries, identity command and the clocked resource. `thm:section51`, `thm:local51`, `thm:occupation51` and `thm:finitegroup51` now genuinely cover arbitrary widths. Exact, rank-tight and approximate assumptions remain separately visible. |
| 10.2 Focus the article rather than accumulating an archive | The controlling narrative now runs from reachable sections to all-width rigidity and stability, then to the exact finite certificates. The arithmetic, word-profile, metric and finite-bit results are retained with proofs in appendices. We have not removed mathematical results or substituted a specialist-venue recommendation for a mathematical response. The enlarged article is not represented as shorter in total pages. |
| 10.3 Replace the purely qualitative positive-error assertion by quantitative stability | `lem:anchor51`, `thm:robust51`, and `cor:robust-four51` supply explicit conditioning, approximate containment, occupation and error/horizon constants. |
| 10.4 Handle surplus states rather than only the simplex case | `cor:surplus51` identifies the two width-D+2 geometries. `thm:surplus-budget51` proves a new occupation bound and an eventual exact six-state frontier. The arbitrary-profile projector system and all-width group theorem address the broader setting without asserting a solved sharp optimizer. |
| 10.5 Give a fixed-dimensional long-horizon noncommutative family | `cor:rational51` fixes D=2 and three rational commands while N tends to infinity. The three-epoch nine-dimensional example is retained for its different purpose; the exponential full-table embedding is not used as the long-horizon result. |
| 10.6 Supply conventional, theorem-level comparison with primary literature | `sec:resources51` compares BF03 Example 4/Theorem 2, BF04 Theorem 2, static extension complexity, KKKR rank-one completion, Gillis–Shitov fixed-sign feasibility/hardness, and the 2026 Nie–Tang–Zhou local noisy-completion theorem. Repository genealogy is kept in the history audit rather than used as priority clearance. |
| 10.7 Separate five algorithmic/resource modes in the paper | The table in `sec:resources51` distinguishes atomic-row existence, real-algebraic synthesis, rational description, finite-bit implementation and uniform computation/sampling. It also separates the new local formula from a general implemented optimizer. |
| 10.8 State the actual interface with the analytic pipeline | The closing paragraph of `sec:resources51` states the independent analytic obligations. `HISTORY_AUDIT.md` and `PIPELINE_STATUS.json` preserve the dependency distinctions; no A2, B4, C2 or eleven-paper analytic closure is inferred. |

## 3. Thirty local requests

| No. | Resolution |
|---|---|
| 1 | The signed spanning seed set, all queries and identity command are stated before the structural summary and again in each relevant section. |
| 2 | Rank-tight is defined once in the introduction as available width D+1; the distinction from ordinary rank is explicit. |
| 3 | Ordinary residual rank is not called positive or stochastic rank. The new local criterion supplies the additional positivity and transition constraints. |
| 4 | The simplex proof records that each binary outcome pair has sum one, so every row-space combination has coefficient sum one. |
| 5 | Full column rank of E_t excludes an available state that is unreachable from every prefix at a rank-tight cut. At larger widths, such states remain counted and the new theorem restricts identities to R_t. |
| 6 | New transition indices consistently use T_(t+1,a) for a map from cut t to cut t+1. |
| 7 | All endpoint volume calculations use vol(C_rho)=(2 rho)^D/D!. |
| 8 | Between separated cuts the word containing one −I is explicitly padded by identities. |
| 9 | The definition of m explicitly includes the initial and terminal command cuts when they have the selected width. |
| 10 | N≥14 remains a sufficient exact bound, not a claimed first four-state horizon. The new N≥16 is likewise a sufficient robust bound. |
| 11 | The retained compactness threshold is written eta_N(A,rho), not as a universal N-only constant. |
| 12 | The planar classification distinguishes one reflection from a half-turn; two distinct allowed reflections must have product of order three in the triangular case. |
| 13 | The old simplex proof distinguishes diagonal extraction over horizons from the later vertex extraction along one nested chain. The new all-width proof instead uses an attained variational minimum. |
| 14 | Strict volume monotonicity is justified for full-dimensional compact convex bodies; degeneration is excluded by the enclosed crosspolytope. |
| 15 | The separation theorem's parameter a is identified as an inradius parameter rather than a command letter. |
| 16 | The regular simplex in the separation proof is contained in the unit ball and has the required inradius. |
| 17 | The orthogonal-example flattening comparison is stated for nontrivial matricizations. |
| 18 | Scaled mean and binary-TV errors are both given. In the nine-dimensional example the flattening values are 40 rho/357 and 20 rho/357, respectively. |
| 19 | The ninth orthogonal coordinate is fixed and is not queried. |
| 20 | Rational nonattainment uses the fact that a finite maximum of rational row errors is rational. |
| 21 | The embedding's bound on cF is justified by 2|F|≤1+F^2≤1+sum F^2. |
| 22 | The dimension 2^n+1 is explicit and is not described as a polynomial-size succinct encoding. |
| 23 | Circuit-record bounds exclude input, sign coverage, basis data and isolating intervals; these are identified as additional costs. |
| 24 | Sign assignments are distinguished from the possibly fewer induced sign patterns. |
| 25 | The certificate and common-field estimates are described as coarse bounds. |
| 26 | Radical powers always designate the positive real roots where magnitudes are reconstructed. |
| 27 | Radical description length is not equated with the degree or bit cost of a full number-field representation. |
| 28 | Exact finite tests, optimized-Python agreement and clean builds are not treated as universal mathematical proof. |
| 29 | Internal revision citations in the active exposition are replaced by local proof references or appropriate classical antecedents; provenance remains in the history audit. |
| 30 | The controlling exposition is reorganized and historical process discussion is moved outside the article. Mathematical proofs are preserved in the integrated article and appendices; no claim of a reduced total page count is made. |

## 4. Preservation, verification, and the remaining distinctions

The preparation step verifies the frozen v50 source-hash manifest before copying its mathematical modules. `PRESERVATION_MANIFEST.json` lists source and revised hashes and every edited copied file. `EXPECTED_V50.json` records the labels from the actually loaded v50 source graph. The build traverses the actual v51 input graph, rather than counting labels in unloaded archives, and rejects a lost original label. Original repository paths and branches are unchanged.

The new rational checker exercises both surplus-rank geometries, a globally unreachable state on which ambient intertwining fails, six-state signed-permutation machines, the rational noncommuting rotation, anchor conditioning, the quarter-extension defect and the explicit robust constants. Negative controls reject invalid projectors, illegal stochastic rows, illegal means, false ambient projection and invalid error/horizon certificates. All inherited checkers run in normal and optimized Python. The PDF receives three TeX passes, reference and layout checks, page rendering, and an isolated core-source rebuild with equal page text and rasters. Actual executions, not this plan, are recorded in `evidence/BUILD_RECEIPT.json`.

The new results answer the requested mathematical directions, but several distinctions remain essential. The variational all-width and six-state constants are not closed-form optimal rates. The local cubic formula is not an implemented general optimizer. The noisy occupation theorem is not an arbitrary-width noisy finite-group classification. The two-state global certificate is not a convex dual over all higher-width lifts. No exhaustive priority clearance or journal acceptance is asserted. These qualifications keep the enlarged theorems precise; they do not replace the paper with a no-go statement or remove its conclusions.
