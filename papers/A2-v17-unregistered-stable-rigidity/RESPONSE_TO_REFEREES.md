# Response to the external A2 v16 report

**Manuscript:** *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*, A2 v17.  
**Report:** `reviews/a2-v16-external-harsh-top4-rereview-2026-09-28/REFEREE_REPORT.md`, frozen at `62c98e9178c5571a19afaccf8b5e67fc892c6c1e`.  
**Reviewed v16 head:** `9b0f76a32d1296b4035b52e43a38b3e3ffb50f18`.

We thank the referee for distinguishing the correctness audit from the significance assessment. This revision addresses the two central mathematical objections—supplied gluing information and absence of a finite-data global inverse—rather than changing the subject or deleting the established results. The previous registered rigidity theorem, the complete local inverse and physical realization, the count-fiber statements, and the full smooth supplement remain in the submission.

## Mathematical advance

**Unregistered reconstruction (Theorem 7.2).** Each selected edge is observed only up to its own reversal, independently of all other edges. A local law reconstructs an entire analytic obstacle pair. If the source obstacle has trivial Euclidean symmetry group, its matching to an already reconstructed copy is unique. Spanning-tree propagation therefore recovers the cross-channel contact registration and relative signs that v16 supplied. Non-tree pairs determine translation displacements, and two independent integer cycle labels recover the marked lattice. For noncircular, possibly symmetric obstacles, the same argument gives a finite candidate bound by the product of source symmetry-group orders. Loops, backwards traversal and nonunimodular cycle markings are included. Proposition 7.4 supplies a nonempty open physical class. The observation still includes local contact origins, obstacle labels, and integer copy labels; it is not an ordinary marked length spectrum.

**Finite noisy-window reconstruction (Theorem 8.1).** On a uniform analytic class with geometric and asymmetry margins, a finite experiment estimates onsets rather than receiving exact limits. A threshold grid gives an onset error of order square-root noise. Positive-node interpolation estimates the required raw moment coefficients; finite triangular inversion recovers the jets. A proved continuation lemma propagates contact-arc error to the entire boundary, quantitative shape matching aligns different experiments, and a displayed matrix bound controls the lattice. The error has the form `C(A_K epsilon^(1/(ceil(K/2)+2)) + B q^K)^theta`, with an admissible slowly increasing order. A charged fresh-preparation bound covers the adaptive two-stage experiment and all failures. No uniform-in-order conditioning, optimal exponent, or computation-time bound is assumed.

## 1. Registered-data equality

Definition 6.1 now uses an abstract oriented metric circle for each boundary, whose perimeter is first recovered by local analytic determination. All half-edge occurrences are explicitly labelled; a loop has separate source and target occurrences. Equality is defined by graph identification and metric-circle isometries preserving reference origins and occurrence points, with the same orientation sign for all circles and edge laws. Thus a numerical residue modulo an unrecovered perimeter is not used as a hidden datum. The displacement formulas now use separate half-edge contact symbols also for loops.

## 2. Exact germs are not finitely many numbers

The introduction and global theorem now say **finite collection of exact germs and limits**. The text explicitly states that the germs contain infinitely many coefficients and that this collection is neither finite-dimensional data nor a finite-sample observation. The finite experiments are stated separately in Sections 8, 10 and 11.

## 3. Supplied coherence and its removal

Immediately after Definition 6.1, we count at most `2|E|-|V|` circle-valued registration entries and `|E|-1` relative edge lift choices, allowing reductions from stabilizers and physical constraints. These are entries, not asserted independent physical coordinates. Definition 7.1 then removes both kinds of inter-experiment information. Theorem 7.2 recovers them by complete-image matching under its shape hypothesis, while the general registered theorem is retained without that hypothesis.

## 4. Parameter-differentiated filtration

Lemma 4.1 now writes the parameter-dependent integral on the fixed Morse disk. The substitution `X -> -X` gives evenness for every parameter, and uniform mixed derivative bounds justify differentiating that identity and extracting coefficients. This does not assume symmetry of the nonlinear Morse map or lower jets. The proof also distinguishes compact finite-jet coefficient boxes from the higher smooth bounds actually needed for uniform Taylor remainders on a common collar.

## 5. Exact analytic count-only scope

Section 9 is retained byte-for-byte. Its finite analytic fibers, formal recursion, and smooth physical realizations with equal count Taylor series are not described as exact analytic count-law counterexamples. Remark 9.3 remains explicit. The new mathematical advance instead concerns the unregistered marked law and its conditional global stability; it does not infer convergence of a formal count-only inverse.

## 6. Exact rigidity and statistical observation

The old fixed-dimensional experiment remains in its original scope. Section 8 adds a different theorem on an infinite-dimensional uniformly analytic physical class. It includes noisy onset localization, curvature and area calibration, analytic continuation, synchronization and lattice inversion, with each loss shown separately. The endpoint sensor remains present; its bounded moments are not called count-only data. The admissible-class estimator is Borel and consistent, but is not advertised as a fast algorithm.

## 7. Commit-bound full-package build

A new read-only workflow checks out the exact triggering revision and runs `tools/run_validation.py --all-volumes`. The validator checks the preserved supplement tree before execution, builds both cross-referenced supplementary documents twice in a staging copy, inspects final logs, checks source immutability, and records the actual commit, tree, runner, commands, exits and hashes. It never repairs sources or pushes from CI.

The actual local execution passed 6,938 finite checks and a warning-free 29-page primary build. It was source-content execution, not an authenticated checkout, and did not rebuild Supplement S. The receipt retains that limitation. The hosted requirement is closed only by an actual passing workflow conclusion on the published candidate; a newly defined, pending or queued workflow does not close it. No earlier v16 pass or page count is reused as v17 hosted evidence.

## 8. Theorem-specific literature comparison

Section 1 retains the six primary billiard comparisons and adds the conditional continuation reference of Trefethen, BIT 60 (2020), 901–915. The intrinsic observation is explained as a Liouville-measure pushforward invariant under Euclidean isometry, with specified local marks. Its information richness is not denied or equated with the marked length spectrum. The advance is the removal of continuous cross-channel registration and relative signs, together with finite-data recovery under quantitative analytic assumptions. Our periodic-strip continuation lemma is proved in the article; we claim neither exhaustive priority clearance nor an optimal continuation or inverse rate.

## Preservation and reassessment

The whole reviewed v16 directory is retained as an immutable history tree, and the full smooth Supplement S remains part of the package. Seven active core files are unchanged by Git blob identity. The revised primary is theorem-led, with assumptions, proofs, examples and distinctions between exact and statistical data in the mathematical text; operational evidence is kept outside it. The Annals/Acta/Inventiones/JAMS target is unchanged. Whether the new theorems meet that editorial threshold remains a matter for independent referee and editorial assessment, not something certified by this response or by arithmetic diagnostics.
