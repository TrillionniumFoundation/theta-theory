# C30a supplemental audit-closure protocol (additive v1)

## Release-authorizing additive v5 amendment

The older v1/v2/v4 layouts and commands retained below are historical design
records only.  They cannot mint supplemental authority.  The sole
release-authorizing implementation is the pinned additive v5 pipeline:

```text
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_common.py
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_trace_lib.py
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_comparator.py
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_trace_auditor.py
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_release_checker.py
deliverables/cm2_round306c30a_supplemental_audit_closure_v5_offline_pipeline.py
```

Every v5 stage runs in a digest-pinned Docker image with kernel network mode
`none`, a read-only root filesystem, all capabilities dropped,
`no-new-privileges`, IPC mode `none`, a numeric non-root user, a read-only
workspace bind, and only run-root-owned writable binds.  A host that cannot
prove those settings from both raw and canonical pre/post Docker inspection
must fail closed.  Syscall traces are additional observed-zero evidence; they
are not substituted for kernel isolation.

The mandatory order is real base precheck, v5 preflight, fresh runtime rebuild
and re-attestation, two true `PYTHONHASHSEED` producers, comparator, verifier
manifest-pre checks, two independent verifiers, verifier manifest-post checks,
ten coherent attacks, independent full-trace recomputation, real base
postcheck, then the five-layer mint.  A stage receipt must bind the original
stdout, stderr, GNU-time report, process/container exit, signal/OOM state,
start receipt, Docker-create streams, and raw plus canonical Docker inspection
from that same invocation.  A GNU-time report containing any
`Command terminated by signal` line is a failure even if it also contains
`Exit status: 0`.  Retrospectively created stderr or numeric-exit files are
forbidden.

The comparator and post-attack trace auditor independently close every nested
analyzer result digest.  Their only allowed normalization is the explicitly
pinned provenance-specific `contract.source`.  Candidate absence, successful
exclusive `mkdir`, absent pycache prefix, zero successful `.pyc` reads, and
zero network syscalls are all recomputed from each retained complete producer
trace; none may be hard-coded.

The five original publication layers are not by themselves authority.  After
their six official targets (sealed directory plus payload, cold, outer, root,
and terminal files) are published with no-replace renames, stage 100 must
replay the complete terminal chain.  Only then may a pipeline-precommit receipt
bind all six official target hashes and the full stage-100
stdout/stderr/time/exit/inspection evidence.  A final checker recomputes that
receipt and writes, with exclusive create, this additional object:

```text
deliverables/cm2_round306c30a_supplemental_audit_closure_final_commit_receipt.json
```

The staged bytes must equal the successful checker invocation's sole stdout,
and publication uses Linux `renameat2(RENAME_NOREPLACE)`.  **No externally
pinned final-commit receipt means zero supplemental authority**, including
after a partial six-target publication, a failed stage-100 replay, or a failed
final checker.  This amendment adds no mathematical credit: the only C30a
transition remains `252 -> 92`, and CM2 remains `NO-GO_FOR_CLAIM`.

## Non-negotiable boundary

This protocol does not alter the original 13-member C30a seal.  Its trust-root
manifest remains

```text
deliverables/cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_promotion_manifest.sha256
SHA256 0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc
```

The only legal C30a ledger transition is `252 -> 92`: 160 whole-origin
exclusions plus two inherited-H holds.  `252 -> 90` is forbidden.  A
supplemental audit failure changes no existing credit and cannot invalidate or
rewrite any C30b/C30c pin.

This file is a run protocol, not a minted closure.  The closure exists only
after every expensive step below passes, all raw evidence is copied into the
fixed sealed directory, an additive manifest is created, and the manifest hash
is independently pinned.  Until then the supplemental formal credit is zero.

## Additive executables

The following new files are outside the original seal:

```text
deliverables/cm2_round306c30a_supplemental_audit_closure_controlled_replay_launcher.py
deliverables/cm2_round306c30a_supplemental_audit_closure_coherent_attack_harness.py
deliverables/cm2_round306c30a_supplemental_audit_closure_independent_verifier.py
deliverables/cm2_round306c30a_supplemental_audit_closure_protocol.md
```

The controlled launcher pins the original producer SHA256
`41a3f11c...c91714`.  It performs one in-memory byte change at offset 36,078:
the exact guard `sys.flags.isolated == 1` becomes `== 0`.  The transformed
producer SHA256 is
`6105ad2e3aeffbd2a27063a7e9b56cdadaeb22e8e96f8daf987f0a5763ac923e`.
No file is patched on disk.  This narrow transform is required because CPython
`-I` ignores `PYTHONHASHSEED`; the historical two `-I` runs are therefore two
byte-identical replays, not controlled-hash-seed evidence.

The launcher permits only seeds `30630071` and `30630929`.  On the pinned
CPython 3.12.3 they must produce distinct probes:

```text
30630071 -> 8841297538927089933
30630929 ->  889641737497572634
```

The persistent attack harness repeats the original nine attacks and adds
`held_to_promoted_162_overclaim_full_reclosure`.  It retains every forged four-file
candidate, mutation descriptor, raw verifier stdout/stderr, and exit JSON.

## Fixed evidence names

Use a never-reused scratch directory created beneath `.cm2-runtime/audit/`.
On any interruption or failure, retain it and create a new directory; do not
clean and reuse a partial run.  The successful run is copied byte-for-byte to:

```text
deliverables/cm2_round306c30a_supplemental_audit_closure_sealed/
```

The sealed directory must have this top-level layout:

```text
00_base_manifest_pre.stdout
00_base_manifest_pre.stderr.raw
00_base_manifest_pre.exit.txt
01_preflight.stdout.json
01_preflight.stderr.raw
01_preflight.exit.txt
02_runtime_attestation.stdout.json
02_runtime_attestation.stderr.raw
02_runtime_attestation.exit.txt
03_seed30630071.provenance.json
03_seed30630071.producer.stdout.json
03_seed30630071.producer.stderr.raw
03_seed30630071.producer.exit.txt
03_seed30630071.producer.time.txt
03_seed30630071.producer.trace.raw
03_seed30630071.candidate/
04_seed30630929.provenance.json
04_seed30630929.producer.stdout.json
04_seed30630929.producer.stderr.raw
04_seed30630929.producer.exit.txt
04_seed30630929.producer.time.txt
04_seed30630929.producer.trace.raw
04_seed30630929.candidate/
05_controlled_seed_comparison.sha256
05_controlled_seed_comparison.stdout
05_controlled_seed_comparison.stderr.raw
05_controlled_seed_comparison.exit.txt
06_seed30630071.verifier.manifest_pre.stdout
06_seed30630071.verifier.stdout.json
06_seed30630071.verifier.stderr.raw
06_seed30630071.verifier.exit.txt
06_seed30630071.verifier.time.txt
06_seed30630071.verifier.trace.raw
06_seed30630071.verifier.manifest_post.stdout
07_seed30630929.verifier.manifest_pre.stdout
07_seed30630929.verifier.stdout.json
07_seed30630929.verifier.stderr.raw
07_seed30630929.verifier.exit.txt
07_seed30630929.verifier.time.txt
07_seed30630929.verifier.trace.raw
07_seed30630929.verifier.manifest_post.stdout
08_attacks/
08_attacks.harness.stdout.json
08_attacks.harness.stderr.raw
08_attacks.harness.exit.txt
08_attacks.harness.time.txt
09_base_manifest_post.stdout
09_base_manifest_post.stderr.raw
09_base_manifest_post.exit.txt
10_invocations.json
11_trace_audit.json
12_closure_result.json
```

Each candidate directory contains exactly the original four output basenames.
`08_attacks/` contains `attack_summary.json` and exactly ten numbered attack
directories created by the supplemental harness.  Empty stderr/stdout files
are retained as zero-byte files rather than omitted.

The final additive manifest is:

```text
deliverables/cm2_round306c30a_supplemental_audit_closure_manifest.sha256
```

Its first dependency is the original manifest file and its remaining members
are the C30b runtime auditor (unchanged), the four additive files above, and
every regular file below the supplemental sealed directory.  The additive
manifest must not list or overwrite the original 13 members individually.

## Ordered execution

### 0. Create a fresh run and record tools

From the workspace root, create a new directory with `mktemp -d` beneath
`.cm2-runtime/audit/`.  Resolve it to an absolute path and record that path,
the exact argv/environment for every command, `/usr/bin/strace --version`,
`/usr/bin/time --version`, kernel/architecture, and UTC start/end times in
`10_invocations.json`.  Do not use `rm` as part of this protocol.

The locked interpreter is:

```text
.cm2-runtime/python-flint-0.9.0/bin/python
```

### 1. Manifest-first preflight

Before reading a candidate or launching a C30a executable:

```text
cd deliverables
sha256sum -c cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_promotion_manifest.sha256
```

Retain stdout, stderr, and the numeric exit code under the `00_` names.  It
must report 13/13 `OK`; the manifest file itself must hash to the trust-root
SHA above.

Then run the additive preflight with the locked venv and retain all three raw
streams/status files:

```text
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c30a_supplemental_audit_closure_independent_verifier.py
```

The sole stdout object must say
`READY_FOR_EXPENSIVE_SUPPLEMENTAL_REPLAYS__NOT_A_C30A_AUDIT_CLOSURE_PASS`,
formal credit zero, `252_TO_92_ONLY`, and `252_to_90 = FORBIDDEN`.

### 2. Fresh runtime evidence

Run the unchanged, pinned runtime auditor separately so its complete JSON is
retained rather than only summarized by the preflight:

```text
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c30b_python_flint_runtime_attestation_auditor.py
```

The additive closure pins the auditor bytes but does not change its C30b seal.
The fresh attestation must independently establish all of the following:

- resolved `/usr/bin/python3.12` SHA256
  `1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118`;
- CPython 3.12.3 / cache tag `cpython-312` / x86_64;
- glibc exactly 2.39, which is not below the wheel floor 2.17;
- wheel SHA256 `376b88ca...4e4d76` and exactly the two expected
  `cp310-abi3` manylinux tags;
- sealed-wheel RECORD: 113 rows, 112 independently hashed rows, only RECORD
  itself unhashed;
- installed RECORD: 139 rows, all 114 hash-bearing rows verified, exactly 25
  permitted unhashed rows (24 generated `.pyc` rows plus RECORD itself);
- all 112 non-RECORD wheel members byte-identical to the installed files;
- imported `python-flint` 0.9.0 / FLINT 3.6.0 release 30600.

The complete reconstruction recipe, frozen as a recipe rather than falsely
claimed as historical provenance, is:

```text
/usr/bin/python3.12 -m venv --clear .cm2-runtime/python-flint-0.9.0
.cm2-runtime/python-flint-0.9.0/bin/python -I -B -m pip install \
  --no-index --no-deps --only-binary=:all: --require-hashes \
  --find-links deliverables/cm2_round306c30a_runtime \
  -r deliverables/cm2_round306c30a_python_flint_requirements.lock
```

For an audit replay, apply that recipe only to a dedicated fresh copy/path;
do not clear the resident venv in place while C30b/C30c work may be running.

### 3. Two real controlled hash seeds

For each seed, the candidate directory, provenance file, and
`PYTHONPYCACHEPREFIX` must all be absent before launch.  Use `env -i` and
exactly these environment keys: `HOME=/nonexistent`, `PYTHONHASHSEED`,
`PYTHONPYCACHEPREFIX`, `PATH=/usr/bin:/bin`, `LANG=C.UTF-8`, `LC_ALL=C.UTF-8`,
and `TZ=UTC`.
Launch with `python -P -s -B`; never use `-I` for these two runs.

The release-authorizing scrubbed command shape (mandatory for the second
seed, and recommended for both), wrapped by `/usr/bin/time` and
`/usr/bin/strace`, is deliberately full-syscall capture:

```text
strace -f -qq -s 4096 -e trace=all -o TRACE \
  env -i HOME=/nonexistent \
  PYTHONHASHSEED=SEED PYTHONPYCACHEPREFIX=ABSENT_CACHE \
  PATH=/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
  .cm2-runtime/python-flint-0.9.0/bin/python -P -s -B \
  deliverables/cm2_round306c30a_supplemental_audit_closure_controlled_replay_launcher.py \
  --expected-hash-seed SEED \
  --expected-pycache-prefix ABSENT_CACHE \
  --candidate-dir ABSENT_CANDIDATE \
  --provenance ABSENT_PROVENANCE
```

Run seed 30630071 first and seed 30630929 second.  The second run is the
scrubbed replay: it must use a newly created run root, absent candidate, absent
pycache prefix, empty process environment except the exact seven keys, and no
successful `.pyc` read in its raw trace.  The trace must show the candidate
directory's `mkdir` succeeding, not returning `EEXIST`.  This is a scrubbed
process/import/output replay; it makes no unverifiable claim that the host OS
page cache was globally dropped.

A first-seed replay captured with a selective trace may still prove its exit,
seed contract, and output bytes, but that trace is auxiliary evidence only.
In particular, `%file` plus
the ordinary `write*` calls does not cover every descriptor/metadata or
kernel-assisted mutation route (`fchmod`, `fsetxattr`, `fallocate`, `splice`,
`io_uring`, and similar calls).  The release checker therefore rejects any
zero-mutation claim whose retained command is not `trace=all`.

The earlier `-v1-` run roots are retained as fail-closed development evidence
and must never be reused or deleted.  In particular, the completed seed
`30630929` v1 full trace has SHA-256
`8421884d2dd3f7763dc666eeeac5d336062f75f9f677ea70a747ee7f8eb99314`
and contains exactly two successful `socket(AF_UNIX, ...)` calls followed by
two failed `connect("/var/run/nscd/socket") = -1 ENOENT` calls.  Its candidate
bytes remain useful determinism evidence, but the four network syscalls forbid
release use.  The cause was the six-key environment's missing `HOME`, which
made Python startup perform an NSS passwd lookup.

At the time this protocol was updated, the following fresh `-v2-` candidate,
pycache, and provenance targets were all absent.  These are the two directly
copyable launcher calls (wrap them with the strace/time capture above for the
formal run).  If any target has since appeared, choose a new suffix; never
delete and reuse it.

```bash
env -i \
  HOME=/nonexistent \
  PYTHONHASHSEED=30630071 \
  PYTHONPYCACHEPREFIX=/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630071-v2-pycache \
  PATH=/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/python-flint-0.9.0/bin/python -P -s -B \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round306c30a_supplemental_audit_closure_controlled_replay_launcher.py \
  --expected-hash-seed 30630071 \
  --expected-pycache-prefix /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630071-v2-pycache \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630071-v2-candidate \
  --provenance /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630071-v2-provenance.json
```

```bash
env -i \
  HOME=/nonexistent \
  PYTHONHASHSEED=30630929 \
  PYTHONPYCACHEPREFIX=/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630929-v2-pycache \
  PATH=/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/python-flint-0.9.0/bin/python -P -s -B \
  /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round306c30a_supplemental_audit_closure_controlled_replay_launcher.py \
  --expected-hash-seed 30630929 \
  --expected-pycache-prefix /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630929-v2-pycache \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630929-v2-candidate \
  --provenance /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.cm2-runtime/audit/c30a-supplemental-controlled-seed30630929-v2-provenance.json
```

With either exact command, `dict(os.environ)` has exactly seven entries:
`HOME`, `PYTHONHASHSEED`, `PYTHONPYCACHEPREFIX`, `PATH`, `LANG`, `LC_ALL`, and
`TZ`.
The launcher compares the full dictionary, not a subset.

Both launcher provenance objects must pin the original and transformed
producer hashes, record different seed probes, and state preflight-only at the
moment of launch.  Completion is established separately by exit code 0, the
producer stdout object, and the exact four output files.

All four outputs from both runs must be mutually byte-identical and equal to
the original sealed files.  Retain raw `cmp` output/exit and a sorted SHA256
table under the `05_` names.  A hash list without the actual candidate files is
insufficient.

### 4. Independent verifier and manifest-first stdout contract

Immediately before each verifier run, repeat the original 13-member manifest
check and retain its stdout.  Run the unchanged pinned verifier under strace:

```text
strace -f -qq -s 4096 -e trace=all -o TRACE \
  env -i HOME=/nonexistent \
  PATH=/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
  .cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_promotion_independent_verifier.py \
  --candidate-dir CANDIDATE
```

Run this exact five-key verifier environment on both controlled candidates.
`HOME=/nonexistent` is mandatory here too: omitting it can make Python startup
attempt an AF_UNIX NSS/nscd lookup, which violates the zero-network contract.
Retain stdout, stderr, exit, time, and the complete trace; then repeat the
manifest check and retain that output.

The authoritative conclusion must be exactly one newline-terminated canonical
JSON document on stdout, with the independent 12,888 + 160 + 2 reconstruction,
result object SHA `32c449bc...3538e09`, and transition `252 -> 92`.  The trace
must show one authoritative stdout write and no write/open-for-write beneath
either `deliverables/` or either candidate directory.

The pinned R215 dependency emits progress on stderr (historically 50 writes).
Those bytes must be retained and checked as diagnostics only; no conclusion
JSON may appear there.  If the governing meaning of “stdout-only” is instead
literal zero stderr bytes, the closure must fail rather than suppress, filter,
or relabel those writes.

### 5. Persistent coherent attacks

Run the additive harness on one controlled candidate:

```text
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c30a_supplemental_audit_closure_coherent_attack_harness.py \
  --candidate-dir CONTROLLED_CANDIDATE \
  --evidence-dir ABSENT_08_ATTACKS_DIRECTORY
```

All ten attacked verifier invocations must exit nonzero.  The final attack is
the core full held-to-promoted overclaim: it moves both inherited-H holds into
the promotion ledger, forges `160/2 -> 162/0` and `252 -> 90`, and recomputes
row hashes, both ledger descriptors, result counters, remaining partition,
conservation identity, theorem hash, and result hash.  It must still be rejected
by reconstruction from the pinned sources.  The harness must retain the ten
forged candidates and every raw stream/status; summary-only `10/10` text is not
enough.

### 6. Trace audit, post-check, and minting

Derive `11_trace_audit.json` from the retained raw traces, not from the old
C30a verification JSON.  It must enumerate every stdout/stderr write, every
network attempt, all candidate/deliverable write attempts, the successful
fresh candidate `mkdir`, and successful `.pyc` reads.  Any network syscall,
candidate/deliverable verifier write, reused candidate, or successful pycache
read in the scrubbed replay fails closed.

Repeat the original 13-member manifest check into the `09_` files.  Build
`12_closure_result.json` from the raw evidence.  Its only permitted success
status is a supplemental audit closure of the already legal `252 -> 92`
transition; it grants zero new whole-origin exclusions and leaves D02 blocked.

Copy the successful evidence into the fixed sealed directory without changing
bytes.  Generate the additive manifest only after the copy, with paths sorted
bytewise under `LC_ALL=C`; include zero-byte raw files.  Verify the additive
manifest from a separate clean process, record its SHA256 externally, and only
then call P0 audit evidence closed.  Never edit the original C30a manifest or
replace any C30b/C30c source/result file.

## Fail-close matrix

- Any base-manifest mismatch: no closure, existing `252 -> 92` credit remains.
- Any runtime/RECORD mismatch: no closure.
- Equal hash probes, `-I`, extra environment keys, reused candidate/cache, or
  outputs not equal to the original seal: no controlled-seed credit.
- Missing raw stderr/trace/exit, or summary without forged attack candidates:
  no audit closure.
- Any accepted attack, especially held-to-promoted full reclosure: no closure.
- Any result containing remaining `90`, 162 new exclusions, D02 clear, or CM2
  go: reject immediately.
- P0 audit closure never supplies P1 credit; the fixed result stays `252 -> 92`.
