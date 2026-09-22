from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parent
log = (ROOT / "geometry.log").read_text(encoding="utf-8", errors="replace")
pdf = ROOT / "geometry.pdf"
statement = (ROOT / "parts/01b-boundary-atlas.tex").read_text(encoding="utf-8")
proof = (ROOT / "parts/09b-boundary-atlas-proofs.tex").read_text(encoding="utf-8")
relative = (ROOT / "parts/09c-relative-primary-specialization.tex").read_text(encoding="utf-8")
driver = (ROOT / "geometry.tex").read_text(encoding="utf-8")
generic = ROOT / "evidence/GENERIC_BOUNDARY_CERTIFICATES.json"
boundary = ROOT / "evidence/BOUNDARY_ATLAS_CERTIFICATES.json"

checks = {
    "pdf_exists": pdf.exists() and pdf.stat().st_size > 100_000,
    "no_undefined_references": "undefined references" not in log.lower(),
    "no_undefined_citations": "undefined citations" not in log.lower(),
    "no_latex_error": "! LaTeX Error" not in log,
    "self_contained_source_tree": "../v12" not in driver,
    "bounded_principal_colon_theorem_present":
        "Bounded principal-colon primary stratification" in statement,
    "two_short_exact_sequence_repair_present":
        "0\\longrightarrow I_q" in relative and
        "0\\longrightarrow K_q" in relative and
        "flatness of the final cokernel" in relative,
    "constructible_assassin_reference_present": "Tag 05KR" in relative,
    "corank4_invariant_projection_present":
        "Equivariance of the corank-four residual ideal" in proof and
        "completely reducible" in proof,
    "generic_rankdrop_factor_proof_present":
        "9s^2+64s+288" in relative and "161" in relative,
}

if boundary.exists():
    data = json.loads(boundary.read_text(encoding="utf-8"))
    checks["boundary_exact_regressions"] = bool(
        data.get("wedge6_sym2_GL4_decomposition")
        and data.get("corank3_GL3_character_identities")
        and data.get("b0_exact_delta_cubed")
    )
else:
    checks["boundary_exact_regressions"] = False

if generic.exists():
    data = json.loads(generic.read_text(encoding="utf-8"))
    sat = data.get("generic_embedded_saturation", {}).get("a1_b3_W3", {})
    fac = data.get("generic_rank_one_factors", {})
    checks["generic_slice_exact_regressions"] = bool(
        len(data.get("mixed_kernel_generic_slices", [])) == 7
        and len(data.get("rankdrop_generic_slices", [])) == 9
        and fac.get("a2_b2_W2", {}).get("quadratic_discriminant")
        and fac.get("a1_b3_W3", {}).get("discriminant") == "161"
        and sat.get("embedded_vertex_length") == 3
        and data.get("pieri_horizontal_strip_combinatorics_only") is True
    )
else:
    checks["generic_slice_exact_regressions"] = False

if pdf.exists():
    doc = fitz.open(pdf)
    checks["pdf_pages"] = len(doc)
    checks["pdf_page_floor"] = len(doc) >= 40
else:
    checks["pdf_pages"] = 0
    checks["pdf_page_floor"] = False

evidence_scope = {
    "script_executed": [
        "exact_k3.py", "exact_corank_two.py", "stratified_rank_two.py",
        "boundary_atlas.py", "generic_boundary_atlas.py",
    ],
    "exact_algebra_checked": [
        "generic transverse-slice Groebner bases",
        "generic (2,2) and (1,3) rank-one factors over fraction fields",
        "(1,3) generic saturation Hilbert quotient of length three",
        "finite determinant-depth witness regressions",
    ],
    "structural_proof_only": [
        "bounded principal-colon base-change theorem",
        "finite geometric-assassin stratification",
        "coordinate-ring Cauchy-Pieri projection and semisimple ideal projection",
    ],
}

out = {
    "revision": 129,
    "checks": checks,
    "evidence_scope": evidence_scope,
    "ok": all(v for k, v in checks.items() if k != "pdf_pages"),
}
(ROOT / "evidence" / "BUILD_RECEIPT.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
if not out["ok"]:
    raise SystemExit(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
