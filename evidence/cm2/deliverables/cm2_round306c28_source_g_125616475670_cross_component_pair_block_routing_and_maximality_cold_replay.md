# C28 Cold Replay

- Two hash seeds produced both routing ledgers and the result byte-identically.
- Second producer replay: 43.16 seconds; peak RSS 146,944 KiB.
- Independent reconstruction: 46.94 seconds; peak RSS 137,464 KiB.
- Published manifest-first replay: 45.55 seconds; peak RSS 135,080 KiB.
- The verifier reassigned all 502,204 members, rebuilt all 57,876 component block profiles, and reconstructed all 32,896 pair-route shards.
- The manifest-first replay performed one stdout write and zero deliverable writes.
