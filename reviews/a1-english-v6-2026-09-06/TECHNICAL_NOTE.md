# Referee technical note: an exact dimension jump at fixed finite resolution

**Source under review:** A1 v6, commit `750a65ef62422e81307b4a61fd891ee42fa2639e`.  
**Status:** A deduction supplied in this review, not a counterexample to the printed theorem and not a claim of literature priority. The exact dimensions use the reviewed Theorems 3.3–3.4; the base finite-state code uses Theorem 5.3. The perturbation estimates below are proved here.

## 1. One uniformly positive family

Fix the uniform prior on `[0,1]`, total horizon `N=5`, comparator margin `eta=1/4`, and `0<=theta<=1/2`. Set

\[
A_\theta=\{0,1,2+\theta\},\qquad
k_1^\theta=\tfrac13+\tfrac1{12}t,\quad
k_2^\theta=\tfrac13+\tfrac1{12}t^{2+\theta},\quad
k_0^\theta=\tfrac13-\tfrac1{12}(t+t^{2+\theta}).
\]

These three cells sum to one, span `W_(A_theta)`, and are at least `1/6` throughout the interval. Every accepted or rejected report likelihood under any command in `[1/4,3/4]^3` is consequently at least `kappa=1/24`. This margin is independent of `theta`. The prior and horizon are fixed. No rare-history conditioning or vanishing sensor amplitude is introduced.

At `theta=0`, the causal dimensions for `n=0,...,5` are

\[
(0,2,4,4,2,0),\qquad D_{A_0}(5)=4.
\]

For every `0<theta<=1/2`, the six elements of `2A_theta` are

\[
0,\ 1,\ 2,\ 2+\theta,\ 3+\theta,\ 4+2\theta,
\]

and are distinct. Hence `d_(A_theta)(3,2)=5`. At `n=2` the past bound is four and at `n=4` the future bound is two; `3A_theta` has at least five elements. The complete profile is therefore

\[
(0,2,4,5,2,0),\qquad D_{A_\theta}(5)=5.
\]

This does not rely on irrational exponents: arbitrarily small positive rational `theta` already has this property at five trials. The v6 theorem thus changes the eventual squared-prediction power from `M^(-1/2)` to `M^(-2/5)`.

## 2. Keep the physical command and query labels fixed

Take three one-step probe failures

\[
F_j^\theta=c+\delta k_j^\theta,\qquad c=\tfrac12,\quad\delta=\tfrac18.
\]

They are implemented by the same command labels for all `theta`: accept at probability `3/8` on cell `j` and at probability `1/2` on the other two cells. Their sum is the nonzero constant `3c+delta`, and they span the same three-dimensional space as the cells. All ordered `m`-fold products, labelled by `j_1,...,j_m`, provide a common finite spanning query menu for every model. There are `3^m` query labels, independent of `theta`; linear dependencies at `theta=0` do not invalidate the menu.

Use the same independent uniform exploration commands as in Theorem 5.4 and the peak checkpoint `n=3`. The following estimates in fact hold uniformly over all admitted command-report histories and all checkpoints. Thus they also hold for the unconditional fixed exploration protocol.

## 3. Uniform prediction perturbation

For `0<t<=1`, the mean value theorem in the exponent gives

\[
|t^{2+\theta}-t^2|
\le\theta t^2|\log t|\le\theta.
\]

At zero this follows by continuity. For every individual report factor, accepted or rejected, the difference between the two models is at most `L theta`, where `L=1/12` suffices. For failure reports the two varying cell differences cancel to the coefficient `g_0-g_2`, so the same bound holds.

Let `P_theta` and `P_0` be the unnormalized product likelihoods of the same length-`n` prefix and let `Z_theta=mu P_theta`. All factors lie in `[kappa,1]`. Telescoping products gives

\[
\|P_\theta-P_0\|_\infty\le nL\theta,
\quad |Z_\theta-Z_0|\le nL\theta,
\quad Z_\theta,Z_0\ge\kappa^n.
\]

Consequently the normalized likelihood densities satisfy

\[
\int\left|\frac{P_\theta}{Z_\theta}-\frac{P_0}{Z_0}\right|d\mu
\le\frac{2nL\theta}{\kappa^n}.
\]

For a common length-`m` probe label, the actual tests `H_theta,H_0` are products of `m` report factors, so

\[
\|H_\theta-H_0\|_\infty\le mL\theta,\qquad 0\le H_\theta,H_0\le1.
\]

Their posterior predictions obey

\[
|p_\theta(h,j)-p_0(h,j)|
\le L\left(m+\frac{2n}{\kappa^n}\right)\theta
\le K_5\theta,
\]

where `K_5` is finite and independent of `theta`, the history and query. These estimates are deliberately coarse; no sharp conditioning constant is asserted. Crucially, the constants do not diverge as the two exponents approach their additive collision.

## 4. A smaller-dimension streaming code remains competitive

For the base model `theta=0`, Theorem 5.3 supplies an actual `M`-state streaming filter, updated after every input, satisfying

\[
\frac1{3^m}\sum_j(a_j(h)-p_0(h,j))^2\le C_0 M^{-1/2}
\]

at every checkpoint. Run exactly this transducer, with its base-model read-only tables, on the `theta` experiment. It receives the same input and query labels and stores only its original index. Every such history is admitted in both models. No model-`theta` exact prefix or posterior is supplied to the transducer.

The elementary inequality `(x+y)^2<=2x^2+2y^2` then yields

\[
\frac1{3^m}\sum_j(a_j(h)-p_\theta(h,j))^2
\le 2C_0M^{-1/2}+2K_5^2\theta^2.
\]

Taking a maximum over histories or integrating under the actual `theta` experiment proves, with one constant independent of `M` and `theta`,

\[
\boxed{\mathcal R_{M,5}^{\theta}\le C(M^{-1/2}+\theta^2).}
\]

Here the left side can be either optimal minimax checkpoint-uniform streaming regret or optimal unconditional streaming regret at `n=3` in the fixed exploration experiment. The displayed single filter bounds both. The base-model predictions stay in `[0,1]`; no loss rescaling or unbounded decoder is used.

## 5. What this implies, and what it does not

For each fixed positive `theta`, v6 gives a lower bound `c_theta M^(-2/5)` in the specified experiment. Any such constant valid for every integer `M>=1` must satisfy

\[
c_\theta\le C\{M^{-1/10}+\theta^2 M^{2/5}\}.
\]

Choose `M=ceil(theta^(-4))`. Since `M<=2theta^(-4)` for `theta<=1`,

\[
\boxed{c_\theta\le C'\theta^{2/5}.}
\]

This is only an upper restriction on a permissible lower-bound constant. It is not a matching estimate for the optimal constant, and the balancing choice `M` is not proved to be the true crossover scale.

One disappearing direction can also be seen without asymptotics of a code: under the uniform prior,

\[
\int_0^1(t^{2+\theta}-t^2)^2dt
=\frac1{5+2\theta}-\frac2{5+\theta}+\frac15
=\frac{2\theta^2}{5(5+\theta)(5+2\theta)}.
\]

The exact independent diagnostics verify the dimension profiles and normalized ranks at several rational amplitudes, and verify this rational identity. They are not the proof of the all-amplitude estimates above.

The lesson is specific: exact sumset cardinality can jump while resolved prediction directions remain uniformly close at a fixed horizon and a fixed positivity margin. V6 explicitly allows the nonuniform lower constant, so there is no contradiction. The note supplies a concrete quantitative test for the claimed explanatory role of the exact dimension. It is not a demand to add another example and announce that a general robust theory has thereby been proved.
