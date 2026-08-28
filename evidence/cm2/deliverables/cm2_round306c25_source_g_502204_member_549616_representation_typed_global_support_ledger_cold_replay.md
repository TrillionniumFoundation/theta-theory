# C25 Cold Replay

- Two hash seeds produced both global ledgers and the result byte-identically.
- Second producer replay: 341.49 seconds; peak RSS 765,420 KiB.
- Independent full reconstruction: 341.42 seconds; peak RSS 766,548 KiB.
- Published manifest-first replay: 345.19 seconds; peak RSS 766,412 KiB.
- The verifier reconstructed all 502,204 member rows and 549,616 representation rows from the sealed C15/C16 and C19-C24 inputs.
- The manifest-first replay performed one stdout write and zero deliverable writes.
