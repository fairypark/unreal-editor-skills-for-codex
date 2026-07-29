# Unreal Toolsets Extension handoff

This is the implementation contract for a separate public Unreal Editor plugin
project. This Codex skills repository owns only discovery, orchestration,
guidance, and capability-gap documentation. It must not contain, build, package,
publish, or install the runtime plugin.

## Product boundary

- Use the client-neutral working name `Unreal Toolsets Extension` and repository
  name `unreal-toolsets-extension`; exclude `Codex` and `Community` from runtime
  identifiers.
- State that the project is independent and unofficial.
- Add new ToolsetRegistry classes without editing Epic Engine,
  `ModelContextProtocol`, `AllToolsets`, or any Fab plugin.
- Expose the same typed tools to Claude, Codex, and every compatible MCP client.
- Keep the implementation broadly useful: no project paths, map names,
  coordinates, private assets, credentials, or user-specific defaults.
- Publish source and verified release artifacts from its own public GitHub
  repository. Do not update a maintainer's personal marketplace installation.

## P0 Landscape safety

Implement and test:

- `GetLandscapeInfo`, `CreateLandscape`, `ImportHeightmap`,
  `ReimportHeightmap`, `ImportWeightmap`, `SetLandscapeMaterial`,
  `GetHeightStatistics`, `ValidateBuildingPad`, and `SaveLandscape`.
- A combined preflight/dry-run plus atomic reimport for `.r16` heightmaps and
  `.r8` layer maps. It may auto-select only when exactly one canonical
  Landscape exists.
- Exact source format, byte depth, resolution, vertex extent, edit-layer,
  `LandscapeLayerInfo`, package-writability, and loaded-coverage validation.
- A durable pre-mutation package checkpoint and exact raw height/layer backup.
- Preservation and post-verification of transform, section/component layout,
  material, layer assignments, World Partition, Data Layers, height range, and
  nine representative vertices.
- Typed success only after verification and requested save. Raise stable errors
  on failure and distinguish verified rollback from reload-required recovery.

Add a read-only Landscape Streaming Proxy audit that reports grid size, proxy
count, components per proxy, loaded coverage, outliers, and evidence-based
recommendations. Landscape resolution and reserve extent must be separate from
streaming grid design. Proxy count is not a target. A rebuild path must default
to dry-run and require a stale-plan guard, explicit confirmation, complete
coverage, recovery point, post-audit, and save verification.

## P0 placement and collision

Add a structured `SnapActorToGround` operation that:

- ignores the target Actor, its components, and optionally attached Actors;
- supports an explicit trace channel, complex/simple query, Landscape-only and
  Landscape-preferred filters;
- uses the Actor bounds bottom offset rather than assuming the pivot is ground;
- traces across negative world Z without a fixed `8000 cm` floor;
- returns hit Actor/component, location, normal, trace range, and applied delta;
- raises a clear no-hit or rejected-hit error.

Acceptance tests must reproduce self-collision and negative-elevation failures.
The environment workflow preserves good visual placement and fixes collision
through local response changes, collision-safe mesh variants, convex hulls,
trunk capsules, or decoration-only `NoCollision`.

## P1 Landscape, PCG, and capture

Implement structured APIs for:

- creating and editing `LandscapeGrassType` assets;
- connecting Landscape Grass Output layers to grass types;
- resolving unnamed/default material output pins such as
  `LandscapeLayerCoords`;
- add/update/remove/reorder/replace CRUD for PCG weighted mesh entries;
- auditing generated HISM/ISM counts by graph instance and mesh, collision,
  navigation, cull distances, Landscape-hit ratio, rejection reasons, and empty
  volumes;
- `CaptureViewport` with a real default for optional annotations;
- a PIE-safe game viewport capture path or an explicit fallback, with examples
  that always stop PIE after capture.

Preserve compatibility with existing official callable tools. Prefer wrappers
or new extension toolsets over shadowing official class or tool names.

## P0 PCG biome orchestration

Provide a reusable UE 5.8 PCG biome preset/template or typed creation/editing
API with these independent stages:

1. `Biome Boundary`
2. `Density Field`
3. `Exclusion Sources`
4. `Layer Subgraphs`
5. `Output/Audit`

The density field must support spline/volume signed-distance or equivalent
edge-to-core gradients, multi-scale noise warp, falloff, and edge breakup.
Expose seed, density curve, layer toggles, species set, and biome preset per
instance.

Use distinct subgraphs and density/spacing policies for canopy, secondary
trees/saplings, shrubs, fern/herb, groundcover, deadwood/debris, and geology.
Each stratum consumes prior footprints and environmental metadata to model
competition, shade, and gaps; do not mix differently scaled meshes onto one
shared point set.

Coordinate generators through shared masks and edge data:

- River: water exclusion, inner/outer bank bands, moisture falloff, riparian
  species, and boulder/stone/debris points.
- Path: surface, clear width, shoulder, edge bands, canopy removal, edge
  recovery, and path assets.
- Building, yard, road, stream, and hero-view exclusions: masks/subtractions
  that regenerate when source Actors change, never destructive deletion.
- Preserve Landscape layer, slope, height, normal, curvature/concavity, and
  `WorldRayHitQuery` metadata when available.

Default distribution combines Poisson/blue-noise spacing, multi-scale noise,
cluster centers, and edge gradients. Audit core/mid/edge coverage, layer/mesh
instance counts, rejection reasons, exclusion correctness, collision/culling,
and deterministic seeds. Add top-down heatmap, per-layer preview, and exclusion
overlay outputs.

Performance policy is strata-specific HISM/ISM, partitioned generation, cull
tiers, HLOD/Nanite suitability, and collision scope. Optimize these before
removing vegetation. A reduced canopy silhouette or player-height understory
coverage is a visual regression and fails acceptance.

Automated tests must cover density gradient edge-to-core, exclusion
subtraction, deterministic seed, weighted-entry CRUD, layer toggles,
collision/culling policy, and complete audit output.

## Fab feasibility

A guarded, read-only Fab support toolset is feasible only through stable,
documented local or public surfaces. Candidate tools are
`GetFabIntegrationInfo`, `GetFabCacheSummary`, `ListFabCachedEntries`,
`GetFabCacheEntryStatus`, and `GetFabImportTypeSupport`.

Do not automate sign-in, extract cookies/tokens, call private Fab endpoints,
circumvent entitlements, or claim reliable download/install control without a
documented API. Keep the existing `fab-library-advisor` skill responsible for
the user's private owned-library workflow.

## Required verification

- BuildPlugin from a clean source package for each declared UE version/platform.
- Reflection/schema tests and success/error automation tests for every tool.
- Disposable-project source and packaged-binary installation.
- Live MCP discovery and calls from at least two compatible clients.
- World Partition, rollback, save-failure, collision, PCG determinism, and
  capture tests on disposable test content.
- Draft GitHub Release first; publish only after the complete matrix passes.

The current unverified implementation draft, if transferred, must be treated as
source material rather than a release candidate.
