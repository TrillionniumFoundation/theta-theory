# Independent referee report on A2 v13

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Date:** 10 September 2026. **Requested benchmark:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status:** author-requested, AI-assisted independent referee-style assessment. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Source and recommendation

This report reviews `revision/a2-v13-two-flight-relative-invariants-2026-09-10`, pinned at author commit **`0e54099f079232df233316ae6fe7986fc51b7ea1`**, dated 10 September 2026, 04:49:10 UTC. The manuscript directory is `papers/A2-v13-two-flight-relative-invariants`. The repository root tree is `41f68e02205e10d48e917559f0f5092c10799948`. The parent is the v12 review commit `2ae2751f61224b66f314915fd5fc22f6321b606f`; the preceding v12 author commit is `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`.

All manuscript paths below are relative to this v13 directory. TeX labels, rather than potentially changing display numbers, identify the statements definitively. Section and theorem numbers follow the author's current reading map; no independently compiled PDF numbering is claimed. Permanent source anchors appear in Section 11, and `SOURCE_AUDIT.json` records the actual reading coverage.

**Recommendation at the requested four-journal benchmark: reject in the present form on significance grounds.** This is my assessment of the completed contribution, not an assertion that the central theorems are false. **I found no fatal mathematical defect in the principal proof chain examined.** Nor did I find an unresolved instance of any of the three concrete v12 revision requests. I would not describe this as another round of major revision in which merely expanding the response letter will lead to acceptance.

These judgments must not be conflated. The revision is mathematically substantive, the new short-record theorem is properly proved, and the previously requested distinctions have been made. Nevertheless, after those distinctions are made, I am not persuaded that the combination reaches the exceptional significance required for my positive recommendation at the requested level. An editor or another specialist may judge that significance differently. This report supplies reasons for my judgment; it does not purport to certify a common editorial policy of four different journals.

## 2. What v13 has actually accomplished

The central result is a nonlinear relative law for selected near-onset records near a normal period-two channel. It controls a mixed endpoint derivative whose reference magnitude decays exponentially, uniformly on a collar that does not shrink with the number of flights. Its half-line factorization survives physical residual-time integration, with every fixed mixed derivative. This is more than a leading quadratic approximation.

The resulting two oriented same-type laws determine two complete symmetrized boundary energy profiles, not merely their formal Taylor series. Their mixed-type law is predicted by a Volterra compatibility identity. A weighted Abel coordinate gives a specified stable inverse topology, and a regularized binary-observation construction acquires the profiles while charging rare-event preparations and a separate normalization pilot.

In the independently even-contact class, the paper also establishes two invertible jet maps: one from limiting laws and one from two-flight laws. Their last-jet blocks remain invertible at coincident curvatures. The support-function construction realizes independent jet directions in actual analytic tables while preserving the selected leading hierarchy. At each fixed order, finitely many positive windows at two flights give a locally invertible physical probability map and a regular parametric experiment.

These are genuine results. The paper is not merely an abstract autoconvolution exercise, an identical-contact calculation, or a collection of formal perturbations lacking physical realization. Conversely, it is not a solution of unrestricted smooth billiard rigidity, a uniform growing-order reconstruction theorem, or an optimal infinite-dimensional statistical experiment. The revision now largely makes these boundaries explicit.

## 3. Disposition of the v12 requests

| Previous request | Evidence in v13 | Disposition |
| --- | --- | --- |
| R12-1: prove the independent-contact two-flight comparator and extract the direct finite-window consequence | `article/29_two_flight_benchmark.tex`, `thm:v13-two-flight`, `cor:v13-jet-coordinates`, `thm:v13-two-flight-observation` | **Closed.** The action, twist, moments, finite-jet dependence, recursion and physical experiment are supplied. The referee origin of the comparator is acknowledged. |
| R12-2: distinguish short-record finite-jet determination from the principal relative and smooth function-valued result | Abstract, introduction, especially Sections 1.1–1.2, and the finite-coordinate corollary | **Closed as a revision request.** The contribution is now stated accurately. Whether that completed contribution merits the requested journal level is a separate editorial judgment, addressed in Section 8. |
| R12-3: give a theorem-level spectral-rigidity comparison, rather than a generic assertion that observations differ | Introduction, `sec:v13-literature` | **Closed at the requested level of comparison.** Classes, data, supplied information, recovered objects and mechanisms are distinguished; the enriched spectrum is not silently replaced by ordinary periodic lengths. |

The previously closed objections concerning the integrated-flux two-derivative gain, structured versus unstructured errors, uncharged failures, an exact-family calibration oracle, measurable fitting, and smooth uniqueness versus equality of jets remain closed in the arguments examined. It would be unfair to restate them as current defects.

The new theorem should not be represented as an independently originated author discovery without qualification: the v12 report supplied the finite two-flight block and its observation consequence. The present manuscript explicitly acknowledges this and supplies its own full presentation. I see no attribution objection in the text examined.

## 4. Audit of the new two-flight argument

### 4.1 The finite action and its physical measure agree

**Source:** `article/29_two_flight_benchmark.tex`, `thm:v13-two-flight`; the phase formula in `v3/20_integration.tex`, `eq:g-full-flux`.

Fix a starting contact type b and write o = 1 − b. With endpoints u,v and intermediate coordinate w, the quadratic two-flight excess action is

$$
\frac{c_bu^2+2c_ow^2+c_bv^2-2w(u+v)}{2g},
\qquad c_b=1+g\kappa_b.
$$

The linear stationary point is w₀ = (u+v)/(2c_o). Eliminating it gives

$$
H_b=\frac1g
\begin{pmatrix}
c_b-(2c_o)^{-1}&-(2c_o)^{-1}\\
-(2c_o)^{-1}&c_b-(2c_o)^{-1}
\end{pmatrix}.
$$

For z = c₀c₁ − 1 and L_b = g/(2c_bz), its inverse gives

$$
\nu(u)=\nu(v)=L_b(1+2z),\qquad \nu(w_0)=L_o,
\quad \nu(\ell)=\ell^tH_b^{-1}\ell.
$$

Also det H_b = c_bz/(c_og²) = a_b² and the reference twist is d₂⁰ = 1/(2gc_o) = a_b/sinh(2γ). These normalizations agree with the earlier alternating Jacobi formula. In particular, the computation is not being carried out under an arbitrarily imposed endpoint density.

The exact normalized physical law is

$$
G_b(d)=\frac{a_b}{\pi d^2}
\int(d-E_2(u,v))_+b_2(u,v)\,du\,dv,
\qquad b_2=-W_{2,uv}/d_2^0.
$$

The first-residual interval is not clipped: on the chosen collar its length is less than the minimum roof, and another complete flight cannot fit after the final hit. The first-impact arclength factor cancels in the change from section position–momentum to endpoint coordinates. The source therefore retains the correct full-phase preparation measure.

### 4.2 Both the action and the twist must be varied

Keeping lower jets fixed, the first action variations are

$$
\partial_{q_{b,2m}}E_2
 =\frac{u^{2m}+v^{2m}}{(2m)!}+O(|(u,v)|^{2m+2}),
$$

$$
\partial_{q_{o,2m}}E_2
 =\frac{2w_0^{2m}}{(2m)!}+O(|(u,v)|^{2m+2}).
$$

The factor two counts the middle contact in both flights. Evenness makes the first orbit correction cubic, so it cannot change these leading varying terms. Differentiating in both endpoints then gives a zero own-contact twist contribution at the relevant degree and the other-contact contribution

$$
\partial_{q_{o,2m}}b_2
 =-\frac{g}{c_o}\frac{w_0^{2m-2}}{(2m-2)!}
   +O(|(u,v)|^{2m}).
$$

This is an essential term, not an optional amplitude correction. Retaining only the action would incorrectly replace the off-diagonal factor 1+2mz by 1.

The two ellipse moments used in the source are consistent. With E₀(y)=yᵗH_by/2 and I₀(d)=πd²/a_b,

$$
I_0(d)^{-1}\int_{E_0<d}(\ell\cdot y)^{2m}\,dy
 =\frac{2(2m)!\nu(\ell)^m}{2^m(m!)^2(m+1)}d^{m-1},
$$

$$
I_0(d)^{-1}\int(d-E_0)_+(\ell\cdot y)^{2k}\,dy
 =\frac{2\binom{2k}{k}\nu(\ell)^k}{2^k(k+1)(k+2)}d^k.
$$

The residual weight vanishes at the sublevel boundary, eliminating a first-variation boundary term. The common Morse-domain argument justifies the degree calculation: multiplying the first varying term by a lower nonlinear correction raises the normalized offset order. This is not an uncontrolled substitution of a quadratic domain for a nonlinear one.

Consequently, with k_m = 4/[2^m(m+1)(m!)²],

$$
D_{q_m}\xi_{m-1}=-
\begin{pmatrix}
(1+2z)^m&1+2mz\\
1+2mz&(1+2z)^m
\end{pmatrix}
\operatorname{diag}(k_mL_0^m,k_mL_1^m).
$$

The strict separating factor

$$
(1+2z)^m-(1+2mz)
 =\sum_{r=2}^m\binom mr(2z)^r>0
$$

proves invertibility for every m ≥ 2. There is no curvature-difference denominator. At g=1, c₀=c₁=2, m=2, the block is −(1/1728)[[49,13],[13,49]], with antisymmetric eigenvalue magnitude 1/48. The independent rational diagnostics reproduce this example and the general finite formulas on their stated grids.

### 4.3 The all-order statement is justified, but its quantifiers matter

The proof does not infer an all-order theorem from a finite list of checks. At each fixed degree, differentiating the stationary equation leaves the same positive scalar on its highest unknown derivative. The law coefficient uses action terms through degree 2m and twist terms through degree 2m−2, so no higher graph derivative enters. The last-jet derivative is independent of the last jet, giving affine dependence and the explicit recursive inverse.

Compact finite-order stability follows from positive denominators on positive leading-geometry boxes. It is not uniform in m or M. Equality of all recovered jets determines analytic even graph germs, but not arbitrary smooth graphs. The continuation argument for connected analytic boundaries is an exact arclength-curvature identity argument, not noisy reconstruction of distant points. These restrictions are present in the manuscript and are mathematically appropriate.

### 4.4 The finite-to-limiting coordinate comparison is exactly that

**Source:** `cor:v13-jet-coordinates` and `article/23_two_contact_rigidity.tex`, `thm:v12-two-contact`.

The limiting last-jet block has the form −[[P_m,Q_m],[Q_m,P_m]] diag(K_m,0,K_m,1), with

$$
P_m-Q_m=m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
$$

The half-line action and determinant sums give the stated unequal-curvature factors. In particular, K_m,b r_b^(2m)=K_m,1−b is needed to obtain the column scaling. Strict concavity of tanh gives the displayed separation, including equal curvatures.

For fixed M, composing the two already invertible triangular jet maps proves the analytic coordinate changes. This is a correct corollary. It neither equates finite and limiting law functions nor establishes an ordering of noisy experiments. It also supplies no uniform infinite-jet inverse. The manuscript explicitly avoids these three stronger claims.

## 5. Physical realization and the direct observation theorem

**Sources:** `article/24_physical_image.tex`, `thm:v12-realization`; `article/29_two_flight_benchmark.tex`, `thm:v13-two-flight-observation`.

The support-function realization gives genuine independent directions. Near the disk, the two perturbations [(1±cosθ)/2]sin^(2m)θ begin at order 2m at their selected horizontal contact and at order 2m+2 at the other. The area compensator begins at order 2M+2 at both contacts. Its area derivative at the disk is strictly positive, so the implicit-function argument preserves area exactly. The contact-to-support Jacobian has nonzero diagonal entries −(2m)!κ_b^(2m), and lower jets are unaffected by higher-order perturbations. Positive curvature and clearance survive after a small restriction. A uniform diameter bound reduces potential competing translates to a finite verification.

Thus the physical open image is not an assertion that arbitrary abstract profiles are realizable. It is a specific finite-dimensional analytic construction, near the stated lattice/disk geometry, with gap, area and both labelled curvatures fixed. This suffices for the physical alternatives used subsequently.

In the new observation theorem, use the two-flight jet coefficients Ξ as local coordinates and write, for n=M−1,

$$
G_b(d;\Xi)=1+\sum_{k=1}^{n}\Xi_{b,k}d^k+d^{n+1}R_b(d;\Xi).
$$

At positive nodes d=ℓh, the principal Jacobian blocks are V_h=((ℓh)^k). Since ||V_h^−1|| ≤ Ch^−n, the O(h^(n+1)) remainder becomes O(h) after preconditioning. A fixed small h establishes rank without any finite-to-infinite bridge approximation. Multiplication by the positive, parameter-independent physical normalizers preserves it. Restricting to a convex parameter ball where the preconditioned Jacobian stays close to the identity gives an actual bi-Lipschitz map, not just pointwise nonsingularity.

The Borel finite-net estimator and its deterministic high-confidence preparation count follow correctly from the finite vector of sample means. For the risk lower bound, the alternatives θ*±aN^−1/2v are actual tables in that same family. Fixed probability margins give a uniform quadratic Bernoulli entropy bound. Conditioning on the past and independent random seed makes the entropy chain rule valid for adaptive window choices; early stopping can be padded. The resulting testing argument gives c/N, matching the regular parametric upper bound.

The scope is important: the family, leading geometry and fixed finite window menu are supplied. Constants and windows may deteriorate with M. This does not prove a parametric rate for an unknown smooth contact family, a complete-profile lower bound, or minimality of two flights in every restricted model. The present text says so. R12-1 is therefore resolved by an actual strengthened experiment, not by a disclaimer.

## 6. Audit of the general relative and function-valued chain

### 6.1 Localization and the relative determinant are the central technical work

**Sources:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-relative`; `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`, `thm:v4-law`; `article/15_operator_comparison.tex`.

The localization argument uses the positive minimum inter-obstacle distance, finitely many minimizing pairs, unique closest segments and separated normal collision states. A total excess shorter than a fixed collar forces every flight to be short, and reflection then forces alternation. This is a local selected-channel statement; absence of a finite-horizon hypothesis here does not constitute a global infinite-horizon rigidity or mixing theorem.

The weighted bridge contraction gives endpoint-localized coordinates and differentiated bounds independent of the number of interior sites. The exact cofactor is normalized before taking a limit:

$$
b_j=\frac{\prod_i(J_i/J_i^0)}{\det(I+G_j\Delta H_j)}.
$$

Tridiagonality and endpoint decay imply a summable entrywise perturbation and hence a uniform trace-norm bound. In each term of the logarithmic determinant series, one factor is controlled in trace norm and the remaining factors in operator norm. Fixed differentiation preserves a trace-class factor. This avoids an artificial multiplier equal to the matrix dimension.

The two-boundary proof does not stop with a bound on that determinant. It glues the half-lines, controls the finite-minus-glued orbit in ℓ¹, truncates the perturbations to the first and last floor(j/3) sites, and controls remote-boundary reflections and cross-block Green kernels. The trace-norm error is exponentially small after polynomial factors are absorbed in a strict exponential margin. This produces relative convergence of b_j, not merely an absolute bound for W_j.

Finally, the positive endpoint Hessian supplies common Morse coordinates. The integration comparison uses sufficiently many endpoint derivatives for each requested offset derivative and exploits evenness of the integrated radial expression, without assuming even obstacle graphs. This gives the closed-collar physical convergence down to the onset. I found no step here that illicitly divides an uncontrolled absolute error by an exponentially small flux.

### 6.2 Complete smooth uniqueness is not being replaced by formal jets

**Source:** `article/20_boundary_compatibility.tex`, `thm:v9-compatibility`.

The signed Morse pushforward gives normalized positive profiles V_b and kernels k_b(x)=x^−1/2V_b(x). The observed integrated laws satisfy

$$
K_{bc}=(\pi/2)(d^2\mathcal F_{bc})''=k_b*k_c,
\qquad K_{01}*K_{01}=K_{00}*K_{11}.
$$

The constants, including K_bc(0)=π, agree with the quadratic normalization. For two candidates k,ℓ, set f=k−ℓ and a=k+ℓ. The leading singularity in a is 2x^−1/2. Convolution with x^−1/2 and differentiation reduce a*f=0 to 2πf+R'*f=0 with bounded R'. Gronwall proves uniqueness on the collar. This is a genuine smooth-function uniqueness proof, not a formal square-root argument.

The invariant sums the two transverse energy branches. The paper does not claim that this sum determines unrestricted asymmetric contact geometry. Abstract profile candidates used in the statistical upper bound need not be actual billiards; physical alternatives would be required for an accompanying geometric lower bound, which is not claimed.

### 6.3 The Abel inverse and preparation accounting remain correct in their stated setting

**Sources:** `article/21_abel_stability.tex`, `thm:v11-abel-inverse`; `article/28_regularized_observation.tex`, `lem:v12-gain`, `lem:v12-reconstruction`, `thm:v12-acquisition`, `thm:v12-self-calibrated`; `article/27_profile_calibration.tex`, `lem:v11-calibration`.

For integrated flux H, the linear Abel transform is

$$
(\mathscr AH)(x)=\frac\pi2\left[H''(0)+\sqrt{x}
\int_0^x\frac{H'''(s)}{\sqrt{x-s}}\,ds\right].
$$

Its affine nullspace is removed on physical flux differences by the zero initial value and slope. The weighted Volterra identity gives the claimed two-sided bounds; the geometric mean in the mixed estimate is used as an estimate, not incorrectly treated as the definition of a norm.

For the unchanged C^(m−1,1) profile class, the exact H'' identity gives two additional integrated-flux derivatives. The positive-node reconstruction uses m+2 nodes and obtains bias O(h^(m−1/2)) in the Abel seminorm. Structured C³ bridge/calibration errors are bounded without mesh amplification; scalar sampling errors receive the h^−5/2 factor. Mixing these two error mechanisms would invalidate the budget, but the source keeps them separate.

The Bernoulli variance retains the small success probability. With ν=m−1/2, h comparable to ε^(1/ν), t comparable to εh^(5/2), and τ^j comparable to ε, the deterministic sufficient preparation exponent is

$$
2+\frac6{m-1/2}+\frac{\gamma}{|\log\tau|}.
$$

At m=4 the part preceding the bridge contribution is 26/7. This is a sufficient exponent for the stated construction, not a minimax theorem or an intrinsic invariant of the table.

I also examined the actual smooth-class pilot, not just its invocation. Its one-sided onset bracket charges every trial; its widths shrink on bad histories as well. Positive-node extrapolation uses unknown smooth remainders, rather than a supplied exact-family probability oracle. With s comparable to ξ^(1/m) and gap accuracy ρ comparable to ξs, both bracketing and nodal estimation cost order ξ^−(2+2/m), up to the printed logarithm. The maps recovering area and multiplier are Lipschitz on the supplied positive boxes.

The profile stage has exact conditional mean R H_j(d+Δ), where Δ=j(ĝ−g)≥0. Its C³ translation estimate uses the supplied C^(3,1) flux bound. It does not divide by d² and thus does not create a spurious Δ/d singularity. Projection to the supplied boxes bounds the preparation charge even on pilot failures. The strict gap between the profile exponent and 2+2/m absorbs the pilot cost and fixed logarithmic powers. I found no reason to reopen the earlier calibration objection.

## 7. Literature comparison: what has and has not been checked

The revised introduction now compares mathematical statements rather than merely different terminology. The distinction between marked periodic lengths, an enriched marked spectrum, a Laplace spectrum and selected event probabilities is substantive. The same is true of the distinction between entire-table isometry and a contact/profile invariant.

For this review I independently checked the primary institutional publication record for De Simoi–Kaloshin–Leguil, the official Finamore–Leguil v1 HTML introduction and Theorem A with the enriched-data definition, and the official Annals abstract and bibliographic record for Zelditch. The detailed DSKL symmetry/nondegeneracy clauses and Zelditch class definitions printed in v13 were not independently re-audited from their complete proofs in this session. The author records a more detailed source examination in its own literature note; I do not relabel that examination as mine.

The verified comparison is consistent at the level needed here. The DSKL record describes analytic dispersing billiards with axial symmetry/genericity and global determination from marked lengths. Finamore–Leguil's cited theorem concerns diffeomorphic finite-horizon Sinai billiards with the same **enriched** marked spectrum and concludes isometry. Zelditch's publisher description concerns analytic symmetry classes and wave-trace/stationary-phase extraction from spectral data. None of these sources is being used as a theorem that already proves the A2 relative physical law. Conversely, A2 does not provide those sources' observations or global conclusions.

I read the manuscript's separate deautoconvolution comparison. It correctly notes that x^−1/2V(x), V(0)=1, is locally integrable but not square-integrable at the origin; an L² inverse theorem cannot simply be substituted without checking hypotheses. I did not independently re-referee all cited regularization papers.

This is targeted literature verification, not an exhaustive priority search. I found no source in this examination establishing duplication of the central A2 theorem. My negative journal-level recommendation is not a plagiarism or prior-publication finding, nor an assertion that an unidentified classical theorem subsumes this work.

## 8. Why I still withhold a four-journal recommendation

The revision has answered the comparison request. That does not oblige a positive judgment of the resulting contribution. My reservation is now about the completed mathematics, not about the absence of a paragraph explaining it.

First, the broad nonsymmetric theorem gives a carefully constructed invariant of a **selected local channel**. Its generality is real: it removes evenness and finite horizon from that local construction. The recovered object, however, is the symmetrized pushforward of an action-weighted half-line measure. The unrestricted smooth geometry is not determined by the stated result. This is a comparison of the actual targets, not a demand that a local theorem must become global to be valuable.

Second, the most substantial analytic work is the simultaneous, differentiated control of the nonlinear bridge, the relative determinant and the physical sublevel integral. It is well executed in the arguments examined. But the underlying proof architecture remains a localized contraction for a one-dimensional nearest-neighbor action, a trace-ideal logarithm estimate, and smooth Morse transport. In my assessment, the paper demonstrates an effective and technically complete application of this architecture rather than establishing a new general rigidity principle or a method whose wider force is already demonstrated here. This is an assessment of the written proof, not a claim that its simultaneous hypotheses follow for free or that a citation can replace the proof.

Third, the strongest geometric conclusion uses individually even analytic contacts and supplied labelled leading geometry. The two-flight block and the physical independent-contact image are useful, explicit contributions. Once the short-record calculation is available, however, their finite-dimensional observation consequence follows from a nonsingular finite mean map. The N^−1 risk does not supply additional exceptional significance beyond that map. The paper now recognizes this; I agree with that recognition rather than treating the statistical rate as a second independent breakthrough.

Fourth, the full-profile observation result closes a legitimate gap between exact invariant determination and finite preparations, including nuisance calibration. Its norm choice and bookkeeping are important. Its conclusion is nevertheless a sufficient bound under supplied regularity, collar, label and convergence certificates. It neither identifies an optimal experiment nor gives a matching physical infinite-dimensional lower bound. Again, these are not errors or newly imposed prerequisites; they delimit the strength of the statistical evidence actually available for evaluating the paper as submitted.

The positive counterweight is that these components fit together: the relative physical law supplies a nontrivial invariant, the Volterra argument identifies it, and the charged experiment makes that identification operational. A referee could reasonably attach more weight than I do to this combination. On the manuscript's present evidence, I regard it as a substantial specialized contribution but remain unconvinced of the exceptional mathematical reach needed for my requested-level recommendation.

It would be inappropriate to convert that judgment into an endless list of mandatory new theorems. This report does **not** demand unrestricted asymmetric rigidity, full-profile minimax optimality, growing-order stability, removal of every supplied certificate, or arbitrary deletion of valid material. It also does not promise that a further rewrite of the introduction will change the verdict. The three preceding revision requests are closed; the remaining disagreement is evaluative.

## 9. Limited author-facing clarifications

These points are minor and would not by themselves change the recommendation.

**C13-1 — State the normalization convention immediately before the finite inverse.** The section supplies g and the two curvatures, while its displayed definition of G_b also uses A. The theorem is valid when the normalized germs themselves are the input. For an exact unnormalized probability germ p_b, this normalization can be written G_b(d)=p_b(d)/(a₀d²), where a₀=lim_{d↓0}p_b(d)/d²=1/[2A sinh(2γ)]. A sentence separating this exact-data equivalence from finite-preparation calibration would remove a possible ambiguity. The physical finite-family theorem already supplies A, and the general pilot already charges its estimation; I am not alleging a hidden oracle in either proof.

**C13-2 — Make the current A2 entry point visible from the repository root.** The pinned root README emphasizes the A1 workstream. A short link to the current A2 native source and its exact review status would improve reproducibility. This is a navigation issue, not an objection to a theorem.

Keep the distinction between the earlier long-bridge finite-window construction and the stronger direct two-flight design visible. The v13 text already does this; no deletion of the former proof is requested. Likewise, retain the qualification that the full-profile exponent is sufficient and that the analytic continuation conclusion is exact, not noise-stable.

## 10. Independent verification and limits of this review

The accompanying `verify_review.py` was executed in ordinary and optimized Python. Both runs passed, and `checks.normal.json` and `checks.optimized.json` are byte-identical. It uses only the standard library and imports no author verification routine or manuscript code. It raises explicit exceptions rather than relying on assertions that optimized Python removes.

There are **2,757 finite exact-rational diagnostics**:

| Category | Checks | Scope |
| --- | ---: | --- |
| Two-flight block | 2,378 | Polynomial action variations, mixed-derivative twist, Gaussian-moment recurrence with exact ellipse conversion, covariance and block identities, binomial separation and the printed quartic example |
| Limiting block | 165 | Rationalized half-line sum identities, P±Q and positivity at the tested parameters/orders |
| Abel and profile algebra | 132 | Monomial linearization, endpoint normalization, exact Abel cancellation, finite-polynomial Volterra compatibility and coefficient recovery |
| Sampling algebra | 82 | Mesh/noise exponent balance, pilot power gap and the m=4 exponent |

For the finite block the grid uses three positive gap values, three c₀ values, three c₁ values, orders m=2,…,9 and both orientations. The limiting-block grid uses five rational values of exp(−2γ) and m=2,…,12. The checks test repeated structural identities; they are not thousands of independent proofs. In particular, the all-order argument is the mathematical argument in the manuscript and Section 4 above, not extrapolation from the grid.

Reproduction from this review directory:

```sh
python3 verify_review.py --output checks.normal.json
python3 -O verify_review.py --output checks.optimized.json
cmp checks.normal.json checks.optimized.json
```

Script SHA-256: `f69c9d3af8dae7411a14110fa0ec1a5754f96fd24e1988934440a86204a605e0`.

Either output SHA-256: `860a4184507a84c90b07d561e0ec4f46ed3c391be27a8d3d823e87b42593331c`.

Ordered diagnostic-identifier-list digest: `81939c49ab4175f9ef7621119f30aefa01201997bcfecf51e304df75ef521b58`. This last hash identifies the deterministic check list, not a certificate of the numerical identities or proofs.

The central source chain, the new Section 11, the main limiting-contact inverse, physical realization, compatibility/Abel arguments, regularized observation and the actual calibration lemma were read as described in `SOURCE_AUDIT.json`. The report does not certify all retained appendices, the two-collision companion, the historical eleven-paper program, or all bibliography proofs. Some historical/alternative material was read only in the indicated ranges.

I did **not** independently reconstruct the full native checkout, compile TeX, inspect PDF pages, run remote CI, rerun the author's 3,295-check suite, or verify the claimed byte-identical retention of all 212 earlier formal blocks. The author's 123-page build and preservation counts are author-reported metadata, not results of this review. The present exact checks are not nonlinear billiard simulations, proofs of infinite-dimensional smoothness, or certifications of concentration and minimax theorems.

## 11. Permanent source anchors

**[M13] Reviewed native source:** https://github.com/TrillionniumFoundation/theta-theory/tree/0e54099f079232df233316ae6fe7986fc51b7ea1/papers/A2-v13-two-flight-relative-invariants . All relative paths and TeX labels in this report refer to this immutable source.

**[R12] Previous report:** https://github.com/TrillionniumFoundation/theta-theory/blob/2ae2751f61224b66f314915fd5fc22f6321b606f/reviews/a2-v12-independent-harsh-two-flight-2026-09-10/REFEREE_REPORT.md .

**[A13] Author response:** https://github.com/TrillionniumFoundation/theta-theory/blob/0e54099f079232df233316ae6fe7986fc51b7ea1/papers/A2-v13-two-flight-relative-invariants/RESPONSE_TO_REFEREES.md .

**[P1]** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. DOI: `10.1007/s00222-023-01191-8`. Primary institutional publication record and abstract checked: https://research-explorer.ista.ac.at/record/12877 . The scope of this review's verification is stated in Section 7.

**[P2]** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, 21 October 2025. Official version-specific introduction, enriched-data definition and Theorem A checked: https://arxiv.org/html/2510.18983v1 . No assertion of later publication status is made.

**[P3]** S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI: `10.4007/annals.2009.170.205`. Official abstract and bibliographic record checked: https://annals.math.princeton.edu/2009/170-1/p06 . No full-proof audit of this paper is claimed.

## 12. Final disposition

V13 resolves the concrete v12 requests and contains a correct-looking, substantive main proof chain under its printed hypotheses. A severe review should recognize that progress instead of manufacturing a new fatal flaw or reopening closed objections.

My recommendation nevertheless remains negative at the requested four-journal benchmark, now as a judgment of significance on the completed merits. It is not a claim that the program is impossible, that the principal theorem has been disproved, or that the author has failed to supply the requested two-flight proof. The full report, reading audit and actually executed independent diagnostics are deposited together so that the next evaluation can start from these distinctions rather than another undifferentiated verdict.
