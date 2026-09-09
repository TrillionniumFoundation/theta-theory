# Referee comparison: a fixed-offset parametric curvature experiment

**Date:** September 9, 2026.  
**Status:** A mathematical comparison developed during this independent review, not a theorem claimed in either submitted v7 and not a numerical reconstruction of a billiard. It is supplied to make the significance objection testable. The construction uses the explicitly printed analytic physical family; it does not apply to an arbitrary smooth family with unspecified higher-jet nuisance functions.

## 1. Proposition and the precise comparison

In a sufficiently small fixed physical neighborhood of the circular member of

\[
 h_{R,\alpha,\beta,\zeta}(\vartheta)
 =R+(1-\cos6\vartheta)(\alpha+\beta\cos2\vartheta+\zeta\sin2\vartheta),
 \qquad R_*=1/4,
\]

there is a count-only experiment using four **fixed physical windows**, flight numbers only 1, 2, and 3, and fresh full-phase preparations, which estimates the unordered curvature triple to matching accuracy \(\varepsilon\), uniformly with confidence \(1-\eta\), using

\[
             N\le C\varepsilon^{-6}\log(C/\eta),\qquad 0<\eta<1/4.
\tag{C1}
\]

The true gap is unknown. The design requires a fixed sufficiently small local neighborhood and the known formula for the family, not an accuracy-dependent gap bracket, positions, channel labels, or the true area. The preparation count is deterministic. At this budget the same estimator gives gap, area, and symmetric-coefficient errors of order \(\varepsilon^3\).

For bounded-flight Bernoulli designs staying in a fixed sufficiently small onset collar, the physical two-point argument gives the matching lower order \(c\varepsilon^{-6}\log(1/\eta)\) for uniform high-confidence **curvature** recovery on this neighborhood.

This is not a counterexample to either manuscript's lower bound for offsets constrained to \(d_i\le H_m h_\varepsilon\), where \(h_\varepsilon\to0\). The present fixed offsets are outside that narrower design. It also does **not** reproduce the stronger joint gap target \(O(h^{m+1})=O(\varepsilon^{3+3/m})\) of the extrapolation theorem. It compares its headline curvature-acquisition cost, not that finer simultaneous timing target. Neither comparison involves sending an extrapolation order to infinity.

## 2. Exact finite-offset probabilities descend to symmetric coordinates

Let \(x_i=r_i-R\) be the contact-radius increments and \(e=(e_1,e_2,e_3)\) their elementary symmetric functions. The map from \((\alpha,\beta,\zeta)\) to \(x\) is the invertible linear map displayed in `eq:g-contact-curvatures`. A lattice rotation through \(\pi/3\) cycles the three radii; reflection in the horizontal axis interchanges the other two while fixing the first. These generate all permutations. Both are isometries of the whole triangular-lattice preparation and preserve the unlabelled count. Thus each exact normalized probability

\[
 F_j(g,x,d)=d^{-2}\Pr_{g,x}\{N_{jg+d}\ge j+1\},\quad j=1,2,3,
\]

is symmetric in all three radius increments, not only invariant under the order-three rotation used for the lower bound.

In this particular analytic family these functions extend jointly analytically across \(d=0\). Here is why this assertion does not follow just by formally dividing a probability. For fixed \(j\), the local analytic stationary action, its twist, and the positive endpoint Hessian give analytic Morse coordinates on a common neighborhood. After integrating residual time, the normalized probability is an integral of an analytic amplitude evaluated at \(\sqrt{2d}\,z\) over a fixed disk with polynomial weight. The power series converges uniformly on a smaller complex parameter neighborhood. Odd total degrees in \(z\) integrate to zero, leaving a convergent series in integer powers of \(d\). The six local channel contributions have a common gap throughout this family and add; there is no channel-activation interface inside the normalization under consideration. These are fixed-flight applications of `lem:g-relative` and the constructive proof of `lem:g-radial`, not an appeal to a statistical limit.

For clarity, analytic descent at coincident roots can be justified directly. Complexify the radius increments in a small permutation-invariant polydisk. On the set of cubic coefficients with distinct small roots, symmetry makes the expression single-valued and holomorphic in \(e\), using local holomorphic root branches. On a smaller coefficient neighborhood all roots stay in the original polydisk, including as they coalesce. The descended function is locally bounded there. The removable-singularity theorem across the discriminant hypersurface extends it holomorphically. The same argument with \(g,d\) retained as additional variables gives a joint extension. Its value at \(d=0\) is the manuscript's symmetric amplitude map, by equality on distinct real-root configurations and analytic continuation.

Consequently there are analytic functions, on a full coefficient neighborhood before restriction to the physical real-rooted subset, such that

\[
                F_j(g,e,d)=C_j(g,e)+d B_j(g,e,d).
\tag{C2}
\]

The derivatives needed below are bounded on a smaller neighborhood. This full coefficient extension is essential: continuity in the labelled radii alone would not justify a perturbation of the coefficient Jacobian at a triple root. No analogous claim is made here when arbitrary unknown higher contact jets are allowed.

## 3. Four fixed physical windows also estimate the unknown gap

Write \(g_*=1/2\), \(v=g-g_*\), and choose one sufficiently small positive constant \(a\), independent of accuracy and confidence. Use the following four queries:

\[
 (j,t)=(1,g_*+a),\ (1,g_*+2a),\ (2,2g_*+a),\ (3,3g_*+a).
\tag{C3}
\]

Restrict the fixed local family so that \(|v|<a/6\) and every actual excess lies inside the common onset collar. The excesses are \(a-v,2a-v,a-2v,a-3v\), all positive. The normalized means, using known design constants rather than unknown excesses, are

\[
 Q_a(g,e)=\left(
 {\Pr(N_{g_*+a}\ge2)\over a^2},
 {\Pr(N_{g_*+2a}\ge2)\over(2a)^2},
 {\Pr(N_{2g_*+a}\ge3)\over a^2},
 {\Pr(N_{3g_*+a}\ge4)\over a^2}
 \right).
\tag{C4}
\]

These are exact physical probabilities in the known model, not substituted leading amplitudes.

Let \(D\) be the three-by-three derivative of \((C_1,C_2,C_3)\) with respect to \(e\) at \((g_*,0)\), holding \(g\) fixed. The source proves

\[
 \det D=-{2\sqrt2(15804720 A_*+64253\pi)\over72930375 A_*^4}\ne0,
 \qquad A_*={\sqrt3\over2}-{\pi\over16}>0.
\tag{C5}
\]

The first amplitude satisfies \(C_1>0\). Subtract the first row of \(DQ_a\) from its second, put that difference first, and multiply its gap column by \(a\). By (C2), as \(a\downarrow0\) this transformed matrix tends to

\[
 \begin{pmatrix}
 C_1&0&0&0\\
 -2C_1&D_{11}&D_{12}&D_{13}\\
 -4C_2&D_{21}&D_{22}&D_{23}\\
 -6C_3&D_{31}&D_{32}&D_{33}
 \end{pmatrix}.
\tag{C6}
\]

Indeed a query with flight number \(j\) and programmed excess \(la\) has gap derivative \(-2jC_j/(la)+O(1)\) after division by \((la)^2\), and coefficient derivative \(D_eC_j+O(a)\). The two first-flight queries therefore separate gap variation from the three shape-coefficient variations. The determinant of (C6) is \(C_1\det D\), which is nonzero. Fix a small enough \(a\) once. The exact map \(Q_a\), with this fixed value of \(a\), is locally invertible in \((g,e)\).

An inverse on a smaller convex data neighborhood has bounded derivative. Choose a compact physical parameter neighborhood whose image lies there. Compact minimum-discrepancy fitting, with either manuscript's Borel tie-breaking rule, then satisfies

\[
 |\widehat g-g|+|\widehat A-A|+\|\widehat e-e\|
 \le C\|\widehat Q_a-Q_a\|,
 \quad
 \operatorname{dist}_{\rm match}(\widehat\kappa,\kappa)
 \le C\|\widehat Q_a-Q_a\|^{1/3}.
\tag{C7}
\]

The second estimate is the cubic root-matching bound already used in the submission; the radius-to-curvature map is Lipschitz on the fixed positive radius interval. Repeated roots are retained. The fit requires the family formula, not the unknown parameter, and no efficiently computable global minimizer is being asserted.

## 4. Sampling and the matching lower bound

Take \(n\) independent Bernoulli observations in each of the four windows. Since \(a\) is a fixed constant, Hoeffding's exponential bound and a union bound give

\[
 \|\widehat Q_a-Q_a\|
 \le C_a\sqrt{\log(8/\eta)/n}
\]

with probability at least \(1-\eta\). Constants may be large as \(a\) decreases, but \(a\) never depends on \(\varepsilon\). Taking \(n=C\varepsilon^{-6}\log(C/\eta)\) in (C7) proves (C1), with \(N=4n\). It also proves the asserted \(O(\varepsilon^3)\) gap and area errors. Bernstein instead of Hoeffding can improve constants in \(a\), not the accuracy exponent at fixed \(a\).

For the lower bound, use the physical alternatives \(R=1/4,\alpha=\zeta=0,\beta=\pm s\) inside the same small neighborhood. Their gaps agree. The manuscript proves matching curvature separation at least \(c|s|\) and per-query Bernoulli divergence at most \(C d_i^2s^6\). On a fixed collar \(d_i\le d_*\), the stopped-transcript divergence is at most \(C d_*^2s^6\mathbb E_sT\). With \(s=L\varepsilon\) chosen so the matching separation exceeds \(2\varepsilon\), a uniformly accurate estimator induces a binary test with both errors at most \(\eta\). Data processing gives

\[
 D_{\rm KL}(\mathsf P_s\Vert\mathsf P_{-s})
 \ge (1-2\eta)\log{1-\eta\over\eta}
 \ge {1\over4}\log(1/\eta),\quad 0<\eta<1/4.
\]

Thus the worst-case expected count is at least \(c\varepsilon^{-6}\log(1/\eta)\). Common below-onset queries, if included, are deterministic failures for this pair and add no information. No positions, full lower-count values, or unbounded flight numbers are used in this comparison.

## 5. Consequence for the referee recommendation

The narrower shrinking-offset lower bound remains correct. The fixed-order extrapolation upper bound, including its stronger timing accuracy, also remains correct. The new fixed-bracket construction is a real repair of a previously uncharged acquisition stage. None of these facts should be reclassified as a false theorem.

Nevertheless, for curvature recovery in the **fully specified finite-dimensional analytic physical family**, the advertised \(6+6/m\) exponent is not the natural unrestricted-local Bernoulli benchmark. Four fixed-window probabilities already retain the nondegenerate coefficient information, including information about the unknown gap, and yield exponent six without an uncontrolled \(m\to\infty\) passage. A paper emphasizing optimal statistical acquisition should distinguish this exact-model benchmark from robustness to unspecified smooth remainder functions, and distinguish a curvature-only loss from its stronger joint gap target. The reviewer is not asking the author to delete either theorem or weaken the general smooth relative law.

## Source locators and verification boundary

The ingredients are `v3/40_inverse.tex` (`eq:g-isogap-family`, `eq:g-contact-curvatures`), `v3/10_geometry_action.tex` (`lem:g-relative`), `v3/20_integration.tex` (`lem:g-radial` and its fixed-domain proof), `v6/30_three_amplitudes.tex` (`eq:v6-three-determinant`), and the physical finite-offset lower-bound chapters of the two v7s. They are pinned by `VERIFICATION.json` to commits `fc2f0599f5b6d905859722891265232dc7ef3c5b` and `e3f5cba851f6216e879d1effa13fa171d92861b7`.

The accompanying diagnostic script independently checks the radius permutation action, the amplitude derivative table and determinant, and the limiting four-window determinant. It does not compute an exact finite-offset billiard probability or certify analytic descent numerically. The written argument above supplies those steps and is open to the same mathematical scrutiny as the submitted proofs.
