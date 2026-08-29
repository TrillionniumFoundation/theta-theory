# Common actual platform — v5 external-review series

## 1. Physical flagship: `OB3-MG-v1`

For \(a\in[-1/20,1/20]\), take three circular obstacles

\[
K_1(a)=\overline B((0,0),1+a),\qquad
K_2=\overline B((6,0),1),\qquad
K_3=\overline B((0,9),1)
\]

in the plane and use specular exterior billiard dynamics.  Uniform no-eclipse
margins give a fixed obstacle-code shift

\[
\Sigma=\{\omega\in\{1,2,3\}^{\mathbb Z}:\omega_{k+1}\ne\omega_k\}.
\]

The invariant reference law is the stationary Markov-Gibbs law with

\[
P=\begin{pmatrix}
0&2/3&1/3\\
1/3&0&2/3\\
2/3&1/3&0
\end{pmatrix},
\qquad \pi=(1/3,1/3,1/3).
\]

The actual free-flight roof is \(\tau_a\), not a constant or substituted
clock.  Paper I proves strict mean-roof response.  Paper II proves correlated
rough convergence, nonzero area anomaly, and physical-time change.  Paper III
uses the same code, law, roof, and collision observable in its microscopic DPP
and HJB limit.

## 2. Collision observable

\[
g_1=(1,0),\quad
g_2=(-1/2,\sqrt3/2),\quad
g_3=(-1/2,-\sqrt3/2).
\]

The exact collision coefficients are

\[
\Sigma_{\rm coll}=\frac17I_2,\qquad
\Gamma_{\rm coll}^{\rm as}
=-\frac{\sqrt3}{28}
\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

Physical coefficients are divided by the same mean roof \(\bar\tau_a\).

## 3. Exact benchmark: `FB4-EXACT-v1`

The four-branch full-cover moving-seam map remains active only as an exact
all-order response, finite-difference, exact-innovation, and CI benchmark.
Its coefficients may not be inserted into an `OB3-MG-v1` same-platform theorem.

## 4. Similarity control: `SL-SIM-v1`

The similarity Lorentz family remains active only as:

- an exact conjugate specular control;
- a tensorial scaling and rotation check;
- the similarity-maximality/no-coordinate-bypass theorem.

It is not a nonzero moving-singularity source.

## 5. Downstream extensions

Paper IV uses `OB3-MG-v1 × AR-FILTER-v1`.  Paper V core uses the physical
theta-semigroup from Paper III.  Its volatility-uncertain branch is separately
typed `SV-CONTROL-v1`.

## 6. Status boundary

The active papers are research drafts prepared for external review.  The
platform registry distinguishes manuscript proof, machine checks, and
independent review.  No successful verifier grants peer-review status.
