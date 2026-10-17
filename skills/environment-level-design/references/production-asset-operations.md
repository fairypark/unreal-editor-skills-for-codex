# Production Asset Operations

The plugin bundles dependency-free JSON contracts, not Unreal assets:

- `ProductionAssetCatalog.template.json`
- `terrain-projected-gravel-route.system.json`
- `clustered-water-vegetation.system.json`
- `meadow-ground-cover.system.json`
- `environment-source-check.template.json`

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

## Curate a completed level into a source collection

Use native Unreal duplication rather than copying or renaming `.uasset` files in the filesystem. This is a collection operation, not a new level build; do not place actors, switch maps, or reopen unrelated design gates solely to organize approved sources.

1. Inventory the exact sources, dirty state, original consumers, direct and transitive dependencies, and source visual evidence. Exclude prototypes, superseded trials, and rejected sources. Separate `SELF_AUTHORED`, `PROJECT_DEPENDENT`, and `MAP_SPECIFIC_EXAMPLE` records; these labels describe dependencies, not license grants.
2. Choose a new versioned destination outside existing read-only libraries. Verify every destination is absent before duplication. Record source hashes or another recovery baseline, and journal successful copies so an interruption can resume without overwrite or duplication.
3. Duplicate the selected family through the Editor. Rebind copied meshes, material instances, and other owned links to copied dependencies only where the complete family has been included. Never replace the original scene's references. Keep licensed external dependencies explicit rather than silently copying a whole pack.
4. Add catalog metadata, then save only the new assets. Compare source/copy bounds, LOD/triangle counts, material slots, parameters, and relevant graph/settings state. Re-query the dependency graph and dirty state; compare original hashes and consumers. These are copy checks, not a new visual verdict.
5. Preserve source evidence with its scope and hashes. Mark old screenshots as source evidence rather than new-copy renders. Record `REVALIDATION_REQUIRED`, map-specific coordinates or inputs, missing wind/performance/platform checks, and distribution limits.
6. Add the collection catalog to the project's discoverable index and provide a Korean review guide when required. Future use duplicates the candidate into the destination map folder, replaces map-specific inputs, checks dependency closure, and runs the new scope's representative comparison.

For example, a curved-grass mesh family and its own shader may be self-authored, while a ground material still requires licensed textures and an authored field's world coordinates. Archive all useful cases, but do not label the coordinate-bound material as a portable drop-in asset. Consult [vegetation-and-ground-cover.md](vegetation-and-ground-cover.md) for source and field checks and the paired [Korean review](environment-reuse-review.ko.md) for the collection boundaries.

## Distribute actual UAssets

Do not add project UAssets to this Codex plugin. Package them separately only after an Asset Registry dependency report classifies every direct and transitive dependency as project-owned, engine-provided, redistributable, user-supplied, or prohibited. Replace prohibited dependencies with user-supplied slots, test in a clean project, and re-run the applicable runtime and visual checks.
