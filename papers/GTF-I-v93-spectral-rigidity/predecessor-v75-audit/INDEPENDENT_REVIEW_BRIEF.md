# Independent rereview brief — Revision 75

This file prepares a concrete specialist review of the new manuscript. No reviewer has been contacted or commissioned. Independent priority review requested in r48 remains externally pending. The preceding brief is preserved in `predecessor-v74-audit/INDEPENDENT_REVIEW_BRIEF.md`.

## Manuscript objects and comparison baseline

Review `quantitative.tex` as the focused quantitative article and `structural.tex` as the separate structural article. The complete research edition preserves the derivation history and is an archival research object. Structural mathematics remains inherited and should receive its own assessment.

The controlling report is the v74 external referee report r48, which found no fatal correctness defect in the unbiased-ball theorem package but requested a direct comparison with Fiurášek–Mičuda (2009), independent priority review and a stronger mathematical response to the restricted target class. The v75 quantitative extension addresses the complete ordered binary-qubit effect body

```text
E = ((1+b) I + x·sigma)/2,       |b| + |x| <= 1,
```

including biased effects. The supplied target is the effect itself. Redundant axes at scalar effects are not separate target points.

Section 51 (`thm:biasedmetric75`) gives a global finite-use metric comparison. Section 52 (`thm:biasedcover75`) gives covering order `N² log(N+2) delta^(-4)` for all `N>=1` and `0<delta<=delta_0`, with absolute `delta_0>0`. Its rational realization is `thm:biasedcodec75`. The logarithm is attributed to the projective corner where both eigenvalue support deficits become small.

## New proof questions

1. **Spectral endpoints.** Check the finite-horizon Bernoulli comparison uniformly on the closed probability interval, including support changes at zero and one. Distinguish a controlled two-row oracle from the maximum of two homogeneous product experiments; adaptivity may affect the exact commuting value even when these quantities are comparable.

2. **Angular comparison.** Check the operational upper and lower moduli for two eigenbases with the same arbitrary spectrum, including asymmetric noise. In particular, the unbiased spin-flip state-discrimination reduction does not apply automatically when the bias is nonzero.

3. **No cancellation.** Check that changing both eigenvalues and the axis cannot conceal either component at the scale used by `thm:biasedmetric75`. The proof must use legal tests and common hypothesis-independent processing; no one input should be asserted to attain two unrelated endpoint extrema simultaneously.

4. **Identifiable body and local balls.** Check uniform localization where the spectrum becomes scalar, where one effect eigenvalue reaches its support boundary, and near the projective corner. Any angular multiplicity must disappear when the effect becomes scalar.

5. **Covering consequence.** Check the small-error covering law and its logarithmic horizon factor by the rational lattice count and separated projective-corner boxes. In the upper count, the cutoff `U=B²/N` gives `B/sqrt(U)=sqrt(N)`, preventing an extraneous logarithm in the requested accuracy. In the lower count, distinct depth boxes require uniform spectral separation. Preserve arbitrary legal centres in the lower bound. The global pair-metric comparison and the local covering theorem have different quantifiers.

6. **Constructive realization.** Check exact rational legality, the treatment of irrational norms arising from rational Cartesian targets, canonical encoding and replay, and one-index charging of all target data. Finite exact code enumeration does not establish a polynomial-time algorithm in the binary numerical input lengths.

## Inherited dependencies

Recheck the points where the extension uses the v73 angular block proof and finite majority bound, the v74 support-cutoff and noncancellation arguments, and the small-ball weighted-covering method. The v74 Ahlfors criterion retains its compactness, regularity and identifiable-image hypotheses. Its contact trichotomy and disk logarithm remain distinct statements from the full biased-body covering calculation.

## Primary-source priority questions

Compare the new statements against the four primary papers detailed in `LITERATURE_AUDIT.md`:

- Fiurášek–Mičuda (2009), Sections I, III and IV: two-use projective-qubit strategies under the restriction excluding additional ancillary measurements.
- Sedlák–Ziman (2014), Theorem 1 and Section VI, Example 4, equation (37): general binary perfect single-use discrimination and unequal-visibility unbiased state reduction.
- Puchała–Pawela–Krawiec–Kukulski (2018), Theorem 1, equation (19): single-use projective diamond distance.
- Puchała–Pawela–Krawiec–Kukulski–Oszmaniec (2021), Corollary 1 and Theorem 2: exact projective N-use distance and parallel optimality with ancillary access.

The main comparison should test whether the biased spectral/angular metric or its finite-use covering consequence is equivalent to an established result under another parametrization. Identification of programme, discrimination and entropy ingredients is not itself priority clearance. The two-use restricted-strategy improvements and the ancillary-assisted projective parallel-optimality theorem should be read with their distinct admissible tests.

## Scope and evidence

All outcomes remain ordered and trace distance is unhalved. The encoder receives exact target data. Pair-dependent separating tests prove packing separation and do not by themselves identify every codeword with one common measurement. The full biased-body result does not assert a classification of arbitrary multi-outcome measurements, quantum-output instruments or growing-dimensional channel bodies. The inherited common-estimator theorems retain their own families and ranges.

The work branch is `revision/general-theta-foundations-i-v75-full-measurement-body-2026-10-04`. Review the referee-ready alias only at the final recorded publication head. Reproduction receipts, source hashes and CI bind the actual source and PDF artifacts; they do not certify mathematical correctness, novelty, journal suitability or human authorship. The response and provenance files identify the exact completed checks.
