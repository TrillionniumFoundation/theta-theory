#!/usr/bin/env python3
"""C79g v16r2 build-only producer source template.

This is an inert semantic-regeneration template.  It intentionally cannot
build, verify, assemble, authorize, reject, publish, or write runtime state.
Executable source must be regenerated and independently reviewed after the
full active transition/pin graph is closed.
"""
from __future__ import annotations

RUNTIME_AUTHORIZED = False
FINAL_BASE7_PINS_INSTALLED = False
FORMAL_GLOBAL_CLOSURE_CREDIT = 0
D02_UNLOCK = False
ACTIVE_SUCCESSOR_NAMESPACE = 'v16r2-semantic-regeneration'
ACTIVE_PREDECESSOR_SUPERSESSION = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json'
ACTIVE_SCHEMA = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2.json'
ACTIVE_CONTRACT = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2.json'
ACTIVE_PRODUCER = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2.py'
ACTIVE_CONSUMER = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2.py'
ACTIVE_TRANSITION = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_to_v16r2_static_launch_transition_receipt_v1.json'
ACTIVE_AUDIT = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2.json'
ACTIVE_LAUNCHER = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2.py'
ACTIVE_MANIFEST = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2.sha256'
ACTIVE_OUTER = 'deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2.json'
ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION
SOURCE_TEMPLATE_METADATA = {
  "D02_unlock": false,
  "active_successor_paths": {
    "audit": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_static_audit_v16r2.json",
    "candidate_a": ".cm2-runtime/c79g-v16r2-candidate-a-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    "candidate_b": ".cm2-runtime/c79g-v16r2-candidate-b-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    "consumer": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2.py",
    "contract": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_contract_v16r2.json",
    "launcher": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_v16r2.py",
    "manifest": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_manifest_v16r2.sha256",
    "outer": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2.json",
    "predecessor_supersession": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json",
    "producer": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2.py",
    "rejection": ".cm2-runtime/c79g-v16r2-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b/rejection.json",
    "rejection_ns": ".cm2-runtime/c79g-v16r2-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    "schema": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_schema_v16r2.json",
    "transition": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "verification_a": ".cm2-runtime/c79g-v16r2-verification-a-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b",
    "verification_b": ".cm2-runtime/c79g-v16r2-verification-b-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
  },
  "formal_global_closure_credit": 0,
  "manifest_or_outer_created": false,
  "origin_v15_ast_node_count": 58900,
  "origin_v15_file_bytes": 503176,
  "origin_v15_file_sha256": "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
  "positive_runtime_surface_created": false,
  "role": "producer",
  "runtime_authorized": false,
  "template_status": "INERT_SOURCE_TEMPLATE__RUNTIME_NOT_AUTHORIZED",
  "v16_semantic_rejection_file_sha256": "6513121e6aeb17f8adf7ee09a77c266152572698f50296a4e44e216adb71c7bd",
  "v16_semantic_rejection_object_sha256": "93032ecbeaf76b3c669bc7ef7f1e565f35fc774bc575de09bbfc3bb152baf172",
  "v16_semantic_rejection_path": ".cm2-runtime/c79g-v16-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b/rejection.json",
  "v16_semantic_supersession_file_sha256": "4b05c7dcd7303311fed7b51ea878641e006e707b5fe413f2aefbc3146afddb3c",
  "v16_semantic_supersession_object_sha256": "430c663c5ccababd932246d9bc87ecc08fa9957113792aa2bd1e10e205a2ff7c",
  "v16_semantic_supersession_path": "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16_semantic_rejection_supersession_receipt_v1.json"
}

def fail_closed() -> None:
    raise RuntimeError(
        "C79G_V16R2_SOURCE_TEMPLATE_ONLY__RUNTIME_NOT_AUTHORIZED__"
        "SEMANTIC_REVIEW_AND_COLD_FREEZE_REQUIRED"
    )

def main() -> int:
    fail_closed()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
