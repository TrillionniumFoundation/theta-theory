# Independent Referee Report — Round Eleven

**Manuscript:** A4 — History, Memory, and Universal Pressure  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/A4_CENTERED_DOOB_RENEWAL_MEMORY.tex` (Git blob `f9751bd75649af54e51ac7cec2989c2e11e3779d`)

## Executive assessment

The Poisson martingale algebra and the eigenfunction Doob normalization are finally written correctly. This closes two direct round-ten errors. The remainder of the manuscript still does not follow. A path LDP does not imply the asserted one-step Lyapunov drift, Feller coupling, or spectral gap of the past kernel; the quenched enhanced invariance principle is reduced to a paragraph; and unspecified polynomial vertical resolvent bounds are promoted into an ordinary exponentially decaying memory kernel.

## Major mathematical objections

### 1. The past-kernel spectral gap is assumed rather than derived

The first theorem begins with “assume the spectral gap.” The next theorem's proof then says that the A3 recurrent–recession rate gives a Lyapunov inequality

\[
PW\le\rho W+C.
\]

A large-deviation rate does not imply a one-step drift inequality for a conditional history kernel. Nor does an exponential return tail by itself give a successful coupling of two conditional futures or a spectral gap on a weighted Hölder space. These are separate model-specific theorems.

The paper therefore lacks the analytic input needed even to guarantee convergence of the Poisson series on the stated history space.

### 2. The quenched rough invariance principle is not proved

Uniform convergence in the initial past requires, at minimum:

- conditional Lindeberg bounds;
- locally uniform convergence of predictable brackets;
- tightness of the roof interpolation;
- control of the coboundary on unbounded histories;
- convergence of second iterated integrals; and
- treatment of singularity/renewal residuals.

Invoking Feller coupling and “the ergodic theorem uniformly on compact history sets” does not prove these statements. Ordinary ergodic theorems are not uniform over all initial histories in a compact set without a quantitative mixing theorem.

### 3. A2 does not supply the claimed continuous-time meromorphic theorem

The renewal–resolvent theorem asserts a common strip, vertical estimates, finitely many principal parts, finitely many transmission zeros, and invertibility of a residual block. These do not follow merely by saying that the denominator is the A2 roof-twisted operator. Entrance operators, residual flights, graph domains, and the continuous-time renewal equation must be constructed and bounded.

Moreover, A2 itself has no valid complete high-frequency theorem in the current revision.

### 4. Polynomial vertical bounds do not imply an ordinary decaying kernel

After removing polynomial principal parts, the manuscript does not state a decay rate along vertical lines. A meromorphic function that is merely polynomially bounded can invert to a distribution, not to an ordinary function satisfying

\[
\|K(t)\|\le Ce^{-\gamma t}.
\]

A Bromwich contour shift requires vertical integrability, or sufficiently many integrable derivatives, uniformly on the shifted line. The proof supplies neither. Separating formal large-\(z\) polynomial terms is insufficient to control the residual inverse transform.

### 5. Finiteness of transmission zeros is unproved

A finite-dimensional analytic matrix can have infinitely many zeros in an unbounded strip. A Smith–McMillan factorization is local unless one first proves high-frequency invertibility and a finite zero count in the remaining compact region. The manuscript assumes precisely this conclusion.

### 6. Descriptor modes do not create a unique memory decomposition automatically

The number, state space, normalization, and coupling of the descriptor modes are unspecified. Different realizations can produce the same transfer function. The claimed unique decomposition into instantaneous distributions, resonant exponentials, and a regular kernel therefore needs a minimal-realization theorem and a normalization convention.

### 7. The rough-pressure convergence is entirely downstream of missing inputs

Passing Feynman–Kac eigenvalues/eigenfunctions through a rough scaling requires uniform operator perturbation, exponential integrability, and convergence of the conditional semigroups. The final proof simply cites the unproved quenched theorem and analytic perturbation.

## Status of earlier objections

The martingale difference

\[
D_{k+1}=h(H_{k+1})-Ph(H_k)
\]

with \(h=\sum_{j\ge0}P^jg\) is correct, and the Doob log semigroup is correctly normalized. The Feller/spectral, rough-limit, and memory-decay interfaces remain open.

## Minimum reconstruction

The authors should isolate and prove a weighted spectral/coupling theorem for the actual past kernel, then a separate quenched rough invariance principle. The memory part must state explicit vertical decay estimates and prove a genuine inverse-Laplace theorem after all distributional principal parts are removed.

## Recommendation

**Reject.** Two algebraic errors are repaired, but the Sinai-specific stochastic and memory theorems are still assumed rather than proved.