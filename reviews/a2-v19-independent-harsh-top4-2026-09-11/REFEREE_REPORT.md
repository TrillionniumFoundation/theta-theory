# Independent harsh referee-style report on A2 v19

**Manuscript:** Qian Qi, *Boundary laws, signed contact rigidity, and nonregular information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society  
**Author revision branch:** `revision/a2-v19-signed-endpoint-rigidity-2026-09-11`  
**Immutable author head reviewed:** `837d785dc92c22253aa8809e32d97dd6579aef3c`  
**Immediate review context:** `review/a2-v18-independent-harsh-top4-2026-09-11`  
**Active source manifest:** `papers/A2-v17-boundary-information-coarsening/ACTIVE_SOURCE_MANIFEST_V19.md`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any of the journals named above. I distinguish mathematical correctness, theorem scope, physical/statistical implementability, novelty/significance, exposition, and submission readiness. Source manifests, proof ledgers, response letters and CI metadata are audit aids only; I do not treat them as proof certificates.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested four-journal level.**

This recommendation is materially different from my v18 recommendation. V19 is not a cosmetic revision. It directly attacks the two substantive weaknesses that drove the v18 top-four rejection:

1. the general smooth inverse previously stopped at a symmetrized boundary profile, while the explicit all-jet inverse required individually even contacts and supplied leading geometry;
2. the statistical theorem previously concerned a fixed-table simple comparison rather than a local experiment in which the geometry itself is the parameter.

The new signed-endpoint theorem is a genuine strengthening. Under the explicitly printed assumption that the two contact frames are **labelled** and their signed endpoint coordinates are retained, the support threshold recovers the two unsymmetrized half-line actions. The resulting all-order last-jet block has determinant one and, at the formal level audited here, removes both the even-contact restriction and the supplied-curvature input. I did **not** find a direct mathematical contradiction in this new rigidity theorem under its stated fixed-frame hypotheses.

The abstract vector moving-support theorem is also a serious addition. Its logarithmic rate, information matrix, Gaussian likelihood limit, testing profile and local quadratic minimax value are internally consistent with the scalar coarea mechanism. Again, I did not find a simple counterexample to the abstract theorem as printed.

The decisive problem is the step from that abstract LAN theorem to the claimed **unknown-billiard physical experiment**. The active manuscript defines the geometric derivatives in channel-centered coordinates

` t = j g_e(eta) + d `

with `d` held fixed, and the new billiard likelihood is written in signed contact coordinates attached to the perturbed geometry. These are parameter-dependent coordinates and, in the centered-time case, a parameter-dependent experimental window. A statistical experiment for an unknown table must be formulated on a common observation space with a parameter-independent acquisition rule, or the paper must prove an asymptotic-equivalence/calibration theorem that justifies replacing the raw experiment by the centered one. The manuscript does not presently supply that theorem. The protocol paragraph says that physical windows can be chosen without observing an unknown gap and that pilots may be retained, but the v19 LAN proof does not propagate such a pilot/calibration construction through the local asymptotics.

There is a second, related proof gap in the asserted nonsingularity of the billiard information design. The signed-rigidity theorem explicitly uses **onset time** to identify the gap `g`; the endpoint-support laws recover the actions. By contrast, the kernel argument for the new information matrix uses only derivatives of those endpoint actions and concludes only that the tangent vector vanishes “on the graph-jet parameter space.” This does not prove positive definiteness on a local model that also allows the gap/onset coordinate to vary. The introduction and abstract use broader phrases such as “finite-dimensional family of unknown billiard geometries.” As written, one must either fix the gap (and all frame/calibration parameters), add the onset statistic to the LAN experiment, or prove separately that the endpoint family already identifies those missing directions.

These are not stylistic complaints. They sit exactly at the point where v19 tries to cross from a known mathematical boundary model to a physically implementable unknown-geometry experiment. Consequently I would not recommend a routine “major revision” carrying an implied route to acceptance at a four-journal venue. The new mathematics is substantially stronger than v18 and, after the gaps below are repaired, deserves a fresh significance assessment. In its current form, however, the headline statistical conclusion is not established at the level claimed.

## 2. Scope of this review

I reviewed the active v19 source graph at author head `837d785d...`, with emphasis on the new claims and on the dependencies promoted into the abstract and introduction. In particular I inspected:

- `main.tex` and `article/01_introduction_v19.tex`;
- `article/01c_geometric_setup_v18.tex`, especially the centered derivative convention;
- `article/01a_protocol_scope.tex` and the observation hierarchy;
- the retained nonlinear relative law and its half-line action/amplitude framework;
- `article/23_two_contact_rigidity.tex` as the predecessor all-jet calculation;
- **`article/23a_signed_endpoint_rigidity_v19.tex`** in detail;
- `article/18_boundary_information_v18.tex` as the scalar statistical base;
- **`article/18a_vector_boundary_information_v19.tex`** in detail;
- `PROOF_LEDGER_V19.md`, `RESPONSE_TO_REFEREE_V19.md`, `HISTORICAL_DERIVATION_AUDIT_V19.md`, `LITERATURE_VERIFICATION_V19.md` and `ACTIVE_SOURCE_MANIFEST_V19.md` as revision evidence;
- the v19 native-build workflow status.

I also compared the paper's claimed information set with the modern dispersing-billiard rigidity literature. Relevant benchmarks include the marked-length results of Bálint--De Simoi--Kaloshin--Leguil, the Inventiones result of De Simoi--Kaloshin--Leguil, Osterman's length-spectrum rigidity work, and the recent Finamore--Leguil enriched marked-length approach to Sinai billiards. These works use different data and hypotheses; none is an immediate substitute for the signed endpoint law here. They are nevertheless the appropriate scale for judging the strength of a top-four billiard-rigidity claim.

On the statistics side, I treated Smith's 1985 linearly vanishing endpoint regime, Ibragimov--Has'minskii, Hirano--Porter, and the newer parameter-dependent-support literature as prior mechanisms rather than as automatic objections. The question for v19 is not whether nonregular support-dependent asymptotics existed before—it did—but whether the paper proves a sufficiently new geometric experiment and whether the physical billiard specialization is correctly formulated.

As in the previous report, I did not independently machine-reprove every historical appendix theorem. The v19 review is deliberately concentrated on the new main theorems and on whether they really close the v18 blockers.

## 3. What v19 genuinely improves

### 3.1 C18-E1 is substantially closed: the signed endpoint record really is stronger

The new observation is elementary once stated, but it is mathematically consequential. For a same-type limiting endpoint law the density is positive on

`S_b(u) + S_b(v) < d`.

Since the amplitude is strictly positive, the support threshold

`T_b(u,v) = inf { d : (u,v) lies in the interior support }`

satisfies

`T_b(u,v) = S_b(u)+S_b(v)`

and therefore

`S_b(u)=T_b(u,0)`.

This cleanly explains why the earlier scalar onset profile could recover only a symmetrized energy invariant: endpoint-sign integration is the information-destroying map. Once signed endpoint positions in labelled frames are retained, the unsymmetrized action is observable.

This resolves an important conceptual weakness of v18. The stronger inverse does not arise from imposing more geometry; it arises from retaining a strictly richer component of the same physical collision record.

### 3.2 The leading geometry reconstruction is algebraically consistent

Let `a_b=S_b''(0)`. The retained half-line formula gives

`a_b = c sinh(gamma) / (g c_{1-b})`,  `c=sqrt(c_0 c_1)=cosh(gamma)`.

Hence

`a_0 a_1 = sinh(gamma)^2/g^2`,

and

`a_0/a_1 = c_0/c_1`.

If physical onset supplies `g`, the displayed v19 reconstruction

`gamma=asinh(g sqrt(a_0 a_1))`,

`c_0=cosh(gamma) sqrt(a_0/a_1)`,

`c_1=cosh(gamma) sqrt(a_1/a_0)`,

`kappa_b=(c_b-1)/g`

is correct. In particular the new theorem no longer needs the two contact curvatures to be supplied externally.

This point should be preserved in any revision. It is an actual strengthening, not repackaging.

### 3.3 The new odd/even all-jet block is plausible and structurally clean

For arbitrary degree `n>=3`, v19 claims that after the lower graph jets are fixed,

`D_{q_n}s_n = [[coth(n gamma), r_0^n csch(n gamma)], [r_1^n csch(n gamma), coth(n gamma)]]`

with `r_0 r_1=1` for the curvature-ratio factors denoted `frak r_b` in the manuscript. The determinant is therefore

`coth(n gamma)^2 - csch(n gamma)^2 = 1`.

The envelope calculation is the natural nonsymmetric extension of the even-jet computation already present in the v12 block: at the first degree at which `q_{b,n}` appears, variation of the stationary orbit does not change the new homogeneous degree, so one evaluates the pure endpoint powers along the linear half-line orbit. The geometric series give exactly the `coth/csch` entries.

I specifically looked for the obvious sign/label objection. It does **not** refute the printed theorem because v19 explicitly fixes **signed coordinates in two labelled contact frames**. If one quotient by contact exchange or forget endpoint signs, odd information is lost; but that is not the observation model stated by the theorem. Any future revision should retain this labelled-frame hypothesis prominently because it is essential.

Subject to the global coordinate issue discussed later for the unknown-parameter statistical experiment, I regard the deterministic signed-rigidity theorem as a real and credible advance over v18.

### 3.4 C18-E2 is addressed at the abstract statistical level

The new vector theorem moves from a one-parameter known-pair comparison to a finite-dimensional local parameter `theta in R^r` and defines

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`,

where `V=D_theta w_theta|_0`.

At

`n p_n delta_n^2 log(1/delta_n) -> 1`,

the theorem states the LAN expansion

`log dP_{n,h}^n/dP_{n,0}^n = h^T Delta_n - (1/2) h^T J_Sigma h + o_P(1)`

with `Delta_n -> N(0,J_Sigma)`.

The rate and coefficient are consistent with the linearly vanishing support mechanism. The proof truncates at

`q_n = delta_n log(1/delta_n)^(1/4)`.

Under the null, the omitted boundary strip has probability of order `q_n^2`; because `n p_n delta_n^2 log(1/delta_n)` is order one, the probability of seeing the omitted strip is `o(1)`. The leading score behaves like `V/w`, so its truncated second moment is logarithmic, its third moment is of order `q_n^{-1}`, and its fourth moment is of order `q_n^{-2}`. With the chosen truncation these give the stated CLT and quadratic-term concentration scales. The support-exclusive mass is order `delta_n^2` per successful observation, hence accumulated mass is order `1/log(1/delta_n)` and vanishes.

The Gaussian testing formula

`2 Phi(sqrt(h^T J_Sigma h)/2)-1`

is the correct total-variation distance for the corresponding equal-covariance Gaussian shift. The local quadratic minimax value `tr(W J_Sigma^{-1})` is also the standard Gaussian-shift value when `J_Sigma` is positive definite.

I therefore do **not** reject v19 because the abstract vector LAN theorem is obviously false. The major issue arises in its billiard realization.

### 3.5 The source architecture and novelty positioning are better than v18

`main.tex` now presents two main parts and sends the historical auxiliary modules through a single compendium entry point. This is a real improvement over the flat, dossier-like v18 input list. Likewise, `LITERATURE_VERIFICATION_V19.md` more responsibly separates classical parameter-dependent-support asymptotics from the specific geometric coefficient and billiard realization claimed here.

These changes do not by themselves establish top-four significance, but I regard C18-E3 and C18-E4 as **substantially improved** rather than simply repeated blockers.

## 4. Major mathematical/statistical blockers introduced by v19

### C19-M1 — the “unknown-geometry billiard LAN experiment” is written in parameter-dependent observation coordinates

This is the most important issue in the present revision.

The formal setup declares that geometric derivatives are taken in channel-centered coordinates

` t = j g_e(eta) + d `

with `d` fixed. Thus when the geometry `eta` changes, physical time `t` changes with the unknown gap `g_e(eta)`. The new endpoint likelihood is likewise written in signed contact coordinates centered on the participating contact frames of the geometry.

For deterministic comparison of a fixed table or for differentiating a geometrically defined family, such centered coordinates are legitimate. For a **statistical experiment with unknown eta**, however, the sample space and acquisition rule must be common across eta, or an explicit Markov-kernel/asymptotic-equivalence argument must transport the raw physical experiment to the centered one.

At present the manuscript moves directly from the abstract model

`f_eta,d(u,v) = C_eta,d B_{0,eta}(u) B_{p,eta}(v) (d-S_{0,eta}(u)-S_{p,eta}(v))_+`

to an “unknown billiard geometry” LAN conclusion. This suppresses two parameter dependences:

1. **time centering:** fixing excess `d` means selecting a physical time window centered at the unknown `j g_e(eta)`;
2. **spatial centering/orientation:** the signed endpoint variables are naturally expressed in the contact frames of the unknown table.

If instead one fixes laboratory coordinates and a physical time window independent of eta, the derivative of the support function is not simply

`-D_eta S_0 - D_eta S_p`.

It also contains the derivative induced by the moving onset and, unless the frames are externally calibrated, coordinate-motion terms. In particular, at fixed physical time the centered offset changes like `-j D_eta g_e`, which can be the dominant contribution as `j` grows.

`article/01a_protocol_scope.tex` does not close this gap. It states that a policy can select physical windows without observing an unknown gap and that pilot observations can be kept exact. That is a useful protocol principle, but the v19 LAN theorem never constructs such a pilot, never quantifies the pilot error relative to `delta_n`, never proves that re-centering by an estimated gap/frame is negligible in Le Cam distance, and never derives the displayed `J_d` from a parameter-independent raw experiment.

**Required repair.** The paper needs one of the following, stated and proved as a theorem:

- a LAN theorem directly for fixed laboratory endpoint coordinates and parameter-independent physical time windows, including all frame/onset derivatives; or
- a two-stage calibration theorem: use a charged pilot sample to estimate the channel, onset and contact frames, prove the calibration error is `o(delta_n)` in precisely the sense needed by the likelihood expansion, and then prove asymptotic equivalence between the raw physical experiment and the centered endpoint model; or
- restrict the statistical theorem to a calibrated local model in which the gap and the contact frames are known/fixed by design, and remove the broader “unknown billiard geometry” language.

Until one of these is done, `J_d` is an information matrix for a convenient parameterized boundary model, not yet the information matrix of the raw unknown-table physical experiment advertised in the abstract.

### C19-M2 — positive definiteness is proved only on the graph-jet directions, while gap/onset is a separate geometric coordinate

The second major issue can be seen entirely inside the manuscript's own logic.

The signed-rigidity theorem states:

- signed endpoint supports determine `S_0,S_1`;
- **if the physical time origin is retained, onset determines the gap `g`;**
- from `g` and the quadratic action coefficients one reconstructs the curvatures and then all jets.

Thus the theorem itself distinguishes endpoint-action information from onset information.

The information-matrix argument in `article/18a_vector_boundary_information_v19.tex` assumes a tangent vector `h` lies in the kernel of every endpoint matrix `J_{b,d}`. Positivity of the boundary weight gives

`D_h S_b(u)+D_h S_b(v)=0`

on every relevant level set. Taking `v=0` yields `D_h S_b(u)=0`. The manuscript then invokes the signed-rigidity block recursion and concludes that `h=0` “on the graph-jet parameter space.”

That final qualifier is doing essential work. Vanishing derivatives of the two actions prove injectivity only for the parameter directions for which the actions themselves are the complete coordinates after the leading geometry has been fixed appropriately. The preceding rigidity theorem needed onset to recover the separate gap direction. The present proof therefore does **not** establish positive definiteness for an arbitrary finite-dimensional family of unknown billiard geometries if that family includes gap/onset or other calibration directions.

I am not asserting that a gap-varying null direction must exist in every parametrization. I am asserting that the current proof does not rule it out, and the text claims more than the proof establishes.

**Required repair.** Choose one of the following clean formulations:

1. explicitly define the LAN parameter space as a finite-dimensional **contact-jet model at fixed gap and fixed calibrated frames**, and state positive definiteness only there;
2. augment the statistical observation by the onset/time-origin statistic and compute the joint local experiment/information contribution for `g`;
3. prove a new injectivity lemma showing that the full family of endpoint actions over the chosen physical design already detects the gap direction, without using onset.

The abstract and introduction must then use exactly the same parameter space as the theorem.

### C19-M3 — the finite-bridge LAN transfer is asserted at the product-TV level without a complete local-experiment statement

V19 writes that if `k_n` successful endpoint records are retained and

`k_n tau^{j_n} -> 0`,

then the product total-variation error between finite bridges and the boundary model vanishes, and hence the boundary LAN experiment transfers to actual long bridges.

The basic inequality is plausible: if one has a **uniform one-observation TV bound** of order `tau^j` on a common sample space, product TV is at most of order `k tau^j`. The retained relative law is strong enough that such a result may well be obtainable.

For a top-four statement, however, the paper must make explicit which theorem supplies the one-record TV bound **uniformly in the local alternative `eta=delta_n h` and in the selected windows**, with the failure atom included. This becomes especially important after C19-M1: the existing relative theorem is differentiated in centered variables, whereas the desired statistical experiment must use a parameter-independent physical observation rule.

The raw-preparation formulation also requires the success probability to be part of the common experiment. If the design or the centering varies with eta, the Bernoulli failure component itself can carry local information and its derivative must be included rather than silently treated as a fixed thinning probability.

**Required repair.** State a finite-bridge Le Cam-distance/deficiency theorem, not only a sentence about multiplying TV errors. The theorem should specify:

- the raw observation space;
- the parameter-independent acquisition policy;
- the success/failure atom and its eta dependence;
- the local parameter range `h in K`;
- the exact uniform single-record bound;
- the condition on `(n,j_n,delta_n)` under which the product experiment is asymptotically equivalent to the boundary LAN experiment.

This would turn the transfer from an attractive heuristic corollary into a theorem strong enough to support the abstract.

### C19-M4 — “efficient estimator” is a local central-sequence estimator, not yet an implementable unknown-table procedure

In the abstract boundary model the estimator

`hat h_n = J_Sigma^{-1} Delta_n`

is completely natural: LAN is formulated around the known reference `theta=0`, so the central sequence and `J_Sigma` are evaluated at that base point.

In the billiard application, however, the prose repeatedly speaks of an “unknown geometry.” If this is intended as an actual estimation procedure over an unknown table rather than a local asymptotic benchmark around a specified reference table, then the score, support function, contact frames and information matrix are themselves unknown.

This is not a defect in LAN theory—local asymptotic minimax statements are routinely centered at a fixed base parameter. It is a defect of **interpretation** if the paper calls the displayed central-sequence object an implementable estimator for an unknown billiard without a localization/pilot step.

The revision should either call it what it is—an efficient estimator in the local experiment centered at a specified reference geometry—or provide the preliminary localization and plug-in argument needed for a data-driven procedure.

I rank this below C19-M1 and C19-M2, but it should be fixed in the same rewrite.

## 5. Audit of the abstract vector boundary-LAN theorem

Because the principal objections above concern the billiard specialization, I record why I do not presently see a fatal error in the abstract theorem itself.

### 5.1 Boundary score scaling

For `f_theta=a_theta(w_theta)_+`, the interior score at zero is

`S = D_theta log a_theta|_0 + V/w_0`.

Under `f_0=a_0 w_0`, the singular quadratic score contribution is

`a_0 V V^T / w_0`.

Coarea therefore gives the logarithm

`J_Sigma log(1/q)`

with exactly the matrix printed in the theorem. Lower-order amplitude and tangential terms contribute only `O(1)` to the truncated second moment.

### 5.2 Truncation is compatible with the local rate

With

`q_n=delta_n L_n`, `L_n=log(1/delta_n)^(1/4)`,

one has under the baseline law a boundary-strip probability `O(q_n^2)`. Thus

`n p_n q_n^2 = O(L_n^2/log(1/delta_n)) = o(1)`.

The largest normalized singular score on the truncated set is of order `1/L_n`, giving Lindeberg. The third- and fourth-moment orders used to control the likelihood remainder and `Q_n` are also compatible with this choice.

The uncentered truncated score has a small bias because the omitted strip contributes order `q_n` to the first moment; after multiplication by `n p_n delta_n`, that bias is order `L_n/log(1/delta_n)=o(1)`.

### 5.3 Moving-support exclusivity is negligible at this rate

A linearly vanishing density assigns quadratic mass to a support strip of width `delta_n`. Therefore the support-exclusive probability accumulated over the sample is of order

`n p_n delta_n^2 = 1/log(1/delta_n) -> 0`.

This justifies contiguity at the logarithmic LAN scale and distinguishes the theorem from genuinely endpoint-dominated regimes with non-Gaussian limit experiments.

### 5.4 What should be expanded in a top-four proof

The proof is currently compressed. For a theorem that is meant to carry part of the paper's significance, I recommend making the following explicit rather than referring to “the same bounds as the scalar proof”:

- a vector-valued collar lemma with uniform constants on compact `h`-sets;
- the centering estimate for the truncated score;
- the uniform matrix LLN for `Q_n`;
- a stated compact-uniform likelihood-ratio lemma;
- the precise experiment-convergence theorem used for the minimax lower bound;
- the uniform-integrability step needed for risk attainment.

These are not presently counterexamples, but at four-journal standard the vector theorem should stand on its own rather than read as bookkeeping attached to the scalar case.

## 6. Top-four significance after v19

V19 deserves a substantially more favorable significance assessment than v18, but I still do not think the current manuscript clears the requested bar.

### 6.1 The geometric theorem is now genuinely strong locally

The signed-endpoint result removes the most artificial hypotheses from the local jet inverse. It recovers arbitrary labelled smooth contact jets, odd and even, without assuming equal contacts, reflection symmetry or supplied curvature. In the analytic class it determines the participating contact germs, and with connected analytic boundaries it continues those local germs to the boundary images in their fixed contact frames.

This is no longer accurately described as merely a symmetrized-profile inverse. C18-E1 should therefore **not** be recycled against v19.

### 6.2 But the information set remains highly localized and labelled

The theorem uses a selected closest-pair channel, labelled contacts, signed endpoint coordinates and the onset structure of long alternating bridges. It does not recover unobserved obstacles or a global table from one local channel. That is perfectly legitimate mathematics, but it is a narrower rigidity statement than the strongest modern marked-length/spectral results.

For comparison, De Simoi--Kaloshin--Leguil obtain analytic billiard determination from marked-length data under symmetry/genericity hypotheses; Osterman relates marked-length data to analytic conjugacy near a homoclinic orbit and obtains recovery results for scatterers; recent Finamore--Leguil work studies global rigidity for Sinai billiards using an enriched marked-length spectrum. The data are different, so there is no direct implication either way. The comparison nevertheless shows that a four-journal case must explain why the **new physical endpoint information set and the relative-law mechanism** constitute a conceptual advance of comparable depth, not merely why the theorem is not covered by those papers.

The introduction is moving in that direction but is not yet there.

### 6.3 The statistical theorem is interesting, but the generic mechanism is not itself top-four novelty

Smith's linearly vanishing endpoint regime already exhibits the borderline normal/nonregular behavior; Ibragimov--Has'minskii and Hirano--Porter supply broad frameworks for singular and parameter-dependent-support experiments. The v19 hypersurface coefficient and vector matrix are useful and, as far as this review established, not trivially copied from those sources. Still, the proof mechanism is a coarea reduction plus a truncated-score triangular-array LAN argument.

That would be an elegant theorem in a strong paper. It is unlikely by itself to justify Annals/Acta/Inventiones/JAMS.

The potential top-four feature is the **coupling**: a nonlinear billiard relative law creates a linearly vanishing endpoint model; signed support gives full local geometric injectivity; that injectivity then should force a nonsingular information design; and the finite bridge should inherit a sharp local experiment. If that full chain were formulated on a genuine raw physical observation space and proved without calibration gaps, the editorial case would be materially stronger.

At present C19-M1 and C19-M2 break the chain at precisely that point.

### 6.4 The article architecture is improved but still overinclusive

The single auxiliary compendium is much better than v18's flat module list. I no longer regard source navigation itself as a decisive rejection reason.

However, the paper still compiles an unusually broad historical research dossier: adaptive experiments, acquisition/calibration schemes, profile inversion, minimax side results, multiple finite benchmarks and earlier comparison theorems remain in the active article. Once the v19 main chain is fixed, the author should seriously consider whether all historical consequences belong in the submitted article. A top-four paper can be long, but every section should reinforce the main conceptual theorem rather than document the full development history.

I classify this as an editorial weakness, not a mathematical blocker.

## 7. Literature and originality audit

`LITERATURE_VERIFICATION_V19.md` is a meaningful improvement over v18. It explicitly concedes that parameter-dependent support, nonregular normality, general Le Cam methods and generic optimal testing are not new. That is the correct posture.

For submission at the requested level, I would still strengthen the audit in two directions.

First, the statistics comparison should be theorem-to-theorem rather than topic-to-topic. In particular, identify the precise one-dimensional “linear vanishing” model corresponding to the logarithmic rate, state which ingredients of the vector hypersurface theorem are genuinely absent from Smith/Hirano--Porter and later support-dependent efficiency work, and explain whether the matrix `J_Sigma` can be obtained by localization/polarization of existing differentiability-in-quadratic-mean results at the borderline exponent.

Second, the billiard section should compare the exact information content of the signed endpoint law with modern marked-length/marked-Lyapunov/enriched-length data. The question is not only “different data?” but “strictly weaker, stronger, incomparable, or locally transformable?” A clean proposition or discussion locating the endpoint-support germ in that information hierarchy would significantly improve the originality case.

I did not find, in the search performed for this review, a published source that obviously states the manuscript's exact determinant-one signed action block together with the hypersurface information matrix and finite-bridge transfer. That is **not** an exhaustive priority certification.

## 8. Submission-readiness defects

### C19-R1 — there is still no successful native full build at the reviewed head

The v19 workflow `A2 v19 complete native build` has run `34577476783`, but the run concluded `failure`. The response letter records that the job failed before runner steps executed and therefore does not interpret the failure as a TeX error. That distinction is fair.

Nevertheless, from a referee/submission perspective the result is simple: there is still no successful native compilation evidence for the active manuscript. Moreover, the reviewed author head `837d785d...` is later than the workflow head `1f3bc3f...`.

This is not a mathematical objection, but it must be closed before submission. A successful build should verify the actual reviewed head, all references/citations, duplicate labels, bibliography and the complete source graph.

### C19-R2 — `VERIFICATION_V19.json` is referenced by the manifest but absent at the reviewed head

`ACTIVE_SOURCE_MANIFEST_V19.md` says `VERIFICATION_V19.json` is to be present once execution/build evidence is recorded. At the reviewed head that file is absent. The absence is consistent with the failed workflow, but the source manifest should not leave submission status ambiguous.

Either generate the verification record from an actually successful build or state explicitly in the manifest that native verification remains open.

### C19-R3 — the “unknown geometry” wording is broader than the theorem proved

This is partly a presentation consequence of C19-M1/M2. Until the raw-experiment and gap-direction issues are solved, phrases such as

- “unknown billiard geometries,”
- “finite physical endpoint design,”
- “efficient estimator,”
- “actual positive-offset billiard experiment”

should be qualified as local statements around a calibrated reference geometry, with the exact fixed/nuisance coordinates listed.

The abstract should be the last thing broadened, not the first.

## 9. Required revision program

I would require the following before reconsidering the paper at anything like the requested level.

### Blocker 1 — formulate the raw physical statistical experiment

Give a theorem whose observation space is expressed in parameter-independent laboratory variables. Specify what the experimentalist knows before seeing the data, how the channel is selected, what time window is used, what endpoint coordinates are recorded, and which calibration variables are fixed or estimated.

### Blocker 2 — close the gap/onset information direction

Either fix `g` in the LAN parameter space, add onset data to the local experiment and derive its joint information, or prove endpoint-only injectivity including `g`. The information-matrix theorem and the abstract must state the same parameter space.

### Blocker 3 — prove calibration/asymptotic equivalence if centered coordinates are retained

If the author wants the elegant centered support `d-S_0-S_p`, introduce an explicit pilot/sample-splitting or adaptive calibration theorem and show that replacing the unknown onset/contact frame by its estimate perturbs the experiment by `o(1)` in Le Cam distance at the logarithmic LAN scale.

### Blocker 4 — state a finite-bridge local-experiment transfer theorem

Replace the informal product-TV sentence by a uniform theorem for `eta=delta_n h`, including failure probabilities and a parameter-independent design. The conclusion should be convergence/equivalence of experiments, not merely pointwise density approximation.

### Blocker 5 — make the vector LAN proof self-contained at theorem level

Promote the vector collar/moment/uniformity lemmas into explicit statements and give the exact local asymptotic minimax theorem being invoked. This is necessary because the vector theorem is now a headline result.

### Blocker 6 — sharpen the top-four positioning

After the physical LAN chain is repaired, rewrite the introduction around one dominant theorem package:

**relative boundary law -> signed local rigidity -> physical unknown-geometry local experiment**.

Everything not needed for that chain should be moved to a companion paper/appendix only if it materially shortens and clarifies the article. Compare the new information set directly with the strongest billiard-rigidity benchmarks rather than presenting a list of adjacent literatures.

### Blocker 7 — obtain a successful native build of the final source head

No top-four submission should rely on an unexecuted/failed CI record for a manuscript of this source complexity.

## 10. Status of the previous v18 objections

| Previous issue | v19 status | Referee assessment |
|---|---|---|
| C18-E1: general smooth inverse weaker than even-contact all-jet inverse | **Substantially closed** | Signed endpoint supports recover unsymmetrized actions; new determinant-one all-jet block removes evenness and supplied-curvature assumptions, conditional on labelled signed frames and onset for `g`. |
| C18-E2: fixed-table simple statistical experiment only | **Closed abstractly, not yet physically** | Vector LAN treats geometry as a parameter in a boundary model, but the raw unknown-table billiard realization has C19-M1/M2 gaps. |
| C18-E3: dossier architecture | **Improved** | Two-part main chain plus one auxiliary compendium is materially better; still overinclusive, but no longer my principal rejection ground. |
| C18-E4: novelty audit too weak | **Improved but not complete** | V19 concedes classical mechanisms and adds relevant literature; theorem-level comparison remains needed. |
| C18-M1: notation overload | **Closed** | No renewed objection. |
| C18-M2: centered geometric derivatives not explicit | **Closed as notation; creates a new statistical issue** | The convention is now explicit, which reveals C19-M1 when `eta` becomes unknown. |
| C18-R1: no successful native build | **Open** | V19 workflow failed before steps; no successful full build at reviewed head. |

## 11. New v19 verdict matrix

| Item | Severity | Status |
|---|---:|---|
| C19-M1 parameter-dependent centered time/contact frames in the unknown-geometry LAN claim | **Major / decisive** | Open |
| C19-M2 endpoint information proof does not include the separate gap/onset direction | **Major / decisive** | Open |
| C19-M3 finite-bridge LAN transfer not formulated as a uniform raw-experiment theorem | **Major** | Open |
| C19-M4 efficient central-sequence estimator overinterpreted as an implementable unknown-table estimator | Moderate | Open |
| Signed-endpoint support recovery of `S_b` | Major positive result | Pass under printed labelled-frame hypotheses |
| Leading curvature reconstruction from `g,a_0,a_1` | Major positive result | Algebraically consistent |
| All-order signed jet block and determinant one | Major positive result | No direct defect found in this audit |
| Abstract vector boundary-LAN rate/matrix/testing profile | Major positive result | Internally consistent; proof should be expanded |
| Top-four originality/significance after v19 | Editorial | Promising but not established while the physical LAN chain is incomplete |
| Native full build at reviewed head | Submission blocker | Open |

## 12. Bottom-line mathematical assessment

A harsh report should distinguish a failed idea from an unfinished theorem. V19 is **not** a failed idea.

The signed-endpoint rigidity mechanism is clean and materially stronger than the v18 inverse. The simple identity

`T_b(u,v)=S_b(u)+S_b(v)`

turns the endpoint support into an unsymmetrized dynamical action, and the determinant-one last-jet block gives a convincing route to arbitrary labelled smooth contact jets. This is the strongest new geometric contribution in the revision.

The vector boundary-LAN theorem also appears mathematically viable as an abstract local experiment for linearly vanishing moving supports. The information matrix is the natural hypersurface coefficient and the logarithmic normalization is consistent with the borderline singular score.

What is not yet proved is the statement that these pieces combine into the claimed **physical unknown-billiard LAN/minimax experiment**. The paper differentiates in coordinates that track the unknown geometry and then treats the resulting model as though it were already the raw statistical experiment. It also uses endpoint-action injectivity to claim positive information on a parameter space broader than the graph-jet directions actually handled by the kernel proof, despite separately using onset to identify the gap.

Those two gaps sit in a headline theorem, not in an appendix. They prevent acceptance in the present form.

## 13. Editor-only recommendation

If this manuscript were submitted to one of the four journals named above in its current form, I would recommend **reject** rather than “major revision.” My reason is not that the v19 mathematics is uninteresting; on the contrary, the revision has crossed an important threshold relative to v18. The reason is that the principal new top-four significance claim—the transition from local signed rigidity to a sharp physical statistical experiment for unknown geometry—is not yet established on a parameter-independent observation space and is not yet injective in every geometric direction advertised.

If a subsequent manuscript closes C19-M1 through C19-M3 with a clean raw-experiment theorem, incorporates onset/gap correctly, and then presents the relative-law/signed-rigidity/LAN chain as one unified result, I would regard that as a genuinely new revision requiring fresh evaluation rather than as another cosmetic response to the same rejection.

At that point the editorial question would become one of **significance and conceptual reach**, not basic theorem formulation. In v19, theorem formulation still comes first.
