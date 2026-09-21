# Response to the referee report on A2 revision 111

Controlling report: `review/a2-v111-independent-harsh-top4-2026-09-21`, commit `cafc6c1bd403dae4acc66177fb43feee54c02b1d`.
Revision: v112, independently branched from that exact review snapshot.

## The principal mathematical response

The report correctly asks for a structural explanation of both branches of the codimension minimum, rather than another list of witnesses or matrix families. Section 5 now proves such a theorem. This is not a change of the original theorem's hypotheses: Theorem 1.1 retains its complete c>=4 scope. The new component and scheme conclusions have additional, expressly stated stable-range hypotheses c>=8 and k>=2c+1.

The new geometric objects are signed secant varieties. A rank-two Hankel form has two isotropic hyperplanes. Different contacts can choose them independently. The common-secant incidence from v111 is the all-equal choice, not the whole multi-contact rank-two locus. The other choices give 2^(L-1) distinct components modulo simultaneous sign reversal.

Theorem 5.1 proves all components and the entire scheme in expected codimension: integrality and Cohen--Macaulayness when a<b, and reduced Cohen--Macaulay structure with exactly one nondegenerate and 2^(L-1) signed secant components at a=b. In excess codimension it classifies all maximal-dimensional components and proves their generic scheme smoothness. The generic corank is one on every listed component. The full-rank component is birationally parametrized by the nondegenerate isotropic incidence; the signed components are rational.

The key new connection is the residual wall. Intersecting each U with the radical of its rank-two annihilator and removing the two secant points yields (c-1)-planes in a (k-2)-space. Their multiplication is saturated precisely when a>=b. Applying the previously proved full-range codimension theorem to this residual problem gives the actual tangent dimension, not just an expected count. This is the basis of the generic scheme-smoothness and local conditioning statements.

The Eagon--Northcott grade criterion and Thom--Porteous cycle formula are explicitly attributed classical tools. The new work is in identifying the components, proving the strict incidence gap, showing the nondegenerate component exists and is generically corank one, and proving the residual tangent statement that makes these tools apply to this particular multiplication family.

## Response to the major directions in Section 16 of R111

A (components): proved for the entire failure scheme in the expected-codimension stable range and for all maximal-dimensional components in the excess stable range. The determinantal branch now has a geometric component, not only a height upper bound.

B (scheme, cycle, singularity): proved reducedness and Cohen--Macaulayness throughout expected codimension, integrality in the strict determinantal regime, the cycle c_a((direct sum Sym^2 S_nu)^*), and generic scheme smoothness of the listed components. No assertion of normality, global smoothness, or excess-range unmixedness is made.

C (higher products): not needed by the selected structural route and not asserted. The requested serious advance is supplied by A and B, not by a superficial new family.

D (random conditioning): Corollary 5.8 proves a local small-singular-value exponent at specified smooth real native strata. It is not a dimension-uniform global random-design tail theorem.

E (statistical interpretation): the quantized protocol removes the need for actual observation-side jitter; the full exposure tangent model is treated before taking the nuisance quotient. It remains a known-mark local score experiment, not an invented physical distance observation or global unknown-mark sufficiency theorem.

F (singular statistical rates): the existing physical root-rate result is retained with a finite-sample moment proof. No new minimax transition at shrinking singular values is claimed in this revision.

G (priority): the introduction and `LITERATURE_AUDIT.md` compare the actual Green--Lazarsfeld and Ballico statements, distinguish their complete-series/fixed-surface problems from the varying subseries problem here, and attribute all determinantal inputs. This is a documented primary-source comparison, not an assertion that no other antecedent exists.

## Detailed comments 1--34

| R111 item | Revision and precise scope |
|---|---|
| 1 | Theorem 1.1 is titled “Reduced failure locus and independent contacts”; Section 5 separately defines the maximal-minor scheme and states scheme conclusions. |
| 2 | Section 5 gives the exact CMSV dimension display on arXiv page 2, with t=r+1, and equation (2.0.1) for the secant identification. |
| 3 | Exact-rank strata and their rank-at-most closures are distinguished explicitly at the start of Section 5. |
| 4 | Lemmas 4.2 and 5.4 give the relative radical-intersection and isotropic-Grassmannian descriptions, including the hyperplane restriction calculation. |
| 5 | Lemma 5.2 proves a strict gap away from rank two and full rank in the stable range. The paragraph following it explains the endpoint geometry; the residual wall gives the deformation interpretation. The original small-case proof is retained unchanged. |
| 6 | Lemma 5.3 defines the double-hyperplane exceptional incidence and computes its dimension, proving birationality rather than merely an incidence upper bound. |
| 7 | Theorem 1.1's common-secant component qualification is retained. Section 5 distinguishes all signed subvarieties from the regimes where they are actual maximal components. |
| 8 | At a=b the entire scheme has exactly 1+2^(L-1) components in the stable range, with generic corank and scheme structure identified. |
| 9 | The proof of Theorem 5.1 specifies the polynomial coordinate ring in Lc(k-c) variables, the p-by-Lq matrix, maximal-minor ideal, height, grade and resolution. |
| 10 | Corollary 5.7 constructs real open subsets in every signed incidence, uses birationality over the reals, and intersects the residual-spanning and smooth opens before transferring codimension. |
| 11 | The proof of Corollary 5.7 states that s and -s define the same unordered coordinate partition. |
| 12 | The same proof restates Euclidean openness and Zariski density; positivity is not described as Zariski openness. The original exact realization theorem is preserved. |
| 13 | Lemma 6.2 retains explicit dependence on the fixed loading, germ and compact metric set. |
| 14 | No dimension-uniform projection tube is claimed. The new conditioning corollary explicitly restricts constants to a compact fixed chart. |
| 15 | Corollary 5.8 specifies the compact frame/loading chart for its two-sided distance law; Theorem 7.2 retains its compact-chart proof. |
| 16 | The spectral example remains in the paper but is not a principal abstract contribution. No extra elementary family is added. |
| 17 | Theorem 9.1 specifies a Euclidean compact index set and the supremum absolute remainder in baseline probability. |
| 18 | Corollary 9.2 now derives bounded variance and uniform bias directly from finite-cell score moments and actual-allocation information I_N, separately from weak LAN. |
| 19 | Lemma 10.1 now has a quantitative L1 proof: Stirling remainder, central region, within-cell interpolation, tails, tensorization and covariance replacement. The explicit order is N^(-1/5); no optimal rate is asserted. |
| 20 | Both deficiencies and their symmetric maximum are defined before Lemma 10.1; forward and reverse kernels are exhibited. |
| 21 | The local target section is defined before observation. Proposition 10.4 additionally decomposes the full exposure tangent model into target and unrestricted nuisance coordinates without claiming their full experiments equivalent after discarding the nuisance. |
| 22 | The score statistic is consistently distinguished from physical distance measurements. |
| 23 | The jittered protocol discards the auxiliary draws; this is observation-side randomization, not just a proof device. |
| 24 | Theorem 10.3 proves the deterministic finite-precision alternative with an explicit two-sided error bound and an optional overflow symbol for a finite alphabet. |
| 25 | The final paragraph gives a sufficient independent-pilot regime sqrt(N)*centre_error -> 0, explains the root-M implication M/N -> infinity, and does not claim an ordinary comparable-size pilot satisfies it. |
| 26 | “Known-mark” appears in Theorem 10.2's title and its first sentence specifies the centre and submodel. |
| 27 | The information projector is treated as standard Gaussian linear algebra applied after the experiment comparison. |
| 28 | The introduction compares GL86 Theorems 1 and 3 and Ballico96 Theorem 0.2; the audit records the precise reading scope and classical inputs. |
| 29 | The abstract and introduction lead with failure schemes, components and the residual wall; sharp native recovery is an application. |
| 30 | No historical theorem is discarded. Three inherited mathematical parts are byte-identical, and all 68 prior labels remain. Complementary material stays organized in appendices rather than being removed or used as the principal novelty claim. |
| 31 | Workflow receipts, response history and preservation material are outside the mathematical source. |
| 32 | No witness tables were added to the article. Finite diagnostics remain separate and are not evidence of universal correctness. |
| 33 | No additional matrix family was added. |
| 34 | The next revision is organized around the new structural theorem and residual wall, not around a sequence of referee objections inside the article. |

## Proof dependencies and remaining scope

The strict gap, signed incidence separation and nondegenerate-incidence lemmas are proved before the structural theorem. The residual tangent proof uses Theorem 1.1 already established in Section 4, with k replaced by k-2 and c by c-1; it does not invoke the structural theorem inductively. Expected-codimension purity is obtained from the Eagon--Northcott criterion, and generic reducedness is then proved component by component. This closes the logical dependence needed for the asserted whole-scheme statement.

The stable-range theorem does not classify the low-dimensional equality exceptions of the full codimension theorem. The excess case does not classify smaller components, embedded structure, all component intersections, or global singularities. These are not represented as solved, and no original full-range result is weakened to avoid them. The known-mark and local nature of the statistical experiments also remains visible. Venue-level significance and the correctness of the new universal proofs remain matters for the next independent referee, not outputs of the build script.
