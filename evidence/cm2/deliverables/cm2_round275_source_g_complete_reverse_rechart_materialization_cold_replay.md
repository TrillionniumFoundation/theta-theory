# Round275 cold replay

- producer seeds: `275071`, `275929`
- result SHA256 for both seeds:
  `9c33f2e8799b777cb14694c2917bd4c4cfec1b98a6f168227e1fec96a4495bd6`
- complete certificate SHA256 for both seeds:
  `e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386`
- byte comparison: identical
- independent verifier: `PASS_INDEPENDENT_ROUND275`
- semantic/structural attacks rejected: `5/5`

Both runs reconstruct all 880 guards from the frozen Round174/Round179
inputs.  The seed is deliberately excluded from the mathematical result and
cannot influence cover order, arrangement classification, signatures, row
order, or any digest.
