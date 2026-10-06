# Author-side proof and implementation audit — Revision 72

This document reports explicit derivations and adversarial checks, not an independent referee endorsement. The controlling reports are v71/r46; they reviewed the v71 full-error/fixed-readout chains and independently inspected the v70 tensor-coherent predecessor. All remain available and are not reclassified as new v72 results.

## 1. Observable readout: premises and metric

The family emits (x,y), or x is recoverable by fixed orthogonal output projections. Every x-row has one normalization. The flag dimension is d^2-d, not d^2-1: all column phases disappear but label permutations do not. Outcomes remain labelled in both the target and centre interface.

The one-use measurement norm is comparable to the tuple Frobenius norm q of projection differences. A single event gives twice its operator-norm difference; a rank-one projector difference has Frobenius norm sqrt(2) times operator norm. Reference upper bounds use blockwise trace duality, not scalar-input reasoning.

The full N-use measurement distance is imported from Puchala et al., Corollary 1 and Theorem 2. The already-perfect one-use case is separated before inverting sine. Public stopping is embedded in a fixed N-slot network with irrelevant discarded calls. A plateau of 2/pi in the conservative local lower modulus exceeds twice every allowed radius delta<=1/32. This is not extrapolated to the whole unhalved interval below two.

## 2. Product packing and absence of parameter cancellation

The basis packing has scale delta/N. If two product points have different bases, discarding all conditional quantum outputs and y leaves a measurement witness independent of their rows. If their bases agree and rows differ, a known eigenvector input extracts the differing row and the inherited product-state test separates it at scale delta/sqrt(N). These two cases justify the Cartesian product packing. One does not require a single input to distinguish every pair, nor add two tangent dimensions in the presence of cancellation. Arbitrary legal memoryless centres enter only through the metric triangle inequality.

For unflagged equal rows, summing x gives tr(X)sigma_y identically. The exact cancellation is an implementation negative control and states why observability is a hypothesis. Orthogonal-output recovery is a fixed output postprocessing, not a common input retraction for all varying bases.

## 3. Rational chart audit

The chart begins with nonzero unnormalized columns P_x e_k. They are orthogonal and span an invertible matrix. Standard partial row pivoting gives Pi A=L R, with unit lower triangular L and all subdiagonal multiplier moduli at most one; previous L entries are swapped along with row pivots. Right upper triangular multiplication preserves each leading span. Hence unnormalized Gram--Schmidt on Pi^{-1}L recovers the ordered projectors exactly, even when a normalized eigenvector has irrational coordinates.

The full rectangular coordinate cube permits modulus sqrt(2), so the perturbation proof uses the conservative norm 2d, not the smaller bound for pivoted target multipliers. Since det L=1, sigma_min(L)>= (2d)^(-(d-1)); each leading column block has at least that singular-value bound. Projection differences follow from (I-E')E=(I-E')(Z-Z')Z^dagger and its adjoint analogue. Every valid rounded chart is invertible, and every decoder image is an exactly legal rational flag. No numerical eigensolver, minimum eigenvalue or finite search cap is a theorem premise.

The permutation uses ceil(log2 d!) bits and the d(d-1) real grid digits are charged. Coordinatewise binary padding adds only a fixed-dimensional constant. Rational adjugates yield expanded bit lengths O_d(log B), independently of the conditioning of the supplied input. The encoder's input-processing space remains a different resource from its output payload.

## 4. Conditional rows, Choi transpose and validation

Row factor encoders remain unchanged. Their actual pivot masks, anchors and signs are counted, and their errors combine through one copy of each row programme per slot. This is a proof simulation, not a hardware-resource accounting theorem. Conditional zero blocks and ranks survive the factor code and multiplication by a rank-one input projector.

Input-first Choi blocks use transpose(P_x) tensor sigma_xy. The complex +i test gives probability one with this convention and zero after the wrong transpose. Each decoded row is normalized; the flag resolves identity, so joint partial trace is identity. The expanded common denominator is obtained exactly, not counted as the compressed payload.

The decoder rejects invalid metadata, permutations, body lengths, boolean integers, noncanonical fraction certificates and incompatible row headers. Target verification compares the entire canonical encoding against a rerun. A different but legal chart digit need not fail bare decoding; it must fail canonical target replay when it is not the target's canonical codeword. A certificate never establishes unknown-target accuracy by itself.

## 5. Uniform seizing and arbitrary centres

The ambient-domain condition B(A(omega))=omega is assumed for every state of the whole fixed programme algebra, not just the target stratum or a selected pair. Otherwise B(K) might leave the domain on which the claimed retraction is idempotent. The one-use superchannel first holds the outer input, then consumes a fresh K call in B, and finally applies A. This is compatible with reference memory, stopping and the N-call budget.

Common programme processing proves the product-state upper bound; repeated seizing proves equality. State centres map through A and arbitrary instrument centres map through B, so the covering cardinalities agree at exactly the same radius. This centre-class argument is stated as a consequence of established environment-state equivalence, not as a new seizing principle.

The standard Pauli/Bell pair satisfies the hypotheses over the full probability simplex. A unitary with four equally weighted Pauli components has Choi rank one but retracts to rank four. This prevents conflating arbitrary-centre retraction with the zero-preserving rank-aware target encoder. Full error delta<=delta_*<2 comes from the inherited state theorem; it does not establish a large-error coherent readout exponent.

## 6. Evidence and remaining scope

The new exact suite exercises direct and rounded charts through dimension five, rational rank-one projectors without rational normalized lifts, qubit/qutrit codecs, tiny positive eigenvalues, Choi action, pure-programme tensor estimates, adaptive classical policies, two-shot projective measurement discrimination, observable output embedding, Pauli seizing and maliciously altered certificates. All earlier suites remain unchanged. Counts in this document are deliberately delegated to the actual build receipt.

The mathematical proofs quantify over continuum families and all admissible quantum testers; finite regression does not certify those quantifiers. Hosted reconstruction attests sources and rendered artifacts, not independent priority, author identity, a journal decision or the separate A/B/C/D programme. General nonrecoverable readout, coupled coherent/support-changing geometry, dimension-uniform constants and a full-error coherent law remain distinct mathematical questions.
