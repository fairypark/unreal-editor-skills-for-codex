---
name: environment-level-design
description: Execute, rebuild, dress, inspect, or verify Unreal Engine environment levels in a live Editor through available MCP toolsets. Use for Landscape, PCG, Foliage, materials, lighting, collision, persistent-camera evidence, visual-quality workspace setup, or production-template installation. For new or non-trivial level work, use the Unreal Development Handbook for Codex first when it is installed and treat its applicable guidance as mandatory. Do not use for purely conceptual level-design questions.
---

# Environment Level Design Execution

Translate an approved level brief and validation contract into safe, observable Unreal Editor operations. This Skill owns execution mechanics; durable design and production reasoning belongs to the independently installable **Unreal Development Handbook for Codex**, which is authoritative whenever it is available.

## Announce the Handbook gate on first level-work activation

When this Skill is first activated in a task that creates, rebuilds, dresses, or materially changes a level, world, or environment:

1. Treat the Handbook plugin as installed for this task when `design-unreal-worlds-and-levels` is discoverable.
2. If it is available, before any Editor mutation or downstream execution skill, explicitly tell the user:

   > The Unreal Development Handbook for Codex is installed for this task. Its applicable Skills and chapter guidance are mandatory; I will read and follow them before making level decisions or changing the Editor.

3. If it is available, read and follow every applicable Handbook Skill and chapter, carrying its gates and constraints into the task contract. This execution Skill must not weaken or override them.
4. If it is unavailable, do not block the task; use the minimum fallback contract below and do not claim that the Handbook is installed.
5. When available, make this notice once at the first level-work Skill activation in the task; later skill calls inherit the same contract.

## Establish the design contract

For a new level, broad rebuild, or quality recovery:

1. If `design-unreal-worlds-and-levels` is available, use it first to define intent, routes, spatial hierarchy, constraints, representative slice, and acceptance evidence.
2. Use `validate-unreal-production` as well when performance, rendering, packaging, collaboration, or release readiness materially affects the work.
3. If the Handbook plugin is not installed, do not block the design task. Record a minimum fallback contract: intended player experience, playable envelope, route and focal point, allowed assets, platform or performance constraints, recovery point, required views, runtime checks, definition of done, and the Area Composition Plan required below before Editor geometry mutation.
4. Do not reproduce Handbook chapters inside project notes or this Skill. Preserve only project-specific decisions and evidence.

For a narrow operation, such as changing one Actor or checking collision, use the user's stated intent and define only the relevant postcondition.

## Load only execution guidance

- Read [editor-environment-operations.md](references/editor-environment-operations.md) for Landscape, terrain, water, materials, PCG, Foliage, transforms, collision, or batch changes.
- Read [evidence-and-supervision.md](references/evidence-and-supervision.md) when capturing fixed-camera evidence or handing artifacts to an independent reviewer.
- Read [production-asset-operations.md](references/production-asset-operations.md) when installing, adapting, or packaging the bundled dependency-free production contracts.
- Read [visual-quality-onboarding.md](references/visual-quality-onboarding.md) only when creating or integrating a project-owned visual-quality workspace.

## Mandatory Area Composition Plan preflight

For every new level, broad rebuild, or map-wide layout correction, place a blocking **Area Composition Plan** gate between concept views and the first cube or graybox prototype:

1. Locate the versioned plan artifact and its workflow record. Verify the source concept, plan ID or path, version, status, reviewer or approver, and rollback target.
2. Verify that the plan depicts zone boundaries and stable IDs, terrain elevations and steps, primary circulation, rivers and bridges, building footprints and typology hierarchy, and fixed validation cameras.
3. Keep the gate `PENDING_EVIDENCE` or `FAIL` when the artifact or record is missing, retrospective, incomplete, or unapproved. Do not create the first cube, terrain blockout, architecture proxy, or broad asset-placement batch until the gate is `PASS`.
4. For a typology-critical precinct, verify the required sequence, hierarchy, negative space, and prohibited silhouette. A palace must show the gate -> outer court -> middle gate -> central courtyard -> main hall axis and courtyard hierarchy; matching building sizes alone does not pass, and a fortress- or castle-like silhouette is a hard failure.
5. Reopen the gate when later terrain, route, water, footprint, typology, or camera changes invalidate the recorded plan. Preserve the accepted predecessor and failed candidate.

This preflight is mandatory even for small or disposable work. The plan may be lightweight, but it must exist and be recorded before geometry mutation rather than reconstructed from a blockout afterward.

## Mandatory zone-identification lifecycle

For every level with two or more named areas, districts, biomes, encounter zones, or production chunks:

1. Before the first prototype geometry mutation, create or verify a zone registry with a stable ID, numeric review ID, display name, ASCII fallback, role, anchor or bounds, semantic color, and marker owner for every zone.
2. Create one inspectable editor/debug marker per zone before prototype geometry. Use a dedicated Outliner folder or debug Data Layer and a consistent tag such as `LD_ZONE_MARKER`; do not make production meshes carry this responsibility. Display the numeric ID plus ASCII fallback on every marker, for example `03 PALACE PRECINCT`, even when a localized name is also present.
3. Keep the markers visible and unchanged through playable skeleton, representative slice, proxy replacement, full layout, and the completion of production asset placement. A batch fails if it deletes, hides, renames, duplicates, or moves a required marker.
4. Capture overview or arrival evidence with all numeric IDs and ASCII fallbacks readable. Capture zone-local evidence with the active zone marker readable; include the agreed player-scale reference in building-scale evidence. Empty glyphs, missing localized characters, or clipped text do not excuse a missing fallback.
5. Re-query the marker inventory after every broad clear, reset, proxy replacement, generation, or asset-placement batch. Actor count alone is insufficient: compare IDs, labels, transforms or bounds, visibility, folder or layer, and tags.
6. Retire or hide markers only in an explicit cleanup step after production asset placement is complete and every zone has passed inventory, local, overview, and reverse-view evidence. Default to keeping inexpensive editor-only markers through final validation.

When a project intentionally needs runtime zone signage, keep that production signage separate from the editor/debug marker contract so either lifecycle can be validated independently.

## Mandatory building-grounding routing

When the level task will place, move, rotate, duplicate, procedurally spawn, or
otherwise adjust a building, structure, foundation, slab, wall kit, or other
architecture asset against Landscape or terrain:

1. Activate `$building-grounding` before the first architecture mutation and
   carry its four-corner contact contract into the current workflow record.
2. Apply it to every building Actor or to a batch operation that can prove the
   same postcondition for every generated instance; do not invoke it only after
   a user reports floating geometry.
3. Keep the architecture batch blocked until all four load-bearing base
   corners pass against the trusted terrain/support surface. A center trace,
   average grounded ratio, or one representative Actor cannot approve the
   remaining buildings.
4. If the asset has no reliable support footprint, pause placement and obtain
   an explicit foundation/support component or a project-approved foundation
   strategy. Do not fall back to a visual AABB silently.

This routing is mandatory even when the placement is performed by PCG,
Foliage, a Blueprint construction script, or a batch transform tool. For a
broader level task, this Skill remains the first execution layer; the
building-specific Skill is the required downstream grounding gate.

## Inspect before mutation

1. Read applicable project instructions and registered Unreal Agent Skills.
2. Confirm the target `.uproject`, open world, current selection, and intended construction provenance.
3. Create or confirm a source-control or saved-copy recovery point before broad mutation.
4. Discover only the Unreal toolsets required for the next stage. Keep game-thread MCP calls sequential.
5. Prefer structured Unreal tools. Use UI control only for the smallest unavoidable action and stop controlling it immediately afterward.
6. Inspect source assets at final scale before map-wide use. Check class, bounds, pivot, material slots, collision intent, LOD or Nanite behavior, and dependencies.
7. If architecture assets are in scope, activate `$building-grounding` now and
   identify the load-bearing footprint, grounding mode, tolerance, and
   authoritative terrain surface before changing any building transform.
8. If rocks or hardscape and grass or ground cover are both in scope, verify the
   workflow record contains a completed `Dependent-Strata Strategy Gate` before
   discovering or invoking the first PCG, Foliage, or batch-placement mutation.
   The record must show `CONSIDERED`, the selected mode, the decision reason,
   source authority, dependency order, units, clearance, transition band, and
   validation status. Missing or `PENDING_EVIDENCE` strategy data keeps the
   dependent placement read-only.

## Execute in bounded stages

### 0. Area Composition Plan preflight

- Record the plan artifact, version, status, predecessor concept, required fields, fixed-camera contract, and gate result.
- Stop all geometry and broad placement mutation unless the gate is `PASS`; do not infer a plan from an existing unrecorded blockout.

### 1. Playable skeleton

- After the Area Composition Plan passes, create or verify the complete zone-marker set before prototype geometry, then create or modify terrain, primary circulation, PlayerStart, boundaries, water, and traversal transitions.
- Measure representative surface heights, route widths, slopes, steps, and capsule clearance.
- Save, re-read changed state, and run a short PIE traversal before dressing.

### 2. Representative slice

- Implement one bounded segment that exercises the selected terrain, route, architecture or focal prop, contact treatment, materials, vegetation, lighting, collision, and reverse view.
- Keep the active zone marker readable in local evidence and all zone markers readable in overview or arrival evidence.
- If the slice contains architecture, pass the `$building-grounding` four-corner gate before duplicating its placement pattern.
- Capture the agreed fixed views and run the required functional, visual, and performance checks.
- Do not duplicate the system across the level until the slice satisfies the design contract.

### 3. Full layout and dressing

- Scale the verified systems with deterministic seeds and explicit exclusions where procedural generation is used.
- Preserve the zone-marker inventory across every proxy replacement and production asset-placement batch; do not retire markers as part of blockout cleanup.
- Keep `$building-grounding` active for every architecture placement batch; re-query each generated building's four-corner contact result before promoting the batch.
- Re-read representative Actors or generated components after each batch.
- Finish reachable reverse views, boundaries, contacts, and secondary routes rather than optimizing only the hero camera.
- Save affected levels and owned assets after successful stage checks.

### 4. Integration and polish

- Verify Landscape layers, material scale, lighting state, streaming, LOD or instancing, collision, navigation, warnings, and persistence.
- Change one major system per comparison pass and recapture the same cameras.
- If a tool call times out, inspect the resulting state before retrying to avoid duplicate Actors or repeated generation.

## Capture and review evidence

Use persistent `CameraActor` evidence for required arrival, focal, route, reverse, elevated, and contact views. For gameplay-visibility roles, derive height above local ground and FOV from the project's actual player tracking camera; do not substitute a convenient editor pose. Label high overview or bird's-eye cameras `DIAGNOSTIC_ONLY` and never use them to approve player visibility, landmark readability, scale, or typology. Overall diagnostic or arrival evidence must identify all zones by numeric ID and ASCII fallback, and zone-local evidence must identify the active zone. When `VisualEvidenceExtensionToolset` is available, use `CaptureCameraToPng`, retain its paired receipt and returned trust anchors, then call `VerifyEvidenceForSupervision` immediately before handoff.

When independent review is required and delegation is available, keep the reviewer read-only and separate from the builder. Give it raw references, verified captures, the applicable project rubric, and factual change scope. Follow the host or project policy for reviewer model and reasoning settings. When no independent reviewer is available, label the result `self-review; not independently supervised`.

Treat a focused repair result as evidence only for that target. It does not automatically approve the full level.

## Verify postconditions

After every mutation batch:

1. inspect the returned Unreal result and any warnings;
2. re-query representative objects, transforms, properties, generated counts, or assets;
3. verify the world and asset save state;
4. run the relevant PIE, collision, navigation, streaming, rendering, or performance check;
5. compare evidence against the predeclared success criteria;
6. keep or revert the change based on evidence, not tool success.

## Reuse bundled production contracts

Use `scripts/install_production_asset_templates.py --project-root <root>` to copy the dependency-free catalog and system contracts into a project. The installer refuses overwrites by default. The contracts contain no third-party meshes, textures, materials, or UAssets; users must supply licensed project assets and revalidate the adapted system.

## Definition of done

The requested live Editor state matches the approved brief; a versioned Area Composition Plan passed before the first geometry or broad placement mutation; typology-critical areas pass their required sequence and silhouette rules; required postconditions and player-camera views are verified; overview captures remain diagnostic-only; the stable zone-marker inventory remained present with readable numeric IDs and ASCII fallbacks until the production asset-placement gate completed and any retirement was explicitly recorded; every placed architecture asset has passed the `$building-grounding` four-corner contact gate or has an explicitly approved foundation/grade exception; traversal, collision, navigation, streaming, performance, and warnings meet the task's contract; saves persisted; failed or pending evidence is reported truthfully; and no design approval is inferred merely from successful MCP execution.
