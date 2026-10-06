# Response to the v65/r42 reports — Revision 66

**Quantitative manuscript:** *Reference-Stable Rational Instruments, Positive Streaming, and Spectral Space Bounds*.

**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.

**Reviewed predecessor:** `34e5719ce5c7109c8c31f98079716b8ce6dcfffe`.
**Controlling external report:** `5c0796bc1f0ea24d379dfd28888f16d88315a525`.
**Companion proof/pipeline audit:** `b5d71e67b879f9ada861993caedf8151734f85ba`.

We thank the referee for separating the correctness assessment from the questions of scope, priority and significance. The present revision retains the general-journal objective and all previous mathematical results. It addresses the reference-system and fixed-input objections with two additional constructions, rather than by changing the meaning of the earlier theorems. The prior spectral, realization and causal arguments remain part of the active complete edition. The structural article no longer duplicates the computational instrument sections, which remain fully proved in the quantitative article and the complete edition.

## Principal mathematical changes

### 1. Rational instrument descriptions with a diamond-error bound

The old positive map `R_B` acts nonlinearly on a stored numerical state. It cannot be tensored with an identity on an unknown entangled reference. We have not attempted that invalid extension.

Section `36-reference-instruments.tex` instead repairs an instrument's Choi description once, independently of its input. For input dimension `d`, output dimension `n`, `m` outcomes and Hermitian grid approximations at coordinate error at most `1/B`, set

    c = 2nd(1+mn),   D = B+mnc.

A single integral partial-trace correction, followed by a scalar diagonal buffer and normalization, produces positive Gaussian-integer Choi numerators over denominator `D`. Their summed output partial trace is exactly the input identity. The instrument diamond error is at most

    3mndc/(B+mnc) <= 6mn^2d^2(1+mn)/B.

The proof supplies the full tensor convention and an elementary Choi/diamond bound for arbitrary reference dimension. It does not require a spectral projection, a Kraus factorization over the rationals, or a spectral gap. The grid may be dyadic, but the repaired denominator generally is not; the theorem deliberately says rational, not dyadic.

The companion adaptive comparison retains arbitrary quantum tester memory, an initially entangled state, common feedback operations and bounded public stopping. Choosing each one-use error at most `2^(-L)/N` bounds the stopped joint-state trace error by `2^(-L)`, with transcript total variation at most half that amount. This is a theorem about genuine approximating channels and their operational distance, not a claim that a classical computer accepts an unknown physical quantum state and prepares its replacement. Numerical simulation of a specified tester charges the joint dimension.

The Choi criteria, channel hybrid argument, and mixing with an identity buffer are classical. The manuscript now compares the explicit arithmetic formula directly with projected least-squares channel estimation, rather than claiming the general correction principle as new.

### 2. One numerical program with variable dimension and rational Choi input

Section `37-uniform-choi-streaming.tex` allows the instrument description and dimension to vary as part of the input. It directly contracts rational Choi coefficients with the stored matrix. No rational Kraus factorization is inferred from a rational channel matrix.

For total description length `S`, dimension `d`, maximum denominator bit length `H`, initial trace length `ell_0`, horizon `N` and precision `L`, put

    Q = ell_0+NH,
    b = L+ceil(log_2(6d^2(N+1))),
    u = min(Q,b).

After polynomial-time, polynomial-space input validation, the streaming stage uses

    O(S+d^2[H+log(d+1)+u]+log(N+1))

writable bits, with a fixed encoding and an absolute implicit constant. Validation is separately charged, and the total peak includes its polynomial workspace. Exact mode retains unnormalized positive numerators; grid mode retains the earlier fixed state denominator. Outcomes are sampled from exact integer weights computed from the stored approximate state. The whole subnormalized history error remains at most `2^(-L)`, including zero and arbitrarily rare outcomes.

The new validator uses reduced rational Schur complements. It does not reuse the unreduced scaled Schur recursion of the fixed-dimensional implementation as an unproved polynomial-in-dimension procedure. Expected time and fresh-bit use remain separate from worst-case storage on each rejection trial.

This is an explicit variable-input upper bound. The fixed-program spectral lower theorem remains fully stated under its original assumptions and is not falsely extended to every noisy transcript-only task.

### 3. Posterior guarantees at a chosen stopping time

The new posterior proposition converts a subnormalized block error `delta` into

    E_true ||rho_h-rhohat_h||_1 <= 2 delta,
    P_true{||rho_h-rhohat_h||_1 > eta} <= min(1,2 delta/eta).

For an event of true probability `alpha`, pooled conditional-state error is at most `min(2,2 delta/alpha)`. The estimates apply at a common bounded public stopping time without a union bound over all previous times. This provides a quantitative posterior conclusion, while preserving the distinction from a guarantee on every rare history. The explicit rare-event regression has global error tending to zero and conditional error two, so the distinction is not merely verbal.

## Responses to the fourteen required revisions

| r42 item | Change and exact location |
|---|---|
| 1. Separate products | `structural.tex` no longer loads Sections 32–33; both are still loaded by `quantitative.tex` and `main.tex`. The preservation manifest records all 16 relocated prior labels and checks both destinations. No mathematical source is deleted. |
| 2. Operational interface | The quantitative abstract and page-one convention distinguish rational channel descriptions with diamond control, numerical trajectory states, and the inherited numerical-output lower bound. Sections 36–37 state the reference and tester costs explicitly. |
| 3. Fixed-input convention | The old fixed-input theorems remain unchanged. The new `thm:uniformchoi66` gives a separate variable-description result with `S,d,H,ell_0` and preprocessing costs. |
| 4. Fixed-program lower quantifier | The introduction and Section 37 explicitly retain program-dependent lower constants and starting horizons. No minimization over arbitrary free hardwired programs is asserted. |
| 5. General upper versus conditional lower | Both new upper constructions need no gap. The existing lower theorem still requires an expanding unitary subsystem and a legal numerical matrix interface. |
| 6. Expected and worst-case resources | `thm:uniformchoi66` and the schema state expected time/fair-bit use, almost-sure termination, and worst-case trial storage separately. No time lower bound is added. |
| 7. Rare outcomes | `prop:posterior66` supplies true-law expectation, high-probability and event-conditioned bounds. Zero simulated mass is treated without dividing by zero; no every-rare-history guarantee is claimed. |
| 8. Quantum trajectory/filtering comparison | `LITERATURE_AUDIT.md` and the quantitative comparison discuss Rouchon–Ralph, Section II, equations (10)–(13), and distinguish time discretization from finite-integer precision and subnormalized history control. |
| 9. Current literature versioning | The retained Chen–Wu comparison pins `2604.07058v2` and `2605.10682v1`; their current version histories were rechecked on 29 September 2026. The predecessor audit retains the exact theorem numbers. |
| 10. Full-action gap | The new constructions do not invoke the gap. The inherited lower conclusions continue to cite it as an imported hypothesis, not a finite-test output. |
| 11. Crossover gap | The abstract and proof-status file retain the `exp(O(sqrt(N log N)))` multiplicative uncertainty in v63 label width. Neither the diamond compiler nor the space theorem closes that gap. |
| 12. Independent priority | A broader author-side comparison is supplied, including the close Choi-repair antecedent. No independent human report has been commissioned or fabricated; that requested external assessment is not represented as completed. |
| 13. Attestation | The source-bound build and the subsequent read-only exact-head reconstruction remain separate. They establish provenance/reproduction, not universal proof, priority, or journal acceptance. |
| 14. Wider pipeline | The frozen ledger and history remain. No analytic A/B/C/D aggregate flag changes; the local stopped finite-dimensional estimate is not a stopped-path LDP or a filtering/LAN theorem. |

## Responses to the twenty-four detailed comments

| Comment | Treatment |
|---|---|
| 1. Last diagonal of `Q_B` | A small correction to the suggested wording is necessary. On a density input, the actual directed-truncation definition gives `0<=Q_dd<=1`: all other diagonal entries are nonnegative and their sum is at most one. `rem:diagonal66` proves this. The rounded matrix can still be indefinite because of its off-diagonal entries; the existing rank-one counterexample is retained. We therefore do not insert the false scalar claim. |
| 2. Loose constants | The new remark and Choi theorem identify safe, nonoptimized constants; no optimal leading coefficient is claimed. |
| 3. Positivity versus CP | The inherited direct-sum proof retains its weaker positivity/trace premise. The new reference theorem requires complete positivity and proves it through positive Choi matrices. A transposition-map negative control separates these conditions. |
| 4. Zero outcome schema | `CHOI_INPUT_SCHEMA.md` documents both representations: an explicit zero matrix in a nonempty Kraus list for v65, or a zero Choi block for v66. |
| 5. Trace-norm normalization | All new formulas use unhalved trace norm and transcript TV at most half the bound, including in the abstract/interface discussion and tests. |
| 6. Same controller | `thm:adaptivediamond66` allows arbitrary quantum memory but compares the same tester. Numerical streaming retains the same classical adaptive controller; there is no private-state oracle. |
| 7. Approximate branch weights | The numerical proof and code explicitly use weights computed from the stored approximate state. The block recursion is the implemented law. |
| 8. Initial repair | The bound `(t+1)6d^2/B` remains explicit in `thm:uniformchoi66`; a description-only diamond comparison starting from the same input has no artificial state-rounding term. |
| 9. Rejection runtime | The theorem retains almost-sure termination and expected runtime. Rejected words are discarded; no unbounded trial counter is stored. |
| 10. Unnormalized exact state | `lem:choitrajectory66` explicitly states cancellation of accumulated denominator factors. Exact mode retains the selected numerator and divides only when interpreting the output. |
| 11. Fixed denominator | The state grid denominator `B+2d^2` and the different channel-description denominator `B+mnc` are explicitly separated. |
| 12. Mode choice | The proof says the switch is an order-level choice and not a small-instance optimizer. |
| 13. Randomness | The reference CLI states that OS randomness implements the recurrence but is not an ideal-fair-bit certificate. Regressions use deterministic supplied bits. |
| 14. Output correctness | The old lower theorem remains mean Frobenius with samplewise legality; the one-outcome numerical upper bound remains deterministic trace-norm accuracy. The new process theorem has its own subnormalized metric. |
| 15. Residual amplitude | The inherited matrix-space theorem retains `L>=2` and its fixed-dimensional normalization. Neither new upper result silently invokes that residual estimate. |
| 16. Fixed finite program | The variable-input upper uses one actual program; the inherited lower remains asymptotic for each fixed program. These two quantifiers are not conflated. |
| 17. Explicit alphabet | Explicit input matrices are not renamed numerically certified expansion. The general algebraic gap remains qualitative. |
| 18. Matrix interface | No transcript-only lower bound is inferred. The new reference-stable instrument comparison is an upper approximation theorem, not a replacement lower interface. |
| 19. Attenuation | Section 35 is retained as a semantic separator; no new automata simulation priority is claimed for it. |
| 20. Threshold margin | The effect-margin proposition is unchanged. Norm approximation and strict-cutpoint sign preservation remain different. |
| 21. Structural abstract | The disturbing-instrument construction is removed from the structural abstract and full constructive sections relocated to the quantitative/complete editions. The finite-response classification still concerns repeatable nondisturbing probes. |
| 22. Archival edition | `COMPLETE_REVISION.pdf` preserves all development. The journal package contains only the two focused proof graphs and their current artifacts. |
| 23. Signatures | No author signature is fabricated. The immutable source/publication/request chain and read-only attestation are retained as provenance. |
| 24. Finite tests | New exact tests cover repair, Choi tensor conventions, entangled/stopped comparisons, state updates and malformed certificates. Their scope explicitly excludes universal mathematics, spectral certification, formal machine-space verification and priority. |

## Remaining questions and release object

The new results remove the absence of an external-reference-stable instrument-description approximation, and provide an explicit variable-data numerical upper bound. They do not claim a general disturbing-process finite-state classification, a sharp lower bound for every noisy transcript-only instrument, optimal dimension dependence, an optimal leading constant, or a multiplicatively sharp v63 crossover. No theorem has been discarded or weakened to obtain this distinction.

All 85 predecessor native files remain at their prior repository paths. Their exact hashes and the 347 prior complete-edition labels are checked separately from the intentional focused relocation. The final referee object is the newly published revision branch at a single exact commit, with complete written proofs, source-bound PDFs, the code and actual build/reconstruction receipts. Independent priority and the editorial decision remain questions for the next referee, not outcomes manufactured by the source verifier.
