#!/usr/bin/env python3
"""Round-73 shared base-R1 quotient certificate producer."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from typing import Any
from cm2_round68_common import canonical_bytes,digest,require,sha256_path,strict_json_path
HERE=Path(__file__).resolve().parent
PROOF=HERE/'cm2-round73-base-r1-quotient-vertices-2026-07-21.json'
ROUND72=HERE/'cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json'
MANIFEST=HERE/'cm2-round73-base-r1-shared-quotient-manifest-2026-07-21.json'
VERIFIER=HERE/'cm2_round73_base_r1_shared_quotient_verifier.py'
SCHEMA='cm2.round73.base-r1-shared-quotient.v1'
def build()->dict[str,Any]:
 proof=strict_json_path(PROOF); previous=strict_json_path(ROUND72); q=proof['result']
 require(q['quotient_vertices']==144 and q['quotient_edges']==160 and q['quotient_two_cells']==40,'quotient f-vector')
 require(q['quotient_vertices']-q['quotient_edges']+q['quotient_two_cells']==q['connected_components']==24,'Euler')
 require(len(q['rows'])==16 and all(len(r['endpoint_vertices'])==2 for r in q['rows']),'cell rows')
 require(all(r['pullback_intersection_vertex']['krawczyk_strict_interior'] for r in q['rows']),'Krawczyk')
 numeric=previous['result']['numeric_local_field_registry']
 f10=numeric['F10_integer_sum']
 f13=numeric['F13_32_face_current_variation_strict_upper']
 f16=numeric['F16_32_face_flux_cost_strict_upper']
 result={
  'scope':'s=0 depth-1 union of 24 disjoint physical core rectangles',
  'quotient':{k:q[k] for k in ('stationary_face_instances_before_subdivision','stationary_faces_split_once','stationary_segments_after_subdivision','pullback_face_components','quotient_vertices','quotient_edges','quotient_two_cells','survival_cells','positive_return_cells','connected_components','euler_identity','rows_sha256')},
  'incidence':{
   'positive_cell_combinatorial_type':'curvilinear_quadrilateral',
   'positive_cell_boundary_slots':'1 original core corner + 2 stationary/pullback endpoints + 1 pullback/pullback vertex',
   'endpoint_vertices_certified':'32/32 by 90-step sign bisection',
   'interior_vertices_certified':'16/16 by strict Krawczyk inclusion',
   'stationary_face_subdivision':'32 faces split exactly once; remaining 64 stationary faces unsplit',
   'cellular_boundary_identity':'partial_1 partial_2 = 0 on the finite quotient',
   'internal_trace_cancellation':'all 32 pullback edges cancel pairwise in the oriented sum of all 40 two-cells',
  },
  'base_fibre_field_attachment':{
   'F10_integer_sum_on_32_pullbacks':f10,
   'F13_current_variation_sum_strict_upper':f13,
   'F16_Piola_flux_sum_strict_upper':f16,
   'oriented_quotient_duplicate_trace_multiplier':0,
   'exterior_stationary_boundary_segments':96,
  },
  'F14_F15_F17_attack':{
   'F14':'NOT_CERTIFIED__BASE_FIBRE_F10_480_AVAILABLE_BUT_RECOVERED_STRONG_BLOCK_ABSENT',
   'F15':'NOT_CERTIFIED__FINITE_QUOTIENT_AVAILABLE_BUT_RAW_ORLICZ_RECOVERY_AND_POSITIVE_CEMETERY_ABSENT',
   'F17_boundary_sector':'CERTIFIED_BASE_FIBRE__INTERNAL_PULLBACK_TRACES_CANCEL_BEFORE_TV',
   'F17_bulk_sector':'NOT_CERTIFIED__NO_ALL_INPUT_ANISOTROPIC_CURRENT_RECIPIENT_OR_SUFFIX_BOUND',
   'F17_official':'NOT_CERTIFIED',
   'F18':'NOT_CERTIFIED__NO_SINGLE_ALL_DEPTH_18_FIELD_BLOCK',
  },
  'strict_frontier':{
   'shared_96_stationary_plus_32_pullback_face_subdivision_incidence_quotient':'CERTIFIED_BASE_FIBRE',
   'depth2_finite_rank_atlas':'NOT_CERTIFIED',
   'arbitrary_depth_Rn_face_atlas':'NOT_CERTIFIED',
   'limiting_rank_path_weighted_sum':'NOT_CERTIFIED',
   'Gate5':'NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0',
   'complete_composite_gates':'0/5','CM2':'NO-GO_FOR_CLAIM'
  }
 }
 return {'schema':SCHEMA,'pins':{PROOF.name:sha256_path(PROOF),ROUND72.name:sha256_path(ROUND72)},'result':result,'result_sha256':digest(result)}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--manifest-json',action='store_true');p.add_argument('--verifier');a=p.parse_args();doc=build()
 if a.manifest_json:sys.stdout.buffer.write(canonical_bytes(doc));return 0
 print(json.dumps(doc,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
