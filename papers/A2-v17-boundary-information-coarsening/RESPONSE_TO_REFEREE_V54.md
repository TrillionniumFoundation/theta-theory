# Response to the independent report on A2 revision 53

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 54, September 15, 2026

The report addressed is `reviews/a2-v53-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at `000ce24f65f8381d2180cbd1f080d3d8470c8157`. It reviews source `42cc62f230473c34d78af1d06b9ca5c2651ae86d`, not the older v50 source. The report and its audit ledger were read completely. They identify no mandatory correction to the three new v53 statements. This response preserves that disposition and distinguishes the requested mathematical improvements from the nonbinding publication assessment.

## 1. Changes in the article

We have strengthened Corollary 23.3 in place and completed its interpretation in the same Section 23 with Theorem 23.4. No separate research section is appended. Theorems A and B, the actual geometric realization, the attained conditional-mark scale, the window inverse, the finite geometric fibers, the unknown-lattice and differential theorems, and all older quantitative and calibration statements remain unchanged.

The revised corollary gives `H^2 <= C tau^(2J)` per successful record and `TV <= C sqrt(n) tau^J` for the product experiment, uniformly in the small window. It separately gives a direct exponential bound for the bounded-moment test when `tau^J=o(h^4)`. The added theorem uses the actual acceptance probabilities of the same two tables to compare an accepted mark with its repeat-to-first-acceptance transcript. Their reverse binary deficiency tends to one half. It then proves the limiting optimal error under a deterministic preparation cap, including a necessary and sufficient consistency criterion. Thus the sample-size, finite-flight and charged-record statements now have their own explicit experiments and quantifiers within one argument.

The Hellinger improvement and the uncapped waiting-record comparison are credited to Sections 4 and 5 of the referee memorandum in the article, acknowledgments and bibliography. The deterministic-cap risk calculation is developed here from the same stopped experiment. We do not present tensorization, binary testing identities or geometric waiting laws as new general principles.

## 2. R53-Q1: finite-flight comparison and direct testing

The proof preceding the old corollary already supplies an interior supremum-norm estimate on one fixed physical square, uniform in the family. After recording and cropping, both the unnormalized integral error and its normalizer have area order `h^2`. The revised proof retains this cancellation rather than applying a generic conditional-TV inequality which loses inverse window area.

After shrinking the fixed collar and increasing the minimum flight, both rescaled densities have a common lower bound `m>0`. The explicit estimate is

`H^2(P,Q) = integral (p-q)^2/(sqrt(p)+sqrt(q))^2 <= m^(-1) ||p-q||_infinity^2`

on the square of area four. Affinity tensorization then bounds product squared Hellinger by the sum of the one-record squared distances, for any fixed allocation among the four labels. This proves `TV <= min(1,C sqrt(n) tau^J)`. Expectations of all [0,1]-valued tests, and their optimal equal-prior risks after infimization, obey the same comparison. Consequently `n tau^(2J) -> 0` suffices for all three conditional testing regimes. The old sufficient condition and old error bound are explicitly retained as weaker consequences; no old assertion has been made false by the replacement.

At the critical scale `n h^8` of constant positive order, `tau^J=o(h^4)` suffices. The corollary prints a joint even-flight choice with coefficient `(4+epsilon)/|log tau|` in front of `log(1/h)`, not the former stronger coefficient associated with `tau^J=o(h^8)`. This is a sufficient coefficient for the supplied convergence rate, not an optimal geometric convergence exponent.

For the direct mean test, let `D_h=mu_1(h)-mu_0(h)=c_0 h^4+O(h^6)>0`, with the two exact ideal means. Each finite-flight mean is within `C tau^J` of the corresponding ideal mean. Under `tau^J=o(h^4)`, the same midpoint has distance at least `D_h/4` from every finite-flight mean, on the correct side. The range-one exponential inequality gives `exp(-n D_h^2/8) <= exp(-c' n h^8)` directly under the finite-flight laws. This statement does not require a small distance between the entire growing product experiments. That distinction is printed in the statement, proof and introduction.

## 3. R53-Q2: the same actual pair with waiting counts retained

The two tables keep their gap fixed, but have contact curvatures `80/7` and `40/3`. Their exponents are therefore `gamma_0=arcosh(71/7)` and `gamma_1=arcosh(35/3)>gamma_0`. The positive fixed-offset law and recorded mass yield

`p_i(h) = pi_i,J r_i,J(h) asymp h^2 exp(-gamma_i J)`,

so `rho_h=p_1/p_0 -> 0` along any even `J_h -> infinity`. The recording profiles are the original fixed ones; they are not adjusted with h or J to manufacture this ratio.

For independent preparations, the article proves the exact identity

`P_i(W=k,Y in A) = (1-p_i)^(k-1) p_i Q_i,J,h(A)`.

Hence deleting W gives precisely the conditional finite-flight mark from the same acquisition, not the output of a different protocol. The terminal mark becomes indistinguishable, with TV bounded by `C(h^4+tau^J)`, while the threshold `ceil((p_0 p_1)^(-1/2))` on W has errors bounded by `exp(-rho_h^(-1/2))` and `sqrt(rho_h)+p_1`. There is no assumption relating h and J beyond their separate limits for this one-record comparison.

Theorem 23.4 defines binary deficiency explicitly, proves the zero deficiency in the forgetting direction, and gives both bounds for the reverse limit. The lower bound uses contraction and a triangle inequality. The upper bound is a legitimate parameter-independent kernel returning the equal mixture of the two full laws. The resulting limit is exactly one half, not merely a positive information loss. Its thresholds and kernels may depend on the two specified hypotheses, not on the unknown generating alternative.

## 4. Deterministic preparation caps: the same record, with a charge guaranteed in advance

The old corollary's identity `E W=1/p_i` is unchanged. We agree that this expectation cannot itself give a deterministic-cap guarantee. The new theorem instead defines the capped experiment explicitly: output `(W,Y)` if the first acceptance occurs by a fixed integer `b_h`, and a cemetery outcome otherwise. At most `b_h` preparations are used, and a failed preparation retains only its acceptance/failure symbol. No raw position or residual-time information from failed shots is supplied.

Let `a_i=1-(1-p_i)^b`. Eventually `p_1<p_0`, and the two capped laws share a cemetery mass of at least `1-a_0`. Their total variation therefore satisfies

`a_0-a_1 <= TV(F_0^[b], F_1^[b]) <= a_0`.

If `b_h p_0 -> lambda < infinity`, then `b_h p_1 -> 0`, `a_0 -> 1-exp(-lambda)` and `a_1 -> 0`. This proves that the *optimal* equal-prior error tends to `exp(-lambda)/2`. The simple event test deciding zero exactly upon any acceptance by the cap attains this limit. The argument uses a common atom and applies to the full capped mark/count record; it does not assume identical accepted marks or a small approximation error for a large sample.

For arbitrary cap sequences, consistency holds exactly when `b_h p_0 -> infinity`. Sufficiency uses the observable threshold `min(b_h,ceil((p_0 p_1)^(-1/2)))`. Necessity follows by extracting a bounded subsequence of `b_h p_0` and applying the finite-lambda risk limit. The exact charge is `E min(W,b)=[1-(1-p)^b]/p`, derived by summing the survival probabilities. This includes every unsuccessful preparation.

The corresponding critical order is `p_0^(-1) asymp h^(-2) exp(gamma_0 J_h)` for this specified stopped binary experiment. It is not a universal physical inverse complexity, a comparison optimized over all flight designs, or an estimator over arbitrary unknown detector profiles. In particular, the experiment can stop without ever observing a successful mark under the rarer alternative. Such negative evidence cannot be inserted retrospectively into the successful-mark experiment by calling its cost ancillary.

## 5. Disposition of the remaining technical findings

| Referee item | Disposition and manuscript treatment |
|---|---|
| R53-M1: normalized h^4 density contrast, h^8 Hellinger coefficient, and moments | Lemma 23.1 and its complete proof remain verbatim. The old finite controls are retained and rerun through the v54 checker. |
| R53-M2: actual noncircular support family and fixed admissible profiles | Theorem 23.2's geometry, half-line Hessian, clearance and recording construction remain verbatim. Higher nonlinear action coefficients are not suppressed. |
| R53-M3: subcritical, critical and supercritical testing regimes | The theorem and proof remain verbatim. No unrestricted-profile minimax meaning or preparation lower bound is assigned to its h^(-8) successful-record scale. |
| R53-M4: uniform shrinking crop and accepted mass | The corollary is strengthened as described above, preserving the area cancellation, all mass formulas and expected n-success charge. |
| R53-M5: nonlinear relative amplitude, gluing and trace-class mechanism | The complete source is unchanged. The main proof architecture and its exponentially small reference remain the forward foundation. |
| R53-M6: actual-smooth finite remainders before signed jet inversion | The complete source is unchanged. There is no replacement by formal jets or order-uniform conditioning. |
| R53-M7: interior-window, global matching and differential interfaces | All statements and proofs remain unchanged. Critical-line visibility, signed units, exact offsets, true gain-matrix inversion and common-strip analytic variations retain their respective roles. |

Previously closed calibration, support-centering, attribution and finite-fiber issues are not reopened. The richer physical pilot, the hard-category perturbation bounds and the cap accounting in Part III retain their original sensors and quantitative margins. A fresh proof certification of every old statistical theorem is not claimed by this revision.

## 6. R53-E1–E3: contribution, article scope and attribution

We agree that a finite number of law-valued channels is not a finite scalar observation, that local smooth extraction is not an unrestricted noisy inverse, and that two-point testing with specified nuisance alternatives is not a uniform unknown-nuisance procedure. Those distinctions remain part of the actual theorem hypotheses, not qualifications relegated to this letter.

The article continues to rest on the relative physical boundary measure and the signed actual-smooth geometric inverse. The revised Section 23 now demonstrates within one realized family exactly how normalizing or retaining the accepted mass changes inferential content. The conditional scale, reverse deficiency and capped-risk limit give complementary, explicitly different consequences of that measure. The finite-flight improvement belongs inside the existing corollary, and the waiting/cap result belongs beside its mass calculation; we have not introduced another disconnected part or a second introduction.

These improvements are submitted for evaluation, not asserted to compel a favorable journal decision. We neither downgrade correct structural conclusions nor claim that their checksums or accumulated theorem count settle significance. The author-requested AI-assisted reports remain identified as memoranda, not commissioned journal reviews.

The targeted primary-record check is retained in `LITERATURE_CHECK_V54.md`. Osius's established association framework is credited; the spectral comparators retain their different observations and version-specific scopes. No reduction between marked-length and boundary-law experiments, exhaustive priority claim, or renewed validity of Florio–Leguil's removed geometric assertion is alleged.

## 7. Preservation and verification

All 111 inherited active inputs remain active in their former relative order. 107 are byte-identical in place; four exact originals and the v53 native manifest are archived in `history/v53-review-baseline/`. Of the 544 inherited statement/proof blocks, 542 are preserved verbatim. The two exceptions are exactly Corollary 23.3 and its proof, strengthened in place; their original bytes remain in the archive, and every former conclusion is explicitly retained as a consequence. One theorem and proof are added. The complete catalogue still compiles in Appendix A.1, and the companion is unchanged.

`check_revision_v54.py` checks these identities, exact changed-file transformations, all labels/citations, inherited finite diagnostics, Hellinger/tensorization controls, direct-test constants, capped law normalization and charge, the common-atom bounds and necessary negative controls. It uses explicit guards in ordinary and optimized Python. These are finite checks, not a theorem prover. Full native builds, post-download verification and actual sampled visual coverage are identified in the final `REVIEW_READY_V54.md` ledger. Only new revision branches are used; A1, unrelated workstreams, past reports, the default branch and repository permissions remain untouched.
