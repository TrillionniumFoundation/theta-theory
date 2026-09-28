# Response to the independent referee on A2 v84

## Version and scope

The report answered here is `reviews/a2-v84-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md` at commit `372f5235c3fad2c5a9734bb7649261de207dbf1b`. Its reviewed manuscript is v84 at `b3da64f38742459620d624ea9a565abb3550aba9`. The new branch starts from the review commit, so both the reviewed source and the controlling report remain in its ancestry.

The manuscript for renewed review is **`rigidity_v85.tex`**, titled *Action rigidity from selective observations*. `rigidity_v85_full.tex` has the identical principal body followed by every companion input retained in the v84 expanded edition. It is background, not a competing principal submission. The original v84 and historical source files have not been overwritten or removed. The introduction has been rewritten in `article/v85/01_rigidity.tex`; its sharp action statements and proofs are retained. The other original principal modules are included unchanged.

The revision responds by proving two further results at the level requested in the report: a finite structural classification in the rational-derivative category, and an integrated finite noisy geometric theorem. It also gives a sharp statistical theorem for geometrically realizable finite-dimensional priors and charges unsuccessful raw attempts. The claims are stated with their actual geometric, apparatus, and statistical hypotheses; the existing positive exact results are not replaced by weaker ones.

## Major comments

### M1. An intrinsic classification, rather than only a quotient embedding criterion

**New results:** Theorem `thm:v85-polar`, Corollary `cor:v85-maximal`, and Theorem `thm:v85-budget`, in `article/v85/07_polar_structure.tex`.

For a detector space containing constants with rational derivatives, let E be its derivative space in partial-fraction coordinates. Exact action separation is equivalent to exclusion from E of a finite set of integer residue vectors with zero total charge and positive charge at most two. Regular inversion additionally excludes nonzero intersections with the double-pole coordinate spaces supported on at most two action poles. The proof establishes both directions, including a common-anchor realization of every charge-one obstruction. Thus the test contains no unknown moving action coordinates.

Within a fixed ambient divisor class and under principal-part closure, the manuscript classifies all maximal admissible spaces: every safe principal part and polynomial direction is included; action double-pole directions are excluded; at most one action simple-pole direction is included. This closure assumption is explicit. For nonsaturated spaces the full finite membership tests, rather than a pole-count shortcut, apply. The theorem is a classification of the stated broad rational-derivative category, not a classification of all analytic function spaces.

### M2. Generic analytic experiments and their predecessors

The sufficient generic `d+5` theorem is retained, with its precise collision and normalized-tangent dimensions. The manuscript now compares its proof principle directly with Sontag's analytic experiment-count theory and Alberti--Santacesaria's finite-measurement stability framework. It no longer asks the reader to regard incidence dimension counting as the principal innovation. No sharpness or quantitative random-design conditioning is inferred from an almost-everywhere statement. The new structural classification and pole budget answer a different question: which detector subspaces are admissible before a design is selected?

### M3. A common property behind the rational examples

The pole budget uses two invariants of the derivative space: the degree of its least common denominator and its maximal order at infinity. The proof treats secants and tangents by the same numerator estimate. It recovers the protected-logarithm bound and the six-clock sign-changing example, with the latter's improved count arising from cancellation of total residue at infinity. The action-divisor argument is explained through the same integer-residue mechanism. The sharper polynomial interval argument and the exponential positive-kernel example are retained with their additional structure; they are not inaccurately identified as rational-derivative cases.

### M4. Finite records, supplied margins, and an implementable certificate

**New results:** Theorem `thm:v85-confidence` and Proposition `prop:v85-grid`, in `article/v85/08_confidence_sets.tex`.

The forward parameter class is a displayed closed compact polytope, including singular channels. The confidence sets are formed by intersecting that forward class with observed matrix residual bounds. Their action extrema give simultaneous confidence intervals without supplying a channel-rank floor, inverse modulus, or spectral separation constant to the procedure. A finite parameter grid, a displayed forward Lipschitz constant, and explicit padding yield a terminating finite search with the same coverage guarantee.

On true regular subsets the intervals contract at the usual square-root rate. The rank lower bound indexes this rate theorem but is not an input to the confidence construction. At singular channels coverage remains valid and the intervals can be wide. The two-arm architecture, degree bound, and coarse physical bounds remain supplied information. The new theorem does not claim unrestricted model-order selection.

For the earlier covering theorem, `eq:v85-closed-covering-class` and `eq:v85-C0` make its compact class and global inverse modulus explicit. They are not represented as data-estimated quantities.

### M5. A finite noisy geometric theorem with a variable reference

**New result:** Theorem `thm:v85-geometric`, in `article/v85/09_finite_geometry.tex`.

At finitely many boundary pairs, unknown two-arm projective readouts produce action confidence intervals. Both channels, every relative detector coefficient, and the bounded reference delay may vary independently between sampled pairs. The propagation action is selected by the known apparatus ordering. The largest observed interval width, plus a deterministic boundary-mesh interpolation term, bounds the full boundary-distance error. Stefanov--Uhlmann's stated local stability theorem then gives a C2 metric bound after a boundary-fixing pullback. The proof requires no interpolation of nuisance fields and no component covering.

The geometry class is stated before the theorem, including the regularity bound, proximity to a simple s-injective reference metric, and the exact imported estimate. The broader exact continuum theorem for all simple surfaces and a constant reference arm remains unchanged. These are complementary results, not a substitution of a local noisy claim for the original global exact theorem.

### M6. Common return lifts and observed domains

The exact compatibility theorem and the maximal word-evaluation domain recursion are preserved. Their roles are stated accurately in the new introduction: they certify full lifts on the observed invariant domain, including primitive constants. They do not turn a small commutator residual into an exact root or infer an unobserved invariant domain. The principal new finite geometric theorem does not require this group lemma: it proceeds directly through boundary distances. Thus the new geometric conclusion is not made conditional on an unproved approximate-root step.

### M7. A connected mathematical argument

The central finite-observation chain is now explicit:

`finite records -> compact action confidence sets -> finite boundary-distance constraints -> uniform distance error -> C2 metric error modulo boundary-fixing diffeomorphisms`.

The sharpness argument uses the same scalar fibre in the reverse direction: a one-parameter scaling family of actual simple metrics is hidden at `q+2` clocks by a variable reference delay and an interpolated detector polynomial. At `q+3` clocks this ambiguity disappears. The observation quotient therefore governs both the positive geometric theorem and its clock threshold. Covering and exact-return results are retained for the distinct multiple-sheet regime, rather than introduced as assumptions for the two-arm geometric argument.

### M8. Closest literature and exact attribution

The added references include Sontag; Alberti--Santacesaria; Ling--Strohmer; Nguyen--Zhang; Stefanov--Uhlmann; and Tsybakov. Comparisons appear at the relevant results, not only in a bibliography. The paper distinguishes analytic experiment counting, stable finite measurements, bilinear self-calibration, noisy pairwise permutation synchronization, and boundary-distance stability from its own observation model. The geometric stability estimate is attributed to the precise theorem used. The existing references for observable operators, Chebyshev systems, divided differences, Prony maps, covering spaces, exact symplectic lifts, and global simple-surface rigidity remain.

### M9. Join statistics to geometry and identify the loss

Theorem `thm:v85-geometric` gives a C2 pullback error from finitely many noisy acquisitions. Corollary `cor:v85-budget-rate` translates spatial resolution and per-cell sample size into a total readout budget. For surfaces it gives the sufficient exponent `mu/4`; it does not label this nonparametric exponent minimax.

Theorem `thm:v85-parametric-risk` separately proves matching `N^{-1}` mean squared parameter risk on a finite-dimensional geometric family. Its upper bound uses a finite boundary design whose differential is a nonsingular ray-transform matrix. Its lower bound fixes admissible nuisance parameters and varies actual metrics; it does not perturb an arbitrary unrealizable action field.

Theorem `thm:v85-raw` then extends confidence to fixed raw-attempt budgets with an observed failure symbol. It uses the actual retained counts at each cell, remains valid without a supplied success floor, and gives a raw-budget rate on classes with positive actual acceptance. Missed detections, late arrivals and rejected readings are charged in that budget.

### M10. Mathematical scale of the revision

The additional main statements are a finite polar classification with maximal admissible enlargements, a finite noisy metric confidence theorem, a geometrically realizable parametric risk theorem, and a sharp geometric clock threshold. They are not another isolated detector example or a claim based on compilation and simulation. The algebraic checks accompanying the revision only guard signs and finite constructions; the mathematical arguments are in the manuscript. Suitability for the requested journals remains an independent mathematical and editorial judgment.

## Technical comments

| Item | Location and action |
|---|---|
| T1 | Section `sec:v85-polar` explicitly fixes the Euclidean norm on action pairs. |
| T2 | The same section records positive separation of compact action classes from the diagonal and clock singularities. |
| T3 | The analytic comparison records collision dimension `d+4` and normalized-tangent dimension `d+3`, including nuisance and action coordinates. |
| T4 | Generic incidence and quantitative conditioning are distinguished; no condition number is inferred from a null exceptional set. |
| T5 | Equation `eq:v85-closed-covering-class` displays the closed bounded class with all rank, mass, action, coefficient and signature inequalities. |
| T6 | Equation `eq:v85-C0` states the global compact inverse modulus. It is not data-estimated; the new confidence theorem does not require it as input. |
| T7 | Independence within each cell is explicit. The union bounds do not require cross-cell independence. The parametric lower-bound experiment separately assumes independent cells. |
| T8 | Section `sec:v85-raw` explains that edge permutations and triangular-face relations specify monodromy on the two-skeleton, hence the covering of the whole triangulated domain. |
| T9 | The original simple-surface theorem remains a continuum theorem. The new theorem separately specifies a finite boundary mesh. |
| T10 | Metric error is written as `g' - psi^*g`, with `psi` fixing the boundary; equality of coordinate tensors is not substituted for the gauge. |
| T11 | The finite boundary experiment uses pointwise ordered actions and does not require covering recovery. |
| T12 | The known two-arm architecture, coarse delay separation and degree bound are displayed. Unknown reference values and channel coefficients remain unknown. |
| T13 | Exact polar identities and compact conditioning are separated. Fixed-pole and clock-collision margins enter constants only where their class requires them. |
| T14 | `rigidity_v85.tex` is the sole principal submission; `rigidity_v85_full.tex` shares its exact principal body and retains background. |
| T15 | Theorem-level predecessor comparisons have been added in the introduction and the structural, confidence, and geometric sections. |

## Historical material used

The revision uses the v84 complete scalar fibre, compact inverse and spectral matching, mesh-covering, observed-domain and simple-surface developments. It also revisits the v79 sharp action-risk and raw-preparation-cost derivations, especially the distinction between retained records and raw attempts, and preserves the earlier v77--v82 companion inputs. Their apparatus and regularity hypotheses have not been imported silently into the new two-arm experiment.
