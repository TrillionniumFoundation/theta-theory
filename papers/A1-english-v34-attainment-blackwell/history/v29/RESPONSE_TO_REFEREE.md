# Response to the independent report on A1 English v26

**Revised manuscript:** *Attainable information, exponent collisions, and adaptive memory*, Qian Qi, A1 English v29, 8 September 2026.  
**Controlling review:** `19fbf4fe0e7495afd537de73a63670a9cf5616e0`, report blob `a1419587213b25dfccab55476416db2b900a6cf0`.  
**Submission assessed by that report:** `a2e5d3737085241137211f1cf21393d5bcafa1ce` (v26).  
**Integration base:** `090f9875d71a7765d60838f737508f0b17bdc9da`, the published localized v28.  
**New branch:** `revision/a1-english-v29-occupation-flow-2026-09-08`.

We thank the referee for distinguishing proof correctness, quantitative content, and the editorial assessment of significance. The report found no fatal counterexample or unclosed central gap in the examined collision and graph proofs, but retained its negative recommendation at the requested journal level. We do not rewrite that recommendation as an acceptance prediction or as a false theorem that can be repaired by a test receipt. We retain the full positive theory and submit additional mathematical results for renewed assessment.

The present revision also completes an earlier unfinished line of work. An unpublished occupation-flow draft had been prepared under a v28 filename, while a different, localized v28 was actually published. We integrate the recovered draft under v29 labels, on the complete published v28 tree. No published v27 or v28 result is displaced, and no existing manuscript or review branch is overwritten. The recovered draft is prior work for this revision, not evidence of a previously completed GitHub publication.

## 1. What is new relative to the reviewed submission

The v27 policy-curve and evaluated-model results and the v28 localized growing-graph results are retained as intervening developments. They are not counted as new v29 theorems. The v29 contribution is an integrated variational treatment of the local acquisition bounds.

For a finite layered path model, suppose that the probability of the common event, a visit to vertex w, and loss at most t is bounded by beta times c_w(t). Write phi_w(x) = integral from 0 to 1 of [x - c_w(t)]_+ dt. Rather than choose a new separator independently at each threshold and then divide an expected maximum by the checkpoint count, we retain one conditional occupation flow through every threshold and checkpoint. Theorem `thm:v29-occupation` proves the lower bound beta Gamma, where Gamma is the minimum, over feasible unit occupation flows, of the maximum of the level sums of phi. Terminal capacities x_w <= c_w(1) are included; an infeasible capacity vector is not silently treated as a probability model.

Theorem `thm:v29-relaxation-exact` constructs a matching random-path loss model by flow decomposition and inverse distribution functions. Thus Gamma is exactly the sharp consequence of the specified local path inequalities. This is an exact result about the information carried by those inequalities, not a claim that every Bayes experiment or common finite-label decoder realizes the extremizing abstract losses.

The actual experiment contains more information: before the first vertex is selected, no tape entry has been observed. Theorem `thm:v29-pre` retains this restriction conditional on the independent seed and produces a larger perspective-flow value Gamma_pre. Conditional Jensen is applied separately at every fixed checkpoint, and the maximum is taken only after averaging the seed. Theorem `thm:v29-dual` gives an exact convex dual expressed using supporting costs and capacitated minimum-cost flows. Feasible dual values have the correct lower-bound direction; a nonoptimal feasible primal value does not certify a statistical lower bound.

The comparison is explicit: for the original decoder and the same capacities, the maximum-tape risk is at least the average risk, which is at least beta Gamma_pre, then beta Gamma, then the original separator integral divided by the checkpoint count. The old result is preserved and strictly strengthened, not weakened. On a chain with identical power capacities the occupation improvement is exactly the number of checkpoints. In the actual two-vertex experiment the pre-acquisition constraint gives a factor four over the unanchored relaxation with identical input constants.

## 2. Report Section 8.1: quantitative meaning and same-model evaluation

The report correctly observed that the v26 certificate was not shown to be a sharp statistical minimax formula, and that comparing event masses alone does not compare complete lower bounds. V27 had supplied the full acquired law and an evaluated separator bound. The new `v29/evaluated_refinement.tex` uses that same detector, command law, two-trial horizon, four equiprobable queries and decoder.

The full first-failure submeasure has mass beta = 1/2 and acquired-mean density bounded by H = 26. The arbitrary-centre recovery norm has square L^2 = 128. The pre-acquisition bound is beta^3/(12 L^2 H^2) times M^(-2), hence exactly M^(-2)/8306688 for every integer M >= 1. The accepted-report atoms are not silently removed from the statistical law: their nonnegative error is omitted only in this lower-bound calculation.

Keeping the previously used restricted command event, its mass 35/1024, its density bound 177957/20480, and the same recovery norm gives exactly four times the earlier separator certificate. Passing additionally to the known whole first-failure law gives the exact total ratio 1499109768/1071875, greater than 1398, relative to the earlier complete restricted-event separator bound. The response and manuscript identify these as two different improvements; the large ratio is not attributed merely to a larger event mass.

An additional completion-failure restriction scales the entire first-block subprobability density and its mass by one half, because the averaged completion failure likelihood is one half at every latent value. The capacity shape is therefore unchanged and the complete lower bound is exactly halved, to M^(-2)/16613376. This is a like-for-like quantitative comparison. It does not reveal a future completion report to the implemented predictor.

The retained exact reduction is R_av = D_M(nu)/128, with the full mixed acquired law nu. Its sharp high-resolution coefficient is (1/1536)(integral f^(1/3))^3. The ratio of that exact coefficient to 1/8306688 is rigorously enclosed between 4.05 and 4.06. This comparison is asymptotic in M; no finite-budget approximation ratio or equality with the maximum-tape risk is asserted.

## 3. Reports Sections 4, 7.3 and 8.4: decoder and resolution quantifiers

The principal introduction now contains a compact statement of the information conventions. Their implications are also collected here.

| Result | Decoder/query convention | What is uniform or shared |
|---|---|---|
| Inherited scalar and v25 qualitative graph profiles | The graph converse may allow the finite order prefix | Calibration and integer budget; fixed experiment and graph |
| v26 separator and v29 original-task flow certificates | Label plus visited-set query descriptor; no extra prefix unless explicitly counted | One controller; displayed event, density and recovery constants |
| v29 finite-descriptor extension | At most K_S extra descriptor values at S give at most M K_S centres | Cardinality costs remain in the capacities; no continuous history is free |
| v27 prediction-curve and policy-menu results | The stated scheduler/decoder relaxations are retained | Acquisition law or menu fixed across resolutions; predictors may be redesigned |
| v26 deterministic-order regret | A deterministic permutation is shared | Codebooks and predictors may be reoptimized at each resolution |
| v28 localized growing-graph theorem | Explicitly augmented local-and-tensor query menu | Graph size, calibration and small resolution under the printed graph hypotheses |

In particular, the graph-size-uniform theorem does not silently apply to the original tensor-only loss. Conversely, the original-task flow certificate does not acquire graph-uniform constants simply because it appears beside the localized theorem. At a fixed visited set, a full finite prefix has at most |S|! possibilities; equation `eq:v29-descriptor` counts them explicitly, or one may lift the finite path graph to prefix vertices. The exact two-trial comparison is valid under either decoder because the first prefix conveys only the already specified first vertex.

## 4. Report Sections 6–8: depth, scope and classical ingredients

The report judged the finite separator union bound, classical flow certificate and finite affine phase envelope insufficient to alter its venue assessment. We do not rename those ingredients as new mathematics. Their proofs and attribution remain intact. The occupation result addresses a different variational question: what is the strongest consequence of the local random-path distribution bounds when one path occupation law must serve every threshold and checkpoint? The exactness theorem answers that question, and the pre-acquisition theorem explains precisely which additional information strengthens the answer.

The convex minimax input is classical and is credited to R. T. Rockafellar, *Minimax theorems and conjugate saddle-functions*, Mathematica Scandinavica 14 (1964), 151–173. Its metadata were verified against the author-hosted original journal reprint, including the scanned cover. Supporting functions, flow decomposition and separation are not claimed as new methods in themselves. The claimed content is their proved application to the acquisition constraints, the exact local-information variational characterization, its seedwise refinement, and the fully evaluated statistical comparison. These are statements to be assessed mathematically, not an assertion of exhaustive literature priority.

The intervening v28 theorem supplies a graph-growth consequence while retaining explicit hypotheses and a precisely stated augmented task. The present revision preserves it in full, including its graph-existence proof, once-per-edge upper construction, and joint collision/growth corollary. It does not manufacture breadth by suppressing these hypotheses. The significance objection remains a matter for renewed independent assessment; neither another theorem label nor the finite check count decides it.

## 5. Previously closed corrections and source preservation

E25.1, E25.2 and E25.3 remain closed: the corrected Amarilli–Groz reference, the delivered proof ledger, and the actual quantifier/individual-cap controls are retained. The principal/companion separation and early scalar example are not reopened. The reviewed scalar acquisition, confluence, covering and causal proofs are not replaced by summaries, and no companion section is removed.

The new native directory starts from Git tree `e4d7c85782d0157ee606464ada62d82824aea7e6`. Its inherited mathematical subtrees and companion are copied as the same Git objects. `baseline-v28-main.tex`, `PROOF_LEDGER_V28.md`, and `RESPONSE_TO_REFEREE_V28.md` retain the immediately preceding entry point and records. The original scalar bridge proof keeps both the finite upper maximum and the positive lower minimum. The v10 scheduling derivation is retained as historical input, not re-attributed to this revision.

## 6. Execution and remaining review work

The new suite completed 11,345 explicit finite checks and a rational enclosure of the acquired-law integral. Normal Python and `python -O` produced byte-identical JSON. These checks include genuine expectation/max and infimum/max counterexamples, the infeasible terminal-capacity control, primal-versus-dual direction controls, seedwise Jensen, descriptor cardinalities, power integrals and full coefficient ratios. They do not prove the continuum inverse-chart theory or certify the full program.

The new proof component was compiled as a separate twelve-page document in three passes and visually inspected. It labels inherited references as source locators rather than inventing main-volume theorem numbers. It is not the full principal article. The complete native main and companion inputs and an offline two-volume builder are supplied, but no completed native two-volume build or successful GitHub Actions execution is asserted for this session. The builder records failure as failure and produces a full-build success flag only after both volumes actually complete their reference and layout checks.

The revision is submitted for renewed review of the new proofs, their statistical interpretation, the retained dependencies, and the resulting significance case. It is not approved or merged as a consequence of its construction or finite diagnostics.
