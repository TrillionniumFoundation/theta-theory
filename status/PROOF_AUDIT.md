# Hostile proof audit - deterministic path-ensemble v6

## Audit conclusion

Within platform `FB4-PE-v1`, every load-bearing arrow in

\[
\text{deterministic map}
\to \text{natural law}
\to \text{path LDP}
\to \theta
\to \text{driven law}
\to \text{physical diffusion}
\to \text{free-energy DPP}
\to \theta\text{-HJB}
\]

has a named producer. No theorem imports the old specified Markov matrix,
microscopic Brownian noise, or an independently selected risk parameter.

## Theorem interfaces

| UID | Producer | Output | Principal risk checked |
|---|---|---|---|
| NAT-LAW | Paper I, Prop. 1.1 | Lebesgue Bernoulli branch law | Probability is a natural invariant volume, not a selected kernel |
| PATH-LDP | Paper I, Thm. 2.1 | Explicit `I(a)` and `theta=I'(a)` | Strict convexity and parameter inversion |
| MICRO-EQUIV | Paper I, Thm. 3.1 | Quantitative local ensemble equivalence | Conditioning is not replaced by an unsupported tilt |
| DRIVEN-MAP | Paper I, Thm. 4.1 | Exact deterministic realization of canonical tilt | Driven law stays in one moving-seam family |
| EXCESS-PRESSURE | Paper I, Thm. 5.1 | Dynamic theta-expectation | Log-sum-exp is a partition-function ratio, not a utility axiom |
| RESPONSE | Paper I, Thm. 6.1 | Graded resolvent response | Centered norm really contracts |
| PHYS-CHAR | Paper II, Prop. 1.1 | `C(a)`, `bar tau(a)` | Impulses centered even conditional on roof class |
| DET-ROUGH | Paper II, Thm. 2.1 | Brownian rough limit | No microscopic noise |
| PHYS-CLOCK | Paper II, Thm. 3.2 | Physical-time covariance | Correct renewal normalization |
| EXP-WINDOW | Paper II, Thm. 6.1 | Exponential random-horizon bound | Random index is not assumed to be an independent stopping time |
| MICRO-FE-DPP | Paper III, Thm. 2.1 | Exact microscopic nonlinear recursion | Derived from excess pressure |
| THETA-CONSISTENCY | Paper III, Thm. 3.1 | Endogenous gradient-square term | Same `theta=I'(a)` and same covariance |
| ENTROPIC-CLOCK | Paper III, Thm. 5.2 | Physical-horizon value replacement | Uses tilted-measure Orlicz comparison |
| THETA-HJB | Paper III, Thm. 6.1 | Physical theta-semigroup | Cole-Hopf comparison in fixed-law core |
| SADDLE-ENV | Paper IV, Thm. 4.1 | Covariance plus optimizer correction | Controlled branch is not confused with fixed law |
| AXIOM-RIGID | Paper V, Thm. 1.1 | Linear-or-exponential certainty equivalent | `theta` family uniqueness |
| TANGENT | Paper V, Thm. 3.1 | Tangent probabilities and covariance | Restricted to fixed law/fixed policy |
| CONTROLLED-TANGENT | Paper IV/V | Optimizer-response correction | Former Paper III-to-V type gap closed |

## Resolved historical blockers

```yaml
arbitrary_probability_kernel:
  resolution: natural Lebesgue physical measure of the deterministic map

arbitrary_theta:
  resolution: theta = I'(a) from the prepared mechanical current

exponential_utility_inserted_by_definition:
  resolution: canonical excess-pressure identity

microcanonical_to_canonical_jump:
  resolution: quantitative finite-window conditioning theorem

canonical_law_not_deterministically_realized:
  resolution: exact driven moving-seam map

Brownian_noise_at_microlevel:
  resolution: deterministic iid branch coding and martingale limit

physical_clock_only_in_expectation:
  resolution: renewal time change plus exponential random-window theorem

additive_to_entropic_random_horizon_jump:
  resolution: tilted entropic Orlicz comparison

controlled_theta_game_equals_fixed_law_entropic_semigroup:
  resolution: explicit separation and saddle-envelope correction

cash_additive_time_consistent_family_leaves_theta_free:
  resolution: axiomatic exponential rigidity plus mechanical theta selection
```

## Scope boundaries, not internal gaps

1. The macro current `a` is a preparation condition. Bare deterministic
   equations cannot choose which atypical macrostate an experiment realizes.
2. The collision-port impulses and roof are part of the mechanical model.
3. The exact reset/Bernoulli property is special to the full-cover map.
4. A periodic finite-horizon specular Sinai version requires a separate
   natural-measure path-LDP and is not silently claimed.
5. External specialist review remains pending.
