# C71 successor v2 pre-monotone staging rejection / supersession

Status: **REJECTED BEFORE PUBLICATION; SUPERSEDED; ZERO CREDIT**.

Two isolated prefinal staging builds were byte-identical, but their shared
result object `c564c760cc42260a5cf054f5599fc26b48a82b94f9498c1423d67247707d2f79`
left one of the 33,100 C69c-decision-source children as
`BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE`.  Their staged artifact
SHA256 values were:

- intersection rows: `38f46d7135028f9cf2bae220eb4197ca58a419523ed66abdc44ee88863e1ac15`
- source summaries: `8a20c6c35d30629b14adf475b609412a8dc82f67d46a2f6b07bd7d35fe69b21a`
- result: `9c6f7f91fa7effef85321104fdf6e9ba0c4c27087f757ef42efa694616b1f9d3`
- report: `e239e9a0445df6e29bdc0009519ee3045bfd2b0e33b443db17601efbd3fca2b4`

The lone row was pair 631, child path
`011110101000001011110010111`.  Its full-child-box `dH1/dt` and `dH1/dp`
are uniformly strictly positive, while the monotone maximum corner
`(t1,p1)` has the strict upper bound approximately
`-1.016724192422537e-10`.  Thus coordinate monotonicity proves the entire
child has `H1<0`; with both normal components strictly negative it is an
S-side strict slab.  Treating it as inconclusive was sound but incomplete.

The successor contract and both independent implementations now include the
rigorous method `MONOTONE_COORDINATE_CORNER_EXTREMUM_STRICT_SIDE`.  The above
bytes were never published, never installed, and may not be consumed.  Their
formal, whole-parent, terminal-disposition, and D02 credit are all zero.
