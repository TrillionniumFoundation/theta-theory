# Response to the referee on A2, revision 68

Qian Qi — September 16, 2026.

Report: `reviews/a2-v68-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, frozen at `33bd2164d68cae0b412407c8176440fe8d7eaa9b`. The reviewed mathematical source was `de0deffc2ca7b0fd2f0d2d5ad5fbdff1eee0f0a6`, manuscript tree `23f07201ea4c6a33270cf4d4a977da1eddf8e8fe`.

We thank the referee for distinguishing a substantive smooth extension from an editorial judgment about its significance. The report establishes neither a new fatal error nor a mandatory core proof repair within its stated coverage. We do not recast that assessment as acceptance or as certification of the whole manuscript. This revision retains the previously examined smooth argument and supplies an integrated statistical consequence: the differentiated law norm required by that argument is now constructed from finite endpoint records, with the cost of unsuccessful physical preparations included.

## 1. The added argument and what it changes

The sole new active proof input is `article/10e_sampled_smooth_recovery_v69.tex`, “Smooth contact recovery from finite preparations.” It has one lemma and two theorems, with proofs. They form one acquisition-to-inversion argument, not three independent claims of exceptional novelty.

For a fixed marked periodic polygon and two separated exact offsets, take independent full-phase preparations at a returning flight number N. Success is the selected windowed itinerary, gated on a larger positive-residual square. The success tag is exact; endpoint values after acceptance may have arbitrary bounded readout displacement delta. The observation on a smaller square avoids an unproved density extension at the gate boundary. Uniform positive geometric margins and finitely many derivative bounds are priors on a realizable class of actual tables, not an assumed error bound for an observed density. No analytic prior is used.

The interior kernel lemma estimates the complete C^m density error from n accepted endpoint samples. The proof includes moment cancellation, the variance calculation in dimension two, an exponential tail bound, a spatial grid, and a pathwise readout-error estimate. The estimator need not be a positive density. Rather than apply an exact geometric identity to this arbitrary estimate, a countable measurable minimum-distance selection is taken in the image of actual marked tables. The geometric stability theorem is applied only between two realizable limiting laws. This avoids assuming that empirical densities factorize, or that every nearby density has a physical inverse.

For fixed orders m and s, the accepted-sample bound is

`C [exp(-omega N) + (log(C J n/zeta)/n)^alpha + delta^gamma]`,

where `alpha = s/(2(m+s)+2)`, `gamma = s/(m+s+3)` and `J = 2r`. The confidence is at least `1-zeta`. An explicit binomial lower-tail estimate then charges all `J B` preparations, not merely accepted bridges. Balancing the finite-flight error against the exponentially rare probability lower bound gives

`C [(log(C J B/zeta)/B)^beta + delta^gamma]`,

where `beta = alpha omega/(omega+alpha Gamma) > 0`, with confidence at least `1-2zeta`. The flight number is a multiple of the oriented period and grows logarithmically with B. The sufficient-success, bandwidth and small-error conditions are printed. This is an attainable upper rate, not an optimal or minimax claim. The measurable selector is an existence estimator, not an efficient enumeration algorithm.

This changes the input statement in a concrete way: differentiated limiting laws are no longer required as observations for this fixed-period recovery result. The result uses finitely many physical preparations and controls complete smooth profiles, including flat changes at every fixed nonzero separation. It does not solve unknown-mark registration, erroneous acceptance labels, noisy offsets, or single-trajectory dependence.

## 2. Mathematical observations R68-M1–M5

**R68-M1, actual constant-one contraction.** Preserved without modification in `article/10d_smooth_contact_rigidity_v68.tex`. The tail identity from the signed actual half-line is used before choosing the vanishing order. We do not replace it by a bound with an uncontrolled prefactor raised to that order.

**R68-M2, integrated pair-dependent separation.** Preserved without modification. The averaged operator is a separation device for a fixed candidate pair, not an observation-only reconstruction formula. The new minimum-distance estimator compares realizable laws and invokes that device only through the established stability theorem.

**R68-M3, smooth germs versus Taylor series.** Preserved without modification. Equality of all jets remains insufficient in the smooth category. Full action information is used again to remove a flat difference. The new statistical corollary concerns complete C^0 profiles, not an all-order jet norm.

**R68-M4, polynomial alignment and the density norm.** Preserved without modification. Polynomial alignment still precedes the weighted estimate. The new kernel lemma supplies precisely the required finite C^m density norm under explicit C^{m+s} forward bounds. Neither total variation nor a raw histogram is treated as if it controlled derivatives. The finite-smoothness prior, smaller common collar, and nonoptimal derivative allowance are retained.

**R68-M5, actual flat equal-area family.** Preserved without modification. The end of the new section gives a two-point testing consequence at a fixed nonzero contact displacement: choose the charged profile error below one third of the profile separation. The construction is still not an equal-full-marked-length-spectrum example and does not assert equality of normalized density jets. The remote area correction does not affect the tested contact coordinate.

## 3. R68-E1: the significance objection

The principal theorem, abstract, and mechanism discussion now state the finite-preparation consequence with its actual assumptions. It follows the geometric inverse immediately in the paper, rather than appearing as a detached abstraction. The proof uses the relative physical law to control both the finite-flight differentiated bias and the rare acceptance probability. Conditioning and absolute action approximation cannot replace that relative argument. Its inverse step uses the actual smooth boundary mechanism, not a generic inverse for arbitrary densities.

We agree that kernel estimation, minimum-distance selection and binomial concentration are classical techniques. They are not advertised as independent breakthroughs. The significance claim remains the combined relative-law/actual-contact mechanism and its consequences for a specified physical observation. The new acquisition theorem shows that the full function-valued law need not be supplied as an oracle in this bounded fixed-period class. The model still has known marks and controlled offsets. Constants deteriorate when margins degenerate; no uniform-in-period or same-data comparison with marked-length-spectral problems is asserted.

Whether this mechanism has the exceptional depth and influence sought by the four requested journals remains a matter for an independent editorial assessment. This response does not lower the target, invent a no-go statement, or claim that a further theorem compels acceptance.

## 4. R68-E2: no manufactured repair cycle

The report requests no arbitrary deletion and no nominal repair of a correct theorem. Accordingly all six v68 statements and their proofs are unchanged, as are the corrected curvature stopping formulas. All inherited active proof inputs remain active. The new acquisition result addresses the stated observation issue directly. Earlier analytic/global reconstruction, moving-family, calibration, statistical and companion material remains in the complete manuscript with its original qualifications.

## 5. R68-P1: raw source-ZIP modes

The defect was in archive headers, not in source bytes or remote Git modes. The new `source_archive` implementation reads each original mode from the frozen Git manifest and writes a Unix ZIP header with that mode. It does not read permissions from the deliberately read-only build snapshot. Both previously affected executable scripts retain mode `100755`.

`tools/verify_source_zip_v69.py` verifies every member's bytes, length, Git blob and raw Unix mode. Its optional extraction accepts only a new destination and restores those modes explicitly. This distinction matters because Python's ordinary `ZipFile.extractall` does not restore executable bits. The old v68 ZIP is expected to fail the strict header check at the two reported scripts; its immutable historical delivery is not rewritten. A deliberately corrupted executable header is a negative control in the v69 checker.

## 6. Disposition codes

| Code | Response in revision 69 |
|---|---|
| R68-D1 | The examined v68 proof module is byte-identical. No newly mandatory core repair is alleged. |
| R68-D2 | Complete smooth contact-germ identification, no candidate-closeness assumption, and finite-smoothness real stability remain central. |
| R68-D3 | Marks, shared offset amplitudes, differentiated topology, finite priors and class-dependent collar are explicit. Exact selection tags and offsets, independent resets, and bounded post-acceptance readout are declared for the new experiment. Analytic-global conclusions stay separate. |
| R68-D4 | Raw ZIP modes now follow the Git manifest; strict verification and mode-faithful extraction are supplied. |
| R68-D5 | The combined mechanism is submitted again without a self-issued significance verdict. The new finite-preparation consequence is proved, not substituted for an editor's judgment. |

## 7. Retention and evidence

All 876 reviewed source paths remain present. Eight inherited files are edited, with byte-exact originals and their original modes in `history/v68-review-baseline/`; 868 paths remain unchanged. All 135 inherited active inputs remain; the sole added proof module makes 136. The companion source is unchanged. These are source-retention counts, not a census of independent theorems.

The v69 checker covers retained exact controls, kernel-moment algebra, rate balances, finite successful-mark mixture identities, and ZIP-mode negative controls under normal and optimized Python. The native build freezes its actual Git source and retains all three complete PDFs, their source archive, logs and input manifests. Build success, hash agreement and finite controls do not certify the infinite-dimensional proofs; the new proofs and their geometric dependencies are submitted for independent examination.
