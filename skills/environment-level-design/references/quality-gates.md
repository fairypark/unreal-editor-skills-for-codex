# Environment Quality Gates

Use these gates for both construction and review. Numerical checks support visual judgment; they do not excuse a level that still reads as flat, empty, repetitive, unfinished, or below the selected reference.

## Gate A — Concept and scope

Pass only when:

- one primary concept or reference direction is selected;
- arrival, hero, route, and reverse views are represented;
- each required view has an observable frame contract covering normalized
  anchors, spatial relations, depth layers, value hierarchy, horizon target
  and tolerance, primary-mass occupancy, maximum unarticulated area, and hard
  blockers;
- a frame-contract overlay can be generated for each fixed comparison camera;
- route, focal hierarchy, enclosure, terrain silhouette, architecture vocabulary, vegetation strata, material palette, atmosphere, and prohibited motifs are written down;
- the concept is feasible with available assets, systems, time, and performance budget;
- construction provenance is explicit.

Stop if the design depends on unavailable capabilities. Obtain suitable assets, revise the concept, or reduce scope before building.

Frame-contract limits are diagnostic constraints, not automatic beauty scores.
Do not loosen them after seeing a weak build merely to manufacture a pass.

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

For every acceptance image, preserve a paired evidence receipt that binds the
camera role and persistent camera identity, world, transform, complete camera
view and post-process state, FOV, pixel dimensions, file byte count, SHA-256,
capture start and end, file modification time, UI-clean state, and temporal,
streaming, asset-compilation, and shader-compilation settlement. Preserve the
capture-returned PNG and receipt hashes outside those files and pass them as
trust anchors when re-running the handoff verifier immediately before
independent review. An existing filename without a matching receipt and
successful handoff-time verification is not evidence.

For golden-slice and full-level promotion, use a reusable Movie Render Queue or
Movie Render Graph beauty-evidence configuration when available. Rendering
selected persistent cameras is not enough by itself: enable
`Render Warm Up Frames` so engine warm-up frames are submitted to the GPU.
Record the configuration asset and output paths. Keep Object ID and other
diagnostic passes separate; they cannot substitute for beauty evidence.

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

## Complete decision package

Before claiming any aspirational, benchmark, golden-slice, or full-level gate,
create one project-owned quality-run manifest that links:

- the exact recipe, stage audit, and golden-slice brief;
- the append-only visual iteration history, including macro-composition IDs,
  consecutive verdicts, and documented reset evidence;
- every procedural pattern card required for that decision;
- the persistent-camera evidence, paired receipts, and external PNG/receipt
  hash trust anchors;
- the reusable MRQ/MRG beauty-render configuration;
- the research-freshness policy;
- the exact read-only independent evaluator role.

Run one project-owned validator over the complete package. Its result must
distinguish:

- `GO`: visual, procedural, evidence, render, and package gates all pass;
- `NO-GO`: the visual verdict or a procedural scope blocks promotion;
- `PENDING_RUNTIME`: the authoring package is structurally valid but the
  independent visual audit, trusted runtime evidence, sanitized handoff, or
  render configuration remains incomplete;
- `INVALID`: the package contradicts its schema, stage, paths, or child
  artifacts.

Do not assemble a favorable completion claim from several individually passing
commands when the complete decision package has not returned `GO`.

A project initializer may generate overlays, a stage brief, and a Quality Run
from a validated recipe and frame contract. It must begin at
`PENDING_RUNTIME`, refuse overwrites, and never manufacture an audit, evidence
hash, camera transform, or passing verdict. Concept-ready cameras may remain
unplaced; the aspirational camera becomes mandatory at
`aspirational_frame_ready`, and all required persistent cameras become
mandatory for later promotion states.

Every independent stage decision must append one immutable audit reference to
the visual iteration history. When one macro composition reaches the recipe's
consecutive `NO-GO` threshold, the complete package remains `NO-GO` even if a
local target later passes. Clear the blocker only with
`composition_reset=true`, a new macro-composition ID, and new concept,
contract, or blockout evidence. Fog, foliage, props, lighting, and contact
dressing are not composition resets.

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
