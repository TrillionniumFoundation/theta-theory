#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

DATA={
"A1-exact-benchmarks": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"A1_MAPPING_TORUS_ONE_SIDED_RESPONSE.tex",
 "items":[
  ("False bilateral directional Lasota--Yorke inequality", "Replace the bilateral inverse-shift estimate by two one-sided Ruelle operators on future and past tails; the translated-cylinder counterexample is included as a regression test.", "lem:r10-a1-one-sided; cor:r10-a1-resolvent"),
  ("Physical section confused with symbolic natural extension", "Keep the square as the Liouville section and the two-sided shift only as a measurable coding extension.", "thm:r10-a1-factor"),
  ("Hybrid reset called one autonomous Hamiltonian", "Use the exact symplectic mapping torus; the global autonomous Hamiltonian is H=E on the quotient, so no external reset is applied.", "thm:r10-a1-suspension"),
  ("Undefined products of seam currents", "Use typed Hadamard cut derivatives between graded trace spaces; intersections are represented by ordered traces, never by multiplying distributions.", "lem:r10-a1-currents"),
  ("Physical and symbolic response mixed", "Transport observables through the coding maps and differentiate the commutative physical/symbolic diagram.", "thm:r10-a1-response"),
  ("Mechanical valuation overclaim", "Retain the identification only under equality of canonical likelihood cocycles.", "thm:r10-a1-work"),
 ]},
"A2-sinai-homological-pressure": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"A2_EXPLICIT_CERTIFICATE_FOURIER_RANGES.tex",
 "items":[
  ("Birth bundle undefined across the no-branch side", "Use one-sided physical coefficients and a renormalized fold chart; no inverse of a vanishing current is asserted.", "lem:r10-a2-birth"),
  ("Moving-billiard spectral theorem only sketched", "State one uniform graph theorem with expansion, distortion, multiplier, compactness, and trace-mode exclusion on the renormalized bundle.", "thm:r10-a2-spectral"),
  ("Arithmetic determinant not computed", "List triangular/rhombic certificates and verify the determinant with a checked lower bound on the parameter interval.", "lem:r10-a2-arithmetic; A2_ROUND10_CERTIFICATE.json"),
  ("UNI inferred from a picture", "Construct two returned inverse branches on a common interval and compute the temporal-distance derivative including moving endpoints.", "thm:r10-a2-uni"),
  ("Dolgopyat tail not Fourier integrable", "Split compact, Gaussian, Dolgopyat, and very-high-frequency ranges; the last uses enough roof derivatives for an integrable tail.", "thm:r10-a2-four-range"),
  ("Sharp-window formula exceeds central LLT", "Prove a density LLT and state local/central/saturated/macroscopic regimes separately with the correct sum-window factor.", "thm:r10-a2-llt"),
 ]},
"A3-full-empirical-path-ldp": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"A3_DETERMINISTIC_SPEED_PROJECTIVE_FLOW_LDP.tex",
 "items":[
  ("Random total return time used as LDP speed", "Use deterministic block count N for the induced LDP and deterministic collision/physical horizons after clock contraction.", "thm:r10-a3-finite; thm:r10-a3-main"),
  ("State did not retain branch/edge information", "Retain vertices, admissible edge flow, return/roof marks, and actual excursion profiles.", "lem:r10-a3-state"),
  ("Projective rate and compactness unproved", "Build finite-core Markov rates, exponential tightness, and the projective supremum rate.", "thm:r10-a3-finite; thm:r10-a3-projective"),
  ("Recession functional defined circularly", "Define it by actual long-excursion epigraph limits and prove liminf plus legal recovery.", "thm:r10-a3-recession"),
  ("Clock inversion discarded terminal excursion", "Retain the terminal profile and quantify its sublinear effect.", "lem:r10-a3-clock"),
 ]},
"A4-history-memory-universal-pressure": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"A4_DOOB_PAST_KERNEL_MEMORY.tex",
 "items":[
  ("Claimed martingale difference was not centered", "Solve the correctly oriented Poisson equation and use g+h_g-P h_g.", "lem:r10-a4-poisson"),
  ("Stable/future quotient still deterministic", "Condition on a genuine past-only natural-extension history and construct its nondegenerate future kernel.", "thm:r10-a4-feller"),
  ("Conditional rough theorem only asserted", "Use uniform conditional moments, Lindeberg, bracket convergence, and singularity-shield truncation.", "thm:r10-a4-quenched"),
  ("Normalized Feynman--Kac ratio not a semigroup", "Normalize by the positive eigenfunction and eigenvalue, producing an exact Doob semigroup.", "thm:r10-a4-doob"),
  ("Finite descriptor omitted unresolved Q-space / sign issue", "Retain the full Q-space and add finite principal-part modes; use Khat=zP-PLP-C(z)^{-1}.", "thm:r10-a4-memory"),
 ]},
"B1-microcanonical-preparation": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"B1_INTERIOR_SADDLE_REGENERATIVE_SHELL.tex",
 "items":[
  ("Shell theorem covered exponentially rare targets", "Restrict to regular interior targets satisfying affine-span and moderate-width conditions.", "cor:r10-b1-saddle; thm:r10-b1-shell"),
  ("Covariance derived from a fixed rare particle sector", "Use linearly many typical insertion cells under the compound law.", "lem:r10-b1-covariance"),
  ("A local full-rank patch was mistaken for global smoothing", "Use linearly many regenerative full-rank blocks; the event of too few good blocks is exponentially small.", "lem:r10-b1-goodblocks"),
  ("Minor/large Fourier arcs uncontrolled", "Decompose into central, lattice minor, regenerative smooth, and exponentially small bad-block sectors.", "thm:r10-b1-characteristic"),
  ("Fixed source saddle", "Center at the exact source-dependent finite-volume saddle and then pass to the limit.", "thm:r10-b1-shell; thm:r10-b1-main"),
 ]},
"B2-collision-clusters-dynamic-ldp": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"B2_COMPATIBLE_TRACE_INTEGRATED_JACOBI_LDP.tex",
 "items":[
  ("Interior/boundary measures were independent and incompatible", "Define the closed graph of the kinetic transport operator with its normal trace and Green identity.", "thm:r10-b2-trace"),
  ("Trace hierarchy semigroup unconstructed", "Build the positive boundary-renewal semigroup on the factorial graph product.", "prop:r10-b2-renewal"),
  ("QR reset hid physical singular values", "Remove QR reset and prove an integrated flux-weighted small-singular-value estimate for the true Jacobi map.", "lem:r10-b2-jacobi; thm:r10-b2-surplus"),
  ("Future deleted after surplus contact", "Keep the true post-collisional future and sum all later contacts by the renewal semigroup.", "thm:r10-b2-surplus"),
  ("One-block source theorem asserted", "Compare the exact and Boltzmann renewal Duhamel expansions with explicit tree/cycle/multiple-event errors and mesh consistency.", "thm:r10-b2-block"),
  ("Balance-preserving smoothing absent", "Use conservative shell retraction, positive background, finite-cell incidence repair, and exact weak balance.", "lem:r10-b2-repair"),
  ("Full lower bound incomplete", "Expose smooth positive balanced pairs and pass to all finite-action pairs through the conservative recovery.", "thm:r10-b2-main"),
 ]},
"B3-hamilton-boltzmann-cotangents": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"B3_COVARIANCE_FIRST_GAUGE_PROCESS.tex",
 "items":[
  ("Indefinite perspective Hessian treated as a metric", "Acknowledge the sign-indefinite term and prove short-time coercivity directly on the balanced tangent by an energy estimate.", "thm:r10-b3-linear; cor:r10-b3-curvature"),
  ("False multiplier curvature", "No curvature is attributed to the linear balance multiplier; the actual constrained second epi-derivative is used.", "cor:r10-b3-curvature; thm:r10-b3-mosco"),
  ("Closed range/gauge asserted", "Prove backward micro--macro observability in the B2 Green graph and invoke the closed-range theorem.", "thm:r10-b3-gauge"),
  ("Covariance/action circularity", "Construct covariance from exact finite cumulants first, then identify the rate's second epi-derivative by finite-dimensional conjugacy and Mosco passage.", "thm:r10-b3-finite; thm:r10-b3-mosco"),
  ("Process tightness lacked time-local estimates", "Root connected graphs at an anchor time and integrate tree-decaying relative-time cumulant densities.", "lem:r10-b3-cumulants; thm:r10-b3-main"),
 ]},
"B4-nonlinear-kinetic-semigroups": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex",
 "items":[
  ("Law and observable semigroups conflated", "Separate microscopic flow, Koopman observables, dual push-forward laws, ensemble log-Laplace values, and the limiting semigroup.", "prop:r10-b4-tower"),
  ("State resolvent applied to observables", "Use the observable Koopman resolvent and its Hille--Yosida graph identity.", "thm:r10-b4-core"),
  ("Order-j propagator did not close", "Solve one terminal equation on the full triangular product hierarchy and prove normal graph summability.", "lem:r10-b4-corrector"),
  ("Microscopic nonlinear generator ill-typed", "State convergence for corrected ensemble pressure derivatives, not for a deterministic law generator.", "thm:r10-b4-hamiltonian"),
  ("Initial preparation double-counted", "The transition action is dynamic only; preparation appears once at the initial boundary.", "thm:r10-b4-action"),
  ("Comparison penalty either noncoercive or leaves source core", "Use a coercive Tataru distance with fixed slope cutoff, send the diagonal scale first and source cutoff second.", "thm:r10-b4-comparison"),
  ("Truncation limit formal", "Use entropy coercivity, exact balance repair, local uniform semigroup convergence, and viscosity stability.", "thm:r10-b4-main"),
 ]},
"C1-information-risk-sensitive-saddles": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"C1_STRATIFIED_EVIDENCE_FILTERING.tex",
 "items":[
  ("Observation-current tower not closed", "Construct an arbitrary-codimension normal-current tower with oriented intersections and B2-compatible prediction.", "thm:r10-c1-tower"),
  ("Posterior not Feller at zero evidence", "Retain unnormalized current, projective direction, and log evidence; compactify directions rather than normalize the zero current.", "lem:r10-c1-evidence; thm:r10-c1-dpp"),
  ("General observation lacked coefficient theorem", "Restrict to the declared finite coarea family and prove a uniform joint constraint-observation coefficient.", "thm:r10-c1-coefficient"),
  ("Reachable chaos class circular", "Define it as the closure generated by preparation, controlled prediction, and observation updates; prove its connected hierarchy estimate inductively.", "lem:r10-c1-chaos"),
  ("Reduced game/BvM unsupported", "Use kernel convergence on the reachable class and the exact finite-centred B3 tangent.", "thm:r10-c1-main"),
 ]},
"C2-cotangent-rigidity-tangent-representations": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"C2_COMMON_TRANSFER_BUNDLE_COTANGENTS.tex",
 "items":[
  ("Null sets were not linear spaces", "Use closed linear spans of rational/all-time coboundaries, with constants separated for pressure equivalence.", "thm:r10-c2-null"),
  ("Cesaro averaging lacked uniform moments", "Prove platform-specific uniform averaged Lyapunov bounds before applying weighted tightness.", "lem:r10-c2-cesaro"),
  ("Kato ODE lost regularity / RN trivialization invalid", "Work on one fixed transfer Banach bundle using a smoothing Kato connection; do not identify infinite-path measures by densities.", "thm:r10-c2-kato"),
  ("Resolved Hilbert projection not constructed", "Construct the correlation Hilbert realization and its resolved projection separately from the transfer eigenline.", "thm:r10-c2-memory"),
  ("Memory zeros/domains ignored", "State covariant formulas on the common resolvent set and track transmission zeros/descriptors.", "thm:r10-c2-memory"),
  ("Optional projection and nonlinear pullback ill typed", "Use the A4 past filtration and the derivative of composition by a nonlinear observable map.", "thm:r10-c2-optional; thm:r10-c2-main"),
 ]},
"D1-deterministic-theta-contractions": {
 "report":"REFEREE_REPORT_ROUND9_GPT56_PRO.md",
 "source":"D1_MICROSCOPIC_PHASE_DISINTEGRATION.tex",
 "items":[
  ("Phase labels were tilted laws, not an exact physical disintegration", "Construct positive finite-volume component measures from measurable phase basins/projectors on one common sample space.", "thm:r10-d1-mixture"),
  ("Minimum component rate assumed", "Prove a subexponential microscopic mixture LDP; the rate minimum follows from the exact component sum, not from pressure conjugacy.", "thm:r10-d1-mixture"),
  ("Zero-free charts incompatible with coexistence", "Use phase-restricted analytic charts and allow Lee--Yang pinching after labels are contracted.", "thm:r10-d1-charts"),
  ("Projective/topology recovery assumed", "Prove component exponential tightness, face recovery, and labelled Dawson--Gartner passage before contraction.", "thm:r10-d1-projective"),
  ("Uniform shell coefficients missing", "Integrate the phase-local coefficients with the prior rate and treat phase-boundary degeneracy separately.", "thm:r10-d1-shell"),
  ("Standalone result tautological", "The new theorem's nontrivial input is the exact microscopic phase decomposition and uniform component LDP, not ordinary contraction alone.", "thm:r10-d1-main"),
 ]},
}

for folder,meta in DATA.items():
    p=ROOT/'papers'/folder/'AUTHOR_RESPONSE_ROUND10.md'
    lines=[
      '# Author Response — Round Ten', '',
      f"**Referee report:** `{meta['report']}`  ",
      f"**Registered controlling source:** `revision/round10-referee-final/{meta['source']}`  ",
      '**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.', '',
      '## Blocker-to-proof map', '',
      '| Referee blocker | Positive reconstruction | Controlling labels |',
      '|---|---|---|',
    ]
    for blocker,fix,labels in meta['items']:
        lines.append(f'| {blocker} | {fix} | `{labels}` |')
    lines += ['', '## Verification boundary', '',
      'The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.', '']
    p.write_text('\n'.join(lines),encoding='utf-8')

inventory={
 'schema':'theta-theory-round10-referee-inventory-v1',
 'review_branch':'review/round9-gpt56-pro-harsh-11paper-2026-08-31',
 'review_head':'322e4efe825146254d5f4eb6850625b8f99052ea',
 'paper_count':len(DATA),
 'blocker_count':sum(len(x['items']) for x in DATA.values()),
 'papers':{k:{'report':v['report'],'source':v['source'],'blockers':len(v['items'])} for k,v in DATA.items()},
}
(ROOT/'ROUND10_REFEREE_INVENTORY.json').write_text(json.dumps(inventory,indent=2,sort_keys=True)+'\n',encoding='utf-8')
md=['# Round-Ten Referee Inventory','',f"- Review branch: `{inventory['review_branch']}`",f"- Review head: `{inventory['review_head']}`",f"- Papers: **{inventory['paper_count']}**",f"- Major blocker entries: **{inventory['blocker_count']}**",'', '| Paper | Report | Round-ten source | Blockers |','|---|---|---|---:|']
for k,v in DATA.items(): md.append(f"| `{k}` | `{v['report']}` | `{v['source']}` | {len(v['items'])} |")
(ROOT/'ROUND10_REFEREE_INVENTORY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(f"ROUND10_RESPONSES_WRITTEN papers={len(DATA)} blockers={inventory['blocker_count']}")
