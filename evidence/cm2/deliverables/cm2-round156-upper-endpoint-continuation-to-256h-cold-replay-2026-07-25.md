# CM2 Round156 — cold replay record

Date: 2026-07-25

The producer replay under `PYTHONHASHSEED=6156` is byte-identical to the
certificate produced under `PYTHONHASHSEED=156`. Both retain result SHA256
`b5e6b6d9fc596f5e005c568cc4dcd3d11cca8cc9c80ce323635c02c55f0df4a5`
and file SHA256
`3d4deffd799cfc3b01ddcd48bc8784c165a7b9778603facbcdc01d414f2ec347`.

The verifier replay under `PYTHONHASHSEED=6510` is byte-identical to the
verification produced under `PYTHONHASHSEED=651`. Both retain result SHA256
`5e27affce89eb5743368a98c6617cdfc396f66e3af48f7e674efa461e6ad711d`
and file SHA256
`f94cd81f563cb14458c50203dbc49e771d26f3dcf3bce92754e4f1dba33f6973`.

Final result: producer and verifier cold replays are byte-identical.
