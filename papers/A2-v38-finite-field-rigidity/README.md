# A2 v38 — finite-field and isotropic collision rigidity

**Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.**

The complete manuscript is [main.tex](main.tex). It continues the existing v37
revision at `02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d` and responds to the same
controlling v36 external report at `3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`.
No subsequent A2 review was found when this revision was initiated; v38 does
not describe v37 as having received a new referee report.

Author branch: `revision/a2-v38-finite-field-rigidity-2026-10-04`.
Referee-copy branch: `revision/a2-v38-referee-copy-2026-10-04`.
The final delivery uses identical commits on these branches; neither is main.

## Mathematical content

The new finite-stencil theorem expresses pointwise occupation as a linear
program on a fixed killed compass walk. It includes a converse realization
of feasible occupation measures, a dual certificate, and an inverse modulus
for arbitrary nonphysical measurement errors. At accuracy epsilon it uses
at most `2 M ceil(8 H_S^2 epsilon^-2 log(4M/delta))` attempted bits at `M`
fixed nominal sites. The computational boundary is not assumed to be a
physical zero set. No boundary-mass, smoothness, or periodicity assumption
is needed for this pointwise result.

A second extension proves exact period rigidity for every bounded centered
displacement law of positive second moment. For uniform directions,
`integral F = (t/pi) perimeter(C)` gives an intrinsic footprint deficit.
It recovers translated homothetic footprints without a preferred direction,
common origin, or cross-setting component labels. Exact homothety, labelled
settings, separation, and the prescribed reciprocal joint law remain inputs.

All 24 v37 core files are copied byte-for-byte and remain active. This retains
the global period theorem, complete translation ambiguity, finite periodic
reconstruction, sharp stationary power `(3s/2+1)/(s-2)`, and all historical
localized and calibration proofs. One logarithmic factor remains in the
stationary minimax bracket. The finite-stencil occupation count is not a
replacement boundary minimax rate or a finite crystallinity certificate.

## Reading and reproduction

[Response to referees](RESPONSE_TO_REFEREES.md) maps every controlling
qualification to the revised manuscript. [Proof ledger](PROOF_LEDGER.md)
records the new arguments and dependencies. [History and literature audit](HISTORY_AND_LITERATURE.md)
separates retained achievements from this revision. [Submission map](SUBMISSION_MAP.md)
provides source and output navigation. [Source pins](SOURCE_PINS.json)
identify the immutable baseline and controlling review.

From this directory in a clean checkout, run:

```sh
python3 tools/validate_v38.py --expected-head "$(git rev-parse HEAD)"
```

The validator checks exact source bytes, retained core identities, active
inputs, labels and citations; executes exact finite diagnostics in ordinary
and optimized Python; builds the complete primary; and creates a SHA-bound
receipt, PDF, logs and source archive under `verification/current/`.
The workflow `.github/workflows/a2-v38-verify.yml` performs the same checks.
Build and finite checks are not formal proofs or physical experiments. This
README does not predeclare the success of a future hosted run.
