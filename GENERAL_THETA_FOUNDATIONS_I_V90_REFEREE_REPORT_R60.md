# Referee Report — General Theta Foundations I, Revision 90 (r60)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current linked supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed review-ready branch:** `revision/general-theta-foundations-i-v90-operational-memory-review-ready-2026-10-06`  
**Reviewed final head:** `906e6e12841816f07e4ca31137690fd18bb65853`  
**Artifact-only publication:** `80e543020199edd7e9b9c908c78410aef7ae4dd6`  
**Qualified native source:** `e9f9673d7648c64e167994533e4b6f8a859fc2be`  
**Completed predecessor:** Revision 89, `df7ed618813224b058b97c6cbda720ad936e2c53`  
**Controlling external report:** v89/r59, `a7d030d635a2bb40c8b4f7f2265df877bad95492`  
**Controlling proof/pipeline audit:** v89/r59, `994c41dbeec1da13b6b6486876855fa30ad7cfd5`  
**Exact-final-head read-only run:** `37392910176`, conclusion `success`  
**Exact-final-head job:** `112041959803`, conclusion `success`  
**Exact-final-head artifact:** `11381544204`  
**Review branch:** `review/general-theta-foundations-i-v90-operational-memory-external-referee-r60-2026-10-06`  
**Date:** 6 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 90 is a genuine and substantial mathematical advance over Revision 89. The preceding report correctly observed that the v89 negative-partial-transpose witness separated two tester sets but did not establish a strict separation of optimal discrimination scores. Revision 90 now closes that gap on an explicit finite ensemble. For every input dimension `d>=2` and every deformation parameter `0<=t<=1`, the authors construct a finite weighted family of ordered basis measurements and prove the exact two-call Bayes values

```text
P_ca    = (d+1)/L,
P_reset = (d+1)/L + t^2(d-1)/(2dL),
P_all   = (d+1+t^2)/L,
L       = 2(d+1)-t^2.
```

Here `P_ca` is the optimum for complete first-call measurement followed by measure-and-reprepare classical adaptation, `P_reset` is the optimum for the entire unit-reset class with arbitrary receiver quantum memory and classical feedback, and `P_all` is the optimum over all two-call adaptive protocols. Both inequalities are strict for `t>0`. The separation therefore persists throughout the full-rank interval `0<t<1`, not only at a rank-deficient endpoint. In the qubit instance the exact values are

```text
3/5 < 13/20 < 4/5.
```

The proof is not merely an evaluation of three exhibited strategies. It supplies upper bounds for all protocols in the three classes and matching constructions. The middle upper, which is the difficult part, uses a filtered-swap negative-mass identity after reducing an arbitrary unit-reset protocol to a branchwise purified normal form. I have checked the displayed second moments, payoff blocks, filtered-swap spectrum, branch trace accounting, reset attainment, causal-tester upper and antisymmetric attainment. I did not find a fatal mathematical gap in Section 82 or in the inherited profile and hard-budget results used elsewhere in the paper.

The four-leading-general-journal conclusion nevertheless remains negative. The new theorem is exact and attractive, but it concerns a deliberately engineered two-use ensemble with a shared hidden basis index and specially chosen priors. It is not a theorem for an arbitrary fixed pair of measurements or channels, not a classification of finite-memory strategies, not a global metric geometry of the ordered-POVM body, and not a general equivalence between memory resources and operational advantage. The local profile theorem remains fixed-tube and nonuniform in the base measurement and tangent. The principal mechanisms—second-moment designs, swap/antisymmetric comparison, quantum comb normalization, constrained-memory discrimination, and receiver-versus-acquisition resource distinctions—have substantial antecedents. The present synthesis is strong specialist mathematics, but in my judgment it does not yet cause the breadth or conceptual displacement expected at the four leading general mathematics journals.

**Disposition outside the four leading general journals:** the focused quantitative article should receive serious consideration at a leading specialist journal in mathematical quantum information, quantum statistics, operator theory, or mathematical physics, after the proof-presentation, priority and package-hygiene revisions listed below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Frozen object and release genealogy

The latest General Theta Foundations I revision found in the complete branch survey is Revision 90. No Revision 91 branch was present when these review branches were created.

The exact review-ready head is

```text
906e6e12841816f07e4ca31137690fd18bb65853.
```

The mathematical source is frozen at

```text
e9f9673d7648c64e167994533e4b6f8a859fc2be,
```

and the artifact-only publication is

```text
80e543020199edd7e9b9c908c78410aef7ae4dd6.
```

The publication commit is the direct child of the native source and adds the four rendered manuscripts and source-bound evidence. It does not change theorem source. The review-ready head is two metadata-only commits beyond publication: it adds the review entry and the exact-final-head request. It does not change source, executables, PDFs or build receipts.

The controlling r59 report and pipeline audit reviewed v89 at `df7ed618...` and are frozen in the v90 directory by commit and blob identity. The response does not rewrite their negative recommendation as approval.

The current package contains:

```text
primary article:             49 pages,
linked binary supplement:    87 pages,
independent structural paper:41 pages,
complete research edition:  263 pages.
```

The primary is the journal-facing mathematical object. The complete edition is an archival preservation object, not a second submission or an additional significance claim.

---

## 2. Main mathematical contribution

### 2.1 The finite ensemble

Let `S` be the swap on `C^d tensor C^d`. The paper chooses a finite weighted family of ordered orthonormal bases whose rank-one projections satisfy

```text
sum_b w_b P_y^b tensor P_z^b
 = (I+S)/(d(d+1))                  if y=z,
 = (d I-S)/(d(d^2-1))              if y!=z.
```

The existence proof averages an ordered basis over Haar measure and applies Carathéodory in a real vector space of dimension at most `d^6`, giving at most `d^6+1` bases. This is a valid compactness argument. It is not an efficient construction, and the manuscript states that limitation.

The two hypotheses are:

```text
C_y       = I/d,
E_y^b(t)  = (1-t)I/d + t P_y^b.
```

The basis index `b` is sampled once and the same device is used twice. The prior is chosen as

```text
p_C=(d+1-t^2)/L,
p_E=(d+1)/L,
L=2(d+1)-t^2.
```

The first moments coincide:

```text
sum_b w_b E_y^b(t)=C_y.
```

Thus every one-call strategy sees the same averaged channel under the two hypotheses, and the one-call optimum is the larger prior `p_E`. The two-call signal is a second-moment signal generated by reusing the same hidden device. If the alternative basis were independently redrawn at the two calls, the signal would disappear. This distinction is stated correctly and is essential.

### 2.2 Payoff blocks

In the fully transposed unnormalized Choi convention, after dephasing the classical outputs, the gain over always declaring the alternative is

```text
P-p_E = sum_yz tr(T_{0,yz} W_yz).
```

With `k=t^2/(dL)`, the moment identities give

```text
W_yy = -k S,
W_yz = -2k Pi_-/(d-1)  for y!=z.
```

I checked this substitution. The off-diagonal payoff blocks are negative semidefinite. The only possible positive gain comes from the negative spectrum of the swap in the equal-label blocks.

### 2.3 Complete-measurement classical adaptation

Every effect of the measure-and-reprepare class is a limit of sums of positive products across the two complete call slots. For a positive product,

```text
tr[(A tensor B)S]=tr(AB)>=0.
```

Therefore the diagonal block `-kS` gives no positive gain, and the off-diagonal blocks are already nonpositive. The optimum is exactly the constant decision:

```text
P_ca=p_E=(d+1)/L.
```

This argument is concise and correct for the stated closed class.

### 2.4 Filtered-swap identity

For positive `A,B`, define

```text
K=(sqrt(A) tensor sqrt(B)) S (sqrt(A) tensor sqrt(B)).
```

The new lemma proves

```text
tr(-K)_+
 = 1/2[(tr sqrt(sqrt(A) B sqrt(A)))^2-tr(AB)]
 <= (d-1) tr(A) tr(B)/(2d).
```

The spectrum consists of the positive eigenvalues `lambda_i` of `sqrt(A)Bsqrt(A)` and the pairs `+/-sqrt(lambda_i lambda_j)`. This gives the equality formula. The upper follows from

```text
tr(AB) >= ||sqrt(A)sqrt(B)||_1^2/d,
||sqrt(A)sqrt(B)||_1^2 <= tr(A)tr(B).
```

The equality characterization is also correct: for nonzero factors, equality in both steps forces the normalized positive operators to coincide and the common spectrum to be flat, hence both factors are scalar multiples of the identity. The manuscript should nevertheless expand the equality proof, as requested below, because this is load-bearing and the current polar-decomposition sentence is compressed.

### 2.5 Upper for the entire unit-reset class

The authors purify the first acquisition and retain the environment of every intervening receiver instrument as an upper relaxation. On a branch `(y,h)`, the first conditional receiver operator is represented by a rectangular map `C_yh`, with

```text
A_yh=C_yh^* C_yh,
sum_h A_yh=C_0^* C_0  for every y,
tr(C_0^*C_0)=1.
```

The fresh second acquisition is conditionally independent of the old receiver and has a purification map `D_yh`, with

```text
B_yh=D_yh^*D_yh,
tr B_yh=1.
```

For an equal-label payoff block, arbitrary final receiver processing can extract at most the positive mass of the filtered swap. The lemma gives branch contribution at most

```text
k(d-1) tr(A_yh)/(2d).
```

The trace accounting is

```text
sum_yh tr(A_yh)=d.
```

Consequently

```text
P_reset-p_E <= k(d-1)/2
              = t^2(d-1)/(2dL).
```

This upper permits arbitrary receiver quantum dimension, arbitrary common instruments, retained environments, public randomization, classical feedback and countably many outcomes. No bound on receiver dimension enters. The proof uses the reset cut only at the fresh preparation, not as a separability condition on final tester effects.

The reduction is mathematically plausible and, in my reading, correct. It is also the most delicate step in the paper. The current argument should be promoted to a separate normal-form lemma with explicit spaces and maps so that a reader can verify that every mixed, randomized, history-dependent unit-reset protocol is covered without relying on narrative compression.

### 2.6 Reset attainment and equality information

Two independently prepared normalized maximally entangled input-reference pairs attain the reset upper. Declare the scalar hypothesis precisely when the two classical labels agree and the two references occupy the antisymmetric subspace. The event probability is

```text
(d-1)/(2d^2)       under C,
(1-t^2)(d-1)/(2d^2) under every E^b(t).
```

The resulting gain equals the reset upper.

The equality condition of the filtered-swap lemma further shows that a nonrandomized optimal protocol in the displayed purified normal form has branchwise isotropic factors. This is an informative rigidity observation. The paper correctly avoids claiming uniqueness of dilations or final readouts.

### 2.7 Upper and attainment for all adaptive protocols

The deterministic two-call tester normalization is written in output-dephased blocks as

```text
T_0+T_1=Xi tensor I_{Y_2},
tr_{I_2} Xi_y=rho,
tr rho=1.
```

Rather than invoking this abstractly, the revision derives it from an initial purification, a trace-preserving intervening map after the first classical label, and the final decision effect. This establishes positivity of `Xi_y`, positivity of the complementary tester and

```text
0 <= T_{0,yz} <= Xi_y,
tr Xi_y=1.
```

Because `-kS<=kI` and the off-diagonal payoff blocks are nonpositive,

```text
P_all-p_E <= k sum_y tr Xi_y = kd=t^2/L.
```

A normalized antisymmetric state on the two device inputs, followed by the equal-label event, attains this bound. Its equal-label probability is `1/d` under `C` and `(1-t^2)/d` under every alternative. Hence

```text
P_all=(d+1+t^2)/L.
```

The upper and attainment are correct in the stated classical-output interface.

### 2.8 Robustness and budget normalization

The two-call hybrid estimate changes any fixed decision probability by at most `delta` when every channel is perturbed by at most `delta` in unhalved diamond norm. Taking suprema over a fixed class preserves the same two-sided bound. A hard pathwise preparation defect `epsilon` changes the exhibited reset score by at most `epsilon/2`. The displayed sufficient condition

```text
2 delta + epsilon/2 < t^2(d-1)/(2dL)
```

correctly preserves the reset-over-classical gap.

The normalization of real hard thresholds to integer resources is also correct for positive integer reservations. It must remain separated from expected-cost and fractional-duration models.

---

## 3. Relation to the inherited pipeline

The local discrimination chain remains:

```text
coupled covariance
 -> complete support kernel
 -> corrected finite orbits
 -> normalized curves and one-sided tubes
 -> nonempty neighborhoods
 -> complete-group width
 -> conditional reset fidelity
 -> prescribed allocation profile V=sum n_r^2
 -> hard policy budget Q=max_paths sum n(h)^2.
```

The upper chain is

```text
normalized finite realization
 -> one-block Bures bound retaining n r s^2
 -> conditional subnormalized fidelity
 -> profile/policy upper.
```

The lower chain is

```text
corrected GHZ block
 -> finite binary event retaining m kappa s^2
 -> common unequal-signal readout
 -> integer packing.
```

Revision 90 does not replace these results. It adds a logically separate exact finite experiment that turns the receiver-versus-acquisition distinction into a strict optimal-score hierarchy. The exact game is conceptually connected to the local resource taxonomy, but it is not a corollary of the fixed-tube theorem and does not make that theorem global.

The wider analytic programme remains independent. In particular, the finite measurement results do not close the historical A2 replacement, B4 aggregate, C2 aggregate, eleven-paper aggregate or whole-Theta-program aggregate. The current machine-readable status correctly leaves all five flags false.

---

## 4. Priority and significance

The v90 comparison now discusses the directly relevant 2026 memory literature. Zonnios–Binder introduce a coherent-memory-dimension hierarchy for autonomous multi-time process testers and prove finite-time completeness. Ohst–Zhang–Nguyen–Plávala–Quintino formulate auxiliary-memory restrictions through constrained separability and treat classical and quantum adaptive memory. These models differ from the present hard reset cut and quadratic reservation, and neither source appears to contain the exact theorem above.

The paper also credits finite second-moment designs, antisymmetric measurement comparison and single-shot measurement discrimination. A targeted search did not reveal an equivalent statement giving all three exact values over the complete unit-reset class on this particular ensemble. That observation is not an independent priority certificate. The exact optimum for unrestricted receiver storage under a fresh-preparation cut is specialized enough that it should be checked by a human specialist familiar with quantum combs, memory-constrained testers and measurement comparison before a strong novelty formulation is accepted.

The mathematical advance over v89 is real:

- strict tester inclusion is upgraded to strict exact score separation;
- the middle upper covers the full unit-reset class, not a separable-effect relaxation;
- the theorem holds in every dimension;
- it persists along a full-rank depolarizing family;
- matching strategies and a rigidity condition are given.

The reason for my negative four-journal recommendation is therefore not that the revision failed to answer r59. It answered the central objection positively. The remaining issue is journal scale. The exact game is highly structured, two-use and ensemble-specific. The local geometric theorem remains fixed-object and nonuniform. The paper does not yet derive a general structural invariant determining when retained receiver memory, reset feedback or coherent acquisition yield strict operational gaps. Such a theorem—or a comparably broad global geometry—would change the general-journal assessment.

---

## 5. Reproducibility and provenance

The native source reports 746 files, preserves all 710 predecessor native files in active or byte-identical audit paths, and retains all 998 predecessor complete-edition labels. Forty auxiliary labels were moved to the linked supplement without deletion. The structural source graph remains unchanged.

The build receipt records:

```text
30 regression suites,
normal and python -O outputs identical,
isolated native reconstruction successful,
standalone journal reconstruction successful,
no unresolved references or citations,
no reported overfull or underfull boxes.
```

The finite game checker exercises the qubit moments and scores, filtered-swap identities in several dimensions, noncommuting examples, strictness formulas and negative controls. These are useful regressions, not proofs of the universal theorem.

The publication transport run `37391691284` has overall conclusion `failure`; it completed the build and produced the exact native and publication commits, but the final atomic ref update failed after a workflow-permission timeout. The repository records the subsequent sequential API handoff honestly. This failed run must not be displayed as a successful publication badge.

The exact final head `906e6e...` separately triggered run `37392910176`. Its read-only `final-head` job `112041959803` completed successfully, checked out that exact SHA without persisted write credentials, reconstructed the submitted object and uploaded artifact `11381544204`. That is the controlling exact-head qualification. The successful Actions check is not a legacy commit status; the legacy combined-status list is empty.

The native, publication and review-ready commits are unsigned. Object identity, reproducible reconstruction and Actions checks have their stated provenance value, but are not cryptographic human-authorship signatures. The manuscript does not claim otherwise.

---

## 6. Required revisions before specialist-journal submission

### R01 — Isolate the unit-reset normal-form lemma

State and prove a standalone lemma that every two-call unit-reset protocol, including mixed fresh inputs, arbitrary receiver instruments, public randomization, countable outcomes, null histories and unrestricted receiver dimension, admits the branchwise `C_yh,D_yh` representation used in the upper. Specify all Hilbert spaces, transposes, rectangular maps and trace identities. The current proof contains the right ideas but compresses the decisive reduction.

### R02 — Define the three optimization classes formally in Section 82

Give self-contained definitions of `P_ca`, `P_reset` and `P_all`, including closure, classical randomization, early stopping, final joint measurements and the convention for a discarded second call. Cross-reference the inherited reset definition, but do not make the exact theorem depend on reconstructing a resource model from prose scattered across earlier sections.

### R03 — Expand the filtered-swap equality proof

Separate the spectrum calculation, the two inequalities and their equality conditions. State explicitly that equality in normalized fidelity forces equality of the normalized positive operators, and then that equality in the eigenvalue Cauchy–Schwarz step forces the flat spectrum. Treat singular nonzero factors without relying only on approximation language.

### R04 — Put the shared-latent-variable experiment on the theorem page

The fact that one basis index is drawn once and reused twice is mathematically load-bearing. Repeat it immediately in the theorem statement or a boxed game definition. Also state there that independently redrawing the basis makes the two-use averaged alternative equal to the scalar product channel.

### R05 — Add a fully explicit qubit tester calculation

For the `3/5,13/20,4/5` example, display the seven devices, priors, two normalized maximally entangled pairs, antisymmetric reference effect, antisymmetric two-input state, and all normalization factors in one compact appendix or example. This will prevent confusion between normalized and unnormalized maximally entangled vectors and between input and reference antisymmetry.

### R06 — Complete independent priority assessment

Obtain specialist comparison against memory-constrained comb/tester formulations, measurement comparison and design-based ensemble discrimination. The author-side literature audit is materially improved, but it is not independent priority clearance. Phrase novelty as the specific exact three-class optimization unless and until broader priority is established.

### R07 — Separate the two main theorems conceptually

The primary should explain more sharply what the local profile theorem and the exact ensemble theorem share and what they do not. The former is an asymptotic local-order theorem for a fixed tube and arbitrary hard resources; the latter is a finite exact Bayes theorem for one designed ensemble. Neither implies the other.

### R08 — Replace stale current-audit headings

The top-level `PROOF_AUDIT.md` and `HISTORY_AND_PIPELINE_AUDIT.md` still identify Revision 89, while `INTERNAL_MATHEMATICAL_REVIEW.md` identifies Revision 81. Preserve those historical files under predecessor audit paths, but provide current v90-named audits at the active top level. A referee should not have to infer which top-level audit is current.

### R09 — Use printed numbering consistently

The source module `sections/82-...` compiles as Section 15 in the primary and Section 81 in the complete edition. Journal-facing prose should use printed primary numbering first and source-module numbering second. The current review entry explains the distinction, but the response and audit files still rely heavily on source numbers.

### R10 — Tighten the finite-design statement

Make explicit whether the Carathéodory weights are merely real, whether exact algebraic/rational data are needed anywhere, and that no efficient design construction or polynomial bit-complexity result is claimed. The crude `d^6+1` bound is acceptable for existence but should not be read as a complexity theorem.

### R11 — Clarify robustness quantifiers

State whether the same `delta` bounds the scalar device and every basis device individually, and that the priors and latent-index law remain fixed. Keep the unhalved diamond convention adjacent to the score perturbation. Distinguish optimal-class stability from the additional preparation defect of the exhibited reset implementation.

### R12 — Preserve the exact release semantics

Continue to distinguish the failed publication transport, sequential API ref handoff, successful exact-head Actions check, empty legacy-status list and unsigned commits. Do not collapse these into a single “CI passed” statement.

### R13 — Reduce archival apparatus in the journal-facing package

The 49-page primary is substantially improved, but the surrounding repository package remains difficult to navigate. The journal submission should consist of the primary, one linked supplement and a concise reproducibility note. Historical responses, dozens of schemas and complete-edition preservation material should remain available in the archive rather than in the referee’s initial route.

### R14 — Retain all scope restrictions

Do not promote the finite ensemble hierarchy to an arbitrary fixed-pair theorem, a universal score separation, a full coherent-memory-dimension hierarchy, a global POVM-body metric, or a general synthesis result. The present machine-readable flags are appropriately conservative.

### R15 — Keep the wider Theta pipeline logically separate

The historical A2/B4/C2 and later statistical/analytic obligations remain independent. No finite-dimensional measurement theorem should be used as a substitute for raw local limits, path recovery, process CLT/Mosco, nonlinear generator cores, filtering/LAN or labelled posterior contraction.

---

## 7. Detailed comments

### D01 — Priors

Verify at the first occurrence that `p_C+p_E=1` and that `p_E>=p_C`, with equality only at `t=0`. This makes the constant-decision baseline immediate.

### D02 — One-call equality

State the equality of the averaged one-call channels as a channel identity, not only componentwise effects. This clarifies that arbitrary one-call entangled inputs do not help.

### D03 — Finite design terminology

Use “weighted exact second-moment family” consistently. It need not be an unweighted projective 2-design.

### D04 — Carathéodory dimension

The `d^6` ambient bound is safe but loose. Say “at most” and avoid suggesting optimal support size.

### D05 — Classical class closure

The sentence “This proof also covers limits” should identify the topology, preferably finite-dimensional trace/operator norm closure of the tester cone.

### D06 — Complete call slots

In the separable tester formula, specify that the bipartition is across complete call slots, including each input and classical output factor under the adopted Choi ordering.

### D07 — Transpose convention

Repeat once in the proof that `S` and `Pi_-` are real in the chosen basis, so the full transpose does not change the payoff blocks.

### D08 — Rectangular maps

The notation `C_yh E_y^T C_yh^*` and `D_yh` permits larger receiver spaces. State dimensions explicitly to avoid an accidental square-matrix reading.

### D09 — Instrument completeness

Derive `sum_h A_yh=C_0^*C_0` from the trace-preserving sum of the branch maps, including a remainder branch when a countable instrument is truncated.

### D10 — Null histories

The exact game has positive effects for `t<1`, but the theorem includes `t=1`. Preserve the formal-history convention at zero-probability branches.

### D11 — Positive-part optimization

State the elementary identity

```text
sup_{0<=F<=I} tr(FX)=tr(X_+)
```

where it is used in the reset upper.

### D12 — Equality rigidity

Clarify whether branchwise isotropy is asserted only for nonrandomized protocols in the selected dilation normal form. The present qualification is correct and should remain.

### D13 — Countable outcomes

A short lemma or citation for monotone trace-class convergence would be preferable to an inline truncation remark.

### D14 — Reset attainment

Make clear that the two device inputs are independent, while the two retained references are measured jointly only after both calls.

### D15 — Classical feedback

The optimal reset construction uses no feedback. The theorem’s significance is that feedback and arbitrary receiver processing cannot improve it; emphasize this asymmetry.

### D16 — Adaptive tester construction

The direct circuit-to-tester derivation is valuable. Move it into a named proposition so the positivity and marginal constraints can be cited independently.

### D17 — Antisymmetric attainment

State that the antisymmetric state is normalized and supported entirely on `Pi_-`; for `d>=2` the subspace is nonzero.

### D18 — Qubit ordering

The six devices are the three Pauli eigenbases with both outcome orders. State why both orders are included in the weighted ordered-basis family.

### D19 — Score versus unhalved norm

Keep the factor `1/2` when converting an unhalved trace-norm perturbation into a decision-probability perturbation. The current robustness proof does this correctly.

### D20 — Perturbed latent family

Clarify whether perturbations may depend on the basis index and label, provided each entire measurement channel is within `delta`.

### D21 — Exact values at `t=0`

At `t=0`, all devices coincide and all three values are `1/2`. State this beside the strictness clause.

### D22 — Endpoint `t=1`

At `t=1`, alternatives are projective and some branch probabilities vanish. This does not invalidate the normal-form proof, but the endpoint convention should be explicit.

### D23 — Local theorem constants

The exact finite game is uniform in dimension only through its formula. Do not use it to suggest uniform constants for the fixed-tube local theorem.

### D24 — Effective width

Continue to state that `V/N` and hard `Q` are call-allocation resources, not Hilbert-space memory dimensions.

### D25 — Individual policy versus class optimum

A large `Q_pi` is an upper resource certificate, not a lower information certificate. The manuscript states this correctly.

### D26 — Relocated mathematics

The forty relocated labels are active in the current linked supplement. The journal package should contain the supplement and preserve cross-reference stability.

### D27 — Build warnings

The complete-edition log has three font-expansion warnings. The current review entry reports them honestly; do not describe the build as entirely warning-free.

### D28 — Actions semantics

Use “check run” for `final-head` and reserve “commit status” for the legacy status API. The latter is empty at the reviewed head.

### D29 — Signatures

Unsigned commits are not evidence against mathematical correctness, but object reconstruction is not a human signature. Keep these concepts separate.

### D30 — External review

The current report is an author-requested external mathematical assessment stored in the repository. It is not a commissioned editorial decision by any named journal.

---

## 8. Final assessment

Revision 90 succeeds on its own stated mathematical objective. It turns the receiver-versus-acquisition distinction into an exact operational hierarchy, proves the difficult unit-reset upper over the full intended class, retains the finite local profile and hard-budget laws, and corrects the provenance weakness identified in earlier rounds. I find no fatal correctness defect in the new theorem as submitted.

The reason for rejection at the four leading general mathematics journals is significance and breadth, not proof failure. The exact hierarchy is an elegant, specialized two-use ensemble theorem; the local geometry remains fixed-tube and nonuniform; the wider memory and global geometry questions remain open; and independent specialist priority has not yet been supplied. With the normal-form proof expanded and the package streamlined, the focused article is a strong specialist-journal submission.
