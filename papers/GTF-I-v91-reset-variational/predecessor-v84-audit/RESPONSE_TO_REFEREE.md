# Response to the referee — General Theta Foundations I, Revision 84 (R53)

We thank the referee for the detailed assessment of the normalized-tuple covariance and the affine legalizer. We retain the requested four-leading-general-journal objective and the paper's measurement topic. Rather than treating an editorial recommendation as a mathematical obstruction, this revision gives selected new proofs and a substantially more focused journal object. We do not edit the report's recommendation or represent the referee as endorsing this revision.

The controlling objects are the two R53 reports on completed v83 at `58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7`, frozen verbatim in this directory. The principal new section files are 69–71. The previous complete-body upper, balanced learning and all binary boundary results retain their statements and proof text. All 495 native predecessor files and all prior label graphs are accounted for; the quantitative graph is preserved in the explicit union of the current primary and binary supplement.

## Principal mathematical response

The covariance kernel now has a complete support-based real-linear parameterization and an exact dimension formula. The unitary tangent is in the covariance range exactly when its generator belongs to the measurement Kraus-product support span. This yields a directly proved finite-angle trichotomy on **every fixed unitary orbit**: stationary, square-root, or linear accumulation. The linear lower has an explicit corrected-channel remainder and uses only the actual output and an external reference. The underlying metrological Kraus-span criterion and error-correction principle are credited to prior work; they are not claimed new.

A public scalar-measurement covariance supplies a separately defined regularization that contracts under arbitrary stochastic output processing when its weights are transported. This addresses the fixed-ridge caveat without falsely promoting the old fixed Euclidean ridge. Exact rational support decisions are polynomial. General entropy-optimal dictionaries, growing-k minimax and arbitrary readout synthesis remain distinct from these statements.

## R53 required revisions

| Item | Referee issue | Response | Location |
|---|---|---|---|
| R01 | Separate objects | The primary quantitative article and its complete binary supplement form one proof package. The structural article is independent and unchanged. The complete edition is archival. | `quantitative.tex; supplement.tex; structural.tex; main.tex` |
| R02 | Independent specialist priority | No human clearance is claimed. The expert brief is updated; the established HNKS and error-correction criteria are explicitly attributed. | `INDEPENDENT_REVIEW_BRIEF.md; sec:comparison84` |
| R03 | Global upper scope | All arbitrary-pair complete-body claims remain upper certificates. The new two-sided result is restricted precisely to each fixed unitary orbit. | `eq:frontupper84; thm:orbittrichotomy84` |
| R04 | Current theorem comparisons | Full primary-text comparisons cover Fisher/frame information, kernel embeddings and adaptive channel discrimination. Zhou–Jiang is added as a direct prior criterion. Only the announced covariant-learning result was retrieved; its full-text comparison remains outstanding rather than fabricated. | `sec:comparison84; LITERATURE_AUDIT.md` |
| R05 | Kernel caveat | The caveat is strengthened into a complete real-linear kernel parameterization and exact dimension formula. Nonprojective measurements can have nontrivial kernels. | `thm:supportkernel84` |
| R06 | Two processing statements | The inherited unregularized theorem is retained. A separate transported-weight ridge contracts under arbitrary stochastic output processing; this is not a fixed Euclidean-ridge claim. | `thm:transportedridge84; prop:ridgeupper84` |
| R07 | Crossover scope | The earlier noisy projector family retains its fixed-k d=2 range. The new orbit theorem supplies matching finite-angle scales for every fixed E,G, with nonuniform E,G-dependent constants. | `thm:noisecrossover83; thm:orbittrichotomy84` |
| R08 | Pair geometry versus learning | The correction recovery is designed for known E,G and common to both hypotheses. It is not handed to the unknown-device learner. | `rem:orbitresources84; RESOURCE_LEDGER.md` |
| R09 | Growing outcome gap | The abstract and introduction display fixed-k sharpness and the k^3 upper. No growing-k equality is asserted. | `quantitative.tex abstract; sec:introduction84` |
| R10 | Algorithmic language | Polynomial claims concern rational support decisions, covariance evaluation and affine legalization only. Dictionary, arbitrary recovery/readout synthesis and physical execution remain separate. | `prop:supportexact84; SUPPORT_SCHEMA.md` |
| R11 | Compress the article | The primary is reduced to a focused covariance/support/orbit narrative with balanced learning consequences. All old binary proofs remain active in the current supplement, with reconstructed cross-document references and a machine-checked relocation list. | `supplement.tex; PRESERVATION_MANIFEST.json` |
| R12 | Centralize resources | One ledger distinguishes horizon, calls, index bits, public reconstruction, trusted controls, synthesis and implementation error. Ideal orbit recovery is expressly separate from actual-control common learning. | `sec:introduction84; RESOURCE_LEDGER.md` |
| R13 | Every-record quantifiers | Inherited total fallback and bounded stopping remain unchanged. New lower protocols use deterministic m<=N, and all upper estimates allow the full stopped class. | `thm:orbittrichotomy84; thm:affinerepair83` |
| R14 | Signed release if available | No authorship key or independently verified signature was supplied. No signature or signed archival release is invented. Source and exact-head receipts report actual identities only. | `PROOF_STATUS.json; exact-head workflow` |
| R15 | Independent analytic programme | No A/B/C/D aggregate is promoted by the finite-dimensional measurement results. All five flags stay false and the dependency ordering is retained. | `HISTORY_AND_PIPELINE_AUDIT.md; PROOF_STATUS.json` |

## R53 detailed comments

| Item | Comment | Treatment |
|---|---|---|
| D01 | Adjoint in covariance | The original S* term remains byte-identical in section 67; support proofs use S=B+iA rather than assuming S Hermitian. |
| D02 | Real Hilbert space | The support span, covariance, Gram projection and orthogonality are explicitly over Hermitian matrices as a real space. |
| D03 | Projection factorization | The complete original factorization proof precedes the new kernel analysis in the primary article. |
| D04 | Zero operator versus null direction | The support parameterization and nullity formula distinguish these notions at every rank. |
| D05 | Interior differentiation | Original gauge differentiation and boundary approximation remain unchanged; new support identities never differentiate a singular square root. |
| D06 | Inaccessible environment | The new recovery acts on the actual classical label and retained reference. No dilation environment is provided to the tester. |
| D07 | Common tester | The finite-angle lower uses one base recovery under both hypotheses; adaptive optimality is not replaced by a nonadaptive claim. |
| D08 | Residual is algebraic | The original path proof and residual convention are unchanged. |
| D09 | Midpoint ridge scaling | Original first-half scaling remains in section 67 without shorthand. |
| D10 | Binary factor two | The exact restriction and original regression remain unchanged and active. |
| D11 | Stochastic convention | Column-stochastic T is stated in both new support-processing and transported-ridge theorems. |
| D12 | Infinite energy | The extended regularized dual energy is infinite off the range, including zero-weight boundary cases. |
| D13 | Reference-preserving reduction | The original noisy-family proof stays intact; the new Kraus-product code separately proves reference-preserving correction. |
| D14 | Noise endpoints | Earlier epsilon=0 versus epsilon>0 statements retain their ranks and ranges; no uniform orbit constants across this limit are asserted. |
| D15 | Crossover constants | Original numerical constants are retained and not called optimal. New orbit constants are also not optimality constants. |
| D16 | Certificate meaning | The new certificate decides support membership and a local orbit regime. It computes neither D_N nor an optimal tester. |
| D17 | Gram matrix | Orthogonal generator projection uses an exact Hilbert–Schmidt Gram system; real coordinates are used only for rank. |
| D18 | Exact PSD/ranks | Input validation and support calculation use exact rational elimination and PSD predicates; no tolerance cutoff is substituted. |
| D19 | Affine repair scope | Balanced legalization remains its own retained elementary theorem, not a general convex projection claim. |
| D20 | Uniform fallback | Every-record legality of the inherited learner is retained unchanged. |
| D21 | Dictionary independent | The support decision and affine map do not construct an entropy-optimal dictionary. |
| D22 | Mele–Bittel substitution | It remains a sufficient upper and not a suboptimality result for the source estimator. |
| D23 | Single-copy versus coherent | The comparison keeps the cited single-copy access and the present coherent future-use lower distinct. |
| D24 | Known symmetry | Known symmetry is explicitly stated; no full-text theorem or runtime separation is attributed to the unavailable text. |
| D25 | Structural independence | No structural theorem is a premise for covariance, support, or orbit proofs. |
| D26 | Archive not competing paper | The complete edition is labeled preservation only; the primary and supplement are the quantitative reading object. |
| D27 | Finite exact evidence | The exact BB84 code calculation is a symbolic example, not proof of the universal theorem or a physical experiment. |
| D28 | Current exact head | New source and exact-head workflows are revision-specific and cannot reuse v83 success as v84 qualification. |
| D29 | Five false flags | All five independent aggregate fields remain false, checked by the builder. |
| D30 | Focused contribution | The principal narrative is normalized covariance, complete support kernel and finite-angle orbit scales, with transported regularization and retained learning consequences. |

## Proof-pipeline acceptance gates

The 28 gates below retain their mathematical, priority, editorial and reproducibility distinctions. Addressing a gate does not mean fabricating its external completion.

### Mathematical

| Gate | Requirement | Status and treatment |
|---|---|---|
| M01 | Complete-body one-sided | Global arbitrary-pair upper versus fixed-orbit two-sided theorem are separated. |
| M02 | Factorization | Section 67 is unchanged and actively loaded. |
| M03 | Kernel caveat | Complete parameterization and dimension, not a false positive-definiteness claim. |
| M04 | Interior/boundary | Original limiting proof remains active. |
| M05 | Reference/memory | Model definition and actual-output recovery retain these quantifiers. |
| M06 | Processing types | Transported weights are essential; original Euclidean ridge not promoted. |
| M07 | Crossover ranges | Old noisy d2 family and new fixed-orbit interval are different statements. |
| M08 | Gram matrix | Exact support projection and inherited covariance system use their correct Gram matrices. |
| M09 | Fallback | The balanced learner remains total on exceptional records. |
| M10 | Growing-k | Gap stays visible in abstract and first theorem discussion. |

### Priority

| Gate | Requirement | Status and treatment |
|---|---|---|
| P01 | External specialist | Uncompleted; no human review is asserted. |
| P02 | Fisher/frame geometry | Theorem 1 of the primary text is compared. |
| P03 | Operator-valued embeddings | Theorem 3.6, Definition 3.7 and Remark 4.4 are compared. |
| P04 | Adaptive discrimination | Version 3 section IV is compared; no QFI-only finite lower is inferred. |
| P05 | Closest-theorem record | The support/Kraus-span identity and Zhou–Jiang prior criterion are explicit. |
| P06 | Firstness | No historical-firstness language or independent clearance is introduced. |

### Editorial

| Gate | Requirement | Status and treatment |
|---|---|---|
| E01 | Separate structural article | Independent source graph and PDF retained. |
| E02 | Shorten quantitative article | Separate current binary supplement, not deletion. |
| E03 | Self-contained dependency package | Current TeX cross-references and standalone reconstruction include both files. |
| E04 | Central resources | Unified ledger and first-section resource paragraph. |
| E05 | Separate provenance | R53 crosswalks live outside journal prose. |
| E06 | Principal contribution | Support kernel and finite-angle orbit theorem lead the argument. |

### Reproducibility

| Gate | Requirement | Status and treatment |
|---|---|---|
| V01 | SHA chain | Native source, direct-child publication and metadata-only final head are pinned. |
| V02 | Read-only verification | Exact final HEAD is rebuilt independently. |
| V03 | Fresh receipts | All 22 suites and four documents are current-run evidence. |
| V04 | Finite evidence scope | Machine-readable flags deny continuum proof/physical execution. |
| V05 | Resource caps | Exceeded cap rejects without a partial certificate. |
| V06 | Signature | No key supplied; no signature claim. This item remains conditional. |

## Ten audit risks

| Risk | Name | Current treatment |
|---|---|---|
| K01 | Full-boundary overstatement | Controlled by distinguishing arbitrary-pair upper from fixed-orbit classification; full-boundary entropy remains open. |
| K02 | Priority | HNKS/correction prior art is credited; independent specialist and newest full-text comparison remain open. |
| K03 | Growing-k | The k^3 gap is explicit. |
| K04 | Architecture | Primary/supplement split substantially reduces the journal-facing article while preserving all proofs. |
| K05 | Computational scope | Support decision and legalization polynomial; general synthesis not claimed. |
| K06 | Interface | Classical output, consuming input, memoryless device; references are external. |
| K07 | Boundary kernel | All null directions are parametrized; nonprojective degeneracy retained. |
| K08 | Processing | Only transported-weight regularization has the new contraction property. |
| K09 | Evidence | Exact run/commit checks and source preservation; no unsigned-as-signed interpretation. |
| K10 | Whole programme | All independent analytic aggregate flags remain false. |

## Proof and evidentiary boundaries

The new orbit theorem has constants and an angle neighborhood depending on the fixed measurement and generator. It supplies matching actual finite-use trace-distance orders on that family; it does not establish a two-sided midpoint formula or entropy law for arbitrary full-boundary pairs. The code is pair-dependent, with ideal trusted controls, and is not a common estimator. The exact BB84 recovery computation is a finite symbolic identity, not general physical execution.

The final source-qualified receipt and exact-head read-only run are the authorities for current execution status. Before those runs complete, this response is a native mathematical revision, not a self-qualifying build certificate. The primary, current supplement, unchanged structural article and complete edition are all reconstructed from native sources. Independent human priority clearance and a genuine authorship signature are not supplied by this workflow. The announced known-symmetry paper still requires an independently obtained full-text comparison. These external limitations do not change the proved hypotheses or the retained journal objective.
