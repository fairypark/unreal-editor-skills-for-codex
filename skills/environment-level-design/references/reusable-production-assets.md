# Reusable Production Assets

Use this workflow to turn successful scene work into production assets that can
survive another level, project, team, or user without copying private content or
pretending that visual approval transfers automatically.

## Separate three distribution layers

1. **Project source library:** preserve exact approved UAssets in a read-only
   project folder. Keep original evidence, dependencies, hashes, and source
   paths. This layer may contain project-licensed dependencies.
2. **Portable system contract:** distribute dependency-free JSON contracts,
   schemas, parameter roles, exclusion rules, collision intent, and promotion
   requirements through the Codex plugin.
3. **Unreal content plugin:** distribute actual UAssets to other users only when
   every included dependency is license-clean, redistributable, and declared.
   Prefer user-supplied asset slots over bundling marketplace content.

Do not describe project-local UAssets or an agent's memory as a shared asset
library. A reusable public artifact must be present in the versioned plugin or
another explicit distribution package.

## Promote an asset deliberately

For each candidate, record:

- stable asset ID, role, class, and version;
- source asset and immutable approval evidence;
- exact approval scope and visual category scores;
- direct and required transitive dependencies;
- portable logic versus map-specific data;
- points, splines, masks, transforms, materials, or asset sets that a new user
  must replace;
- decorative collision, overlap, and Navigation intent;
- hard failures and rejected predecessor systems;
- `REVALIDATION_REQUIRED` as the default reuse state.

Never promote an asset solely because it generated successfully, saved, or has
many instances. Promote only the system that passed the fixed-camera visual
gate.

## Build dependency-free contracts

The plugin includes two example system contracts under
`assets/production-assets/`:

- `terrain-projected-gravel-route.system.json`
- `clustered-water-vegetation.system.json`

They specify responsibilities, inputs, outputs, failure imagery, and promotion
gates without embedding project coordinates or proprietary asset paths. Treat
them as implementation contracts, not finished Unreal graphs.

Install the templates into a project with:

```text
python scripts/install_production_asset_templates.py --project-root <root>
```

The installer validates its bundled JSON, writes only under
`Docs/VisualQuality/ProductionAssets/Templates/`, and refuses to overwrite an
existing file unless `--force` is explicitly supplied.

## Package actual Unreal assets safely

Before placing UAssets in a distributable Unreal content plugin, complete a
license and dependency audit:

1. Generate a dependency report from the Asset Registry.
2. Classify every dependency as project-owned, engine-provided,
   redistributable, user-supplied, or prohibited.
3. Replace prohibited dependencies with soft slots, parameters, or documented
   user-supplied requirements.
4. Remove map coordinates, private paths, credentials, user data, and unused
   failed candidates.
5. Add asset metadata for version, role, source contract, approval scope, and
   reuse status.
6. Test the content plugin in a clean project containing only declared
   dependencies.
7. Re-run a golden-slice visual gate. Portability does not preserve aesthetic
   approval.

If a clean-project test is not possible, distribute only the system contract
and installer templates. Do not ship opaque UAssets that silently depend on a
private project.
