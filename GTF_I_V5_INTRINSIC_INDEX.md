# General Theta Foundations I — fifth intrinsic revision

**Author:** Qian Qi. **Date:** 22 September 2026.  
**Complete preserved article:** [paper.pdf](papers/GTF-I-v5-intrinsic/paper.pdf), **74 pages**.  
**Same-source principal reading edition:** [principal-paper.pdf](papers/GTF-I-v5-intrinsic/principal-paper.pdf), **21 pages**.  
**Working branch:** `revision/general-theta-foundations-i-v5-intrinsic-2026-09-22`  
**Referee snapshot branch:** `revision/general-theta-foundations-i-v5-intrinsic-referee-ready-2026-09-22`

This revision responds to the v4 referee report at `aba384e8bbadd36b4ce27a2c932c1a9cb5e63b53`, which reviewed the v4 snapshot `d7c94af2a1e0521cdb9c3dddd1b8bc86ec8e86b1`. The new proofs address intrinsic orbit complexity, finite-state realizability, nonconstant metric expansion and persistent hidden memory. They do not merely repeat the response to the older v3 report.

## Start the next referee pass here

| Material | Location and purpose |
|---|---|
| Principal reading edition | [principal-paper.pdf](papers/GTF-I-v5-intrinsic/principal-paper.pdf): the complete new causal-memory chain and all retained causal proofs it invokes |
| Complete article | [paper.pdf](papers/GTF-I-v5-intrinsic/paper.pdf): the same chain plus all preceding quantitative and foundational theorem/proof bodies |
| Native TeX and build | [README.md](papers/GTF-I-v5-intrinsic/README.md), [main.tex](papers/GTF-I-v5-intrinsic/main.tex), [principal.tex](papers/GTF-I-v5-intrinsic/principal.tex) |
| Point-by-point reply | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v5-intrinsic/RESPONSE_TO_REFEREE.md): E1–E7, Sections 11–15, and proposed routes A–E of the controlling report |
| Proof dependencies | [PROOF_LEDGER.md](papers/GTF-I-v5-intrinsic/PROOF_LEDGER.md): hypotheses, actual proof work, quantifiers and constant dependence |
| Entire-pipeline consultation | [HISTORY_AUDIT.md](papers/GTF-I-v5-intrinsic/HISTORY_AUDIT.md) and [HISTORY_INPUT_MANIFEST.json](papers/GTF-I-v5-intrinsic/HISTORY_INPUT_MANIFEST.json) |
| Primary-literature comparison | [LITERATURE_AUDIT.md](papers/GTF-I-v5-intrinsic/LITERATURE_AUDIT.md) |
| Complete standalone source archive | [COMPILED_SOURCES.zip](papers/GTF-I-v5-intrinsic/evidence/COMPILED_SOURCES.zip): 78 exact repository-relative inputs |
| Executed build | [BUILD_RECEIPT.json](papers/GTF-I-v5-intrinsic/evidence/BUILD_RECEIPT.json) |
| Independent publication verification | [GTF_I_V5_INTRINSIC_RENDER_REVIEW.json](GTF_I_V5_INTRINSIC_RENDER_REVIEW.json) |

## Main mathematical revision

| Statement | Principal / complete page | Content |
|---|---:|---|
| Theorem 2.1 | 5 / 7 | Matched intrinsic greedy-cylinder profile for weighted-orbit quantization and optimal causal risk on separated nonlinear expanding repellers with stationary Hölder Gibbs laws |
| Lemmas 3.1–3.3 | 6–7 / 8–9 | Physical cylinder separation, balanced energy tree and arbitrary off-image Hilbert-centre lower bounds |
| Lemma 3.4 | 8 / 10 | Exact suffix closure of the full greedy tree; exactly `(bL-1)/(b-1)` states for L leaves, hence `2L-1` for binary branching |
| Theorem 2.2; Lemma 4.1 | 5, 9 / 7, 11 | Orbit partition pressure equals the maximum of spatial and survival pressures; exponent is derived rather than assumed |
| Corollary 4.2; Proposition 4.3 | 10 / 12 | Entropy/energy variational formulas and certified finite-cylinder pressure enclosures |
| Corollary 4.4; Example 4.5 | 11 / 13 | Positive-Markov Perron-root formulas, unequal branch contractions and an explicit genuinely nonlinear family |
| Theorem 5.1 | 12 / 14 | Conditional-minorization comparison with hidden state persisting across acquisitions and general observation kernels |
| Corollaries 5.2–5.3 | 13 / 15 | Intrinsic pressure law and noisy expanding profile with retained hidden memory |

Theorem 2.1 proves `c G_M(q) <= e_M^2(Z_q) <= R_M <= C G_M(q)`. The lower bound covers arbitrary randomized, time-dependent finite-register observers; the upper construction is a stationary deterministic machine. The tree has exact suffix closure, so no logarithmic age multiplier is introduced.

With `P(phi)=0` and the logarithmic inverse-derivative potential `psi`, Theorem 2.2 derives the roots `P(s_g phi+2s_g psi)=0` and `P(s_t phi)+s_t log(q)=0`. The squared-error exponent is `(1-s_*)/s_*`, where `s_*=max(s_g,s_t)`, and the threshold is `q_c=exp(-P(s_g phi)/s_g)`. These are intrinsic quantities of the branch geometry, stationary law and acquisition survival. The finite profile is matched for every budget; the pressure formula alone is not represented as a universal optimal leading constant or universal critical logarithm.

Theorem 5.1 permits invariant `Q(x,.) >= epsilon mu(.)`, including `(1-epsilon)delta_{Tx}+epsilon mu`. The refresh coin is not observed, and full hidden state may persist across acquisitions. Its proof dominates the actual conditional law rather than equating it to the independent law. The single-acquisition reference term is not incorrectly identified with the dependent full-history Bayes floor.

The two PDFs are coordinated views of one native source, not incompatible revisions. All old mathematical bodies remain in the complete edition, including the root-collision, exact calibration quotient, HMM, control and foundational results. Both views contain the full posterior-orbit and noisy expanding proofs needed by the new chain. All **217 retained mathematical labels** resolve; **95 shared core labels** have identical numbers between views. Previous source editions, introductions and review records are untouched.

## History and literature

The consultation manifest records all eleven historical components, the master programme and implementation addendum, selected native history/pressure arguments, and the modern A1-v37/A2-v112 source editions with exact ranges and hashes. It does not claim that all historical archive files were reread word for word. The new pressure theorem uses no unresolved Sinai spectral/local-limit, particle LDP, nonlinear-semigroup, common unbounded-operator-domain or physical-phase theorem as a premise.

The new introduction compares directly with Linder–Yüksel (2014), Wood–Linder–Yüksel (2017, Theorem 3), Luschgy–Pagès (2004), and Roychowdhury (2014). Classical Gibbs pressure is attributed to Bowen and greedy variable-to-fixed trees to Tunstall. The literature audit distinguishes full primary-text checks from publication-record or indirect bibliographic checks.

## Exact identities and executed verification

- Controlling review commit: `aba384e8bbadd36b4ce27a2c932c1a9cb5e63b53`.
- Native mathematical source commit: `90c525c2ddc78475f9fe3d8a0972bb3792e51674`.
- PDF/evidence publication commit: `de7544e1735d50bf2cced7d68727b934cba4a578`.
- Successful GitHub Actions run: `35715066917`.
- Complete PDF SHA-256: `b13735539cdb0b1fa0272c6c67aaffda8835be54ea57494fa016e60c13585a01`.
- Principal PDF SHA-256: `d77c10f13287dbe471b524281926efb7a3f779837687ac0636adc8b535925608`.
- Source archive SHA-256: `ce84fc65bde164dd9668af39791cd4083d13984cc9d7c7c4cc2c0d8992acf8b0`.

Both PDFs compiled in three stable TeX passes, with no unresolved references or overfull boxes. All **32431 finite deterministic checks** passed; ordinary and optimized runs agree. Five incorrect variants were rejected in both modes. All inherited v1/v2/v3/v4 diagnostic suites passed. Preserved legacy, A1-v37 and A2-v112 Git tree identities were checked against the exact native source commit.

All **78 downloaded source inputs** match the locally authored or inherited bytes. A fresh archive-only rebuild passed independently. All **74 complete-edition pages and 21 principal-edition pages** agree pixel for pixel with the locally inspected editions at 90 dpi. Remote and local PDF container bytes differ; no byte-identical cross-environment PDF claim is made. The full page overviews and selected full-size proof pages were visually inspected.

The final referee snapshot adds only this index and the rendering-verification record to the publication commit. It changes neither compiled mathematical input nor published PDF. Main, previous reviews/revisions and the pre-existing plain v5 branch are not updated by this revision.

This edition is supplied for independent mathematical refereeing. New proofs, not diagnostic counts, answer the substantive objections. No formal proof certificate, independent approval, priority determination, closure of unrelated historical hard gates, or four-journal acceptance is claimed.
