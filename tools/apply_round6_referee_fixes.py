#!/usr/bin/env python3
"""Materialize the round-six referee reconstruction into all eleven papers."""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
SRC = ROOT / "revision" / "round6-referee-final"

DATA = {
    "A1-exact-benchmarks": {
        "code": "A1",
        "source": "A1_FULL_PORT_SUSPENSION_RESPONSE.tex",
        "platform": "A1-HAM-PORT-R6",
        "abstract": r"""We construct a graph-completed four-port symplectic self-return map and
an autonomous Hamiltonian suspension whose work layer covers every regular
incoming port point.  The integrated mechanical work is therefore exactly the
branch-current cocycle on the full Liouville path law.  A finite trace-jet
Banach scale gives an all-order physical moving-seam response calculus and its
common-root finite-difference realization.  Identification of a valuation
coefficient with the mechanical conjugate field is stated precisely as a
canonical-cocycle compatibility theorem.""",
        "repairs": [
            "full-port work before recutting",
            "one graph-completed symplectic return section",
            "autonomous Hamiltonian port cobordism",
            "all-order physical trace-jet response",
        ],
    },
    "A2-sinai-homological-pressure": {
        "code": "A2",
        "source": "A2_AMBIENT_TRACE_DOLGOPYAT_LLT.tex",
        "platform": "TL2-AMBIENT-ROOF-R6",
        "abstract": r"""For a compact finite-horizon Sinai radius family we build one fixed
ambient bulk-and-trace distribution field across all singularity births,
deaths, tangencies, and intersections.  Trace jets through order two close
parameter differentiation and yield a uniform complex vector--roof spectral
bundle.  Explicit return, non-concentration, and paired cancellation operators
prove a radius-uniform Dolgopyat estimate.  Fourier inversion gives a master
vector-lattice/roof-nonlattice local-limit theorem with absolute errors and
separate local, central, and saturated roof-window regimes.""",
        "repairs": [
            "fixed ambient trace field instead of zero/nonzero fibre isomorphisms",
            "second-order trace jets",
            "complete Dolgopyat return/cancellation operators",
            "relative LLT only on valid window scales",
        ],
    },
    "A3-full-empirical-path-ldp": {
        "code": "A3",
        "source": "A3_DEFECT_COMPACTIFICATION_LDP.tex",
        "platform": "TL3-DEFECT-PATH-R6",
        "abstract": r"""We prove collision- and physical-time empirical-path large-deviation
principles on a recession-completed state.  A positive collision-clock fraction
carried by return levels tending to infinity is retained by a finite defect
measure on compact normalized excursion profiles.  Recurrent phases are
approximated by admissible finite-state Markov laws using only genuine graph
edges and connector words, with quantitative entropy and free-energy
convergence.  The resulting recurrent--defect variational principle, survivor
spectral theorem, singularity shield, and terminal clock surgery give full
upper and lower bounds.""",
        "repairs": [
            "explicit recession defect coordinate",
            "admissible entropy-preserving Markov recovery",
            "survivor strong/weak spectral spaces",
            "full collision and physical clock lower bounds",
        ],
    },
    "A4-history-memory-universal-pressure": {
        "code": "A4",
        "source": "A4_RAY_TRANSMISSION_ZERO_ROUGH_KERNEL.tex",
        "platform": "TL3-HISTORY-MEMORY-R6",
        "abstract": r"""Prepared Sinai paths admit a common-exceptional-set Ray right process
and, on exposed phases, a concrete weighted-history Feller realization.  A
bounded positive history eigenfunction produces the genuine Doob Markov
semigroup.  The exact finite-dimensional Volterra equation has forcing
$PLQB$ at time zero; no false orthogonality is asserted.  Every resonance and
transmission zero in a left half-strip is promoted to a finite auxiliary mode,
leaving an exponentially decaying residual memory.  The enhanced and
conditional invariance principles retain the deterministic rough-area
anomaly and yield compact-history kernel homogenization.""",
        "repairs": [
            "common-exceptional-set Ray process",
            "genuine history eigenfunction Doob transform",
            "transmission-zero auxiliary realization",
            "area-corrected conditional rough kernels",
        ],
    },
    "B1-microcanonical-preparation": {
        "code": "B1",
        "source": "B1_COMPOUND_POISSON_FINITE_SADDLE.tex",
        "platform": "HSBG-SHELL-R6",
        "abstract": r"""We prove source-dependent microcanonical preparation at the exact
finite-volume saddle.  The grand-canonical logarithm is decomposed into its
true compound-Poisson singleton exponent and a connected remainder; smooth
convolution powers arise only after exponentiating the singleton term.  Under
explicit lattice-span, rank, and nonlattice hypotheses this yields a uniform
mixed characteristic-function theorem and exact-number shrinking-shell local
limit.  The conditioned pressure, initial rate, and fluctuation covariance are
the source-dependent constrained infimum and its Schur complement.""",
        "repairs": [
            "exact compound-Poisson singleton decomposition",
            "uniform finite mean-image theorem",
            "exact finite-volume saddle",
            "mixed lattice/nonlattice shell coefficient",
        ],
    },
    "B2-collision-clusters-dynamic-ldp": {
        "code": "B2",
        "source": "B2_TRACE_CLASS_GRAMIAN_LDP.tex",
        "platform": "HSBG-ACTUAL-CONTACT-R6",
        "abstract": r"""Every actual deterministic hard-sphere contact is marked on a
trace-regular correlation hierarchy.  Incoming flux traces, rather than
interior mass alone, control future contact exponential moments and exclude
boundary-layer counterexamples.  A genealogical controllability Gramian
containing root translations, root velocities, and all creation variables
gives a first-surplus codimension-two tube estimate.  The true reflected future
is retained and propagated by the trace semigroup.  Fixed-horizon source
sewing, conservative action-dense regularization, and normalized deterministic
tilts establish grand-canonical and microcanonical joint density--contact
LDPs.""",
        "repairs": [
            "incoming-flux trace hierarchy",
            "root-inclusive genealogical Gramian",
            "future-preserving contact ledger",
            "fixed-horizon pressure and full GC/MC LDP",
        ],
    },
    "B3-hamilton-boltzmann-cotangents": {
        "code": "B3",
        "source": "B3_TWO_DOMAIN_GAUGE_CUMULANT_GAUSSIAN.tex",
        "platform": "HSBG-GAUGE-GAUSSIAN-R6",
        "abstract": r"""The density--actual-contact action is placed in one weighted strict
Radon duality, with separate local analytic and global convex source domains.
The complete cotangent is the Hausdorff quotient by
$(r,-\Delta r)$, and arbitrary bounded-source exhaustion recovers the full
entropy action and detects singular current.  Local covariance is strictly
positive exactly modulo the balance gauge, endpoint coboundaries, and prepared
constraints.  Exact finite-volume centring and time-localized connected
cumulants yield a process-level joint Gaussian limit with all density--contact
cross covariances and without an assumed point-process compensator.""",
        "repairs": [
            "separate local analytic and global convex source domains",
            "closed weighted gauge and Radon dual",
            "quadratic-action covariance cohomology",
            "exact-centred cumulant process CLT",
        ],
    },
    "B4-nonlinear-kinetic-semigroups": {
        "code": "B4",
        "source": "B4_WEAK_ENERGY_FULL_BBGKY_SEMIGROUP.tex",
        "platform": "HSBG-KINETIC-SEMIGROUP-R6",
        "abstract": r"""The exact finite object is the complete probability law on
hard-sphere microstates, with a genuine polynomial algebra of factorial
correlation coordinates.  A normally summable full triangular BBGKY Duhamel
corrector gives the Hamilton--Boltzmann logarithmic generator on bounded
collision-increment cylinders.  The kinetic state uses ordinary weak
convergence with energy as a lower-semicontinuous containment function, so
energy sublevels are compact without requiring second-moment convergence.
Action compactness, bounded-core comparison, the B2 Laplace principle, and the
perturbed-test theorem identify the unique nonlinear kinetic semigroup.""",
        "repairs": [
            "genuine law-coordinate polynomial algebra",
            "full triangular BBGKY corrector",
            "weak energy topology with compact sublevels",
            "bounded-increment comparison and microscopic convergence",
        ],
    },
    "C1-information-risk-sensitive-saddles": {
        "code": "C1",
        "source": "C1_OBSERVED_POSTERIOR_CHERNOFF_LAN.tex",
        "platform": "HSBG-POSTERIOR-CONTROL-R6",
        "abstract": r"""The exact information state is the resolved history together with the
controlled posterior law of the complete microstate.  Each transition consists
of normalized controlled prediction followed by disintegration with respect
to the newly observed block, yielding measurable strategy laws and an exact
posterior-state DPP.  Conditional source estimates prove the adaptive kinetic
Isaacs limit.  Typical posterior density odds have a directed relative-entropy
rate, whereas expected posterior error has the Chernoff testing rate.  The
canonical experiment is centred at the exact finite-volume mean and satisfies
LAN and a finite-dimensional Bernstein--von Mises theorem.""",
        "repairs": [
            "observation-aware Bayes transition",
            "strategy-dependent posterior DPP",
            "KL odds versus Chernoff expected error",
            "exact finite-centred LAN and BvM",
        ],
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "code": "C2",
        "source": "C2_COERCIVE_HISTORY_DOOB_MEMORY.tex",
        "platform": "TYPED-HISTORY-REPRESENTATION-R6",
        "abstract": r"""Physical platforms form a labelled coproduct and their source spaces a
locally convex direct sum.  Explicit rate--moment coercivity makes weighted
strict pressures finite and their phase sets compact.  Every mechanical
observable is a continuous or exponentially approximable typed contraction.
Finite likelihoods are exact conditional-expectation martingales on complete
history filtrations and converge through the A4 conditional-kernel theorem to
diffusion optional projections, Girsanov densities, and BSDEs.  Linearized
pressure and compressed memory are paired in one declared Doob Hilbert space
with one orthogonal projection.""",
        "repairs": [
            "rate-coercive strict source domain",
            "typed platform contractions",
            "complete-history optional-projection convergence",
            "one-Hilbert Doob pressure-memory identity",
        ],
    },
    "D1-deterministic-theta-contractions": {
        "code": "D1",
        "source": "D1_PROJECTIVE_STEEP_COMMUTATION.tex",
        "platform": "PROJECTIVE-COMMUTATION-R6",
        "abstract": r"""We derive full path-space LDPs from compatible finite-dimensional
pressures which are finite, differentiable, and steep on their support
quotients, followed by Dawson--Gärtner passage and exponential tightness.  The
resulting global rate uses only the proved cylinder source algebra and requires
no rate-dense exposed-point hypothesis.  Typed contraction, exact
source-dependent conditioning, their closed joint-infimum interchange, and
additive dynamic programming commute with pressure derivatives and Gaussian
tangents.  Every local canonical likelihood is exactly centred at the
finite-volume mean and is a mean-one Radon--Nikodym density.""",
        "repairs": [
            "finite-dimensional steep-pressure lower bounds",
            "projective full LDP without P3",
            "closed primal conditioning/contraction interchange",
            "exact finite-centred likelihoods and dynamic triangle",
        ],
    },
}

CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
INPUT_RE = re.compile(r"\\input\{ROUND\d+_POSITIVE_CLOSURE\.tex\}")
CONTROL_MARKER_RE = re.compile(
    r"\\noindent\\textbf\{Controlling revision:\}\s*"
    r"\\texttt\{[^}]+\}\."
)
DATE_RE = re.compile(r"\\date\{[^}]*\}")
ABSTRACT_RE = re.compile(
    r"\\begin\{abstract\}.*?\\end\{abstract\}", re.DOTALL
)

for paper, meta in DATA.items():
    source = SRC / meta["source"]
    if not source.is_file():
        raise SystemExit(f"missing round-six source: {source}")
    text = source.read_text(encoding="utf-8")
    match = CONTROL_RE.search(text)
    if match:
        raise SystemExit(
            f"{source}: ASCII control byte {ord(match.group(0))} at {match.start()}"
        )
    target = PAPERS / paper / "ROUND6_POSITIVE_CLOSURE.tex"
    target.write_text(
        "% ROUND6-REFEREE-POSITIVE-CLOSURE\n" + text,
        encoding="utf-8",
    )

    main = PAPERS / paper / "main.tex"
    old = main.read_text(encoding="utf-8")
    old = DATE_RE.sub(r"\\date{August 31, 2026}", old, count=1)
    old = ABSTRACT_RE.sub(
        "\\begin{abstract}\n"
        + meta["abstract"].strip()
        + "\n\\end{abstract}",
        old,
        count=1,
    )
    old = CONTROL_MARKER_RE.sub(
        r"\\noindent\\textbf{Controlling revision:} "
        r"\\texttt{ROUND6-REFEREE-POSITIVE-CLOSURE}.",
        old,
        count=1,
    )
    if INPUT_RE.search(old):
        old = INPUT_RE.sub(r"\\input{ROUND6_POSITIVE_CLOSURE.tex}", old, count=1)
    elif r"\input{ROUND6_POSITIVE_CLOSURE.tex}" not in old:
        raise SystemExit(f"{main}: controlling input not found")
    old = old.replace("round-three dependency ledger", "round-six dependency ledger")
    old = old.replace("round-five dependency ledger", "round-six dependency ledger")
    main.write_text(old, encoding="utf-8")

    report = PAPERS / paper / "REFEREE_REPORT_ROUND5_GPT56_PRO.md"
    if not report.is_file():
        raise SystemExit(f"missing latest report: {report}")
    response = PAPERS / paper / "AUTHOR_RESPONSE_ROUND6.md"
    lines = [
        f"# {meta['code']} author response to the round-five independent report",
        "",
        "The report was checked against the active controlling bytes and the",
        "unmaterialized round-five candidate.  Both source-control and mathematical",
        "objections were treated as load-bearing.",
        "",
        "## Positive reconstruction",
        "",
    ]
    lines.extend(f"- {item}." for item in meta["repairs"])
    lines += [
        "",
        "The paper now loads `ROUND6_POSITIVE_CLOSURE.tex`, which is byte-copied",
        f"from `revision/round6-referee-final/{meta['source']}` by the fail-closed",
        "materializer.  No headline theorem is replaced by a no-go statement or",
        "removed from the series.",
        "",
    ]
    response.write_text("\n".join(lines), encoding="utf-8")

manifest_lines = [
    "schema: theta-theory-round6-referee-v1",
    "report_branch: review/round5-gpt56-pro-harsh-11paper-2026-08-31",
    "reviewed_head: 557c88ef447ab8c693b11e1c072efe97b4452556",
    "revision_branch: revision/round6-referee-positive-closure-11paper-2026-08-31",
    "papers: 11",
    "policy:",
    "  positive_closure: true",
    "  downgrade: false",
    "  nogo_substitution: false",
    "  controlling_source_identity: required",
    "paper_sources:",
]
for paper, meta in DATA.items():
    manifest_lines += [
        f"  - paper: {paper}",
        f"    source: revision/round6-referee-final/{meta['source']}",
        f"    controlling_module: papers/{paper}/ROUND6_POSITIVE_CLOSURE.tex",
        f"    platform: {meta['platform']}",
    ]
(ROOT / "ROUND6_REVISION_MANIFEST.yaml").write_text(
    "\n".join(manifest_lines) + "\n", encoding="utf-8"
)

print(f"ROUND6_MATERIALIZATION_PASS papers={len(DATA)}")
