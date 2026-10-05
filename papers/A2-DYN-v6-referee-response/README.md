# A2-DYN — revision 6

**Qian Qi, Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Revision date: 5 October 2026. Main source: `main.tex`. Native build: 44 pages.

This is a new mathematical revision of the A2-DYN paper, responding to the external report at `a81eb226c013ca062a6901bb472a90668de29eec`. The reviewed mathematical source was `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`; its v5-named remote branch was an exact alias of v4. Revision 6 is not that alias. Its mathematical checkpoint is `65551575d46469c3b47c7bf53ff63d787be02085`, and its core tree is `4a5568bd65a67bf1fcdebf33bba37d5cea83fb18`.

The model, raw mixed-density LLT objective, genuine return records, physical clock, geometric comparison and positive-denominator interfaces are retained. All 37 reviewed proof bodies and all 107 reviewed labels remain active and byte-preserved. Eight further proofs are recovered from the explicitly identified unpublished v5 source. Thirteen proofs are new in v6. The complete article has 58 proof bodies and 173 labels; these counts describe the source, not a mathematical certification.

## Principal additions

Theorems 14.3 and 17.2 prove uniform exponential moments of the genuine return block and a logarithmic bound on all unfinished blocks over a growing stationary interval, including conditioning on events with polynomially small positive probability. Corollary 17.3 gives an explicit square-root path-comparison error. The collision spectral input is stated separately and checked against the actual radius family.

Theorem 7.1 strengthens the physical phase coercivity by thickening a single one-step defect; Theorem 7.2 states a precise phase-reconstruction/Fredholm criterion for an induced resolvent. Lemma 15.1 and Proposition 15.2 expand the moving-domain coarea argument with common charts and an initial-state remainder. Section 18 distinguishes finite-lag covariance continuity and finite-band truncation from the infinite covariance and all-branch derivative sums.

The full uniform raw mixed-density LLT is not claimed unconditionally: the actual induced phase reconstruction, the infinite covariance/cohomology criterion and global raw residual estimates still need verification. No theorem is replaced by a smoothed observation model, independent flights, or a different topic.

## Reading and reproduction

Read `RESPONSE_TO_REFEREE.md` for the seven numbered requests, `PROOF_LEDGER.md` for theorem-level dependencies and `SOURCE_AUDIT.md` for provenance and source preservation. The final section of the main article contains the mathematical realization boundary rather than development or publication logs.

From a clean checkout, with Python 3.10 or later, mpmath 1.3.0, pdfLaTeX, AMS packages, Latin Modern, microtype, geometry and hyperref installed, run:

```sh
bash papers/A2-DYN-v6-referee-response/build.sh
```

The build checks exact inherited blobs, the active input graph and references, executes the retained and new finite diagnostics in normal and optimized Python modes, compiles until references stabilize, rejects TeX warnings and over/underfull boxes, and checks the actual TeX recorder input set. It writes `build/main.pdf` and `evidence/build-receipt.json`. The receipt distinguishes a local source build from an exact, clean GitHub event checkout.

The dedicated workflow `.github/workflows/a2-dyn-v6-qualification.yml` builds the exact event SHA and archives the PDF, log and evidence. An installed workflow is not evidence that a run has passed; consult the run attached to the actual final SHA. No main branch, old manuscript, prior report or unrelated paper is changed by this revision. Independent human specialist review remains to be obtained.
