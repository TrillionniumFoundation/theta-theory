# A2 v37 — scalar response rigidity and the stationary minimax power

**Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.**

This is the complete revision responding to the external v36 report at commit
`3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`, which reviewed the v36 author source
`2559749a038fd2b5ec46d7cc74fdb4bd844b266a`. The controlling report is
[`../../reviews/a2-v36-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md`](../../reviews/a2-v36-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md).

The author branch is `revision/a2-v37-stationary-rigidity-2026-10-04`.
The identical referee-copy branch is `revision/a2-v37-referee-copy-2026-10-04`.
Both are intended to resolve to the same qualified commit. The manuscript entry
point is [`main.tex`](main.tex). It includes every required proof and reference.
The native draft has 65 pages.

## Principal mathematical changes

1. **A global inverse without a supplied positive set.** Theorem 2.2 reconstructs
   occupation from the reciprocal difference by a stopped-Poisson formula and
   an exponentially convergent obstacle iteration. The class consists of
   arbitrary locally finite, uniformly bounded and separated convex components.
   Neither periodicity nor a finite species list is assumed.
2. **The full translation group is an observable invariant.** Theorem 2.4 proves
   `Per(F,R) = Per(F-R) = Per(O)`. Rank-two crystallinity is therefore determined
   by the exact full response field without a periodicity prior.
3. **Unknown setting origins and scales.** Theorem 3.2 reconstructs homothetic
   footprints with independent unknown translations. Width deficits identify
   scale ratios without matched components. Centered support envelopes recover
   the footprint and the translated configuration. Corollary 3.3 classifies the
   complete geometric ambiguity. Theorem 3.5 and Corollary 3.6 give finite
   reconstruction for periodic and finite nonperiodic configurations,
   respectively, under their quantitative acquisition hypotheses.
4. **The stationary polynomial gap is closed.** Theorem 4.4 proves the lower
   power `(3s/2+1)/(s-2)` for a common uniform-disk launch law, including adaptive
   commands with arbitrarily small length. The physical estimate is a uniform
   squared-Hellinger bound of order `epsilon^(3/2)`. Proposition 4.5 removes one
   logarithm from the upper construction. Corollary 4.6 matches the minimax
   power for both pooled-compass and arbitrary-short-command designs, on the
   same physical class and worst-case expected-cost criterion.

The revised primary begins with these results. Sections 5–9 retain the
stationary, footprint, rare-query, scalar-normalization and earlier converse
arguments. Section 10 gives the literature and information-model comparison.
Appendices A–H retain the complete localized, finite-control, period-locking,
physical-packing and calibration arguments.

## Reading and audit documents

| File | Purpose |
| --- | --- |
| [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md) | Direct response to the controlling report, including each qualification in §6 and both substantive issues in §7 |
| [SUBMISSION_MAP.md](SUBMISSION_MAP.md) | Result locations, model distinctions, source and evidence navigation |
| [PROOF_LEDGER.md](PROOF_LEDGER.md) | The sixteen new proved results, dependencies and delicate proof steps |
| [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md) | Exact source lineage and use of historical derivations |
| [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) | Primary-source comparisons and the limits of each comparison |
| [SOURCE_PINS.json](SOURCE_PINS.json) | Hashes of all revision sources and preserved historical trees |

## Source qualification

From this directory, with Python 3, `latexmk`, `pdflatex`, the listed TeX
packages and Poppler installed, run:

```sh
python3 tools/validate_v37.py --expected-head "$(git rev-parse HEAD)"
```

The validator checks committed source bytes, active TeX closure, preserved
historical trees and proof bodies; runs finite diagnostics and contract checks
in ordinary and optimized Python; builds the primary; and writes evidence under
`verification/current/`. The evidence contains the PDF, journal and repository
source archives, source pins, build logs, receipt and artifact binding. It is
generated from the checked source and is not checked back into the manuscript.

For a development checkout only, `--allow-dirty` runs the checks without claiming
qualification of a commit. After intentional source edits,
`--freeze-manifest` updates the source manifest. A publication qualification
must use a clean committed checkout and its exact expected SHA.

The workflow [a2-v37-verify.yml](../../.github/workflows/a2-v37-verify.yml) checks
the actual triggering SHA and uploads the same evidence, including a failure
receipt if a gate fails. Its artifact name is `A2-v37-<SHA>-<run-attempt>`.
A hosted success claim must be read from the run and receipt for that SHA;
this source document does not predeclare a future workflow result.

All 162 v36 labels and all 43 v36 proof bodies remain active; those proof bodies
are byte-identical. The revision contains 233 labels, 59 proof bodies and 62
formal statements. The old paper and review directories are unchanged. Finite
diagnostics check explicit finite algebra and models; continuum arguments are
given in the manuscript itself.

## Scope of the new statements

The exact global inverse uses whole-field data and no patch margin. Uniform
finite periodic decisions retain the quantitative nonperiod-patch margin.
Finite reconstruction with unknown setting translations uses a known coarse
bound on those translations to keep the aperture fixed. The finite nonperiodic
corollary instead assumes that its protected aperture contains every component
and required response envelope.

The sharp statistical power concerns a fixed positive uniform-disk spread and
fixed confidence. One logarithmic factor remains between the bounds. The
density-independent upper results are more general, but sharpness for every
boundary-mass exponent is not claimed. All attempts, including solid starts and
misses, are counted. Distinct sites, center-labelled batches, repetitions and
digital descriptions are accounted for separately.
