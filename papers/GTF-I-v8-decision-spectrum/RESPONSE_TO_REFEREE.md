# Response to the nominal-v8 external report — actual eighth decision-spectrum revision

**Manuscript:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction.  
**Author:** Qian Qi. **Date:** 23 September 2026.  
**Controlling report:** `fc6d51a47b42a3f097ea530b67616591c421db3b`, report blob `0559636028b2122cc6c6690ae8668b4f1bc026c5`, `reviews/general-theta-foundations-i-v8-spectrum-external-harsh-referee-2026-09-23/REFEREE_REPORT.md`.

The latest report appeared during this revision. It reviews the unchanged v7 mathematical source under the nominal `v8-spectrum` branch and adds submission-identity and current-A2 dependency objections to the preceding report. We read it in full and made it controlling. The complete response initially written to v7 round 2 is preserved separately as `RESPONSE_TO_V7_R2.md`; its contents are not silently relabelled as a response to a different report.

The mathematical response is an actual new article organized around a marked decision spectrum, its causal transport, a parameter-uniform sufficient quotient, and an exact finite-history characterization of causal realizability. The tree, posterior-measure and sequential Gaussian results are evaluated as explicitly different marked slices. Source and build materials identify this article; they are not the argument for its significance.

## Sections 1–3 and objection of submission identity

The referee is right that a branch pointing only to an old review is not a new manuscript. We do not treat the existing nominal-v8 branch as a mathematical edition. The new article has its own native directory `papers/GTF-I-v8-decision-spectrum/`, source manifests, canonical and complete-development TeX entry points, substantive new proofs, a theorem delta and a response to this controlling report. The old nominal-v8 branch is not overwritten.

There remains an execution limitation, which must not be turned into a false scholarly claim: the current connector exposes reads only and terminal GitHub access fails DNS resolution. The article and new commits have been produced locally, and the delivery contains an additions-only patch with a guarded real-history import/rebuild script. **No remote publication or referee-ready GitHub branch is represented as completed.** The importer uses the actual latest review commit as its base and refuses to push the local source-archive reconstruction as though it were the whole repository.

## I–II: one mathematical centre and an actual theta invariant

Section 2 defines the marked spectrum

`Theta_E(b;D) = inf_Q sup_{d in D} [r_E(Q,d)-beta_E(d)]`.

The encoder Q is chosen before the task d. A mark declares the target, output type, loss, horizon and Bayesian or minimax convention. Persistent states, physical labels, acquisition length, program description, precision, workspace, time and randomness are separate signature coordinates. The definition does not take coordinatewise closure before an infinite uniform supremum.

Theorem `thm:v8-spectrum` fixes initialized causal simulations, the equivalence of their induced joint laws, their global parameter/policy/task quantifiers and their resource transformers. Composition composes the transformers and adds simulation errors. Raw risks have a one-way transport inequality; excess risks also require the displayed control of the full-observation baseline. Exact resource-controlled equivalence consequently gives an invariant family of attainable spectra, including cardinality exponents under fixed budget dilations.

Theorem `thm:v8-duality` identifies the all-bounded-terminal-decision slice with deficiency at a fixed common encoder. This is explicitly the classical Blackwell–Le Cam criterion in the stated compact, TV-continuous setting, with a self-contained finite minimax and approximation proof; it is not advertised as a new unconstrained randomization theorem. The invariant is a family indexed by marks and resource signatures, not a universal exponent that erases the experiment's geometry. Tree quadratic prediction, realized posterior-law presentation and sequential Gaussian decision completeness are actual instances of that same definition.

## III: a necessity theorem instead of another sufficient tree criterion

Theorem `thm:v8-congruence` gives an exact finite-horizon formula for finite report alphabets and a fixed Bayesian weighted quadratic target: the optimum over randomized, time-dependent S-state observers is the minimum conditional-variance cost over all width-S successor-compatible history partitions. Both implications are proved: a machine induces compatible fibres, and compatible partitions construct a machine. Independent coding tapes can be frozen for this fixed Bayesian criterion; no minimax supremum is interchanged with that averaging argument.

Thus same-order static/causal realization is equivalent to existence of compatible partitions with the corresponding width and variance cost. A particular suffix tree is sufficient, not necessary. Relabelling histories does not change the characterization. The continuation corollary states the classical stationary congruence obstruction, with its credit to Nerode. The queried-bit example has a two-valued checkpoint but requires 2^d exact persistent states and has an entropy lower bound for approximation. This exhibits a genuine temporal obstruction that static marginal geometry cannot detect.

For the modern A1 finite-cell instrument, `cor:v8-a1` derives the accepted and common-failure likelihoods, the actual history law and posterior query vector, then invokes this characterization. It is a finite-command, fixed-prior, scalarized specialization, not a claimed solution of the different continuous-command or privately randomized maximum criterion.

## IV–V: simultaneous resource bounds and finite acquisitions

Theorem `thm:v8-certified` replaces exact ordering of arbitrary real energies by certified rational estimates within a fixed relative factor. Taking the minimum over all contiguous factors produces an envelope with the exact prefix/suffix monotonicity needed by a rational threshold cut. The proof establishes balance, arbitrary-centre lower bounds, exact charged tree vertices and a same-order budget conversion.

An acquisition reads only until it reaches a leaf, at depth O(log S); the remaining snapshot is never read or stored. The theorem fixes the physical interface: the snapshot is frozen during these charged microsteps and the output deadline permits them. It does not claim to observe an evolving state after an unmodelled delay.

For bounded finite-dimensional readouts and an explicitly assumed effective representative oracle, the compiled machine has precision p=O(log S), program size O(S log S+Sd p), transient storage O(log S+dp), and O(log S) symbol queries, with stated RAM or conservative bit-table costs. Offline oracle complexity is separately excluded rather than hidden. Infinite-dimensional Hilbert readouts are not called finite-bit outputs. `RESOURCE_SIGNATURES.md` distinguishes this genuine finite-description result from pure cardinality results.

## VI: bridge from Bayesian coordinates to parameter-uniform experiments

Theorem `thm:v8-sufficient` constructs posterior coordinates from a countable dense parameter set and a positive dominating mixture. One disintegration reconstructs every member of the compact TV-continuous experiment. The completed sufficient sigma-field is minimal; changing the dominating prior changes coordinates but not the parameter-decision equivalence class. A constant future-test counterexample explains why an unsaturated prior-relative quotient does not suffice.

The causal theorem `thm:v8-causal-sufficiency` adds precisely the recursion that is needed: a reference predictive kernel factors through the recursive state, and all parameter likelihoods are functions of that state. Conditioning on successive quotient states cancels the likelihood ratio and gives a parameter-independent causal reconstruction under every admissible policy. If the quotient has K0 values, the simulator's retained state costs K0 S; a general Borel quotient is not falsely called finite memory. Extra latent targets require their own conditional law in the saturation condition. Equality of report laws alone does not establish equality of hidden targets.

## VII: consequential causal morphisms

The morphism data, initialized execution, policy lifting, equivalence of induced joint kernels and monotone budget transformer are fixed in Section 2. Associativity is kernel composition modulo the stated equivalence and associativity of transformer composition. Proposition `prop:v8-forgetful` gives the finite-horizon uncontrolled forgetful map to transcript experiments and specifies which causal/resource information it discards. Theorems `thm:v8-spectrum` and `thm:v8-causal-sufficiency` then use these morphisms to obtain invariant profiles and concrete quotient reconstructions. No universality or categorical novelty is claimed for elementary kernel composition itself.

## VIII: a matching nonlinear measure-valued result

Theorem `thm:v8-measureentropy` proves the matching order 1/log(S+1) for uniform presentation of a probability law on [0,1] in expected realized W1 error. The lower bound uses a binary packing whose W1 distances are exactly scaled Hamming distances and permits independent randomized coding. The upper bound is the explicit empirical-grid cover. This is one minimax law-presentation task, not a supremum of point-prior Bayes risks that would disclose the unknown law to the decoder.

The nonlinear instrument's update is bi-Lipschitz on laws, with constants 1/5 and 6/25. For every fixed time, the all-priors posterior class inherits a matching logarithmic register order. The lower constant can deteriorate with time; no arbitrary fixed-prior stationary lower rate is asserted. The continuous-coordinate obstruction is proved on finite-dimensional simplices using Borsuk–Ulam. It rules out every continuous finite-dimensional exact coordinate for all bounded Lipschitz tests, not merely prescribed polynomial moments. It does not exclude discontinuous Borel encodings.

The separate one-probe simulation example is intentionally distinguished from realized-law presentation. Randomly simulating one output law can be easier than presenting one close realized posterior. These are different output tasks, not contradictory estimates for the same invariant slice.

## IX: a genuinely sequential Gaussian total-register theorem

Theorem `thm:v8-seqgaussian` observes n independent r-dimensional Gaussian blocks with a compact full-dimensional parameter product and retains only the current S-state register. Its final decoder receives no external transcript or public seed. The decision-complete terminal spectrum has order S^(-2/(nr)). The lower bound covers every randomized time-dependent S-state encoder because its terminal experiment has at most S outcomes. The upper rule appends quantized coordinates while never exceeding S register values, then uses the retained positive reconstruction.

This is a dynamic total-register consequence of the same marked spectrum. It is not a relabelling of an n-message channel: supplying the transcript changes the resource model. Constants depend on the fixed horizon and Gaussian geometry. The result is not a claim about growing-n uniform asymptotics or all Gaussian filtering models.

## X–XIII: current A2 and theorem-level pipeline contracts

The new report correctly identifies the stale endpoint. We read the complete A2 v121 dependency map at `c05cfac02579638987f57aa5727c4cc8880f9f6a`. The fresh repository check already found A2 **v122**, source `790fff70e40ccdbe97d2569792535d6fe6cb6b2a`, publication `37480f3872b5c9f4ae18731e60a799986114c427`; we read its complete dependency map and statistical body. The latter is exactly Git blob `e52ed7b8d75f840e73bed815ca0441dc21a886c3`, unchanged from the earlier consulted statistical section. That equality was checked, not inferred from its filename.

Corollary `cor:v8-a2adapter` is an explicit GTF-side adapter for the actual current known-mark exposure protocol. It verifies DB*=I, the compressed mean map, full row rank, positive covariance and positive local exposures, then invokes the retained count/Gaussian theorem and the new decision-spectrum transport. It preserves the joint S<=K N^(r/6) window and the specified Gaussian target. This supplies a concrete theorem arrow, not an assertion that v122's independent primary algebra has already been rewritten to use GTF.

The v121/v122 primary chains concern weighted determinantal and intrinsic ramification/primary constructions; their maps explicitly do not rely on the retained statistical sections. They are recorded as independent. The historical Sinai A2 is also a separate component from this modern statistical/algebraic manuscript. No spectral, stopped-path LDP, particle, nonlinear-semigroup, common-domain or phase conclusion follows merely from the name of a GTF object.

`PIPELINE_DEPENDENCIES.json` records all eleven components with exact source snapshots, actual GTF/adapter labels, verified or conditional hypotheses, the transported quantity and remaining model work. Every noninstantiated historical gate is explicitly conditional or not used. The checker rejects missing labels and moved observed endpoints; its optional live mode reports network failure as failure. JSON validates identities and declared arrows, not the mathematical truth of hypotheses. This is stricter than a prose claim that every downstream paper has already adopted GTF.

## XIV–XV: novelty and the preservation companion

The introduction and `LITERATURE_AUDIT.md` compare the actual mechanisms with predictive/causal sufficient states, classical automaton congruence, Blackwell/Le Cam sufficiency and randomization, filtered experiment comparison, zero-delay coding, posterior contraction, Wasserstein entropy, and functional/graph-directed quantization. They explicitly distinguish fresh primary-text reads, publication-record checks and unavailable full texts. No priority clearance is inferred from incomplete access.

The canonical article proves the new chain and includes every supporting v7 proof it invokes. The complete-development companion preserves all earlier bodies and is not used as implicit evidence of depth or as an unrefereed substitute for a missing principal proof. Old source editions remain untouched. Numerical diagnostics and rendering records remain supplementary.

## Section 19 technical comments

Bounded unary chains remain an actual structural hypothesis for the tree count and budget conversion. Exact suffix closure is a construction; necessity is expressed instead by compatible partitions. The arbitrary-centre static argument is retained and independently used for the rational-threshold cut. Deficiency directions remain explicit: garblings have zero forward deficiency, general experiments require both directions for symmetric comparison, and baseline control is not dropped. Positive reconstruction remains a genuine Markov kernel. The A2 sample/register window and the distinction between physical randomness, proof-only jitter, private reconstruction, public coins and persistent seeds are repeated at the applicable statements.

## Section 21 requested conditions A–K

A is satisfied at the level of actual authored source/PDF and a guarded import package, but remote publication is explicitly pending. B/C/F are answered by the defined marked spectrum and its transport and decision-completeness theorems. D is answered by the exact compatible-partition theorem and continuation obstruction. E is answered by likelihood saturation and causal reconstruction. G/H are answered by the exact-source contracts, verified finite-command A1/current A2 statistical adapters and refreshed v122 endpoint. I is answered by the sequential total-register Gaussian theorem. J is answered by the certified finite-prefix/finite-description theorem. K is addressed by the mechanism-level primary-literature audit, with its access limits disclosed.

The response does not declare the venue judgment closed by the author. The next referee is being given actual new proofs and their precise scopes, rather than another empty branch name or an acceptance-by-infrastructure claim.
