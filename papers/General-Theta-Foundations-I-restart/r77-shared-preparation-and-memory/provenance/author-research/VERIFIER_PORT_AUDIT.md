# Read-only R74 verifier and source-sealer port audit

This is a separate author-team AI code/provenance inspection. It is not a
native build receipt, a theorem proof, hosted CI, or a referee assessment.
No repository files, Git configuration, refs, or index were modified by this
audit. The author was editing the port during inspection; the final inspected
snapshot was captured at `2026-10-20T12:59:05.990370+00:00`.

| Snapshot | SHA-256 |
|---|---|
| `verify.py`, 23,792 bytes | `9647a69d2ab6deebd937612596c98f5b689f27a470ace625be016c07f69ecd7e` |
| `seal_source.py`, 11,599 bytes | `a1480b81f6aaa579b30ce995a3d9f2bbf13a9f0973f9df9efc4eb255f36fe53e` |

The exact snapshots and read receipt are in `r74-research/verifier-audit-snapshot/`.
Later edits require the final source-bound execution and receipt; this record
does not authenticate a later commit by implication.

## Port findings and dispositions

1. The first inspected port still had 185 current statements, fourteen total
   diagnostic suites, and a literal `CURRENT_COUNT` in its failure message.
   These were communicated and corrected during inspection. The captured
   snapshot expects **201 current statements**, preserves **185 inherited
   statements**, and registers **18 diagnostic suites**: fourteen inherited
   suites and four R74 suites. A separate recursive traversal of the actual
   main/supplement input closures found exactly 201 distinct statement labels,
   all 185 inherited labels, and no duplicate labels. This traversal does not
   replace the final compiled number/page comparison.

2. The remaining `DIAGNOSTICS[:14]` and count fourteen in the inherited-source
   receipt are intentional: those are the fourteen byte-preserved R61–R73
   scripts, not the total R74 suite count. The R73 predecessor path, R73 tree,
   old index, and inherited count 185 are likewise valid historical controls.
   They must not be replaced by R74 identities simply because their names are old.

3. The three new author diagnostic scripts expose a positive `total_checks`,
   consistent exact/floating totals, and grouped counts in the schema accepted
   by `diagnostic_counts`. Their ASTs contain no `assert` statements. The
   separately authored `challenge_c2_four.py` was updated to that schema and
   now contains the full robust-witness checks. Its exact source SHA-256 is
   `cdecc602737d0eafa45536c47c51fb6db1c7b6fa5e3f94ffdc9ce5dbe51772cf`.
   Actual ordinary and optimized executions give byte-identical JSON and
   5,170 exact checks. The final source must include this version, not the
   earlier 1,197-check file lacking the grouped-count schema.

4. The sealer's actual `pinned_body_checks` passed on the working source:
   47 retained current bodies; the 32,284-byte supplement suffix with SHA-256
   `a1505059fc305c8918875445ca07b5c69e79b16f1d247e402bad8089b101ead7`;
   all 185 inherited labels; the pinned R65 report; and all 34 files of the
   R58 companion, whose tree is `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`.
   Separately, every retained body's blob was compared with the actual R73
   publication commit, with zero mismatches. The supplement suffix was also
   independently extracted from that actual predecessor blob and matched in
   bytes and SHA-256. Thus the suffix identity is currently authentic.

5. One reproducibility improvement remains available: strict Git verification
   binds every listed retained body and the inherited theorem index to the
   actual predecessor objects, but it does not itself re-extract the old
   supplement suffix. It trusts the declared suffix hash after checking the
   current bytes. Add the same direct predecessor-blob extraction used in
   this audit if the strict receipt is intended to re-establish that old/new
   suffix identity without this separate audit. This is an assurance gap in
   the executable check, **not an observed suffix mismatch**.

## Source and build gates that must remain

The strict path correctly requires the declared full commit SHA to be the
actual Git HEAD, recomputes the complete current source tree, compares it to
that commit, preserves the full R73 tree, checks R73 ancestry, and confines
all committed changes relative to R73 publication to the independent R74
folder. The local source inventory includes every regular file; symlinks and
nonregular entries are rejected. The original report's bytes are pinned.

The paired build uses native `pdflatex` without shell escape, three passes
for each current document and the companion, fresh output directories,
cross-document label files, and final-log rejection of undefined references,
duplicate labels, unresolved reruns, and overfull boxes. It compares the
compiled theorem index with the sealed source index. Strict mode rechecks
the manifest, complete source tree, and Git HEAD after execution. Draft mode
cannot issue the final PASS and cannot authenticate a source commit.

The final sequence therefore remains: integrate the final proofs and all
four R74 scripts; obtain the actual compiled index; update the source seal;
commit the complete source; then execute strict verification on that exact
HEAD into a fresh output directory. Record its real diagnostic totals and
PDF hashes. A publication artifact, visual inspection, hosted Actions run,
or remote push needs its own actual matching identity. The present code
inspection does not claim that any of those later steps has occurred.

## Follow-up after the inheritance correction

The author removed four duplicate R68 numbered statements from the active
R74 packet, retaining their drafts as superseded research and the complete
stronger R68 source as current authority. The later inspected port therefore
correctly uses **197 current labels**, not the earlier snapshot's 201.
The 185 inherited labels and eighteen registered diagnostic suites remain.
This is an intentional mathematical-authority correction, not missing proofs.
The additional dictionary/instrument diagnostic now validates retained R68
mathematics rather than certifying a new R74 theorem.

The suggested direct predecessor-suffix verification was also implemented:
strict mode retrieves the actual R73 `supplement.tex` blob, checks that the
retained marker occurs once, extracts the suffix, and compares its byte
count and SHA-256 with the declared identity. The associated receipt flag
is `predecessor_supplement_suffix_verified`. The assurance gap in item 5
is therefore closed in this later code version.

The follow-up source identities actually read were:

| File | SHA-256 |
|---|---|
| `verify.py`, 24,572 bytes | `135a36cd804da34111497d2bb9923f97023ff7eb162587449e367b71ecaff188` |
| `seal_source.py`, 11,599 bytes | `8ac38aafe5754938fa7a2171c4776b68c7e6bc6784a459281c56c7c127350982` |

No remaining stale R72/R73 control or statement-count hardcode was identified
in the executable port at this follow-up. Final execution on the actual sealed
source commit remains the gate for a native-verification PASS.
