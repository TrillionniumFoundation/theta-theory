# Theorem dependency graph

Identifiers below are stable LaTeX labels; final numbered statements are in BUILD_RECEIPT.json.

```mermaid
graph TD
  Raw[Prepared kernels and executable audit] --> Ref[Actual reference and all-strategy effort]
  Raw --> Bal[Common unnormalized task balance]
  Raw --> Quot[Borel predictive quotient conditions]
  Ref --> Lower[lem:lower — acquired count domination]
  Bal --> Upper[lem:upper — conditional-hazard implementation]
  Stop[def:stopping] --> Pack[lem:packing]
  Ports[prop:physical] --> Pack
  Lower --> Main[thm:main — three resource interfaces]
  Upper --> Main
  Pack --> Main
  Moment[prop:approx-moments] --> Approx[thm:approx — fixed-budget defect transfer]
  Lower --> Approx
  Approx --> Sharp[prop:sharp-approx]
  Main --> Geometry[prop:geometry and prop:atom]
  Raw --> Classical[thm:classical]
  Raw --> Quantum[thm:quantum]
  Classical --> Validation[Raw verification of Main and Approx]
  Quantum --> Validation
  Sensor[Raw nonintervening Gaussian sensor] --> Direction[thm:directional]
  Lower --> Direction
  Sphere[Actual audit-support covering] --> Direction
  Pack --> Simulation[prop:role-composition]
  Main --> Joint[thm:joint]
  Simulation --> Costs[Complete-law error and physical cost]
  Effective[Partitions, integration, precision and evaluation certificates] --> Finite[prop:finite]
```

No realization is a premise in the proof of thm:main. The arrows from classical/quantum are verification arrows. The directional result does not assume exact balance and is proved independently using the acquired-count converse plus a uniform radial upper.
