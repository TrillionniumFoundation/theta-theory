# Source and execution audit: A2 v15 independent review

This file delimits the evidence behind [REFEREE_REPORT.md](REFEREE_REPORT.md). Reading a statement, checking its proof, running finite diagnostics, and formally certifying it are different activities. No formal certification is claimed.

## Immutable source identity

Repository: `TrillionniumFoundation/theta-theory`.

Author branch: `revision/a2-v15-intrinsic-scalar-transport-2026-09-11`.

Author commit: `627c16b951994fa65acfbf3a621d0e4306131db3`.

Author root tree: `5f17c9f2038a67b050bba74e2ce857cbb4c4c5f6`.

Native manuscript: `papers/A2-v15-intrinsic-scalar-transport`.

Preceding report commit: `0c523413ef7ffa2dedd1ab471ce58b3275896a93`.

Preceding report path: `reviews/a2-v14-independent-harsh-intrinsic-density-2026-09-11/REFEREE_REPORT.md`.

The preceding author version identified in that report is `e136929b120912586266fb78e0ae7b3c9d43bfd6`. That provenance is not a claim to have re-read the entire v14 source tree. The current repository was accessed through authenticated GitHub connector reads. There was no complete local clone. Review files are added on a new branch based on the pinned author tree; no author source, earlier report, workflow, branch protection, or membership change is part of this review.

## Material actually read

Except where noted, paths are relative to the native manuscript directory at the author commit above. Ranges describe source access, not independently verified typeset page numbering. Where a large connector response truncated, the narrower actual coverage is stated instead of claiming a full-file read.

| Source | Actual review coverage |
| --- | --- |
| Repository `README.md` | Complete current-version navigation and status text. |
| Native `README.md` | Complete reading map, diagnostic commands, and explicit isolated-build versus full-build distinction. |
| `RESPONSE_TO_REFEREES.md` | Complete response to C14-1/C14-2, width comparison, significance statement, preservation and execution claims. |
| `main.tex` | Complete abstract, top-level input graph, acknowledgments and bibliography input. No independent enumeration certificate for all nested inputs was produced. |
| `article/01_introduction.tex` | Substantial initial portion: stated contribution hierarchy, geometric/observation setting, multiplier convention, main relative theorem and its listed dependencies. The large response truncated in the later hyperbolic-positioning discussion; a complete-file read is not claimed. |
| `article/16a_scalar_linearization.tex` | Complete lemma, mixed-derivative proof, normalized uniqueness, iterate estimates, finite product and alternating scalar comparison. |
| `article/16b_determinant_transport.tex` | Complete corollary, exact finite logarithmic remainder, uniqueness identification and scope statement. |
| `article/16_hyperbolic_coordinates.tex` | Read in source ranges 1-210 and 211-470: analytic mixed-boundary comparison, physical projection, origin normalization, scalar input, physical cocycle proof, width and comparison discussion. |
| `v4/10_boundary_layers.tex` | Read in ranges 1-240 and 241-420: half-line construction, trace-class amplitude, gluing and relative determinant proof, physical integration, conditional law, tied-onset and pole corollaries. The report concentrates on the principal factorization/integration chain. |
| `article/23_two_contact_rigidity.tex` | Requested range 1-300; response truncated near the final discussion. The full principal block-inverse proof and analytic-boundary corollary were read, including action, determinant and residual-time coefficients. No claim to have read beyond the returned final discussion. |
| `article/24_physical_image.tex` | Range 1-235: full support-function realization, finite-fibre statement, finite-window theorem and its proof through the initial concentration calculation. Its final risk proof was not read here; the complete direct two-flight proof below was read instead. |
| `article/29_two_flight_benchmark.tex` | Ranges 1-220 and 220-390: complete two-flight action/twist/moment inverse, fixed-order coordinate comparison, and direct observation theorem including adaptive-window lower bound. |
| `article/20_boundary_compatibility.tex` | Range 1-250: full profile definition, pushforward, convolution identity, smooth Volterra uniqueness and stability; also finite-jet statements and the beginning of their proof. Subsequent finite-jet material not claimed as fully read. |
| `article/21_abel_stability.tex` | Complete Abel transform, two-sided inverse, nullspace, mixed estimate and monomial/fixed-class instability benchmark. |
| `article/28_regularized_observation.tex` | Ranges 1-250 and 251-520: complete revised gain, positive-node reconstruction, dictionary, concentration, calibration plug-in, budget and limitations. |
| `article/27_profile_calibration.tex` | Ranges 1-240 and 240-360: complete pilot construction and plug-in discussion, including the terminal projections and cost proof; earlier self-calibrated theorem retained in that file. |
| Preceding v14 `REFEREE_REPORT.md` at its own pin | Initial substantive sections and the remainder obtained with range 220-430. Read verdict, mathematical findings, C14-1/C14-2, diagnostic scope and literature discussion. |

The earlier referee's separate scalar/width memorandum was discussed in the current response and preceding report, but was not separately retrieved for a full read in this review. The present scalar benchmark and code were independently written. No claim is made to have audited every historic derivation directory, old review branch, companion, or auxiliary appendix.

In particular, the older finite-bridge physical localization and geometric-action source files were not re-read in their entirety. Their dependency role is stated in the current manuscript, and relevant uses were examined in the half-line/factorization and direct two-flight proofs. The report's finding of no new fatal error is explicitly confined to the inspected core, not promoted to a complete fresh proof of all inherited input lemmas.

## Selected independently returned blob pins

All entries are UTF-8 source blobs returned by the connector; the full commit pin above remains authoritative even for files not separately listed here.

| Source | Git blob SHA |
| --- | --- |
| Native `README.md` | `fbb8767c95a2ee2227e7a274dcbdfd7bc8b199b6` |
| `RESPONSE_TO_REFEREES.md` | `a2000ba4371b2c1d40d4d68b423d8cd5b210832b` |
| `main.tex` | `035f66f5d1e50205de0f3f0f440f13ff6cb072f4` |
| `article/16a_scalar_linearization.tex` | `f043720b2306b5470c3f2de9cd3ab33efbd296da` |
| `article/16b_determinant_transport.tex` | `f75e7d7793817060328497c189a50d974eb2035a` |
| `article/16_hyperbolic_coordinates.tex` | `836f0036c4d2c3ae279086fd013c87eb652ca227` |
| `v4/10_boundary_layers.tex` | `892a88e37a24e591fa525013c41910c791e28e73` |
| `article/29_two_flight_benchmark.tex` | `07174156a9048407b96c0281b75767b57b897421` |
| `article/20_boundary_compatibility.tex` | `a6292a952053187e872a2d69f7ce1540ee382c07` |
| `article/21_abel_stability.tex` | `f7d11b05702d7a47599f54c2f75efde5844b7329` |
| `article/24_physical_image.tex` | `520455630bf55e5ae07af5ffaffcccfdb4653cea` |
| `article/27_profile_calibration.tex` | `c2aedf2d3c08d545373fbdd26c3f3577956a1c2c` |
| `article/28_regularized_observation.tex` | `919ba3c9d9492529d30a9edb862298b34c695096` |
| Preceding v14 report at its own commit | `2005062d3bff602350c9a8b64011cbfeaf3dcc29` |

## Independent execution

The following commands were executed locally on the newly written script. From this review directory they reproduce the same operations:

```sh
python3 verify_review.py --output diagnostics.normal.json
python3 -O verify_review.py --output diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

Both Python invocations returned success with **3,318 explicit checks**. The `cmp` invocation returned success. Environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. Byte identity is a statement about the two recorded runs in that environment, not a cross-platform floating-point guarantee.

Script SHA-256: `f68f215d27b9ebada57ba2710af4106e4174078761aac859589d18af5556b681`.

Script Git blob hash computed locally: `2029cbc259b93c9d0733c197451bab467aaf5653`.

Both JSON files have SHA-256 `9ae8d861d7d68a2a3d6f6ad2cca454bf12afb210583a23f8299c224cc045f8d4` and Git blob hash `2090e2a23f19b834ee46c38f4ab00af7603a7fa6`. Their identity permits the same blob to be stored at two paths without altering either recorded output.

| Diagnostic group | Explicit checks |
| --- | ---: |
| Exact mixed scalar jets | 2,880 |
| Exact alternating first-flight cocycles | 8 |
| Wrong-normalization negative controls | 16 |
| Essential strict-margin benchmark | 1 |
| Finite Euclidean bridge residuals, twists and Hessian pivots | 270 |
| Exact-origin reference normalization in floating point | 40 |
| Direct cofactor versus Schur complement | 16 |
| Nonzero-endpoint relative separation at 32 flights | 4 |
| Truncated scalar derivative-product comparison | 1 |
| Exact contact-block identities and quartic example | 73 |
| Width/profile monomial inversion | 9 |
| **Total** | **3,318** |

The count reflects explicit equality or tolerance checks, including individual rational Taylor coefficients. It is not a measure of the number of independent theorems verified.

### Interpretation of the numerical physical checks

The local patches are

`psi(x) = kappa*x^2/2 + cubic*x^3/6 + quartic*x^4/24`.

The two model parameter pairs are recorded exactly as supplied to the floating-point solver in the JSON. Both include odd terms; one has equal curvatures and one unequal curvatures. Small tested endpoints remain in positively curved facing patches. No global periodic completion was constructed in this diagnostic.

The stationary bridge solver starts from the quadratic Green solution and applies banded Newton steps. It checks the resulting residual, negative local mixed flight derivatives, and positive interior Hessian pivots. The normalized cofactor is evaluated by logarithms and LDL pivots rather than by subtracting tiny determinants. A direct tridiagonal Schur calculation independently checks the reduced mixed derivative.

The nonzero-endpoint separation quantity is

`abs(b_j(u,v)/(b_j(u,0)*b_j(0,v)) - 1)`.

This compares finite bridge amplitudes, not numerically certified infinite half-line amplitudes. Nonlinear separation is sampled at even flight numbers 4, 8, 16 and 32, for both starting types; the zero-endpoint normalization check also includes odd flight numbers. A zero floating-point defect in a row means rounding equality, not exact equality of the nonlinear functions.

The JSON group `physical_scalar_identification` is an abbreviated diagnostic label. Its single check follows a 42-flight stationary bridge, multiplies first-coordinate derivatives through ten flights, divides by the five-return reference multiplier, and includes the remaining 32-flight normalized amplitude. This is a finite Schur-concatenation/truncated stable-branch consistency test. It does not compute or certify the infinite Fredholm determinant independently, and it must not be cited as a numerical proof of the infinite identity.

The exact rational mixed-jet tests differentiate the explicit scalar family in the report in `(lambda, a, u)` through total order three. They do not establish all-order smoothness by sampling, nor do they differentiate the nonlinear Euclidean model in all geometric directions. The strict-margin conclusion itself follows from the printed analytic formula, not from its four numerical values.

## Work explicitly not performed

No full article or companion TeX compilation; no rendered-PDF inspection; no remote CI execution; no formal proof-assistant run; no interval arithmetic; no global periodic-table trajectory simulation; no empirical success-probability experiment; no independent rerun of the author's 10,549 checks or the old referee's 3,216 checks; no exhaustive nested-source retention comparison; no complete re-refereeing of all historical material or appendix statements.

The author's README and response distinguish the isolated 18-page smoke build from a complete manuscript build. This review records that disclosure rather than turning it into either a claimed successful full build or an observed full-build failure. The requested complete integrated build is a submission-readiness check.

## External comparison scope

The primary-source HTML of Eynard-Bontemps--Navas, arXiv:2212.13646v2, was inspected for the classical one-dimensional linearization comparison. The versioned HTML of De Simoi--Kaloshin--Leguil, arXiv:1905.00890v4, was inspected for the local hyperbolic normal form and its separation from geometric symmetry assumptions. For Hofmann--Werner--Deng, arXiv:2212.06534, only the abstract-level description of the L2 deautoconvolution setting was used. The full references and precise limitations are in the report.

No exhaustive priority claim is based on this targeted search. The scalar formulas, strict-margin benchmark, weighted Volterra verification and finite diagnostics in the report are presented with their own calculations, not as unnamed results imported from those papers.
