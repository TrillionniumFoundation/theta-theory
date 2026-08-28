# K2R233 cold replay

Environment: `.venv-cm2`, Python 3.12, `python-flint 0.9.0`.

Two final publish replays of the frozen verifier were run with independent hash
seeds:

- `PYTHONHASHSEED=233017`: rc `0`, `97.75` s, peak RSS `2,393,888` KiB;
- `PYTHONHASHSEED=233093`: rc `0`, `98.25` s, peak RSS `2,393,220` KiB.

Both runs reproduced byte-identical ledger, attack, and verification files:

- ledger `4c1a097c2c42dd71323a0276e7bb81dedad330bcdcf02572288009db6c563c1c`;
- attack `ebe10211757401a849ee1178202f025b0e4c106f4e64934ccc8b61e830d69240`;
- verification `7180d972020c39b0680d47cf0eee34355c64776f0777c88525cd13a7c2893c5b`;
- verification result `b45d127bec5f1321ceb5ca49a5a2207d8cddfb87d3468da6169b465d4d503391`.

Both closed `38,872/38,872` selected row appearances and `3,148/3,148`
input-bound conclusions.  Main replay used no spill file and ignored `TMPDIR`.
The embedded attack suite passed `14/14` coherent attacks.

