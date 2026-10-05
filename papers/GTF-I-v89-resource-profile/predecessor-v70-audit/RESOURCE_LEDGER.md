# Resource ledger — Revision 70

| Interface | Charged object | Public/fixed data and separate costs |
|---|---|---|
| Tensor-family covering | One reusable codeword: unitary chart headers/digits and preparation pivot/body | d,n,m,r,N,delta fixed/public; exact encoder workspace and search time separate |
| Direct qubit codec | At most ceil log2[4(2B_U+1)^3] plus inherited preparation fixed-length bits | JSON schema text is transport metadata, not the fixed-length packed body; no hidden real constants |
| General unitary atlas | d^2-1 signed grid digits plus fixed-dimension chart headers | Exhaustive exact rational search is finite, not claimed polynomial in input length |
| Expanded decoder | Full rational U, factors and Choi matrices | Denominators, arbitrary-precision integers and all expanded entries occupy workspace; not identified with payload |
| Preparation retraction | Exact partial-trace arithmetic on a supplied legal centre | May increase ranks; no claim to an optimal compressed representation of the centre |
| Physical operation | The decoded mathematical quantum instrument | No finite-classical-message physical implementation on unknown entangled inputs is provided |
| Learning | No learning interface used | Encoder has supplied matrix parameters; no query/sample complexity claim |

N and delta ranges of the coding theorem are N>=1 and 0<delta<=1/32. Retraction alone is valid at every positive covering radius. The fixed-dimension constants are not uniform as dimensions grow; the inherited general interior theorem also retains its positive margin. Ordinary hidden-label widths and old uniform bit-space theorems remain separate resources.
