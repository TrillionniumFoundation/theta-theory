# Round-Thirty-One Proof Dependency Ledger

This ledger records active theorem exports and their permitted direction of use. It separates grand-canonical and conditioned hard-sphere results, separates transition count from holding time, and keeps D1 terminal.

## A chain

| Export | Depends on | Used by |
|---|---|---|
| `A1-BUFFER` common reporting Hilbert level and projective response | labelled affine current geometry | `A1-FCLT`, finite current outputs in C2/D1 |
| `A1-PROJECTION` seam-current two-sided projection decay | product branch weights, incidence bound | `A1-FCLT` |
| `A1-FCLT` continuous Hilbert current limit and trace-norm covariance response on the common level | `A1-BUFFER`, `A1-PROJECTION` | finite current outputs only |
| `A2-ARITH` exact Diophantine arithmetic leaf | finite periodic orbit construction | `A2-FOURIER` |
| `A2-FOURIER` zero-frequency spectral split and integrable noncentral estimate | `A2-ARITH`, Jacobian-weighted stable-curve calculus | `A2-EDGE`, `A3-STOP`, `A4-RENEW` |
| `A2-EDGE` mixed Edgeworth local theorem with four source derivatives | `A2-FOURIER` | `A3-STOP`, `D1-LOCAL` |
| `A3-COUNT` transition-count entropy and exact renewal relation to holding occupation | A2 return kernel | `A3-LDP`, A4 drift/state |
| `A3-TWOSCALE` fast balance plus mesoscopic chronological divergence | `A3-COUNT`, legal connector recovery | `A3-LDP`, C2 path state |
| `A3-STOP` terminal-state/overshoot Markov-renewal local theorem | `A2-EDGE`, enlarged residual-clock operator | conditioned A3 principles, D1 finite stopped outputs |
| `A3-LDP` chronological two-clock Laplace principle | `A3-COUNT`, `A3-TWOSCALE`, recession compactness | A4 history platform, C2 prediction |
| `A4-HARRIS` weighted weak-Harris operator gap | A3 fractional moment and exact history kernel | `A4-FK` |
| `A4-FK` local pressure and certified finite-amplitude bridges | `A4-HARRIS`, bridge irreducibility/contours | C2 rigidity |
| `A4-RENEW` typed suspension resolvent | A3 state/roof moments, A2 Fourier calculus | `A4-COMPRESS`, memory |
| `A4-COMPRESS` resolvent-small compressed generator | stable spectral complement, finite-rank graph map | `A4-MEMORY` |
| `A4-MEMORY` Hilbert-admissible memory kernel and vertical expansion | `A4-COMPRESS`, Hilbert-bounded observation | C2/D1 resolved outputs |

## B chain

| Export | Depends on | Used by |
|---|---|---|
| `B2-KERNEL` disintegrated cut-kernel algebra | hard-sphere cut reference measures | `B2-OVS`, B3 cumulants |
| `B2-PIVOT` constructed tree right inverse and chronological tangent pivots | regular finite collision equations | `B2-LOOP` |
| `B2-LOOP` all-graph simultaneous surplus-contact gain | `B2-PIVOT`, relative-velocity and singular-stratum bounds | `B2-OVS`, pressure |
| `B2-OVS` Ovsyannikov history evolution with `a(t)=a0-Lambda t` | `B2-KERNEL`, creation Cauchy estimate | `B2-GC`, B3 deterministic moments, B4 core |
| `B2-GC` grand-canonical pressure and joint GC LDP | `B2-LOOP`, `B2-OVS`, initial cumulants, local exact recovery | B1 |
| `B1-ANCHOR` regular coarea plus quadratic relative-energy anchor | reserved non-anchor event split, B2 conditional preparation | `B1-EDGE` |
| `B1-EDGE` exact-number mixed Edgeworth coefficient and coarea fibre | `B2-GC`, `B1-ANCHOR` | `B2-MC`, B3 initial Schur data, D1 local input |
| `B2-MC` exact-number/microcanonical contraction | `B2-GC`, `B1-EDGE` | B3, B4, C1 |
| `B3-GRAPH` full normal/cycle contact graph estimate | B2 regular controlled paths | B3 CLT/Mosco, C2 annihilator |
| `B3-MODULUS` deterministic-interval moments and dyadic temporal modulus | B2 pressure derivatives/Ovsyannikov majorant | `B3-CLT` |
| `B3-CLT` joint density/contact Gaussian process | `B3-GRAPH`, `B3-MODULUS`, B1 initial covariance | C2 prediction, D1 Gaussian outputs |
| `B3-MOSCO` full-contact second epi-derivative | `B3-GRAPH`, `B3-CLT` | B4 tangent core, C2 cotangents |
| `B4-COMPACT` ballistic energy path compactness | elastic energy, B2 joint action | `B4-SEMIGROUP`, comparison |
| `B4-SEMIGROUP` shellwise Nisio semigroup/comparison/microscopic limit | `B4-COMPACT`, B2 core, B1 realization saddle | D1 kinetic values |

## Synthesis chain

| Export | Depends on | Used by |
|---|---|---|
| `C1-CHANNEL` normalized stratum-selection observation kernel | independent sensor channels | C1 filter/statistics |
| `C1-JETS` projective cylindrical hidden/filter derivatives | `C1-CHANNEL`, A/B hidden maps | C1 observability/LAN |
| `C1-OBS` induced-law observable-quotient Riccati stability | `C1-JETS`, diagnostic window Gramian | `C1-LAN`, C2 filter stability |
| `C1-LAN` adaptive LAN/BvM under induced-law identification | `C1-OBS` | C2 likelihoods, D1 beliefs |
| `C2-STRICT` weighted mixed-strict dual on arbitrary Polish states | Polish platform only | C2 rigidity/prediction |
| `C2-ADJOINT` full contact annihilator | `B3-GRAPH` | cotangent representation |
| `C2-RIGID` certified bridge pressure-to-Livsic theorem | `A4-FK`, `C2-STRICT` | rigidity outputs |
| `C2-PRED` parameter-specific likelihood and stable optional projections | `C1-OBS`, A3/B3 path limits | channel-specific BSDEs |
| `D1-LOCAL` lattice fibre/cell phase coefficients | `A2-EDGE` or `B1-EDGE` | `D1-POLICY` |
| `D1-POLICY` finite-memory approximation and policy-uniform expansion | `D1-LOCAL`, C1 beliefs | `D1-EPI` |
| `D1-EPI` positive-support common-policy lexicographic selection | `D1-POLICY`, B4 shellwise values | final synthesis only |

## Acyclicity and interface assertions

1. `B2-GC -> B1-EDGE -> B2-MC` is the only conditioning chain; B2-GC never imports B1.
2. B2 pivot construction and local recovery use only finite collision geometry; they do not import B3's later graph inverse.
3. B3 uses B2 deterministic-interval source derivatives; B2 does not use B3 process or Mosco results.
4. B4 contracts the established joint B2/B3 theory and never feeds back into B2 or B1.
5. A3 entropy is integrated against the transition marginal `nu`; holding occupation `L` is derived through the renewal relation and is not used as the KL clock.
6. C1 observation randomness comes from the explicit stratum-selection/channel law, not from D1 or an aggregate local theorem.
7. C2 likelihoods use parameter-specific filters and import only certified A4 pressure bridges.
8. D1 imports exactly the finite-dimensional four-derivative Edgeworth exports in A2/B1 and is terminal.
