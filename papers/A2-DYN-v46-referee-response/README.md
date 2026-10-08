# A2-DYN, revision 46

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The frozen author baseline is revision 45 at `5ab781065787b1aca00ff5182a62da49f847d2e4`; the controlling external report is at `0ada8feead815b267b530a92ed4e14f5445867f2`. This revision retains the original four-coordinate actual-return problem and its arithmetic transition main term.

## New mathematical content

`core/98_noncritical_window_transport.tex` extends endpoint continuation and relative distortion from critical centers to arbitrary protected regular sources. An explicit graded guard has a word-length-independent weak endpoint derivative. The roof-translation flow converts an exact-label level integral into a positive fixed roof-window mass. The inherited arithmetic interval law then gives an actual `O(m^-2)` first-derivative budget for the protected noncritical density. Integration by parts keeps all physical and decision-boundary terms accounted for.

`core/99_protected_raw_reduction.tex` completes a near-normal protected source to an actual protected critical center. The critical-cluster estimate and the new regular estimate control the entire smoothly protected signed correction. For fixed `B >= C epsilon^-12`, its normalized collision limsup is `O(B^-1/2)`. For fixed protection it also tends to zero for any diverging bandwidth, without a claimed rate in the collision count. A direct one-flight geometry argument gives a uniform `O(epsilon)` mass bound on the complementary source. At `epsilon(B)=A B^-1/12`, the full arithmetic raw theorem is reduced to the signed correction of this positive collapsing-margin source.

The remaining boundary correction is not proved pointwise small. Its small mass, the old exponential height bound, and the new qualitative count diagonal are not substitutes for that estimate. No unmodulated arithmetic law, complete weighted pointwise bridge, or independent human audit is claimed.

## Source and execution

All 97 inherited core modules and all 119 inherited Python scripts remain byte-identical. The full article includes 99 numbered core modules and the compiled A--X synopsis. The preceding main, bibliography, manifest, response and proof ledger are archived under `provenance/v45-*`.

Run `bash papers/A2-DYN-v46-referee-response/build.sh` from a complete checkout. The revision-specific verifier checks frozen baseline identity, unchanged inherited sources, all inclusions and references, the ordinary-source Merkle manifest, controlling report and workflow hashes, and normal/optimized finite diagnostics. The read-only workflow builds and renders the exact event SHA. Dynamic receipts distinguish source and typesetting checks from continuum proof verification.
