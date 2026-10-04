# Internal mathematical and source audit — A2 v41

## Status and scope

This is an **AI-assisted internal audit**, produced during the author revision. It is separate from the controlling v40 referee report and is not a human specialist report, journal decision, physical-apparatus test or formal proof certificate.

The controlling report and all of its accompanying source, literature and verification material were read at review commit `24baf07cf2952668d61881c727cc6417e952c76e`. The old v40 exact, finite geometry and finite law proofs were read together with the actual supplement proofs they use. New arguments were prepared in separate tasks and reviewed in the integrated source. A second independent internal pass checked the exact support/curvature expansions and the supplement interface without relying on finite diagnostics.

## Mathematical audit

| Area | Direct checks and resulting source |
| --- | --- |
| Positive measure supports | Both support inclusions; positivity in every neighborhood; Tonelli passage from physical strips to a.e. convolution densities; no density assumption on the launch law. See `core/24_measure_support.tex`. |
| Connected components and periods | Continuity of extreme section endpoints by compactness/strict convexity; exact `0<s<=t` convention; local finiteness; gaps and incidence matching; finite null-set translation union; support cancellation for periods. Same file. |
| Nonsmooth curvature | Closed-hemisphere maxima; semiconvex support function; distributional positivity; one-sided support-face derivative formulas; atom mass equals exposed length; corners and singular continuous curvature; chord orientation and Jordan decomposition. See `core/25_nonsmooth_curvature.tex`. |
| Finite geometry | Tangential collar and candidate conjunction; conditional fresh draws; grazing Jacobian and injectivity; footprint cap rectangle; boundary-cell grid error uniform in displacement; distance enclosures and fragment cutoff; exact signed-plateau determinant. See `core/26_finite_geometry_details.tex`. |
| Finite law | Fixed coordinate reserve; positive physical area normalization; genuine rational polygon factor and exact moments; atomic-law quadrature; padded grid; irrational comparison law versus rational optimizer; factorial bound; compression preserving the moment constraints; complete confidence and cost allocation. See `core/27_moment_factor_details.tex`. |
| Supplement interface | Checked against actual proofs for cap mass, complete coarse hulls, projection normals, relaxed bisection, radial/support regularity, signed smoothing, period lattice relations and translation-invariant defect. See `core/29_supplement_interface.tex`. |
| Literature | Direct cross-covariogram factorization, unknown-noise hypotheses and overlapping submodel, precise signed-difference role, compact Fourier uniqueness and finite conditioning. See `LITERATURE_AUDIT.md`. |

No mathematical repair requiring a weaker theorem class, altered command alphabet or changed sufficient rate was identified in these audited chains. Two precision corrections were made during integration: the exterior sure-zero assertion refers to the actual rounded target, and exact period decisions refer to candidates' matched true differences, not exact real coordinates of their estimates. The rational-factor implementation also removes the need to regard independently approximated moments as a consistent probability factor.

## Finite diagnostics

`tools/verify_v41.py` retains the full inherited finite diagnostic programme and adds targeted exact or finite-model checks for cornered strictly convex lenses, oblique contact chords, singular segment probabilities with endpoint atoms, signed moment matrices, rational polygon factors, padding and positive weight compression. The ordinary and optimized Python executions must have identical JSON output.

These checks exercise algebra, boundary conventions and explicit models. They do not approximate a proof of the continuum support decomposition, infinite obstacle configurations, arbitrary singular continuous measures, uniform statistical acquisition or literature priority. The continuum arguments are written in the mathematical source.

## Source preservation and document qualification

The preservation baseline is the active union of both v40 journal documents, read at their frozen Git source. Before the final qualification, direct comparison found:

- all 402 reviewed labels retained;
- all 92 reviewed proof bodies byte-identical;
- 46 current TeX inputs, 456 labels, 113 formal blocks and 110 complete proofs;
- primary closure of 13 inputs and supplement closure of 35, sharing only the label-free preamble and bibliography;
- eleven historical directory-tree pins.

The workflow runs ordinary and optimized mathematical diagnostics and contract checks. It compiles both documents until their auxiliary states stabilize, checks the recorded input closure against actual TeX openings, rejects undefined references and final TeX findings, archives the sources, and binds PDFs and logs to the exact author commit. Failure paths retain evidence and cannot claim successful qualification. The final receipt supplies the actual execution result and hashes.

## Further review

The referee's requested human specialist review has not been represented as completed. `SPECIALIST_REVIEW_BRIEF.md` prepares a concrete review of the five named areas against the frozen author source. A completed human report, if obtained later, should identify its reviewer, scope and commit independently of this internal document.
