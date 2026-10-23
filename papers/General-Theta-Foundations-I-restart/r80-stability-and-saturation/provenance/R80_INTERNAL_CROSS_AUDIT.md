# R80 author-side mathematical cross-audit

This is an internal author-team AI check, not an independent human referee report, proof-assistant verification, editorial evaluation, or certification of worldwide novelty.

## Inspected sources

- Section 57: `/tmp/theta-math-structure/57-sharp-stability.tex`, SHA-256 `d7566b473142d8e87797a5929f17186b48d790754583d233799be1a8080d43ce`.
- Section 58: `/tmp/theta-math-challenge/58-arithmetic-saturation.tex`, SHA-256 `eb24afb20c54ca916293324a74ecc0a8c193489bae58d1030d956400013897de`.
- Current arithmetic diagnostic: SHA-256 `bb4184dabccce2900f184ab922e3a840c15722275e57f9acb6fc617314236a66`.

These are author-development source identities. The integrated revision verifier must bind its actual final source and execution separately.

## Section 57: sharp square-root stability

The following points were read independently of the derivation and checked directly.

1. The six controller probabilities cover arbitrary two-label stochastic command rows and command-conditioned stochastic updates, including unused labels. No converse restriction to the displayed realizing controller is introduced.
2. The two-state cost ordering is valid whenever both label values are finite; replacing routing by a preferable destination can also be justified by the old positive cost vector and finite-prefix iteration, so the properness comparison is not circular.
3. The zero-perturbation positive-polynomial identity has all required nonnegative factors in the stated orientation. Strict equality in the interior forces exactly the claimed zero coordinates. The inaccessible dark-label case is handled by its actual initial restriction, avoiding an invalid singular inverse.
4. In the opposite orientation, a proposed bound below the stated competing optimum implies `b >= 4`, `br < 1`, and `bs > 1`. These justify every division. The relaxed gamma substitution has positive denominator and the listed derivative signs on that same domain. Its minimizing endpoint and exact positive-root obstruction were recomputed.
5. Near the boundary optimum, the positive polynomial has uniform positive coefficients of gamma, delta squared, s delta and s squared. Its denominator is at most a constant times `s + delta + gamma`. This proves the stated coercivity, including the needed stronger `gamma = O(Delta * (s + delta))` bound.
6. Compactness and lower semicontinuity force every optimizer limit to the unique effective baseline program. No convergence of the unused update coordinate is necessary. The baseline cost comparison is monotone because the perturbed failure matrix adds a nonnegative matrix.
7. The trap identity gives `s + delta` bounded below at the square-root scale; its upper bound follows from coercivity. The nonnegative gamma term may be discarded in a lower estimate. The other model's routing improvement provides a bound for unrestricted alpha and xi, so their rates are not silently assumed.
8. The independently recomputed coefficients are `F = beta / D^2`, `S = r0 / (beta D)`, `L = (1-beta) r0^2 / (beta D^2)`, with `S-L = r0/D^2 > 0`. The optimizing escape coefficient and the leading constant agree with the text.
9. Unit costs and a fixed one-row fallback make this a primitive stability obstruction at fixed memory and fixed feasibility margin. The result does not contradict the stronger theorem assuming a positive success floor at every command.

An additional symbolic script independently expanded the polynomial, differentiated the opposite-orientation reduced function, checked its endpoint, checked the three Taylor coefficients, and verified the leading constant algebraically. Its output is `sharp57-symbolic-crosscheck.json`; the unqualified default interpreter initially lacked SymPy, and the successful command used `PYTHONPATH=/tmp/theta-r79-deps python crosscheck_sharp57.py`. Only that completed execution is a successful symbolic check. Floating display of the constant is an illustrative value, not part of the exact equality verification.

No substantive proof gap was found in this pass. Finite symbolic identities do not establish the compactness and limiting arguments; those were checked as written mathematical arguments.

## Section 58: arithmetic saturation and positive-memory realization

The structural family permits arbitrary positive command costs. The exact memory-one value is `ca/qa + cb/qb`. Its classical index is `pi * qa/ca * r^i` against `(1-pi) * qb/cb * s^j`.

The final native-layout pass split the long constant display and refined the index attribution to Blackwell as reported by Matula; no mathematical statement or proof changed. The full search lemma is expressly attributed to the two-location specialization of classical search theory, including the Clarkson–Lin–Glazebrook interior-prior/equalizer and at-most-two consistent-tie conclusions. The manuscript reproduces their necessary argument instead of claiming these facts as novel or using an undocumented minimax hypothesis.

The load-bearing points checked are:

1. A law on planned all-failure words corresponds to model-independent causal kernels because failure likelihood for a fixed command prefix is common to all its private implementations. Nonnegative costs allow Tonelli without an integrability assumption.
2. Fixed-count adjacent exchanges preserve all later survival probabilities. Infinite greedy optimality follows by finitely sorting each target prefix and taking monotone prefix limits, rather than assuming that an infinite bubble sort converges.
3. The upward finite risk set is convex and closed by cylinderwise compactness and finite-prefix cost continuity. Finite-dimensional separation supplies an actual least-favorable prior and robust attainment without swapping an unjustified infinite minimax.
4. For arbitrary positive costs, properness in both models forces a positive-probability wrong-command call in each model. Every finite prefix has positive failure likelihood, so both costs strictly exceed their respective known-model optima. Apply that fact to the already attained robust optimum to exclude endpoint priors. It is not a claimed uniform strict gap over all policies.
5. Tied items are disjoint adjacent pairs in the merged numerical lists. Their cost differences all lie on one Bayes-level line and sum absolutely. This proves that two extreme word risks suffice even when infinitely many ties exist.
6. Irrational log ratio permits at most one tied pair, after which all optimal words have an identical deterministic suffix with irrational symbol frequency. The support-set argument covers arbitrary stochastic finite controllers, not merely deterministic cycles. Its time after which the suffix is fixed is a deterministic finite time.
7. For rational log ratio, a fixed tie rule has a finite phase coset in a bounded interval. The counted initial-label construction realizes mixtures of finite tails by a legal command-conditioned update; it does not supply a persistent uncounted random seed or freely mixed initial label.
8. Strict finite-budget gaps use the inherited fixed-budget attainment theorem. Nonexistence of an attaining finite controller alone would not prove a strict value gap without that step.
9. The explicit rate, prior margin, tail constant and rational label cap are explicitly restricted to normalized costs `ca=qa`, `cb=qb`. They are not exported to arbitrary costs without new constants. The structural arithmetic dichotomy itself allows arbitrary positive costs.
10. For rational primitives, prime-exponent proportionality decides exact finite saturation. In the affirmative normalized case, the cap is computed with rational comparisons `t^(-J) >= (1-delta)/delta`; it needs no exact logarithmic-prior computation. Algebraic synthesis at that finite cap computes the history optimum. No exact computation or transcendence statement about the irrational history optimum is made.

The arithmetic diagnostic independently evaluated 9,180 finite words, 120 counted prefix-mixture controllers, exact product-chain costs, commensurate phase/cycle formulas, explicit powered tail bounds, the rational exponent criterion, the general-cost memory-one formula, and a finite irrational tied-pair/strip probe. It completed 21,237 exact conditions with zero floating conditions. Ordinary and `python -O` JSON outputs agree byte-for-byte. Those are finite diagnostics; the irrational nonperiodicity and universal no-finite-controller conclusion are supplied by the written proof, not by finite prefix enumeration.

## Remaining scope

The arithmetic classification applies to the displayed two-model search-type family. It is not an intrinsic finite-saturation criterion for arbitrary quantum instruments. The exponential finite-memory approximation has no claimed matching lower rate. The sharp stability coefficient is specific to its displayed model, while its positive square-root lower exponent applies to the full stated R79 class. Neither result solves the original general-M squared-sign minimax-risk frontier, the unrestricted-decoder approximation gap, or independent A1/A2/global geometric construction problems.


## Final targeted Section 57 reread

At the parent's request, the complete Section 57 source was reread at unchanged SHA-256 `d7566b473142d8e87797a5929f17186b48d790754583d233799be1a8080d43ce`, together with `R80_SHARP_DECLARED_STATEMENTS.json`. This was a targeted internal proof challenge, not an additional numerical or exhaustive-controller validation run.

No concrete proof gap was found. The reread checked finite/infinite and inaccessible-label cases before denominator divisions; the direction and applicability of a-failure routing improvements; the positive-polynomial equality conditions; opposite-orientation elimination, including the bs>1 domain and the attained endpoint; uniform coefficient bounds in coercivity; compactness and lower semicontinuity for arbitrary optimizing controllers; exclusion of a vanishing scaled escape rate; and the lower limit over all six stochastic parameters.

The coefficient declarations were recomputed analytically from the displayed rational costs: A=r0^(-2), F=beta/D^2, L=q*r0^2/(beta*D^2), S=r0/(beta*D), S-L=r0/D^2, k=beta/sqrt(q), and 2*sqrt(F*A*L)/(A+F)=2*sqrt(q)*r0^2/(D^2+beta*r0^2)=c0. The convex-combination weights cancel the arbitrary scaled r displacement H, and the arithmetic-geometric mean bound matches the explicit realizing controller. The unused xi coordinate and possible nonconvergence of that coordinate do not enter the argument.

The declarations accurately restrict the exact leading constant and optimizer rigidity to this displayed beta=1/4 family, while the exponent counterexample addresses the general inherited primitive-modulus class. A metadata completeness point was sent to the declaration owner: the sharp-modulus theorem's direct dependency list should explicitly include `thm:r79-frontier-stability` for its stated inherited-exponent consequence. This is a dependency-map correction, not a mathematical proof defect. No additional finite tests were run in this reread.
