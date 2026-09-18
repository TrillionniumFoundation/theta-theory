# Response to the independent A2 v80 referee report

**Revision:** A2 v81, *Blind clock pencils and action rigidity*.  
**Reviewed manuscript:** `831dc905d139377e117138238d20d96833f4122d`.  
**Controlling report:** `reviews/a2-v80-calibrated-records-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`, substantive commit `69949b8be016cdaafcb2fae818aa0ca548e2f96e`, formatted head `2edd50e3f97228432ab3c7a1e1f11618f8f45a09`.  
**New branch:** `revision/a2-v81-blind-clock-pencils-2026-09-18`.

The revision does not answer the conceptual objection by changing the requested venue or by deleting the earlier theorem chain. It introduces one principal observation theorem and makes the previous regimes its companions. All substantive inputs of the reviewed v80 manuscript remain active in the full entry `papers/A2-v17-boundary-information-coarsening/rigidity_v81.tex`; all old source files are unchanged. The shorter `rigidity_v81_core.tex` is a reading edition of the new development, not a substitute for the full manuscript.

## Principal mathematical change

Two uncalibrated noisy readings of a retained trajectory give

`M_j = U diag(a_b (T_j-W_b)) V^T`.

Conditional independence is given the hidden branch **and endpoint**. Channels may depend on endpoint but are invariant across clocks. The observer is not given their entries, the component count, a ground-truth audit, or structural names. Full column rank and separated action values are explicit hypotheses. Subtracting two raw matrices gives a rank-B slope; the reduced observable operator has eigenvalues `T_1-W_b`. Polynomial spectral projectors recover rank-one component matrices and hence both channels.

The genuinely coarsened version observes only `N_j=c_j(z)M_j`, with independent unknown positive scale functions at the clocks. Three matrices determine the unique relation `N_3=alpha N_1+beta N_2`. Known clock interpolation coefficients identify the relative scales. This restores the affine pencil up to a harmless common factor. Absolute actions and channels, and relative weights, are recovered. A branch-blind endpoint-dependent detector is therefore an **exact nuisance symmetry**, not an efficiency error floor.

This is a replacement observation architecture, not an assertion that two independent sensors are free. The paper states this explicitly and proves a one-readout ambiguity. A nonconvex three-sheet exact shear with positive roof and two positive Vandermonde readout channels proves nonvacuity without true-component labels. A two-projective-clock ambiguity shows that the third clock carries information.

## Response to the major comments

| Comment | Response and exact location |
|---|---|
| R80-M1 | The main theorem is now blind latent-sheet recovery, not calibrated recovery called unmarked. See `thm:v81-main`. The old calibrated theorem keeps its correct name and scope. |
| R80-M2 | No ground-truth audit is used in the new inverse or its sampling theorem. The additional capability is two conditionally independent readouts, stated before the main theorem and realized in `prop:v81-shear`. |
| R80-M3 | `U(z),V(z)` may vary smoothly with endpoint. Clock invariance replaces endpoint invariance in the new model. The old one-channel calibrated model still explicitly requires endpoint independence. |
| R80-M4 | The visible component count is recovered by rank, without a supplied catalogue. `rem:v81-count` states the signal threshold and the exclusion of invisible duplicate columns. Smooth small extra components are covered only in the stated matrix norm, not as arbitrary omitted components. |
| R80-M5 | `prop:v81-common-clocks` constructs simultaneous windows from a class-wide elapsed-time bound using an independent release delay. Equation `eq:v81-old-window` gives a sufficient condition for the different, original flow-box protocol; branchwise windows alone are not used as a proof. |
| R80-M6 | Raw slope/intercept inversion is retained but no longer carries the principal conceptual burden. The main result handles unknown channels, unknown count and projective laws. |
| R80-M7 | `lem:v81-projective` allows unknown deadline-dependent exposures, lost failure counts and even unknown endpoint-dependent common detector functions. `prop:v81-two-projective` proves a genuine ambiguity for two projective clocks. |
| R80-M8 | `thm:v81-unpaired` starts from unpaired endpoint matrices, not full lifted powers as observed inputs. Counts, channels, absolute primitives and sheets are reconstructed first. The subsequent Bezout identity is explicitly described as elementary. |
| R80-M9 | The regular phase-cover and global-section assumptions are stated in `def:v81-cover` and `cor:v81-reeb`. The new theorem removes supplied sheet pairing and calibration, not these dynamical hypotheses. |
| R80-M10 | The existing-Reeb corollary uses actual return time. It does not claim an intrinsic inverse for arbitrary contact flows with no section or regular observation domain. Its precise positive improvement is the projective, unpaired observation theorem on those domains. |
| R80-M11 | The retained billiard reconstruction remains marked/reference-atlas dependent. Unknown latent indices are not called recovered reflection words. The new unpaired graph theorem needs no such semantic identification. |
| R80-M12 | The delayed clock rule is class-wide once a flight/return bound is fixed. This does not convert the inherited local identifying atlas into a universal geometric acquisition algorithm. |
| R80-M13 | The revision attacks the audit and catalogue assumptions directly and proves one-readout and two-projective-clock obstructions. These concern the declared observation class, not necessity of every billiard mark. |
| R80-M14 | `thm:v81-fixed-source` keeps one normalized raw source density fixed in common scalar phase coordinates. The proof distinguishes a changing physical embedding of that chart from a changing source law. |
| R80-M15 | `cor:v81-detector` and `thm:v81-fixed-source` separate exact identification under a common detector from confounding under branch-selective retention. The latter compensator is not inserted into the former model. |
| R80-M16 | `thm:v81-sampling` removes the calibration sample and its rarity term, but makes no unsupported matching geometric sampling-rate claim. The new main result is an information theorem rather than an asserted minimax theorem. |
| R80-M17 | Section `sec:v81-retained` imposes conditional independence of audit availability and reported label given the true component, gives an independent Bernoulli design, and explains why audited column frequencies are then unbiased. |
| R80-M18 | Section 1.1 distinguishes spectral latent identification, affine/projective clock reconstruction, generating-function calculus and classical return-time geometry. The bibliography adds Allman--Matias--Rhodes, Anandkumar--Hsu--Kakade, Bonhomme--Jochmans--Robin, Hu--Schennach and Geiges. No general spectral or group-theoretic priority claim is made. |
| R80-M19 | Section 1.1 explains that endpoint actions contain local canonical-relation information after differentiation, not just periodic lengths; a finite atlas is not a global scattering relation, and Euclidean scattering coordinates differ from abstract scalar labels. No unjustified total ordering of these data is asserted. |
| R80-M20 | The principal theorem is blind projective action identification. Unpaired dynamics, detector invariance and sampling follow from this common inverse. The older conditional/calibrated/convex/billiard results remain active as companion appendices rather than being removed. |

## Response to the technical comments

| Comment | Revision |
|---|---|
| R80-T1 | Endpoint independence is stated for every calibrated companion in Section 8.1; endpoint dependence and clock invariance are stated at the new main theorem. |
| R80-T2 | The audit sampling law and its conditional-independence requirement are explicit in Section 8.1. |
| R80-T3 | New delayed common-clock construction and separate old-protocol simultaneous-window inequality; the two experiments are not conflated. |
| R80-T4 | Blind visible-count recovery is distinguished from calibrated closed-world label robustness, and from semantic word recovery. |
| R80-T5 | A full fixed-source physical lower-bound proof is included. |
| R80-T6 | The inherited rank obstruction and new fractional ambiguity are explicitly scoped to the unrestricted action observation class. |
| R80-T7 | The full entry changes only the displayed convex section heading to “six conditional laws and four raw laws”; its original source is untouched. |
| R80-T8 | One principal theorem appears first. Companions follow the blind action, physical and sampling development. |
| R80-T9 | The in-paper data-dependence table separates raw/projective/conditional, blind/calibrated, phase/billiard and exact/sampling assumptions. |
| R80-T10 | Geiges is added to the contact context; the Reeb identity and lift product are derived, and the arithmetic step is not claimed new. |
| R80-T11 | Classical latent and repeated-measurement identification and Econometrica measurement-error work are added, not just neural-network loss correction. |
| R80-T12 | The stability proposition and sampling theorem enumerate clock, rank, spectral, weight, gate, smoothness, exposure and geometric collar dependencies. |
| R80-T13 | The old nonclaims remain attached to their old model. Catalogue learning is claimed only under the new independent-readout/full-rank model. No arbitrary-caustic, universal-billiard, or geometric-minimax conclusion is inferred. |
| R80-T14 | A new root handoff, exact source manifest, response and build-status record accompany the new branch. Historical root material is preserved. |
| R80-T15 | An actual LaTeX build script and workflow compile both entries and reject unresolved references. The locally compiled core PDF is distinguished from the full integrated build; a queued or unexecuted job is not called successful. |

## Prior-art comparison at the level of implications

The affine blind diagonalization is a specialized observable-operator argument; classical latent-variable identification already contains its spectral mechanism. The extra structured information is the known clock dependence, which turns eigenvalues into absolute actions. The projective step uses ordinary linear dependence of three matrices but recovers an affine clock pencil despite unknown endpoint-dependent scales. Composing these two facts produces the stated exact detector quotient. The paper does not claim these elementary operations separately as new mathematics.

The deterministic phase-graph and contact operations are likewise classical. Their data are different here: unpaired, unknown-count projective mixtures are converted to absolute sheets before those operations can be performed. A complete regular cover is still needed for the chosen target. The three-sheet shear is a concrete nonconvex example, not a proof of recovery at a caustic. The fixed-source lower bound and common-detector inverse are deliberately different apparatus models.

## Verification and further independent assessment

The written proofs, finite-dimensional algebra regression, source preservation and LaTeX compilation have different evidentiary roles. Eleven deterministic regression tests cover exact inverses, endpoint-dependent channels, conditional joint matrices, the two ambiguities, the three-sheet shear, compensation and windows. They are not formal proof certification and do not verify every inherited geometric lemma. The new core was natively compiled and its rendered pages inspected. The source-matched full-build state is recorded separately in the handoff.

The requested general-journal ambition is retained. No acceptance decision or independent endorsement is represented by this revision or by a passing build. The new proofs and their significance are submitted for a fresh mathematical assessment rather than marked editorially settled.
