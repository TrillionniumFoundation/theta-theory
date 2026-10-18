# Independent Round-2 Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

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
**Earlier R59 external report:** commit `b83df25572188d512e7d042311bf3db637c28f47`, report blob `0f25939c7028ef09519f82ca67eef92852444985`  
**This review branch:** `review/general-theta-restart-r59-causal-task-order-external-top4-referee-r59-round2-2026-10-15`  
**Date:** 15 October 2026

This is a second, independently written mathematical assessment of the same immutable R59 referee object. No newer completed `General Theta Foundations I` referee-ready branch was present in a complete two-page branch enumeration at the time of review. The earlier R59 report is preserved unchanged and is treated as part of the review history, not as a substitute for the source audit below.

This report is author-requested and repository-deposited. It is not a commissioned editorial decision of a named journal, a proof-assistant certificate, a priority certificate, or a claim of acceptance.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**.

My independent reading reaches essentially the same high-level conclusion as the first R59 report, but for reasons established again from the mathematical source. R59 contains a coherent and nontrivial transfer theorem. It correctly separates one-witness all-strategy lower bounds from one-program all-model upper bounds; compares stopped experiments on actual pre-call occupation rather than on a fictitious comparison execution; distinguishes relative task order from additive defects; and repairs the earlier conflation of live routing states with terminal output states by defining separate event-stopped and state-stopped interfaces.

The main theorem is not merely a repackaged static quantization statement. Its lower direction constructs a finite accepted comparison measure from every competing program while keeping the competitor's actual history law. Its upper direction uses one parameter-independent acquisition program, a conditional acceptance hazard valid after every surviving history, and a predictable sum of whole-attempt costs. The proof does not use a minimax interchange, does not assume that the reference experiment is an operating model, and does not require the competing policy to terminate under that reference experiment.

The relative-order extension is mathematically meaningful. Two-sided positive order of unnormalized task measures preserves exact zero-task directions and changes only constants and effective budgets. Additive one-call defects, by contrast, accumulate under actual occupation and can be amplified by selection. The matrix-measure criterion and its measurable changing-rank formulation capture this distinction without inverting small eigenvalues uniformly.

In the load-bearing arguments checked, I did not find an elementary gap invalidating:

- attainment and monotonicity of the marked trimmed profile;
- the actual-history comparison-measure construction;
- the all-strategy lower from one fixed operating witness;
- the common conditional-hazard upper across all models;
- the separate event-stopped and state-stopped role counts;
- the exact checkpoint, event-stopped, and state-stopped specializations;
- the scale-uniform relative-order transfer;
- the positive matrix-measure order criterion;
- the measurable common-range characterization through rank changes;
- the raw positive-instrument continuity inequalities through likelihood zeros;
- the non-power sublevel bounds;
- the regular marked profile with its reliability and location scales;
- the finite mixed-dimensional profile retaining selected component masses;
- the acquired zero-loss atom threshold;
- the killed-potential occupation estimate;
- the transitive classical realization;
- the noncommuting quantum Weyl realization;
- the effective finite-description upper under its additional hypotheses;
- the simulator composition with distinct continuing and terminal state factors;
- the same-task core, erased-sign, and calibration construction;
- the guarded finite command-calibration proposition; or
- the compact-exhausted predictive quotient construction at the stated fixed-law scope.

The negative top-four recommendation concerns the **intrinsic reach, external mathematical consequence, novelty relative to neighboring rejection-sampling and experiment-comparison theories, and the breadth suggested by the title**, rather than a fatal proof defect.

The central theorem remains a powerful sufficient-class theorem whose decisive hypotheses are externally supplied certificates: one full-report order witness valid for every competing command and reached history, one all-program effort lower, uniform actual-occupation defect bounds, and one common upper program valid on every surviving history in every model. These assumptions are verified in carefully designed positive classical and quantum families, but the manuscript does not establish an intrinsic, near-necessary characterization of the causal experiments for which such witnesses and constructions exist.

The geometric profile is a marked trimmed population-quantization functional with classical antecedents. The new content lies in its causal transfer, resource typing, and singular task-order stability. That synthesis is technically valuable, but the manuscript has not yet shown a consequence for a widely recognized difficult natural problem commensurate with a leading general-mathematics journal.

For a strong specialist journal in mathematical statistics, information theory, stochastic control, sequential decision theory, quantization, selective prediction, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object and review status

A fresh branch enumeration found the following latest completed referee-ready revision:

```text
referee-ready/general-theta-restart-r59-causal-task-order-2026-10-14
```

The continuation page was empty. The branch still points to

```text
8da12b07fbed64e13bb4bb42bfc73fc56c85d37a.
```

The existing first R59 review branch is

```text
review/general-theta-restart-r59-causal-task-order-external-top4-referee-r59-2026-10-15
```

and is one commit ahead of the same R59 head. Because the manuscript head has not changed, the present report is deliberately a **round-2 independent review**, not a claim to review a newer revision and not an update of the earlier report.

The terminal R59 evidence commit has artifact commit

```text
fcdb32640e4bb69922f07233fa6148bfc9b13165
```

as its sole parent. The ordinary source is

```text
29de5433c2c4f45d5174a87a8588fd3a24d3f84a.
```

The native article is 25 pages. The complete R58 companion is 37 pages. I treated the native article as the editorial object and used the companion to inspect inherited exact-stopping semantics, absolute-calibration theory, nonintervening sensing, and prior computation statements. The companion is not a hidden premise of the R59 transfer theorem.

The source audit included:

- `main.tex`, all eight native sections, both appendices, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, and `NOTATION_AUDIT.md`;
- the complete R56 report pinned in `inputs/review/` and the R57/R58 repair history;
- the profile, actual-history lower, common upper, task-order, geometry, realization, effective, simulator, joint-task, pilot, quotient, and boundary arguments;
- the build receipt, publication receipt, clean rebuild record, final read-only verification, and referee entry; and
- the earlier R59 report, read after the source audit to identify overlap and unresolved external-positioning issues.

I did not re-prove all v1--v96 historical mathematics or all independent realization branches. The repository's own history audit correctly disclaims such a conclusion.

---

## 2. Executive description of the theorem

### 2.1 The physically acquired profile

A prepared comparison experiment supplies a genuine joint report--audit probability

```text
K_0(dx,dz)
```

with report marginal `nu`. The task coordinates are derived by disintegration:

```text
f(x) = E_0[Z | x],
w(x) = E_0[||Z-f(x)||^2 | x].
```

For a finite output dictionary `C`, the conditional squared task is

```text
w(x) + dist(f(x),C)^2.
```

The profile is

```text
Q_m(b)
 = min ∫ [w+dist(f,C)^2] h dnu,
```

subject to

```text
|C| <= m,   0 <= h <= b,   ∫h dnu = 1.
```

This is a marked and renormalized trimmed-quantization functional. The cap `b` retains the physical price of rejected reports: a selected probability law obtained from a proposal law with expected-attempt budget `b` cannot have proposal density exceeding `b`. The residual mark `w` prevents the argument from replacing a report--audit task by location quantization alone.

The profile itself is classical in spirit. The manuscript correctly cites trimmed `k`-means and does not claim invention of the variational object. Its claimed contribution is the two-sided causal resource transfer to this profile.

### 2.2 Quantifiers in the lower and upper

The lower fixes one operating model `theta_*`, independently of the competing program. At every actually reached productive prehistory and each chosen legal command, it compares the **full current report--audit row** with a reference row. It also requires:

```text
E_* C_tau >= kappa_- E_* A_tau
```

for every competitor and actual-occupation bounds on accumulated mass and task defects.

The upper is logically separate. One parameter-independent attempt program must work after every surviving history in every model. It has a conditional expected whole-attempt cost bounded by `kappa_+`, a lower mass certificate, an upper task certificate, a finite live-role count, and a finite export-width factor.

This is a valid robust architecture:

- one actual witness lower-bounds `inf_program sup_theta`;
- one common program upper-bounds `inf_program sup_theta`;
- the lower and upper need not use the same operating model;
- the comparison experiment need not belong to the model class; and
- there is no exchange of minimization and maximization.

### 2.3 Central inequalities

With

```text
b_- = N/kappa_-,
b_+ = N/kappa_+,
t_N = (1-A_N)_+/u_-,
```

and the interface-dependent widths `m_-(M),m_+(M)`, the lower is

```text
R_i^Theta(N,M)
 >= [l_- t_N Q_{m_-(M)}(b_-/t_N)-E_N]_+.
```

For

```text
beta_N = l_+ b_+/(1+b_+a_+) >= 1,
```

the upper is

```text
R_i^Theta(N,M)
 <= [u_+(1+b_+a_+)/l_+] Q_{m_+(M)}(beta_N)+b_+e_+.
```

When `beta_N<1`, the first-attempt construction gives the stated cap-one upper. These directions and constants are internally consistent.

---

## 3. Independent audit of the lower proof

### 3.1 Why the actual-history construction matters

A stopped policy that terminates under the operating experiment may fail to terminate, or may have a different cost, under a substituted comparison experiment. Running the policy under the comparison law would therefore be unjustified.

R59 avoids this. It preserves the actual distribution of every pre-call history under `theta_*` and replaces only the current productive row inside a nonnegative occupation integral. This is the correct mechanism.

For every terminal decoder value `c`, the proof defines a finite measure `xi_c` on the comparison mark space. The sum `xi` satisfies

```text
xi <= (E_* A_tau) nu <= b_- nu.
```

The mass of the analogous actual accepted measure is exactly one because commitment occurs exactly once almost surely. Summing the lower mass inequalities gives

```text
1 <= u_- xi(X)+A_N.
```

The task inequalities give

```text
actual risk >= l_- Σ_c ∫d_c dxi_c - E_N.
```

The proof conditions the reference task moments on the full current report, not merely on the compressed mark. This is necessary: an additional visible coordinate can reveal the audit even when the mark marginal is unchanged.

### 3.2 Normalization and cap

Let `s=xi(X)`. When `t_N>0`, the mass inequality gives `s>=t_N`. Scaling

```text
xi'=(t_N/s)xi
```

preserves the domination `xi'<=b_-nu` and gives mass `t_N`. Thus

```text
h=(d xi'/dnu)/t_N
```

has unit mass and cap `b_-/t_N`.

Because the loss is nonnegative and the competitor's dictionary has the appropriate interface-dependent width,

```text
Σ_c ∫d_c dxi_c
 >= t_N Q_{m_-(M)}(b_-/t_N).
```

This establishes the lower without a minimax swap. The zero case `t_N=0` is also stated correctly: no meaningless evaluation of the profile at an infinite cap is required.

### 3.3 Width converse

A checkpoint or event-stopped observer has at most one decoder value per retained label. A state-stopped observer with at least `B_0` actually reached live labels has at most `M-B_0` terminal labels because the halt map is intrinsic and live and terminal types are disjoint.

The physical live-state certificate is not based on command names. It uses intersections of physically legal command sets across mandatory contexts. Stateless renaming or recoding does not evade the bound. This repairs the earlier inference criticized in the R56 report.

I find the lower proof correct under its stated certificates.

---

## 4. Independent audit of the common upper

### 4.1 Conditional hazard

Choose an attained profile optimizer `(C,h)` at cap

```text
beta_N=l_+b_+/(1+b_+a_+).
```

The common attempt program accepts the virtual mark with probability `h/beta_N`. Since `h<=beta_N`, this is a legal Borel probability.

The lower mass certificate for the upper program gives, conditionally on every surviving history,

```text
P(accept next attempt)
 >= l_+/beta_N-a_+
 = 1/b_+.
```

This is a history-uniform hazard. Induction gives a geometric survival bound even if rejection changes the hidden physical state arbitrarily. No renewal or independence between attempts is needed.

### 4.2 Cost

Every begun attempt has conditional expected whole-attempt cost at most `kappa_+`. The sum of probabilities that the successive attempts are begun is at most `b_+`. Predictable summation therefore gives actual expected cost at most

```text
kappa_+ b_+ = N.
```

The proof does not use bounded task total variation to infer an unbounded time or cost statement.

### 4.3 Loss

The one-attempt unnormalized accepted loss is bounded by

```text
u_+ Q/beta_N + e_+.
```

Summing on disjoint terminal events with the same survival bound gives the stated upper. The export factor is charged by enlarging the finite output dictionary. Live roles and terminal roles are then packed according to the declared stopping interface.

When `beta_N<1`, committing on the first attempt and using the cap-one profile is valid because `b_+>=1` already implies `N>=kappa_+`.

I find the upper proof correct under its stated all-history and all-model construction hypotheses.

---

## 5. Stopping semantics and exact resource laws

The manuscript now defines two distinct autonomous interfaces.

### 5.1 Event stopping

A post-report kernel emits both a retained label and a public terminal event. On a terminal branch, no next command is executed. A label may therefore be used as a live routing state on one path and as a terminal decoder value on another. The correct packing count is

```text
max(live roles, output roles).
```

This reuse does not smuggle a continuing mode bit into the machine because the terminal event ends computation.

### 5.2 State stopping

A fixed map on the persistent label determines whether the state is terminal. Terminal labels have no command rows and are globally disjoint from live labels. The correct count is

```text
live roles + output roles.
```

### 5.3 Exact formulas

Under exact matching, identity exports, equal effort constants, and a sharp live lower `B_0=B`, the proof correctly obtains:

```text
R_cp(N,m)=Q_m(N/kappa),
R_ev(N,M)=Q_M(N/kappa)       for M>=B,
R_st(N,B+m)=Q_m(N/kappa).
```

The subtraction by `B` belongs only to state stopping. The prior universal subtraction was mathematically invalid; R59's typed repair is sound.

---

## 6. Relative order versus additive defect

This distinction is one of the strongest conceptual parts of the paper.

### 6.1 Relative task order

When all additive defects vanish, fixed factors `l_-,u_-,l_+,u_+` change effective caps and multiply risk constants:

```text
(l_-/u_-) Q_{m_-}(u_-b_-)
 <= R
 <= (u_+/l_+) Q_{m_+}(l_+b_+).
```

The factors need not approach one. In particular, if the comparison task is exactly zero on a report stratum, two-sided positive order forces the operating task to remain zero there.

### 6.2 Additive defects

A fixed absolute one-call task defect can be magnified by selective acquisition. The boundary construction with a report set of proposal mass `1/b` produces a stopped-risk discrepancy `b e` from one-call defect `e`.

This example confirms that relative order and absolute proximity are not interchangeable near a zero-loss stratum. The all-scale result is therefore not a consequence of a small total-variation or bounded-loss perturbation alone.

### 6.3 Actual occupation

Nonuniform defects are integrated along the actual pre-call occupation. The killed-potential lemma is a valid way to replace worst-row bounds with actual preparation and residence information. It uses deterministic truncation and monotone convergence, not an optional-stopping theorem with an unverified uniform-integrability condition.

---

## 7. Raw matrix order and singular ranges

### 7.1 Localized affine-square order

For a full report--audit law `P`, the positive matrix measure

```text
J_P(D)=∫_{D×H}(1,z)(1,z)^T dP
```

encodes every localized affine-square test. Two-sided matrix-measure order is exactly equivalent to two-sided inequalities for all such tests. Rational affine vectors suffice because quadratic forms are continuous.

Taking the constant affine coordinate gives report-mass order. Summing the coordinate squares for `z-r` gives squared-task order for finite-image readouts, and monotone approximation extends from simple selectors to arbitrary Borel acceptance probabilities.

This is an exact characterization for the declared affine-square test family. It is a sufficient primitive criterion for the narrower main task; it is not claimed necessary for every possible causal balancing construction.

### 7.2 Changing rank

With a common scalar dominating measure, the order is equivalent almost everywhere to:

- equality of the kernels of the two positive matrix densities; and
- spectral bounds on their common measurable range after congruence by the Moore--Penrose inverse square root.

The proof uses the pseudoinverse pointwise and does not take a uniform inverse norm. Rank may change and positive eigenvalues may approach zero. The result correctly preserves null task directions.

### 7.3 Positive instruments

Positive classical or quantum instruments carry input order to output measure order. Componentwise relative command-weight bounds similarly carry nominal averaged laws to actual averaged laws. Lower and upper factors multiply under successive relative comparisons; they do not create an additive acquisition-amplified floor.

These arguments are finite-dimensional and correctly avoid normalization by zero report probabilities.

---

## 8. Geometry of the acquired profile

### 8.1 Non-power sublevel bound

The sublevel functional `Omega_m(r)` gives a clean finite-scale statement:

```text
sup_r r^2[1-b Omega_m(r)]_+
 <= Q_m(b)
 <= inf{r^2:Omega_m(r)>=1/b}.
```

The proof keeps the actual mass and density cap. A cover of a formal reachable set alone would not imply either inequality.

### 8.2 Regular marked law

For the actual pushforward law of `(f,sqrt(w))`, the global rectangle condition

```text
c r^d s^alpha
 <= sigma(B(x,r)×[0,s])
 <= C r^d s^alpha
```

leads to

```text
Q_m(b)
 asymp max{b^{-2/alpha},(bm)^{-2/(d+alpha)}}.
```

The two terms have different meanings:

- the first is the price of acquiring sufficiently reliable task mass;
- the second couples reliable mass with a finite spatial dictionary.

The lower and upper retain actual acquired mass. The proof permits singular noninteger location dimension.

### 8.3 Mixed-dimensional law

For a finite mixture, the theorem optimizes over selected component masses `s_j` subject to `s_j<=b lambda_j`. The lower keeps the full dictionary width `m` on every component; the upper allocates a fixed fraction of the dictionary to each positive component and combines the component-selected measures by a Radon--Nikodym density with respect to the actual mixture.

This remains valid even when component labels are not observed. The construction is analytical on the actual marked law, not a latent component selector supplied to the observer.

### 8.4 Acquired atom

A zero-loss atom of mass `lambda` gives exact zero profile when `b lambda>=1`. Below threshold, at least `1-b lambda` selected mass must come from the remainder. The lower and upper correctly retain that amount and the remaining dictionary width.

Under relative transfer, the impossible and attainable thresholds differ by the lower and upper order constants. Only exact matching recovers the numerical threshold `N=kappa/lambda`.

I find the geometric arguments sound at their stated finite-component and global-mass scope.

---

## 9. Classical and quantum raw realizations

### 9.1 Paid gate

The gate and productive ports are physically distinct and both cost one. Every productive call requires a gate success. With witness success at most `p_1` and common-program success at least `p_0`, the proof obtains

```text
kappa_- = 1+1/p_1,
kappa_+ = 1+1/p_0.
```

The two physically incompatible pre-call contexts require two live roles. Even `p_0=1` costs two calls.

### 9.2 Classical transitive group

A near-uniform witness input gives commandwise lower order relative to the genuinely prepared uniform reference law. A near-uniform command distribution independent of the hidden current symbol gives an all-input upper order after averaging over the transitive group.

The hidden-input independence of the current command is essential and is correctly stated as a physical implementation property. Marginal command frequencies alone would not suffice.

The binary example derives `f` and `w` from the report--audit law, supports regular, stratified, and atomic geometries, and includes an actual task-rank change.

### 9.3 Quantum Weyl realization

The witness state is relatively ordered around the maximally mixed state. Every selected Weyl conjugation preserves this order. Near-uniform Weyl weights independently of the current input put the averaged state between fixed multiples of the exact twirl for every incoming state, including pure states.

A positive report--audit instrument then transfers this order to the full observable task law. The example with noncommuting qubit effects has actual pure and full-rank posterior strata and a changing-rank task measure. No common eigenbasis or normalized-filter contraction is used.

The task is explicitly a post-command audit. It is not an estimation theorem for an untouched pre-command physical state. The distinction should remain prominent.

---

## 10. Predictive quotient appendix

The appendix does more than assume a Borel quotient.

A countable determining response map `q` is continuous on each compact positive-evidence patch `C_n`. Therefore each image `q(C_n)` is compact and the realized image is a countable union of compact sets, hence Borel.

The proof constructs a Borel section by choosing the first compact patch containing the image point and then a nested sequence of compact cells of vanishing diameter whose images contain that point. This is a legitimate compact-selection construction.

Continuation closure gives equality of the next-report law and almost-sure equality of the updated quotient under compared representatives. Impossible reports are completed arbitrarily rather than being assigned a fictitious canonical posterior.

The result is intentionally fixed-law and sufficient. A common executable quotient for an arbitrary merely Borel unknown-model family is not established. I regard this as a correct and useful appendix, but not as a general classification theorem for predictive-state realizability.

A future revision should cite a standard measurable-selection result alongside the explicit construction, both to shorten the proof and to make clear which parts are classical descriptive-set theory and which are specific to the positive-evidence setup.

---

## 11. Numerical implementation, simulation, and calibration

### 11.1 Numerical implementation

Acceptance rounding is incorporated into the hazard denominator, so the actual expected cost is restored rather than asserted from the ideal program. One-attempt task error is summed over actual attempts. Decoder error is added in stopped root-mean-square loss and is not multiplied by the waiting time.

The stated program, scratch, and arithmetic counts are upper accounts for a specified implementation, not universal optimal lower bounds.

### 11.2 Effective finite-description upper

The effective corollary adds the necessary hypotheses absent from Borel existence:

- effective compactness and dictionary nets;
- finite physical report partitions;
- certified mass and task integration;
- actual-report domination by the reference law;
- finite classifiers and their costs; and
- readout approximation.

Strict hazard and loss margins allow finite enumeration to terminate. The theorem does not claim efficient global synthesis.

### 11.3 Simulator composition

Continuing simulator state and terminal sufficient export classes are counted separately. A target with `ell` live and `t` terminal roles lifts to

```text
ell K+tE
```

state-stopped labels or

```text
max(ell K,tE)
```

event-stopped labels.

Complete stopped scored-law deficiencies add under composition. Raw-call count and physical time still require separate certificates because they are unbounded path functionals. A reverse risk inequality requires a reverse simulator or an independent lower witness.

### 11.4 Same-task lower

The core witness, erased fair sign, and inaccessible fixed calibration sign are placed in one experiment with compatible pre-audit laws. The three losses can therefore be added before taking the worst model. This avoids the invalid practice of summing minimax lower bounds proved under incompatible alternatives.

The early sign deficiency is an attained property of a real interface, not an arbitrary permitted error tolerance.

### 11.5 Finite pilot

The calibration proposition correctly distinguishes high-probability certification from robust termination. It charges:

- physical calibration draws;
- count-vector memory;
- a safe fallback;
- a deterministic attempt guard;
- the guard's live-state multiplier; and
- the false-certificate and true-certificate-rejection risks.

The result is limited to one fixed independent sampler used throughout calibration and deployment. It is not arbitrary unknown-kernel learning.

---

## 12. Response to the earlier referee history

The R56 report identified a genuine resource-semantics error: a count of reached live labels did not justify subtracting those labels from terminal output width in an event-stopped machine.

R59, through the R57/R58 repair, resolves this by defining the two interfaces and reproving the packing rules. The new R59 theorem then goes beyond that repair by combining relative order and additive defects in one affine transfer statement.

The following earlier concerns are now resolved or substantially improved:

| Earlier concern | Round-2 assessment of R59 |
|---|---|
| Live/output roles conflated | Resolved by event versus state stopping. |
| Checkpoint and autonomous widths conflated | Resolved by separate width formulas and exact corollaries. |
| Lower compared a hypothetical reference execution | Resolved by actual-history row replacement. |
| Unequal effort constants hidden | Resolved by `kappa_-` and `kappa_+`. |
| Report balance used without task moments | Resolved by full-report task order and an explicit failure witness. |
| Relative and additive errors conflated | Resolved; the selection-amplification boundary is explicit. |
| Calibration confidence used as termination | Resolved for a fixed sampler by fallback and guard. |
| Effective implementation hidden inside Borel existence | Resolved in scope by a separate effective corollary. |
| Intrinsic necessity of the sufficient class | Still open. |
| Broad natural application with external impact | Still open. |
| Matched total computational-resource region | Still open. |

---

## 13. Literature positioning

The native bibliography appropriately cites:

- Blackwell comparison of experiments;
- trimmed `k`-means;
- causal-state and input--output predictive representations;
- finite quantum randomization; and
- quantum statistical sufficiency.

It does not yet adequately position the paid causal selection mechanism against the closest sampling and endogenous-stopping literature.

At minimum, a revision should compare the following primary works at theorem level.

### 13.1 Liu--Verdú, rejection sampling under moment constraints

Jingbo Liu and Sergio Verdú, *Rejection Sampling and Noncausal Sampling under Moment Constraints*, ISIT 2018, DOI `10.1109/ISIT.2018.8437857`.

That work studies sequential selection of a proposal sample to realize a target distribution, moment costs of the selected index, the effect of causality, and a sampling--covering duality. R59 differs by adding a marked squared task, finite output width, an unknown-model witness/common-construction split, and finite-state stopping semantics. Nonetheless the density cap and expected-attempt interpretation belong in the same comparison paragraph.

### 13.2 Goc--Flamich, causal rejection samplers

Daniel Goc and Gergely Flamich, *On Channel Simulation with Causal Rejection Samplers*, arXiv:`2401.16579`.

That work develops lower and upper bounds for expected runtime and codelength of causal rejection samplers, including a Rényi-infinity runtime obstruction and a channel-simulation divergence. R59 studies a different task-risk and hard-label resource, but its common conditional-hazard upper and paid rejection profile should be contrasted with those channel-simulation limits.

### 13.3 Li, experiment order under endogenous stopping

Zihao Li, *The Order of Binary Experiments under Endogenous Stopping*, arXiv:`2608.19897`.

That work introduces stopping and decision dominance for binary experiments and characterizes them through directed Kullback--Leibler divergences, with an exact repeated-observation simulation theorem. R59 treats a broader nonbinary marked task but gives a sufficient affine order rather than a necessity theorem. This is a particularly important comparison because it sharply exposes what R59 does and does not classify.

These neighboring results do not appear to subsume R59's combination of finite output geometry, actual-history defect integration, event/state role accounting, singular task-matrix order, and one-witness/one-construction robust quantifiers. They do, however, narrow the reasonable novelty claim. The paper should state the distinction directly rather than rely on the absence of identical terminology.

No literature search can certify earliest priority. The repository and any revision should continue to avoid such a claim.

---

## 14. Major comments for revision

### 14.1 State the theorem class in the title-level summary

The abstract and introduction should say earlier and more compactly that the main theorem is a sufficient transfer theorem requiring:

- one commandwise full-report order witness;
- one common all-model acquisition construction;
- an all-program effort lower;
- actual-occupation defect control; and
- finite live/export roles.

The present abstract is accurate but dense enough that the strength of these certificates is easy to miss.

### 14.2 Separate the intrinsic question from the certificate theorem

The paper should formulate, as an explicit open problem, the intrinsic characterization of experiment families admitting the lower witness and common construction. This is the most important missing conceptual step.

### 14.3 Add the rejection-sampling and endogenous-stopping comparison

The three works listed above should enter the native bibliography and Section 1 comparison. The comparison should use precise coordinates: target/proposal law, causality, cost moment, output task, finite output width, model robustness, stopping semantics, and necessity versus sufficiency.

### 14.4 Explain the relationship to Blackwell order more sharply

The positive matrix order is exact for localized affine-square tests. It is not Blackwell dominance for all decision problems, nor a complete quantum sufficiency criterion. A short proposition or table should make this hierarchy explicit.

### 14.5 Distinguish static profile novelty from transfer novelty

The profile `Q_m(b)` should be introduced immediately as marked trimmed quantization with classical statistical ancestry. The new contribution is the causal transfer and resource typing. This will strengthen, rather than weaken, the novelty claim.

### 14.6 Clarify when the lower certificates are realistically verifiable

The raw classical and quantum examples verify them, but the general theorem asks for commandwise inequalities at every reached history for every competitor. The paper should discuss reusable primitive conditions beyond transitive group or Weyl averaging, or clearly identify this as the central bottleneck.

### 14.7 Promote the actual-history lemma

Lemma `lem:comparison` is arguably the conceptual center. The introduction should emphasize that the reference measure is an accepted occupation measure, not the law of a reference run. This distinction is broader than the particular profile formula.

### 14.8 Shorten the role-semantics discussion but retain both interfaces

The event/state repair is necessary, but it currently occupies substantial narrative bandwidth inherited from the earlier defect. A diagram of the two transducers could replace repeated prose while preserving the exact formulas.

### 14.9 Give one less engineered natural application

The transitive finite-channel and Weyl examples are mathematically clean but tailored to make relative order visible. A major strengthening would be a naturally occurring selective prediction, sequential sensing, or post-command quantum-control problem whose optimal finite-resource curve was not previously known.

### 14.10 Strengthen the effective result or narrow its presentation

The effective corollary establishes finite discoverability under supplied partitions, integration certificates, and nets. It is not an efficient synthesis theorem. Either derive a meaningful complexity result for a natural subclass or move the exhaustive-certification discussion out of the main narrative.

### 14.11 Keep the fixed-law scope of the quotient theorem explicit

The appendix does not produce one common quotient for an arbitrary unknown-model family. This caveat should appear in the theorem's introductory sentence, not only after the proof.

### 14.12 Update the evidence status append-only

The frozen R59 entry and final verification recorded GitHub Actions run `38562870143` as queued and did not count it as a pass. Current remote readback shows the run completed successfully for source commit `29de5433c2c4f45d5174a87a8588fd3a24d3f84a`. A successor should append a dated evidence correction. The immutable historical receipt should not be silently rewritten.

### 14.13 Reduce the scope implied by “Foundations” or supply a stronger bridge

The current theorem advances the Foundations program, but it does not classify general causal experiments. The title can remain for project continuity only if the introduction clearly identifies the present theorem as one sufficient layer in a larger program.

### 14.14 Preserve the post-command versus nonintervening distinction

The raw R59 realizations score post-command audits. The companion's nonintervening sensing theorem concerns a different task. No future revision should combine their conclusions without an explicit causal simulator or a new theorem.

### 14.15 Provide a one-page assumption/conclusion chart in the article

The repository assumption matrix is useful, but the article should not require a reader to consult repository metadata to understand which conclusions need relative order, which allow additive defects, which require effective primitives, and which are exact only under matched effort and role counts.

---

## 15. Technical comments

1. In the definition of the profile, say explicitly that repeated dictionary points are permitted when compactness is implemented through `H^m`; this is used in the attainment proof.

2. The left-continuity proof is for `b>1`. The endpoint `b=1` need not be discussed unless used, but the scope should remain explicit.

3. In Lemma `lem:comparison`, emphasize once more that the auxiliary independent uniform is current-call randomness and is not retained between calls.

4. The measure `xi` is finite because `E_*A_tau<=b_-`; cite the effort inequality at that exact point.

5. The full-report conditional moment identity is indispensable. It would be helpful to move the constant-mark/visible-bit counterexample closer to the lemma.

6. The physical live-state certificate assumes every mandatory context is visited with positive probability under the same witness. State explicitly whether “positive” may depend on the competitor; the proof only needs reachability of each context for the program being lower-bounded.

7. In the upper proof, distinguish the within-attempt random choice `J` from a persistent state. The resource table does this; one sentence in the proof would help.

8. The first-attempt branch for `beta_N<1` is correct because `b_+>=1`; state that implication inline.

9. The exact event formula uses `M>=B`. Do not suppress this feasibility condition in summaries.

10. The matrix-measure criterion is exact for affine-square tests. Use “task-complete for the declared affine family” rather than an unqualified “exact order” in informal prose.

11. In the singular-range theorem, the common-kernel conclusion uses the strict lower factor `l>0`. Keep this visible when the theorem is reused.

12. The pseudoinverse map is Borel but generally unbounded near rank change. The proof correctly avoids a uniform norm; the introduction should not suggest a quantitative inverse estimate.

13. Proposition `prop:continuity` uses trace/base-norm contraction for a normalized instrument. A reference to the base-norm contraction principle would improve readability.

14. The stopped-instrument extension gives no expected stopping-cost bound. This caveat is correctly stated and should remain adjacent to the result.

15. In the regular-profile upper, the separated location balls make the reliability-location rectangles disjoint. Say this explicitly before summing their lower masses.

16. The bounded-`b` regime is controlled because `b^{-2/alpha}` has a positive lower bound on a fixed compact interval. This is correct but worth one extra phrase.

17. In the stratified theorem, components may overlap. The upper's Radon--Nikodym construction is what removes the need for an observed component label; emphasize that this is an existence argument, not automatically an effective classifier.

18. In the atom theorem, strict positivity below threshold uses `w>0` almost surely on the remainder. It does not follow merely from absence of another atom at `(x_*,0)`.

19. The metastable bound uses actual initial bad-mode mass. Do not replace it by a stationary bad-mode probability in applications.

20. In the gate calculation, define the gate and productive call counters before the expectation inequality. This will make `kappa_-` easier to verify.

21. The classical upper needs the command draw independent of the current hidden input conditional on the visible past. The manuscript states this; retain it in every corollary.

22. The quantum upper similarly requires the Weyl-weight sampler to be independent of the current hidden state. A merely correct marginal distribution is insufficient.

23. The qubit example uses one productive call containing pulse and instrument. Laboratory implementations with separate operations must add cost and routing states.

24. The quotient theorem's compact exhaustion includes only positive-likelihood histories under one prepared law. This is not a uniform likelihood floor.

25. The Borel section construction is sound but longer than necessary. A standard compact-fiber measurable-selection citation would help readers verify the descriptive-set-theoretic step.

26. The numerical proposition uses a pointwise acceptance-probability error. An `L^1` error would require the additional actual-law domination used later in the effective corollary.

27. The effective corollary's finite enumeration may be enormous. Avoid “algorithm” without the modifier “terminating exhaustive certification.”

28. The simulator deficiency is for the complete stopped scored transcript. A terminal-output marginal is insufficient, particularly for premature stopping.

29. The joint theorem's lower projects the enlarged decoder to the core coordinate. State explicitly that projection cannot increase the number of core values beyond `M`.

30. The erased-sign lower uses erasure probability `2 epsilon` and conditional squared loss one, hence contribution `2 epsilon`. Keep this normalization fixed when comparing to deficiency `epsilon`.

31. The pilot count-vector bound `(n+1)^J` is conservative; the exact number is smaller. The conservative count is acceptable and should be described as such.

32. The pilot proposition's small rejection-risk conclusion requires the tighter true band. Without it, only false-certification control and guarded termination remain.

33. The finite tests and structural negative controls are useful diagnostics but should not be described as evidence for continuum inequalities.

34. The current successful status of workflow run `38562870143` postdates the frozen receipt. Record the dates to avoid making the old “queued” observation appear false at its own timestamp.

35. The native bibliography has only eight items. For a top-four submission on a mature intersection of sampling, experiment comparison, quantization, stopping, predictive representation, and quantum sufficiency, this is too narrow.

36. The first R59 report and this report should remain separate immutable review objects. A future author response should identify which comments are answered rather than merging the reports.

---

## 16. Top-four significance assessment

R59 has a real mathematical center. The actual-history comparison lemma, the relative/additive split, and the event/state resource semantics are not cosmetic. The theorem gives a reusable template for deriving finite-resource curves from unnormalized task order.

Nevertheless, I do not currently see the breadth or external consequence required for a top-four general journal.

The principal reasons are:

1. **The theorem is sufficient rather than intrinsic.** The lower witness and common upper construction carry much of the difficulty. No near-necessary criterion explains when general causal experiments admit them.

2. **The static profile is classical in origin.** The novelty is the transfer architecture, not a new quantization or trimming principle.

3. **The raw examples are highly structured.** Transitive group and Weyl averaging are effective verifiers, but they are tailored to the order certificate.

4. **No recognized natural problem is resolved.** The paper does not determine a previously unknown optimum for a standard selective-sampling, POMDP, causal coding, or quantum-control model.

5. **The effective layer is certificate-heavy.** It proves finite describability under supplied partitions, nets, integrations, and margins, not a nontrivial global complexity theorem.

6. **The predictive realization remains fixed-law.** A common quotient for an unknown-model family is still an explicit open obligation.

7. **The title suggests a broader classification.** The actual theorem is one important layer of the Foundations program, not the completion of that program.

The paper would have a stronger top-four case if it achieved at least one of the following:

- an intrinsic necessary-and-sufficient task-order characterization;
- a converse showing that any near-optimal causal program induces an approximate witness/common-construction structure;
- a natural application solving an established open finite-memory or selective-sampling problem;
- a generalization beyond transitive/Weyl averaging to state-dependent likelihoods with a sharp resource curve;
- a matched lower and upper for program bits, precision, workspace, and time in addition to persistent labels; or
- a common predictive quotient and transfer theorem for a substantial unknown-model class.

---

## 17. Specialist-journal path

For a specialist venue, the manuscript could become publishable after a focused revision that:

- centers the article on the actual-history comparison lemma and affine task-order theorem;
- adds the missing causal rejection-sampling and endogenous-stopping literature;
- shortens repository/process discussion in the mathematical article;
- states the strong certificate assumptions in one table;
- adds one natural application or a broader primitive verification theorem;
- preserves the event/state stopping repair and relative/additive distinction; and
- moves exhaustive effective-certification details to an appendix unless a stronger complexity theorem is obtained.

The native article is already substantially more coherent than the long historical pipeline. The correct editorial object is the 25-page article, with the 37-page companion used for technical ancestry rather than presented as an additional main submission.

---

## 18. Build and evidence audit

The frozen R59 packet records:

- ordinary source `29de5433c2c4f45d5174a87a8588fd3a24d3f84a`;
- artifact commit `fcdb32640e4bb69922f07233fa6148bfc9b13165`;
- terminal referee-ready head `8da12b07fbed64e13bb4bb42bfc73fc56c85d37a`;
- native PDF SHA-256 `d242364dc8d2e67dd76b0aede802cb3fc7e0bfa3879fce4e4612ee38f644ac7d`;
- 25 native pages and 37 companion pages;
- 13,247 new exact finite checks plus four deliberate negative controls;
- byte-identical ordinary and optimized regression outputs;
- three-pass TeX builds with no undefined references, citations, or overfull boxes; and
- a clean read-only export reproducing both PDF and text artifacts on the recorded toolchain.

The packet's final verification observed GitHub Actions run `38562870143` while it was queued and correctly did not count it as a successful independent-host run at that time. Current remote readback shows:

```text
status:     completed
conclusion: success
head_sha:   29de5433c2c4f45d5174a87a8588fd3a24d3f84a
```

This later status strengthens reproducibility evidence but does not alter the mathematics. The proper repository action is an append-only successor note, not retroactive mutation of the frozen receipt.

Builds, hashes, finite checks, and rendered PDFs certify delivery consistency only. They do not certify the continuum arguments, novelty, priority, or journal significance.

---

## 19. Final recommendation

R59 is a serious mathematical paper. Its central proof is coherent under explicit hypotheses, the earlier stopping-resource error has been repaired, and the relative task-order extension is substantive. I found no new fatal correctness defect in the load-bearing arguments reviewed.

I nevertheless recommend **rejection at the top-four general-mathematics level in the present form**. The result is not yet an intrinsic foundations theorem for broad causal experiments, and the manuscript has not demonstrated a sufficiently strong natural external consequence. The closest sampling and endogenous-stopping literature is also absent from the native comparison.

For a strong specialist journal, I would support a **focused major revision** rather than a negative assessment of the mathematics itself.
