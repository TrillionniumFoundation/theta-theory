# Resource ledger — revision 39

| Quantity | Charged or specified convention |
|---|---|
| Label width | Maximum available persistent labels in the complete finite, clocked transducer, including constituent branch identifiers. |
| Label bits | Ceiling of log2 of the label count; a polynomial number of labels is logarithmic label-bit growth. |
| Initialization | Stochastic seed-dependent kernel; no copy of the seed remains outside the label. |
| Commands | One actual input from a fixed finite alphabet at each epoch; no future command is available. |
| Query | One selected coordinate at the declared terminal time; no joint independent output law is requested. |
| Decoder | Bounded in [-1,1], may depend on N. A held binary answer uses a separate two-label cut. |
| Rows | Exact atomic stochastic kernels; common command rows suffice for the upper construction. |
| Advice and computation | Epoch, horizon, row tables, table construction/lookup and arithmetic are not charged. This is not uniform computational space or total branching-program size. |
| Gap | Full mean-zero compact-group norm gap, imported where externally needed. A finite representation truncation is insufficient. |
| Direct sum | Probability d_i/D selects branch i. Its conditional signal is multiplied by D/d_i. All branches occupy a disjoint union of paid labels. |
| General signal | rho<=min(1/10,1/(8D)) for arbitrary spanning seeds in a reducible space. |
| Minimal-orbit seeds | Original irreducible/projective rho<=1/10 range remains valid. |
| Error | Fixed uniform binary row-TV; explicit seed-activation threshold in the reducible theorem. |
| Quantum dimension | Fixed q for the preserved complex projective example; not equated with classical label bits or arbitrary real/quaternionic representation dimensions. |
| Fair-bit implementation | Distinct problem; rational projector coordinates and sparse algebraic rows do not establish an exact finite fair-bit compiler. |
| Sign simulation | The constant-label positive embedding preserves only cutpoint signs; its numerical amplitude decays with length. |

Every asymptotic fixes the representation, dimension, signal, command law and allowed error before N grows. Constants, gap estimates and uniform high-dimensional limits are not optimized.
