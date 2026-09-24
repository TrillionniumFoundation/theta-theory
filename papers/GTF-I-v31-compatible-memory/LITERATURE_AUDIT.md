# Source and theorem audit — revision 31

Audit date: 25 September 2026. The new comparison concerns the exact sources below, not an assertion of exhaustive priority clearance. All bibliography entries in the article refer to external work; previous GTF revisions are identified as repository provenance and supporting results, not peer-reviewed publications.

## Nevskii–Ukhalov: cube absorption

Inspected: *Five-dimensional Perfect Simplices*, arXiv:1709.06068v3, full HTML and PDF; especially Theorem 2 (centroids), Theorem 3 (Hadamard construction), Theorem 4 and Section 6 (dimension five), Section 9 (dimension nine), and the introductory axial-diameter/absorption discussion. PDF pages 15 and 23 were visually inspected for the actual matrices/vertex lists. Published form: *Perfect simplices in R^5*, Beitr. Algebra Geom. 59 (2018), 501–521, DOI 10.1007/s13366-018-0386-6.

The classical quantity uses homothety about the simplex centroid. At the critical factor n, their centroid theorem makes the centered [-1,1] decoder formulation identical after x -> 2x-1. The universal factor, Hadamard static equality and static equality in dimensions five and nine are prior results. The latter nine-dimensional critical simplex is not perfect in the stronger all-vertices-touching sense. The manuscript makes that distinction.

The current transfer theorem supplies a finite sequential encoder for every enclosing simplex, with no increase in peak labels. For a critical simplex the inverse barycentric matrix explicitly supplies q_i(s|x_i)=|b_si|+b_si*x_i and the replacement rows. Static seed geometry is not novelty evidence. The new checks independently multiply the displayed centered matrices and verify their inverse identities, rational probabilities and full input/query laws.

## Kondo–Sato–Yano–Maeda–Ito–Yamamoto: worst-case RAC geometry

Inspected full version: *Random Access Codes: Explicit Constructions, Optimality, and Classical–Quantum Gaps*, arXiv:2604.21274v3, 16 July 2026. The full HTML and PDF were read at the directly relevant statements; PDF pages 12–13 were visually inspected. Primary comparison: Theorem 14, Lemma 15, equations (123)–(149), and Theorems 16–17. The article's no-shared-randomness convention agrees with our checkpoint convention. The source uses 2^k messages; our state alphabet can have any integer cardinality.

Theorem 14 minimizes directed l-infinity Hausdorff distance from Boolean corners to a convex hull of decoder vectors. Lemma 15 explicitly reformulates this through a centered cube contained in the transformed hull. The correct normalization is eta=1-2e and p=(1+eta)/2. Thus exact conditional channel synthesis and worst-case success have equal minimum checkpoint alphabet: changing the encoder alone gives exactification. This static equivalence is credited, not claimed new. Symmetrization with an uncharged seed is neither needed nor used.

The source's static simplex-code optima overlap the Hadamard/Sylvester checkpoint results. Its statements dependent on a conjecture are not used as unconditional input. Its model does not charge all states used to compute the encoder from successive acquired symbols; our additive theorem and explicit full-support incompatible profile address that different question. No conclusion about arbitrary larger codebooks or sharp second-order streaming excess is inferred.

## Positive and residual realization

The article uses the classical positive-realization/invariant-cone background of Heller (1965) and Vidyasagar (2011), the probabilistic residual line of Esposito–Lemay–Denis–Dupont (2002), and the later Denis–Esposito treatment (arXiv:cs/0602093v1, Section 2 and Propositions 16,19). Residual generators and arbitrary normalized positive generators are different minimization classes. The new automaton definition internalizes stopping, proper state-language normalization and unreachable-state removal, and the finite-language separation is re-proved in that convention.

A new exhaustive proof audit of the original 2002 chapter, Heller or Norberg has not been completed. No theorem number or assertion of non-overlap is fabricated for an uninspected original passage. The classical invariant-section mechanism is acknowledged explicitly; the concrete two-cut family and additive transfer are the statements presented for further independent scrutiny.

## Nonnegative rank and incomplete specifications

Gillis–Glineur's nested-polytope viewpoint concerns static positive factorization; the current obstruction uses two different cuts whose independently minimal factorizations cannot be jointly executed. It supplies the example requested by r15, rather than treating an existence-of-transitions witness as a classification. Reusch–Merzenich's incomplete-machine setting remains distinct: our arrays are specified on the full alphabet. Full support of the obstruction family removes any need to choose an almost-sure completion.

## Classical coding exponent and remaining boundaries

The entropy exponent and logarithmic communication overhead are attributed to Ambainis–Nayak–Ta-Shma–Vazirani. The unchanged v30 proof remains valid, but exact checkpoint rows are not now presented as a different optimization objective. No new sharp second-order law, global adaptive collision optimum, unrestricted positive-rank classification, or independent A2/B4/C2 analytic closure is claimed.
