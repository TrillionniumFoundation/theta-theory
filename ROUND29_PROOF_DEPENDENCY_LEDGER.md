# Round-Twenty-Nine Proof Dependency Ledger

This ledger records theorem-level exports and the direction in which they are used. It separates grand-canonical and conditioned hard-sphere statements and keeps D1 terminal.

## A chain

| Export | Depends on | Used by |
|---|---|---|
| `A1-LIPCC` loss-indexed response and seam-current membership | affine baker geometry | A1-FCLT, C2 current pairing |
| `A1-FCLT` continuous Hilbert FCLT and trace-norm covariance response | A1-LIPCC, martingale projections | C2/D1 finite current outputs |
| `A2-JWFG` finite weighted grammar and arithmetic certificate | dispersing billiard chart data | A2-FOURIER |
| `A2-FOURIER` all-frequency anisotropic estimate | A2-JWFG | A2-LLT, A3-STOP, A4-RENEW |
| `A2-LLT` mixed source-uniform local theorem | A2-FOURIER | A3 stopping, D1 finite observables |
| `A3-TCTCC` exact discrete balance and two-clock compact state | A2 return kernel | A3-LDP, A4 drift/state |
| `A3-DRIFT` fractional conditional moment and power drift | A2 weighted return tail | A4-HARRIS/FK |
| `A3-LDP` chronological path Laplace principle | A3-TCTCC, legal reference recovery | A4 history platform, C2 path state |
| `A3-STOP` Gaussian--overshoot local theorem | A2-LLT, typed renewal kernel | conditioned A3 principles, D1 |
| `A4-HARRIS` weighted operator gap | A3-DRIFT, history coupling | A4-FK, A4-RENEW |
| `A4-FK` local analytic pressure charts | A4-HARRIS | C2 exposing rays |
| `A4-RENEW` typed suspension resolvent | A2 Fourier/roof bounds, A4-FK | A4-MEMORY |
| `A4-MEMORY` graph compression and vertical-line kernel expansion | A4-HARRIS, explicit coupling domains | C2/D1 resolved outputs |

## B chain

| Export | Depends on | Used by |
|---|---|---|
| `B2-DKC` disintegrated cut-kernel algebra | hard-sphere cut reference measures | B2-DUHAMEL, B3 revealment, B4 core |
| `B2-CPP` constraint-preserving loop pivots and coarea gain | finite collision-map derivatives | B2-DUHAMEL/pressure |
| `B2-GC` grand-canonical pressure and joint GC LDP | B2-DKC, B2-CPP, initial cumulant input, local recovery | B1 |
| `B1-UCAF` all-component Fourier smoothing | B2 GC conditional density, finite coarea anchors | B1-LOCAL |
| `B1-LOCAL` exact-number mixed local coefficient and coarea fibre | B2-GC, B1-UCAF | B2-MC, B3 initial covariance, D1 |
| `B2-MC` exact-number/microcanonical contraction | B2-GC, B1-LOCAL | B3, B4, C1 |
| `B3-OCCNS` full contact normal/cycle graph | B2 regular path class | B3-CLT, B3-MOSCO |
| `B3-REVEAL` stopped cluster bracket/cumulants | B2-DKC/Duhamel factorial tails | B3-CLT |
| `B3-CLT` joint density/contact Gaussian process | B3-OCCNS, B3-REVEAL, B1 initial Schur data | C2 prediction, D1 Gaussian outputs |
| `B3-MOSCO` full-contact second epi-derivative | B3-OCCNS, B3-CLT | B4 tangent core, C2 cotangents |
| `B4-PRAF` joint/density action and preparation-running factorization | B2-MC, B3 contact contraction | B4-SEMIGROUP |
| `B4-ENERGY` energy/entropy path compactness | Gaussian preparation, elastic energy, B2 action | B4 comparison/limit |
| `B4-SEMIGROUP` Nisio comparison and microscopic limit | B4-PRAF, B4-ENERGY, B2 core, B1 realization saddle | D1 kinetic values |

## Synthesis chain

| Export | Depends on | Used by |
|---|---|---|
| `C1-SEDBJ` exact observation envelope and distributional filter jets | A/B hidden signal maps | C1-LAN |
| `C1-LAN` pointwise adaptive information and BvM | C1-SEDBJ | C2 prediction/likelihood, D1 beliefs |
| `C2-STRICT` weighted mixed-strict dual on arbitrary Polish spaces | Polish platform only | C2 rigidity/prediction |
| `C2-ADJOINT` full-contact annihilator | B3-OCCNS | cotangent representation |
| `C2-RIGID` finite-amplitude pressure-to-Livsic theorem | A4-FK, C2-STRICT | rigidity outputs |
| `C2-PRED` fixed stopped-path optional projections and channel likelihoods | C1-LAN, A3/B3 process limits | innovation and BSDE outputs |
| `D1-LOCAL` finite-dimensional mixed phase coefficient | A2-LLT or B1-LOCAL | D1-CONTROL |
| `D1-CONTROL` positive-support epi-argmax common control | D1-LOCAL, C1 beliefs, B4 semigroup | final synthesis only |

## Acyclicity assertions

1. `B2-GC -> B1-LOCAL -> B2-MC` is the only conditioning chain; `B2-GC` never imports B1.
2. B2 recovery uses local finite collision frames and does not import the later B3 graph inverse.
3. B3 uses B2 histories; B2 does not use B3 process or Mosco results.
4. B4 contracts the already established B2/B3 joint theory; its dynamic semigroup is not used to prove B2.
5. C1 observation density comes from an independent sensor channel, not from D1 or a downstream local theorem.
6. D1 is terminal: no upstream theorem imports phase or policy asymptotics.
