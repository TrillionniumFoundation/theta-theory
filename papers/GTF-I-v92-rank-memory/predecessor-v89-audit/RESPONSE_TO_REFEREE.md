# Response to R58 external report and proof/pipeline audit — Revision 89

We thank the referee for the detailed validation of the conditional-fidelity and reset-width proofs and for identifying the precise provenance and memory-literature deficiencies. We retain the general mathematics journal objective, the discrimination topic and the complete inherited mathematical corpus. The referee's recommendation is frozen without being rewritten to imply approval.

The controlling object is remote v88 at `d1add4a7ba45230b3cba71b47ef46da5e4a88d72`; both R58 commits and file digests are recorded in `CONTROLLING_REPORTS.json`. A different local allocation draft also used the number v88 but was not pushed. We preserve that derivation separately and reconcile it here rather than falsely identifying it with the reviewed reset manuscript.

The mathematical response develops the policy cost singled out in R58. Section 80 proves matching fixed-profile orders for both independent groups and reset-constrained feedback, using a common unequal-signal readout. Section 81 proves a sharp hard quadratic-budget law, a conditional reset-preparation perturbation bound, and an explicit strict tester-level relation to the requested Ohst et al. class. All older section sources remain byte-identical and active.

## Required revisions

### R01 — Memory-constrained comparison

The current main-text comparison reads Ohst et al. Definition 6, Theorem 9, Definition 23, Theorem 24 and (65)–(68). Proposition memorycomparison89 proves inclusion of the two-call measure-and-reprepare class in unit-reset testers and a strict tester-operator witness. This separates a final tester-effect separability constraint from conditional fresh-state independence. It does not assert a score gap for every identical-channel ensemble or rule out other lifted formulations.

### R02 — Exact-head provenance

R58 is correct: the frozen v88 response overstated a directly triggered final-head run. RELEASE_PROVENANCE.md explicitly corrects that assertion. A separate read-only run 37322744298 has now reconstructed pinned v88 with verified_head d1add4..., but its trigger is v89 anchor 4f48db...; these identities are not equated. The v89 release specification requires its own actual final-head-triggered receipt. Its existence and success are determined by that receipt, never by this response or a YAML file.

### R03 — Conditional complete independence

The abstract, new introduction, Definition allocation89 and the budget theorem repeat that the whole fresh probe–reference/within-block-memory system is independent of all old receiver memory conditional on history. The preparation rule is common even at null histories.

### R04 — Receiver versus input memory

Receiver quantum storage and joint instruments remain unrestricted, while no old receiver subsystem may be coherently imported into a later acquisition. This distinction also drives the explicit comparison proposition.

### R05 — No dimension/depth identification

The new quantities are prescribed reservation sizes and hard pathwise sums of their squares. Neither reset width nor Q is called memory dimension or standard probe-marginal entanglement depth.

### R06 — Worst-path resources

All N_pi,Q_pi and B_pi definitions take suprema over formal terminal histories. Theorem quadraticbudget89 optimizes over hard N,Q caps; no average cost is substituted.

### R07 — Finite remainders

The new independent and reset upper proofs retain n*r*s² before Bures conversion; each GHZ group pays m*kappa*s² before the unequal-signal readout; the regular upper keeps the inherited N*s² term and absorbs it only with the explicit x²<=x/cap argument.

### R08 — Conditional executable

RESOURCE_BUDGET_SCHEMA.md and machine outputs distinguish arithmetic validation from physical reset, gamma and preparation-error certification. The inherited feedback verifier remains unchanged and is wrapped rather than relaxed.

### R09 — Local order versus distances

Both main theorems quantify over each fixed tube with constants uniform only in its public profile/budget and permitted remainders. The parallel/adaptive consequence remains local-order comparison; reset b=N equality remains a distinct exact class inclusion fact.

### R10 — Two scale intervals

Theorem allocation89 explicitly states that the sufficient legality interval s_* does not compute the discrimination interval s_0. Lambda_* remains sufficient and coarse.

### R11 — Distinct linear mechanisms

Opening uses the fixed impossible-label experiment with singleton blocks. Coherent tangency uses known-direction GHZ/correction and an unequal common readout. These are not conflated.

### R12 — Product converse scope

The independent product converse stays in its original class. Reset-profile upper bounds use the separate subnormalized conditional-fidelity argument, not the product converse or unconditional tensorization.

### R13 — Separate journal objects

Primary, current binary supplement, independent structural article and complete archive remain separate. New discrimination statements lead the abstract and introduction. No retained proof section is deleted.

### R14 — Wider programme boundary

The history audit records the whole deposited mathematical pipeline and the separate A/B/C/D order. The finite-dimensional measurement theorem promotes none of the five analytic aggregate flags.

### R15 — Independent priority

Not claimed completed. INDEPENDENT_REVIEW_BRIEF.md identifies the exact specialist questions. Current primary-source reading, finite tests and this author-side response are not an independent human opinion. The general mathematics journal objective and the referee’s recommendation are both retained without misrepresenting agreement.

## Detailed comments

### D01 — Common preparation

Definition allocation89 says one conditional map on every formal history, not equal hypothesis-dependent receiver states.

### D02 — Unrestricted receiver

Every new summary couples unrestricted storage with prohibition of coherent import.

### D03 — Reset endpoint

The inherited one-block explanation of reset b=N equals adaptive remains active; it is recalled in the comparison and response.

### D04 — Unit width

No equality with the product-reference class is asserted. The memory witness shows why receiver-retaining strategies require their own model.

### D05 — Positive operators

The reset-profile, policy and reset-defect inductions retain arbitrary positive subnormalized incoming operators.

### D06 — Countable histories

Sections 80–81 explicitly require trace-class direct sums and sum nonnegative branch quantities; no branch is normalized.

### D07 — Exact finite factor

The inherited (1-A+a)(1-a) induction is preserved verbatim. New upper bounds invoke it, not an exponential approximation.

### D08 — Public randomization

Public mixtures retain a common classical record and are handled by the same instrument/direct-sum framework.

### D09 — Within-block memory

The complete fresh system includes all quantum memory used by adaptive controls within that block.

### D10 — Environment inaccessible

All inherited Stinespring environment qualifications remain unchanged. The memory witness acts only on actually retained references and labels.

### D11 — Deficit refinement

Proposition policyprofile89 avoids the sqrt(n)<=n coarsening and retains the separate sqrt(r*N_pi) contribution.

### D12 — Q visibility

Proposition policyprofile89 is theorem-level, and Theorem quadraticbudget89 proves a matching budget-class local law. It deliberately does not claim a lower for each individual policy.

### D13 — Unknown remainder

The common unequal-signal readout and the GHZ events are fixed by E,H,Lambda and public scale/profile. Neither depends on F-E-sH.

### D14 — Opening witness

The singleton impossible-label witness is fixed throughout the tube and needs no feedback.

### D15 — Endpoint distinctions

The article separates exact reset/adaptive class equality at b=N from parallel/adaptive local-order comparison.

### D16 — Shared subtrees

RESOURCE_BUDGET_SCHEMA.md states the inherited feedback graph is a DAG and allows shared subtrees while checking all worst-path maxima. FEEDBACK_SCHEMA.md stays byte-identical with its earlier source.

### D17 — External gamma

The supplied majorant is not reconstructed from a channel pair. Its false flag is retained and separately repeated for reset defects.

### D18 — Finite memory tests

Old receiver-memory examples and the new explicit Bell tester are finite algebraic experiments; none is called synthesis of the general support code.

### D19 — Earlier dispatch

The failed and successful v87 verification histories are preserved as v87 history. Neither is counted as v88 or v89 final-head verification.

### D20 — Unsigned commits

No human signature is claimed. Git identities and page hashes are byte/provenance evidence only.

### D21 — Title

Finite-Use Discrimination Geometry of Ordered Quantum Measurements is retained.

### D22 — Learning subordinate

The new profile/budget theorems lead the primary. Retained learning remains in later sections with explicit supplement dependencies.

### D23 — Archive

The complete edition is labeled preservation material, not another journal contribution.

### D24 — Polynomial scope

Compressed integer budgets, represented support/profile arithmetic and affine repair remain distinct from quantum recovery/dictionary/readout synthesis.

### D25 — Feedback qualifier

New headings and summaries use reset-constrained feedback; no classification of all feedback architectures is stated.

## Pipeline acceptance gates

### Mathematical

M01. Complete fresh-system reset assumption: abstract, Definition allocation89 and both main statements.

M02. Subnormalized fidelity and null histories: unchanged Section 79 plus explicit applications in Sections 80–81.

M03. Full finite tube remainder: profilefinite89 and policyprofile89; no early asymptotic deletion.

M04. Canonical/horizontal factors: separate coherent/reset and regular arguments in both proofs.

M05. Policy Q: Proposition policyprofile89 and sharp budget-class Theorem quadraticbudget89.

M06. Integer saturation: both no-clipping and at-least-one-clipped cases in the profile lower.

M07. Two linear mechanisms: classical opening versus coherent encoded phase.

M08. Zero jets/higher order: inherited full-remainder restrictions retained, no zero-jet classification.

M09. Fixed-object constants: main theorem quantifiers and abstract.

M10. No exact-distance/exponent inference: all new conclusions are explicitly local orders.

### Priority

P01. Ohst comparison: current main text with Definition 23, Theorem 24 and (65)–(68).

P02. Constrained-separability relation: explicit proper tester inclusion, not class identification.

P03. HMNW/Yuan–Fung/GHPS: retained active main-text parameter and resource comparisons.

P04. Independent specialist review: still an external obligation, not marked complete.

P05. No search-based firstness: known methods credited and absence of a match not used as proof of priority.

### Editorial

E01. Reset-constrained classical feedback stated in the new models and prose.

E02. Complete probe/reference independence included in the abstract.

E03. Receiver storage and input coherent transfer distinguished.

E04. Primary, linked binary supplement and independent structural article separate.

E05. Complete edition remains archival.

E06. Learning consequences are secondary to discrimination.

E07. Hard pathwise resource bounds, not expectations.

### Reproducibility

R01. Frozen-v88 provenance corrected; separate pinned-v88 read-only reconstruction reported with actual trigger/verified identities.

R02. Exact final v89 check required on its actual triggering head; successful receipt, not configured YAML, supplies the status. The baseline status attachment is separately identified when present.

R03. Publication artifacts must be a direct child of qualified native source.

R04. All 28 suites run ordinary and optimized; previous receipts are not reused as current evidence.

R05. Physical reset, gamma, reset-defect calibration, continuum-proof and execution flags remain false.

R06. Unsigned status reported; no fabricated human signature.

R07. Failed v87 dispatch and successful v87 follow-up remain historical and distinct.

## Risk-by-risk response

K01 — **False product after feedback.** Controlled by conditional fresh append and receiver-instrument induction; independent tensorization is not reused.

K02 — **Shared reference.** Excluded across fresh complete acquisitions; permitted inside each block and within receiver processing.

K03 — **Receiver/input conflation.** Controlled by an explicit strict tester-level example and repeated no-import qualification.

K04 — **Expected resources.** All budgets remain hard worst-path quantities.

K05 — **Physical reset.** Not certified by these finite executables; independent physical certificate needed.

K06 — **Local coefficient.** Gamma remains an external verified-majorant hypothesis, not inferred from JSON.

K07 — **Finite remainders.** Written upper/lower formulae retain all nrs²/mκs²/Ns² terms.

K08 — **Global overclaim.** No uniform arbitrary-pair covariance equivalence or boundary entropy is inferred.

K09 — **All-feedback overclaim.** Only the exact reset model is classified by profile and Q.

K10 — **Known mechanisms.** QEC, GHZ, fidelity, semidefinite geometry and squared-group principles are credited.

K11 — **Priority.** Direct Ohst omission addressed; independent human priority assessment remains outstanding.

K12 — **Computation.** No exact distance, optimal recovery or general circuit synthesis is claimed.

K13 — **Regression.** Finite tests are not universal proofs or physical executions.

K14 — **Provenance.** Old v88 overstatement corrected; current exact-head success must be read from its new external receipt.

K15 — **Signature.** No human signature supplied.

K16 — **Editorial size.** All old proof text retained; new central theorems lead the article; archive and supplement remain distinct.

K17 — **Growing outcomes.** The inherited fixed-k learner does not close growing-k minimax dependence.

K18 — **Whole programme.** Five independent analytic aggregate flags remain false.

## Present evidentiary boundary

This is an author-side mathematical revision and literature comparison. It does not supply an independent human priority judgment, a verified human signature, a physical reset or gamma calibration, or an acceptance decision from a journal. New source-bound and actual-final-head receipts must independently establish each claimed execution stage. No prior successful build is recycled as evidence for changed source.
