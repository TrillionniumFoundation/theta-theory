# Response to the controlling referee reports — Revision 73

**Quantitative manuscript:** *Noise-Uniform Readout Geometry and Reusable Instrument Descriptions*.
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.
**Controlling report:** v71/r46, `b78c1dddd41de645edf207bc415406b3fc1b5e83`.
**Companion proof/pipeline audit:** `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.
**Mathematical predecessor:** completed v72 `12296ed387dbc197ff7cb854d3a78d0bf964960e`.

We thank the referee for separating mathematical correctness from scope and significance and for identifying the precise next boundary: varying readout and coupled noise/coherent directions. The general-journal mathematical objective is unchanged. We do not answer by deleting earlier results, relabelling a description invariant as memory, or asserting that implementation tests certify novelty.

Revision 72 had already been completed before the present revision began. It treats observable varying projective readout and uniformly seizable families, with a direct rational projector chart. No separate external report on v72 was located. These results are inherited here with their proofs; the new mathematical response addresses a different remaining issue, the nonuniform positive-margin constant as a noisy readout approaches the projective boundary.

## Principal mathematical response

Section 49 considers E_theta,lambda^±=(I±lambda(cos theta sigma_1+sin theta sigma_2))/2 with both classical labels retained and public lambda in [0,1]. Set

    K(N,lambda)=lambda * min(N,sqrt(N/(1-lambda^2))),
    K(N,1)=N, K(N,0)=0.

For every angle pair, the full reference-assisted adaptive N-call distance is between (1/64)min(1,K h) and min(2,K h). For 0<delta<=2^-10, arbitrary-centre covering and rational-circle covering are therefore both of order 1+K/delta, with constants uniform in noise, horizon and accuracy. This supplies log2(1+K/delta)+O(1) description bits. Public visibility may depend on both horizon and accuracy. At lambda=0 the basis is erased exactly, while lambda=1 recovers the linear coherent resolution. The theorem does not assume a fixed positive eigenvalue margin as lambda tends to one.

The upper proof uses two common projective endpoints for each pair and retains their exact finite-product fidelity. This gives a common-processor bound for every adaptive tester, including reference systems and bounded public stopping. It is not a common seizer of the entire circle. The lower proof prepares GHZ blocks of explicitly chosen finite size, obtains opposite parity biases lambda^k sin(kh/2), and proves the needed Bernoulli-product estimate directly from a finite majority polynomial. Different angular regimes require different block lengths; no unjustified local-to-global extrapolation is used.

The exact rational code selects one of two semicircle charts and a single integer digit. It makes no trigonometric or floating-point decision. Every accepted chart word decodes to positive effects with the exact promised visibility. A conditional-state corollary adds the rank-stratum contribution (V/2)log N+V log(1/delta). Its lower proof uses a maximally mixed input to isolate fixed half-weight conditional states uniformly in visibility, and its upper code combines the circle with the inherited singular state factors. Conditional ranks do not increase.

The classical simulation method and noise-dependent metrological crossover are established antecedents, prominently credited to Demkowicz-Dobrzanski–Kolodynski–Guta. Common adaptive environment processing is credited to Das–Wilde, Wilde–Berta–Hirche–Kaur, and Wang–Wilde. The asserted addition is the explicit noise-uniform finite-distance family covering, legal rational codec and conditional-rank consequence, not the invention of the familiar crossover or GHZ principle. Independent priority review remains genuinely external.

## Sixteen required revisions

| R46 item | Treatment in this revision |
|---|---|
| 1. Focused submission object | The quantitative paper leads with the noise-uniform theorem. The structural article remains independent; the full research edition preserves all previous proofs. |
| 2. Attribution of v70/v71 | The coherent tensor result is still v70, full-error and fixed-readout are v71, observable varying readout and seizing are v72. Section 49 is v73. |
| 3. Environment literature | The three requested direct comparisons introduced in v72 remain intact. A further metrological comparison distinguishes an exact finite-distance cover from local precision or discrimination exponents. |
| 4. Fixed-readout hypothesis | Every retained v71 statement keeps its fixed basis. Varying projective basis is a separately proved v72 family; noisy equatorial readout is explicitly defined as a new family. |
| 5. Fixed public convention | Page one lists dimensions, rank bounds, horizon, error and public visibility. Only reusable payload is counted. Noise is uniform but not an encoded unknown coordinate. |
| 6. Unhalved norm | The definition of d_N stays before use. Classical event differences are half the displayed distance; the majority lemma includes this factor. |
| 7. Centre versus rank | Retractions remain memoryless-centre results and can increase ranks. The noisy theorem uses arbitrary-centre packing without claiming a retraction. Conditional rank preservation belongs to the exact encoder. |
| 8. Sandwich versus equality | Noisy d_N has two-sided bounds, not an asserted exact formula. Fixed-readout retains its N-use sandwich. The stronger v72 equality still requires ambient uniform seizing. |
| 9. Error ranges | Retained half-dimensional laws keep every fixed submaximal cap below two. New noise-uniform angular coding is proved for delta<=2^-10; conditional coding has a fixed small cap. No coherent large-error inference is made. |
| 10. Programme hardware | Pair-dependent programme bits are an upper-proof device, not an implementation-resource budget. The rational code specifies a quantum operation. |
| 11. Learning | Inputs are supplied matrices/rational coordinates. No estimator of an unknown device or visibility is claimed. |
| 12. Real/rational input | The metric and covering are real-parameter theorems. Rational visibility and unit-circle coordinates have an exact rational CLI. Centres at an arbitrary real public visibility need not have rational matrix entries. |
| 13. Legal codewords | Headers, index range, canonical rational strings, schemas, CP/TP legality, nested rank promises and complete target replay are checked. Arbitrary JSON bodies are not codewords. |
| 14. Exact final head | Source qualification, generated publication and read-only final request are separate. An external exact-head artifact is required before the referee alias is created. |
| 15. Independent priority | Author-side primary comparison is strengthened; no human priority report is invented and no code test is described as one. |
| 16. Analytic graph | Every A/B/C/D aggregate flag remains false. No finite-dimensional coding result is credited with an independent analytic gate. |

## Twenty-six detailed comments

| R46 local item | Treatment |
|---|---|
| 1. Definition of d_N | The focused introduction retains common testers, references, feedback, memoryless slots and bounded stopping before the first new formula. |
| 2. Normalized Choi | The retained 1/d convention in test states is unchanged. The new decoded matrices are input-first unnormalized Choi matrices E^T tensor rho, explicitly distinguished from test-state normalization. |
| 3. Common sigma-algebra | The inherited full-error proof keeps one common estimator. Each new pairwise test uses the same parity/majority output alphabet under both hypotheses; it is not substituted into the common-estimator theorem. |
| 4. Cap approaching two | No old full-error constant is made uniform at two. The new absolute small-error cap is stated numerically. |
| 5. Estimator optimality | The retained Choi estimator is informationally complete, not claimed optimal. The new proof is binary discrimination rather than tomography. |
| 6. Compact inverse chart | Rank-state lower patches and their inverse Lipschitz constants remain. The new circular metric uses two explicit rational charts with angular speed at most two. |
| 7. Row normalizations | The old subtraction of one per cq row is retained. In the new conditional-state result each of the two states is trace one, giving one subtraction per state. |
| 8. Readout/output distinction | The new equatorial effects are genuinely input dependent; arbitrary noncommuting singular conditional states are allowed. Retaining the outcome is essential. |
| 9. Retraction composition | The old input-side dephasing and the v72 superchannel are unchanged. No unproved noisy-circle retraction is added. |
| 10. Memoryless centres | All new and inherited unrestricted centres are legal memoryless instruments, not arbitrary memoryful processes. |
| 11. Programme overhead | A pairwise N-bit programme and 2N conditional state programmes are proof resources. Their size is not the compressed payload or processor hardware. |
| 12. One-use equality | The new binary effects have exact d_1=2lambda sin(h/2); its proof includes an entangled reference bound. Multi-use noise gives bounds only. |
| 13. Pivot masks | Inherited state pivot masks remain charged. The new circle chart sign and integer coordinate index are charged in fixed_length_bits. |
| 14. Zero/rank preservation | The singular state encoder retains zeros and does not increase conditional state rank. Fixed visibility preserves the effect spectrum. The lambda=0 readout collapses to one codeword. |
| 15. lcm denominator | Expanded Choi denominators are separate from the compressed index and factor digits. JSON transport size is not the theorem's payload. |
| 16. Canonical replay | Verification compares the complete canonical object after re-encoding the supplied target; extra nested fields and changed certificates are rejected. Bare decoding supplies no unknown-target guarantee. |
| 17. Projective unitary gauge | The inherited dimensions d^2-1 and d^2-d remain distinct. The new equatorial circle retains ordered outcome signs and does not quotient theta by pi. |
| 18. Atlas complexity | The old general unitary search keeps its stated complexity boundary. The new two-chart rational map has a direct finite encoder, not a retroactive improvement claim for the old search. |
| 19. Pair-dependent witness | The new GHZ phase and block length may depend on the two known alternatives, but not on the unknown hypothesis. This suffices for metric packing. |
| 20. Full-error coherent transition | Noise-uniformity is not large-error uniformity. The proof does not infer a global successful estimator or all-error coherent cover from pairwise tests. |
| 21. Structural probes | The unchanged structural proof remains about fresh repeatable nondisturbing classical probes, not repeated observation of one unknown quantum system. |
| 22. Authorship | A final-head reconstruction is a source/artifact check, not an author signature or independent proof review. |
| 23. Finite tests | GHZ probabilities, majority derivatives, exact rounding, endpoint collapse, ranks and malformed envelopes are finite regression only. Written proofs control continuum angles and all adaptive testers. |
| 24. Aggregate flags | All five existing analytic aggregate flags remain explicitly false. |
| 25. Introduction | The new finite-use noise-uniform modulus and joint coding law lead the focused abstract/introduction. Revision genealogy is in the history note. |
| 26. Next mathematical boundary | The projective boundary is now approached with noise-dependent constants controlled. General nonrecoverable readout, unknown noise coding, large-error coherent covers and coupled tangent geometry remain separately formulated, not answered by deletion or a claim of generality. |

## Preservation and reproducibility

The v73 branch was created directly from completed v72 and anchored remotely before substantive assembly. The predecessor native archive has 197 files; its complete proof graph has 482 mathematical labels. They remain at their prior repository paths and all active labels remain in the new complete edition. Earlier front matter and replaced audit records are additionally retained under `predecessor-v72-audit/`. The exact source manifest verifies rather than assumes this preservation.

The three manuscripts, all ten regression suites, complete source reconstruction and independent minimal journal reconstruction are executed by the build. Results, page counts and hashes belong to the actual receipt, not this letter. Source qualification and a separate read-only final-head run do not certify independent priority, a cryptographic author identity or editorial acceptance. No submission target has been changed.
