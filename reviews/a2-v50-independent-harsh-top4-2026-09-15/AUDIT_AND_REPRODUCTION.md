# A2 v50: source audit and reproduction record

This document defines the source identifiers in [REFEREE_REPORT.md](REFEREE_REPORT.md), records the independent checks actually performed, and separates them from claims not made. The assessment is dated September 15, 2026, in the review's Europe/Amsterdam calendar; some underlying Git and local build timestamps fall on September 14 in UTC. This is an author-requested AI-assisted review, not a journal commission.

## 1. Immutable review objects

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v50-review-ready-2026-09-15` |
| Frozen review-ready head | `9c358bb5792f244bab7b510b36c65c50eab6302a` |
| Its root tree | `fd80e62ccbd30614c05955b4fb13e1ceeb4a0c24` |
| Actual compiled mathematical source | `49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4` |
| Mathematical source directory | `papers/A2-v17-boundary-information-coarsening` |
| Source-directory Git tree | `aef336df33a8754390f74e02f1fd855045095661` |
| Native Actions run / attempt | `34908647982` / `1` |
| Downloaded native artifact | `10373213966` |
| Workflow preparation, not compiled source | `17fb13a1ee1af533fdd5cbff5a43f28657d7149d` |
| Product-attestation head | `d46dd93d2068a8cd950dc4604ebf505cea522ca7` |

The review-ready head was re-read immediately before publication of this review and remained unchanged. The review branch is based on that head, not on the repository's default branch or an inferred version number. This review adds only its own report, source audit, evidence record and finite-control script. It does not change manuscript source, native products, prior reports or the author's revision branch.

**D1** denotes the native artifact and frozen delivery, together with the independently generated [EVIDENCE.json](EVIDENCE.json) and [independent_controls.py](independent_controls.py) in this review. The published products and manifests are under:

`deliveries/a2-v50/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/`

at the frozen review-ready head. The full native source ZIP, main PDF and companion PDF are included there. Author-maintained verification records are useful provenance but are not substitutes for the checks described below.

## 2. Mathematical source map

All S-identifiers below refer to files at the **actual compiled source commit**, not to moving branch URLs. Their paths are relative to `papers/A2-v17-boundary-information-coarsening`. A permanent source URL is obtained by appending the relative path to:

`https://github.com/TrillionniumFoundation/theta-theory/blob/49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4/papers/A2-v17-boundary-information-coarsening/`

Line ranges refer to these frozen UTF-8 sources. Page references in the report refer to the delivered 263-page main PDF. Reading a source in full and independently re-proving every result appearing in it are different claims; the coverage column specifies the argument examined.

| ID | Relative path; complete line range | Focus of fresh examination |
|---|---|---|
| S01 | `article/00_structural_introduction_v48.tex`, 1–289 | Observation design, Theorem A, and the new explanation of equations (1.2)–(1.5); full introduction read. |
| S02 | `v3/10_geometry_action.tex`, 1–305 | Local geometry, alternating quadratic reference, Hessian and action interfaces; selective proof coverage. |
| S03 | `v4/10_boundary_layers.tex`, 1–386 | Full relative boundary-layer argument: weighted orbits, normalized cofactor, trace-class localization, gluing and limiting physical law. |
| S04 | `article/23a_signed_endpoint_rigidity_v27.tex`, 1–599 | Full signed-contact source read; finite smooth remainder, terminal-envelope passage, jet filtration and last-jet matrix checked. |
| S05 | `article/23f_single_offset_law_inverse_v42.tex`, 1–270 | Positive interior density ratio, nonzero scalar anchor, amplitude elimination and exact-law interpretation. |
| S06 | `article/23n_finite_symmetry_v49.tex`, 1–243 | Finite symmetry group, congruence enumeration, cochain and completeness; full source read. |
| S07 | `article/23o_two_branch_example_v50.tex`, 1–183 | Full new source. Proposition 19.5 and proof: lines 12–123. Proposition 19.6 and proof: lines 128–177. |
| S08 | `article/23m_differential_rigidity_v48.tex`, 1–505 | Full source read; moving reference, normalization, differentiated inverse, analytic family, local registration, derivative kernel and model-local scalar coordinates. |
| S09 | `article/23k_quantized_law_stability_v46.tex`, 1–574 | Selective: theorem hypotheses and margins, finite-jet/analytic-continuation interface, especially lines 1–153 and 274–318. Not a fresh certification of all quantitative estimates. |
| S10 | `article/23l_calibrated_histograms_v47.tex`, 1–305 | Selective: bounded-displacement category control, inner/outer edges, conditioning on the pilot, amplified gap error and budget interfaces. |
| S11 | `article/18a1_compact_experiments_v32.tex`, 1–160 | Compact finite-net upgrade and uniform-continuity hypotheses. Upstream finite-experiment convergence and all LAN assertions are not certified by this check. |
| S12 | `article/29a_signed_one_flight_benchmark_v25.tex`, 1–67 | Full benchmark source; different observation record and direct one-flight inverse. |
| S13 | `RESPONSE_TO_REFEREE_V50.md`, 1–65 | Author's point-by-point response; read as an account of claimed changes, not as mathematical evidence by itself. |

For exact content matching, the corresponding Git blob identities are:

```text
S01 ef6e770121ac39bd77e5c6b1370601fc44bfd67f
S02 bbfcaa2d01c229ec0147d5305352b536397842ae
S03 892a88e37a24e591fa525013c41910c791e28e73
S04 0285c90309b8ab88d1ce1ecf8d492ea6d71f268e
S05 aea44fc8ed3273174a225b143d3fdf5b5c9b5a19
S06 3bc39ac137812340b9426e9f2b7457a39d6e7f91
S07 e7b85e6238ac0662b7bf91bb13d276ea3dec2c5b
S08 1eb8db48bd184378ebd10be30c033b91edd8f36d
S09 6f507c272f9f69b996872926141aed5df984655b
S10 70f30ea4fdd3048bdac04ee0d3febcf40591a341
S11 176e2588344ce0646ed47c09c64f371d6d16a045
S12 8aebfdef0afa1574dec884b26905cd1024a4364d
S13 43194516ae7c7b7055a034d11a0fe28446fec9d0
```

The complete `main.tex`, active-input manifests, bibliography, historical derivation audit and delivery records were used to trace the compilation and dependency chain. The inherited statistical corpus and appendices are not all newly re-proved in this round. The complete companion was rebuilt and its statements and selected source inspected; its seven pages are not given a new blanket mathematical certificate.

**R49:** [Independent referee-style report on A2 revision 49](https://github.com/TrillionniumFoundation/theta-theory/blob/5051b7789a424656a558179922607d8b55061b28/reviews/a2-v49-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md), frozen at `5051b7789a424656a558179922607d8b55061b28`, report blob `66f0c09d8c1481afdd1b4d71343ff6396302de26`. Its reviewed mathematical source was `a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7`. The prior report's reasoning and the author's response were read; its conclusions were not treated as proof premises. The noncircular example's attribution is retained in the current manuscript and in this report.

## 3. Independent source and product verification

The complete native Actions artifact was downloaded through the authorized GitHub connection. The source ZIP contains `SOURCE_MANIFEST.json` and a `source/` directory. For every one of its **567** manifested files, the local bytes were compared with the recorded size, SHA-256 and Git blob identity. Git blob identities use SHA-1 of `blob <length>\0` followed by the bytes.

The manifest's paths, file modes and verified blob IDs were then assembled into Git tree objects bottom-up. Tree entries were sorted with Git's directory ordering, serialized as mode, name, a zero byte and the raw object hash, then hashed with the appropriate Git tree header. This reconstructs source subtree **`aef336df33a8754390f74e02f1fd855045095661`**. The connected repository's directory listing at commit `49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4` independently reports exactly that tree for the source directory. This ties the archive to the compiled source commit, rather than merely checking an archive against its own file list. The manifest has no excluded tracked products. All **107** active source records also match their local bytes.

Original product hashes computed locally:

| Product | Bytes | SHA-256 |
|---|---:|---|
| `main.pdf` | 1971486 | `cd907cac027839c11f89bfccbbad069ad961cd5e0d21499f03028606d7619112` |
| `two_collision.pdf` | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| `native-source.zip` | 1914215 | `a7e395201f892bb7fc0754b964ab01b9d7be4ab047cd6ad658e22317b17ea272` |

The corresponding computed Git blob IDs are retained in `EVIDENCE.json`. This table records checks of the downloaded products; it should not be misread as an independent rerun of the author's entire publication-attestation workflow.

## 4. Rebuild and test commands

The following commands were executed against the downloaded source. In the recipe, `SOURCE` is its unpacked `source/` directory and `REVIEW` is the directory containing this review's `independent_controls.py`. They are supplied as explicit environment variables so the recipe is independent of this session's temporary paths.

```sh
: "${SOURCE:?Set SOURCE to the unpacked native-source source directory}"
: "${REVIEW:?Set REVIEW to this review directory}"
cd "$SOURCE"
python tools/check_revision_v50.py > /tmp/a2-v50-author-normal.json
python -O tools/check_revision_v50.py > /tmp/a2-v50-author-optimized.json
cmp /tmp/a2-v50-author-normal.json /tmp/a2-v50-author-optimized.json

latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex

python "$REVIEW/independent_controls.py" > /tmp/a2-v50-independent-normal.json
python -O "$REVIEW/independent_controls.py" > /tmp/a2-v50-independent-optimized.json
cmp /tmp/a2-v50-independent-normal.json /tmp/a2-v50-independent-optimized.json
```

Both complete builds succeeded, companion first. Both pairs of Python executions succeeded with byte-identical output within each pair. The independently executed author suite is **`tools/check_revision_v50.py`**, including its retained v47/v48/v49 controls; no claim is made that every historical script or every old native test was independently rerun.

The independent script ran on Python **3.13.5**, SymPy **1.14.0**. Its exact SHA-256 is `328fbe7e8b4f2a8cdeebed21114089cadb1cd4f2dd0c6a281469aebcaa340de2`; its Git blob is `6a3827f227435f2432483c618a18ad4f1f265b56`. It uses explicit exceptions rather than assertions, so `python -O` does not disable its checks.

The author suite independently returned: 106 inherited active inputs, 103 unchanged in place, exact archives of three edited originals, all 518 inherited statement/proof blocks preserved verbatim, including 243 proofs, and two new propositions with two new proofs. These are preservation facts, not mathematical correctness results.

## 5. PDF parity and direct visual scope

Every rebuilt page was compared to the corresponding native page using PyMuPDF **1.26.7** with MuPDF **1.26.12**. The comparison used both `page.get_text()` and RGB `page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csRGB, alpha=False)` including image dimensions and complete pixel arrays. It was performed on **all 263 main pages and all 7 companion pages**. There are no text or 72-dpi pixel mismatch pages.

The rebuilt PDF byte hashes are different from the native hashes:

```text
main.pdf          f1ee823e7d6a331164be9141b9f94b02d59a06a865ea436f57156757cc433a64
two_collision.pdf a386b0f73e46963932afad47b4f6b97a2310db8ca817f9adabeded3f5cf91659
```

Therefore neither byte-identical PDF reproduction nor renderer-independent visual identity is claimed. The stronger statement supported here is all-page equality of the specified extracted text and the specified same-renderer pixels.

Direct visual inspection at 108 dpi covered **main pages 5, 18, 44, 46, 82 and 83**, and **companion pages 1 and 7**. These are samples, not a claim of human-style visual inspection of all 270 pages. In particular, the new relative-normalization display and both new propositions were viewed in the delivered composition.

The final main log contains three underfull-box notices, no overfull box and no unresolved-reference or citation warning. The companion has neither underfull nor overfull boxes and no unresolved-reference or citation warning. Both logs contain the expected `epstopdf` warning that shell escape is disabled. These notices do not establish a theorem defect.

## 6. Independent finite controls and their limitations

The exact-arithmetic controls cover the alternating reference twist and normalized cofactor for lengths 1–10; determinant-one signed contact matrices and boundary/interior multiplicities for orders 3–12; a noncommuting three-by-three moving-reference derivative; four-density amplitude cancellation and the signed scalar-anchor derivative at five signed points; and symbolic all-lattice determinant identities and exact inequalities for the two-branch example.

Negative controls detect the invalid use of an absolute error as a relative bound, the wrong interior multiplicity, omission of the moving inverse derivative, and a radial assumption for the new channel. Perturbed matrices are algebraic controls, not asserted realizations of actual billiards. The finite determinant identity does not prove trace-class convergence; the finite derivative identity does not prove infinite-operator differentiability; the finite jet controls do not prove an order-uniform analytic inverse.

For the exact original two-point fiber, the new deterministic separator control gives threshold approximately `1.3065629648763766`, strict permissible additional-gap error approximately `0.339196100146197`, and actual-segment clearance lower bound approximately `0.18068343236508977`. The exact radical expressions and scope are given in the report and script. This is not a result on noisy perturbations of the original laws or a requested new manuscript theorem. `EVIDENCE.json` records the complete independently generated control output.

## 7. Primary literature checked

The following primary arXiv records were rechecked on September 15, 2026. Version identifiers are part of the citation. This is a targeted observation-model comparison, not an exhaustive priority investigation or a fresh full proof audit of these outside papers.

**L1.** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), submitted October 21, 2025. The latest version visible in the checked record was v1. The comparison concerns finite-horizon Sinai billiards, the enriched marked length spectrum and the isometry conclusion. Relevant primary PDF pages were also inspected.

**L2.** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), August 17, 2022. The comparison preserves the analytic open-billiard, non-eclipse, symmetry and genericity qualifications. It does not identify that observation with the present fixed-offset conditional law.

**L3.** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), June 3, 2021. The v5 record explicitly reports removal of an earlier geometric spectral-rigidity assertion affected by an error while retaining dynamical conjugacy results. The reviewed A2 source does not rely on the removed assertion.

No reduction in information content between these marked-length records and the manuscript's signed conditional laws was established in this review. Neither priority nor a stronger-than-literature claim is inferred just from different assumptions.

## 8. Scope statement

The machine-readable evidence deliberately sets `mathematical_certification` to `false`. The report gives bounded technical findings and an expressly nonbinding contribution judgment. No newly established fatal error is reported in its fresh proof coverage. This is not a certificate for all inherited mathematics and not a forecast of a particular editor's decision. The report and evidence should travel together so that the coverage limitations are not lost when the recommendation is quoted.
