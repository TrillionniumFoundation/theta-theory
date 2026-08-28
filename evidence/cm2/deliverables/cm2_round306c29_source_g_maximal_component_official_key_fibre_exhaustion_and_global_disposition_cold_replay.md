# C29 Cold Replay

- Two hash seeds produced all three ledgers and the result byte-identically.
- Second producer replay: 173.30 seconds; peak RSS 284,756 KiB.
- Independent reconstruction: 176.49 seconds; peak RSS 285,524 KiB.
- Published manifest-first replay: 187.59 seconds; peak RSS 284,476 KiB.
- The verifier reconstructed 57,876 maximal-component rows, 124 official-key fibre rows, and 502,204 global member dispositions.
- The manifest-first replay performed one stdout write and zero deliverable writes.
