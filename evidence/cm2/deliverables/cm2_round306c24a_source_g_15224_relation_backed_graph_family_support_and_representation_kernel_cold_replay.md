# C24a Cold Replay

- Two hash seeds produced the 15,224-row ledger and result byte-identically.
- Second producer replay: 194.34 seconds; peak RSS 5,527,352 KiB.
- Independent full reconstruction replay: 240.83 seconds; peak RSS 5,523,032 KiB.
- Published manifest-first replay: 207.72 seconds; peak RSS 5,525,300 KiB.
- The verifier rebuilt all exact support ASTs, C16 identity bindings, C16b relation theorems, and C17 pullback certificates row by row.
- The manifest-first replay recorded one stdout write and zero non-stdout writes.
