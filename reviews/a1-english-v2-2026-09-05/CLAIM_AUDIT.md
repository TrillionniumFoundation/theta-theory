# A1 English-v2: statement-by-statement audit

Reviewed source tree: `900059b847980a27be4866d495b00eeb96562dc5`.

This table covers all **63** proof-bearing entries in the author's `PROOF_LEDGER.md`. Numbers and line starts are taken from that source ledger; PDF page claims were not independently verified. The complete numbered sections and four appendices were read, not just the excerpts at these line starts.

**Status vocabulary:** `C` = argument inspected, no specific mathematical objection identified under its stated/intended hypotheses; `H` = a printed scope requires the explicit repair in the report; `T` = valid-looking conditional/transfer argument whose model-specific inputs remain to be established; `M` = concrete model result inspected. None of these codes means formal certification or a positive novelty verdict. `M1`, `M2`, `M3`, and `S1` refer to findings in [REFEREE_REPORT.md](REFEREE_REPORT.md).

Paths in the third column are relative to `source/sections/`.

| Statement | Label | Source / start line | Status | Referee assessment |
|---|---|---|---|---|
| Theorem 2.1 | `thm:instrument-path` | `02_instruments.tex:24` | C | Standard chronological kernel extension; normalization and deterministic specialization are correct. |
| Proposition 2.2 | `prop:likelihood` | `02_instruments.tex:48` | C | Common policy factors cancel at the realized history, not after conditioning on the final design. |
| Proposition 2.3 | `prop:pointer` | `02_instruments.tex:68` | C | Canonical shear and back-action agree with Hamilton's equations; no universal energy price follows. |
| Lemma 2.4 | `lem:instrument-stability` | `02_instruments.tex:102` | C | Evidence-weighted variation estimate uses the declared factor-of-two TV convention consistently. |
| Lemma 3.1 | `lem:flow` | `03_mechanics.tex:12` | C | Local flow/variation calculation on the common regular neighborhood; standard Gronwall mechanism. |
| Proposition 3.2 | `prop:reflection` | `03_mechanics.tex:37` | C | Mass-metric reflection, involution, conservation and flux calculation are consistent. |
| Proposition 3.3 | `prop:balance` | `03_mechanics.tex:57` | C | Finite-flight telescoping includes impact jumps and the terminal convention. |
| Theorem 4.1 | `thm:character` | `04_selection.tex:3` | C | Continuous positive multiplicative character is an exponential; classical functional equation. |
| Theorem 4.2 | `thm:gibbs` | `04_selection.tex:20` | C | Bounded-source Gibbs gap and extended entropy handling are sound. |
| Proposition 4.3 | `prop:cumulants` | `04_selection.tex:33` | C | Bounded exponential domination and partition cumulants; no global complex log is asserted. |
| Proposition 4.4 | `prop:constraints` | `04_selection.tex:52` | H | M1: explicitly reset B=0 or retain QB and change the minimized objective. Event-conditioning branch unaffected. |
| Theorem 5.1 | `thm:real-gap` | `05_realizability.tex:9` | C | Direct infimum of Gibbs gap; zero deficit without attainment does not imply implementation. |
| Theorem 5.2 | `thm:coarse-prep` | `05_realizability.tex:36` | C | Conditional-mean source is correct for constrained preparation; equality criterion follows from strict Jensen. |
| Proposition 5.3 | `prop:coarse-expansion` | `05_realizability.tex:59` | C | Nested classes and total-variance expansion; fixed reference/statistic conditions are explicit. |
| Theorem 5.4 | `thm:cap` | `05_realizability.tex:83` | C | Clipped exponential and uniqueness follow from strict concavity and normalization. |
| Proposition 5.5 | `prop:cap-response` | `05_realizability.tex:101` | C | Two optimality inequalities plus Pinsker give the TV constant; first-order value envelope is appropriately scoped. |
| Proposition 5.6 | `prop:acceptance` | `05_realizability.tex:118` | C | Correct acceptance law and geometric count under actual independent repetitions. |
| Theorem 6.1 | `thm:projection` | `06_information.tex:9` | C | Conditional exponential source and tower identity, distinct from coarse preparation. |
| Proposition 6.2 | `prop:jensen` | `06_information.tex:22` | C | Conditional Hoeffding-type bound with oscillation squared divided by eight. |
| Theorem 6.3 | `thm:entropy-chain` | `06_information.tex:34` | C | Conditional density factorization handles negative parts before extended-value integration. |
| Proposition 6.4 | `prop:hidden-tangent` | `06_information.tex:49` | C | Quadratic entropy loss is conditional variance; boundedness controls remainders. |
| Theorem 7.1 | `thm:history-doob` | `07_chronology.tex:15` | C | Telescoping includes initial-history reweighting and may change action factors. |
| Proposition 7.4 | `prop:entropic` | `07_chronology.tex:45` | C | Tower, Lipschitz property and convex/concave sign distinction hold for the fixed reference law. |
| Proposition 7.5 | `prop:dirac-linear` | `07_chronology.tex:57` | C | Dirac evaluation is linear; no coarse semigroup is inferred. |
| Theorem 8.1 | `thm:finite-state` | `08_predictive_states.tex:20` | C | Exact all-tests predictor is Borel and sufficient for a common continuation rule; not a reduction theorem. |
| Proposition 8.2 | `prop:minimal` | `08_predictive_states.tex:34` | C | Countable measurable coordinate factorization, not finite-dimensional minimal realization. |
| Theorem 8.3 | `thm:response-state` | `08_predictive_states.tex:47` | C | Finite sums permit adaptive jet comparison; quotient update needs positive evidence. |
| Theorem 9.1 | `thm:continuous-state` | `09_continuous_experiments.tex:21` | C | Compact positive-density quotient argument resolves common-version and continuous-update issues. Not automatic for the complete Lorentz record; see S1. |
| Theorem 10.1 | `thm:budget-dpp` | `10_resources.tex:7` | C | Finite backward induction preserves residual budget and feasible continuations. |
| Proposition 10.2 | `prop:continuous-dpp` | `10_resources.tex:26` | C | Upper/lower hemicontinuity and compactness support continuous maxima and Borel selection. |
| Theorem 10.3 | `thm:info-dpp` | `10_resources.tex:46` | T | Entropy chain gives additive cost under fixed updates, implemented kernel classes, and legal pasting. Those are substantive inputs. |
| Lemma 11.1 | `lem:normalization` | `11_approximation.tex:3` | C | Conservative normalization and tilt constants are valid. |
| Proposition 11.2 | `prop:tv-budget` | `11_approximation.tex:19` | C | Conditioning cost and chronological TV accumulation explicitly charge evidence and initial error. |
| Theorem 11.3 | `thm:test-tilt` | `11_approximation.tex:46` | T | Correct numerator/denominator algebra, requiring control of the actual weighted tests. |
| Proposition 11.4 | `prop:coupling` | `11_approximation.tex:64` | T | Coupled weak-test estimate is useful when the stated report/source coupling is established. |
| Theorem 11.5 | `thm:jet-error` | `11_approximation.tex:85` | T | Quotient-jet perturbation recursion is consistent; derivative errors are inputs, not consequences of value convergence. |
| Theorem 11.6 | `thm:value-error` | `11_approximation.tex:106` | T | Finite-horizon continuation-test bound requires common feasible actions and actual next-report error. |
| Theorem 12.1 | `thm:regular-response` | `12_response.tex:5` | C | Product/quotient differentiation requires the printed variation regularity; not applicable to S1's full record. |
| Theorem 12.2 | `thm:shape` | `12_response.tex:37` | H | M2: branchwise density requires two traces, or an explicit globally matching density trace. |
| Lemma 12.3 | `lem:dirac` | `12_response.tex:59` | C | Fourier summability at exponent > d/2+r supports strong Dirac jets and dominated Bochner integration. |
| Lemma 12.4 | `lem:sum` | `12_response.tex:73` | T | Standard uniform derivative summation criterion; no model-specific tail estimate supplied by the criterion itself. |
| Proposition 13.1 | `prop:saltation` | `13_hybrid.tex:9` | C | Fixed-comparison-time correction and parameter terms have the correct signs. |
| Theorem 13.3 | `thm:chamber` | `13_hybrid.tex:48` | H | M3: trajectory conclusion is sound; integral/law conclusion needs fixed or regular preparation, not just fixed support. |
| Theorem 14.1 | `thm:assembly` | `14_assembly.tex:5` | T | Banach-valued fundamental theorem of calculus under a full Cauchy hierarchy. Does not prove that hierarchy for long billiard histories. |
| Corollary 14.2 | `cor:tail-budget` | `14_assembly.tex:19` | T | Summable increment bounds give explicit tails once established for the same physical assembly. |
| Proposition 15.1 | `prop:lorentz-geometry` | `15_lorentz_local.tex:10` | M | Disk separation, compactness finite-horizon argument, regular-flow null sets and normalized flux are plausible as proved. |
| Proposition 15.2 | `prop:roof` | `15_lorentz_local.tex:26` | M | Mean roof and marked two-period ratio are correct; only marked constant-time equivalence is excluded. |
| Lemma 15.3 | `lem:tube` | `15_lorentz_local.tex:56` | M | Conservative local geometric margins and one-collision horizon are consistent. |
| Theorem 15.4 | `thm:local-hit` | `15_lorentz_local.tex:80` | M | Moving lower endpoint and distributional Bell signs are correct for the fixed smooth beam preparation. |
| Lemma 16.1 | `lem:tube-jacobian` | `16_lorentz_global.tex:47` | M | R*cos(phi) Jacobian; one-collision gap gives injectivity and coverage up to null sets. |
| Theorem 16.2 | `thm:global-tube` | `16_lorentz_global.tex:57` | M | Exact subtract-and-replace identity; assembled positivity, not termwise positivity. |
| Theorem 16.3 | `thm:global-response` | `16_lorentz_global.tex:87` | M | Credible strong negative-Sobolev proof for the stated density and smooth tests; S1 prevents an unrestricted likelihood interpretation. |
| Corollary 16.4 | `cor:global-hit` | `16_lorentz_global.tex:133` | M | p=2RT/A_R, positive first/second derivatives and recursion checked independently. |
| Theorem 17.1 | `thm:binary-info` | `17_observation.tex:5` | M | Smooth positive Bernoulli probabilities give identification, Fisher information and QMD. It is a coarsened experiment. |
| Theorem 17.2 | `thm:channel-info` | `17_observation.tex:26` | C | Mixture-channel lower/upper information bounds and square-root envelope are consistent. |
| Proposition 17.3 | `prop:smoothing` | `17_observation.tex:49` | T | L1 response follows from the joint channel/mechanical derivative envelope. That envelope must be verified for each proposed instrument. |
| Proposition 18.1 | `prop:direction-prep` | `18_operational_examples.tex:5` | M | Fixed-direction footprint has area 2RT; restricted value and nonzero deficit follow. |
| Theorem 18.2 | `thm:lorentz-selection` | `18_operational_examples.tex:34` | M | Parameter-independent postselection and bounded-trial conditional output are correct; failure mass remains. |
| Proposition 18.3 | `prop:calibration-error` | `18_operational_examples.tex:63` | C | Binary conditional supports yield exact TV reduction; logistic derivative gives the quarter constant. |
| Theorem 19.1 | `thm:diagonal` | `19_limits.tex:5` | T | Selection/conditioning budget follows from previous inequalities; actual approximation rates are separate inputs. |
| Proposition 19.2 | `prop:bilateral` | `19_limits.tex:59` | T | Geometric interpolation exponents are algebraically correct; the same physical atom must satisfy both bounds. |
| Theorem 20.1 | `thm:synthesis` | `20_synthesis.tex:2` | T | Conjunction of established short-time claims with conditional applications; not yet a deep new integrated model theorem. |
| Lemma A.1 | `lem:pinsker` | `A_measure.tex:19` | C | Bernoulli reduction gives Pinsker with the stated TV normalization. |

## Additional text inspected

Examples 7.2 and 7.3 are finite consistency counterexamples rather than extra proof-ledger entries. Assumption 13.2 is assessed with Theorem 13.3. The stopped marked-clock balance, the current/roof implicit differentiation, and the conditional generator calculations were read with their printed qualifications. Appendices A–D were inspected for extended-value handling, common versions, Bell/implicit/quotient recursions, threshold signs, finite examples, and provenance claims.

The referee has not separately re-audited the historical A1/A3/C2/CM2 repository sources cited as provenance, all branches of the eleven-paper series, or every bibliographic theorem in full text. The reviewed A1 re-proves the geometric statements it uses; this audit does not import historical correctness from repository status labels.

## Priority for a response letter

A response should give exact revised statements for M1–M3, state the complete-record separation in S1, identify the actual shared observation/instrument when combining theorems, and address the contribution objection with a substantive theorem or a precise literature comparison. A passing finite check or additional proof-ledger rows is not a response to the significance assessment.
