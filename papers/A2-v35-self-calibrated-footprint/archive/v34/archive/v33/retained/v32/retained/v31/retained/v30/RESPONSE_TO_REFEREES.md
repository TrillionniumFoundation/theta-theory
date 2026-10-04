# Response to the v29 referee report

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Report:** `6444b57768313ac68978b3ee04a428b4832ccb6e`, report blob `d5e4be543ceb354341e01897fda83532707b1481`  
**Reviewed author head:** `b81664d3961cdbad58563f37dcaed03288de199e`  
**Revision:** A2 v30, robust scalar reconstruction

We thank the referee for distinguishing the validity of the scalar reversal and period arguments from the information-contract and contribution questions. The current revision retains the title, collision-law topic and every reviewed mathematical chapter. It responds with two mathematical extensions and a constructive theorem, not by replacing the problem or inferring journal significance from an upper-bound exponent. We also recognize that v29 already had a successful exact-source twelve-document qualification; that source-delivery issue is not reopened or described as still defective.

## 1. Capacity functionals, morphology and active probing

Section 8 proves the precise comparison before discussing priority. If Q has the commanded law and X=O-Q, Proposition 8.1 gives

`P_a(f) = T_X([0,a]) - T_X({0})`.

The first term is a classical hit-capacity datum; the second subtracts solid starts. The translated reverse command has the same segment-hit capacity and a different singleton capacity, so their difference is exactly the signed endpoint occupation difference. We neither claim capacity functionals as new nor confuse this endpoint convention with a free-phase conditional law. Matheron's hit/containment formulation and Molchanov's capacity framework are explicitly credited. Theorem-level comparisons then identify the different responses in Edelsbrunner–Skiena X-ray determination and Bose–De Carufel–Shaikhet–Smid Theorem 4.1 on wedge probing. No ordering of those richer individual responses against this localized Bernoulli protocol is inferred. `LITERATURE_AUDIT.md` records versions and the portions actually accessible.

## 2. Solid starts in headline statements

The abstract, opening paragraph, unnumbered Main theorem, Theorem 5.2 and Theorem 6.3 all state the convention: one is a free segment hit; solid starts and free misses both give zero; every attempt remains in the denominator. The original endpoint proof and original five chapters are unchanged. Conditioning on a successful launch is not substituted for this protocol, and no implementability of solid-start accounting is inferred from an output bit.

## 3. Scalar output and spatial input complexity

The abstract and Main theorem place `O(nu^-3)` spatial commands beside the one-bit output and the attempt count. Exact data are functionals on spatial launch laws, not two numbers. The finite construction commands a complete deterministic grid and retains command identities. Earlier uniformly prepared count germs, intrinsic endpoint laws and localized active scalar laws are still separate experiments. Neither Blackwell dominance nor a common minimax rate is asserted.

The new randomized-preparation theorem also makes the input coupling explicit: a forward draw (q,a) is paired in law with the reverse preparation (q+a,-a). Independent reverse starts with no coupling to their displacement do not supply the stated forcing.

## 4. Mean stability versus apparatus calibration

Proposition 2.1 still has a scale-independent `2m epsilon` mean-error bound. The new Theorem 5.2 proves a different, scale-dependent physical bound. For coupled position error ell, duration error tau and angular error alpha at nominal duration at most b, put `r=ell+tau+b alpha`. When r<=sigma, the scalar bias is at most `C r/sigma`, plus any exceptional coupling probability. The proof uses swept convex bodies and a local convex-boundary tube bound. It includes nominal grazing directions and errors depending on the commanded start; it does not assume zero mean jitter.

Consequently the constructive finite experiment permits `ell+tau+t alpha <= c sigma`, with sigma proportional to nu^(3/2). This is a sufficient certified tolerance, not a scale-free promise or an estimator of the apparatus errors. Curved pre-impact dynamics outside the specified model are not included.

Theorem 5.3 gives a complementary exact relaxation: known bounded distributions of directions and durations satisfy a finite stopped inverse under a geometric cone condition. Its Bellman recursion recovers occupation in m steps with error amplification at most m. The proof makes the stopping mechanism and its failure without a bounded hitting time explicit; it does not relabel ordinary stochastic averaging as automatically invertible.

## 5. The known patch margin

Known positive eta is stated in the abstract, Main theorem and Theorem 6.3 and remains in the finite period proof. The new threshold/hull procedure does not require eta for local component recovery. Uniform exact orbit and rational-period decisions use eta at the subsequent period-classification step. The bounded periodic-presentation hypothesis still supplies a protected representative patch; it is not a conclusion inferred for an arbitrary aperiodic set.

The unknown-margin pointwise corollary and repeated-disk symmetry-increase example remain unchanged. The constructive sequence has the same eventual fixed-table consequence but no observable uniform finite stopping certificate without a margin.

## 6. Exact relations versus estimated Euclidean vectors

The Main theorem and Theorem 6.3 state that the recovered discrete data are rational relations in a true independent-pair basis. The real coordinates of that basis and of the geometric periods have error O(sigma), not zero. Lemma 3.6 classifies physical periods before rational locking; neither the old nor the new algorithm takes the integer span of noisy real vectors. The final smooth-presentation area has error O(sigma^(2/3)); the separate raw polygonal area estimate has error O(sigma). These two quantities are distinguished in the new proof.

## 7. Existence selection and actual finite reconstruction

Theorem 4.1 and its countable dense-family selector remain explicitly existence-based, byte-identical to the reviewed text. We do not rename that selection an algorithm. Instead Lemma 6.1 proves a new threshold/cluster/hull construction directly from the finite recovered occupation averages. Interior rolling disks give connected retained grids and componentwise Hausdorff error below 3sigma, with protective collars excluding outer fragments. Proposition 6.2 differentiates a compensated kernel rather than assuming a smoothness bound on a polygon; a finite quadrature gives a genuine smooth convex support representation.

Theorem 6.3 combines that construction with the retained finite period tests. A conservative operation count is O(sigma^-4)=O(nu^-6) in a stated arithmetic/comparison/fixed-kernel model after the means are supplied. It is neither optimized bit complexity nor apparatus-travel cost. The accompanying numerical implementation exposes the finite chain, Bellman, hull and rational stages and is labeled floating point rather than interval certified. The continuum theorem provides the numerical-enclosure requirements; the code is not represented as having certified every such requirement.

## Current source and verification

All five v29 cores remain active with their original Git blobs. The exact whole reviewed v29 paper tree is retained at `retained/v29`, with its twelve-document supplementary chain intact. The new primary is 19 pages. The actual local source-content run passed 6,800 mathematical/source checks and 34 contract checks in both normal and optimized Python, and compiled without final TeX diagnostics. It did not run physical hardware or rebuild retained volumes. The new read-only exact-SHA workflow requires a current thirteen-document inventory and publishes actual failures as failures. Its actual hosted outcome is separate evidence, not inferred from the v29 pass or from this local receipt.

The contributions submitted for renewed mathematical review are the stopped mixed-preparation inverse, the grazing-uniform calibration bound and a finite geometric reconstruction under explicit priors, together with the retained scalar reversal and whole-period recognition. They are not claims of a passive count-only theorem, minimax optimality or an editorial decision.
