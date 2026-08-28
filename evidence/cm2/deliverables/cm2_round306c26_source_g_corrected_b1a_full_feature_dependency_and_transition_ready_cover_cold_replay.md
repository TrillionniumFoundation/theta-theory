# C26 Cold Replay

- Two hash seeds produced both B1A ledgers and the result byte-identically.
- Second producer replay: 348.61 seconds; peak RSS 200,268 KiB.
- Independent full reconstruction: 373.43 seconds; peak RSS 224,456 KiB.
- Published manifest-first replay: 376.22 seconds; peak RSS 225,520 KiB.
- The verifier reconstructed all 691,424 feature obligations and all 549,616 transition-ready representation handles.
- The manifest-first replay performed one stdout write and zero deliverable writes.
