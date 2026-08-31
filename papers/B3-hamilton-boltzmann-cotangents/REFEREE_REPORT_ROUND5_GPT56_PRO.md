# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents and Prepared Fluctuation Fields*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `4c76a34348f8207598b169879b0509ff8170a687`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/B3_WEIGHTED_GAUGE_RADON_GAUSSIAN.tex`, blob `ae6e291d9ec66c3cc7cc25bf86a8ae5a1db95949`

## Source-control verdict

The active B3 paper is unchanged from round four. Its gauge map is still ill typed because a quadratic collision increment is mapped into an unweighted `C_b` collision-source space, and its process Gaussian theorem lacks a valid tightness/compensator construction.

The round-five candidate places the increment and source in a common weighted space, which is the correct direction. It is not materialized. Its Fenchel theorem is inconsistent with its own bounded exponential chart, and its martingale/CLT argument again treats deterministic actual contacts as if a compensator had already been constructed.

## Audit of the proposed round-five replacement

### 1. The declared source charts cannot generate the full entropy dual

The candidate fixes a Maxwellian exponent `beta` and takes the union of charts

\[
\left\{z:\|z/w_c\|_\infty<\eta\right\},
\qquad \eta<\beta/8.
\]

The union is still bounded by `beta/8` in weighted norm. The proof of full Fenchel duality then performs two operations outside that domain:

- it scales a separating balance test without bound to make a nonzero defect cost infinite; and
- it takes `z=n 1_K` with `n` tending to infinity to detect a collision measure singular to `A_f`.

Neither family remains in any chart with `eta<beta/8` once `n` is large. The supremum over the declared domain therefore cannot equal `+infinity` on every singular or unbalanced pair, and it cannot recover the unrestricted relative entropy `ell(q)` for arbitrarily large density ratios.

The paper must distinguish a local analytic Hamiltonian chart from the larger lower-semicontinuous convex dual domain. It currently identifies them.

### 2. Weighted energy moments do not provide the stated exponential chart for arbitrary finite-action states

The proof says that Maxwellian moment sublevels supplied by B2 dominate `exp(eta w_c)`. B2’s proposed LDP state space is based on energy and collision entropy; a finite-energy density need not have a positive quadratic exponential moment. Thus the Hamiltonian is finite only on a much smaller exponential-tail class, not uniformly on all finite-action pairs used in the duality and LDP.

If the analytic chart is restricted to Maxwellian-biased regular phases, the global Radon duality must be proved separately by truncation, without claiming that every truncated source belongs to one common analytic neighborhood.

### 3. The cohomological-kernel proof begins from a false implication

The candidate argues that zero limiting speed-normalized variance makes the microscopic observable constant on every open regular phase configuration. This is false. A nontrivial coboundary has zero asymptotic variance while varying pointwise on open sets.

Deriving the complete kernel of a hard-sphere path covariance requires a genuine cohomology/closed-range theorem for the balance adjoint on the selected weighted spaces. Local variations of one free flight and one collision do not establish that theorem, nor do they prove that the range is closed.

### 4. No actual-contact compensator is constructed

The packet defines martingale parts from “the exact balance and the compensated actual-contact ledger.” B2’s candidate ledger is only a proposed exponential moment inequality; it does not construct a predictable compensator for the deterministic collision measure in any filtration.

Conditional on the complete initial microstate, the collision path is deterministic. In a coarser filtration a Doob–Meyer compensator may exist, but its intensity is the conditional law of future contacts and is not shown to equal `q A_f`. Without such a construction, the Burkholder, quadratic-variation, and bracket calculations are formal.

### 5. The fluctuation fields are centered at limiting means without a convergence rate

The candidate defines

\[
\zeta^\varepsilon=\sqrt{\mu_\varepsilon}(\pi^\varepsilon-f),
\qquad
\Xi^\varepsilon=\sqrt{\mu_\varepsilon}(\Gamma^\varepsilon-\Gamma).
\]

Here `f` and `Gamma` are limiting biased means. Analytic convergence gives convergence of finite-volume means, but not necessarily at rate `o(mu_epsilon^{-1/2})`. A deterministic drift may therefore survive or diverge under this centering. The exact central-limit field must first be centered at the finite-volume tilted expectations; replacement by the limit requires a separate rate theorem.

### 6. The Aldous–Mitoma estimates are unsupported

The fourth-moment bound

\[
C(h^2+h/\mu_\varepsilon)
\]

is obtained by assuming the collision count has predictable intensity of order `mu_epsilon h` and jumps of order `mu_epsilon^{-1/2}`. This is exactly the stochastic-contact structure that the deterministic microscopic theorem is supposed to derive. It does not follow from a constant-source exponential moment alone, especially uniformly at stopping times.

### 7. The Gaussian bracket is a formal derivative of the candidate Hamiltonian

The expressions

\[
\int q\,\Delta\phi\Delta\chi\,dA_f,
\qquad
\int q\,\psi\chi\,dA_f
\]

are natural Boltzmann collision-noise covariances. Differentiating a formal exponential Hamiltonian produces them. It does not prove convergence of deterministic hard-sphere likelihoods or martingale brackets. That conclusion depends on B2’s unproved all-contact source theorem and on the missing compensator/tightness result.

### 8. The microcanonical projection formula is downstream of B1/B2

The Schur-complement covariance is the right candidate, but B1’s shell coefficient and B2’s grand-canonical process theorem are not established. B3 cannot promote their formal combination into a proved process CLT.

## Genuine improvement

The candidate fixes the obvious source-space mismatch by placing `Delta p` and `psi` in the same weighted space, retains the full gauge `(r,-Delta r)`, and uses weighted-strict Radon tests rather than equivalence classes modulo `A_f`. These are substantive typing improvements. The global dual and Gaussian theorem remain invalid.

## Required reconstruction

The paper needs two separate dual domains: a local exponential-tail analytic chart and a global lower-semicontinuous Radon source class. It must prove the complete balance cohomology, center finite-volume fluctuation fields exactly, and construct the relevant conditional compensator or an alternative cumulant-based process-tightness argument that does not assume Poisson contact noise.

## Recommendation

**Reject.** The active source is still ill typed. The unmaterialized candidate repairs the ambient gauge space but its full entropy dual leaves the declared chart, its covariance-kernel proof is invalid, and its deterministic-to-Gaussian martingale theorem assumes the missing stochastic contact structure.