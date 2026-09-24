# Response to the fourteenth pipeline-aware referee report

**General Theta Foundations I — Revision 30**  
**Positive Realization and Exact Streaming Memory**  
24 September 2026

Controlling report: `reviews/general-theta-foundations-i-v29-intrinsic-continuation-pipeline-harsh-top4-r14-2026-09-24/REFEREE_REPORT.md`, frozen at `c039e5bc8bc8b30fca92246bc1458f66214522e1`. Reviewed publication: v29 at `b0bd13753456c15815b174db1106e2ce6ee7433b`, native source `966cb98627d3384f756c3d7a0d9a680e4f59d2e9`.

The report accepts the v29 intrinsic lower argument and its compatible residual-vertex construction, but identifies the simplex hypothesis, the missing intermediate-signal analysis and the probabilistic-residual priority boundary as the main mathematical limitations. The revision responds with a necessary-and-sufficient rank-saturation criterion, an exact-synthesis rate for every fixed interior signal, a priced streaming construction, an exact approximation exponent, a larger minimal-profile signal window and a sharp threshold in an infinite sequence of dimensions. The paper is reorganized as a focused article. Every inherited result remains in unchanged supporting and cumulative volumes.

Stable labels below are resolved to final theorem numbers and pages in `evidence/THEOREM_LOCATIONS.json`. The analytic proofs, not the checks, establish the claims.

## 7.1 — Priority and the omitted 2002 probabilistic-residual work

**The omitted reference is restored, the operational distinction is proved directly, and source-access limitations are explicit.**

Esposito–Lemay–Denis–Dupont (ICGI 2002, LNCS 2484, 77–91, DOI 10.1007/3-540-45790-9_7) now appears in the main article. Its publisher abstract announces finite generation by residuals and canonical minimal forms. We inspected the full later Denis–Esposito treatment, especially the probabilistic-residual definition in Section 2 and Propositions 16 and 19. We do not pretend that the paywalled 2002 chapter itself was obtained in full or attach invented theorem numbers to it. The original Heller/Norberg proof-level audit likewise remains distinct from this comparison.

`thm:prfa-gap` constructs a finite stochastic language within the paper's own growing query family. All length-n query residuals are the `2^n` vertices of an affine cube. Positivity and remaining word length force a residual automaton to represent each by actual query residuals, so each extreme point requires a state. An arbitrary positive automaton instead uses the online reservoir construction and has at most `(n+1)*(n+2)/2+n*(n+1)+1` states. Its phase and generated-query buffer are included. Thus residual-only minimality cannot be used as all-machine minimality for this explicit task.

`prop:ranks` formally states `rank A <= rank_+(A)=K(A) <= K_aff(A) <= K_res(A)` for a single output alphabet. It also explains why a queried family requires every block to normalize, so ordinary nonnegative rank of the concatenated matrix is only a lower bound without those constraints. The comparison with Gillis–Glineur specifies the transpose-normalized restricted-rank convention. Stable positive realizations and residual shift constructions are acknowledged as classical, not claimed as new names for established theory.

A further important adjacent result was checked rather than overlooked: Ambainis–Nayak–Ta-Shma–Vazirani already prove the classical communication exponent `1-h2(p)` and logarithmic communication overhead for recovery probability at least p (Theorems 2.1–2.2 of their inspected 1998 preprint). The abstract and introduction explicitly attribute that exponent. The present operational theorems require exact conditional probabilities and charge the entire streaming computation. We do not use the entropy function itself as novelty evidence.

`LITERATURE_AUDIT.md` records the objects, generator restrictions, minimality statements, shifts, completeness conventions and inspected material. The explicit comparison is stronger than a bare bibliography; it is not represented as exhaustive priority clearance.

## 7.2 — Beyond residual-hull simpliciality

**Addressed by an exact equivalence for simultaneous support-rank saturation.**

`thm:coherence` states necessary and sufficient conditions for `K_t=s_t` at every charged cut. A competing rank-saturating realization must use exactly `r_(t,j)` generators for component j. Enclosure and dimension force those generators into the component's affine slice and make them independent. Its actual rows then satisfy common positive shift equations. Conversely, any such collection of enclosing simplices and shift coefficients constructs a single normalized causal machine.

The residual hull need not be a simplex, and the generators need not be residuals. The old componentwise-simplicial theorem is a sufficient special case obtained by choosing residual vertices. The growing weak-signal query family has nonsimplicial cube residual hulls and is rank-saturating by explicit non-residual enclosures. This supplies an unbounded family, not one new polytope shape in a small example.

`cor:algebraic` writes recognition of this equality profile as a finite existential polynomial system for fully listed rational or real-algebraic input. The defining equations have degree at most two in generator and mixing variables. Cylindrical algebraic decomposition gives a decision and an algebraic witness. Input algebraic numbers require defining polynomials and isolating intervals. No efficient algorithm in a succinct horizon is inferred.

The theorem characterizes rank saturation, not the globally least positive dimension when rank is not attained. It gives the precise simultaneous compatibility test; it does not invent an example of statically rank-complete cuts failing joint realizability. Autonomous shared-row equalities remain extra constraints. `prop:squares` now gives full proofs both of a nonsimplicial rank equality and a full-support strict rank gap.

## 7.3 — The intermediate random-access regime

**Addressed by matching leading asymptotics for every fixed interior signal, together with new exact finite thresholds.**

Let `I(eta)=1-h2((1+eta)/2)`. `thm:rate` proves, for every fixed `0<eta<1`,

```
n I(eta) <= log2 K_n(eta) <= n I(eta)+O_eta(log(n+1)),
n I(eta) <= log2 W_n^ad(eta) <= log2 W_n^fo(eta)
          <= n I(eta)+O_eta(sqrt(n log(n+1))).
```

This separates checkpoint, adaptive-acquisition peak and fixed-order streaming peak while showing that all three have the same leading exponent. It covers the entire fixed interior interval, not only the v29 endpoint windows.

The all-machine lower bound uses exponential corner caps for arbitrary outer-cube generators. The upper proof samples a codebook and proves its convex hull contains the whole inner cube, through a weighted Hamming-layer bound, an l1 sphere net and a support-function argument. Consequently every row is synthesized **exactly**. No sign-bias inequality is substituted for the requested conditional law. The codebook is fixed offline, not selected for free at runtime.

`lem:blocks` converts any exact block codebook into a sequential machine with peak at most `max(2,2^ell M^floor(n/ell))`. Both the raw partial block and all compressed block labels are charged. Taking block length of order `sqrt(n log n)` gives the stated whole-schedule bound. This distinguishes storage used to compute an encoder from the final message length.

`thm:approx-rate` additionally proves the sharp fixed-tolerance exponent `I(max(eta-2 epsilon,0))` for uniform row-TV error epsilon. The converse controls every row, not one selected prior. The construction exactly realizes the appropriately attenuated channel; at tolerance eta/2 a fair response uses one query state.

`thm:reservoir` improves the exact minimal profile window from `eta<=n^(-2)` to `eta<=1/(2n-1)`. It has precisely `t+1` acquisition states at every time. Its explicit stochastic update retains the old label with probability `t/(t+1)` and otherwise records the new positive index or zero. Only a label is stored.

`lem:trace` proves that **any** `(n+1)`-vertex checkpoint enclosure requires `eta<=1/n`, not merely that one construction fails above that value. `thm:hadamard` gives an online matching construction whenever a Hadamard matrix of order n+1 exists, including every n=2^k-1. Thus for those dimensions the checkpoint and whole-streaming n+1-state thresholds agree exactly. The construction may use n+1 states already at an early cut; its claim is peak optimality, not simultaneous t+1 optimality.

These results do not determine every finite integer state count, the sharp lower-order streaming excess, or a uniform critical phase diagram for eta varying with n. Explicit finite enclosure/block bounds are provided without overstating what the fixed-signal limits prove.

## 7.4 — Controlled scheduling

**The general rank-saturation criterion permits specified causal action arrays; unrestricted policy optimization and adaptive collision validation are not claimed solved.**

Next-action probabilities in `thm:coherence` are independent of unread reports, while subsequent updates use the observed report. Buffers and protocol distinctions are included in the declared cuts. Hence its compatible realization is causal for informative action interfaces, not just a terminal matrix factorization.

The exact rate and finite-query converses cover adaptive acquisition under the explicit terminal barrier. We agree with the report that this is not the full physical scheduling problem. The old fixed-clock collision result and its twelve-state bound retain their original quantifier in the supporting volume. No unsupported universal adaptive twelve-state bound or better feedback schedule is asserted.

The revision pursues the report's rank-compatibility and intermediate-signal routes as its main progress, rather than claiming all proposed research directions have been closed.

## 7.5 — Consumers and repository history

**A uniform approximate-sensor theorem is proved locally; no independent historical analytic gate is claimed discharged.**

The exact and approximate streaming laws give a new uniform memory–error theorem for an installed one-query sensor, and `cor:consumer` transports it through bounded decision losses and independent reinstalls. Jointly independent answers to all n queries are deliberately distinguished: their product channel has full rank `2^n`, so a one-query code cannot be silently reused to supply that law.

This is a genuine mathematical consequence but is not described as an independent A2/B4/C2 theorem unlocked by the present paper. The current frozen Round-Seventeen ledger and v29 derivations were consulted. Their Fourier/LLT, LDP, nonlinear semigroup, common-domain and optional-projection obligations remain unchanged. The report's requested external analytic consumer remains a separate objective, not a fabricated metadata edge.

## 7.6 — A focused article without deleting the mathematics

**Addressed by separating the journal core from the preserved complete volumes.**

The canonical `paper.pdf` now contains a single compact theorem sequence: compatible positive rank, finite online thresholds, exact interior-signal rates, uniform approximation and a precise residual-automaton comparison. It has its own definitions, notation table, proofs, literature boundaries and conclusions. No proof needed for its new claims is delegated to a build receipt.

The entire v29 article is reproduced without alteration as `supporting-results.pdf`. The new complete mathematical and development volumes append the unchanged v29 cumulative volumes after the full current article and a divider. All original repository sources remain at unchanged paths. Thus the accumulated physical, saddle, transport, revelation, autonomous and historical derivations are preserved while no longer obscuring the main article's new theorem hierarchy.

## Editorial dispositions

The residual-hull simplex condition is explicitly only sufficient; the new coherent criterion is necessary and sufficient for a different, precisely specified equality question. A notation table is in the introduction. Static normalization, queried block constraints and ordinary/restricted/unrestricted/residual ranks are in `prop:ranks`. The square examples have complete proofs. Exact algebraic input and the decision procedure are stated. The former weak/strong windows are identified as regimes, while the new theorem fills the fixed-signal interval at leading exponential order. Known atomic rows, external clocks, acquired calibration and finite-bit implementation remain separate resources. The conclusion has distinct paragraphs for proved rank saturation, unrestricted realization/policy questions, and remaining finite-size or varying-signal questions.

The checks and publication records support reproducibility only. They do not establish priority, independent proof verification, or a top-four editorial decision.
