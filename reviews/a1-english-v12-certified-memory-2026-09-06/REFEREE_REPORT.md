# Referee report — A1, English revision 12

**Manuscript:** *Sparse observation algebras and certified memory across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation: REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted independent referee-style assessment, not a report commissioned by any of the named journals. The recommendation concerns this submission. It is not a claim that the principal collision law is false, that an identical theorem has been found elsewhere, or that the research program cannot succeed.

## 1. Submission and scope

```text
repository:        TrillionniumFoundation/theta-theory
revision branch:   revision/a1-english-v12-referee-response-2026-09-06
submission SHA:    71907d83ba4eb235949e2a929b4b7f85349e96e5
submission tree:   a1d1e43a25cd1d7652b4365dd8b952fdd9f56892
commit time:       2026-09-06T10:52:41Z
principal path:    papers/A1-english-v12/
controlling review:7492bf0d74236e866048ef9e5e5b28e4ea9a7f56
new review branch: review/a1-english-v12-harsh-referee-2026-09-06
```

The review is pinned to that commit, not to an indefinitely moving branch. I read the complete new construction/stability section, the effective and certified-resource sections, the introduction and comparisons, and the critical inherited experiment, transversality, confluent-positivity, Newton-flag, global-covering and causal arguments. The source index records the actual ranges and exclusions. Source labels identify mathematical locations; unverified PDF numbering is not used. [S0–S13]

I independently reconstructed the main probability and geometric reductions, the two stopping arguments, the dominated-prior uniformity argument and the two-point advice lower bound. I also executed exact-rational diagnostics against three byte-for-byte, Git-blob-verified source modules. Four nominal compiler runs passed the independent radius checks; four wrong-precision compiler mutations were accepted with false radius brackets; two truncated-horizon mutations were accepted and failed at the required second transition. A separate positive control confirms rejection of the old collapsed-transition mutation. [X]

I did **not** rerun the complete v10, v11 or v12 author suites, reproduce their aggregate assertion counts, rebuild LaTeX, inspect the rendered manuscript PDF, verify the entire preservation inventory, or certify every retained appendix. The 62-page build and preservation/test totals in the revision response remain author-reported in this review. The primary-source PDF pages identified in the source index were separately inspected; they are not the manuscript PDF. None of these activities constitutes formal proof verification.

## 2. Overall assessment

V12 contains a genuine mathematical addition, not merely a new response letter. It distinguishes a residual bound for a supplied program from a construction guarantee, derives stability of feasible-history states in finite moment data, specifies a legitimate dominated prior family, constructs one program from common imperfect advice, and supplies an actual positive-experiment uncertainty lower witness. The precision sentence and the version-specific citation have been repaired. These changes must receive credit. [S8–S12]

**No blocking counterexample or essential unfilled step was found in the examined principal mathematical theorem chain under its printed hypotheses.** In particular, the dominant prior family is not being silently substituted for the earlier arbitrary fixed full-support prior; the covering-profile comparison is not circular; exact collisions do not require division by a zero pivot; and the common-advice proof does not select an unsupplied true model. The new implementation findings below do not refute those statements.

Nevertheless, I do not recommend the submission at the requested level. Its strongest theorem remains the collision-uniform attainment of the full anisotropic prediction profile, together with the matching global cover and causal lower law. This is more than a Vandermonde identity. The new common-advice result is a useful interpretation of that geometry, but its additional mechanism is finite-dimensional perturbation stability followed by the existing covering construction and a floor in the stopping test. The sharp lower example has rank two and no additive collision. Neither that example nor the corrected implementation evidence establishes a further structural phenomenon at the difficult collision strata. The submission has not yet persuaded me that the complete contribution has the exceptional mathematical depth or reach required for the four requested journals. This is an editorial judgment, not an invented priority objection. Section 5 explains its basis.

There is also a concrete remaining problem with the claimed independent construction acceptance layer: its contract is not bound to the synthesis request. It checks internal consistency of a program using precision and horizon taken from the very program being checked. The resulting weaknesses are independently reproducible and can yield a false numerical certificate or an unusable returned program. They are not merely requests for more tests.

## 3. Disposition of the v11 report

| Earlier issue | V12 finding | Disposition |
|---|---|---|
| P11.1: collapsed transitions survive the old suite | A separately implemented nearest-centre/rounding contract is now called by both adaptive routines. My independent collapse control is rejected. | **Closed for that mutation.** The new precision/horizon findings are different faults, not a repetition of the old objection. |
| P11.2: no integrated adaptive physical diagnostic | The source now includes adaptive physical fixtures at exact, near and separated calibrations, with explicit finite-alphabet or exact common-command-line domains and an independent finite covering oracle. | **Addressed in source and author evidence.** I did not rerun the entire fixture suite. Full-cube or all-phase validation is not claimed and is not falsely demanded here. |
| P11.3: exact arithmetic described as additive precision overhead | The proof now states input/output accuracy separately from multiplicative, fixed-circuit intermediate bit lengths; an explicit denominator example is proved. | **Closed.** |
| P11.4: version/theorem-number mismatch | The linked arXiv v3 is correctly identified as Theorem 5.2 for discounted cost, rather than its average-cost Theorem 5.3. I checked the relevant PDF pages. | **Closed.** |
| E11.1: mathematical significance | A real common-advice theorem and positive lower witness have been added. | **Substantive response, but not sufficient for a positive editorial recommendation.** |
| E11.2: distinct meanings of certification | The mathematics distinguishes input accuracy, program residuals and covering-order construction. | **Improved.** The executable boundary must additionally bind the request, as P12.1–P12.2 show. |
| E11.3: preservation and organization | Complete historical material is retained and the new section is placed in the principal chain. | No deletion is requested. The complete preservation counts were not independently recertified here. |

These dispositions are deliberately asymmetric: a genuine repair stays closed even when a new fault is found. Earlier objections about discarded failure evidence, unattainable ambient dimension or uncharged historical access should not be recycled without new evidence. [S1–S12, R, L1]

## 4. Concrete findings

### P12.1 — The acceptance gate trusts the program's precision, producing false stopping certificates

**Severity: major certification-interface deficiency; not a counterexample to the printed mathematical theorem.**

**Locations:** `construction_contracts.py`, lines 54–84; `certified_compiler.py`, lines 174–201 and 205–239. The critical assignments are `bits = program.output_bits` and the use of those bits when independently rebuilding the numerical lists. Both adaptive routines request `b+2` places, but neither binds the returned program or the checker to that requested precision. The checker is therefore independent of the transition helper, but not independent of the program's declaration of the numerical experiment being checked. [S10]

I replaced the compiler call site by a wrapper that invokes the original compiler with `bits=0`. No distance, greedy-selection, transition or rounding helper was changed. The callback values are exact rationals, the command grids are valid, and the label budgets are unchanged. The resulting tables and representative histories are mutually consistent at the wrong precision. The checker accepts them and the adaptive routine then inserts their radii into a bracket whose error allowance is based on the requested mesh.

Use the same elementary compact system as the interval diagnostic:

\[
 U=[1/4,3/4],\qquad s_0=1/2,\qquad
 T(s,u)=(s+u)/2,\qquad Q(s)=s.
\]

Its one-step reachable interval is `[3/8,5/8]`, and its unrestricted M-centre maximum-norm radius is exactly `1/(8M)`. Here the history-net constant is `A=1/2`. The ordinary routine uses absolute tolerance `1/128`; the robust routine uses advice floor `1/128`. Every callback is exact, so this failure cannot be attributed to a false oracle certificate. [A, X]

| Routine | M | Final b | Requested bits | Accepted bits | Returned final radius bracket | True radius |
|---|---:|---:|---:|---:|---|---|
| `adaptive_compile` | 1 | 4 | 6 | 0 | `[7/16, 37/32]` | `1/8` |
| `adaptive_compile` | 2 | 7 | 9 | 0 | `[0, 5/256]` | `1/16` |
| `robust_adaptive_compile` | 1 | 5 | 7 | 0 | `[15/32, 69/64]` | `1/8` |
| `robust_adaptive_compile` | 2 | 7 | 9 | 0 | `[0, 5/256]` | `1/16` |

All four independent construction gates accept. All four brackets are false. In the M=1 cases the radius condition itself triggers, so the problem is not confined to the tolerance/floor exit. In the M=2 cases the numerical radius is zero, although the true radius is `1/16 = 16/256`; the upper certificate `5/256` is therefore explicitly wrong. The maximum query error over the tested grid is `5/8` for the M=1 mutations and `1/2` for M=2. The four corresponding unmutated controls satisfy every returned bracket. [X]

The logical defect is precise. The mathematical theorem assumes that state and query errors **including rounding** satisfy the prescribed tolerance. The checker currently certifies correct rounding to the program's self-selected scale, not compliance with that tolerance. Acceptance is subsequently used as though the latter had also been checked.

**Required correction.** Bind the checker to an immutable caller-supplied construction specification containing the requested precision or an independently derived rounding allowance. Check the returned metadata against it before rebuilding numerical lists. The rounding allowance used in a stopping bracket must be derived from this bound specification and the fixed input-error hypothesis, not from an unchecked self-description. Preserve the external-input-certification boundary: this does not ask the checker to prove an arbitrary oracle accurate. Add both fine-to-coarse and misleading-metadata negative controls at the adaptive call sites, with an independently known true radius.

I have not claimed that the full author suite passes this new mutation. I executed the attached independent probes. Nor does the unmodified compiler spontaneously choose zero bits; this is a fault-injection counterexample to what the acceptance layer currently excludes.

### P12.2 — A requested two-stage program may pass as a one-stage program

**Severity: structural request-validation deficiency in the same acceptance layer.**

At line 69 the checker obtains `T` from `len(program.transitions)`. It checks that the audit, outputs and state counts have lengths consistent with that inferred T. It is not supplied the horizon requested by the adaptive caller. Thus a self-consistent shorter construction is accepted as a result of a longer request. [S10]

I requested horizon two and wrapped the compiler so that it invoked the unchanged implementation with horizon one. The exact finite command alphabet is `{1/4,1/2,3/4}`, with the same recursively evaluated state update. Because this is the complete command alphabet, the command discretization error is zero. Both adaptive entry points return a one-transition program after all their construction gates accept. Executing its first transition succeeds; executing the required second transition raises `IndexError`. This is a concrete failure of the requested runtime contract, not a matter of choosing a loose mathematical error constant. [X]

**Required correction.** Supply and enforce the requested horizon, stage dimensions and query interface independently of the returned table. A program may not redefine these by omitting its final stages. Treat this and P12.1 as two consequences of one architectural issue: internal consistency is weaker than conformance to an external synthesis request. There is no need to redesign the collision theorem or to enlarge the persistent-state budget to repair it.

### P12.3 — The new physical common-advice conclusion is not yet tested end to end

**Severity: limited evidence gap, not an analytic objection or a reason to demand full-cube enumeration.**

The revised physical diagnostics call the ordinary `adaptive_compile` on one actual model at a time. The calls to `robust_adaptive_compile` in `robust_floor_tests` use a scalar interval example and compare two shifted systems. The positive monomial uncertainty witness is then checked separately through moment and query formulas. This is useful component evidence, but it is not the execution of one robustly compiled physical program from a single imperfect moment table against multiple compatible monomial experiments. [S11]

For the next evidence package, one modest such fixture would be more informative than more repetitions of the same component checks. Freeze one common moment name; use it to construct one program; evaluate that identical program against two explicitly compatible physical models using independent exact truths. Record the requested tolerances, actual query discrepancies and stopping bracket. A finite command subexperiment is adequate. A pair crossing an additive equality would be particularly relevant, but an asymptotic simulation or enumeration of the full command cube is not required. This request concerns evidence for the new flagship corollary, not a hidden extra hypothesis for its proof.

## 5. Mathematical significance at the requested level

### E12.1 — The geometric theorem is the contribution; the new safeguards are not a second foundation

The author correctly identifies the non-routine input: actual positive histories attain the entire collision-normalized flag, uniformly on a compact calibration chamber and for every fixed full-support prior, while a separate bounded-format argument supplies the global cover. I agree with that identification. The normalized tangent, acquisition probability and causal compatibility matter. A spectral estimate alone would not supply them. [S3–S7]

My reservation is about the depth and consequences of the resulting classification, not about whether the author has named its mechanism. Once the flag attainment and global cover are available, the prediction lower bound is a finite-dimensional volume argument, causal realization is a fixed-horizon Lipschitz recurrence, and the precision selector is a greedy-radius bracket. V12's common-advice extension adds a finite rational perturbation estimate and a floor to that selector. These are coherent deductions, but the additional steps do not substantially deepen the collision geometry. The audit gives the dependency calculation rather than merely labelling it routine. [A]

The comparison proposition concerning a truthful residual bound is correct and useful for preventing a mistaken inference. Its collapsed interval example separates two assertions about arbitrary programs. It does not separate the paper's geometric theorem from a strongest existing approximation theorem, and it is not itself evidence of an exceptional new mathematical principle. The revision does not expressly claim otherwise; it should not rely on that proposition to carry the editorial significance argument. [S9]

Likewise, the statements about exact rational workspace and the newly independent verifier are repairs and implementation specifications. They cannot be counted as independent mathematical advances merely because they occupy named-result environments. The manuscript generally acknowledges their classical character; that honesty should be preserved.

### E12.2 — The uncertainty lower witness has a narrower scope than the upper theorem

The positive detector in `prop:advice-floor` is a legitimate and clean witness. Its lower bound is unconditional after a positive-probability report event and uses the same advice in both experiments. However, it has `r=2`, `N=2`, one attainable direction and no additive exponent collision. It proves that a `delta^2` uncertainty term can be necessary in this physical framework; it does not characterize the uncertainty modulus at a general colliding model or prove a sharp noisy-collision classification throughout K. [S9, A]

The author does not claim such a universal lower theorem, so this is not a false-statement finding. It does limit how much new mathematical force the consequence adds to the complete submission. A sharper understanding of ambiguous finite moment names at actual collision strata would be one possible substantive direction within the existing program. It is not an instruction to assert an unproved theorem or to abandon the current results. A different persuasive consequence of the attained geometry could serve the same editorial purpose.

### E12.3 — The decision concerns the whole submission, not a repair checklist

Specialization by itself is not disqualifying, and using classical tools is not a defect. Nevertheless, the principal results here are formulated at fixed horizon and fixed finite format, with constants allowed to depend on the prior, positivity and horizon. The supplied difficult examples organize a finite exterior-volume profile into resource phases; the new uncertainty consequence uses generic finite-horizon stability. On the evidence and proofs examined, I regard the work as a technically careful specialized classification with useful constructive consequences, rather than a demonstrated advance of exceptional general-mathematical significance.

This assessment does not impose an infinite-horizon theorem, a uniform theorem over all full-support priors, a nonmonomial theory, or a universal precision/program-size converse. Those would change the task and are not conditions smuggled into this review. Equally, fixing P12.1–P12.3 will remove those specific objections, not by itself justify acceptance at the requested level.

## 6. Decision and requirements for another response

I recommend neither acceptance nor minor revision at the requested four-journal level. The examined mathematical chain survives this audit, but the claimed acceptance interface still permits demonstrably incorrect certified outputs, and the complete significance case remains unpersuasive to this referee.

A useful next response should bind numerical and structural request data independently of the returned program; reproduce and reject both new mutations without weakening the true-radius checks; retain the successful old collapse control; add the modest common-advice physical execution described above; and explain what substantive conclusion of the collision-uniform attainment theorem carries the paper's mathematical importance beyond generic stability and resource bookkeeping. Closed prior corrections should remain closed.

No arbitrary deletion of established proofs, replacement of the full profile by a weaker floor, prior-density assumption, or abandonment of the research direction is requested. No finding in this report should be converted into a claim that an unmodified numerical program fails a theorem whose hypotheses it satisfies.

---

Detailed calculations: [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md).  
Pinned sources and reading boundaries: [SOURCE_INDEX.md](SOURCE_INDEX.md).  
Executed independent results: [EXECUTION.json](EXECUTION.json).  
Reproduction script: [reproduce_review.py](reproduce_review.py).
