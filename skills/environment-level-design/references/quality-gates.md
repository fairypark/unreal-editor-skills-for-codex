# Environment quality gates

Use gates in this order. A later gate cannot compensate for an earlier failure.

## Gate 0 — Minimum safety

Repair immediately when:

- the player starts underwater or below terrain;
- an unavoidable lethal fall prevents evaluation;
- the primary route is completely blocked;
- global collision is materially wrong;
- the Editor or runtime crashes.

Do not broaden this gate into encounter, route, or performance polish.

## Gate 1 — Visual benchmark

Do not start Gameplay Polish until this gate passes.

Capture:

- primary concept/reference beside matching fixed-camera views;
- at least two hero views plus arrival, route, and reverse views;
- four cardinal directions from a representative point, or eight for a large
  space;
- low, player-height, middle, and elevated views;
- foreground, midground, and background coverage;
- close contacts for buildings, paths, water, vegetation, and rock;
- top-down PCG density, layer preview, and exclusion overlay when PCG is used.

Score each applicable category from 1 to 5 and require every category to reach
at least 4:

1. concept/reference fidelity and art direction;
2. 360-degree completeness and intentional density;
3. composition, silhouette, depth, and focal hierarchy;
4. non-planar macro/mid terrain and distant landform;
5. locally flat building pads with natural surrounding blends;
6. material-layer transitions, scale, breakup, and contact;
7. canopy, secondary tree/sapling, shrub, herb/fern, groundcover,
   deadwood/debris, and geology readability;
8. ecological exclusion, cluster diversity, and edge breakup;
9. river, bank, path, drainage, and geology logic;
10. architecture-ground contact and reverse-side finish;
11. foreground/midground/background vegetation at player height;
12. empty-space ratio: openings read as intentional composition, not missing
    work.

For the PCG forest benchmark, additionally require:

- closed but varied core canopy, a readable middle band, and an irregular
  gradient at the forest edge;
- path and river masks that carve cleanly while shoulders and banks recover
  naturally;
- no rectangular volume edge, grid, repeated mesh rhythm, identical
  rotation/scale, or unexplained broad vegetation void;
- layer toggles and previews that prove each vertical stratum is independent;
- reverse and ground-level frames whose foreground, midground, and background
  all contain readable layers.

## Gate 2 — Performance

Measure frame time, memory, streaming, generation cost, instance counts,
collision, navigation, and warnings. Before removing visual density, adjust:

1. HISM/ISM and partitioned generation;
2. cull-distance tiers;
3. LOD, Nanite suitability, and HLOD;
4. collision scope and navigation relevance;
5. streaming grid and regeneration scope.

Fail the gate if canopy silhouette, player-height understory coverage, material
quality, geology, or 360-degree completeness regresses from Gate 1.

## Gate 3 — Gameplay

Validate spawn, traversal, capsule clearance, route choices, encounter layout,
water and bank intent, stairs, boundaries, sightlines, and navigation. Preserve
the passed visual composition. Adjust local collision and layout mechanics
before deleting or thinning visual assets.

Fail the gate when its repair causes a Visual Gate regression.

## Hard visual failures

- wholly planar outdoor terrain without an explicit planar brief;
- only the camera-facing side is finished;
- Landscape edges, world voids, raw foundations, floating corners, or buried
  entrances;
- one texture everywhere, hard rectangular paint, visible tiling, or
  contradictory material scale;
- uniform scatter, perimeter rings, one point set with differently scaled
  meshes, or obvious repetition;
- arbitrary rocks embedded in cultural walls, oversized rocks used as
  mountains, or geology without exposure/cluster logic;
- deleting a well-composed asset merely because collision needs repair;
- performance improvement achieved by visibly collapsing density or
  silhouette;
- secretly reusing a failed/existing map when the provenance is blank-level.

## Evidence loop

For each failure, record the category, visible symptom, system cause, fixed
baseline camera, one major change, result capture, performance/gameplay side
effects, and keep/revert decision.
