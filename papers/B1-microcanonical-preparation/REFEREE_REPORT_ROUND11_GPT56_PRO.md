# Independent Referee Report — Round Eleven

**Manuscript:** B1 — Microcanonical Preparation  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/B1_DYNAMIC_BLOCK_CRAMER_SHELL.tex` (Git blob `6941f0e6e6bbca7aff2389306eec6aa1583bbcc4`)

## Executive assessment

The source-dependent finite saddle and the restriction to regular, CLT-wide shells are correct conceptual repairs. The central new input, however—the “dynamical regenerative block” theorem—is geometrically impossible in the stated Boltzmann–Grad setting. After the proposed velocity truncation, the propagation radius grows like \(\sqrt{\log\mu_arepsilon}\) in a fixed torus, so one cannot place \(c\mu_arepsilon\) mutually separated spatial blocks. The discarded high-velocity event is not exponentially small at speed \(\mu_arepsilon\). Consequently the full-frequency characteristic estimate and sharp shell coefficient have no proof.

## Major mathematical objections

### 1. The claimed number of separated blocks is impossible

The paper truncates at

\[
V_arepsilon=K\sqrt{\log\mu_arepsilon}
\]

and requires boxes of the same color to be separated by more than \(2TV_arepsilon\). The physical torus has fixed volume. As \(arepsilon\to0\), that separation tends to infinity (and eventually exceeds the torus diameter). The maximum number of such spatially separated boxes is therefore bounded, ultimately one—not \(c\mu_arepsilon\).

Adding velocity colors cannot restore spatial finite propagation: trajectories from velocity-distinct boxes still occupy the same physical region and can collide.

### 2. The high-velocity complement is not exponentially negligible at the LDP speed

Under a Maxwellian tail,

\[
\mathbb P(|v|>K\sqrt{\log\mu})
\asymp \mu^{-cK^2}.
\]

Among order-\(\mu\) particles, the probability that at least one particle exceeds the cutoff is polynomial or otherwise subexponential in \(\mu\), depending on \(K\). It is not \(e^{-c\mu}\). Thus it cannot be absorbed into the exponential remainder used in the characteristic theorem.

A cutoff large enough to make the complement exponentially small would have order \(\sqrt\mu\), making the propagation-radius obstruction still worse.

### 3. A global path/contact tilt does not yield conditional block minorization

The complete source depends on future particle paths and actual contacts. Conditioning on previously exposed colors changes the likelihood of a local block through all trajectories connecting it to the rest of the system. A convergent polymer expansion may bound correlations, but it does not supply a source-uniform positive Radon–Nikodym lower bound for \(c\mu\) sequential conditional block laws. This is the theorem to be proved, not a consequence of the words “polymer correction.”

### 4. The full-frequency estimate is therefore unsupported

The bounds

\[
e^{-c\mu_arepsilon}
\quad\text{and}\quad
(1+|u|)^{-sc\mu_arepsilon}
\]

come from multiplying contractions across linearly many blocks. Since those blocks have not been constructed, neither estimate follows. In particular, the large-frequency tail required for a relative local coefficient remains open.

### 5. The finite-volume mean-map theorem is not established globally

A local covariance lower bound gives local invertibility. It does not imply properness, outward-pointing boundary gradients, or degree one on a common multiplier domain. The proof states all three without constructing the domain or controlling the pressure near its boundary.

### 6. The shell notation and conclusion do not match

The theorem writes

\[
\sqrt{\mu_arepsilon}(Y-a)\in W_arepsilon
\]

while separately imposing conditions on a scalar \(\delta_arepsilon\) that is not tied to \(W_arepsilon\). A general bounded Lipschitz domain with subexponential Gaussian mass need not be centered or have Gaussian mass tending to one. The last sentence is valid only for explicitly centered expanding sets.

### 7. Relative error needs quantitative Fourier bounds at the shell scale

The condition

\[
\mathfrak g(W_arepsilon)\ge e^{-o(\mu_arepsilon)}
\]

is much weaker than a lower bound that dominates the actual Fourier remainder. A noncentral error of order \(e^{-c\mu}\) is harmless, but a merely polynomial or fixed-order integration-by-parts error may dominate a small shell mass. The proof does not compare the exponents or powers.

### 8. B1 remains downstream of an unproved B2 grand-canonical theorem

Even a correct coefficient argument would require the full source-uniform B2 pressure and derivative bounds. Those inputs are not established in the present revision.

## Status of earlier objections

The fixed zero-source saddle error is repaired, the frequency annulus omitted in round ten is explicitly recognized, and exponentially tiny arbitrary shells are excluded in principle. The new dynamic-block mechanism replacing the old argument is false at the most basic geometric scale.

## Minimum reconstruction

A valid proof must avoid spatial independence at a growing propagation radius. Possible routes would require a genuine dependency-graph/cluster Fourier theorem whose constants remain exponential in \(\mu\), or a direct complex-pressure coefficient theorem. The shell family must be defined precisely and its mass compared quantitatively with every Fourier remainder.

## Recommendation

**Reject.** The formula for the constrained pressure is plausible, but the full-frequency theorem and hence the microcanonical transfer are unsupported by an impossible block geometry.