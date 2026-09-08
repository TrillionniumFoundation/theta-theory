# Proof dependency and claim ledger

## Controlling identity

The revision answers the two-collision report at `50e2bd898e3168d43f1519729a0d88ccbc03946a`. It retains the note at `e8d3b658ead4996dabfc9f31a07b812e070f5446` without alteration and adds a new self-contained main article.

## Principal chain

1. **Physical preparation and exact marked flux** (`sections/02_flux.tex`, Proposition 2.1). Flight-tube volume gives the finite mean roof from the full normalized phase measure, including infinite-horizon radius ranges. Lower gap excludes collision accumulation. Changing to the first future collision retains the residual-time variable and all marks. The complete maximal-count event is exactly the integral over S_j tau<T with 0<r<T−S_j tau.

2. **Global event localization** (`sections/03_geometry.tex`, Lemma 3.1). Every individual flight has nonnegative excess. A small total excess forces each target to be nearest and each reflection close to a normal chord. Angular separation forces alternating backtracking, uniformly in j. The six charts cover the whole event, not a preselected transverse ensemble. Arc stationarity corresponds to actual unobstructed specular flights.

3. **Uniform boundary-value solution** (`sections/04_uniform_action.tex`, Lemma 4.1). The exact circular length gives a tridiagonal Jacobi system. Its Green inverse is written explicitly. A weighted supremum norm with endpoint-decaying weights makes the cubic remainder a contraction on a j-independent ball. Strict convexity proves uniqueness over the entire chosen box. Uniform complex neighborhoods give fixed-order parameter derivatives. Summing the endpoint weights controls the action remainder without a factor j.

4. **Effective Hessian and relative flux** (Lemmas 4.2--4.3). The exact endpoint quadratic Hessian is proportional to the matrix with diagonal coth(j chi) and off-diagonal −csch(j chi). Its determinant stays nonzero while the mixed derivative decays exponentially. An exact corner-cofactor identity expresses the actual twist as a product of one-step twists divided by an interior determinant. The perturbation has trace norm O(u^2+v^2) independent of j; log-determinant comparison therefore gives a relative, not merely absolute, error. This is the step preventing loss of the principal exponential scale.

5. **Physical coordinates and uniform Morse integration** (Proposition 4.4; Lemma 5.1). First variation turns the endpoint twist into the normalized collision flux. An explicitly constructed even matrix square root gives odd Morse coordinates with one common neighborhood. Coercivity proves that the whole active set is within it. Integrating the residual-time factor on the exact two-dimensional ball gives the quadratic onset and the explicit coefficient at every j.

6. **Sources and derivative sums** (Lemma 5.2; Theorem 1.2). The actual outgoing states and both velocity traces depend on neighboring bridge coordinates. Additive deviations from the axial mark sum have uniformly bounded fixed derivatives because their endpoint weights sum. Even integration removes odd Taylor terms, giving a smooth right-hand source expansion. Derivatives of csch(j chi) and of the axial source factor cost only powers of j. The printed source bound leaves a strictly positive exponential margin for summation.

7. **Record and sampling cuts** (`sections/06_records.tex`, Theorem 6.1). Retaining r gives the common paraboloid domain. Exact density comparison yields O(epsilon) unweighted total variation. Scaled positions/times and velocities are obtained from the same trajectory. A sampling cut has derivative one in the residual-time coordinate, giving an explicit strip bound. General source-weighted conditional total variation is only O(sqrt(epsilon)); the stronger integrated error is not misapplied to it.

## Consequences and distinct regimes

Section 5.1 proves the derivative jumps and distributional singular terms across every onset surface. These are not obtained by differentiating through a regular level that does not exist there.

Corollary 7.1 compares with genuinely independent roofs sharing the exact same marginal. Simplex integration yields exponent j+1, whereas the actual billiard has exponent two. Corollary 7.2 computes the period-two multiplier and the meromorphic generating series of threshold coefficients. That series is not a pressure or a fixed-window count generating function.

The original note is an exact independent companion for R in [0.45,0.47] and T=0.11. It includes its previous geometric proofs and all-order moving-level formulas. Its strict terminal-level witness is added in the new main Section 7.3, not used to erase the original proof.

## Historical and external inputs

The exact original note was recovered from a library cache only after checking its Git blob against the connected repository. The repository's DYN one-event flux appendix was consulted as historical background; the new main proves its own flux identities. The Round 33 A2 chapter was read at its pinned carrier and is retained as an arithmetic/conditional-inversion source. No conditional high-frequency or central remainder estimate is silently treated as a proven billiard input.

Marklof supplies the classical stationary/Palm comparison. Bolotin--Treschev supplies context for action-Hessian/monodromy identities. The BDKL inverse marked-length theorem concerns a different data set and model. Demers--Zhang and Demers--Melbourne--Nicol concern perturbative spectral theory and typical-orbit limit laws. Their statements are compared, not substituted for the present proof. Section 8 and the bibliography give precise distinctions and source locators.

## What remains separate

The new main proves a uniform extremal threshold hierarchy for actual billiards. It does not assert the original unrestricted source-differentiated mixed Edgeworth theorem. That application still needs the corresponding full characteristic family, periodic-data realization and source-dependent operator/remainder estimates. The current source summability is over distinct threshold windows and is not an estimate of every itinerary in one typical long record.

## Verification status

The native build and its source closure were executed. The companion source is exactly preserved. The 411 diagnostic checks and ordinary/optimized agreement are recorded separately. Their finite rational and floating scope is explicit. The 13 new proof environments contain the analytical arguments; no formal proof-assistant certificate or external acceptance is implied by this ledger.
