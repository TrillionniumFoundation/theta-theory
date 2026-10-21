# Preserved first strict execution and verifier correction

The first source commit `a05bed516b86ea1273ff542e1b2988cd326da214` was published
before strict execution. Its real-SHA run stopped at the predecessor Git-tree
inventory, before any native build or mathematical diagnostic. The actual
`BUILD_FAILURE.json` is preserved here without alteration.

The fixed old subtree was not missing: the `git ls-tree` call used the current
paper directory as cwd and therefore applied that path prefix inside the
already selected old subtree. The original command returned zero entries;
adding `--full-tree` returned all 275 expected predecessor files. A further path audit found that the old working-tree diff also needed a
repository-root pathspec. The correction therefore uses `--full-tree` for the
subtree enumeration, `:(top)` for that worktree pathspec, and `--no-relative`
for changed-path reporting. It retains every inventory, scope and byte-identity
check, and changes no mathematical TeX. `CORRECTION.json` records the two verifier
identities. A new append-only source commit and full strict run are required;
the failed commit is neither rewritten nor reported as passing.
