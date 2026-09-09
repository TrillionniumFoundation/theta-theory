# Response to the uniform-threshold referee report

**Manuscript:** *Geometric stability and curvature identification for uniform collision thresholds*.  
**Author:** Qian Qi.  
**Revision:** A2 geometric thresholds v2, September 9, 2026.  
**Controlling review:** `review/a2-uniform-thresholds-harsh-independent-2026-09-09`, commit `14aaea8937f8b2d373bc642f3568d7280dcbbbd7`.  
**Reviewed manuscript:** `500cf06faccb6eadd6c122abeb63c60a0cb7522e`, native subtree `2e4303afeec148b5c318629443463db301d6e3c5`.  
**New revision branch:** `revision/a2-geometric-thresholds-curvature-2026-09-09`.

The report recognized the collision-order-uniform boundary-value and relative-flux arguments, while questioning the geometric scope and the informational content of the application. The revision retains the entire circular theorem and its proof and develops the noncircular route identified in UCT-R1. It also constructs an uncertainty not resolved by the threshold locations and proves its resolution by amplitudes. The record-response claims now have explicit metrics, differentiable test classes, and a moving-boundary calculation. We do not treat the absence of a counterexample in the previous review as a certificate of these new proofs; they are submitted for examination in their own right.

## UCT-R1 — An open geometric theorem, including competing shortest channels

**Statements:** Theorems 1.1–1.2, p. 2.  
**Proofs:** Sections 9–11, pp. 14–19.  
**Sources:** `v2/00_geometric_results.tex`, `v2/10_geometry.tex`, `v2/11_integration_inverse.tex`.

The parameter family is no longer a radius interval. It consists of smooth support functions in a sufficiently small open C4 neighborhood of a circle, on the fixed triangular lattice. No rotational or reflection symmetry is imposed. A compact smooth finite-dimensional family can vary unequal endpoint curvatures and nonsymmetric boundary jets. Higher derivative constants depend on the corresponding norms of that fixed family; the theorem does not pretend that a C4 bound alone controls arbitrarily high derivatives.

The six candidate closest channels have smooth gaps g_e and endpoint curvatures kappa_e,0 and kappa_e,1. Lemma 9.1 verifies their selection from the physical geometry: the lattice gap excludes more distant translates, the positive distance Hessian selects one closest chord for each pair, and angular separation plus specular reflection forces every sufficiently short multi-flight segment to alternate in a single pair. The neighborhood, clearance, contact arcs and total-excess collar are independent of the number of flights. This is a reduction of the complete event, not an assumption that the initial distribution has already been restricted to a normal orbit.

The unequal-curvature Jacobi equation is reduced by a two-periodic diagonal scaling. Its effective exponent satisfies

\[
\cosh\gamma_e=\sqrt{(1+g_e\kappa_{e,0})(1+g_e\kappa_{e,1})}.
\]

Lemma 10.1 gives the full endpoint Hessian and the exact quotient of its mixed twist by its determinant square root. The quotient is csch(j gamma_e), including the parity of the two different endpoint curvatures. The period-two physical multiplier is exp(2 gamma_e). These formulas specialize exactly to the circle.

Lemma 10.2 then proves the nonlinear statement. The graph functions need not be even; the gradient perturbation is quadratic and its endpoint action has a cubic, rather than necessarily quartic, remainder. Exponential endpoint weights are summable uniformly in itinerary length. For the relative flux, the exact corner-cofactor identity is divided by its own quadratic value. The one-flight logarithmic errors and the trace norm of the interior perturbation have bounded sums independent of j. The proof uses this relative argument rather than an absolute error added to an exponentially small twist. Smooth parameter bounds follow by differentiating the weighted fixed-point equation and the determinant identities; no analyticity of a general smooth boundary is asserted.

The full stationary measure contributes the factor 1/(2 pi A) in endpoint and residual-time coordinates. The perimeter cancels between section normalization and mean roof. Uniform smooth Morse integration yields the channel contribution

\[
\frac{d_+^2}{2A\sinh(j\gamma_e)}[1+d_+H_{j,e}(\xi,d_+)],
\qquad d=t-jg_e.
\]

Radial cancellation of odd terms gives a smooth relative remainder in d despite the nonsymmetric local geometry. The complete maximal-count probability is the sum of these contributions in a j-independent collar of the shortest onset. This summation keeps every candidate gap separate and therefore does not differentiate the nonsmooth minimum of the gaps.

Corollary 11.2 gives the moving physical threshold jump, with reversed orientations and coincident surfaces explicitly added. The support deformation h_s(theta)=R+s cos(2 theta) verifies a change of minimizing pair: the horizontal gap derivative is -2, while the other two pair derivatives are 1. Their competition is resolved by the positive offsets in the theorem, with activation on the scale epsilon/j. Thus the extension includes genuine minimizer changes, rather than imposing a fixed itinerary type as an unexplained parameter hypothesis.

This is the proposed substantive answer to the significance objection: full-preparation threshold laws are stable under nonsymmetric geometric changes, relative exponential flux remains controlled at arbitrary collision order, and the formula resolves competing onsets. The new inverse consequence below supplies additional geometric information. No claim about editorial acceptance follows from this proposed answer.

## UCT-R2 — Curvature uncertainty not determined by threshold positions

**Location:** Theorem 12.1 and Corollary 12.2, pp. 19–21; `v2/11_integration_inverse.tex`.

The response accepts the exact information issue in the circular model. The old multiplier corollary remains, but the manuscript no longer relies on it as identifying a degree of freedom independent of the known radius.

We construct the noncircular support family

\[
h(\theta)=R+(1-\cos6\theta)
       (\alpha+\beta\cos2\theta+\zeta\sin2\theta).
\]

All six supporting values and their first derivatives at lattice normals are unchanged. The complete set of maximal-count threshold locations is therefore exactly j(1-2R) for every member of the family. Strict convexity, exact closest gaps, and separation from more distant translates are verified in the proof. On the other hand, at the three unoriented contacts the curvature radii are R+36 b(theta_r), and the map from (alpha,beta,zeta) to these three values is invertible. The family has three genuine curvature degrees of freedom invisible to the threshold positions.

The unlabelled threshold coefficients satisfy

\[
 C_j=A^{-1}\sum_{r=0}^2\operatorname{csch}(j\gamma_r).
\]

An absolutely convergent odd-index Möbius inversion gives

\[
 F_j=\sum_{k\ge1,\ k\text{ odd}}\mu(k)C_{kj}
    =\frac2A\sum_{r=0}^2e^{-j\gamma_r}.
\]

We prove recovery from this finite positive moment sequence using the two Hankel matrices, their generalized eigenvalues, and a Vandermonde system. Multiplicities are included. The preparation area is recovered from the weights rather than supplied as extra inverse data. Together with the observed gap, the amplitudes determine the unordered contact-curvature triple. No ordering of lattice directions or recovery of the entire scatterer is claimed.

For beta=zeta=0, two coefficients already give

\[
\alpha=\frac1{36}
       \left[\frac{g}{C_1/(2C_2)-1}-R\right].
\]

The ratio varies while every threshold location stays fixed. This supplies a direct nonredundancy statement without calling infinitely many coefficients infinitely many independent parameters. For the full three-parameter case the original infinite sequence is used by the Möbius transform; we distinguish this exact identification from a finite noisy-data stability theorem.

Corollary 12.2 gives a related dynamical consequence: at exactly equal metric thresholds, the more weakly unstable channel can dominate the conditional event by an exponential factor in j. The leading-amplitude weights and fixed-positive-offset corrections are kept distinct.

## UCT-R3 — Comparison with periodic rare-event statistics

**Location:** Section 14.3, pp. 23–24, and bibliography; `v2/13_comparison.tex`, `v2/references.tex`.

The manuscript now compares directly with Carney–Nicol–Zhang, Theorems 1–2. It acknowledges their compound-Poisson and extreme-value laws, the foliation-adapted target metric and derivative-dependent extremal index. Statistical detection of periodic instability is not presented as a new idea of this revision.

The comparison then identifies the different theorem proved here: a complete physical maximal-count event, a common onset collar and relative derivative bounds for every collision order, noncircular deformations, and competition between threshold surfaces. The inverse statement identifies unknown curvatures in an explicitly isogap family. Neither mere replacement of an observable nor a new name for the Lambert series is used as the contribution argument. Conversely, the local threshold theorem is not promoted to a compound-Poisson theorem for unrestricted long observation sequences.

The prior marked-length-spectrum and variational comparisons remain. They identify other inverse data and the classical origin of the action/monodromy mechanism; the present proof does not supersede those theories or assert exhaustive worldwide priority. The primary CNZ text was read, including the metric, normalization and theorem statements. PDF screenshot retrieval failed; a visual inspection of that external PDF is not claimed.

## UCT-R4 — Separate record topology, smooth response, and discontinuous tests

**Location:** Propositions 13.1–13.2, pp. 21–23; `v2/12_record_response.tex`.

The common-coordinate conditional density is written explicitly on the fixed latent domain. Total variation is asserted there, not between physical measures on varying embedded surfaces. The growing record array uses a maximum norm. The circular theorem's stronger unweighted rate is preserved; nonsymmetric geometry and general source weighting have the appropriate O(sqrt(d)) rate in the scaled coordinates.

For response, Proposition 13.1 specifies smooth tests whose derivatives have uniformly bounded operator norms in that maximum-norm space. Tests on a fixed finite set of entries form a nonempty sufficient class. The proof differentiates the actual bridge, Morse inverse, density and reconstructed record on the fixed latent domain. Taylor division at zero and summable endpoint weights justify the uniform parameter-differentiated error. No derivative is inferred from a total-variation inequality.

Proposition 13.2 treats a moving physical sample near impact k. On a transverse cut separated from the other latent boundaries, its exact derivative includes the boundary term

\[
\partial_\xi I_j=\int\left[
\int_{\psi}^{1-|z|^2}\partial_\xi F_j\,d\eta
 -F_j(z,\psi)\partial_\xi\psi\right]dz.
\]

Repeated Leibniz differentiation gives the fixed-order response and its differentiated limit. The transversality class is verified to be nonempty uniformly, even for interior impacts: choose a=1/2 and support the test in |z|<1/2; positivity and the exact total-excess identity give both margins at least 1/4.

Fixed physical schedules have additional factors k/d. The formula remains valid where its stated margins hold, but uniform onset derivative bounds for every fixed schedule or arbitrary bounded decoder are not claimed. The complete-record limit and original finite-cut convergence are retained with their correct separate meanings.

## Axial source-domain refinement

Theorem 1.2 now proves the exact real source domain suggested by Section 5 of the report, and does so for the noncircular channels. The axial parity identity, positive relative amplitudes and exponential hyperbolic factor give convergence if and only if max_e(q bar f_e-gamma_e)<0. At equality one positive term fails to decay. On compact subsets of the strict domain every fixed mixed derivative is summable, because only polynomial factors in j occur. The old conservative circular source condition is unchanged and is a sufficient subdomain.

## Historical derivations and preservation

The revision was checked against the exact published v1 objects, not inferred from the cached package's name. The circular contact geometry, Green kernel, relative determinant, residual-time integral, record construction, terminal witness and source calculations supplied the proof route for the extension. The Round 33 A2 chapter was also read: its arithmetic proposition and conditional Fourier-inversion budget remain separate from an unrestricted billiard local-limit theorem. The new threshold series is not silently substituted for those missing model-level hypotheses.

The new repository subtree is based on the complete reviewed native tree. All original eight section files remain byte-identical, including the now-inactive old comparison file. The new comparison retains the previous mathematical discussion while incorporating the closer source and geometric distinctions. All 18 inherited theorem-like blocks and 17 inherited proof blocks are still verbatim in the active two-volume source closure. The new closure contains 29 statement blocks and 28 proof blocks. The two-collision companion remains Git blob df44402b17031525c087d39dfedf8dac3ada611d; all seven rebuilt pages have the same extracted text. These counts describe preservation, not significance.

The earlier response, proof ledger, source pins, review and verification records remain historical evidence. A new README and submission index identify the current manuscript; their former versions and the old main entrypoint are additionally preserved under history/v1. No previous branch or manuscript directory is overwritten.

## Executions and verification limits

The current full native build produces a 25-page main article and seven-page companion. All six compiler invocations succeed, auxiliary files converge after three paired cycles, recorder inputs agree with the 16 active TeX objects, and final logs have no unresolved citations/references, changing or multiply defined labels, or overfull boxes. Sources are identified by Git object hashes and SHA-256 values because the build precedes publication.

The unchanged circular diagnostic was rerun: 411 checks passed. The new geometric diagnostic passed 328 checks, including exact unequal-curvature Schur/cofactor identities, support jets, source parity, Möbius tail bounds and moving-boundary differentiation, together with non-interval nonlinear reflection and onset quadrature tests. Both programs were run normally and with python -O, with byte-identical corresponding outputs. The nonlinear tests include unequal curvatures and non-even cubic jets at lengths through 256. They concern local facing arcs, not a simulation of the full equilibrium billiard.

A preliminary diagnostic compared the total action remainder at two amplitudes. At one input the cubic and quartic terms nearly cancelled at the larger amplitude, invalidating that test's ratio rule. The final test instead evaluates the cubic term on the linear stationary bridge and checks the remaining quartic scaling. This is recorded as a corrected diagnostic design, not concealed as a manuscript counterexample or a theorem repair.

The reviewer's separate 125-check program has not been replayed in this revision. No interval proof, formal proof assistant, exhaustive priority search, remote CI success, finite-noisy-data inverse estimate or general long-time characteristic-function theorem is claimed. The new arbitrary-length geometric assertions rest on the written analytic proofs and remain subject to independent referee scrutiny.
