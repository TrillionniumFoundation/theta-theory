# Shared-preparation structure: author-revision handoff

## Files

- `49-shared-preparation.tex`: seven new numbered results with complete
  proofs, extending the finite-group theory to a common device for a
  family of selected preparations.
- `diagnostics_r77_shared.py`: dependency-free exact rational diagnostics.
- `diagnostics-shared.json` and `diagnostics-shared-optimized.json`:
  byte-identical successful ordinary and Python `-O` runs.
- `AUTHOR_AI_CHALLENGE_UNRESTRICTED.md`: focused internal mathematical
  challenge of the other author's new unrestricted-approximation proof.

## Mathematical additions

1. Common convex-specification normal form for any finite group and finite
   preparation/outcome alphabets, with one common decoder and transitions.
   Pure resource is core labels plus the number of distinct nonpoint
   preparation rows; equal preparation rows share an initializer.
2. Exact invariant-polytope formulas. Mixed resource is the least vertex
   count. Pure resource is that count plus the number of distinct prescribed
   response tables that are not vertices. The proof counts redundant
   nonextreme core profiles separately, preventing double-charge when a
   recurrent label is used as another preparation's initial label.
3. Joint Fourier multiplicity uses **horizontal concatenation** of the
   prior stacked output blocks. Its rank is the joint irreducible
   multiplicity and may exceed the irreducible degree. Separate single-
   response ranks are insufficient.
4. Exact common-mean low-contrast core cost for every finite group, via the
   complete irreducible multiplicity integer cover and a constructive
   simultaneous positivity proof. A four-preparation trivial-group example
   proves why unequal means cannot be silently included: linear rank three
   but nonnegative rank four.
5. Weighted joint singular-value robustness, with error operator norm at
   most `sqrt(2)*delta` independent of the number of preparations. Weights
   may be independently selected for different irreducibles.
6. Fixed `C2`, q preparations, q+1 outcomes: each preparation individually
   costs two labels, but simultaneous mixed and pure resource is exactly
   `2q`, robust for `delta < epsilon/sqrt(2q)` in the displayed family.
7. Fixed `C2`, binary output, r prepared amplitudes: mixed shared core two,
   pure shared memory exactly r+1. Thus one initializer is not sufficient
   for an arbitrary preparation family.

## Actual diagnostic coverage

- Eight exact rational C2 multiplicity families, q=1,...,8, 324 individual
  preparation/word-length checks (lengths 0,...,8), strict probabilities,
  exact joint ranks and Gram matrices.
- Nine exact rational initialization families, r=1,...,9, 405 checks
  (lengths 0,...,8), matching counted labels, stochasticity, and the explicit
  sign-separation premises of the pure lower bound.
- The four-row mean obstruction: exact rank three and four-element
  positive-diagonal fooling-set certificate.
- A nonabelian S3 test with three natural-orbit copies: each individual
  standard multiplicity is one, joint multiplicity is three (larger than
  degree two), and direct residual rank is seven. The 36 representation
  multiplication identities were checked exactly.

These calculations are finite diagnostics and do not substitute for the
written arbitrary-group proofs. The script uses explicit exceptions,
so optimized Python does not remove its checks.

## Provenance and theorem dependencies

The baseline R76 source was read without modification. New proofs use
the inherited identity-word stochastic projection and closed-convex
all-word normal form (`thm:r76-convex-normal-form`), classical finite-group
complete reducibility and its already proved real descent
(`lem:r75-fourier-multiplicity`), the inherited stacked Fourier definition
(`eq:r75-fourier-block`), and the elementary norm/rank certificate in
`thm:r76-robust-multiplicity`. All new resource counting and simultaneous
positivity details are proved in the new section.

The group need not be a faithful observable quotient. The controller's
terminal decoder has no free access to the preparation selection. Pure
external selection means choosing one counted label; mixed preparation is
the separately stated free-initial-mixture convention. The general common-
mean theorem does not replace the original single-state experiment theory,
rank-constrained reset problems, communication accounting or companions.

## Literature and priority inspection

The following primary sources were located or inspected on 2026-10-23.
No absence-of-search-hit is treated as priority clearance.

- **Gouveia, Parrilo, Thomas**, *Lifts of Convex Sets and Cone Factorizations*,
  Mathematics of Operations Research 38(2) (2013), 248--264,
  DOI `10.1287/moor.1120.0575`.
  The author-deposited 2011 PDF was opened at
  https://optimization-online.org/wp-content/uploads/2011/11/3249.pdf .
  It explicitly treats cone-factorization/lift equivalence and symmetry;
  its symmetric theorem is numbered 2.9 in that preprint (the existing
  manuscript cites published Theorem 2.12). This priority is acknowledged;
  the invariant-polytope interpretation itself is not advertised as a new
  discovery of the connection between positivity and convex geometry.
- **Benvenuti and Farina**, *A Tutorial on the Positive Realization Problem*,
  IEEE TAC 49 (2004), 651--664, DOI `10.1109/TAC.2004.826715`.
  Author institution record and abstract were inspected at
  https://iris.uniroma1.it/handle/11573/232104 .
  They explicitly describe classical geometric existence and minimality
  conditions. The full attached publisher PDF was access-restricted, so
  no new theorem-specific attribution was made from this metadata alone.
- **Heller**, *On Stochastic Processes Derived From Markov Chains*,
  Annals of Mathematical Statistics 36(4) (1965), 1286--1291,
  DOI `10.1214/aoms/1177700000`.
  The publisher result at
  https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-36/issue-4/On-Stochastic-Processes-Derived-From-Markov-Chains/10.1214/aoms/1177700000.full
  verified bibliographic identity; opening yielded only an iframe.
  Its classical invariant-cone place is inherited from the manuscript's
  earlier literature analysis, not asserted as newly inspected full text.

Targeted searches for shared/multiple preparations, finite-group positive
realizations and initial distributions did not establish an independent
priority verdict. The finite-group common-device, exact prescribed-label
charge, noncyclic multiplicity synthesis and explicit sharp families form
the proposed contribution. Their publication significance remains for a
genuine independent assessment; no claim of top-four acceptance is made.
