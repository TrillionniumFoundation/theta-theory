# Response to the R55 external report and proof/pipeline audit — Revision 86

We thank the referee for the detailed reading and the specific requests on local curvature, reference-uniform norms, fixed-object quantifiers and the boundary of the first-jet result. We retain the general mathematics journal objective. The original recommendation is preserved verbatim; neither this response nor a successful build claims referee or editorial approval.

The exact reviewed v85 object is `ca39533970c77a156cafe916ee6287c54c91fa00`. The controlling external report is commit `107182f19e0534ae99cd68fc10cd71dddd1563a7`; the controlling pipeline audit is `7dc5d76ace1aa993c946770e0b5b2d8b853e5419`. Their complete original texts are frozen in the new source, and the existing pipeline history remains intact.

The mathematical response has four parts. We prove the complete one-sided tangent cone, then a finite-pair dichotomy uniform over every legal second-order remainder at a fixed base and direction. We distinguish support-opening linear accumulation from the coherent linear mechanism through a matching independent-product theorem. We give controlled higher-order consequences and a complete mixed-rate scalar family. Finally, we supply an exact cone/pair certificate and clarify the old curvature and channel-norm proofs without removing their text. These results extend the scope by proofs, not by suppressing qualifications. They do not settle arbitrary-pair global geometry or certify independent priority.

## 1. Required revisions

### R01 — Novelty beside the main theorem

The discussion immediately following `thm:tubedichotomy86` distinguishes first-order support opening from the established coherent Kraus-span correction mechanism, with Zhou–Jiang and Knill–Laflamme attribution. The additional result is uniformity over a fixed finite quadratic tangent neighborhood and its three acquisition mechanisms, not new metrological exponents. Standard fidelity tensorization is credited explicitly in `thm:producttrichotomy86`.

### R02 — Local curvature definition

Registered insertions in Sections 73 and 74 state `L=sup_{|u|<=a0} sum_j ||E_j''(u)||op` as numbered `eq:curvature86`, repeat it inside the logical-channel lemma and the control theorem, and cite it with kappa. The new finite-pair proof has a different given remainder Lambda and explicitly uses `kappa=Lambda+2||Gamma||op^2`; it does not infer curvature from a first jet.

### R03 — Existence and computation

The analytic normalized factors remain existence constructions. `cone_geometry.py` uses exact rational support projectors, PSD tests and Hilbert–Schmidt Gram projection. It certifies the one-sided cone and optionally one supplied pair, not a symbolic square root, entire curve, quantum recovery or its gate synthesis.

### R04 — Fixed-object quantifiers

The old fixed-curve quantifiers are retained. The new theorem fixes E,H,Lambda, and is uniform only over all legal second-order remainders obeying its displayed bound. Constants and the interval may depend on support eigenvalues, nonzero tangent size and residual gap. The abstract, introduction, theorem, schema and README repeat this distinction.

### R05 — Arbitrary pairs

The global midpoint covariance is still a one-sided upper certificate. The new theorem does not assert uniformity across base points or arbitrary pairwise directions: it proves a two-sided law on the precisely defined fixed tangent neighborhood. No global volume, entropy or boundary learner is inferred.

### R06 — Zero jets and one-sided hypotheses

The v85 theorem still assumes a nonzero two-sided first jet and its old exclusions are not edited away. A separate proved cone theorem now handles one-sided openings, and a higher-order corollary covers only E+t^qH+O(t^(2q)). The mixed scalar law explicitly accounts for an intervening opening outside that corollary. Both exact programs still report a zero tangent alone as higher-order undetermined.

### R07 — Reference-uniform channel estimate

New `lem:channelnorm86` proves the diamond bound for arbitrary amplified trace-class inputs by the adjoint block-test norm, rather than relying on an unstated state-optimization theorem. It states Hermiticity preservation and trace annihilation for the derivative/difference case, and the old smooth-curve proof now points to it.

### R08 — Known-pair versus common learning

The code, recovery, scale, integer cycle count and logical Helstrom measurement are known-pair resources. The opening branch instead uses a single fixed missing-support probe and a classical impossible-output event. Neither is supplied as private advice to the retained unknown-measurement common learner.

### R09 — Implementation budgets

The inherited control theorem and new finite-neighborhood corollary retain worst-case, reference-stable diamond bounds under both hypotheses. The sufficient per-cycle tolerance shrinks with sDelta; it is not a fixed-hardware-noise guarantee. The error ledger does not assume independence or claim execution.

### R10 — Primary-source priority

The detailed v85 full-text comparisons remain in the current article. The official Watrous Chapter 3 fidelity statements and current primary arXiv abstracts were rechecked; `LITERATURE_RECHECK86.json` distinguishes this from the prior full-HTML retrieval. Independent human specialist assessment remains unsupplied and is not declared completed by this author-side revision.

### R11 — Growing outcome count

The balanced learner keeps its fixed-k sharp order, explicit k^3 constructive upper and binary-subfamily lower. Neither the new neighborhood classification nor its product restriction supplies a growing-k learning converse.

### R12 — Computational boundary

The new polynomial result is exactly cone/range classification and a sufficient PSD test of a supplied pair remainder. It adds an exact opening witness probability. It does not compute the theorem interval, arbitrary adaptive distance, optimal code, public dictionary or general recovery/readout circuit.

### R13 — Dependency table

The main introduction preserves and extends the human-readable table. The core neighborhood and cone proofs use covariance, complete support kernel, finite Bernoulli lemma and completed correction already proved in the primary. The product upper adds explicitly stated standard fidelity facts. Balanced learning continues to identify its exact supplement premises.

### R14 — Independent programme

The A/B/C/D history and ordering are retained in the current history audit and frozen ledger. The five aggregate flags remain false. The independent structural article is neither a premise nor a significance multiplier for the measurement result.

### R15 — Fresh release identity

A new response branch starts at the exact reviewed v85 final head. The new source is qualified as an actual native Git object; publication must directly inherit it; the final metadata-only head is separately reconstructed read-only. The build runs all 24 suites on current source, not inherited successful receipts.

## 2. Minor comments

### C01 — Small neighborhood

All local assertions use an interval belonging to the fixed E,H,Lambda or fixed curve; no neighborhood uniform over the body is claimed.

### C02 — Notation order

P,Q,J,Gamma and the real support span are defined before the new introduction theorem display; the abstract uses the covariance range rather than an undefined generator.

### C03 — Analytic inverse root

`lem:factorremainder86` explicitly notes that I+s²B*B is positive definite for all real s and that its inverse square root is analytic near zero.

### C04 — Stack and dilation norms

The normalized-factor lemma states that duplication of the label into a discarded environment is an isometric embedding of the stacked factors and preserves their operator and derivative norms.

### C05 — Unhalved conventions

The introduction, channel-norm lemma, finite-neighborhood section and error ledger all specify unhalved trace/diamond norms; the product fidelity proof uses the matching factor two.

### C06 — Zero tangent certificate

Old `curve_geometry.py` remains unchanged. New `cone_geometry.py` also returns `higher_order_undetermined`, with no stationarity inference from incomplete curve data.

### C07 — Rank-opening example

The original v85 example stays active in the primary. New one-sided rational cone realizations and an exact higher-order scalar mixed-rate example are additional statements, not replacements.

### C08 — Literature provenance

The original v85 retrieval digest remains bound to its actual event. Current rechecks, inherited full-text comparison, independent priority and release verification are explicitly separated.

## 3. All pipeline acceptance gates

The table indexes every gate in Section 10 of the controlling R55 audit. An execution gate is established by the actual new receipt, not by the planned workflow or this table. P01 remains explicitly external and unfulfilled.

| Gate | Referee requirement | Revision response |
|---|---|---|
| M01 | Preserve the complete v84 kernel and do not replace it with an incomplete tangent ansatz. | The complete v84 kernel is unchanged and directly invoked, including all independent missing-support Z_j variables. |
| M02 | Keep two-sided first-jet legality `Q_jH_jQ_j=0` explicit. | The old two-sided J_j=0 hypothesis remains; new right-sided realizability is a separate J_j>=0 theorem. |
| M03 | Keep the sufficiency construction separate from factorization of the actual curve. | Finite surrogate effects are constructed separately; no differentiable exact root of F or its curve is assumed. |
| M04 | Preserve the exact sign and factor in the `Gamma` kernel pairing. | The full range proof preserves -2tr(A Gamma), and the exact suite compares direct covariance range on eight fixtures. |
| M05 | State the fixed-curve curvature norm `L` wherever `kappa` or channel remainders are invoked. | Equation curvature86 is inserted and repeated in both old logical/control statements; finite Lambda is separately named. |
| M06 | Retain the actual-versus-surrogate `Nt^2` error before truncation. | Both old Nt² and new (Lambda+K_b)Ns² remainders remain before truncation. |
| M07 | Preserve the main-text finite Bernoulli proof or an equally transparent replacement. | The entire primary Bernoulli proof is byte-identical and active. |
| M08 | Keep the recovery interface restricted to actual label and retained reference. | Actual label/reference only; the factor environment is discarded and never available to recovery. |
| M09 | Retain global CPTP completion before differentiating the recovery. | The full completed CPTP recovery remains unchanged; the finite-pair derivative uses its completeness identities. |
| M10 | Preserve the exact integer-call and angle-cap bookkeeping. | The new theorem records m=min(N,floor(1/(sDelta))), the floor at least two, and the half-truncated-angle bound. |
| M11 | Keep zero first derivative outside the theorem. | H nonzero remains required for generic dichotomies; zero H alone remains undetermined, with separately hypothesized higher-order results. |
| M12 | Keep one-sided openings outside the two-sided first-jet statement. | One-sided openings are not inserted into the old two-sided theorem; they receive a new cone and impossible-event proof. |
| M13 | Do not promote fixed-curve comparison to uniform arbitrary-pair covariance equivalence. | Fixed E,H,Lambda uniformity over a finite neighborhood is explicitly distinguished from body-wide midpoint equivalence. |
| M14 | Keep the control theorem conditional on supplied diamond-error certificates. | Only supplied uniform diamond certificates under both hypotheses qualify the implemented-control corollary. |
| M15 | Do not infer general recovery synthesis from the exact first-jet decision. | The cone certificate is a represented classical decision and does not synthesize any recovery. |
| M16 | Keep the transported-weight ridge distinct from a freshly uniform output ridge. | The old transported-weight ridge proof and its same-tau/Tw convention are unchanged. |
| M17 | Keep growing-`k` minimax explicitly open. | The current comparison and resource ledger retain the k^3 versus binary-lower gap. |
| M18 | Preserve the distinction between pair discrimination and common learning. | Known-pair controls and independent-product inputs are not private advice to a common learner. |
| P01 | Obtain an independent specialist assessment of support-kernel and first-jet priority. | Not established. The current specialist brief identifies the exact kernel/cone/neighborhood/product statements to assess. |
| P02 | Continue to credit Zhou–Jiang for the metrological exponent criterion. | Zhou–Jiang attribution appears beside the main finite-neighborhood theorem and in the current comparison. |
| P03 | Continue to credit Knill–Laflamme for exact correction. | Knill–Laflamme attribution and completed correction proof remain explicit. |
| P04 | Keep the covariant-learning comparison tied to exact models, losses, and query architecture. | The entire v85 theorem-level known-symmetry comparison is retained in current-comparison86.tex. |
| P05 | Do not identify parameter-count sharpness at fixed accuracy with joint error sharpness. | The inherited comparison retains the source general diamond accuracy exponent and distinguishes fixed-accuracy parameter count. |
| P06 | Do not infer firstness from the absence of an identical targeted-search result. | No firstness or priority clearance is inferred from author-side targeted search or exact reproduction. |
| P07 | Distinguish efficient Hayashi measurement implementation from this recovery's diamond certificate. | The specialized Hayashi gate guarantee remains distinct from a uniform diamond certificate for this pair recovery. |
| E01 | Keep the quantitative article as the journal-facing object. | paper.pdf remains the primary mathematical article. |
| E02 | Keep the binary supplement current and reconstructible. | The current binary supplement is rebuilt, linked by current xref source and preserved in both packages. |
| E03 | Keep the structural article independent. | The structural source graph is unchanged and independently complete. |
| E04 | Keep the complete edition archival. | The complete edition remains archival with all old and new proofs actively typeset. |
| E05 | Preserve the human-readable prerequisite table. | The dependency table now includes the finite-neighborhood and independent-product proof premises. |
| E06 | Place novelty and prior-principle attribution beside the main theorem. | Prior mechanism, elementary cone/fidelity ingredients and the finite-neighborhood contribution are stated next to the theorem. |
| E07 | Keep curve dependence and excluded regimes visible in abstract and introduction. | Fixed-object constants, zero-jet limits and product-access restrictions occur in the abstract/introduction, not only audits. |
| E08 | Keep audit/provenance detail outside the central mathematical narrative. | Frozen reports, hashes, gate crosswalks and execution metadata stay outside the mathematical proof narrative. |
| V01 | Any changed theorem source requires a fresh native-source commit. | The native-source workflow commits and checks the full new inventory before publication qualification. |
| V02 | Publication artifacts must be a direct child of that native source. | The publication workflow enforces native parent identity and stages only declared artifacts plus its root marker. |
| V03 | The exact final head must be reconstructed read-only. | A separate read-only workflow is triggered by the exact final review request commit; its actual verified_head is authoritative. |
| V04 | All four current documents must be rebuilt. | The builder reconstructs primary, binary supplement, structural and complete PDFs. |
| V05 | All inherited and current exact suites must run anew. | All 23 inherited suites and the new cone suite run under ordinary and optimized Python, with result equality. |
| V06 | No unresolved references, citations, or bad boxes may be hidden. | Unresolved references/citations and bad boxes fail qualification; raw engine warnings remain in the receipt. |
| V07 | Finite tests must retain false continuum-proof and physical-execution fields. | All finite scope records keep physical/continuum-proof flags false. |
| V08 | Resource-cap violations must reject without partial certificates. | The cap is checked before matrix work, and certificate mutations/insufficient budgets reject instead of returning partial success. |
| V09 | Build identity must not be represented as a human cryptographic signature. | No signature or human authorship claim is inferred from Git/CI identity. |

## 4. Risk register

| Risk | Subject | Current handling |
|---|---|---|
| K01 | Local-to-global overstatement | Only a fixed-base/direction quadratic neighborhood is uniform; no arbitrary-pair midpoint equivalence. |
| K02 | Existing metrological mechanism | Established exponent/correction mechanism and fidelity facts remain credited; no primitive discovery claim. |
| K03 | Nonuniform constants | Constants and interval retain base, direction, remainder, support and gap dependence. |
| K04 | Zero first derivative | Generic zero jets remain undetermined. Controlled power jets and one explicit mixed-rate family have separate proofs. |
| K05 | One-sided rank opening | Addressed positively by the exact one-sided cone and repeated impossible-label lower, without altering the old two-sided hypothesis. |
| K06 | Smooth-root assumption | Actual roots are not differentiated; finite surrogates and remainder bounds are explicit. |
| K07 | Recovery environment | No inaccessible environment or consumed input is provided to recovery. |
| K08 | Conditional controls | Supplied angle-dependent diamond certificates are required; fixed-noise robustness is not claimed. |
| K09 | Pair-versus-learning resources | Known pair/code/scale/readout and common learning resources remain separate. |
| K10 | Computational overreach | Cone and pair decisions do not infer curvature, interval, tester, distance or compiled quantum control. |
| K11 | Regression overreach | 353/27 checks are exact finite regressions, not continuum proof or hardware execution. |
| K12 | Current literature | Inherited full-text comparison and current primary rechecks are distinguished; independent priority remains absent. |
| K13 | Growing outcomes | Fixed-k learning retained without upgrading the growing-k gap. |
| K14 | Wider programme | All five independent analytic flags remain false. |
| K15 | Archive as novelty multiplier | Complete edition and separate structural paper are not multipliers of novelty. |
| K16 | Signature | No signature claim is made; identity and reconstruction establish bytes only. |

## 5. Proof preservation and execution boundary

Every original mathematical proof byte is retained. The only changed predecessor proof files are Sections 73 and 74, through registered insertions that state curvature and the reference-uniform norm. Removing those exact strings restores the original SHA-256 values. All other inherited proof sections are byte-identical. The old primary/supplement, full and structural label graphs remain active; no additional labels are moved to the supplement.

The new source must execute 24 exact suites, including the 353-positive/27-negative cone suite and the full inherited corpus, under ordinary and optimized Python. Four documents and the linked standalone journal package are rebuilt. Native qualification, publication and final-head reconstruction have distinct identities. No old successful receipt is current qualification, and finite tests do not establish mathematical priority, universal theorem truth or a physical recovery.

The next mathematical review can concentrate on `thm:tubedichotomy86`, `thm:producttrichotomy86` and `prop:mixedrates86`, together with the complete cone/range lemma and finite normalized-factor remainder. The exact hypotheses and remaining general questions are part of these statements, not hidden in metadata.
