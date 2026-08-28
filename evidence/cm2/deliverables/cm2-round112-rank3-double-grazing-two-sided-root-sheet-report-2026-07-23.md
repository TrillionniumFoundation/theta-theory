# CM2 Round112 — rank-3 double-grazing two-sided root sheets

Date: 2026-07-23  
Verdict: **VERIFIED local two-sided root-sheet geometry; CM2 remains NO-GO.**

## Result

Round112 freezes the first rigorous positive-width blow-up at all eight corrected `SOURCE_GRAZING` / designated-third-tangency corners:

- 8 HIT sheets;
- 8 BYPASS sheets;
- 16 independently replayed sheet rows in total;
- rational enclosing root box `0 <= c0,z3 <= 1/16384`, where `z3=c3` on HIT and `z3=b3` on BYPASS;
- exact source/HIT angle subbox boundary `sin(128^-2)`, certified by directed rounding to lie strictly inside `1/16384`;
- producer replay at 512 and 640 bits, plus a verifier that does not import the producer and recomputes at 768 bits.

Certificate result digest: `4e077c2b4703d475fb9dc21bcb0c56d8f2a634387f1dc66758160275dac2f917`  
Verification result digest: `ad6b1f789ab70916e09ecd035898ba461b6c10bf00a0722f917b69e434cafe4d`

## Coordinates and equations

The source grazing blow-up uses

```text
c0 = sqrt(1-p0^2),
p0 = sigma0 * sqrt(1-c0^2).
```

The two designated-third sides are kept separate:

```text
HIT:    F_hit(t,c0,c3)    = Delta3(t,c0) - R3^2 c3^2 = 0,
BYPASS: F_bypass(t,c0,b3) = Delta3(t,c0) + R3^2 b3^2 = 0.
```

For every sheet, both `t` faces have strict opposite signs, `partial_t F` has one strict sign on the whole enclosing box, and

```text
|partial_t F| > 3,
partial_c0 F < -3.
```

Therefore each parameter pair in the enclosing rectangle has a unique local `t` root.

The only valid nondegenerate corner Jacobian installed here is the blown-up one. With rows `(c0,F_sheet)` and columns `(c0,t)`,

```text
det D_(c0,t)(c0,F_sheet) = partial_t F_sheet,
|det| > 3.
```

No classical determinant in `p0` or in the squared coordinate `g0=1-p0^2=c0^2` is claimed. The computed `partial_c0 F` is strictly nonzero at the corner, so `Delta3` is not `C1` as a function of `g0` there; squaring the root coordinate would destroy the valid smooth chart.

## Geometry margins

Every row stores and the independent verifier recomputes:

- the actual rational `t` box and both face signs;
- `partial_t F`, `partial_c0 F`, and blown-up determinant enclosures;
- strict source adjacent-chart dominance `1-2t^2>0` on the entire box;
- selected first and second collision discriminants, cosine squares, and flights with `0 < flight < 3`;
- fixed selected outgoing charts and strict component/dominance margins;
- fixed designated-third transverse sign and positive longitudinal margin;
- on HIT, the strict forward near-flight margin `longitudinal3-R3*c3>0`;
- on BYPASS interior (`b3>0`), the equation identity `Delta3=-R3^2 b3^2<0`, hence the designated target is a whole-line miss; `b3=0` remains the tangent edge.

The producer adds a declared outward rational halo `1/1000000` to general stored interval evidence (and `1/10^20` to the angle boundary). The 768-bit verifier checks that every recomputed core enclosure is contained in its stored 512-bit hull. It also rejects 19 re-signed semantic/schema/enclosure attacks, including forged owners, 57-order promotion, false BYPASS status, false determinant lower bound, a classical-`C1` claim, forged IDs/sequences/conclusions, false stored enclosures, unknown keys, duplicate keys, and nonfinite JSON.

These are selected-lift geometry statements. They are not complete first/second owner-ordering statements.

## Homogeneity interface

For the HIT side only, the next legal angle partition may use the exact half-open strips

```text
sin((n+1)^-2) < c <= sin(n^-2),    n >= 128,
```

and hence the future double index `(sigma0,sigma3,j,k)` with `j,k>=128`. This is an admissible schema, not an installed countable-tail theorem. The BYPASS coordinate `b3` is an analytic miss-side normal coordinate, not a collision-angle homogeneity coordinate.

## Strict nonclaims

- No whole-box 57-candidate ordering is installed.
- Neither side installs an actual next owner.
- No official word, canonical child, or Gate5 field is installed.
- The local endpoint sheets are not whole trace collars.
- Round112 does not repair the Round101 seam-to-grazing chain or the Round102 face quotient.
- The certified width is not claimed optimal.

## Next core gate

Round113 should replay the complete immutable candidate tables on every positive-width sheet: prove the designated HIT candidate is the strict next owner, find and order the actual BYPASS next owner, then install the exact half-open source/actual-collision homogeneity children. Only those actual children may receive the first legal Gate5 field `F1`.
