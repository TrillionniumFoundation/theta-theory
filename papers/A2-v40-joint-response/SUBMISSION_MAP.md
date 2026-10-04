# Submission map — A2 v40

## Documents and reading order

The primary and technical companion are independently compiled parts of one submission with the original title and author. The primary contains the complete new argument. The companion preserves the complete reviewed mathematics and the auxiliary interpolation and period-locking proofs cited in the finite construction.

| Read | Source | Content |
|---|---|---|
| Primary Section 1 | `core/00j_two_field_introduction.tex` | Collision convention, exact data, finite priors, patch defect, loss, resources and attribution |
| Primary Section 2 | `core/21_two_field_rigidity.tex` | Finite prefix inverse; support matching and cancellation; exact joint rigidity, fiber, periods, completion; one-orientation example |
| Primary Section 3 | `core/22_two_field_finite.tex` | Two-direction rare query; positive-record hulls; stable chord; finite periodic and complete-cloud geometry |
| Primary Section 4 | `core/23_two_field_law.tex` | Finite moments; probability recovery; all bounded-length predictions; BV density and uniform raw-mean estimates |
| Companion opening and Sections 1–6 | `companion.tex`, retained original core inputs | Reviewed single-law germ, one-resolved extension, finite germ acquisition, known-disk benchmark and comparison |
| Companion appendices | All other retained v39 core inputs | Full global, localized, stationary, calibration, interpolation, precision, period and information arguments |

The PDF names are `A2-v40-primary.pdf` and `A2-v40-companion.pdf`. Place them in the same directory for the external hyperlinks. The primary uses `H-` to import companion labels; the companion uses `M-` for primary labels. Each document has its own bibliography. Shared references do not import duplicate citation labels.

## Main proof dependencies

The exact primary inverse is self-contained apart from standard support-measure and Fourier facts explicitly explained and cited. Its finite prefix formula is proved directly, with its historical source credited in the audit. The finite law and prediction proofs are complete in the primary.

The finite geometric construction cites the following retained auxiliary proofs in the companion. Their arguments remain active, with unchanged proof bodies.

| Primary use | Companion reference | Input actually used |
|---|---|---|
| Coarse occupation components | `lem:coarse` | Fixed grid, clustering, protected complete components and radial brackets; the new primary supplies the correct unknown-law threshold |
| Uniform interior occupation mass | `lem:cap-mass` | Smooth convex cap geometry and lower boundary-mass hypothesis |
| Fixed-accuracy normal acquisition | `lem:rare-coarse-normals` | Radial interpolation and uniform rolling/curvature bounds |
| Fine boundary acquisition | `lem:bisection`, `lem:radial` | Relaxed labels, dyadic radial bisection and `C2` interpolation |
| Stable support smoothing | `sec:stationary` | Fixed signed approximation kernel and finite smooth representation |
| Canonical-frame period margin | `lem:registration-period-margin` | Cancellation of common support addition and translation in the patch defect |
| Period locking and periodic assembly | `core/03_period_recognition.tex` | Positive margin, exact primitive relations, matched basis and area estimates |

The new occupation and rare-label premises replace the observation premises of the cited auxiliary constructions. The primary explicitly supplies their cap-mass thresholds and reserves; it does not assume observations from another preparation model. The retained experiments remain available as separate results under their own hypotheses.

## Response documents

- [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md) maps the report's seven Section 10 requirements to the new proofs and manuscript architecture.
- [PROOF_LEDGER.md](PROOF_LEDGER.md) lists all 16 new complete proof blocks and the exact v39 retention baseline.
- [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md) pins the controlling review, reviewed author source and relevant earlier derivations.
- [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) records primary literature, classical tools and differences between observation models.
- [README.md](README.md) gives the build and exact-SHA qualification commands.

## What the source and artifact bind

The manifest lists both journal documents, each literal input closure, their deduplicated union, hashes of every submitted source file and the workflow, and nine preserved historical trees. The qualifier verifies source bytes against the requested commit, the preservation of 322 baseline labels and 76 proof bodies, mathematical ownership between the PDFs, all finite diagnostics and qualification contracts, and both final TeX logs and recorders. Only the explicitly declared opposite-document entry-file existence probe is separated from the typeset closure; missing inputs and unrelated extra sources remain errors.

The hosted artifact supplies the two PDFs, a journal-source ZIP, a complete pinned-source ZIP, final logs and recorders, the manifest and a receipt bound to the workflow run and exact source SHA. Source capture occurs before environment installation. A failed installation or build retains source and failure evidence and cannot be reported as a successful qualification.

The author branch and referee-copy alias are intended to resolve to the same final source commit. All prior manuscript and review trees are preserved; the new material is confined to this paper directory and `.github/workflows/a2-v40-verify.yml`.
