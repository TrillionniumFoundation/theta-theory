#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import os
import shutil
import stat
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path


SH_TZ = timezone(timedelta(hours=8))


def human_bytes(n: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(n)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{n} B"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def apparent_size(path: Path) -> int:
    total = 0
    if path.is_file():
        return path.stat().st_size
    if not path.exists():
        return 0
    for root, _, files in os.walk(path):
        for name in files:
            p = Path(root) / name
            try:
                total += p.stat().st_size
            except FileNotFoundError:
                pass
    return total


def active_dataset_audit(data_root: Path) -> dict:
    files = 0
    dirs = 0
    bytes_total = 0
    symlinks = 0
    broken_entries = 0
    rsync_partials = 0
    dedup_residue = 0
    for root, dirnames, filenames in os.walk(data_root, topdown=True):
        dirnames[:] = [d for d in dirnames if d != "_control"]
        dirs += len(dirnames)
        for name in filenames:
            p = Path(root) / name
            try:
                st = p.lstat()
            except FileNotFoundError:
                broken_entries += 1
                continue
            if stat.S_ISLNK(st.st_mode):
                symlinks += 1
                continue
            files += 1
            bytes_total += st.st_size
            if ".rsync-partial" in p.parts or name.endswith(".partial"):
                rsync_partials += 1
            if name.endswith(".dedup") or name.endswith(".dedup.tmp"):
                dedup_residue += 1
    return {
        "payload_files": files,
        "payload_dirs": dirs,
        "payload_bytes": bytes_total,
        "payload_human": human_bytes(bytes_total),
        "symlinks": symlinks,
        "broken_entries": broken_entries,
        "rsync_partial_files": rsync_partials,
        "dedup_residue_files": dedup_residue,
    }


def find_latest(control_dir: Path, prefix: str) -> Path | None:
    candidates = [p for p in control_dir.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


def source_disk_status() -> dict:
    mount_line = ""
    mounted_ro = None
    try:
        with open("/proc/mounts", "r", encoding="utf-8") as fh:
            for line in fh:
                if "/media/qian-qi/TOSHIBA_CLEAN2" in line or line.startswith("/dev/sdc1 "):
                    mount_line = line.strip()
                    fields = line.split()
                    if len(fields) >= 4:
                        mounted_ro = "ro" in fields[3].split(",")
                    break
    except OSError:
        pass

    sys_ro = None
    ro_path = Path("/sys/block/sdc/sdc1/ro")
    if ro_path.exists():
        try:
            sys_ro = ro_path.read_text(encoding="utf-8").strip()
        except OSError:
            sys_ro = None

    return {
        "device": "/dev/sdc1",
        "mount_line": mount_line,
        "mounted_read_only": mounted_ro,
        "sys_block_ro": sys_ro,
    }


def docker_sql_status() -> dict:
    try:
        out = subprocess.check_output(
            ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return {"docker_checked": False, "matching_containers": []}
    matches = []
    for line in out.splitlines():
        lower = line.lower()
        if "oc_sqlschema" in lower or "mssql" in lower or "sqlserver" in lower:
            matches.append(line)
    return {"docker_checked": True, "matching_containers": matches}


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="/data/toshiba_clean2_data_clear/database")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    data_root = Path(args.data_root)
    control_dir = data_root / "_control"
    now = datetime.now(SH_TZ)
    stamp = now.strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out) if args.out else control_dir / f"final_checkpoint_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    panel_package = find_latest(control_dir, "panel_analysis_package_")
    db_report = find_latest(control_dir, "db_source_profile_report_")
    panel_summary = read_json(panel_package / "PACKAGE_SUMMARY.json") if panel_package else {}
    db_summary = read_json(db_report / "DB_SOURCE_PROFILE_SUMMARY.json") if db_report else {}

    active = active_dataset_audit(data_root)
    disk = shutil.disk_usage("/data")
    disk_status = {
        "path": "/data",
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "free_human": human_bytes(disk.free),
    }
    source_status = source_disk_status()
    docker_status = docker_sql_status()

    deliverables = []
    if panel_package:
        deliverables.append({
            "name": "panel_analysis_package_strict_v2",
            "path": str(panel_package),
            "kind": "privacy_safe_panel_package",
            "bytes": apparent_size(panel_package),
            "status": panel_summary.get("status", "unknown"),
            "notes": "Final strict v2 event/source appearance panel package; HMAC key is not copied into package.",
        })
    if db_report:
        deliverables.append({
            "name": "db_source_profile_report",
            "path": str(db_report),
            "kind": "schema_only_db_backup_profile",
            "bytes": apparent_size(db_report),
            "status": db_summary.get("status", "unknown"),
            "notes": "Schema/catalog and row-count estimates only; raw-like column names redacted.",
        })

    hmac_ref = panel_summary.get("hmac_key_reference", {})
    hmac_path = Path(hmac_ref.get("path", "")) if hmac_ref.get("path") else None
    key_status = {
        "hmac_key_path": str(hmac_path) if hmac_path else "",
        "hmac_key_exists": bool(hmac_path and hmac_path.exists()),
        "hmac_key_mode_octal": hmac_ref.get("mode_octal", ""),
        "copied_to_panel_package": hmac_ref.get("copied_to_package", None),
    }

    summary = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "out": str(out_dir),
        "active_dataset": active,
        "disk": disk_status,
        "source_disk": source_status,
        "docker_sql_status": docker_status,
        "panel_package": {
            "path": str(panel_package) if panel_package else "",
            "summary": panel_summary,
        },
        "db_source_profile_report": {
            "path": str(db_report) if db_report else "",
            "summary": db_summary,
        },
        "hmac_key_status": key_status,
        "status": "complete",
    }

    with (out_dir / "FINAL_CHECKPOINT_SUMMARY.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    write_tsv(out_dir / "DELIVERABLES.tsv", ["name", "kind", "status", "bytes", "path", "notes"], deliverables)
    write_tsv(out_dir / "ACTIVE_DATASET_AUDIT.tsv", ["metric", "value"], [
        {"metric": key, "value": value} for key, value in active.items()
    ])

    next_steps = [
        "# Next-step decision checkpoint",
        "",
        "## Current conclusion",
        "",
        "- The strict v2 panel package is the current clean analysis checkpoint.",
        "- DB/backup sources that could be restored/read on this host look more like static entity/source-presence data than strict event panel data.",
        "- QQ MDF files are SQL Server database version 539 and need a legacy SQL Server upgrade/export path before schema-only analysis can continue.",
        "",
        "## Recommended branch",
        "",
        "1. Preserve the panel analysis package, DB source profile report, and the HMAC key reference path.",
        "2. Do not merge MDB/BAK registry-like sources into the strict event panel without external source dates or validated event-time semantics.",
        "3. Treat QQ MDF as a separate optional project: legacy SQL Server schema-only export first, no payload row export.",
        "4. If space cleanup is needed, create a separate dry-run cleanup manifest for redundant prototype/profile directories before deletion.",
        "",
        "## Privacy posture",
        "",
        "- This checkpoint contains metadata, counts, paths, package summaries, and hashes only.",
        "- It does not include raw payload rows or raw entity values.",
    ]
    (out_dir / "NEXT_STEP_DECISION.md").write_text("\n".join(next_steps) + "\n", encoding="utf-8")

    readme = [
        "# Final Checkpoint",
        "",
        f"Generated at: {summary['generated_at']}",
        "",
        "This checkpoint summarizes the current SSD active dataset, final privacy-safe panel package, DB/backup source profile report, and current safety status.",
        "",
        "## Active Dataset",
        "",
        f"- Files: {active['payload_files']}",
        f"- Apparent bytes: {active['payload_bytes']} ({active['payload_human']})",
        f"- Symlinks: {active['symlinks']}",
        f"- Broken entries: {active['broken_entries']}",
        f"- rsync partial files: {active['rsync_partial_files']}",
        f"- .dedup residue files: {active['dedup_residue_files']}",
        "",
        "## Deliverables",
        "",
    ]
    for row in deliverables:
        readme.extend([
            f"- {row['name']}: {row['path']}",
            f"  - kind: {row['kind']}",
            f"  - status: {row['status']}",
            f"  - size: {human_bytes(int(row['bytes']))}",
        ])
    readme.extend([
        "",
        "## Safety Status",
        "",
        f"- Source disk mount: `{source_status.get('mount_line', '')}`",
        f"- Source sysfs RO: `{source_status.get('sys_block_ro', '')}`",
        f"- SQL staging containers matching mssql/sqlserver: {len(docker_status.get('matching_containers', []))}",
        f"- /data free: {disk_status['free_human']}",
    ])
    (out_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    manifest_rows = []
    for p in sorted(out_dir.iterdir()):
        if not p.is_file() or p.name == "PACKAGE_MANIFEST.tsv":
            continue
        manifest_rows.append({
            "path": p.name,
            "size": p.stat().st_size,
            "sha256": sha256_file(p),
        })
    write_tsv(out_dir / "PACKAGE_MANIFEST.tsv", ["path", "size", "sha256"], manifest_rows)

    print(json.dumps({
        "out": str(out_dir),
        "active_files": active["payload_files"],
        "active_bytes": active["payload_bytes"],
        "deliverables": len(deliverables),
        "manifest_files": len(manifest_rows),
        "source_ro": source_status.get("sys_block_ro"),
        "sql_containers": len(docker_status.get("matching_containers", [])),
        "status": "complete",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
