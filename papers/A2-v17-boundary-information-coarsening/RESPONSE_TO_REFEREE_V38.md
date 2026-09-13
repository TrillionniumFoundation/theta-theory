# A2 v38 — response to the v37 referee

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 13, 2026

This revision responds to [the complete v37 report](../../reviews/a2-v37-external-harsh-top4-2026-09-13/REFEREE_REPORT.md) at review commit `377efa79597776e75e3cc1d399c1986edd097aaf`. That report examines v37 submission `6c311aa389e3af833f06f14ae98de7bfc28c1327`. The present branch descends from the review commit, retaining the reviewed manuscript and the report together.

The mathematical changes are committed at `c206a27ba01f20f1a21b780e6d71c77a837ef11d`; the complete inherited native source and the repaired build tools are at `7d34d96a7c2dd974ab3725e009bbb584d3228114`. The revision branch is `revision/a2-v38-source-pinned-native-referee-response-2026-09-13`.

The manuscript retains its relative-law, all-order inverse, intrinsic periodic-rigidity, compact-experiment and charged-acquisition conclusions. The changes below align the introductory statements with the detailed theorems and remove an unnecessary ambiguity in the dependency order of the statistical proof. The source-provenance defect is repaired in the build implementation, not merely described in this response. **C2 remains open: a complete-main PDF and its visual inspection have not been delivered in this session.** The actual executions and their distinct scopes are documented below.

## Disposition of the report

| Comment | Revision and evidence | Present disposition |
|---|---|---|
| E2, accepted in v37 | The detailed single-offset theorem still states realizability, common-frame rank-two anchoring and rooted signature-rigid propagation to every obstacle orbit. Its source is unchanged. | Accepted repair retained. |
| R37-M1 | The abstract and introductory rigidity theorem now use the common-frame rank-two anchoring pair. The introductory theorem cites its definition, and its proof explicitly cites the full periodic-rigidity theorem for rooted propagation. | Addressed in the native manuscript. |
| R37-M2 | The short contiguity proof now invokes the existing normalized-likelihood argument and states that no alternative central-sequence limit is assumed. | Addressed in the native manuscript. |
| R37-V1 | The builder now freezes Git-object bytes, hashes actual compilation inputs, requires recorder and recursive input coverage, and distinguishes generated data. Forty-one finite regression tests pass in ordinary and optimized Python. | Reproduced failure modes addressed; implementation and execution evidence supplied for independent verification. |
| C2 | A genuine seven-page native companion was built and inspected. The complete hosted build had no executed steps or artifacts. The complete native main was not locally built. | Open; no complete-build or submission-readiness certificate is claimed. |
| I1, accepted in v37 | Both current navigation pages identify v38 and link to the present response, verification and preservation records. Earlier navigation is preserved. | Maintained. |

## 1. Common-frame anchoring and complete periodic reconstruction — R37-M1

The introductory theorem `thm:v26-intro-rigidity` now assumes that the marked data are realizable by a periodic table and that the measured graph contains a rank-two anchoring pair based at one channel frame, as defined in `def:v24-rank-two-anchoring`. The rooted signature-rigid spanning tree must reach every obstacle orbit. The abstract now states the same common-frame anchoring requirement and identifies the rooted tree as signature-rigid.

The introductory proof distinguishes two applications. The theorem `thm:v24-lattice-gram-recovery` determines the lattice in a chosen common frame; `thm:v24-uncalibrated-periodic-rigidity` supplies propagation to the complete marked table. In the common frame, the measured translation holonomies form a matrix V and the independent marked deck displacements form a matrix M. Thus L = V M^{-1}, and the marked Gram matrix is M^{-T} V^T V M^{-1}. This is not a placement theorem for obstacles outside the anchoring cycles. Their placements are fixed successively by the rooted signature-rigid tree. Realizability supplies existence and admissibility; the recovery and propagation supply uniqueness modulo a single common SE(2) motion.

The detailed single-offset theorem, its proof, the lattice chapter and the definition of an anchoring pair are preserved byte-for-byte. In particular, the two independent deck displacements are not required to form an integral unimodular basis. No ambient position samples or prescribed lattice metric have been added to the intrinsic observation map.

Locations: [main abstract](main.tex), [introductory theorem and proof](article/01_introduction_v27.tex), [unchanged detailed composition](article/23f_single_offset_law_inverse_v26.tex), and [unchanged lattice and full-table theorems](article/23d_rank_two_lattice_recovery_v24.tex).

## 2. Noncircular contiguity — R37-M2

The proof of `lem:v22-contiguity` now refers explicitly to the normalized-likelihood argument in `prop:v34-tilting-moments`. For a convergent bounded local sequence, the null LAN expansion gives a strictly positive limiting likelihood of mean one. Convergence of bounded truncations, together with the unit means of the prelimit likelihoods, gives uniform integrability and forward contiguity. Positivity of the null-law limit gives reverse contiguity. Subsequence extraction treats a general bounded local sequence. The common-space censoring coupling transfers the assertion to the original moving-support experiment.

This part of the argument requires the null LAN expansion and likelihood normalization, not a central-sequence limit under an alternative. The forward reference to the detailed proposition therefore specifies an already independent argument rather than a circular invocation of the theorem being proved.

The original-alternative density expansion, alternative mean, centered fourth-moment estimate and compact-local quadratic-risk argument are unchanged. In particular, an excluded observation contributes zero to the central sequence; its occurrence does not discard the other observations in the sample. The unbounded quadratic-risk conclusion is not inferred from total variation alone. The separate Hellinger-modulus and finite-net passage to compact experiments is also retained.

Locations: [short proof](article/18a_vector_boundary_information_v26.tex), [unchanged detailed tilting and moment proof](article/18a2_likelihood_tilting_moments_v34.tex), and [unchanged compact-experiment passage](article/18a1_compact_experiments_v32.tex).

## 3. Actual-input provenance — R37-V1

The reported defect was substantive: a recorder naming a temporary compilation copy did not justify hashing a different file in the original source directory. Nor could an absent recorder be accepted as an empty but successful source inventory.

The new [build driver](tools/build_submission.py) and [provenance module](tools/source_provenance.py) replace those behaviors. They construct a frozen source snapshot from the declared Git commit's objects, record the commit and tree identities, and verify each blob's bytes and SHA-256 digest. The manuscript working-tree scope must be clean. Untracked and ignored files cannot enter the Git-object snapshot; symbolic links and unsafe paths are rejected. Previously tracked root build products are explicitly listed as excluded rather than reused as fresh output.

After each native build, the recorder must be nonempty, name the correct working directory, include the native entry and cover every recursive static TeX input. The verifier reads and hashes the actual compilation files and compares them with the frozen manifest. Missing, mutated or unexplained inputs fail the build. Installed TeX dependencies have a separate actual-input inventory; their font files are not distributed as standalone assets.

Generated auxiliary inputs are not presented as frozen source. In particular, the main's external references require `two_collision.aux`. That file is transferred only from a successful, source-verified companion build, with its producer, source commit, PDF digest and recorder digest recorded. Its bytes are checked again when consumed by the main, and its occurrence in the main recorder is mandatory. This dependency is necessary for a complete native build and is tested explicitly.

Forty-one finite software regressions were executed in normal and optimized Python, with byte-identical output. They include the exact new driver's matching-copy control and rejection of divergent compilation bytes, absent recorder and absent native entry. External processes in those unit cases are deliberately mocked. A separate genuine-TeX integration run exercised the exact full CLI on labelled one-page fixtures, including the cross-document auxiliary transfer. Neither class of tests is represented as an A2-main build. The old builder is preserved unchanged under [history/v37/tools](history/v37/tools/build_submission.py).

The trust boundary remains Git and the installed compiler/toolchain. The verifier is not an attestation against a malicious compiler or a transient change-and-restore attack during a read. The [verification ledger](VERIFICATION_V38.md) records both the achieved checks and their scope.

## 4. Complete native delivery — C2

The complete-main requirement is retained without substitution by an abridged entry, a wrapper with omitted modules, or a new mathematical statement. All 52 direct inputs of `main.tex` and the unchanged 36-input auxiliary compendium remain in the native source chain.

The new hosted task targeted the complete source at `7d34d96a7c2dd974ab3725e009bbb584d3228114`. Run `34743133630`, job `103686134246`, ended in failure with no executed steps, no assigned runner identity and no artifacts. The returned metadata do not establish the underlying cause and record no executed TeX command. This is not reported as a compiler failure, much less as a successful main build.

Separately, the exact unchanged native companion source was checked against its remote Git blob, compiled using the repaired verifier and rendered for inspection. It produced seven pages with no unresolved-reference, duplicate-label, missing-glyph or overfull-box report. All seven rendered pages were inspected. Its PDF, source package and raw local evidence accompany this revision's conversation; their identities are recorded in the ledger. This supplies companion evidence only.

The complete native main has not been compiled or visually inspected in this session. C2 therefore remains open. The [native build protocol](NATIVE_BUILD_PROTOCOL_V38.md) states the exact required execution and deliverables; the existence of that protocol or workflow is not counted as their execution.

## 5. Retained mathematical checks and scope

The six finite mathematical families used by the preceding referee were independently re-executed here from their unchanged, hash-verified script: asymmetric four-density inversion, leading contact recovery and finite jet blocks, nonlinear finite half-line envelope coefficients, lattice/Gram/common-reflection identities, the moving-ceiling layer budget, and the original-alternative mean. All six passed in normal and optimized Python with identical output. The historical commit field inside that unchanged script remains historical; the present execution ledger does not relabel it as a full v38 source audit.

These checks do not replace the analytic proofs. In particular, the radial probability examples are not asserted to be billiard-realizable, finite jet blocks do not certify an infinite-order condition bound, and a finite stationary solve is not the weighted half-line theorem. The [historical dependency audit](HISTORICAL_DERIVATION_AUDIT_V38.md) identifies the actual derivations consulted and distinguishes them from the inherited report's bounded dispositions.

The article continues in theorem–proof form. Referee dispositions, build status and version history are kept in separate documents. No theorem, observation level, appendix or mathematical workstream has been removed to make the present checks pass.
