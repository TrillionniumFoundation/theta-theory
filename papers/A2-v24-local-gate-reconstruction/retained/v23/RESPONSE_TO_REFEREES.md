# Response to the v22 referee report

**Manuscript:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Report:** `ecfe49c9ab244ade504c9a727a4d110f72db4433`, report blob `c6a72684714f01f99f0600fff1413a85c87c39a9`  
**Reviewed author head:** `ef51836da1744fc4a7133e3a3fd0e85848c73dc6`  
**Revision:** A2 v23, 29 September 2026

We thank the referee for separating the audited correctness of the completion identity and reference-free arithmetic from the acquisition, normalization and information-category questions. The present revision retains those results and the topic. It adds an operational unknown-cell preparation, carries its error through the finite experiment, and proves time-uniform soundness and finite stopping for a growing record catalogue under explicit arrival assumptions. A randomized version of the geometric scanner realizes those assumptions. Its geometric access is not disguised as information obtained from unmarked trajectories.

The principal new result is Theorem 1.1, proved as Theorem 7.1 and Corollary 7.2. Its proof includes Proposition 5.1 (unknown-cell preparation), Lemma 5.2 (histograms with preparation bias), Lemma 6.1 (small saturated witness without a primitive pair), Lemma 6.3 (adaptive discovery hazards), Proposition 6.4 (geometric realization) and Proposition 6.5 (pointwise local-margin exhaustion). The local inverse, exact defect and finite-error certificate remain self-contained in Sections 2–4, with their three source files unchanged.

## 1. A certificate does not acquire records

The abstract and Section 1 state this distinction. The new theorem no longer begins with a fixed finite complete list. Before each validation epoch a producer may add one genuine replayable record or no record, using the previous history. The learner retains repetitions, validates the current list with fresh data, and stops only after the physical completion test succeeds.

Soundness needs no discovery assumption. Termination needs an unknown finite saturated witness whose records have divergent cumulative conditional discovery hazards. These hypotheses are formalized in Definition 6.2, rather than hidden in a claim of eventual enumeration. Under a common positive hazard p, the stopping tail is bounded by the current epoch error plus w exp(-pk). Neither the witness nor p is an input to the stopping decision.

Proposition 6.4 proves one realization using the retained geometric primitives, with a bounded body-list size and a positive probability of proposing every required bridge. It does not establish the stronger claim that an unmarked trajectory observer with no geometric access generates genuine normal-channel gates. The new result closes adaptive discovery and stopping for the explicitly stated producer class, not for every possible observer.

## 2. Reference-free is not prior-free

The abstract, introduction and Section 4 list the obstacle-count bound, positive free/body-area and covolume bounds, bounded lattice presentation, analytic strip and graph bounds, quantitative shape/asymmetry separation, and local physical margins. The new sampler additionally uses a bound on a fundamental-parallelogram diameter, not its vectors or location.

Proposition 6.5 separately treats pointwise exhaustion of unknown local margins. Its level-dependent sample sizes may deteriorate arbitrarily; the uniform polynomial schedule and expected-cost statement are not transferred to that exhaustion. Global analytic and separation priors remain. Thus the revision adds a pointwise extension without deleting the conditions needed for a uniform rate.

## 3. Operational absolute normalization with an unknown cell

Section 5 supplies a precise apparatus: choose laboratory positions uniformly in [-L,L]^2, reject solid positions, choose a uniform direction on each accepted free launch, and retain every record outcome including failures. No primitive cell, full obstacle list or successful-return normalization is used in this preparation.

Proposition 5.1 proves, by complete-cell and boundary-tile decomposition, that the projected free-launch law is within 8 V1 b/(A0 L) in total variation of the ideal quotient Liouville law. It also bounds free-launch acceptance and charges rejected launch attempts. The finite experiment is not called an exact cell sampler. Lemma 5.2 amplifies the total-variation bias through cell averages and two derivatives, adding tau_L h^-4 to the density error. Choosing a sufficiently large launch square retains the fixed-list rate.

The periodic-gate condition is essential and explicit: the gate recognizes all translated occurrences of a selected local branch. A detector attached to only one physical copy is excluded. The geometric producer may install such gates by comparing complete pair images, but that is an access primitive, not a consequence of the box-sampling proof. No mixing assumption or finite-horizon condition is introduced.

## 4. Separate the statistical statements

Sections 7.2 and 8.3 distinguish (a) the conditional fixed-list whole-table upper bound, (b) the new stopping-time and proposal-cost bounds, and (c) the retained fixed-window hidden-area N^-1/2 decision scale. They have different parameters, losses and observation contracts. The manuscript does not call their combination a sharp whole-table recovery rate.

The explicit epoch budget delta/[8(k+1)^6] gives simultaneous validity over the infinite horizon. Its decay is also strong enough to give finite expected launch cost under uniform discovery hazards; a merely summable but too slowly decaying validation budget would not justify that conclusion. Proposal work, accepted preparations, rejected launch attempts and spatial aperture are separately identified.

## 5. Preserve failure-closed decisions

Rank deficiency, unresolved rational arithmetic, insufficient precision and a failed defect test all return a noncertificate. They do not assert that no table exists, that another component cannot certify, or that acquisition is exhausted. On the simultaneous accuracy event, the deterministic omission-safe certificate applies to every data-selected component and deletion of the accumulated list.

Arbitrary deletions preserve soundness but can destroy termination. The latter theorem explicitly retains all witness records once acquired. Empirical fitting never substitutes for the producer's genuine-branch validity. The integer subgroup is still recovered before area calibration, and noisy real vectors are never directly treated as an integer lattice basis.

## 6. Catalogue countability and computational status

Section 6.3 distinguishes three notions. A fixed periodic table has countably many copy pairs and a countable sufficient set of rational-window descriptors. This is not an enumeration of arbitrary analytic density functions. With the stated body/clearance oracle, increasing finite apertures and descriptor refinements give an oracle-relative enumeration. Without those primitives, countability alone implies neither effective acquisition nor a complexity bound.

Lemma 6.1 bounds a sufficient witness by r0+1+floor(log2 Q) records. The argument retains a spanning tree and independent cycle pair, then halves the lattice index at every strict subgroup enlargement. It explicitly covers the 2/3/5-minor example where no recorded pair is primitive. The arithmetic is finite once its rational inputs are separated. Continuous analytic fitting remains a measurable compact-class existence construction.

## 7. Retain theorem-level inverse-geometry comparisons

Section 8 keeps the primary comparison with Stefanov–Uhlmann–Vasy, Gurfinkel–Noakes–Stoyanov and Noakes–Stoyanov: unknown ambient metrics or exterior travelling times versus local reflecting arcs, selected endpoint laws and absolute normalization. Proposition 2.2 retains the exact local action/normalization equivalence. Santaló-type volume relations are distinguished from the finite-square preparation argument.

Time-uniform confidence is now compared with Howard–Ramdas–McAuliffe–Sekhon. The proof uses elementary error spending and fresh conditional validation, not a claimed new concentration principle. Proximity-graph and Hermite/Smith comparisons are retained with their actual computational scope. The literature audit records primary sources and does not claim exhaustive priority.

## 8. Exact-source qualification

The revision supplies its own source pins, read-only validator, native retained tree references and exact-triggering-SHA workflow. The primary-only local execution reruns the new and selected retained diagnostics in normal and optimized Python, checks identical output, compiles the complete primary and records actual logs and hashes. It is labelled source-content execution, not a Git checkout or a hosted all-volume pass.

The hosted mode requires a clean exact checkout, verifies the whole retained v22 and Supplement S trees, runs the unchanged v22 checker in a staged copy, and builds the primary plus five retained entry documents. It records failures as failures. Its actual run conclusion must be checked separately; source publication or a queued workflow is not reported as successful hosted qualification. Neither the original reviewed v22 files nor their historical receipts are rewritten.

## 9. Focused primary and complete preservation

The primary follows one chain: local inversion, omission-safe completion, unknown-cell phase preparation, growing-catalogue discovery and stopping. It contains all proofs needed by that chain. The exact entire reviewed v22 paper tree is supplied as Supplement C at retained/v22, including its prior v21/v18 material, statistical testing and all historical inputs. The complete relative-law Supplement S is also preserved by its original tree identity.

The older moment, registered symmetric/repeated-shape, count-fiber, relative-law and auxiliary experiments are not deleted, weakened or presented as published outside this submission. They remain explicit companions with a reading map. No full-law result is reinterpreted as exact analytic count-only rigidity or nonrigidity.

## Scope of the response

The manuscript advances the acquisition analysis within the intrinsic endpoint-law programme. It does not infer an editorial decision from a finite diagnostic count, a compilation result or a fixed upper-bound exponent. The strongest remaining observer question—genuine record production from unmarked trajectories alone—is not silently declared solved by granting the producer geometric access. The new propositions and stopping theorem are stated for the access and priors actually used in their proofs.
