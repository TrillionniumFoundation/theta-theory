# General Theta Foundations I — Revision 90: response to R59

**Date:** 6 October 2026. **Objective:** the four leading general mathematics journals; unchanged.

**Controlling external report:** `a7d030d635a2bb40c8b4f7f2265df877bad95492`, blob `b95c190a89823651c656e1d47a6e7e5ffaf5a2ee`.
**Controlling proof/pipeline audit:** `994c41dbeec1da13b6b6486876855fa30ad7cfd5`, blob `10c0f8bca52d016ae6fed65b9b7ef8d594a6ac86`.
**Reviewed predecessor:** `df7ed618813224b058b97c6cbda720ad936e2c53`, qualified native source `89773eff80ca81718641ec72d5efb9e20e03559a`.
Both R59 documents are frozen verbatim beside this response. Their recommendations have not been altered or redescribed as approval.

## Principal mathematical response

The referee correctly distinguishes an NPT tester from an operational advantage. Revision 90 supplies an exact finite-ensemble result with a matching upper for the *entire* unit-reset class, including arbitrary receiver instruments, classical feedback, and unrestricted retained receiver dimension.

For every dimension `d>=2`, choose a finite weighted family of ordered bases with simultaneous Haar second moments. The new lemma proves existence with at most `d^6+1` bases. Let `C_y=I/d` and `E_y^b(t)=(1-t)I/d+t P_y^b`, where `0<=t<=1`. The device is selected once and reused twice; the decision is scalar measurement versus the basis family, not identification of every basis. Put `L=2(d+1)-t^2`, with prior probabilities `(d+1-t^2)/L` and `(d+1)/L`.

Theorem `thm:operationalhierarchy90` proves exactly

```
P_ca    = (d+1)/L,
P_reset = (d+1)/L + t^2(d-1)/(2dL),
P_all   = (d+1+t^2)/L.
```

Both inequalities are strict for `t>0`. They hold on the full-rank interval `0<t<1`, not only on a rank-deficient example. In dimension two, the scalar device with prior `2/5` and the six ordered Pauli devices with priors `1/10` give `3/5 < 13/20 < 4/5`.

The core upper-bound tool is the exact negative-mass identity for a filtered swap, Lemma `lem:swapfilter90`. It controls each instrument-conditioned receiver branch without a separable-effect assumption. Independent maximally entangled pairs attain the reset optimum; a two-input antisymmetric state attains the unrestricted optimum. The classical upper is proved by positive-product contraction, while the unrestricted upper uses full causal tester normalization. Corollary `cor:robustgame90` gives an explicit stability margin. Proposition `prop:budgetdomain90` also extends the existing budget theorem to arbitrary real hard thresholds by exact integer normalization.

This directly answers the ensemble alternative in R03. It does not claim a separation for every pair of fixed channels or a complete memory-dimension classification. It strengthens the same ordered-measurement topic rather than replacing it. The fixed-tube profile and hard-budget theorems, their unknown-remainder controls, and all earlier mathematical sections remain available and active in the linked proof package.

## Point-by-point required revisions

| Request | Revision and location | Status |
|---|---|---|
| R01 Zonnios–Binder | `editions/memory-comparison90.tex`: Proposition 2, Theorem 1 and Corollary 1 are compared by object, autonomy, memory dimension, reset cut and hard quadratic budget. | Addressed |
| R02 tester normalization | In the proof of `prop:memorycomparison89`: full-transposed unnormalized Choi representative; ordered factors; exact two-pair contraction; factor `1/4`; positive complement; both causal trace constraints; closed separable cone; precise partial transpose. | Addressed |
| R03 operator inclusion versus scores | Old proposition retains its qualification. New Section 82 proves the finite ensemble hierarchy and the smaller-class uppers, including all unit-reset feedback. | Strengthened by a new theorem |
| R04 independent specialist priority | A targeted independent-review brief identifies the exact new claim and its antecedents. No independent human opinion has been obtained in this revision; the clearance flag remains false. | External review remains required |
| R05 complete reset cut | Definitions 79–80, new introduction, abstract and reset upper all require the whole fresh probe/reference/within-block memory to be independent of the entire old receiver conditional on history. | Preserved |
| R06 hard resources | `N_pi,Q_pi` remain formal path suprema. New threshold normalization explicitly distinguishes expected cost and fractional duration. | Preserved and clarified |
| R07 finite remainder | The `sqrt(rN)` contribution and every `m_r kappa s^2` lower error are unchanged in active proofs. | Preserved |
| R08 individual versus class | `D(pi;E,F)` remains policy-specific. Class notation denotes suprema. New budget proposition notes that spending a large budget does not force information retention. | Preserved |
| R09 fixed-object dependence | Abstract, introduction and the local theorems keep their fixed-tube quantifiers. The new exact ensemble family is separately defined and is not presented as a global measurement-body metric. | Addressed |
| R10 relative reset error | `prop:approxreset89` now states the symmetric bound and sufficient `epsilon<=c omega/4`, hence `epsilon=o(omega)`; `cor:robustgame90` gives the explicit score-gap threshold. | Addressed |
| R11 memory terminology | Acquisition width, `V/N`, hard `Q`, receiver storage, and coherent ancillary dimension are kept distinct. | Addressed |
| R12 journal narrative | Introduction shortened from 411 to 157 source lines. Main proof ends with the exact operational hierarchy. Sections 65, 66, 68 and 71 move, unaltered, to the current linked supplement. All their labels and proofs remain active. | Addressed without deleting mathematics |
| R13 executable scope | New checks and status explicitly deny continuum proof by replay, physical reset calibration, arbitrary-pair separation and independent priority certification. | Preserved |
| R14 API provenance | Source qualification, artifact-only publication and metadata-only final-head request are separated. Read-only final execution must be observed; a configured workflow is not evidence. Actions checks are not called legacy commit statuses. | Enforced by release procedure |
| R15 wider pipeline | The historical A2 replacement, B4, C2, eleven-paper and whole-program flags remain false. | Preserved |

## Detailed comments D01–D30

| Comments | Treatment |
|---|---|
| D01 complete acquisition group | Used throughout the new introduction and theorem statements. |
| D02 unhalved distance | Explicit in abstract/interface and unchanged norm estimates; probability perturbations use half the unhalved trace norm. |
| D03 zero padding | Section 80 records deterministic terminal symbols; positive reservations remain charged; zero-length symbols are not profile components. |
| D04 retained public mixture label | Existing direct-sum convention retained; the new reset normal form also retains the seed. |
| D05–D06 common rules and null histories | No equality of conditional old states is assumed; preparations remain defined on every formal history. |
| D07 integer `N<=V` | New threshold proposition proves the pathwise integer inequalities and does not extend them to fractional durations. |
| D08 Bures notation | New introduction explains root fidelity, state Bures notation, and distinct bound coefficients. |
| D09 nonoptimal old constants | No sharpness is assigned to the unequal-signal constants; exactness is claimed only for the separately proved finite game. |
| D10–D11 phase and floors | The positive-real-part, total-phase and two clipping regimes are unchanged. |
| D12 readout dependence | Repeated immediately in the unequal-signal lemma: only `E,H,Lambda,s,profile`, not the actual remainder or biases. |
| D13–D14 ideal controls and reference size | Inherited known-direction control and per-used-call reference bounds remain unchanged. |
| D15 effective width | Explicitly not an integer or memory dimension. |
| D16 coarsening | The independent-allocation inclusion remains separate from the reset rate comparison. |
| D17–D18 compressed costs and exact `Q` | Arithmetic witness is not a circuit; `Q/4<=V<=Q` remains the precise packing claim. |
| D19–D20 diamond norm and cap | Auxiliary references are included; inherited per-node cap remains; score stability uses the same norm. |
| D21 complex transpose | The full Choi contraction is written before the old Bell effect; it is valid for complex effects, not just the real Bell matrix. |
| D22 PPT | Necessary only. Closedness is proved via the compact trace-one separable slice. |
| D23 classical outputs | Neither the Bell witness nor the new game uses residual device output; references are experimenter supplied. |
| D24 Lüders instruments | Direct interface comparison with Eid–Quintino, including corrected author name and versioned reference. |
| D25–D26 receipts and proof | Source/publication archives contain manuscripts; final receipt certifies reconstruction, not originality or correctness. |
| D27 signatures | Automated/native commits are not human-authorship signatures. |
| D28 structural article | Its active source graph remains byte-identical and independent. |
| D29 complete archive | Preserved as one historical research edition, not an additional journal submission. |
| D30 aggregate flags | All five independent analytic closure flags remain false. |

## Audit gates and risk register

The R59 mathematical gates M01–M10 remain enforced by the unchanged load-bearing proofs and the registered convention insertions. M11 is answered inside the witness proof. M12 continues to apply to the local theorem; the new exact values apply only to the explicitly specified finite game. Priority gates P01–P04 and P06 are addressed; P05 remains an external human-review requirement. Editorial gates E01–E06 are addressed by the focused primary, linked supplement and separate operator/score statements. Reproducibility gates R01–R08 require fresh source execution and a genuinely observed final-head receipt. Pipeline gates A01–A05 remain independent.

Risks K01–K12 and K14 remain controlled by the retained definitions and estimates. K13 is answered positively by an actual optimal-score theorem, without promoting the old witness alone. K15–K16 are addressed by the new comparisons. K17 and K20–K25 retain explicit scope restrictions. K18–K19 are tested by the release procedure and reported using exact Actions/API semantics, not assumed from workflow configuration.

## Preservation and proof provenance

`V89_BASELINE.json` records all 710 predecessor native files and the active source graphs. All original files remain either unchanged at their original relative paths or additionally frozen byte-for-byte under `predecessor-v89-audit/`. The only old mathematical section edits are additive convention/proof paragraphs in Sections 79–81, enumerated in `EDITORIAL_INSERTIONS_V90.json`; removing those registered additions exactly reproduces the predecessor section hashes. No original proof paragraph is removed.

All 998 predecessor complete-edition labels remain active. The predecessor primary and current supplement are checked jointly, and every relocated label must remain available. The independent structural source graph is unchanged. The old 28 finite regression suites are rerun normally and with `python -O`, together with two new suites. The written all-dimension proof, not those finite checks, supports the new theorem.

## Significance and remaining independent questions

We have responded to the principal significance objection by proving more mathematics: an exact, all-dimension, noise-dependent operational hierarchy for the same classical-output interface, rather than relabelling the prior set inclusion. The objective and paper topic are unchanged. The old referee's venue judgment is left intact for the next referee to reconsider against the new result.

No arbitrary-pair global midpoint equivalence, full-boundary entropy theorem, growing-outcome minimax theorem, unrestricted higher-order classification, general efficient recovery synthesis, or whole-program analytic closure is inferred. Independent human assessment of the novelty and breadth of the new exact hierarchy remains necessary. These are precise boundaries of the established results, not replacements for the requested positive revision.


## Completion of the unpublished v90 response

The completion retains the exact staged Section 82 under `staged-v90-audit/` and strengthens the written argument rather than reusing the failed publication as evidence. Lemma `lem:swapfilter90` now proves that its nonzero equality cases are exactly scalar positive factors; the reset proof explains the resulting branchwise isotropy in its purified normal form. The arbitrary-adaptive upper constructs its positive tester blocks, positive complements and causal marginals directly from the initial purification and intervening trace-preserving maps. The first-moment identity explicitly distinguishes a once-selected alternative device from independently redrawn alternatives. The exact finite suite checks the added identities and equality counterexamples under both Python modes.

The current README and release account supersede inherited v89 headings without erasing the original records. The controlling R59 report and full pipeline audit remain byte-identical. Contemporary literature was checked again against the original arXiv texts (Zonnios–Binder, Proposition 2, Theorem 1, Corollary 1; Ohst et al., Definition 23, equation (64), Theorem 24 and Section 6.2; Eid–Quintino's classical-label-plus-Lueders-state interface). This is a documented source comparison, not an independent human priority opinion. Publication and exact-final-head qualification must be newly observed for the completion commit.
