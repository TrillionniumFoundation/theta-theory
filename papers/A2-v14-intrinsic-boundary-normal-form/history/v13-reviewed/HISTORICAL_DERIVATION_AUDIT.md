# Historical derivation and source audit — A2 v13

## Authoritative source

The live GitHub v12 author commit is
`2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`; its native manuscript tree is
`cc541ad7590229be38cddf5d25a8461c8f17de30`. The latest report used for this
revision is at `2ae2751f61224b66f314915fd5fc22f6321b606f`, whose parent is
that author commit. The new root is based on the review commit and adds a
new manuscript directory; the earlier sources and report remain unchanged.

For local compilation, an earlier complete source archive was accepted
only after checking all 110 native file blob hashes in its manifest. Its
unchanged subtrees were compared with the live v12 tree. The computed
sections/v2/v3/v4/v6/v7 subtree hashes match the live native tree exactly.
Changed v12 main, bibliography and the three new v12 mathematical sections
were reconstructed from live reads and checked against their Git blob
hashes. A differently organized v12 payload archive was not substituted
for the reviewed source. The reference is the pinned live Git tree.

## Historical mathematical material used

`v3/10_geometry_action.tex`: convex first-hit localization, alternating
Jacobi scaling, finite bridge, relative cofactor and differentiated bounds.
`v3/20_integration.tex`: full-phase normalization, residual-time interval,
common Morse-domain integration and uniform onset derivatives.
`v4/10_boundary_layers.tex`: half-line stationary action, trace-class
amplitude, relative two-boundary gluing, physical limiting law.
`v5/15_differentiated_operators.tex` and
`article/15_operator_comparison.tex`: derivative and operator comparisons.
`v5/20_contact_rigidity.tex`: highest-jet degree bookkeeping, action and
amplitude contributions, earlier identical-contact recursion.
`article/20_boundary_compatibility.tex`: full smooth energy-profile
representation, Volterra uniqueness and finite coefficient structure.
`article/21_abel_stability.tex`: the actual Abel seminorm and stability.
The three v12 core sections supply the independent limiting block,
physical support realization and corrected integrated-flux observation.
The latest referee report supplies the all-order two-flight comparator.

The new proof recomputes the finite Schur complement rather than applying
the half-line block at finite length. Its twist contribution is checked
against the reviewed `finite_block_row` routine at j=2. This historical
connection is acknowledged explicitly; the older finite routine is neither
deleted nor described as erroneous.

## Preservation method

The published v13 native tree is built on the exact live v12 native tree.
Only the new front matter, new Section 11, bibliography addition, current
revision metadata and verification additions differ. Replaced v12 text
and metadata are copied to `history/v12-reviewed/` by their original blob
identifiers. Prior directories, tools, history and proofs are retained.
The active-source verifier compares the sorted byte-hash multiset of all
212 reviewed formal blocks and the reviewed input set. All are present;
six new formal blocks bring the total to 218.

This is a targeted derivation audit for the latest report, not a claim to
have independently re-proved every historical assertion in the repository.
