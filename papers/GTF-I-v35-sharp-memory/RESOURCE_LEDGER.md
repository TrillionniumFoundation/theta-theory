# Resource ledger — Revision 35

| Item | Convention |
|---|---|
| Main input | Four seed symbols, N ordinary binary commands, one of two coordinate queries |
| Width | Maximum available persistent label count; padding counts; positive-mass states used only under a fixed test law |
| Transition | Arbitrary row-stochastic matrix, allowed to vary by cut and horizon |
| Free description | External epoch, horizon-specific design, complete read-only row tables and arithmetic |
| Randomness | Fresh atomic samples from specified rows; no retained seed or random tape outside the register |
| Packet | 2k-1 actual command slots, uniform J chosen externally; J is not a free machine input |
| Packet independence | Different packets independent of the past; bits within a packet deliberately correlated |
| Packet endpoint | At most k positive-mass states; no bound needed on internal or earlier packet registers |
| Error | Worst binary row-TV error over every seed, complete word and final query |
| Robust range | Main theorem: fixed epsilon<1/20 at fixed signal 1/10 |
| Upper construction | Exact real atomic rows, common command matrices, N-dependent decoder |
| Compact extension | All SO(d) matrices are exact atomic external inputs; Borel row lookup; not a binary-alphabet implementation |
| Compact error | Fixed d and epsilon<1/(20 sqrt(d)) |
| Final output | One selected answer, not two jointly independent coordinate answers |
| State/bit comparison | ceil(log2 width) label bits only; neither description length nor uniform computational space |
| Fair-bit compiler | Inherited rational-row, self-paced construction has extra workspace; not an implementation preserving the atomic optimum |
| Deficiency | Actual terminal optimum defined separately from an additive local certificate; cancellation not ruled out |

The compact group theorem and the fixed binary rotation theorem have different command alphabets. The matched exponent does not assert exact finite counts or optimized constants. No uncharged output history, command-count register or protocol distinction is used in the lower or upper construction.
