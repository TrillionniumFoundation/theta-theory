# Primary literature and priority audit — R73

This document distinguishes classical tools, the precise mathematical increment
over the complete R72 source, and comparisons whose full text was not inspected.
It is an author-side literature audit, not an exhaustive priority certificate or
an independent expert verdict. All inherited bibliography entries and previous
audits remain available in the unchanged R72 tree.

## Sources inspected for the new structural chain

| Primary source and locus | Retrieval actually completed in this resumed revision | Role in the manuscript |
|---|---|---|
| Š. Schwarz, *On the structure of the semigroup of stochastic matrices*, Publ. Math. Inst. Hungar. Acad. Sci. 9 (1964), 297–311, Theorems 7–8 | Complete 15-page scan in the Hungarian Academy repository; theorem and proof text inspected | The normal form of stochastic idempotents and the symmetric-group structure at an idempotent of fixed rank are classical. R73 supplies its own finite Markov-chain proof while crediting this antecedent. |
| P. Flor, *On groups of non-negative matrices*, Compositio Math. 21 (1969), 376–382, Theorems 2–3 | Complete primary journal scan, including the introductory account of Brown and Schwarz | Nonnegative idempotent structure and the reduction of a bounded nonnegative matrix group to permutations are classical. The current assertion is not the discovery that a stochastic group is finite or acts on simplex vertices. |
| D. R. Brown, *On clans of non-negative matrices*, Proc. Amer. Math. Soc. 15 (1964), 671–674, DOI 10.1090/S0002-9939-1964-0165504-6 | Original article's title, pages and attribution checked through Flor's primary text; the direct publisher request was not accessible in the resumed pass, so no fresh complete Brown-text read is asserted | Flor attributes finiteness of compact nonnegative matrix groups to Brown. The attribution is retained rather than assigning that fact to the present paper. |
| J.-P. Serre, *Bounds for the orders of the finite subgroups of G(k)*, in *Group Representation Theory*, EPFL Press (2007), 405–450, §1.2 | Complete author lecture scan; its internal date is April 2006, while the bibliographic publication is 2007 | The congruence-kernel torsion argument and finite linear-group bounds are classical. R73 proves the elementary modulus-three bound it actually uses; it does not claim Serre's sharper bounds as new. |
| S. Kiefer and B. Wachter, *Stability and complexity of minimising probabilistic automata*, ICALP 2014, LNCS 8573, 268–279; author version arXiv:1404.6673, §4.2 and Proposition 10 | Complete 26-page author version, especially the existential-real reduction and its proof | Positive/probabilistic automaton minimization via real algebraic feasibility is established. R73 makes no first-decidability or general polynomial-time claim for that problem. Its finite group enumeration and exact pure-start realization formula define a specific supplied-input synthesis theorem. |

Primary source links:

- [Schwarz, original scan](https://real.mtak.hu/189463/1/cut_MATKUTINT_1964_3_pp297_-_311.pdf).
- [Flor, original journal scan](https://www.numdam.org/article/CM_1969__21_4_376_0.pdf).
- [Brown, publisher DOI](https://doi.org/10.1090/S0002-9939-1964-0165504-6).
- [Serre, author lecture text](https://www.college-de-france.fr/media/professeurs-honoraires/UPL61351_Serre_Lausanne.pdf) and [author-deposited publication record](https://arxiv.org/abs/1011.0346).
- [Kiefer–Wachter, full author version](https://arxiv.org/pdf/1404.6673) and [publisher DOI](https://doi.org/10.1007/978-3-662-43951-7_23).

## The increment being asserted

The new normal form begins with an **arbitrary stochastic hidden realization of
a compactly reversible observable response**. The hidden matrices need not
form a group, be invertible, commute, or act on the observable quotient without
a reachability restriction. The proof constructs an identity-loop averaging
projection, proves the sandwiched loop identities, and then descends to a
faithful permutation action. This lifting argument and the exact charge for a
prescribed pure initial label are the steps that must be checked before any
classical stochastic-group theorem can be applied.

The resulting invariant is a bounded probability factorization of the complete
group response. It gives an exact minimum of the deterministic residual count
and one plus the smallest permissible permutation factorization. The rank
rigidity result, the sharp group-order inequalities, the two-command
`S_k` family with `k+1` stochastic versus `k!` deterministic-transition labels,
and the recovery of the inherited periodic partition formula follow with
explicit hypotheses and implementations. These are precise additions to R72;
the audit does not claim that no equivalent formulation appears anywhere in the
literature.

The `S_k` realization may be written as a diagonal quantum preparation,
permutation unitaries and a diagonal effect. Its state-count separation is
between stochastic and deterministic classical simulation. This example does
not establish a specifically quantum advantage over classical stochastic
memory.

Finite-word equivalence and finite-dimensional reachable-span stabilization are
classical automata methods. R73 uses them to obtain a positive uniform finite
probe gap for an excluded memory budget, algebraic certificate extraction for
algebraic inputs, and a stable exact-memory interval under damping toward the
group-averaged response. The explicit period-four certificate is proved by a
nonnegative polynomial identity. Neither bounded diagnostics nor an unevaluated
quantifier-elimination statement is represented as an executed general
certificate computation.

## Other classical and inherited inputs

| Input or nearby theory | Present attribution and extent of comparison |
|---|---|
| Moore / Myhill–Nerode residual equivalence | The deterministic residual-index construction is classical, as already acknowledged in R65–R72. The current stochastic minimum is a different quantity. The inherited bibliography and proof are retained. |
| Tzeng, *A polynomial-time algorithm for the equivalence of probabilistic automata*, SIAM J. Comput. 21 (1992), 216–227, DOI 10.1137/0221017 | The bounded-word / reachable-span equivalence argument is credited to the established equivalence theory and is reproved in the current text. No fresh complete publisher-PDF read is claimed in this resumed pass. |
| Babai, Beals and Rockmore, *Deciding finiteness of matrix groups in deterministic polynomial time*, ISSAC 1993, 117–126, DOI 10.1145/164081.164104 | Rockmore's author bibliography was successfully read and identifies the prior matrix-group finiteness algorithm; the alternate Babai bibliographic page returned a gateway error in this resumed pass. The present deliberately elementary search is a terminating construction for the stated algebraic representation, not a competing efficiency claim. |
| Seidenberg / real quantifier elimination | Semialgebraic projection and effective algebraic witness extraction are classical. They remain explicitly named tools, with the finite polynomial system and bounds supplied in the current proof. |
| Heller; Thon–Jaeger; Benvenuti–Farina; Monras–Winter; Fanizza–Lumbreras–Winter | The predecessor bibliography and audits credit linear rank, positive/invariant-cone realization and quantum/classical memory obstructions. R72 records a complete publisher-text comparison with Fanizza et al. (2024), DOI 10.1007/s00220-023-04913-4. That recorded prior read is not relabeled a newly completed full-text comparison with every cited work. |
| Nussbaum–Scheutzow and stochastic periodic-orbit theory | The classical cycle/lcm restrictions remain prior art. The inherited response-mode partition optimization, bounded decoder and initialization charge are the particular exact conclusions used here. |
| Dmitriev–Dynkin, stochastic spectral sectors, continued fractions and irrationality exponents | The existing citations and full R69–R72 proof chain remain intact. The new structural theorem does not reclaim these earlier results or infer a sharp arithmetic constant from numerical samples. |

## Boundaries of the generality claim

The structural result concerns finite-dimensional compactly reversible response
systems and their finite stochastic realizations. Its unitary corollary covers
arbitrary finite command families after removing invisible directions. It is
not a theorem for every feedback-controlled experiment or every finite-memory
boundary optimization problem. The original general causal-transfer theorems,
reset/discrimination companions, local spectral geometry and specific exact
model formulae retain their separate mathematical authority.

The algebraic synthesis theorem assumes supplied exact algebraic data and the
stated probability/compactness promises, or the physical unitary input that
provides those promises. It does not decide positivity of an arbitrary rational
series, learn an unknown physical system from finite data, or establish matching
time/program/precision lower bounds. The finite certificate and stable-memory
results strengthen the quantitative theory without identifying the different
old fixed-`M` squared-sign risk frontier as solved.

The original General Theta Foundations I research identity and the
Annals / Acta / Inventiones / JAMS objective are unchanged. Whether the combined
contribution meets any journal's threshold is an independent editorial question;
this author revision supplies stronger proved statements and transparent
attribution for that assessment.
