#!/usr/bin/env python3
"""Run the pinned official Codex Plugin and Skill validators."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.error import URLError
from urllib.request import urlopen


CODEX_REVISION = "985cf47a4eb6084b2ff6b30ebdb1216acda85bb4"
SOURCE_ROOT = (
    f"https://raw.githubusercontent.com/openai/codex/{CODEX_REVISION}/"
    "codex-rs/skills/src/assets/samples"
)
VALIDATORS = {
    "validate_plugin.py": "plugin-creator/scripts/validate_plugin.py",
    "identifier_validation.py": "plugin-creator/scripts/identifier_validation.py",
    "quick_validate.py": "skill-creator/scripts/quick_validate.py",
}
REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if importlib.util.find_spec("yaml") is None:
        print(
            "PyYAML is required. Install it in this Python environment with: "
            "python -m pip install PyYAML==6.0.3",
            file=sys.stderr,
        )
        return 1

    skills = sorted((REPO_ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        print("No bundled Skills found; validation cannot pass.", file=sys.stderr)
        return 1

    print(f"Official Codex validators: {CODEX_REVISION}", flush=True)
    try:
        with tempfile.TemporaryDirectory(prefix="codex-plugin-validation-") as directory:
            temporary = Path(directory)
            for filename, source in VALIDATORS.items():
                with urlopen(f"{SOURCE_ROOT}/{source}", timeout=30) as response:
                    contents = response.read(256 * 1024 + 1)
                if len(contents) > 256 * 1024:
                    raise ValueError(f"Unexpected validator size: {filename}")
                contents.decode("utf-8")
                (temporary / filename).write_bytes(contents)

            subprocess.run(
                [sys.executable, "-X", "utf8", "-B", str(temporary / "validate_plugin.py"), str(REPO_ROOT)],
                check=True,
                timeout=120,
            )
            for skill in skills:
                print(f"Validating Skill: {skill.parent.name}", flush=True)
                subprocess.run(
                    [sys.executable, "-X", "utf8", "-B", str(temporary / "quick_validate.py"), str(skill.parent)],
                    check=True,
                    timeout=120,
                )
    except (OSError, URLError, ValueError, subprocess.SubprocessError) as error:
        print(f"Official validation failed: {error}", file=sys.stderr)
        return 1

    print(f"Official validation passed: 1 Plugin and {len(skills)} Skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
