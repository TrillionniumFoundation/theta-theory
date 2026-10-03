# Response to the v20 referee report

**Manuscript:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Controlling review:** `40e9f1beaf49bf7f870f2f6f73ac027feab1a84e`  
**Report blob:** `d5adb7728eff4dbc8d69cf07937de73b5ecb445f`  
**Reviewed author source:** `c376e802e6e86735888dcd685f987c7a8f475903`  
**Revision:** A2 v21, 29 September 2026.

We thank the referee for distinguishing correctness, information content, and editorial significance. We retain the paper's topic and the complete reviewed mathematics. The present response adds two results rather than treating the recommendation as a reason to retreat from the problem. First, a bounded unquotiented spatial scan replaces an acquisition output already indexed by an unknown period group. Second, a sparse period-generating witness permits local statistical recovery across changes of redundant catalogue edges. Neither result removes the stated local probability sensor, the global analytic/genericity conditions, or all acquisition priors.

## 7.1. Proximity and visibility literature

Section 7.5 now compares the proof mechanism directly with Toussaint's relative-neighborhood graph theorem, the Jaromczyk–Toussaint survey, and Pocchiola–Vegter's visibility-complex and free-bitangent constructions. Proposition 7.10 defines a gap-relative subgraph for periodic bodies and proves its component equivalence by strict shorter-gap replacement. We credit the classical third-neighbor mechanism rather than presenting it as a new abstract proximity principle. Body gaps need not be a metric, and a finite point-set minimum spanning tree is not itself a period-generating object; the periodic conclusion uses the retained covering and path-lifting proofs.

For visibility, we compare Theorem 1 of the authors' 1995 LIENS report: free bitangents of given obstacles are computed in output-sensitive time with linear workspace under a constant-time bitangent primitive. Tangent segments are not the normal, non-grazing bridges used by the local billiard law. We therefore import neither its graph nor its algorithmic complexity. The new finite padding argument also states its own geometric primitives. The existing boundary-distance, lens, scattering and marked-length comparisons remain unchanged in Section 8. The literature ledger records which full primary text and which metadata/abstract were actually accessed; it makes no exhaustive-priority claim.

## 7.2. Catalogue equality and the unknown translation quotient

Definition 7.1 and Lemma 7.2 distinguish literal experimental equality from normalized information equality. Literal records retain their absolute times. Normalization recovers the action germ and free area; full analytic pair images with marked contacts give a geometric key independent of the chosen return orientation. The physical quotient is defined by the intrinsic group `P(O)={v: O+v=O}`, not by a chosen integer basis or cell. On the asymmetric shape-separated class, equality of pair keys is proved equivalent to equality of undirected translation orbits. Repeated scans and reverse returns can consequently be removed by the inverse, not by a device that already knows the lattice.

Theorem 7.4 gives a finite acquisition reduction. With known bounds `r<=r0`, `diam(C)<=D0`, `rho*<=rho0`, and `R>2rho0`, an exhaustive midpoint scan in radius

`B = rho0 + D0 + (r0-1)(R+2D0) + xi`, with `xi>0`,

contains at least one representative of every required bridge orbit. Lemma 7.3 derives the bound on the unknown lattice covering radius from the retained clear-bridge connectivity theorem. Padding by `R/2+D0` encloses every endpoint or blocking body relevant to the scan. Positive separation bounds the number of bodies, hence reduces selection to finitely many geometric tests.

This replaces an unknown-group representative oracle by exhaustive observation in a known finite physical region. It does not remove exhaustive scanning, construct the scanner's geometric access from unmarked trajectories, or replace the original cell-normalized phase law by a disk-normalized law. Those distinctions are explicit in the theorem and abstract. The scanner need not transmit its spatial coordinates to the inverse.

## 7.3. Covering and other global priors

The aperture theorem and its headline Theorem 1.1 display all bounds: number, diameter, covering radius, sufficient range, and positive aperture slack. These are prior bounds and are not recovered from a list with unknown omissions. The old finite-index ambiguities remain valid when a sufficient collection is not observed. No claim that an arbitrary bounded list certifies unseen coverage has been added.

The new number/diameter bounds make a known aperture possible. They were already among the bounded-geometry priors of the statistical classes, but they are now exposed for this exact acquisition statement. We do not disguise this exchange of assumptions as the elimination of every oracle.

## 7.4. Stability without freezing the whole catalogue

Proposition 7.5 extracts a saturated witness with at most `r+1+floor(log2 n)` records from a spanning tree and a cycle pair of index `n`. Each added independent subgroup generator reduces the remaining index by a proper divisor; no observed pair needs to be primitive. Theorem 7.6 proves that this finite witness persists under small smooth table and lattice deformations, with positive margins only on those edges. The integer labels used to track the deformation are proof coordinates, not observation inputs.

Proposition 7.7 supplies an actual analytic asymmetric family in which a surplus `(1,2)` channel crosses a fixed range cutoff while horizontal and vertical generating channels remain. Thus the full catalogue really changes in the scope of the new result.

Theorem 7.9 treats qualified unlabelled lists which retain the witness and may otherwise vary in number, include repetitions and reverse returns, or omit channels lacking the required local margins. Lemma 7.8 separates the witness keys from all finitely many possible bounded-range pair types in a local physical neighborhood, including types obstructed at its center. Histogram fits to physical pairs select the witness without input labels; a second admissible table fit and the retained all-cycle locking lemma give the table/lattice rate. Concentration is simultaneous over every inspected qualified record, not just the eventually selected ones.

The theorem is local on a compact analytic/generic physical prior. Qualification and witness retention remain acquisition conditions. It neither tolerates loss of every generating set nor consistently estimates a discontinuous full-catalogue topology. These are materially different conditions from a fixed indexing, positive cutoff margin, and positive clearance for every catalogue edge. The older global fixed-catalogue theorem is retained in full, not replaced by the local statement.

## 7.5. Analyticity, asymmetry and repeated shapes

The smooth local inverse and geometric persistence theorem remain separate from the analytic whole-table inverse. Analytic continuation, asymmetry and separation of different shape classes are explicit in the abstract and headline theorems. In Lemma 7.2, asymmetry is exactly what makes an isometry between translated copies a unique translation; shape separation is exactly what identifies obstacle type. Their use is proved rather than called incidental. The registered and finite-candidate results for other information categories remain in the current primary and Supplements R/S. No exact analytic count-only rigidity or nonrigidity is inferred.

## 7.6. Mathematical inverse versus algorithm

The aperture reduction gives a finite geometric selection problem and an exact duplicate-orbit rule. It does not give an efficient representation of arbitrary analytic bodies, a practical congruence test, or a global optimizer. The statistical estimator uses a compact physical prior and Borel approximate minimization; finite record permutation and reversal are canonicalized. The information and computational limitations are adjacent to the theorem statements, not hidden in the execution ledger. Two windows remain two density functions or two growing histograms.

## Preservation and execution

All six v20 mathematical core files remain active and byte-identical. The complete reviewed v20 paper tree, including its historical files and execution records, is preserved at `history/v20-reviewed`. The unchanged v18 tree is still Supplement R, and the complete smooth-theory tree is still Supplement S. No earlier manuscript or review path is edited.

This revision supplies its own source pins, validator, finite diagnostics and exact-triggering-SHA read-only workflow. Its local receipt records actual source-content execution with null checkout/run fields where unavailable. A historical v20 hosted pass is not relabelled as a v21 pass; the new hosted run must provide its own conclusion. The README and execution receipts state the observed verification scope. Finite computations and builds are not mathematical proof certification or a journal decision.
