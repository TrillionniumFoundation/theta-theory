# General Theta Foundations I — fifth intrinsic revision

**Author:** Qian Qi. **Date:** 22 September 2026.
**Complete preserved article:** [paper.pdf](papers/GTF-I-v5-intrinsic/paper.pdf), 74 pages.
**Same-source principal reading edition:** [principal-paper.pdf](papers/GTF-I-v5-intrinsic/principal-paper.pdf), 21 pages.

Working branch: `revision/general-theta-foundations-i-v5-intrinsic-2026-09-22`.
A separate referee snapshot is frozen after the downloaded publication is checked.

This edition responds to the v4 referee report, not merely the preceding v3 report. The full article retains all preceding mathematical bodies; the principal reading edition compiles the same new proofs and their full causal dependencies.

## Read this edition

| Material | Location |
|---|---|
| Complete article | [paper.pdf](papers/GTF-I-v5-intrinsic/paper.pdf) |
| Principal argument | [principal-paper.pdf](papers/GTF-I-v5-intrinsic/principal-paper.pdf) |
| Native TeX and build instructions | [README.md](papers/GTF-I-v5-intrinsic/README.md) |
| Every current referee objection | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v5-intrinsic/RESPONSE_TO_REFEREE.md) |
| Proof dependencies and quantifiers | [PROOF_LEDGER.md](papers/GTF-I-v5-intrinsic/PROOF_LEDGER.md) |
| Historical pipeline consultation | [HISTORY_AUDIT.md](papers/GTF-I-v5-intrinsic/HISTORY_AUDIT.md) |
| Primary-literature comparison | [LITERATURE_AUDIT.md](papers/GTF-I-v5-intrinsic/LITERATURE_AUDIT.md) |
| Complete standalone source archive | [COMPILED_SOURCES.zip](papers/GTF-I-v5-intrinsic/evidence/COMPILED_SOURCES.zip) |
| Executed checks | [BUILD_RECEIPT.json](papers/GTF-I-v5-intrinsic/evidence/BUILD_RECEIPT.json) |

## Principal mathematical changes

Theorem 2.1 identifies optimal causal risk and weighted-orbit quantization with a directly constructed greedy cylinder profile for separated nonlinear expanding repellers with stationary Gibbs laws. Lemma 3.4 proves exact suffix closure of the whole greedy tree, using (bL-1)/(b-1) states for L leaves, rather than a logarithmic age expansion.

Theorem 2.2 computes the exponent from two pressure roots: spatial contraction and acquisition survival. Corollary 4.2 gives entropy/energy ratios, Proposition 4.3 gives certified finite-cylinder pressure enclosures, and Corollary 4.4 gives Perron-root formulas for nonuniform Markov branches. Example 4.5 has genuinely nonlinear branches and unequal fixed-point multipliers.

Theorem 5.1 treats hidden state persisting across acquisitions through a stationary minorized transition, with general observation kernels. Corollaries 5.2 and 5.3 transfer the intrinsic pressure law and the noisy expanding profile. The proof does not replace the full dependent posterior by the latest-observation posterior.

The complete article preserves the earlier root-collision, calibration, filtering, control and foundational proofs. The principal edition is a second reading view, not deletion of these results. No unresolved historical spectral, LDP, kinetic, operator or phase gate is asserted to be proved by preservation.

## Exact source and build

- Controlling review: `aba384e8bbadd36b4ce27a2c932c1a9cb5e63b53`.
- Native mathematical source commit: `90c525c2ddc78475f9fe3d8a0972bb3792e51674`.
- GitHub Actions run: `35715066917`.
- Complete PDF SHA-256: `b13735539cdb0b1fa0272c6c67aaffda8835be54ea57494fa016e60c13585a01`.
- Principal PDF SHA-256: `d77c10f13287dbe471b524281926efb7a3f779837687ac0636adc8b535925608`.
- Source archive SHA-256: `ce84fc65bde164dd9668af39791cd4083d13984cc9d7c7c4cc2c0d8992acf8b0`.
- Archive inputs: 78; retained mathematical labels: 217; shared core labels: 95.
- Finite deterministic checks: 32431. Ordinary and optimized runs agree; five wrong variants are rejected in both modes.
- Both editions compile in three stable passes, with no undefined references or overfull boxes. The core statement numbers agree between editions. All inherited diagnostic suites pass.

The publication commit containing this index is separate from the mathematical source commit above. Build and finite-regression records identify the submitted object; they are not a formal proof certificate, independent referee approval, priority determination, or journal acceptance.
