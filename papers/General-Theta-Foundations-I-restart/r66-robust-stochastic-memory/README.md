# General Theta Foundations I — R66 author revision

Start with `main.tex`, the current `supplement.tex`, and `RESPONSE_TO_REFEREE.md`. Keep the paired PDFs together for cross-document links. The original title and Annals / Acta / Inventiones / JAMS objective are unchanged.

## New mathematics

`sections/23-robust-realization.tex` proves a weighted cost-potential rigidity identity for state- and model-dependent herald instruments; a robust optimal face allowing arbitrary Bayes ties; an anchored invariant-convex-family characterization of exact stochastic live memory; and a random-horizon calibration theorem forcing replication of every protected Born probability. It gives exact memory k for every k>=2, finite versus infinite realization for a damped algebraic qubit, a globally sharp three-label threshold, and finite algebraic certificates which yield minimal exact synthesis for the strictly damped family. Classical residual, Hankel and positive-realization ingredients are explicitly credited.

The new realization criterion is not a generic finite algorithm for arbitrary robust optimal faces. Its explicit algebraic algorithm assumes a supplied finite linear response and, for minimal synthesis, a proved size upper. The calibration loss is different from the preserved squared-sign prediction loss. No general-M solution of that older risk frontier or of the separate timing problem is claimed.

## Immutable baseline and review

The complete author source is continued from R65 source `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`, delivered at `ee79ca9114f8009d62c056d07381b766645e3fc4`. Its exact paper tree `3a0ea744d1e4721f2c47b5e038023becd4da2ce0` is fully retained in `retained/r65-native/`.

The controlling R65 report is commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, blob `d1ff9c5662390156ee212c82b173e86a21180e84`. It reviews R65, not R66. It was read in full from the repository; its unchanged Git object accompanies the remote publication directory. The local source contains an explicit reference rather than falsely treating an unmaterialized body as locally rehashed. All earlier reports and author responses retain their separate identities.

## Build and verification

Run `python3 verify.py --out /tmp/theta-r66-build --source-commit <exact-SHA>` with the pinned Python packages and native LaTeX dependencies. All outputs must be outside the source tree. The verifier checks the complete source manifest and retained predecessor tree, runs six diagnostic generations in ordinary and optimized Python, builds the main and supplement in alternating native passes, builds the complete R58 companion, and checks the theorem map against actual auxiliary files.

`MINIMAL_READING_GUIDE.md` separates the new proof chain from complementary current results and frozen historical material. The complete exported historical text corpus and its rehash record accompany the downloadable review package. Historical scanning is not a reproof of every archived theorem.

Only an actually completed workflow with the correct SHA is a hosted pass. Local diagnostics and native compilation are not formal proof, independent human approval, exhaustive priority certification, or an editorial decision.
