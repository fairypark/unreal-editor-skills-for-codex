# Reusable Production Assets

Turn successful scene work into assets that can survive another level, project,
team, or user without copying private content or transferring visual approval.

## Separate three distribution layers

1. **Project source library:** preserve exact approved UAssets in a read-only
   project folder with evidence, dependencies, hashes, and provenance.
2. **Portable system contract:** distribute dependency-free JSON contracts,
   parameter roles, exclusion rules, collision intent, and promotion gates
   through the Codex plugin.
3. **Unreal content plugin:** distribute actual UAssets only when every bundled
   dependency is license-clean, redistributable, and declared. Prefer
   user-supplied asset slots over marketplace content.

Do not describe project-local UAssets or an agent's memory as a shared asset
library. A public artifact must exist in a versioned plugin or explicit package.

## Promote deliberately

For each candidate, record its stable ID, role, class, version, source,
immutable approval evidence, approval scope, direct and transitive dependencies,
portable logic, map-specific substitutions, collision intent, hard failures,
rejected predecessors, and default `REVALIDATION_REQUIRED` state.

Promote only the system that passed a fixed-camera visual gate. Generation,
save success, grounding, or instance count alone never grants promotion.

The plugin bundles these dependency-free contracts:

- `terrain-projected-gravel-route.system.json`
- `clustered-water-vegetation.system.json`

Install them with:

```text
python scripts/install_production_asset_templates.py --project-root <root>
```

The installer writes only under
`Docs/VisualQuality/ProductionAssets/Templates/` and refuses overwrites unless
`--force` is explicit.

## Package actual Unreal assets safely

Before distributing UAssets, complete a license and dependency audit:

1. Generate an Asset Registry dependency report.
2. Classify every dependency as project-owned, engine-provided,
   redistributable, user-supplied, or prohibited.
3. Replace prohibited dependencies with soft slots, parameters, or documented
   user-supplied requirements.
4. Remove map coordinates, private paths, credentials, user data, and failed
   candidates.
5. Add version, role, contract, approval-scope, and reuse-status metadata.
6. Test in a clean project containing only declared dependencies.
7. Re-run a golden-slice visual gate; portability does not preserve approval.

If a clean-project test is unavailable, distribute only the contract and
templates. Do not ship opaque UAssets that depend on a private project.
