#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
MAPPING={'A1-exact-benchmarks': {'source': 'A1_PHYSICAL_IMPACT_MASS_FLAG_COMPLEX.tex', 'platform': 'A1-HAM-IMPACT-FLAG-v7', 'abstract': 'We separate the physical generalized-baker impact system from its coupled symbolic natural extension.  The physical branches are realized by exact autonomous Hamiltonian channels with a canonical work pair, while the symbolic map is the correctly coupled update \\((x,y)\\mapsto(\\sigma x,x_0y)\\).  A geometric mass norm on compatible bulk, face, corner, and higher flag currents is nondegenerate under arbitrary refinement and supports every finite material-response order.  The response theorem explicitly includes the transported-observable convention and reduces to zero for a genuinely fixed physical observable.', 'code': 'A1'}, 'A2-sinai-homological-pressure': {'source': 'A2_FOUR_DIMENSIONAL_INTEGRABLE_LLT.tex', 'platform': 'TL2-HOM-4D-LLT-v7', 'abstract': 'For the compact finite-horizon triangular Sinai family we construct a parent-fold anisotropic transfer bundle, prove full lattice rank and returned temporal nonintegrability, and give an exhaustive integrable Fourier decomposition.  The local variable is the four-vector consisting of two homology coordinates, return count, and physical roof, so the joint density has the correct \\(n^{-2}\\) prefactor.  Small, covariance-annulus, compact, Dolgopyat, and very-high-frequency ranges cover the entire Fourier domain, with an integrable \\(e^{-cn}(1+|b|)^{-3}\\) tail.  The resulting local limit and conditioning theorems use one consistent saddle convention.', 'code': 'A2'}, 'A3-full-empirical-path-ldp': {'source': 'A3_GRAPH_CONTROLLED_STOPPED_LDP.tex', 'platform': 'TL3-GRAPH-RENEWAL-LDP-v7', 'abstract': 'We prove collision- and physical-clock empirical-path large deviations directly from a graph-completed controlled Markov-renewal process.  The state retains complete excursion marks, singularity exposure, all mesoscopic and macroscopic clock mass, and the pointed terminal prefix.  A stopped entropy variational formula charges the final excursion exactly once and yields one good rate at the deterministic clock speed; recession coordinates are projective contractions of that rate rather than an independently normalized action.  A separate controlled time-change proof gives the physical-clock rate and continuity of path concatenation at graph-completed singular states.', 'code': 'A3'}, 'A4-history-memory-universal-pressure': {'source': 'A4_WEIGHTED_COUPLING_SCHUR_MEMORY.tex', 'platform': 'TL3-HISTORY-SCHUR-MEMORY-v7', 'abstract': 'The genuine past kernel of the prepared Sinai process contracts in a weighted Wasserstein metric; remote deterministic tails are discounted rather than falsely minorized in total variation.  An exponential multiplier algebra makes the Feynman--Kac and Doob operators well defined, the Poisson martingale is exactly centered, and a uniform quenched enhanced invariance principle follows from coupling and bracket control.  The continuous-time resolvent is derived from entrance, excursion, and residual renewal operators.  Memory descriptors are extracted only from the final Schur complement after pole--zero cancellation, and integrable vertical bounds produce a canonical instantaneous, descriptor, and exponentially decaying residual decomposition.', 'code': 'A4'}, 'B1-microcanonical-preparation': {'source': 'B1_EXACT_NUMBER_POLYMER_SHELL.tex', 'platform': 'HSBG-EXACT-N-SHELL-v7', 'abstract': 'We extract the exact particle-number coefficient before Fourier inversion of continuous constraints, thereby removing the grand-canonical empty-sector atom.  A coefficient-level trajectory-polymer theorem proves that either linearly many bounded regular components are present or the coefficient weight is exponentially small.  This yields a compact-annulus gap and an integrable high-frequency bound whose power grows linearly with particle number, without any impossible spatial block independence.  Exact activity and continuous saddles, a quantitatively defined regular shell class, the mixed local coefficient, and the source-dependent microcanonical pressure and covariance Schur complement follow.', 'code': 'B1'}, 'B2-collision-clusters-dynamic-ldp': {'source': 'B2_TRUE_JACOBI_FIXED_HORIZON_LDP.tex', 'platform': 'HSBG-TRACE-JACOBI-LDP-v7', 'abstract': 'We construct the compatible hard-sphere Green trace graph using the normal-flux measure exactly once and analyze recollisions on the full fixed horizon.  For every fixed cyclic genealogy the actual linearized collision law has an explicitly witnessed transverse analytic minor; genealogy-dependent sublevel exponents are then summed by dominated convergence under one factorial trajectory majorant.  The limiting marked Hamiltonian is derived directly from the global tree series.  Smooth positive balanced pairs are exposed by actual contact sources, a continuous kinetic Hodge repair supplies rate-dense recovery, and full grand-canonical and source-conditioned microcanonical density--contact LDPs follow.', 'code': 'B2'}, 'B3-hamilton-boltzmann-cotangents': {'source': 'B3_JOINT_COLLISION_GAUSSIAN_TIGHTNESS.tex', 'platform': 'HSBG-JOINT-GAUSSIAN-v7', 'abstract': 'The density--contact covariance is constructed first from exact finite-volume cumulants and is driven by an isonormal Gaussian measure on collision space.  Its coefficient is the complete \\(\\Delta p+\\psi\\), so pure contact and density--contact brackets are present.  A perturbative nonautonomous energy theorem types the regular biased chart, while process tightness uses unconditional deterministic-interval cumulants with the required microscopic diagonal term and a multiscale grid, not an impossible full-state stopping-time estimate.  The balanced gauge includes endpoints and transport, and the second epi-derivative is the closed Cameron--Martin form on \\(\\operatorname{Ran}\\Sigma^{1/2}\\).', 'code': 'B3'}, 'B4-nonlinear-kinetic-semigroups': {'source': 'B4_ENSEMBLE_BOUNDARY_NISIO_SEMIGROUP.tex', 'platform': 'HSBG-ENSEMBLE-NISIO-v7', 'abstract': 'We distinguish the deterministic hard-sphere flow, its Koopman derivation, law pushforward, ensemble log-Laplace functional, and limiting kinetic value.  The exponential collision Hamiltonian is derived from the ensemble Green boundary jump, not from exponential conjugation of an interior derivation.  An exact law--hierarchy intertwiner and a \\(1/j!\\)-weighted full triangular corrector give generator convergence.  The dynamic entropy action constructs a Nisio semigroup and discounted nonlinear resolvent; primal resolvent comparison avoids uncontrolled doubled jets.  One-time microcanonical preparation and the full density--contact Gaussian risk-sensitive tangent are then obtained from B1--B3.', 'code': 'B4'}, 'C1-information-risk-sensitive-saddles': {'source': 'C1_POSITIVE_BLOWUP_GROWING_BELIEF.tex', 'platform': 'HSBG-BELIEF-BLOWUP-v7', 'abstract': 'Observations are represented by positive joint kernels and Rokhlin disintegrations; geometric currents are used only to calculate coarea densities.  The exact information state is the full unnormalized belief on an oriented blow-up of the positive cone, where distinct zero-evidence directions are retained rather than simultaneously collapsed and used.  A regular positive posterior kernel is Feller on this compact state.  An inserted exact-number coefficient controls additive path/contact observations.  Growing finite nets of bounded-Lipschitz tests, rather than a fixed list of moments, approximate the full belief game with an explicit Bellman error, and a fully specified regular parametric class satisfies a controlled Bernstein--von Mises theorem.', 'code': 'C1'}, 'C2-cotangent-rigidity-tangent-representations': {'source': 'C2_TWO_TOPOLOGY_COMMON_FORM_RESPONSE.tex', 'platform': 'TYPED-TWO-TOPOLOGY-FORM-v7', 'abstract': 'We separate the weighted strict topology, whose dual is the vector space of signed Radon measures, from the stronger Hölder/graph topology, whose dual may contain distributions.  The invariant-integral nullspace excludes constants, and full-pressure rigidity is proved by platform-specific Sinai Livšic or finite-horizon balance-coboundary arguments.  A uniformly equivalent real coercive form norm yields one common type-(B) domain for generator and compressed-memory response.  Resolved projections are treated separately, source and state derivatives have distinct chain rules, and conditional-kernel convergence gives the optional-projection, Girsanov, and quadratic-BSDE representation.', 'code': 'C2'}, 'D1-deterministic-theta-contractions': {'source': 'D1_POSITIVE_PHASE_SHEAF_LOGSUM.tex', 'platform': 'POSITIVE-PHASE-SHEAF-v7', 'abstract': 'We construct a projectively consistent positive phase label on the original microscopic sample space from isolated rate components and an explicit boundary band.  Component rates are basin-interior lower-semicontinuous recovery costs, so boundary points are not assigned the unrestricted rate by fiat.  Positive component operators provide phase-local response charts.  Exact nonlinear aggregation is log-sum-exp at finite volume and a maximum with an active-phase subdifferential in the limit, never a linear mixture of log values.  Target-dependent shell costs, Gaussian mixtures, and labelled law-level commutation give a standalone positive phase-sheaf theorem without interpreting spectral projections as probabilities.', 'code': 'D1'}}

for name,meta in MAPPING.items():
    paper=ROOT/"papers"/name
    source=ROOT/"revision"/"round14-referee-final"/meta["source"]
    active=paper/"ROUND14_POSITIVE_CLOSURE.tex"
    main=paper/"main.tex"
    if not source.is_file() or not main.is_file():
        raise SystemExit(f"missing source or main: {name}")
    active.write_bytes(source.read_bytes())
    old=main.read_text(encoding="utf-8")
    marker=r"\begin{document}"
    if marker not in old:
        raise SystemExit(f"missing document marker: {main}")
    preamble=old.split(marker,1)[0].rstrip()
    body = (
        preamble+"\n"+marker+"\n"
        r"\raggedbottom"+"\n"
        r"\begin{abstract}"+"\n"
        +meta["abstract"].strip()+"\n"
        r"\end{abstract}"+"\n"
        r"\maketitle"+"\n"
        r"\noindent\textbf{Platform identifier:} \texttt{"+meta["platform"]+r"}. "+"\n"
        r"\noindent\textbf{Controlling revision:} \texttt{ROUND14-REFEREE-POSITIVE-CLOSURE}. "+"\n"
        r"\noindent\textbf{Registered proof source:} \texttt{"+meta["source"].replace("_",r"\_")+r"}. "+"\n"
        r"\tableofcontents"+"\n\n"
        r"\input{ROUND14_POSITIVE_CLOSURE.tex}"+"\n\n"
        r"\section*{Scope and verification status}"+"\n"
        "This manuscript states positive theorem closure in the declared model-specific "
        "regular regime. Cross-paper inputs follow the round-fourteen dependency ledger. "
        "Repository source, proof-structure, direct-counterexample, and build gates are "
        "internal reproducibility checks and do not replace independent external mathematical review.\n"
        r"\printbibliography"+"\n"
        r"\end{document}"+"\n"
    )
    main.write_text(body,encoding="utf-8")

manifest={
    "schema":"theta-theory-round14-materialization-v1",
    "review_branch":"review/round13-gpt56-pro-harsh-11paper-2026-09-01",
    "review_head":"7bdc2ef6fd248fd18fa347e02dce3c40883bb173",
    "papers":[
        {
            "folder":f"papers/{name}",
            "registered_source":f"revision/round14-referee-final/{meta['source']}",
            "active_module":f"papers/{name}/ROUND14_POSITIVE_CLOSURE.tex",
            "author_response":f"papers/{name}/AUTHOR_RESPONSE_ROUND14.md",
            "platform":meta["platform"],
        }
        for name,meta in MAPPING.items()
    ],
}
(ROOT/"ROUND14_MATERIALIZATION_MANIFEST.json").write_text(
    json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
)
print(f"ROUND14_MATERIALIZED {len(MAPPING)}/11")
