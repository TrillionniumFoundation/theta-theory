# Response to the R52 referee report and proof-pipeline audit

**General Theta Foundations I — Revision 83**  
**Primary article:** *Finite-Use Geometry and Learning of Ordered Quantum Measurements*  
**Exact reviewed predecessor:** `57937576a6f413594589d0509a6816ca4ea3a83e` (v82)  
**External report:** `5bb27a43c0f78ba99020f605a0489bcbd403e236`  
**Proof-pipeline audit:** `7d5b1033f31c348ae60ebfb04e8b8d57b3b9e75e`  
**Date:** 5 October 2026

We thank the referee for the detailed correctness analysis and for identifying the normalized horizontal principle, boundary scope, computational legalization and article architecture as the most useful directions. The report is frozen verbatim; its disposition is not edited or represented as approval of this successor. We retain the general-mathematics-journal objective and address the mathematical criticism through specific new results rather than a change of topic or deletion of the established theory.

## Principal changes

The new Section 67 constructs a positive concave normalized-tuple covariance on the **complete** finite-outcome POVM body. A regularized horizontal-energy identity proves an adaptive path and midpoint upper through zero effects and changing ranks. The binary restriction is exactly the existing Sylvester variance, not a merely comparable proxy. The same form has an unregularized data-processing inequality, a projection-valued zero-operator characterization and a finite-angle noise/horizon crossover with a matching fixed-k lower on an explicit family. A rational Gram-corrected system evaluates the upper certificate with polynomial bit complexity.

The new Section 68 proves a **search-free affine legalization** of balanced component estimates, with uniform error and polynomial bit complexity. Its guarded version is legal on every record. It retains the fixed-k joint call and description orders while removing grid enumeration from the statistical legalization step. We do not extend this efficiency claim to the global dictionary or arbitrary collective-readout synthesis.

The main article begins with the finite-outcome results and these two additions. The entire binary prerequisite graph is retained in appendices; the structural companion remains separate and unchanged. The main comparison now gives the actual MB/ZRK substitutions, with the required legality repair before an interior metric is applied. All old section files are byte-identical, and all old active labels are retained in the same editions. The full preservation edition remains archival.

These changes do not constitute a matching full-boundary entropy theorem or a growing-k minimax law. They establish a global coupled upper principle and a specific computational consequence while keeping those further mathematical questions precise. Independent human priority assessment remains an external step; neither this response nor CI supplies it.

## I. Required revisions (R01–R15)

### R01. Separate journal objects

The quantitative article, unchanged structural companion and complete research edition remain distinct. The quantitative source is self-contained and no structural theorem is used to amplify its scope.

**Location:** JOURNAL_README.md; quantitative.tex; structural.tex.

### R02. Independent human priority review

The targeted primary-source comparison is expanded, but no human opinion is supplied or inferred. The specialist brief now identifies four exact proof objects and the possible equivalent prior formulations to inspect. This external gate remains uncompleted.

**Location:** INDEPENDENT_REVIEW_BRIEF.md; LITERATURE_AUDIT.md.

### R03. Finite-outcome theorem first

The quantitative main text begins with the noncommuting balanced-interior geometry, exact code and learner, then the new closed-body covariance and affine repair. All binary prerequisites are fully retained in appendices, including the old introduction labels through a guide appendix. This is reorganization, not proof deletion.

**Location:** quantitative.tex; editions/operational-introduction83.tex; editions/operational-guide83.tex.

### R04. Balanced-interior headlines

Every new summary of the sharp finite-outcome entropy/learning law explicitly specifies the balanced interior. The new covariance upper has a different, genuinely complete-body domain, and is named an upper certificate rather than a full classification.

**Location:** Abstract; Introduction; thm:closedcovariance83; RESOURCE_LEDGER.md.

### R05. Fixed outcome count

All minimax summaries state fixed k and display the k³ upper. The new closed-body upper and rational evaluator are uniform statements with explicit k-dependence, not a growing-k minimax law.

**Location:** Introduction; cor:affinelearner83; PROOF_STATUS.json.

### R06. Direct tomography comparisons

The main text states Mele–Bittel III.3/III.9 and ZRK Theorem 2 in their actual one-use normalizations and access models. It includes the sufficient d²k⁴N/delta² and k²Nd²[d+k+log(1/eta)]/delta² substitutions, after an explicit balanced legalization. Neither substitution is claimed sharp for the original estimator.

**Location:** editions/operational-priority83.tex, eq:mbdirect83, eq:zrkexact83, eq:zrkfuture83.

### R07. Pair geometry versus common learning

The pair-dependent eigenvector lower witness remains separate from the target-independent component simulations and guarded affine learner. No learner receives a true effect, eigenbasis, target pair, or private dictionary.

**Location:** thm:multioutcomemetric82; thm:multioutcomelearning82; cor:affinelearner83.

### R08. Actual metric coding converse

The inherited arbitrary-centre converse and fixed public decoder argument remain unchanged and active. The new covariance modulus is expressly not identified as a metric and is never used through a triangle inequality.

**Location:** thm:multioutcomeentropy82; Section 66; thm:closedcovariance83.

### R09. Every-record and stopping quantifiers

The original learner and lower theorem remain intact. The new adaptive upper pads bounded stopping with discarded dummy slots, and affine repair has a defined legal output on every Hermitian record.

**Location:** Proof of thm:closedcovariance83; thm:affinerepair83; cor:affinelearner83.

### R10. Honest public dictionaries

The public exact dictionary remains target independent and its finite but exhaustive cost is stated. Polynomial covariance evaluation and polynomial statistical legalization are separately proved; neither is called an efficient dictionary.

**Location:** prop:covarianceexact83; thm:affinerepair83; RESOURCE_LEDGER.md.

### R11. Finite-control guarantee

The affine learner uses the inherited actual-control component procedure, with the same control budget. The ideal certificate still requires a fixed readout and its own additional implementation-law allowance. These hypotheses are not merged.

**Location:** cor:affinelearner83; thm:multicertificate82; priority section.

### R12. Scalar replay scope

The scalar ternary certificate is rerun unchanged. The new suite checks exact covariance and repair kernels, not a general physical learner or general matrix risk net. Machine-readable scope flags remain false for those executions.

**Location:** covariance_check.py; PROOF_STATUS.json; COVARIANCE_SCHEMA.md.

### R13. Visible ranges

The Introduction and resource ledger distinguish unrestricted closed-body upper geometry, balanced covering with delta<1/128, balanced learning with delta<=2^-24 and eta<=1/8, and rational-input computation. The crossover lower specifies d=2, epsilon<=1/2 and its angle range.

**Location:** Introduction; thm:noisecrossover83; RESOURCE_LEDGER.md.

### R14. Reduce revision language

The front narrative uses mathematical questions, definitions, theorems and direct comparisons, not a revision-by-revision history. Detailed provenance and crosswalks are outside the article. Historical binary development is preserved as proof appendices and in the complete edition.

**Location:** quantitative.tex; editions/operational-priority83.tex; complete edition.

### R15. Full boundary and growing k

The new covariance theorem makes a concrete full-boundary advance: a rank-stable adaptive upper with exact binary restriction and a sharp noisy-projector crossover. A matching arbitrary-boundary lower/entropy theorem and growing-k minimax law are still identified as distinct mathematical targets.

**Location:** Section 67; Further questions in editions/operational-priority83.tex.

## II. Detailed comments (D01–D30)

| Item | Point | Response |
|---|---|---|
| D01 | Matrix order | The inherited H A^{-1} H order is untouched. New covariance formulas retain S and S* separately, and its factorization is computed over a real Hilbert space. |
| D02 | Inaccessible duplicate label | Both inherited and new horizontal proofs specify the proof environment; it is not a device output. |
| D03 | Stopped output | The proof says explicitly that the original stopped output is a common postprocessing of the padded experiment. |
| D04 | Pair-dependent witness | Retained as a pairwise metric lower only; no common-design inference. |
| D05 | Arbitrary legal centres | The inherited component witness and covering lower continue to allow centres outside the balanced interior. |
| D06 | Affine subspace | The balanced ball remains inside sum H_j=0. The new covariance uses that same normalized tangent condition, with no dimension loss from an ambient Euclidean conversion. |
| D07 | Dependent final effect | The original grid and its final residual effect are unchanged. The alternative affine repair normalizes by a mean correction rather than independent rounding. |
| D08 | Equality conventions | Strict greedy separation and closed assignment remain intact. New exact PSD and certificate equality checks use rational decisions, never tolerance. |
| D09 | Represented real inputs | The original real-input codec still requires certified approximations. The new evaluator explicitly requires Gaussian-rational data. |
| D10 | Finite versus efficient | Finite exact dictionary is retained as such. Polynomial claims are restricted to covariance evaluation and affine legalization. |
| D11 | Charge all component calls | The alternative learner charges k fresh component procedures at a=delta/(32k ceil(sqrt(N))). Their sum retains the k³ upper. |
| D12 | Reference-preserving relabeling | The 3/4,1/4 instrument-level identity is retained and cited, not reduced to scalar outcome equality. |
| D13 | Bad-record fallback | The guarded affine candidate undergoes exact balanced tests and returns the uniform tuple on failure. No good-event search termination is assumed. |
| D14 | 5delta/8 slack | The old 5delta/8 construction remains unchanged. The new alternative allocates delta/4 to repaired estimation and delta/4 to coding, giving delta/2. |
| D15 | Odd-k erased reference | The complete subnormalized-reference calculation in Section 66 remains active and unchanged. |
| D16 | Coarse-graining actual distance | The old coherent converse uses channel postprocessing. New noise witnesses likewise coarse-grain at the instrument level. |
| D17 | Weyl plus triangle | The inherited clipping proof is retained. No operator-Lipschitz shortcut is inserted. |
| D18 | Binary confidence invocation | The exact cor:operatorconfidence80 label and accuracy cap remain at the lower-bound invocation. |
| D19 | Pointwise success for codes | The inherited public fixed-length converse still requires positive success at every target, not only a prior average. |
| D20 | Fixed good-label event | The finite certificate transfers one event chosen at the nearby grid point before moving probability. |
| D21 | Trace-to-TV factor | The inherited Mk r/2 factor remains explicit; covariance certificates instead report an unhalved operational trace-norm upper. |
| D22 | Complete finite enumeration | The scalar statistical checker still requires all net points and strings. A covariance solver resource cap returns an error, not an incomplete upper certificate. |
| D23 | Implementation-law error | Kept separate in the ideal certificate discussion and resource ledger. |
| D24 | Finite versus universal proof | New regression reports explicitly say continuum_theorem_verified_by_finite_tests=false. Universal arguments are written in Sections 67–68. |
| D25 | Unsigned commits | No human signature or cryptographic authorship is asserted. Actual-source reconstruction is a byte identity claim. |
| D26 | Structural scope | The structural companion and its active source graph are unchanged and are not inputs to the new measurement proofs. |
| D27 | Full-body binary dimension gap | The d⁴ full-body learner upper remains a separate unmatched growing-dimensional bound; no contrary claim is made. |
| D28 | Two different optimalities | Affine entropy depends on p=(k-1)d², whereas query matching is fixed k. Summaries display both separately. |
| D29 | Single-copy comparison | The ZRK main-text substitution states the unentangled global-design acquisition, worst-input TV loss and explicit repair before future-loss conversion. |
| D30 | Strongest message | The article connects future-use geometry, coherent converse, public descriptions and exact risk. It now adds coupled full-body upper geometry and polynomial legalization, without claiming first POVM tomography. |

## III. Proof-pipeline acceptance gates

The 24 gates below follow the four groups in Section 16 of the controlling audit. “Required” reproduction refers to v83 receipts only; a successful v82 run is not evidence for this revision.

### Mathematical

| Gate | Requirement | Current response |
|---|---|---|
| M01 | Horizontal identities | Inherited identities are byte-identical; the new energy identity and adaptive cancellation are fully proved in Section 67. |
| M02 | Arbitrary centres | The old covering proof remains active in the main text. |
| M03 | Dependent rounding | The original public code and grid remain unchanged; the affine alternative is not substituted into the covering proof. |
| M04 | Fixed k | Displayed upper/lower k-dependence and remaining growing-k question retained. |
| M05 | Odd-alphabet reference | Section 66 unchanged. |
| M06 | Clipping | Weyl-plus-triangle retained. |
| M07 | Description conventions | Fixed-length public code distinguished from the retained shared-randomness expected-prefix theorem. |
| M08 | Complete certificates | All scalar net points and strings checked; no prefix accepted. |
| M09 | Implementation-law budget | Ideal and actual-control models kept distinct. |

### Priority

| Gate | Requirement | Current response |
|---|---|---|
| P01 | Independent expert opinion | Not obtained; brief supplied, no completion claim. |
| P02 | Main-text theorem comparison | MB and ZRK exact parameter/loss/access substitutions supplied, including legality. |
| P03 | Prior horizontal gauges | Antecedents credited; exact covariance equivalence remains a concrete specialist priority question. |
| P04 | No first-learner language | No first POVM learner or broad new optimal tomography assertion. |
| P05 | Precise contribution | New claims enumerated by exact theorem labels, domains and resources. |

### Editorial

| Gate | Requirement | Current response |
|---|---|---|
| E01 | Separate structural article | Unchanged self-contained companion retained separately. |
| E02 | Finite-outcome narrative | The first proof sections are finite-outcome geometry and learning. |
| E03 | Move historical detail | Binary proof corpus in appendices; revision crosswalk only in repository package. |
| E04 | Ranges and resources | Introduction, theorem statements and resource ledger agree. |
| E05 | Further questions | One main-text subsection distinguishes matching boundary theory, growing k, and general efficient synthesis. |

### Reproducibility

| Gate | Requirement | Current response |
|---|---|---|
| V01 | Exact-head read-only verification | A new source-bound build and final-head reconstruction are required for v83; no predecessor run qualifies it. |
| V02 | Source/page hashes | Builder regenerates source inventory, theorem locations and all page signatures. |
| V03 | Machine-readable scope | Current PROOF_STATUS and each finite regression distinguish execution from proof. |
| V04 | Scalar versus matrix checks | Complete scalar statistical certificate distinguished from local matrix algebra and pair evaluation. |
| V05 | Signatures | No unsigned object is described as signed; no signature is invented. |

## IV. Audit risk register

| Risk | Subject | Current treatment |
|---|---|---|
| A01 | Priority | Independent expert opinion still required; main-text quantitative comparisons and a precise brief are now supplied. |
| A02 | Growing k | No new minimax equality in growing k is claimed; current k³ versus k-independent gap is visible. |
| A03 | Full boundary | Advanced by a global coupled adaptive upper, singular covariance identities and a sharp family crossover; matching general lower and entropy remain distinct. |
| A04 | Accretive architecture | Main narrative reorganized and history moved out; all binary proof text retained in appendices. Total page count is not represented as reduced. |
| A05 | Efficient synthesis | A specific computational gap is closed by polynomial affine legalization and polynomial covariance evaluation. Dictionary and general readout costs remain separate. |
| A06 | Trusted controls | Actual-control learner and ideal certificate have separate guarantees. |
| A07 | Code interpretation | All scope fields reject a general physical-learning execution inference. |
| A08 | Constant/range proliferation | Centralized ranges and explicit conversion constants supplied; old theorem ranges unchanged. |
| A09 | Structural companion | Retained separately without merging physical interfaces. |
| A10 | Whole programme | Frozen analytic order and all five false aggregate flags preserved. |

## V. Verification and preservation boundary

The exact new suite contains 140 positive checks and 17 negative controls. It exercises noncommuting and singular effects, the binary identity, the covariance Gram convention, stochastic processing, exact scalar product comparisons, and affine face/fallback cases. All 20 inherited suites run again in ordinary and optimized Python. Written proofs, finite regression, source/page reconstruction, and human priority are separate forms of evidence.

`V82_BASELINE.json` pins 465 prior native files and 827/329/116 complete/quantitative/structural labels. The prior section text remains byte-identical and active. Original entry, audit and build wrappers are archived before revision. New proofs appear in both quantitative and complete editions. No old revision directory or review branch is changed.

Production qualification requires an actual committed native source, isolated reconstruction of all three manuscripts, a standalone reconstruction of both journal articles, and read-only verification of the exact final submitted head. The corresponding receipts, rather than this prospective response text, establish what was executed. This revision does not supply a cryptographic human signature, an independent specialist opinion, journal acceptance, or closure of the independent A/B/C/D analytic programme.
