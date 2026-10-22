# Current native proof navigation

This derived navigation aid records current reference numbers and actual PDF destinations. It is not a proof certificate, independent referee endorsement, or a claim that the original raw pointwise local limit theorem is complete.

## Exact current compiled identity

- Native PDF: `build/typeset-final-norm/native/main.pdf` (255 pages).
- PDF SHA256: `60b08184ad7bfa001aae76deb98d99062212cc647723a8e096485e89861df6f5`.
- Current `main.tex` SHA256: `251d44ddb3e56b4f88b277ff1f333946b668abaeb2be804e47694f0d48580f6b`.
- Final auxiliary SHA256: `a70b100d598e8757d2ac139760a30d0337a65a5e7070739081bc78371184c56e`.

The active input closure contains 84 source files, all 73 core bodies 260–332 exactly once, and 1125 unique source labels. Every label has one compiled record and an actual PDF named destination. The 6 current new bodies contain 94 labels; no inherited label count was imposed. The complete label map, source hashes, source line positions, and input edges are in `PROOF_INDEX.json`.

All pages below are one-based physical PDF pages read directly from the compiled PDF. Original auxiliary page labels and printed PDF page labels are preserved separately.

## 6 new proof bodies in actual article order

| Current native body | Actual section | Section begins on PDF page | Labels |
|---|---|---:|---:|
| `core/327_length_sensitive_physical_source_transport.tex` | 71: Length-sensitive transport of actual clearance sources | 215 | 17 |
| `core/328_localized_clearance_physical_roof_height.tex` | 72: A selected physical roof height for an actual clearance witness | 219 | 16 |
| `core/329_original_normalized_deep_clearance_payment.tex` | 73: Deep clearance at the original normalization and the same comparison pool | 224 | 15 |
| `core/330_all_label_physical_roof_variation.tex` | 74: One-copy variation of the complete exact-label vector | 228 | 7 |
| `core/331_return_tower_and_polynomial_likelihood.tex` | 75: The actual return tower and positive finite-band likelihoods | 229 | 21 |
| `core/332_endpoint_tested_marked_roof_operator.tex` | 76: Endpoint-tested marked roof operators on the actual collision chain | 234 | 18 |

## Numbered statements in the 6 current bodies

Each row locates the numbered statement. Its proof may begin or continue on later pages; no unverified proof-page range is assigned. Numbered equations and all other source labels are included in the complete JSON index.

### Section 71: Length-sensitive transport of actual clearance sources

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Theorem 71.1 | Length-sensitive physical renewal | `thm:lc-renewal` | 216 |
| Lemma 71.2 | Actual-flight clearance cover | `lem:lc-cover` | 217 |
| Theorem 71.3 | Localized half-source capacity | `thm:lc-local-half` | 218 |
| Corollary 71.4 | The selected angular source mass | `cor:lc-source-mass` | 219 |

### Section 72: A selected physical roof height for an actual clearance witness

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Lemma 72.1 | Turning on the actual selected interval covers | `lem:lc-turning` | 220 |
| Lemma 72.2 | Selected old clearance boundaries and new level boundaries | `lem:lc-selected-boundary` | 221 |
| Lemma 72.3 | Selected endpoint-cap payment by the physical Jacobian | `lem:lc-selected-cap` | 222 |
| Theorem 72.4 | Complete physical selected roof height | `thm:lc-selected-roof-height` | 223 |

### Section 73: Deep clearance at the original normalization and the same comparison pool

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Theorem 73.1 | Complete deep-clearance height and its collision payment | `thm:lc-deep-payment` | 225 |
| Theorem 73.2 | Original-height equivalence of the two shortages | `thm:lc-same-pool` | 226 |

### Section 74: One-copy variation of the complete exact-label vector

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Theorem 74.1 | Summed variation over every exact physical label | `thm:av-all-bv` | 228 |
| Corollary 74.2 | Bounded tests of the exact labels | `cor:av-label-tests` | 229 |

### Section 75: The actual return tower and positive finite-band likelihoods

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Lemma 75.1 | The conservative physical return tower | `lem:av-tower` | 229 |
| Lemma 75.2 | Exact components and a positive proof restriction | `lem:av-return-components` | 230 |
| Lemma 75.3 | The kernel and its first absolute moment | `lem:av-kernel` | 231 |
| Theorem 75.4 | Positive likelihoods on the original trajectories | `thm:av-likelihood` | 231 |
| Corollary 75.5 | The full finite-band transform uses the true law | `cor:av-exact-fourier` | 232 |
| Corollary 75.6 | Arbitrary polynomial normalized accuracy | `cor:av-polynomial` | 233 |
| Corollary 75.7 | Fixed collision count and the original $m^2$ scale | `cor:av-fixed-collision` | 233 |
| Corollary 75.8 | The actual conditional denominator | `cor:av-denominator` | 233 |

### Section 76: Endpoint-tested marked roof operators on the actual collision chain

| Actual item | Title from the compiled reference | Label | PDF page |
|---|---|---|---:|
| Lemma 76.1 | Actual Gauss derivatives of the endpoint tests and orbit phase | `lem:wo-derivatives` | 234 |
| Theorem 76.2 | Summed variation with specified smooth trajectory tests | `thm:wo-bv` | 235 |
| Corollary 76.3 | The weak marked roof operator and its actual norms | `cor:wo-fourier` | 236 |

## Actual PDF pages and auxiliary references

7 current auxiliary page labels differ from the actual destination page label. These current offsets were detected afresh; no earlier offset list was reused. The navigation uses the actual PDF page.

| Label | Auxiliary page label | Actual PDF page | Printed PDF page label |
|---|---:|---:|---:|
| `cor:dc-unique` | 39 | 40 | 40 |
| `prop:el-logomega` | 74 | 75 | 75 |
| `thm:gr-jets` | 79 | 80 | 80 |
| `thm:at-height` | 137 | 138 | 138 |
| `cor:nm-moments` | 158 | 159 | 159 |
| `thm:rbv-height` | 197 | 198 | 198 |
| `cor:v110-holder-constant` | 248 | 249 | 249 |

## Reproduction and mathematical scope

Run `python tools/build_proof_index.py` from the article directory after the final native build. The default inputs are the current native PDF and auxiliary file; `--aux` and `--pdf` select another actual build. The command fails on missing or duplicate source labels, an incomplete active core closure, or a missing PDF destination. The tool and its exact hash are recorded in the index.

Whether a statement is unconditional on pressure, uses an inherited input, or specifies an unresolved closure is determined by its complete native statement, proof, and dependency ledger. The six new bodies prove length-sensitive physical source renewal, full selected-clearance roof height, original-normalized deep clearance payment with the unchanged comparison pool, all-label variation, actual return-tower and positive finite-band likelihood estimates, and weak endpoint-tested marked roof operator estimates. All preceding full proof bodies remain inherited. The endpoint-layer same-roof shortage, strong joint spectral and arithmetic evaluation, actual microscopic conditional denominators and the final raw pointwise inverse retain their precise remaining obligations. Finite checks, compilation and this navigation are not independent mathematical certificates.
