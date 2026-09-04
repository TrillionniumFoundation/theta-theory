# Historical derivations used in Round 45

The controlling source was the actual Round 43 v2 article at
`1a96a07f12c69ec4390d9848e05e29ffc808f479`, inherited by the Round 44 report
commit `9417c8d9ed14f8a8c4ba538435bf29837630b0ae`.

- The homogeneous response jets, six-duration embedding, finite-prefix sign
  design and random-information Gaussian likelihood were checked against
  `round43/lattice.tex` and `round43/triangular.tex`. Their theorem content is
  retained, with explicit prior and common-bound conventions.
- The fixed separable dual spaces, concentrated push-forward argument, memory
  transform and finite preparation mixture are retained from
  `round43/filter_memory.tex` and `round43/preparations.tex`.
- The Weyl reconstruction and full-support compact posterior LDP are retained
  from `round43/infinite_jacobi.tex`, with the washout derivative repair.
- `round43/effective_inversion_details.tex` supplied the exact moment recursion
  and finite Gram systems. The former exponent estimates were not reused:
  the new coefficient-norm argument and finite-map ledger replace them.
- `round43/linear_time_protocol.tex` supplied the predictable-intercept sign
  decomposition. Its uniform-probability outline is replaced by a complete
  common-metric finite-n argument and adaptive Laplace tracking.
- The Round 40 and Round 42 reports document the delayed-calibration,
  uncountable-net and missing-source failures. None is treated as closed by a
  historical verification JSON. Current sources are independently hashed and
  built. The current Gaussian shrinking-net lemma also avoids the older
  overly broad integrable-but-not-identically-distributed noise formulation.

New work is concentrated in `inverse_stability.tex`,
`uniform_statistics.tex`, and `growing_depth_uncertainty.tex`.
