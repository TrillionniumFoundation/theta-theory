#!/usr/bin/env python3
"""Verify the downloaded prior exact-head CI artifact without executing it."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "CI_ARTIFACT_12147833077.zip"
EXPECTED_ARCHIVE = "1ba49c4be60136ddeac29138075189a16ed7ed20b92aa43d9d67e99d91d65c1f"
EXPECTED_HEAD = "878d3da9309ed7f71bce80c55cc52d96836ea920"
EXPECTED_MATH = "6a75ad99bb5034581bb5d18e0cd2a6d008d87d17a97c40e76665ab14bd1c54f7"
HIST_PREFIX = "evidence/current-execution/historical-recovery/20261018T192458932107Z/"


def require(condition, text):
    if not condition:
        raise RuntimeError(text)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", type=Path,
                    help="Complete previous native article directory")
    args = ap.parse_args()
    old = args.baseline
    if old is None:
        for parent in (ROOT, *ROOT.parents):
            candidates = [
                parent/"papers/A2-DYN-global-minimizer-localization-author-revision",
                parent/"theta-theory/papers/A2-DYN-global-minimizer-localization-author-revision",
            ]
            old = next((p for p in candidates if (p/"main.tex").is_file()), None)
            if old is not None:
                break
    require(old is not None and (old/"main.tex").is_file(),
            "complete previous source available; pass --baseline if relocated")
    data = ARCHIVE.read_bytes()
    require(sha(data) == EXPECTED_ARCHIVE, "GitHub artifact digest")
    with zipfile.ZipFile(ARCHIVE) as z:
        files = [i for i in z.infolist() if not i.is_dir()]
        require(len({i.filename for i in files}) == len(files), "unique artifact paths")
        require(all(not PurePosixPath(i.filename).is_absolute()
                    and ".." not in PurePosixPath(i.filename).parts
                    for i in files), "safe artifact paths")
        file_rows = [{"path":i.filename,"bytes":i.file_size,
                      "sha256":sha(z.read(i.filename))}
                     for i in files]
        require(z.read("build/current/CI_CHECKOUT_SHA.txt").decode().strip()
                == EXPECTED_HEAD, "actual checkout head")
        require(z.read("build/current/CI_BUILD_OUTCOME.txt").decode().strip()
                == "success", "actual build outcome")
        phase = json.loads(z.read("build/current/PHASE_all.json"))
        require(phase["status"] == "passed"
                and set(phase["completed"]) == {"source","math","typeset"},
                "all native phases passed")
        require(phase["mathematical_source"]["sha256"] == EXPECTED_MATH,
                "same mathematical source identity")
        source_rows = phase["mathematical_source"]["files"]
        for row in source_rows:
            require(sha((old / row["path"]).read_bytes()) == row["sha256"],
                    "local native source matches CI: " + row["path"])
        m = json.loads(z.read("build/current/mathematical-checks.json"))
        require(m["commands_expected"] == m["commands_completed"] == 38,
                "all expected math commands ran")
        require(not m["failures"], "no recorded math command failure")
        for cmd in m["commands"]:
            require(cmd["exit_code"] == 0, "math command exit: " + cmd["tag"])
            output = z.read("build/current/" + cmd["log"])
            require(len(output) == cmd["log_bytes"]
                    and sha(output) == cmd["log_sha256"],
                    "math command stdout identity: " + cmd["tag"])
            require(cmd["current_mathematical_source_sha256"] == EXPECTED_MATH,
                    "math command source identity: " + cmd["tag"])
        for cmp in m["normal_optimized_comparisons"]:
            suffix = ".log" if cmp["scope"] == "stdout" else ".details.json"
            left = z.read("build/current/" + cmp["program"] + "-normal" + suffix)
            right = z.read("build/current/" + cmp["program"] + "-optimized" + suffix)
            require(cmp["byte_identical"] and left == right
                    and sha(left) == cmp["sha256"], "normal/-O actual byte comparison")
        src = json.loads(z.read("build/current/source-checks.json"))
        require(src["status"] == "passed" and src["manifest"]["verified"],
                "source gate passed")
        native = json.loads(z.read("build/current/native-typeset.json"))
        require(native["status"] == "passed" and not native["layout_or_reference_problems"],
                "native document diagnostics passed")
        for cmd in native["commands"]:
            output = z.read("build/current/native/" + cmd["log"])
            require(cmd["exit_code"] == 0 and len(output) == cmd["log_bytes"]
                    and sha(output) == cmd["log_sha256"],
                    "actual native compile command and log: " + cmd["tag"])
        require(sha(z.read("build/current/native/main.pdf")) == native["pdf_sha256"],
                "actual native PDF identity")
        history = json.loads(z.read(HIST_PREFIX + "REBUILD_RECEIPT.json"))
        require(history["success"] and history["source_files_checked"] == 390
                and len(history["commands"]) == 9,
                "fresh historical assembly and nine-command build")
        for cmd in history["commands"]:
            output = z.read(HIST_PREFIX + Path(cmd["output"]).name)
            require(cmd["returncode"] == 0
                    and len(output) == cmd["output_identity"]["bytes"]
                    and sha(output) == cmd["output_identity"]["sha256"],
                    "actual historical command and log")
        for document in history["documents"]:
            name = document["document"]
            require(sha(z.read("history/historical-v108/build/" + name + ".pdf"))
                    == document["pdf"]["sha256"], "actual historical PDF identity")
        result = {
            "status": "passed",
            "scope": "Independent integrity and scope check of actual prior GitHub CI artifact; no code from archive executed",
            "observed_run_id":39151057063,
            "observed_job_id":117744614636,
            "exact_ci_head":EXPECTED_HEAD,
            "artifact_id":12147833077,
            "artifact_bytes":len(data),
            "artifact_sha256":sha(data),
            "archive_file_count":len(files),
            "mathematical_source_sha256":EXPECTED_MATH,
            "same_local_native_inputs_verified":len(source_rows),
            "phase_started_utc":phase["started_utc"],
            "phase_finished_utc":phase["finished_utc"],
            "math_commands_verified":len(m["commands"]),
            "normal_optimized_actual_output_pairs_verified":len(m["normal_optimized_comparisons"]),
            "source_manifest":src["manifest"],
            "original_reports_verified":src["original_reports_verified"],
            "reachable_native_tex":src["reachable_native_tex"],
            "current_native_pages":native["pages"],
            "current_native_pdf_sha256":native["pdf_sha256"],
            "current_aux_sha256":native["aux_sha256"],
            "native_compile_commands_verified":len(native["commands"]),
            "current_document_advisories":native["advisories"],
            "fresh_historical_receipt_path":HIST_PREFIX+"REBUILD_RECEIPT.json",
            "fresh_historical_commands_verified":len(history["commands"]),
            "fresh_historical_documents":[{"name":d["document"],"pages":d["pages"],"pdf_sha256":d["pdf"]["sha256"]} for d in history["documents"]],
            "fresh_historical_completed_utc":history["completed_utc"],
            "earlier_historical_failures_in_archive":"Retained separately; not confused with the fresh 19:24:58--19:25:17 UTC successful execution",
            "prior_native_ci_success_verified":True,
            "new_iteration_ci_success_claimed":False,
            "continuum_mathematical_proof_certificate":False,
            "independent_human_specialist_certification":False,
        }
    (ROOT/"CI_ARTIFACT_FILE_MANIFEST.json").write_text(
        json.dumps({"archive_sha256":EXPECTED_ARCHIVE,"files":file_rows},indent=2)+"\n")
    (ROOT/"PRIOR_CI_ARTIFACT_VERIFICATION.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
