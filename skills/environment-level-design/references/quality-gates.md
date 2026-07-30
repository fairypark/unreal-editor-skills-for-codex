# Environment Quality Gates

Use these gates for both construction and review. Numerical checks support visual judgment; they do not excuse a level that still reads as flat, empty, repetitive, unfinished, or below the selected reference.

## Gate A — Concept and scope

Pass only when:

- one primary concept or reference direction is selected;
- arrival, hero, route, and reverse views are represented;
- route, focal hierarchy, enclosure, terrain silhouette, architecture vocabulary, vegetation strata, material palette, atmosphere, and prohibited motifs are written down;
- the concept is feasible with available assets, systems, time, and performance budget;
- construction provenance is explicit.

Stop if the design depends on unavailable capabilities. Obtain suitable assets, revise the concept, or reduce scope before building.

## Gate B — Topography and playable structure

For outdoor maps wider than roughly 50 m, aim for at least 200 cm of readable ground-surface relief between the lowest and highest playable land zones, with at least one important zone differing from the main route by 100 cm or more. Smaller maps still need a visible, traversable elevation change.

Pass only when:

- low, circulation, and elevated height-band roles are evident;
- relief comes from coherent terrain, slopes, terraces, banks, or stepped construction rather than props on a flat floor;
- six or more representative surface measurements prove variation;
- major height bands are reachable or intentionally bounded;
- route width, slope, stairs, banks, and capsule clearance work in PIE;
- an elevated overview does not read as one plane.

Stop immediately if all representative land measurements fall within a 50 cm band, the height change is decorative but not traversable, or the level is a coplanar grid of floor meshes.

## Gate C — Asset readiness

Pass only when a final-scale asset lineup proves enough compatible variation for:

- coherent terrain and water edges;
- architecture, enclosure, and foundations;
- canopy, understory, ground cover, and ecological transitions;
- contact detail and focal storytelling;
- finished fronts, backs, sides, and silhouette views.

Primitive planes, cubes, spheres, default materials, and extremely scaled rocks are blockout-only. They must not survive into the golden slice or final evidence.

## Gate D — Golden slice

The 10–20 m representative slice must include:

- a readable route and gameplay decision;
- focal architecture or a meaningful focal prop;
- macro-to-micro terrain transition;
- architecture-ground, wall-terrain, water-bank, and vegetation-hardscape contact where applicable;
- layered vegetation and an intentional boundary;
- final materials and representative lighting;
- a credible reverse view.

Judge it at player height and from above. Do not scale a weak slice.

## Gate E — Full-level visual acceptance

Capture:

- at least two hero views;
- arrival, reverse, and route views;
- four cardinal directions from PlayerStart, or eight directions for a large space;
- representative movement points and reachable boundaries;
- one elevated overview;
- close contact views for buildings, water, paths, and vegetation.

Score each category from 1 to 5:

1. concept or reference fidelity;
2. terrain topology;
3. gameplay readability and traversal;
4. architecture-ground contact;
5. material finish and scale;
6. vegetation ecosystem;
7. composition and depth;
8. lighting and atmosphere;
9. cultural and biome coherence;
10. 360-degree continuity;
11. collision and boundary integrity;
12. performance and streaming viability.

Advance only when every applicable category is at least 4. Do not hide a failing category inside an average.

## Independent acceptance rule

When agent delegation is available, the builder must not close the golden-slice or full-level gate from self-review alone. Use the read-only supervisor contract in [independent-visual-supervision.md](independent-visual-supervision.md).

The supervisor must judge raw fixed-camera evidence against the selected reference, change scores only when visible evidence supports the change, and return hard failures, per-camera blockers, the weakest system, one next change, and a verdict.

A focused target `PASS` closes only that target. It does not clear unresolved full-level hard failures. Preserve failed and superseded audits as history.

When delegation is unavailable, label the result `self-review; not independently supervised`. Never describe it as an independent verdict.

## Hard failures

Any one of these blocks completion:

- a wholly planar outdoor playable surface without an explicit planar brief;
- visible floor or Landscape edges, world voids, or unfinished reserve terrain;
- raw box foundations, floating corners, buried entrances, or buildings dropped on slopes;
- rectangular water seams, vertical terrain cuts, or unshaped banks;
- visible placeholders, default materials, stretched UVs, or contradictory texture scale;
- perimeter rings, uniform scatter, obvious tiling, or repeated hero assets without variation;
- floating roots, vegetation through water or hardscape, or impossible ecological placement;
- oversized rocks used as mountains or wedged into cultural walls without geological logic;
- empty reverse sides, exposed diorama backs, or a hero-only quality distribution;
- deleting a visually appropriate placed asset merely to avoid fixing its collision;
- blocked primary routes, unreliable collision closure, or failed capsule clearance;
- a representative frame materially below the selected quality reference;
- warnings, memory, streaming, or frame cost that make the intended scene unusable.

## Evidence-based repair loop

For each failed gate:

1. name the weakest category and its visible symptom;
2. identify the likely system-level cause;
3. record a fixed-camera baseline;
4. change one major variable;
5. capture the same camera and test the same route;
6. keep or revert the change based on evidence;
7. record the transferable lesson.

Actor count is useful for detecting missing batches or duplicates. It is never proof of quality.
