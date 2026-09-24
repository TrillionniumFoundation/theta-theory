# Resource ledger — revision 31

| Result | Inputs and storage convention | Exact count or bound |
|---|---|---|
| Canonical affine slices | Complete finite clocked causal array; all persistent buffers included; atomic rows | r_t simultaneously when every canonical slice is a simplex; always when each r_t<=2 |
| Two-cut incompatibility | One atomic 4-valued x, one atomic 5-valued command, then one binary query; only final answer emitted | Feasible region is upward closure of (3,4),(4,3); terminal answer has 2 states; peak 4 |
| Full support | Same experiment for 9/10<=h<1; all input triples specified | At h=9/10 every conditional answer probability lies in [1/20,19/20] |
| Additive encoder | Product input alphabet, fixed declared order, fresh random draws | Same m labels at every acquisition cut; no retained summand selector |
| Arbitrary simplex query encoder | Known eta and decoder vertices, one query after acquisition | K_n=n+1 iff W_n^fo=W_n^ad=n+1; peak statement, not t+1 prefix optimality |
| Critical non-Hadamard examples | Classical rational 5D and 9D decoder simplices, exact atomic rows | 6 and 10 labels, respectively; sharp eta=1/5 and eta=1/9 |
| Rational sampler | T self-paced stages; m old labels; input alphabet d; row denominators<=D | <=2(T+1)md*2^ceil(log2 D) states, including phase/current input/prefix; expected <2 ceil(log2 D) fair bits per stage |
| Stochastic-language comparison | Generated input symbols, generated query, stopping; proper normalized states | Inherited lower 2^n residual states vs upper (n+1)(n+2)/2+n(n+1)+1 arbitrary positive states |

Fixed-order acquisition uses a known time index, not a free data-dependent schedule. Adaptive acquisition is covered only through the stated checkpoint lower bound and a matching fixed-order upper construction. The two-cut example does not optimize collision-validation order. Codebook construction time and general program length are not included in primary label counts. The rational critical families have explicit finite matrices and sampling formulas; this is separate from efficient construction of the old fixed-signal exponential codebook. Known exact rows and acquired calibration are not interchangeable.
