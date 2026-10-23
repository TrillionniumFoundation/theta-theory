# Independent author-side check of the fixed-window bridge

## Verdict and scope

No substantive mathematical defect was found in the added proofs of lem:ui-reference-modulus and prop:ui-inherited-bridge in the integrated native 334, at their explicitly stated inherited-input scope. The proofs correctly evaluate the reference-modulus and scalar interval-comparison terms using historical native 87. They leave the complete normalized local derivative charge as a sufficient, unproved closing condition.

The check read the full integrated 334, the current physical model and finite-peak reference, historical native 87 (Git blob 4d8d66fe6734a8e54d9dca1af673ab8b7cbcdc31), historical exact-return event and spectral pairing, and the actual variation constants in native 330 and 332. It does not independently reconstruct the entire inherited spectral theorem.

The final checked source is papers/A2-DYN-section-multipliers-exact-inversion-author-revision/core/334_exact_unsmoothed_interval_inversion.tex, with SHA256 96f6515d305e1989fbd26233720e4c58262c675edc13522a9fba0f722b5de047. Its original radius, return-index and lattice-target ranges were reread after the accepted quantifier clarification.

## Gaussian constants and the real drift

Historical lem:v41-moving-maxima explicitly supplies a real interior critical point of the real function log|lambda| at each continued peak. Thus Re grad log(lambda)=0 there, and mu=(1/i) grad log(lambda) is real even when the eigenvalue is nonunit and the Hessian is complex. The argument (y-m mu)/sqrt(m) of every Gaussian in the current reference is consequently real.

For complex symmetric H with Re H >= a I_4 and real z, the oscillatory factor has modulus one. The exact integrals are

\[
(2\pi)^{-4}\int_{\mathbb R^4}e^{-a|v|^2/2}\,dv
 =(2\pi)^{-2}a^{-2}=M_0,
\]

\[
(2\pi)^{-4}\int_{\mathbb R^4}|v_3|e^{-a|v|^2/2}\,dv
 =M_0\sqrt{\frac{2}{\pi a}}=M_1.
\]

For the second calculation, the third-coordinate integral is 2/a and each other coordinate contributes sqrt(2 pi/a). Differentiating under the integral is justified by this integrable majorant. Neither positivity of the complex Gaussian nor a real-valued Hessian is used.

The roof derivative of each reference summand has exactly two contributions: the phase contributes |b_j| M_0 and the Gaussian argument contributes m^(-1/2) M_1. Its remaining coefficient is bounded by c_*^(-1) B_pk exp(-m kappa_j). The finite peak sum therefore gives the displayed D_m with exactly one section-conditioning factor. The bound is global in all real target coordinates; an analysis interval may extend outside the central target without invalidating it.

## Uniform damping of moving nonunit roof frequencies

The historical moving-maxima lemma explicitly defines peak data on open neighborhoods of the compact parameter supports of the partition functions, including where a partition vanishes at its peak. It also gives continuity, kappa_j >= 0, and

\[
\kappa_j(R)=0\ \Longrightarrow\ b_j(R)=0.
\]

For every epsilon>0, the sets K_j intersect {|b_j|>=epsilon} are compact. On their finite disjoint union, kappa has a strictly positive minimum unless the union is empty. Hence

\[
\max_j\sup_{R\in K_j}|b_j(R)|e^{-m\kappa_j(R)}
 \le \epsilon+b_*e^{-m c_\epsilon}.
\]

This is uniform over all active radii and all finitely many continued peaks. Taking m to infinity before epsilon to zero proves the claimed qualitative vanishing. The proof does not discard nonunit peaks or assert an unjustified polynomial damping rate.

The reference modulus factor is also exact:

\[
\frac1{2h}\int_{-h}^h |u|\,du=\frac h2,
\]

so Omega_g <= h D_m/2, not h D_m or a factor involving the window length twice.

## Fixed-window normalization and the scalar comparison

Historical eq:v38-return-mass defines P using the original conditional law and the event T_n-t in J. Its exact fixed-count disintegration uses initial and terminal section tests with the occupation count at times 0 through m-1. This matches current eq:v76-event. Historical thm:v41-uniform-transition is uniform over R, 1<=n<=m, all lattice targets and all real window centers.

Taking J=(-h,h), its conclusion is

\[
\sup\left|m^2\int_{t-h}^{t+h}p(u)\,du
                    -2h\,\mathcal L_m(t)\right|\to0.
\]

Since h is fixed and positive before the collision limit, division by 2h proves precisely E_m(h)->0. No rate uniform in an m-dependent h is used.

The sharp interval tail is 2 D_all^1/(pi S). Multiplication by m^2/(2h) gives exactly

\[
\frac{D_{\rm all}^{1}m^2}{\pi hS}.
\]

Inserting the actual interval mass in Xi, then the reference at the window center, gives

\[
\Xi\le E_m(h)+\frac{hD_m}{2}
                  +\frac{D_{\rm all}^{1}m^2}{\pi hS}.
\]

There is no missing factor two. Native 330 makes D_all^1 independent of m and R. The specified S=m^(P+2)/h therefore makes the final term D_all^1 m^(-P)/pi.

## Suprema, the direct bridge, and the remaining condition

At every Lebesgue point of a BV density,

\[
\left|p(t)-\frac1{2h}\int_{t-h}^{t+h}p(u)\,du\right|
 \le |Dp|([t-h,t+h]).
\]

Consequently the sharper direct inequality is indeed

\[
\operatorname{rawerror}_m\le\Omega^p_{m,B}+E_m(h_B).
\]

Take the radius and exact-label suprema and the roof essential supremum as written; each radius may have its own exceptional null set. The inherited E_m is uniform over the full target range, so restricting its center to the original central set causes no loss. With h_B fixed, the collision limsup gives E_M <= limsup_m Omega^p_(m,B); only afterwards is the outer B limit taken.

The quantifier clarification has been implemented in the checked source: immediately after specifying w=1 and V=1, it states that every raw-target supremum below uses R in [R_-,R_+], 1<=n<=m, and k in Z^2. The subsequent bare suprema and the explicitly ranged definition of E_m therefore have the same original target scope. No unresolved notation correction remains from this check.

The sharper direct proof needs no growing-band estimate. The separate Xi statement evaluates its particular scalar truncated interval expression through the exact tail and the inherited fixed-window law; it does not estimate a strong operator on that growing band. The analysis intervals do not replace the original microscopic conditioning events.

The unscaled global BV bound supplies no proof that lim_B limsup_m Omega^p_(m,B)=0. The manuscript states this limitation accurately. No new raw pointwise local limit conclusion, arbitrary microscopic shrinking-rate assertion, or enlargement of the observation class is justified or claimed by these two proofs.

