# General Theta Foundations I — fourth revision

**Complete manuscript:** [papers/GTF-I-v4/paper.pdf](papers/GTF-I-v4/paper.pdf), 64 pages.  
**Author:** Qian Qi. **Date:** 22 September 2026.  
**Revision branch:** `revision/general-theta-foundations-i-v4-2026-09-22`  
**Referee snapshot branch:** `revision/general-theta-foundations-i-v4-referee-ready-2026-09-22`

This revision responds to the latest v3 report at `d084e3cf505f3978ddaab9b954aac94b97fe7bd3`, not merely the older v1 report. It continues the v3 referee snapshot and preserves all prior source editions and review records.

## Start the next referee pass here

| Material | Location and purpose |
|---|---|
| Integrated article | [paper.pdf](papers/GTF-I-v4/paper.pdf): new principal results, complementary quantitative development, full foundational proofs |
| Native mathematical source | [main.tex](papers/GTF-I-v4/main.tex), [README.md](papers/GTF-I-v4/README.md) |
| Point-by-point response | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v4/RESPONSE_TO_REFEREE.md): E1–E7, M1–M7, technical comments 19.1–19.6 and routes A–E |
| Proof dependencies | [PROOF_LEDGER.md](papers/GTF-I-v4/PROOF_LEDGER.md): assumptions, proofs, constants and precise scope |
| Entire-pipeline consultation | [HISTORY_AUDIT.md](papers/GTF-I-v4/HISTORY_AUDIT.md), [HISTORY_INPUT_MANIFEST.json](papers/GTF-I-v4/HISTORY_INPUT_MANIFEST.json) |
| Theorem-level literature | [LITERATURE_AUDIT.md](papers/GTF-I-v4/LITERATURE_AUDIT.md) |
| Complete standalone source archive | [COMPILED_SOURCES.zip](papers/GTF-I-v4/evidence/COMPILED_SOURCES.zip): 56 exact repository-relative inputs |
| Executed build | [BUILD_RECEIPT.json](papers/GTF-I-v4/evidence/BUILD_RECEIPT.json) |
| Downloaded-artifact and rendering verification | [GTF_I_V4_RENDER_REVIEW.json](GTF_I_V4_RENDER_REVIEW.json) |

## Principal mathematical changes

| Result | Page | Content |
|---|---:|---|
| Lemma 2.1; Theorem 2.2 | 7 | Standard Borel kernel realization; posterior-orbit lower bound for arbitrary randomized, time-dependent machines; explicit Nn+1-state realization of an N-centre depth-n orbit code |
| Corollary 2.3; Proposition 2.4; Example 2.5 | 8–9 | Equality of quantization exponents under stretched-exponential renewal tails; autonomous shift closure; exact separation between static orbit quantization and same-cardinality causal realization |
| Theorem 3.1; Lemma 3.2 | 10–11 | Matching noisy expanding-torus risk bounds in every dimension for renewal laws with bounded mean residual life; lower bounds are not restricted to interval or suffix quantizers |
| Corollaries 3.3–3.4; Proposition 3.5 | 11–13 | Noise-floor/memory decomposition, uniform critical crossover, and transfer to conjugate nonconstant-slope maps |
| Theorem 4.1; Lemmas 4.2–4.3 | 14–16 | Global and separated-cluster minimax laws for calibrated colliding-root moments; contact exponents derived from Newton identities and root geometry, with matching testing alternatives |

The general realization theorem preserves exponents rather than asserting a universal same-cardinality constant-factor converse. The expanding theorem supplies the sharp constant-factor bounds in its stated class. The critical-window result identifies the universal profile and the explicit suffix machine's coefficient, not an unproved optimal leading constant. The collision theorem does not assume a global two-sided contact law.

All v3 quantitative bodies, the v2 quantitative body, and first-edition foundational proofs are present in the compiled article. The old editions remain independently available. Their 160 retained mathematical labels resolve. The integrated manuscript contains 23 theorem, 13 lemma, 17 proposition, 7 corollary, 60 proof and 14 example environments. Counts and preservation are not significance claims.

## Source, publication and verification identities

- Controlling review: `d084e3cf505f3978ddaab9b954aac94b97fe7bd3`.
- Native mathematical source commit: `29475ad3c5ff9b7c694e282a3d69e3f3de34483c`.
- Generated PDF/evidence publication commit: `c379f2af73a0f7e29f7b9a63da605f2b92384853`.
- Successful GitHub Actions run: `35697115807`.
- PDF SHA-256: `dda5a1df4f2601f24852cd91e2a37af3d9af374ef90f637319371a57da3425bd`.
- Complete source archive SHA-256: `62c49fc1d3f16afb1ba6e3f02e12285692abddddb59e28393acfa57ec24ee4e3`.

Three TeX passes stabilized all references. There are no unresolved references or overfull boxes. All 3037 finite deterministic regressions passed; ordinary and optimized runs agree. Four negative controls are rejected in both modes. Inherited v1/v2/v3 diagnostics passed. Preserved legacy and modern A1-v37/A2-v112 trees were checked against pinned Git identities, and no earlier paper edition or review changed.

All 56 downloaded source files match the locally authored or inherited bytes. A fresh archive-only rebuild passed independently. All 64 downloaded publication pages agree pixel for pixel with the locally inspected edition at 100 dpi. PDF container bytes differ between the remote and local builds; this is not presented as byte-identical PDF reproduction. All page overviews and selected full-size proof pages were visually inspected.

The final snapshot adds only this handoff index and the rendering-verification record to the publication commit. It does not change any compiled input or the published PDF. Main, old review branches, and previous revision branches are not updated.

This edition is submitted for further mathematical refereeing. Its new proofs, rather than its build receipts, address the substantive objections. No independent referee approval, formal proof certificate, closure of unrelated historical hard gates, or four-journal acceptance is claimed.
