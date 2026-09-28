# Source audit for the external A2 v18 rereview

## 1. Reviewed repository object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v18-stable-intrinsic-reconstruction`

The reviewed object is pinned by Git object rather than by a branch label:

- revision branch: `revision/a2-v18-stable-intrinsic-reconstruction-2026-09-28`;
- commit: `0708f67908355e9881d1993b42bcc698b0c350c6`;
- tree: `2e63e7f7cb8c73cda6ce8436bf1f716da3358f78`;
- author/committer time: `2026-09-28T09:45:22Z`;
- parent: `2e01331b1c9e20cf9d11d330fab0a163555aec6b`;
- commit title: `A2 v18: two-window smooth boundary inverse and fixed-exponent whole-table reconstruction`.

A branch search immediately before publication found no `revision/a2-v19...` branch. The v18 branch head was re-read after the mathematical audit and still pointed to the commit above.

The review branch

`review/a2-v18-external-harsh-top4-rereview-2026-09-28`

was created directly from the reviewed author SHA. The review writes only under

`reviews/a2-v18-external-harsh-top4-rereview-2026-09-28/`.

No author manuscript file, author revision branch, earlier review, or unrelated paper was edited.

## 2. Prior report and revision chain

The v18 commit states that it responds to the frozen v16 review at

`62c98e9178c5571a19afaccf8b5e67fc892c6c1e`.

The prior review branch is

`review/a2-v16-external-harsh-top4-rereview-2026-09-28`.

The v16 report withheld a top-four recommendation despite finding no fatal counterexample. Its principal remaining objections were that the intrinsic endpoint law was tailored and rich, the global theorem supplied substantial registration and lattice marking, the exact analytic count-only problem remained open, and the only available whole-table noisy inverse was order-dependent and conditionally analytic.

Version 17, commit

`2e01331b1c9e20cf9d11d330fab0a163555aec6b`,

inserted unregistered image synchronization and an order-dependent finite-data regularization. Version 18 preserves that line and adds a second, function-level inverse based on two full endpoint densities. The present report therefore does not treat v18 as a renamed v16 manuscript.

## 3. Current source map

The v18 manuscript root contains:

- `main.tex`;
- `references.tex`;
- `proof_extract.tex`;
- `core/`;
- `complete/`;
- `tools/`.

The primary article includes the following active core files:

- `core/00_intrinsic_setting.tex`;
- `core/01_full_law_overview.tex`;
- `core/02_local_law.tex`;
- `core/13_two_window_inverse.tex`;
- `core/06_intrinsic_calibration.tex`;
- `core/07_filtered_arclength.tex`;
- `core/03_asymmetric_inverse.tex`;
- `core/08_global_rigidity.tex`;
- `core/11_unregistered.tex`;
- `core/12_stable_reconstruction.tex`;
- `core/09_count_fibers.tex`;
- `core/04_physical_observation.tex`;
- `core/10_intrinsic_experiments.tex`;
- `core/05_relative_laws.tex`.

The principal v18 addition is `core/13_two_window_inverse.tex`. `core/01_full_law_overview.tex` advertises it as a second inverse from the uncompressed endpoint law. The older moment-compressed theorem and its coefficientwise proofs remain active, as do both registered and unregistered network results, the older noisy moment regularization, count-fiber results, and the supplementary relative-law programme.

`proof_extract.tex` contains only the new two-window chapter. It is explicitly not the complete article or supplement.

## 4. Files read for this rereview

The mathematical review read at least the following v18 files in detail:

- `main.tex`;
- `core/00_intrinsic_setting.tex`;
- `core/01_full_law_overview.tex`;
- `core/11_unregistered.tex`;
- `core/12_stable_reconstruction.tex`;
- `core/13_two_window_inverse.tex`;
- `references.tex`;
- `proof_extract.tex`;
- `tools/verify_two_window.py`;
- `tools/validate_v18.py`;
- `tools/run_validation.py`;
- `tools/verify_revision.py`.

The report also read the frozen v16 referee report and checked the v17 parent identity. The audit concentrated on the mathematical delta rather than attempting to re-prove every retained statement in the complete supplement.

## 5. Mathematical delta confirmed

The new source proves or claims the following additions.

### 5.1 Function-level two-window inverse

On a strictly active endpoint rectangle, the physical density is affine in absolute time:

`f_T=(-W_st)/(2 pi A) (T-W)`.

Two complete density functions eliminate the unknown flux factor and recover the action. The diagonal gradient and Hessian yield explicit formulas for both curvatures. Frenet integration and the nearest-point map reconstruct both smooth arcs in relative placement.

This route does not assume analyticity or individual evenness for the local theorem and does not pass through an increasing finite-jet recursion.

### 5.2 Conditional local stability

Under uniform physical `C^3` bounds and positive active, twist, projection, and time-separation margins, the quotient is locally Lipschitz from two `C^2` density functions to the action and then to both intrinsic `C^2` boundary arcs.

### 5.3 Finite histograms

A `3 x 3` tensor cell-average stencil locally reproduces coordinatewise quadratic polynomials. On a uniform `C^{2,beta}` class, cell probabilities known to absolute error `epsilon` give density error

`C(h^beta + epsilon h^(-4))`

in `C^2` on a smaller rectangle.

### 5.4 Fixed-exponent whole-table regularization

A finite onset pilot selects two strictly active absolute times. Two endpoint histograms per channel recover local arcs; quantitative analytic continuation gives complete obstacle images; asymmetry margins synchronize edgewise reflection orbits; marked cycle labels recover the lattice. Balancing the cell width gives a class-dependent exponent independent of contact-jet order.

This is a real improvement over the retained order-dependent moment theorem.

## 6. Independent diagnostics

The review's `verify_review.py` imports no author module. Its exact standard-library suite performs 11,525 checks:

| Group | Checks |
|---|---:|
| source curvature | 900 |
| opposite curvature | 900 |
| nearest-foot arclength speed | 900 |
| positivity and twist margins | 900 |
| two-window bivariate coefficient identity through degree 3 | 3,000 |
| flux factor recovery | 300 |
| coherent reversal equivariance | 300 |
| one-dimensional cell-average matrix inverse | 9 |
| tensor polynomial reproduction | 81 |
| histogram rate balance | 6 |
| rank-two lattice recovery | 4,224 |
| Fourier asymmetry obstructions | 5 |
| **Total** | **11,525** |

A separate nonlinear numerical check used five asymmetric quartic local graph pairs, nine source arclength values per pair, direct stationary midpoint solutions, and independently differenced actions. It produced 90 curvature comparisons with maximum absolute error approximately `1.29e-8`.

These diagnostics support finite formulas only. They do not certify uniform physical clearance, density derivation, analytic continuation, Borel selection, the retained supplement, novelty, or editorial significance.

## 7. Delivery and validation audit

The v18 source contains a validator, `tools/validate_v18.py`, designed to:

- bind the exact checkout;
- verify retained source objects;
- run `verify_two_window.py` normally and under optimized Python;
- build the proof extract;
- invoke the retained all-volume build;
- record source and PDF hashes.

That qualification cannot complete on the reviewed commit as stored.

### 7.1 Missing pins

`validate_v18.py` reads

`papers/A2-v18-stable-intrinsic-reconstruction/SOURCE_PINS.json`,

but no such file exists in the v18 manuscript root.

### 7.2 Missing workflow

There is no

`.github/workflows/a2-v18-verify.yml`

on the reviewed branch. Workflows exist for A2 versions through v17, but not for v18.

### 7.3 No exact-SHA Actions evidence

The GitHub Actions query for head SHA

`0708f67908355e9881d1993b42bcc698b0c350c6`

returned zero runs.

### 7.4 Retained historical schema

`tools/run_validation.py` and `tools/verify_revision.py` retain v17 descriptions and schemas. Nesting a retained historical suite is acceptable only if the v18 wrapper actually runs and records a current exact-SHA receipt. No such receipt exists at the reviewed head.

### 7.5 Consequence

The commit message accurately calls v18 a “mathematical checkpoint” and disclaims a hosted build or formal proof certification. The report does not infer a failed TeX build. It records that no authenticated full v18 build or exact-checkout qualification has been supplied.

## 8. Scope limitations of this audit

This is a harsh external referee-style review, not a formal verification of every result in a long multi-volume programme.

The audit did not:

- execute a complete TeX build of the primary article and Supplement S;
- reproduce the exact Git-object retention checks in a local checkout;
- exhaustively search the literature or prove historical priority;
- re-prove every older moment, Volterra, Abel, count-fiber, or physical-realization statement;
- certify statistical optimality;
- make a journal decision.

The review did:

- pin the exact author commit and tree;
- compare the new theorem with the frozen objections;
- inspect the complete new proof chapter;
- independently check its finite algebra and nonlinear stationary geometry;
- inspect the global synchronization and regularization logic;
- audit the current delivery pipeline;
- assess the package at the requested top-four standard.

## 9. Audit conclusion

Version 18 is a genuine mathematical revision. Its new local inverse is substantially cleaner and stronger than the previous coefficientwise route, and the fixed-exponent histogram theorem closes an important conditional stability gap.

The reviewed source is unambiguously pinned, and the new review branch is isolated. The absence of v18 pins and exact-SHA workflow evidence is a real reproducibility defect but not, by itself, a counterexample to the mathematics.

The negative recommendation in `REFEREE_REPORT.md` rests primarily on information richness, missing nearest-neighbour literature comparison, the strongly marked and conditional global model, unresolved count-only questions, and the exceptional significance threshold of the requested journals.
