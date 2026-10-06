# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 83 (r53)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7`  
**Candidate publication:** `f90f8f2fb7488f6a71521a4c2304240532835284`  
**Qualified native source:** `736c313c35e1face0fc8e00d9b8a041188880a5f`  
**Revision 82 base:** `57937576a6f413594589d0509a6816ca4ea3a83e`  
**Prior external report:** v82/r52, `5bb27a43c0f78ba99020f605a0489bcbd403e236`  
**Prior proof/pipeline audit:** v82/r52, `7d5b1033f31c348ae60ebfb04e8b8d57b3b9e75e`  
**Source qualification run:** `37260382025`, success  
**Exact-head read-only run:** `37260982071`, success  
**Audit branch:** `review/general-theta-foundations-i-v83-coupled-boundary-proof-pipeline-audit-r53-2026-10-05`  
**Date:** 5 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** v83 is the latest GTF-I object located; no v84 branch was present. |
| Branch identity | **Pass.** Response/review-ready aliases identify exact final head `58cbb260...`; native and publication aliases identify the pinned predecessors. |
| Source genealogy | **Pass.** v83 native is ten commits ahead of reviewed v82; publication and final-head request are direct one-commit successors. |
| New coupled covariance algebra | **Pass.** Factorization, positivity, concavity, tangent range, kernel formula, and projective zero characterization are coherent. |
| Regularized energy identity | **Pass.** The constrained quadratic minimizer and constants check exactly. |
| Complete-body adaptive upper | **Pass with stated interface.** No fatal gap found in local horizontal realization, cross-slot cancellation, residual hybrid bound, stopping padding, or boundary passage. |
| Midpoint formula | **Pass.** Operator concavity and inverse order give the factor two. |
| Binary restriction | **Pass.** It is exactly twice the inherited binary squared modulus. |
| Classical processing | **Pass for the unregularized energy.** No general fixed-ridge monotonicity is proved. |
| Noise crossover | **Pass as fixed-`k` family result.** The general upper and explicit rotating-projector lower have matching `N,epsilon,theta` order. |
| Exact rational evaluation | **Pass.** The nonorthogonal-basis Gram matrix is essential and included. |
| Affine legalizer | **Pass.** It is total, every-record legal, polynomial on represented input, and has the stated `4a` error. |
| Inherited v82 interior theory | **Pass as previously audited.** The new results do not remove fixed-`k` and balanced-interior qualifications. |
| Full-boundary two-sided classification | **Open.** v83 proves a global upper, not matching general lower/entropy. |
| Growing-`k` minimax | **Open.** `k^3` upper versus binary-subfamily lower remains. |
| Dictionary/readout synthesis | **Open as efficient computation.** Covariance evaluation and legalizing estimates are polynomial; global code/readout may be exhaustive. |
| New finite regression | **Pass as regression evidence.** It does not prove continuum theorems or priority. |
| Source qualification | **Pass.** Run `37260382025` completed successfully. |
| Exact final-head reconstruction | **Pass.** Run `37260982071` verified exact head read-only. |
| Cryptographic authorship | **Open.** The final commit is unsigned; no signature claim is made. |
| Independent human priority | **Not established.** Author-side comparisons are targeted and non-exhaustive. |
| Whole Theta A/B/C/D closure | **Open.** All five aggregate flags remain false. |
| Four-leading-journal threshold | **Not met.** This is significance/scope, not a correctness failure. |

The local v83 proof package is coherent in the portions inspected. Its strongest new theorem is a one-sided complete-body adaptive comparison. The wider analytic programme remains independent.

---

## 1. Frozen object and genealogy

The latest manuscript branches located were

```text
revision/general-theta-foundations-i-v83-coupled-boundary-native-2026-10-05
revision/general-theta-foundations-i-v83-coupled-boundary-publication-2026-10-05
revision/general-theta-foundations-i-v83-coupled-boundary-review-ready-2026-10-05
revision/general-theta-foundations-i-v83-r52-response-2026-10-05.
```

The exact final object is

```text
58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7.
```

Its sole change from publication `f90f8f2...` is the exact-head request JSON. Publication is one commit beyond native source `736c313...` and adds PDFs and evidence, not theorem-source changes. The native source is ten commits beyond the exact reviewed v82 head `57937576...`.

The current revision directory is

```text
papers/GTF-I-v83-coupled-boundary-geometry.
```

It preserves 465 predecessor native files, reports 495 current source files, and retains all predecessor mathematical section files byte-identically. The quantitative proof graph is reordered, while the structural source graph is unchanged.

Both r53 branches were created directly from the exact final head. Each contains exactly one new report file and does not alter manuscript source, PDFs, evidence, workflows, predecessor material, or the other review branch.

---

## 2. Submitted objects and resource boundaries

### 2.1 Quantitative article

The 90-page focused article is titled *Finite-Use Geometry and Learning of Ordered Quantum Measurements*. Its main text now presents:

- the v82 balanced finite-outcome metric and entropy;
- the v82 common learner and coherent lower;
- the new complete-body covariance upper;
- the new noise crossover and rational evaluator;
- the new affine legalizer; and
- direct tomography comparisons.

The complete binary boundary theory remains in appendices.

### 2.2 Structural companion

The 41-page structural companion is unchanged. It contains terminal stationarization/purification and the repeatable-observation strong converse. It is not a proof dependency of the new covariance theorem.

### 2.3 Complete edition

The 225-page complete edition is a preservation object. It is not a third independent journal submission.

### 2.4 Device interface

The v83 measurement is an ordered `k`-outcome, memoryless, input-consuming measurement channel

```text
M_E(rho)=sum_j tr(E_j rho)|j><j|,
sum_j E_j=I.
```

The device returns no residual quantum system. Testers may retain references and adaptive quantum memory between calls. Public stopping is bounded and may depend on observed outcomes. The operational norm is unhalved trace norm.

This interface excludes general instruments with quantum output, persistent device memory, and destructive/repeatable process interfaces from the structural paper.

---

## 3. Active mathematical dependency graph

### 3.1 Covariance algebra

```text
E_j >= 0, sum_j E_j=I
  -> stack A_j=sqrt(E_j), A^*A=I
  -> P=I-AA^* orthogonal projection

T_A(B)_j=A_j^*B_j+B_j^*A_j
T_A^*(K)_j=2A_jK_j

C_E = T_A P T_A^*/4
  -> C_E self-adjoint and positive
  -> constants in kernel
  -> range has zero tuple sum
  -> exact covariance/variance identity
  -> singular-support kernel formula
```

### 3.2 Concavity and projective zero

```text
first covariance term linear in E
S_E(K) linear in E
  -> C_((1-t)E+tF) - (1-t)C_E - tC_F
     has form t(1-t)||S_F-S_E||_HS^2
  -> operator concavity

C_E|_tangent = 0
  + constant tuples in kernel
  -> C_E form vanishes on all tuples
  -> tr(E_j-E_j^2)=0 for each j
  -> every E_j projection
  + sum_j E_j=I
  -> pairwise orthogonality
```

### 3.3 Regularized horizontal energy

```text
K=(C_E+tau I)^(-1)H
B=P T_A^*K/4
R=tau K
  -> A^*B=0
  -> T_AB+R=H
  -> objective = <H,K>
  -> feasible perturbation linear term vanishes
  -> exact minimum
```

### 3.4 Adaptive differential comparison

```text
positive effects at one path point
  + horizontal H_0=T_AB
  -> differentiate positive square roots
  + anti-Hermitian gauge
  -> effect factors with derivative B

A^*B=0
  -> W^* dot W=0
  -> cross-slot derivative terms vanish
  -> horizontal trace derivative <=2 sqrt(N)||B||_HS

residual R
  -> one reference block <=||R_j||_op
  -> N-slot hybrid <=N sum_j||R_j||_op
  -> <=N sqrt(k)||R||_HS

regularized energy with tau=1/N
  + Cauchy--Schwarz
  -> local derivative <=sqrt(k+1) g_(N,E)(H)
```

### 3.5 Boundary and midpoint

```text
mix path with uniform POVM
  -> strictly positive path
  + polynomial covariance continuity
  + ridge positivity
  + uniform g<=N||H||
  -> dominated convergence
  + ordinary hybrid endpoint convergence
  -> complete-body path bound

straight segment through midpoint M
  + covariance concavity/positivity
  -> C_E(t)+I/N >=2t(C_M+I/N), t<=1/2
  -> inverse-order square-root bound
  -> two scalar integrals sum to 2
  -> global midpoint upper
```

### 3.6 Processing and noise

```text
classical output map T
  -> same S matrix after lifting
  + matrix Jensen square
  -> <L,C_(TE)L> >= <T^*L,C_E T^*L>
  -> variational unregularized energy contracts

uniform POVM U
  -> C_U=I/k on zero-sum tangent
  + concavity
  -> noise floor epsilon I/k
  -> inverse-order global noisy upper
```

### 3.7 Matching family

```text
rotating binary projective pair
  + zero extra outcomes
  + uniform k-outcome noise
  + common fair-bit processing of extra labels
  -> exact binary noisy effects on subnormalized references
  -> inherited binary finite-pair lower
  -> scale beta N sin(theta)/sqrt(1+N epsilon)
```

### 3.8 Rational evaluator

```text
rational Hermitian basis
  + last tuple component = negative sum of first k-1
  -> rational nonorthogonal tangent basis B_a

G_ab=<B_a,B_b>
L_ab=<B_a,C_MB_b>
b_a=<B_a,F-E>

(L+G/N)x=b
  -> Q_N^2=N b^T x
  + exact PSD legality
  + fraction-free elimination/determinant bounds
  -> polynomial represented-input bit complexity
```

### 3.9 Affine legalization

```text
raw Hermitian estimates B_j
  -> arithmetic mean correction
  -> A_j=B_j+(I-sum_iB_i)/k
  -> exact normalization
  + good-event component error <=2a

shift A_j by 4aI and divide by 1+4ka
  -> exact balanced spectral bounds
  -> component error <=4a/(1+4ka)

exact legality test
  + uniform-tuple fallback
  -> total every-record legal procedure
```

### 3.10 Learning consequence

```text
k fresh actual-control binary component learners
  -> component error a=delta/(32k ceil(sqrt N))
  -> guarded affine repair
  -> future-use error <=delta/4
  + inherited public dictionary at delta/2
  -> total future-use error <=delta/2
  -> fixed-k query and description orders retained
```

The public dictionary is still a separate finite global object.

---

## 4. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Coupled covariance factorization | Section 67, Lemma `covarianceidentities83` | Correct | Real Hilbert structure; `S_E(K)` need not be Hermitian. |
| Positivity/self-adjointness | same | Correct | Follows from `T_APT_A^*/4`. |
| Operator concavity | same | Correct | Form identity, not entrywise matrix concavity. |
| Kernel formula | same | Correct | Other kernel directions may exist. |
| PVM zero-operator iff | same | Correct | Concerns zero restriction on full tangent, not one direction. |
| Regularized energy | Section 67, Lemma `horizontalenergy83` | Correct | Residual is algebraic tangent, not physical POVM. |
| Complete-body path bound | Section 67, Theorem `closedcovariance83` | No fatal gap found | Input-consuming classical-output measurement interface. |
| Midpoint upper | same | Correct | One-sided certificate; `Q_N` is not asserted to be a metric. |
| Binary reduction | same | Correct | Squared tuple modulus equals twice binary squared modulus. |
| Unregularized data processing | Section 67, Proposition `covarianceprocessing83` | Correct | Does not establish arbitrary fixed-ridge contraction. |
| General noise upper | Section 67, Theorem `noisecrossover83` | Correct | Constant depends on `k`. |
| Rotating-projector lower | same | Correct via inherited binary theorem | `d=2`, fixed `k`, specified angle/noise range. |
| Exact covariance certificate | Section 67, Proposition `covarianceexact83` | Correctly scoped | Computes proved upper, not exact adaptive distance. |
| Affine legalizer | Section 68 | Correct | Balanced target and good-event input error. |
| Total fallback | Section 68 | Correct | Exact tests on represented input. |
| Affine learner | Section 68 | Correct consequence | Still `k` component calls and public dictionary. |
| Full-boundary lower/entropy | none | Open | Not implied by the example family. |
| Growing-`k` minimax | none | Open | `k^3` upper remains. |
| Polynomial dictionary/readout | none | Open | No such claim proved. |
| General physical learner execution | evidence | Not executed | Written theorem only. |
| Whole Theta closure | status/ledger | Correctly false | No analytic aggregate gate changes. |

---

## 5. Detailed proof audit: covariance algebra

### 5.1 Real adjoint and factorization

The relevant inner product is the real part of the Hilbert--Schmidt pairing. For Hermitian `K`,

```text
(T_A^*K)_j=2A_jK_j.
```

Applying `P=I-AA^*` gives

```text
(P T_A^*K)_j=2A_j(K_j-S_E(K)).
```

Applying `T_A/4` yields exactly

```text
(C_EK)_j
 = [E_jK_j+K_jE_j-E_jS_E(K)-S_E(K)^*E_j]/2.
```

The adjoint on `S_E(K)` is necessary. The formula proves the range has zero sum and constant tuples lie in the kernel.

### 5.2 Covariance form

Because `P` is an orthogonal projection,

```text
<K,C_EK>=||P T_A^*K||_HS^2/4>=0.
```

Expanding gives both displayed covariance forms. No effect inverse or support restriction appears.

### 5.3 Concavity

The term `sum_j tr(E_jK_j^2)` is linear in `E`; the negative squared norm `-||S_E(K)||^2` is concave. Exact polarization gives the positive remainder. Thus the theorem uses operator-form ordering on the tuple Hilbert space, not entrywise ordering of output matrices.

### 5.4 Zero operator

If the covariance vanishes on every zero-sum tuple, write any tuple as its componentwise arithmetic mean plus a zero-sum tuple. Constants are already in the kernel, so the form vanishes on all tuples.

For the tuple with `K_j=I` at one index and zero elsewhere,

```text
<K,C_EK>=tr(E_j-E_j^2).
```

The spectral interval `[0,1]` forces `E_j^2=E_j`. The identity sum then forces pairwise orthogonality. The converse follows from orthogonal ranges.

No stronger kernel statement is proved or needed.

---

## 6. Detailed proof audit: regularized energy

Let `K=(C_E+tau I)^(-1)H`. With

```text
B=P T_A^*K/4,
R=tau K,
```

one has `A^*B=0` and `T_AB=C_EK`. The objective at this point is

```text
4||B||^2 + tau^(-1)||R||^2
 = <K,C_EK> + tau||K||^2
 = <H,K>.
```

For every feasible perturbation, `T_A Delta B+Delta R=0`; the linear objective term is twice its pairing with `K` and vanishes. The remaining quadratic terms are nonnegative.

The coefficient `1/4` in `B` and the factor four in the objective are consistent. This proof works on boundary effects because no `E_j^{-1}` appears.

---

## 7. Detailed proof audit: adaptive path bound

### 7.1 Local horizontal factors

At a strictly positive point, the positive square root is differentiable. For horizontal `H_0=T_AB`, the anti-Hermitian

```text
U_j=(B_j-R_j'(0))A_j^(-1)
```

makes `exp(sU_j)R_j(s)` a valid factor curve with derivative `B_j`. Anti-Hermiticity follows after multiplying `U_j+U_j^*` on both sides by `A_j` and using the derivative of `R_j(s)^2`.

This argument is used only in the interior. Singular effects are treated later by mixing, not by differentiating a square root at zero.

### 7.2 Common adaptive dilation

The measurement isometry records the outcome and an inaccessible duplicate label/factor environment. It satisfies

```text
W^*dot W=sum_j A_j^*B_j=0.
```

For derivative terms inserted at different slots of one purified tester, remove common future isometries. At the later insertion the remaining local contraction is `W^*dot W` or its adjoint, so the cross term vanishes regardless of the incoming reference-memory state.

Therefore the derivative-vector norm is the square root of the sum of diagonal slot contributions, yielding the `sqrt(N)` horizontal scaling. Final partial trace and processing contract trace norm.

### 7.3 Residual

For a joint state `rho` and Hermitian residual effect `R_j`, duality gives

```text
||Tr_A[(R_j tensor I)rho]||_1 <= ||R_j||_op.
```

A telescoping channel derivative over `N` slots then costs at most `N sum_j||R_j||_op`. The inequality to `N sqrt(k)||R||_HS` is standard.

The residual is not required to preserve positivity. It is only one term in a linear channel derivative decomposition.

### 7.4 Cauchy--Schwarz constants

Put

```text
x=2 sqrt(N)||B||,
y=N||R||.
```

Then

```text
x+sqrt(k)y <= sqrt(k+1)sqrt(x^2+y^2).
```

The squared term equals `g_(N,E)(H)^2` by the energy identity at `tau=1/N`.

### 7.5 Stopping

A publicly stopped tester can be padded to `N` calls with outputs discarded after stopping. The original record is a common postprocessing. This does not assume stopping is independent of prior outcomes.

---

## 8. Boundary passage and midpoint

For `E^epsilon=(1-epsilon)E+epsilon U`, every effect is positive. The mixed path derivative is `(1-epsilon)E'`. The regularized inverse is continuous in the polynomial covariance, and

```text
g_(N,E)(H)^2 <= N^2||H||_HS^2.
```

This uniform integrable bound justifies dominated convergence. The ordinary `N`-slot hybrid bound gives endpoint-distance convergence.

For the segment and `t<=1/2`, write

```text
E(t)=(1-2t)E+2tM.
```

Concavity and positivity give `C_E(t)>=2tC_M`. Since `I/N>=2t I/N`,

```text
C_E(t)+I/N >=2t(C_M+I/N).
```

Inverse order gives the scalar factor `(2t)^(-1/2)`. The first- and second-half integrals are each one.

---

## 9. Binary restriction and processing

### 9.1 Binary normalization

For `E=(A,I-A)` and `H=(B,-B)`, direct substitution gives the binary Sylvester variance in each component. The tuple inner product sums two equal terms, so the squared v83 modulus equals twice the inherited binary squared modulus.

### 9.2 Processing inequality

For a column-stochastic classical channel `T`, the lifted tuple `T^*L` and the processed tuple have the same `S` matrix. The form difference is

```text
sum_j tr[E_j( sum_a T_aj L_a^2
              -(sum_a T_aj L_a)^2 )].
```

The bracket is

```text
(1/2)sum_(a,b) T_aj T_bj (L_a-L_b)^2,
```

which is positive because every difference is Hermitian. Substitution into the variational energy and enlargement of the test set prove contraction.

The fixed ridge `I/N` depends on the Euclidean tuple metric and is not shown to transform monotonically under arbitrary `T`.

---

## 10. Noise crossover

On tangent tuples, the uniform measurement has `S_U(K)=0` and `C_UK=K/k`. Concavity gives the noise floor.

At the midpoint, the difference direction is multiplied by `1-epsilon`. Inverse order then gives the stated global upper.

For the lower family:

1. the first two labels carry a rotating projective binary measurement;
2. all extra effects are zero before noise;
3. uniform noise makes every extra effect `epsilon I/k`;
4. a common classical map sends labels one and two to opposite bits and each extra label to a fair bit; and
5. the resulting binary effect is `(1-epsilon)P+epsilon I/2`.

This equality holds as a channel on subnormalized reference blocks. The inherited binary lower can therefore be applied without losing entangled-input validity.

The midpoint eigenvalues and scalar modulus give the `z` scale. The upper uses the tuple Hilbert--Schmidt norm `2 sin(theta)` and the inequality between the two noise denominators.

The theorem is sharp only in the stated fixed-`k` family sense.

---

## 11. Exact evaluator and code audit

### 11.1 Linear system

The last-component-elimination basis has a nontrivial Gram matrix. The coordinate representation of `C_M+I/N` is therefore `L+G/N`, not `L+I/N`.

The exact solver computes

```text
x=(L+G/N)^(-1)b,
Q_N^2=N b^T x.
```

All entries are rational on Gaussian-rational input. The matrix is positive definite because `G` is positive definite and `L` is positive semidefinite.

### 11.2 Complexity

Clearing denominators, fraction-free elimination, determinant bit bounds, and exact inertia/PSD tests yield polynomial bit complexity in the represented input size, `d,k`, and `log N`.

This complexity statement does not cover:

- constructing the global entropy-optimal dictionary;
- optimizing the true adaptive distance;
- synthesizing arbitrary collective readouts; or
- implementing the general physical learner.

### 11.3 Regression

The new finite suite checks:

- noncommuting `d=2,k=3` examples;
- projective zero covariance;
- a nonprojective singular rank-one tuple with nonzero covariance;
- exact concavity and noise floor;
- binary normalization at singular endpoints;
- label and rational-unitary invariance;
- output processing;
- exact scalar product-law comparisons;
- affine good-event faces and bad-record fallback;
- Gram omission;
- exact certificate replay; and
- malformed input and resource-limit rejection.

Its 140 positive checks and 17 negative controls are appropriate regressions. They do not prove universal path geometry.

---

## 12. Affine repair and learner audit

### 12.1 Normalization correction

If every `B_j` is within `a` of balanced `E_j`, then

```text
A_j-E_j = (B_j-E_j) - (1/k)sum_i(B_i-E_i)
```

has operator norm at most `2a`. The sum of the `A_j` is exactly the identity.

### 12.2 Spectral repair

The corrected effects lie between

```text
(1/(2k)-2a)I and (3/(2k)+2a)I.
```

After adding `4aI` and dividing by `1+4ka`, the lower and upper bounds become exactly `I/(2k)` and `3I/(2k)`. The tuple remains normalized.

### 12.3 Error

The repaired-target difference is

```text
[A_j-E_j+4ka(I/k-E_j)]/(1+4ka).
```

The balanced radius gives `||I/k-E_j||<=1/(2k)`, so the numerator has norm at most `4a`.

### 12.4 Totality and complexity

On arbitrary records, exact balanced legality is tested. A failed test returns the uniform tuple. Thus the algorithm is total without assuming a good event. On the good event it accepts the repaired tuple.

The arithmetic correction is polynomial. Exact PSD tests are polynomial on represented rational input. There is no search over a global net.

### 12.5 Learning ledger

The learner still invokes `k` fresh component procedures at a reduced accuracy. Their union-bound failure is `eta`. Repair gives future-use error `delta/4`; the inherited public code adds `delta/4` without further calls. The `k^3` query upper and fixed-length description order remain.

The pair-dependent metric lower witness is not supplied to this common learner.

---

## 13. Source, build, and workflow audit

### 13.1 Source qualification

Run `37260382025` is the successful `GTF-I v83 native-source qualification and publication` workflow. It was triggered on the response branch, assembled/qualified native source, executed current and inherited checks, built the manuscripts and packages, and published the derived artifacts.

The source receipt identifies `736c313...` as the qualified source commit.

### 13.2 Publication delta

The publication commit is one commit beyond native source. Its changes are PDFs, logs, package archives, page checks, regression results, source hashes, theorem locations, and a build/review record. Native theorem source is unchanged.

### 13.3 Exact final-head reconstruction

Run `37260982071` is triggered by exact final head `58cbb260...`. The read-only job:

- checks out the exact object;
- installs pinned reconstruction dependencies;
- verifies native ancestry;
- reconstructs all manuscripts;
- reruns exact regressions;
- verifies the standalone journal package; and
- preserves an exact-head receipt.

All steps concluded successfully.

### 13.4 Build receipt

The current receipt records:

```text
paper.pdf              90 pages
STRUCTURAL_PAPER.pdf    41 pages
COMPLETE_REVISION.pdf  225 pages
source files           495
predecessor files      465
regression suites       21
```

All predecessor mathematical sections are reported byte-identical; normal and optimized Python outputs agree; the isolated native and standalone journal rebuilds succeed; and no unresolved references/citations are reported.

### 13.5 Evidentiary boundary

These records establish source identity and reproducibility. They do not establish:

- the continuum theorem;
- optimality outside the stated regimes;
- literature priority;
- cryptographic authorship;
- journal acceptance; or
- completion of the wider Theta programme.

---

## 14. Literature and priority audit

The current author audit checks Mele--Bittel, Zambrano--Ramos-Calderer--Kueng, and the newly posted covariant-learning paper of Yoshida--Okigami--Posta--Grinko. It also credits channel geometry, horizontal gauges, adaptive metrology, and finite-path comparison.

This is useful but not independent priority clearance. The following adjacent objects need direct expert comparison:

1. Saini, Kiukas, Burgarth, and Gilchrist, *Characterizing Fisher information of quantum measurement*, arXiv:2512.15428. Its frame-operator measurement-information geometry is not obviously the same covariance, but the distinction should be explicit.
2. Mayer and Yun, *Kernel Embedding for Operator-Valued Measures and Its Application to Quantum Tomography*, arXiv:2605.25146. Its “Quantum Covariance Embedding” uses different kernel machinery, but overlapping covariance/POVM language makes a theorem-level comparison necessary.
3. Sieniawski and Demkowicz-Dobrzański, *Adaptive quantum channel discrimination using methods of quantum metrology*, arXiv:2510.15506. Its adaptive discrimination/metrology framework is directly adjacent to the present horizontal finite-use bound.
4. Yoshida, Okigami, Posta, and Grinko, arXiv:2609.39280. The known-symmetry and gate-efficient assumptions differ, but the current article should compare theorem statements rather than only abstracts.

No inference of equivalence is made here. The point is that firstness or definitive priority of the normalized-tuple covariance is not established by the current package.

---

## 15. Repository-wide pipeline assessment

The independent analytic ordering remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent.
```

The unresolved gates include:

- raw unsmoothed local limits;
- stopped-path recovery;
- global past kernels;
- exact shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio graph cores;
- filtering/QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction.

The v83 measurement covariance does not prove one of these gates. The five machine-readable aggregate flags remain false:

```text
historical_A2_replacement = false
B4_aggregate = false
C2_aggregate = false
eleven_paper_aggregate = false
whole_Theta_program = false
```

Local theorem closure and whole-program closure remain distinct.

---

## 16. Risk register

### R1 — Full-boundary overstatement: high

A global upper certificate is not a complete metric characterization. The abstract and title must preserve this distinction.

### R2 — Priority risk: high

The exact covariance may be new, but equivalent channel-geometric formulations have not been ruled out independently.

### R3 — Growing-`k` risk: high

Fixed-`k` minimax language can be misread as joint outcome-optimality. The `k^3` gap must remain visible.

### R4 — Architecture risk: high

A ninety-page focused article with a large binary appendix remains difficult to position as one general-journal paper.

### R5 — Computational overclaim risk: moderate

Polynomial certificate/legalization can be incorrectly generalized to polynomial dictionary/readout/learner synthesis.

### R6 — Interface risk: moderate

The theorem concerns measurement channels with only classical output. Instruments and device memory are excluded.

### R7 — Boundary-kernel risk: moderate

Nonprojective measurements may have zero-energy directions. The zero-operator theorem should not be strengthened informally.

### R8 — Data-processing risk: low to moderate

Only unregularized energy monotonicity is proved. Fixed-ridge claims require separate analysis.

### R9 — Evidence risk: low

The exact-head read-only verification is strong. The commit is unsigned, but no signature claim is made.

### R10 — Whole-program overclaim risk: controlled

The current files keep all aggregate flags false. Future summaries must do the same.

---

## 17. Specialist-release acceptance gates

### Mathematical gates

- keep the complete-body result explicitly one-sided;
- keep the full derivation of `C_E=T_APT_A^*/4`;
- state the kernel caveat next to the PVM characterization;
- distinguish interior differentiation from boundary approximation;
- retain reference and adaptive-memory quantifiers;
- distinguish unregularized and regularized processing;
- state all fixed-`k`, `d=2`, noise, and angle ranges in the crossover;
- keep the Gram matrix in the evaluator contract;
- preserve every-record fallback; and
- keep the growing-`k` question open.

### Priority gates

- obtain external specialist review;
- compare current measurement Fisher/frame geometry;
- compare operator-valued-measure covariance embeddings;
- compare adaptive channel discrimination/metrology formulations;
- give a precise closest-theorem table for the covariance, not only the learning results; and
- avoid historical-firstness language until this is complete.

### Editorial gates

- submit structural work separately;
- reduce the quantitative journal object substantially;
- move cumulative binary proofs to a supplement/companion while keeping the theorem dependency self-contained;
- centralize all resource conventions;
- separate theorem statements from revision-history records; and
- present one principal contribution rather than the entire programme.

### Reproducibility gates

- retain exact native/publication/final SHA chain;
- retain read-only exact-head reconstruction;
- retain current, not predecessor, receipts;
- keep finite tests classified as regressions;
- retain resource-cap rejection in the certificate tool; and
- publish a signed archival tag/release if available.

---

## 18. Final audit verdict

### Local proof status

**Pass with qualifications.** No fatal gap was found in the new covariance identities, regularized energy, adaptive upper, boundary passage, binary restriction, unregularized processing inequality, noise family, exact evaluator, or affine legalizer.

### Quantitative completeness

**Open.** The complete multi-outcome boundary lacks a matching general lower, entropy law, and minimax learner. The growing-outcome regime is also open.

### Computational status

**Partial positive closure.** Covariance evaluation and statistical legalization are polynomial on represented rational input. Global dictionary construction, arbitrary collective readout synthesis, and general learner execution are not made polynomial.

### Reproducibility

**Pass.** Source qualification and exact-head read-only reconstruction succeeded on the pinned v83 chain. The final commit is unsigned.

### Priority

**Open.** No independent human specialist clearance is supplied, and several current adjacent geometries require direct comparison.

### Whole programme

**Open.** All A/B/C/D aggregate flags remain false.

### Four-leading-journal threshold

**Not met.** This is a scope, significance, architecture, and priority conclusion rather than a correctness dismissal.

```text
local new proofs:                 PASS WITH QUALIFICATIONS
full-boundary adaptive upper:     PASS
full-boundary two-sided theory:   OPEN
fixed-k interior minimax:         PASS AS INHERITED
joint growing-k minimax:          OPEN
polynomial covariance evaluator: PASS
polynomial statistical legalizer:PASS
global efficient synthesis:      OPEN
exact-head reproducibility:       PASS
independent priority:             OPEN
whole Theta pipeline:             OPEN
four-leading-journal bar:         NOT MET
```
