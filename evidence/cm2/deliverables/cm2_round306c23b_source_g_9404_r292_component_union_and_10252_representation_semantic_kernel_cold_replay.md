# C23b Cold Replay

- Two hash seeds produced the 19,656-row ledger and result byte-identically.
- Second producer replay: 59.72 seconds; peak RSS 163,084 KiB.
- Independent full reconstruction replay: 59.38 seconds; peak RSS 150,452 KiB.
- Published manifest-first replay: 60.08 seconds; peak RSS 147,660 KiB.
- The verifier rebuilt all 9,404 component unions, consumed exactly 848 sealed internal physical-face reglues, and reconstructed all 10,252 representation dispositions.
- The manifest-first replay recorded one stdout write and zero non-stdout writes.
