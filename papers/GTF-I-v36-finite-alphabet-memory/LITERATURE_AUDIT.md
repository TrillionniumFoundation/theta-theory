# Primary-source and theorem-level audit — revision 36

Audit date: 25 September 2026. This record distinguishes material inspected from mathematical inferences made in the present revision. It is not an independent or exhaustive priority certification. External papers are cited, not copied into the distributed source packages.

## Direct external input

**Bourgain–Gamburd, A Spectral Gap Theorem in SU(d).** JEMS 14 (2012), 1455–1511; DOI 10.4171/JEMS/337; preprint https://arxiv.org/pdf/1108.6264. Theorem 1 and its density qualification were inspected in the original PDF, including its rendered theorem page. It supplies the spectral gap for algebraic dense generators. The revision proves that its particular SU(2) gates generate densely, adds laziness, and passes to the homogeneous sphere quotient. The theorem is invoked, not reproved. No explicit numerical gap is extracted. The orbit-quantization-to-width argument is additional; the existence of a spectral gap is not new here.

## Quantum finite automata

**Chen–Wu, The State Cost of Classical Simulation of One-Way General Quantum Finite Automata.** https://arxiv.org/html/2604.07058v2, 27 August 2026. This is the current revised title, not the earlier April title quoted by the referee. Inspected Definition 2.1, model definitions in Section 2.2, Proposition 3.1 and its proof, Theorem 3.2 and its proof; also the stated dynamic-shattering construction.

- Minimized object: PFA state cardinality preserving a strict-cutpoint language of a general one-way QFA.
- Resource variable: quantum dimension n, with worst-case PFA bound n^2+1.
- Kernels: CPTP quantum updates, general PFA stochastic updates; fixed updates at all lengths.
- Preserved quantity: threshold signs, not probabilities. Proposition 3.1 gives a positive length-dependent attenuation of the cutpoint deviation.
- Present comparison: the exact same rational-gate qubit behavior has dimension two, hence a threshold-language PFA of at most five states, while numerical wordwise fixed-tolerance simulation has a growing classical width. The latter permits cut-dependent horizon-specific machines. The two objectives are neither conflated nor presented as a contradiction.

**Chen–Wu, On the Simulation Cost of Quantum Finite Automata.** https://arxiv.org/html/2605.10682v1, 11 May 2026. Inspected the model conventions, Definition 7, Theorem 14, Corollary 15 and Theorem 19, with their surrounding argument. Theorem 14 supplies a worst-case strict-cutpoint lower bound for measure-once QFAs; Corollary 15 gives its quadratic comparison; the finite prepare--test matrix/sign-rank framework is in Theorem 19. These are language-simulation/state-cost results as quantum dimension varies, not the finite-horizon numerical accuracy problem here. The revision does not assert its reset model is measure-once unitary on every alphabet symbol; it uses the general CPTP convention when invoking the five-state consequence.

**Chen, Behavioral Memory under Symmetry in One-Way Quantum Automata.** https://arxiv.org/html/2609.01451v1, September 2026. Inspected the stated strict-cutpoint scope, behavioral Hankel-rank discussion and invariant-algebra interpretation. This adjacent source motivates distinguishing predictive rank from operational memory. No numerical-probability simulation theorem is attributed to it, and no additional lemma in the current paper depends on its conclusions.

**Lumbreras–Ma–Thompson–Gu, An Irreducible Quantum Advantage in Aligning World Models with Reality.** https://arxiv.org/html/2608.19779v1, 21 August 2026. Inspected the problem formulation, Theorem 12, the stationary irrational-phase mechanism, and Theorems 28–30 with relevant surrounding proofs. The objects are stationary finite recurrent world models, policy/value or decision errors, and an exact qutrit comparator. Our machine is reselected at each finite horizon and can change rows at each cut; the objective is uniform numerical terminal behavior on complete external command words. Their stationary argument is not used as a lower bound for this larger finite-horizon class. Quantum/classical separations as a subject are not claimed new.

## Branching programs and random walks

The primary statements and distinctions checked in v35 remain relevant: Reingold–Steinke–Vadhan (RANDOM 2013), Steinke–Vadhan–Wan (Theory of Computing 13, 2017, Article 12), Lee–Pyne–Vadhan (APPROX/RANDOM 2022, Article 2), and Berkes–Borda (JLMS 108, 2023, 409–440). The first group studies Boolean-input Fourier growth/pseudorandomness under its regular, permutation, or width restrictions. The second studies arithmetic/harmonic mixing of circle walks. The matrix-product Fourier identity is algebraic and is not our endpoint-compression inequality. Arbitrary row stochasticity is not double stochasticity; extending a deterministic bound by averaging tables must not introduce a shared seed as a free decoder input.

The sphere spectral gap in the present revision is a stronger, separate analytic hypothesis than a circle Diophantine bound. A finite iid-letter distribution mixes at a logarithmic command-time cost in the proof. The matched monomial theorem instead uses correlated width-dependent packets on a cyclic sublanguage. These are distinct test laws.

## Inherited realization and implementation mechanisms

The v35 article and its audit preserve Heller/Vidyasagar positive-realization antecedents, reachable/observable quotient issues, Blackwell deficiency, orbit quantization, and the direct wordwise/clocked conventions. No priority for these frameworks is asserted. The new general packet lemma makes full-word dependence explicit; fiber averaging could also bridge the earlier formal implication when the whole word is fresh. A same-product spelling witness is not offered as a counterexample to the repaired numerical bound.

The finite-coin implementation uses elementary dyadic comparison and coupling. The claimed theorem is its charged sparse-row control bound and its application to the new exact constructions, not priority for binary threshold sampling. It does not provide zero-error finite-bit sampling of an arbitrary irrational row, uniform algorithmic table construction, or an autonomous stopping-time theorem.

## Limits of this audit

No exhaustive search of every quantum-automata, positive-system, geometric-quantization or probabilistic-branching-program result is claimed. The proof-level comparisons above identify the actual objects and quantifiers in the directly named sources. Independent priority review has not been obtained. The spectral-gap upper/lower logarithmic gap is explicitly unclosed. The matched noncommuting theorem has monomial structure; its converse uses a cyclic restriction. These are substantive scope statements, not claims of universal coverage.
