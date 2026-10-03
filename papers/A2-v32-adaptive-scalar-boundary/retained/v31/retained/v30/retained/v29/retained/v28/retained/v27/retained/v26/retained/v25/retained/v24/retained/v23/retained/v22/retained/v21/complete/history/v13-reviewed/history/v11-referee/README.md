# A2 v11 independent harsh review

Review date: 10 September 2026. Start with [REFEREE_REPORT.md](REFEREE_REPORT.md).

Reviewed source: `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`, on `revision/a2-v11-abel-stable-boundary-profiles-2026-09-10`.

Recommendation: reject at the requested top-four mathematics-journal level in the present form. No fatal error was found in the new principal proofs examined. Previous acquisition and specified smooth-class calibration objections are explicitly closed.

The report supplies a new two-derivative regularity argument. With the same profile assumptions, it improves the sufficient preparation power from `2+6/(m-5/2)+gamma/|log(tau)|` to `2+6/(m-1/2)+gamma/|log(tau)|`; unknown calibration uses `gamma_+`. This is not a counterexample to the weaker bound or a minimax claim.

`SOURCE_AUDIT.json` records pinned files and coverage. `verify_review.py` provides independent standard-library exact arithmetic checks; `checks.json` and `VERIFICATION.json` record actual runs and limitations.

```sh
python verify_review.py --output checks.normal.json
python -O verify_review.py --output checks.optimized.json
cmp checks.normal.json checks.optimized.json
```

No manuscript, old review, or existing revision path is changed by this review packet. This is author-requested AI-assisted refereeing, not a commissioned journal report or a formal proof certificate.
