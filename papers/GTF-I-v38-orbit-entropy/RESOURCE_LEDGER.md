# Resource ledger — v38

The main resource is the maximum cardinality of available persistent labels in a horizon-specific probabilistic ordered read-once transducer. State alphabets and rows may vary by epoch. Unreachable labels count if available; normalized arbitrary unused rows are harmless. A retained final binary output needs two labels.

| Item | Accounting |
|---|---|
| Current command | An atomic external symbol; only updated label survives it. |
| Seed, previous inputs, past random coins, data-dependent schedule | Must be retained inside the charged label or discarded. |
| Epoch, horizon, row table, table construction and lookup | Free nonuniform program advice, not claimed uniform space. |
| Exact stochastic row | Atomic; no exact finite fair-bit compiler for irrational data is asserted. |
| Projective machine | Fixed q, `O_q(N^(q-1))` labels; at most q² successors per row; common command rows and an N-dependent terminal decoder. A matrix is a read-only description of a state label, not a runtime register. |
| Six-gate machine | `<150 N` labels, rational rows with at most four successors, known horizon and common command matrices. |
| Quantum realization | One q-dimensional register, fixed seed reset channels, prescribed unitary commands, one selected two-outcome query. |
| Quantum/classical units | Dimension q versus `(q-1) log2 N+O(1)` classical label bits at fixed calibrated error; not linear classical bits or program description. |
| Conditional centroids and Gaussian smoothing | Proof-only quantities, unavailable as free runtime state or oracle. |
| Padded fair-bit implementation | Inherited separately as an approximate compiler with additional control labels and free threshold tables. Fixed duration eliminates the specified coin-dependent timing channel only. |

The numerical gap certificate belongs to the six V-gates only. General-q alphabets have a qualitative full group gap, and the old five-gate constant remains non-evaluated. A full group gap is different from a pure-state quotient gap or a gap in one finite representation.
