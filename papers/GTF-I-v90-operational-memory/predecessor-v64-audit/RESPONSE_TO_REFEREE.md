# Response to the controlling referee reports — Revision 64

**Manuscript:** *Spectral Entropy, Stochastic Widths, and Uniform Streaming Space*.
**Companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.
**Controlling report:** v61/r40, commit `4a99da0aab823418d95631d5dbbd8e9b8178994d`.
**Companion audit:** commit `02c642d3c08774d2dbaee939ffb2eee57b545f92`.
**Mathematical predecessor:** v63 publication `f5c1e5d6eacecc1597fba18697a715f8e7844e09`.

The reports concern v61. Subsequent v62 and v63 manuscripts were already present remotely when this revision began. Their return-free quantitative argument, causal strong converse, subexponential matching and exponential-accuracy rate are inherited here with their complete proofs. They are not represented as new v64 results or as externally approved results. The new revision keeps the general-journal mathematical objective and responds by strengthening the connection to computation rather than by deleting conclusions or changing the submission target.

## Principal response: a separately charged computational theorem

The central model objection in §§9.1 and 10.5 of the report is well founded: a theorem about nonuniform hidden-label width is not by itself a theorem about an implemented machine's memory. We have not changed the definition of width to conceal that distinction. Section `31-uniform-streaming.tex` instead proves a separate theorem for a single uniform numerical program.

For exactly the six rational LPS Bloch rotations, a one-pass simulator with legal density-matrix outputs and Frobenius mean error `2^(-L)` requires complete-configuration bit-space of order

    min(N, L + log(N+1)),  N >= 2, L >= 2.

The lower bound allows arbitrary internal randomization and no running-time restriction. The boundary reduction integrates the algorithm's actual between-command computation into stochastic rows; every piece of persistent private information is counted. It uses conditional mean correctness, not a stronger pointwise assumption on sampled labels. The explicit finite estimate is

    N <= 1 + 6 log(12 * 2^B)
         + 648 pi^2 * [sqrt(2) epsilon / (1 - sqrt(2) epsilon)] * 2^B.

This follows from the previously proved no-idle entropy budget. The logarithmic or linear alternative gives the uniform space lower bound, including exponential and faster requested precision. The exact profile supplies the stronger endpoint count `B >= N log_2(5)` at zero error. Taking logarithms loses information: this result does not remove the subexponential multiplicative gap remaining in the v63 width theorem.

The upper bound is supplied by an actual deterministic integer recurrence. At moderate precision it applies each exact rational rotation and truncates each coordinate toward zero on a fixed dyadic grid. Absolute coordinate contraction preserves the closed unit ball, so the numerical density decoder remains positive semidefinite without eigenvalue tests or projection oracles. A telescoping norm estimate controls the error after every prefix. At very high precision, exact denominator-five numerators use only linear space and are cheaper. The theorem accounts for temporary buffers, integer signs, parameter handling, validation counters, binary output and per-command bit operations. Very large precision headers are read with a saturated counter; no enormous integer precision request must be retained. The program uses neither an external clock nor random sampling.

The rational-orthogonal corollary extends the same space order beyond the LPS example, under a full action gap and an all-direction positive-power cap law, with a rational unit seed and legal unit-ball outputs. Its proof includes the initial seed-rounding error and a fixed common-denominator exact fallback. It does not assert that coordinate truncation preserves arbitrary orbit hulls or higher-dimensional density-matrix cones.

This responds to the resource objection with an additional theorem and implementation, not with a reinterpretation of the old invariant. The elementary configuration reduction and finite-precision arithmetic are not claimed as new general techniques. The mathematical consequence is their sharp combination with the spectral entropy obstruction for this fixed experiment.

## Response to the ten required revisions

| Report item | Revision response and location |
|---|---|
| 1. Separate focused manuscripts | `quantitative.tex` and `structural.tex` remain independently proof-complete. `main.tex` preserves the combined research edition. No old mathematical section is removed. |
| 2. Independent priority review | `LITERATURE_AUDIT.md` adds primary-source, theorem-level comparisons with positive realization and quantum/weighted automata. Classical ingredients are explicitly credited. No independent human report has been obtained or invented; an author-side comparison is not described as external clearance. |
| 3. Full action gap | The abstract, quantitative introduction and streaming theorem discussion retain the full spherical Koopman hypothesis. The lower bound uses the imported six-letter LPS norm, not contraction of a three-dimensional matrix. |
| 4. Synchronization | The v62 drift-covariant proof removes identity/return assumptions from quantitative occupation. It is retained and cited as inherited. General terminal stationarization still has its own eventual approximate-return hypothesis. The uniform program uses six commands and no idle instruction. |
| 5. Resource convention on page one | The original nonuniform convention stays on page one. A separate sentence identifies the charged uniform model. Section 31 defines complete configurations, input access, randomization, legal numerical output, arithmetic and temporary storage. |
| 6. Distinct alphabets | The old rational-unitary pair retains its non-effective Bourgain–Gamburd input. The six rational Bloch matrices retain their exact LPS input. The new program uses only the latter. The seven-letter example remains an explicitly separate earlier example. |
| 7. Exact, robust and positive-error regimes | The exact `5^t` profile and `25^(-N)/16` interval, subexponential matching, and v63 exponential rate are all retained. The new bit-space law is uniform over positive dyadic tolerances and treats exact computation separately. It is not an assertion that the exact width plateau begins at a specified exponential rate. |
| 8. Repeatable-probe scope | The structural article remains a theorem about fresh nondisturbing classical probes. No irreversible, general HMM/POMDP or repeated-quantum-measurement classification is inferred from it. The new numerical streaming theorem has no probe process. |
| 9. Minimal journal bundle | The new bundle contains the focused PDFs, their active TeX proof graph, a short response and a verifier. The full combined edition and code are in a research bundle. All predecessor paths remain immutable in the repository rather than being duplicated recursively into the journal submission. |
| 10. Pipeline volume | The history audit identifies actual dependencies, not a count of revisions. The numerical-space result proves no stopped-path LDP, local-limit, filtering, Mosco, Nisio, or response gate in the independent A/B/C/D program. |

## Response to the twenty-four detailed comments

| Local comment | Treatment |
|---|---|
| 1. Invariant projection | `Pi` remains projection onto all invariant functions; no general replacement by scalar constants. |
| 2. Inverse/adjoint convention | The Peter–Weyl transfer and inverse convention are retained. The six implemented matrices are checked against the published rational input. |
| 3. Zeros of the kernel | The complete compact-support regularization argument remains in the active quantitative and complete manuscripts. |
| 4. Which entropy | The introduction distinguishes spherical relative entropy from hidden-register Shannon entropy. The new space theorem does not confuse either with a stored density. |
| 5. Direction weights | All entropy/transport lemmas retain the weights `p_s ||c_s||`. The computational reduction invokes those lemmas unchanged. |
| 6. Mean correctness | The lower theorem explicitly uses mean correctness; only the deterministic upper program supplies pointwise error. |
| 7. External word distribution | Width-dependent but private-state-independent word laws are retained. No adaptive adversarial access to private random bits is introduced. |
| 8. Hidden processing on fillers | The stronger v62 argument permits arbitrary deterministic physical drift and arbitrary hidden processing. It is not reintroduced as a v64 discovery. |
| 9. Additive logarithm | The finite bit–accuracy inequality keeps the entire `6 log(12k)` term. The dichotomy uses it, rather than dropping it near exact accuracy. |
| 10. Zero-error endpoint | Exact computation uses denominator-five integers and the exact orbit profile, not a zero-slack use of a positive-error polytope construction. |
| 11. Spectral averaging measure | The imported gap is for six nonidentity rotations. The reference parser rejects an identity instruction. |
| 12. Rational matrices | The program's finite data are rational Bloch matrices with integer numerators. No claim that their unitary lifts are rational is added. |
| 13. Coset count | The cyclic-stabilizer proof and exact right-coset profile remain intact. No free-group ball count is substituted. |
| 14. Oriented seed | The exact stabilizer remains the stabilizer of the vector `e_1`, not the unoriented axis. |
| 15. Explicit constants | The inherited constant 6500 is not called optimal. Section 31 retains the more informative finite entropy constants and does not claim sharp leading bit constants. |
| 16. Causal threshold | The stronger v62 tail-capacity theorem establishes eventual minimum for each error below one. The earlier one-half result remains as an inherited weaker result, not the final limit of the theory. |
| 17. Common itinerary | The common diagnostic schedule and its proof are retained without pair-specific incompatible continuations. |
| 18. Rare prefixes | Prefix observations are marginalized in the causal lower argument; no conditional accuracy on a rare observed prefix is assumed. |
| 19. Auxiliary law | The adaptive compiler's coupling is still a proof device, not free computational memory. |
| 20. Strict probe positivity | The KL compiler retains strict positivity of affine probe laws. |
| 21. Output and random-bit resources | Numerical matrix output, sampled probe output and physical quantum preparation remain separate. The new upper algorithm is deterministic and outputs a rational numerical matrix. |
| 22. Exact final-head evidence | A contents-read-only workflow rebuilds the exact pushed v64 commit. Source and PDF hashes, isolated rebuild and tests are checked. No cryptographic authorship claim is inferred. |
| 23. Scope of finite tests | New tests exercise exact integer identities, all six-letter words through length five, long streamed words, parser rejection, output legality, signed-rounding failures and precise rational error bounds. Neither those tests nor inherited checks prove the universal entropy or LPS theorem. |
| 24. Meaning of sharpness | The new sharp result is a two-parameter space-order equivalence for a fixed rational experiment. It is distinct from optimal leading width constants and a multiplicative equivalent through the width transition. |

## Theorem-level priority boundaries

The active paper now compares the new result directly with Benvenuti–Farina's invariant-cone theorem for positive realization, Ambainis–Watrous's two-way quantum/classical automata, and Panduranga Rao–Vinay's complex-weighted simulation theorem. The input access, positivity, output criterion and arithmetic costs are different in each comparison. The comparisons identify which inference is not licensed by each cited theorem; they do not purport to rule out every equivalent formulation in the literature. The earlier entropy, nonbacktracking, arithmetic gate and nonhomogeneous-chain comparisons remain available and are not suppressed.

In particular, keeping a three-dimensional real amplitude vector is not a constant-bit classical realization. Conversely, the manuscript does not claim that all quantum automata need our amount of numerical simulation memory for language recognition. The theorem concerns one precise all-word numerical task. This makes its content testable without using a larger application claim as a substitute for a proof.

## Preservation, proof and evidence

The predecessor native archive at v63 has Git blob `d8b3e752460b1b2f8a453b99926bbf722b21d08a`. Its 478 files are listed by SHA256 in the preservation manifest and remain at their existing repository paths. All prior active proof labels are retained in the new combined manuscript. The added mathematical labels and the exact locations of new versus inherited results appear in `PROOF_STATUS.json` and the build's label inventory.

The source verifier distinguishes manuscript proof, finite regression, typesetting and source identity. It does not manufacture a referee endorsement, independent priority finding, universal proof-assistant verification, journal acceptance or an analytic-pipeline completion flag. Those are different assertions from the written and executed results supplied here.
