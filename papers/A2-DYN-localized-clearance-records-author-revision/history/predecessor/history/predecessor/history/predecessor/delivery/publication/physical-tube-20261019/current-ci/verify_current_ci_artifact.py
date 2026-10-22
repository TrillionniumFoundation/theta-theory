#!/usr/bin/env python3
"""Independently verify actual C2 CI bytes; execute no code from the archive."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
HEAD = "8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2"
ARTICLE_TREE = "c1ddfd34dd2b79900c747c3a16e941835bc94025"
RUN = 39187286448
JOB = 117852268064
ARTIFACT = 12158866926
ARTIFACT_SHA = "4b5c090e1a2ef608b48b08b4d0ffa648ffc34813243e597d4b85135464406406"
MATH_SHA = "fdfeab7b2dbb2febcf0b5a06ab47f2088e7b46a6a31b8e326fbaf2a7c76dca9d"
MANIFEST_SHA = "a891751e40fd6bb41fec5bd099883f78a66e616aeb4a95496694f991d95cc069"
ARTICLE_NAME = "A2-DYN-physical-tube-source-height-author-revision"
WORKFLOW = ".github/workflows/a2-dyn-physical-tube-source-height-20261019.yml"
HISTORICAL_RECEIPT = "evidence/current-execution/historical-recovery/20261019T015452772763Z/REBUILD_RECEIPT.json"


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def mathematical_path(path):
    p = PurePosixPath(path)
    return ((len(p.parts) == 1 and p.suffix == ".tex")
            or (len(p.parts) == 2 and p.parts[0] == "core" and p.suffix == ".tex")
            or (len(p.parts) == 2 and p.parts[0] == "tools" and p.suffix == ".py"))


def actual_pdf_pages(data):
    result = subprocess.run(["pdfinfo", "-"], input=data, capture_output=True)
    require(result.returncode == 0, "Independent pdfinfo inspection")
    match = re.search(rb"^Pages:\s+(\d+)\s*$", result.stdout, re.M)
    require(match is not None, "Actual PDF page count is readable")
    return int(match.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article", type=Path)
    ap.add_argument("--expected-identities", type=Path,
                    default=ROOT/"EXPECTED_C2_FILE_IDENTITIES.json")
    ap.add_argument("--manifest", type=Path,
                    help="Frozen SOURCE_MANIFEST.json; defaults to the complete article's manifest")
    ap.add_argument("--archive", type=Path, default=ROOT/f"CI_ARTIFACT_{ARTIFACT}.zip")
    ap.add_argument("--observation", type=Path, default=ROOT/"FINAL_OBSERVATION.json")
    ap.add_argument("--output-dir", type=Path, default=ROOT)
    args = ap.parse_args()
    article = args.article
    if article is None:
        for ancestor in (ROOT, *ROOT.parents):
            candidates = [ancestor, ancestor/"papers"/ARTICLE_NAME,
                          ancestor/"theta-theory/papers"/ARTICLE_NAME]
            article = next((p for p in candidates
                            if p.name == ARTICLE_NAME and (p/"main.tex").is_file()), None)
            if article is not None:
                break
    require(article is not None, "Complete current article available; pass --article")
    expected_document = json.loads(args.expected_identities.read_text())
    require(expected_document["article_tree_sha"] == ARTICLE_TREE, "Expected C2 article tree")
    expected = {r["path"]: r for r in expected_document["files"]}
    require(len(expected) == len(expected_document["files"]), "Unique C2 expected paths")

    observation = json.loads(args.observation.read_text())
    run = observation["run"]
    require(run["id"] == RUN and run["head_sha"] == HEAD
            and run["path"] == WORKFLOW and run["event"] == "push",
            "Actual dedicated push workflow at exact C2 head")
    require(run["status"] == "completed" and run["conclusion"] == "success",
            "Actual run completed successfully")
    jobs = observation["jobs"]["jobs"]
    require(len(jobs) == 1 and jobs[0]["id"] == JOB
            and jobs[0]["run_id"] == RUN and jobs[0]["status"] == "completed"
            and jobs[0]["conclusion"] == "success", "Actual exact-run job completed")
    require(len(jobs[0]["steps"]) == 11 and all(
        s["status"] == "completed" and s["conclusion"] == "success"
        for s in jobs[0]["steps"]), "All eleven actual job steps passed")
    artifact = next(a for a in observation["artifacts"]["artifacts"] if a["id"] == ARTIFACT)
    require(artifact["digest"] == "sha256:" + ARTIFACT_SHA
            and artifact["workflow_run"]["head_sha"] == HEAD
            and artifact["workflow_run"]["id"] == RUN, "Artifact belongs to exact C2 run")

    manifest_data = (args.manifest or article/"SOURCE_MANIFEST.json").read_bytes()
    require(sha(manifest_data) == MANIFEST_SHA
            == expected["SOURCE_MANIFEST.json"]["sha256"], "Frozen manifest identity")
    manifest = json.loads(manifest_data)
    require(manifest["source_count"] == len(manifest["files"]) == 1408,
            "All 1408 frozen source/evidence inputs")
    require(sum(r["bytes"] for r in manifest["files"]) == manifest["source_bytes"],
            "Frozen source byte total")
    for row in manifest["files"]:
        data = (article/row["path"]).read_bytes()
        e = expected[row["path"]]
        require(len(data) == row["bytes"] == e["bytes"]
                and sha(data) == row["sha256"] == e["sha256"]
                and blob(data) == row["git_blob"] == e["sha"],
                "Frozen input matches expected C2 bytes: " + row["path"])

    archive = args.archive
    archive_data = archive.read_bytes()
    require(len(archive_data) == artifact["size_in_bytes"] == 10763491
            and sha(archive_data) == ARTIFACT_SHA, "Actual downloaded artifact digest and size")
    with zipfile.ZipFile(archive) as z:
        files = [i for i in z.infolist() if not i.is_dir()]
        names = [i.filename for i in files]
        require(len(set(names)) == len(names), "Unique artifact paths")
        require(all(not PurePosixPath(n).is_absolute()
                    and ".." not in PurePosixPath(n).parts for n in names), "Safe artifact paths")
        file_manifest = [{"path":i.filename, "bytes":i.file_size, "sha256":sha(z.read(i.filename))}
                         for i in files]
        require(z.read("build/current/CI_CHECKOUT_SHA.txt").decode().strip() == HEAD,
                "Actual checkout SHA recorded in archive")
        require(z.read("build/current/CI_BUILD_OUTCOME.txt").decode().strip() == "success",
                "Actual native build outcome")
        entrypoints = []
        for line in z.read("build/current/CI_ENTRYPOINT_SHA256.txt").decode().splitlines():
            digest, path = line.split(None, 1)
            path = path.lstrip("*")
            require(expected[path]["sha256"] == digest, "Actual entrypoint identity: " + path)
            entrypoints.append(path)
        require(len(entrypoints) == 3, "Three actual entrypoint identities")

        phase = json.loads(z.read("build/current/PHASE_all.json"))
        require(phase["status"] == "passed"
                and set(phase["completed"]) == {"source", "math", "typeset"},
                "Actual source, math and typeset phases completed")
        require(stamp(phase["started_utc"]) >= stamp(run["run_started_at"]),
                "Native execution is from this run, not an inherited receipt")
        mathematical_rows = [{"path":p, "sha256":expected[p]["sha256"]}
                             for p in sorted(expected) if mathematical_path(p)]
        require(len(mathematical_rows) == 98, "All 98 native/tool inputs identified")
        require(phase["mathematical_source"]["files"] == mathematical_rows,
                "Archive native/tool input list exactly matches C2")
        require(sha(json.dumps(mathematical_rows, sort_keys=True).encode())
                == phase["mathematical_source"]["sha256"] == MATH_SHA,
                "Independent mathematical fingerprint reconstruction")
        for row in mathematical_rows:
            require(sha((article/row["path"]).read_bytes()) == row["sha256"],
                    "Current native/tool bytes match C2: " + row["path"])

        math = json.loads(z.read("build/current/mathematical-checks.json"))
        require(math["status"] == "passed" and not math["failures"]
                and math["commands_expected"] == math["commands_completed"]
                == len(math["commands"]) == 44, "All 44 actual math commands")
        require(len({c["tag"] for c in math["commands"]}) == 44, "Distinct actual math command tags")
        require(math["mathematical_source"] == phase["mathematical_source"],
                "Math phase source identity")
        for command in math["commands"]:
            data = z.read("build/current/" + command["log"])
            require(command["exit_code"] == 0
                    and len(data) == command["log_bytes"]
                    and sha(data) == command["log_sha256"]
                    and command["current_mathematical_source_sha256"] == MATH_SHA,
                    "Actual math command and output: " + command["tag"])
            require(json.loads(z.read("build/current/" + command["tag"] + ".command.json"))
                    == command, "Individual command receipt agrees: " + command["tag"])
        comparisons = math["normal_optimized_comparisons"]
        require(len(comparisons) == 35, "All 35 normal/optimized comparisons")
        for compare in comparisons:
            require(compare["scope"] in ("stdout", "details"), "Known comparison scope")
            suffix = ".log" if compare["scope"] == "stdout" else ".details.json"
            left = z.read("build/current/" + compare["program"] + "-normal" + suffix)
            right = z.read("build/current/" + compare["program"] + "-optimized" + suffix)
            require(compare["byte_identical"] and left == right
                    and sha(left) == compare["sha256"], "Actual paired output bytes")

        source = json.loads(z.read("build/current/source-checks.json"))
        require(source["status"] == "passed" and source["manifest"]["verified"]
                and source["manifest"]["source_count"] == manifest["source_count"]
                and source["manifest"]["source_bytes"] == manifest["source_bytes"]
                and source["original_reports_verified"] == 90
                and source["active_complete_core_bodies"] == 54
                and source["reachable_native_tex"] == 64
                and not source["unresolved_references"], "Actual complete source gate")
        require(source["mathematical_source"] == phase["mathematical_source"],
                "Source phase native/tool identity")
        for key in ("immutable_source_anchor_sha256", "preceding_author_native_anchor_sha256"):
            require(source["manifest"][key] == manifest[key], "Actual inherited anchor: " + key)

        native = json.loads(z.read("build/current/native-typeset.json"))
        require(native["status"] == "passed" and not native["layout_or_reference_problems"]
                and native["mathematical_source"] == phase["mathematical_source"],
                "Actual native document and source identity")
        require(len(native["commands"]) == 4
                and sum(Path(c["command"][0]).name == "pdflatex" for c in native["commands"]) == 3,
                "Three actual TeX passes and one PDF inspection")
        for command in native["commands"]:
            data = z.read("build/current/native/" + command["log"])
            require(command["exit_code"] == 0 and len(data) == command["log_bytes"]
                    and sha(data) == command["log_sha256"]
                    and command["current_mathematical_source_sha256"] == MATH_SHA,
                    "Native command and output: " + command["tag"])
        native_pdf = z.read("build/current/native/main.pdf")
        require(sha(native_pdf) == native["pdf_sha256"]
                and len(native_pdf) == native["pdf_bytes"]
                and actual_pdf_pages(native_pdf) == native["pages"] == 164,
                "Actual native PDF identity and 164 pages")
        require(sha(z.read("build/current/native/main.aux")) == native["aux_sha256"],
                "Actual native auxiliary-file identity")
        require(native["main_tex_sha256"] == expected["main.tex"]["sha256"], "Main TeX identity")

        historical = []
        earlier_historical = []
        for name in names:
            if name.endswith("/REBUILD_RECEIPT.json"):
                receipt = json.loads(z.read(name))
                if stamp(receipt["started_utc"]) >= stamp(phase["finished_utc"]):
                    historical.append((name, receipt))
                else:
                    earlier_historical.append({"path":name, "success":receipt["success"]})
        require(len(historical) == 1, "One fresh post-native historical execution")
        historical_path, history = historical[0]
        require(historical_path == HISTORICAL_RECEIPT,
                "Explicit current-CI historical receipt, not an inherited execution")
        require(history["success"] and history["source_files_checked"] == 390
                and len(history["commands"]) == 9
                and stamp(history["completed_utc"]) <= stamp(run["updated_at"]),
                "Actual fresh historical 390-source, nine-command rebuild")
        historical_prefix = str(PurePosixPath(historical_path).parent) + "/"
        for command in history["commands"]:
            data = z.read(historical_prefix + Path(command["output"]).name)
            require(command["returncode"] == 0
                    and len(data) == command["output_identity"]["bytes"]
                    and sha(data) == command["output_identity"]["sha256"],
                    "Actual historical command/output identity")
        documents = []
        require({d["document"] for d in history["documents"]} == {"main", "supplement"},
                "Both complete historical documents present")
        for document in history["documents"]:
            name = document["document"]
            expected_pages = 26 if name == "main" else 883
            data = z.read("history/historical-v108/build/" + name + ".pdf")
            require(len(data) == document["pdf"]["bytes"]
                    and sha(data) == document["pdf"]["sha256"]
                    and actual_pdf_pages(data) == document["pages"] == expected_pages,
                    "Actual historical PDF identity and pages: " + name)
            log = z.read("history/historical-v108/build/" + name + ".log")
            require(sha(log) == document["log"]["sha256"], "Actual historical final log: " + name)
            documents.append({"name":name, "pages":expected_pages, "pdf_sha256":sha(data),
                              "diagnostics":document["diagnostics"]})

        post_status = z.read("build/current/CI_POST_RUN_STATUS.txt").decode().splitlines()
        allowed = ["papers/" + ARTICLE_NAME + "/" + p for p in
                   ("build/", "history/historical-v108/build/",
                    "evidence/current-execution/historical-recovery/")]
        require(all(len(line) >= 4 and any(line[3:].startswith(p) for p in allowed)
                    for line in post_status), "Post-run changes are generated build/evidence only")
        environment = z.read("build/current/CI_ENVIRONMENT.log").decode()
        require(environment.startswith("Python 3.11.17\n")
                and all(x in environment for x in
                        ("mpmath==1.3.0", "numpy==2.3.5", "scipy==1.17.0", "sympy==1.14.0")),
                "Actual pinned Python/math environment")

    log_identity = json.loads((ROOT/"CI_JOB_LOG_IDENTITY.json").read_text())
    job_log = (ROOT/log_identity["file"]).read_bytes()
    require(len(job_log) == log_identity["bytes"] and sha(job_log) == log_identity["sha256"]
            and log_identity["exact_returned_utf8_text"], "Exact purpose-built job-log text")
    result = {
        "status":"passed", "verified_utc":datetime.now(timezone.utc).isoformat(),
        "scope":"Independent actual C2 CI artifact integrity, execution and source-identity checks; no archive code executed",
        "run_id":RUN, "job_id":JOB, "exact_head":HEAD, "article_tree_sha":ARTICLE_TREE,
        "run_status":run["status"], "run_conclusion":run["conclusion"],
        "run_updated_utc":run["updated_at"], "actual_job_steps_verified":len(jobs[0]["steps"]),
        "artifact_id":ARTIFACT, "artifact_bytes":len(archive_data), "artifact_sha256":ARTIFACT_SHA,
        "artifact_files":len(files), "mathematical_source_sha256":MATH_SHA,
        "native_tool_inputs_verified_against_C2":len(mathematical_rows),
        "frozen_manifest_sha256":MANIFEST_SHA, "frozen_inputs_verified_against_C2":1408,
        "frozen_input_bytes":manifest["source_bytes"], "entrypoints_verified":entrypoints,
        "phase_started_utc":phase["started_utc"], "phase_finished_utc":phase["finished_utc"],
        "math_commands_verified":44, "normal_optimized_actual_pairs_verified":35,
        "original_reports_verified":90, "active_core_bodies":54, "reachable_native_tex":64,
        "native_compile_commands_verified":4, "actual_pdflatex_passes":3, "native_pages":164,
        "native_pdf_sha256":native["pdf_sha256"], "native_pdf_bytes":len(native_pdf),
        "native_aux_sha256":native["aux_sha256"], "native_advisories":native["advisories"],
        "fresh_historical_receipt":historical_path, "fresh_historical_commands_verified":9,
        "fresh_historical_sources_verified":390, "historical_documents":documents,
        "historical_started_utc":history["started_utc"],
        "historical_completed_utc":history["completed_utc"],
        "earlier_historical_receipts_preserved_separately":earlier_historical,
        "post_run_changed_paths":post_status, "post_run_changes_only_generated":True,
        "environment":environment, "exact_job_log":log_identity,
        "actual_current_ci_success_verified":True,
        "continuum_mathematical_proof_certificate":False,
        "independent_human_specialist_certification":False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"CURRENT_CI_ARTIFACT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.output_dir/"CURRENT_CI_ARTIFACT_FILE_MANIFEST.json").write_text(
        json.dumps({"artifact_sha256":ARTIFACT_SHA, "files":file_manifest}, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
