# Response to R57 — General Theta Foundations I, Revision 88

We thank the referee for the detailed assessment of the finite block upper, corrected parallel acquisition, and unknown-remainder quantifiers. We retain the general mathematics journal objective and the paper's subject. The recommendation in the actual report is not rewritten as an approval. No previous mathematical statement is deleted to avoid a criticism.

The controlling reviewed publication is `aab076189b7276f6a0b4113b472ea09a7ac640cc`, with native source `d4fc44a02ee0585bf9da899239c3f976d75cc9cf`. The external report is at `796657054bac22426f33520474e4b6020892ee32`; the pipeline audit is at `0546af1e2f9caebbbc29376e9eee192440f2e1a2`. Both full reports were read through authenticated repository retrieval and are pinned by Git blob in `CONTROLLING_REPORTS.json`. A local byte-for-byte copy of those two new reports is not claimed. All previously frozen reports remain in the retained source corpus.

The substantive addition is a theorem for **every prescribed allocation of independent complete probe–reference groups**, with coherent local rate `min(1,s sqrt(sum n_r²))`. This refines a largest-width budget to the resource actually allocated. The lower uses one bounded classical readout for unequal independent signals and the whole unknown-remainder tube. No logarithmic loss from grouping sizes is introduced. The main text also supplies the exact HMNW/Yuan–Fung comparison, distinguishes the block-i.i.d. taxonomy, and repeats the scope and finite-error conventions.

## Required revisions

### R01 — Channel-Bures comparison

Addressed in `editions/channel-bures-comparison88.tex`. Theorem 17 and Remark 18 of HMNW identify the generic parallel inequality and its Yuan–Fung antecedent; Theorem 19 supplies the different adaptive upper. An explicit fixed-gauge substitution recovers the surrogate `3 beta_0 n s/2` estimate, and the actual tube's `n r_0 s²` diamond remainder contributes `s sqrt(r_0 n)` in Bures distance. The new profile theorem adds a matching common lower and unequal-allocation quantifiers, not a new generic fidelity principle.

### R02 — Block-i.i.d. comparison

The resource-model comparison is now in the primary, based on the retrieved primary arXiv abstract of Ghosal–Halder–Patra–Sen. Their fixed-size identical blocks and composite asymptotic Stein problem are distinguished from our unequal independent complete groups and finite shrinking simple-pair separation. Full-text attempts failed in this connection; theorem numbers, constants and theorem-level novelty exclusions are not invented. A complete specialist priority comparison of that paper remains pending.

### R03 — Independent specialist priority

Not supplied or represented as complete. `INDEPENDENT_REVIEW_BRIEF.md` identifies the support-kernel, finite-tube, complete allocation-profile and nonempty-realization questions, including equivalent metrological formulations. The current author-side mathematical and bibliographical work cannot substitute for an independent specialist opinion.

### R04 — Parallel/adaptive local orders

The abstract, introduction, profile theorem discussion and resource ledger all say local orders. Neither exact distances nor globally optimal tests, perfect discrimination thresholds or fixed-pair error exponents are equated.

### R05 — Complete group definition

The abstract and first model discussion now explicitly factor complete probe–reference groups. New Definition 12.1 repeats this. Separable probe marginals with one shared quantum reference do not meet the definition merely by being separable.

### R06 — Unknown remainder

The allocation theorem is uniform over every legal member of the fixed quadratic tube, with constants independent of the allocation and remainder. The individual Pauli-Y events, public clipping and final bounded weighted statistic depend only on E,H,Lambda,s and the allocation, not on the remainder or its actual output biases. The common-readout lemma is included precisely to establish this last point for unequal groups.

### R07 — Finite errors

The upper retains `n_r r_0 s²` before converting to Bures distance. The lower retains `m_r kappa s²` inside each event's probability interval before amplification. The regular proof also retains the inherited `N s²` term. These appear in the introduction, formal proof, proof audit and resource ledger.

### R08 — Two intervals

The inherited `s_*` is a legality/nonemptiness interval. The profile theorem uses a separate `s_0` containing the canonical-factor, phase and quadratic-error restrictions. Neither the exact allocation routine nor the sufficient tube certificate claims to compute that discrimination interval.

### R09 — Sufficient allowance

`Lambda_*` remains sufficient and coarse, not minimal, unique or canonical. All inherited examples and their smaller valid allowances remain unchanged. The new theorem quantifies only over legal members when no nonemptiness assertion for the requested allowance is available.

### R10 — Two linear mechanisms

Classical support opening has a product-input impossible-event lower and depends only on the total call count. Coherent tangency depends on the second moment of complete group sizes and uses a known-direction corrected GHZ signal. These remain separate rows.

### R11 — Product upper versus entangled upper

The proof uses the horizontal adaptive upper for the regular row and the canonical-factor block Bures bound for the coherent row. It does not apply the old independent-pair converse to entangled inputs. Final joint processing remains arbitrary.

### R12 — Independent exact-head verification

The delivery supplies read-only workflow definitions for (a) the actual reviewed v87 publication and (b) the eventual v88 publication head, with credential persistence disabled and distinct execution receipts. They use immutable checkouts and do not commit during verification. **They have not been run remotely in this delivery:** the current connector exposes no write actions, and container GitHub access failed. No status/check on `aab076...` or a v88 remote SHA is claimed. Local reconstruction is separately recorded and is not a substitute. The deployment script requalifies source on the actual pinned remote base and must be run in an authenticated real clone before remote release is asserted.

### R13 — Computational outputs

The new exact routine computes only allocation moments, an exact integer resource maximum and optional public phase clipping. It does not classify a measurement, compute `D_N`, optimal constants, an optimal test, curvature, recovery synthesis or a physical protocol. Complete typed replay refuses malformed, partial and tampered certificates.

### R14 — Global learning and growing outcomes

All retained learning and coding results keep their own balanced-interior and fixed-k hypotheses. The profile theorem is a discrimination theorem, not full-boundary common learning. The unmatched growing-k learning dependence and global midpoint equivalence/entropy are not declared closed.

### R15 — Separate journal objects

The primary remains focused on discrimination. The current binary supplement accompanies its explicitly identified learning dependencies. The structural article remains independent and unchanged. The complete mathematical edition is archival. All previous proof sections remain active; no historical theorem is sacrificed for a page-count target.

## Detailed comments

| Comment | Action or preserved argument |
|---|---|
| D01 | The profile theorem states `||R||_Sigma=sum_j||R_j||op` directly. |
| D02 | Abstract and theorem state uniformity in the full allocation, N and F, not E,H,Lambda. |
| D03 | The horizontal solution for regular directions and canonical solution for the coherent block upper are named separately. |
| D04 | Root fidelity and `beta²=2(1-f)`, `beta²<=||rho-sigma||1<=2beta` are displayed in the new proof. |
| D05 | Fidelity multiplication is used only across independent complete groups. |
| D06 | Public randomization is handled as direct sums with common weights and the public label retained. |
| D07 | The new lower repeats that the Pauli-Y observable is extended by zero off the GHZ subspace, giving a legal effect on the whole output. |
| D08 | The 2d reference bound is per used call; the entire group reference grows with the group. |
| D09 | The correction remains an ideal known-direction construction without a gate-complexity or hardware assertion. |
| D10 | Groupwise clipping depends on the public phase, allocation and fixed base/direction; not the unknown remainder. |
| D11 | If any group clips, its logical phase is at least 1/4; a fixed positive lower controls the target because the latter is at most one. |
| D12 | Complete unequal-group qubit probability laws are exact regression examples, not general recovery execution. |
| D13 | The original PSD cone attribution and coupled-normalization distinction are preserved verbatim. |
| D14 | The original represented-input support-eigenvalue lower argument remains in Section 10; a resource cap is not substituted for a complexity proof. |
| D15 | Zero tangent and higher-order limitations, including the full `O(t^(2q))` remainder premise, are unchanged. |
| D16 | Blockwise binary readout plus one classical statistic is an admissible lower construction inside an upper class with arbitrary final collective processing. |
| D17 | Local-order equivalence is explicitly separated from the global utility of feedback. |
| D18 | The initial source and local commits are unsigned; no verified human authorship is asserted. |
| D19 | The new profile theorem is highlighted in the abstract/introduction. Existing learning consequences follow the discrimination results and are not used to inflate the new result. |
| D20 | The complete edition remains a preservation object, not an additional journal submission. |

## Audit release gates — 21 items

| Gate | Status and location |
|---|---|
| M1: fixed tube quantifiers | Retained and expanded to every prescribed allocation; abstract and Theorem 12.3. |
| M2: finite quadratic remainders | All three required error scales retained in proof and summaries. |
| M3: integer lower cases | Both no-clipping and at-least-one-clipping cases proved; inherited equal-width proof unchanged. |
| M4: opening/coherent distinction | Separate rows and constructions. |
| M5: zero-jet and higher-order limits | Preserved. |
| M6: sufficient allowance only | Preserved. |
| M7: local parallel/adaptive order | Preserved; no exact equality. |
| P1: HMNW/Yuan–Fung | Full-text comparison and explicit parameter substitution added. |
| P2: GHPS | Abstract-supported resource-model comparison added; full-text priority analysis pending. |
| P3: independent assessment | Not supplied; precise review brief prepared. |
| P4: no firstness from search | No such inference made. |
| E1: page-one group definition | Complete group factorization in abstract. |
| E2: shared reference excluded | Explicit in abstract and definition. |
| E3: discrimination focus | New allocation law foregrounded; prior proofs retained. |
| E4: structural article separate | Independent source graph unchanged. |
| E5: complete edition archival | Explicit. |
| V1: v87 exact publication run | Read-only definition supplied; remote execution pending. |
| V2: status attached to v87 SHA | Not claimed; deployment requires actual remote check evidence. |
| V3: long-lived receipt/package | Local source-bound packages produced; workflow requests 90-day artifacts, remote upload pending. |
| V4: signature or unsigned notice | Unsigned notice supplied; no signature fabricated. |
| V5: machine-readable scope | Current exact routine and status/evidence flags distinguish tests, mathematical proof and execution. |

## Audit risks — 16 items

| Risk | Treatment |
|---|---|
| K1: global overclaim | Every theorem headline retains fixed-tube scope. |
| K2: adaptivity overclaim | Local orders, never exact equality or global feedback uselessness. |
| K3: terminology | Complete probe-reference allocation is the defined resource. |
| K4: priority | Current specific comparisons; independent assessment and GHPS full-text examination remain separate. |
| K5: mechanism novelty | Standard Bures, GHZ, second-moment and QEC principles explicitly credited. |
| K6: nonempty threshold | Sufficient, not minimal; original countercomparison preserved. |
| K7: remainder loss | Errors paid before Bures or statistical amplification. |
| K8: shared reference | Excluded across complete groups; no probe-marginal shortcut. |
| K9: exact-certificate overreach | Integer bookkeeping only for the new routine, with explicit false scope flags. |
| K10: regression overreach | Exact finite tests are not continuum proofs. |
| K11: growing outcomes | Retained fixed-k learning theorem is not promoted. |
| K12: control synthesis | No efficient general quantum implementation or physical execution claimed. |
| K13: provenance | Local and remote identities distinguished; remote push and independent remote verification pending, not mislabeled as success. |
| K14: editorial accumulation | Profile result made visible without deleting the existing development; supplement and archival edition remain separate. |
| K15: wider programme | All five independent A/B/C/D aggregate flags remain false. |
| K16: general-journal significance | The objective is retained; the new mathematical extension is offered for assessment, not declared to establish editorial acceptance. |

## What this revision actually supplies

The written allocation theorem, its common-readout lemma and exact budget corollary are new and included in both primary and complete editions. Every predecessor proof section is byte-identical. The current comparison, response, audit, exact routines, local source-bound rebuilds and deployment definitions accompany them. Remaining independent priority and remote-release steps are stated as remaining, not silently converted into passed gates.
