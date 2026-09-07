# Response to the referee report on A1 English v23

**Revision:** A1 English v24, 7 September 2026.  
**Main article:** *Attainable information at exponent collisions*, Qian Qi.  
**Complete companion:** *Attainable information in positive experiments: complete companion developments*.  
**Submission examined by the referee:** `e7c1111d0ab8fb39e4b213902186db2cdf6d0dea`, `papers/A1-english-v23/`.  
**Controlling report:** `78e948fe03a3969fde4c96411ae1fee5915cb908`, `reviews/a1-english-v23-harsh-independent-2026-09-07/REFEREE_REPORT.md`.

## 1. The report being answered

We thank the referee for distinguishing the concrete mathematical requests from the editorial recommendation. The report closes E22.1–E22.4, finds no fatal counterexample or unresolved central gap in the audited collision route and direct saturated-algebra proof, and explicitly limits that finding to the inspected material. It nevertheless recommends against acceptance at the requested journal level on grounds of significance and proportion. We do not recast this as an acceptance recommendation, as a certification of all appendices, or as a new list of fatal defects.

This revision addresses E23.1–E23.3 without weakening a theorem or adding an unrelated application. The 20-page main article contains the complete direct collision argument. The 108-page companion contains the complete transfer, saturated-algebra, structural, exact-kernel, other-geometric, decision and effective developments. The combined mathematical submission therefore retains the previous body of results, but its principal article no longer asks the reader to traverse those separate developments in order to evaluate the collision theorem.

The principal classification is unchanged, word for word. The revision does not announce a new theorem with enlarged hypotheses. It changes the architecture, makes the strongest existing multiscale example visible immediately, and writes the monomial risk quantifiers locally. The venue-level disagreement remains a matter for reassessment; it cannot be closed by an author-side test receipt.

## 2. E23.1 — Significance and the scale of the article

**Disposition: a reasoned response and a materially reorganized submission; the editorial judgment is not claimed to be resolved.**

The report already recognizes that the collision theorem is more than a Vandermonde-rank observation and gives credit to its acquisition/global-cover/causal conjunction. Our response does not suggest that the referee overlooked those points. Rather, we now present that entire conjunction as the object of a single, independently readable article, with the complete argument occupying Sections 2–6 and its consequences in Section 7.

The specific result on which we request reassessment is Main Theorem 1.1. Starting from a fixed positive monomial experiment, a fixed full-support prior and a compact strictly ordered one-step calibration chamber, it computes the optimal retained-label prediction profile for every integer budget, uniformly through all additive collisions. The profile is not posited as the geometry of a prescribed quantization measure. Its scales and its acquired truncation are derived from the experiment. Both an unconditional lower bound under one actual exploration law and an all-history upper bound hold, and a single causal filter attains the same profile without access to discarded commands or reports.

There are four closely linked points in the proof. First, the past-generated product tangent and evidence normalization give the acquired dimension, which may be smaller than the future observation dimension. Second, every complete Newton–Hermite prefix required by a nonzero scale has uniformly positive acquired mass. This uses a square inverse chart with complementary command coordinates and the actual report-word probability, not a conditioned command slice. Third, rationality and the acquired dimension give a dimension-truncated cover of the whole image, rather than a local acquisition patch. Fourth, raw remaining moments carry a reachable-state Bayes update whose bound does not invert a collision scale. These four conclusions hold at the same degeneracies. The direct argument now makes their dependence inspectable without first introducing an abstract transfer framework.

The two-parameter example makes the quantitative content particularly concrete. For the stated four-cell, five-trial experiment, the complete risk profile has six-, eight- and nine-dimensional regimes. Along a path of contact order k, the two memory crossover orders are θ⁻⁶ and θ⁻⁽⁸ᵏ⁻²⁾. Thus a rank at a fixed nonsingular parameter does not identify when either asymptotic regime becomes visible. The example also explains why a seven-dimensional branch is redundant rather than merely absent from the exposition.

We maintain these conclusions and their full original uniformity. We do not replace them by a collision-free result, assume a density for the prior, remove integer budgets, restrict the converse to deterministic encoders, condition away the report word, or substitute unrelated checkpoint encoders for one common filter. Equally, we do not infer unrestricted-prior monomial uniformity or an unbounded-horizon result. Those restrictions were already in the theorem reviewed, and the report explicitly identifies them as such.

The covariance theorem remains a complete prior-uniform multistep classification in the companion, including support and rank loss. Its finite observable quotient and immediate saturation are stated and proved. It is not presented as a second instance of delayed Newton-flag acquisition or as an additional conceptual breakthrough needed to enlarge the principal article's apparent contribution. Its direct elementary argument and the alternative transfer argument are both retained.

The revised article gives the central result a proportionate presentation. This is our positive response to the report's assessment. It is not an assertion that rearrangement creates a new mathematical advance, establishes exhaustive priority, or forces a different editorial decision. No result has been weakened in order to manufacture agreement.

## 3. E23.2 — Architecture without loss of mathematics

**Disposition: implemented.**

The main article now follows the chain

> physical future equivalence → actual product-tangent rank → confluent acquisition and whole-image covering → optimal checkpoint compression → one causal filter → collision phases and bit budgets.

The title and abstract name this problem. The introduction states the theorem before discussing general-purpose mechanisms, gives the two-parameter profile on page 3, and explains the proof's experiment-specific steps. General programmatic claims and the rebuttal to the report are not placed in the mathematical article.

The main route uses the existing direct checkpoint and causal proofs, previously located in the long appendix. Both proofs are included in full. A short final proof of Theorem 1.1 identifies their exact implications; it does not replace either proof. The general transfer theorem and its separate verification for monomials are now complete companion developments. Consequently, the main proof does not depend on the transfer theorem, the saturated observation algebra, the exact-kernel theory, uncertainty, mechanical realization, or effective construction.

The source-reference audit finds one cross-volume reference inside an inherited main proof: the statement that a separate mechanical realization is treated elsewhere. That sentence expressly disclaims a mechanical claim for the general categorical construction. It is not a premise. The other main-to-companion references concern an alternative affine specialization and the detailed literature comparison, not missing proof steps. This distinction is recorded in `PRESERVATION_REPORT.json` rather than hidden behind the phrase “self-contained.”

The companion is an active, independently typeset document, not a directory of uncompiled remnants. It contains the general causal transfer theorem, its monomial verification, the full saturated algebra theorem and its direct proof, the alternative algebra transfer proof, and every inherited structural, pairing, exact-kernel, circular, inverse-profile, directional, uncertainty, decision, numerical and resource argument. Its introduction states the inherited monomial conventions and separates them from each other class's local hypotheses. Section and equation labels in that volume have prefix C; imported references to the main article have prefix M.

The preservation checks give a stronger record than a page-count comparison. All 130 inherited theorem/lemma/proposition/corollary blocks remain active and byte-identical. All 129 inherited proof blocks remain complete and occur once in the active union: 128 are byte-identical, and one has only a documented navigation-sentence change. In the exterior spectral proof, “proved below” was changed to “proved in the main article” after relocating the Leja argument. No formula, hypothesis or mathematical step in that proof changed. `EDITORIAL_PROOF_EDITS.json` records the exact before/after sentence and hashes. Six inherited formal definition/remark blocks and all 402 inherited labels remain present. There is one additional short main-theorem proof and one additional local risk definition, not an additional classification theorem.

The complete 772-file manifest-covered v23 source is preserved separately, with its GitHub-pinned manifest. The v22 base manifest, reconstructed v23 expansion, baseline-generated TeX, and controlling report are retained for checking the source lineage. Existing repository directories and historical branches are not deletion targets of the supplied additive patch.

## 4. E23.3 — The two-parameter example

**Disposition: implemented in Main §1.3, page 3, with its full proof retained as Corollary 7.3.**

The early example specifies the detector rather than showing only an abstract exponent set. For Aᵤ,ᵥ = {0,1,2+u,3+v}, it records the four positive cells and N=5. With ρ=max(|u|,|v|) and τ=min(|u|,|v−u|,|v−2u|), both common-filter risk criteria have the uniform order

    max{ M^(-1/3), ρ^(1/2) M^(-1/4), (ρ² τ)^(2/9) M^(-2/9) }.

The discussion identifies peak dimensions 6, 8 and 9 at the intersection, on a nontrivial collision line and off the lines, respectively. It describes the six separated groups and the three internal gaps, and explains the redundancy of the seven-dimensional branch. On u=θ, v=θ+θᵏ, k≥2, it displays both crossover orders and the corresponding regret orders θ² and θ²ᵏ. These are stated as comparison orders, not exact numerical thresholds for an integer budget.

No new hypothesis or additional theorem was needed for this exposition. The old five-future-direction/two-acquired-dimension example is retained in §1.4 for its distinct purpose: explaining why the observation-side affine hull gives the wrong acquired cap.

## 5. Local risk definitions and the already closed E22 requests

Main Definition 2.5 explicitly defines the actual unconditional acquisition law and its prefix marginals. It writes both checkpoint infima and both common-filter infima. In the latter, the infimum over one filter is outside the checkpoint maximum; independent coding randomness is averaged before the worst-history supremum. It also distinguishes compatible checkpoint marginals from executing multiple future probes in one physical run. This is a local clarification of the monomial notation, not a new objection attributed to the report.

The E22.1–E22.4 repairs remain in force. The theorem-level contribution is stated in the main article; the complete nonlinear-filter comparison is retained in Companion §C.10; the algebra quotient, saturation proposition and direct proof are retained in §C.3, with the alternative proof in §C.7.1; and the algebra's local risk definition is unchanged. The revision does not reopen those requests as alleged defects of v23.

## 6. Verification and its limits

The controlling report and manuscript identity were read through the connected GitHub repository. Local source bytes were recovered from the saved v23 package and checked against the repository-pinned manifest and report blob; they were not accepted merely because an archive filename said “v23.” The baseline generated source was reconstructed before reorganizing the article.

The submitted build compiles both volumes with shell escape disabled, resolves cross-volume references, and reports no undefined, duplicate, overfull or unsettled-reference warnings after the final passes. All pages were rendered for layout review; selected formula- and reference-heavy pages were inspected at higher resolution. The visual scope is recorded separately and is not a line-by-line proof audit.

The directly relevant v22 and v23 author suites completed 45,393 assertions. The published v23 referee diagnostic script completed 3,878 checks, with byte-identical ordinary and optimized-Python receipts. This is a replay by the revising assistant, not a newly independent referee assessment. An additional 201 finite exact-arithmetic/source checks cover the early phase calculations and risk ordering. Mutation checks reject a weakened integer-budget statement, removal of either a direct or companion proof, corruption of a historical source, and an unrecorded change inside a proof.

An initial attempt to rerun all older author suites completed v10 and v11 but reached the enclosing execution timeout during v12. That incomplete attempt is recorded and is not counted as a completed v12 test, a failure of the mathematics, or a successful full-suite audit. The focused validation receipt states precisely what completed. All old test scripts remain available through the optional full-suite mode.

These checks establish source preservation, finite regression behavior and successful typesetting. They do not prove the uniform acquisition-mass and entropy estimates, compute the exact minimax infimum, exhaust prior literature, or certify journal suitability. Those remain mathematical and editorial matters to be judged from the complete arguments.

## 7. Requested reassessment

The concrete architectural and example recommendations have been implemented without loss of the established mathematics. We request a fresh assessment of the collision classification as the now self-contained main article, with the complete companion available for the separate results and alternative proofs. We maintain the theorem and its exact quantifiers. We neither claim that the referee's venue-level judgment has been reversed nor treat that judgment as a reason to abandon the positive result.
