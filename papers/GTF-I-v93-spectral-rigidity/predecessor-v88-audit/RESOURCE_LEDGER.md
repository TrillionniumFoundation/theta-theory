# Resource ledger — v88

| Resource | Exact convention |
|---|---|
| Unknown-device calls | At most N on every record; each adaptive block reserves n(h) positive calls; padding remains charged |
| Coherent reset width | n(h)<=b; the complete fresh probe-reference state is conditionally product with all old receiver memory |
| Within-block control | Arbitrary common quantum adaptive controls and references, including bounded internal stopping |
| Between-block feedback | Arbitrary classical history; fresh states depend on that history through a common rule |
| Receiver quantum memory | Arbitrary dimension and common joint receiver instruments; cannot be fed coherently into later acquisition |
| Policy quadratic cost | Q=max_complete_paths sum n(h)²<=bN, not an expectation under either hypothesis |
| Final processing | Arbitrary joint channel or measurement of all accessible stored systems and classical history |
| Lower construction | Parallel encoded GHZ blocks or fixed product witnesses, no remainder-dependent advice |
| Reference size in lower | At most 2d per device call; total reference for a block grows with its width |
| Controls and public parameters | Fixed-pair E,H,Lambda,N,b,s; known-direction ideal encoding/recovery is not common-learning advice |
| Local constants | Fixed E,H,Lambda dependent, uniform N,b,F; not uniform through support/gap degenerations |
| Nonempty certificate | One sufficient normalized realization and a legality interval s_*, not a minimum allowance or discrimination interval |
| Exact policy arithmetic | Complete finite graph, max-call and square-cost bounds, conditional fidelity/trace-square consequences |
| Unverified policy premises | Physical fresh-state independence and supplied nodewise fidelity majorant are not verified by arithmetic |
| Learning and bits | Retained balanced-interior fixed-k law and public fixed-length dictionary; growing-k upper/lower not matched |
| Computational complexity | Existing represented-input covariance/support/tangent/repair routines remain polynomial in their stated inputs; no general efficient dictionary or recovery synthesis follows |
| Physical execution | Finite exact model replays only; no hardware reset, general optimal learner, or recovery circuit execution claimed |

The old independent width b=N is the parallel channel class. The new reset width b=N is exactly the adaptive class. Parallel and adaptive have comparable local orders in the fixed tube; their exact distances and fixed-pair exponents are not equated. At b=1 the reset class still has receiver quantum memory and classical feedback, so it is not declared identical to the old independent-product class.
