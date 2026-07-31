#!/usr/bin/env python3
"""Install dependency-free production-asset templates into an Unreal project."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


TEMPLATE_NAMES = (
    "ProductionAssetCatalog.template.json",
    "terrain-projected-gravel-route.system.json",
    "clustered-water-vegetation.system.json",
)


def validate_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError(f"Unsupported or missing schema_version in {path.name}")


def install(project_root: Path, force: bool = False) -> dict[str, object]:
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise FileNotFoundError(f"Project root does not exist: {project_root}")

    source_root = Path(__file__).resolve().parents[1] / "assets" / "production-assets"
    destination_root = (
        project_root / "Docs" / "VisualQuality" / "ProductionAssets" / "Templates"
    )
    sources = [source_root / name for name in TEMPLATE_NAMES]
    for source in sources:
        if not source.is_file():
            raise FileNotFoundError(f"Bundled template is missing: {source}")
        validate_json(source)

    destinations = [destination_root / source.name for source in sources]
    conflicts = [path for path in destinations if path.exists()]
    if conflicts and not force:
        joined = ", ".join(str(path) for path in conflicts)
        raise FileExistsError(f"Refusing to overwrite existing templates: {joined}")

    destination_root.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for source, destination in zip(sources, destinations, strict=True):
        shutil.copy2(source, destination)
        validate_json(destination)
        installed.append(str(destination))

    return {
        "status": "INSTALLED",
        "destination_root": str(destination_root),
        "installed": installed,
        "overwrote_existing": bool(conflicts),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = install(args.project_root, args.force)
    except (FileExistsError, FileNotFoundError, ValueError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
