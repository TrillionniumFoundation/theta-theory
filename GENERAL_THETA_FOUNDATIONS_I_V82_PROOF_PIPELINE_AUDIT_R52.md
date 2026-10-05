# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 82 (r52)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `57937576a6f413594589d0509a6816ca4ea3a83e`  
**Candidate publication:** `4fe7ac00523cbff0e437d06fa2fe1969eb15cc73`  
**Qualified native source:** `868c841240f62a35cf7fc16ace388b0d11dfa920`  
**Revision 81 base:** `67ada63a593d452f23e8d26540504b8fb8ab8acc`  
**Controlling external report:** v77/r51, `96a3666ed516ea12fcdb8ede341b7082e4ff2c78`  
**Controlling proof/pipeline audit:** v77/r51, `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`  
**Source qualification workflow:** `37254696596`, success  
**Exact-head read-only workflow:** `37255323514`, success  
**Audit branch:** `review/general-theta-foundations-i-v82-proof-pipeline-audit-r52-2026-10-05`  
**Date:** 5 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** The v82 response and referee-ready aliases coincide at `57937576...`; no later GTF-I revision was located. |
| Source genealogy | **Pass.** The native source, publication, and metadata-only exact review head form a pinned direct chain from completed v81. |
| New finite-outcome metric | **Pass with stated interior hypothesis.** No fatal gap found in the horizontal ODE, adaptive cancellation, stopping reduction, or Bernoulli lower witness. |
| New affine entropy | **Pass.** The target is a genuine `(k-1)d^2`-dimensional norm ball and arbitrary legal covering centres are handled. |
| New exact public code | **Pass as finite construction.** Normalization, spectral legality, equality cases, and real-input representation are treated; runtime/workspace are not efficient. |
| New common learner | **Pass with fixed-`k` qualification.** The public relabeling, binary learners, simultaneous legalization, and error ledger are coherent. |
| New coherent converse | **Pass.** The split-label simulation is reference preserving, including the odd-alphabet erasure branch. |
| Description converse | **Pass for fixed-length public deterministic decoders.** It is distinct from expected-prefix conventions. |
| Finite certificate transfer | **Pass.** The normalized Choi trace bound, tensor telescoping, fixed-event transfer, and exact verification conditions are correct. |
| Growing-`k` minimax optimality | **Open.** The upper has `k^3`; the lower is inherited from one binary subfamily. |
| Full multi-outcome boundary | **Open.** v82 covers a balanced interior; binary full-body results do not automatically extend. |
| Reference implementation | **Pass for the stated finite kernels.** No physical learner or general matrix-grid certificate is executed. |
| Finite regression | **Pass as exact regression evidence.** It does not prove continuum theorems or priority. |
| Source qualification | **Pass.** Run `37254696596` committed and qualified source/publication artifacts. |
| Exact-head reconstruction | **Pass.** Run `37255323514` reconstructed the exact final head read-only. |
| Cryptographic authorship | **Open.** The final commit is unsigned and no signature claim is made. |
| Independent human priority | **Not established.** The author audit is targeted; no specialist opinion is supplied. |
| Whole Theta analytic programme | **Open.** All aggregate completion flags remain false. |
| Four-leading-journal threshold | **Not met.** This is a scope/significance assessment, not a correctness rejection. |

The new local proof chain is coherent. The strongest caveat is not an identified counterexample but the difference between fixed-`k` sharpness and a genuinely joint multi-outcome minimax theorem.

---

## 1. Frozen object and branch genealogy

The audited manuscript aliases are

```text
revision/general-theta-foundations-i-v82-finite-outcome-native-2026-10-05
revision/general-theta-foundations-i-v82-finite-outcome-publication-2026-10-05
revision/general-theta-foundations-i-v82-finite-outcome-review-ready-2026-10-05
revision/general-theta-foundations-i-v82-r51-response-2026-10-05.
```

The response and review-ready aliases point to

```text
57937576a6f413594589d0509a6816ca4ea3a83e.
```

The final commit has parent `4fe7ac...` and changes only the exact-head request record. It declares the publication commit, native source, completed predecessor, controlling reports, source-qualification run, and the fact that no manuscript change occurred after publication.

The publication points back to native source

```text
868c841240f62a35cf7fc16ace388b0d11dfa920.
```

The completed predecessor is v81 at

```text
67ada63a593d452f23e8d26540504b8fb8ab8acc.
```

A comparison from v81 to v82 native source shows nine commits in the response chain. The mathematical delta is concentrated in Sections 65–66 and their proof, resource, implementation, evidence, and response files. All predecessor section files are reported byte-identical.

Both r52 review branches were created directly from `57937576...`. Each contains exactly one new report file and does not modify manuscript sources, PDFs, workflows, evidence, predecessor material, or the other review branch.

---

## 2. Submitted theorem objects

### 2.1 Quantitative article

The 81-page focused paper contains:

- retained complete binary matrix-effect geometry;
- retained full fixed-dimensional entropy;
- retained common binary learning and exact matrix coding;
- retained independent-block, dimension/accuracy, confidence, finite-control, and risk-certificate results;
- new finite-outcome geometry and exact coding;
- new finite-outcome common learning and coherent converse; and
- new finite-outcome certificate transfer.

### 2.2 Structural companion

The 41-page structural article is unchanged at the source-graph level. It contains stationarization, stochastic purification, finite physical actions, and the strong converse for fresh repeatable nondisturbing classical probes.

### 2.3 Complete edition

The 220-page complete edition preserves the cumulative programme. It is a provenance object, not an additional independent submission.

### 2.4 New interface

The v82 device is an ordered, memoryless, input-consuming `k`-outcome measurement

```text
M_E(rho)=sum_j tr(E_j rho)|j><j|,
sum_j E_j=I.
```

It returns no residual device quantum system. An external reference and adaptive tester memory are allowed around calls. The new sharp statements restrict the unknown tuple to

```text
I/(2k) <= E_j <= 3I/(2k).
```

No commutativity or common eigenbasis is assumed.

---

## 3. Active dependency graph

### 3.1 Finite-outcome metric

```text
balanced tuple segment A_j(t)=E_j+tH_j
  + strict positivity
  -> solve dot X_j = X_j A_j^(-1) H_j /2
  -> X_j^*X_j=A_j
  -> X_j^* dot X_j=H_j/2
  -> dot X_j^* dot X_j=H_j A_j^(-1) H_j/4

sum_j H_j=0
  -> W_t^* dot W_t=0
  -> cross-slot cancellation in a common adaptive dilation
  -> path derivative <= sqrt(N)||dot W_t||

A_j^(-1)<=2k I
  -> adaptive upper O(k sqrt(N) r)

one outcome eigenvector
  + repeated nonadaptive probes
  + Bernoulli product lower
  -> absolute lower Omega(min{1,sqrt(N)r})
```

### 3.2 Entropy and public code

```text
balanced tuple body
  = affine r-ball of radius 1/(2k)
  and dimension p=(k-1)d^2

metric lower with arbitrary legal centres
  -> each small D_N-ball lies in r-ball O(delta/sqrt(N))
  -> affine volume lower covering bound

maximal r-net
  + metric upper
  -> matching cover upper

inward tuple displacement
  + round first k-1 matrices
  + define final exact residual
  -> finite rational legal grid

strict greedy separation
  + closed assignment
  -> finite public exact dictionary
  -> optimal fixed-length order
```

### 3.3 Learning upper

```text
one k-outcome call
  + public 3/4-versus-1/4 relabeling for outcome j
  -> exact binary effect F_j=I/4+E_j/2

k inherited confidence-optimal binary learners
  -> raw Hermitian estimates B_j

complete tuple grid search
  -> simultaneous normalization and spectral legality
  -> r-error <=3epsilon

future-N metric upper
  + exact public dictionary
  -> D_N-error <=5delta/8
  -> fixed-length index at affine entropy order
```

### 3.4 Learning lower

```text
binary interior effect F
  -> split first binary outcome across m labels
  -> split second across m labels
  + optional erasure label I/k
  -> balanced k-outcome tuple E(F)

one binary query + public label randomization
  -> exact k-outcome instrument simulation
  -> arbitrary coherent adaptive k-learner yields binary learner

coarse-grain first m learned labels
  -> effect H close to qF in d_N
  -> metric lower gives operator error
  -> Weyl clipping into binary interior
  -> inherited binary confidence lower
```

### 3.5 Finite certificate

```text
Omega(E)=d^(-1) direct_sum_j E_j^T
  -> ||Omega(E)-Omega(G)||_1 <= k r(E,G)
  -> M-copy trace difference <= Mk r
  -> index-law TV <= Mk r/2

complete finite tuple net
  + complete fixed readout
  + exact finite success inequalities
  -> one fixed good-label event at each grid point
  -> radius a+r0 and failure alpha+Mk r0/2 on every real target
```

### 3.6 Inherited prerequisites

The v82 upper invokes `thm:rationallearner81`, whose proof depends on the v80 confidence-optimal binary interior learner, finite rational risk grids, and inherited finite-control synthesis. The v82 lower invokes `cor:operatorconfidence80`, whose proof already allows arbitrary coherent adaptive training on the binary interior.

The new theorem does not prove these prerequisites again. The predecessor sources are preserved and loaded in the focused article.

---

## 4. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Dimension-independent finite-outcome comparison | Section 65, `thm:multioutcomemetric82` | No fatal gap found | Upper displays `k`; target must be balanced interior. |
| Arbitrary-centre entropy lower | Section 65 | Correct | Uses component Bernoulli lower valid for arbitrary legal centre. |
| Affine covering order | Section 65, `thm:multioutcomeentropy82` | Correct | Sharp for fixed `k`; constants include `k`. |
| Rational normalization-safe net | Section 65, `lem:multigrid82` | Correct | Finite exact enumeration; no efficiency claim. |
| Public exact code | Section 65, `thm:multioutcomecode82` | Correctly scoped | Fixed public decoder and represented real/rational inputs. |
| Common upper learner | Section 66, `thm:multioutcomelearning82` | No fatal gap found | `k` fresh binary procedures; upper has `k^3`. |
| Coherent-adaptive query lower | Section 66 | No fatal gap found | Binary embedding yields no growing-`k` lower. |
| Joint fixed-`k` minimax order | Section 66 | Correct consequence | Must not be advertised as growing-`k` optimal. |
| Simultaneous learned word | Section 66 | Correct | No extra device calls; good-event error `5delta/8`. |
| Fixed-length description lower | Section 66 | Correct | Requires fixed public deterministic decoder and nonzero pointwise success. |
| Finite certificate transfer | Section 66, `thm:multicertificate82` | Correct | Ideal fixed readout; implementation error separate. |
| General matrix certificate execution | code/evidence | Not executed | Only scalar ternary certificate complete. |
| General physical learner execution | evidence | Not executed | Written existence/synthesis theorem only. |
| Full multi-outcome boundary | none | Open | Not implied by binary boundary theory. |
| Growing-`k` minimax | none | Open | Upper/lower gap. |

---

## 5. Detailed audit: finite-outcome metric

### 5.1 The target really is an affine norm ball

Writing `E_j=I/k+H_j`, the spectral inequalities are equivalent to

```text
-I/(2k) <= H_j <= I/(2k).
```

For Hermitian matrices this is equivalent to `||H_j||_op<=1/(2k)`. Together with `sum_j H_j=0`, the body is exactly the radius-`1/(2k)` unit ball of the max-operator tuple norm inside the translated affine space. The dimension is `(k-1)d^2` because the last Hermitian component is determined by the first `k-1`.

### 5.2 Existence and identities for the horizontal lift

Every segment effect is at least `I/(2k)`, so the ODE coefficients are continuous. Let `B_j=X_j^*X_j`. Direct differentiation gives

```text
dot B_j=(1/2)H_j A_j^(-1)B_j
       +(1/2)B_j A_j^(-1)H_j.
```

The curve `A_j` solves the same equation because substitution gives `dot A_j=H_j`. Uniqueness of the linear ODE implies `B_j=A_j`.

Then

```text
X_j^* dot X_j=(1/2)A_j A_j^(-1)H_j=H_j/2,
```

and

```text
dot X_j^* dot X_j=(1/4)H_j A_j^(-1)H_j.
```

The matrix order is correct. No simultaneous diagonalization is used.

### 5.3 Stinespring representation

The isometry

```text
W_t psi = sum_j |j>_Y |j>_Z X_j(t) psi
```

is normalized because `sum_j X_j^*X_j=I`. Tracing the duplicate label and the postmeasurement system gives the ordered classical measurement channel. The duplicate label and remaining system are proof environments, not outputs returned by the device.

### 5.4 Horizontal cancellation

The tuple normalization implies

```text
W_t^* dot W_t=sum_j X_j^* dot X_j=(1/2)sum_j H_j=0.
```

For a purified adaptive tester, the derivative of the final vector is a sum over differentiated slots. When taking the inner product of two different summands, cancel all later common isometries. At the later differentiated slot the inner product contains `W_t^*dot W_t` or its adjoint and therefore vanishes.

The incoming states before that slot may differ; the operator identity makes the cancellation state independent. Coherent controls conditioned on past labels remain common isometries and do not spoil the argument.

### 5.5 Diagonal tangent terms

Each diagonal derivative term has squared norm bounded by `||dot W_t^*dot W_t||`. Orthogonality of distinct derivative terms gives the total derivative norm at most `sqrt(N)||dot W_t||`. The derivative of the pure-state density operator has trace norm at most twice the vector derivative norm.

Partial traces, dephasing, observed-label measurement, and final tester processing are common quantum channels and contract trace norm.

### 5.6 Public stopping

A public stopping rule with at most `N` calls can be embedded into an `N`-slot coherent experiment by recording the stop flag and feeding fixed dummy states through all unused slots, then discarding their outputs. The original stopped record is a common postprocessing. The path bound therefore applies without assuming a deterministic call count.

### 5.7 Bounding the tangent energy

From `A_j>=I/(2k)`,

```text
A_j^(-1)<=2k I.
```

Because `2kI-A_j^(-1)` is positive,

```text
H_j(2kI-A_j^(-1))H_j>=0,
```

so `H_j A_j^(-1)H_j<=2kH_j^2`, without commutativity. Since `H_j^2<=r^2I`,

```text
||sum_j H_j A_j^(-1)H_j||<=2k^2 r^2.
```

This gives `sqrt(2)k sqrt(N)r`; the theorem uses the weaker convenient constant `2k`.

### 5.8 Lower witness

For one component difference `H_j`, take a unit eigenvector attaining `||H_j||`. Reusing this state and recording whether outcome `j` occurred gives product Bernoulli laws with parameter gap exactly `||H_j||`. The inherited finite Bernoulli modulus gives an absolute lower bound of order `min{1,sqrt(N)||H_j||}`.

Maximizing over `j` gives the tuple norm. The lower bound does not require the balanced interior and therefore applies to arbitrary legal covering centres later.

---

## 6. Detailed audit: entropy and exact code

### 6.1 Lower covering count

Suppose a target `E` is within operational radius `delta<1/128` of an arbitrary legal centre `F`. The metric lower gives

```text
min{1,sqrt(N)r(E,F)}<=128delta<1,
```

hence

```text
r(E,F)<=128delta/sqrt(N).
```

The intersection of the target affine space with this ball has volume at most the full `r`-ball volume at that radius. Covering the radius-`1/(2k)` target ball therefore needs at least

```text
(sqrt(N)/(256k delta))^p
```

centres when this exceeds one.

### 6.2 Upper covering count

A maximal `epsilon`-separated subset of the compact target ball is an `epsilon`-net. The half-radius balls around its points are disjoint and lie in the ball of radius `R+epsilon/2`. Norm-ball volume scaling gives

```text
#net <= (1+2R/epsilon)^p.
```

Taking `epsilon=delta/(2k sqrt(N))` and using the metric upper gives an operational cover. The stated simplified constant follows for `N>=1` and `delta<1`.

### 6.3 Inward margin in the rational grid

Put

```text
e=(k-1)d/K,
gamma=4ke.
```

The denominator bound gives `gamma<=1/2` and `e<=t/4`. The displaced tuple

```text
E'_j=(1-gamma)E_j+gamma I/k
```

has distance at most `2e` from `E_j` and margin exactly at least `2e` from both spectral faces.

### 6.4 Coordinate rounding

For the first `k-1` effects, round diagonal and upper-triangular real/imaginary coordinates. The row-sum norm estimate gives operator error at most `d/K`. Define the last effect by exact subtraction from `I`; its error is at most `(k-1)d/K=e`.

The first effects lose at most `d/K<=e` of their `2e` margin. The last loses at most `e`. Thus all remain legal and normalized exactly. Their distance from the original target is at most `3e<=3t/4<t`.

### 6.5 Exact predicates

For rational Hermitian matrices,

```text
A>=0,
sI+(E-F)>=0,
sI-(E-F)>=0
```

are exact semialgebraic predicates over the Gaussian rationals. Full positive-semidefinite tests, not only a subset of principal minors used as a heuristic prefilter, decide legality and tuple distance. Equality is accepted where the theorem uses closed balls.

### 6.6 Greedy dictionary

The grid is finite. Scan it in fixed order. Retain a point only if its distance from every retained predecessor is strictly greater than `s`. Every rejected point is within closed distance `s` of a retained predecessor. Every real target is within strict distance below `s` of a grid point. Hence every target is within `2s` of a dictionary centre.

The operational error is at most

```text
2k sqrt(N) * 2s <= delta/2.
```

Strict separation makes the half-radius balls disjoint and yields the fixed-length upper count. The entropy theorem gives the matching lower order even when decoder centres may lie outside the target interior.

### 6.7 Input representation

The covering theorem is geometric and holds for all real targets. The executable encoder requires either rational target data or certified rational approximations. The strict `3s/4<s` margin ensures eventual termination of certified comparisons. There is no hidden exact-real oracle.

### 6.8 Resource boundary

The code transmits only an index. Both parties reconstruct the same public dictionary from public parameters. The dictionary itself can contain exponentially or worse many candidates and pair tests. The theorem makes no polynomial-time or workspace claim.

---

## 7. Detailed audit: common learning upper

### 7.1 Binary simulation

Conditional on original label `x`, return bit one with probability `3/4` if `x=j` and `1/4` otherwise. The bit-one effect is

```text
(3/4)E_j+(1/4)sum_(x!=j)E_x
    = I/4+E_j/2.
```

Since this is classical postprocessing of the device output, the equality holds for the full measurement instrument acting on inputs entangled with a retained reference.

### 7.2 Component estimation

The simulated binary effects lie in `[I/4,3I/4]`. Invoke the inherited rational learner at one-use operator accuracy corresponding to

```text
epsilon=delta/(16k ceil(sqrt(N)))
```

and failure `eta/k`. Fresh records are used for each component. On the common good event, all raw reconstructed effects are within `epsilon` of their true components.

### 7.3 Simultaneous legalization

Raw component estimates need not sum to `I`. Reconstruct the complete legal tuple grid at radius `epsilon/2` and select the first grid tuple within `2epsilon` of every raw estimate. A grid tuple within `epsilon/2` of the true target exists, so on the good event the search succeeds. The selected tuple is within `3epsilon` of the target.

On any other record, failure to find a tuple returns the public uniform tuple. Thus the algorithm is total and every output is legal.

### 7.4 Future-loss and description ledger

The metric upper gives

```text
D_N(E,G)<=6k sqrt(N)epsilon<=3delta/8.
```

Encoding `G` with the public dictionary at parameter `delta/2` adds at most `delta/4`, for a total of at most `5delta/8`. No further device call is needed.

### 7.5 Query count

Each binary learner costs

```text
O(epsilon^(-2)[d^2+d log(k/eta)]).
```

Multiplication by `k` and `ceil(sqrt(N))^2<=4N` gives

```text
O(k^3 N delta^(-2)[d^2+d log(k/eta)]).
```

This is valid but not sharp in growing `k`.

### 7.6 Nonrational parameters

Choosing rational `delta'` and `eta'` within constant factors preserves the target error/failure and changes query constants only absolutely. Effective synthesis claims remain restricted to rational public parameters.

---

## 8. Detailed audit: coherent-adaptive lower

### 8.1 Balanced embedding

Let `m=floor(k/2)` and `q=2m/k`. For a binary interior effect `F`, define `m` copies of `2F/k`, `m` copies of `2(I-F)/k`, and, when `k` is odd, one `I/k` effect. The tuple sums to `I` and every component lies between `I/(2k)` and `3I/(2k)`.

### 8.2 Reference-preserving simulation

Query the binary effect once. With probability `q`, keep the bit and choose uniformly among the corresponding group of `m` labels. A specified label in the first group has effect

```text
(q/m)F=2F/k.
```

The second group is analogous. In the odd case, with probability `1-q=1/k`, erase the bit and output the extra label. The two binary subnormalized reference states sum to the original reference marginal, so the extra branch is exactly the effect `I/k`.

This establishes equality of instruments, not merely equality of scalar outcome probabilities.

### 8.3 Coarse-graining the learner output

Given a legal learned tuple, sum its first `m` effects to obtain `H`. Coarse-graining is a fixed postprocessing of both true and learned measurements, so its actual finite-use distance is at most the original `delta`.

The true coarse effect is `qF`. Since the metric lower applies to arbitrary legal binary effects and `delta<1/128`,

```text
||H-qF||<=128delta/sqrt(N).
```

### 8.4 Clipping

Divide by `q`. Because the true `F` lies in `[I/4,3I/4]`, Weyl's inequality bounds every spectral excursion of `H/q` outside this interval by `||H/q-F||`. Clipping back to the interval moves by no more than this amount. The clipped estimate is therefore within twice the original distance from `F`.

Using `q>=2/3` gives the constant `384delta/sqrt(N)`. The stated accuracy cap places this inside the inherited binary-confidence theorem's range.

### 8.5 Transfer of confidence and stopping

The k-outcome learner, together with the exact simulator and clipping postprocessing, would be a binary learner with the same unknown-device call count, every-record budget, and public stopping convention. The inherited coherent-adaptive lower therefore transfers.

The lower proves

```text
Omega(N delta^(-2)[d^2+d log(1/eta)])
```

with no growing-`k` factor. This is enough for fixed-`k` sharpness and no more.

---

## 9. Description-length converse

Let the fixed public decoder have at most `2^B` output tuples. At each target, failure below one implies that at least one output word with positive probability decodes inside the target's operational ball. Thus the entire decoder image is an operational cover of the target family.

The entropy lower gives the bit lower order independently of training cost. Randomized expected-prefix codes with shared randomness obey a different theorem and are not covered by this fixed-length argument.

---

## 10. Finite certificate audit

### 10.1 Choi record

For a maximally entangled input, the ordered classical–reference record is

```text
Omega(E)=d^(-1) direct_sum_j E_j^T.
```

It is normalized because `sum_j tr(E_j)=d`.

### 10.2 One-copy continuity

Block diagonality gives

```text
||Omega(E)-Omega(G)||_1
 = d^(-1) sum_j ||E_j-G_j||_1
 <= k r(E,G).
```

The last inequality uses `||A||_1<=d||A||_op` componentwise.

### 10.3 Product continuity

For normalized states, tensor telescoping gives

```text
||Omega(E)^⊗M-Omega(G)^⊗M||_1<=Mk r(E,G).
```

A fixed quantum readout and classical decoder contract this to total variation at most half that amount.

### 10.4 Fixed success event

At each grid point `G`, define the labels whose decoded centres are within radius `a` of `G`. The finite certificate lower bounds the probability of this fixed set. For a nearby real target `E`, every such label lies within `a+r0` of `E`. Transfer the probability of this one event using the index-law TV bound.

No continuity of a target-dependent acceptance set is assumed.

### 10.5 Exact finite verification

With rational net points, rational decoding centres, and Gaussian-rational conditional POVM effects, all probabilities and norm predicates are exact rational/algebraic expressions. Completeness requires:

- every tuple-net point;
- every classical string of length `M`;
- every conditional readout effect;
- positivity and normalization of every conditional POVM;
- every good-label equality case; and
- every risk inequality.

The supplied executable enforces completeness in the scalar ternary interface. A cutoff, omitted string, supplied partial net, illegal centre, or false failure allowance is rejected.

### 10.6 Execution boundary

The complete executed certificate has `d=1,k=3`, 3169 legal net points, and nine length-two strings. The matrix tests check exact local identities at `d=2,k=3`. They do not execute the general optimal learner or a general matrix net.

---

## 11. Implementation audit

### 11.1 `finite_outcome_certificate.py`

The program:

- parses canonical rational data;
- reconstructs the complete scalar grid;
- rejects a candidate-budget cutoff below the complete grid;
- requires every classical string;
- verifies every probability row is nonnegative and normalized;
- reconstructs the risk exactly with rational arithmetic;
- applies the theorem's continuum radius and failure buffers; and
- reports that no physical device or general matrix grid was executed.

The reusable matrix kernels implement exact tuple legality, tuple norm balls, Choi records, and conditional readout completeness.

### 11.2 `finite_outcome_check.py`

The regression pins:

- one noncommuting balanced `d=2,k=3` tuple;
- segment legality;
- ordered horizontal identities;
- exact horizontal cancellation;
- the noncommutative inverse-order bound;
- even and odd binary embeddings;
- the public relabeling equality;
- dependent final-effect rounding;
- all ternary length-two records;
- conditional readout completeness;
- closed equality cases;
- the complete scalar certificate; and
- negative controls for incomplete/illegal/tampered inputs.

The script explicitly reports that continuum theorems are not verified by finite tests.

### 11.3 What the code does not establish

The code does not prove:

- the adaptive path theorem for arbitrary dimensions;
- the affine entropy asymptotic;
- the minimax lower theorem;
- correctness of an arbitrary physical readout implementation;
- polynomial-time synthesis;
- general matrix-grid completion; or
- novelty and priority.

Those are written mathematical or external-review obligations.

---

## 12. Build and workflow audit

### 12.1 Source qualification

Workflow run `37254696596` completed successfully. Its job:

1. checked out the revision anchor and immutable predecessor;
2. installed pinned dependencies;
3. expanded the checked delta and verified proof preservation;
4. committed and pushed the actual native source without force;
5. built all manuscripts and exact suites;
6. reconstructed the complete source and standalone journal package;
7. committed qualified artifacts on the native-source parent;
8. verified the exact publication head read-only; and
9. preserved manuscripts, packages, and receipts.

### 12.2 Exact final head

Workflow run `37255323514` was triggered by exact SHA `57937576...`. It checked out the submitted object read-only and verified native ancestry, all manuscripts, finite regressions, and the standalone journal package. It then uploaded the exact-head receipt.

This closes the final-head status gap present in some earlier revisions.

### 12.3 Build receipt

The receipt records:

```text
focused article: 81 pages
structural article: 41 pages
complete edition: 220 pages
source files: 465
predecessor native files: 438
preserved complete labels: 800
preserved focused labels: 302
preserved structural labels: 116
regression suites: 20
isolated native rebuild: true
standalone journal rebuild: true
normal/optimized identical: true
physical learner executed: false
independent human priority clearance: false
```

LaTeX references/citations and bad boxes are clean in the receipt. Raw font-engine warnings are not represented as layout defects.

### 12.4 Trust boundary

The exact-head run verifies source identity and reproducibility. The commits remain unsigned. Therefore the pipeline supports byte/provenance claims but not cryptographic human authorship.

---

## 13. Preservation audit

Revision 82 states 438 predecessor native files and 800/302/116 complete/focused/structural labels. All predecessor section sources are reported byte-identical. Changed predecessor-named paths are audits, manifests, entry documents, build scripts, and manuscript loaders that incorporate the new sections.

Original changed files are retained under the predecessor-v81 audit. Earlier revision directories and review branches remain unchanged.

This is a clean cumulative-source strategy, although the resulting complete edition is too large to be a journal-facing object.

---

## 14. Literature and priority audit

### 14.1 Current primary sources

The repository correctly identifies and rechecks:

- Antonio Anna Mele and Lennart Bittel, *Optimal learning of quantum channels in diamond distance*, arXiv:2512.10214v3 (15 June 2026 revision);
- Leonardo Zambrano, Sergi Ramos-Calderer, and Richard Kueng, *Fast quantum measurement tomography with optimal error bounds*, Quantum 10, 2162 (15 July 2026).

### 14.2 Distinctions from Mele–Bittel

Their general theorem covers finite-output channels and their binary result supplies the upper primitive used by v82. They do not state the v82 future-`N` horizontal tuple metric, affine operational entropy, fixed-`k` coherent-adaptive minimax law, or public exact code.

The v82 upper learner is therefore a new reduction and resource synthesis around an existing tomography primitive, not a new primitive tomography estimator.

### 14.3 Distinctions from Zambrano–Ramos-Calderer–Kueng

Their theorem concerns known input ensembles, nonadaptive single-copy acquisition, projected least squares, and specified worst/average measurement distances. V82 permits independent maximally entangled probe–reference acquisition with collective completed-output processing, and its lower theorem allows arbitrary coherent adaptive training under future-use operational loss.

The existing tomography upper can still be translated into a sufficient v82 future-loss budget. Such a quantitative comparison should be prominent in the mathematical article.

### 14.4 Remaining uncertainty

No independent specialist has certified that the normalized tuple lift, fixed-`k` minimax law, or exact description theorem has no equivalent formulation in channel discrimination, multiparameter metrology, measurement tomography, or statistical experiment comparison. The author audit is useful but cannot settle that question.

---

## 15. Risk register

### R1 — Priority risk: high

The nearest current tomography papers are powerful and recent. The exact novelty boundary is subtle and requires human specialist review.

### R2 — Fixed-`k` versus growing-`k`: high

The manuscript's strongest minimax equality hides constants depending on `k`. The explicit upper/lower gap is large when `k` grows.

### R3 — Full-boundary scope: high

The positive margin removes the coupled rank/support singularities likely to be the hardest multi-outcome phenomenon.

### R4 — Accretive architecture: high

The focused article is 81 pages and loads many inherited generations. Reviewability and theorem visibility are at risk.

### R5 — Efficient synthesis: moderate

Finite exact procedures can be astronomically expensive. No algorithmic complexity theorem accompanies the payload theorem.

### R6 — Trusted-control interpretation: moderate

The actual-control learner and ideal finite certificate use different hypotheses. Summaries must not merge them.

### R7 — Code overinterpretation: moderate

The exact scalar certificate is strong regression evidence but could be misread as execution of the general learner.

### R8 — Constant/range proliferation: moderate

Binary full-body, binary interior, finite-outcome geometry, learning, coding, and certificate theorems have different error ranges.

### R9 — Structural-companion scope: controlled but separate

Repeatable nondisturbing probes remain an oracle-like model and are not a theorem about repeated quantum measurement.

### R10 — Whole-program overclaim: controlled

Current status files correctly keep all aggregate analytic flags false. Future summaries must preserve that separation.

---

## 16. Specialist-release acceptance gates

### Mathematical gates

- retain complete proofs of the horizontal identities and adaptive cancellation;
- keep arbitrary legal covering centres in the entropy lower;
- preserve normalization-safe dependent rounding;
- state fixed-`k` sharpness and growing-`k` openness;
- retain the subnormalized-reference proof for odd-alphabet erasure;
- keep the clipping argument as Weyl plus triangle;
- distinguish fixed-length description from expected-prefix coding;
- require complete nets and classical strings in certificates; and
- budget implementation-law error separately.

### Priority gates

- obtain independent review from experts in POVM tomography and channel discrimination;
- compare the exact access/loss/query statements of Mele–Bittel and Zambrano–Ramos-Calderer–Kueng in the main paper;
- identify prior horizontal-gauge results for normalized POVM tuples;
- avoid “first learner” or broad “optimal POVM tomography” language; and
- state precisely that novelty lies in future-use operational geometry and the combined resource theorem.

### Editorial gates

- submit the structural companion separately;
- make Sections 65–66 the main narrative;
- move revision crosswalks, implementation histories, and much binary detail to appendices or repository packages;
- place all ranges and resource conventions next to the headline theorems; and
- retain one concise open-problems section on full boundaries, growing `k`, and efficient synthesis.

### Reproducibility gates

- preserve the exact-head read-only workflow;
- retain source and page hashes;
- keep finite-test scope fields machine readable;
- distinguish complete scalar replay from local matrix checks; and
- add a signature only if one is actually produced and independently verifiable.

---

## 17. Repository-wide analytic pipeline

The frozen dependency structure remains

```text
A1 independent
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Open obligations include:

- raw unsmoothed local limits;
- controlled stopped-path laws and recovery;
- a global past kernel;
- exact canonical shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio graph cores;
- filtering/QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction.

The finite-outcome measurement results neither assume nor prove these gates. Therefore the following remain false:

```text
historical_A2_replacement
B4_aggregate
C2_aggregate
eleven_paper_aggregate
whole_Theta_programme.
```

The local article should not gain or lose credit because these independent projects share a repository.

---

## 18. Final audit verdict

### Local mathematics

**Pass with qualifications.** No fatal gap found in the new finite-outcome proof chain. The balanced-interior metric, affine entropy, exact code, fixed-`k` learner, coherent converse, and finite certificate are mutually consistent in their declared ranges.

### Implementation and evidence

**Pass as source-bound regression and reconstruction evidence.** The exact-final-head workflow is successful. The general learner and general matrix certificate are not executed and are not claimed executed.

### Priority

**Open.** The current author audit treats the two nearest 2026 sources responsibly, but independent specialist priority clearance is absent.

### Scope

**Specialist-level, not top-four-general.** The principal theorem is balanced-interior and fixed-`k`; full multi-outcome boundary geometry, growing-`k` minimax rates, and efficient synthesis remain open.

### Wider pipeline

**Open and independent.** No aggregate analytic gate changes status.

### Overall classification

```text
latest object identity:               PASS
source genealogy:                     PASS
new finite-outcome metric:            PASS WITH INTERIOR HYPOTHESIS
new affine entropy/code:              PASS
new learner:                          PASS FOR FIXED k
new coherent converse:                PASS
finite certificate:                   PASS
exact-head reconstruction:            PASS
independent priority:                 OPEN
growing-k optimality:                 OPEN
full multi-outcome boundary:          OPEN
whole Theta programme:                OPEN
four-leading-journal threshold:       NOT MET
```

Revision 82 is a strong and credible mathematical quantum-information paper. Its appropriate next step is independent specialist review and a more focused submission, not another cumulative expansion.
