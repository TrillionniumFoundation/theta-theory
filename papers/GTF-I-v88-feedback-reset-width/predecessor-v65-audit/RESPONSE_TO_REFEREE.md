# Response to the v64/r41 referee reports — Revision 65

**Quantitative manuscript:** *Positive Streaming Simulation and Spectral Space Bounds*.
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.

The controlling external report is `GENERAL_THETA_FOUNDATIONS_I_V64_REFEREE_REPORT_R41.md` at `bee28d9c8af25880c548b4650f2fdc7eacbdf8af`; the companion proof/pipeline audit is at `7284bc1e406665a8f89edf2741abdd5e71e8555d`. Both review the v64 final head `abd5600b0085463ff78a1525d9588f42c8a514d5`, the base of this revision. The new remote work anchor is `c380b067d51bae80d4e20297b96b4563e6c26835`.

The report finds no fatal gap in the audited v64, v62 and v63 arguments. Its objections concern breadth, the distinction between label width and implemented space, a residual crossover gap, the scope of repeatable observations, and incomplete current-literature comparison. We retain the mathematical objective and all predecessor theorem sections. The response adds a positive matrix-state construction and a disturbing-instrument theorem, rather than renaming a Euclidean-ball algorithm or silently changing the earlier hypotheses.

## Principal mathematical changes

### Positive outputs beyond the Bloch ball

Section `32-positive-density.tex` proves a fixed-denominator map on the full density-matrix set. For a trace-preserving Hermitian grid approximation Q_B(rho), put

    R_B(rho) = (B Q_B(rho) + 2d I)/(B + 2d^2).

The output is positive semidefinite of trace one, with trace-norm error at most `6d^2/B`. The proof gives the norm estimates and an explicit integer algorithm. It requires no spectral decomposition, eigenvalue clipping, cone-membership oracle, or barycentric orbit-hull table. A rational two-dimensional counterexample shows why the diagonal correction cannot be omitted. The map is a numerical operation, not an affine quantum channel.

### Disturbance, adaptation and rare outcomes

Section `33-adaptive-instruments.tex` constructs one fixed program for every fixed finite Gaussian-rational Kraus description. The simulator emits each outcome as the command arrives and maintains a legal numerical density matrix. Irreversible channels, projective measurements, multiple Kraus operators per outcome and zero-probability outcomes are allowed.

The error is the trace norm of the difference of the classical–quantum history blocks. Positive homogeneous branch repair and the classical instrument contraction inequality give

    D_(t+1) <= D_t + 6d^2/B.

This avoids a lower bound on outcome probabilities and avoids asserting normalized conditional accuracy after a rare history. The resulting bound holds for every prefix and every common adaptive classical controller. Classical transcript total variation and common terminal-measurement error are at most half the classical–quantum bound.

Integer interval sampling realizes the actual rational outcome probabilities using fresh fair bits and rejection, almost surely terminating with bounded space. Exact unnormalized Gaussian-integer branches provide an `O(N)` fallback. Choosing the smaller construction yields

    O_input(min(N, L + log(N+1)))

writable bits at error `2^(-L)`. The theorem accounts for integer products, divisions, temporary buffers, capped parameter input, command counting and numerical output. It is not a total-variation assertion about binary encodings of approximate matrices, an arbitrary external-entanglement simulation, or a physical state-preparation procedure.

This answers the observation-scope objection with a separate constructive result. It does **not** remove the fresh nondisturbing-probe premise from the inherited finite-response-quotient classification.

### Sharp matrix-output space in every fixed dimension

Section `34-matrix-space.tex` combines positive matrix rounding with the existing return-free entropy obstruction. Center a density matrix at `I/d` and divide by `sqrt((d-1)/d)`. Every legal decoder then has norm at most one, and a pure target has norm one. Under the explicit full action gap and all-direction cap hypothesis, the inherited occupation proof gives

    N <= C0 + C1 log k + C2 epsilon k^(2/p).

The complete-configuration reduction and the logarithmic-or-linear alternative give the matching fixed-program space lower bound. A deterministic rational channel simulation supplies the upper bound with pointwise trace-norm error. The explicit adjacent-coordinate rational unitary family already present in the pipeline therefore has the same sharp space order in every fixed dimension. Its gap is an imported algebraic spectral result, not a new numerical constant.

The lower-bound constants for a conventional work-tape machine may depend on its fixed finite control; no pointwise minimization over different uncharged programs for every pair N,L is intended. Instrument families containing such a unitary subsystem inherit sharpness when the interface includes a legal numerical matrix. No matching lower bound is claimed for transcript-only simulation of every noisy channel.

### Current literature and semantics

Section `35-cutpoint-comparison.tex` adds the requested Chen–Wu papers at exact versions and gives a sign-preserving attenuation proposition. A strict-cutpoint language can be preserved while numerical acceptance values change substantially. Conversely, numerical approximation preserves a decision only when the error is smaller than the cutpoint margin. This identifies why sign-pattern obstructions and calibrated mean-output obstructions cannot simply replace one another.

The April paper's August v2 has the revised title *The State Cost of Classical Simulation of One-Way General Quantum Finite Automata* and the exact value `n^2+1` for `n>=2`, not only the quadratic-order statement in the report. The n=1 exception is not silently included. Primary sources and theorem numbers are recorded in `LITERATURE_AUDIT.md`. No independent expert opinion is represented as having been obtained.

## Response to the fourteen required revisions

| Item | Treatment |
|---|---|
| 1. Current 2026 comparisons | Section 35 and the literature audit use Chen–Wu April v2 and May v1, with strict-cutpoint semantics, numerical error and implementation resources explicitly separated. The attenuation proposition addresses transfer of proof techniques. |
| 2. Separate width and charged space | The primary definition and page-one resource convention remain. Sections 31 and 33–34 use a separately specified fixed-program bit model. Arbitrary real tables are not retroactively priced. |
| 3. Fixed finite program | The abstract, introductions, new theorems and input protocol all retain this quantifier. Lower work-tape constants may depend on the fixed program. Finite control depending on N,L is not free. |
| 4. Fixed rational-orthogonal data | The inherited corollary now repeats dimension, alphabet, denominators, seed, cap and gap dependence. The new matrix theorem states the same fixed-input convention in its statement. |
| 5. Crossover uncertainty | The v63 theorem and its subexponential multiplicative factor remain unchanged. Neither the new positive construction nor taking logarithms removes that factor or identifies the exact saturation window. |
| 6. Full action gap | The matrix converse assumes the full Koopman gap off all invariant functions. The positive upper construction requires no spectral hypothesis. The LPS and algebraic SU(d) imports remain distinct. |
| 7. No-idle versus stationarization | Quantitative drift covariance remains return-free. General terminal stationarization retains eventual approximate returns. The instrument upper theorem does not invoke stationarization. |
| 8. Structural observation scope | The finite-state classification still concerns fresh nondisturbing classical probes. A separate rational-instrument approximation theorem now admits genuine disturbance without pretending to classify all such processes. |
| 9. Separate articles | Quantitative and structural entry points remain independently proof-complete. The combined edition is archival and contains all previous active mathematical labels. |
| 10. Journal-facing provenance | The abstracts and introductions foreground mathematical problems, estimates and constructions. Commit genealogy and regression records are in separate documents; the minimal journal archive needs no historical PDF. |
| 11. Bibliography | BF04 is the single canonical Benvenuti–Farina key; BF64 citations are redirected. PLP arXiv v2 Theorem 1.1 (one-step LPS) and Theorem 1.2 (radial norms) are explicitly distinguished. |
| 12. Independent priority opinions | The author-side comparison is expanded and accurately labeled. Independent human priority opinions have not been obtained or fabricated; this request remains an external assessment, not a theorem premise. |
| 13. Exact-head attestation | Source-bound publication and a separate contents-read-only exact-final-head workflow are retained. Native sources, PDFs, short journal archive and their hashes are committed, not available only as expiring Actions artifacts. |
| 14. Signed release | Signing is optional archival hardening. No new unauthenticated key is created or attributed to the author. Unsigned commits are not called signed; an existing authorized signing facility would be needed for an author-signed tag. |

## Response to the twenty-four detailed comments

| Comment | Treatment |
|---|---|
| 1 | Complete private configurations remain the primitive in the inherited boundary lemma and the new matrix lower proof. |
| 2 | The induced stochastic boundary row may depend on the public boundary index; the new proof says explicitly that this enlarges the lower-bound comparison class. |
| 3 | Almost-sure termination is retained for all boundary rows. The new sampler has an explicit acceptance probability exceeding one half and requires no counter of rejected trials. |
| 4 | The lower matrix theorem assumes only mean correctness. The deterministic channel upper bound supplies the stronger pointwise trace guarantee. |
| 5 | Every numerical output is legal samplewise; the positive rounding lemma proves this rather than hiding illegal values by averaging. |
| 6 | The explicit two-word one-configuration witness in Section 31 is retained unchanged. |
| 7 | N is stored, L is scanned with saturation at N, and the input string length is charged to reading time rather than assumed resident. |
| 8 | The new program also emits fixed-radix hexadecimal integers; the theorem uses equivalent binary bit lengths. |
| 9 | Both reference programs disclaim allocator-level CPython optimality. The new program also distinguishes ideal fair bits in the theorem from practical OS entropy. |
| 10 | New finite tests check exact matrix identities, positivity, trace-norm enclosures, adaptive tree bounds and register sizes. The written arguments, not a finite horizon list, establish universal statements. |
| 11 | The b>=N mode switch remains an order-level choice. Exact and approximate costs are not asserted to be pointwise optimal for small inputs. |
| 12 | The existing LPS coset profile, oriented-seed stabilizer and right-coset convention remain adjacent and unchanged. |
| 13 | The robust exact-profile interval still depends exponentially on N. It is not interpreted as fixed-positive-error exponential width. |
| 14 | The exact-profile and positive-error proofs remain separately identified. |
| 15 | Formal reduced words and the nonbacktracking operator recurrence are unchanged, including the treatment of physical relations. |
| 16 | The full invariant projection is retained in the entropy argument and explicitly required in the new matrix theorem. |
| 17 | The auxiliary spherical entropy is not a stored register or Shannon entropy. The new process theorem instead uses subnormalized matrix trace distance. |
| 18 | Observation-tail capacity remains a statement about tail events. It is not invoked as a lower bound for arbitrary quantum instruments. |
| 19 | The inherited repeatable-probe strong converse keeps the error threshold one; the earlier one-half theorem is retained as a weaker historical result. |
| 20 | The quantitative abstract leads with charged matrix space and positive instrument simulation, then gives the accuracy crossover with its remaining factor. Preservation statements are outside the abstract. |
| 21 | The unit-ball corollary still simulates a rational linear orbit directly. The new density-matrix construction replaces its positivity mechanism instead of claiming coordinate truncation preserves a PSD cone. |
| 22 | Both algorithms return numerical density matrices, not physical preparations. |
| 23 | No time lower bound is introduced. The new upper sampler has expected time bounds; the converse allows unlimited internal time. |
| 24 | The final verifier writes its attestation outside the attested tree and has no repository write permission. |

## Preservation and the next review

All 71 v64 native files remain at their original repository paths, and all 321 prior active mathematical labels remain in the complete v65 proof graph. Every applicable prior label remains in each focused article as well. Changes to introductions, bibliography aliases and resource clarification are recorded, not used to delete proofs. The earlier historical audits and the frozen Round-Seventeen analytic ledger were consulted; the local new instrument theorem supplies no bridge to the independent local-limit, stopped-LDP, filtering, Mosco, Nisio or response gates.

The build and exact regression receipts report only executed source and implementation evidence. They do not turn this author response into independent priority clearance, a proof-assistant certificate or a journal decision. The mathematical additions are complete written arguments for another referee to inspect; the journal objective has not been changed.
