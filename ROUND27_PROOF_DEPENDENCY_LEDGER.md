# Round-Twenty-Seven Proof Dependency Ledger

**Purpose.** This ledger names theorem-level exports, not paper titles alone.  It is acyclic because the hard-sphere grand-canonical and microcanonical nodes are separated.

## A-chain

| Node | Active export | Depends on | Used by |
|---|---|---|---|
| A1-CURRENT | projective response, geometric current domain, trace-class FCLT | exact baker benchmark | C2 current duality |
| A2-FOURIER | certified anisotropic all-frequency estimate | finite billiard certificate | A2-LLT |
| A2-LLT | source-uniform mixed local theorem | A2-FOURIER | A3-STOP, A4-RENEW, C1 signal design, D1 local charts |
| A3-STATE | Polish chronological graph-current state and compactness | A2 branch moment | A3-LDP |
| A3-LDP | ordered collision/physical-clock Laplace principle | A3-STATE, reference recovery, connector lower bound | A4 history platform, C2 contractions |
| A3-STOP | random-stop joint local density and coarea conditioning | A2-LLT, A3-STATE | conditioned A3 LDP, D1 |
| A4-HARRIS | weighted weak-Harris operator gap | A3 exact kernel and Lyapunov function | A4-FK, A4-RENEW |
| A4-FK | fixed-space analytic pressure/Doob family | A4-HARRIS | C2 exposing rays |
| A4-RENEW | typed flow/history renewal | A2-LLT, A4-FK | A4-MEMORY, C2 |
| A4-MEMORY | stable compressed semigroup and domain-safe Schur--Feshbach kernel | A4-HARRIS plus finite-rank angle/coupling certificate | C2 form transport, D1 memory outputs |

## B-chain

| Node | Active export | Depends on | Used by |
|---|---|---|---|
| B2-GEOM | relative-velocity bound and causal triangular loop rank | regular preparation | B2-HIER |
| B2-HIER | associative cut-history algebra and factorial Duhamel propagation | B2-GEOM | B2-GC, B3-CUT, B4-CORE |
| B2-GC | analytic grand-canonical pressure and GC LDP | B2-HIER, positive collision-simplex recovery | B1 |
| B1-LOCAL | source-uniform exact-number/mixed local coefficient and coarea fibre | B2-GC | B2-MC, B3 initial Schur data, D1 |
| B2-MC | exact-number/microcanonical dynamic LDP | B2-GC, B1-LOCAL | B3, B4, C1 |
| B3-GRAPH | quotient collision-defect closed range | B2 regular path class | B3-CLT, B3-MOSCO |
| B3-CUT | conditional cut density/cumulants | B2-HIER | B3-CLT |
| B3-CLT | nuclear kinetic fluctuation process | B3-GRAPH, B3-CUT, B1-LOCAL | C2 optional projections, D1 Gaussian outputs |
| B3-MOSCO | quotient second epi-derivative | B3-GRAPH, B3-CLT | B4 recovery core, C2 cotangent form |
| B4-ACTION | attainable lsc entropy rate and exponential/Povzner containment | B2-GC, B2-MC | B4-SEMIGROUP |
| B4-SEMIGROUP | Nisio comparison and microscopic semigroup limit | B4-ACTION, B2-HIER, B1-LOCAL | D1 leading kinetic value |

## Synthesis chain

| Node | Active export | Depends on | Used by |
|---|---|---|---|
| C1-CHANNEL | consistent deterministic-signal plus independent-noise observation kernel | A/B signal maps | C1-FILTER |
| C1-FILTER | Feller belief kernel, derivative filter, adaptive LAN/BvM | C1-CHANNEL | C2 prediction, D1 phase posterior |
| C2-DUAL | weighted mixed strict dual on Polish states | A3/B4 compact containment | C2-RIGID, C2-PRED |
| C2-ADJOINT | complete kinetic annihilator with initial boundary source | B3-GRAPH | C2 cotangent representation |
| C2-RIGID | pressure-to-periodic-to-Livsic theorem | A4-FK, C2-DUAL | rigidity outputs |
| C2-PRED | path-augmented optional projection/bracket convergence | C1-FILTER, A3/B3 process limits | innovation/BSDE outputs |
| D1-LOCAL | full joint Morse--Bott phase coefficient | A2-LLT or B1-LOCAL | D1-CONTROL |
| D1-CONTROL | uniform finite-scale and subleading shared-policy theorem | C1-FILTER, D1-LOCAL, B4-SEMIGROUP | final synthesis |

## Non-circularity checks

1. `B2-GC -> B1-LOCAL -> B2-MC` is a directed sequence; B2-GC never imports B1.
2. B2's positive collision-simplex correction is finite-dimensional and does not import the later B3 graph inverse.
3. B4 uses B3 only for tangent/strong-core recovery after the B2 microscopic LDP is already established.
4. C1 observation density comes from independent noise, not from D1 or from a downstream filtering theorem.
5. D1 is terminal: no upstream root theorem imports a D1 phase or policy result.
