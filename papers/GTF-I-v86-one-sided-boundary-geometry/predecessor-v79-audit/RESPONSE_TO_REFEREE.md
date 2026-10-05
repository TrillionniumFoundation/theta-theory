# Response to the controlling reports — Revision 79 / R51

## Current object and further substantive response

The immediate baseline is completed v78 `1906166f98f47f4fe387143617948766395ba186` (qualified source `f893d00e51bf008c530de6046b008a3237001f81`). R51 instead reviewed v77 `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`. The external and pipeline report commits remain `96a3666ed516ea12fcdb8ede341b7082e4ff2c78` and `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`. No later report, human opinion, or new review of v78 is invented. The complete reports and their hashes are retained.

We have further strengthened the mathematics in the same paper rather than changing its objective or deleting difficult results. The new active Section 61 contains four theorems, with complete proofs in both mathematical editions:

* `thm:interiorentropy79`: for every `d,N>=1`, `0<delta<=2^-13`, arbitrary legal lower centres and absolute constants, the interior covering number lies between `(sqrt(N)/(2048 delta))^(d^2)` and `(25 sqrt(N)/delta)^(d^2)`. This is joint in dimension, horizon and accuracy, with no hidden `O_d` constant.
* `thm:interiorcodec79`: an explicitly ordered finite rational dictionary, exact two-sided PSD comparisons, equality rejection, certified rounding and `5delta/16` error. The payload is `(d^2/2)log2 N+d^2log2(1/delta)+O(d^2)`, without the entrywise `d^2log d` cost. Enumeration remains a separate, potentially enormous resource.
* `thm:prefixrate79`: with shared and private randomness, per-target failure at most `eta<=1/8`, and seedwise prefix-free one-way messages, the optimal worst-target expected length is `(1-eta)[(d^2/2)log2 N+d^2log2(1/delta)]+O(d^2)`. The converse permits randomized decoding. No abort flag, timing or target-dependent advice is free.
* `thm:interiorlearnedcode79`: one common finite-output learner attains the joint optimal training order `Theta(d^2 N delta^-2)` and deterministic-decoder payload order on the same interior. It credits and reanalyses Mele–Bittel's estimator, uses independent one-call acquisitions, and adds no device call for encoding. The theorem retains that estimator's ideal trusted operations and does not claim efficient physical synthesis.

These are positive additions on a full-dimensional interior; they do not replace the full closed-body theorem or its endpoint logarithms. All 61 inherited section files and all 745/245/116 active predecessor labels remain. The focused article is the journal-facing object; the complete edition retains the historical development.

## Current disposition of the twelve required revisions

| Item | Current response and locator |
|---|---|
| R01 | Focused submission is independently complete; the new journal package includes only its active graph, PDF and verifier. Structural paper separate, complete edition archival. |
| R02 | The human specialist task remains open. The brief now includes the four new theorem objects and standard-method credit; no AI/CI output is counted as human priority clearance. |
| R03 | Headline and all new statements retain ordered binary, memoryless, input-consuming classical output and arbitrary retained external reference. |
| R04 | New Section 61 supplies uniform growing-dimensional entropy and coding, complementing v78's sharp interior learning. The full-body `d^4` upper is still explicitly unmatched. |
| R05 | The direct Mele–Bittel reanalysis in section 60 is retained. The new learned-word theorem connects it to the sharp dimension-uniform description law, with explicit clipping and measurable finite readout. The fresh-block full-body separation in section 58 remains. |
| R06 | Entropy packings and pair witnesses prove converses; the learned-word theorem uses one parameter-independent estimator and one fixed decoder. |
| R07 | All new packing arguments use the actual metric `d_N` or the operator norm. No triangle inequality or exact-optimum interpretation is assigned to `Q_N`. |
| R08 | Calls, trusted measurement operations, dictionary enumeration, workspace, fixed length, expected prefix length, public seeds and nonpublic headers are now distinguished explicitly. |
| R09 | Uniform interior matching range is `d,N>=1`, `delta<=2^-13`; exact codec alone works for rational `0<delta<=1`; prefix risk `0<=eta<=1/8`; learned-word theorem has failure `1/8`. Earlier ranges remain unchanged. |
| R10 | The existing finite trusted-control theorem for the full-body learner remains. The imported query-optimal interior estimator is kept in its ideal trusted-operation model; finite output does not establish efficient gate synthesis. |
| R11 | Every successor source, PDF, standalone package and exact published head is qualified afresh. Source reconstruction, finite regression and continuum proof remain separate. |
| R12 | The entire historical A/B/C/D gate inventory is retained and its five aggregate flags stay false. No local measurement theorem is substituted for those analytic obligations. |

## Detailed comments, pipeline gates and risk status

The complete v78 line-by-line response reproduced below supplies the retained answers D01–D26 and the full M/P/C/V/E submission-gate crosswalk. Those passages are identified as predecessor response, not as new execution claims. Their mathematical locators continue to exist in v79. In particular: D04/D22 gain the dimension-uniform interior description theorem; D17–D20 gain an exact inner dictionary and the separate randomized-prefix converse; D24 is governed by the new current-object receipt, never the inherited runs; D26 continues to leave independent programme flags unchanged. P01 remains external. All source/PDF/CI gate outcomes are execution-dependent and must be read from the matching v79 receipts.

The ten R51 pipeline risks have the following current dispositions. R1 human priority remains open. R2 binary interface breadth is unchanged. R3 growing dimension is strengthened for both learning and descriptions on the stated interior, not solved for the closed body. R4 `Q_N` remains a comparison modulus. R5 exhaustive computational cost remains explicit. R6 new ranges have absolute constants and earlier ranges retain their original caps. R7 trusted tomography synthesis is not hidden in the call budget. R8 finite checks are not proofs. R9 archival volume is not a significance argument. R10 no whole-program closure is claimed.

## Preserved detailed response from v78 (historical text)

The following document is retained verbatim. References to “this revision”, old file counts or earlier runs within this historical block describe v78 only; the current objects and changes are the ones stated above and in the v79 manifests.

---

# Response to the controlling referee reports — Revision 78 / R51

## 1. Reviewed object, governing reports, and response

This revision responds to the latest reports on **completed Revision 77**, not to the earlier R50 assessment of Revision 76. The reviewed final head is `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`; its qualified native-source commit is `91df620ec7b6e02a6f0fe1c7798639c2626c742b`.

| Governing object | Exact identity | Frozen copy |
| --- | --- | --- |
| External R51 report | `96a3666ed516ea12fcdb8ede341b7082e4ff2c78`, `GENERAL_THETA_FOUNDATIONS_I_V77_REFEREE_REPORT_R51.md` | `FROZEN_R51_REPORT.md` |
| R51 proof/pipeline audit | `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`, `GENERAL_THETA_FOUNDATIONS_I_V77_PROOF_PIPELINE_AUDIT_R51.md` | `FROZEN_R51_PIPELINE_AUDIT.md` |

`CONTROLLING_REPORTS.json` records the review branches, Git blobs and SHA256 values. The complete predecessor responses and audits remain in `predecessor-v77-audit/`; their R50 identifiers are historical. In this document **R01–R12** refer to external R51 Section 8 and **D01–D26** to external R51 Section 9. The companion audit's Section 16 gates receive separate identifiers M, P, U, V and E below, so its priority gate cannot be confused with an earlier review number.

The reports find no fatal gap in the reviewed common matrix learner, finite exact matrix codec, learned-description corollary or corrected first-rejection procedure. They nevertheless judge the reviewed object below the threshold of Annals, Inventiones, JAMS and Acta, principally on breadth, significance, growing-dimensional sharpness, computational efficiency and independent priority. That assessment is preserved verbatim. The present response retains the requested general-mathematics-journal objective and addresses the mathematical reasons with additional theorems. It neither substitutes the reports' suggested publication destination for the author's objective nor represents a subsequent editorial acceptance as obtained.

The principal addition is a sharp training-resource law. For the complete ordered binary effect body in each fixed dimension `d>=2`, with fresh quantum training blocks of at most `b<=N` calls,
\[
 M_b^\star(d,N,\delta,\eta)
 =\Theta_d\!\left(\frac{N^2}{b\delta^2}\log\frac1\eta\right).
\]
The explicit upper bound is `C d^4 N^2/(b delta^2) log(d/eta)`. The model permits classical feedback, retained quantum outputs and collective measurements at block boundaries. Each new block, including its fresh reference and unused inputs, is conditionally tensor-separated from old retained systems and remains isolated from them until its last query. Its length is declared and charged in full before it begins. The theorem concerns this precisely stated training model; the future loss retains unrestricted adaptive access.

This establishes a worst-case quadratic horizon cost for fresh one-call Choi/probe acquisition, even with collective processing, and a linear horizon cost when blocks of length up to `N` are available. It gives a direct mathematical answer to the reports' request to assess existing one-use tomography interfaces under the future loss. Dimension one has the separate scalar order `Theta(N delta^-2 log(1/eta))`, independent of the block cap.

A second addition supplies finite trusted-control specifications. The learning and learned-code guarantees retain the same requested loss `delta`, risk `eta` and call orders when all known preparation/control errors have an every-record sum of unhalved trace/diamond norm at most `eta` and the ideal learner is run at risk `eta/2`. The resulting output-law total variation is at most `eta/2`. Exact physical preparation is therefore unnecessary for these guarantees. Gate count, preparation time, arithmetic, quantum storage and dictionary reconstruction remain separately accounted resources.

A third addition proves the joint dimension-and-accuracy obstruction even for arbitrary coherent adaptive training. Section 60 obtains
\[
 M\ge c d^2N\delta^{-2}
\]
already on the full-dimensional interior \(I_d/4\preceq E\preceq3I_d/4\). A dimension-free interior comparison then reanalyses the existing Mele–Bittel binary estimator and gives the matching \(\Theta(d^2N\delta^{-2})\) law at fixed failure probability \(1/8\), using fresh one-call probes. Thus a stronger future-loss analysis of an existing estimator is valid on a fixed interior, while the boundary obstruction prevents its uniform extension to the whole effect body. The full-body \(d^4\) upper factor remains unmatched.

These are written mathematical results in Sections 58–60, with author-side internal checks. They are not yet an external referee opinion on v78. Independent **human** priority assessment remains outstanding, and source reconstruction is not an authorship attestation.

## 2. Responses to the twelve required revisions

### R01 — Primary article and archival complete edition

The primary mathematical submission is `quantitative.tex`, producing `paper.pdf`. It contains the focused chain needed for the quantitative theorems, including the new block-resource and finite-control results. The structural paper has its own `structural.tex` entry point and `STRUCTURAL_PAPER.pdf`. The cumulative source and all its proofs remain in `main.tex`, producing `COMPLETE_REVISION.pdf`.

The reviewed 45-page and 185-page counts describe v77. The expanded v78 objects have their own generated page checks and build receipt; predecessor counts are not copied as current metadata. The complete edition and history remain available for audit and future development without making a competing journal manuscript or using their length as evidence of significance.

### R02 — Independent human priority assessment

**Outstanding external judgment.** `INDEPENDENT_REVIEW_BRIEF.md` specifies the midpoint comparison, endpoint-logarithmic entropy, common future-use learner and exact public matrix codec, together with the new training-resource statements. `LITERATURE_AUDIT.md` supplies theorem-level comparisons for that review. No independent human specialist opinion has been obtained in this revision work, and no person has been contacted on the author's behalf.

An author-side literature comparison, internal agent cross-review, successful computation, and the AI-assisted R51 report have different evidentiary roles. None is labelled human priority clearance. This requirement remains visible in `PROOF_STATUS.json` as R02/P01; it is not silently declared resolved by the additional proofs.

### R03 — Binary qc interface in the headline claims

The interface is an ordered binary memoryless measurement `(E,I_d-E)` with `0<=E<=I_d`. Each call consumes its input and returns a classical outcome, with no residual device quantum output or access to its environment. All-rank and full-body statements concern this whole Hermitian effect interval in the given Hilbert dimension.

Retained references are external systems of the tester. Their presence does not turn the measurement into a residual-output instrument. The current model, abstract-level claims, theorem discussions and resource ledger retain these distinctions. The new block parameter restricts training access within this same interface.

### R04 — Fixed-dimensional optimality and visible dimension factors

The inherited full-body common learner retains the explicit bound
\[
 M\le C d^4N\delta^{-2}\log(d/\eta).
\]
The new block theorem has the explicit upper bound
\[
 M_b^\star\le C d^4N^2(b\delta^2)^{-1}\log(d/\eta)
\]
and the matching fixed-dimensional order in `N,b,delta,eta` for `d>=2`. The dimension-free projective lower bound is not presented as matching `d^4`. The scalar case is stated separately.

Section 60 now strengthens the converse to \(\Omega(d^2N\delta^{-2})\), including arbitrary coherent adaptive training, and proves a matching joint \(d,N,\delta\) law on \(I_d/4\preceq E\preceq3I_d/4\) at fixed failure \(1/8\). Its upper procedure is credited to the existing Mele–Bittel estimator with the new interior loss analysis. For the complete body and the fresh-block model, the two lower bounds combine, within their common range, to
\[
 M\ge c\delta^{-2}\left(d^2N+\frac{N^2}{b}\log\frac1\eta\right).
\]
This does not match the full-body \(d^4\) upper factor. Global covering and payload constants remain fixed-dimensional.

### R05 — Direct comparison with present tomography

The prior substitution of one-use accuracy `delta/N` into a tomography theorem was a sufficient baseline. Section 58 now proves a converse for the relevant acquisition class itself.

For the projective family `E_phi` in `lem:blockfidelity78`,
\[
 d_N(\mathcal M_{E_0},\mathcal M_{E_\theta})
 =2\sin(N|\theta|/2),\qquad N|\theta|\le\pi.
\]
Any fresh-block training protocol with cap `b` and every-record budget `M` has final root fidelity at least `exp(-Mb theta^2/4)` when `b|theta|<=1`. Taking `theta=4delta/N` and reducing estimation to a two-point test gives
\[
 M\ge \frac{N^2}{24b\delta^2}\log\frac1\eta
 \quad(0<\eta\le1/8).
\]
For `b=1` this applies even when outputs are stored and collectively processed, and even with classical adaptation of later fresh probes.

`cor:onecallseparation78` and `LITERATURE_AUDIT.md` match this model to the independent Choi preparations in Mele–Bittel and the separately prepared known probes in Zambrano–Ramos-Calderer–Kueng. Consequently, no estimator retaining those acquisition interfaces can have the uniform full-body linear-horizon guarantee. This conclusion does not identify nonadaptive access with product probes inside a general block, prohibit collective decoding, or extend the lower bound to coherent cross-block feedback. Section 60 supplies the positive half of the requested reanalysis. Its weak-measurement information lemma applies even when inputs and retained memory are parameter-correlated through previous calls; an operator-norm packing and Fano's inequality yield the joint \(d^2N\delta^{-2}\) converse. On \(I/8\preceq E,F\preceq7I/8\), the unregularized horizontal Sylvester solution proves
\[
 d_N(E,F)\le 4\sqrt N\,\|E-F\|_{\rm op}
\]
with no dimension factor. The Mele–Bittel binary estimator, used at operator error \(\delta/(8\sqrt N)\), therefore achieves \(O(d^2N\delta^{-2})\) on the fixed interior \(I/4\preceq E\preceq3I/4\), at failure \(1/8\). This matches the new coherent-training converse. The answer is consequently precise in both domains: the existing estimator admits a sharp interior future-loss analysis; no estimator with the same one-call acquisition interface attains the full-body linear-horizon order.

### R06 — Pair geometry and one common estimator

Sections 53–54 compare a supplied pair and measure actual operational balls. Section 56 specifies a single data-dependent calibration, fresh compressed qubit experiments and a legal common matrix estimator. Its design does not receive the unknown effect or a hard pair as advice.

The Section 58 upper bound invokes that common learner at horizon `b` and accuracy `delta/ceil(N/b)`. The projective hard pair is used only for its converse. The new result therefore preserves the distinction between existence of a pair-dependent distinguishing experiment and a common procedure that learns every effect.

### R07 — Meaning of the comparison modulus

`Q_N` remains the midpoint-resolvent comparison modulus. The proof uses its explicitly proved upper and lower comparisons with `d_N`. No triangle inequality for `Q_N` is assumed in matrix assembly, coding or covering.

The exact projective distance in `lem:blockfidelity78` is restricted to the stated two-point orbit and angular range. It does not supply a general exact distance formula for arbitrary binary effects. Both the greedy-code cardinality proof and learned-code composition use the triangle inequality of the actual operational distance.

### R08 — Payload, reconstruction, workspace and training

The exact arbitrary-dimensional codec is retained with its full legal-grid enumeration, strict rational comparisons, deterministic reconstruction and equality rules. Its optimal fixed-length payload is
\[
 \frac{d^2}{2}\log_2N+
 \lfloor d/2\rfloor\log_2\log(N+2)+
 d^2\log_2(1/\delta)+O_d(1)
\]
in the fixed-dimensional small-error range.

The ambient grid can contain `(K+1)^d(2K+1)^{d(d-1)}` coordinate tuples, where `K=ceil(32dN/delta)`. Enumeration, exact arithmetic, stored dictionary entries and preparation work are not bits transmitted in the index and are not optimized by the payload theorem. `cor:blocklearnedcode78` attains this payload after block-constrained learning with no additional device calls. It proves the two resource orders simultaneously while keeping them separate.

### R09 — Ranges and exceptional cases

The full-body learning theorem has an absolute small-error cap and `0<eta<=1/8`. The new block law assumes integers `d>=2`, `N>=1` and `1<=b<=N`, and `delta_*` no larger than the inherited learning cap and `1/4`. The scalar `d=1` case is a separate clause. Section 60 uses `delta<=2^-13`; its sharp interior law has fixed failure `1/8`, while its lower bound holds for every `0<eta<=1/8`. Its one-use operator-norm corollary uses `epsilon<=2^-14`.

The exact matrix construction is finite for rational `0<delta<=1`; the matching lower payload law uses `delta<=delta_d` for each fixed dimension. The learned-code corollaries use the intersection of these ranges. Finite control specifications use rational tolerances or supplied smaller rational tolerances of comparable size. None of these statements asserts a new full-error entropy law.

### R10 — Finite physical preparation and control

Section 59 gives `lem:controlhybrid78` and `thm:finitecontrollearning78`. The error assumption is pathwise over every complete record, including rejected guards and failed concentration events. A quantum instrument is charged as its entire flagged CPTP channel; separate branchwise CP error bounds must first be summed. This avoids treating discontinuous decisions as stable under rounding.

The actual and ideal experiments retain exactly the same classical output rule. With ideal failure probability at most `eta/2` and aggregate known-operation norm error at most `eta`, their output laws differ in total variation by at most `eta/2`, so the actual risk at the original `delta` is at most `eta`. No extra approximation of the returned effect or `delta/N` hardware tolerance is needed for this transfer.

For a block state of dimension `D=d^m`, a normalized algebraic state specified through a Gaussian-rational vector has a finite direct coordinate description of order `D log(D(M_*+S)/eta)` bits at the stated error budget, where `M_*` is a public every-record call cap and `S` bounds other trusted events. The model assumes certified realizations within the assigned trace/diamond errors. It is not a physical experiment or a polynomial state-preparation theorem. Approximate preparation retains the same fresh-block separation.

### R11 — Provenance and compact journal evidence

The frozen R51 identities are stated above. The predecessor native object, metadata publication steps and final-head reconstruction remain historical evidence for v77. The new native-source identity, source hashes, theorem locations, PDF hashes, package manifest, page checks and exact-head reconstruction must come from the v78 source-freeze process.

`evidence/JOURNAL_PACKAGE.zip` contains the focused and structural entry points with their dependencies. The full repository retains the expanded proof corpus and predecessor audits. The generated current receipts, rather than a success statement copied into this response, determine which source and final head were reconstructed. Font-expansion warnings in raw logs and findings from rendered-page review are reported separately. No cryptographic human signature is inferred.

### R12 — Independent A/B/C/D programme

`HISTORY_AND_PIPELINE_AUDIT.md` retains the full derivation route and the model-specific A/B/C/D gates. All five aggregate completion flags remain false. The measurement theorems do not prove raw unsmoothed local limits, stopped-path large deviations, the global past kernel, nonlinear Nisio cores, filtering/QMD/LAN, changing-filtration response or labelled posterior contraction.

The historical record is preserved because it is part of the research derivation and prevents false dependency claims. The mathematical case for this article consists of its actual measurement theorems and consequences.

## 3. Responses to all twenty-six detailed comments

| R51 item | Disposition and precise location |
| --- | --- |
| **D01 — Full body** | The full body is `mathfrak E_d={E=E*:0<=E<=I_d}` of ordered binary effects. The consuming classical-output interface is stated in the model, theorem discussions and resource ledger. |
| **D02 — Immediate dimension factor** | The explicit `d^4` upper factor accompanies the common learner and block law. Fixed-dimensional optimality is not a growing-dimensional matching claim. |
| **D03 — Norm convention** | `d_N` uses unhalved final trace norm; classical total variation is half that quantity. Section 59 uses this factor in the `eta/2` transfer. |
| **D04 — Nonadaptive access** | A nonadaptive tester may have entangled inputs and references. Definition `def:freshblocks78` separately describes fresh block length, within-block adaptive access, classical feedback and collective retained-output processing. |
| **D05 — Bounded stopping** | The future distance and training lower bounds retain public bounded stopping. In Section 58 each block is predeclared and fully charged; stopping between blocks may use the entire history. |
| **D06 — Multiplicities** | Section 56 keeps the deterministic ordered-eigenspace/public-basis projection/Gram–Schmidt rule in the proof. Section 59 explains its finite algebraic specification. |
| **D07 — Algebraic preparation** | The inherited ideal preparation is an explicit reference experiment. Section 59 supplies finite trusted approximations with a separate control-error budget and preparation complexity. |
| **D08 — Calibration clipping** | On the good event the raw spectrum is already inside the enlarged interval and clipping is inactive; outside it clipping and affine contraction provide legality and a deterministic budget. No global clipping-monotonicity claim is used. |
| **D09 — Both support endpoints** | `lem:matrixcalibration77` controls `E+tI` and `I-E+tI` in relative Loewner order. Its additional operator error is used for leakage; it does not replace either endpoint estimate. |
| **D10 — Compression identity** | `lem:matrixcompression77` displays `C(I-C)=P E(I-E)P+P(E-A)(I-P)(E-A)P`, then bounds the positive leakage by the calibration error squared. |
| **D11 — Fresh observations** | Product, dyadic, fine, endpoint and pair observations are fresh after their conditioning record fixes the experiment. The horizon substitution in Section 58 leaves that property intact. |
| **D12 — First rejection** | Section 55 terminates at the first rejected amplitude or phase guard and returns the preceding accepted state of the selector. No later stage is reached after rejection. |
| **D13 — Conditional union** | Pair guarantees are conditional on the complete calibration record and use an ordinary conditional union bound. Independence of their adaptive failure events is not asserted. |
| **D14 — Designated diagonals** | Weighted assembly takes diagonal entries from fixed designated incident pairs and off-diagonals from the corresponding pair; duplicate outputs need not agree. |
| **D15 — Public legalization basis** | The finite rational legal grid uses the original public input basis; its error objective is the calibrated quadratic form. Section 59 keeps these roles separate in finite computation. |
| **D16 — Strict greedy comparison** | The exact codec retains a grid candidate precisely when every `Q_N^2` comparison is strictly greater than the rational squared threshold; equality is covered, with exact tie behavior. |
| **D17 — Full PSD tests** | Principal-minor pruning remains only a necessary prefilter. Full exact PSD tests for both `G` and `I-G` decide legality in all dimensions. |
| **D18 — Actual balls** | The size proof separates actual `d_N` balls using the proved comparison and uses their uniform volume. It does not posit a `Q_N` packing metric. |
| **D19 — Represented real inputs** | A real target requires a supplied representation giving certified approximation. The unknown-device learner supplies a legal rational estimate; neither interface assumes arbitrary real oracle input. |
| **D20 — Decoder class** | Payload optimality is for a fixed public deterministic decoder into legal memoryless binary effects. Positive success for each target forces the decoded family to cover. Interactive descriptions are not included in this converse. |
| **D21 — Finite enumeration evidence** | Complete scalar dictionaries, small matrix kernels and finite theorem-grid prefixes retain their exact scope. Current receipts identify which checks were executed; no full large-dimensional dictionary execution is inferred. |
| **D22 — Evidence boundary** | Written proofs establish continuum results and risk bounds. Builds and rendered checks establish reproducibility and layout, and finite tests establish the listed implementation contracts. |
| **D23 — Raw font warnings** | Engine font-expansion warnings and page-inspection conclusions are recorded separately. A rendered defect is assessed from actual page checks; compilation alone does not erase raw warnings. |
| **D24 — Unsigned provenance** | The reviewed final head is unsigned. No human authorship signature is inferred from it or from Actions; current publication metadata records its own signature status. |
| **D25 — Structural independence** | The structural companion's fresh repeatable nondisturbing classical probes retain their own assumptions and proof chain. They are not merged into the consuming quantum measurement model. |
| **D26 — The theorem package** | The article foregrounds closed-body finite-use geometry, exact entropy, common future-loss learning and public optimal-order coding, now with a sharp training-block resource law, finite-control realization and a joint dimension/accuracy law on a fixed full-dimensional interior. This describes the mathematical content without adopting a reduced journal objective. |

## 4. Complete crosswalk to the pipeline report's submission gates

These identifiers are local audit labels for the ordered items in frozen pipeline R51 Section 16. “Retained” refers to a written argument in the active source graph. Execution-dependent gates refer to their corresponding current receipts, and an open external human judgment is explicitly left open.

| Gate | Group | R51 request | Response and evidence |
| --- | --- | --- | --- |
| M01 | Mathematical | Complete endpoint calibration | Retained in Section 56 (`lem:matrixcalibration77`) and audited below: simultaneous lower-endpoint and complement Loewner control, plus the operator error needed for leakage. |
| M02 | Mathematical | Compression identity and leakage | Retained in `lem:matrixcompression77`; the exact positive leakage term and its upper bound are displayed, before applying the qubit learners. |
| M03 | Mathematical | First-rejection termination | Retained in Section 55: the first failed amplitude or phase guard terminates and returns the preceding accepted scale; every exceptional record has a defined legal output. |
| M04 | Mathematical | Conditional confidence | Retained in Section Section 55–56, including conditioning on the calibration record; Section 58 changes the public horizon and accuracy but preserves those ledgers. |
| M05 | Mathematical | Pair-assembly multiplicities | Retained in Section 56: each off-diagonal coordinate is taken from its own pair and each diagonal from a designated incident pair; no consistency of duplicate estimates is assumed. |
| M06 | Mathematical | Finite rational legalization | Retained in Section 56 in the original public basis; Section 59 explains finite algebraic comparisons and certified evaluation with slack. |
| M07 | Mathematical | Exact codec equality cases | Retained in Section 57: a candidate is retained only when every squared comparison is strictly above the exact rational threshold. |
| M08 | Mathematical | Actual-metric packing | Retained in Section Section 54 and 57: separated actual `d_N` balls, the triangle inequality for `d_N`, and their uniform measure bounds control cardinality. |
| M09 | Mathematical | All theorem ranges | Learning has an absolute small-error cap and eta<=1/8; fixed-dimensional entropy/payload uses delta<=delta_d; Section 58 states d>=2 and 1<=b<=N with a separate scalar case. Section 60 has delta<=2^-13; its sharp interior and one-use upper/lower laws use fixed failure 1/8. |
| P01 | Priority | Independent human expert review | OPEN EXTERNAL TASK. The supplied independent-review brief is a request, not a completed human opinion. Neither internal agents nor the AI-assisted R51 reports close this gate. |
| P02 | Priority | Direct Mele–Bittel comparison | Section 58 proves the one-call Choi/probe-class lower bound with collective processing. Section 60 imports the binary Mele–Bittel upper estimator, credits it explicitly, and proves a stronger interior future-loss analysis. The literature audit matches the actual access and normalizations. |
| P03 | Priority | Zambrano–Ramos-Calderer–Kueng comparison | The literature audit compares known-input acquisition, one-use loss normalization, confidence and dimension factors; the Section 58 corollary applies to the matched fresh one-call class. |
| P04 | Priority | Reanalysis of existing estimators under future loss | Section 60 gives a positive reanalysis: the existing binary Mele–Bittel estimator attains Theta(d^2 N delta^-2) at fixed confidence on I/4<=E<=3I/4, using a dimension-free interior metric comparison. Section 58 proves no uniform full-body linear-horizon guarantee for the same fresh one-call acquisition class. |
| P05 | Priority | Equivalent endpoint-log volume literature | The literature audit states the precise two-endpoint logarithmic exponent and its cited matrix-volume antecedents. A search/comparison does not certify universal priority; this question is included in P01. |
| P06 | Priority | Qualified optimal-learning language | Headlines specify ordered binary consuming classical-output effects, future-N loss, the training model, fixed-dimensional full-body optimality and the explicit d^4 upper factor. The joint d,N,delta interior law is identified separately at fixed confidence. |
| U01 | Resources | Separate all resources | `RESOURCE_LEDGER.md/json` separately charge calls, fresh-block cap, trusted preparation precision, arithmetic, quantum storage, reconstruction, workspace, and transmitted bits. |
| U02 | Resources | Finite exact codec terminology | The matrix codec is a terminating exact construction. Exhaustive dictionary reconstruction has no polynomial-time or optimal-workspace guarantee. |
| U03 | Resources | Incomplete construction cutoff | The retained implementation reports a cutoff as incomplete construction and emits no completed codebook or payload; a finite prefix remains a prefix. |
| U04 | Resources | Nonpublic headers | Dimension, horizon, tolerance, code convention and other public parameters are excluded only when shared publicly; any nonpublic header representation must be charged. |
| U05 | Resources | Encoding versus learning | A supplied legal matrix is the codec input. Unknown-device acquisition is a separate learner; their composition uses no further device calls. |
| V01 | Reproducibility | Exact-head read-only reconstruction | The predecessor's run verifies the predecessor only. Current source-freeze and final-head status are execution-dependent and are identified by the matching generated receipts. |
| V02 | Reproducibility | Source/PDF hashes and manifest | Frozen report identities are in `CONTROLLING_REPORTS.json`; current native/PDF/package identities belong to generated `evidence/SOURCE_HASHES.json`, `evidence/BUILD_RECEIPT.json` and publication evidence. |
| V03 | Reproducibility | Ordinary/optimized equality | The current comparison must be executed and recorded against current sources. The historical v77 result is retained with its own identity and is not reused as successor evidence. |
| V04 | Reproducibility | Raw warning wording | Raw font-expansion warnings and rendered layout findings are reported separately; no blanket warning-free claim is inferred from successful compilation. |
| V05 | Reproducibility | Optional cryptographic authorship | No cryptographic human authorship signature is supplied or inferred. The conditional suggestion to sign a release does not authorize signing as a person or make source reconstruction an authorship attestation. |
| V06 | Reproducibility | CI evidence boundary | CI reconstructs identified sources and artifacts and executes stated finite checks. It is not a proof certificate, independent priority judgment, or journal decision. |
| E01 | Editorial | Focused article primary | `quantitative.tex` produces the primary `paper.pdf`; journal-facing presentation foregrounds the current theorem chain. |
| E02 | Editorial | Structural companion separate | `structural.tex` produces `STRUCTURAL_PAPER.pdf`; its repeatable classical-probe assumptions remain independent of consuming quantum measurement learning. |
| E03 | Editorial | Complete edition archival | `main.tex` produces `COMPLETE_REVISION.pdf`, preserving the full proof corpus. Its size supplies no extra mathematical significance. |
| E04 | Editorial | Compact journal history | Detailed derivation, revision responses, provenance and A/B/C/D routing remain in repository audit materials; the focused article contains the mathematical dependencies it actually needs. |
| E05 | Editorial | Theorem objects before chronology | Presentation foregrounds geometry, entropy, common learning, public coding, the sharp fresh-block tradeoff, finite controls and the joint dimension/accuracy interior theorem; revision numbers identify source history. |
| E06 | Editorial | Concise scope paragraph | The introduction states the binary interface, fixed-dimensional full-body versus joint interior optimality, the exact-modulus limitation, finite reconstruction cost and independent status of the wider programme. |

## 5. Disposition of the ten risks in pipeline R51 Section 15

The report's severity assessments describe its reviewed v77 object. The following records what v78 changes and what remains a boundary; it does not overwrite the frozen assessments.

| Risk | Frozen assessment | Current response |
| --- | --- | --- |
| Risk01 | Independent priority — high | The four inherited theorem objects and new resource theorems have explicit comparison questions. Independent human expert priority assessment remains outstanding; R02/P01 is not closed by this author-side response. |
| Risk02 | Interface breadth — high for top four | The target remains the entire ordered binary effect interval. The new result distinguishes a continuum of training-resource classes within that interface; it does not assert multiple-outcome or residual-output theorems. |
| Risk03 | Growing dimension — high in the reviewed object | Section 60 now proves an all-dimensional Omega(d^2 N delta^-2) lower bound even under coherent adaptive training, and a matching fixed-confidence interior law using the existing Mele–Bittel upper estimator. The full-body d^4 upper factor and global entropy constants remain unmatched in growing dimension. |
| Risk04 | Exact distance — moderate | `Q_N` remains a comparison modulus. Section 58 proves an exact projective two-point distance for its hard family; this is not a general exact formula for arbitrary effects. |
| Risk05 | Computational efficiency — high | The codec is finite, exact and payload-optimal in its range. Dictionary enumeration, exact arithmetic, and workspace remain separate and may be very large. |
| Risk06 | Small-error/range — moderate | All learner, block, confidence, scalar and fixed-dimensional entropy ranges are stated individually. Small-error covering is not promoted to the full submaximal-error interval. |
| Risk07 | Physical resources — moderate in the reviewed object | Section 59 now proves robustness at the same loss and failure targets under finite trusted preparation/control specifications. The certified norm-error model does not optimize hardware, gate count, arithmetic, or preparation workspace. |
| Risk08 | Finite-regression overinterpretation — controlled | Finite checks establish their listed arithmetic/control-flow examples and replay contracts. Continuum laws and statistical risk follow from the written proofs. |
| Risk09 | Historical volume — controlled | The complete source corpus and predecessor audits are preserved as history. The focused article remains primary; successor page counts belong to its generated receipt. |
| Risk10 | Whole-program overclaim — controlled | All five aggregate analytic completion flags remain false; the detailed A/B/C/D gates are retained without substitution by finite-dimensional measurement results. |

## 6. Preservation and evidentiary conclusion

The preservation baseline is the complete qualified v77 source corpus: **330 native source files and 707 active complete-edition labels**. Current counts and permitted successor additions are checked by the v78 preservation machinery. The earlier v76 baseline was 296 native files and 658 labels; 557 labels was a v75 figure. No old count is used as a new mathematical verification.

The six audit/status/resource documents, frozen reports, retained predecessor documents and active theorem sources jointly make the revision reviewable. The proofs establish the stated mathematics; a successful final reconstruction establishes the identified build; an independent human priority report would establish its own specialist assessment. The remaining external task is R02/P01. Editorial acceptance, cryptographic human authorship and whole-program analytic closure are not recorded as obtained.
