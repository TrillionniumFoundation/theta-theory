# Historical derivation audit — A2 v40

This audit identifies the mathematical inheritance of the revision, the changes in the observation model, and the location of the preserved arguments. Repository manuscripts are a derivation record, not independently published references. The controlling comparison is with the reviewed v39 source, rather than with an earlier revision.

## 1. Frozen review and author sources

The controlling report is the [v39 external rereview](https://github.com/TrillionniumFoundation/theta-theory/blob/790654161f2f069fb4d1d1ee18bfe86ea5290d74/reviews/a2-v39-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md), on branch `review/a2-v39-external-harsh-top4-rereview-2026-10-04`. The following identities fix the material addressed by this revision.

| Object | Git identity |
|---|---|
| Review commit | `790654161f2f069fb4d1d1ee18bfe86ea5290d74` |
| Review repository tree | `68f2180a31407c7c86851beb7132167a3bd0feaa` |
| Review directory tree | `99a365ce0caa40d473dd89c9e2e4bd8f869796d5` |
| `REFEREE_REPORT.md` blob | `c31e05b056c889caa168e6e0f86acf0e558f6e7d` |
| `SOURCE_AUDIT.md` blob | `0dde45b8d03c07813ce4479a243d209e0f97eedc` |
| Review `LITERATURE_AUDIT.md` blob | `cb91917a4c9f33d631d939726e8aaae34a6f5332` |
| Reviewed author commit | `f815a7acdb5c03e03b9996fc7052b405db66936d` |
| Author repository tree | `3d26fc322785102d5eda2964bdfd94fdaacf0fc7` |
| Author paper tree | `e60aaed448b772942ffd38d556babab35b3c3880` |
| Author core tree | `113a60e9545374aee5ae6fd80b14f4fedf8e8ed6` |
| Author `main.tex` blob | `ff9cfb17e896489a6a59432bf6184711e0ecea52` |
| Author `SOURCE_PINS.json` blob | `01ef2c7863c8535ad19ec25d6ae6ea22a2b73903` |

The reviewed author aliases were `revision/a2-v39-response-rigidity-2026-10-04` and `revision/a2-v39-referee-copy-2026-10-04`. The reviewed closure contained 34 active TeX files, 322 labels, 79 formal result blocks, and 76 proof environments. These numbers specify the preservation baseline; they are not counts for the new main paper.

The report found no fatal counterexample in the audited v39 core. It accepted the coherence of the strip limit, angular distribution identity, recovery of separated density copies, translation fiber, response completion, period equality, one-resolved-obstacle extension, and finite regularization argument. Its remaining objections concerned the extensive continuum observation family, the limited finite probabilistic conclusions, the strong quantitative priors and nonsharp costs, and the accumulated 85-page presentation. The present main paper addresses those objections through a different geometric identification mechanism and a finite law-and-prediction theorem. The companion preserves the reviewed mechanism and its proofs.

## 2. Fixed-length reversal and the v29 finite-chain inverse

The directly inspected antecedent is [`papers/A2-v29-scalar-collision-tomography/core/01_reversal.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/790654161f2f069fb4d1d1ee18bfe86ea5290d74/papers/A2-v29-scalar-collision-tomography/core/01_reversal.tex), blob `e5cc7e7c52284ecb0b773a06a6d86dc1d6dd0a20`. Its physical convention is unchanged: a free start with a first collision along the unreflected segment gives one; a solid start or a free miss gives zero; every attempted preparation is counted.

For the obstacle union \(\mathcal O\), the pointwise identity is

\[
B_a(q)-B_{-a}(q+a)
=\mathbf 1_{\mathcal O}(q+a)-\mathbf 1_{\mathcal O}(q).
\]

This identity uses the common image of a segment and its reversal. It does not need convexity, separation, periodicity, or a short-flight limit. The same v29 file proves that a nonnegative function with a zero somewhere on each chain is determined by its translation difference. In the notation of v40,

\[
r(x)=v(x+a)-v(x),\qquad
v(x)=\max_{0\le m\le M}\left\{-\sum_{k=0}^{m-1}r(x+ka)\right\}.
\]

The empty prefix is included. An error \(\eta\) in the difference gives an error at most \(M\eta\) in the recovered occupation. This formula and its stability are inherited arguments, explicitly reused in `lem:two-field-prefix`.

The stationary single-law specialization integrates the pointwise identity against the unknown Borel probability measure \(\mu\):

\[
F_+(x)-F_-(x+a)=v(x+a)-v(x),\qquad
v(x)=\int\mathbf 1_{\mathcal O}(x+z)\,d\mu(z).
\]

Both means are ordinary forward observations with the same hidden launch law. If obstacle diameters are at most \(D\), obstacle separation is at least \(d\), and the convex support \(A=\operatorname{supp}\mu\) has diameter at most \(\Delta\), the condition \(a=te\), \(t>0\), \(t+\Delta<d\), gives a chain witness with

\[
M=\left\lfloor\frac{D+\Delta}{t}\right\rfloor+1.
\]

The expanded components \(C-A\) have diameter at most \(D+\Delta\) and gap at least \(d-\Delta>t\). A chain leaves its current component before the last step and cannot jump directly to another. No zero site is supplied to the experiment. Under singular launch laws, the correct observable supports are supports of the measures \(v(x)\,dx\) and \(F_\pm(x)\,dx\); pointwise boundary values and continuity are not silently imposed.

The original v29 text distinguished functionals on arbitrary launch densities from finitely many real numbers. The same distinction remains essential here: v40 uses two fixed command vectors, each supplying an entire spatial scalar field in the exact theorem.

## 3. What the v31 mean-exit construction contributes

The directly inspected source is [`papers/A2-v31-reciprocal-command-reconstruction/core/09_mean_exit_inverse.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/790654161f2f069fb4d1d1ee18bfe86ea5290d74/papers/A2-v31-reciprocal-command-reconstruction/core/09_mean_exit_inverse.tex), blob `f6147757d0a82b2c5ff1e0debd26a4e9f33f9f74`.

That argument uses a bounded centered displacement law with positive second moment, including singular covariance, to define a computational random walk. A bounded stopping identity yields a mean-exit estimate, geometric tails, a monotone Bellman inverse, and a comparison of physical occupation functions without supplied zero sets. Its aperture localization is explicit. It distinguishes the computational walk from an actual billiard trajectory and retains the reciprocal joint preparation needed for pooled randomized commands.

The deterministic chain in v40 provides a finite geometric witness for its two-command experiment. It does not replace the hypotheses of the older random-command theorem. The common inheritance is the physical balance relation and the recovery of occupation from differences. The random-walk, stopping, and finite-polytope programmes retain their complete proofs in the companion.

## 4. The reviewed v39 calibration and the new geometric separation

| Reviewed source under `papers/A2-v39-response-rigidity/` | Blob | Preserved mathematical role |
|---|---|---|
| `core/19_single_law_rigidity.tex` | `60e3bd25168c3232806a9eb59454ec622516358b` | Directional short-flight flux, angular density copies, joint inverse, translation fiber, completion and periods |
| `core/19a_one_resolved_component.tex` | `67472c760fae98a6bd3a6626bd30a1cc9097046e` | Minimum-area pure-copy selection and odd-flux occupation recovery with one resolved obstacle |
| `core/20_single_law_finite.tex` | `399fb6ca047744713ecfa0f26ec469f78e4862a8` | Positive regularization, rational forward-bit acquisition, quantitative geometric recovery |
| `HISTORICAL_DERIVATION_AUDIT.md` | `49dcc281b6112eb0fb4a7e2cf5d56c25f674f747` | Earlier flux, registration, lattice and aperture derivations |

The v39 method applies the planar angular operator to the short-flight germ. It obtains antipodal translated copies of the launch density, uses spatial separation to identify a pure copy, and recovers its support, mass, and translation through Steiner centering. Its direct theorem, one-resolved-obstacle extension, and quantitative theorem retain their distinct hypotheses. The companion contains the full arguments.

The new main theorem does not require a resolved density copy or an obstacle wider than the footprint. After occupation recovery, let \(P=C-A\) and let \(K_+\), \(K_-\) be the associated collision-support components. Their association is observable: each meets \(P\) and no other occupation component. For \(a=te\), the key identity is

\[
H_C(u):=2h_P(u)-h_{K_+}(u)-h_{K_-}(u)+t|u\cdot e|
=h_C(u)-h_L(u),
\]

where \(L\) joins the unique contacts with outer normals \(\pm e^\perp\). The footprint terms cancel. If \(\ell\) is the chord length and \(\pm n\) its normal directions, then

\[
(\partial_\varphi^2+1)H_C
=S_C-\ell(\delta_n+\delta_{-n}).
\]

For a strictly convex planar body, the surface-area measure \(S_C\) has no atoms: atoms correspond to boundary segments. It may have a singular continuous part. Thus the positive and negative Jordan parts of this signed measure identify \(S_C\) and the centered chord. This is an atomic-versus-nonatomic separation, not an assumption that the obstacle has a smooth curvature density. Adding the centered chord support to \(H_C\) recovers the obstacle support up to translation. Steiner centering and support cancellation then put all obstacles and the footprint in one common frame.

The exact theorem permits nonsmooth strictly convex obstacles and any compactly supported probability law whose support is nonempty and convex, including a point, a segment, or a singular measure. Its two fixed fields may be specified almost everywhere. After geometric recovery, one isolated occupation component is

\[
v_C=\mathbf 1_{C_0}*\check\mu_0.
\]

The compact obstacle indicator has an entire Fourier transform, nonzero at the origin, whose real zero set has empty interior. Division on its nonzero set determines the launch characteristic function on a dense set; continuity and Fourier uniqueness determine the whole law. This proof does not assume a launch density or divide at every frequency.

The geometric support normal \(u\) is a variable in the recovered support functions. It is not an additional experimental command direction. The new work is the collision-support identity, component association, and geometric separation of the unknown factors. Support-function calculus, Jordan decomposition, and Fourier uniqueness are classical tools, attributed in [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md).

The new proposition `prop:two-field-one-orientation` gives a complementary geometric comparison: smooth strictly convex bodies with identical incoming arcs and different outgoing arcs have identical forward fields in one orientation at every positive length, under the same fixed launch law. Its proof preserves the incoming support semicircle and perturbs the outgoing support semicircle. This proposition belongs to the new two-field analysis, not to the inherited v29 or v39 results, and identifies the information supplied by the opposite orientation.

## 5. Finite law recovery and prediction

The quantitative experiment uses the same two fixed positive-length commands. Its geometric theorem has separate uniform hypotheses for boundary recovery, visibility, component separation, and finite period decisions. In particular, it uses smooth geometric priors of order \(s=6+\beta\), the boundary-mass lower bound \(j(z)\ge b_0\operatorname{dist}(z,\partial A)^\gamma\), and the stronger fixed-command separation \(2t+\Delta<d_0\). The latter gives a uniform reserve for assigning positive nominal records to their obstacle components. The exact theorem's nonsmooth and singular classes are not automatically uniform finite classes. The law-estimation stage itself needs no regularity of the probability law once the geometric estimates and a complete protected component are available.

For footprint support error in \(C^2\) and geometric loss at most \(C\nu\), the geometric acquisition theorem gives

\[
Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2},\qquad
N_{\rm geom}(\nu,\delta)
\le C\nu^{-Q_{\rm pair}}\log(C/\nu)\log(C/(\nu\delta)),
\qquad S_\nu\le J_\nu\le N_\nu.
\]

Its proof combines two-direction boundary acquisition, convex hulls of positive nominal records, and stable extraction of the contact chord. The same positive records serve all support directions. No obstacle-width versus footprint-width restriction is introduced. The exponent is a sufficient upper bound and carries no sharpness claim.

An isolated occupation contribution, divided by its recovered body area, is the law of \(X-Z\), with \(X\) uniform in the obstacle and \(Z\sim\mu_0\). The new finite argument estimates its moments from a rational spatial mesh and empirical prefix maxima. Boundary-band quadrature controls the error uniformly even for singular \(\mu_0\). It then inverts the triangular moment identities, allowing error in the recovered obstacle factor, and fits a positive atomic probability measure on a finite grid.

The explicit stability estimate in `lem:two-field-moment-separation` is

\[
W_1(\mu_0,\widehat\mu_0)
\le C/m+a(Cm)^{Cm}.
\]

The choice \(m\asymp\varepsilon^{-1}\), \(a=\exp[-C m\log(Cm)]\) yields geometric and law error \(C\varepsilon\), with sufficient attempted-bit cost

\[
\exp\!\left[C\varepsilon^{-1}\log(C/\varepsilon)\right]
\log^2(C/\delta)
\]

under the stated quantitative priors. This is an explicit upper bound, not a minimax rate. Moment comparison and polynomial approximation are classical; their acquisition from collision bits and the perturbation of the unknown geometric factor are part of the new finite proof.

For a bounded target window \(U\) and maximum flight length \(T\), the recovered geometry and law give

\[
\sup_{|b|\le T}\int_U
|\widehat F_b(x)-F_b(x)|\,dx\le C_{U,T}\varepsilon.
\]

The proof couples the launch laws and uses bounded variation of collision-start indicators, together with the perimeter and symmetric-difference bounds for swept convex bodies. These are predictions of all bounded-length command responses in the stated spatial norm, with no additional measurements. Exact completion for every finite command remains a separate consequence of exact identification.

If the launch law has a density whose zero extension has known bounded variation at most \(V\), smoothing the finite probability estimate at scale \(\varepsilon\) and acquiring \(W_1\) accuracy of order \(\varepsilon^2\) gives density error \(C(V+1)\varepsilon\) in \(L^1\). Its sufficient cost is \(\exp[C\varepsilon^{-2}\log(C/\varepsilon)]\log^2(C/\delta)\). At this same cost the density output gives uniform raw-mean predictions,

\[
\sup_{x\in U,\,|b|\le T}
|\widehat F_b^{\rm dens}(x)-F_b(x)|
\le C_{U,T,V}\varepsilon.
\]

The planar BV embedding gives \(\|j_0\|_2\le CV\), by layer cake, isoperimetry and coarea. The collision-indicator symmetric difference has area \(O(\xi)\) at geometric tolerance \(\xi\); Cauchy–Schwarz therefore gives uniform mean error \(C_{U,T}V\sqrt\xi\). The construction acquires geometry sufficiently accurately that \(\sqrt\xi\le C\varepsilon\), and replacing \(j_0\) by the estimated density adds its \(L^1\) error. The variation hypothesis belongs to these strong density and uniform raw-mean conclusions. It is not needed for probability recovery or local spatial-mean prediction.

## 6. Preservation, scope, and reading order

The focused main paper presents the two-field exact inverse, its finite geometric acquisition, finite probability recovery, and response prediction. The separately compiled [companion.tex](companion.tex) preserves the complete reviewed v39 mathematical source, including all 322 baseline labels and 76 baseline proof bodies. The two active source closures, rather than only the shorter main file, are the preservation object.

The companion also preserves the earlier localized controls, stationary laws, reciprocal stopping, global response, homothetic registration, isotropic reconstruction, and known-disk minimax programmes. Their original measurement and preparation hypotheses remain attached to them. In particular, the known uniform-disk minimax exponent is a fixed-law benchmark and supplies no lower bound for the joint unknown-law experiment.

The older derivation record retains three distinctions used throughout the revision: a stationary collision-record flux is a different observation model from active forward bits; intrinsic periods are different from a chosen marked lattice basis; and an acquired complete padded scan is different from a finite observed list. The pinned v39 historical audit above documents the v11, v17, v19, and v21 sources of these distinctions.

The seven qualifications in Section 10 of the controlling report remain explicit: full spatial fields in exact identification; separate exact and finite conclusions; separate theorem classes; a stated norm and cost for finite prediction; no periodicity prior for exact periods but a positive patch margin or complete aperture for uniform finite decisions; separate counts for sites, command occurrences, attempted bits, description length and physical positioning; and a focused primary with complete preserved companion proofs. A successful compilation or finite diagnostic is evidence of reproducibility, not a certificate of the continuum mathematical arguments.
