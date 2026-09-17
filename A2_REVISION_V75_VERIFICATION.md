# A2 v75: post-publication verification

Date: September 17, 2026. This record concerns the delivered files, not a journal decision or a formal certificate of the theorems.

## Pinned objects

- Report answered: `1ad828fd3cec7d39881fa4bb31d14423c4fd35da` (v74).
- Frozen compiled source: `89d5a3aa3e9f00a806d48f19f6f6831770184d76`.
- Manuscript tree: `8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d`.
- Native products commit: `be689158f64e1b44e2b7a03ac4ea4cf9ae4058f5`.
- Source branch: `revision/a2-v75-mechanism-first-2026-09-17`.
- Native branch: `revision/a2-v75-native-products-35187395322-1`.
- GitHub Actions run: `35187395322`; native job `105092296064`, completed successfully.
- Retrieved artifact: `10482862451`, `a2-v75-native-35187395322-1`.
- Artifact ZIP SHA-256: `e51cc502c53d82018f5160715d7e0f75f9b872d79d6b7125585a2be41ee31cdf`.

This root-only verification record is committed after the compiled source. It does not change the manuscript subtree or the source identity of the PDFs.

## Native products

| Entry | Pages | SHA-256 |
|---|---:|---|
| `rigidity.pdf` | 48 | `785ae45ea372d521d9792a4c9e669ee14e4bae0bc99f011c8eac08813c49f7e5` |
| `main.pdf` | 369 | `89e5bb53ad11821f67f3381c68b12666a2a16d79ce0b2cdf032fc8fe2dc91d49` |
| `two_collision.pdf` | 7 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |

The principal and full entries overlap; their page counts are not independent mathematical output. The v74 principal/full/companion entries were 190/365/7 pages. The present 48-page principal article includes the complete central smooth proof and observation consequences; the full technical manuscript retains the wider programme.

## Checks actually performed

The native workflow materialized the authored revision against the pinned 992-file baseline and checked the resulting Git tree before building. All 992 original paths remain. The seven edited originals have byte-exact archived copies. All 1,423 old active mathematical labels remain reachable; the revised union contains 1,435. The two core slices are exact prefixes of their unchanged original technical modules.

The workflow compiled all three entries from the frozen Git source, checked generated auxiliary provenance, and ran six diagnostic groups in both normal Python and optimized Python: `check_adaptive`, `check_revision_v32`, `check_revision_v38`, `check_inherited_v73_on_baseline`, `check_revision_v74`, and `check_revision_v75`. Normal and optimized JSON outputs agree. The restored historical checks are not relabeled as checks of newly authored proofs.

After retrieving the artifact through the GitHub connector, a separate local verification checked the artifact digest, all 51 evidence-file hashes recorded by the build report, all 1,017 source-file bytes and ZIP modes, and equality with the locally authored candidate. A bottom-up reconstruction of Git blob/tree objects reproduced manuscript tree `8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d`. No standalone font files occur in the source archive. Page counts and the three PDF hashes match the published provenance. The final logs contain no overfull boxes, LaTeX errors, missing-character diagnostics, undefined references/citations, or multiply-defined-label warnings.

The publisher separately fetched the native branch and verified all 53 retained evidence objects as committed Git blobs. `deliveries/a2-v75/89d5a3aa3e9f00a806d48f19f6f6831770184d76/COMMITTED_OBJECTS_VERIFIED.json` identifies the product commit it verified. It is not a self-referential hash assertion.

## Visual inspection: exact coverage

All 48 principal pages were inspected in rendered contact sheets. Principal pages 1, 2, 3 and 39 were also inspected at larger resolution, covering the title/roadmap, principal theorem, mechanism explanation and new conditioning calculation. The retained full-manuscript material was sampled at pages 1, 364, 368 and 369; page 364 was inspected at larger resolution. Companion pages 1 and 7 were sampled.

After artifact retrieval, raster outputs at scale 0.6 were compared page by page with these inspected local outputs: all 48 principal pages, those four full-manuscript pages and the two companion pages were pixel-identical. No clipping or overlap was observed in that visual coverage. This is not a claim that every one of the 369 technical pages received a fresh full-resolution visual inspection or a new independent proof audit.

## Mathematical review boundary

The new main theorem, its physical-relative and actual smooth-envelope dependencies, the positive-curvature/finite-jet interfaces, the observation refinements, and their hypotheses were checked against the v74 report and retained derivations. The response distinguishes the physical and functional arguments from classical quotient/matrix/concentration tools. The entire analytic/global/lattice/coarsening catalogue remains in the full entry; preservation, native compilation and finite symbolic tests are not substituted for an independent theorem-by-theorem assessment of that catalogue. The significance judgment remains a question for the next referee.

Start with `A2_REVISION_V75_REVIEW_READY.md` and the pinned `RESPONSE_TO_REFEREE_V75.md`.
