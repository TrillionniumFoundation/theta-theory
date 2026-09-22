# Response to the referee: General Theta Foundations I, second revision

**Qian Qi — 22 September 2026**

This response addresses the report at `01d3e78bd40985651f5b4ff24364e1dba5d481f0`, whose report blob is `65b5bc0b50b8faac5dae4fd6770eb201f1ab49f2`. The unchanged report is included in `review-input/REFEREE_REPORT.md`. The revision adopts the report's Routes A and B: a general causal-resolution theorem and an actual singular statistical experiment. It also adds an unrestricted optimal-control comparison. The requested journal standard and the title are retained. The issue of significance is submitted to renewed mathematical assessment, not declared settled by an author checklist.

The main article now begins with the new quantitative results. The original mathematical development is included, unchanged, as appendices. The complete original edition, including its original introduction, PDF, source, and proof ledger, is preserved in `legacy/`. Fixed complete A1 v37 and A2 v112 source editions are included in `source-editions/`. Thus reorganization does not remove the original arguments or replace their sources with summaries.

## E1. The central theorem and the mathematical architecture

**Change:** Theorem 2.1 (`thm:v2-resolution`) relates finite-label resolution to concentration of the actual acquired law and to exact suffix evolutions of the predictive update. Its proof uses a same-word hybrid telescope rather than assuming a one-step contraction. The lower and upper hypotheses are stated separately; neither a small cover nor a full-rank differential is substituted for acquired mass.

Theorem 2.3 supplies a conditional, nonindependent block criterion for infinite-horizon expected resolution. Its hypotheses allow arbitrarily long noncontracting intervals. Theorems 3.2 and 4.1 then verify substantive instances: all positive refresh rates, and a noisy contact experiment with an unknown measured calibration. The general result has both an acquired-law converse and a causal construction. The article is no longer organized around the old strongly refreshing example alone.

**For renewed review:** The claims to assess are the stated theorem class, the same-resource upper/lower conclusions, and the applications outside the previous hypotheses. The manuscript attributes the classical projective, quantization, testing, and Bellman tools and does not use their reappearance as a priority claim.

## E2. Strong refresh and nonuniform stability

**Change:** Theorem 3.2 replaces `gamma >= 4/5` by every `gamma > 0`. In projective distance the positive-likelihood Bayes step is an isometry, while the refresh transition has coefficient

`rho = (1-gamma)/(1-gamma+2 gamma/(d+1))`.

The invariant projective domain shrinks with observation strength. Its fixed cover gives one infinite-time machine. The physical Jacobian and actual report probabilities give the converse, using the floor `gamma/(d+1)`. Equation (3.4) displays both constants. Their dependence on dimension and mixing is not hidden in a fixed-d symbol.

Corollary 3.3 permits observed random refresh modes separated by unbounded noncontracting intervals. Its lower bound retains the probability of a good acquisition, and its upper bound follows from conditional second moments. It proves `sup_t E loss_t`, not `E sup_t loss_t` or a uniform bound on every path. The general suffix theorem also accommodates expanding individual steps when its stated suffix bounds are summable.

The theorem gives matching powers of signal strength and label budget at each positive refresh rate. It does not assert a sharp joint asymptotic power of gamma as gamma tends to zero; the explicit constants permit that separate question to be inspected.

## E3. The stronger A1 transfer theorem

**Change:** Corollary 2.2 recovers the exact A1 v37 anisotropic profile

`Q_t(M) = max_l ((product_{i<=l} s_{t,i})/M)^(2/l)`

and its compatible finite-horizon causal recurrence. The integer-budget argument, including small budgets and zero-width directions, is given explicitly. The A1 bounded-format covering lemma is identified as an imported geometric input; its complete source is present in `source-editions/A1-v37/text/analytic_inputs.tex`. The upstream transfer theorem is in `sections/causal_transfer.tex` of that edition.

The extension is not a claim to have rediscovered A1's G/A/C separation. It is the exact-suffix and infinite-horizon theorem, the conditional intermittent criterion, and applications with a singular acquired law. Proposition 3.4 has Cantor acquired dimension `log(2)/log(3)`, outside the finite-dimensional smooth-density example and the bounded-format geometric setting. A1's model-specific collision geometry remains credited to A1.

## E4. The eleven-paper pipeline

**Change:** The dependency audit is supplied in `HISTORY_AUDIT.md`, with immutable editions and the original acyclic order. The revision adds load-bearing resolution and statistical theorems to the G1/G2/G3 layer, rather than adding further interface names. No proof invokes a later theta manuscript to justify an earlier one.

The original Sinai/vector-roof, empirical-path and particle LDP, microcanonical, kinetic-semigroup, unbounded-domain operator, and phase-synthesis developments remain in the repository with their original dependency obligations. The present revision pursues the referee's Routes A and B, not Route C. It therefore does not infer those model-specific conclusions from finite-label filtering. Their interfaces and boundary examples have not been deleted or rewritten to look completed. This preserves the program while identifying precisely which new results are available to it.

## E5. A matched singular statistical theorem

**Change:** Theorem 4.1 starts with the actual paired observations

`Y_j = theta_j^k_j + eta_j + sigma_j Z_j`,
`W_j = eta_j + tau_j Z'_j`,

where eta is an unrestricted unknown additive calibration and both observations are charged. For the same M-label procedure class it proves

`minimax risk ~ sum_j min(a_j^2, (sigma_j^2+tau_j^2)^(1/k_j)) + Q_M(a)`.

The upper construction uses the observed differences, clipped roots, and an integer-budget anisotropic box codebook. The statistical converse chooses least-favourable calibration shifts within the actual experiment and proves the hypercube testing bound. The representation converse holds for arbitrary randomized encoders and an independent public seed. Zero-noise coordinates are covered explicitly. Constants are independent of the contact orders.

This is a matched finite-sample theorem, not only an inverse-modulus template. Its nonnegative power-coordinate parameter space is explicit. The quadratic-contact rate is compared with A2's physical-ray result; an independently noisy measurement is not identified with A2's raw contact-score statistic, and no equivalence of those distinct experiments is presumed.

## M1. Persistent labels, finite descriptions, and computation

**Change:** Section 6 gives a resource vector: persistent labels, program description, transient workspace, numerical error, and physical acquisitions. Proposition 6.1 constructs an implicit integer log-odds codebook for rational known calibration. The program generates representatives and does not store an arbitrary list of M real vectors. The number of persistent states remains at most M.

Positive-slack interval certification avoids undecidable exact comparisons at quantization ties. Numerical defects enter the proved recurrence. Command rounding has an explicit projective error bound. The construction is a finite-description and accuracy result; no unproved polynomial-time or total-bit-storage theorem is attached to the label law. Unknown calibration is paid for in Theorem 4.1, not hidden in this read-only program.

## M2. The actual command law

**Change:** Theorem 2.1 uses acquired concentration profiles and does not require Lebesgue density. Section 3 treats three distinct interfaces: continuously distributed commands, a finite command alphabet, and Cantor commands. A finite alphabet yields exact checkpoint coding once its finite history support fits the budget. Proposition 3.4 proves the singular rate `epsilon^2 M^(-2/s)` with `s = log(2)/log(3)`. The text also states how finite atoms and a singular component are accounted for without dropping mixture mass.

Adaptive upper assertions require stability under the actual lifted policy. A fixed exploration law independent of coding randomness remains the source of each lower bound. The analog converse is not silently transferred to a digitally rounded acquisition experiment.

## M3. Unrestricted optimal control

**Change:** Theorem 5.1 constructs an optimal stationary table on a finite reference decision process, lifts that table to the actual experiment, and compares its cost with the unrestricted history-dependent optimum. The proof establishes value-function and action-value regularity, bounds the finite Bellman residual, and telescopes the residual along the actual controlled path.

The exact optimal value is used only in the proof. It is not queried by the finite controller. The policy reads the current retained centre; its reference transition integrals, table precision, and transient computation are stated separately. The initial state is charged by reserving a codebook centre. This is a genuine policy approximation theorem in addition to the retained common-controller simulation theorem.

## M4. Dimension and mixing constants

**Change:** Equations (3.1)--(3.4) display the projective coefficient, invariant radius, acquired-density constant, and upper/lower prediction constants. Corollary 3.3 displays the dependence on the frequency of contracting acquisitions. Theorem 4.1 supplies explicit dimension constants and an upper bound `2S + 8d Q_M`, independent of contact orders. Theorem 5.1 displays the discount, Lipschitz, and report-kernel constants. These bounds can be evaluated rather than treated as unnamed fixed-d factors.

## M5. Structure and preservation

**Change:** The main development is now Sections 1--7: general resolution, positive/intermittent applications, singular statistics, optimal control, resource realization, and theorem-level comparison. All 32 original proof blocks and 12 boundary examples remain in the compiled appendices. The 103 labels in those retained mathematical sections resolve in the new PDF. Ten additional complete proof blocks are in the new development. The original introduction remains in the complete preserved first-edition source and PDF instead of being duplicated before the new introduction.

The title and mathematical program are retained. Reordering makes the new theorem statements and proofs prominent without erasing the foundational results.

## M6. Theorem-level literature comparison

**Change:** Section 7 compares A1's transfer theorem; nonlinear filter quantization; Kara--Yuksel, Theorems 12, 16, 17; Subramanian--Sinha--Seraj--Mahajan, Theorems 9 and 27; and A2's physical-ray and score experiments. The bibliography adds the classical projective contraction source and relevant 2024/2026 finite-memory developments.

The control theorem is explicitly described as a specialized quantitative policy-transfer result, not the first approximate-information-state theorem. The asserted contribution is the particular acquired-law and causal-resource conclusions proved here. The literature discussion is not an exhaustive priority certificate.

## M7. Stable dependencies and publication objects

**Change:** The new branch contains complete, immutable copies of A1 v37 and A2 v112, not just moving branch links. `SOURCE_MANIFEST.json` fixes their original commits and exact Git trees and distinguishes them from the new compiled source. The runner verifies the preserved trees on the executed source commit. The original v1 sources are independently checked against their original manifest.

`PROOF_LEDGER.md` distinguishes new proofs, classical inputs, the one imported geometric lemma used by a corollary, and historical model interfaces. A referee can inspect the new principal proofs without fetching a moving manuscript. The copied editions are repository editions, not invented journal publications or DOI registrations.

## Smaller comments and verification

The abstract now leads with the new quantitative results. The fixed preparation, query timing, calibration access, and resource convention occur before the principal theorem. The boundary examples remain. Build evidence is confined to the review package, not offered as mathematical validation.

The local build produced 44 pages in three stabilizing passes, with no undefined citations/references, duplicate labels, or overfull boxes. It retained the original proof blocks and passed the original diagnostics. The new diagnostic suite has 2,195 finite checks; normal and optimized Python outputs agree, and two deliberately incorrect identities are rejected. The repository runner repeats these checks on its exact source checkout and records the PDF hash and input hashes in `evidence/BUILD_RECEIPT.json`. These are reproducibility and regression checks, not a proof-assistant certificate or a replacement for the requested further referee review.
