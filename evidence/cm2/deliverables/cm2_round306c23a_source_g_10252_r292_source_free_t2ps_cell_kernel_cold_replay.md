# C23a Cold Replay

- Two hash seeds produced the 10,252-row ledger and result byte-identically.
- Second producer replay: 76.93 seconds; peak RSS 58,892 KiB.
- Independent reconstruction replay: 79.94 seconds; peak RSS 58,460 KiB.
- Published manifest-first replay: 76.74 seconds; peak RSS 58,204 KiB.
- The verifier reconstructed every R287 source classification, exact R292 uncovered cell, C16 identity binding, T2PS branch map, and row byte.
- The manifest-first replay recorded one stdout write and zero non-stdout writes.
