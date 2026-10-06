# Referee Report — General Theta Foundations I, Revision 88 (r58)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed branch:**
- `revision/general-theta-foundations-i-v88-r57-response-2026-10-05`

**Reviewed publication head:** `d1add4a7ba45230b3cba71b47ef46da5e4a88d72`  
**Qualified native source:** `cebd9b28f8ea603fa98c8c5c8f70d9e1daafb3d1`  
**Completed predecessor:** Revision 87, `aab076189b7276f6a0b4113b472ea09a7ac640cc`  
**Controlling external report:** v87/r57, `796657054bac22426f33520474e4b6020892ee32`  
**Controlling proof/pipeline audit:** v87/r57, `0546af1e2f9caebbbc29376e9eee192440f2e1a2`  
**Source qualification and publication workflow:** `37313946295`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v88-feedback-reset-width-external-referee-r58-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 88 is a real and technically coherent advance over Revision 87. The manuscript now treats a resource class strictly richer than independent entangled blocks and strictly smaller than unrestricted adaptive acquisition: classical feedback is permitted between fresh blocks, arbitrary coherent adaptive control is permitted inside each block, and the receiver may preserve arbitrary quantum memory throughout, but the complete next probe–reference system must be conditionally independent of all old receiver memory. The paper proves that this reset-constrained feedback class obeys the same sharp three-row local width law as the independent block class:

```text
regular tangent:       min{1, sqrt(N) s},
coherent tangent:      min{1, sqrt(N b) s},
support opening:       min{1, N s}.
```

The proof addresses the main logical difficulty correctly. Once feedback is introduced, the two output states are not unconditional tensor products and the v87 fidelity-multiplication argument cannot simply be repeated. Revision 88 instead proves a conditional root-fidelity induction on subnormalized receiver states. Fidelity is multiplied only when a fresh complete block is appended in tensor product with old receiver memory; after the receiver instrument, direct-sum additivity and monotonicity are used, followed by a continuation induction at each classical outcome. I find this architecture sound.

I did not find a fatal mathematical gap in the new Section 79. In particular, the following points are coherent in the form submitted:

1. the definition of reset width on complete probe–reference systems rather than on probe marginals alone;
2. the requirement that the conditional preparation rule be common under both hypotheses, including at histories null under one of them;
3. the distinction between arbitrary receiver quantum storage and coherent import of that storage into a later acquisition;
4. the inclusions
   ```text
   D_N^[b] <= D_N^(reset,b) <= D_N,
   D_N^(reset,N) = D_N;
   ```
5. the use of root fidelity for positive, possibly subnormalized receiver operators;
6. multiplicativity only at the conditional fresh-block append;
7. direct-sum additivity for the retained classical record and monotonicity under the common receiver instrument;
8. the backward continuation induction with the factor
   ```text
   [1-(A-a)](1-a) >= 1-A;
   ```
9. the avoidance of normalization at zero-probability histories;
10. the fresh adaptive-block estimate obtained by purified slotwise isometry telescoping;
11. retention of the complete `n r s^2` channel remainder before conversion to Bures distance;
12. the one-block bound
    ```text
    d_B(omega_E,omega_F) <= s(alpha n + sqrt(r n));
    ```
13. the fidelity-deficit majorant of order `n^2 s^2`;
14. the pathwise cost
    ```text
    Q = max_terminal_paths sum_r n(h_r)^2 <= b N;
    ```
15. the resulting policy-sensitive upper
    ```text
    min{2, 2(alpha+sqrt(r)) s sqrt(Q)};
    ```
16. the use of the v87 GHZ-block construction as a valid reset protocol for the coherent lower;
17. the use of the unrestricted adaptive horizontal upper, rather than the coarser canonical-factor upper, in the regular row;
18. the use of the fixed impossible-label event in the support-opening row;
19. the conclusion at `b=1` that classical feedback plus receiver quantum memory does not recover the coherent linear scale under the stated reset condition; and
20. the conclusion at `b=N` that the reset class equals the unrestricted adaptive class.

The theorem is therefore not a cosmetic restatement of v87. It closes a genuine resource-model gap and clarifies that, locally in the coherent tangential regime, the decisive resource is coherent input-side linkage across unknown-device calls, not receiver-side quantum storage by itself.

The four-leading-general-journal conclusion nevertheless remains negative. The theorem is local to one fixed base measurement, one fixed nonzero tangent and one fixed quadratic remainder allowance. Its constants and small-scale interval may degenerate with support eigenvalues, tangent size, the logical correction gap and the allowance. It does not give a uniform metric equivalence on the ordered-POVM body, a matching arbitrary-pair lower for the global midpoint covariance certificate, a complete stratified boundary geometry, full-boundary entropy or common learning, or an unrestricted higher-order classification.

The reset resource model is precise and mathematically useful, but it is not a classification of all intermediate causal resources. In particular, the theorem excludes coherent quantum information imported across nominal reset boundaries, including strategies whose probe marginals are separable but whose complete probe–reference systems share a quantum register. It also does not classify bounded-dimensional quantum memories, bounded classical memories, indefinite causal structures, or general network constraints.

The principal proof mechanisms are established ones: fidelity monotonicity and direct-sum identities, isometric-extension/Bures estimates, semidefinite tangent geometry, GHZ phase accumulation, entanglement-depth scaling, and the Kraus-span/quantum-error-correction metrological dichotomy. The manuscript's genuine contribution is their exact support-coordinate and finite-tube synthesis, the uniform control of an unknown quadratic remainder, and the sharp reset-width interpolation. That is strong specialist mathematics, but in my judgment it does not yet provide the breadth or conceptual displacement expected by the four leading general mathematics journals.

There is also an unresolved priority boundary. The revised manuscript now compares Huang–Meyer–Nuradha–Wilde, Yuan–Fung, Ghosal–Halder–Patra–Sen, and Salek–Hayashi–Winter. It still omits a directly relevant published source:

- T.-A. Ohst, S. Zhang, H. C. Nguyen, M. Plávala, and M. T. Quintino, *Characterising memory in quantum channel discrimination via constrained separability problems*, **Quantum 10 (2026), 1988**, arXiv:2411.08110v2.

That work systematically characterizes quantum and classical memory restrictions in adaptive channel-discrimination protocols and includes a dedicated classically adaptive analysis. It does not appear to contain the present fixed-tube reset-width theorem or its support-coordinate lower constructions, but it is a much closer resource-taxonomy antecedent than the current audit acknowledges. A theorem-level comparison is required before any strong novelty claim.

**Disposition outside the four leading general journals:** the focused quantitative paper is a strong candidate for a leading specialist journal in mathematical quantum information, quantum statistics, or operator-theoretic information theory, after the priority, provenance and exposition revisions below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Frozen object and genealogy

The latest General Theta Foundations I object located in the final branch survey is Revision 88. No Revision 89 branch was present when these review branches were created.

The active response branch points to publication commit

```text
d1add4a7ba45230b3cba71b47ef46da5e4a88d72.
```

Its direct parent is the qualified native theorem source

```text
cebd9b28f8ea603fa98c8c5c8f70d9e1daafb3d1.
```

A direct comparison shows that the publication child adds rendered manuscripts, archives, logs, page checks, regression results and source-bound receipts; it does not change the theorem source. The mathematical predecessor is completed v87 at `aab076...`, and the two r57 reports are frozen by commit and digest.

The v88 mathematical delta is concentrated in:

- `sections/79-classical-feedback-reset-width.tex`;
- `editions/operational-introduction88.tex`;
- `editions/current-comparison88.tex`;
- `feedback_budget.py`;
- `feedback_check.py`;
- `FEEDBACK_SCHEMA.md`; and
- the current response, proof audit, literature audit, resource ledger and build records.

The build receipt reports that every predecessor mathematical section is byte-identical and active. Revision 88 therefore answers r57 by adding a new resource theorem, not by silently altering the v87 block theorem or one-sided tube theorem.

---

## 2. Mathematical contribution

### 2.1 Reset protocols

A reset protocol is described by a classical history tree. At node `h`, it either stops or reserves `n(h)<=b` fresh calls. Conditional on `h`, a complete new probe–reference state is prepared by the same rule under both hypotheses and is tensor-independent of the receiver's entire old memory. A common adaptive experiment acts only on this fresh system. Afterwards, a common receiver instrument may jointly process the new output and all old memory, preserve arbitrary quantum memory and emit the next classical history.

This definition makes the intended boundary explicit. The old receiver state may differ under the two hypotheses and may be arbitrarily entangled with old outputs. What is forbidden is sending any subsystem of that old state coherently into a later acquisition. Classical information extracted from it may influence the next preparation.

The equality at `b=N` is justified: take one fresh block containing the entire unrestricted adaptive strategy, with trivial pre-existing receiver memory. At `b=1`, the class is strictly richer than the independent product class because later inputs may depend on prior classical records and the receiver may keep quantum memory.

### 2.2 Conditional fidelity accumulation

The new lemma is the conceptual core. Let `R_0,R_1` be the subnormalized receiver operators at one history, and let `omega_{0,h},omega_{1,h}` be the normalized outputs of the fresh block. Conditional independence gives

```text
f(R_0 tensor omega_0, R_1 tensor omega_1)
 = f(R_0,R_1) f(omega_0,omega_1).
```

After the common receiver instrument, retaining outcome `z`, direct-sum additivity and channel monotonicity give

```text
sum_z f(R_{0,z},R_{1,z})
 >= (1-a_h) f(R_0,R_1).
```

Applying the continuation estimate separately at each `z` is legitimate even though the two conditional receiver states differ. If the current deficit is `a` and each child has remaining path budget at most `A-a`, the retained factor is

```text
[1-(A-a)](1-a)
 = 1-A + a(A-a)
 >= 1-A.
```

The proof uses no division by the probability of a history. This is important at branches null under one hypothesis. Since every nonterminal node reserves at least one call, the tree depth is finite and backward induction closes.

I find this lemma correct.

### 2.3 Fresh adaptive-block upper

For tangential directions with all missing-support blocks zero, the inherited canonical factor solution gives a normalized surrogate channel with isometries `W_0,W_s` satisfying

```text
||W_s-W_0|| <= alpha s,
||M_F-M_G(s)||_diamond <= r s^2.
```

Purifying the complete fresh adaptive tester and replacing the isometry in each of `n` slots yields a vector displacement at most `n alpha s`. This is valid for adaptive internal controls because all interleaving operations are common isometries. The dilation environments are proof devices and are not supplied to the tester.

The surrogate-to-actual replacement costs `n r s^2` in diamond norm by adaptive telescoping. The Bures/trace inequalities then give

```text
d_B(omega_E,omega_F)
 <= s(alpha n + sqrt(r n)).
```

Consequently

```text
1-f(omega_E,omega_F)
 <= gamma n^2 s^2,
gamma=(alpha+sqrt(r))^2/2.
```

The use of the canonical, generally nonhorizontal factor here is correct. The sharper horizontal factor is reserved for the regular-direction unrestricted adaptive bound.

### 2.4 Reset-width theorem

For one policy, let

```text
Q=max_terminal_paths sum_r n(h_r)^2.
```

The hard pathwise call budget and `n(h)<=b` imply `Q<=bN`. Conditional fidelity accumulation yields

```text
f_out >= (1-gamma Q s^2)_+.
```

If the deficit is at most one, the trace/fidelity inequality gives the `s sqrt(Q)` bound; if it exceeds one, the universal trace cap two applies. This proves the coherent upper of order `sqrt(Nb)s` for the reset class, without assuming product output states after feedback.

The lower is supplied by the v87 parallel GHZ blocks, which form an admissible reset policy with no feedback. The regular and opening rows follow by sandwiching the reset class between already audited subclasses and the unrestricted adaptive class. The three cases are disjoint and exhaustive by the complete covariance-range criterion.

I find the theorem correct under the stated reset definition.

### 2.5 Unit reset width

At `b=1`, the coherent tangential row has square-root order despite arbitrary classical feedback and arbitrary receiver quantum memory. Parallel and unrestricted adaptive acquisition retain linear order. This is a sharp and conceptually useful separation.

The statement must continue to be described as a local order theorem. It is not an equality of exact operational distances and does not imply that classical feedback is globally useless for channel discrimination.

---

## 3. Finite policy executable

`feedback_budget.py` verifies a finite public policy graph, including:

- canonical rational `s` and `gamma`;
- genuine integer `N` and `b`;
- reachability of every node;
- absence of cycles;
- complete successor declarations;
- hard maximum call budget;
- pathwise square cost;
- the additive fidelity lower;
- the stronger product-recursion lower; and
- the corresponding trace-square consequence.

The implementation correctly sets

```text
local_fidelity_majorant_verified = false,
physical_reset_independence_verified = false,
exact_operational_distance_computed = false,
physical_protocol_executed = false.
```

This boundary is essential. A JSON decision tree cannot certify that a physical preparation is tensor-independent of old receiver memory, nor can it establish the one-block coefficient `gamma` without a separate mathematical or experimental certificate.

`feedback_check.py` performs exact finite receiver-memory experiments and rejection controls. These are useful regressions, but they are not a proof of the continuum theorem or a realization of the general logical recovery.

---

## 4. Literature and priority

### 4.1 Comparisons now handled well

The manuscript now correctly identifies the channel-Bures/isometric-extension antecedents. Huang–Meyer–Nuradha–Wilde give parallel and adaptive Bures bounds in a common framework and identify the Yuan–Fung parallel antecedent. The manuscript does not claim those inequalities as new; it specializes one aligned extension and separately pays the finite tube remainder.

The comparison with Ghosal–Halder–Patra–Sen also has the right scope. Their block-i.i.d. composite Stein setting is a close resource antecedent, but differs in loss, asymptotics, identical-block structure and unknown-remainder quantification.

Salek–Hayashi–Winter remains an appropriate antecedent for classical feedback in asymptotic fixed-pair discrimination.

### 4.2 Missing memory-constrained comparison

The omission of Ohst–Zhang–Nguyen–Plávala–Quintino is material. Their published paper develops a general hierarchy of quantum and classical memory restrictions in single- and multi-copy channel discrimination and explicitly treats classically adaptive schemes. The present reset model is not obviously identical to their dimension-constrained or separability-constrained classes, but that is precisely why a careful comparison is needed.

The revised paper should state:

1. whether reset independence is expressible as one of their constrained-separability conditions;
2. whether arbitrary receiver memory but zero coherent import has a direct analogue in their hierarchy;
3. whether their classically adaptive set contains, is contained in, or is incomparable with the present `b=1` class;
4. which result, if any, already supplies a generic optimization or upper bound for the reset class; and
5. why the finite shrinking-tube width theorem and support-coordinate lower remain additional.

Independent specialist priority review remains necessary after this comparison.

---

## 5. Reproducibility and provenance

The internal qualification record is strong. Workflow run `37313946295` successfully:

1. reconstructed the native source;
2. verified predecessor proof preservation;
3. built four manuscripts;
4. ran twenty-six exact suites in ordinary and optimized Python;
5. committed publication artifacts directly on the native source; and
6. checked the publication head read-only inside the same write-capable job.

The package records a 47-page primary, 78-page supplement, 41-page structural article and 251-page complete edition. It reports 665 current source files, 632 predecessor native files, 962 complete-edition labels, 475 quantitative-package labels and 116 structural labels.

There is, however, a discrepancy in the current provenance prose. `RESPONSE_TO_REFEREE.md` states that the v88 release has its own directly triggered read-only exact-final-head workflow. At the reviewed branch head:

- `GENERAL_THETA_FOUNDATIONS_I_V88_FINAL_HEAD_REQUEST.json` is absent;
- the configured exact-head workflow therefore has not been triggered by the publication commit;
- the Actions API returns no workflow run whose `head_sha` is `d1add4...`; and
- the combined commit-status endpoint returns no statuses for `d1add4...`.

The accurate statement is that the write-capable publication workflow internally checked the exact publication child read-only. That is good evidence, but it is not a separately triggered, trust-separated final-head run. The manuscript should either complete the advertised final-head step or revise the claim.

The native and publication commits are unsigned. No human signature is claimed, which is correct.

---

## 6. Why the four-leading-journal threshold is not met

### 6.1 Local rather than global geometry

The main theorem is uniform in `N`, `b` and the allowed remainder only after `E`, `H` and `Lambda` are fixed. It is not a body-wide theorem and does not control degeneration across support strata.

### 6.2 Resource hierarchy remains partial

The reset theorem fills an important class but does not classify shared-reference strategies, bounded quantum-memory dimension, bounded classical-memory size, general feedback networks or indefinite causal order.

### 6.3 Established conceptual mechanisms

The theorem combines established fidelity, Bures, GHZ, QEC and tangent-cone tools. The synthesis is technically nontrivial, but the conceptual ingredients and phase mechanisms are not newly introduced.

### 6.4 Global boundary and learning questions remain open

The arbitrary-pair midpoint covariance has no matching general lower. Full-boundary entropy, boundary common learning, growing-`k` minimax sharpness and efficient dictionary/recovery/readout synthesis remain open.

### 6.5 Priority remains unsettled

The author-side audit is improved but incomplete, and no independent specialist opinion is supplied.

### 6.6 The wider Theta programme is separate

The finite-dimensional measurement results do not prove any of the raw local-limit, path-recovery, shell-conditioning, Mosco/Nisio, filtering/LAN, changing-filtration or labelled posterior-contraction gates in the independent A/B/C/D programme. All aggregate closure flags remain false.

---

## 7. Required revisions before specialist submission

1. **Add a theorem-level comparison with Ohst–Zhang–Nguyen–Plávala–Quintino.** This is the most important remaining priority omission.

2. **Correct the v88 exact-head provenance claim.** Either create the final-head request and publish the successful directly triggered receipt, or state that verification occurred inside the write-capable publisher.

3. **Keep the conditional tensor-independence assumption on page one.** “Classical feedback” alone is too broad a description of the proved class.

4. **Distinguish receiver memory from input-side coherent memory consistently.** The theorem permits the former without limit and forbids coherent import of it into later acquisitions.

5. **Do not identify reset width with memory dimension or entanglement depth.** These are different resources.

6. **State the pathwise resource convention whenever the theorem is summarized.** `N` and `Q` are worst-path quantities, not expectations.

7. **Keep the complete finite remainder in every summary proof.** The terms `nrs^2`, `m kappa s^2` and the regular-row `Ns^2` term are logically essential.

8. **Clarify that the finite policy executable is conditional.** It verifies arithmetic consequences, not physical reset independence or the local fidelity coefficient.

9. **Retain the distinction between local orders and exact distances.** In particular, parallel/adaptive comparison must not be paraphrased as general equivalence.

10. **Keep the nonempty interval separate from the discrimination interval.** The executable does not compute the latter.

11. **Preserve the two distinct linear mechanisms.** Support opening is classical; coherent tangential accumulation is not.

12. **Keep the independent product converse in its original scope.** The new reset upper is a different proof and should remain so.

13. **Separate specialist article, supplement, structural paper and archive.** The 251-page complete edition is not a journal-facing object.

14. **Do not use the wider repository as a significance multiplier.** The measurement article should stand on its own theorem package.

15. **Obtain independent specialist priority review before making strong novelty claims.** Exact builds and AI reports cannot supply that judgment.

---

## 8. Detailed comments

1. In Definition `def:reset88`, “the same under both hypotheses” should be glossed as one common conditional preparation map defined on every formal history, not equality of the hypothesis-dependent conditional receiver states.

2. The phrase “arbitrary receiver quantum memory” is accurate only together with the prohibition on coherent import into the next acquisition.

3. The equality `D_N^(reset,N)=D_N` is best explained by taking trivial old receiver memory and placing the complete adaptive tester inside one fresh block.

4. At `b=1`, do not write equality with the product-reference class. The current manuscript correctly avoids this.

5. The fidelity accumulation lemma should retain positive operators rather than normalize branches; this is one of its main strengths.

6. The countable-outcome extension is harmless provided all direct sums are trace class; a short sentence to this effect would help.

7. The current factor
   ```text
   (1-A+a)(1-a)
   ```
   is preferable to an exponential relaxation because it keeps a finite exact ledger.

8. Public randomization should always be modeled by a retained common instrument outcome, as in the proof, rather than by an informal convexity sentence.

9. In the adaptive-block lemma, “adaptive experiment acts on the new system alone” must include all within-block quantum memory in the fresh system.

10. The discarded Stinespring environment is a proof device and must never be listed among accessible systems.

11. `sqrt(n)<=n` is the only place the block deficit is coarsened to `n^2`; this should remain visible.

12. The policy-sensitive bound in terms of `Q` is stronger and more informative than the final `bN` corollary. It deserves theorem-level visibility.

13. The lower strategy depends on `E,H,N,b,s` but not on the unknown remainder. This is the correct uniformity statement.

14. The support-opening witness is fixed throughout the tube and does not require feedback.

15. The `b=N` identity for reset/adaptive strategies has a different status from the v87 local-order comparison of parallel and adaptive strategies. The text should not blur them.

16. The finite policy graph may share subtrees. The executable treats it as a DAG representation and still computes worst-path maxima; this should be stated in `FEEDBACK_SCHEMA.md`.

17. The nodewise `gamma` supplied to the executable is not reconstructed from an actual channel pair. The current false flag is correct.

18. The finite receiver-memory examples test nontrivial feedback bookkeeping but do not instantiate the general corrected logical code.

19. The failed baseline-dispatch run is honestly preserved and followed by a successful independent v87 verification. It should not be counted as a v88 final-head run.

20. The publication commit is unsigned. This is a provenance limitation, not a mathematical defect.

21. The current title is appropriately focused on discrimination and should be retained.

22. The learning results remain substantial but should stay secondary to the reset-width theorem in the submitted primary.

23. The complete research edition should be described only as preservation material.

24. All statements about polynomial computation should remain limited to represented classical certificates and affine repair.

25. The paper should avoid the phrase “classifies feedback” without the adjective “reset-constrained.”

---

## 9. Final assessment

Revision 88 successfully answers the principal resource-model objection left by r57. It gives a mathematically coherent conditional-fidelity proof for classical feedback with unrestricted receiver memory and bounded coherent reset width, and it preserves the full finite-remainder and unknown-remainder quantifiers. The new theorem is technically serious and, in my assessment, correct under its stated interface.

It still does not meet the Annals / Inventiones / JAMS / Acta threshold. The result is local and nonuniform, the resource hierarchy is not complete, the central mechanisms have established antecedents, the global boundary/learning programme remains open, and the independent priority boundary is unsettled. The current literature audit also omits a directly relevant published memory-constrained channel-discrimination paper, and the stated v88 exact-head provenance has not yet been realized at the reviewed branch head.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused submission to a leading specialist journal after the priority and provenance corrections above.**
