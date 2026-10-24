# Repository validation

Run validation from the repository root on Windows with Python 3.12 and
`powershell.exe` available. Install the validator dependency in the Python
environment selected for this work:

```powershell
python -m pip install PyYAML==6.0.3
python -X utf8 -B -m unittest discover -s tests -v
python -X utf8 -B scripts/validate_plugin_and_skills.py
git diff --check
```

When the default temporary directory is not writable, set `TEMP` and `TMP` to
an existing writable scratch directory before running the commands. The tests
and validator helper create and clean their temporary children there. The
`-B` option avoids Python bytecode files in the checkout.

The helper downloads the official Plugin validator, its identifier helper,
and the official Skill validator from
[OpenAI Codex revision 985cf47](https://github.com/openai/codex/tree/985cf47a4eb6084b2ff6b30ebdb1216acda85bb4/codex-rs/skills/src/assets/samples).
This is the pinned pre-removal revision used for this repository's release
validation. Downloads require HTTPS access to `raw.githubusercontent.com`;
they remain in a temporary directory and are not vendored into the plugin.
Missing dependencies, download errors, validator failures, and timeouts exit
nonzero. The helper validates the Plugin and every bundled Skill discovered
under `skills/` (currently six).

The [GitHub Actions workflow](../.github/workflows/validate.yml) runs the same
regression suite and official validators for pull requests, pushes to `main`,
and manual dispatch. It uses a Windows runner, read-only repository permission,
immutable action revisions, and a ten-minute job timeout. An authorized
maintainer should review source changes before updating the pinned validator
or action revisions.

## What a pass establishes

- Repository regression tests cover the bundled scripts, guidance invariants,
  and optional usage-metrics privacy and consent behavior.
- Metrics tests use synthetic inputs and isolated temporary storage through
  `UNREAL_CODEX_METRICS_HOME`; they do not enable collection for the user's
  real sessions or read the user's stored metrics.
- Official validators check the Plugin manifest and bundled Skill structure
  and metadata against the pinned Codex validation rules.

These checks do not launch Unreal Editor, connect to MCP, modify a project,
or establish runtime, visual-quality, packaging, or production readiness.
When a release changes those behaviors, record the relevant live checks and
their limits separately. Repository validation also does not replace the
configured credential guards required before staging, committing, or pushing.
