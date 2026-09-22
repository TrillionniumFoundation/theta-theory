# Response to the second v7 structural referee report

**Manuscript:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction.  
**Author:** Qian Qi. **Revision:** eighth decision-spectrum revision, 23 September 2026.  
**Controlling review:** `ba97a2e4ac71a89a966a501837ff78237e85eb10`, report blob `2803882fb52d77d41c81cd9116d4aff715dc56e8`.  
**Report:** `reviews/general-theta-foundations-i-v7-structural-harsh-referee-r2-2026-09-22/REFEREE_REPORT.md`.

We thank the referee for identifying the remaining structural questions separately from the validity of the preceding local calculations. The eighth revision is built around a common marked decision spectrum, its likelihood-saturated representation, and a necessary-and-sufficient recursive partition description. The quantitative consequences concern certified tree compilation, full posterior presentation, sequential Gaussian accumulation, and finite-command cell instruments. Every mathematical body from the preceding canonical article remains in the new canonical article; every preceding development body remains in the complete-development companion. No earlier source file is altered.

Stable theorem labels below refer to the native TeX. The build receipt supplies their actual numbers and pages. Classical randomization, sufficiency, automaton congruences and kernel composition are expressly attributed. The response does not ask that their reformulation, or any numerical diagnostic, be counted as independent novelty.

## I. One mathematical identity rather than four parallel vocabularies

The central object is now `boldsymbol Theta(E)`: the attainable risk vectors of one causal encoder, together with its declared tasks, ideal baselines and full resource signature. The common encoder is chosen before the task; decoders may depend on the task, not on an unknown true parameter. Both fixed-prior risks and fixed-class minimax risks are admitted, with the risk functional specified. Theorem `thm:v8-main` states the representation/realization chain and points to its complete proofs.

Theorem `thm:v8-spectrum` proves transport of entire attainable risk sets and invariance under typed causal equivalence. Theorem `thm:v8-duality` identifies the all-terminal-decision slice as the optimal reverse deficiency of a common finite encoding. Theorem `thm:v8-congruence` identifies a quadratic finite-history slice exactly as minimization over successor-compatible partitions. These are not assertions that every experiment has a tree geometry: the common object is the marked profile, and tree, measure-valued and Gaussian results compute different specified slices.

Two distinctions are necessary. The realized-law Wasserstein task is a single minimax task over unknown input laws, not a supremum of point-prior Bayes tasks, which would reveal the input to the decoder. Marginal-probe simulation is a different output-law criterion. The proposition comparing them exhibits different rates instead of conflating them in a universal scalar dimension.

## II. A characterization and a causal obstruction

Theorem `thm:v8-congruence` removes all tree assumptions. For any finite report alphabets, finite horizon and fixed Bayesian quadratic criterion, the optimum over arbitrary randomized, time-dependent S-state machines is exactly the minimum of the explicit conditional-variance functional over width-S successor-compatible history partitions. Both directions are proved, including deterministic realization of each compatible partition family and the valid fixed-Bayes use of independent-tape freezing.

Thus a same-order comparison with static checkpoint quantization holds if and only if compatible partitions with the corresponding variance bound exist. Exact suffix closure is one construction, not an intrinsic necessary coordinate choice. The continuation corollary records the classical right-congruence obstruction for stationary exact machines and a quantitative residual-diameter obstruction for uniformly accurate machines. Its stationary subclass is not confused with the preceding time-dependent theorem.

Example `ex:v8-index` gives a temporal obstruction with explicit input cost: a d-bit word followed by a coordinate query has a two-valued checkpoint target, but exact causal prediction needs 2^d states. Its nonzero error satisfies the binary entropy lower bound. This is a genuine separation from static geometry, not a failure of a particular tree algorithm.

## III. Full resource signatures and effective compilation

Every current result has a stated signature; the detailed table is `RESOURCE_SIGNATURES.md`. Persistent states S, physical terminal labels A, raw symbol queries L, program bits P, numerical precision p, transient workspace W, update time and independent randomness are distinct. Mathematical existence is not silently converted into an algorithmic complexity claim.

Theorem `thm:v8-certified` strengthens the existing tree theorem. An oracle need only provide certified rational upper energies within a fixed factor. Taking the minimum over all contiguous factors repairs prefix/suffix monotonicity, even when numerical approximations reverse nearly tied energies. Threshold cuts then have exact suffix closure, balanced energies and matching static distortion order. An explicit disjoint-tube argument supplies the lower bound for arbitrary Hilbert centres.

For a fixed finite alphabet and finite-dimensional bounded readout, the selected S-state tree has O(log S) acquisition depth, O(log S) readout precision and O(S log S + S d p) description bits. The proof specifies finite online workspace and table lookup/bit-scan costs. Oracle evaluation and representative construction require effective access and have no uniform offline-time bound under the stated hypotheses. Infinite-dimensional readouts are not claimed to have finite-bit descriptions from their Hilbert-space existence alone.

## IV. Bayesian predictive quotients and parameter-uniform experiments

Theorem `thm:v8-sufficient` constructs a saturated posterior coordinate using a strictly positive dense reference prior in a compact total-variation-continuous experiment. One disintegration kernel reconstructs every parameter law. Minimality is proved by likelihood factorization; changing the positive dense prior changes coordinates but not the completed minimal sufficient sigma-field. Terminal finite-output risk sets are equal at every budget because the reconstruction can be composed before the finite encoder.

This result concerns terminal parameter-decision losses. An additional latent-target loss needs its joint conditional law retained; equality of observation laws alone is insufficient. A constant future-test family on a perfectly observed binary parameter gives an explicit unsaturated counterexample.

Theorem `thm:v8-causal-sufficiency` states the additional conditions required online: recursive coordinates, predictive closure under the reference mixture, and likelihood saturation for every parameter and admissible policy. Conditional disintegration followed by a likelihood-ratio calculation produces a parameter-independent sequential reconstruction. A K0-valued quotient costs K0 extra simulator states, hence a K0 S observer bound. Infinite quotient storage is charged, not called free finite memory. This directly separates terminal sufficiency from causal, resource-controlled sufficiency.

## V. A defined category and a consequential invariant

The objects are marked causal instruments. An arrow includes initialized kernels, the global parameter/policy quantifiers, an error certificate and a monotone resource transformer. Equality is execution equality under every admissible continuation, with the same certificate. Theorem `thm:v8-spectrum` proves associative kernel composition on these classes, identities, composition of transformers and additive variation errors. Its main consequence is transport of the common-encoder attainable sets; exact equivalence gives cardinality-profile comparability and equality of existing positive exponents.

Proposition `prop:v8-forgetful` supplies the precise forgetful functor for uncontrolled finite-horizon instruments: pass to the transcript statistical experiment and its induced Markov kernel. This forgets both causality and cost information. It does not assert that an arbitrary inverse terminal kernel is a finite-state causal inverse. Controlled simulations retain the policy-lifting interface rather than pretending that a controller can be removed by a terminal map.

## VI. Finite-prefix acquisition

The certified tree theorem reads a finite prefix of a frozen acquisition snapshot and stops at a leaf. The maximum number of symbols is the proved tree depth; no later access to the original word is permitted. Between acquisitions, deletion uses only a charged vertex index. The update deadline explicitly permits those finite microsteps. The theorem does not substitute a frozen snapshot for an evolving physical state without specifying the observation latency.

The complete predecessor theorem remains available with its original full-word interface. Its finite-prefix implementation is now a separately proved consequence, with its additional effective-access assumptions and costs stated.

## VII. A matching measure-valued result and a stronger coordinate obstruction

Theorem `thm:v8-measureentropy` proves the sharp order 1/log(S+1) for uniform presentation of an arbitrary law on [0,1] in expected realized W1 distance, allowing randomized encoders and decoders. The upper bound uses the explicit empirical-law net; the lower bound is a Hamming packing with exact W1 distance and a uniform finite-prior centre-counting argument. Randomization is handled before converting average packing risk to worst-input risk.

For the actual nonlinear instrument already present in v7, Corollary `cor:v8-nonlinear` proves a matching lower Lipschitz bound as well as contraction. The resulting all-priors posterior class at each fixed time retains the same entropy order. Its lower constant contains 5^(-t); no long-time bound for one fixed preparation is inferred. A Borsuk–Ulam argument rules out any fixed finite-dimensional continuous exact coordinate on this class, rather than only finite polynomial moments. Arbitrary discontinuous Borel coding is expressly distinguished.

The single-probe proposition explains why this lower bound cannot be transferred to a weaker marginal simulation objective: a common randomized S-label encoder simulates a single Lipschitz Bernoulli probe with error O(1/S). The type of the desired output is therefore a mathematical part of the invariant.

## VIII. A causal Gaussian consequence

Theorem `thm:v8-seqgaussian` studies n sequential independent r-dimensional Gaussian innovations. The current register, not a free transcript of earlier outputs, must contain the entire retained experiment. The decision-complete terminal spectrum is of order S^(-2/(nr)).

The lower bound applies to every randomized time-dependent causal encoder because its final experiment has at most S outcomes; fixed-encoder decision completeness identifies the resulting deficiency with the same marked spectrum. The upper construction appends coordinate cell labels in one register, with at most J^(rt) states at time t and J^(rn)<=S in total. The complete positive Gaussian reconstruction proof is included. Constants are for a fixed horizon; no growing-horizon uniformity or uncharged public side information is implicit.

## IX. Theorem-level pipeline arrows

`HISTORY_AUDIT.md` now contains a row for each of A1, A2, A3, A4, B1, B2, B3, B4, C1, C2 and D1: the exact GTF result, the hypotheses needed or verified, the transported quantity and the remaining model-specific work. Historical native theorem headings and report identities are separately recorded.

There are two direct statistical protocol arrows. Corollary `cor:v8-a1` proves the exact compatible-partition formula for the finite-command specialization of the actual A1 cell instrument, deriving the history probabilities and posterior query means from the accepted/failure likelihoods. This uses the single shared failure report; no encoder is allowed to recover the unobserved raw cell. The result is a scalarized checkpoint criterion, not an unsupported replacement of A1's maximum-risk criterion or its collision geometry.

For modern A2, the complete count-to-contact theorem is retained and placed in the decision-spectrum comparison chain. The source is the fixed known-mark exposure protocol, the target is its specified Gaussian family, and the output statistic is deterministic and unjittered. The historical Sinai paper named A2 is a different model and a different row. No theorem about the latter, or about path LDPs, kinetic limits, common unbounded-operator domains or phase semigroups, is inferred from a local statistical comparison.

## X. The nearest-theorem comparison

The new audit covers minimal predictive states, automaton congruences, zero-delay coding, Gibbs/functional quantization, Wasserstein entropy, nonlinear filter approximation, static randomization/deficiency and filtered experiment comparison. The introduction explicitly states which underlying principles are classical. `LITERATURE_AUDIT.md` identifies the actual primary texts or publication records checked, their versions, the closest theorem or topic, and the different resource or task quantifier.

Where a publisher supplied only a record or a PDF fetch failed, the audit says so. A self-contained proof is provided for the criterion used here; a bibliographic citation is not represented as having completed a full-text priority audit. No exhaustive novelty certification is claimed.

## Technical concerns in Sections 13–16

**Finite outcomes and randomness.** The signature distinguishes the persistent S register, physical A alphabet and reconstruction randomness. The Gaussian slice has no additional public side channel. The squared-error characterization permits independent public randomness because its fixed-Bayes proof conditions on it correctly. The measure lower bound remains valid even after exposing an independent tape, but not by replacing realized output loss with marginal law equality.

**A2 budget quantifiers.** The displayed conclusion names the target Gaussian family and ranges over all finite-output approximating experiments for the lower bound. The upper uses the specified deterministic statistic, within 2^r<=S<=K N^(r/6). The N^(-1/5) target implies and is attained by order N^(r/10) labels in that comparison. It is not an optimal sample-size theorem for every physical objective.

**The invariant.** The attained profile includes its marked tasks and baselines. One-way garbling need not preserve excess risk relative to two different baselines; the reverse simulation is used explicitly in the excess-profile comparison. No product-topology closure is taken before a uniform task supremum. The terminal saturated quotient protects parameter decisions; extra latent targets require their own joint-law condition.

**The companion.** The canonical article includes the complete proofs it invokes. The companion preserves older results and introductions without making them premises of the new theorems. Its length is not evidence for the canonical article's depth. The build verifies preservation only; it does not confer an independent mathematical review on inherited statements.

## Required resubmission items A–H and minor comments

| Requested item | Concrete revision |
|---|---|
| A. Mathematical identity | The marked decision spectrum and its representation/realization theorem; quantitative slices explicitly typed. |
| B. Necessity | Exact successor-compatible partition characterization; continuation and delayed-query obstructions. |
| C. Invariant | Attainable risk sets, certified transport, equivalence and exponent invariance. |
| D. Bayesian/frequentist bridge | Minimal saturated posterior coordinate and parameter-uniform reconstruction; separate causal saturation theorem. |
| E. Local resources | Signature at definitions/results, certified finite-prefix/precision/description theorem, per-result signature table. |
| F. Pipeline arrows | Eleven-component theorem/hypothesis/quantity/obligation table, with direct A1 finite-command and modern A2 protocol instances. |
| G. Literature | Eight strands, identified primary versions and explicit scope of checks. |
| H. Infrastructure secondary | Build and provenance remain supplementary; none enters a mathematical proof. |

The quotient is a canonical completed sufficient sigma-field/equivalence class, not a preferred coordinate chart. Modelwise tree constants are uniform only under uniformly controlled structural constants. The fair hidden-shift exponent is now displayed as alpha=-2 log(r)/log(2) in the resource conventions. The new all-priors topological obstruction is continuous-coordinate impossibility, not an impossibility of Borel encoding. A single normalized Bayes problem suffices for the Gaussian lower bound because deficiency bounds every bounded decision problem. Poisson constants remain nonoptimized, and the A2 statement names its label-budget scope. The symbol Theta now denotes the typed spectrum; it does not assert an unproved physical universality class.

## Delivery and review status

Both manuscript views, full native sources, response, proof/resource/history/literature records and reproducible checks are prepared for the next referee. The publication record distinguishes local source/build commits from any actual GitHub ref update. At the time of this delivery the available GitHub connector is read-only and terminal access to github.com fails DNS resolution; remote publication is therefore not claimed. An additions-only Git patch and guarded import script accompany the revision so that these same files can be committed onto new remote revision branches without altering prior work.

The mathematical response consists of the stated proofs. Independent refereeing must still evaluate their correctness, significance and novelty. No formal proof certificate, external approval or journal acceptance is represented by the delivery record.
