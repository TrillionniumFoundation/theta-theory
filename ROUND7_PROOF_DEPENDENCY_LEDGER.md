# Round-seven proof dependency ledger

## Independent benchmark

```text
A1
```

A1 uses only its explicit affine symplectic construction and anisotropic transfer estimate.

## Sinai chain

```text
A2 physical quotient / Dolgopyat / LLT
  -> A3 canonical excursion compactification and full LDP
  -> A4 coarse-history conditional homogenization and memory
  -> C2 optional projections and Doob-memory response
  -> D1 stratified projective synthesis
```

A3 uses A2 only after the physical quotient and five-word certificate are established. A4 conditions on a stable-leaf quotient and uses A2/A3 estimates; it never uses C2. C2 uses the completed A4 coarse kernel. D1 is downstream.

## Hard-sphere chain

```text
B2-GC frame-reset / measure-trace pressure / GC LDP
  -> B1 sectorwise mixed shell coefficient
  -> B2-MC conditional joint LDP
  -> B3 exact tangent action and Gaussian process
  -> B4 nonlinear kinetic semigroup
  -> C1 belief game and statistics
  -> C2 hard-sphere cotangents
  -> D1 stratified projective synthesis
```

B2-GC does not use B1, B3, or B4. B1 uses the B2-GC bounded-source pressure. B2-MC uses B1 only for the shell ratio. B3 uses B1/B2 for the initial covariance and dynamic pressure, then independently proves the tangent closed-range theorem. B4 uses the already completed B2 lower recovery and B3 covariance. C1 uses B2-B4 only after those interfaces are closed. C2 and D1 are downstream.

## Cross-platform nodes

C2 is a coproduct theorem: its Sinai component depends on A4, while its hard-sphere component depends on B2/B3. It does not identify physical state spaces across platforms.

D1 depends on already proved finite projection pressures, coefficient theorems, and exponential tightness. It does not feed any theorem back into A2-A4 or B1-B4.

## Machine-readable DAG

```yaml
A1: []
A2: []
A3: [A2]
A4: [A2, A3]
B2-GC: []
B1: [B2-GC]
B2-MC: [B1]
B3: [B2-MC]
B4: [B3]
C1: [B4]
C2: [A4, B3]
D1: [A3, A4, B2-MC, B3, B4, C1, C2]
```

The round-seven verifier rejects any cycle or unknown dependency.
