#!/usr/bin/env python3
"""Parameterised r40 cold-freeze guard/publisher adapter.

This file is tooling only.  It does not contain candidate bytes and it never
creates a deliverable by default.  A configuration file supplies the fresh
r40 exact8 pins and the independently reviewed checker paths.  The adapter
loads the immutable r39 wrapper/r34 implementation in memory, binds those
pins, and fixes the inherited publication descriptor bug: the old helper
opened a newly-created file ``O_WRONLY`` and then attempted ``os.read`` on
that same descriptor.  The r40 helper uses ``O_RDWR`` so the held-descriptor
terminal replay remains possible after the 0444 mode transition.

Safety contract:

* no command-line mode is implicit; missing ``--config`` is a refusal;
* ``--preflight`` is read-only and only invokes the configured guard;
* publication additionally requires ``--publish`` and the exact
  ``CM2_R40_PUBLISH_ACK=EXACT8_MANIFEST_OUTER_LAST`` environment token;
* all target paths are derived from the supplied config and are checked for
  direct ``deliverables`` membership; no r39 target is accepted;
* this adapter does not authorize a runtime, write authority, or grant credit.

The config format is intentionally external so this adapter can be prepared
before the r40 candidate pins exist.  A typical config has the following
shape (all eight entries are required, in exact8 order)::

  {"schema":"cm2.c79g.r40.cold-freeze-config.v1",
   "base":"cm2_round306c79g_true_global_no_producer_consumer",
   "tag":"v16r2r40", "predecessor":"v16r2r39",
   "effective_checkpoint_object_sha256":"<b58>",
   "successor_checkpoint_object_sha256":"<dd9>",
   "exact8":[{"path":"deliverables/...", "file_sha256":"...",
               "object_sha256":null, "mode":292}, ...],
   "review_scripts":{"reviewer_A":"scripts/...", ...},
   "review_statuses":{"semantic_audit":"...", "path_checker":"..."}}

The config is read only; callers are responsible for producing it from the
fresh candidate review receipts.  Do not run this module merely to test its
syntax with a bytecode-generating interpreter; use ``python3 -I -B``.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from types import ModuleType
from typing import Any, Callable

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
BASE_DEFAULT = "cm2_round306c79g_true_global_no_producer_consumer"
R39_PUBLISHER = ROOT / "scripts/c79g_v16r2r39_cold_freeze_publisher.py"
R39_GUARD = ROOT / "scripts/c79g_v16r2r39_cold_freeze_guard.py"
R34_PUBLISHER = ROOT / "scripts/c79g_v16r2r34_cold_freeze_publisher.py"
R34_GUARD = ROOT / "scripts/c79g_v16r2r34_cold_freeze_guard.py"

# These are source-template pins, not candidate pins.  They make accidental
# use of a modified template fail before any subprocess or target is touched.
R39_PUBLISHER_SHA256 = "45254a830d00cce895eb0271dc74b5f55e94fbfa426ebaf90e3fcdec5fe48c50"
R39_GUARD_SHA256 = "1133e2469740bc71f2f7d77a67c7b4b4fc1dd57ac4c470793cea1939414a892b"
R34_GUARD_SHA256 = "a80e15bfc745c6a651eb2266f1ee420df68d1d6a63b759e4107e262420b3ed59"

ACK = "EXACT8_MANIFEST_OUTER_LAST"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ConfigError(ValueError):
    """A malformed or unsafe adapter configuration."""


def _strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise ConfigError(f"duplicate config key:{key}")
        out[key] = value
    return out


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_text_pinned(path: Path, expected_sha: str) -> str:
    raw = path.read_bytes()
    if _sha(raw) != expected_sha:
        raise ConfigError(f"template source hash drift:{path}")
    return raw.decode("utf-8")


@dataclass(frozen=True)
class Pin:
    relative: str
    file_sha256: str
    object_sha256: str | None
    initial_mode: int


@dataclass(frozen=True)
class Config:
    config_path: Path
    base: str
    tag: str
    predecessor: str
    checkpoint: str
    successor: str
    exact8: tuple[Pin, ...]
    review_scripts: dict[str, str]
    review_statuses: dict[str, str]
    evidence_receipts: dict[str, str]
    evidence_statuses: dict[str, str]
    c53_file_sha256: str
    c53_object_sha256: str
    guard_check_count: int

    @property
    def manifest_rel(self) -> str:
        return f"deliverables/{self.base}_cold_launch_manifest_{self.tag}.sha256"

    @property
    def outer_rel(self) -> str:
        return f"deliverables/{self.base}_cold_launch_outer_receipt_{self.tag}.json"

    @property
    def guard_rel(self) -> str:
        return f"scripts/c79g_v16r2{self.tag.removeprefix('v16r2')}_cold_freeze_guard.py"


def _direct_deliverable(path: str, *, allow_predecessor_r39: bool = False,
                        allow_manifest_outer: bool = False) -> None:
    parts = Path(path).parts
    if len(parts) != 2 or parts[0] != "deliverables":
        raise ConfigError(f"non-direct-deliverable path:{path}")
    if "v16r2r39" in path and not allow_predecessor_r39:
        raise ConfigError(f"r39 path cannot be rebound into r40:{path}")
    if not allow_manifest_outer and ("cold_launch_manifest" in path or
                                     "cold_launch_outer_receipt" in path):
        raise ConfigError(f"manifest/outer cannot be exact8:{path}")


def load_config(path: Path) -> Config:
    """Read and validate a fresh candidate config without writing anything."""
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"invalid config JSON:{path}") from exc
    if not isinstance(value, dict):
        raise ConfigError("config object required")
    if value.get("schema") != "cm2.c79g.r40.cold-freeze-config.v1":
        raise ConfigError("unexpected config schema")
    base = value.get("base")
    tag = value.get("tag")
    predecessor = value.get("predecessor")
    if base != BASE_DEFAULT:
        raise ConfigError("unexpected base")
    if (not isinstance(tag, str) or not re.fullmatch(r"v16r2r(4[0-9]|[5-9][0-9])", tag)
            or tag == "v16r2r39"):
        raise ConfigError(f"fresh r40+ tag required:{tag!r}")
    if (not isinstance(predecessor, str) or predecessor == tag or
            not re.fullmatch(r"v16r2r[0-9]+", predecessor)):
        raise ConfigError("invalid predecessor")
    checkpoint = value.get("effective_checkpoint_object_sha256")
    successor = value.get("successor_checkpoint_object_sha256")
    if not isinstance(checkpoint, str) or not HEX64.fullmatch(checkpoint):
        raise ConfigError("effective checkpoint pin shape")
    if not isinstance(successor, str) or not HEX64.fullmatch(successor):
        raise ConfigError("successor checkpoint pin shape")

    rows = value.get("exact8")
    if not isinstance(rows, list) or len(rows) != 8:
        raise ConfigError("exact8 must contain exactly eight entries")
    pins: list[Pin] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ConfigError(f"exact8[{index}] object required")
        rel = row.get("path")
        file_pin = row.get("file_sha256")
        object_pin = row.get("object_sha256")
        mode = row.get("mode")
        if not isinstance(rel, str):
            raise ConfigError(f"exact8[{index}] path")
        _direct_deliverable(rel, allow_predecessor_r39=(index == 5))
        if rel in seen:
            raise ConfigError(f"exact8 duplicate:{rel}")
        seen.add(rel)
        if not isinstance(file_pin, str) or not HEX64.fullmatch(file_pin):
            raise ConfigError(f"exact8[{index}] file pin")
        if object_pin is not None and (not isinstance(object_pin, str) or
                                        not HEX64.fullmatch(object_pin)):
            raise ConfigError(f"exact8[{index}] object pin")
        if mode not in (0o444, 0o664):
            raise ConfigError(f"exact8[{index}] mode")
        pins.append(Pin(rel, file_pin, object_pin, mode))
    # The exact8 order is part of the protocol, not just a count check.
    if not pins[0].relative.endswith("_active_predecessor_supersession_receipt_v1.json"):
        raise ConfigError("exact8[0] must be active predecessor anchor")
    if not pins[1].relative.endswith(f"_schema_{tag}.json"):
        raise ConfigError("exact8[1] must be schema")
    if not pins[2].relative.endswith(f"_contract_{tag}.json"):
        raise ConfigError("exact8[2] must be contract")
    if not pins[3].relative.endswith(f"_{tag}_semantic_source.py"):
        raise ConfigError("exact8[3] must be producer source")
    if not pins[4].relative.endswith(
            f"_independent_verifier_assembler_authority_consumer_{tag}_semantic_source.py"):
        raise ConfigError("exact8[4] must be consumer source")
    if not pins[5].relative.endswith(
            f"_{predecessor}_to_{tag}_static_launch_transition_receipt_v1.json"):
        raise ConfigError("exact8[5] must be transition")
    if not pins[6].relative.endswith(f"_static_audit_{tag}.json"):
        raise ConfigError("exact8[6] must be audit")
    if not pins[7].relative.endswith(f"_cold_launch_{tag}_semantic_source.py"):
        raise ConfigError("exact8[7] must be launcher source")

    scripts = value.get("review_scripts", {})
    statuses = value.get("review_statuses", {})
    if not isinstance(scripts, dict) or not isinstance(statuses, dict):
        raise ConfigError("review scripts/statuses objects required")
    required_scripts = ("guard", "reviewer_A", "checker_B", "semantic_audit", "path_checker")
    required_statuses = ("semantic_audit", "path_checker")
    for key in required_scripts:
        val = scripts.get(key)
        if not isinstance(val, str) or not val.endswith(".py"):
            raise ConfigError(f"missing review script:{key}")
        # Scripts are read-only tools and must remain inside this workspace.
        if Path(val).is_absolute() or ".." in Path(val).parts:
            raise ConfigError(f"unsafe review script path:{val}")
    for key in required_statuses:
        if not isinstance(statuses.get(key), str) or not statuses[key]:
            raise ConfigError(f"missing review status:{key}")
    receipts = value.get("evidence_receipts", {})
    if not isinstance(receipts, dict):
        raise ConfigError("evidence_receipts object required")
    for key in ("no_producer", "mutation_attacks", "terminal_replay"):
        rel = receipts.get(key)
        if not isinstance(rel, str):
            raise ConfigError(f"missing evidence receipt:{key}")
        # Side evidence is regenerated for r40; only the exact8 transition
        # member may legitimately contain the predecessor suffix r39.
        _direct_deliverable(rel)
    evidence_statuses = value.get("evidence_statuses", {})
    if not isinstance(evidence_statuses, dict):
        raise ConfigError("evidence_statuses object required")
    for key in ("no_producer", "mutation_attacks", "terminal_replay"):
        if not isinstance(evidence_statuses.get(key), str) or not evidence_statuses[key]:
            raise ConfigError(f"missing evidence status:{key}")
    c53_file = value.get("c53_file_sha256")
    c53_obj = value.get("c53_object_sha256")
    if not isinstance(c53_file, str) or not HEX64.fullmatch(c53_file):
        raise ConfigError("C53 file pin shape")
    if not isinstance(c53_obj, str) or not HEX64.fullmatch(c53_obj):
        raise ConfigError("C53 object pin shape")
    count = value.get("guard_check_count", 7)
    if not isinstance(count, int) or count < 1 or count > 64:
        raise ConfigError("guard check count")
    return Config(path.resolve(), base, tag, predecessor, checkpoint, successor,
                  tuple(pins), dict(scripts), dict(statuses), dict(receipts),
                  dict(evidence_statuses), c53_file, c53_obj, count)


def _load_module(path: Path, name: str, expected_sha: str | None = None) -> ModuleType:
    text = path.read_text(encoding="utf-8")
    if expected_sha is not None and _sha(text.encode("utf-8")) != expected_sha:
        raise ConfigError(f"template source hash drift:{path}")
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = None
    sys.modules[name] = module
    exec(compile(text, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def _stable_read_fd(fd: int, expected: bytes) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        chunks.append(block)
    value = b"".join(chunks)
    os.lseek(fd, 0, os.SEEK_SET)
    if value != expected:
        raise RuntimeError("published bytes replay mismatch")
    return value


def fixed_create_exclusive(module: ModuleType) -> Callable[..., tuple[int, os.stat_result]]:
    """Return the corrected same-FD O_RDWR publication helper."""
    def create_exclusive(out_fd: int, relative: str, raw: bytes):
        rel = Path(relative)
        if rel.parts[:1] != ("deliverables",) or len(rel.parts) != 2:
            raise RuntimeError("publication path is not direct deliverables member")
        name = rel.name
        fd = os.open(name,
                     os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                     getattr(os, "O_NOFOLLOW", 0), 0o444, dir_fd=out_fd)
        try:
            offset = 0
            view = memoryview(raw)
            while offset < len(view):
                count = os.write(fd, view[offset:])
                if count <= 0:
                    raise RuntimeError(f"short write:{relative}")
                offset += count
            os.fsync(fd)
            os.fchmod(fd, 0o444)
            os.fsync(fd)
            os.fsync(out_fd)
            state = os.fstat(fd)
            named = os.stat(name, dir_fd=out_fd, follow_symlinks=False)
            identity = module.identity
            if (not stat.S_ISREG(state.st_mode) or state.st_nlink != 1 or
                    stat.S_IMODE(state.st_mode) != 0o444 or
                    identity(state) != identity(named)):
                raise RuntimeError(f"published identity:{relative}")
            _stable_read_fd(fd, raw)
            return fd, state
        except BaseException:
            os.close(fd)
            raise
    return create_exclusive


def _configured_exact8(module: ModuleType, cfg: Config):
    return tuple(module.Pin(p.relative, p.file_sha256, p.object_sha256,
                            p.initial_mode) for p in cfg.exact8)


def load_publisher(cfg: Config) -> ModuleType:
    """Load r39 wrapper/r34 core and bind a fresh config in memory."""
    wrapper = _load_module(R39_PUBLISHER, "_r40_r39_publisher_wrapper",
                           R39_PUBLISHER_SHA256)
    core = wrapper.load_template()  # r39's immutable in-memory r34 core
    core.TAG = cfg.tag
    core.PREV = cfg.predecessor
    core.CHECKPOINT = cfg.checkpoint
    core.SUCCESSOR_CHECKPOINT = cfg.successor
    core.EXACT8 = _configured_exact8(core, cfg)
    core.SOURCE_PATHS = frozenset(pin.relative for pin in core.EXACT8
                                  if pin.relative.endswith(".py"))
    core.MANIFEST_REL = cfg.manifest_rel
    core.OUTER_REL = cfg.outer_rel
    core.MANIFEST = ROOT / cfg.manifest_rel
    core.OUTER = ROOT / cfg.outer_rel
    core.GUARD = ROOT / cfg.review_scripts.get("guard", "scripts/c79g_v16r2r40_cold_freeze_guard.py")
    core.create_exclusive = fixed_create_exclusive(core)
    # The caller binds run_guard below; this avoids executing a stale r39
    # guard that would point at r34 status strings and paths.
    return core


def _guard_command(cfg: Config) -> list[str]:
    guard = cfg.review_scripts.get("guard")
    if not isinstance(guard, str):
        raise ConfigError("review_scripts.guard is required for publication")
    path = ROOT / guard
    return ["/usr/bin/python3", "-I", "-B", str(path), "--config", str(cfg.config_path)]


def bind_run_guard(module: ModuleType, cfg: Config) -> None:
    """Bind a strict, config-aware read-only guard subprocess to publisher."""
    def run_guard() -> tuple[dict[str, Any], bytes]:
        env = dict(os.environ)
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                    "PYTHONHASHSEED": "1", "CM2_R40_CONFIG": str(cfg.config_path),
                    "CM2_SUCCESSOR_SUFFIX": cfg.tag,
                    "CM2_PREDECESSOR_SUFFIX": cfg.predecessor})
        proc = subprocess.run(_guard_command(cfg), cwd=str(ROOT), env=env,
                              capture_output=True, check=False)
        raw = proc.stdout
        if proc.returncode != 0:
            raise RuntimeError(f"r40 guard rc={proc.returncode}:{proc.stderr[-600:]!r}")
        try:
            report = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise RuntimeError("r40 guard did not emit one JSON object") from exc
        if not isinstance(report, dict):
            raise RuntimeError("r40 guard report object required")
        required = {
            "read_only": True, "formal_global_closure_credit": 0,
            "D02_unlock": False, "runtime_authorized": False,
            "manifest_created": False, "outer_created": False,
            "failed_check_count": 0,
        }
        if any(report.get(k) != v for k, v in required.items()):
            raise RuntimeError("r40 guard zero-credit/read-only predicate failed")
        if report.get("check_count") != cfg.guard_check_count:
            raise RuntimeError("r40 guard check count mismatch")
        rows = report.get("exact8")
        expected = [{"path": p.relative, "file_sha256": p.file_sha256,
                     "object_sha256": p.object_sha256, "mode": p.initial_mode}
                    for p in cfg.exact8]
        if rows != expected:
            raise RuntimeError("r40 guard exact8 report mismatch")
        return report, raw
    module.run_guard = run_guard


def build_publisher(cfg: Config) -> ModuleType:
    module = load_publisher(cfg)
    bind_run_guard(module, cfg)
    return module


def _guard_source_transform(cfg: Config) -> str:
    """Return r34 guard source with candidate-specific checker paths/statuses.

    This is deliberately an in-memory transform; it is used by the guard
    entrypoint and never written back to either r39 or r34 source.
    """
    text = _read_text_pinned(R34_GUARD, R34_GUARD_SHA256)
    replacements = {
        "scripts/c79g_v16r2r20_independent_reviewer.py": cfg.review_scripts["reviewer_A"],
        "scripts/c79g_v16r2r23_structure_checker_b.py": cfg.review_scripts["checker_B"],
        "scripts/c79g_v16r2r34_runtime_semantic_audit.py": cfg.review_scripts["semantic_audit"],
        "scripts/c79g_v16r2r34_path_successor_checker.py": cfg.review_scripts["path_checker"],
        '"PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT"':
            json.dumps(cfg.review_statuses["semantic_audit"]),
        '"PASS_R34_PATCH_SPEC_CHECK__ZERO_CREDIT"':
            json.dumps(cfg.review_statuses["path_checker"]),
        '"PREFLIGHT_PASS_R34_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT"':
            json.dumps(f"PREFLIGHT_PASS_{cfg.tag.upper()}_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT"),
        '"PREFLIGHT_FAIL_CLOSED_R34_COLD_FREEZE_GUARD"':
            json.dumps(f"PREFLIGHT_FAIL_CLOSED_{cfg.tag.upper()}_COLD_FREEZE_GUARD"),
        '"PREFLIGHT_FAIL_CLOSED_R34_COLD_FREEZE_GUARD_EXCEPTION"':
            json.dumps(f"PREFLIGHT_FAIL_CLOSED_{cfg.tag.upper()}_COLD_FREEZE_GUARD_EXCEPTION"),
        '"no_r34_pyc"': '"no_tagged_pyc"',
    }
    # The three side-receipt status strings are candidate-specific too.  They
    # are supplied by the independently sealed evidence config rather than
    # inferred from the r34 template.
    for old, key in (
        ('PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT',
         "no_producer"),
        ('PASS_READ_ONLY_MUTATION_ATTACKS__13_OF_13_FAIL_CLOSED__ZERO_CREDIT',
         "mutation_attacks"),
        ('PASS_DUAL_INDEPENDENT_CHECKERS_AND_TERMINAL_BYTE_REPLAY__ZERO_CREDIT',
         "terminal_replay"),
    ):
        literal = json.dumps(old)
        new_literal = json.dumps(cfg.evidence_statuses[key])
        if text.count(literal) == 0:
            raise ConfigError(f"guard evidence status literal missing:{old}")
        text = text.replace(literal, new_literal)
    for old, new in replacements.items():
        if text.count(old) == 0:
            raise ConfigError(f"guard template literal missing:{old}")
        text = text.replace(old, new)
    return text


def build_guard(cfg: Config) -> ModuleType:
    """Load a candidate-specific guard entirely in memory."""
    # Load the r39 wrapper first so the adapter's provenance is the same
    # append-only r39 template chain used by the publisher.  Its inner r34
    # module is discarded; the pinned source is transformed below without
    # writing either template back to disk.
    wrapper = _load_module(R39_GUARD, "_r40_r39_guard_wrapper",
                           R39_GUARD_SHA256)
    wrapper.load_template()
    text = _guard_source_transform(cfg)
    module = ModuleType("_r40_guard")
    module.__file__ = str(ROOT / "scripts/c79g_v16r2r40_cold_freeze_guard.py")
    module.__package__ = None
    sys.modules[module.__name__] = module
    exec(compile(text, str(R34_GUARD), "exec"), module.__dict__, module.__dict__)
    module.BASE = cfg.base
    module.TAG = cfg.tag
    module.PREV = cfg.predecessor
    module.CHECKPOINT = cfg.checkpoint
    module.SUCCESSOR_CHECKPOINT = cfg.successor
    module.PINS_PENDING = True
    module.ONE_SHOT_FREEZE_PUBLISH_ENABLED = False
    module.EXACT8 = tuple((p.relative, p.file_sha256, p.object_sha256,
                           p.initial_mode) for p in cfg.exact8)
    module.RECEIPTS = {key: ROOT / rel for key, rel in cfg.evidence_receipts.items()}
    module.C53_FILE_SHA256 = cfg.c53_file_sha256
    module.C53_OBJECT_SHA256 = cfg.c53_object_sha256
    return module


def guard_entrypoint(config_path: Path, argv: list[str]) -> int:
    cfg = load_config(config_path)
    if argv not in ([], ["--preflight"]):
        raise ConfigError("guard accepts only --preflight")
    # Build, but do not publish; caller may use this function from a wrapper
    # that executes the in-memory module.  The CLI wrapper below does so.
    module = build_guard(cfg)
    return int(module.main())


def publisher_entrypoint(config_path: Path, publish: bool) -> int:
    cfg = load_config(config_path)
    if not publish:
        raise ConfigError("publisher refuses without --publish")
    if os.environ.get("CM2_R40_PUBLISH_ACK") != ACK:
        raise ConfigError("missing CM2_R40_PUBLISH_ACK exact token")
    module = build_publisher(cfg)
    return int(module.main())


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    if args.preflight and args.publish:
        raise ConfigError("choose one mode")
    if args.preflight:
        return guard_entrypoint(args.config, ["--preflight"])
    if args.publish:
        return publisher_entrypoint(args.config, True)
    raise ConfigError("explicit --preflight or --publish required")


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except Exception as exc:
        # No output surface is created on configuration refusal.  A compact
        # stderr diagnostic is useful to the caller and remains fail-closed.
        print(f"R40_ADAPTER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
