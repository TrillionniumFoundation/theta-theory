# General Theta Foundations I — Revision 81: referee entry

**Primary article:** *Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements*  
**Revision directory:** `papers/GTF-I-v81-finite-risk-certificates`  
**Date:** 5 October 2026

Revision 81 supplies finite rational certificates for the uniform risk of a common learner on the fixed interior of the ordered binary effect body. It preserves the preceding geometry, entropy, learning, coding and structural results. The primary article consolidates repeated introductory and comparison material while retaining the earlier sources and proofs.

## 1. Frozen inputs and review identity

| Object | Exact identity |
| --- | --- |
| Revision 81 native source | `ed70f20a5d1b54a73cb5cd2e50d334c1cc3b357d` |
| Native source tree | `1a3c7aff64d4f78e7074d618e3ee23bcab896d33` |
| Native inventory | 438 files; `evidence/SOURCE_HASHES.json` identifies their contents |
| Immediate predecessor, completed v80 | `31ac2a70a0304a1fe0cafd44a686584e4b8d9be9` |
| Predecessor native source | `98a5cf437ef908bac876902bdb52b53958e30e7c` |
| Controlling external report, R51 | `96a3666ed516ea12fcdb8ede341b7082e4ff2c78` |
| Controlling proof/pipeline audit, R51 | `d01b5b4d48955e8c6f0c5592213b8628e12a66dd` |
| Object examined by those reports, v77 | `5650842e0bc89ca6a8b6d6730115784f0d9ecc12` |
| Revision 81 publication commit | The publication commit containing this entry; its sole parent is the native source above |
| Exact submitted review head | The same containing publication commit; the exact-head run is keyed to that SHA |

R51 remains the latest deposited controlling review. It examined v77; no review of v78–v81 is inferred from it. Its full recommendation and technical comments are preserved in `FROZEN_R51_REPORT.md` and `FROZEN_R51_PIPELINE_AUDIT.md`; `CONTROLLING_REPORTS.json` supplies the original paths, blobs and hashes. The requested Annals/Inventiones/JAMS/Acta objective is retained. No editorial acceptance or independent human priority clearance is represented as obtained.

## 2. The additional mathematical contribution

The inherited theory already gives the joint interior learning order

\[
 M=\Theta\!\left(N\delta^{-2}[d^2+d\log(1/\eta)]\right)
\]

and public description length

\[
 B=\frac{d^2}{2}\log_2N+d^2\log_2(1/\delta)+O(d^2).
\]

It also provides an algebraic collective readout selected by real quantifier elimination. These statements, their proofs and their attribution remain active. Mele–Bittel supplies the statistical upper estimator used in the existence argument; the new section does not claim a new tomography primitive.

Source Section 64 adds a second construction with three explicit components:

1. **Finite-certificate soundness.** The normalized Choi records satisfy `||Gamma_m(E)-Gamma_m(G)||_1 <= 2m ||E-G||op`. Complete risk inequalities on a proved rational `r`-net, with radius `a` and failure `alpha`, imply radius `a+r` and failure `alpha+mr` for every real target. The proof transfers the fixed good-label set at a nearby grid point and accounts for both buffers.
2. **A prescribed rational readout.** A positive mixture, rounding of the first `L-1` components and an exact residual last component produce legal Gaussian-rational conditional POVMs with denominator `Q=ceil(64 L^2 d^m/eta)`. Normalization and positivity hold for every classical conditioning string. The complete output-index variation is at most `3eta/32`.
3. **A terminating search at the same query order.** Each dyadic stage `m=1,2,4,...` exhausts a prescribed finite list and checks every grid inequality exactly. Statistical existence with strict slack makes every `m>=m0` feasible; ignored extra records allow padding. Hence the first accepted stage has `M<=2m0`. The rational readout and its certificate are computed before any unknown-device call.

The theorem applies to integers `d,N>=1`, rational `0<delta<=2^-13` and rational `0<eta<=1/8`, on `I/4 <= E <= 3I/4`. The ideal certificate gives future loss at most `5delta/8` except with probability `5eta/16`. The stated finite trusted-control budget gives actual risk at most `13eta/16 < eta` for the original event `d_N(E,C)>delta`.

## 3. Reading map

The following locations are verified against the production `evidence/THEOREM_LOCATIONS.json`.

| New result | Focused article | Complete edition | Source label |
| --- | --- | --- | --- |
| Uniform validity of finite certificates | Theorem 13.1, p. 53 | Theorem 63.1, p. 195 | `thm:finitecertificate81` |
| Rational approximation of a finite readout | Proposition 13.2, p. 54 | Proposition 63.2, p. 196 | `prop:rationalreadout81` |
| Certified effective learning at the joint rates | Theorem 13.3, pp. 54–55 | Theorem 63.3, pp. 197–198 | `thm:rationallearner81` |

All three statements are in `sections/64-finite-risk-certificates.tex`. `FINITE_RISK_PROOF_AUDIT.md` gives their proof crosswalk. `FINITE_RISK_SCHEMA.md` specifies exact replay, equality handling, full-grid reconstruction and incomplete-search behavior.

The current manuscript objects are `paper.pdf` (focused article), `STRUCTURAL_PAPER.pdf` (independent structural companion), and `COMPLETE_REVISION.pdf` (complete preserved development). The production receipts confirm **74 / 41 / 214 pages**, respectively. Printed numbering differs between editions; source Section 64 is focused Section 13 and complete Section 63.

## 4. Access, resources and executable scope

The device is memoryless, ordered binary, input-consuming and classical-output, with no residual quantum system returned by the device. Acquisition uses independent one-call probe–reference pairs. Collective processing acts only on completed outputs. The public deterministic dictionary and decoded word are inherited unchanged.

The query and payload orders above have absolute constants on the stated interior. At stage `m`, the reference dimension is `d^m`; all `2^m` classical strings have specified readouts. The parameter enumeration has at most `(2K_m+1)^(d^2)` tuples, and the readout enumeration at most `(2Q_m+1)^((L-1)2^m d^(2m))`. These are finite constructions; no polynomial-time synthesis, optimized workspace or gate-count bound is asserted. Nonpublic headers are charged separately.

`finite_risk_certificate.py` verifies a supplied dictionary and rational readout against the complete regenerated grid. Its replay does not reconstruct the optimal dictionary or execute the general optimal-learner search. The recorded scalar certificates and higher-dimensional local checks have the scope stated in `FINITE_RISK_SCHEMA.md`; physical acquisition is not claimed. The analytic transfer theorem supplies the continuous-parameter implication of the exact finite inequalities.

## 5. Response and preservation

`RESPONSE_TO_REFEREE.md` maps all **12 required revisions, 26 detailed comments, 32 pipeline gates and 10 risks** in R51. It distinguishes inherited answers from the new finite-certificate result. `LITERATURE_AUDIT.md` retains the theorem-level source comparisons; `INDEPENDENT_REVIEW_BRIEF.md` adds the new overlap and correctness questions. Independent human priority assessment remains open as **R02/P01**.

The v80 baseline comprises 410 native files and 787/289/116 complete/focused/structural labels. Changed originals are archived under `predecessor-v80-audit/`; all 64 inherited section sources, including both bibliographies, remain byte-identical. Preservation manifests identify the retained sources and active proof labels. The structural companion remains a separate theorem object.

The full historical account and the frozen A/B/C/D ledgers are preserved. Their noncircular routes remain `A2 -> A3 -> A4 -> C2 -> D1` and `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`, with A1 independent. The finite measurement certificate neither assumes nor discharges their model-specific analytic gates. The five aggregate flags—`historical_A2_replacement`, `B4_aggregate`, `C2_aggregate`, `eleven_paper_aggregate`, `whole_Theta_program`—remain false.

## 6. Submitted files and executed verification

| File | Contents |
| --- | --- |
| [paper.pdf](papers/GTF-I-v81-finite-risk-certificates/paper.pdf) | 74-page focused article |
| [STRUCTURAL_PAPER.pdf](papers/GTF-I-v81-finite-risk-certificates/STRUCTURAL_PAPER.pdf) | 41-page independent structural companion |
| [COMPLETE_REVISION.pdf](papers/GTF-I-v81-finite-risk-certificates/COMPLETE_REVISION.pdf) | 214-page complete preserved development |
| [RESPONSE_TO_REFEREE.md](papers/GTF-I-v81-finite-risk-certificates/RESPONSE_TO_REFEREE.md) | Complete R51 crosswalk |
| [evidence/JOURNAL_PACKAGE.zip](papers/GTF-I-v81-finite-risk-certificates/evidence/JOURNAL_PACKAGE.zip) | Both standalone articles, their source graphs, response and verifier |
| [evidence/RESEARCH_PACKAGE.zip](papers/GTF-I-v81-finite-risk-certificates/evidence/RESEARCH_PACKAGE.zip) | Complete sources, all three PDFs and core build evidence |
| [evidence/BUILD_RECEIPT.json](papers/GTF-I-v81-finite-risk-certificates/evidence/BUILD_RECEIPT.json) | Source-qualified production and isolated reconstruction |
| [evidence/VISUAL_REVIEW.json](papers/GTF-I-v81-finite-risk-certificates/evidence/VISUAL_REVIEW.json) | 23 inspected pages and matching production-render identities |

The qualified build used the exact native commit above. It executed all 19 registered regression suites under ordinary and optimized Python with identical outputs, reconstructed the complete native archive in isolation, and independently rebuilt both journal articles without repository dependencies. Every reconstructed page text and raster matched. The unchanged structural companion retains all 41 predecessor page signatures.

The new finite-risk suite executed 150 checks and 27 negative controls. Two complete scalar certificates cover 82 independently checked grid points. The resolving example certifies all-real operator radius `5/32` and failure bound `106041021/134217728`; it is explicitly a diagnostic example of the general transfer assertion. Complete higher-dimensional optimal synthesis was not executed.

There are no unresolved references or citations and no underfull or overfull boxes in the submitted documents. Raw font-engine warnings are retained separately in the LaTeX logs and the build receipt. Twenty-three selected pages were inspected visually, including all new focused proof pages and both comparison-table pages; no rendered defects were found. This is selected-page visual review, supplemented by every-page reconstruction.

**Native source inventory SHA256:** `8e49efa63ed1eaefb7b7c6f9f4cf8d0aa2dfb7c7cb79dc8ddaf067abcfbd549b`.

| PDF | Pages | SHA256 |
| --- | ---: | --- |
| `COMPLETE_REVISION.pdf` | 214 | `d41eb0e1927891af4e56c24fc15a33cee6d813a5a85b941f2b6ef04f340944bb` |
| `STRUCTURAL_PAPER.pdf` | 41 | `5370d03b1d02d1ac99906afb05688edf01bbcb0d0635039c62a307ceb8e8b0ab` |
| `paper.pdf` | 74 | `406baa34ce78f80464365e71f02a67519af0db7ee1d56bdf536e892dd82bd407` |

### Exact publication-head reconstruction

The publication is required to be a direct, single-parent child of the qualified native source. The read-only [v81 exact-head workflow](.github/workflows/gtf-i-v81-exact-head.yml) checks that ancestry, verifies the unchanged workflow and all predecessor bytes, reconstructs the three documents and both journal articles, and compares current finite evidence. Its triggering commit SHA and actual conclusion are available in [GitHub Actions](https://github.com/TrillionniumFoundation/theta-theory/actions/workflows/gtf-i-v81-exact-head.yml). No predecessor run is used to qualify this publication. The run result is kept as an Actions artifact, without adding a post-publication commit that would break the direct-source-child condition.

Reconstruction establishes the stated source and artifact identity. Finite replay establishes its checked hypotheses; the written transfer theorem gives their uniform mathematical interpretation. Independent priority assessment and the next referee judgment remain external to these execution records.
