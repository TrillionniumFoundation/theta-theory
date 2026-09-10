# A2 v13 source, scope and reproducibility audit

Date: 10 September 2026. Companion to `REFEREE_REPORT.md`.

## Frozen identities

- Repository: `TrillionniumFoundation/theta-theory`.
- Author branch: `revision/a2-v13-two-flight-relative-invariants-2026-09-10`.
- Author commit: `0e54099f079232df233316ae6fe7986fc51b7ea1`.
- Author root tree: `41f68e02205e10d48e917559f0f5092c10799948`.
- Manuscript directory: `papers/A2-v13-two-flight-relative-invariants`.
- Parent / previous completed review: `2ae2751f61224b66f314915fd5fc22f6321b606f`.
- Previous author revision: `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`.
- Previous report: `reviews/a2-v12-independent-harsh-two-flight-2026-09-10/REFEREE_REPORT.md`.

Branch enumeration, commit metadata and the manuscript directory were read using the connected GitHub API. Subsequent source reads used the fixed commit, not a moving branch name. The report is not an assessment of unrelated historical A2 directories or the repository's other papers.

## Direct manuscript reading

All paths in this table are relative to the frozen manuscript directory. “Complete” describes the returned source body read for this review; it is not a statement that every theorem has been formally verified. Partial ranges are source line ranges, not the connector's JSON wrapper lines.

| Source | Coverage | Git blob |
| --- | --- | --- |
| `RESPONSE_TO_REFEREES.md` | Complete | `f5631b898e5f681a5671d9f8bcc0513bf31ea728` |
| `README.md` | Complete | `677a6ee6db8642198b4b01be025410d25f92d3e7` |
| `main.tex` | Complete, including active input list and acknowledgments | `302bf56c736014700e025965c6f3763e184d66e8` |
| `article/01_introduction.tex` | Complete | `e7bbdc6a514404f9e9e998f1c27adfbb41832aa8` |
| `article/29_two_flight_benchmark.tex` | Complete new proof and observation theorem | `b679a0c457d013bcd8f60761e28e8b919f0dbf31` |
| `v3/10_geometry_action.tex` | Complete, through relative determinant and analytic extension | `bbfcaa2d01c229ec0147d5305352b536397842ae` |
| `v3/20_integration.tex` | Complete | `56d9767a769591e74397057c6da873bcc584ff2e` |
| `v4/10_boundary_layers.tex` | Complete, including factorization, physical law and final corollaries | `892a88e37a24e591fa525013c41910c791e28e73` |
| `article/15_operator_comparison.tex` | Complete | `886adb2d68e105723f41f6554eeec59391cab44c` |
| `article/20_boundary_compatibility.tex` | Lines 1–245: profile definition, full smooth compatibility/uniqueness and stability proofs, finite-jet theorem and start of its proof | `a6292a952053187e872a2d69f7ce1540ee382c07` |
| `article/21_abel_stability.tex` | Complete | `f7d11b05702d7a47599f54c2f75efde5844b7329` |
| `article/22_deautoconvolution.tex` | Complete | `49fdf2981c18deb6047367790b48057c474a956b` |
| `article/23_two_contact_rigidity.tex` | Complete source body, including analytic continuation corollary; response metadata was truncated after the body | `49d0468658a5b219d5a51720714ffb3194e1110a` |
| `article/24_physical_image.tex` | Lines 1–240: complete realization and fibre proofs, finite-window theorem and proof through the initial estimator construction | `520455630bf55e5ae07af5ffaffcccfdb4653cea` |
| `article/27_profile_calibration.tex` | Complete, including the smooth pilot and its charge | `c2aedf2d3c08d545373fbdd26c3f3577956a1c2c` |
| `article/28_regularized_observation.tex` | Complete | `919ba3c9d9492529d30a9edb862298b34c695096` |
| `v5/references.tex` | Complete bibliography | `ce456be9e1559203443f95d0820b9f1fcfa1ccc6` |

The prior v12 report was read for its recommendation, principal two-flight finding, previous-issue disposition and the detailed mathematical audit visible through the beginning of Section 3.5. Its entire remainder was not independently reread. The new v13 response, proof and introduction were compared with those concrete prior findings. The prior report was contextual evidence, not a substitute for the directly read new proof.

This is not an exhaustive fresh audit of the full auxiliary appendix, the retained companion manuscript or every historical derivation. In particular, the older acquisition algorithms, all collision-record applications and every inherited statistical lower bound were not independently rechecked in this round. The core finite-family risk argument was read in full in the new two-flight section, rather than inferred from the partially read older long-bridge proof.

## Primary literature checks

The review consulted the primary De Simoi–Kaloshin–Leguil preprint, arXiv:1905.00890v4, including its stated inverse hypotheses and local normal form; Finamore–Leguil, arXiv:2510.18983v1, introduction and Theorem A; and Zelditch's primary preprint, arXiv:math/0111078, for the stated symmetry-class spectral comparisons. Relevant PDF pages were inspected as rendered pages as well as parsed text. Exact reading locations and links are supplied in the report and benchmark.

The original Moser 1956 paper was not separately read in full. The historical normal-form input is used in the explicit form recalled in the consulted primary billiard paper. The endpoint projection calculation in the companion memorandum is an independent derivation. No exhaustive priority claim is made.

## Reproducing the independent finite diagnostics

From this review directory, using Python 3 and its standard library:

```sh
python3 verify_review.py --output verification.normal.json
python3 -O verify_review.py --output verification.optimized.json
cmp verification.normal.json verification.optimized.json
cmp verification.normal.json verification.json
```

These commands were run locally for this review; the two execution modes produced byte-identical JSON and passed 5,033 explicit checks. All checks raise on failure rather than relying on `assert`, and no author module is imported.

The script uses exact fractions and finite factorial/binomial identities. It checks finite contact blocks, an omitted-twist negative control, limiting separation identities, and normal-form mixed-boundary/projected derivatives against products of one-step symplectic derivatives. Its small-denominator checks are finite samples, not uniform estimates; uniform arguments are written in the benchmark. The tests do not generate normalizing charts for arbitrary smooth billiards.

## Activities not performed

No author diagnostic suite or earlier referee suite was rerun. No TeX build, rendered manuscript pagination audit, remote CI run, simulation of nonlinear collision probabilities or formal proof verification was performed. The author's page count, number of retained formal blocks and advertised test totals are not independently certified here. Reading a source file and passing finite algebra checks must not be represented as those stronger activities.

The deliverable consists only of a referee report, the analytic comparison memorandum, this audit, the independent script and its result. It contains no edited manuscript, journal submission, permission change or requested merge. Source pins identify the reviewed material independently of the eventual review-branch tip.
