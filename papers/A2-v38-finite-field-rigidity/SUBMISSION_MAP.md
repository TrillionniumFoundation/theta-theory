# Submission map — A2 v38

Entry point: `main.tex`. All required inputs and bibliography are inside this
directory. The core contains 24 unchanged v37 files and three new inputs.

The new overview is `core/00g_finite_field_overview.tex`.
`core/17_finite_stencil.tex` contains the fixed-stencil inverse, arbitrary-data
stability, primal--dual bounds and explicit finite occupation sampling law.
`core/18_isotropic_rigidity.tex` contains the centered-displacement extension,
isotropic perimeter identity and complete origin-free ambiguity theorem.
All other core files are immutable copies of the v37 active tree.

The manuscript continues to lead with exact inverse and rigidity statements,
then treats stationary boundary minimax reconstruction and retains the
localized, numerical precision, period locking and calibration arguments.
The response and audits are separate from the journal narrative.

For the next referee, read the controlling v36 report and the new response,
then audit the finite-stencil boundary argument and the isotropic
normalization. The sharp Hellinger and minimax arguments remain active and
require independent mathematical assessment; copying them does not certify
them. Distinguish the pointwise finite occupation theorem from the whole-field
period statement and from finite boundary reconstruction under a patch margin.

The exact-source workflow writes `verification/current/main.pdf`,
`receipt.json`, build logs, finite diagnostic output, a source archive,
`source-sha256.json`, and `artifact-binding.json`. The receipt records the
actual triggering commit and outcome. Do not transfer a passing receipt from
an earlier SHA or infer journal acceptance from workflow success.
