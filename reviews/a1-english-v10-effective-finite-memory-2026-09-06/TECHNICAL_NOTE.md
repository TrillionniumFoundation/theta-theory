# A stronger sufficient precision law for the A1 v10 compiler

**Reviewed submission:** `d9f48fe08fd694e636c287be7646ae7d723ce3b8`  
**Date:** 6 September 2026  
**Status:** Referee-derived mathematical note. Not a journal endorsement or a claim that the author's stated sufficient bound is false.

This note uses the definitions and compiler in [the intrinsic section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/06b_collision_geometry.tex) and [the effective section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/sections/effective.tex). The deductions below are analytic; the accompanying finite diagnostics are checks, not their proofs.

## 1. Setting

Retain all the hypotheses of `thm:digital-intrinsic`. In particular, the horizon N and one-step dimension r are fixed, N >= 2 and r >= 2; K is compact inside the strictly ordered chamber; the prior, coefficient realization and positive likelihood margin are fixed; the calibration is known; and the required finite numerical data are supplied or effectively approximable. No new uniformity over priors or horizons is asserted.

Write

\[
 a_0=0<a_1<\cdots<a_{r-1}=D(a),\qquad
 \delta_K=\min_{a\in K}\min_{1\le i<r}(a_i-a_{i-1})>0.
\]

Let H be the fixed normalization used in the submission, and put

\[
 k=\lfloor N/2\rfloor,\quad m=N-k,\quad
 d_0=(r-1)k,\quad \bar\delta=\delta_K/H.
\]

The profile \(\Xi_N(M,a)\) is the maximum over checkpoints of

\[
 \Psi_{n,m}(M,a)=
 \max_{1\le\ell\le\min\{n(r-1),q_m\}}
       (\mathcal V_{m,\ell}(a)/M)^{2/\ell}.
\]

Formal labels are retained, but a determinant witness may be chosen among any distinct future sums.

## 2. A uniform separated-chain floor

**Proposition 1.** For every admitted calibration and every integer M >= 1,

\[
 \boxed{\displaystyle
 \Xi_N(M,a)\ge \bar\delta^{\,d_0-1}M^{-2/d_0}.}
 \tag{1}
\]

**Proof.** Consider the following subset of mA:

\[
 C_m(a)=\{jD:0\le j\le m\}
       \cup\{a_i+jD:1\le i\le r-2,\ 0\le j<m\}.
\]

Every displayed exponent is a sum of at most m elements of A, padded with zero to a formal degree-m label. In each interval [jD,(j+1)D], the chain is

\[
 jD<jD+a_1<\cdots<jD+a_{r-2}<(j+1)D.
\]

Its consecutive gaps are the one-step gaps, hence are at least \(\delta_K\). There are exactly \(m(r-1)+1\) distinct chain elements, of which \(m(r-1)\) are positive. This statement also covers r=2, when the interior part is empty.

At the checkpoint n=k, there are therefore at least d_0 positive future sums. The number of formal positive labels q_m is at least m(r-1), so the attainable truncation is exactly

\[
 p_{k,m}=\min\{k(r-1),q_m\}=d_0.
\]

Choose any d_0 positive chain elements and one formal label for each. All pairwise differences of their normalized nodes are at least \(\bar\delta\). Their determinant product is at least

\[
 \bar\delta^{\binom{d_0}{2}}.
\]

Consequently the ell=d_0 term at this one checkpoint gives

\[
 \Xi_N(M,a)\ge
 \left(\bar\delta^{\binom{d_0}{2}}/M\right)^{2/d_0},
\]

which is (1). No additive-gap lower bound, collision test, prior density or rank-continuity assertion has been used. The separated chain is explicit. QED.

This is a stronger floor than the ell=1 inequality \(\Xi_N\ge M^{-2}\) used in v10 whenever d_0>1. It is a profile inequality, not an assertion that the full profile always has exponent 2/d_0. Additional collision-sensitive terms remain important.

## 3. Consequence for numerical compilation

**Proposition 2.** Under the same effective-data assumptions as `thm:digital-intrinsic`, its sharp persistent-state regret order can be attained with

\[
 \boxed{\displaystyle
 b(M)=\frac{1}{d_0}\log_2(M+1)+O(1)
 }
 \tag{2}
\]

binary places for current command approximation and the finite numerical input/output data. The same compiler, with this coarser mesh, has a sufficient finite read-only program bound

\[
 \boxed{\displaystyle
 O\bigl(M^{1+J/d_0}\log(M+1)\bigr)\text{ bits}.}
 \tag{3}
\]

Its state count is still at most M per stage. All comparison constants are uniform over K and M, with the same allowed fixed-experiment dependence as in the manuscript. These are sufficient bounds, not matching lower bounds on precision or program length.

**Proof.** The compiler already proves

\[
 \sup_{n,h}\mathcal R(\widehat Q_n,Q_n(h))
 \le C\{\Xi_N(M,a)+h^2+\tau^2\}.
 \tag{4}
\]

Choose h and tau at most a fixed multiple of \((M+1)^{-1/d_0}\). Equation (1) gives

\[
 h^2+\tau^2\le C_1M^{-2/d_0}
            \le C_1\bar\delta^{1-d_0}\Xi_N(M,a).
\]

Thus (4) is still bounded by a constant times the full sharp profile, including all its collision-dependent terms. The lower law is unchanged: this remains a filter in the original M-label model with a fixed memoryless command interface.

Set the dyadic mesh using

\[
 b=\left\lceil\frac{\log_2(M+1)}{d_0}\right\rceil+b_0,
\]

where b_0 is fixed. Integer comparisons of \(2^{bd_0}\) and M+1 suffice to choose the variable part; no real logarithm oracle is needed. Certified coefficient and moment errors of a fixed multiple of tau suffice by `lem:finite-moments`; any additional fixed accuracy allowance changes b_0 only. The calibration perturbation estimate in `cor:calibration-precision` also transfers unchanged.

The command grid has \(V=O(M^{J/d_0})\) points. The transition table has O(MV) entries, each of O(log(M+1)) bits; the finitely many output tables have O(Mb) bits. This proves (3). With T=N-1, the displayed distance-operation counts in `prop:compiler-size` also yield

\[
 O\bigl(M^{1+JT/d_0}+M^{2+J/d_0}\bigr)
 \tag{5}
\]

fixed-dimensional rational operations, apart from the numerical-oracle running time. The dimensions, constants and exponent dependence remain fixed-horizon quantities. QED.

The algorithm does not need a numerical value of \(\delta_K\) to choose its mesh: r, N and M determine the variable precision. The separation constant certifies the performance comparison, rather than serving as an input to a collision detector. Supplied positivity and coefficient bounds are still needed for the evaluation guarantees, exactly as in the original theorem.

## 4. The displayed two-parameter example

For `cor:two-parameter`, N=5, r=4 and J=4. Therefore d_0=6. The unchanged compiler can attain the entire three-term regret profile using

\[
 b(M)=\tfrac16\log_2(M+1)+O(1),\qquad
 \text{program bits}=O(M^{5/3}\log(M+1)).
\]

The v10 sufficient choices give log_2(M+1)+O(1) places and O(M^5 log(M+1)) program bits for this same fixed experiment. Both bounds are valid; the latter pair is not the strongest consequence of the supplied argument.

Along u=theta and v=theta+theta^k, the original three regret terms remain unchanged. Equations (2) and (3) still require no extra precision proportional to log(1/|v-u|). This is an improvement in sufficient resource accounting, not a new collision classification or an optimal numerical-precision theorem.

## 5. What the compiler itself contributes

For clarity, unrolling the manuscript's recurrence gives, for n >= 1,

\[
 E_n\le\sum_{k=1}^n
 \left(\prod_{j=k}^{n-1}L_j\right)
 \left\{2e_k(M)+(G_{k-1}+A_k)h+8\tau\right\}.
 \tag{6}
\]

The empty product is one. The query error is at most \(K_nE_n+\tau\). Equation (6) follows by induction and explains both the finite-horizon conclusion and the absence of a horizon-uniform stability claim. The construction's important domain safeguard is that every offline transition target is evaluated by appending to an actual representative history, not by applying a posterior update to an infeasible perturbed vector.

More generally, whenever a squared-loss target F(M) has a certified floor c M^(-2/d), a bound of the form C(F+h^2+tau^2) permits errors of order M^(-1/d). Gap-independent precision is therefore partly a general stability-and-floor consequence. The special attainment theorem still supplies the full target F=Xi; it must not be replaced by the floor alone.

## 6. Limits and diagnostic support

Neither proposition proves that the precision coefficient 1/d_0 is necessary. Neither gives a program-size converse, accounts for the running time of an arbitrary moment oracle, or treats an unknown calibration or a growing horizon. A minimum-precision claim would require a separately specified numerical-information model and an appropriate converse.

The independent program tests 35 separated-chain configurations, 245 exact dyadic absorption inequalities, and additional collision, finite-moment and causal examples. Its mathematical role is diagnostic. The proof of the uniform statement is the separated-chain argument above, not an extrapolation from those finite tests.
