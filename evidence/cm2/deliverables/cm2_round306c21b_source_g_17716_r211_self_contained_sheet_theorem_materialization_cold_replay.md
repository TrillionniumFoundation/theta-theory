# C21b Cold Replay

- Two hash seeds produced both data outputs byte-identically.
- Second replay: 235.68 seconds; peak RSS 1,009,920 KiB.
- Published independent replay: 334.52 seconds; peak RSS 871,640 KiB.
- The independent replay rebuilt every formula and derivative AST, crosschecked symbolic differentiation against dual-number automatic differentiation, and recorded one stdout write with zero non-stdout writes.
