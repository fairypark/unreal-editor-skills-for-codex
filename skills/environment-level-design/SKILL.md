---
name: environment-level-design
description: Design, build, rebuild, dress, or review production-quality Unreal Engine environment levels with Visual Gate-first art direction, 360-degree completeness, Landscape, materials, vegetation, PCG biomes, geology, collision, streaming, performance, and final gameplay validation. Use for outdoor maps, open-world spaces, terrain-led environments, environment recovery, PCG forest/river/path systems, or reusable level-design standards. Do not use for one isolated Actor placement or conceptual discussion with no level work.
---

# Environment Level Design

Build the environment as a complete place. Do not trade away the visual target
to polish gameplay before the visual baseline exists.

## Apply the priority order

1. Visual quality and art-direction fidelity.
2. 360-degree environmental completeness and density.
3. Composition, silhouette, terrain, material, foliage, and geology quality.
4. Technical stability and performance budgeting.
5. Gameplay experience and encounter or layout optimization.

Immediately repair only minimum safety blockers before the Visual Gate:
player start underwater or below terrain, lethal unavoidable falls, completely
blocked primary movement, incorrect global collision, and Editor/runtime
crashes. Defer other gameplay polish and optimization until the Visual Gate
passes.

## Load the required references

- Read [quality-gates.md](references/quality-gates.md) for every build or review.
- Read [landscape-ecology-and-collision.md](references/landscape-ecology-and-collision.md) for outdoor terrain, materials, water, vegetation, collision, Landscape import, or streaming proxies.
- Read [pcg-biome-orchestration.md](references/pcg-biome-orchestration.md) for PCG vegetation, forest, biome, river, path, exclusion, or distribution work.
- Use [level-brief-and-iteration-log.md](references/level-brief-and-iteration-log.md) when starting or recovering a level.

## Establish authority and provenance

1. Load relevant project-registered Unreal Agent Skills when available.
2. Discover only the live toolsets needed for the next pass. Never assume a
   documented extension is installed.
3. Prefer structured callable tools. If a capability is absent, record the gap
   in the external runtime handoff; do not create an Editor plugin in this
   repository or disguise generic property edits as a domain API.
4. Use screen control only for a user-approved temporary workaround. Save
   first, observe the smallest subtree, and unobserve in finally-style cleanup.
5. Declare the construction provenance:
   - `blank-level concept-led`: create an original layout;
   - `source-assisted`: reuse authored level content only with explicit user
     permission.
6. Never silently copy a failed or existing map into a new level.

## Create a decision-ready visual brief

Record concept/reference direction, setting, biome, atmosphere, macro terrain
silhouette, foreground/midground/background roles, focal hierarchy, material
transitions, vegetation strata, geology, water logic, architecture contacts,
playable envelope, reserve Landscape envelope, target platform, and prohibited
motifs. Include arrival, hero, route, reverse, and elevated views.

Build an asset lineup at final scale. Verify front, side, back, silhouette,
pivot, material, LOD/Nanite, and collision intent before map-scale production.

## Build in visual passes

1. Form macro terrain and water systems. A wholly planar outdoor base fails.
2. Grade only building footprints into pads and blend each pad naturally into
   surrounding terrain.
3. Complete one golden slice with final terrain transition, material layers,
   architecture contact, canopy-to-ground vegetation, geology, lighting, and a
   credible reverse view.
4. Scale validated systems across every reachable direction.
5. Build coordinated PCG biome, river, and path generators using masks and edge
   data rather than one uniform scatter graph.
6. Add surface contact, erosion, drainage, banks, roots, debris, dampness, and
   culturally or ecologically coherent detail.
7. Capture and pass the Visual Gate before Gameplay Polish.
8. Run Performance and Gameplay Gates. Reject either gate if it regresses the
   passed Visual Gate.

## Preserve visual intent during technical repair

- Do not delete or thin visually appropriate assets before adjusting collision
  scope, culling, LOD, Nanite, instancing, HLOD, navigation, or streaming.
- Use `NoCollision` or lightweight collision for dense decorative PCG layers.
  Use collision-safe mesh variants and convex hulls for hero rocks, and trunk
  capsules or similarly narrow primitives for hero trees.
- Treat streaming proxy count as an outcome of measured streaming needs, not a
  goal.
- When a batch times out, inspect resulting state and counts before retrying.

## Validate, save, and report

Capture the same fixed cameras before and after changes. Name the weakest
system, change one major cause, and keep the change only when it improves the
target without damaging required views. Save affected levels and owned assets
after successful gates. Report unverified runtime gaps explicitly.
