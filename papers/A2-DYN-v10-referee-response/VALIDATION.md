# Revision 10 validation record

## Local source and native build

The starting files were obtained from the successful exact-source artifact of reviewed author commit `872f8695670373a3ca67ff84841a1ea38ed64227` (workflow run `37323262370`). The new revision is based remotely on its controlling review commit `8448e718a22658c94dcb654b52c69b44f9889fe1`.

`bash build.sh` completed in the working environment. It ran source preservation and finite diagnostics in normal and optimized Python modes, compared their JSON results, ran the inherited geometry/clock diagnostic programs and compiled the complete manuscript natively with `pdflatex -no-shell-escape` until references stabilized.

Results: **69 PDF pages; 27 unique core inclusions; 91 proof environments; 266 labels; all 24 inherited core files byte-identical.** The final TeX log contains no unresolved references, LaTeX/package warnings, overfull boxes or underfull boxes. The PDF was rendered and visually inspected at the introductory theorems, new central-band estimates and inversion corollary, both proof-detail appendices and references. No clipping or equation-number overlap was observed on those inspected pages.

The new finite arithmetic checks account for all eight polynomial error terms in the integrated estimate (the ninth term is exponentially small), analytic-domain and pointwise-cubic restrictions, the exact feasible exponent interval and the distinction between the new central radius and the old outer-tail cutoff. Fractional coarse interpolation was checked on 860 rational ratios. Historical finite compensation, chronological return and dyadic-prefix checks remain included.

## Remote qualification

`.github/workflows/a2-dyn-v10-qualification.yml` checks out the exact event SHA with read-only repository permissions, archives the complete source and mathematical baselines, and runs the same build. The artifact includes `build/main.pdf`, the native log, recorder, pass logs and `evidence/`. Its `build-receipt.json` records the actual checked-out SHA, event SHA, scoped clean-source state and source/PDF hashes. A source receipt may record null Git metadata for an extracted local archive; it must not record invented commit identity.

The workflow result must be read from the actual run. This static file does not assert a run outcome before execution.

## Verification boundary

Source preservation, exact rational diagnostics, successful native typesetting and visual inspection are distinct from continuum mathematical review. They do not prove the imported collision-space theorem, a Livsic regularity bridge, covariance nondegeneracy, the induced high-frequency estimates, the all-branch raw residual bound or the full raw LLT. No independent human reviewer or journal decision is represented by these checks.
