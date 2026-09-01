# Independent Referee Report — Round Sixteen

**Paper:** `B3 — Hamilton–Boltzmann Cotangents`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/B3-hamilton-boltzmann-cotangents`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/B3_OBSERVABILITY_MOSCO_GAUSSIAN.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate fixes the previous covariance normalization error. The isonormal noise is now taken on
\[
L^2(q_f A_f)
\]
with integrand \(\Delta p+\psi\), rather than multiplying the integrand by an additional \(\sqrt q\). Consequently the formal covariance is
\[
\int(\Delta p+\psi)(\Delta p'+\psi')\,q_f\,dA_f,
\]
not \(q_f^2A_f\). The module then asserts a quotient observability form, Mosco convergence, a process-level Gaussian limit, and a second-order expansion of the dynamic rate.

The normalization repair is correct. The Gaussian and second-order theorems are not proved by the supplied argument.

## Major objections

### 1. A formal quadratic Hamiltonian expansion is not a central limit theorem

The candidate expands the limiting tilted Hamiltonian to second order and identifies the expected covariance. That identifies a formal Hessian. It does not show that the finite-particle logarithmic moment generating functions admit a uniform expansion at fluctuation scale:
\[
\log \mathbf E e^{N^{-1/2}\langle \xi,Z_N\rangle}
 =\frac12\langle \xi,C\xi\rangle+o(1)
\]
uniformly on the test sets needed for tightness.

A CLT requires control of the third and higher cumulants, or an equivalent martingale/Lindeberg argument. The manuscript cites the B2 genealogy series but gives no cumulant estimate uniform in genealogy size, recollisions, time, or test-function norm. Pointwise convergence of the large-deviation Hamiltonian at order \(N\) does not determine fluctuations at order \(\sqrt N\).

### 2. Mosco convergence of the quotient forms is asserted, not demonstrated

The forms, reference measures, and null spaces vary with the density and with the Boltzmann–Grad parameter. To prove Mosco convergence one needs:

* one common ambient Hilbert space or explicit transport maps;
* a liminf inequality for every weakly convergent sequence;
* a recovery sequence for every point in the limiting quotient domain;
* control of the collision-invariant gauge and its projections;
* closedness and uniform coercivity on the quotient.

The candidate says these follow from dominated convergence of the B2 genealogy expansion. Dominated convergence of kernels is not a Mosco theorem. It does not supply domain convergence or the reverse recovery inequality. The changing null space makes this particularly serious.

### 3. The observability/closed-range theorem is missing

The claimed cotangent representation uses coercivity on the quotient and a closed-range statement for the collision divergence. The proof is a compactness-contradiction sketch that assumes every zero-energy limit is a collision invariant. No compact embedding, hypoelliptic estimate, or boundary control is established.

In the space-time hard-sphere setting, transport, contact traces, and conservation laws interact. The finite-dimensional list of collision invariants does not by itself imply a quantitative spectral gap for the full dynamic form. The closed-range conclusion needed later by C2 is therefore unavailable.

### 4. Nuclear-space tightness is not obtained from finite-dimensional convergence

The candidate states convergence in a distribution-valued path space and invokes a countable determining family. A Mitoma-type theorem still requires uniform tightness of all scalar projections and equicontinuity in a nuclear test space. No Sobolev indices, Hilbert–Schmidt embeddings, or uniform increment estimates are provided.

The contact component is supported on a singular collision manifold, so its covariance need not define a Radon Gaussian measure in the asserted topology without an explicit trace estimate. The manuscript does not calculate one.

### 5. The second-order rate expansion needs twice epi-differentiability

The statement that the dynamic action has quadratic expansion equal to the inverse covariance is not a consequence of the CLT, even if the CLT were proved. One must establish twice epi-differentiability of the entropy action under the balance and positivity constraints, identify the tangent cone, and show Mosco convergence of the rescaled rate functionals.

Near zeros of \(q_fA_f\) the entropy is not uniformly quadratic, and feasible perturbations may lie on the boundary of the positive cone. The candidate writes the pseudoinverse quadratic form but gives no lower and recovery bounds for the rescaled actions.

### 6. The proof depends on the unresolved B2 lower bound

The candidate uses the B2 “positive exposed recovery” to build form recovery sequences and fluctuation correctors. That recovery theorem is precisely what the B2 module fails to prove. Hence the present Mosco and second-order assertions are circularly dependent on an unavailable input.

## Genuine progress

The corrected Gaussian normalization is important and should be retained. It aligns the isonormal control measure with the desired covariance and removes a direct factor-\(q\) error. The candidate also correctly recognizes that quotienting by collision invariants and proving Mosco convergence are the right structural tasks.

Recognizing those tasks is not the same as proving them.

## Dependency and editorial significance

B3 is used as the Gaussian tangent and closed-range input for B4, C2, and D1. Those papers require an actual Radon process limit and an actual quotient coercivity theorem, not merely the formal Hessian of a Hamiltonian.

## Minimum requirements for a new submission

A new proof must provide:

1. uniform finite-particle cumulant or martingale estimates at \(\sqrt N\) scale;
2. a fixed ambient realization and full Mosco liminf/recovery proof;
3. a quantitative quotient coercivity/closed-range theorem;
4. explicit nuclear-space increment and trace estimates;
5. twice epi-differentiability of the constrained entropy action;
6. independence from the presently missing B2 positive recovery theorem, or a repaired B2 input.

## Verdict

**Reject.** The covariance is now normalized correctly, but the process CLT, Mosco convergence, observability, and second-order rate theorem remain formal assertions. These are the substance of the paper, not technical details.
