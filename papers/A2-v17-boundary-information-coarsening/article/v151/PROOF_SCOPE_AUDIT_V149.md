# Proof-scope audit for revision 149

This is the author's revision audit, not an independent referee report or a formal verification certificate.

| Potential failure | Hypothesis or proof step used | What is not asserted |
|---|---|---|
| Fibrewise gcd does not lift to a nilpotent parameter ring | Universal gcd is an isomorphism onto a **locally closed scheme**; the dual-number counterexample is written explicitly | Geometric-point membership alone does not define a family in the stratum |
| A radical loses multiplicity | The common divisor of the actual first-relation space is recovered; for pencils it is exactly `det^(n-1)` | The reduced determinant cone by itself does not recover a pencil |
| A residual coefficient has another common factor | Right-invariance forces any common divisor onto the determinant boundary; the partition has length n-1 and a rank-(n-1) coefficient is nonzero | An arbitrary residual space need not be a Schur coefficient space |
| Reduced-point stabilizers are mistaken for all-base isomorphism sheaves | The determinant orbit, gcd inverse, Cauchy subbundles and Pluecker closed immersion are used as scheme morphisms | The new family theorem is not obtained by reusing a fibrewise reduced-base argument |
| Local algebras can deform outside homogeneous presentations | Normalized trace must be multiplicative; its kernel has nilpotence D+1 and maximal lower graded ranks | Arbitrary finite-flat smoothings are not in this Hilbert stratum |
| Ungraded automorphisms add inertia | The tangent-identity substitution group is computed and retained before taking an effective quotient | The full algebra stack is not the pencil quotient |
| The source GL factor contributes further ineffective automorphisms | Exact `1 -> GL(U) -> G° -> PGL(V) -> 1`; morphism quotient followed by fppf stackification | No global splitting of the group extension is assumed |
| Ambient parameter deformations are conflated with proper reductions | The all-base moduli theorem permits parameter-dependent coordinate changes; the inherited moving theorem uses a proper intrinsic reduction | The new theorem does not weaken actual source recovery or the one-constant-left-map conclusion |
| A normal-space formula assumes an unavailable tangent splitting | Take the quotient of the projective tangent by the Pluecker tangent; only End(F)=C id + sl(F) is split | No canonical splitting of the Pluecker tangent sequence is claimed |
| Gcd-free does not imply absence of codimension-two base loci on GL | The fixed-support theorem separately chooses B avoiding the projective closure of the evaluation image | The whole gcd-free Grassmannian is not claimed to have determinant radical |
| A pencil moduli stack is not proper | Only the framed Grassmannian and the constructed Sigma_B families are projective | No properness or new compactification claim for `[Gr/PGL]` |
| New proofs cannot certify historical originality | Full Ballico 1993 comparison remains explicitly unresolved | No nonanticipation or first-ever claim |

## New proof dependencies

`universal-gcd` uses unique factorization, the differential calculation, and the proper/unramified/universally-injective closed-immersion criterion. `determinant-stratum` adds the determinant stabilizer and homogeneous-space descent. `relative-first-relation` adds a direct filtration and trace calculation. `primitive-pencil` uses the already proved exterior representation and its determinant twist. `pencil-stack-equivalence` uses those four blocks, Cauchy contraction, the Pluecker immersion, and the displayed ineffective-group exact sequence. `transverse-pencil-directions` uses Grassmannian tangent spaces and the Pluecker tangent calculation. `fixed-support-grassmannians` uses projective incidence avoidance and a fixed basepoint-free subsystem.

No spectral classification, covering-map example, applications theorem, or historical archive result is an input to any of these new proofs. The existing determinant-preserver proof is used where explicitly referenced. All other previously established reconstruction results remain in the principal paper with their proofs.
