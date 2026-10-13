# A2-DYN revision 76

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas** — Qian Qi.

The journal article is `main.tex`. Its complete mathematical supplement is `supplement.tex`. Build both in an exact checkout with `bash build.sh`. Outputs: `build/main.pdf`, `build/supplement.pdf`. The explicitly restricted local command `bash build.sh --journal-only` checks only the new journal material and is forbidden in CI.

This revision responds to the v75 report at `3a69da183d94b3bc695717d66971968e5396e624`, report blob `01355269b3c3984bb51dca20e64dc46daa329743`. The reviewed author baseline is `fa296376d1b25b0d10459c00d02c58834c500b45`, paper tree `3787ef425f38505c6d715161bc045ac2eebf0609`.

## The new mathematical argument

Module 171 constructs a stopped transport between the original exact-label physical roof fibers. Its unmatched mass is exactly true exit mass plus positive transported-density loss. This removes artificial first-admissible cap reassignment from the comparison without deleting any real boundary contribution.

Module 172 proves the positive optical transfer identity and the explicit inverse-twist estimate with decay ratio `(53-10*sqrt(6))/47`, retaining simultaneous internal incidence gains. At an interior critical roof, a Morse-adapted forward transport has unit Euclidean Jacobian and does not charge the positive jump coefficient; its nonconstant-weight defect has a local square-root bound.

Module 173 proves complete-source persistence and the ordered implication from a quantitative true-exit/distortion bound to the original pointwise arithmetic law. The complete weighted dynamical bound itself is not asserted proved. The original topic, full pointwise target, exact labels, arithmetic zero classes and downstream objectives are unchanged.

## Preservation, status and review

All 170 inherited cores, all appendices, all inherited Python sources, and both bibliographies are unchanged. The complete v75 article is retained at `provenance/v75-main.tex` and assembled into the supplement. All prior source directories and review reports remain unchanged. Recorder coverage requires 173 cores across the two documents.

`SOURCE_MANIFEST.json` and `PUBLICATION_STATUS.json` state the current claims; inherited Boolean claims are checked against the frozen v75 manifest. `RESPONSE_TO_REFEREE.md` answers all eight requests individually. `PROOF_LEDGER.md` distinguishes inherited results from new proofs. `SPECIALIST_AUDIT.md` lists the checks still requiring independent specialists. Other inherited input maps and historical build notes are provenance, not current status authorities.

The new local journal build passed with nine pages and no TeX warnings. This does not certify the full inherited supplement or a remote checkout. The exact-SHA workflow is `.github/workflows/a2-dyn-v76-qualification.yml`; inspect its actual run result for remote qualification. No independent human review or formal proof certificate is claimed.
