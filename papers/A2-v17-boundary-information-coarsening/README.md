# A2 v19 — signed endpoint rigidity and unknown-geometry boundary information

**Boundary laws, signed contact rigidity, and nonregular information in dispersing billiards**  
Qian Qi · English manuscript · September 11, 2026

Revision branch: `revision/a2-v19-signed-endpoint-rigidity-2026-09-11`  
Review base: `review/a2-v18-independent-harsh-top4-2026-09-11`

[Article entry point](main.tex) · [Active source manifest](ACTIVE_SOURCE_MANIFEST_V19.md) · [Response to the v18 referee](RESPONSE_TO_REFEREE_V19.md) · [Proof ledger](PROOF_LEDGER_V19.md) · [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V19.md) · [Literature audit](LITERATURE_VERIFICATION_V19.md)

## What v19 changes

The v18 referee found no fatal error in the boundary-information/endpoint-critical core but identified two remaining conceptual blockers: local geometric rigidity was still restricted to individually even contacts with supplied leading geometry, and the sharp endpoint experiment was still a fixed-table finite-versus-boundary comparison rather than an unknown-geometry local experiment.

v19 addresses both directly.

**General signed-endpoint rigidity.** Retaining signed endpoint positions exposes the support `S_b(u)+S_b(v)<d`. Its threshold recovers each unsymmetrized half-line action `S_b`. The physical onset gives the gap, the quadratic action terms recover both contact curvatures, and at every order `n>=3` the new labelled graph jets enter through

```
[[coth(n gamma), frak_r_0^n csch(n gamma)],
 [frak_r_1^n csch(n gamma), coth(n gamma)]]
```

whose determinant is exactly one. Thus all finite labelled contact jets, including odd jets, are recursively recovered without reflection symmetry, equality of contacts or supplied curvatures. Analytic endpoint-law germs determine the two participating analytic contact germs.

**Unknown-geometry boundary LAN.** For a vector moving-support model `f_theta=a_theta(w_theta)_+`, v19 proves LAN with intrinsic matrix

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`.

The theorem includes the efficient local score estimator and the sharp quadratic local minimax value. In a finite-dimensional billiard contact-jet family, the support velocity is the derivative of `d-S_0-S_p`; signed-endpoint rigidity forces the collection of boundary information matrices to have trivial common kernel. A finite set of positive endpoint windows therefore has a positive-definite summed information matrix, and the relative law transfers the experiment to actual long finite bridges with failed raw preparations charged.

The fixed-table three-level observation hierarchy from v18 remains active and separate: complete records, endpoint-only records and success bits have different finite-versus-boundary critical scales.

## Referee mechanical items

The channel lattice-translation variable is now `ell`, leaving `lambda=varrho^2` exclusively for the return multiplier. The formal relative theorem explicitly states that geometric derivatives are taken in centered coordinates `t=j g_e(xi)+d`, holding `d` fixed. The active entry point has been simplified by collecting the retained auxiliary modules behind `article/99_auxiliary_compendium_v19.tex`; no earlier mathematical module is deleted.

## Source/provenance convention

The containing directory keeps its historical v17 filesystem name so the large reviewed source graph is not duplicated. The authoritative v19 source identity is the revision branch plus `ACTIVE_SOURCE_MANIFEST_V19.md`. Older `PROOF_LEDGER.md`, `VERIFICATION.json`, `SOURCE_PINS.json` and v18 audit files remain historical records, not current-status metadata.

## Reproduction and build scope

From a complete checkout, the repository build driver remains the required native route:

```sh
python3 tools/build_submission.py --output-dir /absolute/path/outside/this/directory
python3 tools/check_boundary_information.py
python3 -O tools/check_boundary_information.py
```

A successful workflow file or finite diagnostic is not treated as proof certification. `VERIFICATION_V19.json` records only checks actually executed for this revision; remote CI/build status is reported separately from mathematical review.

## Preservation

The revision begins from the latest v18 review branch. Earlier A2 revisions, all referee reports, all retained mathematical sources and the original companion manuscript remain in Git history and are not silently replaced. This branch is offered for renewed independent review; no journal acceptance or formal proof certification is asserted.
