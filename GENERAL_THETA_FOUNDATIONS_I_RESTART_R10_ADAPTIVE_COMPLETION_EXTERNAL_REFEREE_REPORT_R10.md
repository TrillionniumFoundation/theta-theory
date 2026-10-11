# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r10-adaptive-completion-2026-10-08`  
**Reviewed exact branch head:** `49e4c07574e0a17e91a19214247596bbfba4869e`  
**Reviewed branch root tree:** `85b73b5cac52284a05944f5a9a54da348e47270d`  
**Immutable R10 mathematical-source commit:** `6b9677c4444d8b57386d024473a550f0a2b57a27`  
**Hosted artifact commit:** `6d417a72aae936affd1c9ae1fa6b0c2bd8b988bc`  
**R10 paper-directory tree:** `d6f830f1e8e7d92521f62cde7c7aaf7c28c13219`  
**Native source-only tree:** `7378579e02b0f0e51876f560b2fc1cfc0a3a3579`  
**Native PDF blob / SHA-256:** `eaeef8b2df116489f85d0185d39d6f4a58ca1d63` / `7057134523d39d129872e55549b0564d99c3f7d9d76a6b0d4582faf78ac54fef`  
**Integral Supplement S blob / SHA-256:** `9923114cedf6b692acdf06f1fc37c2d413478ecf` / `46460a0ffed95864efc1083fd33e52b81890a1a56edaca5aca6e84ca0323d93c`  
**Latest preceding external restart report located:** R7 review head `f04b0c0c967a75dfa2f09cbfb3d38e54cef639d2`, report blob `637f674f3e074c9f9d82f1d0e7ac61bb7aab3f5d`  
**Review branch:** `review/general-theta-restart-r10-adaptive-completion-external-top4-referee-r10-2026-10-08`  
**Date:** 8 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision R10 is a major mathematical advance over R7 and over the retained R8–R9 line. It directly addresses the strongest unresolved challenge in the R7 report: the paper now treats an acquisition problem in which the optimal next physical observation genuinely depends on the observed history, and it compiles a full-history acquisition policy into one autonomous finite machine whose state budget includes every internal action node, stopping node, and terminal readout node. The central theorem is not a leaf-count statement disguised as a controller theorem. Its proof explicitly pays the conversion from at most `m` leaves to at most `2m-1` total nodes and chooses `m=floor((M+1)/2)`.

R10 also retains the R8–R9 continuation programme: one-cut decoder-side-information geometry, a positive-noise continuous-query separation, a serial acquired-exponent theorem, changing observable rank, and a singular preparation with a noisy suffix. Thus the current submission has both an observation-dependent adaptive-acquisition theorem under separated response refinement and a distinct overlapping-noise theorem under continuation-chart or serial-cover hypotheses.

In the load-bearing arguments I checked, I did not find an elementary gap invalidating:

- the exact full-history checkpoint functional `Psi(n,M)`;
- the actual-mass frontier comparison and its cardinality-stability estimate;
- finite-horizon depth pruning of a full-history policy tree;
- conversion of the pruned tree into an autonomous machine counting all internal and terminal states;
- the comparison `Psi(n,M) asymp A_n+q_M(mu)` without interchanging a policy infimum with a policy-dependent acquired law;
- the correlated graph-directed verification and its strict observation-dependent feedback advantage;
- the common acquisition–memory–calibration–defect profile and exact early erasure deficiency;
- the one-cut functional source-coding identity and product/conditional continuation bounds;
- the serial acquired-exponent theorem and its single recursively executable `M`-label upper;
- the positive-noise Gaussian continuation example;
- the changing-rank and singular-prefix realizations;
- the primitive sparse-Gaussian block theorem for ordinary categorical squared filtering loss;
- the stopped occupation bound, measurable maximal coupling, and common-task causal-morphism implications; or
- the stated source, artifact, and rebuild bindings.

The negative top-four judgment now concerns the **intrinsic reach and concentration of the main advance**, not the absence of serious new mathematics. The autonomous-completion theorem is proved under a strong hierarchical certificate: every positive-probability observation splits the response support into uniformly separated children, branch masses are uniformly bounded below, and child scales are bounded uniformly away from both zero and one. These hypotheses are natural for strongly separated refinement trees, but they exclude the central difficulty of overlapping noisy adaptive sensing. The new Markov realization is exact, elegant, and genuinely feedback dependent, but it is deliberately engineered around binary graph-directed digits with a very small fixed contraction and separated response cylinders. It demonstrates the theorem rather than resolving a broadly recognized natural adaptive-inference problem.

The noisy Gaussian and singular-continuation theorems are more natural and allow overlapping laws, but their acquisition order is fixed. Conversely, the new observation-dependent acquisition theorem does not cover their overlapping-noise regime. The article therefore contains two powerful sufficient mechanisms rather than one intrinsic theory unifying them. It still does not give a necessary-and-sufficient or near-necessary characterization of when optimal full-history acquisition and checkpoint compression can be completed by a finite autonomous machine of the same order.

For a strong specialist journal in probability, information theory, stochastic control, nonlinear filtering, quantization, or applied probability, my assessment is **favorable after a focused major revision**. At that level the autonomous-completion theorem, the correlated feedback realization, the continuation geometry, and the standard-loss filtering consequence form a substantial and coherent contribution.

---

## 1. Review object, provenance, and pipeline inspected

A branch search immediately before depositing this report identified R10 as the latest `referee-ready/general-theta-restart-*` branch. No later R11 referee-ready branch was present. The exact object reviewed is the evidence-only terminal head

```text
49e4c07574e0a17e91a19214247596bbfba4869e.
```

The referee packet identifies the immutable ordinary-source commit

```text
6b9677c4444d8b57386d024473a550f0a2b57a27
```

and the hosted artifact child

```text
6d417a72aae936affd1c9ae1fa6b0c2bd8b988bc.
```

The terminal head adds read-only verification evidence and does not change the mathematical source or PDFs. The complete R4–R9 sibling subtrees and the review-input subtree are retained by Git identity.

I reviewed the submission as a source, proof, and delivery pipeline, not merely from its abstract. The inspection included:

- `main.tex`, all fifteen active section inputs, and `references.tex`;
- the new adaptive-completion and correlated-refinement sections in full;
- the retained continuation, serial-geometry, noisy-regression, changing-rank, singular, progressive-acquisition, sparse-filter, stopped-interface, and morphism sections;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, `RESEARCH_CONTRACT.md`, and `PINNED_INPUTS.md`;
- `SOURCE_MANIFEST.json`, `verify.py`, `regression.py`, `build.py`, the hosted build receipt, the independent rebuild record, the read-only verification record, and the referee packet;
- the complete integral Supplement S and the unchanged retained R6 technical text from which it is built;
- the R7 external report and the subsequent R8–R10 response chain; and
- a targeted independent search of nearby adaptive sensing, optimal decision-tree, adaptive-submodular, active-feature-acquisition, controlled-sensing, source-coding, quantization, filtering, and finite-controller literature.

The source audit records forty-two native source files plus the manifest, sixteen active TeX inputs, thirty-six formal statements, 154 labels, 215 references, and thirty-three bibliography entries. The native PDF has forty-eight pages and the integral supplement has twenty-three pages. The R10 exact finite suite reports 2,734 checks and invokes the retained R9/R8/R7/R6 suites. The verification script checks manifested source hashes, native Git-tree identity, active TeX inputs, labels, references, citations, and statement counts. The new regression script checks the exact rational moment systems, feedback Bellman formulas, positive feedback gap, frontier balancing, cardinality stability, depth truncation, full-node controller count, acquired mass, and the joint erasure-state conversion.

The hosted and independent environments each rebuild the complete native article and integral supplement in isolated directories. Within each environment the paired PDFs are byte-identical. Across TeX environments the PDF bytes differ, while normalized extracted text, page counts, and the declared MuPDF raster comparison agree. The records report zero undefined references and zero overfull boxes. All downloaded packet files are reported unchanged by the independent run.

These controls are unusually careful and useful. They establish source binding, finite arithmetic witnesses, and reproducibility. They do not establish the continuum theorems, priority, or top-four significance, and the submission correctly states those limitations. I did not treat build success or regression counts as mathematical evidence beyond the finite identities they actually test.

I did not independently re-audit every theorem in the frozen v1–v96 archive, every historical report, or every independent realization branch. Exact preservation is not fresh mathematical certification, and the history ledger makes that distinction appropriately.

---

## 2. Executive assessment of R10

The central new problem is no longer a fixed-exploration compression theorem. It is a joint acquisition-and-compression problem. For a legal full-history acquisition policy `pi` with at most `n` physical observations, let

```text
nu_n^pi = Law(m_H),
A_n^pi  = E v_H,
A_n     = inf_pi A_n^pi,
Psi(n,M)= inf_pi {A_n^pi + q_M(nu_n^pi)}.
```

Here `m_H` and `v_H` are the conditional mean and residual variance of the one fixed bounded audit response. The checkpoint class may use the complete acquired history once and retain at most `M` terminal labels. The autonomous class must choose observations, stop, and produce its readout using a machine with at most `M` total data-dependent states.

Under uniform binary response-refinement hypotheses, Theorem `thm:autonomous` proves

```text
R_cp^ref(n,M)-B_infinity = Psi(n,M),
Psi(n,M) <= R_aut^ref(n,M)-B_infinity <= C Psi(n,M),
Psi(n,M) asymp A_n + q_M(mu),
```

with constants independent of `n`, `M`, and the policy. The preparation-response law `mu` is an oracle lower witness; it is not substituted for the finite acquired law.

The proof has four genuinely linked steps.

1. Actual node energies `e_h=w_h ell_h^2` define a greedy frontier profile `G_L`.
2. Uniform branch mass, scale retention, and support separation make `G_L` comparable with `q_L(mu)` and give a doubling/cardinality-stability relation.
3. A full-history variance-minimizing policy tree is pruned simultaneously by depth and leaf count without paying more than its residual acquisition variance plus a frontier term.
4. The finite pruned tree is compiled as a complete autonomous controller, counting every internal and terminal node.

The fourth step is essential. A tree with `m` leaves has at most `2m-1` nodes; choosing `m=floor((M+1)/2)` makes the entire controller fit in the declared alphabet. The node identity supplies the action, depth, and stopping/readout status, so an uncharged observation-dependent clock is not used.

This theorem materially improves the paper. Earlier revisions separately established finite-state prediction under block stability, continuation lower bounds, fixed-order progressive acquisition, and serial observable exponents. R10 closes a different loop: an optimal full-history observation policy is compared with an autonomous bounded-state implementation.

The raw verification also improves the significance of the acquisition result. In the graph-directed example, the first coordinate selected in each digit pair depends on the acquired parity state. The manuscript computes exact conditional variance reductions and proves a strictly positive three-call feedback advantage over every fixed third-coordinate choice. This is not the independent-fair-tail situation criticized in R7.

The remaining question is whether the certificate and realization are broad enough to support the title's foundational and top-four ambition. In my judgment they are not yet broad enough.

---

## 3. Response to the R7 external report

| R7 issue | R10 assessment |
|---|---|
| Adaptive acquisition did not genuinely depend on observed values | **Resolved in substance.** The graph-directed realization has an acquired Markov state and the optimal next coordinate changes with that state. A strict feedback advantage is computed exactly. |
| No autonomous controller theorem counted all internal acquisition states | **Resolved.** Theorem `thm:autonomous` counts every internal and terminal node and pays `2m-1<=M`. |
| No noisy natural use of continuation geometry | **Resolved in the retained R8 line.** The positive-noise Gaussian continuation theorem gives online exponent `d` versus scalar checkpoint exponent one in the same binary task. |
| No quantitative sufficiency/completeness class for continuation widths | **Substantially addressed in R8–R9.** The chart and serial theorems combine actual cut lower bounds with one legal recursive upper on declared certificate classes. They remain sufficient classes, not a general duality. |
| Decoder-side-information and functional-coding antecedents were missing | **Resolved to a satisfactory level.** The article compares Wyner–Ziv, coding for computing, and nonasymptotic side-information coding at theorem level. |
| Classical bit allocation and successive refinement were insufficiently treated | **Resolved.** The article explicitly separates the merged-list argument from classical marginal allocation and successive refinement. |
| Product domination needed reusable raw constructions and conditional localization | **Resolved.** Density lower bounds, regeneration minorization, and conditional cuts are stated and proved. |
| Progressive sensing was structurally nonadaptive in values | **Resolved for one nonproduct separated class, not generally.** R10 supplies observation-dependent control but still assumes separated response refinement. |
| A near-characterization or duality between lower and upper certificates was absent | **Partially addressed.** The serial theorem and autonomous-completion theorem give two classwise equivalences, but no intrinsic criterion covers both overlapping-noise and separated adaptive sensing. |
| Full multi-resource optimality was absent | **Still open and honestly stated.** Program, planning, scratch, precision, simulator state, and time receive feasible upper accounts, not a matching general lower region. |
| Submission status of the retained companion was unclear | **Resolved.** Supplement S is identified as an integral submitted supplement, not an external publication. |
| Title and umbrella terminology promised exceptional breadth | **Still not fully resolved.** The scope is now much stronger, but `Foundations` still suggests an intrinsic general theory rather than two substantial certificate classes. |

R10 is therefore not an incremental response. It answers most concrete requests of the R7 report and directly satisfies one of the report's examples of an advance that could materially change the assessment: genuinely observation-adaptive acquisition on a correlated source.

The top-four recommendation nevertheless remains negative because the new theorem's strong separation structure and the designed nature of its main realization limit its natural reach.

---

## 4. The adaptive response-refinement model

### 4.1 Raw experimental meaning

The response refinement is defined from a prepared physical experiment and one bounded audit task. Observation actions do not alter the audit response or preparation law, and their conditional reports are independent of the audit randomness once the physical response is fixed. This is the appropriate setting for information acquisition rather than intervention on the outcome itself.

At every positive-probability history, each legal binary observation has two children whose conditional probabilities lie in `[p_*,1-p_*]`. The conditional response supports partition the parent support, child supports are separated by at least `g ell_h`, and child scales lie between `a_* ell_h` and `b_* ell_h` with `b_*<1`. These constants are fixed before the policy and budget.

This class is more general than an independent product tree. It permits correlated, nonstationary, singular, and observation-dependent branching. It is, however, a strong-separation class. A noisy report whose two posterior-response supports overlap does not fit merely because it is informative. The manuscript acknowledges this boundary, and it is load-bearing.

### 4.2 Information and state cuts

The distinction between the checkpoint and autonomous classes is clean. The checkpoint procedure may use the complete history for acquisition and then compress once. The autonomous procedure may never reread a report and must keep its entire data-dependent tuple inside the `M` states at every cut. A deterministic program table is separate, but it cannot contain observations. Temporary workspace must be erased before the next persistent cut.

This is a meaningful hard-state model. The paper avoids three common mistakes:

- it does not count only terminal leaves while ignoring internal controller nodes;
- it does not supply the stop time or program position as a data-dependent public register; and
- it does not retain a hidden exact posterior alongside the finite state.

### 4.3 Exact checkpoint functional

For a fixed policy, conditional projection gives acquisition variance plus `M`-center distortion of the actual acquired conditional mean. Infimizing jointly over policies gives `Psi(n,M)` without commuting the policy infimum through either term.

Allowing independent randomized policies does not improve the infimum: after fixing the independent seed, one obtains a deterministic policy and an `M`-center terminal code; averaging cannot beat the best fixed seed. The manuscript uses this principle correctly, although it should be stated as a short standalone lemma because the exact identity is central.

The treatment of early stopping is also sound under the stated model. Additional legal observations do not alter the audit response, and their reports may be ignored. Thus a rule stopping before `n` can be extended to depth `n` without increasing risk. This argument depends on nonempty legal continuation and the nonintervention assumption; both should remain explicit.

---

## 5. Audit of the central proof

### 5.1 Frontier balance

The node energy

```text
e_h = w_h ell_h^2
```

is actual probability mass times squared response scale. Splitting a maximal-energy leaf produces children whose energies are at least

```text
eta e_h,   eta=p_* a_*^2,
```

while the total child energy is at most `b_*^2 e_h`. Induction therefore keeps every greedy-frontier leaf within a fixed multiplicative range of the frontier maximum.

This is the correct quantity. It retains actual branch mass and does not renormalize rare subtrees. A purely geometric diameter would not control expected squared loss, while a pure mass would ignore resolution.

### 5.2 Quantization lower

For two frontier leaves, their first separating children occur below a common ancestor. Strong separation at that ancestor makes appropriately scaled neighborhoods of the leaf supports pairwise disjoint. With at most `L` centers, at least `L` of the `2L` leaf neighborhoods are missed. Each missed leaf contributes its actual mass times the square of the neighborhood radius.

The argument gives

```text
c_0 G_L <= q_L(mu) <= D^2 G_L.
```

The upper uses one conditional response center per leaf. The lower is a union/packing argument on the actual preparation-response law, not on an ambient volume measure.

I found the first-separation and neighborhood-radius calculation consistent with the stated support partition and scale monotonicity.

### 5.3 Cardinality stability

The nontrivial budget conversion is

```text
G_{2L} >= 2 eta^3 G_L.
```

Between the `L`-leaf and `2L`-leaf frontiers, only `L` additional splits occur. Hence at least one original leaf subtree receives at most one split. Balance and child-energy retention then keep the later maximum at least `eta^2` times the earlier maximum, and the later frontier has `2L` leaves each carrying at least another factor `eta` of that maximum.

This estimate is crude when `p_*` or `a_*` is small, but it is uniform and sufficient to compare `q_m(mu)` with `q_M(mu)` when `M<=2m`. The deterioration is honestly displayed through the certificate constants.

### 5.4 Finite-horizon pruning

The policy tree of a full-history acquisition minimizer is finite at depth `n`. The proof first considers the unrestricted max-energy splitting order and then deletes splits below depth `n`. The remaining eligible splits form an initial segment of the filtered order. Continuing the finite-horizon greedy process can only refine the resulting partition.

Leaves stopped before depth `n` pay a frontier-diameter term. Depth-`n` leaves pay their actual conditional residual variance. Summing gives

```text
risk <= A_n^pi + D^2 G_m.
```

This is the correct interaction between acquisition and tree pruning. It does not pretend that all unresolved uncertainty is controlled by a geometric leaf diameter, and it does not substitute the preparation law for the acquired law.

### 5.5 Counting the autonomous machine

A full binary tree with at most `m` leaves has at most `2m-1` nodes. The node identity specifies the next action at an internal node and the stop/readout at a leaf. Since the physical report is binary, the transition to either child is determined by the current node and current report. No complete history, exact response center, or external clock is retained.

Taking

```text
m=floor((M+1)/2)
```

puts all nodes inside `M`. This is the decisive repair of the leaf-count/controller-count distinction. The regression suite contains an explicit negative control for the false identification of leaf count with controller count.

### 5.6 Oracle comparison

Every procedure has two independent lower bounds:

```text
risk-B_infinity >= A_n,
risk-B_infinity >= q_M(mu).
```

The first is full-history acquisition uncertainty. The second relaxes acquisition restrictions and gives an `M`-center reconstruction of the physical response itself. Their maximum is comparable with their sum.

For the upper, choose a policy nearly minimizing `A_n`, compile its pruned tree, and use the frontier comparison at `m`. Cardinality stability converts `q_m(mu)` to `q_M(mu)`. This proves

```text
Psi(n,M) asymp A_n+q_M(mu).
```

The proof does not claim that the actual acquired law equals `mu`, and it does not exchange

```text
inf_pi [A_n^pi+q_M(nu_n^pi)]
```

with separate infima. This is a substantial point and is handled correctly.

### 5.7 Quantifier discipline

The refinement constants, action alphabet, support partition, and audit task are fixed before the policy, depth, and memory budget. The theorem is uniform in all legal policies within this class. The program table implementing the chosen finite tree may depend on the known experiment, `n`, and `M`; it is charged separately from the data-dependent state.

The distinction between existence of a finite autonomous machine and efficient computation of the optimal policy is also maintained. The Bellman programme can be exponentially expensive. Corollary `cor:finitepolicy` gives a feasible finite-table account, not a polynomial-time planning theorem.

---

## 6. Audit of the correlated graph-directed realization

The realization uses two correlated digit streams with a two-state acquired parity process. In state zero, the two next digits have probabilities `(1/2,1/10)`; in state one they are reversed. The first coordinate of the pair is chosen by the controller, while the second must be acquired separately. The next state is the pair parity.

The geometric response is a graph-directed Cantor vector with contraction `r=1/100`. The terminal bounded audit is affine in that vector followed by Bernoulli sampling. All observations are paid calls.

### 6.1 Verification of the refinement assumptions

Every branch probability lies in `[1/10,9/10]`. The response cylinder after a full pair is a scaled copy of the next-state support. After the first digit of a pair, one coordinate has refined scale and the other has not. The manuscript's half-pair scale is comparable to the parent and child scales by fixed constants. Strong separation follows from the digit gap and the small contraction ratio.

The resulting constants are conservative but valid. The support is nonproduct because the parity state couples future digit laws, while every finite word has positive actual mass.

### 6.2 Exact moment system

The mean and second-moment equations are finite linear systems with rational coefficients. The transition matrix of the parity state has both rows `(1/2,1/2)`. Conditional variance reduction from observing coordinate `j` in state `i` is computed by the standard two-child variance identity.

The manuscript proves a strict ordering:

```text
Delta_{i,i} > Delta_{i,1-i}.
```

Thus the best first observation in the next pair is the coordinate indexed by the acquired state. The closed even/odd formula for optimal residual variance follows from this state recursion.

### 6.3 Strict feedback advantage

After one complete pair, the parity state is random. A fixed choice for the third physical observation is optimal in at most one state, whereas the feedback policy chooses the high-value coordinate in either state. The difference is a positive rational multiple of

```text
r^2[(Delta_{0,0}-Delta_{0,1})+(Delta_{1,1}-Delta_{1,0})].
```

This is a genuine observation-dependent advantage, not merely a policy that changes with deterministic depth. The regression script checks both the exact conditional-variance identity and positivity of this gap.

### 6.4 Significance boundary

The example is mathematically clean and directly answers the R7 objection. It remains a certificate-designed model. The binary pair structure, parity transition, exact strong separation, and very small contraction are selected so that all theorem hypotheses and moment equations are explicit. It does not resolve adaptive finite-memory prediction for a standard nonlinear sensor, controlled hidden Markov model with overlapping emissions, or unknown-kernel experiment.

The nonstationary extension permits history-dependent pair laws and scales under uniform floors. That is useful, but it preserves the same separated graph-directed mechanism.

---

## 7. The joint resource profile

Corollary `cor:adaptivejoint` adds an unknown bit, an inaccessible calibration sign, and an early erasure channel to the correlated acquisition experiment. The common direct-sum squared task has one physical audit. The virtual exact-bit report must be completed before the progressive acquisition commands.

The lower contains:

- adaptive acquisition uncertainty;
- physical response quantization under the total state budget;
- the explicit two-sign calibration term; and
- the Bayes error of the erased bit.

The upper stores one of three channel statuses together with one geometric controller state. The chosen geometric budget `L=floor((M-1)/3)` gives

```text
1+3L <= M.
```

Cardinality stability converts the resulting geometric profile back to the `M` scale. This is an appropriate total-state count.

The causal deficiency from the erasure source to the exact-bit target is exactly `epsilon`. On erasure, a fair virtual bit creates joint-law defect `epsilon`; data processing and the triangle inequality between the two parameter laws give the matching lower. This is a specified attained defect, not an assertion that every allowed defect is a risk floor.

The theorem is useful because several resource coordinates occur in one scored task. It is not a general matched region for simulator state, controller state, program length, scratch, precision, planning time, and physical duration. The manuscript says so.

---

## 8. Retained continuation and serial geometry

R10 is not only the new separated-tree theorem. The retained R8–R9 material supplies a second major line.

### 8.1 Exact one-cut problem

At a fixed causal cut, the only prefix-dependent object crossing the cut is one of `M` labels, while the decoder later receives the complete physical suffix. Fixing algorithm coins converts the later computation into at most `M` Borel functions of the suffix. This gives the exact finite-code variational problem

```text
inf_{a_1,...,a_M} E min_i E[||z(H,U)-a_i(U)||^2 | H].
```

Product lower and upper domination compare this value with Hilbert-space quantization of continuation-response functions. Conditional localization handles diagonal or shared-interface situations where a global product submeasure vanishes.

This is correctly identified as a one-shot functional source-coding problem with decoder side information, not as a newly discovered coding reduction.

### 8.2 Continuation-chart realization

The chart theorem combines a positive-mass co-Lipschitz response chart with a global response modulus and tail moment bound. It constructs a legal recursion by quantizing scalar reports as they arrive and proves

```text
online excess asymp M^{-2/d},
checkpoint excess <= M^{-2}.
```

The upper never stores an exact real prefix. This is a genuine sufficiency result on its declared class.

### 8.3 Positive-noise example

The Gaussian experiment has noisy sequential prefix reports, a noisy linear packet, a continuously distributed sphere query, and a binary audit. Normal conditioning yields an explicit response function. A compact acquired prefix event and compact packet interval give a nonzero common suffix sublaw. The response functions are co-Lipschitz in the acquired prefix after integration over the query directions.

The result is a strict same-task separation:

```text
online excess asymp M^{-2/d},
checkpoint excess asymp M^{-2}.
```

No bit or query index is exactly recovered, and the suffix law depends on the prefix. This is a convincing nontrivial use of continuation geometry.

### 8.4 Serial acquired exponents

The serial theorem assigns a task state and exponent to every cut. Actual observable submeasures give lower bounds, while global inward covers and a candidate Lyapunov envelope give a single recursive upper. If `s_*` is the largest intermediate exponent and `s_T` the terminal exponent, then

```text
online excess asymp M^{-2/s_*},
checkpoint excess asymp M^{-2/s_T}.
```

The proof is coherent under its global candidate-domain assumptions. It is not an unconditional theorem that cut widths alone construct a recursion.

### 8.5 Changing rank and singular preparation

The rank-sensitive Gaussian theorem derives the relevant partial task state from the distribution of executable query directions, not from ambient hidden dimension. The singular theorem derives prefix exponents from actual Cantor-cylinder masses and includes the one-dimensional terminal forecast in the maximum. These examples correctly demonstrate that the largest observable cut can be intermediate or terminal.

These results materially strengthen the submission. Their limitation is that they remain fixed-acquisition experiments; they do not close the overlapping-noise adaptive-acquisition problem left outside the R10 theorem.

---

## 9. Sparse filtering, stopping, and morphisms

The primitive sparse-Gaussian filtering theorem remains a useful separate verification. Component-mass preservation prevents microstep rounding from destroying positivity accumulated by a primitive product. A positive-probability report block yields strict projective contraction, while an exponential envelope controls its complement. An actual posterior Jacobian lower gives the ordinary categorical squared-filtering rate `M^{-2/d}`.

The stopped theorem correctly uses an augmented Lyapunov function and predictable continuation indicators. It does not insert a random time into a deterministic estimate. The checkpoint cut counts a retained clock unless that interface is explicitly free and conditioned upon.

The maximal coupling lemma supplies jointly measurable kernels on standard Borel report spaces. The stopped transcript comparison sums first-disagreement probabilities under the actual physical shadow. It is finite-horizon complete-law control, not infinite-path or large-deviation equivalence.

The morphism theorem counts predictor, simulator, controller, and phase states multiplicatively, while workspace, program, precision, physical calls, and time remain separate. Reverse certificates transfer lower bounds with the explicit inflated budget. The exact-bit/erasure example is a genuine complete-law application; the Gaussian report comparison is only a forward same-controller comparison and is not mislabeled as a reverse theorem.

---

## 10. Assessment against the controlling targets

### F1 — Causal acquired-geometry transfer

**Strongly achieved on two substantial certificate classes.**

The paper has a relation-preserving block theorem, continuation lower bounds, a serial observable-exponent theorem, and now an autonomous adaptive-completion theorem. Each begins with raw experimental or task-response hypotheses and produces executable finite-state conclusions.

The remaining limitation is intrinsic completeness: no theorem characterizes arbitrary experiments, and the two strongest classes use different sufficient structures.

### F2 — Resource–resolution–risk composition

**Substantially achieved for the declared coordinates.**

The paper combines acquisition count, total data-dependent state, calibration, numerical error, and an attained deficiency term in explicit common tasks. Simulator/controller/clock state is not silently omitted.

A matched general region for program length, scratch, arithmetic time, planning complexity, physical duration, and minimal simulator state is not proved.

### F3 — Singular or nonuniform extension

**Achieved.**

The submission includes nonhomogeneous singular progressive laws, graph-directed correlated singular acquisition, changing observable rank, singular preparation with a noisy continuation, sparse products without one-step contraction, and changing intermediate exponents.

Constants are not uniform at degeneration, and no such uniformity is claimed.

### F4 — Distinct raw realizations

**Achieved convincingly.**

The correlated separated-refinement model, positive-noise Gaussian continuation model, singular noisy-suffix model, progressive product sensor, and sparse hidden Markov filter are genuinely different experiments. They verify different theorem lines rather than being used circularly to prove the foundations results.

---

## 11. Novelty and literature positioning

The manuscript now has a responsible comparison with quantization, predictive-state representations, Blackwell/Le Cam comparison, recursive filter quantization, decoder side information, functional coding, successive refinement, POMDP belief covering, finite-state-controller synthesis, adaptive tree approximation, Cantor quantization, and Markov-type quantization.

The new R10 section correctly cites Binev–DeVore for adaptive tree approximation and does not claim that greedy tree refinement is itself new. It also correctly separates static fractal quantization from compilation of an acquisition policy into a bounded autonomous controller.

However, the literature map is still incomplete around the precise new claim of observation-dependent acquisition. The revision should compare directly with at least the following neighboring routes.

1. **Adaptive submodularity.** D. Golovin and A. Krause, *Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization*, J. Artificial Intelligence Research 42 (2011), 427–486. This work gives policy-level approximation guarantees for observation-adaptive stochastic optimization. R10's objective, hard total-state budget, actual response quantization lower, and strong-refinement completion theorem are different, but the relationship must be stated.

2. **Active sequential hypothesis testing and controlled sensing.** M. Naghshvar and T. Javidi, *Active Sequential Hypothesis Testing*, Ann. Statist. 41 (2013), and S. Nitinawarat and V. V. Veeravalli, *Controlled Sensing for Sequential Multihypothesis Testing with Controlled Markovian Observations and Non-Uniform Control Cost*, Sequential Analysis 34 (2015), 1–24. These papers study observation-dependent causal sensing, dynamic programming, inferential risk, and Markovian observations. They do not impose the present hard controller-state/quantization objective, but they are closer than the current tree-approximation paragraph suggests.

3. **Optimal decision trees with noisy outcomes.** S. Jia, F. Navidi, V. Nagarajan, and R. Ravi, *Optimal Decision Tree and Adaptive Submodular Ranking with Noisy Outcomes*, JMLR 25 (2024), no. 382, 1–42. Their goal is hypothesis identification with nearly optimal test cost under noisy outcomes, not squared response distortion with an autonomous state budget. Nevertheless, both theories compile observation-dependent testing policies into trees and require a theorem-level distinction.

4. **Active feature acquisition.** M. Valancius, M. Lennon, and J. Oliva, *Acquisition Conditioned Oracle for Nongreedy Active Feature Acquisition*, ICML 2024, and H. von Kleist, A. Zamanian, I. Shpitser, and N. Ahmidi, *Evaluation of Active Feature Acquisition Methods for Time-varying Feature Settings*, JMLR 26 (2025). These works address sequential feature acquisition for prediction and the distributional consequences of changing the acquisition policy. They do not prove R10's finite-state geometric law, but they are necessary context for the claim that the next observation depends on the acquired values.

5. **Cost-sensitive decision trees and budgeted features.** The feature-budgeted prediction and noisy optimal-decision-tree literature should be acknowledged even where its objective is computational or statistical rather than geometric.

A targeted search did not reveal an exact duplicate of Theorem `thm:autonomous`: namely, uniform comparison of optimal full-history acquisition plus terminal `M`-point compression with one autonomous machine having at most `M` total states, under actual-mass separated response refinement. That is not a priority certificate. The neighboring literature is close enough that the present omission weakens the novelty assessment.

The clean distinction is available. Prior active-sensing or decision-tree results generally optimize observations, identification cost, utility, or predictive error under an acquisition budget. R10 additionally proves a hard persistent-state converse from the physical response law and a controller compilation whose **entire** node set fits the same cardinality order. Conversely, R10's strong-separation geometry is much narrower than the noisy-outcome and overlapping-feature models treated in parts of that literature.

---

## 12. Why the paper remains below the top-four threshold

R10 has now answered several objections that previously justified an easy negative decision. The current negative judgment is narrower.

### 12.1 The central theorem is a strong certificate theorem, not an intrinsic classification

The response-support partition and uniform gap are sufficient to turn every observation into a geometrically separated refinement. Many important adaptive experiments have overlapping posterior-response supports after every finite observation. In those models no positive `g` exists, even though finite-state completion may still be possible.

The continuation/serial theorem handles some overlapping-noise fixed-order experiments, but there is no theorem combining adaptive choice with that overlapping geometry. Thus the manuscript has two theories rather than one intrinsic criterion.

### 12.2 The main adaptive realization is designed around the certificate

The graph-directed model is nonproduct and genuinely feedback dependent, which is a real advance. Yet the binary pair structure, parity state, exact digit observations, fixed tiny contraction, and separated cylinders are chosen to make the certificate explicit. The strict feedback gain is positive but occurs in a deliberately small finite mechanism.

A theorem for a standard controlled hidden Markov model, adaptive sensor selection problem, sequential regression model, or partially observed expanding system would carry substantially greater natural-problem impact.

### 12.3 The proof ingredients are elegant but individually elementary

Conditional projection, dynamic programming on a finite tree, greedy frontier balancing, packing separated cylinders, depth pruning, and binary-tree node counting are standard ingredients. Their synthesis is new and nontrivial. For a top-four case, the synthesis would need either broader intrinsic scope or a decisive hard application.

### 12.4 The submission's breadth disperses the novelty

The article and supplement contain several valuable programmes: block stability, continuation widths, serial exponents, noisy rank, singular geometry, progressive acquisition, autonomous completion, stopped comparison, and causal morphisms. The architecture is coherent, but the mathematical peak is spread across multiple sufficient mechanisms. A leading general journal would normally require a smaller number of results with a more unmistakable central breakthrough.

### 12.5 Full computational-resource optimality remains open

The autonomous theorem matches physical observations and total persistent states. Planning can still be exponential; program tables and exact comparison routines can be large; finite precision and scratch receive upper accounts. No matching theorem controls the joint region of acquisition, state, description, workspace, planning time, execution time, and simulation defect.

This is not a flaw in the proved statements. It limits the foundational breadth of the current result.

---

## 13. Major issues before specialist-journal publication

### 13.1 Add a theorem-level active-sensing and decision-tree comparison

This is the most important remaining literature issue. The revision should compare its raw object, objective, policy class, and conclusion with adaptive submodularity, active sequential hypothesis testing, controlled Markovian sensing, noisy optimal decision trees, and active feature acquisition.

The comparison should explicitly address:

- expected test cost versus fixed observation horizon;
- identification error versus squared audit-response distortion;
- adaptive utility approximation versus checkpoint/autonomous risk equivalence;
- policy-tree leaves versus the total persistent node alphabet;
- noisy overlapping outcomes versus separated response supports; and
- computational policy synthesis versus existence of a finite-state completion.

### 13.2 State the structural status of strong separation more prominently

The abstract says the theorem assumes uniformly separated response refinements, but the introduction should explain immediately that this is an ultrametric-like or tree-separation mechanism. It is not a generic consequence of informative observations.

Give at least one example where finite-state completion holds but strong separation fails, or explain why the continuation theorem rather than Theorem `thm:autonomous` is the intended tool there.

### 13.3 Provide a natural overlapping-noise adaptive application

The strongest possible revision would combine the two central lines: an observation-dependent acquisition policy whose reports overlap, together with a matched hard-state law. A controlled Gaussian sensor, finite-state hidden Markov sensor-selection problem, or noisy adaptive query model would be substantially more convincing than another exact separated-digit construction.

### 13.4 Isolate the randomized-policy reduction

The exact checkpoint identity should contain a short lemma saying that conditioning on all independent acquisition and decoder coins produces a deterministic policy/code pair and that averaging cannot beat the deterministic infimum. This is already the logic of the proof, but the quantifier is central enough to deserve explicit treatment.

### 13.5 Clarify the relationship between program size and autonomous state

The node identity contains action and stop/readout instructions because a read-only table is supplied. State clearly whether the theorem permits arbitrary known real constants or only Borel instructions, and point the reader immediately to the finite-table corollary for a computable implementation.

The data-state theorem is valid without polynomial program size; the exposition should make that model choice unmistakable.

### 13.6 Separate planning existence from planning complexity in the headline claims

The theorem proves existence of a finite machine compiled from a full-history minimizer. It does not provide an efficient algorithm for finding that minimizer. This distinction appears later, but should be visible next to the principal theorem summary.

### 13.7 Reduce duplication between the native article and Supplement S

The submission package is now formally self-contained, but the forty-eight-page native article plus twenty-three-page supplement remains heavy. The final specialist submission would benefit from a sharper division: retain only the definitions and previous theorems needed for the new R10 argument, and move provenance/audit material outside the mathematical narrative.

### 13.8 Reconsider the title or define the umbrella term

The title can be retained only if `General Theta` is defined as a mathematical programme and `Foundations` is reconciled with the certificate-class status. A title centered on causal finite-state prediction, continuation geometry, and adaptive acquisition would more accurately set expectations.

---

## 14. Technical and expository comments

1. In the definition of the response refinement, state explicitly that all children of every positive-probability node also have positive probability because of the branch floor. This is used in the complete binary-tree count.

2. Specify whether policies in the definition of `Psi(n,M)` are deterministic, with randomization eliminated by seed conditioning, or randomized with the seed included in the formal history. The proof supports either convention, but one should be chosen.

3. In the exact checkpoint identity, display the fixed-policy projection formula before taking the policy infimum.

4. When extending an early-stopping policy to depth `n`, repeat that observation actions do not alter the audit response and that a legal continuation exists at every node.

5. In Lemma `lem:frontiercomparison`, define the greedy tie-breaking order in the theorem statement rather than only in the proof or implementation notes.

6. The relation between the maximum frontier energy `t_L` and `G_L` drives the doubling estimate. A one-line displayed inequality

   ```text
   L eta t_L <= G_L <= L t_L
   ```

   would make the proof easier to audit.

7. In the packing lower, name the least common ancestor and the two first separating children explicitly, then display the lower bound on the distance between the corresponding leaf supports.

8. Clarify whether the support diameter condition applies to the essential support of the conditional law or a chosen compact carrier. Null-set versions should not alter the geometry.

9. In the pruning lemma, state that the unrestricted split list is filtered by the depth condition and that the truncated tree's splits form an initial segment of this filtered list.

10. In Theorem `thm:autonomous`, put `2m-1<=M` in the theorem statement rather than only in the proof. It is the principal resource conversion.

11. State explicitly that every internal node has exactly two positive-probability outgoing reports, so a tree with `m` leaves has exactly `2m-1` nodes when nonempty.

12. When the terminal code uses conditional response means, explain how ties among nearest centers are broken measurably.

13. The constant-factor comparison between `q_m(mu)` and `q_M(mu)` should display the number of doubling steps required from `m` to `M`; here one step suffices because `M<=2m`.

14. In the correlated realization, label clearly the two scales: full-pair scale and half-pair scale. The current proof is correct but requires careful reconstruction.

15. Display the exact branch-probability floor and support-gap constants obtained for `r=1/100` in one table.

16. In the strict feedback calculation, write the best fixed third observation and best state-dependent observation in adjacent displayed formulas before subtracting them.

17. The nonstationary extension should say whether the policy knows the time/history-dependent calibrated kernels exactly or receives them through a finite program.

18. In Corollary `cor:adaptivejoint`, keep the compulsory early-completion order in bold in every statement and summary. Without it, the exact deficiency assertion changes.

19. Explain whether the channel status is retained throughout acquisition or can be merged with some geometric controller states. The current `1+3L` count is a safe upper; it is not claimed minimal.

20. In the finite-table corollary, separate comparison precision, output precision, and coefficient precision. Their bit requirements can scale differently.

21. State that the policy table may be exponential in `n`, even when sequential execution is linear in depth.

22. In the one-cut theorem, retain the statement that the suffix includes all public actions, phases, costs, and reports, not observation values alone.

23. In conditional continuation cuts, repeat that the conditioning variable is physically reissued or supplied only as a lower-bound relaxation; it is not a free upper register.

24. The serial theorem uses a task realization that may be smaller than the full predictive quotient. Repeat near the morphism section that such a state does not automatically simulate the full experiment.

25. In the noisy Gaussian theorem, identify the chart measure and the compact minorization event before introducing the response co-Lipschitz constant.

26. In the rank theorem, distinguish ambient hidden dimension, acquired task-state rank, and terminal forecast dimension in the theorem statement itself.

27. In the singular theorem, state the product-cylinder cover cardinality and actual small-ball exponent in one lemma before invoking the serial theorem.

28. In the filtering theorem, keep the final action-before-report quantifier adjacent to the posterior Jacobian calculation.

29. In the stopped theorem, distinguish the block-count stopping variable from any variance or noise parameter denoted by a similar symbol elsewhere.

30. The common-risk morphism theorem should list the exact certified target strategy class each time it is invoked. The current final paragraph does this and should not be shortened.

31. The manuscript should not use build counts, branch counts, or regression counts in any novelty argument. The present mathematical text respects this boundary.

32. The proof and resource ledgers are useful to a referee but need not all appear in a journal submission. They can remain repository evidence.

---

## 15. What would materially change the top-four assessment

Additional polishing, more finite checks, or another strongly separated binary example would not by itself change the recommendation. A top-four case would require an advance of a different order, such as one of the following.

1. **An intrinsic completion criterion.** Prove a necessary-and-sufficient or near-necessary condition for when the optimal full-history acquisition/checkpoint profile can be implemented by an autonomous finite machine at the same state order.

2. **A unification of separated and overlapping observations.** Extend autonomous completion to noisy refinements with overlapping response supports, replacing hard support gaps by an intrinsic statistical or transport separation.

3. **A natural hard adaptive application.** Resolve the memory–acquisition law of a recognized controlled filter, adaptive sensor-selection model, regime-switching nonlinear system, partially observed expanding map, or sequential regression problem whose optimal next experiment genuinely depends on noisy observed values.

4. **A duality between continuation lower bounds and recursive upper certificates.** Derive a finite autonomous recursion from a quantitative family of continuation widths under broadly verifiable conditions, or prove that failure of every such recursion forces a width separation.

5. **A matched computational-resource region.** Add lower bounds for several intrinsic coordinates among persistent state, program description, workspace, planning time, execution time, precision, simulator state, and physical acquisition.

6. **A broad controlled-sensing theorem.** Connect the present hard-state risk law to active sequential testing or adaptive-submodular sensing over a natural family, with explicit comparison to optimal full-history policies.

Any one of these could concentrate the current architecture into a result of exceptional general-mathematics significance.

---

## 16. Final evaluation

R10 is the strongest revision in the restart sequence and the first one that fully answers the earlier request for a genuinely observation-dependent acquisition theorem with the acquisition controller itself counted in the finite state budget. The central completion theorem is mathematically meaningful. Its proof correctly links actual-mass frontier geometry, finite-horizon pruning, checkpoint quantization, and full-node controller compilation. The graph-directed realization establishes a strict feedback advantage by exact calculations. The retained continuation and serial theorems supply a second, overlapping-noise route and a convincing noisy online/checkpoint exponent separation.

I found no elementary fatal error in the principal arguments checked. The source and delivery pipeline is unusually disciplined and accurately limits what finite checks and reproducible builds establish.

The paper nevertheless remains below the exceptional threshold of the four leading general mathematics journals. The autonomous theorem relies on uniformly separated response refinements; the main adaptive realization is deliberately constructed around that certificate; overlapping-noise acquisition remains fixed-order; and no intrinsic theory unifies the two mechanisms. The nearest active-sensing, noisy-decision-tree, adaptive-submodular, and active-feature-acquisition literature also requires a fuller theorem-level comparison.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** the manuscript now contains substantial and apparently sound new mathematics, but not yet the intrinsic completeness, natural hard-problem resolution, or concentrated universality expected at that exceptional level. This is not an identified technical-correctness rejection.  
**Specialist-journal outlook:** favorable after a focused major revision addressing the active-sensing/decision-tree literature, the conceptual status of strong separation, randomized-policy quantifiers, program-versus-state accounting, and a natural noisy observation-adaptive application.
