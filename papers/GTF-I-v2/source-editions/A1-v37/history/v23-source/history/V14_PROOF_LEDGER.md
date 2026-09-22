# Proof ledger for A1 revision 14

Stable labels, not page numbers, are the primary locators. Current numbering
below refers to the local 72-page build. All paths are relative to this folder.

## Principal chain

| Mathematical obligation | Source and label | Current locator |
|---|---|---|
| Physical experiment, fixed commands and query realization | `core/02_experiments.tex`, `prop:tests` | Section 2 |
| Separated past tangent exponents and normalized rank | `core/03_transversality.tex` | Section 3 |
| Complete Hermite flag and thin-rectangle global cover | `sections/classical.tex`; generated complete lemmas from `core/05_confluence.tex` and `core/06a_attainable_filtration.tex` | Section 4 |
| Zero-safe Newton coordinates/exterior-volume comparison | `core/06b_collision_geometry.tex`, `lem:leja-scales` | Lemma 5.1 |
| Uniform attainable subprobability cube | same, `lem:newton-attainment` | Lemma 5.2, p.14 |
| Global checkpoint and causal classifications | same, `thm:intrinsic-checkpoint`, `thm:intrinsic-streaming` | Theorems 5.3--5.4, pp.15--16 |
| Uniform full-flag covariance and bounded simultaneous dual | `sections/directional_geometry.tex`, `lem:flag-covariance` | Lemma 6.1, p.20 |
| Relative-prior body inclusions and all linear widths | same, `prop:ambiguity-ellipsoid` | Proposition 6.2, pp.20--21 |
| Exact prefix, charged physical event, separation example | same, `cor:prefix-ambiguity` | Corollary 6.3, pp.21--22 |
| Common-name sharp regret under original joint uncertainty hypotheses | `sections/uncertainty_geometry.tex`, `thm:sharp-common-moments` | Theorem 7.1, p.23 |
| Complete finite implementation and separate resource bounds | `sections/effective.tex`; preserved theorem from `history/V13_introduction.tex`, `thm:effective-main` | Appendix H, Theorem H.9 p.56 |
| Radius certificates, construction stability, independently bound request | `sections/certified_resources.tex`, `sections/construction_stability.tex`, `sections/request_conformance.tex` | Appendices I--K |

## New proof obligations and their resolution

1. Complete normalized flags remain independent even when physical directions
   disappear: add the constant and use complete Hermite blocks, not isolated
   derivative orders. Compactness is applied to each of finitely many node
   orders. Posterior lower domination transfers covariance bounds.
2. All directions must be realized in one declared prior class: a uniformly
   bounded dual realizes every vector in a common cube. Its posterior tilt is
   pulled back to a normalized prior by `(1+s f)/(1+s mu(f))`; positivity,
   total mass and the relative-envelope bound are proved explicitly.
3. Widths must be physical, including at zero pivots: multiply by `L D`, use
   the uniformly invertible active triangular block, and set post-rank widths
   to zero. No inversion of a zero physical coordinate occurs.
4. Exact-prefix information must not be confused with noisy advice: triangular
   equivalence is stated only as an exact identity. The known-calibration local
   class and the separate common-name class are defined separately.
5. A conditional geometry must not silently change priors after observation:
   the set statement fixes one history. The decision realization uses a
   constant-likelihood event, the same prior advice before acquisition and
   its actual event probability, with an explicitly event-weighted payoff.

## Preservation boundary

`V13_PRESERVATION_MANIFEST.json` pins 74 entire proof blocks, 77 entire named
statements and the original source manifest. `build.py` fails if any of these
is missing or changed in the expanded manuscript. The v9 pinned core blobs
and v10/v11/v12 preservation checks remain active, including the already
documented v11 correction. `PRESERVATION_REPORT.json` distinguishes source
retention from proof verification. No complete v13 mathematical statement or
proof was replaced; the new section contributes exactly three of each.

All current compiler modules and tests v10--v13 are unchanged. The new
`tests/test_v14.py` is independent of those test helpers but is author-written;
its result is finite algebraic evidence, not independent refereeing.
