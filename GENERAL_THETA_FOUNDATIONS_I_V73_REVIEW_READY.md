# General Theta Foundations I — Revision 73 referee entry

Controlling v71/r46 report: `b78c1dddd41de645edf207bc415406b3fc1b5e83`; audit: `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.
Base: completed v72 final head `12296ed387dbc197ff7cb854d3a78d0bf964960e`. Its source and exact-head runs succeeded; no v72-specific external review was located.

Quantitative: `papers/GTF-I-v73-noisy-readout-crossover/paper.pdf` (40 pages).
Structural: `papers/GTF-I-v73-noisy-readout-crossover/STRUCTURAL_PAPER.pdf` (40 pages).
Complete research edition: `papers/GTF-I-v73-noisy-readout-crossover/COMPLETE_REVISION.pdf` (140 pages).

Native source: `28ab8c51143df999b444273b954f63a5160c83f7`.
Builder run: `37152200748`.
Transfer/workflow trigger: `5411e3a520518ffffc06888fbceda3a7998840c0`; all native files were committed before qualification.

Main theorem: for public visibility lambda in [0,1], let K=lambda*sqrt(N*min(N,1/(1-lambda^2))), with K(N,1)=N and K(N,0)=0. The adaptive angular metric lies between (1/64)min(1,K h) and min(2,K h). For N>=1 and 0<delta<=2^-10, optimal supplied-description length is log2(1+K/delta)+O(1), uniformly in noise, horizon and accuracy.
The exact finite programme upper bound controls references, adaptive feedback and bounded stopping. Finite GHZ blocks with an elementary Bernoulli product bound give the reverse modulus; no local Fisher-information inference substitutes for a finite-distance proof.
Two rational circle charts yield legal effects. Appending labelled rank-bounded conditional states contributes (V/2)log2N+Vlog2(1/delta), where V=sum_y[r_y(2n-r_y)-1]. Rational visibility gives rational Choi centres, and encoded conditional state ranks never increase.
Classical simulation and the familiar metrological noise crossover are credited to primary antecedents. The new claim is the noise-uniform finite-use covering/rational-code consequence, not invention of those principles. The v72 observable projective-readout and seizing results are inherited with their full proofs.
All sixteen required and twenty-six detailed r46 comments are mapped in RESPONSE_TO_REFEREE.md. No independent priority opinion, author signature or journal acceptance is claimed. Every analytic A/B/C/D aggregate flag remains false.

New quantitative locations:
- `thm:noisycoding73`: 14.1, page 34.
- `lem:noisyupper73`: 14.2, page 34.
- `lem:bernoullimajority73`: 14.3, page 35.
- `lem:noisylower73`: 14.4, page 35.
- `cor:noisyexponents73`: 14.5, page 36.
- `cor:noisypreparation73`: 14.6, page 36.
- `rem:noisyscope73`: 14.7, page 37.

New exact regression: 6461 assertions; 189 readout cases; 72 GHZ block cases; 8 conditional cases; 30 negative controls. Normal and optimized outputs agree. All nine inherited suites execute unchanged.
Preserved: 197 predecessor native files and 482 prior complete-edition labels; current complete edition has 502 labels. Zero unresolved references/citations and zero overfull/underfull boxes.
The native archive and minimal journal package rebuild independently without historical PDFs. Finite regression, written proof, source identity, independent priority and acceptance remain distinct assertions.
Work branch: `revision/general-theta-foundations-i-v73-noisy-readout-crossover-2026-10-04`.
Referee branch after exact-head reconstruction: `revision/general-theta-foundations-i-v73-referee-ready-2026-10-04`.
Package hashes: `papers/GTF-I-v73-noisy-readout-crossover/evidence/PACKAGE_MANIFEST.json`. Final-head attestation remains external.
