# PCG biome orchestration

## Benchmark

Use these videos as a visual and systems benchmark, not as a source-code
dependency:

- [PCG playlist entry](https://www.youtube.com/watch?v=BqPhdQOweqU&list=PLA03OHAaHgYpo0enf8p-2oEpja3grLOKZ)
- [Forest, path, and river tool breakdown](https://www.youtube.com/watch?v=SCDZ8kobv1M&list=PLA03OHAaHgYpo0enf8p-2oEpja3grLOKZ&index=9)

The transferable target is a coordinated Forest Biome + River + Path system
that exchanges exclusions and edge data, exposes independent layers, and
creates an edge-to-core density transition. Do not imitate a screenshot by
raising uniform scatter density.

## Require an orchestrator

Organize the reusable graph or template into:

1. `Biome Boundary`
2. `Density Field`
3. `Exclusion Sources`
4. `Layer Subgraphs`
5. `Output/Audit`

Generate an edge-to-core density field from spline/volume signed distance or an
equivalent gradient. Combine falloff, multi-scale noise warp, and edge breakup
so the boundary never reads as a rectangular PCG volume.

Expose seed, density curve, layer enable toggles, species set, biome preset,
spacing, clump radius, and debug/audit controls on the graph instance.

## Separate vertical strata

Use independent subgraphs, points, density, and spacing for:

- canopy;
- secondary trees and saplings;
- shrubs;
- fern and herb layer;
- groundcover;
- deadwood and debris;
- geology.

Each stratum consumes earlier footprints and environment metadata to model
competition, shade, openings, and succession. Do not mix all mesh sizes on one point set.
Give every weighted species entry explicit weight, cluster seed,
scale, rotation, lean, minimum spacing, and clump radius.

## Coordinate context generators

River output must include water exclusion, inner/outer bank bands, moisture
falloff, riparian species masks, and boulder/stone/debris points.

Path output must include surface, clear width, shoulder, and edge bands. Remove
canopy through subtraction, then restore shrubs, saplings, deadwood, and debris
along a varied shoulder.

Maintain building, yard, road, stream, and hero-view exclusions as source-linked
masks. Regenerate when a source Actor changes; never destructively delete the
underlying distribution rule.

Sample painted Landscape layers, slope, height, normal, and
curvature/concavity when available. Preserve `WorldRayHitQuery` metadata through
filtering and projection.

## Use non-uniform distribution

Combine Poisson or blue-noise spacing, multi-scale noise, cluster centers, and
edge gradients. Define target coverage ranges for core, middle, and edge bands
per preset. The core may form a closed canopy, while the edge must transition
gradually and irregularly.

Fail on visible grid or rectangular edges, repeated mesh rhythms, identical
rotation/scale, unexplained broad voids, or a path/river cut with no natural
shoulder recovery.

## Orchestrate existing UE 5.8 callable tools

Always call `describe_toolset` first and use the returned schema. A safe
creation sequence with the stock UE 5.8 PCG toolset is:

1. `PCGToolset.ListNativeNodes` and `ListAvailableSubgraphs`.
2. `CreateGraph`, then `SetGraphParams` for seed, preset, density curve, layer
   toggles, species references, and audit switches.
3. `AddNode` and `AddSubgraphNode` in the five orchestrator sections.
4. Inspect `GetNativeNodeSchema` before every unfamiliar node.
5. `ConnectNodePins`; when a node exposes an unnamed/default output, use the
   schema's actual label. If the callable cannot address an empty label, record
   the capability gap instead of guessing.
6. Add section comments, then inspect `GetGraphStructure` and
   `GetGraphSchema`.
7. `SpawnGraphInstance`, `SetGraphInstanceParams`, and
   `ExecuteGraphInstance` on disposable or user-approved content.
8. Re-read `GetGraphInstanceParams` and use available data views/audits before
   saving.

Do not use ambiguous generic `ArrayAdd` to resize `MeshEntries`. If the installed
tools lack weighted-entry add/update/remove/reorder/replace operations, record
the external runtime gap and leave the graph unchanged.

## Audit and accept

Collect:

- top-down density heatmap;
- per-layer preview and exclusion overlay;
- instance count by graph instance, layer, and mesh;
- core/middle/edge coverage percentage;
- collision, navigation, and cull-distance policy;
- Landscape-hit ratio and preserved hit metadata;
- slope, layer, height, normal, and exclusion rejection counts;
- explicit empty-volume reasons;
- seed and deterministic output fingerprint.

Capture top-down, player height inside the forest, forest edge, path corridor,
riverbank, and reverse view. Pass only when ground-level foreground, midground,
and background layers read simultaneously, path and river are cleanly carved,
and both sides recover naturally.

Optimize HISM/ISM, partitioned generation, cull tiers, HLOD/Nanite, collision,
and streaming before reducing vegetation. Fail optimization when it weakens
canopy silhouette or player-height understory coverage.
