# A2-DYN v10 proof dependencies

## Frozen mathematical baseline

All 24 core files of the reviewed v9 author source (`872f8695670373a3ca67ff84841a1ea38ed64227`) are copied byte for byte and included once. Their chronology is preserved by the v9 review parent. No original theorem, proof, periodic record, edge extraction or raw inversion route is removed.

## New proved chain

| Statement | Inputs | Output |
|---|---|---|
| A.1–A.3: finite centers, slicing, gluing | Uniform one-flight horizon; explicit entry-root algebra; parameterized semialgebraic monotonicity; distributional slicing | Uniform initial-coordinate BV for the actual one-collision functions; explicit boundary treatment |
| A.4: local-space embeddings | Demers–Zhang Sections 3.2–3.3, (3.11)–(3.13), existing local collision identification | Smooth relative-density norm, multiplier/test pairing, and smoothed initial-vector `O(delta^-2)` bound |
| B.1–B.3: chronological products and complex derivatives | Existing smooth collision perturbation on a complex ball of radius `c delta^2`; uniform complementary powers | Explicit initial-vector and projector factors; no `delta^-2q` loss; zero/short-block treatment; uniform complex Cauchy bound |
| B.4–B.5: interpolation and covariance square root | Interval fourth moments; bounded summands; matrix spectral theorem | Adjacent-block and arbitrary-increment estimates with fixed constants; Brownian-law continuity even at singular matrices |
| 21.1: frequency-explicit collision estimate | Existing smoothing, BV correlations, continuous collision covariance, smooth collision spectral expansion; A.4 | Pointwise error with every real rescaled frequency factor retained; complex initial insertions allowed |
| 21.2: stopped integrated error | Exact physical compensation, genuine return-clock window, deterministic maximal estimate | Nine-term integrated four-dimensional error on a finite rescaled ball |
| 21.3 / Theorem B | `0<epsilon<1/134`, `10epsilon<theta<(1/2-7epsilon)/6` | Actual growing-band integral with positive rate; at `(epsilon,theta)=(1/200,1/14)`, rate `n^-3/280 sqrt(log n)` |
| 21.4: exact raw inversion route | **Proved** central band; **assumed** uniform positive definiteness, residual integrability/tail and exact local edge errors | Conditional raw mixed-density LLT, also for the specified initial insertions, without a fixed-neighborhood induced spectral hypothesis |

All complex weights in the new unconditional theorem are initial collision-coordinate functions supported in the section with uniform supremum and BV bounds. Estimates use their absolute values where positivity would otherwise have been needed. The unweighted section probability is `a_R=s_R`.

## Frequency bookkeeping

The collision smoothing bound contributes integrated losses `U^4`, `U^5`, `U^6` or `U^7` because the joint rescaled frequency is four-dimensional. With `U=n^epsilon` and `delta=(1/4)n^-theta`, the slow exponents are

`theta/2 - 5epsilon`, `1/2 - 6theta - 7epsilon`, `1/5 - 5epsilon`.

Their explicit values are `3/280`, `51/1400`, and `7/40`. The remaining terms and the analytic-radius restrictions are checked independently in the proof and by rational arithmetic diagnostics. Fourier rescaling contributes the physical Jacobian `n^-2`.

The proved physical central radius is `n^-99/200`. The former raw inversion tail started at `n^-2/5`; that is a larger radius. Accordingly, the new conditional inversion route explicitly requires control of the intervening annulus. Neither the old tail nor the new major arc is asserted to cover it automatically.

## Retained analytical boundaries

1. The actual covariance is continuous and positive semidefinite. Its L2 coboundary characterization does not give a periodic-evaluable representative. Uniform positive definiteness remains to be proved.
2. The smooth operators used above act on collision spaces. Hard-section induced multipliers, unbounded induced twists, Fredholm control and reconstructed high-frequency phases have not been constructed by this argument.
3. The one-collision BV bound is not a bound on second distributional derivatives of all inverse-coarea densities. The complete critical/singular branch sum and its `n`-dependence remain to be established.
4. The strict intermediate/outer frequency splice still requires actual growth constants; the new central exponent does not supply them.
5. Initial insertion control does not supply terminal, multiple-time or exact-conditioning weighted raw tails. The same-event maximal unfinished-block theorem is preserved, but it does not authorize changing an exact observation event.

Finite diagnostics check algebra and source identity only. Neither this ledger nor a successful build is an independent continuum proof certificate.
