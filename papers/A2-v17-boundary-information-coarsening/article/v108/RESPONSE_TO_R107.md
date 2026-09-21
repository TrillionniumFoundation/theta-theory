# Response to the independent A2 v107 report

**Report:** `reviews/a2-v107-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md` at `b3d0c5ce18a5f6e4491ed70f50a6991ea846dcd8`.

**Baseline:** A2 v107, `a17d3cad6aeebe75f29102ecb2d1ef6784927f4e`.

**Revision:** *Contact tomography in Hankel information geometry*, A2 v108.

The report correctly distinguishes coexistence from interaction. This revision responds by changing the direction of the inverse problem: the native metric is recovered from the nonlinear cone's observed contact jets. The rank-one constraint is retained; no convex PSD replacement or arbitrary information-metric realization is used. All earlier mathematical source parts and proofs are preserved.

## R107.1 and R107.6 — An essential interaction theorem

The new principal theorem is `thm:general-tomography`, with proofs in `parts/00-general.tex`.

For the synchronized cone, its conormal union is the inverse image of the singular symmetric matrices under the adjoint measurement map. We classify all quadratic forms vanishing on that union. With two shared parameters the kernel is exactly the line spanned by the squared-determinant matrix `B_A`; with at least three shared parameters the kernel is zero. The proof uses the complete normal restrictions of inverse information, not only metric positive definiteness.

Separately, the Cauchy interpolation columns imply all three-site divided-difference relations, and a dimension argument proves that these relations characterize the entire native Hankel span. The two-parameter ambiguity disappears if and only if some three-site functional is nonzero on `B_A`. When they all vanish, the native second-jet fibre is exactly the corresponding affine line intersected with the native cone. Thus the native restriction has a necessary and sufficient downstream role, and replacing the native image by arbitrary positive metrics changes the identifiability theorem.

The theorem applies to any number of root pairs in the stated endpoint-free square-clock class. It is not merely a new numerical example. The explicit three-root corollary (`thm:tomography`) shows that five ordinary directional curvatures recover the native metric, gives an exact reconstruction formula, proves the sharp fixed/adaptive count, and exhibits both a rational transverse configuration and a nondegenerate exceptional loading.

For larger codimension, the count `2k-1` refers to **scalar dual second-jet queries** computed from the normal Hessian. We explicitly distinguish this from a count of raw directional derivatives or statistical samples. The theorem does not conflate equal second jets with equal full contact functions in the ambiguous case.

At unit total exposure the selected dual contact data are a linear isomorphism of native moment coordinates. The positive-Hessian budget region and its singleton/S1 design fibres therefore become an exact geometry of **observed contact data**. This is no longer a budget theorem placed beside a contact theorem without a logical link.

## R107.2 — One principal theorem and a visible hierarchy

The conormal rigidity theorem is the centre. Native interpolation and the synchronized contact limit are its inputs; the explicit five-curvature result, stability, and contact-data budget geometry are consequences. The endpoint inverse theorem is clearly identified as a companion. Finite-map reduction, divisorial certificates, weighted leading maps, tensor envelopes, explicit endpoint strata, local experiments, real resolution, and the binary inverse remain with complete proofs in appendices. The new dependency table records roles rather than a chronological sequence of referee rounds.

No earlier branch or source tree is deleted. Four prepared copies only expose assumptions and clarify descriptive scope; their theorem/proof environment counts are audited. The old positioning discussion is preserved as background for the companion results.

## R107.3 — Function-only inverse data at every stratum

The new `thm:intrinsic-fibre` takes a finite exact semialgebraic graph of the labelled scalar function. A finite polyhedral-quadratic atlas is an equivalent permitted input. It does not require a hidden matrix, endpoint count, or active-set names.

For each candidate endpoint dimension it gives the exact polynomial quantified formula for the entire normalized positive representation fibre. KKT necessity and sufficiency are proved, and real quantifier elimination produces a finite description, an emptiness decision, and an algebraic sample. Under a finite-representability promise, enumeration stops at the minimal endpoint dimension and returns all its representations. Without that promise the theorem still decides every supplied finite upper bound; it does not pretend that unrestricted failure detection follows from enumeration.

The inherited `thm:all-strata` remains explicitly a supplied-reference equality theorem. The new theorem upgrades the input category rather than retroactively relabelling that comparison test. Hardt triviality remains qualitative, and the explicit first-stratum normal forms remain stronger in explicitness than the general effective description.

## R107.4 — Direct inverse-parametric-programming comparison

The manuscript now cites and discusses Hempel–Goulart–Lygeros (2012) and Nguyen–Olaru–Rodriguez-Ayerbe–Hovd–Necoara (2017). The comparison identifies the supplied piecewise-affine optimizer/output map in those inverse-synthesis formulations, contrasts it with a scalar optimal-value graph, and distinguishes constructing a program from returning every minimal positive orthant representation.

It does not falsely claim that those papers assume a known hidden QP active fan. The parameter-only objective-addition example explains why reconstructing an optimizer representation alone cannot imply our value equality or minimality. This comparison is in the manuscript, not merely this letter, and is not an unsupported claim that no related inverse theorem exists.

## R107.5 — General reciprocal geometry versus native design structure

`lem:reciprocal-general` states the argument for any surjective linear map admitting a positive covector. Its strict-convexity proof, analytic minimizer, Hessian, and spherical level fibres are given independently of the binary model. The experiment supplies the reciprocal weights, fixed-clock moment matrix, and corank `2-e`.

The manuscript compares this with Harman–Filová–Rosa (2024), Lemma 1: direct fixed-information approximate-design equivalence gives affine nonnegative-weight fibres, hence polytopes. Here it is inverse nuisance-efficient information that is linear in **reciprocal** exposures; the unit budget is a reciprocal level, yielding spherical fibres. We do not claim that the abstract convex proof is uniquely model-specific or that the degree-minus-one reciprocal value is a norm gauge. The new downstream contribution is its transport to identifiable contact data.

## R107.7 — Tight statements and proof-level refinements

The abstract and definitions distinguish the full residual (free scores plus endpoint orthant) from its profiled rank-one image. Targets remain `b>=0`. The spanning margin is explicitly the least singular value of the linear measurement map on symmetric matrices. The uniform C2 perturbation class uses one fixed ball, bounded second derivatives, and a proved quadratic coercivity margin.

The moment-boundary discussion distinguishes the relative budget boundary, zero exposures, and the boundary of the closed finite moment cone. At fixed positive support, zero exposure sends the zeroth reciprocal moment to infinity; it is not the finite hypersurface `chi=1`. Circle statements are diffeomorphism statements.

The simultaneous-resolution proposition now exposes compact semialgebraicity, positive-time nonvanishing of J, the graph closure, and surjectivity after pruning in its statement. The missing-singleton paragraph spells out the e=3 pair ranges and the exclusion of spurious dependent pairs. The labelled-open-region argument for planar sign orientation is made explicit. The weighted-leading theorem remains a sufficient normal-form class. The overidentified example continues to exclude only the specified subdesign congruence.

## R107.8 — Exact-source native replay

The old native failure was traced to an undefined `\mathscr` command before reference convergence. The new preamble loads `mathrsfs`. The new build verifies exact bytes against its recorded source commit, checks inherited inputs against the pinned report commit, runs both the new and preserved finite checks, and evaluates the **final** log for unresolved citations/references, duplicate labels, and overfull boxes.

`evidence/verification.json` is the authority for the actual source SHA, build status, pages, hashes, and workflow URL. The workflow materializes prepared sources before choosing the compiled source commit, then writes a separate evidence-only commit on this revision branch. Source and evidence commits are not conflated. No success claim is inferred from a queued workflow, a first pass, or finite algebra alone.

## Evidentiary limits

These are new written proofs with finite exact diagnostic checks, not an independent acceptance decision or formal theorem certification. The principal theorem deliberately states its exceptional set and its oracle category. The response does not replace the requested mathematical strengthening by a lower venue target, a no-go disposition, or deletion of the difficult prior material.
