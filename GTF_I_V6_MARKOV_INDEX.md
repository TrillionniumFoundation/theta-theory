# General Theta Foundations I — sixth Markov revision

**Author:** Qian Qi. **Date:** 22 September 2026.  
**Complete preserved article:** [paper.pdf](papers/GTF-I-v6-markov/paper.pdf), **90 pages**.  
**Same-source principal reading edition:** [principal-paper.pdf](papers/GTF-I-v6-markov/principal-paper.pdf), **18 pages**.  
**Working branch:** `revision/general-theta-foundations-i-v6-markov-2026-09-22`  
**Referee snapshot branch:** `revision/general-theta-foundations-i-v6-markov-referee-ready-2026-09-22`

This revision answers the v5 intrinsic report at `ee210f3cfe3b4923ef51310e20cd8b20a6a367e1`, report blob `2fee1ac088b7452eb87423cf36d9dca9b55e138b`, which reviewed snapshot `1fe6b459213ab86e5e49872490a1ec05eb0e0741`. The report's current E1–E7 and Sections 12–15, including proposed routes A–G, control the response.

## Start the next referee pass here

| Material | Location and purpose |
|---|---|
| Principal reading edition | [principal-paper.pdf](papers/GTF-I-v6-markov/principal-paper.pdf): complete Markov-renewal, critical, posterior and operational chains with the full retained orbit converse they invoke |
| Complete article | [paper.pdf](papers/GTF-I-v6-markov/paper.pdf): the same core, the active A2 application, and every preceding mathematical theorem/proof body |
| Native TeX and build | [README.md](papers/GTF-I-v6-markov/README.md), [main.tex](papers/GTF-I-v6-markov/main.tex), [principal.tex](papers/GTF-I-v6-markov/principal.tex) |
| Point-by-point response | [RESPONSE_TO_REFEREE.md](papers/GTF-I-v6-markov/RESPONSE_TO_REFEREE.md) |
| Proof dependencies and constants | [PROOF_LEDGER.md](papers/GTF-I-v6-markov/PROOF_LEDGER.md) |
| Historical and active-pipeline consultation | [HISTORY_AUDIT.md](papers/GTF-I-v6-markov/HISTORY_AUDIT.md), [HISTORY_INPUT_MANIFEST.json](papers/GTF-I-v6-markov/HISTORY_INPUT_MANIFEST.json) |
| Primary-literature comparison | [LITERATURE_AUDIT.md](papers/GTF-I-v6-markov/LITERATURE_AUDIT.md) |
| Standalone exact-source archive | [COMPILED_SOURCES.zip](papers/GTF-I-v6-markov/evidence/COMPILED_SOURCES.zip): 108 repository-relative inputs |
| Executed build | [BUILD_RECEIPT.json](papers/GTF-I-v6-markov/evidence/BUILD_RECEIPT.json) |
| Independent publication verification | [GTF_I_V6_MARKOV_RENDER_REVIEW.json](GTF_I_V6_MARKOV_RENDER_REVIEW.json) |

## Principal mathematical revision

| Result | Principal / complete page | Content |
|---|---:|---|
| Theorem 2.1 | 5 / 7 | Matched finite-register and weighted-orbit cylinder profile on primitive finite-type languages, with forbidden transitions, metric realizations in arbitrary dimension, delay-identifying Holder observables and nongeometric renewal laws |
| Theorem 2.2 | 6 / 8 | Intrinsic pressure exponent on the admissible language, with the exponential renewal rate as input and no assumed quantization exponent |
| Lemmas 3.1–3.4 | 6–8 / 8–10 | Strict renewal-energy suffix domination even at equal cylinder masses, charged unary nodes, controlled budget dilation, arbitrary off-image Hilbert centres and exact suffix realization |
| Corollary 4.2; Example 4.3 | 9–10 / 12 | Structural-zero-preserving Perron formulas and a planar golden-mean example with a noninjective scalar readout recovered by one delay |
| Theorems 5.1–5.2 | 10–11 / 12–13 | Critical power-log, log-log and bounded corrections; uniform finite-profile crossover for polynomially modified renewal tails |
| Theorem 6.1; Lemma 6.2; Corollary 6.3 | 12–13 / 14–15 | Matched whole-register Bayes excess through conditional posterior contraction; inward finite compander on unbounded state space; Gaussian hidden chain with no fixed-step global common minorizer |
| Theorem 7.1; Example 7.2 | 14 / 16 | Pathwise finite-interface simulations and an explicit inequivalence for continuous free decoder observations |
| Theorem 9.1 | — / 20 | Joint sample-size/register-budget Le Cam bound for the actual current A2-v118 known-mark count-to-contact experiment |

The Markov-renewal theorem proves `c G_M(w) <= e_M^2(Z_w^f) <= R_M <= C G_M(w)`. Its lower bound covers randomized time-dependent machines; its upper observer is stationary and deterministic. All retained tree vertices count. In a graph with unary nodes the exact state count is `1 + sum_internal actual_outdegree`, bounded by `(b+1)(2L-1)` for L leaves, rather than the regular full-tree formula from v5. Strict energy domination, not an invalid strict-mass claim at a unique predecessor, proves suffix closure.

The pressure is the maximum of `P_A(s phi+2 beta s psi)` and `P_A(s phi)+s log(q)`. The exponent is `(1-s_*)/s_*` at the larger zero. Strong separation, finite admissibility, metric distortion and quantitative delayed observability remain stated hypotheses. The result is not asserted for overlapping or countably branched systems.

For Parry/equal-ratio systems with survival `q^k(k+1)^(-kappa)`, the critical risk is `M^(-alpha)` times `(log M)^(1-kappa)` for kappa below one, `log log M` at one, and a bounded factor above one. These have the same first-order pressure threshold. The uniform window proves exact finite-profile limits, not unsupported exact optimal-risk coefficients.

The continually observed posterior theorem instead proves `B + Theta(M^(-2/d))` under a true conditional-mean recursion with conditional fourth-moment contraction. It has no renewal clock or common-reference component. The finite inward quantizer controls its own moments; the machine is not initialized with a free exact posterior. The Gaussian autoregressive corollary has no nonzero global common minorizer for any fixed-step hidden kernel.

In the complete edition, the A2 refinement bounds the deficiency by `C [N^(-1/5)+J/(R sqrt(N))+R/J+exp(-cR^2)]` with exactly `J^r+1` designated labels, including overflow. Choosing `R ~ sqrt(log N)` and `J ~ R N^(1/4)` supplies error `O(N^(-1/5))` with `O(N^(r/4)(log N)^(r/2))` labels. This is a sufficient budget, not a minimax-necessity result or a claim uniform through covariance rank degeneration. The physical statistic is unjittered and deterministic; comparison randomization is confined to the experiment-comparison kernels.

## Preservation, history and literature

All preceding v5/v4/v3/v2 quantitative theorem/proof bodies and first-edition foundational bodies remain in the complete edition. The full v4 posterior-orbit proof appears in both views. All **271 retained mathematical labels** resolve, and **77 shared core labels** have identical numbers. Original editions and reviews are untouched. The two PDFs are coordinated reading views, not independent or incompatible revisions.

The history manifest separates the frozen eleven-paper snapshot from active endpoint discovery. Active A1-v37 was fixed at `90465076589f5e5c69227d624f278c47744f1c1d`; active A2-v118 at `44bfc648ead008896a6981a7302a6d5ab8b21bb8`. The new higher-defect conductor, nonreduced-generator and statistical-experiment source passages were read in native form and copied with exact hashes as uncompiled consultation inputs. A2-v112 is retained only as an explicitly historical source edition. No statement about revisions created after this discovery is implied, and no claim to reread every historical archive file is made.

The new probability application uses the current A2 statistical protocol. It does not convert conductor-scheme multiplicity into a noise law or declare the older Sinai LLT, particle/path LDP, nonlinear semigroup, common unbounded-operator domain or physical phase theorem proved. None is an unproved premise of the new chains.

The literature comparison includes Lindsay–Mauldin (2002), Atnip–Roychowdhury–Urbanski (fixed 2018 text), Ghomi–Linder–Yuksel (2022), Kara–Yuksel (2022), and the **published 2026 Cregg–Alajaji–Yuksel paper, Theorem 2 and Corollary 2**. The audit specifies exact versions and the checked statements, and acknowledges classical thermodynamic quantization and stability-based finite-memory approximation rather than claiming them as inventions.

## Source and publication identities

- Controlling review commit: `ee210f3cfe3b4923ef51310e20cd8b20a6a367e1`.
- Native mathematical source commit: `9d844022018a2aa3c0b9e536d6c6c94afc94bf01`.
- PDF/evidence publication commit: `f7faea44e5b93a134f448d599ff63dcb2e2c8d2c`.
- Successful GitHub Actions run: `35723008601`.
- Complete PDF SHA-256: `401088955ccd825ad1245d292772a3d1712ae7a6e395c527c80ec1c5bae0d2ef`.
- Principal PDF SHA-256: `3090671f9e76072548fc7363796f12d0a03d6d3682bb9780d3859fb586e8ee79`.
- Source archive SHA-256: `2ff1f550fe8dc285aacfbd4695428e2d63c3b42ec4f51fe6b98ff1cca251b4b1`.

Both PDFs compiled in three stable TeX passes, with no unresolved references or overfull boxes. **364553 finite deterministic checks** passed; ordinary and optimized outputs agree; eight wrong variants were rejected in both modes. All inherited v1–v5 diagnostic suites passed. Preserved Git tree identities and the copied current A2 source identities were checked against the exact native source commit.

All **108 downloaded archive inputs** match the locally authored or inherited bytes. An independent archive-only rebuild completed with stable three-pass TeX jobs and matching label numbers and pages. The initial single-call local orchestration hit the container execution timeout; the same inputs were then compiled in separate jobs. The independently rebuilt PDFs equal the locally checked PDFs byte for byte. The **90 complete and 18 principal publication pages** equal those editions pixel for pixel at 90 dpi. Remote and local PDF container bytes differ, so cross-environment byte-identical PDF reproduction is not claimed. All local page overviews and selected local and downloaded full-size proof pages were visually inspected.

The final snapshot adds only this index and the rendering-verification record to the publication commit. It changes no compiled mathematical input or published PDF. Main and all preceding review/revision branches are not updated by this revision.

This edition is supplied for independent mathematical refereeing. New proofs, not diagnostic counts, answer the substantive objections. No formal proof certificate, independent approval, priority determination, closure of unrelated historical gates or four-journal acceptance is claimed.
