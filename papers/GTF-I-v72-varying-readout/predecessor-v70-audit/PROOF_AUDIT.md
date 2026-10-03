# Written-proof audit — Revision 70

## Preparation centre retraction

For a memoryless centre C, fresh maximally mixed inputs produce independent states C_y(I/d). This supplies one common lower tester against a preparation target. The inherited exact product identity then turns it into pointwise domination by the preparation retraction. Idempotence and rationality follow from the linear partial trace. No conditioning on a rare outcome is performed; rank preservation is intentionally not asserted. Centres with persistent hidden quantum memory are outside the definition.

## Coherent metric

The projective distance chi^2=1-|tr U*V|^2/d^2 equals half the squared Frobenius distance of normalized Choi projections. Summing eigenvalue differences provides a pair with sin(theta)>=chi/sqrt(2). The same U* correction after every call produces I versus W. A deterministic bounded stopping count gives either a linear N lower bound or a fixed saturated separation. Arbitrary different preparation factors cannot conceal this test, since they are discarded. A separate tester discards the data and retains preparation copies. These two testers need not be compatible with each other; each is a valid witness in the metric supremum.

For the upper bound, the hybrid first changes only U while keeping sigma fixed, costing at most 2dN chi. After holding V fixed, every tester is a common quantum processor consuming N preparation states. This costs Delta_N, not N times the one-copy distance. The final triangle inequality includes both contributions and their cross term when squared.

## Rational unitary atlas

A fixed elimination order uses d(d-1)/2 complex Givens factors, each with two real sphere coordinates, and d-1 diagonal phases. Removing one global phase leaves exactly d^2-1 real digits. Signed stereographic charts cover both sphere dimensions with bounded parameters. Every rational chart word decodes on the sphere and hence exactly unitarily. The chord-distance identity proves the radius with no approximate normalization. Existence of a suitable word does not rely on a finite numerical test. For rational supplied U, the finite search checks the exact squared Choi-ray distance; it has no polynomial-runtime guarantee.

## Packing and preservation

At the identity, the normalized Choi-projection differential is injective on traceless Hermitian matrices. Uniform closeness of this derivative to its value at zero on a small convex coordinate ball proves a bi-Lipschitz patch, not merely an unsupported inverse-continuity claim. The preparation patch is the inherited maximal-rank local Cholesky chart. Their Cartesian product is separated because either the unitary witness or the preparation witness separates each pair. The triangle argument is valid for arbitrary legal centres, including outside the family. The small-error range ensures saturated witnesses remain larger than twice the covering radius.

All v68 theorems remain under their original hypotheses. In particular, the general positive-margin description law is not silently extended to all boundary channels, and the v63 width multiplicative gap remains. The new tensor family has input-independent outcome probabilities; input-dependent measurement/backaction coupling is not classified here.

## What finite verification establishes

`check_coherent.py` independently evaluates exact chart identities, general-d unitary decoder images, finite rational amplification recurrences, combined Choi legality, ranks by separate Gaussian elimination, zero blocks, retraction and its rank-increasing example, malformed codes, target replay and the CLI. Both Python modes must agree. These checks are not a continuum proof, an independent priority opinion or a physical simulation experiment.
