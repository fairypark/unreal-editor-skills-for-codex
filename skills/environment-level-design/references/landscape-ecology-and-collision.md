# Landscape, Ecology, Materials, and Collision

Apply this reference to outdoor levels and any map whose visual quality depends on terrain-led composition.

## Plan an expansion-ready Landscape

Separate the current playable envelope from the Landscape reserve envelope.

- Unless the brief says otherwise, reserve roughly 1.5–2.0 times the current playable width in plausible expansion directions.
- Let the active area occupy roughly 25–50 percent of the total Landscape, biased toward known future routes rather than centered blindly.
- Prefer one coherent valid Landscape layout managed by World Partition or an equivalent streaming strategy over disconnected floor meshes.
- Choose resolution, section size, component count, XY scale, and Z scale together. Record physical dimensions, vertex spacing, sculpt fidelity, collision precision, memory, and streaming cost.
- Give reserve components macro elevation, drainage direction, boundary silhouettes, and a compatible base material. Delay dense props, detailed weight painting, and collision-heavy generation until they enter production scope.
- Verify streaming transitions and prevent any current route or camera from exposing an abrupt edge or world void.

Do not confuse world extent with surface fidelity. A huge low-density Landscape cannot form credible paths and banks; an excessively dense empty Landscape wastes resources.

## Sculpt in three frequency bands

1. **Macro:** basin, valley, ridge, terrace, river course, enclosure, and distant silhouette.
2. **Mid:** banks, path crowns, cut-and-fill slopes, drainage, retaining transitions, terraces, and erosion channels.
3. **Micro:** stones, roots, soil breakup, leaf litter, moss, puddling, and localized wear.

Lock macro and mid forms before dense dressing. Rocks and ground patches cannot repair a flat base.

## Grade every building footprint

Non-flat macro terrain still requires intentionally level architecture sites.

1. Before placement, measure at least nine surface points: center, four corners, and four edge midpoints.
2. For a conventional level structure, target no more than 10 cm ground-height variation across the footprint and no visible cross-slope.
3. If greater variation is intentional, author a stepped foundation, retaining terrace, or pier system that visibly carries the load.
4. Blend the pad into surrounding terrain with slopes, retaining walls, stone edging, stairs, drainage, erosion, and contact materials.
5. After placement, remeasure and inspect every side at player height for floating corners, buried walls, blocked entrances, and inaccessible steps.

Never solve a sloped site by tilting or stretching the building, burying half of it, or hiding gaps with random rocks.

## Build a rule-driven Landscape material

Use a small coherent family of physically meaningful layers rather than painting one texture everywhere. A typical set may include vegetation cover, exposed soil, compacted path, rock or cliff, wet bank, forest floor, and authored detail accents.

Combine:

- slope and normal for rock exposure;
- height and drainage context for wetness or snow;
- path, settlement, or gameplay masks for authored circulation;
- large-scale noise for macro breakup;
- smaller detail variation for close range;
- distance-aware texture treatment and consistent world scale;
- roughness, normal, color, and displacement or virtual-height blending where the renderer and budget support it.

Use automatic rules as a base, then art-direct focal routes, building pads, banks, and contact zones. Eliminate hard rectangular patches, visible tiling, uniform roughness, and abrupt layer seams. Keep material complexity within the target platform budget.

## Use a hybrid vegetation system

Assign each system a clear job:

- **Landscape Grass or equivalent:** dense, inexpensive ground response tied to material layers.
- **Foliage painting or hand placement:** authored hero trees, route framing, landmark clusters, and precise removals.
- **PCG:** repeatable biome distribution, density gradients, ecological clustering, distance rules, slope or height filters, and large-area regeneration.

Build canopy, understory, shrubs, ground cover, deadfall, and contact debris as separate strata. Vary species, spacing, scale, rotation, cluster radius, and density while preserving readable openings.

For procedural generation:

- use deterministic seeds for reviewable changes;
- define exclusion zones for paths, buildings, water, sightlines, and gameplay volumes;
- inspect generated results from player height, reverse views, and above;
- cap density by platform budget and verify instancing, LOD, Nanite, HLOD, and streaming behavior;
- regenerate only after the governing terrain or mask is stable.

Do not use uniform scatter or an evenly spaced perimeter ring. A forest is a spatial volume with gradients, gaps, and ecological logic.

## Preserve visual placement when correcting collision

Collision defects are repair tasks, not permission to delete well-composed assets.

1. Identify the exact failure: wrong preset, missing simple collision, over-broad hull, unsuitable complex collision, bad transform, capsule pinch point, or navigation mismatch.
2. Preserve the placed Actor and its intended composition while evaluating fixes.
3. Prefer the narrowest safe correction:
   - adjust the instance or component collision response when the issue is local;
   - author or refine simple convex collision for traversal-critical static meshes;
   - use complex-as-simple only when appropriate for a static asset and the performance implications are acceptable;
   - disable collision for tiny decorative foliage while retaining collision on gameplay-significant trunks, rocks, walls, and structures;
   - create a project-local mesh variant when changing the shared source would damage other levels;
   - add deliberate invisible blocking only when it matches the visible form and remains maintainable.
4. Retest at ankle, torso, and head height with the actual player capsule. Check entrances, stairs, wall ends, banks, bridges, roots, and narrow gaps.
5. Verify navigation, physics behavior, camera behavior, and reverse-side traversal.

Delete or replace an asset only when the asset itself is visually or functionally unsuitable and the user has authorized that design change—not merely because collision needs work.

## Integrate water and terrain

- Shape banks, depth cues, surface variation, wet transitions, and believable drainage.
- Avoid a hard rectangular water sheet or unexplained vertical shore.
- Keep roots, terrestrial plants, paths, and foundations out of water unless the species or construction supports it.
- Validate collision, swimming or blocking intent, bank traversal, reflections, translucency cost, and views from both shores.

## Verify transforms and batch operations

- Resolve a trusted terrain surface before ground placement; snapping alone can hit props or the wrong surface.
- Read complete transforms before modification and preserve location, rotation, and scale together.
- Re-read representative Actors after batches.
- When an operation times out, verify counts and results before retrying to avoid duplicates.
- Treat bounds as an estimate, not proof that a mesh visually covers the intended ground.
