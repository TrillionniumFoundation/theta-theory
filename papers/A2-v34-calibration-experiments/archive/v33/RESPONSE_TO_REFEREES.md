# Response to the v32 referee report

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Controlling review:** `058d2b7b773038cfa7e43f7f52a3b79fdc4107f6`  
**Report blob:** `e38199da9ea49227f48b94eef8d04b3ee8da871c`  
**Reviewed author source:** `eeb171d4e00242c9813c10e2124556b2cee480d3`  
**Revision:** A2 v33, 4 October 2026

We thank the referee for distinguishing the audited mathematical results and completed source qualification from the conceptual and resource-accounting objections. The revision retains the scalar collision problem, all six active v32 proof chapters and the complete reviewed source tree. It adds proofs addressing the two resources that were previously separated only by qualifications: finite control descriptions and physical calibration resolution. It also proves a genuinely sequential observation lower bound rather than extending the deterministic-cap wording without an argument.

## 8.1. Lower-bound gauge and centering

Section 7.1 defines the parameter-independent disclosed data: the fixed laboratory axes, lattice, species correspondence and fixed second obstacle. It explicitly excludes disclosure of the unknown variable obstacle's Steiner point. Equation (7.2) defines the centered-support accuracy sets, without independent rotations. Lemma 7.1 bounds the first harmonic removed by Steiner centering by `O(h^s)`, uniformly in the number of disjoint bumps. The raw second-derivative separation is `c h^(s-2)`, so at least half survives for small `h`. This proves the lower bound for a weaker centered-shape loss and hence for the stronger laboratory reconstruction loss. The fixed pose is not parameter-dependent shape side information.

## 8.2. Deterministic caps and expected stopping

The original deterministic-cap theorem and its scope paragraph remain unchanged and active. The abstract now names both criteria only because Section 7 supplies a separate proof for random stopping. For a parameter-independent seed, terminal bit words are prefix-free. Their entropy is at most their expected length; the displayed conditional-entropy decoding argument gives

`average E[T] >= (1-delta) log_2 M - h_2(delta)`.

The centered physical packing yields Theorem 7.3, with worst-case expected attempts at least `c nu^(-1/(s-2))`. The stop decision is based only on observed bits and independent controller randomness; no analog waiting-time or success flag is admitted. Arbitrary input precision is allowed in the lower bound. Confidence and logarithmic factors are not claimed sharp.

## 8.3. All resource axes

Theorem 4.1 replaces exact real-valued nominal coordinates by finite dyadic commands. A target is rounded once and its whole compass dependency stencil is then formed exactly on one dyadic grid; reciprocal reverse starts preserve the prescribed nominal joint law. The robust bisection proof gives a geometric width recurrence with a bounded mesh floor, not an accumulated error proportional to the number of iterations. Radial interpolation absorbs the reserved errors, and exact rational period decisions persist below the known gaps.

Batch descriptions use `O(log(1/nu)+log(1/delta))` bits each, with an explicit total and finite output-description bound. For rational numerical priors and rational smoothness, the theorem gives a conservative bit-operation upper bound with a disclosed `nu^(-1/2)` quadrature term; it is not relabelled as the attempted-bit rate. Section 4.1 lists output bits, centers/batches, digital controls, localization, physical calibration, aperture, numerical work and apparatus movement/setup/calibration production together. The last category has no invented physical cost law. A finite kernel command does not by itself construct a cheap apparatus.

## 8.4. Exact scalar sensor contract

The original Sections 1.2 and 2 remain byte-identical. A solid start and a free miss both return zero and are charged. The controller receives no free-start test, impact coordinate, angle or collision time. The forward compass law and translated reciprocal reverse joint law, the localized launch distribution, fresh preparations and pooled means remain the observation contract. The new digital construction changes only how its nominal parameters are described, not its geometric output alphabet.

The new calibration converse is proved in this physical contract. Lemma 8.1 constructs measurable perturbations of actual start positions for two nearby convex arrays. Where nominal bits differ, the hit-side start can be moved either into its solid or outside its swept body, within the allowed spatial error. Thus both worlds produce the same physical bit. No adversarial bit replacement is assumed.

## 8.5. Periodicity and the known margin

The bounded periodic presentation and known positive nonperiod-patch margin remain in the abstract, overview and resource statements. The unchanged Section 5 proves the conditional discrete recovery and distinguishes exact rational relations from estimated Euclidean vectors. No claim is made to infer periodicity from an arbitrary configuration or to learn an unknown uniform stopping margin from finite bits. The new lower-bound family already has a fixed known primitive lattice, two fixed species and a uniform positive patch margin, so its resource lower bounds do not arise from period uncertainty.

## Conceptual resource objection: a necessary calibration power

Section 8 supplies more than a cost disclaimer. For matched bodies at Hausdorff distance `e`, with flight lengths below separation, convex swept-set geometry gives physical start perturbations of size at most `2e` yielding an identical response for every nominal start and direction. The construction is pointwise, so it survives arbitrary adaptive nominal choices and every bit-measurable stopping rule. A fixed physical support bump has Hausdorff size `h^s` and centered `C^2` size `h^(s-2)`. Theorem 8.2 therefore shows that uniform accuracy `nu` under worst-case bounded position errors requires `r <= C nu^(s/(s-2))`, matching the sufficient power in the retained reconstruction. Additional attempts cannot substitute for this resolution.

This converse uses the original worst-case bounded coupling, which may depend on the table and nominal command. It does not assert the same obstruction for a single common offset, known mean-zero errors, or arbitrarily long flights. Position alone is necessary; time and angle may remain exact. The positive reconstruction theorem is retained at the matching sufficient combined tolerance. The new statement characterizes two distinct resources of the same active collision inverse, without changing the topic to a passive invariant or presenting an editorial recommendation as a mathematical conclusion.

## Sources, verification and preservation

The exact reviewed v32 tree is Supplement R32. Its fifteen-document success is baseline evidence only. The v33 full validator has its own source pins, manifest and schema, checks its triggering SHA, and requires the unchanged v32 validator to qualify the retained package at that same SHA before declaring a sixteen-document pass. The actual local source-content run passed the new and retained finite suites and built the 21-page primary without final TeX diagnostics. Local source-content execution is not called a new authenticated checkout or a hosted full-package pass. Actual hosted status remains in the current workflow receipt, not inferred from the workflow definition.

The literature comparison with active boundary estimation remains active and unchanged. Classical coding and entropy are credited, with the sequential argument written in full. No priority or top-four significance claim is inferred from finite diagnostics. The mathematical additions and the unchanged original results are presented for independent review at the requested standard.
