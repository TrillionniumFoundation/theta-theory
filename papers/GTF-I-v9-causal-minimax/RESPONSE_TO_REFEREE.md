# Response to the v8 decision-spectrum referee report

**Submission:** General Theta Foundations I, ninth revision, September 23, 2026.  
**Controlling report:** `1e2ad3c7c5687e9cc9c0e7e0b37e983795f9f4c5`, `reviews/general-theta-foundations-i-v8-decision-spectrum-harsh-referee-2026-09-23/REFEREE_REPORT.md`.  
**Reviewed mathematical baseline:** `83a887b9212c54e5e09f88821296ccce3d051504`.

We thank the referee for distinguishing the genuine eighth-revision advances from the remaining structural question. The present revision addresses that question by proving a **controlled common-encoder converse**, Route C of §18. It retains the title, the general experimental framework and the complete earlier mathematics. It does not follow the proposed split-publication fallback. The new arguments appear in the canonical article, not merely in this response or in implementation metadata.

## §§1–3: central assessment, source identity and preserved advances

The new source is `papers/GTF-I-v9-causal-minimax/`. Its working branch begins at the controlling report itself, preserving both the report and its reviewed source in ancestry. The first new mathematical commit was `3bee574`; the complete new article architecture was then pushed in `b7182b8`. Subsequent source and publication identities are recorded by the build receipt and Git history rather than by a mutable assertion that an earlier branch name is current.

All v8 source files remain unchanged. The canonical v9 article includes the v8 spectrum, sufficiency, partition, tree, measure-presentation, sequential Gaussian and supporting mathematical bodies. The companion also includes the v8 historical introduction and the full predecessor material included by the v8 companion. `INHERITED_INPUTS.json` and the compiled label checks give byte-level and typesetting-level preservation checks. This preserves the advances acknowledged in §3 without pretending that preservation independently proves every historical theorem.

## §4: a framework versus an invariant theorem

Theorem `thm:v9-minimax` constructs an upper risk body directly from the finite controlled instrument and the fixed memory signature. It proves that the shared-seed attainable body is precisely the convex hull of **executable** deterministic common-encoder designs, plus the positive orthant. The positive support function determines this entire body, including a necessary-and-sufficient comparison criterion between two matched row systems.

The equality is not just transport along an assumed simulator. Proposition `prop:v9-partitions` characterizes its deterministic feasible objects by controlled continuation partitions. Theorem `thm:v9-occupancy` computes its support using an exact prescription recursion. Thus the finite marked spectrum has a constructive classification by one variational functional. The claim is not a classification of every infinite-dimensional or unbounded-resource experiment.

## §5: the causal converse and the primary minimax quantifier

The old single Bayesian quadratic objective is no longer the central converse. Theorem `thm:v9-minimax` allows a finite family of arbitrary bounded finite-action tasks, feedback through a finite controlled hidden-state instrument, and both Bayesian and worst-parameter rows. Its encoder is selected once before the task. The controller may know its task but cannot use the parameter row. All rows belonging to a minimax task use that task's full-history minimax baseline, not separate parameterwise oracle baselines.

Randomization is explicit. Independent shared randomness convexifies the joint design risks because its realization is averaged before the worst task/parameter and is not available for an adversarial change of parameter. Private fresh randomness at unchanged width is instead characterized by the finite polynomial flow problem in `prop:v9-private`. Example `ex:v9-privategap` proves the strict values `1/3` and `1/2` for a two-label three-symbol experiment. The theorem never freezes a tape and interchanges averaging with the worst-task maximum.

An optimal shared scheme uses at most `M+1` designs. Storing that design index, including the permitted randomized initialization, gives an actual private register with at most `(M+1)S` states. A signature forbidding randomized initialization must explicitly pay for the enlarged initialization convention; it is not silently equated with the stated model. Positive cardinality exponents agree for a fixed finite row family. The factor is not uniform over an increasing or infinite family.

## §6: constructing, rather than assuming, causal saturation

Theorem `thm:v9-saturation` constructs a quotient for every finite controlled instrument. The backwards key contains the parameter posterior, all next-report probabilities under every control, and the successor quotient classes. Backward induction proves that every deterministic coordinate satisfying likelihood saturation, raw-report predictive closure and recursive update refines this quotient. The resulting widths are simultaneously minimal within that explicitly specified class.

The quotient is independent of the strictly positive reference prior. The proof establishes this by parameterwise likelihood-ratio cancellation, including zero likelihoods, before changing priors. Its finite disintegration kernel reconstructs the report process for every admissible feedback policy. For rational input, the forward vectors, equality tests, quotient and reconstruction table are computable in polynomial time in the expanded history tree and its bit length. Exponential growth of that tree is not hidden.

Examples `ex:v9-saturationcost` and `ex:v9-predictioncost` separately show why future-report closure need not preserve likelihoods and why likelihood preservation need not close prediction. The former gives an exact `2^d` saturation cost for a one-class future-report quotient. This is a derived cost, not an assumption that a bounded-cost saturation exists in arbitrary continuous models.

## §7: effectivity and multiple resources

Theorem `thm:v9-compiler` supplies a finite-source alternative to the certified-tree energy oracle. Rational source and loss tables lead to rational risks and a finite exact optimization. A dyadic lottery with `p` initial bits approximates the optimal at-most-`M+1` mixture within `k 2^(-p)` risk. Fixed program length, initialization bits, persistent state, transient work and conservative bit-serial execution time are all bounded.

The compiler counts the design index in the private register, and it does not count physical acquisition of a finite report as free generation of a continuous sample. An external clock is an explicit convention; otherwise its values are charged. Exact non-dyadic reconstruction tables are computable but do not admit arbitrary fixed-bit exact sampling. Dyadic row approximation is charged through Proposition `prop:v9-stability`.

The old infinite predictive-tree theorem is retained with its energy and representation oracle assumptions. We do not describe this finite theorem as eliminating those assumptions for all infinite trees. It is a non-oracular realization theorem for a broad, precisely given finite input class.

## §8: a common variational principle versus unrelated regimes

Theorems `thm:v9-minimax` and `thm:v9-occupancy` provide the common controlled variational functional. Corollary `cor:v9-quadratic` gives its exact conditional-variance specialization for the **maximum over a family of tasks**, with one causal partition family. Corollary `cor:v9-pressure` gives its exponential-risk specialization, mixing exponential moments before applying logarithms and propagating nonnormalized Feynman–Kac occupancies.

The finite quadratic formula contains the old one-objective partition theorem. Compatible predictive-tree partitions are feasible objects of that same functional, and the retained energy estimates bound that class. The new delayed-query Gaussian proof uses the same conditional-variance geometry at the pre-query register. These are mathematical connections, not just common terminology.

We do not claim that Wasserstein law presentation becomes a decision-complete statistic or that a single scalar pressure determines every metric entropy. The article keeps the output marks that distinguish those questions. The selected main route is the controlled common-encoder converse; a complete metric classification of every retained infinite regime is not asserted.

## §9: genuinely dynamic Gaussian complexity

Theorem `thm:v9-delayed` acquires `d` noisy Gaussian coordinate observations before disclosing which scalar coordinate will be queried. Under a fixed product preparation, its causal excess is bounded above and below by constants times `S^(-2/d)`. The query-aware terminal checkpoint for the same scalar target has error of order `S^(-2)`.

The lower bound uses the register **before the query**. All coordinate readouts factor through its at-most-`S` labels. The posterior-mean vector has a density bounded below on a cube, and an explicit union-of-balls volume estimate gives the exponent. A base-`L` online register and a final query update give the matching upper bound without retaining a free query or transcript. This is not the terminal `nr`-dimensional output argument of the preserved append-only theorem.

## §10: the measure-valued quantifiers

The all-priors, fixed-time Wasserstein presentation result is retained with its actual quantifiers. We do not convert its time-dependent lower constant into a uniform positive constant, or claim a new single-preparation long-run law for that model. The general controlled converse no longer depends on promoting that static presentation theorem into such a claim. The new Gaussian preparation is fixed and its late-query obstruction is proved directly; it is not a replacement name for the Wasserstein theorem.

## §§11–13: pipeline-root claims and the two protocol adapters

The eleven-paper history remains part of the source record. All eleven retained Round-20 reports were read, together with the General Theta master outline, its implementation addendum, the controlling v8 report and the relevant v8 proofs and retained A1 protocol passage. `HISTORY_AUDIT.md` states the precise consultation boundaries.

The A1 finite-command adapter is strengthened in two distinct ways. Corollary `cor:v9-a1` solves the shared-seed **maximum-over-tasks** criterion by the common variance dual. Proposition `prop:v9-a1-private` gives the original private-randomization criterion at unchanged width as an exact finite polynomial optimization over the actual common failure update and compact readouts. The coefficients are the actual prior/likelihood integrals; arbitrary real coefficients are not called computable rational data. Continuous-command collision geometry remains its separate mathematical work.

The A2 count-experiment adapter and its stated joint window are retained. The source-pinned A2 statistical section and the independent primary algebraic chain remain distinguished. This revision does not edit that independent primary manuscript or claim it consumes GTF.

The new controlled occupancy, saturation and exponential-moment results give concrete conditional interfaces for finite report/control specializations relevant to C1 and D1. The hidden-state transition is typed as `(old state, control) -> (new state, report)`. One task controller is shared across hidden-parameter/phase components. The phase example computes the strictly positive common-policy value instead of summing phasewise optima. These address the finite information-pattern defects; they do not construct physical phases, prove Sinai Fourier estimates, repair deterministic contact expansions, or prove a nonlinear kinetic graph theorem by declaration.

Accordingly the pipeline file continues to distinguish two verified protocol adapters from nine conditional historical-model interfaces. That count is not inflated by attaching a theorem label to a still unverified physical kernel. The foundational advance pursued here is Route C, not an unsupported claim that Route D and all eleven model-specific proof programmes have simultaneously been completed.

## §14: terminal versus resource-sensitive Bayesian/frequentist comparison

The preserved standard-Borel terminal sufficient-statistic equality remains a cardinality statement under its stated unrestricted transient computation convention. The new finite saturation theorem constructs an actual sequential reconstruction, with an explicit product-state cost. The finite compiler then addresses rational finite data with finite program and execution resources. These separate assertions prevent a terminal disintegration kernel from being treated as a cost-free online algorithm.

## §15: novelty and closest predecessors

The introduction now discusses real-time coding and common-information control in addition to Blackwell, Le Cam and automata/predictive-state theory. The author preprint of Nayyar–Mahajan–Teneketzis was inspected at Theorem 3, Corollary 5 and Theorem 4: in particular, Corollary 5 already treats finite local memory and an unconditional designer occupancy when common history is empty. We therefore do **not** claim the generic occupancy/designer dynamic-programming idea as new.

`LITERATURE_COMPARISON.md` separates the inherited classical ingredients from the specific coupled minimax risk-body statement, controlled feasible-set converse, priced randomization, constructed saturation and Gaussian temporal comparison. Witsenhausen's publisher abstract was checked; Norberg's publisher record was checked, but a complete proof-by-proof comparison with its inaccessible full text is not represented as completed. The revision contains no exhaustive-priority or journal-acceptance certificate.

## §16: technical comments

**16.1 Transport.** The old controller-uniform transport theorem is retained; the finite coupling proof `prop:v9-stability` additionally displays the accumulated row errors and the factor two from comparing constrained risks and their full-history baselines.

**16.2 Terminal duality.** The retained proof fixes the task and encoder quantifiers, uses finite subexperiments and a finite dominated partition, and sends their uniform total-variation errors to zero. The new finite minimax proof works directly on a finite payoff matrix and needs no limiting approximation. Its finite primal and dual are displayed explicitly. No assertion is made that a pointwise, nonuniform approximation suffices for the standard-Borel theorem.

**16.3 Saturated statistic.** The terminal dense-prior construction retains its TV-continuity and common-version assumptions. The new finite construction provides actual finite posterior vectors and rational equality tests instead of assuming a computable dense real sequence.

**16.4 Causal saturation.** The old theorem retains its common-null-set hypotheses. The new finite proof constructs supported histories jointly over all parameters and controls and assigns null continuations explicitly. Its prior-independence and reconstruction proof includes zero-likelihood parameters.

**16.5 Partitions.** The converse now checks every action/report successor on the entire finite history tree. Task reachability cannot make the common encoder task-dependent. Private kernels are not silently replaced by independent taskwise partitions.

**16.6 Factor envelope.** The certified-tree assumptions and positive multiplier remain unchanged; the finite-source compiler is not described as computing that multiplier from an arbitrary oracle-free infinite source.

**16.7 Wasserstein entropy.** The retained packing and presentation proofs are unchanged. Their metric and all-priors marks remain explicit.

**16.8 Sequential Gaussian.** The append-only result remains intact; the new delayed-query theorem proves the different, stronger temporal distinction requested in §9.

**16.9 A2 window.** The known-mark, fixed-rank, local parameter and joint-budget restrictions remain in force. No unknown-mark or independent primary-algebraic consequence is inferred from that statistical comparison.

## §§17–18: the structural requirement and the chosen route

The new principal theorem is a controlled common-encoder minimax converse, not an enumeration of unrelated example rates. It provides one execution risk body, one support-function optimization, one controlled partition characterization and a dynamic recursion with the encoder coupling intact. Both randomization conventions are accounted for; a strict separation example prevents accidental convexification. The exact private A1 formula and priced finite compiler are consequences at the appropriate signatures.

This directly follows Route C. Within its finite controlled class it also gives the support-function classification and common variational structure requested in Routes A and B. It does not assert a classification of arbitrary infinite task families or a proof of the entire physical pipeline. Those distinctions are theorem hypotheses, not a withdrawal of the broader research programme.

## §§19–20: organization and resubmission

The manuscript is not split and no predecessor proof is deleted. The new controlled theorem leads the canonical paper; the full predecessor development is preserved in the companion. This is submitted as a new mathematical revision for independent reconsideration, with exact source and build evidence. The analytical arguments, the claimed connections and the novelty assessment remain available for a fresh referee to challenge. Compilation and finite diagnostics establish neither independent approval nor acceptance.
