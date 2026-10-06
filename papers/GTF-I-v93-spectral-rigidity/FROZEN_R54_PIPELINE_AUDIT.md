# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 84 (r54)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `9ee14476f539a38f2f45f9bd4ed99a658a7eb14d`  
**Candidate publication:** `71681519882357a080106d571f478f5f13b9e541`  
**Qualified native source:** `bd90865ed1d755399bcf047ec4d353cac0f48206`  
**Completed predecessor:** Revision 83, `58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7`  
**Prior external report:** v83/r53, `0077ff4b39633c3e9b6947e89f0bbcdd8e5ffe2e`  
**Prior proof/pipeline audit:** v83/r53, `89c8c9cb3d1494d90c3d449d981a7424665256ab`  
**Source qualification run:** `37269000936`, success  
**Exact-head read-only run:** `37269932771`, success  
**Audit branch:** `review/general-theta-foundations-i-v84-support-geometry-proof-pipeline-audit-r54-2026-10-05`  
**Date:** 5 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** Revision 84 is the latest GTF-I object located; no Revision 85 branch was present at the final survey. |
| Exact reviewed object | **Pass.** Response and review-ready aliases identify `9ee14476...`; the final commit is metadata-only. |
| Source genealogy | **Pass.** Native source `bd90865...`, publication `7168151...`, and exact final head `9ee1447...` form a direct source/artifact/request chain from completed v83. |
| Current-document identity | **Pass.** The qualified object contains a 24-page primary, 78-page binary supplement, 41-page structural article, and 232-page preservation edition. |
| Complete covariance-kernel parameterization | **Pass.** The support-block decomposition, converse, injectivity, and nullity formula are coherent, including zero effects. |
| Unitary tangent range criterion | **Pass.** The exact kernel pairing gives `i[G,E] in Ran(C_E)` if and only if `G in W_E`. |
| Square-root orbit regime | **Pass.** The covariance-path upper and one-label Bernoulli lower give matching local `sqrt(N)|t|` order for a fixed moving orbit in the support span. |
| Linear orbit regime | **Pass with stated resources.** The flagged code, Knill–Laflamme recovery, first-derivative identity, finite-angle remainder, and call-number choice yield matching `N|t|` order under ideal pair-dependent controls. |
| Recovery interface | **Pass.** The recovery uses the actual classical label and retained reference, not a discarded input or inaccessible dilation environment. |
| Finite-angle constants | **Pass as nonuniform local constants.** `c,C,t0` depend on the fixed `E,G` and may degenerate near support transitions. |
| Support processing | **Pass.** Classical output processing enlarges the support span; a moving square-root orbit cannot become a linear orbit, though it may become stationary. |
| Transported-weight regularization | **Pass.** The extended variational energy contracts when both direction and public weights are transported through the same stochastic map. |
| Relation to operational upper | **Pass.** `B_w <= w_max I` gives the stated comparison; the uniform case requires `tau=k/N`. |
| Exact support decision | **Pass on represented input.** Rational support projectors, real-rank selection, Hilbert–Schmidt Gram projection, and exact commutator tests are properly separated. |
| New finite regression | **Pass as exact finite evidence.** The BB84 symbolic recovery and 280 positive/18 negative controls do not prove continuum theorems or execute a physical device. |
| Inherited v83 covariance theorem | **Pass as previously audited.** The new results preserve its one-sided arbitrary-pair scope. |
| Arbitrary-pair full-boundary lower/equivalence | **Open.** The orbit theorem does not classify general rank-changing pairs. |
| Full-boundary entropy/common learning | **Open.** Only balanced interiors have matching entropy and fixed-`k` learning laws. |
| Growing-`k` minimax | **Open.** The constructive learning upper retains a `k^3` factor and the lower remains binary-subfamily based. |
| Efficient dictionary/recovery/readout synthesis | **Open.** Support decisions and affine repair are polynomial; the global dictionary and general quantum-control synthesis are not. |
| Source qualification | **Pass.** Run `37269000936` rebuilt all four documents and 22 exact suites and committed source-bound artifacts. |
| Exact-head reconstruction | **Pass.** Run `37269932771` checked out and reconstructed the exact final head read-only. |
| Cryptographic authorship | **Open.** No independently verified signature is supplied; no signature claim is made. |
| Independent human priority | **Not established.** The author-side audit is targeted, and one cited recent full text now requires an updated theorem-level comparison. |
| Whole Theta A/B/C/D closure | **Open.** `historical_A2_replacement`, `B4_aggregate`, `C2_aggregate`, `eleven_paper_aggregate`, and `whole_Theta_program` remain false. |
| Four-leading-general-journal threshold | **Not met.** This is a significance, breadth, and priority determination, not a correctness rejection. |

The local v84 proof package is coherent in the portions inspected. The new support-kernel theorem is the strongest genuinely new algebraic object. The finite-use trichotomy is a useful nonasymptotic measurement-channel realization of the established Kraus-span/error-correction metrological dichotomy. The manuscript is suitable for specialist consideration after priority and exposition revisions, but the top-four general-journal threshold is not met.

---

## 1. Frozen object and branch genealogy

The current manuscript aliases are

```text
revision/general-theta-foundations-i-v84-support-native-2026-10-05
revision/general-theta-foundations-i-v84-support-publication-2026-10-05
revision/general-theta-foundations-i-v84-support-review-ready-2026-10-05
revision/general-theta-foundations-i-v84-r53-response-2026-10-05.
```

The response and review-ready aliases point to

```text
9ee14476f539a38f2f45f9bd4ed99a658a7eb14d.
```

Its only change relative to publication is

```text
GENERAL_THETA_FOUNDATIONS_I_V84_FINAL_HEAD_REQUEST.json.
```

That record pins:

```text
publication_commit = 71681519882357a080106d571f478f5f13b9e541
native_source_commit = bd90865ed1d755399bcf047ec4d353cac0f48206
completed_predecessor = 58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7
controlling_external_report = 0077ff4b39633c3e9b6947e89f0bbcdd8e5ffe2e
controlling_pipeline_audit = 89c8c9cb3d1494d90c3d449d981a7424665256ab.
```

The publication is one commit beyond the native source. It adds the rendered documents, native/source packages, page checks, theorem-location index, regression receipts, and build records. It does not modify the qualified theorem source. The exact final head is one metadata-only commit beyond publication.

A comparison from completed v83 to v84 native source shows twelve commits. The mathematical delta is localized to:

```text
sections/69-support-kernel.tex
sections/70-finite-angle-orbits.tex
sections/71-transported-regularization.tex
editions/operational-introduction84.tex
editions/current-comparison84.tex
support_geometry.py
support_check.py
SUPPORT_SCHEMA.md
```

plus current entry, response, audit, resource, bibliography, preservation, and build files. The source package reports all 495 predecessor native files represented and every predecessor mathematical section byte-identical.

Both r54 review branches were created directly from exact final head `9ee14476...`. Each review branch is intended to contain one new report and no mutation of manuscript sources, PDFs, workflows, evidence, predecessor directories, or the other review branch.

---

## 2. Submitted objects and document boundaries

### 2.1 Focused quantitative article

The 24-page primary article is titled *Finite-Use Geometry and Learning of Ordered Quantum Measurements*. Its journal-facing proof order is:

1. normalized covariance and global complete-body upper;
2. complete support description of the covariance kernel;
3. finite-angle unitary-orbit classification;
4. transported-weight regularization;
5. retained finite-outcome balanced geometry and learning consequences;
6. search-free affine legalization; and
7. current literature comparison.

### 2.2 Binary supplement

The 78-page *Binary Foundations and Auxiliary Proofs* supplement contains the complete inherited binary boundary, code, confidence, control, and certificate material. Cross-document references are rebuilt from current source using `xr-hyper`. The preservation record identifies 307 labels relocated from the v83 primary into the current supplement.

The supplement is a current proof dependency package, not a historical PDF. The main concern is editorial transparency rather than missing source: a reader should be told exactly which supplement results are prerequisites of the new primary and which are preserved but logically unused.

### 2.3 Structural companion

The 41-page structural article is unchanged at the source-graph level and independently complete. It is not a premise of the covariance, support, orbit, regularization, learning, or coding theorems in the quantitative paper.

### 2.4 Complete edition

The 232-page complete edition is a preservation object. It keeps the entire historical mathematical corpus actively typeset. It should not be presented as an additional journal submission or as a multiplier of novelty.

---

## 3. Device interface and resource model

The ordered measurement is the memoryless, input-consuming, classical-output channel

```text
M_E(rho)=sum_j tr(E_j rho)|j><j|,
sum_j E_j=I.
```

The device returns no residual quantum system. The tester may:

- entangle the device input with an external reference;
- retain arbitrary quantum memory between calls;
- choose later controls using earlier classical labels;
- use the same control rule under both hypotheses; and
- stop at a public bounded stopping time not exceeding `N`.

The operational quantity `D_N` is the supremum of unhalved final-state trace distance. Thus `0<=D_N<=2`.

The new linear-regime lower uses a different resource profile from common learning:

- the pair `E,G` is known;
- the code and recovery may depend on that pair;
- a logical qubit is carried between calls;
- a retained reference of dimension at most `2d` is used at an individual call;
- controls are ideal and trusted;
- no polynomial gate synthesis is proved; and
- no unknown-device learner is thereby constructed.

The resource ledger correctly distinguishes unknown-device calls, future horizon, transmitted index length, dictionary reconstruction, exact arithmetic, trusted-control synthesis, implementation error, and physical execution.

---

## 4. Active mathematical dependency graph

### 4.1 Inherited covariance input

```text
E_j >= 0, sum_j E_j=I
  -> stack A_j=sqrt(E_j), A^*A=I
  -> P=I-AA^* orthogonal projection

T_A(B)_j=A_j^*B_j+B_j^*A_j
C_E = T_A P T_A^*/4

  -> C_E self-adjoint and positive
  -> constant tuples in kernel
  -> range has zero tuple sum
  -> variance identity
     <K,C_E K>
       = sum_j tr(E_j K_j^2)-||S_E(K)||_HS^2
       = sum_j ||sqrt(E_j)(K_j-S_E(K))||_HS^2
  -> operator concavity in E
  -> regularized horizontal energy
  -> complete-body adaptive path upper.
```

### 4.2 Complete support kernel

```text
<K,C_E K>=0
  -> sqrt(E_j)(K_j-S_E(K))=0
  -> P_j K_j=P_j S_E(K)

S_E(K)=B+iA, A,B Hermitian
  -> P_j A P_j=0
  -> A in A_E=W_E^perp

support/cross/missing block decomposition
  -> K_j=B+i[P_j,A]+Z_j
     with Z_j=Q_j Z_j Q_j

sum_j K_j=0
  -> B=-mean_j(i[P_j,A]+Z_j)

converse reconstruction
  + sum_j E_j(i[P_j,A]+Z_j)=iA
  -> all parameter tuples are covariance-null

zero mean-subtracted tuple
  -> all X_j equal common Hermitian D
  -> D=iA
  -> D=A=0 and all Z_j=0
  -> bijection and exact nullity.
```

### 4.3 Unitary tangent range

```text
H_j=i[G,E_j]
Q_j H_j Q_j=0
sum_j H_j=0
  -> no pairing with Z_j or tuple mean

sum_j tr(H_j i[P_j,A])
  = -2 tr(GA)
    + pairing with support-block terms
  = -2 tr(GA)

C_E self-adjoint finite dimensional
  -> Ran(C_E)=ker(C_E)^perp
  -> H in Ran(C_E) iff G orthogonal to A_E
  -> H in Ran(C_E) iff G in W_E.
```

### 4.4 Spectral tangent scales

```text
Tangent decomposition H=Pi_0 H + sum_l <H,u_l>u_l
C_E u_l=lambda_l u_l

N <H,(C_E+I/N)^(-1)H>
 = N^2 ||Pi_0 H||^2
   + N sum_l |<H,u_l>|^2/(lambda_l+1/N)

fixed E,H:
  H in range and nonzero -> sqrt(N) comparison scale
  H has kernel component -> N comparison scale.
```

This is only a comparison-form statement until an operational lower is proved.

### 4.5 Square-root orbit branch

```text
E_j(t)=e^{itG}E_j e^{-itG}
H_j(t)=i[G,E_j(t)]

G in W_E and H != 0
  -> H in Ran(C_E)
  -> h^2=<H,C_E^dagger H><infinity

unitary conjugation intertwines C_E and H
  -> h constant along orbit
  -> g_{N,E(t)}(E'(t)) <= sqrt(N) h
  -> inherited path theorem gives O(sqrt(N)|t|)

some component H_j !=0
  -> choose v with <v,H_jv> !=0
  -> one-label Bernoulli gap >=c_0|t|
  -> product Bernoulli lower
  -> Omega(min(1,sqrt(N)|t|)).
```

### 4.6 Support-complement code

```text
G not in W_E
A=G-Pi_{W_E}G !=0
I in W_E -> tr A=0
A=A_+-A_-, tr A_+=tr A_-=s
rho_+=A_+/s, rho_-=A_-/s

A orthogonal to P_j H_d P_j
  -> P_j rho_+ P_j=P_j rho_- P_j

flagged purifications of rho_+,rho_-
  -> logical basis states orthogonal
  -> off-diagonal logical elements vanish
  -> diagonal elements agree for every B in P_j M_d P_j

measurement Kraus products at label j span P_j M_d P_j
  -> Knill-Laflamme conditions
  -> exact recovery on actual label and retained reference

logical generator diagonal
  -> gap Delta=tr(G(rho_+-rho_-))
              =||A||_HS^2/s >0.
```

### 4.7 Finite-angle corrected channel

```text
T=R o (M_E tensor Id)
T o J = Id_2
  -> V_l J=c_l I
  -> sum_l conjugate(c_l)V_l=J^*

Phi_t=T o Ad(e^{-itG}) o J
U_t=Ad(e^{-itG_L})

Phi_0=U_0=Id
Phi'_0=U'_0=-i[G_L,.]
second derivative diamond norms <=4||G||_op^2
  -> ||Phi_t-U_t||_diamond <=4t^2||G||_op^2
  -> m-fold telescoping <=4m t^2||G||_op^2

logical equal superposition
  -> ideal trace separation 2|sin(m t Delta/2)|
  -> actual lower after subtracting channel error.
```

### 4.8 Choice of call number

```text
m=min{N,floor(1/(|t|Delta))}
|t|<=min{1/(2Delta), Delta/(4pi||G||^2)}

x=m|t|Delta
  -> 0<x<=1
  -> x >= (1/2)min{1,N|t|Delta}
  -> 2 sin(x/2)>=2x/pi
  -> accumulated error <=x/pi
  -> D_N >= (1/(2pi))min{1,N|t|Delta}.
```

The elementary hybrid bound for the input unitaries gives the matching local upper.

### 4.9 Output processing of supports

```text
F_a=sum_j T_aj E_j, T column stochastic
support(F_a) contains support(E_j) whenever T_aj>0
one positive entry in every column
  -> W_E subset W_F

same generator after processing
  -> moving square-root orbit cannot become linear
  -> reversible splitting gives equality of support spans.
```

A processed moving orbit may become stationary; the precise monotonic statement is about exclusion of a new linear regime.

### 4.10 Transported scalar-covariance ridge

```text
public probability vector w
W_j=w_j I
B_w=C_W
(B_w K)_j=w_j(K_j-sum_l w_l K_l)

physical covariance Jensen inequality under T
scalar covariance Jensen inequality under T
linear pairing transports
  -> each left variational objective <= a right objective
  -> E_{TE,Tw,tau}(TH)<=E_{E,w,tau}(H)

stochastic S with ST=Id
  -> apply inequality to S
  -> equality.
```

### 4.11 Relation to operational covariance certificate

```text
0<=B_w<=w_max Id
positive w_j -> B_w positive definite on zero-sum tangent

tau=1/(N w_max)
C_M+tau B_w <= C_M+I/N
  -> inverse order
  -> original covariance upper <= transported-ridge energy upper.

uniform w_j=1/k
B_w|_T=Id/k
tau=k/N
  -> tau B_w=Id/N
  -> exact recovery of original Q_N normalization.
```

### 4.12 Exact represented-input decision

```text
Gaussian-rational effects
  -> exact PSD and normalization validation
  -> independent rational columns V_j
  -> P_j=V_j(V_j^*V_j)^(-1)V_j^*

compress rational Hermitian basis by P_j
  -> real coordinate rank selection for basis of W_E
  -> Hilbert-Schmidt Gram system for orthogonal projection of G

projection residual zero? -> support membership
commutators zero? -> stationarity
rank formula -> covariance nullity
fraction-free elimination + determinant bounds
  -> polynomial represented-input bit complexity.
```

The certificate classifies one known orbit. It does not compute the adaptive distance, synthesize a recovery, or run a learner.

---

## 5. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Kernel condition `P_jK_j=P_jS` | Section 69 | Correct | Uses equality of kernels of left multiplication by `sqrt(E_j)` and `P_j`; no effect inverse. |
| Support span/complement | Section 69 | Correct | Real Hermitian subspaces; `W_E` need not be an algebra. |
| Kernel parameterization | Theorem `supportkernel84` | Correct | Includes all support-cross and missing-support blocks. |
| Kernel injectivity | same | Correct | Common Hermitian matrix equals anti-Hermitian `iA`, forcing zero. |
| Kernel dimension | same | Correct | Zero effects contribute `(d-r_j)^2=d^2`. |
| Dependence only on supports | same | Correct | Nonzero eigenvalues do not enter the nullspace formula. |
| Unitary range criterion | Proposition `unitaryrange84` | Correct | Pairing is `-2 tr(GA)` on the complete kernel. |
| Spectral tangent formula | Corollary `tangentscales84` | Correct | Comparison form only; not itself an operational lower. |
| Exact support decision | Proposition `supportexact84` | Correctly scoped | Gaussian-rational represented input and exact arithmetic. |
| Orbit stationary branch | Theorem `orbittrichotomy84` | Correct | Exact equality of all conjugated effects. |
| Orbit square-root upper | same | Correct | Constants depend on `E,G`. |
| Orbit square-root lower | same | Correct | Product, nonadaptive, one-label Bernoulli witness. |
| Support-complement code | Lemma `supportcode84` | Correct | Known pair, ideal controls, reference dimension at most `2d`. |
| KL recovery | same | Correct | Recovery receives actual label and external reference only. |
| Logical gap | same | Correct | Positive but nonuniform near `W_E`. |
| Corrected-channel one-use error | Lemma `correctedchannel84` | Correct | Conservative unhalved diamond constant four. |
| Corrected-channel m-use error | same | Correct | Channel telescoping; no independence premise. |
| Explicit finite-angle lower | Theorem `orbittrichotomy84` | Correct | Local two-sided angle interval; deterministic `m<=N`. |
| Linear hybrid upper | same | Correct | Pair-dependent constant `2||G||`. |
| Full-rank corollary | Corollary `orbitexamples84` | Correct | One full-rank effect makes `W_E=H_d`. |
| Rank-one IC corollary | same | Correct | Support span equals real effect span only in rank one. |
| PVM corollary | same | Correct | Support span equals block-diagonal commutant. |
| Support processing | Proposition `supportprocessing84` | Correct | A moving square-root orbit may become stationary, not linear. |
| Extended transported energy | Section 71 | Correct | Infinite off range; constants quotient out. |
| Transported ridge contraction | Theorem `transportedridge84` | Correct | Same `tau`, transported `w`, column-stochastic convention. |
| Reversible splitting equality | same | Correct | Requires stochastic left inverse. |
| Ridge operational upper | Proposition `ridgeupper84` | Correct | Positive weights and `w_max`; does not prove arbitrary fresh-uniform monotonicity. |
| Uniform-ridge normalization | same | Correct | Uses `tau=k/N`. |
| Balanced entropy | inherited Sections 65–66 | Previously audited | Balanced interior and fixed `k`. |
| Balanced common learning | inherited Sections 66/68 | Previously audited | `k^3` constructive upper; total fallback. |
| Arbitrary-pair complete-boundary equivalence | none | Open | Current complete-body theorem is upper only. |
| Complete-boundary entropy | none | Open | Fixed-orbit result is insufficient for a volume law. |
| Growing-`k` minimax | none | Open | Binary lower does not match `k^3`. |
| Efficient public dictionary | none | Open | Exact dictionary may be exhaustive. |
| Efficient general recovery synthesis | none | Open | The support theorem is existential. |
| Physical recovery/learner execution | evidence | Not executed | Symbolic exact example only. |

---

## 6. Detailed proof audit: support kernel

### 6.1 Real Hilbert structure

All dimensions and orthogonal complements are over the real Hilbert space of Hermitian matrices with pairing `tr(AB)`. For Hermitian `P,A`, the commutator `[P,A]` is anti-Hermitian and `i[P,A]` is Hermitian. Thus every parameter tuple lies in the correct real space.

### 6.2 Kernel condition at singular effects

The inherited variance identity gives a sum of nonnegative squared Hilbert–Schmidt norms. Its vanishing is equivalent to

```text
sqrt(E_j)(K_j-S)=0.
```

Left multiplication by `sqrt(E_j)` and by its support projection `P_j` have the same kernel, so this is equivalent to `P_jK_j=P_jS`. This uses neither a Moore–Penrose inverse nor a rank-continuity assumption.

### 6.3 Non-Hermitian covariance mean

`S=sum_jE_jK_j` need not be Hermitian because `E_j` and `K_j` need not commute. Writing `S=B+iA` is therefore essential. Compression by `P_j` compares two Hermitian matrices and forces `P_jAP_j=0`.

### 6.4 Block reconstruction

The left and adjoint equations determine the support-support and cross-support blocks of `K_j-B`. The only free block is `Q_j(K_j-B)Q_j`, denoted `Z_j`. The formula `i[P_j,A]` has exactly the required cross blocks.

### 6.5 Zero-sum normalization

The common Hermitian term `B` is fixed by `sum_jK_j=0`. Subtracting the ordinary tuple mean, rather than independently normalizing outcomes, preserves every cross-block identity.

### 6.6 Converse identity

For `A` orthogonal to every support block, `E_jAP_j=0` and `E_jP_j=E_j`. Therefore the weighted sum of `i[P_j,A]` is `iA`; the `Z_j` terms vanish under `E_j`. After mean subtraction the resulting `S` makes `P_jK_j=P_jS` exact.

### 6.7 Injectivity

If the mean-subtracted tuple is zero, every pre-mean component `X_j` equals a common Hermitian matrix `D`. The weighted-sum identity identifies that common matrix with `iA`. Since `A` and `D` are Hermitian, `D=iA` is both Hermitian and anti-Hermitian, so both vanish. Each `Z_j` then vanishes. No quotient ambiguity remains.

### 6.8 Dimension count

`A_E` has dimension `d^2-dim W_E`. The Hermitian matrices supported on `Q_j` have real dimension `(d-r_j)^2`. The proven bijection makes the sum direct and gives the displayed formula.

---

## 7. Detailed proof audit: unitary range and orbit trichotomy

### 7.1 Pairing with the complete kernel

For `H_j=i[G,E_j]`, `Q_jH_jQ_j=0`. Hence the `Z_j` parts have zero pairing. The zero tuple sum of `H` removes the mean. Cyclic expansion of the remaining commutators produces `-2G` plus support-block terms, and those support-block terms are orthogonal to `A`. The pairing is exactly `-2tr(GA)`.

### 7.2 Range equality

The covariance is finite-dimensional and self-adjoint; therefore its range is exactly the orthogonal complement of its kernel. The complete kernel parameterization then converts orthogonality to every `A in A_E` into `G in W_E`.

### 7.3 Covariance energy along the orbit

Conjugation by `e^{itG}` is an orthogonal transformation of the Hermitian tuple Hilbert space. It transports supports, covariance, tangent, range, and pseudoinverse. Consequently the finite pseudoinverse quadratic energy is constant along the orbit.

### 7.4 Regularized upper in the range branch

On the positive spectrum, `(lambda+1/N)^(-1)<=lambda^(-1)`. Multiplying by `N` gives `g<=sqrt(N)h`. Integrating the inherited complete-body path theorem gives the local upper for every adaptive tester and bounded public stopping rule.

### 7.5 Bernoulli lower

A nonzero Hermitian component `H_j` has a unit vector with nonzero expectation. The event “output label j” therefore has a nonzero first derivative. A smooth two-sided probability curve with nonzero derivative cannot be at probability zero or one at the expansion point. On a sufficiently small interval the Bernoulli parameters remain in the regime needed for the inherited finite product lower. Repeating the same input is a valid product, nonadaptive experiment.

### 7.6 Traceless support residual

The identity lies in `W_E`: indeed each `E_j` belongs to `P_jH_dP_j` and their sum is the identity. Thus the orthogonal residual `A` is traceless. A nonzero traceless Hermitian matrix has both positive and negative parts with equal nonzero trace.

### 7.7 Compression equality

For every `B` supported on `P_j`, orthogonality of `A` to `P_jH_dP_j` gives `tr(B rho_+)=tr(B rho_-)`. This is equivalent to equality of the support compressions of the two states.

### 7.8 Correctable code

Flagged purifications are orthogonal. Their flags make off-diagonal matrix elements vanish for every device operator on the input. Equal support compressions make diagonal elements equal for every Kraus product at one label. Products from different labels vanish because the output labels are orthogonal. These are the full Knill–Laflamme conditions.

### 7.9 Availability of systems

After a measurement call the input has been consumed, but the device output retains the classical label and the tester retains the external reference. The recovery acts precisely on these available systems. The proof does not invoke the environment used in a Stinespring representation.

### 7.10 CPTP completion

Diagonalization of the correction matrix gives orthogonal error subspaces. Inverse isometries recover the logical state on those subspaces. Preparing a fixed state on the orthogonal complement completes a trace-preserving channel on the entire output space. This completion is needed before differentiating and composing the corrected channel.

### 7.11 Logical generator gap

The flags make `G_L` diagonal. Since the projected part of `G` is orthogonal to `A`, `tr(GA)=tr(A^2)`. Dividing by the common trace of the positive/negative parts gives the stated positive gap.

### 7.12 First derivative of the corrected channel

The identity channel has rank-one Choi matrix, so every Kraus operator of an exact corrected realization is a scalar multiple of the code isometry on the code. Trace preservation supplies the summed adjoint identity. These identities recover exactly the logical commutator at first order.

### 7.13 Taylor remainder

The commutator generator in diamond norm is at most `2||G||`. Its square is at most `4||G||^2`. Taylor’s integral remainder contributes one half of this second-derivative bound, namely `2t^2||G||^2`, to each of the actual and ideal channels. Their difference is at most four. No analytic asymptotic notation replaces the explicit inequality.

### 7.14 Accumulation through calls

The distance between `m` compositions is bounded by summing `m` one-use channel differences, since all intervening channels are contractions in diamond norm. This is deterministic telescoping, not a stochastic-independence argument.

### 7.15 Integer call selection

The small-angle condition ensures `1/(|t|Delta)>=2`, so the floor is at least one. If `N` is smaller, `m=N`; otherwise the floor approximates the inverse angle within a factor two. The resulting logical angle lies in `[0,1]` and is at least half the truncated target scale. The second angle cap controls the quadratic error relative to this angle.

### 7.16 Exhaustiveness and disjointness

Stationary orbits have zero tangent. Proposition `unitaryrange84` implies a stationary generator belongs to `W_E`; hence the stationary and outside-span branches cannot overlap. Every generator is either in or outside the span, making the three alternatives exhaustive.

---

## 8. Detailed proof audit: processing and transported ridge

### 8.1 Support of positive sums

For positive semidefinite matrices, the kernel of a positive weighted sum is the intersection of the kernels of the positively weighted summands. Therefore its support contains every positively weighted summand support. The argument is exact and noncommutative.

### 8.2 Regime interpretation

`W_E subset W_F` means a generator inside the original span remains inside the processed span. Thus a moving square-root orbit cannot become linear. It may become stationary because the processed effects can commute with the generator. A generator outside `W_E` can enter the larger `W_F`, so a linear orbit can become square-root or stationary.

### 8.3 Scalar covariance

The operator `B_w` is the covariance of the scalar POVM `(w_jI)`. Its quadratic form is a matrix-valued weighted variance and is positive semidefinite. Constants are in its kernel. With all weights positive, its restriction to the zero-sum tangent is positive definite.

### 8.4 Extended variational convention

When the stiffness has a kernel, the supremum is finite exactly when the tangent lies in its range; otherwise the linear functional can grow along a zero-cost direction. Using `+infinity` off range is the correct convention and is necessary when transported weights contain zeros.

### 8.5 Jensen comparison

The inherited physical covariance comparison is valid on the full tuple space. Applying the same identity to the scalar measurement gives the corresponding ridge comparison. No assertion that `T^*L` has zero tuple sum is needed because the dual supremum is taken on the full tuple space modulo constants.

### 8.6 Equality under reversible processing

If `S` is stochastic and `ST=Id`, applying contraction to `S` after `T` gives the reverse inequality. Hence equality holds. This applies to reversible label splitting when public weights are split through the same channel.

### 8.7 Relation to the fixed Euclidean ridge

The upper bound `B_w<=w_max I` is in the tuple Hilbert order. Multiplying by `1/(Nw_max)` gives a ridge no stronger than `I/N`. Adding the same covariance and reversing inverses yields an energy no smaller than the original fixed-ridge energy, which is the direction needed for an operational upper.

### 8.8 No refreshed-uniform inference

The processing theorem compares `(E,w,H)` with `(TE,Tw,TH)` at the same `tau`. Replacing `Tw` by a new uniform vector on a different alphabet or changing `tau` with the alphabet size is not covered. The paper states this limitation correctly.

---

## 9. Implementation and finite-evidence audit

### 9.1 `support_geometry.py`

The implementation:

- validates exact Hermiticity, positivity, and normalization;
- constructs supports from exact rational column spaces;
- verifies projector identities exactly;
- builds a rational compressed Hermitian candidate family;
- uses real coordinates only to select a linearly independent span;
- uses the Hilbert–Schmidt Gram matrix for orthogonal projection;
- checks the projection residual against every support block;
- classifies stationarity by exact commutators;
- computes the kernel dimension from exact ranks;
- computes transported energies through a tangent Gram system;
- returns `None` for infinite off-range energy;
- rejects resource-cap overflow before producing a certificate; and
- records that no distance, recovery synthesis, physical execution, or continuum proof is claimed.

This is aligned with the theorem scope.

### 9.2 `support_check.py`

The suite checks:

- PVM, BB84, Pauli-six, noisy BB84, zero-effect, split-projective, and scalar examples;
- support-span and direct covariance-nullity agreement;
- unitary range membership via exact augmented-rank tests;
- the commutator/kernel pairing;
- support-complement identities;
- missing-support null directions;
- stationary, square-root, and linear classifications;
- rational unitary and label invariance;
- support inclusion under coarse-graining;
- reversible splitting equality for transported ridge;
- noisy coarse-graining contraction;
- infinite off-range energy;
- an exact nonprojective BB84 flagged-code and conditional-reference recovery;
- an exact rational nonzero-angle corrected logical channel;
- finite-angle floor bookkeeping; and
- malformed certificate, legality, dimension, schema, and resource controls.

The suite reports 280 positive checks and 18 negative controls. It explicitly denies that the tests prove continuum statements or execute a device.

### 9.3 Scope of the BB84 example

The exact BB84 calculation is a valuable algebraic fixture. It demonstrates one complete nonprojective code/recovery identity. It does not synthesize the recovery for arbitrary input, establish robust gate complexity, or represent a laboratory execution.

### 9.4 Current and inherited suites

The builder reruns all 21 inherited suites plus the new support suite under ordinary and optimized Python. The current receipt reports matching outputs. This protects against accidental regression of inherited kernels and current exact arithmetic; it is not an independent proof of universal mathematical claims.

---

## 10. Preservation and linked-document audit

`V83_BASELINE.json` pins:

```text
495 predecessor native files
856 complete-edition labels
363 quantitative-package labels
116 structural labels.
```

The current preservation receipt states:

- every predecessor mathematical section is byte-identical;
- the complete edition keeps all predecessor sections active;
- the structural graph is unchanged;
- the current primary/supplement union preserves all prior quantitative labels;
- 307 labels were relocated to the current supplement;
- exact originals of changed entry/audit/build files are kept under `predecessor-v83-audit/`; and
- current cross-document references are rebuilt from current TeX auxiliary data.

The linked journal package reconstructs the primary, supplement, and structural article without a historical PDF, hidden source file, or repository checkout. Four compilation rounds and a standalone rebuild report no unresolved references or citations.

The conservation claim is therefore supported at the source and label level. Editorially, the package would benefit from a human-readable prerequisite map rather than relying only on the machine relocation inventory.

---

## 11. Build and workflow audit

### 11.1 Source qualification run

Run `37269000936` completed successfully. Its steps include:

1. checkout of the revision anchor and immutable predecessor;
2. retrieval of immutable r53 reports;
3. installation of pinned typesetting and exact-arithmetic dependencies;
4. expansion of the checked source delta and preservation verification;
5. commit of native source;
6. build of four manuscripts and 22 exact suites;
7. reconstruction of native and linked journal packages;
8. commit of qualified artifacts directly on the native-source parent;
9. read-only verification of the publication head; and
10. preservation of manuscripts and source-bound receipts.

The resulting native and publication commits are the SHAs stated above.

### 11.2 Exact-head run

Run `37269932771` checked out exact SHA `9ee14476...` and completed:

1. pinned dependency installation;
2. reconstruction of all four documents;
3. execution of exact regressions;
4. linked journal-package reconstruction; and
5. preservation of the exact-head receipt.

The run conclusion is `success`.

### 11.3 Build receipt

The committed receipt records:

```text
paper.pdf                 24 pages
BINARY_SUPPLEMENT.pdf     78 pages
STRUCTURAL_PAPER.pdf      41 pages
COMPLETE_REVISION.pdf    232 pages
regression_suites         22
isolated_native_rebuild   true
standalone_journal_rebuild true
normal_optimized_identical true
unresolved references/citations false.
```

### 11.4 Evidentiary boundary

These workflows establish reproducible identity of the submitted object. They do not establish:

- correctness of continuum proofs;
- historical novelty;
- independent journal merit;
- cryptographic authorship;
- physical implementation;
- efficient recovery synthesis; or
- completion of the wider Theta programme.

---

## 12. Priority and external-literature audit

The current manuscript correctly attributes:

- the Hamiltonian-not-in-Kraus-span channel-metrology criterion and error-correction attainability to Zhou–Jiang;
- exact quantum-error-correction conditions to Knill–Laflamme;
- adaptive discrimination/path antecedents to channel-extension work;
- fixed-state measurement Fisher/frame results to Saini–Kiukas–Burgarth–Gilchrist;
- operator-valued kernel embeddings to Mayer–Yun;
- tomography primitives to Mele–Bittel and Zambrano–Ramos-Calderer–Kueng; and
- known-symmetry learning to Yoshida–Okigami–Posta–Grinko.

The present mathematical novelty claim is narrower:

1. complete support-coordinate parameterization of the normalized-tuple covariance kernel;
2. exact identification of its unitary range with the measurement Kraus-product span;
3. a written direct finite-angle trace-distance lower with explicit accumulated error; and
4. transported scalar-covariance regularization.

Independent priority remains unresolved. The author-side literature audit states that the full text of arXiv:2609.39280 was unavailable. That statement is no longer current: the complete arXiv HTML is available. Its known-symmetry state/channel tomography theorems, parameter dimensions, query counts, and efficient Hayashi-measurement implementation should be compared directly. I did not identify an immediate statement there that subsumes the fixed-pair support trichotomy, but the comparison must be updated rather than left as unavailable.

A specialist priority review should also determine whether the support-kernel formula is already implicit in:

- semidefinite HNKS formulations;
- quotient-space descriptions of correctable channel tangents;
- operator-algebraic sufficiency or statistical experiment theory;
- measurement-frame geometry; or
- nonasymptotic channel-estimation corollaries.

No repository build can discharge this gate.

---

## 13. Independent whole-pipeline boundary

The finite-dimensional measurement paper inherits historical terminology from a much larger programme, but the active analytic dependency routes remain:

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The frozen ledger continues to distinguish:

- raw unsmoothed local limits;
- stopped-path recovery;
- global past kernels;
- exact shell conditioning;
- finite cumulants before covariance/CLT;
- process CLT;
- positive Mosco recovery;
- nonlinear Nisio graph cores;
- filtering/QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction.

The support kernel, finite-dimensional correction code, orbit trace comparison, and transported ridge prove none of these model-specific obligations. The five aggregate flags remaining false is the correct status.

---

## 14. Acceptance gates

### Mathematical gates

| Gate | Requirement | Audit status |
|---|---|---|
| M01 | Exact covariance variance identity active | **Pass.** Inherited Section 67 is active and unchanged. |
| M02 | Complete singular kernel | **Pass.** Section 69 gives a bijection and exact dimension. |
| M03 | No effect inversion at boundary | **Pass.** Support projections replace inverses. |
| M04 | Real-space dimension conventions | **Pass.** Hermitian real Hilbert spaces used consistently. |
| M05 | Range criterion from complete kernel | **Pass.** Pairing and finite-dimensional self-adjointness are explicit. |
| M06 | Comparison scale not confused with lower bound | **Pass.** Corollary 69 is followed by a separate operational proof. |
| M07 | Square-root lower valid locally | **Pass.** Nonzero first derivative and Bernoulli product argument. |
| M08 | Recovery uses accessible systems | **Pass.** Actual label plus retained reference only. |
| M09 | KL products complete | **Pass.** Full within-label support blocks and cross-label zeros included. |
| M10 | CPTP recovery completed globally | **Pass.** Orthogonal complement gets a fixed-state branch. |
| M11 | Finite-angle remainder explicit | **Pass.** One-use and m-use diamond bounds stated. |
| M12 | Integer-call bookkeeping | **Pass.** Small-angle cap and floor estimates check. |
| M13 | Nonuniform constants visible | **Pass with editorial repetition requested.** |
| M14 | Processing statement precise | **Pass.** Span inclusion; stationarization caveat should be explicit in prose. |
| M15 | Transported ridge not fixed-ridge overclaim | **Pass.** Same `tau`, transported weights, no refreshed uniform inference. |
| M16 | Exact arithmetic scope | **Pass.** Represented Gaussian-rational input and exact tests. |
| M17 | Arbitrary-pair boundary limitation | **Open by design.** No matching lower/equivalence. |
| M18 | Growing-`k` minimax | **Open.** Gap preserved. |

### Priority gates

| Gate | Requirement | Audit status |
|---|---|---|
| P01 | Independent specialist opinion | **Uncompleted.** No external priority clearance supplied. |
| P02 | HNKS/QEC attribution | **Pass.** Zhou–Jiang and Knill–Laflamme credited. |
| P03 | Exact novelty boundary | **Mostly pass.** Should be stated even more prominently after the main theorem. |
| P04 | Current covariant-learning comparison | **Needs update.** Full text is now available. |
| P05 | Fisher/frame distinction | **Pass.** Fixed-state versus varying-measurement models separated. |
| P06 | Operator-valued kernel distinction | **Pass.** Support-block span versus one-effect span is explicit. |
| P07 | No firstness inference from search | **Pass.** No historical-firstness claim. |

### Editorial gates

| Gate | Requirement | Audit status |
|---|---|---|
| E01 | Focused primary | **Pass.** 24-page current primary. |
| E02 | Complete current supplement | **Pass.** 78-page linked source package. |
| E03 | Structural article separate | **Pass.** Independent graph and PDF. |
| E04 | Archive not journal object | **Pass.** Complete edition labeled preservation. |
| E05 | Human-readable prerequisite map | **Needs improvement.** Machine relocation data are not enough for ordinary readers. |
| E06 | Pair discrimination separated from learning | **Pass.** Known-pair recovery explicitly scoped. |
| E07 | Resource distinctions centralized | **Pass.** Current ledger is clear. |
| E08 | Main theorem novelty phrasing | **Needs sharpening.** Known dichotomy versus new support/finite-angle formulation. |

### Reproducibility gates

| Gate | Requirement | Audit status |
|---|---|---|
| V01 | Exact native/publication/final chain | **Pass.** Direct commits pinned. |
| V02 | Current source qualification | **Pass.** Run `37269000936`. |
| V03 | Exact final-head read-only reconstruction | **Pass.** Run `37269932771`. |
| V04 | Four current documents reconstructed | **Pass.** Primary, supplement, structural, complete. |
| V05 | Current exact suites | **Pass.** 22 suites, normal/optimized agreement. |
| V06 | No unresolved references/citations | **Pass.** Current build receipt. |
| V07 | Finite-test scope flags | **Pass.** Continuum and physical execution denied. |
| V08 | Resource-cap rejection | **Pass.** No partial certificate. |
| V09 | Signature status | **Open.** No independently verified signature. |

---

## 15. Risk register

| Risk | Subject | Independent assessment |
|---|---|---|
| K01 | Known-principle novelty | The `sqrt(N)`/`N` exponent dichotomy and QEC mechanism are established channel-metrology principles. The new claim must remain the support-kernel and finite-angle specialization. |
| K02 | Full-boundary overstatement | “Complete body” applies to the upper and support formula, not an arbitrary-pair two-sided metric/entropy classification. |
| K03 | Nonuniform orbit constants | Constants can collapse near stationarity, span transitions, or small residual gap. No uniform stratum theorem is proved. |
| K04 | Pair-versus-common resources | The orbit tester knows `E,G`; it cannot be imported into unknown-device learning without charging that advice. |
| K05 | Ideal controls | Existence of recovery does not prove efficient or robust implementation. |
| K06 | Processing prose | Output processing may stationarize an orbit; only conversion from square-root to linear is excluded. |
| K07 | Linked-document opacity | Preservation is strong, but a 78-page supplement can obscure which inherited results are logically necessary. |
| K08 | Current literature | One “unavailable full text” statement is stale and must be corrected. |
| K09 | Computation overreach | Polynomial support classification is not adaptive-distance computation or control synthesis. |
| K10 | Regression overreach | Exact finite checks are not continuum proof or experiment. |
| K11 | Growing outcome | `k^3` versus binary lower remains visible and unresolved. |
| K12 | Wider programme | All A/B/C/D aggregate flags must remain false. |
| K13 | Signature | Reproducible SHA identity is not human cryptographic authorship. |
| K14 | Journal significance | Strong specialist contribution does not by itself establish top-four general-journal breadth. |

---

## 16. Required revisions recorded by this audit

1. Replace the statement that arXiv:2609.39280 full text is unavailable with a current theorem-level comparison.
2. Seek independent specialist priority assessment of the support-kernel formula and finite-angle corollary.
3. State immediately after the orbit theorem that the exponent/QEC dichotomy is established prior metrology; identify exactly what is newly proved here.
4. Repeat that the complete-body arbitrary-pair result remains an upper certificate.
5. Keep `E,G` dependence of constants and angle interval in all summaries.
6. Clarify that output processing may make a moving orbit stationary.
7. Add a compact main-text statement of the Bernoulli lower premise used by the square-root branch.
8. Add a human-readable primary/supplement dependency table.
9. Preserve pair-dependent known-control versus common unknown-device learning separation.
10. Preserve ideal-control, no-gate-complexity, and no-physical-execution qualifications.
11. Preserve exact represented-input versus general real-input distinctions.
12. Preserve transported-weight versus freshly uniform ridge distinctions.
13. Keep growing-`k`, full-boundary entropy, dictionary synthesis, and readout synthesis open.
14. Bind any successor to new source and exact-head receipts.
15. Keep all five wider-program aggregate flags false absent their independent proofs.

---

## 17. Final pipeline assessment

The v84 source, publication, and exact-head chain is coherent and reproducible. The new support-kernel and orbit arguments form a logically connected theorem package. I found no fatal flaw in the parameterization, range criterion, correction code, finite-angle trace estimate, or transported ridge in the submitted form.

The main remaining obstacles are not hidden implementation failures. They are:

- the distinction between a new support-coordinate formulation and an established metrological dichotomy;
- unresolved independent priority;
- lack of arbitrary-pair full-boundary lower geometry and entropy;
- lack of growing-outcome minimax sharpness;
- lack of general efficient dictionary, recovery, or readout synthesis; and
- specialist rather than broad general-mathematics reach.

**Pipeline classification:** mathematically coherent specialist-level revision; reproducibility passed; priority incomplete; independent analytic programme open; four-leading-general-journal threshold not met.
