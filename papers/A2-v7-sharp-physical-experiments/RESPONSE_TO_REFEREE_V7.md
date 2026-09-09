# Response to the independent referee memorandum on A2 v6

**Manuscript:** Relative Boundary Laws and Statistical Reconstruction in Periodic Dispersing Billiards  
**Author:** Qian Qi  
**Revision:** A2 v7, September 9, 2026

## Version and preservation

This response addresses the report on `review/a2-v6-relative-transfer-harsh-independent-2026-09-09`, frozen at `f1728f5d96ea01b1326daf9a6a36352b2e270be1`, report blob `2a82c198d758a10e0dd2414192d2155c542f2df1`. The reviewed manuscript is the complete materialized A2 v6 at `4ca186258c92dcbc75accc4eb576e307cc612189`, not one of the earlier partial v6 pointers.

We have preserved the general forward theorem, its absence of finite-horizon and symmetry assumptions, and the complete analytical and inverse development. The new manuscript directory is constructed from the full reviewed subtree. No inherited source is deleted. Every previously active mathematical body file is still an active input; the bibliography retains every original key in author–year form. The old entry points are separately archived. The changes below add proofs and distinguish their statistical roles rather than replace the paper by a narrower note.

We thank the referee for separating previously resolved mathematical points from the remaining questions of observation, interpretation, significance, and evidence. The present response addresses V6-R1–V6-R4 individually. The report's tangent overlap and physical two-point construction are credited where used; they are not presented as new priority claims by the author.

## V6-R1 — State the experiment and asymptotics in one place

**Change.** The new introduction begins with the distinction between identifying a physical parameter, approximating a statistical experiment, and acquiring the observations. Table `tab:v7-experiments` gives four separate rows: long-bridge endpoint/residual experiments; fixed-order contact coefficients; unlabelled Bernoulli acquisition with `J=3` or `4`; and selected-position acquisition at odd flight numbers.

Each row records the actual observation, supplied side information, unknown object, error topology, preparation cost, and variables in the uniformity statement. In particular:

- The long-bridge row retains the failure symbol in a raw preparation and charges the inverse success probability when successful records are collected. A fixed-excess schedule requires a supplied or calibrated onset; scaling in the proof is not a free gap observation.
- The fixed-jet row is a deterministic coefficient-data theorem, uniform in flight number at each fixed jet order. It is not assigned a raw-sampling rate or a uniform-in-jet-order condition number.
- The count row uses only the indicator `1{N_t >= j+1}`. Its coarse bracket is supplied; the fine pilot is charged; its flight numbers and extrapolation order are fixed while the offset shrinks.
- The position row retains selected endpoints and its distinct bracket `|j(g-g0)| <= h/4`, and charges both fine calibration and selection. Its Lipschitz curvature inverse is not attributed to the count datum.

The complete-array comparison is explicitly left in its retained bounded-Lipschitz topology. The new total-variation results concern the common endpoint/residual observation space, not distinct embedded full-record surfaces.

**Locations.** `v7/00_introduction.tex`, Table `tab:v7-experiments`; retained `v6/10_experiment_transfer.tex`, `v6/40_count_only_acquisition.tex`, and `v5/50_self_calibration.tex`.

## V6-R2 — Give rigorous statistical benchmarks without unsupported optimality

### R2(a): Moving supports and growing successful samples

**Change.** Proposition `prop:v7-overlap` gives a complete proof of the referee's exact tangent calculation. Both quadratic endpoint Hessians have determinant `a^2`. Their fixed-residual sections are a disk and an equal-area ellipse, giving

`delta_j = (2/pi) asin(exp(-j gamma))`.

The equal-density support intersection makes the selected product distance exactly `1-(1-delta_j)^k`. Restoring the common tangent success mass gives raw distance `1-(1-p_j^0(d) delta_j)^n`. These formulae are expressly restricted to the defined tangent laws. The one-factor, product, and physical success normalizations are proved rather than inferred from numerical checks.

**Additional positive-offset result.** Lemma `lem:v7-tangent` proves uniform physical-to-tangent errors `C d` conditionally and `C p_j^0(d) d` per raw preparation in the identical-even contact class. The key input is the retained uniform `C^4` action and `C^2` normalized-twist control, together with simultaneous sign symmetry. The residual-fibre proof accounts for both moving supports and changes in success mass.

Theorem `thm:v7-phase` then proves a joint limit for the **actual nonlinear positive-offset laws**, under `d_j / exp(-j gamma) -> 0`. The distance tends to `1-exp(-2b/pi)` when `k_j exp(-j gamma) -> b`, or when `n_j p_j^0(d_j) exp(-j gamma) -> b` for raw preparations. The proof includes `b=infinity` by projection onto finite-critical subexperiments; it does not incorrectly apply a `k_j d_j` remainder when that remainder need not vanish. Vanishing distance is equivalent to a vanishing scaled sample size in this regime. The corresponding equal-prior simple-testing error is stated with its exact factor one-half.

This supplies the requested first-order moving-support interpretation and a new simultaneous physical conclusion. It neither declares the block-localization rate in the unrestricted general theorem optimal nor replaces the general theorem by an even-contact assumption.

**Locations.** `v7/10_sharp_experiments.tex`, especially `lem:v7-tangent`, `thm:v7-phase`, and the critical raw cost `d_j^-2 exp(2j gamma)`.

### R2(b): A lower bound for the actual count design

**Change.** The new design section states precisely what a query returns: a Bernoulli indicator at bounded flight number, with every history constrained to an actual offset no larger than `Hh`. It includes adaptive choices, parameter-independent randomization, and stopping. It does not claim a lower bound after retaining richer lower-count values or positions.

Lemma `lem:v7-cubic-count` proves the referee's physical obstruction at **finite positive offsets**. A 60-degree spatial rotation acts as a 120-degree rotation of the two shape parameters, forcing the first differential of the normalized count probability to vanish. Uniform third derivatives then give opposite-parameter probability discrepancy `O(d^2 s^3)`. Explicit physical curvature radii give matching distance comparable to `|s|`. The alternatives have the same exact gap; giving that gap to a procedure does not defeat the lower bound.

**Additional confidence-dependent result.** Lemma `lem:v7-stopped-kl` gives a stopped-transcript KL bound `C H^2 h^2 s^6 E_s T`. Theorem `thm:v7-count-lower` combines it with the binary testing requirement

`KL >= (1-2 eta) log((1-eta)/eta)`

to obtain the necessary order `h^-2 epsilon^-6 log(1/eta)`. Corollary `cor:v7-design-optimal` verifies that the retained pilot and second stage obey the required all-history collar and matches the upper bound at each fixed `m`, when `h` is proportional to `epsilon^(3/m)`. Thus both the accuracy exponent `6+6/m` and the confidence logarithm match within the stated Bernoulli design.

No passage `m -> infinity` is made with uncontrolled constants. No global minimax claim over arbitrary count schedules, all recorded counts, or position observations is made. The conclusion is an explicit positive optimal-order result for the design actually implemented in the manuscript.

**Location.** `v7/30_count_design_lower_bound.tex`.

## V6-R3 — Center the contribution on the genuinely uniform nonlinear mechanism

**Change.** The opening argument, result summary, experiment table, and conclusion now put the long-bridge relative law and its operational experiment range first. The proof architecture remains: localized stationary action; relative determinant control; physical residual-time integration; and risk-level experiment comparison.

The new positive-offset theorem makes a use of uniformity that is unavailable from separate fixed-flight Taylor expansions. Its constants must hold on the same contact box as flight number changes. It identifies the success budget at which the nonlinear finite experiment can and cannot be replaced by the boundary model, and translates that budget into raw preparations.

We do not claim that long bridges reveal contact coordinates absent from a one-flight germ. The one-flight identification statement and the flight-uniform finite-jet theorem remain separate positive results. Likewise, the calibrated count estimator uses fixed `J`; it is not advertised as a consequence requiring `j -> infinity`. The introduction and conclusion explain what each component contributes without using a false additional identification claim to motivate long bridges.

The geometric realization, ordered endpoint inverse, constrained and independent-area inverses, marked-response formulas, circular appendices, and complete companion remain in the integrated source. The writing now follows an observation–identification–risk–cost progression, with explicit assumptions and author–year references. No economic application, institutional interpretation, or acceptance claim has been fabricated to imitate a journal style.

**Locations.** `v7/00_introduction.tex`, `v7/10_sharp_experiments.tex`, and `v7/40_conclusion.tex`, together with the retained relative proof chapters.

## V6-R4 — Make the estimator measurable and separate evidence categories

**Change in the mathematics.** Proposition `prop:v7-measurable` supplies an exact Borel minimum-discrepancy fit. A fixed nested dyadic cube rule chooses the first child intersecting the compact minimizer set. Membership is tested by equality of two continuous minimum-residual functions. The selected cube centers are Borel; their limit is a minimizing parameter. The inherited `2 delta` data discrepancy bound is unchanged. This rule applies to all compact inverse fits and fixed fallbacks in the manuscript and does not assume a unique minimizer or claim efficient computation.

**Change in the verification packet.** The proof ledger identifies assumptions, dependencies, and provenance for every new theorem. The standard-library finite suite uses explicit runtime checks, not optimization-removable assertions. It distinguishes exact rational identities, numerical quadrature, finite tangent-limit diagnostics, and a finite tie-breaking illustration. The local pre-push execution contained 136 passing checks; normal and `python -O` output agreed byte-for-byte. The branch build reruns this suite and records its actual result rather than inheriting that local statement as a CI certificate.

The build script checks that no inherited file is missing, all original active mathematical body inputs remain, replaced entry points are archived exactly, every original bibliography key is retained, and the abstract has at most 150 words. It compiles the companion first, then the full manuscript, with shell escape disabled. A generated `verification-v7/BUILD_V7.json` records the actual source commit, output hashes, pages, diagnostic agreement, and reference/box warnings. Until that file exists, no full-build success is asserted. Visual inspection is a separate recorded step, not a feature claimed by this script.

Inherited author tests, the referee's independent diagnostics, the new finite suite, PDF compilation, visual inspection, mathematical proofs, and editorial/priority judgments are explicitly distinct. This response is not an independent journal report and does not self-certify acceptance.

## Handoff

The new revision branch preserves the reviewed source and latest report as its ancestry. The manuscript, point-by-point response, proof ledger, source pins, and reproducibility scripts are delivered for the next independent referee round. The new mathematical conclusions are stated positively with their exact experiment quantifiers; they are not a no-go substitute for the original research program.
