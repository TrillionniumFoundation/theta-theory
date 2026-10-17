# General Theta Foundations I — R67 author continuation

**Current mathematical entry:** `main.tex`, `supplement.tex`, `RESPONSE_TO_REFEREE.md`, `MINIMAL_READING_GUIDE.md`. The original title and Annals / Acta / Inventiones / JAMS objective remain unchanged.

This continues complete R66 source c9b19397af8dcb68dd32506e38ee8add5ca6f299, delivered at c8980d067272984990709de3c964464f6c8dca78. R66's entire native mathematical closure reproduces its published PDFs exactly and is retained; its new proof and diagnostic bodies match the remote Git blobs. R66's already completed robust-tie and damped-qubit results are inherited, not claimed as new in this continuation.

The new core gives an exact normalized-budget stopping criterion, a common squared-loss probability-replication construction, a finite rational uncertainty family with an explicit lower-memory risk gap, and exact algebraic optimization of the unknown robust risk at prescribed finite memory. It does not settle general multi-command boundary stopping or the sharp general-M squared-sign qubit frontier.

Build outside the source directory with:

```sh
python verify.py --out /tmp/theta-r67-rebuild --source-commit <actual-checked-out-SHA>
```

The verifier checks the source manifest, complete retained R65 tree, retained native R66 inputs and exact R66 diagnostic bytes; runs inherited and new diagnostics in ordinary and optimized Python; builds paired native manuscript/supplement and the retained companion; and checks actual theorem numbers/pages. All outputs are outside the immutable source. The source SHA is checked against Git HEAD when a checkout is present.

The accompanying delivery record states the actual commit and remote-push status. A local source-bound build, an old run, or a queued workflow is not a successful hosted rebuild. No existing paper folder, old report, or old branch is intentionally overwritten.
