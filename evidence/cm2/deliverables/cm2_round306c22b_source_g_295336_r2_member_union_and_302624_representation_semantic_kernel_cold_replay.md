# C22b Cold Replay

- Two hash seeds produced the 302,624-row ledger and result byte-identically.
- Second producer replay: 296.11 seconds; peak RSS 312,148 KiB.
- Independent full reconstruction passed for all 295,336 member unions, 295,336 primary representation equalities, and 7,288 alias dispositions.
- Published manifest-first replay: 280.14 seconds; peak RSS 883,288 KiB.
- The manifest-first replay used an in-memory index and recorded one stdout write with zero non-stdout writes.
