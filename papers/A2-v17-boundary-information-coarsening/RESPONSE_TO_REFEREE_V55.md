# Response to the two referee memoranda on A2 revision 54

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** A2 v55, September 15, 2026

This response addresses both reports on the actual v54 mathematical source `2cedae961195f97df802aaa81112d95cd32974e1`. The first report is frozen at `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4`, in `reviews/a2-v54-independent-harsh-top4-2026-09-15/`. The later, second memorandum is frozen at `67250d08714acf76274e82158f107246f0de7eee`, in `reviews/a2-v54-second-referee-top4-2026-09-15/`. The revision starts from the latter and preserves both reports. Their shared review-ready baseline is `802cb27e731a3a821903a7308cba9d5da29bbf79`.

## 1. Disposition and the scope of this revision

We thank both referees for distinguishing the successful technical examination from their separate judgment about placement. Neither report establishes a new fatal theorem error or requires a mandatory correction to Corollary 23.3 or Theorem 23.4. The earlier Hellinger, waiting-record and deterministic-cap points therefore remain closed. We do not characterize this revision as repairing a false v54 theorem, and do not claim that another verified consequence settles the editorial reservation.

The revision completes the interpretation of the existing stopped experiment in place. Theorem 23.4 retains its three original clauses and their entire proof text; two further clauses and their proofs identify exactly how the full record reduces to the censored count and, at finite cap intensity, to an acceptance bit. There is no new theorem number, new section, new geometric family, or new hypothesis on Theorems A and B. The nonlinear relative boundary law and actual-smooth signed inverse remain the article's principal mechanism.

The new reductions are attributed jointly to the first memorandum's R54-Q1–Q3 and the second memorandum's Section 4. Their overlap is acknowledged, not counted as two independent contributions. The exact full-record overlap formula is printed alongside the count formula so that the latter cannot be misread as the full finite-sample risk.

## 2. First report R54-Q1; second report Section 4: count sufficiency

For the original actual table/profile pair, write `eta_h=TV(Q_0,Q_1)` and `a_i(b)=1-(1-p_i)^b`. The expanded theorem defines three actual records of the same stopped acquisition: the full pair with its cemetery outcome, the censored waiting count with its cemetery outcome, and the acceptance bit. In particular, a censored count distinguishes success at the final preparation from no success by that preparation.

The count-to-full simulation retains each accepted count and independently appends a mark from the zero-alternative law, preserving the cemetery symbol. It is one kernel for both alternatives. Under zero it is exact; under one its error is exactly `a_1(b) eta_h`, because accepted-count components are disjoint. The proof gives both deficiency directions and the sharper equal-prior risk comparison:

`delta(F^[b],C^[b])=0`, `delta(C^[b],F^[b]) <= a_1(b) eta_h`,

`0 <= R_C^*(b)-R_F^*(b) <= a_1(b) eta_h/2`.

Since `eta_h -> 0`, the experiment comparison is uniform over every deterministic cap, including caps increasing much faster than either inverse success probability. The uncapped version follows by summing the infinite geometric series. The kernel preserves the observed count, censoring flag and therefore the realized preparation charge pointwise. This is stronger bookkeeping than matching an expected charge, but is not a new sampling protocol.

The estimate is an absolute error bound. We explicitly do not turn it into a relative-error approximation to very small risks, a kernel uniform over unrestricted unknown profiles, or a claim that terminal marks are exactly ancillary at finite sample size. The finite controls include cases in which unequal marks strictly improve the full risk.

## 3. First report R54-Q3; second report Section 4: the exact finite count risk

For `0<p_1<p_0<1`, the count likelihood ratio decreases strictly with the accepted count. The theorem prints the exact threshold

`K_b=min{b,floor[1+log(p_0/p_1)/log((1-p_1)/(1-p_0))]}`

and the count-only equal-prior risk

`R_C^*(b)=[(1-p_0)^K_b+1-(1-p_1)^K_b]/2`.

The proof includes the cemetery likelihood and permits either decision at an exact likelihood tie. The geometric convention is one-based: the successful preparation is included in the waiting count. No continuous threshold approximation replaces the integer formula.

A separate displayed identity gives the full risk as half the sum of the smaller cemetery mass and the overlap integral over all accepted-count components. This identity allows arbitrary terminal mark laws dominated by a common measure. Consequently the distinction between an exact count formula, an exact full overlap identity and their controlled absolute difference is visible in the theorem itself, not only in the response.

## 4. First report R54-Q2: the finite-intensity bit experiment

On an acceptance bit equal to zero, the reverse kernel returns the cemetery symbol. On a bit equal to one, it draws the entire stopped pair according to the zero-alternative law conditional on acceptance by the cap. Under zero it is exact, while under one its error is at most `a_1(b)`. This does not require the two terminal mark laws to be close.

When `b_h p_0,h -> lambda < infinity`, the theorem now proves convergence of the full experiment in Le Cam distance to the two-point experiment whose acceptance probabilities are `1-exp(-lambda)` and zero. The proof prints an explicit bound in terms of `a_1` and the differences between the two actual Bernoulli probabilities and their limits. It includes `lambda=0`. The old limiting risk `exp(-lambda)/2` is preserved and its experiment-level meaning is now explicit.

The finite-intensity restriction is not dropped. The same statement proves that when `b_h p_1,h -> infinity`, the acceptance bit has risk tending to one half while the count/full experiment has risk tending to zero, with reverse bit-to-full deficiency tending to one half. This supplies a precise boundary to the bit reduction rather than using the any-acceptance rule for every cap. The earlier optimal truncated waiting threshold and the necessary-and-sufficient cap criterion remain unchanged.

A statistical simulation from a bit need not preserve the original realized stopping time. The final proof explicitly contrasts it with the count-preserving kernel. Neither simulation changes the real acquisition's deterministic cap or the tail-sum charge formula.

## 5. Closed technical interfaces: first R54-M1–M8; second M1–M9

The strengthened Corollary 23.3 is unchanged, including uniform pre-crop density control, the cancellation of both window-area factors, the common positive density floor, Hellinger tensorization, `C sqrt(n) tau^J` product comparison, and the separately proved direct mean-test bound. No weak-convergence argument is substituted for the fixed-collar estimate and no uniform statement is inferred after removing its density floor.

The actual noncircular support family, its fixed profiles, the nonlinear action expansion, critical likelihood coefficient, attained successful-record scale, physical hyperbolic exponents, first-acceptance factorization, two deficiency directions, deterministic-cap lower bound and full charge all retain their original text. The profiles are fixed as the window shrinks but may differ between the specified alternatives. The thresholds may depend on those two hypotheses, not on which one generated the data.

The inherited relative determinant and signed actual-smooth contact mechanisms, interior-window extraction, finite matching and unknown-lattice inverse, and differential-kernel proofs are unchanged. In particular, common-strip analyticity concerns the variation; finite-dimensionality is used only for scalar local coordinates; finite rotations are not assumed to persist after symmetry breaking; the marked gain matrix is genuinely inverted.

The second report's additional calibrated-histogram examination is respected without broadening it into a certificate of all the underlying pilot theory. The full calibrated source remains byte-identical: internal and outer cell edges, timing amplification, pilot-history bounds, uncapped comparison and failure charges are preserved. No claim of calibration from transverse histograms alone is introduced. We retain the separate sensors and quantitative margins of Part III.

## 6. E1–E3: the article-level case

The revised abstract and the existing acquisition/information subsection now name the stopped experiment's sufficient record and its cap-dependent reduction. This makes the common-measure interpretation concrete without equating all experiments. Normalized endpoint interaction and accepted mass are two different outputs of the relative physical measure. The former supports the geometric inverse; the latter carries the stopped discrimination of this pair. Their roles are not interchangeable.

Our case for the central theorem continues to rest on the flight-independent nonlinear collar, normalization relative to an exponentially small twist, and the actual-smooth finite-remainder factorization preceding the signed inverse. The exact law-valued observation, marks, gaps, signed physical units and visibility conditions remain explicit. The independent count/bit calculations use standard probability arguments once the actual table laws have been obtained; we do not present them as a second geometric breakthrough or a universal unknown-nuisance theory.

The three-part dependency order, the complete compiled technical catalogue and every valid inherited mathematical claim are retained. The main rigidity target is not replaced by a smaller theorem in response to a nonbinding placement judgment. At the same time, no assertion is made that the reviewers' significance reservation is mechanically resolved by this expansion or by a build. The manuscript is offered for renewed assessment of the same substantive inverse and its now more fully identified observation models.

## 7. Preservation and verification

All 111 inherited active inputs remain active in their original relative order. Four exact amended-file originals and the source-matched manifest are archived under `history/v54-review-baseline/`; 107 active inputs remain byte-identical in place. Of 546 inherited statement/proof blocks, 544 are verbatim. The remaining two are Theorem 23.4 and its proof with inserted material only: removing the new insertions reproduces their old bytes exactly. The full inventory, including 257 proofs, is unchanged. No new theorem or proof environment is added.

`tools/check_revision_v55.py` checks these facts and 90 exact finite marked/count laws, including equal, unequal and disjoint mark distributions; tie decisions; the full overlap formula; simulation errors; preservation of charge; finite-intensity limits; and large-cap negative controls. Earlier finite controls are rerun. Ordinary and optimized Python must agree. These are finite diagnostics, not an infinite-operator or mathematical certificate.

The version-scoped workflow builds both complete entries from actual committed source, retains the PDFs/source/evidence as Git objects, and verifies the fetched product branch. The final review ledger records the completed source and products, actual warnings and actual visual coverage. Neither workflow preparation nor this response is used to assert success before it occurs. Both v54 reports remain separately identifiable and are not rewritten. These author-requested AI-assisted memoranda are not actual journal evaluations.
