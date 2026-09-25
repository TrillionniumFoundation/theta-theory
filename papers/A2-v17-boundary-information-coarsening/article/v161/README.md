# A2 revision 161 — controlling referee entry

Branch: `revision/a2-v161-multiple-incidence-contact-singularities-2026-09-25`.
Authored source commit: `e347ed575268adbf9b561f1b9826d533a72fe3d7`.
Controlling complete-v160 report: `596df442f9155c79b6b33378c0a208259385b2ae`.
Preserved complete predecessor: `58c33453bf01d1f73083cb744d0479ecdc3dcf2f`.

## Complete reading objects

**Paper I — Finite failure schemes and the reconstruction of quadratic pencils.** 68 pages. [PDF](reconstruction.pdf) · [complete standalone LaTeX](reconstruction.tex).

**Paper II — Power ideals and the Hilbert boundary of quadratic pencils.** 65 pages. [PDF](divisor-geometry.pdf) · [complete standalone LaTeX](divisor-geometry.tex).

**Preservation master — not a third submission.** 126 pages. [PDF](geometry.pdf) · [complete standalone LaTeX](geometry.tex).

Paper I has a seven-section main inverse proof; its full applications
and prior extensions are in appendices. Paper II has a six-section main
route ending in the multiple-incidence and higher-contact theorems;
all earlier power, spectral, collision and reciprocal-fibre extensions
remain in appendices. Embedded companion references are stable and do
not require an external auxiliary file.

[All 30 referee responses](RESPONSE_TO_V160_REPORT.md) ·
[Theorem/page index](THEOREM_INDEX_V161.json) ·
[Primary-source comparison](LITERATURE_AUDIT_V161.md) ·
[Build receipt](BUILD_RECEIPT_V161.json) ·
[Preservation audit](NONDELETION_V161.json) ·
[Exact checks](EXACT_CHECKS_V161.json).

## Principal changes

The full reduced corank-two incidence open now has a normalized Hilbert
modification given by a Fitting-ideal blow-up. Its entire fibre at k
incidences is (P^1)^k. Independence is proved from the distinct spectral
radicals, not assumed generically. Every symmetric Jordan contact slice
of order m >= 2 has an explicitly computed thick tail, length-m
attachment, A_(m-1) graph singularity and degree-m stable-map tail after
ramified base change. The effective stack, multi-Rees equations and
relative Artin lifting conditions are stated in their precise categories.

The full ambient nonreduced and higher-corank boundary is not claimed
classified by the slice theorem. The original all-pencil sharp inverse
and all inherited statements retain their scopes. The envelope is not a
subquotient of the original algebra, and the recovered pencil line is
an essential intermediate object of the boundary interpretation.

## Preservation and verification

All 421 predecessor labels and
277 mathematical environment blocks are
retained. The current master has 453 labels and
299 blocks. The audit checks old mathematical
blocks byte for byte and allocates the body exactly once across the
companions. All three previous introductions and the former root entry
are archived. The full inherited v160 check chain was actually executed.
Finite computations are audits of explicit equations, not certification
of universal proofs, historical priority or editorial acceptance.
The Ballico 1993 theorem/proof-level comparison remains incomplete in
both papers; a separate available 1996 theorem is not substituted for it.

The authored input commit above precedes the materialization commit
containing the complete sources and PDFs. After remote read-back,
`papers/A2-v17-boundary-information-coarsening/article/v161/PUBLICATION_SEAL_V161.json` records the output commit and the
checks actually performed. No self-referential commit hash is asserted.

## Reproduction

From this directory in a full branch checkout:

```sh
python3 check_v161.py
python3 assemble_v161.py --build
```

The complete `.tex` files can also be compiled independently with pdflatex.
