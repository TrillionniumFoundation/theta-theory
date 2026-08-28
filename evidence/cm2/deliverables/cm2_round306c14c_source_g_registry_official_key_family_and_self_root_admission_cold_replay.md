# C14c cold replay

- Two scrubbed runs used `env -i`, `LANG=C`, `LC_ALL=C`, and `PYTHONHASHSEED=1` / `777`.
- Both runs exited 0 and were byte-for-byte identical to each other and to the initial candidate for all three generated artifacts.
- Seed 1: 2m09.55s, maximum RSS 2,147,808 KiB.
- Seed 777: 2m10.64s, maximum RSS 2,145,464 KiB.
- Published producer replay: 2m17.88s, maximum RSS 2,145,492 KiB.
- Manifest-first independent verifier on the published bytes: PASS, 2m12.00s, maximum RSS 2,201,020 KiB. `strace` recorded exactly one 240-byte write to stdout and zero writes to deliverables.
- No random seed is semantically consumed. The seed variation tests serialization/order independence only.

Strict boundary: C14c admits members, representations, official-key bindings, and self roots, and forces the retained old sheets into `NON_GRAPH`. It assigns no fresh component, edge, union, pullback, normalized-support, B1A, B2, maximality, or CM2 credit.
