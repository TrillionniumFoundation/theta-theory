# A2 v36 proof ledger

Baseline: v35 author **70c055e1ff090d58ecd61a5644e0fa62a7766f13**, reviewed at **985d798e172d38c0a9df2a068fe414b2fd13bcbc**.

| Statement | Assumptions/data | Proof mechanism and conclusion |
|---|---|---|
| lem:rare-coarse-normals | Fixed reciprocal queries, support regularity and rolling radius | Radial interpolation and normal Lipschitz control on fixed tubular neighborhoods |
| prop:rare-query | Pooled compass bits; \(2t+D_*<d_0\); boundary-mass lower bound | At most two outward candidates; deterministic exterior zero; interior probability at least \(b_e/4\); inverse-probability finite batch |
| thm:rare-stationary | Calibrated support or two known scales, stationary density, \(\mathcal B_\eta\) | Rare queries, relaxed bisection, support interpolation and retained period locking |
| lem:unk-scale-flux | Complete isolated component and pooled forward mean | Cavalieri strip area plus Fubini gives \(\Phi=t\mathcal W(C)/2\) |
| thm:unk-scale-flux | \((g_1,g_2,F_1)\), unknown ratio bounded away from one | Nesting and linear width normalization; denominator and curvature margins |
| prop:unk-scale-flux-measure | A pooled bit at a uniformly selected finite-grid center | Bounded integral statistic; convex boundary-cell bias without density modulus |
| thm:unk-scale-finite | Two homothetic settings, unknown ratio/footprint, fixed common origin and priors | Rare boundary recovery plus \(O(\nu^{-2})\) scalar measurement; all centers and digital descriptions charged |
| thm:unk-scale-exact | \((g_1,g_2)\) alone; weaker separation | Occupation mass is obstacle area; unique physical mixed-area root |
| prop:unk-scale-stability | Matched supports and area errors with uniform convexity | Hausdorff stability of area/mixed area, discriminant margin, support perturbation |
| prop:unk-scale-mass | Coarse dyadic domain and reciprocal bits | Finite rational killed adjoint; \(M=-\int w g\); geometric quadrature and bounded sampling |
| Retained thm:stationary-lower | Known common disk, fixed laboratory gauge, bounded short commands, expected stopping | Original physical packing, mean contraction, binary range and stopped chain rule |

## Preservation

All 33 original proof bodies and all 117 labels remain active. Ten formal statements with ten proofs are added. The original localized upper/lower results, digital theorem, period chain, expected-stopping converse, bounded-error calibration converse, fixed-footprint inverse and known-scale footprint theorem remain active. Earlier sufficient bounds are not represented as sharp stationary rates.

## Finite checks and their scope

tools/verify_v36.py exercises compass-candidate geometry, segment/disk collision decisions, support/calibration algebra including translations, direct flux and independent area normalization, a finite killed-chain adjoint, binary-information inequalities and exponent accounting. The actual script emits its sections and check counts. tools/test_contract_v36.py exercises validation rejection cases; tools/validate_v36.py binds sources and, in exact mode, a clean commit.

The continuum arguments remain the proofs in the manuscript. Finite checks do not establish general continuum correctness, physical controllability or journal acceptance.

## Explicit distinctions

For \(\gamma=0\), the remaining stationary exponent gap is \(s/(2(s-2))\). The ratio is learned; exact homothety and the common origin are supplied. Unknown unscaled offsets give the stated translation gauge. Uniform finite period decisions use the positive patch margin. Digital command descriptions are distinct from physical calibration, travel and arithmetic time.
