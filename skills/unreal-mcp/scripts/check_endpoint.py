#!/usr/bin/env python3
"""Verify that Codex and a live Unreal Editor agree on one MCP endpoint."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse


SETTINGS_SECTION = "/Script/ModelContextProtocolEngine.ModelContextProtocolSettings"
START_RE = re.compile(r"Starting MCP server on port\s+(\d+)", re.IGNORECASE)
LISTENER_LOG_RE = re.compile(
    r"Created new HttpListener on\s+([^\s:]+):(\d+)", re.IGNORECASE
)
NETSTAT_RE = re.compile(
    r"^\s*TCP\s+(\S+):(\d+)\s+\S+\s+LISTENING\s+(\d+)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _collect_json_urls(value: object, prefix: tuple[str, ...] = ()) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = (*prefix, str(key))
            if key == "url" and isinstance(child, str) and child.startswith(("http://", "https://")):
                found.append((".".join(child_prefix), child))
            else:
                found.extend(_collect_json_urls(child, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_collect_json_urls(child, (*prefix, str(index))))
    return found


def _read_client_urls(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(_read_text(path))
        pairs = _collect_json_urls(payload)
    elif suffix == ".toml":
        try:
            import tomllib
        except ImportError as exc:  # pragma: no cover - Python 3.11+ is expected
            raise RuntimeError("Python 3.11 or newer is required for TOML config.") from exc
        payload = tomllib.loads(_read_text(path))
        pairs = _collect_json_urls(payload)
    else:
        raise ValueError(f"Unsupported client config format: {path}")

    unreal_urls = [url for key, url in pairs if "unreal" in key.lower()]
    return unreal_urls or [url for _, url in pairs if urlparse(url).path.rstrip("/") == "/mcp"]


def _parse_unreal_settings(path: Path) -> dict[str, object]:
    text = _read_text(path)
    section_pattern = re.compile(
        rf"(?ms)^\[{re.escape(SETTINGS_SECTION)}\]\s*(.*?)(?=^\[|\Z)"
    )
    match = section_pattern.search(text)
    if not match:
        return {}

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if "=" not in line or line.lstrip().startswith(("#", ";")):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    port_text = values.get("ServerPortNumber", "")
    return {
        "port": int(port_text) if port_text.isdigit() else None,
        "path": values.get("ServerUrlPath"),
        "auto_start": values.get("bAutoStartServer", "").lower() == "true",
        "tool_search": values.get("bEnableToolSearch", "").lower() == "true",
    }


def _latest_project_log(project_root: Path, project_name: str) -> Path | None:
    log_dir = project_root / "Saved" / "Logs"
    preferred = log_dir / f"{project_name}.log"
    if preferred.is_file():
        return preferred
    logs = sorted(
        (path for path in log_dir.glob("*.log") if not path.name.lower().startswith("cef")),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return logs[0] if logs else None


def _parse_latest_log_endpoint(path: Path) -> dict[str, object]:
    text = _read_text(path)
    starts = START_RE.findall(text)
    listeners = LISTENER_LOG_RE.findall(text)
    return {
        "start_port": int(starts[-1]) if starts else None,
        "listener_host": listeners[-1][0] if listeners else None,
        "listener_port": int(listeners[-1][1]) if listeners else None,
    }


def _run_netstat() -> str:
    completed = subprocess.run(
        ["netstat", "-ano", "-p", "tcp"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def _listeners(netstat_text: str) -> list[dict[str, object]]:
    return [
        {"host": host, "port": int(port), "pid": int(pid)}
        for host, port, pid in NETSTAT_RE.findall(netstat_text)
    ]


def _process_name(pid: int) -> str | None:
    completed = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    rows = list(csv.reader(line for line in completed.stdout.splitlines() if line.strip()))
    if not rows or not rows[0]:
        return None
    name = rows[0][0].strip()
    return name if name.lower().endswith(".exe") else None


def _discover_client_configs(project_root: Path, script_path: Path) -> list[Path]:
    plugin_root = script_path.resolve().parents[3]
    candidates = [
        project_root / ".mcp.json",
        project_root / ".codex" / "config.toml",
        plugin_root / ".mcp.json",
    ]
    return [path for path in candidates if path.is_file()]


def inspect_endpoint(
    project_root: Path,
    *,
    client_configs: list[Path] | None = None,
    log_path: Path | None = None,
    netstat_text: str | None = None,
    process_name_lookup: Callable[[int], str | None] = _process_name,
    script_path: Path = Path(__file__),
) -> dict[str, object]:
    project_root = project_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    projects = sorted(project_root.glob("*.uproject"))
    if len(projects) != 1:
        errors.append(
            f"Expected exactly one .uproject in {project_root}; found {len(projects)}."
        )
        project_name = project_root.name
    else:
        project_name = projects[0].stem

    config_paths = client_configs or _discover_client_configs(project_root, script_path)
    client_evidence: list[dict[str, object]] = []
    for config_path in config_paths:
        try:
            urls = _read_client_urls(config_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"Could not read client config {config_path}: {exc}")
            continue
        client_evidence.append({"path": str(config_path.resolve()), "urls": urls})

    all_urls = sorted(
        {url for item in client_evidence for url in item["urls"]}  # type: ignore[index]
    )
    if not all_urls:
        errors.append("No Unreal HTTP MCP URL was found in the client configuration.")
        endpoint = None
    elif len(all_urls) > 1:
        errors.append(f"Client configurations disagree on the MCP URL: {all_urls}")
        endpoint = None
    else:
        endpoint = urlparse(all_urls[0])
        if endpoint.scheme != "http" or not endpoint.hostname or not endpoint.port:
            errors.append(f"Client MCP URL is not an explicit HTTP host and port: {all_urls[0]}")

    ini_path = (
        project_root
        / "Saved"
        / "Config"
        / "WindowsEditor"
        / "EditorPerProjectUserSettings.ini"
    )
    settings = _parse_unreal_settings(ini_path) if ini_path.is_file() else {}
    if not settings:
        errors.append(f"Unreal MCP settings section was not found in {ini_path}.")

    effective_log = log_path or _latest_project_log(project_root, project_name)
    log_evidence = (
        _parse_latest_log_endpoint(effective_log)
        if effective_log is not None and effective_log.is_file()
        else {}
    )
    if not log_evidence:
        errors.append("No readable Unreal project log was found.")

    listener_rows = _listeners(netstat_text if netstat_text is not None else _run_netstat())
    expected_port = endpoint.port if endpoint and endpoint.port else None
    expected_host = endpoint.hostname if endpoint else None
    expected_path = endpoint.path if endpoint else None

    if expected_port is not None and settings.get("port") != expected_port:
        errors.append(
            f"Unreal setting port {settings.get('port')} does not match client port {expected_port}."
        )
    if expected_path is not None and settings.get("path") != expected_path:
        errors.append(
            f"Unreal setting path {settings.get('path')} does not match client path {expected_path}."
        )
    if expected_port is not None and log_evidence.get("start_port") != expected_port:
        errors.append(
            f"Latest log start port {log_evidence.get('start_port')} does not match client port {expected_port}."
        )
    if expected_port is not None and log_evidence.get("listener_port") != expected_port:
        errors.append(
            f"Latest log listener port {log_evidence.get('listener_port')} does not match client port {expected_port}."
        )

    matching = [
        row
        for row in listener_rows
        if row["port"] == expected_port
        and (
            row["host"] == expected_host
            or {str(row["host"]), str(expected_host)} <= {"127.0.0.1", "localhost"}
        )
    ]
    owner: dict[str, object] | None = None
    if expected_port is not None and not matching:
        errors.append(f"No active TCP listener matches {expected_host}:{expected_port}.")
    elif matching:
        if len(matching) > 1:
            warnings.append(f"Multiple matching listeners were found: {matching}")
        listener = matching[0]
        owner_name = process_name_lookup(int(listener["pid"]))
        owner = {**listener, "process_name": owner_name}
        if not owner_name or "unrealeditor" not in owner_name.lower():
            errors.append(
                f"Listener {expected_host}:{expected_port} is owned by {owner_name or 'an unknown process'} "
                f"(PID {listener['pid']}), not UnrealEditor."
            )

    if not settings.get("auto_start"):
        warnings.append(
            "bAutoStartServer is not true; explicit launch arguments are required on restart."
        )

    runtime_ready = not errors
    return {
        "schema_version": 1,
        "project_root": str(project_root),
        "client_configs": client_evidence,
        "client_url": all_urls[0] if len(all_urls) == 1 else None,
        "unreal_settings": {"config_path": str(ini_path), **settings},
        "unreal_log": {
            "path": str(effective_log.resolve()) if effective_log else None,
            **log_evidence,
        },
        "listener_owner": owner,
        "runtime_endpoint_verdict": "PASS" if runtime_ready else "FAIL",
        "mutation_gate": "PENDING_LIST_TOOLSETS" if runtime_ready else "BLOCKED",
        "next_required_check": (
            "In a newly initialized Codex task, call list_toolsets and one read-only Unreal query."
            if runtime_ready
            else "Resolve every reported endpoint mismatch before starting or restarting the server."
        ),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the configured and live Unreal MCP endpoint before mutations."
    )
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--client-config", action="append", default=[], type=Path)
    parser.add_argument("--log", type=Path)
    args = parser.parse_args()

    result = inspect_endpoint(
        args.project_root,
        client_configs=args.client_config or None,
        log_path=args.log,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["runtime_endpoint_verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
