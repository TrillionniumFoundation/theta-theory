# Round-Three GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/round3-full-positive-closure-11paper-2026-08-30`  
**Reviewed commit:** `6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Reviewed base:** `main@970d88ae41faf601ae609d833b48288f213e5c5c`  
**Review standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**

## Scope of this review

This round reviews the materialized eleven-paper revision, not the preceding `main` tree. The branch is 57 commits ahead of the reviewed base and rewrites all eleven controlling manuscripts. Each `main.tex` now consists essentially of a preamble, abstract, and

```tex
\input{ROUND3_POSITIVE_CLOSURE.tex}
```

so the paper-level `ROUND3_POSITIVE_CLOSURE.tex` module is treated as the controlling mathematical text.

The revision records 11/11 successful LaTeX builds and 94/94 theorem-like environments paired with proof environments. Those checks receive no theorem credit beyond confirming that the files compile and have the expected structural markers.

## Repository-level materialization failure

The branch’s own hostile audit identified seven load-bearing defects and prescribed replacements. Eight repair files were then added under:

```text
revision/round3-rereview/A2_UNIFORM_GEOMETRY.tex
revision/round3-rereview/A2_TEMPORAL_PACKET.tex
revision/round3-rereview/A3_DIRECT_PATH_LDP.tex
revision/round3-rereview/A4_RAY_FELLER.tex
revision/round3-rereview/B1_B3_NULLSPACE_PACKET.tex
revision/round3-rereview/B2_GLOBAL_SOURCE_LDP.tex
revision/round3-rereview/C1_BLOCK_NORMALIZED_CONTROL.tex
revision/round3-rereview/C2_STRICT_MEMORY.tex
```

None of these files is input by the eleven controlling `main.tex` files. Several active closure modules still contain the exact statements that the internal audit declared false or ill typed. In particular:

- A3 still claims a superexponential long-excursion truncation under an exponential return tail;
- A4 still claims uniform-norm strong continuity for every Ray realization;
- B2 still derives a full entropy action from a fixed small source ball;
- C1 still uses a Poisson-compensator likelihood for deterministic contacts; and
- C2 still contains the ill-typed memory derivative and unnormalized generator.

The revision status itself leaves the exact-commit harsh rereview and `main` update as `PENDING`. The present external-style review confirms that the publication gate must remain closed.

## Editorial verdicts

| Paper | Recommendation | Decisive round-three finding | Status of prior blocker |
|---|---|---|---|
| A1 — Exact Benchmarks | Reject | The proposed baker branch is not a well-defined symplectomorphism of the announced `T²`; `qp` is not a global torus Hamiltonian | Symbolic typing improved; mechanical claim still invalid |
| A2 — Sinai Homological Pressure | Reject | Geometry/UNI repairs are orphaned; controlling proof lacks the moving-singularity and Dolgopyat estimates and has the roof-sign error | Target theorem correctly identified; proof open |
| A3 — Full Empirical-Path LDP | Reject | One-big-excursion counterexample directly falsifies the superexponential mark truncation and pure ratio rate | Central theorem still false in active source |
| A4 — History, Memory, Universal Pressure | Reject | General Ray theorem uses the wrong topology; normalized Feynman–Kac log transform does not satisfy the claimed tower | `QLQ` issue improved; new exact tower error |
| B1 — Microcanonical Preparation | Reject | Source-dependent saddle is correct, but the safe-box lattice gap is too weak by one power of `epsilon`; coefficient theorem unproved | Former counterexample conceptually closed |
| B2 — Collision Clusters and Dynamic LDP | Reject | First-cycle sketch does not control all recollisions; a small source ball cannot dualize to the full entropy action | Orientation/circularity improved; main theorem open |
| B3 — Hamilton–Boltzmann Cotangents | Reject | Orlicz source space cannot see measures singular to `A_f`; covariance nullspace and process CLT unproved | Full representation gauge conceptually fixed |
| B4 — Nonlinear Kinetic Semigroups | Reject | Positive exponential source in `|v|^m`, `m>6`, diverges under Gaussian tails; collisions do not conserve that moment | Exact-state architecture improved; analytic framework false |
| C1 — Information and Saddles | Reject | Adaptive finite-volume density uses a nonexistent Poisson compensator; posterior expected-error exponent is wrong | Three game timings correctly separated |
| C2 — Cotangent Rigidity and Representations | Reject | Platform labels are fixed, but likelihood filtration convergence and memory typing remain unproved; repair file is orphaned | Category error closed; theorem still conditional |
| D1 — Deterministic Theta Contractions | Reject; remove standalone | Constrained dual omits the constrained minimum; “likelihood ratio” is not mean one and Gaussian field is centered at the wrong finite-volume mean | `mu Cov` normalization fixed; new theorem false |

## Root-level mathematical findings

### 1. A3’s long-excursion estimate is false

With an exponential return tail, one block of length `epsilon N` has probability of order `exp(-c epsilon N)`. Hence

```text
lim_L limsup_N N^{-1} log P(N^{-1} sum r_j 1_{r_j>L} > epsilon)
```

is finite, not `-infinity`. An ordinary empirical block measure can lose a macroscopic excursion. The collision-time rate needs a direct pressure or defect/escape completion; the orphaned `A3_DIRECT_PATH_LDP.tex` recognizes this but is not part of the paper.

### 2. A4’s normalized Feynman–Kac tower is algebraically false

For

\[
\mathcal E_tF=\log P_t(e^F)-\log P_t1,
\]

one has

\[
\mathcal E_s(\mathcal E_tF)
=
\log P_s\left(P_t(e^F)/P_t1\right)-\log P_s1,
\]

which is not `mathcal E_{s+t}F` when `P_t1` depends on the state. A Doob transform or a two-parameter conditional normalization is required.

### 3. B1’s particle-number gap has the wrong scale

At activity `mu_epsilon=epsilon^{-2}`, a cube of volume `O(epsilon^3)` has one-particle activity `O(epsilon)`, not order one. The proof uses only order `mu_epsilon` safe cubes and therefore obtains at best `exp(-c epsilon^{-1})`, not the required `exp(-c mu_epsilon)`. The mixed lattice/continuous shell coefficient is unproved.

### 4. B2 cannot obtain a global LDP from one local source chart

The exposing source for collision density `q` is `log q` modulo gauge. Finite-action approximations require arbitrarily large bounded sources. Normal convergence for `||psi|| <= r0` gives only a local exposed family, not the full Poisson entropy. The real-source continuation and balance-preserving regularization were placed in an orphaned file.

### 5. B3’s declared dual pair is inconsistent with singular measures

An exponential Orlicz heart relative to `A_f` identifies functions modulo `A_f`-null sets. It cannot be paired with a collision measure singular to `A_f`; the proof’s test `n 1_B` is the zero Orlicz element when `A_f(B)=0`. Thus the claimed `+infinity` singular branch of the conjugate is not available.

### 6. B4’s containment weight is nonintegrable

For `m>2` and every positive `delta`,

\[
\int e^{\delta|v|^m}e^{-\beta|v|^2}dv=\infty.
\]

The positive source used for exponential compact containment at `m>6` therefore does not exist. Moreover elastic collisions conserve the quadratic energy, not `|v|^m`. The viscosity comparison framework collapses at its Lyapunov step.

### 7. C1’s controlled contact likelihood is not normalized

Microscopic contacts are deterministic conditional on the initial state. The process does not have predictable compensator `A_{pi^epsilon}`. Therefore

\[
\exp\{\sum_c\log q(c)-\mu\int(q-1)dA_{\pi^\epsilon}\}
\]

is not an exact finite-volume Radon–Nikodym derivative. The internal block-normalized replacement is not included.

### 8. D1’s local likelihood theorem is false under its hypotheses

The exact local tilt must be centered at `DQ_epsilon(Theta)`. The paper centers at `DQ(Theta)` while normalizing with the finite derivative. Its displayed density differs from the exact mean-one likelihood by

\[
\exp\{\sqrt\mu\,h(DQ_\epsilon-DQ)\}.
\]

Local holomorphic convergence gives no `o(mu^{-1/2})` rate. The factor can diverge, and the Gaussian field centered at the limiting mean can drift.

## Series-wide standalone-source defect

The old theorem bodies were removed, but the new closure modules frequently use symbols and state spaces defined only in superseded drafts. LaTeX accepts mathematically undefined notation. A top-journal manuscript must define every controlling model, observable, topology, source norm, and imported theorem in the active source or through precise, stable cross-paper references.

## Dependency propagation

```text
A1  independent benchmark, but Hamiltonian realization invalid

A2  unproved vector/roof packet
 |
 +--> A3  false active path-LDP proof
       |
       +--> A4  false normalized tower / conditional memory claims
       |     |
       |     +--> C2 / D1
       +--------> C2 / D1

B2-GC  unproved all-contact/global-source theorem
 |
 +--> B1  source-dependent formula correct, coefficient theorem open
       |
       +--> B2-MC
             |
             +--> B3  dual/CLT open
                   |
                   +--> B4  invalid containment/comparison
                         |
                         +--> C1 / C2 / D1
```

No downstream synthesis, manifest, compiler, build receipt, or theorem/proof counter closes an upstream mathematical gap.

## Improvements that should be preserved

This review is not a claim that the revision made no progress. It records the following genuine advances:

- A1 uses a common symbolic path space and separates calibration from preference axioms.
- A2 targets the correct vector/roof spectral and local-limit theorem.
- A3 recognizes singularity shielding, deterministic clocks, and a closed coboundary span.
- A4 replaces formal orthogonal dynamics by a compressed-resolvent idea.
- B1 adopts the correct source-dependent constrained saddle.
- B2 fixes contact orientation and the grand-canonical/microcanonical construction order.
- B3 adopts the complete balance gauge and correct Hessian normalization.
- B4 retains the full hierarchy as the finite state and constructs a candidate action semigroup.
- C1 separates three distinct control games.
- C2 introduces platform labels.
- D1 records the correct speed-normalized covariance.

These are architectural corrections, not completed proofs.

## Recommended reconstruction order

1. **Fix the materialization contract.** No publication status should be generated from orphaned repair packets. The exact controlling modules must be the files reviewed and built.
2. **A1:** either construct the impact system on a correct cut/disjoint-port symplectic manifold or demote the paper to a symbolic benchmark.
3. **A2:** produce a standalone parameter-uniform anisotropic/UNI/local-limit paper with complete estimates and correct clock signs.
4. **A3:** abandon the false superexponential truncation and prove a direct defect-completed collision pressure/LDP before physical-time contraction.
5. **B2-GC:** prove the all-contact graph surgery and real-source continuation on every bounded source set.
6. **B1:** prove the mixed lattice/continuous shell coefficient with correctly scaled insertion regions.
7. **B2-MC/B3:** establish the microcanonical joint rate, a dual pair that sees singular collision measures, and a separate process CLT.
8. **B4:** choose Gaussian-compatible weights, construct the hierarchy correctors, and prove comparison on a valid compact-containment topology.
9. **C1:** install exact block-normalized feedback laws and formulate posterior rates through testing/LAN theory.
10. **C2:** select one fixed-platform representation theorem and prove stable filtration/Doob-memory convergence.
11. **D1:** retain only as a final theorem section after the upstream chain is valid, with corrected constrained constants and finite-mean centering.

## Files added by this review

Each paper folder receives:

```text
REFEREE_REPORT_ROUND3_GPT56_PRO.md
```

The series-level index is:

```text
papers/ROUND3_GPT56_PRO_REFEREE_REPORTS_INDEX.md
```

No manuscript source, bibliography, internal audit, or prior referee report is modified by the review commit.