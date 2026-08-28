# C24b Cold Replay

- Two hash seeds produced the 168-row ledger and result byte-identically.
- Second producer replay: 98.44 seconds; peak RSS 27,608 KiB.
- Independent full reconstruction replay: 97.93 seconds; peak RSS 27,776 KiB.
- Published manifest-first replay: 104.19 seconds; peak RSS 27,328 KiB.
- The verifier rebuilt every exact one-sided carrier, C13 empty-branch certificate, C16 identity binding, and `EMPTY_SET` support equality.
- The manifest-first replay recorded one stdout write and zero non-stdout writes.
