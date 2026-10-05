# Referee Report — General Theta Foundations I, Revision 89 (r59)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed revision branch:** `revision/general-theta-foundations-i-v89-r58-response-2026-10-05`  
**Reviewed review-ready head:** `df7ed618813224b058b97c6cbda720ad936e2c53`  
**Publication parent:** `810e2aea70e18a5efe54b033a40584f07844f192`  
**Qualified native source:** `89773eff80ca81718641ec72d5efb9e20e03559a`  
**Completed predecessor:** Revision 88, `d1add4a7ba45230b3cba71b47ef46da5e4a88d72`  
**Controlling external report:** v88/r58, `601b5b72ce223ee6650e346457a8915ea38a51de`  
**Controlling proof/pipeline audit:** v88/r58, `c493692c529b0bfe73fcb3c7de9a3b676308f233`  
**Source qualification run:** `37329503815`  
**Exact-final-head read-only run:** `37331064634`, conclusion `success`  
**Exact-final-head artifact:** `11354223086`  
**Review branch:** `review/general-theta-foundations-i-v89-resource-profile-external-referee-r59-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 89 is a substantial and mathematically coherent strengthening of Revision 88. The new manuscript replaces the coarse largest-block parameter by the complete public allocation profile and identifies the exact second-moment quantity

```text
V = sum_r n_r^2
```

that governs the coherent local scale. It then passes from deterministic profiles to history-dependent reset policies and proves a sharp hard-budget theorem in terms of

```text
N_pi = max_paths sum_h n(h),
Q_pi = max_paths sum_h n(h)^2.
```

The resulting three-row law is

```text
regular tangent:       min{1, sqrt(N) s},
coherent tangent:      min{1, sqrt(Q) s},
support opening:       min{1, N s},
```

when optimized over reset-constrained policies with hard bounds `N_pi <= N` and `Q_pi <= Q`. For a prescribed deterministic profile, the coherent row is `min{1,sqrt(V)s}`.

The revision also supplies:

1. a single bounded classical readout that combines unequal coherent block signals without knowledge of the unknown quadratic remainder;
2. a refined policy upper retaining the two contributions
   ```text
   alpha sqrt(Q_pi)  and  sqrt(r N_pi);
   ```
3. a conditional stability theorem for approximate reset-preparation channels;
4. an explicit strict tester-operator inclusion between the two-call measure-and-reprepare class of Ohst–Zhang–Nguyen–Plávala–Quintino and the unit-reset retained-receiver class; and
5. a corrected and now successful exact-final-head provenance chain.

I did not find a fatal gap in Sections 80–81 or in the inherited results they invoke. The principal estimates, integer cases, resource inclusions, and finite remainder bookkeeping are internally consistent. The exact-final-head workflow also now does what Revision 88 had only claimed: the metadata-only head `df7ed618...` itself triggered a read-only reconstruction, and the preserved receipt identifies that same SHA as `verified_head`.

The four-leading-general-journal conclusion nevertheless remains negative. The new profile and quadratic-budget theorems are natural, precise, and useful refinements of the already established v88 reset-width theorem. Their proof architecture is an exact synthesis of known second-moment metrological scaling, block Bures estimates, conditional fidelity, GHZ phase accumulation, and elementary integer packing. The unequal-signal readout is a neat finite device, but the revision does not create a new global geometry, a new memory hierarchy, or a new operational equivalence of broad classes. The Bell witness establishes a strict inclusion of tester sets, not a discrimination-score separation. The approximation proposition is a standard hybrid stability estimate. In my judgment the package is now strong specialist mathematics, but not a conceptual displacement of the scale expected by the four leading general mathematics journals.

A further literature issue has appeared since the r58 review. The manuscript now gives the requested theorem-level comparison with Ohst et al., but it does not discuss:

- M. Zonnios and F. C. Binder, *Distinguishing quantum processes with bounded coherent memory*, arXiv:2606.19511 (2026).

That paper introduces a coherent-memory-dimension hierarchy for multi-time process discrimination and proves finite-time completeness of its autonomous-machine class. Its process model, stationary-instrument constraint, and memory resource are different from the present memoryless measurement tube, conditional reset cut, and hard quadratic call budget. I do not see it as containing Theorems `allocation89` or `quadraticbudget89`. It is nonetheless a direct 2026 antecedent for any discussion framed around bounded coherent memory, memory-parametrized discrimination, and completeness of adaptive strategy classes. A theorem-level comparison is required.

**Disposition outside the four leading general journals:** after the literature and exposition revisions below, the focused quantitative paper should be seriously considered by a leading specialist journal in mathematical quantum information, quantum statistics, operator theory, or mathematical physics. I would not request another reconstruction of the full historical corpus.

---

## 1. Frozen object and genealogy

The latest General Theta Foundations I object located in the final branch survey is Revision 89. No Revision 90 branch was present when these review branches were created.

The active response branch and the review-ready alias both point to

```text
df7ed618813224b058b97c6cbda720ad936e2c53.
```

Its direct parent is the publication commit

```text
810e2aea70e18a5efe54b033a40584f07844f192,
```

whose direct parent is the qualified native theorem source

```text
89773eff80ca81718641ec72d5efb9e20e03559a.
```

A direct comparison gives the following clean release structure.

### Native source to publication

The single publication commit adds only:

- the four rendered manuscripts;
- source, research, and journal archives;
- build and isolated-rebuild receipts;
- page, theorem-location, source-hash, and preservation checks;
- regression outputs and LaTeX logs; and
- root publication metadata.

No theorem source changes between `89773eff...` and `810e2aea...`.

### Publication to review-ready head

The single final commit adds only

```text
GENERAL_THETA_FOUNDATIONS_I_V89_FINAL_HEAD_REQUEST.json.
```

No mathematical source, executable, manuscript, or PDF changes between `810e2aea...` and `df7ed618...`.

The completed predecessor is the actual remote v88 publication `d1add4...`, not the distinct unpublished local allocation draft that happened to use the same local version number. Revision 89 records that collision explicitly, preserves seven local derivation files under `unpublished-local-v88/`, and does not invent remote ancestry for them.

The source receipt reports:

```text
710 current source files,
665 predecessor native files,
975 complete-edition labels,
488 current quantitative-package labels,
116 structural labels,
28 regression suites.
```

Every inherited mathematical section is reported byte-identical and active.

---

## 2. Main mathematical contribution

### 2.1 Prescribed allocation profiles

For a nonempty public list

```text
n = (n_1,...,n_l),
```

Revision 89 retains both

```text
N_n = sum_r n_r,
V_n = sum_r n_r^2.
```

An independent allocation tester is a tensor product of complete probe–reference groups, arbitrary inside each group, with arbitrary final joint processing. A prescribed-profile reset tester may use history-dependent preparation and adaptive controls inside each fresh group, and arbitrary receiver processing between groups, but the entire fresh probe–reference/within-block-memory system is conditionally independent of all old receiver memory.

Theorem `allocation89` proves, uniformly over all public profiles and every legal member of one fixed quadratic tube,

```text
regular:    min{1,sqrt(N_n)s},
coherent:   min{1,sqrt(V_n)s},
opening:    min{1,N_n s}.
```

The same order holds for the independent and prescribed-profile reset classes.

This is a genuine strengthening of the `sqrt(Nb)` statement. Two profiles with the same total call count and the same largest block can have different `V`, and hence different coherent local orders.

### 2.2 Unequal-signal common readout

The new finite classical lemma is the key lower-bound improvement. Given independent signs with biases satisfying

```text
alpha x_r <= u_r <= x_r,
0 <= x_r <= 1/2,
```

it constructs one binary randomized readout depending only on the public vector `x`, not the unknown actual biases `u`, and obtains separation

```text
(alpha/64) min{1,(sum_r x_r^2)^(1/2)}.
```

The proof uses

```text
T(X) = sin(sum_r t_r X_r),
t_r = x_r/(16 max{sqrt(S),S}),
S = sum_r x_r^2.
```

The modulus and phase estimates are consistent:

```text
sum t_r^2 <= 1/256,
R >= 1/2,
alpha S/(16A) <= phi <= S/(4A) <= 1/4,
E_u T >= alpha S/(64A).
```

The conversion of the bounded statistic to a randomized binary decision is legal and yields the claimed unhalved separation. The `S=0` case is removed before division. No likelihood-ratio test depending on the unknown remainder is hidden in the construction.

### 2.3 Profile upper bounds

For independent groups, the inherited finite block estimate gives

```text
d_B,r <= s(3 beta_0 n_r/2 + sqrt(r_0 n_r)).
```

Tensor fidelity across genuinely independent complete groups and trace/Bures conversion yield

```text
D^n(E,F)
 <= min{2,2s [sum_r(3 beta_0 n_r/2 + sqrt(r_0 n_r))^2]^(1/2)}
 <= min{2,2s(3 beta_0 sqrt(V)/2 + sqrt(r_0 N))}.
```

The `sqrt(r_0 n_r)` contribution retains the full `n_r r_0 s^2` channel remainder before Bures conversion.

For prescribed-profile reset feedback, the same formula follows by a different argument. Nodewise fresh-block fidelity deficits are accumulated with the subnormalized conditional-fidelity lemma. The proof does not multiply unconditional output fidelities after feedback.

Since `N <= V` for positive integer block sizes, the stated coherent order follows.

### 2.4 Profile coherent lower

Each group uses

```text
m_r = min{n_r, floor((2 Delta s)^(-1))},
x_r = m_r Delta s.
```

The inherited logical GHZ construction gives a common binary event with actual bias `u_r` satisfying

```text
|u_r - sin(x_r)/2| <= m_r kappa s^2/2.
```

After shrinking the fixed-tube interval, the manuscript obtains

```text
x_r/(2 pi) <= u_r <= x_r.
```

The unequal-signal lemma therefore gives

```text
D^n(E,F)
 >= (128 pi)^(-1) min{1, Delta s (sum_r m_r^2)^(1/2)}.
```

Both integer regimes are handled.

- If no group clips, `m_r=n_r` and the target is `sqrt(V)s`.
- If some group clips, the floor input is at least two and the corresponding `x_r` is at least `1/4`; this supplies a uniform positive lower bound in the saturated regime.

The lower event and final randomized readout are independent of the unknown remainder.

### 2.5 Effective width and profile packing

The profile corollary correctly identifies the maximal square sum under

```text
sum n_r <= N,
n_r <= b
```

as

```text
q b^2 + r^2,
q=floor(N/b),
r=N-qb.
```

The bounds

```text
Nb/2 <= q b^2+r^2 <= Nb
```

are correct. Thus the old `sqrt(Nb)` law is recovered up to universal constants, while

```text
b_eff = V/N
```

retains the actual profile.

The manuscript appropriately restricts the operational set-inclusion statement under coarsening to independent allocation testers. Removing a reset boundary can remove an allowed receiver interaction, so no analogous inclusion is asserted for arbitrary feedback testers.

### 2.6 Policy-sensitive upper

For an individual reset policy, Revision 89 defines

```text
B_pi = max_paths sum_h (alpha n(h)+sqrt(r n(h)))^2.
```

Conditional fidelity gives

```text
D(pi;E,F) <= min{2,2s sqrt(B_pi)}.
```

Pathwise Minkowski then gives

```text
D(pi;E,F)
 <= min{2,2s(alpha sqrt(Q_pi)+sqrt(r N_pi))}.
```

This is sharper than replacing `sqrt(n)` by `n` at every node. The proof uses hard path suprema, not expected costs or probabilities of histories.

### 2.7 Sharp quadratic-budget law

For integers

```text
N <= Q <= N^2,
```

let the class contain reset policies with `N_pi<=N` and `Q_pi<=Q`.

The coherent upper follows immediately from the policy estimate. For the lower, put

```text
b=floor(Q/N).
```

Then

```text
Nb <= Q,
Nb >= Q/2.
```

Packing `N` calls into blocks of width `b` gives a deterministic profile with

```text
Q/4 <= V <= Q.
```

The profile lower therefore yields `min{1,sqrt(Q)s}` up to fixed constants. The proof does not claim exact attainment of every integer `Q`.

The regular and opening rows are attained with singleton profiles and retain their earlier adaptive uppers. This establishes the announced budget-class theorem.

The manuscript also correctly warns that `Q_pi` is not a lower certificate for an individual policy. A high-cost policy may erase all outputs or spend its cost on an uninformative branch.

### 2.8 Certified deviation from reset

Proposition `approxreset89` assumes a uniform diamond-norm estimate

```text
||P_tilde,h - (Id tensor sigma_h)||_diamond <= delta_h
```

at every formal history, including auxiliary references, and a worst-path sum at most `epsilon`.

A backward hybrid induction shows that each hypothesis's final state moves by at most `epsilon`; hence the two-hypothesis separation increases by at most `2epsilon`:

```text
D_tilde(pi;E,F) <= min{2,D(pi;E,F)+2epsilon}.
```

This is correct under the stated channel certificate. The manuscript expressly does not infer the certificate from marginal separability, a policy graph, or average calibration. It also notes that fixed positive `epsilon` may dominate a shrinking signal.

### 2.9 Retained receiver memory versus measure-and-reprepare

For the two-call classically adaptive model of Ohst et al., the effects have the form

```text
T_i = sum_z R_z tensor S_{i|z}.
```

Such testers are unit-reset testers: measure the first call completely, keep the classical outcome, and prepare the second tester freshly.

Revision 89 proves strictness at the tester-operator level. Its unit-reset strategy prepares two independent maximally entangled input–reference pairs, retains the first reference and classical label, prepares the second pair freshly, and performs a final Bell measurement on the two references. One effect is

```text
T_0 = (1/4) Pi^T_{I_1 I_2} tensor |00><00|_{Y_1Y_2}.
```

The complementary effect is positive and the pair has the deterministic tester normalization. Partial transpose across the complete first-call factor has eigenvalue `-1/8`. Every positive sum of complete-call product effects is PPT across this cut, so `T_0` is outside the measure-and-reprepare cone.

This argument is sound in finite dimension. The manuscript correctly limits the conclusion to strict inclusion of tester operators. It does not establish a strict optimal-score gap for every channel pair or ensemble.

For publication, however, the derivation of the `1/4` normalization, tensor-factor ordering, and comb normalization should be written in the proof itself rather than left partly to the exact regression. The finite-dimensional closure statement for the relevant separable tester cone should also be stated explicitly.

---

## 3. What Revision 89 resolves from r58

### 3.1 Ohst et al.

The omission identified in r58 is substantially repaired. The manuscript now distinguishes:

- memory dimension and coherent transfer constraints in Ohst et al.;
- complete-measurement/measure-and-reprepare classical adaptation;
- conditional independence at a reset preparation cut; and
- arbitrary retained receiver memory with no coherent import into the next acquisition.

The new NPT tester gives a concrete model boundary.

### 3.2 Provenance

The v88 overstatement has been corrected without rewriting the frozen v88 report response.

For v89, run `37331064634` was triggered by the exact review-ready head `df7ed618...`, checked out that SHA without write credentials, rebuilt the source, four manuscripts, twenty-eight regression suites, and linked journal package, and preserved an artifact whose receipt states

```text
status = success,
read_only = true,
verified_head = df7ed618813224b058b97c6cbda720ad936e2c53,
source_commit = 89773eff80ca81718641ec72d5efb9e20e03559a.
```

This closes the specific r58 execution gap.

The GitHub legacy combined-status endpoint is empty for the final SHA; the successful Actions check suite and receipt should not be redescribed as a separate legacy status context.

### 3.3 Local versus global scope

The abstract and introduction repeatedly state that the conclusions are local fixed-tube orders, not exact-distance identities, arbitrary-pair metric equivalences, or memory-dimension classifications.

### 3.4 Policy certificates

The new executable preserves false flags for physical reset independence, local fidelity calibration, reset-defect calibration, exact operational distance, recovery synthesis, physical execution, continuum proof by replay, and priority clearance.

---

## 4. Remaining correctness and exposition requests

I do not regard the following as fatal gaps, but they should be resolved before specialist-journal submission.

### 4.1 Memory-witness normalization

Give a self-contained contraction calculation for `T_0`, including:

- the exact normalized or unnormalized Choi convention;
- the ordering of `I_1,Y_1,I_2,Y_2`;
- the origin of the factor `1/4`;
- positivity of the complementary effect;
- deterministic tester normalization; and
- the precise bipartition used for partial transpose.

The current regression verifies these identities on a finite family, but the manuscript should not require code to recover the convention.

### 4.2 Closed cone language

Replace the phrase “including limits of such sums” by a precise finite-dimensional statement. Identify the relevant cone of positive separable complete-call tester effects, note its closedness in finite dimension, and then apply the PPT obstruction.

### 4.3 Profile reset definition

State explicitly whether a prescribed profile includes padded terminal rounds in the formal classical record, or whether they are absorbed into a fixed continuation channel. The current proof works either way, but the convention should be unique.

### 4.4 Countable branching

The conditional-fidelity applications invoke trace-class direct sums with countably many outcomes. Add one sentence identifying the normal instrument/direct-sum convention and the monotone limit from finite truncations.

### 4.5 Public readout dependence

The unequal-signal readout depends on `E,H,Lambda,s` and the public profile through `x_r`, but not on the unknown remainder. Repeat this exact dependence immediately after the lemma statement; “depending only on `(x_r)`” is mathematically correct but less informative to a reader entering through the theorem.

### 4.6 Budget domain

The theorem restricts to integer `N<=Q<=N^2`. Explain explicitly that every policy with at most `N` positive integer reservations automatically lies in this ambient range, while smaller real-valued or expected quadratic budgets are different models.

### 4.7 Reset perturbation

State the corresponding two-sided estimate

```text
|D_tilde(pi;E,F)-D(pi;E,F)| <= 2epsilon
```

when the same diamond certificate compares both implementations. The present upper is sufficient for the paper, but the hybrid proof gives the symmetric statement by exchanging ideal and implemented channels if the same bound is available.

### 4.8 Individual policy versus class optimum

The manuscript already states the distinction. It should also be reflected in notation: use a symbol such as `D(pi;E,F)` consistently for a fixed policy and reserve `D_{N,Q}^{reset}` only for the supremum class.

---

## 5. Priority and literature

### 5.1 Established mechanisms

The manuscript appropriately does not claim priority for:

- sum-of-squared-block-size metrological scaling;
- GHZ enhancement;
- entanglement-depth bounds;
- root-fidelity identities and monotonicity;
- channel Bures/isometric-extension estimates;
- semidefinite tangent geometry;
- Kraus-span/QEC metrology; or
- Bell-reference/NPT separation as a general mechanism.

Its genuine contribution is the finite ordered-measurement tube synthesis with unknown quadratic remainder, exact complete-support trichotomy, profile-sensitive matching lower, reset-feedback conditional upper, and hard pathwise `Q` optimization.

### 5.2 Ohst et al.

The theorem-level comparison is now adequate as a first pass. The strict operator inclusion is useful because it prevents an erroneous identification of reset independence with separability of final tester effects.

It should remain clear that the paper does not classify all auxiliary-dimension slices, all coherent-memory restrictions, or all lifted constrained-separability formulations.

### 5.3 Zonnios–Binder

The current paper must add a direct comparison with *Distinguishing quantum processes with bounded coherent memory*.

At minimum, the comparison should record:

1. their unknown objects are multi-time processes rather than repeated uses of a memoryless classical-output measurement channel;
2. their resource is coherent memory dimension in an autonomous repeated-instrument machine, not a worst-path sum of squared fresh-block reservations;
3. their hierarchy is monotone and complete at finite time when the coherent memory is sufficiently large and a counter is included;
4. the present reset class permits time-dependent public history rules and unrestricted receiver storage but prohibits coherent import across a specified fresh-preparation cut;
5. neither result supplies the other one's theorem; and
6. their work narrows any claim that the present paper is the first systematic interpolation involving coherent memory in process discrimination.

### 5.4 Post-measurement-state discrimination

A brief scope sentence should also distinguish the 2026 work of Eid–Quintino on discrimination of Lüders instruments with accessible post-measurement states. The present unknown interface has only classical output and no residual device system. No detailed theorem comparison is required unless the authors invoke general “measurement discrimination” novelty beyond the POVM-channel model.

### 5.5 Independent priority

The author-side audit, exact builds, and this AI-assisted referee report are not a substitute for an independent human specialist opinion. The most important unresolved priority questions remain:

- whether the complete support-kernel identity has an equivalent coordinate-free prior form;
- whether the fixed-tube profile law has appeared in local channel metrology under another resource name;
- whether the hard pathwise `Q` law follows from an existing strategy-norm or Fisher-information theorem with matching finite remainder;
- whether reset preparation has an existing comb/separability characterization; and
- whether the NPT tester boundary is already standard in the process-tensor literature.

---

## 6. Why the four-leading-general-journal threshold is not met

### 6.1 The principal theorem remains local and fixed-object dependent

All constants and the small-scale interval depend on a fixed base measurement `E`, fixed nonzero tangent `H`, and fixed allowance `Lambda`. They may degenerate when support floors close, correction gaps vanish, tangent norms shrink, or the allowance changes.

The paper does not prove a uniform bi-Lipschitz or stratified equivalence on the ordered-POVM body.

### 6.2 The profile theorem is a refinement rather than a new global structure

Once v88 supplies the one-block Bures estimate, conditional fidelity, and matching GHZ blocks, the appearance of

```text
sum n_r^2
```

is structurally natural. The new common readout is technically valuable because it avoids dyadic grouping and logarithmic losses, but it does not by itself reorganize a broad area.

### 6.3 The hard-budget law is an optimization corollary of the profile law

The lower uses the elementary packing `b=floor(Q/N)` and realizes `V` within an absolute factor of `Q`. This is clean and sharp, but conceptually close to optimizing the deterministic profile result.

### 6.4 The memory result is set-theoretic, not yet operationally separating

The Bell tester proves strict inclusion of operator classes. It does not exhibit a pair of measurement channels for which the optimal unit-reset score strictly exceeds the measure-and-reprepare score, let alone quantify that gap.

Such a score separation is not required for correctness, but without it the memory proposition has limited independent significance.

### 6.5 The approximation result is standard hybrid stability

The `2epsilon` bound is useful for scope control and possible implementation, but its proof is a direct telescoping/triangle argument rather than a new robustness theory.

### 6.6 Major global questions remain open

Revision 89 does not close:

- arbitrary-pair matching lower bounds for the global midpoint covariance certificate;
- complete stratified boundary geometry;
- full-boundary entropy or common learning;
- growing-outcome minimax sharpness;
- unrestricted zero-jet or higher-order classification;
- efficient general recovery, dictionary, or collective-readout synthesis;
- a complete memory-dimension/reset-width dictionary; or
- the independent A/B/C/D analytic programme.

These limitations are stated honestly in the repository. They nevertheless matter to the four-leading-general-journal assessment.

---

## 7. Required revisions before specialist submission

### R01 — Compare Zonnios–Binder

Add a theorem-level resource comparison and modify any broad bounded-memory novelty language accordingly.

### R02 — Complete the tester-witness derivation

Write the Choi contraction, normalization, factor ordering, separable-cone closure, and partial-transpose calculation directly in the manuscript.

### R03 — Keep operator inclusion distinct from score separation

Retain the present qualification. If the authors want the memory proposition to carry larger significance, exhibit a concrete ordered-measurement pair or ensemble with a strict optimal-score gap and prove the smaller-class upper.

### R04 — Obtain independent specialist priority review

Do not infer priority from repository search, source retrieval, exact arithmetic, or this report.

### R05 — Preserve the exact resource cut

Every theorem statement and summary must continue to require conditional independence of the complete fresh probe–reference/within-block-memory system, not merely probe-marginal separability.

### R06 — Preserve hard pathwise budgets

Do not replace `N_pi,Q_pi` by expectations, likely-path costs, or costs under one hypothesis.

### R07 — Preserve the finite remainder terms

Keep the separate `sqrt(rN)` contribution in policy bounds and the full `m_r kappa s^2` lower error before amplification.

### R08 — Clarify policy versus budget-class lower bounds

No individual-policy matching lower follows from a large `Q_pi`.

### R09 — State fixed-object nonuniformity prominently

Do not describe the theorem as a global metric equivalence or uniform boundary geometry.

### R10 — State reset-defect scaling requirements

A fixed nonzero calibration error can overwhelm a local signal. Any asymptotic robustness corollary must impose `epsilon=o(omega)` or another explicit relative scale.

### R11 — Keep memory dimension separate from reset width and `Q`

The new coherent-memory literature makes this terminological boundary particularly important.

### R12 — Tighten the focused journal object

The fifty-five-page primary remains broad. The profile/reset theorem, covariance/support geometry, and direct consequences should form the main narrative. Retained learning and coding results should remain clearly subordinate or be moved to the linked supplement without deleting their mathematical record.

### R13 — Preserve executable scope flags

Finite arithmetic checks do not prove continuum theorems, physical reset, local fidelity calibration, recovery synthesis, or priority.

### R14 — Report provenance with exact API semantics

The final Actions check and receipt succeeded. The legacy combined-status list is empty. Do not conflate these two mechanisms.

### R15 — Preserve the wider-pipeline boundary

No finite-dimensional discrimination theorem closes the historical A2 replacement, B4 aggregate, C2 aggregate, eleven-paper aggregate, or whole Theta programme.

---

## 8. Detailed comments

### D01 — Terminology

“Complete acquisition group” is preferable to “entanglement block” in the profile theorem, because the whole reference and within-block memory determine the reset cut.

### D02 — Unhalved norm

Continue to repeat that all trace distances are unhalved when comparing constants with external sources.

### D03 — Profile positivity

The profile definition correctly requires positive integers. State once that zero-length padded rounds are not profile components.

### D04 — Public mixtures

The retained mixture label is essential. Without it, convex mixing could reduce the final trace separation. The proof uses the correct direct-sum convention.

### D05 — Common conditional rule

“Common” means the preparation/control channel is the same under both hypotheses; it does not mean the old conditional receiver states coincide.

### D06 — Null histories

Keep the preparation rule defined on all formal histories, including those null under one hypothesis.

### D07 — `N<=V`

This uses positive integer block sizes. It should not be silently extended to fractional time allocations.

### D08 — Bures notation

The primary uses both `beta` and `d_B` in neighboring inherited sections. A short notation table would help.

### D09 — Unequal readout

The lower bound is deliberately nonoptimal in constants. Do not market `1/64` or `1/(128pi)` as sharp.

### D10 — Phase unwrapping

The proof ensures each factor has positive real part and the total phase lies in `[0,1/4]`; this removes branch ambiguity. Retain these inequalities.

### D11 — Clipped group

The floor argument requires `(2 Delta s)^(-1)>=2`; the stated restriction supplies it. Keep the two saturation cases visible.

### D12 — Unknown remainder

The actual biases `u_r` may vary across legal tube members. The final readout depends on `x_r`, not on `u_r`.

### D13 — Ideal controls

The GHZ encoding and recovery are known-direction ideal controls. They are not learned from the unknown device.

### D14 — Reference size

The `2d` reference bound is per used call. The reference of a whole coherent group grows with group size.

### D15 — Effective width

`V/N` is a profile statistic, not an integer width and not a memory dimension.

### D16 — Coarsening

Merging independent groups enlarges the admissible input set. For reset profiles, removing a boundary may remove a receiver operation, so only the rate comparison is asserted.

### D17 — Quadratic budgets

The certificate's compressed run-length witness is an arithmetic representation of one profile. It is not an efficient physical state-preparation circuit.

### D18 — Exact `Q`

The lower profile realizes `V` within a factor four of `Q`, not exactly `Q`. The theorem needs only constants.

### D19 — Reset error norm

The diamond norm must include arbitrary auxiliary references; an induced trace norm without reference is not enough for the stated hybrid.

### D20 — Reset error cap

Because unhalved channel distance is at most two, per-node `delta_h` may be capped at two. The executable enforces this.

### D21 — Memory witness

The transpose in `Pi^T` is harmless because the chosen Bell projector is real, but the convention should not rely on that accident in the prose.

### D22 — PPT obstruction

PPT is used only as a necessary condition for separability. No claim of PPT sufficiency is needed.

### D23 — Classical outputs

The projector `|00><00|` fixes one pair of classical labels. The witness does not use residual quantum output from the unknown measurement device.

### D24 — Lüders instruments

The paper's interface differs from discrimination with accessible post-measurement states. Add one scope sentence to prevent readers from importing instrument results into the POVM-channel model.

### D25 — Final-head evidence

The receipt artifact is small because it records identities and hashes rather than republishing the full source. The source and publication archives remain in the publication evidence package.

### D26 — CI and proof

Successful reconstruction confirms byte identity and execution, not mathematical correctness or originality.

### D27 — Signatures

The native, publication, and final metadata commits are unsigned. No human authorship signature should be inferred from GitHub identity.

### D28 — Structural companion

The structural article is independent and should not be counted as an additional premise or novelty multiplier for the profile theorem.

### D29 — Complete edition

The 258-page edition is archival preservation material, not a second journal submission.

### D30 — Historical aggregate flags

The five independent analytic closure flags correctly remain false.

---

## 9. Referee assessment of the pipeline

The recent local discrimination chain is coherent:

```text
finite-outcome interior geometry
 -> coupled covariance
 -> support kernel
 -> finite corrected orbit
 -> one-sided tangent tube
 -> nonempty neighborhoods
 -> entangled block width
 -> reset-feedback conditional fidelity
 -> complete allocation profiles
 -> hard quadratic budgets and memory boundary.
```

The new theorems use the correct immediate dependencies:

```text
canonical normalized factor + finite tube remainder
 -> one-block adaptive Bures estimate
 -> profile/policy fidelity deficits
 -> conditional feedback accumulation
 -> profile and Q uppers;

corrected GHZ block + finite Bernoulli signal
 -> unequal-signal common readout
 -> profile lower
 -> packed Q-budget lower.
```

The structural paper and the broader stochastic/analytic A/B/C/D programme are not premises. Raw local limits, stopped-path recovery, global past kernels, exact shell conditioning, process CLT/Mosco recovery, nonlinear Nisio cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction remain separate obligations.

This separation is correctly recorded.

---

## 10. Final disposition

Revision 89 closes the main mathematical and provenance objections raised in r58. In the portions reviewed, its profile theorem, hard quadratic-budget theorem, reset stability estimate, and strict tester-level memory inclusion are correct under their stated hypotheses.

The manuscript is stronger, cleaner, and more useful than Revision 88. It now gives a complete fixed-profile and hard-budget description of the local finite-use orders inside its reset resource model.

My recommendation for the four leading general mathematics journals remains **reject**, because the contribution is still a local resource refinement built from established mechanisms, with fixed-object constants and no global metric, memory-hierarchy, entropy, minimax, or synthesis theorem of comparable breadth. This judgment is about venue and conceptual scale, not a finding of mathematical invalidity.

For a leading specialist journal, I recommend **major revision**, focused on:

1. the new 2026 bounded-coherent-memory literature;
2. a completely self-contained tester-witness derivation;
3. sharper separation between operator-set inclusion and operational score separation;
4. independent specialist priority assessment; and
5. a tighter journal-facing narrative centered on the profile/reset theorem.
