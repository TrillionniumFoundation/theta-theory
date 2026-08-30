# Round-Four GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed branch:** `revision/round4-referee-positive-closure-11paper-2026-08-30`  
**Reviewed commit:** `cbee394d6ee33db471b63420131314bd05909a0f`  
**Reviewed tree:** `eec24bdce1a672a4049dbb0f1a61547ce0145793`  
**Review branch:** `review/round4-gpt56-pro-harsh-11paper-2026-08-31`  
**Standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**

## Scope and evidence boundary

This review concerns the materialized round-four revision, which is substantially different from the preceding `main` tree and from the round-three revision. All eleven controlling manuscripts retain a short `main.tex` which inputs the paper-level `ROUND3_POSITIVE_CLOSURE.tex`; the latter file is therefore treated as the controlling mathematical text.

The repository records:

- 11/11 clean LaTeX builds;
- 113/113 theorem-like environments paired with proof environments;
- a structural verifier marked `PASS`; and
- an internal dependency-aware hostile rereview marked `PASS`.

Those facts confirm source materialization and compilation. They do not certify that the arguments prove the stated theorems. This review gives no theorem credit to build success, marker counts, manifests, or internal status labels.

Unlike the previous revision, the round-four repair packets have largely been incorporated into the controlling modules. The principal problem is no longer orphaned proof text. The active proofs themselves contain new mathematical errors and unresolved interfaces.

## Editorial verdicts

| Paper | Recommendation | Decisive round-four finding | Status of the prior principal objection |
|---|---|---|---|
| A1 — Exact Benchmarks | Reject | The cut-port map has incompatible incoming/outgoing boundaries in the proposed mapping torus; the work one-form does not descend; response operators are undefined | Torus `qp` obstruction and common-path typing improved, mechanical realization still invalid |
| A2 — Sinai Homological Pressure | Reject | The LLT is false for the stated full `b_n=o(n)` range: windows wider than `sqrt(n)` must saturate rather than remain linear in `b_n`; moving-cut and Dolgopyat proofs remain sketches | Roof sign and moving-cut bookkeeping improved, main packet open |
| A3 — Full Empirical-Path LDP | Reject | The survivor-pressure lower bound uses periodic orbit measures to approximate positive-entropy laws with rate convergence, which is impossible; survivor spectral theory is unproved | One-big-excursion obstruction recognized, replacement theorem not proved |
| A4 — History, Memory, Universal Pressure | Reject | Memory decay is assumed through a meromorphic decomposition; the rough limit omits the generally nonzero deterministic area anomaly; history Doob eigenfunction interface is unproved | State-dependent tower and `QLQ` errors improved, model-specific theorem open |
| B1 — Microcanonical Preparation | Reject | The shell LLT is centered at the limiting saddle `lambda_H`, not the finite saddle `lambda_{H,epsilon}`; no rate keeps the finite mean in the local window | Fixed-saddle counterexample conceptually closed, coefficient extraction open |
| B2 — Collision Clusters and Dynamic LDP | Reject | Uniform ancestral transversality is not proved; deleting a recollision changes the entire future trajectory; source continuation time shrinks with source size and cannot yield the full fixed-horizon entropy action | Orientation and dependency order fixed, all-contact theorem open |
| B3 — Hamilton--Boltzmann Cotangents | Reject | The gauge map is ill typed: `Delta p` may have quadratic growth while the codomain is `C_b`; covariance nullspace and process tightness are unproved | Full gauge and Radon singular-current detection improved |
| B4 — Nonlinear Kinetic Semigroups | Reject | The declared linear hierarchy functionals are not an algebra; the exact tower mixes deterministic law states with random states; energy alone does not control `exp(Delta p)` | High-degree nonintegrable Lyapunov source corrected, HJ framework still invalid |
| C1 — Information and Saddles | Reject | The random conditional hierarchy state is not constructed; continuous posterior odds `rho(dz)/rho(dz0)` are undefined; LAN is overclaimed beyond a canonical exponential chart | Three game timings and block normalization corrected |
| C2 — Cotangent Rigidity and Representations | Reject | The finite slow coordinate is falsely treated as Markov; finite likelihoods need not be martingales; statewise Feynman--Kac normalization is again confused with a Doob transform | Platform labels/coercive source domain fixed, representation theorems false |
| D1 — Deterministic Theta Contractions | Reject; remove standalone paper | Local holomorphic pressure is used as a global dual over all sources; the full LDP and exposed-density theorem are assumed in H2; process conclusions import broken interfaces | `mu Cov`, finite centering, and normalization constants fixed |

## Root-level mathematical findings

### 1. A2's local-limit theorem has an elementary wide-window contradiction

The theorem permits

\[
b_n\to\infty,\qquad b_n=o(n),
\]

and claims a leading factor proportional to

\[
2b_n n^{-3/2}
\]

for two lattice displacement coordinates and one continuous roof coordinate. If

\[
b_n=n^{3/4},
\]

the roof window contains asymptotically all of the central Gaussian roof mass. The joint event is then of order `n^{-1}` from the two-dimensional lattice local limit, not `n^{-3/4}`. The formula is only plausible in a genuinely local regime such as `b_n=o(sqrt(n))`; wider regimes require the Gaussian interval probability itself.

This directly invalidates A2's ratio conditioning and every downstream use of that theorem.

### 2. A3's exposed-phase approximation cannot preserve entropy

The zero-magnet-frequency branch is handled by periodic orbit approximation in finite survivor systems, with a claim that entropy plus potential cost converges. Periodic orbit measures have entropy zero. They cannot rate-approximate a positive-entropy invariant survivor law by this argument.

Since the full LDP lower bound is proved only at unique exposed phases and extended using this false rate-density lemma, the global lower bound is missing.

### 3. B1 uses the limiting saddle where a finite-volume saddle is required

The source-dependent candidate pressure is correct, but coefficient extraction under the `lambda_H`-tilted finite system is centered at

\[
D_\lambda Q_\varepsilon(H,\lambda_H),
\]

not at the target

\[
D_\lambda Q(H,\lambda_H)=a.
\]

Derivative convergence without a quantitative rate does not imply that the mismatch is `o(mu_epsilon^{-1/2})` or smaller than the continuous shell width. The claimed uniform exact-number coefficient may therefore acquire a moderate-deviation penalty.

The proof must use a finite saddle `lambda_{H,epsilon}` or establish an explicit convergence rate.

### 4. B2's recollision surgery is incompatible with deterministic dynamics

The proposed ledger “forgets” later recollisions after the first cycle and identifies adjacent chronological cells. Removing a hard-sphere collision changes the outgoing velocities and every subsequent collision involving the affected particles. It is not a bounded-multiplicity map to the same future creation forest.

The claimed exponential generating bound for all later contacts therefore does not follow. The uniform first-cycle power also requires a quantitative transversality theorem for infinitely many composed ancestral minors; finitely many local variable types do not provide a uniform Łojasiewicz exponent.

### 5. B3's complete gauge is still not typed

The graph space allows

\[
|\Delta p|\lesssim 1+|v|^2+|v_*|^2,
\]

while the source and codomain of the gauge complex are `C_b`. Thus

\[
\mathfrak D(p,\psi)=\Delta p+\psi
\]

need not be bounded, and

\[
\mathfrak G r=(r,-\Delta r)
\]

need not belong to the declared product space. The exact sequence cannot be true as a sequence of those spaces.

### 6. B4's energy topology is incompatible with its exponential Hamiltonian

A uniform second-moment bound controls integrals of subquadratic functions, but not their exponentials. There are finite-energy probability densities for which

\[
\int e^{c|v|^{2-\delta}}f(dv)=\infty.
\]

Therefore a cotangent with subquadratic `Delta p` can make

\[
\int ff_*B(e^{\Delta p+\psi}-1)
\]

infinite. The Hamiltonian continuity lemma and comparison theorem fail on the declared energy state space unless cotangents are bounded or stronger velocity tails are imposed.

### 7. C2 reintroduces two algebraic/category errors

First, the prelimit slow coordinate `X^epsilon` is generally not Markov; A4 explicitly says the exact state is complete history. Hence

\[
E[F(X_T^\varepsilon)\mid\mathcal G_t^\varepsilon]
=P_{t,T}^\varepsilon F(X_t^\varepsilon)
\]

is false without a new sufficient-statistic theorem.

Second,

\[
D\left(\log P_t(e^F)-\log P_t1\right)_{F=0}A
=\frac{P_tA}{P_t1},
\]

not the Doob transform

\[
e^{-\lambda t}h^{-1}P_t(hA).
\]

Thus the finite likelihood process and the memory-pressure identity are not established.

### 8. D1 uses a local pressure as though it were global

H1 gives `Q` only on a local ball, but the theorem writes

\[
I(x)=\sup_{\Theta\in X}
\{\langle\Theta,x\rangle-Q(\Theta)+Q(0)\}.
\]

A local analytic cumulant cannot determine the global rate. H2 then assumes the full good LDP and rate-dense exposed points—the hard model theorem—so D1 is a conditional packaging lemma rather than an independent closure result.

## Genuine improvements recognized

This review is harsh but not revision-blind.

### A1

The paper no longer claims that `qp` is a global Hamiltonian on a torus. It places the Bernoulli laws on one common symbolic path space and makes the valuation coefficient conditional on a canonical-cocycle axiom.

### A2

The roof sign is corrected, and the manuscript attempts to represent moving singularity derivatives by explicit current coordinates and to construct a temporal UNI packet.

### A3

The paper correctly abandons the false superexponential truncation of one macroscopic return excursion and introduces a survivor/escape pressure branch.

### A4

The finite-dimensional Volterra memory construction is a useful domain-safe device. The nonlinear tower is now written using a genuine Doob transform rather than subtracting `log P_t1` inside a later semigroup.

### B1

The fixed zero-source saddle has been replaced by the correct source-dependent variational formula, and the old time-zero counterexample is no longer an objection to the active candidate formula.

### B2

Collision orientation and the exchange quotient are corrected, and the logical order `B2-GC -> B1 -> B2-MC` removes the earlier circularity.

### B3

The full balance gauge is recognized, and continuous Radon tests can now detect collision measures singular to `A_f`.

### B4

The invalid high-degree exponential velocity source is removed; exact quadratic energy is used as the Lyapunov quantity.

### C1

The three control timings are separated, and the adaptive finite-volume law uses exact conditional block normalizers instead of a fictitious Poisson compensator.

### C2

Physical platforms are explicitly labelled, and pressure is restricted to a coercive weighted source domain.

### D1

The finite-volume Hessian, constrained normalization constant, and finite-volume likelihood centering are corrected.

These are real improvements, but they do not close the active headline theorems.

## Dependency propagation

```text
A1  independent benchmark

A2  -- invalid/unproved LLT and spectral packet --> A3 --> A4 --> C2
 |                                                |          |
 +------------------------------------------------+----------> D1 comparisons

B2-GC -- unproved all-contact expansion/source continuation --> B1
   |                                                       |
   +--------------------------------------------------> B2-MC
                                                            |
                                                            +--> B3 --> B4
                                                                       |
                                                                       +--> C1/C2 --> D1
```

The hard-sphere chain remains blocked at B2-GC. B1's candidate saddle is mathematically better, but its proof still uses the B2 pressure and an unproved shell coefficient. Every downstream kinetic theorem remains conditional.

## Recommended reconstruction order

1. **A2:** correct the LLT statement by separating local (`b_n=o(sqrt n)`), central, and wide-window regimes; then supply the complete moving-cut/Dolgopyat proof.
2. **A3:** build a genuine survivor/open-system spectral theorem and an entropy/rate-dense lower-bound approximation; do not use periodic measures to approximate positive entropy.
3. **B2:** prove one narrowly scoped actual-contact marked cumulant theorem with a rigorous recollision surgery before claiming a full LDP.
4. **B1:** condition at the exact finite-volume saddle and prove a mixed lattice/nonlattice local limit under explicit hypotheses.
5. **B3:** choose compatible weighted source spaces for `Delta p+psi`, and prove the covariance cohomology and process tightness theorem.
6. **B4:** define the exact nonlinear state on microscopic histories/laws, restrict the HJ core to a domain on which the exponential Hamiltonian is finite, and then prove comparison.
7. **C1/C2:** retain history/posterior states at finite scale and prove optional-projection convergence before writing Markov likelihood diagrams.
8. **D1:** merge the correct finite-dimensional normalization and Schur-complement lemmas into the eventual principal hard-sphere paper; remove the standalone closure manuscript.
9. **A1/A4 abstract portions:** publish, if desired, as benchmark or methods notes after their global constructions and domains are corrected.

## Top-four assessment

No manuscript is currently suitable for submission to the four journals under the stated standard. A2, A3, and B2 contain potentially significant research problems, but their central model-specific theorems remain open. B1 now contains the correct variational candidate and could become a serious preparation theorem after finite-volume coefficient extraction. The other papers are dependent syntheses, abstract devices, or benchmark calculations whose independent novelty is insufficient in their present form.

## Files added in this review

Each paper folder receives:

```text
REFEREE_REPORT_ROUND4_GPT56_PRO.md
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
papers/ROUND4_GPT56_PRO_REFEREE_REPORTS_INDEX.md
```
