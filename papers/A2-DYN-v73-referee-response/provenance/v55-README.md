# A2-DYN, revision 55

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Active manuscript: `main.tex`. Controlling review: v54 at `7d4e3f6cafebf96da91d2d3a81147841418d9e61`; author baseline: `63135318e1eadd80341d4d0656a17e8caba60c90`.

## The new theorem

The normalized original exact-label roof density has a uniform weak `L^(145/144)` bound. The complete arithmetic scalar and path-valued raw laws hold in every local `L^q`, `1<q<145/144`, and in logarithmically weakened endpoint convex modulars. The corresponding forward likelihood and Renyi range is explicit under the unchanged pointwise arithmetic reference floor.

A finite two-regime estimate combines local thin mass `epsilon^(1/16)+exp(-kappa*m)` with exact global thin mass `m^2 epsilon`. It removes the finite-count error at all counts and protection scales. With polynomial protected height `epsilon^(-9)`, this gives a cap-free density-weighted tail `L^(-1/144)`. Both physical remainders have simultaneous finite-count power estimates `epsilon^(9(145/144-q))` and all-band correction estimates by convolution.

The two-sided pointwise arithmetic raw-density theorem remains the original target. Its positive incidence and clearance essential-height requirements are not asserted by these finite-norm results.

## Files

New proofs: `core/117_cap_free_boundary_layers.tex`, `core/118_endpoint_raw_laws.tex`. Itemized reply: `RESPONSE_TO_REFEREE.md`. Dependencies and exact scope: `PROOF_LEDGER.md`, `SPECIALIST_AUDIT_MAP.md`. Reproduction: `bash papers/A2-DYN-v55-referee-response/build.sh` from a full checkout. The read-only two-branch workflow qualifies the exact source SHA and renders the new theorem pages. All 116 old core files, 151 old Python files, the bibliography and 1549 old labels are retained; prior main/status files are under provenance.

A build receipt is not a continuum proof certificate or an independent human specialist review.
