# Technical audit: finite-flight nonlinearity and the erasure limit

**Status.** Referee-derived checks accompanying the September 10, 2026 review of the A2-v9 carrier at `12a3f50e143cc4951d8e9bea888206d965b90e51`. Its mathematical manuscript is identical to v8. This note is not a replacement author manuscript, a publication-priority claim, or a formal proof certificate. Neither calculation below is presented as a counterexample to a theorem actually stated in that manuscript.

All source paths below are relative to `papers/A2-v9-relative-flux-poisson-minimax/` at that commit. The source labels, rather than unverified PDF page numbers, are the controlling locators.

## 1. The fixed-leading-data example is already visible at one flight

### 1.1 General one-flight coefficient

Assume identical even facing graphs, and keep the gap and curvature fixed:

$$
\psi(y)=\frac\kappa2 y^2+\frac q{24}y^4+O(y^6),\qquad c=1+g\kappa>1.
$$

Here $q$ is the fourth graph derivative. It is unrelated to the exponentially small parameter used in Section 2. Define the normalized selected-channel probability and its first offset coefficient by

$$
F_j(d)=\frac{2A\sinh(j\gamma)}{d^2}\Pr(E_{j,e}(d)),
\qquad F_j(d)=1+d\mathcal R_j(0)+O(d^2),
\qquad \gamma=\operatorname{arcosh}c.
$$

For one flight the endpoint Hessian and inverse are

$$
H_1=\frac1g\begin{pmatrix}c&-1\\-1&c\end{pmatrix},
\qquad
M_1=H_1^{-1}=\frac g{c^2-1}\begin{pmatrix}c&1\\1&c\end{pmatrix}.
$$

The $q$-dependent fourth-order term of the flight action is $q(u^4+v^4)/24$. Its mixed derivative is zero, so there is no $q$-dependent quadratic contribution from the one-flight twist. There is also no interior determinant at one flight. Differentiating the residual-time integral therefore gives

$$
\boxed{\ \partial_q\mathcal R_1(0)
=-\frac{(M_1)_{00}^2+(M_1)_{11}^2}{24}
=-\frac{g^2c^2}{12(c^2-1)^2}.\ }
\tag{1}
$$

For completeness, the moment normalization in (1) can be checked without using a long-bridge limit. For any positive $2\times2$ matrix $H$, put $Q(Y)=Y^{\mathsf T}HY/2$ and $M=H^{-1}$. A linear change to the disk gives

$$
\int(d-Q)_+\,dY=\frac{\pi d^2}{\sqrt{\det H}},\qquad
\int_{Q<d}Y_i^4\,dY=\frac{\pi d^3 M_{ii}^2}{\sqrt{\det H}}.
$$

The derivative of $(d-Q-q(u^4+v^4)/24)_+$ contributes the negative fourth moment. No moving-boundary term remains, because the undifferentiated residual weight vanishes on that boundary. Terms of degree six or higher cannot affect this coefficient. This independently recovers the $j=1$ specialization of `eq:v4-finite-quartic` in `v4/20_nonlinear_information.tex`.

### 1.2 Specialization to the manuscript's exactly fixed-area family

The family in `thm:v4-jet-fiber` has support function

$$
h_{s,z(s)}(\theta)=1+s\sin^4\theta+z(s)\sin^6\theta
$$

on the lattice $3\mathbb Z\times4\mathbb Z$. The analytic choice of $z(s)$ preserves obstacle area $\pi$. At the two horizontal contacts, $g=1$, $\kappa=1$, and the graph fourth derivative is exactly $q_s=3-24s$. Thus $c=2$ and (1) yields

$$
\boxed{\ \left.\partial_s\mathcal R_1^{(s)}(0)\right|_{s=0}
=(-24)\left(-\frac1{27}\right)=\frac89.\ }
\tag{2}
$$

The half-line calculation printed in `prop:v4-quartic` gives instead

$$
\partial_q\mathcal R_\infty(0)
=-\frac{\cosh(2\gamma)+2}{12a^2\sinh(2\gamma)},
\qquad a=\frac{\sinh\gamma}{g},
$$

and hence, at the same family,

$$
\boxed{\ \left.\partial_s\mathcal R_\infty^{(s)}(0)\right|_{s=0}
=\frac{\sqrt3}{2}.\ }
\tag{3}
$$

The constants in (2) and (3) are both nonzero. In particular, uniform differentiated Taylor expansion gives

$$
\left.\partial_s F_1^{(s)}(d)\right|_{s=0}=\frac89d+O(d^2).
$$

Every sufficiently small fixed positive one-flight offset detects this deformation locally. The two reversed horizontal channels have equal laws and exhaust the ground onset; summing them and normalizing by their summed leading coefficient gives the same conclusion for the complete two-collision count event. This is not a comparison of statistical efficiency between designs: normalization and the cost of obtaining selected records would have to be charged in such a comparison.

### 1.3 What this establishes, and what it does not

The example genuinely distinguishes nonlinear probabilities while preserving area, gap, and all leading Hessian data. It does **not** demonstrate that long bridges are necessary to detect this higher jet. The manuscript does not expressly assert that necessity, and its separate one-flight contact-germ result already points in the same direction.

The long-bridge contribution must therefore be assessed as a relative, differentiated, collision-order-uniform limit and as an approximation for growing experiments—not as the first possible access to this quartic information. This is a precise significance diagnostic, not a reason to delete the nonlinear example or a finding that its theorem is false.

## 2. A marked Poisson experiment is already implicit in the exact erasure pair

### 2.1 Finite experiment and reversible kernels

Consider a fixed simple hypothesis $h\in\{0,1\}$. Assume that in observation $i$ the two laws have a common restricted measure of mass $1-r_i$, and mutually exclusive remaining supports of mass $r_i$ under either hypothesis. These are the equal-on-overlap experiments of `thm:v7-exact-tv` in `v7/10_critical_experiments.tex`.

Their independent product is equivalent, by hypothesis-independent Markov kernels, to

$$
E_n(h):\quad \Pr_h\{*=\text{erasure}\}=s_n,
\quad \Pr_h\{h\}=1-s_n,
\quad s_n=\prod_i(1-r_i).
\tag{4}
$$

Map a product observation in the common support to $*$ and every exclusive observation to its revealing label. Conversely, on $*$ sample from the normalized common product restriction; on a revealing label sample from that hypothesis's normalized exclusive product restriction. These are well-defined fixed kernels for this known simple pair; outcomes null under both hypotheses and zero-mass branches can be assigned arbitrarily. They do not require knowledge of which hypothesis is true.

Thus

$$
\|P_{0,n}-P_{1,n}\|_{\rm TV}=1-s_n,
\qquad \inf\{\text{equal-prior testing error}\}=\frac{s_n}{2}.
\tag{5}
$$

Their Hellinger affinity is also $s_n$, because the densities agree on the overlap and have disjoint supports outside it. When at least one $r_i>0$, each hypothesis has a positive-mass exclusive support: the two directed relative entropies are infinite. A finite two-sided KL or a regular Gaussian likelihood expansion is therefore not the appropriate justification for this exact support experiment.

### 2.2 The Poisson observation must retain the revealing mark

Define $Z_\lambda(h)$ by first drawing $K\sim\operatorname{Poisson}(\lambda)$, independently of $h$. If $K=0$, report an erasure; if $K>0$, report $(K,h)$. This experiment is exactly equivalent to an erasure experiment with common mass $e^{-\lambda}$. The forward kernel discards $K$ after deciding whether it is zero. The reverse kernel draws a positive-truncated Poisson count after a revealing label and uses $K=0$ after an erasure. At $\lambda=0$, the unused revealing branch is assigned an arbitrary distribution.

The unmarked Poisson variable $K$ alone has the **same distribution under both hypotheses**, and carries no information about $h$. Any description of a Poisson limit of the testing experiment must retain this mark or an equivalent revealing observation.

Put $\lambda_n=\sum_i r_i$ and $m_n=\max_i r_i<1$. The elementary inequality

$$
0\le-\log(1-r)-r
=\sum_{k\ge2}\frac{r^k}{k}
\le\frac{r^2}{2(1-m_n)}\quad(0\le r\le m_n)
$$

gives

$$
0\le e^{-\lambda_n}-s_n
\le\frac{\sum_i r_i^2}{2(1-m_n)}.
\tag{6}
$$

On the common three-symbol erasure space, the total variation distance for each hypothesis between common masses $s$ and $t$ is $|s-t|$. Consequently the Le Cam distance $\Delta=\max\{\delta(E,F),\delta(F,E)\}$, with deficiencies defined using the manuscript's TV convention, obeys the upper bound

$$
\Delta(E_n,Z_\lambda)
\le \frac{\sum_i r_i^2}{2(1-m_n)}+|\lambda_n-\lambda|.
\tag{7}
$$

This is an upper bound, not a claim that the bound equals the exact Le Cam distance. If $m_n\to0$ and $\lambda_n\to\lambda<\infty$, the right side vanishes. No independence theorem for successive visits of one billiard trajectory is used here; independence is already an assumption of the preparation design.

### 2.3 Application to the printed tangent experiments

For conditional successes and raw preparations respectively, the exact revealing probabilities are

$$
r_i=\delta_{j_i}=\frac2\pi\arcsin(e^{-j_i\gamma}),
\qquad
r_i=p^0_{j_i,d_i}\delta_{j_i},\quad
p^0_{j,d}=\frac{d^2}{2A\sinh(j\gamma)}.
\tag{8}
$$

For a homogeneous schedule, write $q_j=e^{-j\gamma}$. If $k_jq_j\to b<\infty$ in the conditional experiment, or $n_jp^0_{j,d_j}q_j\to b<\infty$ in the raw experiment, the Poisson intensity in (7) tends to $2b/\pi$. The limiting equal-prior risk is $e^{-2b/\pi}/2$.

For the actual nonlinear laws, their printed tangent approximation adds, by the triangle inequality and the identity kernels on the common observation space, an error at most

$$
C\sum_i\omega(d_i)\quad\text{or}\quad C\sum_i p^0_{j_i,d_i}\omega(d_i),
\qquad
\omega(d)=\sqrt d\ \text{generally},\quad \omega(d)=d\ \text{for even graphs}.
\tag{9}
$$

At a finite homogeneous critical intensity, $\omega(d_j)/q_j\to0$ makes these errors vanish. It requires $d_j=o(q_j^2)$ in the general case or $d_j=o(q_j)$ in the even case. These are precisely tangent regimes, not fixed-positive-offset regimes. The supercritical case is handled by the manuscript's projection to finite critical subsamples; no finite-intensity Poisson variable with parameter infinity is needed.

### 2.4 Limits of the strengthening

The manuscript already states two-way randomizations after its triangular-schedule limit. Equations (4)–(9) make an explicit marked-Poisson formulation and a quantitative finite-schedule error bound from that existing structure. They do not repair a missing experiment-convergence proof. This is a useful elementary corollary, not evidence by itself of a new nonlinear Poisson theorem. The v9 branch name does not establish that such a theorem has been written.

The reverse kernels may depend on the known table and on the two specified hypotheses. These arguments do not construct a parameter-free simulator on the family of unknown billiard tables. They also do not prove a compound-Poisson hitting-time law along one dependent orbit, or the sharp fixed-positive-offset nonlinear approximation rate. The manuscript already states the relevant restrictions; this note records why they must remain in any later revision.

## 3. Reproducible checks and their limits

`verify_review.py` checks the finite Jacobi Schur complements and Green matrices, the physical area and three-amplitude determinant, the one-flight and half-line quartic constants, overlap quadrature, exact finite erasure products, the bound (6), and auxiliary envelope/entropy identities. It was run normally and with `python -O`; outputs agree byte for byte. The 112 symbolic and 22 ordinary 60-decimal checks are finite diagnostics, not interval enclosures, a nonlinear probability solver, or a certification of the infinite-dimensional proofs. The mathematical claims in this note are justified by the arguments above, not by the check count.
