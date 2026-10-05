# Written-proof audit — Revision 74

This is an author-side adversarial audit, not an independent referee report or proof-assistant certificate.

## 1. Radial reduction and support change

The radial pair M_ru, M_su uses one common projective measurement and Bernoulli flip programmes. Every adaptive tester is a common channel of the N bits; repeated +u eigenstate inputs attain the classical product distance. Thus the radial equality is exact, not merely a local estimate.

The converse groups trials into k=min(N,floor(1/(2q))), q=(1-s)/2. The no-success probability gap is at least k(q-p)/2. An explicitly written stochastic affine map gives symmetric Bernoulli biases; its two row probabilities are checked in [0,1]. The inherited finite majority lemma supplies the square-root amplification. The floor bounds and the zero/singular cases are included. The result has cutoff 1-s²+1/N, so it also describes a pure endpoint compared with a nearby mixed effect. A variance-only or Gaussian argument at q=0 would not suffice.

## 2. Coupling radial and angular changes

A naive subtraction of an angular error from a radial error can cancel and does not prove the desired joint lower bound. Instead, a fixed +u input gives success parameter q'=(1-s cos h)/2>=q. Monotone likelihood ratio for binomial counts shows that this pair is at least as distinguishable as the aligned radial pair. Consequently d_radial<=d_actual. Triangle inequality then gives d_same-radius<=2d_actual. Both coordinates are therefore controlled without cancellation. This is the crucial coupled step.

The previous angular theorem applies to any pair of sphere directions by one common unitary change of coordinates. Ordered labels remain fixed. At zero radius no angular parameter is assigned or charged. The one-use norm calculation is repeated to fix normalization. The full adaptive supremum is used in the upper bound; the lower tests may be nonadaptive and pair dependent.

## 3. Weighted local geometry

Let e_N(x)=1-|x|²+1/N and w_N=sqrt(N/e_N). On a Euclidean ball of radius t/w_N(x), the relative change of e_N is at most 2t because N e_N>=1. Conversely, sufficiently small operational distance forces such a Euclidean localization first at the smaller-norm endpoint, and hence at either endpoint. This proves local comparability of weights and balls, not a globally constant metric.

For k-Ahlfors measure mu, the weighted measure nu=w_N^k mu assigns order t^k to each sufficiently small operational ball. Separated nets give the upper and lower covering bounds. The lower packing excludes all off-family legal centres solely by triangle inequality. No unproved retraction, one common estimator, or global seizer is invoked. The regularity constants and small-error cap are fixed with X and independent of N.

The criterion applies on the identifiable Bloch image X. A redundant parametrization with a collapsed direction at erasure does not receive extra dimension. Ahlfors regularity is an actual hypothesis; arbitrary nonregular sets are not silently included.

## 4. Contact trichotomy

The depth distribution F(t)=mu{1-|x|²<=t} enters by Stieltjes integration; no density for F is assumed. For F(0)=0 and F(t) comparable to t^alpha, integration against (t+1/N)^(-k/2) gives the three regimes. A positive boundary atom contributes N^k exactly. The disk is critical (k=2,alpha=1), explaining the logarithm. The ball has k=3,alpha=1 and boundary-dominated exponent 2. These are joint-family covers, not integrals of fixed-visibility code lengths treated as independent statements.

The contact-order illustration explicitly assumes two-sided transverse volume and deficit estimates. It is not an assertion that every singular geometric set has such a normal form.

## 5. Rational code and all-word legality

Radial grids discretize beta=arcsin|x| through rational tan(beta/2) values. The derivative bound for 2 arctan gives the radial error. The exact scalar comparisons use squared rational norms and monotonicity, so rational inputs with irrational norm are accepted. For direction digits, the sign of b-va is tested before squaring; omitting that test yields wrong choices.

Every signed-axis stereographic cube point has exactly unit norm, including overlaps and cube corners. Multiplication by the decoded rational radius keeps the centre in the closed ball. Choi blocks use the input-first transpose E_y^T. Their determinants equal (1-r_i²)/4 and their sum is the identity. Every index is legal; encoder replay, a stricter target-specific assertion, is checked separately.

One index enumerates all radial layers and angular words. Neither the radial digit nor visibility is an uncharged header. The harmonic sum in dimension two yields N log(N+2) delta^-2; the squared reciprocal sum in dimension three yields N² delta^-3. The implementation enumerates only radial sizes but makes no optimal-workspace or encoded-input polynomial-time claim.

## 6. Preserved dependencies and exclusions

The v73 angular metric and majority lemma, v72 observable readout and ambient seizing theorems, and previous Choi, state, coherent and streaming results remain in their original proof graphs. Their full hypotheses are retained. The structural companion is inherited, including fresh nondisturbing classical probes; no quantum repeatability interpretation is added.

Remaining assertions not established here include a general biased-POVM or disturbing-instrument criterion, a large-error coupled-ball cover, a common optimal estimator, independent priority, and human author signing. The new small-error criterion is a theorem with explicit scope, not a claim that all instrument boundary geometry is classified.

## 7. Evidence

`check_coupled_geometry.py` supplies exact finite binomial comparisons, stochastic-processing checks, algebraic comparisons, rational sphere identities, effect determinants, index accounting, and target replay with negative controls. It does not prove the continuum theorem or adaptive supremum. All ten inherited suites are executed unchanged. Native/source hashes, PDF rendering and isolated builds are evidentiary checks of the submitted object, not substitutes for the written proofs.
