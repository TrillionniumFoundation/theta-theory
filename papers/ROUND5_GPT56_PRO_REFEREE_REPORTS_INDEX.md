# Round-Five GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Reviewed tree:** `608d7227adec8454462017b47d832730ebb5da09`  
**Review branch:** `review/round5-gpt56-pro-harsh-11paper-2026-08-31`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**

## Evidence boundary and source-control finding

This branch contains eleven proposed round-five final proof packets under:

```text
revision/round5-referee-final/
```

and a materializer intended to copy them into the eleven paper-level controlling modules. That materialization did not happen.

The eleven files actually read by the manuscripts remain the same `ROUND3_POSITIVE_CLOSURE.tex` blobs reviewed in round four. The complete `papers/` tree is unchanged at the controlling-source level. The new packets are therefore candidate repair text, not theorem text of the submitted manuscripts.

The fail-closed workflow run `33338718987` confirms this boundary. Its job `99330256232` failed at step:

```text
Materialize all eleven controlling manuscripts
```

with the exact diagnostic:

```text
revision/round5-referee-final/A1_RECUT_HAMILTONIAN_RESPONSE.tex:
ASCII controls [8]
```

All subsequent exact-source hostile gates, eleven-paper clean builds, undefined-reference checks, certificate generation, commit, and publication steps were skipped. A second control character is also present in the C2 candidate source. No round-five candidate has a clean materialized manuscript or publication certificate.

Each report therefore gives two separate verdicts:

1. the formal editorial verdict on the active controlling manuscript; and
2. a mathematical pre-review of the unmaterialized round-five candidate packet.

No build receipt, theorem/proof count, manifest, internal `PASS` label, or workflow intention is treated as theorem evidence.

## Editorial verdicts

| Paper | Recommendation | Decisive active/candidate finding | Status of prior objection |
|---|---|---|---|
| A1 — Exact Benchmarks | Reject | Active round-four mechanical construction remains; candidate work form equals the branch current only on port cores, not the full Liouville section, and the suspension/response proof is incomplete | Recut architecture improved, exact mechanical realization still open |
| A2 — Sinai Homological Pressure | Reject | Active false wide-window LLT remains; candidate assigns zero trace spaces at component births while demanding invertible maps to one fixed reference space, and still sketches Dolgopyat theory | Three-regime formula improved, bundle/spectral theorem open |
| A3 — Full Empirical-Path LDP | Reject | Active entropy approximation remains false; candidate’s ordinary finite-moment probability space cannot retain a nonzero macroscopic recession mass and its Markovization adds forbidden graph edges | One-big-excursion issue recognized, full lower bound open |
| A4 — History, Memory, Universal Pressure | Reject | Active memory/area defects remain; candidate falsely says the residual forcing is orthogonal at time zero and incorrectly infers a zero-free compressed resolvent from covariance positivity | Genuine Doob transform and area anomaly added, memory theorem open |
| B1 — Microcanonical Preparation | Reject | Active limiting-saddle coefficient remains; candidate uses the right finite saddle but inserts an unproved `m0` singleton block into the connected logarithm and lacks the uniform mixed LLT | Fixed-saddle counterexample conceptually closed, coefficient theorem open |
| B2 — Collision Clusters and Dynamic LDP | Reject | Active contact-deletion surgery remains; candidate boundary-flux ledger is directly false for `L1` densities concentrated near a collision boundary | Future is retained, but replacement ledger/Gramian theorem fails |
| B3 — Hamilton–Boltzmann Cotangents | Reject | Active gauge is ill typed; candidate’s bounded exponential charts cannot be scaled to detect singular currents or balance failure, and no actual-contact compensator exists | Weighted gauge/Radon architecture improved, global dual and CLT open |
| B4 — Nonlinear Kinetic Semigroups | Reject | Active hierarchy/state errors remain; candidate’s second-moment sublevel is not compact in the topology requiring second-moment convergence, and the BBGKY corrector remains formal | Law-state typing and bounded increments improved, HJ convergence open |
| C1 — Information and Saddles | Reject | Active control/filter theorem remains; candidate omits new-observation conditioning in its posterior update, assigns KL rather than Chernoff exponent to expected posterior error, and miscentres LAN | Posterior law state and block normalization improved |
| C2 — Cotangent Rigidity and Representations | Reject | Active prelimit Markov/Doob errors remain; candidate drops rate coercivity for weighted pressure and assumes an A4 conditional-kernel theorem that does not exist | Exact history martingale and formal Doob transform improved |
| D1 — Deterministic Theta Contractions | Reject; remove standalone paper | Active local/global dual error remains; candidate’s claimed exact likelihood is not mean one because the field is centered at `DQ` while the normalizer uses `DQ_epsilon`; P3 assumes the global lower-bound theorem | Exhausted source domain improved, standalone theorem still circular/false |

## Root-level mathematical findings

### 1. Round five is not a materialized revision of the eleven papers

The branch adds candidate packets and automation, but the controlling paper blobs do not change. The workflow fails on invalid source before applying any packet. Consequently every round-four rejection remains formally dispositive.

This is not an editorial technicality. A theorem can be reviewed only in the bytes included by the manuscript. Orphaned candidate text, however sophisticated, cannot close an active proof.

### 2. B2’s proposed boundary-flux ledger has a direct boundary-layer counterexample

For fixed `z>0`, choose an `L1` density concentrated in a layer of thickness `o(t)` immediately inside one regular incoming collision boundary. Almost every state collides before time `t`, so

\[
M_z(t,\rho)\approx e^z\|\rho\|_1.
\]

The candidate bound is

\[
M_z(t,\rho)
\le\|\rho\|_1
\exp\{Ckt(e^z-1)\},
\]

whose right side tends to `||rho||_1` as `t` tends to zero. This is impossible. Interior `L1` mass does not uniformly control collision-boundary trace.

The hard-sphere dependency chain remains blocked at B2-GC.

### 3. A2’s fixed all-depth bundle is internally inconsistent

At a radius where a labelled singular component is empty, the candidate assigns its trace coordinate the zero space. Across a birth it demands a boundedly invertible identification with one fixed reference Banach space. A nonzero summand cannot be uniformly isomorphic to zero. A genuine ambient distribution field or non-invertible bundle formalism is required.

The candidate correctly replaces the old wide-window factor by a Gaussian interval mass, but the formal LLT remains too broad for arbitrarily small windows and the Dolgopyat proof is still a programme.

### 4. A3 still lacks a recession-complete state space

A fixed positive mass moving to symbols with return level tending to infinity cannot converge as an ordinary probability with finite `W`-moment. Either the moment diverges or the escaping mass vanishes. The candidate therefore cannot retain a nonzero macroscopic recession fraction in its declared phase space.

Its finite-state Markov approximation also adds positive probability to zero transitions, which can create dynamically forbidden edges. Entropy/rate density is not proved.

### 5. A4’s memory-decay inference is invalid

Positive Green–Kubo covariance at zero frequency does not exclude complex zeros of the compressed correlation transform

\[
P(z-L)^{-1}P.
\]

Such zeros create poles in the inverse and in the memory transform. The candidate’s zero-free strip and exponential memory kernel do not follow from covariance positivity.

The candidate also claims the residual forcing is orthogonal at time zero, although it equals `PLQB`, a resolved vector.

### 6. B3’s analytic chart cannot produce the global entropy conjugate

The candidate permits

\[
\|z/w_c\|_\infty<\eta<\beta/8.
\]

The union of these charts is still bounded. Its proof then sends `z=n 1_K` and scaled balance tests to infinity. These sources leave the declared domain. Hence singular collision current and balance failure are not assigned infinite cost by the stated supremum.

The proposed process CLT also assumes a compensated actual-contact martingale which neither B2 nor B3 constructs.

### 7. B4’s compactness theorem is false

In the topology of weak convergence plus second-moment convergence, the set of measures with bounded second moment is not compact. For example,

\[
\mu_n=(1-n^{-2})\delta_0+n^{-2}\delta_n
\]

has second moment one and converges weakly to `delta_0`, whose second moment is zero. No subsequence converges in the declared topology. Higher-moment uniform integrability or a weaker topology is necessary.

### 8. C1 reintroduces two previously corrected errors

Expected posterior error is governed by testing/Chernoff information, not directed KL divergence. The candidate nevertheless uses KL in its expected posterior-mass theorem.

Its LAN score is

\[
\sqrt{\mu_\varepsilon}(X_\varepsilon-DQ(\theta_0)),
\]

while exact likelihood expansion requires `DQ_epsilon(theta0)`. No convergence rate removes the resulting deterministic shift.

### 9. C2 assumes conditional homogenization rather than proving it

Weak convergence of slow paths does not imply uniform convergence of conditional kernels or optional projections on history filtrations. The candidate invokes an A4 “conditional-kernel theorem” which is not in A4’s proposed packet. Its likelihood/Girsanov conclusion is therefore conditional on a missing quenched/stable limit theorem.

### 10. D1’s “exact” local likelihood is algebraically not exact

With

\[
Z_\varepsilon=\sqrt{\mu_\varepsilon}
(\mathcal X_\varepsilon-DQ(\Theta)),
\]

the candidate likelihood differs from the true finite-volume Radon–Nikodym density by

\[
\exp\left\{
\sqrt{\mu_\varepsilon}
\langle h,DQ_\varepsilon(\Theta)-DQ(\Theta)\rangle
\right\}.
\]

It need not have mean one. The field must be centered at the finite-volume mean.

## Genuine round-five improvements recognized

The review is hostile to invalid proof, not to revision itself.

- **A1:** introduces an explicit recutting idea and defines symbolic transfer operators.
- **A2:** recognizes local, central, and wide roof-window regimes.
- **A3:** abandons periodic measures as entropy approximants.
- **A4:** uses a genuine eigenfunction Doob transform and includes the rough-area anomaly.
- **B1:** moves conditioning to an exact finite-volume saddle.
- **B2:** retains the true future trajectory after the first surplus contact.
- **B3:** places `Delta p` and `psi` in a common weighted gauge space.
- **B4:** distinguishes law states from hierarchy coordinates and restricts collision increments.
- **C1:** identifies a posterior probability law as the exact information state.
- **C2:** defines finite likelihoods as exact history martingales.
- **D1:** introduces an exhausted source domain instead of evaluating a local pressure globally.

These are meaningful architectural corrections. They are candidate text only and, even as candidates, do not close the mathematical gates identified above.

## Dependency-propagation audit

```text
A1  independent benchmark

A2  -- unmaterialized/inconsistent spectral bundle --> A3 --> A4 --> C2
 |                                                    |          |
 +----------------------------------------------------+----------> D1

B2-GC -- false proposed contact ledger / unproved source pressure --> B1
   |                                                               |
   +----------------------------------------------------------> B2-MC
                                                                    |
                                                                    +--> B3
                                                                          |
                                                                          +--> B4
                                                                                |
                                                                                +--> C1/C2 --> D1
```

The hard-sphere series is blocked at B2-GC. The Sinai series is blocked at A2 and A3. No downstream synthesis can close those gates by importing their theorem labels.

## Recommended reconstruction order

1. **Fix repository materialization first.** Remove control bytes, materialize the exact candidate sources, compile them, and record immutable blobs before another review round.
2. **B2-GC:** replace the false arbitrary-`L1` contact ledger with estimates on the actual initial/tilted density class, including trace regularity and a proved genealogical transversality theorem.
3. **A2:** construct a coherent ambient all-depth distribution/trace space and a complete Dolgopyat proof; state the LLT in rigorously separated window regimes.
4. **A3:** add an explicit recession/defect coordinate and prove admissible entropy-preserving Markov approximation without adding forbidden edges.
5. **B1:** derive the mixed characteristic function from the compound-Poisson/hard-core expansion at the exact finite saddle.
6. **A4:** prove the history right-process/eigenfunction theorem and replace the invalid zero-free memory argument; retain the area correction.
7. **B3:** separate local analytic and global Radon dual domains, center finite fields exactly, and prove process tightness without assuming a contact compensator.
8. **B4:** choose a topology with compact Lyapunov sublevels, construct exact BBGKY perturbed tests, and keep comparison penalties inside the bounded-increment core.
9. **C1/C2:** prove controlled posterior kernels and conditional/stable homogenization before claiming filtering, Girsanov, or BSDE limits.
10. **D1:** remove the standalone paper and retain only correctly centered, explicitly conditional commutation lemmas in the eventual principal paper.

## Top-four assessment

No manuscript is suitable for submission to the four journals in the reviewed branch. A2, A3, and B2 still contain potentially important research problems; B1 now has the correct variational target. The remaining papers are benchmarks, abstract devices, or dependent synthesis papers whose model-specific inputs are not proved.

## Files added in this review

Each paper folder receives:

```text
REFEREE_REPORT_ROUND5_GPT56_PRO.md
```

The folders are:

- `papers/A1-exact-benchmarks/`
- `papers/A2-sinai-homological-pressure/`
- `papers/A3-full-empirical-path-ldp/`
- `papers/A4-history-memory-universal-pressure/`
- `papers/B1-microcanonical-preparation/`
- `papers/B2-collision-clusters-dynamic-ldp/`
- `papers/B3-hamilton-boltzmann-cotangents/`
- `papers/B4-nonlinear-kinetic-semigroups/`
- `papers/C1-information-risk-sensitive-saddles/`
- `papers/C2-cotangent-rigidity-tangent-representations/`
- `papers/D1-deterministic-theta-contractions/`

The series-level audit is this file:

```text
papers/ROUND5_GPT56_PRO_REFEREE_REPORTS_INDEX.md
```