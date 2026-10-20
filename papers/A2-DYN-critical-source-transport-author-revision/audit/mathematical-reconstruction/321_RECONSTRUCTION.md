# Native module 321: mathematical reconstruction and inequality audit

## Completed result and precise scope

The new proof body is `321_all_class_transversal_capacity.tex`. Every new label begins literally with `tc:`. This is an author proof contribution, not a referee report and not a replacement for the original scientific target.

For each original radius (R\in[9/20,47/100]) and each finite physical collision count (N\ge1), it partitions actual backward-regular states by their **complete normalized lifted past word and the original homogeneity labels at times (-1,\ldots,-N)**. A class includes all its disconnected components. The fixed disjoint assignment of artificial strip boundaries is retained, so boundary-only classes are also included. There is no homogeneity label at time zero in this class definition.

For each class (C), the weight is the supremum of the original true stable **Euclidean ((s,\varphi)) arclength** cocycle, evaluated from time (-N) to time zero. Its geometric capacity is the angle measure of the class's actual outgoing directions, on the physical direction circle of circumference (2\pi). The main result proves a uniform, pointwise bound on the sum of weights of **every class meeting each such direction fiber**, and therefore a uniform bound on the sum of weight times capacity over all classes. It also proves a uniform unweighted bound for classes with any prescribed positive capacity, including classes containing a prescribed length of a genuine unstable cone arc.

This is stronger than the predecessor's pairwise comparison and discharges a long-class summation/assignment obligation without assuming planar connectedness, stable convexity, a finite test chosen to cross every cell, or continuation through a singular wall. It does not prove a positive lower capacity for every class, the whole unweighted physical-word pressure, a conditioned roof density bound, the original normalized positive-source limit, the raw pointwise local limit theorem, or final four-coordinate inversion.

## Source identity and inherited dependencies

The complete native predecessor used here is:

- Repository: `https://github.com/TrillionniumFoundation/theta-theory`.
- Complete source directory: `papers/A2-DYN-marked-boundary-source-author-revision`.
- Commit label supplied and fixed for this reconstruction: `6cdd9ae88cd358d524ecb89092361ac1522ba351`.
- The exact SHA-256 of each read native dependency, the new proof body, and the checker is recorded in `execution/normal.json`. Identical hashes are in `execution/optimized.json`.

| Native source | Exact role in the new proof | Additional hypothesis introduced here |
| --- | --- | --- |
| 266, `input:v112-geometric-pressure` | Original physical-word supremum and original arclength convention | None; its unproved whole-pressure bound is not used |
| 281, `eq:uc-second`, `thm:uc-curvature` | Exact first-image graph curvature, including arbitrarily small initial incidence | None; the new affine source has curvature zero and the admissible cone slope |
| 282, `lem:uc-central`, `thm:uc-expansion`, `eq:uc-adapted` | Uniform physical first-hit complexity and target-homogeneity inverse-Jacobian sum | The extension to an initially nonhomogeneous graph is proved by checking the literal native hypotheses |
| 283, `thm:uc-growth` | Subsequent homogeneous curve inverse-growth sum with common (C_g) | None; this is applied only after one genuine collision and the fixed subdivision |
| 287, `thm:eh-horizon`, `cor:eh-counts` | Explicit uniform finite geometry; optional exact admissibility check for a finite (k_0) | No new radius or horizon assumption |
| 313, `thm:eo-optical` | The original ((\alpha,p)) optical multiplier with its terminal incidence and factor (30000) | None; this is a consequence, not a pressure premise |
| 318, `cor:xd-backward-curves` | Comparison of arbitrary stable-cone tangents on the same complete physical word and past strips, across disconnected physical components | None; no connecting physical path or two-dimensional cell-shape premise is inserted |

The new source does not rewrite any of those complete proof bodies. Parent integration is responsible for preserving predecessor sources and recording the final combined source tree and commit.

## Reconstruction of each nontrivial new step

### 1. Intrinsic physical direction and exact metric

The outgoing direction is 

\[
\pi_R(s,\varphi)=s/R+\varphi\pmod{2\pi}.
\]

This is a globally defined physical angle because increasing the lifted arclength by the exact circumference (2\pi R) increases the displayed angle by exactly (2\pi). It does not deform the lattice or the disk, alter an orbit, change the clock, or substitute a symbolic map.

At fixed direction, (ds/d\varphi=-R). Hence (d\ell=\sqrt{1+R^2}\,|d\varphi|), and the complete fiber has exact length (\pi\sqrt{1+R^2}). The lifted horizontal span is (\pi R), strictly less than one full circumference. Thus the fiber is injective and includes the current coordinate seam as an ordinary interior point. This avoids both dropping seam states and counting periodic copies twice. Its slope is exactly (-1/R), allowed on the boundary of the native stable cone; its curvature is zero.

### 2. Why the first step does not require current homogeneity

An entire direction fiber meets infinitely many current homogeneity strips. Splitting first at all of them would introduce an unjustified infinite sum of source costs. The proof instead first restricts to finitely many short affine windows and applies one actual backward collision to each window.

After the isometric time reversal, these are affine positive graphs of slope (1/R). The relevant arguments in 282 use only the cone slope bounds, short length, finite physical candidate set, and strict positive-foot monotonicity. The initial-grazing limiting argument is already included in `lem:uc-central`. Neither this argument nor the adapted expansion uses a lower bound for the initial incidence or the initial homogeneity index. The exact curvature formula in 281 likewise applies to this initial affine graph before homogeneity has been imposed. Homogeneity is required at the **target**, which is time (-1) in the original direction of time.

The resulting maximal first-image sum is at most (\Gamma\theta_*) in Euclidean arclength. The metric comparison is paid once. Every homogeneous image graph satisfies

\[
d\ell\le\sqrt{1+a^{-2}}\,|d\varphi|,
\qquad a=100/47,
\]

so its length is at most (S_{\rm im}=\pi\sqrt{1+a^{-2}}). The finite fixed subdivision factor (N_{\rm im}=1+\lceil2S_{\rm im}/\ell_*\rceil) suffices to make every first image an element of the inherited homogeneous class. Only then are the remaining (N-1) collisions estimated by 283. The chain rule gives the exact order and budget (C_g N_{\rm im}\Gamma\theta_*). Neither (Gamma) nor (C_g) is raised to (N).

### 3. Finite regularity, countable coverage, and actual endpoints

On each short initial window, the finite physical first-hit cuts and countable target-strip cuts leave countably many regular image pieces. Each regular restriction is injective. After any finite number of steps, the set of removed source points is countable, so coverage is full in curve arclength. This is proved on the actual test curve; bulk nullity is not used as a substitute.

The proof separately verifies local finiteness at every state with a finite regular past. On a small neighborhood of such a state, all finitely many past iterates are smooth, all relevant collision angles stay away from true grazing, and only finitely many homogeneity levels are possible. Cone invariance makes their crossings transverse. Fixed length subdivisions are locally finite because their interior cuts have positive separation in image arclength. A removed regular point is therefore adjacent to a genuine one-sided open curve piece. Its finite Jacobian extends to that endpoint with the actual derivative value.

True grazing states remain outside the original stable derivative domain. No assertion is made that their trace charge, the endpoints in a different pairing construction, or a boundary term in the physical roof problem has vanished.

### 4. All classes and the factor three

For one short test window choose **one** representative for each class that meets it. Different connected intersections of the same class are not counted repeatedly. A representative in an open growth interval is charged to that interval. The interval has one fixed word/strip tuple, so only one distinct interior class can be charged there.

A representative on an assigned artificial strip face is charged to a one-sided adjacent growth interval. Each interval has at most two endpoints; each endpoint belongs to one class under the disjoint convention. Hence a growth interval receives at most its one interior class and two endpoint classes. The multiplicity is at most three. Classes consisting entirely of regular strip-face points are retained in this argument.

For a class supremum point (y\in M_R'), true stable invariance gives

\[
j_N(T_R^{-N}y)=\frac1{J_{E^s(y)}T_R^{-N}(y)}.
\]

Native 318 compares this backward derivative with the test tangent at the chosen representative. Its strip hypotheses hold at exactly (-1,\ldots,-N). Taking reciprocals therefore gives (d_N(C)\le C_\times/J_WT_R^{-N}(p_C)). At a regular endpoint, the latter equals the corresponding one-sided curve limit. No true stable field continuity on the entire test or future regularity of (p_C) is needed. This is why a test need not meet (M_R') in positive curve length.

### 5. Measurability and the full positive sum

There is a finite physical one-flight alphabet and a countable homogeneity alphabet. A finite tuple therefore gives countably many classes. The current center is fixed to the actual origin; the whole past lift is then unique. Classes merge arbitrary disconnected domains with the same tuple.

The fixed horizontal strip intervals, with the original assigned endpoints, are countable unions of closed sets. On a regular physical-word domain the finite past iterates are continuous. A compact exhaustion therefore expresses each class as a countable union of compact sets. Its projection onto the physical direction circle is a countable union of compact sets and thus Borel, even for a boundary-only class.

Each complete fiber has a uniformly finite cover by short overlapping affine windows. The pointwise positive sum over every class meeting that fiber is at most

\[
K_{\rm tc}=3N_{\rm aff}C_\times C_{\rm aff}.
\]

Tonelli applies to the actual countable nonnegative sum. The parameter circle has length exactly (2\pi), so the complete capacity moment is at most (2\pi K_{\rm tc}). This is a pointwise bound before integration, not an average dynamical limit.

### 6. Long unstable arcs and no wrap loss

For a genuine connected unstable cone arc with (v=d\varphi/ds\in[\kappa_R,U]),

\[
\frac{d\vartheta_{\rm lift}}{d\ell}
=\frac{v+\kappa_R}{\sqrt{1+v^2}}
\ge\frac{2a}{\sqrt{1+U^2}}=\beta_{\rm tc}>0.
\]

The inequality uses (v\ge\kappa_R\ge a) and (v\le U) separately, with no missing normalization. In addition (d\vartheta_{\rm lift}=(1+\kappa_R/v)d\varphi\le2d\varphi). The real collision angle has range length (pi), so the lifted outgoing-angle variation is at most (2\pi). The image loses no measure when projected to the direction circle. Thus an arc of length at least (delta) gives capacity at least (eta_{\rm tc}\delta). There is no inferred long arc from an unproved diameter or convexity property.

### 7. Original pressure and optical factors

Forward-to-backward relabeling sends ((0,O_1,\ldots,O_N)) to ((0,O_{N-1}-O_N,\ldots,-O_N)). It is an involution after current-center normalization and is invariant under an arbitrary lattice translation of the record. Therefore the original (P_N(R)) is exactly the sum over physical words of the supremum of the refining class weights. Artificial strip boundary values are included directly; no density or continuity approximation is needed for this equality.

The remaining upper bound at fixed capacity threshold (delta>0) is `tc:remaining-pressure-interface`. Its unresolved part is a sum over physical words of the supremum over their **small-capacity** classes. A uniform bound for this specific positive sum would suffice for the original physical-word pressure along this route. It is weaker than requiring a uniform sum over every homogeneous refinement, and is not asserted here.

Native 313 gives (omega_N(x)\in[30000^{-1},30000],c(T_R^Nx)j_N(x)). The induced class comparison uses the precise ratio (omega_N(T_R^{-N}y)/c(y)). No optical factor is silently discarded. The arclength and outgoing-angle calculations contain no (1/(4\pi R)), (1/c_*), roof interval width, or (N^{-2}). Those factors stay at their original probability and conditioning interfaces.

A fixed exact Borel observation event may restrict the points in a class supremum, which only decreases a positive upper bound. That does not permit duplicating a class for each extra label and summing all those suprema, and does not produce a uniform microscopic roof density. The original radius range, time direction, collision clock, section event, exact return/displacement/collision information, roof intervals, and order of limits are unchanged.

## Primary literature verification and citation correction

### Demers–Zhang

Primary PDF: <https://arxiv.org/pdf/1210.1261>, *A functional analytic approach to perturbations of the Lorentz gas*. The inspected file has 45 pages, arXiv `1210.1261v1`, and SHA-256 `f20938fe161c0b4acd775bcd26ed2df1e1dba6901b8d04438359648b528f5e7f`. **Lemma 3.2 is printed on page 12 of this file.** Its part (b) gives the uniformly bounded sum of suprema of inverse-curve arclength contraction after the recursive homogeneous, short-length subdivision. The proof specifies only (H2)–(H4) and gives the dependence (C_2=C_2(\delta_0,\theta_*,C_1,C_d)). Its class consists of homogeneous cone-stable curves; the first-step extension in module 321 is therefore necessary. Native 283's “p. 14” citation must be corrected for this pinned PDF, or explicitly tied to a different verified pagination. No external family spectral theorem is invoked in module 321.

### Baladi–Demers

Primary PDF: <https://arxiv.org/pdf/2009.10936>, *Thermodynamic formalism for dispersing billiards*, arXiv `2009.10936v3`, 62 pages, SHA-256 `3b8efc436aa4e276821252d2c1b23297d486928c3ebb0f44c6e2d56296f3d2e3`. Its finite-horizon definition excludes trajectories with only tangential contacts; native 287's strict all-direction geometric bound is compatible. Lemma 3.6 (pp. 16–20) contains the full two-dimensional small-cell estimate (3.18) and long-ancestor renewal. Lemma 3.8 (p. 20) obtains bounded (Q_n(1)) through Proposition 3.14 and a curve-growth result. Proposition 3.14 (pp. 25–27) uses finite Cantor rectangles and a mixing crossing time. These additional table-dependent constants have not been made radius-uniform merely by native 318. Definition 3.2 (p. 12) also changes the homogeneity exponent with a thermodynamic parameter interval; it is not the native fixed (q=2) partition. Module 321 cites none of these as an unverified shortcut and keeps the remaining short-capacity obligation explicit.

The exact inspected primary files are retained at `audit-corpus/literature/1210.1261.pdf` and `audit-corpus/literature/2009.10936.pdf` in the shared work area; the parent source/literature audit determines their final preservation path.

## Executed exact checks

Program: `check_transversal_capacity.py`. It uses only Python's standard library, `Fraction` arithmetic, and a small exact polynomial ring. There are no floating-point orbit samples and no Python `assert` statements. Passing with `-O` therefore does not remove the verification gates.

The seven check groups cover:

1. The physical fiber metric, radius length factorization, and exact circumference-to-angle conversion.
2. A nonnegative-coefficient polynomial certificate for the universal cone projection inequality, and the no-extra-wrap inequality.
3. The image arclength bound, adapted metric factors, exact (59/47) expansion, and one finite admissible homogeneity-threshold witness. The proof retains its inherited (k_0); no numerical value for (ell_*) is invented.
4. The reversal/translation involution and terminal strip indices, with 1,554 exact algebraic word tuples. These tuples check label algebra and are not presented as realized physical orbits.
5. A failure-sensitive endpoint accounting example requiring the multiplicity-three budget, with one representative per disconnected class.
6. An exact logical non-implication example: disjoint angular sets with individually decaying weights can satisfy the capacity moment bound while their unweighted sum grows. This is an abstract counterexample to an invalid inference, not a counterexample for the Lorentz model and not a replacement stochastic model.
7. The optical/normalization factor ledger and unchanged limit-order declarations.

Both normal execution and `-O` completed with exit code zero and empty stderr on 2026-10-20. Their compact stdout and detailed JSON files are byte-identical. Actual commands, interpreter identity, runtime timestamps, source hashes, and result comparisons are in `execution/receipt.json`. The detailed evidence is `execution/normal.json` and `execution/optimized.json`; complete stdout/stderr streams are retained beside them. The exact computation supports the written proof; it does not independently certify its continuous geometric premises or the final raw theorem.

## Minimal remaining closures

The new theorem is a complete geometric contribution in its stated scope. The current route still requires a genuine uniform payment for the physical-word small-capacity supremum sum in `tc:remaining-pressure-interface`, or a different mechanism that directly establishes the original (Q_*) bound. A complete conditioned physical-roof source/capacity estimate must additionally provide the original normalization and all required boundary and singular contributions. Neither gap is resolved by renaming a residual, discarding a small class, changing a conditioning event, invoking independence, widening a microscopic window, or exchanging the original outer limit and collision limsup.

No independent external specialist reconstruction or journal acceptance is asserted by this audit. The parent coauthor integration has separately reconstructed module 321's major geometric steps; final compile and repository publication evidence belong to the integrated revision record.
