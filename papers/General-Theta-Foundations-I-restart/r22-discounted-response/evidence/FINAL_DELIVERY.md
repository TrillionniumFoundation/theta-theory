# Final delivery — General Theta Foundations I restart R22

This is a substantive revision against the R20 external report, not a replacement of the General Theta mother problem by a realization. All assertions below refer to the explicitly declared experiment/controller classes. The native paper contains complete proofs for those assertions, subject to independent mathematical scrutiny.

## New general mathematics

Write `V_beta^Theta(M)` for the robust total discounted risk of one stationary M-state controller, chosen before an inaccessible parameter theta fixed along the path. The raw input consists of actual finite-intervention report laws and scored-response submeasures from prepared positive causal kernels. Under finite-history product domination and compact continuous decisions, Theorem 2.2 proves attainment by one Borel controller and

```
V_beta^Theta(M) = sup_{nonempty finite F subset Theta} V_beta^F(M),
V_beta,N^Theta(M) <= V_beta^Theta(M) <= V_beta,N^Theta(M) + beta^N.
```

Proposition 2.3 proves the load-bearing topology: L1 tensor tests make repeated controller rows continuous at distinct report coordinates. This extends the earlier finite-horizon finite-dimensional physical argument; it does not assume pointwise multiplication is weak-star continuous. Arbitrary Theta is permitted at this exact layer. Compactness and finite-intersection are credited as standard tools; no witness-cardinality bound or minimax exchange is inferred.

Theorem 3.3, under separate effective certificates, proves

```
max(0, L-E_N-B_N) <= V_beta^Theta(M)
                  <= min(1, U+Omega_N(s)+beta^N),   U-L <= zeta.
```

The lower end holds against every legal Borel controller, not only the enumerated grid; the upper end is implemented by a common finite table with the same M states. E_N, B_N, Omega_N, zeta and beta^N respectively account for response coarsening, row/readout rounding, raw-model approximation, certified evaluation and temporal tail. The proof supplies the complete finite list, not a practical complexity claim. No hidden phase, exact posterior or true-parameter readout is available to the machine. Equal active report supports are unnecessary because every primitive action is always legal in this continuing interface. This does not remove the inherited exact-deadline support assumptions.

For unstable raw couplings with expansion L>1, Theorem 4.2 gives a controller-uniform model modulus of order s if beta L<1, s(1+|log s|) at beta L=1, and s^{log(1/beta)/log L} if beta L>1. A controlled logistic family with moving interval-report supports verifies the assumptions. These orders are sharp for the stated raw-modulus class, not a claim that its memory problem is always difficult or that constants are uniform as beta approaches one.

## Two raw realizations and acquired geometry

Theorem 4.1 derives the response hypotheses from arbitrary nonlinear standard-Borel hidden-state dynamics with dominated conditional observations, including Gaussian full tails, moving supports and non-finite-dimensional physical states. It does not assume a finite-dimensional filter or contraction. Effective synthesis still requires additional uniform computable certificates.

Theorem 4.3 independently derives the same general hypotheses from noncommuting positive quantum instruments. The proof uses unnormalized completely positive maps and trace bounds, allowing projective zeros, pure preparations and changing rank. Physical quantum state is not free observer memory: M counts the classical controller states. Only an actually selected terminal audit is scored; incompatible unperformed earlier audits are not jointly assumed.

Corollary 4.4 handles Cantor/countable/tagged singular report references with actual masses. Separately, the direct blind-preparation theorem gives, for every beta and M,

```
V_beta^Theta(M) = min_{c_1,...,c_M} sup_theta
                  integral min_j ||x-c_j||^2 mu_theta(dx).
```

Here mu_theta is the actual prepared/acquired law, not a formal reachable set. The same formula is the checkpoint risk. The class includes a genuinely nondominated family of preparations; this direct proof is not a nondominated extension of the general compactness theorem. Actual submeasure mass m, an s-dimensional small-ball bound and a global cover give matching M^{-2/s} bounds, retaining the m-dependent constant. Middle-thirds Cantor preparation is verified rather than asserted as an interface. Exact quantization retains anisotropy without substituting ambient dimension.

## Continuous matching curve and fully completed certificate

Proposition 7.1 starts from iid fresh fair bits and the continuous raw likelihood

```
g_p(y|x)=1+(2x-1)p(2y-1),  y in [0,1],  p in [p0,p1] subset (0,1).
```

One parameter-independent M-cell controller attains

```
V_beta(M) = 1/4 - (p0^2/12)(1-M^{-2}),
V_beta(M)-B_* = p0^2/(12 M^2),  B_* = 1/4-p0^2/12.
```

A true invisible offset in the scored target adds exactly delta^2 in the declared enlarged readout space. This is an attained calibration alternative, not an allowed numerical error automatically promoted to a lower bound.

For beta=1/2, M=2, p in [1/4,1/2], two report cells, Q=2 and readouts {7/16,1/2,9/16}, all 729 finite tables are evaluated with rational arithmetic. Endpoint maximization is exact because the stationary resolvent risk is affine in p. The selected deterministic table overwrites its state with the current report half and reads out 7/16 or 9/16; L=U=63/256. The supplied generic report allowance is 1/64, yielding [59/256,63/256]; a separate continuous-parameter all-Borel lower proof tightens it to [63/256,63/256]. An extra cell-optimality proof justifies zero value-rounding allowance for this instance; it is not uniform closeness of every Borel row at Q=2. Exact infinite resolvent evaluation eliminates a truncation term for this instance.

## Error and full resource accounting

Theorem 6.1 composes scored-prefix causal simulation with S internal states by multiplying controller state to MS, using the stated source-call completion bound C(t), and adding discount-weighted prefix defects. Reverse lower transfer needs a reverse simulator. Model error, report-classification error and output numerical error retain their own moduli. Program description, workspace, random sampling, lookup cost and physical time are separate resources.

Proposition 6.2 realizes sharp irreversible-erasure amplification: failure probability e before each operating call gives the exact three-readout risk e/[4(1-beta+beta e)], against an ideal two-readout zero risk. The identity-comparison prefix TV is 1-(1-e)^t; no unsupported minimum-deficiency claim is made. A geometric scoring selector has mean 1/(1-beta) calls and is external scoring machinery, not a free internal clock. N in the general effective theorem is a prefix approximation length, not a hard acquisition budget. At beta=1/2, expected two calls does not mean at most two calls.

## History and proof gaps

Complete R20 and earlier articles are preserved in A/X/W/V/U/T/S; controls and all inherited child trees are unchanged by Git identity. Unified or connected: executable-test equivalence, actual conditional pooling, common-parameter controller quantifiers, finite-state risk transfer, actual-law quantization and typed causal simulation. Ordered-measurement/reset discrimination, finite actions, streaming/spectral space and older causal-memory realizations remain independent with original hypotheses, and are not reverse premises of the new theorem.

Still unproved: arbitrary nondominated controller compactification; a universal intrinsic numerical frontier or quotient realization; general unknown-kernel learning/regret; average cost and unbounded internal stopping; a general hard-N adaptive resource law combining every cost; efficient global synthesis and a matched optimal region for program length, workspace, planning/physical time and minimum simulator state. Full line-by-line rereview of all v1–v96, every report/pipeline and every realization was not completed; actual targeted coverage is documented in HISTORY_COVERAGE.md.

## Delivery identities and verification

Ordinary source: `9e57657bc82cd61fcf11d196a747e7e66793e5bd`; native tree `87751144b2241f66757cb67298b1c46326b03d9f`.
Artifact direct child: `7cd3ad1a5edb0670280617aa81861e78dc066f94`.
Final evidence identity: the append-only commit containing this file, to be read back from all three delivery refs.
Hosted run: `37906167388`, successful; downloaded artifact `11604811816`.

Both environments passed 22 isolated builds with three TeX passes each; normal/optimized regression parity; 3,694 native assertions; full inherited regression chain; source inventory, labels and references. Native source: 31 ordinary files plus manifest, 10 TeX inputs, 48 labels, 57 cross-references, nine bibliography entries, 15 formal statements. All 526 downloaded input files were unchanged. Eight PDFs contain 234 pages; all normalized text and RGB page pixels agree across environments at the recorded renderer/resolution. Cross-environment PDF bytes differ, whereas same-environment repeated builds are byte-identical. All 16 native pages were visually inspected. No undefined references or overfull boxes remain. Builds and finite tests are not continuum proofs or evidence of journal acceptance or independent priority.
