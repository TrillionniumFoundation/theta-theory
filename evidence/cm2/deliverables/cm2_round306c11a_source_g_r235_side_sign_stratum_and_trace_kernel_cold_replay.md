# C11a cold replay

The producer was run with `python3 -I -B` under an environment reduced to `PATH`, `LANG=C`, `LC_ALL=C`, and `TZ=UTC`.

The cold output was byte-identical to both ordinary seeds:

- kernel ledger: `87a37e007408adf667ae30a7575c928263512bf8a08cfd9e7144db11296680cd`
- result: `0450965cdebb245532fbfd2875d78306b0f2d237ef3976ec29f9bcf9038abdb8`

The formally published bytes passed the independent verifier. The coherent attack suite rejected 8/8 mutations after recomputing compression, descriptors, and result closure.
