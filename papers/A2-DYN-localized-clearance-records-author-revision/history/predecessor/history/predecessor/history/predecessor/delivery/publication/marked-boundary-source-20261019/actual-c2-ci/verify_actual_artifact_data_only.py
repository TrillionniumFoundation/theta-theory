#!/usr/bin/env python3
"""Check actual artifact bytes and execution receipts, without certifying CI completion.

The unchanged full verifier has actually failed at its completed/success gate.
This separate data audit neither invokes nor patches that verifier's main(),
does not change an API object, and never supplies invented steps or timestamps.
Only its hash-pinned pure parsing/identity helpers are reused. No archive code
is imported, executed or extracted. A successful data audit is not green CI.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

SEALED_SHA256 = "e44db871d6afaea2aaac23ec836ceb1e57993ecb464afcf884475530b1e7b42f"


def now():
    return datetime.now(timezone.utc).isoformat()


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {"file": str(path.resolve()), "bytes": len(data), "sha256": sha(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict-execution", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    started = now()
    execution = json.loads(args.strict_execution.read_bytes())
    command = execution["command"]
    require(len(command) >= 4 and len(command[2:]) % 2 == 0, "Actual strict argv has complete option/value pairs")
    options = dict(zip(command[2::2], command[3::2]))
    require(len(options) == len(command[2:]) // 2, "Actual strict argv has unique options")
    require(set(options) == {
        "--article", "--archive", "--tested-commit", "--tested-article-tree", "--tested-root-tree",
        "--workflow", "--expected-identities", "--manifest", "--reference-build", "--reference-source",
        "--reference-history", "--observation", "--artifact-id", "--job-id", "--job-log-identity",
        "--job-log", "--output-dir"}, "All actual strict input options are preserved")
    helper_path = Path(command[1])
    require(sha(helper_path.read_bytes()) == SEALED_SHA256 == execution["verifier_identity"]["sha256"],
            "The original sealed full verifier remains byte-identical")
    require(execution["exit_code"] == 1 and execution["status"] == "failed", "The actual full-verifier failure is preserved")
    strict_stderr = Path(execution["stderr"]["file"])
    strict_stdout = Path(execution["stdout"]["file"])
    require(identity(strict_stderr) == execution["stderr"] and identity(strict_stdout) == execution["stdout"],
            "Exact original strict stdout/stderr bytes are retained")
    require(strict_stdout.read_bytes() == b"" and strict_stderr.read_text().endswith(
        "RuntimeError: Actual run completed successfully\n"), "The actual full verifier stopped at its original completion gate")
    spec = importlib.util.spec_from_file_location("sealed_artifact_identity_helpers", helper_path)
    require(spec is not None and spec.loader is not None, "Hash-pinned helper module can be read")
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)

    article = Path(options["--article"]).resolve()
    article_name = article.name
    require(article_name == helpers.AUTHOR_ARTICLE and options["--workflow"] == helpers.AUTHOR_WORKFLOW,
            "Actual article and dedicated workflow match the author contract")
    expected_path = Path(options["--expected-identities"])
    require(identity(expected_path) == execution["tested_inventory_identity"], "Actual tested inventory is unchanged")
    expected_doc = json.loads(expected_path.read_bytes())
    expected = {row["path"]: row for row in expected_doc["files"]}
    require(len(expected) == len(expected_doc["files"]), "Unique expected file rows")
    tree, trees = helpers.expected_tree(expected_doc["files"])
    require(tree == expected_doc["article_tree_sha"] == options["--tested-article-tree"], "Complete expected article tree reconstructs")
    require(expected_doc["root_tree_sha"] == options["--tested-root-tree"], "Actual expected root identity agrees")
    require(all(trees[name] == h for name, h in expected_doc.get("subtree_hashes", {}).items()), "All expected subtree identities reconstruct")
    local_identities = {}

    def checked_local(path):
        require(not path.is_symlink(), "No source/reference symlink substitution")
        path = path.resolve()
        require(path.is_relative_to(article), "Every source/reference lies within the tested article")
        relative = path.relative_to(article).as_posix()
        require(relative in expected, "Referenced file exists in the actual tested inventory: " + relative)
        data = path.read_bytes()
        record = helpers.file_identity(data)
        row = expected[relative]
        mode = "100755" if path.stat().st_mode & 0o111 else "100644"
        require(record == {"bytes": row["bytes"], "sha256": row["sha256"], "git_blob": row["sha"]}
                and mode == row["mode"] and row.get("type", "blob") == "blob",
                "Actual tested source byte/mode identity: " + relative)
        local_identities[relative] = {"path": relative, "mode": mode, **record}
        return data

    manifest_data = checked_local(Path(options["--manifest"]))
    manifest = json.loads(manifest_data)
    require(manifest["schema"] == 5 and len(manifest["files"]) == manifest["source_count"]
            == len({r["path"] for r in manifest["files"]}), "Complete schema-5 frozen manifest")
    require(sum(r["bytes"] for r in manifest["files"]) == manifest["source_bytes"], "Frozen source byte total")
    for row in manifest["files"]:
        data = checked_local(article / helpers.safe_path(row["path"]))
        require(helpers.file_identity(data) == {k: row[k] for k in ("bytes", "sha256", "git_blob")},
                "Every actual frozen manifest row: " + row["path"])
    anchors = helpers.immutable_anchor_contract(checked_local, article, manifest)
    contract = helpers.native_and_driver_contract(checked_local, article, expected)
    original_reports = json.loads(checked_local(article / "audit/reports_index.json"))
    require(len(original_reports) == 90, "All original 90 report rows remain present")
    for row in original_reports:
        data = checked_local(article / helpers.safe_path(row["artifact_relative_report_path"]))
        require(helpers.file_identity(data) == {"bytes": row["bytes"], "sha256": row["sha256"], "git_blob": row["blob_sha"]},
                "Every original report has its exact original bytes")
    extra_report = checked_local(article / helpers.ORIGINAL_REPORT_PATH)
    require(helpers.file_identity(extra_report) == {"bytes": 35703, "sha256": helpers.ORIGINAL_REPORT_SHA256,
                                                   "git_blob": helpers.ORIGINAL_REPORT_BLOB}, "Exact distinct original v73 report")
    mathematical_rows = [{"path": p, "sha256": expected[p]["sha256"]}
                         for p in sorted(expected) if helpers.mathematical_path(p)]
    mathematical_sha = sha(json.dumps(mathematical_rows, sort_keys=True).encode())
    for row in mathematical_rows:
        require(sha(checked_local(article / row["path"])) == row["sha256"], "Every current native/tool source byte")
    reference_build = Path(options["--reference-build"])
    ref_math = json.loads(checked_local(reference_build / "mathematical-checks.json"))
    ref_native = json.loads(checked_local(reference_build / "native-typeset.json"))
    ref_source = json.loads(checked_local(Path(options["--reference-source"])))
    ref_history = json.loads(checked_local(Path(options["--reference-history"])))
    for receipt in (ref_math, ref_native, ref_source):
        require(receipt["status"] == "passed" and receipt["mathematical_source"] == {
            "files": mathematical_rows, "sha256": mathematical_sha}, "Every actual final local reference has the tested source fingerprint")
    require(not ref_math["failures"] and not ref_native["layout_or_reference_problems"], "Passed actual final local mathematical/native references")
    require(ref_source["active_complete_core_bodies"] == len(contract["core_paths"]) == 59
            and ref_source["reachable_native_tex"] == len(contract["reachable"]) == 69
            and ref_source["native_labels"] == len(contract["labels"])
            and ref_source["new_body_labels"] == contract["new_body_labels"], "Actual complete native source graph and labels")
    local_pdf = checked_local(reference_build / "native/main.pdf")
    local_aux = checked_local(reference_build / "native/main.aux")
    require(sha(local_pdf) == ref_native["pdf_sha256"] and len(local_pdf) == ref_native["pdf_bytes"]
            and helpers.pdf_pages(local_pdf) == ref_native["pages"] and sha(local_aux) == ref_native["aux_sha256"],
            "Actual final local native PDF/aux identities and independent PDF page count")
    ref_commands = {c["tag"]: c for c in ref_math["commands"]}
    require(len(ref_commands) == ref_math["commands_expected"] == ref_math["commands_completed"] == 52
            and set(ref_commands) == contract["tags"], "All actual final local mathematical commands")
    for tag, item in ref_commands.items():
        require(helpers.normalize_command(item["command"], article_name) == contract["normalized_commands"][tag],
                "Actual local reference argv agrees with declared source contract: " + tag)
    require({(p["program"], p["scope"]) for p in ref_math["normal_optimized_comparisons"]} == contract["pairs"]
            and len(ref_math["normal_optimized_comparisons"]) == 43
            and all(p["byte_identical"] for p in ref_math["normal_optimized_comparisons"]), "Actual final local 43-pair contract")
    require(ref_history["success"] and len(ref_history["commands"]) == 9 and ref_history["source_files_checked"] == 390,
            "Actual final local historical reference")

    observation_path = Path(options["--observation"])
    require(identity(observation_path) == execution["observation_identity"], "Actual unmodified strict observation bytes")
    observation = json.loads(observation_path.read_bytes())
    run = observation["run"]
    jobs = observation["jobs"]["jobs"]
    require(run["head_sha"] == options["--tested-commit"] and run["event"] == "push"
            and run["head_branch"] == helpers.AUTHOR_BRANCH and run["path"] == helpers.AUTHOR_WORKFLOW,
            "Actual observed push head, author branch and workflow")
    require(observation["jobs"]["total_count"] == len(jobs) == 1
            and jobs[0]["id"] == int(options["--job-id"]) and jobs[0]["run_id"] == run["id"]
            and jobs[0]["head_sha"] == options["--tested-commit"], "Actual job identity and complete collection")
    require(run["status"] == "queued" and run["conclusion"] is None
            and jobs[0]["status"] == "queued" and jobs[0]["conclusion"] is None and jobs[0]["steps"] == [],
            "This data-only audit records the actual unresolved queued observation, without inventing completion")
    require(observation["artifacts"]["total_count"] == len(observation["artifacts"]["artifacts"]), "Actual complete artifact collection")
    selected = [a for a in observation["artifacts"]["artifacts"] if a["id"] == int(options["--artifact-id"])]
    require(len(selected) == 1, "Exactly one actual selected artifact")
    artifact = selected[0]
    require(not artifact["expired"] and artifact["workflow_run"]["id"] == run["id"]
            and artifact["workflow_run"]["head_sha"] == options["--tested-commit"], "Actual artifact run/head identity")
    archive_path = Path(options["--archive"])
    archive_bytes = archive_path.read_bytes()
    require(len(archive_bytes) == artifact["size_in_bytes"] and artifact["digest"] == "sha256:" + sha(archive_bytes),
            "Actual complete downloaded artifact bytes match its advertised size and digest")
    log_identity = json.loads(Path(options["--job-log-identity"]).read_bytes())
    log_bytes = Path(options["--job-log"]).read_bytes()
    require(log_identity["job_id"] == int(options["--job-id"]) and log_identity["exact_returned_utf8_text"]
            and len(log_bytes) == log_identity["bytes"] and sha(log_bytes) == log_identity["sha256"], "Exact actual job-log UTF-8 bytes")
    log_text = log_bytes.decode("utf-8")
    times = re.findall(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z) ", log_text, re.M)
    require(times and all(helpers.utc(a) <= helpers.utc(b) for a, b in zip(times, times[1:])), "Actual log timestamps are chronological")
    log_first, log_last = times[0], times[-1]
    command_results = []
    pair_results = []
    archive_manifest = []
    with zipfile.ZipFile(archive_path) as archive:
        all_entries = archive.infolist()
        require(len({e.filename for e in all_entries}) == len(all_entries), "Every ZIP entry name is unique")
        entries = [entry for entry in all_entries if not entry.is_dir()]
        for entry in all_entries:
            helpers.safe_path(entry.filename.rstrip("/") if entry.is_dir() else entry.filename)
            require(not stat.S_ISLNK(entry.external_attr >> 16), "No ZIP symlink members")
        for entry in entries:
            archive_manifest.append({"path": entry.filename, **helpers.file_identity(archive.read(entry.filename))})
        require(archive.testzip() is None, "Every actual ZIP member is read with a clean CRC")
        names = [entry.filename for entry in entries]

        def read(name):
            return archive.read(helpers.safe_path(name))

        def load(name):
            return json.loads(read(name))

        prefix = "build/current/"
        require(read(prefix + "CI_CHECKOUT_SHA.txt").decode().strip() == options["--tested-commit"], "Actual archived checkout identity")
        require(read(prefix + "CI_BUILD_OUTCOME.txt").decode().strip() == "success", "Actual archived build outcome records success")
        entrypoints = []
        for line in read(prefix + "CI_ENTRYPOINT_SHA256.txt").decode().splitlines():
            h, path = line.split(None, 1)
            path = helpers.safe_path(path.lstrip("*"))
            require(h == expected[path]["sha256"] == sha(checked_local(article / path)), "Actual dedicated entrypoint bytes")
            entrypoints.append({"path": path, "sha256": h})
        require(len(entrypoints) == 3 and {p["path"] for p in entrypoints} == {
            "build.sh", "requirements.txt", "ci/" + Path(options["--workflow"]).name}, "All three actual dedicated entrypoints")
        phase = load(prefix + "PHASE_all.json")
        require(phase["status"] == "passed" and set(phase["completed"]) == {"source", "math", "typeset"}
                and phase["mathematical_source"] == {"files": mathematical_rows, "sha256": mathematical_sha},
                "Actual complete source/math/native phase at the exact frozen source")
        require(helpers.utc(log_first) <= helpers.utc(phase["started_utc"]) <= helpers.utc(phase["finished_utc"]) <= helpers.utc(log_last),
                "Actual archived complete phase lies within the actual job-log interval")

        def command_check(item, base, reference):
            data = read(base + helpers.safe_path(item["log"]))
            require(item["exit_code"] == 0 and len(data) == item["log_bytes"] and sha(data) == item["log_sha256"]
                    and item["current_mathematical_source_sha256"] == mathematical_sha, "Actual command exit/log/source: " + item["tag"])
            require(helpers.utc(phase["started_utc"]) <= helpers.utc(item["started_utc"])
                    <= helpers.utc(item["finished_utc"]) <= helpers.utc(phase["finished_utc"]), "Actual command phase interval: " + item["tag"])
            require(Path(item["cwd"]).name == article_name and helpers.normalize_command(item["command"], article_name)
                    == helpers.normalize_command(reference["command"], article_name), "Actual command argv and article: " + item["tag"])
            require(load(base + item["tag"] + ".command.json") == item, "Exact individual command receipt: " + item["tag"])
            command_results.append({"tag": item["tag"], "command": item["command"], "exit_code": item["exit_code"],
                                    "started_utc": item["started_utc"], "finished_utc": item["finished_utc"],
                                    "log": base + item["log"], "log_bytes": len(data), "log_sha256": sha(data),
                                    "individual_receipt_matches": True, "expected_argv_matches": True})

        math = load(prefix + "mathematical-checks.json")
        require(math["status"] == "passed" and not math["failures"] and math["mathematical_source"] == phase["mathematical_source"],
                "Actual archived mathematical phase")
        require(math["commands_expected"] == math["commands_completed"] == len(math["commands"]) == 52
                and {c["tag"] for c in math["commands"]} == contract["tags"], "Every one of the 52 required actual mathematical commands")
        for item in math["commands"]:
            command_check(item, prefix, ref_commands[item["tag"]])
        comparisons = math["normal_optimized_comparisons"]
        require(len(comparisons) == 43 and {(p["program"], p["scope"]) for p in comparisons} == contract["pairs"], "All 43 actual declared paired outputs")
        for pair in comparisons:
            suffix = ".log" if pair["scope"] == "stdout" else ".details.json"
            left = read(prefix + pair["program"] + "-normal" + suffix)
            right = read(prefix + pair["program"] + "-optimized" + suffix)
            require(pair["byte_identical"] and left == right and sha(left) == pair["sha256"], "Actual paired bytes: " + pair["program"] + "/" + pair["scope"])
            pair_results.append({"program": pair["program"], "scope": pair["scope"], "bytes": len(left),
                                 "sha256": sha(left), "actual_bytes_equal": True})
        source = load(prefix + "source-checks.json")
        require(source["status"] == "passed" and source["manifest"]["verified"] and not source["unresolved_references"]
                and source["mathematical_source"] == phase["mathematical_source"], "Actual archived source/reference gate")
        for key in ("original_reports_verified", "additional_original_reports_verified", "active_complete_core_bodies",
                    "reachable_native_tex", "native_labels", "new_body_labels"):
            require(source[key] == ref_source[key], "Actual source/reference count: " + key)
        for key in ("source_count", "source_bytes", *helpers.ANCHOR_PATHS):
            require(source["manifest"][key] == ref_source["manifest"][key] == manifest[key], "Actual frozen source/anchor identity: " + key)
        native = load(prefix + "native-typeset.json")
        require(native["status"] == "passed" and not native["layout_or_reference_problems"]
                and native["mathematical_source"] == phase["mathematical_source"], "Actual archived native build")
        native_reference_commands = {c["tag"]: c for c in ref_native["commands"]}
        require(len(native["commands"]) == len(native_reference_commands) == 4
                and {c["tag"] for c in native["commands"]} == set(native_reference_commands)
                and sum(Path(c["command"][0]).name == "pdflatex" for c in native["commands"]) == 3, "Three real TeX passes and one real PDF inspection")
        for item in native["commands"]:
            command_check(item, prefix + "native/", native_reference_commands[item["tag"]])
        native_pdf, native_aux = read(prefix + "native/main.pdf"), read(prefix + "native/main.aux")
        require(len(native_pdf) == native["pdf_bytes"] and sha(native_pdf) == native["pdf_sha256"]
                and helpers.pdf_pages(native_pdf) == native["pages"] == ref_native["pages"], "Actual native PDF bytes and independently read final page count")
        require(sha(native_aux) == native["aux_sha256"] == ref_native["aux_sha256"]
                and native["main_tex_sha256"] == expected["main.tex"]["sha256"], "Actual native auxiliary and main-source identities")
        fresh, older = [], []
        for name in names:
            if name.startswith("evidence/current-execution/historical-recovery/") and name.endswith("/REBUILD_RECEIPT.json"):
                receipt = load(name)
                if helpers.utc(receipt["started_utc"]) >= helpers.utc(phase["finished_utc"]):
                    fresh.append((name, receipt))
                else:
                    older.append({"path": name, "sha256": sha(read(name)), "started_utc": receipt["started_utc"], "success": receipt["success"]})
        require(len(fresh) == 1, "Exactly one actual post-native historical rebuild, distinct from retained old receipts")
        history_path, history = fresh[0]
        require(history["success"] and len(history["commands"]) == len(ref_history["commands"]) == 9
                and history["source_files_checked"] == ref_history["source_files_checked"] == 390
                and helpers.utc(phase["finished_utc"]) <= helpers.utc(history["started_utc"])
                <= helpers.utc(history["completed_utc"]) <= helpers.utc(log_last), "Actual current historical rebuild and job-log time interval")
        require(history["historical_whole_repository_gate_executed"] is False
                and history["mathematical_proof_certificate"] is False, "Actual historical scope is preserved")
        historical_prefix = str(PurePosixPath(history_path).parent) + "/"
        history_command_results = []
        for item, reference in zip(history["commands"], ref_history["commands"]):
            member = historical_prefix + Path(item["output"]).name
            data = read(member)
            require(item["returncode"] == 0 and helpers.file_identity(data) == item["output_identity"], "Every actual historical command output identity")
            require(helpers.normalize_command(item["argv"], article_name) == helpers.normalize_command(reference["argv"], article_name)
                    and helpers.utc(history["started_utc"]) <= helpers.utc(item["started_utc"])
                    <= helpers.utc(history["completed_utc"]), "Every actual historical command argv and timestamp")
            history_command_results.append({"argv": item["argv"], "returncode": item["returncode"],
                                            "started_utc": item["started_utc"], "output": member,
                                            "actual_output_identity": helpers.file_identity(data)})
        reference_documents = {d["document"]: d for d in ref_history["documents"]}
        require(set(reference_documents) == {"main", "supplement"} and len(history["documents"]) == 2
                and {d["document"] for d in history["documents"]} == set(reference_documents), "Both complete historical documents")
        documents = []
        for document in history["documents"]:
            name = document["document"]
            data = read("history/historical-v108/build/" + name + ".pdf")
            log = read("history/historical-v108/build/" + name + ".log")
            require(helpers.file_identity(data) == {k: document["pdf"][k] for k in ("bytes", "sha256", "git_blob")}
                    and helpers.pdf_pages(data) == document["pages"] == reference_documents[name]["pages"], "Actual historical PDF bytes and pages: " + name)
            require(helpers.file_identity(log) == {k: document["log"][k] for k in ("bytes", "sha256", "git_blob")}, "Actual historical final log: " + name)
            for kind, suffix in (("pdf", ".pdf"), ("log", ".log")):
                require(document[kind]["path"].endswith("/" + article_name + "/history/historical-v108/build/" + name + suffix),
                        "Actual historical output belongs to this article")
            documents.append({"name": name, "pages": document["pages"], "pdf": helpers.file_identity(data),
                              "log": helpers.file_identity(log), "diagnostics": document["diagnostics"]})
        post_status = read(prefix + "CI_POST_RUN_STATUS.txt").decode().splitlines()
        allowed = ["papers/" + article_name + "/" + p for p in ("build/", "history/historical-v108/build/", "evidence/current-execution/historical-recovery/")]
        require(all(len(line) >= 4 and any(line[3:].startswith(p) for p in allowed) for line in post_status), "Actual post-run changes only generated outputs")
        environment = read(prefix + "CI_ENVIRONMENT.log").decode()
        require(re.match(r"Python 3\.11\.\d+\n", environment), "Actual recorded CI Python 3.11 environment")
        requirements = checked_local(article / "requirements.txt").decode().splitlines()
        pins = [line.strip() for line in requirements if re.fullmatch(r"[A-Za-z0-9_.-]+==[^\s;]+", line.strip())]
        require(pins and all(pin in environment.splitlines() for pin in pins), "Every frozen requirement pin appears in the actual archived environment")

    require(sha(helper_path.read_bytes()) == SEALED_SHA256, "The strict verifier remains unchanged after data checks")
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    result = {
        "schema": 1, "data_checks_status": "passed", "workflow_completion_verified": False,
        "classification": "Actual artifact data verified; structured workflow completion unverified",
        "started_utc": started, "finished_utc": now(),
        "scope": "Byte/source/command/build data in the actual downloaded artifact and exact job log; not a successful full CI verification",
        "strict_full_verifier": {"source_sha256": SEALED_SHA256, "execution": identity(args.strict_execution),
                                  "exit_code": execution["exit_code"], "stderr": identity(strict_stderr),
                                  "original_gate_failure": "Actual run completed successfully", "completion_gate_changed": False},
        "run_id": run["id"], "job_id": jobs[0]["id"], "exact_head": options["--tested-commit"],
        "root_tree_sha": options["--tested-root-tree"], "article_tree_sha": options["--tested-article-tree"],
        "actual_run_status": run["status"], "actual_run_conclusion": run["conclusion"],
        "actual_job_status": jobs[0]["status"], "actual_job_conclusion": jobs[0]["conclusion"],
        "actual_job_steps": jobs[0]["steps"], "job_steps_completion_verified": False,
        "observation_identity": identity(observation_path), "synthetic_status_steps_or_timestamps_used": False,
        "actual_run_updated_at": run["updated_at"], "actual_job_log_first_timestamp": log_first,
        "actual_job_log_last_timestamp": log_last, "actual_log_identity": log_identity,
        "artifact_id": artifact["id"], "artifact_bytes": len(archive_bytes), "artifact_sha256": sha(archive_bytes),
        "artifact_member_count": len(all_entries), "artifact_file_count": len(entries), "all_member_crc_verified": True,
        "expected_file_count": len(expected), "expected_git_subtrees_reconstructed": len(trees),
        "frozen_manifest_sha256": sha(manifest_data), "manifest_schema": manifest["schema"],
        "frozen_input_count": manifest["source_count"], "frozen_input_bytes": manifest["source_bytes"],
        "immutable_anchor_count": 4, "immutable_anchor_checks": anchors,
        "distinct_original_report_count": 91, "recovered_v73_report_sha256": helpers.ORIGINAL_REPORT_SHA256,
        "mathematical_source_sha256": mathematical_sha, "native_tool_input_count": len(mathematical_rows),
        "native_core_count": len(contract["core_paths"]), "native_tex_count": len(contract["reachable"]),
        "native_label_count": len(contract["labels"]), "new_body_label_count": contract["new_body_labels"],
        "entrypoints": entrypoints, "phase_started_utc": phase["started_utc"], "phase_finished_utc": phase["finished_utc"],
        "phase_within_actual_job_log_interval_verified": True,
        "phase_within_structured_run_update_interval_verified": False,
        "mathematical_commands_verified": len(math["commands"]), "normal_optimized_pairs_verified": len(pair_results),
        "actual_math_and_native_command_checks": command_results, "actual_pair_checks": pair_results,
        "native_commands_verified": len(native["commands"]), "actual_pdflatex_passes": 3,
        "native_pages": native["pages"], "native_pdf": helpers.file_identity(native_pdf),
        "native_aux_sha256": sha(native_aux), "native_aux_matches_actual_final_local": True,
        "native_advisories": native["advisories"], "fresh_historical_receipt": history_path,
        "fresh_historical_commands_verified": len(history_command_results), "fresh_historical_source_count": history["source_files_checked"],
        "fresh_historical_command_checks": history_command_results, "historical_documents": documents,
        "historical_started_utc": history["started_utc"], "historical_completed_utc": history["completed_utc"],
        "older_historical_receipts_preserved_separately": older,
        "post_run_changed_paths": post_status, "post_run_changes_only_generated": True,
        "environment": environment, "frozen_requirement_pins_verified": pins,
        "archive_code_executed": False, "archive_extracted": False,
        "continuum_mathematical_proof_certificate": False, "independent_human_specialist_certification": False,
    }
    (output / "ARTIFACT_DATA_ONLY_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    (output / "ARTIFACT_MEMBER_IDENTITIES.json").write_text(json.dumps({"artifact_sha256": sha(archive_bytes), "files": archive_manifest}, indent=2) + "\n")
    (output / "ACTUAL_LOCAL_INPUT_IDENTITIES.json").write_text(json.dumps({"tested_commit": options["--tested-commit"],
        "files": [local_identities[key] for key in sorted(local_identities)]}, indent=2) + "\n")
    print(json.dumps({"data_checks_status": result["data_checks_status"], "workflow_completion_verified": False,
                      "result_file": str(output / "ARTIFACT_DATA_ONLY_VERIFICATION.json"),
                      "artifact_files": len(entries), "mathematical_commands_verified": len(math["commands"]),
                      "normal_optimized_pairs_verified": len(pair_results), "native_pages": native["pages"],
                      "fresh_historical_receipt": history_path}, indent=2))


if __name__ == "__main__":
    main()
