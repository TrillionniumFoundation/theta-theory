# Resource ledger — revision 32

The exact principal model is Definition 2.1 (stable label `def:machine`; use the built theorem-location file for numbering). Counts are available persistent labels, including all retained private randomness. A current atomic symbol is read in the update, but cannot be reread later without storage. Table construction, read-only program size and arithmetic are not charged. A phase-dependent clock is external.

| Construction or bound | Internal profile / peak | Additional conventions |
|---|---|---|
| Separate rotation cut | 3 | The other cuts of its embedding may have large registers. |
| Rational counter realization | `3(t+1)` after t commands; peak `3(N+1)` | Stores vertex index and actual count of rotation commands. Initial singleton and final binary output included. |
| Polygon realization | `M=4*ceil(sqrt(N+1))` at every internal cut | Stores one label; real vertices are row descriptions, not runtime vectors. Command rows may be common across epochs; decoder depends on N. |
| Golden-angle converse | `sum_(t<N)2^(-6*K_t)<=24000000` | All stochastic, cut-dependent, hidden-state implementations; no residual-only restriction. |
| Tagged m-fold primitive | `(3m+j,4m-j)`, j=0,...,m | Terminal `(tag,bit)` alphabet has 2m labels. Tag must pass through internal memory. |
| Rational row fair-bit implementation | Separate additional sampler workspace | Use retained v31 self-paced sampler; its cost depends on denominators and is not the atomic optimum. |

The initial seed is an atomic symbol in an alphabet of size four; commands and terminal queries each have two symbols. Exact full response laws are required on all input words. The tag construction deliberately has wrong-tag zeros and growing initial/output alphabets. Only the rotation family is claimed fixed-alphabet and uniformly full support. No probability distribution on the external commands is supplied to weaken the requirement.

No minimum autonomous total-state count, input-length recognition bound, succinct program-size claim, finite-denominator golden-angle sampler or horizon-uniform approximation tolerance is asserted. The separate-positive-rank statement is stronger than an ordinary rank statement but is not a simultaneous factorization claim.
