# Independent audit ledger: A2 v65

Review date: September 16, 2026. This accompanies `REFEREE_REPORT.md`; it is not a proof certificate or a commissioned journal report.

## 1. Frozen objects

Repository: `TrillionniumFoundation/theta-theory`. Manuscript path: `papers/A2-v17-boundary-information-coarsening/`.

| Object | Identity |
|---|---|
| Actual compiled source | `06a197e4d11bc3d4193e9f0b7904105df35875fa` |
| Source repository tree | `e8a436f62cd1bcbfd7632e4856cd8efc4c361dcf` |
| Reconstructed manuscript subtree | `469aba06035399f96f07417b172653228df36114` |
| Native-products review parent | `5425d9846069a0d23d454d20fe19ed0586d39270` |
| Products repository tree | `fae02fb1fd4287869b2aeb73d83f5b28a2da4817` |
| Workflow / attempt / artifact | `35059519641` / `1` / `10432052220` |
| Preparation commit, not the compiled source | `8433bc580b63ed166752d38cea7995aa9830894a` |
| Previous review commit | `838e62dd0435f350ca9f398df09374e189a6e44c` |
| Previous mathematical source | `ee2380ceb76808dd2969d6b5faaa180737020eff` |

Current artifact SHA-256: `8aa528bb293e31daecb88522210f2f8418779d2a3ac11536041b308b13a983d3`.

Current frozen source ZIP SHA-256: `836cbacce93c3ea8cf9173f718f048259e8daa42ecb71811fe6312b4684f4499`.

Baseline artifact: `10429927974`, SHA-256 `5d77b2174e56fd5021c0384f4b9811add1b7ba79b2f975ad8ce2678f65b57aa6`.

The source and completed products branches were found; no separately named v65 review-ready branch was listed at the discovery snapshot. The GitHub comparison from source to products contains two delivery commits and no alteration of compiled mathematical inputs. The new module was additionally read directly at the immutable source; its Git blob is `fb311379b077bfbbe88e862b7f5818136d3e59b8`, matching the archive.

Hash checks establish consistency of the compared objects. They do not authenticate authorship, certify mathematical truth, or independently reconstruct the entire repository tree. The manuscript subtree is reconstructed with the Git modes in the frozen manifest and compared to the native build record.

## 2. Mathematical reading and exclusions

The complete 708-line `article/10b_periodic_contact_inverse_v65.tex` was read, including all nine statements. The key obligations examined are the marked graph sensor, signed chord Hessian, one-step contraction, nonlinear coordinate gauge, two-offset action extraction, actual smooth envelope, nonlinear curvature map, signed cyclic response, variable-quadratic Banach construction, full low-degree/tail inverse, and downstream scope and realization.

The independent Riccati derivation of the curvature derivative and the explicit polar-convexity bound appear in the report. They are mathematical cross-checks rather than claims that the source had omitted necessary arguments. The offset-dependent recording example is outside the declared common-amplitude model, not a counterexample to the printed theorem.

The shared introductory theorem, current abstracts, response, cover letter, historical audit, dependency ledger and literature note were read. The retained v64 periodic module and the v60 contracted-evaluation/real-to-disc interfaces were examined for their role in the new result. Full reading details and source ranges are in S1–S5 of the report.

Not freshly certified in their entirety: all older finite-chain/full-phase prerequisites; every inherited alternating inverse, global registration/lattice and moving-family argument; all calibration and statistical constructions; the companion. No line-by-line audit of all 469 delivered pages, semantic census of independent theorems, or exhaustive priority investigation is claimed.

## 3. Source preservation and native evidence

`verify_delivery.py` is reused unchanged from the preceding independent review. It imports no author checker. It verifies each recorded byte count, SHA-256 and Git blob, reconstructs the manuscript subtree, checks the active-input manifest, and checks the build-report evidence and product hashes.

Results: **818 frozen files**, **131 distinct active inputs**, and **45 evidence entries**. Active per-entry counts are 120 full, 52 principal and one companion; shared inputs explain the difference between the sum and the union.

`compare_baseline.py` independently verifies both frozen archives. All **800** inherited paths remain: **793** unchanged and **seven** changed, with byte-exact originals in `history/v64-review-baseline/`. All 129 inherited active paths remain. The two new active paths are `article/00f_periodic_contact_overview_v65.tex` and `article/10b_periodic_contact_inverse_v65.tex`. The complete v64 periodic-forward module, corrected finite-experiment module and physical position-pilot module are byte-identical. Five finite-experiment statement bodies are also compared syntactically. These are preservation results, not renewed proof certifications.

The author's preservation and mathematical checker was **not rerun**. Its recorded output is among the native evidence whose file hashes are checked, which is a different operation.

## 4. Fresh builds and actual visual scope

All entries were rebuilt in a clean copy of the extracted manuscript source, with regenerated auxiliaries and shell escape disabled. Build order: companion, full manuscript, principal article. The actual command template is

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' ENTRY.tex
```

All builds succeeded. Principal **143**, full **319**, companion **7** pages total **469**. Every page matches the native delivery in extracted text and same-renderer 72-dpi RGB arrays. PDF byte identity is false. The fresh PDF hashes and final log summaries are in `AUDIT_RESULTS.json`.

The final full log has four underfull-box notices; principal and companion have none. No undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found in the checked final logs. This is a disclosed pattern scan, not a claim that every possible TeX warning has been semantically analyzed.

Actual visual inspection covered principal pages **36, 38, 40 and 42**, rendered at **108 dpi**. No clipping or unreadable formula was observed there. Additional pages were rendered while locating the proofs but are not counted as inspected. All-page image-array equality is not all-page visual inspection.

## 5. Independent mathematical diagnostics

`independent_checks.py` imports no manuscript code and uses no removable assertions. It requires NumPy and SymPy. Ordinary and optimized Python emit identical complete JSON in this environment.

The exact checks cover 240 signed cyclic blocks for periods 2–7 and degrees 2–11, six curvature Jacobians obtained by implicit Riccati differentiation, and 15 odd-cycle sign-erasure controls. The constructed rational recurrence parameters are positive, but arbitrary such tuples are not declared globally realized billiards.

The two-offset checks use explicitly normalized positive polynomial densities: 294 action identities and 42 axis-amplitude recoveries. The 252 changed-efficiency controls show why offset-dependent nuisance factors are outside the shared-amplitude conclusion; these are not defects in the theorem.

The numerical geometric check solves actual Euclidean chord stationarity on local graph arcs based at an equilateral and a scalene contact triangle, with unequal curvatures and cubic terms. It checks 72 configurations, both endpoint signs, three phases, 12 or 18 flights, and variations of degrees 2–4. It detects doubling the initial variation in all 72. The largest envelope relative discrepancy is `9.66234331881726e-08`; the two finite-difference curvature Jacobians have maximum-entry discrepancy at most `1.5266454767015603e-11`. A finite small-endpoint cyclic comparison has maximum absolute discrepancy `4.740375538325736e-06`.

The solver uses the analytic tridiagonal chord Hessian in Newton steps and verifies the final stationarity residual. An exploratory generic root solver stalled on tiny tail coordinates and was replaced; that numerical implementation issue is not a mathematical counterexample. These finite graph arcs are not being represented as a separately certified global periodic realization, nor are the finite differences rigorous infinite-limit bounds.

The polar check establishes the exact contact curvature `1-delta` and positive analytic convexity lower bounds in three parameter boxes. Complete lattice-clearance persistence still relies on the geometric margins of the source proof, not on a sampled plot.

No diagnostic certifies Banach holomorphy, arbitrary-order differentiation, trace-class convergence, global continuation or a statistical theorem. Full configuration output, hashes and toolchain information accompany the local audit archive.

## 6. Primary-literature verification

The report's L1–L5 identify the sources and limits. Bolotin–Treschev Theorem 2.1 and the orientation discussion were checked in the primary PDF, including a successful screenshot of printed page 12. Bálint–De Simoi–Kaloshin–Leguil Theorem D, Corollary E and Remark 2.3 were read in the primary PDF text; a screenshot request failed and is not claimed successful. The other three sources were checked at primary abstract/version-record level. Their full proofs were not audited.

These comparisons distinguish observation models rather than establish a reduction, priority, or redundancy. The Florio–Leguil version-5 correction is retained as a correction, not cited as an available geometric inverse theorem.

## 7. Reproduction

Extract artifact 10432052220 into `WORK/artifact/` and its `native-source.zip` into `WORK/source/`. The source layout is `WORK/source/SOURCE_MANIFEST.json` and `WORK/source/source/`. Start without `WORK/rebuild/`. From this review directory run:

```sh
python verify_delivery.py WORK
python verify_delivery.py WORK --build two_collision
python verify_delivery.py WORK --build main
python verify_delivery.py WORK --build rigidity
python verify_delivery.py WORK --compare
python compare_baseline.py a2-v64-native-products.zip a2-v65-native-products.zip > SOURCE_DIFF.json
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS_OPTIMIZED.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS_OPTIMIZED.json
```

PDF comparison additionally requires PyMuPDF; builds require a working TeX installation and manuscript packages. Numeric last digits and byte hashes can change across environments. The scripts use frozen archives, not a moving branch, and make no network requests.

Only files in the new review directory are added. Manuscript source, previous reports, deliveries, the default branch and repository permissions are not changed by this review. No merge, PR approval, or commissioned editorial decision is implied.
