#!/usr/bin/env python3
"""Independent replay of the Round306B1AF3 construction-source frontier.

This file never imports or executes an upstream producer or the primary AF3
replay.  Its production path is a read-only, held-descriptor verification of
an embedded catalog.  Static AST support below exists to independently audit
how that catalog's direct pin edges were derived; it admits no analytic or
formal-full-support credit.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable, Mapping, Sequence


DELIVERABLES = Path(__file__).resolve().parent
SCHEMA = (
    "cm2.round306b1af3.source-g-full-support-construction-source-"
    "authority-frontier.replay-result.v1"
)
EXPECTED_INVENTORY_SHA256 = (
    "40d971a646e59ffbc6854913c1c9dbc831253ba80d00451f79524fd371c8097a"
)
EXPECTED_ROOT_COUNT = 36
EXPECTED_CLOSURE_FILE_COUNT = 143
EXPECTED_CLOSURE_TOTAL_BYTES = 3_201_364_049
EXPECTED_EDGE_COUNT = 261
EXPECTED_EDGES_SHA256 = (
    "916a2d8b587e1ed06202bee903779bccdb8f7555c4de02f1a176fa91fd55a16b"
)

ROOT_FILENAMES = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py",
    "cm2_round179_source_g_residual_tube_arrangement.py",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py",
    "cm2_round204_source_g_wall_return_signature_local_replacement.py",
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py",
    "cm2_round211_source_g_outgoing_half_open_owner_materialization.py",
    "cm2_round220_source_g_round179_resolved_child_boundary_atlas.py",
    "cm2_round234_source_g_wall_endpoint_order_depth6_materialization.py",
    "cm2_round235_source_g_single_endpoint_graph_word_key_partition.py",
    "cm2_round236_source_g_wall_residual_closure_and_root_key_partition.py",
    "cm2_round242_source_g_outgoing_graph_existence_stratum_materialization.py",
    "cm2_round245_source_g_retained_graph_mixed_sheet_quotient.py",
    "cm2_round246_source_g_whole_signature_retained_quotient.py",
    "cm2_round247_source_g_crossing_and_source_seam_retained_quotient.py",
    "cm2_round248_source_g_wall_finite_key_retained_quotient.py",
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure.py",
    "cm2_round266_source_g_expanded_curved_face_closure.py",
    "cm2_round269_source_g_closed_collar_direct_signature_materialization.py",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization.py",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization.py",
    "cm2_round272_source_g_boundary_dual_factor_wall_closure.py",
    "cm2_round275_source_g_complete_reverse_rechart_materialization.py",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze.py",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe.py",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit.py",
    "cm2_round289_source_g_outgoing_seam_tail_child_materialization.py",
    "cm2_round290_source_g_isolated_atom_inner_support_closure.py",
    "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze.py",
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe.py",
    "cm2_round293_source_g_r289_r291_witness_binding_canonical_closure.py",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion.py",
    "cm2_round294b_source_g_registry_builder_admission_closure.py",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py",
    "cm2_round306b0_source_g_r306a_universe_support_source_freeze.py",
    "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py",
    "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py",
)

# Independently derived exact-PINS closure.  The compact tuples are merely a
# source representation; CLOSURE_RECORDS below is the frozen canonical domain.
FROZEN_CATALOG: tuple[tuple[str, int, str, bool], ...] = (
    ('cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json', 2795, '1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b', False),
    ('cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json', 7853, 'f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987', False),
    ('cm2-gate3-first-hit-atlas-manifest-2026-07-15.json', 7112, '0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4', False),
    ('cm2-gate3-ge-interval-atlas-manifest-2026-07-15.json', 3926, 'd502d0b1c8ef6dba349fa5b7211da4c0a3fcff78bf92a46457cb4f4b64f760f5', False),
    ('cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json', 10733, '47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866', False),
    ('cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json', 7097635, '64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0', False),
    ('cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json', 8995, '57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f', False),
    ('cm2-round161-dyadic-sheared-recentering-to-2500000000000000h-2026-07-25.json', 35673, '317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd', False),
    ('cm2-round161-dyadic-sheared-recentering-to-2500000000000000h-verification-2026-07-25.json', 5180, '01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db', False),
    ('cm2-round171-compact-gate3-source-g-coordinate-bridge-manifest-2026-07-26.sha256', 895, 'b86a5faa33f503a2de6139f7765fda4e54e027954373ecdf8b8d587ba179417c', False),
    ('cm2-round173-source-g-exact-return-signature-transport-manifest-2026-07-26.sha256', 901, 'ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275', False),
    ('cm2_gate3_candidate_first_hit_cert.py', 13832, '6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2', False),
    ('cm2_gate3_chart_seam_quotient_cert.py', 9486, 'fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1', False),
    ('cm2_gate3_chart_seam_quotient_verifier.py', 6927, '3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6', False),
    ('cm2_gate3_eight_cell_symmetry_atlas_cert.py', 18141, 'd867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da', False),
    ('cm2_gate3_ge_interval_atlas_cert.py', 17052, 'ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b', False),
    ('cm2_gate5_return_word_three_norm_frontier_cert.py', 20702, 'ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695', False),
    ('cm2_gate5_return_word_three_norm_frontier_verifier.py', 14236, '0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b', False),
    ('cm2_round146_physical_centered_jet_2d_engine.py', 37018, 'ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb', False),
    ('cm2_round161_dyadic_sheared_recentering_engine.py', 10615, 'ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f', False),
    ('cm2_round162_compact_angular_coordinate_engine.py', 17332, 'f8ec6e2760ff19c6fdd65689ed134cd925b5c382778699e16e0e2f933ae162ed', False),
    ('cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json', 226291, 'f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1', False),
    ('cm2_round162_compact_angular_coordinate_infrastructure_verification_2026_07_25.json', 3481, '880a8b06af9243314d987493be631e4b3b8c4ff41c49c623ea85f5340e5c6214', False),
    ('cm2_round162_compact_angular_coordinate_producer.py', 9003, 'c03761fc21765311f41c65b7cda0da2a975c30071372cbcf613dac31e95af36b', False),
    ('cm2_round162_compact_angular_coordinate_verifier.py', 34028, 'eb97c3cbfea8a69dadfb3b6f264b0f6084841f36a129aa477737be95113f26b6', False),
    ('cm2_round162_compact_gate3_coordinate_bridge_certificate.json', 13693, '7a9889bd306567d8f68b203cab54e6fd821dd303f801e61bd82d9f32e012e4fe', False),
    ('cm2_round162_compact_gate3_coordinate_bridge_verification.json', 911, '99b443650b5f74c508e25d982aa09b06632432bd9dd880f1364c69ff7afa1583', False),
    ('cm2_round163_outgoing_chart_pruning_certificate.json', 4165, '90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539', False),
    ('cm2_round163_outgoing_chart_pruning_verification.json', 869, '28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6', False),
    ('cm2_round164_tangency_strata_pruning_certificate.json', 28514, '2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092', False),
    ('cm2_round164_tangency_strata_pruning_verification.json', 1634, '850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0', False),
    ('cm2_round169_source_g_return_signature_coverage_survey.py', 38300, '2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9', False),
    ('cm2_round169_source_g_return_signature_coverage_survey_certificate.json', 19420, '87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb', False),
    ('cm2_round169_source_g_return_signature_coverage_survey_verification.json', 2180, '90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f', False),
    ('cm2_round169_source_g_return_signature_coverage_survey_verifier.py', 38283, 'ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67', False),
    ('cm2_round171_compact_gate3_source_g_coordinate_bridge.py', 26183, 'bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75', False),
    ('cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json', 23061, '1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5', False),
    ('cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json', 3083, 'effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9', False),
    ('cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py', 38840, 'aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0', False),
    ('cm2_round173_source_g_exact_return_signature_transport.py', 47760, 'bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f', False),
    ('cm2_round173_source_g_exact_return_signature_transport_certificate.json', 36739, '5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a', False),
    ('cm2_round173_source_g_exact_return_signature_transport_verification.json', 3937, 'e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99', False),
    ('cm2_round173_source_g_exact_return_signature_transport_verifier.py', 59083, 'eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1', False),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py', 81094, '3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218', True),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json', 15984, '10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7', False),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_manifest.sha256', 1037, '9e92db7748a2c0acdce532c830f899ce153765de64a59e9f372df3099ac91b76', False),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json', 113656620, '9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54', False),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verification.json', 5011, '1f65b5e02b1d1e63bd7e41d6a88d5eb180e2be92620af4b8afa2141c9f6e344c', False),
    ('cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py', 96797, 'c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058', False),
    ('cm2_round179_source_g_residual_tube_arrangement.py', 63683, '8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab', True),
    ('cm2_round179_source_g_residual_tube_arrangement_certificate.json', 19563, 'edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111', False),
    ('cm2_round179_source_g_residual_tube_arrangement_manifest.sha256', 883, '8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76', False),
    ('cm2_round179_source_g_residual_tube_arrangement_rows.json', 131273924, 'f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42', False),
    ('cm2_round179_source_g_residual_tube_arrangement_verification.json', 4808, '37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc', False),
    ('cm2_round179_source_g_residual_tube_arrangement_verifier.py', 78867, '292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679', False),
    ('cm2_round182_source_g_clipped_graph_and_pair_arrangement.py', 67870, '8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56', True),
    ('cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json', 158815476, 'ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c', False),
    ('cm2_round204_source_g_wall_return_signature_local_replacement.py', 112111, '7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77', True),
    ('cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json', 7157575, 'e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818', False),
    ('cm2_round208_source_g_outgoing_direct_signature_materialization.py', 38692, 'c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913', True),
    ('cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json', 193161618, '4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938', False),
    ('cm2_round211_source_g_outgoing_half_open_owner_materialization.py', 20461, '9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02', True),
    ('cm2_round220_source_g_round179_resolved_child_boundary_atlas.py', 59606, 'ae5c4fc259050bafeef335b88a3504ba3de49c64154f128ec26a461ebefdd3f4', True),
    ('cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json', 294422681, '569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974', False),
    ('cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json', 67327799, '88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73', False),
    ('cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json', 3596500, 'a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0', False),
    ('cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json', 6808749, 'cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41', False),
    ('cm2_round234_source_g_wall_endpoint_order_depth6_materialization.py', 13464, '4bc6867e660cfe1ec936f03fd5543a12a8d69d3dab480366e4a9c3fbd3768d89', True),
    ('cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json', 50766450, '6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac', False),
    ('cm2_round235_source_g_single_endpoint_graph_word_key_partition.py', 13043, '8e5f807dfc43632d59cc9c994fd58907080a52bedc7789f8bb507b002ce8641a', True),
    ('cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json', 67765471, 'e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787', False),
    ('cm2_round236_source_g_wall_residual_closure_and_root_key_partition.py', 13336, '6eb2641df1b64676f145c922dc074d935813e15ce62fe1bee64309da0e509514', True),
    ('cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json', 2061199, 'b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217', False),
    ('cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json', 346302, '5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3', False),
    ('cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json', 399196, '8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446', False),
    ('cm2_round239_source_g_unaccepted_interface_local_classification_ledger_certificate.json', 4852429, '08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf', False),
    ('cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json', 49052, '65285cd08662006015c388f8dbf1eb077ca2434d80b715dbdc99c332de629359', False),
    ('cm2_round242_source_g_outgoing_graph_existence_stratum_materialization.py', 29286, '227cb00be470f33f87ee6b69612b319f8fedda51b6aa51a1ebe69ea59042de24', True),
    ('cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json', 13734655, '8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e', False),
    ('cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json', 95999515, '5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f', False),
    ('cm2_round245_source_g_retained_graph_mixed_sheet_quotient.py', 33299, '797ad3a9436740a9832c819b64cc42f3a282dc7634754cf7c2361ffb19703b1e', True),
    ('cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json', 20683081, 'c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1', False),
    ('cm2_round246_source_g_whole_signature_retained_quotient.py', 21923, '9bfa9b7cc78e510ccebba6a9184366ad4481645b0ce89d1516aa86f222981dd0', True),
    ('cm2_round246_source_g_whole_signature_retained_quotient_certificate.json', 18283721, 'a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9', False),
    ('cm2_round247_source_g_crossing_and_source_seam_retained_quotient.py', 25252, '36de859af799a02be1db22406c339a376ee752f12a563e6fbc242ef1b9340405', True),
    ('cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json', 13400149, '72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7', False),
    ('cm2_round248_source_g_wall_finite_key_retained_quotient.py', 49279, 'ac2ee77032b0f051583d891a35a4baa6bafddc0d109cc20e0a3f1f51f883e991', True),
    ('cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure.py', 72674, '72eb667b7f98fc6ed10f8617b8f8a289c4cc127b494b8777fa4cb1d99dace34c', True),
    ('cm2_round266_source_g_expanded_curved_face_closure.py', 63672, '22c2fa3555a69681f724088ad01d080e5f8925ae974f5e69307d72badd08a999', True),
    ('cm2_round266_source_g_expanded_curved_face_closure_certificate.json', 934776249, '2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf', False),
    ('cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json', 116140190, '66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f', False),
    ('cm2_round268_source_g_true_seam_candidate_geometry_exhaustion.py', 15548, 'd79f5e8b360fa494dd44968aa84ea1f108ced1645f05f6024a65e862686db71d', False),
    ('cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json', 157477, '10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9', False),
    ('cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256', 843, 'd2d4c0c34cc25dd92626a656e3a08abb031190f168f4acfe11cd451d886a538f', False),
    ('cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verification.json', 1236, 'a1b43f9f81555a1f48d0593c941c6c5741b99b473649834635ee0ccabc8a53b6', False),
    ('cm2_round269_source_g_closed_collar_direct_signature_materialization.py', 11738, 'e83da8687df53770f8294aedeb2f318468dcc8d2f466f3c3971c937c320d91e5', True),
    ('cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json', 319672585, '472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3', False),
    ('cm2_round270_source_g_outgoing_g_factor_signature_materialization.py', 13077, '0ed0df9e4873e93b03ba11e8ad8ce6274d3b9de01875363c1a1818fdbc8867df', True),
    ('cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json', 56705100, '72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea', False),
    ('cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization.py', 16839, 'ec3c3d27a766b565ce5769ff7ea2b1d42887b0f29d6bb7c5d17877eb7b62e822', True),
    ('cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json', 112741715, 'c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747', False),
    ('cm2_round272_source_g_boundary_dual_factor_wall_closure.py', 15667, 'ea2af5da7162216cce64e058515b2160bb2a96b03dbbb8c7454819d33b5ebeda', True),
    ('cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json', 1250159, '16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2', False),
    ('cm2_round273_source_g_reverse_rechart_probe.py', 10652, '40b18650a1fe8d797daf776cb9305686c21fa2eb5a7886c48ce91d697c93105c', False),
    ('cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py', 10336, '677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292', False),
    ('cm2_round275_source_g_complete_reverse_rechart_materialization.py', 11442, '4534a7000ddbc52933361f0d323ffc450e979ffc2b7ee891d3a0e770a216482f', True),
    ('cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json', 35517526, 'e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386', False),
    ('cm2_round279_source_g_collar_atom_and_face_edge_freeze.py', 18526, '03a0c55a95d3f9bd2fcd3bf39060c9f3e2cb6799d321210375e1e793972bbda1', True),
    ('cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz', 112858007, '283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe', False),
    ('cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz', 92749868, 'bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695', False),
    ('cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json', 2376, 'a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21', False),
    ('cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json', 9276, '873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc', False),
    ('cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz', 504159, '074b27dd062844331d2d43a91283f5d467fe957123294719e32237fece05d814', False),
    ('cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz', 5046131, '8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b', False),
    ('cm2_round282_source_g_strict_true_seam_normal_corridor_probe.py', 9369, '61e30d129ff27762abcf25eb074c0ba147027df08aa3cd3860496323f79306fe', False),
    ('cm2_round282_source_g_strict_true_seam_normal_corridor_probe_ledger.json.gz', 241603, '6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e', False),
    ('cm2_round282_source_g_strict_true_seam_normal_corridor_probe_result.json', 2236, 'cd054a7036d9c482357611e9af11d028179e0f34a828dca2fbe91332b178f532', False),
    ('cm2_round283_source_g_outgoing_seam_tail_independent_probe.py', 31160, '8e809f1e749408f36aa04edc06490a8b033a0da55a7e0d3454a99cf6d274bb1e', False),
    ('cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz', 15374, '2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786', False),
    ('cm2_round283_source_g_outgoing_seam_tail_independent_probe_manifest.sha256', 540, '2b8d58adf6d8857518e30ec5537e16003ac4d3c9900c10b13eaeb6f69bcc0f82', False),
    ('cm2_round283_source_g_outgoing_seam_tail_independent_probe_report.md', 4307, '697bcd1219790c7312b1331b4a3ec1409ff5e0c6508828da12d8f34e7e32c87a', False),
    ('cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json', 5325, '29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca', False),
    ('cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz', 2843201, '39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92', False),
    ('cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json', 2181, 'e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692', False),
    ('cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_verification.json', 4309, 'f1b3c6f3b9ccb8525fdf29379a7369c958a80ce278f3e5afb7232f5bbd842aa6', False),
    ('cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz', 1617322, 'bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda', False),
    ('cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json', 2642, 'a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e', False),
    ('cm2_round286_source_g_partial_overlap_exact_refinement_probe_verification.json', 4931, '817a212eeac8d855927a617dd07462747c636127e4f4b15ec709f9975a74698e', False),
    ('cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe.py', 45732, 'b39849e3aee21688ccf3eb5443984e9e0e8d7a88ed2d61e059ed3485d84c780d', True),
    ('cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit.py', 54067, 'f4821f38182bc2a14672be56edccaf8fa1c3a4b103f42fd472cdd2e42a089c6a', True),
    ('cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz', 134114861, '6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a', False),
    ('cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json', 8981, '9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569', False),
    ('cm2_round289_source_g_outgoing_seam_tail_child_materialization.py', 35853, 'e96cac6b48e333b19a44f50e50536c87b81b744b3b16bb0e28ae209cb965fffc', True),
    ('cm2_round290_source_g_isolated_atom_inner_support_closure.py', 47847, 'b528acc2d71fd71a141d4067e6dd1f172d49a23a6c44ef19dc991a57da753418', True),
    ('cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze.py', 61764, '1f485f0add666eecb83e73b5cd498b490d0f8895726717bccb4c8727600838c7', True),
    ('cm2_round292_source_g_r287_registry_overlap_exhaustion_probe.py', 48343, '69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c', True),
    ('cm2_round293_source_g_r289_r291_witness_binding_canonical_closure.py', 9992, '988282e3ef57c10f882c9796056d7ca68109ee5d294feb2512b554908251ef00', True),
    ('cm2_round294_source_g_occurrence_registry_atomic_promotion.py', 22823, '6e0ab06cf6ab7dfb7868b2fe7a4699a914e6a3b0f8b18e4181d138bc2d887a9b', True),
    ('cm2_round294b_source_g_registry_builder_admission_closure.py', 20783, 'ed8346b550c461cea28a4a01393c4c5d1be802f9e6145537a0ae7fe5c2e13192', True),
    ('cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py', 55309, 'd147b6299a5e37b0e2ec104af64920e9b61f8a00491eb616b6a0e0eed66d6d08', True),
    ('cm2_round306b0_source_g_r306a_universe_support_source_freeze.py', 61939, '48f38e2b90aa2c1b934ba657f8c6e66a8cb97fa89f9439a0b11ed5fbb3d20d83', True),
    ('cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py', 90721, '97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321', True),
    ('cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze.py', 73458, '3538e17fd523384d31a2fbf46505ff4ee5bf7ba8f41db14534e55edaa04eabca', True),
)

CLOSURE_RECORDS: tuple[dict[str, Any], ...] = tuple(
    {
        "filename": filename,
        "exact_size": exact_size,
        "sha256": sha256,
        "root_source": root_source,
    }
    for filename, exact_size, sha256, root_source in FROZEN_CATALOG
)
ROOT_RECORDS: tuple[dict[str, Any], ...] = tuple(
    record for record in CLOSURE_RECORDS if record["root_source"]
)


GOVERNANCE_SEALS: tuple[dict[str, Any], ...] = (
    {"label": "AF0_CONTRACT", "filename": "cm2_round306b1af0_source_g_formal_full_feature_cover_schema_contract.py", "size": 46865, "sha256": "d2edaf5247e90ad1e9344261e18b29612ed37b8d928bd1f715c5a6fab3a70e04"},
    {"label": "AF1_CONTRACT", "filename": "cm2_round306b1af1_source_g_formal_full_feature_cover_pre_schema_admission_contract.py", "size": 30391, "sha256": "93d35ed11c98b3721f8ec24ec8c440278e5e947b8f5e63a7dbdc4b1d66380e39"},
    {"label": "AF2_CONTRACT", "filename": "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", "size": 52538, "sha256": "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"},
    {"label": "AF2_INDEPENDENT_REPLAY", "filename": "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_replay.py", "size": 23694, "sha256": "38551c822f9aa74989b54749a3e05e8fe9bdce205fb12efb12eaa7382e6ccab4"},
    {"label": "AF2_INDEPENDENT_RESULT", "filename": "cm2_round306b1af2_source_g_primitive_support_source_partition_independent_result.json", "size": 2540, "sha256": "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"},
    {"label": "AF2_PRIMARY_REPLAY", "filename": "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_replay.py", "size": 20783, "sha256": "b7fcae488bd1e9e301f7191e65ade22f87c393a083a1335147ccf1bc92cddb27"},
    {"label": "AF2_PRIMARY_RESULT", "filename": "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", "size": 2540, "sha256": "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"},
    {"label": "B0_MANIFEST", "filename": "cm2_round306b0_source_g_r306a_universe_support_source_freeze_manifest.sha256", "size": 1760, "sha256": "9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269"},
    {"label": "B0_RESULT", "filename": "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json", "size": 9450, "sha256": "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735"},
    {"label": "B0_VERIFICATION", "filename": "cm2_round306b0_source_g_r306a_universe_support_source_freeze_verification.json", "size": 7003, "sha256": "f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590"},
    {"label": "B1G0_MANIFEST", "filename": "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", "size": 1959, "sha256": "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"},
    {"label": "B1G0_RESULT", "filename": "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", "size": 5006, "sha256": "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e"},
    {"label": "B1G0_VERIFICATION", "filename": "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json", "size": 11575, "sha256": "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a"},
    {"label": "B1R0_MANIFEST", "filename": "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_manifest.sha256", "size": 1571, "sha256": "f23f4639629e920596e1ecadbb1cd7708f93308dc5780a0f82c196edc0f46aec"},
    {"label": "B1R0_RESULT", "filename": "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_result.json", "size": 3019, "sha256": "ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04"},
    {"label": "B1R0_VERIFICATION", "filename": "cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_verification.json", "size": 11531, "sha256": "2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040"},
    {"label": "OLD_C0_CONTRACT", "filename": "cm2_round306b2c0_source_g_feature_transition_pair_routing_contract.py", "size": 53212, "sha256": "6a4fbbc3c614b7adaf275d0870a0205360827ed9fe89b8e26748e966a04f4d69"},
)


# Final byte/row/role authority domains copied development-time from the
# audited freeze contract.  Runtime code parses only these inert literals;
# it never imports or executes that contract or an upstream producer.
AUTHORITY_FILE_RECORDS_JSON = '[{"exact_size":113656620,"filename":"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json","sha256":"9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"},{"exact_size":131273924,"filename":"cm2_round179_source_g_residual_tube_arrangement_rows.json","sha256":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"},{"exact_size":158815476,"filename":"cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json","sha256":"ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"},{"exact_size":7157575,"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"exact_size":193161618,"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"exact_size":140690802,"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","sha256":"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"},{"exact_size":294422681,"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"exact_size":3596500,"filename":"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json","sha256":"a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"},{"exact_size":50766450,"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","sha256":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"},{"exact_size":67765471,"filename":"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json","sha256":"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"},{"exact_size":2061199,"filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","sha256":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"},{"exact_size":346302,"filename":"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json","sha256":"5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3"},{"exact_size":399196,"filename":"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json","sha256":"8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446"},{"exact_size":13734655,"filename":"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json","sha256":"8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"},{"exact_size":95999515,"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"exact_size":20683081,"filename":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","sha256":"c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"},{"exact_size":18283721,"filename":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","sha256":"a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"},{"exact_size":13400149,"filename":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","sha256":"72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"},{"exact_size":205148977,"filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","sha256":"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"},{"exact_size":406539851,"filename":"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json","sha256":"ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"},{"exact_size":934776249,"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","sha256":"2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"},{"exact_size":319672585,"filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","sha256":"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"},{"exact_size":56705100,"filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","sha256":"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"},{"exact_size":112741715,"filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","sha256":"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"},{"exact_size":1250159,"filename":"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","sha256":"16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2"},{"exact_size":35517526,"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","sha256":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"},{"exact_size":112858007,"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz","sha256":"283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe"},{"exact_size":92749868,"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz","sha256":"bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695"},{"exact_size":7529109,"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"exact_size":134114861,"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz","sha256":"6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"},{"exact_size":7237078,"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz","sha256":"d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e"},{"exact_size":9576526,"filename":"cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz","sha256":"9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025"},{"exact_size":5544437,"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","sha256":"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"},{"exact_size":262951902,"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz","sha256":"c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"},{"exact_size":26672326,"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz","sha256":"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"},{"exact_size":162499140,"filename":"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz","sha256":"c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"},{"exact_size":32731854,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz","sha256":"79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"},{"exact_size":23240985,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz","sha256":"2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"},{"exact_size":13922080,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz","sha256":"041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"},{"exact_size":25932945,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz","sha256":"d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"},{"exact_size":11720893,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz","sha256":"5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"},{"exact_size":140958,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz","sha256":"834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a"},{"exact_size":108363350,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz","sha256":"c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56"},{"exact_size":123019951,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz","sha256":"4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"},{"exact_size":105989322,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz","sha256":"19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"}]'
AUTHORITY_FILE_ROWS_JSON = '[{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":113656620,"filename":"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":131273924,"filename":"cm2_round179_source_g_residual_tube_arrangement_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"exact_size":158815476,"filename":"cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE","ANALYTIC_LINEAGE"],"exact_size":7157575,"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE","ANALYTIC_LINEAGE"],"exact_size":193161618,"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"exact_size":140690802,"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE","PROOF_EVIDENCE"],"exact_size":294422681,"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":3596500,"filename":"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":50766450,"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":67765471,"filename":"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE","PROOF_EVIDENCE"],"exact_size":2061199,"filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":346302,"filename":"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":399196,"filename":"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":13734655,"filename":"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"exact_size":95999515,"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"],"sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":20683081,"filename":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":18283721,"filename":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":13400149,"filename":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"exact_size":205148977,"filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":406539851,"filename":"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":934776249,"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":319672585,"filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":56705100,"filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":112741715,"filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":1250159,"filename":"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2"},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"exact_size":35517526,"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"],"sha256":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":112858007,"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe"},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"exact_size":92749868,"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"],"sha256":"bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695"},{"admitted_for_construction":false,"authority_roles":["OUTER_ENVELOPE_ONLY"],"exact_size":7529109,"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["EXISTENCE_OR_EQUIVALENCE_THEOREM","INNER_SUPPORT","NORMALIZED_FULL_SUPPORT"],"sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":134114861,"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":7237078,"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e"},{"admitted_for_construction":false,"authority_roles":["DIAGNOSTIC_ONLY"],"exact_size":9576526,"filename":"cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE"],"sha256":"9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025"},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE","OUTER_ENVELOPE_ONLY"],"exact_size":5544437,"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["EXISTENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT","INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"],"sha256":"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":262951902,"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":26672326,"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":162499140,"filename":"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":32731854,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"exact_size":23240985,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"],"sha256":"2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":13922080,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":25932945,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":11720893,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":140958,"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a"},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"exact_size":108363350,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"],"sha256":"c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56"},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"exact_size":123019951,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"],"sha256":"4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"exact_size":105989322,"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"],"sha256":"19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"}]'
TABLE_AUTHORITIES_JSON = '[{"admitted_for_construction":true,"authority":"R182.collar_leaf_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{"native_attachment_result_sha256":"9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269"},"filename":"cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.collar_leaf_rows[]","ledger_sha256":null,"row_count":202840,"row_hashes_sha256":null,"row_id_field":"row_id (packed column 0)","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"ced6d2764a7e1f5d404c1d56249e428f0754e53e7dded620e5904f9eb80b694c","source_exact_size":158815476,"source_sha256":"ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c"},{"admitted_for_construction":true,"authority":"R220.coordinate_corner_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.coordinate_corner_rows.rows[]","ledger_sha256":null,"row_count":137536,"row_hashes_sha256":null,"row_id_field":"corner_id (packed column 0)","row_ids_sha256":"032a80a350c671341ed4a231f92319fe6af3ccd48297f401170e789d6d0a9868","row_schema_contract":{},"rows_sha256":"226fb12c2c3f6ac1a59e4e6a2d9f32a2b257d33f6edcb229f81954e4506e8efd","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R220.coordinate_edge_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.coordinate_edge_rows.rows[]","ledger_sha256":null,"row_count":206304,"row_hashes_sha256":null,"row_id_field":"edge_id (packed column 0)","row_ids_sha256":"7511a3ecb63328b0389bdc9eab0dd7fa2560f476c50d8b78c18d3410848c0408","row_schema_contract":{},"rows_sha256":"cfb3b2a341695b8b0a7d741931ca1494787dc3cfdec53031c59b23cb12c53977","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R220.coordinate_face_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.coordinate_face_rows.rows[]","ledger_sha256":null,"row_count":103152,"row_hashes_sha256":null,"row_id_field":"face_id (packed column 0)","row_ids_sha256":"b6ac692bb13db5519a83c21d433159f124748cc32f1a85d550e8fd8a0f64a402","row_schema_contract":{},"rows_sha256":"9eb5d5eb90757d2a724302c1682929eacc6638bcd197aaac80fddd3f59207b34","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R220.formal_coordinate_adjacency_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.formal_coordinate_adjacency_rows.rows[]","ledger_sha256":null,"row_count":10384,"row_hashes_sha256":null,"row_id_field":"coordinate_adjacency_id (packed column 0)","row_ids_sha256":"ab8fbea5baaac034b905d4ad2760519f87da25378cd8c2782015e8081ebd68cf","row_schema_contract":{},"rows_sha256":"dca8ddbb66b73ef615f1b1cd2c4b7ee453737ff18ed44e03e2ac222d5005d88f","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R220.one_step_split_interface_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.one_step_split_interface_rows.rows[]","ledger_sha256":null,"row_count":13076,"row_hashes_sha256":null,"row_id_field":"split_interface_id (packed column 0)","row_ids_sha256":"6c907805c3980146287fd765fafa4f279c4ecedf19b314947b2e975b458c3297","row_schema_contract":{},"rows_sha256":"221b5568223c452c9c590157afd592dfdc0f244e1322c275d55263b747d18f57","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":false,"authority":"R220.rejected_exact_coordinate_coincidence_rows","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.rejected_exact_coordinate_coincidence_rows.rows[]","ledger_sha256":null,"row_count":9830,"row_hashes_sha256":null,"row_id_field":"candidate_id (packed column 0)","row_ids_sha256":"289f8995be84c457d8e55cb7d17313c4fa57dd65019d4cd85784018c8f03921a","row_schema_contract":{},"rows_sha256":"e61aae78e76404959074465e299a256e24c778d195d2902a452db8fed2d21092","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R220.resolved_child_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.coordinate_boundary_atlas.tables.resolved_child_rows.rows[]","ledger_sha256":null,"row_count":17192,"row_hashes_sha256":null,"row_id_field":"atlas_child_id (packed column 0)","row_ids_sha256":"a966de2c22eabfcfe695ae3d66ee88b1908047e916f3345ea65c80be1b42edb1","row_schema_contract":{},"rows_sha256":"30d27f8d112331412a8db92e12acc69b2184b881a7ff1a256148ab335aa30ed2","source_exact_size":294422681,"source_sha256":"569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"},{"admitted_for_construction":true,"authority":"R232.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.whole_origin_promotion_rows[]","ledger_sha256":null,"row_count":2220,"row_hashes_sha256":null,"row_id_field":"whole_origin_promotion_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"65ff4166409729d6678e40b7435c137096bab158d8f41ce47c1588c0329f74ca","source_exact_size":3596500,"source_sha256":"a33d14fd7fd0ca0bb8e64efefd97be0839a5a8107b759f2219c14580ef3aa8c0"},{"admitted_for_construction":true,"authority":"R234.root_summary_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.root_summary_rows[]","ledger_sha256":null,"row_count":2640,"row_hashes_sha256":null,"row_id_field":"root_summary_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"9a1887e1b7caf00cf5c6d247f71fc8af5c06e7dc1025d5a9f06cc4c287019361","source_exact_size":50766450,"source_sha256":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"},{"admitted_for_construction":true,"authority":"R234.resolved_descendant_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.resolved_descendant_rows[]","ledger_sha256":null,"row_count":12200,"row_hashes_sha256":null,"row_id_field":"materialized_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"04700e272242cd97ae7851ffcd7cdb255afdb0921d3e681373a4fc8b1edcd3a0","source_exact_size":50766450,"source_sha256":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"},{"admitted_for_construction":true,"authority":"R234.depth6_frontier_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.depth6_frontier_rows[]","ledger_sha256":null,"row_count":38376,"row_hashes_sha256":null,"row_id_field":"frontier_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"a1b3bf193ad10045f52244c3e40c52f78e0aeacffa3ba52c262bc8912fc9b5a6","source_exact_size":50766450,"source_sha256":"6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"},{"admitted_for_construction":true,"authority":"R237.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.whole_origin_promotion_rows[]","ledger_sha256":null,"row_count":240,"row_hashes_sha256":null,"row_id_field":"whole_origin_promotion_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"fcec0a5790b05960acc1cdf9aa3f2cc9838264ee7583a70a445da1e0dba792f4","source_exact_size":346302,"source_sha256":"5fa46f8c6d8074770ebbf8cbdb2f0590dbdf5710254d05c6a0a3aca0953359f3"},{"admitted_for_construction":true,"authority":"R238.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.whole_origin_promotion_rows[]","ledger_sha256":null,"row_count":264,"row_hashes_sha256":null,"row_id_field":"whole_origin_promotion_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"e2e69aafa1444ba504b006a53ff44fe51c81dba52aa8edd3a2fff746c6fdec30","source_exact_size":399196,"source_sha256":"8200ba9c35ba32c938eb66beb7a4040908db9b81fc449881a55b09e67b517446"},{"admitted_for_construction":false,"authority":"R244.formal_Round244_known_connectivity_block_carry_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_Round244_known_connectivity_block_carry_ledger.rows[]","ledger_sha256":null,"row_count":7388,"row_hashes_sha256":"5f7469b8952e782838b4636b2c6e2d25f37b2d128efe7fdca357e2c92fdb398f","row_id_field":"block_carry_row_id","row_ids_sha256":"ccd7d9d5be04889105e43fe00a71511d10e249bf2cd8a1e1c38560e3b1cb79d2","row_schema_contract":{},"rows_sha256":"748d83634271e0e45df55c840291a85d67fe1c4b4f5aacca2d8976197977ace4","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_cross_parent_same_chart_bulk_edge_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_cross_parent_same_chart_bulk_edge_ledger.rows[]","ledger_sha256":null,"row_count":328,"row_hashes_sha256":"936e5f039960d168d5a4f4866335ad4b6f4cd27752e4f562a434ea3042b5ed47","row_id_field":"cross_parent_bulk_edge_row_id","row_ids_sha256":"327dbfdf6c9b221173d23dfcb237114a07a53f9da9133f9a158f6fbc81fb1641","row_schema_contract":{},"rows_sha256":"17c1f65799070a1549ca4158eeb133d4ff39d924e361c1076780580144593ac8","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_different_parent_candidate_reconciliation_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_different_parent_candidate_reconciliation_ledger.rows[]","ledger_sha256":null,"row_count":9830,"row_hashes_sha256":"fc3cf7ec9af53b7cf9a191fea8f15d634858ff5293de5723e2478eeab2d98e0d","row_id_field":"candidate_reconciliation_row_id","row_ids_sha256":"c22aac287a6ad9da8c2842ed9c8e9b5ee1bddc97a1ce0bf0de298e239e4aee19","row_schema_contract":{},"rows_sha256":"a8642fbdff97dda0f321829af22442b8a6e1e952390c12761e760b2f634c08dc","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_occurrence_known_block_incidence_delta_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_occurrence_known_block_incidence_delta_ledger.rows[]","ledger_sha256":null,"row_count":20,"row_hashes_sha256":"1969564950552cf1d832bb3e02cdd3b014d943f456fa191938b4bcb2648ff700","row_id_field":"incidence_delta_row_id","row_ids_sha256":"23c5165548a2916f1aefa5dd0a8cc0fb895a3a3796ebf24c554af3b29bbd06e9","row_schema_contract":{},"rows_sha256":"a877293b6ce57915ddb3a0e6092cded34eb597f4e4e81d1c2c583889d880f397","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_post_Round244_key_frontier_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_post_Round244_key_frontier_ledger.rows[]","ledger_sha256":null,"row_count":116,"row_hashes_sha256":"1c4c8ade9c8f0c3393e2be83ca5252c90bc3d6c7e58f6f347ddbbec698918230","row_id_field":"key_frontier_row_id","row_ids_sha256":"8734c757768db678eea09be5c05cbcdb5c688b4bfd8d19240d6171007bfb5b9f","row_schema_contract":{},"rows_sha256":"4200e1b4d58013403610f1d002bf75934d35e8830df7fa142bd44411ff444cec","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_post_Round244_occurrence_known_block_frontier_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_post_Round244_occurrence_known_block_frontier_ledger.rows[]","ledger_sha256":null,"row_count":53968,"row_hashes_sha256":"a69039a0ba44a832664ff4ad29193c282fcfc5ae240baa115b10ac69986f2edb","row_id_field":"post_frontier_row_id","row_ids_sha256":"1df792189eac227bb8cd61b111f408a67650da1a28b875f95257deee10b4e547","row_schema_contract":{},"rows_sha256":"3deef6442de789fe29b8866e08fb1056ed2f4c2c68c986a297c2f25faf7b1211","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":false,"authority":"R244.formal_resolved_bulk_component_ledger","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.formal_resolved_bulk_component_ledger.rows[]","ledger_sha256":null,"row_count":8148,"row_hashes_sha256":"52fb16c30fa7c30b8e844a2777b44ecc6721c2ea5d424b07690e2e0b86ce2c78","row_id_field":"resolved_bulk_component_row_id","row_ids_sha256":"d19bcbd02bb583fd242485eb037fbbf28db3e23a587a3729d1a4b6fd56bb8e23","row_schema_contract":{},"rows_sha256":"7a65957c962885f9e67d3aff19349744360211f2923e99fdf7313996d28116a1","source_exact_size":95999515,"source_sha256":"5b08d568cccd302ac2dd62e7e9b6573ce83e015181ead168812159c9f882712f"},{"admitted_for_construction":true,"authority":"R235.single_endpoint_graph_partition_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.single_endpoint_graph_partition_rows[]","ledger_sha256":null,"row_count":38328,"row_hashes_sha256":null,"row_id_field":"endpoint_graph_partition_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731","source_exact_size":67765471,"source_sha256":"e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"},{"admitted_for_construction":true,"authority":"R236.double_endpoint_partition_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.double_endpoint_partition_rows[]","ledger_sha256":null,"row_count":16,"row_hashes_sha256":null,"row_id_field":"double_endpoint_partition_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"68f41212de0da7f3468a321a682978daa052cb65a611d756a901ca095bcc0bf6","source_exact_size":2061199,"source_sha256":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"},{"admitted_for_construction":false,"authority":"R236.crossing_dependency_discharge_rows","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".result.crossing_dependency_discharge_rows[]","ledger_sha256":null,"row_count":32,"row_hashes_sha256":null,"row_id_field":"crossing_dependency_discharge_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"26a8e54cb98f181d79d868ba446dd5cce32e3f9ab00104b4a05616623740e71d","source_exact_size":2061199,"source_sha256":"b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"},{"admitted_for_construction":true,"authority":"R242.formal_positive_2D_transition_sheet_patch_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_positive_2D_transition_sheet_patch_ledger.rows[]","ledger_sha256":null,"row_count":264,"row_hashes_sha256":"6ed321a2f28be8b51b83b48cb3bff50f4ab67a3020170b8f63d5bac934ab9407","row_id_field":"transition_sheet_patch_row_id","row_ids_sha256":"0f03acdd1fa621e64a89a79181c83af802a6a3ff338290132acbf0641155baa8","row_schema_contract":{},"rows_sha256":"aaf7a94af40427dd8e1b805f2aa5c8c0532e7dc5b2420c803e165d39ba5c0a0f","source_exact_size":13734655,"source_sha256":"8d32c381e21c03aad6a531b7e5a527d295783b7e3e38baa1e6bcba20c40db22e"},{"admitted_for_construction":true,"authority":"R245.formal_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_retained_stratum_node_ledger.rows[]","ledger_sha256":null,"row_count":3664,"row_hashes_sha256":"86bad0d45642388bcac65633d47088b93184d77abdb2be68096cb139e192110c","row_id_field":"retained_stratum_node_id","row_ids_sha256":"ef81a9a7d264961541edfb9ba9e8e4c37ddbf7dea01efa3eb72d500a82b44ed5","row_schema_contract":{},"rows_sha256":"38583b1aa3f37e37dc03c2b59b2a31c18346462d3d918e001040d6651b11401b","source_exact_size":20683081,"source_sha256":"c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"},{"admitted_for_construction":true,"authority":"R246.formal_new_whole_signature_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_new_whole_signature_retained_stratum_node_ledger.rows[]","ledger_sha256":null,"row_count":2220,"row_hashes_sha256":"f43d31209c552f275144ede960e49bd1ee4044cb40ee3050340e23d6d38bc671","row_id_field":"retained_stratum_node_id","row_ids_sha256":"488711dda41780ef47dbe34834ab8e3a41995a471260d7743b562c0190b6c86f","row_schema_contract":{},"rows_sha256":"476a4fe0955fd1672ba5ba1177e65f479bf10a2bfdb62d6443f3d702c1649414","source_exact_size":18283721,"source_sha256":"a448359c0a9b4495e54afe6e2d860c20fb222684bae46ee108574782a5a33bc9"},{"admitted_for_construction":true,"authority":"R247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_new_crossing_and_source_seam_retained_stratum_node_ledger.rows[]","ledger_sha256":null,"row_count":504,"row_hashes_sha256":"23e3495f9f481cc3f1d037741b27403d7bc4c0be8afe118201ba52a6fc4ce9a7","row_id_field":"retained_stratum_node_id","row_ids_sha256":"8896ff95e8e1c4dd5eb7f53ce3dcf9f39abbcd883c2641846b69129fc7040143","row_schema_contract":{},"rows_sha256":"737b59a2a4a9e67664b9e0a080034083190b67c614849bac9b87b5b4ecaf9629","source_exact_size":13400149,"source_sha256":"72188f5d99a220f44698f3023dd606633b364adbd02d5e20e5d4fa0ff6e1b2c7"},{"admitted_for_construction":true,"authority":"R248.formal_wall_positive_volume_bulk_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_wall_positive_volume_bulk_ledger.rows[]","ledger_sha256":null,"row_count":88936,"row_hashes_sha256":"e46f242e15bcba4111e14aac3c1dc5d82a5350e9e1514f2b9f90cdbc853e525d","row_id_field":"wall_bulk_node_id","row_ids_sha256":"6106c39894a7947293934b0b061bcae04e1a2902976b63ccd1756d7790cb6154","row_schema_contract":{},"rows_sha256":"aff5ea1401a6919529d1d54fe54bb9b8d378456fa48f88a75043505b5ee7b8b0","source_exact_size":205148977,"source_sha256":"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"},{"admitted_for_construction":true,"authority":"R248.formal_wall_half_open_sheet_owner_ledger","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_wall_half_open_sheet_owner_ledger.rows[]","ledger_sha256":null,"row_count":38360,"row_hashes_sha256":"be2e8b880f3a0c8fb833a7ba8dce0bd86d5526b400569377f0fcb66692a8c7e0","row_id_field":"wall_sheet_node_id","row_ids_sha256":"fbb15ef7122367925c72f9d0e396141d3f04a271b78064af41e1f68d9d06cd61","row_schema_contract":{},"rows_sha256":"e61754dc51732c4c82876d1c2e83fa040747d23253addd64350728169f5ae44b","source_exact_size":205148977,"source_sha256":"fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"},{"admitted_for_construction":true,"authority":"R264.formal_endpoint_empty_branch_correction_disposition_ledger","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_endpoint_empty_branch_correction_disposition_ledger.rows[]","ledger_sha256":null,"row_count":400,"row_hashes_sha256":"3d3e744252a300176a464f1de9e8369d580d6732e50eae292bd0d51176028e3a","row_id_field":"endpoint_empty_branch_disposition_row_id","row_ids_sha256":"9b6b78f9feb488bf6e35ed3821e40066e8a665d007145601330ed22f97d89c09","row_schema_contract":{},"rows_sha256":"fdf499ca22f287866a24685a7671f8cfe950015be72c3da03db2331db7e38285","source_exact_size":406539851,"source_sha256":"ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f"},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_valid_virtual_node_frontier_ledger","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_post_Round266_valid_virtual_node_frontier_ledger.rows[]","ledger_sha256":null,"row_count":133284,"row_hashes_sha256":"9c31ba929e13eeaea29a9f6abe7cf324222eacb25d123a9b12252b386c12a32e","row_id_field":"post_Round266_valid_virtual_node_frontier_row_id","row_ids_sha256":"2d42533f48f864f01e6bd4a46470e7266c1a2cec590380483cfb7cbfb84634f2","row_schema_contract":{},"rows_sha256":"8c394c1d1b2b42025c25a00ef24ecba748981ed93c75b9aba20ddf15ff8597d5","source_exact_size":934776249,"source_sha256":"2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_component_member_frontier_ledger","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_post_Round266_component_member_frontier_ledger.rows[]","ledger_sha256":null,"row_count":259752,"row_hashes_sha256":"1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee","row_id_field":"post_Round266_component_member_frontier_row_id","row_ids_sha256":"f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6","row_schema_contract":{},"rows_sha256":"28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257","source_exact_size":934776249,"source_sha256":"2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"},{"admitted_for_construction":true,"authority":"B1G0.graph_source_inventory_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".graph_source_inventory_rows[]","ledger_sha256":"a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0","row_count":38624,"row_hashes_sha256":"7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace","row_id_field":"Round306B1G0_graph_source_inventory_row_id","row_ids_sha256":"982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc","row_schema_contract":{},"rows_sha256":"beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f","source_exact_size":11720893,"source_sha256":"5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"},{"admitted_for_construction":true,"authority":"B1G0.graph_sheet_join_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".graph_sheet_join_rows[]","ledger_sha256":"3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda","row_count":38624,"row_hashes_sha256":"a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5","row_id_field":"Round306B1G0_graph_sheet_join_row_id","row_ids_sha256":"b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300","row_schema_contract":{},"rows_sha256":"9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f","source_exact_size":13922080,"source_sha256":"041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"},{"admitted_for_construction":true,"authority":"B1G0.graph_side_join_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".graph_side_join_rows[]","ledger_sha256":"108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e","row_count":76848,"row_hashes_sha256":"2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6","row_id_field":"Round306B1G0_graph_side_join_row_id","row_ids_sha256":"9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53","row_schema_contract":{},"rows_sha256":"43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2","source_exact_size":25932945,"source_sha256":"d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"},{"admitted_for_construction":true,"authority":"B1G0.r264_correction_disposition_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".r264_correction_disposition_rows[]","ledger_sha256":"a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671","row_count":400,"row_hashes_sha256":"f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592","row_id_field":"Round306B1G0_R264_correction_disposition_row_id","row_ids_sha256":"b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf","row_schema_contract":{},"rows_sha256":"a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67","source_exact_size":140958,"source_sha256":"834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a"},{"admitted_for_construction":true,"authority":"B1G0.b0_member_backbinding_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".b0_member_backbinding_rows[]","ledger_sha256":"65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541","row_count":115456,"row_hashes_sha256":"88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae","row_id_field":"Round306B1G0_B0_member_backbinding_row_id","row_ids_sha256":"ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72","row_schema_contract":{},"rows_sha256":"35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6","source_exact_size":32731854,"source_sha256":"79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"},{"admitted_for_construction":false,"authority":"B1G0.gap_rows","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".gap_rows[]","ledger_sha256":"5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e","row_count":154096,"row_hashes_sha256":"ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35","row_id_field":"Round306B1G0_gap_row_id","row_ids_sha256":"f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421","row_schema_contract":{},"rows_sha256":"d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b","source_exact_size":23240985,"source_sha256":"2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"},{"admitted_for_construction":true,"authority":"B0.member_support_source_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".member_support_source_rows[]","ledger_sha256":"58ad4ebe98be5023f31870a0d0d3e0d135d153553393aa56a67f4ef1760f68a3","row_count":564492,"row_hashes_sha256":"382e7a7ae0e857b812635e0d4bb10571d1aa459a27acd178d81b12f9c68d6285","row_id_field":"Round306B0_member_support_source_row_id","row_ids_sha256":"87b4d34c40c3c1caf053ccb9b4c6c6c32cf6a33ac184f6181864105b500b6d3a","row_schema_contract":{},"rows_sha256":"c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5","source_exact_size":162499140,"source_sha256":"c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"},{"admitted_for_construction":true,"authority":"R294.occurrence_registry_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{"occurrence_ids_sha256":"169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936"},"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":431208,"row_hashes_sha256":"ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56","row_id_field":"Round294_occurrence_registry_row_id","row_ids_sha256":"bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509","row_schema_contract":{},"rows_sha256":"33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044","source_exact_size":262951902,"source_sha256":"c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb"},{"admitted_for_construction":true,"authority":"R294.representation_binding_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":46288,"row_hashes_sha256":"538ddd3aaa79da6ff5dd0738523bcc7bb6c6c192051ada1f96131053fd8190b3","row_id_field":"Round294_occurrence_representation_binding_row_id","row_ids_sha256":"1a03d7c6d95d6144d4b271e46eb6b83ab4c577f7eb5b9f94d34de692247e50ff","row_schema_contract":{},"rows_sha256":"ece198bf5e8b95448b09f60061677feafca3416525ba80f3b88a51e766414be7","source_exact_size":26672326,"source_sha256":"f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833"},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_expanded_occurrence_frontier_ledger","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_post_Round266_expanded_occurrence_frontier_ledger.rows[]","ledger_sha256":null,"row_count":126468,"row_hashes_sha256":"08fa74d62a0673cb02339bae0df05007e7f4cb9d452d69feef79a958ceaa5ad9","row_id_field":"post_Round266_expanded_occurrence_frontier_row_id","row_ids_sha256":"db01addd10a5112d56109695684d64994b927ce009e71b5e39dc95de2846acce","row_schema_contract":{},"rows_sha256":"441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351","source_exact_size":934776249,"source_sha256":"2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"},{"admitted_for_construction":true,"authority":"R174.resolved_3d_occurrence_rows","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.resolved_3d_occurrence_rows[]","ledger_sha256":null,"row_count":72500,"row_hashes_sha256":null,"row_id_field":"packed column 0 row_id","row_ids_sha256":"3748e6a910c2d009d984d5402ad8310f81ac0c4b33b618ce3a420924e4ede496","row_schema_contract":{},"rows_sha256":"bbd6c0742f16314f4d865e5ba7d3f693939d77764fca11978bb984a5fdb181d5","source_exact_size":113656620,"source_sha256":"9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"},{"admitted_for_construction":true,"authority":"R179.resolved_3d_child_rows","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round179_source_g_residual_tube_arrangement_rows.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.resolved_3d_child_rows[]","ledger_sha256":null,"row_count":17192,"row_hashes_sha256":null,"row_id_field":"packed column 0 row_id","row_ids_sha256":"51294c66bb9e48c95c97dab1547380f288d3eaaa902b1ee71ec6d2f224b05a5d","row_schema_contract":{},"rows_sha256":"3b62a6e259b99484a6a398bc1b1e961dcaae2b4c1dc3671375134aff893b8936","source_exact_size":131273924,"source_sha256":"f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"},{"admitted_for_construction":true,"authority":"R204.formal_local_open_3D_region_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_local_open_3D_region_ledger.rows[]","ledger_sha256":null,"row_count":736,"row_hashes_sha256":"3be5e63b0ba9e11e77ac8c828c7d8212e9edb74735e475024bcafcdcdbf0a85a","row_id_field":"region_row_id","row_ids_sha256":"814edddc1d7ccb6bcd83cd7a6784fe16e1e85a1f8f3948bc26e591fa63095b60","row_schema_contract":{},"rows_sha256":"8a1141a6890fc5165adf4e6accf4130750107ec1336bb8177150c08825785d08","source_exact_size":7157575,"source_sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"admitted_for_construction":true,"authority":"R208.formal_local_open_3D_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_local_open_3D_signature_ledger.rows[]","ledger_sha256":null,"row_count":36040,"row_hashes_sha256":"df3eccd71d413522e516177bf65f9369ffc7c0fc1f3ebfcec1aecc5165095297","row_id_field":"region_row_id","row_ids_sha256":"85c6ae741dcee053d8fa4a37eceb2c97b1ad5859b7636194086a03947969b1d0","row_schema_contract":{},"rows_sha256":"59dd5ee4159b093709f9d484302aba0133e0af52f16adac646b44c83ace8237f","source_exact_size":193161618,"source_sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"admitted_for_construction":true,"authority":"R204.formal_2D_sheet_lineage.target_sheet_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_2D_sheet_lineage.target_sheet_rows[]","ledger_sha256":null,"row_count":224,"row_hashes_sha256":"ce9c795e707e5aad2c8adb81bdff107153bbc07e648440750948fde2a13571f3","row_id_field":"sheet_row_id","row_ids_sha256":"2efad6307c5601e2ddb040fe36df17b5525461fc22598874ab8feaab54f4dc43","row_schema_contract":{},"rows_sha256":"bece147e2a055cefec795808eedfb488ca2febbf072160cff887c12421d24d07","source_exact_size":7157575,"source_sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"admitted_for_construction":true,"authority":"R208.formal_direct_leaf_signature_base_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_direct_leaf_signature_base_ledger.rows[]","ledger_sha256":null,"row_count":18324,"row_hashes_sha256":"5ee61b8ecdf998d7a92783d43ca36e934b27b574b2f2538104e67e36f9666b62","row_id_field":"leaf_row_id","row_ids_sha256":"cd36d56f3e4b408a9470e55656a7b2a6979b705041500549698efa6b8330316a","row_schema_contract":{},"rows_sha256":"db6d4b0ddab0ea74774fe62d0dc1c9ef474336c7bb310ca26b0ad2f593e0a36d","source_exact_size":193161618,"source_sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"admitted_for_construction":true,"authority":"R208.formal_leaf_geometry_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_leaf_geometry_ledger.rows[]","ledger_sha256":null,"row_count":18324,"row_hashes_sha256":"1bd19072c4093b5175dc7d4fbb6838159aaed775c870aeb2ddbb1b90e19d1bd3","row_id_field":"leaf_row_id","row_ids_sha256":"cd36d56f3e4b408a9470e55656a7b2a6979b705041500549698efa6b8330316a","row_schema_contract":{},"rows_sha256":"da21fae5a5a5734690f152526958d30e1baf2f0aa64077a89febf4bbdbcf55a0","source_exact_size":193161618,"source_sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"admitted_for_construction":true,"authority":"R208.formal_final_factor_face_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_final_factor_face_ledger.rows[]","ledger_sha256":null,"row_count":18412,"row_hashes_sha256":"7c63ea6f4786e5b9702d7ef5054dffbae4a6287615c4f3aace0331930aa666c8","row_id_field":"face_row_id","row_ids_sha256":"a04fa242a668f5cd7d389701c149b1347ca15b4c3a2f2efddd31ed136745dbec","row_schema_contract":{},"rows_sha256":"1530fd15aff865fd7d6c3b0c2425b5429e886e780d63af5e52136495f8e84fbd","source_exact_size":193161618,"source_sha256":"4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"},{"admitted_for_construction":true,"authority":"R211.formal_2D_sheet_owner_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_2D_sheet_owner_ledger.rows[]","ledger_sha256":null,"row_count":17716,"row_hashes_sha256":"97e1b400d0df06228239f5bda23051cdae8b0b0caa1be0fdb64d8b4bc5527c7e","row_id_field":"sheet_row_id","row_ids_sha256":"bb25748d3c7bc46043f9588983788ecc3cb4a38faa8d40c6ea13383c262570aa","row_schema_contract":{},"rows_sha256":"ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb","source_exact_size":140690802,"source_sha256":"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"},{"admitted_for_construction":true,"authority":"R204.filtered_target_graph_curve_incidence_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_1D_boundary_and_intersection_lineage.rows[] | select(.exact_source_target_intersection == true)","ledger_sha256":null,"row_count":504,"row_hashes_sha256":"734e76aad1d6e6e3c71a94d52e3760f308d5254229d7fbaa45ade55ea8e3cc71","row_id_field":"edge_row_id","row_ids_sha256":"b1eb2b37951706889aec96208218605e8cf28bdc836e314a64b066a487072baa","row_schema_contract":{},"rows_sha256":"220aeb46880c96144592ce6f1789b20275c0e497916a60d5dbfb0f260283890a","source_exact_size":7157575,"source_sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"admitted_for_construction":true,"authority":"R204.filtered_target_graph_point_incidence_rows","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_0D_endpoint_and_corner_lineage.rows[] | select(.exact_source_target_intersection_endpoint == true)","ledger_sha256":null,"row_count":280,"row_hashes_sha256":"d4e18500ac0a0fa8733ac7347e69c27bf9e83cc965dd5142da9bad03c0077272","row_id_field":"point_row_id","row_ids_sha256":"7fc15d641a88eca6f347e8e6108dbae21fedbf043a72031e0e64fe433ac746cc","row_schema_contract":{},"rows_sha256":"c3b6b05c84bbeaa1f4787024803cfa46b5d9d93fc6b320df127e1967d9582127","source_exact_size":7157575,"source_sha256":"e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818"},{"admitted_for_construction":true,"authority":"R211.formal_1D_curve_incidence_owner_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_1D_curve_incidence_owner_ledger.rows[]","ledger_sha256":null,"row_count":20456,"row_hashes_sha256":"3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522","row_id_field":"curve_row_id","row_ids_sha256":"a9d68f724a257ae768657dff51767207277a9fff6eebd345d539434789b88270","row_schema_contract":{},"rows_sha256":"c604ff7fee7d12c7bb39f5f670848f673e1afa0a44b9fad75d829f264e8fbb71","source_exact_size":140690802,"source_sha256":"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"},{"admitted_for_construction":true,"authority":"R211.formal_0D_endpoint_incidence_owner_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_0D_endpoint_incidence_owner_ledger.rows[]","ledger_sha256":null,"row_count":40912,"row_hashes_sha256":"e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712","row_id_field":"endpoint_row_id","row_ids_sha256":"dd9b72a5e03904dcf649a54e5828aa1e3fa41aa6f453b88a32f7b2abd3005e39","row_schema_contract":{},"rows_sha256":"de9c48038c7da03671941bd713b9f393a4a5a5b89a0dc53f76bd418a8cd13ed8","source_exact_size":140690802,"source_sha256":"bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f"},{"admitted_for_construction":true,"authority":"R269.formal_direct_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_direct_side_signature_ledger.rows[]","ledger_sha256":null,"row_count":187128,"row_hashes_sha256":"bad6026508e3bcc0ef23e84638b4c4be76903bbabe5f1d041a759bac50f4c416","row_id_field":"signed_region_row_id","row_ids_sha256":"30d17682e40900b86780ba0c001c95fd81ec85a00df4d02d0281e1dc14291ec4","row_schema_contract":{},"rows_sha256":"992392cc52465cd5ea427e7776fc16fd889048553950b5338042581c14d98755","source_exact_size":319672585,"source_sha256":"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"},{"admitted_for_construction":true,"authority":"R269.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_failclosed_leaf_ledger.rows[]","ledger_sha256":null,"row_count":70420,"row_hashes_sha256":"467b5b1076dadcc264b9d2f60aeaf5290e1c9dec9a1e0119d706342ddff3b275","row_id_field":"failclosed_leaf_row_id","row_ids_sha256":"ebcc6fd540a72ea862ab0cdc4c6544f1a0920263d534d0c1554b54552bcfc5e9","row_schema_contract":{},"rows_sha256":"e76ea912adb01d0f82a7fc7779d4504577b40acca7ba1fba09ec94565120e109","source_exact_size":319672585,"source_sha256":"472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3"},{"admitted_for_construction":true,"authority":"R270.formal_direct_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_direct_side_signature_ledger.rows[]","ledger_sha256":null,"row_count":37712,"row_hashes_sha256":"04baca4f94ee7a95ba441e95974240d4de323e08713e183e9a543408792f1e84","row_id_field":"signed_region_row_id","row_ids_sha256":"da02199cd0fd960d6b9b635414c6261f92634a6e96373322ccb4805ffceb265a","row_schema_contract":{},"rows_sha256":"6f23d7d545ff8c3add454fe01da64d095f237222228c1dd382ca9b19420d746e","source_exact_size":56705100,"source_sha256":"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"},{"admitted_for_construction":true,"authority":"R270.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_failclosed_leaf_ledger.rows[]","ledger_sha256":null,"row_count":8,"row_hashes_sha256":"2766aff887de89b4389408585d01fbb7adbb6f9b24fbb3eeb6cef25f4daa291f","row_id_field":"failclosed_leaf_row_id","row_ids_sha256":"4ec77e44a85ed2e42f4560225f0c96363243921a6f2eae9ce63bbc3d373a2a03","row_schema_contract":{},"rows_sha256":"e4e3807c3fb2c53b18a02ec5edfd5891283d38e48d0b57bdabcf70a373435361","source_exact_size":56705100,"source_sha256":"72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea"},{"admitted_for_construction":true,"authority":"R271.formal_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_side_signature_ledger.rows[]","ledger_sha256":null,"row_count":70420,"row_hashes_sha256":"f8601678041dd7f79bc276b926ca565995e87d79075b5dd4210af18787ab6da0","row_id_field":"signed_region_row_id","row_ids_sha256":"b71b0d65e1b0511829856e2c5dc42b002a7fc1ad8b7afe4230bcf29b8c338901","row_schema_contract":{},"rows_sha256":"cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8","source_exact_size":112741715,"source_sha256":"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"},{"admitted_for_construction":true,"authority":"R271.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_failclosed_leaf_ledger.rows[]","ledger_sha256":null,"row_count":496,"row_hashes_sha256":"59b2500b739714c2799bdae507559c490cbf1a15693c9a3d3340ca31ae76a74e","row_id_field":"failclosed_leaf_row_id","row_ids_sha256":"327e884fb879227d171895bc7b87759aad2f6aa70102874850ceb536596510ef","row_schema_contract":{},"rows_sha256":"4820153f78f785914c33b3738885f136b987cf8c2d3b01b509692454d32d6491","source_exact_size":112741715,"source_sha256":"c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747"},{"admitted_for_construction":true,"authority":"R272.formal_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.formal_side_signature_ledger.rows[]","ledger_sha256":null,"row_count":720,"row_hashes_sha256":"4c41486591353204f59929f6f8288bbcfca09f7a1f767831ac376b0d878b4069","row_id_field":"signed_region_row_id","row_ids_sha256":"9fc1d777079646ddedab5f5a308bf08bccb5ec8088de2b1f5d168bf5cb8a3247","row_schema_contract":{},"rows_sha256":"f23f389e39a9715f67fa827026072db638aee34c6f1e539b5ec36bf225e075da","source_exact_size":1250159,"source_sha256":"16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2"},{"admitted_for_construction":true,"authority":"R279.canonical_atom_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":332016,"row_hashes_sha256":"52aed35a8b1b423da27c7b6f05bc6f6721398c606ebe7ec3239770ada9f8887f","row_id_field":"canonical_atom_id","row_ids_sha256":"a685a017d5ae1a4d735a84142b3a2f2c3ed1b3cd2be3c41ad3dca3297f0acbe3","row_schema_contract":{},"rows_sha256":"d2680baed100e4e1a236aa929999c7d93be5eeddabb2cc0660fca5e756882105","source_exact_size":112858007,"source_sha256":"283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe"},{"admitted_for_construction":false,"authority":"R279.formal_face_edge_witness_rows","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{"candidate_indices_sha256":"855b6fa614c281074513344934fa3cc3c044495f3dd752589c21d1f977bd7cfb"},"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":330724,"row_hashes_sha256":"29efd6ba3b9b1a04580cf2a2593496bd5c1ddabffdb0eab9eaea9f0ac2762b78","row_id_field":"formal_face_edge_witness_row_id","row_ids_sha256":"5ef215767717f96cab2f4efb29851f41f2efbe8f5aec1c63e4ddef486abe8e92","row_schema_contract":{},"rows_sha256":"bfcb9979545b6abb2e85d54e0200f4394b6e967dbb888e3bcda7ee726cdc6bf7","source_exact_size":92749868,"source_sha256":"bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695"},{"admitted_for_construction":true,"authority":"R288.atom_disposition_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":332016,"row_hashes_sha256":"30a167baab36fab7e3e37fd0014c35b9fd94b5491494d21c83dc39080e191f50","row_id_field":"Round288_atom_disposition_row_id","row_ids_sha256":"09a0039e5d9e82413c949823697c794fc65095c1f71d2e6c2f576df0699ec13b","row_schema_contract":{},"rows_sha256":"8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849","source_exact_size":134114861,"source_sha256":"6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a"},{"admitted_for_construction":true,"authority":"R288.existing_overlap_relation_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":36680,"row_hashes_sha256":"4ef685a10bbcea11132eff991224dff8a89c137759d1707330faa3aaa5fd2f59","row_id_field":"Round288_existing_overlap_relation_row_id","row_ids_sha256":"ee2af535c82a4c79042c0e0c55797fb35db22a74d618ee79b2ed4e2c4a25bca6","row_schema_contract":{},"rows_sha256":"8a93bc24e836f2aca8cf59869217851be8dbedb8c930b325549ded7e8098cb7e","source_exact_size":7237078,"source_sha256":"d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e"},{"admitted_for_construction":false,"authority":"R290.inner_support_rows","authority_role":"DIAGNOSTIC_ONLY","auxiliary_commitments":{},"filename":"cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[]","ledger_sha256":null,"row_count":21160,"row_hashes_sha256":"925b4c51ea0c6ee2142a4b4fdf4c20cedb351fb24044c953fa5faf3652cefc81","row_id_field":"Round290_inner_support_row_id","row_ids_sha256":"90364fbc92c8ec21100eba1d7ba5cb8ceeb616506f138dfdc21315e63709edb1","row_schema_contract":{"forbidden_as_normalized_full_support":true,"forbidden_as_outer_support_equivalence_certificate":true,"role":"DIAGNOSTIC_ONLY_INNER_WITNESS"},"rows_sha256":"3ab9344c1fa492d87eee4937d11659872ea848c6ff9bf02419c10ae77a0636cd","source_exact_size":9576526,"source_sha256":"9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025"},{"admitted_for_construction":true,"authority":"B1R0.predicate_source_cell_rows","authority_role":"SUPPORT_ROW_SOURCE","auxiliary_commitments":{},"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".predicate_source_cell_rows[]","ledger_sha256":"f473914afa7d9dab1598a3259be8a4ec2b08ab7992d7a7039cff8bde5f19512b","row_count":295340,"row_hashes_sha256":"33ce0c07cf6eeeb7e8d3d10129dad7652aec94e3d30d18d807499380b35f279d","row_id_field":"Round306B1R0_predicate_source_cell_row_id","row_ids_sha256":"b3fb242c0c130122b0e2e7e0c1e38f866f214e332aea93dc6ce03e705201fe9a","row_schema_contract":{},"rows_sha256":"b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246","source_exact_size":105989322,"source_sha256":"19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96"},{"admitted_for_construction":true,"authority":"B1R0.member_union_rows","authority_role":"IDENTITY_BINDING","auxiliary_commitments":{},"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".member_union_rows[]","ledger_sha256":"28c6e7944f440f9fee06f9ade150de2566a3aaa85b40c49d63e3721ec4a4c4c5","row_count":295336,"row_hashes_sha256":"d106b9e68817aa9504ec176be9c679f2e4fd29948c3614f7c109030a893f289f","row_id_field":"Round306B1R0_member_union_row_id","row_ids_sha256":"6c136186cd30608304293cc91185615ba6bec6418cb2c43a48ac833055c69bfe","row_schema_contract":{},"rows_sha256":"6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d","source_exact_size":123019951,"source_sha256":"4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7"},{"admitted_for_construction":false,"authority":"B1R0.gap_rows","authority_role":"PROOF_EVIDENCE","auxiliary_commitments":{},"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"],"json_path":".gap_rows[]","ledger_sha256":"6a61506040c6f48236d8f35ee393f3a1d08dc36dbbcfd5a6d58b9290ef1e8904","row_count":590676,"row_hashes_sha256":"713e8415b88299f6db95446574f160b864f99a93ef8b12b14c8176cd12904df7","row_id_field":"Round306B1R0_gap_row_id","row_ids_sha256":"98aca1023d164e131c4755b0f35c777f3a984c8ffac6b58aaf1640bddb2dfdba","row_schema_contract":{},"rows_sha256":"c6bc641ea84b5a25ed851b0d13cef3b8694fcf4224b59868e641a3339496cf3d","source_exact_size":108363350,"source_sha256":"c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56"},{"admitted_for_construction":true,"authority":"R275.strict_region_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.strict_region_ledger.rows[]","ledger_sha256":null,"row_count":5288,"row_hashes_sha256":"dcd6f565597f2ca5f60f767362a1907cfee6fc8b43affdb9bdae1c424fd5cbe5","row_id_field":"reverse_rechart_region_row_id","row_ids_sha256":"f4700e1b6e69ec15b6a7a13189d0b57c9eaa205b6791d944748ee1bd71d1d3bd","row_schema_contract":{},"rows_sha256":"f1fc71b904d3dd060173c48480c09f2c7960dee2ad51db935d4d80966e0b38b6","source_exact_size":35517526,"source_sha256":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"},{"admitted_for_construction":true,"authority":"R275.arrangement_region_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.arrangement_region_ledger.rows[]","ledger_sha256":null,"row_count":8500,"row_hashes_sha256":"936960229d026545d07fd5a5db1586499cb2812852b89af04e149410be004da9","row_id_field":"reverse_rechart_region_row_id","row_ids_sha256":"6826e35ff8d9e2bd7c75196dc602082817b4bebe5f0751334fa4a4bd2726060f","row_schema_contract":{},"rows_sha256":"6ef756cfb1d5b1f5226643142e77ba897b5dcac326edb301c5d2d01963470ba5","source_exact_size":35517526,"source_sha256":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"},{"admitted_for_construction":true,"authority":"R275.guard_closure_ledger","authority_role":"ANALYTIC_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".result.guard_closure_ledger.rows[]","ledger_sha256":null,"row_count":880,"row_hashes_sha256":"6c52c6225fee422e5c01bc6b87dc65ff6eb292818d8ec1dbc612ce0f754983c1","row_id_field":"reverse_rechart_guard_closure_row_id","row_ids_sha256":"49722a30fb6c78931b7d5b7ee19cb74e0f8a77ec1f67f3c41533dd417d92d06c","row_schema_contract":{},"rows_sha256":"fcf3671715938cf106e27a04a7677dbb12821dd64fb7c9b8ce615b42670d7dc8","source_exact_size":35517526,"source_sha256":"e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386"},{"admitted_for_construction":false,"authority":"R287.region_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".region_rows[]","ledger_sha256":null,"row_count":13788,"row_hashes_sha256":null,"row_id_field":"Round287_region_disposition_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"7d07e90c481b1c511ccce1d56df67f95140aa8d9b5cf5ea30b1d962ace5d8765","source_exact_size":7529109,"source_sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":false,"authority":"R287.refinement_cell_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".refinement_cell_rows[]","ledger_sha256":null,"row_count":7616,"row_hashes_sha256":null,"row_id_field":"Round287_refinement_cell_disposition_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"951e8d912a4bf9494c928fbbdc99663485c019cee79580df98f838e0157555c9","source_exact_size":7529109,"source_sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":false,"authority":"R287.valid_internal_physical_face_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".valid_internal_physical_face_rows[]","ledger_sha256":null,"row_count":648,"row_hashes_sha256":null,"row_id_field":"Round287_internal_physical_face_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"9a05d9a41aa0877a5066d2477e376706a7a5e296b71e7f2209e9825c25fca2b3","source_exact_size":7529109,"source_sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":false,"authority":"R287.potential_new_support_union_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".potential_new_support_union_rows[]","ledger_sha256":null,"row_count":10020,"row_hashes_sha256":null,"row_id_field":"Round287_potential_new_support_union_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"2185915efd9a8d52ab13a5edea05e0d4e711f1d5cfce1e3f43a7a183a9326800","source_exact_size":7529109,"source_sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":false,"authority":"R287.mutually_exclusive_outer_overlap_pair_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".mutually_exclusive_outer_overlap_pair_rows[]","ledger_sha256":null,"row_count":3488,"row_hashes_sha256":null,"row_id_field":"Round287_mutually_exclusive_outer_overlap_pair_row_id","row_ids_sha256":null,"row_schema_contract":{},"rows_sha256":"5477ecd5518ba0bb7f89f6ee3e1fcb55d82f4ee8f895d4f03136b8ccb71b3848","source_exact_size":7529109,"source_sha256":"29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a"},{"admitted_for_construction":false,"authority":"R292.complete_heterogeneous_probe_rows","authority_role":"OUTER_ENVELOPE_ONLY","auxiliary_commitments":{},"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"],"json_path":".rows[]","ledger_sha256":null,"row_count":22820,"row_hashes_sha256":null,"row_id_field":"NO_UNIFORM_ROW_ID__SEE_ROW_SCHEMA_CONTRACT","row_ids_sha256":null,"row_schema_contract":{"row_shapes":[{"row_count":1564,"row_id_field":"Round292_registry_overlap_row_id","selector":"has(Round292_registry_overlap_row_id)","shape":"REGISTRY_OVERLAP"},{"row_count":11852,"row_id_field":"Round292_R287_existing_overlap_refinement_cell_id","selector":"has(Round292_R287_existing_overlap_refinement_cell_id)","shape":"EXACT_REFINEMENT_CELL"},{"row_count":9404,"row_id_field":"Round292_refined_new_support_component_id","selector":"has(member_refinement_cell_ids)","shape":"REFINED_NEW_SUPPORT_COMPONENT"}],"uniform_row_id_field":null,"whole_table_stored_order_commitment_only":true},"rows_sha256":"556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055","source_exact_size":5544437,"source_sha256":"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"},{"admitted_for_construction":true,"authority":"R292.exact_refinement_cell_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{},"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[] | select(has(\\"Round292_R287_existing_overlap_refinement_cell_id\\"))","ledger_sha256":null,"row_count":11852,"row_hashes_sha256":"abae741fe7aef5d6aa4ede7ac188d66a6edb6052ffb2b3a4e7d3b89ffd572f0c","row_id_field":"Round292_R287_existing_overlap_refinement_cell_id","row_ids_sha256":"331a400d3ee35f70fd1ffd52137cdb80d601886f05b4fe6c1e45d9d653d73068","row_schema_contract":{},"rows_sha256":"77c674fa6c5a72ef085b0f36568d17fb10a10d4721fa5734d3b35ab0fe4eacf0","source_exact_size":5544437,"source_sha256":"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"},{"admitted_for_construction":true,"authority":"R292.refined_new_support_component_rows","authority_role":"CONSTRUCTION_LINEAGE","auxiliary_commitments":{"component_map_sha256":"1128b9b7e23be09390db715d06b73e0f71828aa396792c29c2b587b483046378"},"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"],"json_path":".rows[] | select(has(\\"member_refinement_cell_ids\\"))","ledger_sha256":null,"row_count":9404,"row_hashes_sha256":"597d18bff0717f82bd2cc6def5884b5b7055f87366b52c5c1c36dade2dbcb709","row_id_field":"Round292_refined_new_support_component_id","row_ids_sha256":"e5ff9eb634175c893c6422a961e1a32c0a7dfa290c967cd6846e641ce963d33f","row_schema_contract":{},"rows_sha256":"696d484a174f1e5a53a874c4bd5109f00824a8c9a4f090c225e7ab17a7005fc2","source_exact_size":5544437,"source_sha256":"8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab"}]'
AUTHORITY_ROLE_POLICY_ROWS_JSON = '[{"admitted_for_construction":true,"authority_role":"IDENTITY_BINDING","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"SUPPORT_ROW_SOURCE","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"ANALYTIC_LINEAGE","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"CONSTRUCTION_LINEAGE","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority_role":"PROOF_EVIDENCE","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority_role":"OUTER_ENVELOPE_ONLY","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority_role":"DIAGNOSTIC_ONLY","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]}]'
AUTHORITY_ROLE_CATALOG_JSON = '{"authority_files":[{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round179_source_g_residual_tube_arrangement_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"filename":"cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE","ANALYTIC_LINEAGE"],"filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE","ANALYTIC_LINEAGE"],"filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE","PROOF_EVIDENCE"],"filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE","PROOF_EVIDENCE"],"filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE"],"filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["ANALYTIC_LINEAGE"],"filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"]},{"admitted_for_construction":false,"authority_roles":["OUTER_ENVELOPE_ONLY"],"filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["EXISTENCE_OR_EQUIVALENCE_THEOREM","INNER_SUPPORT","NORMALIZED_FULL_SUPPORT"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":false,"authority_roles":["DIAGNOSTIC_ONLY"],"filename":"cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE"]},{"admitted_for_construction":true,"authority_roles":["CONSTRUCTION_LINEAGE","OUTER_ENVELOPE_ONLY"],"filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["EXISTENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT","INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":false,"authority_roles":["PROOF_EVIDENCE"],"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","MAXIMALITY_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT"]},{"admitted_for_construction":true,"authority_roles":["IDENTITY_BINDING"],"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","SUPPORT_GEOMETRY"]},{"admitted_for_construction":true,"authority_roles":["SUPPORT_ROW_SOURCE"],"filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz","forbidden_as":["FORMAL_B1A_OR_CM2_CREDIT","NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE"]}],"role_policies":[{"admitted_for_construction":true,"authority_role":"IDENTITY_BINDING","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"SUPPORT_ROW_SOURCE","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"ANALYTIC_LINEAGE","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority_role":"CONSTRUCTION_LINEAGE","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority_role":"PROOF_EVIDENCE","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority_role":"OUTER_ENVELOPE_ONLY","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority_role":"DIAGNOSTIC_ONLY","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]}],"table_authorities":[{"admitted_for_construction":true,"authority":"R182.collar_leaf_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.coordinate_corner_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.coordinate_edge_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.coordinate_face_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.formal_coordinate_adjacency_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.one_step_split_interface_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R220.rejected_exact_coordinate_coincidence_rows","authority_role":"PROOF_EVIDENCE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R220.resolved_child_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R232.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round232_source_g_depth6_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R234.root_summary_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R234.resolved_descendant_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R234.depth6_frontier_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R237.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round237_source_g_crossing_time_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R238.whole_origin_promotion_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round238_source_g_source_chart_seam_whole_origin_promotion_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_Round244_known_connectivity_block_carry_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_cross_parent_same_chart_bulk_edge_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_different_parent_candidate_reconciliation_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_occurrence_known_block_incidence_delta_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_post_Round244_key_frontier_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_post_Round244_occurrence_known_block_frontier_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R244.formal_resolved_bulk_component_ledger","authority_role":"PROOF_EVIDENCE","filename":"cm2_round244_source_g_cross_parent_same_chart_bulk_quotient_rebuild_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R235.single_endpoint_graph_partition_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R236.double_endpoint_partition_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R236.crossing_dependency_discharge_rows","authority_role":"PROOF_EVIDENCE","filename":"cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R242.formal_positive_2D_transition_sheet_patch_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round242_source_g_outgoing_graph_existence_stratum_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R245.formal_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R246.formal_new_whole_signature_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round246_source_g_whole_signature_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R247.formal_new_crossing_and_source_seam_retained_stratum_node_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round247_source_g_crossing_and_source_seam_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R248.formal_wall_positive_volume_bulk_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R248.formal_wall_half_open_sheet_owner_ledger","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R264.formal_endpoint_empty_branch_correction_disposition_ledger","authority_role":"IDENTITY_BINDING","filename":"cm2_round264_source_g_lower_dimensional_endpoint_correction_and_glue_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_valid_virtual_node_frontier_ledger","authority_role":"IDENTITY_BINDING","filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_component_member_frontier_ledger","authority_role":"IDENTITY_BINDING","filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1G0.graph_source_inventory_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1G0.graph_sheet_join_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1G0.graph_side_join_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1G0.r264_correction_disposition_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1G0.b0_member_backbinding_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"B1G0.gap_rows","authority_role":"PROOF_EVIDENCE","filename":"cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B0.member_support_source_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R294.occurrence_registry_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R294.representation_binding_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R266.formal_post_Round266_expanded_occurrence_frontier_ledger","authority_role":"IDENTITY_BINDING","filename":"cm2_round266_source_g_expanded_curved_face_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R174.resolved_3d_occurrence_rows","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R179.resolved_3d_child_rows","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round179_source_g_residual_tube_arrangement_rows.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R204.formal_local_open_3D_region_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R208.formal_local_open_3D_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R204.formal_2D_sheet_lineage.target_sheet_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R208.formal_direct_leaf_signature_base_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R208.formal_leaf_geometry_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R208.formal_final_factor_face_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R211.formal_2D_sheet_owner_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R204.filtered_target_graph_curve_incidence_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R204.filtered_target_graph_point_incidence_rows","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R211.formal_1D_curve_incidence_owner_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R211.formal_0D_endpoint_incidence_owner_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round211_source_g_outgoing_half_open_owner_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R269.formal_direct_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R269.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R270.formal_direct_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R270.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R271.formal_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R271.formal_failclosed_leaf_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R272.formal_side_signature_ledger","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R279.canonical_atom_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R279.formal_face_edge_witness_rows","authority_role":"PROOF_EVIDENCE","filename":"cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R288.atom_disposition_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R288.existing_overlap_relation_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_existing_overlap_relations.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R290.inner_support_rows","authority_role":"DIAGNOSTIC_ONLY","filename":"cm2_round290_source_g_isolated_atom_inner_support_closure_inner_support_ledger.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","OUTER_SUPPORT_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1R0.predicate_source_cell_rows","authority_role":"SUPPORT_ROW_SOURCE","filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_predicate_source_cell.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"B1R0.member_union_rows","authority_role":"IDENTITY_BINDING","filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_member_union.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT","SUPPORT_GEOMETRY","PHYSICAL_INCIDENCE_OR_EQUIVALENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"B1R0.gap_rows","authority_role":"PROOF_EVIDENCE","filename":"cm2_round306b1r0_source_g_r288_predicate_source_inventory_and_union_freeze_gap.json.gz","forbidden_as":["CONSTRUCTION_ROW_SOURCE","NORMALIZED_FULL_SUPPORT","MAXIMALITY_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R275.strict_region_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R275.arrangement_region_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R275.guard_closure_ledger","authority_role":"ANALYTIC_LINEAGE","filename":"cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json","forbidden_as":["PHYSICAL_SUPPORT_OR_GLUE_WITHOUT_EQUIVALENCE_CERTIFICATE","NORMALIZED_FULL_SUPPORT","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":false,"authority":"R287.region_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority":"R287.refinement_cell_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority":"R287.valid_internal_physical_face_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority":"R287.potential_new_support_union_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority":"R287.mutually_exclusive_outer_overlap_pair_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":false,"authority":"R292.complete_heterogeneous_probe_rows","authority_role":"OUTER_ENVELOPE_ONLY","filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["INNER_SUPPORT","NORMALIZED_FULL_SUPPORT","EXISTENCE_OR_EQUIVALENCE_THEOREM"]},{"admitted_for_construction":true,"authority":"R292.exact_refinement_cell_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]},{"admitted_for_construction":true,"authority":"R292.refined_new_support_component_rows","authority_role":"CONSTRUCTION_LINEAGE","filename":"cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz","forbidden_as":["NORMALIZED_FULL_SUPPORT_WITHOUT_TYPED_AST_AND_EQUIVALENCE_CERTIFICATE","PHYSICAL_INCIDENCE_THEOREM","FORMAL_B1A_OR_CM2_CREDIT"]}]}'
AUTHORITY_FILE_RECORDS: tuple[dict[str, Any], ...] = tuple(json.loads(AUTHORITY_FILE_RECORDS_JSON))
AUTHORITY_FILE_ROWS: tuple[dict[str, Any], ...] = tuple(json.loads(AUTHORITY_FILE_ROWS_JSON))
TABLE_AUTHORITIES: tuple[dict[str, Any], ...] = tuple(json.loads(TABLE_AUTHORITIES_JSON))
AUTHORITY_ROLE_POLICY_ROWS: tuple[dict[str, Any], ...] = tuple(json.loads(AUTHORITY_ROLE_POLICY_ROWS_JSON))
AUTHORITY_ROLE_CATALOG: dict[str, Any] = json.loads(AUTHORITY_ROLE_CATALOG_JSON)
EXPECTED_AUTHORITY_FILE_COUNT = 45
EXPECTED_AUTHORITY_FILE_BYTES = 4_665_362_689
EXPECTED_AUTHORITY_FILES_SHA256 = "13993a345ec98b14d84faf6db8d29c1f5e23dbfbc1ae47e44798adea931caa0a"
EXPECTED_TABLE_AUTHORITY_COUNT = 82
EXPECTED_TABLE_AUTHORITIES_SHA256 = "a49a38afbea65b5a8e837bc4932328447ad0ee553f18596cdff5ea788a879678"
EXPECTED_AUTHORITY_ROLE_CATALOG_SHA256 = "807e5502f5329577fc6f3c823bf835879c637f4b083fd417ff69e27cc3190117"

SIX_PARTITION_CENSUS = {
    "member_count": 564492,
    "partition_count": 6,
    "mutually_exclusive": True,
    "exhaustive": True,
    "partitions": [
        {"family": "preserved", "member_count": 126468},
        {"family": "R2", "member_count": 295336, "source_cell_count": 295340},
        {"family": "R292", "member_count": 9404},
        {"family": "G2a", "member_count": 38624},
        {
            "family": "G2b",
            "member_count": 76832,
            "source_reference_count": 76848,
        },
        {"family": "non_graph_bulk", "member_count": 17828},
    ],
}

FIELD_SCOPED_PRECEDENCE = (
    {
        "field_scope": "B0_member_identity_and_primary_source",
        "precedence": ["B0_MEMBER_SUPPORT_SOURCE_IDENTITY"],
    },
    {
        "field_scope": "occurrence_registry_identity",
        "precedence": [
            "R294_OCCURRENCE_REGISTRY_IDENTITY",
            "B0_MEMBER_SUPPORT_SOURCE_IDENTITY",
        ],
    },
    {
        "field_scope": "preserved_source_geometry",
        "precedence": [
            "PRESERVED_R174_RESOLVED_3D",
            "PRESERVED_R179_RESOLVED_3D_CHILD",
            "PRESERVED_R204_OPEN_3D_REGION",
            "PRESERVED_R208_OPEN_3D_SIGNATURE_REGION",
            "R266_PRESERVED_EXPANDED_IDENTITY",
            "R294_OCCURRENCE_REGISTRY_IDENTITY",
        ],
    },
    {
        "field_scope": "A1_root_and_sheet_definition",
        "precedence": [
            "A1_R204_TARGET_REGULAR_GRAPH_SHEET",
            "A1_R208_R211_FACTOR_SHEET_OWNER",
            "A1_R208_DIRECT_LEAF_SIGNATURE_BASE",
            "A1_R208_LEAF_GEOMETRY",
            "A1_R208_FINAL_FACTOR_FACE",
        ],
    },
    {
        "field_scope": "A2_physical_incidence_and_equivalence",
        "precedence": [
            "A2_R204_TARGET_GRAPH_CURVE_INCIDENCE",
            "A2_R204_TARGET_GRAPH_POINT_INCIDENCE",
            "A2_R208_R211_CURVE_INCIDENCE_OWNER",
            "A2_R208_R211_ENDPOINT_INCIDENCE_OWNER",
        ],
    },
    {
        "field_scope": "normalized_full_support_AST",
        "precedence": [],
        "status": "UNFROZEN",
    },
)

FORBIDDEN_AS_SUPPORT_EXCLUSIONS = (
    "AF2_PRIMITIVE_SOURCE_FAMILY_LABEL",
    "THEOREM_OBLIGATION_CENSUS",
    "OUTER_ENVELOPE",
    "INNER_WITNESS",
    "CARRIER_BOX",
    "SOURCE_HANDLE_WITHOUT_TYPED_SUPPORT_AST",
    "PREDICATE_CELL_WITHOUT_EQUIVALENCE_AND_FINITE_UNION_PROOF",
    "REPRESENTATION_WITHOUT_PULLBACK_CERTIFICATE",
    "OLD_C0_INERT_TRANSITION_PAIR_ROUTING_CONTRACT",
)

class ReplayBlocked(RuntimeError):
    """Fail-closed admission error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ReplayBlocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def is_basename(value: Any) -> bool:
    return (
        type(value) is str
        and value not in {"", ".", ".."}
        and os.path.basename(value) == value
        and "/" not in value
        and "\\" not in value
        and "\x00" not in value
    )


@dataclass(frozen=True)
class _PathLiteral:
    value: str

    @property
    def name(self) -> str:
        return os.path.basename(self.value)


class _UnknownStaticValue(Exception):
    pass


def _static_value(node: ast.AST, environment: Mapping[str, Any]) -> Any:
    """Evaluate only inert literals needed by the frozen pin grammar."""

    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (str, int, bool, type(None)))
    ):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in environment:
            raise _UnknownStaticValue(node.id)
        return environment[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(_static_value(item, environment) for item in node.elts)
    if isinstance(node, ast.List):
        return [_static_value(item, environment) for item in node.elts]
    if isinstance(node, ast.Set):
        return {_static_value(item, environment) for item in node.elts}
    if isinstance(node, ast.Dict):
        result: dict[Any, Any] = {}
        for key_node, value_node in zip(node.keys, node.values, strict=True):
            if key_node is None:
                update = _static_value(value_node, environment)
                if type(update) is not dict:
                    raise _UnknownStaticValue("non-dict unpack")
                result.update(update)
            else:
                result[_static_value(key_node, environment)] = _static_value(
                    value_node, environment
                )
        return result
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _static_value(node.left, environment) + _static_value(
            node.right, environment
        )
    if isinstance(node, ast.JoinedStr):
        pieces: list[str] = []
        for item in node.values:
            if isinstance(item, ast.Constant) and type(item.value) is str:
                pieces.append(item.value)
            elif (
                isinstance(item, ast.FormattedValue)
                and item.conversion == -1
                and item.format_spec is None
            ):
                pieces.append(str(_static_value(item.value, environment)))
            else:
                raise _UnknownStaticValue("non-literal JoinedStr")
        return "".join(pieces)
    if isinstance(node, ast.Subscript):
        return _static_value(node.value, environment)[
            _static_value(node.slice, environment)
        ]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        right = _static_value(node.right, environment)
        require(type(right) is str and is_basename(right), "unsafe static path join")
        try:
            left = _static_value(node.left, environment)
        except _UnknownStaticValue:
            left = _PathLiteral("")
        prefix = left.value if isinstance(left, _PathLiteral) else str(left)
        return _PathLiteral(os.path.join(prefix, right))
    if isinstance(node, ast.Attribute) and node.attr == "name":
        value = _static_value(node.value, environment)
        if not isinstance(value, _PathLiteral):
            raise _UnknownStaticValue(".name of non-path literal")
        return value.name
    # Calls (including Path/resolve), comprehensions, lambdas, imports, and
    # every other executable form are deliberately outside the grammar.
    raise _UnknownStaticValue(type(node).__name__)


def _first_file_sha(value: Any) -> str | None:
    if is_sha256(value):
        return value
    if type(value) in {tuple, list} and value and is_sha256(value[0]):
        return value[0]
    return None


def static_direct_pins(
    source: bytes, existing_names: set[str] | None = None
) -> dict[str, str]:
    """Extract direct file pins without compiling, importing, or executing."""

    require(b"\x00" not in source, "NUL in Python source")
    tree = ast.parse(source.decode("utf-8"), mode="exec")
    environment: dict[str, Any] = {}
    assignments: dict[str, Any] = {}
    # A bounded fixpoint admits harmless forward references without ever
    # compiling the source.  Every pass evaluates only the grammar above.
    for _ in range(max(1, len(tree.body) + 1)):
        changed = False
        for statement in tree.body:
            if isinstance(statement, ast.Assign):
                targets = statement.targets
                value_node = statement.value
            elif isinstance(statement, ast.AnnAssign):
                targets = [statement.target]
                value_node = statement.value
                if value_node is None:
                    continue
            else:
                continue
            if len(targets) != 1 or not isinstance(targets[0], ast.Name):
                continue
            try:
                value = _static_value(value_node, environment)
            except (KeyError, IndexError, TypeError, ValueError,
                    _UnknownStaticValue, ReplayBlocked):
                continue
            name = targets[0].id
            if name not in environment or environment[name] != value:
                environment[name] = value
                assignments[name] = value
                changed = True
        if not changed:
            break

    result: dict[str, str] = {}
    if "PINS" not in assignments:
        return result
    mapping = assignments["PINS"]
    require(type(mapping) is dict, "top-level PINS is not a dict")
    for filename, value in mapping.items():
        require(is_basename(filename), "non-basename PINS key")
        if existing_names is not None and filename not in existing_names:
            continue
        candidate = _first_file_sha(value)
        require(candidate is not None, "invalid PINS value:" + filename)
        prior = result.setdefault(filename, candidate)
        require(prior == candidate, "conflicting direct pin:" + filename)
    return result


def _fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_uid,
        info.st_gid,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _hash_fd(descriptor: int) -> str:
    state = hashlib.sha256()
    os.lseek(descriptor, 0, os.SEEK_SET)
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            break
        state.update(block)
    os.lseek(descriptor, 0, os.SEEK_SET)
    return state.hexdigest()


@dataclass
class _HeldFile:
    filename: str
    descriptor: int
    admitted_stat: os.stat_result
    expected_sha256: str
    source: bytes | None
    admitted_realpath: str


def _open_one(
    directory: Path,
    directory_fd: int,
    record: Mapping[str, Any],
    label: str,
) -> _HeldFile:
    filename = record.get("filename")
    expected_size = record.get("exact_size", record.get("size"))
    expected_sha256 = record.get("sha256")
    require(is_basename(filename), label + ":basename")
    require(type(expected_size) is int and expected_size >= 0, label + ":size")
    require(is_sha256(expected_sha256), label + ":sha256")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    require(hasattr(os, "O_NOFOLLOW"), "platform lacks O_NOFOLLOW")
    flags |= os.O_NOFOLLOW
    descriptor = os.open(filename, flags, dir_fd=directory_fd)
    try:
        before = os.fstat(descriptor)
        path_before = os.stat(
            filename, dir_fd=directory_fd, follow_symlinks=False
        )
        require(stat.S_ISREG(before.st_mode), label + ":regular")
        require(before.st_nlink == 1, label + ":nlink1")
        require(_fingerprint(before) == _fingerprint(path_before), label + ":fd/path")
        admitted_realpath = os.path.realpath(directory / filename)
        require(
            admitted_realpath == str(directory / filename),
            label + ":realpath",
        )
        require(before.st_size == expected_size, label + ":exact-size")
        observed_sha256 = _hash_fd(descriptor)
        after_hash = os.fstat(descriptor)
        require(_fingerprint(after_hash) == _fingerprint(before), label + ":stable-first-hash")
        require(observed_sha256 == expected_sha256, label + ":exact-sha256")
        source = None
        if filename.endswith(".py"):
            source = b""
            os.lseek(descriptor, 0, os.SEEK_SET)
            chunks: list[bytes] = []
            while True:
                block = os.read(descriptor, 1 << 20)
                if not block:
                    break
                chunks.append(block)
            source = b"".join(chunks)
            require(
                hashlib.sha256(source).hexdigest() == expected_sha256,
                label + ":captured-source-sha256",
            )
            require(len(source) == expected_size, label + ":captured-source-size")
            os.lseek(descriptor, 0, os.SEEK_SET)
        return _HeldFile(
            filename,
            descriptor,
            before,
            expected_sha256,
            source,
            admitted_realpath,
        )
    except Exception:
        os.close(descriptor)
        raise


def verify_held_catalog(
    directory: Path,
    records: Sequence[Mapping[str, Any]],
    *,
    phase_hook: Callable[[], None] | None = None,
) -> dict[str, bytes]:
    """Verify all bytes twice while every admitted descriptor remains held."""

    require(directory.is_absolute(), "catalog directory must be absolute")
    directory_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    require(hasattr(os, "O_DIRECTORY"), "platform lacks O_DIRECTORY")
    require(hasattr(os, "O_NOFOLLOW"), "platform lacks O_NOFOLLOW")
    directory_flags |= os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = os.open(directory, directory_flags)
    held: list[_HeldFile] = []
    try:
        directory_before = os.fstat(directory_fd)
        directory_path_before = os.stat(directory, follow_symlinks=False)
        directory_realpath_before = os.path.realpath(directory)
        require(directory_realpath_before == str(directory), "deliverables realpath")
        require(stat.S_ISDIR(directory_before.st_mode), "deliverables regular directory")
        require(
            _fingerprint(directory_before) == _fingerprint(directory_path_before),
            "deliverables fd/path admission",
        )
        seen: set[str] = set()
        for index, record in enumerate(records):
            filename = record.get("filename")
            require(filename not in seen, "duplicate catalog filename")
            seen.add(filename)
            held.append(
                _open_one(directory, directory_fd, record, f"catalog[{index}]")
            )
        if phase_hook is not None:
            phase_hook()
        for item in held:
            observed_sha256 = _hash_fd(item.descriptor)
            after = os.fstat(item.descriptor)
            path_after = os.stat(
                item.filename, dir_fd=directory_fd, follow_symlinks=False
            )
            require(
                observed_sha256 == item.expected_sha256,
                "same-fd rehash:" + item.filename,
            )
            require(
                _fingerprint(after) == _fingerprint(item.admitted_stat),
                "same-fd post-stat:" + item.filename,
            )
            require(
                _fingerprint(path_after) == _fingerprint(item.admitted_stat),
                "path replacement:" + item.filename,
            )
            require(
                os.path.realpath(directory / item.filename)
                == item.admitted_realpath,
                "realpath replacement:" + item.filename,
            )
        directory_after = os.fstat(directory_fd)
        directory_path_after = os.stat(directory, follow_symlinks=False)
        require(
            _fingerprint(directory_after) == _fingerprint(directory_before),
            "deliverables fd post-stat",
        )
        require(
            _fingerprint(directory_path_after) == _fingerprint(directory_before),
            "deliverables path replacement",
        )
        require(
            os.path.realpath(directory) == directory_realpath_before,
            "deliverables realpath replacement",
        )
        return {
            item.filename: item.source
            for item in held
            if item.source is not None
        }
    finally:
        for item in held:
            os.close(item.descriptor)
        os.close(directory_fd)


def _ordered_catalog_records(
    records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    normalized = [
        {
            "filename": record["filename"],
            "exact_size": record["exact_size"],
            "sha256": record["sha256"],
            "root_source": record["root_source"],
        }
        for record in records
    ]
    normalized.sort(key=lambda record: record["filename"])
    return normalized


def _validate_frozen_catalog() -> None:
    require(len(ROOT_FILENAMES) == EXPECTED_ROOT_COUNT, "root filename census")
    require(len(set(ROOT_FILENAMES)) == len(ROOT_FILENAMES), "unique roots")
    records = _ordered_catalog_records(CLOSURE_RECORDS)
    require(len(records) == EXPECTED_CLOSURE_FILE_COUNT, "closure file census")
    require(
        sum(record["exact_size"] for record in records)
        == EXPECTED_CLOSURE_TOTAL_BYTES,
        "closure byte census",
    )
    require(digest(records) == EXPECTED_INVENTORY_SHA256, "closure inventory digest")
    require(
        tuple(
            record["filename"]
            for record in _ordered_catalog_records(ROOT_RECORDS)
        )
        == tuple(sorted(ROOT_FILENAMES)),
        "root record identity",
    )


def _inventory_domain(
    records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    normalized = _ordered_catalog_records(records)
    return {
        "count": len(normalized),
        "file_count": len(normalized),
        "total_bytes": sum(row["exact_size"] for row in normalized),
        "records": normalized,
        "records_sha256": digest(normalized),
        "inventory_rows_sha256": digest(normalized),
    }


def _governance_domain() -> dict[str, Any]:
    records = [
        {
            "label": row["label"],
            "filename": row["filename"],
            "size": row["size"],
            "sha256": row["sha256"],
        }
        for row in GOVERNANCE_SEALS
    ]
    records.sort(
        key=lambda row: (
            row["label"], row["filename"], row["size"], row["sha256"]
        )
    )
    return {
        "count": len(records),
        "total_bytes": sum(row["size"] for row in records),
        "records": records,
        "records_sha256": digest(records),
    }


def _merge_file_domains(
    domains: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    """Deduplicate file pins while preserving and checking domain membership."""

    merged: dict[str, dict[str, Any]] = {}
    memberships: dict[str, set[str]] = {}
    for domain, records in domains.items():
        require(is_basename(domain), "domain label")
        for record in records:
            filename = record.get("filename")
            size = record.get("exact_size", record.get("size"))
            sha256 = record.get("sha256")
            require(is_basename(filename), domain + ":filename")
            require(type(size) is int and size >= 0, domain + ":size")
            require(is_sha256(sha256), domain + ":sha256")
            normalized = {
                "filename": filename,
                "size": size,
                "sha256": sha256,
            }
            if filename in merged:
                require(
                    merged[filename] == normalized,
                    "cross-domain file pin conflict:" + filename,
                )
            else:
                merged[filename] = normalized
            memberships.setdefault(filename, set()).add(domain)
    result = []
    for filename in sorted(merged):
        result.append(
            {
                **merged[filename],
                "domains": sorted(memberships[filename]),
            }
        )
    return result


def _reconstruct_edges(sources: Mapping[str, bytes]) -> list[dict[str, str]]:
    catalog = {row["filename"]: row for row in CLOSURE_RECORDS}
    known: dict[str, str] = {
        row["filename"]: row["sha256"] for row in ROOT_RECORDS
    }
    queue = sorted(name for name in known if name.endswith(".py"))
    scanned: set[str] = set()
    edges: set[tuple[str, str, str]] = set()
    while queue:
        parent = queue.pop(0)
        if parent in scanned:
            continue
        scanned.add(parent)
        source = sources.get(parent)
        require(type(source) is bytes, "held Python source:" + parent)
        for child, sha256 in sorted(static_direct_pins(source).items()):
            require(child in catalog, "PINS child outside frozen catalog:" + child)
            require(
                catalog[child]["sha256"] == sha256,
                "PINS/catalog conflict:" + child,
            )
            edges.add((parent, child, sha256))
            prior = known.setdefault(child, sha256)
            require(prior == sha256, "transitive pin conflict:" + child)
            if child.endswith(".py") and child not in scanned:
                queue.append(child)
        queue.sort()
    require(set(known) == set(catalog), "exact-PINS closure identity")
    result = [
        {"parent": parent, "child": child, "sha256": sha256}
        for parent, child, sha256 in sorted(edges)
    ]
    require(len(result) == EXPECTED_EDGE_COUNT, "direct edge census")
    require(digest(result) == EXPECTED_EDGES_SHA256, "direct edge digest")
    return result


def _validate_authority_constants() -> None:
    table_rows = [dict(row) for row in TABLE_AUTHORITIES]
    require(
        len(table_rows) == EXPECTED_TABLE_AUTHORITY_COUNT,
        "table authority census",
    )
    require(
        digest(table_rows) == EXPECTED_TABLE_AUTHORITIES_SHA256,
        "table authority digest",
    )
    authority_records = [dict(row) for row in AUTHORITY_FILE_RECORDS]
    authority_records.sort(key=lambda row: row["filename"])
    require(
        len(authority_records) == EXPECTED_AUTHORITY_FILE_COUNT,
        "authority file census",
    )
    require(
        sum(row["exact_size"] for row in authority_records)
        == EXPECTED_AUTHORITY_FILE_BYTES,
        "authority file bytes",
    )
    require(
        digest(authority_records) == EXPECTED_AUTHORITY_FILES_SHA256,
        "authority file digest",
    )
    authority_file_rows = [dict(row) for row in AUTHORITY_FILE_ROWS]
    authority_file_rows.sort(key=lambda row: row["filename"])
    require(
        [
            {
                "filename": row["filename"],
                "exact_size": row["exact_size"],
                "sha256": row["sha256"],
            }
            for row in authority_file_rows
        ]
        == authority_records,
        "authority file role-row projection",
    )
    require(
        list(AUTHORITY_ROLE_CATALOG["role_policies"])
        == list(AUTHORITY_ROLE_POLICY_ROWS),
        "authority role policy projection",
    )
    require(
        digest(AUTHORITY_ROLE_CATALOG)
        == EXPECTED_AUTHORITY_ROLE_CATALOG_SHA256,
        "authority role catalog digest",
    )
    require(
        AUTHORITY_ROLE_CATALOG["authority_files"]
        == [
            {
                key: row[key]
                for key in (
                    "filename",
                    "authority_roles",
                    "admitted_for_construction",
                    "forbidden_as",
                )
            }
            for row in authority_file_rows
        ],
        "authority file role catalog projection",
    )
    require(
        AUTHORITY_ROLE_CATALOG["table_authorities"]
        == [
            {
                key: row[key]
                for key in (
                    "authority",
                    "filename",
                    "authority_role",
                    "admitted_for_construction",
                    "forbidden_as",
                )
            }
            for row in table_rows
        ],
        "table role catalog projection",
    )
    closure = {row["filename"]: row for row in CLOSURE_RECORDS}
    authority = {row["filename"]: row for row in authority_records}
    require(len(authority) == len(authority_records), "unique authority files")
    for row in authority_records:
        frozen = closure.get(row["filename"])
        if frozen is not None:
            require(
                frozen["exact_size"] == row["exact_size"]
                and frozen["sha256"] == row["sha256"],
                "authority/closure identity:" + row["filename"],
            )
    require(
        {row["filename"] for row in table_rows} == set(authority),
        "every table file exactly pinned",
    )
    for row in table_rows:
        require(
            row["filename"] in authority,
            "table lacks authority file pin:" + row["authority"],
        )
        pinned = authority[row["filename"]]
        require(
            row["source_exact_size"] == pinned["exact_size"]
            and row["source_sha256"] == pinned["sha256"],
            "table source identity:" + row["authority"],
        )


def _result_from_sources(sources: Mapping[str, bytes]) -> dict[str, Any]:
    inventory = _inventory_domain(CLOSURE_RECORDS)
    root_domain = _inventory_domain(ROOT_RECORDS)
    edge_records = _reconstruct_edges(sources)
    table_rows = [dict(row) for row in TABLE_AUTHORITIES]
    return {
        "schema": SCHEMA,
        "status": "ZERO_FULL_SUPPORT_CREDIT",
        "direct_root_count": EXPECTED_ROOT_COUNT,
        "transitive_file_count": EXPECTED_CLOSURE_FILE_COUNT,
        "transitive_file_bytes": EXPECTED_CLOSURE_TOTAL_BYTES,
        "inventory_rows_sha256": EXPECTED_INVENTORY_SHA256,
        "algorithm": {
            "closure_domain": (
                "ROOTS_UNION_RECURSIVE_EXACT_TOP_LEVEL_PINS_KEYS_"
                "ALL_FILE_TYPES"
            ),
            "direct_edges_only": True,
            "expected_closure_file_count": EXPECTED_CLOSURE_FILE_COUNT,
            "static_ast_parse_only": True,
            "safe_literal_nodes": [
                "Constant",
                "Name",
                "List",
                "Tuple",
                "Set",
                "Dict",
                "string_Add",
                "JoinedStr",
                "Subscript",
                "Attribute.name",
                "lexical_Path_Div",
            ],
            "rejected_executable_nodes": [
                "Call",
                "Comprehension",
                "Lambda",
                "Starred",
                "ImportExecution",
                "compile",
                "eval",
                "exec",
            ],
            "tuple_or_list_pin_value": "FIRST_64HEX_IS_FILE_SHA256",
            "mapping_domains": "EXACT_TOP_LEVEL_VARIABLE_NAMED_PINS_ONLY",
            "ignored_mapping_names": [
                "SOURCE_PINS",
                "INPUT_PINS",
                "BYTE_PINS",
                "DIRECT_FILE_PINS",
                "DEPENDENCIES",
                "UPSTREAM_PINS",
                "BASELINE_PINS",
            ],
            "catalog_key_domain": "ALL_EXISTING_BASENAME_FILE_TYPES",
            "recursive_key_domain": "PY_SUFFIX_ONLY",
            "upstream_import_count": 0,
            "upstream_exec_count": 0,
            "upstream_compile_count": 0,
            "B1A_or_B2_heavy_run": False,
        },
        "root_producers": root_domain,
        "closure": {
            **inventory,
            "python_file_count": sum(
                row["filename"].endswith(".py")
                for row in inventory["records"]
            ),
            "edges": edge_records,
            "edges_sha256": digest(edge_records),
            "conflict_count": 0,
            "static_ast_parse_only": True,
        },
        "governance_seals": _governance_domain(),
        "authority_contract": {
            "schema": "cm2.round306b1af3.authority-frontier.v1",
            "six_partition_census": SIX_PARTITION_CENSUS,
            "authority_file_count": EXPECTED_AUTHORITY_FILE_COUNT,
            "authority_file_bytes": EXPECTED_AUTHORITY_FILE_BYTES,
            "authority_file_catalog_sha256": EXPECTED_AUTHORITY_FILES_SHA256,
            "authority_files": [dict(row) for row in AUTHORITY_FILE_ROWS],
            "authority_role_policies": [
                dict(row) for row in AUTHORITY_ROLE_POLICY_ROWS
            ],
            "authority_role_catalog_sha256": (
                EXPECTED_AUTHORITY_ROLE_CATALOG_SHA256
            ),
            "table_authority_count": len(table_rows),
            "table_authorities": table_rows,
            "table_authority_catalog_sha256": digest(table_rows),
            "field_scoped_precedence": list(FIELD_SCOPED_PRECEDENCE),
            "field_scoped_precedence_sha256": digest(
                list(FIELD_SCOPED_PRECEDENCE)
            ),
            "forbidden_as_support_exclusions": list(
                FORBIDDEN_AS_SUPPORT_EXCLUSIONS
            ),
            "analytic_AST_frozen": False,
            "typed_support_AST_frozen": False,
            "certificate_grammar_frozen": False,
            "member_representation_schema_frozen": False,
            "transition_ready_handles_frozen": False,
            "formal_B1A": False,
            "theorem_obligation_census_is_final_feature_ledger_count": False,
            "theorem_obligation_census": 824864,
        },
        "formal_credit": {
            "normalized_full_support_members": 0,
            "normalized_full_support_denominator": 564492,
            "representation_cover": 0,
            "representation_cover_denominator": 611904,
            "formal_B1A": False,
            "transition_atlas_families": 0,
            "transition_atlas_denominator": 20,
            "known_edge_geometry_first_rediscovery": 0,
            "known_edge_geometry_first_denominator": 478718,
            "pair_routing": 0,
            "pair_routing_denominator": 158838084354,
            "component_maximality_credit": 0,
            "official_fibre_credit": 0,
            "source_G_disposition_credit": 0,
            "D02": "BLOCKED",
            "D03": "NOT_REACHED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "safety": {
            "read_only": True,
            "candidate_files_written": 0,
            "filesystem_write_calls": 0,
            "held_fd_SHA256": True,
            "two_pass_same_fd_SHA256": True,
            "all_domain_fds_held_until_global_reaudit": True,
            "O_NOFOLLOW": True,
            "regular_file_required": True,
            "nlink_one_required": True,
            "pre_post_fstat_required": True,
            "same_fd_hash_required": True,
            "path_lstat_realpath_inode_replacement_fail_close": True,
            "directory_fd_held_and_reaudited": True,
            "TOCTOU_fail_close": True,
        },
    }


def _self_test() -> dict[str, Any]:
    _validate_frozen_catalog()
    _validate_authority_constants()
    require(canonical({"b": 1, "a": 2}) == b'{"a":2,"b":1}', "canonical JSON")
    static_source = (
        b"A='fixture.py'\n"
        b"PINS={A:('" + b"0" * 64 + b"','not-file-hash')}\n"
        b"BYTE_PINS={'ignored.py':'" + b"1" * 64 + b"'}\n"
    )
    require(
        static_direct_pins(static_source, {"fixture.py"})
        == {"fixture.py": "0" * 64},
        "static pin fixture",
    )
    builder = "cm2_round292_source_g_occurrence_registry_candidate_construction.py"
    require(builder not in ROOT_FILENAMES, "builder outside roots")
    require(
        builder not in {row["filename"] for row in CLOSURE_RECORDS},
        "builder outside exact-PINS closure",
    )
    merged = _merge_file_domains(
        {
            "one": [{"filename": "x", "size": 1, "sha256": "0" * 64}],
            "two": [
                {"filename": "x", "exact_size": 1, "sha256": "0" * 64}
            ],
        }
    )
    require(
        merged == [
            {
                "filename": "x",
                "size": 1,
                "sha256": "0" * 64,
                "domains": ["one", "two"],
            }
        ],
        "cross-domain identical pin merge",
    )
    full_domain = _merge_file_domains(
        {
            "closure": CLOSURE_RECORDS,
            "governance": GOVERNANCE_SEALS,
            "authority": AUTHORITY_FILE_RECORDS,
        }
    )
    require(len(full_domain) == 179, "unique held file census")
    require(
        sum(row["size"] for row in full_domain) == 4_881_101_972,
        "unique held byte census",
    )
    with tempfile.TemporaryDirectory(prefix="cm2-af3-independent-") as temporary:
        root = Path(temporary).resolve()
        fixture = root / "fixture.bin"
        fixture.write_bytes(b"held-fd-fixture")
        payload = fixture.read_bytes()
        record = {
            "filename": fixture.name,
            "size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        verify_held_catalog(root, [record])

        replacement_rejected = False
        def replace_path() -> None:
            staged = root / "replacement.bin"
            staged.write_bytes(payload)
            os.replace(staged, fixture)
        try:
            verify_held_catalog(root, [record], phase_hook=replace_path)
        except ReplayBlocked:
            replacement_rejected = True
        require(replacement_rejected, "path replacement attack rejected")

        symlink_rejected = False
        fixture.unlink()
        target = root / "target.bin"
        target.write_bytes(payload)
        fixture.symlink_to(target.name)
        try:
            verify_held_catalog(root, [record])
        except (OSError, ReplayBlocked):
            symlink_rejected = True
        require(symlink_rejected, "symlink attack rejected")

        fixture.unlink()
        target.unlink()
        target.write_bytes(payload)
        os.link(target, fixture)
        hardlink_rejected = False
        try:
            verify_held_catalog(root, [record])
        except ReplayBlocked:
            hardlink_rejected = True
        require(hardlink_rejected, "hardlink attack rejected")

    return {
        "schema": "cm2.round306b1af3.source-g-full-support-construction-source-authority-frontier.independent-self-test.v1",
        "status": "PASS",
        "static_ast_parse_only": True,
        "producer_imported_or_executed": False,
        "filesystem_attacks_rejected": 3,
    }


def replay_result() -> dict[str, Any]:
    _validate_frozen_catalog()
    _validate_authority_constants()
    merged_records = _merge_file_domains(
        {
            "closure": CLOSURE_RECORDS,
            "governance": GOVERNANCE_SEALS,
            "authority": AUTHORITY_FILE_RECORDS,
        }
    )
    sources = verify_held_catalog(
        DELIVERABLES,
        merged_records,
    )
    return _result_from_sources(sources)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--print-result", action="store_true")
    action.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.self_test:
        result = _self_test()
        print("SELF_TEST_PASS " + digest(result))
        return 0
    if arguments.print_result:
        sys.stdout.buffer.write(canonical(replay_result()) + b"\n")
        return 0
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
