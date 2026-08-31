# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — History, Memory, and Universal Pressure for Prepared Sinai Paths  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `c50367fa25158328b73f3efed5a0e879539e5e05`

## Executive assessment

The revision correctly distinguishes complete microscopic history from a proposed coarse history, uses a genuine eigenfunction Doob transform, retains transmission zeros rather than declaring them absent, and preserves the rough-area anomaly. These are meaningful repairs.

The selected quotient is nevertheless the wrong quotient for the claimed conditional randomness. Quotienting by stable leaves retains the future-determining unstable coordinate; integrating over a stable fiber therefore does not generate a nondegenerate future symbolic law. The Riesz–Schur realization is not constructed as a compression of the microscopic generator, and the memory transform is written with the wrong algebraic sign. The conditional diffusion theorem and all downstream optional-projection claims remain invalid.

## Major mathematical objections

### 1. A stable-leaf quotient does not create future randomness

For a hyperbolic map, points on the same local stable leaf have the same forward symbolic itinerary. The quotient by stable leaves therefore retains the unstable/future coordinate. In the baker model this is immediate: the stable leaf is vertical, while the quotient coordinate \(q\) determines every future branch label.

If \(x,x'\) lie in the same stable fiber, forward invariance gives

\[
\pi_s(\Phi_t x)=\pi_s(\Phi_t x')
\]

for the quotient dynamics, apart from transient geometric coordinates which contract and cannot produce long-time Brownian randomness. Hence the integrand in

\[
K_t^arepsilon(h,A)=
\int_{\pi_s^{-1}(y)}
1_A(\pi_s(\Phi_{[0,t]}x))\,d\lambda_h^arepsilon(x)
\]

is constant on the fiber at the symbolic level. The kernel is therefore Dirac on the future quotient itinerary. A positive-dimensional fiber is irrelevant if all its points have the same future quotient path.

To obtain a nondegenerate quenched future, one must forget the future-determining unstable coordinate, introduce observation noise, or condition only on a genuinely coarser sigma-field. The manuscript has replaced “complete history” by a quotient which still encodes the future.

### 2. The \(g\)-kernel is used in the wrong temporal direction

A normalized \(g\)-function naturally describes compatible conditional probabilities of past symbols given a future tail (or the chosen one-sided orientation). The paper uses it as a forward transition kernel after conditioning on a coarse past without specifying the natural extension, orientation, or disintegration theorem that makes this legitimate. The assertion that “transporting the quotient \(g\)-kernel along the past” produces \(\lambda_h^arepsilon\) is not a construction of a regular conditional law.

The continuous-time renewal formula consequently starts from an unproved stochastic kernel. Its Feller and Chapman–Kolmogorov properties cannot be established merely by splitting the displayed sum.

### 3. The Riesz–Schur dilation is not an operator realization of the microscopic compression

The compressed resolvent

\[
C(z)=P(z-L_D)^{-1}P
\]

contains the complete unresolved \(Q=I-P\) dynamics. The proposed finite block operator

\[
\widetilde L=
\begin{pmatrix}PL_DP&C_Z\\B_Z&A_Z\end{pmatrix}
\]

acts only on \(V\oplus Z\) and omits that infinite-dimensional unresolved space. The sentence “with the unresolved \(Q\)-resolvent retained in the \(V\) block” is not a definition of an operator. A \(z\)-dependent Schur complement cannot be inserted into a fixed generator block without enlarging the state by the actual unresolved Hilbert space.

Moreover, principal parts of the matrix \(C(z)^{-1}\) can be represented by a finite linear system, but there is no proof that the realization is an orthogonal compression of a contraction/Markov generator, preserves positivity, or has the claimed invariant Hilbert structure. Formal companion matrices are not an operator-compatible microscopic dilation.

### 4. The memory-transform sign is wrong

For

\[
C'(t)=AC(t)+(K*C)(t),\qquad C(0)=I,
\]

Laplace transformation gives

\[
z\widehat C(z)-I=A\widehat C(z)+\widehat K(z)\widehat C(z),
\]

and therefore

\[
\widehat K(z)=zI-A-\widehat C(z)^{-1}.
\]

The manuscript defines instead

\[
\widehat K_{\rm res}(z)=C_{\rm res}(z)^{-1}-zI-A_{\rm res},
\]

which has the inverse and \(zI\) terms with the wrong signs. The subsequent contour-shift theorem is therefore a theorem about a quantity that is not the Volterra memory kernel of the displayed resolved equation.

### 5. The conditional rough invariance principle is only asserted

Even with a correct coarse filtration, a uniform conditional kernel theorem requires a quenched martingale approximation, uniform moment bounds over conditional measures, control of singular histories, stable convergence of the second level, and a topology for histories on which the kernels are continuous. The proof provides none of these estimates. “Truncate at a Young return and let the truncation recede” is a program, not a theorem.

### 6. The paper remains dependent on unresolved A2/A3 inputs

The claimed spectral gap, singularity shield, Gibbs disintegrations, and phase pressure are all inherited from A2/A3, whose main theorems remain open. A4 cannot turn them into proved interfaces by restating them in history notation.

## Required reconstruction

The conditioning sigma-field must be redesigned so that it genuinely leaves future uncertainty. The authors must construct the conditional kernels from a precise natural-extension disintegration, prove a quenched enhanced invariance principle, and formulate the memory realization on an actual Hilbert-space extension containing the unresolved dynamics. The Volterra sign convention must be corrected throughout.

## Recommendation

**Reject.** The revision avoids the complete-history contradiction in words but chooses a quotient that still retains the future itinerary. Its memory kernel is algebraically misdefined, and the conditional diffusion theorem is not proved.
