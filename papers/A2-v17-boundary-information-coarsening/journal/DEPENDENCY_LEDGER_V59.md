# Principal article: theorem inputs and comparison references — v59

This is the current reading-based dependency ledger. It carries forward the corrected v57 classification, which the latest v58 referee report keeps closed. The v56 all-comparisons classification remains superseded; historical maps and responses are not overwritten. Literal reference occurrences and declared roles are in `DEPENDENCY_MAP_V59.json`. Neither ledger is a formal proof certificate.

## External theorem application

**Consumer:** Corollary `cor:v45-physical-chart`, principal Corollary 19.9.  
**Input:** `thm:v25-global-physical-reconstruction`, full Theorem F.47.3, “Uniform global reconstruction from long same-type records.”  
**Full source:** `article/25b_augmented_global_reconstruction_v26.tex`.  
**Role:** substantive theorem input, including the acquisition/risk conclusion and its hypotheses. The same label is internal in the full manuscript.

| Requirement | Origin and use |
|---|---|
| Fixed persistent N+1 marked design | Selected skeleton in the principal article; not unmarked discovery. |
| Unique transition matching and compact inverse | Proper asymmetry on the selected neighborhood plus the finite analytic signature/compact inverse section. |
| Uniform selected-channel laws | Fixed finite clearances and stipulated compact-family bounds, using the selected-locality lemma. |
| Independent holonomies with uniform nonsingularity | Fixed real-invertible integer gain matrix M and compact nonsingular lattice family; `sigma_min(LM)` has positive minimum. No unimodularity or known Gram form is inserted. |
| Analytic/chart and physical sensor conventions | Additional assumptions imported from the acquisition theorem and its common-record construction. |
| Pilot and estimator risk, charged caps and prescribed budgets | Conclusions supplied by the full theorem, not reproved from exact law-valued injectivity. |

The physical record contains both planar components of endpoints in channel sensor frames, the clock and preparation outcomes; the two endpoint types share a channel frame, while different channels are unregistered. The post-pilot estimator can discard coordinates. That does not turn the calibration into an endpoint-histogram-only sensor. The corollary retains every failed preparation in the charge.

The full theorem is downstream of the geometric inverse. Its application is not used by the proof of Theorem 1.1, A or B. That statement records the reviewed argument direction, not an implication of where a `ref` token occurs. The principal article's three main geometric proof paths remain printed internally, including the graph/support conversion. The entire article must not therefore be advertised as having no external theorem-dependent consequence.

## The uniform-block refinement

Proposition `prop:v58-uniform-blocks` is proved in `article/23a1_uniform_blocks_v58.tex`, included by the existing signed-contact section in both entries. Its algebra uses the internally defined positive-curvature parameters and the existing exact block; its actual-smooth consequence invokes `lem:v27-smooth-jet-factorization` and `prop:v22-last-jet-block`, both printed internally. The factorial coefficient-space claim is proved by absolute summation of the displayed bounds. The v57 referee memorandum is cited for attribution, not used in place of the printed proof. No new full-only theorem input is introduced.

The new block estimate does not give the entire lower-triangular nonlinear inverse a uniform bound. The separate factorization in `eq:v58-triangular-factorization` locates this limitation without attributing it to the diagonal blocks. The geometric theorems and the acquisition corollary retain their distinct assumptions.

## The complete local analytic action inverse

The new `article/23a2_analytic_contact_inverse_v59.tex` has three proved statements. Its half-line lemma uses the internally printed Green kernel and protects internal evaluation discs; its envelope lemma uses finite stationarity and a terminal estimate; its inverse theorem combines the existing finite low-jet matrices with a norm-convergent high-vanishing tail inverse. All these proof bodies are compiled in the principal article. No acquisition or probability theorem is imported into this argument.

The whole derivative is a nonvanishing multiplication operator plus a compact sum of contracted boundary visits. This is additional structure beyond the block-diagonal estimate. The new theorem gives a local inverse in a fixed-disc bounded-holomorphic norm and order-independent linearized quotient bounds in the induced analytic norms. It does not claim that the full map improves holomorphic radius, that weak density errors control that norm, or that contact-germ inversion removes global matching or acquisition hypotheses.

The source and hypothesis path is `lem:v4-halfline` / `eq:v4-half-green` -> `lem:v59-holomorphic-halfline` -> `lem:v59-envelope-operator`, together with `lem:v27-smooth-jet-factorization` / `prop:v22-last-jet-block` -> `thm:v59-analytic-contact-inverse`. The same local statement is shared with the full technical entry. These are reading-derived dependencies, not a syntax-only independence certificate.

## Other full-manuscript targets

| Label | Role in its printed context |
|---|---|
| `sec:g-inverse` | Comparison with the equal-gap parametric inverse. |
| `sec:v10-acquisition` | Comparison with regularized finite-preparation recovery and its additional smoothness requirements. |
| `sec:v25-analytic-variation-bundle` | Comparison with fixed-contact finite-jet bundles and positive designs. |
| `sec:v25-common-observables` | Discussion of the richer physical pilot and common observation space. |
| `sec:v25-uniform-physical-global` | Discussion of implementing a law inverse after that pilot. |
| `sec:v26-position-benchmark` | Contrast with the direct-position experiment, not statistical equivalence. |
| `sec:v3-amplitude-data` | Leading-amplitude comparison and its parametrized inverse. |
| `thm:v5-jets` | Identification of the identical-contact specialization of a displayed block. |

These eight targets are background/comparison references in those contexts. A target is not classified as a comparison merely because it lies outside a proof environment. If later changes use any of them as a substantive theorem hypothesis, the role declaration must be updated.

## Regression checks and their limits

The checker scans labelled statements together with associated proofs and separately reports prose occurrences. A fixture with the only external reference in a corollary hypothesis still produces a theorem input. The fixture fails if that input is misdeclared as a comparison or is attached to an undeclared consumer. The headline literal-reference graph is checked only for unexpected new named edges. It does not resolve all anaphora, unlabelled mathematical reasoning, section-wide hypotheses or imported definitions. Reading-derived declarations and syntax validation are kept separate.
