# C14d cold replay

- Scrubbed `env -i` runs with `PYTHONHASHSEED=1` and `777` exited 0.
- Both runs and the initial candidate were byte-for-byte identical for the edge ledger, empty negative-disposition ledger, and result.
- Seed 1: 33.35s, maximum RSS 808,192 KiB.
- Seed 777: 32.02s, maximum RSS 808,668 KiB.
- Published producer replay: 33.24s, maximum RSS 808,464 KiB.
- The manifest-first independent verifier rechecks all nine sealed members and independently rebuilds the C14c x C11a x C6 join.

Strict boundary: the 8,864 edges have rowwise authority, but none is applied to a DSU in C14d. Component/rank-reduction figures remain conditional until the fresh DSU seal.
