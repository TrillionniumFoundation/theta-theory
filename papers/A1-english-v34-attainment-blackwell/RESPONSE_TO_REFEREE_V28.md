# Response to the independent report on A1 v26

**Controlling report:** `reviews/a1-english-v26-harsh-independent-2026-09-07/REFEREE_REPORT.md`, review commit `19fbf4fe0e7495afd537de73a63670a9cf5616e0`, report blob `a1419587213b25dfccab55476416db2b900a6cf0`.

**Reviewed submission:** `a2e5d3737085241137211f1cf21393d5bcafa1ce`.

**Present revision:** A1 v28, `revision/a1-english-v28-localized-acquisition-2026-09-08`.

**Additional inherited revision:** v27, pinned at `49dd2eddb09017c91eede14358cb873fe666f3cf`. Its whole-curve theorem, policy-menu theorem and evaluated scalar model were already in the repository when this revision was prepared. They are retained and credited as v27 contributions, not counted as new v28 results.

## 1. The recommendation and the mathematical response

We thank the referee for distinguishing mathematical validity from the editorial assessment of significance. The report found no fatal counterexample or unclosed central proof gap in the principal arguments examined, but recommended rejection at the requested journal level. We do not recast that recommendation as a list of already repaired errors. E25.1–E25.3 remain closed, and the existing scalar, graph, separator and phase results are not weakened.

The new mathematical question is whether the acquired-information mechanism can give a memory law whose constants remain controlled when the number of experiments increases. The all-edge regularity event and the tensor recovery norm are distinct impediments to such a conclusion. The revision addresses them separately rather than assuming that fewer trace indices solve both.

First, Theorem `thm:v28-localized` uses an event requiring a regular acquired witness on every cut of one compulsory level. Only edges belonging to the selected witness enter its subprobability density. It applies to the original tensor task with its actual recovery norms, and has an explicit provision for finite decoder side information. It bounds the expected loss at one fixed boundary directly, without a factor obtained by passing from an expected maximum to a maximum of expectations.

Second, Theorem `thm:v28-size-uniform` concerns an explicitly augmented, executable query menu. Half its queries retain the original full tensor experiment; half read a uniformly selected edge. Both use the same future test space, and all remaining raw trials are executed. For independent copies of a fixed scalar experiment on linear-size graphs with sufficiently strong balanced cuts, the theorem proves

`r_0 b(epsilon,a) - C_- v <= B_G^{diamond,av} <= B_G^{diamond,max} <= cw(G) [b(epsilon,a)+C_+]`,

with `r_0=floor(beta_0 h v/2)` and constants independent of graph size and calibration. In particular, at sufficiently small resolutions both optimal bit requirements have order `v b(epsilon,a)`, uniformly through additive exponent collisions. This is a statement over an increasing family of experiments, not a reinterpretation of a fixed-graph comparison constant.

Proposition `prop:v28-graph-existence` proves that the required graph families exist at every even size. Corollary `cor:v28-joint-limit` then permits graph size to increase at an arbitrary rate while calibration approaches an analytic collision path. We present these results as a mathematical basis for renewed consideration, not as a proof that the editorial recommendation has been reversed.

## 2. Section 8.1: a quantitative certificate is not an exact minimax constant

We retain that distinction. The v26 separator integral is not relabelled an equality, and the new localized integral is also a lower certificate rather than a general sharp distortion constant. For equal-dimensional witnesses its integral is evaluated exactly as

`[k/(k+2)] rho^{1+2/k} (A M)^{-2/k}`.

The factor in front is the exact integral of the stated tail envelope, not the exact constant of the underlying statistical optimum.

The lower bound now starts from selected-edge measures, not the event that every edge is regular. For a witness with edge set F, every edge outside F is integrated over its full law and contributes one. The acquired-event evidence on F is retained. The proof never conditions the coordinate density on an adaptively selected visited set. Thus the loss of the all-edge probability product is not concealed in a conditional-density assumption.

The code-centre count is equally explicit. At a visited set S, a single finite side value determined before the independent query, with at most J_S possible values, gives at most M J_S prediction vectors. The original visited-set decoder has J_S=1. Giving the entire order prefix can cost as much as j! at level j; this cost is not omitted in the new general statement. The size-uniform specialization uses the visited-set decoder, not the stronger prefix oracle.

### Complete same-model numerical evidence

The requested fully evaluated example was supplied by the existing v27 and remains active in `v27/evaluated_model.tex`. It computes the full mixed law of the acquired posterior mean, its exact scalar quantization reduction, and its sharp high-resolution average-distortion coefficient. Separately, it evaluates the first-block mass, the evidence-weighted coordinate density and the query recovery norm for the separator certificate. Under the same decoder, requiring the extra completion failure halves both the event mass and its density; the normalized capacity is unchanged and the complete certificate is halved. This is not merely a comparison of two event probabilities.

We have not counted this worked example as a fresh v28 discovery. Nor do we compare the two-vertex separator constant to the new growing-graph theorem as though their statistical models or objectives were identical.

## 3. Section 8.1: growing graphs and the query-recovery cost

The revised proof accounts for the two growth-sensitive quantities separately.

For the acquisition event, if every balanced cut has at least h v edges and each independent first block is regular with probability at least beta_0, Lemma `lem:v28-retention` gives

`P(E) >= 1 - exp[-(beta_0 h/8 - log 2)v]`.

The strict condition `beta_0 h/8 > log 2` is printed in the main theorem. It ensures that enough regular coordinates occur on every candidate balanced cut before any scheduler selects one. The graph construction proves that this is a nonempty class; it does not assert the condition for every sparse graph or every bounded-degree family.

For readout, we do not pretend that a full tensor inverse has a graph-independent norm. The augmented menu gives recovery of selected edge coordinates with norm at most `sqrt(2P) L_ell`, where P is the number of edges. The lower bound keeps the dimension-dependent ball volume `omega_k <= (2 pi e/k)^{k/2}`. Since the acquired witness dimension is proportional to v and P is at most d v, the apparent recovery loss contributes only a controlled additive O(v) term to the bit bound. Equation `eq:v28-finite-size-bits` gives the complete finite-size inequality, including the factor 16 from query mixture, Markov threshold and Gaussian normalization.

The upper construction likewise avoids a growing-horizon constant. An edge is quantized once when first acquired, its index is kept unchanged while it is active, and it is discarded on completion. Independent edges do not require mutual posterior updates. The proof separately bounds the retained tensor component by a geometric damping estimate and the local component by its actual average. Consequently it does not prove only the easier local half of the enlarged task.

This gives a uniform order-of-memory theorem, not an exact cutwidth coefficient or a universal sharp adaptivity constant. The mathematical advance claimed is the controlled increasing-experiment regime and its collision uniformity.

## 4. Sections 7.3 and 8.2: phases and the fixed-rule quantifier

The v26 four-phase star and interval-regret calculation are unchanged. Their leading envelope is not treated as an exact finite-calibration switching rule. Their fixed-order conclusion still shares only the order across resolutions; the predictive codebooks may be redesigned.

The inherited v27 strengthens this particular quantifier by fixing the entire acquisition law across resolutions. Its heavy trace is selected before the predictive budget and codebook, giving simultaneous deterministic domination and deterministic completeness of finite policy menus. A program reading a budget-dependent compressed state does not automatically have such a fixed acquisition law. We retain that explicit distinction.

The new size-uniform theorem is different: its acquisition rule may depend on the requested resolution. Its proof applies separately to every such controller with constants uniform in resolution, calibration and graph size. It does not borrow the fixed-rule conclusion to justify a larger policy class.

## 5. Sections 8.3–8.4: scope, exposition and preservation

A compact decoder-and-uniformity table is now active in `v28/introduction.tex`. It contrasts the qualitative graph law, the quantitative separator certificate, the whole-curve result, the localized bound with finite side information, and the size-uniform theorem. The augmented query menu is identified in the abstract, introduction, theorem and proof; it is never silently substituted for the original tensor loss.

The original tensor probes remain with probability one half. The enlarged task also controls their original loss within a factor two. All raw trials, including those after a nonfailure and those on edges not selected by a local query, are still executed and counted. No uncharged continuous tape, history-correlated seed, or separate persistent edge memories have been introduced. The stored tuple of active indices is one joint label under the existing atomic-batch convention.

The native v28 directory contains the complete inherited v26 tree, the complete v27 mathematical subdirectory, the new v28 modules and the unchanged companion manuscript. All inherited mathematical module trees are copied by their Git object identities. The principal entry point uses the reviewed v26 proof connecting checkpoint bounds to the main theorem, including both the finite maximum and the positive minimum of constants. Both earlier entry points are retained as baseline files. The original v26, v27 and review directories in the repository are unchanged.

The historical derivation route consulted includes the original v10 scheduling argument at `da5abea9f40244879115d5fbcfbda375bc9a123e`, Section 9; the retained scalar whole-image and raw-moment causal arguments; the v25 product, regular-box and adaptive-selection proofs; the v26 first-block certificate; and the v27 whole-curve, menu and evaluated-model developments. The v10 argument already explains why completed independent blocks can be discarded. The new upper construction uses that operational fact but replaces graph-length requantization by one quantization per active edge. This reading is not represented as a fresh exhaustive audit of every historical file or all eleven planned papers.

## 6. Verification and remaining review work

`diagnostics_v28.py` executed 6,600 explicit finite checks. Normal Python and `python -O` produced byte-identical JSON. The checks include exact retained-edge probabilities over all labelled simple graphs on two through four vertices, parallel-edge and isolated-cut cases, selected-edge marginalization, nonconstant data-selected paths and losses, tail integrals, dimension normalization, collision-budget shifts and the tensor part of the upper bound. Tests use explicit exceptions, not removable assertions. These are finite diagnostics, not proofs of the general continuum theorems.

The new mathematical modules were compiled as a nine-page validation extract and visually inspected. That extract uses explicit external locators for inherited results and is not a substitute for the complete principal article or companion. No fresh native two-volume compilation is claimed in the session record. An attempted GitHub Actions source-export run failed before returning step logs; its cause was not established by the available response. The native builder records actual source, diagnostic and TeX outcomes in a separate build directory and does not mark an unavailable or failed build as a pass.

The significance objection remains a matter for independent reassessment of the added mathematics. We ask that the localized acquired-event theorem, the size-uniform two-sided bit law, the explicit nonempty graph families and the simultaneous graph/collision regime be assessed on their proofs and consequences, while preserving the credit and scope of the previously established results.
