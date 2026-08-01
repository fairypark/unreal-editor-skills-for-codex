# Production Asset Operations

The plugin bundles dependency-free JSON contracts, not Unreal assets:

- `ProductionAssetCatalog.template.json`
- `terrain-projected-gravel-route.system.json`
- `clustered-water-vegetation.system.json`

Use them as implementation inputs after content ownership, licensing, reuse scope, and revalidation requirements have been decided. When the Handbook plugin is installed, use `design-unreal-content-architecture` for those decisions.

## Install the contracts

From the `environment-level-design` Skill directory, run:

```text
python scripts/install_production_asset_templates.py --project-root <PROJECT_ROOT>
```

The installer validates the bundled JSON and writes only beneath:

```text
Docs/VisualQuality/ProductionAssets/Templates/
```

It refuses existing destinations. Use `--force` only after inspecting the exact files that will be replaced and confirming the user intends an overwrite.

## Adapt in the project

1. Read each contract's required inputs, responsibilities, parameters, exclusions, collision intent, and hard failures.
2. Fill asset slots only with dependencies the project is authorized to use.
3. Implement the system in a bounded representative slice.
4. Verify source assets, deterministic generation, contact, collision, Navigation, performance, and fixed-camera output.
5. Record the adapted project asset, dependency report, evidence, approval scope, and version in the project-owned catalog.
6. Begin every use in a new world, biome, scale, lighting, platform, or gameplay context as `REVALIDATION_REQUIRED`.

The route contract expects one coherent width-bearing route projected to a trusted terrain surface. The vegetation contract expects asymmetric clusters, open-water or route exclusions, and separate low-frequency accents. Neither contract is a finished PCG graph.

## Distribute actual UAssets

Do not add project UAssets to this Codex plugin. Package them separately only after an Asset Registry dependency report classifies every direct and transitive dependency as project-owned, engine-provided, redistributable, user-supplied, or prohibited. Replace prohibited dependencies with user-supplied slots, test in a clean project, and re-run the applicable runtime and visual checks.
