# C22a Cold Replay

- Two hash seeds produced the ledger and result byte-identically.
- Second producer replay: 204.08 seconds; peak RSS 1,007,000 KiB.
- First independent replay: 185.81 seconds; peak RSS 1,009,152 KiB.
- Published manifest-first replay: 183.97 seconds; peak RSS 1,002,848 KiB.
- The independent replay reconstructed all 295,340 source-free predicate-cell support equalities and all source authority joins.
- The manifest-first replay recorded one stdout write and zero non-stdout writes.
