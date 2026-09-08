# Referee report on A1 English v25

**Manuscript:** *Attainable information, exponent collisions, and adaptive order*, Qian Qi.  
**Assessment date:** 7 September 2026.  
**Examined revision branch:** `revision/a1-english-v25-adaptive-graph-width-2026-09-07`.  
**Immutable submission:** `8a84075ee518035069d38fd9262bd455aff4ac86`.  
**Principal entry point:** `papers/A1-english-v25/main.tex`, with the explicitly shared, unchanged v24 dependencies.  
**Controlling report:** `c7fee8b92fd779573bd3b9ccdf5e37183c5cefa6`, `reviews/a1-english-v24-harsh-independent-2026-09-07/REFEREE_REPORT.md`.  
**Previous submission:** `6f648bc3da0543e8361b4053ae7da33cb172f597`.

This is an owner-requested, AI-assisted repository assessment at the requested Annals/Inventiones/JAMS/Acta level of scrutiny. It is not an appointment by any journal, a human referee report, or formal proof certification. The assessment distinguishes a mathematical defect from a negative judgment of mathematical significance. Its computational checks were designed after reading the submission, without importing the author's implementation.

## 1. Recommendation and principal conclusion

**I do not recommend acceptance at the requested four-journal level. My recommendation is rejection on the significance assessment in Section 8, not rejection for a demonstrated false principal theorem or an unresolved central proof gap found in this reading.**

The revision makes a genuine mathematical addition. It is not merely a new title, another compilation receipt, or a rearrangement of the previous result. The added theorem compares the optimal deterministic vertex order with arbitrary measurable history-dependent order selection, uniformly through calibration collisions, for a precisely specified fixed graph experiment. The common-event argument addresses the central difficulty correctly: conditioning on an adaptively selected order would generally destroy the product-history minorization. The manuscript does not make that invalid conditioning step.

The resulting graph-width interpretation and the three-edge ordering transition are coherent consequences. In particular, the stated two-resolution penalty is not contradicted by the fact that the graph is fixed: calibration approaches a collision, and the relevant bit differences can diverge even on that fixed graph.

Nevertheless, I judge the additional advance insufficient to change the requested venue recommendation. Once the scalar acquisition charts and product compression law are available, the new converse is a finite-selection small-ball argument on a common positive-mass event. The graph optimization and bit inversion then organize the scalar profiles rather than introduce a new graph-structural theorem. This is a useful and nontrivial extension of the existing classification, but I do not regard the mathematical depth and reach demonstrated here as exceptional enough for the requested venues. This is an editorial assessment, not a claim that an identical theorem has already been published.

There are also concrete corrections: a materially incorrect bibliographic entry, an absent proof-ledger file at the location invoked by the response, and a diagnostic negative control that does not actually instantiate the quantifiers it purports to test. These should be repaired. They are not substitutes for a central mathematical objection, and repairing them would not by itself reverse the significance judgment.

## 2. Submission identity, reading scope, and evidentiary limits

All v25 mathematical readings were pinned to the submission commit above. Relative v25 paths below refer to [this immutable directory](https://github.com/TrillionniumFoundation/theta-theory/tree/8a84075ee518035069d38fd9262bd455aff4ac86/papers/A1-english-v25). References to inherited scalar files refer to [the sibling v24 directory at the same commit](https://github.com/TrillionniumFoundation/theta-theory/tree/8a84075ee518035069d38fd9262bd455aff4ac86/papers/A1-english-v24).

The reading included the complete new mathematical source: `v25/introduction.tex`, `v25/graph_model.tex`, `v25/adaptive_proof.tex`, and `v25/graph_consequences.tex`; the principal entry point and additional bibliography; the README, response, build script and diagnostic script; and the inherited direct scalar route. That scalar route comprises the introduction and classification statement, experiment and resource definitions, risk criteria, exact information statement, transversality argument, analytic inputs, collision flags, direct checkpoint and causal proofs, and collision consequences.

The controlling v24 report was read rather than inferred from the author's response. For historical attribution, the shared-memory v10 entry point, the statements and principal constructions in its Section 8, and its complete scheduling Section 9 were inspected at `da5abea9f40244879115d5fbcfbda375bc9a123e`. This is a targeted comparison with the actual shared-memory branch, not with the different v10-effective branch and not an exhaustive new audit of v10.

The GitHub comparison from the v24 submission to v25 returned 11 commits and 15 changed files, all additions: the ten v25 files and five files belonging to the v24 review. It reported no modification or deletion of a v24 manuscript file. This independently supports preservation of the committed v24 source tree, including the retained companion. It is not an independent reproduction of the author's expanded-source block counters, a typesetting audit, or a new proof review of every companion result.

The new theorem's direct proof does not invoke the separate companion developments. I did not conduct a new exhaustive audit of the algebra, exact-kernel, uncertainty, mechanical, decision, or effective-construction companion material, nor of the eleven-paper program. Previous favorable assessments of those materials are not relabelled as new verification.

Authenticated GitHub source reads and writes were available. Direct runtime access to GitHub failed at DNS resolution, so no native checkout or two-volume LaTeX build was executed. Neither submitted PDF was visually inspected. The author's build and diagnostics were inspected as source, not adopted as successful executions. The independent local diagnostic execution described in Section 10 is separate from all author and prior-referee receipts. No successful GitHub Actions run is asserted.

## 3. Disposition of the controlling report

| Controlling matter | v25 response and source | Disposition in this review |
|---|---|---|
| E23.1, as assessed in v24: mathematical significance | The author adds an adaptive-order theorem and a collision-dependent change of optimal order, and explicitly credits the inherited deterministic composition law. | A genuine addition requiring reassessment. The venue judgment remains negative, for the reasons below; this is not an unclosed missing-proof checkbox. |
| E23.2: a submission-focused principal article, with separate complete companion | The direct scalar route remains active; the new graph proof uses that route rather than importing essential companion-only assertions. The v24 source is unchanged in the repository comparison. | Remains closed at the source-architecture level. The existence of a retained companion is not a reason to count all its pages as principal-article pages. |
| E23.3: place the intersecting-collision example earlier | The existing four-cell example remains in the retained introduction. The star example is additional, not a replacement. | Remains closed. |
| Earlier E22 obligations already closed by the controlling report | No weakening or removal of the relevant scalar statements was found in the committed changes. | Not reopened. This does not amount to a fresh audit of every companion theorem. |

The response is appropriately explicit that the new theorem is submitted for review and has not already earned a favorable significance verdict. It does not claim graph-size uniformity, a correlated-prior theorem, or equivalence between batch-boundary memory and memory after every raw report. These disclosures must remain visible, but they are not defects to be invented after the fact.

## 4. What the new theorem actually classifies

For a fixed finite loopless multigraph, each edge carries an independent scalar positive experiment, a fixed full-support prior, and fixed acquisition and completion lengths `n_e,m_e >= 1`. Visiting its first endpoint acquires its first block; visiting its second endpoint completes it. Commands are exogenous and revealed only after the next vertex has been selected. The controller may choose the vertex, not the command values.

A vertex is an atomic observation batch. Only one joint label, with at most `M` possible values, persists between batches. The scheduler's history-dependent information is included in that label. The known graph, calibration, clock and fixed real-valued program are read-only. Temporary work on the current batch is not this memory resource. Thus the theorem is not a statement about total computational space or the maximum memory inside a batch.

At a queried boundary, the future menu is the full tensor product of the remaining scalar failure-product menus. Unopened edges have known prior vectors; completed edges contribute one; active edges contribute their acquired remaining-moment vectors. A single independently selected query is executed and all its remaining raw trials are counted, even after a nonfailure. There is one queried checkpoint per run. The total count is `sum_e(n_e+m_e)` for every order.

For each active edge, the inherited determinant volumes are retained up to its own acquired cap `p_e`. For a cut `F`, the coefficient `A_{F,k}` is the maximum of the products of edge volumes over allocations summing to `k`, with every individual cap enforced. The risk profile is `Theta_F(M)=max_k(A_{F,k}/M)^(2/k)`. The graph profile is the minimum, over vertex orders, of the maximum cut profile along the order.

Theorem `thm:v25-adaptive` compares both optimal risk criteria with this graph profile. It requires one controller across all boundaries. In the maximum-tape criterion, coding randomness is averaged before the tape supremum. In the average criterion, the law includes actual commands and actual report probabilities; it is not the command law conditioned on an all-failure word.

The stronger converse grants the scheduler its full revealed past and grants the decoder the finite order prefix, while limiting retained command/report information to `M` labels. For a fixed graph this finite extra side information can be absorbed by the constants. The theorem does not grant an uncharged continuous history to the decoder, and it does not assert a graph-uniform bound on the cost of the order information.

These distinctions are substantive. With correlated edge priors, completed edges could still inform active or unopened edges. With chosen or previewed commands, the common acquisition event need not have the asserted policy-independent law. With raw-internal checkpoints, a vertex cut need not capture the actual peak resource. None of those different models is being established by this manuscript.

## 5. Technical assessment of the adaptive converse

### 5.1 The inherited scalar ingredients are adequate

The graph proof needs more than fixed-calibration rank. The necessary inherited results were checked directly in `text/collision_flags.tex`, `text/analytic_inputs.tex`, `text/collision_direct.tex`, and `core/03_transversality.tex`.

At the attainable binomial command tuple, the unnormalized product tangent has `n(r-1)+1` distinct monomials. Strict mixed-moment positivity follows from the integrated product of two generalized Vandermonde determinants. Full support supplies positive mass on separated interior intervals, so no density of the latent prior is required. Evidence normalization removes exactly the one-dimensional constant direction, giving the stated acquired rank.

At repeated future nodes, an initial list of divided differences spans a complete Hermite family, including all lower derivatives in each cluster. This is the relevant fact; an arbitrary selection of isolated logarithmic derivatives would not suffice. Adjoining the constant test and pairing with the attainable tangent gives the required normalized surjectivity. Bounds on positive powers times logarithms justify continuity through collisions, and fixed-dimensional compactness over finitely many label orders gives a uniform positive least row singular value.

The Leja matrix is uniformly invertible only on its leading nonzero block. This is exactly the block used in the prediction lower bound. Zero scales are not inverted. Formal probe coefficients remain full-column-rank when evaluated exponent values coincide: coincidence imposes relations on reachable moment vectors, not on the symbolic change-of-basis matrix. These two distinctions prevent spurious singularity objections.

The global covering step controls the entire attainable image, not merely the regular patch used for the lower bound. At a fixed report word its coordinates are rational in command variables with positive evidence denominator; prior moments are real coefficients. Independent normalization of the factors bounds the image dimension by the acquired cap. The bounded-format anisotropic covering argument truncates at that dimension, with the small-integer-budget case treated separately. Its classical real-geometric input should be credited, not counted as a newly proved general entropy theory.

Finally, the causal update is in raw remaining moments. The Bayes denominator is bounded below on posterior-mixture segments, and the quotient estimate contains no reciprocal collision gap. The error recurrence includes earlier quantization errors. I found no substitution of separately optimal checkpoint encoders for one causal filter.

These observations support the use of the scalar route in v25. They are not a claim of formal verification or of uniformity over all full-support priors or unbounded horizons.

### 5.2 Prescribed-order product compression

Source: `v25/graph_model.tex`, `prop:v25-fixed-order`, `eq:v25-tensor-metric`, and `eq:v25-product-cover`.

For a deterministic order, grouping factors by independent edge gives the entire product of active reachable images. The tensor probe matrix has a fixed left inverse. Selecting tensor coordinates with every other index constant recovers each raw edge vector. This is a bounded linear recovery map on arbitrary prediction centers, not merely on attainable tensor predictions. The upper metric bound follows by telescoping tensor products of bounded factors.

Taking products of scalar covers and expanding their cardinalities gives the capped allocation polynomial. Keeping each `p_e` is essential: replacing it by a total ambient-dimensional cap can allocate unavailable directions to one edge. The large-budget argument absorbs the constant term in the cover count; the small-budget argument uses `A_{F,1}=1` on a nonempty cut. Empty cuts are singletons. Thus the bound is not restricted to an asymptotic subsequence of label budgets.

The causal product construction is also legitimate. During a batch, new components start at their known priors, active components update in raw coordinates, and completed components are discarded. A reachable representative remains reachable after an admitted batch. Quantizing at the next boundary gives the printed recurrence with all preceding errors retained. There are finitely many batches and orders, so taking uniform constants over them is permitted.

This proposition is substantively the deterministic shared-memory development already present in v10, now specialized to graph-batch checkpoints. The manuscript credits that history correctly. It should not be counted again as an independent new theorem when assessing this revision's incremental contribution.

### 5.3 One regular box really does control every needed prefix

Source: `v25/adaptive_proof.tex`, `lem:v25-regular-box`.

The full-cap Jacobian has `p` rows and is surjective at the common interior command tuple. Completing its row space by orthonormal kernel coordinates gives a square map whose derivative has uniformly bounded norm and inverse norm. The quantitative inverse argument supplies a product box in output and complementary coordinates, with inverse inside the command cube. The determinant of that inverse has both a positive lower bound and a finite upper bound.

Integrating the complementary coordinates gives a density bounded above and below on the same full `p`-box. Integrating unwanted output coordinates and then scaling a positive prefix gives the density bound `C/D_{e,ell}`. This is an upper bound for the restricted command measure as well as a lower-mass construction. A mere lower minorization would not justify the later arbitrary measurable restriction step.

The use of the full formal cap at an exact collision is not a contradiction. Some additional unscaled divided-difference coordinates remain functions of the command history even when their physical prediction scales vanish. The converse subsequently uses only positive scaled prefixes. It never asks the prediction vector to recover a zero-scaled coordinate.

No latent-prior density has been differentiated. The chart is in actual command variables, and the retained lower-dimensional output distribution is obtained by integrating, not by assigning positive probability to a frozen command slice.

### 5.4 The common event retains report evidence

Source: `eq:v25-common-mass` and `eq:v25-restricted-density`.

The event requires every first command block to lie in its regular box and every report on the complete tape to be a failure. Completion commands are not fixed. The full report-word evidence is the product of the actual edge evidences and lies between `kappa^T` and one. Independence of command tapes and the positive box masses give a common probability at least `beta > 0`, independent of the scheduler and coding seed.

Using unrevealed tape entries to define a subevent in a proof does not supply those entries to the implemented controller. This coupling is legitimate because the commands are exogenous and vertex selection is nonanticipatory. The potential first-block coordinates are defined before the realized trace is selected; on the common event they equal the relevant active-edge posterior coordinates whenever that edge is active.

The upper density bound follows by change of variables in the first blocks, integration over complementary coordinates and completion commands, and the upper bound of one on the report evidence. Therefore, for every allowed cut allocation, the restricted subprobability satisfies `P(A, X in U) <= C vol(U)/D`.

Crucially, this estimate is established before intersecting with an adaptive trace event. Intersecting can only decrease its left-hand side. No assertion of independence under the conditional law given a selected trace is needed or made. The manuscript's argument addresses exactly the selection problem identified in its response.

### 5.5 Finite traces, arbitrary centers, and the order of quantifiers

Source: the proof of `thm:v25-adaptive` and `eq:v25-bottleneck-volume`.

Fix the independent coding seeds. For each complete vertex permutation choose a bottleneck boundary and an allocation achieving its profile. These choices depend on the permutation, calibration and budget, not on the particular tape within that trace class. The factorial comparison between determinant volumes and Newton products gives the required lower bound on `(D_pi/M)^(2/k_pi)` by a fixed multiple of the optimal graph profile.

At a fixed trace and boundary, the decoder has at most `M` prediction vectors, even when supplied the finite order prefix. The tensor recovery and leading nonzero Newton inverse apply to arbitrary centers with uniform bounds. Small loss therefore puts the selected scaled coordinates in a union of at most `M` balls. The restricted-density estimate bounds the probability of this event without conditioning on the trace.

A union over at most `v!` traces leaves positive mass on which some boundary loss exceeds a small multiple of the graph profile. This controls the expectation of the maximum loss. The manuscript then correctly passes through the sum of boundary losses and divides by `v-1` to obtain a lower bound for the maximum of the expected losses. It does not interchange those two operations. The constants are independent of the fixed seed, so the seeds can be integrated before the infimum over common controllers is taken.

Pre-sampling decoder randomness for each member of a finite query menu is legitimate. The tape law is independent of those seeds. Nothing in this step allows a history-correlated random seed to become uncharged persistent storage.

I found no central gap in this converse under the stated model. The proof's strength and its limitation are both visible: it tolerates arbitrary measurable trace classes, but the finite number of traces and the common event's probability enter its constants.

### 5.6 An explicit finite-selection reduction clarifies the contribution

The essential selection step can be isolated without the graph notation. Suppose a common event has mass at least `beta`, there are `K` possible traces, and each trace has a coordinate recovery with

`P(A, trace=pi, max_j L_j <= r^2) <= C_0 M r^{k_pi}/D_pi`,

where `1 <= k_pi <= P` and `(D_pi/M)^(2/k_pi) >= gamma Q`. Enlarging `C_0` to cover the finite choices, put `r=t sqrt(gamma Q)`, with

`t=min{1, beta/(2 K C_0)}`.

Each summand is at most `C_0 t^{k_pi} <= C_0 t`. Their sum is at most `beta/2`. Consequently

`max_j E L_j >= beta gamma t^2 Q / (2(v-1))`.

This is a derivation from the submitted proof, not an asserted sharp constant and not a proposed counterexample. It makes explicit why arbitrary measurable selection is harmless here once a common restricted-density estimate exists. It also makes explicit why this argument is not graph-size uniform. The common-event probability contains all block restrictions and all report evidences; the trace count can be factorial. No claim is made that such dependence is necessary or optimal.

## 6. The bit law and the star example

### 6.1 The logarithmic inversion is correct

Source: `v25/graph_consequences.tex`, `cor:v25-graph-bits`.

With `M=2^B`, the inequalities for a fixed cut are equivalent to

`B >= max_k { (k/2) log_2(1/epsilon) + log_2 A_{F,k} }`.

Including the feasible zero allocation lets the finite maximum separate exactly into the sum of edge bit profiles. Zero determinant factors contribute negative infinity at positive indices, while the zero-index contribution remains zero. This handles exact collisions without an artificial rounding of component memories.

Taking the maximum over cuts and then the minimum over orders gives the weighted cutwidth expression. The risk comparison constants replace the accuracy by fixed multiples; all affine profile slopes are bounded by the fixed sum of acquired caps divided by two. Thus the replacement changes the optimal bit profile by a bounded additive amount, and final integer rounding costs at most one more bit.

At a fixed calibration, the last positive index of the cut profile is the sum of the active acquired dimensions. The stated fixed-calibration exponent follows. Its comparison constants may depend on that fixed calibration; the full determinant-profile theorem is the statement that remains uniform across collisions. These are different claims, and the manuscript distinguishes them.

### 6.2 The two optimal star partitions really differ

Source: `cor:v25-star` and its proof.

The experiment uses 14, 8 and 2 raw trials on its three edges, respectively. The middle edge has nine positive formal three-fold sums and six limiting groups. Three groups contain pairs with separation proportional to `theta`. Hence the determinant contact orders for cardinalities one through nine are

`0, 0, 0, 0, 0, 0, 1, 2, 3`.

The stated positive detector cells and full-rank coefficient matrices supply an actual fixed experiment, not a formal list of independently adjustable scale parameters. With `L=log_2(1/epsilon)` and `U=log_2(1/theta)`, the leading bit profiles are

`b_1=(7/2)L+O(1)`, `b_2=max{3L,(9/2)L-3U}+O(1)`, and `b_3=L/2`.

Every vertex order of a three-edge star determines the partition of leaves before and after its center. Its maximum cut weight is the larger of the two partition sums. For the two resolutions the leading costs are as follows; all entries are coefficients of `U`.

| Partition type | Accuracy `theta` | Accuracy `theta^4` |
|---|---:|---:|
| Isolate edge 1 | 7/2 | 17 |
| Isolate edge 2 | 4 | 16 |
| Isolate edge 3 | 13/2 | 29 |
| Empty part | 7 | 31 |

Thus the respective optima are `7U/2+O(1)` and `16U+O(1)`. Every fixed order loses at least `U/2-O(1)` at one of the two accuracies. This remains true when the order depends on `theta`, provided it is the same at the two compared accuracies. Finiteness makes the additive remainders simultaneous across all orders.

The independent calculation checked all 24 orders and reproduced these leading optima and the minimum worst-penalty coefficient `1/2`. The calculation is not a numerical evaluation of the true optimal finite-budget risk; it checks the exact profile arithmetic used in the consequence.

This is a meaningful illustration of collision resolution changing the preferred observation order. It is not a theorem that every adaptive schedule has a positive penalty relative to every fixed schedule, nor a claim of exact integer transition thresholds. The adaptive theorem establishes comparability with the best order chosen separately for each accuracy and calibration.

## 7. Concrete corrections and presentational requests

### E25.1 — Incorrect graph reference: correction required

**Location:** `v25/references.tex`, bibliography key `AmarilliGroz2025`; invoked in `v25/graph_consequences.tex` near `eq:v25-weighted-width`.

The submitted entry attributes arXiv `2504.01574v2` to A. Amarilli, F. Groz and W. J. Tan under the title *Edge Minimum Linear Arrangement*. The actual primary-source record and article identify **Antoine Amarilli and Benoît Groz, *Cutwidth Bounds via Vertex Partitions***, version 2 dated 3 April 2025. There is no third author in that record. Both the title and author metadata need correction.

This is not an inconsequential spelling issue: cutwidth is a maximum crossing-load objective, whereas a sum of crossing loads corresponds to a different layout objective. The printed v25 definition uses the correct maximum. I found no reliance on a false graph theorem from the cited article; its role here is attribution for the parameter. Accordingly this is a definite citation defect, not a counterexample to the graph-risk theorem.

Correct the entry against the primary source [P1]. Do not introduce a stronger literature-priority claim while repairing it.

### E25.2 — The response cites a proof ledger not supplied at its relative location

**Location:** `RESPONSE_TO_REFEREE.md`, Section 4.

The response says that the listed obligations are recorded in `PROOF_LEDGER.md`. That file is absent from the v25 directory at the immutable submission: it is not in the directory listing or the additions, and a direct lookup of `papers/A1-english-v25/PROOF_LEDGER.md` returned not found. No alternative versioned path is supplied there.

Supply the intended ledger with an unambiguous path and theorem labels, or correct the response to point directly to the proofs actually present. The mathematical arguments themselves are in the TeX source; the missing auxiliary document is not evidence that those arguments are missing. The required repair is source traceability, not another layer of theorem assertions.

### E25.3 — Replace the nominal quantifier negative control with an actual witness

**Location:** `diagnostics.py`, `check_probability_and_quantifiers`.

The purported negative control for the expectation of a maximum versus the maximum of expectations tests only `Fraction(1) > Fraction(1,2)`. It does not construct losses or evaluate either operation. The ambient-cap negative control can also succeed merely because the output arrays have different lengths. These checks are too weak to support the descriptive names attached to them.

A useful quantifier witness is the equally likely pair of loss vectors `(1,0)` and `(0,1)`: the expectation of the maximum is one, while the maximum of the expectations is one half. The same two-by-two array, read as controllers versus checkpoints, gives `inf max = 1` and `max inf = 0`. A useful cap witness keeps the same total cap but moves one forbidden direction into the wrong component, changing an actual common-index coefficient. The independent diagnostics supplied with this report instantiate these calculations.

The proof itself uses the correct quantifiers, and the author does not claim the diagnostics formally prove it. This is therefore a low-severity validation improvement, not an unresolved theorem-level objection.

### Expository suggestion, not an additional acceptance condition

Isolating the finite-selection argument of Section 5.6 as a short abstract lemma would make the new contribution and its constants easier to evaluate. It would also prevent the reader from mistaking the finite-trace step for a graph-specific combinatorial theorem. The required argument is already present; this suggestion must not be recast as a demand for a new research result or as a guarantee of a changed editorial recommendation.

## 8. Why the significance judgment remains negative

The appropriate comparison is with the actual v24 scalar classification and the earlier shared-memory development, not with an imaginary manuscript containing only a Vandermonde determinant. The existing scalar theorem combines actual acquisition, complete confluent flags, a whole-image upper bound, arbitrary-center lower bounds, every integer budget and one causal filter. That conjunction is substantive and survives this reading.

The revision's incremental advance consists principally of the following: a simultaneous regular-box upper density estimate; a policy-independent positive-mass tape event; a converse robust under finitely many measurable history-dependent order choices; and an experiment-induced family of weighted layout problems. The star shows that the optimal layout changes with resolution. These additions deserve to be acknowledged as mathematical work rather than dismissed as stylistic changes.

My objection at the requested level is that the new mechanisms do not, in their present form, supply the depth or reach needed to change the earlier venue assessment. The regular-box strengthening records both sides of the same local change of variables. The selection step is the finite-union consequence displayed in Section 5.6 once that density estimate is available. The deterministic product geometry and additive bit profiles were already established in v10. The passage to cutwidth is the choice of which independent edge components remain live at a vertex boundary. The ordering transition is a sharp and useful application of the resulting weights, but its additional combinatorics is a three-item partition comparison.

This is not an argument that elementary consequences cannot be important. The question is what substantial further phenomenon is established here beyond the inherited collision classification. The submission demonstrates a robust finite-choice extension and a well-designed example. I do not see a correspondingly large new structural insight, a resolution of a recognized difficult problem, or a demonstrated consequence of exceptional reach. This is a judgment of the advance exhibited, not a bibliographic proof that no such consequence could ever follow.

The graph is fixed, and both the theorem and proof explicitly permit constants depending on its size, its block horizons, the common report event, the query menu and the finite traces. Thus the statement does not currently give a uniform adaptivity-gap theory over growing graphs or an algorithmic graph-width classification with controlled complexity. It would be inaccurate to market it as either. Conversely, those different theorems were not promised, and their absence is not a logical gap in the result that was promised.

A specialist could reasonably assign more weight to the collision-uniform conjunction. My recommendation is not a mathematical impossibility result, and it is not a reason to weaken a correct theorem, erase the companion or discard the program. It is also not a major-revision checklist in which a repaired reference and one more example force acceptance. I would preserve the valid theorem and its explicit scope rather than respond to the venue disagreement with inflated claims.

## 9. Targeted primary-source and historical comparisons

**[P1]** Antoine Amarilli and Benoît Groz, *Cutwidth Bounds via Vertex Partitions*, arXiv:2504.01574v2, 3 April 2025. The primary record and HTML article were inspected. Its definition minimizes the maximum number of crossing edges over vertex orders, with multiplicities for a multigraph. This supports the parameter identification and the correction in E25.1; it is not a source for the adaptive statistical theorem. Sources: [record](https://arxiv.org/abs/2504.01574v2), [article](https://arxiv.org/html/2504.01574v2).

**[P2]** Yifan Zhang and Joe Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4. The accessible primary HTML treatment of semialgebraic regularity, covering and classical variation methods was inspected. It supports the identification of established geometric inputs, not the experimental acquisition or causal claims. The specific anisotropic rectangle deduction was assessed from the proof supplied in A1; no unseen PDF theorem was treated as independently inspected. Source: [article](https://arxiv.org/html/2311.05116v4).

**[H1]** Qian Qi, *Sparse observation algebras: collision geometry and shared memory*, A1 English v10, immutable source `da5abea9f40244879115d5fbcfbda375bc9a123e`, Sections 8–9. Section 8 already states the unrestricted joint-label product classification. Section 9 gives additive bit profiles, serial/overlapping schedules and schedule-dependent exponents; its concluding paragraph explicitly excludes adaptive schedule selection. This establishes the repository-relative distinction between the inherited deterministic law and the new adaptive extension. Source: [historical manuscript](https://github.com/TrillionniumFoundation/theta-theory/tree/da5abea9f40244879115d5fbcfbda375bc9a123e/papers/A1-english-v10).

These were targeted checks, not an exhaustive priority search. In particular, this report does not assert that classical graph layout, nonlinear-filter quantization, or read-once branching-program results already prove the submitted adaptive theorem. No publication-priority conclusion follows from a finite literature check.

## 10. Executed independent diagnostics

The accompanying `independent_diagnostics.py` completed **4,789 explicit checks** using exact `fractions.Fraction` arithmetic. Ordinary Python and `python -O` produced byte-identical JSON output. Requirements raise exceptions rather than use optimizable `assert` statements. The executed script's SHA-256 is

`6ace6fb494b77f5514fb901e5d788255dff566e27ae215da0aa409f78923d252`.

`DIAGNOSTICS.json` records the categories and concrete witnesses. The suite includes 500 capped-profile factorization checks; 3,500 finite integer-budget inversion witnesses; exhaustive weighted-cutwidth comparisons on all 74 simple graphs with two, three or four labelled vertices; parallel-edge, isolated-vertex and empty-graph cases; all 24 vertex orders of the star; and 64 nonnegative star-weight partition comparisons.

It also checks the nine formal future labels, their exact subset contact orders, 36 Leja/volume comparisons including exact collisions, and 36 positivity-index checks. The probability tests evaluate a genuine positive binary-detector report law with a uniform latent prior: all 363 words through horizon five have their evidence retained, complete word masses sum to one, and the failure word is not assigned probability one. Those finite-law checks use fixed commands and do not simulate the theorem's full uniform-command experiment.

Restricted-subprobability examples include a disconnected selected set and exact interval intersections. The quantifier controls calculate the actual two-by-two loss witnesses, and the causal control retains preceding error terms. The cap control compares actual coefficients at the same total cap. These are intentionally small diagnostics of logical and algebraic steps, not numerical substitutes for the continuum converse.

The tests do not prove the common regular-box construction for arbitrary priors, the uniform small-ball estimate over all calibrations, the global covering theorem, or the true minimax optimizer. They do not certify source preservation beyond the separate repository comparison, successful LaTeX compilation, any GitHub Actions run, or correctness of all companion results. The author's tests and the prior referee's 13,903 checks were not included in this count or represented as fresh executions.

## 11. Final disposition

The added graph theorem has a coherent proof under its explicitly fixed-graph, independent-prior, exogenous-command, vertex-batch resource model. The common event, density restriction and finite-trace union correctly avoid the adaptive-conditioning trap. The bit law and two-resolution star consequence survive the present analytic reading and independent finite calculations. No fatal counterexample or unresolved central proof gap was found in the inspected principal route.

The definite corrections are E25.1–E25.3, with the first two being concrete source/publication repairs and the third a validation improvement. The previous architecture and early-example requests remain closed. No older resolved objection should be recycled as a new defect.

My recommendation at the requested four-journal level remains **reject**, for the significance reasons in Section 8. That negative recommendation should neither be softened into an acceptance prediction nor rewritten as a mathematical error the author has not made. The valid statements, complete proofs and explicit limitations should be preserved. Any subsequent revision and review should identify its genuinely new mathematical content against this pinned submission rather than restart the same cycle of attribution, packaging and test-count claims.
