# A2-DYN revision 43

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The full manuscript is `main.tex`. This revision responds to the v42 report at `1d854ffbf468393c80e4f1bb744bfdadbb3e15a8`, from author baseline `7e155f0fda2a7a5f77a061ed5b54cab5943fb24b`.

The new modules are `92_count_compatible_raw_correction.tex` and `93_complete_raw_inversion.tex`. They construct a count-compatible correction for the complete raw law, including all singular/decision-boundary germs, with arbitrarily prescribed total-variation mass. The correction converges absolutely over every actual collision label. Each residual has an absolute roof inverse; label-dependent bandwidths certify a prescribed summed pointwise reconstruction error. The arithmetic transition kernel is the main term in an exact full-source raw-closure criterion.

This is not a claim of a full raw density LLT: the signed central-scale correction has not been shown small. The new all-boundary localized germ series is not the unlocalized regular-word exponential two-jet series. Neither summed second-derivative bounds nor a quantitative growing-band spectral theorem follow from the mass budget.

All 91 inherited cores, the bibliography, all inherited Python scripts, all inherited labels and the compiled A--X statements are retained. See `RESPONSE_TO_REFEREE.md` for the nine requests and the exact remaining boundary, `PROOF_LEDGER.md` for dependencies, and `SPECIALIST_AUDIT_MAP.md` for verification questions.

Build: `bash papers/A2-DYN-v43-referee-response/build.sh`. Exact remote receipts, including event SHA, run ID, clean-source state and PDF hash, are generated in `evidence/build-receipt.json`. A source build is not a continuum proof certificate or independent human review.
