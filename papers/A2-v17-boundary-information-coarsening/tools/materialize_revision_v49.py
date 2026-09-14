#!/usr/bin/env python3
"""Materialize A2 v49 from the exact reviewed v48 active source.

All old inputs remain active. Reordering moves repeated expositions to the
compiled appendix; five edited originals are archived and checked bytewise.
No source is inferred from a branch name or a build-preparation commit.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P = Path(__file__).resolve().parents[1]
ARCHIVE = P/'history/v48-review-baseline'
ASSETS = P/'tools/revision_v49'
SOURCE_V48 = 'fe21046e47a89ec3b3df8493f4d885b087e3ad7f'
REVIEW_V48 = 'a512f70ca77d711bd6c9ee61988f1e8dd4dba790'
CHANGES = ('main.tex', 'article/00_structural_introduction_v48.tex',
           'article/01_introduction_v41.tex',
           'article/23m_differential_rigidity_v48.tex', 'v5/references_v43.tex')
NEW_INPUTS = ('article/23n_finite_symmetry_v49.tex',)
CATALOGUE = ('article/01_introduction_v41',
 'article/01f_generic_rigidity_overview_v45',
 'article/01g_quantized_reconstruction_overview_v46',
 'article/01h_calibration_overview_v47',
 'article/01e_realization_overview_v44', 'article/01d_proof_architecture_v41')
LOCAL = ('article/01c_geometric_setup_v43', 'article/02_finite_results',
 'v3/10_geometry_action', 'v3/20_integration', 'v4/10_boundary_layers',
 'v5/15_differentiated_operators', 'article/15_operator_comparison',
 'article/16_hyperbolic_coordinates', 'article/16c_strict_margin',
 'article/20_boundary_compatibility', 'article/23_two_contact_rigidity',
 'article/23a_signed_endpoint_rigidity_v27',
 'article/23f_single_offset_law_inverse_v42',
 'article/23f1_equivariant_density_extension_v29',
 'article/23g_density_support_distinction_v27',
 'article/23c_analytic_continuation_v23',
 'article/23b_intrinsic_multichannel_rigidity_v28',
 'article/23b1_signature_rigid_rerooting_v40',
 'article/23h_global_orientation_quotient_v29',
 'article/23d_rank_two_lattice_recovery_v43',
 'article/23e_signature_stability_v25',
 'article/23i_nonsymmetric_periodic_realization_v44',
 'article/23j_generic_finite_channel_rigidity_v45',
 'article/23n_finite_symmetry_v49', 'article/23m_differential_rigidity_v48')
STATISTICS = ('v6/10_experiment_transfer', 'article/17_adaptive_experiments_v31',
 'article/18_boundary_information_v18', 'article/18a_vector_boundary_information_v26',
 'article/18a2_likelihood_tilting_moments_v34',
 'article/18b0_anchored_realization_v43', 'article/18b_raw_physical_multirate_v22',
 'article/18a1_compact_experiments_v32', 'article/18c_full_endpoint_time_information_v26',
 'article/18c1_endpoint_time_deficiency_v43',
 'article/18f_domination_and_position_comparison_v27',
 'article/18d_count_endpoint_multirate_v32', 'article/18d1_intrinsic_count_geometry_v43',
 'article/18e_compatible_rates_v23', 'article/19_endpoint_critical',
 'article/21_abel_stability', 'article/22_deautoconvolution',
 'article/28_regularized_observation')
PHYSICAL = ('article/23k_quantized_law_stability_v46',
 'article/23l_calibrated_histograms_v47', 'article/24_physical_image',
 'article/29_two_flight_benchmark', 'article/29a_signed_one_flight_benchmark_v25',
 'article/29b_direct_position_benchmark_v26', 'article/25_analytic_global_bridge_v23',
 'article/25a_common_observables_v25', 'article/25b_augmented_global_reconstruction_v26',
 'article/25c_analytic_variation_bundles_v25')


def once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1, 'Unexpected edit anchor: '+old)
    return text.replace(old,new,1)


def inputs(names: tuple[str,...]) -> str:
    return ''.join('\\input{'+x+'}\n' for x in names)


def revised(name: str, text: str) -> str:
    if name==CHANGES[1]:
        return (ASSETS/'introduction.tex').read_text()
    if name==CHANGES[2]:
        text=once(text, r'\section{Local mechanisms and observation-specific consequences}',
                  r'\section{Collected theorem statements and comparisons}')
        start=text.index(r'\subsection{Organization}')
        return text[:start]+r'''\subsection{Organization of the proof and the collected statements}

The statements and extended comparisons in this appendix retain the
alternative local, signature-rigid and observation-specific formulations.
The primary proof of Theorem~\ref{thm:v48-main} runs through Part I:
relative boundary laws, signed contact inversion, analytic image recovery,
finite incidence matching and the derivative kernel.  Part II treats the
local information experiments.  Part III contains finite-resolution
inversion, calibrated acquisition and complete physical reconstruction,
including the short-flight and direct-position comparisons.
The following appendices retain the complete auxiliary derivations.
'''
    if name==CHANGES[3]:
        text=text.replace(r'\mathscr A_N',r'\mathscr C_N')
        old='''The differentiated relative construction of
Theorem~\\ref{thm:v8-main-relative} supplies the amplitude derivatives.
Thus the half-line actions $S_t$ and amplitudes $B_t$ depend $C^1$ in
any fixed finite smooth norm on the collars used here.'''
        text=once(text,old,(ASSETS/'amplitude.tex').read_text().rstrip())
        text=once(text,'''stationary to first order.
\\end{lemma}''', '''stationary to first order.
For noncircular obstacles, the same conclusions hold on a local alignment
branch through the actual base realization, without asserting globally
single-valued registration.
\\end{lemma}''')
        old='''This proves the
last assertion without assuming a differentiable inverse to analytic
continuation.
\\end{proof}'''
        addition=(ASSETS/'local_registration.tex').read_text().rstrip()
        text=once(text,old,'''This proves the
last assertion without assuming a differentiable inverse to analytic
continuation.

'''+addition+'\n\\end{proof}')
        return text
    if name==CHANGES[4]:
        entry=r'''
\bibitem{A2ReviewV48}
Independent AI-assisted referee-style memorandum,
\emph{A2 revision 48}, September 14, 2026, Section 4,
repository \texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
review commit
\href{https://github.com/TrillionniumFoundation/theta-theory/commit/a512f70ca77d711bd6c9ee61988f1e8dd4dba790}{\texttt{a512f70c\allowbreak a77d711b\allowbreak d6c9ee61\allowbreak 988f1e8d\allowbreak d4dba790}}.
An author-requested memorandum, not a commissioned journal report.

'''
        return once(text,r'\end{thebibliography}',entry+r'\end{thebibliography}')
    require(name=='main.tex','Unknown amended input')
    text=text.replace('A2 revision 48','A2 revision 49')
    text=once(text,'''lattice up to a common proper Euclidean motion.  The same observation map
is infinitesimally rigid on common-strip analytic-support families.''',
      '''lattice up to a common proper Euclidean motion.  For noncircular obstacles
with finite symmetries we enumerate the finite reconstruction branches.
On this larger class the same observation map is infinitesimally rigid
on common-strip analytic-support families.''')
    start=text.index(r'\part{Relative laws, signed inversion, and intrinsic rigidity}')
    end=text.index(r'\subsection*{Acknowledgments}')
    body=(r'\part{Relative laws, signed inversion, and intrinsic rigidity}'+'\n'+inputs(LOCAL)
       +'\n'+r'\part{Boundary information and physical local experiments}'+'\n'
       +r'\section{Observation spaces and coarsenings}'+'\n'
       +r'\label{sec:v49-record-spaces}'+'\n'
       +inputs(('article/01a_protocol_scope_v25','article/01b_observation_hierarchy_v29'))
       +inputs(STATISTICS)+'\n'
       +r'\part{Finite-resolution inversion and global physical reconstruction}'+'\n'
       +inputs(PHYSICAL)+'\n')
    text=text[:start]+body+text[end:]
    text=once(text,'''provenance are archived separately from the mathematical article.''',
       '''provenance are archived separately from the mathematical article.
The distinction between finite rotations and infinitesimal symmetry, and
the circular-lattice comparison in Section~\\ref{sec:v49-finite-symmetry},
were suggested in the author-requested memorandum~\\cite{A2ReviewV48}.
The finite enumeration of compatible reconstruction branches is developed
here from that distinction and the intrinsic cochain inverse.''')
    return once(text,r'\part{Complete auxiliary proofs and applications}',
       r'\part{Collected statements, comparisons and complete auxiliary proofs}'+'\n'+inputs(CATALOGUE))


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(),'Missing readable mathematical module: '+name)
    for name in ('introduction.tex','amplitude.tex','local_registration.tex'):
        require((ASSETS/name).is_file(),'Missing editorial asset: '+name)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest=ARCHIVE/'active-source-manifest.json'
    if not manifest.exists():
        original=P.parents[1]/'deliveries/a2-v48'/SOURCE_V48/'active-source-manifest.json'
        require(original.is_file(),'Missing native v48 baseline manifest')
        manifest.write_bytes(original.read_bytes())
    source=json.loads(manifest.read_text())
    old={name:info for group in source.values() for name,info in group.items()}
    require(len(old)==105,'Unexpected baseline input count')
    for name,info in old.items():
        archived=ARCHIVE/name
        path=archived if name in CHANGES and archived.exists() else P/name
        data=path.read_bytes()
        require(hashlib.sha256(data).hexdigest()==info['sha256'],'Baseline mismatch: '+name)
        if name in CHANGES:
            if not archived.exists():
                archived.parent.mkdir(parents=True,exist_ok=True)
                archived.write_bytes(data)
            expected=revised(name,data.decode())
            require((P/name).read_text() in (data.decode(),expected),'Unrecognized edit: '+name)
            (P/name).write_text(expected)
    return {'review_head':REVIEW_V48,'reviewed_mathematical_source':SOURCE_V48,
            'baseline_inputs':len(old),'exact_amended_originals':list(CHANGES),
            'new_inputs':list(NEW_INPUTS),'mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),sort_keys=True,indent=2))
