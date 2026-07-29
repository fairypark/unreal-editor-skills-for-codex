# Landscape, ecology, collision, and streaming

## Separate world extent from streaming

Reserve a coherent Landscape envelope larger than the current playable area
when future expansion is plausible. Choose resolution, XY/Z scale, section
size, component count, and physical size together. Give reserve terrain macro
elevation, drainage, silhouette, and a compatible base material.

Choose World Partition cells and Landscape streaming proxy grid from measured
streaming needs. Do not create more proxies merely because the Landscape
resolution is large. Audit loaded coverage, grid size, components per proxy,
external packages, Data Layers, and performance before proposing a rebuild.

## Build terrain in three frequencies

1. Macro: valley, basin, ridge, terrace, river course, and distant silhouette.
2. Meso: banks, path crown, cut/fill slopes, drainage, retaining transitions,
   erosion, and building-pad blends.
3. Micro: stones, roots, soil breakup, litter, moss, wetness, and wear.

Do not flatten the complete level. Measure the center, four corners, and four
edge midpoints of every conventional building footprint. Flatten only the pad,
then connect it with slopes, terraces, foundations, stairs, retaining stone,
drainage, erosion, and contact materials.

## Reimport Landscape data safely

Before heightmap or layer-map import/reimport:

1. Discover an official typed tool and any actually installed extension.
2. Resolve the canonical Landscape; auto-select only when exactly one exists.
3. Dry-run `.r16`/`.r8` format, resolution, extent, edit layer,
   `LandscapeLayerInfo`, World Partition coverage, Data Layers, transform,
   material, packages, and source-control writability.
4. Save affected packages and create a durable recovery point.
5. Execute only through a structured API. Reject partial loaded-only writes.
6. Re-read height range and nine representative points; verify every layer,
   material, transform, layout, and save result.

If these typed operations are absent, stop and record the gap in
`docs/UNREAL_TOOLSETS_EXTENSION_HANDOFF.md`. A UI import is a temporary,
user-approved workaround only. Observe the smallest subtree, perform one
action, call `SlateInspectorToolset.Unobserve` in finally-style cleanup, confirm
no observer remains, and report the result as unverified unless structured
reads prove it.

## Snap and place without self-hits

Prefer a structured ground-snap tool that returns the hit Actor/component,
location, normal, and applied delta. Require it to ignore the Actor and its
components, support explicit trace channels, optionally prefer or require
Landscape, align the Actor bounds bottom, and trace below negative world Z.

When no such callable exists:

- do not trust the stock `snap_to_ground` boolean for a critical batch;
- trace or sample the intended Landscape first with a discovered read tool;
- move using the complete transform and an Actor-bounds bottom offset;
- re-read representative Actors and verify the hit target;
- stop on no-hit rather than leaving an Actor at an arbitrary positive Z.

## Preserve placement while repairing collision

Collision defects do not authorize deletion of well-composed assets.

- Dense PCG groundcover and tiny debris: `NoCollision` or narrow query-only
  policy.
- Hero rocks: project-local collision-safe duplicate with reviewed convex
  collision.
- Hero trees: trunk capsule or another narrow simple primitive; branches and
  leaves should not create broad blockers by default.
- Structures and walls: simple collision matching visible form, checked at
  ankle, torso, and head height.

Adjust component responses, collision variants, convex hulls, capsules,
navigation relevance, and cull/LOD policy before changing composition.

## Build ecology as vertical and spatial layers

Use macro, meso, and micro spatial organization plus independent vertical
strata. Define exclusion masks for architecture, yards, paths, water, roads,
hero views, and gameplay volumes. Use rock as geologically plausible clusters,
exposures, bank material, talus, or erosion evidence—not random wall filler.

Read [pcg-biome-orchestration.md](pcg-biome-orchestration.md) for the full PCG
contract.
