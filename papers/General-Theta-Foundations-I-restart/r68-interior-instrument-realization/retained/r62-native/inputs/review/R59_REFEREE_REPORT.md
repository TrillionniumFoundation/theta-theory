# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r59-causal-task-order-2026-10-14`  
**Reviewed exact branch head:** `8da12b07fbed64e13bb4bb42bfc73fc56c85d37a`  
**Reviewed branch root tree:** `16a4d37aac0df4be5ea3e0b8c5c843ff8e1991b1`  
**Ordinary mathematical-source commit:** `29de5433c2c4f45d5174a87a8588fd3a24d3f84a`  
**Stored artifact commit:** `fcdb32640e4bb69922f07233fa6148bfc9b13165`  
**Native PDF SHA-256:** `d242364dc8d2e67dd76b0aede802cb3fc7e0bfa3879fce4e4612ee38f644ac7d`  
**Native article length:** 25 pages  
**Complete source-built R58 companion:** 37 pages  
**Complete deposited mathematical packet:** two PDFs, 62 pages  
**Predecessor external report:** R56 review head `73d3876b1186672d83ab2df515221bff2abd391f`  
**Review branch:** `review/general-theta-restart-r59-causal-task-order-external-top4-referee-r59-2026-10-15`  
**Date:** 15 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript’s present form.**

This is **not a technical-correctness rejection**.

Revision R59 is a genuine and substantial mathematical response to the R56 report. The load-bearing ambiguity in the earlier autonomous resource theorem has been repaired: the manuscript now defines two distinct finite-state interfaces. In the event-stopped interface, live routing and terminal output roles may reuse the same labels because the terminal event ends the computation. In the state-stopped interface, a fixed state-only halt map makes live and terminal labels globally disjoint. The resulting resource formulas use `max(live, outputs)` in the former interface and `live + outputs` in the latter. I find this semantic repair correct and sufficient to remove the principal technical objection in the R56 report.

The new center is also mathematically stronger than the earlier exact-balance theorem. R59 no longer requires the lower and upper constructions to match one reference experiment exactly. Instead it combines:

1. relative order of unnormalized report and task measures;
2. actual-occupation-weighted additive mass and loss defects;
3. one fixed operating witness for the all-strategy lower;
4. one parameter-independent common acquisition program for the all-model upper;
5. separate effort constants for the two directions; and
6. explicit checkpoint, event-stopped, and state-stopped resource widths.

The proof avoids a common but serious error in stopped comparison arguments. It never runs the competing strategy on the comparison experiment and never assumes that such a hypothetical execution would terminate. It keeps every pre-call history distributed according to the actual witness model and replaces only the current productive report–audit row in an unnormalized occupation integral. This yields a finite comparison measure with a density cap, a retained mass lower, and a task-loss lower. The upper is independently obtained from a uniform conditional hazard and a predictable sum of whole-attempt costs. No renewal or independent-attempt assumption is used.

In the load-bearing arguments I checked, I did not find an elementary gap invalidating:

- attainment of the trimmed task profile;
- construction of the actual-history comparison measures;
- the all-strategy lower at one fixed witness;
- the common all-model conditional-hazard upper;
- the event/state role-packing lemma;
- the exact checkpoint and typed/event specializations;
- the scale-uniform relative-order corollary;
- the positive matrix-measure criterion for localized affine-square tasks;
- the measurable changing-rank range characterization;
- the positive-instrument continuity estimates through likelihood zeros;
- the non-power sublevel comparison;
- the regular marked profile and its two competing scales;
- the finite mixed-dimensional acquired-law theorem;
- the exact acquired zero-loss-atom threshold;
- the classical transitive-group realization;
- the noncommuting quantum Weyl realization;
- the effective finite-description approximation under the additional declared inputs;
- the resource-certified simulator composition;
- the same-task core/erasure/calibration construction;
- the guarded finite command-calibration proposition; or
- the source, artifact, and read-only reconstruction claims at the level at which they are stated.

The negative top-four judgment concerns the **intrinsic reach, novelty relative to the surrounding experiment-comparison and causal sampling literature, natural external consequences, and breadth suggested by the title**, rather than an identified fatal proof defect.

The theorem remains a strong sufficient-class transfer result. Its lower requires one actual model with full-report task-order inequalities at every reached history and every chosen legal command, an all-strategy effort inequality, and occupation-defect bounds uniform over every budget-feasible competitor. Its upper requires one parameter-independent attempt program satisfying full conditional mass and task inequalities on every surviving history in every operating model. These assumptions are mathematically meaningful and verified in the displayed raw classes, but they are not an intrinsic or near-necessary classification of general causal experiments.

The reference profile itself is a marked trimmed population-quantization functional. R59 correctly credits trimmed quantization. However, its bibliography still does not adequately compare the paid causal selection mechanism with the direct rejection-sampling and endogenous-stopping literatures. In particular, the manuscript should compare its density cap, expected-attempt budget, and common conditional hazard with:

- Jingbo Liu and Sergio Verdú, *Rejection Sampling and Noncausal Sampling under Moment Constraints*, ISIT 2018, DOI `10.1109/ISIT.2018.8437857`;
- Daniel Goc and Gergely Flamich, *On Channel Simulation with Causal Rejection Samplers*, arXiv:`2401.16579`; and
- Zihao Li, *The Order of Binary Experiments under Endogenous Stopping*, arXiv:`2608.19897`.

These papers do not obviously contain R59’s finite-output task geometry, event/state role accounting, actual-history defect integration, or singular task-matrix order. They do, however, occupy the closest conceptual neighborhood of causal rejection, expected sampling cost, experiment order under stopping, and sampling–covering duality. A top-four novelty claim cannot be assessed persuasively without a theorem-level comparison.

For a strong specialist journal in mathematical statistics, information theory, stochastic control, quantization, sequential decision theory, selective prediction, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance, and pipeline inspected

A fresh complete enumeration of `referee-ready/general-theta-restart-*` branches identified

```text
referee-ready/general-theta-restart-r59-causal-task-order-2026-10-14
```

as the latest completed `General Theta Foundations I` referee-ready revision. The continuation page was empty. The external-review catalogue stopped at R56; no R59 external report existed before the present branch was created.

The exact review object is the terminal evidence-bound head

```text
8da12b07fbed64e13bb4bb42bfc73fc56c85d37a.
```

Its sole parent is the artifact publication commit

```text
fcdb32640e4bb69922f07233fa6148bfc9b13165.
```

The immutable ordinary mathematical source is

```text
29de5433c2c4f45d5174a87a8588fd3a24d3f84a.
```

I reviewed the 25-page native article as the editorial object. The complete 37-page R58 companion was used to inspect inherited theorem ancestry, the R56 semantic repair, absolute-calibration theory, nonintervening directional sensing, and earlier computation and stopped-flow statements. I did not treat the companion as a hidden premise of the new affine theorem.

The inspection included:

- `main.tex`, all eight native sections, both appendices, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, and `NOTATION_AUDIT.md`;
- the complete R56 external report and the R59 point-by-point response;
- the role of R57 and R58 as intervening author repairs and inherited mathematics rather than external decisions;
- the canonical restart controls, theorem targets, and predictive-quotient boundary;
- the source manifest, verification and regression scripts, build program, publication receipt, clean rebuild receipt, final read-only verification, and referee entry;
- the relation between the native manuscript and the complete R58 companion; and
- targeted primary-source comparison with trimmed quantization, Blackwell comparison, causal rejection sampling, moment-constrained rejection sampling, endogenous-stopping experiment order, predictive-state representations, and quantum statistical sufficiency.

The build receipt records:

- 25 native pages;
- 37 companion pages;
- 82 native labels and 91 native cross-references;
- 13,247 new exact finite checks plus four deliberate structural negative controls, as summarized by the referee entry;
- byte-identical ordinary and optimized regression results;
- three-pass TeX builds with no undefined references, citations, or overfull boxes; and
- a clean read-only rebuild reproducing both PDFs and extracted texts on the recorded host and toolchain.

The publication packet originally recorded GitHub Actions run `38562870143` as queued and correctly declined to count it as a passed independent-host build. A later direct remote readback shows that this run completed successfully. The repository evidence should be updated in a successor revision to distinguish the time-stamped earlier observation from the later final result.

These controls are valuable source-integrity and reproducibility evidence. They are not mathematical proof, novelty certification, or journal acceptance. I did not independently re-prove every theorem in the v1–v96 archive or every historical realization branch. The repository’s own history audit states the same limitation.

---

## 2. Executive mathematical assessment

### 2.1 The central profile

The comparison preparation produces a genuine joint report–audit law

```text
K_0(dx,dz)
```

with report marginal `nu`. The task coordinates are derived, not prescribed:

```text
f(x) = E_0[Z | x],
w(x) = E_0[||Z-f(x)||^2 | x].
```

For a finite dictionary `C`, the conditional squared task is

```text
d_C(x) = w(x) + dist(f(x),C)^2.
```

The profile is

```text
Q_m(b)
 = min ∫ [w+dist(f,C)^2] h dnu,
```

where `|C|<=m`, `0<=h<=b`, and `∫h dnu=1`.

The density cap has a physical interpretation. Selecting a unit output law from a proposal law with expected-attempt budget `b` cannot place density more than `b` on any report set. Rejected reports remain charged through that cap. The task mark `w` remains in the objective and prevents a formal location quantizer from conditioning away residual audit uncertainty.

This profile is a useful object. Its statistical ancestors should be kept visible: it is a marked, renormalized trimmed-quantization functional, not a newly discovered static variational principle. The mathematical contribution lies in the causal lower and upper which connect it to an unknown-model experiment with explicit resources.

### 2.2 The quantifier split

R59 separates the two directions correctly.

The lower assumes one fixed actual model `theta_*`. For every competing program, every reached productive prehistory, and every selected legal command, the current actual report–audit row is compared with a reference row on the **full current report space**. This is supplemented by:

```text
E_* C_tau >= kappa_- E_* A_tau
```

for every competitor and by actual-occupation bounds on accumulated mass and task defects.

The upper assumes one parameter-independent attempt program `G`, valid after every surviving history in every model. Its complete attempt cost is uniformly bounded, and its current virtual report and exported task readout satisfy lower mass and upper task inequalities relative to the same reference law.

This is the correct minimax architecture:

- one witness model lower-bounds `inf_program sup_theta`;
- one common program upper-bounds `inf_program sup_theta`;
- no `inf sup = sup inf` exchange is used; and
- the witness and construction need not be the same operating experiment.

### 2.3 New mathematical content over R56

The earlier theorem used exact task balance. R59 permits simultaneous relative and absolute errors. Relative order changes the effective budget and risk constants but preserves zero task directions. Absolute defects accumulate under actual acquisition occupation and can be amplified by repeated selection.

This distinction is substantive. A small one-call absolute task error can become a `b e` stopped-risk error when a sampler concentrates on a set of proposal mass `1/b`. A two-sided relative task order cannot create positive loss on a task direction which was exactly zero. R59’s boundary example and singular matrix-order theorem correctly isolate these two regimes.

---

## 3. Response to the R56 external report

R59 and its R57/R58 ancestry address the principal R56 defect correctly.

| R56 issue | R59 assessment |
|---|---|
| `B` reached live labels did not imply only `M-B` terminal values | **Resolved.** Event stopping permits role reuse and uses `max(live,outputs)`; state stopping has a fixed global halt type and uses `live+outputs`. |
| The observer semantics were under-specified | **Resolved.** Command inputs, current report, fresh coins, persistent label, decoder and halt interface are formally separated. |
| Headline equalities conflated checkpoint and autonomous resources | **Resolved.** General inequalities are stated first; exact checkpoint, event, and state formulas are separate. |
| The sufficient class needed a name and full quantifiers | **Resolved.** The affine task-order theorem declares one witness, one common construction, actual occupation and effort hypotheses. |
| Unequal effort constants were hidden | **Resolved.** `kappa_-` and `kappa_+` are retained throughout. |
| Report balance alone was insufficient | **Resolved.** Full-report task moments/order are assumed; Appendix B supplies an all-program failure witness. |
| Pre-command and post-command tasks were conflated | **Improved.** The new raw realizations explicitly concern post-command audits; the nonintervening directional result remains in the companion. |
| Effective implementation was not separated from Borel existence | **Resolved in scope.** The effective corollary adds physical partitions, integration, approximation and finite costs. |
| Calibration confidence could fail robust termination | **Resolved for the fixed sampler model.** A deterministic guard, fallback, pilot cost and memory are charged. |
| The theorem remained a sufficient balance class | **Still true.** R59 does not provide an intrinsic necessary-and-sufficient classification. |
| A major natural application was needed | **Still unresolved.** The displayed classical and quantum families validate the mechanism but do not settle a widely recognized open problem. |
| Top-four impact was not established | **Still unresolved.** The new theorem is stronger, but its external reach remains limited by its certificates. |

The repair is not cosmetic. The autonomous exact statements now have a coherent formal model, and the new central theorem addresses a larger class of comparison errors.

---

## 4. Audit of the all-strategy lower

### 4.1 Actual-history construction

The central lower does not define a comparison stopping time. This is essential.

For a fixed competitor and terminal dictionary `C`, the proof adjoins one current independent uniform variable so that randomized stopping and output can be represented as deterministic functions of the current augmented report. At each actual reached productive history `h` and selected command `a`, it integrates the acceptance/output functions against the comparison row `P^0_{h,a}` and then averages these contributions over the **actual pre-call occupation** under `theta_*`.

This produces finite measures `xi_c` on the comparison mark space. Their sum `xi` is not claimed to be the terminal law of any comparison execution.

That qualification is mathematically decisive. A competitor which terminates under the actual model may fail to terminate if its reports were replaced at every time by comparison reports. R59 never requires such a pathwise substitution.

### 4.2 Density cap

Dropping the current acceptance indicator gives

```text
xi <= E_* A_tau * nu.
```

The effort inequality and actual expected-cost budget imply

```text
E_* A_tau <= N/kappa_- = b_-.
```

Hence

```text
xi <= b_- nu.
```

This is the correct unnormalized proposal domination. No rare report stratum is conditioned to mass one without paying for its acquisition.

### 4.3 Retained selected mass

The actual commitment indicators have total mass one because the actual competitor commits exactly once almost surely. Applying the lower mass inequality at each reached current row and summing gives

```text
1 <= u_- xi(X) + A_N.
```

Therefore

```text
xi(X) >= t_N = (1-A_N)_+/u_-.
```

The proof then scales `xi` down, not up, to a measure of mass `t_N`. This preserves the cap and avoids an invalid normalization when the retained mass is less than one.

### 4.4 Task lower

The lower task inequality is conditioned on the full current report. This excludes an important failure mode: a displayed mark may be constant while another visible report coordinate reveals the audit.

Summing over the disjoint actual commitment events gives

```text
actual risk
 >= l_- Σ_c ∫ d_c dxi_c - E_N.
```

For each mark, the chosen output cannot beat the nearest point of the competitor’s terminal dictionary. Scaling the accepted comparison measure gives

```text
R_i >= [l_- t_N Q_{m_-}(b_-/t_N)-E_N]_+.
```

The decoder-width bounds used here are now correct:

- checkpoint: at most `M` outputs;
- event-stopped: at most `M` outputs;
- state-stopped: at most `M-B_0` terminal outputs when `B_0` reached live labels are certified.

I find this lower proof sound under the stated hypotheses.

### 4.5 Strength of the lower hypotheses

The mathematical validity of the lower should not obscure its strength. The full-report inequalities must hold:

- at one common actual model;
- for every actual reached history;
- for every legal command selected by an arbitrary competitor;
- before averaging the command;
- for every Borel acceptance weight; and
- for every finite-image readout.

The occupation bounds `A_N,E_N` must also hold uniformly over the entire budget-feasible competing class. A certificate verified only along the proposed upper program is insufficient. This is the principal lower-side restriction on the theorem’s reach.

---

## 5. Audit of the common upper

### 5.1 Conditional hazard

Choose a profile optimizer at cap

```text
beta_N = l_+ b_+/(1+b_+ a_+).
```

Accept the current virtual mark with probability `h/beta_N`. The lower mass inequality for the upper construction gives, conditionally on every surviving history,

```text
P(accept next attempt)
 >= l_+/beta_N - a_+
 = 1/b_+.
```

This is a conditional hazard statement. Independence of attempts is neither stated nor needed. Induction gives survival after `j` attempts at most `(1-1/b_+)^j`.

### 5.2 Expected cost

Each begun attempt has conditional expected total attempt cost at most `kappa_+`, including unfavorable outcomes. Predictable summation gives expected total cost at most

```text
kappa_+ b_+ = N.
```

The physical hidden state need not reset after rejection.

### 5.3 Risk

The one-attempt unnormalized task contribution is at most

```text
u_+ Q_m(beta_N)/beta_N + e_+.
```

Summation over disjoint terminal attempts gives

```text
R_i
 <= [u_+(1+b_+a_+)/l_+] Q_m(beta_N) + b_+ e_+.
```

The absolute task defect is amplified by expected attempt count, exactly as the boundary example predicts.

### 5.4 Resource widths

The program uses `B` continuing roles and at most `D_0 m` terminal exports. Therefore:

- state stopping uses `B+D_0m` labels;
- event stopping uses `max(B,D_0m)` labels;
- checkpoint counts only the output width.

This correctly repairs the R56 inference.

### 5.5 First-attempt regime

When the designed cap would be below one, the manuscript uses an always-accept first attempt. This avoids evaluating the profile at an infeasible cap and preserves the physical cost bound.

I find the common upper proof sound under the declared conditional certificates.

---

## 6. Relative order versus absolute defect

The scale-uniform corollary is one of the most important conceptual points in R59.

With no additive defects, fixed constants

```text
0 < l_- <= 1 <= u_-,
0 < l_+ <= 1 <= u_+
```

lead to

```text
(l_-/u_-) Q_{m_-}(u_- b_-)
 <= R_i
 <= (u_+/l_+) Q_{m_+}(l_+ b_+).
```

Thus fixed nonunit relative calibration changes only constants and effective resource scales. It does not create a positive risk floor on a zero-loss task stratum.

By contrast, a one-call additive task error `e` can produce a stopped-risk error of order `b e`. Appendix B gives a sharp construction with a rare report set of mass `1/b`.

This distinction should be made even more prominent in the abstract and introduction. It is the most general mathematical reason for preferring task-measure order over ordinary one-call absolute proximity in selective acquisition.

---

## 7. Positive matrix task order

### 7.1 Localized affine-square family

For a report–audit law `P`, define

```text
J_P(D) = ∫_{D×H} (1,z)(1,z)^T dP.
```

The measure inequalities

```text
l J_{P0} <= J_P <= u J_{P0}
```

are equivalent to order of every localized affine-square test. Taking the constant affine coordinate gives report-mass order; summing coordinate squares of `z-r` gives squared-task order.

The extension from event indicators to arbitrary Borel `q∈[0,1]` and finite-image readouts is standard and correctly proved by simple-function approximation.

This criterion is exact for the declared rich affine-square test family. The manuscript correctly states that it is only sufficient, not necessary, for the narrower squared-prediction theorem or for existence of arbitrary causal balancing programs.

### 7.2 Singular ranges

The measurable density theorem correctly avoids a uniform inverse-eigenvalue assumption. With

```text
lambda = tr J_0 + tr J_1,
J_i = A_i lambda,
```

positive order is equivalent almost everywhere to:

- equality of kernels; and
- bounded spectrum of the congruence `A_0^{dagger/2} A_1 A_0^{dagger/2}` on the actual range.

The Moore–Penrose inverse is used pointwise, and no uniform norm of it enters the risk bound. Consequently changing rank and arbitrarily small positive eigenvalues are permitted, while a genuinely new positive task direction violates relative order. This is the correct behavior near an acquired zero-loss stratum.

### 7.3 Relation to broader experiment order

The manuscript should distinguish this localized second-moment order more sharply from:

- Blackwell order over all decision problems;
- quantum statistical sufficiency over general payoff families;
- stopping dominance and decision dominance under sequential acquisition; and
- channel simulation or rejection sampling under divergence constraints.

The present matrix order is exact for one finite-dimensional affine-square task family, not a complete order of statistical experiments.

---

## 8. Predictive quotient

Appendix A supplies a useful sufficient construction rather than assuming a quotient manifold.

A countable determining family of finite executable future tests defines a Borel map

```text
q:H_history -> [0,1]^N.
```

If the positive-evidence history space is a countable union of compact sets on which every coordinate is continuous, then the image is a countable union of compact sets and hence Borel. A Borel section is built by nested finite closed covers and shrinking compact cells.

The continuation argument uses countably many localized one-step tests. Equality of current response coordinates then implies equality of the next quotient almost surely under the common report law. Impossible reports are completed arbitrarily rather than assigned a false canonical posterior.

This is a careful and useful result. Its scope remains fixed-law and compact-exhausted. A common executable quotient for an arbitrary merely Borel unknown-model family is not established. The main upper does not store the unknown-model posterior family, which is an important and correctly stated separation.

---

## 9. Acquired geometry

### 9.1 Non-power comparison

The sublevel functional

```text
Omega_m(r)
 = max_C nu{w+dist(f,C)^2 <= r^2}
```

gives the elementary but useful bounds

```text
sup_r r^2[1-b Omega_m(r)]_+
 <= Q_m(b)
 <= inf{r^2: Omega_m(r)>=1/b}.
```

These bounds retain actual acquired mass and require no preassigned local dimension. They should be used as the conceptual geometric theorem, with the power laws treated as corollaries.

### 9.2 Regular marked profile

Under the global rectangle estimate

```text
sigma(B(x,r)×[0,s]) ~ r^d s^alpha,
```

R59 obtains

```text
Q_m(b)
asymp max{b^{-2/alpha}, (b m)^{-2/(d+alpha)}}.
```

The two scales have clear meanings:

- insufficient reliability mass, even with unlimited dictionary width; and
- joint location/reliability quantization under finite width.

The proof keeps selected mass and uses both packing and covering of the actual acquired location law. I find the argument persuasive under the stated global estimates.

### 9.3 Mixed dimensions

The finite-mixture theorem is stronger than merely stating that different strata are present. It optimizes their selected masses jointly under

```text
s_j <= b lambda_j,
Σ s_j = 1,
```

and allocates finite dictionaries to each positive-mass component. Every term retains the actual selected mass `s_j`; no stratum is renormalized to probability one without paying for it.

This theorem is valuable. The paper should give one explicit numerical example showing a phase transition in the minimizing mass allocation, rather than leaving the coupled formula entirely abstract.

### 9.4 Acquired zero-loss atom

The zero-risk threshold is correct:

```text
b lambda >= 1
```

permits selection entirely from the acquired atom. Below threshold a positive amount of the remainder must be selected. Relative order changes the lower and upper threshold by fixed multiplicative factors; exact matching recovers the exact physical threshold.

This is a clean illustration of why relative order, rather than absolute perturbation, is the appropriate singular stability notion.

---

## 10. Raw realizations

### 10.1 Paid gate interface

The two-port gate/productive interface correctly charges a strictly positive gate floor. With gate success bounded above at the lower witness and bounded below for the upper construction, the effort constants are

```text
kappa_- = 1 + 1/p_1,
kappa_+ = 1 + 1/p_0.
```

Both mandatory physical ports are visited, so two live roles are required. This role lower is based on incompatible physical command domains, not duplicated action names.

### 10.2 Classical transitive-group realization

A witness whose hidden symbol weights remain within fixed componentwise factors of uniform produces, after any selected group element, a full joint report–audit law relatively ordered around the uniform comparison law. A common near-uniform group randomization, independent of the hidden current symbol, produces the corresponding upper order.

The independence condition is essential and correctly stated. Marginal command frequencies alone would not justify uniformization if the command were correlated with the current hidden input.

The binary marked example realizes regular, stratified, and atomic acquired laws, including changing task-matrix rank.

### 10.3 Quantum Weyl realization

Weyl averaging sends every density matrix to the maximally mixed state. Relative Loewner order around that state therefore transfers through any positive report–audit instrument.

The displayed qubit instrument has noncommuting effects and actual pure/full-rank posterior strata. The lower witness itself remains relatively bounded around the maximally mixed state; the rank claim concerns post-report states and task strata. The manuscript states this distinction honestly.

These are valid realizations of the sufficient theorem. Their external significance is limited by their engineered randomization structure and post-command audit. A natural application in which the balancing command is not designed into the experiment would strengthen the paper materially.

---

## 11. Effective implementation, simulation, and calibration

### 11.1 Numerical implementation

The numerical proposition correctly restores the physical budget after acceptance rounding. It modifies the designed cap so the worst-case conditional hazard remains `1/b`, then charges:

- acceptance error;
- design/integration suboptimality;
- decoder approximation;
- whole-attempt physical and arithmetic time;
- program constants; and
- scratch space.

The stopped decoder perturbation enters once through an `L^2` triangle inequality rather than being multiplied by waiting time.

### 11.2 Effective upper

The effective corollary explicitly adds:

- finite physical partitions;
- certified integration;
- effective compact dictionary nets;
- finite readout approximation;
- actual report-law domination; and
- strict hazard and loss margins.

This is the right separation from Borel existence. The resulting search may still be exhaustive and is not a practical synthesis-complexity theorem.

### 11.3 Causal morphisms

The simulator state accounting is now role-aware:

- continuing simulator states multiply target live roles;
- sufficient terminal export classes multiply output roles;
- state stopping adds the two role counts;
- event stopping takes their maximum.

Complete stopped scored-law total variation controls bounded risk, but not unbounded expected duration. Separate cost or killed-potential certificates remain necessary. This is correct.

### 11.4 Same-task joint law

The core loss, erased early sign, and inaccessible calibration sign are combined in one physical task. Their lower bounds hold simultaneously under compatible pre-audit laws, rather than being added from unrelated least-favorable models.

The upper state counts are stated as sufficient, not minimal. This is an honest selected multiresource law.

### 11.5 Finite pilot

The pilot proposition correctly observes that a high-confidence certificate does not imply robust almost-sure termination. A false certificate may select an acceptance set of zero actual mass. The deterministic guard and first-attempt fallback repair this.

The result is restricted to a fixed independent command sampler whose deployment draws are independent of the hidden current input. It should not be described as unknown-kernel learning.

---

## 12. Pipeline and reproducibility assessment

The source and artifact separation is clear:

```text
ordinary source: 29de5433c2c4f45d5174a87a8588fd3a24d3f84a
artifact commit:  fcdb32640e4bb69922f07233fa6148bfc9b13165
referee head:     8da12b07fbed64e13bb4bb42bfc73fc56c85d37a
```

The final referee-ready commit adds review-entry and verification evidence without changing the mathematical source or built PDFs.

The local clean rebuild and finite checks pass. The separate GitHub workflow initially remained queued at the time of publication and was therefore correctly excluded from the package’s success claims. It has since completed successfully. A successor response should record both observations with their timestamps rather than silently rewriting the older receipt.

The evidence is unusually careful about limitations. It repeatedly states that:

- finite checks do not prove continuum theorems;
- PDF reconstruction does not establish novelty;
- Git object identity does not re-referee inherited mathematics; and
- referee-ready does not mean accepted.

I agree with those boundaries.

---

## 13. Literature positioning

The current native bibliography contains only eight entries. It covers trimmed quantization, Blackwell comparison, predictive states/transducers, private quantum channels, and quantum sufficiency. That is too narrow for the central paid-stopping mechanism.

At minimum, the revision should compare the following primary works.

### 13.1 Rejection sampling and sampling–covering duality

Liu and Verdú study sequential rejection sampling under moment constraints, distinguish causal and noncausal sampling costs, and use an optimization duality between sampling and covering. R59’s profile also combines a proposal density cap, stopping cost, and covering/quantization. The differences are substantial—R59 has a marked squared task, finite output width, actual-history model uncertainty, and finite-state role accounting—but the conceptual overlap is direct.

### 13.2 Causal rejection samplers for channel simulation

Goc and Flamich derive runtime and code-length lower bounds for causal rejection samplers and characterize tight quantities for channel simulation. R59’s common upper is also a causal rejection construction with a conditional hazard. It should explain why its profile is a task-risk variational object rather than a channel-simulation divergence, and why its converse uses one actual experiment witness rather than a universal proposal/target divergence.

### 13.3 Experiment order under endogenous stopping

Li introduces stopping and decision orders for binary experiments when the number of observations depends on realized evidence and characterizes them through directed Kullback–Leibler divergences. R59’s task order is local, unnormalized, and affine-square; its stopping rule has a paid finite-output geometry. The two theories are not equivalent, but the comparison is indispensable because both connect experiment order to endogenous acquisition cost.

### 13.4 Broader comparison questions

The paper should also state explicitly that its matrix-measure order is not:

- Blackwell order over all decision problems;
- a Le Cam deficiency characterization;
- a general quantum statistical morphism criterion;
- a necessary causal balancing condition; or
- a divergence characterization of expected sampling cost.

A careful comparison would strengthen, rather than weaken, the novelty claim by isolating what is genuinely new: the combination of actual-history lower certification, finite dictionary geometry, full-report task order, live/output role accounting, and singular acquired strata.

---

## 14. Why the present paper does not meet the top-four bar

### 14.1 The theorem is sufficient rather than intrinsic

The central result starts from certificates which already encode much of the desired comparison:

- one all-competitor actual witness;
- full-report rowwise mass and task inequalities;
- all-strategy effort and occupation bounds;
- one all-model common acquisition program;
- full conditional upper mass and task inequalities;
- finite export multiplicity; and
- live-role counts.

The theorem then transfers these certificates sharply into resource-risk bounds. This is valuable, but it does not explain when a general causal experiment admits such certificates in intrinsic terms.

### 14.2 The lower and upper witnesses are externally supplied

The theory does not construct the actual lower witness or the common upper program from the original family. The classical and quantum examples do so by transitive group or Weyl randomization, but those are structured realization mechanisms.

A near-necessary criterion, separation theorem, or dual obstruction for existence of a common construction would change the conceptual status of the result.

### 14.3 Natural consequences remain limited

The raw examples are mathematically valid, but they are designed to verify the theorem. The paper does not yet solve a recognized difficult problem in:

- selective prediction under costly observation;
- robust sequential design;
- finite-memory POMDPs;
- causal coding;
- controlled quantum sensing; or
- simulator-memory complexity.

The complete companion contains a nonintervening directional sensing result, but R59 correctly treats it as inherited and separate. A new natural application derived from the affine theorem would strengthen the top-four case.

### 14.4 Computational optimality is not closed

The effective upper is finite but potentially exhaustive. There are no matching lower bounds for:

- program description;
- temporary workspace;
- arithmetic time;
- calibration sample complexity beyond the fixed sampler;
- simulator state; or
- physical elapsed time.

Persistent labels alone are not total computational complexity.

### 14.5 The title remains broader than the proved classification

The title suggests foundations for acquired geometry and causal resource transfer generally. The native theorem proves a sophisticated transfer result for an explicitly certified affine task-order class. The scope audit is honest, but the title and abstract should signal more clearly that this is a sufficient task-order theory rather than a universal classification.

---

## 15. Major revision requests

### 15.1 Add a direct causal-sampling literature comparison

Add theorem-level comparisons with Liu–Verdú, Goc–Flamich, and Li. Compare:

- proposal-density caps;
- expected attempts;
- causal versus noncausal selection;
- output-width or code-length resources;
- decision order versus task-matrix order;
- exact simulation versus risk transfer; and
- divergence-based versus acquired-geometry profiles.

### 15.2 Isolate the genuine new invariant

State explicitly whether the proposed central object is:

- the profile `Q_m(b)`;
- the pair of lower/upper task-order certificates;
- the actual-history accepted comparison measure;
- the matrix task order; or
- the full theorem combining these objects.

The profile alone is classical in spirit. The strongest novelty appears to be the all-strategy actual-history lower plus the common finite-role upper under one affine order.

### 15.3 Provide a near-necessity result

A meaningful next step would be one of:

- a dual obstruction to any common acquisition program;
- a necessary task-order inequality for all programs in a broad finite experiment class;
- a minimax separation theorem yielding a witness model and task measure; or
- an intrinsic characterization in finite alphabets.

Without such a result, the theorem remains certificate-driven.

### 15.4 Add a natural application not designed around transitive randomization

The strongest application would start from a recognized problem and derive the certificates rather than building an experiment to fit them. Candidates include costly selective prediction, controlled sensing with post-command audits, finite-memory causal coding, or a finite-dimensional quantum decision problem with a pre-existing operational interpretation.

### 15.5 Give an explicit mixed-strata phase diagram

For at least two components with different `(d_j,alpha_j,lambda_j)`, solve or plot the selected-mass minimization in representative regimes. This would make the mixed-dimensional theorem independently useful.

### 15.6 Move the relative/absolute distinction to the headline

The sharp distinction between relative task order and acquisition-amplified absolute defect is conceptually central. The abstract should state that a fixed relative distortion preserves zero tasks and all scales, whereas a fixed additive task error can be amplified linearly by expected acquisition count.

### 15.7 Clarify necessity levels

For every order statement, label whether it is:

- necessary and sufficient for localized affine-square tests;
- sufficient for the squared-prediction theorem;
- sufficient for one common construction; or
- a realization-specific verifier.

This hierarchy currently appears in the prose but should be visible in the main theorem architecture.

### 15.8 Tighten the quotient discussion

The quotient theorem is useful but somewhat orthogonal to the transfer theorem, whose upper stores no quotient. Explain precisely which later statement actually requires the quotient, and avoid allowing the appendix to suggest a common unknown-model posterior representation which is not proved.

### 15.9 Update the independent-run evidence

The package correctly recorded the workflow as queued at final observation. The run has since succeeded. Add a new append-only observation rather than editing the historical receipt, and retain the distinction between local clean rebuild and hosted independent workflow.

### 15.10 Add a complete assumption-flow figure

A one-page diagram should separate:

```text
raw kernels
 -> full-report task order
 -> actual-history lower witness
 -> common upper program
 -> profile transfer
 -> geometric mass/cover laws
 -> effective implementation.
```

The current theorem map is useful but still requires significant reconstruction by the reader.

### 15.11 Distinguish post-command from nonintervening tasks more prominently

The classical and quantum native realizations concern the state after a balancing command. The companion’s directional sensing concerns a target not changed by the sensing action. This distinction should be stated in each realization theorem title or opening sentence.

### 15.12 Keep journal claims proportional to proved scope

The paper should not describe the theorem as a classification of causal acquisition. It is a sharp transfer theorem for a broad, carefully certified sufficient class.

---

## 16. Technical comments

1. In the theorem statement, identify `A_N,E_N` as suprema over the entire feasible competing class, not properties of a fixed program.
2. State in the main theorem that `theta_*` is fixed before the competing program is selected.
3. Retain the full-current-report condition in every summary; mark-only moments are insufficient.
4. State explicitly that the comparison row may depend on the actual history and chosen command, while its mark law remains the common `nu`.
5. Keep the case `t_N=0` separate; do not write `Q_m(infinity)`.
6. In the upper, retain the whole-attempt cost condition rather than a cost conditional on acceptance.
7. Keep the first-attempt alternative when `beta_N<1`; the cap is otherwise infeasible.
8. In exact event stopping, make clear that live/output reuse is a semantic feature of the public terminal event, not a hidden continuing bit.
9. In state stopping, make clear that terminal labels have no command rows and are globally typed by the fixed halt map.
10. Preserve the physical command-intersection certificate; action-name counting is not invariant.
11. State whether `D_0` counts distinct exported values or command choices. The proof needs the former.
12. In the matrix-order proposition, emphasize that rational-vector testing detects strict failure but is not by itself an efficient numerical algorithm.
13. In the singular theorem, specify that kernel equality is an almost-everywhere statement relative to the common scalar dominator.
14. Do not describe the pseudoinverse as uniformly bounded.
15. In the continuity proposition, retain the actual-mass weight `min(p,q)`; an unweighted posterior bound is false near likelihood zeros.
16. In the regular geometry theorem, make the bounded task-carrier constant visible in the global constants.
17. In the mixed-strata theorem, state explicitly that a component label need not be observed; the implemented density is the Radon–Nikodym derivative on actual marked coordinates.
18. For the atom theorem with `m=1`, retain the separate upper statement; one center cannot simultaneously be reserved and optimized.
19. In the classical upper, keep hidden-input independence of command randomization as a physical implementation assumption.
20. In the quantum lower, do not describe relative order around the maximally mixed state as permitting a pure lower witness.
21. In the qubit example, retain the distinction between post-report state rank and task-matrix rank.
22. In the numerical proposition, report both the acceptance error and decoder error in any simplified statement.
23. In simulator composition, complete scored stopping time and premature commitment must be part of the compared law.
24. Do not infer expected duration from total variation of terminal outputs.
25. In the joint theorem, retain that the state counts are sufficient rather than minimal.
26. In the pilot proposition, state the tighter-band condition whenever quoting the small rejection-risk bound.
27. Record the actual cost of the deterministic guard and its attempt-index memory.
28. Update the bibliography with DOI/arXiv identifiers and publication status for the direct causal-sampling neighbors.
29. The workflow success occurred after the frozen verification observation; preserve both timestamps.
30. The companion is complete mathematical ancestry, not an automatically re-refereed 37-page appendix.

---

## 17. Changes that could alter the top-four judgment

The following would materially change my assessment:

1. **An intrinsic or near-necessary characterization** of when a causal family admits the lower witness and common upper construction.
2. **A separation/duality theorem** producing a witness or obstruction from primitive finite experiments.
3. **A recognized natural application** whose unresolved finite-resource curve is solved by the affine theorem.
4. **A general state-dependent or unknown-kernel extension** with all-strategy lower and common-program upper.
5. **A matched computational-resource theorem** including program bits, workspace, precision, time, or simulator memory.
6. **A sharper connection to endogenous-stopping experiment order** which reveals a new order or divergence rather than only a sufficient comparison.
7. **A necessity theorem for singular task ranges** extending beyond the declared affine-square family.

Absent one of these advances, the paper appears better suited to a strong specialist venue than to a top-four general mathematics journal.

---

## 18. Editorial conclusion

R59 is a serious revision.

It repairs the principal R56 model-semantics defect, provides a coherent affine task-order theorem, keeps lower comparisons on actual histories, preserves selected mass and acquisition cost, separates relative order from absolute error, treats singular task ranges correctly, and accounts for live, terminal, simulator, calibration, and numerical resources with unusual care.

I found no elementary fatal flaw in the center after checking the load-bearing arguments listed above. The manuscript should not be rejected on the ground that the central proof is obviously incorrect.

The current obstacle is instead the top-four standard of breadth and external consequence. The theorem is certificate-driven, the closest causal-sampling literature is not yet adequately integrated, the raw examples are structured around available balancing symmetries, and the work does not yet resolve a widely recognized natural problem or provide an intrinsic classification.

My recommendation is therefore:

- **top-four general mathematics:** reject in the present form;
- **strong specialist journal:** potentially favorable after a focused major revision; and
- **mathematical status:** substantial, technically credible under the stated hypotheses, and deserving of further independent scrutiny.
