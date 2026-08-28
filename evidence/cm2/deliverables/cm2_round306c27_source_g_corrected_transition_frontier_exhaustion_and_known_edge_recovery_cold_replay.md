# C27 Cold Replay

- Two hash seeds produced both transition ledgers and the result byte-identically.
- Second producer replay: 124.85 seconds; peak RSS 124,528 KiB.
- Independent full reconstruction: 128.18 seconds; peak RSS 124,680 KiB.
- Published manifest-first replay: 131.11 seconds; peak RSS 124,000 KiB.
- The verifier reconstructed all 487,582 transition candidates and all 20 transition-family exhaustion rows.
- The manifest-first replay performed one stdout write and zero deliverable writes.
