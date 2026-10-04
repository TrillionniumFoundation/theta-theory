#!/usr/bin/env python3
"""Finite rejection tests for the v36 source and publication contract."""
from __future__ import annotations

from collections import Counter
import copy
import json
from pathlib import Path
import tempfile
import zipfile

from validate_v36 import (
    PACKAGE, REQUIRED_FILES, WORKFLOW, collect_sources, deterministic_zip,
    digest, inspect_tex_log, manifest_document, prepare_evidence_directory,
    tex_input_closure, validate_head_binding, validate_manifest,
    verify_preservation, verify_recorded_inputs,
)

COUNTS: Counter[str] = Counter()


def require(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    COUNTS[group] += 1


def reject(function, group: str) -> None:
    try:
        function()
    except (ValueError, FileNotFoundError):
        COUNTS[group] += 1
    else:
        raise RuntimeError("invalid contract accepted: " + group)


def fixture(repo: Path) -> Path:
    paper = repo / Path(PACKAGE)
    for name in REQUIRED_FILES:
        path = paper / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")
    (paper / "core").mkdir()
    (paper / "core/proof.tex").write_text("A finite proof fixture.\n", encoding="utf-8")
    (paper / "main.tex").write_text("\\input{core/proof}\n\\input{references}\n", encoding="utf-8")
    workflow = repo / WORKFLOW
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: fixture\n", encoding="utf-8")
    return paper


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary)
        paper = fixture(repo)
        actual, inputs = collect_sources(paper, repo), tex_input_closure(paper)
        pins = manifest_document(actual, inputs)
        validate_manifest(pins, actual, inputs)
        require(True, "complete_manifest_accepted")

        for field in pins:
            damaged = copy.deepcopy(pins)
            del damaged[field]
            reject(lambda: validate_manifest(damaged, actual, inputs), "missing_manifest_field_rejected")
        for field, value in [
            ("schema", "a2-v35-source-pins-1"),
            ("journal_documents", ["main.tex", "archive/main.tex"]),
            ("reviewed_author_commit", "0" * 40),
            ("controlling_review_commit", "0" * 40),
            ("preserved_trees", {}),
            ("tex_inputs", []),
            ("formal_proof_certificate", True),
            ("physical_sensor_executed", True),
        ]:
            damaged = copy.deepcopy(pins)
            damaged[field] = value
            reject(lambda: validate_manifest(damaged, actual, inputs), "altered_manifest_contract_rejected")
        damaged = copy.deepcopy(pins)
        damaged["unexpected_claim"] = "passed"
        reject(lambda: validate_manifest(damaged, actual, inputs), "extra_manifest_field_rejected")

        target = paper / "core/proof.tex"
        original = target.read_bytes()
        target.write_bytes(original + b"Tampered.\n")
        reject(lambda: validate_manifest(pins, collect_sources(paper, repo), inputs),
               "tampered_source_bytes_rejected")
        target.write_bytes(original)
        target.unlink()
        reject(lambda: validate_manifest(pins, collect_sources(paper, repo), inputs),
               "missing_pinned_source_rejected")
        reject(lambda: tex_input_closure(paper), "missing_active_tex_input_rejected")
        target.write_bytes(original)
        extra = paper / "tools/unadvertised.py"
        extra.write_text("print('unexpected')\n", encoding="utf-8")
        reject(lambda: validate_manifest(pins, collect_sources(paper, repo), inputs),
               "unadvertised_source_rejected")
        extra.unlink()
        required = paper / "tools/verify_v36.py"
        required_data = required.read_bytes()
        required.unlink()
        reject(lambda: collect_sources(paper, repo), "missing_required_validator_rejected")
        required.write_bytes(required_data)
        workflow = repo / WORKFLOW
        workflow_data = workflow.read_bytes()
        workflow.write_bytes(workflow_data + b"changed: true\n")
        reject(lambda: validate_manifest(pins, collect_sources(paper, repo), inputs),
               "changed_workflow_rejected")
        workflow.write_bytes(workflow_data)
        target.chmod(0o644)
        link = paper / "alias.tex"
        link.symlink_to(target)
        reject(lambda: collect_sources(paper, repo), "symlink_source_rejected")
        link.unlink()
        orphan = paper / "core/orphan.tex"
        orphan.write_text("Inactive result.\n", encoding="utf-8")
        reject(lambda: tex_input_closure(paper), "inactive_tex_result_rejected")
        orphan.unlink()
        main_path = paper / "main.tex"
        main_bytes = main_path.read_bytes()
        main_path.write_text("\\input{../outside}\n", encoding="utf-8")
        reject(lambda: tex_input_closure(paper), "escaping_tex_input_rejected")
        main_path.write_bytes(main_bytes)

        old_proof = "\\begin{lemma}\\label{lem:old}A statement.\\end{lemma}\n"
        old_proof += "\\begin{proof}The retained argument.\\end{proof}\n"
        reviewed = {"core/proof.tex": old_proof}
        extended = {"core/proof.tex": old_proof,
                    "core/new.tex": "\\begin{proof}A new argument.\\end{proof}"}
        preservation = verify_preservation(reviewed, extended)
        require(preservation["reviewed_proof_bodies"] == 1
                and preservation["current_proof_bodies"] == 2,
                "retained_proofs_with_new_proofs_accepted")
        reject(lambda: verify_preservation(reviewed, {"proof.tex": old_proof.replace(
            "\\label{lem:old}", "")}), "deleted_reviewed_label_rejected")
        reject(lambda: verify_preservation(reviewed, {"proof.tex": old_proof.replace(
            "The retained argument.", "A changed argument.")}), "changed_reviewed_proof_rejected")
        reject(lambda: verify_preservation(reviewed, {"proof.tex": old_proof + "\\label{lem:old}"}),
               "duplicate_current_label_rejected")
        reject(lambda: verify_preservation({}, extended), "empty_preservation_baseline_rejected")

        head = "a" * 40
        require(validate_head_binding(head, head, "", False) == "exact_expected_checkout",
                "exact_clean_head_accepted")
        require(validate_head_binding(None, head, " M changed.tex", True)
                == "development_source_content", "development_label_explicit")
        for expected, observed, dirty, allow in [
            (None, head, "", False), (head[:12], head, "", False),
            (head, "b" * 40, "", False), (head, head, " M main.tex", False),
            (head, head, "", True), (None, "unknown", "", True),
        ]:
            reject(lambda: validate_head_binding(expected, observed, dirty, allow),
                   "false_commit_qualification_rejected")

        for diagnostic in ["LaTeX Warning: reference undefined", "Overfull \\hbox (1.0pt)",
                           "Underfull \\hbox", "! Fatal error", "Reference X undefined"]:
            require(bool(inspect_tex_log(diagnostic)), "tex_diagnostic_detected")
        require(inspect_tex_log("Output written on main.pdf (3 pages).\n") == [],
                "clean_tex_log_accepted")

        members = {name: (str(PACKAGE / name), actual[str(PACKAGE / name)]) for name in inputs}
        first, second = repo / "first.zip", repo / "second.zip"
        deterministic_zip(first, repo, members)
        deterministic_zip(second, repo, members)
        require(first.read_bytes() == second.read_bytes(), "source_zip_deterministic")
        with zipfile.ZipFile(first) as archive:
            require(archive.namelist() == sorted(inputs), "journal_zip_contains_only_primary_inputs")
            for name in archive.namelist():
                require(archive.read(name) == (paper / name).read_bytes(), "journal_zip_bytes_match_source")
        target.write_bytes(original + b"changed after manifest\n")
        reject(lambda: deterministic_zip(repo / "bad.zip", repo, members),
               "packaging_race_rejected")
        target.write_bytes(original)
        reject(lambda: deterministic_zip(repo / "unsafe.zip", repo,
                                         {"../escape.tex": next(iter(members.values()))}),
               "unsafe_archive_path_rejected")

        build = paper / "build"
        build.mkdir()
        fls = build / "main.fls"
        fls.write_text("INPUT ./main.tex\nINPUT " + str(build / "main.aux") + "\n", encoding="utf-8")
        verify_recorded_inputs(fls, paper, repo, build, actual)
        require(True, "pinned_tex_inputs_accepted")
        fls.write_text("INPUT ./not-pinned.sty\n", encoding="utf-8")
        reject(lambda: verify_recorded_inputs(fls, paper, repo, build, actual),
               "unrecorded_tex_input_rejected")

        evidence = paper / "verification/current"
        prepare_evidence_directory(evidence)
        (evidence / "receipt.json").write_text("{}\n", encoding="utf-8")
        (evidence / "old.log").write_text("old generated evidence\n", encoding="utf-8")
        prepare_evidence_directory(evidence)
        require(not list(evidence.iterdir()), "stale_generated_evidence_removed")
        protected = evidence / "user-data.txt"
        protected.write_text("preserve this\n", encoding="utf-8")
        reject(lambda: prepare_evidence_directory(evidence), "unknown_evidence_files_preserved")
        require(protected.read_text() == "preserve this\n", "unknown_evidence_file_not_deleted")
        require(collect_sources(paper, repo) == actual, "generated_evidence_excluded_from_source_hashes")

    print(json.dumps({"schema": "a2-v36-contract-tests-1", "status": "passed",
                      "checks": dict(sorted(COUNTS.items())),
                      "total_checks": sum(COUNTS.values()),
                      "formal_proof_certificate": False,
                      "physical_sensor_executed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
