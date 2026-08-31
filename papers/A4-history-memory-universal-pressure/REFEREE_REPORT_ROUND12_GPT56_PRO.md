# Independent Referee Report — Round 12

**Manuscript:** A4 — *History, Memory, and Universal Pressure*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `e5745998473c30200de353ba9d64642b1e7de1f1ce159976df94970b946f8de0`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 correctly repairs the Poisson martingale algebra, uses an eigenfunction Doob transform rather than a statewise Feynman–Kac quotient, and keeps instantaneous distributions separate from an ordinary memory kernel. Those are substantive improvements.

The first theorem of the new paper is nevertheless impossible on the declared complete-past state space. A finite number of forward transitions appends new excursions but leaves the remote past as a deterministic tail. Transition laws from two different remote pasts therefore have disjoint supports in those tail coordinates. No common nonzero Doeblin minorizing measure can be dominated by both. The displayed Harris–Doeblin theorem and the proof of the weighted spectral gap are thus false as stated. The Feynman–Kac eigenpair and memory theorem are then built on an unavailable spectral interface, and the latter also inherits A2's invalid high-frequency estimate.

## Decisive objections

### 1. Doeblin minorization is impossible on a complete-past history state

Let

\[
H=(\ldots,A_{-2},A_{-1},A_0)
\]

and let one transition append a new excursion. After \(m\) transitions, the coordinates older than the newest \(m\) entries are still the shifted deterministic tail of \(H\). Thus the support of \(P^m(H,\cdot)\) is contained in

\[
\{H':H'_{-(m+j)}=A_{-j}\text{ for every }j\ge1\}.
\]

If \(H\) and \(\widetilde H\) differ in any remote-past coordinate, these support sets are disjoint. Consequently there is no nonzero probability \(\nu_K\) such that

\[
P^m(H,\cdot)\ge\epsilon\nu_K(\cdot)
\]

for all \(H\) in a small set containing more than one remote tail.

Downweighting remote coordinates in the topology does not change this measure-theoretic support obstruction. One may obtain Wasserstein/Hölder contraction because the deterministic tail becomes less important, but not a Doeblin minorization on the full history sigma-field.

### 2. The Harris proof therefore does not establish the claimed spectral gap

The proof says that a connector word gives a common terminal cylinder. It randomizes the newest coordinates only. It does not erase the old infinite tail. Standard Harris total-variation theory cannot be applied to this state without quotienting the remote tail or changing the distance/coupling theorem.

A spectral gap on dynamically Hölder functions may still be provable through a transfer-operator or coupling argument, but that is a different theorem. The present conclusion

\[
\|P^nf-\pi(f)\|_{W,\alpha}
\le C\rho^n\|f\|_{W,\alpha}
\]

is not derived from the displayed drift/minorization statement.

### 3. The Feynman–Kac eigenpair is not supplied by the Harris theorem

The paper next takes an arbitrary bounded potential \(V\) and invokes a simple leading eigenpair

\[
(e^{t\lambda_V},h_V)
\]

“from Theorem 2.1.” That theorem concerns the untwisted Markov kernel. Even geometric ergodicity of \(P\) does not give a simple isolated Feynman–Kac eigenvalue for every bounded potential. One needs a declared small source chart and a quasi-compact perturbation theorem, with control of positivity and the weighted domain.

The Doob algebra is correct once such eigen-data exist; the manuscript has not proved their existence on the stated class.

### 4. The renewal-resolvent strip depends on A2's false high-frequency theorem

A4 claims that A2 yields integrable vertical bounds for \((I-\mathcal L_{V,z})^{-1}\). In Round 12, A2's very-high-frequency estimate contains a constant \(Ce^{-cn}\) on an infinite frequency interval, whose Fourier integral diverges. It therefore cannot imply the \(O((1+|\Im z|)^{-1-\delta})\) residual bound asserted here.

The entrance/terminal-flight integrations may gain powers of \(|\Im z|^{-1}\) for their own factors, but they do not automatically regularize the constant bad-family term inside the return resolvent.

### 5. The transmission-zero decomposition omits higher-order zero structure

The theorem assumes only finitely many zeros, not that they are simple. If the compressed transfer function has a zero of order \(k>1\), then \(C_V(z)^{-1}\) has a pole of order \(k\), whose inverse Laplace transform contains

\[
t^{j}e^{\zeta t},\qquad 0\le j<k,
\]

not merely a term \(e^{\zeta t}P\). The displayed memory decomposition is incomplete unless semisimplicity of every transmission zero is proved or polynomial-exponential descriptor terms are included.

### 6. Stability of all descriptor exponents is not established

The theorem places every \(\zeta_\ell\) strictly in the left half-plane. Stability of the Markov generator does not by itself force every zero of a non-selfadjoint compressed resolvent to be minimum phase. A collocated dissipative realization can have stronger positivity properties, but the manuscript does not prove the required positive-real/accretive theorem for the selected resolved projection.

Tracking a zero is not the same as proving \(\Re\zeta_\ell<0\).

### 7. The quenched rough theorem is stronger than the established input

Uniform convergence over compact sets of complete pasts requires uniform conditional bracket convergence, Lindeberg control, roof inversion, and tightness in the rough topology. The proof invokes the disputed spectral estimate and an “ergodic theorem uniformly on compact history sets” without proving such a quenched theorem. The A3 LDP does not supply it.

### 8. Downstream consequences are therefore conditional

C2 uses A4's common history kernels, Doob form domain, and differentiable memory decomposition. D1 uses phase-wise semigroups and tangents. None may treat these as closed interfaces while the complete-past spectral theorem and A2 resolvent input remain open.

## Genuine improvements recognized

The following changes should be retained:

- the correct solution \(h=\sum_{j\ge0}P^jg\) and martingale increment;
- the exact eigenfunction Doob normalization;
- the causal sign
  \(\widehat K=zR-RLR-C^{-1}\);
- explicit instantaneous distribution terms; and
- retention of terminal-flight and rough-area effects.

## Required reconstruction

The paper should replace total-variation Harris minorization on complete histories by a precisely proved contraction theorem in a weighted history metric or by a one-sided transfer operator on a quotient state. It must then prove the Feynman–Kac spectral chart independently. The renewal-resolvent and memory statements require an actually integrable A2 frequency theorem, a complete treatment of higher-order zeros, and a stability theorem for descriptor modes.

## Recommendation

**Reject.** Correct universal algebra has been installed, but the model-specific spectral theorem begins with an impossible minorization, and the memory theorem imports an invalid high-frequency estimate. The paper does not establish the claimed Sinai history, rough, or memory closure.