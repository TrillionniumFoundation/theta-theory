# Independent referee report: A2 geometric collision thresholds, revision v2

## Recommendation: reject at the requested top-four-journal level in its present form

**Review date:** September 9, 2026 (Asia/Singapore).  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment requested by the repository owner, not a report commissioned by a journal or an editorial decision of a journal.  
**Author:** Qian Qi.  
**Manuscript:** *Geometric stability and curvature identification for uniform collision thresholds*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-geometric-thresholds-curvature-2026-09-09`.  
**Frozen manuscript commit:** `daeea828a7666acc42adcabdb9ab9057e9e1bac7`.  
**Commit time:** September 8, 2026, 22:51:54 UTC, equivalently September 9, 2026, 06:51:54 Singapore time.  
**Controlling previous review:** `14aaea8937f8b2d373bc642f3568d7280dcbbbd7`.  
**New review branch:** `review/a2-geometric-thresholds-v2-harsh-independent-2026-09-09`.

All source locators below refer to `papers/A2-geometric-thresholds-v2/` at the frozen commit. The source branch was checked again before publication of this report and still pointed to that commit. The review adds material on a new branch; it does not revise the manuscript or overwrite a previous review.

## 1. Editorial judgment and the status of the mathematics

The revision is a substantial response to the previous report. It proves a noncircular geometric extension, treats unequal endpoint curvatures and nonsymmetric boundary jets, retains competing threshold surfaces, constructs a genuinely nonredundant inverse example, and supplies an actual differentiated moving-cut formula. The former objections that the article treats only a circular one-parameter family, that its inverse corollary merely rediscovers an already known radius, and that its record discussion lacks a specified topology cannot simply be repeated against v2.

I have not established an in-scope counterexample or a fatal error in the principal threshold theorem, the stated restricted inverse theorem, or the specified smooth-test response. The strongest argument remains the combination of a length-uniform boundary-value construction with a relative estimate of the exponentially small flux. The geometric extension of that argument is credible and is materially stronger than a fixed-length Morse calculation. Independent finite diagnostics support the alternating-curvature coefficient and nonlinear local mechanics; they are not a certification of the continuum theorem.

Nevertheless, I do not recommend publication at the requested top-four level. The mathematical center is a carefully controlled local calculation near isolated shortest period-two mechanisms. The new geometric freedom is real, but its leading observable still compresses the geometry into one Floquet product per channel. The competition is a finite sum of independent localized contributions. The inverse consequence is an exact finite-dimensional identification on a deliberately selected equal-gap, centrally symmetric family; after the dynamical coefficient formula, its recovery step is elementary exponential-moment algebra. The response propositions, while correct and necessary for precision, are consequences of the smooth parametrization and ordinary moving-boundary differentiation rather than a separate advance in singular billiard response.

This judgment is about the significance demonstrated by this particular submission, not a universal rule against local results, explicit formulas, or finite-dimensional inverse problems. Nor does it assert that the result is already in the literature. The targeted search performed for this review did not establish a prior theorem containing the exact statement here. What is missing is a compelling mathematical consequence or organizing principle commensurate with the requested venue, not another layer of source indices or another count of verification checks.

The report therefore distinguishes three categories throughout: a verified limitation of what the data can encode; an exposition or attribution correction; and a discretionary editorial judgment. None is to be relabelled as a fatal contradiction of Theorem 1.1.

## 2. Disposition of the previous objections

| Previous item | Disposition for v2 |
|---|---|
| UCT-R1: circular scope and no competing geometric mechanisms | The concrete scope objection is addressed by Theorem 1.1 and Sections 9–11. Nonsymmetric deformations and changes of the minimizing pair are actually treated. The editorial importance question remains a separate judgment, discussed below; it is not the unchanged circular-scope objection. |
| UCT-R2: radius/multiplier redundancy | Addressed by Theorem 12.1. Its contact curvatures vary while every maximal-count threshold location stays fixed. The additional area claim has a more limited informational weight than a further independent unknown; Section 5.2 below computes this precisely. |
| UCT-R3: missing periodic rare-event comparator | Substantially addressed in Section 14.3 through the explicit Carney–Nicol–Zhang comparison. The new inverse section should also acknowledge its Prony-type recovery step and update the periodic inverse-billiard comparison. Neither omission establishes a priority collision. |
| UCT-R4: record topology and response versus convergence | Addressed for the stated test class. Section 13 gives a maximum norm, a common-coordinate density, uniform operator-norm assumptions on test derivatives, and the moving-boundary term. It expressly excludes the formerly problematic unrestricted decoder interpretation. |
| Suggested exact axial source domain | Addressed in Theorem 1.2, with necessity at the boundary and differentiated summability inside the strict domain. |

Completion of these concrete requests is genuine progress. It would be unfair to treat the earlier report's suggested route as though it had not been followed. It would also be inappropriate to treat those suggestions as a promise that any implementation automatically meets a particular journal's significance threshold.

## 3. The actual theorem under review

The scatterer is a smooth strictly convex body repeated on the triangular lattice. Its support function ranges over compact smooth finite-dimensional families in a sufficiently small C4 neighborhood of a circle. Higher derivative constants may depend on higher norms of the chosen smooth family. This is not a claim that a C4 bound controls arbitrary derivative orders, and not a claim uniform up to a vanishing gap or loss of curvature.

For an oriented nearest-neighbor channel, write

$$c_b=1+g\kappa_b,\qquad c=\sqrt{c_0c_1},\qquad \gamma=\operatorname{arcosh}c.$$

The full-preparation contribution near that channel's own threshold is

$$\frac{d_+^2}{2A\sinh(j\gamma)}\,[1+d_+H_j(\xi,d_+)],$$

with a common collar and every prescribed normalized derivative bound independent of j. In the collar of the globally shortest onset, the entire maximal-count event is the sum over the six oriented channels, with offsets d_e=t-jg_e. No differentiation of the nonsmooth minimum of the gaps is needed.

There are two different observation statements here. Near j times the minimum gap, the formula describes the entire unlabelled count event. Near the threshold of a nonminimal channel, the separate channel formula requires selection of its facing-arc itinerary. These are not interchangeable experiments. The manuscript makes this distinction, and it must remain visible in any later summary of the result.

The additive-source theorem factors out the exact normal-orbit mark sum. Its source series runs over different threshold windows, not over all histories in one unrestricted long window. Its exact real convergence condition is

$$\max_e\{q\bar f_e-\gamma_e\}<0.$$

The inverse theorem then specializes to an equal-gap, centrally symmetric three-parameter support family. The unlabelled amplitudes retain the collision-order labels j; it is the channel labels that have been discarded. They identify an unordered curvature triple. No general shape-rigidity theorem or noisy-data reconstruction theorem is stated.

## 4. Proof audit

### 4.1 Complete-event localization and stationary normalization

Locators: `v2/10_geometry.tex`, `lem:g-channels`; `sections/02_flux.tex`, `prop:marked-flux`; `v2/11_integration_inverse.tex`, `eq:g-full-flux`.

The gap between lattice lengths 1 and square root of 3 excludes all more distant translates from a sufficiently short flight. Each nearest pair has a nondegenerate closest chord, and small perturbations preserve its clearance from the other obstacles. Since every flight has length at least the global minimum gap, a small total excess forces each flight separately into one of the short-flight neighborhoods. Nearly normal reflection and the fixed angular separation of candidate channels force the next short flight back to the preceding obstacle. The argument uses the same geometric constants at every impact, rather than a constant depending on the number of impacts.

This supplies the important global-to-local step: the preparation is not silently restricted to a preselected stable manifold or transverse ensemble. Strict convexity and clearance identify the stationary local chords with actual first hits. The possibility of infinite horizon elsewhere is irrelevant to this localized event; the flux argument needs almost-everywhere flight-tube coverage and the positive minimum gap, not a common upper roof bound.

For perimeter P, normalized collision flux is ds dp/(2P), the mean roof is pi A/P, and the stationary intensity is P/(pi A). Their product is ds dp/(2 pi A). First variation gives p=-W_u/(ds/du), so the arclength factor cancels and the endpoint-residual measure is

$$\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.$$

The residual-time interval has length d-(W-jg), is shorter than every preceding roof, and leaves less than a minimum flight after the last impact. It therefore has neither an omitted truncation nor an extra terminal collision. The argument also works for a selected nonminimal channel at its own threshold: it is the residual and terminal excess, not the total observation time alone, that excludes extra end collisions there.

### 4.2 Unequal-curvature quadratic reduction

Locator: `v2/10_geometry.tex`, `lem:g-jacobi`, `eq:g-effective`, `eq:g-ratio`.

The quadratic interior recurrence is

$$y_{i+1}-2c_{i\bmod2}y_i+y_{i-1}=0.$$

The substitution y_i=sigma_i z_i with sigma_i squared equal to c_{1-i mod 2} converts it to the constant-coefficient recurrence with parameter c. Importantly, this substitution transforms the whole quadratic action, not only its interior equation. The endpoint factors must therefore be retained.

With D=diag(sigma_0,sigma_j), the endpoint Hessian is

$$\mathcal H_j=\frac{c\sinh\gamma}{g}D^{-1}
\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\
-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix}D^{-1}.$$

Both parity cases give

$$\frac{-W_{uv}(0,0)}{\sqrt{\det\mathcal H_j}}
=\operatorname{csch}(j\gamma).$$

For j=1 the formula reduces to g inverse times the matrix with diagonal c0,c1 and off-diagonal -1. This is a useful normalization check. The determinant of the two-step transfer matrix is one and its trace is 4c0c1-2=2cosh(2 gamma), giving the multiplier exp(2 gamma). I find no missing parity factor or incorrect factor of two in this calculation.

The supplied independent program verifies the Schur reduction, determinant, and squared relative-twist identities using exact rational arithmetic at unequal-curvature inputs and lengths through 128. It separately checks the two-step transfer trace. These finite identities corroborate the displayed algebra, not its arbitrary-parameter proof.

### 4.3 Uniform nonlinear bridges and the relative flux

Locator: `v2/10_geometry.tex`, `lem:g-relative`; inherited `sections/04_uniform_action.tex`, `eq:weighted-green`, `eq:log-det`.

For general boundary jets the gradient perturbation is quadratic, the bridge correction is quadratic in the endpoints, and the action remainder begins cubically. The revision correctly changes these orders rather than importing circular evenness. The scaled Green kernel has uniform exponential off-diagonal decay. Endpoint weights rho^i+rho^(j-i) make the nonlinear fixed-point map contractive on a common neighborhood. Strict diagonal dominance supplies uniqueness throughout the local box, which is the uniqueness needed for all physically localized paths.

The essential flux identity is

$$-W_{uv}=\frac{\prod_{i=0}^{j-1}b_i}{\det H_{\rm int}},\qquad b_i=-\ell_{uv}(y_i,y_{i+1}).$$

An absolute error on W_uv would be useless at long length. The manuscript instead bounds the sum of logarithmic one-flight errors and the trace norm of the tridiagonal Hessian perturbation. Summable endpoint weights give both bounds independently of j. The uniformly bounded reference inverse then controls the logarithmic determinant relatively, without a dimension factor. This is the right argument.

The differentiated version is also reasonably supported. Parameter derivatives of the Green kernel introduce polynomial factors in index distances, which the strict exponential margin absorbs. Differentiated perturbations retain bounded trace norm; differentiated reference inverses retain bounded operator norm because the reference Hessians and their derivatives are uniformly banded. Endpoint differentiation reduces powers of endpoint size but not summability. The smooth-family hypothesis supplies the higher derivatives needed at each prescribed order.

I do not identify a missing estimate that invalidates the lemma. For a cleaner final exposition, the derivative induction could be packaged once as a precise parameter-dependent weighted-space lemma, rather than split between the circular and noncircular proofs. That is an exposition improvement, not a newly discovered obstruction.

### 4.4 Radial integration, marks, and moving onsets

Locator: `v2/11_integration_inverse.tex`, `lem:g-radial`, proofs of `thm:g-stability` and `thm:g-marked`, `cor:g-interfaces`.

The effective endpoint Hessian stays uniformly positive even though its off-diagonal entry is exponentially small. The two-dimensional matrix-square-root Morse construction consequently has a common domain. Coercivity puts the entire active sublevel inside it. No chart-boundary contribution is being discarded.

The exact residual-time integral is

$$\int_{|w|^2<2d}(d-|w|^2/2)\,dw=\pi d^2.$$

Combining this with the physical flux gives the printed coefficient 1/(2A sinh(j gamma)). Summing six equal circular contributions gives 3/(A sinh(j chi)), agreeing with the inherited circular theorem.

Nonsymmetric boundary jets do not produce a surviving relative square-root term in this integrated probability. The radial domain and weight are symmetric; replacing the smooth amplitude by its even part leaves the integral unchanged. An even smooth function of sqrt(d) is smooth on the right as a function of d, with each finite derivative controlled by sufficiently many endpoint derivatives. Thus the claimed relative O(d) remainder is compatible with cubic geometry.

Likewise, subtracting the axial mark value at each impact leaves a sum of endpoint-localized deviations with uniform derivatives. Odd terms cancel only after integration. The distinction between O(d) for the integrated marked normalization and O(sqrt(d)) for a general conditional latent density is correct.

The exact parity identity for the axial mark sum, together with positivity, proves both directions of the source-domain assertion. At equality a positive term does not decay; inside the strict domain parameter and source derivatives cost only polynomial factors in j. This is genuine summability of the stated onset series, not a pressure theorem.

Finally, the second-derivative jump is twice the leading channel coefficient times the square of the derivative of d. The printed jump and the addition of coincident oriented contributions are consistent. For a transverse gap crossing, the activation condition j(g_e-g_*)<epsilon indeed gives the scale epsilon/j.

### 4.5 Exact inverse identification

Locator: `v2/11_integration_inverse.tex`, `thm:g-inverse`, `eq:g-isogap-family`, `eq:g-mobius`.

At the lattice normals the support function equals R and its first derivative vanishes. Supporting-line separation gives the lower bound g=1-2R, and the axial contact points attain it. This proves exact equal gaps, rather than equality merely to first order. The three contact curvature radii are R+36b(theta_r), and their dependence on the three parameters has full rank.

Writing x_r=exp(-gamma_r), the amplitude formula is

$$C_j=\frac{2}{A}\sum_{r=0}^2\sum_{m\ge1,\ m\ {m odd}}x_r^{mj}.$$

Odd-index Mobius inversion is valid: absolute convergence permits collecting terms with the same odd product, and the divisor sum of the Mobius function leaves only product one. No conditional rearrangement is concealed here.

After this transform the sequence is a positive finite exponential sum. The Hankel factorization and generalized eigenvalue argument recover the distinct nodes. The shifted moments start at j=1, but that is harmless because every node is strictly positive. The weights recover multiplicities using the known total multiplicity three, and the formula A=6/sum(weights) is correct. Coalescent nodes are handled by the rank, not by pretending a singular three-by-three Vandermonde matrix is invertible.

The two-amplitude formula in the one-parameter symmetric subfamily is also correct. Consequently the old claim that the threshold spacing already determines all the asserted inverse data is no longer applicable. The limitations below concern what this correct identification amounts to, not a failure of its uniqueness proof.

### 4.6 Record response and historical separation

Locator: `v2/12_record_response.tex`, `prop:g-smooth-tests`, `prop:g-moving-cut`; `sections/06_records.tex`; `history/round33_A2.tex`.

The record array now has an explicit maximum norm. Requiring test derivatives to be bounded in the corresponding operator norms avoids the hidden dimension growth that an unnormalized Euclidean norm could introduce. Division by the scaling parameter extends smoothly because positions and transverse velocities vanish to first order and flight excesses to second order. The sum of the time errors is controlled by the summable bridge weights.

The response proof differentiates the exact latent parametrization and density. It does not differentiate a total-variation bound. For a moving cut eta>psi, Leibniz differentiation gives the boundary term -F(z,psi) times the parameter derivative of psi. The uniform interior margin excludes intersections with the other latent boundaries. The displayed example a=1/2, with support inside |z|<1/2, verifies that the test class is nonempty uniformly in the chosen impact index.

This resolves the previous response objection for the stated class. It does not establish uniform response for all fixed physical schedules or arbitrary discontinuous decoders, but the manuscript explicitly says so. Requiring those excluded assertions merely to manufacture a proof gap would be improper.

The inherited circular record theorem, renewal comparison, and companion remain consistent with these distinctions. The companion's regular terminal-level calculation is separate from an onset singularity. The Round 33 chapter proves an arithmetic estimate and a conditional Fourier-inversion budget; it expressly leaves model-level operator and central-remainder inputs open. The current article does not supply those inputs, and does not claim to. Failure to complete that different programme is not the sole or principal reason for the recommendation here.

## 5. New substantive assessments

### GTC-R1 — The geometric extension is genuine, but the significance argument still overcounts consequences

**Classification: major editorial objection; not a falsity finding.**

The active theorem is no longer limited to circles. Nevertheless, every contributing segment still alternates along one isolated normal period-two channel. The geometric deformation changes a gap, two endpoint curvatures, and higher-order local amplitudes. Competition between channels is resolved by summing their positive-part contributions. It does not require interacting histories or a new symbolic transition mechanism; the manuscript correctly acknowledges this.

Once the common bridge and relative determinant are available, radial integration, source convergence, onset jumps, conditional record convergence, smooth-test response, and exponential selection are comparatively direct consequences. Counting them as several independent conceptual advances exaggerates the breadth of the achievement. The paper's real case for importance must rest on the uniform local geometric theorem and what its data subsequently reveal.

A persuasive further development could be a sharp inverse or observability theorem for a less prescribed geometric uncertainty, or a quantitative result that separates what leading amplitudes, higher onset coefficients, and marks can identify. Another possibility is a genuinely reusable geometric criterion replacing closeness to a circle, with its nontrivial applications proved. These are examples of mathematical directions, not a requirement to add all of them, not a theorem that generality is always necessary, and not a promise of acceptance after another checklist.

### GTC-R2 — The inverse theorem identifies curvature, but its area recovery is not an additional independent geometric degree of freedom

**Classification: contribution calibration, supported by an explicit calculation; Theorem 12.1 is not contradicted.**

For the exact support family in the paper, the obstacle area can be computed without the count data. Since q=h n+h' t and q'=(h+h'')t,

$$|D|=\frac12\int_0^{2\pi}(h^2-(h')^2)\,d\theta.$$

Fourier orthogonality then gives

$$|D|=\pi\left[R^2+2R\alpha-\frac{33}{2}\alpha^2
-\frac{45}{4}(\beta^2+\zeta^2)\right]. \tag{R1}$$

To check the coefficients, h has mean R+alpha; its order-6 coefficient is -alpha; the order-2, order-4 and order-8 modes contribute respectively -3, -15/4 and -63/4 times beta squared plus zeta squared inside the Fourier sum. This produces (R1).

Put b_r=(kappa_r^{-1}-R)/36. The unordered triple already determines

$$\alpha=\frac{b_0+b_1+b_2}{3},\qquad
\beta^2+\zeta^2=\frac23\sum_{r=0}^2(b_r-\alpha)^2. \tag{R2}$$

Hence A=square root of 3 divided by 2 minus the quantity in (R1) is a symmetric function of the recovered curvature triple and the observed gap. In this chosen family it is not a fourth independent unknown. The algorithm's ability to eliminate an initially unsupplied normalizer is useful and correctly proved, but it must not be assigned the weight of an additional independent inverse invariant. The manuscript does not literally assert a fourth parameter; this calculation calibrates the importance argument rather than correcting a false dimension count printed in a theorem.

The real positive result survives intact: threshold locations alone leave three curvature parameters unresolved, and amplitudes distinguish them up to the stated loss of labels. That is the inverse contribution that should be defended.

### GTC-R3 — Exact multiplicity recovery conceals a concrete first-order loss of observability

**Classification: analytical limitation of the inverse application, not a counterexample to exact uniqueness.**

The paper explicitly disclaims noisy reconstruction. The following calculation shows that this caveat is substantive even inside its own geometric family, rather than a generic warning appended to every inverse theorem.

Fix R and take alpha=zeta=0, beta=s. The curvature radii are

$$(R+36s,\ R-18s,\ R-18s),$$

and (R1) gives

$$A(s)=A(0)+\frac{45\pi}{4}s^2.$$

For each j let

$$\Phi_j(r)=\operatorname{csch}\left(j\operatorname{arcosh}(1+g/r)\right).$$

Then the exact leading coefficient is

$$C_j(s)=\frac{\Phi_j(R+36s)+2\Phi_j(R-18s)}{A(s)}.$$

Its first derivative at zero vanishes: the numerator derivative is (36-18-18) times Phi_j'(R), and A'(0)=0. Thus for every fixed finite collection of collision orders,

$$\max_{1\le j\le J}|C_j(s)-C_j(0)|=O_J(s^2),$$

while the distance of the curvature multiset from the circular triple is of order |s|. No locally Lipschitz inverse from those finite amplitude vectors to that multiset can hold at the circular point. The simpler identity (x+h)^j+(x-h)^j-2x^j=O(h^2) expresses the same coalescence mechanism for exponential moments.

This does not refute recovery from exact infinite data, nor does it prove that useful quantitative recovery is impossible. It identifies a concrete regime a serious statistical inverse application must address. A sharp stability statement on separated-curvature strata, together with the correct behavior at coalescence, would add substantially more content than the present rank-and-Vandermonde argument. Without such a development, the inverse theorem remains an exact finite-dimensional identifiability result of limited depth.

### GTC-R4 — The general geometric theorem and the restricted curvature inverse should not be rhetorically merged

**Classification: scope and information-content distinction; the printed restriction is correct.**

For unequal endpoint curvatures, the leading channel amplitudes at known g and A depend only on

$$(1+g\kappa_0)(1+g\kappa_1).$$

At the level of these local data, replacing c0 by c0 times exp(s) and c1 by c1 times exp(-s) leaves every leading coefficient of that channel unchanged. This is an algebraic information bottleneck. It is not presented here as a constructed pair of globally isospectral billiard tables with all constraints simultaneously verified, and it is not a counterexample to the centrally symmetric inverse theorem. Central symmetry removes precisely this endpoint ambiguity by imposing equality of the two curvatures.

There is also an observation bottleneck away from equal gaps. A fixed nonminimal gap difference Delta>0 contributes to the ground-onset collar only while j Delta<epsilon. Consequently the complete unlabelled maximal-count data near the ground threshold eventually discard that channel as j grows. The separate own-threshold channel formulas require extra itinerary selection. The equal-gap construction avoids this difficulty by design.

The title and abstract are defensible when read with their explicit qualifications. The introduction should nevertheless identify these two restrictions immediately next to the inverse claim. The article has not shown general curvature recovery throughout its nonsymmetric open geometric class. A natural next mathematical question is which higher onset coefficients or additional marks resolve the product ambiguity and which nonminimal channels remain observable without labels.

### GTC-R5 — Attribution and architecture need a final, noncosmetic revision

**Classification: literature and exposition issues; not evidence that the main theorem is known.**

The newly added comparison with periodic rare-event statistics is appropriate. Carney–Nicol–Zhang study derivative-sensitive periodic clustering in a long-observation, shrinking-target regime [1]. This does not supply the complete physical onset formula here. The manuscript now makes that distinction adequately.

The recovery after Mobius inversion belongs to the theory of finite exponential sums, or Prony-type systems. Batenkov–Yomdin provide a pertinent primary reference for this algebraic reconstruction and its conditioning [2]. A citation would distinguish the specific billiard-to-amplitude theorem and odd-index transform from the classical Hankel/Vandermonde recovery machinery. The recommendation is not to replace the self-contained proof by a citation.

The inverse comparison should also acknowledge the more recent periodic setting. Finamore–Leguil's October 2025 preprint establishes rigidity for finite-horizon Sinai billiards from an enriched marked length spectrum [3]. Those data include more than the unlabelled threshold amplitudes considered here and are defined through a different construction. Their result neither contains the present theorem nor makes its observable redundant. It does mean that comparison only with open three-obstacle billiards is no longer an adequate account of the surrounding inverse literature. Bálint–De Simoi–Kaloshin–Leguil remain relevant for their recovery of period-two curvatures and periodic Lyapunov data from marked lengths [4].

The general relation between variational Hessians and monodromy is classical [5]; the paper correctly locates its own effort in the uniform relative use of that mechanism. That distinction should govern the entire contribution discussion.

Finally, the article currently states the geometric result, develops the old circular proof at length, and only then returns to the geometric proof. The two levels of argument obscure rather than strengthen the center of the paper. Prove the reusable boundary-value/relative-flux result once, present the geometric threshold theorem as its main application, and retain the circular formulas and their full details in a clearly identified specialization or appendix. Preservation of historical source files is compatible with a more coherent active article. No mathematical content needs to be arbitrarily deleted.

The scalar remainder H_{j,e} in the main theorem and the endpoint Hessian H_{j,e} in the action section also share notation. Rename one. This is a minor readability issue, not a mathematical flaw. State the scalar versus finite-dimensional parameter conventions and derivative norms once, and use them consistently instead of repeatedly re-establishing them in prose.

## 6. Independent diagnostic record and its limits

The accompanying `diagnostics.py` imports no repository code and makes no network calls. It completed **241 of 241** named checks in both ordinary Python and `python -O`; the full JSON outputs were byte-identical. The checks comprise **174 exact-rational, 20 exact-symbolic, and 47 non-interval numerical** checks. Explicit conditions, not removable Python assertions, determine the exit status.

The exact calculations cover alternating Schur complements and their relative determinant identity, source parity, support jets, the area formula above, a controlled finite Mobius truncation, and an elementary moving-boundary differentiation example with a nonzero boundary term. The numerical moment recovery includes distinct nodes and repeated nodes. The local nonlinear calculation uses unequal curvatures and non-even cubic jets, solves the stationary reflection equations, and evaluates the relative twist through logarithmic tridiagonal determinants at lengths through 256.

For the nonlinear local model the graph functions are

$$\psi_b(y)=\kappa_b y^2/2+a_b y^3/6+b_b y^4/24,$$

with gap 0.12, curvatures (2.1,2.5), cubic coefficients (0.8,-0.5), and quartic coefficients (40,30). This tests local facing arcs; it is not a construction or simulation of an entire periodic equilibrium billiard. The source formula and global localization are judged primarily from the written proof, not inferred from these local computations.

Independent endpoint radial quadrature solves the nonlinear sublevel boundary rather than using the author's exact Morse map. The ratios below divide the computed local-channel integral by the stated leading coefficient times d squared; the area cancels from the ratio.

| Complete flights j | d=0.0001 | d=0.00001 |
|---|---:|---:|
| 1 | 0.999557541668 | 0.999955732043 |
| 2 | 0.999700240379 | 0.999970016346 |
| 5 | 0.999734301041 | 0.999973425261 |
| 16 | 0.999735583328 | 0.999973553569 |

These values support the leading normalization and the cancellation scale. They are non-interval quadratures with explicit finite tolerances; they do not certify the remainder, all parameter derivatives, arbitrary collision order, or the complete equilibrium measure. The printed scaled quartic remainders are diagnostics, not additional passed theorem checks.

Execution environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. The exact executable Git blob is `340cb74c1952b63edcbce5936e6a55d5b7741dd7`; its SHA-256 is `ca9d21b8b49fb32d77b4d9c6c101d069eeedca7b9cb2bd37afffb7758b5cdc1a`. The full ordinary JSON output has SHA-256 `bc6a8dd9a0a0c6eed000bca21a8b7151ab20c4220d7e0ed5cc521dd93ce72df2`. Full output is regenerated by running the committed script; the committed verification record retains the counts, selected values, and hashes. Floating-point byte identity across other library versions is not promised.

The author's reported 328 new checks, 411 inherited checks, and 25+7-page native build were not replayed in this review. The previous referee's 125-check suite was not replayed either. No manuscript PDF rebuild or visual PDF inspection, interval proof, formal proof assistant, remote CI execution, exhaustive literature search, or complete audit of every historical derivation is claimed. The active mathematical main sources, complete unchanged companion, controlling report, current response, and preserved Round 33 chapter were read. The review distinguishes that source audit from unexecuted build claims.

## 7. Required disposition of this report

For a further submission, address each GTC item separately. Do not answer the editorial objection solely with counts of added pages, theorem blocks, or tests. State which part of the result is the main advance, attribute the reconstruction machinery, and explain what the recovered data distinguish in the actual admissible class. The area calculation and the circular coalescence calculation above should either be incorporated with their correct interpretation or answered mathematically.

No deletion of the established theorem is requested. No unsupported unrestricted long-time theorem should be added to create an appearance of greater scope. The existing hypotheses about smooth families, complete-event localization, relative flux, and the physical test class should remain explicit. A broader or deeper consequence must be proved rather than announced, and it need not be the entire historical A2 programme.

## 8. Primary literature consulted

[1] M. Carney, M. Nicol and H.-K. Zhang, *Compound Poisson law for hitting times to periodic orbits in two-dimensional hyperbolic systems*, Journal of Statistical Physics 169 (2017), 804–823. DOI: 10.1007/s10955-017-1893-9. Primary preprint: https://arxiv.org/abs/1709.00530. The current search returned the primary abstract; direct page/HTML retrieval attempts failed. This review does not claim a fresh full-text or PDF audit of its theorem numbering.

[2] D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), 134–154. DOI: 10.1137/110836584. Primary preprint: https://arxiv.org/abs/1106.1137. Used for the reconstruction/conditioning context, not as a claimed source of the present billiard threshold law.

[3] D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. Primary text: https://arxiv.org/html/2510.18983v1. The abstract and introduction were inspected in HTML. Its enriched marked data and finite-horizon assumptions differ from the present experiment. No claim about a later journal publication is made.

[4] P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Communications in Mathematical Physics 374 (2020), 1531–1575. DOI: 10.1007/s00220-019-03448-x. Primary preprint: https://arxiv.org/abs/1809.08947. The primary abstract was checked for the data, geometric setting, and recovery conclusions.

[5] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary preprint: https://arxiv.org/abs/1006.1532. The primary abstract was checked for the discrete variational and monodromy framework.

## Final disposition

**Reject at the requested top-four-journal level as presented.** The concrete geometric, nonredundancy, and scoped record-response requests from the preceding round have been substantially fulfilled. The main proofs are credible, and this review has not established a fatal error in their stated regime. The remaining objection is the depth and significance of the contribution actually extracted from the uniform local theorem. The exact area dependence, first-order coalescence degeneracy, and general curvature-product bottleneck make that assessment more precise; none should be misrepresented as disproving the restricted inverse theorem. Preserve the valid mathematics, but do not equate a longer list of correct corollaries with a demonstrated top-four contribution.
