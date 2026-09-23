# Response to the controlling v17 reports — revision v19

**Manuscript:** General Theta Foundations I: Continuation Complexity and Stable Causal Certification. **Author:** Qian Qi. **Date:** 23 September 2026.

The controlling external r3 report is frozen at `a94ec98d6e33d9719f72deec160f5c8270ce006f`, report blob `b1515103564c6c0de02b1751dad24ea23bee1f5f`. The pipeline-aware r2 report is at `9f4787221c086e25f7d95b36e97aff870bd2b0c5`, report blob `09646a80c6b6fc9f89a3e575d6e2dd2a832a200f`. Both full reports were read, including their technical comments and concluding requirements. They concern v17, not v18. The remote already contained the subsequent v18 publication `e7d020c49959009a775081ea9aa70c7e7fec5d52`; v19 therefore builds on that publication rather than discarding its answers. The separate first v17 report is not represented as a separate full-text audit here.

We retain every predecessor source and every page of the 294-page v18 complete development. The journal-facing article is organized around Theorem `thm:v19-main`, with full proofs, a canonical dependency diagram and an explicit inherited baseline. Revision discussion and proof-status records are outside the article.

## What is actually added beyond v18

The central additions are not another revealed-law identity. Theorem `thm:v19-residual` turns insufficient continuation width into a quantitative decision error. Theorem `thm:v19-binarywidth` identifies exactly the streaming widths that attain the optimal odd-sample binary reset value and gives an explicit strictly positive deficit below them. Lemma `lem:v19-counter` uses the private continuation constraint to replace the general multinomial audit by two truncated counters: 400 training resets, two validation trials, at most 504,008 states, or nineteen retained bits. Theorem `thm:v19-global` upgrades the bounded entropic consumer from localized integrand convergence to global physical-law and coupled H2 estimates, with S2 convergence of its martingale integral. Theorem `thm:v19-composition` carries this same small auditor and the global conditional-law consumer through changing collision trajectories.

These are manuscript proofs submitted for independent review. Their significance and priority are not conclusions of the build system.

## E17-R3.1 — Constrain the tester rather than reveal its law

V18 correctly renamed the inherited partition-of-unity theorem “Revealed-behavior adaptive representation” and introduced the finite-reset information pattern. We retain both, with their different interfaces. V19 additionally constrains the auditor's persistent register, forbids an uncharged history store and specifies the free schedule clock. Fresh randomness and an independent persistent selector are distinguished.

For a Boolean final decision, the equivalence of two prefixes means agreement on every possible suffix. Theorem `thm:v19-residual` proves exact stochastic width equals the number of these continuation classes at every cut. Its proof uses extremality of zero--one continuation responses, not a false minimax exchange on a nonconvex fixed-width policy class. The statistical consequence explicitly prices both reset count and streaming width. The finite-reset moment dual inherited from v18 remains valid on its original coefficient simplex; it is not silently transferred to the restricted class.

## E17-R3.2 — A lower bound tied to the same continuation invariant

If a decision has r distinct continuation rows at a cut but the tester retains only K states, the sum of its wordwise errors is at least `(r-K)_+/(r-1)`. The proof sums pairwise overlaps of state distributions and controls the multiplicity of distinguishing suffixes. This inequality applies to stochastic implementations and survives independent mixing of same-width auditors.

For n=2m+1 samples from the two Bernoulli candidates, Theorem `thm:v19-binarywidth` proves the exact optimal-value profile

`r_t = min(t+1, n-t+2), 0 <= t < n`.

At any deficient cut the value loss is at least

`2 h^2 (1/4-h^2)^m (r_t-K_t)_+/(r_t-1)`.

The final decision is emitted on the last transition, so the terminal register is not confused with the last pre-decision register. For n>=3 the least peak training width attaining the unrestricted value is m+2. The n=1 boundary case is stated separately. We do not claim this small positive penalty is an asymptotically sharp joint memory/sample/error law. It is an exact attainment classification with an explicit obstruction. The v18 erasure-cut spectrum and sharp uniform sampling exponent remain intact.

## E17-R3.3 — Formal chart effectiveness

The exact input/output algorithm of Proposition `prop:v18-chart` is retained unchanged. Rational simplex equalities are eliminated; coefficient-span linear algebra computes the observable quotient dimension and a rational basis; rational sample tuples are enumerated; a quantified polynomial determinant inequality certifies the bounded chart; substitution gives the rational pullback. Dimension is computed rather than assumed. Strict half-maximum slack and density prove termination. No numerical optimization oracle, polynomial-time guarantee or coefficient-height estimate is added without proof.

The new counter rule requires no chart oracle: its thresholds are the integers 150 and 250. The chart remains relevant to the general rational polynomial verification framework and the effective-presentation clause of the final theorem.

## E17-R3.4 — One theorem using resource geometry, scattering and transport

Theorem `thm:v19-composition` improves the v18 composition rather than leaving the three modules parallel. Private width one forces independent report parameters p,q and an independent fair actual mark. The ideal target has only four supported marked atoms, determined on the candidate side by `(1-p)(1-q)` and `pq`. This resource restriction is used to build the two-count audit; it is not valid against arbitrary hidden mixtures.

The pointwise empirical-event regret is bounded by the sum of errors of these two empirical probabilities. Its expected value is at most `1/sqrt(n)`. At n=400, scattering's target perturbation of less than 1/300 gives expected physical score greater than `sqrt(5/2)-9/8-1/20-1/300 > 2/5`. The candidate law is never revealed. Training need not read the mark; independent validation uses the actual mark and actual physical target.

The clipped count register has 251 squared possibilities. Including the complete transcript buffer gives 504,008 states; the smaller validation phase reuses them. There are 402 trials including validation, and this is stated explicitly. The nineteenth bit count is a retained-state bound, not a transition-table description bound and not a claim of minimality.

Changing contact distance changes actual collision times and trajectories. The signal modulus `rho=|d'-d|+2700|d'-d|^2` gives joint marked variation at most `min(1,sqrt(rho)/(2 sigma))`. Because the source is unchanged, that is also the loss of this same fixed audit, with no factor of 400. The same estimate feeds the global backward theorem. These are explicit proof dependencies in the article, not inferred from a repository graph.

## E17-R3.5 — Preserve the mechanism and its actual physical scale

Both the main theorem and physical proof say that B--W correlation is prepared and collision transduces B into a measured transverse velocity. The model has two labeled spheres and one nongrazing collision; the control is an acquisition gate. Neither kinetic scaling nor a particle-number-uniform estimate is claimed. The no-collision conclusion remains in the main theorem: all three deficiencies vanish at d<=2/5. The stronger finite-register audit is added without deleting the older exact nonlinear certificate or the 2,800-trial general audit.

## E17-R3.6 — Global conditional-law and backward transport

V18 already replaced the fixed-flow specialization by a common-preparation Gaussian theorem allowing changing microscopic paths. V19 keeps all its hypotheses and strengthens the conclusion rather than changing the target equation. Lemma `lem:v19-posterior` proves a denominator-free integrated posterior estimate under either physical law. The innovation coefficient therefore has global H2 error at most

`A_n = (2 eta_n^2 + 16 M^2 T epsilon_n)/sigma^2`.

A bounded terminal tilt identifies the numerator logarithmic coefficient as a posterior signal in another common-preparation model. This gives global H2 error of the backward integrand at most `2(1+exp(4 gamma)) A_n/gamma^2`, under either physical law. Uniform coefficient bounds also remove localization under the reference law, though no new explicit reference rate is claimed. Own-path estimates on the latent-preserving coupling are stated separately.

The already identified BSDE then gives supremum-L2 convergence of its martingale integral; innovations converge uniformly in probability. No Brownian or martingale property in the joined coupling filtration is asserted. The terminal condition remains the observable conditional certainty equivalent, not the latent payoff. This supplies the full bounded entropic backward representation in the stated changing-path class, not an unspecified theorem for arbitrary nonlinear drivers or singular noise limits.

## E17-R3.7 — Statement-level proof credit and supersession

`PROOF_STATUS.json` identifies every theorem/lemma/proposition by its statement hash, source file, source hash, version credit, dependencies and review status. The executed build binds these statements to the actual source commit and compiled page. `PIPELINE_STATUS.json` retains the entire v18 namespaced graph and all eleven historical components while adding the v19 consumer and its edges.

The old C2 optional-projection inference is not re-endorsed: finite-dimensional convergence plus a maximal amplitude estimate alone does not prove path tightness. The v18 direct likelihood/posterior estimate is the scoped repair; v19 strengthens its backward-integrand consumer globally. The C2 strict dual, form response, rigidity and aggregate theorem retain their separate proof burdens.

The B4 normalized-resolvent identity still fails on the constant-one payoff and is not used. This does not delete B4 or convert a local countercheck into a negative theorem about the whole program. The historical statements are retained, with source assertion distinguished from current proof credit.

## E17-R3.8 — Actual downstream use

The new C2 consumer has a verifiable proof chain: moving microscopic path -> common-preparation joint variation and likelihood transport -> posterior comparison and bounded tilt -> global innovation, backward-integrand and martingale-integral transport. The same input transports an explicitly implemented finite resource certificate. All physical hypotheses are discharged in the moving-collision family.

The independent A2 primary geometric chain is left independent; its results are not assigned a fictitious GTF ancestor. The general foundational objective is retained, with an actual conditional-law consumer instead of a universal-closure assertion unsupported by the manuscript. The new binary theorem supplies an intrinsic continuation/test-complexity relation rather than a second unrelated example of revealed-law selection.

## E17-R3.9 — Norberg original proof comparison

**Still unverified, not marked resolved.** The publisher original-PDF route and related national-library record did not yield the original proof body in this audit. The AMS original route for Nerode also returned an access error; the residual construction is therefore proved in full and credited as classical, without a new claim of original-text inspection. Fliess's original positive-cone theorem and proof were obtained and inspected; their mechanism is expressly subtracted.

The Norberg checklist remains: precise deficiency, filtered operator class, adaptation convention, persistent information, convexity, additivity, necessity/sufficiency and proof mechanism. Metadata or secondary quotations cannot establish these points. `LITERATURE_AUDIT.md` preserves the distinction. No absolute priority claim or claim of absence from Norberg is made. This item remains a publication-level limitation of the revision.

## E17-R3.10 — A theorem spine without arbitrary deletion

The opening theorem leads to exact streaming complexity and to one finite-register microscopic certificate with a global conditional-law consumer. The canonical diagram explicitly says which branch supplies a lower bound and which supplies the physical upper construction; it does not invent an essential proof dependence of the counter algorithm on the binary lower bound. The inherited baseline summary is identified in the appendix. All inherited mathematical modules are reproduced unchanged; prior introduction and historical material remain in the complete companion. The source preservation map and page comparison are separate from the proofs.

## E17-R3.11 — Theorem-level subtraction

`PROOF_LEDGER.md` distinguishes classical residual-state/positive-cone ideas, inherited GTF statements, and the additional overlap-to-regret inequality, exact optimal-value width profile, compressed private-family audit and global terminal-tilt bounds. Elementary two-point testing, empirical second moments, Girsanov and exponential transformation are not claimed as discoveries. The organizing contribution offered for review is their proved compatibility with both sides' persistent resources and with the same changing microscopic experiment.

## E17-R3.12 — Reproducibility is not proof

The finite diagnostics exercise residual counts, likelihood margins, small deterministic auditors, all feasible clipped-count pairs, rational regret cases and posterior inequalities. They do not prove the continuum transducer theorem or stochastic-process limits. Negative controls test the checker rather than provide independent mathematical review. Compiled labels, hashes, preserved pages and artifact identities are reproducibility evidence only. The analytical claims stand on the written proofs and remain subject to external review.

## Pipeline report crosswalk

| Item | Response |
|---|---|
| E17-P1 | Exact inherited namespace and new statement identities in `PIPELINE_STATUS.json` and `PROOF_STATUS.json`; no global closure flag inferred. |
| E17-P2 | Historical C2 optional step retains its scoped replacement; v19 supplies global bounded-backward integrand and integral transport. |
| E17-P3 | Actual changing-path C2 consumer with discharged physical hypotheses; no manufactured A2 dependence. |
| E17-P4 | `thm:v19-composition` uses the private continuation restriction, fixed streaming audit, scattering and global transport. |
| E17-P5 | Revealed-law identity remains correctly named; tester memory is now constrained and analyzed directly. |
| E17-P6 | Exact optimal-value width profile and explicit positive deficit, in addition to the retained cut and sampling lower bounds. |
| E17-P7 | Original Norberg proof-level audit remains unverified. |
| E17-P8 | Exact original B4/C2 Round-Seventeen sources were read; their aggregate assertions are not accepted as proof inputs. |

All specific technical comments about common latent laws, equivalence, noncausal coupling, strict chart inputs, prepared correlations, no-collision controls, hidden convexification and existential support bounds retain their explicit qualifications. The requested mathematical scope is preserved. The remaining priority audit and the journal's independent significance judgment are not disguised as completed tasks.
