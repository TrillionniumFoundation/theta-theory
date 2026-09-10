# Independent referee report on A2 v12

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Date:** 10 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status:** author-requested, AI-assisted referee-style assessment. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Source, recommendation, and principal finding

The manuscript reviewed here is the revision on `revision/a2-v12-two-contact-rigidity-2026-09-10`, frozen at commit `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`. Its source directory is `papers/A2-v12-two-contact-rigidity`. The repository root tree at that commit is `8c7863ff0144c2ebf23b1c9a4181588f334856c9`. Its parent, `bcde40b514e4dc00a3252f2d0710002a2caeac7b`, is the completed v11 review; the preceding author revision is `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`. This is a review of the completed v12 source, not of an earlier branch bearing an A2 label.

All manuscript paths below are relative to the v12 directory. TeX labels are the definitive statement identifiers; the displayed section and theorem numbers follow the revision's own cross-reference map. The companion audit records the source blobs and reading coverage.

**Recommendation: major revision; I do not recommend acceptance at the requested four-journal level in the present form.** This is not a minor-revision recommendation. Equally, it is not a finding that the new principal theorems are false. In the arguments examined, I found no fatal error in the two-contact block inverse, the stated finite-dimensional physical realization and observation theorem, or the revised complete-profile acquisition and calibration bounds.

The new geometric results are genuine progress. The v11 report suggested a consequential rigidity, physical-image, or physical-testing result as possible ways to strengthen the paper. V12 supplies an independent-contact inverse, an open finite-jet physical image, and physical alternatives for a specified statistical experiment. It would be unfair to repeat the earlier objection as though the paper still contained only an identical-contact calculation or a single nonconstant fourth-jet example.

The principal new finding of this review is a concrete comparison that the manuscript should not leave unexamined:

> For the same class of two independent even contacts with known labelled leading geometry, the two oriented **two-flight** probability germs already have an explicitly invertible block-triangular jet map at every order. Consequently, on the finite-dimensional physical families used in Theorem 10.3, the fixed flight number can be chosen to be **two**, independently of the jet order. Only the offset windows and conditioning constants need depend on that order.

Section 4 proves this statement from the finite stationary action and the exact physical flux. The separating coefficient is a strict binomial remainder, rather than an asymptotic half-line calculation. This is a new comparison developed in this report, not a claim that a previously published theorem has been found to contain Theorem 9.1. It does not identify finite-flight and limiting laws as the same datum, does not establish domination of statistical experiments, and does not invalidate the limiting theorem.

The finding matters to the contribution assessment. The finite-dimensional contact-separation and observation conclusions have a much shorter route than the route through a sufficiently long bridge. What remains particularly distinctive is the **uniform nonlinear relative physical law**, its half-line factorization, and the general smooth function-valued invariant. The revision needs to separate that achievement sharply from geometric information already accessible to very short nonlinear records, and then make a theorem-level significance comparison with the relevant inverse-billiard literature. Adding another unrelated theorem or reporting more verification checks would not answer this objection.

## 2. Disposition of the previous report

A severe review must distinguish unresolved issues from issues that have actually been repaired.

| Previous issue | Disposition in the source now reviewed |
| --- | --- |
| V11 Section 5 / R2: the integrated-flux identity supplies two derivatives that the acquisition construction did not use | **Closed.** Lemma `lem:v12-gain`, the higher-order reconstruction, and Theorems `thm:v12-acquisition` and `thm:v12-self-calibrated` implement the improvement under the same profile and calibration hypotheses. The previous referee's contribution is credited. |
| V11 R1: the significance case needs more than identical-contact inversion and isolated finite-jet nonconstancy | **Substantially answered mathematically.** Theorems 9.1, 10.1, and 10.3 provide independent-contact inversion, an open physical finite-jet image, and physical testing alternatives. The remaining concern is the comparison and significance of these results, not their absence. |
| V11 R3: keep the information set and the symmetrized target explicit | **Satisfied in the statements examined.** Separate contact curvatures are supplied for geometric inversion; the smooth-class pilot removes the actual gap, area, and multiplier, not labels, collars, boxes, or convergence certificates. |
| V11 R4: establish a main-result hierarchy without deleting valid material | **Substantially answered.** The main argument now separates relative laws and geometry from full-profile observation; earlier constructions and auxiliary experiments are placed in appendices. Preservation counts are not an objection or a certificate. |
| Previously closed objections about derivative observations, uncharged failures, an exact-law calibration oracle, nonmeasurable fitting, and smooth-function uniqueness being replaced by formal jets | **Remain closed.** I found no basis to revive them in the new proofs. |

The stronger sufficient exponent is not, by itself, a solution of the exceptional-significance question. However, it is now also wrong to criticize v12 for still discarding the two derivatives identified in v11. Similarly, the finite-dimensional physical lower bound is correctly confined to its own experiment; the manuscript does not import it as a lower bound for complete-profile acquisition.

## 3. Mathematical audit

### 3.1 The two-contact block is a real extension, including coincident curvatures

**Source:** `article/23_two_contact_rigidity.tex`, Theorem 9.1, `thm:v12-two-contact`; equations `eq:v12-action-block`, `eq:v12-amplitude-block`, `eq:v12-block`, and `eq:v12-minus`.

Write

$$
c_b=1+g\kappa_b,\qquad c=\sqrt{c_0c_1},\qquad
\gamma=\operatorname{arcosh}c,\qquad \lambda=e^{-\gamma},
$$

and retain the manuscript's labelled even jets. Its claimed last-jet derivative is

$$
D_{q_m}f_{m-1}=-
\begin{pmatrix}P_m&Q_m\\Q_m&P_m\end{pmatrix}
\operatorname{diag}(K_{m,0},K_{m,1}).
$$

The factors of the unequal curvatures are important. For a half-line starting at type $b$, the linear orbit is $\lambda^iu$ at even sites and $r_b\lambda^iu$ at odd sites, where $r_b^2=c_b/c_{1-b}=a_b/a_{1-b}$. A highest-jet variation in the stationary action counts the boundary site once and each interior site twice. This gives the own-contact coefficient $\coth(2m\gamma)$ and the other-contact coefficient $r_b^{2m}\operatorname{csch}(2m\gamma)$.

For the amplitude, the first varying homogeneous length term is pure in its two endpoints. The edge twist therefore has no variation at degree $2m-2$. At that degree the interior Hessian variation is diagonal. Contracting it against

$$
G_{ii}^{(b)}=\frac{1-\lambda^{2i}}{2a_{(b+i)\bmod2}}
$$

gives exactly the displayed even- and odd-site sums $E_m$ and $O_m$. The change in the nonlinear orbit cannot affect this degree: it starts at degree $2m-1$, while the unvaried Hessian perturbation starts at degree two. For the same reason, products with lower positive-degree determinant terms do not change the first varying coefficient.

The residual-time moments then give the common factor

$$
K_{m,b}=\frac{4}{2^m(m+1)(m!)^2a_b^m}.
$$

The identity $K_{m,b}r_b^{2m}=K_{m,1-b}$ explains the column scaling in the displayed matrix. Omitting that identity would lead to a wrong unequal-curvature block; the source includes it correctly.

The algebraic separation is also correct:

$$
P_m-Q_m=m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
$$

Strict concavity of $\tanh$ on the positive half-line proves the inequality, while $P_m+Q_m$ is positive from the displayed geometric sums. There is no division by a curvature difference. At equal curvatures the symmetric restriction agrees with the older identical-contact coefficient, but the antisymmetric direction is genuinely additional to that restriction.

The argument for finite-jet dependence is adequate at each fixed order. Stationary equations use the same positive quadratic Jacobi inverse at each induction step; the coefficient of $d^{m-1}$ requires action terms only through degree $2m$ and amplitude terms through degree $2m-2$. The highest-jet derivative is independent of that jet, so the dependence is affine. Recursive inversion gives the asserted finite-dimensional analytic inverse and compact-set Lipschitz estimates.

The limitations printed in the theorem are necessary and correctly retained. There is no estimate uniform in the jet order, and smooth graphs are not recovered from equality of all formal jets. Analytic germ determination uses convergence of the graph series. Corollary 9.2 then uses exact analytic continuation and the Frenet equations for connected analytic closed boundaries; it is not a stability theorem for distant boundary points. I found no curvature-coalescence counterexample to the stated result.

### 3.2 The physical open-image theorem supplies independent directions

**Source:** `article/24_physical_image.tex`, Theorem 10.1, `thm:v12-realization`, and Corollary 10.2.

The support-function construction is more than a one-parameter nonconstancy example. At the two horizontal normals, the two functions

$$
\frac{1+\cos\theta}{2}\sin^{2m}\theta,
\qquad
\frac{1-\cos\theta}{2}\sin^{2m}\theta
$$

start at order $2m$ at their selected contact and at order $2m+2$ at the other. Their leading coefficients at the selected contacts are one. The area compensator starts at order $2M+2$ at both contacts. Its area derivative at the disk is a strictly positive integral, so the implicit-function argument really preserves the obstacle area exactly.

The envelope calculation at fixed transverse coordinate yields

$$
\partial_{s_{bm}}q_{b,2m}=-(2m)!\kappa_b^{2m},
\qquad
\partial_{s_{1-b,m}}q_{b,2m}=0.
$$

These are the diagonal blocks of a lower-triangular map. The area adjustment cannot alter them. Positive curvature, a fixed horizontal gap, and clearance survive on a sufficiently small neighborhood. The distant translates cause no hidden infinite verification problem because a uniform diameter bound reduces possible competitors to finitely many translates.

Thus both sets of graph jets, and by Theorem 9.1 both sets of statistical jets, form genuine local coordinates of dimension $2(M-1)$. The free area, the gap, and both labelled curvatures are fixed, so the selected channel's entire leading hierarchy remains constant. This is a meaningful physical separation from leading data.

Corollary 10.2 follows by projection in these coordinates. Its dimension count describes fibres inside a specified larger finite-dimensional family. The source does not present it as a classification of all smooth physical fibres. No such classification is needed to make the statement true.

### 3.3 The finite-window theorem is correct for its specified experiment

**Source:** the same file, Theorem 10.3, `thm:v12-finite-observation`.

The proof first obtains a block Vandermonde Jacobian for the limiting nodal laws, with a higher-order remainder controlled in first parameter derivatives. It then uses differentiated relative convergence to choose a sufficiently large fixed even flight number. The physical normalizing factors are independent of the family parameter because the leading geometry and area were fixed in the realization. Multiplying the rows by these positive constants preserves rank.

A sufficiently small convex parameter ball makes the Jacobian, after a fixed linear transformation, uniformly close to the identity. Integrating along line segments then gives an actual bi-Lipschitz map, not merely pointwise nonsingularity. The finite ordered-net estimator is Borel. The high-confidence preparation count follows from bounded independent summands and the inverse Lipschitz estimate.

For squared risk, every allowed window probability lies in a fixed compact subinterval of $(0,1)$. Interior alternatives separated by $N^{-1/2}$ are actual tables in the constructed family. Bernoulli relative entropy is uniformly quadratic there. The conditional entropy chain rule covers adaptive selection among the fixed windows, including random seeds and early stopping by padding. The resulting two-point testing argument gives the stated $c/N$ lower bound. The upper bound is of the same order.

This is a legitimate physical finite-dimensional theorem. Its $N^{-1}$ risk is nevertheless a regular parametric consequence once the finite probability map has full rank. The rate should not be treated as a separate new general statistical principle. The useful content is the physical coordinate map and the construction of admissible alternatives. Section 4 below shows that the full-rank step can be obtained already at two flights.

### 3.4 The regularity gain and the new preparation exponent are justified

**Source:** `article/28_regularized_observation.tex`, Lemmas 13.1–13.2, Theorem 13.3, Corollary 13.4, and Theorem 13.5; labels `lem:v12-gain`, `lem:v12-reconstruction`, `thm:v12-acquisition`, `cor:v12-modulus`, and `thm:v12-self-calibrated`.

For the unchanged sum-norm class $\mathcal K_m\subset C^{m-1,1}$, the identity

$$
H(V,W)''(d)=\frac2\pi\int_0^1
\frac{V(ds)W(d(1-s))}{\sqrt{s(1-s)}}\,ds
$$

has an integrable endpoint weight. Differentiating through order $m-1$ and using the Lipschitz bounds gives a uniform $C^{m-1,1}$ bound for this second derivative. The zero initial value and first derivative then give $H\in C^{m+1,1}$, uniformly. No extension across zero or stronger profile class is being assumed.

The $m+2$-node smooth reconstruction uses only positive nodes and reproduces degree $m+1$. The denominator in its partition of unity is uniformly positive after rescaling, including at the endpoints. Taylor subtraction and the mixed Abel estimate yield

$$
|JH-H|_{\mathscr A}\le Ch^{m-1/2},\quad
|Jf|_{\mathscr A}\le C\|f\|_{C^3},\quad
|Jz|_{\mathscr A}\le Ch^{-5/2}\max|z_k|.
$$

The second estimate is essential: structured bridge and calibration errors are not amplified by a negative power of the mesh. Only unstructured scalar observation errors receive that amplification. The source keeps these uses separate.

The scaled Bernoulli variance, the logarithm in the simultaneous concentration bound, and the sum of all preparation ceilings are consistent. Compactness of the nodal forward image supplies a finite dictionary, and the first-minimizer convention gives measurability. The resulting sufficient exponent is

$$
2+\frac6{m-1/2}+\frac{\gamma}{|\log\tau|},
$$

with $26/7$ before the bridge term when $m=4$. The conditional uniform-data modulus follows by balancing $h^{m-1/2}$ with $eh^{-5/2}$. These are correctly stated as sufficient and conditional bounds, not optimal exponents.

I also read the retained smooth-class pilot in `article/27_profile_calibration.tex`, including `lem:v11-calibration`. The one-sided onset bracket has a deterministic cost bound even on bad histories. Positive-node extrapolation uses the supplied smoothness rather than an exact-family probability oracle. Its variance uses the small success probability, giving power $2+2/m$. The maps recovering area and multiplier are Lipschitz on the supplied positive boxes. In the profile stage, the exact plug-in mean is $R H_{j,b}(d+\Delta)$; the $C^{3,1}$ bound controls translation in $C^3$. The strictly larger profile-stage power absorbs the charged pilot and its logarithmic factors. The energy origin is not discarded.

### 3.5 The relative physical law remains the technically central input

**Sources:** `v3/10_geometry_action.tex`, `v3/20_integration.tex`, the half-line, factorization, and limiting-law arguments in `v4/10_boundary_layers.tex`, and the compatibility and Abel inverse proofs in `article/20_boundary_compatibility.tex` and `article/21_abel_stability.tex`.

The central distinction is between an absolute action estimate and a relative estimate for an exponentially small twist. The source uses the cofactor formula before taking the limit. Endpoint localization controls the Hessian perturbation in trace norm; telescoping logarithmic determinants costs a trace norm rather than the number of interior sites. The two separated blocks converge to half-line objects, and common Morse coordinates transfer the estimate to the physical residual-time integral down to zero offset.

The full-phase normalization and residual-time interval are retained. This is not an arbitrary endpoint ensemble. The near-onset localization uses a positive lower roof bound and clearance, not a finite-horizon assumption. The energy pushforward identifies the symmetrized profiles, and the Volterra argument proves uniqueness as functions on a collar, not merely uniqueness of Taylor coefficients. The Abel discrepancy is linear, includes its endpoint term, and has a genuine triangle inequality.

These observations explain why the two-flight comparison below does not dispose of the general theorem. It does not construct the half-line profiles of arbitrary asymmetric smooth contacts, establish their nonlinear parity compatibility, or replace the uniform relative convergence argument. Those remain substantial parts of the manuscript.

## 4. A two-flight benchmark for independent contacts

### 4.1 Statement and information set

Use the same labelled channel, individually even graphs, and known $g,\kappa_0,\kappa_1$ as in Theorem 9.1. The physical preparation law and selected events are unchanged. The normalizations below use the area as in the manuscript; equivalently the normalized germs can be specified by dividing their probabilities by their own leading coefficients. This equivalence does not make unknown normalization free in a sampling experiment.

Set

$$
z=c_0c_1-1=\sinh^2\gamma>0,\qquad
L_b=\frac{g}{2c_bz},\qquad
k_m=\frac4{2^m(m+1)(m!)^2}.
\tag{R1}
$$

Let

$$
G_b(d)=F_{2,b}(d)=\frac{2A\sinh(2\gamma)}{d^2}
\Pr(E_{2,b}(d)),\qquad
\xi_{b,m-1}=[d^{m-1}]G_b(d).
\tag{R2}
$$

There are two flights and three impacts, of types $b,1-b,b$. The event is observed at physical time $2g+d$.

**Proposition (finite two-contact block).** At every $m\ge2$, the vector $\xi_{m-1}=(\xi_{0,m-1},\xi_{1,m-1})^t$ depends only on the graph jets through degree $2m$, is affine in $q_m=(q_{0,2m},q_{1,2m})^t$, and satisfies

$$
D_{q_m}\xi_{m-1}=-
\begin{pmatrix}
(1+2z)^m&1+2mz\\
1+2mz&(1+2z)^m
\end{pmatrix}
\operatorname{diag}(k_mL_0^m,k_mL_1^m).
\tag{R3}
$$

Both eigenvalues of the symmetric factor are positive. In particular,

$$
(1+2z)^m-(1+2mz)
=\sum_{r=2}^{m}\binom mr(2z)^r>0.
\tag{R4}
$$

Thus the two oriented two-flight law jets give a block-triangular analytic inverse at every fixed finite order, with compact-set Lipschitz bounds and no curvature-separation denominator. Equality of their germs determines the two analytic even contact graph germs at fixed labelled leading geometry.

### 4.2 Quadratic elimination and the physical normalization

**Proof.** Fix the starting type $b$, put $o=1-b$, and write the endpoints as $u,v$ and the single interior coordinate as $w$. The quadratic part of the two-flight excess action before elimination is

$$
\frac1{2g}\{c_bu^2+2c_ow^2+c_bv^2-2w(u+v)\}.
$$

Consequently the linear stationary coordinate is

$$
w_0=\frac{u+v}{2c_o}.
\tag{R5}
$$

Evenness makes the full stationary coordinate $w=w_0+O((|u|+|v|)^3)$. Eliminating $w$ gives the quadratic endpoint Hessian

$$
\mathsf H_b=\frac1g
\begin{pmatrix}
c_b-(2c_o)^{-1}&-(2c_o)^{-1}\\
-(2c_o)^{-1}&c_b-(2c_o)^{-1}
\end{pmatrix}.
\tag{R6}
$$

Write $C_b=\mathsf H_b^{-1}$ and $\nu(\ell)=\ell^tC_b\ell$ for a linear functional with coefficient vector $\ell$. Direct inversion gives

$$
\nu(u)=\nu(v)=L_b(1+2z),\qquad
\nu(w_0)=L_o.
\tag{R7}
$$

Also

$$
\det\mathsf H_b=\frac{c_bz}{c_og^2}=a_b^2,
\qquad d_2^0=-W_{2,uv}(0,0)=\frac1{2gc_o}
=\frac{a_b}{\sinh(2\gamma)}.
\tag{R8}
$$

The exact full-phase calculation already established in the manuscript therefore gives

$$
G_b(d)=\frac{a_b}{\pi d^2}
\int(d-E_{2,b}(u,v))_+\,b_{2,b}(u,v)\,du\,dv,
\qquad b_{2,b}=-W_{2,uv}/d_2^0.
\tag{R9}
$$

For $E_0(y)=y^t\mathsf H_by/2$, its quadratic normalizing integral is

$$
I_0(d)=\int(d-E_0)_+\,dy=\frac{\pi d^2}{a_b}.
\tag{R10}
$$

Thus the computation concerns precisely the normalized physical probability in (R2), not a newly chosen endpoint density.

### 4.3 Highest-jet action and twist variations

Keep all lower even jets fixed. The first varying term in a one-flight length is the corresponding pure endpoint power divided by $(2m)!$. The stationary envelope identity then gives the degree-$2m$ terms

$$
\partial_{q_{b,2m}}E_{2,b}
=\frac{u^{2m}+v^{2m}}{(2m)!}+O(|y|^{2m+2}),
\tag{R11}
$$

$$
\partial_{q_{o,2m}}E_{2,b}
=\frac{2w_0^{2m}}{(2m)!}+O(|y|^{2m+2}).
\tag{R12}
$$

The factor two in (R12) is the multiplicity of the interior site. Substitution of the cubic and higher corrections to $w$ changes only higher degrees. Smooth Taylor remainders suffice at each fixed order; analyticity is not needed for this coefficient calculation.

The reference twist is constant under these higher-jet variations. Differentiating (R11) and (R12) in both endpoints gives the first amplitude variations:

$$
\partial_{q_{b,2m}}b_{2,b}=O(|y|^{2m}),
\tag{R13}
$$

$$
\partial_{q_{o,2m}}b_{2,b}
=-\frac{g}{c_o}\frac{w_0^{2m-2}}{(2m-2)!}
+O(|y|^{2m}).
\tag{R14}
$$

Indeed, $\partial_uw_0=\partial_vw_0=(2c_o)^{-1}$ and $d_2^0=(2gc_o)^{-1}$. These factors give the coefficient $-g/c_o$ in (R14). This direct mixed-derivative calculation avoids any need to approximate a long interior determinant.

At order $d^{m-1}$, only the displayed homogeneous terms can enter the first variation of (R9). The unvaried action is quadratic plus terms of degree at least four, and the unvaried normalized amplitude is one plus terms of degree at least two. Multiplying a first varying term by either correction raises the offset order. The common Morse-domain argument justifies the coefficient extraction and the parameter differentiation. Differentiation of the residual factor gives the integral over $E_0<d$, with no first moving-boundary term because the residual weight vanishes on its boundary.

### 4.4 Ellipse moments and the block

For any linear functional with variance $\nu=\ell^tC_b\ell$, polar integration after the change $y=\mathsf H_b^{-1/2}r$ gives

$$
\frac1{I_0(d)}\int_{E_0<d}(\ell\cdot y)^{2m}\,dy
=\frac{2(2m)!}{2^m(m!)^2(m+1)}\nu^m d^{m-1},
\tag{R15}
$$

and

$$
\frac1{I_0(d)}\int(d-E_0)_+(\ell\cdot y)^{2k}\,dy
=\frac{2\binom{2k}{k}}{2^k(k+1)(k+2)}\nu^k d^k.
\tag{R16}
$$

For completeness, the angular average of the relevant even power is $\binom{2k}{k}/4^k$. The unweighted radial integral is $(2d)^{k+1}/(2k+2)$; the residual-weighted radial integral is $2^kd^{k+2}/((k+1)(k+2))$. These give (R15) and (R16), including their factors of two.

The own-contact action variation (R11) contributes

$$
-k_m\{L_b(1+2z)\}^m,
$$

and its twist variation has no contribution at this order. The other-contact action variation (R12) contributes $-k_mL_o^m$. Substituting $k=m-1$ in (R16), the other-contact twist variation (R14) contributes

$$
-\frac{g}{c_o}\,
\frac{4}{2^m(m+1)m!(m-1)!}\,L_o^{m-1}
=-k_mL_o^m(2mz),
\tag{R17}
$$

where $g/(c_oL_o)=2z$ was used in the last equality. This proves the first row of (R3); swapping the labels proves the second.

The coefficient of $d^{m-1}$ uses only graph derivatives through order $2m$, by the same finite stationary-equation and scaling argument as above. Its derivative with respect to the last pair of jets is constant in that pair and in higher jets. Thus the dependence is affine at fixed lower jets. Both column factors are positive. Formula (R4), together with positivity of the sum of the two entries, proves block invertibility. Recursive inversion gives the finite-order analytic inverse and its compact-set Lipschitz estimates. For analytic even graphs, equality of all recovered jets gives equality of the two graph germs. This completes the proof.

A normalization check is available at $g=1$, $c_0=c_1=2$, and $m=2$:

$$
D_{q_2}\xi_1=-\frac1{1728}
\begin{pmatrix}49&13\\13&49\end{pmatrix}.
\tag{R18}
$$

Its antisymmetric eigenvalue has magnitude $1/48$. This is a check of (R3), not the proof of the all-order statement.

### 4.5 Consequence for the finite-window experiment

**Corollary.** On the physical families of Theorem 10.1, the conclusion of Theorem 10.3 holds with $j_0=2$ for each fixed $M$, after choosing a sufficiently small parameter neighborhood and sufficiently small positive offsets. The high-confidence preparation order and the squared-risk order remain the stated parametric ones.

**Proof.** Put $n=M-1$. The support parameters map locally invertibly to the finite graph jets by Theorem 10.1. The proposition maps these jets locally invertibly to

$$
\Xi=(\xi_{b,k})_{b=0,1;\,1\le k\le n}.
$$

Use $\Xi$ as coordinates on a small neighborhood. Analyticity and compact restriction give

$$
G_b(d;\Xi)=1+\sum_{k=1}^{n}\Xi_{b,k}d^k
+d^{n+1}R_b(d;\Xi),
$$

with bounded first parameter derivatives of the remainders. At offsets $d=\ell h$, $1\le\ell\le n$, the nodal Jacobian is the block matrix with Vandermonde blocks $((\ell h)^k)$, plus $O(h^{n+1})$. The inverse of each block has norm $O(h^{-n})$. Choose $h$ small enough that the transformed remainder is less than one half.

Passing to probabilities multiplies rows by

$$
\frac{(\ell h)^2}{2A\sinh(2\gamma)},
$$

which are positive and constant over the family. The small-ball argument in Theorem 10.3 now gives a bi-Lipschitz physical probability map directly, without a $\tau^{j_0}$ approximation step. The original limiting-jet coordinates $\vartheta$ and the new coordinates $\Xi$ are related by a local analytic diffeomorphism, so the conclusion transfers to the parameter used in that theorem. The finite-net upper bound and the physical two-point lower bound then apply unchanged on a compact ball. The windows, probability margins, and coordinate Lipschitz constants may depend on $M$. No uniform bound as $M\to\infty$ is obtained.

### 4.6 What the benchmark does not establish

The finite laws $G_b$ are not the limiting laws $\mathcal F_{bb}$. Invertibility of one map does not replace the proof of invertibility of the other. The proposition supplies a comparison for the same geometric target and leading information, not an identification of the two data sets.

The result does not remove evenness, the supplied separate contact curvatures, or the supplied physical family in the finite-window statistical conclusion. It does not recover general smooth graph germs from their jets. It does not improve the full-profile preparation exponent, prove a lower bound for that experiment, or provide a noise-stable conversion between finite and limiting function-valued laws.

I also do not claim that one flight is insufficient for every restricted finite-dimensional family, or that two flights are globally optimal among all possible observations. The manuscript already has a valid one-flight result for identical even contacts. The point here is the explicit two-contact extension of the short-record comparison.

Finally, `tools/verify_v12.py` already contains a related finite Dirichlet-Green/ellipse-moment routine, `finite_block_row`. Its test loop compares flight numbers 16, 32, and 64 with the limiting block. This makes the finite-flight ingredients present in the repository. The source examined does not state or prove (R3)–(R4), or the consequence $j_0=2$. I therefore describe the present addition as an extracted and proved finite-flight benchmark, not as a discovery that the author's finite calculations were wrong or nonexistent.

## 5. Remaining substantive requests

### R12-1 — Complete the short-record comparison for the actual new contact class

**Classification:** major mathematical comparison and contribution issue; not a counterexample to Theorems 9.1 or 10.3.

The introduction recognizes that the old identical-contact information can be present at one flight. That is accurate but no longer the relevant complete baseline once independent contacts become the principal geometric result. The comparison must now include independent contacts, both orientations, and unequal as well as equal curvatures.

The author should check (R3) against the finite action and the existing finite-block routine, then incorporate the proposition and its consequences, or identify a precise error in the proof above. Merely responding that the paper never claimed long records were necessary would miss the issue: the benchmark changes the shortest proof and the physical design of a highlighted new theorem. Conversely, it would be incorrect to describe this report as disproving the asymptotic block or its physical normalization.

The revision should explicitly distinguish the following assertions: leading amplitudes fail to determine higher contact jets; nonlinear short-record laws can determine those jets in the even class; and the long-bridge theorem supplies a uniform relative factorization and a general smooth invariant. These are compatible assertions, with different mathematical content. The strongest presentation makes all three visible.

### R12-2 — State the exceptional contribution after that comparison, not before it

**Classification:** unresolved four-journal significance assessment.

The independent-contact block has a clear and useful separating coefficient. The physical open image confirms that the independent directions are not formal artifacts. Nevertheless, the finite-window rate itself is the familiar regular parametric rate after a locally invertible mean map has been established. Its lower bound verifies the specified experiment; it does not by itself add a general statistical rigidity principle.

After Section 4, the finite-dimensional observation theorem no longer demonstrates a need for the half-line limit. The most compelling remaining case rests on controlling the nonlinear physical twist relatively on a nonshrinking collar, identifying the resulting invariant without symmetry, and relating it to actual preparations. The paper should explain exactly why this combination resolves a substantial inverse question, and what is obtained from limiting laws rather than simply from nonlinear short-record data.

This request does **not** require solving the unrestricted asymmetric fibre problem, proving a full-profile minimax theorem, removing every supplied class certificate, or adding a growing-order stability theory. The preceding report offered several possible routes; the revision has already pursued concrete ones. I am not adding all remaining open extensions as new acceptance conditions. I am asking for an accurate assessment of the completed contribution in light of a proved comparator.

Nor is an additional rate improvement the required response. The v12 rate correction is mathematically addressed and should remain closed. The question is the significance of the principal physical result, not whether every sufficient statistical exponent has been optimized.

### R12-3 — Replace the generic literature disclaimer with a theorem-level comparison

**Classification:** major exposition and novelty-positioning issue; no established duplication claim.

The introduction says, correctly, that spectral and marked-length problems use different observations. That sentence avoids an overclaim, but it does not explain the gain and cost of the present data. A compact comparison should specify the geometric class, observations, supplied leading information, recovered object, and principal mechanism for the nearest results. It should not count all of these different inverse problems as already solved by one another.

The following primary-source checks illustrate the needed precision. They are a targeted comparison, not an exhaustive novelty search or a re-refereeing of the cited papers.

**De Simoi–Kaloshin–Leguil [P1].** The inspected Main Theorem concerns marked periodic-orbit lengths for analytic open dispersing billiards satisfying non-eclipse, in the authors' symmetric class with a genericity condition. Its conclusion is determination up to isometry. The reconstruction uses Birkhoff data and asymptotics near a period-two orbit. This is relevant both to hyperbolic jet recovery and to analytic continuation, but its data and global geometric objective differ from A2's selected near-onset probabilities. One cannot infer an implication between the two inverse results merely from the shared period-two setting.

**Finamore–Leguil [P2].** Theorem A in the inspected version concerns diffeomorphic finite-horizon Sinai billiards with the same **enriched** marked length spectrum and concludes isometry. The enrichment is substantive; it must not be silently replaced by ordinary periodic-orbit lengths. Its CAT(0) and geodesic-approximation mechanism differs from A2's local relative-flux construction. A2's absence of a finite-horizon assumption applies to its selected-channel result, not to an unrestricted global analogue of that theorem.

**Zelditch [P3].** The official Annals abstract describes spectral determination in analytic symmetry classes using wave-trace invariants near a bouncing-ball orbit and stationary-phase calculations. This is an important precedent for obtaining analytic geometry from local invariant expansions. It does not supply the physical event-probability invariant in A2. The comparison should identify which data-extraction problem is new rather than presenting analytic continuation itself as the novel step. Only the publisher abstract and bibliographic record were checked here, not the full proof.

No source checked in this review establishes that the complete relative physical boundary law is already known. Equally, the present targeted reading does not certify historical priority. A credible revision should make its precise contribution legible without claiming either unsupported reduction or unsupported novelty clearance.

## 6. Information sets that must remain separated

The manuscript now mostly does this correctly. The following distinctions are recorded to prevent the next revision from sacrificing accuracy while answering the significance question.

| Result or comparison | Supplied information / model | Target and limit |
| --- | --- | --- |
| Limiting two-contact inverse, Theorem 9.1 | Two individually even graphs; labelled gap and separate contact curvatures; two normalized limiting even-law germs | Each fixed finite pair of even graph jets; both analytic graph germs in the analytic case. No uniform all-order stability. |
| Two-flight benchmark in this report | Same geometric class and leading information; two normalized finite two-flight germs | Same finite-jet and analytic-germ conclusions from a different datum. No statistical experiment ordering asserted. |
| Theorem 10.3 and its two-flight strengthening | Supplied exact finite-dimensional physical family, labels, and fixed leading data; a fixed finite set of positive windows | Local parameter or finite graph-jet recovery; squared risk of order $N^{-1}$ in that fixed experiment. |
| Theorem 13.5 | General smooth contacts; unknown smooth finite-flight remainders; supplied labels, boxes, bracket, collars, and regularity/convergence bounds; charged pilot | Complete symmetrized energy profiles and predicted odd law. Not arbitrary unsymmetrized graph branches. |

The pilot estimates $g,A,\gamma$, not two separate curvatures from their single product relation. The finite physical alternatives are not infinite-dimensional profile alternatives. Exact analytic continuation does not supply a noise-stable reconstruction of distant boundary points. These are restrictions of the actual theorems, not newly discovered defects in their proofs.

## 7. Verification and scope of this review

The completed v12 revision, its response letter, and the complete retained v11 referee report were read through the authenticated GitHub connector at the pinned commit. All three new core mathematical files were read in full, as were the Abel inverse, the smooth-class calibration argument, and the original identical-contact inverse and one-flight comparison. The selected finite-action, physical-integration, half-line, factorization, and compatibility chain was also examined. `SOURCE_AUDIT.json` records which files were read in full and which were read only through the indicated principal arguments.

This is not an exhaustive audit of every retained appendix, the two-collision companion, the historical eleven-paper program, or every original bibliographic proof. I did not reconstruct the complete manuscript checkout, compile either PDF, inspect PDF pages, rerun the author's verification suites, or check remote CI. The reported 117-page main manuscript and preservation of 192 earlier formal environments within 212 current environments are author-session statements in the response letter, not independent build or retention results from this review. I do not relabel them as such.

The separate `verify_review.py` was actually executed in normal and optimized Python modes. It uses only the standard library and imports no manuscript code. Both runs passed, and their JSON outputs are byte-identical. It performs **1,335 finite exact-rational diagnostics**: 1,082 for the two-flight block and its covariance, determinant, and inverse identities; 72 for the limiting-block algebra; and 181 for integrated-flux and acquisition/pilot algebra.

For the two-flight block, the implementation expands the varying finite stationary action as a polynomial, differentiates it to obtain the twist, and integrates monomials using a Gaussian-moment recurrence with the exact ellipse conversion. This is separate code from the author's finite Jacobi routine. The two approaches share the underlying finite-action and ellipse identities, so neither the implementation nor the test count should be advertised as a collection of independent proofs.

The committed compact output contains the diagnostic-list digest, counts, an explicit quartic example, and limitations. The full list is deterministically generated in memory by the script; a failed check raises an exception with its identifier. There is no reliance on Python `assert` statements.

Reproduce the checks with:

```sh
python verify_review.py --output checks.normal.json
python -O verify_review.py --output checks.optimized.json
cmp checks.normal.json checks.optimized.json
```

The script SHA-256 is `5facb5194149cee33008050ab84aaea25ed978c387991bae87aa1201bfa28edd`.

The output SHA-256 is `35b4e51f804f201bde87fcf8a761417231abd550ec9b1140e45cc1acccc5649e`.

These are finite algebraic checks, not proofs of smooth dependence, infinite-dimensional operator estimates, physical realization, concentration, or minimax statements. They are not nonlinear billiard simulations, formal proof certificates, remote CI results, or a journal verdict. The all-order mathematical argument for the new benchmark is Section 4 of this report.

## 8. Final disposition

V12 should not receive a recycled v11 verdict. It genuinely addresses the previous quantitative objection, produces independent-contact geometry and physical testing alternatives, and improves the hierarchy of the article. I found no new fatal correctness objection in the central proofs examined.

It is nevertheless premature to recommend acceptance at the requested level. The independent-contact short-record benchmark is a substantial missing comparison, and the significance case must be rebuilt around what the relative physical law and the general invariant actually add. The literature discussion should then compare theorems and information sets rather than stop at the observation that the data are different.

A satisfactory response should verify the two-flight block, incorporate the finite-window consequence or identify a precise mathematical obstruction, and give a focused revised account of the principal contribution. It should retain the valid general relative law, the closed status of acquisition and calibration, and the complete proofs. It need not manufacture another unrestricted inverse theorem merely to answer this report.

**Major revision is required.** This recommendation withholds acceptance at the four-journal standard; it does not assert that the research program is impossible, demand arbitrary deletion of content, or promise acceptance after one more revision.

## References and permanent source anchors

**[M12]** Qian Qi, A2 v12, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*. Author source commit `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`. Permanent source: https://github.com/TrillionniumFoundation/theta-theory/tree/2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86/papers/A2-v12-two-contact-rigidity . Paths and TeX labels are given at each substantive finding.

**[R11]** Author-requested independent v11 referee-style memorandum, review commit `bcde40b514e4dc00a3252f2d0710002a2caeac7b`; retained report blob `75f604f50085fc2e2824f46288892a2ed1a80089`. Permanent retained source: https://github.com/TrillionniumFoundation/theta-theory/blob/2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86/papers/A2-v12-two-contact-rigidity/history/v11-referee/REFEREE_REPORT.md .

**[P1]** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked length spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4. Official HTML introduction and Main Theorem consulted 10 September 2026: https://arxiv.org/html/1905.00890v4 .

**[P2]** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, 21 October 2025. Official HTML introduction, Theorem A, and enriched-data definition consulted 10 September 2026: https://arxiv.org/html/2510.18983v1 . The comparison is to this specified version and does not assert a later publication status.

**[P3]** S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI `10.4007/annals.2009.170.205`. Official abstract and bibliographic record consulted 10 September 2026: https://annals.math.princeton.edu/2009/170-1/p06 .
