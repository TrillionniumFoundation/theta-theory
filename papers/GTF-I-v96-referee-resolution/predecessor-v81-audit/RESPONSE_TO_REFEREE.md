# Response to the controlling reports — Revision 81 / R51

## 1. Frozen review, immediate predecessor, and mathematical scope

Revision 81 continues completed v80 at `31ac2a70a0304a1fe0cafd44a686584e4b8d9be9`, whose native source is `98a5cf437ef908bac876902bdb52b53958e30e7c`. The latest controlling reports remain **R51 on v77**, reviewed head `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`. The external and pipeline commits are respectively `96a3666ed516ea12fcdb8ede341b7082e4ff2c78` and `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`. Complete report texts, original paths, blobs and SHA256 digests remain frozen in `CONTROLLING_REPORTS.json` and the two `FROZEN_R51_*` documents. Remote review-reference inspection found no later review. No new round or external assessment of v78–v81 is inferred.

The paper retains the author's Annals/Inventiones/JAMS/Acta objective, its full closed ordered-binary effect body, every inherited theorem and proof, and its structural companion. The original report's recommendation is kept intact. Revision 81 supplies a further constructive result within the existing subject and consolidates repeated introductory/comparison prose. The detailed v80 versions remain available unchanged.

References below to Sections 53–64 identify source units rather than the printed section numbers. The current `evidence/THEOREM_LOCATIONS.json` supplies each edition's generated theorem and page locations. In particular, the new source is `sections/64-finite-risk-certificates.tex`.

## 2. A finite rational witness for the optimal learner

The immediate predecessor proved the joint interior law
\[
 M^*_{\rm int}(d,N,\delta,\eta)
 =\Theta\!\left(\frac N{\delta^2}[d^2+d\log(1/\eta)]\right)
\]
and dimension-uniform description length
\[
 B=\frac{d^2}{2}\log_2N+d^2\log_2(1/\delta)+O(d^2).
\]
Those results, the Mele–Bittel upper-estimator credit, and the algebraic selection proof by real quantifier elimination remain active. Their statements and proofs are unchanged. The new result makes the collective readout Gaussian rational and gives a finite certificate whose exact inequalities establish its risk for **every real effect** in the same interior.

### 2.1 Soundness of finite risk certificates

For the normalized record of `m` independent Choi acquisitions,
\[
 \|\Gamma_m(E)-\Gamma_m(G)\|_1\le2m\|E-G\|_{\rm op}.
\]
A fixed readout therefore changes the probability of any fixed subset of indices by at most `m r` between parameters at operator distance at most `r`. If every point `G` of a proved `r`-net satisfies
\[
 \Pr_G\{j:\|G-C_j\|_{\rm op}\le a\}\ge1-\alpha,
\]
then **thm:finitecertificate81** proves
\[
 \sup_E\Pr_E\{\|E-C_J\|_{\rm op}>a+r\}\le\alpha+mr.
\]
The radius buffer and probability buffer are both needed. The proof transfers the fixed set of labels associated with one nearby net point; it does not assume continuity of a moving success event.

The public net is fully explicit: with `K=ceil(4d/r)`, enumerate Gaussian-rational Hermitian coordinate matrices with coordinates in `K^{-1} Z` and retain precisely `I/4 <= G <= 3I/4` by exact PSD tests. An inward displacement followed by coordinate rounding proves coverage with error at most `3d/K`. Thus verification is over the complete mathematically specified net, not a sampled collection or an unverified claimed cover.

### 2.2 Rational readouts and a terminating search at the same call order

**prop:rationalreadout81** gives a prescribed denominator bound for a complete readout on reference dimension `D=d^m` with `L` decoded centres. Mix any ideal POVM with `s I/L`, `s=eta/16`. Round the first `L-1` Hermitian matrices to coordinates in `Q^{-1} Z`, where
\[
 Q=\left\lceil64L^2D/\eta\right\rceil,
\]
and define the last effect as the exact residual. The strictly positive margin controls both ordinary rounding and the accumulated residual; all effects remain positive and sum exactly to identity. The complete output-index variation is at most `3eta/32`, uniformly over all classical conditioning blocks. All `2^m` classical strings receive legal readouts, including strings of probability zero for particular targets.

At `m=1,2,4,...`, the new construction exhausts a **finite** list with this prescribed denominator. Every candidate undergoes exact legality and complete risk checks. An infeasible stage ends after its finite list; there is no indefinite witness search at small `m`. The retained estimator and dictionary prove that every `m >= m0` has a feasible rational candidate, with `m0` at the optimal joint statistical order. Ignoring extra records supplies feasibility above `m0`. Hence the first accepted dyadic stage satisfies `M <= 2m0`.

For `k=ceil(sqrt(N))`, set
\[
 a=\delta/(8k),\quad r_m=\min\{\delta/(32k),\eta/(16m)\},\quad\alpha=\eta/4.
\]
The finite certificate gives ideal future loss at most `5delta/8` except with probability `5eta/16`. A total trusted-control unhalved error budget `eta` changes the final index law in TV by at most `eta/2`. Thus actual risk for the original event `d_N(E,C)>delta` is at most `13eta/16<eta`.

**thm:rationallearner81** consequently attains the same joint optimal calls and reusable payload, for all integers `d,N>=1` and rational `0<delta<=2^-13`, `0<eta<=1/8`. It uses fresh one-call Choi preparations and only completed-output collective processing. The rational tuple, full risk certificate, and call count are computed before unknown-device access. Real quantifier elimination is unnecessary for this second construction.

### 2.3 Exact computation and journal exposition

The explicit finite search bounds charge up to `(2K+1)^(d^2)` parameter tuples and `(2Q+1)^((L-1)2^m d^(2m))` readout tuples per stage. Readout storage, exact arithmetic, quantum reference space, trusted-control synthesis, training calls and transmitted index length are distinct resources. The result provides finite rational certificates and a terminating construction, not a polynomial-time synthesis theorem.

`finite_risk_certificate.py` supplies a strict exact replay kernel. Its two complete scalar examples, complex-matrix local checks, mutation controls and incomplete-enumeration handling are recorded by `finite_risk_check.py`. These executed examples are distinguished from a general optimal learner and physical acquisition experiment. The continuum conclusion comes from the written transfer theorem, while the replay establishes the finite instance's hypotheses.

The focused introduction and comparison now organize the result by mathematical objects and access models. Repeated chronology and repeated scope discussions have been consolidated, with all original labels and displayed substantive conclusions preserved. The original edition files, all 64 inherited section sources (62 mathematical sections and two bibliographies), the old semialgebraic construction, and all historical A/B/C/D materials remain available. The detailed crosswalk below retains every R51 request and identifies the inherited answers as well as the new finite-certificate contribution.


## 3. All twelve required revisions in external R51 Section 8

| Item | Current answer and source |
| --- | --- |
| **R01 — Primary article** | `quantitative.tex` gives the primary focused `paper.pdf`. `structural.tex` gives the separate `STRUCTURAL_PAPER.pdf`. The current journal package includes both active source graphs and both articles for reconstruction; they remain separate mathematical submissions. `main.tex` gives the archival complete edition. Page counts are read from current receipts. |
| **R02 — Human priority** | **Open external task.** The specialist brief covers all retained and added theorem objects and their standard-method antecedents. No human specialist has been contacted or represented as providing clearance. AI reports, internal agents, finite checks and CI are not substitutes. |
| **R03 — Interface** | Every headline remains about ordered binary memoryless, input-consuming, classical-output measurements with no residual device quantum output. External retained references and collective readout do not change that interface. |
| **R04 — Dimension and optimality** | Sections 60–63 now provide joint interior call and description laws with absolute constants, including all positive confidence levels in the stated range. The complete body has the two-construction upper and strengthened lower in source Section 62 (`eq:fullbodyconfidenceupper80` and `eq:fullbodyconfidencelower80`); they do not close its growing-dimensional minimax problem. |
| **R05 — Tomography comparison** | Section 58 supplies the matched full-body one-call acquisition lower bound. Section 60 positively reanalyses existing tomography on a fixed interior. Section 62 removes its fixed-confidence restriction, with direct credit to MB's tail guarantee; Section 63 derives an effective readout by a separate finite search. Access, loss, confidence and computation remain distinct in `LITERATURE_AUDIT.md`. |
| **R06 — Pair witnesses versus estimator** | Pair-dependent Bernoulli and projective witnesses establish separation. Common learning uses one parameter-independent estimator, and the effective synthesis uses one public readout selected uniformly over all unknown effects. |
| **R07 — Comparison modulus** | `Q_N` is not renamed the exact distance and receives no unstated triangle inequality. Coding uses actual operational balls or operator-norm balls with proved metric transfer. The new confidence reduction uses continuity and the triangle inequality of `d_N`. |
| **R08 — Resources** | Calls, fresh acquisition width, retained output memory, trusted precision, dictionary size, algebraic search, gate count, workspace and transmitted bits are separately stated. Randomized expected prefix length remains a distinct theorem from deterministic fixed-length learned words. Section 64 adds explicit candidate-count and raw readout-storage bounds; optimal transmitted length is kept separate. |
| **R09 — Ranges** | The new interior law has `delta<=2^-13` and `0<eta<=1/8`; its operator specialization uses `epsilon<=2^-14`. Effective synthesis takes rational positive `delta,eta`. The earlier global `delta_d` entropy cap, block `delta_*` cap, and prefix theorem allowing `eta=0` retain their own meanings. |
| **R10 — Preparation/control model** | Section 59 retains the explicit full-body finite-control theorem. Section 63 now gives a finite algebraic specification and norm-certified realization of the query-optimal interior learner. Ideal risk `eta/2` plus output-law TV at most `eta/2` proves actual risk `eta` at the original loss; no exact physical preparation or exact-real decoder side channel is assumed. Section 64 supplies Gaussian-rational readouts and the same certified finite-control realization. |
| **R11 — Provenance** | Same frozen R51 identities, new v80 source baseline, fresh v81 source freeze, PDF/page checks, package reconstruction and exact-head read-only CI. Their actual outcomes belong to matching generated receipts. The predecessor's successful run does not qualify changed successor sources. The v81 introduction/comparison consolidate repeated process prose; all original labels and edition files are preserved. |
| **R12 — Wider history** | The historical derivation is preserved route by route; all five analytic aggregate flags remain false. None of the measurement theorems substitutes for a missing A/B/C/D analytic gate or adds significance merely by sharing a repository. |

## 4. All twenty-six detailed comments in external R51 Section 9

| Item | Topic | Current answer |
| --- | --- | --- |
| **D01** | Full body | The complete effect interval means ordered binary effects; the fixed interior is explicitly a subfamily of that interval, not a multi-outcome extension. |
| **D02** | Visible dimension factor | Full-body d^4 is displayed separately from the new interior d^2+d log(1/eta) factor and the one-use joint binary result. |
| **D03** | Normalization | All operational distances are unhalved trace norm. Finite-control output total variation is one half the trace error. |
| **D04** | Nonadaptive access | Entangled inputs and references are not excluded by the nonadaptive definition. The new upper has fresh single-call pairs and arbitrary collective processing of completed references. |
| **D05** | Stopping | Both lower arguments permit every-record bounded stopping. The diagonal confidence proof pads stopped records by ignored calls and sums counts under one common null process. |
| **D06** | Repeated eigenvalues | The exact calibration eigenbasis rule remains in Section56. Effective synthesis uses public coordinates and PSD predicates, requiring no unknown eigenbasis. |
| **D07** | Finite preparation | Sections 59 and63 separately specify algebraic instructions, certified physical norm errors and computation costs; exact physical state preparation is unnecessary for the stated transfer. |
| **D08** | Clipping | Inherited calibration clipping is inactive only on its good event. Interior spectral clipping uses Weyl plus a two-epsilon triangle bound, not noncommutative operator-Lipschitzness. |
| **D09** | Two support endpoints | Both regularized endpoint Loewner inequalities remain in the calibration proof. Operator error alone is not used to replace them. |
| **D10** | Compression | The exact positive-leakage compression identity and its squared calibration-error bound remain active before the compressed learners are invoked. |
| **D11** | Fresh data | Inherited adaptive stages use fresh experiments after their defining histories. Section62 uses independent complete seed runs; Section 63 uses independent fresh pairs. |
| **D12** | First rejection | The dyadic selector still terminates at first rejected amplitude/phase guard; fallbacks and every-record budgets remain fully specified. |
| **D13** | Conditional probability | Calibration/pair guarantees use conditional union bounds. Independent seed amplification is explicitly a different construction with fresh independent runs. |
| **D14** | Assembly | Designated incident pairs supply each diagonal, and the corresponding pair supplies each off-diagonal; duplicate estimates need not agree. |
| **D15** | Public rational coordinates | Both legalization and dictionaries use the original public basis. The semialgebraic readout variables are also in fixed public coordinates. |
| **D16** | Equality | Global squared-modulus and interior PSD codec tests retain exact strict acceptance and equality rejection. In the synthesis risk predicate, operator error equal to a is good; the complement uses strict inequalities. Section 64 includes equality in both finite good-label PSD tests and the risk inequality. |
| **D17** | PSD completeness | Principal-minor pruning is only a necessary prefilter in code. Full PSD predicates decide matrix legality; all principal minors or an equivalent real representation make the synthesis formula exact. |
| **D18** | Actual metric packing | Operational lower bounds use actual d_N-separated points and the metric triangle. Operator-norm volume arguments invoke the proved dimension-free interior comparison. |
| **D19** | Represented reals | A supplied real target needs certified approximation. The effective learner takes no unknown matrix or oracle: E is universally quantified offline; its computed readout has algebraic entries. Section 64 instead returns a rational tuple by prescribed-denominator finite enumeration, requiring no universal-algebraic solver. |
| **D20** | Decoder class | The learned-word converse uses a fixed public deterministic legal decoder. The retained randomized-prefix theorem separately permits shared/private randomness and expected length via Fano–Kraft. |
| **D21** | Finite checks | Small dictionaries, matrix kernels, finite transcripts and semialgebraic examples have their stated finite scope. No large general synthesis or theorem-scale matrix enumeration is claimed executed. The new replay records complete scalar verification and clearly limited higher-dimensional local checks. |
| **D22** | Evidence | Written proofs and cited decision procedures establish uniform laws and termination. Regression, builds and page review establish only their stated finite and reconstruction properties. |
| **D23** | Warnings | Raw font-expansion warnings are distinguished from inspected layout defects; current logs and page evidence determine the actual findings. |
| **D24** | Signatures | The predecessor identity and CI do not imply human authorship. Current publication metadata governs any current signature status; none is fabricated. |
| **D25** | Structural companion | Its fresh repeatable nondisturbing classical probes remain a separate theorem interface and source graph. |
| **D26** | Joint package | The article retains closed-body geometry, entropy, common learning and public coding, and adds joint confidence and effective synthesis on the fixed interior while preserving the original journal objective. Section 64 further supplies finite rational risk certificates at the same joint rates. |

## 5. Complete pipeline gate crosswalk

The groups reproduce all requests in frozen pipeline R51 Section 16: nine M mathematical, six P priority, five U resource, six V reproducibility and six E editorial items. Their original wording and recommendations remain in the frozen report. Execution-dependent gates are settled by current receipts, not by this author-side document.

| Gate | Group | Request | Current response |
| --- | --- | --- | --- |
| **M01** | Mathematical | Complete endpoint calibration | Retained in Section 56 (`lem:matrixcalibration77`) and audited below: simultaneous lower-endpoint and complement Loewner control, plus the operator error needed for leakage. |
| **M02** | Mathematical | Compression identity and leakage | Retained in `lem:matrixcompression77`; the exact positive leakage term and its upper bound are displayed, before applying the qubit learners. |
| **M03** | Mathematical | First-rejection termination | Retained in Section 55: the first failed amplitude or phase guard terminates and returns the preceding accepted scale; every exceptional record has a defined legal output. |
| **M04** | Mathematical | Conditional confidence | The calibration, qubit and pair confidence ledgers remain active. Section 62 adds independent seed amplification with q_d=2^(-3d); Section 63 separately allocates ideal risk eta/2 and output-law error eta/2. |
| **M05** | Mathematical | Pair-assembly multiplicities | Retained in Section 56: each off-diagonal coordinate is taken from its own pair and each diagonal from a designated incident pair; no consistency of duplicate estimates is assumed. |
| **M06** | Mathematical | Finite rational legalization | Retained in Section 56 in the original public basis; Section 59 explains finite algebraic comparisons and certified evaluation with slack. |
| **M07** | Mathematical | Exact codec equality cases | Retained in Section 57: a candidate is retained only when every squared comparison is strictly above the exact rational threshold. The new certificate uses exact rational comparisons and a fully regenerated target net. |
| **M08** | Mathematical | Actual-metric packing | Retained in Sections 54 and 57: separated actual `d_N` balls, the triangle inequality for `d_N`, and their uniform measure bounds control cardinality. |
| **M09** | Mathematical | All theorem ranges | Closed-body ranges remain unchanged. Sections 60–62 use delta<=2^-13; Section 62 proves all 0<eta<=1/8. Effective synthesis in Section 63 takes rational delta,eta; one-use operator confidence uses epsilon<=2^-14. Prefix descriptions separately allow eta=0. The new optimal rational construction uses the same rational delta,eta range; its general certificate-transfer assertion has separate parameters. |
| **P01** | Priority | Independent human expert review | OPEN: independent human specialist priority judgment is not obtained. The brief covers the retained and new theorem objects; neither internal agent checks, AI reports nor CI close this gate. |
| **P02** | Priority | Direct Mele–Bittel comparison | The existing MB binary tomography upper is credited. Section 62 exploits its dimension-dependent confidence tail; Section 63 uses it only to establish finite-search feasibility, and computes a new algebraic readout. Section 64 uses the already credited upper estimator only as a statistical existence bound. |
| **P03** | Priority | Zambrano–Ramos-Calderer–Kueng comparison | The literature comparison retains the distinction between separate known probes and Choi probes, external references, one-use loss and confidence. The full-body fresh-one-call lower remains valid for the precisely matched acquisition class. |
| **P04** | Priority | Reanalysis of existing estimators under future loss | The existing estimator has a sharp interior future-loss analysis, now joint in d,N,delta,eta. On the whole effect body, the one-call boundary lower excludes the uniform linear-horizon rate. These domains remain separate. |
| **P05** | Priority | Equivalent endpoint-log volume literature | Endpoint-logarithmic multiplicity and equivalent matrix-volume formulations remain explicit questions for specialist review. Bounded literature checks and standard-method credit are supplied, without universal priority certification. |
| **P06** | Priority | Qualified optimal-learning language | Current headlines distinguish the full-body d^4 upper from the absolute-constant interior joint law; ordered binary consuming classical-output access, confidence ranges and finite versus efficient computation remain explicit. |
| **U01** | Resources | Separate all resources | The resource ledger separates queries, acquisition width, retained output memory, finite trusted precision, quantifier elimination, algebraic descriptions, dictionary reconstruction, workspace and transmitted bits. Section 64 now states explicit finite parameter-grid, readout-search and raw storage bounds. |
| **U02** | Resources | Finite exact codec terminology | Both global and interior dictionaries remain finite exact constructions. The new readout search terminates but is not efficient; query optimality does not imply gate or arithmetic optimality. The new learner has a prescribed finite rational search at every dyadic stage; no efficiency inference is made. |
| **U03** | Resources | Incomplete construction cutoff | A finite prefix or resource cutoff remains incomplete construction. Finite semialgebraic tests do not execute the general high-dimensional synthesis theorem. New certificate replay reports a resource cutoff as incomplete and never promotes a checked prefix to a continuum certificate. |
| **U04** | Resources | Nonpublic headers | Only genuinely public dimension, horizon, accuracy, confidence and algorithm conventions are excluded from the word; nonpublic headers, seeds or target-dependent advice must be charged. |
| **U05** | Resources | Encoding versus learning | Supplied-effect encoding, device acquisition and public reconstruction remain distinct. Sections 62–63 compose them with no extra device calls for encoding. |
| **V01** | Reproducibility | Exact-head read-only reconstruction | The completed v80 native and publication objects are pinned in CONTROLLING_REPORTS.json. Current v81 native/publication objects require their own matching read-only receipts; no predecessor CI run is treated as current evidence. |
| **V02** | Reproducibility | Source/PDF hashes and manifest | CONTROLLING_REPORTS.json freezes the same R51 pair. Current evidence/SOURCE_HASHES.json, evidence/BUILD_RECEIPT.json and evidence/PACKAGE_MANIFEST.json bind the new sources, PDFs and packages. |
| **V03** | Reproducibility | Ordinary/optimized equality | Current ordinary/optimized equality must be executed against the current source inventory; historical success is retained only as historical evidence. |
| **V04** | Reproducibility | Raw warning wording | Raw typesetting warnings and inspected rendered defects are reported separately by current diagnostics and page checks. |
| **V05** | Reproducibility | Optional cryptographic authorship | No cryptographic human authorship signature is supplied or inferred. The conditional suggestion to sign a release does not authorize signing as a person or make source reconstruction an authorship attestation. |
| **V06** | Reproducibility | CI evidence boundary | CI reconstructs identified sources and artifacts and executes stated finite checks. It is not a proof certificate, independent priority judgment, or journal decision. |
| **E01** | Editorial | Focused article primary | quantitative.tex produces the primary focused paper.pdf. The current journal package contains this article and the separate structural companion, each with its own active source graph. |
| **E02** | Editorial | Structural companion separate | structural.tex produces the separate STRUCTURAL_PAPER.pdf; repeatable nondisturbing classical-probe assumptions remain logically independent of consuming quantum measurements. |
| **E03** | Editorial | Complete edition archival | main.tex produces COMPLETE_REVISION.pdf as the preserved archival proof corpus, not a competing significance claim. |
| **E04** | Editorial | Compact journal history | Detailed history and review routing stay in repository audits and predecessor archives. Both journal entry points are independently reconstructible. New edition files consolidate duplicate journal-facing discussions while retaining their complete predecessor text. |
| **E05** | Editorial | Theorem objects before chronology | The article foregrounds geometry, entropy, common learning and public coding, strengthened by confidence-optimal learning and effective algebraic readout; revision chronology is provenance. |
| **E06** | Editorial | Concise scope paragraph | Scope states the binary interface, global versus interior domains, absolute confidence law, unmatched full-body dimension factor, finite synthesis costs and independent analytic programme. |

## 6. The ten pipeline risks

| Risk | Frozen assessment | Current disposition |
| --- | --- | --- |
| **Risk01** | Independent priority — high | Independent human priority assessment remains R02/P01. Standard amplification, coin reduction, real quantifier elimination and code construction are credited; no first-result or acceptance certification is inferred. |
| **Risk02** | Interface breadth — high for top four | The target remains ordered binary consuming classical-output measurements. The new synthesis is for a full-dimensional interior and does not claim a multi-outcome or residual-output extension. |
| **Risk03** | Growing dimension — high in the reviewed object | The interior now has the absolute-constant joint call law N delta^-2[d^2+d log(1/eta)], plus dimension-uniform description length. The two-construction full-body upper remains unmatched by the joint lower; global growing-dimensional entropy constants also remain unclosed. |
| **Risk04** | Exact distance — moderate | Q_N is still a comparison modulus. Exact projective-pair formulas and fixed-interior comparisons do not give a general exact adaptive distance. |
| **Risk05** | Computational efficiency — high | Finite algebraic synthesis, the prescribed-denominator rational readout search and exact dictionaries terminate. Section 64 gives explicit finite enumeration and storage bounds. Their time, bit complexity, quantum workspace and gate count may be enormous; query/payload optimality does not certify efficiency. |
| **Risk06** | Small-error/range — moderate | Every current theorem states its own small-error, confidence, rational-input and decoder conventions; eta=0 is permitted only in the supplied-target prefix theorem. |
| **Risk07** | Physical resources — moderate in the reviewed object | Sections 63 and 64 give algebraic and Gaussian-rational finite trusted-control learners at the joint optimal query/payload rates. Certified trace/diamond errors remain physical assumptions; no device experiment or efficient synthesis is claimed. |
| **Risk08** | Finite-regression overinterpretation — controlled | Partial regression verifies its declared identities and interfaces. A complete rational certificate, combined with the proved analytic transfer in Section 64, certifies all-real interior risk. Termination and the optimal rate follow from the written construction; the two scalar replays do not execute general optimal synthesis. |
| **Risk09** | Historical volume — controlled | The entire predecessor history is retained; current focused and structural articles remain separate from COMPLETE_REVISION.pdf. |
| **Risk10** | Whole-program overclaim — controlled | All five A/B/C/D aggregate flags remain false; the complete route-by-route gate inventory is preserved. |


## 7. Preservation, current evidence, and the next review

The immediate baseline contains 410 native files and 787/289/116 complete/focused/structural active labels. Every baseline file is preserved in place or, for changed source entries and audit documents, additionally byte-for-byte under `predecessor-v80-audit/`. All old mathematical section sources are unchanged. The new manuscript and current build evidence are identified by their own source inventory, actual native commit, and publication commit. The separate structural source graph and 41-page content are unchanged.

Current execution results are supplied only by `evidence/BUILD_RECEIPT.json`, `REGRESSION_RESULTS.json`, `PAGE_CHECKS.json`, `VISUAL_REVIEW.json`, the standalone journal rebuild, and the exact-publication-head reconstruction. Old successful builds remain old evidence. Finite replay, continuum proof, independent priority assessment and editorial judgment have distinct meanings.

R02/P01, an independent human specialist priority opinion, remains an external review task. The prepared brief now includes the rational-certificate theorem and its precise overlap question. No outside reviewer is represented as contacted or as approving this revision. The requested journal objective is retained. The five separate analytic aggregate flags remain false; the finite-dimensional measurement results neither assume nor close those historical analytic obligations.
