# Response to the R54 external report and proof/pipeline audit — Revision 85

We thank the referee for the detailed verification of the support-kernel, finite-angle and transported-ridge arguments, and for the specific requests concerning primary-text dependencies and priority. We retain the general mathematics journal objective. Neither the referee's recommendation nor any previous mathematical statement has been rewritten to suggest approval.

The controlling object is completed v84 at `9ee14476f539a38f2f45f9bd4ed99a658a7eb14d`; the external report is commit `e96b4d271e60ec636e1e6022d1708b755a9e4d4a` and the audit is `57d23a10cb08171b2ab23464fca8ba89e808f253`. Their full texts and digests are supplied. The new mathematical sections are 72–74; all prior mathematical sections remain byte-identical.

The response has three substantive parts. First, a new finite Bernoulli lemma and a human dependency map make the main support/discrimination proof independently readable. Second, the support criterion now classifies every fixed two-sided C2 measurement curve with nonzero first derivative, including second-order rank openings, using a normalized horizontal surrogate and an actual corrected-channel Taylor bound. Third, a certified implementation-error ledger quantifies which approximate controls preserve the finite-use linear lower. The full primary text of arXiv:2609.39280v1 is now compared theorem by theorem. We distinguish that author-side work from the independent human priority assessment still not supplied.

## Required revisions
### R01 — Update covariant learning

Completed the full-text comparison in `editions/current-comparison85.tex`. It states Theorem 7, Corollary 9, Theorems 12–13, 15 and 18 with models, losses, parameter definitions, query architecture and gate scope. In particular the general diamond lower has exponent xi/2, not an invented inverse-square optimum. `LITERATURE_RETRIEVAL.json` pins the successful primary-text retrieval.

### R02 — Independent priority

Not represented as completed. `INDEPENDENT_REVIEW_BRIEF.md` specifies the specialist questions and the exact new theorem package. An author-side primary-source comparison and this revision cannot supply an independent human opinion.

### R03 — Novelty immediately visible

The introduction after the orbit formula and the discussion immediately after the new curve theorem credit the established Zhou–Jiang exponent criterion and Knill–Laflamme correction mechanism. The additions are a complete support-coordinate first-jet classification, a direct finite-angle C2 proof through rank openings, and explicit control-error accounting.

### R04 — Arbitrary-pair scope

The complete-body midpoint theorem remains a one-sided upper. The new matching result is for every fixed two-sided C2 curve with nonzero first derivative, with curve-dependent constants. No uniform midpoint equivalence or full-body entropy is inferred.

### R05 — Fixed-object constants

The abstract, introduction, curve theorem and README explicitly state fixed-orbit or fixed-curve constants and interval. The proofs exhibit dependence on curvature, tangent, support eigenvalues and the support-complement gap.

### R06 — Output processing

The introduction repeats that processing may stationarize a moving square-root orbit and cannot turn it into a linear orbit when it remains nonconstant. The unchanged support inclusion and transported-weight theorem are the precise statements.

### R07 — Finite Bernoulli premise

Added `lem:bernoulli85` with a complete finite proof in the primary. The universal 1/128 bound includes endpoints, and the two-sided nonzero-derivative endpoint explanation is explicit. The inherited stronger binary lemma remains preserved in the supplement.

### R08 — Pair versus common learning

The new code uses the known base measurement and its support generator Gamma. It is used only for pair discrimination. The common learner and its public advice, call and confidence conventions remain separately stated and unchanged.

### R09 — Ideal controls

The ideal-control existence statement is retained. New `thm:controlstability85` additionally proves a conditional implemented-control theorem with uniform diamond error allowances under both hypotheses. It does not assert a synthesized circuit or physical execution, nor fixed-noise robustness as t tends to zero.

### R10 — Computational scope

New `prop:curveexact85` adds a polynomial exact first-order decision on represented rational input. The covariance evaluator, support projection and affine repair remain polynomial; dictionary construction, general recovery synthesis and collective-readout synthesis are separate and not upgraded.

### R11 — Growing outcomes

The balanced learner still has a displayed k^3 upper and a binary-subfamily lower. Fixed-k sharpness is retained; no joint growing-k classification is asserted.

### R12 — Primary/supplement map

Added the human-readable table in `editions/operational-introduction85.tex`. Core support/orbit/curve proofs have all probability, covariance and correction premises in the primary. The learning consequences cite exact supplement labels. The noisy-projector auxiliary consequence is identified separately.

### R13 — Proof versus regression

All test summaries preserve continuum-proof and physical-execution false fields. The new 313/17 suite covers exact local algebra, first jets, finite product laws and error budgets. The general curve and recovery theorems are written proofs, not claims derived from samples.

### R14 — Fresh release identities

The response branch starts at the exact reviewed v84 final head. All altered source is requalified in the v85 native object; publication must directly inherit it; the final exact HEAD is reconstructed read-only. Old v84 successes are provenance only, not v85 verification.

### R15 — Independent analytic programme

All five aggregate flags remain false. The history audit preserves the precise A/B/C/D ordering and states why finite-dimensional measurement geometry supplies none of those independent analytic gates.

## Detailed comments

### D01 — Real spaces

The support generator, kernel parameters and all orthogonal complements are real Hermitian spaces; the factor perturbation is complex rectangular. The distinction is repeated at dimension and range calculations.

### D02 — Span not algebra

The primary retains the warning that the support span contains full support blocks, need not be an algebra, and differs from the effect span at higher rank.

### D03 — Zero effects

Zero supports use P=0. The new first-jet test forces H=0 on a zero effect, as required by two-sided positivity; second-order openings remain allowed.

### D04 — Non-Hermitian mean

The original B+iA decomposition is unchanged. New pairings use that complete kernel rather than replacing the covariance mean by a Hermitian one.

### D05 — Injectivity

The original common-Hermitian-equals-iA argument is retained verbatim.

### D06 — Range

Both original and new criteria use finite-dimensional self-adjointness and full-kernel orthogonality; no analytic closed-range assumption is introduced.

### D07 — Stationary generator

The new first-jet lemma explicitly derives G in W_E for stationary unitary generators. It separately refuses stationarity inference from H=0 for nonunitary curves.

### D08 — Product lower

The lower in the square-root branch uses one fixed input, one label event and repeated product observations; no entanglement is needed for that lower.

### D09 — Probability endpoint

The main-text Bernoulli section explains the local two-sided minimum/maximum obstruction to a nonzero probability derivative at endpoints.

### D10 — Recovery output

Both old and new code recover from the available classical label and retained reference only.

### D11 — Complete Kraus span

The primary comparison retains the full within-label support-block Kraus-product span. The new normalized-factor proof keeps all Kraus rows, not only effect coordinates.

### D12 — Flags and dimension

Orthogonal flags and the per-call 2d reference bound remain. This is not a compiled circuit-size bound.

### D13 — Recovery completion

The exact CPTP completion is retained. The general-curve derivative explicitly uses recovery completeness, making it a genuine channel before Taylor expansion.

### D14 — Logical gap

The new gap is ||Z||HS²/tr Z_+ for Z=Gamma-Pi_W Gamma. It is positive for the linear branch but nonuniform near the support span.

### D15 — Derivative identities

The proof writes R_l L_mu J=c_lmu I and sums the adjoint/completeness identity explicitly to obtain -i Gamma_L. It differentiates a first-order surrogate, not an assumed smooth exact root of the actual curve.

### D16 — Diamond constants

The original orbit constant four remains. The general curve uses kappa=L/2+2||Gamma||op² from two Taylor remainders; constants are not claimed sharp.

### D17 — Composition

Every accumulated error is channel telescoping, without independence.

### D18 — Integer calls

The new proof records floor(1/(|t|Delta))>=2 before taking the minimum with N and the half-truncated-scale bound for x.

### D19 — Sign

All local estimates use |t| or t² and are valid on the stated two-sided interval.

### D20 — Full rank

A positive-definite component still makes W_E all Hermitian matrices. New regression includes full-rank first jets, while rank-opening curves show why the base support, not nearby full rank, governs the fixed-base first-order law.

### D21 — Rank one

The rank-one informational-completeness corollary and its higher-rank caveat are unchanged.

### D22 — PVM

The original PVM commutant criterion is preserved. The new binary rank-opening example starts at a PVM and has a linear nonunitary finite-use law.

### D23 — Positive support sums

The noncommuting support-inclusion proof is unchanged; no commuting shortcut is substituted.

### D24 — Extended energy

The variational definition with infinite values and zero transported weights remains unchanged.

### D25 — Transported weights

The same tau and Tw are essential and retained. No freshly uniformized ridge is declared monotone.

### D26 — Uniform ridge

The exact coefficient k/N remains; the Euclidean ridge is I/N on the zero-sum tangent.

### D27 — Projection matrices

The first-jet implementation reuses real coordinate rank selection followed by Hilbert–Schmidt Gram projection; it does not confuse the two systems.

### D28 — Caps

The exact first-jet and inherited support certificates reject a cap violation before computing or emitting a partial classification.

### D29 — Human dependency map

The new main-text table distinguishes actual supplement premises from preserved auxiliary material and separates the structural article.

### D30 — Strongest message

The article now presents the support kernel together with a finite-pair classification for every fixed two-sided C2 effect curve with nonzero first jet, including second-order rank changes, and certified control budgets. It credits the established metrological mechanism and does not claim optimal general POVM learning.

## All proof/pipeline acceptance gates

| Gate | Requirement in R54 | Current response |
|---|---|---|
| M01 | Exact covariance variance identity active | Retained Section 67 and its variance/factorization proof, unchanged. |
| M02 | Complete singular kernel | Retained full Section 69 kernel, all support and missing-support blocks. |
| M03 | No effect inversion at boundary | The original kernel uses no inverse. The new realizability proof explicitly inverts only the fixed positive support, never a singular effect on the full space; its rational decision uses projectors only. |
| M04 | Real-space dimension conventions | Real Hermitian dimensions and complex factor spaces explicitly distinguished. |
| M05 | Range criterion from complete kernel | New Gamma criterion proved by pairing with the complete kernel, not an ansatz. |
| M06 | Comparison scale not confused with lower bound | The surrogate upper and corrected-channel lower are separately proved before the classification conclusion. |
| M07 | Square-root lower valid locally | New self-contained finite Bernoulli lemma and endpoint explanation in the primary. |
| M08 | Recovery uses accessible systems | Actual label and retained reference; no inaccessible device system. |
| M09 | KL products complete | Full Kraus-product span retained; new derivative sums all Kraus rows. |
| M10 | CPTP recovery completed globally | CPTP completion retained and used in the derivative calculation. |
| M11 | Finite-angle remainder explicit | General curve remainder kappa t² and m kappa t²; old orbit remainder unchanged. |
| M12 | Integer-call bookkeeping | Floor bound and two-sided small-angle caps are explicit. |
| M13 | Nonuniform constants visible | Constants and interval explicitly fixed-curve in abstract, introduction, theorem and README. |
| M14 | Processing statement precise | Stationarization caveat repeated; no square-root-to-linear conversion for a nonconstant processed orbit. |
| M15 | Transported ridge not fixed-ridge overclaim | Same tau and transported weights remain, including singular extended values. |
| M16 | Exact arithmetic scope | New exact rational first-order decision, cap rejection and replay; no unrepresented-real or hardware oracle. |
| M17 | Arbitrary-pair boundary limitation | Not claimed closed. New local C2 matching theorem does not imply uniform arbitrary-pair covariance equivalence. |
| M18 | Growing-`k` minimax | Not claimed closed. Fixed-k learning scope and k³ upper remain. |
| P01 | Independent specialist opinion | Independent human specialist opinion remains outstanding; a concrete revised brief is supplied. |
| P02 | HNKS/QEC attribution | Zhou–Jiang and Knill–Laflamme credited in the introduction, immediately after the new theorem, and in the current comparison. |
| P03 | Exact novelty boundary | New support/first-jet/finite-angle proof distinguished from established exponent and QEC principles. |
| P04 | Current covariant-learning comparison | Full text retrieved and read; current primary compares exact theorem statements and losses, including nonmatching diamond epsilon exponents. |
| P05 | Fisher/frame distinction | State Fisher/frame versus varying-measurement tangent models remain distinguished. |
| P06 | Operator-valued kernel distinction | Kernel embedding/effect span versus full support-block span remain distinguished. |
| P07 | No firstness inference from search | No firstness inferred from a targeted search or build. |
| E01 | Focused primary | Focused primary expanded only for the new proof chain and necessary premise; cumulative binary material stays in its separate supplement. |
| E02 | Complete current supplement | Complete supplement and its 307 labels preserved unchanged. |
| E03 | Structural article separate | Independent structural source graph unchanged. |
| E04 | Archive not journal object | Complete edition remains the active mathematical preservation object, not an additional journal submission. |
| E05 | Human-readable prerequisite map | Added a human-readable main-text prerequisite table. |
| E06 | Pair discrimination separated from learning | Known-pair code and controls never used as uncharged advice for common learning. |
| E07 | Resource distinctions centralized | Central current resource ledger distinguishes first-jet input, full curve constants, ideal/implemented controls, queries and payload. |
| E08 | Main theorem novelty phrasing | Known-principle attribution and the new finite-C2 scope placed at the first theorem discussion. |
| V01 | Exact native/publication/final chain | This revision requires its own native-source, direct publication and exact final-head chain. |
| V02 | Current source qualification | Fresh v85 source qualification required; actual result resides in its new build receipt. |
| V03 | Exact final-head read-only reconstruction | Fresh exact-final-head read-only reconstruction required; no v84 receipt reused. |
| V04 | Four current documents reconstructed | All four current source graphs are rebuilt and page-checked. |
| V05 | Current exact suites | 23 suites run ordinary and optimized, including all 22 predecessors. |
| V06 | No unresolved references/citations | Builder rejects unresolved references/citations and bad boxes in each current document. |
| V07 | Finite-test scope flags | All new schema outputs separate finite replay, continuum proof and physical execution. |
| V08 | Resource-cap rejection | New and inherited resource caps reject instead of returning partial certificates. |
| V09 | Signature status | No independently verified human signature is claimed; commit identity is only provenance. |


## Risk register

| Risk | Subject | Current treatment |
|---|---|---|
| K01 | Known-principle novelty | Prior exponent/QEC mechanism explicitly credited; new C2 finite-pair proof and support coordinates identified without firstness claim. |
| K02 | Full-boundary overstatement | Local curve matching is not arbitrary-pair midpoint equivalence or a full-body entropy theorem. |
| K03 | Nonuniform orbit constants | All comparison constants and intervals remain fixed-curve and may degenerate. |
| K04 | Pair-versus-common resources | Pair-dependent code remains separate from unknown-device common learning. |
| K05 | Ideal controls | Conditional uniform diamond-error robustness is now proved; synthesis and hardware execution remain unclaimed. |
| K06 | Processing prose | Stationarization caveat retained; no erroneous strictly moving conclusion. |
| K07 | Linked-document opacity | Main-text finite Bernoulli proof and human dependency map remove the core hidden supplement dependency. |
| K08 | Current literature | Full current primary text retrieved and read, with exact loss, query and gate comparisons. |
| K09 | Computation overreach | Polynomial first-jet decision does not compute adaptive distance or synthesize controls. |
| K10 | Regression overreach | Exact tests explicitly marked finite; no physical protocol executed. |
| K11 | Growing outcome | Growing-k minimax remains unmatched and visible. |
| K12 | Wider programme | All five A/B/C/D aggregate flags remain false. |
| K13 | Signature | No human cryptographic authorship inference from reconstruction. |
| K14 | Journal significance | The general-journal objective is retained; acceptance and independent significance judgment are not asserted by the author-side revision. |

## Release and evidentiary status

The primary, current supplement, independent structural article and complete edition are separate rendered objects. Source preservation is checked from `V84_BASELINE.json`; original altered entry files are retained. Source and final-head qualification are separate, fresh v85 operations. Their actual success or failure must be read from the new receipts and Actions runs, not inferred from this source response. No independent human priority clearance, physical recovery execution or journal approval is claimed.
