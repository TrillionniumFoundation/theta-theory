# Response to the round-five independent referee reports

**Reports:** `review/round5-gpt56-pro-harsh-11paper-2026-08-31`  
**Reviewed candidate:** `revision/round5-referee-positive-closure-11paper-2026-08-31@557c88ef447ab8c693b11e1c072efe97b4452556`  
**Revision:** `revision/round6-referee-positive-closure-11paper-2026-08-31`

## Source-control response

The referee was correct that the prior candidate packets were not part of the
manuscripts.  The round-five materializer stopped on an ASCII control byte in
A1, and C2 contained another control byte.  The active paper modules therefore
remained unchanged.  Round six does not repair this merely by rerunning the
old script.  It replaces every candidate packet by a new UTF-8 round-six
module, copies the exact bytes into each paper, changes each `main.tex` to load
the new module, and checks source identity before any theorem or build gate is
credited.

## Mathematical response by paper

| Paper | Referee's decisive finding | Round-six positive repair |
|---|---|---|
| **A1** | core-supported work did not equal the branch current on the full port; suspension and physical trace calculus were incomplete | Work is accumulated on four disjoint full incoming-port components before branch/recutting, so every regular point receives exactly its branch work.  A one-section graph-completed symplectic map, autonomous suspension, relative port cobordisms, and a finite trace-jet response scale are proved in `lem:r6-a1-section`, `thm:r6-a1-suspension`, `prop:r6-a1-work`, and `thm:r6-a1-response`. |
| **A2** | a nonzero trace summand could not be invertibly identified with zero at a birth; second trace derivatives and the Dolgopyat theorem were missing; the LLT was still too broad | All labels live in one fixed ambient distribution/trace field and births/deaths are zero realization amplitudes.  Jets through order two close parameter differentiation.  Return/nonconcentration and paired cancellation operators prove the high-frequency estimate.  A master Fourier theorem gives absolute errors, with relative asymptotics only in explicitly valid local, central, and saturated regimes. |
| **A3** | ordinary finite-moment probabilities could not retain macroscopic escaped clock mass; candidate Markovization added forbidden edges | The state is a pair `(recurrent measure, recession defect measure)` with an exact collision-clock normalization.  Defects live on compact normalized excursion profiles.  Markov approximants use only actual graph edges and connector words and preserve entropy by uniform integrability of the information function.  This yields full recurrent--defect collision and physical path LDPs. |
| **A4** | `eta_B(0)` was not orthogonal; covariance positivity did not imply a zero-free compressed resolvent; conditional kernels were absent | The exact identity `eta_B(0)=PLQB` is stated without orthogonality.  All compressed-transfer zeros in a left strip are realized as finite auxiliary modes by a Smith--McMillan factorization; only the residual minimum-phase memory is claimed exponentially decaying.  A common-exceptional-set Ray process, history eigenfunction, area-corrected enhanced invariance principle, and uniform conditional-kernel theorem are proved. |
| **B1** | the proposed `m0` smoothing block was not a connected-log term; mixed Cramér and shell estimates were unproved | The logarithm is split exactly into its compound-Poisson one-label exponent and the connected remainder.  Smooth convolution powers are obtained by exponentiating the singleton term, with all Poisson combinatorics retained.  Uniform number/mark covariance, finite mean image, exact finite-volume saddle, global mixed characteristic estimates, and the shrinking-shell coefficient follow. |
| **B2** | the arbitrary-`L1` boundary-flux ledger was false; the Gramian omitted roots; source sewing and lower bounds were unproved | Contact moments are controlled only on a trace-regular hierarchy class containing the actual initial and tilted laws.  The trace norm includes incoming flux and tangential traces and survives stopping contacts.  The genealogical Gramian includes independent root translations, root velocities, and every creation control.  The first surplus contact gets a codimension-two tube gain; the complete true reflected future is retained and controlled by the trace semigroup.  Fixed-horizon pressure, regularized lower bounds, and GC/MC joint LDPs are proved. |
| **B3** | the bounded analytic chart could not yield a global entropy dual; zero covariance was confused with pointwise constancy; a compensator and finite centring were absent | Local analytic response and global Fenchel duality are separate source domains.  The global domain is the union of all bounded compact-source balls and supports arbitrary scaling/truncation.  The balance gauge is closed in one weighted strict space.  Covariance nondegeneracy is proved from the quadratic action on balanced tangents, not pointwise constancy.  Exact finite means are used, and time-localized connected cumulants give Aldous--Mitoma tightness without a contact compensator. |
| **B4** | the exact law semigroup was tautological, the BBGKY corrector formal, second-moment sublevels noncompact in the chosen topology, and comparison penalties left the core | The exact finite state remains the full probability law, while the kinetic nonlinear semigroup is explicitly a proved LDP limit.  A genuine polynomial algebra on law coordinates replaces the false linear hierarchy algebra.  One normally summable full triangular BBGKY Duhamel corrector is built.  The density topology is ordinary weak topology with l.s.c. energy, whose energy sublevels are compact; no convergence of second moments is required.  A convergence-determining compact-support core keeps all doubling penalties inside the bounded-increment Hamiltonian domain. |
| **C1** | Bayes update omitted the new observation; expected posterior error used KL; LAN used the limiting centre | Each step is controlled prediction followed by disintegration with respect to the newly observed block.  Ionescu--Tulcea constructs the strategy law from the already controlled observed posterior.  Typical posterior density odds have the directed KL rate, while expected posterior error has the Chernoff/testing rate.  The score is exactly centred at `DQ_epsilon`; uniform tests plus local analytic bounds give canonical BvM. |
| **C2** | weighted pressure lacked coercivity; conditional homogenization was assumed; memory was not typed in one Hilbert space | Every platform rate satisfies an explicit rate--moment coercivity inequality and sources stay below its slope.  The A4 compact-history conditional-kernel theorem proves optional-projection convergence.  Finite likelihoods are exact history martingales.  Pressure tangent and memory are paired in `L2(nu_D)` for the genuine Doob semigroup and one orthogonal projection; no equality with an untitled Koopman compression is asserted without an intertwiner. |
| **D1** | the exact likelihood was not mean one and P3 assumed the global lower bound | Every local likelihood is centred at `DQ_epsilon` and is algebraically the exact Radon--Nikodym density.  The global LDP is derived instead from finite-dimensional pressures that are finite, differentiable, and steep, followed by Dawson--Gartner and exponential tightness.  Conditioning/contraction interchange is proved by a closed joint primal infimum, not by an assumed exposed-density theorem.  D1 is retained and strengthened rather than deleted. |

## Dependency response

The hard-sphere proof order is now strictly

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The Sinai order is

```text
A2 -> A3 -> A4 -> C2/D1.
```

A1 is independent.  No downstream label is used to prove an upstream packet.
The exact dependency and publication gates are recorded in
`ROUND6_PROOF_DEPENDENCY_LEDGER.md`.

## Scope and editorial threshold

The reports also express journal-novelty judgments.  Those judgments are not
answered by deleting results or weakening them to negative statements.  The
mathematical response is to provide the missing constructions and proofs at
the stated model level.  The A1 mechanical--valuation identification remains
explicitly conditional on equality of likelihood cocycles; no stronger
preference-selection claim is made.

## Publication condition

No internal status is counted as closure until the exact eleven controlling
modules pass the counterexample-aware verifier, dependency-aware hostile
rereview, clean 11/11 LaTeX build, undefined-reference gate, source-hash
certificate, archive check, and post-publication ref check.  These are
repository-internal verification gates and do not claim external journal
acceptance.
