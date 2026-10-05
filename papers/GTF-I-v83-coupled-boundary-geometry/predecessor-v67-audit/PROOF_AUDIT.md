# Author proof audit — Revision 67

This is an author-side proof/dependency audit, not an independent referee report.

## 1. Affine geometry

The real Hermitian input has m(dn)^2 coordinates. Summed output partial trace is surjective onto Herm(d), so its kernel has codimension d^2. The central blocks I/(mn) are positive definite; consequently the legal body has the full affine dimension s. For the associated block map, tuple Frobenius <= block trace sum <= d times diamond. Thus a diamond ball of radius 1/(dmn) is legal. The body is in the radius-two channel ball. Volume comparison, followed by rational centre perturbation, gives the finite cover bounds. Rational density comes from the following independent construction, not from the covering theorem itself.

## 2. Intrinsic rational construction

Only the s unomitted independent coordinates are truncated. Marginal completion uses no coordinate that was itself omitted. The omitted independent real error is at most (mn-1)/B; all other independent errors are at most 1/B. The bound 2dn mn/B <= c/B controls operator error. Exact marginal correction plus cI buffering gives CP and joint TP. The three-term Choi difference is bounded by 3mndc/D using total Choi trace d. No entrywise notion of matrix positivity is used. Arbitrary digit words can fail CP; exact validation or a canonical fallback makes the decoder's domain explicit. Code validity is not target proximity.

## 3. Interior common-tester bound

For two instruments with blocks >=lambda I, let their tuple-Frobenius distance be r<=lambda. Their midpoint plus/minus lambda times the unit difference direction consists of genuine CP/TP instruments. Weights 1/2 +/- r/(4lambda) represent the two targets and are >=1/4. Relative entropy is bounded by 2r^2/lambda^2. A programme string sampled independently at each potential use, passed through one common quantum processor representing the tester, reproduces the complete experiments. Product Pinsker gives trace error <=2sqrt(N)r/lambda. This proof includes adaptive measurements, reference entanglement and public stopping by linearity and ignoring unused signs. It does not replace quantum operations by classical messaging. The classical-mixture principle is explicitly credited to its metrology antecedent.

## 4. Interior description converse

Feed independent normalized maximally entangled inputs. Their outcome-retaining normalized Choi states differ by block trace distance >=tuple-Frobenius/d. One pair-specific binary measurement gives probability gap >=r/(2d). Repeated binary observations yield the stated Hoeffding lower bound, with an elementary log-moment proof included. A Frobenius ball of radius R=1/(mn)-a fits in the fixed-margin body. Points separated by c_delta/sqrt(N) have operational distance >2delta and cannot share a decoded centre. This proves the lower cardinality exponent s/2. The same tester must be used for the two states of each comparison, but a metric-separating test may depend on the pair. No hidden-experiment information is given to it.

## 5. Achievability and parameter ranges

The codec error in tuple Frobenius is <=K/B. Taking B>= (K/a)(2+4ceil(sqrt N)/delta) gives error <=a/2, so the decoded margin is >=a/2, and the interior lemma applies with lambda=a/2. It bounds stopped joint-state error by delta. The bit coefficient s/2 is asserted with dimensions, margin and delta fixed. Finite inequalities are displayed for variable parameters, without claiming optimal constants. The strict-boundary unitary example disproves a uniform extension of the square-root modulus to all channels but makes no claim of a full boundary entropy classification.

## 6. Schur validation

After positive pivots I, remaining entries are ordered bordered minors divided by the positive principal minor det A[I,I]. Zero residual rows may be skipped without adding an index to I. Hadamard bounds real/imaginary determinant lengths; reduced fractions cannot enlarge them. This supplies polynomial explicit-input validation, not a matching streaming-memory bound or an optimized polynomial exponent. The code follows the same leading-pivot/zero-row procedure.

## 7. Preserved scope

The v66 arbitrary-reference description theorem and variable-data numerical upper theorem retain their separate error meanings. The inherited fixed-program spectral lower bounds do not become general numerical-workspace lower bounds. The structural repeatable-probe and v63 width-crossing hypotheses remain unchanged. No local theorem uses or closes the independent A/B/C/D analytic gates. The complete manuscript and source inventory preserve earlier mathematical labels.

## 8. Executed evidence is reported separately

`check_codec.py` validates finite coordinate/mixed-radix cases, Choi legality, exact margin and square-root grid inequalities, two-programme algebra, product-binomial distances, Schur bordered minors, malformed inputs and a rational unitary boundary family. Existing v66/v65/v64/v63 suites are rerun unchanged. The build binds tests and PDFs to native source hashes and reconstructs in an empty directory. None of these computations is a universal formal proof, spectral certificate or independent priority opinion.
