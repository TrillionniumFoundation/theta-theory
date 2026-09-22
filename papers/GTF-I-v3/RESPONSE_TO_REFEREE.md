# Response to the referee — General Theta Foundations I, third revision

The controlling report is `reviews/general-theta-foundations-i-v1-2026-09-22/REFEREE_REPORT.md` at `01d3e78bd40985651f5b4ff24364e1dba5d481f0` (report blob `65b5bc0b50b8faac5dae4fd6770eb201f1ab49f2`). The present revision begins from the subsequent v2 referee-ready edition `75d8f3f8672ab78a844cc0a7a68808b46edf56f5`; it does not present the already completed v2 work as a new response or invent a v2 referee report.

We thank the referee for separating the correctness of the original refreshing-HMM calculation from the much more demanding question of the paper's mathematical centre. The third revision answers that question by proving a sharp separation between checkpoint and causal finite-label complexity, and by extending the measured-calibration analysis to correlated, nonseparable experiments. The title and the foundational development are retained. All v2 quantitative statements and proofs are preserved byte for byte, as are the v1 foundational proofs and boundary examples in the inherited source tree. Only the introductory exposition is replaced; its earlier versions remain in the earlier editions.

## E1 — A stronger mathematical centre

The new main theorem is `thm:v3-phase`, with the general converse `thm:v3-orbit`. In the expanding regenerative experiment the acquired state is uniform at every checkpoint, independently of the reset probability. Its exact checkpoint risk is always `1/(12 M^2)`. The optimal risk of a single causal M-label machine has three different rates:

- `M^(-2)` when `q < 1/4`;
- `(1 + log M) M^(-2)` when `q = 1/4`;
- `M^(-log(1/q)/log 2)` when `q > 1/4`.

The lower bound covers arbitrary randomized, time-dependent finite-state machines and even their lower limiting temporal-average risk. The upper bound is one deterministic binary-suffix machine, with all suffix lengths charged as labels. It does not use q. This is not a smooth density estimate followed by a stable-filter grid: the checkpoint law is identical across the regimes, the unobserved dynamics expand, and the converse must resolve a whole weighted future orbit. The critical logarithm is derived and matched, not absorbed into a hidden constant.

We submit this new theorem and its full proof for the referee's assessment of mathematical significance. Neither a compilation record nor our description of the contribution is offered as a substitute for that assessment.

## E2 — Beyond strong, known-calibration refreshing

The complete every-positive-refresh theorem and conditional block-stability analysis of v2 remain in the paper. The new experiment goes further in a different direction: arbitrarily long intervals of expanding dynamics are allowed, and no uniform contracting update is assumed. The exact finite geometric sum in `lem:v3-tree` displays the transition and its dependence on q. The program is the same at every q and needs no supplied reset-frequency calibration. The paired statistical experiment separately treats an unrestricted unknown additive calibration through an actually observed second measurement.

The new theorems state which parameters are known: the contact map and covariance are specified parts of that experiment. Unknown reset frequency and unknown additive calibration are not silently promoted into a theorem for an arbitrary unknown transition or observation law.

## E3 — Strict distinction from the strongest A1 result

A1 v37's global-cover/acquired-mass/causal-compatibility transfer is retained as `cor:v2-a1`, not advertised as new. The new orbit theorem addresses information that must survive after a reset for all possible subsequent nonacquisition intervals. Its lower bound is the quantization error in the Hilbert space of future readouts, not the quantization error of the current acquired state. In `thm:v3-phase`, the latter is exactly the same uniform law for all q and hence cannot distinguish the causal rates. This gives a concrete separation beyond a checkpoint anisotropic rate and does not infer uniform infinite-time constants from a finite-horizon transfer.

## E4 — Relation to the entire historical pipeline

The historical snapshot `c04845b6613208406703695c9c184ae461f95805` was exported in full, its complete Git inventory retained in the context artifact, and its eleven controlling Round-17 source modules and Round-13/17 dependency ledgers used in the mathematical audit. `HISTORY_AUDIT.md` records every pipeline component and its precise role. A1 v37, A2 v112, the GTF outline, and both earlier GTF source editions remain available in the inherited tree.

The revision pursues the report's substantive routes A and B. It does not rename a finite-label estimate as a Sinai raw local limit theorem, a particle/contact LDP, an unbounded compressed-resolvent result, or a latent-phase semigroup. Those mathematical programs are retained, not removed or relabelled as completed. The new main theorems have self-contained proofs and no dependence on an unverified pipeline completion claim.

## E5 — An actual singular, noisy, measured-nuisance experiment

`thm:v3-quotient` proves exact equality, for every label budget and every bounded loss, between the paired experiment with unrestricted additive calibration and the Gaussian difference experiment. The joint measurement covariance may have arbitrary cross-channel and cross-coordinate correlations, subject to positive definiteness. The nuisance lower bound is a diffuse-prior argument with an explicit parameter-independent simulation and vanishing total-variation error.

`thm:v3-contact` then proves the matched statistical-plus-label law under a two-sided contact geometry in the actual Mahalanobis metric. Neither separability of the mean nor independence of its coordinates is required. `ex:v3-coupled` gives a nonlinear triangular shear of quadratic/cubic contacts and a concrete correlated Gaussian pair. The independent-coordinate theorem of v2, including degenerate zero-noise endpoints, remains intact. The proof does not infer contact geometry from rank alone and does not claim full experimental equivalence for the nuisance parameter.

## M1 — Persistent labels, program, workspace, and acquisition

The finite machine uses the union of all binary words of lengths 0 through B, exactly `2^(B+1)-1` states. An integer sentinel encodes the suffix length. There is no uncharged age register, past output buffer, or real-valued codebook. Its read-only parameter is the integer B; prefix acquisition and formatting use O(B+1) transient bits. Any persistent random-generator state or data-dependent tape position must also be charged to the label. Modes and prefix bits are explicitly acquisitions. These conventions appear before the main theorem, not only in a later qualification.

The existing v2 section on finite program descriptions and numerical error is preserved in full. Neither section equates a label bound with a bound on all computational resources.

## M2 — Acquisition laws

The acquired-law/small-ball formulation, subprobability converse, discrete finite-history endpoint, and Cantor-dimensional example from v2 remain. The new regenerative theorem allows any standard Borel acquisition space, Borel dynamics, acquired law, and bounded Borel readout; its explicit matching expanding example specifies its uniform acquisition rather than treating that example as a theorem for every command law.

## M3 — Common-controller comparison versus optimal control

`thm:v2-control` and its complete Bellman proof remain. They compare the actual finite-reference policy with unrestricted history-dependent optimal control under the theorem's predictive-state sufficiency and Lipschitz/discount assumptions. The introduction now directly compares this result with Kara–Yuksel Theorem 12 and approximate-information-state Theorems 9 and 27. These antecedents are acknowledged as genuine policy results; Kim's fixed-policy comparison is not treated as an unrestricted-optimality theorem.

## M4 — Dimension and stability constants

The explicit d/gamma constants in the v2 HMM theorem remain. The new sharp causal theorem displays its q dependence through the finite geometric sum and gives the concrete lower constant `(1-q)/4096`. The nonseparable contact theorem states its constants in d, observation dimension m, and the contact-metric distortion constants lambda and Lambda. No high-dimensional uniformity is inferred from fixed-dimensional comparison notation.

## M5 — Paper architecture without mathematical deletion

The abstract and opening sections now begin with the future-orbit converse, sharp causal transition, and exact calibration quotient. The earlier quantitative development follows them, and all foundational proofs and boundary examples remain in the appendices. The theorem/proof preservation test is byte-based for the complete v2 mathematical body and input-hash-based for the inherited foundational sources. Old introductions remain in their original directories. Build receipts, provenance, and the response letter are supplementary, not inserted as theorem evidence.

## M6 — Theorem-level literature comparison

The revised introduction distinguishes future-prediction representations and predictive rate-distortion (including Marzen–Crutchfield and Loomis–Crutchfield) from the hard persistent-state, arbitrary-machine converse proved here. It also distinguishes established filter quantization, finite-window policy near-optimality, and approximate information states from the new sharp lower/upper phase law. The v2 comparison table is retained. External theorem statements and current primary-source records were checked; a universal priority or exhaustive literature-certification claim is not made.

## M7 — Stable source editions and reproducibility

The new revision descends from v2's stable referee-ready snapshot, which already contains the complete pinned A1 v37 and A2 v112 source editions. Their Git trees and the original GTF foundational tree are checked unchanged. `SOURCE_MANIFEST.json` binds all new mathematical/executable inputs and the exact derivations of the retained body and bibliography. `evidence/BUILD_RECEIPT.json` separately records the actual executed source commit, PDF hash, source-archive contents, and build result. There is no circular assumption that an ancestor SHA equals the new source identity.

This repository edition is a reviewable mathematical edition; it is not represented as a journal publication or DOI-registered preprint. The retained internal sources are permanently available on the revision branches rather than only through expiring workflow artifacts.

## Smaller comments and next referee pass

The title is retained, the abstract now separates the new quantitative claims from the framework, the master outline is not counted as proof, every boundary example remains, the resource model precedes the main theorem, and the original theorem-to-literature table remains. The decisive new proofs to inspect are the reset-time disjointness argument, the off-image-centre orbit small-ball bound, the critical logarithm and exact suffix-state count, and the diffuse-nuisance simulation under the unchanged label budget.

The branch is supplied for further referee review. Successful source checks and finite diagnostics certify only the executed checks described in their receipts, not the mathematical correctness or editorial acceptance of the paper.
