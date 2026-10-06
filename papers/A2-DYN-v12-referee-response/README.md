# A2-DYN — revision 12

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi — 6 October 2026

Revision 12 is the source-repair and exact-requalification revision responding to the substantive revision-11 report at commit `fd84da57359a3ad2fefed532b0b5094ab8c6e436`. The reviewed author SHA was `dfacd56110f80a9621671028d2aa0a5782659055`.

The mathematical topic and theorem package are retained. In particular, the Gaussian/FCLT chain, growing integrated central band, single marked-return theorem, periodic arithmetic, critical-edge calculations, and raw mixed-density endpoint are all kept. No theorem is removed or recast as a no-go result.

## Exact repairs

Revision 11 failed its own exact-SHA preservation check because `core/06_downstream.tex` differed from the revision-10 baseline. Revision 12 restores that file from the reviewed revision-10 blob `20df3335f2c8e2819e23dc1bfdc70d6f3bc96c4b`.

It also repairs the visible TeX defects identified by the referee:

- `\nef{sec:marked-return-band}` is corrected to `\ref{sec:marked-return-band}`;
- the stray `.+` fragment in the marked-event display is removed;
- Theorem C now states locally that its transform uses `nu|_{Y_R^*}` and that division by `c_*` converts it to the normalized section probability.

All other v11 core files are preserved byte-for-byte except `core/28_marked_return_band.tex`, whose only mathematical-source change is the displayed-event syntax repair above. The full raw-LLT endpoint remains unchanged.

## Verification

Run `bash build.sh` in this directory. The active verifier checks exact restoration, inherited-file identity, known-defect removal, one-time core inclusion, reference integrity, and the inherited v11 marked-return/exponent diagnostics.

The corresponding exact-event workflow is `.github/workflows/a2-dyn-v12-qualification.yml`.

## Mathematical scope

Revision 12 repairs and requalifies the reviewed mathematical object; it does not manufacture claims that the substantive referee explicitly found still open. Uniform positive definiteness, the complete complementary-frequency integral, the full critical/singular residual sum, and exact-event weighted raw tails remain the next mathematical closure targets. Their statements and interfaces remain in the paper, and the original raw mixed-density topic is preserved.
