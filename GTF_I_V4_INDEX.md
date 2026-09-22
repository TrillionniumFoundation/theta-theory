# General Theta Foundations I — fourth revision

**Author:** Qian Qi. **Date:** 22 September 2026.
**Complete manuscript:** [paper.pdf](papers/GTF-I-v4/paper.pdf), 64 pages.

Revision branch: `revision/general-theta-foundations-i-v4-2026-09-22`.
The referee-ready branch is frozen separately after the published artifact is checked.

## Read this edition

| Material | Location |
|---|---|
| Integrated manuscript | [paper.pdf](papers/GTF-I-v4/paper.pdf) |
| Native TeX | [main.tex](papers/GTF-I-v4/main.tex) |
| Every v3 objection and technical comment | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v4/RESPONSE_TO_REFEREE.md) |
| Statements, assumptions and proof dependencies | [PROOF_LEDGER.md](papers/GTF-I-v4/PROOF_LEDGER.md) |
| Entire eleven-paper pipeline and modern A1/A2 context | [HISTORY_AUDIT.md](papers/GTF-I-v4/HISTORY_AUDIT.md) |
| Theorem-level primary literature comparison | [LITERATURE_AUDIT.md](papers/GTF-I-v4/LITERATURE_AUDIT.md) |
| Hash-bound complete rebuild archive | [COMPILED_SOURCES.zip](papers/GTF-I-v4/evidence/COMPILED_SOURCES.zip) |
| Executed evidence | [BUILD_RECEIPT.json](papers/GTF-I-v4/evidence/BUILD_RECEIPT.json) |

## Mathematical revision

Theorem 2.2 gives a posterior-orbit converse for noisy renewal observations and an Nn+1-state realization of an N-centre depth-n code. Corollary 2.3 identifies the causal quantization exponent under stretched-exponential renewal tails. Proposition 2.4 treats autonomous shift closure, and Example 2.5 separates orbit quantization from same-cardinality realizability.

Theorem 3.1 gives matched bounds for noisy expanding torus experiments in every dimension with bounded mean residual renewal life. Corollaries 3.3–3.4 separate the noise floor and establish the uniform expansion–renewal critical crossover. Proposition 3.5 transfers the experiment to conjugate nonconstant-slope maps.

Theorem 4.1 proves global and separated-cluster minimax laws for calibrated observations of colliding-root moments. Lemmas 4.2–4.3 derive the singular modulus and matching alternatives from Newton identities and polynomial root geometry.

All v3 quantitative bodies, the v2 quantitative body, and the first-edition foundational proofs remain in the compiled article. Previous source editions and reviews are not modified. No unresolved historical spectral, LDP, operator or phase theorem is used as a premise.

## Exact source and executed build

- Controlling v3 review commit: `d084e3cf505f3978ddaab9b954aac94b97fe7bd3`.
- Native mathematical source commit: `29475ad3c5ff9b7c694e282a3d69e3f3de34483c`.
- GitHub Actions run: `35697115807`.
- PDF SHA-256: `dda5a1df4f2601f24852cd91e2a37af3d9af374ef90f637319371a57da3425bd`.
- Complete source archive SHA-256: `62c49fc1d3f16afb1ba6e3f02e12285692abddddb59e28393acfa57ec24ee4e3`.
- TeX passes: 3; retained resolved mathematical labels: 160.
- Complete archive input files: 56.
- Ordinary and optimized diagnostics agree; four negative controls rejected in both modes; inherited v1/v2/v3 diagnostics passed.
- No unresolved references or overfull boxes; preserved historical source trees checked against their pinned Git identities.

Build evidence identifies and checks the submitted object. It is not a formal proof certificate, independent referee approval, or journal acceptance. The publication commit is the commit containing this index and the generated PDF; the mathematical source commit above is its separately recorded predecessor.
