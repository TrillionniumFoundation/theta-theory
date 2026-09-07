# Response to the v24 referee report

## Source and scope of this revision

This response addresses the report in `reviews/a1-english-v24-harsh-independent-2026-09-07/REFEREE_REPORT.md` at commit `c7fee8b92fd779573bd3b9ccdf5e37183c5cefa6`, assessing the v24 submission at `6f648bc3da0543e8361b4053ae7da33cb172f597`. It is not a response to an earlier review selected in place of that report.

The report distinguishes mathematical correctness from the significance required by the proposed journals. It does not identify a counterexample to the principal classification, and it closes the earlier architecture and early-example items. We have not treated its negative venue recommendation as a reason to weaken a correct theorem, suppress hypotheses, delete proofs, or declare the research direction impossible. Nor do we claim that changing the title, adding tests, or rearranging the manuscript establishes journal significance.

The revision retains the complete scalar classification and companion and submits an additional structural theorem for review: a calibration-uniform classification of shared memory under adaptive vertex-batch scheduling, in terms of a resolution-dependent graph width. The new theorem and its proofs are mathematical additions, not claims that the original referee has already approved them.

## 1. E23.1 as assessed in v24: structural significance

The reviewed collision theorem determined optimal compression for a prescribed scalar experiment and horizon. The added graph experiment lets the observation order itself depend measurably on the observed data. Independent edge experiments have acquisition and completion blocks; a visited vertex releases the corresponding incident blocks. The controller and scheduler share one finite persistent label.

At an active cut, edge determinant profiles compose with their individual acquired caps retained. Taking the maximum over cuts of an order, then the minimum over orders, defines `Q_G(M,a)`. Theorem `thm:v25-adaptive` proves

`c Q_G(M,a) <= R_G,M^av(a) <= R_G,M^max(a) <= C Q_G(M,a)`

for every integer budget and every calibration in the fixed chambers, including exact collisions. One deterministic order and one causal joint-label filter attain the upper bound. The converse permits arbitrary measurable history-dependent scheduling, and even grants the scheduler its full revealed past and the decoder the finite order prefix. Constants do not depend on the policy, calibration or memory budget.

The new step is not the deterministic product law. That law was already developed in Sections 8–9 of the shared-memory v10 manuscript at `da5abea9f40244879115d5fbcfbda375bc9a123e`. It is explicitly credited and proved in the form needed here in Proposition `prop:v25-fixed-order`. Treating it alone as a new contribution would misstate the repository's history.

The adaptive lower bound cannot be obtained by conditioning on the order selected from a history and then reusing a product-history minorization. The selected history sets need not have any regularity, and the conditioned law need not factor. Section `sec:v25-adaptive-proof` instead uses the following argument.

First, the complete acquired flag gives one regular inverse chart with two-sided Jacobian bounds. The same chart controls every positive scaled prefix. Second, a single event in the complete command/report tape puts every acquisition block in its regular box and retains the actual probability of every report in a full failure word. This event has positive mass uniformly over policies. Third, its restricted subprobability measure satisfies a small-ball upper bound for every cut and prefix allocation, before any adaptive trace is selected. Finally, a union over the finitely many vertex traces gives a lower bound for the sum of boundary losses. Integrating coding seeds and then comparing the sum with the maximum of expectations preserves the required quantifier order.

The bound is therefore about adaptive observation order, not merely tensor notation for a fixed product experiment. It gives two concrete consequences. Corollary `cor:v25-graph-bits` identifies the optimal persistent bits with the cutwidth of accuracy-dependent edge weights, up to a calibration-uniform additive constant. Corollary `cor:v25-star` constructs a fixed three-edge, 24-raw-trial experiment in which the optimal cut partition changes between accuracies theta and theta^4. Every single order loses at least one-half log2(1/theta) minus a fixed constant at one of those resolutions. The effect is caused by unresolved collision directions, not by a change in the graph or a free change in the available experiment.

These are the proposed grounds for renewed assessment of structural reach. We do not assert that they mechanically determine a favorable significance verdict or establish priority over every possible related formulation.

## 2. E23.2: retain the closed main/companion architecture

The direct proof of the scalar classification remains in the principal manuscript, with the original experiment, operational model, risk definitions, exact information, transversality, analytic inputs, acquired flags, whole-image compression, causal realization and collision consequences all retained. The separate companion is retained in full. Its source is not replaced by a summary or removed from the branch.

The new graph theorem uses the scalar acquisition, covering and raw-update results already proved on the principal route. Its regular-box argument and adaptive converse are supplied in the new principal sections. It does not send an essential new proof obligation to an unproved companion assertion.

The source layout shares unchanged v24 files explicitly rather than copying hundreds of identical files into a second native tree. The v25 builder materializes a full working source tree and both volumes in an isolated directory. It checks all inherited v24 statement, proof, definition and remark blocks with their multiplicities and checks preservation of inherited labels. The original v24 directory and review directory are not build outputs and are never rewritten by that builder.

## 3. E23.3: retain the closed early-example item

The earlier two-parameter intersecting-collision example and its six-, eight- and nine-dimensional regimes remain in the original introduction and full scalar consequences section. They are not replaced by the graph example.

The three-edge example is additional and serves a different purpose: it demonstrates a change of the optimal observation order with the required accuracy. Its proof gives the detector cells, fixed horizons, all nine formal positive future sums, the six collision groups, the determinant contact orders, the edge bit profiles and the comparison of every star cut partition. Its raw-trial count is explicitly 14 + 8 + 2 = 24.

## 4. Preserve the earlier resolved mathematical obligations

No resolved E22 item is reopened by weakening the statement. In particular, the original actual-command tangent construction, complete acquired prefixes, full-support-prior positivity, arbitrary-centre lower bounds, whole-image dimension truncation, all-integer-budget estimates and raw-moment causal updates remain available on their original proof route.

The extension has analogous explicit obligations. Its lower-bound event retains full word evidence rather than conditioning failures to probability one. The product cover retains each edge's acquired cap rather than replacing them by an ambient total cap. Decoder recovery maps act on arbitrary prediction centres. The update recurrence retains errors accumulated at previous batches. Coding randomness is averaged before the maximum-tape supremum. The infimum over one controller is outside the maximum over boundaries. These points are recorded in `PROOF_LEDGER.md` and proved at the indicated labels.

## 5. Exact resource and uniformity statements

The new graph result charges persistent memory at vertex-batch boundaries. It does not claim the same width when memory is charged after every constituent raw report. This is a defined new experiment, not a silent reinterpretation of the retained scalar experiment. All raw trials inside the batches and the selected future query are still counted.

Commands are exogenous and revealed after vertex selection. The controller cannot choose command values, look ahead, or keep a continuous history outside its label. The analysis uses a pre-sampled tape as a coupling of actual exploration laws; the operational controller never sees unrevealed tape entries. Independent edge priors and fixed finite graph/horizons are substantive hypotheses. Constants may depend on these fixed data. There is no graph-size-uniform, correlated-prior, efficient-layout-algorithm, or raw-internal-checkpoint claim hidden in the theorem.

Stating these hypotheses is necessary to make the additional theorem precise. It does not remove or narrow any claim of the reviewed scalar theorem.

## 6. Validation and the next mathematical review

The revision includes an isolated two-volume build procedure, explicit preservation checks, and standard-library diagnostics for capped max-product profiles, graph cutwidth, collision orders, normalized-volume examples and several conditioning/quantifier negative controls. The diagnostic requirements remain active under Python -O.

A fresh successful build or diagnostic run must be established by its own source-hashed output. The earlier referee's checks, earlier PDF page counts and older CI outcomes are not relabelled as v25 validation. Compilation and finite diagnostics are not substitutes for the proofs, an independent audit of the adaptive converse, or a judgement of journal significance.

The principal new proof to review is the policy-uniform restricted-density and finite-trace argument, followed by the resolution-dependent graph-width inversion and ordering transition. The retained scalar classification remains available unchanged for comparison.
