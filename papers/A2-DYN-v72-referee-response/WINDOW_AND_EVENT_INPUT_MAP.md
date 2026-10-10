# Inputs for unsmoothed windows and physical-event comparison

## Analytic construction

The interval majorant/minorant is the classical Beurling--Selberg construction. Primary contextual source: E. Carneiro and J. D. Vaaler, *Some extremal functions in Fourier analysis, II*, arXiv:0809.4050, Introduction, pp. 1–2. That introduction records interval one-sided approximants and compact Fourier support. The new article proves the required version directly from the sinc-squared partition and integral comparisons, including closed/open endpoints, the angular-frequency factor `2*pi`, the exact mass errors, and the tensor minorant. No optimality theorem is required.

Only the source's introduction is used for provenance; no result for Gaussians, powers, logarithms or higher-dimensional extremizers is imported. The PDF text was checked online. The web screenshot endpoint failed; no claim of visual inspection of that external PDF is made.

## Inherited manuscript inputs

- `thm:adaptive-cross-fixed-count`: full prescribed-count integrated characteristic error on the retained union, with separated supremum and BV costs.
- `thm:joint-uniform-nondegeneracy`: parameter-uniform Gaussian upper, derivative and lower bounds on central windows.
- `prop:exact-raw-cutoff-transport`: almost-everywhere identity `R_chi=p^L-K_chi*mu^L`.
- The third-count kernel separation for the three retained cutoffs: high-count convolution is negligible on the same central boxes.
- `eq:all-stopped-moment-bound`: every fixed moment of the actual centered return record; the projection uses order 64, and coupling uses a fixed moment selected for each tail power.
- Kac mean, invariance of the actual return map, positive lower flight length, and the actual exponential one-return tail.

## Important non-imports

No restriction of a four-dimensional L1 Fourier error to a three-dimensional plane. No independent-return model. No stationary-suspension law silently substituted for the section-start law. No positivity attributed to complex weights. No product of signed lower envelopes. No singleton lattice denominator inferred from a growing-width window. No absolute or L-infinity correction norm inferred from a signed average. No density-derivative budget inferred from collision moments.
