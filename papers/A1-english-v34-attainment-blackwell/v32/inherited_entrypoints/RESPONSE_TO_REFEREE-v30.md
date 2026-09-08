# Response to the independent A1 v29 referee report

Report: `reviews/a1-english-v29-harsh-independent-2026-09-08/REFEREE_REPORT.md` at `90c7acd0e4efe3280eb1a8faa3c6d9461870c36f`.
Reviewed article: `610233410ff6600e76167fad98a3f610faa6191b`.
Revised native entry points: `papers/A1-english-v30-multilevel/main.tex` and `companions.tex`.

We thank the referee for distinguishing mathematical validity, information-model scope, statistical reach, and editorial significance. The revision adds statistical realization theorems rather than treating exactness of a local-path relaxation as an answer to all four questions. It preserves the acquired-rank, confluent-mass, global-cover and raw causal-update proofs, together with the complete companion developments.

## E29.1: the optimized fixed-calibration menu excess

The sentence after `eq:v27-menu-functional` was incorrect. At every fixed finite graph and calibration, the optimized functional is finite, even if the accuracy set accumulates at zero.

**Correction and additional results.** `thm:v30-menu-finite` proves

\[
0\le r_K(\mathcal E,a)\le r_1((0,1],a)<\infty.
\]

It selects an order that is exactly optimal for all sufficiently large log inverse accuracies. The proof first stabilizes each finite edge maximum, then each cut maximum, and finally the minimum over finitely many orders. Every retained intercept is finite; zero determinant branches are omitted. A prescribed menu is bounded precisely when its minimum eventual slope is the global minimum slope. `prop:v30-critical-resolutions` gives an exact finite minimax formula on the entire half-line, and `cor:v30-stratum-uniform` states the positive-volume condition for calibration-uniform boundedness.

The incorrect sentence and the vacuous infinite-value contingency in `cor:v27-menu-regret` have been replaced. The paragraph preceding `cor:v25-star` now states the correct collision-uniform quantifier. All seven proof bodies in these two legacy files are byte-preserved. The actual star and analytic collision results are neither weakened nor removed: their excess can diverge as calibration approaches collision even though it is finite at each fixed calibration.

## The gap between abstract local-path exactness and statistical realization

The new article continues to distinguish `thm:v29-relaxation-exact` from an actual Bayes prediction optimum. The added results establish realization on an explicitly stated class instead of deleting that distinction.

**First, arbitrary regenerative blocks on committed routes.** `thm:v30-regenerative` handles arbitrary finite one-block query menus and acquired laws. At every integer budget its statistical risk is exactly

\[
\min_{\rho\in\Delta_R}\max_j\sum_r\rho_r d_{rj}(M)
=\max_{\lambda\in\Delta_J}\min_r\sum_j\lambda_j d_{rj}(M).
\]

The lower proof conditions on the tape-independent seed, counts the actual decoder centers, averages each checkpoint risk, and only then takes the maximum. The upper proof constructs one M-label causal reset controller. The equality is not obtained by independently selecting an incompatible encoder at every checkpoint.

**Second, predictable acquisition on arbitrary finite regenerative networks.** `thm:v30-predictable-exact` permits branching, recombination and history-dependent choices along arcs. It assumes that a vertex is chosen before its new block is revealed and that this block has its prescribed conditional law given the choice and the past. The exact statistical formula is

\[
\mathcal R_{\mathscr D,M}^{\rm reg}
=\min_{x\in\mathcal F}\max_j\sum_{w\in\mathscr V_j}x_wd_w(M)
=\max_{\lambda\in\Delta_J}\min_{P:o\rightsquigarrow d}
  \sum_{w\in P}\lambda_{j(w)}d_w(M).
\]

The converse allows the scheduler its entire revealed history. The attaining controller does not need that relaxation: a pre-acquisition seed selects at most J+1 deterministic paths, and each fresh block is quantized into the same label set. Conditioning just before every acquisition is the new structural input. `prop:v30-predictable-bound` explicitly proves why unconditional local capacities alone are insufficient to supply its linear occupation cost.

The decoder's finite vertex descriptor is public by definition, not hidden uncharged history. The manuscript separately gives the state cost when that descriptor must be retained. The theorem is not asserted for a correlated nonregenerative posterior or a scheduler inspecting the current block before choosing its vertex.

## A fully evaluated multilevel positive statistical family

At every visited vertex we use a fresh copy of the reviewed positive two-trial detector. The complete acquired law is

\[
\nu=(5/16)\delta_{8/15}+(3/16)\delta_{4/9}+f(z)\,dz,
\qquad \int f=1/2,\quad \|f\|_\infty=26.
\]

For a specified gain s, the second detector trial is executed, and its scored failure indicator is retained with independent probability s; otherwise the scored event is an independent fair coin. This is an explicit physical randomization of the readout. It changes neither the acquired law nor which histories are included. The squared query metric is s squared times scalar error divided by 128.

`thm:v30-positive-realization` and `cor:v30-network-gap` prove the exact all-budget identity

\[
\mathcal R_{\mathscr D,M}^{\rm reg}
= D_M(\nu)V_{\mathscr D}(s^2)/128.
\]

One network path law is optimal at every budget; codebooks can be redesigned at each budget. An actual run has 2J detector trials, not one trial with J labels attached.

### No exponentially small all-stage event

The capacities retain the entire mixed law:

\[
c_w(t)=\min\{1,1/2+(2HLM/s_w)\sqrt t\},
\qquad H=26,\quad L=8\sqrt2.
\]

The 1/2 term is the actual atom mass. The event is the whole probability space, with mass one, so there is no factor (1/2)^J from requiring every block to report failure. Exact integration gives

\[
\phi_w(x)=\frac{(x-1/2)_+^3}{3(2HLM/s_w)^2},
\qquad \phi_w(1)=s_w^2/(8306688M^2).
\]

The predictable certificate therefore has the same design factor as the true statistical risk. Their ratio is exactly `(8306688/128) M^2 D_M(nu)`, independent of the graph, horizon and positive gains. It is below 129 at every budget. Its limiting value is between 4.05 and 4.06, with a newly executed exact rational enclosure approximately `[4.057499747239961, 4.059550634480326]`. The interval calculation certifies this scalar enclosure, not every theorem in the article.

### Common-controller consistency matters at arbitrarily many checkpoints

In `cor:v30-checkpoint-gap`, R=J, diagonal gains are one and off-diagonal gains are 1/J. Uniform route probabilities and uniform checkpoint dual weights give matching optimizers:

\[
V=1/J+1/J^2-1/J^3.
\]

Separate checkpoint optimization would give design value 1/J squared. The ratio of the true common-controller optimum to that separate-checkpoint value is exactly J+1-1/J at every finite budget. This is an unbounded consistency penalty in actual positive experiments, not merely in freely assigned abstract path losses. On the same committed-route family, the unanchored atom-aware relaxation is zero whereas the pre-acquisition certificate is strictly positive. On general regenerative networks, conditioning before every acquisition gives the further predictable refinement.

## Growing graphs and the loss metric

The augmented local-and-tensor theorem is retained with its independence, retained balanced-cut, query-weight and size-uniformity hypotheses. The unified introduction explicitly states that sharing an exact future test space is not graph-size-uniform equivalence of weighted prediction losses. No augmented-task lower bound is presented as a tensor-only theorem. The new attenuated regenerative family is likewise not silently substituted into the original graph theorem. The original localized tensor certificate and all growing-graph proofs remain active.

## One article rather than six chronological introductions

`main.tex` now inputs one introduction, `v30/introduction.tex`. It introduces the scalar experiment and acquired determinant profile, states the inherited main classification through its original input, exhibits intersecting collisions, explains the proof mechanism, then develops graph reuse, occupation information and statistical realization in a single dependency order. All six historical introductions remain in the source tree. Main theorem statements and proof modules were not replaced by summaries. The companion is still a separate complete volume; its prior-uniform saturated-algebra result is not conflated with fixed-prior delayed monomial acquisition.

The abstract no longer uses a certificate-improvement ratio as a substitute for a structural contribution. Classical interpolation, covering, quantization, finite separation and shortest-path duality are attributed as such. The additions put the burden on explicit statistical laws, information timing, simultaneous realizability and a quantitative comparison with the true minimax value. We do not treat diagnostic counts or absence of found counterexamples as a measure of journal-level exceptionality.

## Reproducibility and verification scope

The new arithmetic suite `diagnostics_v30.py` was executed in ordinary and optimized Python modes. The outputs agree byte for byte. It uses rational arithmetic and integer cube-root enclosures, checks affine menu negative controls, primal/dual identities, atom-aware integration, fresh-block selection, and the multilevel family. There are 50,790 finite checks; the count is not a mathematical certificate.

The exact new TeX modules were built through `new-results.tex` in three pdflatex passes, yielding a ten-page proof packet with no unresolved references, duplicate labels or overfull boxes. Every rendered page was inspected. Background source locators are explicitly marked in that packet; it is not passed off as the full article.

`build_v30.py` and the current `build.py` provide a native two-volume procedure with active proof preservation, cross-volume label and bibliography audits, legacy and new diagnostics, alternating label-only exports, and final-log checks. It writes failures as well as successes to `BUILD_RECORD_V30.json`. A proof-packet build is not a native two-volume build, and an unexecuted native procedure is not a successful build. The actual status is recorded separately in `SESSION_VALIDATION_V30.json` and, when executed, the workflow/build records.

The original reviewed directory and review branch remain unchanged. This revision is submitted for independent examination of the new statements and their stated hypotheses; it does not purport to certify its own mathematical correctness or a journal's editorial judgment.
