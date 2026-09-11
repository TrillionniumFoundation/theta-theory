# Independent harsh referee-style report on A2 v23

**Manuscript:** Qian Qi, *Boundary laws, intrinsic rigidity, and multiscale physical information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the American Mathematical Society*  
**Author revision branch reviewed:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Canonical manuscript-source commit declared by the revision:** `8840bf01ee8a7752504d2913bf00af54656afbb5`  
**Immediate predecessor report:** `reviews/a2-v22-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Principal manuscript entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and it is not an editorial decision by any journal named above. I treated the response letter, manifest and verification record as audit aids, not as proof certificates. I re-read the new v23 modules against the active v22 dependencies and against the objections in the preceding report.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested top-four level, with encouragement to resubmit only after another mathematically substantive reconstruction.**

This is a materially more favorable mathematical assessment than the v22 report, even though the formal recommendation remains negative. V23 genuinely resolves the main registration defect in v22. The new periodic gluing/holonomy formalism is not a cosmetic rewrite: the channel frames are no longer supplied in one common laboratory, obstacle symmetries are exposed as actual inverse ambiguities, nonzero deck holonomy can anchor the marked lattice orientation, and a rooted signature-rigid spanning tree gives a concrete propagation mechanism. I therefore do **not** repeat the v22 complaint that the global theorem simply assumes all relative channel placements.

V23 also does real work on the physical statistical side. The endpoint--time record has a plausible non-dominated Poisson boundary limit at the `k^{-1}` support scale, and retaining waiting counts after residual-time coarsening produces a coherent faster hyperbolic Gaussian direction at `(j sqrt(k))^{-1}`. The displayed simultaneous regime in `18e_compatible_rates_v23.tex` is nonempty, so I do not see a hidden inconsistency among the stated asymptotic rate conditions.

Nevertheless, I do not think the present manuscript is ready for any of the four journals listed above. My negative recommendation rests on three issues.

1. **The new endpoint--time theorem claims full Le Cam asymptotic equivalence, but the reverse-deficiency argument is only sketched.** The proof establishes the rare boundary-layer Poisson approximation and argues that the bulk likelihood is asymptotically deterministic, then jumps to a parameter-independent reconstruction kernel by saying that one can generate the bulk from the reference conditional law. For a principal non-dominated local experiment this is not enough at the requested standard. A uniform conditional total-variation/Hellinger lemma and an explicit kernel are needed.

2. **The promised physical-to-global statistical bridge remains conditional rather than proved for the paper's actual analytic billiard class.** The diagonal theorem assumes that every fixed finite action-jet vector is uniformly consistently estimable over a compact analytic class. The preceding local asymptotic theory does not prove this global uniform-consistency premise. More pointedly, the finite-jet physical realization used by the statistical theory is built with compactly supported smooth bumps and explicitly states that it is separate from the analytic continuation theorem. Thus v23 has an abstract compactness bridge, but it still does not supply an end-to-end theorem from the actual finite-bridge observation to global analytic table consistency.

3. **The headline phrase `fully intrinsic periodic table rigidity` is stronger than the actual inverse problem solved.** The new theorem fixes from the outset a marked abstract lattice with a **known Euclidean Gram form**. One nonzero holonomy vector then determines only the orientation-preserving realization of that already metrized lattice relative to a channel frame. The lattice metric (scale and shape) is not recovered from the endpoint data. This is mathematically legitimate if the lattice metric is declared ambient calibration, but it is a substantial scope restriction for a theorem advertised as complete intrinsic recovery of the periodic table. Moreover, the general `G_per(D)` classification is close to a repackaging of the set of globally admissible placements; the genuinely nontrivial global theorem is the singleton criterion under a lattice-anchoring cycle and a signature-rigid spanning tree. The manuscript should calibrate both the claim and the top-four significance accordingly, or recover more of the ambient periodic geometry from the observations.

I also note that the exact-head native-build workflow remains uncertified: the recorded run and rerun both fail with `steps=null`, before checkout or any TeX/numerical step. This is an infrastructure failure, not evidence of a mathematical or TeX error, but it means there is still no successful canonical submission build.

My overall assessment is therefore:

> **V23 contains serious and apparently original mathematics, and it fixes the most important conceptual defect of v22. I do not presently see an algebraic contradiction in the new holonomy theorem or in the two-speed scale calculations. The remaining objections are deeper: one principal Le Cam equivalence is underproved, the global statistical conclusion is conditional on a uniform estimation theorem not established for the analytic physical class, and the global `intrinsic` theorem still treats the Euclidean lattice metric as known background. At a specialist-journal level these may be repairable qualifications; at Annals/Acta/Inventiones/JAMS level they prevent acceptance in the current form.**

## 2. Scope of this review

I concentrated on the theorem interfaces that changed from v22 to v23 and on the inherited results on which they depend. In particular I inspected:

- `papers/A2-v17-boundary-information-coarsening/main.tex`;
- `article/01_introduction_v23.tex` and the observation-hierarchy discussion;
- `article/23b_intrinsic_multichannel_rigidity_v23.tex`;
- `article/23c_analytic_continuation_v23.tex`;
- the accepted v22 all-order signed endpoint inverse `23a_signed_endpoint_rigidity_v22.tex` at its interfaces with v23;
- `article/18c_full_endpoint_time_information_v23.tex`;
- `article/18d_count_endpoint_multirate_v23.tex`;
- `article/18e_compatible_rates_v23.tex`;
- `article/18b0_anchored_realization_v22.tex` and `18b_raw_physical_multirate_v22.tex`;
- `article/25_analytic_global_bridge_v23.tex`;
- the stopped finite-to-boundary transfer dependencies retained from v22;
- `responses/a2-v23-referee-response-2026-09-11/RESPONSE_TO_REFEREE.md`;
- `A2_REVISION_V23_MANIFEST.md` and `A2_REVISION_V23_VERIFICATION.md`;
- the full v22 referee report, to distinguish resolved objections from surviving or newly exposed ones.

For significance calibration I also checked the current rigidity landscape represented by De Simoi--Kaloshin--Leguil, *Inventiones Mathematicae* 233 (2023), and the 2025 Finamore--Leguil work on enriched marked-length rigidity for finite-horizon Sinai billiards. These use different observation architectures, so I do not claim a direct dominance relation. They are relevant because the requested venue level requires the paper to make very clear what geometry is recovered from what genuinely intrinsic data.

I have not machine-reproved every inherited lemma. The present report is directed at the active headline theorem chain and the places where v23 claims to close the v22 top-four blockers.

## 3. What v23 genuinely fixes

### 3.1 The common-laboratory registration defect of v22 is substantially fixed

This is the strongest new part of v23.

The intrinsic datum for a measured edge `e=(a,b,ell)` now consists of the lifted channel label, physical onset, two signed endpoint-law germs and transverse sign convention in the **edge's own channel-adapted frame**. The relative Euclidean placement of that frame with respect to another channel or to the lattice is not supplied.

The all-order inverse plus the new analytic continuation lemma recovers complete oriented analytic curve images `C_{e,-}` and `C_{e,+}` in each edge frame. The remaining problem is formulated as a periodic Euclidean gluing problem with unknown `A_e in SE(2)` and unknown oriented realization `iota` of the marked Euclidean lattice.

The gluing relation

`tau_{-iota(nu(e,sigma))} A_e C_{e,sigma}
 = tau_{-iota(nu(f,sigma'))} A_f C_{f,sigma'}`

is the correct periodic compatibility relation between two incidences of the same quotient obstacle. The quotient by a single simultaneous `SE(2)` action is also the correct global gauge.

The cycle-holonomy identity is a real new mechanism. For a signature-rigid cycle the data determine a Euclidean holonomy `H_c`; realizability forces its rotational part to be trivial and gives

`R_{e0} v_c = iota(eta_c)`.

Once the Euclidean Gram form on the abstract lattice is fixed, a nonzero `eta_c` indeed determines the orientation-preserving lattice realization relative to the starting edge frame. A rooted signature-rigid tree can then propagate the remaining obstacle placements. I do not find the old v22 disconnected-registration objection in this construction.

### 3.2 The analytic germ-to-global lemma is plausible and appropriately isolated

The new analytic continuation lemma uses equality of an oriented analytic boundary germ to identify the full lifted curvature functions. Since the curvature is positive and each strictly convex closed curve has total turning `2 pi`, two possible arclength periods for the same positive analytic curvature function must coincide. Uniqueness of the planar Frenet system then identifies the entire boundary image.

This is not the difficult part of the paper, but it is the right lemma to state explicitly. I see no immediate defect in this argument.

### 3.3 The richer physical observation hierarchy is now mathematically meaningful

V23 no longer tries to call the endpoint-only Gaussian theorem the complete physical experiment. It distinguishes:

1. the stopped endpoint--time transcript, including residual time and failures;
2. the count--endpoint coarsening, retaining waiting counts but discarding residual time;
3. the endpoint-output coarsening, discarding both residual time and waiting counts.

The three different singularity structures naturally lead to three different local limits. This is a significant conceptual improvement over earlier versions.

### 3.4 The endpoint--time Poisson scaling is internally plausible

For a successful record the null density is

`rho(u,v) 1_{0<r<w(u,v)}`,

so the density has positive trace at the moving ceiling. At a `1/k` displacement of the ceiling the relevant null slack `y=k(w-r)` lies in an `O(1)` strip. The corner where the moving ceiling meets `r=0` has endpoint area `O(1/k)` and residual length `O(1/k)`, hence one-record mass `O(1/k^2)` and total mass `o(1)` over `O(k)` records. This is the right codimension-two estimate.

On the remaining layer, the binomial-to-Poisson scaling with intensity

`alpha_l rho_l(u,v) 1_{y>U_l(u,v)z}`

is also the natural limit. The non-domination statement is correct in spirit: a local expansion of the ceiling creates a region with positive alternative intensity and zero reference intensity.

### 3.5 The two-speed count--endpoint algebra is coherent

Let `lambda=D_theta gamma`, choose `v_gamma` with `lambda(v_gamma)=1`, and set `H_gamma=ker lambda`. At

`k delta^2 log(1/delta) -> 1`,

using

`theta = b/(j sqrt(k)) v_gamma + delta h`, `h in H_gamma`,

and `g-g0 = delta a/j`, the leading exponent perturbation of the success probability is `-b/sqrt(k)`. The slow gap contribution is `O(delta)` after multiplication by `j`, and the quadratic iso-hyperbolic contribution is `O(j delta^2)`. After multiplication by `sqrt(k)`, both are negligible under the stated conditions.

Conversely, a moving endpoint displaced by `eta=1/(j sqrt(k))` contributes total squared Hellinger order

`k eta^2 log(1/eta) = log(j sqrt(k))/j^2`,

which vanishes under the theorem's condition. The exact stopped Bernoulli-mark factorization then makes the count and endpoint central sequences independent. I did not find a scale contradiction here.

The explicit common regime

`delta_n=n^{-1}, k_n=floor(n^2/log n), j_n=2 ceil(C log n)`

with `C>|log tau|^{-1}` satisfies the displayed endpoint, count and transfer assumptions. Thus the multi-rate theorem is not vacuous because of incompatible asymptotic requirements.

## 4. Major blocker C23-M1: the endpoint--time theorem has not yet proved the claimed two-sided Le Cam equivalence

Theorem `thm:v23-et-poisson` is one of the most interesting additions in v23, so the standard of proof must be correspondingly high.

The proof convincingly addresses the **forward rare-layer approximation**. On a fixed `|y|<=R_K` strip, the one-record retained-layer probability is `O(1/k)`, the conditional location law converges, and standard binomial--Poisson coupling gives the correct Poisson random measure. The corner near `r=0` is negligible.

The proof then removes a reference ceiling layer and writes the bulk density ratio as

`1 + k^{-1} a_z(u,v,r) + o_K(k^{-1})`.

It observes that the centered one-record log likelihood has variance `O(k^{-2})`, hence the centered sum over `O(k)` records has variance `O(k^{-1})`. The deterministic first-order normalizing term is identified with the negative of the ceiling-layer mass, i.e. the Poisson compensator.

Up to this point I agree with the heuristic and I expect the result to be true. The proof then says, in effect:

> extract the boundary process; conversely generate the asymptotically parameter-free bulk from the reference conditional law and attach it to the Poissonized boundary layer.

That sentence does not yet prove the reverse deficiency.

### 4.1 What is missing

A full Le Cam equivalence statement needs a **parameter-independent Markov kernel** from the limiting Poisson observation (plus a parameter-free factor) back to the original fixed-size sample whose total variation error is uniformly `o(1)` for `z` in compact sets.

For that one needs, at minimum, a lemma of the following sort.

After conditioning on the retained boundary configuration (or at least on its count), let `B_{n,z}^{bulk}` be the conditional law of the remaining labeled bulk observations. Prove

`sup_{z in K} || B_{n,z}^{bulk} - B_{n,0}^{bulk} ||_TV -> 0`

uniformly over boundary configurations in a set of probability `1-o(1)`, or prove an integrated version strong enough to construct the reverse kernel. This requires keeping track of:

- the random bulk sample size `k-N_layer`;
- the parameter dependence of the conditional bulk normalizing constant;
- the dependence between the boundary count and the bulk count created by the fixed total sample size;
- the replacement of the binomial boundary count by a Poisson count;
- negligible exceptional events such as a Poisson count larger than the fixed sample size;
- uniformity in `z` on compact sets;
- the fact that the original local family is non-dominated across parameters at the ceiling.

The variance calculation for the centered bulk log likelihood strongly suggests that such a lemma is available, but it is not itself the lemma. Convergence of a likelihood ratio in probability under a reference law is not automatically the same thing as a uniform parameter-independent simulation statement required by reverse deficiency.

### 4.2 A clean repair is available

I do not regard this as evidence that the Poisson theorem is false. A repair should be possible by proving a one-record Hellinger or `chi^2` estimate for the **conditional common-support bulk law**, then tensorizing over the random remaining sample size, and combining it with an explicit binomial--Poisson coupling. One can then write the reverse kernel: sample the coupled boundary count/locations, fill the remaining labeled slots from the reference bulk conditional law, randomize slot positions according to the parameter-free combinatorial law, and add the parameter-free failure/order information.

But this argument must appear. At the requested venue level, a principal theorem advertised as a non-dominated Poisson boundary experiment cannot rest on the phrase `generate the asymptotically parameter-free bulk` without the uniform conditional estimate that makes the kernel legal.

### 4.3 The same point propagates to the complete stopped theorem

Theorem `thm:v23-complete-et` inherits the Poisson equivalence. Its waiting-count ancillarity estimate is plausible, and the finite-to-boundary transfer may then be composed with the limit. But until the two-sided equivalence of `thm:v23-et-poisson` is fully established, the claim that the **entire** stopped endpoint--time transcript has the stated Le Cam limit remains underproved.

This is my principal correctness-level objection to v23.

## 5. Major blocker C23-M2: the global statistical recovery theorem is conditional on a premise not proved by the physical theory

V23 was explicitly designed to answer the v22 criticism that the exact all-order analytic theorem and the fixed finite-jet statistical theorem were disconnected. The new section `25_analytic_global_bridge_v23.tex` is a useful abstract bridge, but it does not yet close that gap for the actual physical experiment.

### 5.1 The compactness theorem is correct but qualitative

Let `K` be a compact analytic class with singleton admissible periodic gluing. If the complete data map `D_infty` is injective and every fixed finite coordinate `D_M` varies continuously, then compactness indeed implies finite-coordinate resolution:

for every `q` and `epsilon` there exist `M` and `eta` such that

`||D_M(T)-D_M(T')||<eta => d_q(T,T')<epsilon`.

The contradiction proof is standard and sound. Likewise, **if** every fixed `D_M` has a uniformly consistent estimator, a diagonal choice `M_n -> infinity` can yield one globally consistent table estimator for every fixed `C^q` loss. No uniform-in-`M` condition number is needed for this purely qualitative diagonal argument.

I therefore have no objection to the abstract compactness theorem itself.

### 5.2 The missing premise is exactly the hard statistical interface

The diagonal theorem assumes, rather than proves, that for each fixed `M`

`sup_{T in K} P_T{ ||Dhat_{n,M}-D_M(T)|| > epsilon } -> 0`.

Nothing in the preceding local asymptotic theory establishes this statement on the compact analytic class.

The finite positive-design lemma is **local**: the design may depend on `M` and on the reference geometry. The LAN/Poisson statements are local experiments around an anchored reference table. Local injectivity and local asymptotic information do not by themselves produce a single estimator uniformly consistent over a compact nonlinear class, much less a common acquisition design or a finite adaptive atlas that works uniformly over `K`.

The new corollary therefore says, accurately, `whenever K admits a common finite acquisition atlas for which every fixed action-jet vector is uniformly consistently estimable...`. That qualifier is mathematically honest, but it means the paper still lacks the end-to-end theorem that the surrounding narrative suggests is now present.

### 5.3 There is also an analytic/smooth realization mismatch

The interface is sharper than a generic `local versus global` concern.

`18b0_anchored_realization_v22.tex` realizes arbitrary finite labeled contact jets by multiplying polynomial jet perturbations with compactly supported smooth cutoffs. The section explicitly notes that this serves the finite-dimensional statistical local experiment and that the analytic continuation conclusions are **separate deterministic statements**; no compactly supported analytic bump is used.

By contrast, the global bridge works on a compact class of real-analytic periodic tables.

Thus the current physical local model is not itself a proved local chart of the compact analytic class used by the global reconstruction theorem. One cannot simply cite the smooth finite-jet realization to discharge the fixed-`M` uniform consistency assumption on `K`.

This does not mean an analytic statistical theory is impossible. It means it has not been supplied.

### 5.4 What a genuine closure would require

At least one of the following routes is needed.

**Route A: global fixed-order estimation on the analytic class.** For each fixed `M`, construct from the actual finite-bridge records a common finite (possibly adaptive) acquisition scheme over `K`, prove uniform separation/identifiability of the finite action-jet vector, and build `Dhat_{n,M}` with the required uniform consistency. Compactness may help extract a finite atlas from local designs, but the atlas construction and transition logic must be proved.

**Route B: analytic local charts.** Replace the smooth cutoff realization by finite-dimensional real-analytic perturbation families that preserve the periodic dispersing geometry and span the needed contact-jet directions, then prove uniform control over a finite cover of `K`. This would connect the local experiment more directly to the analytic class.

**Route C: weaken the claimed statistical consequence.** Keep the compactness theorem explicitly as an abstract conditional proposition and stop presenting it as closure of the physical-to-global statistical chain. This would improve correctness of positioning but would lower the venue-level scope.

For the requested top-four target, Route A (or something comparably strong) is the convincing response.

## 6. Major blocker C23-M3: `fully intrinsic periodic table rigidity` still fixes the Euclidean lattice metric externally

The v23 global theorem is substantially more intrinsic than v22, but the current terminology overstates what is reconstructed.

At the start of `23b_intrinsic_multichannel_rigidity_v23.tex` the paper fixes

`Lambda_abs ~= Z^2`

**with its fixed Euclidean Gram form and the orientation induced by its marked basis**. The unknown `iota` is then only an orientation-preserving linear isometry from this already metrized abstract lattice to `R^2`.

Consequently, once a lattice-anchoring cycle supplies one nonzero relation

`R_{e0} v_c = iota(eta_c)`,

the unknown is just the orientation of a lattice whose lengths and angle are already known. In two dimensions one nonzero vector indeed fixes an orientation-preserving isometry between two oriented Euclidean planes. The proof is correct under this hypothesis.

But the hypothesis matters.

### 6.1 The theorem does not recover the lattice modulus/scale

If by `periodic table` one means the obstacle configuration together with the ambient periodic lattice, then the Euclidean geometry of that lattice is part of the object. V23 does not infer that geometry from the signed endpoint laws. It assumes the Gram matrix of the marked lattice is the same in the compared tables.

Thus the strongest accurate formulation is closer to:

> intrinsic recovery of the labelled obstacle configuration and channel-to-lattice registration **relative to a fixed marked Euclidean lattice metric**.

That is a meaningful theorem. It is not the same as complete intrinsic recovery of the periodic billiard geometry from channel laws alone.

The distinction is especially important when the paper is compared, at a four-journal significance level, with global rigidity results based on marked or enriched length data. I am not asserting that those data are weaker in every sense; the observation architectures differ radically. I am saying that a headline global inverse theorem should state plainly which ambient metric data are given and which are recovered.

### 6.2 The general gluing-space theorem is more a classification formalism than a rigidity theorem

The theorem identifying table realizations with `G_per(D)` is useful organization, but by definition an `admissible` gluing is already required to produce a genuine periodic dispersing table with disjoint translated closures and the prescribed measured closest-pair channels. Once the complete edge-frame curve images are known, the statement

`realizations modulo SE(2) <-> admissible gluings modulo SE(2)`

is close to a restatement of the remaining global placement problem.

The real mathematical global rigidity result is the subsequent singleton criterion: an anchoring cycle plus a rooted signature-rigid spanning tree forces at most one gluing. That result is nontrivial and should be presented as such.

At the requested venue level I would want one more structural theorem around this criterion, for example:

- a genericity/open-denseness theorem showing that the signature-rigid anchoring/tree hypotheses hold for a natural large class;
- a theorem showing how multiple cycles resolve finite symmetry ambiguities beyond the signature-rigid case;
- a quantitative/stable version of the gluing reconstruction;
- or recovery of the lattice Gram form itself from the intrinsic observations.

Without such a strengthening, I regard the global theorem as a serious mechanism but not yet an obviously Annals/Acta/Inventiones/JAMS-level global rigidity theorem.

### 6.3 The claim should at least be calibrated everywhere

If the author does not attempt to recover the lattice metric, the title, abstract, introduction and corollary should consistently say `relative to a fixed marked Euclidean lattice` rather than using `fully intrinsic` without the qualifier. The present source does disclose the Gram-form assumption in the technical section, so this is not a hidden logical contradiction; it is a mismatch between headline scope and theorem input.

## 7. Additional technical points

### 7.1 State the flight-number divergence explicitly wherever it is used

The count-score lemma uses a fast coordinate `eta_n=1/(j_n sqrt(k_n))` and treats smooth prefactor contributions `O(eta_n)` as `o(k_n^{-1/2})`. This uses `j_n -> infinity`. The surrounding physical setup and the final joint theorem effectively force or assume this, but the local lemma should state all asymptotic conditions it uses rather than relying on remote context.

This is minor and easily fixed.

### 7.2 Make the parameter-free failure-order factor explicit

The stopped iid Bernoulli-mark factorization is correctly written in terms of the negative-binomial waiting count and the iid successful marks. The full transcript also retains the exact success/failure order. Conditional on the terminal count, that combinatorial order is parameter-free. Since the manuscript repeatedly emphasizes exact sigma-fields, it should state this factor explicitly when passing from `(T, successful marks)` to the whole retained failure sequence.

Again, I do not think the result is wrong; the exact factor should simply be written down.

### 7.3 Clarify the `connected measured graph` convention

The intrinsic reconstruction theorem defines quotient curves `C_1,...,C_N` from incidences. This presupposes that every obstacle orbit to be reconstructed is incident to the measured network. If `connected measured lifted-channel graph` is defined to have all `N` obstacle labels as its vertex set, this is automatic (apart from degenerate one-vertex/no-edge conventions). The source should say so explicitly. The signature-rigid spanning-tree corollary is clearer on this point than the general classification theorem.

### 7.4 Distinguish `fastest for this declared sigma-field` from globally optimal physical rate

The manuscript is much more careful than v22 and explicitly excludes the full growing collision array. Keep that discipline. Phrases such as `fastest geometric scale` should always be read as fastest for the declared endpoint--time transcript, not as an efficiency lower bound among all physically measurable collision histories. The present text mostly does this; it should be made completely uniform.

### 7.5 The compactness bridge is nonconstructive

The finite-coordinate resolution theorem and diagonal `M_n` theorem are existence statements. They provide neither an effective required jet order `M(q,epsilon)` nor a usable growth rate for `M_n`, and no sharp global minimax rate is claimed. The manuscript says this, which is good. The abstract and introduction should continue to avoid language suggesting a quantitative analytic continuation/stability theorem.

### 7.6 Build verification is still pending

`A2_REVISION_V23_VERIFICATION.md` records the canonical source commit `8840bf01ee8a7752504d2913bf00af54656afbb5` and workflow run `34602335326`. The run and explicit rerun both report a failed `native-build` job with `steps=null`, before checkout or any other runner step.

Therefore:

- this is **not** evidence of a TeX error;
- it is **not** evidence that the numerical diagnostic fails;
- it is also **not** a successful build certificate.

A submission-ready branch should eventually carry an executing native build, unresolved-reference check and reproducible PDF hash.

## 8. Venue-level significance assessment

The most original-looking piece remains the all-order signed contact inverse, especially the determinant-one new block at every jet order combined with the relative boundary law. V23 now adds a credible global placement mechanism instead of simply registering all channel frames externally. This is a substantial improvement.

However, a top-four referee must evaluate the theorem package as a whole rather than count the number of technically sophisticated modules.

The current package has four layers:

1. a strong relative boundary asymptotic;
2. a local all-order inverse for contact geometry;
3. an intrinsic-but-fixed-lattice gluing/holonomy theorem under explicit rigidity hypotheses;
4. several local statistical experiments, plus a conditional compactness bridge to global consistency.

The mathematical ambition is high, but the last two layers are not yet fused into a single unconditional global information theorem. In particular, the paper does **not** currently prove:

- recovery of the Euclidean lattice metric from the observations;
- a global uniformly consistent fixed-order estimator on the compact analytic class;
- an unconditional global table estimator from the actual finite-bridge record;
- a sharp global minimax rate;
- or the local limit of the complete growing collision array.

The manuscript is honest about several of these limitations. Honesty is a virtue, but it does not by itself raise the result to the requested venue threshold.

For comparison, the recent billiard rigidity literature has moved toward genuinely global geometry recovery from globally organized dynamical data (marked or enriched spectra) under its own hypotheses. The present endpoint-law data are different and in some senses much richer locally. To justify a top-four claim on that different architecture, the paper should exploit that richness to obtain a correspondingly decisive global theorem rather than stop at a conditional gluing and consistency framework.

## 9. Required changes before I would recommend a fresh top-four assessment

I would require the following, in priority order.

### R23-1. Complete the Poisson Le Cam proof

Add a precise bulk-ancillarity lemma with a uniform total-variation/Hellinger estimate conditional on the boundary layer, construct the reverse parameter-independent kernel explicitly, and prove the two deficiencies vanish uniformly on compact local parameter sets. Then propagate the strengthened statement to the complete stopped transcript.

### R23-2. Prove the fixed-order uniform estimation premise on the analytic class

Do not leave `every fixed D_M is uniformly consistently estimable` as an assumption if the paper is to claim an actual physical-to-global statistical theorem. Construct a common finite/adaptive acquisition atlas on `K`, prove uniform fixed-order identifiability and consistency from the actual finite-bridge records, and then invoke the diagonal theorem.

This step should also resolve the present analytic/smooth realization mismatch.

### R23-3. Strengthen or recalibrate the intrinsic global theorem

Preferably recover the marked lattice Gram form (or otherwise show it is identifiable from the same observations). If that is outside the intended inverse problem, then explicitly formulate every headline theorem relative to a fixed marked Euclidean lattice metric.

In addition, strengthen the singleton mechanism beyond a hand-selected signature-rigid tree if possible: prove genericity, stability, or a multi-cycle symmetry-resolution theorem.

### R23-4. Preserve the v22/v23 improvements

Do not regress on:

- the all-order action-jet filtration;
- determinant-one signed inversion;
- even-flight parity convention;
- parameter-independent physical observation maps;
- reference-based caps;
- non-dominated versus dominated-representative distinction;
- exact observation-sigma-field hierarchy;
- stopped finite-to-boundary transfer at the record level actually proved;
- the intrinsic edge-frame gluing formulation;
- explicit obstacle-symmetry handling;
- the multirate count/endpoints distinction.

### R23-5. Obtain a real exact-head build certificate

Run the native workflow on an executing runner, archive the exact source, compile the paper, run the numerical diagnostic under the declared modes, reject unresolved references/citations, and record the PDF/source hashes.

## 10. Final recommendation

**Top-four decision: reject in the present form.**

I would not advise abandoning the project or deleting the new v23 modules. The correct next move is the opposite: finish the hard interfaces that v23 has now exposed clearly.

The registration problem of v22 is no longer the main obstacle. The next revision should concentrate on:

`rigorous two-sided Poisson experiment equivalence`

`+ unconditional fixed-order physical estimation on the analytic class`

`+ a stronger or more accurately scoped intrinsic global theorem`.

If those three points are resolved, the paper would be qualitatively different from v23 and would deserve a fresh high-level review rather than another cosmetic round.