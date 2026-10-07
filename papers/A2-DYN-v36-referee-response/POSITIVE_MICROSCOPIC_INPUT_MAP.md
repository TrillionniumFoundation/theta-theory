# Source geometry and positive microscopic reconstruction

## Frozen source

Author baseline: `c0b184a89ff3d38675d0bc90a9e60b584476e5c3`; ordinary paper tree `06d63ae32efec644d907a0d3d0118c54b8e74c4c`. Controlling report: v31, commit `ea8b02f156b1d99633443103ae5e88eb96a89fce`, blob `068e7f72d813f9ce2a558fb237af624d5cca90af`.

## Inherited inputs actually used

The fixed family, uniform horizon and separation; exact collision and return invariance; the cumulative-return and one-return exponential tails; the geometric cutoff and transverse field of core 63; its source-side all-label second-derivative estimate; the equilibrium suspension and roof-bias identity of core 60; the Fourier convention of core 64. The new argument does not use an unproved induced resolvent, an arbitrary-path multiplier theorem or a microscopic Gaussian denominator.

The coordinate differential was compared with Stenlund--Young--Zhang, *Dispersing billiards with moving scatterers*, arXiv:1210.0011v4, Section 3.1 (PDF page 9). The new text derives it independently from the flight equation, reflection and the changes of variables. The expanded literature paragraph uses only the primary works already in the bibliography: Szász--Varjú, arXiv:math/0309359; Dolgopyat--Nándori, arXiv:1710.08568; and Baladi--Demers--Liverani, arXiv:1506.02836. No new theorem is imported from their abstracts.

## New proof chain

Exact differential and action -> complete first-hit transition guard -> formal source partition and zero extension -> stationary positive extraction -> all-label interpolation -> positive finite-band output density -> original-space microscopic likelihood -> uniform bounded-selector error -> relative posterior estimate with the actual denominator.

The kernel has Fourier support [-1,1], mass 1, zero first signed moment and second moment 12. Its dilation yields a B^-2 density approximation and a B^-1 interval-likelihood estimate. Positivity controls the discarded measure by its mass without multiplying that error by a logarithm or by B. The selected statistic remains inside the full actual Fourier expectation; it is not differentiated.

## Verification boundary

Symbolic and quadrature diagnostics check kernel joins/moments, inverse-Fourier constants, interpolation arithmetic, oscillatory weighted interval formulas, posterior normalization, finite roof-bias models and bandwidth exponents. Negative controls reject sharp-truncation positivity, equality of stationary and section biases, and an L1-to-Linfinity inference. They do not prove the continuum partition, the long-time geometry or the remaining raw local theorem.
