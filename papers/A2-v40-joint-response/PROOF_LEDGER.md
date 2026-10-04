# Proof ledger — A2 v40

## 1. Reviewed baseline and preservation object

The reviewed source is `papers/A2-v39-response-rigidity` at commit `f815a7acdb5c03e03b9996fc7052b405db66936d`, paper tree `e60aaed448b772942ffd38d556babab35b3c3880`, core tree `113a60e9545374aee5ae6fd80b14f4fedf8e8ed6`. Its executed TeX closure contains **322 mathematical labels, 76 proof bodies and 79 formal blocks**. These are the preservation baseline.

The new [companion.tex](companion.tex) executes all 32 copied v39 core files. Every core byte and every baseline proof body is retained. Main and companion share only the label-free [preamble.tex](preamble.tex) and [references.tex](references.tex). The qualifier compares the union of both executed input closures with all submitted TeX files, rejects duplicate mathematical ownership, and verifies the actual recorder of each final build. Declared cross-reference entry-file existence probes are recorded separately from typeset inputs; they cannot satisfy a missing mathematical input. The original historical directories are independently pinned by Git tree.

## 2. New primary proof blocks

All 16 new formal blocks below have complete proofs in the primary. The [independent source audit](INDEPENDENT_SOURCE_AUDIT.md) records the mathematical checks and incorporated clarifications. The introduction contains no additional unproved formal assertion. New proof bodies are independently audited; finite diagnostic checks are a separate evidence layer.

| Source and label | Statement | Principal proof mechanism |
|---|---|---|
| `21_two_field_rigidity.tex`, `lem:two-field-prefix` | Finite occupation inverse and stability | Endpoint identity, telescoping prefixes, separated-component exit witness |
| `21_two_field_rigidity.tex`, `lem:two-field-supports` | Identification and matching of the two collision support families | Incoming-strip geometry, positive-measure convolution support and component gaps |
| `21_two_field_rigidity.tex`, `lem:two-field-calibration` | Obstacle identification from three support functions | Footprint cancellation, contact chord and Jordan decomposition of signed curvature |
| `21_two_field_rigidity.tex`, `thm:two-field-rigidity` | Exact canonical geometry and full probability law | Steiner centering, support cancellation, compact Fourier uniqueness |
| `21_two_field_rigidity.tex`, `cor:two-field-fiber` | Complete common-translation fiber, periods and every forward response | Canonical triple, translation coupling and component cancellation |
| `21_two_field_rigidity.tex`, `prop:two-field-one-orientation` | A single forward orientation is insufficient on the exact class | Smooth outgoing support perturbation with identical incoming collision strips |
| `22_two_field_finite.tex`, `lem:two-field-rare` | Finite boundary test from only the two fixed directions | Outer tangent disk, near-tangent candidate selection and rare cap mass |
| `22_two_field_finite.tex`, `lem:two-field-hulls` | Shared positive-record support hulls | Uniform strip area, footprint cap mass, conditional rational quadrature and a direction net |
| `22_two_field_finite.tex`, `lem:two-field-stable-chord` | Stable atom direction, chord length and smooth body recovery | Sine difference, signed plateau moments and structure-sensitive smoothing |
| `22_two_field_finite.tex`, `thm:two-field-finite-geometry` | Finite `C2` geometry and periodic discrete data | Expanded bodies, one calibration chord, common footprint subtraction and retained period locking |
| `22_two_field_finite.tex`, `cor:two-field-finite-cloud` | Complete finite configuration | Same geometry construction on the supplied complete protected aperture |
| `23_two_field_law.tex`, `lem:two-field-finite-moments` | Occupation moments from finite bits | Shared rational grid, fresh prefix queries and translated convex boundary-cell bounds |
| `23_two_field_law.tex`, `lem:two-field-moment-separation` | Quantitative bivariate law separation | Triangular factorial conditioning, tensor Jackson approximation and transport duality |
| `23_two_field_law.tex`, `thm:two-field-finite-law` | Finite positive probability output and joint reconstruction | Certified obstacle moments, finite rational LP and explicit accuracy allocation |
| `23_two_field_law.tex`, `cor:two-field-finite-prediction` | All bounded-length responses in local spatial `L1` | Convex swept-body stability, indicator variation and probability coupling |
| `23_two_field_law.tex`, `cor:two-field-finite-density` | Density `L1` and uniform raw prediction under a known BV bound | Kernel smoothing, `BV -> L2`, geometric symmetric differences and finer law acquisition |

The union therefore has **92 proof bodies and 95 formal blocks**. Label and input-closure counts are computed from the complete submitted source by the qualifier; the final receipt is authoritative for generated PDFs and execution results.

## 3. Assumption and loss ledger

| Result family | Geometric and law class | Observation/loss |
|---|---|---|
| Exact two-field inverse | Strictly convex bodies, bounded diameters, positive gap; arbitrary compact probability with nonempty convex support; `t + Delta < d` | Two whole-plane fields at fixed `±te`; exact canonical triple |
| Exact completion and periods | Same exact class; no periodicity prior | All finite command means with prescribed boundary convention; full period group |
| Finite geometry | Known smooth support and curvature bounds, density lower boundary mass, `2t + Delta < d0` | Finite bits at fixed `±te1`; `C2` geometry, stated nominal mesh |
| Finite periodic discrete decisions | Above plus bounded presentation and known positive patch margin | Exact primitive discrete relations and orbit count; estimated basis and free area |
| Complete finite configuration | Above geometry priors plus a complete protected aperture and bounded number of components | All matched components, no period assumption or patch margin |
| Finite law stage | Arbitrary compact probability conditional on the required geometric estimates; composed theorem uses finite geometry class | Positive atomic output in `W1` |
| Finite response prediction | Same composed class, fixed window and maximum command length | `sup_b ||Fhat_b - F_b||_L1(U)` |
| Strong density and raw prediction | Additional known BV bound on the zero-extended density | Density `L1` and `sup_{x in U, |b| <= T}` raw-mean error |

## 4. Quantitative chains checked

For expanded-body support tolerance `epsilon`, the positive-record hull requires `epsilon^{-(gamma+9/2)}` attempts up to its confidence logarithm. It dominates the rare radial cost `epsilon^{-(gamma+3/2+1/s)}`. Chord correction gives `C2` error `epsilon^{(s-2)/s}`; substituting `epsilon ~ nu^{s/(s-2)}` yields `Q_pair = (gamma+9/2)s/(s-2)`. The displayed theorem retains both logarithmic factors and the full nominal grid.

The law stage takes `m ~ epsilon^{-1}` and `a_m ~ exp[-C m log(Cm)]`. It separately charges geometry at tolerance `c a_m` and at most `C m^2 a_m^{-4} log(Cm/(a_m delta))` moment bits. The finite moment LP allows exponentially amplified error in the estimated geometric moments before applying the factorial bound. The resulting sufficient cost is exponential in `epsilon^{-1} log(C/epsilon)`. No Fourier division through small values is used for the finite estimate.

Under BV, law accuracy `epsilon^2` and smoothing scale `epsilon` give density error `C(V+1) epsilon`. The same acquisition retains geometry at `xi = C a_m`; `BV -> L2` gives raw-mean geometric error `C V sqrt(xi)`, which is smaller than the target. This is why the uniform prediction and strong density corollary have the stated `epsilon^{-2}` cost.

## 5. Reproducibility and remaining review role

The diagnostic programme preserves every inherited v39 finite check and adds endpoint, support-cancellation, moment, prediction and exponent checks. The contract tests cover the two-document source closure, historical proof retention, exact-SHA binding, ordinary/optimized parity, and preservation of evidence on failure. Both final PDFs must have clean stable references and actual recorder closures matching the manifest.

The finite checks and independent source audits support examination of these arguments. The continuum statements are established by the displayed proofs and remain open to the next referee's mathematical review; the ledger makes no journal-acceptance or formal-verification claim.
