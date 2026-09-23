# Resource ledger

All widths count retained labels, not arbitrary-precision real registers. Fresh random bits are independent; any seed carried across cuts belongs to the state. Time-dependent transition descriptions are read-only and cannot depend on the unknown candidate. A free schedule clock is not an autonomous finite-state implementation.

| Construction | Training preparations | Decision labels | Whole-schedule labels | Other charged resources |
|---|---:|---:|---:|---|
| General finite cover, Theorem 7.2 | N = 2LR(K−1) | K | at most 12Kd | r+2 fair bits per comparison observation; r event-selection bits; O(K²d(r+3)+log L+log R+log K) read-only bits |
| Physical 399-sample selector, retained | 399 (optionally one ignored slot) | 3 | at most 40,602 | acquisition clock; deterministic tables |
| Physical block selector, Theorem 22.1 | 4LR; concrete 12,800·2^400 | 3 | at most 12 | L=400, R=8·2^400; enormous external schedule, no training randomizer |
| Independent confidence lift, Theorem 23.1 | J copies of n+2 total trials | task-dependent | W(2J+1) | retained signed-score accumulator; J≥8γ^−2 log(1/α) |
| One training phase, repeated validation, Theorem 23.2 | 4LR+2m total trials | 3 witness labels | 12(2m+1) | retained witness and validation sum |
| Point-source family, Theorem 9.2 | 1 | d | at most 2d | 2 validation observations; deterministic |
| Overlapping labels, Theorem 9.3 | specified reveal schedule | full profile | exact D_t at each cut | no external output tape; error lower bound (1−ε)D_t |

The general comparison theorem uses L=ceil(log(2/δ)/(4θ)) and R=ceil(2^L log(2/δ)). Larger L and R satisfying the same two error inequalities are allowed. Its score loss is at most 2^(1−r)+2ρ+4(K−1)θ+2(K−1)δ. Training-source perturbation adds 2 min(1,Nα); validation perturbations add β_c+β_t. A zero training multiplier is available only when α=0.

For the general machine T≤N(r+3)+r+4 is a coarse bound on the number of epochs. Adding an autonomous clock gives at most 12Kd(T+1) states. Input alphabet symbols are atomic in that general definition; finer input acquisition is priced by Proposition 6.3. The physical twelve-state bound already includes bit-by-bit acquisition and validation, not merely atomic completed trials.

The profile value V_(N,K) fixes N and every charged cut. The asymptotic strict-threshold quantity W_c takes the infimum over finite N. These are different optimizations. The theorem κ≤W≤12dκ does not claim a small N or an optimal fixed-N memory frontier.
