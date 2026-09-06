# Technical note — what the v7 theorems imply, and where their hypothesis matters

**Source:** A1 English v7, submission `02f68484cf92ef312037cf455bd3f3737ae4facd`.  
**Status:** Deductions made in the present referee review. Neither part is a counterexample to a printed v7 theorem. Part I extracts a further corollary; Part II demonstrates why a stated restriction cannot simply be dropped.

## I. The order of the budget for beating the uncompressed erased statistic is necessary too

Use exactly the experiment and notation of Section 8. In particular, `V_T^theta` gives the comparator the entire exact statistic

\[
T_\theta=(M_1,M_2,M_{3+\theta},M_{4+2\theta})
\]

without a memory restriction. Write

\[
E_\theta=V_*^\theta-V_T^\theta,
\qquad L_M^\theta=V_*^\theta-V_M^\theta,
\qquad \Psi_\theta(M)=\max\{M^{-1/2},\theta^{2/5}M^{-2/5}\}.
\]

Theorem 8.2 and Proposition 8.1, using Theorem 7.1, establish positive constants independent of `M` and `0<theta<=1/2` such that

\[
c_e\theta^2\le E_\theta\le C_e\theta^2,
\qquad c_s\Psi_\theta(M)\le L_M^\theta\le C_s\Psi_\theta(M).
\tag{N1}
\]

These inequalities use the same payoff and the same acquired-history distribution. Their difference can therefore be taken without changing a Bayes baseline.

**Proposition.** There are constants `0<k<K<infinity`, independent of `theta`, such that every integer `1<=M<=k theta^(−4)` satisfies

\[
V_M^\theta-V_T^\theta\le-C_e\theta^2<0,
\tag{N2}
\]

whereas every integer `M>=K theta^(−4)` satisfies

\[
V_M^\theta-V_T^\theta\ge \tfrac12 c_e\theta^2>0.
\tag{N3}
\]

The first assertion is vacuous when its integer range is empty.

**Proof.** The exact identity `V_M−V_T=E_theta−L_M`, together with (N1), gives

\[
V_M^\theta-V_T^\theta
\le C_e\theta^2-c_s M^{-1/2}.
\]

Take `k=(c_s/(2 C_e))^2`. When `M<=k theta^(−4)`, the second term is at least `2 C_e theta^2`, proving (N2). Decrease `k` if necessary to arrange `k<K` below.

For the opposite direction, (N1) gives

\[
V_M^\theta-V_T^\theta
\ge c_e\theta^2-C_s\Psi_\theta(M).
\]

For `M>=K theta^(−4)`,

\[
\Psi_\theta(M)
\le\theta^2\max\{K^{-1/2},K^{-2/5}\}.
\]

Choose `K>=1` large enough that the last maximum multiplied by `C_s` is at most `c_e/2`. This proves (N3), which is the sufficient direction already in the manuscript. ∎

Define the first budget at which the full streaming experiment can beat the uncompressed statistic by

\[
M_{\mathrm{beat}}(\theta)
=\min\{M\in\mathbb N:V_M^\theta>V_T^\theta\}.
\]

It is finite by (N3). The classes of admissible filters are nested as `M` increases; extra states can be ignored. Hence this is an appropriate first-crossing budget, and (N2)–(N3) imply

\[
M_{\mathrm{beat}}(\theta)\asymp\theta^{-4}.
\tag{N4}
\]

Integer rounding changes only the constants. No equality at a particular integer budget, limiting coefficient, or sharp numerical transition point is implied.

**Comparator boundary.** This necessity statement concerns beating the *uncompressed* `T_theta` comparator. It does not imply that the full and erased experiments have equal risks for all smaller equal finite budgets. Compressing `T_theta` to `M` messages can lose additional value, and the sign of that different comparison is not determined by (N2). At `theta=0`, `T_0` is sufficient, so no streaming policy can have value exceeding `V_T^0=V_*^0`.

The finite diagnostics verify the algebraic constant selection, not the analytic bounds (N1). Those bounds are supplied by the reviewed manuscript's proofs.

## II. A seven-trial boundary inside the same positive detector family

Keep the same detector, calibration range, comparator cube and full-support prior, but set the total horizon to seven. This changes no apparatus amplitude, positivity margin or parameter space.

For `A_theta={0,1,2+theta}` and `0<theta<=1/2`, put `D=2+theta`. The three-fold sumset is

\[
3A_\theta=
\{0,1,2,D,3,D+1,D+2,2D,2D+1,3D\}.
\tag{N5}
\]

All ten numbers are distinct in that parameter range. For example, `2<D<3`, `3<D+1`, `D+2<2D`, and `2D+1<3D`; the remaining successive inequalities follow immediately from `D>2`. At zero, `3A_0={0,1,2,3,4,5,6}`.

The exact theorem `d_A(n,m)=min{2n,|mA|−1}` consequently gives the entire profiles

\[
\begin{aligned}
(d_{A_0}(n,7-n))_{n=0}^{7}
  &=(0,2,4,6,6,4,2,0),\\
(d_{A_\theta}(n,7-n))_{n=0}^{7}
  &=(0,2,4,6,8,5,2,0),\qquad 0<\theta\le1/2.
\end{aligned}
\tag{N6}
\]

For completeness, the `n=4` value uses (N5), the `n=5` value uses the six distinct elements of `2A_theta`, and the `n=6` value uses `|A_theta|=3`. For `n<=3`, monotonicity of zero-padded sumsets and (N5) already give enough future dimension to attain `2n`. Thus possible additive relations at longer sumset lengths do not affect (N6).

At the positive-calibration peak, `n=4,m=3`, the unnormalized binomial tangent has nine dimensions. The future space has ten dimensions. Strict mixed pairing therefore has rank nine, and normalization gives **eight**, not nine, attainable directions. The full-future hypothesis of Theorem 5.1 fails:

\[
K_3-1=9>8=4(3-1).
\tag{N7}
\]

The formal pair clusters at zero have multiplicities

| Limiting exponent | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Multiplicity | 1 | 1 | 2 | 2 | 2 | 1 | 1 |

After deleting the constant, the ambient future order list is six zeros and three ones. If one were to drop (N7)'s restriction and use Theorem 5.1's ambient formula unchanged, its `ell=9` term would give a lower bound proportional to

\[
\theta^{2/3}M^{-2/9}.
\tag{N8}
\]

But at every fixed positive `theta`, the manuscript's exact profile and fixed-calibration streaming upper theorem give an upper bound

\[
\mathcal R_{M,7}^{\theta}\le C_\theta M^{-1/4}.
\tag{N9}
\]

For the prescribed uniform exploration at `n=4`, Theorem 6.4 gives the matching lower power as well. Alternatively, at this checkpoint alone, one can cover eight normalized-factor coordinates and use the eight-dimensional local rank section to obtain the same order.

For a fixed positive calibration, (N8) cannot be a positive-constant lower bound compatible with (N9), because

\[
\frac{\theta^{2/3}M^{-2/9}}{M^{-1/4}}
 =\theta^{2/3}M^{1/36}\longrightarrow\infty.
\tag{N10}
\]

**Conclusion.** Ambient cluster multiplicities alone cannot extend the full-future formula to the past-limited peak. One must also understand how the attainable image sits in the scaled future space. V7 correctly retains the restriction; there is no contradiction with its five-trial theorem. This calculation does not determine the seven-trial *uniform-in-calibration* law, and no candidate such law is claimed here.

This is a concrete scope diagnostic, not a demand that the author append a seven-trial example and declare all significance questions settled. It distinguishes a genuinely general attainable-geometry extension from a formally incorrect extrapolation of an already valid formula.
